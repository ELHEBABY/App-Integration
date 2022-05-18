from django import forms
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User

from .models import IntegrationSettings


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))


class User_register(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First name",
                "class": "form-control",
                'checked' : 'checked'
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last name",
                "class": "form-control"
            }
        ))
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password= forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    # is_active= forms.ChoiceField(
    #     widget=forms.RadioSelect(
    #         attrs={
    #             "placeholder": "Is Active",
    #             "class": "form-control"
    #         }
    #     ))
    # password2 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "placeholder": "Password check",
    #             "class": "form-control"
    #         }
    #     ))

    # password2 = password1


    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'username', 'email', 'password','is_active')



class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Last name",
                "class": "form-control"
            }
        ))
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "First name",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    # is_active = forms.BooleanField(
        # widget=forms.ChoiceField(
        #     attrs={
        #         "placeholder": "Is active",
        #         "class": "form-control"
        #     }

        # )
        # widget=forms.RadioSelect(choices=("False", "True"))
        # )
    # is_active = forms.CharField(
    #     widget=forms.RadioSelect(
    #         attrs={
    #             "placeholder": "Is active",
    #             "class": "form-control"
    #         }
    #     ))
    class Meta:
        model = User
        fields = ('username', 'email','last_name','first_name','is_active')


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "form-control"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "form-control"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')



class IntegrationSettingsForm(forms.ModelForm):

    chois =(
        ('automatic','automatic'),
        ('manual','manual'))
    type = forms.ChoiceField(
        label="Type",
        initial='',
        choices=chois,
        widget=forms.Select(
            attrs={'class': 'form-control',
            'placeholder' : 'Type'}),
        required=True)

    frequency =(
        ('day','Day'),
        ('two_days','Two days'),
        ('week','Week'))
    frequenc = forms.ChoiceField(
        label="Frequenc",
        initial='',
        choices=frequency,
        widget=forms.Select(
            attrs={'class': 'form-control',
            'placeholder' : 'Frequenc'}),
        required=True)

    time = forms.TimeField(
        widget = forms.TimeInput(format='%H:%M', attrs={'class': 'form-control','type': 'time'}
        )
    )

    class Meta:
        model = IntegrationSettings
        fields = ('type', 'frequenc','time')




class PasswordChangeForm(PasswordChangeForm):

    old_password = forms.CharField(label="Old password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Old password :",
                "class": "form-control"
            }
        ))

    new_password1= forms.CharField(label="New password",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "New password",
                "class": "form-control"
            }
        ))
    
    new_password2= forms.CharField(label="New password confirmation",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "New password confirmation ",
                "class": "form-control"
            }
        ))

    class Meta:
        model = IntegrationSettings
        fields = ('old_password','new_password1', 'new_password2')








class ChangePasswordForm(forms.ModelForm):
    
    password= forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "form-control"
            }
        ))
        
# password2 = forms.CharField(
    #     widget=forms.PasswordInput(
    #         attrs={
    #             "placeholder": "Password check",
    #             "class": "form-control"
    #         }
    #     ))


    class Meta:
        model = User
        fields = ('password',)
