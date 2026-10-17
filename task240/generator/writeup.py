"""task240 owed figures (figures.json) and the submission, both emitted from the analysis, never typed."""
import json
import os

import pandas as pd

import estim as E
import params as P

REGIONS = [(r[0], r[1]) for r in P.REGIONS]
NAME = dict(REGIONS)
INDS = list(P.INDICATORS)
IND_NAME = dict(INDS)
WORDS = {4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten", 11: "Eleven", 12: "Twelve", 13: "Thirteen", 14: "Fourteen",
         15: "Fifteen"}
NORTH = ["R01", "R02", "R03", "R04"]


def fmt(n):
    return "{:,}".format(int(n))


def r1(x):
    return float("%.1f" % x)


def answers(X, F):
    T = X["T"]
    cv = {r: {} for r, _ in REGIONS}
    est = {r: {} for r, _ in REGIONS}
    fixed = {r: {} for r, _ in REGIONS}
    for _, row in T.iterrows():
        cv[row["region"]][row["ind"]] = r1(row["golden"])
        est[row["region"]][row["ind"]] = r1(row["est"] / 1000.0)
        fixed[row["region"]][row["ind"]] = r1(row["fixed"])
    order = [y for y, _ in INDS]
    warned = sorted(X["warned"], key=lambda k: (k[0], order.index(k[1])))
    df = X["df"]
    extra = [k for k in X["routes"]["fixed"] if k not in warned]
    A = dict(
        files=F, cv=cv, est=est, fixed=fixed, warned=warned, warned_set=set(warned), n_warned=len(warned),
        n_estimates=len(T), n_fixed=len(X["routes"]["fixed"]), fixed_extra=extra,
        n_srs=len(X["routes"]["srs"]), n_kish=len(X["routes"]["kish"]), n_region_ps=len(X["routes"]["region_ps"]),
        adults=int(len(df)), households=int(df["hh_id"].nunique()), cells=int(df.groupby(["region", "ag", "sex"]).ngroups),
        psus=int(df["psu"].nunique()), strata=int(df["stratum"].nunique()),
        rr={r: r1(v) for r, v in X["rr"].items()}, calls={r: int(v) for r, v in X["calls"].items()},
        warned_min=r1(min(T.loc[[(r, y) in set(warned) for r, y in zip(T["region"], T["ind"])], "golden"])),
        unwarned_max=r1(max(T.loc[[(r, y) not in set(warned) for r, y in zip(T["region"], T["ind"])], "golden"])),
        unwarned_max_key=max(((r, y) for r, y in zip(T["region"], T["ind"]) if (r, y) not in set(warned)),
                             key=lambda k: float(T.loc[(T["region"] == k[0]) & (T["ind"] == k[1]), "golden"].iloc[0])),
        pen_north_min=min(cv[r]["PEN"] for r in NORTH), pen_north_max=max(cv[r]["PEN"] for r in NORTH),
        issued=int(len(X["iss"])),
    )
    A["rr_min"] = min(A["rr"].values())
    A["rr_max"] = max(A["rr"].values())
    hh_ids = set(X["hh"]["hh_id"])
    last = X["out"].sort_values(["address_id", "issue_no"]).groupby("address_id")["outcome_code"].last()
    A["late"] = int(sum(1 for a in hh_ids if last.get(a) != 110))
    A["unworked"] = int(len(set(X["iss"]["address_id"]) - set(X["out"]["address_id"])))
    psu_reg = dict(zip(X["hh"]["psu"], X["hh"]["region"]))
    moved = X["iss"].drop_duplicates("psu")
    A["moved_psus"] = int(sum(1 for p, c in zip(moved["psu"], moved["region_code"]) if psu_reg.get(p, c) != c))
    o = X["out"].sort_values(["address_id", "issue_no"]).groupby("address_id")["outcome_code"].last().astype(float)
    o[o.index.isin(hh_ids)] = 110.0
    base = X["iss"][["address_id"]].merge(o.rename("final").reset_index(), on="address_id", how="left")["final"]
    A["e"] = float(base.isin(E.ELIGIBLE).sum() / base.isin(E.ELIGIBLE + E.INELIGIBLE).sum())
    c = X["cr"][X["cr"]["event_type"].isin(E.CALL_TYPES)]
    A["copies"] = int(c.duplicated(["address_id", "issue_no", "event_time", "event_type", "result",
                                    "interviewer_id"]).sum())
    # the fieldwork table's counts behind each rate, every address in the region its PSU lies in
    reg = X["iss"]["psu"].map(lambda p: psu_reg.get(p)).fillna(X["iss"]["region_code"])
    fr = pd.DataFrame({"region": reg.values, "final": X["iss"][["address_id"]].merge(
        o.rename("final").reset_index(), on="address_id", how="left")["final"].values})
    A["issued_by_region"] = {r: int(n) for r, n in fr.groupby("region").size().items()}
    A["interviews_by_region"] = {r: int((g["final"] == 110).sum()) for r, g in fr.groupby("region")}
    el = fr["final"].isin(E.ELIGIBLE).sum()
    un = (~fr["final"].isin(E.ELIGIBLE + E.INELIGIBLE)).sum()
    A["rr_all"] = r1(100 * (fr["final"] == 110).sum() / (el + A["e"] * un))
    A["calls_all"] = int(sum(A["calls"].values()))
    A["n_region"] = {r: int(n) for r, n in df.groupby("region").size().items()}
    return A


