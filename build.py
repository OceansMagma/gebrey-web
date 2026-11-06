# -*- coding: utf-8 -*-
"""Construye el sitio GEBREY: dist/ (para el servidor) y preview/ (para la vista previa como artifact)."""
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
    '<path d="M32 10v20M32 30c0 8-6 10-14 16M32 30c0 8 6 10 14 16M32 30v22" fill="none" stroke="#ff5a47" stroke-width="5" stroke-linecap="round"/>'
    '<circle cx="32" cy="10" r="5" fill="#ffb347"/></svg>', quote=True))

SUN = '<svg class="sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>'
MOON = '<svg class="moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a7 7 0 1 0 10.5 10.5z"/></svg>'

PROJECTS = [
    dict(
        slug="viaconextahub", name="ViaConextaHub", kicker="Plataforma SaaS para agencias de viajes",
        one="Un solo portal para que cada agencia busque y reserve con sus mayoristas, usando sus propias claves.",
        url="https://viaconextahub.es", url_label="viaconextahub.es",
        what="ViaConextaHub conecta a las agencias de viajes con sus mayoristas desde un único buscador. La agencia introduce las claves que cada mayorista le ha dado y trabaja con todos a la vez, con sus condiciones y su facturación de siempre. La plataforma no vende producto ni intermedia: es la pasarela.",
        who="Agencias de viajes de Canarias y la Península que ya operan con varios mayoristas y quieren dejar de saltar entre portales.",
        role="Idea, modelo de negocio, desarrollo completo de la aplicación y de la web, integración con cada mayorista y la operación del servicio.",
        facts=[("Modelo", "Suscripción mensual, desde 25 € más impuestos"), ("Usuarios", "Hasta tres por agencia"),
               ("Aplicación", "app.conexta.es"), ("Demostración", "Dos agencias de prueba, Canarias y Península")],
        schema='{"@context":"https://schema.org","@type":"SoftwareApplication","name":"ViaConextaHub","applicationCategory":"BusinessApplication","operatingSystem":"Web","url":"https://viaconextahub.es","description":"Plataforma SaaS que conecta a las agencias de viajes con sus mayoristas usando las claves de cada agencia.","author":{"@type":"Person","name":"Francisco Gebrie Vicente"},"offers":{"@type":"Offer","price":"25","priceCurrency":"EUR","description":"Suscripción mensual, más impuestos"}}',
        shot='''<div class="shot vch" aria-hidden="true">
  <div class="chips"><span class="chip on">Mayorista A</span><span class="chip">Mayorista B</span><span class="chip">Mayorista C</span><span class="chip">Tus claves</span></div>
  <div class="rows">
    <div class="row"><span class="bar w3"></span><span class="price">184 €</span></div>
    <div class="row"><span class="bar w2"></span><span class="price">211 €</span></div>
    <div class="row"><span class="bar w4"></span><span class="price">176 €</span></div>
    <div class="row"><span class="bar w1 hot"></span><span class="price">199 €</span></div>
  </div>
</div>'''),
    dict(
        slug="citras", name="Citras", kicker="Consola para centros coordinadores de transporte sanitario",
        one="La pantalla desde la que un centro coordinador ve su flota, sus servicios y lo que está pasando ahora.",
        url="https://mbtenerife.es", url_label="mbtenerife.es",
        what="Citras es el producto de MBTenerife para centros de coordinación de ambulancias y transporte de pacientes: servicios programados y urgentes, vehículos y equipos, tiempos y estados, en una consola pensada para turnos largos. Nació para un caso concreto y está generalizada para cualquier centro coordinador.",
        who="Centros coordinadores de transporte sanitario, empresas de ambulancias y servicios de transporte de pacientes.",
        role="Diseño del producto, desarrollo y mantenimiento, bajo la marca MBTenerife.",
        facts=[("Marca", "MBTenerife, fundada en 2024"), ("Nombre anterior", "Pulso"),
               ("Catálogo", "Listado en G2, categoría Fleet Management"), ("Web", "mbtenerife.es")],
        schema='{"@context":"https://schema.org","@type":"SoftwareApplication","name":"Citras","applicationCategory":"BusinessApplication","operatingSystem":"Web","url":"https://mbtenerife.es","description":"Consola para centros coordinadores de ambulancias y transporte de pacientes.","author":{"@type":"Organization","name":"MBTenerife","founder":{"@type":"Person","name":"Francisco Gebrie Vicente"}}}',
        shot='''<div class="shot citras" aria-hidden="true">
  <div class="rows">
    <div class="svc"><i class="state"></i><span class="bar w3"></span><time>08:40</time></div>
    <div class="svc"><i class="state urg"></i><span class="bar w2"></span><time>08:52</time></div>
    <div class="svc"><i class="state wait"></i><span class="bar w4"></span><time>09:10</time></div>
    <div class="svc"><i class="state"></i><span class="bar w1"></span><time>09:25</time></div>
  </div>
  <div class="map"><i class="dot" style="left:22%;top:30%"></i><i class="dot sea" style="left:62%;top:52%"></i><i class="dot amber" style="left:38%;top:74%"></i></div>
</div>'''),
    dict(
        slug="teidetravel", name="TeideTravel", kicker="Agencia de viajes especializada en grupos",
        one="Viajes de grupo organizados desde Santa Cruz de Tenerife, de principio a fin.",
        url="https://teidetravel.es", url_label="teidetravel.es",
        what="TeideTravel es una agencia de viajes minorista para cliente final, centrada en viajes de grupo: viajes de estudios, asociaciones, empresas y familias que viajan juntas. Presupuesto, proveedores, reservas y facturación, con una sola persona de contacto.",
        who="Colegios, asociaciones, empresas y grupos de amigos que viajan juntos desde Canarias.",
        role="Titular de la agencia: comercial, operaciones y facturación. También la web y los sistemas con los que trabaja.",
        facts=[("Licencia", "I-AV-0004172.1"), ("Sede", "Santa Cruz de Tenerife"),
               ("Contacto", "info@teidetravel.es"), ("Especialidad", "Viajes de grupo")],
        schema='{"@context":"https://schema.org","@type":"TravelAgency","name":"TeideTravel","url":"https://teidetravel.es","email":"info@teidetravel.es","address":{"@type":"PostalAddress","addressLocality":"Santa Cruz de Tenerife","addressRegion":"Canarias","addressCountry":"ES"},"founder":{"@type":"Person","name":"Francisco Gebrie Vicente"},"description":"Agencia de viajes especializada en viajes de grupo. Licencia I-AV-0004172.1."}',
        shot='''<div class="shot tt" aria-hidden="true">
  <div class="row"><span class="chip on">Grupo de 42 viajeros</span><span class="chip">4 días</span></div>
  <div class="days">
    <div class="day"><i style="height:38%"></i><span>Día 1</span></div>
    <div class="day"><i style="height:72%"></i><span>Día 2</span></div>
    <div class="day"><i style="height:56%"></i><span>Día 3</span></div>
    <div class="day"><i style="height:30%"></i><span>Día 4</span></div>
  </div>
  <div class="total"><span>Presupuesto por persona</span><span class="price">385 €</span></div>
</div>'''),
    dict(
        slug="web-hosting", name="Web y hosting", kicker="Webs, portales y alojamiento para asociaciones y pymes",
        one="Tu web y tu portal de gestión, alojados y mantenidos por la misma persona que los construye.",
        url=None, url_label=None,
        what="Diseño y desarrollo de webs y portales internos a medida, alojados en un servidor gestionado en España con correo, copias de seguridad y certificados incluidos. Dominios, DNS y correo quedan bajo control y documentados, sin depender de un tercero.",
        who="Asociaciones, despachos y pequeñas empresas que necesitan una web seria y, a menudo, una herramienta interna que ninguna plantilla resuelve.",
        role="Todo el ciclo: diseño, desarrollo, alojamiento, mantenimiento y soporte.",
        facts=[("Ejemplo", "Web y portal de gestión para una asociación (marnin.es)"), ("Alojamiento", "Servidor gestionado en España"),
               ("Incluye", "Correo, copias, certificados y mantenimiento"), ("Facturación", "Como profesional autónomo")],
        schema='{"@context":"https://schema.org","@type":"Service","serviceType":"Diseño web, desarrollo y hosting","provider":{"@type":"Person","name":"Francisco Gebrie Vicente"},"areaServed":"ES","description":"Webs, portales internos y alojamiento gestionado para asociaciones y pymes."}',
        shot='''<div class="shot web" aria-hidden="true">
  <div class="dots"><i></i><i></i><i></i></div>
  <div class="win">
    <div class="col"><span class="bar w4 hot"></span><span class="bar w3"></span><span class="bar w2"></span><span class="bar w3"></span></div>
    <div class="col"><span class="bar w4"></span><span class="bar w4"></span><span class="bar w3"></span><span class="bar w2 sea"></span></div>
  </div>
  <div class="status"><span><b>SSL</b> activo</span><span><b>Copias</b> cada noche</span><span><b>Correo</b> en tu dominio</span></div>
</div>'''),
]

