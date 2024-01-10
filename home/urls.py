from django.urls import path
from .views import *

urlpatterns = [
    path('' , HomeView.as_view(), name='home'),
    path('download/<uid>/' ,DownloadFileView.as_view(), name='download_file'),
    path('handle/', HandleFileUpload.as_view(), name='upload'),   
]