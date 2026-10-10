'use strict';
// ============================================================
//  幻想之境 Online — 客戶端
// ============================================================
const TILE = 32;
const FONT = '"PMingLiU","新細明體","MingLiU","Microsoft JhengHei",sans-serif';
const NUMFONT = 'Verdana,Tahoma,Arial,sans-serif';
const T_GRASS = 0, T_WATER = 1, T_TREE = 2, T_SAND = 3, T_STONE = 4, T_WALL = 5,
      T_FLOWER = 6, T_DARK = 7, T_BRIDGE = 8, T_ASH = 9;
const MAP_CX = 48, MAP_CY = 48;
const SKIN = '#f2c79c';
const HAIRS = ['#3a2412', '#1c1c1c', '#7a4a1c', '#c08a3a', '#a03020', '#d8c070', '#4a3a6a'];

const $ = s => document.querySelector(s);
const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);

const S = {
  ws: null, myId: 0, myName: '', W: 0, H: 0, tiles: null, vars: null, mmBase: null,
  ents: new Map(), npcs: [], mobInfo: {}, items: {}, skills: [], cls: '', clsName: '',
  me: null, inv: [], equip: {}, gold: 0, cdEnd: [0, 0],
  ox: 0, oy: 0, mouse: { x: -1, y: -1, in: false }, hover: null,
  keys: {}, dir: [0, 0], shopOpen: false, dlg: null, twTimer: 0,
  floats: [], projs: [], aoes: [], beams: [], dying: [], marks: [], impacts: [], projEnd: {},
};

// ---------- 小工具 ----------
function hash2(x, y) {
  let n = (Math.imul(x, 374761393) + Math.imul(y, 668265263)) | 0;
  n = Math.imul(n ^ (n >>> 13), 1274126177);
  return ((n ^ (n >>> 16)) >>> 0) / 4294967296;
}
function hashStr(s) {
  let h = 2166136261;
  for (const ch of s) { h ^= ch.codePointAt(0); h = Math.imul(h, 16777619); }
  return h >>> 0;
}
function rng(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function mkCanvas(w, h) { const c = document.createElement('canvas'); c.width = w; c.height = h; return c; }
const tintCache = new Map();
function tint(hex, k) {
  const key = hex + k;
  let v = tintCache.get(key);
  if (v) return v;
  const n = parseInt(hex.slice(1), 16);
  const f = c => clamp(Math.round(k > 0 ? c + (255 - c) * k : c * (1 + k)), 0, 255);
  v = '#' + ((1 << 24) | (f(n >> 16) << 16) | (f((n >> 8) & 255) << 8) | f(n & 255)).toString(16).slice(1);
  tintCache.set(key, v);
  return v;
}
const shade = c => tint(c, -0.28), lighten = c => tint(c, 0.3);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
function itemName(id) { const it = S.items[id]; return it ? ((it.cn && it.cn[S.cls]) || it.name) : id; }

// ============================================================
//  圖塊與樹木 (程式繪製的像素風)
// ============================================================
const tileCache = new Map();
function tileImg(t, v) {
  const k = t * 8 + v;
  let c = tileCache.get(k);
  if (!c) { c = paintTile(t, v); tileCache.set(k, c); }
  return c;
}
function paintTile(t, v) {
  const c = mkCanvas(TILE, TILE), g = c.getContext('2d'), R = rng(t * 977 + v * 131 + 7);
  const px = (x, y, w, h, col) => { g.fillStyle = col; g.fillRect(x, y, w, h); };
  const speck = (cols, n) => { for (let i = 0; i < n; i++) px((R() * 16 | 0) * 2, (R() * 16 | 0) * 2, 2, 2, cols[R() * cols.length | 0]); };
  const blades = (col, n) => {
    for (let i = 0; i < n; i++) { const x = (R() * 14 | 0) * 2, y = (R() * 13 | 0) * 2 + 4; px(x, y, 2, 2, col); px(x + 2, y - 2, 2, 2, col); }
  };
  if (t === T_GRASS || t === T_FLOWER) {
    px(0, 0, 32, 32, '#4c9637'); speck(['#58a541', '#43872f', '#539e3c'], 40); blades('#67b64c', 3);
    if (t === T_FLOWER) {
      const cols = ['#f05050', '#f8e050', '#ffffff', '#e070e0', '#70b0ff'];
      for (let i = 0; i < 3; i++) {
        const x = 4 + (R() * 12 | 0) * 2, y = 4 + (R() * 12 | 0) * 2, col = cols[R() * cols.length | 0];
        px(x - 2, y, 2, 2, col); px(x + 2, y, 2, 2, col); px(x, y - 2, 2, 2, col); px(x, y + 2, 2, 2, col); px(x, y, 2, 2, '#f8d030');
      }
    }
  } else if (t === T_DARK) {
    px(0, 0, 32, 32, '#3a6630'); speck(['#335a2a', '#44733a', '#2e5226'], 40); blades('#4f8443', 2);
  } else if (t === T_SAND) {
    px(0, 0, 32, 32, '#d2ad72'); speck(['#c39c5e', '#ddbd88', '#b88f55'], 34);
    if (R() < 0.6) px((R() * 14 | 0) * 2, (R() * 14 | 0) * 2, 4, 2, '#9c8058');
  } else if (t === T_STONE) {
    px(0, 0, 32, 32, '#a29e93');
    for (let row = 0; row < 4; row++) {
      const off = row % 2 ? 8 : 0;
      px(0, row * 8, 32, 1, '#7d796f');
      for (let bx = off - 16; bx < 32; bx += 16) { px(bx, row * 8, 1, 8, '#7d796f'); px(bx + 1, row * 8 + 1, 15, 1, '#b9b5aa'); }
    }
    speck(['#96928a', '#aaa69c'], 6);
  } else if (t === T_WALL) {
    px(0, 0, 32, 32, '#6a6560'); px(0, 0, 32, 10, '#a39d92'); px(0, 0, 32, 2, '#bdb7ab'); px(0, 10, 32, 2, '#4d4844');
    for (let row = 0; row < 3; row++) {
      const y = 12 + row * 7, off = row % 2 ? 6 : 0;
      px(0, y + 6, 32, 1, '#524d48');
      for (let bx = off - 12; bx < 32; bx += 12) px(bx, y, 1, 7, '#524d48');
    }
  } else if (t === T_BRIDGE) {
    px(0, 0, 32, 32, '#2d6cc0');
    for (let i = 0; i < 4; i++) { px(2, i * 8, 28, 7, i % 2 ? '#94653a' : '#a2713f'); px(2, i * 8 + 7, 28, 1, '#5e3e20'); }
    px(0, 0, 3, 32, '#6e4a26'); px(29, 0, 3, 32, '#6e4a26');
  } else if (t === T_ASH) {
    px(0, 0, 32, 32, '#4a3934'); speck(['#3b2c28', '#5a4741', '#523f3a'], 40);
    if (R() < 0.7) px((R() * 15 | 0) * 2, (R() * 15 | 0) * 2, 2, 2, '#d0582a');
  }
  return c;
}

const treeImgs = [];
function paintTrees() {
  for (let k = 0; k < 4; k++) {
    const c = mkCanvas(48, 64), g = c.getContext('2d');
    const circ = (x, y, r, col) => { g.fillStyle = col; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); };
    g.fillStyle = 'rgba(0,0,0,.25)'; g.beginPath(); g.ellipse(24, 60, 14, 4, 0, 0, 7); g.fill();
    g.fillStyle = '#5e3c1f'; g.fillRect(20, 38, 8, 22); g.fillStyle = '#7a4f2a'; g.fillRect(20, 38, 3, 22);
    if (k < 2) {
      const d = k ? ['#2a5f27', '#37802f', '#4f9c40'] : ['#2e6a2a', '#3e8c35', '#5bab4b'];
      circ(24, 30, 17, d[0]); circ(13, 34, 11, d[0]); circ(35, 34, 11, d[0]);
      circ(22, 26, 13, d[1]); circ(31, 31, 8, d[1]);
      circ(18, 21, 6, d[2]); circ(27, 18, 3, d[2]);
    } else {
      const d = k === 2 ? ['#1d4a2b', '#2a6338'] : ['#23422a', '#2f5a37'];
      for (let i = 0; i < 3; i++) {
        const y = 52 - i * 12, w = 21 - i * 5;
        g.fillStyle = d[0]; g.beginPath(); g.moveTo(24 - w, y); g.lineTo(24 + w, y); g.lineTo(24, y - 22); g.fill();
        g.fillStyle = d[1]; g.beginPath(); g.moveTo(24 - w + 5, y - 2); g.lineTo(24, y - 2); g.lineTo(24, y - 20); g.fill();
      }
    }
    treeImgs.push(c);
  }
}

// ============================================================
//  角色繪製
// ============================================================
function drawHumanoid(g, x, y, o, t) {
  const sc = o.scale || 2;
  g.save();
  g.translate(Math.round(x), Math.round(y));
  g.fillStyle = 'rgba(0,0,0,.3)'; g.beginPath(); g.ellipse(0, 0, 6 * sc, 2.2 * sc, 0, 0, 7); g.fill();
  g.scale((o.face < 0 ? -1 : 1) * sc, sc);
  const ph = o.walk ? t / 1000 * 11 : 0;
  const lp = o.walk ? Math.round(Math.sin(ph) * 1.5) : 0;
  const bob = o.walk && Math.abs(Math.sin(ph)) > 0.6 ? 1 : 0;
  const R = (x, y, w, h, c) => { g.fillStyle = c; g.fillRect(x, y, w, h); };
  g.translate(0, -bob);
  if (o.robe) { R(-5, -7, 10, 7, o.body); R(-5, -1, 10, 1, shade(o.body)); }
  else {
    const sh = o.shoe || '#2b1d12';
    R(-3 + lp, -6, 2, 6, o.legs); R(1 - lp, -6, 2, 6, o.legs);
    R(-3 + lp, -1, 3, 1, sh); R(1 - lp, -1, 3, 1, sh);
  }
  R(-5, -12, 2, 5, shade(o.body));
  R(-4, -13, 8, 7, o.body); R(-4, -13, 8, 1, lighten(o.body));
  R(-4, -7, 8, 1, o.belt || '#3b2a1a');
  if (o.torso) o.torso(R, g);
  R(-4, -21, 8, 8, o.skin);
  if (o.eyes) o.eyes(R); else R(2, -18, 1, 2, '#1b1b1b');
  if (o.hair) { R(-4, -22, 8, 2, o.hair); R(-5, -21, 3, 6, o.hair); R(-2, -20, 2, 1, o.hair); }
  if (o.head) o.head(R, g);
  const sw = o.atk || 0;
  if (o.weapon) {
    g.save(); g.translate(3, -8);
    let ang = o.idleAng !== undefined ? o.idleAng : 0.5;
    if (sw > 0 && o.swing) ang = -1.3 + sw * 2.8;
    g.rotate(ang);
    o.weapon(R, g, sw);
    g.restore();
  }
  R(1, -12, 2, 5, o.arm || shade(o.body)); R(1, -7, 2, 1, o.skin);
  g.restore();
}

