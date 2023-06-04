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

    def wins_in_2023(self):
        home_wins = self.home_matches.filter(
            home_score__gt=models.F("away_score")
        ).distinct()
        away_wins = self.away_matches.filter(
            away_score__gt=models.F("home_score")
        ).distinct()
        wins = home_wins | away_wins
        return wins.count()

    def losses_in_2023(self):
        home_losses = self.home_matches.filter(
            home_score__lt=models.F("away_score")
        ).distinct()
        away_losses = self.away_matches.filter(
            away_score__lt=models.F("home_score")
        ).distinct()
        losses = home_losses | away_losses
        return losses.count()

    def draws_in_2023(self):
        home_draws = self.home_matches.filter(
            home_score__exact=models.F("away_score")
        ).distinct()
        away_draws = self.away_matches.filter(
            away_score__exact=models.F("home_score")
        ).distinct()
        draws = home_draws | away_draws
        return draws.count()


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
    scheduled_time = models.DateTimeField()

    def __str__(self):
        return f"{self.home_team} {self.home_score}-{self.away_score} {self.away_team}"
