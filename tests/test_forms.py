from .forms import BasicForm

def test_rendering():
    form = BasicForm(initial={"myfield": {"issue": "2"}})
    html = form.as_p()
    assert '<label for="id_myfield__volume">' in html
    assert '<label for="id_myfield__issue">' in html
    assert '<label for="id_myfield__comment">' in html
    assert '<input id="id_myfield__volume" name="myfield__volume" type="text" />' in html
    assert '<input id="id_myfield__issue" name="myfield__issue" type="text" value="2" />' in html
    assert '<textarea cols="40" id="id_myfield__comment" name="myfield__comment" rows="10">' in html


def test_invalid_data():
    """
    Invalid issue value, value for comment is missing
    :return:
    """
    form = BasicForm({"myfield__issue": "abc", "myfield__volume": "1"})
    assert form.is_valid() is False
    html = form.as_p()
    assert '<input id="id_myfield__volume" name="myfield__volume" type="text" value="1" />' in html
    assert '<input id="id_myfield__issue" name="myfield__issue" type="text" value="abc" />' in html
    assert '<textarea cols="40" id="id_myfield__comment" name="myfield__comment" rows="10">' in html

    assert '<ul class="errorlist">' in html
    assert 'Enter a valid value' in html
    assert 'This field is required' in html


def test_valid_data():
    hello = "Hello\nworld"
    form = BasicForm({"myfield__issue": "1", "myfield__volume": "my_volume", "myfield__comment": hello})
    assert form.is_valid()
    html = form.as_p()
    assert '<input id="id_myfield__volume" name="myfield__volume" type="text" value="my_volume" />' in html
    assert '<input id="id_myfield__issue" name="myfield__issue" type="text" value="1" />' in html
    assert '<textarea cols="40" id="id_myfield__comment" name="myfield__comment" rows="10">' + "\r\n" + hello + '</textarea>' in html

    assert '<ul class="errorlist">' not in html

    assert form.cleaned_data == {
        "myfield": {
            "issue": "1",
            "volume": "my_volume",
            "comment": hello
        }
    }

