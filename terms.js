(function () {
  'use strict';
  var box = document.getElementById('terms');
  if (!box) return;
  var KEY = 'codemap-term-popups', defs = {};
  function getOn() { try { return sessionStorage.getItem(KEY) !== 'off'; } catch (e) { return true; } }
  function saveOn(v) { try { sessionStorage.setItem(KEY, v ? 'on' : 'off'); } catch (e) {} }
  function idOf(a) { var h = a.getAttribute('href') || '', i = h.indexOf('#'); return i < 0 ? null : h.slice(i + 1); }
  box.querySelectorAll('a[data-def]').forEach(function (a) { defs[idOf(a)] = { term: a.innerHTML, def: a.getAttribute('data-def') }; });
  var on = getOn(), main = document.querySelector('main') || document.body;
  var pop = document.createElement('div');
  pop.className = 'term-pop'; pop.id = 'term-pop'; pop.setAttribute('role', 'tooltip'); pop.hidden = true;
  main.appendChild(pop);
  var current = null, hideTimer = null, touch = false;
  var p = document.createElement('p');
  p.className = 'term-toggle';
  p.innerHTML = '<label><input type="checkbox"> Show definitions when pointing at a term (for this visit)</label>';
  var cb = p.querySelector('input');
  box.insertBefore(p, box.querySelector('p'));
  function setOn(v) { on = v; saveOn(v); cb.checked = v; document.documentElement.classList.toggle('term-popups', v); if (!v) hide(); }
  cb.addEventListener('change', function () { setOn(cb.checked); });
  function show(a, withLink) {
    var d = on && defs[idOf(a)];
    if (!d) return false;
    clearTimeout(hideTimer);
    pop.innerHTML = '<strong>' + d.term + '</strong><br>' + d.def + '<span class="term-pop-actions">' +
      (withLink ? '<a href="' + a.getAttribute('href') + '">Open in the glossary</a>' : '') +
      '<button type="button" class="term-pop-off">Turn off pop-ups</button></span>';
    pop.querySelector('.term-pop-off').addEventListener('click', function () { var a0 = current; setOn(false); if (a0) a0.focus(); });
    pop.hidden = false;
    if (window.MathJax && MathJax.typesetPromise) MathJax.typesetPromise([pop]);
    var r = a.getBoundingClientRect(), w = Math.min(448, window.innerWidth - 32);
    pop.style.width = w + 'px';
    pop.style.left = Math.max(16, Math.min(r.left + window.scrollX, window.scrollX + window.innerWidth - w - 16)) + 'px';
    pop.style.top = (r.bottom + window.scrollY + 6) + 'px';
    var pr = pop.getBoundingClientRect();
    if (pr.bottom > window.innerHeight && r.top > pr.height + 12) pop.style.top = (r.top + window.scrollY - pr.height - 6) + 'px';
    if (current && current !== a) current.removeAttribute('aria-describedby');
    a.setAttribute('aria-describedby', 'term-pop');
    current = a;
    return true;
  }
  function hide() { pop.hidden = true; if (current) current.removeAttribute('aria-describedby'); current = null; }
  function hideSoon() { clearTimeout(hideTimer); hideTimer = setTimeout(hide, 150); }
  main.querySelectorAll('a.term').forEach(function (a) {
    a.addEventListener('touchstart', function () { touch = true; }, { passive: true });
    a.addEventListener('mouseenter', function () { if (!touch) show(a, false); });
    a.addEventListener('mouseleave', hideSoon);
    a.addEventListener('focus', function () { if (!touch) show(a, false); });
    a.addEventListener('blur', function () { if (!pop.contains(document.activeElement)) hideSoon(); });
    a.addEventListener('click', function (e) { if (touch && on && current !== a && show(a, true)) e.preventDefault(); });
  });
  pop.addEventListener('mouseenter', function () { clearTimeout(hideTimer); });
  pop.addEventListener('mouseleave', hideSoon);
  pop.addEventListener('focusin', function () { clearTimeout(hideTimer); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') hide(); });
  document.addEventListener('click', function (e) { if (!pop.hidden && !pop.contains(e.target) && !(current && current.contains(e.target))) hide(); });
  window.addEventListener('resize', hide);
  setOn(on);
})();
