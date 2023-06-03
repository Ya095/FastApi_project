# Реализация отправки писем на почту
#---------------------------------
import smtplib
from email.message import EmailMessage
from celery import Celery
from src.config import SMTP_USER, SMTP_PASSWORD, REDIS_HOST, REDIS_PORT


SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 465

# тоже исп. redis для хранения задач (что бы не отправить дважды одно письмо одному и тому же)
cel = Celery('tasks', broker=f'redis://{REDIS_HOST}:{REDIS_PORT}')

# генерирует шаблон
def get_email_template(username: str):
    email = EmailMessage()
    email['Subject'] = 'Тестовый заголовок'
    email['From'] = SMTP_USER

    # для примера - отправка себе же
    email['To'] = SMTP_USER

    email.set_content(
        '<div>'
        f'<h2 style="color: red;">Здравствуйте, {username}, это тестовое письмо 😊</h2>'
        '<img src="https://s1.1zoom.ru/big0/697/Love_Night_Moon_Trees_Silhouette_Two_Dating_576752_1280x853.jpg"'
        '-management-dashboard-ui-design-template-suitable-designing-application-for-android-and-ios-clean-style-app'
        '-mobile-free-vector.jpg" width="600">'
        '</div>',
        subtype='html'
    )
    return email


# создание задачи (декаратор обязательно)
@cel.task
def sent_email_report(username: str):
    email = get_email_template(username)

    # подключаемся к серверу
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)