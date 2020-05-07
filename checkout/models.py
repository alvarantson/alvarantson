from django.db import models

# Create your models here.
class Buy_history(models.Model):
	date = models.DateField(auto_now_add=True)
	shopping_cart = models.TextField(blank=True)
	shopping_cart_total = models.FloatField()
	buyer_first_name = models.CharField(max_length=999, blank=True)
	buyer_last_name = models.CharField(max_length=999, blank=True)
	buyer_artist_name = models.CharField(max_length=999, blank=True)
	buyer_email = models.CharField(max_length=999, blank=True)
	buyer_address = models.CharField(max_length=999, blank=True)
	receipt = models.TextField()

	def __str__(self):
		return str(self.date) + " - " + str(self.shopping_cart_total) + " - " + self.buyer_email

class License_template(models.Model):
	license = models.FileField(upload_to="checkout_files")

	def __str__(self):
		return "Don't create a new entry!"

class Receipt_template(models.Model):
	receipt = models.FileField(upload_to="checkout_files")
	
	def __str__(self):
		return "Don't create a new entry!"

class Seller(models.Model):
	name = models.CharField(max_length=999)
	email = models.CharField(max_length=999)
	website = models.CharField(max_length=999)
	company = models.CharField(max_length=999, default="Emart Auto OÜ")

	def __str__(self):
		return "Don't create a new entry!"

class Mail_list(models.Model):
	email = models.CharField(max_length=999)

	def __str__(self):
		return self.email

class Stripe_key(models.Model):
	test = models.CharField(max_length=999, blank=True, default="Test")
	public_key = models.CharField(max_length=999)
	private_key = models.CharField(max_length=999)

	def __str__(self):
		return self.test