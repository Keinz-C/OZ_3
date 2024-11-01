# accounts/forms.py
from django import forms

from .models import Accounts


class AccountForm(forms.ModelForm):  # 타입 파라미터 제거
    class Meta:
        model = Accounts
        fields = ["user", "account_number", "bank_code", "account_type", "balance"]
