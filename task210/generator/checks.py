"""The generator's assertions, run on every build against the clean truth and the cut pack.

R1 to R3c are the client's three rules executed (dataset-generation 7.1); SF1 to SF22 are the semantic fork
table's rows; the rest are the ladder and its reflex routes, the estimator family, the ask devices and their
bins, the realism sweep and the input gates."""
import csv
import datetime as dt
import json
import os
import re
import sqlite3
import subprocess
from collections import Counter, defaultdict

import numpy as np

import golden as G
import pack as PK
import routes as RT
import sim
import world as W

PASSED = []


def ok(label, cond, detail=""):
    if not cond:
        raise AssertionError("%s FAILED %s" % (label, detail))
    PASSED.append(label)


def pdf_text(path):
    from pypdf import PdfReader
    r = PdfReader(path, strict=True)
    a = "\n".join(p.extract_text() or "" for p in r.pages)
    b = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    return a, b, len(r.pages)


def edge(x):
    """Distance of a figure from its one-decimal rounding edge, in tenths (0.5 is mid-bin)."""
    return abs((x * 10) % 1 - 0.5)


def hours(iv):
    return sum(b - a for a, b in G.union(iv)) / 3600.0


def overl(x, ys):
    return any(min(x[1], y[1]) > max(x[0], y[0]) for y in ys)


def count_starts(iv):
    """The 12/24 count read the other way: a 24-hour block counts only where a discharge starts in it."""
    u = G.union(iv)
    n, k = 0, 0
    while k < len(u):
        end = u[k][0] + 12 * 3600.0
        n += 1
        while k < len(u) and u[k][0] < end:
            k += 1
        while k < len(u) and u[k][0] < end + 24 * 3600.0:
            n += 1
            end += 24 * 3600.0
            while k < len(u) and u[k][0] < end:
                k += 1
    return n


def months_utc(iv):
    m = [0.0] * 12
    for a, b in G.union(iv):
        t = a
        while t < b:
            d = G.T0 + dt.timedelta(seconds=t)
            nm = dt.datetime(d.year + (d.month == 12), d.month % 12 + 1, 1)
            e = min(b, (nm - G.T0).total_seconds())
            m[d.month - 1] += (e - t) / 3600
            t = e
    return m


def months_local(iv):
    m = [0.0] * 12
    for a, b in G.union(iv):
        t = a
        while t < b:
            ld = G.utc_to_local(t)
            nm = dt.datetime(ld.year + (ld.month == 12), ld.month % 12 + 1, 1)
            nm_utc = (nm - G.T0).total_seconds()
            nm_utc = nm_utc - 3600 if G.BST0 <= nm_utc - 3600 < G.BST1 else nm_utc
            e = min(b, nm_utc)
            m[ld.month - 1] += (e - t) / 3600
            t = e
    return m


def clean_delivered(S, code):
    e = [(t, p, sg, 0.0) for (t, p, sg) in S["stations"][code]["events"]]
    w = W.BY_CODE[code]
    V = S["stations"][code]["area"] * (w["start"] - w["stop"])
    return float(np.median([x[2] for x in G.cycle_rates(e, V)]))


