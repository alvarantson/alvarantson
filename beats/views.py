from django.shortcuts import render
from .models import Beat, Lease_option
# Create your views here.
def beats(request):
	beats_raw = Beat.objects.all()
	tags_raw = []
	tags_selected = []
	searched = ""
	

	# FILTERS
	if request.POST:

		if request.POST["beat_name"] != "":
			beats_raw = beats_raw.filter(name__contains=request.POST["beat_name"])
			searched = request.POST["beat_name"]

		for key in request.POST:
			if "tag_" in key:
				beats_raw = beats_raw.filter(tags__contains=key.replace("tag_",""))
				tags_selected.append(key.replace("tag_",""))


	for beat in beats_raw:
		for tag in beat.tags.replace(", ", ",").replace(" ,", ",").split(","):
			if tag not in tags_raw:
				tags_raw.append(tag)

	beats = []
	for beat in beats_raw:
		beat_holder = {"beat":beat}
		beat_holder["lease_options"] = []
		lease_options = Lease_option.objects.filter(beat=beat)
		for i in range(int(len(lease_options)/2) + 1):
			pair = []
			try:
				pair.append(lease_options[i*2])
			except:
				pass
			try:
				pair.append(lease_options[i*2+1])
			except:
				beat_holder["lease_options"].append(pair)
				break
			beat_holder["lease_options"].append(pair)

		beats.append(beat_holder)



	return render(request, "beats.html", {
		"beats": beats,
		"tags": tags_raw,
		"tags_selected": tags_selected,
		"searched": searched
		})

def beat(request, beat_name):
	beat = Beat.objects.get(name=beat_name)
	return render(request, "beat.html", {
		"beat": beat,
		"leases": Lease_option.objects.filter(beat=beat)
		})