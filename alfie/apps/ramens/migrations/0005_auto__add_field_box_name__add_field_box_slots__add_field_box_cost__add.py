# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Box.name'
        db.add_column('ramens_box', 'name',
                      self.gf('django.db.models.fields.CharField')(default=datetime.datetime(2012, 12, 19, 0, 0), max_length=255),
                      keep_default=False)

        # Adding field 'Box.slots'
        db.add_column('ramens_box', 'slots',
                      self.gf('django.db.models.fields.IntegerField')(default=0, max_length=2),
                      keep_default=False)

        # Adding field 'Box.cost'
        db.add_column('ramens_box', 'cost',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=7, decimal_places=2),
                      keep_default=False)

        # Adding field 'Box.notes'
        db.add_column('ramens_box', 'notes',
                      self.gf('django.db.models.fields.TextField')(max_length=255, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Box.name'
        db.delete_column('ramens_box', 'name')

        # Deleting field 'Box.slots'
        db.delete_column('ramens_box', 'slots')

        # Deleting field 'Box.cost'
        db.delete_column('ramens_box', 'cost')

        # Deleting field 'Box.notes'
        db.delete_column('ramens_box', 'notes')


    models = {
        'ramens.box': {
            'Meta': {'object_name': 'Box'},
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ramens': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'shipping_box'", 'symmetrical': 'False', 'to': "orm['ramens.Ramen']"}),
            'slots': ('django.db.models.fields.IntegerField', [], {'max_length': '2'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4'})
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
            'brand': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ramens.Brand']", 'null': 'True', 'blank': 'True'}),
            'cogs': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dimensions': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'directions': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'flavors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['ramens.Flavor']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'ingredients': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'msrp': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nutrition': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'packaging': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'ratings': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '1', 'blank': 'True'}),
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