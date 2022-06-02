from datetime import datetime, timedelta, date
from urllib import response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
# from numpy import insert
from .forms import LoginForm, SignUpForm, User_register, UserUpdateForm, IntegrationSettingsForm, PasswordChangeForm
from django import template
from django.urls import reverse
from .models import IntegrationSettings, Integrations
from django.contrib import messages
from .decorators import allowedUsers
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from .tasks import test_func
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule
# import datetime


def test(request):
    test_func.delay("lol")
    return HttpResponse("Done")









def success(request):
    template = render_to_string('home/email.html')
    email=EmailMessage(
        'subject',
        template,
        'pferendezvous@gmail.com',
        ['elmehdi.elhebaby@gmail.com'],
    )
    email.fail_silently=False
    email.send()
    # project=Project.objects.get()
    return redirect("/integration")



def login(request):
    if request.user.is_authenticated:
        return redirect("/home")
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("/home")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
    return render(request, "accounts/user_login.html", {"form": form, "msg": msg})


def logout_view(request):
    logout(request)
    return redirect('/login/')





@login_required(login_url="/login/")
def index(request):
    is_admin = is_admin_test(request)
    context = {'segment': 'index',"is_admin" : is_admin}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template
        html_template = loader.get_template('home/' + load_template +'.html')
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))
    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def integration(request):
    is_admin = is_admin_test(request)
    segment='integration'
    settings=IntegrationSettings.objects.get(id=1)
    date = dateNextIntegration()
    integrations=Integrations.objects.all()
    return render(request,"home/integration.html",{'integrations': integrations, 'date': date, "segment": segment, 'settings' : settings, "is_admin" : is_admin})



@login_required(login_url="/login/")
def history(request, id):
    is_admin = is_admin_test(request)
    segment='history'
    integration=Integrations.objects.get(id = id)
    return render(request,"home/history_id.html",{'integration' : integration, "segment": segment, "is_admin" : is_admin})


@login_required(login_url="/login/")
def historys(request):
    is_admin = is_admin_test(request)
    segment='history'
    return render(request,"home/history.html",{"segment": segment, "is_admin" : is_admin})


@login_required(login_url="/login/")
def profile(request):
    is_admin = is_admin_test(request)
    segment='profile'
    msg = None
    msg_change_password = None
    success = False
    success_change_password = False
    current_user = request.user
    if request.method == 'POST':
        if request.POST.get('username'):
            form = UserUpdateForm(request.POST, instance=request.user)
            formPasswordChange = PasswordChangeForm(request.user)
            if form.is_valid():
                form.save()
                success = True
                return render(request, "home/profile.html", {"formPasswordChange": formPasswordChange,"form": form, "msg": msg, "success": success,"segment": segment, 'current_user' : current_user, "is_admin":is_admin
                })
            else:
                msg = 'Form is not valid'
            return render(request, "home/profile.html", {"formPasswordChange": formPasswordChange,"form": form, "msg": msg, "success": success,"segment": segment, 'current_user' : current_user, "is_admin":is_admin
            })
        elif request.POST.get('new_password1'):
            form = UserUpdateForm(instance=request.user)
            formPasswordChange = PasswordChangeForm(request.user, request.POST)
            if formPasswordChange.is_valid():
                user = formPasswordChange.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Your password was successfully updated!')
                msg_chang= "Your password was successfully updated!"
                success_change_password=True
                return render(request, 'home/profile.html', {"formPasswordChange": formPasswordChange,"form": form, "msg": msg, "success": success,"segment": segment, 'current_user' : current_user, "success_change_password" : success_change_password,"msg_change_password":msg_change_password, "msg_chang" : msg_chang, "is_admin":is_admin
                })
            else:
                msg_change_password = True
                msg_chang = "Please correct the error below "
                messages.error(request, 'Please correct the error below.')
            return render(request, 'home/profile.html', {"formPasswordChange": formPasswordChange,"form": form, "msg": msg, "success": success,"segment": segment, 'current_user' : current_user,"msg_change_password":msg_change_password, "msg_chang" : msg_chang, "is_admin":is_admin
            })
    else:
        form = UserUpdateForm(instance=request.user)
        formPasswordChange = PasswordChangeForm(request.user)
        return render(request, 'home/profile.html', {
            'formPasswordChange': formPasswordChange, "msg": msg, "segment": segment,"success": success, "form": form, 'current_user' : current_user, "is_admin":is_admin
        })


