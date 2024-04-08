import requests
from bs4 import BeautifulSoup
import unicodedata
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Função para remover acentos
def remove_acentos(texto):
    return ''.join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

# Função para extrair manchetes e links da DW
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

# Dados para conexão no servidor SMTP:
smtp_server = "smtp-relay.brevo.com"
port = 587
email = os.environ["EMAIL_REMETENTE"]
password = os.environ["SMTP_PASSWORD"]

# Dados para o email que será enviado:
remetente = os.environ ["EMAIL_REMETENTE"]
destinatarios = os.environ ["EMAIL_DESTINATARIOS"]

# Extrair manchetes e links
manchetes_links = manchetes_dw()

# Construir o corpo do e-mail
html = html = """
<!DOCTYPE html>
<html>
  <head>
    <title>Manchetes Deutsch Welle</title>
  </head>
  <body>
    <h1>Destaques Semanais</h1>
    <p>
      Sem tempo para ler as notícias? Sem problemas, eu fiz a ronda no Deutsch Welle e trago os destaques:
      <ul>
"""

# Título do email
titulo_email = "Destaques da Semana - Deutsch Welle"

# Iniciar conexão com o servidor SMTP
server = smtplib.SMTP(smtp_server, port)
server.starttls()  # Altera a comunicação para utilizar criptografia
server.login(email, password)  # Autentica

# Preparando o objeto da mensagem
mensagem = MIMEMultipart()
mensagem["From"] = remetente
mensagem["To"] = ",".join(destinatarios)
mensagem["Subject"] = titulo_email
conteudo_html = MIMEText(html, "html")  # Adiciona a versão em HTML
mensagem.attach(conteudo_html)

# Envio do email
server.sendmail(remetente, destinatarios, mensagem.as_string())

## Páginas do site

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")
    
@app.route("/portfolio")
def portifolio ():
    return render_template("portfolio.html")

@app.route("/curriculo")
def curriculo ():
    return render_template("curriculo.html")

## Parte da página dinâmica com raspagem do BBC 

@app.route("/dw")
def dw ():
    return render_template("dw.html")

