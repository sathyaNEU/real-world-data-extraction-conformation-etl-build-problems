"""task247 ask layer against the careful solver's routes, on the cut pack.

    python3 task247/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The ask of the design
note's ask sheet gives 16 figures: each site's hours at or above its maximum monthly mean at its logger while in the
water, June to October 2024 to 2026 (whole numbers). Every route below is a complete pipeline over the cut pack (the
logger log, the pin register, the readings and the site register for the ask; both satellite records, the
climatology, the register and the bulletins for the call), scored figure by figure against figures.json; a figure is
kept only when it equals the golden.

The cracker is the careful solver. It lands the call (the observed days less the clear-sky difference, every other day
refilled from the observed days either side; verified against figures.json), reads every field by its plain meaning
(the log's pin, serial, deployed and retrieved times with the UTC mark the GPS put on some of them, and boats, its
notes; the pin register with its checked dates; the readings' local clock), executes every filed rule as worded, and
runs the hygiene battery a careful analyst runs unprompted: exact
duplicate rows in the log and the readings, every pin joined to the register and every serial found in both files
(anti-joins), one stop per pin on every service trip, no overlapping intervals per pin or per serial, the notes read
for what they say, each trip's clock checked against the loggers' own step out of the water (it agrees with the
log's UTC mark), and the readings trimmed to the logged times. Then it takes the ask on its natural read:
each log row at the site its pin's tag names in the pin register. The mirror stops at the default path on the call
(the past mean differences of observed and filled days taken out) and takes the ask on its natural read without the
battery (the register, the log's times as marked). The full includer reads the tags written before the re-tag of
August 2025 as the pins' earlier tags, from each trip's stop order, and has to give back figures.json exactly: the
route code's control (exit 1 when it does not). The stops are the sheet's other wrong paths, each scored as a route.

The pair is the ask sheet's formula: 38 recommendation and components, 7 instruction following, 55 asks over the ask
figures, the mirror keeping r of the 38 (its share of the call's 48 per-site criteria, the way the sheet has always
priced it), two careful responses on the call printed beside it."""
from __future__ import annotations

import csv
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import verify as V   # noqa: E402  (the bundle-only readers: the call, the bulletins, the slates, the loggers)

TASK = os.path.dirname(HERE)
REC, INS, ASK = 38.0, 7.0, 55.0
LEVELS = V.LEVELS


def pack_dir(arg):
    """The pack as a folder: target.zip unpacked into a scratch folder (removed after), or the folder given."""
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling247-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    inner = os.path.join(tmp, "target")
    folder = inner if os.path.isdir(inner) else tmp
    md5 = hashlib.md5(open(src, "rb").read()).hexdigest()
    return folder, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(folder)), md5)


