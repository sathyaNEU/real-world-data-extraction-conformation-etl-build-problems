"""Every rung, the golden and every ask figure, computed from target/ alone (no import of world.py)."""
import base64
import csv
import datetime as dt
import os
import re
import zlib
from collections import defaultdict

import numpy as np
import openpyxl

CP = 1.163
D = dt.date


# ------------------------------------------------------------------------------------------------- readers
def find(target, prefix):
    for fn in sorted(os.listdir(target)):
        if fn.startswith(prefix):
            return os.path.join(target, fn)
    raise FileNotFoundError(prefix)


def pdf_text(path):
    raw = open(path, "rb").read()
    out, pos = [], 0
    while True:
        i = raw.find(b"stream", pos)
        if i < 0:
            break
        j = raw.find(b"endstream", i)
        head = raw[max(0, i - 160):i]
        body = raw[i + 6:j].strip(b"\r\n")
        pos = j + 9
        if b"ASCII85Decode" in head:
            body = base64.a85decode(body[:-2] if body.endswith(b"~>") else body)
        if b"FlateDecode" in head:
            try:
                body = zlib.decompress(body)
            except zlib.error:
                continue
        out += [m.decode("latin-1") for m in re.findall(rb"\(((?:[^()\\]|\\.)*)\)\s*Tj", body)]
    return " ".join(s.replace("\\(", "(").replace("\\)", ")") for s in out)


def read_csv(path, delim=","):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=delim))


def fnum(s):
    if s is None or s == "":
        return None
    return float(s.replace(",", "."))


def load(target):
    T = {}
    T["weather"] = read_csv(find(target, "weerstation_"))
    T["amr"] = read_csv(find(target, "amr_warmtemeters_"))
    wb = openpyxl.load_workbook(find(target, "aansluitregister_"))
    T["conns"] = [dict(zip([c.value for c in wb["Aansluitingen"][1]], r)) for r in
                  wb["Aansluitingen"].iter_rows(min_row=2, values_only=True)]
    T["meters"] = [dict(zip([c.value for c in wb["Meters"][1]], r)) for r in
                   wb["Meters"].iter_rows(min_row=2, values_only=True)]
    wb = openpyxl.load_workbook(find(target, "weidehaven_aardgasvrij_fasering"))
    ws = wb["Fasering"]
    head = [c.value for c in ws[4]]
    T["schedule"] = [dict(zip(head, r)) for r in ws.iter_rows(min_row=5, values_only=True) if r[0] is not None]
    wb = openpyxl.load_workbook(find(target, "warmteverliesberekening_weidehaven_rev2"))
    ws = wb["Resultaten"]
    head = [c.value for c in ws[4]]
    T["rev2"] = [dict(zip(head, r)) for r in ws.iter_rows(min_row=5, values_only=True) if r[0] is not None]
    T["hydraulic"] = pdf_text(find(target, "hydraulische_toets"))
    T["concept"] = pdf_text(find(target, "warmteverliesberekening_weidehaven_concept"))
    T["gasreads"] = read_csv(find(target, "gas_telemetrie_"), ";")
    wb = openpyxl.load_workbook(find(target, "meterstamgegevens_gas"))
    T["gas_conn"] = [dict(zip([c.value for c in wb["Aansluitingen"][1]], r)) for r in
                     wb["Aansluitingen"].iter_rows(min_row=2, values_only=True)]
    T["gas_meters"] = [dict(zip([c.value for c in wb["Meters"][1]], r)) for r in
                       wb["Meters"].iter_rows(min_row=2, values_only=True)]
    T["legacy"] = read_csv(find(target, "driveby_opnames_"), ";")
    return T


def asdate(x):
    if isinstance(x, dt.datetime):
        return x.date()
    return x


# ------------------------------------------------------------------------------------------------- the main call
def serial_owner(T):
    """meter serial -> (aansluitnummer, geplaatst, verwijderd)"""
    own = defaultdict(list)
    for m in T["meters"]:
        own[str(m["meternummer"])].append((m["aansluitnummer"], asdate(m["geplaatst"]), asdate(m["verwijderd"])))
    return own


