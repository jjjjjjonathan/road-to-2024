from django import template

register = template.Library()


def clinched_promotion(team, teams):
    index = team.division.number_of_promoted_teams
    threshold = teams[index].max_possible_points
    return team.total_points > threshold


def clinched_relegation(team, teams):
    index = team.division.number_of_promoted_teams - 1
    threshold = teams[index].total_points
    return team.max_possible_points < threshold


register.filter("clinched_promotion", clinched_promotion)
register.filter("clinched_relegation", clinched_relegation)
