from django import forms
import pycountry
from pagedown.widgets import AdminPagedownWidget
from .models import Biography, Essay, Genre
from .widgets import AddAnotherWidgetWrapper


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


def get_language_choices():
    #list of all the language names and codes
    #(try to use the 2-letter code, but fall back to 3-letter if needed)
    langs = [ ('', 'Select a Language'), ('it', 'Italian'), ('fr', 'French'), ('en', 'English') ]
    for language in pycountry.languages:
        try:
            code = language.alpha2
        except AttributeError:
            code = language.bibliographic
        if code not in ['en', 'fr', 'it']:
            langs.append( (code, language.name) )
    return langs


class AnnotationForm(forms.Form):
    original_title = forms.CharField()
    original_title_language = forms.ChoiceField(required=False, choices=get_language_choices())
    english_title = forms.CharField(required=False)
    genre = forms.ModelChoiceField(required=False, queryset=Genre.objects.all().order_by('text'),
            widget=AddAnotherWidgetWrapper(forms.Select(), Genre))
    abstract = forms.CharField(required=False, widget=forms.Textarea)


class NewGenreForm(forms.ModelForm):
    class Meta:
        model = Genre

