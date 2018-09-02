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
import views as work_views

urlpatterns = [
    url(r'^$', work_views.work, name='work'),
    url(r'^image-classification/$', work_views.image_classification, name='image_classification'),
    url(r'^photo-album-alpha/$', work_views.photo_album_alpha, name='photo_album_alpha'),
    url(r'^ajax-upload/$', work_views.AjaxPhotoUploadView.as_view(), name='ajax_photo_upload_view'),
#    url(r'^ajax-cros-request-Tensorflow/$', work_views.AjaxCrosRequestTensorflow.as_view(), name='ajax_cros_request_Tensorflow_view'),
    url(r'^ajax-cros-request-Caffe/$', work_views.AjaxCrosRequestCaffe.as_view(), name='ajax_cros_request_Caffe_view'),
    url(r'^ajax-load-flickr/$', work_views.AjaxLoadFlickrPhotos.as_view(), name='ajax_load_Flickr_photo_view'),
    url(r'^ajax-load-album/$', work_views.AjaxLoadAlbumPhotos.as_view(), name='ajax_load_Album_photo_view'),
    url(r'^ajax-load-keywords/$', work_views.AjaxLoadKeyWords.as_view(), name='ajax_load_Keyword_view'),
    url(r'^ajax_image_search_view/$', work_views.AjaxImageSearch.as_view(), name='ajax_image_search_view'),
]