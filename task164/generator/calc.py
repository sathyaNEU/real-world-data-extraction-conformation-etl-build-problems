"""The analysis from the shipped files alone: the golden at-risk counts and allocation, every rung of the ladder, and
both asks. Reads only <target>; deliver.py, checks.py and cracker.py build on it.

    python3 calc.py [target]"""
from __future__ import annotations

import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(os.path.dirname(HERE), "target")
NAMES = ["Foothill", "Railyard", "Canal", "Mission", "West Bluff", "Crestview", "Lakeside", "Sunrise", "Sandhill",
         "Kingsley", "Highland", "Brookside"]
PILOT = ["Railyard", "Canal", "Brookside"]
TOTAL = 400
THRESH = 1.2
PF = 0.95
REC = pd.Timestamp("2027-03-31")
SIZE_GROUP = {10.0: "S", 15.0: "S", 25.0: "M", 37.5: "M"}
MIN_CELL = 40


def sg_of(k):
    return SIZE_GROUP.get(float(k), "L")


# ------------------------------------------------------------------------------------------------- loading
class Pack:
    def __init__(self, target=TARGET):
        p = lambda f: os.path.join(target, f)
        self.target = target
        self.gis = pd.read_csv(p("gis_service_transformers.csv"), dtype={"unit_installed": str})
        self.gis["loc"] = self.gis["xfmr_loc_id"].str[1:].astype(int)
        codes = pd.read_csv(p("district_codes.csv"))
        code2name = dict(zip(codes["district_code"], codes["district"]))
        t24 = pd.read_csv(p("tlm_summer_peaks_2024.csv"), dtype={"LOC_NO": str})
        t24 = pd.DataFrame({"loc": t24["LOC_NO"].astype(int), "pk": t24["PEAK_KVA"],
                            "date": pd.to_datetime(t24["PEAK_DT"], format="%m/%d/%Y")})
        self.tlm = {2024: t24}
        for y in (2025, 2026):
            t = pd.read_csv(p("tlm_summer_peaks_%d.csv" % y))
            self.tlm[y] = pd.DataFrame({"loc": t["xfmr_loc_id"], "pk": t["peak_kva"], "date": pd.to_datetime(t["peak_date"]),
                                        "district": t["district_code"].map(code2name), "kva": t["kva_rating"],
                                        "sp": t["service_points"]})
        self.sp = pd.read_csv(p("service_points.csv"), dtype={"zip": str, "account_start": str})
        self.sp["loc"] = self.sp["xfmr_loc_id"].str[1:].astype(int)
        self.rate = pd.read_csv(p("rate_schedule_changes.csv"), parse_dates=["request_date", "effective_date"])
        self.dmv = pd.read_csv(p("dmv_pev_notifications.csv"), dtype={"matched_sp_id": str, "reg_zip": str,
                                                                        "status_date": str})
        self.chg = pd.read_csv(p("gis_unit_changes_2024-2027.csv"), dtype={"wo_number": str})
        self.oms = pd.read_csv(p("oms_transformer_outages_summer2026.csv"))
        self.wo = pd.read_excel(p("ptr_pilot_work_orders.xlsx"))
        self.cost = pd.read_csv(p("ptr_pilot_cost_lines.csv"), dtype={"wo_number": str, "amount_usd": str})
        self.lsp = pd.read_csv(p("ev_load_study_2026_participants.csv"))
        self._lsi = None

    @property
    def lsi(self):
        if self._lsi is None:
            self._lsi = pd.read_parquet(os.path.join(self.target, "ev_load_study_2026_intervals.parquet"))
        return self._lsi


