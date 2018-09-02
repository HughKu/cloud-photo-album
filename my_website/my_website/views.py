from django.shortcuts import render, render_to_response
from django.http import Http404, HttpResponseRedirect

# Create your views here.
def index(request):
	return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')

def blog(request):
	return render(request, 'blog.html')

def index_testing(request):
	return render(request, 'index-testing.html')