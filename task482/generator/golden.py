"""The golden: every owed figure computed from the cut pack (bundle.py), written to generator/figures.json, and the two
deliverables, penwick_refrigerator_replacements_2027.xlsx and penwick_vaccine_hours_2026.svg."""
import io
import json
import os

import numpy as np

import bundle as B

HERE = os.path.dirname(os.path.abspath(__file__))
XLSX = "penwick_refrigerator_replacements_2027.xlsx"
SVG = "penwick_vaccine_hours_2026.svg"


def town_of(target):
    rows = B._sheet(target, "stores", "Stores")
    return {int(r["Store"]): r["Town"] for r in rows}


def compute(target):
    I = B.Inputs(target)
    town = town_of(target)
    tau = B.taus(I)
    pooled = B.taus(I, "pooled")
    h = B.golden_hours(I, tau)
    r0 = B.rung_hours(I, "R0")
    ua = B.unaccounted(I)
    sv = B.service(I)
    cov = B.covered(h)
    nb, nbv, short = B.nearest_below(h)
    makes = {}
    for no in I.order:
        makes.setdefault(I.make[no], round(tau[no], 1))
    fit_lag = {mk: round(B.fit(I, [no for no in I.pilot if I.make[no] == mk])[1], 3) for mk in makes}
    fig = {
        "call": {"stores": cov, "count": len(cov), "of": len(I.order)},
        "stores": {str(no): {"town": town[no], "hours": B.hround(h[no]), "replaced": no in cov,
                             "doses_unaccounted": int(ua[no]), "service_usd": B.hround(sv[no])} for no in I.order},
        "components": {
            "nearest_below": {"store": nb, "town": town[nb], "hours": B.hround(nbv), "short_hours": B.hround(short)},
            "tau_minutes": makes, "tau_pooled_minutes": round(pooled[I.order[0]], 1),
            "pilot_stores": len(I.pilot),
            "fit_rms_c": fit_lag,
            "replaced_hours": {str(no): B.hround(h[no]) for no in cov},
        },
        "default": {"stores": B.covered(r0), "count": len(B.covered(r0)),
                    "hours": {str(no): B.hround(r0[no]) for no in I.order}},
        "stated": {"limit_c": 8.0, "line_hours": 24, "year": 2026, "installed_by": "1 September 2027",
                   "tax_pct": 6.0, "platform": "1 July 2026", "inventory_update": "1 June 2026",
                   "record_minutes": 10, "bud_days": 28,
                   "sections": {"recording": 6.3, "device_of_record": 6.4, "criterion": 7.3, "unaccounted": 8.2,
                                "service": 9.2},
                   "replaced_loggers": sorted(no for no in I.order if sum(1 for s, n in I.serial.items()
                                                                           if n == no) > 1)},
        "store_numbers": list(I.order),
        "_unrounded": {"hours": {str(no): round(h[no], 4) for no in I.order},
                       "default": {str(no): round(r0[no], 4) for no in I.order},
                       "service": {str(no): sv[no] for no in I.order},
                       "tau": {str(no): tau[no] for no in I.order}},
    }
    return fig


