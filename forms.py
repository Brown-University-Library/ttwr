from django import forms
from pagedown.widgets import AdminPagedownWidget
from .models import Biography


class BiographyModelForm(forms.ModelForm):
    bio = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Biography

