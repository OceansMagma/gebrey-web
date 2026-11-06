# gebrey.es

Web de GEBREY, la marca profesional de Francisco Gebrie Vicente.

- `src/` — fuentes (CSS, JS); `build.py` genera el sitio en `dist/`.
- `site/` — sitio estático listo para publicar (lo que se copia a `public_html`).
- `.github/workflows/deploy.yml` — cada push a `main` que toque `site/` sube los cambios por FTP (FTPS) a cPanel.

## Publicación automática

En GitHub → Settings → Secrets and variables → Actions, crear:

- `FTP_HOST` = `net1002.webcloud.es`
- `FTP_USER` = la cuenta FTP creada en cPanel con carpeta raíz `public_html` (p. ej. `deploy@gebrey.es`)
- `FTP_PASSWORD` = su contraseña

Para regenerar el sitio: `python3 build.py` y copiar `dist/` a `site/`.
