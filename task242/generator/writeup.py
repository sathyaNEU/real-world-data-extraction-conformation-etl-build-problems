"""task242 owed figures (figures.json) and the submission, both emitted from the analysis, never typed."""
import datetime as dt
import json
import os

import numpy as np
import pandas as pd

import estim as E
import params as P

WORDS = {0: "No", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine",
         10: "Ten", 11: "Eleven", 12: "Twelve"}
BAND = 0.15                       # reasonable smoothings of the panel's curve agree on every estimated share to this


def fmt(n):
    return "{:,}".format(int(n))


def r1(x):
    return float(np.round(x + 1e-9, 1))


LEGIT = {"steps": dict(method="steps"), "bins": dict(method="bins"), "logistic": dict(method="logistic"),
         "kernel": dict(method="kernel"), "dedup": dict(dedup=True), "confirmed_only": dict(cls="CONFIRMED"),
         "zone_midpoint": dict(timing="midpoint")}


def answers(X, F):
    D = X["D"]
    g = X["golden"]
    flagged = E.flagged(g)
    cases_all = E.resident_cases(D)
    rr_all = E.zone_results(D)

    def old60(z):
        n = E.zone_counts(cases_all, z)
        days = np.arange(n.size)
        cd = ((rr_all[rr_all["zone"] == z]["collected"] - E.YEAR0).dt.days).values
        return float(np.mean([np.sum(n * (days < d) * ((d - days) > 60)) / np.sum(n * (days < d)) for d in cd]))
    zones = []
    for k, z in enumerate(E.ZONES):
        x = g[z]
        a = P.DAY0 + dt.timedelta(days=P.ZONES[k][3] - P.FIELD_HALF)
        b = P.DAY0 + dt.timedelta(days=P.ZONES[k][3] + P.FIELD_HALF)
        zones.append(dict(code=E.ROMAN[k], name=z, n=x["n"], a=x["a"], pub=r1(100 * x["p"]), est=r1(100 * x["A"]),
                          ratio=round(x["ratio"], 2), flag=x["flag"], se=round(x["se"], 3), bi=r1(X["breteau"][z]),
                          rr=r1(X["response"][z]), start=str(a), end=str(b), old60=int(round(100 * old60(z)))))
    c = E.panel_cases(D)
    groups = []
    for j, v in enumerate(E.VISITS):
        gi = np.array([np.argmin(np.abs(np.array(E.VISITS) - t)) for t in c["days"].values]) == j
        x = c[gi]
        groups.append(dict(visit=v, lo=int(x["days"].min()), hi=int(x["days"].max()), n=int(len(x)),
                           pos=int(x["pos"].sum()), se=round(float(x["pos"].mean()), 3),
                           mean_day=round(float(x["days"].mean()), 1)))
    pan = D["panel"]
    ctl = pan[pan["arm"] == "NEGATIVE CONTROL"]
    cases = E.resident_cases(D)
    used = cases[cases["t"] >= E.YEAR0]
    ll = D["cases"]
    V = {n: E.call(D, "variant", **kw) for n, kw in LEGIT.items()}
    spread = {n: dict(same=E.flagged(v) == flagged,
                      lo=round(min(v[z]["A"] / g[z]["A"] - 1 for z in E.ZONES), 3),
                      hi=round(max(v[z]["A"] / g[z]["A"] - 1 for z in E.ZONES), 3)) for n, v in V.items()}
    rungs = {}
    for r in ("pooled", "from5", "kit", "city", "peak", "median", "mean", "w60", "w90"):
        f = E.flagged(X[r])
        rungs[r] = dict(n=len(f), flagged=f, extra=sorted(set(f) - set(flagged)), missed=sorted(set(flagged) - set(f)),
                        max_ratio=round(max(X[r][z]["ratio"] for z in E.ZONES), 2),
                        min_ratio=round(min(X[r][z]["ratio"] for z in E.ZONES), 2))
    insp = D["insp"]
    v = D["visits"]
    s = D["sample"]
    lab = D["lab"]
    vv = v.drop_duplicates(["household_id", "start"]).sort_values(["household_id", "start"], kind="mergesort")
    last = vv.groupby("household_id")["visit_outcome"].last()
    final = s["household_id"].map(last)
    A = dict(
        files=F, zones=zones, flagged=flagged, sp=round(X["sp"], 4), groups=groups,
        controls=int(len(ctl)), controls_reactive=int((ctl["result_final"] == "REACTIVE").sum()),
        panel_cases=int(len(c)), panel_patients=int(c["patient_ref"].nunique()),
        se_single={k: round(v, 3) for k, v in X["se_single"].items()},
        line_rows=int(len(ll)), cases_used=int(len(used)),
        non_resident=int(ll["zone"].map(E.zone_of).isna().sum()),
        before_2027=int((cases["t"] < E.YEAR0).sum()),
        tested=int(sum(z["n"] for z in zones)), reactive=int(sum(z["a"] for z in zones)),
        spread=spread, band=BAND, rungs=rungs,
        max_unflagged=max((z for z in zones if not z["flag"]), key=lambda z: z["ratio"]),
        min_flagged=min((z for z in zones if z["flag"]), key=lambda z: z["ratio"]),
        insp_rows=int(len(insp)), insp_exact_dups=int(insp.duplicated().sum()),
        insp_locked=int((insp.drop_duplicates()["remarks"].fillna("") == "LOCKED").sum()),
        insp_houses=int(insp.drop_duplicates().pipe(lambda i: i[i["remarks"].fillna("") != "LOCKED"])["premise_id"].nunique()),
        renumber="2027-11-16",
        sampled=int(len(s)), visits_rows=int(len(v)), visits_resent=int(len(v) - len(vv)),
        vacant=int((final == 4).sum()), not_dwelling=int((final == 5).sum()), never_called=int(final.isna().sum()),
        lab_rows=int(len(lab)), lab_rejected=int((lab["condition"] != "ACCEPTED").sum()),
        responding=int(s["household_id"].isin(set(lab["barcode"].str.slice(3, 9))).sum()),
    )
    A["occupied"] = A["sampled"] - A["vacant"] - A["not_dwelling"]
    return A


