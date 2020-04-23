from django.db import models

# Create your models here.
class Discount(models.Model):
	code = models.CharField(max_length=999, unique=True)
	amount = models.IntegerField()

	def __str__(self):
		return self.code + " - " + str(self.amount)

class Beat(models.Model):
	name = models.CharField(max_length=999, unique=True)
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
	price = models.FloatField()
	file = models.FileField(upload_to="lease_files")

	def __str__(self):
		return self.beat.name + " - " + self.name