const W_SWORD = col => R => { R(-1, -13, 2, 12, col); R(-1, -13, 1, 12, lighten(col)); R(-3, -1, 6, 1, '#c9a227'); R(-0.5, 0, 1, 3, '#5a3a1a'); };
const W_CLUB = R => { R(-1, -9, 2, 10, '#6b4423'); R(-2, -12, 4, 5, '#5a381c'); R(-2, -12, 1, 5, '#7a5030'); };
const W_STAFF = col => (R, g, sw) => {
  R(-0.5, -14, 1, 19, '#7a5030');
  g.fillStyle = col; g.beginPath(); g.arc(0, -15, 2.2, 0, 7); g.fill();
  g.fillStyle = 'rgba(255,255,255,.7)'; g.fillRect(-1, -16, 1, 1);
  if (sw > 0) { g.fillStyle = 'rgba(255,255,255,.45)'; g.beginPath(); g.arc(0, -15, 4.5 * (1 - sw) + 2, 0, 7); g.fill(); }
};
const W_BOW = col => (R, g, sw) => {
  const a = 1.1, rr = 8, cx = -3, cy = -3;
  const tx = cx + rr * Math.cos(-a), ty = cy + rr * Math.sin(-a), by = cy + rr * Math.sin(a);
  const pull = sw > 0 ? Math.sin(sw * Math.PI) * 4 : 0;
  g.strokeStyle = '#eee'; g.lineWidth = 0.5;
  g.beginPath(); g.moveTo(tx, ty); g.lineTo(tx - pull, cy); g.lineTo(tx, by); g.stroke();
  g.strokeStyle = col; g.lineWidth = 1.4;
  g.beginPath(); g.arc(cx, cy, rr, -a, a); g.stroke();
};
const HAT_WARRIOR = R => { R(-5, -23, 10, 4, '#9aa3ad'); R(-5, -23, 10, 1, '#cfd6de'); R(-5, -20, 2, 4, '#9aa3ad'); R(-1, -26, 2, 3, '#d03030'); R(1, -25, 2, 2, '#d03030'); };
const HAT_MAGE = col => (R, g) => {
  g.fillStyle = col; g.beginPath(); g.moveTo(-6, -21); g.lineTo(6, -21); g.lineTo(-3, -32); g.fill();
  R(-7, -22, 14, 2, shade(col)); R(-5, -24, 10, 1, '#e0c040');
};
const HAT_ARCHER = R => { R(-5, -23, 9, 3, '#2f6a2f'); R(-5, -21, 2, 5, '#2f6a2f'); R(-5, -23, 9, 1, '#4a8a4a'); R(-7, -27, 1, 5, '#f4f4f4'); R(-6, -27, 1, 2, '#d03030'); };

function lookPlayer(e) {
  // 新手布衣維持職業原本的服裝顏色,更好的防具才會改變外觀
  const ar = e.a && e.a !== 'cloth' && S.items[e.a], wp = e.w && S.items[e.w];
  const hair = HAIRS[hashStr(e.n || '') % HAIRS.length];
  if (e.c === 'mage') return { skin: SKIN, hair, robe: true, body: ar ? ar.col : '#6a3fa0', head: HAT_MAGE(ar ? shade(ar.col) : '#4b2a80'), weapon: W_STAFF(wp ? wp.col : '#8ad0ff'), idleAng: 0.15 };
  if (e.c === 'archer') return { skin: SKIN, hair, body: ar ? ar.col : '#3f8a3f', legs: '#6b4f2f', head: HAT_ARCHER, weapon: W_BOW(wp ? tint(wp.col, -0.15) : '#8a5a2a'), idleAng: 0 };
  return { skin: SKIN, hair, body: ar ? ar.col : '#3b5fb0', legs: '#4a3a28', head: HAT_WARRIOR, weapon: W_SWORD(wp ? wp.col : '#cfd8e0'), swing: true };
}

const NPC_LOOK = {
  elder: { skin: SKIN, hair: '#dcdcdc', robe: true, body: '#7a5230', head: R => { R(-1, -16, 5, 4, '#f0f0f0'); R(0, -13, 3, 2, '#f0f0f0'); }, weapon: W_STAFF('#9be070'), idleAng: 0.1 },
  merchant: { skin: SKIN, hair: '#7a4a1c', body: '#b8482c', legs: '#4a3a28', torso: R => R(-3, -12, 6, 6, '#efe9d8'), head: R => { R(-5, -23, 10, 3, '#2a6ab0'); R(2, -21, 4, 1, '#2a6ab0'); } },
  healer: { skin: SKIN, robe: true, body: '#eeeeee', torso: R => { R(-1, -13, 2, 7, '#3a5ab0'); R(-3, -11, 6, 2, '#3a5ab0'); }, head: R => { R(-5, -22, 10, 3, '#3a5ab0'); R(-5, -20, 3, 8, '#3a5ab0'); R(-5, -22, 10, 1, '#fff'); } },
  wizard: { skin: SKIN, hair: '#999', robe: true, body: '#2c2c74', head: HAT_MAGE('#2c2c74'), weapon: W_STAFF('#40f0ff'), idleAng: 0.1 },
};

function drawBlob(g, x, y, col, t, size, id, sw) {
  const s = Math.sin(t / 1000 * 5 + id) * 0.1 + (sw > 0 ? Math.sin(sw * Math.PI) * 0.25 : 0);
  const w = 11 * size * (1 + s), h = 10 * size * (1 - s);
  g.save(); g.translate(Math.round(x), Math.round(y));
  g.fillStyle = 'rgba(0,0,0,.28)'; g.beginPath(); g.ellipse(0, 0, w, 3 * size, 0, 0, 7); g.fill();
  g.fillStyle = col; g.beginPath(); g.ellipse(0, -h, w, h, 0, 0, 7); g.fill();
  g.strokeStyle = shade(col); g.lineWidth = 1.5; g.stroke();
  g.fillStyle = 'rgba(255,255,255,.55)'; g.beginPath(); g.ellipse(-w * 0.4, -h * 1.45, w * 0.22, h * 0.18, -0.5, 0, 7); g.fill();
  g.fillStyle = '#222';
  g.fillRect(Math.round(-w * 0.35), Math.round(-h * 1.15), 2, 4); g.fillRect(Math.round(w * 0.25), Math.round(-h * 1.15), 2, 4);
  g.fillStyle = '#c03040'; g.fillRect(-2, Math.round(-h * 0.7), 4, 2);
  g.restore();
}

function drawWolf(g, x, y, e, t, sw) {
  g.save(); g.translate(Math.round(x), Math.round(y));
  g.fillStyle = 'rgba(0,0,0,.28)'; g.beginPath(); g.ellipse(0, 0, 18, 5, 0, 0, 7); g.fill();
  g.scale((e.f < 0 ? -1 : 1) * 2, 2);
  const ph = e.mv ? t / 1000 * 14 : 0, lp = e.mv ? Math.round(Math.sin(ph) * 1.5) : 0;
  g.translate(sw > 0 ? Math.round(Math.sin(sw * Math.PI) * 3) : 0, 0);
  const R = (x, y, w, h, c) => { g.fillStyle = c; g.fillRect(x, y, w, h); };
  const c = '#80858f', d = '#5e626b', l = '#a8adb6';
  R(-12, -11 + Math.round(Math.sin(t / 200)), 4, 2, d);
  R(-8 + lp, -5, 2, 5, d); R(2 + lp, -5, 2, 5, d);
  R(-9, -11, 15, 6, c); R(-9, -11, 15, 2, l); R(-7, -6, 11, 1, '#c8ccd2');
  R(-5 - lp, -5, 2, 5, c); R(5 - lp, -5, 2, 5, c);
  R(4, -15, 7, 6, c); R(4, -15, 7, 1, l); R(10, -12, 3, 3, l); R(12, -12, 1, 1, '#111');
  R(5, -17, 2, 2, d); R(8, -17, 2, 2, d); R(8, -13, 1, 1, '#ff3030');
  g.restore();
}

function drawDragon(g, x, y, e, t, sw) {
  g.save(); g.translate(Math.round(x), Math.round(y));
  g.fillStyle = 'rgba(0,0,0,.35)'; g.beginPath(); g.ellipse(0, 0, 54, 12, 0, 0, 7); g.fill();
  g.scale((e.f < 0 ? -1 : 1) * 3, 3);
  const fl = Math.sin(t / 1000 * 4);
  const P = (pts, col) => { g.fillStyle = col; g.beginPath(); g.moveTo(pts[0], pts[1]); for (let i = 2; i < pts.length; i += 2) g.lineTo(pts[i], pts[i + 1]); g.closePath(); g.fill(); };
  const R = (x, y, w, h, c) => { g.fillStyle = c; g.fillRect(x, y, w, h); };
  P([-2, -16, -10, -30 - fl * 5, -20, -26 - fl * 4, -16, -14], '#6a1812');
  P([-10, -9, -22, -4, -25, -1, -10, -5], '#a02a22');
  R(-8, -5, 4, 5, '#8a2018'); R(3, -5, 4, 5, '#8a2018');
  g.fillStyle = '#b8352b'; g.beginPath(); g.ellipse(-2, -10, 12, 7, 0, 0, 7); g.fill();
  g.fillStyle = '#e8a050'; g.beginPath(); g.ellipse(0, -7, 8, 3.5, 0, 0, 7); g.fill();
  for (let i = 0; i < 4; i++) P([-11 + i * 4, -15, -9 + i * 4, -19, -7 + i * 4, -15], '#efe2c2');
  const lg = sw > 0 ? Math.sin(sw * Math.PI) * 3 : 0;
  R(6, -20, 5, 10, '#b8352b');
  R(8 + lg, -26, 10, 7, '#c23a2f'); R(15 + lg, -21, 4, 2, '#a02a22');
  R(9 + lg, -30, 2, 4, '#efe2c2'); R(12 + lg, -29, 2, 3, '#efe2c2');
  R(14 + lg, -24, 2, 1, '#ffe040');
  if (sw > 0) { g.fillStyle = 'rgba(255,160,40,.8)'; g.beginPath(); g.arc(21 + lg, -21, 2 + sw * 3, 0, 7); g.fill(); }
  P([0, -15, 6, -32 - fl * 6, -6, -28 - fl * 5, -12, -16], '#8e2219');
  P([0, -15, 6, -32 - fl * 6, 2, -20], '#b03024');
  g.restore();
}

