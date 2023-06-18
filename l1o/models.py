from django.db import models
from django.db.models import Q, F, Count


class Division(models.Model):
    class NumberOfPromotedTeams(models.IntegerChoices):
        TEN = 10
        TWELVE = 12

    name = models.CharField(max_length=80)
    number_of_promoted_teams = models.IntegerField(
        choices=NumberOfPromotedTeams.choices
    )

    def __str__(self):
        return self.name


class TeamManager(models.Manager):
    def with_table_records(self):
        return (
            self.annotate(
                matches_remaining=(
                    Count("home_matches", distinct=True)
                    + Count("away_matches", distinct=True)
                    - (
                        Count(
                            "home_matches",
                            distinct=True,
                            filter=Q(home_matches__is_completed__exact=True),
                        )
                        + Count(
                            "away_matches",
                            distinct=True,
                            filter=Q(away_matches__is_completed__exact=True),
                        )
                    )
                ),
                wins=(
                    Count(
                        "home_matches",
                        filter=Q(
                            home_matches__home_score__gt=F("home_matches__away_score")
                        )
                        & Q(home_matches__is_completed__exact=True),
                        distinct=True,
                    )
                    + Count(
                        "away_matches",
                        filter=Q(
                            away_matches__away_score__gt=F("away_matches__home_score")
                        )
                        & Q(away_matches__is_completed=True),
                        distinct=True,
                    )
                ),
                losses=(
                    Count(
                        "home_matches",
                        filter=Q(
                            home_matches__home_score__lt=F("home_matches__away_score")
                        )
                        & Q(home_matches__is_completed__exact=True),
                        distinct=True,
                    )
                    + Count(
                        "away_matches",
                        filter=Q(
                            away_matches__away_score__lt=F("away_matches__home_score")
                        )
                        & Q(away_matches__is_completed__exact=True),
                        distinct=True,
                    )
                ),
                draws=(
                    Count(
                        "home_matches",
                        filter=Q(
                            home_matches__home_score__exact=F(
                                "home_matches__away_score"
                            )
                        )
                        & Q(home_matches__is_completed__exact=True),
                        distinct=True,
                    )
                    + Count(
                        "away_matches",
                        filter=Q(
                            away_matches__away_score__exact=F(
                                "away_matches__home_score"
                            )
                        )
                        & Q(away_matches__is_completed__exact=True),
                        distinct=True,
                    )
                ),
            )
            .annotate(points_in_2023=(F("wins") * 3) + F("draws"))
            .annotate(total_points=(F("points_in_2022") * 0.75) + F("points_in_2023"))
            .annotate(
                max_possible_points=F("matches_remaining") * 3 + F("total_points")
            )
            .order_by("-total_points")
        )


class Team(models.Model):
    name = models.CharField(max_length=80)
    points_in_2022 = models.IntegerField()
    division = models.ForeignKey(
        Division, on_delete=models.CASCADE, related_name="teams"
    )
    objects = TeamManager()

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
        Division, on_delete=models.CASCADE, related_name="matches"
    )
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    e2e_id = models.IntegerField(unique=True)
    scheduled_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"#{self.e2e_id}: {self.home_team} {self.home_score}-{self.away_score} {self.away_team}"
