"""Scratch: the estimators on the window for a trial head design (spans, zeros), against the band."""
import sys, numpy as np, datetime as dt, params as P, sim
from zoneinfo import ZoneInfo

def window_idx():
    mad = ZoneInfo("Europe/Madrid")
    t0 = dt.datetime(*P.WINDOW_LOCAL[0].timetuple()[:3], tzinfo=mad).astimezone(dt.timezone.utc)
    t1 = dt.datetime(*P.WINDOW_LOCAL[1].timetuple()[:3], tzinfo=mad).astimezone(dt.timezone.utc)
    return int((t0 - P.START).total_seconds() // 3600), int((t1 - P.START).total_seconds() // 3600)

def estimators(node, ref, pool):
    out = {}
    out["ols_h"] = np.polyfit(ref, node, 1)[0]
    dn, dr = node.reshape(-1, 24).mean(1), ref.reshape(-1, 24).mean(1)
    out["ols_d"] = np.polyfit(dr, dn, 1)[0]
    out["rom"] = node.mean() / ref.mean()
    sxx, syy, sxy = ref.var(), node.var(), np.cov(ref, node, bias=True)[0, 1]
    out["deming"] = (syy - sxx + np.sqrt((syy - sxx) ** 2 + 4 * sxy ** 2)) / (2 * sxy)
    out["dm_near"] = node.std() / ref.std()
    out["dm_pool"] = node.std() / pool.std()
    iq = lambda v, a, b: np.subtract(*np.percentile(v, [b, a]))
    out["iqr_pool"] = iq(node, 25, 75) / iq(pool, 25, 75)
    out["q90_pool"] = iq(node, 10, 90) / iq(pool, 10, 90)
    out["dm_daily"] = dn.std() / pool.reshape(4, -1, 24).mean(2).reshape(-1).std() if pool.size % 24 == 0 else np.nan
    qs = np.linspace(2, 98, 49)
    out["qq_pool"] = np.polyfit(np.percentile(pool, qs), np.percentile(node, qs), 1)[0]
    out["r"] = np.corrcoef(node, ref)[0, 1]
    return out

if __name__ == "__main__":
    rng = np.random.default_rng(P.SEED)
    an = [(a[2], a[3]) for a in P.ANALYSERS]
    pts = []
    r2 = np.random.default_rng(11)
    while len(pts) < 36:
        x, y = r2.uniform(-30, 30), r2.uniform(-26, 24)
        if min(np.hypot(x - ax, y - ay) for ax, ay in an) > 0.8:
            pts.append((round(x, 1), round(y, 1)))
    true = sim.field(an + pts, rng)
    i0, i1 = window_idx()
    A = true[:4, i0:i1]; N = true[4:, i0:i1]
    pool = A.reshape(-1)
    print("analyser pairs DM:", ["%.3f" % (A[a].std() / A[b].std()) for a in range(4) for b in range(a + 1, 4)])
    print("analyser pairs OLS:", ["%.3f" % np.polyfit(A[b], A[a], 1)[0] for a in range(4) for b in range(a + 1, 4)])
    for j, (x, y) in enumerate(pts):
        d = [np.hypot(x - ax, y - ay) for ax, ay in an]; k = int(np.argmin(d))
        node = N[j] + 2.5 * rng.standard_normal(N.shape[1])
        e = estimators(node, A[k], pool)
        print("n%02d d=%5.1f r=%.2f " % (j, min(d), e["r"]) + " ".join("%s %.3f" % (k_, v) for k_, v in e.items() if k_ != "r"))
