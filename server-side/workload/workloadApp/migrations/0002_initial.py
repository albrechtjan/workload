# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Lecture'
        db.create_table(u'workloadApp_lecture', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('semester', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('startDay', self.gf('django.db.models.fields.DateField')()),
            ('endDay', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'workloadApp', ['Lecture'])

        # Adding model 'Student'
        db.create_table(u'workloadApp_student', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('permanentId', self.gf('django.db.models.fields.IntegerField')()),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal(u'workloadApp', ['Student'])

        # Adding M2M table for field lectures on 'Student'
        m2m_table_name = db.shorten_name(u'workloadApp_student_lectures')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('student', models.ForeignKey(orm[u'workloadApp.student'], null=False)),
            ('lecture', models.ForeignKey(orm[u'workloadApp.lecture'], null=False))
        ))
        db.create_unique(m2m_table_name, ['student_id', 'lecture_id'])

        # Adding model 'WorkingHoursEntry'
        db.create_table(u'workloadApp_workinghoursentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hoursInLecture', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hoursForHomework', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('hoursStudying', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('lecture', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workloadApp.Lecture'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['workloadApp.Student'])),
            ('week', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'workloadApp', ['WorkingHoursEntry'])


    def backwards(self, orm):
        # Deleting model 'Lecture'
        db.delete_table(u'workloadApp_lecture')

        # Deleting model 'Student'
        db.delete_table(u'workloadApp_student')

        # Removing M2M table for field lectures on 'Student'
        db.delete_table(db.shorten_name(u'workloadApp_student_lectures'))

        # Deleting model 'WorkingHoursEntry'
        db.delete_table(u'workloadApp_workinghoursentry')


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
        u'workloadApp.lecture': {
            'Meta': {'object_name': 'Lecture'},
            'endDay': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'startDay': ('django.db.models.fields.DateField', [], {})
        },
        u'workloadApp.student': {
            'Meta': {'object_name': 'Student'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lectures': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['workloadApp.Lecture']", 'symmetrical': 'False', 'blank': 'True'}),
            'permanentId': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'workloadApp.workinghoursentry': {
            'Meta': {'object_name': 'WorkingHoursEntry'},
            'hoursForHomework': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hoursInLecture': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hoursStudying': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lecture': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workloadApp.Lecture']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['workloadApp.Student']"}),
            'week': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['workloadApp']