def tg_by_day(T):
    return {dt.datetime.strptime(r["YYYYMMDD"], "%Y%m%d").date(): int(r["TG"]) / 10.0 for r in T["weather"]}


def per_connection(T, win=0.0, shift=0):
    """Per connection on days with TG <= win: list of daily drops (supply - return), energy and volume sums."""
    tg = tg_by_day(T)
    own = serial_owner(T)
    per = defaultdict(lambda: {"dt": [], "tr": [], "ts": [], "E": 0.0, "V": 0.0, "days": []})
    for r in T["amr"]:
        d = D.fromisoformat(r["datum_utc"])
        dd = d + dt.timedelta(days=shift)
        if dd not in tg or tg[dd] > win:
            continue
        cands = own[r["meternummer"]]
        nr = None
        for a, g, v in cands:
            if g <= d and (v is None or d <= v):
                nr = a
        p = per[nr]
        ts, tr = fnum(r["t_aanvoer_gem_c"]), fnum(r["t_retour_gem_c"])
        if ts is not None and tr is not None:
            p["dt"].append(ts - tr)
            p["tr"].append(tr)
            p["ts"].append(ts)
            p["days"].append(d)
        e, v = fnum(r["energie_kwh"]), fnum(r["volume_m3"])
        if e is not None and v is not None:
            p["E"] += e
            p["V"] += v
    return per


def like_installations(T):
    """The connections in the high-return regime: cold-day mean returns split at the widest gap of the sorted
    distribution; the like installations are the side above it."""
    per = per_connection(T)
    mr = sorted((float(np.mean(p["tr"])), nr) for nr, p in per.items())
    gaps = [(mr[i + 1][0] - mr[i][0], i) for i in range(len(mr) - 1)]
    g, i = max(gaps)
    like = [nr for _, nr in mr[i + 1:]]
    return like, (mr[i][0], mr[i + 1][0]), mr


def pooled(per, ids, kw, how, route="T", supply=None, station=None):
    ps = [per[i] for i in ids if i in per]
    if route == "T":
        if supply == "station":
            ds = np.array([np.mean([station[d] - tr for d, tr in zip(p["days"], p["tr"])]) for p in ps])
        else:
            ds = np.array([np.mean(p["dt"]) for p in ps])
    else:
        ds = np.array([p["E"] / (CP * p["V"]) for p in ps])
    q = np.array([kw[i] for i in ids if i in per])
    if how == "mean":
        return float(ds.mean())
    if how == "median":
        return float(np.median(ds))
    if how == "harm":
        return float(q.sum() / (q / ds).sum())
    if how == "flow":
        return float(sum(p["E"] for p in ps) / (CP * sum(p["V"] for p in ps)))
    raise ValueError(how)


def station_supply_daily(target):
    """Daily mean station supply (UTC days) from the SCADA hours."""
    rows = read_csv(find(target, "os_west_scada_"), ";")
    acc = defaultdict(list)
    for r in rows:
        acc[D.fromisoformat(r["tijdstip_utc"][:10])].append(float(r["t_aanvoer_c"]))
    return {d: float(np.mean(v)) for d, v in acc.items()}


def loads(T):
    """Rev2 design heat load per Weidehaven complex, joined to the schedule's phases."""
    rev = {str(r["complex"]).replace("WH", ""): int(r["ontwerpwarmteverlies_kw"]) for r in T["rev2"]}
    out = []
    for s in T["schedule"]:
        code = str(int(s["complexnr"]))
        out.append({"code": code, "phase": int(s["fase"]), "load": rev[code], "date": asdate(s["aansluiten_gepland"]),
                    "ean": str(s["gas_ean"]), "street": s["complex"].rsplit(" ", 1)[0], "complex": s["complex"]})
    return out


def concept_loads(T):
    txt = T["concept"]
    out = {}
    for m in re.finditer(r"(\d{4}) (\d{2,3}) (\d{3,4})", txt):
        out[m.group(1)] = int(m.group(3))
    return out


def available(T):
    m = re.search(r"=\s*(\d+)\s*m\s*3?\s*/h", T["hydraulic"])
    return int(m.group(1))


