"""Answers, figures.json and submission.md for task234, drafted from the analysis so no figure is typed."""
import json
import os

import estim as E

VIRUSES = ["Influenza", "RSV", "SARS-CoV-2"]
VLOW = {"Influenza": "influenza", "RSV": "RSV", "SARS-CoV-2": "SARS-CoV-2"}
WORDS = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
         11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen"}


def answers(X):
    labs = X["D"]["labs"].set_index("lab_id")
    order = [(r.lab_id, r.virus) for r in X["D"]["streams"].itertuples()]
    g = X["gold"]
    streams = []
    for k in order:
        rec, pos = X["recv"][k]
        streams.append(dict(lab_id=k[0], lab=labs.loc[k[0], "laboratory"], virus=k[1], received=int(rec),
                            positives=int(pos), positivity=round(100 * pos / rec, 1), est=int(round(g["est"][k])),
                            comp=round(100 * g["comp"][k]), comp_raw=g["comp"][k], escalate=k in g["esc"],
                            default_comp=X["routes"]["persist"]["comp"][k], default_esc=k in X["routes"]["persist"]["esc"]))
    week2 = []
    for k in order:
        n, t = X["A_counts"][k]
        week2.append(dict(lab_id=k[0], lab=labs.loc[k[0], "laboratory"], virus=k[1], received=n, report=t,
                          comp=round(100 * n / t, 1), comp_raw=100 * n / t))
    specimens = [dict(lab_id=l, lab=labs.loc[l, "laboratory"], specimens=int(X["B"][l])) for l in labs.index]
    esc = [s for s in streams if s["escalate"]]
    rest = [s for s in streams if not s["escalate"]]
    routes = {n: dict(esc=sorted(r["esc"]), wrong=sorted(r["esc"] ^ g["esc"])) for n, r in X["routes"].items()}
    c = E.week2_check(X)
    check = {"golden": round(100 * c[("pos",) + E.GOLDEN_MODEL][0], 1)}
    for k in ("peers", "received", "persist", "calendar", "poscount", "mean3", "trend"):
        check[k] = round(100 * c[k][0], 1)
    return dict(streams=streams, week2=week2, specimens=specimens, esc=esc, rest=rest, routes=routes, check=check,
                esc_labs=sorted({s["lab"] for s in esc}), min_rest=min(s["comp"] for s in rest),
                min_rest_stream=min(rest, key=lambda s: s["comp_raw"]),
                n_tests=sum(s["received"] for s in streams), labname=dict(labs["laboratory"]))


def figures(A):
    fig = {"call": ["%s %s" % (s["lab"], s["virus"]) for s in A["esc"]],
           "components": {"%s %s" % (s["lab"], s["virus"]): {"received": s["received"], "positivity": s["positivity"],
                                                             "expected_tests": s["est"], "completeness": s["comp"]}
                          for s in A["esc"]},
           "nearest_other": {"stream": "%s %s" % (A["min_rest_stream"]["lab"], A["min_rest_stream"]["virus"]),
                             "completeness": A["min_rest"]},
           "week3_tests": A["n_tests"],
           "default": {"escalated": len(A["routes"]["persist"]["esc"]), "wrong": len(A["routes"]["persist"]["wrong"])},
           "streams": {"%s %s" % (s["lab_id"], s["virus"]): {"received": s["received"], "positivity": s["positivity"],
                                                            "expected_tests": s["est"], "completeness": s["comp"],
                                                            "escalate": s["escalate"]} for s in A["streams"]},
           "week2": {"%s %s" % (w["lab_id"], w["virus"]): {"received_by_cutoff": w["received"], "report_tests": w["report"],
                                                          "completeness": w["comp"]} for w in A["week2"]},
           "week2_range": [min(w["comp"] for w in A["week2"]), max(w["comp"] for w in A["week2"])],
           "specimens": {s["lab"]: s["specimens"] for s in A["specimens"]},
           "line_per_cent": 80, "streams_count": len(A["streams"]), "week2_check_largest_miss": A["check"],
           "reports_span": {"first": "2022 week 40", "last": "2027 week 2"}}
    return fig


