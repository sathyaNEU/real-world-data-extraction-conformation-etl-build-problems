"""task467 ask layer against the careful solver's routes, on the cut pack.

    python3 task467/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The asks are the
brokerage fee ledger, velmont_taxi_fee_ledger_2025_2026.csv: one row per brokerage per month from January 2025 to
August 2026 with its fee-liable pickups (whole trips) and the fees it owes (dollars and cents), 120 rows and 240
figures. Ask A is the 2025 rows (72 brokerage-months), Ask B the 2026 rows (48). A figure is kept when it equals
figures.json's: a count exactly, fees owed to the cent.

The cracker is the careful solver, never a narrowed one. It lands the call (the within-zone restatement, $6.50) and
takes the ledger on its natural read with every filed rule executed as worded and the whole hygiene battery run, in
its own code below (apart from bundle.py and golden.py): by-law s.2 (a fee-liable pickup is a trip a licensed taxi
begins in zone 1; a voided trip is not a trip; days and months in Velmont local time, so every file's meter times are
read in local time: the 2025 file's own zone, the 2026 files' UTC converted, the 2024 file's unzoned times as local),
s.3(1) (the fee Schedule A sets for the year the trip begins, read from the by-law), s.3(2) (each month's pickups
billed to the brokerage the taxi is affiliated with when the trip begins, from the register's effective dates,
counting each trip once) and s.3(3) (the fee in force, whatever a meter charged); the battery: a reversal row
(every amount negated) cancels the one record it mirrors on licence, times, zones and amounts, across files; exact
duplicate rows (every field but the record number); near-exact duplicates (one licence, the same zones, fare and
total, start and stop in the same minute); trips of one licence that overlap in time; the fee column matched
whatever its case; each record placed by its meter start, never by the file it arrived in. The mirror stops at the
default path (the pickups' own fall, $5.75) and, the asks being decoupled from the call, reads the ledger as the
cracker does. The narrowed crackers the shipped sheet scored (the annual file's own brokerage column; exact duplicates
only) are printed as what they are. The full includer is golden.py's route and has to give back figures.json exactly
(the route code's control).

The pair is the ask sheet's formula: 38 recommendation and components, 7 instruction following, 55 asks over the
sheet's 26 ask criteria (each brokerage's monthly pickups and its monthly fees owed in 2025, 12, the same in 2026, 12,
each kept when every month of it is kept; the two files, 2, kept by any response that sends them), a response off
the call keeping r = 5 of the 38; r = 3 is printed beside it. Pair ceiling is the worse of the two. Exit 0 when the
gate holds (the cracker keeps no ask figure, the pair at or under 60, the mirror under half the ask weight, two
careful responses on the call under 70), 2 when it does not, 1 when a control fails. The script modifies nothing."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bundle as B     # noqa: E402  (golden.py's route, the control only)
import golden as G     # noqa: E402
import methods as M    # noqa: E402

TASK = os.path.dirname(HERE)
LOCAL = "America/Toronto"
PAIR_GATE = 60.0
WEIGHTS = {"ask sheet (38, 7, 55; off the call keeps 5)": (38.0, 7.0, 55.0, 5.0),
           "comparable (38, 7, 55; off the call keeps 3)": (38.0, 7.0, 55.0, 3.0)}
N_CRIT = 26          # Ask A 12, Ask B 12, the two files 2 (the ask sheet's planning count)
V2 = {"pickup_datetime": "meter_on", "dropoff_datetime": "meter_off", "pickup_zone": "pu_zone",
      "dropoff_zone": "do_zone", "passenger_count": "passengers", "trip_distance_km": "distance_km",
      "fare_amount": "fare", "tip_amount": "tip", "total_amount": "total", "store_and_fwd_flag": "sf_flag"}


# ------------------------------------------------------------------ the pack
def pack_dir(arg):
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling467-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    inner = os.path.join(tmp, "target")
    folder = inner if os.path.isdir(inner) else tmp
    md5 = hashlib.md5(open(src, "rb").read()).hexdigest()
    return folder, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(folder)), md5)


def one(folder, pattern):
    hits = sorted(f for f in os.listdir(folder) if re.search(pattern, f))
    assert len(hits) >= 1, pattern
    return [os.path.join(folder, h) for h in hits]


def pdf(path):
    return re.sub(r"\s+", " ", subprocess.run(["pdftotext", "-raw", path, "-"], capture_output=True, text=True,
                                              check=True).stdout)


# ------------------------------------------------------------------ the careful solver's own reading
def read_trips(path):
    """One trip file, field names to the version 3 names, the fee column whatever its case, meter times in Velmont
    local time (a zoned column converted, an unzoned one taken as local, by-law s.2)."""
    t = pq.read_table(path).to_pandas()
    t = t.rename(columns={k: V2.get(k, k) for k in t.columns})
    t = t.rename(columns={k: "airport_fee" for k in t.columns if k.lower() == "airport_fee"})
    for k in ("meter_on", "meter_off"):
        if t[k].dt.tz is not None:
            t[k] = t[k].dt.tz_convert(LOCAL).dt.tz_localize(None)
    t["file"] = os.path.basename(path)
    return t


def battery(t, exact_only=False):
    """The hygiene battery on trip records: reversal pairs out, exact duplicates out and, unless exact_only, near-exact
    duplicates (licence, zones, fare and total, start and stop minute) and one licence's overlapping trips out."""
    out = {"rows": len(t)}
    t = t.sort_values("record_id", kind="stable").reset_index(drop=True)
    # a reversal (every amount negated) cancels the one record it mirrors on licence, times, zones and amounts
    key = ["vehicle_id", "meter_on", "meter_off", "pu_zone", "do_zone", "fare", "total"]
    neg = t[t["total"] < 0].copy()
    pos = t[t["total"] >= 0].copy()
    if len(neg):
        neg = neg.assign(fare=-neg["fare"], total=-neg["total"])
        pos["_k"] = pos.groupby(key).cumcount()
        neg["_k"] = neg.groupby(key).cumcount()
        hit = pos.merge(neg[key + ["_k"]], on=key + ["_k"], how="left", indicator=True)
        out["reversals"] = len(neg)
        out["voided"] = int((hit["_merge"] == "both").sum())
        pos = hit[hit["_merge"] == "left_only"].drop(columns=["_k", "_merge"])
    t = pos
    cols = [c for c in t.columns if c not in ("record_id", "file")]
    n0 = len(t)
    t = t[~t.duplicated(subset=cols, keep="first")]
    out["exact"] = n0 - len(t)
    if not exact_only:
        k = pd.DataFrame({"v": t["vehicle_id"].to_numpy(), "a": t["meter_on"].dt.floor("min").to_numpy(),
                          "b": t["meter_off"].dt.floor("min").to_numpy(), "p": t["pu_zone"].to_numpy(),
                          "d": t["do_zone"].to_numpy(), "f": t["fare"].round(2).to_numpy(),
                          "x": t["total"].round(2).to_numpy()})
        n1 = len(t)
        t = t[~k.duplicated(keep="first").to_numpy()]
        out["near"] = n1 - len(t)
        s = t.sort_values(["vehicle_id", "meter_on", "record_id"], kind="stable")
        prev_off = s.groupby("vehicle_id")["meter_off"].shift()
        lap = (s["meter_on"] < prev_off).to_numpy()
        out["overlap"] = int(lap.sum())
        t = s[~lap].sort_values("record_id", kind="stable")
    out["kept"] = len(t)
    return t, out


