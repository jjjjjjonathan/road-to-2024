from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:division_id>/", views.detail, name="division_detail"),
]
