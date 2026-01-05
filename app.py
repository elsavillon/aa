import requests
from bs4 import BeautifulSoup
import unicodedata
from flask import Flask

app = Flask(__name__)

def remove_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def manchetes_dw():
    url = "https://www.dw.com/pt-br/manchetes/headlines-pt-br"
    headers = {"User-Agent": "Mozilla/5.0"}

    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    resultado = []
    vistos = set()

    for a in soup.find_all("a", href=True):
        titulo = a.get_text(strip=True)
        link = a["href"]

        if not titulo:
            continue

        if link.startswith("/"):
            link = "https://www.dw.com" + link

        if "/pt-br/" not in link:
            continue

        chave = (titulo, link)
        if chave in vistos:
            continue

        vistos.add(chave)
        resultado.append([remove_acentos(titulo), link])

    return resultado

@app.route("/")
def home():
    return "App DW rodando no Render ✅"

@app.route("/dw")
def dw():
    dados = manchetes_dw()

    html = "<h1>Manchetes DW</h1><ul>"
    for t, l in dados:
        html += f'<li><a href="{l}" target="_blank">{t}</a></li>'
    html += "</ul>"

    return html

