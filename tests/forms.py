from collections import OrderedDict

from django.core.validators import RegexValidator
from django.forms import forms, fields, widgets

from dictionaryfield.fields import DictionaryFormField


class BasicForm(forms.Form):
    myfield = DictionaryFormField(OrderedDict([
        ('volume', fields.CharField(label='Volume', required=True)),
        ('issue', fields.CharField(label='Issue', required=False, validators=[RegexValidator(r'\d+')])),
        ('comment', fields.CharField(label="Comment", required=True, widget=widgets.Textarea))
    ]))
