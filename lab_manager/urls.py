from django.conf.urls import url 
from lab_manager import views

app_name = 'lab_manager'

urlpatterns = [
    url(r'^api/users$', views.user_list),
    url(r'^api/material$', views.material_usage_default),
    url(r'^api/operating$', views.operating_usage_default),
    url(r'^api/printer$', views.printer_usage_default),
    url(r'^api/usage$', views.usage),
    url(r'^api/usage/(?P<pk>[0-9]+)$', views.usage_detail)
]