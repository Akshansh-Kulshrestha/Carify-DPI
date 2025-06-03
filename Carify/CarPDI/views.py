from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound
from .forms import (
    CustomerForm, VehicleForm, OBDReadingForm, SystemCheckForm, NetworkSystemForm,
    FluidLevelForm, PerformanceCheckForm, PaintFinishForm, TyreConditionForm,
    FlushGapForm, RubberComponentForm, GlassComponentForm, InteriorComponentForm,
    DocumentationForm
)
from .models import *

FORM_CLASSES = {
    'customer': CustomerForm,
    'vehicle': VehicleForm,
    'obdreading': OBDReadingForm,
    'systemcheck': SystemCheckForm,
    'networksystem': NetworkSystemForm,
    'fluidlevel': FluidLevelForm,
    'performancecheck': PerformanceCheckForm,
    'paintfinish': PaintFinishForm,
    'tyrecondition': TyreConditionForm,
    'flushgap': FlushGapForm,
    'rubbercomponent': RubberComponentForm,
    'glasscomponent': GlassComponentForm,
    'interiorcomponent': InteriorComponentForm,
    'documentation': DocumentationForm,
}

def unified_form_view(request, form_name):
    form_keys = list(FORM_CLASSES.keys())



    all_forms = {}

    # Populate forms: bind all if submit_all, else just current one
    if request.method == 'POST' and 'submit_all' in request.POST:
        for key in form_keys:
            all_forms[key] = FORM_CLASSES[key](request.POST, request.FILES, prefix=key)
    else:
        for key in form_keys:
            if request.method == 'POST' and key == form_name:
                all_forms[key] = FORM_CLASSES[key](request.POST, request.FILES, prefix=key)
            else:
                all_forms[key] = FORM_CLASSES[key](prefix=key)

    if request.method == 'POST':
        if "submit_all" in request.POST:
            if all(form.is_valid() for form in all_forms.values()):
                for form in all_forms.values():
                    form.save()
                return redirect('success')

        elif "navigate_previous" in request.POST:
            current = request.POST.get("navigate_previous")
            if current in form_keys:
                idx = form_keys.index(current)
                previous_form = form_keys[idx - 1] if idx > 0 else current
                return redirect('unified_form', form_name=previous_form)

        elif "save_section" in request.POST:
            active = request.POST.get("save_section")
            if active in form_keys:
                current_form = all_forms[active]
                if current_form.is_valid():
                    current_form.save()
                    idx = form_keys.index(active)
                    if idx + 1 < len(form_keys):
                        # Continue to next form
                        return redirect('unified_form', form_name=form_keys[idx + 1])
                    else:
                        # ✅ This is the last form — go to success
                        return redirect('success')

    index = form_keys.index(form_name)
    current = form_keys[index]
    previous = form_keys[index - 1] if index > 0 else None
    next_form = form_keys[index + 1] if index + 1 < len(form_keys) else None

    return render(request, 'car/unified_form.html', {
        'current_form': current,
        'form_names': form_keys,
        'previous_form': previous,
        'next_form': next_form,
        'all_forms': all_forms
    })


def success_view(request):
    return render(request, 'car/success.html')