def figures(A):
    f = {"call": {"warned": ["%s %s" % k for k in A["warned"]], "warned_count": A["n_warned"],
                  "estimates": A["n_estimates"], "line": P.LINE},
         "cited_sections": ["2.1", "2.3", "3.1", "3.2", "3.3", "4.1", "4.2", "4.3", "5.1"],
         "components": {"pension_north_cv": {r: A["cv"][r]["PEN"] for r in NORTH},
                        "rent_cv": {r: A["cv"][r]["RENT"] for r in ("R01", "R03")},
                        "warned_min_cv": A["warned_min"], "unwarned_max_cv": A["unwarned_max"]},
         "steps": {"adults": A["adults"], "households": A["households"], "cells": A["cells"], "psus": A["psus"],
                   "strata": A["strata"], "age_groups": [16, 29, 30, 49, 50, 64, 65], "issued": A["issued"],
                   "late_interviews": A["late"], "unworked": A["unworked"], "moved_psus": A["moved_psus"],
                   "e": round(A["e"], 4), "copies": A["copies"], "regions": 12, "indicators": 4},
         "deliverables": {"cv": A["cv"], "estimates_thousands": A["est"], "response_rate": A["rr"], "calls": A["calls"],
                          "pension_north_range": [A["pen_north_min"], A["pen_north_max"]],
                          "rr_range": [A["rr_min"], A["rr_max"]], "issued_by_region": A["issued_by_region"],
                          "interviews_by_region": A["interviews_by_region"], "rr_all_regions": A["rr_all"],
                          "calls_all_regions": A["calls_all"], "adults_by_region": A["n_region"]},
         "rungs": {"fixed_weights_warned": A["n_fixed"], "fixed_weights_extra": ["%s %s" % k for k in A["fixed_extra"]],
                   "fixed_cv": A["fixed"], "srs_warned": A["n_srs"], "kish_warned": A["n_kish"],
                   "region_ratio_warned": A["n_region_ps"]}}
    return f


