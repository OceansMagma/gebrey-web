# gebrey.es

Web de GEBREY: un escaparate de proyectos en una sola página (ViaConextaHub, AppEquipo, Citras, TeideTravel, Marnin y Web y hosting) más el aviso legal. El nombre del titular solo aparece en el aviso legal.

## Estructura

- `src/` — fuentes: `assets/css/site.css`, `assets/js/reel.js` (coreografía de scroll), `assets/js/site.js` (tema y copiar correo), `assets/img/og.png`.
- `build.py` — genera la página desde los datos de los proyectos (`PROJECTS`) y los textos de contacto (`PERSON`). Escribe `dist/` (para el servidor) y `preview/` (vista previa). Los vídeos de AppEquipo no se copian: se sirven desde `https://mbtenerife.es/video/` (`VIDEO_APPEQUIPO`).
- `og.js` — regenera `src/assets/img/og.png` (la imagen al compartir) con Playwright; ejecútalo si cambia la lista de proyectos.
- `site/` — copia de `dist/` que se publica. **Es lo que sube el workflow.**
- `shot.js` — capturas con Playwright para revisar escritorio, móvil y tema claro.

## Cambiar algo

1. Edita `build.py` (textos, enlaces, teléfono) o `src/assets/…` (estilos, movimiento).
2. `python3 build.py` y copia `dist/` a `site/`.
3. Commit y push a `main`: el workflow **Publicar gebrey.es** sube `site/` por FTPS a `public_html`.

Los secretos del workflow (`FTP_HOST`, `FTP_USER`, `FTP_PASSWORD`) están en Settings → Secrets and variables → Actions.
