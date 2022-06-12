import time
from celery import shared_task
from click import echo
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import random
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from .models import IntegrationSettings, Integrations
from project import settings
# from django.core import mail
from django.core.mail import get_connection, send_mail


@shared_task
def integrationTask():
    template = render_to_string('home/email.html')
    setting=IntegrationSettings.objects.get(id=1)
    gmail_user = setting.email_conix_reporting
    gmail_pwd  = setting.email_conix_reporting_psw
    gmail_reporting  = setting.email_reporting

    # methode 1
    # send_mail(
    #     subject = 'Arkeos App Integration',
    #     message = template,
    #     from_email = 'pferendezvous@gmail.com',
    #     recipient_list = ['elmehdi.elhebaby@gmail.com'],
    #     auth_user = gmail_user,
    #     auth_password = gmail_pwd,
    #     fail_silently = False,
    #     html_message = template,
    #     )

    # methode 2
    connection = get_connection(
        username=gmail_user,
        password=gmail_pwd,
        fail_silently=False
        )
    email = EmailMessage(
        subject='subject',
        body=template,
        to=[gmail_reporting],
        connection=connection
        )
    email.content_subtype = 'html'
    file = open("app/Projet Final/data.txt", "r")
    email.attach("Log.txt",file.read(),'text/plain')
    email.fail_silently = False
    email.send()
    email.attach("Log.txt",file.read(),'text/plain')
    connection.close()
    return 


# @task
# def send_scheduled_emails():
#     pass