from django.contrib import admin
from .models import FileUpload, Campaign


@admin.register(FileUpload)
class FileUploadAdmin(admin.ModelAdmin):
    list_display = ('uploaded_at',)
    search_fields = ('uploaded_at',)


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('advertiser', 'brand', 'start_date', 'end_date', 'format', 'platform', 'impressions')
    search_fields = ('advertiser', 'brand', 'format', 'platform')
    list_filter = ('format', 'platform', 'start_date', 'end_date')
