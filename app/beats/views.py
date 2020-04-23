from django.shortcuts import render
from .models import Beat
# Create your views here.
def beats(request):
	beats = Beat.objects.all()

	if request.POST:

		if "add-to-cart-beat" in request.POST["submit-btn"]:

			if not "shopping_cart" in request.session:
				request.session["shopping_cart"] = []

			request.session["shopping_cart"].append(request.POST["submit-btn"].replace("add-to-cart-beat_","")) 




	return render(request, "beats.html", {
		"beats": beats
		})