from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    phone = models.CharField(max_length=35, blank=True, null=True, verbose_name="phone")
    tg_nick = models.CharField(
        max_length=50, blank=True, null=True, verbose_name="tg_nick"
    )
    avatar = models.ImageField(
        upload_to="users/avatar", blank=True, null=True, verbose_name="avatar"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.email
