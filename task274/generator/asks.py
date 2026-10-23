"""The asks, from the pack's records, with the paths a careful analyst can take beside the golden's.

Ask A: for each county, the weighted percentage (interview weights, interviewed adults) whose supplements averaged at
least 400 IU and at least 1,000 IU of vitamin D a day over the 30 days before the interview.
Ask B: for each county, the unweighted interview and examination response rates of the sample persons aged 20 and
over, those found ineligible left out."""
from __future__ import annotations

from collections import defaultdict

INT_DONE = ("COMPLETE", "PARTIAL", "COMPLETE - PROXY")
NC = 8


def _r1(x):
    return round(100.0 * x + 1e-9, 1)


def supplement_avg(lines, mode="golden"):
    """Average IU a day per person. golden: a GENERIC line that repeats one of the person's label-database lines in
    strength per unit, days and units a day is the same bottle and counts once. cracker: every line counts.
    overclean: every GENERIC line dropped where the person also has a label-database line with vitamin D."""
    by = defaultdict(list)
    for x in lines:
        by[x["seqn"]].append(x)
    out = {}
    for s, xs in by.items():
        keep = []
        cat = [x for x in xs if x["pid"] != "GENERIC" and x["iu"] > 0]
        for x in xs:
            if x["pid"] == "GENERIC" and mode == "golden":
                twin = [c for c in cat if abs(c["iu"] - x["iu"]) < 1e-6 and c["days"] == x["days"] and c["qty"] == x["qty"]]
                if twin:
                    continue
            if x["pid"] == "GENERIC" and mode == "overclean" and cat:
                continue
            keep.append(x)
        out[s] = sum(x["iu"] * x["qty"] * x["days"] / 30.0 for x in keep)
    return out


def ask_a(status, lines, mode="golden", thresholds=(1000.0, 2000.0)):
    avg = supplement_avg(lines, mode)
    num = {t: [0.0] * NC for t in thresholds}
    den = [0.0] * NC
    for s in status:
        if s["int_status"] not in INT_DONE or s["wtint"] is None:
            continue
        den[s["county"]] += s["wtint"]
        a = avg.get(s["seqn"], 0.0)
        for t in thresholds:
            if a >= t - 1e-9:
                num[t][s["county"]] += s["wtint"]
    return {t: [_r1(num[t][c] / den[c]) for c in range(NC)] for t in thresholds}


def superseded(status, screeners):
    """Sample persons selected at a screening of a dwelling that was screened again later."""
    by_dw = defaultdict(list)
    for sid, (dw, d) in screeners.items():
        by_dw[dw].append((d, sid))
    old = set()
    for dw, xs in by_dw.items():
        xs.sort()
        for d, sid in xs[:-1]:
            old.add(sid)
    return {s["seqn"] for s in status if s["screener"] in old}, {dw for dw, xs in by_dw.items() if len(xs) > 1}


def ask_b(status, screeners, mode="golden"):
    drop, twice = superseded(status, screeners)
    dw_of = {sid: dw for sid, (dw, d) in screeners.items()}
    el = [0] * NC
    it = [0] * NC
    ex = [0] * NC
    for s in status:
        if s["int_status"].startswith("INELIGIBLE"):
            continue
        if mode == "golden" and s["seqn"] in drop:
            continue
        if mode == "overclean" and dw_of[s["screener"]] in twice:
            continue
        el[s["county"]] += 1
        it[s["county"]] += s["int_status"] in INT_DONE
        ex[s["county"]] += s["exam"] == "EXAMINED"
    return dict(interview=[_r1(it[c] / el[c]) for c in range(NC)], exam=[_r1(ex[c] / el[c]) for c in range(NC)],
                eligible=el, interviewed=it, examined=ex)