const GOBLIN_HEAD = R => { R(3, -21, 3, 2, '#7cbc4a'); R(-6, -20, 2, 2, '#6aa83c'); R(4, -17, 1, 2, '#6aa83c'); };
const RIBS = R => { for (let i = 0; i < 3; i++) R(-3, -12 + i * 2, 6, 1, '#8a8470'); R(-0.5, -13, 1, 6, '#8a8470'); };
const SKULL_EYES = R => { R(0, -18, 3, 2, '#2a0a0a'); R(1, -18, 1, 1, '#ff3a2a'); R(-1, -15, 5, 1, '#5a5648'); };

function atkProg(e, t) {
  if (!e.atkT) return 0;
  const k = (t - e.atkT) / 280;
  return k >= 0 && k < 1 ? k : 0;
}

function drawMob(g, e, x, y, t) {
  const sw = atkProg(e, t);
  switch (e.c) {
    case 'poring': return drawBlob(g, x, y, '#f49ac0', t, 1, e.i, sw);
    case 'slime': return drawBlob(g, x, y, '#6ccb4c', t, 1.15, e.i, sw);
    case 'goblin': return drawHumanoid(g, x, y, { scale: 1.8, face: e.f, walk: e.mv, atk: sw, swing: true, skin: '#7cbc4a', body: '#7a5a2a', legs: '#4a3a20', head: GOBLIN_HEAD, eyes: R => R(2, -18, 1, 2, '#f0e020'), weapon: W_CLUB }, t);
    case 'wolf': return drawWolf(g, x, y, e, t, sw);
    case 'skeleton': return drawHumanoid(g, x, y, { face: e.f, walk: e.mv, atk: sw, swing: true, skin: '#e8e3cf', body: '#d4cfba', legs: '#d4cfba', shoe: '#a8a290', belt: '#8a8470', torso: RIBS, eyes: SKULL_EYES, weapon: W_SWORD('#a07850') }, t);
    case 'dragon': return drawDragon(g, x, y, e, t, sw);
  }
}

function drawGrave(g, x, y) {
  g.save(); g.translate(Math.round(x), Math.round(y));
  g.fillStyle = 'rgba(0,0,0,.3)'; g.beginPath(); g.ellipse(0, 0, 12, 4, 0, 0, 7); g.fill();
  g.fillStyle = '#8a8a90'; g.fillRect(-9, -22, 18, 22); g.beginPath(); g.arc(0, -22, 9, Math.PI, 0); g.fill();
  g.fillStyle = '#b4b4ba'; g.fillRect(-9, -22, 3, 22);
  g.fillStyle = '#555'; g.fillRect(-1, -26, 2, 14); g.fillRect(-5, -22, 10, 2);
  g.restore();
}

// ============================================================
//  圖示 (道具 / 技能)
// ============================================================
const iconCanvas = {}, iconURL = {};
function iconC(id) {
  if (iconCanvas[id]) return iconCanvas[id];
  const it = S.items[id] || {}, col = it.col || '#ccc';
  const c = mkCanvas(32, 32), g = c.getContext('2d');
  g.scale(2, 2);
  const R = (x, y, w, h, cc) => { g.fillStyle = cc; g.fillRect(x, y, w, h); };
  if (it.icon === 'potion') {
    R(6, 1, 4, 2, '#8a5a2a'); R(6, 3, 4, 3, '#dfe8ef');
    g.fillStyle = col; g.beginPath(); g.arc(8, 10, 5, 0, 7); g.fill();
    g.strokeStyle = '#1a1a1a'; g.lineWidth = 0.7; g.stroke();
    R(5, 8, 2, 2, 'rgba(255,255,255,.75)');
  } else if (it.icon === 'sword') {
    g.translate(8, 8); g.rotate(Math.PI / 4);
    R(-1.2, -8, 2.4, 10, col); R(-1.2, -8, 1, 10, lighten(col));
    R(-3.5, 2, 7, 1.5, '#c9a227'); R(-0.75, 3.5, 1.5, 3, '#5a3a1a'); R(-1.25, 6.5, 2.5, 1.5, '#c9a227');
  } else if (it.icon === 'armor') {
    g.fillStyle = col; g.beginPath();
    [[3, 3], [6, 2], [8, 4], [10, 2], [13, 3], [14.5, 8], [12, 8.5], [12, 14], [4, 14], [4, 8.5], [1.5, 8]].forEach(([a, b], i) => i ? g.lineTo(a, b) : g.moveTo(a, b));
    g.closePath(); g.fill(); g.strokeStyle = '#1a1a1a'; g.lineWidth = 0.7; g.stroke();
    R(7.5, 5, 1, 8, shade(col)); R(4, 9, 8, 1, shade(col));
  }
  iconCanvas[id] = c;
  return c;
}
function icon(id) { return iconURL[id] || (iconURL[id] = iconC(id).toDataURL()); }

const SKILL_COL = { bash: ['#ffc060', '#a03a00'], whirl: ['#a0dcff', '#1a4a90'], fire: ['#ffe070', '#c02000'], ice: ['#e0f8ff', '#2a70c0'], arrow2: ['#c0f090', '#2a6a10'], rain: ['#f8f0a0', '#7a6a10'] };
function skillIcon(sk) {
  const c = mkCanvas(32, 32), g = c.getContext('2d'), cols = SKILL_COL[sk.fx] || ['#888', '#222'];
  const gr = g.createRadialGradient(12, 10, 2, 16, 16, 22);
  gr.addColorStop(0, cols[0]); gr.addColorStop(1, cols[1]);
  g.fillStyle = gr; g.fillRect(0, 0, 32, 32);
  g.strokeStyle = 'rgba(255,255,255,.5)'; g.strokeRect(1.5, 1.5, 29, 29);
  g.font = `bold 20px ${FONT}`; g.textAlign = 'center'; g.textBaseline = 'middle';
  g.lineWidth = 3; g.strokeStyle = 'rgba(0,0,0,.8)'; g.strokeText(sk.name[0], 16, 17);
  g.fillStyle = '#fff'; g.fillText(sk.name[0], 16, 17);
  return c.toDataURL();
}

// ============================================================
//  音效 (WebAudio 合成)
// ============================================================
let AC = null, muted = false;
function initAudio() { try { AC = AC || new (window.AudioContext || window.webkitAudioContext)(); AC.resume(); } catch (e) { AC = null; } }
function tone(type, f0, f1, dur, vol = 0.05, delay = 0) {
  if (!AC || muted) return;
  const t = AC.currentTime + delay, o = AC.createOscillator(), g = AC.createGain();
  o.type = type; o.frequency.setValueAtTime(f0, t); o.frequency.exponentialRampToValueAtTime(Math.max(20, f1), t + dur);
  g.gain.setValueAtTime(vol, t); g.gain.exponentialRampToValueAtTime(0.0008, t + dur);
  o.connect(g); g.connect(AC.destination); o.start(t); o.stop(t + dur + 0.02);
}
const SFX = {
  hit: () => tone('square', 260, 90, 0.07, 0.035),
  crit: () => { tone('square', 520, 120, 0.12, 0.05); tone('sawtooth', 900, 300, 0.08, 0.02); },
  hurt: () => tone('sawtooth', 180, 60, 0.13, 0.05),
  miss: () => tone('triangle', 500, 700, 0.06, 0.03),
  skill: () => tone('triangle', 300, 1100, 0.18, 0.06),
  pick: () => { tone('square', 880, 880, 0.05, 0.03); tone('square', 1320, 1320, 0.07, 0.03, 0.05); },
  lvl: () => [523, 659, 784, 1047].forEach((f, i) => tone('square', f, f, 0.16, 0.05, i * 0.1)),
  die: () => tone('sawtooth', 400, 40, 0.6, 0.06),
  heal: () => tone('sine', 600, 1200, 0.25, 0.05),
  click: () => tone('square', 1200, 1200, 0.02, 0.02),
};
const sfx = k => SFX[k] && SFX[k]();

// ============================================================
//  網路
// ============================================================
function connect(cb) {
  const ws = new WebSocket(`${location.protocol === 'https:' ? 'wss' : 'ws'}://${location.host}/ws`);
  S.ws = ws;
  ws.onopen = cb;
  ws.onmessage = ev => { let m; try { m = JSON.parse(ev.data); } catch (e) { return; } onMsg(m); };
  ws.onclose = () => {
    S.ws = null;
    if (S.myId) showOverlay('連線中斷', '與伺服器的連線中斷了。\n請確認伺服器是否仍在執行。', '重新連線', () => location.reload());
    else { $('#lg-err').textContent = '無法連線到伺服器,請確認 server.py 正在執行。'; $('#lg-btn').disabled = false; }
  };
}
function send(o) { if (S.ws && S.ws.readyState === 1) S.ws.send(JSON.stringify(o)); }

function onMsg(m) {
  switch (m.t) {
    case 'err':
      if (!S.myId) { $('#lg-err').textContent = m.m; $('#lg-btn').disabled = false; } else addChat(m.m, 'err');
      break;
    case 'welcome': startGame(m); break;
    case 'snap': applySnap(m); break;
    case 'inv': S.inv = m.inv; S.equip = m.eq; S.gold = m.g; renderInv(); break;
    case 'chat': onChat(m); break;
    case 'dlg': openDlg(m); break;
    case 'shop': openShop(m); break;
  }
}

