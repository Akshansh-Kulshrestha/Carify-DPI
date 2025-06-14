from django.db import models
from User.models import CustomUser

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone=models.CharField(max_length=10)
    email=models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.name} - {self.email} - {self.phone}"
    
class Status(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    

class VehicleFuelType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class VehicleTransmission(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class VehicleEngineType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Vehicle(models.Model):

    image = models.ImageField(upload_to='cars')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    model = models.CharField(max_length=100)
    vin = models.CharField(max_length=50, unique=True)
    fuel_type = models.ForeignKey(VehicleFuelType, on_delete=models.CASCADE)
    transmission = models.ForeignKey(VehicleTransmission, on_delete=models.CASCADE)
    engine_cc = models.IntegerField()
    engine_type = models.ForeignKey(VehicleEngineType, on_delete=models.CASCADE)
    bhp = models.CharField(max_length=20)
    airbags = models.CharField(max_length=1)
    mileage_kmpl = models.FloatField()
    ncap_rating = models.CharField(max_length=20, null=True, blank=True)
    num_keys = models.IntegerField()
    inspection_date = models.DateField()
    inspected_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='inspected_vehicles')
    health_score = models.FloatField()

    def __str__(self):
        return f"{self.model} - {self.model} - {self.vin}"
    
class OBDReading(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    avg_city_running_kms = models.IntegerField()
    pre_delivery_odo_kms = models.IntegerField()
    current_odo_kms = models.IntegerField()
    obd_running_kms = models.IntegerField()
    obd_tampering = models.BooleanField()

class System(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class SystemCheck(models.Model):

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    number_of_issues = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.system}: {self.status} ({self.number_of_issues})"
    
class NetworkArea(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class NetworkSystem(models.Model):

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    area = models.ForeignKey(NetworkArea, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    remark = models.CharField(max_length=200 )

class FluidArea(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    
class FluidRange(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class FluidLevel(models.Model):

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    area = models.ForeignKey(FluidArea, on_delete=models.CASCADE)
    in_range = models.ForeignKey(FluidRange, on_delete=models.CASCADE)
    contamination = models.ForeignKey(Status, on_delete=models.CASCADE)
    recommendation = models.CharField(max_length=100)

class VoltageInference(models.Model):
    ENGINE_STATE_CHOICES = [
    ("Off", "Off"),
    ("On", "On"),
    ("On (idling)", "On (idling)"),
]

    VOLTAGE_CHOICES = [
        ("< 11.8 V", "< 11.8 V"),
        ("11.8 – 12.0 V", "11.8 – 12.0 V"),
        ("12.1 – 12.3 V", "12.1 – 12.3 V"),
        ("12.4 – 12.7 V", "12.4 – 12.7 V"),
        ("> 12.7 V", "> 12.7 V"),
        ("13.7 – 14.7 V", "13.7 – 14.7 V"),
        ("< 13.5 V", "< 13.5 V"),
        ("> 14.8 V", "> 14.8 V"),
    ]

    INFERENCE_CHOICES = [
        ("Severely discharged battery", "Severely discharged battery"),
        ("Low battery charge", "Low battery charge"),
        ("Partially charged battery", "Partially charged battery"),
        ("Normal resting voltage (healthy battery)", "Normal resting voltage (healthy battery)"),
        ("Possibly overcharged or surface charge present", "Possibly overcharged or surface charge present"),
        ("Normal charging voltage from alternator", "Normal charging voltage from alternator"),
        ("Weak alternator or poor charging", "Weak alternator or poor charging"),
        ("Overcharging – regulator or alternator fault possible", "Overcharging – regulator or alternator fault possible"),
    ]

    RECOMMENDATION_CHOICES = [
        ("Recharge or replace battery immediately", "Recharge or replace battery immediately"),
        ("Recharge soon, monitor usage", "Recharge soon, monitor usage"),
        ("May require charging", "May require charging"),
        ("NIL", "NIL"),
        ("Recheck after load applied", "Recheck after load applied"),
        ("Check alternator and connections", "Check alternator and connections"),
        ("Inspect voltage regulator/alternator", "Inspect voltage regulator/alternator"),
    ]

    voltage = models.CharField(max_length=20, choices=VOLTAGE_CHOICES)
    engine_state = models.CharField(max_length=20, choices=ENGINE_STATE_CHOICES)
    interence = models.CharField(max_length=70, choices=INFERENCE_CHOICES)
    recommendation = models.CharField(max_length=100, choices=RECOMMENDATION_CHOICES)

    def __str__(self):
        return f"{self.voltage}, {self.engine_state}, {self.interence}, {self.recommendation}"

class Parameters(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class LiveParameters(models.Model):

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    system = models.ForeignKey(Parameters, on_delete=models.CASCADE)
    interence = models.ForeignKey(VoltageInference, on_delete=models.CASCADE)

class Performance(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name    

class PerformanceCheck(models.Model):

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    system = models.ForeignKey(Performance, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    recommendation = models.CharField(max_length=100)

class PaintArea(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name
    

class PaintFinish(models.Model):

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    area = models.ForeignKey(PaintArea, on_delete=models.CASCADE)
    repainted = models.BooleanField(default=False)

    condition = models.ForeignKey(Status, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)

class TyrePosition(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class TyreCondition(models.Model):
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    position = models.ForeignKey(TyrePosition, on_delete=models.CASCADE)
    brand = models.CharField(max_length=50)
    condition = models.ForeignKey(Status, on_delete=models.CASCADE)
    manufacturing_date = models.DateField()
    remaining_life_percent = models.FloatField()

class FlushArea(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Operations(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name   

class FlushGap(models.Model):

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    area = models.ForeignKey(FlushArea, on_delete=models.CASCADE)
    operation = models.ForeignKey(Operations, on_delete=models.CASCADE)
    observation_gap = models.CharField(max_length=20)
    action = models.CharField(max_length=100)

class RubberArea(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class RubberComponent(models.Model):

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    area = models.ForeignKey(RubberArea, on_delete=models.CASCADE)
    condition = models.ForeignKey(Status, on_delete=models.CASCADE)
    recommendation = models.CharField(max_length=100)

class GlassArea(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class GlassComponent(models.Model):

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    area = models.ForeignKey(GlassArea, on_delete=models.CASCADE)
    brand = models.CharField(max_length=50)
    condition = models.ForeignKey(Status, on_delete=models.CASCADE)
    recommendation = models.CharField(max_length=100)

class InteriorArea(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class InteriorCategory(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class InteriorComponent(models.Model):

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    category = models.ForeignKey(InteriorCategory, on_delete=models.CASCADE)
    area = models.ForeignKey(InteriorArea, on_delete=models.CASCADE)
    condition = models.ForeignKey(Status, on_delete=models.CASCADE)
    recommendation = models.CharField(max_length=100)

class DocumentType(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Documentation(models.Model):
   
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    document = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    remark = models.CharField(max_length=200)
