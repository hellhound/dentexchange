# -*- coding:utf-8 -*-
from django import forms

from libs.mixins.forms import MeaningfulEmptyValueFormMixin
from employee import constants as employee_constants
from . import strings


class SearchForm(forms.Form):
    keywords = forms.CharField(label=strings.SEARCH_FORM_KEYWORDS,
        required=False)
    location = forms.CharField(label=strings.SEARCH_FORM_LOCATION,
        required=False)


class SearchFiltersForm(MeaningfulEmptyValueFormMixin, forms.Form):
    job_position = forms.ChoiceField(
        label=strings.SEARCH_FILTERS_FORM_JOB_POSITION,
        choices=employee_constants.JOB_POSITION_CHOICES,
        required=False)
    experience_years = forms.ChoiceField(
        label=strings.SEARCH_FILTERS_FORM_EXPERIENCE_YEARS,
        choices=employee_constants.EXPERIENCE_YEARS_CHOICES,
        required=False)
    distance = forms.ChoiceField(
        label=strings.SEARCH_FILTERS_FORM_DISTANCE,
        choices=employee_constants.DISTANCE_CHOICES,
        required=False)
    full_time = forms.BooleanField(
        label=strings.SEARCH_FILTERS_FORM_FULL_TIME,
        required=False)
    part_time = forms.BooleanField(
        label=strings.SEARCH_FILTERS_FORM_PART_TIME,
        required=False)
    visa = forms.BooleanField(
        label=strings.SEARCH_FILTERS_FORM_VISA,
        required=False)
