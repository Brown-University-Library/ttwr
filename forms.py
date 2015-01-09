from django import forms
from pagedown.widgets import AdminPagedownWidget
from .models import Biography, Essay, Genre


class BiographyModelForm(forms.ModelForm):
    bio = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Biography


class EssayModelForm(forms.ModelForm):
    text = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Essay


class PersonForm(forms.Form):
    person = forms.ModelChoiceField(queryset=Biography.objects)
    role = forms.CharField()


class InscriptionForm(forms.Form):
    location = forms.CharField()
    text = forms.CharField()


class AnnotationForm(forms.Form):
    original_title = forms.CharField()
    original_title_language = forms.CharField(required=False)
    english_title = forms.CharField(required=False)
    genre = forms.ModelChoiceField(required=False, queryset=Genre.objects)
    abstract = forms.CharField(required=False, widget=forms.Textarea)

