"""task165 calc: every route on the shipped pack. Reads only files under target/ (and the season dates and the
planning severity, which the plan files). Each rung, rival and ask stop is a function here; checks.py asserts them
and cracker.py scores them."""
from __future__ import annotations

import datetime as dt
import os

import numpy as np
import pandas as pd

import common as K

F_LEGACY = "avl_legacy_segment_shift_2021-11-01_2023-03-31.csv"
F_PASSES = "telematics_segment_passes_2023-10-01_2026-09-23.parquet"
F_XWALK = "gis_segment_crosswalk_2023.csv"
F_REGISTER = "winter_route_register_2026-09-14.csv"
F_REVLOG = "route_audit_revision_log.csv"
F_STORM = "storm_log_2021-22_to_2025-26.xlsx"

PLAN_SEV = 61.7


def season_of_local(ts):
    """Winter label of a local timestamp or date, or None outside 1 November to 31 March."""
    d = ts.date() if hasattr(ts, "date") else ts
    if d.month >= 11:
        return "%d-%02d" % (d.year, (d.year + 1) % 100)
    if d.month <= 3:
        return "%d-%02d" % (d.year - 1, d.year % 100)
    return None


class Pack:
    def __init__(self, target, wsi=None, utc_as_local=False, xwalk=True):
        self.target = target
        self.reg = pd.read_csv(os.path.join(target, F_REGISTER), dtype=str)
        self.reg["lane_km"] = self.reg["lane_km"].astype(float)
        self.reg["centreline_km"] = self.reg["centreline_km"].astype(float)
        self.rev = pd.read_csv(os.path.join(target, F_REVLOG), dtype=str)
        self.wsi = wsi if wsi is not None else self._wsi()
        self._salt(utc_as_local, xwalk)

    def _wsi(self):
        out = {}
        xl = pd.ExcelFile(os.path.join(self.target, F_STORM))
        for w in K.WINTERS:
            df = xl.parse(w, header=None)
            # find the header row and the points column
            hdr = None
            for i in range(min(8, len(df))):
                vals = [str(v).strip().lower() for v in df.iloc[i].tolist()]
                if any(v in ("points", "wsi_points") for v in vals):
                    hdr = i
                    break
            df.columns = [str(v).strip().lower() for v in df.iloc[hdr].tolist()]
            df = df.iloc[hdr + 1:]
            col = "points" if "points" in df.columns else "wsi_points"
            idc = "event" if "event" in df.columns else "event_id"
            ev = df[pd.to_numeric(df[idc], errors="coerce").notna() | df[idc].astype(str).str.match(r"^\d{2}-\d{3}$")]
            out[w] = float(pd.to_numeric(ev[col], errors="coerce").sum())
        return out

    def _salt(self, utc_as_local, xwalk):
        """Rock salt per current segment per winter (tonnes), from both exports."""
        leg = pd.read_csv(os.path.join(self.target, F_LEGACY), dtype={"SEG_ID": str})
        leg = leg[leg["MATL"] == "SALT"].copy()
        leg["d"] = pd.to_datetime(leg["SHIFT_DATE"])
        leg["winter"] = [season_of_local(d) for d in leg["d"]]
        leg = leg[leg["winter"].notna()]
        xw = pd.read_csv(os.path.join(self.target, F_XWALK), dtype=str)
        xw["length_share"] = xw["length_share"].astype(float)
        if xwalk:
            leg = leg.merge(xw, left_on="SEG_ID", right_on="legacy_segment_id", how="left")
            leg["t"] = leg["KG"] / 1000.0 * leg["length_share"]
        else:
            leg["segment_id"] = leg["SEG_ID"]
            leg["t"] = leg["KG"] / 1000.0
        a = leg.groupby(["segment_id", "winter"])["t"].sum()
        ps = pd.read_parquet(os.path.join(self.target, F_PASSES))
        ps = ps[ps["material_code"] == "RS"]
        ent = ps["entry_utc"].dt.tz_convert(None) if utc_as_local else \
            ps["entry_utc"].dt.tz_convert("America/Toronto").dt.tz_localize(None)
        ps = ps.assign(local=ent)
        ps["winter"] = [season_of_local(t) for t in ps["local"]]
        ps = ps[ps["winter"].notna()]
        self.passes = ps
        b = ps.groupby(["segment_id", "winter"])["applied_t"].sum()
        self.salt = pd.concat([a, b]).groupby(level=[0, 1]).sum()

    # --------------------------------------------------------------------------------------- populations
    def moves(self):
        """Collector segments the route audit moved from Priority 2 to Priority 1, with their effective dates."""
        r = self.rev[(self.rev["field"] == "PRIORITY") & (self.rev["old_value"] == "2") & (self.rev["new_value"] == "1")]
        r = r.merge(self.reg[["segment_id", "func_class", "lane_km", "yard", "lanes", "centreline_km", "street"]],
                    on="segment_id")
        r = r[r["func_class"] == "COLLECTOR"]
        r["eff"] = pd.to_datetime(r["effective_date"]).dt.date
        return r

    def earlier_moves(self):
        m = self.moves()
        return m[m["eff"] < K.REDESIGN]

    def new_pool(self):
        m = self.moves()
        return m[m["eff"] == K.REDESIGN]

    def rate(self, sid, winters, lane_km):
        tot = sum(float(self.salt.get((sid, w), 0.0)) for w in winters)
        pts = sum(self.wsi[w] for w in winters)
        return tot / (lane_km * pts)

    def prepost(self, which="all", pre_last=False, post_first=False):
        """For each earlier move: lane-km, pre-move rate and post-move rate (t per lane-km per point)."""
        out = []
        for _, r in self.earlier_moves().iterrows():
            first = "%d-%02d" % (r["eff"].year, (r["eff"].year + 1) % 100)
            pre = [w for w in K.WINTERS if K.WINTERS.index(w) < K.WINTERS.index(first)]
            post = [w for w in K.WINTERS if K.WINTERS.index(w) >= K.WINTERS.index(first)]
            if pre_last:
                pre = pre[-1:]
            if post_first:
                post = post[:1]
            out.append({"segment_id": r["segment_id"], "lane_km": r["lane_km"], "yard": r["yard"],
                        "reason": r["reason"], "eff": r["eff"], "lanes": r["lanes"], "street": r["street"],
                        "pre": self.rate(r["segment_id"], pre, r["lane_km"]),
                        "post": self.rate(r["segment_id"], post, r["lane_km"])})
        return pd.DataFrame(out)

    def new_rates(self, winters=None):
        winters = winters or K.WINTERS
        nn = self.new_pool()
        return pd.DataFrame([{"segment_id": r["segment_id"], "lane_km": r["lane_km"], "yard": r["yard"],
                              "lanes": r["lanes"], "p2": self.rate(r["segment_id"], winters, r["lane_km"])}
                             for _, r in nn.iterrows()])


