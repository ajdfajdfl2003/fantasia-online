'use strict';
// ============================================================
//  幻想之境 Online — 介面:登入、狀態欄、戰鬥指令、寵物、孵蛋器、
//  背包、商店、對話、聊天、提示框
// ============================================================
const UI = (() => {
  const el = id => document.getElementById(id);
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const STAT_NAMES = ['力量', '體質', '智力', '敏捷'];
  let skyRAF = 0, twTimer = 0, shopOpen = false, sellMode = false, petSel = 0, renaming = false;
  let bpKey = '', knobSendT = 0, knob = null, hatchBuilt = false, lastBeat = 0;

  // 小型寵物頭像 (畫在 canvas 上)
  function drawPetFace(c, sp, t = 0, scale = 1) {
    const g = c.getContext('2d');
    g.clearRect(0, 0, c.width, c.height);
    if (!sp) return;
    g.imageSmoothingEnabled = false;
    g.save();
    const big = sp === 'griffin' || sp === 'drake' ? 0.75 : 1;
    g.translate(c.width / 2, c.height * 0.82);
    g.scale(scale * big, scale * big);
    drawCreature(g, sp, 0, 0, { face: 1, t, id: 1 });
    g.restore();
  }
  function petIconURL(sp) {
    const c = mkCanvas(48, 48);
    drawPetFace(c, sp, 0, 0.75);
    return c.toDataURL();
  }
  const elemTag = el => `<span class="elem" style="background:${ELEMENT_COLORS[el] || '#888'}">${esc(S.elements[el] || el)}</span>`;
  const stars = n => '★'.repeat(n) + '<span class="dim">' + '★'.repeat(5 - n) + '</span>';

  // ============================================================
  //  登入
  // ============================================================
  function initLogin() {
    for (const c of document.querySelectorAll('.cls canvas')) {
      const g = c.getContext('2d');
      drawHumanoid(g, 24, 52, { ...lookOwner(c.dataset.cls, c.dataset.cls), scale: 2, face: 1 }, 0);
    }
    const DESC = {
      knight: '騎士:強化寵物的攻擊與防禦,削弱敵人。HP 最高,適合新手。',
      hunter: '獵人:操控時間棒,捕捉成功率高、遇敵率低、逃跑容易。',
      priest: '牧師:治癒術、防護罩、復活術,讓寵物撐得更久。',
      mage: '法師:強化寵物魔法,能改變戰場天氣。遇敵率高,練功快。',
      bard: '吟遊詩人:時間棒最快,用歌聲幫全隊回魔、催眠、加速。',
    };
    const showDesc = () => { el('cls-desc').textContent = DESC[document.querySelector('input[name=cls]:checked').value]; };
    document.querySelectorAll('input[name=cls]').forEach(r => r.addEventListener('change', showDesc));
    showDesc();

    const sky = el('sky'), g = sky.getContext('2d'), R = rng(42);
    const stars = Array.from({ length: 160 }, () => [R(), R() * 0.7, R() * 1.5 + 0.5, R() * 6]);
    const frameSky = t => {
      const w = sky.width = innerWidth, h = sky.height = innerHeight;
      const gr = g.createLinearGradient(0, 0, 0, h);
      gr.addColorStop(0, '#05081c'); gr.addColorStop(0.6, '#1a2458'); gr.addColorStop(1, '#4a3a6a');
      g.fillStyle = gr; g.fillRect(0, 0, w, h);
      for (const [x, y, s, p] of stars) { g.globalAlpha = 0.4 + 0.6 * Math.abs(Math.sin(t / 900 + p)); g.fillStyle = '#fff'; g.fillRect(x * w, y * h, s, s); }
      g.globalAlpha = 1;
      g.fillStyle = '#fff8d8'; g.beginPath(); g.arc(w * 0.82, h * 0.18, 34, 0, 7); g.fill();
      g.fillStyle = 'rgba(255,248,216,.08)'; g.beginPath(); g.arc(w * 0.82, h * 0.18, 70, 0, 7); g.fill();
      g.fillStyle = '#1a1838'; g.beginPath(); g.moveTo(0, h);
      for (let x = 0; x <= w; x += 20) g.lineTo(x, h * 0.78 - Math.sin(x / 140) * 40 - Math.sin(x / 53) * 14);
      g.lineTo(w, h); g.fill();
      const cx = w * 0.16, by = h * 0.8;
      g.fillStyle = '#100e26';
      g.fillRect(cx - 60, by - 70, 120, 90); g.fillRect(cx - 80, by - 110, 30, 130); g.fillRect(cx + 50, by - 110, 30, 130); g.fillRect(cx - 15, by - 150, 30, 170);
      for (const [tx, tw, ty] of [[cx - 80, 30, by - 110], [cx + 50, 30, by - 110], [cx - 15, 30, by - 150]]) {
        g.beginPath(); g.moveTo(tx - 4, ty); g.lineTo(tx + tw / 2, ty - 34); g.lineTo(tx + tw + 4, ty); g.fill();
      }
      g.fillStyle = '#ffd860';
      for (const [x, y] of [[-68, -90], [58, -90], [-6, -125], [-30, -40], [20, -40]]) g.fillRect(cx + x, by + y, 5, 7);
      g.fillStyle = '#0a0918'; g.beginPath(); g.moveTo(0, h);
      for (let x = 0; x <= w; x += 16) g.lineTo(x, h * 0.9 - Math.sin(x / 90 + 1) * 18);
      g.lineTo(w, h); g.fill();
      skyRAF = requestAnimationFrame(frameSky);
    };
    skyRAF = requestAnimationFrame(frameSky);

    const go = () => {
      const name = el('lg-name').value.trim();
      if (name.length < 2) { el('lg-err').textContent = '請輸入 2~12 個字的角色名稱'; return; }
      initAudio();
      el('lg-btn').disabled = true;
      el('lg-err').textContent = '連線中…';
      const msg = { t: 'login', name, pass: el('lg-pass').value, cls: document.querySelector('input[name=cls]:checked').value };
      if (S.ws && S.ws.readyState === 1) send(msg); else connect(() => send(msg));
    };
    el('lg-btn').onclick = go;
    for (const i of [el('lg-name'), el('lg-pass')]) i.addEventListener('keydown', e => { if (e.key === 'Enter') go(); });
    el('lg-name').focus();
  }
  function loginError(m) { el('lg-err').textContent = m; el('lg-btn').disabled = false; }

  function enterGame(m) {
    cancelAnimationFrame(skyRAF);
    el('login').hidden = true; el('game').hidden = false;
    el('st-name').textContent = m.name;
    el('st-cls').textContent = (S.classes[S.cls] || {}).n || '';
    const pg = el('portrait').getContext('2d');
    pg.imageSmoothingEnabled = false;
    drawHumanoid(pg, 30, 74, { ...lookOwner(S.cls, S.myName), scale: 3, face: 1 }, 0);
    for (const b of document.querySelectorAll('#menu [data-win]')) b.onclick = () => toggleWin(b.dataset.win);
    el('btn-snd').onclick = toggleSound;
    el('btn-art').onclick = toggleArt;
    artLabel();
    el('st-pet').onclick = () => toggleWin('pets');
    el('bp-auto').onchange = e => toggleAuto(e.target.checked);
    for (const w of document.querySelectorAll('.win')) {
      w.querySelector('.x').onclick = () => closeWin(w.id.slice(4));
      w.addEventListener('mousedown', () => front(w));
      makeDraggable(w);
    }
    document.addEventListener('mousemove', tipMove);
  }

  // ============================================================
  //  視窗
  // ============================================================
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
  let zTop = 20;
  const front = w => { w.style.zIndex = ++zTop; };
  function toggleWin(n) { const w = el('win-' + n); w.hidden ? openWin(n) : closeWin(n); }
  function openWin(n) {
    el('win-' + n).hidden = false;
    front(el('win-' + n));
    if (n === 'pets') renderPets();
    if (n === 'hatch') renderHatch();
    if (n === 'bank') renderBank();
    sfx('click');
  }
  function closeWin(n) {
    const w = el('win-' + n);
    if (!w || w.hidden) return;
    w.hidden = true;
    if (n === 'shop') shopOpen = false;
    if (n === 'pets') { sellMode = false; renaming = false; }
    if (n === 'dlg') clearInterval(twTimer);
    el('tip').hidden = true;
  }
  function closeAll() { for (const n of ['inv', 'pets', 'hatch', 'help', 'dlg', 'shop', 'bank']) closeWin(n); closeMenus(); }
  function toggleSound() { muted = !muted; el('btn-snd').textContent = '音效:' + (muted ? '關' : '開'); }
  // 美術:圖片 / 程式繪圖 (比較畫風用)
  function artLabel() {
    el('btn-art').textContent = '美術:' + (ART.on ? `圖片${ART.count ? ' (' + ART.count + ')' : ''}` : '程式');
    el('btn-art').title = ART.count ? `public/assets 裡有 ${ART.count} 張圖。沒有圖的角色一律用程式繪圖。` : '還沒有任何圖片,全部用程式繪圖。';
  }
  function toggleArt() {
    ART.on = !ART.on;
    try { localStorage.setItem('fantasia.art', ART.on ? 'on' : 'off'); } catch (e) { /* 忽略 */ }
    artChanged();
  }
  function artChanged() {
    artLabel();
    el('sp-name').dataset.sp = '';   // 讓頭像重畫
    bpKey = '';
    status();
    if (!el('win-pets').hidden) renderPets();
    if (!el('win-bank').hidden) renderBank();
  }

  function overlay(title, msg, btn, fn, extraHTML = '') {
    el('ov-title').textContent = title;
    el('ov-text').textContent = msg;
    el('ov-extra').innerHTML = extraHTML;
    el('ov-btn').textContent = btn;
    el('ov-btn').onclick = () => { el('overlay').hidden = true; fn && fn(); };
    el('overlay').hidden = false;
  }

  // ============================================================
  //  狀態欄
  // ============================================================
  function setBar(id, txt, v, max, label) {
    el(id).style.width = (max ? clamp(v / max, 0, 1) * 100 : 0) + '%';
    el(txt).textContent = `${label}${Math.max(0, v | 0)} / ${max}`;
  }
  function status() {
    const m = S.me;
    if (!m) return;
    setBar('bar-hp', 'txt-hp', m.hp, m.mh, 'HP ');
    setBar('bar-mp', 'txt-mp', m.mp, m.mm, 'MP ');
    const pct = m.nx ? (m.exp / m.nx) * 100 : 0;
    el('bar-xp').style.width = pct + '%';
    el('txt-xp').textContent = `EXP ${pct.toFixed(1)}%`;
    if (el('st-lv').textContent !== String(m.lv)) { el('st-lv').textContent = m.lv; bpKey = ''; }
    // 出戰寵物:戰鬥中用戰鬥單位的即時數值
    const { p } = myUnits();
    const pt = S.pets[S.act];
    const show = p ? { sp: p.c, n: p.n, lv: p.lv, hp: p.hp, mh: p.mh, mp: p.mp, mm: p.mm } : pt ? { sp: pt.sp, n: pt.n, lv: pt.lv, hp: pt.hp, mh: pt.mhp, mp: pt.mp, mm: pt.mmp, star: pt.star } : null;
    el('st-pet').hidden = !show;
    if (!show) return;
    if (el('sp-name').dataset.sp !== show.sp) { drawPetFace(el('pet-face'), show.sp, 0, 0.9); el('sp-name').dataset.sp = show.sp; }
    el('sp-name').textContent = show.n;
    el('sp-lv').textContent = 'Lv.' + show.lv;
    if (pt && !p) el('sp-star').innerHTML = stars(pt.star);
    setBar('sp-hp', 'sp-hptxt', show.hp, show.mh, '');
    setBar('sp-mp', 'sp-mptxt', show.mp, show.mm, '');
    el('sp-foodbar').hidden = !pt;
    if (pt) {
      setBar('sp-food', 'sp-foodtxt', pt.food, 100, '飽食 ');
      el('sp-foodbar').classList.toggle('warn', pt.food < (S.care.hungry || 30));
    }
  }

  // ============================================================
  //  戰鬥指令面板
  // ============================================================
  function battleOpen() {
    el('bpanel').hidden = false;
    el('bp-auto').checked = S.auto;
    bpKey = '';
    drawPetFace(el('bp-ownface'), null);
    const og = el('bp-ownface').getContext('2d');
    og.clearRect(0, 0, 64, 64); og.imageSmoothingEnabled = false;
    drawHumanoid(og, 32, 84, { ...lookOwner(S.cls, S.myName), scale: 3, face: 1 }, 0);
  }
  function battleClose() { el('bpanel').hidden = true; closeMenus(); status(); }
  function battleAuto() { el('bp-auto').checked = S.auto; }

  function btn(label, key, onclick, extra = {}) {
    const b = document.createElement('button');
    b.className = 'bbtn';
    b.innerHTML = `${esc(label)}${extra.sub ? `<small>${esc(extra.sub)}</small>` : ''}<kbd>${key}</kbd>`;
    b.onclick = e => { e.stopPropagation(); onclick(e); };
    for (const [k, v] of Object.entries(extra.data || {})) b.dataset[k] = v;
    if (extra.icon) { b.style.backgroundImage = `url(${extra.icon})`; b.classList.add('has-icon'); }
    return b;
  }
  function buildBattlePanel(p, o) {
    const pb = el('bp-petbtns'), ob = el('bp-ownbtns');
    pb.innerHTML = ''; ob.innerHTML = '';
    if (p) {
      drawPetFace(el('bp-petface'), p.c, 0, 0.9);
      el('bp-petname').textContent = `${p.n} Lv.${p.lv}`;
      pb.appendChild(btn('攻擊', '1', () => petCmd('atk'), { data: { cost: 0, who: 'p' } }));
      const learned = ((S.species[p.c] || {}).skills || []).filter(([, lv]) => p.lv >= lv).map(([s]) => s);
      learned.forEach((s, i) => {
        const sk = S.pskills[s];
        pb.appendChild(btn(sk.name, String(i + 2), () => petCmd('skill', s), { sub: 'MP ' + sk.mp, data: { cost: sk.mp, who: 'p', pskill: s } }));
      });
      pb.appendChild(btn('防禦', '5', () => petCmd('def'), { data: { cost: 0, who: 'p' } }));
      if (p.sy >= 0) pb.appendChild(btn('助攻', 'T', assistCmd, { sub: '默契 0%', data: { who: 'a' } }));
    } else {
      drawPetFace(el('bp-petface'), null);
      el('bp-petname').textContent = '寵物不在場上';
      pb.innerHTML = '<span class="bp-note">寵物倒下了!用「換寵」或「道具 → 復活草」</span>';
    }
    const cls = S.classes[S.cls] || { skills: [] };
    el('bp-ownname').textContent = `${S.myName} Lv.${S.me ? S.me.lv : 1}`;
    cls.skills.forEach((sk, i) => {
      const locked = S.me && S.me.lv < sk.lv;
      ob.appendChild(btn(locked ? `Lv.${sk.lv}` : sk.name, 'QWE'[i], () => ownerSkill(i), { sub: locked ? sk.name : 'MP ' + sk.mp, data: { cost: sk.mp, who: 'o', oskill: i, locked: locked ? 1 : '' } }));
    });
    ob.appendChild(btn('道具', 'R', e => itemMenu(e.currentTarget), { sub: '紅藥水×' + countItem('red_potion'), data: { cost: 0, who: 'o' } }));
    ob.appendChild(btn('封印卡', 'C', () => ownerCmd('cap'), { sub: '×' + countItem('seal_card'), data: { cost: 0, who: 'o', item: 'seal_card' } }));
    ob.appendChild(btn('換寵', 'X', e => swapMenu(e.currentTarget), { data: { cost: 0, who: 'o' } }));
    ob.appendChild(btn('逃跑', 'F', () => ownerCmd('flee'), { data: { cost: 0, who: 'o' } }));
  }
  function battleTick(t) {
    const { rb, o, p } = myUnits();
    if (!rb) return;
    const key = [p && p.i, p && p.lv, p && p.ko, p && p.sy >= 0, o && o.i, S.me && S.me.lv, countItem('red_potion'), countItem('seal_card')].join();
    if (key !== bpKey) { bpKey = key; buildBattlePanel(p && !p.ko ? p : null, o); }
    const atb = (u, id, vals) => {
      el(id).style.width = (u && !u.ko ? unitBar(u, t) : 0) + '%';
      el(id).classList.toggle('ready', !!(u && u.rd && !u.ko));
      el(vals).textContent = u ? `HP ${u.hp}/${u.mh}  MP ${u.mp}/${u.mm}` : '';
    };
    atb(p, 'bp-petatb', 'bp-petvals');
    atb(o, 'bp-ownatb', 'bp-ownvals');
    for (const b of document.querySelectorAll('#bpanel .bbtn')) {
      if (b.dataset.who === 'a') {   // 助攻:默契滿了才能按,不用等主人的時間棒
        const ready = p && !p.ko && p.sy >= 100 && !p.sg && o && !o.ko;
        b.disabled = !ready;
        b.classList.toggle('glow', !!ready);
        b.querySelector('small').textContent = p && p.sg ? '發動中!' : `默契 ${p ? Math.max(0, p.sy) : 0}%`;
        continue;
      }
      const u = b.dataset.who === 'p' ? p : o;
      const ok = u && u.rd && !u.ko && u.mp >= (+b.dataset.cost || 0) && !b.dataset.locked && !(u.st || []).includes('sleep');
      b.disabled = !ok;
    }
    const tg = S.uidx.get(S.target);
    const al = S.uidx.get(S.allyTarget);
    el('bp-target').innerHTML = (tg ? `目標:<b class="foe">Lv.${tg.lv} ${esc(tg.n)}</b> ${elemTag(tg.el)} <small>(Tab 切換)</small>` : '點選敵人作為目標')
      + (al && !al.ko && al.pid !== S.myId ? `  補血對象:<b class="ally">${esc(al.n)}</b>` : '');
  }
  function countItem(id) { return S.inv.filter(s => s.id === id).reduce((a, s) => a + s.n, 0); }

  function popMenu(anchor, items) {
    const m = el('menu-pop');
    m.innerHTML = '';
    for (const it of items) {
      const b = document.createElement('button');
      b.innerHTML = it.html;
      b.disabled = !!it.disabled;
      if (it.cls) b.className = it.cls;
      b.onclick = e => { e.stopPropagation(); closeMenus(); it.fn(); };
      m.appendChild(b);
    }
    m.hidden = false;
    if (anchor && anchor.x !== undefined && !anchor.getBoundingClientRect) {   // 指定螢幕座標 (地圖上點寵物)
      m.style.left = Math.max(4, Math.min(anchor.x + 12, innerWidth - m.offsetWidth - 4)) + 'px';
      m.style.top = Math.max(4, Math.min(anchor.y - m.offsetHeight / 2, innerHeight - m.offsetHeight - 4)) + 'px';
      return;
    }
    const r = (anchor || el('bp-ownbtns')).getBoundingClientRect();
    m.style.left = Math.max(4, Math.min(r.left, innerWidth - 220)) + 'px';
    m.style.top = Math.max(4, r.top - m.offsetHeight - 6) + 'px';
  }
  function closeMenus() { el('menu-pop').hidden = true; }
  function itemMenu(anchor) {
    popMenu(anchor, ['red_potion', 'blue_potion', 'revive_herb'].map(id => ({
      html: `<img src="${iconURLof(id, S.items[id])}"> ${esc(S.items[id].name)} ×${countItem(id)}`,
      disabled: !countItem(id), fn: () => ownerCmd('item', { item: id }),
    })));
  }
  function swapMenu(anchor) {
    if (!S.myBattle) return;
    const { p } = myUnits();
    popMenu(anchor || document.querySelector('#bp-ownbtns .bbtn:nth-last-child(2)'), S.pets.map((pt, i) => ({
      html: `<img src="${petIconURL(pt.sp)}"> ${esc(pt.n)} Lv.${pt.lv} <small>HP ${pt.hp}/${pt.mhp}</small>`,
      disabled: pt.hp <= 0 || (p && i === S.act && !p.ko),
      fn: () => ownerCmd('swap', { i }),
    })));
  }

  // ============================================================
  //  寵物視窗
  // ============================================================
  function openPets(sell) { sellMode = !!sell; openWin('pets'); }
  function petPrice(pt) { return 30 + pt.lv * 15 + pt.q * 25 + ((S.species[pt.sp] || {}).egg ? 100 : 0); }
  function pets() {
    status();
    bpKey = '';
    bank();
    if (el('win-pets').hidden) return;
    if (renaming) renderPetList();   // 改名中不要重畫詳細資料,不然輸入框會被洗掉
    else renderPets();
  }
  function renderPets() {
    renderPetList();
    renderPetDetail();
  }
  function renderPetList() {
    el('pets-title').textContent = sellMode ? '賣寵物給葛莉絲婆婆' : `寵物 (${S.pets.length}/${S.petMax})`;
    petSel = Math.min(petSel, Math.max(0, S.pets.length - 1));
    const list = el('pet-list');
    list.innerHTML = '';
    for (let i = 0; i < S.petMax; i++) {
      const pt = S.pets[i], d = document.createElement('div');
      if (!pt) { d.className = 'pet-slot empty'; d.textContent = '空的封印卡欄位'; list.appendChild(d); continue; }
      d.className = 'pet-slot' + (i === petSel ? ' sel' : '') + (pt.hp <= 0 ? ' ko' : '');
      const mood = MOOD_TAG[pt.mood];
      d.innerHTML = `<img src="${petIconURL(pt.sp)}"><div class="ps-info"><b>${esc(pt.n)}</b>${i === S.act ? '<span class="act">出戰</span>' : ''}
        ${mood ? `<span class="mood-tag ${mood[1]}">${mood[0]}</span>` : ''}<br>
        Lv.${pt.lv} <span class="star">${stars(pt.star)}</span>
        <div class="bar thin hp"><i style="width:${clamp(pt.hp / pt.mhp, 0, 1) * 100}%"></i></div></div>`;
      d.onclick = () => { petSel = i; renaming = false; renderPets(); };
      list.appendChild(d);
    }
  }
  function renderPetDetail() {
    const box = el('pet-detail'), pt = S.pets[petSel];
    if (!pt) { box.innerHTML = ''; return; }
    const sp = S.species[pt.sp] || {}, inBattle = !!S.myBattle;
    const skillsHTML = (sp.skills || []).map(([s, lv]) => {
      const sk = S.pskills[s], ok = pt.lv >= lv;
      return `<span class="skill-chip${ok ? '' : ' locked'}" data-pskill="${s}">${esc(sk.name)}<small>${ok ? 'MP ' + sk.mp : 'Lv.' + lv}</small></span>`;
    }).join('');
    const row = (i, derivedName, derivedVal) => `<tr><th>${STAT_NAMES[i]}</th><td>${pt.st[i]}</td>
      <td><button class="plus" data-s="${i}" ${pt.pts > 0 && !inBattle ? '' : 'disabled'}>+</button></td>
      <th>${derivedName}</th><td>${derivedVal}</td></tr>`;
    box.innerHTML = `
      <div class="pd-top">
        <canvas id="pd-face" width="96" height="96"></canvas>
        <div class="pd-info">
          <div class="pd-name">${renaming ? `<input id="pd-rename" maxlength="8" value="${esc(pt.n)}">` : `<b>${esc(pt.n)}</b> <button class="mini" id="pd-ren">改名</button>`}</div>
          <div>${esc(sp.n || pt.sp)} ${elemTag(sp.el)} <span class="dim">${esc({ beast: '野獸屬', bug: '蟲獸屬', wing: '翼獸屬', humanoid: '類人屬', fairy: '妖精屬' }[sp.fam] || '')}</span></div>
          <div>天生素質 <b class="gold">${pt.q}</b> 點 <span class="star">${stars(pt.star)}</span></div>
          <div>Lv.${pt.lv} <div class="bar thin xp inline"><i style="width:${pt.exp / pt.nx * 100}%"></i><span>${pt.exp}/${pt.nx}</span></div></div>
          <div class="bar thin hp"><i style="width:${clamp(pt.hp / pt.mhp, 0, 1) * 100}%"></i><span>HP ${pt.hp}/${pt.mhp}</span></div>
          <div class="bar thin mp"><i style="width:${clamp(pt.mp / pt.mmp, 0, 1) * 100}%"></i><span>MP ${pt.mp}/${pt.mmp}</span></div>
        </div>
      </div>
      ${careHTML(pt, inBattle)}
      <table class="pd-stats">
        ${row(0, '攻擊', pt.atk)}${row(1, '防禦', pt.def)}${row(2, '魔攻', pt.matk)}${row(3, '魔防', pt.mdef)}
        <tr><th>剩餘點數</th><td class="gold">${pt.pts}</td><td><button class="mini" id="pd-auto" ${pt.pts > 0 && !inBattle ? '' : 'disabled'}>自動</button></td><th>速度</th><td>${pt.spd}</td></tr>
      </table>
      <div class="pd-skills">${skillsHTML}</div>
      <div class="pd-btns">${sellMode
        ? `<button id="pd-sell" ${S.pets.length <= 1 ? 'disabled' : ''}>賣給婆婆 (${petPrice(pt)} 金幣)</button>`
        : `<button id="pd-act" ${petSel === S.act || inBattle ? 'disabled' : ''}>設為出戰</button>
           <button id="pd-rel" ${S.pets.length <= 1 || inBattle ? 'disabled' : ''}>放生</button>`}</div>
      <div class="hint">${inBattle ? '戰鬥中不能配點或更換出戰寵物。' : '點 + 分配能力點數(Shift+點 一次 5 點)。'}</div>`;
    box.querySelectorAll('.plus').forEach(b => b.onclick = e => send({ t: 'palloc', i: petSel, s: +b.dataset.s, n: e.shiftKey ? 5 : 1 }));
    const q = id => box.querySelector('#' + id);
    const idx = petSel;
    if (q('pd-feed')) q('pd-feed').onclick = e => { e.stopPropagation(); feedMenu(e.currentTarget, idx); };
    for (const a of ['pet', 'play', 'trick']) if (q('pd-' + a)) q('pd-' + a).onclick = () => send({ t: 'pact', i: idx, a });
    if (q('pd-auto')) q('pd-auto').onclick = () => send({ t: 'pauto', i: petSel });
    if (q('pd-act')) q('pd-act').onclick = () => send({ t: 'pset', i: petSel });
    if (q('pd-rel')) q('pd-rel').onclick = () => { if (confirm(`確定要放生「${pt.n}」嗎?放生之後就回不來了。`)) send({ t: 'prelease', i: petSel }); };
    if (q('pd-sell')) q('pd-sell').onclick = () => { if (confirm(`確定要把「${pt.n}」以 ${petPrice(pt)} 金幣賣給婆婆嗎?`)) send({ t: 'psell', i: petSel }); };
    if (q('pd-ren')) q('pd-ren').onclick = () => { renaming = true; renderPetDetail(); q('pd-rename') && q('pd-rename').focus(); };
    const ri = q('pd-rename');
    if (ri) {
      ri.focus(); ri.select();
      ri.onkeydown = e => {
        if (e.key === 'Enter') { const v = ri.value.trim(); if (v) send({ t: 'pname', i: petSel, n: v }); renaming = false; renderPetDetail(); }
        else if (e.key === 'Escape') { renaming = false; renderPetDetail(); }
        e.stopPropagation();
      };
    }
  }

  // ============================================================
  //  寵物照顧:飽食度 / 快樂值 / 親密度、餵食、互動
  // ============================================================
  const MOOD_TAG = { starve: ['餓昏', 'bad'], hungry: ['肚子餓', 'warn'], angry: ['鬧脾氣', 'bad'], love: ['♥', 'love'] };
  const careWord = {
    food: v => v <= 0 ? ['餓昏了!', 'bad'] : v < (S.care.hungry || 30) ? ['肚子餓', 'warn'] : v >= (S.care.full || 90) ? ['吃飽了', 'good'] : ['', ''],
    joy: v => v < 10 ? ['非常不開心', 'bad'] : v < 30 ? ['鬧脾氣', 'warn'] : v >= 80 ? ['很開心', 'good'] : ['普通', ''],
    bond: v => v < 20 ? ['陌生', ''] : v < 40 ? ['熟悉', ''] : v < 60 ? ['親近', 'good'] : v < 80 ? ['信賴', 'good'] : ['心意相通', 'love'],
  };
  const tasteOf = (sp, id) => sp.love === '*' ? 'like' : id === sp.love ? 'love' : id === sp.hate ? 'hate' : 'ok';
  function careHTML(pt, inBattle) {
    const sp = S.species[pt.sp] || {}, C = S.care;
    const bar = (k, label, v) => {
      const [w, c] = careWord[k](v);
      return `<div class="care-row"><span>${label}</span><div class="bar thin ${k}"><i style="width:${clamp(v, 0, 100)}%"></i><span>${v} / 100</span></div><em class="${c}">${w}</em></div>`;
    };
    const food = id => id && S.items[id] ? `<img src="${iconURLof(id, S.items[id])}">${esc(S.items[id].name)}` : '—';
    const taste = sp.love === '*' ? '雜食:什麼都喜歡吃' : `最愛 ${food(sp.love)}  討厭 ${food(sp.hate)}`;
    const cd = a => pt.cd && pt.cd[a] > 0 ? '<small>(冷卻)</small>' : '';
    const lock = (need, name) => pt.bond >= need ? `<b class="good">${name}</b>` : `<span class="dim">${name}(親密 ${need})</span>`;
    const syncB = C.sync_bond || 40, trickB = C.trick_bond || 50, guardB = C.guard_bond || 60;
    return `<div class="pd-care">
      ${bar('food', '飽食度', pt.food)}${bar('joy', '快樂值', pt.joy)}${bar('bond', '親密度', pt.bond)}
      <div class="care-taste">${taste}${pt.sulk ? ' <span class="mood-tag bad">賭氣中</span>' : ''}</div>
      <div class="care-btns">
        <button id="pd-feed" ${inBattle ? 'disabled' : ''}>餵食 ▸</button>
        <button id="pd-pet" ${inBattle ? 'disabled' : ''}>摸摸${cd('pet')}</button>
        <button id="pd-play" ${inBattle || pt.food < 10 ? 'disabled' : ''}>玩耍${cd('play')}</button>
        <button id="pd-trick" ${inBattle || pt.bond < trickB ? 'disabled' : ''}>表演</button>
      </div>
      <div class="care-bond">助攻加成 <b class="gold">+${Math.round((C.assist || 0.5) * Math.min(100, pt.bond))}%</b> ·
        ${lock(syncB, '默契助攻')}${pt.bond >= syncB ? ` <small>${pt.sync}%</small>` : ''} · ${lock(trickB, '表演')} · ${lock(guardB, '護主')}</div>
    </div>`;
  }
  function feedMenu(anchor, idx) {
    const pt = S.pets[idx];
    if (!pt) return;
    const sp = S.species[pt.sp] || {}, order = { love: 0, like: 1, ok: 2, hate: 3 };
    const foods = [...S.foods].sort((a, b) => order[tasteOf(sp, a)] - order[tasteOf(sp, b)]);
    const items = foods.map(id => {
      const r = tasteOf(sp, id), n = countItem(id);
      return { html: `<img src="${iconURLof(id, S.items[id])}"> ${esc(S.items[id].name)} ×${n} <small class="taste-${r}">${esc(S.tasteNames[r] || '')}</small>`,
        disabled: !n, fn: () => send({ t: 'feed', i: idx, item: id }) };
    });
    items.unshift({ html: `餵 <b>${esc(pt.n)}</b> 吃什麼?<small>飽食 ${pt.food}</small>`, disabled: true, cls: 'menu-head', fn: () => {} });
    if (!S.foods.some(countItem)) items.push({ html: '<span class="dim">背包裡沒有食物,向莉莉購買吧</span>', disabled: true, cls: 'menu-head', fn: () => {} });
    popMenu(anchor, items);
  }
  // 在地圖上點自己的寵物
  function petMenu(x, y) {
    const idx = S.act, pt = S.pets[idx];
    if (!pt || S.myBattle) return;
    const trickB = S.care.trick_bond || 50, cd = a => pt.cd && pt.cd[a] > 0 ? '<small>冷卻中</small>' : '';
    const trick = (S.species[pt.sp] || {}).trick || [''];
    popMenu({ x, y }, [
      { html: `<b>${esc(pt.n)}</b><small>飽食 ${pt.food} 快樂 ${pt.joy} 親密 ${pt.bond}</small>`, disabled: true, cls: 'menu-head', fn: () => {} },
      { html: `摸摸 ${cd('pet')}`, fn: () => send({ t: 'pact', i: idx, a: 'pet' }) },
      { html: '餵食 ▸', fn: () => setTimeout(() => feedMenu({ x, y }, idx), 0) },
      { html: pt.food < 10 ? '玩耍 <small>太餓了</small>' : `玩耍 ${cd('play')}`, disabled: pt.food < 10, fn: () => send({ t: 'pact', i: idx, a: 'play' }) },
      { html: pt.bond < trickB ? `表演 <small>親密 ${trickB}</small>` : `表演「${esc(trick[0])}」`, disabled: pt.bond < trickB, fn: () => send({ t: 'pact', i: idx, a: 'trick' }) },
      { html: '寵物資料', fn: () => { petSel = idx; openWin('pets'); } },
    ]);
  }

  // ============================================================
  //  寵物旅館
  // ============================================================
  function openBank() { openWin('bank'); }
  function bank() { if (!el('win-bank').hidden) renderBank(); }
  const bankCount = () => S.bank.filter(x => !x.sulk).length;
  function bankRow(pt, i, put) {
    const d = document.createElement('div');
    d.className = 'bank-row' + (pt.sulk ? ' sulk' : '');
    d.innerHTML = `<img src="${petIconURL(pt.sp)}"><div class="ps-info"><b>${esc(pt.n)}</b> Lv.${pt.lv} <span class="star">${stars(pt.star)}</span>
      ${pt.sulk ? '<span class="mood-tag bad">賭氣中</span>' : ''}<br><small>飽食 ${pt.food} · 快樂 ${pt.joy} · 親密 ${pt.bond}</small></div>`;
    const b = document.createElement('button');
    b.textContent = put ? '寄放 →' : '← 領回';
    b.disabled = put ? (S.pets.length <= 1 || bankCount() >= S.bankMax) : S.pets.length >= S.petMax;
    b.onclick = () => send({ t: put ? 'bput' : 'bget', i });
    d.appendChild(b);
    return d;
  }
  function renderBank() {
    const a = el('bank-party'), b = el('bank-list');
    a.innerHTML = ''; b.innerHTML = '';
    S.pets.forEach((pt, i) => a.appendChild(bankRow(pt, i, true)));
    S.bank.forEach((pt, i) => b.appendChild(bankRow(pt, i, false)));
    if (!S.bank.length) b.innerHTML = '<div class="dim bank-empty">旅館裡還沒有寵物。</div>';
    el('bank-n1').textContent = `${S.pets.length}/${S.petMax}`;
    el('bank-n2').textContent = `${bankCount()}/${S.bankMax}`;
  }

  // ============================================================
  //  孵蛋器
  // ============================================================
  function openHatch() { openWin('hatch'); }
  function renderHatch() {
    const body = el('hatch-body');
    hatchBuilt = false;
    if (!S.hatch) {
      const eggs = S.inv.map((s, i) => ({ s, i })).filter(({ s }) => S.items[s.id] && S.items[s.id].type === 'egg');
      body.innerHTML = `<p class="hatch-intro">選一顆蛋放進孵蛋器。孵化需要 ${S.hatchTime} 秒,要一直照顧喔!</p>` +
        (eggs.length ? eggs.map(({ s, i }) => `<div class="shop-row"><div class="slot" data-item="${s.id}" style="background-image:url(${iconURLof(s.id, S.items[s.id])})"></div>
          <div class="nm">${esc(S.items[s.id].name)} ×${s.n}<small>${esc(S.items[s.id].desc)}</small></div><button data-slot="${i}">放入</button></div>`).join('')
          : '<p class="dim">你身上沒有蛋。可以向葛莉絲婆婆購買寵物蛋。</p>');
      body.querySelectorAll('button[data-slot]').forEach(b => b.onclick = () => { knob = null; send({ t: 'hstart', slot: +b.dataset.slot }); });
      return;
    }
    body.innerHTML = `
      <canvas id="hatch-cv" width="300" height="150"></canvas>
      <div class="meter"><span>溫度計</span><div class="mbar temp"><i id="hm-t"></i></div><b id="hm-tv">0</b>°</div>
      <div class="meter"><span>濕度計</span><div class="mbar hum"><i id="hm-h"></i></div><b id="hm-hv">0</b>%</div>
      <div class="knob"><span>加熱器</span><button data-k="t" data-d="-2">◀</button><input type="range" id="hk-t" min="0" max="100" step="1"><button data-k="t" data-d="2">▶</button></div>
      <div class="knob"><span>加濕器</span><button data-k="h" data-d="-2">◀</button><input type="range" id="hk-h" min="0" max="100" step="1"><button data-k="h" data-d="2">▶</button></div>
      <div class="meter"><span id="hm-phase">預熱中</span><div class="mbar time"><i id="hm-time"></i><em style="left:${S.hatchWarmup / S.hatchTime * 100}%"></em></div><b id="hm-left"></b>秒</div>
      <div class="hint">環境溫濕度會慢慢飄動,要一直微調。蛋覺得舒服時心跳會又穩又強。<br>前 ${S.hatchWarmup} 秒是預熱,可以慢慢摸索,不影響結果。</div>`;
    knob = knob || { t: S.hatch.kt, h: S.hatch.kh };
    el('hk-t').value = knob.t; el('hk-h').value = knob.h;
    el('hk-t').oninput = e => { knob.t = +e.target.value; sendKnob(); };
    el('hk-h').oninput = e => { knob.h = +e.target.value; sendKnob(); };
    body.querySelectorAll('button[data-k]').forEach(b => b.onclick = () => {
      knob[b.dataset.k] = clamp(knob[b.dataset.k] + +b.dataset.d, 0, 100);
      el('hk-' + b.dataset.k).value = knob[b.dataset.k];
      sendKnob(true);
    });
    hatchBuilt = true;
    hatchUpdate();
  }
  function sendKnob(now) {
    if (!knob || !S.hatch) return;   // 孵化已結束 (延遲送出的那一次不用送了)
    const t = performance.now();
    if (!now && t - knobSendT < 90) { clearTimeout(sendKnob.tm); sendKnob.tm = setTimeout(() => sendKnob(true), 100); return; }
    knobSendT = t;
    send({ t: 'hknob', kt: knob.t, kh: knob.h });
  }
  function hatchUpdate() {
    const h = S.hatch;
    if (!h || el('win-hatch').hidden) return;
    if (!hatchBuilt) { renderHatch(); return; }
    el('hm-t').style.width = h.at + '%'; el('hm-tv').textContent = h.at.toFixed(0);
    el('hm-h').style.width = h.ah + '%'; el('hm-hv').textContent = h.ah.toFixed(0);
    el('hm-time').style.width = Math.min(100, h.el / S.hatchTime * 100) + '%';
    el('hm-left').textContent = Math.max(0, Math.ceil(S.hatchTime - h.el));
    el('hm-phase').textContent = h.el < S.hatchWarmup ? '預熱中' : '孵化中';
  }
  function drawHatchEgg(t) {
    const c = el('hatch-cv');
    if (!c || !S.hatch) return;
    const g = c.getContext('2d'), h = S.hatch, sp = S.species[h.sp] || {}, col = ELEMENT_COLORS[sp.el] || '#ccc';
    g.clearRect(0, 0, c.width, c.height);
    // 孵蛋器
    const gr = g.createLinearGradient(0, 0, 0, 150);
    gr.addColorStop(0, '#2a1a10'); gr.addColorStop(1, '#4a2e18');
    g.fillStyle = gr; g.fillRect(0, 0, 300, 150);
    g.fillStyle = '#c89a50'; g.fillRect(90, 118, 120, 16); g.fillStyle = '#8a6a30'; g.fillRect(90, 130, 120, 4);
    g.fillStyle = 'rgba(255,240,200,.25)';
    for (let i = 0; i < 8; i++) g.fillRect(100 + i * 13, 108 + Math.sin(i) * 3, 9, 10);   // 稻草
    // 心跳:舒適度越高越強,週期固定
    const period = 900, ph = (t % period) / period;
    const beat = Math.max(0, Math.sin(ph * Math.PI * 2)) ** 6 * h.c;
    if (ph < 0.05 && t - lastBeat > 500 && h.c > 0.25) { lastBeat = t; tone('sine', 110 + h.c * 40, 70, 0.12, 0.03 + h.c * 0.05); }
    const glow = g.createRadialGradient(150, 80, 5, 150, 80, 60 + beat * 25);
    glow.addColorStop(0, `rgba(255,240,200,${0.15 + h.c * 0.45})`); glow.addColorStop(1, 'rgba(255,200,120,0)');
    g.fillStyle = glow; g.fillRect(0, 0, 300, 150);
    const wob = Math.sin(t / 120) * (0.03 + (1 - h.c) * 0.12) * (h.c < 0.3 ? 1.6 : 1);
    const sc = 1 + beat * 0.07;
    g.save(); g.translate(150, 114); g.rotate(wob); g.scale(sc, sc);
    g.fillStyle = '#f6f0dc'; g.beginPath(); g.ellipse(0, -38, 30, 38, 0, 0, 7); g.fill();
    g.strokeStyle = '#6a5a3a'; g.lineWidth = 2; g.stroke();
    g.fillStyle = col;
    [[-12, -52, 7], [12, -40, 6], [-6, -22, 5], [14, -62, 4], [-16, -32, 3]].forEach(([x, y, r]) => { g.beginPath(); g.arc(x, y, r, 0, 7); g.fill(); });
    g.fillStyle = 'rgba(255,255,255,.8)'; g.fillRect(-18, -62, 4, 10);
    g.restore();
    g.font = `bold 13px ${FONT}`; g.textAlign = 'left'; g.textBaseline = 'top';
    g.fillStyle = '#ffe8a8'; g.fillText((S.items['egg_' + h.sp] || {}).name || '寵物蛋', 8, 8);
    // 心跳指示
    g.fillStyle = '#ffffff'; g.fillText('心跳', 222, 8);
    for (let i = 0; i < 5; i++) {
      g.fillStyle = i < Math.round(h.c * 5) ? '#ff6a8a' : 'rgba(255,255,255,.2)';
      g.beginPath(); const x = 228 + i * 13, y = 34;
      g.moveTo(x, y + 4); g.bezierCurveTo(x, y - 2, x - 7, y - 2, x - 6, y + 2); g.lineTo(x, y + 9);
      g.lineTo(x + 6, y + 2); g.bezierCurveTo(x + 7, y - 2, x, y - 2, x, y + 4); g.fill();
    }
  }
  function hatched(pet) {
    knob = null;
    if (!el('win-hatch').hidden) renderHatch();
    const c = mkCanvas(120, 110);
    drawPetFace(c, pet.sp, 0, 1.4);
    overlay('孵化成功!', `${pet.n} 誕生了!`, '太棒了!', null,
      `<img class="ov-pet" src="${c.toDataURL()}">
       <div class="ov-star">${stars(pet.star)}</div>
       <div>天生素質 <b class="gold">${pet.q}</b> 點${pet.q >= 12 ? '  <b class="gold">極品!</b>' : ''}</div>
       <div class="dim">力量 ${pet.st[0]} · 體質 ${pet.st[1]} · 智力 ${pet.st[2]} · 敏捷 ${pet.st[3]}</div>`);
  }

  // ============================================================
  //  背包 / 商店 / 對話
  // ============================================================
  function inv() {
    const grid = el('inv-grid');
    grid.innerHTML = '';
    for (let i = 0; i < 24; i++) {
      const s = S.inv[i], d = document.createElement('div');
      d.className = 'slot';
      if (s) {
        d.dataset.item = s.id;
        d.style.backgroundImage = `url(${iconURLof(s.id, S.items[s.id])})`;
        if (s.n > 1) d.innerHTML = `<span class="cnt">${s.n}</span>`;
        d.ondblclick = () => {
          const it = S.items[s.id];
          if (it.type === 'egg' && !el('win-hatch').hidden && !S.hatch) send({ t: 'hstart', slot: i });
          else send({ t: 'use', slot: i });
        };
        d.oncontextmenu = ev => { ev.preventDefault(); send({ t: 'sell', slot: i }); };
      }
      grid.appendChild(d);
    }
    el('inv-gold').textContent = S.gold.toLocaleString();
    el('st-gold').textContent = S.gold.toLocaleString();
    bpKey = '';
    if (!el('win-hatch').hidden && !S.hatch) renderHatch();
  }

  function shop(m) {
    el('shop-title').textContent = m.title || '商店';
    const list = el('shop-list');
    list.innerHTML = '';
    for (const id of m.items) {
      const it = S.items[id], row = document.createElement('div');
      row.className = 'shop-row';
      row.innerHTML = `<div class="slot" data-shop="${id}" style="background-image:url(${iconURLof(id, it)})"></div>
        <div class="nm">${esc(it.name)}<small>${esc(it.desc || '')}</small></div><div class="pr">${it.price}</div>`;
      const b = document.createElement('button');
      b.textContent = '購買';
      b.onclick = e => send({ t: 'buy', item: id, n: e.shiftKey && it.type !== 'egg' ? 10 : 1 });
      row.appendChild(b);
      list.appendChild(row);
    }
    shopOpen = true;
    openWin('shop');
    openWin('inv');
  }

  function dialog(m) {
    el('dlg-name').textContent = m.n;
    const t = el('dlg-text');
    let i = 0;
    clearInterval(twTimer);
    t.textContent = '';
    twTimer = setInterval(() => { i++; t.textContent = m.text.slice(0, i); if (i >= m.text.length) clearInterval(twTimer); }, 25);
    t.onclick = () => { clearInterval(twTimer); t.textContent = m.text; };
    const opts = el('dlg-opts');
    opts.innerHTML = '';
    for (const [act, label] of m.opts) {
      const b = document.createElement('button');
      b.textContent = '▶ ' + label;
      b.onclick = () => { if (act !== 'close') send({ t: 'dlg', npc: m.i, act }); if (act !== 'hint') closeWin('dlg'); };
      opts.appendChild(b);
    }
    openWin('dlg');
  }

  // ============================================================
  //  聊天
  // ============================================================
  function chat(m) {
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
    const log = el('chat-log'), d = document.createElement('div');
    d.className = 'msg ' + cls;
    d.textContent = str;
    const stick = log.scrollTop + log.clientHeight >= log.scrollHeight - 4;
    log.appendChild(d);
    while (log.children.length > 150) log.firstChild.remove();
    if (stick) log.scrollTop = log.scrollHeight;
    return d;
  }

  // ============================================================
  //  提示框
  // ============================================================
  function itemTip(id, isShop) {
    const it = S.items[id];
    if (!it) return '';
    const type = { use: '消耗品', seal: '捕捉道具', egg: '寵物蛋', food: '寵物食物' }[it.type] || '';
    const tastes = it.type === 'food' && S.pets.length ? '<br>' + S.pets.map(pt => {
      const r = tasteOf(S.species[pt.sp] || {}, id);
      return `${esc(pt.n)}:<span class="taste-${r}">${esc(S.tasteNames[r] || '')}</span>`;
    }).join('  ') : '';
    return `<b>${esc(it.name)}</b><br><span class="t">${type}</span><br>${esc(it.desc || '')}${tastes}<br>` +
      (isShop ? `<span class="p">售價 ${it.price} 金幣</span>` : `<span class="p">賣出價 ${Math.floor(it.price / 3)} 金幣</span>`);
  }
  function pskillTip(s) {
    const sk = S.pskills[s];
    if (!sk) return '';
    const tgt = { enemy: '單一敵人', enemies: '全體敵人', ally: '單一隊友' }[sk.target];
    const kind = { phys: '物理', mag: '魔法', status: '狀態', heal: '治療' }[sk.type];
    let d = sk.desc || (sk.mult ? `${kind} ${Math.round(sk.mult * 100)}%${sk.hits ? ' ×' + sk.hits : ''}` : '');
    return `<b>${esc(sk.name)}</b> ${sk.el ? elemTag(sk.el) : ''}<br><span class="t">${kind} · ${tgt} · MP ${sk.mp}</span><br>${esc(d)}`;
  }
  function oskillTip(i) {
    const sk = (S.classes[S.cls] || { skills: [] }).skills[i];
    if (!sk) return '';
    return `<b>${esc(sk.name)}</b><br><span class="t">需求 Lv.${sk.lv} · MP ${sk.mp}</span><br>${esc(sk.desc)}`;
  }
  function tipMove(e) {
    const tip = el('tip'), t = e.target.closest && e.target.closest('[data-item],[data-shop],[data-pskill],[data-oskill]');
    if (!t) { tip.hidden = true; return; }
    tip.innerHTML = t.dataset.pskill ? pskillTip(t.dataset.pskill) : t.dataset.oskill !== undefined ? oskillTip(+t.dataset.oskill)
      : itemTip(t.dataset.item || t.dataset.shop, !!t.dataset.shop);
    tip.hidden = !tip.innerHTML;
    tip.style.left = Math.min(e.clientX + 14, innerWidth - tip.offsetWidth - 4) + 'px';
    tip.style.top = Math.min(e.clientY + 14, innerHeight - tip.offsetHeight - 4) + 'px';
  }

  // ============================================================
  //  每幀更新
  // ============================================================
  function tick(t) {
    if (S.myBattle) battleTick(t);
    if (!el('win-pets').hidden && S.pets[petSel]) { const c = el('pd-face'); if (c) drawPetFace(c, S.pets[petSel].sp, t, 1.2); }
    if (!el('win-hatch').hidden) drawHatchEgg(t);
  }

  return {
    initLogin, loginError, enterGame, overlay, status, inv, pets, chat, addChat, dialog, shop,
    openHatch, hatchUpdate, hatched, openPets, battleOpen, battleClose, battleAuto, tick,
    closeMenus, swapMenu, toggleWin, toggleSound, closeAll, petMenu, bank, openBank, artChanged,
  };
})();

UI.initLogin();
