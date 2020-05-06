from django.db import models
import string
import random

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
	exists = True
	while exists == True:
		ran = ''.join(random.choice(chars) for _ in range(size))
		if len(Lease_option.objects.filter(random_str=ran)) == 0:
			exists = False

	return ran

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
	img_thumb = models.ImageField(upload_to="beat_covers", null=True, blank=True)
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
	dropbox_url = models.CharField(max_length=999, blank=True)
	random_str = models.CharField(max_length=999, default=id_generator)

	def __str__(self):
		return self.beat.name + " - " + self.name
