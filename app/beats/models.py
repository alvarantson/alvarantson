from django.db import models

# Create your models here.
class Discount(models.Model):
	code = models.CharField(max_length=999, unique=True)
	amount = models.IntegerField()

	def __str__(self):
		return self.code + " - " + str(self.amount)

class Beat(models.Model):
	name = models.CharField(max_length=999, unique=True)
	bpm = models.IntegerField(null=True,blank=True)
	key = models.CharField(max_length=999,blank=True)
	tags = models.TextField(blank=True)
	img = models.ImageField(upload_to="beat_covers")
	mp3 = models.FileField(upload_to="beat_mp3s")
	date = models.DateField(auto_now_add=True)

	def __str__(self):
		return self.name

class Lease_option(models.Model):
	beat = models.ForeignKey(Beat, on_delete=models.CASCADE)
	name = models.CharField(max_length=999)
	description = models.TextField()
	after_views = models.CharField(max_length=999, null=True)
	percent_after_views = models.IntegerField(null=True)
	price = models.FloatField()
	file = models.FileField(upload_to="lease_files", null=True, blank=True)
	file_url = models.CharField(max_length=999, blank=True)

	def __str__(self):
		return self.beat.name + " - " + self.name
