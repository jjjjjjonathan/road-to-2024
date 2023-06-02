from django.http import HttpResponse
from django.template import loader

from .models import Division
from django.db.models import Count, F, Q


def index(request):
    division = Division.objects.get(pk=1)
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

    template = loader.get_template("division/index.html")
    context = {"division": division, "teams": teams}
    return HttpResponse(template.render(context, request))


def team_detail(request, team_id):
    return HttpResponse("You're looking at team %s" % team_id)
