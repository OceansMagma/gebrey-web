# -*- coding: utf-8 -*-
"""Construye el sitio GEBREY: dist/ (para el servidor) y preview/ (para la vista previa como artifact).
Una sola página con los proyectos, más el aviso legal."""
import os, shutil, html, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
DIST = os.path.join(ROOT, "dist")
PREV = os.path.join(ROOT, "preview")
SITE = "https://gebrey.es"
TODAY = datetime.date.today().isoformat()

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,400..800'
         '&family=Instrument+Sans:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap">')

FAVICON = ("data:image/svg+xml," + html.escape(
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#14100e"/>'
    '<text x="32" y="46" text-anchor="middle" font-family="Arial Narrow, Arial, sans-serif" font-weight="800" font-size="40" fill="#ff5a47">R</text></svg>', quote=True))

SUN = '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
MOON = '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a7 7 0 1 0 10.5 10.5z"/></svg>'

PERSON = dict(
    name="Francisco Gebrie Vicente", email="hola@gebrey.es", phone="+34 822 276 190", phone_tel="+34822276190",
    address=["Avda. Tres de Mayo 30, Edif. Adlhers, 1.ª planta", "38005 Santa Cruz de Tenerife"],
)

PROJECTS = [
    dict(
        slug="viaconextahub", name="ViaConextaHub", color="var(--c-vch)",
        kicker="Plataforma SaaS para agencias de viajes",
        one="Un solo buscador para que cada agencia reserve con todos sus mayoristas, usando sus propias claves.",
        url="https://viaconextahub.es", link="Entrar en viaconextahub.es",
        schema='{"@type":"SoftwareApplication","name":"ViaConextaHub","applicationCategory":"BusinessApplication","operatingSystem":"Web","url":"https://viaconextahub.es","description":"Plataforma SaaS que conecta a las agencias de viajes con sus mayoristas usando las claves de cada agencia.","author":{"@id":"https://gebrey.es/#person"},"offers":{"@type":"Offer","price":"25","priceCurrency":"EUR","description":"Suscripción mensual, más impuestos"}}',
        shot='''<div class="shot vch" aria-hidden="true">
  <div class="chips"><span class="chip on pc" style="--i:0">Mayorista A</span><span class="chip pc" style="--i:1">Mayorista B</span><span class="chip pc" style="--i:2">Mayorista C</span><span class="chip pc" style="--i:3">Tus claves</span></div>
  <div class="rows">
    <div class="row pc" style="--i:3"><span class="bar w3 pc" style="--i:4"></span><span class="price">184 €</span></div>
    <div class="row pc" style="--i:4"><span class="bar w2 pc" style="--i:5"></span><span class="price">211 €</span></div>
    <div class="row pc" style="--i:5"><span class="bar w4 pc" style="--i:6"></span><span class="price">176 €</span></div>
    <div class="row pc" style="--i:6"><span class="bar w1 hot pc" style="--i:7"></span><span class="price">199 €</span></div>
    <div class="row pc" style="--i:7"><span class="bar w3 pc" style="--i:8"></span><span class="price">205 €</span></div>
    <div class="row pc" style="--i:8"><span class="bar w2 pc" style="--i:9"></span><span class="price">232 €</span></div>
  </div>
</div>'''),
    dict(
        slug="citras", name="Citras", color="var(--c-citras)",
        kicker="Consola para centros coordinadores de transporte sanitario",
        one="Flota, servicios y lo que está pasando ahora, en una sola pantalla pensada para turnos largos.",
        url="https://mbtenerife.es", link="Entrar en mbtenerife.es",
        schema='{"@type":"SoftwareApplication","name":"Citras","applicationCategory":"BusinessApplication","operatingSystem":"Web","url":"https://mbtenerife.es","description":"Consola para centros coordinadores de ambulancias y transporte de pacientes, de MBTenerife.","author":{"@type":"Organization","name":"MBTenerife","founder":{"@id":"https://gebrey.es/#person"}}}',
        shot='''<div class="shot citras" aria-hidden="true">
  <div class="rows">
    <div class="svc pc" style="--i:0"><i class="state"></i><span class="bar w3 pc" style="--i:1"></span><time>08:40</time></div>
    <div class="svc pc" style="--i:1"><i class="state urg"></i><span class="bar w2 pc" style="--i:2"></span><time>08:52</time></div>
    <div class="svc pc" style="--i:2"><i class="state wait"></i><span class="bar w4 pc" style="--i:3"></span><time>09:10</time></div>
    <div class="svc pc" style="--i:3"><i class="state"></i><span class="bar w1 pc" style="--i:4"></span><time>09:25</time></div>
    <div class="svc pc" style="--i:4"><i class="state wait"></i><span class="bar w3 pc" style="--i:5"></span><time>09:40</time></div>
    <div class="svc pc" style="--i:5"><i class="state"></i><span class="bar w2 pc" style="--i:6"></span><time>09:55</time></div>
  </div>
  <div class="map pc" style="--i:2"><i class="dot pc" style="left:22%;top:30%;--i:4"></i><i class="dot b pc" style="left:62%;top:52%;--i:5"></i><i class="dot c pc" style="left:38%;top:74%;--i:6"></i></div>
</div>'''),
    dict(
        slug="teidetravel", name="TeideTravel", color="var(--c-tt)",
        kicker="Agencia de viajes especializada en grupos",
        one="Viajes de grupo organizados desde Santa Cruz de Tenerife, de principio a fin.",
        url="https://teidetravel.es", link="Entrar en teidetravel.es",
        schema='{"@type":"TravelAgency","name":"TeideTravel","url":"https://teidetravel.es","email":"info@teidetravel.es","address":{"@type":"PostalAddress","addressLocality":"Santa Cruz de Tenerife","addressRegion":"Canarias","addressCountry":"ES"},"founder":{"@id":"https://gebrey.es/#person"},"description":"Agencia de viajes especializada en viajes de grupo. Licencia I-AV-0004172.1."}',
        shot='''<div class="shot tt" aria-hidden="true">
  <div class="row"><span class="chip on pc" style="--i:0">Grupo de 42 viajeros</span><span class="chip pc" style="--i:1">4 días</span></div>
  <div class="days">
    <div class="day pc" style="--i:2;--h:38%"><i></i><span>Día 1</span></div>
    <div class="day pc" style="--i:3;--h:72%"><i></i><span>Día 2</span></div>
    <div class="day pc" style="--i:4;--h:56%"><i></i><span>Día 3</span></div>
    <div class="day pc" style="--i:5;--h:30%"><i></i><span>Día 4</span></div>
  </div>
  <div class="total pc" style="--i:6"><span>Presupuesto por persona</span><span class="price">385 €</span></div>
</div>'''),
    dict(
        slug="marnin", name="Marnin", color="var(--c-marnin)",
        kicker="Web y portal de empleados de una asociación de socorrismo",
        one="La web de la Asociación de Socorrismo Marnin y la app con la que sus socorristas fichan, firman documentos y organizan cada turno desde la playa.",
        url="https://marnin.es", link="Entrar en marnin.es",
        url2="https://marnin.appequipo.es", link2="Ver el Portal Marnin",
        schema='{"@type":"SoftwareApplication","name":"Portal Marnin","applicationCategory":"BusinessApplication","operatingSystem":"Web","url":"https://marnin.appequipo.es","description":"Portal del empleado de la Asociación de Socorrismo Marnin (Adeje, Tenerife): fichaje, documentos y operativa diaria de los socorristas. Web pública en https://marnin.es.","author":{"@id":"https://gebrey.es/#person"}}',
        shot='''<div class="shot marnin" aria-hidden="true">
  <div class="row"><span class="chip on pc" style="--i:0">Playa de Fañabé</span><span class="chip pc" style="--i:1">Turno 8:00–14:30</span></div>
  <div class="clock">
    <div class="t pc" style="--i:2"><b>08:02</b><span>Entrada</span></div>
    <div class="track"><i class="fill pc" style="--i:3"></i><i class="pin pc" style="--i:4"></i></div>
    <div class="t pc" style="--i:5"><b>14:31</b><span>Salida</span></div>
  </div>
  <div class="rows">
    <div class="doc pc" style="--i:5"><span class="bar w3 pc" style="--i:6"></span><span class="chip on">Firmado</span></div>
    <div class="doc pc" style="--i:6"><span class="bar w2 pc" style="--i:7"></span><span class="chip on">Firmado</span></div>
    <div class="doc pc" style="--i:7"><span class="bar w4 pc" style="--i:8"></span><span class="chip">Pendiente</span></div>
  </div>
</div>'''),
    dict(
        slug="web", name="Web y hosting", color="var(--c-web)",
        kicker="Webs y portales a medida, alojados y mantenidos",
        one="Tu web o tu herramienta interna, en un servidor gestionado en España, con correo, copias y certificados.",
        url="mailto:hola@gebrey.es?subject=Web%20y%20hosting", link="Pedir presupuesto",
        schema='{"@type":"Service","serviceType":"Diseño web, desarrollo y hosting","provider":{"@id":"https://gebrey.es/#person"},"areaServed":"ES","description":"Webs, portales internos y alojamiento gestionado para asociaciones y pymes."}',
        shot='''<div class="shot web" aria-hidden="true">
  <div class="dots"><i class="pc" style="--i:0"></i><i class="pc" style="--i:1"></i><i class="pc" style="--i:2"></i></div>
  <div class="win pc" style="--i:1">
    <div class="col"><span class="bar w4 hot pc" style="--i:2"></span><span class="bar w3 pc" style="--i:3"></span><span class="bar w2 pc" style="--i:4"></span><span class="bar w3 pc" style="--i:5"></span></div>
    <div class="col"><span class="bar w4 pc" style="--i:3"></span><span class="bar w4 pc" style="--i:4"></span><span class="bar w3 pc" style="--i:5"></span><span class="bar w2 pc" style="--i:6"></span></div>
  </div>
  <div class="status pc" style="--i:7"><span><b>SSL</b> activo</span><span><b>Copias</b> cada noche</span><span><b>Correo</b> en tu dominio</span></div>
</div>'''),
]

