"""The golden deliverables: coal_reserve_2026.xlsx (the winter reserve by pile area, the cover and the decision; the
book flows) and coalyard_stock_2026.svg (the yard's coal at every survey against the floor), with figures.json, every
figure as the write-up states it."""
import json
import os

import solve as SV
import world as W

GOLDEN = {"workbook": "coal_reserve_2026.xlsx", "chart": "coalyard_stock_2026.svg"}
MONTH = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
         "November", "December"]


def k1000(v):
    return int(round(v / 1000.0) * 1000)


def nice_date(iso):
    y, m, d = iso.split("-")
    return "%d %s %s" % (int(d), MONTH[int(m) - 1], y)


def figures(target):
    c = SV.compute(target)
    S, A, cl = c["S"], c["A"], c["call"]
    per = []
    for name in sorted(A):
        p = c["per"][name]
        dens_date = max(t[0] for t in SV.densities(target) if t[1] == A[name]["coal"] and t[0] < "2026-12-16")
        per.append(dict(area=name, coal=A[name]["coal"], base_survey=S.dates[p["base"]], volume_m3=k1000(p["volume"]),
                        density=p["density"], density_test=dens_date, tonnes=k1000(p["tonnes"]),
                        volume_exact=round(p["volume"], 1), tonnes_exact=round(p["tonnes"], 1)))
    rung = lambda k: dict(reserve=k1000(c["rungs"][k]["reserve"]), cover=int(round(c["rungs"][k]["cover"])),
                          nominate=c["rungs"][k]["nominate"])
    fig = dict(
        call=dict(decision="do not nominate the winter option cargo" if not cl["nominate"] else
                  "nominate the winter option cargo", nominate=cl["nominate"],
                  reserve=k1000(cl["reserve"]), reserve_exact=round(cl["reserve"], 1),
                  cover_days=int(round(cl["cover"])), cover_exact=round(cl["cover"], 3),
                  floor_days=W.FLOOR_DAYS, floor_t=k1000(cl["floor_t"]), margin_t=k1000(cl["margin_t"]),
                  margin_days=int(round(cl["margin_days"])), planned_burn=int(round(cl["burn"])),
                  plan_total=int(cl["plan_total"]), plan_days=int(cl["plan_days"])),
        piles=per,
        rungs=dict(toe_plane=rung("toe_plane"), toe_low=rung("toe_low"), toe_mean=rung("toe_mean"),
                   min_all=rung("min_all")),
        ask_a={k: k1000(v) for k, v in sorted(c["ask_a"].items())},
        ask_b={"Q%d" % (i + 1): k1000(v) for i, v in enumerate(c["ask_b"])},
        monthly=[dict(survey=S.dates[m], tonnes=int(round(v, -2))) for m, v in enumerate(c["monthly"])],
        cited=dict(datum_m=W.DH, rounding=1000, clauses=["3.2", "3.3", "1.1", "1.2", "2.1"]),
    )
    return fig, c


