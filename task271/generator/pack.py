"""Assemble the evidence pack: the world, its exports, the documents, the two distractors, the dictionary and the
contents list."""
import csv
import datetime as dt
import os

import numpy as np

import common as K
import docs
import records
import world as W


def rows(target, key):
    with open(os.path.join(target, K.FILES[key]), encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def weather(path, seed):
    """the county airport's daily summaries, 2023 to 2025 (NOAA GHCN-Daily form)"""
    rng = np.random.default_rng(seed + 404)
    out = []
    d = dt.date(2023, 1, 1)
    cold = {dt.date(2023, 2, 3): -4, dt.date(2023, 2, 4): -7, dt.date(2024, 1, 16): -6, dt.date(2024, 1, 17): -9,
            dt.date(2024, 1, 21): -3, dt.date(2025, 1, 21): -8, dt.date(2025, 1, 22): -5, dt.date(2025, 2, 19): -2}
    while d <= dt.date(2025, 12, 31):
        doy = d.timetuple().tm_yday
        base = 52 - 24 * np.cos(2 * np.pi * (doy - 15) / 365.25)
        tmax = round(base + 9 + rng.normal(0, 7))
        tmin = round(base - 9 + rng.normal(0, 6))
        if d in cold:
            tmin, tmax = cold[d], cold[d] + 14
        prcp = round(float(rng.exponential(0.28)) if rng.random() < 0.33 else 0.0, 2)
        snow = round(prcp * 10 * (1 if tmax < 34 else 0), 1)
        out.append(["USW00014761", "TAMSWOLD COUNTY AIRPORT, PA US", d.isoformat(), "%.2f" % prcp, "%.1f" % snow,
                    tmax, tmin, round(float(rng.gamma(4, 5.5)), 1)])
        d += dt.timedelta(1)
    return records.write_csv(path, ["STATION", "NAME", "DATE", "PRCP", "SNOW", "TMAX", "TMIN", "WSF5"], out)


def permits(path, w, seed):
    rng = np.random.default_rng(seed + 505)
    out = []
    seq = 0
    kinds = [("ROOF", "Reroof, tear-off", 0.34), ("ELECTRICAL", "Service upgrade", 0.16),
             ("PLUMBING", "Water heater replacement", 0.14), ("PLUMBING", "Fixture or supply replacement", 0.08),
             ("MECHANICAL", "Furnace or heat pump replacement", 0.12), ("ADDITION", "Addition or porch", 0.06),
             ("DECK", "Deck", 0.06), ("POOL", "In-ground pool", 0.02), ("DEMOLITION", "Accessory structure", 0.02)]
    for p in w.parcels:
        if p["land_use"] != "R-SFD":
            continue
        for _ in range(rng.poisson(0.19)):
            k = kinds[int(rng.choice(len(kinds), p=[q[2] for q in kinds]))]
            seq += int(rng.integers(1, 3))
            d = dt.date(2023, 1, 2) + dt.timedelta(int(rng.integers(0, 1090)))
            val = int(rng.lognormal(np.log({"ROOF": 14000, "ELECTRICAL": 3500, "PLUMBING": 2600, "MECHANICAL": 8800,
                                            "ADDITION": 46000, "DECK": 9500, "POOL": 52000, "DEMOLITION": 2500}[k[0]]),
                                    0.45)) // 50 * 50
            out.append(["BP-%d-%05d" % (d.year, seq), p["parcel_id"], K.TOWN_NAME[p["town"]].upper(), d.isoformat(),
                        k[0], k[1], val, "FINALED" if rng.random() < 0.86 else "ISSUED"])
    out.sort(key=lambda r: (r[3], r[0]))
    return records.write_csv(path, ["permit_number", "parcel_id", "municipality", "issue_date", "permit_type",
                                    "work_description", "valuation", "status"], out)


DICTIONARY = [
    ("policy_terms_2023_2025.csv", "policy_number", "Policy number; a policy keeps its number at renewal"),
    ("policy_terms_2023_2025.csv", "term_number", "Term of the policy, 1 for the first term written"),
    ("policy_terms_2023_2025.csv", "term_effective / term_expiration", "Term dates; a term covers from 12:01 a.m. on the effective date to 12:01 a.m. on the expiration date"),
    ("policy_terms_2023_2025.csv", "cancellation_effective", "Date a cancellation took effect, blank if the term was not cancelled"),
    ("policy_terms_2023_2025.csv", "cancellation_reason", "SOLD, INSURED REQUEST or NONPAY"),
    ("policy_terms_2023_2025.csv", "reinstatement_effective", "Date coverage was reinstated after a cancellation for non-payment, without a lapse"),
    ("policy_terms_2023_2025.csv", "parcel_id", "County parcel number of the insured home, as on the county assessment roll"),
    ("policy_terms_2023_2025.csv", "municipality_code", "WYV Wyvellton, HLT Holtmere, VRN Varnacott, MRV Merrivane"),
    ("policy_terms_2023_2025.csv", "year_built ... stories", "The home's characteristics as recorded on the term (codes in the underwriting guide)"),
    ("policy_terms_2023_2025.csv", "coverage_a", "Dwelling limit, US dollars"),
    ("policy_terms_2023_2025.csv", "deductible", "All-peril deductible, US dollars"),
    ("policy_terms_2023_2025.csv", "annual_premium", "Written annual premium for the term, US dollars"),
    ("claims_register_2023_2025.csv", "claim_number", "Claim number; a reopened claim is entered as a new line under the original number with the suffix -R1"),
    ("claims_register_2023_2025.csv", "reopened_from", "On a reopened line, the original claim number"),
    ("claims_register_2023_2025.csv", "date_of_loss / date_reported", "Date the loss occurred; date it was first reported (on a reopened line, the date it was reopened)"),
    ("claims_register_2023_2025.csv", "cause_code", "Cause of loss in the code set in force when the line was entered (cause_of_loss_codes.csv)"),
    ("claims_register_2023_2025.csv", "catastrophe_code", "Property Claim Services catastrophe serial, where assigned"),
    ("claims_register_2023_2025.csv", "claim_status", "OPEN, CLOSED or CLOSED WITHOUT PAYMENT at the extract"),
    ("claim_payments_2023_2026.csv", "transaction_type", "INDEMNITY payment to the insured; EXPENSE to an adjuster or vendor; VOID of an earlier check (negative); RECOVERY by subrogation or salvage (negative)"),
    ("claim_payments_2023_2026.csv", "amount", "US dollars; voids and recoveries are negative"),
    ("claim_payments_2023_2026.csv", "claim_number", "Claim the transaction is posted to, as in the claims register"),
    ("cause_of_loss_codes.csv", "maps_to_2024", "For a legacy code, the 2024 codes its losses are entered under from January 1, 2024"),
    ("tamswold_parcels_2026.csv", "parcel_id", "County parcel number"),
    ("tamswold_parcels_2026.csv", "land_use_code", "County land use classification"),
    ("tamswold_parcels_2026.csv", "homestead_farmstead", "H where the owner holds the homestead exclusion (owner's primary residence); F farmstead"),
    ("tamswold_parcels_2026.csv", "x_coord_ft / y_coord_ft", "Parcel point, NAD83 Pennsylvania South state plane, US survey feet (EPSG:2272)"),
    ("tamswold_parcels_2026.csv", "assessed_land / assessed_improvement / assessed_total", "Assessed value on the certified 2026 roll, US dollars, at the county's 1998 base-year values"),
    ("tamswold_parcels_2026.csv", "last_sale_date / last_sale_price", "Most recent recorded deed transfer for value, where one is on file"),
    ("tamswold_dwellings_2026.csv", "card_number", "Dwelling card on the parcel; card 1 is the principal dwelling"),
    ("tamswold_dwellings_2026.csv", "foundation ... exterior_wall", "Assessor's dwelling characteristics"),
    ("assessment_appeals_2026.csv", "decision", "Board of Assessment Appeals decision for the tax year: REDUCED, INCREASED, SUSTAINED or WITHDRAWN"),
    ("assessment_appeals_2026.csv", "assessed_total_after", "Assessed total set by the decision for the tax year; blank where the appeal was withdrawn"),
    ("steb_common_level_ratios.csv", "common_level_ratio", "State Tax Equalization Board common level ratio for the county, in use from effective_from to effective_to"),
    ("tcwa_pressure_zones.geojson", "ZONE_ID / ZONE_NAME", "Authority pressure zone (EPSG:2272 polygons)"),
    ("tcwa_pressure_zones.geojson", "HGL_FT", "Hydraulic grade line at average day demand, feet above sea level"),
    ("tcwa_hydrants.geojson", "HYDRANT_ID", "Hydrant number since the April 1, 2024 renumbering"),
    ("tcwa_hydrants.geojson", "FORMER_ID", "Hydrant number before the April 1, 2024 renumbering; blank for hydrants installed since"),
    ("tcwa_hydrants.geojson", "STATUS / OWNER", "IN SERVICE, OUT OF SERVICE or ABANDONED; TCWA or PRIVATE"),
    ("tcwa_hydrant_flow_tests.csv", "hydrant_id", "Hydrant number in force on the test date"),
    ("tcwa_hydrant_flow_tests.csv", "static_psi / residual_psi / flow_gpm", "Static pressure; residual pressure while the flow hydrant was open; flow from the open hydrant"),
    ("noaa_daily_weather_2023_2025.csv", "TMAX / TMIN / PRCP / SNOW / WSF5", "Daily maximum and minimum temperature (F), precipitation and snowfall (in), fastest 5-second wind (mph)"),
    ("tamswold_building_permits_2023_2025.csv", "permit_type", "County building permit type"),
]

CONTENTS = """Halverstead Mutual Fire Insurance Company - 2027 agency township review
Pack assembled {asm} for the Underwriting Manager.

Company records (extract of {ext})
  policy_terms_2023_2025.csv          policy terms in force at any time in 2023 to 2025
  claims_register_2023_2025.csv       claims with a date of loss in 2023 to 2025, as on the claim system
  claim_payments_2023_2026.csv        payment, void and recovery transactions on those claims to the extract
  cas_bordereau_halverstead_2023_2026.xlsx  Corrigan Adjusting Services' monthly bordereaux, March 2023 to August 2026
  cause_of_loss_codes.csv             legacy and 2024 cause-of-loss codes
  frequency_model_standard_rev2.pdf   Frequency Model Standard, revision 2
  underwriting_guide_homeowners_2025.pdf
  board_expansion_brief_2027.pdf      the President's request for the board paper

Tamswold County (Office of Assessment, extract of {roll})
  tamswold_parcels_2026.csv           certified 2026 assessment roll, seven townships
  tamswold_dwellings_2026.csv         dwelling characteristics, one row per dwelling card
  assessment_appeals_2026.csv         Board of Assessment Appeals decisions for tax year 2026
  steb_common_level_ratios.csv        the county's common level ratios as the State Tax Equalization Board certifies them
  tamswold_building_permits_2023_2025.csv   building permits issued 2023 to 2025

Tamswold County Water Authority (open data, as published)
  tcwa_pressure_zones.geojson         pressure zones (edited {zm})
  tcwa_hydrants.geojson               hydrant register at {hyd}
  tcwa_hydrant_flow_tests.csv         hydrant flow tests 2018 to {hyd}
  tcwa_master_plan_2019_excerpt.pdf   Water System Master Plan 2019, chapters 3 and 6

Other
  noaa_daily_weather_2023_2025.csv    county airport daily summaries
  data_dictionary.csv                 field descriptions
"""


def build_pack(out, seed=K.SEED):
    os.makedirs(out, exist_ok=True)
    w = W.World(seed)
    ex = records.Exports(w)
    p = lambda k: os.path.join(out, K.FILES[k])   # noqa: E731
    n = {}
    n["terms"] = ex.terms(p("terms"))
    n["claims"] = ex.claims(p("claims"))
    n["payments"] = ex.payments_file(p("payments"))
    n["bordereau"] = ex.bordereau(p("bordereau"))
    n["codes"] = ex.codes(p("codes"))
    n["parcels"] = ex.parcels(p("parcels"))
    n["dwellings"] = ex.dwellings(p("dwellings"))
    n["appeals"] = ex.appeals(p("appeals"))
    n["clr"] = ex.clr(p("clr"))
    n["zones"] = ex.zones_geojson(p("zones"), w.zoner)
    n["hydrants"], n["flowtests"] = ex.hydrants_geojson(p("hydrants"), p("flowtests"))
    n["weather"] = weather(p("weather"), seed)
    n["permits"] = permits(p("permits"), w, seed)
    docs.standard(p("standard"))
    docs.guide(p("guide"))
    docs.brief(p("brief"))
    docs.master_plan(p("plan"))
    n["dictionary"] = docs.dictionary(p("dictionary"), DICTIONARY)
    with open(p("readme"), "w", encoding="utf-8", newline="\r\n") as f:
        f.write(CONTENTS.format(asm=K.ASSEMBLED.strftime("%B %d, %Y"), ext=K.EXTRACT.isoformat(),
                                roll=K.ROLL_EXTRACT.isoformat(), zm=K.ZONE_MAP_DATE.isoformat(),
                                hyd=K.HYDRANT_DATE.isoformat()))
    return w, ex, n
