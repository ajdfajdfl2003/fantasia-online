'use strict';
// ============================================================
//  幻想之境 Online — 繪圖 (全部用程式即時畫,不需要圖檔)
//  地圖圖塊、樹、角色、寵物、NPC、道具圖示
// ============================================================
const TILE = 32;
const FONT = '"PMingLiU","新細明體","MingLiU","Microsoft JhengHei",sans-serif';
const NUMFONT = 'Verdana,Tahoma,Arial,sans-serif';
const T_GRASS = 0, T_WATER = 1, T_TREE = 2, T_SAND = 3, T_STONE = 4, T_WALL = 5,
      T_FLOWER = 6, T_DARK = 7, T_BRIDGE = 8, T_ASH = 9;
const SKIN = '#f2c79c';
const HAIRS = ['#3a2412', '#1c1c1c', '#7a4a1c', '#c08a3a', '#a03020', '#d8c070', '#4a3a6a'];
const ELEMENT_COLORS = { earth: '#b08040', water: '#3a80e0', wind: '#50c080', fire: '#e85020', light: '#f0d040', dark: '#7040a0' };

// ---------- 小工具 ----------
const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
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
let NO_SHADOW = false;   // 跟隨寵物做動作時,影子由外面畫在地上,角色本身不畫影子
function shadow(g, rx, ry, a = 0.28) { if (NO_SHADOW) return; g.fillStyle = `rgba(0,0,0,${a})`; g.beginPath(); g.ellipse(0, 0, rx, ry, 0, 0, 7); g.fill(); }
function poly(g, pts, col) {
  g.fillStyle = col; g.beginPath(); g.moveTo(pts[0], pts[1]);
  for (let i = 2; i < pts.length; i += 2) g.lineTo(pts[i], pts[i + 1]);
  g.closePath(); g.fill();
}
function ell(g, x, y, rx, ry, col) { g.fillStyle = col; g.beginPath(); g.ellipse(x, y, rx, ry, 0, 0, 7); g.fill(); }

