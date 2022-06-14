from datetime import datetime, timedelta, date
from urllib import response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from .forms import LoginForm, SignUpForm, User_register, UserUpdateForm, IntegrationSettingsForm, PasswordChangeForm
from django import template, views
from django.urls import reverse
from .models import IntegrationSettings, Integrations
from django.contrib import messages
from .decorators import allowedUsers
from django.contrib.auth import update_session_auth_hash
import random
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from .tasks import integrationTask
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule
from .views_support import *
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


@login_required(login_url = "/login/")
def history(request, id):
    integration = Integrations.objects.get(id = id)
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    lines = []
    lines.append("Datetime integration : " + str(integration.date_time))
    lines.append("Status : " + integration.status)
    lines.append("Description : " + integration.description)
    lines.append(" ")
    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='Log.pdf')


def login(request):
    if request.user.is_authenticated:
        return redirect("/home")
    formLogin = LoginForm(request.POST or None)
    msg = None
    if request.method == "POST":
        if formLogin.is_valid():
            username = formLogin.cleaned_data.get("username")
            password = formLogin.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("/home")
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
    return render(request, "accounts/user_login.html", {"formLogin" : formLogin, "msg" : msg})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url = "/login/")
def index(request):
    is_admin = is_admin_test(request)
    nbr_intrg = Integrations.objects.all().count()
    nbr_intrg_success = Integrations.objects.filter(status='success').count()
    nbr_intrg_erreur = Integrations.objects.filter(status='erreur').count()
    nbr_intrg_automatic = Integrations.objects.filter(type='automatic').count()
    nbr_intrg_manual = Integrations.objects.filter(type='manual').count()
    jan_nbr_intg = Integrations.objects.filter(date_time__month='01').count()
    feb_nbr_intg = Integrations.objects.filter(date_time__month='02').count()
    mar_nbr_intg = Integrations.objects.filter(date_time__month='03').count()
    apr_nbr_intg = Integrations.objects.filter(date_time__month='04').count()
    may_nbr_intg = Integrations.objects.filter(date_time__month='05').count()
    jun_nbr_intg = Integrations.objects.filter(date_time__month='06').count()
    jul_nbr_intg = Integrations.objects.filter(date_time__month='07').count()
    aug_nbr_intg = Integrations.objects.filter(date_time__month='08').count()
    sep_nbr_intg = Integrations.objects.filter(date_time__month='09').count()
    oct_nbr_intg = Integrations.objects.filter(date_time__month='10').count()
    nov_nbr_intg = Integrations.objects.filter(date_time__month='11').count()
    dec_nbr_intg = Integrations.objects.filter(date_time__month='12').count()

    jan_nbr_intg_success = Integrations.objects.filter(date_time__month='01').filter(status='success').count()
    feb_nbr_intg_success = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='02').filter(status='success').count()
    mar_nbr_intg_success = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='03').filter(status='success').count()
    apr_nbr_intg_success = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='04').filter(status='success').count()
    may_nbr_intg_success = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='05').filter(status='success').count()
    jun_nbr_intg_success = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='06').filter(status='success').count()
    jul_nbr_intg_success = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='07').filter(status='success').count()
    aug_nbr_intg_success = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='08').filter(status='success').count()
    sep_nbr_intg_success = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='09').filter(status='success').count()
    oct_nbr_intg_success = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='10').filter(status='success').count()
    nov_nbr_intg_success = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='11').filter(status='success').count()
    dec_nbr_intg_success = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='12').filter(status='success').count()

    jan_nbr_intg_erreur = Integrations.objects.filter(date_time__month='01').filter(status='erreur').count()
    feb_nbr_intg_erreur = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='02').filter(status='erreur').count()
    mar_nbr_intg_erreur = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='03').filter(status='erreur').count()
    apr_nbr_intg_erreur = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='04').filter(status='erreur').count()
    may_nbr_intg_erreur = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='05').filter(status='erreur').count()
    jun_nbr_intg_erreur = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='06').filter(status='erreur').count()
    jul_nbr_intg_erreur = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='07').filter(status='erreur').count()
    aug_nbr_intg_erreur = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='08').filter(status='erreur').count()
    sep_nbr_intg_erreur = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='09').filter(status='erreur').count()
    oct_nbr_intg_erreur = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='10').filter(status='erreur').count()
    nov_nbr_intg_erreur = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='11').filter(status='erreur').count()
    dec_nbr_intg_erreur = Integrations.objects.filter(date_time__month__gte='1', date_time__month__lte='12').filter(status='erreur').count()

    
    settings =IntegrationSettings.objects.get(id = 1)
    date = dateNextIntegration()
        
    context = {'segment': 'index', "is_admin" : is_admin, "nbr_intrg": nbr_intrg, "nbr_intrg_automatic": nbr_intrg_automatic, "nbr_intrg_manual": nbr_intrg_manual, "nbr_intrg_success": nbr_intrg_success, "nbr_intrg_erreur": nbr_intrg_erreur, 'settings': settings, 'date': date, 'jan_nbr_intg': jan_nbr_intg, 'feb_nbr_intg': feb_nbr_intg, 'mar_nbr_intg': mar_nbr_intg, 'apr_nbr_intg': apr_nbr_intg, 'may_nbr_intg': may_nbr_intg, 'jun_nbr_intg': jun_nbr_intg, 'jul_nbr_intg': jul_nbr_intg, 'aug_nbr_intg': aug_nbr_intg, 'sep_nbr_intg': sep_nbr_intg, 'oct_nbr_intg': oct_nbr_intg, 'nov_nbr_intg': nov_nbr_intg, 'dec_nbr_intg': dec_nbr_intg, 
    
    'jan_nbr_intg_success': jan_nbr_intg_success, 'feb_nbr_intg_success': feb_nbr_intg_success, 'mar_nbr_intg_success': mar_nbr_intg_success, 'apr_nbr_intg_success': apr_nbr_intg_success, 'may_nbr_intg_success': may_nbr_intg_success, 'jun_nbr_intg_success': jun_nbr_intg_success, 'jul_nbr_intg_success': jul_nbr_intg_success, 'aug_nbr_intg_success': aug_nbr_intg_success, 'sep_nbr_intg_success': sep_nbr_intg_success, 'oct_nbr_intg_success': oct_nbr_intg_success, 'nov_nbr_intg_success': nov_nbr_intg_success, 'dec_nbr_intg_success': dec_nbr_intg_success,
    
    'jan_nbr_intg_erreur': jan_nbr_intg_erreur, 'feb_nbr_intg_erreur': feb_nbr_intg_erreur, 'mar_nbr_intg_erreur': mar_nbr_intg_erreur, 'apr_nbr_intg_erreur': apr_nbr_intg_erreur, 'may_nbr_intg_erreur': may_nbr_intg_erreur, 'jun_nbr_intg_erreur': jun_nbr_intg_erreur, 'jul_nbr_intg_erreur': jul_nbr_intg_erreur, 'aug_nbr_intg_erreur': aug_nbr_intg_erreur, 'sep_nbr_intg_erreur': sep_nbr_intg_erreur, 'oct_nbr_intg_erreur': oct_nbr_intg_erreur, 'nov_nbr_intg_erreur': nov_nbr_intg_erreur, 'dec_nbr_intg_erreur': dec_nbr_intg_erreur}
    
    return render(request,"home/index.html", context)


