"""The golden and every rung, from the generator's state: the conversion at each glass reading (the mean probe-minus-
glass difference at that reading across the parallel observations), the counts, the lines and the premium; the two
asks; and the figures the write-up states."""
import collections

import numpy as np

import book as B
import climate as C
import pricing as P
import world as W


def world_state():
    mf = C.merrin_flat()
    pairs = C.comparison()
    mem = B.members()
    bl = B.blocks(mem)
    heat_raw, sev_raw = P.counts(P.basis_series(mf, P.uniform(0.0)))
    reg, ledger = B.claims(bl, mem, heat_raw, sev_raw)
    return {"mf": mf, "pairs": pairs, "members": mem, "blocks": bl, "claims": reg, "ledger": ledger}


def conversions(pairs):
    pooled = P.bin_conversion([(g, p) for s, d, g, p in pairs])
    mf_only = P.bin_conversion([(g, p) for s, d, g, p in pairs if s == "MF"])
    mf_rows = [(d, g, p) for s, d, g, p in pairs if s == "MF"]
    diffs = np.array([p - g for d, g, p in mf_rows])
    gl = np.array([g for d, g, p in mf_rows])
    summer = np.array([p - g for d, g, p in mf_rows if d.month in (12, 1, 2)])
    slope, icept = np.polyfit(gl, diffs, 1)
    return {"pooled": pooled, "mf_only": mf_only, "mean": float(diffs.mean()), "summer": float(summer.mean()),
            "linear": (float(icept), float(slope)),
            "hot33": float(diffs[gl >= 33].mean()), "hot35": float(diffs[gl >= 35].mean())}


def main_call(st):
    cv = conversions(st["pairs"])
    mf = st["mf"]
    gold_h, gold_s, gold = P.rung(mf, P.converter(cv["pooled"]))
    raw_h, raw_s, raw = P.rung(mf, P.uniform(0.0))
    ic, sl = cv["linear"]
    rungs = {
        "R0 no conversion": raw,
        "R1 mean difference": P.rung(mf, P.uniform(cv["mean"]))[2],
        "R2 summer mean difference": P.rung(mf, P.uniform(cv["summer"]))[2],
        "R2 linear fit over all days": P.rung(mf, lambda g: g + ic + sl * g)[2],
        "R3 one offset, glass at 33 C or more": P.rung(mf, P.uniform(cv["hot33"]))[2],
        "R3 one offset, glass at 35 C or more": P.rung(mf, P.uniform(cv["hot35"]))[2],
        "R4 at each reading, pooled": gold,
        "R4 at each reading, Merrin Flat only": P.rung(mf, P.converter(cv["mf_only"]))[2],
    }
    glass_seasons = [s for s in P.SEASONS if s < W.CHANGE.year]
    return {"conv": cv, "golden": gold, "heat": gold_h, "severe": gold_s, "raw": raw, "raw_heat": raw_h,
            "raw_severe": raw_s, "rungs": rungs,
            "moved_heat": sum(gold_h[s] - raw_h[s] for s in glass_seasons),
            "moved_severe": sum(gold_s[s] - raw_s[s] for s in glass_seasons)}


def ask_a(st, rate):
    ins = B.schedule_2027(st["blocks"])
    out = {}
    for sd in W.SUB_DISTRICTS:
        bs = [b for b in ins if b.district_new == sd]
        ha = round(sum(b.area for b in bs), 1)
        out[sd] = {"blocks": len(bs), "ha": ha, "premium": P.r_dollar(rate * ha)}
    return out


def ask_b(st):
    paid = collections.defaultdict(float)
    claim_season = {}
    for r in st["claims"]:
        claim_season[r["claim_no"]] = r["season"]
    for p in st["ledger"]:
        paid[p["claim_no"]] += p["amount"]
    out = {}
    for s in range(W.COVER_FIRST_SEASON, W.LAST_SEASON + 1):
        lab = W.season_label(s)
        nos = [c for c, v in paid.items() if claim_season[c] == lab]
        out[lab] = {"claims": len(nos), "amount": P.r_dollar(sum(paid[c] for c in nos))}
    return out


def figures(st):
    mc = main_call(st)
    g = mc["golden"]
    a = ask_a(st, g["premium"])
    b = ask_b(st)
    return {
        "call_premium_per_ha": g["premium"],
        "expected_heat_days_2027_28": "%.1f" % g["expected_heat"],
        "expected_severe_days_2027_28": "%.1f" % g["expected_severe"],
        "heat_line_slope_days_per_decade": "%.2f" % g["slope_heat_decade"],
        "severe_line_slope_days_per_decade": "%.2f" % g["slope_severe_decade"],
        "glass_era_heat_days_added": mc["moved_heat"],
        "glass_era_severe_days_added": mc["moved_severe"],
        "default_premium_per_ha": mc["rungs"]["R1 mean difference"]["premium"],
        "default_expected_heat_days": "%.1f" % mc["rungs"]["R1 mean difference"]["expected_heat"],
        "default_heat_line_slope_days_per_decade": "%.2f" % mc["rungs"]["R1 mean difference"]["slope_heat_decade"],
        "conversion_at_34_5": "%.2f" % mc["conv"]["pooled"][34.5],
        "conversion_at_39_0": "%.2f" % mc["conv"]["pooled"][39.0],
        "mean_conversion_merrin_flat": "%.2f" % mc["conv"]["mean"],
        "sub_districts": a,
        "insured_ha_total": "%.1f" % sum(v["ha"] for v in a.values()),
        "blocks_total": sum(v["blocks"] for v in a.values()),
        "seasons": b,
        "heat_trigger_c": "%.1f" % W.HEAT_C,
        "severe_trigger_c": "%.1f" % W.SEVERE_C,
        "glass_readings_first_over_each_trigger": ["%.1f" % min(k for k in mc["conv"]["pooled"] if k + mc["conv"]["pooled"][k] >= W.HEAT_C and k < W.HEAT_C),
                                                   "%.1f" % min(k for k in mc["conv"]["pooled"] if k + mc["conv"]["pooled"][k] >= W.SEVERE_C and k < W.SEVERE_C)],
        "seasons_in_record": len(P.SEASONS),
        "loading": "%.2f" % W.LOADING,
    }
