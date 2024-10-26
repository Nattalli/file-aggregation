from django.urls import path
from .views import FileUploadView, CampaignListView


urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file_upload'),
    path('campaigns/', CampaignListView.as_view(), name='campaign_list'),
]
