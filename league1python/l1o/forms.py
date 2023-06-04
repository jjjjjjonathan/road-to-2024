from django import forms
from django.forms.widgets import NumberInput


class MatchForm(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     print(kwargs)
    #     self.teams = kwargs["teams"]
    #     team_list = kwargs["teams"]

    match_date = forms.DateField(widget=NumberInput(attrs={"type": "datetime-local"}))
