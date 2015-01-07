from django import forms
from pagedown.widgets import AdminPagedownWidget
from .models import Biography, Essay
from bdrxml import mods


class BiographyModelForm(forms.ModelForm):
    bio = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Biography


class EssayModelForm(forms.ModelForm):
    text = forms.CharField(widget=AdminPagedownWidget())

    class Meta:
        model = Essay


class AnnotationForm(forms.Form):
    title_orig = forms.CharField()
    title_orig_lang = forms.CharField(required=False)
    title_english = forms.CharField(required=False)
    abstract = forms.CharField(required=False)
    people = forms.ModelMultipleChoiceField(queryset=Biography.objects, required=False)

    def to_mods_xml(self):
        mods_obj = mods.make_mods()
        mods_obj.title = self.cleaned_data['title_orig']
        return mods_obj.serialize().decode('utf8')

