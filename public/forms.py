from django import forms
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import ContactUs, Suggestions


class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ('name','email','comments')


class SuggestionsForm(forms.ModelForm):
    class Meta:
        model = Suggestions
        fields = ('name','email','comments')


class DataPrivacyForm(forms.ModelForm):
    class Meta:
        model = Suggestions
        fields = ('name','email','comments')
