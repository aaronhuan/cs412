#File: voter_analysis/views.py
#Author: Aaron Huang (ahuan@bu.edu), 10/26/2025
#Description: views classes to do logic and render a template.

from django.views.generic import ListView, DetailView
from django.utils.http import urlencode
from django.db.models import Count, Sum, Case, When, IntegerField
from django.db.models.functions import ExtractYear
import plotly
import plotly.graph_objs as go
from .forms import FilterForm
from .models import Voter

class VoterListView(ListView):
    """ListView of voters, limiting it to 100 through pagination with form for filtering logic."""
    model = Voter
    template_name= "voter_analytics/show_all_voters.html"
    context_object_name = "voters"
    paginate_by = 100

    def get_queryset(self):
        '''A queryset filtered by GET parameters.'''
        voters = super().get_queryset()
        q = self.request.GET

        # party (exact match)
        party = q.get("party")

        if party:
            voters = voters.filter(party_affiliation=party)

        # year bounds from DOB
        min_year = q.get("min_year")
        if min_year:
            try:
                voters = voters.filter(date_of_birth__year__gte=int(min_year))
            except ValueError:
                pass

        max_year = q.get("max_year")
        if max_year:
            try:
                voters = voters.filter(date_of_birth__year__lte=int(max_year))
            except ValueError:
                pass

        # voter_score
        voter_score = q.get("voter_score")
        if voter_score:
            try:
                voters = voters.filter(voter_score=int(voter_score))
            except ValueError:
                pass

        # election participation checkboxes
        # if your form only sends the key when checked, this is enough:
        if "v20state" in q:
            voters = voters.filter(v20state=True)
        if "v21town" in q:
            voters = voters.filter(v21town=True)
        if "v21primary" in q:
            voters = voters.filter(v21primary=True)
        if "v22general" in q:
            voters = voters.filter(v22general=True)
        if "v23town" in q:
            voters = voters.filter(v23town=True)

        return voters

        

    def get_context_data(self, **kwargs):
        """add the filtering form, the current filters, and preserving query using urlencode."""
        context = super().get_context_data(**kwargs)

        context["form"]= FilterForm(self.request.GET)
        # expose current filters so the template can preserve selections
        context["filters"] = {
            "party": self.request.GET.get("party", ""),
            "min_year": self.request.GET.get("min_year", ""),
            "max_year": self.request.GET.get("max_year", ""),
            "voter_score": self.request.GET.get("voter_score", ""),
            "v20state": self.request.GET.get("v20state", ""),
            "v21town": self.request.GET.get("v21town", ""),
            "v21primary": self.request.GET.get("v21primary", ""),
            "v22general": self.request.GET.get("v22general", ""),
            "v23town": self.request.GET.get("v23town", ""),
        }

        # querystring to preserve filters across pagination
        preserved = self.request.GET.copy()
        preserved.pop("page", None)

        context["filter_qs"] = urlencode(preserved, doseq=True)
        return context
    

class VoterDetailView(DetailView):
    """Detail page for a single 'voter'."""
    model = Voter
    template_name = "voter_analytics/show_voter.html"
    context_object_name = "voter"


class GraphView(ListView):
    """ListView of graphs from plotly, can be filtered."""
    model = Voter
    template_name = "voter_analytics/graphs.html"
    context_object_name = "voters"
    paginate_by = None

    def get_queryset(self):
        '''A queryset filtered by GET parameters.'''
        voters = super().get_queryset()
        q = self.request.GET

        # party (exact match)
        party = q.get("party")

        if party:
            voters = voters.filter(party_affiliation=party)

        # year bounds from DOB
        min_year = q.get("min_year")
        if min_year:
            try:
                voters = voters.filter(date_of_birth__year__gte=int(min_year))
            except ValueError:
                pass

        max_year = q.get("max_year")
        if max_year:
            try:
                voters = voters.filter(date_of_birth__year__lte=int(max_year))
            except ValueError:
                pass

        # voter_score
        voter_score = q.get("voter_score")
        if voter_score:
            try:
                voters = voters.filter(voter_score=int(voter_score))
            except ValueError:
                pass

        # election participation checkboxes
        # if your form only sends the key when checked, this is enough:
        if "v20state" in q:
            voters = voters.filter(v20state=True)
        if "v21town" in q:
            voters = voters.filter(v21town=True)
        if "v21primary" in q:
            voters = voters.filter(v21primary=True)
        if "v22general" in q:
            voters = voters.filter(v22general=True)
        if "v23town" in q:
            voters = voters.filter(v23town=True)

        return voters

    def get_context_data(self, **kwargs):
        '''Make Plotly charts from filtered queryset and add the html to context'''
        context = super().get_context_data(**kwargs)
        voters = context['voters'] 
        # Birth-year histogram
        birth_counts = (
            voters.exclude(date_of_birth__isnull=True)
              .annotate(year=ExtractYear("date_of_birth"))
              .values("year")
              .annotate(total=Count("id"))
              .order_by("year")
        )

        birth_years = [row["year"] for row in birth_counts]
        birth_totals = [row["total"] for row in birth_counts]
       
        fig = go.Bar(x=birth_years, y=birth_totals)
        bar_birth = plotly.offline.plot({"data":[fig],
                                         "layout_title_text": "Voter Distribution based on birth year"},
                                         auto_open=False,
                                         output_type="div")
        context["bar_birth"]= bar_birth


        #party piechart
        party_counts = (
            voters.values("party_affiliation")
                .annotate(total=Count("id"))
                .order_by("party_affiliation")
        )

        party_labels = []
        party_values = []
        for row in party_counts:
            party_labels.append(row["party_affiliation"])
            party_values.append(row["total"])

        fig_party = go.Pie(labels=party_labels, values=party_values)
        pie_party = plotly.offline.plot({"data": [fig_party],
                                          "layout_title_text": "Voter Distribution by Party"},
                                        auto_open=False, 
                                        output_type="div")
        
        context["pie_party"] = pie_party

        #election  histogram
        election_fields = ["v20state", "v21town", "v21primary", "v22general", "v23town"]
        election_labels = ["2020 State", "2021 Town", "2021 Primary", "2022 General", "2023 Town"]

        totals = voters.aggregate(**{
            f: Sum(Case(When(**{f: True}, then=1), default=0, output_field=IntegerField()))
            for f in election_fields
        })
        election_values = [(totals.get(f) or 0) for f in election_fields]

        fig_elections = go.Bar(x=election_labels, y=election_values)
        bar_elections = plotly.offline.plot({"data": [fig_elections], 
                                             "layout_title_text": "Participation by Election"},
                                             auto_open=False,
                                             output_type="div")
        context["bar_elections"] = bar_elections

        context["form"] = FilterForm(self.request.GET)

        return context