def wls(x, y, w):
    X = np.column_stack([np.ones_like(x), x])
    A = X.T @ (X * w[:, None])
    return np.linalg.solve(A, X.T @ (w * y))


# ------------------------------------------------------------------------------------------------- the golden family
def golden(P: Pack, weight=True, pre_last=False, post_first=False, per_segment=False, level=False, sev=PLAN_SEV):
    d = P.prepost(pre_last=pre_last, post_first=post_first)
    nn = P.new_rates()
    w = d["lane_km"].values if weight else np.ones(len(d))
    L = nn["lane_km"].sum()
    if level:
        b = wls(d["pre"].values, d["post"].values, w)
        pred = (b[0] + b[1] * nn["p2"].values) - nn["p2"].values
    else:
        b = wls(d["pre"].values, (d["post"] - d["pre"]).values, w)
        pred = b[0] + b[1] * nn["p2"].values
    if per_segment:
        return float((pred * nn["lane_km"].values).sum() * sev)
    x0 = float((nn["p2"] * nn["lane_km"]).sum() / L)
    if level:
        return float(((b[0] + b[1] * x0) - x0) * L * sev)
    return float((b[0] + b[1] * x0) * L * sev)


def gain_coefficients(P: Pack):
    d = P.prepost()
    return wls(d["pre"].values, (d["post"] - d["pre"]).values, d["lane_km"].values)


# ------------------------------------------------------------------------------------------------- rivals
def p1_collector_rate(P: Pack, only_moves=False):
    """Salt per lane-km per point on every collector segment in each winter it was Priority 1."""
    tot, den = 0.0, 0.0
    mv = P.earlier_moves()
    moved = {r["segment_id"]: r["eff"] for _, r in mv.iterrows()}
    cols = P.reg[(P.reg["func_class"] == "COLLECTOR") & (P.reg["priority"] == "1")]
    newids = set(P.new_pool()["segment_id"])
    for _, r in cols.iterrows():
        sid = r["segment_id"]
        if sid in newids:
            continue
        if sid in moved:
            e = moved[sid]
            first = "%d-%02d" % (e.year, (e.year + 1) % 100)
            ws = [w for w in K.WINTERS if K.WINTERS.index(w) >= K.WINTERS.index(first)]
        else:
            if only_moves:
                continue
            ws = K.WINTERS
        for w in ws:
            tot += float(P.salt.get((sid, w), 0.0))
            den += r["lane_km"] * P.wsi[w]
    return tot / den


