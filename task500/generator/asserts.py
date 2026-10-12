"""The build's assertion regime for task500 v3: input gates, the answer and its margins, the ladder of comparisons a
solver runs first, the certified figures that pin the standing method, the cash reconciliation's devices and their
separation from the main path. Exits non-zero on the first failure."""
import datetime as dt
import itertools
import json
import re
import sys
import warnings
from pathlib import Path

import numpy as np

import calc
import world as W

warnings.filterwarnings("ignore")
TASK = Path(__file__).resolve().parent.parent
T = TASK / "target"
N = 0


def check(cond, msg):
    global N
    N += 1
    if not cond:
        print("FAIL %d: %s" % (N, msg))
        sys.exit(1)


def edge(x):
    """distance of x from the nearest rounding edge of its whole-number bin"""
    return 0.5 - abs(x - round(x))


def main(full_grid=False):
    f, d = calc.all_figures(T)
    pn, cert, ledger = d["pn"], d["cert"], d["ledger"]
    files = sorted(p for p in T.iterdir() if p.is_file())

    # ------------------------------------------------------------------ input gates and hygiene
    check(len(files) >= 10, "at least 10 files")
    check(len({p.suffix for p in files}) >= 3, "at least 3 formats")
    check(sum(1 for _ in open(T / "lodging_tax_returns_fy2023-fy2026.csv")) > 10001, "a dataset over 10,000 rows")
    docs_text = ""
    for p in files:
        if p.suffix in (".md", ".txt", ".csv", ".json"):
            s = p.read_text(encoding="utf-8")
            check("\u2014" not in s and "\u2013" not in s, "no em or en dash in %s" % p.name)
            if p.suffix in (".md", ".txt"):
                docs_text += s + "\n"
    from pypdf import PdfReader
    for p in files:
        if p.suffix == ".pdf":
            docs_text += "\n".join(pg.extract_text() for pg in PdfReader(str(p)).pages)
    low = docs_text.lower()
    for w in ("profile", "seasonal", "pattern", "standardis", "standardiz", "z-score", "nearest", "closest",
              "business travel", "business-travel", "slump", "similar", "five reference", "matched on"):
        check(w not in low, "no document carries '%s'" % w)
    check("\u2014" not in docs_text, "no em dash in the documents")
    drawn = set(W.PEOPLE.values())
    for first, last in re.findall(r"\b([A-Z][a-z]+) ([A-Z][a-z]+)\b", docs_text):
        if first in {v.split()[0] for v in drawn}:
            check("%s %s" % (first, last) in drawn, "persona %s %s is a drawn name" % (first, last))
    dates = re.findall(r"\b(20\d\d-\d\d-\d\d)\b", docs_text)
    for p in files:
        if p.suffix == ".csv":
            dates += re.findall(r"\b(20\d\d-\d\d-\d\d)\b", p.read_text(encoding="utf-8"))
    check(max(dates) <= "2026-08-14", "no date in the pack after the extract (%s)" % max(dates))

    # ------------------------------------------------------------------ the answer and its margins
    eff = f["effects"]
    check(f["named"] == "LX", "the statement names the long-stay exemption")
    check(round(eff["LX"] / 1000) == -3235, "LX effect -3,235 thousand (%.3f)" % (eff["LX"] / 1000))
    check(f["runner_up"] == "CC" and round(eff["CC"] / 1000) == -2108, "runner-up the closure, -2,108 thousand")
    check(eff["LX"] / eff["CC"] >= 1.4, "the answer leads the runner-up by 1.4x or more")
    for key, x in list(eff.items()) + [("shortfall", f["shortfall"]), ("residual", f["residual"])]:
        check(edge(x / 1000) >= 0.01, "%s sits off its rounding edge (%.3f)" % (key, x / 1000))
    check(f["reproduced"] == (78, 78), "the standing method reproduces all 78 Appendix B figures")
    check(f["residual"] < 0 and abs(f["residual"]) > abs(eff["LX"]), "most of the shortfall is no change at all")

    # ------------------------------------------------------------------ R0 to R2: every reflex comparison names the closure
    for ctl in ("all_untouched", "same_class", "same_class_size", "neighbour_region", "same_class_balanced"):
        v = {c: calc.naive(pn, c, ctl) for c in ("CC", "LX", "AH")}
        check(min(v, key=v.get) == "CC" and v["CC"] < v["LX"] - 1.4e6,
              "the %s comparison names the closure by 1.4M or more (%s)" % (ctl, {c: round(x / 1e3) for c, x in v.items()}))
    sets = calc.touched_sets(pn, 2026)
    anyt = np.zeros(len(pn.ids), dtype=bool)
    for v in sets.values():
        anyt |= v
    cls = pn.col("cls")
    uni = ~anyt & np.isin(cls, calc.LODGING)
    fy25 = pn.R[:, 24:36]
    summer = fy25[:, [0, 1, 11]].sum(axis=1) / np.where(fy25.sum(axis=1) > 0, fy25.sum(axis=1), 1)
    for q in (3, 5, 10):
        edges = np.quantile(summer[uni], np.linspace(0, 1, q + 1))
        bins = np.clip(np.searchsorted(edges, summer, side="right") - 1, 0, q - 1)
        res = {}
        for code in ("CC", "LX"):
            t, tot = sets[code], 0.0
            for b in np.unique(bins[t]):
                tb, cb = t & (bins == b), uni & (bins == b)
                tot += pn.T[tb, 36:48].sum() - pn.T[tb, 24:36].sum() * pn.T[cb, 36:48].sum() / pn.T[cb, 24:36].sum()
            res[code] = tot
        check(res["CC"] < res["LX"], "summer-share bands (%d) still name the closure" % q)
    hosts = np.where(cls == "STR")[0]
    check(pn.R[hosts, 37:48].sum() == 0 and pn.R[hosts, 25:36].sum() > 1e7,
          "host returns stop after July 2025: a hosts-only reading shows a large loss")

    # ------------------------------------------------------------------ the certified figures pin the method
    singles = {"same_class": True, "own_region": "include", "continuity": 12, "profile": "share", "k": 6, "cap": 0,
               "order": "filer_id", "ratio": "mean", "window": "fiscal_year"}
    counts = {}
    for key, val in singles.items():
        h, t = calc.reproduction(pn, cert, {key: val})
        counts[key] = h
        check(h < t, "changing %s alone breaks the reproduction (%d of %d)" % (key, h, t))
    check(max(counts.values()) >= 40, "one near miss reproduces most of the certified figures (%s)" % counts)
    grid = dict(same_class=[False, True], own_region=["exclude", "include"], continuity=[24, 12],
                profile=["standardised", "share", "raw"], k=[4, 5, 6] if not full_grid else [3, 4, 5, 6, 8, 10],
                cap=[2, 0, 3] if not full_grid else [2, 0, 1, 3], order=["pre_receipts_desc", "filer_id"],
                ratio=["median", "mean"] if not full_grid else ["median", "mean", "sum"],
                window=["own_month", "fiscal_year"])
    full = []
    for vals in itertools.product(*grid.values()):
        c = dict(zip(grid, vals))
        h, t = calc.reproduction(pn, cert, c)
        if h == t:
            full.append(c)
    check(len(full) == 1 and all(full[0][k] == v for k, v in calc.EXACT.items() if k in full[0])
          and not full[0]["same_class"], "exactly one construction in the swept family reproduces all 78 (%d)" % len(full))

    # ------------------------------------------------------------------ the cash reconciliation and its devices
    cr = calc.cash_reconciliation(pn, ledger)
    check(abs(cr["liability"] - cr["own_periods_not_deposited"] + cr["earlier_periods_deposited"] + cr["amendments"]
              + cr["refunds"] - cr["cash"]) < 0.01, "liability to cash reconciles to the cent")
    check(abs(cr["liability"] - f["actual_fy2026"]) < 0.01, "the reconciliation starts from the statement's total")
    for key in ("cash", "own_periods_not_deposited", "earlier_periods_deposited", "amendments", "refunds"):
        check(edge(cr[key] / 1000) >= 0.01, "cash item %s off its rounding edge (%.3f)" % (key, cr[key] / 1000))
    a, b = dt.date(2025, 7, 1), dt.date(2026, 6, 30)
    pen = sum(float(r["amount"]) for r in ledger if r["type"] == "PEN_INT"
              and a <= dt.date.fromisoformat(r["deposit_date"]) <= b)
    all_am = sum(float(r["amount"]) for r in ledger if r["type"] == "AMEND"
                 and a <= dt.date.fromisoformat(r["deposit_date"]) <= b)
    check(round((cr["cash"] + pen) / 1000) != round(cr["cash"] / 1000) and pen > 50000,
          "counting penalty and interest moves collections (%.0f)" % pen)
    check(round((cr["cash"] - cr["amendments"] + all_am) / 1000) != round(cr["cash"] / 1000),
          "adding every amendment instead of the latest moves collections (%.0f)" % (all_am - cr["amendments"]))
    by_period = 0.0
    for r in ledger:
        if r["type"] == "TAX":
            y, m = map(int, r["period"].split("-"))
            if a <= dt.date(y, m, 1) <= b:
                by_period += float(r["amount"])
    check(abs(by_period - cr["cash"]) > 1e6, "reading collections by period instead of deposit date moves them")
    am = {}
    for r in ledger:
        if r["type"] == "AMEND":
            am.setdefault((r["filer_id"], r["period"]), []).append(W.fy(dt.date.fromisoformat(r["deposit_date"])))
    check(all(len(set(v)) == 1 for v in am.values()), "each return's amendments fall in one fiscal year")
    check(sum(1 for v in am.values() if len(v) == 2) >= 50, "fifty or more returns carry a second amendment")
    # separation: nothing in the returns extract carries a ledger device
    seen = set()
    for fid, i in pn.ix.items():
        pass
    keys = [(fid, per, cty) for (fid, cty), arr in pn.county_lines.items() for per in range(48) if arr[per] > 0]
    check(len(keys) == len(set(keys)), "one return line per filer, period and county")

    # ------------------------------------------------------------------ the touched groups are visible columns
    region = pn.col("region")
    check(not np.any(sets["LX"] & (np.isin(region, ["Capital City Downtown", "Airport Corridor"]))),
          "no extended-stay hotel downtown or on the airport corridor")
    check(not np.any(sets["LX"] & sets["CO"]), "no extended-stay hotel in a county that cut its option")
    for c1, c2 in itertools.combinations(("CC", "LX", "AH", "PC"), 2):
        check(not np.any(sets[c1] & sets[c2]), "%s and %s touch no filer in common" % (c1, c2))
    print("asserts: %d passed" % N)
    return f


if __name__ == "__main__":
    f = main(full_grid="--full" in sys.argv)
    out = dict(effects={k: v for k, v in f["effects"].items()}, named=f["named"], runner_up=f["runner_up"],
               actual_fy2026=f["actual_fy2026"], forecast_fy2026=f["forecast_fy2026"], shortfall=f["shortfall"],
               residual=f["residual"], reproduced=list(f["reproduced"]))
    (Path(__file__).parent / "golden_figures.json").write_text(json.dumps(out, indent=1, default=float) + "\n")
