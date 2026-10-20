"""The fixed world: the Bayline Port Authority, the roadway links around its terminals, the state's continuous count
stations, the program year October 2025 to September 2026, and the traffic each class of vehicle makes by day of
week and month. Every other module reads its parameters from here."""
import datetime as dt

PORT = "Bayline Port Authority"
DOT = "State Department of Transportation, Traffic Monitoring Section"
COUNTY = "Harbor County Public Works, Traffic Engineering"
CONSULTANT = "Meridian Traffic Data LLC"
DEPT = "Environmental Planning"
PEOPLE = {"analyst": ("Paige Hodges", "Senior Environmental Planner"),
          "director": ("Martin Estrada", "Director of Environmental Planning")}
SEED = 4750
GATE_SEED = SEED + 47                                     # the terminals' gate draw
START = dt.date(2025, 10, 1)
DAYS = [START + dt.timedelta(d) for d in range(365)]       # the program year: 1 October 2025 to 30 September 2026
LINE = 5.00                                              # tonnes of NOx per mile per program year; at or above designates
RULES_DATE = "14 January 2026"
MEMO_DATE = "4 November 2026"
CLASSES = ("P", "SU", "CU")                              # passenger vehicles (FHWA 1-3), single-unit trucks (4-7),
                                                         # combination trucks (8-13)
EF = {"P": 0.084, "SU": 1.62, "CU": 3.41}                # grams of NOx per vehicle-mile, 2026 calendar year fleet

# weekly pattern (Monday first) and monthly pattern of each class, relative; trucks fall away at weekends and are flat
# by season, passenger traffic peaks on Fridays and in summer
DOW = {"P": (0.97, 1.00, 1.01, 1.03, 1.09, 0.99, 0.88),
       "SU": (1.17, 1.21, 1.22, 1.20, 1.12, 0.63, 0.45),
       "CU": (1.19, 1.25, 1.27, 1.25, 1.15, 0.53, 0.36)}
MON = {"P": {1: .89, 2: .92, 3: .98, 4: 1.00, 5: 1.04, 6: 1.08, 7: 1.10, 8: 1.09, 9: 1.02, 10: 1.01, 11: .97, 12: .93},
       "SU": {1: .95, 2: .97, 3: 1.00, 4: 1.01, 5: 1.03, 6: 1.03, 7: 1.00, 8: 1.02, 9: 1.01, 10: 1.02, 11: .99, 12: .97},
       "CU": {1: .97, 2: .98, 3: 1.00, 4: 1.00, 5: 1.02, 6: 1.02, 7: .99, 8: 1.01, 9: 1.01, 10: 1.02, 11: 1.00, 12: .98}}
HOLIDAYS = {dt.date(2025, 11, 27): (.72, .40), dt.date(2025, 12, 25): (.62, .22), dt.date(2026, 1, 1): (.80, .45),
            dt.date(2026, 5, 25): (.85, .50), dt.date(2026, 7, 3): (.90, .60), dt.date(2026, 9, 7): (.86, .48)}