def season_call(KA, KAB, d, H):
    f3, f6 = KA / (CP * d), KAB / (CP * d)
    if f3 > H:
        return "2027-28", f3, f6
    if f6 > H:
        return "2028-29", f3, f6
    return "none", f3, f6


def main_call(target, T=None):
    T = T or load(target)
    kw = {c["aansluitnummer"]: int(c["gecontracteerd_vermogen_kw"]) for c in T["conns"]}
    by = {c["aansluitnummer"]: int(c["bouwjaar"]) for c in T["conns"]}
    cat = {c["aansluitnummer"]: c["categorie"] for c in T["conns"]}
    allids = list(kw)
    like, gap, mr = like_installations(T)
    L = loads(T)
    H = available(T)
    KA = sum(b["load"] for b in L if b["phase"] <= 3)
    KAB = sum(b["load"] for b in L)
    phase_load = {ph: sum(b["load"] for b in L if b["phase"] == ph) for ph in range(1, 7)}
    st_sup = station_supply_daily(target)
    fam = {}
    for win in (0.0, -1.0, 1.0, -2.0, 2.0):
        per = per_connection(T, win)
        for how in ("mean", "median", "harm", "flow"):
            fam[("T", how, win)] = pooled(per, like, kw, how)
    per0 = per_connection(T, 0.0)
    for how in ("mean", "median", "harm"):
        fam[("E", how, 0.0)] = pooled(per0, like, kw, how, route="E")
    wide = {}
    for how in ("mean", "median", "harm"):
        wide[("stn", how)] = pooled(per0, like, kw, how, supply="station", station=st_sup)
    perS = per_connection(T, 99.0)
    for how in ("mean", "median", "harm", "flow"):
        wide[("season", how)] = pooled(perS, like, kw, how)
    perm1 = per_connection(T, 0.0, shift=-1)
    wide[("shift", "mean")] = pooled(perm1, like, kw, "mean")
    pre = {}
    sels = {"PRE": [i for i in allids if by[i] < 1985],
            "PRE_RES": [i for i in allids if by[i] < 1985 and cat[i] == "Woningen"],
            "ERA": [i for i in allids if 1955 <= by[i] <= 1975],
            "BLOCKYEARS": [i for i in allids if 1962 <= by[i] <= 1971]}
    for k, ids in sels.items():
        for how in ("mean", "median", "harm", "flow"):
            pre[(k, how)] = pooled(per0, ids, kw, how)
    xs = np.array([by[i] for i in sels["PRE"]])
    ys = np.array([np.mean(per0[i]["dt"]) for i in sels["PRE"]])
    b1, b0 = np.polyfit(xs, ys, 1)
    pre[("REG", "1962-1971")] = float(np.mean([b0 + b1 * y for y in range(1962, 1972)]))
    net = {}
    for k, ids in {"ALL": allids, "RES": [i for i in allids if cat[i] == "Woningen"]}.items():
        for how in ("mean", "median", "harm", "flow"):
            net[(k, how)] = pooled(per0, ids, kw, how)
    golden_d = fam[("T", "mean", 0.0)]
    call, f3, f6 = season_call(KA, KAB, golden_d, H)
    rungs = {"r0_design": 40.0, "r1_network": net[("ALL", "flow")], "r2_pre_lo": min(pre.values()),
             "r2_pre_hi": max(pre.values()), "side_textbook": 20.0}
    con = concept_loads(T)
    KA_c = sum(con[b["code"]] for b in L if b["phase"] <= 3)
    KAB_c = sum(con[b["code"]] for b in L)
    return {"T": T, "like": like, "gap": gap, "returns": mr, "H": H, "KA": KA, "KAB": KAB, "phase_load": phase_load,
            "fam": fam, "wide": wide, "pre": pre, "net": net, "golden_d": golden_d, "call": call, "f3": f3, "f6": f6,
            "rungs": rungs, "loads": L, "KA_concept": KA_c, "KAB_concept": KAB_c, "kw": kw, "cat": cat, "by": by}


