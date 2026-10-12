"""The golden deliverable freeze_gate_2026.html, generator/figures.json (every owed figure as the write-up
states it) and submission.md drafted from those figures."""
import html
import json
import os

import world as W
import estimate as E

TASK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GOLDEN_FILE = "freeze_gate_2026.html"


def money(x):
    return "£{:,.0f}".format(round(x, -3))


def cases(x):
    return "{:,.0f}".format(round(x, -2))


def figures(est, ask_a, ask_b, faces_total):
    share = {n: int(round(est[n][E.GOLDEN_KEY])) for n in W.NAMES}
    qual = [n for n in W.NAMES if est[n][E.GOLDEN_KEY] >= W.LINE]
    order = sorted(W.NAMES, key=lambda n: -ask_b[n])
    return {
        "call": {"qualify": qual, "supervised": [n for n in W.NAMES if n not in qual], "line": "97.0"},
        "in_scope_faces": "{:,}".format(faces_total),
        "share_whole_pc": share,
        "share_unrounded": {n: round(est[n][E.GOLDEN_KEY], 2) for n in W.NAMES},
        "stock_value_gbp": {n: money(ask_a[n]) for n in W.NAMES},
        "forecast_cases": {n: cases(ask_b[n]) for n in W.NAMES},
        "chart_order": order,
        "chart_title_centre": order[0],
        "conventions": {"standard_clauses": ["4.1", "4.4", "4.5", "5.1"], "stock_rounding": "1,000",
                        "survival_base": "1"},
        "dates": ["06:00 on 7 December 2026", "6 December", "7 December", "3 January", "4 January 2027", "27 December",
                  "26 December", "23 November"],
    }


CSS = """
:root{--surface:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--rule:#d9d8d3;--bar:#2a78d6;--bar-top:#1b5aa6;--ok:#0b6b2e;--hold:#9a3b0b}
body{background:var(--surface);color:var(--ink);font:14px/1.45 "Segoe UI",Calibri,Arial,sans-serif;margin:24px auto;max-width:980px;padding:0 16px}
h1{font-size:20px;margin:0 0 4px}
.sub{color:var(--ink2);margin:0 0 18px}
table{border-collapse:collapse;width:100%;margin:8px 0 6px}
th,td{border-bottom:1px solid var(--rule);padding:6px 8px;text-align:right;white-space:nowrap}
th{font-weight:600;color:var(--ink2);border-bottom:2px solid var(--ink2)}
td:first-child,th:first-child{text-align:left}
td.v-ok{color:var(--ok);font-weight:600}
td.v-hold{color:var(--hold);font-weight:600}
.note{color:var(--ink2);font-size:12px;margin:4px 0}
h2{font-size:15px;margin:26px 0 4px}
svg text{font-family:"Segoe UI",Calibri,Arial,sans-serif}
"""


def chart_svg(ask_b, order):
    w, h, left, top, bar_h, gap = 900, 364, 120, 16, 30, 8
    vmax = max(ask_b.values())
    scale = (w - left - 140) / vmax
    out = ['<svg viewBox="0 0 %d %d" width="100%%" role="img" aria-label="Forecast cases by centre over the freeze">' % (w, h)]
    ticks = [0, 200000, 400000, 600000, 800000, 1000000]
    base_y = top + len(order) * (bar_h + gap)
    for t in ticks:
        x = left + t * scale
        out.append('<line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#e6e5e0" stroke-width="1"/>' % (x, top - 4, x, base_y))
        out.append('<text x="%.1f" y="%d" font-size="11" fill="#52514e" text-anchor="middle">%s</text>'
                   % (x, base_y + 16, "{:,}".format(t) if t else "0"))
    for i, n in enumerate(order):
        y = top + i * (bar_h + gap)
        bw = ask_b[n] * scale
        col = "var(--bar-top)" if i == 0 else "var(--bar)"
        out.append('<g><title>%s: %s cases</title>' % (n, cases(ask_b[n])))
        out.append('<text x="%d" y="%.1f" font-size="13" fill="#0b0b0b" text-anchor="end">%s</text>' % (left - 8, y + bar_h / 2 + 4.5, n))
        out.append('<path d="M%d,%d h%.1f a4,4 0 0 1 4,4 v%d a4,4 0 0 1 -4,4 h-%.1f z" fill="%s"/>'
                   % (left, y, bw - 4, bar_h - 8, bw - 4, col))
        out.append('<text x="%.1f" y="%.1f" font-size="12.5" fill="#0b0b0b">%s</text></g>' % (left + bw + 6, y + bar_h / 2 + 4.5, cases(ask_b[n])))
    out.append('<text x="%.1f" y="%d" font-size="11" fill="#52514e" text-anchor="middle">cases, trading days 7 December to 3 January</text>'
               % (left + (w - left - 140) / 2, base_y + 32))
    out.append("</svg>")
    return "\n".join(out)