# ------------------------------------------------------------------------------------------------- the panel
class Panel:
    """Every transformer's vehicles at each summer's peak and at the record date, by rate."""

    def __init__(self, P, use_unmatched=None):
        g = P.gis.set_index("loc")
        self.P = P
        self.locs = g.index.values
        self.district = g["district"]
        self.kva = g["kva_rating"].astype(float)
        self.sg = self.kva.map(sg_of)
        self.pk = {y: P.tlm[y].set_index("loc")["pk"].reindex(self.locs) for y in (2024, 2025, 2026)}
        self.pkd = {y: P.tlm[y].set_index("loc")["date"].reindex(self.locs) for y in (2024, 2025, 2026)}
        sp_loc = dict(zip(P.sp["sp_id"].astype(str), P.sp["loc"]))
        d = P.dmv.copy()
        d = d[d["matched_sp_id"].notna() & (d["matched_sp_id"] != "")]
        if use_unmatched is not None:
            d = pd.concat([d, use_unmatched], ignore_index=True)
        d["loc"] = d["matched_sp_id"].map(sp_loc)
        d = d[d["loc"].notna()].copy()
        d["loc"] = d["loc"].astype(int)
        d["start"] = pd.to_datetime(d["reg_start_date"])
        d["end"] = pd.to_datetime(d["status_date"].where(d["reg_status"] != "CURRENT"))
        self.v = d
        # each service point's base schedule and its move to R-EV2
        ev = P.rate[P.rate["to_schedule"] == "R-EV2"].groupby("sp_id")["effective_date"].min()
        self.ev_from = ev
        self.flat = set(P.sp.loc[P.sp["rate_schedule"] == "R-1", "sp_id"].astype(str))

    def state(self, dates):
        """(non-EV-rate count, EV-rate count) per transformer at a per-transformer date (Series on locs)."""
        v = self.v
        day = v["loc"].map(dates)
        pres = (v["start"] <= day) & (v["end"].isna() | (v["end"] > day))
        evd = v["matched_sp_id"].astype(np.int64).map(self.ev_from)
        on_ev = evd.notna() & (evd <= day)
        k = v[pres & ~on_ev].groupby("loc").size().reindex(self.locs).fillna(0).astype(int)
        e = v[pres & on_ev].groupby("loc").size().reindex(self.locs).fillna(0).astype(int)
        return k, e

    def build(self):
        self.k, self.e = {}, {}
        for y in (2024, 2025, 2026):
            self.k[y], self.e[y] = self.state(self.pkd[y])
        rec = pd.Series(REC, index=self.locs)
        self.k1, self.e1 = self.state(rec)
        return self


def transitions(pn, years=((2024, 2025), (2025, 2026)), weather="ratio"):
    rows = []
    for y0, y1 in years:
        dk = pn.k[y1] - pn.k[y0]
        de = pn.e[y1] - pn.e[y0]
        same = (dk == 0) & (de == 0)
        if weather == "ratio":
            ratio = (pn.pk[y1] / pn.pk[y0])[same].groupby(pn.district[same]).median()
            adj = pn.pk[y1] - pn.district.map(ratio) * pn.pk[y0]
        elif weather == "add":
            addm = (pn.pk[y1] - pn.pk[y0])[same].groupby(pn.district[same]).mean()
            adj = pn.pk[y1] - pn.pk[y0] - pn.district.map(addm)
        else:
            adj = pn.pk[y1] - pn.pk[y0]
        rows.append(pd.DataFrame({"y": y1, "district": pn.district, "sg": pn.sg, "k0": pn.k[y0], "dk": dk, "de": de,
                                  "adj": adj}))
    return pd.concat(rows)


def increments(Pt, by_size=True, by_pos=True, agg="mean"):
    t = Pt[(Pt.dk == 1) & (Pt.de == 0)]
    f = (lambda s: s.mean()) if agg == "mean" else (lambda s: s.median())
    out = {}
    for sg in "SML":
        for pos in (1, 2, 3):
            sel = t
            if by_size:
                sel = sel[sel.sg == sg]
            if by_pos:
                cell = sel[(sel.k0.clip(upper=2) + 1) == pos]
                sel = cell if len(cell) >= MIN_CELL else t[(t.k0.clip(upper=2) + 1) == pos]
            out[(sg, pos)] = float(f(sel["adj"]))
    e = Pt[(Pt.de == 1) & (Pt.dk == 0)]
    return {"tou": out, "ev": float(f(e["adj"]))}


def cum(tab, sg, k, e):
    s = np.zeros(len(k))
    for i in range(1, int(max(k.max(), 1)) + 1):
        add = np.array([tab["tou"][(g, min(i, 3))] for g in sg])
        s += np.where(k >= i, add, 0.0)
    return s + e * tab["ev"]


