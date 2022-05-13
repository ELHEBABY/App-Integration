import email
from pyexpat import model
from statistics import mode
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class IntegrationSettings(models.Model):
    integration_automatic_is_active = models.BooleanField("Integration automatic",default=False)
    
    frequency=(
        ('day','day'),
        ('two_day','two_day'),
        ('week','week'))
    integration_frequency = models.CharField( max_length=50, choices=frequency, default='day')






class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            raise ValueError("Users must haveausername.")
        user=self. model(
            email=self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, password):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email =models. EmailField(verbose_name="email", max_length=60, unique=True)
    username =models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login =models.DateTimeField(verbose_name="1last login", auto_now=True)
    is_admin= models.BooleanField(default=False)
    is_active= models.BooleanField(default=True)
    is_staff= models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)
    hide_email= models.BooleanField(default=True)

    objects=MyAccountManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
                    

    def _str_(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_Label):
        return True