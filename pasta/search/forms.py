from django import forms
from recipes.models import Recipe
from wiki.models import Ingredient, Instrument

class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput, max_length=100, required=False)