"""The golden deliverables, computed from target/ alone: the finance manager's memo to the board (DOCX, with the fee
table and the monthly chart) and the conformed brokerage fee ledger (CSV); and generator/figures.json, every figure the
write-up states."""
import csv
import datetime as dt
import io
import json
import math
import os

import numpy as np
import pandas as pd

import bundle as B
import methods as M
import world as W


def compute(target):
    c = B.counts(target)
    amount = B.budget_amount(target)
    rec = M.recorded(c)
    q = M.restated(c)
    fee = M.fee_for(amount, q)
    kept_s = M.share_kept(c, W.STATION_ZONES)
    kept_o = M.share_kept(c, W.OTHER_ZONES)
    kept_all = M.share_kept(c, W.CITY_ZONES)
    own_kept = rec / M.n(c, M.PRE, "P")
    rivals = {"own_fall": dict(share=1 - own_kept, pickups=M.rung0(c), fee=M.fee_for(amount, M.rung0(c))),
              "all_dropoffs": dict(share=1 - kept_all, pickups=M.rung1(c), fee=M.fee_for(amount, M.rung1(c))),
              "none": dict(share=0.0, pickups=float(rec), fee=M.fee_for(amount, rec))}
    lo, hi = M.flip(rec, amount, fee)
    led = M.ledger(B.ledger_pickups(target))
    monthly = monthly_series(c)
    return dict(amount=amount, recorded=rec, restated=q, fee=fee, share=1 - rec / q, kept_s=kept_s, kept_o=kept_o,
                kept_all=kept_all, rivals=rivals, flip=(lo, hi), settings=M.settings(amount, q),
                surplus=fee * q - amount, shortfall=(fee - W.FEE_STEP) * q - amount, ledger=led, monthly=monthly,
                pre_pickups=M.n(c, M.PRE, "P"))


def monthly_series(c):
    d = pd.to_datetime(c["date"])
    g = c.assign(month=d.dt.strftime("%Y-%m")).groupby(["month", "dir"])["n"].sum().unstack(fill_value=0)
    g = g[(g.index >= "2023-11") & (g.index <= "2026-08")]
    return [(m, int(r["P"]), int(r["D"])) for m, r in g.iterrows()]


def r2(v):
    return "%.2f" % (math.floor(v * 100 + 0.5 + 1e-9) / 100.0)


def money(v):
    return "{:,.2f}".format(v)


def figures(fx):
    k10 = lambda v: "{:,}".format(abs(M.round_to(v, 10000)))
    return {
        "call": {"fee_2027": r2(fx["fee"]), "fee_2026": r2(W.FEES[2026])},
        "components": {"recorded_2025": "{:,}".format(fx["recorded"]),
                       "restated_2025": "{:,}".format(M.round_to(fx["restated"], 1000)),
                       "share_cost_pct": "%d" % M.round_to(100 * fx["share"], 1),
                       "amount_2027": "{:,}".format(int(round(fx["amount"])))},
        "surplus_at_fee": k10(fx["surplus"]), "shortfall_one_step_below": k10(fx["shortfall"]),
        "settings": [{"fee": r2(s["fee"]), "recovers": "yes" if s["recovers"] else "no"} for s in fx["settings"]],
        "flip_pct": {"lo": "%.1f" % (100 * fx["flip"][0]), "hi": "%.1f" % (100 * fx["flip"][1])},
        "strata_pct": {"station_zones": "%.1f" % (100 * (1 - fx["kept_s"])), "other_zones": "%.1f" % (100 * (1 - fx["kept_o"]))},
        "rivals": {kk: {"share_pct": "%d" % M.round_to(100 * v["share"], 1), "fee": r2(v["fee"])}
                   for kk, v in fx["rivals"].items()},
        "pre_pickups": "{:,}".format(fx["pre_pickups"]),
        "ledger": [{"month": r.month, "brokerage_id": int(r.brokerage), "pickups": "{:,}".format(int(r.pickups)),
                    "pickups_raw": int(r.pickups), "owed": money(r.owed)} for r in fx["ledger"].itertuples()],
        "ledger_totals": {**{"2025_%d" % b: {"pickups": "{:,}".format(int(g.pickups.sum())), "owed": money(g.owed.sum())}
                             for b, g in fx["ledger"][fx["ledger"].month < "2026"].groupby("brokerage")},
                          **{"2026_%d" % b: {"pickups": "{:,}".format(int(g.pickups.sum())), "owed": money(g.owed.sum())}
                             for b, g in fx["ledger"][fx["ledger"].month >= "2026"].groupby("brokerage")}},
        "ledger_rows": str(len(fx["ledger"])),
        "stated": {"menu": [r2(f) for f in W.MENU], "sections": ["4.3", "4.4"], "budget_line": "12",
                   "change_day": W.CHANGE.isoformat(), "return_day": W.RETURN.isoformat(),
                   "fees": {str(y): r2(f) for y, f in W.FEES.items()}},
    }


