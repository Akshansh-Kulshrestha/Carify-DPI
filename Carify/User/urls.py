from . import views
from django.urls import path

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    path('', views.admin_dashboard, name="admin_dashboard"),
    path('user/', views.user_dashboard, name='user_dashboard'),
    path('verify-user/<int:user_id>/', views.verify_user_view, name='verify_user'),
    path('unverify-user/<int:user_id>/', views.unverify_user_view, name='unverify_user'),
    path('delete-user/<int:user_id>/', views.delete_user_view, name='delete_user'),

    path('vehicles/inspected/user/<int:user_id>/', views.vehicles_inspected_by_single_user, name='vehicles_inspected_by_user'),
    path('vehicles/inspected/', views.vehicles_inspected, name='vehicles_inspected'),

    path('vehicle/<int:vehicle_id>/print/', views.print_vehicle_report, name='print_vehicle_report'),
    path('vehicle/delete/<int:pk>/', views.delete_vehicle, name='delete_vehicle'),

    path('roles-dashboard/', views.roles_dashboard, name='roles_dashboard'),
    path('role-manage/', views.manage_roles_permissions, name='manage_roles_permissions'),
    path('assign-role-permission/', views.assign_permissions_to_role, name='assign_permissions_to_role'),
    path('assign-user-role/<int:user_id>', views.assign_roles_to_users, name='assign_roles_to_users'),


]
