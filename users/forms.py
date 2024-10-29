from django import forms

from .models import Users


class UserRegistrationForm(forms.ModelForm[Users]):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Users
        fields = ["email", "nickname", "name", "phone_number", "password"]
