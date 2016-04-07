from django.conf.urls import url

from members import views
from members.views import *

app_name = "members"

urlpatterns = [
    url(r'^logout/$', views.logout, name="logout"),

    url(r'^person/$', ListPersonView.as_view(), name="list_person"),
    url(r'^person/create/$', AddPersonView.as_view(), name="add_person"),
    url(r'^person/(?P<pk>[0-9]+)/update/$', ChangePersonView.as_view(), name="change_person"),
    url(r'^person/(?P<pk>[0-9]+)/delete/$', DeletePersonView.as_view(), name="delete_person"),

    url(r'^organization/$', ListOrganizationView.as_view(), name="list_organization"),
    url(r'^organization/create/$', AddOrganizationView.as_view(), name="add_organization"),
    url(r'^organization/(?P<pk>[0-9]+)/update/', ChangeOrganizationView.as_view(), name="change_organization"),
    url(r'^organization/(?P<pk>[0-9]+)/delete/', DeleteOrganizationView.as_view(), name="delete_organization"),
    url(r'^organization/emails/(?P<organizations>[0-9]+(,[0-9]+)*)', EmailOrganizationView.as_view(), name="email_organization"),

    url(r'^preferences/$', PreferencesView.as_view(), name="preferences"),
]
