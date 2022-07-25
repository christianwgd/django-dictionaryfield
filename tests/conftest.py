import pytest
from collections import OrderedDict

from django.conf import settings
from django.forms import fields
from django.core.validators import RegexValidator

from dictionaryfield.fields import DictionaryFormField, DictionaryField


def pytest_configure():
    # For Django 1.8+
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
        }
    ]

    settings.configure(INSTALLED_APPS=(
        'django.contrib.contenttypes',
        'django.contrib.auth',
        'dictionaryfield',
        'bootstrap3',
    ), TEMPLATES = TEMPLATES)


@pytest.fixture
def sample_field():
    return DictionaryField(
        "What is the first volume and issue in which the journal published full-text English?",
        kwargs = {
                'fields': OrderedDict([
                ('volume', fields.CharField(label='Volume', required=True)),
                ('issue', fields.CharField(label='Issue', required=False, validators=[RegexValidator(r'\d+')]))
            ])
        }
    )


@pytest.fixture
def sample_nested_field():
    return DictionaryField(
        "Nested dictionary fields",
        kwargs={
            'fields': OrderedDict([
                ('sub1', DictionaryFormField(label="Sub 1", fields=OrderedDict([
                    ('volume', fields.CharField(label='Volume', required=True)),
                    ('issue', fields.CharField(label='Issue', required=True))
                ]))),
                ('sub2', DictionaryFormField(label="Sub 2", fields=OrderedDict([
                    ('author', fields.CharField(label='Author', required=True)),
                    ('book', fields.CharField(label='Book', required=True)),
                ]))),
            ])
        }
    )
