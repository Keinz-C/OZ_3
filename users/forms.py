# users/forms.py
from django import forms

from .models import Users


class UserRegistrationForm(forms.ModelForm):  # 타입 파라미터 제거
    class Meta:
        model = Users
        fields = ["email", "password", "nickname", "name", "phone_number"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
