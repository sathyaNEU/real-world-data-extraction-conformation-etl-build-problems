"""Golden deliverables for task446: the caseload workbook and the committee chart.

    python3 task446/generator/deliver.py

Every figure comes from solve.golden(), which reads target/ only. The workbook stores each figure at the
precision the prompt asks for; totals are rounded from the unrounded sums. verify() reads both files back.
"""
import datetime as dt
import html
import io
import os
import re
import sys
import zipfile

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve  # noqa: E402

GOLD = os.path.join(HERE, "..", "golden")
XLSX = "watchlist_inflow_2027.xlsx"
CHART = "watchlist_inflow_2027.svg"
BANDS = ["Under £5m", "£5m and under £15m", "£15m and under £40m", "£40m and under £100m", "£100m and over"]
PREPARED = dt.datetime(2026, 10, 27, 16, 18, 0)
AUTHOR = "Jill Berry"
TITLE = "%d of the %d groups we monitor are expected on the watch list by 30 September 2027"


def r1(x):
    return round(x + 1e-12, 1)


def figures(t=solve.TARGET):
    G = solve.golden(t)
    fc, m = G["fc"], G["fc"]["measures"]
    se, f, a1 = m["capture"], m["false_alarm"], fc["a1"]
    p1 = (a1 - f) / (se - f)
    rows = []
    for b, r in zip(BANDS, G["bands"]):
        rows.append(dict(band=b, flagged=r1(r["exp_flagged"]), unflagged=r1(r["exp_unflagged"]),
                         exposure=r1(r["exp_exposure"] / 1e6)))
    total = dict(band="Total", flagged=r1(sum(r["exp_flagged"] for r in G["bands"])),
                 unflagged=r1(sum(r["exp_unflagged"] for r in G["bands"])),
                 exposure=r1(sum(r["exp_exposure"] for r in G["bands"]) / 1e6))
    cohorts = []
    for c in G["tab"][:4]:
        N, F, P = len(c["M"]), len(c["F"]), len(c["R"])
        TP = len(c["R"] & c["F"])
        cohorts.append(dict(date=dt.date.fromisoformat(c["date"]), N=N, F=F, P=P, TP=TP, hit=TP / F, capture=TP / P,
                            false_alarm=(F - TP) / (N - P), share=P / N, flagged_share=F / N))
    F = dict(G=G, call=G["call"], rows=rows, total=total, cohorts=cohorts, measures=m, N1=fc["N1"], F1=fc["F1"],
             a1=a1, p1=p1, p_flag=fc["p_flag"], p_unflag=fc["p_unflag"], expected=fc["total"])
    F["backtest"] = backtest(cohorts)
    return F


def backtest(cohorts):
    """Each closed cohort re-run from the other three, rates pooled and rates averaged. Returns the largest
    absolute miss of the capture and false-alarm model and the count of cohorts the hit and miss model misses
    by more than a third, under each variant; the write-ups quote only what holds under both."""
    out = {}
    for variant in ("pooled", "averaged"):
        err, yld = [], []
        for k, c in enumerate(cohorts):
            rest = [x for j, x in enumerate(cohorts) if j != k]
            if variant == "pooled":
                N, Fl, P, TP = (sum(x[q] for x in rest) for q in ("N", "F", "P", "TP"))
                hit, miss, se, f = TP / Fl, (P - TP) / (N - Fl), TP / P, (Fl - TP) / (N - P)
            else:
                hit = sum(x["TP"] / x["F"] for x in rest) / 3
                miss = sum((x["P"] - x["TP"]) / (x["N"] - x["F"]) for x in rest) / 3
                se = sum(x["capture"] for x in rest) / 3
                f = sum(x["false_alarm"] for x in rest) / 3
            e = c["N"] * (c["F"] / c["N"] - f) / (se - f)
            y = c["F"] * hit + (c["N"] - c["F"]) * miss
            err.append(e / c["P"] - 1)
            yld.append(y / c["P"] - 1)
        out[variant] = dict(err=err, yld=yld, max_err=max(abs(v) for v in err),
                            yld_over_third=sum(1 for v in yld if abs(v) > 1 / 3))
    assert all(v["max_err"] < 0.03 for v in out.values()), out
    assert all(v["yld_over_third"] == 2 for v in out.values()), out
    return out


