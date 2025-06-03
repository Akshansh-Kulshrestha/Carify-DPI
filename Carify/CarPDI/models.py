from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=100)
    phone=models.CharField(max_length=10)
    email=models.EmailField(max_length=254)

    def __str__(self):
        return f"{self.name} - {self.email} - {self.phone}"

class Vehicle(models.Model):

    MAKER_CHOICES = [
    ('maruti_suzuki', 'Maruti Suzuki'),
    ('hyundai', 'Hyundai'),
    ('tata', 'Tata Motors'),
    ('mahindra', 'Mahindra'),
    ('honda', 'Honda'),
    ('toyota', 'Toyota'),
    ('kia', 'Kia'),
    ('skoda', 'Skoda'),
    ('volkswagen', 'Volkswagen'),
    ('renault', 'Renault'),
    ('mg', 'MG Motor'),
    ('nissan', 'Nissan'),
    ('jeep', 'Jeep'),
    ('bmw', 'BMW'),
    ('audi', 'Audi'),
    ('mercedes', 'Mercedes-Benz'),
    ('others', 'Others'),
]

    FUEL_TYPE_CHOICES = [
    ('petrol', 'Petrol'),
    ('diesel', 'Diesel'),
    ('cng', 'CNG'),
    ('electric', 'Electric'),
    ('hybrid', 'Hybrid'),
]   
    TRANSMISSION_CHOICES = [
    ('manual', 'Manual'),
    ('automatic', 'Automatic'),
    ('amt', 'AMT'),              
    ('cvt', 'CVT'),              
    ('dct', 'DCT'),              
]
    ENGINE_TYPE_CHOICES = [
    ('petrol', 'Petrol'),
    ('diesel', 'Diesel'),
    ('cng', 'CNG'),
    ('electric', 'Electric'),
    ('hybrid', 'Hybrid'),
    ('mild_hybrid', 'Mild Hybrid'),
    ('turbo_petrol', 'Turbo Petrol'),
    ('turbo_diesel', 'Turbo Diesel'),
]

    image = models.ImageField(upload_to='cars')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    maker = models.CharField(max_length=100, choices=MAKER_CHOICES)
    model = models.CharField(max_length=100)
    variant = models.CharField(max_length=100)
    vin = models.CharField(max_length=50, unique=True)
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    engine_cc = models.IntegerField()
    engine_type = models.CharField(max_length=100, choices=ENGINE_TYPE_CHOICES)
    bhp = models.CharField(max_length=20)
    airbags = models.CharField(max_length=1)
    mileage_kmpl = models.FloatField()
    ncap_rating = models.CharField(max_length=20, null=True, blank=True)
    num_keys = models.IntegerField()
    inspection_date = models.DateField()
    inspected_by = models.CharField(max_length=100)
    health_score = models.FloatField()

    def __str__(self):
        return f"{self.maker} - {self.model} - {self.variant}"
    
class OBDReading(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    avg_city_running_kms = models.IntegerField()
    pre_delivery_odo_kms = models.IntegerField()
    current_odo_kms = models.IntegerField()
    obd_running_kms = models.IntegerField()
    obd_tampering = models.BooleanField()

class SystemCheck(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default="All OK")
    issues = models.IntegerField(default=0)

class NetworkSystem(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    area = models.CharField(max_length=100)
    remark = models.CharField(max_length=200)

class FluidLevel(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    in_range = models.BooleanField()
    contamination = models.CharField(max_length=20)
    recommendation = models.CharField(max_length=100)

class PerformanceCheck(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    system = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    recommendation = models.CharField(max_length=100)

class PaintFinish(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    area = models.CharField(max_length=100)
    repainted = models.BooleanField()
    condition = models.CharField(max_length=50)
    action = models.CharField(max_length=100)

class TyreCondition(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    position = models.CharField(max_length=50)
    brand = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    manufacturing_date = models.CharField(max_length=20)
    remaining_life_percent = models.FloatField()

class FlushGap(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    area = models.CharField(max_length=100)
    operation = models.CharField(max_length=50)
    observation_gap = models.CharField(max_length=50)
    action = models.CharField(max_length=100)

class RubberComponent(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    area = models.CharField(max_length=100)
    condition = models.CharField(max_length=50)
    recommendation = models.CharField(max_length=100)

class GlassComponent(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    area = models.CharField(max_length=100)
    brand = models.CharField(max_length=50)
    condition = models.CharField(max_length=50)
    recommendation = models.CharField(max_length=100)

class InteriorComponent(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, choices=[('Floor', 'Floor'), ('Plastic', 'Plastic'), ('Fabric', 'Fabric')])
    area = models.CharField(max_length=100)
    condition = models.CharField(max_length=50)
    recommendation = models.CharField(max_length=100)

class Documentation(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    document = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    remark = models.CharField(max_length=200)
