"""Tamralipta Data Services, Kolkata: clients, streams, forms, contracts, calendars and the workforce.

Every constant the pack is built from lives here. Limits are not here: tune.py sets them from the closed
quarter's measured residuals so the ladder's ratios hold, and the quality schedules print what it sets."""
import datetime as dt

SEED = 230
ORG = "Tamralipta Data Services Pvt Ltd"
CENTRE = "Tamralipta Data Services, Salt Lake Sector V capture centre"
ASOF = dt.date(2026, 10, 28)
Q3 = (dt.date(2026, 7, 1), dt.date(2026, 9, 30))
NOV = (dt.date(2026, 11, 1), dt.date(2026, 11, 30))

PEOPLE = {"ops": "Dipta Mukhopadhyay", "mis": "Raghav Bajwa", "quality": "Vasana Reddy"}

# shift windows in IST: the day queue serves Australian and UK clients, the night queue US clients
SHIFT = {"D": (8, 0, 17, 0), "N": (20, 30, 5, 30)}

CLIENTS = {
    "KBA": dict(name="Kessington Benefit Administrators", region="US", ccy="USD", tz="America/New_York", tzlabel="US Eastern"),
    "NDS": dict(name="Northgate Dental Services", region="US", ccy="USD", tz="America/Chicago", tzlabel="US Central"),
    "BMC": dict(name="Brightmoor Comp", region="US", ccy="USD", tz="America/Detroit", tzlabel="US Eastern"),
    "HPB": dict(name="Harbison Pharmacy Benefits", region="US", ccy="USD", tz="America/Chicago", tzlabel="US Central"),
    "WBH": dict(name="Wattlebird Health", region="AU", ccy="AUD", tz="Australia/Brisbane", tzlabel="AEST (Brisbane)"),
    "CIP": dict(name="Coolabah Income Protection", region="AU", ccy="AUD", tz="Australia/Sydney", tzlabel="Sydney"),
    "WPC": dict(name="Whinfell Pet Cover", region="UK", ccy="GBP", tz="Europe/London", tzlabel="UK"),
    "TCM": dict(name="Thistlecombe Motor", region="UK", ccy="GBP", tz="Europe/London", tzlabel="UK"),
    "HPY": dict(name="Hollings & Pryce", region="UK", ccy="GBP", tz="Europe/London", tzlabel="UK"),
}

# code: client, stream id, label, family, Q3 queue, Nov queue, weekday key fields (Q3 mean), OCR error rate
STREAMS = {
    "N1": dict(client="KBA", sid="KBA-INST", label="Kessington, institutional claims (UB-04)", family="printed", q3="N", nov="N", kf=26000, p=0.0140),
    "N2": dict(client="KBA", sid="KBA-PROF", label="Kessington, professional claims (CMS-1500)", family="mixed", q3="N", nov="N", kf=14000, p=0.0320),
    "N3": dict(client="NDS", sid="NDS-DENT", label="Northgate, dental claims (ADA J430D)", family="handwritten", q3="N", nov="N", kf=8000, p=0.0420),
    "N4": dict(client="BMC", sid="BMC-FROI", label="Brightmoor Comp, workers' compensation first reports", family="handwritten", q3="N", nov="N", kf=4000, p=0.0560),
    "N5": dict(client="HPB", sid="HPB-UCF", label="Harbison, pharmacy claim forms (UCF)", family="printed", q3="N", nov="N", kf=10000, p=0.0170),
    "D1": dict(client="WBH", sid="WBH-HOSP", label="Wattlebird, hospital claims", family="printed", q3="D", nov="D", kf=40000, p=0.0150),
    "D2": dict(client="WBH", sid="WBH-EXTR", label="Wattlebird, extras claims", family="mixed", q3="D", nov="D", kf=30000, p=0.0290),
    "D3": dict(client="CIP", sid="CIP-IPCL", label="Coolabah, income protection claims", family="handwritten", q3="D", nov="D", kf=14000, p=0.0400),
    "D4": dict(client="WPC", sid="WPC-PETC", label="Whinfell, pet claims", family="mixed", q3="D", nov="D", kf=24000, p=0.0310),
    "D5": dict(client="TCM", sid="TCM-FNOL", label="Thistlecombe, motor claims (first notification)", family="handwritten", q3="D", nov="N", kf=36500, p=0.0950),
    "D6": dict(client="HPY", sid="HPY-TYPD", label="Hollings & Pryce, typed claims", family="typed", q3=None, nov="D", kf=60000, p=0.0060),
}
ORDER = list(STREAMS)
SID = {k: v["sid"] for k, v in STREAMS.items()}
CODE_OF = {v["sid"]: k for k, v in STREAMS.items()}

