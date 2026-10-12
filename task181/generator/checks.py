"""Assertions on the built pack and goldens: the ladder (every rung's set and margin), the forcing record, the
semantic fork rows, the ask goldens and their wrong paths, the separation of device rows from the main population,
the input gates and the realism sweep. Raises on the first failure; prints one line per assertion."""
import glob
import json
import os
import re
import sys

import numpy as np
import pandas as pd
import pdfplumber

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A          # noqa: E402
import deliver as DL      # noqa: E402
import exposure as X      # noqa: E402
import models as M        # noqa: E402
import world as W         # noqa: E402

N = [0]


def ok(cond, msg):
    N[0] += 1
    if not cond:
        raise SystemExit("CHECK FAILED %d: %s" % (N[0], msg))
    print("  ok %2d  %s" % (N[0], msg))


def name_set(d):
    return sorted(W.NAME[W.SECTORS[s]] for s, v in d.items() if v > W.TOLERANCE)


def run(target, golden, world=None, meta_path=None):
    print("checks: %s" % target)
    c = DL.compute(target)
    r, sets = c["r"], c["sets"]
    g = r["golden"]
    S = range(8)
    T = W.SECTORS.index("TRV")

    # ---------------------------------------------------------------- the call and the ladder
    ok(sets["golden"] == ["TRV"], "golden: Tarvik alone over 40.0 (%s)" % ", ".join("%.1f" % g[s] for s in S))
    ok(g[T] >= 1.15 * W.TOLERANCE, "golden margin: Tarvik %.1f at least 1.15 x 40.0" % g[T])
    ok(max(g[s] for s in S if s != T) <= W.TOLERANCE / 1.15, "golden margin: every other sector at or under 34.8 "
       "(highest %.1f)" % max(g[s] for s in S if s != T))
    for k in ("R0", "R1", "R1_record", "R1_summers", "R2_density", "R2b_own", "R2b_pooled", "R2b_pooled_s26"):
        ok(sets[k] == [], "rung %s names no sector (highest %s %.1f)" % (k, W.SECTORS[max(S, key=lambda s: r[k][s])],
                                                                        max(r[k].values())))
    ok(max(r["R1"].values()) <= W.TOLERANCE / 1.2, "default path: highest forecast at least 1.2 x under 40.0 (%.1f)"
       % max(r["R1"].values()))
    ok(r["R1"][T] < 20, "default path: Tarvik low on the summer 2026 rate (%.1f)" % r["R1"][T])
    ok(sorted(r["R1"], key=lambda s: -r["R1"][s]).index(T) >= 4, "position: Tarvik 5th or lower on the default path")
    ok(sets["R2c_trend"] not in ([], ["TRV"]) and "TRV" not in sets["R2c_trend"],
       "rung R2c (trend) names a wrong set: %s" % sets["R2c_trend"])
    for k in ("R3_summers", "R3_s26", "R3_y26", "R3_own", "R3_all_losses", "R3_meet", "R3_moving_pairs",
              "R3_within_1000ft", "R3_within_2000ft"):
        top = max(r[k][s] for s in S if s != T)
        ok(sets[k] == ["TRV"] and r[k][T] >= 1.15 * W.TOLERANCE and top <= W.TOLERANCE / 1.15,
           "variant %s: Tarvik alone (%.1f), next %.1f" % (k, r[k][T], top))
    s26 = [tuple(int(x.timestamp()) for x in W.season(2026))]
    e26 = M.exposures(c["plan"], {"utc": [(int(pd.Timestamp("2027-06-01", tz="UTC").timestamp()),
                                           int(pd.Timestamp("2027-09-01", tz="UTC").timestamp()))]})
    utc27 = {s: c["lam"] * e26[(s, "utc")]["cross"] / e26[(s, "utc")]["fh"] * 1e5 for s in S}
    ok(name_set(utc27) == ["Tarvik"], "SF2: the season read in UTC gives Tarvik alone (%.1f)" % utc27[T])
    ok(all(abs(g[s] / W.TOLERANCE - 1) >= 0.06 for s in S), "SF8: no sector within 6 per cent of 40.0")
    ok(name_set({s: round(g[s], 1) for s in S}) == ["Tarvik"], "SF9: rates rounded to one decimal first, same set")
    ok(name_set(r["R3_all_losses"]) == ["Tarvik"], "SF1: every loss of separation, pilot-induced included, same set")
    ok(all(name_set(r[k]) == ["Tarvik"] for k in ("R3_summers", "R3_s26", "R3_y26")), "SF5: estimation window, same set")
    ok(all(name_set(r[k]) == ["Tarvik"] for k in ("R3_meet", "R3_moving_pairs", "R3_within_1000ft",
                                                    "R3_within_2000ft")), "SF6: pair definition, same set")
    ok(name_set(r["R3_own"]) == ["Tarvik"], "SF7: each sector's own rate per pair, same set")
    fh_clip = {}
    a27, b27 = (int(x.timestamp()) for x in W.season(2027))
    p = c["plan"]
    for s in S:
        m = p["sec"] == s
        fh_clip[s] = float((np.minimum(p["t1"][m], b27) - np.maximum(p["t0"][m], a27)).clip(min=0).sum()) / 3600
    ok(name_set({s: c["exp27"][s] / fh_clip[s] * 1e5 for s in S}) == ["Tarvik"],
       "SF3: flight hours clipped at the season's edges, same set")
    ok(len(set(c["rec"]["sec"].tolist())) == 8 and set(c["occ"]["code"].dropna()) <= set(W.SECTORS),
       "SF4: occurrences and flight hours are recorded per elementary sector")
    # discriminator dominance
    e27, e26_ = c["ex27"][(T, "s27")], c["ex"][(T, "s26")]
    ok(e27["cross"] / e26_["cross"] >= 4 and e27["fh"] / e26_["fh"] <= 1.12,
       "dominance: Tarvik's pairs x%.1f against flight hours x%.2f, summer 2026 to summer 2027"
       % (e27["cross"] / e26_["cross"], e27["fh"] / e26_["fh"]))

    # ---------------------------------------------------------------- the forcing record
    occ = c["occ"]
    rec = c["rec"]
    smi = occ[occ["occurrence_type"] == "SMI"]
    df = pd.DataFrame({"cs": rec["callsign"], "sec": rec["sec"], "t0": rec["t0"], "t1": rec["t1"], "a": rec["a"],
                       "b": rec["b"]})
    df = df[df["cs"].isin(set(smi["ac1_callsign"]) | set(smi["ac2_callsign"]))]
    grp = {k: v for k, v in df.groupby(["cs", "sec"])}
    crossed = 0
    for o in smi.itertuples():
        def trav(cs):
            d = grp.get((cs, o.sec))
            d = d[(d["t0"] <= o.ts + 60) & (d["t1"] >= o.ts - 60)]
            return d.iloc[0]
        i, j = trav(o.ac1_callsign), trav(o.ac2_callsign)
        lo, hi = max(i.t0, j.t0), min(i.t1, j.t1)
        li = lambda q, t: q.a + (q.b - q.a) * (t - q.t0) / (q.t1 - q.t0)
        if (li(i, lo) - li(j, lo)) * (li(i, hi) - li(j, hi)) < 0:
            crossed += 1
    ok(crossed == len(smi), "every loss of separation in the record is a pair whose levels changed order (%d of %d)"
       % (crossed, len(smi)))
    ok(set(smi["atm_contribution"]) <= {"D", "I", "N"} and set(smi["status"]) == {"Closed"},
       "every loss of separation closed with its ATM contribution determined")
    lam_s = [c["L"][(s, "all")] / c["ex"][(s, "all")]["cross"] for s in S]
    fh_s = [c["L"][(s, "all")] / c["ex"][(s, "all")]["fh"] for s in S]
    ok(max(lam_s) / min(lam_s) < 1.4 and max(fh_s) / min(fh_s) > 1.4,
       "losses per pair hold across sectors (max/min %.2f) while losses per flight hour do not (%.2f)"
       % (max(lam_s) / min(lam_s), max(fh_s) / min(fh_s)))
    ok(max(lam_s) / min(lam_s) >= 1.1, "losses per pair vary by ordinary chance between sectors (max/min %.2f)"
       % (max(lam_s) / min(lam_s)))
    for s in S:
        for win in ("s25", "s26"):
            rate = c["L"][(s, win)] / c["ex"][(s, win)]["fh"] * 1e5
            if rate > W.TOLERANCE / 1.06:
                ok(False, "realised %s rate under the tolerance for %s" % (win, W.SECTORS[s]))
    ok(True, "every sector's realised summer 2025 and 2026 rate at least 6 per cent under 40.0")

    # the close-out reproduces from the record
    with pdfplumber.open(os.path.join(target, "HACC_summer2026_safety_closeout.pdf")) as pdf:
        text = "\n".join(pg.extract_text() or "" for pg in pdf.pages)
    for s in S:
        nm = W.NAME[W.SECTORS[s]]
        m = re.search(r"^%s (\d+) (\d+) ([\d,]+) ([\d.]+)$" % nm, text, re.M)
        ok(m is not None and int(m.group(1)) == c["L"][(s, "s25")] and int(m.group(2)) == c["L"][(s, "s26")] and
           int(m.group(3).replace(",", "")) == round(c["ex"][(s, "s26")]["fh"]) and
           m.group(4) == "%.1f" % (c["L"][(s, "s26")] / c["ex"][(s, "s26")]["fh"] * 1e5),
           "close-out row reproduces for %s" % nm)

    # ---------------------------------------------------------------- the asks
    a = c["asks"]
    d = a["delay"]
    for k, s in enumerate(W.SECTORS):
        v = d["golden"][k]
        ok(abs((v * 100) % 1 - 0.5) >= 0.15, "ask 1 %s %.4f sits mid-bin at two decimals" % (s, v))
    ok(all("%.2f" % d["golden_by_eobt"][k] == "%.2f" % d["golden"][k] for k in S),
       "ask 1 converges: the season read by off-block time takes the same flights as by sector entry")
    ok(all("%.2f" % d["every_plan"][k] != "%.2f" % d["golden"][k] for k in S),
       "ask 1 cracker (plans that never flew kept) misses every sector")
    ok(all("%.2f" % d["every_row"][k] != "%.2f" % d["golden"][k] for k in S), "ask 1 natural read (every row) misses "
       "every sector")
    ok(sum("%.2f" % d["callsign_day"][k] != "%.2f" % d["golden"][k] for k in S) >= 6,
       "ask 1 callsign-and-day dedup misses at least six sectors")
    for s in W.SECTORS:
        mins = int(round(a["hours"][s] * 60))
        ok(mins % 6 in (0, 1, 5), "ask 2 %s %.2f h sits mid-bin at one decimal" % (s, a["hours"][s]))
    ok(all("%.1f" % a["hours_current"][s] != "%.1f" % a["hours"][s] for s in W.SECTORS),
       "ask 2 cracker (current table all season) misses every sector")
    ok(all("%.1f" % a["hours_rev8"][s] != "%.1f" % a["hours"][s] for s in W.SECTORS),
       "ask 2 the manual's table all season misses every sector")
    ok(all(a["enc_rows"][s] != a["enc"][s] for s in W.SECTORS), "ask 3 cracker (report rows counted) misses every sector")
    ok(any(a["enc_utc"][s] != a["enc"][s] for s in W.SECTORS), "ask 3 hazard: the season read in UTC moves a sector")
    ok(len(set(a["enc"].values())) >= 5 and len(set(round(x, 2) for x in d["golden"].values())) == 8,
       "realism: ask figures differ across sectors")
    rev8, rev9 = A.om_table(target), A.current_table(target)
    diff = sorted(k for k in rev9 if sorted(map(tuple, rev9[k])) != sorted(map(tuple, rev8[k])))
    ok(diff == ["C5", "C6A", "C6B"], "the manual's revision 8 differs from the current table in C5, C6A, C6B only")
    log = pd.read_csv(os.path.join(target, "sector_configuration_log_2026-05_2026-09.csv"), keep_default_na=False)
    ok(int(log["remarks"].str.contains("revision 9").sum()) == 1, "one logged entry for the revision taking effect")
    ok(set(log["configuration"]) <= set(rev9) and set(log["configuration"]) <= set(rev8),
       "every logged configuration code is in both tables")

    # ---------------------------------------------------------------- separation and the pack
    slots = pd.read_csv(os.path.join(target, "nm_slot_allocations_2026-05_2026-09.csv"), dtype={"ifplid": str})
    flown = set(rec["ifplid"])
    never = set(slots["ifplid"]) - flown
    ok(len(never) > 0 and not (never & flown), "device rows (plans that never flew, %d) are outside the flight data"
       % len(never))
    ok(set(occ["occurrence_type"][occ["occurrence_type"] == "SMI"]) == {"SMI"} and
       not (set(occ[occ["occurrence_type"] == "ACAS RA"]["occurrence_no"]) & set(smi["occurrence_no"])),
       "the advisory reports (ask 3) are outside the main call's occurrence rows")
    src = open(os.path.join(HERE, "models.py")).read()
    ok("configuration" not in src and "slot" not in src and "roster" not in src and "met_cb" not in src,
       "the main call's computation reads none of the ask files or distractors")
    ok(not any(x in open(os.path.join(HERE, f)).read() for f in ("models.py", "asks.py")
               for x in ("controller_roster", "met_cb")), "no golden computation reads a distractor")
    files = sorted(os.listdir(target))
    meta = json.load(open(meta_path)) if meta_path else None
    ok(len(files) >= 10, "input gate: %d files" % len(files))
    ok(len({f.rsplit(".", 1)[1] for f in files}) >= 3, "input gate: %d formats" % len({f.rsplit(".", 1)[1] for f in files}))
    ok(len(rec["t0"]) >= 25000, "input gate: the flight data has %d rows" % len(rec["t0"]))
    ok(meta is None or (len(meta["distractor_files"]) >= 2 and all(x in files for x in meta["distractor_files"])),
       "input gate: two distractors named in metadata.json")
    p27 = c["plan"]
    ok(p27["t0"].min() >= a27 and p27["t0"].max() < b27, "the planning traffic covers the local summer 2027 season")
    ok(rec["t0"].min() >= int(W.ACTUAL_START.timestamp()) and rec["t0"].max() < int(W.ACTUAL_END.timestamp()),
       "the flight data covers 1 Jan 2025 to 30 Sep 2026")
    ok(occ["ts"].max() < int(W.ACTUAL_END.timestamp()), "no occurrence dated after 30 Sep 2026")

    # ---------------------------------------------------------------- realism sweep
    ok(len({c["L"][(s, "all")] for s in S}) >= 5, "realism: loss counts differ across sectors")
    ok(all(round(c["ex"][(s, "all")]["fh"]) % 100 for s in S), "realism: no round flight-hour totals")
    texts = []
    for f in files:
        if f.endswith((".csv", ".md", ".json")):
            texts.append(open(os.path.join(target, f), encoding="utf-8").read())
        elif f.endswith(".pdf"):
            with pdfplumber.open(os.path.join(target, f)) as pdf:
                texts.append("\n".join(pg.extract_text() or "" for pg in pdf.pages))
    ok(not any("—" in t or "–" in t for t in texts), "no em or en dash anywhere in the pack")
    people = set(json.load(open(os.path.join(HERE, "..", "..", ".claude", "skills", "fingerprint", "cards",
                                             "task181.json")))["world"]["people"])
    named = set(W.PEOPLE.values()) | {"Kenny Lassen"}
    ok(named <= people, "every persona in the pack is on the card (%s)" % ", ".join(sorted(named)))
    for t in texts:
        for bad in ("crossing", "decoy", "golden", "trap", "re-filed", "refiled", "duplicate"):
            if bad in t.lower():
                ok(False, "the pack never names %r" % bad)
    ok(True, "the pack never names a crossing, a re-filing or a duplicate")
    # goldens
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    ok(fig["sectors_over_tolerance"] == ["Tarvik"], "figures.json carries the call")
    ok(sorted(os.listdir(golden)) == sorted([DL.DECK, DL.CSV]), "exactly the two goldens the prompt names")
    print("checks: %d passed" % N[0])
    return N[0]


if __name__ == "__main__":
    task = os.path.dirname(HERE)
    run(os.path.join(task, "target"), os.path.join(task, "golden"), meta_path=os.path.join(task, "metadata.json"))
