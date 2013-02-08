# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Box.cost'
        db.alter_column('ramens_box', 'cost', self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True))

        # Changing field 'Ramen.cogs'
        db.alter_column('ramens_ramen', 'cogs', self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True))

        # Changing field 'Ramen.msrp'
        db.alter_column('ramens_ramen', 'msrp', self.gf('django.db.models.fields.IntegerField')(max_length=7, null=True))

    def backwards(self, orm):

        # Changing field 'Box.cost'
        db.alter_column('ramens_box', 'cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2))

        # Changing field 'Ramen.cogs'
        db.alter_column('ramens_ramen', 'cogs', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2))

        # Changing field 'Ramen.msrp'
        db.alter_column('ramens_ramen', 'msrp', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2))

    models = {
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