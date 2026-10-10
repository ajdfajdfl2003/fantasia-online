'use strict';
// ============================================================
//  幻想之境 Online — 客戶端核心:連線、狀態、畫面、戰鬥演出、輸入
//  (繪圖在 sprites.js,介面視窗在 ui.js)
// ============================================================
const $ = s => document.querySelector(s);
const MAP_CX = 48, MAP_CY = 48;

const S = {
  ws: null, myId: 0, myName: '', cls: '', W: 0, H: 0, tiles: null, vars: null, mmBase: null,
  ents: new Map(), npcs: [], battles: new Map(), uidx: new Map(), followers: new Map(),
  species: {}, classes: {}, pskills: {}, items: {}, elements: {}, statusNames: {}, weatherNames: {},
  hatchTime: 60, hatchWarmup: 20, petMax: 5,
  me: null, inv: [], gold: 0, pets: [], act: 0, hatch: null,
  myBattle: 0, target: 0, allyTarget: 0, auto: false,
  ox: 0, oy: 0, mouse: { x: -1, y: -1, in: false }, hover: null, keys: {}, dir: [0, 0],
  floats: [], projs: [], impacts: [], beams: [], marks: [], dying: [], banners: [], hitDelay: {},
  trans: null, shakeUntil: 0, camX: null, camY: null,
};

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
  hurt: () => tone('sawtooth', 180, 60, 0.13, 0.04),
  miss: () => tone('triangle', 500, 700, 0.06, 0.03),
  skill: () => tone('triangle', 300, 1100, 0.18, 0.05),
  heal: () => tone('sine', 600, 1200, 0.25, 0.05),
  pick: () => { tone('square', 880, 880, 0.05, 0.03); tone('square', 1320, 1320, 0.07, 0.03, 0.05); },
  lvl: () => [523, 659, 784, 1047].forEach((f, i) => tone('square', f, f, 0.16, 0.05, i * 0.1)),
  encounter: () => [330, 392, 494, 659, 494, 659].forEach((f, i) => tone('square', f, f, 0.08, 0.04, i * 0.06)),
  win: () => [523, 523, 523, 659, 784, 1047].forEach((f, i) => tone('square', f, f, i === 5 ? 0.4 : 0.1, 0.045, [0, .12, .24, .36, .5, .66][i])),
  lose: () => [392, 330, 262, 196].forEach((f, i) => tone('triangle', f, f, 0.25, 0.05, i * 0.22)),
  capture: () => [784, 988, 1175, 1568].forEach((f, i) => tone('sine', f, f, 0.15, 0.05, i * 0.08)),
  fail: () => tone('sawtooth', 300, 80, 0.3, 0.04),
  ready: () => tone('square', 1046, 1046, 0.04, 0.025),
  click: () => tone('square', 1200, 1200, 0.02, 0.02),
  egg: () => tone('sine', 140, 90, 0.12, 0.06),
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
    if (S.myId) UI.overlay('連線中斷', '與伺服器的連線中斷了。\n請確認伺服器是否仍在執行。', '重新連線', () => location.reload());
    else UI.loginError('無法連線到伺服器,請確認 server.py 正在執行。');
  };
}
function send(o) { if (S.ws && S.ws.readyState === 1) S.ws.send(JSON.stringify(o)); }

function onMsg(m) {
  switch (m.t) {
    case 'err': if (!S.myId) UI.loginError(m.m); else UI.addChat(m.m, 'err'); break;
    case 'welcome': startGame(m); break;
    case 'snap': applySnap(m); break;
    case 'inv': S.inv = m.inv; S.gold = m.g; UI.inv(); break;
    case 'pets': S.pets = m.pets; S.act = m.act; UI.pets(); break;
    case 'chat': UI.chat(m); break;
    case 'dlg': UI.dialog(m); break;
    case 'shop': UI.shop(m); break;
    case 'hatchui': UI.openHatch(); break;
    case 'hatch': onHatch(m); break;
    case 'hatched': S.hatch = null; UI.hatched(m.pet); sfx('lvl'); break;
    case 'petsell': UI.openPets(true); break;
    case 'bend': onBattleEnd(m); break;
  }
}

