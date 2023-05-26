from django.db import models


class Divisions(models.Model):
    name = models.CharField(max_length=80)


class Teams(models.Model):
    name = models.CharField(max_length=80)
    points_in_2022 = models.IntegerField()
    division = models.ForeignKey(Divisions, on_delete=models.CASCADE)


class Matches(models.Model):
    home_team = models.ForeignKey(
        Teams, on_delete=models.CASCADE, related_name="home_team"
    )
    away_team = models.ForeignKey(
        Teams, on_delete=models.CASCADE, related_name="away_team"
    )
    division = models.ForeignKey(Divisions, on_delete=models.CASCADE)
    home_score = models.IntegerField()
    away_score = models.IntegerField()
    e2e_id = models.IntegerField()
