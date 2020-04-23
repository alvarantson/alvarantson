from django.urls import path
from . import views

urlpatterns = [
    path("", views.releases),
    path("import/", views.import_releases),
    path("tests/", views.tests)
]