"""task243 write-up: the answers every deliverable carries (one dictionary), submission.md and figures.json, every
number in the write-up taken from here."""
import json
import os

import numpy as np

import estim as E
import ggb as G


def answers(X, F):
    D = X["D"]
    cn = X["counts"]
    p1, p2 = E.census_arrays(D)
    dd = E.dg(D)
    nm = E.net_movers(D, "shift")
    lgus = []
    for c, s in zip(E.CODES, E.SHOW):
        raw = X["call"][c]["c"]
        comp, icpt, res = G.completeness(p1[c], p2[c], dd[c], E.T, nm[c], E.GOLD_RANGE[0], E.GOLD_RANGE[1])
        d = E.resident_deaths(D)
        age = E.age_years(d[d["lgu"] == c])
        lgus.append(dict(
            code=c, name=s, raw=raw, completeness=int(round(100 * raw)), interval=list(X["interval"][c]),
            alert=bool(X["call"][c]["alert"]), b1=round(X["ask_a"][c], 1), c1=round(X["ask_b"][c], 1),
            slope=round(1.0 / comp, 3), intercept=round(icpt, 4), closed=X["rungs"]["closed"][c],
            movers50=cn["net_movers_50plus"][c], pop15_2015=int(p1[c][3:].sum()), pop15_2020=int(p2[c][3:].sum()),
            reg_adult=int((age >= 15).sum()),
            rungs={k: X["rungs"][k][c] for k in X["rungs"]}))
    A = dict(lgus=lgus, counts=cn, designated=[r["name"] for r in lgus if r["alert"]],
             sets={k: [s for c, s in zip(E.CODES, E.SHOW) if X["rungs"][k][c] < E.ALERT] for k in X["rungs"]})
    return A


def three(e, m, s):
    if e == m == s:
        return "Esperanza, Magsaysay and Mabini each register %d per cent" % e
    return "Esperanza registers %d per cent, Magsaysay %d and Mabini %d" % (e, m, s)


