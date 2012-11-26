# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Menu'
        db.create_table('orders_menu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('size', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('notes', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('orders', ['Menu'])

        # Adding model 'Order'
        db.create_table('orders_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['orders.Menu'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('month', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('ordered', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('paid', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('shipped', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('stripe_token', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('payment_attempts', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('last_payment_attempt', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('orders', ['Order'])


    def backwards(self, orm):
        # Deleting model 'Menu'
        db.delete_table('orders_menu')

        # Deleting model 'Order'
        db.delete_table('orders_order')


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
        'orders.menu': {
            'Meta': {'object_name': 'Menu'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'orders.order': {
            'Meta': {'object_name': 'Order'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_payment_attempt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.Menu']"}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'ordered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'payment_attempts': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'shipped': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'stripe_token': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['orders']