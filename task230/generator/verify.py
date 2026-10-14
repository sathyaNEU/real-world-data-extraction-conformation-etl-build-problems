"""Independent verifier: reads only the files under target/ (csv module and pyarrow, no generator state, no pandas) and
recomputes the call, every group's coding bias, the release population by route and both asks, then compares them with
figures.json."""
import csv
import json
import os
import sys
from datetime import date, datetime

import pyarrow.parquet as pq

GROUPS = ["11", "12", "13", "14", "21", "22", "23", "24", "25", "26", "31", "32", "33", "34", "35", "41", "42", "43", "44",
          "51", "52", "53", "54", "61", "62", "63", "71", "72", "73", "74", "75", "81", "82", "83", "91", "92", "93", "94",
          "95", "96"]
NAMES = {"O": "online self-response", "P": "paper self-response", "FS": "follow-up, household member",
         "FP": "follow-up, proxy"}


def rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        yield from csv.DictReader(f)


def main(target, figures_path):
    fig = json.load(open(figures_path))
    p = lambda n: os.path.join(target, n)
    # each questionnaire's closing call
    closing = {}
    for r in rows(p("field_visit_log_jun_oct_2026.csv")):
        if r["outcome_code"] in ("10", "20") and r["questionnaire_id"]:
            closing.setdefault(r["questionnaire_id"], r["outcome_code"])
    route, writeins = {}, {}
    for r in rows(p("census2026_receipt_register.csv")):
        m = r["capture_mode"]
        route[r["doc_id"]] = {"ONLINE": "O", "PAPER": "P"}.get(m) or ("FP" if closing.get(r["questionnaire_id"]) == "20" else "FS")
        writeins[r["doc_id"]] = int(r["occupation_writeins"])
    released = {k: 0 for k in NAMES}
    for d, n in writeins.items():
        released[route[d]] += n
    t = pq.read_table(p("census2026_occupation_coding_extract.parquet"), columns=["doc_id", "coding_path", "coder_id",
                                                                                   "coded_at"]).to_pydict()
    coded = {k: 0 for k in NAMES}
    for d in t["doc_id"]:
        coded[route[d]] += 1
    still = {k: released[k] - coded[k] for k in NAMES}
    # the study: weighted net counts by route, under the rule each part is coded under
    K = {g: i for i, g in enumerate(GROUPS)}
    acc = {k: {"t": [0.0] * 40, "do": [0.0] * 40, "dn": [0.0] * 40} for k in NAMES}
    for r in rows(p("census2026_coding_quality_study.csv")):
        a = acc[route[r["doc_id"]]]
        w = float(r["selection_interval"])
        ref = K[r["reference_code"][:2]]
        prod = K[r["production_code"][:2]]
        new = K[(r["autocoder_code"] if float(r["autocoder_score"]) >= 0.80 else r["production_code"])[:2]]
        a["t"][ref] += w
        a["do"][prod] += w
        a["do"][ref] -= w
        a["dn"][new] += w
        a["dn"][ref] -= w
    bias = {}
    for i, g in enumerate(GROUPS):
        num = sum(acc[k]["do"][i] for k in NAMES)
        den = sum(acc[k]["t"][i] for k in NAMES)
        for k in NAMES:
            f = still[k] / coded[k]
            num += acc[k]["dn"][i] * f
            den += acc[k]["t"][i] * f
        bias[g] = 100.0 * num / den
    warned = [g for g in GROUPS if abs(bias[g]) > 2.0]
    errs = []
    want = ", ".join(warned[:-1]) + " and " + warned[-1]
    if want != fig["warned"]:
        errs.append(("warned", want, fig["warned"]))
    for g in GROUPS:
        if f"{bias[g]:.1f}".replace("-0.0", "0.0") != fig["bias"][g]:
            errs.append(("bias", g, f"{bias[g]:.1f}", fig["bias"][g]))
    for k in NAMES:
        if "{:,}".format(coded[k]) != fig["coded"][NAMES[k]] or "{:,}".format(still[k]) != fig["still"][NAMES[k]]:
            errs.append(("route", k, coded[k], still[k]))
    # ask: coding teams in October
    # each person's spells in a team, from the movements log
    spells, open_ = [], {}
    mv = sorted(rows(p("coding_staff_movements_2026.csv")), key=lambda r: (r["effective_date"], r["movement"]))
    for r in mv:
        d = date.fromisoformat(r["effective_date"])
        if r["movement"] in ("TRANSFERRED", "LEFT") and r["staff_no"] in open_:
            s_, c_, t_, f_ = open_.pop(r["staff_no"])
            spells.append((s_, c_, t_, f_, d if r["movement"] == "LEFT" else date.fromordinal(d.toordinal() - 1)))
        if r["movement"] in ("STARTED", "TRANSFERRED"):
            open_[r["staff_no"]] = (r["staff_no"], r["coder_id"], r["team_to"], d)
    for s_, c_, t_, f_ in open_.values():
        spells.append((s_, c_, t_, f_, date(2099, 12, 31)))
    assign = spells

    def team(key, val, day):
        hit = [a[2] for a in assign if a[key] == val and a[3] <= day <= a[4]]
        assert len(hit) == 1, (val, day, hit)
        return hit[0]
    wr = {}
    for path, coder, at in zip(t["coding_path"], t["coder_id"], t["coded_at"]):
        if path == "CLERICAL" and at.year == 2026 and at.month == 10:
            k = team(1, coder, at.date())
            wr[k] = wr.get(k, 0) + 1
    hrs = {}
    for r in rows(p("coding_timesheets_21sep_01nov2026.csv")):
        d = date.fromisoformat(r["work_date"])
        if r["activity"] == "OCC" and d.year == 2026 and d.month == 10:
            k = team(0, r["staff_no"], d)
            hrs[k] = hrs.get(k, 0.0) + float(r["hours"])
    for k, v in fig["teams"].items():
        if "{:,}".format(wr.get(k, 0)) != v["writeins"] or "{:,.2f}".format(hrs.get(k, 0.0)) != v["hours"]:
            errs.append(("team", k, wr.get(k, 0), round(hrs.get(k, 0.0), 2), v))
    # ask: follow-up calls in September by region, and those that made no contact
    region = {r["ed_code"]: r["region_name"] for r in rows(p("enumeration_districts_2026.csv"))}
    seen = set()
    calls, house, homes = {}, {}, set()
    vl = sorted(rows(p("field_visit_log_jun_oct_2026.csv")), key=lambda r: (r["synced_at"], r["visit_id"]))
    for r in vl:
        if r["outcome_code"] == "60":
            continue
        key = (r["address_id"], r["visit_time"], r["outcome_code"])
        if key in seen:
            continue
        seen.add(key)
        if r["visit_time"].startswith("2026-09"):
            n = region[r["ed_code"]]
            calls[n] = calls.get(n, 0) + 1
            if r["outcome_code"] == "31":
                house[n] = house.get(n, 0) + 1
    for n, v in fig["regions"].items():
        if "{:,}".format(calls.get(n, 0)) != v["calls"] or "{:,}".format(house.get(n, 0)) != v["nocontact"]:
            errs.append(("region", n, calls.get(n, 0), house.get(n, 0), v))
    assert not errs, errs[:10]
    print("verify: green (%d groups, %s warned, 5 teams, 8 regions)" % (len(GROUPS), want))
    return bias


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    main(os.path.join(os.path.dirname(here), "target"), os.path.join(here, "figures.json"))