// ============================================================
//  登入畫面
// ============================================================
let skyRAF = 0;
function initLogin() {
  for (const c of document.querySelectorAll('.cls canvas')) {
    const g = c.getContext('2d');
    drawHumanoid(g, 28, 54, { ...lookPlayer({ c: c.dataset.cls, n: c.dataset.cls }), scale: 2, face: 1 }, 0);
  }
  const sky = $('#sky'), g = sky.getContext('2d'), R = rng(42);
  const stars = Array.from({ length: 160 }, () => [R(), R() * 0.7, R() * 1.5 + 0.5, R() * 6]);
  const frame = t => {
    const w = sky.width = innerWidth, h = sky.height = innerHeight;
    const gr = g.createLinearGradient(0, 0, 0, h);
    gr.addColorStop(0, '#05081c'); gr.addColorStop(0.6, '#1a2458'); gr.addColorStop(1, '#4a3a6a');
    g.fillStyle = gr; g.fillRect(0, 0, w, h);
    for (const [x, y, s, p] of stars) { g.globalAlpha = 0.4 + 0.6 * Math.abs(Math.sin(t / 900 + p)); g.fillStyle = '#fff'; g.fillRect(x * w, y * h, s, s); }
    g.globalAlpha = 1;
    g.fillStyle = '#fff8d8'; g.beginPath(); g.arc(w * 0.82, h * 0.18, 34, 0, 7); g.fill();
    g.fillStyle = 'rgba(255,248,216,.08)'; g.beginPath(); g.arc(w * 0.82, h * 0.18, 70, 0, 7); g.fill();
    g.fillStyle = '#1a1838';
    g.beginPath(); g.moveTo(0, h);
    for (let x = 0; x <= w; x += 20) g.lineTo(x, h * 0.78 - Math.sin(x / 140) * 40 - Math.sin(x / 53) * 14);
    g.lineTo(w, h); g.fill();
    // 城堡剪影
    const cx = w * 0.16, by = h * 0.8;
    g.fillStyle = '#100e26';
    g.fillRect(cx - 60, by - 70, 120, 90); g.fillRect(cx - 80, by - 110, 30, 130); g.fillRect(cx + 50, by - 110, 30, 130); g.fillRect(cx - 15, by - 150, 30, 170);
    for (const [tx, tw, ty] of [[cx - 80, 30, by - 110], [cx + 50, 30, by - 110], [cx - 15, 30, by - 150]]) {
      g.beginPath(); g.moveTo(tx - 4, ty); g.lineTo(tx + tw / 2, ty - 34); g.lineTo(tx + tw + 4, ty); g.fill();
    }
    g.fillStyle = '#ffd860';
    for (const [x, y] of [[-68, -90], [58, -90], [-6, -125], [-30, -40], [20, -40]]) g.fillRect(cx + x, by + y, 5, 7);
    g.fillStyle = '#0a0918';
    g.beginPath(); g.moveTo(0, h);
    for (let x = 0; x <= w; x += 16) g.lineTo(x, h * 0.9 - Math.sin(x / 90 + 1) * 18);
    g.lineTo(w, h); g.fill();
    skyRAF = requestAnimationFrame(frame);
  };
  skyRAF = requestAnimationFrame(frame);

  const go = () => {
    const name = $('#lg-name').value.trim();
    if (name.length < 2) { $('#lg-err').textContent = '請輸入 2~12 個字的角色名稱'; return; }
    initAudio();
    $('#lg-btn').disabled = true;
    $('#lg-err').textContent = '連線中…';
    const msg = { t: 'login', name, pass: $('#lg-pass').value, cls: document.querySelector('input[name=cls]:checked').value };
    if (S.ws && S.ws.readyState === 1) send(msg); else connect(() => send(msg));
  };
  $('#lg-btn').onclick = go;
  for (const el of [$('#lg-name'), $('#lg-pass')]) el.addEventListener('keydown', e => { if (e.key === 'Enter') go(); });
  $('#lg-name').focus();
}

// ============================================================
//  進入遊戲
// ============================================================
let cv, ctx, mm, mmc;
function startGame(m) {
  cancelAnimationFrame(skyRAF);
  S.myId = m.id; S.myName = m.name; S.cls = m.cls; S.clsName = m.clsName;
  S.W = m.w; S.H = m.h;
  S.tiles = Uint8Array.from(m.tiles, ch => ch.charCodeAt(0) - 48);
  S.vars = Uint8Array.from({ length: S.W * S.H }, (_, i) => (hash2(i % S.W, (i / S.W) | 0) * 4) | 0);
  S.npcs = m.npcs; S.mobInfo = m.mobs; S.items = m.items; S.skills = m.skills;
  $('#login').hidden = true; $('#game').hidden = false;
  $('#st-name').textContent = m.name; $('#st-cls').textContent = m.clsName;
  cv = $('#view'); ctx = cv.getContext('2d'); mm = $('#minimap'); mmc = mm.getContext('2d');
  paintTrees(); buildMinimap(); buildHotbar(); bindInput(); resize();
  addEventListener('resize', resize);
  requestAnimationFrame(frame);
}

function resize() { cv.width = innerWidth; cv.height = innerHeight; ctx.imageSmoothingEnabled = false; }

function buildMinimap() {
  const COL = { 0: [76, 150, 55], 1: [45, 108, 192], 2: [28, 78, 30], 3: [210, 173, 114], 4: [170, 166, 155], 5: [90, 86, 80], 6: [90, 160, 70], 7: [58, 102, 48], 8: [148, 101, 58], 9: [110, 60, 50] };
  const c = mkCanvas(S.W, S.H), g = c.getContext('2d'), img = g.createImageData(S.W, S.H);
  for (let i = 0; i < S.tiles.length; i++) { const [r, gg, b] = COL[S.tiles[i]]; img.data.set([r, gg, b, 255], i * 4); }
  g.putImageData(img, 0, 0);
  S.mmBase = c;
}

// ============================================================
//  快照 / 特效
// ============================================================
function applySnap(m) {
  const t = performance.now(), seen = new Set();
  for (const e of m.e) {
    seen.add(e.i);
    let r = S.ents.get(e.i);
    if (!r) { r = { rx: e.x, ry: e.y, atkT: 0, hurtT: 0, bubble: null }; S.ents.set(e.i, r); }
    else if (Math.abs(r.rx - e.x) + Math.abs(r.ry - e.y) > 4) { r.rx = e.x; r.ry = e.y; }
    Object.assign(r, e);
  }
  const prevDead = S.me && S.me.dead;
  S.me = m.me;
  S.cdEnd = m.me.cd.map(c => t + c * 1000);
  for (const f of m.fx) handleFx(f, t);
  for (const id of [...S.ents.keys()]) if (!seen.has(id)) S.ents.delete(id);
  updateStatus();
  if (m.me.dead && !prevDead) {
    setTimeout(() => showOverlay('你已經死亡', '勝敗乃兵家常事,大俠請重新來過。', '在村莊復活', () => { send({ t: 'respawn' }); hideOverlay(); }), 900);
  }
}

const chest = e => [e.rx, e.ry - (S.mobInfo[e.c] && S.mobInfo[e.c].boss && e.k === 'm' ? 1.4 : 0.4)];

function handleFx(f, t) {
  const src = f.s && S.ents.get(f.s), tg = f.t && S.ents.get(f.t), mine = f.s === S.myId;
  switch (f.k) {
    case 'atk': {
      if (src) src.atkT = t;
      if (!src || !tg) break;
      const [sx, sy] = chest(src), [ex, ey] = chest(tg);
      const kind = { arrow: 'arrow', arrow2: 'arrow', magic: 'magic', fire: 'fire' }[f.w];
      if (kind) {
        const dur = clamp(Math.hypot(ex - sx, ey - sy) * 45, 120, 380);
        S.projs.push({ sx, sy, ex, ey, tid: tg.i, kind, t0: t, dur });
        if (f.w === 'arrow2') S.projs.push({ sx, sy, ex, ey, tid: tg.i, kind, t0: t + 110, dur });
        S.projEnd[f.s + '>' + tg.i] = t + dur + (f.w === 'arrow2' ? 110 : 0);
      } else if (f.w === 'melee' || f.w === 'bash' || f.w === 'bite') {
        S.impacts.push({ id: tg.i, kind: f.w === 'bash' ? 'bash' : 'slash', t0: t + 90, dur: 260 });
      }
      break;
    }
    case 'hit': {
      const e = S.ents.get(f.id);
      if (!e) break;
      const toMe = f.id === S.myId, byMe = f.s === S.myId;
      const delay = S.projEnd[f.s + '>' + f.id] || 0;
      const t0 = Math.max(t, delay > t ? delay : t);
      const [x, y] = chest(e);
      if (f.v === 0) S.floats.push({ x, y: y - 0.3, text: 'MISS', col: '#8fd0ff', size: 14, t0, dur: 900 });
      else S.floats.push({ x: x + (Math.random() - 0.5) * 0.4, y: y - 0.3, text: String(f.v), col: toMe ? '#ff5050' : f.c ? '#ffd23a' : byMe ? '#ffffff' : '#c8c8c8', size: f.c ? 22 : 16, t0, dur: 1000, crit: f.c });
      e.hurtT = t0;
      if (toMe) sfx(f.v ? 'hurt' : 'miss'); else if (byMe) sfx(f.v === 0 ? 'miss' : f.c ? 'crit' : 'hit');
      break;
    }
    case 'cast': {
      const e = S.ents.get(f.s);
      if (e) S.floats.push({ x: e.rx, y: e.ry - (e.k === 'm' && S.mobInfo[e.c] && S.mobInfo[e.c].boss ? 3.6 : 1.6), text: f.n + '!!', col: '#fff6a0', size: 14, t0: t, dur: 1100, font: FONT });
      if (mine || (e && e.k === 'm')) sfx('skill');
      break;
    }
    case 'aoe': S.aoes.push({ x: f.x, y: f.y, r: f.r, kind: f.w, t0: t, dur: f.w === 'breath' ? 900 : 750 }); break;
    case 'lvl': S.beams.push({ id: f.id, t0: t, dur: 1800 }); if (f.id === S.myId) sfx('lvl'); break;
    case 'heal': {
      const e = S.ents.get(f.id);
      if (e) S.floats.push({ x: e.rx, y: e.ry - 1.2, text: '+' + f.v, col: f.mp ? '#7ab8ff' : '#7cff7c', size: 15, t0: t, dur: 1000 });
      if (f.id === S.myId) sfx('heal');
      break;
    }
    case 'die': {
      const e = S.ents.get(f.id);
      if (e && e.k === 'm') { S.dying.push({ e: { ...e }, t0: t }); S.ents.delete(f.id); }
      if (f.id === S.myId) sfx('die');
      break;
    }
    case 'pick': if (f.id === S.myId) sfx('pick'); break;
    case 'tp': S.beams.push({ id: f.id, t0: t, dur: 900, tp: true }); break;
  }
}

