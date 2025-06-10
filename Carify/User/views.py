# views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.db.models import Avg, Count
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist

from reportlab.pdfgen import canvas

# Custom app models and forms
from CarPDI.models import Vehicle, Customer
from .models import CustomUser, Roles, Permissions, UserRole
from .forms import RegistrationForm, LoginForm, RoleForm, PermissionForm,  UserRoleAssignForm, RolePermissionForm

# Role management utilities
from .permission import assign_role_to_user, assign_permission_to_role, user_has_permission

User = get_user_model()

# ========== Authentication Views ==========

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'user/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me')
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                if not remember_me:
                    request.session.set_expiry(6000)
                return redirect('admin_dashboard')
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# ========== Access Control Decorators ==========

def is_admin(user):
    return user.is_authenticated and user.is_staff

def is_staff(user):
    return user.is_authenticated and user.is_verified_by_admin

def is_both(user):
    return user.is_authenticated and user.is_superuser and user.is_staff


# ========== Dashboard View ==========

@login_required
@user_passes_test(is_staff)
def admin_dashboard(request):
    total_vehicles = Vehicle.objects.count()
    total_customers = Customer.objects.count()
    avg_health_score = Vehicle.objects.aggregate(avg=Avg('health_score'))['avg'] or 0
    recent_inspections = Vehicle.objects.filter(inspection_date__gte=datetime.today() - timedelta(days=7)).count()

    vehicles = Vehicle.objects.select_related('customer').all()

    dashboard_cards = [
        {
            'label': 'Total Customers',
            'icon': 'fa-users',
            'value': total_customers,
            'width': total_customers * 10,
        },
        {
            'label': 'Total Vehicles',
            'icon': 'fa-car',
            'value': total_vehicles,
            'width': total_vehicles * 10,
        },
        {
            'label': 'Avg. Health Score',
            'icon': 'fa-heart-pulse',
            'value': avg_health_score,
            'width': avg_health_score,
        },
        {
            'label': 'Recent Inspections',
            'icon': 'fa-clipboard-check',
            'value': recent_inspections,
            'width': recent_inspections * 10,
        },
    ]

    context = {
        'dashboard_cards': dashboard_cards,
        'vehicles': vehicles,
        'page_title': 'Dashboard'
    }
    return render(request, 'user/admin_dashboard1.html', context)


# ========== Vehicle Views ==========

def print_vehicle_report(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="vehicle_report_{vehicle_id}.pdf"'
    p = canvas.Canvas(response)
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "Vehicle Inspection Report")
    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Customer Name: {vehicle.customer.name}")
    p.drawString(100, 750, f"Vehicle: {vehicle.maker} {vehicle.model}")
    p.drawString(100, 730, f"Health Score: {vehicle.health_score}")
    p.drawString(100, 710, f"Inspection Date: {vehicle.inspection_date.strftime('%Y-%m-%d')}")
    p.showPage()
    p.save()
    return response


def delete_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    vehicle.delete()
    return redirect('admin_dashboard')


@login_required
def vehicles_inspected_by_single_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    vehicles = Vehicle.objects.filter(inspected_by=user).order_by('-inspection_date')
    return render(request, 'car/inspected_by_user.html', {
        'inspector': user,
        'vehicles': vehicles,
        'page_title': 'My Vehicles'
    })


@login_required
def vehicles_inspected(request):
    vehicles = Vehicle.objects.all().order_by('-inspection_date')
    return render(request, 'car/inspected_cars.html', {
        'vehicles': vehicles,
        'page_title': 'All Vehicles'
    })


# ========== User Management ==========

@login_required
@user_passes_test(is_admin)
def user_dashboard(request):
    users = CustomUser.objects.annotate(vehicle_count=Count('inspected_vehicles'))
    total_users = users.count()
    active_user_ids = get_active_user_ids()
    active_users = users.filter(id__in=active_user_ids).count()
    inactive_users = total_users - active_users
    verified_users = users.filter(is_verified_by_admin=True).count()

    dashboard_cards = [
        {
            'label': 'Total Users',
            'icon': 'fa-users',
            'value': total_users,
            'width': total_users * 10,
        },
        {
            'label': 'Active Users',
            'icon': 'fa-user-check',
            'value': active_users,
            'width': active_users * 10,
        },
        {
            'label': 'Inactive Users',
            'icon': 'fa-user-slash',
            'value': inactive_users,
            'width': inactive_users * 10,
        },
        {
            'label': 'Verified by Admin',
            'icon': 'fa-user-shield',
            'value': verified_users,
            'width': verified_users * 10,
        },
    ]

    return render(request, 'user/user_dashboard.html', {
        'dashboard_cards': dashboard_cards,
        'users': users,
        'page_title': 'User Management',
    })


