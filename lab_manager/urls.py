from django.conf.urls import url
from lab_manager import views

app_name = 'lab_manager'

urlpatterns = [
    url(r'^api/printers$', views.fablab_printers),
    url(r'^api/printers/(?P<pk>[0-9]+)$', views.fablab_printers_detail),
    url('api/filament/', views.filament_usage_default),
    url(r'^api/operating$', views.operating_usage_default),
    url(r'^api/maintenance$', views.maintenance),
    url(r'^api/printer$', views.printer_usage_default),
    url(r'^api/usage$', views.usage),
    url(r'^api/usage/(?P<pk>[0-9]+)$', views.usage_detail)

]
