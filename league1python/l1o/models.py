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
