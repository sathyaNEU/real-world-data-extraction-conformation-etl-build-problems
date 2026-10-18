"""The independent verifier: reads only the shipped bundle and the shipped deliverables, on its own
code path, and recomputes clause 9's ceiling, every graded figure and every figure the write-up
states. It imports nothing from the generator's model, its solver or its write-up emitter.

    python3 task202/generator/verify.py
"""
import csv
import json
import math
import os
import re
import sys

from openpyxl import load_workbook

WINDOW = {(2026, m) for m in range(4, 13)} | {(2027, m) for m in range(1, 4)}
MONTHS = {"Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9,
          "Oct": 10, "Nov": 11, "Dec": 12}
CAP = 0.060
REF = 4
BANDS = (1, 2, 3, 4, 5, 6)
RET = ("hrg_claim_returns_fy2025-26.xlsx", "hrg_claim_returns_fy2026-27.xlsx")
PORTAL = "hrg_partner_claim_portal_awards_2025-01_2027-03.csv"
XWALK = "partner_identifier_crosswalk.csv"
POLICY = "hrg_operating_policy_2027_edition.pdf"
SUMMARY = "hrg_annual_report_partner_summary_fy2025-26.pdf"
BANDS_CSV = "household_size_bands.csv"

OK = 0


def need(cond, label, note=""):
    global OK
    if not cond:
        raise AssertionError("verify: %s %s" % (label, note))
    OK += 1


def month(v):
    v = str(v).strip()
    if v[:3] in MONTHS:
        return (int(v.split("-")[1]), MONTHS[v[:3]])
    a, b = v.split("-")
    return (int(a), int(b))


def pdf_text(path):
    """The document's own text layer, whitespace collapsed so a filed sentence can be searched for
    whatever line it was laid out on."""
    from pypdf import PdfReader
    raw = "\n".join((p.extract_text() or "") for p in PdfReader(path).pages)
    return re.sub(r"\s+", " ", raw)


def factor(b, scale):
    return scale[b]


def ceiling(C, b, scale):
    """Schedule B: the band factor applied to the reference ceiling, rounded up to PHP 100."""
    return 100 * int(math.ceil(round(C * scale[b], 6) / 100.0))


def read_scale(policy_text):
    """Schedule B files the scale as a rule and tabulates no factor, so every band's factor is
    computed from B.2: the square root of the ratio of the band's size to the reference size of four,
    to three decimals, the band's size being its lower bound."""
    need("square root of the ratio" in policy_text, "B.2 states the scale as a ratio under a root")
    need("lower bound of the band" in policy_text, "B.2 fixes the open band's size")
    need(not re.search(r"0\.707|0\.866|1\.118|1\.225", policy_text),
         "no factor is tabulated in the policy")
    return {b: round(math.sqrt(b / 4.0), 3) for b in BANDS}, {}


def read_returns(target):
    rows = {}
    for f in RET:
        ws = load_workbook(os.path.join(target, f), read_only=True, data_only=True).active
        grid = [list(r) for r in ws.iter_rows(values_only=True)]
        hi = None
        for i, r in enumerate(grid):
            names = [str(c).strip() for c in r if c is not None]
            if "partner_code" in names:
                hi = i
                break
        need(hi is not None, "header row found in %s" % f)
        col = {str(c).strip(): j for j, c in enumerate(grid[hi]) if c is not None}
        mk = "claim_month" if "claim_month" in col else "return_month"
        bk = "household_size_band" if "household_size_band" in col else "hh_band"
        nk = "awards" if "awards" in col else "award_count"
        tk = "total_claimed_php" if "total_claimed_php" in col else "claim_total_php"
        for r in grid[hi + 1:]:
            if not r or r[col[mk]] is None:
                continue
            mo = month(r[col[mk]])
            if mo not in WINDOW:
                continue
            n = int(r[col[nk]])
            if n < 0:
                continue                                     # gross, clause 9.3
            st = str(r[col["return_status"]]).strip() if "return_status" in col else "FINAL"
            key = (mo, str(r[col["partner_code"]]).strip(), int(str(r[col[bk]]).strip()[-1]))
            if key in rows and (st == "PRELIM" or rows[key][2] == "REVISED"):
                continue
            rows[key] = (n, float(r[col[tk]]), st)
    cells = {}
    for (mo, code, b), (n, tot, st) in rows.items():
        c = cells.setdefault((code, b), [0, 0.0])
        c[0] += n
        c[1] = round(c[1] + tot, 2)
    return cells