def r1_default(P: Pack, only_moves=False):
    nn = P.new_rates()
    L = nn["lane_km"].sum()
    x0 = float((nn["p2"] * nn["lane_km"]).sum() / L)
    return (p1_collector_rate(P, only_moves) - x0) * L * PLAN_SEV


def r2_pooled(P: Pack, reason=None):
    d = P.prepost()
    if reason:
        d = d[d["reason"].str.contains(reason)]
    g = ((d["post"] - d["pre"]) * d["lane_km"]).sum() / d["lane_km"].sum()
    return float(g * P.new_pool()["lane_km"].sum() * PLAN_SEV)


def r0_network(P: Pack, sev=PLAN_SEV, winters=None):
    """The Priority 1 network's salt per lane-km per point (arterials and Priority 1 collectors), gross."""
    winters = winters or K.WINTERS
    tot, den = 0.0, 0.0
    p1 = P.reg[P.reg["priority"] == "1"]
    newids = set(P.new_pool()["segment_id"])
    mv = {r["segment_id"]: r["eff"] for _, r in P.earlier_moves().iterrows()}
    for _, r in p1.iterrows():
        sid = r["segment_id"]
        if sid in newids:
            continue
        ws = winters
        if sid in mv:
            e = mv[sid]
            first = "%d-%02d" % (e.year, (e.year + 1) % 100)
            ws = [w for w in winters if K.WINTERS.index(w) >= K.WINTERS.index(first)]
        for w in ws:
            v = float(P.salt.get((sid, w), 0.0))
            if v <= 0:
                continue
            tot += v
            den += r["lane_km"] * P.wsi[w]
    return tot / den * P.new_pool()["lane_km"].sum() * sev


# ================================================================================================= the asks
F_SCALE = "scale_house_log_2026-08-24_to_2026-09-24.xlsx"
F_DISPATCH1 = "northgrit_dispatch_2026-10_issued_2026-09-14.csv"
F_DISPATCH2 = "northgrit_dispatch_2026-10_issued_2026-09-21.csv"
F_SURVEY = "dome_stock_survey_2026-09.pdf"
F_DOMES = "salt_dome_register.csv"
F_FLEET = "fleet_units_2026-09.csv"
F_LOADING = "yard_loading_log_2023-11_2026-03.csv"
F_PELLARD = "kettlewood_material_returns_2023-24_to_2025-26.xlsx"
YARDS = ["KLV", "MPF", "RDG", "LKS"]
BRINE_KG_L = 1.18            # the plan's plant brine, kilograms a litre
PREWET_L_T = 40.0            # the plan's pre-wet rate, litres a tonne of rock salt
YARD_NAME = {"Kelvin Road Yard": "KLV", "Mapleford Yard": "MPF", "Ridge Yard": "RDG", "Lakeshore Yard": "LKS"}


def pdf_text(path):
    import pypdf
    r = pypdf.PdfReader(path)
    return "\n".join(p.extract_text() for p in r.pages)


def survey(target):
    """Survey date, stock (t) and capture end (UTC) per yard, read off the survey report."""
    import re
    txt = pdf_text(os.path.join(target, F_SURVEY))
    out = {}
    lines = [l.strip() for l in txt.splitlines()]
    for name, y in YARD_NAME.items():
        i = lines.index(name)
        d = dt.datetime.strptime(lines[i + 1], "%d %B %Y").date()
        stock = float(lines[i + 4].replace(",", ""))
        out[y] = {"date": d, "stock": stock}
    for j, l in enumerate(lines):
        if re.match(r"^TG-26-\d{3}$", l):
            y = YARD_NAME[lines[j + 1]]
            start = dt.datetime.strptime(lines[j + 2], "%Y-%m-%d %H:%M")
            hh, mm = map(int, lines[j + 3].split(":"))
            out[y]["capture_start_utc"] = start
            out[y]["capture_end_utc"] = start.replace(hour=hh, minute=mm)
    return out


def scale_log(target):
    xl = pd.ExcelFile(os.path.join(target, F_SCALE))
    frames = []
    for y in YARDS:
        df = xl.parse(y, dtype={"Remarks": str})
        df["sheet"] = y
        frames.append(df)
    df = pd.concat(frames, ignore_index=True)
    df["Remarks"] = df["Remarks"].fillna("")
    df["date"] = pd.to_datetime(df["Date"]).dt.date
    df["t_in"] = [dt.datetime.combine(d, dt.datetime.strptime(str(t), "%H:%M").time())
                  for d, t in zip(df["date"], df["Time in"])]
    return df


