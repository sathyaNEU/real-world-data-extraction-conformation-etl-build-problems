"""task136 ask layer against the careful solver's routes, on the cut pack.

    python3 task136/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The four DER Register
asks give 32 figures: per feeder, the active sites it supplies, how many of them were first lodged in FY2025-26, and
the inverter capacity and battery storage at those sites. Each route below is a complete pipeline over the DER
Register extract, the NMI re-allocation log and the network model, scored figure by figure against figures.json; a
figure is kept within half a unit of the prompt's rounding (a count exactly, kW and kWh within 5).

The cracker lands the call, runs the hygiene battery (an NMI read at ten characters, a replaced NMI read at its
replacement through the re-allocation log, exact duplicate rows dropped) and takes each ask on its natural read: the
sites placed by the extract's own feeder column, a site dated by its active connections, the device rows summed once
the duplicates are gone. The mirror is the best response off the call (the default path, YRB24) on its own natural
read, the pipeline without the battery: NMIs as lodged, the extract's feeder, every device row summed. The single
cracks are the cracker finding one device each; the full includer handles all four and has to give back figures.json
exactly (the route code's control).

The pair is the ask sheet's formula: 36 recommendation and components, 9 instruction following, 55 asks over 32
figures, a method credit of 8 per cent on every figure not kept, a response off the call keeping 4 of the 36; the same
on the comparable 38, 7 and 55 (a wrong call keeping 5) is printed beside it. Pair ceiling is the worst of the
measured pair and every single crack, on either weighting."""
from __future__ import annotations

import hashlib
import itertools
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C     # noqa: E402
import common as K   # noqa: E402

TASK = os.path.dirname(HERE)
CREDIT = 0.08                         # the sheet's method credit on an ask figure not kept
WEIGHTS = {"ask sheet (36, 9, 55; off the call keeps 4)": (36.0, 9.0, 55.0, 4.0),
           "comparable (38, 7, 55; off the call keeps 5)": (38.0, 7.0, 55.0, 5.0)}
FY0, FY1 = (pd.Timestamp(d) for d in K.LAST_FY)
ASKS = [("active_sites", "Ask 1, active sites", 0.5), ("first_lodged_fy2025_26", "Ask 2, first lodged FY2025-26", 0.5),
        ("inverter_kw", "Ask 3, inverter capacity (kW)", 5.0), ("storage_kwh", "Ask 4, battery storage (kWh)", 5.0)]

# a route: key (lodged, ten, hygiene), place (stamp, network), count (sites, connections), first (active, all),
# inv and bat (rows, dedupe, once, convention)
CRACKER = dict(key="hygiene", place="stamp", count="sites", first="active", inv="dedupe", bat="dedupe")
MIRROR = dict(key="lodged", place="stamp", count="sites", first="active", inv="rows", bat="rows")
FULL = dict(key="hygiene", place="network", count="sites", first="all", inv="convention", bat="convention")
CRACKS = {
    "places each site by the network model's feeder (NPP-114 3.1), the stamp found": dict(place="network"),
    "dates each site from every AC connection at it, decommissioned ones included": dict(first="all"),
    "reads an older-portal two-inverter row as the connection's total": dict(inv="convention"),
    "counts a Sungrow SBR stack's module rows once": dict(bat="convention"),
}


def keyed(L, key):
    """The DER extract with each row's site: as lodged, at ten characters, or at ten characters and through the
    re-allocation log."""
    der = L["der"]
    site = der.nmi
    if key in ("ten", "hygiene"):
        site = site.map(C.norm_nmi)
    if key == "hygiene":
        mp = dict(zip(L["realloc"].old_nmi, L["realloc"].new_nmi))
        site = site.map(lambda s: mp.get(s, s))
    return der.assign(site=site.values, reg=pd.to_datetime(der.registered_date))


def route(L, r):
    """The 32 figures a route gives, keyed as figures.json keys them."""
    cols = list(L["der"].columns)
    allrows = keyed(L, r["key"])
    act = allrows[allrows.ac_connection_status == "Active"]
    fd = act.feeder if r["place"] == "stamp" else act.site.map(L["feeder"])
    act = act.assign(fd=fd.values)
    act = act[act.fd.isin(K.FEEDERS)]
    out = {f: {} for f in K.FEEDERS}
    # Ask 1: sites (or connections) by feeder
    n1 = act.groupby("fd").site.nunique() if r["count"] == "sites" else act.groupby("fd").ac_connection_id.nunique()
    # Ask 2: of those sites, the ones whose first lodgement falls in FY2025-26
    first = (act if r["first"] == "active" else allrows).groupby("site").reg.min()
    pairs = act[["fd", "site"]].drop_duplicates()
    pairs = pairs.assign(first=pairs.site.map(first))
    n2 = pairs[(pairs["first"] >= FY0) & (pairs["first"] <= FY1)].groupby("fd").size()

    def per_connection(rows, qty, how, whole_row):
        if how == "dedupe":
            rows = rows.drop_duplicates(subset=cols)
        g = rows.groupby("ac_connection_id")
        once, total = g[qty].first(), g[qty].sum()
        if how == "once":
            per = once
        elif how in ("rows", "dedupe"):
            per = total
        else:
            per = pd.Series(np.where(whole_row(g, once), once, total), index=once.index)
        return per.groupby(g.fd.first()).sum()

    def portal_total(g, once):
        plate = g.model.first().map(C.nameplate)
        n = g.size()
        return (n > 1) & plate.notna() & ((once - plate * n).abs() < 0.011)

    def stack_total(g, once):
        return g.model.first().isin(C.SYSTEM_LODGED)

    inv = act[act.device_type == "Inverter"].assign(kw=lambda d: d.rated_power_kw.astype(float))
    bat = act[act.device_type == "Battery"].assign(kwh=lambda d: d.storage_capacity_kwh.astype(float))
    n3 = per_connection(inv, "kw", r["inv"], portal_total)
    n4 = per_connection(bat, "kwh", r["bat"], stack_total)
    for f in K.FEEDERS:
        out[f] = {"active_sites": int(n1.get(f, 0)), "first_lodged_fy2025_26": int(n2.get(f, 0)),
                  "inverter_kw": float(n3.get(f, 0.0)), "storage_kwh": float(n4.get(f, 0.0))}
    return out


