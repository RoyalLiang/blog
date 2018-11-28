from django.core.mail import send_mail
from lzyblog.settings import EMAIL_FROM


def send_email(email, name, message):
    email_title = message
    email_body = '您的好友' + '<' + name + '>' + '给您分享了网站:http://127.0.0.1:8000'
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
    if send_status:
        pass
