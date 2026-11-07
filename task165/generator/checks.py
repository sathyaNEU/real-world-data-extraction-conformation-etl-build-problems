"""task165 architecture 2: the generator's checks on the built pack (python3 task165/generator/checks.py [target]).

The world's truth against the golden, the ladder (R0, R1, R1b, the decisive R2), every semantic fork of the design
note's table (SF1 to SF11) converging on the golden's call, the three-rules block on the clean truth, the asks'
devices and margins, the separation of the main population from the ask devices, and the input gates."""
import csv
import datetime as dt
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
sys.path.insert(0, HERE)
import golden as G   # noqa: E402
import params as P   # noqa: E402
import world as W    # noqa: E402

FAILS = []
N = [0]


def check(name, ok, detail=""):
    N[0] += 1
    print("%s %-66s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        FAILS.append(name)


def pick_of(ev):
    return next((lab for lab, _, _ in G.ALTS if ev[lab] <= 4.0), None)


def counts(o, room, during=False, gap=96):
    return {lab: G.events(G.replay(o, v, p, room, during), gap) / G.YEARS for lab, v, p in G.ALTS}


def mid_twelfth(x):
    """A count over twelve years printed to one decimal sits off the half."""
    return abs((x * 10) % 1 - 0.5) > 0.05


def main():
    w = W.simulate()
    o = G.read_meter(T)
    ss = G.read_plant(T)
    room = np.repeat(G.CAP - ss, 4)
    gold = counts(o, room)
    pick = pick_of(gold)
    lad = G.ladder(T)

    # ------------------------------------------------------------------ the call
    check("C1 the golden picks Alternative C", pick == "C", str({k: round(v, 2) for k, v in gold.items()}))
    truth = counts(w["o14"], W.ss_room_15(w["ss"]))
    check("C2 the world's own replay (clean flows, clean plant) picks the same", pick_of(truth) == "C",
          str({k: round(v, 2) for k, v in truth.items()}))
    check("C3 the meter read back is the world's overflow within its reading error",
          float(np.abs(o - w["o14"]).max()) < 0.03 * max(1.0, float(w["o14"].max())) and
          ((o > 0) == (w["o14"] > 0)).mean() > 0.9999, "max abs %.3f" % float(np.abs(o - w["o14"]).max()))
    dif = np.abs(ss - w["ss"])
    check("C4 the plant read back is the world's within its throttling noise (the historian's BAD hours aside)",
          float(np.percentile(dif, 99.98)) < 0.8 and float(dif.mean()) < 0.02,
          "p99.98 %.3f, mean %.4f" % (float(np.percentile(dif, 99.98)), float(dif.mean())))
    check("C5 every graded per-alternative figure sits off a twelfth's half", all(mid_twelfth(v) for v in gold.values()),
          str({k: round(v * 12) for k, v in gold.items()}))
    check("C6 B over the limit and C under it by at least 0.8 events", gold["B"] >= 4.8 and gold["C"] <= 3.2,
          "B %.2f C %.2f" % (gold["B"], gold["C"]))

    # ------------------------------------------------------------------ the ladder
    check("LADDER R0 (event volumes, empty tank) picks B", pick_of(lad["r0"]) == "B", str(lad["r0"]))
    check("LADDER R1 (replay at the rating) picks B with B a full event under 4",
          pick_of(lad["r1"]) == "B" and lad["r1"]["B"] <= 3.0, str(lad["r1"]))
    check("LADDER R1b (pumping during the overflow at the rating, against TM-7 3.2) picks a smaller tank",
          pick_of(lad["r1b"]) in ("A", "B"), str(lad["r1b"]))
    check("LADDER the room moves B by at least 3 events a year", gold["B"] - lad["r1"]["B"] >= 3.0,
          "%.2f" % (gold["B"] - lad["r1"]["B"]))
    check("LADDER every cheap route lands wrong (Gate F: no cheap route reaches C)",
          all(pick_of(x) != "C" for x in (lad["r0"], lad["r1"], lad["r1b"])))
    # the Northside back-test confirms the rating replay (and the room replay) at Northside
    nt = W.northside_tank()
    det = G.events(nt["over"])
    rep = G.events(_replay_hold(nt["inflow"], P.NT_VOL, P.NT_CURVE[3]))
    check("BACKTEST the rating replay (O&M 4.3's hold) reproduces Outfall 006's detector events within 3",
          abs(det - rep) <= 3,
          "detector %d, replay %d (the August 2023 cleanout bypass included)" % (det, rep))
    nsroom = np.repeat(P.NS_CAP - w["ns"], 4)[nt["i0"]:]
    pumping = nt["deliv"] > 0
    check("BACKTEST the Northside plant's room never binds the station while it pumps",
          float(nsroom[pumping].min()) > P.NT_CURVE[3], "min room %.1f MGD" % float(nsroom[pumping].min()))

    # ------------------------------------------------------------------ the semantic forks
    def sf(name, ev, detail=""):
        check("%s same call" % name, pick_of(ev) == "C", detail or str({k: round(v, 2) for k, v in ev.items()}))
    sf("SF1 event separation (12 h, 48 h)", {k: max(a, b) for (k, a), b in
                                            zip(counts(o, room, gap=48).items(), counts(o, room, gap=192).values())})
    sf("SF1 event separation 12 h", counts(o, room, gap=48))
    sf("SF1 event separation 48 h", counts(o, room, gap=192))
    # SF2: the mean of the twelve yearly counts equals the record's count over twelve (full years)
    check("SF2 average year identical as a mean of yearly counts", True, "twelve full calendar years")
    # SF3: the record on UTC year ends (five hours later at each end)
    sh = 20
    o_utc = np.concatenate([o[sh:], np.zeros(sh)])
    sf("SF3 the record on UTC year ends", counts(o_utc, np.concatenate([room[sh:], np.full(sh, G.CAP)])))
    check("SF4 under four, not at four: no alternative sits on 4.0", all(abs(v - 4.0) > 0.3 for v in gold.values()))
    sf("SF5 pumping during the overflow", counts(o, room, during=True))
    # SF6: both loggers in the overlap week summed
    a, b = W.meter_swap()
    check("SF6 the overlap week is dry, so summing both loggers changes nothing", float(o[a - 4:b + 4].max()) == 0.0)
    oh = o.reshape(-1, 4).mean(axis=1)
    ev_h = {}
    for lab, v, p in G.ALTS:
        out = np.zeros(len(oh))
        s = 0.0
        for i in range(len(oh)):
            q = oh[i] / 24
            if q > 0:
                t = min(v - s, q)
                s += t
                out[i] = (q - t) * 24
            elif s > 0:
                s -= min(s, min(p, max(0.0, G.CAP - ss[i])) / 24)
        ev_h[lab] = G.events(out, 24) / G.YEARS
    sf("SF7 hourly grain", ev_h)
    check("SF7 hourly grain gives the same figures to one decimal",
          all(round(ev_h[k], 1) == round(gold[k], 1) for k in gold), str(ev_h))
    sf("SF8 the plant limit at 139 MGD", counts(o, np.repeat(139.0 - ss, 4)))
    sf("SF8 the plant limit at the historian's maximum", counts(o, np.repeat(float(ss.max()) - ss, 4)))
    # SF9: the tank full on 1 January 2014
    full = {lab: G.events(_replay_full(o, v, p, room)) / G.YEARS for lab, v, p in G.ALTS}
    sf("SF9 the tank full at the record's start", full)
    for s_ in (-5, -4, -1, 1, 4, 5):
        sf("SF10 the plant clock misread by %+d h" % s_, counts(o, np.repeat(G.CAP - np.roll(ss, s_), 4)))
    sf("SF10 the plant's BAD hours read as zero", counts(o, np.repeat(G.CAP - G.read_plant(T, bad="zero"), 4)))
    dmean = np.repeat(ss.reshape(-1, 24).mean(axis=1), 24)
    sf("SF10 the plant's room at daily grain", counts(o, np.repeat(G.CAP - dmean, 4)))
    costs = [c for _, _, _, c in P.ALTERNATIVES]
    check("SF11 costs rise with size, so the least-cost alternative that meets is the smallest",
          costs == sorted(costs) and pick == "C" and gold["D"] <= 4.0)

    # ------------------------------------------------------------------ the three rules (dataset-generation 7.1)
    easy = {lab: W.per_year(W.replay(w["o14"], v, p)) for lab, v, p, _ in P.ALTERNATIVES}
    check("RULES analyst test on the clean truth: the rating replay picks B", pick_of(easy) == "B",
          str({k: round(v, 2) for k, v in easy.items()}))
    check("RULES no column of any shipped file holds a tank level at Clay Street or a plant room",
          _no_room_column(T))

    # ------------------------------------------------------------------ the asks
    a1 = G.ask1(T)
    rg = W.rain_gauges()
    ok = True
    for g, d in rg["tips"].items():
        tru = np.zeros(12)
        for s_, b_, k_ in zip(d["sec"], d["bucket"], d["kind"]):
            loc = (P.START_UTC + dt.timedelta(seconds=int(s_))).astimezone(W.NY)
            if loc.year == 2025 and k_ == "rain":
                tru[loc.month - 1] += b_
        ok &= bool(np.abs(tru - a1[g]).max() < 1e-9)
    check("ASK1 the golden recovers every gauge-month's recorded rain exactly", ok)
    edge = min(abs((a1[g][m] * 100 + 1e-9) % 1 - 0.5) for g in a1 for m in range(12))
    check("ASK1 no cell on a rounding edge at the exact 0.2/25.4 in a tip (0.002 hundredths)", edge > 0.002, "%.3f" % edge)
    for name, kw, least in (("pours kept", dict(pours="keep"), 25), ("clocks unread", dict(handle_clock=False), 6),
                            ("pours by the logged window", dict(pours="window"), 15),
                            ("every tip at 0.01 in", dict(bucket=False), 22), ("re-sent tips kept", dict(dedupe=False), 4)):
        v = G.ask1(T, **kw)
        moved = sum(int(round(v[g][m] + 1e-9, 2) != round(a1[g][m] + 1e-9, 2)) for g in a1 for m in range(12))
        check("ASK1 device moves at least %d cells: %s" % (least, name), moved >= least, "%d cells" % moved)
    a2, floor = G.ask2(T)
    nt_true = {}
    for k in range(len(nt["deliv"])):
        y = W.local_of(nt["i0"] + k).year
        nt_true[y] = nt_true.get(y, 0.0) + nt["deliv"][k]
    check("ASK2 the mass balance is the delivered volume within 0.4 MG a year, same whole MG",
          all(abs(a2[y] - nt_true[y]) < 0.4 and round(a2[y]) == round(nt_true[y]) for y in a2),
          str({y: round(a2[y] - nt_true[y], 3) for y in a2}))
    check("ASK2 every year sits 0.1 MG or more from a rounding edge",
          all(abs(a2[y] % 1 - 0.5) > 0.1 for y in a2), str({y: round(a2[y], 2) for y in a2}))
    check("ASK2 the re-mounted transducer's floor is 0.45 ft", abs(floor - P.NT_TRANSDUCER_OFFSET) < 1e-9)
    raw = G.ask2(T, offset=False)[0]
    check("ASK2 the uncorrected level moves 2023, 2024 and 2025 out of their bins",
          all(round(raw[y]) != round(a2[y]) for y in (2023, 2024, 2025)))
    noin = G.ask2(T, inflow=False)[0]
    check("ASK2 the level falls without FIT-600's inflow miss 2022 to 2025 (SG-600's leak-by)",
          all(round(noin[y]) != round(a2[y]) for y in (2022, 2023, 2024, 2025)),
          str({y: round(noin[y]) for y in noin}))
    both = G.ask2(T, offset=False, inflow=False)[0]
    check("ASK2 neither handling keeps 2023 to 2025", all(round(both[y]) != round(a2[y]) for y in (2023, 2024, 2025)))
    import ceiling as CE
    pr = CE.pump_route(T)
    check("ASK2 run states times the station curve miss every year", all(round(pr[y]) != round(a2[y]) for y in a2),
          str({y: round(pr[y]) for y in pr}))

    # ------------------------------------------------------------------ separation
    check("SEP the main population (OF-014 meter, Southside influent) carries no ask device rows",
          _meter_clean(T), "no duplicate quarter hour outside the dry overlap week")
    # ------------------------------------------------------------------ input gates
    files = sorted(os.listdir(T))
    fmts = {f.rsplit(".", 1)[-1] for f in files}
    check("GATE 10 or more files", len(files) >= 10, str(len(files)))
    check("GATE 3 or more formats", len(fmts) >= 3, str(sorted(fmts)))
    big = max(_rows(os.path.join(T, f)) for f in files)
    check("GATE one file of 25,000 or more rows", big >= 25000, str(big))
    meta = os.path.join(TASK, "metadata.json")
    if os.path.exists(meta):
        md = json.load(open(meta))
        check("GATE two or more distractors named in metadata.json", len(md.get("distractors", [])) >= 2)
    check("GATE every PDF written by an office application", _pdfs_office(T))

    print("%d checks, %d FAIL" % (N[0], len(FAILS)))
    sys.exit(1 if FAILS else 0)


def _replay_hold(inflow, vol, pump, hold=1.0):
    """The rating replay with O&M 4.3's rule: the station held off while FIT-600 reads 1.0 MGD or more."""
    dtd = 15 / 1440.0
    out = np.zeros(len(inflow))
    s = 0.0
    for i in range(len(inflow)):
        q = inflow[i] * dtd
        if inflow[i] >= hold:
            take = min(vol - s, q)
            s += take
            out[i] = (q - take) / dtd
        else:
            s = max(0.0, s + q - pump * dtd)
            if s > vol:
                out[i] = (s - vol) / dtd
                s = vol
    return out


def _replay_full(inflow, vol, pump, room):
    dtd = 15 / 1440.0
    out = np.zeros(len(inflow))
    s = vol
    lim = np.minimum(pump, np.maximum(0.0, room))
    for i in range(len(inflow)):
        q = inflow[i] * dtd
        if q > 0:
            take = min(vol - s, q)
            s += take
            out[i] = (q - take) / dtd
        elif s > 0:
            s -= min(s, lim[i] * dtd)
    return out


def _rows(path):
    if path.endswith(".csv"):
        return sum(1 for _ in open(path, encoding="utf-8")) - 1
    if path.endswith(".parquet"):
        import pyarrow.parquet as pq
        return pq.read_metadata(path).num_rows
    return 0


def _no_room_column(target):
    bad = ("room", "headroom", "spare", "tank_level_014", "clay_tank")
    for f in os.listdir(target):
        if f.endswith(".csv"):
            head = open(os.path.join(target, f), encoding="utf-8").readline().lower()
            if any(b in head for b in bad):
                return False
    return True


def _meter_clean(target):
    import pyarrow.parquet as pq
    t = pq.read_table(os.path.join(target, "outfall_014_flow_monitoring_2014-2025.parquet")).to_pydict()
    seen = {}
    for lg, ts in zip(t["logger_id"], t["reading_time"]):
        if (lg, ts) in seen:
            return False
        seen[(lg, ts)] = 1
    return True


def _pdfs_office(target):
    from pypdf import PdfReader
    for f in os.listdir(target):
        if f.endswith(".pdf"):
            m = PdfReader(os.path.join(target, f)).metadata
            if "LibreOffice" not in str(m.get("/Producer")) or str(m.get("/Creator")) != "Writer":
                return False
            if not m.get("/Subject") or "unspecified" in str(m.get("/Subject")):
                return False
            if b"ReportLab" in open(os.path.join(target, f), "rb").read():
                return False
    return True


if __name__ == "__main__":
    main()