// ============================================================
//  圖塊與樹木
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
  if (treeImgs.length) return;
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
//  人形角色 (主人、NPC、哥布林、骷髏兵)
// ============================================================
function drawHumanoid(g, x, y, o, t) {
  const sc = o.scale || 2;
  g.save();
  g.translate(Math.round(x), Math.round(y));
  shadow(g, 6 * sc, 2.2 * sc, 0.3);
  g.scale((o.face < 0 ? -1 : 1) * sc, sc);
  const ph = o.walk ? t / 1000 * 11 : 0;
  const lp = o.walk ? Math.round(Math.sin(ph) * 1.5) : 0;
  const bob = o.walk && Math.abs(Math.sin(ph)) > 0.6 ? 1 : 0;
  const R = (x, y, w, h, c) => { g.fillStyle = c; g.fillRect(x, y, w, h); };
  g.translate(0, -bob);
  if (o.back) o.back(R, g);
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
  if (o.hair) {
    R(-4, -22, 8, 2, o.hair); R(-5, -21, 3, 6, o.hair); R(-2, -20, 2, 1, o.hair);
    if (o.long) { R(-5, -15, 3, 6, o.hair); R(-6, -18, 1, 8, o.hair); R(3, -21, 1, 4, o.hair); }   // 女角:長髮垂到背後,臉旁一撮
  }
  if (o.head) o.head(R, g);
  const sw = o.atk || 0;
  if (o.weapon) {
    g.save(); g.translate(3, -8);
    let ang = o.idleAng !== undefined ? o.idleAng : 0.5;
    if (sw > 0 && o.swing) ang = -1.3 + sw * 2.8;
    else if (sw > 0) ang -= Math.sin(sw * Math.PI) * 0.6;   // 施法時舉起武器
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
const W_HOLY = (R, g, sw) => {
  R(-0.5, -14, 1, 19, '#e8e0c0'); R(-0.5, -18, 1, 5, '#e0b030'); R(-2.5, -16.5, 5, 1, '#e0b030');
  if (sw > 0) { g.fillStyle = 'rgba(255,240,150,.5)'; g.beginPath(); g.arc(0, -16, 5 * (1 - sw) + 2, 0, 7); g.fill(); }
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
const W_LUTE = (R, g, sw) => {
  g.save(); g.rotate(-1.1);
  R(-0.5, -12, 1, 9, '#5a3a1a'); R(-1, -13, 2, 2, '#3a2a10');
  ell(g, 0, -1, 3.2, 4, '#b06a28'); ell(g, 0, -1, 1, 1, '#2a1a08');
  if (sw > 0) { g.fillStyle = '#ffe070'; g.fillRect(4, -8 - sw * 6, 2, 2); g.fillRect(6, -10 - sw * 8, 1, 3); }
  g.restore();
};
const HAT_KNIGHT = R => { R(-5, -23, 10, 4, '#9aa3ad'); R(-5, -23, 10, 1, '#cfd6de'); R(-5, -20, 2, 4, '#9aa3ad'); R(-1, -26, 2, 3, '#d03030'); R(1, -25, 2, 2, '#d03030'); };
const HAT_MAGE = col => (R, g) => {
  g.fillStyle = col; g.beginPath(); g.moveTo(-6, -21); g.lineTo(6, -21); g.lineTo(-3, -32); g.fill();
  R(-7, -22, 14, 2, shade(col)); R(-5, -24, 10, 1, '#e0c040');
};
const HAT_HUNTER = R => { R(-5, -23, 9, 3, '#2f6a2f'); R(-5, -21, 2, 5, '#2f6a2f'); R(-5, -23, 9, 1, '#4a8a4a'); R(-7, -27, 1, 5, '#f4f4f4'); R(-6, -27, 1, 2, '#d03030'); };
const HAT_PRIEST = R => { R(-4, -26, 8, 5, '#f4f2ea'); R(-3, -27, 6, 1, '#f4f2ea'); R(-4, -22, 8, 1, '#e0b030'); R(-0.5, -26, 1, 3, '#e0b030'); R(-5, -21, 2, 7, '#f4f2ea'); };
const HAT_BARD = R => { R(-5, -23, 10, 2, '#2a2a6a'); R(-4, -24, 8, 1, '#2a2a6a'); R(-6, -22, 3, 1, '#2a2a6a'); R(-7, -28, 1, 5, '#f0d040'); R(-6, -27, 1, 3, '#f0d040'); };
const SHIELD = R => { R(-8, -13, 4, 7, '#8a929c'); R(-8, -13, 4, 1, '#cfd6de'); R(-7, -11, 2, 3, '#d03030'); };

const CLASS_LOOK = {
  knight: hair => ({ skin: SKIN, hair, body: '#3b5fb0', legs: '#4a3a28', head: HAT_KNIGHT, back: SHIELD, weapon: W_SWORD('#cfd8e0'), swing: true }),
  hunter: hair => ({ skin: SKIN, hair, body: '#3f8a3f', legs: '#6b4f2f', head: HAT_HUNTER, weapon: W_BOW('#8a5a2a'), idleAng: 0 }),
  priest: hair => ({ skin: SKIN, hair, robe: true, body: '#f2f0e8', torso: R => { R(-0.5, -12, 1, 5, '#e0b030'); R(-2, -11, 4, 1, '#e0b030'); }, head: HAT_PRIEST, weapon: W_HOLY, idleAng: 0.1 }),
  mage: hair => ({ skin: SKIN, hair, robe: true, body: '#6a3fa0', head: HAT_MAGE('#4b2a80'), weapon: W_STAFF('#8ad0ff'), idleAng: 0.15 }),
  bard: hair => ({ skin: SKIN, hair, body: '#c04830', legs: '#3a2a5a', torso: R => R(-1, -13, 2, 6, '#f0d040'), head: HAT_BARD, weapon: W_LUTE, idleAng: 0.2 }),
};
function lookOwner(cls, name, sex) {
  const hair = HAIRS[hashStr(name || '') % HAIRS.length];
  return { ...(CLASS_LOOK[cls] || CLASS_LOOK.knight)(hair), long: sex === 'f' };
}

const NPC_LOOK = {
  elder: { skin: SKIN, hair: '#dcdcdc', robe: true, body: '#7a5230', head: R => { R(-1, -16, 5, 4, '#f0f0f0'); R(0, -13, 3, 2, '#f0f0f0'); }, weapon: W_STAFF('#9be070'), idleAng: 0.1 },
  merchant: { skin: SKIN, hair: '#7a4a1c', body: '#b8482c', legs: '#4a3a28', torso: R => R(-3, -12, 6, 6, '#efe9d8'), head: R => { R(-5, -23, 10, 3, '#2a6ab0'); R(2, -21, 4, 1, '#2a6ab0'); } },
  healer: { skin: SKIN, robe: true, body: '#eeeeee', torso: R => { R(-1, -13, 2, 7, '#3a5ab0'); R(-3, -11, 6, 2, '#3a5ab0'); }, head: R => { R(-5, -22, 10, 3, '#3a5ab0'); R(-5, -20, 3, 8, '#3a5ab0'); R(-5, -22, 10, 1, '#fff'); } },
  wizard: { skin: SKIN, hair: '#999', robe: true, body: '#2c2c74', head: HAT_MAGE('#2c2c74'), weapon: W_STAFF('#40f0ff'), idleAng: 0.1 },
  hatcher: { skin: '#e8b890', hair: '#c8c8c8', robe: true, body: '#8a5a9a', torso: R => { R(-4, -13, 8, 3, '#d8b860'); }, head: R => { R(-3, -25, 6, 3, '#c8c8c8'); R(2, -17, 1, 1, '#a07060'); }, weapon: R => { R(-0.5, -6, 1, 11, '#7a5030'); R(-0.5, -7, 3, 1, '#7a5030'); }, idleAng: 0.3 },
  keeper: { skin: SKIN, hair: '#c0602a', robe: true, body: '#e07890', torso: R => { R(-3, -12, 6, 6, '#fff4f0'); R(-3, -12, 6, 1, '#f0c8d0'); }, head: R => { R(-5, -24, 4, 3, '#ff5a8a'); R(-2, -23, 1, 1, '#ffd0e0'); }, weapon: R => { R(-2, -2, 5, 3, '#c89a50'); R(-2, -2, 5, 1, '#e8c070'); R(-1, -3, 3, 1, '#a05a30'); }, idleAng: 0 },
};

// ============================================================
//  心情泡泡與互動用的小圖示
// ============================================================
function heartPath(g, x, y, s) {
  g.beginPath(); g.moveTo(x, y + s * 0.35);
  g.bezierCurveTo(x, y - s * 0.15, x - s * 0.6, y - s * 0.2, x - s * 0.55, y + s * 0.15);
  g.bezierCurveTo(x - s * 0.5, y + s * 0.45, x - s * 0.1, y + s * 0.6, x, y + s * 0.8);
  g.bezierCurveTo(x + s * 0.1, y + s * 0.6, x + s * 0.5, y + s * 0.45, x + s * 0.55, y + s * 0.15);
  g.bezierCurveTo(x + s * 0.6, y - s * 0.2, x, y - s * 0.15, x, y + s * 0.35);
  g.closePath();
}
// 在 (x, y) 畫一個心情圖示,約 14×14
function drawMoodIcon(g, kind, x, y, t) {
  g.save();
  g.lineCap = 'round'; g.lineJoin = 'round';
  if (kind === 'love' || kind === 'heart') {
    heartPath(g, x, y - 6, 13); g.fillStyle = '#ff4a7a'; g.fill(); g.strokeStyle = '#a01040'; g.lineWidth = 1; g.stroke();
    g.fillStyle = 'rgba(255,255,255,.8)'; g.fillRect(x - 4, y - 4, 2, 2);
  } else if (kind === 'angry' || kind === 'anger') {   // 💢 青筋
    g.strokeStyle = '#e02020'; g.lineWidth = 2.2;
    for (const [sx, sy] of [[-1, -1], [1, -1], [-1, 1], [1, 1]]) {
      g.beginPath(); g.moveTo(x + sx * 6, y + sy * 2); g.quadraticCurveTo(x + sx * 2, y + sy * 2, x + sx * 2, y + sy * 6); g.stroke();
    }
  } else if (kind === 'hungry' || kind === 'starve' || kind === 'meat') {   // 🍖
    g.save(); g.translate(x, y); g.rotate(-0.6);
    g.fillStyle = '#f4f0e0'; g.fillRect(-1.5, 1, 3, 7); g.beginPath(); g.arc(-1.5, 8, 2, 0, 7); g.arc(1.5, 8, 2, 0, 7); g.fill();
    g.fillStyle = '#b0502a'; g.beginPath(); g.ellipse(0, -2, 5, 6, 0, 0, 7); g.fill();
    g.fillStyle = '#d8784a'; g.beginPath(); g.ellipse(-1.5, -4, 2, 2.5, 0, 0, 7); g.fill();
    g.restore();
    if (kind === 'starve') {
      g.strokeStyle = '#e02020'; g.lineWidth = 2.4;
      g.beginPath(); g.moveTo(x - 6, y - 6); g.lineTo(x + 6, y + 6); g.moveTo(x + 6, y - 6); g.lineTo(x - 6, y + 6); g.stroke();
    }
  } else if (kind === 'scared') {   // 💦 冷汗
    for (const [dx, dy, s] of [[-3, -1, 1], [4, 2, 0.75]]) {
      g.fillStyle = '#6ab8ff'; g.beginPath(); g.moveTo(x + dx, y + dy - 6 * s);
      g.quadraticCurveTo(x + dx + 4 * s, y + dy, x + dx, y + dy + 3 * s); g.quadraticCurveTo(x + dx - 4 * s, y + dy, x + dx, y + dy - 6 * s); g.fill();
      g.fillStyle = 'rgba(255,255,255,.8)'; g.fillRect(x + dx - 1, y + dy - 1, 1, 2);
    }
  } else if (kind === 'sleepy') {
    g.font = `bold 11px ${NUMFONT}`; g.textAlign = 'center'; g.textBaseline = 'middle';
    g.fillStyle = '#4a5ab0'; g.fillText('z', x - 3, y + 2); g.font = `bold 8px ${NUMFONT}`; g.fillText('z', x + 4, y - 3);
  } else if (kind === 'happy' || kind === 'note') {   // ♪
    g.fillStyle = '#ffb020'; g.strokeStyle = '#ffb020'; g.lineWidth = 1.6;
    g.beginPath(); g.ellipse(x - 2, y + 4, 3, 2.2, -0.4, 0, 7); g.fill();
    g.beginPath(); g.moveTo(x + 0.6, y + 3.6); g.lineTo(x + 0.6, y - 6); g.quadraticCurveTo(x + 4, y - 4, x + 5, y - 1); g.stroke();
  } else if (kind === 'flame') {
    const f = Math.sin(t / 60) * 1.2;
    poly(g, [x - 5, y + 5, x - 3, y - 3, x, y - 8 + f, x + 3, y - 3, x + 5, y + 5], '#ff7a20');
    poly(g, [x - 2.5, y + 5, x, y - 3 + f, x + 2.5, y + 5], '#ffe060');
  }
  g.restore();
}
// 對話泡泡底 + 圖示 (地圖與戰鬥中寵物頭上用)
function drawMoodBubble(g, kind, x, y, t) {
  if (kind === 'sleepy') {   // 打瞌睡不用泡泡,Z 會一直往上飄
    const k = (t / 1400) % 1;
    g.save(); g.globalAlpha = 1 - k;
    g.font = `bold 12px ${NUMFONT}`; g.textAlign = 'center'; g.textBaseline = 'middle';
    g.lineWidth = 3; g.strokeStyle = 'rgba(0,0,0,.6)';
    g.strokeText('Z', x + 4 + k * 8, y - k * 14); g.fillStyle = '#d8e4ff'; g.fillText('Z', x + 4 + k * 8, y - k * 14);
    g.font = `bold 9px ${NUMFONT}`; g.strokeText('z', x + 12 + k * 6, y - 8 - k * 10); g.fillText('z', x + 12 + k * 6, y - 8 - k * 10);
    g.restore();
    return;
  }
  const w = 22, h = 19, bx = Math.round(x - w / 2), by = Math.round(y - h);
  g.save();
  g.fillStyle = 'rgba(255,255,255,.95)'; g.strokeStyle = '#333'; g.lineWidth = 1;
  g.beginPath(); g.roundRect ? g.roundRect(bx, by, w, h, 6) : g.rect(bx, by, w, h); g.fill(); g.stroke();
  g.beginPath(); g.moveTo(x - 3, by + h - 0.5); g.lineTo(x - 1, by + h + 5); g.lineTo(x + 3, by + h - 0.5); g.fill();
  g.beginPath(); g.moveTo(x - 3, by + h); g.lineTo(x - 1, by + h + 5); g.lineTo(x + 3, by + h); g.stroke();
  drawMoodIcon(g, kind, x, by + h / 2 + 0.5, t);
  g.restore();
}

// ============================================================
//  寵物 / 怪物
// ============================================================
// 每種生物頭頂大約的高度 (像素),用來放名字、血條
const CREATURE_H = { poring: 26, slime: 28, imp: 40, goblin: 44, wolf: 36, fox: 38, skeleton: 50, dove: 44, bat: 44, griffin: 58, drake: 52, dragon: 110,
  silverwolf: 36, duskbird: 44 };
// 進化型態的樣子 (伺服器送來的 species[sp].look):{ from: 初階, filter: 濾鏡, scale: 放大, shine: 高階的金色光點 }
// 沒有自己的圖片時,用初階的樣子 (圖片或程式繪圖) 套濾鏡、放大
const LOOKS = {};
function setLooks(species) { for (const [k, v] of Object.entries(species || {})) if (v && (v.look || v.from)) LOOKS[k] = v.look || v; }

// ============================================================
//  圖片 (public/assets/):有圖用圖,沒圖退回程式繪圖
//  規格見 docs/art/美術規格.md:256×256 透明 WebP、腳底貼齊底邊正中央、朝右
// ============================================================
const ART = { on: true, imgs: {}, meta: {}, bust: {}, sizes: {}, count: 0, onload: null, ready: null, loaded: false };
try { ART.on = localStorage.getItem('fantasia.art') !== 'off'; } catch (e) { /* 沒有 localStorage 也沒關係 */ }

// 量出圖片實際內容的範圍 (用來算頭頂高度、影子寬度)
function measureArt(img) {
  const w = img.width, h = img.height, c = mkCanvas(w, h), g = c.getContext('2d');
  g.drawImage(img, 0, 0);
  const d = g.getImageData(0, 0, w, h).data;
  let top = h, l = w, r = 0;
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    if (d[(y * w + x) * 4 + 3] > 24) { if (y < top) top = y; if (x < l) l = x; if (x > r) r = x; }
  }
  if (r < l) { top = 0; l = 0; r = w - 1; }
  return { top: top / h, l: l / w, r: (r + 1) / w, pixel: w < 256 };
}
// 登入畫面就開始讀 (職業小圖要用主人圖),進遊戲時已經在讀就不重讀
function loadArt(sizes) {
  if (ART.ready) return ART.ready;
  ART.sizes = sizes || {};
  return (ART.ready = fetch('/assets.json', { cache: 'no-store' }).then(r => r.json()).then(m => {
    ART.sizes = m.art || ART.sizes;
    return Promise.all(m.files.map(f => new Promise(done => {
      const img = new Image(), key = f.p.replace(/\.webp$/i, '');
      img.onload = () => { ART.imgs[key] = img; ART.meta[key] = measureArt(img); done(); };
      img.onerror = () => done();   // 讀不到就算了,退回程式繪圖
      img.src = '/assets/' + f.p + '?v=' + f.v;
    })));
  }).then(() => {
    ART.count = Object.keys(ART.imgs).filter(k => !k.includes('_')).length;
    ART.loaded = true;
    if (ART.onload) ART.onload();
  }).catch(() => { ART.ready = null; }));   // 清單讀不到:進遊戲時再試一次
}
// 這個角色現在要用哪張圖 (可選動作圖:寵物的攻擊 / 受傷 / 睡著,主人的施法)
function artFor(key, o) {
  if (!ART.on || !ART.imgs[key]) return null;
  if (o.atk > 0 && ART.imgs[key + '_attack']) return ART.imgs[key + '_attack'];
  if (o.atk > 0 && !o.leanOnly && ART.imgs[key + '_cast']) return ART.imgs[key + '_cast'];
  if (o.hurt && ART.imgs[key + '_hurt']) return ART.imgs[key + '_hurt'];
  if (o.sleep && ART.imgs[key + '_sleep']) return ART.imgs[key + '_sleep'];
  return ART.imgs[key];
}
// 圖片實際畫出來的邊長:所有圖用同一個比例 (256 圖片像素 = size),動作圖的畫布比主圖大時就畫得比較大;
// 像素圖一律 2 倍不平滑放大
function artDrawSize(key, img, size) { return ART.meta[key] && ART.meta[key].pixel ? img.width * 2 : img.width * size / 256; }
// 把程式動畫套在圖片上:呼吸、走路彈跳、浮空、攻擊前傾、受傷閃白、倒下變灰、朝左翻轉
// o.owner:主人走路時左右微微搖擺 (每跳一步換邊),施法時在原地前傾、不往前衝
function drawArt(g, key, x, y, o, size, hover) {
  const img = artFor(key, o);
  if (!img) return false;
  const meta = ART.meta[key], t = o.t || 0, face = o.face || 1, sw = o.atk || 0, id = o.id || 0;
  const ds = artDrawSize(key, img, size);
  const breathe = Math.sin(t / 1000 * 3 + id) * 0.025;
  const hop = o.walk ? Math.abs(Math.sin(t / 1000 * 10)) * 3 : 0;
  const sway = o.owner && o.walk ? Math.sin(t / 1000 * 10) * 0.06 : 0;
  const hov = hover ? hover + Math.sin(t / 300 + id) * 2.5 : 0;
  const lunge = sw > 0 ? Math.sin(sw * Math.PI) : 0;
  g.save();
  g.translate(Math.round(x), Math.round(y));
  const cw = (meta.r - meta.l) * ds;
  shadow(g, Math.max(6, cw * 0.36), Math.max(2, cw * 0.1), hover ? 0.2 : 0.28);
  g.translate(o.owner ? 0 : lunge * 5 * face, -hop - hov);
  g.scale(face < 0 ? -1 : 1, 1);
  if (sway) g.rotate(sway);
  if (lunge && o.owner) g.rotate(lunge * 0.15);
  else if (lunge) { g.translate(0, -ds * 0.3); g.rotate(lunge * 0.14); g.translate(0, ds * 0.3); }
  g.scale(1 - breathe * 0.6, 1 + breathe);
  const f0 = g.filter && g.filter !== 'none' ? g.filter + ' ' : '';   // 進化型態的變色濾鏡要保留
  if (o.hurt) g.filter = f0 + 'brightness(2.4)';
  else if (o.ko) g.filter = f0 + 'grayscale(1)';
  g.imageSmoothingEnabled = !meta.pixel;
  if (!meta.pixel) g.imageSmoothingQuality = 'high';
  g.drawImage(img, -ds / 2, -ds, ds, ds);
  g.restore();
  return true;
}
// 頭頂高度 (放名字、血條、泡泡):有圖就依圖片內容計算
function creatureH(sp) {
  const key = 'pets/' + sp, img = ART.on && ART.imgs[key];
  if (img) {
    const a = ART.sizes[sp] || {}, ds = artDrawSize(key, img, a.size || 64);
    return Math.round((1 - ART.meta[key].top) * ds + (a.hover || 0));
  }
  const lk = LOOKS[sp];
  if (lk) return Math.round(creatureH(lk.from) * lk.scale);
  return CREATURE_H[sp] || 40;
}
// 身體寬度 (跟隨距離用):有圖就依圖片內容計算;pose = 'sleep' 等動作圖 (沒有那張圖就用主圖)
const CREATURE_W = { poring: 22, slime: 26, imp: 24, goblin: 22, wolf: 36, fox: 36, skeleton: 22, dove: 28, bat: 30, griffin: 48, drake: 44, dragon: 140,
  silverwolf: 36, duskbird: 28 };
function creatureW(sp, pose) {
  const base = 'pets/' + sp, key = pose && ART.imgs[base + '_' + pose] ? base + '_' + pose : base, img = ART.on && ART.imgs[key];
  if (img) { const m = ART.meta[key]; return Math.round((m.r - m.l) * artDrawSize(key, img, (ART.sizes[sp] || {}).size || 64)); }
  const lk = LOOKS[sp];
  if (lk) return Math.round(creatureW(lk.from, pose) * lk.scale);
  return CREATURE_W[sp] || 26;
}
// 地上的影子 (跟隨寵物做動作時用,大小和圖片版的影子一樣)
function creatureShadow(g, sp, x, y) {
  const w = creatureW(sp);
  g.save(); g.translate(Math.round(x), Math.round(y));
  shadow(g, Math.max(6, w * 0.36), Math.max(2, w * 0.1), (ART.sizes[sp] || {}).hover ? 0.2 : 0.28);
  g.restore();
}
function drawNpcArt(g, cls, x, y, face, t) {   // 每位 NPC 各自的大小:ART 的 npc_<代號> (spec 第 8 節)
  return drawArt(g, 'npcs/' + cls, x, y, { t, face, id: cls.length }, (ART.sizes['npc_' + cls] || {}).size || 52, 0);
}

// 主人 (spec 第 7 節):有圖用 owners/<職業>-<m|f>,沒圖用程式繪圖 (髮色依名字變、女角長髮)。
// 只有男版圖時女角也用程式繪圖,不拿男版代替。who 要有 c 職業、sx 性別、n 名字 (地圖快照、戰鬥單位都有)
const CAST_GLOW = { knight: '255,140,90', hunter: '130,255,160', priest: '255,235,140', mage: '170,160,255', bard: '255,215,90' };
const ownerKey = who => `owners/${who.c}-${who.sx === 'f' ? 'f' : 'm'}`;
function drawOwner(g, x, y, who, o, t) {
  const key = ownerKey(who), size = (ART.sizes.owner || {}).size || 52, face = o.face || 1;
  if (!drawArt(g, key, x, y, { ...o, t, id: (who.n || '').length, owner: true }, size, 0)) {
    drawHumanoid(g, x, y, { ...lookOwner(who.c, who.n, who.sx), ...o }, t);
    return;
  }
  if (!(o.atk > 0) || o.leanOnly) return;   // 用道具、封印卡、換寵只前傾,不發光
  const m = ART.meta[key], ds = artDrawSize(key, ART.imgs[key], size), k = Math.sin(o.atk * Math.PI);
  drawCastGlow(g, x + face * (m.r - m.l) * ds * 0.5, y - (1 - m.top) * ds * 0.55, CAST_GLOW[who.c] || CAST_GLOW.mage, k, t);
}
// 施法的光芒 (k:0 → 1 → 0):白色核心、職業色光暈、往外轉的光點
function drawCastGlow(g, x, y, rgb, k, t) {
  const r = 6 + k * 14, gr = g.createRadialGradient(x, y, 0, x, y, r);
  gr.addColorStop(0, `rgba(255,255,255,${0.9 * k})`); gr.addColorStop(0.4, `rgba(${rgb},${0.7 * k})`); gr.addColorStop(1, `rgba(${rgb},0)`);
  g.save();
  g.fillStyle = gr; g.beginPath(); g.arc(x, y, r, 0, 7); g.fill();
  g.fillStyle = `rgba(255,255,255,${k})`;
  for (let i = 0; i < 6; i++) {
    const a = i / 6 * Math.PI * 2 + t / 300, d = r * (0.6 + 0.6 * k);
    g.fillRect(Math.round(x + Math.cos(a) * d) - 1, Math.round(y + Math.sin(a) * d) - 1, 2, 2);
  }
  g.restore();
}
// 頭像 (左上角、戰鬥面板):有主人圖時取上半身,畫好回傳 true;沒圖時只清空畫布,回傳 false 讓呼叫的地方用程式繪圖
function drawOwnerBust(c, who) {
  const g = c.getContext('2d'), key = ownerKey(who), img = ART.on && ART.imgs[key];
  g.clearRect(0, 0, c.width, c.height);
  if (!img) return false;
  const b = ART.bust[key] || (ART.bust[key] = bustBox(img, ART.meta[key]));
  g.save();
  g.imageSmoothingEnabled = true; g.imageSmoothingQuality = 'high';
  g.drawImage(img, b.x, b.y, b.s, b.s, 0, 0, c.width, c.height);
  g.restore();
  return true;
}
// 上半身的範圍:從內容頂端往下取內容高度 55% 的正方形,水平對準這一段不透明像素的重心 (手上的杖、弓不會把臉擠到旁邊)
function bustBox(img, meta) {
  const w = img.width, h = img.height, top = Math.floor(meta.top * h), s = Math.max(8, Math.round((h - top) * 0.55));
  const c = mkCanvas(w, h), g = c.getContext('2d');
  g.drawImage(img, 0, 0);
  const d = g.getImageData(0, top, w, Math.min(s, h - top)).data;
  let sum = 0, n = 0;
  for (let i = 3; i < d.length; i += 4) if (d[i] > 24) { sum += (i >> 2) % w; n++; }
  const cx = n ? sum / n : w / 2;
  return { x: clamp(Math.round(cx - s / 2), 0, Math.max(0, w - s)), y: clamp(Math.round(top - s * 0.04), 0, Math.max(0, h - s)), s };
}

function drawCreature(g, sp, x, y, o) {
  const t = o.t || 0, sw = o.atk || 0, face = o.face || 1;
  g.save();
  const a = ART.sizes[sp], lk = LOOKS[sp];
  if (lk && !(ART.on && ART.imgs['pets/' + sp])) {   // 進化型態沒有自己的圖:用初階的樣子變色、放大 (倒下變淡由初階那層處理)
    g.translate(Math.round(x), Math.round(y));
    g.scale(lk.scale, lk.scale);
    const f0 = g.filter && g.filter !== 'none' ? g.filter + ' ' : '';
    g.filter = f0 + lk.filter;
    drawCreature(g, lk.from, 0, 0, o);
    g.filter = f0 || 'none';
    if (lk.shine && !o.ko) drawShine(g, creatureW(lk.from), creatureH(lk.from), t, o.id || 0);
    g.restore();
    return;
  }
  if (o.ko) { g.globalAlpha *= 0.45; }
  if (a && drawArt(g, 'pets/' + sp, x, y, o, a.size, a.hover || 0)) { g.restore(); return; }
  switch (sp) {
    case 'poring': drawBlob(g, x, y, '#f49ac0', t, 1, o.id || 0, sw); break;
    case 'slime': drawBlob(g, x, y, '#6ccb4c', t, 1.15, o.id || 0, sw); break;
    case 'imp': drawImp(g, x, y, face, t, sw); break;
    case 'goblin': drawHumanoid(g, x, y, { scale: 1.8, face, walk: o.walk, atk: sw, swing: true, skin: '#7cbc4a', body: '#7a5a2a', legs: '#4a3a20', head: GOBLIN_HEAD, eyes: R => R(2, -18, 1, 2, '#f0e020'), weapon: W_CLUB }, t); break;
    case 'wolf': drawWolf(g, x, y, face, t, o.walk, sw, WOLF_PAL); break;
    case 'fox': drawWolf(g, x, y, face, t, o.walk, sw, FOX_PAL); break;
    case 'skeleton': drawHumanoid(g, x, y, { face, walk: o.walk, atk: sw, swing: true, skin: '#e8e3cf', body: '#d4cfba', legs: '#d4cfba', shoe: '#a8a290', belt: '#8a8470', torso: RIBS, eyes: SKULL_EYES, weapon: W_SWORD('#a07850') }, t); break;
    case 'dove': drawBird(g, x, y, face, t, sw, DOVE_PAL, 2); break;
    case 'bat': drawBat(g, x, y, face, t, sw); break;
    case 'griffin': drawGriffin(g, x, y, face, t, o.walk, sw); break;
    case 'drake': drawDragon(g, x, y, face, t, sw, 1.25, DRAKE_PAL); break;
    case 'dragon': drawDragon(g, x, y, face, t, sw, 3, DRAGON_PAL); break;
    case 'silverwolf': drawWolf(g, x, y, face, t, o.walk, sw, SILVER_PAL); break;
    case 'duskbird': drawBird(g, x, y, face, t, sw, DUSK_PAL, 2); break;
    default: drawBlob(g, x, y, '#aaa', t, 1, 0, sw);
  }
  g.restore();
}

// 高階寵物身邊環繞的金色光點
function drawShine(g, w, h, t, id) {
  for (let i = 0; i < 4; i++) {
    const a = t / 700 + id + i * Math.PI / 2, x = Math.cos(a) * w * 0.62, y = -h * 0.5 + Math.sin(a) * h * 0.38;
    const k = 0.5 + 0.5 * Math.sin(t / 160 + i * 1.7), r = 1.5 + k * 2;
    g.globalAlpha = 0.45 + 0.55 * k;
    g.fillStyle = '#fff2a0';
    g.beginPath(); g.moveTo(x, y - r * 2); g.lineTo(x + r * 0.5, y - r * 0.5); g.lineTo(x + r * 2, y); g.lineTo(x + r * 0.5, y + r * 0.5);
    g.lineTo(x, y + r * 2); g.lineTo(x - r * 0.5, y + r * 0.5); g.lineTo(x - r * 2, y); g.lineTo(x - r * 0.5, y - r * 0.5); g.fill();
  }
  g.globalAlpha = 1;
}

function drawBlob(g, x, y, col, t, size, id, sw) {
  const s = Math.sin(t / 1000 * 5 + id) * 0.1 + (sw > 0 ? Math.sin(sw * Math.PI) * 0.25 : 0);
  const w = 11 * size * (1 + s), h = 10 * size * (1 - s);
  g.save(); g.translate(Math.round(x), Math.round(y));
  shadow(g, w, 3 * size);
  ell(g, 0, -h, w, h, col);
  g.strokeStyle = shade(col); g.lineWidth = 1.5; g.beginPath(); g.ellipse(0, -h, w, h, 0, 0, 7); g.stroke();
  g.fillStyle = 'rgba(255,255,255,.55)'; g.beginPath(); g.ellipse(-w * 0.4, -h * 1.45, w * 0.22, h * 0.18, -0.5, 0, 7); g.fill();
  g.fillStyle = '#222';
  g.fillRect(Math.round(-w * 0.35), Math.round(-h * 1.15), 2, 4); g.fillRect(Math.round(w * 0.25), Math.round(-h * 1.15), 2, 4);
  g.fillStyle = '#c03040'; g.fillRect(-2, Math.round(-h * 0.7), 4, 2);
  g.restore();
}

function drawImp(g, x, y, face, t, sw) {
  const hov = 6 + Math.sin(t / 300) * 2;
  g.save(); g.translate(Math.round(x), Math.round(y));
  shadow(g, 10, 3, 0.22);
  g.scale(face < 0 ? -2 : 2, 2);
  g.translate(sw > 0 ? Math.sin(sw * Math.PI) * 2 : 0, -hov / 2);
  // 火焰頭髮
  const fl = i => Math.sin(t / 90 + i * 1.7) * 1.2;
  poly(g, [-5, -9, -3, -17 + fl(0), -1, -10], '#ff9a20');
  poly(g, [-2, -10, 1, -20 + fl(1), 3, -10], '#ffb830');
  poly(g, [1, -9, 4, -16 + fl(2), 5, -8], '#ff9a20');
  poly(g, [-1, -10, 1, -15 + fl(3), 2, -10], '#fff0a0');
  ell(g, 0, -5, 6, 6, '#e8502a');
  ell(g, -1.5, -7, 2.5, 2, '#ff8a50');
  g.fillStyle = '#ffe040'; g.fillRect(1, -7, 2, 2); g.fillRect(-2, -7, 1, 2);
  g.fillStyle = '#3a0a00'; g.fillRect(2, -6, 1, 1);
  g.fillStyle = '#5a1a08'; g.fillRect(0, -3, 3, 1);
  poly(g, [-3, -10, -4, -13, -1, -10.5], '#3a2a20');
  poly(g, [3, -10, 4, -13, 1, -10.5], '#3a2a20');
  g.fillStyle = '#c03a18'; g.fillRect(-7, -5, 2, 2); g.fillRect(5, -5, 2, 2);
  g.restore();
}

const WOLF_PAL = { c: '#80858f', d: '#5e626b', l: '#a8adb6', belly: '#c8ccd2', eye: '#ff3030' };
const FOX_PAL = { c: '#d6e4f6', d: '#9fb4d0', l: '#f4f8ff', belly: '#ffffff', eye: '#3a80e0', fox: true };
const SILVER_PAL = { c: '#a9bcd8', d: '#6f84a8', l: '#dbe8fa', belly: '#eef4ff', eye: '#40b0ff' };   // 銀月狼 (混種)
function drawWolf(g, x, y, face, t, walk, sw, P) {
  g.save(); g.translate(Math.round(x), Math.round(y));
  shadow(g, 18, 5);
  g.scale((face < 0 ? -1 : 1) * 2, 2);
  const ph = walk ? t / 1000 * 14 : 0, lp = walk ? Math.round(Math.sin(ph) * 1.5) : 0;
  g.translate(sw > 0 ? Math.round(Math.sin(sw * Math.PI) * 3) : 0, 0);
  const R = (x, y, w, h, c) => { g.fillStyle = c; g.fillRect(x, y, w, h); };
  if (P.fox) {   // 蓬鬆的大尾巴
    g.save(); g.translate(-9, -10); g.rotate(-0.5 + Math.sin(t / 400) * 0.15);
    ell(g, -4, 0, 6, 3, P.c); ell(g, -9, 0, 2.5, 2.2, '#ffffff'); g.restore();
  } else R(-12, -11 + Math.round(Math.sin(t / 200)), 4, 2, P.d);
  R(-8 + lp, -5, 2, 5, P.d); R(2 + lp, -5, 2, 5, P.d);
  R(-9, -11, 15, 6, P.c); R(-9, -11, 15, 2, P.l); R(-7, -6, 11, 1, P.belly);
  R(-5 - lp, -5, 2, 5, P.c); R(5 - lp, -5, 2, 5, P.c);
  R(4, -15, 7, 6, P.c); R(4, -15, 7, 1, P.l); R(10, -12, 3, 3, P.l); R(12, -12, 1, 1, '#111');
  if (P.fox) { R(4, -19, 2, 4, P.c); R(8, -19, 2, 4, P.c); R(5, -18, 1, 2, '#f8b0c0'); R(9, -18, 1, 2, '#f8b0c0'); }
  else { R(5, -17, 2, 2, P.d); R(8, -17, 2, 2, P.d); }
  R(8, -13, 1, 1, P.eye);
  g.restore();
}

const DOVE_PAL = { body: '#f4f4f8', wing: '#d8d8e8', head: '#ffffff', tail: ['#f04040', '#f0c030', '#40c060', '#4080f0', '#a050e0'] };
const DUSK_PAL = { body: '#6a5a8c', wing: '#43345f', head: '#7c6ca0', tail: ['#ffb040', '#f07050', '#c050a0', '#7040b0', '#302868'] };   // 暮光鳥 (混種)
function drawBird(g, x, y, face, t, sw, P, sc) {
  const hov = 14 + Math.sin(t / 250) * 3;
  g.save(); g.translate(Math.round(x), Math.round(y));
  shadow(g, 10, 3, 0.2);
  g.scale((face < 0 ? -1 : 1) * sc, sc);
  g.translate(sw > 0 ? Math.sin(sw * Math.PI) * 4 : 0, -hov / sc);
  const flap = Math.sin(t / 70);
  P.tail.forEach((c, i) => poly(g, [-5, -6, -12, -9 + i * 1.6, -12, -7.4 + i * 1.6], c));
  poly(g, [-1, -9, -5, -15 - flap * 5, 3, -9], shade(P.wing));
  ell(g, 0, -6, 7, 4.5, P.body);
  ell(g, 6, -10, 3.5, 3.5, P.head);
  poly(g, [9, -10.5, 12, -9.5, 9, -8.5], '#f0b030');
  g.fillStyle = '#1a1a1a'; g.fillRect(7, -11, 1, 1);
  g.fillStyle = '#f08080'; g.fillRect(6, -9, 1, 1);
  poly(g, [-2, -8, -3, -16 - flap * 6, 4, -8], P.wing);
  g.restore();
}

function drawBat(g, x, y, face, t, sw) {
  const hov = 16 + Math.sin(t / 200) * 4;
  g.save(); g.translate(Math.round(x), Math.round(y));
  shadow(g, 9, 3, 0.2);
  g.scale((face < 0 ? -1 : 1) * 2, 2);
  g.translate(sw > 0 ? Math.sin(sw * Math.PI) * 4 : 0, -hov / 2);
  const f = Math.sin(t / 55);
  const wing = s => poly(g, [0, -6, s * 4, -10 - f * 3, s * 9, -12 - f * 5, s * 11, -6 - f * 2, s * 8, -5, s * 6, -3, s * 3, -4], '#4a2a5a');
  wing(-1); wing(1);
  ell(g, 0, -6, 3.5, 4, '#5a3470');
  poly(g, [-3, -9, -3, -13, -1, -9.5], '#5a3470'); poly(g, [3, -9, 3, -13, 1, -9.5], '#5a3470');
  g.fillStyle = '#ff3040'; g.fillRect(-2, -8, 1, 1); g.fillRect(1, -8, 1, 1);
  g.fillStyle = '#ffffff'; g.fillRect(-1, -5, 1, 1); g.fillRect(1, -5, 1, 1);
  g.restore();
}

function drawGriffin(g, x, y, face, t, walk, sw) {
  g.save(); g.translate(Math.round(x), Math.round(y));
  shadow(g, 22, 6);
  g.scale((face < 0 ? -1 : 1) * 2.4, 2.4);
  const lp = walk ? Math.round(Math.sin(t / 1000 * 12) * 1.5) : 0, fl = Math.sin(t / 300);
  g.translate(sw > 0 ? Math.sin(sw * Math.PI) * 3 : 0, 0);
  const R = (x, y, w, h, c) => { g.fillStyle = c; g.fillRect(x, y, w, h); };
  poly(g, [-2, -11, -10, -22 - fl * 3, -14, -16, -6, -10], '#8a5a2a');
  R(-12, -10, 3, 1, '#c89a50'); R(-14, -11, 2, 3, '#8a5a2a');
  R(-8 + lp, -5, 2, 5, '#b08040'); R(3 + lp, -5, 2, 5, '#b08040');
  R(-9, -11, 14, 7, '#d8a860'); R(-9, -11, 14, 2, '#e8c080');
  R(-6 - lp, -5, 2, 5, '#d8a860'); R(5 - lp, -5, 2, 5, '#f0d080'); R(5 - lp, -1, 3, 1, '#f0b030');
  R(4, -17, 6, 8, '#f8f8f8'); R(3, -15, 2, 5, '#e8e8e8');
  poly(g, [10, -15, 13, -13, 10, -11], '#f0b030');
  R(8, -15, 1, 1, '#1a1a1a');
  poly(g, [0, -11, 4, -24 - fl * 4, -6, -20 - fl * 3, -8, -11], '#a06a30');
  poly(g, [0, -11, 4, -24 - fl * 4, 1, -15], '#c08040');
  g.restore();
}

const DRAGON_PAL = { far: '#6a1812', tail: '#a02a22', leg: '#8a2018', body: '#b8352b', belly: '#e8a050', head: '#c23a2f', near: '#8e2219', near2: '#b03024', horn: '#efe2c2' };
const DRAKE_PAL = { far: '#b05a10', tail: '#d07020', leg: '#b05a18', body: '#e88030', belly: '#f8d080', head: '#f09040', near: '#c06018', near2: '#e07a28', horn: '#fff4d8' };
function drawDragon(g, x, y, face, t, sw, sc, P) {
  g.save(); g.translate(Math.round(x), Math.round(y));
  shadow(g, 18 * sc, 4 * sc, 0.35);
  g.scale((face < 0 ? -1 : 1) * sc, sc);
  const fl = Math.sin(t / 1000 * 4);
  const R = (x, y, w, h, c) => { g.fillStyle = c; g.fillRect(x, y, w, h); };
  poly(g, [-2, -16, -10, -30 - fl * 5, -20, -26 - fl * 4, -16, -14], P.far);
  poly(g, [-10, -9, -22, -4, -25, -1, -10, -5], P.tail);
  R(-8, -5, 4, 5, P.leg); R(3, -5, 4, 5, P.leg);
  ell(g, -2, -10, 12, 7, P.body);
  ell(g, 0, -7, 8, 3.5, P.belly);
  for (let i = 0; i < 4; i++) poly(g, [-11 + i * 4, -15, -9 + i * 4, -19, -7 + i * 4, -15], P.horn);
  const lg = sw > 0 ? Math.sin(sw * Math.PI) * 3 : 0;
  R(6, -20, 5, 10, P.body);
  R(8 + lg, -26, 10, 7, P.head); R(15 + lg, -21, 4, 2, P.tail);
  R(9 + lg, -30, 2, 4, P.horn); R(12 + lg, -29, 2, 3, P.horn);
  R(14 + lg, -24, 2, 1, '#ffe040');
  if (sw > 0) { g.fillStyle = 'rgba(255,160,40,.8)'; g.beginPath(); g.arc(21 + lg, -21, 2 + sw * 3, 0, 7); g.fill(); }
  poly(g, [0, -15, 6, -32 - fl * 6, -6, -28 - fl * 5, -12, -16], P.near);
  poly(g, [0, -15, 6, -32 - fl * 6, 2, -20], P.near2);
  g.restore();
}

const GOBLIN_HEAD = R => { R(3, -21, 3, 2, '#7cbc4a'); R(-6, -20, 2, 2, '#6aa83c'); R(4, -17, 1, 2, '#6aa83c'); };
const RIBS = R => { for (let i = 0; i < 3; i++) R(-3, -12 + i * 2, 6, 1, '#8a8470'); R(-0.5, -13, 1, 6, '#8a8470'); };
const SKULL_EYES = R => { R(0, -18, 3, 2, '#2a0a0a'); R(1, -18, 1, 1, '#ff3a2a'); R(-1, -15, 5, 1, '#5a5648'); };

function drawGrave(g, x, y) {
  g.save(); g.translate(Math.round(x), Math.round(y));
  shadow(g, 12, 4, 0.3);
  g.fillStyle = '#8a8a90'; g.fillRect(-9, -22, 18, 22); g.beginPath(); g.arc(0, -22, 9, Math.PI, 0); g.fill();
  g.fillStyle = '#b4b4ba'; g.fillRect(-9, -22, 3, 22);
  g.fillStyle = '#555'; g.fillRect(-1, -26, 2, 14); g.fillRect(-5, -22, 10, 2);
  g.restore();
}

// ============================================================
//  道具與技能圖示
// ============================================================
const iconCanvas = {}, iconURL = {};
function iconC(id, it) {
  if (iconCanvas[id]) return iconCanvas[id];
  it = it || {};
  const col = it.col || '#ccc', c = mkCanvas(32, 32), g = c.getContext('2d');
  g.scale(2, 2);
  const R = (x, y, w, h, cc) => { g.fillStyle = cc; g.fillRect(x, y, w, h); };
  if (it.icon === 'potion') {
    R(6, 1, 4, 2, '#8a5a2a'); R(6, 3, 4, 3, '#dfe8ef');
    g.fillStyle = col; g.beginPath(); g.arc(8, 10, 5, 0, 7); g.fill();
    g.strokeStyle = '#1a1a1a'; g.lineWidth = 0.7; g.stroke();
    R(5, 8, 2, 2, 'rgba(255,255,255,.75)');
  } else if (it.icon === 'herb') {
    R(7.5, 6, 1, 9, '#2a7a2a');
    [[4, 6, -0.6], [11, 5, 0.6], [5, 10, -0.5], [11, 10, 0.5], [8, 3, 0]].forEach(([x, y, a]) => {
      g.save(); g.translate(x, y); g.rotate(a); ell(g, 0, 0, 2, 3.4, col); ell(g, -0.5, -0.5, 0.6, 1.8, '#9af09a'); g.restore();
    });
  } else if (it.icon === 'card') {
    g.save(); g.translate(8, 8); g.rotate(-0.2);
    R(-5, -7, 10, 14, '#1a1028'); R(-4.5, -6.5, 9, 13, col); R(-3.5, -5.5, 7, 11, '#3a2060');
    g.strokeStyle = '#f0d060'; g.lineWidth = 0.8; g.beginPath(); g.arc(0, 0, 2.6, 0, 7); g.stroke();
    g.beginPath(); for (let i = 0; i < 5; i++) { const a = -Math.PI / 2 + i * Math.PI * 4 / 5; g.lineTo(Math.cos(a) * 2.6, Math.sin(a) * 2.6); } g.closePath(); g.stroke();
    g.restore();
  } else if (it.icon === 'egg') {
    g.fillStyle = '#f6f0dc'; g.beginPath(); g.ellipse(8, 9, 5.2, 6.4, 0, 0, 7); g.fill();
    g.strokeStyle = '#6a5a3a'; g.lineWidth = 0.6; g.stroke();
    g.fillStyle = col; [[6, 7, 1.6], [10, 9, 1.3], [7, 12, 1.2], [10, 5, 1]].forEach(([x, y, r]) => { g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); });
    R(5, 5, 1, 2, 'rgba(255,255,255,.9)');
  } else if (it.icon === 'food_meat') {
    g.save(); g.translate(8, 8); g.rotate(-0.7);
    R(-1, 2, 2, 6, '#f4f0e0'); ell(g, -1.2, 8, 1.4, 1.4, '#f4f0e0'); ell(g, 1.2, 8, 1.4, 1.4, '#f4f0e0');
    ell(g, 0, -1.5, 5, 5.5, '#c8402a');
    ell(g, -1.5, -3, 2, 2.2, '#f07a5a'); ell(g, 1.5, 0.5, 1.6, 1, '#f4e0d0');
    g.restore();
  } else if (it.icon === 'food_fish') {
    g.save(); g.translate(8, 8); g.rotate(-0.3);
    poly(g, [4, 0, 8, -4, 8, 4], '#3a70c0');
    ell(g, -1, 0, 6, 3.4, '#5a9ae0'); ell(g, -1, 1.2, 5, 1.6, '#d8ecff');
    R(-5, -1, 1, 1, '#1a1a1a'); R(-1, -3, 4, 1, '#3a70c0');
    g.restore();
  } else if (it.icon === 'food_berry') {
    poly(g, [8, 2, 11, 1, 10, 4], '#3a9a3a'); R(7.5, 2, 1, 4, '#5a7a2a');
    [[5.5, 9, '#a02880'], [10.5, 9, '#b83090'], [8, 12, '#c040a0'], [8, 7, '#d050b0']].forEach(([x, y, c]) => {
      ell(g, x, y, 2.6, 2.6, c); R(x - 1, y - 1.2, 1, 1, 'rgba(255,255,255,.8)');
    });
  } else if (it.icon === 'food_wheat') {
    R(7.5, 4, 1, 11, '#b08a30');
    for (let i = 0; i < 4; i++) { ell(g, 6.3, 4 + i * 2.2, 1.4, 1.1, '#f0c040'); ell(g, 9.7, 4 + i * 2.2, 1.4, 1.1, '#e0b030'); }
    ell(g, 8, 2.5, 1.2, 1.5, '#f8d860');
  } else if (it.icon === 'food_wood') {
    g.save(); g.translate(8, 9); g.rotate(-0.35);
    R(-6, -3, 11, 6, '#8a5a2a'); R(-6, -3, 11, 1, '#a87038'); R(-6, 2, 11, 1, '#6a4018');
    ell(g, 5, 0, 2.2, 3, '#d8b070'); ell(g, 5, 0, 1, 1.4, '#a07038');
    g.restore();
  } else if (it.icon === 'food_ore') {
    poly(g, [2, 12, 4, 6, 9, 4, 14, 7, 14, 12, 9, 14], '#7a7a8a');
    poly(g, [4, 6, 9, 4, 9, 9, 5, 10], '#9a9aaa');
    poly(g, [8, 7, 10, 3, 12, 7, 10, 10], '#ff8a40'); poly(g, [10, 3, 12, 7, 10, 6], '#ffd080');
    R(5, 11, 2, 1, '#5a5a6a');
  } else if (it.icon === 'sword') {
    g.translate(8, 8); g.rotate(Math.PI / 4);
    R(-1.2, -8, 2.4, 10, col); R(-1.2, -8, 1, 10, lighten(col));
    R(-3.5, 2, 7, 1.5, '#c9a227'); R(-0.75, 3.5, 1.5, 3, '#5a3a1a');
  } else {
    R(3, 3, 10, 10, col);
  }
  iconCanvas[id] = c;
  return c;
}
function iconURLof(id, it) { return iconURL[id] || (iconURL[id] = iconC(id, it).toDataURL()); }

const SKILL_COLORS = {
  slam: ['#ffc060', '#a03a00'], slash: ['#f0f0f0', '#606870'], poison: ['#c0f080', '#407010'], drain: ['#f08080', '#601020'],
  rock: ['#e0c080', '#6a4a20'], quake: ['#d0a060', '#5a3a10'], fire: ['#ffe070', '#c02000'], flamerain: ['#ffd060', '#a01800'],
  ice: ['#e0f8ff', '#2a70c0'], icicle: ['#c8f0ff', '#1a50a0'], wind: ['#c0ffd0', '#208050'], storm: ['#a0f0c0', '#106040'],
  laser: ['#ffffc0', '#c0a000'], holy: ['#fffff0', '#d0b040'], darkc: ['#d0a0ff', '#301050'], sleep: ['#e0d0ff', '#4a3a90'],
  debuff: ['#ffb0b0', '#702020'], heal: ['#c0ffc0', '#208030'], breath: ['#ffb040', '#901000'],
};
const OWNER_SKILL_COLORS = {
  buff: ['#ffd080', '#a05010'], debuff: ['#ffa0a0', '#701818'], bar: ['#b0f0ff', '#1a6090'], heal: ['#c0ffc0', '#208030'],
  shield: ['#d0e8ff', '#3050a0'], revive: ['#fff8c0', '#b09020'], weather: ['#ffe8a0', '#a06010'],
  mpall: ['#b0c8ff', '#2040a0'], sleep: ['#e0d0ff', '#4a3a90'], hasteall: ['#f0ffb0', '#608010'],
};
const skillIconCache = {};
function skillIcon(name, cols) {
  const key = name + cols.join();
  if (skillIconCache[key]) return skillIconCache[key];
  const c = mkCanvas(32, 32), g = c.getContext('2d');
  const gr = g.createRadialGradient(12, 10, 2, 16, 16, 22);
  gr.addColorStop(0, cols[0]); gr.addColorStop(1, cols[1]);
  g.fillStyle = gr; g.fillRect(0, 0, 32, 32);
  g.strokeStyle = 'rgba(255,255,255,.5)'; g.strokeRect(1.5, 1.5, 29, 29);
  g.font = `bold 18px ${FONT}`; g.textAlign = 'center'; g.textBaseline = 'middle';
  g.lineWidth = 3; g.strokeStyle = 'rgba(0,0,0,.8)'; g.strokeText(name[0], 16, 17);
  g.fillStyle = '#fff'; g.fillText(name[0], 16, 17);
  return (skillIconCache[key] = c.toDataURL());
}
