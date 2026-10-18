"""Read the shipped bundle, compute every figure the write-up and the goldens owe, and emit
figures.json and submission.md. Nothing here reads the generator's simulated truth."""
import csv
import json
import os

import numpy as np
from openpyxl import load_workbook

import params as P
import solve

WINDOW = [(2026, m) for m in range(4, 13)] + [(2027, m) for m in range(1, 4)]
MON = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9,
       "Oct": 10, "Nov": 11, "Dec": 12}


def _month(lab):
    lab = str(lab).strip()
    if "-" in lab and lab[:3] in MON:
        return (int(lab.split("-")[1]), MON[lab[:3]])
    y, m = lab.split("-")
    return (int(y), int(m))


def _band(lab):
    return int(str(lab).strip()[-1])


def read_returns(paths):
    """Every claim return row in the window, the revised return superseding the preliminary."""
    rows = {}
    for path in paths:
        ws = load_workbook(path, read_only=True, data_only=True).active
        grid = [[c for c in r] for r in ws.iter_rows(values_only=True)]
        hdr = next(i for i, r in enumerate(grid)
                   if r and any(str(c).strip() in ("return_month", "claim_month") for c in r if c))
        cols = {str(c).strip(): j for j, c in enumerate(grid[hdr]) if c}
        mc = cols.get("return_month", cols.get("claim_month"))
        bc = cols.get("hh_band", cols.get("household_size_band"))
        nc = cols.get("award_count", cols.get("awards"))
        tc = cols.get("claim_total_php", cols.get("total_claimed_php"))
        sc = cols.get("return_status")
        pc = cols["partner_code"]
        for r in grid[hdr + 1:]:
            if not r or r[mc] is None:
                continue
            mo = _month(r[mc])
            if mo not in WINDOW:
                continue
            n = int(r[nc])
            if n < 0:                                  # a recovery is not an award (clause 9.3)
                continue
            st = str(r[sc]).strip() if sc is not None and r[sc] is not None else "FINAL"
            k = (mo, str(r[pc]).strip(), _band(r[bc]))
            if st == "PRELIM" and k in rows:
                continue
            if k in rows and rows[k][2] == "REVISED" and st != "REVISED":
                continue
            rows[k] = (n, float(r[tc]), st)
    cells = {}
    for (mo, code, b), (n, tot, st) in rows.items():
        c = cells.setdefault((code, b), [0, 0.0])
        c[0] += n
        c[1] = round(c[1] + tot, 2)
    return cells


def read_crosswalk(path):
    out = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out[r["partner_ref_portal"]] = r["ledger_partner_code"].strip()
    return out


def read_portal(path, xwalk):
    """The portal's awards inside the window, keyed to the grants ledger's partner code."""
    out = []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if _month(r["claim_return_month"]) not in WINDOW:
                continue
            out.append((xwalk[r["partner_ref_portal"]], _band(r["size_band"]),
                        float(r["award_amount_php"])))
    return out


def figures(target, F):
    cells = read_returns([os.path.join(target, F[k]) for k in ("ret2526", "ret2627")])
    xwalk = read_crosswalk(os.path.join(target, F["xwalk"]))
    por = read_portal(os.path.join(target, F["portal"]), xwalk)
    mean = {k: v[1] / v[0] for k, v in cells.items()}
    cnt = {k: v[0] for k, v in cells.items()}
    shape = np.array([a / mean[(c, b)] for c, b, a in por], float)
    shape = shape / shape.mean()
    C = solve.lowest(lambda x: solve.share_cells(x, mean, cnt, shape))
    W = dict(mean=mean, cnt=cnt, shape=shape)
    f = solve.figures_for(C, W)
    s0 = solve.share_cells(C, mean, cnt, shape)
    s1 = solve.share_cells(C - P.ROUND_TO, mean, cnt, shape)
    default = solve.lowest(lambda x: solve.share_cells(x, mean, cnt, np.array([1.0])))
    fig = {
        "call": int(C),
        "call_php": "PHP %s" % "{:,}".format(int(C)),
        "call_down": int(C - P.ROUND_TO),
        "round_to": P.ROUND_TO,
        "share_pct": round(100 * s0, 2),
        "share_down_pct": round(100 * s1, 2),
        "committed_pct": round(100 * P.COMMITTED_SHARE, 1),
        "awards": int(round(f["awards"])),
        "cells": len(cnt),
        "partners": len({k[0] for k in cnt}),
        "portal_partners": len({c for c, b, a in por}),
        "portal_window_rows": len(por),
        "cv": round(float(shape.std(ddof=1) / shape.mean()), 2),
        "referred_share": round(f["referred_share"], 1),
        "referred_value_share": round(f["referred_value_share"], 1),
        "referred_awards": int(round(f["referred"])),
        "ks_lognormal": None, "ks_gamma": None,
        "default_call": int(default),
        "default_share_pct": round(100 * solve.share_cells(default, mean, cnt, shape), 2),
        "bands": {},
    }
    for b in P.BANDS:
        d = f["bands"][b]
        fig["bands"][str(b)] = {
            "ceiling": int(d["ceiling"]), "factor": round(d["factor"], 3),
            "referred_share": round(d["referred_share"], 1),
            "referred_value_share": round(d["referred_value_share"], 1),
            "awards": int(round(d["awards"])),
        }
    from scipy.stats import norm as _n, gamma as _g
    xs = np.sort(shape)
    n = len(xs)
    ecdf = np.arange(1, n + 1) / n
    crit = 1.36 / np.sqrt(n)
    cv = float(shape.std(ddof=1) / shape.mean())
    v = np.log(1 + cv ** 2)
    kk = 1.0 / cv ** 2
    fig["ks_lognormal"] = int(round(float(np.abs(_n.cdf((np.log(xs) + 0.5 * v) / np.sqrt(v)) - ecdf).max()) / crit))
    fig["ks_gamma"] = int(round(float(np.abs(_g.cdf(xs * kk, kk) - ecdf).max()) / crit))
    fig["_test"] = _test_block(fig, mean, cnt, shape, C)
    return fig


