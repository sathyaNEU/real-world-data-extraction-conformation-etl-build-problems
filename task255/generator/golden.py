"""The golden deliverables, computed from the shipped files under target/ alone (analysis.py): the medicines unit's
workbook statinprogram_2027.xlsx and its one-page note statinprogram_2027.pdf for the practice planning committee."""
import io
import os

import analysis as AN
import io_util as IO

WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
         10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen"}


def figures(target):
    """Every graded figure, in the form the write-up states it."""
    C = AN.main_call(target)
    pay = AN.pilot_payments(target)
    stm = AN.pilot_payments(target, "statements")
    cu = AN.continuing_users(target)
    h, rows = IO.read_csv(os.path.join(target, AN.FILES["pharmacies"]))
    names = {r[0]: r[1] for r in rows}
    practices = []
    for code in sorted(C.n):
        practices.append({"code": code, "name": C.names[code], "n": C.n[code], "k": C.k[code],
                          "share": C.share[code], "pct": int(round(C.share[code])), "joins": code in C.joins})
    pharm = []
    for code in sorted(names):
        held = int(round(pay[code] / pay[code + ":rates"][0]))
        pharm.append({"code": code, "name": names[code], "rate": int(pay[code + ":rates"][0]), "held": held,
                      "due": int(round(pay[code])), "paid": int(round(stm[code])),
                      "balance": int(round(pay[code] - stm[code]))})
    users = [{"code": code, "name": C.names[code], "users": cu[code]} for code in sorted(cu)]
    ddd = AN.main_call(target, "ddd")
    D = AN.load(target)
    singles = sum(1 for pid, pr, st in C.cohort
                  if len([d for d in D["disp"][pid] if d["date"] >= st and (d["date"] - st).days < AN.HORIZON]) == 1)
    return {"practices": practices, "joins": [p for p in practices if p["joins"]], "pharmacies": pharm,
            "users": users, "cohort": sum(C.n.values()),
            "ddd_escape": [C.names[c] for c in C.joins if c not in ddd.joins],
            "ddd_adds": [C.names[c] for c in ddd.joins if c not in C.joins],
            "floor_others": int(min(p["share"] for p in practices if not p["joins"])),
            "singles": singles, "region_share": 100.0 * sum(C.k.values()) / sum(C.n.values())}


def kr(x):
    return "{:,}".format(int(x)).replace(",", ".")


