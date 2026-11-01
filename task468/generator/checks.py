"""task468 architecture 6: the generator's assertions on the cut pack (the call, the ladder, the family, the asks)."""
import glob
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen as G     # noqa: E402
import solve as SV  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
FAILS = []


def ok(name, cond, detail=""):
    print("%s  %-60s %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond:
        FAILS.append(name)


def main():
    D = SV.load(TARGET)
    S = SV.lab(D)
    vol = SV.volumes(D)
    name = {G.C[k]["name"]: k for k in G.KEYS}
    lim = D["limit"]

    def run(route):
        conv = SV.converter(S, route)
        cod = SV.masses(D, S, vol, conv)
        return cod, sorted(name[c] for c in D["custs"] if cod[c] > lim[c])
    gold_cod, gold = run("golden")
    ok("C1 the golden set", gold == sorted(["COOL", "TALL", "GMEA", "RIVP"]), gold)
    margin = min(abs(gold_cod[c] / lim[c] - 1) for c in D["custs"])
    ok("C1 every customer at least 5 per cent from its limit (golden)", margin >= 0.05, "%.3f" % margin)
    for route in ("chloride_origin", "chloride_wls"):
        cod, s = run(route)
        m = min(abs(cod[c] / lim[c] - 1) for c in D["custs"])
        ok("C2 family member %s files the golden set" % route, s == gold and m >= 0.04, "%s %.3f" % (s, m))
    want = {"pooled_ratio": ["GMEA", "RIVP", "SUND"], "pooled_ols": ["GMEA", "RIVP", "SUND"],
            "own_ratio": ["COOL", "GMEA", "MTED", "RIVP"], "own_median_ratio": ["COOL", "GMEA", "MTED", "RIVP"],
            "own_ols": None}
    for route, exp in want.items():
        cod, s = run(route)
        ok("C3 rung %s files a wrong set" % route, s != gold and (exp is None or s == exp), s)
    # the data's own evidence: residuals of the TOC-only fit track chloride on the parallel samples
    par = SV.parallel(S)
    b = SV.fit(par, form="toc")
    res = np.array([s["an"]["cod"] - b[0] - b[1] * s["an"]["toc"] for s in par])
    cl = np.array([s["an"]["cl"] for s in par])
    r = float(np.corrcoef(res, cl)[0, 1])
    ok("C4 TOC-only residuals correlate with chloride on the parallel samples", r > 0.9, "%.3f" % r)
    # the conformed volumes equal the world's metered volumes
    import pack as K
    W = G.world()
    K.clear_volume_edges(W)
    tv = {k: [sum(W["flow"][k][d] for d in G.local_dates(2026, 2026) if (d.month - 1) // 3 == q) for q in range(4)]
          for k in G.KEYS}
    diff = max(abs(vol[G.C[k]["name"]]["q"][q] - tv[k][q]) for k in G.KEYS for q in range(4))
    ok("C5 conformed quarterly volumes equal the meters' (kL)", diff < 0.6, "%.2f" % diff)
    import liquid as LQ
    liq = SV.liquid(TARGET)
    tru = LQ.truth(LQ.world())
    dl = max(abs(liq[t][q] - tru[t][q]) for t in liq for q in range(4))
    ok("C6 ask A, tankered waste by type and quarter equals the receival truth (kL)", dl < 0.02, "%.3f" % dl)
    edge_a = min(abs((liq[t][q] % 1) - 0.5) for t in liq for q in range(4))
    ok("C6 no tankered volume within 0.1 kL of a rounding edge", edge_a >= 0.1, "%.3f" % edge_a)
    ss = SV.masses(D, S, vol, None, analyte="ss")
    edge_b = min(abs(((ss[c] * 10) % 1) - 0.5) for c in D["custs"])
    ok("C7 no suspended solids mass within 0.012 t of a rounding edge", edge_b >= 0.12, "%.3f" % edge_b)
    # each ask's primary device moves its figures on the careful solver's path
    liq_dk = SV.liquid(TARGET, join="docket")
    moved_a = sum(int(round(liq_dk[t][q])) != int(round(liq[t][q])) for t in liq for q in range(4))
    ok("C8 ask A, a docket-only join moves the tankered figures", moved_a >= 14, "%d of 16" % moved_a)
    ss_all = SV.masses(D, S, vol, None, analyte="ss", composites_only=False)
    moved_b = sum("%.1f" % ss_all[c] != "%.1f" % ss[c] for c in D["custs"])
    ok("C9 ask B, the inspection grabs counted as samples move the suspended solids masses", moved_b >= 11,
       "%d of 12" % moved_b)
    S_dup = SV.lab(D, dup="own", rerun="ignore")
    ss_dup = SV.masses(D, S_dup, vol, None, analyte="ss")
    moved_h = sum("%.1f" % ss_dup[c] != "%.1f" % ss[c] for c in D["custs"])
    ok("C9 ask B hazard: duplicates and original results kept move some masses", moved_h >= 3, moved_h)
    grabs = [s for s in S.values() if not ("toc" in s["an"] or "cod" in s["an"])]
    ok("C10 separation: no inspection grab carries COD, TOC or chloride", all(set(s["an"]) <= {"ss", "ph"}
                                                                            for s in grabs) and len(grabs) >= 60,
       len(grabs))
    # the semantic fork table, row by row
    conv = SV.converter(S, "golden")

    def over_with(samples, volumes, limits=None):
        cod = SV.masses(D, samples, volumes, SV.converter(samples, "golden"))
        lm = limits or lim
        return sorted(name[c] for c in D["custs"] if cod[c] > lm[c])
    ok("SF1 the chloride family files the golden set (C2) and every ratio route another (C3)", True, "")
    vol_utc = None
    ok("SF2 samples dated in UTC in place of Queensland time file the same set",
       over_with(SV.lab(D, year_clock="utc"), vol) == gold, "")
    seg_reg = {r["Customer"]: [(r["Flow meter"], None, None, None, None)] for r in D["reg"]}
    try:
        reg_only = over_with(S, SV.volumes(D, seg=seg_reg))
    except KeyError:
        reg_only = "register meter has no reading at the year start"
    ok("SF3 the register's meter alone cannot reach the year's start (closed by policy section 3)",
       reg_only != gold, str(reg_only))
    cod_unw = {}
    for c in D["custs"]:
        xs = [s["an"]["cod"] if "cod" in s["an"] else conv(c, s["an"]) for s in S.values()
              if s["cust"] == c and s["when"].year == 2026 and ("cod" in s["an"] or "toc" in s["an"])]
        cod_unw[c] = vol[c]["year"] * float(np.mean(xs)) / 1e6
    ok("SF4 an unweighted mean files the same set",
       sorted(name[c] for c in D["custs"] if cod_unw[c] > lim[c]) == gold, "")
    ok("SF5 duplicates and original results kept file the same set",
       over_with(SV.lab(D, dup="own", rerun="ignore"), vol) == gold, "")
    ok("SF6 no COD result carries a below-limit flag",
       all(s["an"].get("cod", 1) > 0 for s in S.values()), "")
    jan_toc = [s for s in S.values() if s["when"].year == 2026 and s["when"].month == 1 and "toc" in s["an"]]
    ok("SF7 no January 2026 sample was tested for TOC", not jan_toc, len(jan_toc))
    lim_t = {c: float([r for r in D["reg"] if r["Customer"] == c][0]["COD limit"]) for c in D["custs"]}
    ok("SF8 kilograms read as tonnes files the same set", over_with(S, vol, lim_t) == gold, "")
    ok("SF9 no customer within 6 per cent of its limit", margin >= 0.06, "%.3f" % margin)
    files = sorted(os.listdir(TARGET))
    fmts = sorted(set(f.rsplit(".", 1)[1] for f in files))
    ok("G1 ten or more files in three or more formats", len(files) >= 10 and len(fmts) >= 3, "%d %s" % (len(files),
                                                                                                         fmts))
    n = sum(1 for _ in open(os.path.join(TARGET, G.FILES["telemetry"]))) - 1
    ok("G2 a file of 25,000 rows or more", n >= 25000, n)
    dash = [f for f in glob.glob(os.path.join(TARGET, "*")) if f.endswith((".csv", ".eml")) and
            chr(0x2014) in open(f, encoding="utf-8").read()]
    ok("G3 no em dash in any text file", not dash, dash)
    print("%d checks, %d failed" % (len(FAILS) + 0 + sum(1 for _ in []), len(FAILS)) if False else
          "checks done, %d failed" % len(FAILS))
    sys.exit(1 if FAILS else 0)


if __name__ == "__main__":
    main()