def write_xlsx(path, f):
    import openpyxl
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = openpyxl.Workbook()
    bold = Font(name="Calibri", size=11, bold=True)
    thin = Side(style="thin", color="808080")
    fill = PatternFill("solid", fgColor="DDEBF7")
    st = f["stores"]
    nb = f["components"]["nearest_below"]

    ws = wb.active
    ws.title = "2027 replacements"
    n_rep = f["call"]["count"]
    words = {1: "One store gets", 2: "Two stores get", 3: "Three stores get", 4: "Four stores get", 5: "Five stores get",
             6: "Six stores get", 7: "Seven stores get", 8: "Eight stores get"}
    ws["A1"] = "%s a new vaccine refrigerator before the 2027 respiratory season" % words.get(n_rep, "%d stores get" % n_rep)
    ws["A1"].font = Font(name="Calibri", size=14, bold=True)
    ws["A2"] = ("Pharmacy Operations, for the capital committee, February 2027. Standard PO-114 section 7.3: 24 hours or "
                "more with the vaccine above 8.0 \u00b0C in 2026.")
    ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="555555")
    ws.append([])
    ws.append(["Store", "Town", "Hours above 8.0 \u00b0C, 2026", "New refrigerator"])
    for c in ws[4]:
        c.font = bold
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
        c.border = Border(bottom=thin)
    for no in sorted(st, key=lambda k: (-f["_unrounded"]["hours"][k], int(k))):
        x = st[no]
        ws.append([int(no), x["town"], x["hours"], "Yes" if x["replaced"] else "No"])
        if x["replaced"]:
            for c in ws[ws.max_row]:
                c.fill = fill
    last = ws.max_row
    for row in ws.iter_rows(min_row=5, max_row=last):
        row[2].number_format = "#,##0"
        row[3].alignment = Alignment(horizontal="center")
    ws.cell(row=last + 2, column=1, value="Nearest store below the line: %d %s, %d hours, %d short of 24."
            % (nb["store"], nb["town"], nb["hours"], nb["short_hours"]))
    ws.cell(row=last + 2, column=1).font = Font(name="Calibri", size=10, bold=True)
    for col, wd in zip("ABCD", (8, 14, 14, 13)):
        ws.column_dimensions[col].width = wd
    ws.row_dimensions[4].height = 30
    ws.freeze_panes = "A5"

    s2 = wb.create_sheet("Stock and service")
    s2.append(["Store", "Town", "2026 vaccine doses unaccounted for", "2026 Brannon refrigerator service (USD)"])
    for c in s2[1]:
        c.font = bold
        c.alignment = Alignment(wrap_text=True, vertical="bottom")
        c.border = Border(bottom=thin)
    for no in sorted(st, key=int):
        x = st[no]
        s2.append([int(no), x["town"], x["doses_unaccounted"], x["service_usd"]])
    s2.append(["All stores", None, sum(x["doses_unaccounted"] for x in st.values()),
               int(round(sum(f["_unrounded"]["service"].values())))])
    for c in s2[s2.max_row]:
        c.font = bold
        c.border = Border(top=thin)
    for row in s2.iter_rows(min_row=2, max_row=s2.max_row):
        row[2].number_format = "#,##0"
        row[3].number_format = "#,##0"
    for col, wd in zip("ABCD", (8, 14, 16, 18)):
        s2.column_dimensions[col].width = wd
    s2.row_dimensions[1].height = 46
    s2.freeze_panes = "A2"

    s3 = wb.create_sheet("Notes")
    tau = f["components"]["tau_minutes"]
    notes = [
        ("Hours above 8.0 \u00b0C", "Each logger record put on UTC and joined to its store through the monitoring roster "
         "(Kelvra converted from Fahrenheit, Brumal from standard time, one Kelvra day exported twice counted "
         "once). A logger's probe follows the air in minutes and the vaccine follows it in most of an hour, so each "
         "logger record is carried through the vaccine's response, a first-order lag with each record holding over its "
         "ten minutes. Its time constant is fitted on the two weeks each pilot store's logger kept recording after its "
         "in-carton sensor went in: %.1f minutes for Frostline, %.1f for Kelvra and %.1f for Brumal. A record counts "
         "its ten minutes when the estimated vaccine temperature at its time stamp is above 8.0 \u00b0C; at the pilot stores "
         "the in-carton sensor's readings count from its first reading." % (tau["Frostline"], tau["Kelvra"],
                                                                            tau["Brumal"])),
        ("Doses unaccounted for", "The 2025 year-end count, plus Meridale deliveries and transfers in, less doses "
         "administered, written off and transferred out, less the 2026 year-end count, each flow taken between the two "
         "counts' own closing times. Write-offs of multi-dose vials before the 1 June 2026 inventory update are in "
         "vials (ten doses each). Meridale's return credits are the expired 2025-26 doses already written off and are "
         "not taken off again."),
        ("Brannon service", "Each invoice once, for work completed in 2026 (its last visit). Invoices dated before "
         "Brannon's 1 July 2026 platform move show the amount before sales tax, so 6.0 per cent is added to them. A "
         "maintenance route invoiced for two stores is split by each unit's maintenance price in Schedule B of the "
         "agreement."),
        ("Rounding", "Hours, doses and dollars to the whole unit, each from the unrounded figure."),
    ]
    s3.append(["Item", "Note"])
    for c in s3[1]:
        c.font = bold
    for k, v in notes:
        s3.append([k, v])
    for row in s3.iter_rows(min_row=2):
        row[1].alignment = Alignment(wrap_text=True, vertical="top")
        row[0].alignment = Alignment(vertical="top")
    s3.column_dimensions["A"].width = 22
    s3.column_dimensions["B"].width = 100
    wb.save(path)
    import postprocess as PP
    PP.normalize_ooxml(path, "Pharmacy Operations", "Pharmacy Operations", "2027-02-01T14:20:00Z",
                       "2027-02-08T21:37:44Z", excel=True, company="Penwick Pharmacy, Inc.")


