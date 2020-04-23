from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def checkout(request):
	request.session["shopping_cart"]=[{
				"beat_id": "1",
				"lease_id": "1",
				"name": "mp3 lease",
				"beat_name": "Tense",
				"price": "25.50"
				}]	
	request.session["shopping_cart_total"] = 25.50
	return render(request, "checkout.html", {})

def empty(request):
	request.session["shopping_cart"]=[]
	return HttpResponseRedirect(request.META['HTTP_REFERER'])