def register(folder):
    a = pd.read_csv(one(folder, r"vehicle_affiliations\.csv$")[0], dtype=str, keep_default_na=False)
    a["a"] = pd.to_datetime(a["effective_from"])
    a["z"] = pd.to_datetime(a["effective_to"].replace("", "2100-01-01"))
    a["brokerage_id"] = a["brokerage_id"].astype(int)
    return a


def affiliated(p, reg):
    """By-law s.3(2): the brokerage the taxi is affiliated with on the day the trip begins (each spell from its
    effective_from to its effective_to, both days in)."""
    day = p["meter_on"].dt.normalize()
    m = pd.DataFrame({"vehicle_id": p["vehicle_id"].to_numpy(), "day": day.to_numpy(), "i": np.arange(len(p))}).merge(
        reg[["vehicle_id", "a", "z", "brokerage_id"]], on="vehicle_id", how="left")
    m = m[(m["a"] <= m["day"]) & (m["day"] <= m["z"])]
    assert m["i"].is_unique and len(m) == len(p), "one spell for every trip"
    return m.sort_values("i")["brokerage_id"].to_numpy()


def schedule(folder):
    law = pdf(one(folder, r"fees_bylaw_gt3\.pdf$")[0])
    return {int(y): float(v) for y, v in re.findall(r"\b(20\d\d) \$(\d+\.\d\d)\b", law)}


