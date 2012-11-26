# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cutelist'
        db.create_table('profiles_cutelist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal('profiles', ['Cutelist'])

        # Adding model 'Profile'
        db.create_table('profiles_profile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mugshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('privacy', self.gf('django.db.models.fields.CharField')(default='closed', max_length=15)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('menu', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('ship_address_1', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('ship_address_2', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('ship_city', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('ship_state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2, null=True, blank=True)),
            ('ship_zip_code', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('spice', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('allergy', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('subscribed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cancelled', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('killed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_4_digits', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
        ))
        db.send_create_signal('profiles', ['Profile'])

        # Adding M2M table for field cuter on 'Profile'
        db.create_table('profiles_profile_cuter', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('profile', models.ForeignKey(orm['profiles.profile'], null=False)),
            ('cutelist', models.ForeignKey(orm['profiles.cutelist'], null=False))
        ))
        db.create_unique('profiles_profile_cuter', ['profile_id', 'cutelist_id'])


    def backwards(self, orm):
        # Deleting model 'Cutelist'
        db.delete_table('profiles_cutelist')

        # Deleting model 'Profile'
        db.delete_table('profiles_profile')

        # Removing M2M table for field cuter on 'Profile'
        db.delete_table('profiles_profile_cuter')


    models = {
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
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'profiles.cutelist': {
            'Meta': {'object_name': 'Cutelist'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        'profiles.profile': {
            'Meta': {'object_name': 'Profile'},
            'allergy': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'cancelled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cuter': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['profiles.Cutelist']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'killed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_4_digits': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'menu': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'mugshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.CharField', [], {'default': "'closed'", 'max_length': '15'}),
            'ship_address_1': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'ship_address_2': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'ship_city': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'ship_state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'ship_zip_code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'spice': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'subscribed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['profiles']