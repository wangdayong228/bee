# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: settings-diagnostics.spec.ts >> 英文异步失败/未确认/空/加载场景及弹层无漏译
- Location: tests/settings-diagnostics.spec.ts:296:1

# Error details

```
Error: expect(received).toEqual(expected) // deep equality

- Expected  - 1
+ Received  + 3

- Array []
+ Array [
+   "划转结果未确认",
+ ]
```

# Page snapshot

```yaml
- generic [ref=f15e3]:
  - complementary [ref=f15e4]:
    - generic [ref=f15e5]: Bee
    - navigation "Main navigation" [ref=f15e7]:
      - button "Overview" [ref=f15e8] [cursor=pointer]
      - button "AI accounts" [ref=f15e14] [cursor=pointer]
      - button "Earnings" [ref=f15e20] [cursor=pointer]
      - button "Diagnostics" [ref=f15e25] [cursor=pointer]
      - button "Settings" [ref=f15e28] [cursor=pointer]
    - generic [ref=f15e32]:
      - generic [ref=f15e33]:
        - text: Real supply is not connected
        - paragraph [ref=f15e35]: Reopen from the tray after closing
      - generic [ref=f15e36]:
        - generic [ref=f15e37]: B
        - generic [ref=f15e38]:
          - text: Bee Desktop
          - generic [ref=f15e39]: Local demo workspace
  - generic [ref=f15e40]:
    - banner [ref=f15e41]:
      - generic [ref=f15e42]:
        - generic [ref=f15e43]: Workspace
        - generic [ref=f15e46]: Earnings
      - generic [ref=f15e47]:
        - generic [ref=f15e48]: This device
        - generic [ref=f15e53]: Demo data
    - main [ref=f15e54]:
      - generic [ref=f15e55]:
        - generic [ref=f15e56]:
          - heading "Earnings" [level=1] [ref=f15e57]
          - paragraph [ref=f15e58]: View contribution earnings and available balance.
        - generic [ref=f15e59]:
          - text: Demo scene
          - combobox "Demo scene" [ref=f15e60]:
            - option "Lifecycle failure"
            - option "Lifecycle result unknown"
            - option "Lifecycle pending"
            - option "ready"
            - option "diagnostics-partial"
            - option "diagnostics-export-error"
            - option "earnings-loading"
            - option "earnings-error"
            - option "earnings-empty"
            - option "quote-conflict"
            - option "quote-unknown"
            - option "transfer-pending"
            - option "transfer-unknown" [selected]
            - option "authorization-expired"
            - option "account-change"
            - option "quota-unknown"
            - option "removal-pending"
            - option "removal-unknown"
            - option "loading"
            - option "empty"
            - option "error"
            - option "unknown-tasks"
            - option "active-tasks"
            - option "tasks-loading"
            - option "tasks-error"
            - option "onboarding"
            - option "configured"
            - option "external"
            - option "offline"
            - option "unknown"
            - option "partial"
            - option "pending"
            - option "unknown-result"
            - option "operation-error"
      - generic [ref=f15e61]:
        - button "Back to earnings" [ref=f15e62] [cursor=pointer]
        - generic [ref=f15e64]:
          - heading "Transfer to buyer balance" [level=2] [ref=f15e65]
          - paragraph [ref=f15e66]: Transfer within the same Hive account · Demo data
        - generic [ref=f15e67]:
          - generic [ref=f15e68]:
            - generic [ref=f15e69]:
              - generic [ref=f15e70]: Available earnings
              - strong [ref=f15e71]: $128.56
            - generic [ref=f15e72]:
              - generic [ref=f15e73]: Buyer balance
              - strong [ref=f15e74]: $24.6
            - generic [ref=f15e75]:
              - generic [ref=f15e76]: Destination account
              - strong [ref=f15e77]: demo-user · Current account
          - generic [ref=f15e78]:
            - generic [ref=f15e79]:
              - generic [ref=f15e80]: Transfer amount
              - button "All earnings" [disabled] [ref=f15e81]
            - textbox "Transfer amount" [disabled] [ref=f15e82]: "1"
            - generic [ref=f15e83]: Amounts are in USD, with up to 9 decimal places. Transfers cannot be reversed after completion.
          - status [ref=f15e84]: "Demo only: 划转结果未确认, Original requestId=5cba0ce7-e66f-44d4-861a-35d131332da4; Only the original operation can be checked."
          - paragraph [ref=f15e85]: Result unconfirmed · requestId=5cba0ce7-e66f-44d4-861a-35d131332da4 · Original amount 1
          - generic [ref=f15e86]:
            - button "Refresh original operation" [ref=f15e87] [cursor=pointer]
            - button "Check original operation" [ref=f15e88] [cursor=pointer]
      - region "Demo lifecycle" [ref=f15e89]:
        - generic [ref=f15e90]:
          - button "Exit demo" [ref=f15e91] [cursor=pointer]
          - button "Update demo" [ref=f15e92] [cursor=pointer]
        - paragraph [ref=f15e93]: Closing the window keeps Bee running; preview exit and update flows here.
    - contentinfo [ref=f15e94]:
      - text: Bee · Development build
      - generic [ref=f15e95]: Demo actions do not affect real accounts or funds
```

