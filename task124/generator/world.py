"""The book: premises, their enrolments with Sabine Crest, the fourteen Business Saver members, Harlan Ridge's 31 new
centres, the twin pair, and the March 2027 amendment run. Everything downstream reads this frame."""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pandas as pd

from common import BOOKS, EXTRACT, NC, PEAKS

GROWTH = {"Coast": 0.035, "East": 0.030, "Far West": 0.020, "North": 0.015, "North Central": 0.055,
          "South Central": 0.040, "Southern": 0.030, "West": 0.020}
# dedup book at the extract, centres excluded, members included (MW): the scale the growth path ends on
M27 = {"Coast": 1496.8, "East": 645.7, "Far West": 431.3, "North": 377.9, "North Central": 1118.1,
       "South Central": 898.6, "Southern": 567.1, "West": 501.0}
IDR_SHARE = {"Coast": 0.085, "East": 0.070, "Far West": 0.090, "North": 0.065, "North Central": 0.080,
             "South Central": 0.075, "Southern": 0.072, "West": 0.088}

TDSP_OF = {"Coast": [("CENTERPOINT", 0.93), ("TNMP", 0.07)], "East": [("ONCOR", 1.0)],
           "Far West": [("ONCOR", 0.62), ("TNMP", 0.38)], "North": [("ONCOR", 0.55), ("AEP_NORTH", 0.45)],
           "North Central": [("ONCOR", 0.91), ("TNMP", 0.09)], "South Central": [("ONCOR", 0.58), ("AEP_CENTRAL", 0.42)],
           "Southern": [("AEP_CENTRAL", 1.0)], "West": [("AEP_NORTH", 0.71), ("ONCOR", 0.29)]}
ESI_PREFIX = {"CENTERPOINT": "1008901", "ONCOR": "10443720", "TNMP": "10400511", "AEP_NORTH": "10204049",
              "AEP_CENTRAL": "10032789"}

PROFILED_NAICS = [("722511", 0.14), ("445120", 0.09), ("811111", 0.07), ("531120", 0.09), ("621111", 0.07),
                  ("812112", 0.04), ("448140", 0.04), ("541110", 0.05), ("238220", 0.05), ("813110", 0.05),
                  ("611110", 0.04), ("441110", 0.04), ("721110", 0.05), ("424490", 0.04), ("332710", 0.04),
                  ("484121", 0.04), ("522110", 0.06)]
IDR_NAICS = [("531120", "office"), ("518210", "flat"), ("622110", "hospital"), ("611310", "office"),
             ("326199", "plant"), ("325998", "plant"), ("332312", "plant"), ("493110", "warehouse"),
             ("423830", "warehouse"), ("452311", "retail"), ("721110", "hospital"), ("336390", "plant")]
IDR_NAICS_P = [0.17, 0.06, 0.08, 0.06, 0.09, 0.07, 0.08, 0.13, 0.08, 0.08, 0.04, 0.06]

PLANS_PROF = ["BIZ-FX12", "BIZ-FX24", "BIZ-FX36", "BIZ-IDX12"]
PLANS_IDR = ["LCI-FX24", "LCI-FX36", "LCI-IDX12", "LCI-BLK36"]
AGE = ["pre-1980", "1980-1999", "2000-2014", "2015+"]

