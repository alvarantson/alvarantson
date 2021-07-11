from django.shortcuts import render
from .models import Video
# Create your views here.
def videos(request):


	#for item in Video.objects.filter(yt_link__contains="/watch"):
	#	item.yt_link = item.yt_link.replace('/watch', '/embed')
	#	item.save()

	return render(request, "videos.html", {
		'videos' : Video.objects.all()[::-1]
		})
