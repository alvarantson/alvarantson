from django.urls import path, re_path
from . import views

urlpatterns = [
    path("", views.checkout),
    path("empty/", views.empty),
    re_path(r'^remove/(?P<beat_id>\d+),(?P<lease_id>\d+)/$', views.remove, name="remove"),
    re_path(r'^add/(?P<lease_id>\d+)/$', views.add, name="add"),
    path("charge/", views.charge, name='charge'),
    path("download_receipt/", views.download_receipt),
    re_path(r'^download_license/(?P<lease_id>\d+)/$', views.download_license, name="download_license"),
    re_path(r'^download_files/(?P<random_str>.*)$', views.download_files, name="download_files"),
    path("complete/", views.complete),
]