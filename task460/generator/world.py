"""The fiction's constants: eight balancing areas and their fleets, Corvane's eight candidate stores and their
planned arrays, the delivery utilities and the national supplier, the people, the dates and the file names."""
import datetime as dt

SEED = 4602027
YEAR = 2025

ORG = "Corvane Home & Garden, Inc."
ORG_SHORT = "Corvane"
COMMITTEE = "Capital Committee"
AGENCY = "Electricity Data Commission"
AGENCY_SHORT = "EDC"
RATES_TITLE = "Generation and Emission Rates by Balancing Area"
HOURLY_TITLE = "Hourly Balancing Area Operating Data (Form EDC-H1)"
VENDOR_MODEL = "Lumen Ridge Solar Engineering"
SUPPLIER = "Ardley Retail Energy LLC"
PEOPLE = {"director": "Barbara Rangel", "analyst": "Russell Scott"}
TITLES = {"director": "Director, Energy and Sustainability", "analyst": "Energy Analyst"}

# Dates in the fiction.
CHARTER_DATE = dt.date(2026, 9, 15)
CAPITAL_PLAN_DATE = dt.date(2026, 12, 4)
RATES_RELEASE = dt.date(2026, 9, 8)
RATES_2024_RELEASE = dt.date(2025, 9, 30)
HOURLY_PULL = dt.date(2026, 10, 20)
MODEL_RUN = dt.date(2026, 8, 28)
AP_PULL = dt.date(2026, 10, 21)
PACK_DATE = dt.date(2026, 10, 23)
MEMO_DATE = dt.date(2026, 11, 13)
LABEL_DATE = dt.date(2026, 6, 30)
KSTP_RENAME = dt.date(2025, 7, 1)      # the Kestrel Point area's code changed from KPLP to KSTP (local midnight)