def figures(A):
    Z = A["zones"]
    early = [g["se"] for g in A["groups"] if 7 <= g["visit"] <= 30]
    return {"panel_summary": {"early_lo_pct": int(round(100 * min(early))), "early_hi_pct": int(round(100 * max(early))),
                              "day75_pct": int(round(100 * [g["se"] for g in A["groups"] if g["visit"] == 75][0])),
                              "kit_window_days": [5, 60], "fixed_window_days": 90,
                              "scheduled_visits": [g["visit"] for g in A["groups"]], "breteau_per_houses": 100},
            "call": {"flagged": [z["name"] for z in Z if z["flag"]], "flagged_count": len(A["flagged"]), "zones": 12,
                     "tolerance": [round(P.TOL_LOW, 4), P.TOL_HIGH], "tolerance_text": ["two thirds", "one and a half"]},
            "components": {"estimated_flagged": {z["name"]: z["est"] for z in Z if z["flag"]},
                           "published_flagged": {z["name"]: z["pub"] for z in Z if z["flag"]},
                           "ratio_flagged": {z["name"]: z["ratio"] for z in Z if z["flag"]},
                           "max_unflagged": {"zone": A["max_unflagged"]["name"], "ratio": A["max_unflagged"]["ratio"]},
                           "min_flagged": {"zone": A["min_flagged"]["name"], "ratio": A["min_flagged"]["ratio"]},
                           "band": A["band"], "band_percent": int(round(100 * A["band"]))},
            "steps": {"tested": A["tested"], "reactive": A["reactive"], "panel_cases": A["panel_cases"],
                      "panel_patients": A["panel_patients"], "controls": A["controls"],
                      "controls_reactive": A["controls_reactive"], "specificity": A["sp"],
                      "visit_sensitivity": {str(g["visit"]): g["se"] for g in A["groups"]},
                      "visit_counts": {str(g["visit"]): g["n"] for g in A["groups"]},
                      "visit_days": {str(g["visit"]): [g["lo"], g["hi"]] for g in A["groups"]},
                      "single_sensitivity": A["se_single"], "line_rows": A["line_rows"], "cases_used": A["cases_used"],
                      "non_resident": A["non_resident"], "before_2027": A["before_2027"],
                      "effective_sensitivity": {z["name"]: z["se"] for z in Z},
                      "insp_rows": A["insp_rows"], "insp_exact_dups": A["insp_exact_dups"],
                      "insp_locked": A["insp_locked"], "insp_houses": A["insp_houses"], "renumber": A["renumber"],
                      "sampled": A["sampled"], "visits_rows": A["visits_rows"], "visits_resent": A["visits_resent"],
                      "vacant": A["vacant"], "not_dwelling": A["not_dwelling"], "never_called": A["never_called"],
                      "occupied": A["occupied"], "lab_rows": A["lab_rows"], "lab_rejected": A["lab_rejected"],
                      "responding": A["responding"]},
            "old_cases_pct": {z["name"]: z["old60"] for z in Z},
            "deliverables": {"published": {z["name"]: z["pub"] for z in Z}, "estimated": {z["name"]: z["est"] for z in Z},
                             "ratio": {z["name"]: z["ratio"] for z in Z},
                             "flag": {z["name"]: ("M" if z["flag"] else "") for z in Z},
                             "breteau": {z["name"]: z["bi"] for z in Z}, "response": {z["name"]: z["rr"] for z in Z},
                             "tested": {z["name"]: z["n"] for z in Z}, "reactive": {z["name"]: z["a"] for z in Z}},
            "rungs": dict(A["rungs"], spread=A["spread"])}