@login_required(login_url = "/login/")
def integration(request):
    is_admin = is_admin_test(request)
    segment ='integration'
    settings =IntegrationSettings.objects.get(id = 1)
    date = dateNextIntegration()
    integrations = Integrations.objects.all()
    
    context = {'integrations' : integrations, 'date' : date, "segment" : segment, 'settings' : settings, "is_admin" : is_admin}
    return render(request, "home/integration.html", context )





# @login_required(login_url = "/login/")
# def historys(request):
#     is_admin = is_admin_test(request)
#     segment ='history'
#     context = {"segment" : segment, "is_admin" : is_admin}
#     return render(request, "home/history.html", context )


@login_required(login_url = "/login/")
def profile(request):
    is_admin = is_admin_test(request)
    segment = 'profile'
    msg = None
    msg_change_password = None
    success = False
    success_change_password = False
    current_user = request.user
    if request.method == 'POST':
        if request.POST.get('username'):
            formUserUpdate = UserUpdateForm(request.POST, instance = request.user)
            formPasswordChange = PasswordChangeForm(request.user)
            if formUserUpdate.is_valid():
                formUserUpdate.save()
                success = True
                context = {"formPasswordChange" : formPasswordChange, "formUserUpdate" : formUserUpdate, "msg" : msg, "success" : success, "segment" : segment, 'current_user' : current_user, "is_admin" : is_admin}
                return render(request, "home/profile.html", context )
            else:
                msg = 'Form is not valid'
            context = {"formPasswordChange" : formPasswordChange, "formUserUpdate" : formUserUpdate, "msg" : msg, "success" : success, "segment" : segment, 'current_user' : current_user, "is_admin" : is_admin}
            return render(request, "home/profile.html", context)
        elif request.POST.get('new_password1'):
            formUserUpdate = UserUpdateForm(instance = request.user)
            formPasswordChange = PasswordChangeForm(request.user, request.POST)
            if formPasswordChange.is_valid():
                user = formPasswordChange.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                msg_chang = "Your password was successfully updated!"
                success_change_password = True
                context = {"formPasswordChange" : formPasswordChange, "formUserUpdate" : formUserUpdate, "msg" : msg, "success" : success, "segment" : segment, 'current_user' : current_user, "success_change_password" : success_change_password, "msg_change_password" : msg_change_password, "msg_chang" : msg_chang, "is_admin" : is_admin }
                return render(request, 'home/profile.html', context )
            else:
                msg_change_password = True
                msg_chang = "Please correct the error below "
                messages.error(request, 'Please correct the error below.')
            context = {"formPasswordChange" : formPasswordChange, "formUserUpdate" : formUserUpdate, "msg" : msg, "success" : success, "segment" : segment, 'current_user' : current_user,"msg_change_password" : msg_change_password, "msg_chang" : msg_chang, "is_admin" : is_admin}
            return render(request, 'home/profile.html', context)
    else:
        formUserUpdate = UserUpdateForm(instance = request.user)
        formPasswordChange = PasswordChangeForm(request.user)
        context = {'formPasswordChange' : formPasswordChange, "msg": msg, "segment": segment, "success" : success, "formUserUpdate" : formUserUpdate, 'current_user' : current_user, "is_admin" : is_admin }
        return render(request, 'home/profile.html', context)


