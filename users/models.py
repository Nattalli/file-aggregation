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


class FileUploadLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)
    error_type = models.CharField(max_length=255, blank=True, null=True)


class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_date = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=10, choices=User.ROLE_CHOICES)
