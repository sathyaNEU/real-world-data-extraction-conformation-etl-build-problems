"""Every figure the build owes, computed forward from the world's samples and the meters: the call and its
components, the rungs and the grid, the asks under the golden handling and under every mishandling."""
import datetime as dt
import itertools
import math

import numpy as np

import asks as A
import core


def gpm_gap(use):
    return use / 1440.0 - core.FIRM


def call_of(use):
    g = gpm_gap(use)
    return None if g <= 0 else int(math.ceil(g))


def main_figures(W):
    Bal, H = W["Bal"], W["H"]
    days, P, U = Bal["days"], Bal["P"], Bal["U"]
    ig, i0 = int(np.argmax(U)), int(np.argmax(P))
    gap = gpm_gap(U[ig])
    F = dict(days=days, P=P, U=U, dS=Bal["dS"], gold_day=days[ig], gold_use=int(U[ig]), gold_P=int(P[ig]),
             gold_dS=int(Bal["dS"][ig]), gold_dSm=int(Bal["dSm"][ig]), gap=gap, call=call_of(U[ig]),
             call_round=int(round(gap)), firm=core.FIRM, firm_gal=core.FIRM * 1440, tested=dict(core.TESTED),
             largest=core.LARGEST)
    # rungs
    F["R0"] = dict(day=days[i0], figure=int(P[i0]), gap=gpm_gap(P[i0]), call=call_of(P[i0]))
    iu = int(np.nanargmax(Bal["Um"]))
    F["R1"] = dict(day=days[iu], figure=int(Bal["Um"][iu]), gap=gpm_gap(Bal["Um"][iu]), call=call_of(Bal["Um"][iu]))
    j = int(np.nanargmax(Bal["Uu"]))
    F["R2"] = dict(day=days[j], figure=int(Bal["Uu"][j]), gap=gpm_gap(Bal["Uu"][j]), call=call_of(Bal["Uu"][j]))
    k = int(np.nanargmax(Bal["Ub"]))
    F["R3"] = dict(day=days[k], figure=int(round(Bal["Ub"][k])), gap=gpm_gap(Bal["Ub"][k]), call=call_of(Bal["Ub"][k]))
    F["gold_prod_rank"] = int((P > P[ig]).sum()) + 1
    srt = np.sort(U)
    F["second_use"] = int(srt[-2])
    F["second_ratio"] = float(srt[-2] / srt[-1])
    F["grid"] = grid(W)
    F["rolling"] = rolling_max(W)
    return F


def grid(W):
    """Three constructions by three clocks; production alone has no storage term."""
    H, Bal = W["H"], W["Bal"]
    t = H["t"]
    pos = {x: i for i, x in enumerate(t)}
    store = {tk: (core.GPF[tk] // 100) * np.round(H["lev"][tk] * 100).astype(np.int64) for tk in core.TANKS}
    S = {"all": sum(store.values()), "main": store["A"] + store["B"], "none": np.zeros(len(t), dtype=np.int64)}
    tot = np.zeros(len(t), dtype=np.int64)
    for w in core.WELLS:
        g = H["tot"][w].astype(np.int64).copy()
        if w == "W3":
            wrap = np.concatenate([[0], np.cumsum(np.diff(g) < 0)])
            g = g + wrap * core.W3_REGISTER
        tot += g
    out = {}
    days = core.eval_days()
    for clock in ("local", "utc", "est", "mean"):
        for cons in ("none", "main", "all"):
            if clock == "mean" and cons == "none":
                continue
            vals = []
            for d in days:
                if clock == "local":
                    a = Bal["by_date"][d]
                    b = Bal["by_date"][d + dt.timedelta(1)]
                    v = (tot[b] - tot[a]) - (S[cons][b] - S[cons][a])
                elif clock in ("utc", "est"):
                    ta = dt.datetime(d.year, d.month, d.day, tzinfo=core.UTC) + dt.timedelta(hours=5 if clock == "est" else 0)
                    if ta not in pos or ta + dt.timedelta(1) not in pos:
                        continue
                    a, b = pos[ta], pos[ta + dt.timedelta(1)]
                    v = (tot[b] - tot[a]) - (S[cons][b] - S[cons][a])
                else:
                    a = Bal["by_date"][d]
                    b = Bal["by_date"][d + dt.timedelta(1)]
                    c = Bal["by_date"].get(d + dt.timedelta(2), b + 24)
                    v = (tot[b] - tot[a]) - (S[cons][b:c].mean() - S[cons][a:b].mean())
                vals.append((v, d))
            v, d = max(vals)
            out[(cons, clock)] = dict(day=d, figure=float(v), gap=gpm_gap(v), call=call_of(v))
    return out


def rolling_max(W):
    """The most water used in any 24 consecutive hours (hourly samples), for SF2."""
    H, Bal = W["H"], W["Bal"]
    store = {tk: (core.GPF[tk] // 100) * np.round(H["lev"][tk] * 100).astype(np.int64) for tk in core.TANKS}
    S = sum(store.values())
    tot = np.zeros(len(H["t"]), dtype=np.int64)
    for w in core.WELLS:
        g = H["tot"][w].astype(np.int64).copy()
        if w == "W3":
            g = g + np.concatenate([[0], np.cumsum(np.diff(g) < 0)]) * core.W3_REGISTER
        tot += g
    a0 = Bal["by_date"][core.EVAL0]
    a1 = Bal["by_date"][core.EVAL1 + dt.timedelta(1)]
    best = (-1, None)
    for a in range(a0, a1 - 24 + 1):
        v = (tot[a + 24] - tot[a]) - (S[a + 24] - S[a])
        if v > best[0]:
            best = (int(v), H["t"][a])
    return dict(figure=best[0], start=best[1], gap=gpm_gap(best[0]))


def ask_figures(W, final):
    G = A.figures(W, final)
    gold = dict(lost=[int(x) for x in G["lost"]], year=G["year"], share=G["share"], used=[int(x) for x in G["used"]],
                metered=[int(x) for x in G["metered"]], used_year=G["used_year"], groups=dict(G["groups"]))
    G["gold"] = gold
    G["share_r"] = "%.1f" % G["share"]
    return G


def compositions(G):
    """Every subset of mishandlings: (subs, vault dropped, partials dropped, multipliers ignored, production as use)
    for Ask L, and (subs, vault, partials, multipliers, P2) for Ask C, each figure set against the golden."""
    gold = G["gold"]
    cells = []
    for key, st in G["stops"].items():
        if key == (False, True, True, True, "used"):
            continue
        for k in range(12):
            cells.append(("L", key, "month %d" % k, abs(int(st["lost"][k]) - gold["lost"][k])))
        cells.append(("L", key, "year", abs(st["year"] - gold["year"])))
        cells.append(("L", key, "share", abs(round(st["share"], 1) - round(gold["share"], 1))))
    for key, gr in G["gstops"].items():
        if key == (False, True, True, True, "golden"):
            continue
        for g in A.GROUPS:
            cells.append(("C", key, g, abs(gr[g] - gold["groups"][g])))
    return cells
