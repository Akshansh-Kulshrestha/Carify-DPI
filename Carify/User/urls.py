from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    path('', views.admin_dashboard, name="admin_dashboard"),
    path('vehicle/<int:vehicle_id>/print/', views.print_vehicle_report, name='print_vehicle_report'),
    path('vehicle/delete/<int:pk>/', views.delete_vehicle, name='delete_vehicle'),

]
