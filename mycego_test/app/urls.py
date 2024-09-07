from django.urls import path
from app import views

urlpatterns = [
    path("", views.home, name='home'),
    path("download_files/", views.page_for_files, name='page-for-files'),
    path("download_files/<str:filter_string>", views.filtered_page, name='filtered-files-page')
]