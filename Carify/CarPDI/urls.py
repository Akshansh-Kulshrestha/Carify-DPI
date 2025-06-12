from django.urls import path
from . import views

urlpatterns = [
    path('', views.unified_form_view, name='unified_form'),
    path('success/', views.success_view, name='success'),  

    path('add-transmission/', views.add_transmission_ajax, name='add_transmission_ajax'),
    path('add-fuel-type/', views.add_fuel_type_ajax, name='add_fuel_type_ajax'),


]
