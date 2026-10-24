# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: accounts.spec.ts >> 换号明确旧新标识与影响，取消不变、确认保持暂停
- Location: tests/accounts.spec.ts:43:1

# Error details

```
Test timeout of 30000ms exceeded.
```

```
Error: expect(locator).toContainText(expected) failed

Locator: getByRole('region', { name: 'OpenAI 账号' })
Expected substring: "another@example.com"
Received string:    ""

Call log:
  - Expect "toContainText" getByRole('region', { name: 'OpenAI 账号' }) with timeout 5000ms
  - waiting for getByRole('region', { name: 'OpenAI 账号' })
  - 

```

# Page snapshot

```yaml
- generic:
  - generic:
    - generic:
      - complementary [aria-hidden]:
        - generic: Bee
        - navigation:
          - button: 概览
          - button: AI 账号
          - button: 收益
          - button: 诊断
          - button: 设置
        - generic:
          - generic:
            - text: 尚未接通真实供给
            - paragraph: 关窗后可从托盘找回
          - generic:
            - generic: B
            - generic:
              - text: Bee 桌面端
              - generic: 本地演示空间
      - generic:
        - banner [aria-hidden]:
          - generic:
            - generic: 工作空间
            - generic: AI 账号
          - generic:
            - generic: 本机设备
            - generic: 演示数据
        - main:
          - generic [aria-hidden]:
            - generic:
              - heading [level=1]: AI 账号
              - paragraph: 管理这台设备用于贡献的 AI 账号。
            - generic:
              - text: 演示场景
              - combobox
          - paragraph [aria-hidden]: 检测已有官方登录，或通过官方授权接入。接入与换号后保持暂停，由你决定何时贡献。
          - generic [aria-hidden]:
            - region:
              - generic:
                - generic:
                  - generic: O
                  - heading [level=2]: OpenAI
                - generic: 订阅套餐 Plus
              - paragraph: dayong@example.com
              - paragraph: 已接入 · 已暂停
              - paragraph: 5 小时 · 剩余 82% · 2 小时后重置
              - button: 查看详情
              - generic:
                - button [disabled]: 检测已有登录
                - button [disabled]: 官方授权接入
                - button [disabled] [expanded]: 确认换号
                - button [disabled]: 移除账号
            - region:
              - generic:
                - generic:
                  - generic: ✳
                  - heading [level=2]: Claude
                - generic: 订阅套餐 Pro
              - paragraph: dayong@example.com
              - paragraph: 已接入 · 已暂停
              - paragraph: 5 小时 · 剩余 46% · 48 分钟后重置
              - button: 查看详情
              - generic:
                - button [disabled]: 检测已有登录
                - button [disabled]: 官方授权接入
                - button [disabled]: 确认换号
                - button [disabled]: 移除账号
          - paragraph [aria-hidden]: 演示接入不会读取或修改官方客户端；官方授权尚未接通。
          - region "演示生命周期":
            - generic [aria-hidden]:
              - button: 退出演示
              - button: 更新演示
            - paragraph: 关窗继续后台运行；这里仅预览退出和更新流程。
          - status: 正在处理演示操作…
        - contentinfo [aria-hidden]:
          - text: Bee · 开发版本
          - generic: 演示操作不会影响真实账号或资金
  - dialog [active] [ref=e2]:
    - heading "切换 AI 账号？" [level=2] [ref=e3]
    - paragraph [ref=e4]: 当前账号：dayong@example.com；新检测账号：another@example.com。确认后停止新任务，更换 Bee 接入账号并保持暂停，历史收益继续保留。
    - generic [ref=e5]:
      - button "取消" [disabled] [ref=e6]
      - button "处理中…" [disabled] [ref=e7]
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
  21  |   await page.getByRole('button', { name: '概览', exact: true }).click();
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
> 54  |   await expect(openai).toContainText('another@example.com');
      |                        ^ Error: expect(locator).toContainText(expected) failed
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
  122 |   expect(result.change.accounts.value?.find((a: Account) => a.platform === 'openai')?.paused).toBe(
  123 |     true,
  124 |   );
  125 |   expect(result.change.accounts.value?.find((a: Account) => a.platform === 'claude')?.paused).toBe(
  126 |     false,
  127 |   );
  128 | });
  129 | 
  130 | test('任务未知时移除保留卡片和未确认提示', async ({ page }) => {
  131 |   await accounts(page, 'unknown-tasks');
  132 |   const openai = page.getByRole('region', { name: 'OpenAI 账号' });
  133 |   await openai.getByRole('button', { name: '移除账号' }).click();
  134 |   await page.getByRole('button', { name: '确认移除', exact: true }).click();
  135 |   await expect(openai).toContainText('移除结果未确认');
  136 |   await expect(openai).toContainText('dayong@example.com');
  137 |   await expect(openai).toContainText('已暂停');
  138 | });
  139 | 
  140 | for (const [scene, expected] of [
  141 |   ['ready', 'confirmed'],
  142 |   ['active-tasks', 'pending'],
  143 |   ['unknown-tasks', 'unknown'],
  144 |   ['tasks-loading', 'unknown'],
  145 |   ['tasks-error', 'unknown'],
  146 |   ['removal-pending', 'pending'],
  147 |   ['removal-unknown', 'unknown'],
  148 | ] as const) {
  149 |   test(`移除收尾守门 ${scene} 返回 ${expected}，重试不能越过未决状态`, async ({ page }) => {
  150 |     await page.goto('/');
  151 |     const result = await page.evaluate(async (scene) => {
  152 |       const { createDemoClient } = await import(/* @vite-ignore */ String('/src/client/demo.ts'));
  153 |       const client = createDemoClient(scene);
  154 |       const before = await client.snapshot();
```