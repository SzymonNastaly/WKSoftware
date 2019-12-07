from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .choices import runs, ages, age_classes, competitions


class RunForm(forms.Form):
    """For updates of a run during the meeting, i.e. the existence of a violation"""
    lauf = forms.ChoiceField(choices=runs, initial=1)
    geschlecht = forms.ChoiceField(choices=[("m", "m"), ("w", "w")])
    alter = forms.ChoiceField(choices=ages)
    laufnummer = forms.IntegerField(initial=1, min_value=1)
    wechsel_bereit = forms.BooleanField(required=False)
    verstoß_existent = forms.BooleanField(required=False)


class AddForm(forms.Form):
    """Takes all data necessary to create a run (before competition)"""
    wettkampf = forms.ChoiceField(choices=competitions)
    name = forms.CharField()
    geschlecht = forms.ChoiceField(choices=[("m", "m"), ("w", "w")])
    alter = forms.ChoiceField(choices=age_classes)
    anzahl = forms.IntegerField(initial=1, min_value=1)
    ist_staffel = forms.BooleanField(required=False)


class EditForm(forms.Form):
    """Takes all data necessary to edit a run (before competition)"""
    # Note: required=False because otherwise "This field is required" - errors for every field, even
    # before submit - TODO
    wettkampf = forms.ChoiceField(choices=competitions, required=False)
    name = forms.CharField(required=False)
    geschlecht = forms.ChoiceField(choices=[("m", "m"), ("w", "w")], required=False)
    alter = forms.ChoiceField(choices=(age_classes), required=False)
    #anzahl = forms.IntegerField(initial=1, min_value=1, required=False)
    ist_staffel = forms.BooleanField(required=False)


class CustomLoginForm(AuthenticationForm):
    """Used as the AuthenticationForm. Overwrites username to have a select-widget/field."""
    username = UsernameField(
        widget=forms.Select(choices=[("Helfer", "Helfer")
            , ("Schiedsrichter", "Schiedsrichter")]))
