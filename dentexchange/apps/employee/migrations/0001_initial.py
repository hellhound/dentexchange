# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmployeeQuestionnaire'
        db.create_table(u'employee_employeequestionnaire', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('job_position', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('solo_practitioner', self.gf('django.db.models.fields.BooleanField')()),
            ('multi_practitioner', self.gf('django.db.models.fields.BooleanField')()),
            ('corporate', self.gf('django.db.models.fields.BooleanField')()),
            ('fee_for_service', self.gf('django.db.models.fields.BooleanField')()),
            ('insurance', self.gf('django.db.models.fields.BooleanField')()),
            ('capitation_medicaid', self.gf('django.db.models.fields.BooleanField')()),
            ('zip_code', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=0, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2, blank=True)),
            ('distance', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
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
            ('experience_years', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('dental_school', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('graduation_year', self.gf('django.db.models.fields.PositiveSmallIntegerField')(null=True, blank=True)),
            ('visa', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('specific_strengths', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('is_private', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'employee', ['EmployeeQuestionnaire'])

        # Adding model 'Resume'
        db.create_table(u'employee_resume', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('cv_file', self.gf('validatedfile.fields.ValidatedFileField')(content_types=(u'application/pdf', u'application/msword', u'application/vnd.openxmlformats-officedocument.wordprocessingml.document'), max_upload_size=1048576, null=True, max_length=100, blank=True)),
        ))
        db.send_create_signal(u'employee', ['Resume'])


    def backwards(self, orm):
        # Deleting model 'EmployeeQuestionnaire'
        db.delete_table(u'employee_employeequestionnaire')

        # Deleting model 'Resume'
        db.delete_table(u'employee_resume')


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
        u'employee.employeequestionnaire': {
            'Meta': {'object_name': 'EmployeeQuestionnaire'},
            'annualy_wage': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'capitation_medicaid': ('django.db.models.fields.BooleanField', [], {}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'collection': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'compensation_type': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'corporate': ('django.db.models.fields.BooleanField', [], {}),
            'dental_school': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'distance': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'experience_years': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'fee_for_service': ('django.db.models.fields.BooleanField', [], {}),
            'friday_daytime': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'friday_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'graduation_year': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'hourly_wage': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'insurance': ('django.db.models.fields.BooleanField', [], {}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_position': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'monday_daytime': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'monday_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'multi_practitioner': ('django.db.models.fields.BooleanField', [], {}),
            'production': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'saturday_daytime': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'saturday_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'schedule_type': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'solo_practitioner': ('django.db.models.fields.BooleanField', [], {}),
            'specific_strengths': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2', 'blank': 'True'}),
            'sunday_daytime': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sunday_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thursday_daytime': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'thursday_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tuesday_daytime': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tuesday_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'}),
            'visa': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'wednesday_daytime': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wednesday_evening': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'zip_code': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '0', 'blank': 'True'})
        },
        u'employee.resume': {
            'Meta': {'object_name': 'Resume'},
            'cv_file': ('validatedfile.fields.ValidatedFileField', [], {'content_types': "(u'application/pdf', u'application/msword', u'application/vnd.openxmlformats-officedocument.wordprocessingml.document')", 'max_upload_size': '1048576', 'null': 'True', 'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['employee']