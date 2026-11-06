/* GEBREY — coreografía. El scroll manda: este archivo mide, y escribe en cada escena
   --e (entrada, 0→1 mientras sube) y --x (salida, 0→1 mientras la siguiente la cubre).
   Además recoge el wordmark en la cabecera, ajusta los nombres al ancho, inclina las
   pantallas con el puntero, mantiene el raíl y reproduce los vídeos de cada pantalla solo en su
   escena. Con movimiento reducido no mueve nada. */
(function () {
  const html = document.documentElement;
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const scenes = Array.from(document.querySelectorAll('main > .scene'));
  const mark = document.querySelector('.mark');
  const slot = document.querySelector('.mark-slot');
  const phEl = slot && slot.querySelector('.mark-ph');
  const logo = document.querySelector('.top .logo');
  const rail = Array.from(document.querySelectorAll('.rail a'));
  if (!scenes.length) return;

  const clamp = (v, a, b) => (v < a ? a : v > b ? b : v);
  const easeInOut = (t) => (t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2);

  /* ---- nombres a todo el ancho: se mide cada uno a 100px con wdth 100 ---- */
  const fits = Array.from(document.querySelectorAll('[data-fit]'));
  const probe = document.createElement('span');
  probe.className = 'fit-probe';
  probe.setAttribute('aria-hidden', 'true');
  probe.style.cssText = 'position:absolute;left:-9999px;top:0;visibility:hidden;white-space:nowrap;font-size:100px;line-height:1;display:inline-block;';
  document.body.appendChild(probe);
  function fit() {
    fits.forEach((el) => {
      const src = el.querySelector('.mark-ph') || el;   // el wordmark se mide por su marcador de sitio
      const cs = getComputedStyle(src);
      probe.style.fontFamily = cs.fontFamily;
      probe.style.fontWeight = cs.fontWeight;
      probe.style.fontVariationSettings = '"wdth" ' + (el.getAttribute('data-fit-wdth') || '100') + ', "opsz" 96';
      const ls = parseFloat(cs.letterSpacing) || 0;
      probe.style.letterSpacing = (ls / parseFloat(cs.fontSize) * 100) + 'px';
      probe.innerHTML = src.innerHTML;
      const w = probe.getBoundingClientRect().width / 100;
      if (w > 0) el.style.setProperty('--w', w.toFixed(3));
    });
    // el wordmark fijo vive fuera de la portada: hereda el tamaño medido allí
    if (mark && slot) {
      const ph = slot.querySelector('.mark-ph');
      if (ph) mark.style.fontSize = getComputedStyle(ph).fontSize;
    }
  }

  /* ---- geometría de las escenas ---- */
  let tops = [], heights = [], vh = window.innerHeight, mainTop = 0;
  function measure() {
    vh = window.innerHeight;
    const main = scenes[0].parentElement;
    mainTop = main.getBoundingClientRect().top + window.scrollY;
    let acc = mainTop;
    tops = []; heights = [];
    scenes.forEach((s) => { tops.push(acc); heights.push(s.offsetHeight); acc += s.offsetHeight; });
  }

  /* ---- el wordmark que se recoge ---- */
  let morph = null; // {x0,y0,x1,y1,s}
  function measureMark() {
    if (!mark || !slot || !logo || !html.classList.contains('reel')) { morph = null; return; }
    const was = html.classList.contains('docked');
    html.classList.remove('docked');
    mark.style.transform = 'none';
    const ph = phEl.getBoundingClientRect();
    const lg = logo.getBoundingClientRect();
    const mk = mark.getBoundingClientRect();
    morph = {
      x0: ph.left, y0: ph.top + window.scrollY,   // posición en el documento
      x1: lg.left, y1: lg.top,                    // destino en la ventana (cabecera fija)
      s: lg.width / (mk.width || 1),
      span: Math.max(240, (heights[0] || vh) * 0.62)
    };
    if (was) html.classList.add('docked');
  }

  const state = new Map();
  function setVar(el, name, v) {
    const key = name;
    const prev = state.get(el);
    if (prev && prev[key] === v) return;
    if (!prev) state.set(el, {});
    state.get(el)[key] = v;
    el.style.setProperty(name, v);
  }

  /* ---- vídeos de las pantallas (video[data-src], sin extensión): las fuentes se añaden cuando la
     escena está a dos pantallas, y solo se reproducen mientras su escena es la activa. Con
     movimiento reducido o ahorro de datos se muestra el primer fotograma, sin reproducir. ---- */
  const videos = scenes.map((s) => Array.from(s.querySelectorAll('video[data-src]')));
  const still = reduce.matches || !!(navigator.connection && navigator.connection.saveData);
  function loadVideos(i) {
    videos[i].forEach((v) => {
      if (v.dataset.ready) return;
      v.dataset.ready = '1';
      v.muted = true;
      [['mp4', 'video/mp4'], ['webm', 'video/webm']].forEach(([ext, type]) => {
        const src = document.createElement('source');
        src.src = v.dataset.src + '.' + ext; src.type = type;
        v.appendChild(src);
      });
      v.preload = still ? 'metadata' : 'auto';
      v.load();
    });
  }
  function playVideos(i) {
    videos.forEach((vs, j) => vs.forEach((v) => {
      if (j === i && !still) { const p = v.play(); if (p && p.catch) p.catch(() => {}); }
      else if (!v.paused) v.pause();
    }));
  }

  let active = -1;
  function update() {
    raf = 0;
    const y = window.scrollY;
    let best = 0, bestScore = -1;
    scenes.forEach((s, i) => {
      const top = tops[i], h = heights[i] || vh;
      const e = i === 0 ? 1 : clamp((y - (top - vh)) / vh, 0, 1);
      const x = clamp((y - top) / h, 0, 1);
      setVar(s, '--e', e.toFixed(3));
      setVar(s, '--x', x.toFixed(3));
      if (videos[i].length && y > top - vh * 2) loadVideos(i);
      const score = e * (1 - x);
      if (score > bestScore) { bestScore = score; best = i; }
    });
    if (best !== active) {
      active = best;
      rail.forEach((a, i) => { if (i === best - 1) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
      playVideos(best);
    }
    if (morph) {
      const p = easeInOut(clamp(y / morph.span, 0, 1));
      if (p >= 1) {
        html.classList.add('docked');
      } else {
        html.classList.remove('docked');
        // la portada es fija (la siguiente escena la cubre), así que el punto de partida
        // es la posición real del marcador de sitio en cada fotograma
        const ph = phEl.getBoundingClientRect();
        const x = ph.left + (morph.x1 - ph.left) * p;
        const yy = ph.top + (morph.y1 - ph.top) * p;
        const s = 1 + (morph.s - 1) * p;
        mark.style.transform = `translate3d(${x.toFixed(2)}px, ${yy.toFixed(2)}px, 0) scale(${s.toFixed(4)})`;
      }
    }
  }

  let raf = 0;
  function schedule() { if (!raf) raf = requestAnimationFrame(update); }

  /* ---- inclinación de las pantallas con el puntero ---- */
  const fine = window.matchMedia('(hover: hover) and (pointer: fine)');
  function tilt() {
    if (!fine.matches || reduce.matches) return;
    document.querySelectorAll('.s-shot').forEach((box) => {
      const shot = box.querySelector('.shot');
      let tx = 0, ty = 0, cx = 0, cy = 0, run = 0;
      const scene = box.closest('.scene');
      const tick = () => {
        cx += (tx - cx) * 0.12; cy += (ty - cy) * 0.12;
        box.style.setProperty('--ry', (cx * 7).toFixed(2) + 'deg');
        box.style.setProperty('--rx', (-cy * 7).toFixed(2) + 'deg');
        if (Math.abs(tx - cx) > 0.002 || Math.abs(ty - cy) > 0.002) run = requestAnimationFrame(tick); else run = 0;
      };
      scene.addEventListener('pointermove', (ev) => {
        const r = shot.getBoundingClientRect();
        tx = clamp(((ev.clientX - r.left) / r.width - 0.5) * 2, -1.4, 1.4);
        ty = clamp(((ev.clientY - r.top) / r.height - 0.5) * 2, -1.4, 1.4);
        shot.style.setProperty('--mx', (clamp((ev.clientX - r.left) / r.width, -0.5, 1.5) * 100).toFixed(1) + '%');
        shot.style.setProperty('--my', (clamp((ev.clientY - r.top) / r.height, -0.5, 1.5) * 100).toFixed(1) + '%');
        if (!run) run = requestAnimationFrame(tick);
      });
      scene.addEventListener('pointerleave', () => { tx = 0; ty = 0; if (!run) run = requestAnimationFrame(tick); });
    });
    // portada: las letras del wordmark se apartan ligeramente del puntero, cada una a su ritmo
    const hero = document.querySelector('.hero');
    if (hero && mark) {
      const ls = Array.from(mark.querySelectorAll('.l'));
      let hx = 0, hy = 0, gx = 0, gy = 0, hrun = 0;
      const htick = () => {
        hx += (gx - hx) * 0.1; hy += (gy - hy) * 0.1;
        ls.forEach((l, i) => {
          const k = (i - 2.5) / 2.5;                       // -1 … 1 de izquierda a derecha
          l.style.translate = `${(hx * (6 + 4 * Math.abs(k))).toFixed(2)}px ${(hy * 10 - hx * k * 6).toFixed(2)}px`;
        });
        if (Math.abs(gx - hx) > 0.002 || Math.abs(gy - hy) > 0.002) hrun = requestAnimationFrame(htick); else hrun = 0;
      };
      hero.addEventListener('pointermove', (ev) => {
        if (html.classList.contains('docked')) return;
        gx = (ev.clientX / window.innerWidth - 0.5) * 2; gy = (ev.clientY / window.innerHeight - 0.5) * 2;
        if (!hrun) hrun = requestAnimationFrame(htick);
      });
      hero.addEventListener('pointerleave', () => { gx = 0; gy = 0; if (!hrun) hrun = requestAnimationFrame(htick); });
    }
    // foco de luz: la escena activa recibe la posición del puntero
    document.addEventListener('pointermove', (ev) => {
      const s = scenes[active] || scenes[0];
      s.style.setProperty('--lx', (ev.clientX / window.innerWidth * 100).toFixed(1) + '%');
      s.style.setProperty('--ly', (ev.clientY / window.innerHeight * 100).toFixed(1) + '%');
    }, { passive: true });
    // botones magnéticos
    document.querySelectorAll('.s-link').forEach((btn) => {
      const parent = btn.closest('.s-text') || btn.parentElement;
      parent.addEventListener('pointermove', (ev) => {
        const r = btn.getBoundingClientRect();
        const dx = ev.clientX - (r.left + r.width / 2), dy = ev.clientY - (r.top + r.height / 2);
        const d = Math.hypot(dx, dy), R = 110;
        if (d < R) { const k = (1 - d / R) * 0.35; btn.style.transform = `translate(${(dx * k).toFixed(1)}px, ${(dy * k).toFixed(1)}px)`; }
        else btn.style.transform = '';
      });
      parent.addEventListener('pointerleave', () => { btn.style.transform = ''; });
    });
  }

  function relayout() { fit(); measure(); measureMark(); update(); }

  /* ---- arranque ---- */
  if (!reduce.matches) {
    html.classList.add('motion');
    if (mark && slot && logo) {
      // el wordmark sale de la portada (que se escala al ser cubierta) y pasa a ser fijo
      document.body.appendChild(mark);
      html.classList.add('reel');
    }
    // tras la secuencia de carga, las letras dejan de recortarse (para que el brillo de la R se vea)
    setTimeout(() => html.classList.add('risen'), 1500);
  }
  fit(); measure(); measureMark(); update();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(relayout);
  window.addEventListener('load', relayout);
  window.addEventListener('scroll', schedule, { passive: true });
  let rt = 0;
  window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(relayout, 100); });
  if (!reduce.matches) tilt();
})();
