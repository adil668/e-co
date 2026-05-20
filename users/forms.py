from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=80)
    last_name = forms.CharField(max_length=80)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class": "form-check-input"}))

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        for name, field in self.fields.items():
            if name != "remember_me":
                field.widget.attrs.update({"class": "form-control"})


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone", "address", "city", "state", "postal_code", "avatar")
        widgets = {
            "address": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})
