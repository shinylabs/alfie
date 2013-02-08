# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Order.stripe_fee'
        db.alter_column('orders_order', 'stripe_fee', self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True))

        # Changing field 'Order.product_cost'
        db.alter_column('orders_order', 'product_cost', self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True))

        # Changing field 'Order.prints_cost'
        db.alter_column('orders_order', 'prints_cost', self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True))

        # Changing field 'Order.packaging_cost'
        db.alter_column('orders_order', 'packaging_cost', self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True))

        # Changing field 'Order.shipping_cost'
        db.alter_column('orders_order', 'shipping_cost', self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True))

        # Changing field 'Order.prize_cost'
        db.alter_column('orders_order', 'prize_cost', self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True))

        # Changing field 'Menu.price'
        db.alter_column('orders_menu', 'price', self.gf('django.db.models.fields.IntegerField')(max_length=7))

    def backwards(self, orm):

        # Changing field 'Order.stripe_fee'
        db.alter_column('orders_order', 'stripe_fee', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2))

        # Changing field 'Order.product_cost'
        db.alter_column('orders_order', 'product_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2))

        # Changing field 'Order.prints_cost'
        db.alter_column('orders_order', 'prints_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2))

        # Changing field 'Order.packaging_cost'
        db.alter_column('orders_order', 'packaging_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2))

        # Changing field 'Order.shipping_cost'
        db.alter_column('orders_order', 'shipping_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2))

        # Changing field 'Order.prize_cost'
        db.alter_column('orders_order', 'prize_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2))

        # Changing field 'Menu.price'
        db.alter_column('orders_menu', 'price', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2))

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
            'price': ('django.db.models.fields.IntegerField', [], {'max_length': '7'}),
            'slots': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'orders.order': {
            'Meta': {'object_name': 'Order'},
            'box': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ramens.Box']", 'null': 'True', 'blank': 'True'}),
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['orders.Menu']", 'null': 'True', 'blank': 'True'}),
            'coupon': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'gotpaid': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_4_digits': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'last_payment_attempt': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'packaging_cost': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'payment_attempts': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'prints_cost': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'prize_cost': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'product_cost': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'shipped': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'shipping_cost': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'stripe_fee': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['auth.User']"}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        'ramens.box': {
            'Meta': {'object_name': 'Box'},
            'cost': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ramens': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'ramens'", 'symmetrical': 'False', 'to': "orm['ramens.Ramen']"}),
            'slots': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4'})
        },
        'ramens.brand': {
            'Meta': {'object_name': 'Brand'},
            'address': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'ramens.flavor': {
            'Meta': {'object_name': 'Flavor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'taste': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'ramens.ramen': {
            'Meta': {'object_name': 'Ramen'},
            'boxed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ramens.Brand']", 'null': 'True', 'blank': 'True'}),
            'cogs': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dimensions': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'directions': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'flavors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['ramens.Flavor']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'msrp': ('django.db.models.fields.IntegerField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nutrition': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'packaging': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'ratings': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '1', 'blank': 'True'}),
            'saved_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'upc': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['orders']