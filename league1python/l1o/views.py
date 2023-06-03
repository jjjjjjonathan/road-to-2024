from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Division
from django.db.models import Count, F, Q


def index(request):
    divisions = Division.objects.all()
    context = {"divisions": divisions}
    return render(request, "division/index.html", context)


def detail(request, division_id):
    division = get_object_or_404(Division, pk=division_id)
    teams = (
        division.team_division.annotate(
            wins=(
                Count(
                    "home_matches",
                    filter=Q(
                        home_matches__home_score__gt=F("home_matches__away_score")
                    ),
                )
                + Count(
                    "away_matches",
                    filter=Q(
                        away_matches__away_score__gt=F("away_matches__home_score")
                    ),
                )
            ),
            losses=(
                Count(
                    "home_matches",
                    filter=Q(
                        home_matches__home_score__lt=F("home_matches__away_score")
                    ),
                )
                + Count(
                    "away_matches",
                    filter=Q(
                        away_matches__away_score__lt=F("away_matches__home_score")
                    ),
                )
            ),
            draws=(
                Count(
                    "home_matches",
                    filter=Q(
                        home_matches__home_score__exact=F("home_matches__away_score")
                    ),
                )
                + Count(
                    "away_matches",
                    filter=Q(
                        away_matches__away_score__exact=F("away_matches__home_score")
                    ),
                )
            ),
        )
        .annotate(points_in_2023=(F("wins") * 3) + F("draws"))
        .annotate(total_points=(F("points_in_2022") * 0.75) + F("points_in_2023"))
        .order_by("-total_points")
    )

    context = {"division": division, "teams": teams}
    return render(request, "division/division.html", context)
