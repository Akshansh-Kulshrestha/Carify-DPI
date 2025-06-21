# Carify-DPI

    MAKER_CHOICES = [
    ('Suzuki', 'Suzuki'),
    ('Hyundai', 'Hyundai'),
    ('Tata', 'Tata Motors'),
    ('Mahindra', 'Mahindra'),
    ('Honda', 'Honda'),
    ('Toyota', 'Toyota'),
    ('Kia', 'Kia'),
    ('Skoda', 'Skoda'),
    ('Volkswagen', 'Volkswagen'),
    ('Renault', 'Renault'),
    ('MG', 'MG Motor'),
    ('Nissan', 'Nissan'),
    ('Jeep', 'Jeep'),
    ('BMW', 'BMW'),
    ('Audi', 'Audi'),
    ('Mercedes', 'Mercedes-Benz'),
    ('Others', 'Others'),
]

    FUEL_TYPE_CHOICES = [
    ('Petrol', 'Petrol'),
    ('Diesel', 'Diesel'),
    ('CNG', 'CNG'),
    ('Electric', 'Electric'),
    ('Hybrid', 'Hybrid'),
]   
    TRANSMISSION_CHOICES = [
    ('Manual', 'Manual'),
    ('Automatic', 'Automatic'),
    ('AMT', 'AMT'),              
    ('CVT', 'CVT'),              
    ('DCT', 'DCT'),              
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

    SYSTEM_CHOICES = [
        ('Motor', 'Motor'),
        ('Brakes', 'Brakes'),
        ('AC & Heating', 'AC & Heating'),
        ('Clutch & Transmission', 'Clutch & Transmission'),
        ('Steering & Suspension', 'Steering & Suspension'),
        ('Fuel Systems', 'Fuel Systems'),
        ('Battery', 'Battery'),
        ('Exhaust System', 'Exhaust System'),
        ('Filters', 'Filters'),
        ('Ignition', 'Ignition'),
        ('Light', 'Light'),
        ('Sensors', 'Sensors'),
    ]

    NETWORK_AREA_CHOICES = [
        ('Network electrical', 'Network electrical'),
        ('Network communications', 'Network communications'),
        ('Network software', 'Network software'),
        ('Network data', 'Network data'),
        ('Body sytems', 'Body sytems'),
        ('Brakes and Traction control', 'Brakes and Traction control'),
        ('Fuel and air metering and auxiliary emission control', 'Fuel and air metering and auxiliary emission control'),
        ('Fuel and air metering', 'Fuel and air metering'),
        ('Fuel and air metering injector circuit', 'Fuel and air metering injector circuit'),
        ('Ignition system or misfire', 'Ignition system or misfire'),
        ('Emission control', 'Emission control'),
        ('Vehicle or idle speed control', 'Vehicle or idle speed control'),
        ('ECM computer output circuit', 'ECM computer output circuit'),
        ('Transmission', 'Transmission'),
        ('Cylinder deactivation', 'Cylinder deactivation'),
    ]

    FLUID_CHOICES = [
        ('Engine Oil', 'Engine Oil'),
        ('Coolant', 'Coolant'),
        ('Brake Oil', 'Brake Oil'),
        ('Washer Fluid', 'Washer Fluid'),
        ('Auxillary Belts', 'Auxillary Belts'),
        ('Leakages', 'Leakages'),
    ]
    RANGE_CHOICES = [
        ('In Range', 'In Range'),
        ('Not In Range', 'Not In Range'),
        ('Ok', 'Ok'),
        ('Not Ok', 'Not Ok'),
        ('No Leakage Detected', 'No Leakage Detected'),
        ('Leakage Detected', 'Leakage Detected'),
    ]

    PARAMENTERS_CHOICES = [
        ('Battery Voltage', 'Battery Voltage'),
        ('Charging Voltage', 'Charging Voltage'),
        ('Ignition Voltage', 'Ignition Voltage'),
    ]

    PERFORMANCE_CHOICES = [
        ('Instrument Cluster', 'Instrument Cluster'),
        ('Vibrations , Noise & Odour', 'Vibrations , Noise & Odour'),
        ('Excessive Smoke from exhaust', 'Excessive Smoke from exhaust'),
        ('Gear Shifting', 'Gear Shifting'),
        ('Pedal Play', 'Pedal Play'),
        ('Steering Responsiveness', 'Steering Responsiveness'),
        ('Parking Brake', 'Parking Brake'),
        ('Reverse Gear & Sensor', 'Reverse Gear & Sensor'),
        ('Speedometer', 'Speedometer'),
    ]

    PAINT_FINISH_CHOICES = [
        ('Bonnet', 'Bonnet'),
        ('Boot', 'Boot'),
        ('Front right door', 'Front right door'),
        ('Front left door', 'Front left door'),
        ('Rear right door', 'Rear right door'),
        ('Rear left door', 'Rear left door'),
        ('Roof', 'Roof'),
        ('Front right quarter panel', 'Front right quarter panel'),
        ('Front left quarter panel', 'Front left quarter panel'),
        ('Rear right quarter panel', 'Rear right quarter panel'),
        ('Rear left quarter panel', 'Rear left quarter panel'),
        ('Front Bumper', 'Front Bumper'),
        ('Rear Bumper', 'Rear Bumper'),
        ('Fuel filler cap', 'Fuel filler cap'),
    ]

    POSITION_CHOICES=[
        ('Front Left', 'Front Left'),
        ('Front Right', 'Front Right'),
        ('Rear Left', 'Rear Left'),
        ('Rear Right', 'Rear Right'),
        ('Spear', 'Spear'),
    ]

    FLUSH_CHOICES = [
        ('Bonnet Right', 'Bonnet Right'),
        ('Bonnet Left', 'Bonnet Left'),
        ('Front Right Door', 'Front Right Door'),
        ('Front Left Door', 'Front Left Door'),
        ('Rear Right Door', 'Rear Right Door'),
        ('Rear Left Door', 'Rear Left Door'),
        ('Boot right', 'Boot right'),
        ('Boot left', 'Boot left'),
    ]
    OPERATION_CHOICES = [
        ('Smooth', 'Smooth'),
        ('Hard', 'Hard'),
        ('Loose','Loose'),
        ('Noisy', 'Noisy'),
        ('Does not operate', 'Does not operate'),
        ('Misaligned', 'Misaligned'),
        ('Uneven Movement', 'Uneven Movement'),
        ('Rattling', 'Rattling'),

    ]

    RUBBER_CHOICES = [
        ('Beading: Front left door', 'Beading: Front left door'),
        ('Beading: Front right door', 'Beading: Front right door'),
        ('Beading: Rear left door', 'Beading: Rear left door'),
        ('Beading: Rear right door', 'Beading: Rear right door'),
        ('Beading: Boot', 'Beading: Boot'),
        ('Wiper: Front left', 'Wiper: Front left'),
        ('Wiper: Front right', 'Wiper: Front right'),
        ('Wiper: Rear', 'Wiper: Rear'),
        ('Front Under Bonnet', 'Front Under Bonnet'),
    ]

    GLASS_CHOICES = [
        ('Front Windscreen', 'Front Windscreen'),
        ('Rear WindScreen', 'Rear WindScreen'),
        ('Front right Window', 'Front right Window'),
        ('Front left Window', 'Front left Window'),
        ('Rear left Window', 'Rear left Window'),
        ('Rear right Window', 'Rear right Window'),
        ('ORVM - Left Mirror', 'ORVM - Left Mirror'),
        ('ORVM - Right Mirror', 'ORVM - Right Mirror'),
        ('Sunroof', 'Sunroof'),
    ]

    INTERIOR_CHOICES = [
        ('Driver Side', 'Driver Side'),
        ('Co-Driver Side', 'Co-Driver Side'),
        ('Driver Rear', 'Driver Rear'),
        ('Co-Driver Rear', 'Co-Driver Rear'),
        ('Boot', 'Boot'),
        ('Dashboard', 'Dashboard'),
        ('Gear Console', 'Gear Console'),
        ('Driver Seat Headrest', 'Driver Seat Headrest'),
        ('Co Driver Seat', 'Co Driver Seat'),
        ('Driver Seat', 'Driver Seat'),
        ('Co-Driver Headrest', 'Co-Driver Headrest'),
        ('Rear Seat', 'Rear Seat'),
        ('Rear Seat Headrest', 'Rear Seat Headrest'),
    ]
    CATEGORY_CHOICES=[
        ('Floor', 'Floor'),
                       ('Plastic', 'Plastic'), 
                       ('Fabric', 'Fabric'),
                       ]

    DOCUMENTATION_CHOICES = [('Invoice/ Challan', 'Invoice/ Challan'),
                             ('All payment receipts', 'All payment receipts'),
                             ('Owner Manual', 'Owner Manual'),
                             ('Duplicate Keys', 'Duplicate Keys'),
                             ]

# Voltage Inference
import pandas as pd
from CarPDI.models import VoltageInference  
df = pd.read_csv(
    'C:/Users/Akshansh/OneDrive/Desktop/Sudo Technolab/Carify/Carify/voltage_interence.csv',
    encoding='ISO-8859-1'
)
records = [
    VoltageInference(
        voltage=row['Voltage (V)'],
        engine_state=row['Engine State'],
        interence=row['Inference'],
        recommendation=row['Recommendation']
    )
    for _, row in df.iterrows()
]
VoltageInference.objects.bulk_create(records)

# System Model
import pandas as pd
from CarPDI.models import System
df = pd.read_csv('C:/Users/Akshansh/OneDrive/Desktop/Sudo Technolab/Carify/Carify/system_check.csv')
df = df.dropna(subset=['name'])
df = df.drop_duplicates(subset=['name'])
records = [System(name=row['name']) for _, row in df.iterrows()]
System.objects.bulk_create(records, ignore_conflicts=True)  # Avoid duplicate entry errors
print(f"{len(records)} systems inserted successfully.")