def testlol(request):
    msg = None
    success = None
    if request.method == "POST":
        if request.POST.get('email'):
            formUserAdd = User_register(request.POST)
            if formUserAdd.is_valid():
                formUserAdd.save()
                success = 'The user was successfully added'
                context = {"formUserAdd" : formUserAdd, "success" : success}
                return render(request, "home/admin/lol.html", context)
            else:
                msg1 = 'Form is not valid'
                context = {"formUserAdd" : formUserAdd, "success" : success, "msg1" : msg1}
                return render(request, "home/admin/lol.html", context)
        else:
            context = {"formUserAdd" : formUserAdd, "msg" : msg, "success" : success}
            return render(request, "home/admin/lol.html", context)
    else:
        formUserAdd = User_register()
        context = {"formUserAdd" : formUserAdd, "msg" : msg, "success" : success}
        return render(request, "home/admin/lol.html", context)


def test5(request):
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
    context = {"form": form, "msg": msg, "success": success}
    return render(request, "accounts/register.html", context )



@login_required(login_url = "/login/")
@allowedUsers(allowedGroups = ['admin'])
def settings(request):
    users = users_pagination(request, 8)
    is_admin = is_admin_test(request)
    msg = None
    msg_settings = None
    success = None
    success_settings = None
    segment = 'settings'
    settings = IntegrationSettings.objects.get(id = 1)
    form_settings = IntegrationSettingsForm( instance = settings)
    formUserAdd = User_register()
    if request.method == "POST":
        if request.POST.get('email'):
            formUserAdd = User_register(request.POST)
            if formUserAdd.is_valid():
                formUserAdd.save()
                success = 'The user was successfully added'
                users = users_pagination(request,8)
                context = {"formUserAdd" : formUserAdd, "success" : success, "segment" : segment, "users" : users, 'form_settings' : form_settings, "is_admin" : is_admin}
                return render(request, "home/admin/settings.html", context)
            else:
                msg1 = 'Form is not valid'
                context = {"formUserAdd" : formUserAdd, "success" : success, "segment" : segment, "users" : users, 'form_settings' : form_settings, "is_admin" : is_admin, "msg1" : msg1}
                return render(request, "home/admin/settings.html", context)
        elif request.POST.get('frequenc'):
            form_settings = IntegrationSettingsForm(request.POST, instance = settings)
            if form_settings.is_valid():
                form_settings.save()
                scheduleIntegrationTask()
                success_settings = 'The modification has successfully been saved'
                context = {"formUserAdd" : formUserAdd, "msg" : msg, "success" : success, "segment" : segment, 'success_settings' : success_settings, "users" : users, 'form_settings' : form_settings, "is_admin" : is_admin}
                return render(request, "home/admin/settings.html", context)
            else:
                msg_settings = 'Form is not valid'
                context = {"formUserAdd" : formUserAdd, "msg" : msg, "success" : success, "segment" : segment, 'msg_settings' : msg_settings, "users" : users, 'form_settings' : form_settings, "is_admin" : is_admin}
                return render(request, "home/admin/settings.html", context)
        else:
            context = {"formUserAdd" : formUserAdd, "msg" : msg, "success" : success, "segment" : segment, "users" : users, 'form_settings' : form_settings, "is_admin" : is_admin}
            return render(request, "home/admin/settings.html", context)
    else:
        form_settings = IntegrationSettingsForm(instance = settings)
        context = {"formUserAdd" : formUserAdd, "msg" : msg, "success" : success, "segment" : segment , "users" : users, 'form_settings' : form_settings, "is_admin" : is_admin}
        return render(request, "home/admin/settings.html", context)



