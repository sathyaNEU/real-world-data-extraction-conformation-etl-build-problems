"""The fiction: one Norwegian county's pilot of a 2027 grant for activating vacant dwellings, certified by the national
statistics office from the cadastre and the meter data hub's hourly reads. Every name is invented; the people come from
guard.py names --geo Norway --seed 470."""
import datetime as dt

SEED = 470
COUNTY = "Hvitfjell"
OFFICE = "Statistics Office"
OFFICE_FULL = "the national statistics office"
MINISTRY = "Ministry of Local Government and Housing"
HUB = "the meter data hub"
PEOPLE = {
    "section_head": ("Martine Strøm", "Head of Section, Dwelling Statistics"),
    "ministry": ("Eirik Haug", "Senior Adviser, Housing Policy Department"),
}

# number, name, character, counted dwellings, golden vacant, composition of the vacant (heated house, heat-pump
# dwelling, near-empty flat, switched off), share of counted dwellings that are central-heated flats, share of the
# occupied unregistered on 1 November, share of the vacant still carrying a registered resident
MUNICIPALITIES = [
    # nr,   name,          kind,       N,    V,  heated, hp, tiny, off,  flats, unreg, regvac
    ("5801", "Brekkevoll", "town",     1640, 66, 0.34, 0.18, 0.40, 0.08, 0.46, 0.13, 0.20),
    ("5802", "Tverrvika", "coast",      520, 38, 0.82, 0.08, 0.04, 0.06, 0.04, 0.02, 0.42),
    ("5803", "Hesteby", "suburb",       980, 63, 0.20, 0.66, 0.08, 0.06, 0.32, 0.03, 0.12),
    ("5804", "Kvernhaug", "industry",   860, 33, 0.48, 0.20, 0.24, 0.08, 0.30, 0.17, 0.24),
    ("5805", "Solmoen", "inland",       430, 28, 0.36, 0.06, 0.46, 0.12, 0.05, 0.02, 0.38),
    ("5806", "Ravnsund", "town",        740, 34, 0.44, 0.22, 0.28, 0.06, 0.38, 0.06, 0.26),
    ("5807", "Ørnevik", "coast",        380, 31, 0.86, 0.06, 0.04, 0.04, 0.03, 0.03, 0.45),
    ("5808", "Langgrav", "suburb",     1120, 36, 0.30, 0.42, 0.20, 0.08, 0.22, 0.05, 0.22),
    ("5809", "Fjordeid", "mixed",       560, 30, 0.58, 0.16, 0.20, 0.06, 0.14, 0.04, 0.33),
    ("5810", "Snøholt", "mixed",        790, 37, 0.50, 0.22, 0.22, 0.06, 0.08, 0.05, 0.30),
]
THRESHOLD = 5.0
OLD_NUMBER = {"5810": "5809"}            # Snøholt was split from Fjordeid on 1 January 2024; the grid's records lag

FORTNIGHT_START = dt.date(2026, 11, 9)   # a Monday
DAYS = 14
HOURS = DAYS * 24
UTC_OFFSET = 1                           # Norwegian time is UTC+1 in November
REGISTER_DAY = dt.date(2026, 11, 1)
SNAPSHOT_DAY = dt.date(2027, 1, 5)
EVENTS_FROM = dt.date(2026, 10, 1)
CERTIFY_BY = dt.date(2027, 1, 15)

FILES = {
    "regulation": "regulation_vacant_dwelling_grant_2027.pdf",
    "assignment": "ministry_assignment_2026-12-01.eml",
    "cadastre": "matrikkel_bruksenheter_hvitfjell_2027-01-04.csv",
    "municipalities": "kommuner_hvitfjell_2026.csv",
    "meterpoints": "elhub_malepunkter_hvitfjell_2027-01-04.csv",
    "hourly": "elhub_timeverdier_2026-11-09_2026-11-22.parquet",
    "register": "folkeregister_bosatte_2027-01-05.csv",
    "events": "folkeregister_hendelser_2026-10-01_2027-01-05.csv",
    "titles": "grunnbok_hjemmel_2027-01-05.csv",
    "transfers": "grunnbok_overdragelser_2026.csv",
    "entities": "enhetsregisteret_utdrag_2027-01-05.csv",
    "shareholders": "aksjonaerregisteret_2025.csv",
    "prices": "spotpriser_no1_2026-11.csv",
    "outages": "nettselskap_avbrudd_2026-11.xlsx",
}
DISTRACTORS = ["prices", "outages"]
GOLDEN = {"xlsx": "county_dwelling_occupancy_2026-11.xlsx", "docx": "vacancy_grant_certification_2027.docx"}
