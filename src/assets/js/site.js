/* GEBREY — tema claro/oscuro y copiar el correo */
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
})();
