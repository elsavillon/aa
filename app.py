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
    requisicao = requests.get('https://www.dw.com/pt-br/manchetes/headlines-pt-br')
    html = requisicao.content
    sopa = BeautifulSoup(html, 'html.parser')
    dw = sopa.findAll('div', {'class': 'teaser-wrap col-12 col-md-6 col-lg-4'})
    lista_dw = []
    for item in dw:
        titulo = item.find('h3').text
        link = item.find('a').get('href')
        if link.startswith('/'):
            link = 'https://www.dw.com' + link
        link_sem_acentos = remove_acentos(link)
        lista_dw.append([titulo, link_sem_acentos])
    return lista_dw

smtp_server = "smtp-relay.brevo.com"
port = 587
email_remetente = os.environ.get("EMAIL_REMETENTE")
smtp_password = os.environ.get("SMTP_PASSWORD")
email_destinatarios = os.environ.get("EMAIL_DESTINATARIOS")

envio_realizado = False

app = Flask(__name__)

def enviar_email():
    manchetes_links = manchetes_dw()

    html = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>Manchetes Deutsche Welle</title>
      </head>
      <body>
        <h1>Destaques Semanais</h1>
        <p>
          Sem tempo para ler as notícias? Sem problemas, eu fiz a ronda no Deutsche Welle e trago os destaques:
          <ul>
    """
    for titulo, link in manchetes_links:
        html += f'<li> <a href="{link}">{titulo}</a> </li>'
    html += """
          </ul>
        </p>
      </body>
    </html>
    """

    titulo_email = "Destaques da Semana - Deutsche Welle"

    if email_remetente and smtp_password and email_destinatarios:
        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  
        server.login(email_remetente, smtp_password)  

        mensagem = MIMEMultipart()
        mensagem["From"] = email_remetente
        mensagem["To"] = email_destinatarios
        mensagem["Subject"] = titulo_email
        conteudo_html = MIMEText(html, "html")  # Adiciona a versão em HTML
        mensagem.attach(conteudo_html)

        server.sendmail(email_remetente, email_destinatarios.split(','), mensagem.as_string())
        server.quit()

        global envio_realizado
        envio_realizado = True
    else:
        print("Erro: Verifique as variáveis de ambiente EMAIL_REMETENTE, SMTP_PASSWORD e EMAIL_DESTINATARIOS")

@app.route("/")
def index():
    global envio_realizado
    if not envio_realizado:
        enviar_email()
    return render_template("home.html")
    
@app.route("/portfolio")
def portifolio():
    return render_template("portfolio.html")

@app.route("/curriculo")
def curriculo():
    return render_template("curriculo.html")

@app.route("/dw")
def dw():
    global envio_realizado
    if not envio_realizado:
        enviar_email()
    return render_template("dw.html")  

if __name__ == "__main__":
    app.run(debug=True)

