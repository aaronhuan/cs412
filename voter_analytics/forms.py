#File: voter_analysis/forms.py
#Author: Aaron Huang (ahuan@bu.edu), 10/31/2025
#Description: form class to display the filter form.

from django import forms
from .models import Voter
from django.db.models import Min, Max


class FilterForm(forms.Form):
    """ Filter form for filtering specific 'Voters' in."""
    party = forms.ChoiceField(required=False)
    min_year = forms.ChoiceField(required=False)
    max_year = forms.ChoiceField(required=False)
    voter_score = forms.ChoiceField(required=False)


    v20state   = forms.BooleanField(required=False)
    v21town    = forms.BooleanField(required=False)
    v21primary = forms.BooleanField(required=False)
    v22general = forms.BooleanField(required=False)
    v23town    = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        """Build the form choices based on current 'voter' data. """
        super().__init__(*args, **kwargs)
        all_parties = (
            Voter.objects.values_list("party_affiliation", flat=True)
            .exclude(party_affiliation__isnull=True)
            .distinct()
        )

        party_choices = [("", "choose")]

        for raw in all_parties:
            display = (raw or "").strip()
            party_choices.append((raw, display))

        if len(party_choices) == 1:
            party_choices = [("", "choose")]
        self.fields['party'].choices = party_choices


        min_max = Voter.objects.aggregate(
            min = Min("date_of_birth"),
            max = Max("date_of_birth"),
        )
        start_date = min_max["min"]
        end_date = min_max["max"]
        if start_date and end_date:
            all_years = [("", "choose")] + [
                (str(year), str(year)) for year in range(start_date.year, end_date.year + 1)
            ]
        else:
            all_years = [("", "choose")]

        self.fields['min_year'].choices = all_years
        self.fields['max_year'].choices = all_years

        scores = [('', 'choose')] + [(str(i), str(i)) for i in range(6)]
        self.fields['voter_score'].choices = scores