# ------------------------------------------------------------------------------------------------ areas
# load: night base, business plateau, the hour business opens and closes (local standard), summer afternoon
# cooling, winter evening heating; a block: name, fuel, prime mover, cost rank, must-run share by season (DJF, MAM,
# JJA, SON), and its plants (code, name, nameplate MW, tonnes CO2 per net MWh).
AREAS = {
    "BRKW": dict(sky=0.78, name="Brackwell", ba="Brackwell Balancing Authority", utc=-5, lat=40.2, lon=-80.6,
                 wind=450, solar=200, ti=300, ti_sd=50,
                 load=dict(peak=8000, night=0.58, plateau=0.86, cool=0.10, up=7.0, down=19.0),
                 blocks=[
                     ("coal", "coal", "ST", 18, (0.6,) * 4, [(3361, "Ferris Bend Generating Station", 2500, 0.969),
                                                            (3366, "Hollin Creek Power Plant", 1850, 0.947),
                                                            (3372, "Marrow Hill Station", 1450, 0.941)]),
                     ("gas_cc", "natural gas", "CC", 30, (0.1,) * 4, [(56741, "Brackwell Energy Center", 1250, 0.392),
                                                                      (56902, "Sallow Run Combined Cycle", 1150, 0.388),
                                                                      (57188, "Tinsdale Power Station", 1000, 0.391)]),
                     ("gas_ct", "natural gas", "GT", 62, (0,) * 4, [(55120, "Ferris Bend Peaking Units", 600, 0.581),
                                                                     (55377, "Odell Road Peaker", 650, 0.585),
                                                                     (55410, "Granger Peaking Station", 550, 0.574)]),
                 ]),
    "QLBY": dict(sky=0.74, name="Quillbury", ba="Quillbury Grid Operator", utc=-5, lat=44.1, lon=-74.3,
                 nuc=1200, hydro=500, wind=400, solar=150, ti=0, ti_sd=50,
                 load=dict(peak=5400, night=0.78, plateau=0.86, heat=0.12, heat_c=20.0, heat_w=2.4, seas_w=0.04, up=7.0, down=20.0),
                 blocks=[
                     ("gas_cc", "natural gas", "CC", 22, (0.45,) * 4, [(55870, "Quill River Energy Center", 1450, 0.386),
                                                                        (56116, "Danvers Hollow Generating Plant", 1150, 0.392),
                                                                        (56480, "Eastbrook Combined Cycle", 850, 0.389)]),
                     ("coal_old", "coal", "ST", 46, (0,) * 4, [(2523, "Kittredge Station", 900, 1.126),
                                                               (2529, "Pellam Falls Generating Station", 600, 1.109)]),
                     ("oil_st", "petroleum", "ST", 98, (0,) * 4, [(2551, "Harbor Street Station", 600, 0.918)]),
                 ]),
    "TNFD": dict(sky=0.80, name="Tennaford", ba="Tennaford Power Pool", utc=-6, lat=41.6, lon=-93.2,
                 nuc=2000, wind=900, wind_diurnal=0.06, solar=150, ti=0, ti_sd=50,
                 load=dict(peak=7600, night=0.55, plateau=0.88, cool=0.08, up=7.0, down=18.0),
                 blocks=[
                     ("coal", "coal", "ST", 17, (0.36,) * 4, [(6018, "Cutler Prairie Station", 1500, 1.193),
                                                              (6031, "Ransom Lake Generating Station", 1150, 1.172),
                                                              (6044, "Vail Township Power Plant", 900, 1.181)]),
                     ("gas_cc", "natural gas", "CC", 33, (0,) * 4, [(57301, "Tennaford Energy Center", 1300, 0.3995),
                                                                     (57355, "Big Muddy Combined Cycle", 1200, 0.3955),
                                                                     (57420, "Orrin Valley Generating Station", 1000, 0.3985)]),
                     ("gas_ct", "natural gas", "GT", 60, (0,) * 4, [(55901, "Cutler Prairie Combustion Turbines", 800, 0.592),
                                                                     (55944, "Wakeman Peaking Plant", 700, 0.588)]),
                 ]),
    "GRSF": dict(sky=0.82, name="Gorsefield", ba="Gorsefield Balancing Authority", utc=-6, lat=38.5, lon=-90.4,
                 nuc=3000, wind=450, solar=250, ti=-200, ti_sd=50,
                 load=dict(peak=8600, night=0.56, plateau=0.86, cool=0.10, up=5.0, down=18.0),
                 blocks=[
                     ("gas_cc", "natural gas", "CC", 24, (0.15,) * 4, [(58012, "Gorsefield Energy Center", 1250, 0.368),
                                                                        (58066, "Lockhart Bend Combined Cycle", 1050, 0.373)]),
                     ("coal", "coal", "ST", 31, (0.25,) * 4, [(6705, "Ashby Ridge Generating Station", 1300, 0.8931),
                                                              (6712, "Merriweather Power Plant", 1250, 0.8861),
                                                              (6727, "Sutter Creek Station", 1050, 0.8911)]),
                     ("gas_ct", "natural gas", "GT", 57, (0,) * 4, [(55602, "Lockhart Bend Peaking Units", 700, 0.579),
                                                                     (55644, "Fenwick Road Peaker", 600, 0.584),
                                                                     (55690, "Gorsefield North Combustion Turbines", 500, 0.576)]),
                 ]),
    "FRVW": dict(sky=0.68, name="Faraview", ba="Faraview Power Administration", utc=-8, lat=46.6, lon=-121.4,
                 hydro=2000, wind=600, solar=150, ti=200, ti_sd=50,
                 load=dict(peak=5600, night=0.62, plateau=0.80, heat=0.14, seas_w=0.08, up=7.0, down=20.0),
                 blocks=[
                     ("gas_cc", "natural gas", "CC", 30, (0.1,) * 4, [(56230, "Copperline Generating Station", 1900, 0.392),
                                                                      (56244, "Faraview Energy Center", 1700, 0.388)]),
                     ("gas_ct", "natural gas", "GT", 60, (0,) * 4, [(55515, "Tolt Basin Peakers", 700, 0.603),
                                                                     (55522, "Kerrigan Combustion Turbines", 500, 0.597)]),
                 ]),
    "OSTM": dict(sky=0.93, name="Ostlemere", ba="Ostlemere Electric Grid", utc=-7, lat=33.4, lon=-111.9,
                 wind=300, solar=1000, ti=0, ti_sd=50,
                 load=dict(peak=7000, night=0.58, plateau=0.78, cool=0.16, cool_c=19.8, cool_w=1.3, seas_s=0.06, up=7.0, down=21.0),
                 blocks=[
                     ("gas_cc", "natural gas", "CC", 29, (0.12,) * 4, [(57701, "Saguaro Flats Energy Center", 1600, 0.390),
                                                                        (57738, "Ostlemere Combined Cycle", 1500, 0.393),
                                                                        (57766, "Red Mesa Generating Station", 1450, 0.392),
                                                                        (57790, "Cholla Wash Power Plant", 1250, 0.389)]),
                     ("gas_ct", "natural gas", "GT", 57, (0,) * 4, [(55801, "Ostlemere Peaking Station", 900, 0.578),
                                                                     (55830, "Dry Lake Combustion Turbines", 850, 0.583),
                                                                     (55866, "Pima Road Peaker", 850, 0.580)]),
                 ]),
    "KSTP": dict(sky=0.88, name="Kestrel Point", ba="Kestrel Point Grid Authority", utc=-8, lat=37.1, lon=-121.9,
                 former="KPLP", former_ba="Kestrel Point Light and Power", nuc=1800, wind=1200, solar=400, ti=0, ti_sd=50,
                 load=dict(peak=6000, night=0.58, plateau=0.80, cool=0.12, up=7.0, down=20.0),
                 blocks=[
                     ("gas_cc", "natural gas", "CC", 30, (0.05,) * 4, [(57902, "Kestrel Point Energy Center", 1300, 0.391),
                                                                        (57915, "Morro Gap Combined Cycle", 1200, 0.389),
                                                                        (57966, "Las Pulgas Generating Station", 1100, 0.388)]),
                     ("gas_ct", "natural gas", "GT", 60, (0,) * 4, [(55950, "Kestrel Point Peakers", 800, 0.592),
                                                                     (55977, "Alviso Combustion Turbines", 600, 0.587)]),
                 ]),
    "HLVN": dict(sky=0.80, name="Halvane", ba="Halvane Electric Balancing Authority", utc=-5, lat=35.6, lon=-79.1,
                 wind=300, solar=400, ti=0, ti_sd=50,
                 load=dict(peak=6300, night=0.58, plateau=0.84, cool=0.10, up=6.0, down=20.0),
                 blocks=[
                     ("gas_cc_a", "natural gas", "CC", 27, (0.3,) * 4, [(58310, "Halvane Energy Center", 1300, 0.379),
                                                                         (58322, "Tar Fork Combined Cycle", 1150, 0.383),
                                                                         (58347, "Pembury Generating Station", 1070, 0.381)]),
                     ("coal", "coal", "ST", 35, (0.45,) * 4, [(2711, "Cedar Shoals Steam Station", 900, 0.9937),
                                                              (2718, "Brannock Generating Station", 700, 0.9857)]),
                     ("gas_cc_b", "natural gas", "CC", 35, (0,) * 4, [(58390, "Halvane South Combined Cycle", 1000, 0.381),
                                                                       (58402, "Yadkin Bend Energy Center", 800, 0.379)]),
                     ("gas_ct", "natural gas", "GT", 60, (0,) * 4, [(55710, "Halvane Peaking Station", 900, 0.590),
                                                                     (55744, "Rocky Branch Combustion Turbines", 700, 0.586)]),
                 ]),
}
ORDER = ["BRKW", "QLBY", "TNFD", "GRSF", "FRVW", "OSTM", "KSTP", "HLVN"]