@login_required(login_url="/login/")
@allowedUsers(allowedGroups=['admin'])
def settings(request):
    users = pages(request,7)
    is_admin = is_admin_test(request)
    msg = None
    msg_settings = None
    success = None
    success_settings = None
    segment='settings'
    settings=IntegrationSettings.objects.get(id=1)
    form_settings = IntegrationSettingsForm( instance=settings)
    if request.method == "POST":
        if request.POST.get('email'):
            form = User_register(request.POST)
            # form.username='user'
            if form.is_valid():
                form.save()
                success = 'The user was successfully added'
                users = pages(request,7)
                return render(request, "home/admin/settings.html",{"form": form, "success": success,"segment": segment, "users" : users,'form_settings' : form_settings, "is_admin" : is_admin})
            else:
                msg1 = 'Form is not valid'
                return render(request, "home/admin/settings.html",{"form": form, "success": success,"segment": segment, "users" : users,'form_settings' : form_settings, "is_admin" : is_admin, "msg1" : msg1})
        elif request.POST.get('frequenc'):
            form = User_register()
            form_settings = IntegrationSettingsForm(request.POST, instance=settings)
            if form_settings.is_valid():
                form_settings.save()
                # methood 1
                # if(settings.type == 'automatic'):
                #     datetime = dateNextIntegration()
                #     integration_schedule(datetime)
                # if(settings.type == 'manual'):
                #     # anuuler tout les integration schedule
                #     pass
                periodic_task = PeriodicTask.objects.get(name='schedule_mail_task_2')
                if(settings.type == 'automatic'):
                    periodic_task.enabled = True
                    interval = IntervalSchedule.objects.get(id=periodic_task.interval_id)
                    # crontab.minute = settings.time.minute
                    # crontab.hour = settings.time.hour
                    # periodic_task.crontab_id = NULL
                    # crontab.save()
                    if(settings.frequenc == 'day'):
                        interval.every = 1
                    if(settings.frequenc == 'two_days'):
                        interval.every = 2
                    if(settings.frequenc == 'week'):
                        interval.every = 7
                    interval.save()
                    # periodic_task.start_time = settings.time
                    # dd= str(date.today())+" "+str(settings.time)
                    periodic_task.start_time = datetime(date.today().year, date.today().month, date.today().day, settings.time.hour, settings.time.minute, 00, 000000)
                    periodic_task.save()
                if(settings.type == 'manual'):
                    periodic_task.enabled = False
                    periodic_task.save()
                success_settings = 'The modification has successfully been saved'
                # return HttpResponse(crontab)
                return render(request, "home/admin/settings.html",{"form": form, "msg": msg, "success": success,"segment": segment,'success_settings' : success_settings, "users" : users,'form_settings' : form_settings, "is_admin" : is_admin})
            else:
                msg_settings = 'Form is not valid'
                return render(request, "home/admin/settings.html", {"form": form, "msg": msg, "success": success,"segment": segment ,'msg_settings' : msg_settings, "users" : users, 'form_settings' : form_settings, "is_admin" : is_admin})
        else:
            return render(request, "home/admin/settings.html", {"form": form, "msg": msg, "success": success,"segment": segment , "users" : users, 'form_settings' : form_settings, "is_admin" : is_admin})
    else:
        form = User_register()
        form_settings = IntegrationSettingsForm(instance=settings)
        return render(request, "home/admin/settings.html", {"form": form, "msg": msg, "success": success,"segment": segment , "users" : users, 'form_settings' : form_settings, "is_admin" : is_admin})




def integration_schedule(datetime):
    settings=IntegrationSettings.objects.get(id=1)
    if(settings.frequenc == 'day'):
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute=settings.time.minute,
            hour=settings.time.hour,
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
        )
    elif(settings.frequenc == 'two_days'):
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute=settings.time.minute,
            hour=settings.time.hour,
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
        )
    elif(settings.frequenc == 'week'):
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute=settings.time.minute,
            hour=settings.time.hour,
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
        )
    task = PeriodicTask.objects.create(
            crontab = schedule,
            name = "schedule_mail_task_"+ str(random.randint(0,99999)),
            task = 'app.tasks.test_func'
        )