def letters(text, cls="l"):
    """Cada carácter en un span (para animarlos uno a uno). Los espacios se marcan."""
    out = []
    for i, ch in enumerate(text):
        if ch == " ":
            out.append(f'<span class="{cls} sp" style="--i:{i}"> </span>')
        else:
            out.append(f'<span class="{cls}" style="--i:{i}">{html.escape(ch)}</span>')
    return "".join(out)

def head(title, desc, canonical, css_rel, extra="", preview=False):
    base = (f'<title>{html.escape(title)}</title>'
            + ('<meta name="claude:viewport-fit-sides" content="cover">' if preview else '')
            + f'<meta name="description" content="{html.escape(desc, quote=True)}">'
            + f'<link rel="canonical" href="{canonical}">'
            + f'<meta property="og:title" content="{html.escape(title, quote=True)}">'
            + f'<meta property="og:description" content="{html.escape(desc, quote=True)}">'
            + f'<meta property="og:type" content="website"><meta property="og:url" content="{canonical}">'
            + f'<meta property="og:image" content="{SITE}/assets/img/og.png"><meta name="twitter:card" content="summary_large_image">'
            + '<meta name="theme-color" content="#14100e" media="(prefers-color-scheme: dark)"><meta name="theme-color" content="#efe3cf" media="(prefers-color-scheme: light)">'
            + f'<link rel="icon" href="{FAVICON}">'
            + FONTS
            + f'<link rel="stylesheet" href="{css_rel}">'
            + '<script>if(!matchMedia("(prefers-reduced-motion: reduce)").matches)document.documentElement.classList.add("motion");</script>'
            + extra)
    if preview:
        return base
    return ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            + base + '</head><body>')

