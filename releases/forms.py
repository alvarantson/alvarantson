from django import forms

class UploadFileForm(forms.Form):
	empty = forms.BooleanField()
	file = forms.FileField()