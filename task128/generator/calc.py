"""The golden arithmetic, from the shipped files only (shared by golden.py and checks.py; verify.py has its own)."""
import datetime as dt
import os

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

import pack as P

YEAR_FROM, YEAR_TO = dt.date(2025, 7, 1), dt.date(2026, 6, 30)
NEW_TEAM = 400
BAR = 694
RPC_CODES = {"RPC", "PTP", "ARR", "RTP", "CBK"}
CENTRES = ["TBY", "SUD", "KGN", "LON", "WPG"]
NAMES = {"TBY": "Thunder Bay", "SUD": "Sudbury", "KGN": "Kingston", "LON": "London", "WPG": "Winnipeg"}


def load(target):
    L = pd.read_csv(os.path.join(target, P.FILES["lists"]), dtype={"ACCT_NO": str, "CYCLE_CD": str, "RESULT_CD": str},
                    keep_default_na=False)
    L["day"] = pd.to_datetime(L.LIST_DT).dt.date
    H = pq.read_table(os.path.join(target, P.FILES["history"])).to_pandas()
    H["CYCLE_DT"] = pd.to_datetime(H.CYCLE_DT).dt.date
    return L, H


def outcomes(L, H):
    """rolled: 90 or more days past due on the record's cycle date two months after its list day (CP-14 6.3)."""
    cd = H.groupby(["CYCLE_CD", H.CYCLE_DT.map(lambda d: (d.year, d.month))]).CYCLE_DT.first()
    def plus2(day, cyc):
        y, m = day.year, day.month + 2
        y, m = y + (m - 1) // 12, (m - 1) % 12 + 1
        return cd.get((cyc, (y, m)))
    L = L.copy()
    L["out_dt"] = [plus2(d, c) for d, c in zip(L.day.values, L.CYCLE_CD.values)]
    late = H[H.DPD >= 90][["ACCT_NO", "CYCLE_DT"]].drop_duplicates()
    late["roll"] = True
    L = L.merge(late, left_on=["ACCT_NO", "out_dt"], right_on=["ACCT_NO", "CYCLE_DT"], how="left").drop(columns="CYCLE_DT")
    L["roll"] = L.roll.fillna(False).astype(bool)
    return L


def status(L):
    L = L.copy()
    L["left"] = L.RESULT_CD == ""
    L["skipped"] = L.RESULT_CD.isin(["DNC", "NDN"])
    L["dialled"] = ~L.left & ~L.skipped
    L["reached_by_dialler"] = ~L.left
    return L


def sizing(L, frm=YEAR_FROM, to=YEAR_TO):
    """Per centre: the over-capacity list days, the records left at shift end, the share of the reached records the
    dialler skipped, a dial's effect from the same-list comparison, the new team's dials and the rolls they prevent."""
    Y = L[(L.day >= frm) & (L.day <= to)]
    out = {}
    for c in CENTRES:
        D = Y[Y.CENTRE_CD == c]
        over_days = sorted(D[D.left].day.unique())
        ov = D[D.day.isin(over_days)]
        g = ov.groupby(["day", "left"]).roll.agg(["sum", "size"]).unstack("left")
        rb = g[("sum", True)] / g[("size", True)]
        ra = g[("sum", False)] / g[("size", False)]
        nb = g[("size", True)]
        itt = float((nb * (rb - ra)).sum() / nb.sum())
        reached = ov[~ov.left]
        s = float(reached.skipped.mean())
        per_dial = itt / (1 - s)
        dials = float(np.minimum((1 - s) * nb, NEW_TEAM).sum())
        out[c] = dict(over_days=len(over_days), left=int(nb.sum()), skip_share=s, itt=itt, per_dial=per_dial,
                      dials=dials, rolls=per_dial * dials, bind_lo=float(((1 - s) * nb).min() / NEW_TEAM),
                      bind_hi=float(((1 - s) * nb).max() / NEW_TEAM))
    return out


def upgrade_days(target):
    W = pd.read_csv(os.path.join(target, P.FILES["worklog"]), dtype=str, keep_default_na=False)
    W["day"] = pd.to_datetime(W.WORK_DT).dt.date
    return {c: min(W[(W.CENTRE_CD == c) & (W.DIALLER_VER == "CX2.1")].day) for c in CENTRES}


def contacts(L, up):
    """Right-party contacts per 100 accounts dialled and promises to pay per 100 right-party contacts, the review
    year; before a centre's upgrade AR was the old dialler's arrangement code."""
    Y = L[(L.day >= YEAR_FROM) & (L.day <= YEAR_TO) & L.dialled]
    out = {}
    for c in CENTRES:
        D = Y[Y.CENTRE_CD == c]
        pre = D.day < up[c]
        rpc = D.RESULT_CD.isin(RPC_CODES) | ((D.RESULT_CD == "AR") & pre)
        ptp = D.RESULT_CD == "PTP"
        out[c] = dict(dialled=len(D), rpc=int(rpc.sum()), ptp=int(ptp.sum()),
                      rpc_rate=100.0 * rpc.sum() / len(D), ptp_rate=100.0 * ptp.sum() / rpc.sum())
    return out


def balances(target, H):
    A = pd.read_csv(os.path.join(target, P.FILES["arrangements"]), dtype={"ACCT_NO": str}, keep_default_na=False)
    A["setup"] = pd.to_datetime(A.SETUP_DT).dt.date
    R = pd.read_csv(os.path.join(target, P.FILES["rates"]), dtype=str)
    rate = dict(zip(pd.to_datetime(R.RATE_DT).dt.date, R.BOOKING_RATE.astype(float)))
    prod = H.drop_duplicates("ACCT_NO").set_index("ACCT_NO").PRODUCT_CD
    A["usd"] = A.ACCT_NO.map(prod).eq("VUSD")
    A = A[(A.setup >= YEAR_FROM) & (A.setup <= YEAR_TO)]
    A["cad"] = np.where(A.usd, A.ARR_BAL.astype(float) * A.setup.map(rate), A.ARR_BAL.astype(float))
    out = {}
    for c in CENTRES:
        D = A[A.CENTRE_CD == c]
        out[c] = dict(n=len(D), usd_n=int(D.usd.sum()), cad=float(D.cad.sum()), as_cad=float(D.ARR_BAL.astype(float).sum()))
    return out


def r100(x):
    return int(np.floor(x / 100.0 + 0.5) * 100)


def r100k(x):
    return int(np.floor(x / 100000.0 + 0.5) * 100000)


def r1(x):
    return float(np.floor(x * 10 + 0.5) / 10)


def everything(target):
    L, H = load(target)
    L = status(outcomes(L, H))
    up = upgrade_days(target)
    return dict(L=L, H=H, size=sizing(L), contacts=contacts(L, up), balances=balances(target, H), upgrade=up)