def write_workbook(F, path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = Workbook()
    thin = Side(style="thin", color="9AA5AD")
    bold = Font(bold=True)
    head_fill = PatternFill("solid", fgColor="DCE6EC")
    join_fill = PatternFill("solid", fgColor="F6E3C8")

    def header(ws, row, cols, widths):
        for i, (c, w) in enumerate(zip(cols, widths), start=1):
            cell = ws.cell(row=row, column=i, value=c)
            cell.font = bold
            cell.fill = head_fill
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = Border(bottom=thin)
            ws.column_dimensions[cell.column_letter].width = w
        ws.row_dimensions[row].height = 30

    ws = wb.active
    ws.title = "Programme 2027"
    ws["A1"] = "Statin follow-up programme 2027: twelve-month persistence of new statin users, second half of 2025"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("New statin users 1 July to 31 December 2025 (no statin in the 365 days before), followed 365 days from "
                "the first dispensing; persistent = never more than 30 days in a row without tablets, the tablets timed "
                "at each patient's own daily dose read from their dispensings (programme description 3.1 and 3.2).")
    ws["A3"] = "Joins 2027: persistence under 60 per cent (programme description 2.1)."
    header(ws, 5, ["Provider no.", "Practice", "New statin users", "Persistent 12 months", "Persistent (%)",
                   "Joins 2027"], [12, 32, 14, 14, 13, 11])
    r = 6
    for p in F["practices"]:
        ws.cell(row=r, column=1, value=p["code"])
        ws.cell(row=r, column=2, value=p["name"])
        ws.cell(row=r, column=3, value=p["n"])
        ws.cell(row=r, column=4, value=p["k"])
        c = ws.cell(row=r, column=5, value=p["share"] / 100.0)
        c.number_format = "0%"
        ws.cell(row=r, column=6, value="Yes" if p["joins"] else "No")
        if p["joins"]:
            for col in range(1, 7):
                ws.cell(row=r, column=col).fill = join_fill
        r += 1
    ws.cell(row=r, column=2, value="Region").font = bold
    ws.cell(row=r, column=3, value=sum(p["n"] for p in F["practices"])).font = bold
    ws.cell(row=r, column=4, value=sum(p["k"] for p in F["practices"])).font = bold
    c = ws.cell(row=r, column=5, value=F["region_share"] / 100.0)
    c.number_format = "0%"
    c.font = bold
    ws.freeze_panes = "A6"
    ws.print_title_rows = "5:5"

    ws = wb.create_sheet("Pilot settlement 2026")
    ws["A1"] = "Pharmacy pilot 2026: what each pharmacy is entitled to for its follow-up conversations"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Rate per conversation from each pharmacy's quarterly statements over the conversations they covered "
                "(held in the quarter and not yet cancelled on the statement date); entitled = rate x conversations "
                "held in 2026 and never cancelled (agreement 2.1).")
    header(ws, 4, ["Pharmacy", "Name", "Rate (DKK)", "Conversations held, not cancelled", "Entitled 2026 (DKK)",
                   "Paid on statements (DKK)", "To recover (DKK)"], [10, 24, 11, 15, 15, 15, 13])
    r = 5
    for p in F["pharmacies"]:
        vals = [p["code"], p["name"], p["rate"], p["held"], p["due"], p["paid"], p["paid"] - p["due"]]
        for i, v in enumerate(vals, start=1):
            c = ws.cell(row=r, column=i, value=v)
            if i >= 3:
                c.number_format = "#,##0"
        r += 1
    ws.cell(row=r, column=2, value="Total").font = bold
    for i, key in ((4, "held"), (5, "due"), (6, "paid")):
        c = ws.cell(row=r, column=i, value=sum(p[key] for p in F["pharmacies"]))
        c.font = bold
        c.number_format = "#,##0"
    c = ws.cell(row=r, column=7, value=sum(p["paid"] - p["due"] for p in F["pharmacies"]))
    c.font = bold
    c.number_format = "#,##0"
    ws.freeze_panes = "A5"
    ws.print_title_rows = "4:4"

    ws = wb.create_sheet("Continuing users 2026")
    ws["A1"] = "Continuing statin users in 2026 by practice"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Persons with a statin dispensed in each quarter of 2026, each person once (a personal number replaced "
                "during 2026 joined to the person's earlier pseudonym), at the practice that prescribed their last "
                "dispensing of 2026 (programme description 3.3).")
    header(ws, 4, ["Provider no.", "Practice", "Continuing users 2026"], [12, 32, 14])
    r = 5
    for u in F["users"]:
        ws.cell(row=r, column=1, value=u["code"])
        ws.cell(row=r, column=2, value=u["name"])
        ws.cell(row=r, column=3, value=u["users"])
        r += 1
    ws.cell(row=r, column=2, value="Region").font = bold
    ws.cell(row=r, column=3, value=sum(u["users"] for u in F["users"])).font = bold
    ws.freeze_panes = "A5"
    ws.print_title_rows = "4:4"

    ws = wb.create_sheet("Notes")
    notes = [
        ("Source", "statin_dispensings_202401_202612.csv (register extract, dispensings 2 January 2024 to 31 December "
                   "2026), statin_products.csv, practice_register_2026.xlsx, pilot_conversations_2026.xlsx, "
                   "pilot_statements_2026.pdf."),
        ("New statin user", "First statin dispensing (ATC C10AA) 1 July to 31 December 2025 with none in the 365 days "
                            "before, at the practice that prescribed it (programme description 3.1)."),
        ("Persistent", "Never more than 30 days in a row without tablets in the 365 days from the first dispensing, "
                       "tablets in hand used first (3.2). The register holds no dose: each patient's daily dose is "
                       "the tablets dispensed before the last dispensing over the days from the first to the last."),
        ("One dispensing", "%d new users had a single dispensing in their first year; at any dose it runs out within "
                           "the year, so they count as not persistent." % F["singles"]),
        ("Continuing user", "A person with a statin dispensed in each quarter of 2026, counted once at the practice "
                            "that prescribed their last 2026 dispensing (3.3)."),
        ("Pilot", "Entitled = the pharmacy's rate x conversations held in 2026 and never cancelled (agreement 2.1). "
                  "Statements were drawn on each quarter's last day and paid; conversations cancelled after that "
                  "date stayed on them."),
        ("Rounding", "Shares to the whole per cent from the unrounded share; the 60 per cent line applied to the "
                     "unrounded share; amounts in whole kroner."),
        ("Prepared", "Medicines unit, 12 February 2027."),
    ]
    ws.column_dimensions["A"].width = 18
    ws.column_dimensions["B"].width = 110
    for i, (k, v) in enumerate(notes, start=1):
        ws.cell(row=i, column=1, value=k).font = bold
        c = ws.cell(row=i, column=2, value=v)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for s in wb.worksheets:
        s.sheet_view.zoomScale = 100
    wb.save(path)
    IO.repack_ooxml(path, "Hanne Overgaard", "Hanne Overgaard", "2027-02-08T09:05:00Z", "2027-02-12T13:47:00Z",
                    "Statin programme 2027", "Region Lindholt")


