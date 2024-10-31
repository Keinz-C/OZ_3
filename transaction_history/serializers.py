# transaction_history/serializers.py
from rest_framework import serializers

from .models import Transaction_History


class TransactionHistorySerializer(serializers.ModelSerializer[Transaction_History]):
    class Meta:
        model = Transaction_History
        fields = [
            "id",
            "account_info",
            "amount",
            "post_transaction_balance",
            "transaction_details",
            "transaction_type",
            "payment_method",
            "transaction_datetime",
        ]  # 응답할 필드들
        read_only_fields = ["post_transaction_balance", "transaction_datetime"]  # 읽기 전용 필드 설정
