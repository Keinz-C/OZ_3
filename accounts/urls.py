# accounts/urls.py
from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.AccountListView.as_view(), name="account_list"),  # 계좌 목록 조회
    path("create/", views.AccountCreateView.as_view(), name="account_create"),  # 계좌 생성
    path("<int:pk>/", views.AccountDetailView.as_view(), name="account_detail"),  # 계좌 세부 조회
    path("<int:pk>/update/", views.AccountUpdateView.as_view(), name="account_update"),  # 계좌 수정
]
