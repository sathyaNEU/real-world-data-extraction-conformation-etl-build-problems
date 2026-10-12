"""The answer, computed from the world in memory: the load table and every graded figure.
verify_pack.py recomputes all of it from the shipped files on a code path that shares nothing."""
import datetime as dt
from collections import defaultdict
from decimal import Decimal

import ledger as L
from params import ACCOUNTS, MAP_V2, GROUP_CLASSES_V2, SITES, COUNT_CUTOFF_LOCAL
import world as W

D = Decimal
Z = D("0")


def sighting(w):
    """Valid sightings: a scan taken inside the window (Monday 28 September to 5:00 pm local on Friday
    9 October) matched on the keyed rating plate where there is one and on the tag otherwise, or a line on the
    Raymond Terrace count sheet. Returns {asset id: site}."""
    v = w.verification
    seen = {}
    by_tag = {a["tag"]: a for a in w.assets if a["tag"]}
    by_serial = {a["serial"]: a for a in w.assets if a["serial"] and a["kind"] != "duplicate"}
    cutoff_utc = W.utc_from_local(COUNT_CUTOFF_LOCAL)
    start_utc = W.utc_from_local(W.WINDOW_START_LOCAL)
    for a, site, t_utc, tag, serial in v["scans"]:
        if t_utc >= cutoff_utc or t_utc < start_utc:      # the time the scan was taken, whatever the clock wrote
            continue
        # a keyed rating plate names the unit in hand; the tag is read only where no plate was keyed
        hit = by_serial.get(serial) if serial in by_serial else by_tag.get(tag)
        if hit is not None:
            seen[hit["id"]] = site
    for a, site in v["sheet"]:
        seen[a["id"]] = site
    return seen


def solve(w, variant=None, seen=None, mapping=None, reclass=True):
    eng = L.Engine(w.ledger_assets(), variant)
    seen = sighting(w) if seen is None else seen
    mapping = MAP_V2 if mapping is None else mapping
    rows = []
    written_off = []
    for a in w.ledger_assets():
        if a["disposed"]:
            continue
        nbv_dec = eng.nbv(a, L.DEC26)
        if a["tag"] and a["id"] not in seen and nbv_dec == 0:
            written_off.append(a)
            continue
        acc_ac = ACCOUNTS[a["category"]][0]
        if reclass and a is w.joinery:
            acc_ac = "1-6140"
        site = seen.get(a["id"], a["site"])
        rows.append(dict(asset=a["id"], description=a["description"], site=site, group_class=mapping[acc_ac],
                         cost=a["cost"], acc_sep=eng.accumulated(a, L.SEP26), q4=eng.q4(a),
                         acc_dec=eng.accumulated(a, L.DEC26), nbv=nbv_dec, remaining=eng.remaining_at_cutover(a),
                         h2=eng.h2(a), a=a))
    out = dict(rows=rows, written_off=written_off, eng=eng)
    out["h2"] = sum((r["h2"] for r in rows), Z)
    per = {}
    for s in SITES:
        rr = [r for r in rows if r["site"] == s]
        per[s] = dict(nbv_sep=sum((r["cost"] - r["acc_sep"] for r in rr), Z), q4=sum((r["q4"] for r in rr), Z),
                      nbv_load=sum((r["nbv"] for r in rr), Z), h2=sum((r["h2"] for r in rr), Z),
                      nil_count=sum(1 for r in rr if r["nbv"] == 0),
                      nil_cost=sum((r["cost"] for r in rr if r["nbv"] == 0), Z))
    out["sites"] = per
    cls = defaultdict(lambda: Z)
    for r in rows:
        cls[r["group_class"]] += r["nbv"]
    out["classes"] = dict(cls)
    out["load_rows"] = len(rows)
    out["load_nbv"] = sum((r["nbv"] for r in rows), Z)
    out["load_cost"] = sum((r["cost"] for r in rows), Z)
    out["q4"] = sum((r["q4"] for r in rows), Z)
    return out


def rnd(x):
    """Whole dollars, half up."""
    return int(D(x).quantize(D("1"), rounding="ROUND_HALF_UP"))
