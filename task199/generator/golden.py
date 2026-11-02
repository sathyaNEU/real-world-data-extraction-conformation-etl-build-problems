"""Golden deliverables and figures.json for task199 (architecture 2), computed from target/ through analysis.py."""
import datetime as dt
import io
import json
import os

import analysis as A
import zipfix

ACCENT = "#2a78d6"
NEXT = "#9cbde8"
MUTED = "#b9b7b0"
INK = "#0b0b0b"
INK2 = "#52514e"


def money_m(x):
    return int(round(x / 1e6))


def compute(target):
    F = A.figures(target)
    res, order = F["res"], F["order"]
    first, second = order[0], order[1]
    pairs = F["aux"]["pairs"]
    inn = A.load(target)["inn"]
    out = A.load(target)["out"]
    in_by_ref = {m["ref"]: m for m in inn}
    out_by_ref = {m["ref"]: m for m in out}
    stmts = A.load(target)["stmts"]
    conv = A.read_conversion(target)
    owner = A.acct_owner(stmts, conv)
    tum_pairs = [(in_by_ref[i], out_by_ref[o]) for i, o in pairs.items() if owner.get(in_by_ref[i]["bene_acct"]) ==
                 first[0]]
    reg = A.read_register(target)
    fig = {
        "call_cif": first[0], "call_name": first[1]["name"], "call_tp_m": money_m(first[1]["tp"]),
        "call_expected_m": money_m(first[1]["expected"]), "call_ratio": "%.2f" % first[1]["ratio"],
        "runner_cif": second[0], "runner_name": second[1]["name"], "runner_ratio": "%.2f" % second[1]["ratio"],
        "call_uturn_n": len(tum_pairs), "call_uturn_m": money_m(first[1]["parts"].get("uturn", 0.0)),
        "runner_elsewhere_m": money_m(second[1]["parts"].get("own_external", 0.0)),
        "uturn_lag_min": min(A.business_days_between(o["value"], i["value"], A.kenya_holidays(A.load(target)["rates"]))
                             for i, o in tum_pairs),
        "uturn_lag_max": max(A.business_days_between(o["value"], i["value"], A.kenya_holidays(A.load(target)["rates"]))
                             for i, o in tum_pairs),
        "uturn_gap_min": "%.2f" % min(o["amount"] - i["amount"] for i, o in tum_pairs),
        "uturn_gap_max": "%.2f" % max(o["amount"] - i["amount"] for i, o in tum_pairs),
        "pair_window_bd": 10, "pair_tol_usd": 200,
        "threshold_usd": 10000,
        "customers": [],
    }
    for cif in sorted(reg):
        r = res[cif]
        cash = F["cash"].get(cif, (0, 0.0))
        sal = F["sal"].get(cif, (0, 0.0))
        vat = F["vat"].get(cif, 0.0)
        fig["customers"].append(dict(cif=cif, name=r["name"], tp_m=money_m(r["tp"]), expected_m=money_m(r["expected"]),
                                     ratio="%.2f" % r["ratio"], cash_n=cash[0], cash_kes=int(round(cash[1])),
                                     sal_n=sal[0], sal_kes=int(round(sal[1])), vat_kes=int(round(vat)),
                                     tp_exact=round(r["tp"], 2), ratio_exact=round(r["ratio"], 6),
                                     dev_exact=round(r["dev"], 6)))
    return fig, F


