from django import forms
from .models import (
    Customer, Vehicle, OBDReading, SystemCheck, NetworkSystem, FluidLevel,
    PerformanceCheck, PaintFinish, TyreCondition, FlushGap, RubberComponent,
    GlassComponent, InteriorComponent, Documentation
)

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone']



class VehicleForm(forms.ModelForm):


    class Meta:
        model = Vehicle
        fields = ['customer', 'image','maker', 'model', 'variant', 'vin', 'fuel_type',
            'transmission', 'engine_cc', 'engine_type', 'bhp', 'airbags',
            'mileage_kmpl', 'ncap_rating', 'num_keys', 'inspection_date',
            'inspected_by', 'health_score']

class OBDReadingForm(forms.ModelForm):


    class Meta:
        model = OBDReading
        fields = [
            'vehicle', 'avg_city_running_kms', 'pre_delivery_odo_kms',
            'current_odo_kms', 'obd_running_kms', 'obd_tampering'
        ]

class SystemCheckForm(forms.ModelForm):
    class Meta:
        model = SystemCheck
        fields = ['vehicle', 'name', 'status', 'issues']

class NetworkSystemForm(forms.ModelForm):
    class Meta:
        model = NetworkSystem
        fields = ['vehicle', 'area', 'remark']

class FluidLevelForm(forms.ModelForm):
    class Meta:
        model = FluidLevel
        fields = ['vehicle', 'name', 'in_range', 'contamination', 'recommendation']

class PerformanceCheckForm(forms.ModelForm):
    class Meta:
        model = PerformanceCheck
        fields = ['vehicle', 'system', 'status', 'recommendation']

class PaintFinishForm(forms.ModelForm):
    class Meta:
        model = PaintFinish
        fields = ['vehicle', 'area', 'repainted', 'condition', 'action']

class TyreConditionForm(forms.ModelForm):
    class Meta:
        model = TyreCondition
        fields = ['vehicle', 'position', 'brand', 'condition', 'manufacturing_date', 'remaining_life_percent']

class FlushGapForm(forms.ModelForm):
    class Meta:
        model = FlushGap
        fields = ['vehicle', 'area', 'operation', 'observation_gap', 'action']

class RubberComponentForm(forms.ModelForm):
    class Meta:
        model = RubberComponent
        fields = ['vehicle', 'area', 'condition', 'recommendation']

class GlassComponentForm(forms.ModelForm):
    class Meta:
        model = GlassComponent
        fields = ['vehicle', 'area', 'brand', 'condition', 'recommendation']

class InteriorComponentForm(forms.ModelForm):
    class Meta:
        model = InteriorComponent
        fields = ['vehicle', 'category', 'area', 'condition', 'recommendation']

class DocumentationForm(forms.ModelForm):
    class Meta:
        model = Documentation
        fields = ['vehicle', 'document', 'status', 'remark']