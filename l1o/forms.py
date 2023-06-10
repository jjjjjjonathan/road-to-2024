from django.forms import ModelForm, ChoiceField
from .models import Match, Division


class MatchForm(ModelForm):
    class Meta:
        model = Match
        fields = [
            "id",
            "home_score",
            "away_score",
            "e2e_id",
            "is_completed",
        ]
