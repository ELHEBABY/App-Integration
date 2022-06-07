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
# from .views import integration_schedule, dateNextIntegration
# from django.core import mail

from django.core.mail import send_mail


@shared_task
def integrationTask():
    template = render_to_string('home/email.html')
    setting=IntegrationSettings.objects.get(id=1)
    # settings.EMAIL_HOST_USER = 'elmehdi.elhebaby@gmail.com'

    gmail_user = setting.email_conix_reporting
    gmail_pwd  = setting.email_conix_reporting_psw

    # email.content_subtype = 'html'
    file = open("app/Projet Final/data.txt", "r")
    # email.attach("Log.txt",file.read(),'text/plain')
    # email.fail_silently=False
    # email.send()
    
    # message.attach("Log.txt",file.read(),'text/plain')
    send_mail(
        subject = 'Arkeos App Integration',
        message = template,
        from_email = 'pferendezvous@gmail.com',
        recipient_list = ['elmehdi.elhebaby@gmail.com'],
        auth_user = gmail_user,
        auth_password = gmail_pwd,
        fail_silently = False,
        )

    return 


# @task
# def send_scheduled_emails():
#     pass