from django.db import models


class Division(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=80)
    points_in_2022 = models.IntegerField()
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, related_name="team_division"
    )

    def __str__(self):
        return self.name

    def wins(self):
        home_wins = self.home_matches.filter(
            home_score__gt=models.F("away_score")
        ).count()
        away_wins = self.away_matches.filter(
            away_score__gt=models.F("home_score")
        ).count()
        return home_wins + away_wins

    def losses(self):
        home_losses = self.home_matches.filter(
            home_score__lt=models.F("away_score")
        ).count()
        away_losses = self.away_matches.filter(
            away_score__gt=models.F("home_score")
        ).count()
        return home_losses + away_losses

    def draws(self):
        home_draws = self.home_matches.filter(
            home_score__exact=models.F("away_score")
        ).count()
        away_draws = self.away_matches.filter(
            away_score__exact=models.F("home_score")
        ).count()
        return home_draws + away_draws

    def points_in_2023(self):
        return (self.wins() * 3) + (self.draws())

    def total_points(self):
        return self.points_in_2023() + (self.points_in_2022 * 0.75)


class Match(models.Model):
    home_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="home_matches"
    )
    away_team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="away_matches"
    )
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, related_name="match_division"
    )
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    e2e_id = models.IntegerField()

    def __str__(self):
        return f"{self.home_team} vs. {self.away_team}"


# Team.objects.annotate(
#     wins=(
#         Count(
#             "home_matches",
#             filter=Q(home_matches__home_score__gt=F("home_matches__away_score")),
#         )
#     )
#     + Count(
#         "away_matches",
#         filter=Q(away_matches__away_score__gt=F("away_matches__home_score")),
#     ),
#     losses=(
#         Count(
#             "home_matches",
#             filter=Q(home_matches__home_score__lt=F("home_matches__away_score")),
#         )
#     )
#     + Count(
#         "away_matches",
#         filter=Q(away_matches__away_score__lt=F("away_matches__home_score")),
#     ),
#     draws=(
#         Count(
#             "home_matches",
#             filter=Q(home_matches__home_score__exact=F("home_matches__away_score")),
#         )
#     )
#     + Count(
#         "away_matches",
#         filter=Q(away_matches__away_score__exact=F("away_matches__home_score")),
#     ),
# ).annotate(points_in_2023=(F("wins") * 3) + F("draws")).annotate(
#     total_points=(F("points_in_2022") * 0.75) + F("points_in_2023")
# ).all()
