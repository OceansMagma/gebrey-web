/* GEBREY — tema claro/oscuro, copiar el correo y el formulario de presupuesto */
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

  // pedir presupuesto: los botones abren la frase con huecos; sin JS siguen siendo un mailto
  const dlg = document.getElementById('presupuesto');
  if (dlg && typeof dlg.showModal === 'function') {
    const form = dlg.querySelector('.q-form');
    const done = dlg.querySelector('.q-done');
    const err = dlg.querySelector('.q-error');
    const send = dlg.querySelector('.q-send');
    const blanks = Array.from(form.querySelectorAll('input[type="text"], input[type="email"]'));
    // cada hueco mide lo que lleva escrito (o su pista), con un margen
    const fit = (el) => { const n = el.value.length || el.placeholder.length; el.style.width = (Math.min(Math.max(n, 4), 40) * 0.54 + 1) + 'em'; };
    blanks.forEach((el) => { fit(el); el.addEventListener('input', () => fit(el)); });
    document.querySelectorAll('[data-quote]').forEach((a) => {
      a.addEventListener('click', (ev) => {
        ev.preventDefault();
        form.hidden = false; done.hidden = true; err.hidden = true;
        form.querySelector('[name="t"]').value = Math.floor(Date.now() / 1000);
        dlg.showModal();
        const first = form.querySelector('#q-para');
        if (first && window.matchMedia('(hover: hover)').matches) first.focus();
      });
    });
    dlg.querySelectorAll('[data-quote-close]').forEach((b) => b.addEventListener('click', () => dlg.close()));
    dlg.addEventListener('click', (ev) => { if (ev.target === dlg) dlg.close(); });   // clic fuera de la tarjeta
    const phrase = () => {
      const f = new FormData(form);
      return `Quiero ${f.get('tipo')} para ${f.get('para')}, que sobre todo tiene que ${f.get('que')}. Lo necesito ${f.get('cuando')}.\nMe llamo ${f.get('nombre')} y me escribes a ${f.get('correo')}.\n\n${f.get('mas') || ''}`;
    };
    form.addEventListener('submit', async (ev) => {
      ev.preventDefault();
      err.hidden = true;
      if (!form.reportValidity()) return;
      send.disabled = true;
      try {
        const r = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
        const data = await r.json();
        if (!data.ok) throw new Error(data.error || 'No se ha podido enviar.');
        form.hidden = true; done.hidden = false;
        form.reset(); blanks.forEach(fit);
      } catch (e) {
        // si el servidor no responde, se abre el correo con la frase ya escrita
        err.textContent = (e.message && e.message !== 'Failed to fetch' ? e.message + ' ' : '') + 'Se abre tu correo con el mensaje preparado.';
        err.hidden = false;
        location.href = 'mailto:hola@gebrey.es?subject=' + encodeURIComponent('Presupuesto') + '&body=' + encodeURIComponent(phrase());
      } finally {
        send.disabled = false;
      }
    });
  }
})();
