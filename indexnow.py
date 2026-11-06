"""Avisa por IndexNow (Bing, Yandex, Seznam, Naver, Yep…) de que las páginas de gebrey.es han cambiado.
Ejecutar después de publicar: python3 indexnow.py   (la clave es INDEXNOW_KEY en build.py y está publicada en la raíz de la web)."""
import json, urllib.request
from build import INDEXNOW_KEY, SITE

urls = [SITE + "/", SITE + "/legal.html"]
body = json.dumps({"host": "gebrey.es", "key": INDEXNOW_KEY, "keyLocation": f"{SITE}/{INDEXNOW_KEY}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        print("IndexNow:", r.status, r.reason, "(200/202 = aceptado)")
except urllib.error.HTTPError as e:
    print("IndexNow:", e.code, e.reason, e.read().decode()[:200])