def header(home):
    return (f'<a class="skip" href="#main">Saltar al contenido</a>'
            f'<header class="top"><div class="wrap">'
            f'<a class="logo" href="{home}" aria-label="GEBREY, inicio">GEB<span class="r">R</span>EY</a>'
            f'<div class="top-right"><a href="mailto:{PERSON["email"]}">{PERSON["email"]}</a>'
            f'<button class="theme" type="button" aria-label="Cambiar entre tema claro y oscuro">{SUN}{MOON}</button></div>'
            f'</div></header>')

def scripts(rel, reel=False):
    s = f'<script src="{rel}assets/js/site.js" defer></script>'
    if reel:
        s += f'<script src="{rel}assets/js/reel.js" defer></script>'
    return s

# ---------- índice ----------
def index_page(preview=False):
    rel, home = "", "#inicio"
    index = "".join(f'<a href="#{p["slug"]}" style="--dot:{p["color"]};--i:{i}">{p["name"]}</a>' for i, p in enumerate(PROJECTS))
    rail = "".join(f'<a href="#{p["slug"]}" style="--dot:{p["color"]}" data-name="{p["name"]}" aria-label="{p["name"]}"></a>' for p in PROJECTS)
    scenes = ""
    for p in PROJECTS:
        scenes += f'''
<section class="scene" id="{p["slug"]}" style="--c:{p["color"]}" aria-labelledby="t-{p["slug"]}">
  <div class="wrap s-in">
    <p class="s-kicker">{p["kicker"]}</p>
    <h2 class="s-name" id="t-{p["slug"]}" data-fit="{p["name"]}"><span class="vh">{p["name"]}</span><span aria-hidden="true">{letters(p["name"])}</span></h2>
    <div class="s-row">
      <div class="s-text">
        <p class="s-one">{p["one"]}</p>
        <div class="s-links"><a class="s-link" href="{p["url"]}"{' rel="noopener"' if p["url"].startswith("http") else ''}>{p["link"]}</a>{f'<a class="s-link s-link-2" href="{p["url2"]}" rel="noopener">{p["link2"]}</a>' if p.get("url2") else ''}</div>
      </div>
      <div class="s-shot">{p["shot"]}</div>
    </div>
  </div>
</section>'''
    schema = ('{"@context":"https://schema.org","@graph":['
              '{"@type":"Organization","@id":"https://gebrey.es/#org","name":"GEBREY","url":"https://gebrey.es","email":"hola@gebrey.es","telephone":"+34822276190",'
              '"founder":{"@id":"https://gebrey.es/#person"},"address":{"@type":"PostalAddress","streetAddress":"Avda. Tres de Mayo 30, Edif. Adlhers, 1.ª planta","postalCode":"38005","addressLocality":"Santa Cruz de Tenerife","addressRegion":"Canarias","addressCountry":"ES"},'
              '"description":"Software y web a medida, hechos en Tenerife: ViaConextaHub, Citras, TeideTravel, Marnin y desarrollo web con hosting."},'
              '{"@type":"Person","@id":"https://gebrey.es/#person","name":"Francisco Gebrie Vicente","jobTitle":"Desarrollador de software y web, profesional autónomo","worksFor":{"@id":"https://gebrey.es/#org"},"email":"hola@gebrey.es","address":{"@type":"PostalAddress","addressLocality":"Santa Cruz de Tenerife","addressCountry":"ES"}},'
              + ",".join(p["schema"] for p in PROJECTS)
              + ']}')
    extra = f'<script type="application/ld+json">{schema}</script>'
    out = head("GEBREY — software y web hechos en Tenerife",
               "Cinco proyectos de software y web hechos en Tenerife: ViaConextaHub, Citras, TeideTravel, Marnin y desarrollo web con hosting. GEBREY es la marca de Francisco Gebrie Vicente.",
               SITE + "/", "assets/css/site.css", extra, preview)
    out += header(home)
    out += f'''
<main id="main">
<section class="scene hero" id="inicio" aria-label="GEBREY">
  <div class="wrap hero-in">
    <div class="mark-slot" data-fit="GEBREY" data-fit-wdth="88"><span class="mark-ph" aria-hidden="true">GEBREY</span><a class="mark" href="#inicio" aria-label="GEBREY, inicio"><span class="lw" style="--i:0"><span class="l">G</span></span><span class="lw" style="--i:1"><span class="l">E</span></span><span class="lw" style="--i:2"><span class="l">B</span></span><span class="lw r" style="--i:3"><span class="l">R</span></span><span class="lw" style="--i:4"><span class="l">E</span></span><span class="lw" style="--i:5"><span class="l">Y</span></span></a></div>
    <h1 class="tag">Cinco proyectos de software y web, hechos en Tenerife.</h1>
    <nav class="index" aria-label="Proyectos">{index}</nav>
  </div>
  <a class="cue" href="#{PROJECTS[0]["slug"]}" aria-label="Bajar al primer proyecto"></a>
</section>
{scenes}
<section class="scene end" id="contacto" aria-labelledby="t-contacto">
  <div class="wrap s-in end-in">
    <h2 id="t-contacto">Cuéntame tu proyecto.</h2>
    <div class="mail-row">
      <a class="mail" id="mail" href="mailto:{PERSON["email"]}" data-fit="{PERSON["email"]}"><span class="vh">{PERSON["email"]}</span><span aria-hidden="true">{letters(PERSON["email"])}</span></a>
      <button class="copy" type="button" data-copy="{PERSON["email"]}" aria-controls="mail">Copiar el correo</button>
    </div>
    <div class="end-meta">
      <a class="tel" href="tel:{PERSON["phone_tel"]}">{PERSON["phone"]}</a>
      <p>También colaboro en los desarrollos de <a href="https://vianexo.es" rel="noopener">Vianexo</a> y <a href="https://oceansmagma.es" rel="noopener">Ocean's Magma</a>.</p>
    </div>
    <div class="end-foot">
      <span>GEBREY</span>
      <span>{PERSON["name"]}, profesional autónomo</span>
      <span>{PERSON["address"][1]}</span>
      <a href="legal.html">Aviso legal y privacidad</a>
    </div>
  </div>
</section>
</main>
<nav class="rail" aria-label="Posición">{rail}</nav>
'''
    out += scripts(rel, reel=True)
    if not preview:
        out += '</body></html>'
    return out

