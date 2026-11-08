"""The two asks from the 2026 session export: each hub's high-power charges begun January to October 2026 and the
energy they delivered, under Schedule 6 (a charge is a vehicle's connection from connection to disconnection, counted
once; its energy what the meter registered). The golden handling and each response's handling, on the cut pack."""
import csv
import datetime as dt
import os
from decimal import ROUND_HALF_UP, Decimal

import parse as PA

WIN_A = PA.sec(dt.datetime(2026, 1, 1, tzinfo=PA.IE).astimezone(PA.UTC))
WIN_B = PA.sec(dt.datetime(2026, 11, 1, tzinfo=PA.IE).astimezone(PA.UTC))


def mwh(wh):
    return float(Decimal(wh / 1e6).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def load(target):
    units, alias, serial, hubs = PA.read_register(target)
    recs = []
    with open(os.path.join(target, "charging_sessions_2026.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            recs.append(dict(sid=r["session_id"], cp=r["charge_point_id"], con=int(r["connector_id"]),
                             a=PA.from_utc_iso(r["start_time_utc"]), b=PA.from_utc_iso(r["stop_time_utc"]),
                             m0=int(r["meter_start_wh"]), m1=int(r["meter_stop_wh"]), kwh=float(r["energy_kwh"]), tag=r["id_tag"]))
    return recs, units, [h["code"] for h in hubs]


def dedup(recs):
    seen, out = set(), []
    for r in recs:
        if r["sid"] in seen:
            continue
        seen.add(r["sid"])
        out.append(r)
    return out


def per_connector(recs):
    by = {}
    for r in recs:
        by.setdefault((r["cp"], r["con"]), []).append(r)
    for k in by:
        by[k].sort(key=lambda r: (r["a"], r["sid"]))
    return by


def connections(recs, register=True, adjacency=True, token_merge=False):
    """Records grouped into charges: a record continues the one before it on its connector when it opens above that
    record's closing register (energy flowed with no record open) or within five seconds of its close."""
    out = []
    for key, lst in sorted(per_connector(recs).items()):
        cur = None
        for r in lst:
            cont = False
            if cur is not None:
                prev = cur[-1]
                if register and r["m0"] > prev["m1"]:
                    cont = True
                if adjacency and 0 <= r["a"] - prev["b"] <= 5:
                    cont = True
                if token_merge and r["tag"] and r["tag"] == prev["tag"] and r["a"] - prev["b"] < 1800:
                    cont = True
            if cont:
                cur.append(r)
            else:
                if cur:
                    out.append(cur)
                cur = [r]
        if cur:
            out.append(cur)
    return out


def tally(groups, units, hubs, energy="register"):
    n = {h: 0 for h in hubs}
    e = {h: 0 for h in hubs}
    for g in groups:
        u = units.get(g[0]["cp"])
        if u is None or u["model"] != "HX150":
            continue
        if not (WIN_A <= g[0]["a"] < WIN_B):
            continue
        wh = (g[-1]["m1"] - g[0]["m0"]) if energy == "register" else int(round(sum(r["kwh"] for r in g) * 1000))
        if wh <= 0:
            continue
        n[u["hub"]] += 1
        e[u["hub"]] += wh
    return n, e


def golden(target):
    recs, units, hubs = load(target)
    n, e = tally(connections(dedup(recs)), units, hubs)
    return {h: n[h] for h in hubs}, {h: mwh(e[h]) for h in hubs}, e


def cracker(target):
    """The battery: one copy of each session number, failed starts out, one token on one connector within half an
    hour merged, the energy column summed."""
    recs, units, hubs = load(target)
    recs = [r for r in dedup(recs) if r["kwh"] > 0]
    n, e = tally(connections(recs, register=False, adjacency=False, token_merge=True), units, hubs, energy="column")
    return n, {h: mwh(e[h]) for h in hubs}


def full_includer(target):
    """The battery plus the register merge: every record that opens above the last one's closing register joined to
    it, energy from the registers; the card continuations (one to four seconds on, register unchanged) left."""
    recs, units, hubs = load(target)
    recs = [r for r in dedup(recs) if r["kwh"] > 0]
    n, e = tally(connections(recs, register=True, adjacency=False, token_merge=True), units, hubs)
    return n, {h: mwh(e[h]) for h in hubs}


def register_advance(target):
    """Each unit's register advance over its window records, a stress row for the energy block."""
    recs, units, hubs = load(target)
    recs = [r for r in dedup(recs) if WIN_A <= r["a"] < WIN_B]
    n, _ = tally(connections([r for r in recs if r["kwh"] > 0], register=False, adjacency=False, token_merge=True), units, hubs,
                 energy="column")
    e = {h: 0 for h in hubs}
    for (cp, con), lst in per_connector(recs).items():
        u = units.get(cp)
        if u and u["model"] == "HX150":
            e[u["hub"]] += max(r["m1"] for r in lst) - min(r["m0"] for r in lst)
    return n, {h: mwh(e[h]) for h in hubs}


def natural(target):
    recs, units, hubs = load(target)
    n = {h: 0 for h in hubs}
    e = {h: 0.0 for h in hubs}
    for r in recs:
        u = units.get(r["cp"])
        if u and u["model"] == "HX150" and WIN_A <= r["a"] < WIN_B:
            n[u["hub"]] += 1
            e[u["hub"]] += r["kwh"]
    return n, {h: mwh(e[h] * 1000) for h in hubs}


def kept(resp, gold):
    return sum(1 for h in gold if resp[h] == gold[h])
