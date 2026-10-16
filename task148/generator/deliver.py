"""The goldens, computed from the shipped pack: sba_allowance_fy2026.xlsx (the allowance and its split, the Section 1112
table, the net charge-off table) and allowance_note_fy2026.docx (the board's one-page note with its chart), and
generator/figures.json, every figure the write-up states."""
from __future__ import annotations

import io
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AS           # noqa: E402
import calc as C            # noqa: E402
import common as K          # noqa: E402
import postprocess as PP    # noqa: E402

GOLD_BOOK = "sba_allowance_fy2026.xlsx"
GOLD_NOTE = "allowance_note_fy2026.docx"
FYS = (2019, 2020, 2021)


def compute(target, Wd=None):
    P = C.panel_from_pack(target)
    B = C.book_from_pack(P)
    rk = P.risk
    co = P.co_share
    hs = C.rate_table(rk[rk.k == 1], "dflt")
    hp = C.rate_table(rk, "po")
    hd = C.rate_table(rk, "dflt")
    g = C.union(B, hs, hp, co)
    pool = B.pool
    c = {"P": P, "B": B, "g": g, "co": co, "hs": hs, "hp": hp, "hd": hd}
    c["allowance"] = float(g.sum())
    c["split"] = {f: float(g[pool.fy == f].sum()) for f in FYS}
    c["ugp"] = {f: float((pool.bal * pool.ug)[pool.fy == f].sum()) for f in FYS}
    c["loans"] = {f: int((pool.fy == f).sum()) for f in FYS}
    c["in_default"] = {f: int(((pool.fy == f) & ~pool.perf).sum()) for f in FYS}
    c["textbook"] = float(C.loan_level(B, hd, hp, co).sum())
    mem = B.members
    gk = mem.groupby("gid").size()
    pool_k = pool.gid.map(gk).fillna(1).astype(int)
    c["pool_in_groups"] = int((pool_k > 1).sum())
    c["groups"] = int(pool[pool_k > 1].gid.nunique())
    pg = set(pool[pool_k > 1].gid)
    out = mem[mem.gid.isin(pg) & ~mem.fy.between(*K.POOL_FY)]
    c["outside"] = int(len(out))
    c["outside_fy2026"] = int((out.fy == 2026).sum())
    c["ug_share_groups"] = float((pool.bal * pool.ug)[pool_k > 1].sum() / (pool.bal * pool.ug).sum())
    c["ask_a"] = C.ask_a_from_pack(target)
    c["ask_b"] = C.ask_b_from_pack(target)
    if Wd is not None:
        qa, nb = AS.ask_goldens(Wd.W, Wd.A, Wd.B)
        for k, v in qa.items():
            assert abs(v - c["ask_a"][k]) < 0.01, ("ask A from the pack against the world", k, v, c["ask_a"][k])
        for k, v in nb.items():
            assert abs(v - c["ask_b"][k]) < 0.01, ("ask B from the pack against the world", k, v, c["ask_b"][k])
    return c


def rounded(c):
    r = {"allowance": K.round_to(c["allowance"], 1e6)}
    r["split"] = {f: K.round_to(c["split"][f], 5e5) for f in FYS}
    r["ugp"] = {f: K.round_to(c["ugp"][f], 1000) for f in FYS}
    r["ask_a"] = {k: K.round_to(v, 1000) for k, v in c["ask_a"].items()}
    r["ask_b"] = {k: K.round_to(v, 1000) for k, v in c["ask_b"].items()}
    return r