# ---------- legal ----------
def legal_page():
    out = head("Aviso legal — GEBREY", "Aviso legal y política de privacidad de gebrey.es.", SITE + "/legal.html", "assets/css/site.css")
    out += header("index.html")
    out += f'''
<main id="main" class="wrap"><div class="legal">
  <h1>Aviso legal y privacidad</h1>
  <h2>Titular</h2>
  <p>{PERSON["name"]}, profesional autónomo. NIF 07.979.288-J. Domicilio: {PERSON["address"][0]}, {PERSON["address"][1]}. Correo: {PERSON["email"]}. Teléfono: {PERSON["phone"]}.</p>
  <h2>Qué es este sitio</h2>
  <p>gebrey.es presenta los proyectos que desarrolla su titular y enlaza a cada uno de ellos. Cada proyecto tiene su propio titular, condiciones y política de privacidad en su web.</p>
  <h2>Datos personales</h2>
  <p>Los únicos datos que se tratan son los que tú envías al escribir por correo o llamar: se usan para responderte y, si lo pides, para preparar un presupuesto. La base legal es tu consentimiento y, en su caso, la relación precontractual. No se ceden a terceros salvo obligación legal y se conservan mientras dure la conversación o la relación profesional.</p>
  <p>Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a {PERSON["email"]}. También puedes reclamar ante la Agencia Española de Protección de Datos.</p>
  <h2>Cookies</h2>
  <p>Este sitio no usa cookies de seguimiento ni analítica de terceros. Solo guarda en tu navegador, si la eliges, la preferencia de tema claro u oscuro.</p>
  <h2>Propiedad intelectual</h2>
  <p>Los textos, el diseño y el código de gebrey.es son de su titular. Las marcas de los proyectos enlazados pertenecen a sus respectivos titulares.</p>
  <p><a class="back" href="index.html">Volver a los proyectos</a></p>
</div></main>
'''
    out += scripts("")
    out += '</body></html>'
    return out

