"""Each Layer 1 item of the pack, mishandled the natural way, read back off the shipped bundle.

The claim is that none of them moves the call or a graded figure: the mess complicates the work and
carries nothing. Every number here is measured on the pack, not on the simulation.
"""
import csv
import os

import numpy as np
from openpyxl import load_workbook

import build as B
import params as P
import solve
import writeup as WU

ITEMS = ["prelim_only", "both_counted", "net_recovery", "legacy_band_labels", "normalised_key"]


def _grid(path):
    ws = load_workbook(path, read_only=True, data_only=True).active
    grid = [[c for c in r] for r in ws.iter_rows(values_only=True)]
    h = next(i for i, r in enumerate(grid)
             if r and any(str(c).strip() in ("return_month", "claim_month") for c in r if c))
    cols = {str(c).strip(): j for j, c in enumerate(grid[h]) if c}
    return grid, h, cols


def cells(target, mode):
    """Resolve one row per partner, band and claim month first, then aggregate over the window."""
    rows = {}
    for k in ("ret2526", "ret2627"):
        grid, h, cols = _grid(os.path.join(target, B.FILES[k]))
        mc = cols.get("return_month", cols.get("claim_month"))
        bc = cols.get("hh_band", cols.get("household_size_band"))
        nc = cols.get("award_count", cols.get("awards"))
        tc = cols.get("claim_total_php", cols.get("total_claimed_php"))
        sc = cols.get("return_status")
        pc = cols["partner_code"]
        for i, r in enumerate(grid[h + 1:]):
            if not r or r[mc] is None:
                continue
            mo = WU._month(r[mc])
            if mo not in WU.WINDOW:
                continue
            n = int(r[nc])
            if n < 0 and mode != "net_recovery":
                continue
            st = str(r[sc]).strip() if sc is not None and r[sc] is not None else "FINAL"
            key = (mo, str(r[pc]).strip(), WU._band(r[bc]))
            if mode == "both_counted":
                rows[key + (st, k, i)] = (n, float(r[tc]), st)
                continue
            if mode == "prelim_only" and st == "REVISED":
                continue
            if st == "PRELIM" and key in rows:
                continue
            if key in rows and rows[key][2] == "REVISED" and st != "REVISED":
                continue
            rows[key] = (n, float(r[tc]), st)
    out = {}
    for key, (n, tot, st) in rows.items():
        agg = out.setdefault((key[1], key[2]), [0, 0.0])
        agg[0] += n
        agg[1] = round(agg[1] + tot, 2)
    return out


def portal(target, mode):
    xw = WU.read_crosswalk(os.path.join(target, B.FILES["xwalk"]))
    out = []
    with open(os.path.join(target, B.FILES["portal"]), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if WU._month(r["claim_return_month"]) not in WU.WINDOW:
                continue
            if mode == "normalised_key":
                code = r["partner_ref_portal"].strip().upper().replace("_", "-")
            else:
                code = xw[r["partner_ref_portal"]]
            out.append((code, WU._band(r["size_band"]), float(r["award_amount_php"])))
    return out


def one(target, mode):
    cl = cells(target, mode)
    po = portal(target, mode)
    mean = {k: v[1] / v[0] for k, v in cl.items()}
    cnt = {k: v[0] for k, v in cl.items()}
    if mode == "legacy_band_labels":
        # the band column was relabelled in July 2026; resolve it through the reference table's own
        # mapping rather than by the order of the codes
        with open(os.path.join(target, B.FILES["bands"]), newline="", encoding="utf-8") as fh:
            m = {r["legacy_band_code"]: int(r["band_code"][-1]) for r in csv.DictReader(fh)}
        assert all(m["HH%d" % b] == b for b in P.BANDS), m
    sh = np.array([a / mean[(c, b)] for c, b, a in po if (c, b) in mean], float)
    sh = sh / sh.mean()
    C = solve.lowest(lambda x: solve.share_cells(x, mean, cnt, sh))
    F = solve.figures_for(C, {"mean": mean, "cnt": cnt, "shape": sh})
    return {"call": int(C), "awards": int(round(F["awards"])),
            "share": 100 * solve.share_cells(C, mean, cnt, sh),
            "b4": F["bands"][P.REF_BAND]["referred_share"],
            "joined": len(sh), "rows": len(po)}


def all_items(target):
    return {m: one(target, m) for m in ITEMS}


if __name__ == "__main__":
    T = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "target")
    base = one(T, "filed")
    print("filed            %s" % base)
    for m, v in all_items(T).items():
        print("%-18s call %d (%+d pu) awards %+d share %.4f b4 %.4f joined %d"
              % (m, v["call"], (v["call"] - base["call"]) // 100, v["awards"] - base["awards"],
                 v["share"], v["b4"], v["joined"]))
