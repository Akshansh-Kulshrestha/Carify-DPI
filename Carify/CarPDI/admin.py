from django.contrib import admin
from .models import (
    Customer, Vehicle, OBDReading, SystemCheck, NetworkSystem, FluidLevel,
    PerformanceCheck, PaintFinish, TyreCondition, FlushGap, RubberComponent,
    GlassComponent, InteriorComponent, Documentation
)

# Inline models for Vehicle
class OBDReadingInline(admin.StackedInline):
    model = OBDReading
    extra = 0
    max_num = 1

class SystemCheckInline(admin.TabularInline):
    model = SystemCheck
    extra = 1

class NetworkSystemInline(admin.TabularInline):
    model = NetworkSystem
    extra = 1

class FluidLevelInline(admin.TabularInline):
    model = FluidLevel
    extra = 1

class PerformanceCheckInline(admin.TabularInline):
    model = PerformanceCheck
    extra = 1

class PaintFinishInline(admin.TabularInline):
    model = PaintFinish
    extra = 1

class TyreConditionInline(admin.TabularInline):
    model = TyreCondition
    extra = 1

class FlushGapInline(admin.TabularInline):
    model = FlushGap
    extra = 1

class RubberComponentInline(admin.TabularInline):
    model = RubberComponent
    extra = 1

class GlassComponentInline(admin.TabularInline):
    model = GlassComponent
    extra = 1

class InteriorComponentInline(admin.TabularInline):
    model = InteriorComponent
    extra = 1

class DocumentationInline(admin.TabularInline):
    model = Documentation
    extra = 1

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'model', 'variant', 'vin', 'inspection_date', 'health_score')
    search_fields = ('vin', 'model')
    list_filter = ('fuel_type', 'transmission')
    inlines = [
        OBDReadingInline,
        SystemCheckInline,
        NetworkSystemInline,
        FluidLevelInline,
        PerformanceCheckInline,
        PaintFinishInline,
        TyreConditionInline,
        FlushGapInline,
        RubberComponentInline,
        GlassComponentInline,
        InteriorComponentInline,
        DocumentationInline,
    ]

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
