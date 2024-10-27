from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    USER_ROLE = 'user'
    ADMIN_ROLE = 'admin'

    ROLE_CHOICES = [
        (USER_ROLE, 'Користувач'),
        (ADMIN_ROLE, 'Адмін'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=USER_ROLE)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='Групи, до яких належить користувач',
        verbose_name='групи'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions_set',
        blank=True,
        help_text='Спеціальні дозволи для користувача',
        verbose_name='дозволи'
    )

    def is_admin(self):
        return self.role == self.ADMIN_ROLE

    def is_user(self):
        return self.role == self.USER_ROLE


class LogEntry(models.Model):
    LEVEL_CHOICES = [
        ('DEBUG', 'Debug'),
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]

    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='custom_log_entries'
    )

    def __str__(self):
        return f"[{self.timestamp}] {self.level}: {self.message}"
