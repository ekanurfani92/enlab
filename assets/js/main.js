/* ENLab - logika situs: tema, bahasa, navigasi, animasi, dan perender data. */
(function () {
  'use strict';

  var LS_LANG = 'enlab-lang';
  var LS_THEME = 'enlab-theme';
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) { /* mode privat */ } }
  };

  /* ---------- Bahasa ---------- */
  var lang = (function () {
    var q = new URLSearchParams(location.search).get('lang');
    if (q === 'id' || q === 'en') return q;
    var saved = store.get(LS_LANG);
    if (saved === 'id' || saved === 'en') return saved;
    return (navigator.language || 'id').toLowerCase().indexOf('id') === 0 ? 'id' : 'en';
  })();

  function t(key) {
    var dict = (window.I18N && window.I18N[lang]) || {};
    return Object.prototype.hasOwnProperty.call(dict, key) ? dict[key] : key;
  }

  function applyLang() {
    document.documentElement.lang = lang;

    document.querySelectorAll('[data-i18n]').forEach(function (el) {
      var key = el.getAttribute('data-i18n');
      var attr = el.getAttribute('data-i18n-attr');
      if (attr) {
        el.setAttribute(attr, t(key));
      } else if (el.hasAttribute('data-i18n-html')) {
        // Hanya untuk nilai dari kamus kita sendiri (mis. penegasan akronim EN).
        el.innerHTML = t(key);
      } else {
        el.textContent = t(key);
      }
    });

    document.querySelectorAll('[data-lang-btn]').forEach(function (btn) {
      btn.setAttribute('aria-pressed', String(btn.getAttribute('data-lang-btn') === lang));
    });

    // Tautan bahasa-sadar untuk atribut hreflang alternatif
    var alt = document.querySelector('link[rel="alternate"][data-dynamic]');
    if (alt) alt.setAttribute('hreflang', lang === 'id' ? 'en' : 'id');

    document.dispatchEvent(new CustomEvent('langchange', { detail: { lang: lang } }));
  }

  function setLang(next) {
    if (next === lang) return;
    lang = next;
    store.set(LS_LANG, next);
    applyLang();
  }

  /* ---------- Tema ---------- */
  function currentTheme() {
    var explicit = document.documentElement.getAttribute('data-theme');
    if (explicit) return explicit;
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function toggleTheme() {
    var next = currentTheme() === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    store.set(LS_THEME, next);
  }

  /* ---------- Utilitas ---------- */
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function scholarURL(title) {
    return 'https://scholar.google.com/scholar?q=' + encodeURIComponent('"' + title + '"');
  }

  /* ---------- Navigasi ---------- */
  function initNav() {
    var toggle = document.querySelector('.menu-toggle');
    var nav = document.querySelector('.site-nav');
    var header = document.querySelector('.site-header');
    if (!nav) return;

    function close() {
      nav.classList.remove('is-open');
      if (toggle) toggle.setAttribute('aria-expanded', 'false');
    }

    if (toggle) {
      toggle.addEventListener('click', function () {
        var open = nav.classList.toggle('is-open');
        toggle.setAttribute('aria-expanded', String(open));
      });
    }

    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) close();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') close();
    });

    if (header) {
      var onScroll = function () {
        header.classList.toggle('is-stuck', window.scrollY > 8);
      };
      addEventListener('scroll', onScroll, { passive: true });
      onScroll();
    }

    // Sorot bagian yang sedang dibaca (khusus halaman beranda)
    var links = Array.prototype.slice.call(nav.querySelectorAll('a[href^="#"]'));
    if (!links.length || !('IntersectionObserver' in window)) return;
    var map = {};
    links.forEach(function (a) {
      var s = document.querySelector(a.getAttribute('href'));
      if (s) map[s.id] = a;
    });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) { a.classList.remove('is-active'); });
        if (map[en.target.id]) map[en.target.id].classList.add('is-active');
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    Object.keys(map).forEach(function (id) { spy.observe(document.getElementById(id)); });
  }

  /* ---------- Animasi masuk ---------- */
  function initReveal() {
    var nodes = document.querySelectorAll('.reveal');
    if (!nodes.length) return;
    if (!('IntersectionObserver' in window) ||
        matchMedia('(prefers-reduced-motion: reduce)').matches) {
      nodes.forEach(function (n) { n.classList.add('is-visible'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        en.target.classList.add('is-visible');
        io.unobserve(en.target);
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    nodes.forEach(function (n) { io.observe(n); });
  }

  /* ---------- Perender: publikasi ---------- */
  function pubNode(p) {
    var li = el('li', 'pub');
    li.appendChild(el('div', 'pub-year', String(p.y)));

    var body = el('div');
    var kindKey = 'pub.filter.' + p.k;
    var chip = el('span', 'chip chip-neutral', t(kindKey));
    chip.setAttribute('data-i18n', kindKey);
    body.appendChild(chip);

    var h = el('h3');
    var a = el('a', null, p.t);
    a.href = scholarURL(p.t);
    a.target = '_blank';
    a.rel = 'noopener';
    h.appendChild(a);
    body.appendChild(h);

    var venue = el('p', 'pub-venue');
    venue.appendChild(el('em', null, p.v));
    if (p.d) venue.appendChild(document.createTextNode(' - ' + p.d));
    body.appendChild(venue);
    li.appendChild(body);

    var go = el('a', 'pub-go', '↗');
    go.href = scholarURL(p.t);
    go.target = '_blank';
    go.rel = 'noopener';
    go.setAttribute('data-i18n', 'pub.open');
    go.setAttribute('data-i18n-attr', 'aria-label');
    go.setAttribute('aria-label', t('pub.open'));
    li.appendChild(go);
    return li;
  }

  function initPublications() {
    var list = document.getElementById('pub-list');
    if (!list || !window.PUBLICATIONS) return;

    var all = window.PUBLICATIONS;
    var search = document.getElementById('pub-search');
    var yearSel = document.getElementById('pub-year');
    var pills = document.querySelectorAll('[data-kind]');
    var countEl = document.getElementById('pub-count');
    var state = { q: '', kind: 'all', year: 'all' };

    // Isi pilihan tahun
    if (yearSel) {
      var years = Array.from(new Set(all.map(function (p) { return p.y; })))
        .sort(function (a, b) { return b - a; });
      var optAll = el('option', null, t('pub.year.all'));
      optAll.value = 'all';
      optAll.setAttribute('data-i18n', 'pub.year.all');
      yearSel.appendChild(optAll);
      years.forEach(function (y) {
        var o = el('option', null, String(y));
        o.value = String(y);
        yearSel.appendChild(o);
      });
    }

    function render() {
      var q = state.q.trim().toLowerCase();
      var rows = all.filter(function (p) {
        if (state.kind !== 'all' && p.k !== state.kind) return false;
        if (state.year !== 'all' && String(p.y) !== state.year) return false;
        if (q && (p.t + ' ' + p.v).toLowerCase().indexOf(q) < 0) return false;
        return true;
      });

      list.textContent = '';
      if (!rows.length) {
        var empty = el('div', 'empty-state');
        var msg = el('p', null, t('pub.empty'));
        msg.setAttribute('data-i18n', 'pub.empty');
        empty.appendChild(msg);
        var reset = el('button', 'btn btn-ghost btn-sm', t('pub.reset'));
        reset.type = 'button';
        reset.style.marginTop = '16px';
        reset.addEventListener('click', function () {
          state.q = ''; state.kind = 'all'; state.year = 'all';
          if (search) search.value = '';
          if (yearSel) yearSel.value = 'all';
          pills.forEach(function (o) {
            o.setAttribute('aria-pressed', String(o.getAttribute('data-kind') === 'all'));
          });
          render();
        });
        empty.appendChild(reset);
        list.appendChild(empty);
      } else {
        var frag = document.createDocumentFragment();
        rows.forEach(function (p) { frag.appendChild(pubNode(p)); });
        list.appendChild(frag);
      }

      if (countEl) {
        countEl.textContent = t('pub.count')
          .replace('{n}', String(rows.length))
          .replace('{total}', String(all.length));
      }
    }

    if (search) {
      search.addEventListener('input', function () { state.q = search.value; render(); });
    }
    if (yearSel) {
      yearSel.addEventListener('change', function () { state.year = yearSel.value; render(); });
    }
    pills.forEach(function (b) {
      b.addEventListener('click', function () {
        state.kind = b.getAttribute('data-kind');
        pills.forEach(function (o) {
          o.setAttribute('aria-pressed', String(o === b));
        });
        render();
      });
    });

    document.addEventListener('langchange', render);
    render();
  }

  /* ---------- Perender: publikasi terbaru (beranda) ---------- */
  function initLatestPublications() {
    var host = document.getElementById('pub-latest');
    if (!host || !window.PUBLICATIONS) return;
    function render() {
      host.textContent = '';
      var frag = document.createDocumentFragment();
      window.PUBLICATIONS.slice(0, 5).forEach(function (p) { frag.appendChild(pubNode(p)); });
      host.appendChild(frag);
    }
    document.addEventListener('langchange', render);
    render();
  }

  /* ---------- Perender: hibah penelitian ---------- */
  function initGrants() {
    var host = document.getElementById('grant-list');
    if (!host || !window.GRANTS) return;

    function render() {
      host.textContent = '';
      var frag = document.createDocumentFragment();
      window.GRANTS.forEach(function (g) {
        var li = el('li', 'pub');
        li.appendChild(el('div', 'pub-year', String(g.y)));
        var body = el('div');
        var role = el('span', 'chip ' + (g.r === 'pi' ? '' : 'chip-neutral'),
                      t(g.r === 'pi' ? 'grant.pi' : 'grant.member'));
        body.appendChild(role);
        body.appendChild(el('h3', null, g.t[lang]));
        body.appendChild(el('p', 'pub-venue', g.f[lang]));
        li.appendChild(body);
        frag.appendChild(li);
      });
      host.appendChild(frag);
    }

    document.addEventListener('langchange', render);
    render();
  }

  /* ---------- Perender: mata kuliah ---------- */
  function courseNode(c) {
    var d = el('details', 'course reveal');

    var sum = el('summary');
    var title = el('div', 'course-title');
    title.appendChild(el('h3', null, c.t[lang]));

    var meta = el('div', 'course-meta');
    if (c.sks) meta.appendChild(el('span', 'chip chip-neutral', c.sks + ' ' + t('teach.sks')));
    meta.appendChild(el('span', 'chip chip-neutral', c.prodiName[lang]));
    if (c.m.length && window.MATERI_TERSEDIA) {
      meta.appendChild(el('span', 'chip', c.m.length + ' ' + t('teach.materials')));
    }
    title.appendChild(meta);
    sum.appendChild(title);

    var caret = el('span', 'course-caret');
    caret.setAttribute('aria-hidden', 'true');
    caret.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" ' +
      'stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">' +
      '<path d="M6 9l6 6 6-6"/></svg>';
    sum.appendChild(caret);
    d.appendChild(sum);

    var body = el('div', 'course-body');
    body.appendChild(el('p', null, c.d[lang]));
    if (c.note) body.appendChild(el('p', 'course-note', c.note[lang]));

    if (c.m.length && window.MATERI_TERSEDIA) {
      var ul = el('ul', 'material-list');
      c.m.forEach(function (m) {
        var li = el('li');
        var a = el('a', 'material');
        // Nama berkas boleh memuat spasi atau huruf beraksen;
        // tiap ruas jalur disandikan agar tautannya tetap sah.
        a.href = m.f.split('/').map(encodeURIComponent).join('/');
        a.target = '_blank';
        a.rel = 'noopener';
        a.setAttribute('aria-label', t('teach.download') + ': ' + m.t);
        a.appendChild(el('span', 'pdf-ico', 'PDF'));
        var wrap = el('div');
        wrap.appendChild(el('b', null, m.t));
        a.appendChild(wrap);
        a.appendChild(el('small', null, m.s + ' MB'));
        li.appendChild(a);
        ul.appendChild(li);
      });
      body.appendChild(ul);
    } else {
      body.appendChild(el('p', 'no-material', t('teach.nomaterial')));
    }

    d.appendChild(body);
    return d;
  }

  function initCourses() {
    var mt = document.getElementById('courses-mt');
    var other = document.getElementById('courses-other');
    if (!mt || !window.COURSES) return;

    function render() {
      mt.textContent = '';
      if (other) other.textContent = '';
      window.COURSES.forEach(function (c) {
        var host = c.prodi === 'MT' ? mt : other;
        if (host) host.appendChild(courseNode(c));
      });

      var countEl = document.getElementById('course-count');
      if (countEl) {
        var files = window.COURSES.reduce(function (n, c) { return n + c.m.length; }, 0);
        countEl.textContent = window.MATERI_TERSEDIA
          ? t('teach.count').replace('{n}', String(window.COURSES.length))
                            .replace('{m}', String(files))
          : t('teach.count.soon').replace('{n}', String(window.COURSES.length));
      }
      initReveal();
    }

    document.addEventListener('langchange', render);
    render();
  }

  /* ---------- Bootstrap ---------- */
  function init() {
    applyLang();
    initNav();
    initReveal();
    initPublications();
    initLatestPublications();
    initGrants();
    initCourses();

    document.querySelectorAll('[data-lang-btn]').forEach(function (b) {
      b.addEventListener('click', function () { setLang(b.getAttribute('data-lang-btn')); });
    });

    var themeBtn = document.querySelector('.theme-toggle');
    if (themeBtn) themeBtn.addEventListener('click', toggleTheme);

    document.querySelectorAll('[data-year]').forEach(function (n) {
      n.textContent = String(new Date().getFullYear());
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