def ledger(rows, fees):
    g = rows.groupby(["month", "b"]).size().rename("n").reset_index()
    return {(r.month, int(r.b)): (int(r.n), round(r.n * fees[int(r.month[:4])], 2)) for r in g.itertuples()}


def careful(folder, how="careful"):
    """The ledger by a route. careful: every filed rule and the whole battery. label: the 2025 rows by the annual
    file's own brokerage column (the shipped sheet's Ask A cracker). exact: the 2026 rows with exact duplicates only
    (the shipped sheet's Ask B cracker)."""
    fees = schedule(folder)
    reg = register(folder)
    y25, s25 = battery(read_trips(one(folder, r"airport_2025\.parquet$")[0]))
    p25 = y25[y25["pu_zone"] == 1]
    b25 = p25["brokerage_id"].astype(int).to_numpy() if how == "label" else affiliated(p25, reg)
    d26 = pd.concat([read_trips(p) for p in one(folder, r"airport_2026-\d\d\.parquet$")], ignore_index=True)
    y26, s26 = battery(d26, exact_only=(how == "exact"))
    p26 = y26[y26["pu_zone"] == 1]
    b26 = affiliated(p26, reg)
    agree = float((b26 == p26["brokerage_id"].astype(int).to_numpy()).mean())
    rows = pd.concat([pd.DataFrame({"month": p25["meter_on"].dt.strftime("%Y-%m"), "b": b25}),
                      pd.DataFrame({"month": p26["meter_on"].dt.strftime("%Y-%m"), "b": b26})], ignore_index=True)
    return ledger(rows, fees), dict(s25=s25, s26=s26, agree26=agree)


def golden_route(folder):
    led = M.ledger(B.ledger_pickups(folder))
    return {(r.month, int(r.brokerage)): (int(r.pickups), round(float(r.owed), 2)) for r in led.itertuples()}


# ------------------------------------------------------------------ scoring
def gold():
    F = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    return F, {(r["month"], int(r["brokerage_id"])): (int(r["pickups_raw"]), float(r["owed"].replace(",", "")))
               for r in F["ledger"]}


def score(fig, g):
    """Figures kept (of 2 per brokerage-month) and criteria kept (of the sheet's 26)."""
    keep = {k: (fig.get(k, (None, None))[0] == v[0], fig.get(k, (None, None))[1] is not None and
                abs(fig.get(k, (0, 0))[1] - v[1]) < 0.005) for k, v in g.items()}
    figs = {"A": sum(a + b for k, (a, b) in keep.items() if k[0] < "2026"),
            "B": sum(a + b for k, (a, b) in keep.items() if k[0] >= "2026")}
    crit = 2                                      # the two files, sent by any response
    for yr in ("2025", "2026"):
        for b in range(1, 7):
            ks = [k for k in keep if k[0].startswith(yr) and k[1] == b]
            crit += all(keep[k][0] for k in ks) + all(keep[k][1] for k in ks)
    return figs, crit


def pair(kc, km, w):
    rec, ins, ask, off = w
    c = rec + ins + ask * kc / N_CRIT
    s = off + ins + ask * km / N_CRIT
    return c, s, (c + s) / 2.0


def show(name, fig, g):
    figs, crit = score(fig, g)
    print("  %-86s A %3d of 144, B %3d of 96; criteria %2d of %d" % (name, figs["A"], figs["B"], crit, N_CRIT))
    return figs, crit