# Saturday and holiday key fields (Q3): Australian paper only on day Saturdays, Brightmoor and Northgate on night Saturdays
SAT_KF = {"D1": 32000, "D2": 3000, "D3": 600, "N3": 1200, "N4": 5000}
US_HOLIDAYS_Q3 = [dt.date(2026, 7, 3), dt.date(2026, 9, 7)]
UK_HOLIDAYS_Q3 = [dt.date(2026, 8, 31)]
US_HOLIDAYS_NOV = [dt.date(2026, 11, 26)]
Q3_SCALE = {"D5": 1.10}  # the motor claims ran a little above their contract forecast through the quarter
PILOT = (dt.date(2026, 8, 17), dt.date(2026, 9, 26))
PILOT_KF = 2000
PILOT_AUDIT_SHARE = 1.00
AUDIT_SHARE = {"N": 0.30, "D": 0.10}


def audit_share(code):
    if code == "D6":
        return PILOT_AUDIT_SHARE
    return AUDIT_SHARE[STREAMS[code]["q3"]]

# weekday profiles (Mon..Fri), by region; UK motor is Monday heavy after weekend accidents
PROFILE = {"US": [1.10, 1.04, 1.00, 0.96, 0.90], "AU": [1.04, 1.02, 1.00, 0.98, 0.96],
           "UK": [1.06, 1.02, 1.00, 0.97, 0.95], "TCM": [1.30, 1.06, 0.94, 0.88, 0.82]}

# stream-specific weekday profiles, daily volume spread and Kessington's month-end cycle billing
PROFILE.update({"N4": [0.92, 0.96, 1.00, 1.04, 1.12], "N5": [1.28, 1.04, 0.95, 0.90, 0.86], "N3": [0.95, 1.00, 1.02, 1.03, 1.00]})
DAILY_SD = {"D5": 0.30, "N1": 0.28, "N2": 0.24, "N3": 0.26, "N4": 0.28, "N5": 0.26}
CYCLE = {"N1": 1.75}

FIELD_TYPES = {"ID": (1.00, 0.00), "DATE": (0.80, -0.15), "CODE": (1.20, 0.10), "AMOUNT": (0.90, -0.20), "TEXT": (1.30, 0.20)}

