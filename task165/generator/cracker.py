"""task165 cracker, mirror, the two blind readers' paths and the judge's literal readings, run on the cut pack: the pair
ceiling, the mirror's leakage, and what each path keeps of the 20 ask figures.

The measured opponents are the two blind scored readers (medium threads that saw only prompt.txt and target/), whose
own methods are re-implemented here as their paths on the asks, and the determinism judge's literal readings:
  reader 1  domes: the survey's stock brought forward by every weighing in less every weighing out after each flight's
            start (the flight log's UTC taken to Eastern daylight time), a weighing at another yard's scale counted at
            the dome its remarks name, transfers out at Ridge and in at Lakeshore, the wet load netting to nil, and the
            BOOKED October lines of the 21 September dispatch issue; room is the rated capacity less the stock.
            arterials: the platform's rock salt rows on A circuits under the yard of the route code as run, local
            season dates, the fleet list's older controllers halved (the fleet list names none, so nothing is), and
            Kettlewood's returns added under its City circuit's yard;
  reader 2  domes: the same, from each flight's end; arterials: the older controllers found from their rows and each
            of their runs counted once, the brine left in, the realigned circuits taken back to Mapleford through the
            revision log, Kettlewood's returns added;
  judge     the double weighings kept (domes); the brine kept, and the brine's salt (23 per cent of its 1.18 kg a litre)
            taken off every row (arterials), each on reader 2's arterial path.
The cracker lands the call and takes a path on the asks; the mirror stops at the default path (the Priority 1
collectors' rate less the new streets' own Priority 2 salt) and is as careful on the asks. Each response is scored on
Part 0's weights: the call and its components 38, the instructions 7, the asks 55 shared over every ask figure and the
chart's parts. The variants re-run each reader's path with one new device found at a time.

    python3 cracker.py [target]"""
import datetime as dt
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C  # noqa: E402

TARGET = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
W_CALL, W_IF, W_ASK = 38.0, 7.0, 55.0
CHART_PARTS = 2          # every yard and winter shown and labelled; the title
CHART_CONTENT = 1        # the chart carries Ask B's figures
W3 = ["2023-24", "2024-25", "2025-26"]
BRINE_SALT = 0.23        # the plan's plant brine, salt by weight


def r1(v):
    return round(v + 1e-9, 1)


def ask_points(stock, room, art, gold):
    gs, gr, ga = gold
    ka = sum(1 for y in C.YARDS if r1(stock[y]) == r1(gs[y])) + sum(1 for y in C.YARDS if r1(room[y]) == r1(gr[y]))
    kb = sum(1 for k in ga if C.r50(art[k]) == C.r50(ga[k]))
    content = 1 if kb == len(ga) else 0
    n = 8 + 12 + CHART_CONTENT + CHART_PARTS
    keep = ka + kb + content + CHART_PARTS
    return keep / n * W_ASK, (ka, kb, content), keep, n


def reader_domes(target, cutoff="start", dedupe=False):
    """A reader's dome path; dedupe: False (every weighing kept), "weights" (only the exact repeats of gross, tare and
    net dropped) or True (a truck weighed in at two scale houses inside a round trip on one gross counted once)."""
    return C.ask_a(target, cutoff=cutoff, dedupe=dedupe)


