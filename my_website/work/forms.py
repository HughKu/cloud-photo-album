from django import forms
from models import Image

# form for uploading images via Dropzone
class imageForm(forms.Form):
	#img = forms.ImageField(required=True)
	class Meta:
		model = Image