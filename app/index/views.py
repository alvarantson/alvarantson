from django.shortcuts import render
from beats.models import Beat
from contact.models import Social_media, About
from releases.models import Release
# Create your views here.
def index(request):

	beats = Beat.objects.all().order_by('-date')[:6]
	releases = Release.objects.all().order_by('-release_date')[:5]
	the_stu = About.objects.all()[0].the_stu

	return render(request, "index.html", {
		'beats' : beats,
		'socials' : Social_media.objects.all(),
		'flickr' : Social_media.objects.filter(url__contains='flick')[0],
		'releases' : releases,
		"the_stu" : the_stu
		})