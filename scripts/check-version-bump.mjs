#!/usr/bin/env node
// PR 专用：这次 PR 改了哪个效果的 code/，那个效果的「版本」就必须比 main 上的大。
// 用法：node scripts/check-version-bump.mjs <base-sha>
import { execFileSync } from 'node:child_process';
import { appendFileSync } from 'node:fs';

const base = process.argv[2];
if (!base) { console.error('缺 base sha'); process.exit(2); }
const git = (...a) => execFileSync('git', a, { encoding: 'utf8' });
const changed = git('diff', '--name-only', `${base}...HEAD`).split('\n').filter(Boolean);
const codeTouched = new Set(changed.map((f) => f.match(/^effects\/([^/]+)\/code\//)?.[1]).filter(Boolean));
const ver = (ref, id) => {
  try { return git('show', `${ref}:effects/${id}/README.md`).match(/^-\s*版本[：:]\s*(\d+\.\d+\.\d+)/m)?.[1] || null; }
  catch { return undefined; } // 文件在 base 上不存在 = 新效果
};
const gt = (a, b) => { const x = a.split('.').map(Number), y = b.split('.').map(Number);
  for (let i = 0; i < 3; i++) if (x[i] !== y[i]) return x[i] > y[i]; return false; };
const problems = [];
const rows = [];
for (const id of codeTouched) {
  const before = ver(base, id); const after = ver('HEAD', id);
  if (!after) { problems.push(`\`${id}\`：改了代码，但 README 没有「- 版本：x.y.z」`); continue; }
  if (before === undefined || before === null) { rows.push(`\`${id}\`：首次登记版本 ${after}`); continue; }
  if (!gt(after, before)) problems.push(`\`${id}\`：改了代码，版本还是 ${after}（main 上是 ${before}），要往上涨`);
  else rows.push(`\`${id}\`：${before} → ${after}`);
}
const md = problems.length
  ? ['## 版本检查未通过', '', ...problems.map((p) => '- ' + p), '', '小改（修 bug、调参数）涨最后一位：1.0.0 → 1.0.1；新增玩法涨中间：1.0.1 → 1.1.0；不兼容的大改涨第一位。'].join('\n')
  : ['## 版本检查通过', '', ...(rows.length ? rows.map((r) => '- ' + r) : ['- 这次没有改任何效果的代码。'])].join('\n');
console.log(md);
if (process.env.GITHUB_STEP_SUMMARY) appendFileSync(process.env.GITHUB_STEP_SUMMARY, md + '\n');
process.exit(problems.length ? 1 : 0);
