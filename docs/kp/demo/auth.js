/**
 * Bloom CRM · demo auth + profile
 * Test: admin / admin
 */
(function (global) {
  'use strict';

  var STORAGE_KEY = 'bloom_demo_auth_v1';
  var PROFILE_KEY = 'bloom_demo_profile_v1';
  var DEMO_USER = 'admin';

  var USERS = {
    admin: {
      pass: 'admin',
      displayName: 'Анна К.',
      role: 'Владелец сети',
      email: 'anna@bloom.local',
      phone: '+7 900 111-22-33',
      shop: 'Вся сеть',
      notify: true
    },
    florist: {
      pass: 'florist',
      displayName: 'Светлана П.',
      role: 'Флорист',
      email: 'sveta@bloom.local',
      phone: '+7 900 555-66-77',
      shop: 'Ленина 92',
      notify: true
    }
  };

  function defaultProfile(user) {
    var u = USERS[user] || USERS.admin;
    return {
      login: user || DEMO_USER,
      displayName: u.displayName,
      role: u.role,
      email: u.email,
      phone: u.phone,
      shop: u.shop,
      notify: u.notify,
      avatarDataUrl: null
    };
  }

  function readSession() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return null;
      var s = JSON.parse(raw);
      if (!s || !s.user || !s.at) return null;
      return s;
    } catch (_) {
      return null;
    }
  }

  function writeSession(user) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      user: user,
      at: Date.now(),
      role: user === DEMO_USER ? 'owner' : 'user'
    }));
  }

  function clearSession() {
    localStorage.removeItem(STORAGE_KEY);
  }

  function readProfile() {
    var user = currentUser() || DEMO_USER;
    var base = defaultProfile(user);
    try {
      var raw = localStorage.getItem(PROFILE_KEY);
      if (!raw) return base;
      var p = JSON.parse(raw);
      if (!p || p.login !== user) return base;
      return Object.assign({}, base, p, { login: user });
    } catch (_) {
      return base;
    }
  }

  function writeProfile(p) {
    var cur = readProfile();
    var next = Object.assign({}, cur, p || {}, { login: currentUser() || cur.login });
    localStorage.setItem(PROFILE_KEY, JSON.stringify(next));
    return next;
  }

  function isAuthed() {
    return !!readSession();
  }

  function currentUser() {
    var s = readSession();
    return s ? s.user : null;
  }

  function login(user, pass) {
    user = String(user || '').trim().toLowerCase();
    pass = String(pass || '');
    var u = USERS[user];
    if (!u || u.pass !== pass) return { ok: false, error: 'Неверный логин или пароль' };
    writeSession(user);
    var existing = null;
    try { existing = JSON.parse(localStorage.getItem(PROFILE_KEY) || 'null'); } catch (_) {}
    if (!existing || existing.login !== user) writeProfile(defaultProfile(user));
    return { ok: true };
  }

  function logout() {
    clearSession();
  }

  function initials(name) {
    var parts = String(name || 'A').trim().split(/\s+/).filter(Boolean);
    if (!parts.length) return 'A';
    if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
    return (parts[0][0] + parts[1][0]).toUpperCase();
  }

  function ensureStyles() {
    if (document.getElementById('bloom-auth-styles')) return;
    var css = document.createElement('style');
    css.id = 'bloom-auth-styles';
    css.textContent = [
      '#bloomAuthGate{position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;overflow:hidden;',
      'background:linear-gradient(165deg,#FBF8F4 0%,#F6EFE5 55%,#F2E9DE 100%),',
      'radial-gradient(720px 430px at 10% 0%,rgba(180,99,47,.14),transparent 55%),',
      'radial-gradient(640px 420px at 100% 8%,rgba(109,75,98,.13),transparent 52%),',
      'radial-gradient(560px 400px at 82% 100%,rgba(92,122,99,.13),transparent 55%),#FBF8F4;',
      'font-family:Inter,system-ui,-apple-system,sans-serif;padding:20px}',
      '#bloomAuthGate.hidden{display:none}',
      '#bloomAuthGate::before{content:"";position:absolute;inset:0;pointer-events:none;opacity:.05;',
      'background-image:url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' width=\'120\' height=\'120\'%3E%3Cfilter id=\'n\'%3E%3CfeTurbulence type=\'fractalNoise\' baseFrequency=\'.85\' numOctaves=\'2\' stitchTiles=\'stitch\'/%3E%3C/filter%3E%3Crect width=\'120\' height=\'120\' filter=\'url(%23n)\'/%3E%3C/svg%3E")}',
      '#bloomAuthGate::after{content:"";position:absolute;inset:0;pointer-events:none;',
      'box-shadow:inset 0 0 0 1px rgba(255,255,255,.4),inset 0 0 160px rgba(180,99,47,.07)}',
      '#bloomAuthGate .petal{position:absolute;z-index:0;pointer-events:none;opacity:0;',
      'border-radius:62% 38% 55% 45%/48% 58% 42% 52%;',
      'background:linear-gradient(135deg,rgba(180,99,47,.16),rgba(180,99,47,.02));',
      'animation:bloomPetal 11s ease-in-out infinite}',
      '#bloomAuthGate .petal.p1{width:130px;height:92px;left:5%;bottom:-130px}',
      '#bloomAuthGate .petal.p2{width:104px;height:72px;right:7%;bottom:-120px;',
      'background:linear-gradient(135deg,rgba(109,75,98,.16),rgba(92,122,99,.03));',
      'animation-duration:13s;animation-delay:2.6s}',
      '@keyframes bloomPetal{0%{transform:translateY(0) rotate(-10deg);opacity:0}',
      '12%{opacity:.65}70%{opacity:.45}100%{transform:translateY(-140vh) rotate(14deg);opacity:0}}',
      '@keyframes bloomGateIn{from{opacity:0;transform:translateY(14px) scale(.97)}',
      'to{opacity:1;transform:none}}',
      '#bloomAuthGate .box{position:relative;z-index:1;width:100%;max-width:430px;',
      'background:linear-gradient(rgba(255,253,249,.78),rgba(255,253,249,.78)) padding-box,',
      'linear-gradient(150deg,rgba(180,99,47,.5),rgba(109,75,98,.45)) border-box;',
      'border:1px solid transparent;border-radius:22px;padding:34px 32px 30px;',
      'box-shadow:0 24px 70px rgba(43,36,32,.16),0 6px 22px rgba(43,36,32,.07);',
      'backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);',
      'animation:bloomGateIn .5s cubic-bezier(.22,1,.36,1) both}',
      '#bloomAuthGate .head{text-align:center;margin-bottom:22px}',
      '#bloomAuthGate .kicker{font-size:.66rem;font-weight:750;letter-spacing:.16em;text-transform:uppercase;',
      'color:#B4632F;margin:0 0 12px}',
      '#bloomAuthGate .mark{width:60px;height:60px;border-radius:18px;display:grid;place-items:center;',
      'background:linear-gradient(145deg,#B4632F,#6D4B62);color:#FFFDF9;font-weight:900;font-size:1.35rem;margin:0 auto 16px;',
      'box-shadow:inset 0 1px 0 rgba(255,255,255,.28),inset 0 -8px 16px rgba(43,36,32,.22),',
      '0 0 0 7px rgba(180,99,47,.08),0 14px 30px rgba(180,99,47,.22)}',
      '#bloomAuthGate h1{font-size:1.5rem;font-weight:900;letter-spacing:-.03em;margin:0 0 6px;color:#2B2420}',
      '#bloomAuthGate .sub{font-size:.87rem;color:#8B8178;margin:0;line-height:1.5}',
      '#bloomAuthGate .roles{display:flex;flex-direction:column;gap:11px;margin-bottom:16px}',
      '#bloomAuthGate .role{position:relative;display:flex;align-items:center;gap:14px;width:100%;',
      'padding:16px 16px 16px 20px;border:1px solid #E9E2DA;border-radius:16px;',
      'background:rgba(251,248,244,.85);cursor:pointer;text-align:left;font-family:inherit;',
      'transition:transform .22s cubic-bezier(.22,1,.36,1),border-color .22s,background .22s,box-shadow .22s}',
      '#bloomAuthGate .role::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;border-radius:8px;',
      'background:linear-gradient(180deg,#B4632F,#6D4B62);opacity:0;transition:opacity .22s}',
      '#bloomAuthGate .role:hover{border-color:#E4C6A8;background:#FFFDF9;transform:translateY(-2px);',
      'box-shadow:0 16px 34px rgba(43,36,32,.1),0 4px 12px rgba(180,99,47,.08)}',
      '#bloomAuthGate .role:hover::before{opacity:1}',
      '#bloomAuthGate .role:active{transform:translateY(0) scale(.995)}',
      '#bloomAuthGate .r-ico{width:48px;height:48px;flex:none;border-radius:15px;display:grid;place-items:center;',
      'background:linear-gradient(145deg,#C9763C,#9C5327);color:#FFFDF9;font-weight:800;font-size:.95rem;letter-spacing:.02em;',
      'box-shadow:inset 0 1px 0 rgba(255,255,255,.22),0 6px 14px rgba(180,99,47,.25)}',
      '#bloomAuthGate .r-ico.sp{background:linear-gradient(145deg,#6D4B62,#5C7A63);',
      'box-shadow:inset 0 1px 0 rgba(255,255,255,.22),0 6px 14px rgba(109,75,98,.22)}',
      '#bloomAuthGate .r-txt{flex:1;min-width:0}',
      '#bloomAuthGate .r-txt b{display:block;font-size:.95rem;font-weight:800;color:#2B2420;letter-spacing:-.01em}',
      '#bloomAuthGate .r-sub{display:block;font-size:.77rem;color:#8B8178;margin-top:3px;line-height:1.4}',
      '#bloomAuthGate .r-go{flex:none;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;',
      'color:#B4632F;background:#FFFDF9;border:1px solid #E9E2DA;font-weight:800;font-size:.95rem;',
      'transition:transform .22s cubic-bezier(.22,1,.36,1),background .22s,border-color .22s,color .22s}',
      '#bloomAuthGate .role:hover .r-go{background:#F6E9DE;border-color:#E4C6A8;color:#9C5327;transform:translateX(3px)}',
      '#bloomAuthGate .manual-toggle{display:block;width:100%;background:none;border:0;cursor:pointer;',
      'font-family:inherit;font-size:.78rem;font-weight:650;color:#A39A8F;text-align:center;padding:4px 0 0;margin-bottom:16px;',
      'transition:color .18s}',
      '#bloomAuthGate .manual-toggle:hover{color:#B4632F}',
      '#bloomAuthGate label{display:block;font-size:.67rem;font-weight:750;text-transform:uppercase;',
      'letter-spacing:.06em;color:#A39A8F;margin:0 0 6px}',
      '#bloomAuthGate .field{margin-bottom:13px}',
      '#bloomAuthGate input{width:100%;box-sizing:border-box;border:1px solid #E0D5C9;border-radius:12px;',
      'padding:11px 13px;font-size:.92rem;outline:none;background:#FBF8F4;color:#2B2420;font-family:inherit;',
      'transition:border-color .18s,box-shadow .18s,background .18s}',
      '#bloomAuthGate input:focus{border-color:#B4632F;background:#FFFDF9;box-shadow:0 0 0 3px #F6E9DE}',
      '#bloomAuthGate input::placeholder{color:#B9B0A6}',
      '#bloomAuthGate .err{min-height:1.2em;font-size:.8rem;color:#B3563F;font-weight:650;margin:4px 0 10px}',
      '#bloomAuthGate .btn{width:100%;border:0;border-radius:12px;padding:13px 14px;font-size:.92rem;',
      'font-weight:800;cursor:pointer;background:linear-gradient(145deg,#C9763C,#9C5327);color:#FFFDF9;',
      'font-family:inherit;box-shadow:0 10px 22px rgba(180,99,47,.24),inset 0 1px 0 rgba(255,255,255,.18);',
      'transition:transform .18s cubic-bezier(.22,1,.36,1),box-shadow .18s,filter .18s}',
      '#bloomAuthGate .btn:hover{filter:brightness(1.05);transform:translateY(-1px);',
      'box-shadow:0 14px 28px rgba(180,99,47,.3)}',
      '#bloomAuthGate .btn:active{transform:translateY(0) scale(.99)}',
      '@media (prefers-reduced-motion:reduce){',
      '#bloomAuthGate .box{animation:none}',
      '#bloomAuthGate .petal{animation:none}',
      '#bloomAuthGate .role,#bloomAuthGate .r-go,#bloomAuthGate .btn,#bloomAuthGate input,',
      '#bloomAuthGate .manual-toggle{transition:none}}',
      '@media (max-width:420px){#bloomAuthGate{padding:14px}#bloomAuthGate .box{padding:26px 20px 24px}}',

      /* avatar button */
      '#bloomAuthUserbar{display:inline-flex;align-items:center;gap:10px}',
      '#bloomAuthAvatarBtn{width:40px;height:40px;border-radius:50%;border:2px solid #EDE4DD;padding:0;',
      'cursor:pointer;overflow:hidden;background:linear-gradient(145deg,#E06B4A,#7A5A74);',
      'box-shadow:0 4px 14px rgba(28,25,23,.12);transition:transform .15s,border-color .15s,box-shadow .15s;',
      'display:grid;place-items:center;position:relative}',
      '#bloomAuthAvatarBtn:hover{transform:translateY(-1px);border-color:#E06B4A;',
      'box-shadow:0 8px 20px rgba(224,107,74,.28)}',
      '#bloomAuthAvatarBtn img{width:100%;height:100%;object-fit:cover;display:block}',
      '#bloomAuthAvatarBtn .ini{color:#fff;font-weight:800;font-size:.85rem;letter-spacing:.02em;',
      'font-family:Inter,system-ui,sans-serif}',

      /* profile modal */
      '#bloomProfileScrim{position:fixed;inset:0;z-index:200;background:rgba(28,25,23,.52);',
      'opacity:0;pointer-events:none;transition:opacity .25s;backdrop-filter:blur(2px)}',
      '#bloomProfileScrim.show{opacity:1;pointer-events:auto}',
      '#bloomProfileModal{position:fixed;left:50%;top:50%;z-index:210;width:min(440px,calc(100vw - 32px));',
      'max-height:calc(100vh - 48px);background:#fff;border:1px solid #EDE4DD;border-radius:16px;',
      'box-shadow:0 28px 80px rgba(28,25,23,.28);transform:translate(-50%,-46%) scale(.96);',
      'opacity:0;pointer-events:none;transition:opacity .25s,transform .3s;display:flex;flex-direction:column;',
      'overflow:hidden;font-family:Inter,system-ui,sans-serif}',
      '#bloomProfileModal.show{opacity:1;pointer-events:auto;transform:translate(-50%,-50%) scale(1)}',
      '#bloomProfileModal .ph{padding:18px 20px;border-bottom:1px solid #EDE4DD;display:flex;',
      'align-items:center;justify-content:space-between;gap:12px}',
      '#bloomProfileModal .ph h3{margin:0;font-size:1.05rem;font-weight:900;letter-spacing:-.02em;color:#1C1917}',
      '#bloomProfileModal .ph .x{border:0;background:transparent;cursor:pointer;font-size:1.1rem;color:#A8A29E;',
      'padding:4px 8px;border-radius:8px;font-family:inherit}',
      '#bloomProfileModal .ph .x:hover{background:#F3EEEA;color:#1C1917}',
      '#bloomProfileModal .pb{padding:20px;overflow-y:auto}',
      '#bloomProfileModal .hero{display:flex;align-items:center;gap:14px;margin-bottom:18px}',
      '#bloomProfileModal .hero .big{width:72px;height:72px;border-radius:50%;overflow:hidden;',
      'background:linear-gradient(145deg,#E06B4A,#7A5A74);display:grid;place-items:center;',
      'border:3px solid #FCEBE5;flex-shrink:0;position:relative}',
      '#bloomProfileModal .hero .big img{width:100%;height:100%;object-fit:cover}',
      '#bloomProfileModal .hero .big .ini{color:#fff;font-weight:900;font-size:1.2rem}',
      '#bloomProfileModal .hero .meta .nm{font-size:1.05rem;font-weight:900;color:#1C1917;letter-spacing:-.02em}',
      '#bloomProfileModal .hero .meta .rl{font-size:.82rem;color:#78716C;margin-top:2px}',
      '#bloomProfileModal .hero .chg{margin-top:8px;font-size:.78rem;font-weight:750;color:#E06B4A;',
      'background:none;border:0;cursor:pointer;padding:0;font-family:inherit}',
      '#bloomProfileModal .hero .chg:hover{text-decoration:underline}',
      '#bloomProfileModal .field{margin-bottom:12px}',
      '#bloomProfileModal .field label{display:block;font-size:.68rem;font-weight:750;text-transform:uppercase;',
      'letter-spacing:.04em;color:#A8A29E;margin-bottom:6px}',
      '#bloomProfileModal .field input,#bloomProfileModal .field select{width:100%;box-sizing:border-box;',
      'border:1px solid #E0D5CC;border-radius:10px;padding:10px 12px;font-size:.9rem;outline:none;',
      'background:#FBF7F4;color:#1C1917;font-family:inherit}',
      '#bloomProfileModal .field input:focus,#bloomProfileModal .field select:focus{border-color:#E06B4A;',
      'box-shadow:0 0 0 3px #FCEBE5}',
      '#bloomProfileModal .row2{display:grid;grid-template-columns:1fr 1fr;gap:10px}',
      '#bloomProfileModal .tog{display:flex;align-items:center;justify-content:space-between;gap:12px;',
      'padding:12px;background:#FBF7F4;border:1px solid #EDE4DD;border-radius:12px;margin-bottom:12px}',
      '#bloomProfileModal .tog .t{font-size:.88rem;font-weight:750;color:#1C1917}',
      '#bloomProfileModal .tog .d{font-size:.76rem;color:#78716C;margin-top:2px}',
      '#bloomProfileModal .sw{width:42px;height:24px;border-radius:999px;background:#E0D5CC;position:relative;',
      'cursor:pointer;flex-shrink:0;border:0;padding:0}',
      '#bloomProfileModal .sw.on{background:#6F8F72}',
      '#bloomProfileModal .sw::after{content:\"\";position:absolute;top:3px;left:3px;width:18px;height:18px;',
      'border-radius:50%;background:#fff;transition:left .15s;box-shadow:0 1px 3px rgba(0,0,0,.15)}',
      '#bloomProfileModal .sw.on::after{left:21px}',
      '#bloomProfileModal .pf{padding:14px 20px;border-top:1px solid #EDE4DD;display:flex;flex-wrap:wrap;',
      'gap:8px;justify-content:space-between}',
      '#bloomProfileModal .pf .left,#bloomProfileModal .pf .right{display:flex;gap:8px;flex-wrap:wrap}',
      '#bloomProfileModal .btn{border:1px solid #E0D5CC;background:#fff;border-radius:10px;padding:10px 14px;',
      'font-size:.86rem;font-weight:750;cursor:pointer;font-family:inherit;color:#44403C}',
      '#bloomProfileModal .btn:hover{border-color:#E06B4A;color:#E06B4A}',
      '#bloomProfileModal .btn.terra{background:#E06B4A;border-color:#E06B4A;color:#fff}',
      '#bloomProfileModal .btn.terra:hover{background:#C85A3C;color:#fff}',
      '#bloomProfileModal .btn.ghost{border-color:transparent;background:transparent;color:#78716C}',
      '#bloomProfileModal .hint{font-size:.76rem;color:#A8A29E;margin-top:4px;line-height:1.4}',
      '@media (max-width:520px){#bloomProfileModal .row2{grid-template-columns:1fr}}'
    ].join('');
    document.head.appendChild(css);
  }

  function ensureProfileUi() {
    if (document.getElementById('bloomProfileModal')) return;
    var scrim = document.createElement('div');
    scrim.id = 'bloomProfileScrim';
    var modal = document.createElement('div');
    modal.id = 'bloomProfileModal';
    modal.innerHTML =
      '<div class="ph"><h3>Профиль</h3><button type="button" class="x" id="bloomProfileClose" aria-label="Закрыть">✕</button></div>' +
      '<div class="pb">' +
        '<div class="hero">' +
          '<div class="big" id="bloomProfileBigAv"><span class="ini">AK</span></div>' +
          '<div class="meta">' +
            '<div class="nm" id="bloomProfileHeroName">—</div>' +
            '<div class="rl" id="bloomProfileHeroRole">—</div>' +
            '<button type="button" class="chg" id="bloomProfilePickPhoto">Сменить фото</button>' +
            '<input type="file" id="bloomProfileFile" accept="image/*" style="display:none" />' +
          '</div>' +
        '</div>' +
        '<div class="field"><label for="pfName">Имя</label><input id="pfName" type="text" autocomplete="name" /></div>' +
        '<div class="row2">' +
          '<div class="field"><label for="pfRole">Роль</label>' +
            '<select id="pfRole">' +
              '<option>Владелец сети</option>' +
              '<option>Директор</option>' +
              '<option>Менеджер портала</option>' +
              '<option>Менеджер магазина</option>' +
              '<option>Флорист</option>' +
            '</select></div>' +
          '<div class="field"><label for="pfShop">Точка</label>' +
            '<select id="pfShop">' +
              '<option>Вся сеть</option>' +
              '<option>Мира 14</option>' +
              '<option>Ленина 92</option>' +
              '<option>Рижская 8</option>' +
            '</select></div>' +
        '</div>' +
        '<div class="field"><label for="pfEmail">Email</label><input id="pfEmail" type="email" autocomplete="email" /></div>' +
        '<div class="field"><label for="pfPhone">Телефон</label><input id="pfPhone" type="tel" autocomplete="tel" /></div>' +
        '<div class="field"><label for="pfLogin">Логин</label><input id="pfLogin" type="text" disabled /></div>' +
        '<div class="tog"><div><div class="t">Уведомления в кабинете</div><div class="d">Новые заказы и чаты</div></div>' +
          '<button type="button" class="sw on" id="pfNotify" aria-label="Уведомления"></button></div>' +
        '<div class="field"><label for="pfPass">Новый пароль</label><input id="pfPass" type="password" placeholder="Оставьте пустым, если не меняете" autocomplete="new-password" />' +
          '<div class="hint">В демо пароль не сохраняется на сервере — только в сессии браузера.</div></div>' +
      '</div>' +
      '<div class="pf">' +
        '<div class="left">' +
          '<button type="button" class="btn ghost" id="bloomProfileLogout">Выйти</button>' +
          '<a class="btn" id="bloomProfileAdmin" href="admin-access.html" style="text-decoration:none;display:inline-flex;align-items:center">Права доступа</a>' +
        '</div>' +
        '<div class="right">' +
          '<button type="button" class="btn" id="bloomProfileCancel">Отмена</button>' +
          '<button type="button" class="btn terra" id="bloomProfileSave">Сохранить</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(scrim);
    document.body.appendChild(modal);

    scrim.addEventListener('click', closeProfile);
    document.getElementById('bloomProfileClose').addEventListener('click', closeProfile);
    document.getElementById('bloomProfileCancel').addEventListener('click', closeProfile);
    document.getElementById('bloomProfileLogout').addEventListener('click', function () {
      logout();
      location.reload();
    });
    document.getElementById('bloomProfileSave').addEventListener('click', function () {
      var p = {
        displayName: document.getElementById('pfName').value.trim() || 'Анна К.',
        role: document.getElementById('pfRole').value,
        shop: document.getElementById('pfShop').value,
        email: document.getElementById('pfEmail').value.trim(),
        phone: document.getElementById('pfPhone').value.trim(),
        notify: document.getElementById('pfNotify').classList.contains('on')
      };
      writeProfile(p);
      refreshAvatarUi();
      closeProfile();
      document.dispatchEvent(new CustomEvent('bloom:profile', { detail: readProfile() }));
      if (global.toast) global.toast('Профиль сохранён');
      else {
        // soft toast via custom event
        try {
          var t = document.getElementById('toast');
          if (t) {
            t.textContent = 'Профиль сохранён';
            t.classList.add('show');
            setTimeout(function () { t.classList.remove('show'); }, 2000);
          }
        } catch (_) {}
      }
    });
    document.getElementById('pfNotify').addEventListener('click', function () {
      this.classList.toggle('on');
    });
    document.getElementById('bloomProfilePickPhoto').addEventListener('click', function () {
      document.getElementById('bloomProfileFile').click();
    });
    document.getElementById('bloomProfileFile').addEventListener('change', function (e) {
      var f = e.target.files && e.target.files[0];
      if (!f) return;
      if (f.size > 2 * 1024 * 1024) {
        alert('Файл слишком большой (макс. 2 МБ)');
        return;
      }
      var reader = new FileReader();
      reader.onload = function () {
        writeProfile({ avatarDataUrl: reader.result });
        fillProfileForm();
        refreshAvatarUi();
      };
      reader.readAsDataURL(f);
    });
  }

  function setAvatarEl(el, profile, sizeClass) {
    if (!el) return;
    var name = (profile && profile.displayName) || 'A';
    var ini = initials(name);
    if (profile && profile.avatarDataUrl) {
      el.innerHTML = '<img src="' + profile.avatarDataUrl + '" alt="" />';
    } else {
      el.innerHTML = '<span class="ini">' + ini + '</span>';
    }
  }

  function fillProfileForm() {
    var p = readProfile();
    document.getElementById('pfName').value = p.displayName || '';
    document.getElementById('pfRole').value = p.role || 'Владелец сети';
    document.getElementById('pfShop').value = p.shop || 'Вся сеть';
    document.getElementById('pfEmail').value = p.email || '';
    document.getElementById('pfPhone').value = p.phone || '';
    document.getElementById('pfLogin').value = p.login || currentUser() || 'admin';
    document.getElementById('pfPass').value = '';
    document.getElementById('pfNotify').classList.toggle('on', p.notify !== false);
    document.getElementById('bloomProfileHeroName').textContent = p.displayName || '—';
    document.getElementById('bloomProfileHeroRole').textContent = p.role || '—';
    setAvatarEl(document.getElementById('bloomProfileBigAv'), p);
  }

  function openProfile() {
    ensureStyles();
    ensureProfileUi();
    fillProfileForm();
    document.getElementById('bloomProfileScrim').classList.add('show');
    document.getElementById('bloomProfileModal').classList.add('show');
    document.body.style.overflow = 'hidden';
  }

  function closeProfile() {
    var s = document.getElementById('bloomProfileScrim');
    var m = document.getElementById('bloomProfileModal');
    if (s) s.classList.remove('show');
    if (m) m.classList.remove('show');
    // don't unlock if auth gate open
    if (!document.getElementById('bloomAuthGate') || document.getElementById('bloomAuthGate').classList.contains('hidden')) {
      if (!document.querySelector('.modal.show') && !document.querySelector('.order-drawer.show')) {
        document.body.style.overflow = '';
      }
    }
  }

  function refreshAvatarUi() {
    var btn = document.getElementById('bloomAuthAvatarBtn');
    if (!btn) return;
    setAvatarEl(btn, readProfile());
  }

  function mountGate(opts) {
    opts = opts || {};
    ensureStyles();
    var existing = document.getElementById('bloomAuthGate');
    if (existing) existing.remove();

    var gate = document.createElement('div');
    gate.id = 'bloomAuthGate';
    gate.innerHTML =
      '<i class="petal p1" aria-hidden="true"></i>' +
      '<i class="petal p2" aria-hidden="true"></i>' +
      '<div class="box">' +
        '<div class="head">' +
          '<div class="kicker">Демо-кабинет · Bloom CRM</div>' +
          '<div class="mark">B</div>' +
          '<h1>' + (opts.title || 'Bloom CRM') + '</h1>' +
          '<p class="sub">' + (opts.subtitle || 'Вход для менеджера и флориста сети цветочных салонов') + '</p>' +
        '</div>' +
        '<div class="roles">' +
          '<button type="button" class="role" data-user="admin">' +
            '<span class="r-ico">АК</span>' +
            '<span class="r-txt"><b>Кабинет менеджера</b><span class="r-sub">Анна К. · владелец сети · все магазины и заказы</span></span>' +
            '<span class="r-go">→</span>' +
          '</button>' +
          '<button type="button" class="role" data-user="florist">' +
            '<span class="r-ico sp">СП</span>' +
            '<span class="r-txt"><b>Кабинет флориста</b><span class="r-sub">Светлана П. · свой магазин · сборка и фото</span></span>' +
            '<span class="r-go">→</span>' +
          '</button>' +
        '</div>' +
        '<button type="button" class="manual-toggle" id="bloomManualToggle">Войти по логину</button>' +
        '<form id="bloomAuthForm" autocomplete="on" hidden>' +
          '<div class="field"><label for="bloomAuthUser">Логин</label>' +
          '<input id="bloomAuthUser" name="username" type="text" autocomplete="username" placeholder="admin" required></div>' +
          '<div class="field"><label for="bloomAuthPass">Пароль</label>' +
          '<input id="bloomAuthPass" name="password" type="password" autocomplete="current-password" placeholder="••••" required></div>' +
          '<div class="err" id="bloomAuthErr"></div>' +
          '<button type="submit" class="btn">Войти</button>' +
        '</form>' +
      '</div>';
    document.body.appendChild(gate);

    function enterUser(user) {
      var u = USERS[user];
      if (!u) return;
      login(user, u.pass);
      hideGate();
      if (typeof opts.onLogin === 'function') opts.onLogin(readSession());
      document.dispatchEvent(new CustomEvent('bloom:auth', { detail: readSession() }));
    }

    gate.querySelectorAll('.role').forEach(function (b) {
      b.addEventListener('click', function () { enterUser(b.getAttribute('data-user')); });
    });

    var toggle = document.getElementById('bloomManualToggle');
    var form = document.getElementById('bloomAuthForm');
    var err = document.getElementById('bloomAuthErr');
    var userInp = document.getElementById('bloomAuthUser');
    var passInp = document.getElementById('bloomAuthPass');

    toggle.addEventListener('click', function () {
      var hidden = form.hidden;
      form.hidden = !hidden;
      toggle.textContent = hidden ? 'Скрыть форму' : 'Войти по логину';
      if (hidden) {
        userInp.value = DEMO_USER;
        setTimeout(function () { passInp.focus(); }, 60);
      }
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var res = login(userInp.value, passInp.value);
      if (!res.ok) {
        err.textContent = res.error || 'Ошибка входа';
        passInp.focus();
        passInp.select();
        return;
      }
      err.textContent = '';
      hideGate();
      if (typeof opts.onLogin === 'function') opts.onLogin(readSession());
      document.dispatchEvent(new CustomEvent('bloom:auth', { detail: readSession() }));
    });
  }

  function hideGate() {
    var gate = document.getElementById('bloomAuthGate');
    if (gate) gate.classList.add('hidden');
    document.body.style.overflow = '';
  }

  function showGate(opts) {
    document.body.style.overflow = 'hidden';
    mountGate(opts);
  }

  function requireAuth(opts) {
    opts = opts || {};
    if (isAuthed()) {
      hideGate();
      mountUserbar(opts.userbarParent);
      if (typeof opts.onReady === 'function') opts.onReady(readSession());
      return true;
    }
    showGate({
      title: opts.title,
      subtitle: opts.subtitle,
      onLogin: function (s) {
        mountUserbar(opts.userbarParent);
        if (typeof opts.onReady === 'function') opts.onReady(s);
      }
    });
    return false;
  }

  function mountUserbar(parent) {
    ensureStyles();
    ensureProfileUi();
    var host = parent
      ? (typeof parent === 'string' ? document.querySelector(parent) : parent)
      : document.querySelector('.tb-chips') || document.querySelector('.tb-right') || document.querySelector('.topbar');
    if (!host) return;

    var old = document.getElementById('bloomAuthUserbar');
    if (old) old.remove();

    var bar = document.createElement('span');
    bar.id = 'bloomAuthUserbar';
    bar.innerHTML =
      '<button type="button" id="bloomAuthAvatarBtn" title="Профиль и настройки" aria-label="Профиль">' +
        '<span class="ini">A</span>' +
      '</button>';
    host.appendChild(bar);
    refreshAvatarUi();
    document.getElementById('bloomAuthAvatarBtn').addEventListener('click', openProfile);
  }

  global.BloomAuth = {
    STORAGE_KEY: STORAGE_KEY,
    DEMO_USER: DEMO_USER,
    isAuthed: isAuthed,
    currentUser: currentUser,
    login: login,
    logout: logout,
    requireAuth: requireAuth,
    showGate: showGate,
    hideGate: hideGate,
    mountUserbar: mountUserbar,
    session: readSession,
    profile: readProfile,
    openProfile: openProfile,
    closeProfile: closeProfile
  };
})(typeof window !== 'undefined' ? window : this);
