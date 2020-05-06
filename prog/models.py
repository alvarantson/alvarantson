from django.db import models

# Create your models here.
class Skill(models.Model):
	description = models.TextField()

class Project(models.Model):
	name = models.CharField(max_length=999)
	description = models.TextField()
	img = models.FileField(upload_to="code", null=True, blank=True)
	color = models.CharField(max_length=999, blank=True) # https://docs.microsoft.com/en-us/sharepoint/dev/design/themes-colors
	url = models.CharField(max_length=999, blank=True)
	git = models.CharField(max_length=999, blank=True)

	def __str__(self):
		return self.name