def forecast(pn, tab):
    sg = pn.sg.values
    return (pn.pk[2026].values + cum(tab, sg, pn.k1.values, pn.e1.values) -
            cum(tab, sg, pn.k[2026].values, pn.e[2026].values))


def at_risk(pn, f, kva=None):
    kva = pn.kva.values if kva is None else kva
    at = f > THRESH * kva
    return pd.Series(at, index=pn.locs).groupby(pn.district).sum().reindex(NAMES).astype(int)


def allocate(counts, total=TOTAL):
    c = pd.Series(counts, dtype=float).reindex(NAMES)
    q = total * c / c.sum()
    fl = np.floor(q)
    rem = q - fl
    order = sorted(NAMES, key=lambda d: (-rem[d], -c[d]))
    out = fl.astype(int).copy()
    for d in order[: int(total - fl.sum())]:
        out[d] += 1
    return out, q


# ------------------------------------------------------------------------------------------------- the load study
def load_study_demand(P):
    """Average EVSE demand (kVA) per participant-interval across the 4 to 9 pm window, and at the window's busiest
    quarter hour, by rate; the mean charging rate (kVA)."""
    I = P.lsi
    t = I["interval_ending"]
    mins = t.dt.hour * 60 + t.dt.minute
    w = I[(mins >= 16 * 60 + 15) & (mins <= 21 * 60)].copy()
    w["rate"] = w["participant_id"].map(dict(zip(P.lsp["participant_id"], P.lsp["rate_schedule"])))
    w["kva"] = w["kwh"].astype(float) * 4 / PF
    w["qh"] = mins[w.index]
    avg = w.groupby("rate")["kva"].mean()
    busy = w.groupby(["rate", "qh"])["kva"].mean().groupby(level=0).max()
    return {"avg_tou": float(avg["R-TOU4"]), "avg_ev": float(avg["R-EV2"]), "busy_tou": float(busy["R-TOU4"]),
            "busy_ev": float(busy["R-EV2"]), "rating": float(P.lsp["charging_kw"].mean() / PF)}


def constant_forecast(pn, t, e, new_only=False):
    """2026 peak plus t per default-rate vehicle and e per EV-rate vehicle, on every change since the 2026 peak
    (or the vehicles added only)."""
    k0, e0, k1, e1 = pn.k[2026].values, pn.e[2026].values, pn.k1.values, pn.e1.values
    if new_only:
        return pn.pk[2026].values + np.clip(k1 - k0, 0, None) * t + np.clip(e1 - e0, 0, None) * e
    return pn.pk[2026].values + (k1 - k0) * t + (e1 - e0) * e


# ------------------------------------------------------------------------------------------------- the asks
PILOT_LO, PILOT_HI = pd.Timestamp("2025-10-06"), pd.Timestamp("2026-04-24")


def ask_a(P):
    c = P.chg.copy()
    c["date"] = pd.to_datetime(c["change_date"])
    dist = dict(zip(P.gis["xfmr_loc_id"], P.gis["district"]))
    c["district"] = c["xfmr_loc_id"].map(dist)
    ptr = c[(c.reason_code == "PTR") & (c.date >= PILOT_LO) & (c.date <= PILOT_HI) & c.district.isin(PILOT)]
    real = ptr[ptr.removed_serial != ptr.installed_serial]
    corr = ptr[ptr.removed_serial == ptr.installed_serial].groupby("district").size().reindex(PILOT).fillna(0).astype(int)
    n = real.groupby("district").size().reindex(PILOT).astype(int)
    kva = (real.installed_kva - real.removed_kva).groupby(real.district).sum().reindex(PILOT)
    wo_d = dict(zip(P.wo["Work Order"].astype(str), P.wo["District"]))
    cost = P.cost.copy()
    cost["amt"] = cost["amount_usd"].astype(float)
    cost["district"] = cost["wo_number"].map(wo_d)
    tot = cost.groupby("district")["amt"].sum().reindex(PILOT)
    return pd.DataFrame({"replaced": n, "kva_added": kva, "total_cost": tot, "cost_per": tot / n, "corrected": corr})


