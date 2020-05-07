from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
import stripe
from django.conf import settings
from .models import Buy_history, License_template, Receipt_template, Seller, Mail_list, Stripe_key
from beats.models import Lease_option
from LEHT.settings import BASE_DIR
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

	template += '<script type="text/javascript">window.print();</script>'

	return template

def checkout(request):
	if not "shopping_cart" in request.session or request.session["shopping_cart"] == None:
		request.session["shopping_cart"] = []
		request.session["shopping_cart_total"] = 0
	request.session["shopping_cart_total_int"] = int(float(request.session["shopping_cart_total"])*100)
	
	license = read_and_clean_template(BASE_DIR+License_template.objects.all().first().license.url)
	stripe_public_key = Stripe_key.objects.all()[0].public_key


	return render(request, "checkout.html", {
		"stripe_public_key":stripe_public_key,
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
		"price": item.price,
		"random_str": item.random_str
		}
	request.session["shopping_cart_total"] += item.price
	request.session["shopping_cart"].append(add_to_cart)

	return HttpResponseRedirect(str(request.META['HTTP_REFERER']))


def charge(request): # https://testdriven.io/blog/django-stripe-tutorial/
	if request.method == 'POST':
		stripe_private_key = Stripe_key.objects.all()[0].private_key
		stripe.api_key = stripe_private_key

		description = (
			'alvarantson.com -' + 
			request.POST["buyer_first_name"] + " " + 
			request.POST["buyer_last_name"] + " - " + 
			request.POST["buyer_email"]
			)

		charge = stripe.Charge.create(
			amount=request.session["shopping_cart_total_int"],
			currency='eur',
			description= description,
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

		buy_history.receipt = download_receipt(request).content.decode('utf-8')
		buy_history.save()

		try:
			if request.POST["mail_list"]:
				Mail_list.objects.create(email=request.POST["buyer_email"])
		except:
			pass
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
		"<head>": (
			"<head><title>" + 
			lease.beat.name + "_" +
			lease.name + "_" +
			buy_history["buyer_artist_name"] + "_" +
			"_license</title>"
			),
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
	response = HttpResponse(template)
	#response = HttpResponse(template, content_type='application/text charset=utf-8')
	#response['Content-Disposition'] = 'attachment; filename="{}.html"'.format(filename)
	return response
	

def download_receipt(request):
#	content = read_and_clean_template(BASE_DIR+Receipt_template.objects.all().first().receipt.url)
#	content.replace()
	filename = "test"
	seller = Seller.objects.all()[0]
	shopping_cart = request.session["shopping_cart"]
	buy_history = request.session["Buy_history"]
	context = {
		"<head>": "<head><title>"+str(buy_history["buy_id"])+"_aacom</title>",
		"&lt;ORDER_ID&gt;": "Order: "+str(buy_history["buy_id"]),
		"&lt;BUYER_NAME&gt;": buy_history["buyer_first_name"]+" "+buy_history["buyer_last_name"],
		"&lt;BUYER_EMAIL&gt;": buy_history["buyer_email"],
		"&lt;ARTIST_NAME&gt;": buy_history["buyer_artist_name"],
		"&lt;SELLER_NAME&gt;": seller.name,
		"&lt;SELLER_EMAIL&gt;": seller.email,
		"&lt;COMPANY&gt;": seller.company,
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
	response = HttpResponse(template)
	filename = str(buy_history["buy_id"])
	#response = HttpResponse(template, content_type='application/text charset=utf-8')
	#response['Content-Disposition'] = 'attachment; filename="{}.html"'.format(filename)
	return response


def download_files(request, random_str):
	lease = Lease_option.objects.get(random_str=random_str)
	if lease.dropbox_url != "":
		url = lease.dropbox_url.replace("dl=0","dl=1")
		return HttpResponseRedirect(url)
	else:
		files = lease.file
		response = HttpResponse(files, content_type='audio/mpeg')
		return response


def complete(request):
	request.session["shopping_cart"] = []
	request.session["shopping_cart_total"] = 0
	request.session["shopping_cart_total_int"] = 0
	return HttpResponseRedirect("/")