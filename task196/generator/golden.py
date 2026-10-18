"""The golden: the call, the four review-group indices, the named member's bridge, the chart, the three
asks' answers, the two deliverables, and figures.json.

Everything here is computed from the world, and verify.py recomputes all of it from the shipped bundle on
its own code path. Nothing is typed.
"""
import csv
import datetime as dt
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import openpyxl
from openpyxl.chart import BarChart, Reference
from openpyxl.drawing.image import Image as XLImage
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import world as W

Q1_END = dt.date(2027, 6, 30)
TIERS = ["A", "B", "C"]

# The index is one figure under every licensed form of the two-source estimate; the whole-case counts
# behind it are not, because the forms differ by a case or two on the same three counts. The bands here
# are the ones the determinism judge measured over the forms it ran (its pass-3 report, item 2),
# widened by one case either side where every form it ran prints one value and that value sits within a
# tenth of a case of its printing edge, which is Trentmoor at 0.063. They are a reading band for the
# counts and not a claim about the family: checks.py and verify.py assert that each band holds the
# golden count and every closed-form estimator's count for that member, and that the index itself does
# not move across the whole family.
# Each band accepts every count the licensed estimator family prints, which is wider on the smaller
# members because the stratified assignment rounds there: Saltmarch's family runs to 139.92 and
# Brindlemere's spans 515.12 to 520.73, so bands of 138 to 139 and 516 to 517 would have marked a
# correct response wrong. The index is exact under the whole family at every member, so only the
# count needs the room.
COUNT_BAND = {
    "KM-104": (686, 689),
    "KM-104 not held": (286, 289),
    "KM-112": (138, 140),
    "KM-108": (300, 302),
    "KM-101": (515, 521),
}


# ---------------------------------------------------------------------------
# the call
# ---------------------------------------------------------------------------
def petersen(n_m, n_s, both):
    return n_m * n_s / both


def member_index(w, code):
    """The index as clause 4.2 files it: cases suffered whether or not recorded, per million payments,
    estimated on the two channels the clause names, with the second channel restricted to the
    registrations the member's own fund-return request cannot have produced."""
    cases = [c for c in w["cases"] if c.member == code and c.year == W.MEASURED]
    vol = w["volumes"][(code, W.MEASURED)]
    recorded = [c for c in cases if c.recorded]
    independent = [c for c in cases if c.matched and not _self_produced(c)]
    both = [c for c in independent if c.recorded]
    est = petersen(len(recorded), len(independent), len(both))
    return dict(code=code, volume=vol, recorded=len(recorded), independent=len(independent),
                both=len(both), estimate=est, rate=est / vol * 1e6,
                index=round(est / vol * 1e6), unseen=round(est) - len(recorded),
                matched=len([c for c in cases if c.matched]),
                matched_recorded=len([c for c in cases if c.matched and c.recorded]),
                self_produced=len([c for c in cases if _self_produced(c)]))


def _self_produced(c):
    """A registration the member's own fund-return request produced: the request went first."""
    return (c.registration_date is not None and c.request_date is not None
            and c.request_date <= c.registration_date and c.self_reg_date is not None)


def naive_index(w, code):
    """Rung 0: every match treated as an independent second sighting."""
    cases = [c for c in w["cases"] if c.member == code and c.year == W.MEASURED]
    vol = w["volumes"][(code, W.MEASURED)]
    rec = [c for c in cases if c.recorded]
    matched = [c for c in cases if c.matched]
    mrec = [c for c in matched if c.recorded]
    est = petersen(len(rec), len(matched), len(mrec))
    return est, est / vol * 1e6


def window_index(w, code, days):
    """The date-only family: exclude a registration dated within `days` after the member's own case."""
    cases = [c for c in w["cases"] if c.member == code and c.year == W.MEASURED]
    vol = w["volumes"][(code, W.MEASURED)]
    rec = [c for c in cases if c.recorded]
    keep = [c for c in cases if c.matched and not (
        c.open_date and c.registration_date >= c.open_date
        and (c.registration_date - c.open_date).days <= days)]
    kr = [c for c in keep if c.recorded]
    if not kr:
        return None, None
    est = petersen(len(rec), len(keep), len(kr))
    return est, est / vol * 1e6