# form specifications: field lists by stream and version (field name, type); versions with effective dates
_F = {
    "N1": [("patient_control_no", "ID"), ("type_of_bill", "CODE"), ("statement_from", "DATE"), ("statement_through", "DATE"),
           ("admission_date", "DATE"), ("member_id", "ID"), ("patient_dob", "DATE"), ("revenue_code", "CODE"),
           ("hcpcs_rate", "CODE"), ("total_charges", "AMOUNT"), ("attending_npi", "ID"), ("principal_dx", "CODE"),
           ("billing_npi", "ID"), ("payer_name", "TEXT")],
    "N2": [("insured_id", "ID"), ("patient_dob", "DATE"), ("dos_from", "DATE"), ("place_of_service", "CODE"),
           ("cpt_hcpcs", "CODE"), ("modifier", "CODE"), ("dx_pointer", "CODE"), ("line_charges", "AMOUNT"),
           ("units", "AMOUNT"), ("rendering_npi", "ID"), ("icd10_dx", "CODE")],
    "N3": [("subscriber_id", "ID"), ("patient_dob", "DATE"), ("procedure_date", "DATE"), ("cdt_code", "CODE"),
           ("tooth_number", "CODE"), ("tooth_surface", "CODE"), ("fee", "AMOUNT"), ("billing_npi", "ID"),
           ("billing_tin", "ID"), ("oral_cavity_area", "CODE"), ("group_number", "ID"), ("subscriber_name", "TEXT")],
    "N4": [("claim_admin_no", "ID"), ("date_of_injury", "DATE"), ("employer_fein", "ID"), ("nature_of_injury", "CODE"),
           ("part_of_body", "CODE"), ("cause_of_injury", "CODE"), ("avg_weekly_wage", "AMOUNT"), ("disability_began", "DATE"),
           ("employee_dob", "DATE"), ("jurisdiction", "CODE"), ("policy_number", "ID"), ("date_reported", "DATE"),
           ("hire_date", "DATE"), ("class_code", "CODE"), ("employee_name", "TEXT")],
    "N5": [("cardholder_id", "ID"), ("bin", "ID"), ("pcn", "ID"), ("group_id", "ID"), ("rx_number", "ID"),
           ("date_filled", "DATE"), ("ndc", "CODE"), ("qty_dispensed", "AMOUNT"), ("days_supply", "AMOUNT")],
    "D1": [("member_no", "ID"), ("admission_date", "DATE"), ("separation_date", "DATE"), ("mbs_item", "CODE"),
           ("ar_drg", "CODE"), ("provider_no", "ID"), ("charge", "AMOUNT"), ("accommodation_code", "CODE"),
           ("theatre_fee", "AMOUNT"), ("prosthesis_code", "CODE"), ("episode_no", "ID"), ("principal_dx", "CODE"),
           ("separation_mode", "CODE")],
    "D2": [("member_no", "ID"), ("service_date", "DATE"), ("item_code", "CODE"), ("provider_no", "ID"),
           ("fee_charged", "AMOUNT"), ("tooth_id", "CODE"), ("quantity", "AMOUNT"), ("benefit_claimed", "AMOUNT")],
    "D3": [("policy_no", "ID"), ("claimant_dob", "DATE"), ("date_of_disablement", "DATE"), ("occupation_code", "CODE"),
           ("pre_disability_income", "AMOUNT"), ("employer_abn", "ID"), ("last_day_worked", "DATE"), ("icd10_dx", "CODE"),
           ("treating_doctor_no", "ID"), ("benefit_period", "CODE"), ("waiting_period", "CODE"), ("super_fund_usi", "ID"),
           ("bsb", "ID"), ("account_no", "ID"), ("claimant_name", "TEXT"), ("return_to_work_date", "DATE")],
    "D4": [("policy_no", "ID"), ("microchip_no", "ID"), ("treatment_date", "DATE"), ("practice_id", "ID"),
           ("condition_code", "CODE"), ("invoice_total", "AMOUNT"), ("invoice_no", "ID"), ("pet_name", "TEXT"),
           ("first_signs_date", "DATE"), ("species_breed", "CODE")],
    "D5": [("policy_no", "ID"), ("vehicle_reg", "ID"), ("incident_date", "DATE"), ("incident_time", "CODE"),
           ("incident_postcode", "CODE"), ("tp_vehicle_reg", "ID"), ("driver_dob", "DATE"), ("driver_licence", "ID"),
           ("circumstance_code", "CODE"), ("damage_area", "CODE"), ("est_repair", "AMOUNT"), ("police_ref", "ID"),
           ("witness_count", "AMOUNT"), ("tp_insurer", "TEXT"), ("injury_flag", "CODE"), ("mileage", "AMOUNT"),
           ("driver_name", "TEXT"), ("recovery_agent", "TEXT")],
    "D6": [("claim_ref", "ID"), ("policy_no", "ID"), ("loss_date", "DATE"), ("notified_date", "DATE"),
           ("peril_code", "CODE"), ("postcode", "CODE"), ("sum_claimed", "AMOUNT"), ("excess", "AMOUNT"),
           ("broker_code", "ID"), ("claimant_name", "TEXT"), ("dob", "DATE"), ("bank_sort_code", "ID")],
}
# extra fields added by a later version (field, type), and the version table: (version, effective from, added fields)
_ADD = {"N2": ("referring_npi", "ID"), "N3": ("treating_dentist_npi", "ID"), "D2": ("provider_location", "ID"),
        "D3": ("rehab_provider", "TEXT"), "D4": ("excess_applied", "AMOUNT"), "D6": ("vat_amount", "AMOUNT")}