@login_required(login_url="/login/")
def settings_user_update(request, id):
    users = users_pagination(request,6)
    is_admin = is_admin_test(request)
    msg = None
    success = None
    segment = 'settings'
    user = User.objects.get(id = id)
    formUserUpdate = UserUpdateForm(instance = user)
    settings = IntegrationSettings.objects.get(id = 1)
    form_settings = IntegrationSettingsForm( instance = settings)
    if request.method == "POST":
        if request.POST.get('username'):
            formUserUpdate = UserUpdateForm(request.POST, instance = user)
            if formUserUpdate.is_valid():
                formUserUpdate.save()
                success = 'success'
                context = {"formUserUpdate": formUserUpdate, "msg": msg, "success": success,"segment": segment, "users" : users,'form_settings' : form_settings, "is_admin" : is_admin}
                return render(request, "home/admin/settings_user_update.html", context)
            else:
                msg = 'Form is not valid'
        elif request.POST.get('frequenc'):
            form_settings = IntegrationSettingsForm(request.POST, instance = settings)
            if form_settings.is_valid():
                form_settings.save()
                scheduleIntegrationTask()
                success_settings = 'The modification has successfully been saved'
                context = {"formUserUpdate": formUserUpdate, "msg": msg, "success": success,"segment": segment,'success_settings' : success_settings, "users" : users,'form_settings' : form_settings, "is_admin" : is_admin}
                return render(request, "home/admin/settings_user_update.html", context)
            else:
                msg_settings = 'Form is not valid'
                context = {"formUserUpdate": formUserUpdate, "msg": msg, "success": success,"segment": segment ,'msg_settings' : msg_settings, "users" : users, 'form_settings' : form_settings, "is_admin" : is_admin}
                return render(request, "home/admin/settings_user_update.html", context)
    else:
        formUserUpdate = UserUpdateForm(instance=user)
        form_settings = IntegrationSettingsForm(instance=settings)
        context = {"formUserUpdate": formUserUpdate, "msg": msg, "success": success,"segment": segment , "users" : users, 'form_settings' : form_settings, "is_admin" : is_admin}
        return render(request, "home/admin/settings_user_update.html", context)



def handel404(request, exception):
    return render(request, 'home/page-404.html', status=404)

def handel403(request, exception):
    return render(request, 'home/page-403.html', status=404)

def handel500(request):
    return render(request, 'home/page-500.html', status=404)








# function test
def test(request):
    integrationTask.delay("lol")
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
            task = 'app.tasks.integrationTask'
        )

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



def test3(request):
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
    context = {"form": form, "msg": msg, "success": success}
    return render(request, "accounts/register.html", context )
# the end functions test


