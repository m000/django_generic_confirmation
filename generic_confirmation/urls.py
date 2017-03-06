from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.confirm, {'token': None},  name="generic_confirmation_by_form"),
    url(r'^(?P<token>\w+)/$', views.confirm, {}, name="generic_confirmation_by_get"),
]
