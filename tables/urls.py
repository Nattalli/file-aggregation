from django.urls import path
from .views import FileUploadView, AggregatedResultsView


urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file_upload'),
    path('aggregated-results/', AggregatedResultsView.as_view(), name='aggregated_results'),
]
