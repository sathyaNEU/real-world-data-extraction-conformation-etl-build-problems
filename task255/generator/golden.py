"""The golden deliverables: the finance director's retention workbook for the trustees and the chart of the policy's
test at each quoted attachment."""
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                       # noqa: E402
import openpyxl                                       # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402
from openpyxl.utils import get_column_letter          # noqa: E402

import world as W                                     # noqa: E402

WORKBOOK = "retention_2027.xlsx"
CHART = "attachment_test_2027.png"
CLASS_ORDER = ["city", "fire district", "water-sewer district", "port district", "transit authority",
               "park and recreation district", "library district"]
NAVY, TEAL, PALE = "1F3A5F", "2E7D6B", "E8F1EE"


def millions(a):
    return "$%.1f million" % (a / 1e6)


def write_workbook(path, fig):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Retention 2027"
    rec = fig["call"]["attachment"]
    bold = Font(bold=True)
    ws["A1"] = W.POOL
    ws["A1"].font = Font(bold=True, color=NAVY, size=12)
    ws["A2"] = ("Keep the first %s of each 2027 liability occurrence: the lowest quoted attachment the pool expects "
                "its 2027 occurrences to exceed once or less (%.1f)" % ("${:,.0f}".format(rec), fig["counts"][str(rec)]))
    ws["A2"].font = Font(bold=True, size=11)
    ws["A3"] = ("Risk financing policy 4.1 to 5.1; expected occurrences from the actuary's %.1f law enforcement and %.1f "
                "other occurrences above $25,000, each carried by its own ground-up severity at 2027 cost; premiums from "
                "the broker's indications of October 2, 2026." % (W.COUNT_LE, W.COUNT_OT))
    ws["A3"].font = Font(italic=True, color="5D646C", size=9)
    heads = ["Attachment per occurrence", "Expected 2027 occurrences above it", "Within the policy (one or fewer)",
             "Rate per $1,000 of operating expenditures", "Rate per scheduled unit", "2027 premium"]
    ws.append([])
    ws.append(heads)
    for c in ws[5]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=NAVY)
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    ws.row_dimensions[5].height = 44
    for a in W.OPTIONS:
        gl, al = W.QUOTES[a]
        cnt = fig["counts"][str(a)]
        ws.append([a, round(cnt, 1), "Yes" if cnt <= W.BAR else "No", gl, al, fig["premiums"][str(a)]])
        row = ws[ws.max_row]
        row[0].number_format = "$#,##0"
        row[1].number_format = "0.0"
        row[2].alignment = Alignment(horizontal="center")
        row[3].number_format = "$0.0000"
        row[4].number_format = "$#,##0.00"
        row[5].number_format = "$#,##0"
        if a == rec:
            for c in row:
                c.fill = PatternFill("solid", fgColor=PALE)
                c.font = bold
    r0 = ws.max_row + 2
    lines = [
        ("Severity, law enforcement liability (lognormal, from the first dollar at 2027 cost)",
         "log mean %.2f, log standard deviation %.2f; %d occurrences, %d of them stopped at the retention"
         % (fig["curves"]["LE"]["mu"], fig["curves"]["LE"]["sigma"], fig["curves"]["LE"]["n"],
            fig["curves"]["LE"]["capped"])),
        ("Severity, general, auto, public officials' and employment practices liability",
         "log mean %.2f, log standard deviation %.2f; %d occurrences, %d of them stopped at the retention"
         % (fig["curves"]["OT"]["mu"], fig["curves"]["OT"]["sigma"], fig["curves"]["OT"]["n"],
            fig["curves"]["OT"]["capped"])),
        ("Fitted to", "%d occurrences of accident years 2014 to 2021 in the pool's record (%d closed, %d suits still "
         "open with the pool's layer paid)" % (fig["fit"]["n"], fig["fit"]["closed"], fig["fit"]["open"])),
        ("How the record enters the fit", "each occurrence truncated at its member's deductible and, where it reached "
         "the pool's retention, censored there; costs, deductibles and retentions at 2027 cost by the claim cost index; "
         "one curve over every coverage part does not fit the record (likelihood ratio %.0f on two degrees of freedom)"
         % fig["lr"]["pooled"]),
        ("Runner-up", "%s: %.1f expected occurrences above it, more than the policy's one"
         % ("${:,.0f}".format(fig["call"]["runner_up"]), fig["counts"][str(fig["call"]["runner_up"])])),
        ("Rated exposure", "2027 operating expenditures of ${:,.0f} as declared; {:,d} units on the vehicle schedules "
         "at September 30, 2026 (sheet Rated exposure)".format(fig["exposure"]["toe"], fig["exposure"]["units"])),
    ]
    for k, (lab, val) in enumerate(lines):
        ws.cell(row=r0 + k, column=1, value=lab).font = bold
        ws.cell(row=r0 + k, column=2, value=val)
    for i, wd in enumerate((26, 20, 17, 20, 15, 16), 1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    ws.freeze_panes = "A6"
    ws.print_title_rows = "5:5"

    ex = wb.create_sheet("Rated exposure")
    ex["A1"] = "Exposure the 2027 indications are rated on, by member class"
    ex["A1"].font = Font(bold=True, size=11)
    ex["A2"] = ("Operating expenditures: each member's 2027 total as declared for the renewal (once per member). "
                "Vehicles: units on the members' schedules at September 30, 2026, one per vehicle.")
    ex["A2"].font = Font(italic=True, color="5D646C", size=9)
    ex.append([])
    ex.append(["Member class", "Members", "2027 operating expenditures ($000)", "Scheduled vehicles"])
    for c in ex[4]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=NAVY)
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    ex.row_dimensions[4].height = 32
    for k in CLASS_ORDER:
        e = fig["by_class"][k]
        ex.append([k[0].upper() + k[1:], e["members"], e["toe_000"], e["units"]])
        row = ex[ex.max_row]
        row[2].number_format = "#,##0"
        row[3].number_format = "#,##0"
    tot = fig["exposure"]
    ex.append(["All members", tot["members"], tot["toe_000"], tot["units"]])
    for c in ex[ex.max_row]:
        c.font = bold
    ex[ex.max_row][2].number_format = "#,##0"
    ex[ex.max_row][3].number_format = "#,##0"
    for i, wd in enumerate((30, 10, 20, 12), 1):
        ex.column_dimensions[get_column_letter(i)].width = wd
    ex.freeze_panes = "A5"

    nt = wb.create_sheet("Notes")
    notes = [
        "Prepared for the executive director's 2027 budget proposal, from the claims records at September 30, 2026, "
        "the actuary's study of October 9, 2026 and the broker's indications of October 2, 2026.",
        "Cost of an occurrence: from its first dollar, damages and defense together, whoever pays (policy 2.2). "
        "Attachments are from the first dollar, inclusive of the member's deductible (policy 2.3).",
        "The pool's record holds an occurrence only once its member's payments reached the deductible in force on "
        "the date of the occurrence, and holds its cost only up to the pool's retention ($500,000 for 2014 to 2017, "
        "$1,000,000 from 2018); severity is fitted to that record as it came to exist.",
        "Expected occurrences above an attachment: the actuary's %.1f law enforcement occurrences above $25,000 times "
        "that severity's probability of a cost above the attachment given a cost above $25,000, plus the same for "
        "the %.1f other occurrences (policy 4.3, Exhibit 6). Shown to one decimal; compared unrounded."
        % (W.COUNT_LE, W.COUNT_OT),
        "Premiums: the indicated rates applied to the declared 2027 operating expenditures and the scheduled units; "
        "annual, before the Washington surplus lines tax and stamping fee; rounded to the dollar.",
        "Vehicles loaded from the fleet consortium's lists on %s carry the consortium's asset numbers; "
        "a vehicle counts once, under the latest number added for it." % W.CONSORTIUM_LOAD.strftime("%B %-d, %Y"),
        "Rated exposure: each class's operating expenditures are rounded to the thousand on their own and the total "
        "from the unrounded sum, so the classes can differ from the total by a thousand dollars.",
    ]
    nt["A1"] = "Notes"
    nt["A1"].font = Font(bold=True, size=11)
    for k, t in enumerate(notes, 3):
        c = nt.cell(row=k, column=1, value=t)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        nt.row_dimensions[k].height = 44
    nt.column_dimensions["A"].width = 110
    wb.save(path)


