'use strict';
// ============================================================
//  幻想之境 Online — 去背 / 裁切小工具
//  原圖 → 去背 (從邊緣漫水) → 清碎塊 → 筆刷修改 → 裁切置中、腳底對齊 → (像素化) → 存進遊戲
//  圖檔規格見 docs/art/美術規格.md
// ============================================================
const $ = id => document.getElementById(id);
const OUT = 256;          // 成品畫布邊長
const SRC_MAX = 1024;     // 原圖太大就先縮到這個大小 (處理比較快)

const T = {
  man: null,              // /assets.json
  w: 0, h: 0,
  src: null,              // 原圖像素 (Uint8ClampedArray)
  auto: null,             // 自動去背後的像素
  edits: null,            // 筆刷:0 沒改、1 擦掉、2 還原
  final: null,            // 自動去背 + 筆刷
  out: null,              // 成品畫布 (256×256,或像素化的小畫布)
  brush: 'erase', painting: false, viewScale: 1,
  bgInfo: null,
  loaded: '',             // 目前載入的是哪個目標的哪張原圖 (避免重複自動載入)
};
const ZH_FRAME = { attack: '攻擊', hurt: '受傷', sleep: '睡著' };

// ---------- 目標 (要做哪一張) ----------
function target() {
  const kind = $('sel-kind').value, id = $('sel-target').value, frame = kind === 'pets' ? $('sel-frame').value : '';
  const file = `${kind}/${id}${frame ? '_' + frame : ''}.png`;
  const art = T.man ? T.man.art : {};
  const size = kind === 'pets' ? ((art[id] || {}).size || 64) : ((art.npc || {}).size || 72);
  return { kind, id, frame, file, key: file.replace(/\.png$/, ''), baseKey: `${kind}/${id}`, size, hover: kind === 'pets' ? ((art[id] || {}).hover || 0) : 0 };
}
function fillTargets() {
  const kind = $('sel-kind').value, sel = $('sel-target'), names = kind === 'pets' ? T.man.species : T.man.npcs;
  const prev = sel.value;
  sel.innerHTML = Object.entries(names).map(([k, n]) => {
    const has = T.man.files.some(f => f.p === `${kind}/${k}.png`);
    const src = findSrc({ kind, id: k, frame: '' });
    return `<option value="${k}">${n}${has ? '  ✔有圖' : ''}${src ? '  · 有原圖' : ''}</option>`;
  }).join('');
  if (names[prev]) sel.value = prev;
  $('frame-row').hidden = kind !== 'pets';
  updateTarget();
}
function updateTarget() {
  const tg = target(), pix = $('pix').checked;
  $('fname').textContent = 'public/assets/' + tg.file;
  $('finfo').textContent = `遊戲中顯示 ${tg.size}px` + (pix ? `,像素化畫布 ${Math.round(tg.size / 2)}×${Math.round(tg.size / 2)}` : `,成品畫布 ${OUT}×${OUT}`)
    + (tg.hover ? `,浮空 ${tg.hover}px` : '');
  const cur = T.man && T.man.files.find(f => f.p === tg.file);
  if (cur) $('cur-img').src = `/assets/${cur.p}?v=${cur.v}`; else $('cur-img').removeAttribute('src');
  $('cur-img').style.visibility = cur ? 'visible' : 'hidden';
  $('cur-cap').textContent = cur ? '遊戲裡目前的圖' : '遊戲裡還沒有這張圖';
  $('b-del').disabled = !cur;
  $('fscale-row').hidden = !tg.frame;
  if (tg.frame) loadMainRef(tg); else $('fscale-note').textContent = '';
  const src = findSrc(tg);
  $('srcfind').textContent = src ? `art-src/${src}` : `art-src/ 裡沒有這張的原圖(檔名:${srcNames(tg)[0]}.png)`;
  if (src && T.loaded !== tg.file + '|' + src) loadSrc(src, tg);
  else if (T.loaded && !T.loaded.endsWith('|manual') && !T.loaded.startsWith(tg.file + '|')) clearWork();   // 別張的原圖,不能拿來存成這張
  else if (T.src) buildOutput();
}
// 動作圖的大小基準:遊戲裡這隻寵物的主圖 (算出不透明的面積,換算成 256 畫布的單位)
function loadMainRef(tg) {
  const f = T.man.files.find(x => x.p === tg.baseKey + '.png');
  if (!f) { T.mainRef = null; delete ART.imgs.cmp; return; }
  const tag = f.p + '?v=' + f.v;
  if (T.mainRef && T.mainRef.tag === tag) return;
  const img = new Image();
  img.onload = () => {
    const c = mkCanvas(img.width, img.height), g = c.getContext('2d');
    g.drawImage(img, 0, 0);
    const d = g.getImageData(0, 0, img.width, img.height).data;
    let n = 0;
    for (let i = 3; i < d.length; i += 4) if (d[i] > 128) n++;
    T.mainRef = { key: tg.baseKey, tag, area: n * (OUT / img.width) ** 2 };
    ART.imgs.cmp = img; ART.meta.cmp = measureArt(img);
    if (T.src) buildOutput();
  };
  img.src = '/assets/' + tag;
}
function clearWork() {
  T.src = T.auto = T.final = T.out = null;
  T.loaded = '';
  workCv = null;
  $('work-wrap').innerHTML = '<div class="empty-hint">這張還沒有原圖。把原圖放到 art-src/ 後重新整理,或直接拖曳圖片進來。</div>';
  $('srcinfo').textContent = '';
  refreshOutput();
}
// art-src/ 裡的原圖:檔名用中文名字 (噗噗.png、噗噗_攻擊.png),也接受英文代號 (poring.png、poring_attack.png)
function srcNames(tg) {
  const zh = tg.kind === 'pets' ? T.man.species[tg.id] : T.man.npcs[tg.id];
  const bases = [zh, (zh || '').split(' ').pop(), tg.id].filter(Boolean);
  const out = [];
  for (const b of bases) {
    out.push(b + (tg.frame ? '_' + (ZH_FRAME[tg.frame] || tg.frame) : ''));
    if (tg.frame) out.push(b + '_' + tg.frame);
  }
  return out;
}
function findSrc(tg) {
  if (!T.man || !T.man.src) return null;
  const want = srcNames(tg).map(n => n.toLowerCase());
  return T.man.src.find(f => want.includes(f.replace(/\.[^.]+$/, '').toLowerCase())) || null;
}
function loadSrc(name, tg) {
  T.loaded = tg.file + '|' + name;
  fetch('/api/src?f=' + encodeURIComponent(name)).then(r => { if (!r.ok) throw new Error(r.status); return r.blob(); })
    .then(b => loadFile(new File([b], name, { type: b.type || 'image/png' }), 'art-src/'))
    .catch(() => msg('讀不到 art-src/' + name + '(重開伺服器後再試試)', true));
}

