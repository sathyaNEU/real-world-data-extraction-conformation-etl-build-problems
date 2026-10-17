"""Write task154/submission.md from the computed figures (every number from figures.json's objects)."""
from __future__ import annotations

import asks as A
import calc as C
import common as K


def r1(x):
    return K.round_half_up(x, 1)


def r2(x):
    return K.round_half_up(x, 2)


def sg1(x):
    v = r1(x)
    return "+%.1f" % v if v > 0 else ("-%.1f" % -v if v < 0 else "0.0")


def sg2(x):
    v = r2(x)
    return "+%.2f" % v if v > 0 else ("-%.2f" % -v if v < 0 else "0.00")


def mny(x):
    v = r1(x)
    s = "{:,.1f}".format(abs(v))
    return ("+" if v > 0 else "-" if v < 0 else "") + s


def text(B, res, figs):
    g, fa, fb = res["golden"], res["a"], res["b"]
    c = g["contrib"]
    q2 = C.cipi(B, "2026Q2")
    q1 = B["base"]["CIPI_NF"]
    bt = figs["backtest_rmse_m"]["turnover"]
    x2, m2 = C.goods(B, "2026Q2", "x"), C.goods(B, "2026Q2", "m")
    lines = []
    w = lines.append
    w("## Tags")
    w("")
    w("**Domain:** Economics & Econometrics (forecasting and forecast evaluation: a statistical office's first "
      "estimate of quarterly GDP growth).")
    w("**Analytical objective:** Forecasting & Predictive Modeling.")
    w("")
    w("## 1. Final Recommendation")
    w("")
    w("**The Statistics Office's advance estimate will show real GDP growth of %.1f%% at an annualised rate in the June "
      "quarter of 2026.**" % r1(g["ann"]))
    w("Quarterly growth is %.2f%%, with business inventories, each industry's book-value stocks revalued over its own "
      "stockholding period at both quarter ends, taking %.2f percentage points off. Not each industry's book value over "
      "its month-end price index, which reads the rise in import prices inside the stockholding period as a fall in the "
      "volume of stocks bought before it; not the quarter's average index, which reads it the other way; not a "
      "two-month stockholding period for every industry, which ignores each industry's own stock-to-sales ratio."
      % (r2(g["q"]), -r2(c["CIPI_NF"])))
    w("")
    w("## 2. Critical Components")
    w("")
    w("1. The change in business inventories at 2025 prices in the June quarter is **%s million dollars**, after the "
      "March quarter's published **%s million**: a contribution of **%.2f** percentage points."
      % ("{:,.0f}".format(q2), "{:,.0f}".format(q1), r2(c["CIPI_NF"])))
    w("2. Goods exports contribute **%s** and goods imports **%s** percentage points." % (sg2(c["X_G"]), sg2(c["M_G"])))
    w("3. GDP grows **%.2f%%** on the March quarter." % r2(g["q"]))
    w("")
    w("## 3. Step-by-Step Solution")
    w("")
    w("1. Took the June-quarter estimates of the ten lines TBS's bulletin does not feed, with their contributions, and "
      "the March-quarter base from tarbert_gdp_tracker_2026q2.xlsx: March-quarter GDP is %s million dollars."
      % "{:,.0f}".format(B["gdp_q1"]))
    w("2. Rebased the export and import price indexes in so_price_indexes_2026-06.xlsx from 2019 to their 2025 "
      "average and divided the seasonally adjusted April to June values by SITC section in "
      "tbs_merchandise_trade_business_stocks_2026-06.pdf by them (user guide, sources and price measures): goods "
      "exports %s and imports %s million dollars at 2025 prices, against the March quarter's %s and %s."
      % ("{:,.1f}".format(x2), "{:,.1f}".format(m2), "{:,.0f}".format(B["base"]["X_G"]),
         "{:,.0f}".format(B["base"]["M_G"])))
    w("3. For each of the bulletin's eight industries, divided the end-March and end-June book value by the average of "
      "the industry's input price index, rebased to 2025, over the months its stock-to-sales ratio covers at that "
      "date, counted back from the month end: the change in business inventories is %s million dollars at 2025 prices."
      % "{:,.0f}".format(q2))
    w("4. Rebuilt every quarter from 2019Q2 to 2026Q1 the same way from tbs_portal_monthly_2019-01_2026-05.csv: it comes "
      "within %.1f million dollars root mean square of the Office's latest estimates of non-farm business inventories, "
      "the 25 June release in so_realtime_gdp_database.csv." % bt)
    w("5. Took each line's change over March-quarter GDP (user guide, contributions to growth), summed the thirteen "
      "contributions to %.2f%% and compounded to an annual rate (user guide, the headline): %.1f%%."
      % (r2(g["q"]), r1(g["ann"])))
    w("")
    w("## 4. Deliverable Answers")
    w("")
    w("### gdp_preview_2026q2.pdf")
    w("")
    w("1. The call, in the headline and the first sentence: real GDP growth of %.1f%% at an annualised rate, %.2f%% on "
      "the March quarter, in the June quarter of 2026." % (r1(g["ann"]), r2(g["q"])))
    w("2. A chart of each quarter's growth from the June quarter 2023 to the March quarter 2026 in its advance "
      "estimate and in the latest estimates, and the thirteen contributions.")
    w("")
    w("### gdp_preview_2026q2_tables.xlsx")
    w("")
    w("1. The revision from the advance estimate to the latest estimate of annualised growth, percentage points:")
    for q, lab in (("2025Q3", "September quarter 2025"), ("2025Q4", "December quarter 2025"),
                   ("2026Q1", "March quarter 2026")):
        w("   - %s: %s" % (lab, sg1(fa[q])))
    w("2. Over the twelve quarters from June 2023 to March 2026: mean revision %s, mean absolute revision %.2f."
      % (sg2(fa["mean"]), r2(fa["mar"])))
    w("3. The change in the value of coal and of LNG shipped in the June quarter of 2026 on the June quarter of "
      "2025, millions of dollars:")
    for mk in A.MARKETS:
        w("   - %s: coal %s, LNG %s" % (A.MARKET_NAMES[mk], mny(fb[(mk, "32")]), mny(fb[(mk, "34")])))
    w("   - The five markets: coal %s, LNG %s" % (mny(fb[("total", "32")]), mny(fb[("total", "34")])))
    return "\n".join(lines) + "\n"


def write(path, B, res, figs):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text(B, res, figs))
