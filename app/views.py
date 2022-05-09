import imp
from urllib import response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from numpy import insert
from .forms import LoginForm, SignUpForm, User_register, UserUpdateForm, IntegrationSettingsForm
from django import template
from django.urls import reverse
from .models import IntegrationSettings

def test(request):
    return render(request,"home/Oprofile.html")

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
    context = {'segment': 'index'}

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
    segment='integration'
    return render(request,"home/integration.html",{"segment": segment})



@login_required(login_url="/login/")
def history(request):
    segment='history'
    return render(request,"home/history.html",{"segment": segment})



@login_required(login_url="/login/")

def profile(request):
    segment='profile'
    msg = None
    success = False
    
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        # profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            success = True

            return redirect("/profile")

        else:
            msg = 'Form is not valid'
    else:
        form = UserUpdateForm(instance=request.user)
    # print(segment)
    return render(request, "home/profile.html", {"form": form, "msg": msg, "success": success,"segment": segment})



@login_required(login_url="/login/")
def settings(request):
    msg = None
    success = None
    segment='settings'
    users=User.objects.all()
    settings=IntegrationSettings.objects.get(id=1)

    if request.method == "POST":
        if request.POST.get('username'):
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                form.save()
                # username = form.cleaned_data.get("username")
                # raw_password = form.cleaned_data.get("password")
                # user = authenticate(username=username, password=raw_password)
                # msg = 'User created - please <a href="/login">login</a>.'
                success = 'success'
                # request = None
                return render(request, "home/admin/settings.html",{"form": form, "msg": msg, "success": success,"segment": segment, "users" : users,'form_settings' : form_settings})
            else:
                msg = 'Form is not valid'
        elif request.POST.get('integration_frequency'):
            form = UserUpdateForm(request.POST)
            form_settings = IntegrationSettingsForm(request.POST, instance=settings)
            if form_settings.is_valid():
                form_settings.save()
                return render(request, "home/admin/settings.html",{"form": form, "msg": msg, "success": success,"segment": segment, "users" : users,'form_settings' : form_settings})

    else:
        form = UserUpdateForm()
        form_settings = IntegrationSettingsForm(instance=settings)

        return render(request, "home/admin/settings.html", {"form": form, "msg": msg, "success": success,"segment": segment , "users" : users, 'form_settings' : form_settings})





@login_required(login_url="/login/")
def settings_user_update(request,id):
    msg = None
    success = None
    segment='settings'
    user=User.objects.get(id=id)
    form = UserUpdateForm(instance=user)
    users=User.objects.all()

    if request.method == "POST":
        form = UserUpdateForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            success = 'success'
            return render(request, "home/admin/settings_user_update.html",{"form": form, "msg": msg, "success": success,"segment": segment, "user" : user, "users" : users})
        else:
            msg = 'Form is not valid'
    else:
        form = UserUpdateForm(instance=user)
    return render(request, "home/admin/settings_user_update.html", {"form": form, "msg": msg, "success": success,"segment": segment , "user" : user, "users" : users})




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