def page(est, ask_a, ask_b, figs):
    order = figs["chart_order"]
    rows = []
    for n in W.NAMES:
        q = n in figs["call"]["qualify"]
        rows.append("<tr><td>%s</td><td>%d%%</td><td>97.0%%</td><td class=\"%s\">%s</td><td>%s</td><td>%s</td></tr>" % (
            n, figs["share_whole_pc"][n], "v-ok" if q else "v-hold", "Qualifies" if q else "Does not qualify (supervised)",
            figs["stock_value_gbp"][n], figs["forecast_cases"][n]))
    sup = " and ".join(figs["call"]["supervised"])
    top = order[0]
    body = """<!doctype html>
<html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Thornacre peak gate 2026, record accuracy at the stand-down</title>
<style>%(css)s</style></head>
<body>
<h1>Six of our eight centres meet SCS-07 at the stand-down; %(sup)s stay on supervised replenishment</h1>
<p class="sub">Corderoy Logistics, Inventory Control and BI. Measurement time 06:00 on 7 December 2026 (SCS-07 4.4); freeze 06:00 on 7 December 2026 to 06:00 on 4 January 2027.</p>

<p>No full count was taken at 06:00, so each centre's record accuracy is the SCS-07 4.5 estimate: what a full count of its in-scope pick faces at the stand-down would be expected to find. Every count posts the confirmed quantity as the record, so a face is as good as its last count and drifts only with the trading days since. We fitted, centre by centre and class by class, the per-day chance of a record going wrong from the routine (CYC) counts, each measured from the face's previous count of any kind, and applied it to the days each in-scope face had run since its own last count of any kind (none for a face counted on the night of 6 December). Exception counts are raised because something looked wrong, so they are not used to fit the rate; they still reset the faces they counted.</p>

<table>
<thead><tr><th>Centre</th><th>Record accuracy, 06:00 7 Dec</th><th>SCS-07 line</th><th>Peak gate</th><th>Thornacre stock on gate faces</th><th>Forecast cases, freeze</th></tr></thead>
<tbody>
%(rows)s
</tbody></table>
<p class="note">Record accuracy in whole per cents; the gate is applied to the unrounded estimate. Gate faces are SCS-07 4.1 pick faces: slotted to a Thornacre line on the location master at 06:00 on 7 December and not on QA hold or recall.</p>
<p class="note">Stock value: the 06:00 stock-by-location quantity taken once per face (the WMS repeats the face total on each batch row; batches checked against the batch register), eaches converted at the case size valid on 7 December, at Thornacre cost per case with the period 10 changes effective 6 December applied over the 28 November list. Nearest £1,000.</p>
<p class="note">Forecast cases: run of 23 November over the 28 trading days of the freeze, each store-day assigned to the depot on the servicing map for that date (PZ26-04 from 7 December, part of it reverting on 27 December), single-pick categories converted from units at the category table's units per case, and store-days the trading calendar shows closed (including the Boxing Day closures added on 1 December) removed. Nearest hundred.</p>

<h2>%(top)s draws the most over the freeze</h2>
<p class="sub">Forecast cases by centre, 7 December to 3 January, largest first</p>
%(svg)s
</body></html>
""" % dict(css=CSS, rows="\n".join(rows), sup=html.escape(sup), top=top, svg=chart_svg(ask_b, order))
    return body


