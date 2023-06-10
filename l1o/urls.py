from django.urls import path

from . import views

app_name = "l1o"

urlpatterns = [
    path("", views.index, name="index"),
    path("division/<int:division_id>/", views.division, name="division"),
    path("match/<int:e2e_id>/edit", views.edit, name="edit"),
    path("match/update", views.update, name="update"),
    path("team/<int:team_id>/", views.team, name="team"),
]
