from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


def email_connect():
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587
    smtp_username = 'devtudo_avaliacao360@outlook.com'
    smtp_password = 'devtudo2023!'

    smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
    smtp_connection.starttls()

    smtp_connection.login(smtp_username, smtp_password)

    return smtp_connection

export = email_connect

def send_email(smtp_connection, destinatario, assunto, mensagem):
    smtp_username = 'devtudo_avaliacao360@outlook.com'

    email_message = MIMEMultipart()
    email_message['From'] = smtp_username
    email_message['To'] = destinatario
    email_message['Subject'] = assunto
    email_message.attach(MIMEText(mensagem, 'html'))

    smtp_connection.send_message(email_message)

export = send_email