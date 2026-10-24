"""Constants for task279: the Hoogheemraadschap van het Lageveen, its twelve peat polder units, the monitoring network,
the laboratories, the people, the dates and the pack's file names."""
import datetime as dt

SEED = 12
DW_STREAM = 50          # the dipwell records' own random stream (the asks only)
BOARD = "Hoogheemraadschap van het Lageveen"
SHORT = "HHLV"
COMPANY = BOARD
NETWORK = "Lageveen peat monitoring network"
LAB97 = "Bodemlab Wageveld"
LAB24 = "Gouwlanden Laboratoria B.V."
SURVEY24 = "Landmeetbureau Hoekstra-Venema"
ASSEMBLED = dt.datetime(2026, 11, 2, 9, 40)
PROTOCOL_DATE = dt.date(2024, 1, 15)
ORDER_YEAR = 2027

# code, name, 1997 point prefix
UNITS = [
    ("PG-104", "Oudelaak", "OL"), ("PG-107", "Ruigeland", "RL"), ("PG-111", "Hazelweer", "HW"),
    ("PG-115", "Kortewaard", "KW"), ("PG-118", "Zuidergeer", "ZG"), ("PG-122", "Lindeschot", "LS"),
    ("PG-126", "Bovenmade", "BM"), ("PG-129", "Wedderkamp", "WK"), ("PG-133", "Goorsloot", "GS"),
    ("PG-137", "Ravenbroek", "RB"), ("PG-140", "Hellerwaard", "HL"), ("PG-144", "Meerkoog", "MK"),
]
UNIT_CODES = [u[0] for u in UNITS]
UNIT_NAME = {u[0]: u[1] for u in UNITS}
UNIT_PREFIX = {u[0]: u[2] for u in UNITS}
POINTS_PER_UNIT = 3

T97, T24 = 1997, 2024
CORE97_DEPTH, SLICE97 = 100, 5
CORE24_DEPTH, SLICE24 = 130, 10
# current NAP = 1997 survey level less this (the benchmark re-adjustments since 1997, as the 2024 survey report states)
DATUM_OFFSET_M = 0.054

PEOPLE = {
    "field_lead": "Zara Lelijveld",      # the 2024 coring campaign's field lead
    "analyst24": "Olivier Fredriks",     # Gouwlanden Laboratoria's analyst
    "hydrologist": "Yfke Gemen",         # the board's hydrologist, dipwell network
    "secretary": "Joëlle Kleijse",       # the board's secretary
    "analyst97": "Sep Ulrich",           # Bodemlab Wageveld's analyst in 1997
    "surveyor": "Michael Kalman",        # Landmeetbureau Hoekstra-Venema's surveyor in 2024
}

FILES = {
    "protocol": "veenmonitoring_protocol_2024.pdf",
    "points": "meetpunten_veenmonitoring.csv",
    "core97": "veenkernen_1997_bodemlab_wageveld.txt",
    "core24": "lims_export_veenkernen_2024.csv",
    "qc24": "lims_qc_2024.csv",
    "grid": "waterpassing_raster_1997_2024.csv",
    "survey": "hoogteonderzoek_lageveen_2024.pdf",
    "dw_series": "peilbuizen_reeksen_2014_2026.csv",
    "dw_meta": "peilbuizen_metadata.csv",
    "dw_maint": "peilbuizen_onderhoud.csv",
    "register": "peilvakken_register_2026.xlsx",
    "parcels": "percelen_gewaspercelen_2025.csv",
    "soils": "bodemkaart_peilvakken.csv",
    "weather": "weerstation_gemaal_lageveen_2014_2026.csv",
    "dictionary": "data_dictionary.txt",
    "contents": "README_files.txt",
}
DISTRACTORS = ("qc24", "parcels", "soils", "weather")
GOLDEN = "peat_carbon_loss_1997_2024.xlsx"
CHART = "peilbesluit_2027_first_raise.png"
DELIVERABLES = (GOLDEN, CHART)
REQUESTER = "Hoogheemraadschap van het Lageveen, water systems"