def ask_b(P):
    o = P.oms.copy()
    o["start"] = pd.to_datetime(o["outage_start_utc"]) - pd.Timedelta(hours=7)
    o["end"] = pd.to_datetime(o["restored_utc"]) - pd.Timedelta(hours=7)
    f = o[(o.cause_code == "EQ-XFMR") & (o.start >= pd.Timestamp("2026-06-01")) & (o.start < pd.Timestamp("2026-10-01"))].copy()
    nsp = P.sp.groupby("xfmr_loc_id").size()
    f["sp"] = f["xfmr_loc_id"].map(nsp)
    f["district"] = f["xfmr_loc_id"].map(dict(zip(P.gis["xfmr_loc_id"], P.gis["district"])))
    f["hours"] = (f["end"] - f["start"]).dt.total_seconds() / 3600.0
    ch = (f["sp"] * f["hours"]).groupby(f["district"]).sum().reindex(NAMES)
    o8 = f[f.hours > 8].groupby("district")["sp"].sum().reindex(NAMES).fillna(0).astype(int)
    return pd.DataFrame({"customer_hours": ch, "over_8h": o8}), f


# ------------------------------------------------------------------------------------------------- everything
def golden(target=TARGET):
    P = Pack(target)
    pn = Panel(P).build()
    Pt = transitions(pn)
    tab = increments(Pt)
    f = forecast(pn, tab)
    counts = at_risk(pn, f)
    alloc, q = allocate(counts)
    A = ask_a(P)
    Bq, _ = ask_b(P)
    return dict(P=P, pn=pn, Pt=Pt, tab=tab, f=f, counts=counts, alloc=alloc, q=q, A=A, B=Bq)


if __name__ == "__main__":
    G = golden(sys.argv[1] if len(sys.argv) > 1 else TARGET)
    print("increments", {k: round(v, 2) for k, v in G["tab"]["tou"].items()}, "EV", round(G["tab"]["ev"], 2))
    print(pd.DataFrame({"at_risk": G["counts"], "quota": G["q"].round(3), "alloc": G["alloc"]}).to_string())
    print(G["A"].round(2).to_string())
    print(G["B"].round(2).to_string())


# ------------------------------------------------------------------------------------------------- the ladder
def flows(pn):
    """Per transformer: vehicles added since its 2026 peak (by rate at the record date), vehicles there at the peak
    and gone by the record date (by rate at the peak), and vehicles there at both whose premise moved to R-EV2."""
    v = pn.v
    pk = v["loc"].map(pn.pkd[2026])
    pres_pk = (v["start"] <= pk) & (v["end"].isna() | (v["end"] > pk))
    pres_rec = (v["start"] <= REC) & (v["end"].isna() | (v["end"] > REC))
    evd = v["matched_sp_id"].astype(np.int64).map(pn.ev_from)
    ev_pk = evd.notna() & (evd <= pk)
    ev_rec = evd.notna() & (evd <= REC)
    cnt = lambda m: v[m].groupby("loc").size().reindex(pn.locs).fillna(0).astype(int).values
    return dict(newT=cnt(~pres_pk & pres_rec & ~ev_rec), newE=cnt(~pres_pk & pres_rec & ev_rec),
                goneT=cnt(pres_pk & ~pres_rec & ~ev_pk), goneE=cnt(pres_pk & ~pres_rec & ev_pk),
                switched=cnt(pres_pk & pres_rec & ~ev_pk & ev_rec))


