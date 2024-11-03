from decimal import Decimal

from django.db import models

from constans import ACCOUNT_TYPE, BANK_CODES
from users.models import Users  # users 앱의 Users 모델을 임포트


class Accounts(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name="accounts")
    account_number = models.CharField(max_length=20, unique=True)  # 계좌 번호는 고유값으로 설정
    bank_code = models.CharField(max_length=10, choices=BANK_CODES)  # 은행 코드 길이를 조정하여 관리 효율성 향상
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE)  # 선택 필드로 설정
    balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal("0.00")
    )  # 금액은 DecimalField로 처리

    class Meta:
        db_table = "accounts"  # 테이블 이름 설정
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    def __str__(self) -> str:
        return f"{self.user}'s Account - {self.account_number} ({self.bank_code})"