// ---------- 讀圖 ----------
function loadFile(file, from = '') {
  if (!file || !file.type.startsWith('image/')) return msg('這不是圖片檔。', true);
  const url = URL.createObjectURL(file), img = new Image();
  img.onload = () => {
    const k = Math.min(1, SRC_MAX / Math.max(img.width, img.height));
    const w = Math.max(1, Math.round(img.width * k)), h = Math.max(1, Math.round(img.height * k));
    const c = mkCanvas(w, h), g = c.getContext('2d');
    g.imageSmoothingQuality = 'high';
    g.drawImage(img, 0, 0, w, h);
    T.w = w; T.h = h;
    T.src = g.getImageData(0, 0, w, h).data;
    T.edits = new Uint8Array(w * h);
    $('srcinfo').textContent = `原圖 ${img.width}×${img.height}` + (k < 1 ? `(處理時縮成 ${w}×${h})` : '') + ` · ${from}${file.name || '貼上的圖片'}`;
    if (!from) T.loaded = target().file + '|manual';
    URL.revokeObjectURL(url);
    process();
  };
  img.onerror = () => msg('讀不到這張圖。', true);
  img.src = url;
}

// ---------- 去背 ----------
function colorDist(d, i, bg) {
  const dr = d[i] - bg[0], dg = d[i + 1] - bg[1], db = d[i + 2] - bg[2];
  return Math.sqrt(dr * dr + dg * dg + db * db);
}
// 統計邊框顏色:背景色 = 最常出現的顏色;也順便偵測「已經透明」與「畫出來的灰白格子」
function borderInfo(d, w, h) {
  const cnt = new Map();
  let transparent = 0, total = 0;
  const visit = (x, y) => {
    const i = (y * w + x) * 4;
    total++;
    if (d[i + 3] < 16) { transparent++; return; }
    const k = ((d[i] >> 4) << 8) | ((d[i + 1] >> 4) << 4) | (d[i + 2] >> 4);
    const e = cnt.get(k);
    if (e) { e.n++; e.r += d[i]; e.g += d[i + 1]; e.b += d[i + 2]; } else cnt.set(k, { n: 1, r: d[i], g: d[i + 1], b: d[i + 2] });
  };
  for (let x = 0; x < w; x++) { visit(x, 0); visit(x, h - 1); }
  for (let y = 1; y < h - 1; y++) { visit(0, y); visit(w - 1, y); }
  const top = [...cnt.values()].sort((a, b) => b.n - a.n);
  const col = e => e && [e.r / e.n, e.g / e.n, e.b / e.n];
  const opaque = total - transparent;
  const checker = top.length >= 2 && top[0].n > opaque * 0.25 && top[1].n > opaque * 0.25
    && Math.abs(top[0].r / top[0].n - top[1].r / top[1].n) > 20 && Math.max(...col(top[1])) - Math.min(...col(top[1])) < 20;
  return { transparent: transparent / total, bg: col(top[0]) || [255, 255, 255], checker };
}
function removeBg(d, w, h, o) {
  const N = w * h, out = new Uint8ClampedArray(d);
  const info = T.bgInfo = borderInfo(d, w, h);
  if (info.transparent > 0.6) {   // 原圖已經是透明背景
    for (let i = 0; i < N; i++) if (out[i * 4 + 3] < 10) out[i * 4 + 3] = 0;
    return out;
  }
  const bg = info.bg, tol = o.tol, soft = Math.max(1, o.soft);
  const m = new Uint8Array(N);    // 1 = 背景
  const isBg = i => d[i * 4 + 3] < 16 || colorDist(d, i * 4, bg) <= tol;
  if (o.enclosed) {
    for (let i = 0; i < N; i++) if (isBg(i)) m[i] = 1;
  } else {   // 從邊緣漫水
    const q = new Int32Array(N);
    let qh = 0, qt = 0;
    const push = i => { if (!m[i] && isBg(i)) { m[i] = 1; q[qt++] = i; } };
    for (let x = 0; x < w; x++) { push(x); push((h - 1) * w + x); }
    for (let y = 0; y < h; y++) { push(y * w); push(y * w + w - 1); }
    while (qh < qt) {
      const i = q[qh++], x = i % w;
      if (x > 0) push(i - 1);
      if (x < w - 1) push(i + 1);
      if (i >= w) push(i - w);
      if (i < N - w) push(i + w);
    }
  }
  for (let i = 0; i < N; i++) if (m[i]) out[i * 4 + 3] = 0;
  // 柔邊:緊鄰背景 (2 格內) 而且顏色接近背景的像素,改成半透明並去掉背景色
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const i = y * w + x;
    if (m[i]) continue;
    const dist = colorDist(d, i * 4, bg);
    if (dist >= tol + soft) continue;
    let near = false;
    for (let dy = -2; dy <= 2 && !near; dy++) for (let dx = -2; dx <= 2; dx++) {
      const xx = x + dx, yy = y + dy;
      if (xx >= 0 && yy >= 0 && xx < w && yy < h && m[yy * w + xx]) { near = true; break; }
    }
    if (!near) continue;
    const a = Math.min(1, Math.max(0.05, (dist - tol) / soft)), j = i * 4;
    for (let c = 0; c < 3; c++) out[j + c] = (d[j + c] - (1 - a) * bg[c]) / a;
    out[j + 3] = d[j + 3] * a;
  }
  return out;
}
// 清掉小碎塊:只留比最大那塊的 pct% 還大的區塊
function cleanSpecks(px, w, h, pct) {
  const N = w * h, lab = new Int32Array(N), q = new Int32Array(N), sizes = [0];
  let n = 0;
  for (let s = 0; s < N; s++) {
    if (lab[s] || px[s * 4 + 3] < 32) continue;
    n++;
    let qh = 0, qt = 0, size = 0;
    lab[s] = n; q[qt++] = s;
    while (qh < qt) {
      const i = q[qh++], x = i % w, y = (i / w) | 0;
      size++;
      for (let dy = -1; dy <= 1; dy++) for (let dx = -1; dx <= 1; dx++) {
        const xx = x + dx, yy = y + dy;
        if (xx < 0 || yy < 0 || xx >= w || yy >= h) continue;
        const j = yy * w + xx;
        if (!lab[j] && px[j * 4 + 3] >= 32) { lab[j] = n; q[qt++] = j; }
      }
    }
    sizes.push(size);
  }
  const keep = Math.max(...sizes) * pct / 100;
  let removed = 0;
  for (let i = 0; i < N; i++) {
    if (px[i * 4 + 3] === 0) continue;
    if (!lab[i] || sizes[lab[i]] < keep) { px[i * 4 + 3] = 0; if (lab[i]) removed++; }
  }
  return removed;
}

