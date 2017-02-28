from django.contrib import admin
from .models import DeferredAction

class DeferredActionAdmin(admin.ModelAdmin):
	list_display = ('token', 'valid_until', 'confirmed', 'is_expired')
	readonly_fields=('form_input',)
admin.site.register(DeferredAction, DeferredActionAdmin)