# ------------------------------------------------------------------------------------------------- ask 1: gas by phase
def gas_by_phase(T, L):
    """Gas each phase's boiler rooms used between the reads at 06:00 local on 1 October 2025 and 1 October 2026:
    every EAN that served the boiler room (old EANs found through the master data's description), every meter on each
    EAN, each meter's consumption from its first register in the year (the 1 October read or its placement reading)
    to its last (the 1 October read or its removal reading)."""
    desc = {}
    for g in T["gas_conn"]:
        desc.setdefault(g["omschrijving"], []).append(str(g["ean"]))
    ean_desc = {str(g["ean"]): g["omschrijving"] for g in T["gas_conn"]}
    meters = defaultdict(list)
    for m in T["gas_meters"]:
        meters[str(m["ean"])].append(m)
    reads = defaultdict(list)
    seen = set()
    for r in T["gasreads"]:
        key = (r["ean"], r["meternummer"], r["tijdstip"], r["meterstand_m3"], r["soort"])
        if key in seen:
            continue
        seen.add(key)
        reads[(r["ean"], r["meternummer"])].append((r["tijdstip"][:16], int(r["meterstand_m3"]), r["soort"]))
    start, end = "2025-10-01T06:00", "2026-10-01T06:00"
    out = {}
    per_block = {}
    for b in L:
        eans = desc[ean_desc[b["ean"]]]
        tot = 0
        for ean in eans:
            for m in meters[ean]:
                ser = str(m["meternummer"])
                rs = sorted(reads.get((ean, ser), []))
                rs = [x for x in rs if start <= x[0] <= end]
                if m["geplaatst"] and asdate(m["geplaatst"]) > D(2025, 10, 1) and m["beginstand_m3"] is not None:
                    first = int(m["beginstand_m3"])
                else:
                    first = rs[0][1]
                if m["verwijderd"] and asdate(m["verwijderd"]) < D(2026, 10, 1) and m["eindstand_m3"] is not None:
                    last = int(m["eindstand_m3"])
                else:
                    last = rs[-1][1]
                tot += last - first
        per_block[b["code"]] = tot
    for ph in range(1, 7):
        out[ph] = sum(per_block[b["code"]] for b in L if b["phase"] == ph)
    return out, per_block


# ------------------------------------------------------------------------------------------------- ask 2: heat by category
def heat_by_category(T):
    """Heat taken in the 2024-25 gas year (from the drive-by annual or connection read to the AMR opening register on
    1 October 2025, bridging each meter's summer 2025 migration) and in 2025-26 (AMR registers), by category."""
    cat = {c["aansluitnummer"]: c["categorie"] for c in T["conns"]}
    leg = defaultdict(list)
    for r in T["legacy"]:
        d = dt.datetime.strptime(r["opnamedatum"], "%d-%m-%Y").date()
        f = 277.7778 if r["eenheid"] == "GJ" else 1000.0
        leg[r["meternummer"]].append((d, fnum(r["stand"]) * f, r["soort"]))
    amr = defaultdict(list)
    for r in T["amr"]:
        amr[r["meternummer"]].append(r)
    for k in amr:
        amr[k].sort(key=lambda r: r["datum_utc"])
    by_conn = defaultdict(list)
    for m in T["meters"]:
        by_conn[m["aansluitnummer"]].append(m)
    y1, y2 = defaultdict(float), defaultdict(float)
    for nr, ms in by_conn.items():
        ms = sorted(ms, key=lambda m: asdate(m["geplaatst"]))
        # 2024-25
        first_meter = [m for m in ms if m["uitlezing"] != "AMR" or str(m["uitlezing"]).startswith("AMR (module")][0]
        ser0 = str(first_meter["meternummer"])
        lr = sorted(leg[ser0])
        start = [x for x in lr if x[2] in ("J", "A")][0][1]
        amr_meters = [m for m in ms if str(m["uitlezing"]).startswith("AMR")]
        m_amr = amr_meters[0]
        rows = amr[str(m_amr["meternummer"])]
        opening = float(rows[0]["telwerk_energie_kwh"]) - float(rows[0]["energie_kwh"])
        if first_meter["uitlezing"] == "drive-by":
            eind = [x for x in lr if x[2] == "W"][0][1]
            g = (eind - start) + (opening - float(m_amr["stand_bij_plaatsing_kwh"]))
        else:
            g = opening - start
        y1[cat[nr]] += g
        # 2025-26: every AMR meter's register from its opening (or placement) to its last register
        tot = 0.0
        for m in amr_meters:
            rs = amr[str(m["meternummer"])]
            op = float(rs[0]["telwerk_energie_kwh"]) - float(rs[0]["energie_kwh"])
            tot += float(rs[-1]["telwerk_energie_kwh"]) - op
        y2[cat[nr]] += tot
    return {k: v / 1000.0 for k, v in y1.items()}, {k: v / 1000.0 for k, v in y2.items()}


