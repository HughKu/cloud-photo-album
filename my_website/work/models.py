from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill, ResizeToFit
# PIL
from PIL import Image as PILImage
from PIL.ExifTags import TAGS as PILTags
from PIL.ExifTags import GPSTAGS as PILGpsTags
# Built-in
import os
import hashlib
from datetime import datetime

def upload_path(instance, filename):
	# provide upload_to with a function that re-names the data to hashed name
	name = hashlib.sha1(filename)
	_, ext = os.path.splitext(filename)
	return "album/{0}{1}".format(name.hexdigest(), ext)

# Tag of image (user-defined text, classified key-word, etc)
class Tag(models.Model):
	name = models.CharField(max_length=50, unique=True)

	def __unicode__(self):
		return self.name

# Metadata of image, i.e. exchangable image file format (EXIF)
class Meta(models.Model):
	name = models.CharField(max_length=50)

	def __unicode__(self):
		return self.name

# Image
class Image(models.Model):
	# data source
	data = models.ImageField(upload_to=upload_path)
	data_thumbnail = ImageSpecField(source='data', processors=[ResizeToFit(height=512)], format='JPEG', options={'quality': 80})

	# date time collection
	date_uploaded = models.DateTimeField(auto_now_add=True)
	date_original = models.DateTimeField()

	# tag which describes the data
	tag = models.ManyToManyField(Tag)

	# filtering properties
	is_public = models.BooleanField(default=True)
	is_search_history = models.BooleanField(default=False)

	def __unicode__(self):
		return self.data.name

	def save(self, *args, **kwargs):
		"""
		TODO: make an exif model that retrieves metadata of uploaded image
		"""
		# save "date_original" above (use PIL EXIF package)
		if self.data:
			img = PILImage.open(self.data)
			info = img._getexif()
			for tag, value in info.items():
				decode = PILTags.get(tag, tag)
				if decode == 'DateTimeOriginal':
					self.date_original = datetime.strptime(value, '%Y:%m:%d %H:%M:%S')

		super(Image, self).save()

# Album
class Album(models.Model):
	title = models.CharField(max_length=250)
	images = models.ManyToManyField(Image, related_name="images")
	cover_image = models.OneToOneField(Image, related_name="cover_image")

	def __unicode__(self):
		return self.title
