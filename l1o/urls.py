from django.urls import path
from .views import IndexView

from . import views

app_name = "l1o"

urlpatterns = [
    path("", IndexView.as_view()),
    path("division/<int:division_id>/", views.division, name="division"),
    path("match/<int:e2e_id>/edit", views.edit, name="edit"),
    path("match/update", views.update, name="update"),
    path("team/<int:team_id>/", views.team, name="team"),
]
