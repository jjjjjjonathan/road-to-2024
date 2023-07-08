from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from .models import Division, Match, Team
from .forms import MatchForm


class IndexView(generic.ListView):
    template_name = "division/index.html"
    context_object_name = "divisions"

    def get_queryset(self):
        return Division.objects.only("id", "name")


def division(request, division_id):
    division = get_object_or_404(Division, pk=int(division_id))

    teams = division.teams.with_table_records()
    max_points_teams = teams.order_by("-max_possible_points")
    promotion_threshold = max_points_teams[
        division.number_of_promoted_teams
    ].max_possible_points
    relegation_threshold = teams[division.number_of_promoted_teams - 1].total_points

    context = {
        "division": division,
        "teams": teams,
        "promotion_threshold": promotion_threshold,
        "relegation_threshold": relegation_threshold,
        "number_of_successful_teams": division.number_of_promoted_teams,
    }
    return render(request, "division/division.html", context)


def edit(request, e2e_id):
    match = (
        Match.objects.select_related("home_team")
        .select_related("away_team")
        .select_related("division")
        .get(e2e_id=e2e_id)
    )
    form = MatchForm(instance=match)
    context = {
        "form": form,
        "match": match,
        "home_team": match.home_team.name,
        "away_team": match.away_team.name,
        "division": match.division.name,
    }
    return render(request, "match/edit.html", context)


def update(request):
    match = Match.objects.get(pk=int(request.POST["match_id"]))
    match = MatchForm(request.POST, instance=match)
    match.save()

    return redirect(f"/division/{request.POST['division_id']}")


def team(request, team_id):
    team = get_object_or_404(
        Team.objects.with_table_records().prefetch_related(
            "home_matches", "away_matches"
        ),
        pk=int(team_id),
    )
    matches = team.home_matches.all() | team.away_matches.all()
    sorted_matches = (
        matches.distinct()
        .select_related("home_team", "away_team")
        .order_by("scheduled_time")
    )
    context = {
        "team": team,
        "matches": sorted_matches,
        "wins": team.wins,
        "losses": team.losses,
        "draws": team.draws,
    }
    return render(request, "team/team.html", context)


def playoffs(request, division_id):
    division = get_object_or_404(Division, pk=int(division_id))

    teams = division.teams.with_playoffs()
    max_points_teams = teams.order_by("-max_possible_points")
    playoff_threshold = max_points_teams[6].max_possible_points
    sixth_place_points = teams[5].total_points

    context = {
        "division": division,
        "teams": teams,
        "promotion_threshold": playoff_threshold,
        "relegation_threshold": sixth_place_points,
        "number_of_successful_teams": 6,
    }
    return render(request, "division/division.html", context)
