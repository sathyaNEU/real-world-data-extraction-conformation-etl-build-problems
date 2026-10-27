"""task305 constants: the planning region, Marrable Foodstores' estate, the competitors, the six sites, the holiday
parks, the spend-share model's filed parameters and the pack's file names."""
import datetime as dt

ORG = "Marrable Foodstores Ltd"
PEOPLE = {"chair": "Pauline Sullivan", "property": "Joshua Ingram", "gis": "Hazel Lucas",
          "workforce": "Hollie Richardson", "transport": "Kathryn Hughes"}
SEED = 7                      # the world (towns, output areas, villages)
OPS_SEED = 30517              # the asks' operational records
E0, N0 = 492000, 352000       # grid origin of the region, metres (British National Grid)
AREA = "LQ"                   # the region's postcode area
LAD = "E06000099"
AS_OF = dt.date(2026, 10, 9)  # the appraisal folder

# the spend-share model as filed (spend_share_model_2025.pdf)
ALPHA, BETA, ROADF, INSTORE, MARGIN, MIN_AREA = 1.0, 0.22, 1.25, 0.88, 0.26, 280
GROCERY = ("SUPERMARKET AND PREMISES", "SUPERSTORE AND PREMISES", "FOOD STORE AND PREMISES")

# the world's guests: in-store grocery spend a holiday pitch's guests make in a season (1 March to 31 October)
V_PITCH = 2500.0
VFR = 0.003                   # cardholders living outside the region who shop all year (visiting family, work)
SEASON = (3, 4, 5, 6, 7, 8, 9, 10)

TOWNS = [  # name, x km, y km, output areas, households per OA, postcode sectors
    ("Darrowfield", 36, 22, 34, 128, 5), ("Bellingtoft", 50, 28, 22, 122, 3), ("Brackenmere", 22, 30, 26, 125, 4),
    ("Sallowmere", 60, 12, 18, 118, 3), ("Quellby", 12, 14, 20, 120, 3), ("Withybeck", 44, 38, 16, 119, 2),
    ("Corrinby", 6, 40, 14, 112, 2), ("Wrentoft", 66, 42, 6, 112, 2), ("Raddleford", 28, 8, 15, 121, 2),
    ("Sedgeton", 54, 4, 12, 117, 2), ("Haddrell Fen", 16, 24, 9, 115, 1), ("Loderwell", 40, 12, 10, 116, 1)]
N_VILL = 140

OWN = [  # store no, town, x, y, rating-list floor area m2, opened
    ("101", "Darrowfield", 34.5, 21.0, 2300, 1993), ("102", "Brackenmere", 22.5, 31.0, 1900, 1999),
    ("103", "Quellby", 12.5, 13.5, 1700, 2002), ("104", "Sallowmere", 60.5, 12.5, 1600, 2004),
    ("105", "Withybeck", 44.0, 38.5, 1400, 2008), ("106", "Corrinby", 6.2, 40.1, 1500, 2009),
    ("107", "Raddleford", 28.5, 8.2, 1500, 2011), ("108", "Loderwell", 40.2, 12.4, 1300, 2016),
    ("109", "Sedgeton", 54.2, 4.3, 1200, 2017), ("110", "Haddrell Fen", 16.3, 24.2, 1100, 2021)]
COMP = [  # fascia, town, x, y, rating-list floor area m2
    ("Fairbasket", "Darrowfield", 37.5, 23.0, 3200), ("Brightmart", "Darrowfield", 36.0, 20.5, 900),
    ("Pettifer's", "Bellingtoft", 50.5, 28.0, 1800), ("Fairbasket", "Brackenmere", 21.5, 29.5, 1500),
    ("Pettifer's", "Quellby", 11.8, 14.6, 2100), ("Valuewise", "Sallowmere", 59.5, 11.5, 1400),
    ("Brightmart", "Withybeck", 44.6, 37.5, 900), ("Valuewise", "Corrinby", 5.6, 39.6, 650),
    ("Brightmart", "Wrentoft", 66.4, 42.3, 850), ("Valuewise", "Raddleford", 27.6, 8.8, 1000),
    ("Brightmart", "Loderwell", 39.6, 11.6, 700), ("Valuewise", "Sedgeton", 53.6, 4.8, 800),
    ("Brightmart", "Bellingtoft", 49.4, 27.2, 600), ("Valuewise", "Brackenmere", 23.6, 30.4, 500),
    ("Fairbasket", "Raddleford", 29.75, 6.75, 3600), ("Fairbasket", "Withybeck", 47.3, 41.3, 3200),
    ("Pettifer's", "Sallowmere", 58.05, 14.5, 3000)]