def dome_of(row):
    rem = str(row["Remarks"]).upper()
    if "LKS" in rem or "LAKESHORE" in rem:
        return "LKS"
    if "MPF" in rem or "MAPLEFORD" in rem:
        return "MPF"
    return row["sheet"]


ASK_A_MODES = {
    "golden": {},
    "day_after": {"cutoff": "day_after", "dome_by": "sheet"},        # the cracker's natural read
    "day_after_dome": {"cutoff": "day_after"},                       # remarks read, the survey day left out
    "day_whole": {"cutoff": "day_whole"},
    "utc_local": {"cutoff": "utc_local"},
    "sheets": {"dome_by": "sheet"},
    "supplier_only": {"flows": "supplier_only"},
    "first_issue": {"issue": 1},
}


def ask_a(target, mode="golden", cutoff="time", dome_by="remarks", flows="all", issue=2):
    """Each dome's stock on 1 November 2026 and its room. cutoff: time (after the capture's end, local), day_after
    (from the day after the survey), day_whole (the survey day whole), utc_local (the capture's UTC end read as
    local); dome_by: remarks (a load weighed for another yard's dome counts there) or sheet; flows: all (in and out)
    or supplier_only; issue: the dispatch issue used."""
    kw = dict(cutoff=cutoff, dome_by=dome_by, flows=flows, issue=issue)
    kw.update(ASK_A_MODES[mode])
    sv = survey(target)
    df = scale_log(target)
    cap = pd.read_csv(os.path.join(target, F_DOMES)).set_index("yard")["rated_capacity_t"].astype(float)
    disp = pd.read_csv(os.path.join(target, F_DISPATCH1 if kw["issue"] == 1 else F_DISPATCH2))
    stock, room = {}, {}
    for y in YARDS:
        v = sv[y]["stock"]
        end_utc = sv[y]["capture_end_utc"]
        end_local = end_utc - dt.timedelta(hours=4)       # EDT in September
        if kw["cutoff"] == "utc_local":
            end_local = end_utc
        for _, r in df.iterrows():
            dome = r["sheet"] if kw["dome_by"] == "sheet" else dome_of(r)
            if dome != y:
                continue
            if kw["cutoff"] == "day_after":
                if r["date"] <= sv[y]["date"]:
                    continue
            elif kw["cutoff"] == "day_whole":
                if r["date"] < sv[y]["date"]:
                    continue
            elif r["t_in"] <= end_local:
                continue
            if kw["flows"] == "supplier_only":
                if r["Direction"] == "IN" and str(r["Carrier"]).startswith("Northgrit"):
                    v += r["Net kg"] / 1000.0
                continue
            v += (r["Net kg"] if r["Direction"] == "IN" else -r["Net kg"]) / 1000.0
        bk = disp[(disp["ship_to"] == "QB-" + y) & (disp["status"] == "BOOKED")]
        bk = bk[pd.to_datetime(bk["delivery_date"]).dt.month == 10]
        v += float(bk["planned_net_t"].sum())
        stock[y] = v
        room[y] = float(cap[y]) - v
    return stock, room


