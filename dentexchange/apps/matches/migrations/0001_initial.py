# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Match'
        db.create_table(u'matches_match', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('match_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='match_match_set', to=orm['contenttypes.ContentType'])),
            ('match_object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('source_content_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='match_source_set', null=True, to=orm['contenttypes.ContentType'])),
            ('source_object_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'matches', ['Match'])

        # Adding unique constraint on 'Match', fields ['match_content_type', 'match_object_id', 'source_content_type', 'source_object_id', 'user']
        db.create_unique(u'matches_match', ['match_content_type_id', 'match_object_id', 'source_content_type_id', 'source_object_id', 'user_id'])

        # Adding model 'Automatch'
        db.create_table(u'matches_automatch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('match_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='automatch_match_set', to=orm['contenttypes.ContentType'])),
            ('match_object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('source_content_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='automatch_source_set', to=orm['contenttypes.ContentType'])),
            ('source_object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('saved_match', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['matches.Match'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'matches', ['Automatch'])

        # Adding unique constraint on 'Automatch', fields ['match_content_type', 'match_object_id', 'source_content_type', 'source_object_id', 'user']
        db.create_unique(u'matches_automatch', ['match_content_type_id', 'match_object_id', 'source_content_type_id', 'source_object_id', 'user_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Automatch', fields ['match_content_type', 'match_object_id', 'source_content_type', 'source_object_id', 'user']
        db.delete_unique(u'matches_automatch', ['match_content_type_id', 'match_object_id', 'source_content_type_id', 'source_object_id', 'user_id'])

        # Removing unique constraint on 'Match', fields ['match_content_type', 'match_object_id', 'source_content_type', 'source_object_id', 'user']
        db.delete_unique(u'matches_match', ['match_content_type_id', 'match_object_id', 'source_content_type_id', 'source_object_id', 'user_id'])

        # Deleting model 'Match'
        db.delete_table(u'matches_match')

        # Deleting model 'Automatch'
        db.delete_table(u'matches_automatch')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'matches.automatch': {
            'Meta': {'unique_together': "(('match_content_type', 'match_object_id', 'source_content_type', 'source_object_id', 'user'),)", 'object_name': 'Automatch'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'automatch_match_set'", 'to': u"orm['contenttypes.ContentType']"}),
            'match_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'saved_match': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['matches.Match']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'source_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'automatch_source_set'", 'to': u"orm['contenttypes.ContentType']"}),
            'source_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'matches.match': {
            'Meta': {'unique_together': "(('match_content_type', 'match_object_id', 'source_content_type', 'source_object_id', 'user'),)", 'object_name': 'Match'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match_content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'match_match_set'", 'to': u"orm['contenttypes.ContentType']"}),
            'match_object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'source_content_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'match_source_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'source_object_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['matches']