def reader_arterials(target, back=False, older="fleet"):
    """A reader's arterial path. back: the circuit codes taken back through the revision log; older: fleet (the fleet
    list's older controllers halved, reader 1's own step), runs (each older run once, the brine left in, reader 2's),
    full (each older run once, the brine's weight off), salt_all (each older run once and the brine's salt off every
    row, the judge's reading) or salt_old (the same on the older runs only); the older controllers found from their
    own rows."""
    ps = pd.read_parquet(os.path.join(target, C.F_PASSES))
    ps = ps[(ps["material_code"] == "RS") & ps["route_code"].str.contains("-A")].copy()
    ps["local"] = ps["entry_utc"].dt.tz_convert("America/Toronto").dt.tz_localize(None)
    ps["winter"] = [C.season_of_local(t) for t in ps["local"]]
    ps = ps[ps["winter"].isin(W3)].copy()
    ps["day"] = ps["local"].dt.date
    if back:
        hist = C.circuit_history(target)
        codes = [hist[rc][0] if rc in hist and d < hist[rc][1] else rc for rc, d in zip(ps["route_code"], ps["day"])]
    else:
        codes = list(ps["route_code"])
    ps["yard"] = ["MPF" if rc in ("MPF-A01", "MPF-A02") and d < dt.date(2026, 7, 1) else rc[:3]
                  for rc, d in zip(codes, ps["day"])]
    brine_t = ps["prewet_l"] * C.BRINE_KG_L / 1000.0
    if older == "fleet":
        fl = pd.read_csv(os.path.join(target, C.F_FLEET), dtype=str)
        retro = {}
        if "spreader_controller" in fl.columns:
            for u, c, d in zip(fl["unit_id"], fl["spreader_controller"], fl.get("controller_retrofit", [None] * len(fl))):
                if c == "M410" or isinstance(d, str):
                    retro[u] = dt.date.fromisoformat(d) if isinstance(d, str) else None
        m410 = pd.Series([u in retro and (retro[u] is None or d < retro[u]) for u, d in zip(ps["unit_id"], ps["day"])],
                         index=ps.index)
        v = ps["applied_t"].where(~m410, ps["applied_t"] / 2.0)
        tot = v.groupby([ps["yard"], ps["winter"]]).sum()
    else:
        olduw = C.older_unit_winters(ps)
        ps["m410"] = [(u, w) in olduw for u, w in zip(ps["unit_id"], ps["winter"])]
        if older == "runs":
            ps["solid"] = ps["applied_t"]
        elif older == "full":
            ps["solid"] = ps["applied_t"] - brine_t.where(ps["m410"], 0.0)
        elif older == "salt_all":
            ps["solid"] = ps["applied_t"] - BRINE_SALT * brine_t
        elif older == "salt_old":
            ps["solid"] = ps["applied_t"] - (BRINE_SALT * brine_t).where(ps["m410"], 0.0)
        else:
            raise ValueError(older)
        a_ = ps[~ps["m410"]].groupby(["yard", "winter"])["solid"].sum()
        b_ = ps[ps["m410"]].groupby(["yard", "winter", "run_ref"])["solid"].first().groupby(level=[0, 1]).sum()
        tot = pd.concat([a_, b_]).groupby(level=[0, 1]).sum()
    out = {(y, w): float(tot.get((y, w), 0.0)) for y in C.YARDS for w in W3}
    xl = pd.ExcelFile(os.path.join(target, C.F_PELLARD))
    for w in W3:
        df = xl.parse(w, header=2)
        df = df[df["Month"].notna()]
        df = df[[C.season_of_local(pd.Timestamp(m + "-01")) == w for m in df["Month"]]]
        for rc, t in zip(df["City circuit"], df["Rock salt (t)"]):
            out[(rc[:3], w)] += float(t)
    return out


def litres_per_tonne(target):
    """The consistency check on the arterial rows against the plan's 40 litres a tonne: the median litres of pre-wet a
    tonne for the unit-winters whose runs repeat one total and for every other row, as written and under each handling
    of the brine."""
    ps = pd.read_parquet(os.path.join(target, C.F_PASSES))
    ps = ps[(ps["material_code"] == "RS") & ps["route_code"].str.contains("-A") & (ps["prewet_l"] > 0)].copy()
    ps["local"] = ps["entry_utc"].dt.tz_convert("America/Toronto").dt.tz_localize(None)
    ps["winter"] = [C.season_of_local(t) for t in ps["local"]]
    ps = ps[ps["winter"].isin(W3)].copy()
    olduw = C.older_unit_winters(ps)
    old = np.array([(u, w) in olduw for u, w in zip(ps["unit_id"], ps["winter"])])
    lit, t = ps["prewet_l"].to_numpy(), ps["applied_t"].to_numpy()
    b = lit * C.BRINE_KG_L / 1000.0
    med = lambda a: float(np.median(a))
    return {"newer as written": med(lit[~old] / t[~old]),
            "newer, brine's salt off": med(lit[~old] / (t - BRINE_SALT * b)[~old]),
            "older as written": med(lit[old] / t[old]),
            "older, brine's salt off": med(lit[old] / (t - BRINE_SALT * b)[old]),
            "older, brine's weight off": med(lit[old] / (t - b)[old])}


