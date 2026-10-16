"""Answers, figures.json and submission.md for task233, drafted from the analysis so no figure is typed."""
import json
import os

import numpy as np

import estim as E

ORDER = ["neet", "he"]
LONG = {"neet": "NEET rate", "he": "higher-education entry rate"}


def answers(R):
    flags = []
    for c in sorted(R["cells"], key=lambda c: (c["district"], ORDER.index(c["stat"]))):
        rate = R["A"][c["district"]]["right"][c["stat"]]
        flags.append(dict(district=c["district"], name=c["name"], stat=c["stat"], rate=round(rate, 1), rate_raw=rate,
                          shift=round(c["shift"], 2), shift_raw=c["shift"], flag=c["flag"], default_flag=c["default_flag"],
                          default=c["default"]))
    lists = {k: ["%s %s" % (f["name"], LONG[f["stat"]]) for f in flags if f["flag"] == k] for k in ("Suppressed", "Standard", "Caution")}
    bands = [dict(band=b, leavers=q["leavers"], neet=round(q["right"]["neet"], 1), he=round(q["right"]["he"], 1),
                  neet_raw=q["right"]["neet"], he_raw=q["right"]["he"]) for b, q in R["B"].items()]
    cells = {}
    for s in ORDER:
        cs = sorted(R["E"][s]["cells"], key=lambda c: (R["T"]["name"][c["district"]], c["band"]))
        cells[s] = [dict(c, name=R["T"]["name"][c["district"]]) for c in cs]
    f26 = R["f26"]
    return dict(flags=flags, lists=lists, bands=bands, cells=cells, n_cases=int(R["E"]["neet"]["n"]),
                odds_ratio={s: round(float(np.exp(R["E"][s]["delta"])), 2) for s in ORDER},
                gap={s: round(R["E"][s]["gap"] * 100, 1) for s in ORDER},
                slope={s: round(R["E"][s]["slope"], 2) for s in ORDER},
                ll={s: R["E"][s]["ll"] for s in ORDER},
                leavers=int(len(f26)), nonresp=int(f26["nonresp"].sum()),
                drawn=int(len(R["T"]["xw"])), unresolved=int((R["T"]["fu"]["outcome_code"] == "F99").sum()))


def figures(A, R):
    fig = {"call": {k: v for k, v in A["lists"].items()},
           "components": {"comparable_cases": A["n_cases"], "odds_ratio_neet": A["odds_ratio"]["neet"],
                          "odds_ratio_he": A["odds_ratio"]["he"], "calibration_slope_neet": A["slope"]["neet"],
                          "calibration_slope_he": A["slope"]["he"], "leavers_2026": A["leavers"], "nonrespondents_2026": A["nonresp"],
                          "followup_drawn": A["drawn"], "followup_unresolved": A["unresolved"],
                          "followup_late_returns": A["drawn"] - A["unresolved"] - A["n_cases"]},
           "rival": {"points_gap_neet": A["gap"]["neet"], "points_gap_he": A["gap"]["he"],
                     "default_wrong": sum(f["flag"] != f["default_flag"] for f in A["flags"])},
           "flags": {"%s %s" % (f["district"], f["stat"]): {"rate": f["rate"], "shift": f["shift"], "flag": f["flag"]} for f in A["flags"]},
           "bands": {b["band"]: {"leavers": b["leavers"], "neet": b["neet"], "he": b["he"]} for b in A["bands"]}}
    return fig


