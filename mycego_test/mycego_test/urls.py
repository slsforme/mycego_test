from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from mycego_test import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

