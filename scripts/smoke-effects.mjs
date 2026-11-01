#!/usr/bin/env node
// 浏览器冒烟：用无头 Chromium 真打开每个 effects/<id>/code/index.html。
// 断网打开（任何外网请求都记为问题），收集控制台报错，等 3 秒后截图（桌面 + 手机），
// 并检查画面不是一片纯色（白屏/黑屏）。截图放 shots/，CI 里作为附件给人看。
import { chromium } from 'playwright-core';
import { readdirSync, existsSync, mkdirSync, appendFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const ROOT = resolve(process.argv[2] || '.');
const OUT = resolve(process.env.SHOTS_DIR || 'shots');
const WAIT_MS = Number(process.env.SMOKE_WAIT_MS || 3000);
const VIEWPORTS = [{ name: 'desktop', width: 1280, height: 800 }, { name: 'mobile', width: 390, height: 844 }];
mkdirSync(OUT, { recursive: true });

const ids = readdirSync(join(ROOT, 'effects'), { withFileTypes: true })
  .filter((e) => e.isDirectory() && existsSync(join(ROOT, 'effects', e.name, 'code', 'index.html')))
  .map((e) => e.name);

const browser = await chromium.launch({
  executablePath: process.env.CHROME_PATH || undefined,
  args: ['--use-gl=swiftshader', '--enable-unsafe-swiftshader', '--autoplay-policy=no-user-gesture-required'],
});
const rows = [];
let failed = 0;
for (const id of ids) {
  for (const vp of VIEWPORTS) {
    const page = await browser.newPage({ viewport: { width: vp.width, height: vp.height } });
    const errors = [];
    const external = [];
    page.on('console', (m) => { if (m.type() === 'error') errors.push(m.text().slice(0, 160)); });
    page.on('pageerror', (e) => errors.push(String(e.message || e).slice(0, 160)));
    await page.route('**/*', (route) => {
      const u = route.request().url();
      if (u.startsWith('file:') || u.startsWith('data:') || u.startsWith('blob:')) return route.continue();
      external.push(u.slice(0, 120));
      return route.abort();
    });
    let loadError = '';
    try {
      await page.goto(pathToFileURL(join(ROOT, 'effects', id, 'code', 'index.html')).href, { waitUntil: 'load', timeout: 20000 });
      await page.waitForTimeout(WAIT_MS);
    } catch (e) { loadError = String(e.message || e).split('\n')[0]; }
    const shot = join(OUT, `${id}-${vp.name}.png`);
    let blank = false;
    try {
      await page.screenshot({ path: shot });
      // 用页面自己的 canvas 解码截图，算颜色差异；几乎全一个颜色 = 白屏/黑屏
      const b64 = (await page.screenshot({ type: 'png', scale: 'css' })).toString('base64');
      const spread = await page.evaluate(async (src) => {
        const img = new Image(); img.src = 'data:image/png;base64,' + src; await img.decode();
        const c = document.createElement('canvas'); c.width = 64; c.height = 64;
        const g = c.getContext('2d'); g.drawImage(img, 0, 0, 64, 64);
        const d = g.getImageData(0, 0, 64, 64).data; let min = 765, max = 0;
        for (let i = 0; i < d.length; i += 4) { const v = d[i] + d[i + 1] + d[i + 2]; if (v < min) min = v; if (v > max) max = v; }
        return max - min;
      }, b64);
      blank = spread < 24;
    } catch { /* 截图失败也算问题 */ blank = true; }
    const issues = [];
    if (loadError) issues.push('打不开：' + loadError);
    if (errors.length) issues.push('控制台报错：' + errors.slice(0, 3).join(' / '));
    if (external.length) issues.push('偷偷连外网：' + [...new Set(external)].slice(0, 3).join(' , '));
    if (blank) issues.push('画面几乎是纯色（白屏/黑屏？）');
    if (issues.length) failed++;
    rows.push(`| \`${id}\` | ${vp.name} | ${issues.length ? '❌ ' + issues.join('；').replace(/\|/g, '\\|') : '✅'} |`);
    await page.close();
  }
}
await browser.close();
const md = [`## 浏览器冒烟${failed ? '未通过' : '通过'}`, '', `打开了 ${ids.length} 个效果 × ${VIEWPORTS.length} 种屏幕。截图在本次运行的附件 \`effect-screenshots\` 里。`, '',
  '| 素材 | 屏幕 | 结果 |', '|---|---|---|', ...rows].join('\n');
console.log(md);
if (process.env.GITHUB_STEP_SUMMARY) appendFileSync(process.env.GITHUB_STEP_SUMMARY, md + '\n');
process.exit(failed ? 1 : 0);
