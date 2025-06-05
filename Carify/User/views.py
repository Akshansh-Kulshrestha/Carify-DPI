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
        