# the fourteen Business Saver members: book, kW, firm level share, uncalled share, start, NAICS, account, customer
MEMBERS = [
    ("Coast", 2150.0, 0.612, 0.9012, date(2011, 4, 18), "493120", "SC-4410286", "Gulf Prairie Cold Storage LLC"),
    ("Coast", 1480.0, 0.574, 0.8987, date(2014, 9, 2), "493120", "SC-4415733", "Tidewater Freezer Terminal Inc"),
    ("Coast", 980.0, 0.637, 0.8992, date(2022, 11, 14), "493120", "SC-4471160", "Cedar Bayou Cold Chain LP"),
    ("East", 1320.0, 0.589, 0.9031, date(2012, 2, 6), "493120", "SC-4411902", "Piney Woods Refrigerated Warehousing LLC"),
    ("Far West", 860.0, 0.648, 0.8975, date(2013, 6, 24), "312113", "SC-4413018", "Monahans Draw Ice Co"),
    ("North", 740.0, 0.556, 0.9038, date(2015, 3, 9), "312113", "SC-4416245", "Sulphur Fork Ice Company"),
    ("North Central", 2400.0, 0.600, 0.9000, date(2010, 8, 16), "493120", "SC-4409517", "Trinity Bottoms Freezer Terminal LLC"),
    ("North Central", 1920.0, 0.583, 0.9017, date(2012, 10, 1), "493120", "SC-4412266", "Mountain Creek Cold Storage Inc"),
    ("North Central", 1130.0, 0.621, 0.8981, date(2016, 1, 11), "493120", "SC-4419080", "Lakeview Frozen Logistics LLC"),
    ("South Central", 1760.0, 0.597, 0.9024, date(2009, 5, 26), "312113", "SC-4407731", "Cibolo Ice Works"),
    ("South Central", 1240.0, 0.628, 0.8969, date(2020, 3, 2), "493120", "SC-4458812", "Balcones Cold Storage LLC"),
    ("Southern", 2210.0, 0.594, 0.9006, date(2010, 11, 8), "493120", "SC-4410286", "Gulf Prairie Cold Storage LLC"),
    ("Southern", 1690.0, 0.606, 0.8994, date(2014, 4, 21), "312113", "SC-4407731", "Cibolo Ice Works"),
    ("West", 1720.0, 0.581, 0.9010, date(2018, 10, 22), "493120", "SC-4451507", "Concho Valley Cold Storage LLC"),
]
TWIN_COLD = 6        # index of the NC 2,400 kW cold store in MEMBERS
CENTRE_TOTAL_KW = 186_000.0
N_CENTRES = 31
AMEND_TARGET_KW = 275_000.0
AMEND_BROKER = "B417"


def _years(d0: date, d1: date) -> float:
    return (d1 - d0).days / 365.25


def target_md(book: str, d: date) -> float:
    """Growth path of the book's dedup MD in kW (centres excluded)."""
    return M27[book] * 1000.0 * (1 + GROWTH[book]) ** (-_years(d, EXTRACT))


class Builder:
    def __init__(self, rng):
        self.rng = rng
        self.rows = []
        self.used_esi = set()
        self.bad_days = set()
        for y, (d, _, _) in PEAKS.items():
            for k in (-1, 0, 1):
                self.bad_days.add(d + timedelta(days=k))
        for k in range(-3, 1):
            self.bad_days.add(EXTRACT + timedelta(days=k))

    def esi(self, tdsp):
        p = ESI_PREFIX[tdsp]
        while True:
            tail = "".join(str(int(x)) for x in self.rng.integers(0, 10, 17 - len(p)))
            e = p + tail
            if e not in self.used_esi and tail[0] != "0":
                self.used_esi.add(e)
                return e

    def tdsp(self, book):
        opts = TDSP_OF[book]
        names, w = [o[0] for o in opts], np.array([o[1] for o in opts])
        return names[int(self.rng.choice(len(names), p=w / w.sum()))]

    def clean_day(self, d: date) -> date:
        while d in self.bad_days:
            d += timedelta(days=-4 if d >= EXTRACT - timedelta(days=3) else 3)
        return d

    def add(self, **kw):
        self.rows.append(kw)


def _draw_md(rng, comp):
    if comp == "prof":
        return float(np.clip(np.round(rng.lognormal(np.log(78.0), 0.75), 1), 14.0, 680.0))
    return float(np.clip(np.round(rng.lognormal(np.log(1850.0), 0.45), 0), 720.0, 6400.0))


