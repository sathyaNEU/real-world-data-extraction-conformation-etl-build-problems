"""task306 constants: Voltwerk Accu Revisie B.V. (Tilburg), its five traction-battery platforms, the Dutch register on
30 June 2026, the 2027 tooling plan, the line's 2025-26 financial year and the seeds."""
import datetime as dt

ORG = "Voltwerk Accu Revisie B.V."
TOWN = "Tilburg"

SEED_WORLD = 3448          # the cars, their packs and their arrivals (scratch prototype search2.py, seed 3448)
SEED_REG = 30601           # plates, trade names, colours and the register's other columns
SEED_LOG = 30602           # countries and sources of the replacement log
SEED_FITS = 30603          # the Voltwerk fittings after the register's date (July and August 2026)
SEED_LINE = 31062          # the line: cores, work orders, stores, end-of-line runs, shipments, the recycler
SEED_DOCS = 30604          # the distractors' values

# platform: (launch year, new registrations a year at peak, used imports a month, import age mean, sd,
#            OEM curve Weibull scale, shape)
PLAT = {"Volta hatch": (2014, 2600, 45, 5.6, 1.1, 13.0, 3.3),
        "Kestrel SUV": (2016, 2400, 15, 4.8, 1.1, 14.5, 3.4),
        "Plover saloon": (2015, 2000, 18, 5.2, 1.1, 15.0, 3.2),
        "Mira city car": (2013, 180, 150, 8.2, 0.7, 10.0, 7.0),
        "Tern van": (2017, 1100, 3, 4.0, 1.1, 13.5, 3.5)}
NAMES = list(PLAT)
WARRANTY = {"Volta hatch": 8, "Kestrel SUV": 8, "Plover saloon": 8, "Mira city car": 5, "Tern van": 8}
VW_WARRANTY = 2
REFURB = (7.5, 2.6)        # Voltwerk's refurbished pack, all platforms
EXIT_MEAN = 60.0           # years: cars leaving the fleet before the snapshot (scrapped or exported)

SNAP = dt.date(2026, 6, 30)
Y0, Y1 = dt.date(2027, 1, 1), dt.date(2028, 1, 1)
END = dt.date(2027, 12, 31)
FY0, FY1 = dt.date(2025, 7, 1), dt.date(2026, 6, 30)     # Voltwerk's 2025-26 financial year
AS_OF = dt.date(2026, 8, 14)

SLOTS = 3000
LOT = 50

# the register
MERK = {"Volta hatch": "VOLTA", "Kestrel SUV": "KESTREL", "Plover saloon": "PLOVER", "Mira city car": "MIRA",
        "Tern van": "TERN"}
TRADE = {"Volta hatch": [("HATCH", 0.46), ("HATCH E", 0.22), ("E-HATCH 40", 0.17), ("HATCH LONG RANGE", 0.15)],
         "Kestrel SUV": [("KESTREL", 0.41), ("KESTREL EV", 0.27), ("KESTREL AWD", 0.18), ("KESTREL 77 KWH", 0.14)],
         "Plover saloon": [("PLOVER", 0.52), ("PLOVER E", 0.21), ("PLOVER SALOON", 0.17), ("PLOVER GT", 0.10)],
         "Mira city car": [("MIRA", 0.38), ("MIRA E", 0.27), ("MIRA ELECTRIQUE", 0.21), ("MIRA CITY", 0.14)],
         "Tern van": [("TERN VAN", 0.44), ("TERN E-VAN", 0.25), ("TERN VAN L2H1", 0.19), ("TERN VAN L1", 0.12)]}
SOORT = {"Tern van": "Bedrijfsauto"}
INRICHTING = {"Volta hatch": "hatchback", "Kestrel SUV": "MPV", "Plover saloon": "sedan", "Mira city car": "hatchback",
              "Tern van": "gesloten opbouw"}
SEATS = {"Volta hatch": 5, "Kestrel SUV": 5, "Plover saloon": 5, "Mira city car": 4, "Tern van": 2}
MASS = {"Volta hatch": 1545, "Kestrel SUV": 2090, "Plover saloon": 1830, "Mira city car": 1195, "Tern van": 1985}
PRICE = {"Volta hatch": 33490, "Kestrel SUV": 52990, "Plover saloon": 44790, "Mira city car": 23950,
         "Tern van": 41850}
