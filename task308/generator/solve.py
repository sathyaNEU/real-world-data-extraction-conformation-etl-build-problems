"""The golden, computed from the pack alone (target/ or the zip's members): every station's classic stock rebuilt in
continuous time from the 03:00 audit, every undock and dock, and every van move; each station's requests per stocked
second in each month, day type and local hour; the requests its empty seconds turned away; the pilot's e-bike share,
its new-rider uplift and the e-bike fare's premium; each network's net fare revenue; and the three supporting tables.
Variants of the construction are exposed for the checks (family, ladder)."""
import datetime as dt
import json
import math
import os
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

TZ = ZoneInfo("America/Chicago")
YEAR = 2025
NETS = ["Central", "University", "Riverside", "Old Town", "Hillcrest"]
FN = {"q1": "tripsys_export_2025Q1.csv", "q2": "tripsys_export_2025Q2.csv", "q3": "rides_2025Q3.csv",
      "q4": "rides_2025Q4.csv", "moves": "dispatch_moves_2025.csv", "audit": "audit_0300_2025.xlsx",
      "stations": "station_information.json", "regions": "system_regions.json",
      "accounts": "account_register_2025-12-31.csv", "charging": "charging_sessions_harbour_2025.csv",
      "workshop": "workshop_jobs_2025.csv", "pilot": "ebike_pilot_harbour_2025.pdf"}
T0 = int(dt.datetime(YEAR, 1, 1, tzinfo=TZ).timestamp())
T1 = int(dt.datetime(YEAR + 1, 1, 1, tzinfo=TZ).timestamp())


EPOCH = pd.Timestamp("1970-01-01", tz="UTC")


