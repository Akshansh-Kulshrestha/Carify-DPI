from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Roles, Permissions, UserRole
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

class RoleForm(forms.ModelForm):
    class Meta:
        model = Roles
        fields = ['name', 'permissions', 'status']
        widgets = {
            'permissions': forms.CheckboxSelectMultiple
        }

class PermissionForm(forms.ModelForm):
    class Meta:
        model = Permissions
        fields = ['name']



class UserRoleAssignForm(forms.Form):
    role = forms.ModelChoiceField(queryset=Roles.objects.all(), label="Select Role")

class RolePermissionForm(forms.Form):
    role = forms.ModelChoiceField(queryset=Roles.objects.all(), label="Select Role")
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permissions.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Assign Permissions"
    )