def golden_der():
    der = json.load(open(os.path.join(HERE, "figures.json")))["der"]
    return {f: {k: float(str(v).replace(",", "")) for k, v in der[f].items()} for f in K.FEEDERS}


def kept(fig, gold):
    """Per ask, the figures within half a unit of the prompt's rounding."""
    return {name: sum(abs(fig[f][k] - gold[f][k]) <= half + 1e-9 for f in K.FEEDERS) for k, name, half in ASKS}


def pair(kc, km, n, w):
    rec, ins, ask, off = w
    pts = lambda k: ask * (k + CREDIT * (n - k)) / n
    c, s = rec + ins + pts(kc), off + ins + pts(km)
    return c, s, (c + s) / 2.0


def pack_dir(arg):
    """The pack as a folder: target.zip unpacked into a scratch folder (removed after), or the folder given."""
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling136-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    md5 = hashlib.md5(open(src, "rb").read()).hexdigest()
    return tmp, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(tmp)), md5)


def main(arg=None):
    folder, scratch, stamp = pack_dir(arg)
    try:
        return run(folder, stamp)
    finally:
        if scratch:
            shutil.rmtree(scratch)


def run(folder, stamp):
    print("pack: " + stamp)
    L = C.load(folder)
    gold = golden_der()
    n = 4 * len(K.FEEDERS)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    fc = C.forecast(L)
    call = (fc["winner"], round(fc["excess"][fc["winner"]] + 1e-12, 1), fc["runner"])
    gcall = figs["call"]
    on_call = call == (gcall["feeder"], float(gcall["excess_mw"]), gcall["runner_up"])
    r0 = C.forecast(L, measure="systems", basis="letterboxed")
    print("cracker's call: %s %.1f MW over hosting capacity, runner-up %s (%s the golden)" % (
        call + ("lands" if on_call else "MISSES",)))
    print("mirror's call (default path): %s %.1f MW, runner-up %s (%s)" % (
        r0["winner"], r0["excess"][r0["winner"]], r0["runner"],
        "off the call" if r0["winner"] != gcall["feeder"] else "ON THE CALL"))
    if not on_call or r0["winner"] == gcall["feeder"] or r0["runner"] == gcall["runner_up"]:
        print("the rows below assume the cracker on the call and the mirror off it with another runner-up: they are not")
        return 1

    full = kept(route(L, FULL), gold)
    if sum(full.values()) != n:
        print("CONTROL FAILED: the full includer's route gives %s of %d, the route code does not reproduce the golden"
              % (full, n))
        return 1

    def scored(r):
        k = kept(route(L, r), gold)
        return k, sum(k.values())

    kc_by, kc = scored(CRACKER)
    km_by, km = scored(MIRROR)
    for who, r in (("cracker", CRACKER), ("mirror", MIRROR)):
        fig = route(L, r)
        print("\n%s's figures by feeder (golden in brackets):" % who)
        for k, name, half in ASKS:
            print("  %-30s %s" % (name, "; ".join("%s %s (%s)" % (f, "{:,.0f}".format(fig[f][k]), "{:,.0f}".format(gold[f][k]))
                                                  for f in K.FEEDERS)))
    print("\nper ask, figures kept of %d each:" % len(K.FEEDERS))
    print("  %-34s %-9s %-9s %s" % ("", "cracker", "mirror", "full includer (control)"))
    for _, name, _ in ASKS:
        print("  %-34s %-9d %-9d %d" % (name, kc_by[name], km_by[name], full[name]))
    print("  %-34s %-9d %-9d %d of %d" % ("all asks", kc, km, sum(full.values()), n))

    worst = []
    for wname, w in WEIGHTS.items():
        c, s, p = pair(kc, km, n, w)
        print("\n%s: cracker %.1f, mirror %.1f, pair %.1f" % (wname, c, s, p))
        worst.append(p)
        for nm, ch in CRACKS.items():
            k = scored(dict(CRACKER, **ch))[1]
            pc = pair(k, km, n, w)[2]
            worst.append(pc)
            print("  if the cracker %s: %d of %d, pair %.1f" % (nm, k, n, pc))
        km2 = scored(dict(CRACKER))[1]
        pm = pair(kc, km2, n, w)[2]
        worst.append(pm)
        print("  if the mirror runs the hygiene battery (the cracker's ask path, off the call): %d of %d, pair %.1f"
              % (km2, n, pm))
        two = max(((a, b, scored(dict(CRACKER, **CRACKS[a], **CRACKS[b]))[1]) for a, b in
                   itertools.combinations(CRACKS, 2)), key=lambda t: t[2])
        print("  (two devices found, the worst pair: %d of %d, pair %.1f; the full includer: %d of %d, pair %.1f; "
              "both top responses on the call with no device found: %.1f)" % (
                  two[2], n, pair(two[2], km, n, w)[2], n, n, pair(n, km, n, w)[2],
                  (w[0] + w[1] + w[2] * CREDIT) * 1.0))
    print("\nCracker keeps: %d of %d ask figures" % (kc, n))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * (km + CREDIT * (n - km)) / n))
    print("Pair ceiling: %.1f (the worst of the measured pair and each single crack, on either weighting)" % max(worst))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