def _secs(ts):
    """tz-aware timestamps to epoch seconds, whatever the resolution pandas parsed them at"""
    return ((ts - EPOCH) // pd.Timedelta(seconds=1)).astype("int64")


def _epoch_local(s):
    """naive local timestamps to epoch seconds (fold 0 for the repeated November hour)"""
    ts = pd.to_datetime(s)
    return _secs(ts.dt.tz_localize(TZ, ambiguous=np.zeros(len(ts), bool), nonexistent="shift_forward"))


def load(src):
    p = lambda k: os.path.join(src, FN[k])
    st = json.load(open(p("stations")))["data"]["stations"]
    rg = {r["region_id"]: r["name"] for r in json.load(open(p("regions")))["data"]["regions"]}
    S = pd.DataFrame(st)
    S["network"] = S.region_id.map(rg)
    by_name = dict(zip(S.name, S.station_id)); by_code = dict(zip(S.short_name, S.station_id))
    old = pd.concat([pd.read_csv(p(q), dtype={"account_no": str}) for q in ("q1", "q2")], ignore_index=True)
    new = pd.concat([pd.read_csv(p(q), dtype={"account_id": str}) for q in ("q3", "q4")], ignore_index=True)
    a = pd.DataFrame({"t0": _epoch_local(old.start_time), "dur": old.duration_sec.astype(int),
                      "s0": old.start_station.map(by_name), "s1": old.end_station.map(by_name),
                      "ebike": old.bike_type.eq("electric"), "acct": old.account_no.map(lambda x: "L" + str(x)),
                      "bike": old.bike_no.str.replace("-", "").map(lambda x: ("EB%04d" % int(x[1:])) if x.startswith("E") else "BK%05d" % int(x[1:])),
                      "fare": old.fare_usd.astype(float)})
    b = pd.DataFrame({"t0": _epoch_local(new.started_at), "dur": new.duration_s.astype(int),
                      "s0": new.start_station_code.map(by_code), "s1": new.end_station_code.map(by_code),
                      "ebike": new.vehicle_type.eq("EBIKE"), "acct": new.account_id,
                      "bike": new.vehicle_id.map(lambda v: ("EB%04d" % (v - 500000)) if v >= 500000 else "BK%05d" % (v - 100000)),
                      "fare": new.fare_cents.astype(float) / 100.0})
    T = pd.concat([a, b], ignore_index=True)
    T["t1"] = T.t0 + T.dur
    assert T.s0.notna().all() and T.s1.notna().all()
    T["false"] = (T.dur < 60) & (T.s0 == T.s1)
    T["net"] = T.s0.map(dict(zip(S.station_id, S.network)))
    M = pd.read_csv(p("moves"), dtype={"from_station": str, "to_station": str})
    M["t"] = _secs(pd.to_datetime(M.completed_utc))
    A = pd.read_excel(p("audit"), dtype={"station_id": str})
    A["t"] = [int(dt.datetime.combine(pd.Timestamp(d).date(), dt.time(3, 0), tzinfo=TZ).timestamp()) for d in A.audit_date]
    return S, T, M, A


def rebuild(S, T, M, A):
    """stocked and empty seconds, and real undocks, per station and UTC hour of the year (classic bikes)"""
    hours = np.arange(T0, T1 + 3600, 3600); NH = len(hours) - 1
    out = {}
    cl = T[~T.ebike]; mv = M[M.bike_class == "classic"]
    for sid in S.station_id:
        dep = cl[cl.s0 == sid]; arr = cl[cl.s1 == sid]
        vo = mv[mv.from_station == sid]; vi = mv[mv.to_station == sid]
        t = np.concatenate([dep.t0.values, arr.t1.values, vo.t.values, vi.t.values])
        d = np.concatenate([-np.ones(len(dep)), np.ones(len(arr)), -vo.qty.values, vi.qty.values]).astype(float)
        pr = np.concatenate([np.zeros(len(dep)), np.ones(len(arr) + len(vo) + len(vi))])
        o = np.lexsort((pr, t)); t, d = t[o], d[o]
        c = A[A.station_id == sid].sort_values("t"); ct = c.t.values; cv = c.classic_docked.values
        Sx = np.zeros(NH); Ex = np.zeros(NH)
        for j in range(len(ct)):
            a0 = ct[j]; a1 = ct[j + 1] if j + 1 < len(ct) else T1
            lo, hi = np.searchsorted(t, a0, "right"), np.searchsorted(t, a1, "right")
            tt = np.concatenate([[a0], t[lo:hi], [a1]]); ss = cv[j] + np.concatenate([[0], np.cumsum(d[lo:hi])])
            assert ss.min() >= 0, (sid, j)
            hb = hours[(hours > a0) & (hours < a1)]; edges = np.union1d(tt, hb)
            stk = ss[np.searchsorted(tt, edges[:-1], "right") - 1]; du = np.diff(edges)
            hi_ = ((edges[:-1] - T0) // 3600).astype(int)
            Sx += np.bincount(hi_, weights=du * (stk > 0), minlength=NH); Ex += np.bincount(hi_, weights=du * (stk == 0), minlength=NH)
        real = dep[~dep["false"]]
        Dx = np.bincount(((real.t0.values - T0) // 3600).astype(int), minlength=NH)[:NH].astype(float)
        Dx[: (ct[0] - T0) // 3600] = 0
        out[sid] = (Sx, Ex, Dx)
    return hours[:-1], out


def calendar_keys(hours):
    loc = [dt.datetime.fromtimestamp(int(h), TZ) for h in hours]
    H = np.array([x.hour for x in loc]); Mo = np.array([x.month for x in loc]) - 1
    Wk = np.array([int(x.weekday() >= 5) for x in loc]); Dw = np.array([x.weekday() for x in loc])
    return H, Mo, Wk, Dw


def turned_away(S, rb, key, pool=None):
    """requests turned away at each station: lambda (undocks per stocked second) in each cell of key, times the
    station's empty seconds in it; pool maps a station to the stations whose seconds are pooled"""
    U = {}
    for sid in S.station_id:
        grp = pool[sid] if pool else [sid]
        s = np.bincount(key, weights=sum(rb[g][0] for g in grp)); d = np.bincount(key, weights=sum(rb[g][2] for g in grp))
        lam = np.divide(d, s, out=np.zeros_like(d), where=s > 0)
        U[sid] = float((lam[key] * rb[sid][1]).sum())
    return U


def pilot(S, T, src):
    """the pilot's stations from its note, its e-bike share, its new-rider uplift and the e-bike fare's premium"""
    from pypdf import PdfReader
    txt = "\n".join(pg.extract_text() for pg in PdfReader(os.path.join(src, FN["pilot"])).pages)
    import re
    pil, cmpn = [], []
    lines = [ln.strip() for ln in txt.splitlines()]
    for j, ln in enumerate(lines):
        if re.fullmatch(r"HBR-\d\d", ln) and j + 2 < len(lines) and lines[j + 2] in ("pilot station", "comparison station"):
            (pil if lines[j + 2] == "pilot station" else cmpn).append(ln)
    assert len(pil) == 24 and len(cmpn) == 12, (len(pil), len(cmpn))
    code2id = dict(zip(S.short_name, S.station_id))
    pil = [code2id[c] for c in pil]; cmpn = [code2id[c] for c in cmpn]
    R = T[~T["false"]]
    rp = R[R.s0.isin(pil)]; rc = R[R.s0.isin(cmpn)]
    X = rp.ebike.mean()
    i = (len(rp) / len(pil)) / (len(rc) / len(cmpn)) - 1
    f_e = rp[rp.ebike].fare.mean(); f_cp = rp[~rp.ebike].fare.mean()
    return {"pilot": pil, "comparison": cmpn, "X": float(X), "i": float(i), "f_e": float(f_e), "f_c_pilot": float(f_cp),
            "delta": float(f_e - f_cp), "rides_pilot": int(len(rp)), "rides_comparison": int(len(rc)),
            "ebike_rides_pilot": int(rp.ebike.sum())}


def net_revenue(S, T, U, pl, induced_on="requests"):
    R = T[~T["false"]]
    out = {}
    for n in NETS:
        ids = set(S.station_id[S.network == n])
        cl = R[(~R.ebike) & R.s0.isin(ids)]
        Sd = len(cl); fc = cl.fare.mean(); Ud = sum(U[s] for s in ids)
        Rq = Sd + Ud
        base = Rq if induced_on == "requests" else Sd
        g = (Ud + pl["i"] * base) * fc + pl["X"] * Rq * (1 + pl["i"]) * pl["delta"]
        out[n] = {"rides": int(Sd), "fare_classic": float(fc), "turned_away": Ud, "requests": Rq, "net": float(g),
                  "default": float(Sd * ((1 + pl["i"]) * (pl["X"] * pl["f_e"] + (1 - pl["X"]) * pl["f_c_pilot"]) - pl["f_c_pilot"]))}
    return out


def r25(x):
    return int(25000 * math.floor(x / 25000 + 0.5))


# ---------------------------------------------------------------------------------------------------- the asks
AREAS = {"central": "Central", "university": "University", "riverside": "Riverside", "old town": "Old Town",
         "hillcrest": "Hillcrest", "harbour": "Harbour", "outside brackenford": "Outside"}


def people(src, T, rule="golden"):
    """people who rode in 2025 by home area. rule: 'accounts' (one per account), 'cards' (one per payment card),
    'golden' (accounts on one card are one person when one was opened after the other's last ride)"""
    A = pd.read_csv(os.path.join(src, FN["accounts"]), dtype={"legacy_account_no": str, "account_id": str})
    A["home"] = A.home_area.str.strip().str.lower().map(AREAS)
    leg = dict(zip("L" + A.legacy_account_no.dropna(), A.account_id[A.legacy_account_no.notna()]))
    R = T[~T["false"]].copy()
    R["aid"] = R.acct.map(lambda x: leg.get(x, x) if x.startswith("L") else x)
    last = R.groupby("aid").t1.max()
    act = A[A.account_id.isin(last.index)].copy()
    act["created"] = _epoch_local(act.created_at).values
    act["last"] = act.account_id.map(last)
    if rule == "accounts":
        return act.groupby("home").size().to_dict(), act
    if rule == "cards":
        return act.groupby("card_fingerprint").home.last().value_counts().to_dict(), act
    persons = 0
    counts = {}
    for card, g in act.groupby("card_fingerprint"):
        g = g.sort_values("created")
        groups = []
        for r in g.itertuples():
            for grp in groups:
                if grp["last"] < r.created:
                    grp["last"] = max(grp["last"], r.last); grp["home"] = r.home
                    break
            else:
                groups.append({"last": r.last, "home": r.home})
        for grp in groups:
            counts[grp["home"]] = counts.get(grp["home"], 0) + 1
    return counts, act


def charging(src, rule="golden"):
    C = pd.read_csv(os.path.join(src, FN["charging"])).sort_values("session_id")
    C["out"] = pd.to_datetime(C.plug_out_utc).dt.tz_convert(TZ)
    C["month"] = C.out.dt.month
    if rule == "all":
        keep = C
    elif rule == "monotone":
        keep = []
        for (s, p), g in C.groupby(["station_code", "point"]):
            g = g.sort_values("plug_in_utc"); hi = -1
            for r in g.itertuples():
                if r.meter_start_wh >= hi:
                    keep.append(r.Index); hi = r.meter_stop_wh
        keep = C.loc[keep]
    else:
        keep = C[~C.duplicated(["station_code", "point", "meter_start_wh", "meter_stop_wh"], keep="first") |
                 (C.meter_start_wh == C.meter_stop_wh)]
    return {m: float(keep[keep.month == m].energy_kwh.sum()) for m in range(1, 13)}


def workshop(src, T, rule="golden"):
    J = pd.read_csv(os.path.join(src, FN["workshop"]))
    J["op"] = _secs(pd.to_datetime(J.opened_utc))
    J["cl"] = _secs(pd.to_datetime(J.closed_utc))
    J["q"] = (pd.to_datetime(J.opened_utc).dt.tz_convert(TZ).dt.month - 1) // 3 + 1
    J["typ"] = np.where(J.asset_class == "E-bike", "ebike", "classic")
    R = T[~T["false"]]
    rides = {b: np.sort(g.t0.values) for b, g in R.groupby("bike")}
    J = J.sort_values(["op", "job_no"])
    keep = []
    last = {}
    for r in J.itertuples():
        prev = last.get(r.asset_tag)
        ok = True
        if rule == "golden" and prev is not None:
            ts = rides.get(r.asset_tag, np.array([]))
            ok = (np.searchsorted(ts, r.op) - np.searchsorted(ts, prev[1], "right")) > 0
        elif rule == "window30" and prev is not None:
            ok = not (prev[2] == r.fault_code and r.op - prev[0] < 30 * 86400)
        if ok:
            keep.append(r.Index); last[r.asset_tag] = (r.op, r.cl, r.fault_code)
        else:
            last[r.asset_tag] = (prev[0], r.cl, r.fault_code)
    K = J.loc[keep] if rule != "all" else J
    R2 = R.assign(q=((pd.to_datetime(R.t0, unit="s", utc=True).dt.tz_convert(TZ).dt.month - 1) // 3 + 1).values)
    out = {}
    for typ in ("ebike", "classic"):
        for q in range(1, 5):
            n_r = int(((R2.ebike == (typ == "ebike")) & (R2.q == q)).sum())
            n_j = int(((K.typ == typ) & (K.q == q)).sum())
            out[(typ, q)] = (n_j, n_r, 1e4 * n_j / n_r)
    return out


def solve(src):
    S, T, M, A = load(src)
    hours, rb = rebuild(S, T, M, A)
    H, Mo, Wk, Dw = calendar_keys(hours)
    U = turned_away(S, rb, Mo * 48 + Wk * 24 + H)
    pl = pilot(S, T, src)
    nr = net_revenue(S, T, U, pl)
    ppl, _ = people(src, T)
    en = charging(src)
    ws = workshop(src, T)
    best = max(NETS, key=lambda n: nr[n]["net"])
    return {"S": S, "T": T, "rb": rb, "keys": (H, Mo, Wk, Dw), "U": U, "pilot": pl, "net": nr, "best": best,
            "people": ppl, "energy": en, "workshop": ws}


if __name__ == "__main__":
    import sys
    import time
    t = time.time()
    G = solve(sys.argv[1])
    pl = G["pilot"]
    print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in pl.items() if k not in ("pilot", "comparison")})
    for n in NETS:
        x = G["net"][n]
        print(f"{n:10s} rides {x['rides']:7d} turned away {x['turned_away']:8.0f} net {x['net']:9.0f} -> {r25(x['net']):7d}  default {x['default']:8.0f}")
    print("call", G["best"])
    print("people", {n: G["people"].get(n) for n in NETS})
    print("energy kWh", {m: round(v) for m, v in G["energy"].items()})
    print("workshop per 10,000", {f"{t}Q{q}": round(v[2], 1) for (t, q), v in G["workshop"].items()})
    print("seconds", round(time.time() - t, 1))
