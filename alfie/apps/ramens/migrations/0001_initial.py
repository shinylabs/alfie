# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Manufacturer'
        db.create_table('ramens_manufacturer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=255, null=True, blank=True)),
            ('origin', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('ramens', ['Manufacturer'])

        # Adding model 'Flavor'
        db.create_table('ramens_flavor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('taste', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('ramens', ['Flavor'])

        # Adding model 'Ramen'
        db.create_table('ramens_ramen', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('upc', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('mfg', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ramens.Manufacturer'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('price', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('directions', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('weight', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('dimensions', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('image_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('saved_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('nutrition', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('ingredients', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('ratings', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('ramens', ['Ramen'])

        # Adding M2M table for field flavors on 'Ramen'
        db.create_table('ramens_ramen_flavors', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('ramen', models.ForeignKey(orm['ramens.ramen'], null=False)),
            ('flavor', models.ForeignKey(orm['ramens.flavor'], null=False))
        ))
        db.create_unique('ramens_ramen_flavors', ['ramen_id', 'flavor_id'])

        # Adding model 'Box'
        db.create_table('ramens_box', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('month', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
        ))
        db.send_create_signal('ramens', ['Box'])

        # Adding M2M table for field ramens on 'Box'
        db.create_table('ramens_box_ramens', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('box', models.ForeignKey(orm['ramens.box'], null=False)),
            ('ramen', models.ForeignKey(orm['ramens.ramen'], null=False))
        ))
        db.create_unique('ramens_box_ramens', ['box_id', 'ramen_id'])

        # Adding model 'Review'
        db.create_table('ramens_review', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ramen', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['ramens.Ramen'])),
            ('text', self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('published', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('ramens', ['Review'])


    def backwards(self, orm):
        # Deleting model 'Manufacturer'
        db.delete_table('ramens_manufacturer')

        # Deleting model 'Flavor'
        db.delete_table('ramens_flavor')

        # Deleting model 'Ramen'
        db.delete_table('ramens_ramen')

        # Removing M2M table for field flavors on 'Ramen'
        db.delete_table('ramens_ramen_flavors')

        # Deleting model 'Box'
        db.delete_table('ramens_box')

        # Removing M2M table for field ramens on 'Box'
        db.delete_table('ramens_box_ramens')

        # Deleting model 'Review'
        db.delete_table('ramens_review')


    models = {
        'ramens.box': {
            'Meta': {'object_name': 'Box'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'ramens': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'shipping_box'", 'symmetrical': 'False', 'to': "orm['ramens.Ramen']"}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        'ramens.flavor': {
            'Meta': {'object_name': 'Flavor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'taste': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'ramens.manufacturer': {
            'Meta': {'object_name': 'Manufacturer'},
            'address': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'origin': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'ramens.ramen': {
            'Meta': {'object_name': 'Ramen'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dimensions': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'directions': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'flavors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['ramens.Flavor']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'mfg': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ramens.Manufacturer']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nutrition': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'ratings': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'saved_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'upc': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'weight': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'ramens.review': {
            'Meta': {'object_name': 'Review'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'ramen': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ramens.Ramen']"}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ramens']