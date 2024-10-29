from decimal import Decimal

from django.db import models

from accounts.models import Accounts  # 계좌 정보 모델 임포트


class Transaction_History(models.Model):
    id = models.AutoField(primary_key=True)
    account_info = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # 거래 금액을 DecimalField로 설정
    post_transaction_balance = models.DecimalField(
        max_digits=12, decimal_places=2
    )  # 거래 후 잔액도 DecimalField로 설정
    transaction_details = models.CharField(max_length=255)  # 세부 정보의 최대 길이 증가

    # 거래 유형을 선택지로 설정
    TRANSACTION_TYPE_CHOICES = [("DEPOSIT", "Deposit"), ("WITHDRAWAL", "Withdrawal")]  # 입금  # 출금
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE_CHOICES)

    # 결제 방법을 선택지로 설정
    PAYMENT_METHOD_CHOICES = [("CASH", "Cash"), ("CARD", "Card"), ("TRANSFER", "Transfer")]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)

    transaction_datetime = models.DateTimeField(auto_now_add=True)  # 거래 생성 시점 기록

    class Meta:
        db_table = "transaction_history"
        verbose_name = "Transaction History"
        verbose_name_plural = "Transaction Histories"

    def __str__(self) -> str:
        return f"{self.account_info.account_number} - {self.transaction_type} - {self.amount}"
