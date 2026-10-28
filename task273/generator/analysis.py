"""task273 architecture 4: the golden, the licensed family, the ladder's rungs and the asks, all from the World."""
from __future__ import annotations

import numpy as np

import params as P

PLP = ("Pathogenic", "Likely pathogenic")


def class_on(site, when):
    """The register's class for a site on a date (its history read forward)."""
    if not site["history"]:
        return site["klass"] if site["since"] <= when else None
    cls = None
    for d, frm, to in sorted(site["history"]):
        if d <= when:
            cls = to
    return cls


def census_sites(w, gene):
    return [s for s in w.study_sites if s["gene"] == gene and class_on(s, P.CENSUS) in PLP]


def _mle(c, s):
    lo, hi = 1e-9, 0.5
    for _ in range(100):
        m = (lo + hi) / 2
        g = (c / m).sum() - ((1 - c) * s / (1 - m * s)).sum()
        lo, hi = (m, hi) if g > 0 else (lo, m)
    return m


def frequencies(w, rung="golden"):
    """Each gene's carrier frequency in the reference cohort (a share) under one construction."""
    co = w.cohort
    N = co.sum()
    out = {}
    for gene, *_ in P.CONDITIONS:
        tot = 0.0
        anycall = np.zeros(w.N, dtype=bool)
        for s in census_sites(w, gene):
            sid = s["site_id"]
            c, sens, d = w.called[sid] & co, w.sens[sid], w.depth[sid]
            anycall |= c
            if rung in ("golden", "mle", "community"):
                groups = [(w.phase == p) & co for p in (1, 2)]
                if rung == "community":
                    groups = [(w.area == a) & co for a, _p, _n in P.AREAS]
                for m in groups:
                    if m.sum() == 0:
                        continue
                    if rung == "mle":
                        tot += _mle(c[m].astype(float), sens[m]) * m.sum()
                    else:
                        tot += c[m].sum() / sens[m].sum() * m.sum()
            elif rung == "ht":
                tot += (c[co] / sens[co]).sum()
            elif rung == "pooled":
                tot += c[co].sum() / sens[co].sum() * N
            elif rung in ("cc10", "cc20"):
                t = 10 if rung == "cc10" else 20
                m = co & (d >= t)
                tot += c[m].sum() / m.sum() * N if m.sum() else 0.0
        if rung == "naive":
            out[gene] = anycall.sum() / N
        else:
            out[gene] = tot / N
    return out


FAMILY = ("golden", "ht", "mle", "community")
EASY = ("naive", "cc10", "cc20", "pooled")


ISLAND_AREAS = ("Morvaig Isles", "Glenhaskel")


def community(w, rung="golden"):
    """Each 2026/27 panel condition's carrier frequency among the cohort's members in each phase 1 area."""
    co = w.cohort
    out = {}
    for area in ISLAND_AREAS:
        m = co & (w.area == area)
        n = m.sum()
        for gene in w.panel_genes:
            tot = 0.0
            anycall = np.zeros(w.N, dtype=bool)
            for s in census_sites(w, gene):
                sid = s["site_id"]
                c, sens, d = w.called[sid] & m, w.sens[sid], w.depth[sid]
                anycall |= c
                if rung == "golden":
                    tot += c[m].sum() / sens[m].sum() * n
                elif rung == "ht":
                    tot += (c[m] / sens[m]).sum()
                elif rung == "mle":
                    tot += _mle(c[m].astype(float), sens[m]) * n
                elif rung == "cc10":
                    k = m & (d >= 10)
                    tot += c[k].sum() / k.sum() * n if k.sum() else 0.0
            out[(area, gene)] = anycall.sum() / n if rung == "naive" else tot / n
    return out


def per_thousand(x):
    return int(np.floor(x * 1000 + 0.5))


def panel(freqs):
    return sorted(g for g, f in freqs.items() if f >= P.PANEL_LINE - 1e-12)


def solve(w):
    R = {r: frequencies(w, r) for r in FAMILY + EASY}
    gold = R["golden"]
    S = dict(rungs=R, freq=gold, panel=panel(gold),
             panel_2026=sorted(g for g, c, on, f, v in P.CONDITIONS if on),
             cohort=int(w.cohort.sum()),
             cohort_by_phase={p: int((w.cohort & (w.phase == p)).sum()) for p in (1, 2)})
    S["joining"] = sorted(set(S["panel"]) - set(S["panel_2026"]))
    S["leaving"] = sorted(set(S["panel_2026"]) - set(S["panel"]))
    S["called"] = {g: {p: int(np.any([w.called[s["site_id"]] & w.cohort & (w.phase == p)
                                     for s in census_sites(w, g)], axis=0).sum()) for p in (1, 2)}
                   for g, *_ in P.CONDITIONS}
    S["ask_b"] = programme_told(w)
    S["ask_b_variants"] = {k: programme_told(w, **v) for k, v in ASK_B_VARIANTS.items()}
    return S


# ---------------------------------------------------------------------------------------------- the asks
HALVES = (("H1", P.PROG_YEAR[0], P.PROG_YEAR[0].replace(month=9, day=30)),
          ("H2", P.PROG_YEAR[0].replace(month=10, day=1), P.PROG_YEAR[1]))


def programme_told(w, date_by="report", vintage="authorised", unit="couple", skip_reused=False):
    """Each 2026/27 panel condition and half of the 2025/26 screening year: the couples whose report told them that
    one or both partners carry it. A couple's report goes when every result its screen needs is authorised (the later
    partner's, or the first partner's alone where a sequential screen stops); a finding counts when the register
    classed it pathogenic or likely pathogenic on the day its result was authorised (policy 4.2, 4.3)."""
    reg = {(s["gene"], s["c"]): s for s in w.sites}
    out = {(h, g): set() for h, _a, _b in HALVES for g in w.panel_genes}
    for r in w.prog:
        if skip_reused and r["reused"]:
            continue
        when = {"report": r["told"], "result": r["result"], "received": r["recv"]}[date_by]
        half = next((h for h, a, b in HALVES if a <= when <= b), None)
        if half is None:
            continue
        for (g, c) in r["found"]:
            if g not in w.panel_genes:
                continue
            if vintage == "authorised":
                k = r["klass"][(g, c)]
            elif vintage == "export":
                k = r["klass"][(g, c)] if r["result"] < P.LIMS_UPGRADE or (g, c) not in reg else \
                    (class_on(reg[(g, c)], P.EXTRACT) or "Uncertain significance")
            else:
                k = class_on(reg[(g, c)], P.EXTRACT) if (g, c) in reg else "Uncertain significance"
            if k in PLP:
                out[(half, g)].add(r["couple"] if unit == "couple" else (r["couple"], r["letter"]))
    return {k: len(v) for k, v in out.items()}


ASK_B_VARIANTS = {"result date": dict(date_by="result"), "received date": dict(date_by="received"),
                  "the export's class column": dict(vintage="export"),
                  "today's register": dict(vintage="current"), "people not couples": dict(unit="partner"),
                  "carried-forward dropped": dict(skip_reused=True)}
