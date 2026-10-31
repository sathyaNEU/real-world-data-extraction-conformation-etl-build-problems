"""The capital arithmetic the capital policy files: the 1-in-200 annual windstorm loss gross, net of the occurrence
cover, and net of the occurrence cover with the second-event cover, each simulated storm costed at a load the caller
supplies. One function, used by the golden, the ladder, the checks and the verifier's own copy."""
import numpy as np


def programme(years, storms, loads, base, sec, n_years, rank):
    """years: year id (1..n) of each storm in date order within its year; storms: modelled losses; loads: the load on
    each storm. Returns the figures the capital policy reads, in pounds."""
    l = storms * loads
    gross = np.bincount(years, weights=l, minlength=n_years + 1)[1:]
    # the occurrence cover: each loss occurrence, one reinstatement at 100 per cent pro rata as to amount
    per = np.minimum(np.maximum(l - base["retention"], 0.0), base["limit"])
    rec = np.minimum(np.bincount(years, weights=per, minlength=n_years + 1)[1:], base["limit"] * (1 + base["reinstatements"]))
    rp = base["premium"] * np.minimum(rec, base["limit"] * base["reinstatements"]) / base["limit"]
    net_base = gross - rec + rp
    # the second-event cover: the mutual's own retention under the occurrence cover, on every loss occurrence
    # after the first of the year
    first = np.ones(len(years), dtype=bool)
    first[1:] = years[1:] != years[:-1]
    kept = np.minimum(l, base["retention"])
    per_s = np.where(first, 0.0, np.minimum(np.maximum(kept - sec["retention"], 0.0), sec["limit"]))
    rec_s = np.minimum(np.bincount(years, weights=per_s, minlength=n_years + 1)[1:], sec["limit"] * (1 + sec["reinstatements"]))
    rp_s = sec["premium"] * np.minimum(rec_s, sec["limit"] * sec["reinstatements"]) / sec["limit"]
    net_both = net_base - rec_s + rp_s

    def q(x):
        # the 1-in-200 the capital policy files: the average of the worst `rank` simulated years
        return float(np.sort(x)[-rank:].mean())
    out = {
        "gross": q(gross), "net_base": q(net_base), "net_both": q(net_both),
        "rec_sec": float(rec_s.mean()), "rp_sec": float(rp_s.mean()),
        "rec_base": float(rec.mean()), "rp_base": float(rp.mean()),
    }
    out["release_sec"] = out["net_base"] - out["net_both"]
    out["release_base"] = out["gross"] - out["net_base"]
    out["margin_sec"] = sec["premium"] + out["rp_sec"] - out["rec_sec"]
    return out


def value(out, coc, sec):
    """the cost of the capital the second-event cover releases, less its margin"""
    return coc * out["release_sec"] - out["margin_sec"]