def _names(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def submission(A):
    F = A["files"]
    Z = A["zones"]
    fl = [z for z in Z if z["flag"]]
    other = [z for z in Z if not z["flag"]]
    rg = A["rungs"]
    L = []
    L.append("# task242 submission\n")
    L.append("## Tags\n")
    L.append("**Domain:** Epidemiology & Public Health (disease surveillance: a city's post-season dengue IgM household "
             "serosurvey and the quality flags on the infection shares published from it).")
    L.append("**Analytical objective:** Data Quality Monitoring & Alerting (which zones' published dengue infection "
             "shares carry the misclassification flag, with each zone's November larval index and the survey's "
             "household response rate beside them).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**%s of the 12 zones' published 2027 dengue infection shares carry the misclassification flag (M): %s. "
             "Their published IgM shares stand for well under two thirds of the residents infected since 1 January; "
             "the other %s zones' values go to the committee without the flag.**\n"
             % (WORDS[len(fl)], _names(["%s %s" % (z["code"], z["name"]) for z in fl]), WORDS[len(other)].lower()))
    L.append("The register says each zone's value, the share of tested residents with a reactive IgM, stands for the "
             "share of residents infected with dengue between 1 January 2027 and the collection of their specimen, and "
             "SOP-EPI-07 puts the M flag on when that share, estimated with allowance for the test's misclassification "
             "as the laboratory measured it, is more than one and a half times the published value or less than two "
             "thirds of it. The laboratory's verification panel shows the IgM assay finding %.0f to %.0f per cent of "
             "infections between one and four weeks after onset, %.0f per cent at about 75 days and almost none after "
             "four months. A zone's residents were therefore read through a sensitivity set by when its own epidemic "
             "ran against its fieldwork: the panel's curve by days since onset, averaged over the zone's cases by onset "
             "date from 1 January up to each specimen's collection. In the flagged zones %d to %d per cent of the year's "
             "cases up to each resident's collection had begun more than 60 days before it (in Vadakkupatti and "
             "Sengalur an August wave nearly as large as their November one), against at most %d per cent in the "
             "others, and the share infected is %.2f to %.2f times the published value; in the others it is at most "
             "%.2f times (%s). Correcting every zone with one sensitivity "
             "from the panel, pooled over all its sera (%.3f), from the fifth day of illness (%.3f) or over the kit's "
             "5 to 60 day window (%.3f), puts every zone between %.2f and %.2f times its published value and flags "
             "none. Reading each zone at the sensitivity of its median day since onset flags %s and misses %s, whose "
             "November waves were days old at fieldwork while their August waves were long past; at its peak day it "
             "flags %s, %s among them; at its mean day %s, %s among them, whose January wave drags the mean back; a "
             "fixed 90-day window flags %s; the city's pooled epidemic curve flags %s.\n"
             % (100 * min(g["se"] for g in A["groups"] if 7 <= g["visit"] <= 30),
                100 * max(g["se"] for g in A["groups"] if 7 <= g["visit"] <= 30),
                100 * [g for g in A["groups"] if g["visit"] == 75][0]["se"],
                min(z["old60"] for z in fl), max(z["old60"] for z in fl), max(z["old60"] for z in other),
                A["min_flagged"]["ratio"], max(z["ratio"] for z in fl), A["max_unflagged"]["ratio"],
                A["max_unflagged"]["name"], A["se_single"]["pooled"], A["se_single"]["from5"], A["se_single"]["kit"],
                min(rg["kit"]["min_ratio"], rg["pooled"]["min_ratio"]), max(rg["kit"]["max_ratio"], rg["pooled"]["max_ratio"]),
                WORDS[rg["median"]["n"]].lower(), _names(rg["median"]["missed"]), WORDS[rg["peak"]["n"]].lower(),
                _names(rg["peak"]["extra"]), WORDS[rg["mean"]["n"]].lower(), _names(rg["mean"]["extra"]),
                WORDS[rg["w90"]["n"]].lower(), WORDS[rg["city"]["n"]].lower()))
    L.append("## 2. Critical Components\n")
    for i, z in enumerate(fl, 1):
        L.append("%d. %s %s: published **%.1f** per cent; estimated share infected since 1 January **%.1f** per cent, "
                 "**%.2f** times the published value." % (i, z["code"], z["name"], z["pub"], z["est"], z["ratio"]))
    mu = A["max_unflagged"]
    L.append("%d. The largest multiple among the other %s zones is **%.2f** (%s %s: published %.1f, estimated %.1f per "
             "cent)." % (len(fl) + 1, WORDS[len(other)].lower(), mu["ratio"], mu["code"], mu["name"], mu["pub"], mu["est"]))
    L.append("")
    L.append("Estimated shares are accepted within %d per cent of these values: smoothing the panel's curve another "
             "reasonable way (steps, fixed bins, a fitted rise and fade, a kernel), counting confirmed cases only, "
             "dropping repeat notifications, or reading each zone at its middle fieldwork day moves no estimate by more "
             "than that, and every such reading flags the same %s zones." % (int(round(100 * A["band"])),
                                                                              WORDS[len(fl)].lower()))
    L.append("")
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Published values: %s and %s in %s (%s residents tested, %s reactive), which reproduce Table 1 of %s; the "
             "quantity each stands for is SERO-D1's in %s and the flag rule is SOP-EPI-07's M flag (%s)."
             % ("residents tested", "IgM reactive by zone", F["results"], fmt(A["tested"]), fmt(A["reactive"]),
                F["bulletin"], F["register"], F["standard"]))
    L.append("2. The assay's sensitivity: %d confirmed-case sera from %d patients in %s, days since onset taken as "
             "collected_on less onset_date, the final result (the repeat reading for a grey-zone first reading). By "
             "scheduled visit: %s. Specificity: %d of the %d control sera reactive, %.4f."
             % (A["panel_cases"], A["panel_patients"], F["panel"],
                "; ".join("day %d (%d to %d, %d sera) %.3f" % (g["visit"], g["lo"], g["hi"], g["n"], g["se"])
                          for g in A["groups"]), A["controls_reactive"], A["controls"], A["sp"]))
    L.append("3. The curve: the visits' sensitivities joined by straight lines at each visit's mean day since onset, "
             "zero at onset.")
    L.append("4. Each zone's 2027 epidemic: %s rows in %s; zone spellings mapped to the 12 zones, the %s notifications "
             "of non-residents left out, and resident cases with onset before 1 January 2027 (%s) left out: %s cases by "
             "onset date." % (fmt(A["line_rows"]), F["cases"], fmt(A["non_resident"]), fmt(A["before_2027"]),
                             fmt(A["cases_used"])))
    L.append("5. Effective sensitivity: for each tested resident, the curve at each day since onset averaged over the "
             "zone's cases with onset from 1 January up to the day before the specimen's collection, weighted by "
             "cases; each zone's mean over its tested residents: %s."
             % "; ".join("%s %.3f" % (z["name"], z["se"]) for z in Z))
    L.append("6. Estimated share infected since 1 January: (p + Sp - 1) / (Se + Sp - 1), with p the published share, "
             "Se the zone's effective sensitivity and Sp %.4f; its multiple of the published value; the M flag where the "
             "multiple is more than 1.5 or less than two thirds: %s zones." % (A["sp"], WORDS[len(fl)].lower()))
    L.append("7. Breteau index, November 2027 round: %s forms in %s, %d of them exact repeats of another row and dropped. "
             "Forms dated before %s carry the earlier ward number (the ward master's former_ward_nos); the zone is "
             "read from the premise's assessment number (its first two digits), which agrees with the ward map in "
             "force on each form's date. A LOCKED call is not an inspection (%d), and each house counts once, at its "
             "first inspection in the month (later forms for the same house are follow-ups after source reduction): "
             "%s houses. Positive containers per 100 houses, by zone."
             % (fmt(A["insp_rows"]), F["insp"], A["insp_exact_dups"], "16 November 2027", A["insp_locked"],
                fmt(A["insp_houses"])))
    L.append("8. Household response rate: the %s sampled households in %s; each household's last call in %s (%d "
             "submissions sent twice counted once); %d found vacant and %d not a dwelling are left out, and %d never "
             "called on stay in (%s households). A household responded when at least one member's specimen reached "
             "the laboratory (%s), whether tested or rejected: %s households. By zone."
             % (fmt(A["sampled"]), F["sample"], F["visits"], A["visits_resent"], A["vacant"], A["not_dwelling"],
                A["never_called"], fmt(A["occupied"]), F["lab"], fmt(A["responding"])))
    L.append("")
    L.append("## 4. Deliverable Answers\n")
    L.append("### dengue_igm_flag_review_2027.xlsx\n")
    L.append("1. Each zone: published share (per cent); estimated share infected since 1 January (per cent, accepted "
             "within %d per cent of the value); flag:" % int(round(100 * A["band"])))
    for z in Z:
        L.append("   - %s %s: %.1f; %.1f; %s" % (z["code"], z["name"], z["pub"], z["est"],
                                               "M" if z["flag"] else "no flag"))
    L.append("2. Breteau index for the November 2027 round, by zone: %s."
             % "; ".join("%s %.1f" % (z["name"], z["bi"]) for z in Z))
    L.append("3. Household response rate, by zone (per cent): %s."
             % "; ".join("%s %.1f" % (z["name"], z["rr"]) for z in Z))
    L.append("")
    L.append("### dengue_igm_flags_health_committee.pptx\n")
    L.append("4. One slide: each zone's published and estimated shares side by side, each zone's flag limits (two "
             "thirds and one and a half times the published value) marked, and the %s flagged zones (%s) marked M."
             % (WORDS[len(fl)].lower(), _names([z["name"] for z in fl])))
    return "\n".join(L) + "\n"


def write(task, here, A):
    fig = figures(A)
    with open(os.path.join(here, "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=2, sort_keys=True, default=str)
        fh.write("\n")
    with open(os.path.join(task, "submission.md"), "w") as fh:
        fh.write(submission(A))
    return fig
