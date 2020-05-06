from django.db import models

# Create your models here.
class Release(models.Model):
	name = models.CharField(max_length=999)
	artist = models.CharField(max_length=999)
	role = models.CharField(max_length=999)

	youtube_url = models.CharField(max_length=999, blank=True)
	soundcloud_url = models.CharField(max_length=999, blank=True)
	spotify_url = models.CharField(max_length=999, blank=True)

	release_date = models.DateField(null=True)
	genre = models.CharField(max_length=999, blank=True)

	def __str__(self):
		return self.artist+" - "+self.name+" "+str(self.release_date)

class Release_stats(models.Model):
	release = models.ForeignKey(Release, on_delete=models.CASCADE)
	fetch_date = models.DateTimeField(auto_now_add=True)

	youtube_views = models.CharField(max_length=999, blank=True)
	youtube_likes = models.CharField(max_length=999, blank=True)
	youtube_dislikes = models.CharField(max_length=999, blank=True)

	soundcloud_views = models.CharField(max_length=999, blank=True)
	soundcloud_likes = models.CharField(max_length=999, blank=True)
	soundcloud_reposts = models.CharField(max_length=999, blank=True)
	soundcloud_comments = models.CharField(max_length=999, blank=True)

	def __str__(self):
		return str(self.release)+" FETCHED: "+str(self.fetch_date)