def write_chart(path, fig):
    rec = fig["call"]["attachment"]
    xs = list(W.OPTIONS)
    ys = [fig["counts"][str(a)] for a in xs]
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9.5})
    f, ax = plt.subplots(figsize=(8.2, 4.8), dpi=150)
    colors = [("#" + TEAL) if a == rec else "#9AA7B4" for a in xs]
    bars = ax.bar(range(len(xs)), ys, color=colors, width=0.62, zorder=2)
    ax.axhline(W.BAR, color="#B23A30", lw=1.4, ls="--", zorder=3,
               label="Risk financing policy 5.1: one expected occurrence a year")
    for b, y in zip(bars, ys):
        if abs(y + 0.2 - W.BAR) < 0.3:      # a label the policy line would cross sits inside its bar
            ax.text(b.get_x() + b.get_width() / 2, y - 0.08, "%.1f" % y, ha="center", va="top", fontsize=8.6,
                    color="white", fontweight="bold")
        else:
            ax.text(b.get_x() + b.get_width() / 2, y + 0.1, "%.1f" % y, ha="center", va="bottom", fontsize=8.6)
    ax.set_xticks(range(len(xs)))
    ax.set_xticklabels(["$%.1fm" % (a / 1e6) for a in xs])
    ax.set_xlabel("Quoted attachment per occurrence (from the first dollar)")
    ax.set_ylabel("Expected 2027 occurrences costing more than the attachment")
    ax.set_ylim(0, max(ys) * 1.15)
    ax.grid(axis="y", color="#E3E6EA", zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    i = xs.index(rec)
    ax.annotate("Recommended: %s" % millions(rec), xy=(i, ys[i] + 0.55), xytext=(i - 1.7, ys[i] + 2.2),
                arrowprops=dict(arrowstyle="->", color="#" + TEAL), color="#" + TEAL, fontsize=9.5, fontweight="bold")
    ax.set_title("%s is the lowest quoted attachment the pool expects to be exceeded once a year or less"
                 % millions(rec), fontsize=10.5, loc="left")
    ax.legend(loc="upper right", frameon=False, fontsize=8.8)
    f.text(0.01, 0.012, "%s, 2027 budget. Ground-up lognormal severities at 2027 cost for law enforcement liability and "
           "the other parts, fitted to the pool's record of 2014 to 2021;\n%.1f and %.1f expected 2027 occurrences "
           "above $25,000 (actuary's study, October 9, 2026); attachments as quoted October 2, 2026."
           % (W.POOL, W.COUNT_LE, W.COUNT_OT), fontsize=7.2, color="#5D646C")
    f.tight_layout(rect=(0, 0.05, 1, 1))
    f.savefig(path, metadata={"Software": None})
    plt.close(f)
