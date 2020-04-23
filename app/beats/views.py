from django.shortcuts import render
from .models import Beat, Lease_option
# Create your views here.
def beats(request):
	beats_raw = Beat.objects.all()
	beats = []
	for beat in beats_raw:
		beat_holder = {"beat":beat}
		beat_holder["lease_options"] = Lease_option.objects.filter(beat=beat)
		beat_holder["lease_width"] = str(100/len(beat_holder["lease_options"]))

		beats.append(beat_holder)

	if request.POST:

		if "add-to-cart-beat" in request.POST["submit-btn"]:

			if not "shopping_cart" in request.session:
				request.session["shopping_cart"] = []

			item = Lease_option.objects.get(id=request.POST["submit-btn"].replace("add-to-cart-beat_",""))
			add_to_cart = {
				"beat_id": item.beat.id,
				"lease_id": item.id,
				"name": item.name,
				"beat_name": item.beat.name,
				"price": item.price
				}

			request.session["shopping_cart"].append(add_to_cart)




	return render(request, "beats.html", {
		"beats": beats
		})