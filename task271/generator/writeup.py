"""submission.md from generator/figures.json: every figure the write-up states is emitted from the figures file."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as K   # noqa: E402

KIND = {c: k for c, n, k in K.TOWNS}


def n(x):
    return "{:,}".format(x)


def write(task):
    f = json.load(open(os.path.join(HERE, "figures.json")))
    c, co, a, cx = f["call"], f["components"], f["asks"], f["context"]
    fr = co["frequency_per_1000"]
    order = sorted(K.CANDIDATES, key=lambda t: fr[t])
    pick, run, last = order
    nm = lambda t: "%s %s" % (K.TOWN_NAME[t], KIND[t])   # noqa: E731
    rel = cx["relativities"]["zone=PZ-3 vs PZ-2"]
    mv, pr, pay, fi = a["market_value_musd"], a["protected_homes"], a["water_payment_by_accident_year"], a["fire_per_1000"]
    vz, hm = co["valley_zone_homes"], co["homes"]
    lines = [
        "## Tags",
        "",
        "> **Domain:** Actuarial Science & Insurance (claims frequency and severity).",
        "> **Analytical objective:** Descriptive & Distribution Analysis.",
        "",
        "## 1. Final Recommendation",
        "",
        "**Open the 2027 agency in %s.** Its owner-occupied single-family homes would bring %d non-weather water claims "
        "per 1,000 house-years at our 2023 to 2025 experience, %d fewer than %s's %d. Not %s, %s of whose %s homes "
        "draw from the water authority's Valley zone. Not %s (%d), whose newer slab-built homes look safest on the "
        "policy record but %s of whose %s homes draw from the Valley zone, where our homes claim at %.2f times the "
        "rate of the Upper zone." % (nm(pick), fr[pick], c["gap_per_1000"], K.TOWN_NAME[run], fr[run], K.TOWN_NAME[run],
                                    n(vz[run]), n(hm[run]), K.TOWN_NAME[last], fr[last], n(vz[last]), n(hm[last]), rel),
        "",
        "## 2. Critical Components",
        "",
        "1. Homes in the Valley zone: %s **%s** of %s, %s **%s** of %s, %s **%s** of %s" % (
            K.TOWN_NAME[pick], n(vz[pick]), n(hm[pick]), K.TOWN_NAME[run], n(vz[run]), n(hm[run]), K.TOWN_NAME[last],
            n(vz[last]), n(hm[last])),
        "2. The Frequency Model Standard's 2025 test chooses foundation and water supply zone at a Poisson deviance of "
        "**{:,.1f}**, against **{:,.1f}** for the best model on the characteristics the policy terms record "
        "(foundation alone)".format(co["deviance_2025_chosen"], co["deviance_2025_best_recorded_only"]),
        "3. Non-weather water claims per 1,000 house-years: %s **%d**, %s **%d**, %s **%d**" % (
            K.TOWN_NAME[pick], fr[pick], K.TOWN_NAME[run], fr[run], K.TOWN_NAME[last], fr[last]),
        "",
        "## 3. Step-by-Step Solution",
        "",
        "1. Earned house-years by home and accident year from policy_terms_2023_2025.csv (standard 2.4) and non-weather "
        "water claims from claims_register_2023_2025.csv (standard 2.1 to 2.3: WTR-P, WTR-A, 3110, 3120 and 3130, "
        "each claim once with the -R1 lines dropped, by date of loss): {:,} claims over {:,.1f} house-years, {} per "
        "1,000.".format(cx["book_water_claims"], cx["book_house_years"], cx["book_frequency_per_1000"]),
        "2. Placed each home's parcel point from tamswold_parcels_2026.csv in tcwa_pressure_zones.geojson (the Upper "
        "zone's two polygons are one zone): %s, %s and %s of the townships' homes are in the Valley zone." % (
            n(vz[pick]), n(vz[run]), n(vz[last])),
        "3. Ran the standard's section 4 search over every main-effects Poisson model on foundation, year built era, "
        "full bathrooms, construction, stories and zone, fitted on 2023 and 2024 and judged on 2025: foundation and "
        "zone win at {:,.1f}, the best model without the zone (foundation alone) scores {:,.1f}.".format(
            co["deviance_2025_chosen"], co["deviance_2025_best_recorded_only"]),
        "4. Refitted the model on 2023 to 2025 (Valley zone %.2f times the Upper zone) and averaged each township's "
        "owner-occupied single-family homes (R-SFD with the homestead exclusion, card 1 of tamswold_dwellings_2026.csv "
        "mapped per the underwriting guide): %s %d, %s %d, %s %d per 1,000 house-years." % (
            rel, K.TOWN_NAME[pick], fr[pick], K.TOWN_NAME[run], fr[run], K.TOWN_NAME[last], fr[last]),
        "5. Protected homes per the underwriting guide section 2: each test in tcwa_hydrant_flow_tests.csv joined to "
        "its hydrant by the number in force on its date (FORMER_ID before April 1, 2024), the latest test's flow "
        "carried to 20 psi residual by NFPA 291 (flow times ((static - 20) / (static - residual)) to the 0.54), "
        "in-service authority hydrants within 1,000 feet: %s %s, %s %s, %s %s." % (
            K.TOWN_NAME[pick], n(pr[pick]), K.TOWN_NAME[run], n(pr[run]), K.TOWN_NAME[last], n(pr[last])),
        "6. Market value: the roll's 2026 assessed totals, replaced by the 2026 decisions in "
        "assessment_appeals_2026.csv, over the common level ratio in effect on January 1, 2026 (%.3f): %s $%.1f "
        "million, %s $%.1f million, %s $%.1f million." % (
            cx["common_level_ratio"], K.TOWN_NAME[pick], mv[pick], K.TOWN_NAME[run], mv[run], K.TOWN_NAME[last],
            mv[last]),
        "7. Water claim payments: indemnity per claim from claim_payments_2023_2026.csv (the -R1 lines' payments "
        "folded into their claim) plus the latest paid to date in cas_bordereau_halverstead_2023_2026.xlsx for the "
        "claims Corrigan Adjusting Services handled, net of recoveries: 2023 $%s, 2024 $%s, 2025 $%s; fire and "
        "lightning claims (FIR, 5110, 5120) on the book's unprotected homes: %.1f per 1,000 house-years." % (
            n(pay["2023"]), n(pay["2024"]), n(pay["2025"]), fi["unprotected"]),
        "8. The agency opens in %s, the township with the fewest non-weather water claims per house-year." % nm(pick),
        "",
        "## 4. Deliverable Answers",
        "",
        "### %s" % K.BOOK,
        "",
        "1. Non-weather water claims per 1,000 house-years: %s %d; %s %d; %s %d" % (
            K.TOWN_NAME[pick], fr[pick], K.TOWN_NAME[run], fr[run], K.TOWN_NAME[last], fr[last]),
        "2. Protected owner-occupied single-family homes: %s %s; %s %s; %s %s" % (
            K.TOWN_NAME[pick], n(pr[pick]), K.TOWN_NAME[run], n(pr[run]), K.TOWN_NAME[last], n(pr[last])),
        "3. Total market value of those homes: %s $%.1f million; %s $%.1f million; %s $%.1f million" % (
            K.TOWN_NAME[pick], mv[pick], K.TOWN_NAME[run], mv[run], K.TOWN_NAME[last], mv[last]),
        "4. Average non-weather water claim payment: 2023 $%s; 2024 $%s; 2025 $%s" % (
            n(pay["2023"]), n(pay["2024"]), n(pay["2025"])),
        "5. Fire and lightning claims per 1,000 house-years, 2023 to 2025, on the homes the guide classes as "
        "unprotected: %.1f" % fi["unprotected"],
        "",
        "### %s" % K.CHART,
        "",
        "1. Horizontal bars of the three townships' frequencies, %s (%d) highlighted, %s %d and %s %d, against a "
        "dashed line at the book's own %d per 1,000 house-years" % (
            K.TOWN_NAME[pick], fr[pick], K.TOWN_NAME[run], fr[run], K.TOWN_NAME[last], fr[last],
            cx["book_frequency_per_1000"]),
        "",
    ]
    with open(os.path.join(task, "submission.md"), "w") as fh:
        fh.write("\n".join(lines))


if __name__ == "__main__":
    write(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE))
