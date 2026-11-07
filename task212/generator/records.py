"""Cut the main-call record systems from the clean truth, each in its own idiom (clock, units, codes).

Sorter container-build log (UTC, hub numbers), DWS induction records (local time with offset, grams, mm), manifest
lines (sender declared kg), the audit app's headers and findings (hub names, local time, the damage code list
replaced on 1 August).
"""
import datetime as dt
import numpy as np
import pandas as pd
from world import HUBS, UTC_OFFSET_H

HUB_NO = {h[0]: h[1] for h in HUBS}
HUB_NAME = {h[0]: h[2] for h in HUBS}
OLD_CODES = {"crush": "D1", "tear": "D2", "wet": "D3", "open": "D4", "puncture": "D5"}
NEW_CODES = {"crush": "AP", "tear": "RO", "wet": "HU", "open": "AB", "puncture": "PE"}
CODE_SWITCH = dt.date(2026, 8, 1)
OLD_KEYER_DEPOTS = ("Durango", "Getafe")   # two depots' handhelds kept the old list loaded after 1 August


def _gap_next(par):
    t = par.scan_local.values.astype("datetime64[s]").astype(np.int64)
    same = par.cage_label.values[1:] == par.cage_label.values[:-1]
    g = np.full(len(par), 10 ** 6, dtype=np.int64)
    g[:-1] = np.where(same, t[1:] - t[:-1], 10 ** 6)
    return g


def load_scans(w, seed):
    """One row per container-build event: OPEN, LOAD, NOREAD, CLOSE; UTC; hub number; chute; device."""
    rng = np.random.default_rng(seed + 10)
    par = w["parcels"].sort_values(["cage_label", "pos"]).reset_index(drop=True)
    n = len(par)
    gnext = _gap_next(par)
    noread = (rng.random(n) < 0.018) & (gnext >= 4)
    rescan = (rng.random(n) < 0.012) & (gnext >= 6) & ~noread
    d_nr = np.minimum(rng.integers(2, 10, n), gnext - 1)
    d_rs = np.minimum(rng.integers(3, 11, n), gnext - 1)
    utc = par.scan_local - pd.Timedelta(hours=UTC_OFFSET_H)
    chute = _chutes(w["depots"], seed)
    hht = {h: ["HHT%02d" % int(x) for x in np.random.default_rng(seed + 12 + i).choice(np.arange(1, 40), 4, replace=False)]
           for i, h in enumerate(HUB_NO)}
    hh = np.array([hht[h][int(k)] for h, k in zip(par.hub, rng.integers(0, 4, n))])
    base = pd.DataFrame({"hub_no": par.hub.map(HUB_NO).values, "chute": par.depot.map(chute).values,
                         "cage_label": par.cage_label.values})
    rows = []
    a = base.copy(); a["event"] = np.where(noread, "NOREAD", "LOAD"); a["barcode"] = np.where(noread, "", par.barcode)
    a["scan_utc"] = utc.values; a["device"] = "AUTO"; rows.append(a)
    b = base[noread].copy(); b["event"] = "LOAD"; b["barcode"] = par.barcode[noread].values
    b["scan_utc"] = (utc[noread] + pd.to_timedelta(d_nr[noread], unit="s")).values; b["device"] = hh[noread]; rows.append(b)
    c = base[rescan].copy(); c["event"] = "LOAD"; c["barcode"] = par.barcode[rescan].values
    c["scan_utc"] = (utc[rescan] + pd.to_timedelta(d_rs[rescan], unit="s")).values; c["device"] = hh[rescan]; rows.append(c)
    first = par.groupby("cage_label").scan_local.min() - pd.Timedelta(hours=UTC_OFFSET_H)
    last = par.groupby("cage_label").scan_local.max() - pd.Timedelta(hours=UTC_OFFSET_H)
    cg = par.drop_duplicates("cage_label").set_index("cage_label")
    k = len(first)
    o = pd.DataFrame({"hub_no": cg.hub.map(HUB_NO).reindex(first.index).values,
                      "chute": cg.depot.map(chute).reindex(first.index).values, "cage_label": first.index,
                      "event": "OPEN", "barcode": "",
                      "scan_utc": (first - pd.to_timedelta(rng.integers(120, 540, k), unit="s")).values, "device": "HMI"})
    cl = o.copy(); cl["event"] = "CLOSE"
    cl["scan_utc"] = (last.reindex(first.index) + pd.to_timedelta(rng.integers(60, 360, k), unit="s")).values
    rows += [o, cl]
    s = pd.concat(rows, ignore_index=True)
    s["scan_utc"] = pd.to_datetime(s.scan_utc).dt.floor("s")
    s = s.sort_values(["hub_no", "scan_utc", "cage_label", "event"], kind="mergesort").reset_index(drop=True)
    return s[["hub_no", "chute", "cage_label", "event", "barcode", "scan_utc", "device"]]


