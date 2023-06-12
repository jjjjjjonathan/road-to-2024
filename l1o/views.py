from django.views import generic
from django.shortcuts import render, get_object_or_404, redirect
from .models import Division, Match, Team
from .forms import MatchForm


class IndexView(generic.ListView):
    template_name = "division/index.html"
    context_object_name = "divisions"

    def get_queryset(self):
        return Division.objects.all()


def division(request, division_id):
    division = get_object_or_404(Division, pk=int(division_id))

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


def edit(request, e2e_id):
    match = Match.objects.get(e2e_id=e2e_id)
    form = MatchForm(instance=match)
    context = {"form": form, "match_id": match.id, "division_id": match.division.id}
    return render(request, "match/edit.html", context)


def update(request):
    match = Match.objects.get(pk=int(request.POST["match_id"]))
    match = MatchForm(request.POST, instance=match)
    match.save()

    return redirect(f"/division/{request.POST['division_id']}")


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
