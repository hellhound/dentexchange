# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Business'
        db.create_table(u'employer_business', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('number_offices', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('is_mso', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('number_employees', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'employer', ['Business'])

        # Adding model 'Praxis'
        db.create_table(u'employer_praxis', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('business', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employer.Business'])),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('contact_first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('contact_last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('zip_code', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=0)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('solo_practitioner', self.gf('django.db.models.fields.BooleanField')()),
            ('multi_practitioner', self.gf('django.db.models.fields.BooleanField')()),
            ('corporate', self.gf('django.db.models.fields.BooleanField')()),
            ('fee_for_service', self.gf('django.db.models.fields.BooleanField')()),
            ('insurance', self.gf('django.db.models.fields.BooleanField')()),
            ('capitation_medicaid', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'employer', ['Praxis'])

        # Adding model 'JobPosting'
        db.create_table(u'employer_jobposting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('praxis', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['employer.Praxis'])),
            ('position_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('posting_title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('job_position', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('schedule_type', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('monday_daytime', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('monday_evening', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tuesday_daytime', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('tuesday_evening', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wednesday_daytime', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wednesday_evening', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('thursday_daytime', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('thursday_evening', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('friday_daytime', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('friday_evening', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('saturday_daytime', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('saturday_evening', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sunday_daytime', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('sunday_evening', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('compensation_type', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('hourly_wage', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('annualy_wage', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('production', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('collection', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('experience_years', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('benefit_1', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('benefit_2', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('benefit_3', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('benefit_4', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('benefit_5', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('benefit_6', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('benefit_other', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('benefit_other_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('visa', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('additional_comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_posted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'employer', ['JobPosting'])


    def backwards(self, orm):
        # Deleting model 'Business'
        db.delete_table(u'employer_business')

        # Deleting model 'Praxis'
        db.delete_table(u'employer_praxis')

        # Deleting model 'JobPosting'
        db.delete_table(u'employer_jobposting')


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
        u'employer.business': {
            'Meta': {'object_name': 'Business'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_mso': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'number_employees': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'number_offices': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'employer.jobposting': {
            'Meta': {'object_name': 'JobPosting'},
            'additional_comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'annualy_wage': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'benefit_1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'benefit_2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'benefit_3': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'benefit_4': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'benefit_5': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'benefit_6': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'benefit_other': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'benefit_other_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'collection': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'compensation_type': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'experience_years': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'friday_daytime': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'friday_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hourly_wage': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_posted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_position': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            'monday_daytime': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'monday_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'position_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'posting_title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'praxis': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['employer.Praxis']"}),
            'production': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'saturday_daytime': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'saturday_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'schedule_type': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sunday_daytime': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sunday_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thursday_daytime': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thursday_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tuesday_daytime': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tuesday_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'visa': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'wednesday_daytime': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wednesday_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'employer.praxis': {
            'Meta': {'object_name': 'Praxis'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'business': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['employer.Business']"}),
            'capitation_medicaid': ('django.db.models.fields.BooleanField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'contact_first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'contact_last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'corporate': ('django.db.models.fields.BooleanField', [], {}),
            'fee_for_service': ('django.db.models.fields.BooleanField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insurance': ('django.db.models.fields.BooleanField', [], {}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'multi_practitioner': ('django.db.models.fields.BooleanField', [], {}),
            'solo_practitioner': ('django.db.models.fields.BooleanField', [], {}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'zip_code': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '0'})
        }
    }

    complete_apps = ['employer']