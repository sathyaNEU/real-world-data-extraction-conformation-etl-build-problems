"""The world's interruptions as the outage system records them (causes, devices, asset keys), before any file."""
import numpy as np
import pandas as pd

SEC_CAUSES = {"winter": (["TREE", "WIND", "ICE", "EQUIP", "UNKN", "VEH"], [0.22, 0.16, 0.18, 0.2, 0.14, 0.1]),
              "summer": (["TREE", "WIND", "LTNG", "EQUIP", "UNKN", "VEH"], [0.26, 0.2, 0.2, 0.16, 0.1, 0.08])}


def normalise(W, seed=4021):
    rng = np.random.default_rng(seed)
    E = W["E"].copy()
    n = len(E)
    month = (pd.Timestamp("2020-10-01") + pd.to_timedelta(E.d.values, "D")).month
    winter = np.isin(month, [11, 12, 1, 2, 3])
    cause = np.empty(n, dtype=object)
    k = E.kind.values
    for i in range(n):
        kk = k[i]
        if kk in ("base", "storm", "stormrep"):
            c, p = SEC_CAUSES["winter" if winter[i] else "summer"]
            cause[i] = rng.choice(c, p=p)
        elif kk == "xbg":
            t = E.temp.values[i]
            if (t < -18 or t > 28) and rng.random() < 0.08:
                cause[i] = "OVLD"
            else:
                cause[i] = rng.choice(["XFMR", "EQUIP", "ANML", "WTHR", "VEH", "UNKN"], p=[0.3, 0.25, 0.14, 0.16, 0.05, 0.1])
        elif kk.startswith("animal"):
            cause[i] = "ANML"
        elif kk.startswith("term"):
            cause[i] = "UGTERM"
        elif kk in ("hpovl", "retrip", "secovl"):
            cause[i] = "OVLD"
        elif kk in ("newunit", "oldunit"):
            cause[i] = "XFMR"
    F = pd.DataFrame(dict(sec=E.sec.values, level=np.where(E.xf.values >= 0, "transformer", "section"), xf=E.xf.values,
                          start=E.t0.values, end=E.t_end.values, ci=E.ci.values.astype(int), cause=cause, kind=k,
                          steps=E.steps.values, repair=E.repair.values, temp=E.temp.values))
    F["site"] = [int(x.split(":")[1]) if x.startswith("animal") else -1 for x in k]
    F["riser"] = [int(x.split(":")[1]) if x.startswith("term") else -1 for x in k]
    F["planned"] = False
    # planned work: weekday daytime, announced to the members affected; and the 1 June 2026 feeder transfers
    S, X = W["S"], W["X"]
    pl = []
    for d in range(365, 2191):
        wd = (pd.Timestamp("2020-10-01") + pd.Timedelta(days=d)).dayofweek
        if wd >= 5:
            continue
        for _ in range(rng.poisson(0.42)):
            if rng.random() < 0.7:
                xf = int(rng.integers(0, len(X)))
                pl.append((X.sec.values[xf], xf, d * 1440 + rng.uniform(540, 840), rng.uniform(45, 180), int(X.members.values[xf])))
            else:
                s = int(rng.integers(0, len(S)))
                pl.append((s, -1, d * 1440 + rng.uniform(540, 840), rng.uniform(30, 120), int(S.members.values[s])))
    dmv = (pd.Timestamp("2026-06-01") - pd.Timestamp("2020-10-01")).days
    for s in S.index[S.feeder_new != S.feeder]:
        pl.append((s, -1, dmv * 1440 + rng.uniform(360, 420), rng.uniform(40, 75), int(S.members.values[s])))
    PL = pd.DataFrame(pl, columns=["sec", "xf", "start", "repair", "ci"])
    PL["end"] = PL.start + PL.repair
    PL["level"] = np.where(PL.xf >= 0, "transformer", "section")
    PL["cause"] = "PLND"; PL["kind"] = "planned"; PL["steps"] = 1; PL["planned"] = True
    xfer = (PL.start // 1440 == dmv) & (PL.xf < 0) & PL.sec.isin(S.index[S.feeder_new != S.feeder])
    PL.loc[xfer, "cause"] = "XFER"; PL.loc[xfer, "kind"] = "transfer"
    PL["temp"] = W["dm"][(PL.start // 1440).astype(int).values]
    PL["site"] = -1; PL["riser"] = -1
    F["cmi"] = F.ci * (F.repair + (F.end - F.start - F.repair) / 2.0)
    PL["cmi"] = PL.ci * PL.repair
    F = pd.concat([F, PL[F.columns]], ignore_index=True)
    F = space(F, W["dm"])
    return F.sort_values("start").reset_index(drop=True)


def space(F, dm, seed=4029, near=35.0, held=25.0):
    """No independent fault starts in the half hour after a restoration on its section (the section's own device or one
    of its transformers): only a re-trip does. A fault the draws put there starts later the same way (40 to 120 minutes
    after), and a re-trip moves with the restoration it follows. Causes, durations and counts are kept."""
    rng = np.random.default_rng(seed)
    F = F.copy()
    nd = len(dm)
    for _ in range(50):
        # every fault at either level, against the latest restoration on its section (either level) before it starts
        last = F[["sec", "end", "start"]].assign(dur=F.end - F.start).sort_values("end")
        cand = F[~F.planned & (F.kind != "retrip")].sort_values("start")
        m = pd.merge_asof(cand[["start", "sec"]].reset_index(), last[["end", "sec", "dur"]].rename(columns={"end": "pend"}),
                          left_on="start", right_on="pend", by="sec", direction="backward")
        bad = m[(m.start - m.pend >= 0) & (m.start - m.pend <= near) & (m.dur >= held)]
        if not len(bad):
            break
        for i, pe in zip(bad["index"].values, bad.pend.values):
            if not (F.start[i] - pe <= near):
                continue
            dlt = pe + 40.0 + rng.uniform(0, 80) - F.start[i]
            kids = F.index[(F.kind == "retrip") & (F.sec == F.sec[i]) & (F.start >= F.end[i]) & (F.start < F.end[i] + 5.0)]
            for j in [i] + list(kids):
                F.loc[j, "start"] += dlt; F.loc[j, "end"] += dlt
                F.loc[j, "temp"] = dm[min(int(F.start[j] // 1440), nd - 1)]
    return F