// ============================================================
//  主迴圈
// ============================================================
let lastT = performance.now();
function frame(t) {
  const dt = Math.min(0.1, (t - lastT) / 1000);
  lastT = t;
  const k = 1 - Math.exp(-dt * 14);
  for (const e of S.ents.values()) { e.rx += (e.x - e.rx) * k; e.ry += (e.y - e.ry) * k; }
  updateHover();
  render(t);
  updateHotbar(t);
  requestAnimationFrame(frame);
}

const feet = e => [e.rx * TILE + S.ox, e.ry * TILE + S.oy + 8];

function render(t) {
  const vw = cv.width, vh = cv.height;
  ctx.fillStyle = '#0b0f08'; ctx.fillRect(0, 0, vw, vh);
  const me = S.ents.get(S.myId);
  const mw = S.W * TILE, mh = S.H * TILE;
  let camX = me ? me.rx * TILE : mw / 2, camY = me ? me.ry * TILE : mh / 2;
  camX = mw > vw ? clamp(camX, vw / 2, mw - vw / 2) : mw / 2;
  camY = mh > vh ? clamp(camY, vh / 2, mh - vh / 2) : mh / 2;
  const ox = S.ox = Math.round(vw / 2 - camX), oy = S.oy = Math.round(vh / 2 - camY);
  const tx0 = Math.max(0, Math.floor(-ox / TILE) - 1), ty0 = Math.max(0, Math.floor(-oy / TILE) - 1);
  const tx1 = Math.min(S.W - 1, Math.ceil((vw - ox) / TILE) + 1), ty1 = Math.min(S.H - 1, Math.ceil((vh - oy) / TILE) + 2);
  const sprites = [];

  // 地面
  for (let ty = ty0; ty <= ty1; ty++) {
    for (let tx = tx0; tx <= tx1; tx++) {
      const i = ty * S.W + tx, tt = S.tiles[i], sx = tx * TILE + ox, sy = ty * TILE + oy, v = S.vars[i];
      if (tt === T_WATER) drawWater(sx, sy, tx, ty, t);
      else if (tt === T_TREE) {
        const far = Math.hypot(tx - MAP_CX, ty - MAP_CY) > 36;
        ctx.drawImage(tileImg(far ? T_DARK : T_GRASS, v), sx, sy);
        sprites.push({ y: ty + 1, img: treeImgs[(far ? 2 : 0) + (v & 1)], sx: sx - 8, sy: sy - 30 });
      } else ctx.drawImage(tileImg(tt, v), sx, sy);
    }
  }

  // 點擊標記
  S.marks = S.marks.filter(m => t - m.t0 < 450);
  for (const m of S.marks) {
    const k = (t - m.t0) / 450;
    ctx.strokeStyle = `rgba(255,230,80,${1 - k})`; ctx.lineWidth = 2;
    ctx.beginPath(); ctx.ellipse(m.x * TILE + ox, m.y * TILE + oy, 12 * (1 - k) + 3, 6 * (1 - k) + 1.5, 0, 0, 7); ctx.stroke();
  }
  // 目標圈
  const tg = S.me && S.me.tg && S.ents.get(S.me.tg);
  if (tg) {
    const [x, y] = feet(tg), big = S.mobInfo[tg.c] && S.mobInfo[tg.c].boss ? 3 : 1;
    ctx.save(); ctx.strokeStyle = '#ff4040'; ctx.lineWidth = 2; ctx.setLineDash([6, 4]); ctx.lineDashOffset = -t / 40;
    ctx.beginPath(); ctx.ellipse(x, y, 16 * big, 6 * big, 0, 0, 7); ctx.stroke(); ctx.restore();
  }
  // 掉落物
  for (const e of S.ents.values()) {
    if (e.k !== 'd') continue;
    const x = e.rx * TILE + ox, y = e.ry * TILE + oy, b = Math.sin(t / 300 + e.i) * 2;
    ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.beginPath(); ctx.ellipse(x, y + 8, 9, 3, 0, 0, 7); ctx.fill();
    ctx.drawImage(iconC(e.c), x - 12, y - 14 + b, 24, 24);
  }

  for (const e of S.ents.values()) if (e.k !== 'd') sprites.push({ y: e.ry + 0.3, e });
  for (const n of S.npcs) sprites.push({ y: n.y + 0.3, n });
  S.dying = S.dying.filter(d => t - d.t0 < 700);
  for (const d of S.dying) sprites.push({ y: d.e.ry + 0.3, d });
  sprites.sort((a, b) => a.y - b.y);

  for (const s of sprites) {
    if (s.img) ctx.drawImage(s.img, s.sx, s.sy);
    else if (s.e) drawEntity(s.e, t);
    else if (s.n) drawHumanoid(ctx, s.n.x * TILE + ox, s.n.y * TILE + oy + 8, { ...NPC_LOOK[s.n.c], face: me && me.rx < s.n.x ? -1 : 1 }, t);
    else {
      const k = (t - s.d.t0) / 700, [x, y] = feet(s.d.e);
      ctx.globalAlpha = 1 - k;
      drawMob(ctx, { ...s.d.e, mv: 0 }, x, y + k * 6, t);
      ctx.globalAlpha = 1;
    }
  }
  drawEffects(t);
  drawLabels(t);
  drawMinimap(t);
}

function drawWater(x, y, tx, ty, t) {
  ctx.fillStyle = '#2d6cc0'; ctx.fillRect(x, y, 32, 32);
  ctx.fillStyle = '#4a8ad8';
  const ph = t / 700 + tx * 0.7 + ty * 1.3;
  for (let i = 0; i < 3; i++) ctx.fillRect(x + ((Math.sin(ph + i * 2.1) * 0.5 + 0.5) * 20 | 0), y + 5 + i * 10, 8, 2);
  if (ty > 0) {
    const up = S.tiles[(ty - 1) * S.W + tx];
    if (up !== T_WATER && up !== T_BRIDGE) { ctx.fillStyle = '#8fc0ee'; ctx.fillRect(x, y, 32, 3); }
  }
}

function drawEntity(e, t) {
  const [x, y] = feet(e);
  if (x < -120 || y < -150 || x > cv.width + 120 || y > cv.height + 150) return;
  const flash = t - e.hurtT < 140 && t >= e.hurtT;
  if (flash) ctx.globalAlpha = 0.55;
  if (e.k === 'p') {
    if (e.d) drawGrave(ctx, x, y);
    else drawHumanoid(ctx, x, y, { ...lookPlayer(e), face: e.f, walk: e.mv, atk: atkProg(e, t) }, t);
  } else if (e.k === 'm') drawMob(ctx, e, x, y, t);
  ctx.globalAlpha = 1;
}

function text(str, x, y, col = '#fff', size = 12, font = FONT, bold = false) {
  ctx.font = `${bold ? 'bold ' : ''}${size}px ${font}`;
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.lineJoin = 'round';
  ctx.lineWidth = 3; ctx.strokeStyle = 'rgba(0,0,0,.85)'; ctx.strokeText(str, x, y);
  ctx.fillStyle = col; ctx.fillText(str, x, y);
}
function bar(x, y, w, h, k, col) {
  ctx.fillStyle = '#000'; ctx.fillRect(x - 1, y - 1, w + 2, h + 2);
  ctx.fillStyle = '#3a1010'; ctx.fillRect(x, y, w, h);
  ctx.fillStyle = col; ctx.fillRect(x, y, Math.round(w * clamp(k, 0, 1)), h);
}

function drawLabels(t) {
  for (const n of S.npcs) {
    const x = n.x * TILE + S.ox, y = n.y * TILE + S.oy + 8;
    text(n.n, x, y + 12, '#9dff9d');
    const b = Math.round(Math.sin(t / 250) * 3);
    ctx.fillStyle = '#000'; ctx.fillRect(x - 3, y - 66 + b, 7, 13);
    ctx.fillStyle = '#ffd84a'; ctx.fillRect(x - 2, y - 65 + b, 5, 7); ctx.fillRect(x - 2, y - 56 + b, 5, 3);
  }
  for (const e of S.ents.values()) {
    if (e.k === 'd') {
      text(itemName(e.c), e.rx * TILE + S.ox, e.ry * TILE + S.oy + 16, '#a8dcff', 11);
      continue;
    }
    const [x, y] = feet(e);
    if (x < -100 || y < -150 || x > cv.width + 100 || y > cv.height + 100) continue;
    let head = y - 52;
    if (e.k === 'p') {
      const self = e.i === S.myId;
      text(e.n, x, y + 12, self ? '#fff1a8' : '#ffffff');
      if (S.hover === e) text(`Lv.${e.lv} ${({ warrior: '劍士', mage: '法師', archer: '弓手' })[e.c]}`, x, y + 26, '#c8d4f0', 11);
      if (self && S.me) { bar(x - 20, y + 20, 40, 4, S.me.hp / S.me.mh, '#3ad04a'); bar(x - 20, y + 26, 40, 3, S.me.mp / S.me.mm, '#3a8af0'); }
      else if (!e.d && e.hp < e.mh) bar(x - 18, y + 20, 36, 4, e.hp / e.mh, '#3ad04a');
    } else {
      const info = S.mobInfo[e.c] || {}, isTg = S.me && S.me.tg === e.i, hv = S.hover === e;
      head = y - (info.boss ? 110 : (e.c === 'poring' || e.c === 'slime') ? 30 : e.c === 'wolf' ? 40 : 50);
      if (hv || isTg || info.boss) text(`${info.boss ? '★ ' : ''}Lv.${info.lv} ${info.n}`, x, head - 8, info.boss ? '#ffcc33' : info.aggro ? '#ff9f80' : '#ffffff', info.boss ? 13 : 12, FONT, info.boss);
      if (e.hp < e.mh || isTg) bar(x - (info.boss ? 40 : 20), y + 6, info.boss ? 80 : 40, 4, e.hp / e.mh, '#e83a3a');
    }
    if (e.bubble && t < e.bubble.until) drawBubble(e.bubble.text, x, head - 14);
  }
}

