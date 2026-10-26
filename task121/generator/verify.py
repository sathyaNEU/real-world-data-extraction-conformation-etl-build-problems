"""Independent verifier for task121: recomputes every graded figure in generator/figures.json from the cut pack with
the csv module alone, sharing no code with the golden's analysis or asks."""
import csv
import datetime as dt
import json
import math
import os
import statistics
import sys
from decimal import ROUND_HALF_UP, Decimal

HERE = os.path.dirname(os.path.abspath(__file__))


def _r(x, q):
    return float(Decimal(repr(float(x))).quantize(Decimal(q), rounding=ROUND_HALF_UP))


def rows(T, name):
    with open(os.path.join(T, name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def lt(s, fmt="%m/%d/%Y %H:%M:%S"):
    return dt.datetime.strptime(s, fmt)


def main(task):
    T = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    out = []

    def ok(label, got, want):
        out.append((label, got == want, "%s against %s" % (got, want)))

    months = [(2025, m) for m in range(9, 13)] + [(2026, m) for m in range(1, 9)]
    key = lambda ym: "%d-%02d" % ym
    split = dt.datetime(2026, 3, 1)
    # ---- the call's figures
    calls = rows(T, "cad_medical_calls_2025_2026.csv")
    worst = {}
    for e in rows(T, "epcr_patient_records_2025_2026.csv"):
        inc = e["incident_number"][:2] + "-" + e["incident_number"][2:]
        a = int(e["crew_acuity"].split(" ")[0])
        worst[inc] = min(a, worst.get(inc, 9))
    emp = {r["cad_login"]: r["employee_no"] for r in rows(T, "call_takers.csv")}
    shifts = {}
    for r in rows(T, "roster_shifts_worked_2025_2026.csv"):
        shifts.setdefault(r["employee_no"], []).append((lt(r["start"], "%m/%d/%Y %H:%M"),
                                                        lt(r["end"], "%m/%d/%Y %H:%M")))
    rest_of = {}
    for e_, ss in shifts.items():
        ss.sort()
        for i, (s, en) in enumerate(ss):
            rest_of[(e_, s)] = None if i == 0 else (s - ss[i - 1][1]).total_seconds() / 3600.0
    starts = {e_: [s for s, _ in ss] for e_, ss in shifts.items()}
    import bisect
    tally = {}
    for c in calls:
        if worst.get(c["incident_no"]) not in (1, 2):
            continue
        t = lt(c["call_answered"])
        if not (dt.datetime(2025, 9, 1) <= t < dt.datetime(2026, 9, 1)):
            continue
        e_ = emp[c["call_taker"]]
        i = bisect.bisect_right(starts[e_], t) - 1
        s, en = shifts[e_][i]
        assert s <= t < en
        rest = rest_of[(e_, s)]
        q = rest is not None and rest < 11
        k = ("after" if t >= split else "before", q)
        n, m = tally.get(k, (0, 0))
        tally[k] = (n + 1, m + (c["response"] == "COLD"))
        mk = (t.year, t.month)
        n, m = tally.get(mk, (0, 0))
        tally[mk] = (n + 1, m + (c["response"] == "COLD"))
    pct = lambda *ks: 100.0 * sum(tally[k][1] for k in ks) / sum(tally[k][0] for k in ks)
    ok("rate before", _r(pct(("before", False), ("before", True)), "0.1"), fig["rates"]["before"])
    ok("rate from March", _r(pct(("after", False), ("after", True)), "0.1"), fig["rates"]["from_march"])
    ok("from March, quick-return shifts", _r(pct(("after", True)), "0.1"),
       fig["components"]["from_march_on_quick_return_shifts"])
    ok("from March, rested shifts", _r(pct(("after", False)), "0.1"), fig["components"]["from_march_on_rested_shifts"])
    ok("rested shifts before", _r(pct(("before", False)), "0.1"), fig["components"]["rested_shifts_before"])
    for ym in months:
        ok("monthly %s" % key(ym), _r(pct(ym), "0.1"), fig["monthly_under_triage"][key(ym)])
    sb = sa = qb = qa = 0
    for e_, ss in shifts.items():
        for s, en in ss:
            if not (dt.date(2025, 9, 1) <= s.date() <= dt.date(2026, 8, 31)):
                continue
            rest = rest_of[(e_, s)]
            q = rest is not None and rest < 11
            if s.date() >= split.date():
                sa += 1
                qa += q
            else:
                sb += 1
                qb += q
    ok("quick-return share before", _r(100.0 * qb / sb, "0.1"), fig["components"]["quick_return_share_before"])
    ok("quick-return share from March", _r(100.0 * qa / sa, "0.1"), fig["components"]["quick_return_share_from_march"])
    # ---- Ask A: a call once, however many CAD incidents carry it (same phone call, answer second and call-taker),
    # at the earliest ambulance any of its incidents had
    first = {}
    for u in rows(T, "cad_unit_history_2025_2026.csv"):
        a = lt(u["assigned"])
        if u["incident_no"] not in first or a < first[u["incident_no"]]:
            first[u["incident_no"]] = a
    call_first = {}
    for c in calls:
        k = (c["che_call_id"], c["call_answered"], c["call_taker"])
        f = first[c["incident_no"]]
        if k not in call_first or f < call_first[k]:
            call_first[k] = f
    per = {}
    for (che, ans, taker), f in call_first.items():
        t = lt(ans)
        per.setdefault((t.year, t.month), []).append((f - t).total_seconds())
    for ym in months:
        v = sorted(per[ym])
        ok("Ask A %s" % key(ym), int(v[math.ceil(0.9 * len(v)) - 1]), fig["asks"]["A"]["p90_processing_s"][key(ym)])
    # ---- Ask B: QA7 keys minutes and seconds without the colon
    answered = {c["incident_no"]: lt(c["call_answered"]) for c in calls}
    per = {}
    for r in rows(T, "tcpr_arrest_reviews_2025_2026.csv"):
        if r["review_type"] != "Primary" or not r["first_compression_s"]:
            continue
        s = int(r["first_compression_s"])
        if r["reviewer"] == "QA7" and s >= 100:
            s = (s // 100) * 60 + s % 100
        t0 = lt(r["recording_started"]) + dt.timedelta(seconds=s)
        ans = answered[r["incident_no"]]
        per.setdefault((ans.year, ans.month), []).append((t0 - ans).total_seconds())
    for ym in months:
        ok("Ask B %s" % key(ym), int(_r(statistics.median(per[ym]), "1")),
           fig["asks"]["B"]["median_first_compression_s"][key(ym)])
    # ---- Ask C: a record arriving the second an earlier record on its trunk group from its number was released is
    # the call passed between positions, not a call arriving
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(T, "centre_reference.xlsx"), read_only=True)
    tg = {r[0] for r in wb["Trunk groups"].iter_rows(min_row=2, values_only=True) if str(r[1]).startswith("911")}
    che = rows(T, "che_call_detail_2025_2026.csv")
    ends = {(r["trunk_group"], r["ani"], r["released_utc"]) for r in che}
    per = {}
    for r in che:
        if r["trunk_group"] not in tg or r["abandoned"] == "Y":
            continue
        if (r["trunk_group"], r["ani"], r["arrived_utc"]) in ends:
            continue
        arr = dt.datetime.strptime(r["arrived_utc"], "%Y-%m-%dT%H:%M:%SZ")
        ans = dt.datetime.strptime(r["answered_utc"], "%Y-%m-%dT%H:%M:%SZ")
        cdt = dt.datetime(2025, 3, 9, 8) <= ans < dt.datetime(2025, 11, 2, 7) or \
            dt.datetime(2026, 3, 8, 8) <= ans < dt.datetime(2026, 11, 1, 7)
        loc = ans - dt.timedelta(hours=5 if cdt else 6)
        n, m = per.get((loc.year, loc.month), (0, 0))
        per[(loc.year, loc.month)] = (n + 1, m + ((ans - arr).total_seconds() <= 15))
    for ym in months:
        n, m = per[ym]
        ok("Ask C %s" % key(ym), _r(100.0 * m / n, "0.1"), fig["asks"]["C"]["answered_within_15s_pct"][key(ym)])
    bad = [o for o in out if not o[1]]
    for label, good, detail in out:
        if not good:
            print("FAIL  %s  %s" % (label, detail))
    print("verify: %d figures, %d differ: %s" % (len(out), len(bad), "PASS" if not bad else "FAIL"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)))