def _populate(B: Builder, book: str, comp: str, share: float, tenure_years: float, extra_active=None):
    """Greedy month-by-month tracking of the component's MD path, with exponential tenures."""
    rng = B.rng
    d0 = date(2015, 1, 1)
    active = []  # (end_date or None, md)

    def tgt(d):
        return share * target_md(book, d)

    def new(start, init=False):
        md = _draw_md(rng, comp)
        start = B.clean_day(start)
        ten = rng.exponential(tenure_years * 365.25)
        end = start + timedelta(days=int(ten))
        if init and end < d0:
            end = d0 + timedelta(days=int(rng.exponential(tenure_years * 365.25)))
        end = B.clean_day(end)
        rec = {"book": book, "comp": comp, "md_kw": md, "start": start, "end": end if end <= EXTRACT else None}
        B.add(**rec)
        active.append((rec["end"], md))
        return md

    tot = 0.0
    while tot < tgt(d0):
        s = date(2008, 1, 1) + timedelta(days=int(rng.integers(0, (d0 - date(2008, 1, 1)).days)))
        tot += new(s, init=True)
    m = d0
    while m <= EXTRACT:
        nxt = (m.replace(day=28) + timedelta(days=4)).replace(day=1)
        end_m = min(nxt - timedelta(days=1), EXTRACT)
        cur = sum(md for e, md in active if e is None or e > end_m)
        goal = tgt(end_m) * (1 + rng.normal(0, 0.002))
        while cur < goal:
            span = (end_m - m).days + 1
            s = m + timedelta(days=int(rng.integers(0, span)))
            cur += new(s)
        m = nxt


def build_premises(rng) -> pd.DataFrame:
    B = Builder(rng)
    for book in BOOKS:
        mem_kw = sum(x[1] for x in MEMBERS if x[0] == book)
        mshare = mem_kw / (M27[book] * 1000.0)
        _populate(B, book, "idr", IDR_SHARE[book], 9.0)
        _populate(B, book, "prof", 1.0 - IDR_SHARE[book] - mshare - (0.0021 if book == NC else 0.0), 10.0)
    df = pd.DataFrame(B.rows)
    # members
    mem = []
    for i, (book, md, phi, u, start, naics, acct, cust) in enumerate(MEMBERS):
        mem.append({"book": book, "comp": "ref", "md_kw": md, "start": start, "end": None, "member": i,
                    "phi": phi, "u": u, "naics": naics, "account": acct, "customer": cust})
    # the twin warehouse: identical enrolment columns to the NC cold store
    twin = {"book": NC, "comp": "idr", "md_kw": 2400.0, "start": MEMBERS[TWIN_COLD][4], "end": None, "twin": True,
            "naics": "493110", "customer": "Midcities Dry Goods Terminal LLC"}
    # Harlan Ridge's 31 centres, service from February and March 2027
    kws = rng.uniform(3800, 8400, N_CENTRES)
    kws = np.round(kws / kws.sum() * CENTRE_TOTAL_KW, 0)
    kws[-1] += CENTRE_TOTAL_KW - kws.sum()
    cen = []
    for j in range(N_CENTRES):
        st = date(2027, 2, 15) + timedelta(days=int(rng.integers(0, 40)))
        cen.append({"book": NC, "comp": "centre", "md_kw": float(kws[j]), "start": st, "end": None,
                    "naics": "493120", "customer": "Harlan Ridge Cold Storage Partners LP", "centre": j})
    df = pd.concat([df, pd.DataFrame(mem), pd.DataFrame([twin]), pd.DataFrame(cen)], ignore_index=True)
    for c in ("member", "centre"):
        df[c] = df[c].astype("Int64")
    df["twin"] = df["twin"].fillna(False).astype(bool)
    # attributes
    n = len(df)
    df["tdsp"] = [B.tdsp(b) for b in df["book"]]
    df.loc[df["comp"].isin(["centre"]) | df["twin"] | (df["member"] == TWIN_COLD), "tdsp"] = "ONCOR"
    df["esi_id"] = [B.esi(t) for t in df["tdsp"]]
    pn = [x[0] for x in PROFILED_NAICS]
    pw = np.array([x[1] for x in PROFILED_NAICS]); pw = pw / pw.sum()
    iw = np.array(IDR_NAICS_P); iw = iw / iw.sum()
    fam = dict(IDR_NAICS)
    nai, famcol = [], []
    for comp, nx in zip(df["comp"], df["naics"]):
        if isinstance(nx, str):
            nai.append(nx); famcol.append("warehouse" if nx == "493110" else "ref")
        elif comp == "prof":
            nai.append(pn[int(rng.choice(len(pn), p=pw))]); famcol.append("")
        else:
            k = int(rng.choice(len(IDR_NAICS), p=iw)); nai.append(IDR_NAICS[k][0]); famcol.append(IDR_NAICS[k][1])
    df["naics"] = nai
    df["family"] = famcol
    df["meter"] = np.where(df["comp"] == "prof", "AMS", "IDR")
    df["plan"] = [str(rng.choice(PLANS_PROF)) if c == "prof" else str(rng.choice(PLANS_IDR)) for c in df["comp"]]
    df["deposit"] = [str(rng.choice(["A", "B", "C", "W"], p=[0.45, 0.3, 0.15, 0.1])) for _ in range(n)]
    df["age_band"] = [str(rng.choice(AGE, p=[0.18, 0.34, 0.33, 0.15])) for _ in range(n)]
    df.loc[df["comp"] == "centre", ["plan", "deposit", "age_band"]] = ["LCI-FX36", "A", "2015+"]
    tw = df["twin"] | (df["member"] == TWIN_COLD)
    df.loc[tw, ["plan", "deposit", "age_band", "meter"]] = ["LCI-FX36", "B", "2000-2014", "IDR"]
    df["broker"] = [str(rng.choice(["", "", "B102", "B230", "B417", "B588"])) for _ in range(n)]
    df.loc[df["comp"] == "centre", "broker"] = "B230"
    df.loc[tw, "broker"] = ""
    df["record_type"] = "NEW"
    lag = rng.integers(3, 25, n)
    df["entered_on"] = [s - timedelta(days=int(k)) for s, k in zip(df["start"], lag)]
    df.loc[tw, "entered_on"] = MEMBERS[TWIN_COLD][4] - timedelta(days=12)
    df["supersedes"] = None
    return df


