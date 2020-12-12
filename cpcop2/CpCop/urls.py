"""CpCop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import ToBi.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/',ToBi.views.index, name='index'),
    path('traffic/', ToBi.views.traffic, name='traffic'),
    path('weather/', ToBi.views.weather, name='weather'),
    path('schedule/', ToBi.views.schedule, name='schedule'),
    path('error/', ToBi.views.error, name='error'),
    path('', ToBi.views.login, name='login'),
    path('.well-known/pki-validation/9C4347E1741BFD986F411C957F5E2036.txt'),
]
