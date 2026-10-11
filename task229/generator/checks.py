"""Assertions over the built pack: the ladder, the grid, the asks' stops, separation, gates, bins.

Run after build.py. Everything is computed from target/ through golden.py, plus the simulated world
where an assertion is about the world itself (separation, the clean-data test)."""
import collections
import datetime as dt
import itertools
import json
import os
import re
import shutil
import sys
import tempfile

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as G
import world as W

N = [0]


def ok(cond, msg):
    N[0] += 1
    if not cond:
        raise AssertionError(msg)


GOLD_FIRE = ("EM3.10.9", "EM3.12.1", "PX5.2.7")


def edge(x):
    return 0.005 - abs((x * 100) % 1 - 0.5) / 100


def run(target, world=None, quiet=False):
    D, g = G.solve(target)
    sc = g["scorecard"]
    log = []

    # ---------------------------------------------------------------- the call
    ok(g["fire"] == GOLD_FIRE, "golden fire set moved: %s" % (g["fire"],))
    hold = tuple(sorted(r for r in G.RELEASES if r not in GOLD_FIRE))
    ok(len(hold) == 5, "five builds hold")
    for r in G.RELEASES:
        v = sc[r]
        m = v["rh"] - v["lcl"]
        ok(abs(m) >= 0.05, "%s sits %.4f from its limit" % (r, m))
        ok(edge(v["rh"]) >= 0.0015 and edge(v["lcl"]) >= 0.0015, "%s two-decimal edge" % r)
    margins = sorted(sc[r]["rh"] - sc[r]["lcl"] for r in G.RELEASES)
    ok(min(b - a for a, b in zip(margins, margins[1:])) >= 0.04, "order by distance to the limit is not a near tie")

    # ---------------------------------------------------------------- the ladder
    vers = {w: G.versions(D["mdm"], w) for w in ("cutoff", "latest", "first")}
    pops = {m: G.assessed(D, m) for m in ("fullweek", "start", "end")}
    rung = {
        "R0 latest deliveries, every installation on its end-of-week build, pooled reads, read-count error": ("latest", "end", "pooled", "binomial_reads"),
        "R1 + reads held at the cut-off": ("cutoff", "end", "pooled", "binomial_reads"),
        "R2 + installations that ran the build all week": ("cutoff", "fullweek", "pooled", "binomial_reads"),
        "R3 + the average installation": ("cutoff", "fullweek", "installation", "binomial_reads"),
        "R4 + installation-level error (the answer)": ("cutoff", "fullweek", "installation", "installation"),
    }
    expect = [("EM3.10.9", "EM3.12.2", "PX5.3.0", "PX5.3.1"),
              ("EM3.10.9", "EM3.12.0", "EM3.12.2", "PX5.2.7", "PX5.3.0", "PX5.3.1"),
              ("EM3.10.9", "EM3.12.0", "PX5.2.7", "PX5.3.0", "PX5.3.1"),
              ("EM3.10.9", "EM3.12.0", "EM3.12.1", "PX5.2.7", "PX5.3.1"),
              GOLD_FIRE]
    sets = []
    for (name, cell), want in zip(rung.items(), expect):
        fs = G.fire_set(G.score(vers[cell[0]], pops[cell[1]], cell[2], cell[3]))
        ok(fs == tuple(sorted(want)), "%s fires %s" % (name, fs))
        sets.append(fs)
        log.append("%s -> fires %s" % (name, ", ".join(fs)))
    ok(len(set(sets)) == len(sets), "every rung names a different set")

    # ---------------------------------------------------------------- the grid, cell by cell
    units = ("installation", "pooled", "row", "stream")
    errs = ("installation", "binomial_reads", "binomial_installations", "none")
    golden_cells = []
    cells = 0
    for v, p, u, e in itertools.product(vers, pops, units, errs):
        fs = G.fire_set(G.score(vers[v], pops[p], u, e))
        cells += 1
        if fs == GOLD_FIRE:
            golden_cells.append((v, p, u, e))
    ok(cells == 144, "grid size")
    ok(golden_cells == [("cutoff", "fullweek", "installation", "installation"), ("first", "fullweek", "installation", "installation")],
       "only the standard's reading (and the first-delivery reading, which moves figures but not the call) lands the call: %s" % golden_cells)
    first = G.score(vers["first"], pops["fullweek"])
    moved = [r for r in G.RELEASES if round(first[r]["rh"], 2) != round(sc[r]["rh"], 2)]
    ok(len(moved) >= 4, "the first-delivery reading moves at least four graded read-health figures: %s" % moved)
    log.append("grid: %d cells; the call lands only on the standard's reading and on first-delivery (which moves %d read-health figures)" % (cells, len(moved)))

    # convergent readings (C1): same population and same figures
    sp_fail = G.running_builds(D["hes"], D["img2rel"], failed_moves=True)
    sp_raw = G.running_builds(D["hes"], D["img2rel"], dedupe=False)
    ok(G.assessed(D, "fullweek", sp_fail) == pops["fullweek"], "a failed activation read as a move changes no assessed installation")
    ok(G.assessed(D, "fullweek", sp_raw) == pops["fullweek"], "replayed events change no assessed installation")
    sc0 = G.score(vers["cutoff"], pops["fullweek"], "installation", "installation_ddof0")
    ok(G.fire_set(sc0) == GOLD_FIRE, "n divisor: same call")
    dd = [r for r in G.RELEASES if round(sc0[r]["lcl"], 2) != round(sc[r]["lcl"], 2)]
    ok(dd == ["PX5.3.1"], "the n divisor moves only the 37-installation pilot's limit at two decimals: %s" % dd)
    # installation-day mean equals the installation mean for every assessed installation
    x = vers["cutoff"][vers["cutoff"]["NMI"].isin(pops["fullweek"].keys())]
    day = x.groupby(["NMI", "READ_DATE"])[["QTY_A", "expected"]].sum()
    day_mean = (100 * day["QTY_A"] / day["expected"]).groupby(level=0).mean()
    wk = x.groupby("NMI")[["QTY_A", "expected"]].sum()
    wk_share = 100 * wk["QTY_A"] / wk["expected"]
    ok(float((day_mean - wk_share).abs().max()) < 1e-9, "installation-day mean equals the installation's week share")
    gap = (D["mdm"]["cutoff"] - D["mdm"]["received"]).dt.total_seconds().abs() / 60
    ok(float(gap.min()) >= 8.0, "no delivery lands within 8 minutes of its cut-off")
    # every row's expected count is the day's interval count
    ok(bool(((D["mdm"]["expected"] * D["mdm"]["INTERVAL_LENGTH"]) == 1440).all()), "every register-day carries a full day of intervals")

    # the deciding contrasts, both directions
    pooled = G.score(vers["cutoff"], pops["fullweek"], "pooled", "installation")
    ok(pooled["PX5.3.0"]["rh"] < pooled["PX5.3.0"]["lcl"] - 0.3 and not sc["PX5.3.0"]["fire"], "PX5.3.0: pooled reads fire, the average installation holds")
    ok(pooled["EM3.12.1"]["rh"] >= 99.52 and sc["EM3.12.1"]["fire"], "EM3.12.1: pooled reads clear the reference, the average installation fires")
    late = G.score(vers["latest"], pops["fullweek"])
    ok(not late["PX5.2.7"]["fire"] and late["PX5.2.7"]["rh"] - late["PX5.2.7"]["lcl"] >= 0.2, "PX5.2.7 holds on the latest deliveries")
    end = G.score(vers["cutoff"], pops["end"])
    ok(end["EM3.12.2"]["fire"] and not sc["EM3.12.2"]["fire"], "EM3.12.2 fires once the week's movers are counted on it")
    binom = G.score(vers["cutoff"], pops["fullweek"], "installation", "binomial_reads")
    ok(binom["EM3.12.0"]["fire"] and binom["PX5.3.1"]["fire"], "a read-count error makes EM3.12.0 and PX5.3.1 breach")
    heavy_share = None
    if world is not None:
        insts = world["insts"]
        px = [i for i in insts if i.group == "full" and i.build_start == "PX5.3.0"]
        hv = [i for i in px if i.profile in W.HEAVY]
        reads = lambda i: len(W.PROFILES[i.profile][0]) * 1440 // W.PROFILES[i.profile][1]
        heavy_share = sum(reads(i) for i in hv) / sum(reads(i) for i in px)
        ok(0.70 <= heavy_share <= 0.85 and len(hv) / len(px) < 0.2, "PX5.3.0: under a fifth of installations, most of the reads")
        e1 = [i for i in insts if i.group == "full" and i.build_start == "EM3.12.1"]
        h1 = [i for i in e1 if i.profile in W.HEAVY]
        ok(sum(reads(i) for i in h1) / sum(reads(i) for i in e1) >= 0.75, "EM3.12.1: the healthy heavy installations carry most of the reads")
    log.append("deciding contrasts: PX5.3.0 pooled %.2f vs average %.2f; EM3.12.1 pooled %.2f vs average %.2f; PX5.2.7 latest %.2f vs cut-off %.2f"
               % (pooled["PX5.3.0"]["rh"], sc["PX5.3.0"]["rh"], pooled["EM3.12.1"]["rh"], sc["EM3.12.1"]["rh"], late["PX5.2.7"]["rh"], sc["PX5.2.7"]["rh"]))

    # clean-data and lens-swap tests: drop every delivery after its cut-off and every mover; the
    # pooled read-count pipeline still files a different set, and the populations differ
    ok(G.fire_set(G.score(vers["cutoff"], pops["fullweek"], "pooled", "binomial_reads")) != GOLD_FIRE, "clean data: pooled still wrong")
    ok(G.fire_set(G.score(vers["cutoff"], pops["fullweek"], "pooled", "installation")) != GOLD_FIRE, "clean data: pooled with an installation error still wrong")
    ok(len(pops["end"]) - len(pops["fullweek"]) >= 1100, "the naive population is not the assessed population")

    # ---------------------------------------------------------------- ask A: Wave 8 moves
    a = g["wave8"]
    ok(a == {"EM3.12.2": 1274, "PX5.3.1": 109}, "wave 8 moves %s" % a)
    wb = __import__("openpyxl").load_workbook(os.path.join(target, "wave8_schedule.xlsx"), read_only=True)
    raw = []
    for name in ("Batch A 13-10", "Batch B 14-10"):
        for r_ in list(wb[name].iter_rows(values_only=True))[2:]:
            raw.append(dict(serial=str(r_[1]), nmi=r_[2], target=r_[5]))
    raw = pd.DataFrame(raw)
    rows_ct = raw.groupby("target").size().to_dict()
    ok(rows_ct != a, "schedule row count is not the answer")
    pad = raw.assign(serial=raw["serial"].str.zfill(8)).drop_duplicates()
    ok(pad.groupby("target").size().to_dict() != a, "distinct scheduled meters is not the answer")
    by_nmi = raw.fillna("").drop_duplicates(["nmi", "target"]).groupby("target").size().to_dict()
    ok(by_nmi != a, "collapsing on the NMI column (blanks included) is not the answer")
    log.append("wave 8: rows %s, distinct meters %s, one-per-NMI-cell %s, answer %s" % (rows_ct, pad.groupby("target").size().to_dict(), by_nmi, a))

    # ---------------------------------------------------------------- ask B: Wave 7 cost
    b = g["wave7"]
    ok(b == {"EM3.12.2": {"installations": 1109, "missing": 16415}, "PX5.3.1": {"installations": 63, "missing": 933}}, "wave 7 cost %s" % b)
    for clock in ("UTC", "AEDT"):
        bb = G.wave7_cost(D, vers["cutoff"], clock)
        ok(bb["EM3.12.2"]["missing"] != b["EM3.12.2"]["missing"], "%s move day lands elsewhere" % clock)
        log.append("wave 7 missing reads on the %s day: %s" % (clock, {k: v["missing"] for k, v in bb.items()}))
    bl = G.wave7_cost(D, vers["latest"])
    ok(bl["EM3.12.2"]["missing"] < b["EM3.12.2"]["missing"], "the latest deliveries understate the move-day loss")
    log.append("wave 7 missing reads on latest deliveries: %s" % {k: v["missing"] for k, v in bl.items()})

    # ---------------------------------------------------------------- chronology (H16)
    if world is not None:
        import records as R
        inv = {v: k for k, v in R.ALL_IMAGES.items()}
        early = sum(1 for es in world["ev"].values() for e in es
                    if e["image"] and e["type"] in ("COMMISSIONED", "FW_ACTIVATED")
                    and e["at"].date() < dt.date.fromisoformat(R.RELEASED[inv[e["image"]]]))
        ok(early == 0, "no meter runs an image before its release date (%d)" % early)
        late = sum(1 for es in world["ev"].values() for e in es if e["at"] > W.EXTRACT_AT)
        ok(late == 0, "no event after the extract")

    # ---------------------------------------------------------------- separation
    if world is not None:
        dev = {i.nmi for i in world["insts"] if i.group in ("w7", "exch")}
        ok(not (dev & set(pops["fullweek"].keys())), "no mover or exchanged installation sits in the main population")
        sched_full = {row["inst"].nmi for row in world["sched"] if row["inst"].group == "full"}
        ok(len(sched_full) > 1000, "schedule rows for full-week installations are separate records, not main-path rows")

    # ---------------------------------------------------------------- gates
    files = sorted(os.listdir(target))
    ok(len(files) >= 10, "ten files")
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(fmts) >= 3, "three formats: %s" % fmts)
    ok(len(D["mdm"]) >= 25000, "a file of 25,000 rows")
    meta = json.load(open(os.path.join(os.path.dirname(target), "metadata.json"))) if os.path.exists(os.path.join(os.path.dirname(target), "metadata.json")) else None
    if meta:
        ok(len(meta["distractor_files"]) >= 2, "two distractors")
        tmp = tempfile.mkdtemp()
        for f in files:
            if f not in meta["distractor_files"]:
                shutil.copy(os.path.join(target, f), tmp)
        _, g2 = G.solve(tmp)
        shutil.rmtree(tmp)
        ok(g2["fire"] == g["fire"] and g2["wave8"] == g["wave8"] and g2["wave7"] == g["wave7"], "the golden ignores the distractors")
    # single statement: the reference and the cut-off hour are stated only in the standard
    txt = {f: open(os.path.join(target, f), errors="ignore").read() for f in files if f.endswith((".md", ".csv")) and "mdm_" not in f}
    for needle in ("99.50", "06:00"):
        hits = [f for f, t in txt.items() if needle in t]
        ok(not hits, "%s stated outside the standard: %s" % (needle, hits))
    for f in files:
        ok("distract" not in f.lower(), "no file named for its role")
    if not quiet:
        print("checks: %d assertions passed" % N[0])
        for line in log:
            print("  " + line)
    return N[0], log


if __name__ == "__main__":
    run(os.path.join(os.path.dirname(HERE), "target"))
