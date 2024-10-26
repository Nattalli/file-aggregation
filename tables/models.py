from django.db import models


class Campaign(models.Model):
    advertiser = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    format = models.CharField(max_length=100)
    platform = models.CharField(max_length=100)
    impressions = models.BigIntegerField()

    def __str__(self):
        return f"{self.advertiser} - {self.brand}"
