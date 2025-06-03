from django.urls import path
from . import views

urlpatterns = [
    path('-<str:form_name>/', views.unified_form_view, name='unified_form'),
    path('success/', views.success_view, name='success'),  
]