def figures(c):
    r = rounded(c)
    f = {"labels": {"program": "SBA 7(a)", "statute": "Section 1112", "default_days_past_due": 90},
         "call": {"allowance_usd": r["allowance"], "allowance_usd_million": r["allowance"] / 1e6,
                  "allowance_unrounded_usd": round(c["allowance"], 2),
                  "allowance_unrounded_usd_million": round(c["allowance"] / 1e6, 2)},
         "critical_components": {"split_usd": {"FY%d" % k: v for k, v in r["split"].items()},
                                 "split_usd_million": {"FY%d" % k: v / 1e6 for k, v in r["split"].items()},
                                 "split_unrounded_usd": {"FY%d" % k: round(v, 2) for k, v in c["split"].items()}},
         "steps": {"pool_loans_on_books": sum(c["loans"].values()),
                   "pool_loans_by_fy": {"FY%d" % k: v for k, v in c["loans"].items()},
                   "pool_loans_in_default": sum(c["in_default"].values()),
                   "charge_off_share_pct": round(100 * c["co"], 1),
                   "pool_loans_in_groups": c["pool_in_groups"], "pool_groups": c["groups"],
                   "group_loans_outside_pool": c["outside"], "group_loans_outside_pool_fy2026": c["outside_fy2026"],
                   "pool_ug_share_in_groups_pct": round(100 * c["ug_share_groups"], 1),
                   "default_path_usd_million": round(c["textbook"] / 1e6, 1)},
         "deliverables": {"unguaranteed_principal_usd": {"FY%d" % k: v for k, v in r["ugp"].items()},
                          "unguaranteed_principal_usd_million": {"FY%d" % k: round(v / 1e6, 1) for k, v in r["ugp"].items()},
                          "unguaranteed_principal_total_usd": K.round_to(sum(c["ugp"].values()), 1000),
                          "section_1112_payments_usd": r["ask_a"],
                          "net_charge_offs_usd": {"FY%d / FY%d approvals" % k: v for k, v in r["ask_b"].items()},
                          "net_recoveries_usd": {"FY%d / FY%d approvals" % k: -v for k, v in r["ask_b"].items() if v < 0}}}
    return f


def m1(v):
    return "{:,.0f}".format(v)


