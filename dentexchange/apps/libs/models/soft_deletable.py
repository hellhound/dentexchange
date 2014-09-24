# -*- coding:utf-8 -*-
import mock
import inspect

from django.db.models.query import QuerySet
from django.db.models.deletion import Collector
from django.db import models

from .. import strings


def soft_delete(self, *args, **kwargs):
    if len(self.data) > 0:
        # normal deletes
        for model, instances in self.data.iteritems():
            if issubclass(model, SoftDeletableModel):
                for instance in instances:
                    instance.is_active = False
                    instance.save()
            else:
                collector = Collector(using=None) # use the default db
                collector.collect(instances)
                collector.delete()
    else:
        # fast deletes
        for qs in self.fast_deletes:
            qs.update(is_active=False)


class QuerySetProxy(object):
    def __init__(self, query):
        self.wrapped_query = query

    def wrap(self, name):
        def inner(*args, **kwargs):
            result = reference(*args, **kwargs)
            if isinstance(result, QuerySet):
                return QuerySetProxy(result)
            return result

        attribute = getattr(type(self.wrapped_query), name, None)
        reference = getattr(self.wrapped_query, name)
        if not inspect.ismethod(attribute):
            return reference
        return inner

    def __getattr__(self, name):
        return self.wrap(name)

    def __deepcopy__(self, memo):
        return self.wrap('__deepcopy__')(memo)

    def __getstate__(self):
        return self.wrap('__getstate__')()

    def __repr__(self):
        return self.wrap('__repr__')()

    def __len__(self):
        return self.wrap('__len__')()

    def __iter__(self):
        return self.wrap('__iter__')()

    def __nonzero__(self):
        return self.wrap('__nonzero__')()

    def __getitem__(self, key):
        return self.wrap('__getitem__')(key)

    def __and__(self, other):
        return self.wrap('__and__')(other)

    def __or__(self, other):
        return self.wrap('__or__')(other)

    @mock.patch('django.db.models.deletion.Collector.delete', soft_delete)
    def delete(self):
        self.wrapped_query.delete()


class SoftDeletableModelManager(models.Manager):
    def get_queryset(self):
        query = super(SoftDeletableModelManager, self).get_queryset()
        if self.model.should_show_active_only():
            query = query.filter(is_active=True)
        return QuerySetProxy(query)


class SoftDeletableModel(models.Model):
    show_active_only = True
    is_active = models.BooleanField(
        verbose_name=strings.SOFT_DELETABLE_MODEL_IS_ACTIVE, default=True)

    class Meta(object):
        abstract = True

    @classmethod
    def show_inactive(cls):
        cls.show_active_only = False

    @classmethod
    def hide_inactive(cls):
        cls.show_active_only = True

    @classmethod
    def should_show_active_only(cls):
        return cls.show_active_only

    @mock.patch('django.db.models.deletion.Collector.delete', soft_delete)
    def delete(self, using=None):
        super(SoftDeletableModel, self).delete(using=using)