// ---------- 處理流程 ----------
const opts = () => ({ tol: +$('tol').value, soft: +$('soft').value, enclosed: $('enclosed').checked,
  clean: $('clean').checked, cleanPct: +$('clean-pct').value });
function process() {
  if (!T.src) return;
  const o = opts();
  T.auto = removeBg(T.src, T.w, T.h, o);
  if (o.clean) cleanSpecks(T.auto, T.w, T.h, o.cleanPct);
  const bi = T.bgInfo;
  $('bgwarn').textContent = bi.transparent > 0.6 ? '原圖已經是透明背景,跳過去背。' :
    bi.checker ? '⚠ 邊緣看起來是「畫出來的灰白格子」,不是真的透明。建議請 AI 改用純白背景重畫。' : '';
  applyEdits();
}
function applyEdits() {
  const f = new Uint8ClampedArray(T.auto), e = T.edits;
  for (let i = 0; i < e.length; i++) {
    if (e[i] === 1) f[i * 4 + 3] = 0;
    else if (e[i] === 2) { const j = i * 4; f[j] = T.src[j]; f[j + 1] = T.src[j + 1]; f[j + 2] = T.src[j + 2]; f[j + 3] = T.src[j + 3]; }
  }
  T.final = f;
  drawWork();
  buildOutput();
}

