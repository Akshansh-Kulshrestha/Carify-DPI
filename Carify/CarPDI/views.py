from .forms import (
    CustomerForm, VehicleForm, OBDReadingForm, SystemCheckForm, NetworkSystemForm,
    FluidLevelForm, PerformanceCheckForm, PaintFinishForm, TyreConditionForm,
    FlushGapForm, RubberComponentForm, GlassComponentForm, InteriorComponentForm,
    DocumentationForm, LiveParameterForm
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Vehicle, Customer
from django.contrib import messages


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



def unified_form_view(request):
    form_order = list(FORM_CLASSES.keys())
    current_form_name = request.GET.get('form', 'customer')

    FormClass = FORM_CLASSES[current_form_name]

    if request.method == 'POST':
        current_form_name = request.POST.get('save_section') or request.POST.get('navigate_previous')
        FormClass = FORM_CLASSES[current_form_name]

        current_form = FormClass(request.POST, request.FILES)

        # Get session IDs
        customer_id = request.session.get('customer_id')
        vehicle_id = request.session.get('vehicle_id')

        # Validation: Customer must be filled before vehicle
        if current_form_name == 'vehicle' and not customer_id:
            messages.error(request, "Please fill out the Customer form first.")
            return redirect(reverse('unified_form') + '?form=customer')

        # Validation: Vehicle must be filled before other forms
        if current_form_name not in ['customer', 'vehicle'] and not vehicle_id:
            messages.error(request, "Please fill out the Vehicle form first.")
            return redirect(reverse('unified_form') + '?form=vehicle')

        if current_form.is_valid():
            instance = current_form.save(commit=False)

            # Associate customer to Vehicle form
            if current_form_name == 'vehicle':
                instance.customer = get_object_or_404(Customer, id=customer_id)

            # Associate vehicle to all other forms except Customer and Vehicle
            if current_form_name not in ['customer', 'vehicle']:
                instance.vehicle = get_object_or_404(Vehicle, id=vehicle_id)

            instance.save()

            # Save customer_id in session after Customer form is saved
            if current_form_name == 'customer':
                request.session['customer_id'] = instance.id

            # Save vehicle_id in session after Vehicle form is saved
            if current_form_name == 'vehicle':
                request.session['vehicle_id'] = instance.id

            # Navigation logic
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

            elif 'navigate_previous' in request.POST:
                prev_index = form_order.index(current_form_name) - 1
                prev_form = form_order[prev_index]
                return redirect(reverse('unified_form') + f'?form={prev_form}')

    else:
        # For GET requests
        initial_data = {}

        # If vehicle form, preload customer foreign key from session
        if current_form_name == 'vehicle':
            customer_id = request.session.get('customer_id')
            if customer_id:
                initial_data['customer'] = customer_id

        # For other forms except customer and vehicle, preload vehicle foreign key
        if current_form_name not in ['customer', 'vehicle']:
            vehicle_id = request.session.get('vehicle_id')
            if vehicle_id:
                initial_data['vehicle'] = vehicle_id

        current_form = FormClass(initial=initial_data)

    all_forms = {
        name: (current_form if name == current_form_name else FORM_CLASSES[name]())
        for name in form_order
    }
    print(form_order)
    return render(request, 'car/unified_form1.html', {
        'all_forms': all_forms,
        'current_form': current_form_name,
        'form_names': form_order,
    })


def success_view(request):
    return render(request, 'car/success.html')