def arterial_salt(target, mode="golden"):
    """Rock salt on each yard's Priority 1 arterials in each of the three winters since October 2023. Modes:
    golden; rows (every row summed); no_contract (the contractor's returns left out); register_yard (the
    register's yard instead of the route code's); utc_season (season dates read in UTC)."""
    ps = pd.read_parquet(os.path.join(target, F_PASSES))
    ps = ps[(ps["material_code"] == "RS") & ps["route_code"].str.contains("-A")]
    if mode == "utc_season":
        ps = ps.assign(local=ps["entry_utc"].dt.tz_convert(None))
    else:
        ps = ps.assign(local=ps["entry_utc"].dt.tz_convert("America/Toronto").dt.tz_localize(None))
    ps["winter"] = [season_of_local(t) for t in ps["local"]]
    ps = ps[ps["winter"].isin(["2023-24", "2024-25", "2025-26"])]
    if mode == "register_yard":
        reg = pd.read_csv(os.path.join(target, F_REGISTER), dtype=str)[["segment_id", "yard"]]
        ps = ps.merge(reg, on="segment_id")
    else:
        ps = ps.assign(yard=ps["route_code"].str[:3])
    if mode == "rows":
        tot = ps.groupby(["yard", "winter"])["applied_t"].sum()
    else:
        fl = pd.read_csv(os.path.join(target, F_FLEET), dtype=str)
        old = fl[fl["spreader_controller"].eq("M410") | fl["controller_retrofit"].notna()]
        retro = {u: (pd.to_datetime(d).date() if isinstance(d, str) else None)
                 for u, d in zip(old["unit_id"], old["controller_retrofit"])}
        ps["day"] = ps["local"].dt.date
        is410 = [u in retro and (retro[u] is None or d < retro[u]) for u, d in zip(ps["unit_id"], ps["day"])]
        ps["m410"] = is410
        if mode == "runs_once":          # run totals taken once, the combined mass left as it is
            ps["solid"] = ps["applied_t"]
        elif mode == "prewet_rate":      # the salt read back from the brine at the plan's 40 litres a tonne
            ps["solid"] = ps["prewet_l"] / PREWET_L_T
        elif mode == "net_brine":        # the brine's mass taken off, every row summed
            ps["solid"] = ps["applied_t"] - np.where(ps["m410"], ps["prewet_l"] * BRINE_KG_L / 1000.0, 0.0)
        else:
            ps["solid"] = ps["applied_t"] - np.where(ps["m410"], ps["prewet_l"] * BRINE_KG_L / 1000.0, 0.0)
        if mode == "net_brine":
            tot = ps.groupby(["yard", "winter"])["solid"].sum()
        else:
            a = ps[~ps["m410"]].groupby(["yard", "winter"])["solid"].sum()
            b = ps[ps["m410"]].groupby(["yard", "winter", "run_ref"])["solid"].first().groupby(level=[0, 1]).sum()
            tot = pd.concat([a, b]).groupby(level=[0, 1]).sum()
    out = {(y, w): float(tot.get((y, w), 0.0)) for y in YARDS for w in ["2023-24", "2024-25", "2025-26"]}
    if mode != "no_contract":
        xl = pd.ExcelFile(os.path.join(target, F_PELLARD))
        for w in ["2023-24", "2024-25", "2025-26"]:
            df = xl.parse(w, header=2)
            df["m"] = pd.to_datetime(df["Month"] + "-01")
            df = df[[season_of_local(d) == w for d in df["m"]]]
            for rc, t in zip(df["City circuit"], df["Rock salt (t)"]):
                out[(rc[:3], w)] += float(t)
    return out


# ================================================================================================= the reflex sweep
def _new_mix(P: Pack):
    nn = P.new_pool().copy()
    nn["lenband"] = pd.cut(nn["centreline_km"], [0, 0.7, 1.0, 1.3, 9], labels=False)
    return nn


def reflex_stratified(P: Pack, key):
    """The earlier moves' pooled gain within strata of one visible field, applied to the new streets' mix."""
    d = P.prepost()
    mv = P.earlier_moves().set_index("segment_id")
    d["lenband"] = pd.cut(mv.loc[d["segment_id"], "centreline_km"].values, [0, 0.7, 1.0, 1.3, 9], labels=False)
    d["gain"] = d["post"] - d["pre"]
    nn = _new_mix(P)
    tot = 0.0
    for k, g in nn.groupby(key):
        sub = d[d[key] == k]
        if len(sub) == 0:
            sub = d
        rate = (sub["gain"] * sub["lane_km"]).sum() / sub["lane_km"].sum()
        tot += rate * g["lane_km"].sum()
    return float(tot * PLAN_SEV)


def reflex_trend(P: Pack):
    """The pooled gain of each move year, trended linearly to 2026."""
    d = P.prepost()
    d["gain"] = d["post"] - d["pre"]
    d["yr"] = [e.year for e in d["eff"]]
    g = d.groupby("yr").apply(lambda x: (x["gain"] * x["lane_km"]).sum() / x["lane_km"].sum())
    b = np.polyfit(g.index.values.astype(float), g.values, 1)
    return float(np.polyval(b, 2026.0) * P.new_pool()["lane_km"].sum() * PLAN_SEV)


def reflex_did(P: Pack):
    """Before-and-after against the never-moved Priority 2 collectors, winter by winter, pooled over the moves."""
    reg = P.reg
    moved = set(P.moves()["segment_id"])
    ctrl = reg[(reg["func_class"] == "COLLECTOR") & (reg["priority"] == "2") & (~reg["segment_id"].isin(moved))]
    cr = {}
    for w in K.WINTERS:
        tot = sum(float(P.salt.get((s, w), 0.0)) for s in ctrl["segment_id"])
        cr[w] = tot / (ctrl["lane_km"].sum() * P.wsi[w])
    base = np.mean(list(cr.values()))
    num, den = 0.0, 0.0
    for _, r in P.earlier_moves().iterrows():
        first = "%d-%02d" % (r["eff"].year, (r["eff"].year + 1) % 100)
        pre = [w for w in K.WINTERS if K.WINTERS.index(w) < K.WINTERS.index(first)]
        post = [w for w in K.WINTERS if K.WINTERS.index(w) >= K.WINTERS.index(first)]
        def adj(ws):
            return np.mean([float(P.salt.get((r["segment_id"], w), 0.0)) / (r["lane_km"] * P.wsi[w]) / cr[w] * base
                            for w in ws])
        num += (adj(post) - adj(pre)) * r["lane_km"]
        den += r["lane_km"]
    return float(num / den * P.new_pool()["lane_km"].sum() * PLAN_SEV)


