"""The golden pipeline on the clean truth: every rung, the call, the flip point, the published 2025 table and the 2024
ask, as the figures every deliverable and the write-up carry."""
import numpy as np

import asks as A
import estim as E
import pack as P
import world as W

GOLDEN = "G_icc"            # the report's published intraclass correlation, projected area by area
FAMILY = ["G_icc", "G_anova", "G_reml", "G_kish_recomputed"]
CALL_ONLY = ["G_pubbase", "G_unfloored", "G_wanova", "G_design", "G_strata"]   # readings a filed sentence rules out; each keeps the call
CHEAP = {"R1": 1, "R2": 3, "R3": 3, "R3_icc": 3, "R3_anova": 3, "R3_reml": 3}      # each cheap route and the region it names


def flip_runner(rows_runner, target):
    """The smallest whole number of extra interviews per area at which the runner-up's boost removes a larger share
    than the target, with the runner-up's published intraclass correlation."""
    sb, sw = E.anova(rows_runner)
    icc = round(max(sb / (sb + sw), 0.0), 3)
    for d in range(1, 400):
        if E.icc_share(rows_runner, icc, float(d)) > target:
            return d, E.icc_share(rows_runner, icc, float(d - 1)), E.icc_share(rows_runner, icc, float(d))
    raise ValueError("no flip")


def main_call(w):
    tab = W.wave_table(w, 2025)
    res = {r: E.routes(tab[r]) for r in (1, 2, 3, 4, 5)}
    order = sorted(res, key=lambda r: -res[r][GOLDEN])
    call, runner = order[0], order[1]
    k_runner = len(tab[runner])
    d, below, at = flip_runner(tab[runner], res[call][GOLDEN])
    published = []
    for r in (1, 2, 3, 4, 5):
        p, v = E.design_var(tab[r])
        published.append(dict(region=W.RNAME[r], n=sum(len(x["y"]) for x in tab[r]), est=100 * p,
                              se=100 * np.sqrt(v), deff=E.deff(tab[r]), icc=res[r]["_"]["icc_pub"]))
    design = []
    for r in (1, 2, 3, 4, 5):
        strata = sorted(set(x["stratum"] for x in tab[r]))
        design.append(dict(region=W.RNAME[r], strata="2 (core, supplement)" if len(strata) > 1 else "1",
                           areas=len(tab[r]), completes=sum(x["m_all"] for x in tab[r])))
    return dict(tab=tab, res=res, call=call, runner=runner, order=order, flip_per_area=d,
                flip_interviews=d * k_runner, flip_below=below, flip_at=at, published=published, design=design)


def response_rate_text(w):
    """The 2025 share of eligible released dwellings giving a complete interview, for the report's sentence."""
    elig = comp = 0
    for c in w["cases"][2025]:
        if c["cls"] in (W.VACANT, W.WITHDRAWN) or c["reissue_of"] is not None:
            continue
        elig += 1
        comp += c["cls"] in (W.COMPLETE, W.PROXY)
    conv = sum(1 for c in w["cases"][2025] if c["reissue_of"] is not None and c["cls"] in (W.COMPLETE, W.PROXY))
    return "%.1f per cent" % (100.0 * (comp + conv) / elig)


def ask_2024(w):
    out = {h: A.figures_2024(w, h, P.code_at) for h in A.HANDLINGS}
    return out
