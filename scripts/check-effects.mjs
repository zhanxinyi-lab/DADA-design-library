#!/usr/bin/env node
// 静态检查：每个 effects/<id>/ 的 README 字段、code/index.html 结构、体积、外链、JS 语法。
// 不装依赖，只用 Node 自带功能。失败 → exit 1，并把人话结果写进 GitHub Job Summary。
import { readdirSync, readFileSync, statSync, existsSync, writeFileSync, mkdtempSync, appendFileSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';
import { spawnSync } from 'node:child_process';

const ROOT = process.argv[2] || '.';
const MAX_HTML_BYTES = Number(process.env.MAX_HTML_BYTES || 1_500_000); // 1.5 MB
const REQUIRED_FIELDS = ['作者', '分类', '状态', '原文'];
const STATUSES = ['needs_recreation', 'has_code', 'ai_recreated', 'pending_cindy', 'video_recreated'];
const NEEDS_CODE = new Set(['has_code', 'ai_recreated', 'video_recreated']);
const ALLOWED_FILE = /^(README\.md|CHANGELOG\.md|code\/index\.html|code\/[^/]+\.(png|jpe?g|webp|gif|svg|mp4|webm|glb|json))$/;
const SECRET = /(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)/;

const problems = []; // { id, what, why }
const add = (id, what, why) => problems.push({ id, what, why });

function walk(dir, base = '') {
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? walk(join(dir, e.name), base + e.name + '/') : [base + e.name]);
}

