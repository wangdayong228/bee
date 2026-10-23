# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: accounts.spec.ts >> 双入口、检测登录和详情分别表达能力、市场与额度时效
- Location: tests/accounts.spec.ts:8:1

# Error details

```
Error: locator.click: Target page, context or browser has been closed
Browser logs:

<launching> /home/runner/.cache/ms-playwright/firefox-1543/firefox/firefox -no-remote -headless -profile /tmp/playwright_firefoxdev_profile-D1Ie6x -juggler-pipe -silent
<launched> pid=23100
[pid=23100][err] [23102] Sandbox: CanCreateUserNamespace() unshare(CLONE_NEWPID): EPERM
[pid=23100][err] *** You are running in headless mode.
[pid=23100][err] JavaScript warning: resource://services-settings/Utils.sys.mjs, line 125: unreachable code after return statement
[pid=23100][out] 
[pid=23100][out] Juggler listening to the pipe
[pid=23100][out] console.warn: services.settings: #fetchAttachment: Forcing fallbackToDump to false due to Utils.LOAD_DUMPS being false
[pid=23100][out] console.error: (new NotFoundError("Could not find fa0fc42c-d91d-fca7-34eb-806ff46062dc in cache or dump", "resource://services-settings/Attachments.sys.mjs", 48))
[pid=23100][out] console.warn: "Unable to find the attachment for" "fa0fc42c-d91d-fca7-34eb-806ff46062dc"
[pid=23100][err] JavaScript error: , line 0: SyntaxError: JSON.parse: unexpected end of data at line 1 column 1 of the JSON data
[pid=23100][out] console.error: services.settings: 
[pid=23100][out]   Message: EmptyDatabaseError: "main/nimbus-desktop-experiments" has not been synced yet
[pid=23100][out]   Stack:
[pid=23100][out]     EmptyDatabaseError@resource://services-settings/Database.sys.mjs:19:5
[pid=23100][out] list@resource://services-settings/Database.sys.mjs:96:13
[pid=23100][out] 
[pid=23100][err] Exiting due to channel error.
Call log:
  - waiting for getByRole('button', { name: '概览', exact: true })
    - locator resolved to <button>…</button>
  - attempting click action
    - waiting for element to be visible, enabled and stable
    - element is visible, enabled and stable
    - scrolling into view if needed
    - done scrolling
    - performing click action

```