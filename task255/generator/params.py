"""Fixed parameters of the Region Lindholt world (architecture 3). Everything the generator draws comes from SEED."""
import datetime as dt

SEED = 25503
TASK = "task255"
AS_OF = dt.date(2027, 2, 12)               # the medicines unit's analysis date (fiction)
EXTRACT_START = dt.date(2024, 7, 1)        # the register extract's first and last dispensing dates
EXTRACT_END = dt.date(2026, 12, 31)
COHORT_START = dt.date(2025, 7, 1)         # new users: first dispensing in the second half of 2025
COHORT_END = dt.date(2025, 12, 31)
LOOKBACK_DAYS = 365
HORIZON_DAYS = 365
GRACE_DAYS = 30
PROGRAMME_LINE = 60.0                      # practices under 60 per cent persistent join the programme

# products: (product number, name, ATC, strength mg, pack size); DDD per ATC in mg
DDD_MG = {"C10AA01": 30.0, "C10AA03": 30.0, "C10AA05": 20.0, "C10AA07": 10.0}
ATC_NAME = {"C10AA01": "simvastatin", "C10AA03": "pravastatin", "C10AA05": "atorvastatin", "C10AA07": "rosuvastatin"}

# practices: code, name, town; habits: shares of the dose patterns among its patients, and its patients' propensity
# to keep taking the tablets (the share persistent at a year)
PRACTICES = [
    # code   name                              town           N     H     H4    T     S     L    keep
    ("041207", "Lægerne Torvegade",             "Lindholt",    .72, .12, .00, .04, .06, .06, .71),
    ("041219", "Lægehuset Østergade",           "Lindholt",    .30, .54, .08, .02, .03, .03, .47),
    ("041224", "Lægerne ved Åen",               "Lindholt",    .48, .08, .00, .04, .34, .06, .69),
    ("041236", "Klinikken Bredgade",            "Lindholt",    .70, .12, .00, .06, .06, .06, .48),
    ("041248", "Lægerne Skovvej",               "Hornslev",    .26, .50, .12, .04, .04, .04, .49),
    ("041251", "Lægehuset Hornslev",            "Hornslev",    .46, .10, .00, .04, .34, .06, .71),
    ("041263", "Lægerne i Vejlby",              "Vejlby",      .50, .10, .00, .04, .06, .30, .69),
    ("041275", "Lægeklinikken Kirkebakken",     "Vejlby",      .36, .14, .00, .44, .02, .04, .49),
    ("041282", "Lægerne Havnegade",             "Rødby Strand",.44, .10, .00, .04, .36, .06, .71),
    ("041294", "Lægehuset Rødby Strand",        "Rødby Strand",.72, .12, .00, .04, .06, .06, .72),
    ("041307", "Lægerne Møllevej",              "Ellerup",     .40, .16, .00, .38, .02, .04, .51),
    ("041319", "Lægeklinikken Ellerup",         "Ellerup",     .50, .10, .00, .04, .04, .32, .71),
    ("041322", "Lægerne Stationsvej",           "Tvede",       .28, .48, .14, .04, .02, .04, .51),
    ("041334", "Lægehuset Tvede",               "Tvede",       .46, .08, .00, .04, .36, .06, .70),
    ("041346", "Lægerne Søndergade",            "Lindholt",    .74, .12, .00, .04, .04, .06, .73),
    ("041358", "Klinikken Vestervang",          "Lindholt",    .70, .12, .00, .06, .06, .06, .70),
]
COHORT_SIZE = (55, 125)          # new users of the second half of 2025 per practice
PREVALENT_PER_PRACTICE = (230, 420)