// ============================================================
//  進入遊戲
// ============================================================
let cv, ctx, mm, mmc;
function startGame(m) {
  S.myId = m.id; S.myName = m.name; S.cls = m.cls;
  S.W = m.w; S.H = m.h;
  S.tiles = Uint8Array.from(m.tiles, ch => ch.charCodeAt(0) - 48);
  S.vars = Uint8Array.from({ length: S.W * S.H }, (_, i) => (hash2(i % S.W, (i / S.W) | 0) * 4) | 0);
  Object.assign(S, { npcs: m.npcs, species: m.species, classes: m.classes, pskills: m.pskills, items: m.items,
    elements: m.elements, statusNames: m.statusNames, weatherNames: m.weather,
    hatchTime: m.hatchTime, hatchWarmup: m.hatchWarmup, petMax: m.petMax });
  cv = $('#view'); ctx = cv.getContext('2d'); mm = $('#minimap'); mmc = mm.getContext('2d');
  paintTrees(); buildMinimap();
  UI.enterGame(m);
  bindInput(); resize();
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
//  快照
// ============================================================
function applySnap(m) {
  const t = performance.now();
  // 地圖上的角色
  const seen = new Set();
  for (const e of m.e) {
    seen.add(e.i);
    let r = S.ents.get(e.i);
    if (!r) { r = { rx: e.x, ry: e.y, atkT: 0, bubble: null }; S.ents.set(e.i, r); }
    else if (Math.abs(r.rx - e.x) + Math.abs(r.ry - e.y) > 4) { r.rx = e.x; r.ry = e.y; S.followers.delete(e.i); }
    Object.assign(r, e);
  }
  // 戰鬥
  const bseen = new Set(), useen = new Set();
  for (const b of m.bt) {
    bseen.add(b.i);
    let rb = S.battles.get(b.i);
    if (!rb) { rb = { t0: t, units: new Map() }; S.battles.set(b.i, rb); }
    Object.assign(rb, { i: b.i, x: b.x, y: b.y, w: b.w, boss: b.boss, np: b.np });
    for (const u of b.u) {
      useen.add(u.i);
      let ru = rb.units.get(u.i);
      if (!ru) { ru = { atkT: 0, hurtT: 0, lunge: null, joinT: t }; rb.units.set(u.i, ru); }
      const wasReady = ru.rd;
      Object.assign(ru, u);
      ru.barT = t;
      ru.b = rb;
      S.uidx.set(u.i, ru);
      if (u.rd && !wasReady && u.pid === S.myId) sfx('ready');
    }
    rb.maxRow = Math.max(0, ...b.u.filter(u => u.s === 1).map(u => u.r));
  }
  const prevBattle = S.myBattle;
  S.me = m.me;
  S.myBattle = m.me.bt;
  if (S.myBattle && S.myBattle !== prevBattle) onMyBattleStart(t);
  for (const f of m.fx) handleFx(f, t);
  // 移除消失的單位 / 戰鬥 / 角色 (放在特效之後,最後一擊的傷害數字才看得到)
  for (const [id, rb] of S.battles) {
    for (const [uid, ru] of rb.units) {
      if (!useen.has(uid)) {
        rb.units.delete(uid); S.uidx.delete(uid);
        if (!ru.capT) S.dying.push({ u: { ...ru }, pos: unitPos(rb, ru), t0: t });
      }
    }
    if (!bseen.has(id)) S.battles.delete(id);
  }
  for (const id of [...S.ents.keys()]) if (!seen.has(id)) { S.ents.delete(id); S.followers.delete(id); }
  if (!S.target || !aliveEnemy(S.target)) autoTarget();
  UI.status();
}

function myBattle() { return S.battles.get(S.myBattle); }
function myUnits() {
  const rb = myBattle();
  let o = null, p = null;
  if (rb) for (const u of rb.units.values()) { if (u.pid === S.myId) { if (u.k === 'o') o = u; else if (u.k === 'p') p = u; } }
  return { rb, o, p };
}
function aliveEnemy(uid) { const u = S.uidx.get(uid); return u && u.s === 1 && !u.ko && u.b && u.b.i === S.myBattle; }
function autoTarget() {
  const rb = myBattle();
  if (!rb) { S.target = 0; return; }
  const foes = [...rb.units.values()].filter(u => u.s === 1 && !u.ko).sort((a, b) => a.r - b.r);
  setTarget(foes.length ? foes[0].i : 0);
}
function setTarget(uid) {
  if (S.target === uid) return;
  S.target = uid;
  if (uid) send({ t: 'btarget', id: uid });
}
function cycleTarget() {
  const rb = myBattle();
  if (!rb) return;
  const foes = [...rb.units.values()].filter(u => u.s === 1 && !u.ko).sort((a, b) => a.r - b.r);
  if (!foes.length) return;
  const i = foes.findIndex(u => u.i === S.target);
  setTarget(foes[(i + 1) % foes.length].i);
}

function onMyBattleStart(t) {
  S.trans = { t0: t, boss: !!(myBattle() || {}).boss };
  S.allyTarget = 0;
  S.target = 0;
  S.keys = {}; S.dir = [0, 0];
  sfx('encounter');
  UI.battleOpen();
}
function onBattleEnd(m) {
  const t = performance.now();
  if (m.win === 1) { S.banners.push({ text: '勝 利 !', sub: `經驗值 +${m.exp}   金幣 +${m.gold}` + (m.items && m.items.length ? '   ' + m.items.join('、') : ''), col: '#ffe14a', t0: t, dur: 2600 }); sfx('win'); }
  else if (m.win === 0) { S.banners.push({ text: '戰 敗 ……', sub: '被送回了村莊', col: '#ff7a6a', t0: t, dur: 2600 }); sfx('lose'); }
  else S.banners.push({ text: '逃跑成功', sub: '', col: '#bfe0ff', t0: t, dur: 1500 });
  S.myBattle = 0; S.target = 0; S.allyTarget = 0;
  UI.battleClose();
}

function onHatch(m) {
  const prevBeat = S.hatch ? S.hatch.beatT : 0;
  S.hatch = m;
  S.hatch.beatT = prevBeat;
  UI.hatchUpdate();
}

// ============================================================
//  戰鬥站位
// ============================================================
// 回傳單位腳底的世界座標
function unitPos(rb, u) {
  if (u.s === 0) {
    const n = Math.max(1, rb.np || 1), y = rb.y + (u.r - (n - 1) / 2) * 1.75;
    return u.k === 'o' ? [rb.x - 3.1, y] : [rb.x - 1.2, y];
  }
  if (u.boss) return [rb.x + 2.5, rb.y + 0.5];
  const m = (rb.maxRow || 0) + 1;
  return [rb.x + 1.3 + (u.r % 2) * 1.1, rb.y + (u.r - (m - 1) / 2) * 1.05];
}
function unitH(u) { return u.k === 'o' ? 50 : (CREATURE_H[u.c] || 40); }
function unitDrawPos(u, t) {
  let [x, y] = unitPos(u.b, u);
  if (u.lunge) {
    const k = (t - u.lunge.t0) / 360;
    if (k >= 1) u.lunge = null;
    else if (k >= 0) {
      const e = k < 0.5 ? k * 2 : (1 - k) * 2, ease = e * e * (3 - 2 * e);
      x += (u.lunge.tx - x) * 0.7 * ease; y += (u.lunge.ty - y) * 0.7 * ease;
    }
  }
  return [x, y];
}
function unitChest(u, t) { const [x, y] = unitDrawPos(u, t); return [x, y - unitH(u) * 0.5 / TILE]; }
function unitHead(u, t) { const [x, y] = unitDrawPos(u, t); return [x, y - unitH(u) / TILE]; }
function unitBar(u, t) { return u.rd ? 100 : Math.min(100, u.bar + (u.rt || 0) * (t - (u.barT || t)) / 1000); }

// ============================================================
//  特效
// ============================================================
const PROJ = { fire: 'fire', ice: 'ice', wind: 'wind', sleep: 'magic', debuff: 'magic', poison: null, owner_seal: 'card' };
const MELEE = new Set(['melee', 'slam', 'slash', 'poison', 'drain', 'bite']);
const AOE_IMPACT = { flamerain: 'meteor', icicle: 'ice', storm: 'wind', holy: 'holy', darkc: 'dark', quake: 'rock', breath: 'burst' };
const SINGLE_IMPACT = { fire: 'burst', ice: 'ice', wind: 'wind', laser: 'burst', rock: 'rock', slam: 'slam', bite: 'slam', poison: 'poison', drain: 'drain' };

function handleFx(f, t) {
  if (f.b !== undefined) return battleFx(f, t);
  const e = S.ents.get(f.id);
  switch (f.k) {
    case 'lvl': S.beams.push({ id: f.id, t0: t, dur: 1800, hatch: f.hatch }); if (f.id === S.myId && !f.hatch) sfx('lvl'); break;
    case 'tp': S.beams.push({ id: f.id, t0: t, dur: 900, tp: true }); break;
    case 'heal':
      if (e) S.floats.push({ x: e.rx, y: e.ry - 1.2, text: f.big ? '完全恢復!' : '+' + f.v, col: f.mp ? '#7ab8ff' : '#7cff7c', size: 15, t0: t, dur: 1100, font: f.big ? FONT : null });
      if (f.id === S.myId) sfx('heal');
      break;
  }
}

function battleFx(f, t) {
  const rb = S.battles.get(f.b), mine = f.b === S.myBattle;
  const U = id => S.uidx.get(id);
  switch (f.k) {
    case 'bstart': if (rb) rb.t0 = t; break;
    case 'act': {
      const a = U(f.s), tg = f.t ? U(f.t) : null;
      if (!a) break;
      a.atkT = t;
      if (f.n) S.floats.push({ uid: a.i, text: f.n + (f.ty === 'owner' || f.ty === 'status' ? '' : '!!'), col: f.ty === 'owner' ? '#bfe8ff' : '#fff6a0', size: 13, t0: t, dur: 1100, font: FONT, head: 0.35 });
      if (MELEE.has(f.w) && tg) {
        const [tx, ty] = unitPos(tg.b, tg);
        a.lunge = { t0: t, tx, ty };
        S.hitDelay[a.i] = t + 180;
        S.impacts.push({ uid: tg.i, kind: SINGLE_IMPACT[f.w] || 'slash', t0: t + 180, dur: 300 });
      } else if (AOE_IMPACT[f.w] && rb) {
        const foes = [...rb.units.values()].filter(u => u.s !== a.s && !u.ko);
        foes.forEach((u, i) => S.impacts.push({ uid: u.i, kind: AOE_IMPACT[f.w], t0: t + 120 + i * 90, dur: 600 }));
        S.hitDelay[a.i] = t + 380;
        if (f.w === 'quake' || f.w === 'breath') S.shakeUntil = t + 500;
      } else if (f.w === 'laser' && tg) {
        S.impacts.push({ uid: tg.i, from: a.i, kind: 'laser', t0: t, dur: 350 });
        S.impacts.push({ uid: tg.i, kind: 'burst', t0: t + 150, dur: 300 });
        S.hitDelay[a.i] = t + 150;
      } else if (f.w === 'rock' && tg) {
        S.impacts.push({ uid: tg.i, kind: 'rock', t0: t, dur: 500 });
        S.hitDelay[a.i] = t + 300;
      } else if (PROJ[f.w] && tg) {
        const [sx, sy] = unitChest(a, t), [ex, ey] = unitChest(tg, t);
        const dur = clamp(Math.hypot(ex - sx, ey - sy) * 90, 180, 420);
        S.projs.push({ sx, sy, ex, ey, tid: tg.i, kind: PROJ[f.w], t0: t, dur });
        if (SINGLE_IMPACT[f.w]) S.impacts.push({ uid: tg.i, kind: SINGLE_IMPACT[f.w], t0: t + dur, dur: 320 });
        S.hitDelay[a.i] = t + dur;
      } else if (f.w === 'roar') S.shakeUntil = t + 700;
      else if (f.w === 'guard') S.impacts.push({ uid: a.i, kind: 'shield', t0: t, dur: 500 });
      if (mine && (f.ty === 'mag' || f.ty === 'owner')) sfx('skill');
      break;
    }
    case 'hit': {
      const u = U(f.id);
      if (!u) break;
      const d = S.hitDelay[f.s] || 0, t0 = d > t ? d : t;
      const [x, y] = unitHead(u, t);
      const mineU = u.pid === S.myId;
      if (f.v === 0) S.floats.push({ uid: u.i, text: 'MISS', col: '#8fd0ff', size: 14, t0, dur: 900 });
      else S.floats.push({ uid: u.i, dx: (Math.random() - 0.5) * 0.5, text: String(f.v), size: f.c ? 22 : f.link ? 12 : 16, crit: f.c, t0, dur: 1000,
        col: f.poison ? '#a8f070' : f.link ? '#ff9a9a' : u.s === 0 ? '#ff5050' : f.c ? '#ffd23a' : '#ffffff' });
      if (f.e === 1) S.floats.push({ uid: u.i, text: '效果絕佳!', col: '#ffb040', size: 12, t0: t0 + 80, dur: 900, font: FONT, head: -0.25 });
      if (f.e === -1) S.floats.push({ uid: u.i, text: '效果不好…', col: '#9ab0c8', size: 12, t0: t0 + 80, dur: 900, font: FONT, head: -0.25 });
      u.hurtT = t0;
      if (mine && !f.link) sfx(f.v === 0 ? 'miss' : mineU ? 'hurt' : f.c ? 'crit' : 'hit');
      break;
    }
    case 'heal': {
      const u = U(f.id);
      if (!u) break;
      S.floats.push({ uid: u.i, text: '+' + f.v, col: f.mp ? '#7ab8ff' : '#7cff7c', size: 15, t0: t + 100, dur: 1000 });
      S.impacts.push({ uid: u.i, kind: f.mp ? 'mp' : 'heal', t0: t, dur: 700 });
      if (mine) sfx('heal');
      break;
    }
    case 'st': {
      const u = U(f.id);
      if (!u) break;
      const name = S.statusNames[f.st] || f.st;
      S.floats.push({ uid: u.i, text: f.ok ? (f.st === 'sleep' ? '睡著了 Zzz' : name) : '無效', col: f.ok ? (/down|slow|sleep|poison/.test(f.st) ? '#d0a0ff' : '#ffe080') : '#aaaaaa', size: 13, t0: t + 150, dur: 1000, font: FONT, head: -0.1 });
      if (f.ok) S.impacts.push({ uid: u.i, kind: /down|slow|sleep|poison/.test(f.st) ? 'debuff' : f.st === 'shield' ? 'shield' : 'buff', t0: t + 100, dur: 700 });
      break;
    }
    case 'ko': { const u = U(f.id); if (u) { u.koT = t; u.ko = 1; } break; }
    case 'revive': {
      const u = U(f.id);
      if (u) { u.ko = 0; S.impacts.push({ uid: u.i, kind: 'revive', t0: t, dur: 900 }); S.floats.push({ uid: u.i, text: '復活!', col: '#fff6a0', size: 15, t0: t + 200, dur: 1100, font: FONT }); }
      if (mine) sfx('heal');
      break;
    }
    case 'cap': {
      const u = U(f.id), a = U(f.s);
      if (!u) break;
      const tCard = t + 380;
      if (f.ok) {
        u.capT = tCard;
        S.dying.push({ u: { ...u }, pos: unitPos(u.b, u), t0: tCard, cap: true });
        S.floats.push({ uid: u.i, text: '封印成功!', col: '#ffe14a', size: 17, t0: tCard + 400, dur: 1500, font: FONT, fixed: unitHead(u, t) });
        if (mine) setTimeout(() => sfx('capture'), 380);
      } else {
        S.impacts.push({ uid: u.i, kind: 'cardbreak', t0: tCard, dur: 500 });
        S.floats.push({ uid: u.i, text: `封印失敗 (${f.pct}%)`, col: '#c8c8c8', size: 13, t0: tCard, dur: 1200, font: FONT });
        if (mine) setTimeout(() => sfx('fail'), 380);
      }
      break;
    }
    case 'flee': { const u = U(f.id); if (u) S.floats.push({ uid: u.i, text: f.ok ? '逃跑成功!' : '逃跑失敗!', col: '#cfe0ff', size: 14, t0: t, dur: 1000, font: FONT }); break; }
    case 'weather':
      if (rb && f.w) S.banners.push({ text: S.weatherNames[f.w] + '!', sub: f.w === 'sun' ? '火、光屬性增強' : '水、風屬性增強', col: f.w === 'sun' ? '#ffcc40' : '#80c0ff', t0: t, dur: 1600, small: true, b: f.b });
      break;
    case 'join': { const u = U(f.id); if (u) S.impacts.push({ uid: u.i, kind: 'revive', t0: t, dur: 600 }); break; }
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
  updateFollowers(dt);
  updateHover();
  render(t);
  UI.tick(t);
  requestAnimationFrame(frame);
}

function updateFollowers(dt) {
  for (const e of S.ents.values()) {
    if (e.k !== 'p' || !e.pt || e.b) { S.followers.delete(e.i); continue; }
    let f = S.followers.get(e.i);
    const tx = e.rx - (e.f || 1) * 0.85, ty = e.ry - 0.1;
    if (!f || f.sp !== e.pt) { f = { x: tx, y: ty, sp: e.pt, face: e.f || 1, walk: false }; S.followers.set(e.i, f); }
    const d = Math.hypot(tx - f.x, ty - f.y);
    if (d > 0.05) {
      const sp = Math.min(d, (d > 1.5 ? 7 : 4.4) * dt);
      if (Math.abs(tx - f.x) > 0.05) f.face = tx > f.x ? 1 : -1;
      f.x += (tx - f.x) / d * sp; f.y += (ty - f.y) / d * sp;
      f.walk = true;
    } else { f.walk = false; f.face = e.f || f.face; }
  }
}

// ============================================================
//  畫面
// ============================================================
function render(t) {
  const vw = cv.width, vh = cv.height;
  ctx.fillStyle = '#0b0f08'; ctx.fillRect(0, 0, vw, vh);
  const me = S.ents.get(S.myId), rbMine = myBattle();
  let tx = me ? me.rx * TILE : S.W * TILE / 2, ty = me ? me.ry * TILE : S.H * TILE / 2;
  if (rbMine) { tx = rbMine.x * TILE; ty = rbMine.y * TILE; }
  if (S.camX === null || Math.abs(S.camX - tx) > 400) { S.camX = tx; S.camY = ty; }
  S.camX += (tx - S.camX) * 0.18; S.camY += (ty - S.camY) * 0.18;
  const mw = S.W * TILE, mh = S.H * TILE;
  let camX = mw > vw ? clamp(S.camX, vw / 2, mw - vw / 2) : mw / 2;
  let camY = mh > vh ? clamp(S.camY, vh / 2, mh - vh / 2) : mh / 2;
  if (t < S.shakeUntil) { camX += (Math.random() - 0.5) * 8; camY += (Math.random() - 0.5) * 6; }
  const ox = S.ox = Math.round(vw / 2 - camX), oy = S.oy = Math.round(vh / 2 - camY);
  const tx0 = Math.max(0, Math.floor(-ox / TILE) - 1), ty0 = Math.max(0, Math.floor(-oy / TILE) - 1);
  const tx1 = Math.min(S.W - 1, Math.ceil((vw - ox) / TILE) + 1), ty1 = Math.min(S.H - 1, Math.ceil((vh - oy) / TILE) + 2);
  const sprites = [];

  for (let yy = ty0; yy <= ty1; yy++) {
    for (let xx = tx0; xx <= tx1; xx++) {
      const i = yy * S.W + xx, tt = S.tiles[i], sx = xx * TILE + ox, sy = yy * TILE + oy, v = S.vars[i];
      if (tt === T_WATER) drawWater(sx, sy, xx, yy, t);
      else if (tt === T_TREE) {
        const far = Math.hypot(xx - MAP_CX, yy - MAP_CY) > 36;
        ctx.drawImage(tileImg(far ? T_DARK : T_GRASS, v), sx, sy);
        sprites.push({ y: yy + 1, img: treeImgs[(far ? 2 : 0) + (v & 1)], sx: sx - 8, sy: sy - 30 });
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
  for (const rb of S.battles.values()) drawBattleGround(rb, t);

  for (const e of S.ents.values()) if (!(e.k === 'p' && e.b)) sprites.push({ y: e.ry + 0.3, e });
  for (const [pid, f] of S.followers) sprites.push({ y: f.y + 0.3, f, pid });
  for (const n of S.npcs) sprites.push({ y: n.y + 0.3, n });
  sprites.sort((a, b) => a.y - b.y);
  for (const s of sprites) {
    if (s.img) ctx.drawImage(s.img, s.sx, s.sy);
    else if (s.e) drawEntity(s.e, t);
    else if (s.f) drawCreature(ctx, s.f.sp, s.f.x * TILE + ox, s.f.y * TILE + oy + 8, { face: s.f.face, walk: s.f.walk, t, id: s.pid });
    else drawHumanoid(ctx, s.n.x * TILE + ox, s.n.y * TILE + oy + 8, { ...NPC_LOOK[s.n.c], face: me && me.rx < s.n.x ? -1 : 1 }, t);
  }
  for (const rb of S.battles.values()) drawBattleUnits(rb, t);
  drawDying(t);
  drawEffects(t);
  drawLabels(t);
  for (const rb of S.battles.values()) drawBattleHUD(rb, t);
  drawFloats(t);
  drawBanners(t);
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

const feet = e => [e.rx * TILE + S.ox, e.ry * TILE + S.oy + 8];
function drawEntity(e, t) {
  const [x, y] = feet(e);
  if (x < -150 || y < -150 || x > cv.width + 150 || y > cv.height + 150) return;
  if (e.k === 'p') drawHumanoid(ctx, x, y, { ...lookOwner(e.c, e.n), face: e.f, walk: e.mv }, t);
  else if (e.k === 'm') drawCreature(ctx, e.c, x, y, { face: e.f, t, id: e.i });
}

// ----- 戰鬥 -----
function battleEllipse(rb) {
  const rows = Math.max(rb.np || 1, (rb.maxRow || 0) + 1);
  return { cx: rb.x * TILE + S.ox, cy: (rb.y + 0.15) * TILE + S.oy, rx: (rb.boss ? 5 : 4.4) * TILE, ry: Math.max(2.4, rows * 0.9 + 1.2) * TILE };
}
function drawBattleGround(rb, t) {
  const E = battleEllipse(rb), k = Math.min(1, (t - rb.t0) / 400);
  ctx.save();
  ctx.translate(E.cx, E.cy);
  ctx.scale(k, k);
  const wc = rb.w === 'sun' ? '255,190,60' : rb.w === 'rain' ? '60,110,200' : '10,12,40';
  ctx.fillStyle = `rgba(${wc},${rb.w ? 0.28 : 0.38})`;
  ctx.beginPath(); ctx.ellipse(0, 0, E.rx, E.ry, 0, 0, 7); ctx.fill();
  ctx.strokeStyle = rb.boss ? 'rgba(255,90,40,.9)' : 'rgba(230,200,110,.85)'; ctx.lineWidth = 2;
  ctx.setLineDash([10, 6]); ctx.lineDashOffset = -t / 50;
  ctx.beginPath(); ctx.ellipse(0, 0, E.rx, E.ry, 0, 0, 7); ctx.stroke();
  ctx.setLineDash([]);
  ctx.strokeStyle = 'rgba(230,200,110,.35)'; ctx.lineWidth = 1;
  ctx.beginPath(); ctx.ellipse(0, 0, E.rx - 8, E.ry - 6, 0, 0, 7); ctx.stroke();
  for (let i = 0; i < 12; i++) {   // 符文
    const a = i / 12 * Math.PI * 2 + t / 4000;
    ctx.fillStyle = 'rgba(255,230,150,.6)';
    ctx.fillRect(Math.cos(a) * (E.rx - 4) - 2, Math.sin(a) * (E.ry - 3) - 2, 4, 4);
  }
  if (rb.w === 'rain') {
    ctx.strokeStyle = 'rgba(180,210,255,.55)'; ctx.lineWidth = 1;
    for (let i = 0; i < 40; i++) {
      const x = (hash2(i, 1) - 0.5) * E.rx * 1.8, y = ((hash2(i, 2) * E.ry * 2 + t / 2) % (E.ry * 2)) - E.ry;
      ctx.beginPath(); ctx.moveTo(x, y - 8); ctx.lineTo(x - 2, y); ctx.stroke();
    }
  } else if (rb.w === 'sun') {
    ctx.fillStyle = 'rgba(255,240,180,.25)';
    for (let i = 0; i < 6; i++) { const x = (i - 2.5) * E.rx * 0.32 + Math.sin(t / 900 + i) * 10; ctx.fillRect(x, -E.ry, 10, E.ry * 2); }
  }
  ctx.restore();
}

function drawBattleUnits(rb, t) {
  const list = [...rb.units.values()].map(u => ({ u, p: unitDrawPos(u, t) })).sort((a, b) => a.p[1] - b.p[1]);
  for (const { u, p } of list) {
    const x = p[0] * TILE + S.ox, y = p[1] * TILE + S.oy;
    if (u.capT && t >= u.capT) continue;
    if (u.pid === S.myId && !u.ko) {   // 自己的單位腳下有光圈
      ctx.strokeStyle = u.rd ? `rgba(255,240,120,${0.6 + 0.4 * Math.sin(t / 120)})` : 'rgba(255,220,100,.45)';
      ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(x, y, 16, 6, 0, 0, 7); ctx.stroke();
    }
    if (u.i === S.target && rb.i === S.myBattle) {
      ctx.save(); ctx.strokeStyle = '#ff4040'; ctx.lineWidth = 2; ctx.setLineDash([6, 4]); ctx.lineDashOffset = -t / 40;
      const big = u.boss ? 3 : 1;
      ctx.beginPath(); ctx.ellipse(x, y, 17 * big, 6 * big, 0, 0, 7); ctx.stroke(); ctx.restore();
    }
    if (u.i === S.allyTarget && rb.i === S.myBattle) {
      ctx.strokeStyle = '#60ff90'; ctx.lineWidth = 2; ctx.beginPath(); ctx.ellipse(x, y, 17, 6, 0, 0, 7); ctx.stroke();
    }
    const flash = t - u.hurtT < 140 && t >= u.hurtT;
    ctx.globalAlpha = flash ? 0.5 : 1;
    const atk = u.atkT ? clamp((t - u.atkT) / 300, 0, 1) : 0, sw = atk > 0 && atk < 1 ? atk : 0;
    if (u.k === 'o') {
      if (u.ko) drawGrave(ctx, x, y);
      else drawHumanoid(ctx, x, y, { ...lookOwner(u.c, u.n), face: 1, atk: sw }, t);
    } else {
      drawCreature(ctx, u.c, x, y, { face: u.s === 0 ? 1 : -1, t, atk: sw, id: u.i, ko: u.ko });
      if (u.st && u.st.includes('sleep') && !u.ko) drawZzz(x, y - unitH(u), t);
    }
    ctx.globalAlpha = 1;
  }
}
function drawZzz(x, y, t) {
  const k = (t / 1200) % 1;
  ctx.globalAlpha = 1 - k;
  text('Z', x + 8 + k * 8, y - k * 14, '#c8d8ff', 12, NUMFONT, true);
  text('z', x + 16 + k * 6, y - 8 - k * 10, '#c8d8ff', 10, NUMFONT, true);
  ctx.globalAlpha = 1;
}

function drawBattleHUD(rb, t) {
  const mineB = rb.i === S.myBattle;
  for (const u of rb.units.values()) {
    if (u.capT && t >= u.capT) continue;
    const [hx, hy] = unitHead(u, t), x = hx * TILE + S.ox, y = hy * TILE + S.oy;
    const w = u.boss ? 80 : 40;
    const isMe = u.pid === S.myId;
    text(`${u.boss ? '★ ' : ''}Lv.${u.lv} ${u.n}`, x, y - 22, u.s === 1 ? (u.boss ? '#ffcc33' : '#ffb8a0') : isMe ? '#fff1a8' : '#ffffff', u.boss ? 13 : 11, FONT, !!u.boss);
    bar(x - w / 2, y - 13, w, 4, u.hp / u.mh, u.s === 1 ? '#e83a3a' : '#3ad04a');
    if (!u.ko) {
      const b = unitBar(u, t) / 100;
      ctx.fillStyle = '#000'; ctx.fillRect(x - w / 2 - 1, y - 8, w + 2, 4);
      ctx.fillStyle = u.rd ? (Math.floor(t / 150) % 2 ? '#ffffff' : '#ffe14a') : '#d8b020';
      ctx.fillRect(x - w / 2, y - 7, Math.round(w * b), 2);
    }
    if (u.st && u.st.length) {
      let sx = x - (u.st.length - 1) * 12;
      for (const st of u.st) { tagText(S.statusNames[st] || st, sx, y - 36, /down|slow|sleep|poison/.test(st) ? '#c8a0ff' : '#ffe080'); sx += 24; }
    }
    if (mineB && isMe && u.rd && !u.ko) text('▼', x, y - 46 + Math.sin(t / 150) * 3, '#ffe14a', 14, NUMFONT, true);
  }
}
function tagText(s, x, y, col) {
  ctx.font = `11px ${FONT}`; const w = ctx.measureText(s).width + 6;
  ctx.fillStyle = 'rgba(0,0,0,.65)'; ctx.fillRect(x - w / 2, y - 7, w, 14);
  ctx.fillStyle = col; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(s, x, y);
}

function drawDying(t) {
  S.dying = S.dying.filter(d => t - d.t0 < 800);
  for (const d of S.dying) {
    if (t < d.t0) continue;
    const k = (t - d.t0) / 800, x = d.pos[0] * TILE + S.ox, y = d.pos[1] * TILE + S.oy;
    ctx.save();
    if (d.cap) {   // 被吸進封印卡
      const s = Math.max(0.01, 1 - k * 1.3);
      ctx.translate(x, y - 20); ctx.scale(s, s); ctx.translate(-x, -(y - 20));
      ctx.globalAlpha = 1 - k * 0.5;
      drawCreature(ctx, d.u.c, x, y, { face: -1, t, id: d.u.i });
      ctx.restore();
      ctx.save(); ctx.globalAlpha = 1 - k;
      const gr = ctx.createRadialGradient(x, y - 20, 0, x, y - 20, 40 * k + 10);
      gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(0.5, 'rgba(200,160,255,.7)'); gr.addColorStop(1, 'rgba(160,100,255,0)');
      ctx.fillStyle = gr; ctx.beginPath(); ctx.arc(x, y - 20, 40 * k + 10, 0, 7); ctx.fill();
    } else {
      ctx.globalAlpha = 1 - k;
      if (d.u.k !== 'o') drawCreature(ctx, d.u.c, x, y + k * 6, { face: d.u.s === 0 ? 1 : -1, t, id: d.u.i });
    }
    ctx.restore();
  }
}

function drawEffects(t) {
  const ox = S.ox, oy = S.oy;
  // 投射物
  S.projs = S.projs.filter(p => t < p.t0 + p.dur);
  for (const p of S.projs) {
    if (t < p.t0) continue;
    const k = (t - p.t0) / p.dur, tg = S.uidx.get(p.tid);
    if (tg) [p.ex, p.ey] = unitChest(tg, t);
    const x = (p.sx + (p.ex - p.sx) * k) * TILE + ox, y = (p.sy + (p.ey - p.sy) * k) * TILE + oy, ang = Math.atan2(p.ey - p.sy, p.ex - p.sx);
    if (p.kind === 'card') {
      ctx.save(); ctx.translate(x, y - Math.sin(k * Math.PI) * 30); ctx.rotate(k * 12);
      ctx.drawImage(iconC('seal_card', S.items.seal_card), -12, -12, 24, 24); ctx.restore();
    } else if (p.kind === 'wind') {
      ctx.save(); ctx.translate(x, y); ctx.strokeStyle = '#a0ffc8'; ctx.lineWidth = 2;
      for (let i = 0; i < 3; i++) { ctx.beginPath(); ctx.arc(0, 0, 5 + i * 4, t / 60 + i, t / 60 + i + 2.5); ctx.stroke(); }
      ctx.restore();
    } else if (p.kind === 'ice') {
      ctx.save(); ctx.translate(x, y); ctx.rotate(ang);
      poly(ctx, [12, 0, 0, -5, -10, 0, 0, 5], '#dff6ff'); ctx.strokeStyle = '#4aa0e0'; ctx.stroke();
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
  // 命中與技能特效
  S.impacts = S.impacts.filter(m => t < m.t0 + m.dur);
  for (const m of S.impacts) {
    if (t < m.t0) continue;
    const u = S.uidx.get(m.uid);
    if (!u) continue;
    const [fx, fy] = unitDrawPos(u, t), [cx, cy] = unitChest(u, t);
    const X = cx * TILE + ox, Y = cy * TILE + oy, FX = fx * TILE + ox, FY = fy * TILE + oy, k = (t - m.t0) / m.dur;
    ctx.save(); ctx.globalAlpha = Math.min(1, (1 - k) * 1.8);
    switch (m.kind) {
      case 'slash':
        ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 3 * (1 - k) + 1;
        ctx.beginPath(); ctx.arc(X - 6, Y + 6, 18, -1.6 + k * 0.6, -0.2 + k * 0.6); ctx.stroke(); break;
      case 'slam': case 'burst': {
        ctx.fillStyle = m.kind === 'burst' ? '#ff9a30' : '#ffb030'; ctx.beginPath();
        for (let i = 0; i < 16; i++) { const a = i / 16 * Math.PI * 2, r = (i % 2 ? 8 : 22) * (0.6 + k * 0.7); ctx.lineTo(X + Math.cos(a) * r, Y + Math.sin(a) * r); }
        ctx.fill(); ctx.fillStyle = '#fff6c0'; ctx.beginPath(); ctx.arc(X, Y, 7, 0, 7); ctx.fill(); break;
      }
      case 'meteor': {
        const fall = Math.min(1, k * 2.2), my = Y - 90 * (1 - fall);
        const gr = ctx.createRadialGradient(X, my, 0, X, my, 12);
        gr.addColorStop(0, '#fff'); gr.addColorStop(0.4, '#ffa030'); gr.addColorStop(1, 'rgba(255,40,0,0)');
        ctx.fillStyle = gr; ctx.beginPath(); ctx.arc(X, my, 12, 0, 7); ctx.fill();
        if (fall >= 1) { ctx.fillStyle = 'rgba(255,120,30,.6)'; ctx.beginPath(); ctx.ellipse(FX, FY, 24 * k, 8 * k, 0, 0, 7); ctx.fill(); }
        break;
      }
      case 'ice':
        for (let i = 0; i < 5; i++) {
          const ix = FX + (i - 2) * 7, h = 26 * Math.min(1, k * 3) * (1 - Math.abs(i - 2) * 0.25);
          poly(ctx, [ix - 4, FY, ix, FY - h, ix + 4, FY], i % 2 ? '#c8f0ff' : '#e8fbff');
        }
        break;
      case 'wind':
        ctx.strokeStyle = '#b0ffd0'; ctx.lineWidth = 2;
        for (let i = 0; i < 4; i++) { ctx.beginPath(); ctx.ellipse(FX, FY - i * 10 - k * 10, 14 - i * 2, 4, 0, t / 80 + i, t / 80 + i + 4); ctx.stroke(); }
        break;
      case 'holy': {
        const gr = ctx.createLinearGradient(FX - 16, 0, FX + 16, 0);
        gr.addColorStop(0, 'rgba(255,250,200,0)'); gr.addColorStop(0.5, 'rgba(255,250,200,.9)'); gr.addColorStop(1, 'rgba(255,250,200,0)');
        ctx.fillStyle = gr; ctx.fillRect(FX - 16, FY - 120, 32, 125); break;
      }
      case 'dark':
        for (let i = 0; i < 3; i++) { ctx.strokeStyle = `rgba(150,80,220,${0.8 - i * 0.2})`; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(X, Y, (1 - k) * 28 + i * 6, 0, 7); ctx.stroke(); }
        ctx.fillStyle = 'rgba(40,0,60,.6)'; ctx.beginPath(); ctx.arc(X, Y, 10 * (1 - k) + 4, 0, 7); ctx.fill();
        break;
      case 'rock': {
        const fall = Math.min(1, k * 2), ry = Y - 80 * (1 - fall);
        poly(ctx, [X - 9, ry, X - 4, ry - 9, X + 7, ry - 7, X + 10, ry + 2, X + 2, ry + 8, X - 7, ry + 6], '#8a6a40');
        if (fall >= 1) { ctx.fillStyle = 'rgba(200,170,120,.6)'; ctx.beginPath(); ctx.ellipse(FX, FY, 22 * k + 6, 7 * k + 2, 0, 0, 7); ctx.fill(); }
        break;
      }
      case 'laser': {
        const a = S.uidx.get(m.from);
        if (!a) break;
        const [sx, sy] = unitChest(a, t);
        ctx.strokeStyle = 'rgba(255,255,180,.9)'; ctx.lineWidth = 6 * (1 - k) + 1;
        ctx.beginPath(); ctx.moveTo(sx * TILE + ox, sy * TILE + oy); ctx.lineTo(X, Y); ctx.stroke();
        ctx.strokeStyle = '#fff'; ctx.lineWidth = 2; ctx.stroke();
        break;
      }
      case 'poison':
        for (let i = 0; i < 6; i++) { ctx.fillStyle = '#90e040'; ctx.beginPath(); ctx.arc(X + (hash2(i, 3) - 0.5) * 30, Y - k * 30 - i * 3, 3 + hash2(i, 4) * 3, 0, 7); ctx.fill(); }
        break;
      case 'drain':
        for (let i = 0; i < 8; i++) { const a = i / 8 * 7 + t / 200; ctx.fillStyle = '#ff5060'; ctx.fillRect(X + Math.cos(a) * 20 * (1 - k), Y + Math.sin(a) * 14 * (1 - k), 3, 3); }
        break;
      case 'heal': case 'mp':
        for (let i = 0; i < 6; i++) {
          const px = FX + (hash2(i, 9) - 0.5) * 30, py = FY - 10 - ((k * 50 + i * 9) % 50);
          ctx.fillStyle = m.kind === 'mp' ? '#80b8ff' : '#80ff90'; ctx.fillRect(px - 1, py - 4, 3, 9); ctx.fillRect(px - 4, py - 1, 9, 3);
        }
        break;
      case 'buff':
        for (let i = 0; i < 8; i++) { ctx.fillStyle = '#ffe060'; ctx.fillRect(FX + (hash2(i, 11) - 0.5) * 34, FY - ((k * 60 + i * 8) % 60), 2, 6); }
        break;
      case 'debuff':
        for (let i = 0; i < 5; i++) { const px = FX + (i - 2) * 9, py = FY - 50 + k * 40; poly(ctx, [px - 4, py, px + 4, py, px, py + 7], '#b070ff'); }
        break;
      case 'shield':
        ctx.strokeStyle = '#a0d0ff'; ctx.lineWidth = 3; ctx.fillStyle = 'rgba(140,190,255,.2)';
        ctx.beginPath(); ctx.ellipse(X, Y, 22 + k * 6, 26 + k * 6, 0, 0, 7); ctx.fill(); ctx.stroke(); break;
      case 'revive': {
        const gr = ctx.createLinearGradient(FX - 20, 0, FX + 20, 0);
        gr.addColorStop(0, 'rgba(255,230,120,0)'); gr.addColorStop(0.5, 'rgba(255,240,160,.8)'); gr.addColorStop(1, 'rgba(255,230,120,0)');
        ctx.fillStyle = gr; ctx.fillRect(FX - 20, FY - 100, 40, 104); break;
      }
      case 'cardbreak':
        for (let i = 0; i < 6; i++) { const a = i / 6 * 7; ctx.fillStyle = '#b890ff'; ctx.fillRect(X + Math.cos(a) * 30 * k, Y + Math.sin(a) * 30 * k, 5, 7); }
        break;
    }
    ctx.restore();
  }
  // 升級光柱 / 傳送 / 孵化
  S.beams = S.beams.filter(b => t < b.t0 + b.dur);
  for (const b of S.beams) {
    const e = S.ents.get(b.id);
    if (!e) continue;
    const [x, y] = feet(e), k = (t - b.t0) / b.dur;
    ctx.save(); ctx.globalAlpha = k < 0.8 ? 1 : (1 - k) / 0.2;
    const gr = ctx.createLinearGradient(x - 22, 0, x + 22, 0);
    const c = b.tp ? '120,220,255' : b.hatch ? '255,180,220' : '255,220,90';
    gr.addColorStop(0, `rgba(${c},0)`); gr.addColorStop(0.5, `rgba(${c},.7)`); gr.addColorStop(1, `rgba(${c},0)`);
    ctx.fillStyle = gr; ctx.fillRect(x - 22, y - 220, 44, 225);
    for (let i = 0; i < 8; i++) { const py = y - ((t / 4 + i * 37) % 160), pxx = x + Math.sin(i * 2 + t / 200) * 16; ctx.fillStyle = '#fff'; ctx.fillRect(pxx, py, 3, 3); }
    if (!b.tp) text(b.hatch ? '孵化成功!' : 'LEVEL UP!!', x, y - 70 - k * 40, b.hatch ? '#ffb0e0' : '#ffe14a', 22, b.hatch ? FONT : NUMFONT, true);
    ctx.restore();
  }
}

function drawFloats(t) {
  S.floats = S.floats.filter(f => t < f.t0 + f.dur);
  for (const f of S.floats) {
    if (t < f.t0) continue;
    let wx, wy;
    if (f.uid) {
      const u = S.uidx.get(f.uid);
      if (u) { [wx, wy] = unitHead(u, t); f.last = [wx, wy]; }
      else if (f.last || f.fixed) [wx, wy] = f.last || f.fixed;
      else continue;
      wy -= (f.head || 0) + 0.2; wx += f.dx || 0;
    } else { wx = f.x; wy = f.y; }
    const k = (t - f.t0) / f.dur;
    const x = wx * TILE + S.ox, y = wy * TILE + S.oy - k * 34 - (f.crit && k < 0.15 ? (0.15 - k) * 60 : 0);
    ctx.globalAlpha = k > 0.7 ? (1 - k) / 0.3 : 1;
    const sz = f.crit && k < 0.15 ? f.size * (1.6 - k * 4) : f.size;
    text(f.text, x, y, f.col, Math.round(sz), f.font || NUMFONT, true);
    ctx.globalAlpha = 1;
  }
}

function drawBanners(t) {
  // 遇敵轉場
  if (S.trans) {
    const k = (t - S.trans.t0) / 1400;
    if (k >= 1) S.trans = null;
    else {
      const vw = cv.width, vh = cv.height;
      ctx.fillStyle = `rgba(255,255,255,${Math.max(0, 0.85 - k * 4)})`; ctx.fillRect(0, 0, vw, vh);
      const bh = vh * 0.12 * Math.sin(Math.min(1, k * 1.4) * Math.PI);
      ctx.fillStyle = '#000'; ctx.fillRect(0, 0, vw, bh); ctx.fillRect(0, vh - bh, vw, bh);
      if (k > 0.1 && k < 0.9) {
        const sx = vw / 2 + (k < 0.25 ? (0.25 - k) * vw * 3 : k > 0.75 ? -(k - 0.75) * vw * 3 : 0);
        text(S.trans.boss ? '炎龍出現了!' : '遭遇野生寵物!', sx, vh * 0.3, S.trans.boss ? '#ff6a3a' : '#ffe14a', 30, FONT, true);
      }
    }
  }
  S.banners = S.banners.filter(b => t < b.t0 + b.dur);
  for (const b of S.banners) {
    const k = (t - b.t0) / b.dur, vw = cv.width, vh = cv.height;
    ctx.globalAlpha = k < 0.1 ? k * 10 : k > 0.8 ? (1 - k) * 5 : 1;
    const y = b.small ? vh * 0.22 : vh * 0.32;
    if (!b.small) { ctx.fillStyle = 'rgba(0,0,0,.45)'; ctx.fillRect(0, y - 34, vw, b.sub ? 88 : 64); }
    text(b.text, vw / 2, y, b.col, b.small ? 22 : 36, FONT, true);
    if (b.sub) text(b.sub, vw / 2, y + 36, '#ffffff', 14, FONT);
    ctx.globalAlpha = 1;
  }
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
    const [x, y] = feet(e);
    if (x < -100 || y < -150 || x > cv.width + 100 || y > cv.height + 100) continue;
    let head = y - 52, bx = x;
    if (e.k === 'p') {
      if (e.b) {   // 戰鬥中:泡泡跟著戰鬥中的主人
        const ou = [...S.uidx.values()].find(u => u.k === 'o' && u.pid === e.i);
        if (ou) { const [hx, hy] = unitHead(ou, t); bx = hx * TILE + S.ox; head = hy * TILE + S.oy - 40; }
      } else {
        text(e.n, x, y + 12, e.i === S.myId ? '#fff1a8' : '#ffffff');
        if (S.hover && S.hover.k === 'p' && S.hover.i === e.i) text(`Lv.${e.lv} ${(S.classes[e.c] || {}).n || ''}`, x, y + 26, '#c8d4f0', 11);
        if (e.pn && S.hover && S.hover.k === 'p' && S.hover.i === e.i) text(`寵物:${e.pn}`, x, y + 39, '#c8d4f0', 11);
      }
    } else if (e.k === 'm') {
      head = y - 110;
      text(`★ Lv.${e.lv} ${e.n}`, x, head - 8, '#ffcc33', 13, FONT, true);
      if (S.hover && S.hover.k === 'boss') text('點擊挑戰 (可多人加入)', x, y + 14, '#ffd0a0', 11);
    }
    if (e.bubble && t < e.bubble.until) drawBubble(e.bubble.text, bx, head - 14);
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

function drawMinimap(t) {
  const s = mm.width / S.W;
  mmc.imageSmoothingEnabled = false;
  mmc.drawImage(S.mmBase, 0, 0, mm.width, mm.height);
  mmc.strokeStyle = 'rgba(255,255,255,.6)';
  mmc.strokeRect(-S.ox / TILE * s, -S.oy / TILE * s, cv.width / TILE * s, cv.height / TILE * s);
  for (const n of S.npcs) { mmc.fillStyle = '#5f5'; mmc.fillRect(n.x * s - 1, n.y * s - 1, 3, 3); }
  for (const rb of S.battles.values()) { mmc.fillStyle = Math.floor(t / 400) % 2 ? '#fa0' : '#f60'; mmc.fillRect(rb.x * s - 2, rb.y * s - 2, 4, 4); }
  for (const e of S.ents.values()) {
    if (e.k === 'm') { mmc.fillStyle = '#f0f'; mmc.fillRect(e.rx * s - 2, e.ry * s - 2, 5, 5); }
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
  const t = performance.now();
  let best = null, bd = 1e9;
  const test = (o, ex, ey, hw, top, bottom) => {
    const dx = wx - ex, dy = wy - ey;
    if (Math.abs(dx) < hw && dy > -top && dy < bottom) { const d = dx * dx + dy * dy * 0.3; if (d < bd) { bd = d; best = o; } }
  };
  for (const rb of S.battles.values()) {
    for (const u of rb.units.values()) {
      const [x, y] = unitDrawPos(u, t), h = unitH(u) / TILE;
      test({ k: 'u', u, i: u.i }, x, y, u.boss ? 1.7 : 0.6, h + 0.1, 0.35);
    }
  }
  if (S.myBattle) return best;
  for (const e of S.ents.values()) {
    if (e.i === S.myId || (e.k === 'p' && e.b)) continue;
    if (e.k === 'm') test({ k: 'boss', i: e.i }, e.rx, e.ry + 0.25, 1.7, 3.4, 0.4);
    else test({ k: 'p', i: e.i }, e.rx, e.ry + 0.25, 0.5, 1.5, 0.35);
  }
  for (const n of S.npcs) test({ k: 'n', i: n.i }, n.x, n.y + 0.25, 0.55, 1.6, 0.35);
  if (!best) {
    for (const rb of S.battles.values()) {
      const E = battleEllipse(rb), sx = wx * TILE + S.ox, sy = wy * TILE + S.oy;
      if (((sx - E.cx) / E.rx) ** 2 + ((sy - E.cy) / E.ry) ** 2 < 1) return { k: 'circle', i: rb.i };
    }
  }
  return best;
}

const CURSOR_SVG = {
  normal: ["<svg xmlns='http://www.w3.org/2000/svg' width='22' height='22'><path d='M1 1 L1 17 L5 13 L8 20 L11 19 L8 12 L14 12 Z' fill='#f8d860' stroke='#5a3a00' stroke-width='1.3'/></svg>", '1 1'],
  atk: ["<svg xmlns='http://www.w3.org/2000/svg' width='24' height='24'><path d='M2 2 L16 16' stroke='#222' stroke-width='5' stroke-linecap='round'/><path d='M2 2 L16 16' stroke='#eef4f8' stroke-width='3' stroke-linecap='round'/><path d='M11 19 L19 11' stroke='#5a3a00' stroke-width='4'/><path d='M11 19 L19 11' stroke='#e0b030' stroke-width='2'/><path d='M17 17 L22 22' stroke='#6b4423' stroke-width='3'/></svg>", '2 2'],
  talk: ["<svg xmlns='http://www.w3.org/2000/svg' width='24' height='22'><path d='M2 2 H22 V14 H10 L5 20 V14 H2 Z' fill='#fffbe0' stroke='#5a3a00' stroke-width='1.5'/><circle cx='7' cy='8' r='1.5'/><circle cx='12' cy='8' r='1.5'/><circle cx='17' cy='8' r='1.5'/></svg>", '2 2'],
  ally: ["<svg xmlns='http://www.w3.org/2000/svg' width='22' height='22'><path d='M1 1 L1 17 L5 13 L8 20 L11 19 L8 12 L14 12 Z' fill='#80ff9a' stroke='#004a1a' stroke-width='1.3'/></svg>", '1 1'],
  join: ["<svg xmlns='http://www.w3.org/2000/svg' width='22' height='22'><path d='M1 1 L1 17 L5 13 L8 20 L11 19 L8 12 L14 12 Z' fill='#8fe0ff' stroke='#003a5a' stroke-width='1.3'/></svg>", '1 1'],
};
const CURSORS = {};
for (const [k, [svg, hs]] of Object.entries(CURSOR_SVG)) CURSORS[k] = `url("data:image/svg+xml,${encodeURIComponent(svg)}") ${hs}, auto`;
document.body.style.cursor = CURSORS.normal;

function updateHover() {
  if (!S.mouse.in) { S.hover = null; return; }
  const [wx, wy] = screenToWorld(S.mouse.x, S.mouse.y);
  S.hover = pick(wx, wy);
  const h = S.hover;
  let k = 'normal';
  if (h) {
    if (h.k === 'u') k = h.u.s === 1 ? 'atk' : h.u.k === 'p' && S.myBattle ? 'ally' : 'normal';
    else k = { boss: 'atk', n: 'talk', circle: 'join' }[h.k] || 'normal';
  }
  if (cv.dataset.cur !== k) { cv.dataset.cur = k; cv.style.cursor = CURSORS[k]; }
}

// ----- 戰鬥指令 -----
function petCmd(a, s) {
  const { p } = myUnits();
  if (!p || !p.rd || p.ko) return;
  const ally = a === 'skill' && S.pskills[s] && S.pskills[s].target === 'ally';
  send({ t: 'bcmd', u: 'p', a, s, tg: ally ? (S.allyTarget || p.i) : S.target });
}
function ownerSkill(i) {
  const { o, p } = myUnits();
  const sk = (S.classes[S.cls] || {}).skills[i];
  if (!o || !o.rd || o.ko || !sk) return;
  const tg = sk.target === 'enemy' ? S.target : sk.target === 'ally' ? (S.allyTarget || (p && p.i)) : 0;
  send({ t: 'bcmd', u: 'o', a: 'oskill', s: i, tg });
}
function ownerCmd(a, extra = {}) {
  const { o, p } = myUnits();
  if (!o || !o.rd || o.ko) return;
  const tg = a === 'cap' ? S.target : (S.allyTarget || (p && p.i));
  send({ t: 'bcmd', u: 'o', a, tg, ...extra });
}
function toggleAuto(v) {
  S.auto = v === undefined ? !S.auto : v;
  send({ t: 'bauto', on: S.auto });
  UI.battleAuto();
}

function bindInput() {
  const chatIn = $('#chat-in');
  cv.addEventListener('mousemove', e => { S.mouse.x = e.clientX; S.mouse.y = e.clientY; S.mouse.in = true; });
  cv.addEventListener('mouseleave', () => { S.mouse.in = false; });
  cv.addEventListener('contextmenu', e => e.preventDefault());
  cv.addEventListener('mousedown', e => {
    if (e.button !== 0) return;
    chatIn.blur(); initAudio(); UI.closeMenus();
    S.mouse.x = e.clientX; S.mouse.y = e.clientY; S.mouse.in = true;
    const [wx, wy] = screenToWorld(e.clientX, e.clientY), h = pick(wx, wy);
    if (S.myBattle) {
      if (h && h.k === 'u' && h.u.b && h.u.b.i === S.myBattle) {
        if (h.u.s === 1 && !h.u.ko) { setTarget(h.u.i); sfx('click'); }
        else if (h.u.s === 0 && h.u.k === 'p') { S.allyTarget = h.u.i; sfx('click'); }
      }
      return;
    }
    if (h && h.k === 'n') send({ t: 'npc', id: h.i });
    else if (h && h.k === 'boss') send({ t: 'boss' });
    else if (h && (h.k === 'circle' || h.k === 'u')) send({ t: 'bjoin', b: h.k === 'circle' ? h.i : h.u.b.i });
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
    if (document.activeElement && ['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
      if (document.activeElement === chatIn) {
        if (e.key === 'Enter') { const v = chatIn.value.trim(); if (v) send({ t: 'chat', m: v }); chatIn.value = ''; chatIn.blur(); }
        else if (e.key === 'Escape') chatIn.blur();
      }
      return;
    }
    const k = e.key.toLowerCase();
    if (k === 'enter') { e.preventDefault(); S.keys = {}; updateDir(); chatIn.focus(); return; }
    if (S.myBattle) {   // 戰鬥快捷鍵
      if (e.repeat) return;
      const { p } = myUnits();
      const skills = p ? (S.species[p.c] || {}).skills || [] : [];
      const learned = p ? skills.filter(([, lv]) => p.lv >= lv).map(([s]) => s) : [];
      if (k === '1') petCmd('atk');
      else if (k >= '2' && k <= '4') { const s = learned[+k - 2]; if (s) petCmd('skill', s); }
      else if (k === '5') petCmd('def');
      else if (k === 'q' || k === 'w' || k === 'e') ownerSkill('qwe'.indexOf(k));
      else if (k === 'r') ownerCmd('item', { item: 'red_potion' });
      else if (k === 'c') ownerCmd('cap');
      else if (k === 'x') UI.swapMenu();
      else if (k === 'f') ownerCmd('flee');
      else if (k === 'tab') cycleTarget();
      else if (k === ' ') toggleAuto();
      else if (k === 'escape') UI.closeMenus();
      else return;
      e.preventDefault();
      return;
    }
    if (MOVE[k]) { e.preventDefault(); if (!S.keys[k]) { S.keys[k] = true; updateDir(); } return; }
    if (e.repeat) return;
    if (k === 'p') UI.toggleWin('pets');
    else if (k === 'i') UI.toggleWin('inv');
    else if (k === 'h') UI.toggleWin('help');
    else if (k === 'm') UI.toggleSound();
    else if (k === 'escape') UI.closeAll();
  });
  addEventListener('keyup', e => { const k = e.key.toLowerCase(); if (S.keys[k]) { delete S.keys[k]; updateDir(); } });
  addEventListener('blur', () => { S.keys = {}; updateDir(); });
}
