# accounts/views.py
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .models import Accounts


class AccountListView(ListView):
    model = Accounts
    template_name = "accounts/account_list.html"
    context_object_name = "accounts"


class AccountDetailView(DetailView):
    model = Accounts
    template_name = "accounts/account_detail.html"
    context_object_name = "account"


class AccountCreateView(CreateView):
    model = Accounts
    fields = ["user", "account_number", "bank_code", "account_type"]
    template_name = "accounts/account_form.html"
    success_url = "/accounts/"  # 성공 후 리디렉션할 URL 설정


class AccountUpdateView(UpdateView):
    model = Accounts
    fields = ["account_number", "bank_code", "account_type"]
    template_name = "accounts/account_form.html"
    success_url = "/accounts/"
