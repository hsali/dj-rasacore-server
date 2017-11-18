"""dj_rasacore_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from rest_framework import routers

from rasacore import api as rasacore_api

router = routers.DefaultRouter()
router.register(r'stories', rasacore_api.StoriesViewSet)
router.register(r'intents', rasacore_api.IntentsViewSet)
router.register(r'user-says', rasacore_api.IntentUserSaysViewSet)
router.register(r'intent-actions', rasacore_api.IntentActionsViewSet)

urlpatterns = [
    # API URLs
    url(r'^api/v1.0/', include(router.urls, namespace='v1.0')),
    # url(r'^api/v1/chat/$', rasacore_api.chatView),

    # Page Views URLs
    url(r'^', include('rasacore.urls')),

    url(r'^admin/', admin.site.urls),
    url(r'^nested_admin/', include('nested_admin.urls')),
]