def add_amendments(rng, df: pd.DataFrame) -> pd.DataFrame:
    """The March 2027 re-papering run: one broker's North Central small commercial accounts, each re-entered as an
    AMEND row on the same ESI ID with the same maximum demand; the NEW row stays open."""
    pool = df[(df["book"] == NC) & (df["comp"] == "prof") & df["end"].isna() & (df["start"] < date(2026, 12, 1))]
    idx = rng.permutation(pool.index.to_numpy())
    pick, tot = [], 0.0
    for i in idx:
        if tot >= AMEND_TARGET_KW:
            break
        pick.append(i)
        tot += df.at[i, "md_kw"]
    am = df.loc[pick].copy()
    am["record_type"] = "AMEND"
    am["broker"] = AMEND_BROKER
    ent = [date(2027, 3, 8) + timedelta(days=int(k)) for k in rng.integers(0, 12, len(am))]
    am["entered_on"] = ent
    am["start"] = [e + timedelta(days=int(k)) for e, k in zip(ent, rng.integers(1, 9, len(am)))]
    am["plan"] = [p.replace("FX36", "FX24").replace("FX12", "FX24") if "FX" in p else "BIZ-FX24" for p in am["plan"]]
    am["amend_of"] = am.index
    out = pd.concat([df, am], ignore_index=True)
    out["amend_of"] = out["amend_of"].astype("Int64")
    return out


def assign_ids(rng, df: pd.DataFrame) -> pd.DataFrame:
    order = np.lexsort((df["esi_id"].to_numpy(), np.array([d.toordinal() for d in df["entered_on"]])))
    df = df.iloc[order].reset_index(drop=True)
    ids = 300_118_000 + np.cumsum(rng.integers(1, 9, len(df)))
    df["enrollment_id"] = ["EN" + str(x) for x in ids]
    return df


def md_on(df: pd.DataFrame, d: date, dedup=True) -> pd.Series:
    """MD (kW) enrolled per book on day d: rows with start <= d <= end (open rows have no end)."""
    act = df[(df["start"] <= d) & (df["end"].isna() | (df["end"].map(lambda e: e is not None and e >= d)))]
    if dedup:
        act = act[act["record_type"] == "NEW"]
    return act.groupby("book")["md_kw"].sum().reindex(BOOKS).fillna(0.0)
