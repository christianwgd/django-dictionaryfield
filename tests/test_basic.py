import pytest

from django.core.exceptions import ValidationError

from dictionaryfield.fields import DictionaryFormField


def test_formfield(sample_nested_field):
    assert isinstance(sample_nested_field.formfield(), DictionaryFormField)


def test_widget(sample_nested_field):
    formfield = sample_nested_field.formfield()
    assert sample_nested_field.fields, formfield.widget.fields


def test_render(sample_field):
    formfield = sample_field.formfield()
    rendered_field = formfield.widget.render('english_data', None)
    assert 'Volume:' in rendered_field
    assert 'Issue:' in rendered_field
    assert 'name="english_data__volume" type="text"' in rendered_field
    assert 'name="english_data__issue" type="text"' in rendered_field


def test_clean(sample_field):
    formfield = sample_field.formfield()
    data = formfield.clean({'volume': '1', 'issue': '2'})
    assert data == {'volume': '1', 'issue': '2'}
    with pytest.raises(ValidationError):
        formfield.clean({'issue': '2'})
    with pytest.raises(ValidationError):
        formfield.clean({'volume': '1', 'issue': 'x'})


def test_has_changed(sample_field):
    formfield = sample_field.formfield()
    assert formfield.has_changed({'volume': '1', 'issue': '2'}, {'volume': '1', 'issue': '2'}) is False
    assert formfield.has_changed('{"volume": "1", "issue": "2"}', {'volume': '1', 'issue': '2'}) is False
    assert formfield.has_changed({"volume": "1", "issue": "1"}, {'volume': '2', 'issue': '1'})

