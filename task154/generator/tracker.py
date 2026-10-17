"""Tarbert Economics' GDP tracker as at 08:00 on Tuesday 28 July 2026: each expenditure line's June-quarter estimate
from the desk's sources, the three lines TBS's June bulletin feeds left open. The household line is the design
parameter that places the call: its June-quarter level is set so the golden lands where the design note says."""
from __future__ import annotations

import common as K
import national as NA

GOLDEN_TARGET = 2.794          # per cent at an annualised rate, the design's placement inside its bin

# tracker label, Office component, June-quarter change on the March quarter (design), the desk's source
LINES = [
    ("Household consumption", "HFCE", None,
     "SO monthly household spending indicator Apr-Jun (14 Jul), deflated by the June quarter CPI (15 Jul)"),
    ("Government consumption", "GFCE", 0.0040, "Treasury monthly statements Apr-May; June from the Budget profile"),
    ("Dwelling investment", "GFCF_DW", -0.0150, "SO building activity indicator, consents to May"),
    ("Machinery and equipment", "GFCF_ME", -0.0250, "SO capital expenditure survey, June quarter early returns"),
    ("Non-dwelling construction", "GFCF_NDC", 0.0030, "SO construction work done survey, early returns"),
    ("Intellectual property products", "GFCF_IPP", 0.0060, "Trend"),
    ("Public investment", "GFCF_PUB", 0.0050, "Treasury monthly statements Apr-May"),
    ("Farm and other inventories", "CIPI_FO", 40.0, "SO livestock and crop indicators"),
    ("Services exports", "X_S", 0.0050, "SO visitor arrivals and spending, Apr-Jun"),
    ("Services imports", "M_S", -0.0030, "SO resident departures, Apr-Jun"),
    ("Goods exports", "X_G", "TBS", "TBS June bulletin (due 22 Jul, delayed)"),
    ("Goods imports", "M_G", "TBS", "TBS June bulletin (due 22 Jul, delayed)"),
    ("Business inventories", "CIPI_NF", "TBS", "TBS June bulletin (due 22 Jul, delayed)"),
]
OPEN = ("X_G", "M_G", "CIPI_NF")


def build(W, bulletin_q2):
    """bulletin_q2: the June-quarter levels of the three open lines as the golden builds them ($m, 2025 prices).
    Returns the tracker's June-quarter estimates ($m, whole) for the lines it carries, HFCE solved."""
    q1 = NA.QI["2026Q1"]
    base = {c: W.NA[c][q1] for _, c, _, _ in LINES}
    gdp1 = W.NA["GDP"][q1]
    est = {}
    for label, c, g, src in LINES:
        if g is None or g == "TBS":
            continue
        est[c] = round(g) if c == "CIPI_FO" else round(base[c] * (1.0 + g))
    target_q = ((1.0 + GOLDEN_TARGET / 100.0) ** 0.25 - 1.0) * 100.0
    known = sum(NA.SIGN[c] * (est[c] - base[c]) for c in est)
    known += sum(NA.SIGN[c] * (bulletin_q2[c] - base[c]) for c in OPEN)
    est["HFCE"] = round(base["HFCE"] + target_q / 100.0 * gdp1 - known)
    W.TRACK = est
    W.TRACK_BASE = base
    return est


def contributions(W):
    q1 = NA.QI["2026Q1"]
    gdp1 = W.NA["GDP"][q1]
    return {c: NA.SIGN[c] * (W.TRACK[c] - W.TRACK_BASE[c]) / gdp1 * 100.0 for c in W.TRACK}
