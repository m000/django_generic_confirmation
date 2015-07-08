# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DeferredAction'
        db.create_table('generic_confirmation_deferredaction', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('valid_until', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('confirmed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('form_class', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('form_input', self.gf('picklefield.fields.PickledObjectField')()),
            ('form_prefix', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'], null=True)),
            ('object_pk', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('generic_confirmation', ['DeferredAction'])


    def backwards(self, orm):
        
        # Deleting model 'DeferredAction'
        db.delete_table('generic_confirmation_deferredaction')


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
