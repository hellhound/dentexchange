# -*- coding:utf-8 -*-
from haystack import indexes

from celery_haystack.indexes import CelerySearchIndex

from location.models import ZipCode


class ZipCodeIndex(CelerySearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # Shitty workaround to the content__contains problem
    contains = indexes.EdgeNgramField(use_template=True,
        template_name='search/indexes/location/zipcode_text.txt')
    code = indexes.DecimalField(model_attr='code')
    city = indexes.CharField(model_attr='city')
    state = indexes.CharField(model_attr='state')
    latitude = indexes.DecimalField(model_attr='latitude')
    longitude = indexes.DecimalField(model_attr='longitude')
    location = indexes.LocationField()

    def get_model(self):
        return ZipCode

    def get_updated_field(self):
        return 'updated'

    def prepare_location(self, obj):
        return '%s,%s' % (obj.latitude, obj.longitude)
