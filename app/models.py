from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

class IntegrationSettings(models.Model):

    chois = (
        ('automatic', 'automatic'),
        ('manual', 'manual')
        )
    type = models.CharField("Type", max_length=50,  choices=chois)
    
    frequency = (
        ('day', 'day'),
        ('two_days', 'two days'),
        ('week', 'week')
        )
    frequenc = models.CharField("frequenc", max_length=50, choices=frequency)
    
    update_date = models.DateTimeField("update date", auto_now_add=True)
    time = models.TimeField("time", default="00:00:00", null=True)
    email_reporting = models.EmailField(max_length=254)
    smtp_server = models.CharField(max_length=100, default=None)
    smtp_port = models.IntegerField( default=None)
    smtp_user = models.EmailField(max_length=254, default=None)
    smtp_password = models.CharField(max_length=100, default=None)

    def __init__(self, *args, **kwargs):
        super(IntegrationSettings, self).__init__(*args, **kwargs)
        self.update_date=self.update_date

    def save (self, *args, **kwargs):
        self.update_date = timezone.now()
        super(IntegrationSettings, self).save (*args, ** kwargs)



class Integrations(models.Model):
    
    date_time = models.DateTimeField("Datetime") 

    chois_status = (
        ('success', 'success'),
        ('erreur', 'erreur'))
    status = models.CharField("Status", max_length=50, choices=chois_status)

    description = models.CharField("Description", max_length=550, default='description')

    chois = (
        ('automatic', 'automatic'),
        ('manual', 'manual')
        )
    type = models.CharField("Type", max_length=50,  choices=chois)
    
    def __str__(self):
        return  str(self.date_time)




class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None




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