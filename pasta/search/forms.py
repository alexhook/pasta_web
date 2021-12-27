from django import forms

class SearchForm(forms.Form):
    text = forms.CharField(widget=forms.TextInput, max_length=100, required=False)