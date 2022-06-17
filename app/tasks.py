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
from django.core.mail import get_connection, send_mail
from app.Projet_Final.connectVantage import connectVantage
from app.Projet_Final.connectSQL import connectSQL
from app.Projet_Final.synchSage import synchSage
from django.core.mail.backends.smtp import EmailBackend


@shared_task
def integrationTask():

        
    # Se connecter à vantage
    # head = connectVantage()
    # # Se connecter à SQL
    # conn = connectSQL()
    # # Synchroniser Invoice
    # synchSage(head, conn)
    # # Se deconnecter de SQL
    # conn.close()

    template = render_to_string('home/email.html')
    setting=IntegrationSettings.objects.get(id=1)
    gmail_reporting  = setting.email_reporting
    smtp_server  = setting.smtp_server
    smtp_port  = setting.smtp_port
    smtp_user = setting.smtp_user
    smtp_password  = setting.smtp_password

    connection = EmailBackend(
        host=smtp_server,
        port=smtp_port,
        password=smtp_password,
        username=smtp_user,
        use_tls=True,
        fail_silently=False
    )

    email = EmailMessage(
        subject='subject',
        body=template,
        to=[gmail_reporting],
        connection=connection
        )
    email.content_subtype = 'html'
    file = open("app/Projet_Final/data.txt", "r")
    email.attach("Log.txt",file.read(),'text/plain')
    email.fail_silently = False
    email.send()
    email.attach("Log.txt",file.read(),'text/plain')
    connection.close()
    
    return 


# @task
# def send_scheduled_emails():
#     pass