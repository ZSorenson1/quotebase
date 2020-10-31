from django import forms

class QuoteForm(forms.Form):
    quotedBy = forms.CharField(label="Quoted By", max_length=50)
    message = forms.CharField(max_length=100)