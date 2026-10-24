//! Desktop window decisions; native adapters are deliberately kept outside the policy.
use std::sync::atomic::{AtomicBool, Ordering};

pub const CALLBACK_SCHEME: &str = "tokhive-bee-dev";

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum WindowIntent {
    Show,
    Hide,
    Quit,
}

#[derive(Clone, Copy, Debug)]
pub enum WindowEvent {
    CloseRequested,
    SecondLaunch,
    Reopen,
    Menu(WindowIntent),
}

pub fn intent_for(event: WindowEvent) -> WindowIntent {
    match event {
        WindowEvent::CloseRequested => WindowIntent::Hide,
        WindowEvent::SecondLaunch | WindowEvent::Reopen => WindowIntent::Show,
        WindowEvent::Menu(intent) => intent,
    }
}

#[derive(Default)]
pub struct LoginReceipt(AtomicBool);

impl LoginReceipt {
    pub fn receive(&self, url: &str) -> bool {
        let accepted = url.split_once(':').is_some_and(|(scheme, rest)| {
            scheme.eq_ignore_ascii_case(CALLBACK_SCHEME) && !rest.is_empty()
        });
        if accepted {
            self.0.store(true, Ordering::Release);
        }
        accepted
    }

    pub fn received(&self) -> bool {
        self.0.load(Ordering::Acquire)
    }
}

#[cfg(test)]
#[path = "lifecycle_tests.rs"]
mod tests;

use tauri::{Emitter, Manager};

#[tauri::command]
pub fn login_return_received(receipt: tauri::State<'_, LoginReceipt>) -> bool {
    receipt.received()
}

pub fn deliver_callback(app: &tauri::AppHandle, url: &str) {
    if app.state::<LoginReceipt>().receive(url) {
        if let Err(cause) = app.emit_to("main", "bee://login-return", true) {
            eprintln!("deliver Bee login-return boolean receipt to main window: {cause}");
        }
        dispatch(app, WindowEvent::Reopen);
    }
}

pub fn dispatch(app: &tauri::AppHandle, event: WindowEvent) {
    qa_trace(app, &format!("dispatch.before event={event:?}"));
    let intent = intent_for(event);
    if let Err(cause) = apply(app, intent) {
        qa_trace(app, &format!("dispatch.error intent={intent:?} cause={cause}"));
        eprintln!("apply Bee main window intent={intent:?}: {cause}");
    }
    qa_trace(app, &format!("dispatch.after event={event:?}"));
}

fn apply(app: &tauri::AppHandle, intent: WindowIntent) -> tauri::Result<()> {
    if intent == WindowIntent::Quit {
        // RunEvent::Exit performs the existing owned Child stop-and-reap path.
        app.exit(0);
        return Ok(());
    }
    // A second launch can arrive while setup is still creating the main window.
    // That window is initially visible; receipt state is already managed above setup.
    let Some(window) = app.get_webview_window("main") else {
        return Ok(());
    };
    match intent {
        WindowIntent::Show => {
            window.show()?;
            window.unminimize()?;
            window.set_focus()?;
        }
        WindowIntent::Hide => window.hide()?,
        WindowIntent::Quit => unreachable!(),
    }
    Ok(())
}

pub fn install_menu_and_tray(app: &mut tauri::App) -> tauri::Result<()> {
    use tauri::menu::{Menu, MenuItem, Submenu};
    let open = MenuItem::with_id(app, "bee-open", "打开 Bee", true, Some("CmdOrCtrl+O"))?;
    let quit = MenuItem::with_id(app, "bee-quit", "退出", true, Some("CmdOrCtrl+Q"))?;
    let app_menu = Submenu::with_items(app, "Bee", true, &[&open, &quit])?;
    app.set_menu(Menu::with_items(app, &[&app_menu])?)?;
    app.on_menu_event(|app, event| match event.id().as_ref() {
        "bee-open" => dispatch(app, WindowEvent::Menu(WindowIntent::Show)),
        "bee-quit" => dispatch(app, WindowEvent::Menu(WindowIntent::Quit)),
        _ => {}
    });
    let tray_menu = Menu::with_items(app, &[&open, &quit])?;
    let mut tray = tauri::tray::TrayIconBuilder::with_id("bee")
        .tooltip("Bee")
        .menu(&tray_menu)
        .show_menu_on_left_click(true);
    if let Some(icon) = app.default_window_icon() {
        tray = tray.icon(icon.clone());
    }
    // A desktop can have no notification area. Single-instance relaunch and the
    // macOS dock reopen remain available, so tray absence must not abort startup.
    let tray_result = tray.build(app);
    qa_trace(app.handle(), &format!("tray.build success={}", tray_result.is_ok()));
    if let Err(cause) = tray_result {
        eprintln!(
            "create Bee tray icon failed; recover the window by launching Bee again: {cause}"
        );
    }
    Ok(())
}

pub async fn shutdown_owned(
    bridge: &crate::sidecar::Bridge,
    release_instance: impl FnOnce(),
) -> Result<(), crate::protocol::BridgeError> {
    bridge.stop().await?;
    release_instance();
    Ok(())
}

// Temporary QA-only trace. Observes the same Tauri window API; performs no UI actions.
pub fn qa_trace(app: &tauri::AppHandle, event: &str) {
    use std::io::Write;
    static SEQ: std::sync::atomic::AtomicU64 = std::sync::atomic::AtomicU64::new(0);
    let seq = SEQ.fetch_add(1, Ordering::SeqCst);
    let now = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_millis();
    let state = app.get_webview_window("main").map(|w| format!("visible={:?} minimized={:?} focused={:?}", w.is_visible(), w.is_minimized(), w.is_focused()));
    let record = format!("ms={now} seq={seq} pid={} event={event} state={state:?}\n", std::process::id());
    let mut file = std::fs::OpenOptions::new().create(true).append(true).open(TRACE_PATH).expect("open temporary QA lifecycle trace");
    file.write_all(record.as_bytes()).expect("append temporary QA lifecycle trace");
}

const TRACE_PATH: &str = "/Users/dayong/myspace/mywork/tokenhive/.worktrees/bee-desktop-p0/.cache/qa/2026-10-24-mac-lifecycle-diagnostic/runtime.log";
