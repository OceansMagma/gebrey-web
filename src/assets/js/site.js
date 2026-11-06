/* GEBREY — comportamiento común: tema, copiar correo, espina de scroll */
(function () {
  const root = document.documentElement;
  const KEY = 'gebrey-theme';

  // tema: respeta el sistema salvo que el visitante elija
  try {
    const saved = localStorage.getItem(KEY);
    if (saved === 'light' || saved === 'dark') root.setAttribute('data-theme', saved);
  } catch (e) { /* sin almacenamiento: se usa el tema del sistema */ }

  function effective() {
    const forced = root.getAttribute('data-theme');
    if (forced) return forced;
    return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }
  document.querySelectorAll('.theme').forEach((btn) => {
    btn.addEventListener('click', () => {
      const next = effective() === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', next);
      try { localStorage.setItem(KEY, next); } catch (e) { /* nada */ }
    });
  });

  // copiar el correo
  document.querySelectorAll('[data-copy]').forEach((btn) => {
    const original = btn.textContent;
    btn.addEventListener('click', () => {
      const text = btn.getAttribute('data-copy');
      const done = () => { btn.textContent = 'Copiado'; setTimeout(() => { btn.textContent = original; }, 1600); };
      const fallback = () => {
        const el = document.getElementById(btn.getAttribute('aria-controls'));
        if (!el) return;
        const r = document.createRange(); r.selectNodeContents(el);
        const s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done).catch(fallback);
      } else fallback();
    });
  });

  // espina: si el navegador no anima con scroll(), se calcula aquí
  const spine = document.querySelector('.spine');
  if (spine && !(window.CSS && CSS.supports && CSS.supports('animation-timeline: scroll()'))) {
    const update = () => {
      const max = document.documentElement.scrollHeight - window.innerHeight;
      const k = max > 0 ? Math.min(1, window.scrollY / max) : 1;
      spine.style.setProperty('--spine', k.toFixed(3));
    };
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
    update();
  }

  // sección actual en la navegación
  const links = Array.from(document.querySelectorAll('.nav a[href^="#"]'));
  if (links.length && 'IntersectionObserver' in window) {
    const map = new Map(links.map(a => [a.getAttribute('href').slice(1), a]));
    const io = new IntersectionObserver((ents) => {
      ents.forEach((e) => {
        const a = map.get(e.target.id);
        if (!a) return;
        if (e.isIntersecting) { links.forEach(l => l.removeAttribute('aria-current')); a.setAttribute('aria-current', 'page'); }
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    map.forEach((a, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
  }
})();
