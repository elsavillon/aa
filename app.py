import requests
from bs4 import BeautifulSoup
import unicodedata
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template

def remove_acentos(texto):
    return ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )

def manchetes_dw():
    url = "https://www.dw.com/pt-br/manchetes/headlines-pt-br"
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    lista_dw = []

    # A DW usa links internos com títulos visíveis
    for a in soup.find_all("a", href=True):
        titulo = a.get_text(strip=True)
        link = a["href"]

        if not titulo:
            continue

        if link.startswith("/"):
            link = "https://www.dw.com" + link

        if "/pt-br/" not in link:
            continue

        lista_dw.append([
            remove_acentos(titulo),
            link
        ])

    # Remove duplicatas mantendo ordem
    vistos
