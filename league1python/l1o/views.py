from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect

from .models import Division, Match, Team
from django.db.models import Count, F, Q


def index(request):
    divisions = Division.objects.all()
    context = {"divisions": divisions}
    return render(request, "division/index.html", context)


def division(request, division_id):
    division = get_object_or_404(Division, pk=int(division_id))

    date = datetime.now()

    if request.method == "GET" and "date" in request.GET:
        date = request.GET["date"]

    teams = (
        division.team_division.annotate(
            matches_played=(
                Count(
                    "home_matches",
                    distinct=True,
                    filter=Q(home_matches__scheduled_time__lte=date),
                )
                + Count(
                    "away_matches",
                    distinct=True,
                    filter=Q(away_matches__scheduled_time__lte=date),
                )
            ),
            wins=(
                Count(
                    "home_matches",
                    filter=Q(home_matches__home_score__gt=F("home_matches__away_score"))
                    & Q(home_matches__scheduled_time__lte=date),
                    distinct=True,
                )
                + Count(
                    "away_matches",
                    filter=Q(away_matches__away_score__gt=F("away_matches__home_score"))
                    & Q(away_matches__scheduled_time__lte=date),
                    distinct=True,
                )
            ),
            losses=(
                Count(
                    "home_matches",
                    filter=Q(home_matches__home_score__lt=F("home_matches__away_score"))
                    & Q(home_matches__scheduled_time__lte=date),
                    distinct=True,
                )
                + Count(
                    "away_matches",
                    filter=Q(away_matches__away_score__lt=F("away_matches__home_score"))
                    & Q(away_matches__scheduled_time__lte=date),
                    distinct=True,
                )
            ),
            draws=(
                Count(
                    "home_matches",
                    filter=Q(
                        home_matches__home_score__exact=F("home_matches__away_score")
                    )
                    & Q(home_matches__scheduled_time__lte=date),
                    distinct=True,
                )
                + Count(
                    "away_matches",
                    filter=Q(
                        away_matches__away_score__exact=F("away_matches__home_score")
                    )
                    & Q(away_matches__scheduled_time__lte=date),
                    distinct=True,
                )
            ),
        )
        .annotate(points_in_2023=(F("wins") * 3) + F("draws"))
        .annotate(total_points=(F("points_in_2022") * 0.75) + F("points_in_2023"))
        .order_by("-total_points")
    )

    context = {
        "division": division,
        "teams": teams,
        "filter_date": (
            request.method == "GET" and "date" in request.GET and request.GET["date"]
        )
        or None,
    }
    return render(request, "division/division.html", context)


def new(request, division_id):
    division = get_object_or_404(Division, pk=division_id)
    teams = division.team_division.order_by("name")
    context = {"name": division.name, "teams": teams, "division_id": division.id}
    return render(request, "match/new.html", context)


def create(request):
    division = Division.objects.get(pk=int(request.POST["division-id"]))
    home_team = Team.objects.get(pk=int(request.POST["home-team"]))
    away_team = Team.objects.get(pk=int(request.POST["away-team"]))

    Match.objects.create(
        home_team=home_team,
        away_team=away_team,
        division=division,
        home_score=int(request.POST["home-score"]),
        away_score=int(request.POST["away-score"]),
        e2e_id=int(request.POST["e2e-id"]),
        scheduled_time=request.POST["scheduled-time"],
    )

    return redirect(f"/division/{division.id}")


def team(request, team_id):
    team = get_object_or_404(Team, pk=int(team_id))
    home_matches = team.home_matches.all()
    away_matches = team.away_matches.all()
    matches = home_matches | away_matches
    sorted_matches = matches.distinct().order_by("scheduled_time")
    print(sorted_matches)
    context = {"team": team, "matches": sorted_matches}
    return render(request, "team/team.html", context)
