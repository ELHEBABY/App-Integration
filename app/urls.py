from cgitb import handler
from . import views, views_integration
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path('login/', views.login, name="login"),
    path('logout/', views.logout_view, name="logout"),
    # path('register/', views.register, name="register"),

    path('home/', views.index),
    path('', views.login),
    path('integration/', views.integration,name="integration"),
    path('history/<int:id>', views.history,name="integration_history"),
    # path('historys/', views.historys,name="history"),
    path('profile/', views.profile,name="profile"),
    path('settings/', views.settings,name="settings"),
    path('settings/user/update/<int:id>', views.settings_user_update,name="update"),





    path('launch_the_integration', views_integration.launch_the_integration,name="launch_the_integration"),



    path('lol/', views.testlol,name="lol"),
    path('test5/', views.test5,name="test5"),
    # path('test2/', views.test2,name="test2"),
    path('test3/', views.test3,name="test3"),
    
    # path('home/', views.index),

]
