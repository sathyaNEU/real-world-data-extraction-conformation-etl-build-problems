"""task270 independent verifier: every graded figure recomputed from the cut pack alone with its own readers and its own
arithmetic (the csv module and openpyxl, no pandas; days covered as a walk over each supply's end; the compliance-aid
cycle as one weekday at a fixed step of 7 or 28 days, a pack due on a closed day supplied the next opening day), then
compared with generator/figures.json. Exit 1 on any difference.

    python3 task270/generator/verify.py [TARGET]"""
from __future__ import annotations

import csv
import datetime as dt
import json
import os
import re
import statistics
import sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
Y0, Y1 = dt.date(2026, 1, 1), dt.date(2026, 12, 31)
HOLIDAYS = {dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1), dt.date(2026, 4, 3),
            dt.date(2026, 4, 6), dt.date(2026, 5, 4), dt.date(2026, 5, 25), dt.date(2026, 8, 31),
            dt.date(2026, 12, 25), dt.date(2026, 12, 28)}


def find(prefix):
    hits = [f for f in os.listdir(TARGET) if f.startswith(prefix)]
    assert len(hits) == 1, (prefix, hits)
    return os.path.join(TARGET, hits[0])


def rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def per_day(text):
    t = text.strip().upper()
    if re.match(r"^(TAKE )?(TWO|2)\b", t):
        return 2
    return 1


def covered(items):
    """items: (date, days) in 2026; the share of days from the first item to 31 December held, a supply bought
    before the last ran out starting where it ends."""
    items = sorted(items)
    start = items[0][0]
    end = None
    held = 0
    for d, n in items:
        s = d if end is None or d > end else end
        e = s + dt.timedelta(days=n)
        s2, e2 = max(s, start), min(e, Y1 + dt.timedelta(days=1))
        if e2 > s2:
            held += (e2 - s2).days
        end = e
    return held / ((Y1 - start).days + 1)


def closed(d):
    return d.weekday() == 6 or d in HOLIDAYS


def set_day(d):
    """The day a pack was due: back over the closed days just before it, to the last of them that was due."""
    out = d
    p = d - dt.timedelta(days=1)
    while closed(p):
        out = p
        p -= dt.timedelta(days=1)
    return out


