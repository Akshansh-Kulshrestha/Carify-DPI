from django.http import HttpResponse
from reportlab.pdfgen import canvas
from CarPDI.models import Vehicle
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, LoginForm, CustomPasswordResetForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.views import PasswordResetView
from CarPDI.models import *
from django.db.models import Avg, Count
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.sessions.models import Session
from django.utils import timezone


User = get_user_model()

class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'auth/password_reset.html'
    email_template_name = 'registration/password_reset_email.html'
    subject_template_name = 'registration/password_reset_subject.txt'
    form_class = CustomPasswordResetForm
    success_url = '/home/password_reset/done'

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            return render(request, 'user/register.html', {'form': form})
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
            if user is not None:
                login(request, user)

                if not remember_me:
                    request.session.set_expiry(6000)  # Session lasts ~100 minutes

                return redirect('admin_dashboard')
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = LoginForm()
    
    return render(request, 'user/login.html', {'form': form})

    
def logout_view(request):
    logout(request)
    return redirect('login')

def is_admin(user):
    return user.is_authenticated and user.is_superuser

def is_staff(user):
    return user.is_authenticated and user.is_verified_by_admin

def is_both(user):
    return user.is_authenticated and user.is_superuser and user.is_staff

@login_required
@user_passes_test(is_staff)
def admin_dashboard(request):
    total_vehicles = Vehicle.objects.count()
    total_customers = Customer.objects.count()
    avg_health_score = Vehicle.objects.aggregate(avg=Avg('health_score'))['avg'] or 0
    recent_inspections = Vehicle.objects.filter(
        inspection_date__gte=datetime.today() - timedelta(days=7)
    ).count()
    
    vehicles = Vehicle.objects.select_related('customer').all()
    width_total_vehicles = total_vehicles * 10
    width_total_customers = total_customers * 10
    width_avg_health_score = avg_health_score 
    width_recent_inspections = recent_inspections * 10
    dashboard_cards = [
        {
            'label': 'Total Customers',
            'icon': 'fa-users',
            'value': total_customers,
            'width': width_total_customers,
        },
        {
            'label': 'Total Vehicles',
            'icon': 'fa-car',
            'value': total_vehicles,
            'width': width_total_vehicles,
        },
        {
            'label': 'Avg. Health Score',
            'icon': 'fa-heart-pulse',
            'value': avg_health_score,
            'width': width_avg_health_score,
        },
        {
            'label': 'Recent Inspections',
            'icon': 'fa-clipboard-check',
            'value': recent_inspections,
            'width': width_recent_inspections,
        },
    ]

    context = {
        'dashboard_cards': dashboard_cards,
        'vehicles': vehicles,
    }
    return render(request, 'user/admin_dashboard1.html', context)



def print_vehicle_report(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    # Create the HttpResponse object with PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="vehicle_report_{vehicle_id}.pdf"'

    # Create a PDF object
    p = canvas.Canvas(response)

    # Add some text
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, 800, "Vehicle Inspection Report")

    p.setFont("Helvetica", 12)
    p.drawString(100, 770, f"Customer Name: {vehicle.customer.name}")
    p.drawString(100, 750, f"Vehicle: {vehicle.maker} {vehicle.model}")
    p.drawString(100, 730, f"Health Score: {vehicle.health_score}")
    p.drawString(100, 710, f"Inspection Date: {vehicle.inspection_date.strftime('%Y-%m-%d')}")

    # Add more details as needed, e.g. vehicle attributes, inspection notes, etc.

    p.showPage()
    p.save()

    return response

def delete_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    vehicle.delete()
    return redirect('admin_dashboard')


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
def user_dashboard(request):
    users = CustomUser.objects.annotate(vehicle_count=Count('inspected_vehicles'))
    total_users = users.count()
    active_user_ids = get_active_user_ids()
    active_users = users.filter(id__in=active_user_ids).count()
    inactive_users = total_users - active_users
    verified_users = users.filter(is_verified_by_admin=True).count()





    # Compute bar widths
    width_total_users = total_users * 10
    width_active_users = active_users * 10
    width_inactive_users = inactive_users * 10

    dashboard_cards = [
        {
            'label': 'Total Users',
            'icon': 'fa-users',
            'value': total_users,
            'width': width_total_users,
        },
        {
            'label': 'Active Users',
            'icon': 'fa-user-check',
            'value': active_users,
            'width': width_active_users,
        },
        {
            'label': 'Inactive Users',
            'icon': 'fa-user-slash',
            'value': inactive_users,
            'width': width_inactive_users,
        },

        {
            'label': 'Verified by Admin',
            'icon': 'fa-user-shield',
            'value': verified_users,
            'width': verified_users * 10,
        },
    ]

    context = {
        'dashboard_cards': dashboard_cards,
        'users': users,
    }
    return render(request, 'user/user_dashboard.html', context)

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

@login_required
def vehicles_inspected_by_single_user(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    vehicles = Vehicle.objects.filter(inspected_by=user).order_by('-inspection_date')
    return render(request, 'car/inspected_by_user.html', {
        'inspector': user,
        'vehicles': vehicles
    })

@login_required
def vehicles_inspected(request):
    vehicles = Vehicle.objects.all().order_by('-inspection_date')
    return render(request, 'car/inspected_cars.html', {
        'vehicles': vehicles,
    })