function drawBubble(str, x, y) {
  ctx.font = `12px ${FONT}`;
  const lines = [];
  let cur = '';
  for (const ch of str) { if (ctx.measureText(cur + ch).width > 150) { lines.push(cur); cur = ch; } else cur += ch; }
  if (cur) lines.push(cur);
  const w = Math.max(...lines.map(l => ctx.measureText(l).width)) + 14, h = lines.length * 15 + 8;
  const bx = Math.round(x - w / 2), by = Math.round(y - h);
  ctx.fillStyle = 'rgba(255,255,255,.95)'; ctx.strokeStyle = '#333'; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.roundRect ? ctx.roundRect(bx, by, w, h, 6) : ctx.rect(bx, by, w, h); ctx.fill(); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(x - 5, by + h - 0.5); ctx.lineTo(x, by + h + 6); ctx.lineTo(x + 5, by + h - 0.5); ctx.fill();
  ctx.beginPath(); ctx.moveTo(x - 5, by + h); ctx.lineTo(x, by + h + 6); ctx.lineTo(x + 5, by + h); ctx.stroke();
  ctx.fillStyle = '#111'; ctx.textAlign = 'center'; ctx.textBaseline = 'top';
  lines.forEach((l, i) => ctx.fillText(l, x, by + 5 + i * 15));
}

function drawEffects(t) {
  const ox = S.ox, oy = S.oy;
  // 投射物
  S.projs = S.projs.filter(p => t < p.t0 + p.dur);
  for (const p of S.projs) {
    if (t < p.t0) continue;
    const k = (t - p.t0) / p.dur, tg = S.ents.get(p.tid);
    if (tg) [p.ex, p.ey] = chest(tg);
    const wx = p.sx + (p.ex - p.sx) * k, wy = p.sy + (p.ey - p.sy) * k;
    const x = wx * TILE + ox, y = wy * TILE + oy, ang = Math.atan2(p.ey - p.sy, p.ex - p.sx);
    if (p.kind === 'arrow') {
      ctx.save(); ctx.translate(x, y); ctx.rotate(ang);
      ctx.fillStyle = '#8a5a2a'; ctx.fillRect(-12, -1, 16, 2);
      ctx.fillStyle = '#e8e8e8'; ctx.beginPath(); ctx.moveTo(8, 0); ctx.lineTo(3, -3); ctx.lineTo(3, 3); ctx.fill();
      ctx.fillStyle = '#fff'; ctx.fillRect(-14, -3, 4, 2); ctx.fillRect(-14, 1, 4, 2);
      ctx.restore();
    } else {
      const fire = p.kind === 'fire', r = fire ? 9 : 6;
      for (let i = 3; i >= 0; i--) {
        const kk = Math.max(0, k - i * 0.06), tx = (p.sx + (p.ex - p.sx) * kk) * TILE + ox, ty = (p.sy + (p.ey - p.sy) * kk) * TILE + oy;
        const gr = ctx.createRadialGradient(tx, ty, 0, tx, ty, r * (1 - i * 0.2));
        gr.addColorStop(0, '#ffffff'); gr.addColorStop(0.35, fire ? '#ffb030' : '#c090ff'); gr.addColorStop(1, fire ? 'rgba(255,60,0,0)' : 'rgba(100,60,255,0)');
        ctx.globalAlpha = 1 - i * 0.22; ctx.fillStyle = gr; ctx.beginPath(); ctx.arc(tx, ty, r * (1 - i * 0.2), 0, 7); ctx.fill();
      }
      ctx.globalAlpha = 1;
    }
  }
  // 近戰衝擊
  S.impacts = S.impacts.filter(m => t < m.t0 + m.dur);
  for (const m of S.impacts) {
    if (t < m.t0) continue;
    const e = S.ents.get(m.id);
    if (!e) continue;
    const [wx, wy] = chest(e), x = wx * TILE + ox, y = wy * TILE + oy, k = (t - m.t0) / m.dur;
    ctx.save(); ctx.translate(x, y); ctx.globalAlpha = 1 - k;
    if (m.kind === 'bash') {
      ctx.fillStyle = '#ffb030'; ctx.beginPath();
      for (let i = 0; i < 16; i++) { const a = i / 16 * Math.PI * 2, r = (i % 2 ? 8 : 22) * (0.6 + k * 0.6); ctx.lineTo(Math.cos(a) * r, Math.sin(a) * r); }
      ctx.fill(); ctx.fillStyle = '#fff6c0'; ctx.beginPath(); ctx.arc(0, 0, 6, 0, 7); ctx.fill();
    } else {
      ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 3 * (1 - k) + 1;
      ctx.beginPath(); ctx.arc(-6, 6, 18, -1.6 + k * 0.6, -0.2 + k * 0.6); ctx.stroke();
    }
    ctx.restore();
  }
  // 範圍技能
  S.aoes = S.aoes.filter(a => t < a.t0 + a.dur);
  for (const a of S.aoes) {
    const k = (t - a.t0) / a.dur, cx = a.x * TILE + ox, cy = a.y * TILE + oy + 8, R = a.r * TILE;
    ctx.save(); ctx.globalAlpha = Math.min(1, (1 - k) * 1.6);
    if (a.kind === 'whirl') {
      ctx.translate(cx, cy - 10); ctx.scale(1, 0.55);
      for (let i = 0; i < 3; i++) {
        ctx.strokeStyle = i ? '#a8d8ff' : '#ffffff'; ctx.lineWidth = 6 - i * 1.5;
        ctx.beginPath(); ctx.arc(0, 0, R * (0.55 + 0.45 * k) - i * 8, k * 14 + i * 2.1, k * 14 + i * 2.1 + 1.6); ctx.stroke();
      }
    } else if (a.kind === 'ice') {
      ctx.fillStyle = 'rgba(140,210,255,.28)'; ctx.beginPath(); ctx.ellipse(cx, cy, R, R * 0.55, 0, 0, 7); ctx.fill();
      for (let i = 0; i < 14; i++) {
        const fx = cx + (hash2(i, 7) - 0.5) * R * 1.6, fy = cy + (hash2(i, 9) - 0.5) * R * 0.9, d = clamp(k * 3 - hash2(i, 3), 0, 1);
        const yy = fy - 90 * (1 - d);
        ctx.fillStyle = '#e8f8ff'; ctx.strokeStyle = '#4aa0e0'; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(fx, yy - 10); ctx.lineTo(fx + 4, yy); ctx.lineTo(fx, yy + 6); ctx.lineTo(fx - 4, yy); ctx.closePath(); ctx.fill(); ctx.stroke();
      }
    } else if (a.kind === 'rain') {
      ctx.strokeStyle = '#f0e0b0'; ctx.lineWidth = 2;
      for (let i = 0; i < 18; i++) {
        const fx = cx + (hash2(i, 5) - 0.5) * R * 1.6, fy = cy + (hash2(i, 6) - 0.5) * R * 0.9, d = clamp(k * 2.5 - hash2(i, 2), 0, 1);
        const yy = fy - 120 * (1 - d);
        ctx.beginPath(); ctx.moveTo(fx - 3, yy - 16); ctx.lineTo(fx, yy); ctx.stroke();
      }
      ctx.fillStyle = 'rgba(255,240,180,.15)'; ctx.beginPath(); ctx.ellipse(cx, cy, R, R * 0.55, 0, 0, 7); ctx.fill();
    } else if (a.kind === 'breath') {
      const gr = ctx.createRadialGradient(cx, cy - 20, 0, cx, cy - 20, R * (0.4 + k * 0.7));
      gr.addColorStop(0, 'rgba(255,250,200,.95)'); gr.addColorStop(0.4, 'rgba(255,140,30,.8)'); gr.addColorStop(1, 'rgba(200,20,0,0)');
      ctx.fillStyle = gr; ctx.beginPath(); ctx.ellipse(cx, cy - 20, R * (0.4 + k * 0.7), R * (0.3 + k * 0.45), 0, 0, 7); ctx.fill();
    }
    ctx.restore();
  }
  // 升級光柱 / 傳送光
  S.beams = S.beams.filter(b => t < b.t0 + b.dur);
  for (const b of S.beams) {
    const e = S.ents.get(b.id);
    if (!e) continue;
    const [x, y] = feet(e), k = (t - b.t0) / b.dur;
    ctx.save(); ctx.globalAlpha = k < 0.8 ? 1 : (1 - k) / 0.2;
    const gr = ctx.createLinearGradient(x - 22, 0, x + 22, 0);
    const c = b.tp ? '120,220,255' : '255,220,90';
    gr.addColorStop(0, `rgba(${c},0)`); gr.addColorStop(0.5, `rgba(${c},.7)`); gr.addColorStop(1, `rgba(${c},0)`);
    ctx.fillStyle = gr; ctx.fillRect(x - 22, y - 220, 44, 225);
    for (let i = 0; i < 8; i++) {
      const py = y - ((t / 4 + i * 37) % 160), pxx = x + Math.sin(i * 2 + t / 200) * 16;
      ctx.fillStyle = '#fff'; ctx.fillRect(pxx, py, 3, 3);
    }
    if (!b.tp) text('LEVEL UP!!', x, y - 70 - k * 40, '#ffe14a', 22, NUMFONT, true);
    ctx.restore();
  }
  // 浮動文字
  S.floats = S.floats.filter(f => t < f.t0 + f.dur);
  for (const f of S.floats) {
    if (t < f.t0) continue;
    const k = (t - f.t0) / f.dur;
    const x = f.x * TILE + ox, y = f.y * TILE + oy - k * 38 - (f.crit && k < 0.15 ? (0.15 - k) * 60 : 0);
    ctx.globalAlpha = k > 0.7 ? (1 - k) / 0.3 : 1;
    const sz = f.crit && k < 0.15 ? f.size * (1.6 - k * 4) : f.size;
    text(f.text, x, y, f.col, Math.round(sz), f.font || NUMFONT, true);
    ctx.globalAlpha = 1;
  }
}

