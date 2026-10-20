"""The independent verifier: reads only the shipped bundle (target/) and the golden deliverables, through bundle.py's
readers and its own completion, and recomputes the call, every county's deaths and rate, both asks' figures and every
filed sentence the call leans on. No generator state: nothing from truth, methods, pack or golden is imported."""
import csv
import json
import os
import re
import sys

import bundle as B

HERE = os.path.dirname(os.path.abspath(__file__))


def edge(v, unit):
    return unit / 2.0 - abs(v - round(v / unit) * unit)


def main(target, golden):
    fails = []

    def ok(label, cond):
        print("%s  verify: %s" % ("ok  " if cond else "FAIL", label))
        if not cond:
            fails.append(label)

    dr = B.directory(target)
    cr = B.census(target, dr)
    comp = B.complete_agencies(dr)
    miles = B.vmt(target)
    g = B.golden_g(B.observed(cr, comp), miles)
    names = dr["counties"]
    call = sorted(names[f] for f, v in g["rates"].items() if v >= 0.60)
    ok("xlsx read back: the directory's %d agencies and %d posts, the DOT's three years of DVMT" % (
        len(dr["agencies"]), len(dr["posts"])), len(dr["posts"]) == 14 and len(miles) == 14)
    ok("csv read back: the census's %d crashes in both layouts" % len(cr), len(cr) > 2500 and
       {c["year"] for c in cr} == {2023, 2024, 2025})
    ok("the complete agencies are the 14 State Patrol posts and the Corwin and Ossian sheriffs (manual 4.2)",
       len(comp) == 16 and {"SO00500", "SO01900"} <= comp)
    gl = pdf = B.pdf_text(B.find(target, "ghso_fy2028"))
    ok("pdf read back: the guidelines' estimand (2.2), drivers (2.3), rate and line (2.4)",
       "whether or not that driver was tested" in re.sub(r"\s+", " ", gl) and
       "A county whose rate is 0.60 or more is high-range." in re.sub(r"\s+", " ", gl) and
       "a motorcycle rider included" in re.sub(r"\s+", " ", gl))
    man = re.sub(r"\s+", " ", B.pdf_text(B.find(target, "fcc_reference_manual")))
    ok("pdf read back: the manual's testing procedures (4.2)",
       "The State Patrol's fatal crash procedure draws blood from every surviving driver" in man and
       "draw blood from a surviving driver arrested at the scene for impaired driving" in man)
    notes = open(B.find(target, "stl_extract_notes"), encoding="utf-8").read()
    ok("txt read back: the laboratory's extract notes (serum ratio, amended reports)",
       "divided by 1.16" in notes and "SUPERSEDED" in notes)
    crs_notes = re.sub(r"\s+", " ", B.pdf_text(B.find(target, "crs_extract_notes")))
    ok("pdf read back: the crash records notes (latest accepted version)",
       "A report as it stands is its latest accepted version." in crs_notes)
    ok("the call: %s" % ", ".join(call), call == ["Corwin", "Hatchell", "Ossian", "Tanager"])
    bt, e_ipw, e_pool = B.backtest(B.observed(cr, comp))
    ok("the State Patrol back-test, each post held out: the catch rates miss by %.2f, the one unarrested share by "
       "%.2f" % (e_ipw, e_pool), len(bt) == 14 and e_pool > 2.5 * e_ipw)
    with open(B.find(golden, "county_impaired_driving_rates"), encoding="utf-8") as fh:
        rows = {r["county_fips"]: r for r in csv.DictReader(fh)}
    a = B.ask_a(B.lab(target), dr)
    b, _ = B.ask_b(target, cr)
    for f in sorted(miles):
        r = rows[f]
        d, rt = g["deaths"][f], g["rates"][f]
        ok("%s: deaths %d, rate %s, arrests %d at %s per cent, injury crashes %d" % (
            r["county"], int(round(d)), "%.2f" % rt, a[f][0], "%.1f" % a[f][1], b.get(f, 0)),
           int(r["ai_driving_deaths_2023_2025"]) == int(round(d)) and r["ai_driving_rate_per_100m_vmt"] == "%.2f" % rt
           and int(r["arrests_blood_specimen_2025"]) == a[f][0] and r["pct_arrests_015_or_more_2025"] == "%.1f" % a[f][1]
           and int(r["injury_crashes_drinking_driver_2025"]) == b.get(f, 0) and
           (r["high_range_fy2028"] == "Y") == (rt >= 0.60))
    ok("bins from the shipped figures: deaths at least 0.2 from a half (tightest %.2f), rates at least 0.002 from a "
       "cell edge (%.4f), per cents at least 0.012 (%.3f)" % (
           min(edge(v, 1.0) for v in g["deaths"].values()), min(edge(v, 0.01) for v in g["rates"].values()),
           min(edge(v[1], 0.1) for v in a.values())),
       min(edge(v, 1.0) for v in g["deaths"].values()) >= 0.2 and min(edge(v, 0.01) for v in g["rates"].values()) >= 0.002
       and min(edge(v[1], 0.1) for v in a.values()) >= 0.012)
    letter = re.sub(r"\s+", " ", B.pdf_text(B.find(golden, "fy2028_high_range")))
    ok("the letter certifies the four with their rates", all(
        ("%s (%s" % (names[f], "%.2f" % g["rates"][f])) in letter for f in miles if g["rates"][f] >= 0.60))
    fig = os.path.join(HERE, "figures.json")
    if os.path.exists(fig):
        F = json.load(open(fig, encoding="utf-8"))
        ok("figures.json carries the bundle's call", sorted(F["high"]) == call)
        ok("figures.json's catch rates are the bundle's (%.1f and %.1f per cent)" % (
            100 * g["catch"][0], 100 * g["catch"][1]),
           F["catch_lo"] == "%.1f" % (100 * g["catch"][0]) and F["catch_hi"] == "%.1f" % (100 * g["catch"][1]))
    print("verify: %d failures" % len(fails))
    return not fails


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    sys.exit(0 if main(os.path.join(task, "target"), os.path.join(task, "golden")) else 1)