ROBOTS = """User-agent: *
Allow: /

User-agent: GPTBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: PerplexityBot
Allow: /

Sitemap: https://gebrey.es/sitemap.xml
"""

def sitemap():
    urls = [SITE + "/", SITE + "/legal.html"]
    body = "".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>'

def llms():
    lines = ["# GEBREY", "", "> Marca profesional de Francisco Gebrie Vicente, profesional autónomo en Santa Cruz de Tenerife (Canarias, España): software y web a medida.", "",
             "Contacto: hola@gebrey.es · +34 822 276 190", "", "## Proyectos", ""]
    for p in PROJECTS:
        site = p["url"] if p["url"].startswith("http") else "https://gebrey.es/#web"
        app = f" App: {p['url2']}" if p.get("url2") else ""
        lines.append(f"- {p['name']} ({p['kicker'].lower()}): {p['one']} Sitio: {site}{app}")
    lines += ["", "## Colaboraciones", "", "- Vianexo (https://vianexo.es) y Ocean's Magma (https://oceansmagma.es): plataformas de viajes de otros compañeros en cuyos desarrollos colabora.", "",
              "## Páginas", "", "- [Inicio](https://gebrey.es/)", "- [Aviso legal y privacidad](https://gebrey.es/legal.html)"]
    return "\n".join(lines) + "\n"

