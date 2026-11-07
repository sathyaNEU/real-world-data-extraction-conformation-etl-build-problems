"""Fixed parameters of the task185 world (architecture 2): Kessler Valley Power Company's 2025 distribution
circuits, AMI voltage events, PV interconnections, voltage complaints and interconnection applications, as the
Tamarack Utility Commission's staff receives them for the 2027 Feeder Voltage Program audit."""
import datetime as dt

SEED = 185_2027
YEAR = 2025
EXPORT_DATE = dt.datetime(2026, 2, 13, 9, 30, 0)
AS_OF = dt.date(2026, 3, 20)          # the fiction's latest date (the order's date)

COMPANY = "Kessler Valley Power Company"
COMMISSION = "Tamarack Utility Commission"
DOCKET = "E-26-0412"

# Range A upper limit (120-volt base) and the head-end's alarm settings
RANGE_A_HIGH = 126.0
RANGE_A_LOW = 114.0
ALARM_HIGH = 126.5
ALARM_LOW = 113.5
PROGRAM_CIRCUITS = 5

# Service conductor resistance, ohms per 1,000 ft of each conductor at 75 C (aluminium triplex and quadruplex)
CONDUCTORS = {
    # code in the GIS register: (code in DCS-410, description, ohms per 1000 ft, ampacity A)
    "TPX-2AL": ("2-2-4 TX", "#2 AL triplex service drop", 0.2650, 135),
    "TPX-1/0AL": ("1/0-1/0-2 TX", "1/0 AL triplex service drop", 0.1670, 180),
    "TPX-4/0AL": ("4/0-4/0-2/0 TX", "4/0 AL triplex service drop", 0.0838, 260),
    "URD-4/0AL": ("4/0-4/0-2/0 UD", "4/0 AL underground triplex", 0.0838, 245),
    "URD-350AL": ("350-350-4/0 UD", "350 kcmil AL underground triplex", 0.0479, 330),
}

# File names (as the source systems name their exports)
F_EVENTS = "ami_voltage_events_2025.csv"
F_METERS = "meter_register_20251231.csv"
F_PV = "pv_interconnection_register_20251231.xlsx"
F_CIRCUITS = "distribution_circuits_2025.xlsx"
F_APPS = "interconnection_application_log_2025.csv"
F_CONTACTS = "crm_voltage_contacts_2025.csv"
F_ORDERS = "wms_field_orders_2025.csv"
F_CAPS = "capacitor_bank_status_2025.csv"
F_LTC = "substation_ltc_settings_2025.xlsx"
F_ORDER = "TUC_order_E-26-0412_feeder_voltage_program.pdf"
F_TARIFF = "KVPC_interconnection_tariff_sections_5_9.docx"
F_DCS = "KVPC_DCS-410_secondary_service_conductors.pdf"
F_SQP = "KVPC_service_quality_plan_2025_excerpt.docx"

DELIVERABLES = ["feeder_voltage_audit_2027.xlsx", "feeder_voltage_audit_2027.pptx"]

# State holidays observed by the company in 2025 (tariff Appendix B)
HOLIDAYS_2025 = [
    dt.date(2025, 1, 1), dt.date(2025, 1, 20), dt.date(2025, 2, 17), dt.date(2025, 5, 26), dt.date(2025, 6, 19),
    dt.date(2025, 7, 4), dt.date(2025, 9, 1), dt.date(2025, 10, 13), dt.date(2025, 11, 11), dt.date(2025, 11, 27),
    dt.date(2025, 11, 28), dt.date(2025, 12, 24), dt.date(2025, 12, 25), dt.date(2025, 12, 31),
]
HOLIDAYS_2026 = [dt.date(2026, 1, 1), dt.date(2026, 1, 19), dt.date(2026, 2, 16)]

COMPLAINT_STANDARD_DAYS = 10
REVIEW_STANDARD_DAYS = 15

PEOPLE = {
    "staff": "Lisa Kent",
    "planning": "Rachel Ballard",
    "customer": "Edward Evans",
}