VERSIONS = {
    "N1": [("UB04-2025.2", dt.date(2025, 4, 1), 0)],
    "N2": [("1500-0212A", dt.date(2024, 9, 2), 0), ("1500-0212B", dt.date(2026, 11, 16), 1)],
    "N3": [("J430D-24", dt.date(2025, 1, 6), 0), ("J430D-24R", dt.date(2026, 8, 10), 1)],
    "N4": [("FROI-IA1", dt.date(2025, 7, 1), 0)],
    "N5": [("UCF-D0", dt.date(2024, 1, 2), 0)],
    "D1": [("WBH-HC7", dt.date(2025, 2, 3), 0)],
    "D2": [("WBH-EX4", dt.date(2025, 2, 3), 0), ("WBH-EX5", dt.date(2026, 11, 9), 1)],
    "D3": [("CIP-IP3", dt.date(2024, 7, 1), 0), ("CIP-IP4", dt.date(2026, 9, 1), 1)],
    "D4": [("WPC-V9", dt.date(2025, 6, 2), 0), ("WPC-V10", dt.date(2026, 11, 16), 1)],
    "D5": [("TCM-FN2", dt.date(2025, 3, 3), 0)],
    "D6": [("HPY-T1", dt.date(2026, 8, 17), 0), ("HPY-T2", dt.date(2026, 11, 23), 1)],
}
_F["D3"] = _F["D3"][:15]  # IP3 carries fifteen key fields; IP4 adds the rehabilitation provider


def fields(code, version):
    base = list(_F[code])
    for v, eff, add in VERSIONS[code]:
        if v == version:
            return base + ([_ADD[code]] if add else [])
    raise KeyError(version)


def version_on(code, day):
    cur = None
    for v, eff, add in VERSIONS[code]:
        if day >= eff:
            cur = v
    return cur


def kfpd(code, day):
    return len(fields(code, version_on(code, day)))


# second-pass minutes per document by form family (truth used to simulate the session export)
SP_MIN = {"printed": 1.55, "mixed": 2.10, "handwritten": 3.05, "typed": 1.20}
Q3_SECOND_PASS = ["N1", "N2", "N3", "N4", "N5"]
OCT_SECOND_PASS = ["N1", "N2", "N3", "N4", "N5"]
HP_BUNDLE = 25

# truth of first-pass detection
TRUTH = dict(g=0.6, base_miss=0.13, base_pool=0.0427, fam={"printed": -0.20, "mixed": 0.0, "handwritten": 0.25, "typed": -0.30},
             skill_sd=0.22, ten_new=0.18, ten_mid=0.06, tos=0.05, ton=0.06, fa=0.00006)

# contracts: credit percentage of the stream's monthly invoice; currency from the client
CREDIT_PCT = {"N1": 6.0, "N2": 6.0, "N3": 8.0, "N4": 10.0, "N5": 5.0, "D1": 7.5, "D2": 7.5, "D3": 10.0,
              "D4": 8.0, "D5": 12.0, "D6": 9.0}
# rate cards: per billing unit, by account band (band floors on the account's documents in the month)
BANDS = {
    "KBA": dict(unit="claim", floors=[0, 50000, 70000], names=["K1", "K2", "K3"],
                price={"N1": [0.62, 0.57, 0.53], "N2": [0.48, 0.44, 0.41]}),
    "NDS": dict(unit="claim", floors=[0, 25000], names=["S", "M"], price={"N3": [0.58, 0.54]}),
    "BMC": dict(unit="claim", floors=[0, 20000], names=["Std", "Vol"], price={"N4": [1.10, 1.02]}, index=(dt.date(2026, 11, 20), 3.4)),
    "HPB": dict(unit="claim", floors=[0, 30000], names=["A", "B"], price={"N5": [0.39, 0.36]}),
    "WBH": dict(unit="claim", floors=[0, 140000, 162000], names=["T1", "T2", "T3"],
                price={"D1": [0.71, 0.66, 0.62], "D2": [0.52, 0.48, 0.45]}),
    "CIP": dict(unit="claim", floors=[0, 25000], names=["Base", "High"], price={"D3": [1.36, 1.27]}, index=(dt.date(2026, 11, 9), 4.1)),
    "WPC": dict(unit="claim", floors=[0, 60000], names=["A", "B"], price={"D4": [0.34, 0.31]}, index=(dt.date(2026, 11, 16), 3.9)),
    "TCM": dict(unit="notification", floors=[0, 40000], names=["Core", "Plus"], price={"D5": [0.86, 0.80]}),
    "HPY": dict(unit="document", floors=[0, 20000, 80000], names=["Pilot", "Band 2", "Band 3"],
                price={"D6": [0.38, 0.29, 0.24]}),
}
BUDGET_INR = {"USD": 84.20, "GBP": 111.60, "AUD": 55.40}