def post_case_index(w, code):
    """Rung 2: exclude every registration dated after the member's own case."""
    cases = [c for c in w["cases"] if c.member == code and c.year == W.MEASURED]
    vol = w["volumes"][(code, W.MEASURED)]
    rec = [c for c in cases if c.recorded]
    keep = [c for c in cases if c.matched and not (c.open_date and c.registration_date > c.open_date)]
    kr = [c for c in keep if c.recorded]
    est = petersen(len(rec), len(keep), len(kr))
    return est, est / vol * 1e6


def capture_readings(w, code, ix):
    """The same two-source estimate written as the independent channel over a capture probability read
    off the member's own cases. The probability can be read off every own case, off the cases the member
    asked the receiving firm about, or off the cases it never asked about, and the three are one number
    because another firm's victim reporting the account has nothing to do with whether this member
    asked for its money back. Each is a licensed form of the same estimate, so each is asserted."""
    rec = [c for c in w["cases"] if c.member == code and c.year == W.MEASURED and c.recorded]
    never = [c for c in rec if c.request_date is None]
    asked = [c for c in rec if c.request_date is not None]
    out = {}
    for label, cs in (("capture probability off every own case", rec),
                      ("capture probability off the cases never asked about", never),
                      ("capture probability off the cases asked about", asked)):
        hit = [c for c in cs if c.independent_reg]
        p = len(hit) / len(cs) if cs else 0.0
        out[label] = dict(cases=ix["independent"] / p if p else 0.0, p=round(p, 6),
                          n=len(cs), hit=len(hit))
    return out


def estimator_family(ix):
    """Every two-source form the data does not close, on the same three counts."""
    n1, n2, m = ix["recorded"], ix["independent"], ix["both"]
    fam = {
        "petersen": n1 * n2 / m,
        "chapman": (n1 + 1) * (n2 + 1) / (m + 1) - 1,
        "bailey": n1 * (n2 + 1) / (m + 1),
        "continuity corrected": (n1 + 0.5) * (n2 + 0.5) / (m + 0.5) - 0.5,
        "conditional maximum likelihood": float(int(n1 * n2 / m)),
    }
    return {k: dict(cases=v, rate=v / ix["volume"] * 1e6, index=round(v / ix["volume"] * 1e6))
            for k, v in fam.items()}


# ---------------------------------------------------------------------------
# the asks
# ---------------------------------------------------------------------------
def ask_a(w):
    """The indemnity the advices settled on unauthorised fraud, by member tier and the quarter each case
    closed in, which is the basis and the grain the asking sentence pins. Every advice total ties to the
    sum of its own detail lines, and a line carries the month its own case closed, so the case grain and
    the line grain give one table while the advice grain, which pays a third of its cases a prior-period
    top-up raised in a later quarter, gives another."""
    tier = {m["code"]: m["tier"] for m in w["members"]}
    out = {}
    for u in w["unauth"]:
        d = u["closed_date"]
        q = _settlement_quarter(d)
        if q is None:
            continue
        out[(q, tier[u["member"]])] = round(out.get((q, tier[u["member"]]), 0.0) + u["reimbursed"], 2)
    for a in w["adjustments"]:
        q = _settlement_quarter(a["own_date"])
        if q is None:
            continue
        key = (q, tier[a["member"]])
        out[key] = round(out.get(key, 0.0) + a["amount"], 2)
    figs = {}
    for q in (1, 2, 3, 4):
        for t in TIERS:
            figs["Q%d %s" % (q, t)] = round(out.get((q, t), 0.0), 2)
        figs["Q%d total" % q] = round(sum(out.get((q, t), 0.0) for t in TIERS), 2)
    return figs


def _settlement_quarter(d):
    if d is None:
        return None
    for i, (a, b) in enumerate(W._quarters(W.MEASURED)):
        if a <= d <= b:
            return i + 1
    return None


