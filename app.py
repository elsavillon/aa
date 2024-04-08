# -*- coding: utf-8 -*-

from flask import Flask, request, render_template
import requests
import os
from bs4 import BeautifulSoup
import smtplib

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

# Iniciar conexão com o servidor SMTP
smtp_server = "smtp-relay.brevo.com"
port = 587
email = os.environ["EMAIL_REMETENTE"]
password = os.environ["SMTP_PASSWORD"]

server = smtplib.SMTP(smtp_server, port)
server.starttls()  
server.login(email, password) 

# Título do email
titulo_email = "Destaques da Semana - Deutsch Welle"

# Preparando o objeto da mensagem
mensagem = MIMEMultipart()
mensagem["From"] = remetente
mensagem["To"] = ",".join(destinatarios)
mensagem["Subject"] = titulo_email
conteudo_html = MIMEText(html, "html")  # Adiciona a versão em HTML
mensagem.attach(conteudo_html)

# Envio do email
server.sendmail(remetente, destinatarios, mensagem.as_string())

# Dados para o email que será enviado:
remetente = "EMAIL_REMETENTE"
destinatarios = ["EMAIL_DESTINATARIOS"]

# Extrair manchetes e links
manchetes_links = manchetes_dw()

app = Flask(__name__)

## Páginas do site

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