PERSON = dict(
    name="Francisco Gebrie Vicente", email="hola@gebrey.es", phone="+34 663 82 29 55", phone_tel="+34663822955",
    address=["Avda. Tres de Mayo 30, Edif. Adlhers, 1.ª planta", "38005 Santa Cruz de Tenerife"],
)

def head(title, desc, canonical, css_rel, extra="", preview=False):
    base = (f'<title>{html.escape(title)}</title>'
            + ('<meta name="claude:viewport-fit-sides" content="cover">' if preview else '')
            + f'<meta name="description" content="{html.escape(desc, quote=True)}">'
            + f'<link rel="canonical" href="{canonical}">'
            + f'<meta property="og:title" content="{html.escape(title, quote=True)}">'
            + f'<meta property="og:description" content="{html.escape(desc, quote=True)}">'
            + f'<meta property="og:type" content="website"><meta property="og:url" content="{canonical}">'
            + f'<meta property="og:image" content="{SITE}/assets/img/og.png"><meta name="twitter:card" content="summary_large_image">'
            + f'<link rel="icon" href="{FAVICON}">'
            + FONTS
            + f'<link rel="stylesheet" href="{css_rel}">'
            + extra)
    if preview:
        return base
    return ('<!doctype html><html lang="es"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
            + base + '</head><body>')