def reflex_ratio(P: Pack):
    d = P.prepost()
    ratio = (d["post"] * d["lane_km"]).sum() / (d["pre"] * d["lane_km"]).sum()
    nn = P.new_rates()
    x0 = float((nn["p2"] * nn["lane_km"]).sum() / nn["lane_km"].sum())
    return float((ratio - 1) * x0 * nn["lane_km"].sum() * PLAN_SEV)


def golden_did(P: Pack):
    """The golden's conditioning with each winter normalised against the never-moved Priority 2 collectors."""
    reg = P.reg
    moved = set(P.moves()["segment_id"])
    ctrl = reg[(reg["func_class"] == "COLLECTOR") & (reg["priority"] == "2") & (~reg["segment_id"].isin(moved))]
    cr = {}
    for w in K.WINTERS:
        tot = sum(float(P.salt.get((s, w), 0.0)) for s in ctrl["segment_id"])
        cr[w] = tot / (ctrl["lane_km"].sum() * P.wsi[w])
    base = np.mean(list(cr.values()))
    rows = []
    for _, r in P.earlier_moves().iterrows():
        first = "%d-%02d" % (r["eff"].year, (r["eff"].year + 1) % 100)
        pre = [w for w in K.WINTERS if K.WINTERS.index(w) < K.WINTERS.index(first)]
        post = [w for w in K.WINTERS if K.WINTERS.index(w) >= K.WINTERS.index(first)]
        def adj(ws):
            return np.mean([float(P.salt.get((r["segment_id"], w), 0.0)) / (r["lane_km"] * P.wsi[w]) / cr[w] * base
                            for w in ws])
        rows.append((r["lane_km"], adj(pre), adj(post)))
    L, pre, post = map(np.array, zip(*rows))
    b = wls(pre, post - pre, L)
    nn = P.new_rates()
    x0 = float((nn["p2"] * nn["lane_km"]).sum() / nn["lane_km"].sum())
    return float((b[0] + b[1] * x0) * nn["lane_km"].sum() * PLAN_SEV)


def bootstrap_sd(P: Pack, n=400, seed=1650925):
    rng = np.random.default_rng(seed)
    d = P.prepost()
    nn = P.new_rates()
    x0 = float((nn["p2"] * nn["lane_km"]).sum() / nn["lane_km"].sum())
    L = nn["lane_km"].sum()
    out = []
    for _ in range(n):
        idx = rng.integers(0, len(d), len(d))
        s = d.iloc[idx]
        b = wls(s["pre"].values, (s["post"] - s["pre"]).values, s["lane_km"].values)
        out.append((b[0] + b[1] * x0) * L * PLAN_SEV)
    return float(np.std(out))


def holdout(P: Pack):
    """Each move year held out in turn: its total gain predicted by the pooled gain and by the conditioned gain of
    the other years, as a share of the observed."""
    d = P.prepost()
    d["gain"] = d["post"] - d["pre"]
    d["yr"] = [e.year for e in d["eff"]]
    out = {}
    for yr in sorted(d["yr"].unique()):
        tr, te = d[d["yr"] != yr], d[d["yr"] == yr]
        obs = (te["gain"] * te["lane_km"]).sum()
        pooled = (tr["gain"] * tr["lane_km"]).sum() / tr["lane_km"].sum() * te["lane_km"].sum()
        b = wls(tr["pre"].values, tr["gain"].values, tr["lane_km"].values)
        cond = ((b[0] + b[1] * te["pre"]) * te["lane_km"]).sum()
        out[int(yr)] = (float(pooled / obs - 1), float(cond / obs - 1))
    return out


# ================================================================================================= the golden's family
def _xw(P: Pack):
    d = P.prepost()
    nn = P.new_rates()
    return d, nn, d["pre"].values, (d["post"] - d["pre"]).values, d["lane_km"].values


def knn(P: Pack, k):
    """Each new street's gain as the lane-km weighted gain of the k earlier moves nearest it in Priority 2 salt."""
    d, nn, x, g, w = _xw(P)
    tot = 0.0
    for p2, L in zip(nn["p2"].values, nn["lane_km"].values):
        idx = np.argsort(np.abs(x - p2), kind="stable")[:k]
        tot += np.average(g[idx], weights=w[idx]) * L
    return float(tot * PLAN_SEV)


