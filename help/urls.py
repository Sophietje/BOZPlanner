from django.conf.urls import url

from help import views

app_name = "help"

urlpatterns = [
    url(r'^$', views.HelpView.as_view(), name="help"),
]
