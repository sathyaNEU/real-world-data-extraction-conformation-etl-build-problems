"""task469: Kelderby International Airport's review of the summer 2027 minimum ground times the carriers filed for
its E gates. The world's fixed facts: calendar, stations, brands, operators, aircraft, the carrier relationships
(segments), how their turns behave, and the pack's file names."""
import datetime as dt

SEED = 469

AIRPORT = "Kelderby International Airport"
AUTHORITY = "Kelderby Airport Authority"
KDY = "KDY"
UTC_OFF = -4                                   # Eastern Daylight Time all summer
TZNAME = "Eastern Daylight Time (UTC-4)"

EXPORT_FROM = dt.date(2026, 6, 1)
EXPORT_TO = dt.date(2026, 9, 30)
PEAK_FROM = dt.date(2026, 6, 15)
PEAK_TO = dt.date(2026, 9, 15)
RETIME_FROM = dt.date(2026, 8, 3)              # the carriers' mid-season retimings (SSIM period splits)

STANDARD = 0.20                                # no more than 20 per cent of turns may need longer
STEP = 5                                       # ground times are filed in whole five minutes
GRID = list(range(20, 75, STEP))

WEEK27 = (dt.date(2027, 7, 12), dt.date(2027, 7, 18))      # the filed peak week (Monday to Sunday)
SEASON27 = (dt.date(2027, 3, 28), dt.date(2027, 10, 30))

BRANDS = {"NV": "Norvale Air", "TQ": "Tellura Airways", "GY": "Grayling Air"}
REGIONAL = {"NV": "Norvale Connect", "TQ": "Tellura Express", "GY": "Grayling Air"}
OPERATORS = {"PMV": ("Pellmont Aviation", "PELLMONT"), "SBC": ("Sable Coast Air", "SABLE"),
             "GYA": ("Grayling Air", "GRAYLING")}
TYPES = {"E75": "Embraer 175", "DH4": "Dash 8-400", "AT7": "ATR 72-600"}
SEATS = {"E75": 76, "DH4": 78, "AT7": 70}
HANDLER = {"NV": "Norvale Ground Services", "TQ": "Aerocrest Handling", "GY": "Grayling Air (self-handled)"}

# segment: brand, operator, type, lines (aircraft), KDY-based lines, round trips a day, 2026 ground time pattern
# (minutes by on-block hour band), filed 2027 minimum, need (median, 80th percentile, minutes), hold propensity
SEGMENTS = {
    "S1": dict(brand="NV", op="PMV", type="E75", lines=8, based=4, trips=5,
               ground=[((0, 11), 35), ((11, 15), 50), ((15, 24), 45)], filed=35, med=32.5, p80=37.5, hold=0.04),
    "S2": dict(brand="NV", op="GYA", type="AT7", lines=3, based=2, trips=5,
               ground=[((0, 24), 45)], filed=40, med=33.0, p80=37.5, hold=0.06),
    "S3": dict(brand="NV", op="SBC", type="DH4", lines=7, based=4, trips=5,
               ground=[((0, 13), 35), ((13, 24), 40)], filed=30, med=23.0, p80=27.0, hold=0.11),
    "S4": dict(brand="TQ", op="PMV", type="E75", lines=3, based=1, trips=5,
               ground=[((0, 12), 50), ((12, 16), 40), ((16, 24), 50)], filed=40, med=37.5, p80=41.5, hold=0.04),
    "S5": dict(brand="TQ", op="SBC", type="DH4", lines=3, based=1, trips=4,
               ground=[((0, 11), 30), ((11, 24), 40)], filed=30, med=29.5, p80=32.5, hold=0.04),
    "S6": dict(brand="GY", op="GYA", type="AT7", lines=3, based=2, trips=5,
               ground=[((0, 17), 40), ((17, 24), 30)], filed=35, med=24.0, p80=27.5, hold=0.03),
}
ORDER = list(SEGMENTS)

# flight number blocks (commercial numbers the brands sell), as the affiliate register files them
BLOCKS = [
    ("NV", "PMV", 3000, 3499, None, None),
    ("NV", "SBC", 3500, 3799, None, None),
    ("TQ", "PMV", 5100, 5299, None, None),
    ("TQ", "SBC", 5300, 5399, None, None),
    ("NV", "GYA", 3800, 3899, None, None),
    ("GY", "GYA", 200, 399, None, None),
]

# outstations: code, name, minutes of block each way, hours behind Kelderby (time zone)
STATIONS = [
    ("VCT", "Vellacott", 55, 0), ("BNH", "Brannoch", 70, 0), ("OLF", "Orlen Falls", 50, 0),
    ("KSB", "Kestrin Bay", 85, 1), ("MWD", "Marrowdale", 65, 0), ("SLV", "Selvig", 95, 1),
    ("HLP", "Hollin Point", 45, 0), ("TRV", "Tarvensey", 80, 0), ("QRN", "Quarne", 110, 2),
    ("PWL", "Penwallow", 60, 0),
]
STATION_NAMES = {c: n for c, n, b, z in STATIONS}

