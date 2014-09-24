# -*- coding:utf-8 -*-
from .base import Mixin
from .. import strings


class MeaningfulEmptyValueFormMixin(Mixin):
    def __init__(self, *args, **kwargs):
        self.base_impl(
            MeaningfulEmptyValueFormMixin, self).__init__(*args, **kwargs)
        self.initialize_empty_values()

    def initialize_empty_values(self):
        for key in self.fields.keys():
            field = self.fields[key]
            if key in getattr(self, 'non_meaningful_fields', ()):
                continue
            if hasattr(field, 'choices') and len(field.choices) > 0:
                if field.choices[0][0] in ('', None):
                    empty_value = field.choices.pop(0)[0]
                else:
                    empty_value = ''
                field.choices.insert(0, (
                    empty_value,
                    strings.MEANINGFUL_EMPTY_VALUE_FORM_LABEL % unicode(
                    field.label)))
                field.widget.choices = list(field.choices)


class UserInitializationFormMixin(Mixin):
    def __init__(self, user=None, *args, **kwargs):
        self.base_impl(
            UserInitializationFormMixin, self).__init__(*args, **kwargs)
        self.user = user

    def save(self, commit=True):
        instance = self.base_impl(
            UserInitializationFormMixin, self).save(commit=False)
        instance.user = self.user
        if commit:
            instance.save()
        return instance
