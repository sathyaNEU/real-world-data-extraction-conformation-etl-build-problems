"""The cracker and mirror sheets as code, run on the cut pack (supplemental-stumping 1.1 and Part 6).

The cracker lands the call, runs the hygiene battery and executes every filed rule: it converts the platform's UTC
to local time, reads the register's two Corn Exchange units as one site, leaves out the intervals the counter did not
keep on both sides, counts only track riders, converts the contractor's minutes and treats a follow-up visit as no
new stoppage. What it does not do is what nothing in the pack tells it: read the interval stamps as interval ends,
find the two loggers left on laptop time, separate a visit that found the counter down again from one that checked a
repair, count a contractor's job inside the unit's job once, or split a stoppage at the year's edge. The mirror stops
on the main call's most attractive wrong rung (each counter's total growth) and handles the asks the same way.

Scoring follows supplemental-stumping Part 0: the call and its components 38, instructions 7, the asks 55 shared
equally over the 24 ask figures; a response off the call keeps 5 of the 38.

    python3 cracker.py <target>        prints the sheet; exit 1 if a ceiling is broken"""
import csv
import os
import sys
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bundle as B                     # noqa: E402
import deliver as DL                   # noqa: E402

CALL, INSTR, ASKS, OFF_CALL = 38.0, 7.0, 55.0, 5.0


