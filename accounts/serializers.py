# accounts/serializers.py
from rest_framework import serializers

from .models import Accounts


class AccountSerializer(serializers.ModelSerializer[Accounts]):
    class Meta:
        model = Accounts
        fields = ["id", "user", "account_number", "bank_code", "account_type", "balance"]  # 응답할 필드들
        read_only_fields = ["balance"]  # balance는 읽기 전용으로 설정
