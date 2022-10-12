"""crowdFunding URL Configuration

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
from django.urls import path , include
from django.contrib import admin
from django.conf.urls.static import static
from . import settings
from projects import urls, views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/' , include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('projects/',include('projects.urls')),
    path('search/',views.search),
    path('',views.home, name = 'home'),
    path('categories/', include('categories.urls')),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