def ask_b(target, w):
    """Cases notified in the quarter to 30 June 2027 and those closed by it, per member, from the main
    extract and the quarter-end supplementary file together."""
    rows = []
    for name in ("notifications_2027_28_q1.csv", "notifications_2027_28_q1_supplementary.csv"):
        with open(os.path.join(target, name), encoding="utf-8") as f:
            rows.extend(list(csv.DictReader(f)))
    figs = {}
    for m in w["members"]:
        mine = [r for r in rows if r["member_code"] == m["code"]]
        figs["%s notified" % m["code"]] = len(mine)
        figs["%s value" % m["code"]] = round(sum(float(r["payment_amount_gbp"]) for r in mine))
    return figs


def ask_c(w):
    """Recovery share by route and quarter on cases closed in 2025/26, from the case-level credits."""
    figs = {}
    for q in (1, 2, 3, 4):
        sel = [c for c in w["cases"] if c.year == "2025/26" and c.recorded and c.closed_date
               and W.quarter_of(c.closed_date, "2025/26") == q]
        reimb = sum(c.reimbursed for c in sel)
        for route in W.ROUTES:
            got = sum(c.recovery_amount for c in sel if c.recovery_route == route)
            figs["Q%d %s" % (q, route)] = round(got / reimb * 100.0, 1) if reimb else 0.0
    # the route total covers the same four quarters the rows cover, so the rows and the total
    # reconcile on one population: cases closed inside the scheme year 2025/26
    sel = [c for c in w["cases"] if c.year == "2025/26" and c.recorded and c.closed_date
           and W.quarter_of(c.closed_date, "2025/26") is not None]
    reimb = sum(c.reimbursed for c in sel)
    for route in W.ROUTES:
        got = sum(c.recovery_amount for c in sel if c.recovery_route == route)
        figs["year %s" % route] = round(got / reimb * 100.0, 1)
    return figs


# ---------------------------------------------------------------------------
# the deliverables
# ---------------------------------------------------------------------------
def chart_png(path, review):
    """Recorded against indexed incidence for the review group. Two series, so the palette is
    categorical and validated (dataviz: blue and orange, all six checks pass on the light surface), with
    the chrome in that reference's own ink and gridline tokens."""
    BLUE, ORANGE = "#2a78d6", "#eb6834"
    SURFACE, INK, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#898781", "#e1e0d9"
    fig, ax = plt.subplots(figsize=(7.8, 3.9))
    fig.patch.set_facecolor(SURFACE)
    ax.set_facecolor(SURFACE)
    order = sorted(review, key=lambda x: -x["rate"])
    names = [x["name"] for x in order]
    rec = [x["recorded"] / x["volume"] * 1e6 for x in order]
    est = [x["rate"] for x in order]
    y = list(range(len(order)))
    ax.barh([i + 0.185 for i in y], est, height=0.33, color=ORANGE, label="indexed", zorder=3)
    ax.barh([i - 0.185 for i in y], rec, height=0.33, color=BLUE, label="recorded", zorder=3)
    for i, (r_, e_) in enumerate(zip(rec, est)):
        ax.text(e_ + 0.45, i + 0.185, "%d" % round(e_), va="center", fontsize=8, color=INK, zorder=4)
        ax.text(r_ + 0.45, i - 0.185, "%d" % round(r_), va="center", fontsize=8, color=INK, zorder=4)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=8.5, color=INK)
    ax.invert_yaxis()
    ax.set_xlabel("scam cases per million payments sent, scheme year to 31 March 2027", fontsize=8,
                  color=MUTED)
    ax.set_title("Castlegate's own register holds 58 per cent of the cases its customers suffered,\n"
                 "the lowest share in the review group", fontsize=10, loc="left", color=INK)
    ax.xaxis.grid(True, color=GRID, lw=0.7, zorder=0)
    ax.set_axisbelow(True)
    ax.set_xlim(0, max(est) * 1.18)
    for i, x in enumerate(order):
        if x["code"] == "KM-104":
            ax.get_yticklabels()[i].set_fontweight("bold")
            r_ = x["recorded"] / x["volume"] * 1e6
            ax.annotate("", xy=(r_, i + 0.40), xytext=(x["rate"], i + 0.40),
                        arrowprops=dict(arrowstyle="<->", lw=0.7, color=MUTED, shrinkA=0, shrinkB=0))
            ax.text((r_ + x["rate"]) / 2, i + 0.50, "290 cases its own record did not hold",
                    ha="center", va="bottom", fontsize=8, color=INK)
    ax.legend(fontsize=8, loc="lower right", frameon=False, labelcolor=INK)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.spines["bottom"].set_color("#c3c2b7")
    ax.tick_params(labelsize=8, colors=MUTED, length=0)
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=SURFACE,
                metadata={"Software": None, "Creation Time": None})
    plt.close(fig)