# the state's continuous count stations in and around the metro area: id, route, road type, AADT, single-unit and
# combination truck shares, whether it classifies
STATIONS = {
    "ATR-0112": ("I-880 at Ridley Avenue", "freeway", 118400, .045, .071, True),
    "ATR-0127": ("I-880 at Cole Creek", "freeway", 96300, .041, .062, False),
    "ATR-0135": ("SR-61 at Mill Street", "arterial", 31200, .036, .028, True),
    "ATR-0141": ("SR-61 at Harbor Boulevard", "arterial", 27800, .044, .039, False),
    "ATR-0156": ("I-580 at Delmar", "freeway", 142900, .038, .054, False),
    "ATR-0163": ("US-9 at Lanford", "arterial", 22600, .031, .021, False),
    "ATR-0178": ("SR-17 at Oakmont", "arterial", 18900, .029, .015, False),
    "ATR-0182": ("I-580 at Pell Road", "freeway", 104700, .040, .066, True),
    "ATR-0194": ("US-9 at Quarry Road", "arterial", 26400, .052, .047, True),
    "ATR-0205": ("SR-17 at Brennan", "arterial", 15200, .027, .012, False),
    "ATR-0211": ("I-880 at Selby", "freeway", 88100, .043, .058, False),
    "ATR-0226": ("SR-4 at Tidewater", "arterial", 21300, .035, .033, False),
}
# the roadway links: id, name, road type, AADT, single-unit and combination truck shares, count program, count start
# (the first of two count days)
LINKS = {
    "L01": ("Terminal Way, Gate 1 to SR-61", "arterial", 15120, .061, .243),
    "L02": ("Harbor Boulevard, 7th to 12th Street", "arterial", 21490, .046, .121),
    "L03": ("I-880 northbound ramps at Port Avenue", "freeway", 19790, .052, .178),
    "L04": ("Port Avenue, I-880 to Terminal Way", "arterial", 13510, .058, .214),
    "L05": ("SR-61, Mill Street to Harbor Boulevard", "arterial", 34420, .041, .083),
    "L06": ("Cargo Drive, Berths 20 to 30", "arterial", 9250, .071, .332),
    "L07": ("7th Street, Harbor Boulevard to Cole Creek", "arterial", 21010, .039, .061),
    "L08": ("I-880 southbound ramps at Port Avenue", "freeway", 15160, .050, .169),
    "L09": ("Delmar Road, I-580 to Cargo Drive", "arterial", 21320, .048, .129),
    "L10": ("Ridley Avenue, I-880 to rail yard", "arterial", 13320, .066, .224),
    "L11": ("Quarry Road truck route", "arterial", 12570, .063, .254),
    "L12": ("Harbor Boulevard, 12th to 20th Street", "arterial", 27910, .035, .052),
    "L13": ("Selby Street, rail yard to Terminal Way", "arterial", 11410, .068, .287),
    "L14": ("Pell Road, I-580 to Berth 40", "arterial", 18210, .055, .196),
}
# the golden's NOx per mile each link is tuned to (tune.py scales each link's AADT)
DESIRED = {"L01": 5.71, "L02": 3.92, "L03": 6.18, "L04": 4.38, "L05": 5.46, "L06": 4.12, "L07": 2.61, "L08": 4.12,
           "L09": 4.57, "L10": 4.21, "L11": 4.26, "L12": 3.27, "L13": 4.44, "L14": 5.48}
PROGRAM = {"L01": "county", "L02": "dot", "L03": "dot", "L04": "consultant", "L05": "dot", "L06": "consultant",
           "L07": "county", "L08": "dot", "L09": "county", "L10": "consultant", "L11": "county", "L12": "dot",
           "L13": "consultant", "L14": "county"}
COUNT_DAY = {"L01": dt.date(2025, 10, 14), "L02": dt.date(2026, 7, 21), "L03": dt.date(2026, 4, 14),
             "L04": dt.date(2026, 3, 10), "L05": dt.date(2026, 6, 16), "L06": dt.date(2026, 1, 13),
             "L07": dt.date(2025, 11, 18), "L08": dt.date(2026, 8, 18), "L09": dt.date(2026, 5, 12),
             "L10": dt.date(2025, 12, 9), "L11": dt.date(2026, 2, 10), "L12": dt.date(2025, 10, 21),
             "L13": dt.date(2026, 9, 15), "L14": dt.date(2026, 6, 23)}

FILES = {
    "stations": "ccs_hourly_volumes_oct2025_sep2026.csv",
    "register": "count_station_register_2026.xlsx",
    "dot": "dot_short_counts_fy2026.csv",
    "county": "county_traffic_counts_2025_2026.xlsx",
    "consultant": "terminal_access_counts_2026.csv",
    "links": "port_roadway_links_2026.xlsx",
    "rates": "onroad_nox_emission_rates_2026.csv",
    "rules": "air_corridor_program_rules_2027.pdf",
    "notes": "data_notes.txt",
    "gates": "terminal_gate_transactions_oct2025_sep2026.csv",
    "fleet": "drayage_truck_registry_2026.csv",
    "no2": "no2_monitor_hourly_2026.csv",
    "complaints": "truck_complaints_311_2025_2026.csv",
}
GOLDEN = {"workbook": "air_corridor_links_2027.xlsx", "memo": "air_corridor_designations_2027.pdf"}

# the asks: the three container terminals' truck gates. Terminal, name, trucks' share of visits, median turn minutes
TERMINALS = {"B20": ("Berth 20 Container Terminal", .42, 58.0),
             "B30": ("Pacific Gateway Terminal (Berths 30 to 34)", .35, 71.0),
             "B40": ("Berth 40 Intermodal Terminal", .23, 49.0)}
N_TRUCKS = 640
QUARTERS = {1: ("2025-10-01", "2025-12-31"), 2: ("2026-01-01", "2026-03-31"), 3: ("2026-04-01", "2026-06-30"),
            4: ("2026-07-01", "2026-09-30")}