function drawMinimap(t) {
  const s = mm.width / S.W;
  mmc.imageSmoothingEnabled = false;
  mmc.drawImage(S.mmBase, 0, 0, mm.width, mm.height);
  mmc.strokeStyle = 'rgba(255,255,255,.6)';
  mmc.strokeRect(-S.ox / TILE * s, -S.oy / TILE * s, cv.width / TILE * s, cv.height / TILE * s);
  for (const n of S.npcs) { mmc.fillStyle = '#5f5'; mmc.fillRect(n.x * s - 1, n.y * s - 1, 3, 3); }
  for (const e of S.ents.values()) {
    if (e.k === 'm') { mmc.fillStyle = S.mobInfo[e.c] && S.mobInfo[e.c].boss ? '#f0f' : '#f33'; mmc.fillRect(e.rx * s - 1, e.ry * s - 1, 2, 2); }
    else if (e.k === 'p' && e.i !== S.myId) { mmc.fillStyle = '#6cf'; mmc.fillRect(e.rx * s - 1, e.ry * s - 1, 3, 3); }
  }
  const me = S.ents.get(S.myId);
  if (me) {
    mmc.fillStyle = Math.floor(t / 300) % 2 ? '#ff0' : '#fff';
    mmc.fillRect(me.rx * s - 2, me.ry * s - 2, 4, 4);
    $('#coords').textContent = `(${me.x | 0}, ${me.y | 0})`;
  }
}

// ============================================================
//  輸入
// ============================================================
function screenToWorld(mx, my) { return [(mx - S.ox) / TILE, (my - S.oy) / TILE]; }

function pick(wx, wy) {
  let best = null, bd = 1e9;
  const test = (o, ex, ey, hw, top, bottom) => {
    const dx = wx - ex, dy = wy - ey;
    if (Math.abs(dx) < hw && dy > -top && dy < bottom) { const d = dx * dx + dy * dy * 0.3; if (d < bd) { bd = d; best = o; } }
  };
  for (const e of S.ents.values()) {
    if (e.i === S.myId) continue;
    if (e.k === 'd') test(e, e.rx, e.ry, 0.5, 0.55, 0.5);
    else if (e.k === 'm') { const boss = S.mobInfo[e.c] && S.mobInfo[e.c].boss; test(e, e.rx, e.ry + 0.25, boss ? 1.7 : 0.6, boss ? 3.4 : 1.5, 0.4); }
    else test(e, e.rx, e.ry + 0.25, 0.5, 1.5, 0.35);
  }
  for (const n of S.npcs) test({ ...n, k: 'n', ref: n }, n.x, n.y + 0.25, 0.55, 1.6, 0.35);
  return best;
}

const CURSOR_SVG = {
  normal: ["<svg xmlns='http://www.w3.org/2000/svg' width='22' height='22'><path d='M1 1 L1 17 L5 13 L8 20 L11 19 L8 12 L14 12 Z' fill='#f8d860' stroke='#5a3a00' stroke-width='1.3'/></svg>", '1 1'],
  atk: ["<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24'><path d='M2 2 L16 16' stroke='#222' stroke-width='5' stroke-linecap='round'/><path d='M2 2 L16 16' stroke='#eef4f8' stroke-width='3' stroke-linecap='round'/><path d='M11 19 L19 11' stroke='#5a3a00' stroke-width='4'/><path d='M11 19 L19 11' stroke='#e0b030' stroke-width='2'/><path d='M17 17 L22 22' stroke='#6b4423' stroke-width='3'/></svg>", '2 2'],
  talk: ["<svg xmlns='http://www.w3.org/2000/svg' width='24' height='22'><path d='M2 2 H22 V14 H10 L5 20 V14 H2 Z' fill='#fffbe0' stroke='#5a3a00' stroke-width='1.5'/><circle cx='7' cy='8' r='1.5'/><circle cx='12' cy='8' r='1.5'/><circle cx='17' cy='8' r='1.5'/></svg>", '2 2'],
  pick: ["<svg xmlns='http://www.w3.org/2000/svg' width='22' height='22'><path d='M1 1 L1 17 L5 13 L8 20 L11 19 L8 12 L14 12 Z' fill='#8fe0ff' stroke='#003a5a' stroke-width='1.3'/></svg>", '1 1'],
};
const CURSORS = {};
for (const [k, [svg, hs]] of Object.entries(CURSOR_SVG)) CURSORS[k] = `url("data:image/svg+xml,${encodeURIComponent(svg)}") ${hs}, auto`;
document.body.style.cursor = CURSORS.normal;

function updateHover() {
  if (!S.mouse.in) { S.hover = null; return; }
  const [wx, wy] = screenToWorld(S.mouse.x, S.mouse.y);
  S.hover = pick(wx, wy);
  const k = S.hover ? { m: 'atk', n: 'talk', d: 'pick' }[S.hover.k] || 'normal' : 'normal';
  if (cv.dataset.cur !== k) { cv.dataset.cur = k; cv.style.cursor = CURSORS[k]; }
}

function nearestMob(maxD) {
  const me = S.ents.get(S.myId);
  if (!me) return null;
  let best = null, bd = maxD;
  for (const e of S.ents.values()) {
    if (e.k !== 'm') continue;
    const d = Math.hypot(e.x - me.x, e.y - me.y);
    if (d < bd) { bd = d; best = e; }
  }
  return best;
}

function useHotkey(i) {
  if (!S.me || S.me.dead) return;
  if (i < 2) {
    const sk = S.skills[i];
    if (!sk) return;
    let tg = S.me.tg || 0;
    if (!tg && sk.kind !== 'self') { const n = nearestMob(9); if (n) tg = n.i; }
    send({ t: 'skill', n: i, tg });
  } else send({ t: 'use', item: i === 2 ? 'red_potion' : 'blue_potion' });
}

function bindInput() {
  const chatIn = $('#chat-in');
  cv.addEventListener('mousemove', e => { S.mouse.x = e.clientX; S.mouse.y = e.clientY; S.mouse.in = true; });
  cv.addEventListener('mouseleave', () => { S.mouse.in = false; });
  cv.addEventListener('contextmenu', e => e.preventDefault());
  cv.addEventListener('mousedown', e => {
    if (e.button !== 0) return;
    chatIn.blur(); initAudio();
    if (!S.me || S.me.dead) return;
    S.mouse.x = e.clientX; S.mouse.y = e.clientY; S.mouse.in = true;
    const [wx, wy] = screenToWorld(e.clientX, e.clientY), h = pick(wx, wy);
    if (h && h.k === 'm') send({ t: 'attack', id: h.i });
    else if (h && h.k === 'd') send({ t: 'pickup', id: h.i });
    else if (h && h.k === 'n') send({ t: 'npc', id: h.i });
    else {
      send({ t: 'move', x: wx, y: wy });
      S.marks.push({ x: Math.floor(wx) + 0.5, y: Math.floor(wy) + 0.5, t0: performance.now() });
    }
  });

  const MOVE = { w: [0, -1], arrowup: [0, -1], s: [0, 1], arrowdown: [0, 1], a: [-1, 0], arrowleft: [-1, 0], d: [1, 0], arrowright: [1, 0] };
  const updateDir = () => {
    let dx = 0, dy = 0;
    for (const k in S.keys) if (S.keys[k] && MOVE[k]) { dx += MOVE[k][0]; dy += MOVE[k][1]; }
    dx = clamp(dx, -1, 1); dy = clamp(dy, -1, 1);
    if (dx !== S.dir[0] || dy !== S.dir[1]) { S.dir = [dx, dy]; send({ t: 'dir', dx, dy }); }
  };
  addEventListener('keydown', e => {
    if (!S.myId) return;
    if (document.activeElement === chatIn) {
      if (e.key === 'Enter') { const v = chatIn.value.trim(); if (v) send({ t: 'chat', m: v }); chatIn.value = ''; chatIn.blur(); }
      else if (e.key === 'Escape') chatIn.blur();
      return;
    }
    const k = e.key.toLowerCase();
    if (k === 'enter') { e.preventDefault(); S.keys = {}; updateDir(); chatIn.focus(); return; }
    if (MOVE[k]) { e.preventDefault(); if (!S.keys[k]) { S.keys[k] = true; updateDir(); } return; }
    if (e.repeat) return;
    if (k >= '1' && k <= '4') useHotkey(+k - 1);
    else if (k === ' ') { e.preventDefault(); const n = nearestMob(12); if (n) send({ t: 'attack', id: n.i }); }
    else if (k === 'i') toggleWin('inv');
    else if (k === 'h') toggleWin('help');
    else if (k === 'm') toggleSound();
    else if (k === 'escape') for (const w of ['inv', 'help', 'dlg', 'shop']) closeWin(w);
  });
  addEventListener('keyup', e => { const k = e.key.toLowerCase(); if (S.keys[k]) { delete S.keys[k]; updateDir(); } });
  addEventListener('blur', () => { S.keys = {}; updateDir(); });

  for (const b of document.querySelectorAll('#menu [data-win]')) b.onclick = () => toggleWin(b.dataset.win);
  $('#btn-snd').onclick = toggleSound;
  for (const w of document.querySelectorAll('.win')) {
    w.querySelector('.x').onclick = () => closeWin(w.id.slice(4));
    makeDraggable(w);
  }
  // 提示框
  document.addEventListener('mousemove', e => {
    const tip = $('#tip'), el = e.target.closest && e.target.closest('[data-item],[data-skill],[data-shop]');
    if (!el) { tip.hidden = true; return; }
    tip.innerHTML = el.dataset.skill !== undefined ? skillTip(+el.dataset.skill) : itemTip(el.dataset.item || el.dataset.shop, !!el.dataset.shop);
    tip.hidden = false;
    tip.style.left = Math.min(e.clientX + 14, innerWidth - tip.offsetWidth - 4) + 'px';
    tip.style.top = Math.min(e.clientY + 14, innerHeight - tip.offsetHeight - 4) + 'px';
  });
}

