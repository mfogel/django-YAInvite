"""
South migration to properly set up the Foreign Key from an Invite to the
object of your choosing.

This migration changes depending on what your
settings.INVITATION_INVITOR_CLASS is set for. If you choose to change this
setting, you'll need to migrate your database again somehow.

You may also want to put a:
    needed_by = (('invitation', '0001_initial'),)
in the migration where the INVITATION_INVITOR_CLASS is actually created.
See http://south.aeracode.org/wiki/Dependencies#ReverseDependencies
for details.
"""

# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.conf import settings
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Invite'
        db.create_table('invitation_invite', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('invited', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('expires', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2012, 6, 26, 0, 0), null=True, blank=True)),
            ('invitor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invite_sent_set', to=orm[settings.INVITATION_INVITOR_CLASS])),
            ('redeemer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='invite_redeemed_set', null=True, to=orm['auth.User'])),
        ))
        db.send_create_signal('invitation', ['Invite'])


    def backwards(self, orm):
        # Deleting model 'Invite'
        db.delete_table('invitation_invite')


    models = {
        # using a stub definition of the linked-to invitor model
        # NOTE: if this entry conflicts with another key in this dictionary,
        #       (ex: auth.user) last one wins (which is good because that
        #       one has a complete ORM definition, and this is just a stub)
        settings.INVITATION_INVITOR_CLASS.lower(): {
            'Meta': {'object_name': settings.INVITATION_INVITOR_CLASS.split('.')[-1], 'db_table': "'{}'".format(settings.INVITATION_INVITOR_DB_TABLE)},
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
        'invitation.invite': {
            'Meta': {'object_name': 'Invite'},
            'expires': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2012, 6, 26, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invited': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'invitor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invite_sent_set'", 'to': "orm['{}']".format(settings.INVITATION_INVITOR_CLASS)}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'redeemer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'invite_redeemed_set'", 'null': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['invitation']
