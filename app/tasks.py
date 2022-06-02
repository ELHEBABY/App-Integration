import time
from celery import shared_task
from click import echo
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import random
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from .models import IntegrationSettings, Integrations
# from .views import integration_schedule, dateNextIntegration



@shared_task
def test_func():
    template = render_to_string('home/email.html')
    settings=IntegrationSettings.objects.get(id=1)
    email=EmailMessage(
        'subject',
        template,
        'pferendezvous@gmail.com',
        [settings.email_reporting],
        # ['elmehdi.elhebaby@gmail.com'],
    )
    email.fail_silently=False
    email.send()
    return


# @task
# def send_scheduled_emails():
#     pass