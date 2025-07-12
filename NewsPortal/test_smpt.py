import smtplib
from email.mime.text import MIMEText

smtp_server = 'smtp.yandex.ru'
port = 465
login = 'viktoriakasenceva95@yandex.ru'
password = 'mhfjiahjmpkumxug'  # подставь тут

msg = MIMEText('Тестовое письмо от Python')
msg['Subject'] = 'Проверка SMTP'
msg['From'] = login
msg['To'] = 'viktoriakasenceva95@gmail.com'  # например, viktoriakasenceva95@gmail.com

try:
    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
    print("Письмо успешно отправлено!")
except Exception as e:
    print(f"Ошибка: {e}")
