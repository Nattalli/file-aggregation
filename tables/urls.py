from django.urls import path
from .views import FileUploadView, AggregatedResultsView


urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file_upload'),
    path('aggregated-results/<int:file_upload_id>/', AggregatedResultsView.as_view(), name='aggregated_results'),
]
