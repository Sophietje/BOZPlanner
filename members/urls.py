from django.conf.urls import url

from members.views import HomePageView

urlpatterns = [
    url(r'', HomePageView.as_view())
]