def on_cycle(dates):
    ds = sorted(set(dates))
    if len(ds) < 5:
        return False
    for w in range(7):
        due = []
        for d in ds:
            if d.weekday() == w:
                due.append(d)
                continue
            back = [d - dt.timedelta(days=k) for k in range(1, 4)]
            hit = [b for b in back if b.weekday() == w and all(closed(x) for x in back[:back.index(b) + 1])]
            if not hit:
                break
            due.append(hit[0])
        else:
            steps = [(b - a).days for a, b in zip(due, due[1:])]
            med = statistics.median(steps)
            if med in (7, 28) and sum(s == med for s in steps) >= 0.9 * len(steps):
                return True
    return False


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    xw = {r["old_pseudonym"]: r["new_pseudonym"] for r in rows(find("pseudonym_crosswalk_"))}
    items = {}
    for r in rows(find("community_pharmacy_statin_dispensing_")):
        d = dt.date.fromisoformat(r["dispensed_date"])
        if not (Y0 <= d <= Y1):
            continue
        k = xw.get(r["patient_pseudonym"], r["patient_pseudonym"])
        items.setdefault(k, []).append((d, int(r["quantity"]) // per_day(r["dosage_instructions"])))
    member = {}
    for r in rows(find("practice_network_membership_")):
        if not r["member_to"]:
            member[r["practice_ods"]] = r["network"][:-4]
    pts = {}
    for r in rows(find("quarvis_practices_lipid_cohort_")):
        pts[r["nhs_pseudo"]] = (member[r["practice_ods"]], int(r["yob"]), bool(r["care_home_since"]),
                                bool(r["mds_since"]))
    ws = openpyxl.load_workbook(find("synaris_practices_lipid_cohort_"), read_only=True)["Lipid cohort"]
    for i, r in enumerate(ws.iter_rows(values_only=True)):
        if i:
            pts[r[0]] = (member[r[1]], int(r[2]), str(r[4]).startswith("Care home"), False)
    count = {}
    base = care = cyc = coded = 0
    for k, (net, yob, home, aid) in pts.items():
        it = items.get(k, [])
        if yob > 1961 or len(it) < 2:
            continue
        base += 1
        if home:
            care += 1
            continue
        if aid or on_cycle([d for d, _ in it]):
            cyc += 1
            coded += aid
            continue
        c = count.setdefault(net, [0, 0])
        c[0] += 1
        c[1] += covered(it) < 0.8
    share = {n: 100.0 * lo / tot for n, (tot, lo) in count.items()}
    tier = sorted(n for n, s in share.items() if s >= 30)
    out = {"tier": tier, "n_base": base, "n_care": care, "n_cycle": cyc, "n_cycle_coded": coded,
           "n_pop": sum(v[0] for v in count.values())}
    left = max((n for n in share if n not in tier), key=lambda n: share[n])
    out["closest_left_out"] = left
    out["gap_points"] = 30 - share[left]
    code = {"Briskdale": "BRK", "Corvendale": "COR", "Ellinholt": "ELL", "Feldcote": "FEL", "Grevmoor": "GRV",
            "Iversford": "IVF", "Krathwold": "KRT", "Lathcombe": "LTH", "Marlwold": "MRL", "Nevgarth": "NVG",
            "Pellholt": "PLH", "Tarvdale": "TRV"}
    for n, s in share.items():
        out["share_" + code[n]] = s
        out["population_" + code[n]] = count[n][0]
    out["lowest_in"] = min(share[n] for n in tier)
    # ------------------------------------------------------------------ the pilot
    ph = {r["ods_code"]: r for r in rows(find("community_pharmacies_"))}
    recs = {}
    for r in rows(find("services_portal_statin_pilot_export_")):
        recs[r["record_id"]] = (r["pharmacy_ods"], r["patient_ref"], r["consultation_type"],
                                dt.datetime.strptime(r["consultation_date"], "%d/%m/%Y").date())
    recovered = set()
    wb = openpyxl.load_workbook(find("pilot_payment_statements_"), read_only=True)
    for sh in wb.worksheets:
        for i, r in enumerate(sh.iter_rows(values_only=True)):
            if not i:
                continue
            if r[6] == "Recovery":
                recovered.add(r[1])
            elif r[1] not in recs:
                recs[r[1]] = (r[0], r[2], r[3], r[4].date() if isinstance(r[4], dt.datetime) else r[4])
    firsts, follows = {}, {}
    for rid, (ods, ref, kind, d) in recs.items():
        k = xw.get(ref, ref)
        (firsts if kind == "First consultation" else follows).setdefault(k, []).append((d, ods, rid in recovered))
    start, stop = dt.date(2025, 10, 1), dt.date(2026, 9, 30)

    def network(ods, d):
        p = ph[ods]
        if p["relocated_on"] and d < dt.date.fromisoformat(p["relocated_on"]):
            return p["previous_locality"]
        return p["locality"]

    def quarter(d):
        return 1 + ((d.year - 2025) * 12 + d.month - 10) // 3

    for k, fs in firsts.items():
        keep = [f for f in fs if not f[2]] if any(not f[2] for f in fs) else fs
        if len(keep) > 1:
            raise SystemExit("patient %s keeps %d first consultations" % (k, len(keep)))
        d, ods, _ = keep[0]
        n = network(ods, d)
        if not (start <= d <= stop) or n not in ("Krathwold", "Lathcombe"):
            continue
        tag = "KRT" if n == "Krathwold" else "LTH"
        key1 = "pilot_first_%s_q%d" % (tag, quarter(d))
        out[key1] = out.get(key1, 0) + 1
        key2 = "pilot_followed_%s_q%d" % (tag, quarter(d))
        out.setdefault(key2, 0)
        if any(0 < (f - d).days <= 42 for f, _o, _r in follows.get(k, [])):
            out[key2] += 1
    # ------------------------------------------------------------------ compare
    names = {v: k for k, v in code.items()}
    bad = []
    filed = {"tier_line_pct": 30, "fallen_behind_pct": 80, "cycle_steps_days": [7, 28],
             "specification_sections": ["2.2", "2.3", "3.1"], "follow_up_days": [1, 41]}
    for key, want in F.items():
        got = out.get(key)
        if key == "parameters":
            ok = want == filed
        elif key == "tier":
            ok = [n for n in tier] == want
        elif key == "closest_left_out":
            ok = got == want
        elif key == "tier_count":
            ok = len(tier) == want
        elif isinstance(want, str) and "." in want:
            ok = got is not None and abs(got - float(want)) <= 0.05 + 1e-9 and "%.1f" % (got + 1e-9) == want
        else:
            ok = got is not None and int(str(want).replace(",", "")) == got
        if not ok:
            bad.append((key, want, got))
    print("verify: %d figures, %d differ" % (len(F), len(bad)))
    for b in bad:
        print("  DIFF %s: figures.json %r, verify %r" % b)
    print("verify: tier %s, %d patients in the population" % (", ".join(tier), out["n_pop"]))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
