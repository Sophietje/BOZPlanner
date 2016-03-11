from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from preferences import views
from preferences.views import SettingsView

app_name = 'preferences'

urlpatterns = [
    url(r'^$', views.SettingsView.as_view(), name="preferences"),
]