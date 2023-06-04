from django.urls import path

from . import views

app_name = "l1o"

urlpatterns = [
    path("", views.index, name="index"),
    path("division/<int:division_id>/", views.detail, name="division"),
    path("division/<int:division_id>/new", views.new, name="new"),
    path("match/create/", views.create, name="create"),
]
