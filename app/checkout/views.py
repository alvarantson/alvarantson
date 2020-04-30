from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import stripe
from django.conf import settings
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm
from .models import Buy_history, License_template, Receipt_template, Seller
from beats.models import Lease_option
from LEHT.settings import BASE_DIR
import pdfkit
from datetime import datetime
# Create your views here.
def read_and_clean_template(template_path):
	with open(template_path,'r') as fm:
		template = str(fm.read())
	template = template.split("<body")[1]
	template = "<div "+template+"</div>"
	template = template.replace("</body>","")
	template = template.replace("</html>","")
	return template

def read_and_replace_template(template_path, context):
	with open(template_path,'r') as fm:
		template = str(fm.read())

	for key in context:
		template = template.replace(key, str(context[key]))

	return template

def checkout(request):
	if not "shopping_cart" in request.session or request.session["shopping_cart"] == None:
		request.session["shopping_cart"] = []
		request.session["shopping_cart_total"] = 0
	request.session["shopping_cart_total_int"] = int(float(request.session["shopping_cart_total"])*100)
	
	license = read_and_clean_template(BASE_DIR+License_template.objects.all().first().license.url)

	return render(request, "checkout.html", {
		"stripe_public_key":settings.STRIPE_PUBLISHABLE_KEY,
		"license": license
		})


def empty(request):
	request.session["shopping_cart"] = []
	request.session["shopping_cart_total"] = 0
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


def remove(request, beat_id, lease_id):
	for i in range(len(request.session["shopping_cart"])):
		item = request.session["shopping_cart"][i]
		if str(item["beat_id"]) == str(beat_id) and str(item["lease_id"]) == str(lease_id):
			request.session["shopping_cart_total"] -= item["price"]
			request.session["shopping_cart"].pop(i)
			break
	return HttpResponseRedirect(str(request.META['HTTP_REFERER']))


def add(request, lease_id):
	if not "shopping_cart" in request.session or request.session["shopping_cart"] == None:
		request.session["shopping_cart"] = []
		request.session["shopping_cart_total"] = 0

	item = Lease_option.objects.get(id=lease_id)
	add_to_cart = {
		"beat_id": item.beat.id,
		"lease_id": item.id,
		"name": item.name,
		"beat_name": item.beat.name,
		"price": item.price
		}
	request.session["shopping_cart_total"] += item.price
	request.session["shopping_cart"].append(add_to_cart)

	return HttpResponseRedirect(str(request.META['HTTP_REFERER']))


def charge(request): # https://testdriven.io/blog/django-stripe-tutorial/
	if request.method == 'POST':
		stripe.api_key = settings.STRIPE_SECRET_KEY
		charge = stripe.Charge.create(
			amount=request.session["shopping_cart_total_int"],
			currency='eur',
			description='Alvar Antson beats',
			source=request.POST['stripeToken']
		)
		shopping_cart = request.session["shopping_cart"]
		shopping_cart_total = request.session["shopping_cart_total"]

		Buy_history.objects.create(
			shopping_cart = shopping_cart,
			shopping_cart_total = request.session["shopping_cart_total"],
			buyer_first_name = request.POST["buyer_first_name"],
			buyer_last_name = request.POST["buyer_last_name"],
			buyer_artist_name = request.POST["buyer_artist_name"],
			buyer_email = request.POST["buyer_email"],
			buyer_address = request.POST["buyer_address"]
			)
		buy_history = Buy_history.objects.filter(shopping_cart = shopping_cart, buyer_email = request.POST["buyer_email"], buyer_address = request.POST["buyer_address"])[0]
		request.session["Buy_history"] = {
			"shopping_cart":shopping_cart,
			"shopping_cart_total":buy_history.shopping_cart_total,
			"buyer_first_name":buy_history.buyer_first_name,
			"buyer_last_name":buy_history.buyer_last_name,
			"buyer_artist_name":buy_history.buyer_artist_name,
			"buyer_email":buy_history.buyer_email,
			"buyer_address":buy_history.buyer_address,
			"buy_id":buy_history.id,
			"date":str(buy_history.date.strftime("%d %B, %Y"))
			}
	#	request.session["shopping_cart"] = []
	#	request.session["shopping_cart_total"] = 0
	#	request.session["shopping_cart_total_int"] = 0
		return render(request, 'charge.html', {
			"shopping_cart":shopping_cart,
			"shopping_cart_total":shopping_cart_total
			})



