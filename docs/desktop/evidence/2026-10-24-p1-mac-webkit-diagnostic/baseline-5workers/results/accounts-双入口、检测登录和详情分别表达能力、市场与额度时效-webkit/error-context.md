# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: accounts.spec.ts >> 双入口、检测登录和详情分别表达能力、市场与额度时效
- Location: tests/accounts.spec.ts:8:1

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: locator.click: Test timeout of 30000ms exceeded.
Call log:
  - waiting for getByRole('button', { name: '概览', exact: true })
    - locator resolved to <button>…</button>
  - attempting click action
    - waiting for element to be visible, enabled and stable

```

# Page snapshot

```yaml
- generic [ref=e3]:
  - complementary [ref=e4]:
    - generic [ref=e5]: Bee
    - navigation "主导航" [ref=e7]:
      - button "概览" [ref=e8] [cursor=pointer]
      - button "AI 账号" [ref=e14] [cursor=pointer]
      - button "收益" [ref=e20] [cursor=pointer]
      - button "诊断" [ref=e24] [cursor=pointer]
      - button "设置" [ref=e27] [cursor=pointer]
    - generic [ref=e31]:
      - generic [ref=e32]:
        - text: 尚未接通真实供给
        - paragraph [ref=e34]: 关窗后可从托盘找回
      - generic [ref=e35]:
        - generic [ref=e36]: B
        - generic [ref=e37]:
          - text: Bee 桌面端
          - generic [ref=e38]: 本地演示空间
  - generic [ref=e39]:
    - banner [ref=e40]:
      - generic [ref=e41]:
        - generic [ref=e42]: 工作空间
        - generic [ref=e45]: AI 账号
      - generic [ref=e46]:
        - generic [ref=e47]: 本机设备
        - generic [ref=e50]: 演示数据
    - main [ref=e51]:
      - generic [ref=e52]:
        - generic [ref=e53]:
          - heading "AI 账号" [level=1] [ref=e54]
          - paragraph [ref=e55]: 管理这台设备用于贡献的 AI 账号。
        - generic [ref=e56]:
          - text: 演示场景
          - combobox "演示场景" [ref=e57]:
            - option "lifecycle-failed"
            - option "lifecycle-unknown"
            - option "lifecycle-pending"
            - option "ready"
            - option "diagnostics-partial"
            - option "diagnostics-export-error"
            - option "earnings-loading"
            - option "earnings-error"
            - option "earnings-empty"
            - option "quote-conflict"
            - option "quote-unknown"
            - option "transfer-pending"
            - option "transfer-unknown"
            - option "authorization-expired"
            - option "account-change"
            - option "quota-unknown"
            - option "removal-pending"
            - option "removal-unknown"
            - option "loading"
            - option "empty" [selected]
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
      - paragraph [ref=e58]: 检测已有官方登录，或通过官方授权接入。接入与换号后保持暂停，由你决定何时贡献。
      - generic [ref=e59]:
        - region "OpenAI 账号" [ref=e60]:
          - generic [ref=e61]:
            - generic [ref=e62]:
              - generic [ref=e63]: O
              - heading "OpenAI" [level=2] [ref=e64]
            - generic [ref=e65]: 订阅套餐 Plus
          - paragraph [ref=e66]: dayong@example.com
          - paragraph [ref=e67]: 已接入 · 已暂停
          - paragraph [ref=e68]: 5 小时 · 剩余 82% · 2 小时后重置
          - button "查看详情" [active] [ref=e69] [cursor=pointer]
          - generic [ref=e70]:
            - button "检测已有登录" [ref=e71] [cursor=pointer]
            - button "官方授权接入" [ref=e72] [cursor=pointer]
            - button "移除账号" [ref=e73] [cursor=pointer]
        - region "Claude 账号" [ref=e74]:
          - generic [ref=e75]:
            - generic [ref=e76]:
              - generic [ref=e77]: ✳
              - heading "Claude" [level=2] [ref=e78]
            - generic [ref=e79]: 尚未接入
          - generic [ref=e80]:
            - button "检测已有登录" [ref=e81] [cursor=pointer]
            - button "官方授权接入" [ref=e82] [cursor=pointer]
            - button "接入账号" [ref=e83] [cursor=pointer]
      - paragraph [ref=e84]: 演示接入不会读取或修改官方客户端；官方授权尚未接通。
      - region "演示生命周期" [ref=e85]:
        - generic [ref=e86]:
          - button "退出演示" [ref=e87] [cursor=pointer]
          - button "更新演示" [ref=e88] [cursor=pointer]
        - paragraph [ref=e89]: 关窗继续后台运行；这里仅预览退出和更新流程。
      - status [ref=e90]: 仅演示：操作已完成，请查看每个平台的结果；不会控制真实供给。
    - contentinfo [ref=e91]:
      - text: Bee · 开发版本
      - generic [ref=e92]: 演示操作不会影响真实账号或资金
