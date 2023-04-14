import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


load_dotenv()
TOKEN = os.getenv('TOKEN')


email_remetente = ""
senha_remetente = TOKEN
assunto = "Recuperação de senha"


def send_email_recovery(email_destinatario, codigo):
    corpo = "Seu código de recuperação é: " + codigo
    msg = MIMEMultipart()
    msg['From'] = email_remetente
    msg['To'] = email_destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_remetente, senha_remetente)
        text = msg.as_string()
        server.sendmail(email_remetente, email_destinatario, text)
    finally:
        server.quit()
