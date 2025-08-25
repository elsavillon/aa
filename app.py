import requests
from bs4 import BeautifulSoup
import unicodedata
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template

def remove_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

def manchetes_dw():
    url = 'https://www.dw.com/pt-br/manchetes/headlines-pt-br'
    requisicao = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    requisicao.raise_for_status()
    sopa = BeautifulSoup(requisicao.content, 'html.parser')

    # Adaptado para o layout atual
    itens = sopa.find_all('a', class_="teaser-link")  # inspecione para confirmar
    lista_dw = []
    for item in itens:
        titulo = item.get_text(strip=True)
        link = item.get('href')

        if not titulo or not link:
            continue

        if link.startswith('/'):
            link = 'https://www.dw.com' + link

        titulo_sem_acentos = remove_acentos(titulo)
        lista_dw.append([titulo_sem_acentos, link])
    return lista_dw

smtp_server = "smtp-relay.brevo.com"
port = 587
email = os.environ["EMAIL_REMETENTE"]
password = os.environ["SMTP_PASSWORD"]

remetente = os.environ["EMAIL_REMETENTE"]
destinatarios = os.environ["EMAIL_DESTINATARIOS"].split(',')

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/portfolio")
def portifolio():
    return render_template("portfolio.html")

@app.route("/curriculo")
def curriculo():
    return render_template("curriculo.html")

@app.route("/dw")
def dw_route():
    manchetes_links = manchetes_dw()

    html = """
    <html>
        <head>
            <title>Manchetes Deutsche Welle</title>
        </head>
        <body>
            <h1>Destaques Semanais DW </h1>
            <p>Sem tempo para ler as notícias? Sem problemas, eu fiz a ronda no Deutsche Welle e trago os destaques:</p>
            <ul>
    """
    for titulo, link in manchetes_links:
        html += f'<li><a href="{link}" target="_blank">{titulo}</a></li>'
    html += """
            </ul>
        </body>
    </html>
    """

    titulo_email = "Destaques da Semana - Deutsche Welle"

    try:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()
        server.login(email, password)

        mensagem = MIMEMultipart()
        mensagem["From"] = remetente
        mensagem["To"] = ",".join(destinatarios)
        mensagem["Subject"] = titulo_email
        conteudo_html = MIMEText(html, "html")
        mensagem.attach(conteudo_html)

        server.sendmail(remetente, destinatarios, mensagem.as_string())
    finally:
        server.quit()

    return html

if __name__ == "__main__":
    app.run(debug=True)
