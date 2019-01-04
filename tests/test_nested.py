def test_render(sample_nested_field):
    formfield = sample_nested_field.formfield()
    rendered_field = formfield.widget.render('nested_data', None)
    assert 'Sub 1' in rendered_field
    assert 'Sub 2' in rendered_field
    assert 'Volume:' in rendered_field
    assert 'Issue:' in rendered_field
    assert 'Author:' in rendered_field
    assert 'Book:' in rendered_field
    assert 'name="nested_data__sub1__volume" type="text"' in rendered_field
    assert 'name="nested_data__sub1__issue" type="text"' in rendered_field
    assert 'name="nested_data__sub2__author" type="text"' in rendered_field
    assert 'name="nested_data__sub2__book" type="text"' in rendered_field


def test_value_from_data(sample_nested_field):
    formfield = sample_nested_field.formfield()
    parsed_data = formfield.widget.value_from_datadict({
        "nested_data__sub1__volume": "val_volume",
        "nested_data__sub1__issue": "val_issue"
    }, None, "nested_data")
    assert parsed_data['sub1']['volume'] == 'val_volume'
    assert parsed_data['sub1']['issue'] == 'val_issue'
