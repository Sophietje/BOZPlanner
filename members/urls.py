from django.conf.urls import url

from members.views import PersonsView, PersonCreateView, PersonUpdateView, PersonDeleteView

urlpatterns = [
    url(r'^$', PersonsView.as_view()),
    url(r'^member/(?P<id>[0-9]+)/create$', PersonCreateView.as_view()),
    url(r'^member/(?P<id>[0-9]+)/update$', PersonUpdateView.as_view()),
    url(r'^member/(?P<id>[0-9]+)/delete$', PersonDeleteView.as_view()),
]