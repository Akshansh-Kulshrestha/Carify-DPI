from django.urls import path
from . import views

urlpatterns = [
    path('', views.unified_form_view, name='unified_form'),
    path('success/', views.success_view, name='success'),  
]