def header(home, anchors=True):
    base = "" if anchors else home
    def a(h, text, cls=""):
        return f'<a href="{base}{h}"' + (f' class="{cls}"' if cls else "") + f'>{text}</a>'
    nav = (a("#proyectos", "Proyectos") + a("#como", "Cómo trabajo") + a("#sobre", "Sobre mí") + a("#contacto", "Contacto", "nav-contact"))
    return (f'<a class="skip" href="#main">Saltar al contenido</a>'
            f'<header class="top"><div class="wrap">'
            f'<a class="logo" href="{home}" aria-label="GEBREY, inicio">GEB<span class="r">R</span>EY</a>'
            f'<nav class="nav" aria-label="Secciones">{nav}'
            f'<button class="theme" type="button" aria-label="Cambiar entre tema claro y oscuro">{SUN}{MOON}</button>'
            f'</nav></div></header>')

def footer(home, rel):
    items = "".join(f'<li><a href="{rel}proyectos/{p["slug"]}.html">{p["name"]}</a></li>' for p in PROJECTS)
    return (f'<footer class="foot"><div class="wrap">'
            f'<div><a class="logo" href="{home}">GEB<span class="r">R</span>EY</a>'
            f'<p style="margin-top:.6rem">Software y web a medida, hechos en Tenerife.</p>'
            f'<p style="margin-top:.6rem">© 2026 {PERSON["name"]}, profesional autónomo.</p></div>'
            f'<div><p style="color:var(--ink);margin-bottom:.5rem">Proyectos</p><ul>{items}</ul></div>'
            f'<div><p style="color:var(--ink);margin-bottom:.5rem">Contacto</p><ul>'
            f'<li><a href="mailto:{PERSON["email"]}">{PERSON["email"]}</a></li>'
            f'<li><a href="tel:{PERSON["phone_tel"]}">{PERSON["phone"]}</a></li>'
            f'<li><a href="{rel}legal.html">Aviso legal y privacidad</a></li></ul></div>'
            f'</div></footer>')

def scripts(rel, root=False):
    s = f'<script src="{rel}assets/js/site.js" defer></script>'
    if root:
        s += f'<script src="{rel}assets/js/root.js" defer></script>'
    return s

def facts_html(facts):
    return '<dl class="facts">' + "".join(f'<div><dt>{html.escape(k)}</dt><dd>{html.escape(v)}</dd></div>' for k, v in facts) + '</dl>'