def rnd(x, unit):
    from decimal import Decimal, ROUND_HALF_UP
    q = Decimal(repr(float(x))) / Decimal(unit)
    return int(q.quantize(Decimal(1), rounding=ROUND_HALF_UP)) * unit


def figures(target):
    M = main_call(target)
    T = M["T"]
    gas, gas_block = gas_by_phase(T, M["loads"])
    h1, h2 = heat_by_category(T)
    H, d = M["H"], M["golden_d"]
    ph_flow = {ph: M["phase_load"][ph] / (CP * d) for ph in range(1, 7)}
    F = {
        "call": M["call"],
        "available_m3h": H,
        "drop_K": round(d, 1),
        "drop_K_rounded": rnd(d, 1),
        "KA_kW": M["KA"], "KAB_kW": M["KAB"],
        "flow_2027_28": rnd(M["f3"], 10), "flow_2028_29": rnd(M["f6"], 10),
        "shortfall_2028_29": rnd(M["f6"] - H, 10),
        "headroom_2027_28": rnd(H - M["f3"], 10),
        "flow_2027_28_exact": round(M["f3"], 1), "flow_2028_29_exact": round(M["f6"], 1),
        "phase_flow": {str(ph): rnd(v, 5) for ph, v in ph_flow.items()},
        "phase_flow_exact": {str(ph): round(v, 1) for ph, v in ph_flow.items()},
        "phase_load_kW": {str(ph): M["phase_load"][ph] for ph in range(1, 7)},
        "gas_m3": {str(ph): rnd(v, 1000) for ph, v in gas.items()},
        "gas_m3_exact": {str(ph): v for ph, v in gas.items()},
        "heat_2425_MWh": {"Woningen": rnd(h1["Woningen"], 1000), "Utiliteit": rnd(h1["Utiliteit"], 100)},
        "heat_2526_MWh": {"Woningen": rnd(h2["Woningen"], 1000), "Utiliteit": rnd(h2["Utiliteit"], 100)},
        "heat_change_MWh": {"Woningen": rnd(h2["Woningen"] - h1["Woningen"], 1000),
                            "Utiliteit": rnd(h2["Utiliteit"] - h1["Utiliteit"], 100)},
        "heat_exact": {"2425": {k: round(v, 1) for k, v in h1.items()}, "2526": {k: round(v, 1) for k, v in h2.items()}},
        "like_n": len(M["like"]),
        "return_gap_C": [round(M["gap"][0], 1), round(M["gap"][1], 1)],
        "rung_drops": {k: round(v, 1) for k, v in M["rungs"].items()},
        "cold_days": sum(1 for t in tg_by_day(T).values() if t <= 0.0),
        "capacity_m3h": None,
    }
    m = re.search(r"design-day flow is ([\d,]+) m", T["hydraulic"])
    F["capacity_m3h"] = int(m.group(1).replace(",", "")) if m else None
    return F, M, gas_block


if __name__ == "__main__":
    import json
    import sys
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                             "target")
    F, M, gb = figures(tgt)
    print(json.dumps(F, indent=1))
    print("like", len(M["like"]), "gap", M["gap"])
    for k in ("fam", "wide", "pre", "net"):
        v = M[k]
        print(k, round(min(v.values()), 3), round(max(v.values()), 3))
