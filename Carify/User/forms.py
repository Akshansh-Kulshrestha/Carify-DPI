from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Roles, Permissions, Roles_Permissions
from django.contrib.auth.forms import PasswordResetForm

# Reset Password
class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter your registered email',
            'autocomplete': 'email'
        })

# CustomUser forms
class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name", "password1", "password2" )

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email",)

class LoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

# Roles form
class RolesForm(forms.ModelForm):
    class Meta:
        model = Roles
        fields = ["name", "status"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "status": forms.NumberInput(attrs={"class": "form-control"}),
        }


# Permissions form
class PermissionsForm(forms.ModelForm):
    class Meta:
        model = Permissions
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }


# Roles_Permissions form
class RolesPermissionsForm(forms.ModelForm):
    class Meta:
        model = Roles_Permissions
        fields = ["role", "permission"]
        widgets = {
            "role": forms.Select(attrs={"class": "form-control"}),
            "permission": forms.Select(attrs={"class": "form-control"}),
        }
