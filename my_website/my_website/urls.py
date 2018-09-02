"""my_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views as main_views

urlpatterns = [
    # default admin
    url(r'^admin/', include(admin.site.urls)),
    
    # testing entrance page
    url(r'^index-testing/$', main_views.index_testing, name='index-testing'),

    # main entrance
    url(r'^index/$', main_views.index, name='index'),

    # app: about
    url(r'^about/$', main_views.about, name='about'),

    # app: blog
    url(r'^blog/$', main_views.blog, name='blog'),
    
    # app: work
    url(r'^work/', include('work.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