ORIGIN = {"Volta hatch": [("DE", 0.48), ("BE", 0.31), ("FR", 0.21)],
          "Kestrel SUV": [("DE", 0.55), ("BE", 0.25), ("AT", 0.20)],
          "Plover saloon": [("DE", 0.46), ("BE", 0.33), ("DK", 0.21)],
          "Mira city car": [("FR", 0.39), ("IT", 0.26), ("ES", 0.16), ("BE", 0.10), ("DE", 0.09)],
          "Tern van": [("DE", 0.62), ("BE", 0.38)]}

# the line
CODE = {"Volta hatch": "VH", "Kestrel SUV": "KS", "Plover saloon": "PS", "Mira city car": "MC", "Tern van": "TV"}
BOM = {"Volta hatch": 12, "Kestrel SUV": 16, "Plover saloon": 14, "Mira city car": 8, "Tern van": 18}
PER_UNIT = {"Volta hatch": 1, "Kestrel SUV": 2, "Plover saloon": 1, "Mira city car": 1, "Tern van": 1}
UNITS_MEAN = {"Volta hatch": 3.1, "Kestrel SUV": 2.2, "Plover saloon": 3.5, "Mira city car": 2.7, "Tern van": 4.0}
FPY = {"Volta hatch": 0.925, "Kestrel SUV": 0.905, "Plover saloon": 0.94, "Mira city car": 0.885,
       "Tern van": 0.89}
BMS_SWAP = 0.7             # share of reworks after a failed end-of-line run that replace the pack's BMS
RETEST_PASS = 0.97
REJECT = {"Volta hatch": 0.088, "Kestrel SUV": 0.071, "Plover saloon": 0.079, "Mira city car": 0.142,
          "Tern van": 0.052}
EOL_HOURS = {"Volta hatch": 5.2, "Kestrel SUV": 6.4, "Plover saloon": 5.8, "Mira city car": 3.6, "Tern van": 7.1}
PROGRAM = {"Volta hatch": ["EOL-VH-3.2", "EOL-VH-3.3"], "Kestrel SUV": ["EOL-KS-2.4"],
           "Plover saloon": ["EOL-PS-2.1", "EOL-PS-2.2"], "Mira city car": ["EOL-MC-4.0", "EOL-MC-4.1"],
           "Tern van": ["EOL-TV-1.3"]}
# supplier-lot holds: (platform, packs held, units each); the replacement pick is booked once for the batch
HOLDS = [("Volta hatch", 4, 2), ("Volta hatch", 5, 2), ("Kestrel SUV", 3, 2), ("Plover saloon", 3, 2),
         ("Plover saloon", 4, 1), ("Mira city car", 4, 2), ("Mira city car", 3, 2), ("Tern van", 2, 3)]

PEOPLE = {"planner": "Imke Recers", "controller": "Maarten Cammel"}

FILES = dict(
    register="rdw_gekentekende_voertuigen_20260630.csv",
    log="accuvervangingen_2014_2026.csv",
    curves="levensduurcurves_tractieaccu.csv",
    warranty="garantievoorwaarden_tractieaccu_2026.pdf",
    plan="tooling_plan_2027_draft.docx",
    rdw_notes="rdw_extract_veldbeschrijving.pdf",
    workorders="mes_werkorders_2025-26.csv",
    stores="magazijn_mutaties_2025-26.csv",
    receipts="magazijn_ontvangsten_2025-26.csv",
    parts="artikelstam_modules.xlsx",
    eol="eol_testlog_2025-26.csv",
    bms="mes_bms_koppelingen_2025-26.csv",
    shipments="verzendingen_2025-26.csv",
    intake="kernen_inname_2025-26.csv",
    recycler="afvoer_recycler_2025-26.xlsx",
    line_notes="lijn_exports_toelichting.md",
    prices="prijslijst_revisiepakketten_2026.pdf",
    leadtimes="module_levertijden_2026.xlsx",
)
