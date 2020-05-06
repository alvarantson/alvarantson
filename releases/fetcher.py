import requests, re
from .models import Release_stats

def only_digits(raw):
	return re.sub('\D', '', raw)

def fetch_youtube_stats(url):
	if url != "":
		r = requests.get(url)

		views_sep1 = '<div class="watch-view-count">'
		views_sep2 = 'vaatamist'

		likes_sep1 = 'likeCount'

		dislikes_sep1 = 'dislikeCount'

		try:
			view_count = only_digits( str(r.text).split(views_sep1)[1].split(views_sep2)[0] )
		except Exception as e:
			print(e)
			view_count = "0"
		try:
			like_count = only_digits( str(r.text).split(likes_sep1)[1] )
		except Exception as e:
			print(e)
			like_count = "0"
		try:
			dislike_count = only_digits( str(r.text).split(dislikes_sep1)[1] )
		except Exception as e:
			print(e)
			dislike_count = "0"
		
	else:
		view_count = "0"
		like_count = "0"
		dislike_count = "0"
	return {
		"views":view_count,
		"likes":like_count,
		"dislikes":dislike_count
		}

def fetch_soundcloud_stats(url):
	if url != "":
		r = requests.get(url)

		views_sep1 = '<meta property="soundcloud:play_count" content="'
		views_sep2 = '">'

		likes_sep1 = '<meta property="soundcloud:like_count" content="'
		likes_sep2 = '">'

		reposts_sep1 = '<meta property="soundcloud:reposts_count" content="'
		reposts_sep2 = '">'

		comments_sep1 = '<meta property="soundcloud:comments_count" content="'
		comments_sep2 = '">'

		try:
			view_count = only_digits( str(r.text).split(views_sep1)[1].split(views_sep2)[0] )
		except Exception as e:
			print(e)
			view_count = "0"
		try:
			like_count = only_digits( str(r.text).split(likes_sep1)[1].split(likes_sep2)[0] )
		except Exception as e:
			print(e)
			like_count = "0"
		try:
			repost_count = only_digits( str(r.text).split(reposts_sep1)[1].split(reposts_sep2)[0] )
		except Exception as e:
			print(e)
			repost_count = "0"
		try:
			comment_count = only_digits( str(r.text).split(comments_sep1)[1].split(comments_sep2)[0] )
		except Exception as e:
			print(e)
			comment_count = "0"

		

	else:
		view_count = "0"
		like_count = "0"
		repost_count = "0"
		comment_count = "0"
	return {
		"views":view_count,
		"likes":like_count,
		"reposts":repost_count,
		"comments":comment_count
		}


def update(release):
	youtube_url = release.youtube_url
	soundcloud_url = release.soundcloud_url
	spotify_url = release.spotify_url

	youtube_stats = fetch_youtube_stats(youtube_url)
	soundcloud_stats = fetch_soundcloud_stats(soundcloud_url)
	old = Release_stats.objects.filter(release=release).order_by('-fetch_date').first()

	try:
		if youtube_stats["views"] == "0":
			youtube_stats["views"] = old.youtube_views
			youtube_stats["likes"] = old.youtube_likes
			youtube_stats["dislikes"] = old.youtube_dislikes

		if soundcloud_stats["views"] == "0":
			soundcloud_stats["views"] = old.soundcloud_views
			soundcloud_stats["likes"] = old.soundcloud_likes
			soundcloud_stats["comments"] = old.soundcloud_comments
			soundcloud_stats["reposts"] = old.soundcloud_reposts
	except:
		pass



	Release_stats.objects.create(
		release = release,
		youtube_views = youtube_stats["views"],
		youtube_likes = youtube_stats["likes"],
		youtube_dislikes = youtube_stats["dislikes"],
		soundcloud_views = soundcloud_stats["views"],
		soundcloud_likes = soundcloud_stats["likes"],
		soundcloud_comments = soundcloud_stats["comments"],
		soundcloud_reposts = soundcloud_stats["reposts"]
		)