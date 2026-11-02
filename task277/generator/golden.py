"""The golden figures from the clean world: the 2026 record as Schedule 3 counts it, the February and March 2027
forecast (each planned line carried at the error probability of the pick it will call for once the Daily range is
held in inners of four), every lower rung's forecast, and the store claims in units by customer and quarter of
delivery."""
import numpy as np
import pandas as pd

import params as P
import world as W

GROUP_ORDER = ["RAV", "HGH", "VLM", "ZLF"]


def nearest(x, step):
    return int(step * np.floor(x / step + 0.5))


def picked(w):
    L = w["lines"]
    pk = L[L["qty_conf"] > 0].copy()
    inner27 = np.array([P.INNER_2027.get(r, i) for r, i in zip(pk["range"].values, pk["inner"].values)])
    pk["inner27"] = inner27
    pk["s27"] = W.structure(pk["qty_conf"].values, inner27)
    return pk


def history(w):
    pk = picked(w)
    g = pk.groupby("month").agg(lines=("fail", "size"), fails=("fail", "sum"))
    g["accuracy"] = 100.0 * (1 - g["fails"] / g["lines"])
    return g


def _apply(pl, ref, fn):
    tot = {"T": 0.0, "W": 0.0}
    for r in pl.itertuples():
        cell = ref[(ref["channel"] == r.channel) & (ref["range"] == r.range)]
        tot[r.channel] += r.lines * fn(cell, r.channel, r.range)
    return tot


def forecast(w):
    pk = picked(w)
    hep = pk.groupby("struct")["fail"].mean().to_dict()
    out = {}
    for m in (2, 3):
        pl = w["plan"][w["plan"]["month"] == m]
        ref = pk[pk["month"] == m]
        t = _apply(pl, ref, lambda c, ch, rg: c["s27"].map(hep).mean())
        n = {ch: int(pl[pl["channel"] == ch]["lines"].sum()) for ch in "TW"}
        tot = t["T"] + t["W"]
        acc = 100.0 * (1 - tot / (n["T"] + n["W"]))
        out[m] = dict(plan_T=n["T"], plan_W=n["W"], plan=n["T"] + n["W"], fail_T=t["T"], fail_W=t["W"], fail=tot,
                      accuracy=acc, holds=acc >= P.KPI)
    out["hep"] = hep
    return out


def rungs(w):
    """Every lower rung's forecast accuracy for February and March."""
    pk = picked(w)
    pk["op"] = pk["qty_conf"] % pk["inner"] != 0
    pk["op27"] = pk["qty_conf"] % pk["inner27"] != 0
    site = pk["fail"].mean()
    chr_ = pk.groupby(["channel", "range"])["fail"].mean()
    sm = pk[pk["month"].isin([2, 3])].groupby(["channel", "range"])["fail"].mean()
    ci = pk.groupby(["channel", "inner"])["fail"].mean()
    cq = pk.groupby(["channel", "qty_conf"])["fail"].agg(["mean", "size"])
    chm = pk.groupby("channel")["fail"].mean()
    co = pk.groupby(["channel", "op"])["fail"].mean()
    lu = pk["qty_conf"] % pk["inner"]
    coef = np.linalg.lstsq(np.c_[np.ones(len(pk)), lu], pk["fail"].astype(float), rcond=None)[0]
    rq = pk.groupby(["range", "qty_conf"])["fail"].agg(["mean", "size"])
    rr = pk.groupby("range")["fail"].mean()
    hep_ch = pk.groupby(["channel", "struct"])["fail"].mean()
    defs = {
        "R0 site rate": lambda c, ch, rg: site,
        "R1 channel and range": lambda c, ch, rg: chr_[(ch, rg)],
        "R1b same months of 2026": lambda c, ch, rg: sm[(ch, rg)],
        "R2a inner size": lambda c, ch, rg: ci.get((ch, int(c["inner27"].iloc[0])), site),
        "R2b channel and quantity": lambda c, ch, rg: np.mean([cq.loc[(ch, q), "mean"] if (ch, q) in cq.index and cq.loc[(ch, q), "size"] > 300 else chm[ch] for q in c["qty_conf"]]),
        "R2c opened inner": lambda c, ch, rg: np.mean([co[(ch, o)] for o in c["op27"]]),
        "R2d loose units": lambda c, ch, rg: float((coef[0] + coef[1] * (c["qty_conf"] % c["inner27"])).mean()),
        "R2e range and quantity": lambda c, ch, rg: np.mean([rq.loc[(rg, q), "mean"] if (rg, q) in rq.index and rq.loc[(rg, q), "size"] > 300 else rr[rg] for q in c["qty_conf"]]),
        "G by channel": lambda c, ch, rg: c["s27"].map(lambda s: hep_ch[(ch, s)]).mean(),
    }
    out = {}
    for name, fn in defs.items():
        out[name] = {}
        for m in (2, 3):
            pl = w["plan"][w["plan"]["month"] == m]
            t = _apply(pl, pk[pk["month"] == m], fn)
            n = pl["lines"].sum()
            out[name][m] = dict(fail=t["T"] + t["W"], accuracy=100.0 * (1 - (t["T"] + t["W"]) / n))
    return out


def claims_units(w):
    ev = w["events"]
    ok = ev[(ev["status"] == "Geaccepteerd") & ev["reason"].isin(["Tekort", "Teveel", "Verkeerd artikel"])].copy()
    ok["quarter"] = [(d.month - 1) // 3 + 1 for d in ok["delivery_date"]]
    ok = ok[[d.year == 2026 for d in ok["delivery_date"]]]
    g = ok.groupby(["group", "quarter"])["units"].sum()
    return {(gr, q): int(g.get((gr, q), 0)) for gr in GROUP_ORDER for q in (1, 2, 3, 4)}
