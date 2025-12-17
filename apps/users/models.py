from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password


from django.core import validators
from django.utils.deconstruct import deconstructible

@deconstructible
class PhoneValidator(validators.RegexValidator):
    regex = r"^\+998\d{9}$"
    message = "To'g'ri keladigan telefon raqam kiriting"
    flags = 0


class CustomUserManager(BaseUserManager):
    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError("The given phone number must be set")

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(phone_number, password, **extra_fields)

    def create_user(self, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    username = None

    phone_validator = PhoneValidator()

    phone_number = models.CharField(
        max_length = 13,
        verbose_name='Phone number',
        validators = [phone_validator],
        unique = True
    )
    birth_date = models.DateField(verbose_name='Birth date', null=True, blank=True)

    objects = CustomUserManager()

    def __str__(self) -> str:
        return f"{self.id} - {self.phone_number}"



