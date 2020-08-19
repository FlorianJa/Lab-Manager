from django.urls import path
from pay_by_use import views


urlpatterns = [
    path('', views.index),
]