def qbins(P: Pack, q):
    """The earlier moves' gain in q bands of Priority 2 salt (equal counts), each new street given its band's gain."""
    d, nn, x, g, w = _xw(P)
    edges = np.quantile(x, np.linspace(0, 1, q + 1))
    edges[0], edges[-1] = -1.0, 9.0
    cx = pd.cut(x, edges, labels=False)
    cn = pd.cut(nn["p2"].values, edges, labels=False)
    return float(sum(np.average(g[cx == b], weights=w[cx == b]) * nn["lane_km"].values[cn == b].sum()
                     for b in range(q)) * PLAN_SEV)


def quadratic(P: Pack):
    d, nn, x, g, w = _xw(P)
    b = np.polyfit(x, g, 2, w=np.sqrt(w))
    return float((np.polyval(b, nn["p2"].values) * nn["lane_km"].values).sum() * PLAN_SEV)


def trimmed(P: Pack, k=3.0):
    """The golden's line refitted without the streets whose gain sits k residual standard deviations off it."""
    d, nn, x, g, w = _xw(P)
    b = wls(x, g, w)
    res = g - (b[0] + b[1] * x)
    keep = np.abs(res) < k * res.std()
    b2 = wls(x[keep], g[keep], w[keep])
    x0 = float((nn["p2"] * nn["lane_km"]).sum() / nn["lane_km"].sum())
    return float((b2[0] + b2[1] * x0) * nn["lane_km"].sum() * PLAN_SEV)


def winter_mean(P: Pack):
    """The golden with each street's rate the mean of its winters' rates rather than its salt over its points."""
    def rm(sid, ws, lk):
        return float(np.mean([float(P.salt.get((sid, w), 0.0)) / (lk * P.wsi[w]) for w in ws]))
    rows = []
    for _, r in P.earlier_moves().iterrows():
        first = "%d-%02d" % (r["eff"].year, (r["eff"].year + 1) % 100)
        pre = [w for w in K.WINTERS if K.WINTERS.index(w) < K.WINTERS.index(first)]
        post = [w for w in K.WINTERS if K.WINTERS.index(w) >= K.WINTERS.index(first)]
        rows.append((r["lane_km"], rm(r["segment_id"], pre, r["lane_km"]), rm(r["segment_id"], post, r["lane_km"])))
    L, pre, post = map(np.array, zip(*rows))
    b = wls(pre, post - pre, L)
    nn = P.new_pool()
    x0 = float(np.average([rm(s, K.WINTERS, l) for s, l in zip(nn["segment_id"], nn["lane_km"])],
                          weights=nn["lane_km"].values))
    return float((b[0] + b[1] * x0) * nn["lane_km"].sum() * PLAN_SEV)


def centreline(P: Pack):
    """The golden on centreline km throughout: rates per centreline km per point, the line weighted by centreline
    km, scaled by the new streets' centreline km."""
    mv = P.earlier_moves()
    rows = []
    for _, r in mv.iterrows():
        first = "%d-%02d" % (r["eff"].year, (r["eff"].year + 1) % 100)
        pre = [w for w in K.WINTERS if K.WINTERS.index(w) < K.WINTERS.index(first)]
        post = [w for w in K.WINTERS if K.WINTERS.index(w) >= K.WINTERS.index(first)]
        cl = r["centreline_km"]
        rows.append((cl, P.rate(r["segment_id"], pre, cl), P.rate(r["segment_id"], post, cl)))
    cl, pre, post = map(np.array, zip(*rows))
    b = wls(pre, post - pre, cl)
    nn = P.new_pool()
    x = np.array([P.rate(s, K.WINTERS, c) for s, c in zip(nn["segment_id"], nn["centreline_km"])])
    c = nn["centreline_km"].values
    x0 = float((x * c).sum() / c.sum())
    return float((b[0] + b[1] * x0) * c.sum() * PLAN_SEV)


def loglog(P: Pack):
    """Each street's Priority 1 rate as a power of its Priority 2 rate (a line in logs), less its Priority 2 rate."""
    d, nn, x, g, w = _xw(P)
    bl = np.polyfit(np.log(x), np.log(d["post"].values), 1, w=np.sqrt(w))
    return float(((np.exp(bl[1] + bl[0] * np.log(nn["p2"].values)) - nn["p2"].values) * nn["lane_km"].values).sum()
                 * PLAN_SEV)


