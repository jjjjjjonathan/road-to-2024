from django.db import models


class Divisions(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Teams(models.Model):
    name = models.CharField(max_length=80)
    points_in_2022 = models.IntegerField()
    division = models.ForeignKey(
        Divisions, on_delete=models.CASCADE, related_name="division"
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


class Matches(models.Model):
    home_team = models.ForeignKey(
        Teams, on_delete=models.CASCADE, related_name="home_matches"
    )
    away_team = models.ForeignKey(
        Teams, on_delete=models.CASCADE, related_name="away_matches"
    )
    division = models.ForeignKey(
        Divisions, on_delete=models.CASCADE, related_name="division"
    )
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    e2e_id = models.IntegerField()

    def __str__(self):
        return f"{self.home_team} vs. {self.away_team}"
