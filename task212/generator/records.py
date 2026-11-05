"""Cut the record systems from the clean truth. Each system writes in its own idiom (clock, units, codes)."""
import datetime as dt
import numpy as np
import pandas as pd
from world import HUBS, HEAVY_ACCOUNT, UTC_OFFSET_H

HUB_NO = {h[0]: h[1] for h in HUBS}
HUB_NAME = {h[0]: h[2] for h in HUBS}
OLD_CODES = {"crush": "D1", "tear": "D2", "wet": "D3", "open": "D4", "puncture": "D5"}
NEW_CODES = {"crush": "CR", "tear": "TR", "wet": "WT", "open": "OP", "puncture": "PU"}
CODE_SWITCH = dt.date(2026, 8, 1)


def cut(w, seed):
    rng = np.random.default_rng(seed + 10)
    par = w["parcels"].copy()
    # ---- sorter load scans (UTC), re-scans after a no-read --------------------------------------------
    scans = pd.DataFrame({
        "hub_no": par.hub.map(HUB_NO), "cage_label": par.cage_label, "barcode": par.barcode,
        "scan_utc": [t - dt.timedelta(hours=UTC_OFFSET_H) for t in par.scan_local], "event": "LOAD",
        "chute": par.depot.map(_chutes(w["depots"], seed))})
    rescan = rng.random(len(par)) < 0.015
    rs = scans[rescan].copy()
    rs["scan_utc"] = [t + dt.timedelta(seconds=int(s)) for t, s in zip(rs.scan_utc, rng.integers(3, 10, len(rs)))]
    rs["event"] = "LOAD"
    scans = pd.concat([scans, rs]).sort_values(["hub_no", "cage_label", "scan_utc", "barcode"]).reset_index(drop=True)
    scans["operator"] = ["OP%04d" % int(x) for x in rng.integers(1000, 9999, len(scans))]
    # ---- DWS (local time with offset, grams, mm), re-weighs -------------------------------------------
    induct = [t - dt.timedelta(minutes=int(m)) for t, m in zip(par.scan_local, rng.integers(2, 24, len(par)))]
    wg = np.round(par.weight_kg.values * 1000 * rng.normal(1, 0.006, len(par)) / 5) * 5
    vol = par.weight_kg.values * rng.uniform(2.5, 9.0, len(par)) * 1000  # cm3, loose density
    L = np.round(np.cbrt(vol * rng.uniform(1.3, 2.2, len(par))) * 10)
    W = np.round(np.cbrt(vol) * 10)
    H = np.maximum(15, np.round(vol * 1000 / np.maximum(L * W, 1)))
    shape = par.pack.map({"BOX": "BOX", "BAG": "BAG", "FLYER": "FLY"})
    dws = pd.DataFrame({"barcode": par.barcode, "hub_no": par.hub.map(HUB_NO),
                        "induct_local": [t.strftime("%Y-%m-%dT%H:%M:%S+02:00") for t in induct],
                        "weight_g": wg.astype(int), "length_mm": L.astype(int), "width_mm": W.astype(int),
                        "height_mm": H.astype(int), "shape": shape,
                        "scanner": ["DWS-%02d-%d" % (HUB_NO[h], 1 + int(x)) for h, x in zip(par.hub, rng.integers(0, 3, len(par)))]})
    rw = rng.random(len(par)) < 0.008
    d2 = dws[rw].copy()
    d2["weight_g"] = (np.round(d2.weight_g * rng.normal(1, 0.01, len(d2)) / 5) * 5).astype(int)
    d2["induct_local"] = [(dt.datetime.strptime(s[:19], "%Y-%m-%dT%H:%M:%S") + dt.timedelta(minutes=int(m))).strftime("%Y-%m-%dT%H:%M:%S+02:00")
                          for s, m in zip(d2.induct_local, rng.integers(1, 6, len(d2)))]
    dws = pd.concat([dws, d2]).sort_values(["hub_no", "induct_local", "barcode"]).reset_index(drop=True)
    # ---- manifests (sender declared weight, kg) --------------------------------------------------------
    acc = w["accounts"].set_index("account")
    dflt = acc.declared_default_kg.reindex(par.account).values
    est = np.round(par.weight_kg.values * rng.uniform(0.7, 1.4, len(par)), 1)
    declared = np.where(dflt > 0, dflt, np.maximum(0.1, est))
    man = pd.DataFrame({"barcode": par.barcode, "account": par.account,
                        "service": par.service, "declared_kg": np.round(declared, 1),
                        "fragile": np.where(par.fragile, "Y", "N"), "depot_code": par.depot,
                        "created": [(d - dt.timedelta(days=int(x))).isoformat() for d, x in zip(par.build_date, rng.integers(0, 2, len(par)))]})
    # ---- audits: routine headers, check audits, findings ----------------------------------------------
    cages = w["cages"].copy()
    aud_rows, line_rows = [], []
    auditors = {}
    for dep in w["depots"].depot_code:
        auditors[dep] = ["AU%03d" % int(x) for x in rng.choice(np.arange(100, 990), size=3, replace=False)]
    by_cage = par.groupby("cage_label")
    seq = int(rng.integers(40000, 60000))
    for c in cages.itertuples():
        g = by_cage.get_group(c.cage_label)
        audit_day = c.build_date + dt.timedelta(days=1)
        a_start = dt.datetime.combine(audit_day, dt.time(6, 0)) + dt.timedelta(minutes=int(rng.integers(0, 210)))
        seq += int(rng.integers(1, 9))
        aid = "A%s%06d" % (c.depot[:2], seq)
        aud = auditors[c.depot][int(rng.integers(0, 3))]
        aud_rows.append((aid, c.cage_label, c.build_date.isoformat(), HUB_NAME[c.hub], c.depot, "ROUTINE", aud,
                         a_start.strftime("%Y-%m-%d %H:%M")))
        lines = _findings(rng, g, c.build_date, c.depot)
        for i, (bc, st, code) in enumerate(lines):
            line_rows.append((aid, i + 1, bc, st, code))
        if rng.random() < 0.04:  # supervisor's check audit of the same cage
            seq += int(rng.integers(1, 9))
            aid2 = "A%s%06d" % (c.depot[:2], seq)
            a2 = a_start + dt.timedelta(minutes=int(rng.integers(25, 140)))
            aud_rows.append((aid2, c.cage_label, c.build_date.isoformat(), HUB_NAME[c.hub], c.depot, "CHECK",
                             "SV%03d" % int(rng.integers(10, 99)), a2.strftime("%Y-%m-%d %H:%M")))
            for i, (bc, st, code) in enumerate(lines):
                if st == "DAMAGED" and rng.random() < 0.08:
                    st, code = "OK", ""
                elif st == "OK" and rng.random() < 0.004:
                    st, code = "DAMAGED", _code(rng, c.build_date, c.depot)
                line_rows.append((aid2, i + 1, bc, st, code))
    audits = pd.DataFrame(aud_rows, columns=["audit_id", "cage_label", "build_date", "hub", "depot_code", "audit_type",
                                             "auditor", "audit_start_local"])
    lines = pd.DataFrame(line_rows, columns=["audit_id", "line_no", "barcode", "condition", "damage_code"])
    return dict(scans=scans, dws=dws, manifests=man, audits=audits, lines=lines)


def _code(rng, build_date, depot):
    kind = rng.choice(["crush", "tear", "open", "puncture", "wet"], p=[0.62, 0.15, 0.1, 0.08, 0.05])
    old_keyers = depot.endswith(("7", "3"))  # two depots' handhelds kept the old list after the switch
    return OLD_CODES[kind] if (build_date < CODE_SWITCH or (old_keyers and rng.random() < 0.7)) else NEW_CODES[kind]


def _findings(rng, g, build_date, depot):
    out = []
    for r in g.itertuples():
        if rng.random() < 0.004:
            out.append((r.barcode, "NOT FOUND", ""))
        elif r.damaged:
            out.append((r.barcode, "DAMAGED", _code(rng, build_date, depot)))
        else:
            out.append((r.barcode, "OK", ""))
    # the auditor empties the cage onto the bench and scans parcels as they come to hand
    idx = rng.permutation(len(out))
    return [out[i] for i in idx]


def _chutes(depots, seed):
    r = np.random.default_rng(seed + 11)
    m = {}
    for h, g in depots.groupby("hub"):
        nums = r.choice(np.arange(1, 64), size=len(g), replace=False)
        for dep, n in zip(sorted(g.depot_code), nums):
            m[dep] = "C%02d" % int(n)
    return m
