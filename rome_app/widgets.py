import copy
from django import forms
from django.templatetags.static import static
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _


class AddAnotherWidgetWrapper(forms.Widget):
    """ 
    This class is a wrapper to a given widget to add the add icon for the
    admin interface. Modeled after
    django.contrib.admin.widgets.RelatedFieldWidgetWrapper
    """
    def __init__(self, widget, model, related_url_name):
        self.needs_multipart_form = widget.needs_multipart_form
        self.attrs = widget.attrs
        self.choices = widget.choices
        self.widget = widget
        self.model = model
        self.related_url_name = related_url_name
 
    def __deepcopy__(self, memo):
        obj = copy.copy(self)
        obj.widget = copy.deepcopy(self.widget, memo)
        obj.attrs = self.widget.attrs
        memo[id(self)] = obj 
        return obj 
 
    @property
    def media(self):
        return self.widget.media

    def render(self, name, value, *args, **kwargs):
        model = self.model
        info = (model._meta.app_label, model._meta.object_name.lower())
        self.widget.choices = self.choices
        output = [self.widget.render(name, value, *args, **kwargs)]
        related_url = reverse(self.related_url_name)
        output.append(('<a href="%s" class="add-another" id="add_id_%s" ' + 'onclick="return showAddAnotherPopup(this);">') % (related_url, name))
        output.append('<img src="%s" width="15" height="15" alt="%s"/></a>' % (static('admin/img/icon_addlink.gif'), _('Add Another')))
        return mark_safe(''.join(output))
 
    def build_attrs(self, extra_attrs=None, **kwargs):
        "Helper function for building an attribute dictionary."
        self.attrs = self.widget.build_attrs(extra_attrs=None, **kwargs)
        return self.attrs

    def value_from_datadict(self, data, files, name):
        return self.widget.value_from_datadict(data, files, name)

    def _has_changed(self, initial, data):
        return self.widget._has_changed(initial, data)

    def id_for_label(self, id_):
        return self.widget.id_for_label(id_)