# ---------------------------------------------------------------------------------------------- ask A routes
def ask_a(target, stamps_end=False, laptop=False, road=False, gap_both=True):
    cw = {}
    with open(os.path.join(target, "count_week_15min_2026-05-11_15.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            ts = datetime.strptime(r["timestamp_utc"], "%Y-%m-%dT%H:%M:%SZ")
            local = ts if (laptop and r["counter_id"] in DL.LAPTOP_CLOCK) else ts + timedelta(hours=1)
            start = local - timedelta(minutes=15) if stamps_end else local
            d = cw.setdefault(r["counter_id"], {})
            d[start] = d.get(start, 0) + int(r["count"])
    vs = DL.read_volunteers(target)
    out = {}
    for cid, v in vs.items():
        C = V = 0
        for s, e, vi, vo, rd in v["rows"]:
            qs = []
            t = s
            while t < e:
                qs.append(t)
                t += timedelta(minutes=15)
            if not all(q in cw[cid] for q in qs) and gap_both:
                continue
            C += sum(cw[cid].get(q, 0) for q in qs)
            V += vi + vo + (rd if road else 0)
        out[cid] = (C, round(100.0 * (V - C) / V, 1))
    return out


# ---------------------------------------------------------------------------------------------- ask B routes
def ask_b(target, join="asset", children="drop_all", years="reported", dupes="sum", minutes="field"):
    rows = DL.read_log(target)
    reg = B.read_register(target)
    dash_ids = {r["counter_id"]: r["legacy_site_name"] for r in reg if r["type"] == "dashboard"}
    site_to_cid = {r["legacy_site_name"]: r["counter_id"] for r in reg if r["type"] == "dashboard" and not r["unit_of_record_to"]}
    by_job = {r["job_no"]: r for r in rows}
    spells = []
    for r in rows:
        if join == "asset":
            if r["asset_id"] not in dash_ids:
                continue
            cid = site_to_cid[dash_ids[r["asset_id"]]]
        else:
            cid = site_to_cid.get(r["site"])
            if cid is None:
                continue
        con = r["logged_by"] != "Traffic Monitoring Unit"
        m = DL.parse_downtime(r["downtime"], con)
        if m is None:
            continue
        if r["parent_job"]:
            if children == "drop_all":
                continue
            if children == "right" and r["downtime"] == by_job[r["parent_job"]]["downtime"]:
                continue
        a, b = DL._ldt(r["reported"]), DL._ldt(r["closed"])
        if minutes == "recompute":
            m = int((b - a).total_seconds() // 60)
        spells.append(dict(cid=cid, a=a, b=b, m=m))
    if dupes == "merge":
        merged = []
        for cid in sorted({s["cid"] for s in spells}):
            cur = None
            for s in sorted([s for s in spells if s["cid"] == cid], key=lambda s: s["a"]):
                if cur and s["a"] <= cur["b"]:
                    if s["b"] > cur["b"]:
                        cur["m"] += DL.B_elapsed(cur["b"], s["b"])
                        cur["b"] = s["b"]
                else:
                    cur = dict(s)
                    merged.append(cur)
        spells = merged
    out = {c: [0, 0] for c in sorted(site_to_cid.values())}
    for s in spells:
        if years == "reported":
            m = s["m"] if s["a"].year == 2025 else 0
        elif years == "closed":
            m = s["m"] if s["b"].year == 2025 else 0
        else:
            full = DL.B_elapsed(s["a"], s["b"])
            m = DL.minutes_in_year(s["a"], s["b"], 2025) * (s["m"] / full if full else 1)
        if m > 0:
            out[s["cid"]][0] += m
            out[s["cid"]][1] += 1
    return {c: (round(v[0] / 60.0, 1), v[1]) for c, v in out.items()}


# ---------------------------------------------------------------------------------------------- scoring
NATURAL_A = dict(stamps_end=False, laptop=False, road=False, gap_both=True)
NATURAL_B = dict(join="asset", children="drop_all", years="reported", dupes="sum", minutes="field")
GOLD_A = dict(stamps_end=True, laptop=True, road=False, gap_both=True)
GOLD_B = dict(join="site", children="right", years="clip", dupes="merge", minutes="field")
CRACKS = [("A1 interval stamps read as ends", "A", dict(stamps_end=True)),
          ("A2 the two laptop clocks found", "A", dict(laptop=True)),
          ("B1 a visit that found the counter down again kept", "B", dict(children="right")),
          ("B2 the log joined by site, so CVC-1180 counts", "B", dict(join="site")),
          ("B3 stoppages split at the year's edge", "B", dict(years="clip")),
          ("B5 the contractor's job inside the unit's counted once", "B", dict(dupes="merge"))]


def hits(target, a_kw, b_kw):
    ga, gb = ask_a(target, **GOLD_A), ask_b(target, **GOLD_B)
    ra, rb = ask_a(target, **a_kw), ask_b(target, **b_kw)
    rows = []
    for cid in ga:
        rows.append(("A", cid, "riders", ra[cid][0] == ga[cid][0]))
        rows.append(("A", cid, "shortfall", ra[cid][1] == ga[cid][1]))
    for cid in gb:
        rows.append(("B", cid, "hours", rb[cid][0] == gb[cid][0]))
        rows.append(("B", cid, "stoppages", rb[cid][1] == gb[cid][1]))
    return rows


def score(on_call, rows):
    n = len(rows)
    got = sum(1 for r in rows if r[3])
    return (CALL if on_call else OFF_CALL) + INSTR + ASKS * got / n, got, n


def sheet(target):
    out = {}
    nat = hits(target, NATURAL_A, NATURAL_B)
    c, got, n = score(True, nat)
    m, mgot, _ = score(False, nat)
    out["cracker"] = (c, got, n)
    out["mirror"] = (m, mgot, n)
    out["pair"] = (c + m) / 2
    out["both_on_call"] = c
    out["cracks"] = {}
    for name, ask, kw in CRACKS:
        a_kw, b_kw = dict(NATURAL_A), dict(NATURAL_B)
        (a_kw if ask == "A" else b_kw).update(kw)
        rr = hits(target, a_kw, b_kw)
        cc, g2, _ = score(True, rr)
        out["cracks"][name] = (cc, g2, (cc + m) / 2)
    out["natural_rows"] = nat
    out["golden_a"] = ask_a(target, **GOLD_A)
    out["golden_b"] = ask_b(target, **GOLD_B)
    out["natural_a"] = ask_a(target, **NATURAL_A)
    out["natural_b"] = ask_b(target, **NATURAL_B)
    return out


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    s = sheet(target)
    print("golden A  ", s["golden_a"])
    print("natural A ", s["natural_a"])
    print("golden B  ", s["golden_b"])
    print("natural B ", s["natural_b"])
    print("cracker %.1f (%d of %d ask figures)   mirror %.1f (%d)   pair %.1f   both on the call %.1f" % (
        s["cracker"][0], s["cracker"][1], s["cracker"][2], s["mirror"][0], s["mirror"][1], s["pair"], s["both_on_call"]))
    worst = 0
    for name, (cc, g2, pair) in s["cracks"].items():
        print("  one crack: %-58s cracker %.1f (%2d figures)  pair %.1f" % (name, cc, g2, pair))
        worst = max(worst, pair)
    ok = s["pair"] <= 40 and s["both_on_call"] <= 45 and worst <= 40
    print("worst single crack pair %.1f; ceilings %s" % (worst, "hold" if ok else "BROKEN"))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
