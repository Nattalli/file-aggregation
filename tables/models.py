from django.db import models


class FileUpload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Campaign(models.Model):
    file_upload = models.ForeignKey(FileUpload, on_delete=models.CASCADE, related_name='campaigns')
    advertiser = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    format = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    impressions = models.BigIntegerField()

    def __str__(self):
        return f"{self.advertiser} - {self.brand}"
