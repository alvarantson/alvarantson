from django.contrib import admin
from .models import Buy_history, License_template, Receipt_template, Seller, Stripe_key, Mail_list
# Register your models here.
admin.site.register(Buy_history)
admin.site.register(License_template)
admin.site.register(Receipt_template)
admin.site.register(Seller)
admin.site.register(Stripe_key)
admin.site.register(Mail_list)