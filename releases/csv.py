from django.http import HttpResponse
from .models import Release
import re
def str_to_date(text):
	return re.match(r"(\d{1,4}([.\-/])\d{1,2}([.\-/])\d{1,2})",text).group(0)

def to_csv(items):
	header = "name\tartist\trole\tyoutube_url\tsoundcloud_url\tspotify_url\trelease_date\tgenre\n"
	for item in items:
		header += item.name+"\t"
		header += item.artist+"\t"
		header += item.role+"\t"
		header += item.youtube_url+"\t"
		header += item.soundcloud_url+"\t"
		header += item.spotify_url+"\t"
		header += str(item.release_date)+"\t"
		header += item.genre+"\n"
	return header


def to_csv_response(items, filename):
	content = to_csv(items)
	response = HttpResponse(content, content_type='application/text charset=utf-8')
	response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
	return response


def csv_to_db(import_file):
	conv = import_file.file.read().decode("UTF-8")
	for row in conv.split("\n"):
		if row == "":
			continue
		if "name" == row.split("\t")[0].replace(" ",""):
			continue

		try:
			name = row.split("\t")[0]
		except:
			name = ""
		try:
			artist=row.split("\t")[1] 
		except:
			artist = ""
		try:
			role=row.split("\t")[2]  
		except:
			role = ""
		try:
			youtube_url=row.split("\t")[3] 
		except:
			youtube_url = ""
		try:
			soundcloud_url=row.split("\t")[4] 
		except:
			soundcloud_url = ""
		try:
			spotify_url=row.split("\t")[5] 
		except:
			spotify_url = ""
		try:
			release_date= str_to_date(row.split("\t")[6])
		except:
			release_date = ""
		try:
			genre= row.split("\t")[7]
		except:
			genre = ""
		item = Release(
			name = name,
			artist = artist,
			role = role,
			youtube_url = youtube_url,
			soundcloud_url = soundcloud_url,
			spotify_url = spotify_url,
			genre = genre
			)
		if release_date != "":
			item.release_date = release_date
		item.save()