def get_active_user_ids():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_ids = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id = data.get('_auth_user_id')
        if user_id:
            user_ids.append(user_id)
    return user_ids


@login_required
@user_passes_test(is_admin)
def verify_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_verified_by_admin = True
    user.save()
    messages.success(request, f"User {user.username} has been verified.")
    return redirect('user_dashboard')


@login_required
@user_passes_test(is_admin)
def unverify_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.is_verified_by_admin = False
    user.save()
    messages.success(request, f"User {user.username} has been unverified.")
    return redirect('user_dashboard')


@login_required
@user_passes_test(is_admin)
def delete_user_view(request, user_id):
    user_obj = get_object_or_404(CustomUser, id=user_id)
    user_obj.delete()
    messages.success(request, 'User deleted successfully.')
    return redirect('user_dashboard')


# ========== Role & Permission Views ==========

@login_required
@user_passes_test(is_admin)
def roles_dashboard(request):
    role_form = RoleForm(request.POST or None)
    permission_form = RolePermissionForm(request.POST or None)

    if request.method == 'POST':
        if 'create_role' in request.POST and role_form.is_valid():
            role_form.save()
            return redirect('roles_dashboard')

        if 'assign_permissions' in request.POST and permission_form.is_valid():
            role = permission_form.cleaned_data['role']
            permissions = permission_form.cleaned_data['permissions']
            role.permissions.set(permissions)  # <-- Correct way now
            return redirect('roles_dashboard')

    roles = Roles.objects.all().prefetch_related('permissions')
    grouped_permissions = {
        role.id: [perm.name for perm in role.permissions.all()]
        for role in roles
    }
    user_roles = UserRole.objects.select_related('user', 'role')

    return render(request, 'roles/dashboard.html', {
        'role_form': role_form,
        'permission_form': permission_form,
        'roles': roles,
        'grouped_permissions': grouped_permissions,
        'user_roles': user_roles,
        'page_title': 'Roles Dashboard'

    })


@login_required
@user_passes_test(is_admin)
def manage_roles_permissions(request):
    roles = Roles.objects.all()
    permissions = Permissions.objects.all()
    role_form = RoleForm(request.POST or None)
    permission_form = PermissionForm(request.POST or None)

    if request.method == 'POST':
        if 'create_role' in request.POST and role_form.is_valid():
            role = role_form.save()
            messages.success(request, f"Role '{role.name}' created successfully.")
            return redirect('manage_roles_permissions')

        elif 'create_permission' in request.POST and permission_form.is_valid():
            permission = permission_form.save()
            messages.success(request, f"Permission '{permission.name}' created successfully.")
            return redirect('manage_roles_permissions')

        elif 'assign_permission_to_role' in request.POST:
            role_id = request.POST.get('role_id')
            permission_id = request.POST.get('permission_id')
            try:
                role = Roles.objects.get(id=role_id)
                permission = Permissions.objects.get(code=permission_id)
                assign_permission_to_role(role.name, permission.name)
                messages.success(request, f"Permission '{permission.name}' assigned to role '{role.name}'.")
            except ObjectDoesNotExist as e:
                messages.error(request, str(e))
            return redirect('manage_roles_permissions')

    return render(request, 'roles/roles_permission.html', {
        'roles': roles,
        'permissions': permissions,
        'role_form': role_form,
        'permission_form': permission_form,
    })


@login_required
@user_passes_test(is_admin)
def assign_permissions_to_role(request):
    form = RolePermissionForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        role = form.cleaned_data['role']
        permissions = form.cleaned_data['permissions']
        role.permissions.set(permissions)
        return redirect('assign_permissions_to_role')

    roles = Roles.objects.all().prefetch_related('permissions')
    grouped_permissions = {
        role.id: [perm.name for perm in role.permissions.all()]
        for role in roles
    }

    return render(request, 'roles/assign_permissions.html', {
        'form': form,
        'grouped_permissions': grouped_permissions
    })


@login_required
@user_passes_test(is_admin)
def assign_roles_to_users(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    form = UserRoleAssignForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        role = form.cleaned_data['role']
        UserRole.objects.update_or_create(user=user, defaults={'role': role})
        return redirect('assign_roles_to_users', user_id=user.id)

    assignments = UserRole.objects.select_related('user', 'role')
    return render(request, 'roles/assign_roles.html', {
        'form': form,
        'assignments': assignments,
        'selected_user': user
    })

