import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(destinatario, assunto, mensagem):
    email_devtudo = 'devtudo_avaliacao360@outlook.com'

    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587
    smtp_username = 'devtudo_avaliacao360@outlook.com'
    smtp_password = 'devtudo2023!'

    email_message = MIMEMultipart()
    email_message['From'] = email_devtudo
    email_message['To'] = destinatario
    email_message['Subject'] = assunto
    email_message.attach(MIMEText(mensagem, 'html'))

    smtp_connection = smtplib.SMTP(smtp_server, smtp_port)
    smtp_connection.starttls()

    smtp_connection.login(smtp_username, smtp_password)

    smtp_connection.send_message(email_message)

    smtp_connection.quit()


export = send_email