def write_book(path, c):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    r = rounded(c)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Allowance"
    bold = Font(name="Calibri", bold=True, size=11)
    head = PatternFill("solid", fgColor="DCE6F0")
    thin = Side(style="thin", color="8EA0B4")
    ws["A1"] = "Fenmore Savings Bank, SBA Lending"
    ws["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws["A2"] = "Allowance for credit losses, unguaranteed portions of 7(a) loans approved in fiscal years 2019 to 2021, at 30 September 2026"
    ws["A2"].font = Font(name="Calibri", size=11)
    hdr = ["Approval fiscal year", "Loans on the books", "Of which in default", "Unguaranteed principal ($)",
           "Allowance ($ million)"]
    ws.append([])
    ws.append(hdr)
    for cell in ws[4]:
        cell.font = bold
        cell.fill = head
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        cell.border = Border(bottom=thin)
    for f in FYS:
        ws.append(["FY%d" % f, c["loans"][f], c["in_default"][f], r["ugp"][f], r["split"][f] / 1e6])
    ws.append(["Total", sum(c["loans"].values()), sum(c["in_default"].values()), sum(r["ugp"].values()),
               r["allowance"] / 1e6])
    for cell in ws[8]:
        cell.font = bold
        cell.border = Border(top=thin)
    for row in ws.iter_rows(min_row=5, max_row=8):
        row[1].number_format = "#,##0"
        row[2].number_format = "#,##0"
        row[3].number_format = "#,##0"
        row[4].number_format = "0.0"
    ws["E8"].number_format = "0"
    notes = [
        "The allowance is rounded to the nearest $1 million and each fiscal year's part to the nearest $0.5 million; "
        "unguaranteed principal to the nearest $1,000.",
        "Basis: each loan is priced at the default of its guarantor group. Under the loan authorization's cross-default "
        "clause (Part B, 4.2) every loan the same guarantors stand behind defaults when any of them does, so a loan's "
        "monthly default probability is that of the first failure among the group's performing loans, each at its own "
        "months on book, with its own payoff and maturity, including the group's loans approved outside fiscal 2019 to "
        "2021.",
        "Failure rates by months on book are measured on loans standing alone (the only performing loan of their "
        "guarantors that month), October 2009 to September 2026; payoff rates on every loan. Exposure is each loan's "
        "unguaranteed principal scheduled at the month-end of default at its 30 September 2026 note rate (CP-SBA-07, "
        "3.1). Charge-off share of resolved defaults %.1f per cent." % (100 * c["co"]),
    ]
    ws.append([])
    for n_ in notes:
        ws.append([n_])
        ws.cell(row=ws.max_row, column=1).alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=ws.max_row, start_column=1, end_row=ws.max_row, end_column=5)
        ws.row_dimensions[ws.max_row].height = 48
    for col, w in zip("ABCDE", (20, 16, 16, 24, 20)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"
    ws.print_title_rows = "1:4"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws2 = wb.create_sheet("Section 1112")
    ws2["A1"] = "Section 1112 payments SBA made on the relief-era loans, by fiscal quarter of the instalment's due date"
    ws2["A1"].font = Font(name="Calibri", bold=True, size=11)
    ws2.append([])
    ws2.append(["Fiscal quarter", "Instalments due", "Payments ($)"])
    for cell in ws2[3]:
        cell.font = bold
        cell.fill = head
        cell.border = Border(bottom=thin)
    labels = {"Q1": "October to December", "Q2": "January to March", "Q3": "April to June", "Q4": "July to September"}
    tot = 0
    for k, v in r["ask_a"].items():
        fy, q = k.split()
        yr = int(fy[2:]) - (1 if q == "Q1" else 0)
        ws2.append([k, "%s %d" % (labels[q], yr), v])
        tot += v
    ws2.append(["Total", "April 2020 to December 2021", tot])
    for cell in ws2[ws2.max_row]:
        cell.font = bold
        cell.border = Border(top=thin)
    for row in ws2.iter_rows(min_row=4, max_row=ws2.max_row):
        row[2].number_format = "#,##0"
    ws2.append([])
    ws2.append(["Each instalment once, at the amount SBA paid on it; to the nearest $1,000."])
    for col, w in zip("ABC", (16, 30, 18)):
        ws2.column_dimensions[col].width = w
    ws2.freeze_panes = "A4"
    ws3 = wb.create_sheet("Net charge-offs")
    ws3["A1"] = "Net charge-offs on the relief-era loans, unguaranteed principal charged off less recoveries the bank kept"
    ws3["A1"].font = Font(name="Calibri", bold=True, size=11)
    ws3.append([])
    ws3.append(["Fiscal year", "FY2019 approvals ($)", "FY2020 approvals ($)", "FY2021 approvals ($)", "Total ($)"])
    for cell in ws3[3]:
        cell.font = bold
        cell.fill = head
        cell.border = Border(bottom=thin)
    for fy in AS.ASK_B_FYS:
        vals = [r["ask_b"][(fy, v)] for v in FYS]
        ws3.append(["FY%d" % fy] + vals + [sum(vals)])
    for row in ws3.iter_rows(min_row=4, max_row=ws3.max_row):
        for cell in row[1:]:
            cell.number_format = "#,##0;(#,##0)"
    ws3.append([])
    ws3.append(["Recoveries the bank kept: its share of each liquidation receipt and the lender's shares of Treasury "
                "offsets SBA remitted; to the nearest $1,000, recoveries above charge-offs in brackets."])
    for col, w in zip("ABCDE", (14, 22, 22, 22, 16)):
        ws3.column_dimensions[col].width = w
    ws3.freeze_panes = "B4"
    wb.save(path)
    PP.normalize_ooxml(path, K.PEOPLE["controller"], K.PEOPLE["controller"], "2026-10-06T13:22:00Z",
                       "2026-10-07T13:48:00Z", excel=True, company=K.BANK)


def chart_png(c):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    r = rounded(c)
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9})
    fig, ax = plt.subplots(1, 2, figsize=(7.2, 2.9), dpi=150)
    xs = ["FY2019", "FY2020", "FY2021"]
    ug = [r["ugp"][f] / 1e6 for f in FYS]
    al = [r["split"][f] / 1e6 for f in FYS]
    b1 = ax[0].bar(xs, ug, color="#7f9bb8", width=0.6)
    b2 = ax[1].bar(xs, al, color="#163b5c", width=0.6)
    for b, v in zip(b1, ug):
        ax[0].text(b.get_x() + b.get_width() / 2, v + 1.2, "%.1f" % v, ha="center", va="bottom", fontsize=8.5)
    for b, v in zip(b2, al):
        ax[1].text(b.get_x() + b.get_width() / 2, v + 0.08, "%.1f" % v, ha="center", va="bottom", fontsize=8.5)
    ax[0].set_title("Unguaranteed principal, $ million", fontsize=9.5, loc="left")
    ax[1].set_title("Allowance, $ million", fontsize=9.5, loc="left")
    ax[0].set_ylim(0, max(ug) * 1.22)
    ax[1].set_ylim(0, max(al) * 1.25)
    for a in ax:
        a.spines["top"].set_visible(False)
        a.spines["right"].set_visible(False)
        a.set_xlabel("Approval fiscal year", fontsize=8.5)
        a.tick_params(labelsize=8.5)
    fig.suptitle("Relief-era 7(a) loans on the books at 30 September 2026", fontsize=10, x=0.02, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def _page_field(par):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    run = par.add_run()
    for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        run._r.append(el)


def write_note(path, c):
    import docx
    from docx.shared import Cm, Pt, RGBColor
    r = rounded(c)
    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    sec = doc.sections[0]
    sec.top_margin = sec.bottom_margin = Cm(1.8)
    sec.left_margin = sec.right_margin = Cm(2.2)
    fp = sec.footer.paragraphs[0]
    fp.text = "Fenmore Savings Bank, Finance. Board of Directors, October 2026. Page "
    _page_field(fp)
    for run in fp.runs:
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
    p = doc.add_paragraph()
    run = p.add_run("FENMORE SAVINGS BANK")
    run.bold = True
    run.font.size = Pt(9.5)
    p = doc.add_paragraph()
    run = p.add_run("The relief-era SBA loans need a $%d million allowance at 30 September 2026" % (r["allowance"] / 1e6))
    run.bold = True
    run.font.size = Pt(13.5)
    q = doc.add_paragraph()
    q.add_run("From: ").bold = True
    q.add_run("Erin Spence, Controller. For the Board's October meeting (CP-SBA-07, 6.1).")
    p = doc.add_paragraph()
    run = p.add_run("We will book an allowance of $%d million on the unguaranteed portions of the 7(a) loans approved in "
                    "fiscal years 2019 to 2021." % (r["allowance"] / 1e6))
    run.bold = True
    run.font.size = Pt(11.5)
    doc.add_paragraph(
        "It is $%.1f million on the fiscal 2019 approvals, $%.1f million on fiscal 2020 and $%.1f million on fiscal "
        "2021, against unguaranteed principal of $%.1f million on %s loans still on the books, %d of them in default."
        % (r["split"][2019] / 1e6, r["split"][2020] / 1e6, r["split"][2021] / 1e6, sum(r["ugp"].values()) / 1e6,
           m1(sum(c["loans"].values())), sum(c["in_default"].values())))
    doc.add_picture(io.BytesIO(chart_png(c)), width=Cm(16.4))
    q = doc.add_paragraph()
    run = q.add_run("Source: servicing history and guarantee register at 30 September 2026; allowance under CP-SBA-07. "
                    "Unguaranteed principal includes the %d loans in default not yet charged off." % sum(c["in_default"].values()))
    run.italic = True
    run.font.size = Pt(8.5)
    doc.add_paragraph(
        "The figure prices each loan with the loans its guarantors stand behind. %s of these loans belong to %s "
        "operators who guarantee other businesses financed by the bank, and the loan authorization cross-defaults "
        "every such loan: when one of an operator's businesses fails, we accelerate all of them. Those operators "
        "added %s units in fiscal 2026 alone, outside this pool. Businesses fail most in their second to fourth "
        "years, so the pool's risk now sits largely in units that are only months old, and it reaches these loans "
        "through the cross-default." % (m1(c["pool_in_groups"]), m1(c["groups"]), m1(c["outside_fy2026"])))
    doc.add_paragraph(
        "Each loan is carried at the probability that the first failure among its group's performing loans, each at "
        "its own age, comes before the loan pays off or matures, on failure rates measured on businesses standing "
        "alone since October 2009, times the share of defaults the bank has charged off (%.1f per cent), on the "
        "unguaranteed principal scheduled for the month of default at 30 September 2026 rates. Loans already in default "
        "are carried at that share. Recoveries are not counted (CP-SBA-07, 2.1)." % (100 * c["co"]))
    q = doc.add_paragraph()
    run = q.add_run("Workbook: sba_allowance_fy2026.xlsx, with the Section 1112 payments on these loans by quarter and "
                    "their net charge-offs by fiscal year.")
    run.italic = True
    run.font.size = Pt(9)
    doc.core_properties.author = K.PEOPLE["controller"]
    doc.core_properties.title = "Allowance for credit losses, relief-era SBA loans"
    doc.save(path)
    PP.normalize_docx(path, K.PEOPLE["controller"], K.PEOPLE["controller"], "2026-10-06T19:41:00Z",
                      "2026-10-07T14:05:00Z", revision=5, total_time=94, seed="task148/note",
                      title="Allowance for credit losses, relief-era SBA loans", company=K.BANK)


def main(target, golden, figures_path, Wd=None):
    os.makedirs(golden, exist_ok=True)
    c = compute(target, Wd)
    figs = figures(c)
    write_book(os.path.join(golden, GOLD_BOOK), c)
    write_note(os.path.join(golden, GOLD_NOTE), c)
    with open(figures_path, "w") as fh:
        json.dump(figs, fh, indent=2, sort_keys=False, default=str)
        fh.write("\n")
    return c
