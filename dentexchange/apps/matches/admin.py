# -*- coding:utf-8 -*-
from django.contrib import admin

from .models import Match, Automatch


class MatchAdmin(admin.ModelAdmin):
    list_display = ('match_content_type', 'match_object_id',
        'source_content_type', 'source_object_id', 'get_email',
        'match', 'source',)
    list_filter = ('match_content_type', 'source_content_type',)
    search_fields = ('match_content_type', 'match_object_id',
        'source_content_type', 'source_object_id', 'user__email',)


class AutomatchAdmin(admin.ModelAdmin):
    list_display = ('match_content_type', 'match_object_id',
        'source_content_type', 'source_object_id', 'get_email',
        'match', 'source',)
    list_filter = ('match_content_type', 'source_content_type',)
    search_fields = ('match_content_type', 'match_object_id',
        'source_content_type', 'source_object_id', 'user__email',)


admin.site.register(Match, MatchAdmin)
admin.site.register(Automatch, AutomatchAdmin)