# Zero-emission plants for the register (area: [(code, name, fuel, prime mover, nameplate MW)]); hourly output comes
# from the area's nuclear, hydro, wind and solar series, shared out by nameplate.
CLEAN_PLANTS = {
    "BRKW": [(59011, "Laurel Gap Wind Farm", "wind", "WT", 260), (59020, "Coalport Ridge Wind", "wind", "WT", 190),
             (64101, "Brackwell Solar One", "solar", "PV", 200)],
    "QLBY": [(2589, "Quillbury Nuclear Station", "nuclear", "ST", 1200), (2601, "Great Chazy Dam", "hydro", "HY", 310),
             (2607, "Saranac Falls Hydro", "hydro", "HY", 190), (59110, "Tug Hill Wind", "wind", "WT", 400),
             (64212, "Penfield Solar", "solar", "PV", 150)],
    "TNFD": [(6090, "Ransom Lake Nuclear Plant", "nuclear", "ST", 2000), (59301, "Tallgrass Ridge Wind", "wind", "WT", 500),
             (59318, "Prairie Crown Wind Energy Center", "wind", "WT", 400), (64330, "Marlow Solar Farm", "solar", "PV", 150)],
    "GRSF": [(6760, "Callis Point Nuclear Station", "nuclear", "ST", 1700),
             (6768, "Bellhaven Nuclear Generating Station", "nuclear", "ST", 1300),
             (59420, "Osage Bluff Wind", "wind", "WT", 450), (64470, "Gorsefield Solar Ranch", "solar", "PV", 250)],
    "FRVW": [(3801, "Chelan Narrows Dam", "hydro", "HY", 1100), (3809, "Whistler Falls Hydroelectric", "hydro", "HY", 950),
             (3815, "Copper Creek Dam", "hydro", "HY", 650), (59511, "Horse Heaven Wind", "wind", "WT", 600),
             (64520, "Yakima Flats Solar", "solar", "PV", 150)],
    "OSTM": [(59601, "Mogollon Rim Wind", "wind", "WT", 300), (64601, "Sonoran Sun Solar", "solar", "PV", 600),
             (64618, "Agua Fria Solar Center", "solar", "PV", 500), (64633, "Ostlemere Solar Park", "solar", "PV", 400)],
    "KSTP": [(4120, "Pescadero Nuclear Power Plant", "nuclear", "ST", 1800), (59705, "Altamont Ridge Wind", "wind", "WT", 700),
             (59712, "Pacheco Pass Wind", "wind", "WT", 500), (64702, "Panoche Valley Solar", "solar", "PV", 400)],
    "HLVN": [(59802, "Pamlico Sound Wind", "wind", "WT", 300), (64810, "Halvane Solar Farm", "solar", "PV", 250),
             (64822, "Sandhills Solar", "solar", "PV", 150)],
}