```

# Test source

```ts
  1   | import { expect, test } from '@playwright/test';
  2   | import type { Account } from '../src/client/types';
  3   | 
  4   | async function accounts(page: import('@playwright/test').Page, scene = 'ready') {
  5   |   await page.goto(`/?scene=${scene}`);
  6   |   await page.getByRole('navigation').getByRole('button', { name: 'AI 账号', exact: true }).click();
  7   | }
  8   | test('双入口、检测登录和详情分别表达能力、市场与额度时效', async ({ page }) => {
  9   |   await accounts(page, 'empty');
  10  |   const openai = page.getByRole('region', { name: 'OpenAI 账号' });
  11  |   await expect(openai.getByRole('button', { name: '官方授权接入' })).toBeVisible();
  12  |   await openai.getByRole('button', { name: '检测已有登录' }).click();
  13  |   await expect(openai).toContainText('dayong@example.com');
  14  |   await openai.getByRole('button', { name: '查看详情' }).click();
  15  |   const sheet = page.getByRole('dialog');
  16  |   await expect(sheet).toContainText('订阅套餐');
  17  |   await expect(sheet).toContainText('账号支持');
  18  |   await expect(sheet).toContainText('平台暂未开放');
  19  |   await expect(sheet).toContainText('更新时间');
  20  |   await page.keyboard.press('Escape');
> 21  |   await page.getByRole('button', { name: '概览', exact: true }).click();
      |                                                               ^ Error: locator.click: Test timeout of 30000ms exceeded.
  22  |   await expect(page.getByText('尚未开始贡献', { exact: true })).toBeVisible();
  23  | });
  24  | test('官方授权未接通，不伪造接入成功', async ({ page }) => {
  25  |   await accounts(page, 'empty');
  26  |   const openai = page.getByRole('region', { name: 'OpenAI 账号' });
  27  |   await openai.getByRole('button', { name: '官方授权接入' }).click();
  28  |   await expect(page.getByRole('status')).toContainText('官方授权尚未接通');
  29  |   await expect(openai).toContainText('尚未接入');
  30  | });
  31  | for (const scene of ['authorization-expired', 'quota-unknown']) {
  32  |   test(`${scene} 不伪造额度或可交易状态`, async ({ page }) => {
  33  |     await accounts(page, scene);
  34  |     await page
  35  |       .getByRole('region', { name: 'OpenAI 账号' })
  36  |       .getByRole('button', { name: '查看详情' })
  37  |       .click();
  38  |     const sheet = page.getByRole('dialog');
  39  |     await expect(sheet).toContainText(scene === 'quota-unknown' ? '额度未知' : '授权已失效');
  40  |     if (scene === 'authorization-expired') await expect(sheet).not.toContainText('可交易');
  41  |   });
  42  | }
  43  | test('换号明确旧新标识与影响，取消不变、确认保持暂停', async ({ page }) => {
  44  |   await accounts(page, 'account-change');
  45  |   const openai = page.getByRole('region', { name: 'OpenAI 账号' });
  46  |   await openai.getByRole('button', { name: '确认换号' }).click();
  47  |   await expect(page.getByRole('dialog')).toContainText('dayong@example.com');
  48  |   await expect(page.getByRole('dialog')).toContainText('another@example.com');
  49  |   await expect(page.getByRole('dialog')).toContainText('历史收益');
  50  |   await page.getByRole('button', { name: '取消', exact: true }).click();
  51  |   await expect(openai).toContainText('dayong@example.com');
  52  |   await openai.getByRole('button', { name: '确认换号' }).click();
  53  |   await page.getByRole('button', { name: '确认切换', exact: true }).click();
  54  |   await expect(openai).toContainText('another@example.com');
  55  |   await expect(openai).toContainText('已暂停');
  56  | });
  57  | for (const scene of ['removal-pending', 'removal-unknown']) {
  58  |   test(`${scene} 保留卡片并停止新任务`, async ({ page }) => {
  59  |     await accounts(page, scene);
  60  |     const openai = page.getByRole('region', { name: 'OpenAI 账号' });
  61  |     await openai.getByRole('button', { name: '移除账号' }).click();
  62  |     await expect(page.getByRole('dialog')).toContainText('官方客户端登录和历史收益');
  63  |     await page.getByRole('button', { name: '确认移除', exact: true }).click();
  64  |     await expect(openai).toContainText(
  65  |       scene === 'removal-pending' ? '移除处理中' : '移除结果未确认',
  66  |     );
  67  |     await expect(openai).toContainText('dayong@example.com');
  68  |     await expect(openai).toContainText('已暂停');
  69  |   });
  70  | }
  71  | test('显式移除记忆、重新接入和收益保留由真实演示适配器保证', async ({ page }) => {
  72  |   await page.goto('/');
  73  |   const result = await page.evaluate(async () => {
  74  |     const { createDemoClient } = await import(/* @vite-ignore */ String('/src/client/demo.ts'));
  75  |     const client = createDemoClient('ready');
  76  |     const before = await client.snapshot();
  77  |     await client.dispatch({ type: 'removeAccount', platform: 'openai' });
  78  |     await client.dispatch({ type: 'detectAccount', platform: 'openai' });
  79  |     const detected = await client.snapshot();
  80  |     await client.dispatch({ type: 'connectAccount', platform: 'openai' });
  81  |     const connected = await client.snapshot();
  82  |     return { before, detected, connected };
  83  |   });
  84  |   expect(result.detected.accounts.value?.some((a: Account) => a.platform === 'openai')).toBe(false);
  85  |   expect(
  86  |     result.connected.accounts.value?.find((a: Account) => a.platform === 'openai')?.paused,
  87  |   ).toBe(true);
  88  |   expect(result.connected.process.value?.state).toBe('paused');
  89  |   expect(result.connected.earnings).toEqual(result.before.earnings);
  90  | });
  91  | test('过期授权和未确认移除不能通过检测或恢复绕过，其他平台暂停不变', async ({ page }) => {
  92  |   await page.goto('/');
  93  |   const result = await page.evaluate(async () => {
  94  |     const { createDemoClient } = await import(/* @vite-ignore */ String('/src/client/demo.ts'));
  95  |     const expired = createDemoClient('authorization-expired');
  96  |     await expired.dispatch({ type: 'detectAccount', platform: 'openai' });
  97  |     const start = await expired.dispatch({
  98  |       type: 'startContribution',
  99  |       platforms: ['openai'],
  100 |     });
  101 |     const pending = createDemoClient('removal-unknown');
  102 |     await pending.dispatch({ type: 'removeAccount', platform: 'openai' });
  103 |     await pending.dispatch({ type: 'connectAccount', platform: 'openai' });
  104 |     await pending.dispatch({
  105 |       type: 'setPlatformPaused',
  106 |       platform: 'openai',
  107 |       paused: false,
  108 |     });
  109 |     const change = createDemoClient('account-change');
  110 |     await change.dispatch({ type: 'startContribution', platforms: ['claude'] });
  111 |     await change.dispatch({ type: 'confirmAccountChange', platform: 'openai' });
  112 |     return {
  113 |       start,
  114 |       pending: await pending.snapshot(),
  115 |       change: await change.snapshot(),
  116 |     };
  117 |   });
  118 |   expect(result.start.kind).toBe('failed');
  119 |   expect(
  120 |     result.pending.accounts.value?.find((a: Account) => a.platform === 'openai'),
  121 |   ).toMatchObject({ state: 'unavailable', paused: true, removal: 'unknown' });
```