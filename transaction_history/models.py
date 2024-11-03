from django.db import models

from accounts.models import Accounts  # 계좌 정보 모델 임포트
from constans import TRANSACTION_METHOD, TRANSACTION_TYPE


class Transaction_History(models.Model):
    id = models.AutoField(primary_key=True)
    account_info = models.ForeignKey(Accounts, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=12, decimal_places=2)  # 거래 금액을 DecimalField로 설정
    post_transaction_balance = models.DecimalField(
        max_digits=12, decimal_places=2
    )  # 거래 후 잔액도 DecimalField로 설정
    transaction_details = models.CharField(max_length=255)  # 세부 정보의 최대 길이 증가

    # 거래 유형을 선택지로 설정
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)

    # 결제 방법을 선택지로 설정
    payment_method = models.CharField(max_length=20, choices=TRANSACTION_METHOD)

    transaction_datetime = models.DateTimeField(auto_now_add=True)  # 거래 생성 시점 기록

    class Meta:
        db_table = "transaction_history"
        verbose_name = "Transaction History"
        verbose_name_plural = "Transaction Histories"

    def __str__(self) -> str:
        return f"{self.account_info.account_number} - {self.transaction_type} - {self.amount}"

    # 잔액 업데이트 로직 추가
    def save(self, *args, **kwargs):
        # 가장 최근의 거래 내역을 조회
        last_transaction = (
            Transaction_History.objects.filter(account_info=self.account_info).order_by("-transaction_datetime").first()
        )

        # 기존 잔액 가져오기 (처음 거래일 경우 0으로 시작)
        last_balance = last_transaction.post_transaction_balance if last_transaction else 0

        # 거래 유형에 따라 금액 더하기 또는 빼기
        if self.transaction_type == "DEPOSIT":
            self.post_transaction_balance = last_balance + self.amount
        elif self.transaction_type == "WITHDRAWAL":
            self.post_transaction_balance = last_balance - self.amount

        super().save(*args, **kwargs)