def rows(folder, name):
    with open(os.path.join(folder, name), newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# ------------------------------------------------------------------ the call, both routes
def call_routes(folder, figs):
    """the cracker's call (the refill) and the mirror's (the default path), each scored on the call's 48 per-site
    criteria (whole-number maximum, level, verdict)"""
    codes, sites, mmm, days, di, nrt, obs, rep, clim = V.series(folder)
    past = np.array([d.year <= 2026 for d in days])
    both = past[None, :] & ~np.isnan(rep) & ~np.isnan(nrt)
    b_obs = float(np.mean((nrt - rep)[both & obs]))
    b_fill = float(np.mean((nrt - rep)[both & ~obs]))
    season = np.array([dt.date(2027, 6, 1) <= d <= dt.date(2027, 10, 31) for d in days])
    idx = np.arange(len(days))
    decl = V.declared(folder, codes)
    gold = {s["code"]: s for s in figs["sites"]}
    out = {}
    for name in ("refill", "default path", "regression"):
        est = {}
        if name == "regression":
            fa = (nrt - clim)[both & ~obs]
            ra = (rep - clim)[both & ~obs]
            k1, k0 = np.polyfit(fa, ra, 1)
        for k, c in enumerate(codes):
            x = np.where(np.isnan(nrt[k]), -99.0, nrt[k])
            if name == "refill":
                an = nrt[k] - b_obs - clim[k]
                o = obs[k]
                x = clim[k] + np.where(o, an, np.interp(idx, idx[o], an[o]))
            elif name == "default path":
                x = x - np.where(obs[k], b_obs, b_fill)
            else:
                x = np.where(obs[k], x - b_obs, clim[k] + k0 + k1 * (x - clim[k]))
            est[c] = float(V.dhw(x, mmm[c])[season].max())
        right = 0
        for c in codes:
            lv = V.level(est[c])
            v = "confirms" if lv == decl[c] else ("raises" if LEVELS.index(lv) > LEVELS.index(decl[c]) else "lowers")
            right += (int(round(est[c])) == gold[c]["dhw"]) + (lv == gold[c]["level"]) + (v == gold[c]["verdict"])
        on = [c for c in codes if est[c] >= 8]
        out[name] = dict(list=on, right=right, lands=on == figs["call"])
    return out


# ------------------------------------------------------------------ the ask: the loggers
P_ = lambda x: dt.datetime.strptime(x.replace(" UTC", ""), "%Y-%m-%d %H:%M")     # the digits as written


def marked_offsets(dep):
    """each trip's clock as the log marks it: five hours for the times written with the GPS's UTC mark"""
    out = {}
    for r in dep:
        for when, boat in (("deployed", "deployed_from"), ("retrieved", "retrieved_from")):
            if r[when]:
                out[(r[boat], r[when][:7])] = 5 if r[when].endswith(" UTC") else 0
    return out


def logger_files(folder):
    dep = rows(folder, V.F["deployments"])
    reg = {r["pin"]: r["site_code"] for r in rows(folder, V.F["pins"])}
    reads = {}
    for r in rows(folder, V.F["readings"]):
        reads.setdefault(r["serial"], []).append((P_(r["datetime_local"]), float(r["temperature_c"])))
    return dep, reg, reads


def trips_of(dep):
    ev = []
    for i, r in enumerate(dep):
        ev.append((P_(r["deployed"]), r["pin"], i))
        if r["retrieved"]:
            ev.append((P_(r["retrieved"]), r["pin"], i))
    ev.sort()
    trips, cur = [], []
    for e in ev:
        if cur and e[0] - cur[-1][0] > dt.timedelta(days=3):
            trips.append(cur)
            cur = []
        cur.append(e)
    trips.append(cur)
    return trips


def battery_b(dep, reg, reads):
    """the hygiene battery on the logger records: each line is (check, passed, detail)"""
    out = []
    tup = [tuple(r.values()) for r in dep]
    out.append(("exact duplicate rows in the log", len(tup) == len(set(tup)), "%d rows" % len(tup)))
    nread = sum(len(v) for v in reads.values())
    nkey = sum(len({t for t, _ in v}) for v in reads.values())
    out.append(("one reading per serial and hour", nread == nkey, "%d readings" % nread))
    out.append(("every pin in the log joins the pin register", {r["pin"] for r in dep} <= set(reg),
                "%d pins, %d in the register" % (len({r["pin"] for r in dep}), len(reg))))
    out.append(("every serial in both the log and the readings", {r["serial"] for r in dep} == set(reads),
                "%d serials" % len(set(reads))))
    trips = trips_of(dep)
    once = all(len({pin for _, pin, _ in t}) == 16 and
               all(sum(1 for _, p, i in t if p == pin and dep[i]["deployed"] and P_(dep[i]["deployed"]) == when) <= 1
                   for when, pin, _ in t) for t in trips)
    out.append(("one stop per pin on every service trip", once, "%d trips" % len(trips)))
    overl = 0
    for key in ("pin", "serial"):
        by = {}
        for r in dep:
            by.setdefault(r[key], []).append(r)
        for g in by.values():
            g.sort(key=lambda r: r["deployed"])
            overl += sum(1 for a, b in zip(g, g[1:]) if not a["retrieved"] or P_(a["retrieved"]) > P_(b["deployed"]))
    out.append(("no overlapping intervals per pin or per serial", overl == 0, "%d overlaps" % overl))
    named = [r["notes"] for r in dep if any(c.isdigit() for c in r["notes"]) and ("PB" in r["notes"] or "E0" in r["notes"])]
    out.append(("the notes read for what they say (none names a site or a pin)", not named,
                "%d notes" % sum(1 for r in dep if r["notes"])))
    return out


def clock_offsets(dep, reads):
    """each trip's clock from the loggers' own step out of the water against the logged retrieval (the verifier's
    reading of the readings)"""
    lag = {}
    for r in dep:
        if not r["retrieved"]:
            continue
        z = P_(r["retrieved"])
        x = [(t, v) for t, v in reads.get(r["serial"], []) if z - dt.timedelta(hours=9) <= t <= z + dt.timedelta(hours=3)]
        if len(x) < 4:
            continue
        j = max(range(1, len(x)), key=lambda i: x[i][1] - x[i - 1][1])
        lag.setdefault((r["retrieved_from"], r["retrieved"][:7]), []).append((z - x[j][0]).total_seconds() / 3600)
    return {k: (5 if np.median(v) > 3 else 0) for k, v in lag.items()}


def placement(folder, dep, reg, how):
    """each log row's site by a route"""
    if how == "register":
        return [reg[r["pin"]] for r in dep]
    if how == "stop order":
        return V.pin_site(folder, rows(folder, V.F["sites"]))[0]
    if how == "earlier trips dropped":
        north = [s["site_code"] for s in sorted(rows(folder, V.F["sites"]), key=lambda s: -float(s["latitude"]))]
        keep = set()
        for t in trips_of(dep):
            seq = []
            for _, pin, i in t:
                if pin not in seq:
                    seq.append(pin)
            if [reg[p] for p in seq] == north:
                keep |= {i for _, _, i in t}
        return [reg[r["pin"]] if i in keep else None for i, r in enumerate(dep)]
    if how == "pairs across the re-tag":
        # a serial that also went in under a register trip's tag is placed where that tag is; every other row by the
        # register
        stop = placement(folder, dep, reg, "earlier trips dropped")
        later = {}
        for r, s in zip(dep, stop):
            if s is not None:
                later.setdefault(r["serial"], s)
        return [later.get(r["serial"], reg[r["pin"]]) if s is None else s for r, s in zip(dep, stop)]
    raise ValueError(how)


def hours_of(dep, reads, mmm, where, offset, trim=True):
    out = {}
    for r, site in zip(dep, where):
        if not r["retrieved"] or site is None:
            continue
        a = P_(r["deployed"]) - dt.timedelta(hours=offset.get((r["deployed_from"], r["deployed"][:7]), 0))
        z = P_(r["retrieved"]) - dt.timedelta(hours=offset.get((r["retrieved_from"], r["retrieved"][:7]), 0))
        out[site] = out.get(site, 0) + sum(1 for t, v in reads.get(r["serial"], []) if (not trim or a <= t <= z)
                                           and t.year in (2024, 2025, 2026) and 6 <= t.month <= 10 and v >= mmm[site])
    return out


def score(route, figs):
    return ["hours " + s["code"] for s in figs["sites"] if route.get(s["code"]) == s["hours"]]


def main(arg=None):
    folder, scratch, stamp = pack_dir(arg)
    try:
        return run(folder, stamp)
    finally:
        if scratch:
            shutil.rmtree(scratch)


def run(folder, stamp):
    print("pack: " + stamp)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    n = len(figs["sites"])
    calls = call_routes(folder, figs)
    print("the cracker's call (refill): %s (%s); %d of 48 per-site criteria"
          % (", ".join(calls["refill"]["list"]), "lands the golden" if calls["refill"]["lands"] else "MISSES",
             calls["refill"]["right"]))
    for k in ("default path", "regression"):
        print("a response off the call at the %s: %s (%s); %d of 48 per-site criteria"
              % (k, ", ".join(calls[k]["list"]), "off the call" if not calls[k]["lands"] else "ON THE CALL",
                 calls[k]["right"]))
    if not calls["refill"]["lands"] or calls["default path"]["lands"]:
        print("the rows below assume the cracker on the call and the mirror off it: they are not")
        return 1

    dep, reg, reads = logger_files(folder)
    mmm = {r["site_code"]: float(r["mmm_c"]) for r in rows(folder, V.F["sites"])}
    print("\nthe cracker's hygiene battery on the logger records:")
    bat = battery_b(dep, reg, reads)
    for check, passed, detail in bat:
        print("  %-4s %s (%s)" % ("ok" if passed else "FLAG", check, detail))
    off = marked_offsets(dep)
    lagged = clock_offsets(dep, reads)
    agree = all(off[k] == v for k, v in lagged.items())
    print("  %-4s each trip's clock against the loggers' step out of the water agrees with the log's UTC mark (%s)"
          % ("ok" if agree else "FLAG", ", ".join("%s %s" % k for k, v in sorted(off.items()) if v)))
    north = [s["site_code"] for s in sorted(rows(folder, V.F["sites"]), key=lambda s: -float(s["latitude"]))]
    follow = 0
    trips = trips_of(dep)
    for t in trips:
        seq = []
        for _, pin, i in t:
            if pin not in seq:
                seq.append(pin)
        follow += [reg[p] for p in seq] == north
    print("  (not a battery item) service trips whose stops read through the register as the sites north to south: "
          "%d of %d" % (follow, len(trips)))

    routes = {
        "cracker (careful: the battery, the clock checked, each pin through the register)":
            hours_of(dep, reads, mmm, placement(folder, dep, reg, "register"), off),
        "mirror (the default path's natural read: the register, the log's times as marked)":
            hours_of(dep, reads, mmm, placement(folder, dep, reg, "register"), off),
        "full includer (control: the earlier tags from the stop order, the clock checked)":
            hours_of(dep, reads, mmm, placement(folder, dep, reg, "stop order"), off),
        "stop: the trips before the re-tag dropped (the over-clean), the clock checked":
            hours_of(dep, reads, mmm, placement(folder, dep, reg, "earlier trips dropped"), off),
        "stop: the pairs across the re-tag placed, the rest by the register, the clock checked":
            hours_of(dep, reads, mmm, placement(folder, dep, reg, "pairs across the re-tag"), off),
        "stop: the earlier tags from the stop order, the UTC mark ignored":
            hours_of(dep, reads, mmm, placement(folder, dep, reg, "stop order"), {}),
        "stop: the earlier tags from the stop order, nothing trimmed":
            hours_of(dep, reads, mmm, placement(folder, dep, reg, "stop order"), off, trim=False),
    }
    keeps = {}
    print("\nper route, ask figures kept of %d:" % n)
    for name, route in routes.items():
        keeps[name] = len(score(route, figs))
        print("  %-88s %2d" % (name, keeps[name]))
    full = keeps["full includer (control: the earlier tags from the stop order, the clock checked)"]
    if full != n:
        print("CONTROL FAILED: the full includer keeps %d of %d, the route code does not reproduce figures.json"
              % (full, n))
        return 1
    print("  control: the full includer reproduces figures.json (%d of %d)" % (full, n))

    kc = keeps["cracker (careful: the battery, the clock checked, each pin through the register)"]
    km = keeps["mirror (the default path's natural read: the register, the log's times as marked)"]
    for rung in ("default path", "regression"):
        r = round(REC * 0.75 * calls[rung]["right"] / 48.0, 1)
        c, s_ = REC + INS + ASK * kc / n, r + INS + ASK * km / n
        print("\nthe sheet's formula with the mirror at the %s (r = %.1f): cracker %.1f, mirror %.1f, pair %.1f"
              % (rung, r, c, s_, (c + s_) / 2))
    two = REC + INS + ASK * kc / n
    print("two careful responses on the call: %.1f each" % two)
    if_found = (REC + INS + ASK + max(round(REC * 0.75 * calls[k]["right"] / 48.0, 1) for k in ("default path",
                "regression")) + INS + ASK * km / n) / 2
    print("if the cracker reads the earlier tags (keeps all %d): pair %.1f" % (n, if_found))
    r = max(round(REC * 0.75 * calls[k]["right"] / 48.0, 1) for k in ("default path", "regression"))
    c, s_ = REC + INS + ASK * kc / n, r + INS + ASK * km / n
    print("\nCracker keeps: %d of %d ask figures" % (kc, n))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * km / n))
    print("Pair ceiling: %.1f (the worse mirror, r = %.1f)" % ((c + s_) / 2, r))
    return 0 if kc == 0 else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