# ---------- index ----------
def index_page(preview=False):
    rel = ""
    home = "index.html"
    nodes = "".join(
        f'<li><a class="node" href="proyectos/{p["slug"]}.html" data-branch="{i}">'
        f'<span class="n-name">{p["name"]}</span><span class="n-kicker">{p["kicker"]}</span></a></li>'
        for i, p in enumerate(PROJECTS))
    branches = "".join(
        f'<article class="branch">'
        f'<div class="b-head"><div><h3><a href="proyectos/{p["slug"]}.html" style="text-decoration:none">{p["name"]}</a></h3>'
        f'<p class="b-kicker">{p["kicker"]}</p></div></div>'
        f'{p["shot"]}'
        f'<p class="b-one">{p["one"]}</p>'
        f'<a class="b-link" href="proyectos/{p["slug"]}.html">Ver {p["name"]}<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg></a>'
        f'</article>'
        for p in PROJECTS)
    schema = ('{"@context":"https://schema.org","@graph":['
              '{"@type":"Organization","@id":"https://gebrey.es/#org","name":"GEBREY","url":"https://gebrey.es","email":"hola@gebrey.es","telephone":"+34663822955",'
              '"founder":{"@id":"https://gebrey.es/#person"},"address":{"@type":"PostalAddress","streetAddress":"Avda. Tres de Mayo 30, Edif. Adlhers, 1.ª planta","postalCode":"38005","addressLocality":"Santa Cruz de Tenerife","addressRegion":"Canarias","addressCountry":"ES"},'
              '"description":"Marca profesional de Francisco Gebrie Vicente: software y web a medida, hechos en Tenerife."},'
              '{"@type":"Person","@id":"https://gebrey.es/#person","name":"Francisco Gebrie Vicente","jobTitle":"Desarrollador de software y web, profesional autónomo","worksFor":{"@id":"https://gebrey.es/#org"},"email":"hola@gebrey.es","address":{"@type":"PostalAddress","addressLocality":"Santa Cruz de Tenerife","addressCountry":"ES"}},'
              '{"@type":"ItemList","name":"Proyectos","itemListElement":['
              + ",".join(f'{{"@type":"ListItem","position":{i+1},"name":"{p["name"]}","url":"https://gebrey.es/proyectos/{p["slug"]}.html"}}' for i, p in enumerate(PROJECTS))
              + ']}]}')
    extra = f'<script type="application/ld+json">{schema}</script>'
    out = head("GEBREY", "Software y web a medida, hechos en Tenerife. ViaConextaHub, Citras, TeideTravel y desarrollo web con hosting, por Francisco Gebrie Vicente.",
               SITE + "/", "assets/css/site.css", extra, preview)
    out += header(home)
    out += f'''
<main id="main">
<section class="hero" aria-labelledby="claim">
  <canvas class="rootcv" aria-hidden="true"></canvas>
  <div class="wrap hero-in">
    <p class="wordmark" aria-label="GEBREY"><span>GEB</span><span class="r" id="root-origin">R</span><span>EY</span></p>
    <div class="hero-grid">
      <div>
        <h1 class="claim" id="claim">Software y web a medida, hechos en Tenerife.</h1>
        <p class="lede">Una raíz: Francisco Gebrie, economista y desarrollador. Cuatro ramas: una plataforma para agencias de viajes, una consola para transporte sanitario, una agencia de viajes de grupo y webs con hosting propio.</p>
        <div class="cta"><a class="btn btn-primary" href="#proyectos">Ver los proyectos</a><a class="btn" href="#contacto">Escríbeme</a></div>
      </div>
      <div aria-hidden="true"></div>
    </div>
    <div class="root" id="root">
      <ul class="nodes" id="nodes">{nodes}</ul>
    </div>
  </div>
</section>

<div class="spine">
<section class="section" id="proyectos">
  <div class="wrap">
    <div class="section-head">
      <h2>Cuatro ramas de una misma raíz</h2>
      <p>Cada proyecto nace de un negocio real que gestiono como autónomo. Producto, código, operación y facturación salen de la misma mesa.</p>
    </div>
    <div class="branches">{branches}</div>
    <p class="collab">También colaboro en los desarrollos de <a href="https://vianexo.es" rel="noopener">Vianexo</a> y <a href="https://oceansmagma.es" rel="noopener">Ocean's Magma</a>, plataformas de viajes que llevan otros compañeros.</p>
  </div>
</section>

<section class="section" id="como">
  <div class="wrap">
    <div class="section-head"><h2>Cómo trabajo</h2></div>
    <div class="ways">
      <div class="way"><h3>Producto completo</h3><p>Del modelo de negocio al código, la facturación y el soporte. No hay un equipo detrás: hay una persona que responde de todo.</p></div>
      <div class="way"><h3>Negocios reales</h3><p>Cada producto nace de una empresa que opero yo mismo, así que se prueba con clientes, proveedores y facturas de verdad antes de ofrecerlo a nadie.</p></div>
      <div class="way"><h3>Infraestructura propia</h3><p>Dominios, DNS, correo y alojamiento en mi servidor gestionado en España. Preparado para los buscadores y para los asistentes de IA que hoy también leen las webs.</p></div>
    </div>
  </div>
</section>

<section class="section" id="sobre">
  <div class="wrap">
    <div class="section-head"><h2>Sobre mí</h2></div>
    <div class="about">
      <div class="text">
        <p>Soy Francisco Gebrie Vicente. Me formé en Economía y he pasado años entre facturación, contratos y gestión. Programo porque es la forma más directa de resolver lo que esos trabajos me pedían, y acabé construyendo productos que ahora usan otros.</p>
        <p>Trabajo como autónomo desde Santa Cruz de Tenerife, con clientes en Canarias y la Península. Además de mis proyectos, colaboro en el desarrollo de Vianexo y Ocean's Magma.</p>
      </div>
      <dl class="facts">
        <div><dt>Formación</dt><dd>Economía</dd></div>
        <div><dt>Base</dt><dd>Santa Cruz de Tenerife</dd></div>
        <div><dt>Figura</dt><dd>Profesional autónomo</dd></div>
        <div><dt>Proyectos propios</dt><dd>ViaConextaHub, Citras (MBTenerife), TeideTravel, web y hosting</dd></div>
        <div><dt>Colaboraciones</dt><dd>vianexo.es y oceansmagma.es</dd></div>
      </dl>
    </div>
  </div>
</section>

<section class="section" id="contacto">
  <div class="wrap contact">
    <div>
      <h2>Cuéntame qué necesitas</h2>
      <p class="lede">Una web, una herramienta interna, un producto desde cero o alojamiento con alguien que responda. Escríbeme y lo vemos.</p>
      <div class="big"><a id="mail" href="mailto:{PERSON["email"]}">{PERSON["email"]}</a><button class="copy" type="button" data-copy="{PERSON["email"]}" aria-controls="mail">Copiar</button></div>
    </div>
    <address>
      <a href="tel:{PERSON["phone_tel"]}">{PERSON["phone"]}</a>
      <span>{PERSON["address"][0]}</span>
      <span>{PERSON["address"][1]}</span>
    </address>
  </div>
</section>
</div>
</main>
'''
    out += footer(home, rel)
    out += scripts(rel, root=True)
    if not preview:
        out += '</body></html>'
    return out

