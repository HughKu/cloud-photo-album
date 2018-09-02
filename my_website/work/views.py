from django.views.generic import View
from django.shortcuts import render
from django.http import HttpResponse

from work.forms import imageForm
from work.models import *

from braces.views import (
    AjaxResponseMixin,
    JSONResponseMixin,
    JsonRequestResponseMixin,
    CsrfExemptMixin,
)

from py_caffe_module.classification import *
from py_caffe_module.feature_extraction import *
#from tensorflow.models.image.imagenet import classification as inception_v3
import flickrapi
import json
import urllib

import os


# Create your views here.
def work(request):
	return render(request, 'work/work.html')

def image_classification(request):
    return render(request, 'work/image_classification.html')
    
# new version entrance page for demo 
def photo_album_alpha(request):
    return render(request, 'work/photo_album_alpha.html')

class AjaxLoadFlickrPhotos(JSONResponseMixin, AjaxResponseMixin, View):
    """
    View for :
        1. load Flickr images via AJAX
    """
    api_key = u'af7edc8ad3abd2f42532746c5b4a93a8'
    api_secret = u'af1a5eabba0030c1'

    def get_ajax(self, request, *args, **kwargs):
        flickr = flickrapi.FlickrAPI(self.api_key, self.api_secret, format='parsed-json')
        extras ='url_m, tags'
        result = flickr.photos.search(text="mountain", per_page=10, extras=extras)
        image_set = result['photos']

        response_dict = {
            'message': 'Photos Loaded Successfully!',
            'image_set': image_set,
        }
        return self.render_json_response(response_dict, status=200)

class AjaxLoadAlbumPhotos(JSONResponseMixin, AjaxResponseMixin, View):
    """
    View for :
        1. load database images via AJAX
    """
    def get_ajax(self, request, *args, **kwargs):

        images = []
        # either by keywords
        if request.GET:
            tags = Tag.objects.get(name__iexact=request.GET['keywords'])
            images = tags.image_set.all()
        # or all
        else:
            images = Image.objects.all()

        image_set = []
        for img in images:
            image_set.append(img.data_thumbnail.url)

        response_dict = {
            'message': 'Photos Loaded Successfully',
            'image_set': image_set,
        }
        return self.render_json_response(response_dict, status=200)

class AjaxPhotoUploadView(CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, View):
    """
    View for :
        1. uploading images via AJAX.
        2. image classification (On)
    """
    def __init__(self):
        # Initialize the classifier of [Caffe AlexNet]
        #self.caffe_alexnet_clf = ImagenetClassifier(**ImagenetClassifier.default_args)
        # Initialize the extraction of [Caffe AlexNet]
        self.extraction = FeatureExtraction()
    
    def classify(self, img_path):
	    try:
	        image = exifutil.open_oriented_im(img_path)

	    except Exception as err:
	        logging.info('Uploaded image open error: %s', err)

	    result = self.caffe_alexnet_clf.classify_image(image)

	    return result

    def post_ajax(self, request, *args, **kwargs):

        # save image 
        new_image = Image(data=request.FILES['img'])
        new_image.save()

        # image classification
        #result = self.classify(new_image.data.path)
        
        # feature extraction
        result = self.extraction.extract(new_image.data.path)

        # metadata (classification result [trueCls/5cls/clsName])
        try:
            tags = Tag.objects.filter(name=result[1][0][0])
            if tags:
                tag = tags[0]
        except Exception as err:
            print '%s (%s)' % (err.message, type(e))

        if not tags:
            tag = Tag(name=result[1][0][0])
            tag.save()

        # attach metadata
        try:
            new_image.tag.add(tag)
        except Exception as err:
            print '%s (%s)' % (err.message, type(e))

        # templates context
        response_dict = {
            'message': 'File Uploaded Successfully!',
            'image_url': new_image.data_thumbnail.url,
            'result': result,
        }

        return self.render_json_response(response_dict, status=200)

class AjaxImageSearch(CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, View):
    """
    View for :
        1. uploading images via AJAX.
        2. image retrieval (On)
    """
    def __init__(self):
        # Initialize the classifier of [Caffe AlexNet]
        #self.caffe_alexnet_clf = ImagenetClassifier(**ImagenetClassifier.default_args)
        # Initialize the extraction of [Caffe AlexNet]
        self.retrieval = ImageRetrieval()

    def post_ajax(self, request, *args, **kwargs):

        # save image 
        new_image = Image(data=request.FILES['img'])
        new_image.save()

        # image retrieval
        image_set = self.retrieval.retrieve(new_image.data.path)

        # delete this instance
        new_image.delete();

        # TO BE FIXED: work-around on removing certain path format
        for i in xrange(len(image_set)):
            split_paths = image_set[i].split("my_website")
            image_set[i] = split_paths[1]

        # context for templates
        response_dict = {
            'message': 'Ajax Image Search Successfully!',
            'image_set': image_set,
        }
        return self.render_json_response(response_dict, status=200)
'''
class AjaxCrosRequestTensorflow(CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, View):
    """
    View for :
        1. downloading images via AJAX of a click event on image element.
        2. image classification via TensorFlow
    """

    def __init__(self):
        # Initialize the classifier of [TensorFlow Google Incetion_v3]
        self.tensorflow_inception_cls = inception_v3.ImagenetClassifier()

    def post_ajax(self, request, *args, **kwargs):
        img_url = request.POST['img_url']
        img_path = "/tmp/imagenet/downloaded.jpg"
        urllib.urlretrieve(img_url, img_path)

        # predicted results
        result = self.tensorflow_inception_cls.classify(img_path)

        # context for templates
        response_dict = {
            'message': 'Ajax-Cros-Requested Successfully!',
            'imageURL': img_url,
            'result': result,
        }
        return self.render_json_response(response_dict, status=200)
'''
class AjaxCrosRequestCaffe(CsrfExemptMixin, JSONResponseMixin, AjaxResponseMixin, View):
    """
    View for :
        1. downloading images via AJAX of a click event on image element.
        2. image classification via Caffe
    """

    def __init__(self):

        # Initialize the classifier of [Caffe AlexNet]
        self.caffe_alexnet_clf = ImagenetClassifier(**ImagenetClassifier.default_args)

    def classify(self, img_path):
        try:
            image = exifutil.open_oriented_im(img_path)

        except Exception as err:
            logging.info('Uploaded image open error: %s', err)

        result = self.caffe_alexnet_clf.classify_image(image)

        return result

    def post_ajax(self, request, *args, **kwargs):
        img_url = request.POST['img_url']
        img_path = "/tmp/imagenet/downloaded.jpg"
        urllib.urlretrieve(img_url, img_path)

        # predicted results
        result = self.classify(img_path)

        # context for templates
        response_dict = {
            'message': 'Ajax-Cros-Requested Successfully!',
            'imageURL': img_url,
            'result': result
        }
        return self.render_json_response(response_dict, status=200)

class AjaxLoadKeyWords(JSONResponseMixin, AjaxResponseMixin, View):
    """
    View for :
        loading keyword suggestion for search input
    """
    def get_ajax(self, request, *args, **kwargs):
        tags = Tag.objects.all()
        keywords = []
        for tag in tags:
            keywords.append(tag.name)

        print "size of db keywords = {0}".format(len(keywords))

        response_dict = {
            'message': 'Keywords Loaded Successfully!',
            'keywords': keywords,
        }
        return self.render_json_response(response_dict, status=200)
