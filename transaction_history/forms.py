from django import forms

from .models import Transaction_History


class TransactionHistoryForm(forms.ModelForm):
    class Meta:
        model = Transaction_History
        fields = ["account_info", "amount", "transaction_type", "payment_method", "transaction_details"]