def write_workbook(path, fig):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = Workbook()
    ws = wb.active
    ws.title = "Winter reserve"
    b = Font(name="Calibri", bold=True)
    thin = Side(style="thin", color="A6A6A6")
    fill = PatternFill("solid", fgColor="DCE6F0")
    cl = fig["call"]
    ws["A1"] = "Winter coal reserve at the December survey, 16 December 2026 (PR-07)"
    ws["A1"].font = Font(name="Calibri", bold=True, size=13)
    ws["A2"] = ("%s, Satama power plant. Decision: %s; %d days of cover against the %d-day floor."
                % (W.ORG, cl["decision"][0].upper() + cl["decision"][1:], cl["cover_days"], W.FLOOR_DAYS))
    ws["A2"].font = Font(name="Calibri", bold=True, color="1F3A5C")
    hdr = ["Pile area", "Coal", "Pad as surveyed bare on", "Volume above pad, m3", "Bulk density, t/m3",
           "Density test of", "Coal, t"]
    for i, h in enumerate(hdr, 1):
        c = ws.cell(row=4, column=i, value=h)
        c.font, c.fill = b, fill
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=thin)
    r = 5
    for p in fig["piles"]:
        vals = [p["area"], p["coal"], nice_date(p["base_survey"]), p["volume_m3"], p["density"],
                nice_date(p["density_test"]), p["tonnes"]]
        for i, v in enumerate(vals, 1):
            c = ws.cell(row=r, column=i, value=v)
            if i in (4, 7):
                c.number_format = "#,##0"
            if i == 5:
                c.number_format = "0.000"
        r += 1
    ws.cell(row=r, column=1, value="Reserve").font = b
    c = ws.cell(row=r, column=7, value=cl["reserve"])
    c.font, c.number_format = b, "#,##0"
    r += 2
    lines = [("Planned burn, January to March 2027, t/d", cl["planned_burn"], "#,##0"),
             ("Days of cover", cl["cover_days"], "0"),
             ("Floor, %d days of planned burn, t" % W.FLOOR_DAYS, cl["floor_t"], "#,##0"),
             ("Reserve above the floor, t", cl["margin_t"], "#,##0"),
             ("Winter option cargo (Silesia, RL-HK-2026-03)", "Do not nominate; the option lapses on 8 January 2027"
              if not cl["nominate"] else "Nominate by 8 January 2027", None)]
    for label, v, fmt in lines:
        ws.cell(row=r, column=1, value=label)
        c = ws.cell(row=r, column=7 if fmt else 4, value=v)
        if fmt:
            c.number_format = fmt
        else:
            c.font = b
        r += 1
    ws.cell(row=r + 1, column=1, value=(
        "Volumes are the December surface above the yard pad as the 2026 surveys recorded it bare in each pile area "
        "(the pad has settled under the long-standing areas, so a base through the pile toe leaves coal out). The "
        "two contractors' surveys are taken onto ETRS-TM35FIN and N2000 by the July 2026 control report. Figures "
        "rounded to the nearest 1,000; days of cover to the whole day."))
    ws.cell(row=r + 1, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r + 1, start_column=1, end_row=r + 1, end_column=7)
    ws.row_dimensions[r + 1].height = 58
    for col, w in zip("ABCDEFG", (34, 9, 20, 14, 12, 18, 12)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"

    ws2 = wb.create_sheet("Book flows")
    ws2["A1"] = "The yard's book flows behind the December survey (OH-12)"
    ws2["A1"].font = Font(name="Calibri", bold=True, size=12)
    ws2["A3"] = "Received into the yard between the 17 December 2025 and 16 December 2026 surveys, CV-01"
    ws2["A3"].font = b
    ws2.append(["Coal", "Received, t"])
    for c in ws2[4]:
        c.font, c.fill = b, fill
    for coal, v in fig["ask_a"].items():
        ws2.append([coal, v])
        ws2.cell(row=ws2.max_row, column=2).number_format = "#,##0"
    ws2.append([])
    ws2.append(["Sent to the boiler house in 2026, CV-21, by calendar quarter (Finnish time)"])
    ws2.cell(row=ws2.max_row, column=1).font = b
    ws2.append(["Quarter", "Delivered, t"])
    for c in ws2[ws2.max_row]:
        c.font, c.fill = b, fill
    for q, v in fig["ask_b"].items():
        ws2.append(["%s 2026" % q, v])
        ws2.cell(row=ws2.max_row, column=2).number_format = "#,##0"
    ws2.append([])
    ws2.append(["Receipts are the unloader's coal on CV-01; coal moved between pile areas through the crossover and "
                "weighed on both belts is neither a receipt nor a delivery. Historian intervals carrying a "
                "communication loss's catch-up are placed back on the hours the shift log shows."])
    for col, w in zip("AB", (64, 16)):
        ws2.column_dimensions[col].width = w

    ws3 = wb.create_sheet("Notes")
    notes = [("As of", "4 January 2027"), ("Prepared by", W.FUEL_MANAGER + ", fuel manager"),
             ("Reserve", "PR-07 3.2: coal above the yard pad at the December survey times the latest density test"),
             ("Planned burn", "PR-07 3.3: the approved Q1 2027 plan's %s t over its %d days"
              % ("{:,}".format(cl["plan_total"]), cl["plan_days"])),
             ("Excluded", "Coal in the boiler house bunkers and coal not yet discharged (PR-07 2)"),
             ("Rounding", "Cubic metres and tonnes to the nearest 1,000, days of cover to the whole day")]
    for k, v in notes:
        ws3.append([k, v])
        ws3.cell(row=ws3.max_row, column=1).font = b
    ws3.column_dimensions["A"].width = 16
    ws3.column_dimensions["B"].width = 96
    wb.save(path)


def write_chart(path, fig):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import datetime as dt
    plt.rcParams["svg.hashsalt"] = "task462"
    plt.rcParams["font.family"] = "DejaVu Sans"
    xs = [dt.date.fromisoformat(m["survey"]) for m in fig["monthly"]]
    ys = [m["tonnes"] / 1000.0 for m in fig["monthly"]]
    cl = fig["call"]
    fl = cl["floor_t"] / 1000.0
    f, ax = plt.subplots(figsize=(8.6, 4.6), dpi=100)
    ax.plot(xs, ys, color="#1f5f8b", lw=2.0, marker="o", ms=4.5, zorder=3)
    ax.axhline(fl, color="#b5462e", lw=1.3, ls="--", zorder=2)
    ax.text(xs[0], fl + 2.2, "Floor for Q1 2027: %d days of planned burn, %s t" % (W.FLOOR_DAYS, "{:,}".format(
        cl["floor_t"])), color="#b5462e", fontsize=8.5)
    ax.annotate("16 December: %s t, %d days" % ("{:,}".format(cl["reserve"]), cl["cover_days"]),
                xy=(xs[-1], ys[-1]), xytext=(-182, 14), textcoords="offset points", fontsize=8.5,
                arrowprops=dict(arrowstyle="-", color="#555555", lw=0.8))
    ax.set_ylabel("Coal in the yard, thousand tonnes")
    ax.set_ylim(0, 175)
    ax.set_title("The yard went into winter with %d days of coal, above the %d-day floor" % (cl["cover_days"],
                                                                                            W.FLOOR_DAYS),
                 fontsize=11.5, loc="left")
    ax.grid(axis="y", color="#e3e6ea", lw=0.8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_xticks(xs)
    ax.set_xticklabels([d.strftime("%b %y") if i in (0, len(xs) - 1) else d.strftime("%b") for i, d in
                        enumerate(xs)], fontsize=8)
    f.text(0.01, 0.01, "Coal yard surveys (December 2025 to December 2026), volume above the pad each pile area "
                       "showed bare in 2026, latest laboratory densities. %s." % W.ORG, fontsize=7, color="#666666")
    f.tight_layout(rect=(0, 0.04, 1, 1))
    f.savefig(path, format="svg", metadata={"Date": None, "Creator": W.ORG})
    plt.close(f)
    svg = open(path, encoding="utf-8").read().replace('id="matplotlib.', 'id="')
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    fig, c = figures(target)
    write_workbook(os.path.join(gdir, GOLDEN["workbook"]), fig)
    import postprocess as PP
    PP.normalize_ooxml(os.path.join(gdir, GOLDEN["workbook"]), W.FUEL_MANAGER, W.FUEL_MANAGER,
                       "2027-01-04T07:05:00Z", "2027-01-04T09:12:00Z", excel=True, company=W.ORG)
    write_chart(os.path.join(gdir, GOLDEN["chart"]), fig)
    with open(fig_path, "w") as f:
        json.dump(fig, f, indent=1)
        f.write("\n")
    return fig