def dws(w, seed):
    """Dimension-weight-scan records at induction: local time with offset, grams, millimetres; re-weighs."""
    rng = np.random.default_rng(seed + 13)
    par = w["parcels"]
    n = len(par)
    induct = par.scan_local - pd.to_timedelta(rng.integers(120, 1400, n), unit="s")
    wg = np.round(par.weight_kg.values * 1000 * rng.normal(1, 0.006, n) / 5) * 5
    vol = par.weight_kg.values * rng.uniform(2.5, 9.0, n) * 1000
    L = np.round(np.cbrt(vol * rng.uniform(1.3, 2.2, n)) * 10)
    W = np.round(np.cbrt(vol) * 10)
    H = np.maximum(15, np.round(vol * 1000 / np.maximum(L * W, 1)))
    shape = par.pack.map({"BOX": "BOX", "BAG": "BAG", "FLYER": "FLY"}).values
    st = np.array(["DWS-%02d-%d" % (HUB_NO[h], 1 + int(x)) for h, x in zip(par.hub, rng.integers(0, 3, n))])
    d = pd.DataFrame({"barcode": par.barcode.values, "hub_no": par.hub.map(HUB_NO).values,
                      "induct_local": induct.dt.strftime("%Y-%m-%dT%H:%M:%S+02:00").values,
                      "weight_g": wg.astype(int), "length_mm": L.astype(int), "width_mm": W.astype(int),
                      "height_mm": H.astype(int), "shape": shape, "station": st})
    rw = rng.random(n) < 0.008
    d2 = d[rw].copy()
    d2["weight_g"] = (np.round(d2.weight_g * rng.normal(1, 0.01, len(d2)) / 5) * 5).astype(int)
    t2 = pd.to_datetime(d2.induct_local.str[:19]) + pd.to_timedelta(rng.integers(40, 300, len(d2)), unit="s")
    d2["induct_local"] = t2.dt.strftime("%Y-%m-%dT%H:%M:%S+02:00").values
    out = pd.concat([d, d2]).sort_values(["hub_no", "induct_local", "barcode"], kind="mergesort").reset_index(drop=True)
    return out


def manifests(w, seed):
    """Manifest lines as the senders' integrations send them: account, service, declared kg, fragile flag."""
    rng = np.random.default_rng(seed + 14)
    par = w["parcels"]
    acc = w["accounts"].set_index("account")
    dflt = acc.declared_default_kg.reindex(par.account).values
    est = np.round(par.weight_kg.values * rng.uniform(0.7, 1.4, len(par)), 1)
    declared = np.where(dflt > 0, dflt, np.maximum(0.1, est))
    created = par.build_date.values.astype("datetime64[D]") - rng.integers(0, 2, len(par)).astype("timedelta64[D]")
    return pd.DataFrame({"barcode": par.barcode.values, "account": par.account.values, "service": par.service.values,
                         "declared_kg": np.round(declared, 1), "fragile": np.where(par.fragile, "Y", "N"),
                         "depot_code": par.depot.values, "manifest_date": pd.to_datetime(created).strftime("%Y-%m-%d")})


