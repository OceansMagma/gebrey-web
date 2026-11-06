# gebrey.es

Web de GEBREY, la marca profesional de Francisco Gebrie Vicente.

- `src/` — fuentes (CSS, JS) y `build.py` genera el sitio.
- `site/` — sitio estático listo para publicar (lo que cPanel copia a `public_html`).
- `.cpanel.yml` — despliegue con Git Version Control de cPanel.

Para regenerar: `python3 build.py` (deja la salida en `dist/`; copiar a `site/`).
