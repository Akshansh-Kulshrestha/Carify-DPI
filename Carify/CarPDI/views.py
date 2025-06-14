# views/customer_view.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import *
from .models import *
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.html import escapejs
import json

@csrf_exempt
def customer_view(request):
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()  
            request.session['customer_id'] = customer.id  
            return redirect('form_vehicle')  
    else:
        form = CustomerForm()

    # 🟡 Always return a response, even after POST fails
    return render(request, 'car/form.html', {
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
        request.POST = request.POST.copy()  

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
        return render(request, 'car/form.html', {
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
            obd.vehicle = vehicle
            obd.save()
            return redirect('form_systemcheck')  
        else:
            return JsonResponse({
                'success': False,
                'message': 'Validation failed.',
                'errors': form.errors
            }, status=400)
    
    form = OBDReadingForm(instance=instance)
    return render(request, 'car/form.html', {
        'form': form,
        'current_form': 'obdreading',
        'vehicle': vehicle
    })



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
        custom_systems = request.POST.getlist('custom_system')
        statuses = request.POST.getlist('status')
        custom_statuses = request.POST.getlist('custom_status')
        issues = request.POST.getlist('number_of_issues')

        total = len(systems)
        if not (len(custom_systems) == len(statuses) == len(custom_statuses) == len(issues) == total):
            return JsonResponse({
                'success': False,
                'message': 'Mismatched row lengths.',
            }, status=400)

        for i in range(total):
            system_id = systems[i]
            status_id = statuses[i]
            num_issues = int(issues[i]) if issues[i] else 0

            # Handle custom system
            if system_id == '__custom__' and custom_systems[i].strip():
                system_obj, _ = System.objects.get_or_create(
                    name__iexact=custom_systems[i].strip(),
                    defaults={'name': custom_systems[i].strip()}
                )
            else:
                try:
                    system_obj = get_object_or_404(System, id=int(system_id))
                except (ValueError, System.DoesNotExist):
                    continue  
            # Handle custom status
            if status_id == '__custom__' and custom_statuses[i].strip():
                status_obj, _ = Status.objects.get_or_create(
                    name__iexact=custom_statuses[i].strip(),
                    defaults={'name': custom_statuses[i].strip()}
                )
            else:
                try:
                    status_obj = get_object_or_404(Status, id=int(status_id))
                except (ValueError, Status.DoesNotExist):
                    continue  
            SystemCheck.objects.create(
                vehicle=vehicle,
                system=system_obj,
                status=status_obj,
                number_of_issues=num_issues
            )

        return redirect('form_networksystem')

    # Querysets for dropdowns (HTML usage)
    systems_qs = System.objects.all()
    statuses_qs = Status.objects.all()

    # JSON-safe data for JavaScript usage
    systems = list(System.objects.values('id', 'name'))
    statuses = list(Status.objects.values('id', 'name'))
    return render(request, 'car/form.html', {
    'current_form': 'systemcheck',
    'vehicle': vehicle,
    'systems': systems_qs,       
    'statuses': statuses_qs,
    'systems_json': json.dumps(systems),
    'statuses_json':json.dumps(statuses),
    })


@csrf_exempt
def networksystem_view(request):
    vehicle_id = request.session.get("vehicle_id")
    if not vehicle_id:
        return JsonResponse({'success': False, 'message': 'Vehicle ID not found in session'}, status=400)

    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == "POST":
        areas = request.POST.getlist('area')
        custom_areas = request.POST.getlist('custom_area')
        statuses = request.POST.getlist('status')
        custom_statuses = request.POST.getlist('custom_status')
        remarks = request.POST.getlist('remark')

        for i in range(len(areas)):
            # Area
            area_id = areas[i]
            if area_id == "__custom__" and custom_areas[i].strip():
                area, _ = NetworkArea.objects.get_or_create(name=custom_areas[i].strip())
            else:
                area = get_object_or_404(NetworkArea, id=area_id)

            # Status
            status_id = statuses[i]
            if status_id == "__custom__" and custom_statuses[i].strip():
                status, _ = Status.objects.get_or_create(name=custom_statuses[i].strip())
            else:
                status = get_object_or_404(Status, id=status_id)

            remark = remarks[i]

            NetworkSystem.objects.create(
                vehicle=vehicle,
                area=area,
                status=status,
                remark=remark
            )

        return redirect('form_liveparameters')  
    # GET: render form
    areas_qs = list(NetworkArea.objects.values('id', 'name'))
    statuses_qs = list(Status.objects.values('id', 'name'))

    return render(request, 'car/form.html', {
        'current_form': 'networksystem',
        'vehicle': vehicle,
        'areas': NetworkArea.objects.all(),
        'statuses': Status.objects.all(),
        'areas_json': json.dumps(areas_qs),
        'statuses_json': json.dumps(statuses_qs)
    })
@csrf_exempt
def liveparameters_view(request):
    vehicle_id = request.session.get("vehicle_id")
    if not vehicle_id:
        return JsonResponse({
            'success': False,
            'message': 'Vehicle ID not found in session.'
        }, status=400)

    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == "POST":
        systems = request.POST.getlist('system')
        custom_systems = request.POST.getlist('custom_system')
        inferences = request.POST.getlist('inference')
        custom_inferences = request.POST.getlist('custom_inference')

        for i in range(len(systems)):
            system_id = systems[i]
            inf_id = inferences[i]

            if system_id == "__custom__" and custom_systems[i].strip():
                system, _ = Parameters.objects.get_or_create(name=custom_systems[i].strip())
            else:
                system = get_object_or_404(Parameters, id=system_id)

            if inf_id == "__custom__" and custom_inferences[i].strip():
                inference, _ = VoltageInference.objects.get_or_create(name=custom_inferences[i].strip())
            else:
                inference = get_object_or_404(VoltageInference, id=inf_id)

            LiveParameters.objects.create(vehicle=vehicle, system=system, interence=inference)

        return redirect('form_performancecheck')  

    # GET request: return form
    param_qs = list(Parameters.objects.values('id', 'name'))
    inf_qs = list(VoltageInference.objects.values('id', 'voltage'))

    return render(request, 'car/form.html', {
        'current_form': 'liveparameters',
        'vehicle': vehicle,
        'parameters': Parameters.objects.all(),
        'inferences': VoltageInference.objects.all(),
        'parameters_json': json.dumps(param_qs),
        'inferences_json': json.dumps(inf_qs),
    })

@csrf_exempt
def performancecheck_view(request):
    vehicle_id = request.session.get("vehicle_id")
    if not vehicle_id:
        return JsonResponse({'success': False, 'message': 'Vehicle ID not in session'}, status=400)

    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == "POST":
        systems = request.POST.getlist("system")
        custom_systems = request.POST.getlist("custom_system")
        statuses = request.POST.getlist("status")
        custom_statuses = request.POST.getlist("custom_status")
        recommendations = request.POST.getlist("recommendation")

        for i in range(len(systems)):
            # System handling
            sys_id = systems[i]
            if sys_id == "__custom__" and custom_systems[i].strip():
                system, _ = Performance.objects.get_or_create(name=custom_systems[i].strip())
            else:
                system = get_object_or_404(Performance, id=sys_id)

            # Status handling
            stat_id = statuses[i]
            if stat_id == "__custom__" and custom_statuses[i].strip():
                status, _ = Status.objects.get_or_create(name=custom_statuses[i].strip())
            else:
                status = get_object_or_404(Status, id=stat_id)

            PerformanceCheck.objects.create(
                vehicle=vehicle,
                system=system,
                status=status,
                recommendation=recommendations[i]
            )

        return redirect('form_fluidlevel')  
    # GET
    systems = list(Performance.objects.values('id', 'name'))
    statuses = list(Status.objects.values('id', 'name'))

    return render(request, "car/form.html", {
        'current_form': 'performancecheck',
        'vehicle': vehicle,
        'performance_systems': Performance.objects.all(),
        'statuses': Status.objects.all(),
        'performance_json': json.dumps(systems),
        'statuses_json': json.dumps(statuses),
    })

@csrf_exempt
def fluidlevel_view(request):
    vehicle_id = request.session.get('vehicle_id')
    if not vehicle_id:
        return JsonResponse({'success': False, 'message': 'Vehicle ID not found'}, status=400)

    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == 'POST':
        areas = request.POST.getlist('area')
        custom_areas = request.POST.getlist('custom_area')
        ranges = request.POST.getlist('in_range')
        custom_ranges = request.POST.getlist('custom_range')
        statuses = request.POST.getlist('contamination')
        custom_statuses = request.POST.getlist('custom_status')
        recommendations = request.POST.getlist('recommendation')

        for i in range(len(areas)):
            # Area
            if areas[i] == '__custom__' and custom_areas[i].strip():
                area, _ = FluidArea.objects.get_or_create(name=custom_areas[i].strip())
            else:
                area = get_object_or_404(FluidArea, id=areas[i])

            # Range
            if ranges[i] == '__custom__' and custom_ranges[i].strip():
                in_range, _ = FluidRange.objects.get_or_create(name=custom_ranges[i].strip())
            else:
                in_range = get_object_or_404(FluidRange, id=ranges[i])

            # Status
            if statuses[i] == '__custom__' and custom_statuses[i].strip():
                contamination, _ = Status.objects.get_or_create(name=custom_statuses[i].strip())
            else:
                contamination = get_object_or_404(Status, id=statuses[i])

            # Save
            FluidLevel.objects.create(
                vehicle=vehicle,
                area=area,
                in_range=in_range,
                contamination=contamination,
                recommendation=recommendations[i]
            )

        return redirect('form_tyrecondition')  
    # GET
    areas = list(FluidArea.objects.values('id', 'name'))
    ranges = list(FluidRange.objects.values('id', 'name'))
    statuses = list(Status.objects.values('id', 'name'))

    return render(request, 'car/form.html', {
        'current_form': 'fluidlevel',
        'vehicle': vehicle,
        'fluid_areas': FluidArea.objects.all(),
        'fluid_ranges': FluidRange.objects.all(),
        'statuses': Status.objects.all(),
        'fluid_areas_json': json.dumps(areas),
        'fluid_ranges_json': json.dumps(ranges),
        'statuses_json': json.dumps(statuses),
    })



@csrf_exempt
def tyrecondition_view(request):
    vehicle_id = request.session.get('vehicle_id')
    if not vehicle_id:
        return redirect('form_vehicle')

    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == 'POST':
        positions = ['Front Left', 'Front Right', 'Rear Left', 'Rear Right', 'Spare']
        brands = request.POST.getlist('brand')
        conditions = request.POST.getlist('condition')
        dates = request.POST.getlist('manufacturing_date')
        lives = request.POST.getlist('remaining_life_percent')
        custom_conditions = request.POST.getlist('custom_condition')

        for i in range(len(positions)):
            # Get or create the TyrePosition (predefined)
            pos_obj, _ = TyrePosition.objects.get_or_create(name=positions[i])

            # Handle condition (may include custom)
            if conditions[i] == '__custom__' and custom_conditions[i].strip():
                cond_obj, _ = Status.objects.get_or_create(
                    name__iexact=custom_conditions[i].strip(),
                    defaults={'name': custom_conditions[i].strip()}
                )
            else:
                cond_obj = get_object_or_404(Status, id=int(conditions[i]))

            TyreCondition.objects.create(
                vehicle=vehicle,
                position=pos_obj,
                brand=brands[i],
                condition=cond_obj,
                manufacturing_date=dates[i],
                remaining_life_percent=lives[i]
            )

        return redirect('form_paintfinish')

    statuses_qs = list(Status.objects.values('id', 'name'))
    return render(request, 'car/form.html', {
        'current_form': 'tyrecondition',
        'vehicle': vehicle,
        'statuses': Status.objects.all(),
        'statuses_json': escapejs(json.dumps(statuses_qs)),
    })


from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import Vehicle, PaintFinish, PaintArea, Status

@csrf_exempt
def paintfinish_view(request):
    vehicle_id = request.session.get('vehicle_id')
    if not vehicle_id:
        return JsonResponse({
            'success': False,
            'message': 'Vehicle ID not found in session.',
            'redirect': '/carify/form/vehicle/'
        }, status=400)

    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == 'POST':
        areas = request.POST.getlist('area')
        custom_areas = request.POST.getlist('custom_area')
        conditions = request.POST.getlist('condition')
        custom_conditions = request.POST.getlist('custom_condition')
        actions = request.POST.getlist('action')

        repainted_flags = request.POST.getlist('repainted')

        total = min(len(areas), len(conditions), len(actions))

        for i in range(total):
            if i >= len(areas): continue

            area_id = areas[i]
            custom_area = custom_areas[i].strip() if i < len(custom_areas) else ''
            if area_id == '__custom__' and custom_area:
                area_obj, _ = PaintArea.objects.get_or_create(name__iexact=custom_area, defaults={'name': custom_area})
            else:
                try:
                    area_obj = get_object_or_404(PaintArea, id=int(area_id))
                except (ValueError, PaintArea.DoesNotExist):
                    continue

            # Condition
            condition_id = conditions[i]
            custom_condition = custom_conditions[i].strip() if i < len(custom_conditions) else ''
            if condition_id == '__custom__' and custom_condition:
                condition_obj, _ = Status.objects.get_or_create(name__iexact=custom_condition, defaults={'name': custom_condition})
            else:
                try:
                    condition_obj = get_object_or_404(Status, id=int(condition_id))
                except (ValueError, Status.DoesNotExist):
                    continue


            repainted_val = False
            if i < len(repainted_flags):
                    repainted_val = request.POST.get(f'repainted_{i}') == 'on'

            action = actions[i].strip() if i < len(actions) else 'NIL'

            PaintFinish.objects.create(
                vehicle=vehicle,
                area=area_obj,
                repainted=repainted_val,
                condition=condition_obj,
                action=action
            )

        return redirect('form_flushgap')

    # GET request
    paint_areas_qs = PaintArea.objects.all()
    status_qs = Status.objects.all()

    return render(request, 'car/form.html', {
        'current_form': 'paintfinish',
        'vehicle': vehicle,
        'paint_areas': paint_areas_qs,
        'statuses': status_qs,
        'paint_areas_json': json.dumps(list(paint_areas_qs.values('id', 'name'))),
        'statuses_json': json.dumps(list(status_qs.values('id', 'name')))
    })

@csrf_exempt
def flushgap_view(request):
    vehicle_id = request.session.get('vehicle_id')
    if not vehicle_id:
        return redirect('form_vehicle')

    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == 'POST':
        areas = request.POST.getlist('area')
        custom_areas = request.POST.getlist('custom_area')
        operations = request.POST.getlist('operation')
        custom_ops = request.POST.getlist('custom_operation')
        observations = request.POST.getlist('observation')
        actions = request.POST.getlist('action')

        for i in range(len(areas)):
            # Area
            if areas[i] == '__custom__' and custom_areas[i].strip():
                area_obj, _ = FlushArea.objects.get_or_create(name__iexact=custom_areas[i].strip(), defaults={'name': custom_areas[i].strip()})
            else:
                area_obj = get_object_or_404(FlushArea, id=int(areas[i]))

            # Operation
            if operations[i] == '__custom__' and custom_ops[i].strip():
                op_obj, _ = Operations.objects.get_or_create(name__iexact=custom_ops[i].strip(), defaults={'name': custom_ops[i].strip()})
            else:
                op_obj = get_object_or_404(Operations, id=int(operations[i]))

            FlushGap.objects.create(
                vehicle=vehicle,
                area=area_obj,
                operation=op_obj,
                observation_gap=observations[i],
                action=actions[i]
            )

        return redirect('form_rubbercomponent')  

    flush_areas = FlushArea.objects.all()
    operations = Operations.objects.all()

    return render(request, 'car/form.html', {
        'current_form': 'flushgap',
        'vehicle': vehicle,
        'flush_areas': flush_areas,
        'operations': operations,
        'flush_areas_json': json.dumps(list(flush_areas.values('id', 'name'))),
        'operations_json': json.dumps(list(operations.values('id', 'name')))
    })

# views.py
@csrf_exempt
def rubbercomponent_view(request):
    vehicle_id = request.session.get('vehicle_id')
    if not vehicle_id:
        return JsonResponse({
            'success': False,
            'message': 'Vehicle ID not found in session.',
            'redirect': '/carify/form/vehicle/'
        }, status=400)

    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == 'POST':
        areas = request.POST.getlist('area')
        custom_areas = request.POST.getlist('custom_area')
        conditions = request.POST.getlist('condition')
        custom_conditions = request.POST.getlist('custom_condition')
        recommendations = request.POST.getlist('recommendation')

        total = min(len(areas), len(conditions), len(recommendations))

        for i in range(total):
            # Handle Area
            if areas[i] == '__custom__' and custom_areas[i].strip():
                area_obj, _ = RubberArea.objects.get_or_create(
                    name__iexact=custom_areas[i].strip(),
                    defaults={'name': custom_areas[i].strip()}
                )
            else:
                area_obj = get_object_or_404(RubberArea, id=int(areas[i]))

            # Handle Condition
            if conditions[i] == '__custom__' and custom_conditions[i].strip():
                condition_obj, _ = Status.objects.get_or_create(
                    name__iexact=custom_conditions[i].strip(),
                    defaults={'name': custom_conditions[i].strip()}
                )
            else:
                condition_obj = get_object_or_404(Status, id=int(conditions[i]))

            RubberComponent.objects.create(
                vehicle=vehicle,
                area=area_obj,
                condition=condition_obj,
                recommendation=recommendations[i]
            )

        return redirect('form_glasscomponent')

    rubber_areas = RubberArea.objects.all()
    statuses = Status.objects.all()

    return render(request, 'car/form.html', {
        'current_form': 'rubbercomponent',
        'vehicle': vehicle,
        'rubber_areas': rubber_areas,
        'statuses': statuses,
        'rubber_areas_json': json.dumps(list(rubber_areas.values('id', 'name'))),
        'statuses_json': json.dumps(list(statuses.values('id', 'name')))
    })

@csrf_exempt
def glasscomponent_view(request):
    vehicle_id = request.session.get('vehicle_id')
    if not vehicle_id:
        return JsonResponse({
            'success': False,
            'message': 'Vehicle ID not found in session.',
            'redirect': '/carify/form/vehicle/'
        }, status=400)

    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == 'POST':
        areas = request.POST.getlist('area')
        custom_areas = request.POST.getlist('custom_area')
        brands = request.POST.getlist('brand')
        conditions = request.POST.getlist('condition')
        custom_conditions = request.POST.getlist('custom_condition')
        recommendations = request.POST.getlist('recommendation')

        total = len(areas)
        for i in range(total):
            # Area
            if areas[i] == '__custom__' and custom_areas[i].strip():
                area_obj, _ = GlassArea.objects.get_or_create(
                    name__iexact=custom_areas[i].strip(),
                    defaults={'name': custom_areas[i].strip()}
                )
            else:
                area_obj = get_object_or_404(GlassArea, id=int(areas[i]))

            # Condition
            if conditions[i] == '__custom__' and custom_conditions[i].strip():
                condition_obj, _ = Status.objects.get_or_create(
                    name__iexact=custom_conditions[i].strip(),
                    defaults={'name': custom_conditions[i].strip()}
                )
            else:
                condition_obj = get_object_or_404(Status, id=int(conditions[i]))

            GlassComponent.objects.create(
                vehicle=vehicle,
                area=area_obj,
                brand=brands[i],
                condition=condition_obj,
                recommendation=recommendations[i]
            )

        return redirect('form_interiorcomponent')

    glass_areas = GlassArea.objects.all()
    statuses = Status.objects.all()

    return render(request, 'car/form.html', {
        'current_form': 'glasscomponent',
        'vehicle': vehicle,
        'glass_areas': glass_areas,
        'statuses': statuses,
        'glass_areas_json': json.dumps(list(glass_areas.values('id', 'name'))),
        'statuses_json': json.dumps(list(statuses.values('id', 'name')))
    })

@csrf_exempt
def interiorcomponent_view(request):
    vehicle_id = request.session.get('vehicle_id')
    if not vehicle_id:
        return redirect('form_vehicle')

    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == 'POST':
        categories = request.POST.getlist('category')
        custom_categories = request.POST.getlist('custom_category')
        areas = request.POST.getlist('area')
        custom_areas = request.POST.getlist('custom_area')
        conditions = request.POST.getlist('condition')
        custom_conditions = request.POST.getlist('custom_condition')
        recommendations = request.POST.getlist('recommendation')

        for i in range(len(categories)):
            # Category
            if categories[i] == '__custom__' and custom_categories[i].strip():
                category_obj, _ = InteriorCategory.objects.get_or_create(
                    name__iexact=custom_categories[i].strip(),
                    defaults={'name': custom_categories[i].strip()}
                )
            else:
                category_obj = get_object_or_404(InteriorCategory, id=int(categories[i]))

            # Area
            if areas[i] == '__custom__' and custom_areas[i].strip():
                area_obj, _ = InteriorArea.objects.get_or_create(
                    name__iexact=custom_areas[i].strip(),
                    defaults={'name': custom_areas[i].strip()}
                )
            else:
                area_obj = get_object_or_404(InteriorArea, id=int(areas[i]))

            # Condition
            if conditions[i] == '__custom__' and custom_conditions[i].strip():
                condition_obj, _ = Status.objects.get_or_create(
                    name__iexact=custom_conditions[i].strip(),
                    defaults={'name': custom_conditions[i].strip()}
                )
            else:
                condition_obj = get_object_or_404(Status, id=int(conditions[i]))

            # Recommendation
            recommendation = recommendations[i].strip() if i < len(recommendations) else 'NIL'

            # Save
            InteriorComponent.objects.create(
                vehicle=vehicle,
                category=category_obj,
                area=area_obj,
                condition=condition_obj,
                recommendation=recommendation
            )

        return redirect('form_documentation') 
    categories = InteriorCategory.objects.all()
    areas = InteriorArea.objects.all()
    statuses = Status.objects.all()

    return render(request, 'car/form.html', {
        'current_form': 'interiorcomponent',
        'vehicle': vehicle,
        'categories': categories,
        'areas': areas,
        'statuses': statuses,
        'categories_json': json.dumps(list(categories.values('id', 'name'))),
        'areas_json': json.dumps(list(areas.values('id', 'name'))),
        'statuses_json': json.dumps(list(statuses.values('id', 'name')))
    })


@csrf_exempt
def documentation_view(request):
    vehicle_id = request.session.get('vehicle_id')
    if not vehicle_id:
        return redirect('form_vehicle')

    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == 'POST':
        documents = request.POST.getlist('document')
        custom_documents = request.POST.getlist('custom_document')
        statuses = request.POST.getlist('status')
        custom_statuses = request.POST.getlist('custom_status')
        remarks = request.POST.getlist('remark')

        for i in range(len(documents)):
            # Handle document type
            if documents[i] == '__custom__' and custom_documents[i].strip():
                document_obj, _ = DocumentType.objects.get_or_create(
                    name__iexact=custom_documents[i].strip(),
                    defaults={'name': custom_documents[i].strip()}
                )
            else:
                document_obj = get_object_or_404(DocumentType, id=int(documents[i]))

            # Handle status
            if statuses[i] == '__custom__' and custom_statuses[i].strip():
                status_obj, _ = Status.objects.get_or_create(
                    name__iexact=custom_statuses[i].strip(),
                    defaults={'name': custom_statuses[i].strip()}
                )
            else:
                status_obj = get_object_or_404(Status, id=int(statuses[i]))

            Documentation.objects.create(
                vehicle=vehicle,
                document=document_obj,
                status=status_obj,
                remark=remarks[i]
            )

        return redirect('admin_dashboard')  

    document_types = DocumentType.objects.all()
    statuses = Status.objects.all()

    return render(request, 'car/form.html', {
        'current_form': 'documentation',
        'vehicle': vehicle,
        'document_types': document_types,
        'statuses': statuses,
        'document_types_json': json.dumps(list(document_types.values('id', 'name'))),
        'statuses_json': json.dumps(list(statuses.values('id', 'name')))
    })