// ---------- 編輯區 ----------
let workCv = null;
function drawWork() {
  if (!workCv) {
    $('work-wrap').innerHTML = '';
    workCv = mkCanvas(T.w, T.h);
    workCv.id = 'work';
    workCv.className = 'checker';
    $('work-wrap').appendChild(workCv);
    bindBrush(workCv);
  }
  if (workCv.width !== T.w || workCv.height !== T.h) { workCv.width = T.w; workCv.height = T.h; }
  const g = workCv.getContext('2d');
  g.putImageData(new ImageData($('show-src').checked ? new Uint8ClampedArray(T.src) : T.final, T.w, T.h), 0, 0);
}
function bindBrush(cv) {
  const paint = ev => {
    const r = cv.getBoundingClientRect(), k = T.w / r.width;
    const cx = (ev.clientX - r.left) * k, cy = (ev.clientY - r.top) * k, rad = +$('brush').value * k / 2;
    const v = T.brush === 'erase' ? 1 : 2;
    for (let y = Math.max(0, cy - rad | 0); y <= Math.min(T.h - 1, cy + rad); y++) {
      for (let x = Math.max(0, cx - rad | 0); x <= Math.min(T.w - 1, cx + rad); x++) {
        if ((x - cx) ** 2 + (y - cy) ** 2 <= rad * rad) T.edits[y * T.w + x] = v;
      }
    }
    if (!paint.pending) { paint.pending = true; requestAnimationFrame(() => { paint.pending = false; applyEdits(); }); }
  };
  cv.addEventListener('mousedown', ev => { T.painting = true; paint(ev); });
  addEventListener('mousemove', ev => { if (T.painting) paint(ev); });
  addEventListener('mouseup', () => { T.painting = false; });
}

