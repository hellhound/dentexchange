# -*- coding:utf-8 -*-
from django.db.models.loading import get_model
from django.core.exceptions import ImproperlyConfigured

from haystack import connections, connection_router
from haystack.utils import get_identifier

from djcelery_transactions import PostTransactionTask as Task


def split_identifier(identifier):
    '''
    Converts 'notes.note.23' into ('notes.note', 23).
    '''
    bits = identifier.split('.')
    if len(bits) < 2:
        return (None, None)
    pk = bits[-1]
    # In case Django ever handles full paths...
    object_path = '.'.join(bits[:-1])
    return (object_path, pk)


def get_model_class(object_path):
    '''
    Fetch the model's class in a standarized way.
    '''
    bits = object_path.split('.')
    app_name = '.'.join(bits[:-1])
    classname = bits[-1]
    model_class = get_model(app_name, classname)
    if model_class is None:
        raise ImproperlyConfigured('Could not load model \'%s\'.' %
           object_path)
    return model_class


def get_instance(model_class, pk):
    '''
    Fetch the instance in a standarized way.
    '''
    try:
        instance = model_class._default_manager.get(pk=int(pk))
    except (model_class.DoesNotExist, model_class.MultipleObjectsReturned):
        return None
    return instance


def get_instance_from_identifier(identifier):
    if isinstance(identifier, basestring):
        object_path, pk = split_identifier(identifier)
        model_class = get_model_class(object_path)
        return get_instance(model_class, pk)
    return identifier


def get_indexes(model_class):
    using_backends = connection_router.for_write(
        models=[model_class])
    for using in using_backends:
        index_holder = connections[using].get_unified_index()
        yield index_holder.get_index(model_class)


class AsyncIndexAdapter(object):
    @staticmethod
    def remove_object(obj):
        HaystackActionTask.delay(HaystackActionTask.REMOVE_ACTION,
            get_identifier(obj))

    @staticmethod
    def update_object(obj):
        HaystackActionTask.delay(HaystackActionTask.UPDATE_ACTION,
            get_identifier(obj))


class HaystackActionTask(Task):
    REMOVE_ACTION = 0
    UPDATE_ACTION = 1

    def run(self, action, identifier):
        instance = get_instance_from_identifier(identifier)
        for index in get_indexes(type(instance)):
            if action == self.REMOVE_ACTION:
                index.remove_object(instance)
            else:
                index.update_object(instance) 
