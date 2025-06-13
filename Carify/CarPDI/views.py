# views/customer_view.py
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .models import *
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect

@csrf_exempt
def customer_view(request):
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()  # ✅ always create new customer
            request.session['customer_id'] = customer.id  # ✅ store in session
            return redirect('form_vehicle')  # ✅ redirect to vehicle form view
    else:
        form = CustomerForm()

    # 🟡 Always return a response, even after POST fails
    return render(request, 'car/index.html', {
        'form': form,
        'current_form': 'customer'
    })


@csrf_exempt
def vehicle_view(request):
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return JsonResponse({
            'success': False,
            'message': 'Customer ID not found in session.',
            'redirect': '/carify/form/customer/'
        }, status=400)

    customer = get_object_or_404(Customer, id=customer_id)
    instance = Vehicle.objects.filter(customer_id=customer_id).first()

    if request.method == 'POST':
        request.POST = request.POST.copy()  # ✅ Make mutable immediately

        # TRANSMISSION
        custom_transmission = request.POST.get('custom_transmission')
        selected_transmission = request.POST.get('transmission')
        if custom_transmission and selected_transmission == '__custom__':
            trans_type, _ = VehicleTransmission.objects.get_or_create(
                name__iexact=custom_transmission,
                defaults={'name': custom_transmission}
            )
            request.POST['transmission'] = trans_type.id

        # ENGINE
        custom_engine = request.POST.get('custom_engine')
        selected_engine = request.POST.get('engine_type')
        if custom_engine and selected_engine == '__custom__':
            eng_type, _ = VehicleEngineType.objects.get_or_create(
                name__iexact=custom_engine,
                defaults={'name': custom_engine}
            )
            request.POST['engine_type'] = eng_type.id

        # FUEL
        custom_fuel = request.POST.get('custom_fuel')
        selected_fuel_id = request.POST.get('fuel_type')
        if custom_fuel and selected_fuel_id == '__custom__':
            fuel_type, _ = VehicleFuelType.objects.get_or_create(
                name__iexact=custom_fuel,
                defaults={'name': custom_fuel}
            )
            request.POST['fuel_type'] = fuel_type.id

        form = VehicleForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.customer = customer
            if not vehicle.inspection_date:
                vehicle.inspection_date = timezone.now().date()
            if not vehicle.inspected_by_id:
                vehicle.inspected_by = request.user
            vehicle.save()
            request.session['vehicle_id'] = vehicle.id
            return redirect ('form_obdreading')

    else:
        initial_data = {
            'customer': customer_id,
            'inspection_date': timezone.now().date(),
            'inspected_by': request.user.id,
        }
        form = VehicleForm(instance=instance, initial=initial_data)
        return render(request, 'car/index.html', {
            'form': form,
            'current_form': 'vehicle',
            'fuel_types': VehicleFuelType.objects.all(),
            'transmission_types': VehicleTransmission.objects.all(),
            'engine_types': VehicleEngineType.objects.all(),
            'customer': customer
        })



@csrf_exempt
def obdreading_view(request):
    vehicle_id = request.session.get('vehicle_id')
    if not vehicle_id:
        return JsonResponse({
            'success': False,
            'message': 'Vehicle ID not found in session.',
            'redirect': '/carify/form/vehicle/'
        }, status=400)

    instance = OBDReading.objects.filter(vehicle_id=vehicle_id).first()
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == 'POST':
        form = OBDReadingForm(request.POST, instance=instance)
        if form.is_valid():
            obd = form.save(commit=False)
            obd.vehicle = get_object_or_404(Vehicle, id=vehicle_id)
            obd.save()
            return redirect('form_systemcheck')
    else:
        form = OBDReadingForm(instance=instance)
        return render(request, 'car/index.html', {'form': form, 'current_form': 'obdreading', 'vehicle': vehicle})

def success_view(request):
    return render(request, 'car/success.html')

from .models import System, Status

@csrf_exempt
def systemcheck_view(request):
    vehicle_id = request.session.get('vehicle_id')
    if not vehicle_id:
        return JsonResponse({
            'success': False,
            'message': 'Vehicle ID not found in session.',
            'redirect': '/carify/form/vehicle/'
        }, status=400)

    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == 'POST':
        systems = request.POST.getlist('system')
        statuses = request.POST.getlist('status')
        issues = request.POST.getlist('number_of_issues')

        for sys, stat, num in zip(systems, statuses, issues):
            system = get_object_or_404(System, id=sys)
            status = get_object_or_404(Status, id=stat)
            SystemCheck.objects.create(
                vehicle=vehicle,
                system=system,
                status=status,
                number_of_issues=int(num)
            )

        return JsonResponse({
            'success': True,
            'message': 'System checks saved successfully.',
            'next_url': '/carify/form/some_next_form/'
        })

    systems = System.objects.all()
    statuses = Status.objects.all()
    return render(request, 'car/index.html', {
        'current_form': 'systemcheck',
        'systems': systems,
        'statuses': statuses,
        'vehicle': vehicle,
    })