// ---------- 成品:裁切、置中、腳底對齊 ----------
function bbox(px, w, h) {
  let x0 = w, y0 = h, x1 = -1, y1 = -1;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    if (px[(y * w + x) * 4 + 3] > 24) { if (x < x0) x0 = x; if (x > x1) x1 = x; if (y < y0) y0 = y; if (y > y1) y1 = y; }
  }
  return x1 < 0 ? null : { x0, y0, x1, y1, w: x1 - x0 + 1, h: y1 - y0 + 1 };
}
// 高品質縮小:每次縮一半,最後再縮到目標大小
function downscale(src, dw, dh) {
  let c = src;
  while (c.width / 2 >= dw && c.height / 2 >= dh) {
    const n = mkCanvas(Math.ceil(c.width / 2), Math.ceil(c.height / 2)), g = n.getContext('2d');
    g.imageSmoothingQuality = 'high';
    g.drawImage(c, 0, 0, n.width, n.height);
    c = n;
  }
  const out = mkCanvas(Math.max(1, Math.round(dw)), Math.max(1, Math.round(dh))), g = out.getContext('2d');
  g.imageSmoothingQuality = 'high';
  g.drawImage(c, 0, 0, out.width, out.height);
  return out;
}
function buildOutput() {
  if (!T.final) return;
  const b = bbox(T.final, T.w, T.h);
  if (!b) { T.out = null; refreshOutput(); return; }
  const crop = mkCanvas(b.w, b.h);
  crop.getContext('2d').putImageData(new ImageData(T.final, T.w, T.h), -b.x0, -b.y0, b.x0, b.y0, b.w, b.h);
  const pad = +$('pad').value, side = 2, tg = target();
  const fill = Math.min((OUT - side * 2) / b.w, (OUT - pad) / b.h);   // 塞滿畫布的倍率
  let k = fill, note = '';
  if (tg.frame) {   // 動作圖:依「遊戲裡主圖」的面積對齊大小,不要各自塞滿 (不然攻擊、受傷、睡著會忽大忽小)
    const ref = T.mainRef && T.mainRef.key === tg.baseKey ? T.mainRef : null;
    if (ref) {
      let area = 0;
      for (let i = 3; i < T.final.length; i += 4) if (T.final[i] > 128) area++;
      k = Math.sqrt(ref.area / Math.max(1, area)) * (+$('fscale').value / 100);
      note = `已依遊戲裡的主圖(${tg.baseKey}.png)對齊大小`;
    } else note = '遊戲裡還沒有這隻的主圖:先做主圖,動作圖才能自動對齊大小(現在是塞滿畫布)';
  }
  // 動作圖比主圖大時,把畫布放大 (遊戲依圖片寬度等比例畫,大小仍然對齊),而不是把角色縮小
  let C = OUT;
  const needW = b.w * k + side * 2, needH = b.h * k + pad;
  if (tg.frame && (needW > OUT || needH > OUT)) {
    C = Math.min(512, Math.ceil(Math.max(needW, needH)));
    if (C === 512) k = Math.min(k, (512 - side * 2) / b.w, (512 - pad) / b.h);
    note += `;這張比主圖大,畫布放大成 ${C}×${C}`;
  }
  $('fscale-note').textContent = note;
  const fit = downscale(crop, b.w * k, b.h * k);
  let out = mkCanvas(C, C);
  const g = out.getContext('2d');
  if ($('flip').checked) { g.translate(C, 0); g.scale(-1, 1); }
  g.drawImage(fit, Math.round((C - fit.width) / 2), C - fit.height);
  if ($('pix').checked) out = pixelate(out, Math.max(8, Math.round(target().size / 2 * C / OUT)), +$('colors').value, $('outline').checked);
  T.out = out;
  refreshOutput();
}

