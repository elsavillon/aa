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

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    manchetes = []
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
        manchetes.append([
            remove_acentos(titulo),
            link
        ])

    return manchetes

@app.route("/")
def home():
    return "<h2>App DW rodando no Render ✅</h2>"

@app.route("/dw")
def dw():
    dados = manchetes_dw()

    html = """
    <html>
      <head><title>DW</title></head>
      <body>
        <h1>Manchetes Deutsche Welle</h1>
        <ul>
    """

    for titulo, link in dados:
        html += f'<li><a href="{link}" target="_blank">{titulo}</a></li>'

    html += """
        </ul>
      </body>
    </html>
    """

    return html
