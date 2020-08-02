from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.beats),
    re_path(r'^(?P<beat_name>.*)/$', views.beat, name="beat")
]