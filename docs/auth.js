/**
 * Bloom CRM · demo auth gate
 * Test credentials: admin / admin
 * Session: localStorage bloom_demo_auth_v1
 */
(function (global) {
  'use strict';

  var STORAGE_KEY = 'bloom_demo_auth_v1';
  var DEMO_USER = 'admin';
  var DEMO_PASS = 'admin';

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

  function isAuthed() {
    return !!readSession();
  }

  function currentUser() {
    var s = readSession();
    return s ? s.user : null;
  }

  function login(user, pass) {
    user = String(user || '').trim();
    pass = String(pass || '');
    if (user === DEMO_USER && pass === DEMO_PASS) {
      writeSession(user);
      return { ok: true };
    }
    return { ok: false, error: 'Неверный логин или пароль' };
  }

  function logout() {
    clearSession();
  }

  function ensureStyles() {
    if (document.getElementById('bloom-auth-styles')) return;
    var css = document.createElement('style');
    css.id = 'bloom-auth-styles';
    css.textContent = [
      '#bloomAuthGate{position:fixed;inset:0;z-index:99999;display:flex;align-items:center;justify-content:center;',
      'background:radial-gradient(900px 480px at 12% -10%,rgba(224,107,74,.14),transparent 55%),',
      'radial-gradient(700px 420px at 100% 0%,rgba(111,143,114,.10),transparent 50%),#FBF7F4;',
      'font-family:Inter,system-ui,-apple-system,sans-serif;padding:20px}',
      '#bloomAuthGate.hidden{display:none}',
      '#bloomAuthGate .box{width:100%;max-width:400px;background:#fff;border:1px solid #EDE4DD;',
      'border-radius:16px;padding:28px 26px 24px;box-shadow:0 12px 40px rgba(28,25,23,.08)}',
      '#bloomAuthGate .mark{width:42px;height:42px;border-radius:12px;display:grid;place-items:center;',
      'background:linear-gradient(145deg,#E06B4A,#7A5A74);color:#fff;font-weight:900;font-size:1rem;margin-bottom:14px}',
      '#bloomAuthGate h1{font-size:1.2rem;font-weight:900;letter-spacing:-.03em;margin:0 0 6px;color:#1C1917}',
      '#bloomAuthGate .sub{font-size:.86rem;color:#78716C;margin:0 0 18px;line-height:1.45}',
      '#bloomAuthGate label{display:block;font-size:.68rem;font-weight:750;text-transform:uppercase;',
      'letter-spacing:.05em;color:#A8A29E;margin:0 0 6px}',
      '#bloomAuthGate .field{margin-bottom:12px}',
      '#bloomAuthGate input{width:100%;box-sizing:border-box;border:1px solid #E0D5CC;border-radius:10px;',
      'padding:11px 12px;font-size:.92rem;outline:none;background:#FBF7F4;color:#1C1917;font-family:inherit}',
      '#bloomAuthGate input:focus{border-color:#E06B4A;box-shadow:0 0 0 3px #FCEBE5}',
      '#bloomAuthGate .err{min-height:1.2em;font-size:.8rem;color:#D6493A;font-weight:650;margin:4px 0 10px}',
      '#bloomAuthGate .btn{width:100%;border:0;border-radius:10px;padding:12px 14px;font-size:.92rem;',
      'font-weight:800;cursor:pointer;background:#E06B4A;color:#fff;font-family:inherit}',
      '#bloomAuthGate .btn:hover{background:#C85A3C}',
      '#bloomAuthGate .hint{margin-top:14px;font-size:.78rem;color:#A8A29E;line-height:1.4;',
      'background:#F3EEEA;border-radius:10px;padding:10px 12px}',
      '#bloomAuthGate .hint b{color:#44403C;font-family:ui-monospace,monospace}',
      '#bloomAuthUserbar{display:inline-flex;align-items:center;gap:8px;font-size:.72rem;font-weight:700;',
      'color:#78716C}',
      '#bloomAuthUserbar button{border:1px solid #E0D5CC;background:#fff;border-radius:8px;',
      'padding:4px 10px;font-size:.72rem;font-weight:750;cursor:pointer;font-family:inherit;color:#44403C}',
      '#bloomAuthUserbar button:hover{border-color:#E06B4A;color:#E06B4A}'
    ].join('');
    document.head.appendChild(css);
  }

  function mountGate(opts) {
    opts = opts || {};
    ensureStyles();
    var existing = document.getElementById('bloomAuthGate');
    if (existing) existing.remove();

    var gate = document.createElement('div');
    gate.id = 'bloomAuthGate';
    gate.innerHTML =
      '<div class="box">' +
        '<div class="mark">B</div>' +
        '<h1>' + (opts.title || 'Вход в Bloom CRM') + '</h1>' +
        '<p class="sub">' + (opts.subtitle || 'Демо-доступ для теста прототипа') + '</p>' +
        '<form id="bloomAuthForm" autocomplete="on">' +
          '<div class="field"><label for="bloomAuthUser">Логин</label>' +
          '<input id="bloomAuthUser" name="username" type="text" autocomplete="username" placeholder="admin" required></div>' +
          '<div class="field"><label for="bloomAuthPass">Пароль</label>' +
          '<input id="bloomAuthPass" name="password" type="password" autocomplete="current-password" placeholder="••••" required></div>' +
          '<div class="err" id="bloomAuthErr"></div>' +
          '<button type="submit" class="btn">Войти</button>' +
        '</form>' +
        '<div class="hint">Тест: логин <b>admin</b> · пароль <b>admin</b></div>' +
      '</div>';
    document.body.appendChild(gate);

    var form = document.getElementById('bloomAuthForm');
    var err = document.getElementById('bloomAuthErr');
    var userInp = document.getElementById('bloomAuthUser');
    var passInp = document.getElementById('bloomAuthPass');
    if (userInp) userInp.value = DEMO_USER;

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

    setTimeout(function () {
      if (passInp) passInp.focus();
    }, 80);
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
    var host = parent
      ? (typeof parent === 'string' ? document.querySelector(parent) : parent)
      : document.querySelector('.tb-right') || document.querySelector('.topbar');
    if (!host) return;

    var old = document.getElementById('bloomAuthUserbar');
    if (old) old.remove();

    var bar = document.createElement('span');
    bar.id = 'bloomAuthUserbar';
    bar.innerHTML =
      '<span class="chip-like">👤 ' + (currentUser() || '—') + '</span>' +
      '<button type="button" id="bloomAuthLogout">Выйти</button>';
    host.appendChild(bar);
    var btn = document.getElementById('bloomAuthLogout');
    if (btn) {
      btn.addEventListener('click', function () {
        logout();
        location.reload();
      });
    }
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
    session: readSession
  };
})(typeof window !== 'undefined' ? window : this);
