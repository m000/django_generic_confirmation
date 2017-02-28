from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.confirm_by_form, {}, name="generic_confirmation_by_form"),
    url(r'^(?P<token>\w+)/$', views.confirm_by_get, {}, name="generic_confirmation_by_get"),
]
