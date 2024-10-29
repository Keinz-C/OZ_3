# accounts/views.py
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .forms import AccountForm
from .models import Accounts


# [Accounts] : []안의 내용은 파라미터화된 제네릭 타입을 나타낸다.
# 이 구문은 python의 타입 힌팅 기능을 사용하여 클래스가 어떤 타입의 인스턴스를 관리하는지를 명시한다.
# ex) mypy = -> list
class AccountListView(ListView[Accounts]):
    model = Accounts
    template_name = "accounts/account_list.html"
    context_object_name = "accounts"


class AccountDetailView(DetailView[Accounts]):
    model = Accounts
    template_name = "accounts/account_detail.html"
    context_object_name = "account"


# CreateView와 UpdateView에서는 폼을 사용해 데이터를 입력받고 저장하는 작업이 필요하기 때문에
class AccountCreateView(CreateView[Accounts, AccountForm]):
    model = Accounts
    form_class = AccountForm
    template_name = "accounts/account_form.html"
    success_url = reverse_lazy("accounts:account_list")


class AccountUpdateView(UpdateView[Accounts, AccountForm]):
    model = Accounts
    form_class = AccountForm
    template_name = "accounts/account_form.html"
    success_url = reverse_lazy("accounts:account_list")
