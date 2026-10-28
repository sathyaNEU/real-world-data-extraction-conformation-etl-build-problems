"""Answers, figures.json and submission.md for task236, drafted from the analysis so no figure is typed."""
import json
import os

import estim as E
import golden as GD
import params as P

NAMES = {r[0]: r[1] for r in P.REGIONS}
KIND = {"poc": "point-of-care testing in general practice", "hours": "respiratory clinics open evenings and weekends",
        "panel": "multiplex panel in emergency departments", "merger": "two laboratories merged",
        "closure": "three drive-through clinics closed"}
FILES = None


def _and(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def f2(v):
    return "%.2f" % round(v, 2)


def answers(X, files):
    global FILES
    FILES = files
    reg = X["D"]["reg"].set_index("region_code")
    regions = []
    for code in E.EIGHT:
        d, cw, text = X["changes"][code]
        w = X["windows"][code]
        regions.append(dict(code=code, name=NAMES[code], entry=reg.loc[code, "entry"], change=text, date=d, week=cw,
                            flag=code in X["flags"], season=int(X["season"][code]), rate36=float(X["rate36"][code]),
                            rate36_raw=float(X["rate36_raw"][code]), ratio=float(X["ratio"][code]),
                            before=w["before"], after=w["after"], panel=X["panel"][code],
                            kind_short=KIND[P.CHANGES[code][1]]))
    R = E.rungs(X["D"], X["N"], X["changes"])
    c = X["cases"]
    tot = dict(cases=int(len(c)), eight=int(c.region.isin(E.EIGHT).sum()))
    notes = [
        "Flag rule: protocol CDB-FLU-03 section 4. A region's notified series is flagged from the report week of its "
        "change when the change moved the share of the region's influenza infections that are notified by more than a "
        "quarter either way, the four report weeks from the change week against the four before.",
        "Share notified: each region's notified cases over the sentinel network's influenza activity, both summed over "
        "each four weeks. Influenza activity is the network's influenza-like-illness rate (ILI consultations per 100,000 "
        "patients on the lists of the region's practices that made a return) times its swab positivity (the share of "
        "tested protocol swabs with influenza A or B detected), protocol SGP-2027.",
        "Cases: CDB-FLU-03 section 2, built from the gateway's results. A person's positive results collected within 14 "
        "days of the first positive specimen are one case, counted in the report week of that specimen and notified when "
        "the first result reporting influenza reached the gateway, preliminary or final.",
        "People: a specimen's preliminary and final reports that the gateway keyed to two people are one person, with "
        "that person's later results under either key; an infant whose results came under its mother's key is its own "
        "case. An age one year higher on a later specimen is the same person after a birthday.",
        "Regions: the residential postcode recorded on any of the case's results (a preliminary sent without the address "
        "is placed by its final report), under the concordance in force at the report (the postcodes moved on 28 June "
        "2027 counted in their new regions for the whole season); cases with no residential postcode on any result "
        "(blank, or 0000 at Northgate Diagnostics and Southern Districts Pathology) in the region of the requesting "
        "service's postcode; residents of other states not counted.",
        "Cut-off: cases notified by 09:00 on Monday 13 September 2027 (23:00 UTC on Sunday 12 September). Week 36 fills "
        "in after the cut-off; later notifications are counted from the week 37 report.",
        "Rates: estimated resident population at 30 June 2026 of the region's postcodes under the concordance in force.",
        "Source: notification gateway extract and sentinel network returns and swabs as at 06:30 on Tuesday 14 September "
        "2027. Prepared for sign-off by %s, surveillance epidemiologist." % P.PEOPLE["epi"],
    ]
    return dict(regions=regions, by={r["code"]: r for r in regions}, flags=X["flags"], rungs=R, tot=tot, notes=notes,
                cuts=X)


def figures(A):
    R = A["rungs"]
    by = A["by"]
    pos = R["positivity"]
    fl = [r for r in A["regions"] if r["flag"]]
    un = [r for r in A["regions"] if not r["flag"]]
    raw_up = [R["raw"][c] for c in E.EIGHT if c != "MS"]
    fig = {
        "call": [r["name"] for r in fl],
        "components": {
            "notified_before_after": {r["name"]: [r["before"], r["after"]] for r in A["regions"]},
            "share_notified_after_over_before": {r["name"]: f2(r["ratio"]) for r in A["regions"]},
        },
        "rivals": {
            "positivity_after_over_before": {NAMES[c]: "%.1f" % pos[c] for c in E.EIGHT},
            "positivity_false_flags": sorted(NAMES[c] for c in E.flagged(pos) - A["flags"]),
            "raw_rise_range": ["%.1f" % min(raw_up), "%.1f" % max(raw_up)],
            "unflagged_ratio_range": [f2(min(r["ratio"] for r in un)), f2(max(r["ratio"] for r in un))],
        },
        "steps": {"cases_built": A["tot"]["cases"], "cases_in_eight_regions": A["tot"]["eight"]},
        "deliverables": {
            GD.XLSX: [{"region": r["name"], "code": r["code"], "flag": "yes" if r["flag"] else "no",
                       "season_to_date": r["season"], "rate_week36": "%.1f" % r["rate36"]} for r in A["regions"]],
        },
        "cutoff": {"local": "09:00 Monday 13 September 2027", "utc": "23:00 Sunday 12 September 2027"},
        "report_week": 36, "weeks": [14, 26, 36], "window_weeks": 4, "line": "a quarter", "rate_base": "100,000",
        "change_weeks": {r["name"]: r["week"] for r in A["regions"]},
    }
    return fig


def submission(A):
    by = A["by"]
    R = A["rungs"]
    pos = R["positivity"]
    fl = [r for r in A["regions"] if r["flag"]]
    un = [r for r in A["regions"] if not r["flag"]]
    poc = [r for r in fl if P.CHANGES[r["code"]][1] == "poc"]
    ms = by["MS"]
    pos_false = [r for r in A["regions"] if r["code"] in E.flagged(pos) - A["flags"]]
    pos_missed = [r for r in A["regions"] if r["code"] in A["flags"] - E.flagged(pos)]
    raw_up = [R["raw"][c] for c in E.EIGHT if c != "MS"]
    lo, hi = min(r["ratio"] for r in un), max(r["ratio"] for r in un)
    F = FILES
    L = []
    L.append("# task236 submission\n")
    L.append("## Tags\n")
    L.append("**Domain:** Epidemiology & Public Health (disease surveillance and outbreak anomaly detection: a state health "
             "department's weekly influenza report, each health region's notified series read against the sentinel "
             "general practice network across a change in the region's testing).")
    L.append("**Analytical objective:** Data Quality Monitoring & Alerting (which regions' notified influenza series carry a "
             "testing-change break flag in the week 36 report of 2027).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Flag the notified influenza series of %s from the report weeks of their testing changes in the week 36 "
             "report, and not those of %s.**\n" % (_and(r["name"] for r in fl), _and(r["name"] for r in un)))
    L.append("Against the sentinel network's influenza activity, the share of influenza infections notified rose %s as "
             "point-of-care testing reached their general practices, and fell to %s of its level in %s when its "
             "drive-through clinics closed; in the other four regions it moved between %s and %s. Not positivity, which "
             "flags %s, whose positivity rose with the season and with who their changes brought to testing, and misses "
             "%s, whose point-of-care tests find influenza about as often as the referrals they replace. Not the notified "
             "counts alone, which rose %s to %s times in every region but %s as the season built. Not "
             "notifications per influenza-like-illness consultation or per sentinel swab positivity, which flag all "
             "eight: RSV filled the consultations before the change weeks, and positivity alone ignores how many people "
             "were ill.\n"
             % (_and("%s times in the %s" % (f2(r["ratio"]), r["name"]) if r["code"] in ("FN", "SC") else
                     "%s times in %s" % (f2(r["ratio"]), r["name"]) for r in poc),
                f2(ms["ratio"]), ms["name"], f2(lo), f2(hi), _and(r["name"] for r in pos_false),
                _and(r["name"] for r in pos_missed), "%.1f" % min(raw_up), "%.1f" % max(raw_up), ms["name"]))
    L.append("## 2. Critical Components\n")
    L.append("1. Notified cases in the four report weeks before each change and the four from it: %s" %
             "; ".join("%s **%s** and **%s**" % (r["name"], format(r["before"], ","), format(r["after"], ","))
                       for r in A["regions"]))
    L.append("2. Share of influenza infections notified, the four weeks from the change over the four before, against the "
             "sentinel network's influenza activity: %s" %
             "; ".join("%s **%s**" % (r["name"], f2(r["ratio"])) for r in A["regions"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Took every result in %s reporting influenza A or B, preliminary or final, and built cases under "
             "CDB-FLU-03 section 2 (%s): a person's positives collected within 14 days of the case's first positive "
             "specimen are one case, in the report week of that specimen, notified at the first such result's receipt, "
             "keys that share a specimen being one person and a key carrying an infant's and an adult's results two "
             "(an age one higher is a birthday); %s cases." % (F["res"], F["prot"], format(A["tot"]["cases"], ",")))
    L.append("2. Placed each case by the residential postcode recorded on any of its results (a preliminary sent without "
             "the address taking its final report's), under the concordance in force at the report (%s, rows with no "
             "effective_to), a case with none recorded on any result (blank or 0000) by the requesting service's "
             "postcode, and left out residents of other states: %s cases in the eight regions with a change in %s." %
             (F["conc"], format(A["tot"]["eight"], ","), F["reg"]))
    L.append("3. Counted each region's notified cases in the four report weeks before its change week and the four from it "
             "(section 4), all notified well before the week 36 cut-off: from %s (%s, before) to %s (%s, after)." %
             (format(by["TB"]["before"], ","), by["TB"]["name"], format(by["MN"]["after"], ","), by["MN"]["name"]))
    L.append("4. Measured each region's influenza activity by week from the sentinel network (%s): influenza-like-illness "
             "consultations per 100,000 patients on the lists of the practices that returned in %s, times the share of "
             "the tested protocol swabs in %s with influenza A or B detected." % (F["sprot"], F["ret"], F["sw"]))
    L.append("5. Divided notified cases by influenza activity, each summed over the four weeks, and took the weeks from the "
             "change over the weeks before: %s, beyond a quarter either way; %s, between %s and %s." %
             (_and("%s %s" % (r["name"], f2(r["ratio"])) for r in fl), _and(r["name"] for r in un), f2(lo), f2(hi)))
    L.append("6. Counted the season to date, cases with a first positive specimen in weeks 14 to 36 notified by 09:00 on "
             "Monday 13 September 2027 (23:00 UTC on Sunday 12 September; section 2): from %s (%s) to %s (%s)." %
             (format(by["TB"]["season"], ","), by["TB"]["name"], format(by["MN"]["season"], ","), by["MN"]["name"]))
    L.append("7. Divided each region's week 36 cases notified by the cut-off by the estimated resident population at 30 June "
             "2026 of its postcodes under the concordance in force (%s; section 3), per 100,000: from %s (%s) to %s (%s)." %
             (F["pop"], "%.1f" % by["MS"]["rate36"], by["MS"]["name"], "%.1f" % by["SC"]["rate36"], by["SC"]["name"]))
    L.append("8. Flagged %s from their change weeks and none of the other four, and charted each region's weekly notified "
             "cases with its change week and its influenza activity.\n" % _and(r["name"] for r in fl))
    L.append("## 4. Deliverable Answers\n")
    L.append("### %s\n" % GD.XLSX)
    L.append("1. One row per region in the file's order, season-to-date notified cases (weeks 14 to 36) whole, week 36 "
             "notified rate per 100,000 residents to one decimal:")
    for r in A["regions"]:
        L.append("   - %s (%s), change in report week %d: %s, %s notified cases season to date, %s per 100,000 in week 36" %
                 (r["name"], r["code"], r["week"], "flagged" if r["flag"] else "not flagged", format(r["season"], ","),
                  "%.1f" % r["rate36"]))
    L.append("")
    L.append("### %s\n" % GD.PNG)
    L.append("2. Eight panels, one per region, of weekly notified cases from week 26 to week 36 with the change week marked "
             "by a dashed line; %s titled as flagged with the weeks the flag covers in red, the other four in grey; the "
             "sentinel network's influenza activity drawn as a line on each panel's right axis." %
             _and(r["name"] for r in fl))
    return "\n".join(L) + "\n"


def write(task_dir, gen_dir, A):
    fig = figures(A)
    with open(os.path.join(gen_dir, "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1)
        fh.write("\n")
    with open(os.path.join(task_dir, "submission.md"), "w") as fh:
        fh.write(submission(A))
    return fig