def dateNextIntegration():
    periodic_task = PeriodicTask.objects.get(name='schedule_mail_task_1')
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
        if (k==1):
            return date2 + timedelta(1)
        else:
            return date2
    elif(settings.frequenc == 'two_days'):
        return date + timedelta(2)
    elif(settings.frequenc == 'week'):
        return date + timedelta(days=7)






# def dateNextIntegration():
#     request = IntegrationSettings.objects.get(id=1)
#     if(request.frequenc == 'day'):
#         return datetime.today()
#     elif(request.frequenc == 'two_days'):
#         return request.update_date.date() + timedelta(2)
#     elif(request.frequenc == 'week'):
#         return request.update_date.date() + timedelta(days=7)

def test3(request):
    periodic_task = PeriodicTask.objects.get(name='schedule_mail_task_2')
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
    k=1
    if(request.frequenc == 'day'):
        if (k==1):
            return date + timedelta(1)
        else:
            return date
    elif(request.frequenc == 'two_days'):
        return date.date() + timedelta(2)
    elif(request.frequenc == 'week'):
        return date.date() + timedelta(days=7)
    # return HttpResponse(date2)







@login_required(login_url="/login/")
def settings_user_update(request, id):
    users = pages(request,6)
    is_admin = is_admin_test(request)
    msg = None
    success = None
    segment='settings'
    user=User.objects.get(id=id)
    form = UserUpdateForm(instance=user)
    settings=IntegrationSettings.objects.get(id=1)
    form_settings = IntegrationSettingsForm(request.POST, instance=settings)
    if request.method == "POST":
        if request.POST.get('username'):
            form = UserUpdateForm(request.POST,instance=user)
            if form.is_valid():
                form.save()
                success = 'success'
                return render(request, "home/admin/settings.html",{"form": form, "msg": msg, "success": success,"segment": segment, "users" : users,'form_settings' : form_settings, "is_admin" : is_admin})
            else:
                msg = 'Form is not valid'
        elif request.POST.get('frequenc'):
            form = User_register(request.POST)
            form_settings = IntegrationSettingsForm(request.POST, instance=settings)
            if form_settings.is_valid():
                form_settings.save()
                periodic_task = PeriodicTask.objects.get(name='schedule_mail_task_2')
                if(settings.type == 'automatic'):
                    periodic_task.enabled = True
                    interval = IntervalSchedule.objects.get(id=periodic_task.interval_id)
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
                success_settings = 'The modification has successfully been saved'
                return render(request, "home/admin/settings.html",{"form": form, "msg": msg, "success": success,"segment": segment,'success_settings' : success_settings, "users" : users,'form_settings' : form_settings, "is_admin" : is_admin})
            else:
                msg_settings = 'Form is not valid'
                return render(request, "home/admin/settings.html", {"form": form, "msg": msg, "success": success,"segment": segment ,'msg_settings' : msg_settings, "users" : users, 'form_settings' : form_settings, "is_admin" : is_admin})
        
    else:
        form = UserUpdateForm(instance=user)
        form_settings = IntegrationSettingsForm(instance=settings)
        return render(request, "home/admin/settings_user_update.html", {"form": form, "msg": msg, "success": success,"segment": segment , "users" : users, 'form_settings' : form_settings, "is_admin" : is_admin})




@login_required(login_url="/login/")
def register(request):
    msg = None
    success = False
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            msg = 'User created - please <a href="/login">login</a>.'
            success = True
            return redirect("/profile")
        else:
            msg = 'Form is not valid'
    else:
        form = SignUpForm()
    return render(request, "accounts/register.html", {"form": form, "msg": msg, "success": success})


def handel404(request, exception):
    return render(request,'home/page-404.html',status=404)

def handel403(request, exception):
    return render(request,'home/page-403.html',status=404)

def handel500(request):
    return render(request,'home/page-500.html',status=404)







def is_admin_test(request):
    group = None
    allowedGroups=["admin"]
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name
    if group in allowedGroups:
        return True
    else:
        return False


def pages(request,a):
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