def submission(A):
    L = A["lists"]
    sup = [f for f in A["flags"] if f["flag"] == "Suppressed"]
    std = [f for f in A["flags"] if f["flag"] == "Standard"]
    names = lambda fs, stat: ", ".join(f["name"] for f in fs if f["stat"] == stat)
    hi = max(A["flags"], key=lambda f: abs(f["shift_raw"])); lo = min(A["flags"], key=lambda f: abs(f["shift_raw"]))
    mt = next(f for f in A["flags"] if f["name"] == "Mill Towns" and f["stat"] == "neet")
    ss = next(f for f in A["flags"] if f["name"] == "Southern Shore" and f["stat"] == "neet")
    wrong = [f for f in A["flags"] if f["flag"] != f["default_flag"]]
    dsup = [f for f in A["flags"] if f["default_flag"] == "Suppressed" and f["flag"] != "Suppressed"]
    out = []
    out.append("## Tags\n")
    out.append("> **Domain:** General Statistics & Data Science (missing data, censoring and measurement error).")
    out.append("> **Analytical objective:** Data Quality Monitoring & Alerting.\n")
    out.append("## 1. Final Recommendation\n")
    out.append("**Suppress the NEET rates of %s and the higher-education entry rates of %s; publish the NEET rates of %s and the "
               "higher-education entry rates of %s with the standard flag; publish the other %d statistics under caution.**\n"
               % (_and(names(sup, "neet")), _and(names(sup, "he")), _and(names(std, "neet")), _and(names(std, "he")), len(L["Caution"])))
    dstd = [f for f in A["flags"] if f["default_flag"] == "Caution" and f["flag"] == "Suppressed" and f["stat"] == "neet"]
    hsup = [f for f in A["flags"] if f["flag"] == "Suppressed" and f["stat"] == "he"]
    out.append("The 2025 follow-up, in five districts chosen across the island's range, found nonrespondents with %.2f "
               "times the odds of NEET and %.2f times the odds of higher education that their allocations gave them, in every "
               "district and band it covered, so each nonrespondent's allocation moves on the odds scale, shifting the district "
               "rates from %.2f points (%s %s) to %.2f (%s %s). Not a flat %.1f-point NEET gap per nonrespondent, which would "
               "suppress the NEET rates of %s, leave those of %s under caution and miss the higher-education suppressions; not a "
               "gap or a ratio per attainment band, which the follow-up's districts reject.\n"
               % (A["odds_ratio"]["neet"], A["odds_ratio"]["he"], lo["shift"], poss(lo["name"]), LONG[lo["stat"]], hi["shift"],
                  poss(hi["name"]), LONG[hi["stat"]], A["gap"]["neet"], _and(", ".join(f["name"] for f in dsup)),
                  _and(", ".join(f["name"] for f in dstd))))
    out.append("## 2. Critical Components\n")
    out.append("1. Comparable follow-up cases (resolved, still nonrespondents in the 2025 final file, one per case): **%s**"
               % format(A["n_cases"], ","))
    out.append("2. The follow-up's departure on the odds scale, one ratio across its districts and bands: NEET **%.2f**, higher "
               "education **%.2f**" % (A["odds_ratio"]["neet"], A["odds_ratio"]["he"]))
    out.append("3. Nonrespondents on the 2026 frame: **%s** of **%s** leavers\n" % (format(A["nonresp"], ","), format(A["leavers"], ",")))
    out.append("## 3. Step-by-Step Solution\n")
    out.append("1. Mapped each school on leaver_destinations_frame_2026.csv to its 2026 district in school_register.xlsx: %s "
               "leavers, %s of them nonrespondents carrying allocations." % (format(A["leavers"], ","), format(A["nonresp"], ",")))
    out.append("2. Joined nonresponse_followup_2025_outcomes.csv to leaver_destinations_final_2025.csv through "
               "followup_case_crosswalk_2025.csv, one outcome per case, keeping resolved cases whose leaver has no form in the final "
               "file (QS-4 section 6): %s of the %s cases drawn." % (format(A["n_cases"], ","), format(A["drawn"], ",")))
    out.append("3. Regressed each case's found destination (field report section 5) on the logit of its 2025 allocation: slope "
               "%.2f for NEET and %.2f for higher education, a constant shift on the odds scale, while the points gap (%.1f for "
               "NEET pooled) grows with the allocation." % (A["slope"]["neet"], A["slope"]["he"], A["gap"]["neet"]))
    out.append("4. Fitted the departure with each case's allocation on the logit scale as offset: odds ratio %.2f for NEET and "
               "%.2f for higher education." % (A["odds_ratio"]["neet"], A["odds_ratio"]["he"]))
    out.append("5. Moved each 2026 nonrespondent's NEET and higher-education allocation by those odds ratios and summed to the "
               "district (QS-4 section 3): shifts from %.2f (%s %s) to %.2f (%s %s) points."
               % (lo["shift"], lo["name"], LONG[lo["stat"]], hi["shift"], hi["name"], LONG[hi["stat"]]))
    out.append("6. Banded each unrounded shift under QS-4 section 4: %d suppressed, %d standard, %d caution."
               % (len(L["Suppressed"]), len(L["Standard"]), len(L["Caution"])))
    out.append("7. Headline rates (QS-4 section 2): returned forms read with activity_codes.csv, online returns on build 7 (the 2025 "
               "edition) with the order the 2025 final file's processed destinations show, plus allocations, over every leaver.")
    out.append("8. Banded leavers on state_exam_points_2026.csv's final points (methodology section 5) for the band table.\n")
    out.append("## 4. Deliverable Answers\n")
    out.append("### leaver_destinations_2026_quality_flags.xlsx\n")
    out.append("1. Each statistic's headline rate (per cent, one decimal) and flag, in district code order:")
    for d in sorted({f["district"] for f in A["flags"]}):
        fs = {f["stat"]: f for f in A["flags"] if f["district"] == d}
        out.append("   - %s (%s): NEET rate %.1f, %s; higher-education entry rate %.1f, %s"
                   % (fs["neet"]["name"], d, fs["neet"]["rate"], fs["neet"]["flag"].lower(), fs["he"]["rate"], fs["he"]["flag"].lower()))
    out.append("2. Attainment bands across the island (leavers; headline NEET and higher-education entry rates, per cent, one decimal):")
    for b in A["bands"]:
        out.append("   - %s: %s leavers, NEET rate %.1f, higher-education entry rate %.1f" % (b["band"], format(b["leavers"], ","), b["neet"], b["he"]))
    return "\n".join(out) + "\n"


def poss(name):
    return name + ("'" if name.endswith("s") else "'s")


def _and(s):
    parts = [p.strip() for p in s.split(",") if p.strip()]
    return parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " and " + parts[-1]


def write(task_dir, gen_dir, A, R):
    fig = figures(A, R)
    with open(os.path.join(gen_dir, "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1)
        fh.write("\n")
    with open(os.path.join(task_dir, "submission.md"), "w") as fh:
        fh.write(submission(A))
    return fig