# Test source

```ts
  225 |   await page.goto('/'); await nav(page, '设置');
  226 |   await page.getByLabel('外观', { exact: true }).selectOption('dark');
  227 |   await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
  228 |   await page.emulateMedia({ colorScheme: 'light' });
  229 |   expect(await page.locator('html').evaluate(e => getComputedStyle(e).getPropertyValue('--paper').trim())).toBe('#222426');
  230 |   await page.getByLabel('外观', { exact: true }).selectOption('light');
  231 |   await expect(page.locator('html')).toHaveAttribute('data-theme', 'light');
  232 |   await page.emulateMedia({ colorScheme: 'dark' });
  233 |   expect(await page.locator('html').evaluate(e => getComputedStyle(e).getPropertyValue('--paper').trim())).toBe('#ffffff');
  234 |   await page.getByLabel('语言', { exact: true }).focus();
  235 |   await page.keyboard.press('Tab');
  236 |   const outline = await page.locator(':focus').evaluate(e => getComputedStyle(e).outlineWidth);
  237 |   expect(outline).toBe('2px');
  238 |   await page.getByLabel('代理地址', { exact: true }).fill('socks5://localhost:1080');
  239 |   await page.getByRole('button', { name: '保存代理', exact: true }).click();
  240 |   await expect(page.getByRole('status')).toContainText('未修改系统代理');
  241 |   await page.reload(); await nav(page, '设置');
  242 |   await expect(page.getByLabel('代理地址', { exact: true })).toHaveValue('socks5://localhost:1080');
  243 |   await page.evaluate(() => { Object.defineProperty(navigator, 'language', { configurable: true, value: 'en-US' }); window.dispatchEvent(new Event('languagechange')); });
  244 |   await expect(page.getByRole('heading', { name: 'Settings', exact: true })).toBeVisible();
  245 |   await page.getByLabel('Language', { exact: true }).selectOption('zh');
  246 |   await expect(page.getByRole('heading', { name: '设置', exact: true })).toBeVisible();
  247 | });
  248 | 
  249 | test('通知四类问题均去重，普通短暂离线不伪称持续离线', async ({ page }) => {
  250 |   await page.goto('/');
  251 |   const result = await page.evaluate(async () => {
  252 |     const { createDemoClient } = await import(/* @vite-ignore */ String('/src/client/demo.ts'));
  253 |     const { notificationIssues } = await import(/* @vite-ignore */ String('/src/features/settings/notifications.ts'));
  254 |     const onboarding = await createDemoClient('onboarding').snapshot();
  255 |     const transient = notificationIssues(onboarding);
  256 |     const state = await createDemoClient('ready').snapshot();
  257 |     state.accounts.value[0].authorization = 'expired'; state.accounts.value[0].pendingChange = { identifier: 'different' }; state.accounts.value[0].quota.remaining = 0;
  258 |     state.connection.value.state = 'disconnected'; state.connection.value.persistentOffline = true;
  259 |     return { transient, issues: notificationIssues(state) };
  260 |   });
  261 |   expect(result.transient).toEqual([]);
  262 |   expect(new Set(result.issues).size).toBe(4);
  263 | });
  264 | 
  265 | test('真实下载API失败保留错误证据并允许重试，不假称文件已交付', async ({ page }) => {
  266 |   await page.goto('/'); await nav(page, '诊断');
  267 |   await page.evaluate(() => { URL.createObjectURL = () => { throw new Error('blob-create-denied: test'); }; });
  268 |   await page.getByRole('button', { name: '导出脱敏报告', exact: true }).click();
  269 |   await expect(page.getByRole('status')).toContainText('blob-create-denied');
  270 |   await expect(page.getByRole('status')).toContainText('未确认完成');
  271 |   await expect(page.getByRole('button', { name: '导出脱敏报告', exact: true })).toBeEnabled();
  272 | });
  273 | 
  274 | test('损坏偏好或不安全的已选Hive读取失败时不借用旧登录，不回显秘密', async ({ page }) => {
  275 |   await page.goto('/');
  276 |   const result = await page.evaluate(async () => {
  277 |     const { createDemoClient } = await import(/* @vite-ignore */ String('/src/client/demo.ts'));
  278 |     const { savePreferences, defaultHive } = await import(/* @vite-ignore */ String('/src/features/settings/preferences.ts'));
  279 |     savePreferences(localStorage, { hive: defaultHive, user: 'demo-user' }, { theme: 'dark' });
  280 |     const key = Object.keys(localStorage).find(k => k.startsWith('bee.demo.preferences.'))!;
  281 |     localStorage.setItem(key, '{"token":"SECRET"');
  282 |     const corrupt = await createDemoClient('ready').snapshot();
  283 |     localStorage.removeItem(key);
  284 |     localStorage.setItem('bee.demo.selected-hive.v1', 'https://secret:password@hive.test');
  285 |     const unsafe = await createDemoClient('ready').snapshot();
  286 |     return { corrupt, unsafe };
  287 |   });
  288 |   for (const state of [result.corrupt, result.unsafe]) {
  289 |     expect.soft(state.binding.value.loggedIn).toBe(false);
  290 |     expect.soft(state.accounts.value).toEqual([]);
  291 |     expect(state.preferences.status).toBe('error');
  292 |     expect(state.preferences.error.message).not.toMatch(/SECRET|secret|password/);
  293 |   }
  294 | });
  295 | 
  296 | test('英文异步失败/未确认/空/加载场景及弹层无漏译', async ({ browser }) => {
  297 |   const context = await browser.newContext({ locale: 'en-US' });
  298 |   const page = await context.newPage();
  299 |   const check = async () => { expect(await page.locator('body').innerText()).not.toMatch(/[\u4e00-\u9fff]/); };
  300 |   for (const scene of ['onboarding', 'configured', 'loading', 'empty', 'error', 'offline', 'unknown', 'tasks-error', 'earnings-error', 'earnings-loading']) {
  301 |     await page.goto(`/?scene=${scene}`);
  302 |     await expect(page.getByRole('heading', { name: 'Overview', exact: true })).toBeVisible();
  303 |     await check();
  304 |     if (scene === 'configured') { await page.getByRole('button', { name: 'Bind this device', exact: true }).click(); await check(); await page.keyboard.press('Escape'); }
  305 |     if (['loading', 'error', 'empty'].includes(scene)) { await nav(page, 'AI accounts'); await check(); }
  306 |     if (scene.startsWith('earnings-')) { await nav(page, 'Earnings'); await check(); }
  307 |   }
  308 |   for (const scene of ['pending', 'unknown-result', 'operation-error']) {
  309 |     await page.goto(`/?scene=${scene}`);
  310 |     await page.getByRole('button', { name: 'Simulate login to Hive', exact: true }).click();
  311 |     await expect(page.getByRole('status')).not.toContainText('Processing demo action'); await check();
  312 |   }
  313 |   for (const scene of ['quote-conflict', 'quote-unknown']) {
  314 |     await page.goto(`/?scene=${scene}`); await nav(page, 'Earnings');
  315 |     await page.getByRole('button', { name: 'Pricing settings', exact: true }).click();
  316 |     await page.getByRole('button', { name: 'Save pricing', exact: true }).click();
  317 |     await expect(page.getByRole('alert')).toBeVisible(); await check();
  318 |   }
  319 |   await page.goto('/?scene=transfer-unknown'); await nav(page, 'Earnings');
  320 |   await page.getByRole('button', { name: 'Transfer to buyer balance', exact: true }).click();
  321 |   await page.getByLabel('Transfer amount', { exact: true }).fill('1');
  322 |   await page.getByRole('button', { name: 'Review transfer', exact: true }).click();
  323 |   await page.getByRole('button', { name: 'Confirm transfer', exact: true }).click();
  324 |   await expect(page.getByText('Result unconfirmed', { exact: false }).first()).toBeVisible(); await check();
> 325 |   expect(await page.evaluate(async () => [...(await import(/* @vite-ignore */ String('/src/i18n/index.ts'))).missingTranslations])).toEqual([]);
      |                                                                                                                                     ^ Error: expect(received).toEqual(expected) // deep equality
  326 |   await context.close();
  327 | });
  328 | 
  329 | test('浅深主题正文/次要文字/金色标签与焦点均具有足够对比', async ({ page }) => {
  330 |   await page.goto('/'); await nav(page, '设置');
  331 |   for (const theme of ['light', 'dark']) {
  332 |     await page.getByLabel('外观', { exact: true }).selectOption(theme);
  333 |     await expect(page.locator('html')).toHaveAttribute('data-theme', theme);
  334 |     const ratios = await page.locator('html').evaluate(root => {
  335 |       const css = getComputedStyle(root);
  336 |       const luminance = (hex: string) => {
  337 |         const color = hex.trim().replace('#', '');
  338 |         const channels = [0, 2, 4].map(i => parseInt(color.slice(i, i + 2), 16) / 255).map(v => v <= 0.04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4);
  339 |         return channels.reduce((sum, value, i) => sum + value * [.2126, .7152, .0722][i], 0);
  340 |       };
  341 |       const ratio = (a: string, b: string) => { const x = luminance(css.getPropertyValue(a)), y = luminance(css.getPropertyValue(b)); return (Math.max(x, y) + .05) / (Math.min(x, y) + .05); };
  342 |       return { text: ratio('--ink', '--paper'), muted: ratio('--muted', '--paper'), badge: ratio('--accent-ink', '--accent-soft'), focus: ratio('--accent', '--paper') };
  343 |     });
  344 |     expect(ratios.text).toBeGreaterThanOrEqual(4.5);
  345 |     expect(ratios.muted).toBeGreaterThanOrEqual(4.5);
  346 |     expect(ratios.badge).toBeGreaterThanOrEqual(4.5);
  347 |     expect(ratios.focus).toBeGreaterThanOrEqual(3);
  348 |   }
  349 | });
  350 | 
  351 | for (const fault of ['corrupt', 'read-error']) {
  352 |   test(`审查I1：非默认Hive登录偏好${fault}失败不提交身份或跨scope写入，可原位重试`, async ({ page }) => {
  353 |     await page.goto('/');
  354 |     const result = await page.evaluate(async (fault) => {
  355 |       const { createDemoClient } = await import(/* @vite-ignore */ String('/src/client/demo.ts'));
  356 |       const hive = 'https://scope-review.test';
  357 |       const key = `bee.demo.preferences.v1.${encodeURIComponent(JSON.stringify([hive, 'demo-user']))}`;
  358 |       const client = createDemoClient('ready');
  359 |       await client.dispatch({ type: 'changeHive', address: hive });
  360 |       localStorage.setItem(key, '{broken');
  361 |       const beforeStorage = JSON.stringify({ ...localStorage });
  362 |       const beforeSession = JSON.stringify({ ...sessionStorage });
  363 |       const get = Storage.prototype.getItem;
  364 |       Storage.prototype.getItem = function(k) { if (fault === 'read-error' && k === key) throw new Error('test user scope read unavailable'); return get.call(this, k); };
  365 |       let login;
  366 |       try { login = await client.dispatch({ type: 'loginHive' }); }
  367 |       finally { Storage.prototype.getItem = get; }
  368 |       const failed = await client.snapshot();
  369 |       const theme = await client.dispatch({ type: 'setPreference', preferences: { theme: 'dark' } });
  370 |       const proxy = await client.dispatch({ type: 'saveProxy', address: 'socks5://proxy.test' });
  371 |       const afterStorage = JSON.stringify({ ...localStorage });
  372 |       const afterSession = JSON.stringify({ ...sessionStorage });
  373 |       localStorage.removeItem(key);
  374 |       const retry = await client.dispatch({ type: 'loginHive' });
  375 |       await client.dispatch({ type: 'setPreference', preferences: { theme: 'dark' } });
  376 |       return { login, failed, theme, proxy, beforeStorage, afterStorage, beforeSession, afterSession, retry, restored: await client.snapshot(), saved: JSON.parse(localStorage.getItem(key)!) };
  377 |     }, fault);
  378 |     expect.soft(result.login.kind).toBe('failed');
  379 |     expect.soft(result.failed.binding.value.loggedIn).toBe(false);
  380 |     expect.soft(result.failed.preferences.value.hiveAddress).toBe('https://scope-review.test');
  381 |     expect.soft(result.failed.finance.value.identity.hive).toBe('https://scope-review.test');
  382 |     expect.soft(result.theme.kind).toBe('failed');
  383 |     expect.soft(result.proxy.kind).toBe('failed');
  384 |     expect.soft(result.afterStorage).toBe(result.beforeStorage);
  385 |     expect.soft(result.afterSession).toBe(result.beforeSession);
  386 |     expect(result.retry.kind).toBe('confirmed');
  387 |     expect(result.restored.finance.value.identity).toEqual({ hive: 'https://scope-review.test', user: 'demo-user' });
  388 |     expect(result.saved.theme).toBe('dark');
  389 |   });
  390 | }
  391 | 
  392 | test('审查I2：英文公共弹层只翻译一次，保留匹配词典的中文业务值', async ({ page }) => {
  393 |   await page.goto('/');
  394 |   await page.evaluate(async () => {
  395 |     const { default: React } = await import(/* @vite-ignore */ String('/node_modules/.vite/deps/react.js'));
  396 |     const { default: { createRoot } } = await import(/* @vite-ignore */ String('/node_modules/.vite/deps/react-dom_client.js'));
  397 |     const { useLanguage } = await import(/* @vite-ignore */ String('/src/i18n/index.ts'));
  398 |     const { AccountActions } = await import(/* @vite-ignore */ String('/src/features/accounts/AccountActions.tsx'));
  399 |     const { AccountDetails } = await import(/* @vite-ignore */ String('/src/features/accounts/AccountDetails.tsx'));
  400 |     const { createDemoClient } = await import(/* @vite-ignore */ String('/src/client/demo.ts'));
  401 |     const snapshot = await createDemoClient('ready').snapshot();
  402 |     const account = { ...snapshot.accounts.value[0], label: '收益', identifier: '收益', pendingChange: { identifier: '账号' } };
  403 |     function Harness() { useLanguage('en'); return React.createElement(React.Fragment, null, React.createElement(AccountActions, { platform: account.platform, account, busy: false, dispatch: async () => {} }), React.createElement(AccountDetails, { account })); }
  404 |     createRoot(document.getElementById('root')!).render(React.createElement(Harness));
  405 |   });
  406 |   await page.getByRole('button', { name: 'Confirm account change', exact: true }).click();
  407 |   await expect(page.getByRole('dialog')).toContainText('收益');
  408 |   await expect(page.getByRole('dialog')).toContainText('账号');
  409 |   await page.getByRole('button', { name: 'Cancel', exact: true }).click();
  410 |   await page.getByRole('button', { name: 'View details', exact: true }).click();
  411 |   await expect(page.getByRole('dialog').getByRole('heading', { level: 2 })).toContainText('收益');
  412 |   await expect(page.getByRole('button', { name: 'Close', exact: true })).toBeVisible();
  413 | });
  414 | 
```