def write_svg(path, f):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import Patch
    matplotlib.rcParams["svg.hashsalt"] = "task482-penwick"
    matplotlib.rcParams["svg.fonttype"] = "none"
    matplotlib.rcParams["font.family"] = "DejaVu Sans"
    un = f["_unrounded"]["hours"]
    st = f["stores"]
    names = sorted(st, key=lambda k: (-un[k], int(k)))
    vals = [un[k] for k in names]
    on = [st[k]["replaced"] for k in names]
    blue, grey, ink, muted, line = "#2a6fb0", "#c3c8ce", "#1f2328", "#59636e", "#b3261e"
    fig, ax = plt.subplots(figsize=(8.6, 8.4), dpi=100)
    ys = np.arange(len(names))[::-1]
    ax.barh(ys, vals, height=0.68, color=[blue if o else grey for o in on], edgecolor="white", linewidth=1.5, zorder=3)
    for y, k, v, o in zip(ys, names, vals, on):
        ax.text(v + 0.8, y, "%d" % st[k]["hours"], ha="left", va="center", fontsize=8.5,
                color=ink if o else muted, fontweight="bold" if o else "normal")
    ax.axvline(24, color=line, linewidth=1.5, zorder=4)
    ax.text(24.6, ys[0] + 0.6, "24 hours", color=line, fontsize=8.5, va="bottom")
    ax.set_yticks(ys)
    ax.set_yticklabels(["%s %s" % (k, st[k]["town"]) for k in names], fontsize=8.5, color=ink)
    ax.set_xlabel("Hours with the vaccine above 8.0 \u00b0C in 2026", fontsize=9, color=muted)
    ax.set_xlim(0, max(vals) * 1.12)
    ax.set_ylim(-0.7, len(names) - 0.1)
    ax.tick_params(axis="x", labelsize=8.5, colors=muted)
    ax.grid(axis="x", color="#e6e8eb", linewidth=0.8, zorder=0)
    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color("#9aa1a9")
    ax.legend(handles=[Patch(color=blue, label="New refrigerator before the 2027 season"),
                       Patch(color=grey, label="Under 24 hours")], loc="lower right", frameon=False, fontsize=8.5)
    nb = f["components"]["nearest_below"]
    n = f["call"]["count"]
    word = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight"}.get(n, str(n))
    fig.suptitle("%s stores' vaccine spent 24 hours or more above 8 \u00b0C in 2026" % word, x=0.012, ha="left",
                 fontsize=11.5, fontweight="bold", color=ink)
    ax.set_title("Hours by store, from each store's temperature record carried to the vaccine.\n"
                 "Nearest below the line: %d %s, %d hours, %d short." % (nb["store"], nb["town"], nb["hours"],
                                                                        nb["short_hours"]),
                 loc="left", fontsize=8.5, color=muted, pad=10, linespacing=1.5)
    fig.text(0.012, 0.01, "Source: Penwick Pharmacy, Pharmacy Operations; store data loggers and Tellvane in-carton "
             "sensors, 2026.", fontsize=7.5, color=muted)
    fig.subplots_adjust(left=0.18, right=0.97, top=0.9, bottom=0.08)
    buf = io.StringIO()
    fig.savefig(buf, format="svg", metadata={"Date": None, "Creator": "Pharmacy Operations"})
    plt.close(fig)
    svg = buf.getvalue().replace('id="matplotlib.', 'id="').replace("'DejaVu Sans'",
                                                                   "'DejaVu Sans', Arial, Helvetica, sans-serif")
    assert "matplotlib" not in svg.lower()
    open(path, "w", encoding="utf-8", newline="\n").write(svg)


def main(target=None):
    target = target or os.path.join(os.path.dirname(HERE), "target")
    f = compute(target)
    json.dump(f, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    out = os.path.join(os.path.dirname(HERE), "golden")
    os.makedirs(out, exist_ok=True)
    for fn in os.listdir(out):
        os.remove(os.path.join(out, fn))
    write_xlsx(os.path.join(out, XLSX), f)
    write_svg(os.path.join(out, SVG), f)
    return f


if __name__ == "__main__":
    import sys
    f = main(sys.argv[1] if len(sys.argv) > 1 else None)
    print(json.dumps({k: v for k, v in f.items() if not k.startswith("_")}, indent=1)[:4000])