function checkReadme(id, dir) {
  const p = join(dir, 'README.md');
  if (!existsSync(p)) { add(id, '缺 README.md', '素材库网站读不到标题和出处。'); return null; }
  const text = readFileSync(p, 'utf8');
  if (!/^#\s+\S/m.test(text)) add(id, 'README 没有一级标题（# 标题）', '网站上会显示成没名字。');
  const fields = {};
  for (const f of REQUIRED_FIELDS) {
    const m = text.match(new RegExp(`^-\\s*${f}[：:]\\s*(.+)$`, 'm'));
    if (!m) add(id, `README 缺「${f}」`, '出处信息不全，以后找不到原帖或作者。');
    else fields[f] = m[1].trim();
  }
  const v = text.match(/^-\s*版本[：:]\s*(\S+)/m);
  if (v) {
    fields['版本'] = v[1];
    if (!/^\d+\.\d+\.\d+$/.test(v[1])) add(id, `版本号「${v[1]}」格式不对`, '要写成 1.0.0 这种三段数字。');
    const cl = join(dir, 'CHANGELOG.md');
    if (!existsSync(cl)) add(id, '写了版本号但没有 CHANGELOG.md', '以后说不清每个版本改了什么。');
    else if (!new RegExp(`^##\\s*${v[1].replace(/\./g, '\\.')}\\b`, 'm').test(readFileSync(cl, 'utf8')))
      add(id, `CHANGELOG.md 里没有「## ${v[1]}」这一节`, '版本号涨了，但没写这一版改了什么、来自哪个项目的反馈。');
  }
  if (fields['状态'] && !STATUSES.includes(fields['状态']))
    add(id, `状态「${fields['状态']}」不认识`, `只能是：${STATUSES.join(' / ')}`);
  return fields;
}

function stripComments(html) { return html.replace(/<!--[\s\S]*?-->/g, ''); }

function externalRefs(html) {
  const hits = [];
  const h = stripComments(html);
  // 1) 标签属性里引用外网资源（<a href> 跳转链接除外）
  for (const m of h.matchAll(/<(?!a[\s>])([a-z0-9-]+)\b[^>]*?\s(src|href|srcset|poster|data|action)\s*=\s*["']?\s*((?:https?:)?\/\/[^"'\s>]+)/gi))
    hits.push(`<${m[1]} ${m[2]}=${m[3]}>`);
  // 2) CSS url(http…) / @import
  for (const m of h.matchAll(/(url\(\s*["']?|@import\s+["'])((?:https?:)?\/\/[^"')\s]+)/gi)) hits.push(m[2]);
  // 3) <script> 里的 import / fetch / Worker / WebSocket 指向外网
  for (const s of h.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)) {
    for (const m of s[1].matchAll(/(?:\bfrom\s*|\bimport\s*\(\s*|\bfetch\s*\(\s*|new\s+(?:Worker|WebSocket|EventSource)\s*\(\s*|\.open\s*\(\s*["'][A-Z]+["']\s*,\s*)["'`]((?:https?:|wss?:)?\/\/[^"'`]+)/g))
      hits.push(m[1]);
  }
  return [...new Set(hits)];
}

function checkScripts(id, html) {
  const dir = mkdtempSync(join(tmpdir(), 'fx-'));
  let i = 0;
  for (const m of stripComments(html).matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script>/gi)) {
    const attrs = m[1];
    if (/\bsrc\s*=/.test(attrs)) continue;
    const type = (attrs.match(/\btype\s*=\s*["']?([^"'\s>]+)/i) || [])[1]?.toLowerCase() || '';
    const isModule = type === 'module';
    if (type && !isModule && !/^(text|application)\/(javascript|ecmascript)$/.test(type)) continue; // json / shader 等跳过
    const file = join(dir, `s${i++}.${isModule ? 'mjs' : 'js'}`);
    writeFileSync(file, m[2]);
    const r = spawnSync(process.execPath, ['--check', file], { encoding: 'utf8' });
    if (r.status !== 0) {
      const line = (r.stderr || '').split('\n').find((l) => /Error/.test(l)) || 'SyntaxError';
      add(id, `第 ${i} 段 <script> 语法错误：${line.trim()}`, '页面打开后动效会直接不动或白屏。');
    }
  }
}

function checkHtml(id, dir) {
  const p = join(dir, 'code', 'index.html');
  const size = statSync(p).size;
  if (size > MAX_HTML_BYTES) add(id, `index.html 有 ${(size / 1e6).toFixed(2)} MB，超过 ${(MAX_HTML_BYTES / 1e6).toFixed(1)} MB`, '网站加载慢；通常是把大图/视频转成 base64 塞进去了。');
  const html = readFileSync(p, 'utf8');
  if (!/^\s*<!doctype html>/i.test(html)) add(id, '开头缺 <!doctype html>', '浏览器会用怪异模式渲染，排版可能错位。');
  for (const [re, name] of [[/<meta[^>]+charset/i, '<meta charset>'], [/<title>[^<]+<\/title>/i, '<title>'], [/<meta[^>]+name=["']?viewport/i, '<meta name="viewport">']])
    if (!re.test(html)) add(id, `缺 ${name}`, name === '<meta charset>' ? '中文可能乱码。' : name === '<title>' ? '浏览器标签页没名字。' : '手机上打开会缩成一小块。');
  const ext = externalRefs(html);
  if (ext.length) add(id, `引用了外网资源：${ext.slice(0, 5).join('，')}`, '不是自包含：断网或 CDN 挂掉时效果打不开，也可能被拿来加载不明脚本。');
  if (SECRET.test(html)) add(id, '代码里疑似有密钥 / token', '密钥进了公开仓库就等于泄露。');
  checkScripts(id, html);
}

const effectsDir = join(ROOT, 'effects');
const ids = existsSync(effectsDir) ? readdirSync(effectsDir, { withFileTypes: true }).filter((e) => e.isDirectory()).map((e) => e.name) : [];
for (const id of ids) {
  const dir = join(effectsDir, id);
  if (!/^[a-z0-9-]+$/i.test(id)) add(id, '目录名只能用字母、数字、横线', '网址里会出问题。');
  for (const f of walk(dir)) if (!ALLOWED_FILE.test(f)) add(id, `多余文件：${f}`, '每条素材只放 README.md 和 code/ 里的东西。');
  const fields = checkReadme(id, dir);
  const hasCode = existsSync(join(dir, 'code', 'index.html'));
  if (fields?.['状态'] && NEEDS_CODE.has(fields['状态']) && !hasCode) add(id, `状态是 ${fields['状态']} 但没有 code/index.html`, '网站会显示「有代码」却打不开。');
  if (hasCode) checkHtml(id, dir);
}

const md = problems.length
  ? ['## 检查未通过', '', `共 ${problems.length} 个问题，修好再合并。`, '', '| 素材 | 问题 | 会导致 |', '|---|---|---|',
     ...problems.map((p) => `| \`${p.id}\` | ${p.what.replace(/\|/g, '\\|')} | ${p.why} |`)].join('\n')
  : `## 检查通过\n\n${ids.length} 条素材的 README、HTML 结构、外链、脚本语法、体积都没问题。`;
console.log(md);
if (process.env.GITHUB_STEP_SUMMARY) appendFileSync(process.env.GITHUB_STEP_SUMMARY, md + '\n');
process.exit(problems.length ? 1 : 0);
