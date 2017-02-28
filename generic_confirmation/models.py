import datetime
from django.db import models
from django.db.models.query import Q
from django.contrib.contenttypes.models import ContentType
try:
    # Django >= 1.8
    from django.contrib.contenttypes.fields import GenericForeignKey
except ImportError:
    # Django <= 1.7
    from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.auth.models import User
from picklefield.fields import PickledObjectField


class ConfirmationManager(models.Manager):
    def confirm(self, token):
        try:
            action = self.exclude(confirmed=True).exclude(declined=True).get(token=token)
        except self.model.DoesNotExist:
            return False

        if not action.is_expired():
            obj = action.resume_form_save()
            action.confirmed = True
            action.save() # FIXME: should we delete() here?
            return obj

        return False

    def pending_for(self, instance):
        ct = ContentType.objects.get_for_model(instance)
        now = datetime.datetime.now()
        return self.exclude(confirmed=True).exclude(declined=True).filter(content_type=ct,
                object_pk=instance.pk).filter(
                Q(valid_until__gt=now) | Q(valid_until__isnull=True)).count()


class DeferredAction(models.Model):
    token = models.CharField(max_length=40)
    valid_until = models.DateTimeField(null=True)
    confirmed = models.BooleanField(default=False)
    declined = models.BooleanField(default=False)
    requested_by = models.ForeignKey(User, null=True, blank=True, related_name='requested_by')
    reviewed_by = models.ForeignKey(User, null=True, blank=True, related_name='reviewed_by')
    created_at = models.DateTimeField(auto_now_add=True)

    form_class = models.CharField(max_length=255)
    form_input = PickledObjectField(editable=False)
    form_prefix = models.CharField(max_length=255, blank=True, null=True)

    content_type = models.ForeignKey(ContentType, null=True)
    object_pk = models.TextField(null=True)
    instance_object = GenericForeignKey('content_type', 'object_pk')

    objects = ConfirmationManager()

    def get_resume_form(self):
        form_class_name = self.form_class
        dot_index = form_class_name.rindex('.')
        module = form_class_name[:dot_index]
        klass = form_class_name[dot_index+1:]
        form_module = __import__(module, {}, {}, [''])
        form_class = getattr(form_module, klass)

        if self.instance_object is None:
            form = form_class(self.form_input)
        else:
            form = form_class(
                self.form_input, instance=self.instance_object,
                prefix=self.form_prefix)
        return form

    def resume_form_save(self, commit=True):
        form = self.get_resume_form()

        if not form.is_valid():
            raise Exception(
                "the deferred form was not cleaned properly before saving")

        obj = form.save_original(commit=commit)
        if commit:
            obj.save()
        return obj

    def is_expired(self):
        if self.valid_until is None:
            return False
        now = datetime.datetime.now()
        return self.valid_until < now
    is_expired.boolean = True
