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
email = os.environ["EMAIL_REMETENTE"]
password = os.environ["SMTP_PASSWORD"]

remetente = os.environ["EMAIL_REMETENTE"]
destinatarios = os.environ["EMAIL_DESTINATARIOS"].split(',')

envio_realizado = False

app = Flask(__name__)

def enviar_email():
    global envio_realizado
    if not envio_realizado:
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

        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  
        server.login(email, password)  

        mensagem = MIMEMultipart()
        mensagem["From"] = remetente
        mensagem["To"] = ",".join(destinatarios)
        mensagem["Subject"] = titulo_email
        conteudo_html = MIMEText(html, "html")  # Adiciona a versão em HTML
        mensagem.attach(conteudo_html)

        server.sendmail(remetente, destinatarios, mensagem.as_string())
        server.quit()

        envio_realizado = True

@app.route("/")
def index():
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
    enviar_email()
    return render_template("dw.html")  

if __name__ == "__main__":
    app.run(debug=True)

