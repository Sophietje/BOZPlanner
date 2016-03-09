from django.conf.urls import url

from members import views
from members.views import PersonsView, PersonCreateView, PersonUpdateView, PersonDeleteView

urlpatterns = [
    url(r'^logout$', views.logout, name="logout"),
    url(r'^person$', PersonsView.as_view(), name="persons"),
    url(r'^person/create$', PersonCreateView.as_view(), name="person_create"),
    url(r'^person/(?P<pk>[0-9]+)/update$', PersonUpdateView.as_view(), name="person_update"),
    url(r'^person/(?P<pk>[0-9]+)/delete$', PersonDeleteView.as_view(), name="person_delete"),
]
