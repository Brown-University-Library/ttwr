from django import forms
from pagedown.widgets import AdminPagedownWidget
from .models import Biography, Essay, Genre, Role
from .widgets import AddAnotherWidgetWrapper


class AdminBiographyForm(forms.ModelForm):
    bio = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Biography
        exclude = ('trp_id',)


class NewBiographyForm(forms.ModelForm):

    class Meta:
        fields = ('name',)
        model = Biography


class EssayModelForm(forms.ModelForm):
    text = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Essay


class PersonForm(forms.Form):
    person = forms.ModelChoiceField(queryset=Biography.objects.all().order_by('name'),
            widget=AddAnotherWidgetWrapper(forms.Select(), Biography, 'new_biography'))
    role = forms.ModelChoiceField(queryset=Role.objects.all().order_by('text'),
            widget=AddAnotherWidgetWrapper(forms.Select(), Role, 'new_role'))


class InscriptionForm(forms.Form):
    location = forms.CharField()
    text = forms.CharField()


def get_language_choices():
    #selected language names and codes
    langs = [('', 'Select a Language'), ('it', 'Italian'), ('fr', 'French'), ('en', 'English'),
              ('la', 'Latin'), ('nl', 'Dutch'), ('de', 'German')]
    return langs


class AnnotationForm(forms.Form):
    title = forms.CharField()
    title_language = forms.ChoiceField(required=False, choices=get_language_choices())
    english_title = forms.CharField(required=False)
    genre = forms.ModelChoiceField(required=False, queryset=Genre.objects.all().order_by('text'),
            widget=AddAnotherWidgetWrapper(forms.Select(), Genre, 'new_genre'))
    abstract = forms.CharField(required=False, widget=forms.Textarea)
    impression_date = forms.CharField(required=False)


class NewGenreForm(forms.ModelForm):
    class Meta:
        model = Genre


class NewRoleForm(forms.ModelForm):
    class Meta:
        model = Role

