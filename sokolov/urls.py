from django.conf.urls import url

from sokolov.views import HomePageView

urlpatterns = [
    url(r'', HomePageView.as_view())
]