def _and(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _lab_short(name):
    return name.replace(" Laboratory Services", "").replace(" Laboratory", "")


SHORT = {"L01": "Tamsen Children's Hospital", "L02": "Ellery Memorial", "L03": "Wexmoor", "L04": "Corrigan Valley",
         "L05": "Brandmoor", "L06": "Bluestem", "L07": "Ridgeline", "L08": "Copperleaf", "L09": "Arbor Point",
         "L10": "Westmarch"}


def _streams_of(keys):
    """the wrong cells of a rung grouped by laboratory, in its words"""
    out = []
    for lab in sorted({k[0] for k in keys}):
        vs = [k[1] for k in sorted(keys) if k[0] == lab]
        out.append("%s's %s" % (SHORT[lab], "three streams" if len(vs) == 3 else _and(VLOW[v] for v in vs)))
    return _and(out)


def submission(A):
    L = A["labname"]
    esc = A["esc"]
    by = lambda lab: [s for s in esc if s["lab_id"] == lab]
    wx, wm = by("L03"), by("L10")
    rt = A["routes"]
    dw = rt["persist"]["wrong"]
    dcov = [k for k in dw if k[1] == "SARS-CoV-2"]
    dchh = [k for k in dw if k[0] == "L01"]
    assert len(dcov) + len(dchh) == len(dw)
    gold = {(s["lab_id"], s["virus"]) for s in esc}
    cal_miss = [k for k in rt["calendar"]["wrong"] if k in gold]
    cal_fp = [k for k in rt["calendar"]["wrong"] if k not in gold and k[1] != "SARS-CoV-2"]
    assert {k for k in rt["calendar"]["wrong"] if k[1] == "SARS-CoV-2"} == set(dcov)
    peer_miss = [k for k in rt["peers"]["wrong"] if k in {(s["lab_id"], s["virus"]) for s in esc}]
    peer_fp = [k for k in rt["peers"]["wrong"] if k not in {(s["lab_id"], s["virus"]) for s in esc}]
    pos_miss = rt["poscount"]["wrong"]
    comps = lambda ss: ", ".join("%d" % s["comp"] for s in ss)
    out = ["# task234 submission\n", "## Tags\n",
           "**Domain:** Epidemiology & Public Health (disease surveillance and outbreak anomaly detection: the completeness "
           "of a county's respiratory laboratory result feeds judged against the tests each laboratory ran, read from each "
           "stream's own positivity).",
           "**Analytical objective:** Data Quality Monitoring & Alerting (which result streams the laboratory liaison escalates "
           "under the feed completeness protocol for MMWR week 3 of 2027).\n",
           "## 1. Final Recommendation\n"]
    out.append("**Escalate the influenza, RSV and SARS-CoV-2 streams of %s and of %s for MMWR week 3 of 2027, and no other "
               "stream.**\n" % (L["L03"], L["L10"]))
    ms = A["min_rest_stream"]
    out.append("Against the tests each stream's own positivity says its laboratory ran in the week, Wexmoor's three streams "
               "(influenza, RSV, SARS-CoV-2) are %s per cent complete and Westmarch's %s, while every other stream is at %d "
               "per cent or more (%s's %s, the lowest). A lost result message drops a positive and a negative alike, so the "
               "week's received positivity is the laboratory's, and the laboratories' tests follow it; the protocol's "
               "week-2 check keeps that way, whose estimates for week 2 missed some stream by %.1f per cent at most, "
               "against %.1f for last week's report. Not last week's "
               "aggregate report as the week's tests, which escalates %d streams, %d of them complete streams whose epidemic "
               "fell in the week (the SARS-CoV-2 streams of %s laboratories and %s). Not the seasonal baseline of the same "
               "weeks in earlier winters, which escalates the same SARS-CoV-2 streams and %s and misses %s, this winter's "
               "influenza running later and higher than any before it. Not the other laboratories' change this week, which "
               "misses %s, the rural clinics' epidemics still rising, and escalates %s. Not the week's positives over last "
               "week's positivity, which misses %s, the lost messages taking their positives with them.\n"
               % (comps(wx), comps(wm), A["min_rest"], SHORT[ms["lab_id"]], VLOW[ms["virus"]], A["check"]["golden"],
                  A["check"]["persist"],
                  len(rt["persist"]["esc"]), len(dw), WORDS[len(dcov)], _streams_of(dchh), _streams_of(cal_fp),
                  _streams_of(cal_miss), _streams_of(peer_miss), _streams_of(peer_fp), _streams_of(pos_miss)))
    assert cal_miss and peer_fp and peer_miss and pos_miss
    out.append("## 2. Critical Components\n")
    out.append("1. Week-3 tests on the platform: %s **%s** (influenza, RSV, SARS-CoV-2), %s **%s**"
               % (SHORT["L03"], ", ".join(format(s["received"], ",") for s in wx), SHORT["L10"],
                  ", ".join(format(s["received"], ",") for s in wm)))
    out.append("2. Their week-3 positivity: %s **%s** per cent, %s **%s** per cent"
               % (SHORT["L03"], ", ".join("%.1f" % s["positivity"] for s in wx), SHORT["L10"],
                  ", ".join("%.1f" % s["positivity"] for s in wm)))
    out.append("3. Tests that positivity predicts: %s **%s**, %s **%s**"
               % (SHORT["L03"], ", ".join(format(s["est"], ",") for s in wx), SHORT["L10"],
                  ", ".join(format(s["est"], ",") for s in wm)))
    out.append("4. Completeness: %s **%s** per cent, %s **%s** per cent; every other stream **%d** per cent or more\n"
               % (SHORT["L03"], comps(wx), SHORT["L10"], comps(wm), A["min_rest"]))
    out.append("## 3. Step-by-Step Solution\n")
    out.append("1. Collapsed the week-3 messages in elr_respiratory_results_extract_2027-01-25.csv to tests under FCP-2 "
               "section 2 (one per laboratory, accession and virus; RV-FLUA and RV-FLUB one influenza test; a corrected "
               "result in place of the one it corrects; cancelled orders out; the week by the county date of the first "
               "release; facilities to laboratories by respiratory_stream_register.xlsx): %s tests across the 29 streams."
               % format(A["n_tests"], ","))
    out.append("2. Took each stream's week-3 positivity from those tests (a test is positive when its standing result is "
               "DETECTED): %s %s per cent, %s %s per cent."
               % (SHORT["L03"], ", ".join("%.1f" % s["positivity"] for s in wx), SHORT["L10"],
                  ", ".join("%.1f" % s["positivity"] for s in wm)))
    ck = A["check"]
    out.append("3. Set the ways of estimating week 2's tests that could have been made at its cutoff, 08:00 on 18 January, "
               "beside the week-2 reports of record (FCP-2 section 5): a Poisson regression of each stream's weekly tests on "
               "the week's positivity and a linear time trend over the reports of record before week 2 "
               "(lab_weekly_aggregate_reports.csv, the weeks holding Thanksgiving, Christmas Day and New Year's Day left out), "
               "read at the positivity of the stream's week-2 tests the platform held at the cutoff, missed some stream by "
               "%.1f per cent at most; those held tests themselves missed by %.1f and last week's report by %.1f."
               % (ck["golden"], ck["received"], ck["persist"]))
    out.append("4. Fitted the same regression on every report of record (2022 week 40 to 2027 week 2) and read it at the "
               "week-3 positivity: %s %s tests, %s %s."
               % (SHORT["L03"], ", ".join(format(s["est"], ",") for s in wx), SHORT["L10"],
                  ", ".join(format(s["est"], ",") for s in wm)))
    out.append("5. Divided each stream's tests on the platform by those tests (FCP-2 section 3) and escalated each stream "
               "below 80 per cent (section 4): %s at %s per cent, %s at %s, every other stream at %d or more."
               % (SHORT["L03"], comps(wx), SHORT["L10"], comps(wm), A["min_rest"]))
    lo, hi = min(A["week2"], key=lambda w: w["comp_raw"]), max(A["week2"], key=lambda w: w["comp_raw"])
    out.append("6. Week 2 (FCP-2 sections 3 and 5): receipt times before the state hub's broker migration "
               "(surveillance_platform_change_log.csv, 19 January 2027 06:00) are county time (read as UTC, most would come "
               "about six hours before the release of the result they carry) and later ones UTC, so the "
               "results each laboratory's interface held from Saturday evening and sent on Monday morning arrived after the "
               "08:00 cutoff on 18 January; "
               "tests whose first result arrived by the cutoff over the week-2 report of record give %.1f (%s %s) to %.1f "
               "(%s %s) per cent." % (lo["comp"], SHORT[lo["lab_id"]], VLOW[lo["virus"]], hi["comp"],
                                      SHORT[hi["lab_id"]], VLOW[hi["virus"]]))
    sp = sorted(A["specimens"], key=lambda s: s["specimens"])
    out.append("7. Specimens (FCP-2 section 6): distinct patient number and collection time among each laboratory's week-3 "
               "tests on the platform, whatever accessions its tests carry: %s (%s) to %s (%s)."
               % (format(sp[0]["specimens"], ","), SHORT[sp[0]["lab_id"]], format(sp[-1]["specimens"], ","),
                  SHORT[sp[-1]["lab_id"]]))
    out[-1] = out[-1] + "\n"
    out.append("## 4. Deliverable Answers\n")
    out.append("### respiratory_feed_escalations_2027-W03.xlsx\n")
    out.append("1. Escalation for week 3, each laboratory's streams:")
    for lab in [s["lab_id"] for s in A["specimens"]]:
        ss = [s for s in A["streams"] if s["lab_id"] == lab]
        out.append("   - %s: %s" % (L[lab], "; ".join("%s %s" % (VLOW[s["virus"]], "escalate" if s["escalate"] else "no")
                                                       for s in ss)))
    out.append("2. Week-2 completeness, per cent to one decimal place:")
    for lab in [s["lab_id"] for s in A["specimens"]]:
        ws = [w for w in A["week2"] if w["lab_id"] == lab]
        out.append("   - %s: %s" % (L[lab], "; ".join("%s %.1f" % (VLOW[w["virus"]], w["comp"]) for w in ws)))
    out.append("3. Specimens tested in week 3 with results on the platform:")
    for s in A["specimens"]:
        out.append("   - %s: %s" % (s["lab"], format(s["specimens"], ",")))
    out.append("\n### respiratory_feed_completeness_2027-W03.png\n")
    out.append("4. Horizontal bar chart of the 29 streams' week-3 completeness against the 80 per cent line, grouped by "
               "laboratory: the six bars of %s and %s below the line, every other bar above it." % (L["L03"], L["L10"]))
    return "\n".join(out) + "\n"


def write(task_dir, gen_dir, A):
    fig = figures(A)
    with open(os.path.join(gen_dir, "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1)
        fh.write("\n")
    with open(os.path.join(task_dir, "submission.md"), "w") as fh:
        fh.write(submission(A))
    return fig
