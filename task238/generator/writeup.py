"""task238 write-up: the answers object from the analysis, figures.json and submission.md, every figure emitted."""
import json
import math
import os

import estim as E
import params as P

NAMES = {x[0]: x[1] for x in P.INDEXES}
QLABEL = {"2027Q2": "second quarter 2027", "2027Q3": "third quarter 2027"}
LNAME = {"A": "letter A (web-first)", "B": "letter B (telephone-first)"}


def rng_text(w):
    lo = int(math.floor(w))
    return "%d to under %d points" % (lo, lo + 1)


def answers(X, files):
    s = X["s"]
    ix = []
    for code, name, item, kind, tol, th in P.INDEXES:
        r = E.routes(s, code, item, kind)
        ix.append(dict(code=code, name=name, item=item, kind=kind,
                       units="points (0 to 10)" if kind == "score" else "percentage points",
                       itt=X["parts"][code]["itt"], dw=100 * X["parts"][code]["dw"], effect=X["effects"][code], tol=tol,
                       widest=X["widest"][code], adj_widest=100 * tol / abs(r["adj"]), tsls=r["tsls"]))
    order = sorted(X["widest"], key=X["widest"].get)
    others = [c for c in order if c not in (X["bind"], X["runner"])]
    floor_others = min(int(math.floor(min(X["widest"][c], 100 * dict((i["code"], i["tol"]) for i in ix)[c] /
                                          abs(next(i["tsls"] for i in ix if i["code"] == c))))) for c in others)
    resp = []
    for q in P.QUARTERS:
        for L in ("A", "B"):
            v = X["response"][(q, L)]
            resp.append(dict(quarter=QLABEL[q], letter=L, letter_name=LNAME[L], eligible=v["eligible"],
                             completes=v["completes"], rate=round(v["rate"], 1), raw=v["rate"]))
    valid = [dict(code=code, name=name, item=item, web=X["valid"][code]["web"], cati=X["valid"][code]["cati"])
             for code, name, item, kind, tol, th in P.INDEXES]
    bind_tol = dict((i["code"], i["tol"]) for i in ix)[X["bind"]]
    lo = int(math.floor(X["widest"][X["bind"]]))
    return dict(band=X["band"], bind=X["bind"], bind_name=NAMES[X["bind"]], runner=X["runner"],
                runner_name=NAMES[X["runner"]], bind_range=rng_text(X["widest"][X["bind"]]),
                runner_range=rng_text(X["widest"][X["runner"]]), others_floor=floor_others,
                effect_lo=round(100 * bind_tol / (lo + 1), 2), effect_hi=round(100 * bind_tol / lo, 2), bind_tol=bind_tol,
                completes=len(s), indexes=ix, response=resp, valid=valid,
                rate_lo=min(r["rate"] for r in resp), rate_hi=max(r["rate"] for r in resp))


def _n(x):
    return format(x, ",")


def figures(A):
    f = {
        "call": {"band": A["band"], "bind": A["bind_name"], "runner": A["runner_name"]},
        "components": {"effect_lo": "%g" % A["effect_lo"], "effect_hi": "%g" % A["effect_hi"],
                       "bind_range": A["bind_range"], "runner_range": A["runner_range"],
                       "others_floor": A["others_floor"], "tolerance": "%.2f" % A["bind_tol"],
                       "departures": [A["band"], A["band"] + 1]},
        "steps": {"completes": _n(A["completes"]), "rate_lo": "%.1f" % A["rate_lo"], "rate_hi": "%.1f" % A["rate_hi"]},
        "response": {"%s %s" % (r["quarter"], r["letter"]): "%.1f" % r["rate"] for r in A["response"]},
        "valid": {r["code"]: [_n(r["web"]), _n(r["cati"])] for r in A["valid"]},
        "conventions": ["23:59", "UTC+13", "30 September", "9", "12", "August", "4.1", "4.3", "6", "18", "0.30"],
        "evidence_not_graded": {i["code"]: {"effect": round(i["effect"], 3), "widest": round(i["widest"], 3),
                                           "tsls": round(i["tsls"], 3)} for i in A["indexes"]},
    }
    return f