HTACCESS = """RewriteEngine On
# https siempre
RewriteCond %{HTTPS} !=on
RewriteRule ^ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
# www y gebrey.com redirigen a gebrey.es
RewriteCond %{HTTP_HOST} !^gebrey\\.es$ [NC]
RewriteRule ^ https://gebrey.es%{REQUEST_URI} [L,R=301]
# las antiguas páginas de proyecto van a su escena
RedirectMatch 301 ^/proyectos/viaconextahub\\.html$ /#viaconextahub
RedirectMatch 301 ^/proyectos/citras\\.html$ /#citras
RedirectMatch 301 ^/proyectos/teidetravel\\.html$ /#teidetravel
RedirectMatch 301 ^/proyectos/web-hosting\\.html$ /#web
# tipos y caché
AddType text/plain .txt
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 7 days"
  ExpiresByType application/javascript "access plus 7 days"
  ExpiresByType image/svg+xml "access plus 30 days"
  ExpiresByType image/png "access plus 30 days"
</IfModule>
"""

def write(path, content, binary=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb" if binary else "w", encoding=None if binary else "utf-8") as f:
        f.write(content)

def build():
    for d in (DIST, PREV):
        if os.path.isdir(d):
            shutil.rmtree(d)
        shutil.copytree(os.path.join(SRC, "assets"), os.path.join(d, "assets"))
    write(os.path.join(DIST, "index.html"), index_page(False))
    write(os.path.join(DIST, "legal.html"), legal_page())
    write(os.path.join(DIST, "robots.txt"), ROBOTS)
    write(os.path.join(DIST, "sitemap.xml"), sitemap())
    write(os.path.join(DIST, "llms.txt"), llms())
    write(os.path.join(DIST, ".htaccess"), HTACCESS)
    # preview (artifact): index sin esqueleto, resto igual
    write(os.path.join(PREV, "index.html"), index_page(True))
    write(os.path.join(PREV, "legal.html"), legal_page())
    print("ok")

if __name__ == "__main__":
    build()
