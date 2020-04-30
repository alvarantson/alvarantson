from django.db import models

# Create your models here.
class About(models.Model):
	description = models.TextField()
	email = models.CharField(max_length=999)
	mugshot = models.FileField(upload_to="contact")

class Social_media(models.Model):
	url = models.CharField(max_length=999)
	img_url = models.CharField(max_length=999, blank=True)
	img = models.FileField(upload_to="contact", blank=True, null=True)

	def __str__(self):
		return self.url