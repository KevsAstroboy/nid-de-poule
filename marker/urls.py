from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path

from .views import PantholeView




urlpatterns = [
    re_path(r'potholes/',PantholeView.as_view())
]

