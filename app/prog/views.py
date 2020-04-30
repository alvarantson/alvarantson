from django.shortcuts import render
from .models import Project
from contact.models import Social_media
# Create your views here.
def prog(request):
	return render(request, 'prog.html', {
		'projects' : Project.objects.all(),
		'linkedin' : Social_media.objects.filter(url__contains='linked')[0]
		})