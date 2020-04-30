from django.db import models

# Create your models here.
class Video(models.Model):
	yt_link = models.CharField(max_length=999)
	role = models.CharField(max_length=999, blank=True)

	def __str__(self):
		return self.yt_link + " - " + self.role