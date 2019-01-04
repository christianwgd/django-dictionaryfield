"""
Make sure widget works well with django-bootstrap3
"""
from bs4 import BeautifulSoup

from django.template import Template, Context

from .forms import BasicForm


def render(form):
    template = Template("""
    {% load bootstrap3 %}

    {% bootstrap_field form.myfield.issue %}
    {% bootstrap_field form.myfield.comment %}
        """)
    context = Context({"form": form})
    return BeautifulSoup(template.render(context), "html.parser")


def test_rendering_initial():
    form = BasicForm(
        initial={"myfield": {"issue": "myissue", "comment": "mycomment"}},
    )
    html = render(form)
    issue = html.select("#id_myfield__issue")[0]
    assert issue.attrs["value"] == "myissue"
    commment = html.select("#id_myfield__comment")[0]
    assert commment.text.strip() == "mycomment"


def test_rendering_data():
    form = BasicForm(
        initial={"myfield": {"issue": "2"}},
        data={"myfield__issue": "invalid_value"}
    )
    html = render(form)

    groups = html.select(".form-group")
    assert len(groups) == 2

    assert "has-error" in groups[0].attrs['class']
    assert groups[0].select("div.help-block")[0].text == 'Enter a valid value.'
    assert groups[0].select("label.control-label")[0].text == "Issue"
    issue_input = groups[0].select("input#id_myfield__issue")[0]
    assert issue_input.attrs["type"] == "text"
    assert issue_input.attrs["name"] == "myfield__issue"
    assert issue_input.attrs["value"] == "invalid_value"
    assert issue_input.attrs["placeholder"] == "Issue"

    assert groups[1].select("div.help-block")[0].text == "This field is required."
    assert groups[1].select("label.control-label")[0].text == "Comment"
    comment_textarea = groups[1].select("textarea#id_myfield__comment")[0]
    assert comment_textarea.attrs["name"] == "myfield__comment"
    assert comment_textarea.attrs["placeholder"] == "Comment"
