/* Platinum Painting – homepage interactions & animations.
 * Recreates the motion from the supplied design (Home v2) on top of
 * editable Elementor widgets. Behaviour is attached via CSS classes set in
 * Elementor (Advanced > CSS Classes) and data-* attributes inside the
 * decorative HTML widgets. Nothing here creates content.
 */
(function () {
  'use strict';
  var d = document;
  function ready(fn) { if (d.readyState !== 'loading') fn(); else d.addEventListener('DOMContentLoaded', fn); }
  function $$(sel, root) { return Array.prototype.slice.call((root || d).querySelectorAll(sel)); }
  function isEditor() { return d.body.classList.contains('elementor-editor-active') || /elementor-preview=/.test(location.search); }

  ready(function () {
    var editor = isEditor();
    var motion = !editor && !window.matchMedia('(prefers-reduced-motion: reduce)').matches && !!d.body.animate;
    var anims = [];
    function loop(el, frames, opts) { if (motion && el.animate) anims.push(el.animate(frames, opts)); }

    /* ---------- split hero headline into words (each revealed in turn, as in the design) ---------- */
    if (!editor) $$('.pp-split .elementor-heading-title').forEach(function (h) {
      var t = h.textContent.trim();
      h.setAttribute('aria-label', t);
      h.innerHTML = t.split(/\s+/).map(function (w, i) { return '<span class="pp-hw pp-r-up pp-d' + Math.min(i, 9) + '" aria-hidden="true">' + w.replace(/</g, '&lt;') + '</span>'; }).join(' ');
    });

    /* ---------- reveal on scroll ---------- */
    var OFF = { up: 'translateY(44px)', left: 'translateX(-70px)', right: 'translateX(70px)', zoom: 'scale(0.86)',
      tl: 'translate(-60px,-60px) scale(0.9)', bl: 'translate(-60px,60px) scale(0.9)', br: 'translate(60px,60px) scale(0.9)', ring: 'scale(0)' };
    function kind(el) { var m = el.className.match(/\bpp-r-(up|left|right|zoom|tl|bl|br|ring)\b/); return m ? m[1] : 'up'; }
    function delay(el) { var m = el.className.match(/\bpp-d(\d)\b/); return m ? +m[1] : 0; }
    function play(el) {
      el.style.opacity = '';
      el.animate([{ opacity: 0, transform: OFF[kind(el)] }, { opacity: 1, transform: 'none' }],
        { duration: 950, delay: delay(el) * 90, easing: 'cubic-bezier(.2,.7,.2,1)', fill: 'backwards' });
    }
    var reveals = $$('[class*="pp-r-"]');
    if (motion && reveals.length && 'IntersectionObserver' in window) {
      var vh0 = window.innerHeight;
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); play(e.target); } });
      }, { threshold: 0.12 });
      reveals.forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.top < vh0 && r.bottom > 0) play(el); else { el.style.opacity = '0'; io.observe(el); }
      });
      var revealScroll = function () {
        var vh = window.innerHeight;
        reveals.forEach(function (el) {
          if (el.style.opacity === '0') { var r = el.getBoundingClientRect(); if (r.top < vh * 0.95 && r.bottom > 0) { io.unobserve(el); play(el); } }
        });
      };
      window.addEventListener('scroll', function () { requestAnimationFrame(revealScroll); }, { passive: true });
    }

    /* ---------- looping decorative motion ---------- */
    $$('.pp-float').forEach(function (el, i) {
      loop(el, [{ transform: 'translateY(0)' }, { transform: 'translateY(-14px)' }], { duration: 2800 + (i % 8) * 600, direction: 'alternate', iterations: Infinity, easing: 'ease-in-out' });
    });
    $$('.pp-badge-star').forEach(function (el, i) {
      loop(el, [{ transform: 'rotate(0)' }, { transform: 'rotate(360deg)' }], { duration: 16000 + i * 14000, iterations: Infinity });
    });
    $$('[data-twinkle]').forEach(function (el, i) {
      loop(el, [{ transform: 'scale(1) rotate(0)', opacity: 1 }, { transform: 'scale(0.6) rotate(45deg)', opacity: 0.4 }, { transform: 'scale(1) rotate(90deg)', opacity: 1 }], { duration: 2600, delay: i * 500, iterations: Infinity, easing: 'ease-in-out' });
    });
    $$('[data-pulse]').forEach(function (el) {
      loop(el, [{ transform: 'scale(1)', opacity: 0.45 }, { transform: 'scale(1.7)', opacity: 0 }], { duration: 2200, iterations: Infinity, easing: 'ease-out' });
    });
    $$('[data-draw]').forEach(function (el) {
      if (!motion) return; var L = el.getTotalLength(); el.style.strokeDasharray = L;
      loop(el, [{ strokeDashoffset: L }, { strokeDashoffset: 0 }, { strokeDashoffset: 0 }, { strokeDashoffset: -L }], { duration: 4200, iterations: Infinity, easing: 'ease-in-out' });
    });
    $$('[data-fan]').forEach(function (el) {
      var k = (+el.getAttribute('data-fan')) - 2;
      loop(el, [{ transform: 'rotate(' + (k * 9) + 'deg)' }, { transform: 'rotate(' + (k * 17) + 'deg)' }], { duration: 2600, direction: 'alternate', iterations: Infinity, easing: 'ease-in-out' });
    });
    $$('[data-rays]').forEach(function (el) { loop(el, [{ transform: 'rotate(0)' }, { transform: 'rotate(360deg)' }], { duration: 24000, iterations: Infinity }); });
    $$('[data-heat]').forEach(function (el, i) { loop(el, [{ transform: 'translateY(0)', opacity: 0 }, { opacity: 0.8, offset: 0.4 }, { transform: 'translateY(-26px)', opacity: 0 }], { duration: 2600, delay: i * 700, iterations: Infinity, easing: 'ease-out' }); });
    $$('[data-dust]').forEach(function (el, i) { loop(el, [{ transform: 'translate(0,0)', opacity: 0 }, { opacity: 0.9, offset: 0.3 }, { transform: 'translate(' + (50 + (i % 4) * 15) + 'px,-' + (20 + (i % 5) * 8) + 'px)', opacity: 0 }], { duration: 3200 + (i % 5) * 500, delay: (i * 260) % 3000, iterations: Infinity, easing: 'ease-out' }); });
    $$('[data-salt]').forEach(function (el, i) { loop(el, [{ transform: 'translate(0,0)', opacity: 0 }, { opacity: 1, offset: 0.15 }, { transform: 'translate(' + (220 + (i % 4) * 30) + 'px,' + ((i % 2 ? 1 : -1) * (10 + i % 12)) + 'px)', opacity: 0 }], { duration: 3600 + (i % 5) * 400, delay: (i * 230) % 3600, iterations: Infinity, easing: 'linear' }); });
    $$('[data-wind]').forEach(function (el, i) { loop(el, [{ strokeDashoffset: 200 }, { strokeDashoffset: -200 }], { duration: 2800 + i * 400, delay: i * 500, iterations: Infinity, easing: 'linear' }); });
    $$('[data-wave]').forEach(function (el) { loop(el, [{ transform: 'translateX(0)' }, { transform: 'translateX(40px)' }], { duration: 1800, iterations: Infinity, easing: 'linear' }); });
    $$('[data-rain]').forEach(function (el, i) { loop(el, [{ transform: 'translate(0,-40px)', opacity: 0 }, { opacity: 0.9, offset: 0.2 }, { transform: 'translate(-12px,60px)', opacity: 0 }], { duration: 900 + (i % 4) * 120, delay: (i * 97) % 900, iterations: Infinity, easing: 'linear' }); });
    $$('[data-flash]').forEach(function (el) { loop(el, [{ opacity: 0 }, { opacity: 0, offset: 0.7 }, { opacity: 0.55, offset: 0.72 }, { opacity: 0, offset: 0.75 }, { opacity: 0.4, offset: 0.78 }, { opacity: 0, offset: 0.82 }, { opacity: 0 }], { duration: 4200, iterations: Infinity }); });
    $$('[data-bolt]').forEach(function (el) { loop(el, [{ opacity: 0 }, { opacity: 0, offset: 0.7 }, { opacity: 1, offset: 0.72 }, { opacity: 0.2, offset: 0.75 }, { opacity: 1, offset: 0.78 }, { opacity: 0, offset: 0.84 }, { opacity: 0 }], { duration: 4200, iterations: Infinity }); });
    $$('[data-cloud]').forEach(function (el, i) { loop(el, [{ transform: 'translateX(0)' }, { transform: 'translateX(' + (i ? -14 : 14) + 'px)' }], { duration: 5000 + i * 1200, direction: 'alternate', iterations: Infinity, easing: 'ease-in-out' }); });

    /* ---------- marquee: duplicate the editable list for a seamless loop ---------- */
    $$('.pp-marquee .elementor-icon-list-items').forEach(function (ul) {
      if (editor) return;
      var items = $$(':scope > li', ul);
      for (var n = 0; n < 3; n++) items.forEach(function (li) { var c = li.cloneNode(true); c.setAttribute('aria-hidden', 'true'); ul.appendChild(c); });
      loop(ul, [{ transform: 'translateX(0)' }, { transform: 'translateX(-50%)' }], { duration: 32000, iterations: Infinity });
    });

    /* ---------- word-by-word colour fill ---------- */
    var fill = d.querySelector('.pp-wordfill');
    var words = [];
    if (fill && !editor) {
      var target = fill.querySelector('.elementor-widget-container') || fill;
      var p = target.querySelector('p') || target;
      var text = p.textContent.trim();
      p.setAttribute('aria-label', text);
      p.innerHTML = text.split(/\s+/).map(function (w) { return '<span class="pp-word" aria-hidden="true">' + w.replace(/</g, '&lt;') + '</span>'; }).join(' ');
      words = $$('.pp-word', p);
    }

    /* ---------- scroll-driven effects: header shadow, word fill, parallax ---------- */
    var header = d.querySelector('.pp-header-pill');
    var PF = { 'pp-parallax-bg': 0.12, 'pp-par-up': 0.06, 'pp-par-down': -0.05 };
    var para = motion ? $$('.pp-parallax-bg, .pp-par-up, .pp-par-down') : [];
    para.forEach(function (el) { for (var k in PF) if (el.classList.contains(k)) el.setAttribute('data-pp-parallax', PF[k]); });
    var raf = 0;
    function onScroll() {
      cancelAnimationFrame(raf);
      raf = requestAnimationFrame(function () {
        var vh = window.innerHeight;
        if (header) header.classList.toggle('pp-scrolled', window.scrollY > 10);
        if (words.length) {
          var r = fill.getBoundingClientRect();
          var pr = motion ? Math.min(1, Math.max(0, (vh * 0.85 - r.top) / (vh * 0.7))) : 1;
          var n = Math.round(pr * words.length);
          words.forEach(function (w, i) { w.classList.toggle('is-on', i < n); });
        }
        para.forEach(function (el) {
          var f = +(el.getAttribute('data-pp-parallax') || 0);
          var rr = el.getBoundingClientRect();
          var c = rr.top + rr.height / 2 - vh / 2;
          el.style.setProperty('--pp-py', (-c * f).toFixed(1) + 'px');
        });
      });
    }
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    onScroll();

    /* ---------- about: hover-to-open feature rows ---------- */
    $$('.pp-acc').forEach(function (group) {
      var rows = $$('.pp-acc-item', group);
      rows.forEach(function (row) {
        var open = function () { rows.forEach(function (r) { r.classList.toggle('is-open', r === row); }); };
        row.addEventListener('mouseenter', open);
        row.addEventListener('focusin', open);
        row.addEventListener('click', open);
      });
    });

    /* ---------- before / after slider ---------- */
    $$('.pp-ba').forEach(function (ba) {
      ba.style.setProperty('--pp-ba', '46.7%');
      var set = function (e) { var r = ba.getBoundingClientRect(); var pc = Math.max(2, Math.min(98, (e.clientX - r.left) / r.width * 100)); ba.style.setProperty('--pp-ba', pc.toFixed(2) + '%'); };
      ba.addEventListener('pointerdown', function (e) {
        if (editor) return; set(e);
        var mv = function (ev) { set(ev); };
        var up = function () { window.removeEventListener('pointermove', mv); window.removeEventListener('pointerup', up); };
        window.addEventListener('pointermove', mv); window.addEventListener('pointerup', up);
      });
      ba.setAttribute('tabindex', '0'); ba.setAttribute('role', 'slider'); ba.setAttribute('aria-label', 'Before and after comparison');
      ba.addEventListener('keydown', function (e) {
        var v = parseFloat(ba.style.getPropertyValue('--pp-ba')) || 46.7;
        if (e.key === 'ArrowLeft') v -= 4; else if (e.key === 'ArrowRight') v += 4; else return;
        e.preventDefault(); ba.style.setProperty('--pp-ba', Math.max(2, Math.min(98, v)) + '%');
      });
    });

    /* ---------- testimonial slider ---------- */
    $$('.pp-tslider').forEach(function (wrap) {
      if (editor) return;
      var track = wrap.querySelector('.pp-ttrack');
      if (!track) return;
      var inner = track.querySelector(':scope > .e-con-inner') || track;
      var cards = $$(':scope > .e-con', inner);
      var section = wrap.closest('.pp-testimonials') || d;
      var prev = section.querySelector('.pp-tprev a, .pp-tprev .elementor-button');
      var next = section.querySelector('.pp-tnext a, .pp-tnext .elementor-button');
      var dotsWrap = d.createElement('div'); dotsWrap.className = 'pp-tdots'; wrap.appendChild(dotsWrap);
      var idx = 0, pv = 3;
      function avail() { var p = wrap.parentElement; return p ? p.clientWidth + 22 : wrap.clientWidth; }
      function perView() { var w = avail(); return w < 640 ? 1 : w < 1000 ? 2 : 3; }
      function render() {
        var max = cards.length - pv;
        if (idx > max) idx = 0; if (idx < 0) idx = max;
        var cw = avail() / pv;
        inner.style.width = (cw * cards.length) + 'px';
        inner.style.maxWidth = 'none';
        inner.style.transform = 'translateX(-' + (idx * cw) + 'px)';
        cards.forEach(function (c) { c.style.flex = '0 0 ' + cw + 'px'; c.style.width = cw + 'px'; c.style.maxWidth = cw + 'px'; });
        dotsWrap.innerHTML = '';
        for (var i = 0; i <= max; i++) {
          var b = d.createElement('button'); b.type = 'button'; b.setAttribute('aria-label', 'Go to slide ' + (i + 1));
          if (i === idx) b.className = 'is-on';
          (function (n) { b.addEventListener('click', function () { idx = n; render(); restart(); }); })(i);
          dotsWrap.appendChild(b);
        }
      }
      function step(dir) { var max = cards.length - pv; idx = idx + dir > max ? 0 : idx + dir < 0 ? max : idx + dir; render(); }
      var timer = null;
      function restart() { clearInterval(timer); timer = setInterval(function () { step(1); }, 5500); }
      if (prev) prev.addEventListener('click', function (e) { e.preventDefault(); step(-1); restart(); });
      if (next) next.addEventListener('click', function (e) { e.preventDefault(); step(1); restart(); });
      window.addEventListener('resize', function () { var n = perView(); if (n !== pv) { pv = n; idx = 0; } render(); });
      pv = perView(); render(); restart();
    });
  });
})();
