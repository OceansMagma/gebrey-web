/* GEBREY — la raíz. Dibuja en un lienzo una raíz que nace de la R del wordmark
   y se ramifica hasta los cuatro proyectos. Crece una sola vez al cargar; después,
   un pulso de savia recorre las ramas de vez en cuando (salvo con movimiento reducido). */
(function () {
  const hero = document.querySelector('.hero');
  const canvas = hero && hero.querySelector('canvas.rootcv');
  const origin = document.getElementById('root-origin');
  const rootBox = document.getElementById('root');
  const nodes = Array.from(document.querySelectorAll('#nodes .node'));
  if (!hero || !canvas || !origin || !rootBox || !nodes.length) return;

  const ctx = canvas.getContext('2d');
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  const narrow = window.matchMedia('(max-width: 860px)');
  let dpr = 1, W = 0, H = 0, offX = 0, offY = 0;
  let paths = [];      // [{pts, len, cum, kind, branch}]
  let hot = -1;
  let progress = 0;    // 0..1 crecimiento
  let t0 = 0, raf = 0, pulses = [], lastPulse = 0, idleRaf = 0;
  const GROW_MS = 2600;

  function css(name) { return getComputedStyle(document.documentElement).getPropertyValue(name).trim(); }
  function rgba(hex, a) {
    const h = hex.replace('#', '');
    const n = parseInt(h.length === 3 ? h.split('').map(c => c + c).join('') : h, 16);
    return `rgba(${(n >> 16) & 255},${(n >> 8) & 255},${n & 255},${a})`;
  }
  function colors() {
    return { a: css('--accent') || '#ff5a47', b: css('--accent-2') || '#ffb347', line: css('--line-strong') || 'rgba(255,255,255,.3)' };
  }

  // muestreo de una cúbica en puntos
  function bezier(p0, p1, p2, p3, n) {
    const pts = [];
    for (let i = 0; i <= n; i++) {
      const t = i / n, u = 1 - t;
      pts.push({
        x: u * u * u * p0.x + 3 * u * u * t * p1.x + 3 * u * t * t * p2.x + t * t * t * p3.x,
        y: u * u * u * p0.y + 3 * u * u * t * p1.y + 3 * u * t * t * p2.y + t * t * t * p3.y
      });
    }
    return pts;
  }
  function measure(pts) {
    const cum = [0];
    for (let i = 1; i < pts.length; i++) {
      const dx = pts[i].x - pts[i - 1].x, dy = pts[i].y - pts[i - 1].y;
      cum.push(cum[i - 1] + Math.hypot(dx, dy));
    }
    return cum;
  }
  function pointAt(path, d) {
    const { pts, cum } = path;
    if (d <= 0) return pts[0];
    if (d >= path.len) return pts[pts.length - 1];
    let i = 1;
    while (cum[i] < d) i++;
    const seg = cum[i] - cum[i - 1], k = seg ? (d - cum[i - 1]) / seg : 0;
    return { x: pts[i - 1].x + (pts[i].x - pts[i - 1].x) * k, y: pts[i - 1].y + (pts[i].y - pts[i - 1].y) * k };
  }
  // ruido determinista por índice para que las curvas no sean simétricas
  function wob(i, k) { return Math.sin(i * 12.9898 + k * 78.233) * 0.5; }

  function layout() {
    const host = narrow.matches ? rootBox : hero;
    const hb = host.getBoundingClientRect();
    const heroB = hero.getBoundingClientRect();
    offX = hb.left - heroB.left; offY = hb.top - heroB.top;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    W = hb.width; H = hb.height;
    canvas.style.left = offX + 'px'; canvas.style.top = offY + 'px';
    canvas.style.width = W + 'px'; canvas.style.height = H + 'px';
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    const ob = origin.getBoundingClientRect();
    let O;
    if (narrow.matches) {
      // en una columna la raíz arranca en el borde superior del bloque, a la altura de la R
      O = { x: Math.min(Math.max(ob.left + ob.width * 0.5 - hb.left, 24), W - 24), y: 0 };
    } else {
      O = { x: ob.left + ob.width * 0.52 - hb.left, y: ob.bottom - hb.top - ob.height * 0.02 };
    }
    const rects = nodes.map((n) => n.getBoundingClientRect());
    const targets = rects.map((b) => ({ x: b.left + b.width * 0.5 - hb.left, y: b.top - hb.top + 1, bottom: b.bottom - hb.top }));
    const nodesTop = Math.min(...targets.map(t => t.y));
    const wide = !narrow.matches;

    paths = [];
    let T, trunk;
    if (wide) {
      // el tronco sale de la R y se desplaza hacia la derecha, lejos del texto, antes de ramificarse
      const tx = Math.max(O.x, W * 0.62);
      T = { x: tx, y: O.y + (nodesTop - O.y) * 0.6 };
      trunk = bezier(O, { x: O.x + (tx - O.x) * 0.5, y: O.y + (T.y - O.y) * 0.06 }, { x: tx + 4, y: T.y - (T.y - O.y) * 0.5 }, T, 60);
    } else {
      T = { x: O.x, y: O.y + (nodesTop - O.y) * 0.42 };
      trunk = bezier(O, { x: O.x + 2, y: O.y + (T.y - O.y) * 0.4 }, { x: T.x - 6, y: T.y - (T.y - O.y) * 0.25 }, T, 40);
    }
    paths.push({ kind: 'trunk', branch: -1, pts: trunk, cum: measure(trunk) });

    // ramas
    const row1 = targets.filter(t => t.y < nodesTop + 10);
    const row1Bottom = Math.max(...row1.map(t => t.bottom));
    targets.forEach((N, i) => {
      let pts;
      if (!wide && N.y > nodesTop + 10) {
        // segunda fila en una columna doble: la rama baja por el canal central y entra por la esquina interior
        const cx = W / 2, gapY = (row1Bottom + N.y) / 2;
        const N2 = { x: cx + (N.x < cx ? -26 : 26), y: N.y };
        pts = bezier(T, { x: T.x, y: T.y + 30 }, { x: cx, y: nodesTop - 24 }, { x: cx, y: nodesTop }, 24)
          .concat(bezier({ x: cx, y: nodesTop }, { x: cx, y: nodesTop + 10 }, { x: cx, y: gapY - 10 }, { x: cx, y: gapY }, 12).slice(1))
          .concat(bezier({ x: cx, y: gapY }, { x: cx, y: gapY + 10 }, { x: N2.x, y: N2.y - 14 }, N2, 16).slice(1));
        paths.push({ kind: 'branch', branch: i, pts, cum: measure(pts), channel: true });
        return;
      }
      const d = N.y - T.y;
      const spread = (N.x - T.x);
      const p1 = { x: T.x + spread * 0.08 + wob(i, 1) * 30, y: T.y + d * 0.45 + wob(i, 2) * 20 };
      const p2 = { x: N.x - spread * 0.12 + wob(i, 3) * 30, y: N.y - d * 0.55 + wob(i, 4) * 20 };
      pts = bezier(T, p1, p2, N, 70);
      paths.push({ kind: 'branch', branch: i, pts, cum: measure(pts) });
    });
    // raicillas: pequeñas curvas laterales que salen de cada rama
    paths.filter(p => p.kind === 'branch' && !p.channel).forEach((p) => {
      [0.33, 0.62].forEach((k, j) => {
        const a = pointAt(p, p.cum[p.cum.length - 1] * k);
        const dir = (j % 2 ? 1 : -1) * (p.branch % 2 ? 1 : -1);
        const len = 26 + wob(p.branch, 5 + j) * 16;
        const e = { x: a.x + dir * len, y: a.y + len * 0.9 };
        const pts = bezier(a, { x: a.x + dir * len * 0.2, y: a.y + len * 0.5 }, { x: e.x - dir * len * 0.2, y: e.y - len * 0.2 }, e, 16);
        paths.push({ kind: 'rootlet', branch: p.branch, at: k, pts, cum: measure(pts) });
      });
    });
    paths.forEach(p => { p.len = p.cum[p.cum.length - 1]; });
  }

  function ease(t) { return t < 0 ? 0 : t > 1 ? 1 : 1 - Math.pow(1 - t, 3); }

  function drawPath(p, frac, width, color, glow) {
    if (frac <= 0) return;
    const d = p.len * frac;
    ctx.beginPath();
    ctx.moveTo(p.pts[0].x, p.pts[0].y);
    let i = 1;
    for (; i < p.pts.length && p.cum[i] <= d; i++) ctx.lineTo(p.pts[i].x, p.pts[i].y);
    if (i < p.pts.length) { const e = pointAt(p, d); ctx.lineTo(e.x, e.y); }
    ctx.lineWidth = width;
    ctx.strokeStyle = color;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.shadowColor = glow || 'transparent';
    ctx.shadowBlur = glow ? 14 : 0;
    ctx.stroke();
    ctx.shadowBlur = 0;
  }

  function render(now) {
    const c = colors();
    ctx.clearRect(0, 0, W, H);
    const grad = ctx.createLinearGradient(0, 0, 0, H);
    grad.addColorStop(0, c.a);
    grad.addColorStop(1, c.b);
    const dim = rgba(c.b.length === 7 ? c.b : '#ffb347', 0.45);

    // tronco: 0–0.32 del progreso; ramas: 0.28–0.95 con escalonado; raicillas al pasar la rama
    const pt = ease(progress / 0.32);
    const trunk = paths[0];
    drawPath(trunk, pt, hot >= 0 ? 3.2 : 3, grad, rgba(c.a, 0.55));

    paths.filter(p => p.kind === 'branch').forEach((p) => {
      const start = 0.28 + p.branch * 0.07;
      const f = ease((progress - start) / 0.6);
      const isHot = hot === p.branch, dimmed = hot >= 0 && !isHot;
      drawPath(p, f, isHot ? 3.2 : 2.1, dimmed ? dim : grad, isHot ? rgba(c.a, 0.8) : rgba(c.b, 0.35));
      // punta brillante mientras crece
      if (f > 0 && f < 1) {
        const e = pointAt(p, p.len * f);
        ctx.beginPath(); ctx.arc(e.x, e.y, 3.2, 0, Math.PI * 2);
        ctx.fillStyle = c.b; ctx.shadowColor = rgba(c.b, 0.9); ctx.shadowBlur = 16; ctx.fill(); ctx.shadowBlur = 0;
      }
    });
    paths.filter(p => p.kind === 'rootlet').forEach((p) => {
      const start = 0.28 + p.branch * 0.07 + p.at * 0.6;
      const f = ease((progress - start) / 0.25);
      const dimmed = hot >= 0 && hot !== p.branch;
      drawPath(p, f, 1.1, dimmed ? dim : rgba(c.b, 0.85), null);
    });
    // nodo de origen
    ctx.beginPath(); ctx.arc(trunk.pts[0].x, trunk.pts[0].y, 4, 0, Math.PI * 2);
    ctx.fillStyle = c.a; ctx.shadowColor = rgba(c.a, 0.9); ctx.shadowBlur = 18; ctx.fill(); ctx.shadowBlur = 0;

    // pulsos de savia
    if (pulses.length) {
      pulses = pulses.filter(pl => now - pl.t0 < pl.dur);
      pulses.forEach((pl) => {
        const k = (now - pl.t0) / pl.dur;
        const total = trunk.len + pl.path.len;
        const d = total * k;
        const pos = d < trunk.len ? pointAt(trunk, d) : pointAt(pl.path, d - trunk.len);
        ctx.beginPath(); ctx.arc(pos.x, pos.y, 2.6, 0, Math.PI * 2);
        ctx.fillStyle = '#fff'; ctx.shadowColor = rgba(c.b, 1); ctx.shadowBlur = 14; ctx.fill(); ctx.shadowBlur = 0;
      });
    }
  }

  function grow(now) {
    if (!t0) t0 = now;
    progress = Math.min(1, (now - t0) / GROW_MS);
    render(now);
    if (progress < 1) raf = requestAnimationFrame(grow);
    else { raf = 0; if (!reduce.matches) idle(now); }
  }

  function idle(now) {
    // cada ~3,5 s sale un pulso por una rama distinta
    if (now - lastPulse > 3500) {
      const branches = paths.filter(p => p.kind === 'branch');
      const b = branches[Math.floor(Math.random() * branches.length)];
      pulses.push({ path: b, t0: now, dur: 1800 });
      lastPulse = now;
    }
    if (pulses.length || now - lastPulse < 50) render(now);
    idleRaf = requestAnimationFrame(idle);
  }

  function restart() {
    cancelAnimationFrame(raf); cancelAnimationFrame(idleRaf);
    layout();
    if (reduce.matches) { progress = 1; render(performance.now()); return; }
    t0 = 0; progress = 0; pulses = []; lastPulse = performance.now();
    raf = requestAnimationFrame(grow);
  }

  // pausa cuando el hero no está a la vista
  let visible = true;
  if ('IntersectionObserver' in window) {
    new IntersectionObserver((ents) => {
      visible = ents[0].isIntersecting;
      if (!visible) { cancelAnimationFrame(idleRaf); idleRaf = 0; }
      else if (progress >= 1 && !idleRaf && !reduce.matches) idleRaf = requestAnimationFrame(idle);
    }, { threshold: 0.05 }).observe(hero);
  }

  nodes.forEach((n, i) => {
    const on = () => { hot = i; render(performance.now()); };
    const off = () => { hot = -1; render(performance.now()); };
    n.addEventListener('mouseenter', on); n.addEventListener('focus', on);
    n.addEventListener('mouseleave', off); n.addEventListener('blur', off);
  });

  let resizeT = 0;
  window.addEventListener('resize', () => {
    clearTimeout(resizeT);
    resizeT = setTimeout(() => { layout(); progress = 1; render(performance.now()); }, 120);
  });
  if (document.fonts && document.fonts.ready) {
    document.fonts.ready.then(restart);
  } else {
    window.addEventListener('load', restart);
  }
  // primer dibujo inmediato para que el primer fotograma no quede vacío
  layout(); progress = reduce.matches ? 1 : 0.0001; render(performance.now());
  new MutationObserver(() => render(performance.now())).observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
})();
