# -*- coding:utf-8 -*-
from django.db import models
from django.db.models import Q
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

from libs.haystack.utils import AsyncIndexAdapter
from . import strings


class Match(models.Model):
    user = models.ForeignKey(User, verbose_name=strings.MATCH_USER)
    match_content_type = models.ForeignKey(ContentType,
        related_name='match_match_set',
        verbose_name=strings.AUTOMATCH_MATCH_CONTENT_TYPE, limit_choices_to=(
        Q(model='employeequestionnaire') | Q(model='jobposting')))
    match_object_id = models.PositiveIntegerField(
        verbose_name=strings.AUTOMATCH_MATCH_OBJECT_ID)
    source_content_type = models.ForeignKey(ContentType,
        related_name='match_source_set',
        verbose_name=strings.AUTOMATCH_SOURCE_CONTENT_TYPE, limit_choices_to=(
        Q(model='employeequestionnaire') | Q(model='jobposting')),
        null=True, blank=True)
    source_object_id = models.PositiveIntegerField(
        verbose_name=strings.AUTOMATCH_SOURCE_OBJECT_ID,
        null=True, blank=True)
    match = generic.GenericForeignKey('match_content_type', 'match_object_id')
    source = generic.GenericForeignKey('source_content_type',
        'source_object_id')

    class Meta(object):
        verbose_name = strings.MATCH_VERBOSE_NAME
        verbose_name_plural = strings.MATCH_VERBOSE_NAME_PLURAL
        unique_together = (('match_content_type', 'match_object_id',
            'source_content_type', 'source_object_id', 'user',),)

    def __unicode__(self):
        return self.match.get_job_position_display()

    def get_email(self):
        return self.user.email


class Automatch(models.Model):
    user = models.ForeignKey(User, verbose_name=strings.AUTOMATCH_USER)
    match_content_type = models.ForeignKey(ContentType,
        related_name='automatch_match_set',
        verbose_name=strings.AUTOMATCH_MATCH_CONTENT_TYPE, limit_choices_to=(
        Q(model='employeequestionnaire') | Q(model='jobposting')))
    match_object_id = models.PositiveIntegerField(
        verbose_name=strings.AUTOMATCH_MATCH_OBJECT_ID)
    source_content_type = models.ForeignKey(ContentType,
        related_name='automatch_source_set',
        verbose_name=strings.AUTOMATCH_SOURCE_CONTENT_TYPE, limit_choices_to=(
        Q(model='employeequestionnaire') | Q(model='jobposting')))
    source_object_id = models.PositiveIntegerField(
        verbose_name=strings.AUTOMATCH_SOURCE_OBJECT_ID)
    match = generic.GenericForeignKey('match_content_type', 'match_object_id')
    source = generic.GenericForeignKey('source_content_type',
        'source_object_id')
    saved_match = models.OneToOneField(Match,
        verbose_name=strings.AUTOMATCH_SAVED_MATCH, blank=True, null=True)

    class Meta(object):
        verbose_name = strings.AUTOMATCH_VERBOSE_NAME
        verbose_name_plural = strings.AUTOMATCH_VERBOSE_NAME_PLURAL
        unique_together = (('match_content_type', 'match_object_id',
            'source_content_type', 'source_object_id', 'user',),)

    @property
    def is_saved(self):
        return self.saved_match is not None

    def __unicode__(self):
        return self.match.get_job_position_display()

    def get_email(self):
        return self.user.email


@receiver([post_save, post_delete], sender=Match, dispatch_uid='update_index')
def update_index_handler(sender, instance=None, **kwargs):
    AsyncIndexAdapter.update_object(instance.match)
