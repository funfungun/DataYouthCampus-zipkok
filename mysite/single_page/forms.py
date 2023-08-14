from django import forms

class AvgCostForm(forms.Form):
    #min_avg_cost = forms.FloatField(label='최소', required=False)
    max_avg_cost = forms.FloatField(label='최대', required=True)
    