// ---------- 像素化:縮小、透明度二值化、減色 (median cut)、加外框 ----------
function medianCut(cols, k) {
  let boxes = [cols];
  while (boxes.length < k) {
    let bi = -1, br = -1, bc = 0;
    boxes.forEach((bx, i) => {
      if (bx.length < 2) return;
      for (let c = 0; c < 3; c++) {
        let lo = 255, hi = 0;
        for (const p of bx) { if (p[c] < lo) lo = p[c]; if (p[c] > hi) hi = p[c]; }
        if (hi - lo > br) { br = hi - lo; bi = i; bc = c; }
      }
    });
    if (bi < 0 || br <= 0) break;
    const bx = boxes[bi].sort((a, b) => a[bc] - b[bc]), mid = bx.length >> 1;
    boxes.splice(bi, 1, bx.slice(0, mid), bx.slice(mid));
  }
  return boxes.map(bx => [0, 1, 2].map(c => Math.round(bx.reduce((s, p) => s + p[c], 0) / bx.length)));
}
function pixelate(src, n, colors, outline) {
  const c = downscale(src, n, n), g = c.getContext('2d'), id = g.getImageData(0, 0, n, n), d = id.data;
  const cols = [];
  for (let i = 0; i < n * n; i++) {
    const j = i * 4;
    if (d[j + 3] >= 110) { d[j + 3] = 255; cols.push([d[j], d[j + 1], d[j + 2]]); } else d[j + 3] = 0;
  }
  if (cols.length) {
    const pal = medianCut(cols, colors);
    for (let i = 0; i < n * n; i++) {
      const j = i * 4;
      if (!d[j + 3]) continue;
      let best = pal[0], bd = 1e9;
      for (const p of pal) { const dd = (d[j] - p[0]) ** 2 + (d[j + 1] - p[1]) ** 2 + (d[j + 2] - p[2]) ** 2; if (dd < bd) { bd = dd; best = p; } }
      d[j] = best[0]; d[j + 1] = best[1]; d[j + 2] = best[2];
    }
    if (outline) {   // 透明像素旁邊有實心像素 → 塗成最深色再壓暗
      const dark = pal.reduce((a, p) => (p[0] + p[1] + p[2] < a[0] + a[1] + a[2] ? p : a)).map(v => Math.round(v * 0.55));
      const was = new Uint8Array(n * n);
      for (let i = 0; i < n * n; i++) was[i] = d[i * 4 + 3] === 255 ? 1 : 0;
      for (let y = 0; y < n; y++) for (let x = 0; x < n; x++) {
        const i = y * n + x;
        if (was[i]) continue;
        if ((x > 0 && was[i - 1]) || (x < n - 1 && was[i + 1]) || (y > 0 && was[i - n]) || (y < n - 1 && was[i + n])) {
          d[i * 4] = dark[0]; d[i * 4 + 1] = dark[1]; d[i * 4 + 2] = dark[2]; d[i * 4 + 3] = 255;
        }
      }
    }
  }
  g.putImageData(id, 0, 0);
  return c;
}

