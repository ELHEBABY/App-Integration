from datetime import datetime, timedelta, date
from .models import IntegrationSettings, Integrations
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def is_admin_test(request):
    group = None
    allowedGroups = ["admin"]
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    if group in allowedGroups:
        return True
    else:
        return False


def dateNextIntegration():
    periodic_task = PeriodicTask.objects.get(name='schedule_integration_task')
    settings = IntegrationSettings.objects.get(id=1)
    if(periodic_task.last_run_at != None):
        date = periodic_task.last_run_at.date()
    else:
        date = periodic_task.date_changed.date()
    present = datetime.now().date()
    if(date < present):
        date2 = present
    else:
        date2 = date
    present_time = datetime.now().time()
    time = settings.time

    if(present_time < time):
        k = 0
    else:
        k = 1
    if(settings.frequenc == 'day'):
        if (k == 1):
            return date2 + timedelta(1)
        else:
            return date2
    elif(settings.frequenc == 'two_days'):
        return date + timedelta(2)
    elif(settings.frequenc == 'week'):
        return date + timedelta(days = 7)


def users_pagination(request, a):
    user = User.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(user, a)
    try:
        users = paginator.page(page)
        return users
    except PageNotAnInteger:
        users = paginator.page(1)
        return users
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
        return users


def scheduleIntegrationTask():
    periodic_task = PeriodicTask.objects.get(name = 'schedule_integration_task')
    settings = IntegrationSettings.objects.get(id = 1)
    if(settings.type == 'automatic'):
        periodic_task.enabled = True
        interval = IntervalSchedule.objects.get(id = periodic_task.interval_id)
        if(settings.frequenc == 'day'):
            interval.every = 1
        if(settings.frequenc == 'two_days'):
            interval.every = 2
        if(settings.frequenc == 'week'):
            interval.every = 7
        interval.save()
        periodic_task.start_time = datetime(date.today().year, date.today().month, date.today().day, settings.time.hour, settings.time.minute, 00, 000000)
        periodic_task.save()
    if(settings.type == 'manual'):
        periodic_task.enabled = False
        periodic_task.save()


# def dateNextIntegration():
#     request = IntegrationSettings.objects.get(id=1)
#     if(request.frequenc == 'day'):
#         return datetime.today()
#     elif(request.frequenc == 'two_days'):
#         return request.update_date.date() + timedelta(2)
#     elif(request.frequenc == 'week'):
#         return request.update_date.date() + timedelta(days=7)