# ------------------------------------------------------------------ container
def normalise_xlsx(path, modified):
    """Fixed member order and times, Excel's own application name, in-fiction core dates."""
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    created = (modified - dt.timedelta(days=6, hours=2, minutes=41)).strftime("%Y-%m-%dT%H:%M:%SZ").encode()
    stamp = modified.strftime("%Y-%m-%dT%H:%M:%SZ").encode()
    out = []
    for n, data in items:
        if n == "docProps/app.xml":
            data = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Excel</Application>", data)
            data = re.sub(rb"<AppVersion>[^<]*</AppVersion>", b"<AppVersion>16.0300</AppVersion>", data)
        if n == "docProps/core.xml":
            data = re.sub(rb"(<dcterms:created[^>]*>)[^<]*(</dcterms:created>)", rb"\g<1>" + created + rb"\g<2>", data)
            data = re.sub(rb"(<dcterms:modified[^>]*>)[^<]*(</dcterms:modified>)", rb"\g<1>" + stamp + rb"\g<2>", data)
        out.append((n, data))
    first = [x for x in out if x[0] == "[Content_Types].xml"]
    rest = sorted(x for x in out if x[0] != "[Content_Types].xml")
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in first + rest:
            zi = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            z.writestr(zi, data)


# ------------------------------------------------------------------ workbook
GREY = "595F66"
HEAD_FILL = PatternFill("solid", fgColor="E9EBEE")
TOTAL_FILL = PatternFill("solid", fgColor="F4F5F7")
THIN = Side(style="thin", color="A6ABB2")