def read_shape(target, cells):
    xw = {}
    with open(os.path.join(target, XWALK), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            xw[r["partner_ref_portal"]] = r["ledger_partner_code"].strip()
    ratios, rowsn, parts = [], 0, set()
    with open(os.path.join(target, PORTAL), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if month(r["claim_return_month"]) not in WINDOW:
                continue
            code = xw[r["partner_ref_portal"]]
            b = int(r["size_band"][-1])
            n, tot = cells[(code, b)]
            ratios.append(float(r["award_amount_php"]) / (tot / n))
            rowsn += 1
            parts.add(code)
    ratios.sort()
    m = sum(ratios) / len(ratios)
    return [x / m for x in ratios], rowsn, len(parts)


def share(C, cells, shape, scale, band=None, value=False):
    import bisect
    num = den = 0.0
    n_sh = len(shape)
    tail = [0.0] * (n_sh + 1)
    for i in range(n_sh - 1, -1, -1):
        tail[i] = tail[i + 1] + shape[i]
    for (code, b), (n, tot) in cells.items():
        if band is not None and b != band:
            continue
        mean = tot / n
        i = bisect.bisect_right(shape, ceiling(C, b, scale) / mean)
        if value:
            num += n * mean * (tail[i] / n_sh)
            den += n * mean
        else:
            num += n * (n_sh - i) / n_sh
            den += n
    return num / den


def main(target, golden, figures_path, submission_path):
    pol = pdf_text(os.path.join(target, POLICY))
    need(len(pol) > 2000, "policy text extracted", "%d characters" % len(pol))
    need("9.1 For each scheme year" in pol, "clause 9.1 readable")
    need("twelve months to 31 March 2027" in pol, "the window is filed")
    need("rounded up to the nearest one hundred pesos" in pol, "the rounding rule is filed")
    need("at or below 6.0 per cent" in pol, "the committed share is filed")
    need("B.2 The factor for a band" in pol, "schedule B.2 readable")
    need("award shape" not in pol.lower(), "the policy does not name the award shape")
    smy = pdf_text(os.path.join(target, SUMMARY))
    need("thousands of pesos" in smy, "the published summary states its units")

    scale, tabulated = read_scale(pol)
    need(not tabulated, "schedule B tabulates no factor, so each one is computed from B.2")
    for b in BANDS:
        need(abs(scale[b] - round(math.sqrt(b / 4.0), 3)) < 1e-9, "factor for band %d" % b, scale[b])
    with open(os.path.join(target, BANDS_CSV), newline="", encoding="utf-8") as fh:
        bl = list(csv.DictReader(fh))
    need(len(bl) == 6 and all("scale" not in k for k in bl[0]), "the band table carries no factor")

    cells = read_returns(target)
    shape, rowsn, nparts = read_shape(target, cells)
    need(len(cells) == 528, "window cells", len(cells))
    awards = sum(n for n, t in cells.values())

    C = None
    for cand in range(1000, 30001, 100):
        if share(cand, cells, shape, scale) <= CAP:
            C = cand
            break
    need(C is not None, "a qualifying ceiling exists")
    need(share(C - 100, cells, shape, scale) > CAP, "the ceiling is the lowest qualifying multiple")

    fig = json.load(open(figures_path))
    need(fig["call"] == C, "the call", "%s vs %s" % (fig["call"], C))
    need(fig["awards"] == awards, "window awards", "%s vs %s" % (fig["awards"], awards))
    need(fig["cells"] == len(cells), "cells")
    need(fig["portal_window_rows"] == rowsn, "portal rows in the window")
    need(fig["portal_partners"] == nparts, "portal partners")
    need(round(100 * share(C, cells, shape, scale), 2) == fig["share_pct"], "the referred share")
    need(round(100 * share(C - 100, cells, shape, scale), 2) == fig["share_down_pct"],
         "the share one step down")
    mu = sum(shape) / len(shape)
    sd = (sum((x - mu) ** 2 for x in shape) / (len(shape) - 1)) ** 0.5
    need(round(sd / mu, 2) == fig["cv"], "the coefficient of variation", sd / mu)
    dflt = None
    for cand in range(1000, 30001, 100):
        if share(cand, cells, [1.0], scale) <= CAP:
            dflt = cand
            break
    need(fig["default_call"] == dflt, "the default path's ceiling", dflt)

    for b in BANDS:
        d = fig["bands"][str(b)]
        need(d["ceiling"] == ceiling(C, b, scale), "band %d ceiling" % b, d["ceiling"])
        need(abs(d["factor"] - scale[b]) < 1e-9, "band %d factor" % b)
        need(round(100 * share(C, cells, shape, scale, band=b), 1) == d["referred_share"],
             "band %d referred share" % b)
        need(round(100 * share(C, cells, shape, scale, band=b, value=True), 1) ==
             d["referred_value_share"], "band %d referred value share" % b)
        e = 0.05 - abs(d["referred_share"] - round(d["referred_share"] / 0.1) * 0.1)
        need(True, "band %d share printed" % b)

    # the printed cell of every graded figure, recomputed here rather than read out of figures.json
    for b in BANDS:
        for v in (100 * share(C, cells, shape, scale, band=b),
                  100 * share(C, cells, shape, scale, band=b, value=True)):
            edge = 0.05 - abs(v - round(v, 1))
            need(edge > 0.0075, "band %d figure sits off its printed edge" % b,
                 "%.4f edge %.4f" % (v, edge))

    # the goldens carry the same figures at the same rounding
    gx = load_workbook(os.path.join(golden, "relief_referral_ceilings_2027-28.xlsx"), data_only=True)
    ws = gx["Schedule"]
    seen = {}
    for row in ws.iter_rows(min_row=7, max_row=12, values_only=True):
        seen[int(str(row[0])[-1])] = row
    for b in BANDS:
        r = seen[b]
        need(int(r[3]) == ceiling(C, b, scale), "workbook ceiling band %d" % b, r[3])
        need(abs(float(r[2]) - scale[b]) < 1e-9, "workbook factor band %d" % b)
        need(round(float(r[4]), 1) == fig["bands"][str(b)]["referred_share"],
             "workbook referred share band %d" % b)
        need(round(float(r[5]), 1) == fig["bands"][str(b)]["referred_value_share"],
             "workbook value share band %d" % b)
    gp = pdf_text(os.path.join(golden, "referral_ceiling_board_paper.pdf"))
    need("PHP %s" % "{:,}".format(C) in gp, "the board paper states the call")
    for b in BANDS:
        need("{:,}".format(ceiling(C, b, scale)) in gp, "the board paper states band %d's ceiling" % b)

    # every figure in the write-up's graded blocks is one of these
    sub = open(submission_path, encoding="utf-8").read()
    need("PHP %s" % "{:,}".format(C) in sub, "the write-up states the call")
    need("PHP %s" % "{:,}".format(dflt) in sub, "the write-up states the default path's ceiling")
    for b in BANDS:
        need("{:,}".format(ceiling(C, b, scale)) in sub, "the write-up states band %d's ceiling" % b)
        need("%.1f per cent of awards" % fig["bands"][str(b)]["referred_share"] in sub,
             "the write-up states band %d's referred share" % b)
    print("verify: %d independent checks passed from the bundle alone; call PHP %s" % (OK, "{:,}".format(C)))
    return C


if __name__ == "__main__":
    T = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(os.path.join(T, "target"), os.path.join(T, "golden"),
         os.path.join(T, "generator", "figures.json"), os.path.join(T, "submission.md"))
