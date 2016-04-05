from django.conf.urls import url

from members import views
from members.views import *

urlpatterns = [
    url(r'^logout/$', views.logout, name="logout"),

    url(r'^person/$', PersonsView.as_view(), name="persons"),
    url(r'^person/create/$', PersonCreateView.as_view(), name="person_create"),
    url(r'^person/(?P<pk>[0-9]+)/update/$', PersonUpdateView.as_view(), name="person_update"),
    url(r'^person/(?P<pk>[0-9]+)/delete/$', PersonDeleteView.as_view(), name="person_delete"),

    url(r'^organization/$', OrganizationsView.as_view(), name="organizations"),
    url(r'^organization/create/$', OrganizationCreateView.as_view(), name="organization_create"),
    url(r'^organization/(?P<pk>[0-9]+)/update/', OrganizationUpdateView.as_view(), name="organization_update"),
    url(r'^organization/(?P<pk>[0-9]+)/delete/', OrganizationDeleteView.as_view(), name="organization_delete"),
    url(r'^organization/emails/(?P<organizations>[0-9]+(,[0-9]+)*)', OrganizationEmailView.as_view(), name="organization_email"),

    url(r'^settings/$', SettingsView.as_view(), name="preferences"),

    # TODO: remove this route, only for testing purposes!
    url(r'sudo/', SudoView.as_view(), name="sudo"),
]
