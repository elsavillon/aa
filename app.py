import requests
from bs4 import BeautifulSoup
import unicodedata
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template

def remove_acentos(texto):
    """Remove acentuação de um texto."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def manchetes_dw():
    url = "https://www.dw.com/pt-br/manchetes/headlines-pt-br"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    # Faz a requisição e verifica se ocorreu com sucesso
    resposta = requests.get(url, headers=headers)
    resposta.raise_for_status()

    sopa = BeautifulSoup(resposta.content, "html.parser")

    lista_dw = []

    # O site DW costuma usar tags <h2>, <h3> ou <a> com link e título visível.
    # Conforme estrutura atual da página, normalmente cada item principal está em
    # um <a> com texto e href válido.
    # Inspecione HTML para confirmar a classe exata se necessário.
    itens = sopa.find_all("a")

    for item in itens:
        titulo = item.get_text(strip=True)
        link = item.get("href")

        # Pulando itens sem título ou sem link
        if not titulo or not link:
            continue

        # Garante que links relativos sejam convertidos em absolutos
        if link.startswith("/"):
            link = "https://www.dw.com" + link

        titulo_sem_acentos = remove_acentos(titulo)

        # Aplica filtros básicos (por exemplo, link válido)
        if "dw.com/pt-br/" in link:
            lista_dw.append([titulo_sem_acentos, link])

    # Remove duplicatas (se houver)
    seen = set()
    lista_filtrada = []
    for titulo, link in lista_dw:
        if (titulo, link) not in seen:
            seen.add((titulo, link))
            lista_filtrada.append([titulo, link])

    return lista_filtrada

# Configurações de SMTP
smtp_server = "smtp-relay.brevo.com"
port = 587
email = os.environ["EMAIL_REMETENTE"]
password = os.environ["SMTP_PASSWORD"]

remetente = os.environ["EMAIL_REMETENTE"]
destinatarios = os.environ["EMAIL_DESTINATARIOS"].split(",")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route("/curriculo")
def curriculo():
    return render_template("curriculo.html")

@app.route("/dw")
def dw_route():
    manchetes_links = manchetes_dw()

    # Monta o HTML de resposta
    html = """
    <html>
        <head>
            <title>Manchetes Deutsche Welle</title>
        </head>
        <body>
            <h1>Destaques Semanais DW</h1>
            <p>Sem tempo para ler as notícias? Aqui estão os principais destaques:</p>
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

    # Envia e-mail com as manchetes (tratamento de erro incluso)
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(email, password)

        mensagem = MIMEMultipart()
        mensagem["From"] = remetente
        mensagem["To"] = ",".join(destinatarios)
        mensagem["Subject"] = titulo_email

        conteudo_html = MIMEText(html, "html")
        mensagem.attach(conteudo_html)

        server.sendmail(remetente, destinatarios, mensagem.as_string())
    except Exception as e:
        print("Erro ao enviar email:", e)
    finally:
        server.quit()

    return html

if __name__ == "__main__":
    app.run(debug=True)