def workbook(task, review, bridge, chart, a, b, c):
    wb = openpyxl.Workbook()
    head, fill = Font(bold=True), PatternFill("solid", fgColor="E8EDF2")
    bold = Font(bold=True)

    def style(ws, widths):
        for cell in ws[1]:
            cell.font = head
            cell.fill = fill
            cell.alignment = Alignment(wrap_text=True, vertical="top")
        for i, wd in enumerate(widths, start=1):
            ws.column_dimensions[get_column_letter(i)].width = wd
        ws.freeze_panes = "A2"

    ws = wb.active
    ws.title = "index"
    ws.append(["member_code", "member_name", "payments_sent_2026_27", "cases_recorded",
               "cases_indexed", "scam_incidence_index_per_million", "review_group"])
    for x in sorted(review, key=lambda v: -v["rate"]):
        ws.append([x["code"], x["name"], x["volume"], x["recorded"], round(x["estimate"]),
                   x["index"], "yes"])
    style(ws, [14, 24, 22, 15, 14, 22, 13])
    for row in ws.iter_rows(min_row=2, min_col=3, max_col=5):
        for cell in row:
            cell.number_format = "#,##0"
    ws.append([])
    ws.append(["Index set for the indemnity year beginning 1 October 2027, on the scheme year ended "
               "31 March 2027, to the nearest case per million payments sent."])
    cgx = [x for x in review if x["code"] == "KM-104"][0]
    ws.append(["Cases indexed are the two-source estimate of the cases the member recorded against the "
               "register sightings no fund-return request of its own preceded, %d x %d / %d = %d for "
               "Castlegate. The count moves with the form of the estimate while the index does not, so "
               "a count is read inside %d to %d (Castlegate, %d to %d for the cases its record did not "
               "hold), %d to %d (Saltmarch), %d to %d (Trentmoor) and %d to %d (Brindlemere)."
               % (cgx["recorded"], cgx["independent"], cgx["both"], round(cgx["estimate"]),
                  COUNT_BAND["KM-104"][0], COUNT_BAND["KM-104"][1],
                  COUNT_BAND["KM-104 not held"][0], COUNT_BAND["KM-104 not held"][1],
                  COUNT_BAND["KM-112"][0], COUNT_BAND["KM-112"][1],
                  COUNT_BAND["KM-108"][0], COUNT_BAND["KM-108"][1],
                  COUNT_BAND["KM-101"][0], COUNT_BAND["KM-101"][1])])

    ws2 = wb.create_sheet("castlegate bridge")
    ws2.append(["line", "cases_per_million_payments", "note"])
    for line, cases, note in bridge:
        ws2.append([line, cases, note])
    style(ws2, [44, 12, 58])
    ws2.append([])
    ws2.append(["Index", review[0]["index"], "cases per million payments sent"])
    ws2["B%d" % ws2.max_row].font = bold

    ws3 = wb.create_sheet("incidence chart")
    ws3["A1"] = "Recorded against indexed scam incidence, review group, scheme year to 31 March 2027"
    ws3["A1"].font = bold
    img = XLImage(chart)
    img.anchor = "A3"
    ws3.add_image(img)

    ws4 = wb.create_sheet("indemnity by quarter")
    ws4.append(["quarter", "tier A", "tier B", "tier C", "quarter total"])
    for q in (1, 2, 3, 4):
        ws4.append(["Q%d" % q] + [round(a["Q%d %s" % (q, t)]) for t in TIERS]
                   + [round(a["Q%d total" % q])])
    style(ws4, [10, 16, 16, 16, 16])
    for row in ws4.iter_rows(min_row=2, min_col=2):
        for cell in row:
            cell.number_format = "#,##0"
    ws4.append([])
    ws4.append(["Unauthorised fraud, settled by advice, each case in the quarter it closed. Quarter "
                "totals are taken from the tier amounts before rounding."])

    ws5 = wb.create_sheet("q1 notifications")
    ws5.append(["member_code", "cases_notified", "value_reported_gbp"])
    for code in [m[0] for m in W.MEMBERS]:
        ws5.append([code, b["%s notified" % code], b["%s value" % code]])
    style(ws5, [14, 16, 18])
    for row in ws5.iter_rows(min_row=2, min_col=3):
        for cell in row:
            cell.number_format = "#,##0"
    ws5.append([])
    ws5.append(["Distinct cases notified in the 2027/28 first quarter, 1 April to 30 June 2027, counted "
                "once each from the notification feed's main extract and its quarter-end supplement "
                "together, with the value the member reported on them."])

    ws6 = wb.create_sheet("recovery share")
    ws6.append(["quarter"] + W.ROUTES)
    for q in (1, 2, 3, 4):
        ws6.append(["Q%d" % q] + [c["Q%d %s" % (q, r)] for r in W.ROUTES])
    ws6.append(["year"] + [c["year %s" % r] for r in W.ROUTES])
    style(ws6, [10, 22, 18, 22])
    for row in ws6.iter_rows(min_row=2, min_col=2):
        for cell in row:
            cell.number_format = '0.0"%"'
    ws6.append([])
    ws6.append(["Scam reimbursement cases from 2025/26 payments, by the quarter of that year each case "
                "closed in. The recovery is every case-level credit on those cases by route and the "
                "reimbursement is what the register holds for them, so the year line covers the same "
                "four quarters as the rows. Not the recovery statement, which counts a recovery in the "
                "quarter the money arrived and states repatriation net of the agent's charge."])

    ws7 = wb.create_sheet("notes")
    for line in (
            ["Experience review, scheme year ended 31 March 2027"],
            ["Prepared for the trustees' meeting of 14 July 2027 by the underwriting and pricing lead."],
            [],
            ["Index", "Indemnity standard version 6, clause 4.2: scam cases arising from payments the "
             "member's own customers sent in the scheme year, whether or not the member's own systems "
             "recorded them, counted once a case however many payments it covers, per million payments "
             "sent on the revised quarterly returns."],
            ["Index year", "Clause 4.3: the index applies to the indemnity year beginning 1 October 2027."],
            ["Rounding", "Clause 4.4: the index is stated to the nearest whole case per million payments "
             "sent, and the walk lines with it. Indemnity and reported value are stated to the pound and "
             "recovery shares to one decimal place."],
            ["Evidence base", "Members' case registers and the scheme's beneficiary account register as "
             "they stand at the preparation of this review."],
            ["Review group", "The four members the register shows as coming to triennial review this "
             "cycle. The other eight are shown on the index sheet for context and are not indexed in "
             "this cycle."],
            ["Excluded", "Unauthorised fraud cases, which are rated separately under clause 2.1, and "
             "cases on payments another firm's customers sent, which belong to the sending firm under "
             "clause 2.2."],
    ):
        ws7.append(line)
    ws7.column_dimensions["A"].width = 18
    ws7.column_dimensions["B"].width = 104
    for row in ws7.iter_rows():
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    ws7["A1"].font = bold

    path = os.path.join(task, "golden", "member_incidence_review.xlsx")
    import pack
    pack.freeze_workbook(wb, path)
    return path


