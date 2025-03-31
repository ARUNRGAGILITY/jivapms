from django import forms

class NewAppForm(forms.Form):
    app_name = forms.CharField(label='App Name', max_length=100)