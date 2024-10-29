# accounts/forms.py
from django import forms

from .models import Accounts


class AccountForm(forms.ModelForm[Accounts]):
    class Meta:
        model = Accounts
        fields = ["account_number", "bank_code", "account_type", "balance"]
        labels = {
            "account_number": "계좌 번호",
            "bank_code": "은행 코드",
            "account_type": "계좌 유형",
            "balance": "잔액",
        }
        widgets = {
            "account_type": forms.Select(choices=Accounts.ACCOUNT_TYPE_CHOICES),  # 선택 필드로 설정
            "balance": forms.TextInput(attrs={"placeholder": "잔액 입력"}),
        }
