'use strict';
// ============================================================
//  幻想之境 Online — 美術進度表 (spec 第 5 節)
//  每張要畫的圖:已進遊戲 / 有原圖還沒處理 / 還缺。資料全部來自伺服器的圖片清單 (/assets.json?catalog=1)
// ============================================================
const $ = id => document.getElementById(id);
const GROUPS = [   // 上方的完成數:[分組, 名稱]。_opt 結尾是可有可無的,不算進「必要的圖」
  ['pet', '寵物主圖'], ['frame', '寵物動作圖'], ['owner', '主人'], ['npc', 'NPC'], ['item', '道具'],
  ['ui', '登入畫面'], ['ground', '地面材質'], ['deco', '樹與裝飾'], ['frame_opt', '中高階動作圖'], ['owner_opt', '主人施法'],
];
const SECTIONS = [   // [分類, 標題, 說明]
  ['pets', '寵物', '一條進化線一排。中高階的動作圖可有可無(沒有的用程式動畫),還缺時是虛線框。'],
  ['owners', '主人', '施法圖可有可無。'],
  ['npcs', 'NPC', ''], ['items', '道具', ''], ['ui', '登入畫面', ''],
  ['ground', '地面材質', '先試草地,好看再畫其他 5 種。'], ['deco', '樹與裝飾', ''],
];
const STATE_TEXT = { done: '已進遊戲', src: '有原圖還沒處理', miss: '還缺' };
const base = f => f.replace(/\.[^.]+$/, '').toLowerCase();

function el(tag, cls, text) {
  const d = document.createElement(tag);
  if (cls) d.className = cls;
  if (text) d.textContent = text;
  return d;
}
function stateOf(e, files, srcIdx, srcv) {
  const f = files.get(e.p), src = e.src.map(n => srcIdx.get(n.toLowerCase())).find(Boolean) || '';
  return { st: f ? 'done' : src ? 'src' : 'miss', f, src, newer: !!(f && src && srcv[src] > f.v) };
}
function cell(r, label) {
  const { e, s } = r, d = el('div', `cell ${s.st}${e.g.endsWith('_opt') ? ' opt' : ''}`), box = el('div', 'box');
  if (s.f) {
    box.classList.add('checker');
    const img = new Image();
    img.loading = 'lazy'; img.alt = '';
    img.src = `/assets/${s.f.p}?v=${s.f.v}`;
    box.appendChild(img);
  } else box.textContent = s.st === 'src' ? '有原圖' : '還缺';
  d.append(box, el('div', '', label));
  if (s.newer) d.appendChild(el('div', 'newer', '原圖比較新'));
  d.title = [STATE_TEXT[s.st] + (s.newer ? '(原圖比成品新,批次模式會重做)' : ''),
    s.src ? '原圖:art-src/' + s.src : '原圖要放:art-src/' + e.src[0] + '.png', '成品:public/assets/' + e.p].join('\n');
  return d;
}

async function load() {
  let man;
  try {
    man = await fetch('/assets.json?catalog=1', { cache: 'no-store' }).then(r => r.json());
  } catch (err) {
    $('msg').textContent = '讀不到 /assets.json,請確認伺服器有在執行。';
    return;
  }
  $('msg').textContent = '';
  const files = new Map(man.files.map(f => [f.p, f])), srcIdx = new Map();
  for (const f of man.src) if (!srcIdx.has(base(f))) srcIdx.set(base(f), f);
  const rows = man.catalog.map(e => ({ e, s: stateOf(e, files, srcIdx, man.srcv || {}) }));

  // 上方的完成數
  const sum = $('sum'), chips = [];
  let reqDone = 0, reqAll = 0;
  for (const [g, name] of GROUPS) {
    const rs = rows.filter(r => r.e.g === g), done = rs.filter(r => r.s.st === 'done').length, src = rs.filter(r => r.s.st === 'src').length;
    if (!g.endsWith('_opt')) { reqDone += done; reqAll += rs.length; }
    const c = el('span', 'chip' + (g.endsWith('_opt') ? ' opt' : ''));
    c.append(name + (g.endsWith('_opt') ? '(可有可無)' : '') + ' ', el('b', '', `${done} / ${rs.length}`));
    if (src) c.append(' ', el('span', 's', `有原圖 ${src}`));
    chips.push(c);
  }
  const all = el('span', 'chip all');
  all.append('必要的圖 ', el('b', '', `${reqDone} / ${reqAll}`));
  sum.replaceChildren(all, ...chips);

  // 各分類
  const out = [];
  for (const [k, title, note] of SECTIONS) {
    const rs = rows.filter(r => r.e.k === k), panel = el('div', 'panel'), body = el('div', 'body');
    const head = el('div', 'title');
    head.appendChild(el('span', '', `${title}(${rs.filter(r => r.s.st === 'done').length} / ${rs.length})`));
    panel.append(head, body);
    if (note) body.appendChild(el('div', 'note', note));
    if (k === 'pets' || k === 'owners') {
      // 同一個代號的主圖與動作圖排成一張卡片;寵物遇到初階 (動作圖是必要的) 就換一排,一條進化線一排
      const cards = new Map();
      for (const r of rs) { if (!cards.has(r.e.id)) cards.set(r.e.id, []); cards.get(r.e.id).push(r); }
      let line = null;
      for (const list of cards.values()) {
        if (!line || (k === 'pets' && list.some(r => r.e.g === 'frame'))) body.appendChild(line = el('div', 'line'));
        const card = el('div', 'card'), cells = el('div', 'cells');
        for (const r of list) cells.appendChild(cell(r, r.e.f ? man.frameNames[r.e.f] : '主圖'));
        card.append(el('b', '', list[0].e.name), cells);
        line.appendChild(card);
      }
    } else {
      const grid = el('div', 'cellgrid');
      for (const r of rs) grid.appendChild(cell(r, r.e.name));
      body.appendChild(grid);
    }
    out.push(panel);
  }
  // art-src/ 裡對不上任何一張圖的檔案 (多半是檔名打錯)
  const names = new Set(man.catalog.flatMap(e => e.src.map(n => n.toLowerCase())));
  const stray = man.src.filter(f => !names.has(base(f)));
  if (stray.length) {
    const panel = el('div', 'panel'), head = el('div', 'title'), body = el('div', 'body');
    head.appendChild(el('span', '', `art-src/ 裡對不上任何一張圖的檔案(${stray.length})`));
    body.appendChild(el('div', 'note', '檔名要照 docs/phase-4/spec.md 第 3 節:中文名或代號,動作圖接「_攻擊」這類後綴。'));
    for (const f of stray) body.appendChild(el('div', 'unmatched', 'art-src/' + f));
    panel.append(head, body);
    out.push(panel);
  }
  $('sections').replaceChildren(...out);
}

$('b-reload').onclick = load;
addEventListener('focus', load);   // 從去背工具切回來時自動更新
load();
