# myapp/scripts/populate_voltage_data.py

from CarPDI.models import VoltageInference

def run():
    data = [
        ("< 11.8 V", "Off", "Severely discharged battery", "Recharge or replace battery immediately"),
        ("11.8 – 12.0 V", "Off", "Low battery charge", "Recharge soon, monitor usage"),
        ("12.1 – 12.3 V", "Off", "Partially charged battery", "May require charging"),
        ("12.4 – 12.7 V", "Off", "Normal resting voltage (healthy battery)", "NIL"),
        ("> 12.7 V", "Off", "Possibly overcharged or surface charge present", "Recheck after load applied"),
        ("13.7 – 14.7 V", "On (idling)", "Normal charging voltage from alternator", "NIL"),
        ("< 13.5 V", "On", "Weak alternator or poor charging", "Check alternator and connections"),
        ("> 14.8 V", "On", "Overcharging – regulator or alternator fault possible", "Inspect voltage regulator/alternator"),
    ]

    for voltage, engine_state, interence, recommendation in data:
        VoltageInference.objects.get_or_create(
            voltage=voltage,
            engine_state=engine_state,
            interence=interence,
            recommendation=recommendation
        )