// ---------- 預覽 ----------
function refreshOutput() {
  const v = $('out-view'), g = v.getContext('2d');
  g.clearRect(0, 0, v.width, v.height);
  const tg = target();
  if (T.out) {
    g.imageSmoothingEnabled = T.out.width >= OUT;
    g.drawImage(T.out, 0, 0, v.width, v.height);
    $('out-cap').textContent = `成品 ${T.out.width}×${T.out.height}`;
    // 讓預覽用的 sprites.js 讀到這張圖 (只在工具頁裡,不影響遊戲)
    ART.imgs[tg.baseKey] = T.out;
    ART.meta[tg.baseKey] = measureArt(T.out);
  } else {
    delete ART.imgs[tg.baseKey];
    $('out-cap').textContent = '成品';
  }
  $('b-save').disabled = $('b-dl').disabled = !T.out;
}
function drawPreview(t) {
  const cv = $('pv'), g = cv.getContext('2d'), tg = target(), W = cv.width;
  g.imageSmoothingEnabled = false;
  for (let y = 0; y < 4; y++) for (let x = 0; x < W / TILE; x++) g.drawImage(tileImg(T_GRASS, (x * 7 + y * 3) % 4), x * TILE, y * TILE);
  g.fillStyle = '#0b1020'; g.fillRect(0, 120, W, 120);
  g.fillStyle = 'rgba(10,12,40,.6)'; g.beginPath(); g.ellipse(W / 2, 200, 220, 34, 0, 0, 7); g.fill();
  g.strokeStyle = 'rgba(230,200,110,.85)'; g.setLineDash([10, 6]); g.beginPath(); g.ellipse(W / 2, 200, 220, 34, 0, 0, 7); g.stroke(); g.setLineDash([]);
  const label = (s, x, y) => { g.font = `11px ${FONT}`; g.textAlign = 'center'; g.fillStyle = '#000'; g.fillText(s, x + 1, y + 1); g.fillStyle = '#fff'; g.fillText(s, x, y); };
  const has = !!ART.imgs[tg.baseKey];
  const drawOne = (x, y, useArt, scale) => {
    g.save(); g.translate(x, y); g.scale(scale, scale);
    const saved = ART.on; ART.on = useArt;
    if (tg.kind === 'pets') drawCreature(g, tg.id, 0, 0, { t, face: 1, id: 3, atk: tg.frame === 'attack' ? 0.5 : 0, hurt: tg.frame === 'hurt', sleep: tg.frame === 'sleep' });
    else if (!(useArt && drawNpcArt(g, tg.id, 0, 0, 1, t))) drawHumanoid(g, 0, 0, { ...(NPC_LOOK[tg.id] || {}), face: 1 }, t);
    ART.on = saved;
    g.restore();
  };
  // 上排:地圖上實際大小
  drawHumanoid(g, 70, 100, { ...lookOwner('knight', '測試'), face: 1 }, t);
  if (has) drawOne(190, 100, true, 1); else label('(還沒有成品)', 190, 90);
  const cmp = tg.frame && T.mainRef && T.mainRef.key === tg.baseKey && ART.imgs.cmp;
  const drawCmp = (x, y, scale) => {
    g.save(); g.translate(x, y); g.scale(scale, scale);
    drawArt(g, 'cmp', 0, 0, { t, face: 1, id: 5 }, tg.size, tg.hover);
    g.restore();
  };
  if (cmp) drawCmp(320, 100, 1); else drawOne(320, 100, false, 1);
  label('主人', 70, 116); label('這張圖', 190, 116); label(cmp ? '主圖(比大小)' : '程式繪圖', 320, 116);
  // 下排:2 倍
  if (has) drawOne(170, 222, true, 2);
  if (cmp) drawCmp(330, 222, 2); else drawOne(330, 222, false, 2);
  requestAnimationFrame(drawPreview);
}