# ---------------------------------------------------------------- the chart
def chart_png(fx):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    rows = fx["monthly"]
    x = [dt.date(int(m[:4]), int(m[5:]), 15) for m, _, _ in rows]
    p = [v for _, v, _ in rows]
    d = [v for _, _, v in rows]
    fig, ax = plt.subplots(figsize=(6.6, 3.4), dpi=150)
    ax.axvspan(dt.date(2024, 11, 4), dt.date(2026, 9, 1), color="#f1ece2", zorder=0)
    ax.plot(x, p, color="#1f4e79", lw=2.0, marker="o", ms=3, label="Fee-liable pickups (taxis leaving the airport)")
    ax.plot(x, d, color="#9c6b30", lw=1.6, marker="s", ms=2.6, label="Drop-offs at the airport")
    ax.axvline(dt.date(2024, 11, 4), color="#555555", lw=0.8, ls="--")
    ax.annotate("4 Nov 2024: taxis to the P2 temporary rank;\nAirport Line opens", xy=(dt.date(2024, 11, 4), max(p) * 0.99),
                xytext=(dt.date(2025, 1, 20), max(p) * 1.005), fontsize=7.2, color="#333333",
                arrowprops=dict(arrowstyle="-", color="#777777", lw=0.6))
    ax.set_ylim(0, max(p) * 1.12)
    ax.set_ylabel("Trips a month", fontsize=8)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: "{:,.0f}".format(v)))
    ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=(1, 4, 7, 10)))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.tick_params(labelsize=7)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.legend(fontsize=7, frameon=False, loc="lower right")
    ax.set_title("Pickups and drop-offs both fell when the rank moved and the Airport Line opened", fontsize=8.6,
                 loc="left")
    fig.text(0.01, 0.01, "Shaded: temporary rank on P2. Source: Vehicle-for-Hire Office trip records (2023 daily "
             "archive, 2024 and 2025 annual files, 2026 monthly files).", fontsize=6.2, color="#555555")
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


