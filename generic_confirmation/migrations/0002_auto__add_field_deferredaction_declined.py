# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'DeferredAction.declined'
        db.add_column('generic_confirmation_deferredaction', 'declined', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'DeferredAction.declined'
        db.delete_column('generic_confirmation_deferredaction', 'declined')


    models = {
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'generic_confirmation.deferredaction': {
            'Meta': {'object_name': 'DeferredAction'},
            'confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True'}),
            'declined': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'form_class': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'form_input': ('picklefield.fields.PickledObjectField', [], {}),
            'form_prefix': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_pk': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'valid_until': ('django.db.models.fields.DateTimeField', [], {'null': 'True'})
        }
    }

    complete_apps = ['generic_confirmation']
