from django.db import models

# Create your models here.
class Buy_history(models.Model):
	date = models.DateField(auto_now_add=True)
	shopping_cart = models.TextField(blank=True)
