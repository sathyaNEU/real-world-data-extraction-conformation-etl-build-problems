"""Golden deliverables for task446, computed by solve.py from target/ only."""
import datetime as dt
import os
import sys

import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve
from docs import normalize_zip

GOLD = os.path.join(HERE, "..", "golden")
XLSX = "limit_check_2026-11-04.xlsx"
PNG = "projected_utilisation_2026Q4.png"
SHORT = {"B1": "Kelderby", "B2": "Meridale", "B3": "Brauneck", "B4": "Corrin", "B5": "Pellow", "B6": "Stannard"}


def m1(x):
    return round(x / 1e6 + 1e-12, 1)


def results():
    pack = solve.Pack()
    res = solve.run(pack, "restated")
    names = {}
    for r in res:
        rec = pack.l1[solve.PROJ].get(r["top"])
        names[r["item"]] = rec["Entity.LegalName"]
    res.sort(key=lambda r: -r["utilisation"])
    return pack, res, names


def workbook(res, names, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Limit check"
    x = [r for r in res if r["item"] == "B1"][0]
    ws["A1"] = "Credit Committee 4 November 2026, Part B: limit check under LMS-03"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Projection date 30 September 2026, projected to 31 December 2026. GBP m unless stated. "
                "Quarter-end exposures are for each group as it stands at 30 September 2026.")
    ws["A3"] = "B1 Kelderby Facilities Ltd: approve GBP %.1fm of the GBP %.1fm term loan." % (x["approvable"], x["request"])
    ws["A3"].font = Font(bold=True)
    hdr = ["Item", "Borrower", "Obligor group", "House limit",
           "Drawn loans", "Undrawn commitments (50%)", "Securities", "Derivatives",
           "30 Sep 2025", "31 Dec 2025", "31 Mar 2026", "30 Jun 2026", "30 Sep 2026",
           "Projected 31 Dec 2026", "Utilisation %", "Requested", "Facility", "Approvable"]
    ws.append([])
    ws.append(hdr)
    hr = ws.max_row
    thin = Side(style="thin", color="999999")
    for c in range(1, len(hdr) + 1):
        cell = ws.cell(row=hr, column=c)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(wrap_text=True, vertical="bottom")
        cell.border = Border(bottom=thin)
    for r in res:
        b = r["books"]
        row = [r["item"], r["borrower"], names[r["item"]], r["limit"],
               m1(b.get("loans_drawn", 0)), m1(b.get("undrawn", 0)), m1(b.get("securities", 0)),
               m1(b.get("derivatives", 0))] + [m1(v) for v in r["series"]] + \
              [m1(r["projected"]), round(r["utilisation"] * 100, 1), r["request"],
               "RCF" if r["ftype"].startswith("Revolving") else "Term", r["approvable"]]
        ws.append(row)
        rr = ws.max_row
        for c in range(4, 17):
            ws.cell(row=rr, column=c).number_format = "0.0"
        ws.cell(row=rr, column=18).number_format = "0.0"
        if r["item"] == "B1":
            for c in range(1, len(hdr) + 1):
                ws.cell(row=rr, column=c).fill = PatternFill("solid", fgColor="E8F0FA")
    ws.append([])
    ws.append(["Exposure under Credit Concentration Policy s3; undrawn commitments counted at 50%. Projection: "
               "30 Sep 2026 exposure plus the least-squares slope over the five quarter-ends (LMS-03 2.2)."])
    ws.append(["Approvable: largest multiple of GBP 0.1m within the request for which projected exposure plus the "
               "new commitment (term loan 100%, RCF 50%) stays within the house limit (LMS-03 3.2)."])
    widths = [6, 32, 30, 8, 9, 13, 10, 11, 10, 10, 10, 10, 10, 12, 11, 10, 8, 11]
    from openpyxl.utils import get_column_letter
    for i, wd in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    ws.row_dimensions[hr].height = 30
    ws.freeze_panes = ws.cell(row=hr + 1, column=3)
    ws.print_title_rows = "%d:%d" % (hr, hr)
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    membership_sheet(wb, res, names)
    notes = wb.create_sheet("Notes")
    for line in [
        ["Notes"],
        ["Projection date", "30 September 2026 (latest closed quarter-end, LMS-03 2.1)"],
        ["Group structure", "GLEIF files archived 30 September 2026, read under Credit Concentration Policy s2"],
        ["Quarter-end exposures", "Each group as constituted at 30 September 2026, restated back to 30 September 2025 (LMS-03 2.3)"],
        ["Loan book", "CRDM quarter-end extracts incl. the late CWB-DUB file for 31 Dec 2025; migrated facilities counted once"],
        ["Derivatives", "CCR-NS-01, 30 Sep 2026 taken from the R2 rerun; GBP 000 converted; cash CSA collateral only"],
        ["Rounding", "Exposures computed in pounds and rounded for display only; components may not add to totals"],
        ["Prepared", "Credit Portfolio Analytics, 2 November 2026"],
    ]:
        notes.append(line)
    notes["A1"].font = Font(bold=True)
    notes.column_dimensions["A"].width = 24
    notes.column_dimensions["B"].width = 110
    p = wb.properties
    p.creator = "Lesley Miller"
    p.lastModifiedBy = "Lesley Miller"
    p.created = dt.datetime(2026, 10, 29, 9, 12)
    p.modified = dt.datetime(2026, 11, 2, 8, 41)
    wb.save(path)
    normalize_zip(path, dt.datetime(2026, 11, 2, 8, 41))