def run(tgt, S, g, info, figs):
    PASSED.clear()
    task = os.path.dirname(tgt)
    st = g["stations"]
    K = g["call_code"]
    L = g["routes"]
    F = PK.FILES

    # ------------------------------------------------------------ the call
    ok("call.one breach", g["breach"] == ["SPS0412"], g["breach"])
    ok("call.gallowfen", g["call"] == "Gallowfen PS storm overflow", g["call"])
    ok("call.delivered under pff", g["delivered"][K] < 0.70 * g["pff"][K], (g["delivered"][K], g["pff"][K]))
    ok("call.every other station clears", all(g["margin"][c] >= 1.12 for c in st if c != K),
       min(g["margin"][c] for c in st if c != K))
    ok("call.k spilled", g["lines"][K]["spills"] >= 6, g["lines"][K]["spills"])

    # ------------------------------------------------------------ R1 the field's raw material ships
    con = sqlite3.connect(os.path.join(tgt, F["telemetry"]))
    cols = {t: [r[1] for r in con.execute("PRAGMA table_info(%s)" % t)] for t in ("rtu", "pump_event", "wet_well_level", "alarm")}
    n_events = con.execute("SELECT COUNT(*) FROM pump_event").fetchone()[0]
    alarm_types = Counter(r[0] for r in con.execute("SELECT alarm FROM alarm"))
    con.close()
    ok("R1.cycle records ship", n_events > 100000, n_events)
    allcols = [c.lower() for v in cols.values() for c in v]
    for f in ("consents", "meters", "edm_log", "edm_status", "edm_list", "workorders", "rain", "borehole"):
        with open(os.path.join(tgt, F[f]), newline="", encoding="utf-8") as fh:
            allcols += [c.lower() for c in next(csv.reader(fh))]
    ok("R1.no column holds a delivered rate", not any(re.search(r"deliver|actual|measured_flow|pass_forward_actual|achieved", c)
                                                      for c in allcols), allcols)

    # ------------------------------------------------------------ R2 each Layer 1 item real and neutral
    ev_raw = defaultdict(list)
    con = sqlite3.connect(os.path.join(tgt, F["telemetry"]))
    for rtu, pump, state, ts, lvl in con.execute("SELECT rtu, pump, state, event_utc, wet_well_m FROM pump_event"):
        ev_raw[rtu].append((G.utc_sec(ts), pump, 1 if state == "RUN" else 0, lvl))
    con.close()
    n_dup = sum(len(v) for v in ev_raw.values()) - sum(len(set(v)) for v in ev_raw.values())
    ok("R2.re-sent events present", n_dup == info["telemetry_dups"] and n_dup > 50, (n_dup, info["telemetry_dups"]))
    for k in ev_raw:
        ev_raw[k].sort()
    dl_raw = G.delivered(st, ev_raw)
    ok("R2.re-sent events neutral", all(round(dl_raw[c]) == round(g["delivered"][c]) for c in st),
       {c: (dl_raw[c], g["delivered"][c]) for c in st})
    m3h = [c for c in st if W.BY_CODE[c]["unit"] == "m3/h"]
    ok("R2.duty in m3/h neutral", all(st[c]["rated"][1] * 3.6 >= g["pff"][c] for c in m3h) and len(m3h) >= 3, m3h)
    ok("R2.duty units converted", abs(st["SPS0412"]["rated"][1] - W.BY_CODE["SPS0412"]["rated"]) < 0.05, st["SPS0412"]["rated"])
    ok("R2.comms gaps drop level polls only", info["telemetry_levels"] < 14 * 35040, info["telemetry_levels"])
    # EDM local time read as UTC: the call does not read the EDM's clock (Gallowfen discharged either way)
    ok("R2.EDM clock neutral to the call", len(g["log"][st[K]["edm"]]) > 0 and len(g["alarms"][st[K]["rtu"]]) > 0)
    ok("R2.retired serials neutral to the call", K not in W.EDM_REPLACED)

    # ------------------------------------------------------------ R3a the analyst test on the clean truth
    truth = {c: clean_delivered(S, c) for c in st}
    ok("R2.clean truth agrees with the cut pack", all(abs(truth[c] - g["delivered"][c]) < 0.15 for c in st),
       {c: (round(truth[c], 2), round(g["delivered"][c], 2)) for c in st})
    spilled = {c: len(S["stations"][c]["spills"]) > 0 for c in st}
    rated_route = [c for c in st if spilled[c] and W.BY_CODE[c]["rated"] < W.BY_CODE[c]["pff"]]
    ok("R3a.rated duty on the clean truth files none", rated_route == [], rated_route)
    for c in st:
        if W.BY_CODE[c]["meter"]:
            q = S["stations"][c]["meter_15"]
            vals = [q[k] for a, b in S["stations"][c]["spills"] for k in range(int(a // 900) + 1, int(b // 900))]
            ok("R3a.meter clears the permit while spilling %s" % c, np.median(vals) >= W.BY_CODE[c]["pff"], np.median(vals))
    ok("R3a.rated duty on the cut pack files none", L["R1"] == ["none"], L["R1"])
    cr = {}
    for c in st:
        e = S["stations"][c]["events"]
        V = S["stations"][c]["area"] * (W.BY_CODE[c]["start"] - W.BY_CODE[c]["stop"])
        runs = [V / (e[k + 1][0] - e[k][0]) for k in range(len(e) - 1)
                if e[k][2] == 1 and e[k + 1][2] == 0 and 0 < e[k + 1][0] - e[k][0] <= 6 * 3600]
        cr[c] = float(np.median(runs)) / W.BY_CODE[c]["pff"]
    ok("R3a.drawdown without the inflow on the clean truth files Hagworth Wold", min(cr, key=cr.get) == "SPS0415"
       and sum(1 for c in cr if cr[c] < 1) <= 4, sorted((round(v, 3), c) for c, v in cr.items())[:4])
    rain = S["rain"]
    mins = np.arange(len(rain[0]))
    lday = (mins + np.where((mins >= sim.BST0) & (mins < sim.BST1), 60, 0)) // 1440
    dry = {}
    for c in st:
        drain = np.bincount(lday, weights=rain[W.ZONES.index(W.BY_CODE[c]["zone"])])
        n = 0
        for a, b in S["stations"][c]["spills"]:
            d = int((a / 60 + (60 if sim.BST0 <= a / 60 < sim.BST1 else 0)) // 1440)
            n += drain[d] < 0.25 and (d == 0 or drain[d - 1] < 0.25)
        dry[c] = n
    ok("R3a.dry-day screen on the clean truth files Hagworth Wold alone", [c for c in st if dry[c]] == ["SPS0415"], dry)
    drain_h = np.bincount(lday, weights=rain[W.ZONES.index(W.BY_CODE["SPS0415"]["zone"])])
    late = [a for a, b in S["stations"]["SPS0415"]["spills"]
            if (lambda d: drain_h[d] < 0.25 and (d == 0 or drain_h[d - 1] < 0.25))(
                int((a / 60 + (60 if sim.BST0 <= a / 60 < sim.BST1 else 0)) // 1440)) and a >= 90 * 86400]
    ok("letter.Hagworth Wold's dry-day discharges all fall in January to March", not late, len(late))
    sp = {c: G.count_1224([(a, b) for a, b in S["stations"][c]["spills"] if b - a >= 60]) for c in st}
    ok("R3a.high spiller on the clean truth is Marram End", max(sp, key=sp.get) == "SPS0419", sp)
    ok("R3a.dry-day screen files Hagworth Wold", L["R0"] == "SPS0415", L["R0"])
    ok("R3a.high spiller files Marram End", L["R2"] == "SPS0419" and L["R2_hours"] == "SPS0419", (L["R2"], L["R2_hours"]))
    # ------------------------------------------------------------ R3b the decisive step alone
    ok("R3b.delivered rate on the clean truth files Gallowfen", [c for c in st if truth[c] < W.BY_CODE[c]["pff"]] == [K])
    ok("R3b.delivered rate on the cut pack files Gallowfen", RT.top({c: g["pff"][c] - g["delivered"][c] for c in st})[0] == K)
    # ------------------------------------------------------------ R3c no plant
    con = sqlite3.connect(os.path.join(tgt, F["telemetry"]))
    lv = defaultdict(list)
    for rtu, lvl in con.execute("SELECT rtu, level_m FROM wet_well_level"):
        lv[rtu].append(lvl)
    con.close()
    rep = 0
    for rtu, xs in lv.items():
        a = np.array(xs)
        for w in (96, 672):
            blocks = Counter(tuple(a[i:i + w]) for i in range(0, len(a) - w, w))
            rep = max(rep, max(blocks.values()))
    ok("R3c.no repeated level block", rep <= 1, rep)
    ok("R3c.no planted record at Gallowfen", K not in W.EDM_REPLACED and W.BY_CODE[K]["meter"] is None)

    # ------------------------------------------------------------ the ladder's reflex routes do not name Gallowfen
    for k, vals in L["reflex"].items():
        xs = {c: x for c, x in vals.items() if x == x}
        hi, lo = max(xs.values()), min(xs.values())
        ok("reflex.top %s not Gallowfen alone" % k, not (xs[K] == hi and list(xs.values()).count(hi) == 1), (k, xs[K], hi))
        ok("reflex.bottom %s not Gallowfen alone" % k, not (xs[K] == lo and list(xs.values()).count(lo) == 1), (k, xs[K], lo))
    # the shipped statistics a solver might sort: Gallowfen is at neither end of any of them
    head = {c: min(st[c]["rated"].values()) / g["pff"][c] for c in st}
    for name, stat in (("rated duty over permitted flow", head), ("permitted flow", g["pff"]),
                       ("rated duty", {c: min(st[c]["rated"].values()) for c in st}),
                       ("wet well area", {c: st[c]["area"] for c in st}),
                       ("control band", {c: st[c]["start"] - st[c]["stop"] for c in st})):
        order = sorted(stat, key=stat.get)
        ok("shock.%s puts Gallowfen at neither end" % name, K not in (order[0], order[-1]), (name, order.index(K)))
    ranks = sorted(st, key=lambda c: -L["spills"][c])
    ok("ladder.Gallowfen mid-pack on spills", 3 <= ranks.index(K) <= 11, ranks.index(K))
    ok("ladder.Gallowfen no dry-day spills", L["dry_day"][K] == 0)
    ok("ladder.dry-day spills at Hagworth Wold alone", [c for c in st if L["dry_day"][c] > 0] == ["SPS0415"], L["dry_day"])

    # ------------------------------------------------------------ the estimator family (SF14, SF15, SF17)
    fam = {}
    for est in ("median", "mean", "trim"):
        for mode in ("prev", "mean"):
            for night in (False, True):
                for logged in (False, True):
                    fam[(est, mode, night, logged)] = G.delivered(st, g["events"], est, mode, night, False, logged)
    ok("SF15.estimator family converges", all(len({round(v[c]) for v in fam.values()}) == 1 for c in st),
       {c: sorted({round(v[c], 2) for v in fam.values()}) for c in st})
    ok("SF14.volume from logged levels", all(round(fam[("median", "prev", False, True)][c]) == round(g["delivered"][c]) for c in st))
    edge_l = min(0.5 - abs(v[c] - round(v[c])) for v in fam.values() for c in st)
    ok("bins.delivered inside its bin across the family", edge_l >= 0.15, edge_l)
    pp = G.delivered(st, g["events"], per_pump=True)
    ok("SF17.per pump same whole figure", all(round(pp[c][1]) == round(pp[c][2]) == round(g["delivered"][c]) for c in st),
       {c: pp[c] for c in st})
    ok("SF5.both Gallowfen pumps under permit", max(pp[K].values()) < g["pff"][K], pp[K])
    mf = L["R1_meter_flow"]
    ok("SF16.meters agree with cycles", all(round(mf[c]) == round(g["delivered"][c]) for c in mf),
       (mf, {c: g["delivered"][c] for c in mf}))
    ok("backtest.meters validate rated duty", all(abs(mf[c] / st[c]["rated"][1] - 1) < 0.035 for c in mf),
       {c: mf[c] / st[c]["rated"][1] for c in mf})
    # rung 0b, the drawdown without the inflow: it files Hagworth Wold, whose groundwater runs into the well through
    # every cycle, below Gallowfen by a stated margin on each way a solver takes it, and flags only a few overflows
    G0 = "SPS0415"
    for name in ("naive", "naive_night", "naive_p90"):
        r = {c: L[name][c] / g["pff"][c] for c in st}
        order = sorted(st, key=r.get)
        ok("rung0b.%s files Hagworth Wold, Gallowfen next" % name, order[:2] == [G0, K], [(c, round(r[c], 3)) for c in order[:4]])
        ok("rung0b.%s Hagworth Wold below Gallowfen by 0.08 of a permit" % name, r[K] - r[G0] >= 0.08, (r[G0], r[K]))
    flagged = L["naive_flagged"]
    ok("rung0b.flags only a few overflows", G0 in flagged and K in flagged and 2 <= len(flagged) <= 4, flagged)
    ok("rung0b.the rest clear their permits on it", all(L["naive"][c] >= 1.02 * g["pff"][c] for c in st if c not in flagged))
    nd = L["naive"]
    ok("rung0b.recorded: the meters read above it at every metered station", all(mf[c] > 1.05 * nd[c] for c in mf),
       {c: (round(nd[c], 1), mf[c]) for c in mf})
    # the meter historian's quality codes sit clear of every spill and leave the meters' spill flows as they were
    mrows = G.read_csv(os.path.join(tgt, F["meters"]))
    codes = Counter(r["quality"] for r in mrows)
    ok("realism.meter quality codes as a historian writes them", set(codes) >= {"G", "M", "C", "E", "S"}
       and codes["G"] > 0.98 * len(mrows), codes)
    tag_rtu = {st[c]["meter"]: st[c]["rtu"] for c in mf}
    bad = 0
    for r in mrows:
        if r["quality"] != "G":
            t = (dt.datetime.strptime(r["interval_start_utc"], "%Y-%m-%dT%H:%M:%SZ") - G.T0).total_seconds()
            bad += any(a - 3600 < t + 900 and t < b + 3600 for a, b in g["alarms"][tag_rtu[r["meter_tag"]]])
    ok("realism.no flagged meter interval near a spill", bad == 0, bad)
    ok("realism.blank meter values only where flagged M", all((r["flow_ls_mean"] == "") == (r["quality"] == "M") for r in mrows))
    rated_hits = sum(1 for c in st if not st[c].get("meter") and round(min(st[c]["rated"].values())) == round(g["delivered"][c]))
    ok("asks.rated duty rarely rounds to the delivered rate", rated_hits <= 2, rated_hits)

    # ------------------------------------------------------------ the main ask's terms (SF1 to SF10)
    alarms = g["alarms"]
    ok("SF1.Gallowfen spilled in every source", len(alarms[st[K]["rtu"]]) > 0 and len(g["log"][st[K]["edm"]]) > 0)
    ok("SF2.pumped station passes forward to the rising main", "rising main" in g["cons"][K]["text"])
    ok("SF3.no station within one l/s of its permit", all(abs(g["delivered"][c] - g["pff"][c]) > 1.0 for c in st))
    ks = [x[2] for x in G.cycle_rates(g["events"][st[K]["rtu"]], st[K]["area"] * (st[K]["start"] - st[K]["stop"]) * 1000.0)]
    ok("SF4.Gallowfen rate steady through the year", np.percentile(ks, 95) < g["pff"][K], np.percentile(ks, [5, 50, 95]))
    in_spill = [x[2] for x in G.cycle_rates(g["events"][st[K]["rtu"]], st[K]["area"] * (st[K]["start"] - st[K]["stop"]) * 1000.0)
                if any(a - 6 * 3600 <= x[0] <= b + 6 * 3600 for a, b in alarms[st[K]["rtu"]])]
    ok("SF4.Gallowfen rate around its spills", len(in_spill) > 20 and np.median(in_spill) < g["pff"][K], len(in_spill))
    ok("SF6.exactly one overflow breached", len(g["breach"]) == 1)
    yr = [a for recs in g["log"].values() for (a, b) in recs]
    ok("SF7.every discharge inside 2026", min(yr) > 0 and max(b for recs in g["log"].values() for (a, b) in recs) < G.YEAR_S)
    a_txt, b_txt, pages = pdf_text(os.path.join(tgt, F["procedure"]))
    flat = " ".join(a_txt.split())
    ok("SF8.procedure names one overflow per self-report", "A self-report names one storm overflow and its permit" in flat)
    ok("SF9.whole litres per second separate every station", all(round(g["delivered"][c]) != round(g["pff"][c]) for c in st))
    cons_rows = G.read_csv(os.path.join(tgt, F["consents"]))
    ok("SF10.one pass forward value per permit", all(str(int(float(r["pass_forward_ls"]))) in r["condition_text"] for r in cons_rows)
       and len({r["permit_ref"] for r in cons_rows}) == len(cons_rows))

    # ------------------------------------------------------------ the asks' terms (SF11 to SF13, SF18 to SF22)
    pooled = {c: [x for s, cc in g["serial_site"].items() if cc == c for x in g["log"].get(s, [])] for c in st}
    per_serial = {c: sum(G.count_1224(g["log"].get(s, [])) for s, cc in g["serial_site"].items() if cc == c) for c in st}
    ok("SF11.12/24 on the pooled discharges", all(G.count_1224(pooled[c]) == g["lines"][c]["spills"] for c in st))
    ok("SF11.per-serial counts summed differ", sum(1 for c in W.EDM_REPLACED if per_serial[c] != g["lines"][c]["spills"]) >= 9,
       {c: (per_serial[c], g["lines"][c]["spills"]) for c in W.EDM_REPLACED})
    # SF22 a 24-hour block contains discharge when any part of a discharge falls within it
    ok("SF22.procedure defines block membership", "A block contains discharge when any part of a discharge falls within it" in flat)
    starts = {c: count_starts(pooled[c]) for c in st}
    moved = sorted(c for c in st if starts[c] != g["lines"][c]["spills"])
    ok("SF22.starts-only reading moves Marram End and Hagworth Wold only, each down",
       moved == ["SPS0415", "SPS0419"] and all(starts[c] < g["lines"][c]["spills"] for c in moved),
       {c: (starts[c], g["lines"][c]["spills"]) for c in moved})
    ok("SF22.the call does not read the count", K not in moved)
    summed = {c: sum(b - a for a, b in pooled[c]) / 3600.0 for c in st}
    ok("SF12.overlap counted once moves every replaced overflow", all(summed[c] - g["lines"][c]["hours"] >= 1.5 for c in W.EDM_REPLACED),
       {c: round(summed[c] - g["lines"][c]["hours"], 2) for c in W.EDM_REPLACED})
    ok("SF12.procedure counts a period once", "any period of discharge counted once" in flat)
    for c in W.EDM_REPLACED:
        old, new = W.EDM_REPLACED[c][0], st[c]["edm"]
        oi, ni = g["log"].get(old, []), g["log"].get(new, [])
        pn = ni + [x for x in oi if not overl(x, ni)]
        po = oi + [x for x in ni if not overl(x, oi)]
        ok("SF12.12/24 count same however the handover is kept %s" % c,
           G.count_1224(pn) == G.count_1224(po) == g["lines"][c]["spills"])
    # SF13 operational time: the most hours any of the overflow's monitors reported each day
    status = g["status"]

    def daylen(d):
        return 23.0 if d == dt.date(2026, 3, 29) else 25.0 if d == dt.date(2026, 10, 25) else 24.0

    mean_moves = {}
    for c in st:
        days = defaultdict(list)
        for s, cc in g["serial_site"].items():
            if cc == c:
                for d, h in status.get(s, {}).items():
                    days[d].append(h)
        cap = sum(min(sum(v), daylen(d)) for d, v in days.items()) / 87.6
        c24 = sum(min(max(v), 24.0) for v in days.values()) / 87.6
        op = g["lines"][c]["operational"]
        ok("SF13.capped sum agrees %s" % c, abs(cap - op) < 1e-9, (cap, op))
        ok("SF13.a 24-hour cap rounds the same %s" % c, "%.1f" % c24 == "%.1f" % op, (c24, op))
        ok("SF13.no day with two partial monitors %s" % c,
           not [d for d, v in days.items() if len(v) > 1 and max(v) < daylen(d) - 0.05])
        ok("SF13.at most 100 %s" % c, op <= 100.0 + 1e-9, op)
        mean = sum(sum(v) / len(v) for v in days.values()) / 87.6
        mean_moves[c] = "%.1f" % mean != "%.1f" % op
    ok("SF13.a mean across monitors moves only replaced overflows", not [c for c in st if mean_moves[c] and c not in W.EDM_REPLACED],
       mean_moves)
    # SF18 to SF20 the monitor mapping
    ok("SF18.mapping recovers every retired serial", all(g["serial_site"][old] == code for code, (old, a, b) in W.EDM_REPLACED.items()))
    ratios = [v["scores"][1][0] / v["scores"][0][0] for v in g["evidence"].values()]
    ok("SF18.mapping separated", max(ratios) < 0.6, ratios)
    # the second route: the old unit's discharges against the batch's new units' discharges, matched as closely as
    # the alarms are (the storms cross zones, so a bare overlap count does not separate them)
    for code, (old, inst, rem) in W.EDM_REPLACED.items():
        batch = [c for c, (o, i2, r2) in W.EDM_REPLACED.items() if r2 == rem]
        scores = {c: G.coincide(g["log"].get(old, []), g["log"].get(st[c]["edm"], [])) for c in batch}
        rank = sorted(scores, key=lambda c: -scores[c])
        ok("SF18.handover-week coincidence agrees %s" % old,
           rank[0] == code, scores)
    for code, (old, inst, rem) in W.EDM_REPLACED.items():
        batch = [c for c, (o, i2, r2) in W.EDM_REPLACED.items() if r2 == rem]
        ok("SF19.retirement follows exactly one batch %s" % old, all(0 <= (rem - i2).days <= 9 for c, (o, i2, r2) in W.EDM_REPLACED.items() if r2 == rem)
           and not [c for c, (o, i2, r2) in W.EDM_REPLACED.items() if r2 != rem and 0 <= (rem - i2).days <= 9])
        ok("SF19.batch in distinct radar zones %s" % old, len({W.BY_CODE[c]["zone"] for c in batch}) == len(batch))
        ok("SF19.step 5's span: installed six to eight days before the retirement %s" % old,
           all(6 <= (rem - i2).days <= 8 for c, (o, i2, r2) in W.EDM_REPLACED.items() if r2 == rem))
    cur_only = {}
    for c in st:
        iv = g["log"].get(st[c]["edm"], [])
        cur_only[c] = (G.count_1224(iv), "%.1f" % hours(iv), "%.1f" % (sum(status.get(st[c]["edm"], {}).values()) / 87.6))
    for c in W.EDM_REPLACED:
        L1 = g["lines"][c]
        ok("SF20.register serial alone misses spills, hours and operational time %s" % c,
           cur_only[c][0] != L1["spills"] and cur_only[c][1] != "%.1f" % L1["hours"] and cur_only[c][2] != "%.1f" % L1["operational"],
           (cur_only[c], L1["spills"], L1["hours"], L1["operational"]))
    for c in st:
        if c not in W.EDM_REPLACED:
            L1 = g["lines"][c]
            ok("SF20.register serial whole where nothing was replaced %s" % c,
               cur_only[c] == (L1["spills"], "%.1f" % L1["hours"], "%.1f" % L1["operational"]))
    # SF21 the discharge log's clock: the data force UK local time, and reading it as UTC moves no graded figure
    naive = defaultdict(list)
    for r in G.read_csv(os.path.join(tgt, F["edm_log"])):
        naive[r["monitor_serial"]].append(((dt.datetime.strptime(r["discharge_start"], "%d/%m/%Y %H:%M:%S") - G.T0).total_seconds(),
                                           (dt.datetime.strptime(r["discharge_end"], "%d/%m/%Y %H:%M:%S") - G.T0).total_seconds()))
    off = {"winter": [], "summer": []}
    share = {"local": {"winter": [0, 0], "summer": [0, 0]}, "utc": {"winter": [0, 0], "summer": [0, 0]}}
    for ser, recs in naive.items():
        al = np.array(sorted(x for x, y in alarms[st[g["serial_site"][ser]]["rtu"]]))
        for (a, b), (ca, cb) in zip(sorted(recs), sorted(g["log"][ser])):
            season = "summer" if G.BST0 <= ca < G.BST1 else "winter"
            near = al[(al > a - 2 * 3600) & (al <= a + 600)]
            if len(near):
                off[season].append(a - near[np.argmin(np.abs(a - near - (3600 if season == "summer" else 0)))])
            for how, t in (("local", ca), ("utc", a)):
                j = np.searchsorted(al, t)
                share[how][season][0] += int(j > 0 and 0 <= t - al[j - 1] <= 300)
                share[how][season][1] += 1
    w, sm = float(np.median(off["winter"])), float(np.median(off["summer"]))
    ok("SF21.winter offset to the UTC alarms about a minute", 0 <= w <= 300, w)
    ok("SF21.summer offset to the UTC alarms about an hour", 3600 <= sm <= 3900, sm)
    fr = {h: {k: v[0] / v[1] for k, v in d.items()} for h, d in share.items()}
    ok("SF21.summer discharges meet the alarms only on local time", fr["local"]["summer"] >= 0.8 and fr["utc"]["summer"] <= 0.05
       and fr["local"]["winter"] >= 0.9 and fr["utc"]["winter"] >= 0.9, fr)
    ss_n, _ = G.map_monitors(st, naive, g["mlist"], alarms, restrict=True)
    ok("SF21.read as UTC every retired serial still lands on its overflow", all(ss_n[o] == c for c, (o, i, r) in W.EDM_REPLACED.items()))
    for c in st:
        nv = [x for s_, cc in g["serial_site"].items() if cc == c for x in naive.get(s_, [])]
        gold_m = ["%.1f" % x for x in g["lines"][c]["months"]]
        ok("SF21.read as UTC the count, hours and every month cell are unchanged %s" % c,
           G.count_1224(nv) == g["lines"][c]["spills"] and "%.1f" % hours(nv) == "%.1f" % g["lines"][c]["hours"]
           and ["%.1f" % x for x in months_local(nv)] == gold_m and ["%.1f" % x for x in months_utc(nv)] == gold_m)
        ok("SF21.UTC months on the converted log agree %s" % c, ["%.1f" % x for x in months_utc(pooled[c])] == gold_m)
    ok("asks.Gallowfen monitor never replaced", K not in W.EDM_REPLACED)
    ok("asks.monthly hours sum to the year", all(abs(sum(g["lines"][c]["months"]) - g["lines"][c]["hours"]) < 1e-6 for c in st))
    ok("asks.no discharge in the repeated October hour", not any(
        G.BST1 - 3600 <= a < G.BST1 + 3600 for recs in g["log"].values() for (a, b) in recs))
    ok("asks.no discharge spans a clock change", not any(a < G.BST0 < b or a < G.BST1 < b for recs in g["log"].values() for (a, b) in recs))
    # every graded ask figure clear of its rounding edge
    # hours: every graded hours figure, the year's in the return and each month's on the chart, a minute or more from
    # its rounding line, so a reader working to the minute rounds it the same way
    sec = lambda h: edge(h) * 360.0
    ok("bins.return hours a minute clear of the line", min(sec(g["lines"][c]["hours"]) for c in st) >= 60,
       {c: round(sec(g["lines"][c]["hours"]), 1) for c in st})
    near = [(c, k + 1, round(h, 4)) for c in st for k, h in enumerate(g["lines"][c]["months"]) if h > 0 and sec(h) < 60]
    ok("bins.every chart month a minute clear of the line", not near, near)
    ok("bins.settling moved a few discharge ends only", 0 < info["ends_settled"] <= 80, info["ends_settled"])
    # operational time: a reader who caps 25 October at 24 hours lowers a figure by 0.0114, so none sits that close
    # above an edge
    above = {c: ((g["lines"][c]["operational"] * 10) % 1 - 0.5) % 1 for c in st}
    ok("bins.operational clear above the edge", min(above.values()) >= 0.13, {c: round(v, 3) for c, v in above.items()})
    # independent detection: no EDM discharge shares both bounds with an overflow alarm
    shared = 0
    for c in st:
        al = set((round(a), round(b)) for a, b in alarms[st[c]["rtu"]])
        shared += sum(1 for a, b in pooled[c] if (round(a), round(b)) in al)
    ok("realism.monitors and alarms detect independently", shared == 0, shared)
    two = [c for c in W.EDM_REPLACED if len(g["log"].get(W.EDM_REPLACED[c][0], [])) and len(g["log"].get(st[c]["edm"], []))]
    same = sum(1 for c in two for x in g["log"][W.EDM_REPLACED[c][0]] if x in set(g["log"][st[c]["edm"]]))
    ok("realism.two units never write the same record", same == 0, same)

    # ------------------------------------------------------------ realism sweep
    names = [s["name"] for s in W.STATIONS]
    shapes = Counter(len(n.split()) for n in names)
    ok("realism.station names vary in shape", len(shapes) >= 2, shapes)
    codes = sorted(int(s["code"][3:]) for s in W.STATIONS)
    ok("realism.station codes not an arithmetic sequence", len(set(np.diff(codes))) > 2, np.diff(codes))
    ok("realism.spill counts vary", len(set(g["lines"][c]["spills"] for c in st)) >= 8)
    ok("realism.alarm table carries the outstation's other alarms", len(alarm_types) >= 4
       and alarm_types["OVERFLOW OPERATING"] < 0.6 * sum(alarm_types.values()), alarm_types)
    wo_rows = G.read_csv(os.path.join(tgt, F["workorders"]))
    wo_txt = " ".join(" ".join(r.values()) for r in wo_rows).lower()
    notes = Counter(r["technician_notes"] for r in wo_rows)
    ok("realism.technician notes vary", notes.most_common(1)[0][1] <= 0.08 * len(wo_rows) and len(notes) >= 0.4 * len(wo_rows),
       notes.most_common(3))
    ok("realism.closure codes from the system's list", {r["closure_code"] for r in wo_rows} <= {"COMPLETE", "NFF", "ATTENDED", "SECURED"})
    restate = [r["technician_notes"] for r in wo_rows
               if (r["technician_notes"].endswith("Back in auto.") and "auto" in r["technician_notes"][:-len("Back in auto.")])
               or (r["technician_notes"].endswith("All ok.") and re.search(r"\bok\b|fine", r["technician_notes"][:-len("All ok.")]))]
    ok("realism.no closing remark restates its note", not restate, restate[:3])
    ok("realism.work orders name no fault at Gallowfen", not re.search(r"block|restrict|rising main|ragg|impeller|drawdown|"
                                                                        r"under ?perform|low flow|duty point", wo_txt))
    ok("dates.work orders inside 2026", all("2026-01-01" <= r["completed"] <= "2026-12-31" for r in wo_rows))
    seq = [(r["completed"], int(r["work_order"][2:])) for r in wo_rows]
    ok("realism.work order numbers run with time", all(seq[i][1] < seq[i + 1][1] for i in range(len(seq) - 1)
                                                        if seq[i][0] < seq[i + 1][0]))
    con = sqlite3.connect(os.path.join(tgt, F["telemetry"]))
    al_hl = defaultdict(list)
    for rtu, a in con.execute("SELECT rtu, raised_utc FROM alarm WHERE alarm='HIGH LEVEL'"):
        al_hl[rtu].append(G.utc_sec(a))
    intr = defaultdict(list)
    for rtu, a in con.execute("SELECT rtu, raised_utc FROM alarm WHERE alarm='INTRUDER'"):
        intr[rtu].append(G.utc_to_local(G.utc_sec(a)).date().isoformat())
    con.close()
    for r in wo_rows:
        rtu = st[r["station_code"]]["rtu"]
        if r["task"] == "High level alarm attended":
            d = dt.date.fromisoformat(r["completed"])
            ok("realism.call-out follows a high level alarm %s" % r["work_order"], any(
                G.utc_to_local(a).date() in (d, d - dt.timedelta(days=1)) for a in al_hl[rtu]))
        ok("realism.every work order opened the kiosk %s" % r["work_order"],
           r["completed"] in intr[rtu] or any(dt.date.fromisoformat(x) == dt.date.fromisoformat(r["completed"]) - dt.timedelta(days=1)
                                              for x in intr[rtu]))
    reg = {r["serial"]: r for r in G.read_csv(os.path.join(tgt, F["edm_list"]))}
    for c in st:
        inst = st[c]["edm_installed"]
        inst = inst.date() if hasattr(inst, "date") else inst
        ok("realism.register and platform agree on the install date %s" % c,
           reg[st[c]["edm"]]["commissioned"] == inst.strftime("%d/%m/%Y"), (reg[st[c]["edm"]]["commissioned"], inst))
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(tgt, F["assets"]), data_only=True)
    done = defaultdict(set)
    for r in wo_rows:
        done[(r["station_code"], r["task"])].add(r["completed"])
    for row in list(wb["Pumps"].iter_rows(values_only=True))[1:]:
        ok("realism.last pump service is a work order %s %s" % (row[0], row[1]),
           row[7].date().isoformat() == max(done[(row[0], "Pump service (6-monthly)")]), (row, done[(row[0], "Pump service (6-monthly)")]))
    for row in list(wb["Flow meters"].iter_rows(values_only=True))[1:]:
        ok("realism.meter verification is a work order %s" % row[0],
           row[4].date().isoformat() in done[(row[0], "Flow meter verification")])

    # ------------------------------------------------------------ the governing document
    ok("doc.procedure read by pypdf strict and pdftotext", len(a_txt) > 2000 and len(b_txt) > 2000, (len(a_txt), len(b_txt)))
    ok("doc.positive control 12/24", "12/24 method" in flat and "12/24 method" in " ".join(b_txt.split()))
    ok("doc.page count matches footer", ("of %d" % pages) in b_txt and ("Page %d of %d" % (pages, pages)) in b_txt, pages)
    for w in ("drawdown", "draw down", "delivered", "rated duty", "duty point", "blockage", "fill and draw",
              "cycle", "wet well", "flow meter", "volume", "retired", "replace", "serial", "alarm"):
        ok("doc.procedure silent on %s" % w, w not in a_txt.lower() and w not in b_txt.lower())
    ok("doc.no em dash", "\u2014" not in a_txt and "\u2013" not in a_txt)

    # ------------------------------------------------------------ input gates and hygiene
    files = [os.path.join(r, f) for r, _, fs in os.walk(tgt) for f in fs]
    ok("gate.ten files or more", len(files) >= 10, len(files))
    fmts = {os.path.splitext(f)[1] for f in files}
    ok("gate.three formats or more", len(fmts) >= 3, fmts)
    ok("gate.a file of 25,000 rows", info["rain_rows"] >= 25000 and info["telemetry_events"] >= 25000)
    meta = json.load(open(os.path.join(task, "metadata.json")))
    ok("gate.two distractors", len(meta["distractor_files"]) >= 2)
    used = {F[k] for k in ("telemetry", "edm_log", "edm_status", "edm_list", "assets", "consents", "procedure")}
    for d in meta["distractor_files"]:
        ok("gate.distractor unused by the golden %s" % d, d.replace("target/", "") not in used)
    for f in files:
        base = os.path.basename(f).lower()
        ok("hygiene.no describing file %s" % base, not re.search(r"readme|dictionar|manifest|field.?notes|codebook|schema", base))
    ok("hygiene.no em dash in csv", not any("\u2014" in open(f, encoding="utf-8", errors="ignore").read()
                                            for f in files if f.endswith(".csv")))
    sub = open(os.path.join(task, "submission.md"), encoding="utf-8").read()
    ok("hygiene.no em dash in submission", "\u2014" not in sub and "\u2013" not in sub)
    ok("figures.call agrees", figs["call"] == g["call"] and figs["call_delivered_ls"] == round(g["delivered"][K]))
    return len(PASSED)
