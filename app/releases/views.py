from django.shortcuts import render
from .models import Release, Release_stats
from .fetcher import update
from django.http import HttpResponseRedirect, HttpResponse
from .csv import to_csv_response, csv_to_db
from .forms import UploadFileForm
# Create your views here.
def releases(request):
	default_release_date1 = "1880-01-01"
	default_release_date2 = "2100-01-01"
	default_artist = ""
	default_name = ""
	default_role = ""
	list_of_releases_unsorted = Release.objects.filter(release_date__range=[default_release_date1,default_release_date2],)

	if request.POST:

		if request.POST["submit-btn"] == "export-releases":

			return to_csv_response(list(Release.objects.all()), "release_export")

		if request.POST["submit-btn"] == "update-all-releases":

			for item in Release.objects.all():
				update(item)
			return HttpResponseRedirect(request.path)

		if request.POST["submit-btn"] == "search":

			release_date1 = request.POST["release_date1"]
			release_date2 = request.POST["release_date2"]
			artist = request.POST["artist"]
			name = request.POST["name"]
			role = request.POST["role"]

			default_release_date1 = release_date1
			default_release_date2 = release_date2
			default_artist = artist
			default_name = name
			default_role = role

			if release_date1 != default_release_date1 or release_date2 != default_release_date2:
				list_of_releases_unsorted = list_of_releases_unsorted.filter(release_date__range=[default_release_date1,default_release_date2])

			if artist != "":
				list_of_releases_unsorted = list_of_releases_unsorted.filter(artist__icontains=artist)

			if name != "":
				list_of_releases_unsorted = list_of_releases_unsorted.filter(name__icontains=name)

			if role != "":
				list_of_releases_unsorted = list_of_releases_unsorted.filter(role__icontains=role)

	list_of_releases = []
	youtube_views_total = 0
	youtube_likes_total = 0
	youtube_dislikes_total = 0
	soundcloud_views_total = 0
	soundcloud_likes_total = 0
	soundcloud_reposts_total = 0
	soundcloud_comments_total = 0

	for item in list_of_releases_unsorted.order_by('-release_date'):
		release = {
			"id":item.id,
			"name":item.name, 
			"artist":item.artist, 
			"role":item.role, 
			"release_date": item.release_date,
			"youtube_url":item.youtube_url,
			"soundcloud_url":item.soundcloud_url,
			"spotify_url":item.spotify_url
			}

		if len( Release_stats.objects.filter(release=item) ) == 0:
			update(item)

		stats = Release_stats.objects.filter(release=item).order_by('-fetch_date').first()
		stats_history = Release_stats.objects.filter(release=item).order_by('-fetch_date')
		
		try:
			youtube_views_total += int(stats.youtube_views)
		except:
			pass
		try:
			youtube_likes_total += int(stats.youtube_likes)
		except:
			pass
		try:
			youtube_dislikes_total += int(stats.youtube_dislikes)

		except:
			pass
		try:
			soundcloud_views_total += int(stats.soundcloud_views)
		except:
			pass
		try:
			soundcloud_likes_total += int(stats.soundcloud_likes)
		except:
			pass
		try:
			soundcloud_reposts_total += int(stats.soundcloud_reposts)
		except:
			pass
		try:
			soundcloud_comments_total += int(stats.soundcloud_comments)
		except:
			pass

		release["stats"] = stats
		release["stats_history"] = stats_history

		list_of_releases.append(release)


	return render(request, "releases.html", {
		"releases":list_of_releases,
		"default_release_date1":default_release_date1,
		"default_release_date2":default_release_date2,
		"default_name":default_name,
		"default_artist":default_artist,
		"default_role":default_role,
		"youtube_views_total":youtube_views_total,
		"youtube_likes_total":youtube_likes_total,
		"youtube_dislikes_total":youtube_dislikes_total,
		"soundcloud_views_total":soundcloud_views_total,
		"soundcloud_likes_total":soundcloud_likes_total,
		"soundcloud_reposts_total":soundcloud_reposts_total,
		"soundcloud_comments_total":soundcloud_comments_total
		})

def import_releases(request):

	form = UploadFileForm()

	if request.POST:

		if request.POST["submit-btn"] == "download-example":
			list_of_releases = []

			example_release = Release(
				name="Salsa", 
				artist="Artist name", 
				role="Songwriter", 
				youtube_url="https://www.youtube.com/watch?v=aVtWSZOttC0",
				soundcloud_url="https://soundcloud.com/d-j-casual/dj-alex-sensation-salsa-mix-eddy-santiago-old-skool-salsa",
				spotify_url="",
				release_date= "2020-01-30"
				)
			list_of_releases.append(example_release)

			example_release = Release(
				name="Salsa2", 
				artist="Artist name", 
				role="Songwriter", 
				youtube_url="https://www.youtube.com/watch?v=aVtWSZOttC0",
				soundcloud_url="https://soundcloud.com/d-j-casual/dj-alex-sensation-salsa-mix-eddy-santiago-old-skool-salsa",
				spotify_url="",
				release_date= "2020-01-31"
				)
			list_of_releases.append(example_release)

			return to_csv_response(list_of_releases, "example")

		if request.POST["submit-btn"] == "upload-releases":

			form = UploadFileForm(request.POST, request.FILES)

			if request.POST["empty"]:
				Release.objects.all().delete()

			csv_to_db(request.FILES["file"])

	return render(request, "import_releases.html", {"form":form})

def tests(request):
	reliis = Release.objects.filter(artist__icontains="EmM").first()
	print(reliis)
	return HttpResponse(str(update(reliis)))