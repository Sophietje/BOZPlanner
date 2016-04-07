"""Global URL configuration from the root, mostly to route to the apps."""
from django.conf.urls import url, include
from django.contrib import admin

import members.urls
import meetings.urls
import help.urls
from bozplanner import views
from bozplanner.settings import HAVE_DJANGOSAML2

urlpatterns = [
    url(r'^$', views.index, name=''),
    url(r'^admin/', admin.site.urls),
    url(r'^members/', include(members.urls)),
    url(r'^meetings/', include(meetings.urls)),
    url(r'^help/', include(help.urls)),
]

if HAVE_DJANGOSAML2:
    urlpatterns += [
        url(r'^saml2/', include('djangosaml2.urls')),
    ]
