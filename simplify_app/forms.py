from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

from .models import User, SimpleUrl
# from .apps import user_registered
from .utilities import user_registered


# URL form

class SimpleUrlForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SimpleUrlForm, self).__init__(*args, **kwargs)
        self.fields['original_url'].widget = forms.TextInput(
            attrs={
                "placeholder": "URL to simplify",
                "class": "form-control"
            })

    class Meta:
        model = SimpleUrl
        fields = ('original_url', )
        # widgets = {'user': forms.HiddenInput, 'simple_url': forms.HiddenInput}


# Auth

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
            attrs={
                "autofocus": True,
                "placeholder": "Username",
                "class": "form-control"
            })

        self.fields['password'].widget = forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "placeholder": "Password",
                "class": "form-control"
            })


class RegisterUserForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email address',
                             widget=forms.EmailInput(
                                 attrs={
                                     "placeholder": "Enter Email",
                                     "class": "form-control"
                                 }))
    password = forms.CharField(label='Password',
                               help_text=password_validation.password_validators_help_text_html(),
                               widget=forms.PasswordInput(
                                   attrs={
                                       "placeholder": "Password",
                                       "class": "form-control"
                                   }
                               ))
    password_confirm = forms.CharField(label='Password confirmation',
                                       help_text='Confirm your password',
                                       widget=forms.PasswordInput(
                                           attrs={
                                               "placeholder": "Password Confirmation",
                                               "class": "form-control"
                                           }
                                       ))

    def __init__(self, *args, **kwargs):
        self.domain = kwargs.pop('domain')
        super(RegisterUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        )
        self.fields['first_name'].widget = forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        )
        self.fields['last_name'].widget = forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control"
            }
        )

    def clean_password(self):
        password = self.cleaned_data['password']
        if password:
            password_validation.validate_password(password)
        return password

    def clean(self):
        super().clean()
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password and password_confirm and password != password_confirm:
            errors = {'password_confirm': ValidationError(
                'Passwords are not same.', code='password_mismatch'
            )}
            raise ValidationError(errors)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        user.is_activated = False
        if commit:
            user.save()
        user_registered.send(RegisterUserForm, instance=user, domain=self.domain)
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm',
                  'first_name', 'last_name')


# Edit User

class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Email address',
                             widget=forms.EmailInput(
                                 attrs={
                                     "placeholder": "Enter Email",
                                     "class": "form-control"
                                 }
                             ))

    def __init__(self, *args, **kwargs):
        super(ChangeUserInfoForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "form-control"
            }
        )
        self.fields['first_name'].widget = forms.TextInput(
            attrs={
                "placeholder": "First Name",
                "class": "form-control"
            }
        )
        self.fields['last_name'].widget = forms.TextInput(
            attrs={
                "placeholder": "Last Name",
                "class": "form-control"
            }
        )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class UserPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget = forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                "autofocus": True,
                "placeholder": "Previous password",
                "class": "form-control"
            }
        )
        self.fields['new_password1'].widget = forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "New password",
                "class": "form-control"
            })
        self.fields['new_password2'].widget = forms.PasswordInput(
            attrs={
                "autocomplete": "new-password",
                "placeholder": "New password confirmation",
                "class": "form-control"
            })
