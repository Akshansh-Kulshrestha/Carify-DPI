from .forms import (
    CustomerForm, VehicleForm, OBDReadingForm, SystemCheckForm, NetworkSystemForm,
    FluidLevelForm, PerformanceCheckForm, PaintFinishForm, TyreConditionForm,
    FlushGapForm, RubberComponentForm, GlassComponentForm, InteriorComponentForm,
    DocumentationForm, LiveParameterForm
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import *
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


FORM_CLASSES = {
    'customer': CustomerForm,
    'vehicle': VehicleForm,
    'obdreading': OBDReadingForm,
    'systemcheck': SystemCheckForm,
    'networksystem': NetworkSystemForm,
    'fluidlevel': FluidLevelForm,
    'liveparameters': LiveParameterForm,
    'performancecheck': PerformanceCheckForm,
    'paintfinish': PaintFinishForm,
    'tyrecondition': TyreConditionForm,
    'flushgap': FlushGapForm,
    'rubbercomponent': RubberComponentForm,
    'glasscomponent': GlassComponentForm,
    'interiorcomponent': InteriorComponentForm,
    'documentation': DocumentationForm,
}



from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages

@login_required
def unified_form_view(request):
    form_order = list(FORM_CLASSES.keys())
    current_form_name = request.GET.get('form', 'customer')
    FormClass = FORM_CLASSES[current_form_name]

    if request.method == 'POST':
        current_form_name = request.POST.get('save_section') or request.POST.get('navigate_previous')
        FormClass = FORM_CLASSES[current_form_name]
        current_form = FormClass(request.POST, request.FILES)

        customer_id = request.session.get('customer_id')
        vehicle_id = request.session.get('vehicle_id')

        # Validation
        if current_form_name == 'vehicle' and not customer_id:
            messages.error(request, "Please fill out the Customer form first.")
            return redirect(reverse('unified_form') + '?form=customer')

        if current_form_name not in ['customer', 'vehicle'] and not vehicle_id:
            messages.error(request, "Please fill out the Vehicle form first.")
            return redirect(reverse('unified_form') + '?form=vehicle')

        if current_form.is_valid():
            instance = current_form.save(commit=False)

            if current_form_name == 'vehicle':
                instance.customer = get_object_or_404(Customer, id=customer_id)
                if not instance.inspected_by_id:
                    instance.inspected_by = request.user
                if not instance.inspection_date:
                    instance.inspection_date = timezone.now().date()

            if current_form_name not in ['customer', 'vehicle']:
                instance.vehicle = get_object_or_404(Vehicle, id=vehicle_id)

            instance.save()

            if current_form_name == 'customer':
                request.session['customer_id'] = instance.id

            if current_form_name == 'vehicle':
                request.session['vehicle_id'] = instance.id

            if 'save_section' in request.POST:
                next_index = form_order.index(current_form_name) + 1
                if next_index < len(form_order):
                    next_form = form_order[next_index]
                    return redirect(reverse('unified_form') + f'?form={next_form}')
                else:
                    messages.success(request, "All sections completed successfully.")
                    request.session.pop('customer_id', None)
                    request.session.pop('vehicle_id', None)
                    return redirect('success')

        if 'navigate_previous' in request.POST:
            if current_form_name in form_order:
                current_index = form_order.index(current_form_name)
                if current_index > 0:
                    prev_form = form_order[current_index - 1]
                    return redirect(reverse('unified_form') + f'?form={prev_form}')

    else:
        # GET request
        initial_data = {}

        if current_form_name == 'vehicle':
            customer_id = request.session.get('customer_id')
            if customer_id:
                initial_data['customer'] = customer_id
            initial_data['inspection_date'] = timezone.now().date()
            initial_data['inspected_by'] = request.user.id

        if current_form_name not in ['customer', 'vehicle']:
            vehicle_id = request.session.get('vehicle_id')
            if vehicle_id:
                initial_data['vehicle'] = vehicle_id

        current_form = FormClass(initial=initial_data)

    all_forms = {
        name: (current_form if name == current_form_name else FORM_CLASSES[name]())
        for name in form_order
    }

    return render(request, 'car/unified_form1.html', {
        'all_forms': all_forms,
        'current_form': current_form_name,
        'form_names': form_order,
    })


def success_view(request):
    return render(request, 'car/success.html')

@csrf_exempt
def add_transmission_ajax(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            transmission = VehicleTransmission.objects.create(name=name)
            return JsonResponse({
                "status": "success",
                "id": transmission.id,
                "name": transmission.name
            })
        return JsonResponse({"status": "error", "message": "Name is required."})

@csrf_exempt  # or use @require_POST and CSRF token properly
def add_fuel_type_ajax(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if not name:
            return JsonResponse({"status": "error", "message": "Fuel name required"})

        obj, created = VehicleFuelType.objects.get_or_create(name=name)
        return JsonResponse({"status": "success", "id": obj.id, "name": obj.name})

    return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)