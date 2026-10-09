"""Unit constructions over the shipped return file and dependents schedule (generator side).

Every construction reads only shipped columns: return_id, filer_tin, federal_primary_tin,
residency_code, county_code, federal_agi (returns) and claimant_return_id, dependent_tin
(schedule). The independent verifier carries its own implementation in DuckDB SQL.
"""
import numpy as np
import pandas as pd

from common import k_top, PCTS

CLASSES = [(100_000, 200_000), (200_000, 300_000), (300_000, 500_000), (500_000, 1_000_000),
           (1_000_000, 1_500_000), (1_500_000, 2_000_000), (2_000_000, 5_000_000),
           (5_000_000, 10_000_000), (10_000_000, None)]
CLASS_LABELS = ["$100,000 under $200,000", "$200,000 under $300,000", "$300,000 under $500,000",
                "$500,000 under $1,000,000", "$1,000,000 under $1,500,000",
                "$1,500,000 under $2,000,000", "$2,000,000 under $5,000,000",
                "$5,000,000 under $10,000,000", "$10,000,000 or more"]

GRID = [(res, unit, dep) for res in ("code1", "all") for unit in ("ffu", "return")
        for dep in ("attached", "dropped", "separate")]
PARTIAL = ("code1", "ffu", "income_attached_units_kept")
ALL_CONSTRUCTIONS = GRID + [PARTIAL]
NAMES = {("code1", "ffu", "attached"): "households (answer)",
         ("code1", "ffu", "dropped"): "rung 3, dependents' returns dropped",
         ("code1", "ffu", "separate"): "rung 2, federal filing units",
         ("code1", "return", "separate"): "rung 1, resident returns",
         ("all", "return", "separate"): "rung 0, all returns",
         PARTIAL: "partial, dependents' income attached and their returns kept"}


def units(ret, sched, residency, unit, deps):
    """Units of one construction: DataFrame with key, agi, county."""
    r = ret if residency == "all" else ret[ret.residency_code == 1]
    r = r[["return_id", "filer_tin", "federal_primary_tin", "county_code", "federal_agi"]]
    # dependents' own returns: a filed return whose filer TIN sits on a schedule of a return in r
    s = sched[["claimant_return_id", "dependent_tin"]]
    s = s[s.claimant_return_id.isin(r.return_id)]
    is_dep = r.filer_tin.isin(s.dependent_tin)
    claim_of = s.set_index("dependent_tin").claimant_return_id
    if unit == "return":
        key = r.return_id.to_numpy().copy()
    else:
        key = r.federal_primary_tin.to_numpy().copy()
    if deps == "dropped":
        r = r[~is_dep.to_numpy()]
        key = key[~is_dep.to_numpy()]
        agi = r.federal_agi.to_numpy()
    elif deps in ("attached", "income_attached_units_kept"):
        dep_rows = np.where(is_dep.to_numpy())[0]
        claimant = claim_of.loc[r.filer_tin.to_numpy()[dep_rows]].to_numpy()
        if unit == "return":
            ck = claimant
        else:
            fp = r.set_index("return_id").federal_primary_tin
            ck = fp.loc[claimant].to_numpy()
        key2 = key.copy()
        key2[dep_rows] = ck
        if deps == "attached":
            key = key2
            agi = r.federal_agi.to_numpy()
        else:
            # dependents' income added to the claimant's unit, their own returns kept as units
            base = pd.DataFrame({"key": key, "agi": r.federal_agi.to_numpy()})
            extra = pd.DataFrame({"key": key2[dep_rows], "agi": r.federal_agi.to_numpy()[dep_rows]})
            g = pd.concat([base, extra]).groupby("key", sort=True).agi.sum()
            cty = _county_of_keys(r, unit, g.index.to_numpy())
            return pd.DataFrame({"key": g.index.to_numpy(), "agi": g.to_numpy(), "county": cty})
    else:
        agi = r.federal_agi.to_numpy()
    g = pd.DataFrame({"key": key, "agi": agi}).groupby("key", sort=True).agi.sum()
    cty = _county_of_keys(r, unit, g.index.to_numpy())
    return pd.DataFrame({"key": g.index.to_numpy(), "agi": g.to_numpy(), "county": cty})


def _county_of_keys(r, unit, keys):
    if unit == "return":
        m = r.set_index("return_id").county_code
        return m.loc[keys].to_numpy()
    prim = r[r.filer_tin == r.federal_primary_tin].set_index("filer_tin").county_code
    return prim.loc[keys].to_numpy()


def nearest_rank_floors(agi):
    v = np.sort(np.asarray(agi))[::-1]
    out = []
    for p in PCTS:
        k = k_top(len(v), p)
        out.append(int(v[k - 1]))
    return out


def published_cells(u, year, appendix_codes):
    """The cells a Household Income Table publishes, computed on construction u."""
    agi = u.agi.to_numpy()
    cells = {}
    for (lo, hi), lab in zip(CLASSES, CLASS_LABELS):
        m = (agi >= lo) & ((agi < hi) if hi else True)
        cells[("units", lab)] = int(m.sum())
        cells[("agi_k", lab)] = half_up_thousands(int(agi[m].sum()))
    cells[("total_agi_k", "all")] = half_up_thousands(int(agi.sum()))
    if year == 2024:
        hi = u[u.agi >= 500_000]
        cnt = hi.county.value_counts()
        for c in appendix_codes:
            cells[("county_units_500k", c)] = int(cnt.get(c, 0))
    return cells


def half_up_thousands(x):
    q, r = divmod(int(x), 1000)
    return q + (1 if r >= 500 else 0)


def hits(cells, published):
    return sum(1 for k, v in published.items() if cells.get(k) == v)
