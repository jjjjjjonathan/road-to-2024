from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import Division, Match, Team


def index(request):
    divisions = Division.objects.all()
    context = {"divisions": divisions}
    return render(request, "division/index.html", context)


def division(request, division_id):
    division = get_object_or_404(Division, pk=int(division_id))

    # date = datetime.now()

    # if request.method == "GET" and "date" in request.GET:
    #     date = request.GET["date"]

    teams = division.teams.with_table_records()

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
    teams = division.teams.order_by("name")
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
    context = {
        "team": team,
        "matches": sorted_matches,
        "wins": team.wins_in_2023(),
        "losses": team.losses_in_2023(),
        "draws": team.draws_in_2023(),
    }
    return render(request, "team/team.html", context)