def _chart(fig, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
    rows = sorted(fig["customers"], key=lambda c: c["ratio_exact"])
    names = [c["name"].replace(" Limited", "").replace(" Ltd", "") for c in rows]
    vals = [c["ratio_exact"] for c in rows]
    colours = [ACCENT if c["cif"] == fig["call_cif"] else (NEXT if c["cif"] == fig["runner_cif"] else MUTED)
               for c in rows]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "svg.hashsalt": "tawi"})
    f, ax = plt.subplots(figsize=(7.2, 4.4), dpi=150)
    f.patch.set_facecolor("#ffffff")
    y = list(range(len(rows)))
    for yi, v, col in zip(y, vals, colours):
        left, width = (v, 1.0 - v) if v < 1 else (1.0, v - 1.0)
        ax.barh(yi, width, left=left, height=0.62, color=col, edgecolor="#ffffff", linewidth=0)
        ha = "right" if v < 1 else "left"
        ax.text(v * (0.96 if v < 1 else 1.04), yi, "%.2f" % v, va="center", ha=ha, fontsize=7.5,
                color=INK if col == ACCENT else INK2, fontweight="bold" if col == ACCENT else "normal")
    ax.axvline(1.0, color=INK2, linewidth=0.9)
    ax.text(1.0, len(rows) - 0.25, "  expected annual turnover (1.00)", fontsize=7.2, color=INK2, va="bottom")
    ax.set_xscale("log")
    ticks = [0.25, 0.5, 1.0, 2.0, 4.0]
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_major_formatter(FixedFormatter(["0.25", "0.50", "1.00", "2.00", "4.00"]))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.set_xlim(0.17, 4.6)
    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=7.8, color=INK)
    ax.set_ylim(-0.7, len(rows) - 0.1)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#c9c7bf")
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", colors=INK2, labelsize=7.5)
    ax.grid(axis="x", color="#ecebe6", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.set_xlabel("Third-party receipts as a multiple of expected annual turnover (log scale)", fontsize=7.6,
                  color=INK2)
    f.text(0.012, 0.965, "%s: third-party receipts %s of declared turnover, furthest from profile"
           % (fig["call_name"].replace(" Ltd", ""), fig["call_ratio"]), fontsize=9.6, fontweight="bold", color=INK)
    f.text(0.012, 0.925, "EDD register, year to 30 September 2026. Next in line: %s at %s."
           % (fig["runner_name"].replace(" Ltd", ""), fig["runner_ratio"]), fontsize=7.8, color=INK2)
    f.text(0.012, 0.012, "Source: core banking statements (legacy and T24), SWIFT MT103 archive, EDD profiles; "
           "receipts per FCC-07 section 3.", fontsize=6.6, color=INK2)
    f.subplots_adjust(left=0.30, right=0.97, top=0.86, bottom=0.14)
    f.savefig(path, dpi=150, metadata={"Software": None})
    plt.close(f)


def write_memo(fig, golden_dir, chart_png):
    from docx import Document
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.shared import Pt, Mm, RGBColor
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(20)
    sec.top_margin, sec.bottom_margin = Mm(16), Mm(16)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)
    hdr = sec.header.paragraphs[0]
    hdr.text = "Tawi Bank Limited | Financial Crime Compliance | Confidential: not for disclosure to the customer"
    hdr.runs[0].font.size = Pt(7.5)
    hdr.runs[0].font.color.rgb = RGBColor(0x52, 0x51, 0x4E)
    ftr = sec.footer.paragraphs[0]
    ftr.text = "FCC-07/2026/REF-01  |  EDD annual review, year to 30 September 2026"
    ftr.runs[0].font.size = Pt(7.5)

    def para(text, bold=False, size=None, space=4, colour=None):
        p = doc.add_paragraph()
        r = p.add_run(text)
        r.bold = bold
        if size:
            r.font.size = Pt(size)
        if colour:
            r.font.color.rgb = colour
        p.paragraph_format.space_after = Pt(space)
        return p

    para("Referral to the Financial Investigations Unit", bold=True, size=14, space=2)
    t = doc.add_table(rows=5, cols=2)
    meta = [("To", "Head, Financial Investigations Unit"),
            ("From", "EDD analyst, Financial Crime Compliance"),
            ("Approved", "Head of Financial Crime Compliance (MLRO)"),
            ("Date", "21 October 2026"),
            ("Reference", "FCC-07/2026/REF-01, EDD annual review of the year to 30 September 2026")]
    for i, (k, v) in enumerate(meta):
        t.cell(i, 0).text = k
        t.cell(i, 1).text = v
        t.cell(i, 0).paragraphs[0].runs[0].bold = True
        for c in (0, 1):
            t.cell(i, c).paragraphs[0].runs[0].font.size = Pt(9)
    t.columns[0].width = Mm(28)
    para("")
    para("%s (customer %s) is referred for a full investigation this cycle." % (fig["call_name"], fig["call_cif"]),
         bold=True, size=11, space=6)
    para("Its third-party receipts for the year to 30 September 2026 were KES %s million against the expected annual "
         "turnover of KES %s million recorded in its profile, a ratio of %s. No other customer on the register is as "
         "far from its profile under FCC-07 4.1. %s is next in line at a ratio of %s and is held for the next cycle."
         % ("{:,}".format(fig["call_tp_m"]), "{:,}".format(fig["call_expected_m"]), fig["call_ratio"],
            fig["runner_name"], fig["runner_ratio"]), space=6)
    para("Why the account is not what it looks like", bold=True, size=10.5, space=3)
    para("On its face the account is busy and close to profile. Most of that activity is the customer's own money. "
         "%d of its dollar credits, KES %s million in all, came from four companies in Dubai, Mauritius and Hong Kong "
         "that are not in its profile, each between %d and %d business days after a dollar payment of its own to one "
         "of four other companies in Hong Kong, Cyprus and Mauritius, and each short of that payment by USD %s to "
         "USD %s, the intermediary charges taken on the way out and back. The remitter is never the payee, so nothing "
         "in either message links the two legs; the amounts and dates do. Under FCC-07 3.1 funds that originate from "
         "the customer itself are not third-party receipts however they reach the account, so these credits are "
         "removed, as are its own currency deals between its shilling and dollar accounts."
         % (fig["call_uturn_n"], "{:,}".format(fig["call_uturn_m"]), fig["uturn_lag_min"], fig["uturn_lag_max"],
            fig["uturn_gap_min"], fig["uturn_gap_max"]), space=6)
    para("What is left is a small wholesale business: shilling receipts from Nairobi buyers and dollar receipts "
         "from buyers in Juba, Kampala and Goma. The pattern should be put to the customer through a source-of-funds "
         "request before any report is filed, and the Unit may wish to check the four remitting and four receiving "
         "companies against correspondent information.", space=6)
    para("%s is next because most of its credits with us this year came from its own account at Ufanisi Bank, "
         "which it declared at its last review (KES %s million). Its business has moved to that bank; the profile "
         "should be refreshed rather than investigated." % (fig["runner_name"], "{:,}".format(fig["runner_elsewhere_m"])),
         space=6)
    doc.add_picture(chart_png, width=Mm(165))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    p = para("Note. Receipts are credits by value date within the review year, foreign currency at the CBK mean rate "
             "for the value date (FCC-07 3.2). Large cash withdrawals, salaries and VAT for every register customer are "
             "in the review workbook edd_review_2026.xlsx.", size=8, colour=RGBColor(0x52, 0x51, 0x4E))
    path = os.path.join(golden_dir, "edd_referral_2026.docx")
    doc.core_properties.author = "Financial Crime Compliance"
    doc.core_properties.title = "Referral to the Financial Investigations Unit"
    doc.core_properties.created = dt.datetime(2026, 10, 21, 9, 0)
    doc.core_properties.modified = dt.datetime(2026, 10, 21, 9, 0)
    doc.core_properties.last_modified_by = "Financial Crime Compliance"
    doc.core_properties.revision = 1
    doc.save(path)
    zipfix.normalise(path, creator="Financial Crime Compliance", app="Microsoft Office Word")
    return path