def submission(A):
    F = A["files"]
    W = A["warned"]
    by_ind = {}
    for r, y in W:
        by_ind.setdefault(y, []).append(r)
    L = []
    L.append("# task240 submission\n")
    L.append("## Tags\n")
    L.append("**Domain:** Survey Research & Official Statistics (nonresponse, calibration and measurement-error "
             "adjustment: the sampling error of a household survey's post-stratified regional estimates, judged against "
             "the commissioning statistics branch's low-reliability line).")
    L.append("**Analytical objective:** Data Quality Monitoring & Alerting (which of the wave's published estimates carry "
             "the low-reliability warning in the quality report delivered with the tables).\n")
    L.append("## 1. Final Recommendation\n")
    parts = []
    for y, label in INDS:
        if y in by_ind:
            regs = by_ind[y]
            parts.append("%s in %s" % (label.lower(), ", ".join("%s (%s)" % (NAME[r], r) for r in regs)))
    L.append("**%s of the %d estimates carry the low-reliability warning: %s. The other %d, the public pension "
             "estimates of all twelve regions among them, do not.**\n"
             % (WORDS[A["n_warned"]], A["n_estimates"], "; ".join(parts), A["n_estimates"] - A["n_warned"]))
    L.append("Each warned estimate's coefficient of variation is %.1f per cent or more and every other estimate's %.1f "
             "or less, against the line of %.1f. The final weights were post-stratified within health region, age group "
             "and sex, so the estimate as published is a post-stratified estimator, and its Taylor linearisation is "
             "each adult's departure from the weighted rate of their cell, not the adult's own weighted value. Treating "
             "the final weights as fixed instead warns %d estimates, adding %s: the number receiving a public pension "
             "is almost fixed by the age and sex totals the weights were scaled to, and the fixed-weight error counts "
             "the weights' spread as sampling error.\n"
             % (A["warned_min"], A["unwarned_max"], P.LINE, A["n_fixed"],
                ", ".join("%s %s" % k for k in A["fixed_extra"])))
    L.append("## 2. Critical Components\n")
    L.append("1. The public pension estimates of the four northern regions carry no warning: coefficients of variation "
             "%s." % ", ".join("**%.1f** (%s)" % (A["cv"][r]["PEN"], r) for r in NORTH))
    L.append("2. The private renting estimates of Far North (R01) and North East (R03) carry no warning: **%.1f** and "
             "**%.1f**." % (A["cv"]["R01"]["RENT"], A["cv"]["R03"]["RENT"]))
    L.append("3. The %s warned estimates' coefficients of variation are all **%.1f or more**; the highest of the other "
             "%d is **%.1f**.\n" % (WORDS[A["n_warned"]].lower(), A["warned_min"], A["n_estimates"] - A["n_warned"],
                                   A["unwarned_max"]))
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Built the responding adults: the members aged 16 and over in %s joined to %s on household and person "
             "number, and to %s on household for health region, stratum, PSU and the household answers: %s adults in "
             "%s households, %d PSUs in %d strata." % (F["members"], F["weights"], F["households"], fmt(A["adults"]),
                                                    fmt(A["households"]), A["psus"], A["strata"]))
    L.append("2. Coded the four estimates from %s (sheet Published tables): pension = 1, tenure = 3 for every adult in "
             "the household, care = 1, arrears = 1 for every adult in the household; don't know and refused not "
             "counted, proxy answers counted (QS-7 2.3)." % F["codebook"])
    L.append("3. Estimated each of the %d totals with the final weights (QS-7 2.1)." % A["n_estimates"])
    L.append("4. Read %s: the final weights are the design weights post-stratified within the %d cells of health "
             "region, age group (16 to 29, 30 to 49, 50 to 64, 65 and over, from age at interview) and sex. The "
             "estimate as published (QS-7 3.2) is therefore a post-stratified total, and its Taylor linearisation is "
             "z = w(y - p), where p is the weighted rate of the adult's cell." % (F["note"], A["cells"]))
    L.append("5. Totalled z by PSU, took each stratum's with-replacement variance (n_h/(n_h - 1) times the sum of "
             "squared deviations of the PSU totals from their stratum mean), summed over the region's strata, and "
             "divided the standard error by the unrounded estimate (QS-7 3.1).")
    L.append("6. Applied the %.1f per cent line (QS-7 3.3): %d estimates carry the warning. The same %d follow from a "
             "delete-one-PSU jackknife with every replicate post-stratified again; with the final weights held fixed "
             "the linearisation warns %d." % (P.LINE, A["n_warned"], A["n_warned"], A["n_fixed"]))
    L.append("7. Response rates (QS-7 4.1 and 4.2): every address in %s (%s) in the health region its PSU lies in, read "
             "from the PSU's region in %s (the master-sample code in %s predates the 2025 boundary review for %d PSUs); "
             "each address's outcome from its last issue in %s, every household in %s taken as a full interview (the "
             "30 September extract still holds %d of them under an earlier status: their interviews reached the office "
             "after it was taken, as the call records' receipt times show), and the %d issued addresses absent from the "
             "extract, each with only its advance letter in the call records, counted as eligibility not established; "
             "e = %.4f across the wave."
             % (F["issued"], fmt(A["issued"]), F["households"], F["issued"], A["moved_psus"], F["outcomes"], F["households"],
                A["late"], A["unworked"], A["e"]))
    L.append("8. Calls (QS-7 4.3): the visit and telephone records in %s for every issue of each address with a full "
             "interview, a call a tablet wrote twice (same address, issue, time, type, result and interviewer, %d copies) "
             "counted once, by health region." % (F["calls"], A["copies"]))
    L.append("")
    L.append("## 4. Deliverable Answers\n")
    L.append("### hrs27_quality_report.xlsx\n")
    L.append("1. Each estimate's coefficient of variation (per cent) and warning:")
    for r, name in REGIONS:
        L.append("   - %s (%s): %s" % (name, r, "; ".join(
            "%s %.1f%s" % (IND_NAME[y].lower(), A["cv"][r][y], ", warned (E)" if (r, y) in A["warned_set"] else "")
            for y, _ in INDS)))
    L.append("2. Each health region's response rate (per cent) and calls to its addresses with a full interview:")
    for r, name in REGIONS:
        L.append("   - %s (%s): %.1f, %s calls" % (name, r, A["rr"][r], fmt(A["calls"][r])))
    L.append("")
    L.append("### hrs27_quality_note.docx\n")
    L.append("3. The note the Branch publishes with the tables, naming the %s warned estimates with their coefficients "
             "of variation: %s." % (WORDS[A["n_warned"]].lower(), "; ".join(
                 "%s %s %.1f" % (r, IND_NAME[y].lower(), A["cv"][r][y]) for r, y in W)))
    return "\n".join(L) + "\n"


def write(task, here, A):
    fig = figures(A)
    with open(os.path.join(here, "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=2, sort_keys=True, default=str)
        fh.write("\n")
    with open(os.path.join(task, "submission.md"), "w") as fh:
        fh.write(submission(A))
    return fig
