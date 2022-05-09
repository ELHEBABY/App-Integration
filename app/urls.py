from . import views
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout_view, name="logout"),
    # path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', views.register, name="register"),




    path('home/', views.index),
    path('', views.login),

    # re_path(r'^.*\.*', views.pages, name='pages'),

    path('integration/', views.integration,name="integration"),
    path('history/', views.history,name="history"),
    path('profile/', views.profile,name="profile"),
    path('settings/', views.settings,name="settings"),
    path('settings/user/update/<int:id>', views.settings_user_update,name="update"),


    path('test/', views.test,name="test"),


    
    # path('home/', views.index),


    
]
