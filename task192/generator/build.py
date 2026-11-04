"""Build task192: the world, the pack under target/, the goldens from the pack, figures.json, metadata.json and
target.zip. Usage: python3 build.py"""
import collections
import datetime as dt
import json
import math
import os
import shutil
import sys
import time
import zipfile

import numpy as np

import deliver
import docs
import golden as G
import pack as PK
import sim
import truth
import world as W

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
SIM_SEED = 19268
STAMP = time.mktime((2026, 11, 3, 7, 41, 0, 0, 0, -1))
ZIP_TIME = (2026, 11, 3, 7, 41, 0)


def edge(v, u):
    """Distance from a value to the nearest edge of the cell it prints in, at unit u."""
    return u / 2 - abs(v - round(v / u) * u)


def event_days(net, S):
    """Local days on which an interruption or a momentary operation reached each transformer."""
    R = truth.Reach(net)
    days = collections.defaultdict(set)
    for o in S["outages"]:
        d0 = sim.local_day(o["start"])
        d1 = sim.local_day(o["restore"])
        dev = o["device"]
        trs = [net["sps"][dev]["transformer"]] if dev in net["sps"] else R.transformers(dev, d0)
        for tid in trs:
            d = d0
            while d <= d1:
                days[tid].add(d)
                d += dt.timedelta(days=1)
    for op in S["ops"]:
        for tid in R.transformers(op["device"], op["day"]):
            days[tid].add(op["day"])
    return days


def tidy_dates(net, S):
    """No service point is connected or retired on a day an interruption or a momentary operation reached it, so
    no reading of 'served on that day' moves a figure; and none on the period's last day, so no reading of
    'supplies on the last day' (DRP-04 2.1) moves the customers served. A date the forward step would carry onto
    or past the last day goes back instead, to the latest free day before it."""
    days = event_days(net, S)
    one = dt.timedelta(days=1)
    moved = 0

    def free(d, busy):
        return d not in busy and (d - one) not in busy

    for sp, v in sorted(net["sps"].items()):
        busy = days.get(v["transformer"], set())
        for key in ("connected", "disconnected"):
            d0 = v[key]
            if d0 is None or d0 < W.DATA0:
                continue
            d = d0
            while not free(d, busy):
                d += one
                moved += 1
            if d >= W.REP1:
                d = min(d0, W.REP1) - one
                while not free(d, busy):
                    d -= one
                moved += 1
            v[key] = d
        if v["disconnected"] and v["disconnected"] <= v["connected"]:
            v["disconnected"] = v["connected"] + dt.timedelta(days=30)
            assert v["disconnected"] < W.REP1, (sp, v)
    return moved


def calibrate(TR):
    """The 2026 threshold the procedure files: the 2.5 beta value of the daily SAIDI history, which in the years
    before 2025 carried the heavier storm seasons, so it sits well above every ordinary 2026 day."""
    vals = [v for d, v in TR["saidi_day"].items() if d.year == 2025 and v > 0]
    la = np.log(vals)
    t25 = float(np.exp(la.mean() + 2.5 * la.std(ddof=1)))
    designed = set(d for d in sim.MED_STORMS if d.year == 2026)
    rest26 = max(v for d, v in TR["saidi_day"].items() if d.year == 2026 and d not in designed)
    return round(max(t25, 1.8 * rest26), 2)


def clear(v):
    return edge(v["saidi"], 0.1) >= 0.01 and edge(v["maifi"], 0.01) >= 0.001


def nudge(net, S, rng):
    """Service points energised in October where a feeder's printed figures would otherwise sit within a tenth of
    a unit of a rounding edge; repeated until every figure is clear, since a new service is interrupted like any
    other from its connection on."""
    added = collections.Counter()
    used = set(int(x) for x in net["sps"])
    by_f = collections.defaultdict(list)
    for tid, T in sorted(net["transformers"].items()):
        by_f[W.device_feeder(net, T["device"], W.REP1) if T["lateral"] else T["feeder"]].append(tid)
    for rnd in range(40):
        TR = truth.compute(net, S)
        bad = [f for f in W.FID if not clear(TR["idx"][f])]
        if not bad:
            return TR, dict(added)
        days = event_days(net, S)
        for f in bad:
            for _ in range(int(rng.integers(1, 4))):
                tid = by_f[f][int(rng.integers(0, len(by_f[f])))]
                busy = days.get(tid, set())
                con = None
                for _ in range(40):
                    d = dt.date(2026, 10, 5) + dt.timedelta(days=int(rng.integers(0, 20)))
                    if d not in busy and d - dt.timedelta(days=1) not in busy:
                        con = d
                        break
                if con is None:
                    continue
                while True:
                    x = int(rng.integers(10000000, 99999999))
                    if x not in used:
                        used.add(x)
                        break
                net["sps"]["%08d" % x] = dict(id="%08d" % x, transformer=tid, cls="RES", connected=con,
                                              disconnected=None)
                added[f] += 1
    raise SystemExit("figures still on a rounding edge after the nudge: %s" % bad)


world_cache = {}


def world():
    net = W.build(np.random.default_rng(W.SEED))
    wx = sim.weather(np.random.default_rng(W.SEED + 1))
    stk = sim.strokes(np.random.default_rng(W.SEED + 2), wx["cells"])
    S = sim.simulate(np.random.default_rng(SIM_SEED), net, wx, stk)
    tidy_dates(net, S)
    TR = truth.compute(net, S)
    W.T_MED_2026 = calibrate(TR)
    TR, added = nudge(net, S, np.random.default_rng(W.SEED + 9))
    world_cache.update(net=net, wx=wx, stk=stk, S=S, TR=TR)
    return net, wx, stk, S, TR, added