def membership_sheet(wb, res, names):
    pack = solve.Pack()
    G = solve.Groups(pack, solve.PROJ, solve.PROJ)
    l1 = pack.l1[solve.PROJ]
    ws = wb.create_sheet("Membership 30 Sep 2026")
    ws.append(["Obligor group", "LEI", "Entity", "Link at 30 Sep 2026", "Change in the year"])
    for c in range(1, 6):
        ws.cell(row=1, column=c).font = Font(bold=True)
    tops = {r["top"]: names[r["item"]] for r in res}
    leis = set(r["customer_lei"] for r in pack.loans) | set(r["Counterparty LEI"] for q in pack.drv.values() for r in q)
    leis |= {(r["issuer_lei"] or pack.isin.get(r["isin"], "")) for r in pack.secs}
    rr = pack.rr[solve.PROJ]
    rows = []
    for lei in sorted(l for l in leis if l):
        t = G.top(lei)
        if t not in tops:
            continue
        rec = l1.get(lei, {})
        link = "ultimate parent"
        if lei != t:
            if rec.get("Registration.RegistrationStatus") == "MERGED":
                link = "merged into " + l1[rec["Entity.SuccessorEntity.SuccessorLEI"]]["Entity.LegalName"]
            elif lei in G.branch:
                link = "branch of " + l1[G.branch[lei]]["Entity.LegalName"]
            elif lei in G.direct:
                link = "consolidated by " + l1[G.direct[lei]]["Entity.LegalName"]
            elif lei in G.parent:
                link = "consolidated by " + l1[G.parent[lei]]["Entity.LegalName"]
        change = ""
        for r in rr:
            if r["Relationship.StartNode.NodeID"] != lei or not r["Relationship.RelationshipType"].endswith("CONSOLIDATED_BY"):
                continue
            st, en = r["Relationship.Period.1.startDate"][:10], r["Relationship.Period.1.endDate"][:10]
            if r["Relationship.RelationshipStatus"] == "ACTIVE" and "2025-09-30" < st <= "2026-09-30":
                change = "joined %s, restated into all five quarter-ends" % st
        rows.append([tops[t], lei, rec.get("Entity.LegalName", ""), link, change])
    # borrowers that left an agenda group during the year
    for lei, newtop in [(r["Relationship.StartNode.NodeID"], None) for r in rr
                        if r["Relationship.RelationshipStatus"] == "INACTIVE"
                        and r["Relationship.EndNode.NodeID"] in tops
                        and "2025-09-30" < r["Relationship.Period.1.endDate"][:10] <= "2026-09-30"
                        and r["Relationship.RelationshipType"] == "IS_ULTIMATELY_CONSOLIDATED_BY"]:
        old = [r for r in rr if r["Relationship.StartNode.NodeID"] == lei and r["Relationship.RelationshipStatus"] == "INACTIVE"
               and r["Relationship.EndNode.NodeID"] in tops][0]
        if lei not in leis or G.top(lei) in tops and tops.get(G.top(lei)) == tops[old["Relationship.EndNode.NodeID"]]:
            continue
        rows.append([tops[old["Relationship.EndNode.NodeID"]], lei, l1[lei]["Entity.LegalName"],
                     "now in " + l1[G.top(lei)]["Entity.LegalName"],
                     "left %s, out of all five quarter-ends" % old["Relationship.Period.1.endDate"][:10]])
    rows.sort(key=lambda r: (r[0], r[3] != "ultimate parent", r[2]))
    for r in rows:
        ws.append(r)
    for col, wd in zip("ABCDE", [30, 23, 40, 50, 44]):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A2"