def write(task, here, A):
    L = {r["name"]: r for r in A["lgus"]}
    des = A["designated"]
    figs = {}

    def f(key, val):
        figs[key] = val
        return val

    the = lambda n: ("the " + n) if n.startswith("City of") else n
    out = []
    out.append("# task243 submission\n")
    out.append("## Tags\n")
    out.append("**Domain:** Survey Research & Official Statistics (census, register and administrative data quality: a "
               "province's review of the completeness of death registration in the civil registry offices of its cities "
               "and municipalities, measured between two censuses).")
    out.append("**Analytical objective:** Data Quality Monitoring & Alerting (which offices' death registration falls "
               "below the 80 per cent completeness alert and goes into the first round of the 2024 Civil Registration "
               "Improvement Programme, with each office's timely birth registration and medical certification of deaths "
               "beside it).\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**Five offices go into the first round of CRIP 2024: the City of Santa Cruz, San Isidro, Libertad, San "
               "Luis and Del Carmen register fewer than 80 per cent of their residents' deaths at ages 15 and over "
               "between the 2015 and 2020 census reference dates (about %d, %d, %d, %d and %d per cent); the other seven "
               "register %d per cent or more and stay out.**\n" % (
                   L["City of Santa Cruz"]["completeness"], L["San Isidro"]["completeness"], L["Libertad"]["completeness"],
                   L["San Luis"]["completeness"], L["Del Carmen"]["completeness"],
                   f("min_out", min(r["completeness"] for r in A["lgus"] if not r["alert"]))))
    ep, mg, sf = L["Esperanza"], L["Magsaysay"], L["Mabini"]
    out.append("Completeness is the general growth balance of the two censuses' household population above each age "
               "against the deaths registered above it, carrying each office's net movement above each age from the 2020 "
               "census's residence five years earlier. Not the balance taken as closed, which reads the older residents "
               "who left Esperanza, Magsaysay and Mabini, most of them for elsewhere in the country, as deaths nobody "
               "registered and would send those three as well: with their movement in the balance %s.\n"
               % three(ep["completeness"], mg["completeness"], sf["completeness"]).replace("Esperanza, Magsaysay and Mabini ", "they "))
    out.append("## 2. Critical Components\n")
    five = [L[n] for n in des]
    out.append("1. The five offices register **%s** per cent of their residents' adult deaths (%s)." % (
        "%d to %d" % (min(r["completeness"] for r in five), max(r["completeness"] for r in five)),
        "; ".join("%s %d" % (r["name"], r["completeness"]) for r in five)))
    out.append("2. Esperanza, Magsaysay and Mabini register **%s** per cent once the residents who left are in the "
               "balance." % ("%d" % ep["completeness"] if ep["completeness"] == mg["completeness"] == sf["completeness"]
                             else "%d, %d and %d" % (ep["completeness"], mg["completeness"], sf["completeness"])))
    rest = [L[n] for n in ("Kalinawan City", "Quezon", "Rizal", "San Miguel")]
    out.append("3. Kalinawan City, Quezon, Rizal and San Miguel register **%d to %d** per cent." % (
        min(r["completeness"] for r in rest), max(r["completeness"] for r in rest)))
    out.append("")
    out.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Deaths (D1 in crvs_review_terms_of_reference_2023.pdf): certificates of death in "
        "crs_death_records_extract_20230331.csv, rows repeated exactly dropped, the province's residents placed by the "
        "residence as written (every spelling mapped, Santa Cruz's records before its 2019 charter included), a death "
        "registered at a second office counted once at its first registration (same names, sex, date of death and date "
        "of birth), dated 1 August 2015 to 30 April 2020, by five-year age group at death, unstated ages spread over the "
        "office's stated ages in proportion.",
        "Population: the household population by five-year age group in "
        "popcen2015_household_population_age_sex_kalinawan.xlsx and cph2020_household_population_age_sex_kalinawan.xlsx; "
        "the interval is %s years (days between the reference dates over %s)." % (f("interval_years", 4.75),
                                                                                f("year_days", 365.25)),
        "Movement: in cph2020_special_tabulation_pdpfp_kalinawan.csv each office's persons in 2020 who lived elsewhere "
        "on 1 May 2015 (NOT STATED spread in proportion to the stated rows of the same age group), less the persons "
        "anywhere in the country in 2020 who lived there then (ELSEWHERE IN THE PHILIPPINES included), by age group; "
        "each group's net movers split equally between that group and the next younger one (the age they moved at), "
        "times the interval over five years.",
        "Balance: for ages x from %d+ to %d+ by five, the persons reaching x per year (the geometric mean of the two "
        "age groups either side of x in each census, the two censuses' values combined geometrically, over five) per "
        "person-year above x (the interval times the geometric mean of the two censuses' populations above x), less the "
        "growth rate above x, plus the net movers above x per person-year, against the registered deaths above x per "
        "person-year; orthogonal fit (the slope is the ratio of the two rates' standard deviations); completeness is one "
        "over the slope." % (f("fit_lo", 15), f("fit_hi", 65)),
        "Accepted range: the same balance fitted from any lowest age of %d+ to %d+ to any highest of %d+ to %d+, with "
        "the movers kept at their census age, the movement not carried to the interval, a least-squares fit, the "
        "arithmetic mean of the two age groups for the persons reaching x, or completeness relative to either census, "
        "gives each office's range in the workbook answer; none of these readings crosses %d per cent." % (
            f("range_lo_min", 10), f("range_lo_max", 30), f("range_hi_min", 55), f("range_hi_max", 75),
            f("alert_line", 80)),
        "B1: births in crs_birth_records_extract_20230331.csv dated in 2022 to mothers resident in each city or "
        "municipality, rows repeated exactly dropped, each child counted once at its first registration (same child's "
        "names, sex, date of birth and mother; twins are two births), registered within %d days." % f("b1_days", 30),
        "C1: the residents' deaths dated in 2022, counted as in step 1; certified by a licensed physician when the "
        "certifier is an MD or attending physician or, for a certificate in the health office's name (MHO, CHO), when "
        "pho_health_office_clinical_staff_2019_2023.xlsx shows its signer in a physician's post on the date of death.",
        "Alert (D1 below %d per cent): %s go into the first round." % (
            80, ", ".join(the(n) for n in des[:-1]) + " and " + the(des[-1])),
    ]
    for i, s in enumerate(steps, 1):
        out.append("%d. %s" % (i, s))
    out.append("\n## 4. Deliverable Answers\n")
    out.append("### lcro_death_registration_completeness_2015_2020.xlsx\n")
    out.append("1. Completeness (whole per cent, accepted range in brackets) and the first round:")
    for r in A["lgus"]:
        key = r["name"].lower().replace("city of ", "").replace(" ", "_")
        out.append("   - %s: %d (%d to %d); %s" % (r["name"], f("comp_" + key, r["completeness"]),
                                                  f("lo_" + key, r["interval"][0]), f("hi_" + key, r["interval"][1]),
                                                  "goes in" if r["alert"] else "stays out"))
    out.append("2. Share of 2022 live births registered within 30 days (per cent): " +
               "; ".join("%s %.1f" % (r["name"], f("b1_" + r["code"], r["b1"])) for r in A["lgus"]) + ".")
    out.append("3. Share of residents' 2022 deaths certified by a licensed physician (per cent): " +
               "; ".join("%s %.1f" % (r["name"], f("c1_" + r["code"], r["c1"])) for r in A["lgus"]) + ".")
    out.append("\n### crvs_committee_note_2023.docx\n")
    out.append("4. One chart: every city and municipality's completeness against the 80 per cent line, the five going "
               "into the first round (the City of Santa Cruz, San Isidro, Libertad, San Luis and Del Carmen) marked.")
    text = "\n".join(out) + "\n"
    with open(os.path.join(task, "submission.md"), "w") as fh:
        fh.write(text)
    figs["call"] = des
    figs["lgus"] = {r["name"]: dict(completeness=r["completeness"], interval=r["interval"], alert=r["alert"], b1=r["b1"],
                                    c1=r["c1"], raw=round(r["raw"], 4), closed=round(r["closed"], 4),
                                    movers50=r["movers50"], reg_adult=r["reg_adult"]) for r in A["lgus"]}
    figs["rung_sets"] = A["sets"]
    with open(os.path.join(here, "figures.json"), "w") as fh:
        json.dump(figs, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    return figs
