from django.urls import path
from . import views

urlpatterns = [
    path("", views.checkout),
    path("empty/", views.empty),
]