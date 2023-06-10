from django.db import models
from django.db.models import Q, F, Count


class Division(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class TeamManager(models.Manager):
    def with_table_records(self):
        return (
            self.annotate(
                matches_played=(
                    Count(
                        "home_matches",
                        distinct=True,
                        filter=Q(home_matches__is_completed__exact=True),
                    )
                    + Count(
                        "away_matches",
                        distinct=True,
                        filter=Q(away_matches__is_completed__exact=True),
                        # filter=Q(away_matches__scheduled_time__lte=date),
                    )
                ),
                wins=(
                    Count(
                        "home_matches",
                        filter=Q(
                            home_matches__home_score__gt=F("home_matches__away_score")
                        )
                        & Q(home_matches__is_completed__exact=True),
                        # & Q(home_matches__scheduled_time__lte=date),
                        distinct=True,
                    )
                    + Count(
                        "away_matches",
                        filter=Q(
                            away_matches__away_score__gt=F("away_matches__home_score")
                        )
                        & Q(away_matches__is_completed=True),
                        # & Q(away_matches__scheduled_time__lte=date),
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
                        # & Q(home_matches__scheduled_time__lte=date),
                        distinct=True,
                    )
                    + Count(
                        "away_matches",
                        filter=Q(
                            away_matches__away_score__lt=F("away_matches__home_score")
                        )
                        & Q(away_matches__is_completed__exact=True),
                        # & Q(away_matches__scheduled_time__lte=date),
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
                        # & Q(home_matches__scheduled_time__lte=date),
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
                        # & Q(away_matches__scheduled_time__lte=date),
                        distinct=True,
                    )
                ),
            )
            .annotate(points_in_2023=(F("wins") * 3) + F("draws"))
            .annotate(total_points=(F("points_in_2022") * 0.75) + F("points_in_2023"))
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

    def wins_in_2023(self):
        home_wins = self.home_matches.filter(
            home_score__gt=models.F("away_score"), is_completed=True
        ).distinct()
        away_wins = self.away_matches.filter(
            away_score__gt=models.F("home_score"), is_completed=True
        ).distinct()
        wins = home_wins | away_wins
        return wins.count()

    def losses_in_2023(self):
        home_losses = self.home_matches.filter(
            home_score__lt=models.F("away_score"), is_completed=True
        ).distinct()
        away_losses = self.away_matches.filter(
            away_score__lt=models.F("home_score"), is_completed=True
        ).distinct()
        losses = home_losses | away_losses
        return losses.count()

    def draws_in_2023(self):
        home_draws = self.home_matches.filter(
            home_score__exact=models.F("away_score"), is_completed=True
        ).distinct()
        away_draws = self.away_matches.filter(
            away_score__exact=models.F("home_score"), is_completed=True
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
        Division, on_delete=models.CASCADE, related_name="matches"
    )
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    e2e_id = models.IntegerField(unique=True)
    scheduled_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"#{self.e2e_id}: {self.home_team} {self.home_score}-{self.away_score} {self.away_team}"