// ---------- 存檔 / 下載 / 刪除 ----------
function msg(text, err) { const m = $('msg'); m.textContent = text; m.className = err ? 'err' : 'ok'; }
function outBlob() { return new Promise(r => T.out.toBlob(r, 'image/png')); }
async function refreshManifest() {
  T.man = await fetch('/assets.json', { cache: 'no-store' }).then(r => r.json());
  ART.sizes = T.man.art;
  setLooks(T.man.looks);   // 進化型態沒有圖時的樣子 (程式繪圖預覽用)
}
async function save() {
  if (!T.out) return;
  const tg = target();
  try {
    const res = await fetch('/api/art?f=' + encodeURIComponent(tg.file), { method: 'POST', body: await outBlob() }).then(r => r.json());
    msg(res.msg + (res.ok ? '。重新整理遊戲頁面就會看到。' : ''), !res.ok);
    await refreshManifest(); fillTargets();
  } catch (e) { msg('存檔失敗:' + e, true); }
}
async function download() {
  if (!T.out) return;
  const a = document.createElement('a');
  a.href = URL.createObjectURL(await outBlob());
  a.download = target().file.split('/')[1];
  a.click();
  setTimeout(() => URL.revokeObjectURL(a.href), 5000);
}
async function del() {
  const tg = target();
  if (!confirm(`確定要刪除遊戲裡的 ${tg.file} 嗎?刪除後會改回程式繪圖。`)) return;
  const res = await fetch('/api/art?del=1&f=' + encodeURIComponent(tg.file), { method: 'POST' }).then(r => r.json());
  msg(res.msg, !res.ok);
  await refreshManifest(); fillTargets();
}

// ---------- 介面 ----------
function bindUI() {
  const drop = $('drop');
  drop.onclick = () => $('file').click();
  $('file').onchange = e => loadFile(e.target.files[0]);
  addEventListener('dragover', e => { e.preventDefault(); drop.classList.add('over'); });
  addEventListener('dragleave', () => drop.classList.remove('over'));
  addEventListener('drop', e => { e.preventDefault(); drop.classList.remove('over'); loadFile(e.dataTransfer.files[0]); });
  addEventListener('paste', e => {
    const it = [...(e.clipboardData || {}).items || []].find(x => x.type.startsWith('image/'));
    if (it) loadFile(it.getAsFile());
  });
  $('sel-kind').onchange = fillTargets;
  $('sel-target').onchange = updateTarget;
  $('sel-frame').onchange = updateTarget;
  const vals = { tol: '', soft: '', 'clean-pct': '%', pad: '', colors: '', brush: '', fscale: '%' };
  for (const [id, unit] of Object.entries(vals)) {   // 滑桿旁邊顯示數值
    const vEl = $(id === 'clean-pct' ? 'clean-v' : id + '-v');
    const upd = () => { vEl.textContent = $(id).value + unit; };
    upd();
    $(id).addEventListener('input', upd);
  }
  let timer = 0;
  const later = fn => () => { clearTimeout(timer); timer = setTimeout(fn, 60); };
  for (const id of ['tol', 'soft', 'enclosed', 'clean', 'clean-pct']) $(id).addEventListener('input', later(process));
  for (const id of ['flip', 'pad', 'pix', 'colors', 'outline', 'fscale']) $(id).addEventListener('input', later(() => { updateTarget(); buildOutput(); }));
  $('show-src').onchange = () => T.src && drawWork();
  $('b-erase').onclick = () => { T.brush = 'erase'; $('b-erase').classList.add('on'); $('b-restore').classList.remove('on'); };
  $('b-restore').onclick = () => { T.brush = 'restore'; $('b-restore').classList.add('on'); $('b-erase').classList.remove('on'); };
  $('b-clear').onclick = () => { if (T.edits) { T.edits.fill(0); applyEdits(); } };
  $('b-save').onclick = save;
  $('b-dl').onclick = download;
  $('b-del').onclick = del;
}

(async function init() {
  bindUI();
  try { await refreshManifest(); } catch (e) { msg('讀不到 /assets.json,請確認伺服器有在執行。', true); return; }
  ART.on = true;
  fillTargets();
  requestAnimationFrame(drawPreview);
})();