def _fit_predict(tr, te, form):
    xt, yt, wt = tr["pre"].values, tr["post"].values, tr["lane_km"].values
    if form == "line":
        b = wls(xt, yt - xt, wt)
        return b[0] + b[1] * te["pre"].values
    if form == "loglog":
        bl = np.polyfit(np.log(xt), np.log(yt), 1, w=np.sqrt(wt))
        return np.exp(bl[1] + bl[0] * np.log(te["pre"].values)) - te["pre"].values
    return np.full(len(te), ((tr["post"] - tr["pre"]) * tr["lane_km"]).sum() / tr["lane_km"].sum())


def cv_wsse(P: Pack, form, folds=10, seed=1650925):
    """Ten-fold cross-validation over the earlier moves: lane-km weighted squared error of each street's gain."""
    d = P.prepost()
    idx = np.random.default_rng(seed).permutation(len(d))
    se = 0.0
    for f in np.array_split(idx, folds):
        te = d.iloc[f]
        tr = d.drop(d.index[f])
        se += float(((_fit_predict(tr, te, form) - (te["post"] - te["pre"]).values) ** 2 * te["lane_km"].values).sum())
    return se


def low_band(P: Pack, form):
    """Fitted on the earlier moves above the new streets' 90th percentile of Priority 2 salt, the error in the total
    gain of the moves at or below it (the band the new streets sit in), as a share of the observed."""
    d = P.prepost()
    nn = P.new_rates()
    q90 = float(np.quantile(nn["p2"].values, 0.9))
    lo, hi = d[d["pre"] <= q90], d[d["pre"] > q90]
    pred = float((_fit_predict(hi, lo, form) * lo["lane_km"].values).sum())
    obs = float(((lo["post"] - lo["pre"]) * lo["lane_km"]).sum())
    return pred / obs - 1, len(lo)


def range_match(P: Pack):
    """The earlier moves whose Priority 2 salt lies within the new streets' range, their gain averaged by lane-km."""
    d = P.prepost()
    nn = P.new_rates()
    lo, hi = float(nn["p2"].min()), float(nn["p2"].max())
    sub = d[(d["pre"] >= lo) & (d["pre"] <= hi)]
    g = ((sub["post"] - sub["pre"]) * sub["lane_km"]).sum() / sub["lane_km"].sum()
    mean_pre = float((sub["pre"] * sub["lane_km"]).sum() / sub["lane_km"].sum())
    return float(g * nn["lane_km"].sum() * PLAN_SEV), len(sub), mean_pre * PLAN_SEV


# ================================================================================================= crude settings
def kernel(P: Pack, bw):
    """Each new street's gain as a Gaussian-kernel mean of the earlier moves' gains, bandwidth bw t a lane-km of
    Priority 2 salt in a planning-severity winter, weighted by lane-km."""
    d, nn, x, g, w = _xw(P)
    xs = x * PLAN_SEV
    tot = 0.0
    for p2, L in zip(nn["p2"].values * PLAN_SEV, nn["lane_km"].values):
        k = np.exp(-0.5 * ((xs - p2) / bw) ** 2) * w
        tot += float(np.sum(k * g) / np.sum(k)) * L
    return tot * PLAN_SEV


def fixed_bands(P: Pack, width):
    """Fixed bands of Priority 2 salt (t a lane-km in a planning-severity winter), each new street given its band's
    lane-km weighted gain."""
    d, nn, x, g, w = _xw(P)
    b = np.floor(x * PLAN_SEV / width)
    tot = 0.0
    for bi, L in zip(np.floor(nn["p2"].values * PLAN_SEV / width), nn["lane_km"].values):
        m = b == bi
        if not m.any():
            m = np.abs(b - bi) == np.abs(b - bi).min()
        tot += float(np.average(g[m], weights=w[m])) * L
    return tot * PLAN_SEV


def nearest_to_mean(P: Pack, k):
    """The k earlier moves nearest the new streets' mean Priority 2 salt, their gain averaged."""
    d, nn, x, g, w = _xw(P)
    x0 = float((nn["p2"] * nn["lane_km"]).sum() / nn["lane_km"].sum())
    idx = np.argsort(np.abs(x - x0), kind="stable")[:k]
    return float(np.average(g[idx], weights=w[idx]) * nn["lane_km"].sum() * PLAN_SEV)


def window(P: Pack, half):
    """The earlier moves within half t a lane-km of the new streets' mean Priority 2 salt, their gain averaged."""
    d, nn, x, g, w = _xw(P)
    x0 = float((nn["p2"] * nn["lane_km"]).sum() / nn["lane_km"].sum())
    m = np.abs(x - x0) * PLAN_SEV <= half
    return float(np.average(g[m], weights=w[m]) * nn["lane_km"].sum() * PLAN_SEV), int(m.sum())
