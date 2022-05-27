import time
from celery import shared_task
from click import echo
from django.template.loader import render_to_string
from django.core.mail import EmailMessage



@shared_task
def test_func():
    a=True
    # while a:
    #     print("This prints once a minute.")
    #     time.sleep(6)

    print('lol')
    # print(' started to sleep')
    # time.sleep(5)
    # print("wake up from sleep")
    
    template = render_to_string('home/email.html')
    email=EmailMessage(
        'subject',
        template,
        'pferendezvous@gmail.com',
        ['elmehdi.elhebaby@gmail.com'],
    )
    email.fail_silently=False
    email.send()
    return



@shared_task
def test_func2():
    print('lol')
    
    template = render_to_string('home/email.html')
    email=EmailMessage(
        'subject',
        template,
        'pferendezvous@gmail.com',
        ['elmehdi.elhebaby@gmail.com'],
    )
    email.fail_silently=False
    email.send()
    return


# @task
# def send_scheduled_emails():
#     pass