# ------------------------------------------------------------------ the run
def main(arg=None):
    folder, scratch, stamp = pack_dir(arg)
    try:
        return run(folder, stamp)
    finally:
        if scratch:
            shutil.rmtree(scratch)


def run(folder, stamp):
    print("pack: " + stamp)
    F, g = gold()
    fx = G.compute(folder)
    c_fee, m_fee = "%.2f" % fx["fee"], "%.2f" % fx["rivals"]["own_fall"]["fee"]
    print("cracker's call (the within-zone restatement): $%s (%s the golden's $%s)" % (
        c_fee, "lands" if c_fee == F["call"]["fee_2027"] else "MISSES", F["call"]["fee_2027"]))
    print("mirror's call (the default path, the pickups' own fall): $%s (%s)" % (
        m_fee, "off the call" if m_fee != F["call"]["fee_2027"] else "ON THE CALL"))
    if c_fee != F["call"]["fee_2027"] or m_fee == F["call"]["fee_2027"]:
        print("CONTROL FAILED: the rows below assume the cracker on the call and the mirror off it")
        return 1
    full = golden_route(folder)
    bad = [k for k in g if full.get(k) != g[k]]
    if bad or len(full) != len(g):
        print("CONTROL FAILED: the full includer does not reproduce figures.json at %s" % bad[:5])
        return 1
    print("full includer (golden.py's route): reproduces figures.json exactly, 240 of 240 figures")
    cr, info = careful(folder)
    print("\nthe careful solver's battery: 2025 file %s; 2026 files %s; the 2026 records' brokerage equals the "
          "register's on the trip date for %.1f per cent of pickups" % (info["s25"], info["s26"], 100 * info["agree26"]))
    print("\nroutes, figures kept (Ask A 144, Ask B 96) and criteria kept (of %d):" % N_CRIT)
    fc, kc = show("cracker: the call, every filed rule as worded, the whole battery", cr, g)
    fm, km = show("mirror: the default path's call, the same ledger route (the asks are decoupled)", cr, g)
    print("  narrowed crackers, printed as what they are (each skips something the careful solver does):")
    show("    the 2025 rows by the annual file's own brokerage column (the shipped sheet's Ask A cracker)",
         careful(folder, "label")[0], g)
    show("    the 2026 rows with exact duplicates only (the shipped sheet's Ask B cracker)", careful(folder, "exact")[0], g)
    print("\nthe cracker's figures against figures.json, the first brokerage-months of each year (stated, golden):")
    for k in [k for k in g if k[0] in ("2025-01", "2026-01")]:
        print("  %s brokerage %d  pickups %5s %5d  owed %10s %10.2f  %s" % (
            k[0], k[1], cr.get(k, (None,))[0], g[k][0], "%.2f" % cr.get(k, (0, 0))[1], g[k][1],
            "kept" if cr.get(k) == g[k] else "miss"))
    worst, both = [], []
    for wname, w in WEIGHTS.items():
        c, s, p = pair(kc, km, w)
        worst.append(p)
        both.append(c)
        print("\n%s: cracker %.1f, mirror %.1f, pair %.1f; two careful responses on the call %.1f" % (wname, c, s, p, c))
    n = 2 * len(g)
    leak = 100.0 * km / N_CRIT
    pc = max(worst)
    print("\nCracker keeps: %d of %d ask figures (%d of %d criteria)" % (fc["A"] + fc["B"], n, kc, N_CRIT))
    print("Mirror leakage: %.1f per cent of ask weight" % leak)
    print("Pair ceiling: %.1f (the worse of the measured pair on either weighting)" % pc)
    ok = fc["A"] + fc["B"] == 0 and pc <= PAIR_GATE and leak < 50.0 and max(both) < 70.0
    print("gate %s: it needs the cracker to keep no ask figure, the pair at or under %.0f, the mirror's leakage under 50 "
          "per cent and two careful responses on the call under 70" % ("HOLDS" if ok else "FAILS", PAIR_GATE))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