SITES = [  # site, address, town, x, y, proposed floor area m2 (rating-list basis), (rent, rates, staffing, other)
    ("S1", "Fenton Road", "Bellingtoft", 50.2, 28.6, 1800, (334000, 158000, 552000, 133000)),
    ("S2", "Eastgate", "Darrowfield", 39.0, 22.5, 1800, (171000, 101000, 470000, 97000)),
    ("S3", "Mill Lane", "Wrentoft", 66.0, 41.8, 1500, (144000, 92000, 571000, 117000)),
    ("S4", "Northfield", "Brackenmere", 22.0, 33.0, 1500, (142000, 84000, 380000, 85000)),
    ("S5", "Sutton Road", "Quellby", 16.0, 17.0, 1600, (128000, 77000, 380000, 74000)),
    ("S6", "Westway", "Sallowmere", 57.0, 13.0, 1500, (116000, 72000, 410000, 64000))]
PARKS = [  # name, x, y, pitches, rating-list description
    ("Raddleford Water Holiday Park", 29.8, 6.6, 640, "CARAVAN PARK AND PREMISES"),
    ("Wrentoft Lakes Holiday Park", 68.5, 44.0, 1750, "CARAVAN PARK AND PREMISES"),
    ("Withybeck Lakes Caravan Park", 47.5, 41.5, 520, "CARAVAN PARK AND PREMISES"),
    ("Sallowmere Mill Caravan Park", 58.0, 14.6, 160, "CARAVAN PARK AND PREMISES")]
DC = ("Loderwell Gate distribution centre", 40.5, 11.0)
PARK_ROAD = {"Raddleford Water Holiday Park": "Water Lane", "Wrentoft Lakes Holiday Park": "Marsh Road",
             "Withybeck Lakes Caravan Park": "Lakes Road", "Sallowmere Mill Caravan Park": "Mill Road",
             "Corrinby Farm Camping and Caravans": "Grange Lane", "Loderwell Brook Touring Park": "Brook Lane"}
# the parishes the villages lie in, named on every rural address (records.py seats them in this order)
PARISHES = [
    "Chalderby", "Dorrelby", "Rushelby", "Scaddleby", "Linnetby", "Gorseyby", "Reedleby", "Winnowby", "Martenby",
    "Skerryby", "Anselham", "Cressetham", "Harrelham", "Kirtleham", "Mosselham", "Saxelham", "Osierham", "Tansyham",
    "Cobbleham", "Teaselton", "Marramton", "Fennelton", "Otterholme", "Emberholme", "Crandleholme", "Flintholme",
    "Carrowholme", "Cinderholme", "Bitternholme", "Hollintoft", "Rooktoft", "Reedtoft", "Burdocktoft", "Farrowstead",
    "Tithestead", "Peatstead", "Ryestead", "Larchstead", "Garretstead", "Elderworth", "Pindercote", "Coppercote",
    "Alderbeck", "Limebeck", "Cantlebeck", "Wharfbeck", "Maltmere", "Bardlemere", "Gimblemere", "Shingledale",
    "Kindledale", "Vetchdale", "Fallowley", "Tindleley", "Heronwell", "Brambleford", "Sorrelfield", "Umbercroft",
    "Ashencroft", "Tallowcroft", "Wimblecroft"]

FY = (dt.date(2025, 4, 1), dt.date(2026, 3, 31))
MONTHS = ["2025-%02d" % m for m in range(4, 13)] + ["2026-%02d" % m for m in range(1, 4)]
TMS_FROM, TMS_TO = dt.date(2025, 10, 6), dt.date(2026, 3, 29)     # 25 weeks, the TMS export
BUS_DAY = dt.date(2027, 1, 15)
BUS_RADIUS = 400.0

FILES = {
    "households": "census2021_ts041_households_oa.csv",
    "pwc": "oa21_population_weighted_centroids.csv",
    "spend": "grocery_spend_estimates_2026_oa21.csv",
    "onspd": "onspd_may2026_lq.csv",
    "voa_list": "voa_list_entries_2026_lq.txt",
    "voa_smv": "voa_summary_valuations_2026_lq.csv",
    "estate": "store_estate_2026.xlsx",
    "cards": "card_spend_by_home_sector_fy2025_26.csv",
    "shortlist": "site_shortlist_2027.xlsx",
    "model": "spend_share_model_2025.pdf",
    "voa_spec": "voa_compiled_list_file_specification_2026.pdf",
    "dc_proc": "loderwell_gate_store_deliveries_procedure.pdf",
    "tms": "tms_stop_export_20251006_20260329.csv",
    "receipts": "goods_in_receipts_20251006_20260329.csv",
    "wfm": "wfm_paid_hours_20251006_20260329.csv",
    "punches": "ta_punches_20251006_20260329.csv",
    "terminals": "ta_terminals.csv",
    "gtfs_lb": "gtfs_sallowmere_motor_services_20261002.zip",
    "gtfs_pdc": "gtfs_wrentoft_district_coaches_20261002.zip",
    "aadf": "dft_aadf_count_points_lq_2025.csv",
    "survey": "customer_survey_store_scores_2025.csv",
}