def submission(A):
    v = A["valid"]
    lines = ["# task238 submission", "",
             "## Tags", "",
             "**Domain:** Survey Research & Official Statistics (nonresponse, calibration and measurement-error "
             "adjustment: the mode-mix monitor of a household wellbeing tracker moving to web-first collection, set from "
             "each headline index's mode effect read through a randomized contact strategy test).",
             "**Analytical objective:** Data Quality Monitoring & Alerting (how far a quarter's web share may move before "
             "the tracker's published indexes are recalibrated).", "",
             "## 1. Final Recommendation", "",
             "**Run the Halvreth Wellbeing Tracker's mode-mix monitor at a band of %d percentage points of web share from "
             "the fourth quarter of 2027.**" % A["band"], "",
             "%s binds: its mode effect, read through the CST-27 letters' random allocation, is more than %g and at most "
             "%g percentage points, which keeps a %d-point departure of the web share within its %.2f-point tolerance and "
             "takes a %d-point departure outside it; %s is next at %s. Not %d points, the band a comparison of web with "
             "telephone completes gives even with every recorded characteristic held fixed: households chose their mode "
             "on traits the questions also measure, so that comparison counts who answered online as an effect of "
             "answering online. Not %d points, the band the letters' raw difference gives: it carries each index's mode effect only for the "
             "households a letter moved online." % (
                 A["bind_name"], A["effect_lo"], A["effect_hi"], A["band"], A["bind_tol"], A["band"] + 1,
                 A["runner_name"].lower(), A["runner_range"], A["band"] - 1, A["band"] + 2), "",
             "## 2. Critical Components", "",
             "1. %s's mode effect, read through the letters, is **more than %g and at most %g percentage points**, so its "
             "widest band within tolerance is **%s**, the narrowest of the twelve indexes." % (
                 A["bind_name"], A["effect_lo"], A["effect_hi"], A["bind_range"]),
             "2. %s is next, with a widest band of **%s**; every other index allows **%d points or more**." % (
                 A["runner_name"], A["runner_range"], A["others_floor"]), "",
             "## 3. Step-by-Step Solution", "",
             "1. Built the test's completes from mwt_cst27_web_returns.csv and mwt_cst27_cati_interviews.csv under the "
             "CST-27 plan's section 5 (mwt_cst27_plan.pdf): web returns reaching section 6 by 23:59 Halvreth time "
             "on the quarter's last day (UTC+13 on 30 September), telephone interviews coded C, an address once at its "
             "first-submitted complete with the CATI clock read as Halvreth time, returns giving an age under 18 left "
             "out as not from the person the letters ask for, and the staff-entry returns of 9 to 12 August taken as the telephone interviews mwt_cst27_close_out.docx "
             "describes: %s completes." % _n(A["completes"]),
             "2. Joined each complete to its letter in mwt_cst27_issued_addresses.csv and scored the twelve headline "
             "indexes on valid answers as mwt_questionnaire_codebook_v9.xlsx (sheet Indexes) sets out.",
             "3. Read each index's mode effect through the random letter allocation: its difference between the letter A "
             "and letter B completes divided by the letters' difference in the share of completes made online (two-stage "
             "least squares with the letter as the instrument sets the same band); %s's is more than %g and at most %g "
             "percentage points." % (A["bind_name"].lower(), A["effect_lo"], A["effect_hi"]),
             "4. Divided each index's continuity tolerance (mso_ms14_tracker_continuity_standard.pdf, Table 2) by its "
             "mode effect: %s's widest band is %s, %s's %s, every other index's %d points or more." % (
                 A["bind_name"].lower(), A["bind_range"], A["runner_name"].lower(), A["runner_range"],
                 A["others_floor"]),
             "5. Took the widest whole-point band within every tolerance (MS-14 section 5): %d points." % A["band"],
             "6. Took each letter's completes in each quarter over its eligible addresses (issued, less outcome codes 4.1 "
             "to 4.3, an address with a complete counted eligible whatever its code): response rates from %.1f to %.1f "
             "per cent." % (A["rate_lo"], A["rate_hi"]),
             "7. Counted each index's completes giving its question a valid answer, online and by telephone.",
             "8. Filed the band, the response rates and the valid answers in the workbook and charted each index's "
             "widest band against the band.", "",
             "## 4. Deliverable Answers", "",
             "### mwt_mode_mix_band_2027q4.xlsx", "",
             "1. The band: %d percentage points of web share, %s binding." % (A["band"], A["bind_name"].lower()),
             "2. Response rate under each letter in each quarter, one decimal place:"]
    for r in A["response"]:
        lines.append("   - %s, letter %s: %.1f per cent" % (r["quarter"], r["letter"], r["rate"]))
    lines.append("3. Completes giving each index's question a valid answer, online and by telephone:")
    for r in v:
        lines.append("   - %s (%s): %s online, %s by telephone" % (r["name"], r["code"], _n(r["web"]), _n(r["cati"])))
    lines += ["", "### mwt_mode_mix_band_2027q4.png", "",
              "4. Each index's widest band within its continuity tolerance against the %d-point band, %s marked as "
              "binding." % (A["band"], A["bind_name"].lower()), ""]
    return "\n".join(lines)


def write(task_dir, gen_dir, A):
    f = figures(A)
    with open(os.path.join(gen_dir, "figures.json"), "w") as fh:
        json.dump(f, fh, indent=1)
        fh.write("\n")
    with open(os.path.join(task_dir, "submission.md"), "w") as fh:
        fh.write(submission(A))
    return f