def _test_block(fig, mean, cnt, shape, C):
    """What the goldens need beyond the graded figures: the reference band's own histogram."""
    shp = np.sort(shape)
    hi = 2500.0 * np.ceil(2.7 * fig["bands"][str(P.REF_BAND)]["ceiling"] / 2500.0)
    edges = np.linspace(0.0, hi, 46)
    counts = np.zeros(len(edges) - 1)
    for k in sorted(cnt):
        if k[1] != P.REF_BAND:
            continue
        m = mean[k]
        cdf = np.searchsorted(shp, edges / m, side="right") / len(shp)
        counts += cnt[k] * np.diff(cdf)
        counts[-1] += cnt[k] * (1.0 - cdf[-1])        # the last bin is open, so nothing is dropped
    return {"hist_edges": [float(x) for x in edges], "hist_counts": [float(x) for x in counts],
            "default_call": fig["default_call"], "default_share_pct": fig["default_share_pct"]}


def golden_content(fig):
    return fig


def write_figures(path, fig):
    out = {k: v for k, v in fig.items() if not k.startswith("_")}
    with open(path, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True)
        fh.write("\n")


# ------------------------------------------------------------------ submission.md
def submission(fig):
    b = fig["bands"]
    g = lambda k, f: b[str(k)][f]
    lines = []
    A = lines.append
    A("# task202 submission")
    A("")
    A("## Tags")
    A("")
    A("**Domain:** General statistics and data science (exploratory data analysis and distribution "
      "assessment).")
    A("**Analytical objective:** Anomaly detection and diagnostics.")
    A("")
    A("## 1. Final Recommendation")
    A("")
    A("**Set the 2027/28 referral ceiling for a four-person household at PHP %s.**" % "{:,}".format(fig["call"]))
    A("The schedule it generates refers %.2f per cent of the awards the scheme resolved in the twelve "
      "months to end-March 2027, inside clause 9's %.1f per cent, and PHP %s refers %.2f per cent. Not "
      "the distribution of the %d partner-band average awards, which carries no spread within a "
      "partner and files PHP %s, a schedule that would refer %.2f per cent. Not the portal's awards "
      "pooled or rescaled to the portfolio, which do not reproduce the average award the returns state "
      "for each of the other partners. Not a lognormal or a gamma at the portal's coefficient of "
      "variation, which the portal's own fit refuses at %d and %d times the five per cent critical "
      "value." % (fig["share_pct"], fig["committed_pct"], "{:,}".format(fig["call"] - 100),
                   fig["share_down_pct"], fig["cells"], "{:,}".format(fig["default_call"]),
                   fig["default_share_pct"], fig["ks_lognormal"], fig["ks_gamma"]))
    A("")
    A("## 2. Critical Components")
    A("")
    A("1. The twelve months to end-March 2027 hold **%s** awards in **%d** partner-band cells across "
      "**%d** accredited partners" % ("{:,}".format(fig["awards"]), fig["cells"], fig["partners"]))
    A("2. The award shape measured on the window's portal claims has a coefficient of variation of "
      "**%.2f**" % fig["cv"])
    A("3. At PHP %s the schedule refers **%.2f per cent** of those awards" %
      ("{:,}".format(fig["call"]), fig["share_pct"]))
    A("4. At PHP %s it refers **%.2f per cent**, above the commitment, so PHP %s is the lowest "
      "qualifying multiple of PHP 100" % ("{:,}".format(fig["call"] - 100), fig["share_down_pct"],
                                          "{:,}".format(fig["call"])))
    A("")
    A("## 3. Step-by-Step Solution")
    A("")
    A("1. Took the claim returns for April 2026 to March 2027 from hrg_claim_returns_fy2025-26.xlsx and "
      "hrg_claim_returns_fy2026-27.xlsx, the revised return superseding the preliminary one for the two "
      "reopened months as the policy requires, and recoveries excluded because the policy counts awards "
      "gross: %s awards in %d partner-band cells." %
      ("{:,}".format(fig["awards"]), fig["cells"]))
    A("2. Divided each cell's claimed total by its award count: each partner-band's own average award, "
      "the only award-level figure the returns state.")
    A("3. Resolved portal_awards_2025-01_2027-03.csv's partner reference to the grants ledger through "
      "partner_identifier_crosswalk.csv and kept the awards claimed in those twelve months: %s award "
      "rows for %d partners." %
      ("{:,}".format(fig["portal_window_rows"]), fig["portal_partners"]))
    A("4. Expressed each of those awards as a multiple of its own partner-band average award: the "
      "award shape, coefficient of variation %.2f, which a single lognormal and a single gamma at that "
      "coefficient of variation fit at %d and %d times the five per cent Kolmogorov-Smirnov critical "
      "value." % (fig["cv"], fig["ks_lognormal"], fig["ks_gamma"]))
    A("5. Rebuilt each cell's award distribution as the cell's own average award times that shape and "
      "weighted each cell by its award count, which is the policy's share of the scheme's awards.")
    A("6. Generated each band's ceiling from a candidate reference ceiling by schedule B.2's factor in "
      "hrg_operating_policy_2027_edition.pdf, rounded up to the nearest PHP 100 under B.3, and took the lowest candidate whose referred share "
      "is at or below %.1f per cent: PHP %s refers %.2f per cent and PHP %s refers %.2f per cent." %
      (fig["committed_pct"], "{:,}".format(fig["call"]), fig["share_pct"],
       "{:,}".format(fig["call"] - 100), fig["share_down_pct"]))
    A("7. Cut instead on the distribution of the %d partner-band averages, the ceiling is PHP %s and "
      "the schedule refers %.2f per cent of the window's awards." %
      (fig["cells"], "{:,}".format(fig["default_call"]), fig["default_share_pct"]))
    A("8. Set the 2027/28 referral ceiling for a four-person household at PHP %s." %
      "{:,}".format(fig["call"]))
    A("")
    A("## 4. Deliverable Answers")
    A("")
    A("### relief_referral_ceilings_2027-28.xlsx")
    A("")
    A("1. Each band's 2027/28 referral ceiling in pesos, its referred share of that band's own awards "
      "and of that band's own award value to one decimal place, and the scale factor applied to three "
      "decimals, in band order:")
    for k in P.BANDS:
        A("   - %s: ceiling PHP %s, refers %.1f per cent of awards and %.1f per cent of award value, "
          "scale factor %.3f" % (P.BAND_LABEL[k], "{:,}".format(g(k, "ceiling")),
                                 g(k, "referred_share"), g(k, "referred_value_share"), g(k, "factor")))
    A("2. All bands together: refers %.1f per cent of awards and %.1f per cent of award value." %
      (fig["referred_share"], fig["referred_value_share"]))
    A("")
    A("### referral_ceiling_board_paper.pdf")
    A("")
    A("1. The recommendation on page 1: set the 2027/28 referral ceiling for a four-person household "
      "at PHP %s." % "{:,}".format(fig["call"]))
    A("2. The same six ceilings, referred shares of awards and of award value, and scale factors as "
      "the workbook, in the schedule table on page 1.")
    A("3. The award distribution and the ceilings drawn across household sizes: a histogram of the "
      "four-person band's award amounts with the PHP %s ceiling marked and the referred tail shaded, "
      "beside the six ceilings stepped across the household-size bands with each band's referred share "
      "labelled, on page 1." % "{:,}".format(fig["call"]))
    A("")
    return "\n".join(lines)