def cut(target, net, wx, stk, S, TR):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    rng = np.random.default_rng(W.SEED + 5)
    info = {}
    info["relay"], info["relay_dropped"] = PK.write_relay(target, net, S, rng)
    info["recloser"] = PK.write_recloser(target, net, S, rng)
    info["soe"] = PK.write_soe(target, net, S, rng)
    info["oms"] = PK.write_oms(target, net, S, TR, rng)
    info["devices"] = PK.write_devices(target, net, rng)
    info["transformers"] = PK.write_transformers(target, net, rng)
    info["sps"] = PK.write_sps(target, net, rng)
    info["feeders"] = PK.write_feeders(target, net, rng)
    info["subs"] = PK.write_subs(target)
    info["strokes"] = PK.write_strokes(target, stk, rng)
    info["asos"] = PK.write_asos(target, wx, rng)
    info["veg"] = PK.write_veg(target, net, rng)
    info["blinks"] = PK.write_blinks(target, net, S, TR, rng)
    docs.build(PK.path(target, "procedure"), W.T_MED_2026, TR["n_sys"])
    for root, dirs, files in os.walk(target):
        for fn in files + dirs:
            os.utime(os.path.join(root, fn), (STAMP, STAMP))
    os.utime(target, (STAMP, STAMP))
    return info


def archive(target, out):
    """The pack's files at the archive root, by their paths under target/: no enclosing folder, no directory entries."""
    names = []
    for root, dirs, files in os.walk(target):
        for f in files:
            p = os.path.join(root, f)
            names.append((os.path.relpath(p, target).replace(os.sep, "/"), p))
    names.sort()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for arc, p in names:
            info = zipfile.ZipInfo(arc, date_time=ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            with open(p, "rb") as fh:
                z.writestr(info, fh.read())
    return len(names)


def metadata(info):
    desc = {
        "relay": "feeder breaker relays' event records retrieved to the relay archive, UTC",
        "recloser": "mid-line recloser controls' event logs, control clock on Central standard time",
        "soe": "SCADA sequence-of-events log for feeder breakers and SCADA-connected reclosers, Central time",
        "oms": "outage management system export: legacy tickets to 31 March 2026, incidents and restoration steps after",
        "feeders": "feeder register with the Cotter Road renumbering of 14 March 2026",
        "devices": "breakers, reclosers and fuses with their in-service history and the protection study's available fault current",
        "transformers": "distribution transformer list from the GIS",
        "sps": "service point extract from the GIS and customer information system, 31 October 2026",
        "strokes": "lightning detection network strokes for the service territory box",
        "asos": "airport weather station hourly observations",
        "subs": "substation locations",
        "veg": "line clearance work orders",
        "blinks": "customer contacts about blinking lights",
        "procedure": "DRP-04 Distribution Reliability Procedure, revision 6 (extract)",
    }
    md = {
        "task": "task192",
        "domain": "energy-systems-utilities",
        "task_type": "grid-reliability-outage-analysis",
        "objective": "Anomaly Detection & Diagnostics",
        "as_of": "2026-11-04",
        "field_terms": ["device"],
        "decision": "which feeder Kestrel Falls Municipal Utilities' overhead line patrol crew works in the week of "
                    "9 November 2026, if any",
        "deliverables": ["line_patrol_2026-11-09.xlsx", "reliability_2026.svg"],
        "distractor_files": ["target/" + PK.FILES[k] for k in PK.DISTRACTORS],
        "files": {},
    }
    for k, fn in PK.FILES.items():
        md["files"]["target/" + fn] = {"source": "constructed for this task (fictional municipal utility)",
                                       "date": "2026-11-03", "licence": "CC BY 4.0 (task author)", "covers": desc[k],
                                       "made": "generated by task192/generator from fixed seeds"}
    return md


def main():
    t0 = time.time()
    net, wx, stk, S, TR, added = world()
    info = cut(TARGET, net, wx, stk, S, TR)
    res = G.compute(TARGET)
    if os.path.isdir(GOLDEN):
        shutil.rmtree(GOLDEN)
    os.makedirs(GOLDEN)
    F = deliver.write(res, GOLDEN)
    for fn in os.listdir(GOLDEN):
        os.utime(os.path.join(GOLDEN, fn), (STAMP, STAMP))
    lad = G.ladder(TARGET, res)
    F["ladder"] = {f: {k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()} for f, r in lad.items()}
    F["constants"] = dict(t_med=W.T_MED_2026, n_sys=TR["n_sys"], window=["2026-08-01", "2026-10-31"],
                          added_late=added, sim_seed=SIM_SEED, patrol_week=W.PATROL_WEEK.isocalendar()[1],
                          drp04_sections=[2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 3.1, 3.2, 4.1, 4.2, 5.2, 5.3, 5.4, 6.1],
                          band_per_cent=2, band_spread_per_cent=4)
    F["pack"] = info
    json.dump(F, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True, default=str)
    json.dump(metadata(info), open(os.path.join(TASK, "metadata.json"), "w"), indent=1)
    n = archive(TARGET, os.path.join(TASK, "target.zip"))
    import writeup
    writeup.main()
    print("built in %.0fs: call %s, runner-up %s, groups %d and %d, others at most %d; MEDs %s; T_MED %.2f; "
          "zip members %d; added %s" % (time.time() - t0, F["call"], F["runner_up"], F["call_group"]["n"],
                                       F["ru_group"]["n"], F["others_max"], F["meds"], W.T_MED_2026, n, added))


if __name__ == "__main__":
    main()