def download_license(request, lease_id):
#	content = read_and_clean_template(BASE_DIR+License_template.objects.all().first().license.url)
#	content.replace()
	filename = "test"
	seller = Seller.objects.all()[0]
	lease = Lease_option.objects.get(id=lease_id)
	buy_history = request.session["Buy_history"]
	template = read_and_replace_template(BASE_DIR+License_template.objects.all().first().license.url, {
		"&lt;TRACK_NAME&gt;": lease.beat.name,
		"&lt;TRACK_PRICE&gt;": lease.price,
		"&lt;LICENSE&gt;": lease.name,
		"&lt;LICENSE_DESCRIPTION&gt;": lease.description,
		"&lt;DATE&gt;": buy_history["date"],
		"&lt;SELLER_NAME&gt;": seller.name,
		"&lt;SELLER_EMAIL&gt;": seller.email,
		"&lt;FIRST_NAME&gt;": buy_history["buyer_first_name"],
		"&lt;LAST_NAME&gt;": buy_history["buyer_last_name"],
		"&lt;BUYER_EMAIL&gt;": buy_history["buyer_email"],
		"&lt;ARTIST_NAME&gt;": buy_history["buyer_artist_name"],
		"&lt;AFTER_VIEWS&gt;": lease.after_views,
		"&lt;PERCENT_AFTER_VIEWS&gt;": lease.percent_after_views,
		"ā‚¬":"€"
		})
#	template = pdfkit.from_string(template, filename+'.pdf')
	response = HttpResponse(template, content_type='application/text charset=utf-8')
	response['Content-Disposition'] = 'attachment; filename="{}.html"'.format(filename)
	return response
	
def download_receipt(request):
#	content = read_and_clean_template(BASE_DIR+Receipt_template.objects.all().first().receipt.url)
#	content.replace()
	filename = "test"
	seller = Seller.objects.all()[0]
	shopping_cart = request.session["shopping_cart"]
	buy_history = request.session["Buy_history"]
	context = {
		"&lt;ORDER_ID&gt;": "Order: "+str(buy_history["buy_id"]),
		"&lt;BUYER_NAME&gt;": buy_history["buyer_first_name"]+" "+buy_history["buyer_last_name"],
		"&lt;BUYER_EMAIL&gt;": buy_history["buyer_email"],
		"&lt;ARTIST_NAME&gt;": buy_history["buyer_artist_name"],
		"&lt;SELLER_NAME&gt;": seller.name,
		"&lt;SELLER_EMAIL&gt;": seller.email,
		"&lt;WEBSITE&gt;": seller.website,
		"&lt;DATE&gt;": buy_history["date"],
		"&lt;ORDER_SUM&gt;": request.session["shopping_cart_total"],
		"ā‚¬":"€"
		}
	for i in ["1","2","3","4","5","6","7"]: # DEFAULTS
		context["&lt;ITEM_NAME_"+i+"&gt;"] = ""
		context["&lt;ITEM_PRICE_"+i+"&gt;"] = ""

	for i in range(len(shopping_cart)):
		context["&lt;ITEM_NAME_"+str(i+1)+"&gt;"] = "\""+shopping_cart[i]["beat_name"]+"\" - "+shopping_cart[i]["name"]
		context["&lt;ITEM_PRICE_"+str(i+1)+"&gt;"] = shopping_cart[i]["price"]

	template = read_and_replace_template(BASE_DIR+Receipt_template.objects.all().first().receipt.url, context)
#	template = pdfkit.from_string(template, filename+'.pdf')
#	print(template)
	response = HttpResponse(template, content_type='application/text charset=utf-8')
	response['Content-Disposition'] = 'attachment; filename="{}.html"'.format(filename)
	return response


def download_files(request, lease_id):
#	content = read_and_clean_template(BASE_DIR+Receipt_template.objects.all().first().receipt.url)
#	content.replace()
	lease = Lease_option.objects.get(id=lease_id)
	if lease.file_url != "":
		return HttpResponseRedirect(lease.file_url)
	else:
		files = lease.file
		filename = lease.file.name
		response = HttpResponse(files, content_type='audio/mpeg')
		print(lease)
		response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
		return response

def complete(request):
	request.session["shopping_cart"] = []
	request.session["shopping_cart_total"] = 0
	request.session["shopping_cart_total_int"] = 0
	return HttpResponseRedirect("/")