def submission(figs):
    q, s = figs["call"]["qualify"], figs["call"]["supervised"]
    sh, sv, fc = figs["share_whole_pc"], figs["stock_value_gbp"], figs["forecast_cases"]
    def lst(xs):
        return ", ".join(xs[:-1]) + " and " + xs[-1]
    text = """# task229: Thornacre peak gate 2026

## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).
**Analytical objective:** Data Quality Monitoring & Alerting.

## 1. Final Recommendation

**%(q)s meet Thornacre's peak stock-record standard and run replenishment unattended through the freeze; %(s)s stay on supervised replenishment.**

%(est)s against the 97.0%% line at 06:00 on 7 December 2026. Not the share of count tasks that matched, which reads each record before the count corrected it and passes no centre. Not the routine counts weighted to the A, B and C mix, which measures records at the end of their cycle rather than at the stand-down and passes only Magor and Hinckley.

## 2. Critical Components

1. In-scope faces at 06:00 on 7 December under SCS-07 4.1: **%(faces)s**
2. A count posts the confirmed quantity as the record, so each face's state at 06:00 runs from its own last count of any kind
3. The per-day chance of a record going wrong is fitted by class from the CYC counts, each measured from the face's previous count of any kind; exception counts (SHP, NEG, EMP, OVR) reset faces but are not fitted
4. Record accuracy at the stand-down: %(comp)s

## 3. Step-by-Step Solution

1. Took the SCS-07 4.1 faces from wms_location_master_THN_eff.csv (PICK, client THN, a Thornacre line, ACTIVE on 2026-12-07): %(faces)s faces.
2. Joined THN_pickface_count_history_20260601_20261207.csv to them on site and location, each count on the trading day of its counted_utc in UK time (06:00 to 06:00).
3. For every CYC count with an earlier count of any kind on the same face, took the trading days since that count as exposure and fitted per centre and class the per-day chance p of a VARIANCE result by maximum likelihood on P(MATCH) = (1 - p)^days.
4. Gave each in-scope face (1 - p)^d, d the trading days from its last count of any kind to the night of 6 December, and averaged by centre: %(comp)s.
5. Compared each with 97.0 per cent (SCS-07 5.1): %(q)s qualify.
6. Stock value: WMS_stock_by_location_THN_20261207_0600.csv qty once per gate face, eaches divided by the case size valid on 7 December, times cost per case from THN_cost_price_list_20261128.csv overridden by THN_cost_changes_P10_2026.csv (effective 6 December).
7. Forecast cases: THN_store_replen_forecast_run_20261123.csv for 7 December to 3 January, depot from THN_store_servicing_map.csv valid on each trading date, EA rows divided by units_per_case, store-days CLOSED in THN_store_trading_calendar_2026_27.csv removed.
8. Recommendation: %(q)s run unattended; %(s)s are supervised.

## 4. Deliverable Answers

### freeze_gate_2026.html
1. Share of correct records at 06:00 on 7 December, whole per cents, against the 97.0%% line:
%(shares)s
2. Thornacre stock value on the gate's faces, nearest £1,000:
%(values)s
3. Cases forecast to be drawn over the freeze, nearest hundred:
%(fcs)s
4. Bar chart of the forecast cases, one bar per centre, largest first (%(order)s), each bar labelled with its value, titled "%(top)s draws the most over the freeze".
""" % dict(q=lst(q), s=lst(s), est=("%s and %s both estimate at %d%%" % (s[0], s[1], sh[s[0]]) if sh[s[0]] == sh[s[1]]
                else "%s and %s estimate at %d%% and %d%%" % (s[0], s[1], sh[s[0]], sh[s[1]])), faces=figs["in_scope_faces"],
           comp=", ".join("%s %d%%" % (n, sh[n]) for n in W.NAMES),
           shares="\n".join("   - %s: %d%%, %s" % (n, sh[n], "qualifies" if n in q else "does not qualify") for n in W.NAMES),
           values="\n".join("   - %s: %s" % (n, sv[n]) for n in W.NAMES),
           fcs="\n".join("   - %s: %s cases" % (n, fc[n]) for n in W.NAMES),
           order=", ".join(figs["chart_order"]), top=figs["chart_title_centre"])
    return text


def main(target, golden_dir, est, ask_a, ask_b, faces_total):
    os.makedirs(golden_dir, exist_ok=True)
    figs = figures(est, ask_a, ask_b, faces_total)
    with open(os.path.join(golden_dir, GOLDEN_FILE), "w") as fh:
        fh.write(page(est, ask_a, ask_b, figs))
    with open(os.path.join(TASK, "generator", "figures.json"), "w") as fh:
        json.dump(figs, fh, indent=1)
        fh.write("\n")
    with open(os.path.join(TASK, "submission.md"), "w") as fh:
        fh.write(submission(figs))
    return figs