def write_workbook(fig, golden_dir):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    wb = Workbook()
    thin = Side(style="thin", color="BFBFBF")
    head_fill = PatternFill("solid", fgColor="DCE6F2")

    def sheet(ws, title, note, headers, rows, fmts, widths):
        ws["A1"] = title
        ws["A1"].font = Font(bold=True, size=12)
        ws["A2"] = note
        ws["A2"].font = Font(italic=True, size=9, color="52514E")
        ws.append([])
        ws.append(headers)
        for c in ws[4]:
            c.font = Font(bold=True)
            c.fill = head_fill
            c.alignment = Alignment(wrap_text=True, vertical="top")
            c.border = Border(bottom=thin)
        for r in rows:
            ws.append(r)
            for k, f in enumerate(fmts):
                if f:
                    ws.cell(row=ws.max_row, column=k + 1).number_format = f
        for col, w in zip("ABCDEFG", widths):
            ws.column_dimensions[col].width = w
        ws.freeze_panes = "C5"
        ws.print_title_rows = "4:4"

    custs = fig["customers"]
    ws = wb.active
    ws.title = "Large cash withdrawals"
    sheet(ws, "Cash withdrawals reportable to the Financial Reporting Centre, year to 30 September 2026",
          "FCC-07 5.1: a customer's withdrawals on one day counted together, USD 10,000 at the CBK mean rate for the day. "
          "Teller day, cheque encashments included, reversed withdrawals left out.",
          ["Customer number", "Customer", "Reportable withdrawals", "Total withdrawn (KES)"],
          [[c["cif"], c["name"], c["cash_n"], c["cash_kes"]] for c in custs], [None, None, "0", "#,##0"],
          (16, 38, 14, 18))
    ws2 = wb.create_sheet("September salaries")
    sheet(ws2, "Salaries paid for September 2026 through the salary upload service",
          "FCC-07 6.1. Payroll period read from the batch reference (SAL-cccc-YYMM-nnn); weekly casual wages left out; "
          "a person paid in two September batches is counted once.",
          ["Customer number", "Customer", "People paid", "Paid for September (KES)"],
          [[c["cif"], c["name"], c["sal_n"], c["sal_kes"]] for c in custs], [None, None, "0", "#,##0"],
          (16, 38, 12, 22))
    ws3 = wb.create_sheet("VAT by period")
    sheet(ws3, "VAT paid through the KRA payment gateway, tax periods October 2025 to August 2026",
          "FCC-07 6.2. By tax period, whenever paid; gateway submissions that never reached the customer's statement "
          "(slips rejected by KRA) left out.",
          ["Customer number", "Customer", "VAT paid (KES)"],
          [[c["cif"], c["name"], c["vat_kes"]] for c in custs], [None, None, "#,##0"], (16, 38, 18))
    ws4 = wb.create_sheet("Notes")
    notes = ["Prepared for the EDD annual review, year to 30 September 2026 (FCC-07 revision 4).",
             "Population: the twelve customers on the EDD register at 16 October 2026.",
             "Sources: teller cash transactions; bulk salary uploads July to October 2026; KRA gateway payments; core "
             "banking statements (legacy to 31 March 2026, T24 from 1 April 2026); CBK indicative mean rates.",
             "Amounts are whole shillings as booked; no rounding has been applied."]
    for i, n in enumerate(notes, start=1):
        ws4.cell(row=i, column=1, value=n)
    ws4.column_dimensions["A"].width = 110
    wb.properties.creator = "Financial Crime Compliance"
    wb.properties.lastModifiedBy = "Financial Crime Compliance"
    wb.properties.created = dt.datetime(2026, 10, 21, 9, 0)
    wb.properties.modified = dt.datetime(2026, 10, 21, 9, 0)
    path = os.path.join(golden_dir, "edd_review_2026.xlsx")
    wb.save(path)
    zipfix.normalise(path, creator="Financial Crime Compliance", app="Microsoft Excel")
    return path


def build(target, golden_dir, gen_dir):
    os.makedirs(golden_dir, exist_ok=True)
    fig, F = compute(target)
    png = os.path.join(gen_dir, "_chart.png")
    _chart(fig, png)
    write_memo(fig, golden_dir, png)
    write_workbook(fig, golden_dir)
    os.remove(png)
    with open(os.path.join(gen_dir, "figures.json"), "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True)
    return fig