def ladder(G):
    P, pn, Pt, tab = G["P"], G["pn"], G["Pt"], G["tab"]
    ls = load_study_demand(P)
    fl = flows(pn)
    sg = pn.sg.values
    k0, e0, k1, e1, p26 = pn.k[2026].values, pn.e[2026].values, pn.k1.values, pn.e1.values, pn.pk[2026].values
    one = Pt[((Pt.dk + Pt.de) == 1) & (Pt.dk >= 0) & (Pt.de >= 0)]
    pooled_any = float(one["adj"].mean())
    pooled = increments(Pt, by_size=False, by_pos=False)
    tou_pooled = pooled["tou"][("S", 1)]

    def fc(tab_, a, b, c, d):
        return p26 + cum(tab_, sg, c, d) - cum(tab_, sg, a, b)

    R = {}
    R["H"] = p26.copy()
    R["R0"] = constant_forecast(pn, ls["avg_tou"], ls["avg_ev"])
    R["R0b"] = constant_forecast(pn, ls["busy_tou"], ls["busy_ev"])
    R["R1"] = p26 + (fl["newT"] + fl["newE"]) * ls["rating"]
    R["R1b"] = constant_forecast(pn, ls["rating"], 0.0)
    R["R2"] = constant_forecast(pn, pooled_any, pooled_any)
    R["R2b"] = constant_forecast(pn, tou_pooled, 0.0)
    R["R3"] = fc(tab, k0, e0, k0 + fl["newT"], e0 + fl["newE"])
    R["R4"] = fc(tab, k0, e0, k1 + fl["switched"], e1 - fl["switched"])
    R["R5"] = fc(tab, k0, e0, k1 + fl["goneT"], e1 + fl["goneE"])
    R["MED"] = forecast(pn, increments(Pt, agg="median"))
    f24 = pn.pk[2024].values + cum(tab, sg, k1, e1) - cum(tab, sg, pn.k[2024].values, pn.e[2024].values)
    f25 = pn.pk[2025].values + cum(tab, sg, k1, e1) - cum(tab, sg, pn.k[2025].values, pn.e[2025].values)
    R["AVG3"] = (f24 + f25 + fc(tab, k0, e0, k1, e1)) / 3
    R["GOLD"] = forecast(pn, tab)
    fam = {
        "size x position": tab,
        "size only": increments(Pt, by_pos=False),
        "position only": increments(Pt, by_size=False),
        "pooled by rate": pooled,
        "additive weather": increments(transitions(pn, weather="add")),
        "no weather adjustment": increments(transitions(pn, weather="none")),
        "2025 to 2026 only": increments(Pt[Pt.y == 2026]),
        "2024 to 2025 only": increments(Pt[Pt.y == 2025]),
    }
    for k, t in fam.items():
        R["FAM " + k] = forecast(pn, t)
    out = {}
    for k, f in R.items():
        c = at_risk(pn, f)
        a, q = allocate(c)
        out[k] = (c, a, q)
    return out, ls, {"pooled_any": pooled_any, "tou_pooled": tou_pooled, "ev_pooled": pooled["ev"]}


def backtest(G):
    """Out of sample: each transformer's 2026 recorded peak forecast from its 2025 peak and the change in its vehicles
    between the two peak days, with the per-vehicle figures taken (a) from the load study's window averages and (b) from
    the 2024 to 2025 transitions alone; the error over the transformers whose vehicles changed."""
    P, pn = G["P"], G["pn"]
    ls = load_study_demand(P)
    dk = (pn.k[2026] - pn.k[2025]).values
    de = (pn.e[2026] - pn.e[2025]).values
    flat = (dk == 0) & (de == 0)
    ratio = (pn.pk[2026] / pn.pk[2025])[flat].groupby(pn.district[flat]).median()
    base = pn.district.map(ratio).values * pn.pk[2025].values
    t25 = increments(transitions(pn, years=((2024, 2025),)))
    sg = pn.sg.values
    fa = base + dk * ls["avg_tou"] + de * ls["avg_ev"]
    fb = base + cum(t25, sg, pn.k[2026].values, pn.e[2026].values) - cum(t25, sg, pn.k[2025].values, pn.e[2025].values)
    act = pn.pk[2026].values
    ch = ~flat
    up = ch & (dk >= 1) & (de == 0)
    out = {}
    for name, f in (("load study average", fa), ("2024-25 recorded-peak rises", fb)):
        res = act - f
        out[name] = {"n": int(ch.sum()), "mean_error": float(res[ch].mean()), "rmse": float(np.sqrt((res[ch] ** 2).mean())),
                     "mean_error_gained_default": float(res[up].mean()),
                     "at_risk_2026_forecast": int((f > THRESH * pn.kva.values).sum()),
                     "at_risk_2026_recorded": int((act > THRESH * pn.kva.values).sum())}
    return out