def main(target=TARGET, quiet=False):
    P = C.Pack(target)
    gold_call = round(C.golden(P) / 100.0) * 100
    gs, gr = C.ask_a(target)
    ga = C.arterial_salt(target)
    gold = (gs, gr, ga)
    mirror_call = round(C.r1_default(P) / 100.0) * 100
    paths = {
        "reader 1": (reader_domes(target, "start"), reader_arterials(target, older="fleet")),
        "reader 2": (reader_domes(target, "time"), reader_arterials(target, back=True, older="runs")),
    }
    readings = {
        "judge, double weighings kept": (reader_domes(target, "time"), None),
        "judge, brine kept": (None, reader_arterials(target, back=True, older="runs")),
        "judge, brine's salt off every row": (None, reader_arterials(target, back=True, older="salt_all")),
        "judge, brine's salt off the older runs": (None, reader_arterials(target, back=True, older="salt_old")),
    }
    lines, out = [], {}
    for who, ((st, rm), art) in paths.items():
        for role, call in (("cracker", gold_call), ("mirror", mirror_call)):
            m = W_CALL if call == gold_call else 5.0
            pts, (ka, kb, cc), keep, n = ask_points(st, rm, art, gold)
            out[(who, role)] = (m + W_IF + pts, pts, ka, kb)
        tot, pts, ka, kb = out[(who, "cracker")]
        lines.append("%s's path: asks %4.1f of %.0f (domes %d of 8, arterials %d of 12) -> cracker %5.1f, mirror %5.1f, "
                     "pair %5.1f" % (who, pts, W_ASK, ka, kb, tot, out[(who, "mirror")][0],
                                     (tot + out[(who, "mirror")][0]) / 2))
    hits = {}
    for name, (dm, art) in readings.items():
        if dm is not None:
            st, rm = dm
            hits[name] = sum(1 for y in C.YARDS if r1(st[y]) == r1(gs[y])) + \
                sum(1 for y in C.YARDS if r1(rm[y]) == r1(gr[y]))
            lines.append("%-42s domes %d of 8" % (name, hits[name]))
        else:
            hits[name] = sum(1 for k in ga if C.r50(art[k]) == C.r50(ga[k]))
            lines.append("%-42s arterials %d of 12" % (name, hits[name]))
    r1d, r1a = paths["reader 1"]
    r2d, r2a = paths["reader 2"]
    variants = {
        "reader 1 + exact repeats dropped": (reader_domes(target, "start", "weights"), r1a),
        "reader 1 + truck inside a round trip once": (reader_domes(target, "start", True), r1a),
        "reader 1 + older runs once, brine kept": (r1d, reader_arterials(target, older="runs")),
        "reader 1 + codes taken back": (r1d, reader_arterials(target, back=True, older="fleet")),
        "reader 2 + exact repeats dropped": (reader_domes(target, "time", "weights"), r2a),
        "reader 2 + truck inside a round trip once": (reader_domes(target, "time", True), r2a),
        "reader 2 + brine's weight off the older runs": (r2d, reader_arterials(target, back=True, older="full")),
    }
    single = {}
    mir = out[("reader 2", "mirror")][0]
    for name, ((st, rm), art) in variants.items():
        pts, parts, keep, n = ask_points(st, rm, art, gold)
        tot = W_CALL + W_IF + pts
        single[name] = (parts[0] + parts[1], tot, (tot + mir) / 2)
        lines.append("%-46s asks %5.1f (domes %d/8, arterials %d/12) -> %5.1f; pair %5.1f" % (
            name, pts, parts[0], parts[1], tot, (tot + mir) / 2))
    pair = max((out[(w, "cracker")][0] + out[(w, "mirror")][0]) / 2 for w in paths)
    leak = max(out[(w, "mirror")][1] for w in paths) / W_ASK * 100
    reader_hits = {w: out[(w, "cracker")][2] + out[(w, "cracker")][3] for w in paths}
    lpt = litres_per_tonne(target)
    lines.append("litres a tonne (median): " + "; ".join("%s %.2f" % kv for kv in lpt.items()))
    lines.append("Pair ceiling (the readers' paths): %.1f" % pair)
    lines.append("Mirror leakage: %.1f per cent of ask weight" % leak)
    if not quiet:
        print("\n".join(lines))
    return {"pair": pair, "leak": leak, "reader_hits": reader_hits, "readings": hits, "single": single, "lpt": lpt,
            "lines": lines}


if __name__ == "__main__":
    main()
