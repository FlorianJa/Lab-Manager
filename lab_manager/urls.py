from django.conf.urls import url
from lab_manager import views

app_name = 'lab_manager'

urlpatterns = [
    url(r'^api/printers$', views.fablab_printers),
    url(r'^api/printers/(?P<pk>[0-9]+)$', views.fablab_printers_detail),
    url(r'^api/filament/(?P<slug>[\w-]+)$',
        views.filament_usage_default),
    url(r'^api/filament$', views.filament_usage),
    url(r'^api/operating/(?P<pk>[0-9]+)$', views.operating_usage_default),
    url(r'^api/maintenance/(?P<pk>[0-9]+)$', views.maintenance),
    url(r'^api/printer/(?P<pk>[0-9]+)$', views.printer_usage_default),
    url(r'^api/usage$', views.usage),
    url(r'^api/usage/(?P<pk>[0-9]+)$', views.usage_detail)
]
