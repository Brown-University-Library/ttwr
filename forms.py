from django import forms
from pagedown.widgets import AdminPagedownWidget
from .models import Biography, Essay


class BiographyModelForm(forms.ModelForm):
    bio = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Biography


class EssayModelForm(forms.ModelForm):
    text = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Essay


class PersonForm(forms.Form):
    name = forms.CharField()
    role = forms.CharField()
    trp_id = forms.CharField()


class AnnotationForm(forms.Form):
    title_orig = forms.CharField()
    title_orig_lang = forms.CharField(required=False)
    title_english = forms.CharField(required=False)
    abstract = forms.CharField(required=False)