# ---------------------------------------------------------------- the memo
def write_memo(path, fx, fig):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Inches, Pt, RGBColor
    c, k = fig["call"], fig["components"]
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = Inches(0.95)
    sec.top_margin = Inches(0.8)
    sec.bottom_margin = Inches(0.8)
    hdr = sec.header.paragraphs[0]
    hdr.text = "Velmont Airport Authority  |  Ground Transportation Finance"
    hdr.runs[0].font.size = Pt(8)
    hdr.runs[0].font.color.rgb = RGBColor(0x5B, 0x60, 0x67)
    foot = sec.footer.paragraphs[0]
    foot.text = "For the Finance and Audit Committee, 4 November 2026, and the Board, December 2026\tPage "
    foot.runs[0].font.size = Pt(8)
    foot.runs[0].font.color.rgb = RGBColor(0x5B, 0x60, 0x67)
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    r = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), "16")
    rpr.append(sz)
    r.append(rpr)
    t = OxmlElement("w:t")
    t.text = "1"
    r.append(t)
    fld.append(r)
    foot._p.append(fld)

    def para(text, bold=False, size=None, space=6, italic=False):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.bold = bold
        r.italic = italic
        if size:
            r.font.size = Pt(size)
        p.paragraph_format.space_after = Pt(space)
        return p

    def heading(text, new_page=False):
        p = doc.add_paragraph()
        p.paragraph_format.page_break_before = new_page
        r = p.add_run(text)
        r.bold = True
        r.font.size = Pt(11)
        r.font.color.rgb = RGBColor(0x17, 0x36, 0x5D)
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True

    t = para("MEMORANDUM", bold=True, size=13, space=2)
    t.runs[0].font.color.rgb = RGBColor(0x17, 0x36, 0x5D)
    for a, b in (("To", "Board of Directors, through the Finance and Audit Committee"),
                 ("From", "%s, %s" % (W.PEOPLE["finance"], "Manager, Ground Transportation Finance")),
                 ("Date", "16 October 2026"),
                 ("Subject", "2027 taxi pickup fee under By-law GT-3, section 4")):
        p = doc.add_paragraph()
        r = p.add_run(a + ":\t")
        r.bold = True
        p.add_run(b)
        p.paragraph_format.space_after = Pt(1)
    para("", space=2)
    para("Set the 2027 taxi pickup fee at $%s, down from $%s in 2026." % (c["fee_2027"], c["fee_2026"]), bold=True,
         size=12, space=8)
    para("The 2027 Ground Transportation Program budget assigns $%s to the taxi pickup fee. Under FP-07 the budgeted "
         "pickups are 2025's %s fee-liable pickups restated to the forecourt rank that returns on 1 January 2027, "
         "%s pickups. At $%s a pickup they recover the amount with about $%s to spare; at $6.25 they would fall about "
         "$%s short." % (k["amount_2027"], k["recorded_2025"], k["restated_2025"], c["fee_2027"],
                         fig["surplus_at_fee"], fig["shortfall_one_step_below"]))

    heading("What the restatement removes")
    para("Since 4 November 2024 taxis have loaded at the temporary rank on the P2 Level 2 road. The Airport Line opened "
         "the same morning, so the fall in pickups that November is two changes at once: the rank, which goes in "
         "2027, and the line, which stays. FP-07 restates only the rank (a taxi loading arrangement), so its effect "
         "has to be read apart from the line's.")
    para("Drop-offs at the departures roadway never used the rank, but the line took riders in both directions on "
         "trips to and from the zones its stations serve (Downtown Central, Midtown, University and Commerce Park). "
         "Those zones send the airport most of its drop-offs but take under half its pickups, so the line cut "
         "drop-offs almost as much as pickups overall. Within the station zones the ratio of pickups to drop-offs was "
         "%s per cent lower in 2025 than in the twelve months before the move, and within the other zones %s per cent "
         "lower: the rank cost %s per cent of the pickups 2025 would have had at the forecourt." % (
             fig["strata_pct"]["station_zones"], fig["strata_pct"]["other_zones"], k["share_cost_pct"]))
    para("Two quicker readings give other fees. Taking the whole %s per cent fall in pickups as the rank's effect "
         "restates the line away as well and gives $%s; setting all pickups against all drop-offs credits the rank "
         "with only %s per cent, because the drop-offs carry more of the line's zones, and gives $%s." % (
             fig["rivals"]["own_fall"]["share_pct"], fig["rivals"]["own_fall"]["fee"],
             fig["rivals"]["all_dropoffs"]["share_pct"], fig["rivals"]["all_dropoffs"]["fee"]))

    heading("How firm the fee is")
    para("$%s is the lowest 25-cent step that recovers the amount (By-law GT-3, s.4) for any rank effect from %s to %s "
         "per cent of the restated pickups; just below that range the fee would be $6.75, just above it $6.25." % (
             c["fee_2027"], fig["flip_pct"]["lo"], fig["flip_pct"]["hi"]), space=6)

    heading("Monthly trips", new_page=True)
    doc.add_picture(io.BytesIO(chart_png(fx)), width=Inches(6.4))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER

    heading("Notes")
    para("1. Base-year pickups are read from the Vehicle-for-Hire Office's final 2025 annual file (FP-07 4.4); no "
         "traffic growth is assumed (FP-07 4.2). Restated pickups are shown to the nearest thousand; the fee is "
         "worked on the unrounded figure.", size=9)
    para("2. The brokerage ledger (velmont_taxi_fee_ledger_2025_2026.csv) bills each pickup to the brokerage the taxi "
         "belonged to when the trip began (By-law GT-3, s.3(2)): 2025 from the annual file with the Office's "
         "affiliation register, 2026 from the monthly files with re-sent and voided records taken out.", size=9)
    doc.save(path)


def write_ledger(path, fx):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["month", "brokerage_id", "brokerage_name", "fee_liable_pickups", "fees_owed"])
        for r in fx["ledger"].itertuples():
            w.writerow([r.month, int(r.brokerage), W.BROKERAGES[int(r.brokerage)], int(r.pickups), "%.2f" % r.owed])


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    fx = compute(target)
    fig = figures(fx)
    json.dump(fig, open(fig_path, "w", encoding="utf-8"), indent=1)
    write_memo(os.path.join(gdir, W.GOLDEN["memo"]), fx, fig)
    write_ledger(os.path.join(gdir, W.GOLDEN["ledger"]), fx)
    return fx, fig