STANDS_E = ["E%d" % i for i in range(1, 15)]
STANDS_R = ["R%d" % i for i in range(1, 7)]

# IATA delay codes the operators use, and the authority's grouping (guideline 4.3): does the code say the aircraft
# was not ready to push back?
NOT_READY = {
    "11": "Late check-in, acceptance after deadline", "12": "Late check-in, congestion in check-in area",
    "15": "Boarding, discrepancies and paging, missing checked-in passenger",
    "18": "Baggage processing, sorting",
    "31": "Aircraft documentation late or inaccurate (weight and balance)",
    "32": "Loading and unloading, bulky items, special load", "33": "Loading equipment, lack of or breakdown",
    "34": "Servicing equipment, lack of or breakdown", "35": "Aircraft cleaning", "36": "Fuelling and defuelling",
    "37": "Catering, late delivery or loading", "39": "Technical equipment, lack of or breakdown (ground power)",
    "41": "Aircraft defects", "63": "Late crew boarding or departure procedures",
    "93": "Aircraft rotation, late arrival of aircraft from another flight or previous sector",
}
HELD_OTHER = {
    "81": "ATFM due to ATC en-route demand and capacity", "83": "ATFM due to restriction at destination airport",
    "84": "ATFM due to weather at destination", "87": "Airport facilities (parking stands, ramp congestion)",
    "89": "Restrictions at airport of departure (ATC start-up and pushback)",
    "71": "Weather at departure station", "96": "Operations control, re-routing or diversion",
    "98": "Industrial action outside own airline", "99": "Other reason",
    "65": "Crew special request outside legal requirements",
    "16": "Commercial publicity and passenger convenience (connecting passengers held)",
}
TURN_CODES = ["32", "35", "36", "37", "31", "15", "33", "34", "18", "12", "39", "41"]
HOLD_CODES = ["81", "89", "87", "16", "83", "71", "84"]

# AHM 731 sub-codes Sable Coast writes after the two digits
SUBCODE = {"15": "A", "31": "B", "32": "A", "33": "C", "34": "A", "35": "A", "36": "B", "37": "A", "18": "A",
           "12": "A", "39": "A", "41": "D", "63": "A", "93": "A", "81": "A", "89": "B", "87": "A", "16": "A",
           "83": "A", "71": "A", "84": "A"}

FILES = {
    "aodb": "kelderby_aodb_stand_events_jun_sep_2026.csv",
    "pellmont": "pellmont_kdy_flight_log_s26.csv",
    "sable": "sable_coast_kdy_movements_s26.xlsx",
    "grayling": "grayling_kdy_sectors_s26.csv",
    "ssim26": "kdy_season_schedule_s26.ssim",
    "ssim27": "kdy_initial_submissions_s27.ssim",
    "ssim_layout": "kdy_schedule_file_layout.pdf",
    "guideline": "kda_schedule_facilitation_guideline_e_gates.pdf",
    "filings": "kdy_e_gates_ground_time_filings_s27.csv",
    "affiliates": "kdy_affiliate_register.xlsx",
    "aircraft": "kdy_regional_aircraft_register.csv",
    "fleet27": "kdy_regional_fleet_plan_s27.csv",
    "delay_codes": "kdy_delay_code_groups.csv",
    "stations": "kdy_regional_stations.csv",
    "otp": "kdy_monthly_punctuality_by_carrier_2026.xlsx",
    "staffing": "e_gates_ground_handling_staffing_s26.csv",
}
GOLDEN = {"workbook": "kelderby_summer2027_ground_time_review.xlsx"}
DISTRACTORS = ["otp", "staffing"]

PEOPLE = {
    "director": ("Joanne Gilbert", "Director, Airside Operations"),
    "analyst": ("Gabriela Armstrong", "Analyst, Airside Performance"),
    "gates": ("Arthur Bryant", "Manager, Gate Planning"),
}


def days(a=EXPORT_FROM, b=EXPORT_TO):
    d, out = a, []
    while d <= b:
        out.append(d)
        d += dt.timedelta(days=1)
    return out


def peak(d):
    return PEAK_FROM <= d <= PEAK_TO


def ground_2026(seg, hour):
    for (a, b), g in SEGMENTS[seg]["ground"]:
        if a <= min(hour, 23) < b:
            return g
    raise ValueError(hour)


def segment_of(brand, op, typ):
    for k, s in SEGMENTS.items():
        if (s["brand"], s["op"], s["type"]) == (brand, op, typ):
            return k
    return None


def block_operator(brand, num, day):
    for b, op, lo, hi, f, t in BLOCKS:
        if b == brand and lo <= num <= hi and (f is None or day >= f) and (t is None or day <= t):
            return op
    return None
