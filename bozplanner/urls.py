"""bozplanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

import members.urls
import meetings.urls
import preferences.urls
from bozplanner import views
from bozplanner.settings import HAVE_DJANGOSAML2

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^members/', (members.urls.urlpatterns, 'members', 'members')),
    url(r'^meetings/', include(meetings.urls)),
    url(r'^$', views.index, name=''),
    url(r'^help/', views.HelpView.as_view(), name="help"),
    url(r'^settings/', include(preferences.urls))
]

if HAVE_DJANGOSAML2:
    urlpatterns += [
        url(r'^saml2/', include('djangosaml2.urls')),
    ]
