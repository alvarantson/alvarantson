from django.contrib import admin
from .models import Buy_history, License_template, Receipt_template, Seller
# Register your models here.
admin.site.register(Buy_history)
admin.site.register(License_template)
admin.site.register(Receipt_template)
admin.site.register(Seller)