# ---------- project pages ----------
def project_page(i):
    p = PROJECTS[i]
    nxt = PROJECTS[(i + 1) % len(PROJECTS)]
    rel = "../"
    home = "../index.html"
    link = (f'<a class="btn btn-primary" href="{p["url"]}" rel="noopener">Ir a {p["url_label"]}</a>' if p["url"]
            else f'<a class="btn btn-primary" href="{home}#contacto">Pedir presupuesto</a>')
    extra = f'<script type="application/ld+json">{p["schema"]}</script>'
    out = head(f'{p["name"]} — GEBREY', p["one"], f'{SITE}/proyectos/{p["slug"]}.html', rel + "assets/css/site.css", extra)
    out += header(home, anchors=False)
    out += f'''
<main id="main">
  <section class="wrap p-hero">
    <p class="kicker">{p["kicker"]}</p>
    <h1>{p["name"]}</h1>
    <p class="one">{p["one"]}</p>
    <div class="cta">{link}<a class="btn" href="{home}#proyectos">Todos los proyectos</a></div>
  </section>
  <section class="wrap p-body">
    <div class="p-text">
      <div><h2>Qué es</h2><p>{p["what"]}</p></div>
      <div><h2>Para quién</h2><p>{p["who"]}</p></div>
      <div><h2>Mi papel</h2><p>{p["role"]}</p></div>
    </div>
    {p["shot"]}
  </section>
  <section class="wrap p-facts">{facts_html(p["facts"])}</section>
  <section class="p-next"><div class="wrap"><a href="{nxt["slug"]}.html"><span class="n-label">Siguiente proyecto</span><span class="n-name">{nxt["name"]}</span></a></div></section>
</main>
'''
    out += footer(home, rel)
    out += scripts(rel)
    out += '</body></html>'
    return out