# ------------------------------------------------------------------------------------------------ stores
# store number, town, latitude, longitude, array kW DC, kW AC, tilt, azimuth; the delivery utility; meters
# (main building and, at two stores, a separately metered garden centre); annual use in MWh by meter, and the
# share of use in summer (cooling) against winter (heating).
STORES = {
    "BRKW": dict(store=2104, town="Brackwell", lat=40.31, lon=-80.71, dc=430, ac=345, roof=96400, tilt=10, az=176,
                 utility="Brackwell Power & Light Company", meters=[("main", 2364)], season=(0.95, 1.12)),
    "QLBY": dict(store=2163, town="Quillbury", lat=44.02, lon=-74.18, dc=390, ac=310, roof=88900, tilt=10, az=189,
                 utility="Quillbury Electric Company", meters=[("main", 2103), ("garden centre", 260)], season=(1.12, 0.96)),
    "TNFD": dict(store=2238, town="Tennaford", lat=41.52, lon=-93.31, dc=450, ac=360, roof=104700, tilt=10, az=172,
                 utility="Tennaford Electric Delivery Company", meters=[("main", 2459)], season=(1.03, 1.08)),
    "GRSF": dict(store=2291, town="Gorsefield", lat=38.61, lon=-90.27, dc=470, ac=375, roof=112300, tilt=10, az=184,
                 utility="Gorsefield Power Company", meters=[("main", 2585)], season=(0.97, 1.14)),
    "FRVW": dict(store=2317, town="Faraview", lat=46.71, lon=-121.36, dc=380, ac=305, roof=83600, tilt=12, az=195,
                 utility="Faraview Electric Utilities", meters=[("main", 1980)], season=(1.14, 0.92)),
    "OSTM": dict(store=2356, town="Ostlemere", lat=33.46, lon=-111.83, dc=500, ac=400, roof=121800, tilt=8, az=170,
                 utility="Ostlemere Electric Service Company", meters=[("main", 2865)], season=(0.86, 1.26)),
    "KSTP": dict(store=2402, town="Kestrel Point", lat=37.18, lon=-121.84, dc=410, ac=330, roof=92100, tilt=10, az=181,
                 utility="Kestrel Point Light & Power", meters=[("main", 2221), ("garden centre", 240)], season=(0.98, 1.06)),
    "HLVN": dict(store=2449, town="Halvane", lat=35.71, lon=-79.02, dc=440, ac=350, roof=99800, tilt=10, az=166,
                 utility="Halvane Gas & Electric", meters=[("main", 2515)], season=(1.00, 1.15), gas=True),
}

# ------------------------------------------------------------------------------------------------ files
FILES = {
    "hourly": "balancing_area_hourly_operating_data_2025.csv",
    "arrays": "pilot_array_output_model_2025.csv",
    "plants": "generating_plant_register_2025.csv",
    "rates": "edc_generation_emission_rates_2025.xlsx",
    "rates24": "edc_generation_emission_rates_2024.xlsx",
    "sites": "corvane_pilot_store_sites.csv",
    "codes": "balancing_area_codes.csv",
    "utilmap": "utility_balancing_area_map.csv",
    "invoices": "corvane_electricity_invoice_lines_fy2025.csv",
    "charter": "solar_pilot_siting_charter_2027.pdf",
    "label": "ardley_power_content_label_2025.pdf",
    "dict": "pilot_siting_data_dictionary.xlsx",
    "manifest": "pilot_siting_extract_manifest.csv",
}
GOLDEN = {"memo": "solar_pilot_site_recommendation_2027.pdf", "hourly": "pilot_sites_hourly_avoided_emissions_2025.csv"}
DISTRACTORS = ["rates24", "label"]