def audits(w, seed):
    """The audit app: one header per audit (routine; a supervisor's check audit of some cages), one line per parcel."""
    rng = np.random.default_rng(seed + 15)
    par = w["parcels"]
    dep = w["depots"].set_index("depot_code").depot_name
    cages = w["cages"]
    aud_rows, line_rows = [], []
    auditors = {d: ["AU%03d" % int(x) for x in rng.choice(np.arange(100, 990), size=3, replace=False)]
                for d in w["depots"].depot_code}
    by_cage = {k: g for k, g in par.groupby("cage_label")}
    seq = int(rng.integers(40000, 60000))
    for c in cages.itertuples():
        g = by_cage[c.cage_label]
        old_keyer = dep[c.depot] in OLD_KEYER_DEPOTS
        a_start = dt.datetime.combine(c.build_date + dt.timedelta(days=1), dt.time(6, 0)) + \
            dt.timedelta(minutes=int(rng.integers(0, 210)))
        seq += int(rng.integers(1, 9))
        aid = "A%s%06d" % (c.depot[:2], seq)
        aud_rows.append((aid, c.cage_label, c.build_date.isoformat(), HUB_NAME[c.hub], c.depot, "ROUTINE",
                         auditors[c.depot][int(rng.integers(0, 3))], a_start.strftime("%Y-%m-%d %H:%M")))
        lines = _findings(rng, g, c.build_date, old_keyer)
        for i, (bc, st, code) in enumerate(lines):
            line_rows.append((aid, i + 1, bc, st, code))
        if rng.random() < 0.04:
            seq += int(rng.integers(1, 9))
            aid2 = "A%s%06d" % (c.depot[:2], seq)
            a2 = a_start + dt.timedelta(minutes=int(rng.integers(25, 140)))
            aud_rows.append((aid2, c.cage_label, c.build_date.isoformat(), HUB_NAME[c.hub], c.depot, "CHECK",
                             "SV%03d" % int(rng.integers(10, 99)), a2.strftime("%Y-%m-%d %H:%M")))
            for i, (bc, st, code) in enumerate(lines):
                if st == "DAMAGED" and rng.random() < 0.08:
                    st, code = "OK", ""
                elif st == "OK" and rng.random() < 0.004:
                    st, code = "DAMAGED", _code(rng, c.build_date, old_keyer)
                line_rows.append((aid2, i + 1, bc, st, code))
    a = pd.DataFrame(aud_rows, columns=["audit_id", "cage_label", "build_date", "hub", "depot_code", "audit_type",
                                        "auditor", "audit_start_local"])
    ln = pd.DataFrame(line_rows, columns=["audit_id", "line_no", "barcode", "condition", "damage_code"])
    return a, ln


def cut(w, seed):
    a, ln = audits(w, seed)
    return dict(scans=load_scans(w, seed), dws=dws(w, seed), manifests=manifests(w, seed), audits=a, lines=ln)


def _code(rng, build_date, old_keyer):
    kind = rng.choice(["crush", "tear", "open", "puncture", "wet"], p=[0.62, 0.15, 0.1, 0.08, 0.05])
    old = build_date < CODE_SWITCH or (old_keyer and rng.random() < 0.7)
    return OLD_CODES[kind] if old else NEW_CODES[kind]


def _findings(rng, g, build_date, old_keyer):
    out = []
    for r in g.itertuples():
        if rng.random() < 0.004:
            out.append((r.barcode, "NOT FOUND", ""))
        elif r.damaged:
            out.append((r.barcode, "DAMAGED", _code(rng, build_date, old_keyer)))
        else:
            out.append((r.barcode, "OK", ""))
    idx = rng.permutation(len(out))   # the auditor empties the cage onto the bench and scans parcels as they come
    return [out[i] for i in idx]


def _chutes(depots, seed):
    r = np.random.default_rng(seed + 11)
    m = {}
    for h, g in depots.groupby("hub"):
        nums = r.choice(np.arange(1, 64), size=len(g), replace=False)
        for d, k in zip(sorted(g.depot_code), nums):
            m[d] = "C%02d" % int(k)
    return m
