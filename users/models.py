# AbstractBaseUser는 비밀번호와 로그인 관련 필드를 제공하는 기본 유저 모델입니다.
# BaseUserManager는 커스텀 유저 생성 메서드를 작성하는데 사용하는 클래스입니다.
# PermissionsMixin은 is_superuser 필드와 권한 관리를 위한 메서드를 제공합니다.
from typing import Any, Optional

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    Permission,
    PermissionsMixin,
    UserManager,
)
from django.db import models

# Create your models here.


# UserManager 클래스는 BaseUserManager를 상속받아 유저 생성 메서드를 정의하는 커스텀 매니저입니다.
class CustomUserManager(BaseUserManager["Users"]):
    user_data: dict[str, Any] = {}

    # create_user는 일반 유저를 생성하는 메서드이며, 이메일과 비밀번호를 필수로 받고, 나머지 정보는 extra_fields로 받아옵니다.
    def create_user(self, email: str, password: Optional[str] = None, **extra_fields: Any) -> "Users":
        # email이 없는 경우 유저 생성을 막음
        if not email:
            raise ValueError("Email is required")

        # normalize_email 메서드를 사용해 이메일 주소를 표준화(소문자 처리 등)합니다.
        # self.model은 Users 모델을 참조하여 새 유저 인스턴스를 생성하는 구문입니다.
        # set_password는 입력받은 비밀번호를 해시화하여 보안을 유지합니다.
        # save 메서드를 통해 유저 정보를 데이터베이스에 저장합니다.
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user  # 생성된 user정보 저장

    # create_superuser 메서드는 관리자 권한이 있는 유저(슈퍼유저)를 생성할 때 사용합니다.
    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> "Users":

        # 슈퍼유저의 staff, admin, active 상태를 True로 설정합니다. 기본적으로 관리자 계정은 활성화되어 있어야 하므로 이 값을 강제로 설정합니다.
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        # staff와 admin이 True가 아닌 경우 에러를 발생시켜 슈퍼유저가 아닌 유저는 생성되지 않도록 합니다.
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have admin=True.")

        # 슈퍼유저 생성 메서드는 create_user 메서드를 호출해 슈퍼유저로 설정된 일반 유저를 생성합니다.
        return self.create_user(email, password, **extra_fields)

    class Meta:
        db_table = "custom_user"  # 데이터베이스 테이블 이름
        ordering = ["email"]  # 기본 정렬 기준
        verbose_name = "Custom User"  # 단수형 verbose 이름
        verbose_name_plural = "Custom Users"  # 복수형 verbose 이름


class Users(AbstractBaseUser, PermissionsMixin):
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # 기본값이 아닌 이름으로 변경
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_set",  # 기본값이 아닌 이름으로 변경
        blank=True,
    )
    # email 필드는 유일한 값이어야 하며(unique=True), 유저를 구분하는 로그인 아이디로 사용됩니다
    # password 필드는 AbstractBaseUser에 포함되어 있지만 명시적으로 추가해 주었습니다.
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # `AbstractBaseUser`에 비밀번호 필드가 포함됨
    nickname = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    last_login = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # 이 모델은 UserManager를 통해 유저를 생성 및 관리합니다. UserManager는 앞에서 정의한 커스텀 매니저입니다.
    objects = CustomUserManager()

    # USERNAME_FIELD는 로그인할 때 기본 아이디로 사용할 필드를 지정하며, 이메일을 기본 필드로 사용합니다.
    # REQUIRED_FIELDS는 유저 생성 시 필수 입력 필드로 설정됩니다.
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname", "name"]