def chart(res, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    surface, ink, ink2, grid = "#fcfcfb", "#0b0b0b", "#52514e", "#e4e2dc"
    base, focus = "#9fbfe6", "#2a78d6"
    x = [r for r in res if r["item"] == "B1"][0]
    labels = ["%s  %s" % (r["item"], SHORT[r["item"]]) for r in res]
    vals = [r["utilisation"] * 100 for r in res]
    fig, ax = plt.subplots(figsize=(9.2, 4.8), dpi=150)
    fig.patch.set_facecolor(surface)
    ax.set_facecolor(surface)
    ys = list(range(len(res)))[::-1]
    for y, r, v in zip(ys, res, vals):
        ax.barh(y, v, height=0.56, color=focus if r["item"] == "B1" else base, zorder=2)
        ax.text(v - 1.0, y, "%.1f%%" % v, va="center", ha="right", fontsize=9,
                color="white" if r["item"] == "B1" else ink, zorder=3)
    ax.axvline(100, color=ink2, linestyle=(0, (4, 3)), linewidth=1.2, zorder=1)
    ax.text(100.6, ys[0] + 0.45, "House limit 100%", fontsize=8.5, color=ink2, va="bottom")
    xy = ys[[r["item"] for r in res].index("B1")]
    ax.annotate("Approve GBP %.1fm of GBP %.1fm" % (x["approvable"], x["request"]),
                xy=(x["utilisation"] * 100, xy), xytext=(101.5, xy - 0.05), fontsize=9, color=ink, va="center",
                arrowprops=dict(arrowstyle="-", color=ink2, lw=0.8))
    ax.set_yticks(ys)
    ax.set_yticklabels(labels, fontsize=9.5, color=ink)
    ax.set_xlim(0, 125)
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"], fontsize=8.5, color=ink2)
    ax.grid(axis="x", color=grid, linewidth=0.8, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(grid)
    ax.tick_params(axis="y", length=0)
    ax.set_xlabel("Projected 31 Dec 2026 exposure as a share of the house limit", fontsize=9, color=ink2)
    fig.suptitle("Kelderby can take GBP %.1fm of its GBP %.1fm term loan" % (x["approvable"], x["request"]),
                 x=0.015, ha="left", fontsize=12.5, fontweight="bold", color=ink)
    ax.set_title("Credit Committee 4 November 2026, Part B requests by projected utilisation", loc="left",
                 fontsize=9.5, color=ink2, pad=8)
    fig.tight_layout(rect=(0, 0, 1, 0.975))
    fig.savefig(path, facecolor=surface, metadata={"Software": None})
    plt.close(fig)


def main():
    os.makedirs(GOLD, exist_ok=True)
    pack, res, names = results()
    workbook(res, names, os.path.join(GOLD, XLSX))
    chart(res, os.path.join(GOLD, PNG))
    for r in res:
        print(r["item"], SHORT[r["item"]], [m1(v) for v in r["series"]], m1(r["projected"]),
              round(r["utilisation"] * 100, 1), r["approvable"],
              {k: m1(v) for k, v in r["books"].items()})


if __name__ == "__main__":
    main()