# ---------- legal ----------
def legal_page():
    rel, home = "", "index.html"
    out = head("Aviso legal — GEBREY", "Aviso legal y política de privacidad de gebrey.es.", SITE + "/legal.html", "assets/css/site.css")
    out += header(home, anchors=False)
    out += f'''
<main id="main" class="wrap legal">
  <h1>Aviso legal y privacidad</h1>
  <h2>Titular</h2>
  <p>{PERSON["name"]}, profesional autónomo. NIF: pendiente de incluir. Domicilio: {PERSON["address"][0]}, {PERSON["address"][1]}. Correo: {PERSON["email"]}. Teléfono: {PERSON["phone"]}.</p>
  <h2>Qué es este sitio</h2>
  <p>gebrey.es presenta la actividad profesional de su titular y enlaza a los proyectos que desarrolla o en los que colabora. Cada proyecto tiene su propio titular, condiciones y política de privacidad en su web.</p>
  <h2>Datos personales</h2>
  <p>Los únicos datos que se tratan son los que tú envías al escribir por correo o llamar: se usan para responderte y, si lo pides, para preparar un presupuesto. La base legal es tu consentimiento y, en su caso, la relación precontractual. No se ceden a terceros salvo obligación legal y se conservan mientras dure la conversación o la relación profesional.</p>
  <p>Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a {PERSON["email"]}. También puedes reclamar ante la Agencia Española de Protección de Datos.</p>
  <h2>Cookies</h2>
  <p>Este sitio no usa cookies de seguimiento ni analítica de terceros. Solo guarda en tu navegador, si la eliges, la preferencia de tema claro u oscuro.</p>
  <h2>Propiedad intelectual</h2>
  <p>Los textos, el diseño y el código de gebrey.es son de su titular. Las marcas de los proyectos enlazados pertenecen a sus respectivos titulares.</p>
</main>
'''
    out += footer(home, rel)
    out += scripts(rel)
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
    urls = [SITE + "/", SITE + "/legal.html"] + [f"{SITE}/proyectos/{p['slug']}.html" for p in PROJECTS]
    body = "".join(f"<url><loc>{u}</loc><lastmod>{TODAY}</lastmod></url>" for u in urls)
    return f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}</urlset>'

def llms():
    lines = ["# GEBREY", "", "> Marca profesional de Francisco Gebrie Vicente, profesional autónomo en Santa Cruz de Tenerife (Canarias, España): software y web a medida.", "",
             "Contacto: hola@gebrey.es · +34 663 82 29 55", "", "## Proyectos propios", ""]
    for p in PROJECTS:
        lines.append(f"- [{p['name']}](https://gebrey.es/proyectos/{p['slug']}.html): {p['one']}" + (f" Sitio: {p['url']}" if p['url'] else ""))
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
    # dist
    write(os.path.join(DIST, "index.html"), index_page(False))
    for i, p in enumerate(PROJECTS):
        write(os.path.join(DIST, "proyectos", p["slug"] + ".html"), project_page(i))
    write(os.path.join(DIST, "legal.html"), legal_page())
    write(os.path.join(DIST, "robots.txt"), ROBOTS)
    write(os.path.join(DIST, "sitemap.xml"), sitemap())
    write(os.path.join(DIST, "llms.txt"), llms())
    write(os.path.join(DIST, ".htaccess"), HTACCESS)
    # preview (artifact): index sin esqueleto, resto igual
    write(os.path.join(PREV, "index.html"), index_page(True))
    for i, p in enumerate(PROJECTS):
        write(os.path.join(PREV, "proyectos", p["slug"] + ".html"), project_page(i))
    write(os.path.join(PREV, "legal.html"), legal_page())
    print("ok")

if __name__ == "__main__":
    build()