def workbook(F, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Caseload 2027"
    ws["A1"] = "Halstow Bank plc  |  Credit Risk Monitoring"
    ws["A1"].font = Font(size=9, color=GREY)
    ws["A2"] = "Watch-list caseload for the year to 30 September 2027"
    ws["A2"].font = Font(bold=True, size=14)
    ws["A3"] = "Executive Risk Committee, 4 November 2026, item 3.1"
    ws["A3"].font = Font(size=10, color=GREY)
    ws["A5"] = "Groups expected to reach the watch list by 30 September 2027"
    ws["A5"].font = Font(bold=True, size=11)
    ws["D5"] = F["call"]
    ws["D5"].font = Font(bold=True, size=18)
    ws["D5"].number_format = "0"
    ws["D5"].alignment = Alignment(horizontal="right", vertical="center")
    ws.row_dimensions[5].height = 27
    ws["A6"] = ("From the %d groups in the monitored book at 30 September 2026, %d of them flagged by the "
                "September early-warning run" % (F["N1"], F["F1"]))
    ws["A6"].font = Font(size=9, color=GREY)

    hdr_row = 8
    hdr = ["Caseload band\n(committed exposure at 30 Sep 2026)", "Expected arrivals,\nflagged in September",
           "Expected arrivals,\nnot flagged", "Expected committed exposure\narriving (£m)"]
    for c, h in enumerate(hdr, start=1):
        cell = ws.cell(row=hdr_row, column=c, value=h)
        cell.font = Font(bold=True, size=10)
        cell.fill = HEAD_FILL
        cell.border = Border(bottom=THIN)
        cell.alignment = Alignment(wrap_text=True, vertical="bottom", horizontal="left" if c == 1 else "right")
    ws.row_dimensions[hdr_row].height = 30
    r = hdr_row
    for row in F["rows"] + [F["total"]]:
        r += 1
        ws.cell(row=r, column=1, value=row["band"])
        ws.cell(row=r, column=2, value=row["flagged"]).number_format = "0.0"
        ws.cell(row=r, column=3, value=row["unflagged"]).number_format = "0.0"
        ws.cell(row=r, column=4, value=row["exposure"]).number_format = "#,##0.0"
        if row["band"] == "Total":
            for c in range(1, 5):
                cell = ws.cell(row=r, column=c)
                cell.font = Font(bold=True)
                cell.fill = TOTAL_FILL
                cell.border = Border(top=THIN)
    last = r
    notes = [
        "1  A group's chance of reaching the watch list depends only on its flag at 30 September 2026 (CRM-07 s5.2): "
        "%.1f%% if flagged AMBER or RED, %.1f%% if not. Set from the 2022 to 2025 cohorts; see Cohorts."
        % (F["p_flag"] * 100, F["p_unflag"] * 100),
        "2  Committed exposure per CRM-07 s6.1: HB-PLC 23:05 rerun for 30/09 and the HB-DAC extract, facilities in "
        "force at the end of 30 September 2026, converted at Group Treasury closing rates.",
        "3  Bands of £40m and over are worked by Restructuring, the rest by Business Support (s6.2).",
        "4  Computed unrounded. Caseload to the nearest whole group, band figures to one decimal (s5.3); "
        "totals rounded from the unrounded sums.",
    ]
    for i, n in enumerate(notes):
        cell = ws.cell(row=last + 2 + i, column=1, value=n)
        cell.font = Font(size=9, color=GREY)
    for col, wd in zip("ABCD", [34, 19, 17, 27]):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = ws.cell(row=hdr_row + 1, column=1)
    ws.print_area = "A1:D%d" % (last + 1 + len(notes))
    ws.page_setup.orientation = "portrait"
    ws.page_setup.fitToWidth = 1
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToHeight = 0

    cohort_sheet(wb, F)
    notes_sheet(wb)
    p = wb.properties
    p.creator = AUTHOR
    p.lastModifiedBy = AUTHOR
    p.title = None
    p.created = PREPARED
    p.modified = PREPARED
    wb.save(path)
    normalise_xlsx(path, PREPARED)


def cohort_sheet(wb, F):
    ws = wb.create_sheet("Cohorts")
    ws["A1"] = "Early-warning performance on the closed cohorts (CRM-07 s4.3)"
    ws["A1"].font = Font(bold=True, size=12)
    hdr = ["Cohort", "Groups\nmonitored", "Flagged", "Reached the\nwatch list", "Flagged and\nreached",
           "Hit rate", "Capture rate", "False-alarm\nrate", "Share of book\nreaching"]
    for c, h in enumerate(hdr, start=1):
        cell = ws.cell(row=3, column=c, value=h)
        cell.font = Font(bold=True, size=10)
        cell.fill = HEAD_FILL
        cell.border = Border(bottom=THIN)
        cell.alignment = Alignment(wrap_text=True, vertical="bottom", horizontal="left" if c == 1 else "right")
    ws.row_dimensions[3].height = 30
    r = 3
    for c in F["cohorts"]:
        r += 1
        vals = [c["date"], c["N"], c["F"], c["P"], c["TP"], round(c["hit"], 3), round(c["capture"], 3),
                round(c["false_alarm"], 4), round(c["share"], 3)]
        for j, v in enumerate(vals, start=1):
            ws.cell(row=r, column=j, value=v)
        ws.cell(row=r, column=1).number_format = "d mmm yyyy"
        ws.cell(row=r, column=1).alignment = Alignment(horizontal="left")
    m = F["measures"]
    r += 1
    tot = ["Four cohorts together", m["N"], m["NF"], m["P"], m["TP"], round(m["hit"], 3), round(m["capture"], 3),
           round(m["false_alarm"], 4), round(m["P"] / m["N"], 3)]
    for j, v in enumerate(tot, start=1):
        cell = ws.cell(row=r, column=j, value=v)
        cell.font = Font(bold=True)
        cell.fill = TOTAL_FILL
        cell.border = Border(top=THIN)
    for rr in range(4, r + 1):
        for j in (2, 3, 4, 5):
            ws.cell(row=rr, column=j).number_format = "#,##0"
        for j in (6, 7, 9):
            ws.cell(row=rr, column=j).number_format = "0.0%"
        ws.cell(row=rr, column=8).number_format = "0.00%"

    r += 2
    ws.cell(row=r, column=1, value="Book at 30 September 2026").font = Font(bold=True, size=11)
    lines = [
        ("Groups monitored", F["N1"], "#,##0", "active on the group register and not on the watch list (s4.1)"),
        ("Flagged AMBER or RED", F["F1"], "#,##0", "September 2026 publication, any member (s3.2)"),
        ("Flagged share", round(F["a1"], 3), "0.0%", ""),
        ("Share of book expected to reach the list", round(F["p1"], 3), "0.0%",
         "(flagged share less false-alarm rate) / (capture rate less false-alarm rate)"),
        ("Probability of reaching, flagged", round(F["p_flag"], 3), "0.0%",
         "capture rate x expected share / flagged share"),
        ("Probability of reaching, not flagged", round(F["p_unflag"], 3), "0.0%",
         "(1 - capture rate) x expected share / (1 - flagged share)"),
        ("Expected arrivals", r1(F["expected"]), "0.0", "%.1f flagged + %.1f not flagged; caseload %d"
         % (F["total"]["flagged"], F["total"]["unflagged"], F["call"])),
    ]
    for label, v, fmt, note in lines:
        r += 1
        ws.cell(row=r, column=1, value=label)
        cell = ws.cell(row=r, column=2, value=v)
        cell.number_format = fmt
        ws.cell(row=r, column=3, value=note).font = Font(size=9, color=GREY)
    hits = [c["hit"] for c in F["cohorts"]]
    caps = [c["capture"] for c in F["cohorts"]]
    fas = [c["false_alarm"] for c in F["cohorts"]]
    shares = [c["share"] for c in F["cohorts"]]
    fsh = [c["flagged_share"] for c in F["cohorts"]]
    r += 2
    text = [
        "The hit rate has moved from %.1f%% to %.1f%% with the share of each cohort that reached the list (%.1f%% to %.1f%%); "
        % (min(hits) * 100, max(hits) * 100, min(shares) * 100, max(shares) * 100)
        + "capture (%.1f%% to %.1f%%) and false-alarm (%.2f%% to %.2f%%) rates have held."
        % (min(caps) * 100, max(caps) * 100, min(fas) * 100, max(fas) * 100),
        "Re-run from the other three cohorts, capture and false-alarm rates reproduce each cohort's arrivals within 3%; "
        "hit and miss rates miss two of the four by more than a third.",
        "This year %.1f%% of the book is flagged, against %.1f%% to %.1f%% in the closed cohorts, so the 2026 probabilities "
        "come from the capture and false-alarm rates, not from the hit rate." % (F["a1"] * 100, min(fsh) * 100,
                                                                                max(fsh) * 100),
    ]
    for t in text:
        ws.cell(row=r, column=1, value=t).font = Font(size=9, color=GREY)
        r += 1
    for col, wd in zip("ABCDEFGHI", [38, 12, 10, 12, 12, 10, 12, 12, 14]):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A4"


def notes_sheet(wb):
    ws = wb.create_sheet("Notes")
    rows = [
        ("Notes", ""),
        ("As at", "Monitored book, flags and committed exposure at 30 September 2026. Forecast window 1 October 2026 "
                  "to 30 September 2027."),
        ("Obligor groups", "Group register customers plus GLEIF accounting-consolidation members in force at each date "
                           "(CRM-07 s2.2, s2.3). Engine signals keyed by LEI or Companies House number."),
        ("Flag", "Any member AMBER or RED in the engine's month-end publication for the date (s3.2)."),
        ("Cohorts", "30 September 2022 to 2025. Reached: placed on the watch list, any watch level, within twelve "
                    "months of the cohort date; groups leaving the book unplaced have not reached it (s4.1, s4.2)."),
        ("Forecast", "Monitored book at 30 September 2026 only, no new groups (s5.1). One probability for flagged "
                     "groups and one for the rest, set from the four cohorts taken together (s4.3, s5.2)."),
        ("Committed exposure", "Committed limits of facilities in force at the end of 30 September 2026: status ACTIVE "
                               "and final maturity after that date. HB-PLC from the 23:05 rerun, the record for 30/09 "
                               "per the extract log; HB-DAC from its own extract, delivered 7 October. Non-sterling "
                               "limits divided by the Group Treasury closing rate, quoted per pound (s6.1)."),
        ("Bands", "Under £5m; £5m and under £15m; £15m and under £40m; £40m and under £100m; £100m and over (s6.2)."),
        ("Source", "Reference Data quarter-end pack as at 30/09/2026, compiled 08/10/2026."),
        ("Prepared", "Credit Risk Monitoring, 27 October 2026."),
    ]
    for a, b in rows:
        ws.append([a, b])
    ws["A1"].font = Font(bold=True, size=12)
    for rr in range(2, ws.max_row + 1):
        ws.cell(row=rr, column=1).font = Font(bold=True, size=10)
        ws.cell(row=rr, column=1).alignment = Alignment(vertical="top")
        ws.cell(row=rr, column=2).alignment = Alignment(wrap_text=True, vertical="top")
    ws.column_dimensions["A"].width = 20
    ws.column_dimensions["B"].width = 96


# ------------------------------------------------------------------ chart
def chart(F, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.transforms as mtransforms
    plt.rcParams["font.family"] = "Carlito"
    plt.rcParams["svg.fonttype"] = "none"
    plt.rcParams["svg.hashsalt"] = "halstow-crm-caseload-2027"
    ink, ink2, grid = "#1f2328", "#5b6169", "#e4e6ea"
    c_flag, c_not = "#a3412b", "#d8ccbc"
    fl = [row["flagged"] for row in F["rows"]]
    un = [row["unflagged"] for row in F["rows"]]
    x = list(range(5))
    fig, ax = plt.subplots(figsize=(10, 6.1), dpi=150)
    fig.patch.set_facecolor("white")
    ax.bar(x, fl, width=0.58, color=c_flag, zorder=2, label="Flagged AMBER or RED by the September run")
    ax.bar(x, un, width=0.58, bottom=fl, color=c_not, zorder=2, label="Not flagged")
    for i in x:
        ax.text(i, fl[i] / 2, "%.1f" % fl[i], ha="center", va="center", color="white", fontsize=11, fontweight="bold",
                zorder=3)
        if un[i] >= 3.0:
            ax.text(i, fl[i] + un[i] / 2, "%.1f" % un[i], ha="center", va="center", color=ink, fontsize=10.5, zorder=3)
        else:
            ax.text(i, fl[i] + un[i] + 0.7, "%.1f" % un[i], ha="center", va="bottom", color=ink, fontsize=10.5, zorder=3)
    ax.set_xlim(-0.6, 4.6)
    ax.set_ylim(0, 50)
    ax.set_yticks([0, 10, 20, 30, 40, 50])
    ax.set_yticklabels(["0", "10", "20", "30", "40", "50"], fontsize=10, color=ink2)
    ax.set_ylabel("Expected arrivals (groups)", fontsize=10.5, color=ink2)
    ax.set_xticks(x)
    ax.set_xticklabels(["Under\n£5m", "£5m and\nunder £15m", "£15m and\nunder £40m", "£40m and\nunder £100m",
                        "£100m\nand over"], fontsize=10.5, color=ink)
    ax.tick_params(axis="x", length=0, pad=6)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="y", color=grid, linewidth=0.8, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#9aa0a8")
    tr = mtransforms.blended_transform_factory(ax.transData, ax.transAxes)
    for lo, hi, name in ((-0.32, 2.32, "Business Support"), (2.68, 4.32, "Restructuring")):
        ax.plot([lo, hi], [-0.175, -0.175], transform=tr, color="#9aa0a8", lw=0.9, clip_on=False)
        ax.text((lo + hi) / 2, -0.195, name, transform=tr, ha="center", va="top", fontsize=10, color=ink2)
    ax.text(0.985, 0.93, "%d" % F["call"], transform=ax.transAxes, ha="right", va="top", fontsize=46,
            fontweight="bold", color=c_flag)
    ax.text(0.985, 0.785, "groups in the 2027 watch-list caseload", transform=ax.transAxes, ha="right", va="top",
            fontsize=12, color=ink)
    ax.text(0.985, 0.73, "%.1f flagged + %.1f not flagged, to the nearest group"
            % (F["total"]["flagged"], F["total"]["unflagged"]), transform=ax.transAxes, ha="right", va="top",
            fontsize=9.5, color=ink2)
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 1.075), ncol=2, frameon=False, fontsize=10,
              handlelength=1.2, columnspacing=1.6)
    fig.text(0.012, 0.968, TITLE % (F["call"], F["N1"]), ha="left", va="top", fontsize=15, fontweight="bold", color=ink)
    fig.text(0.012, 0.922, "Expected arrivals by committed-exposure band at 30 September 2026, split by the "
             "September early-warning flag", ha="left", va="top", fontsize=11, color=ink2)
    fig.text(0.012, 0.018, "Flagged groups reach the list with probability %.1f%%, the rest %.1f%%, set from the 2022 "
             "to 2025 cohorts taken together (CRM-07 s4.3, s5.2). Bands per s6.2."
             % (F["p_flag"] * 100, F["p_unflag"] * 100), ha="left", va="bottom", fontsize=8.5, color=ink2)
    fig.text(0.988, 0.018, "Credit Risk Monitoring, 27 October 2026", ha="right", va="bottom", fontsize=8.5,
             color=ink2)
    fig.subplots_adjust(left=0.075, right=0.985, top=0.82, bottom=0.2)
    buf = io.StringIO()
    fig.savefig(buf, format="svg", facecolor="white",
                metadata={"Date": None, "Creator": None, "Format": None, "Type": None})
    plt.close(fig)
    svg = buf.getvalue()
    # Calibri first (Carlito is its metric twin, so the layout holds); plain group ids
    svg = svg.replace("font-family: 'Carlito'", "font-family: Calibri, Carlito, sans-serif")
    svg = re.sub(r'id="matplotlib\.', 'id="', svg)
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg)