function toggleSound() { muted = !muted; $('#btn-snd').textContent = '音效:' + (muted ? '關' : '開'); }

function makeDraggable(w) {
  const bar = w.querySelector('.title');
  bar.addEventListener('mousedown', e => {
    if (e.target.classList.contains('x')) return;
    const r = w.getBoundingClientRect(), dx = e.clientX - r.left, dy = e.clientY - r.top;
    const mv = ev => { w.style.left = (ev.clientX - dx) + 'px'; w.style.top = (ev.clientY - dy) + 'px'; w.style.right = 'auto'; w.style.marginLeft = '0'; };
    const up = () => { removeEventListener('mousemove', mv); removeEventListener('mouseup', up); };
    addEventListener('mousemove', mv); addEventListener('mouseup', up);
  });
}
function toggleWin(n) { const w = $('#win-' + n); w.hidden ? openWin(n) : closeWin(n); }
function openWin(n) { $('#win-' + n).hidden = false; sfx('click'); }
function closeWin(n) {
  const w = $('#win-' + n);
  if (!w || w.hidden) return;
  w.hidden = true;
  if (n === 'shop') S.shopOpen = false;
  if (n === 'dlg') clearInterval(S.twTimer);
  $('#tip').hidden = true;
}

// ============================================================
//  介面
// ============================================================
function setBar(k, v, max) {
  $('#bar-' + k).style.width = (max ? clamp(v / max, 0, 1) * 100 : 0) + '%';
  $('#txt-' + k).textContent = `${k.toUpperCase()} ${v} / ${max}`;
}
function updateStatus() {
  const m = S.me;
  if (!m) return;
  setBar('hp', m.hp, m.mh); setBar('mp', m.mp, m.mm);
  const pct = m.nx ? (m.exp / m.nx) * 100 : 0;
  $('#bar-xp').style.width = pct + '%';
  $('#txt-xp').textContent = `EXP ${pct.toFixed(1)}%`;
  if ($('#st-lv').textContent !== String(m.lv)) { $('#st-lv').textContent = m.lv; buildHotbar(); }
  $('#st-atk').textContent = m.atk; $('#st-def').textContent = m.def;
}

function buildHotbar() {
  const hb = $('#hotbar');
  hb.innerHTML = '';
  const lv = S.me ? S.me.lv : 1;
  S.skills.forEach((sk, i) => {
    const d = document.createElement('div');
    d.className = 'hk' + (lv < sk.lv ? ' locked' : '');
    d.dataset.skill = i;
    d.style.backgroundImage = `url(${sk._icon || (sk._icon = skillIcon(sk))})`;
    d.innerHTML = `<div class="cd"></div><span class="key">${i + 1}</span>` + (lv < sk.lv ? `<span class="lock">Lv${sk.lv}</span>` : '');
    d.onclick = () => useHotkey(i);
    hb.appendChild(d);
  });
  ['red_potion', 'blue_potion'].forEach((id, j) => {
    const d = document.createElement('div');
    d.className = 'hk'; d.dataset.item = id;
    d.style.backgroundImage = `url(${icon(id)})`;
    d.innerHTML = `<span class="key">${j + 3}</span><span class="cnt" id="hk-cnt-${id}"></span>`;
    d.onclick = () => useHotkey(j + 2);
    hb.appendChild(d);
  });
  updatePotionCounts();
}
function updatePotionCounts() {
  for (const id of ['red_potion', 'blue_potion']) {
    const el = $('#hk-cnt-' + id);
    if (el) el.textContent = S.inv.filter(s => s.id === id).reduce((a, s) => a + s.n, 0);
  }
}
function updateHotbar(t) {
  const els = document.querySelectorAll('#hotbar .hk .cd');
  S.skills.forEach((sk, i) => {
    if (!els[i]) return;
    const rem = Math.max(0, S.cdEnd[i] - t) / 1000;
    els[i].style.height = (rem > 0 ? Math.min(1, rem / sk.cd) * 100 : 0) + '%';
  });
}

function itemTip(id, shop) {
  const it = S.items[id];
  if (!it) return '';
  const type = { use: '消耗品', weapon: '武器', armor: '防具' }[it.type];
  let s = `<b>${esc(itemName(id))}</b><br><span class="t">${type}</span><br>`;
  if (it.hp) s += `<span class="s">恢復 HP ${it.hp}</span><br>`;
  if (it.mp) s += `<span class="s">恢復 MP ${it.mp}</span><br>`;
  if (it.atk) s += `<span class="s">攻擊力 +${it.atk}</span><br>`;
  if (it.def) s += `<span class="s">防禦力 +${it.def}</span><br>`;
  s += shop ? `<span class="p">售價 ${it.price} 金幣</span>` : `<span class="p">賣出價 ${Math.floor(it.price / 3)} 金幣</span>`;
  return s;
}
function skillTip(i) {
  const sk = S.skills[i];
  if (!sk) return '';
  return `<b>${esc(sk.name)}</b><br><span class="t">需求等級 Lv.${sk.lv} · 消耗 MP ${sk.mp} · 冷卻 ${sk.cd} 秒</span><br>${esc(sk.desc)}`;
}

function renderInv() {
  const grid = $('#inv-grid');
  grid.innerHTML = '';
  for (let i = 0; i < 24; i++) {
    const s = S.inv[i], d = document.createElement('div');
    d.className = 'slot';
    if (s) {
      d.dataset.item = s.id;
      d.style.backgroundImage = `url(${icon(s.id)})`;
      if (s.n > 1) d.innerHTML = `<span class="cnt">${s.n}</span>`;
      d.ondblclick = () => send({ t: 'use', slot: i });
      d.oncontextmenu = ev => {
        ev.preventDefault();
        if (S.shopOpen) send({ t: 'sell', slot: i });
        else addChat('要販賣物品,請先和道具商人莉莉對話並打開商店。', 'sys');
      };
    }
    grid.appendChild(d);
  }
  for (const k of ['weapon', 'armor']) {
    const el = $('#eq-' + k), id = S.equip[k];
    el.style.backgroundImage = id ? `url(${icon(id)})` : '';
    if (id) el.dataset.item = id; else delete el.dataset.item;
    el.ondblclick = () => id && send({ t: 'unequip', slot: k });
  }
  $('#inv-gold').textContent = S.gold.toLocaleString();
  $('#st-gold').textContent = S.gold.toLocaleString();
  const m = S.me;
  $('#inv-stats').innerHTML = m ? `攻擊力 <b>${m.atk}</b><br>防禦力 <b>${m.def}</b><br><small>雙擊裝備可卸下</small>` : '';
  updatePotionCounts();
  drawPortrait();
}

function drawPortrait() {
  const c = $('#portrait'), g = c.getContext('2d');
  g.clearRect(0, 0, c.width, c.height);
  g.imageSmoothingEnabled = false;
  drawHumanoid(g, 30, 74, { ...lookPlayer({ c: S.cls, n: S.myName, a: S.equip.armor, w: S.equip.weapon }), scale: 3, face: 1 }, 0);
}

function onChat(m) {
  if (m.ch === 'all') {
    const d = addChat('', 'all');
    d.innerHTML = `<b>${esc(m.n)}</b>:${esc(m.m)}`;
    const e = S.ents.get(m.i);
    if (e) e.bubble = { text: m.m, until: performance.now() + 5000 };
  } else if (m.ch === 'w') addChat(`[密語] ${m.n}:${m.m}`, 'w');
  else if (m.ch === 'ann') addChat(`【公告】${m.m}`, 'ann');
  else addChat(m.m, m.ch === 'err' ? 'err' : 'sys');
}
function addChat(str, cls) {
  const log = $('#chat-log'), d = document.createElement('div');
  d.className = 'msg ' + cls;
  d.textContent = str;
  const stick = log.scrollTop + log.clientHeight >= log.scrollHeight - 4;
  log.appendChild(d);
  while (log.children.length > 120) log.firstChild.remove();
  if (stick) log.scrollTop = log.scrollHeight;
  return d;
}

function openDlg(m) {
  S.dlg = m;
  $('#dlg-name').textContent = m.n;
  const el = $('#dlg-text');
  let i = 0;
  clearInterval(S.twTimer);
  el.textContent = '';
  S.twTimer = setInterval(() => { i++; el.textContent = m.text.slice(0, i); if (i >= m.text.length) clearInterval(S.twTimer); }, 28);
  el.onclick = () => { clearInterval(S.twTimer); el.textContent = m.text; };
  const opts = $('#dlg-opts');
  opts.innerHTML = '';
  for (const [act, label] of m.opts) {
    const b = document.createElement('button');
    b.textContent = '▶ ' + label;
    b.onclick = () => { if (act !== 'close') send({ t: 'dlg', npc: m.i, act }); closeWin('dlg'); };
    opts.appendChild(b);
  }
  openWin('dlg');
}

function openShop(m) {
  const list = $('#shop-list');
  list.innerHTML = '';
  for (const id of m.items) {
    const it = S.items[id], row = document.createElement('div');
    row.className = 'shop-row';
    row.innerHTML = `<div class="slot" data-shop="${id}" style="background-image:url(${icon(id)})"></div>
      <div class="nm">${esc(itemName(id))}<small>${it.hp ? 'HP +' + it.hp : it.mp ? 'MP +' + it.mp : it.atk ? '攻擊 +' + it.atk : '防禦 +' + it.def}</small></div>
      <div class="pr">${it.price}</div>`;
    const b = document.createElement('button');
    b.textContent = '購買';
    b.onclick = e => send({ t: 'buy', item: id, n: e.shiftKey && it.type === 'use' ? 10 : 1 });
    row.appendChild(b);
    list.appendChild(row);
  }
  S.shopOpen = true;
  openWin('shop');
  openWin('inv');
}

function showOverlay(title, msg, btn, fn) {
  $('#ov-title').textContent = title;
  $('#ov-text').textContent = msg;
  $('#ov-btn').textContent = btn;
  $('#ov-btn').onclick = fn;
  $('#overlay').hidden = false;
}
function hideOverlay() { $('#overlay').hidden = true; }

initLogin();