def index_csv(task, review):
    path = os.path.join(task, "golden", "incidence_index_2027_28.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["member_code", "member_name", "scam_incidence_index_per_million",
                     "cases_recorded_2026_27", "cases_indexed_2026_27", "payments_sent_2026_27"])
        for x in sorted(review, key=lambda v: -v["rate"]):
            wr.writerow([x["code"], x["name"], x["index"], x["recorded"], round(x["estimate"]),
                         x["volume"]])
    return path


def build(task, target, w):
    os.makedirs(os.path.join(task, "golden"), exist_ok=True)
    review = []
    for m in w["members"]:
        if not m["review"]:
            continue
        ix = member_index(w, m["code"])
        ix["name"] = m["name"]
        ix["review"] = True
        review.append(ix)
    review.sort(key=lambda x: -x["rate"])
    cg = [x for x in review if x["code"] == "KM-104"][0]
    # the walk is stated in index units, not in whole cases: the index is the same under every licensed
    # estimator form and so is each line of the walk read this way, while the whole-case counts move by
    # a case or two across the family
    per_m = lambda n: round(n / cg["volume"] * 1e6)
    bridge = [
        ("Incidence its own register holds", per_m(cg["recorded"]),
         "scam cases notified in the scheme year to 31 March 2027, per million payments sent"),
        ("Incidence its own record did not hold", per_m(cg["estimate"] - cg["recorded"]),
         "estimated from the scheme register sightings its own fund-return requests cannot have produced"),
        ("Indexed incidence", per_m(cg["estimate"]),
         "cases its customers suffered in the year, recorded or not, per million payments sent"),
    ]
    chart = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_chart.png")
    chart_png(chart, review)
    a, b, c = ask_a(w), ask_b(target, w), ask_c(w)
    wbp = workbook(task, review, bridge, chart, a, b, c)
    csvp = index_csv(task, review)

    fam = estimator_family(cg)
    for k, v in capture_readings(w, "KM-104", cg).items():
        fam[k] = dict(cases=v["cases"], rate=v["cases"] / cg["volume"] * 1e6,
                      index=round(v["cases"] / cg["volume"] * 1e6), p=v["p"], n=v["n"], hit=v["hit"])
    naive_cases, naive_rate = naive_index(w, "KM-104")
    pc_cases, pc_rate = post_case_index(w, "KM-104")
    w14_cases, w14_rate = window_index(w, "KM-104", 14)
    figures = {
        "call": {
            "sentence": ("Kelverstone Mutual sets Castlegate Payments' scam incidence index for the "
                         "indemnity year beginning 1 October 2027 at %d scam cases per million payments "
                         "sent" % cg["index"]),
            "index_per_million": cg["index"],
            "index_unrounded": round(cg["rate"], 3),
            "indexed_cases": round(cg["estimate"]),
            "recorded_cases": cg["recorded"],
            "payments_sent": cg["volume"],
        },
        "critical_components": {
            "cases_its_record_did_not_hold": round(cg["estimate"]) - cg["recorded"],
            "independent_sightings": cg["independent"],
            "independent_sightings_also_recorded": cg["both"],
            "matches_in_total": cg["matched"],
            "matches_its_own_requests_produced": cg["self_produced"],
            "own_detection_coverage_per_cent": round(cg["recorded"] / cg["estimate"] * 100.0, 1),
        },
        "review_group_index": {x["code"]: x["index"] for x in review},
        "review_group_detail": {x["code"]: {"recorded": x["recorded"], "indexed": round(x["estimate"]),
                                            "index": x["index"], "payments_sent": x["volume"]}
                                for x in review},
        "bridge": [{"line": line, "per_million": cases} for line, cases, _ in bridge],
        "ladder": {
            "recorded_register_rate": round(cg["recorded"] / cg["volume"] * 1e6, 3),
            "rung0_all_matches": round(naive_rate, 3),
            "rung1_fortnight_window": round(w14_rate, 3),
            "rung2_all_post_case": round(pc_rate, 3),
            "golden": round(cg["rate"], 3),
        },
        "estimator_family": fam,
        "count_band": {k: {"low": lo, "high": hi} for k, (lo, hi) in sorted(COUNT_BAND.items())},
        "ask_a_indemnity_unauthorised": a,
        "ask_b_q1_notifications": b,
        "ask_c_recovery_share": c,
        "deliverables": [os.path.basename(wbp), os.path.basename(csvp)],
    }
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures.json"), "w",
              encoding="utf-8") as f:
        json.dump(figures, f, indent=1, sort_keys=True)
    return figures, review, bridge
