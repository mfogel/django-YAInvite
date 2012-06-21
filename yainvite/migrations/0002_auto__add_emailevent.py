# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.conf import settings
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EmailEvent'
        db.create_table('yainvite_emailevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invite', self.gf('django.db.models.fields.related.ForeignKey')(related_name='emailevent_set', to=orm['yainvite.Invite'])),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('sent_to', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('sent_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('yainvite', ['EmailEvent'])


    def backwards(self, orm):
        # Deleting model 'EmailEvent'
        db.delete_table('yainvite_emailevent')


    models = {
        # using a stub definition of the linked-to inviter model
        # NOTE: if this entry conflicts with another key in this dictionary,
        #       (ex: auth.user) last one wins (which is good because that
        #       one has a complete ORM definition, and this is just a stub)
        settings.YAINVITE_INVITER_CLASS.lower(): {
            'Meta': {'object_name': settings.YAINVITE_INVITER_CLASS.split('.')[-1], 'db_table': "'{}'".format(settings.YAINVITE_INVITER_DB_TABLE)},
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'yainvite.emailevent': {
            'Meta': {'object_name': 'EmailEvent'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emailevent_set'", 'to': "orm['yainvite.Invite']"}),
            'sent_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'sent_to': ('django.db.models.fields.EmailField', [], {'max_length': '255'})
        },
        'yainvite.invite': {
            'Meta': {'object_name': 'Invite'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True'}),
            'expires_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 28, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inviter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invite_sent_set'", 'to': "orm['{}']".format(settings.YAINVITE_INVITER_CLASS)}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_index': 'True'}),
            'redeemer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'invite_redeemed_set'", 'null': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['yainvite']
