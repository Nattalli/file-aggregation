from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, FileUploadLog, AccessLog


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )


@admin.register(FileUploadLog)
class FileUploadLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'file_name', 'upload_date', 'status', 'error_type')
    search_fields = ('user__email', 'file_name', 'status')
    list_filter = ('status',)


@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'access_date', 'level')
    search_fields = ('user__email',)
    list_filter = ('level',)
