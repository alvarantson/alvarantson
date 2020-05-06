from django.shortcuts import render
from .models import Social_media, About
# Create your views here.
def contact(request):



	return render(request, "contact.html", {
		'about' : About.objects.all().first(),
		'socials' : Social_media.objects.all()
		})