def chart_png(F, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "svg.hashsalt": "task255"})
    ps = sorted(F["practices"], key=lambda p: p["share"])
    fig, ax = plt.subplots(figsize=(6.6, 3.9), dpi=150)
    ys = range(len(ps))
    cols = ["#eb6834" if p["joins"] else "#2a78d6" for p in ps]
    ax.xaxis.grid(True, color="#e4e4e2", lw=0.6)
    ax.set_axisbelow(True)
    ax.barh(list(ys), [p["share"] for p in ps], color=cols, height=0.7)
    ax.set_yticks(list(ys))
    ax.set_yticklabels(["%s  %s" % (p["name"], p["code"]) for p in ps])
    for y, p in zip(ys, ps):
        ax.text(p["share"] + 0.8, y, "%d" % p["pct"], va="center", fontsize=7.8, color="#333333")
    ax.axvline(60, color="#222222", lw=1.0, ls="--")
    ax.text(60.6, len(ps) - 0.1, "programme line 60%", fontsize=7.6, va="bottom")
    ax.set_ylim(-0.7, len(ps) + 0.5)
    ax.set_xlim(0, 90)
    ax.set_xlabel("New statin users of H2 2025 persistent at 12 months (%)")
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color="#eb6834", label="Joins 2027"), Patch(color="#2a78d6", label="Stays out")],
              loc="lower right", frameon=False, fontsize=7.8)
    ax.set_title("%s practices under the 60%% line" % WORDS[len(F["joins"])].capitalize(), loc="left", fontsize=9.5,
                 fontweight="bold")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=150, metadata={"Software": None})
    plt.close(fig)


def write_note(F, path, png):
    from reportlab.lib.units import mm
    joins = F["joins"]
    names = ["%s (%s, %d%%)" % (p["name"], p["code"], p["pct"]) for p in joins]
    due = sum(p["due"] for p in F["pharmacies"])
    paid = sum(p["paid"] for p in F["pharmacies"])
    blocks = [
        ("t", "%s general practices join the statin follow-up programme in 2027" % WORDS[len(joins)].capitalize()),
        ("s", "To: the practice planning committee. From: Hanne Overgaard, medicines unit. 12 February 2027. "
              "Subject: practices joining the 2027 programme (programme description 2.1)."),
        ("h", "Recommendation"),
        ("p", "Yes. %s practices join the programme in 2027: " % WORDS[len(joins)].capitalize() + "; ".join(names) +
              ". Each kept fewer than 60 per cent of its new statin users of the second half of 2025 on treatment for "
              "twelve months; the other %s practices are at %d per cent or more."
              % (WORDS[len(F["practices"]) - len(joins)], F["floor_others"])),
        ("img", (png, 170 * mm, 100 * mm)),
        ("s", "Source: statin dispensings 2024 to 2026 (register extract), statin products, practice register 2026; "
              "new statin users of 1 July to 31 December 2025 by the practice of their first prescription."),
        ("p", "Persistence is counted as the programme description sets it out (3.1 and 3.2): the %s patients who "
              "started a statin between 1 July and 31 December 2025, each followed for 365 days, persistent if never "
              "more than 30 days in a row without tablets. The register holds no dose, so each patient's tablets are "
              "timed at the daily dose shown by the patient's own refills. Timing them at the WHO defined daily dose "
              "instead would let %s off, where many patients take two defined doses in one tablet or two tablets a "
              "day, and take in %s, where many take half of one." % ("{:,}".format(F["cohort"]),
                                                                       ", ".join(F["ddd_escape"][:-1]) + " and " +
                                                                       F["ddd_escape"][-1],
                                                                       " and ".join(F["ddd_adds"]))),
        ("h", "Pilot settlement and 2026 baseline"),
        ("p", "The 2026 pilot pharmacies are entitled to DKK %s for conversations held and never cancelled; the "
              "quarterly statements paid DKK %s, because conversations cancelled after a statement date stayed on "
              "it. The workbook gives the amount per pharmacy and each practice's continuing statin users of 2026, "
              "each person counted once." % (kr(due), kr(paid))),
        ("s", "Note: %s of the new users had one dispensing in their first year; at any dose it runs out within the "
              "year, so they count as not persistent." % "{:,}".format(F["singles"])),
    ]
    IO.write_pdf(path, "Statin follow-up programme 2027", "Hanne Overgaard", "Region Lindholt", blocks,
                 "Region Lindholt, medicines unit", "D:20270212140500+01'00'", "D:20270212140500+01'00'")


def build(target, out_dir, scratch):
    F = figures(target)
    os.makedirs(out_dir, exist_ok=True)
    write_workbook(F, os.path.join(out_dir, "statinprogram_2027.xlsx"))
    png = os.path.join(scratch, "persistence_chart.png")
    chart_png(F, png)
    write_note(F, os.path.join(out_dir, "statinprogram_2027.pdf"), png)
    return F