# ------------------------------------------------------------------ read back
def verify(F):
    wb = openpyxl.load_workbook(os.path.join(GOLD, XLSX))
    ws = wb["Caseload 2027"]
    assert ws["D5"].value == F["call"] == 134
    got = []
    for row in ws.iter_rows(min_row=9, max_row=14, values_only=True):
        got.append(tuple(row[:4]))
    want = [(r["band"], r["flagged"], r["unflagged"], r["exposure"]) for r in F["rows"] + [F["total"]]]
    assert got == want, (got, want)
    assert abs(sum(r["flagged"] for r in F["rows"]) - F["total"]["flagged"]) < 1e-9
    assert abs(sum(r["unflagged"] for r in F["rows"]) - F["total"]["unflagged"]) < 1e-9
    assert abs(sum(r["exposure"] for r in F["rows"]) - F["total"]["exposure"]) < 1e-9
    assert round(F["total"]["flagged"] + F["total"]["unflagged"]) == F["call"]
    with zipfile.ZipFile(os.path.join(GOLD, XLSX)) as z:
        meta = b"".join(z.read(n) for n in z.namelist() if n.startswith("docProps/"))
    assert b"openpyxl" not in meta and b"2026-10-2" in meta
    svg = open(os.path.join(GOLD, CHART), encoding="utf-8").read()
    texts = [html.unescape(t) for t in re.findall(r"<text[^>]*>([^<]*)</text>", svg)]
    assert "matplotlib" not in svg.lower() and "carlito'" not in svg.lower()
    assert TITLE % (F["call"], F["N1"]) in texts, texts
    assert str(F["call"]) in texts
    for row in F["rows"]:
        assert "%.1f" % row["flagged"] in texts and "%.1f" % row["unflagged"] in texts, row
    assert all("\u2014" not in t and "\u2013" not in t for t in texts)
    for wbk in (wb,):
        for s in wbk.worksheets:
            for row in s.iter_rows(values_only=True):
                for v in row:
                    if isinstance(v, str):
                        assert "—" not in v and "–" not in v, v
    return want


def main():
    os.makedirs(GOLD, exist_ok=True)
    F = figures()
    workbook(F, os.path.join(GOLD, XLSX))
    chart(F, os.path.join(GOLD, CHART))
    for w in verify(F):
        print("%-22s %6.1f %6.1f %9.1f" % w)
    print("caseload", F["call"], "p_flag %.4f p_unflag %.4f p1 %.4f a1 %.4f" % (F["p_flag"], F["p_unflag"], F["p1"], F["a1"]))


if __name__ == "__main__":
    main()
