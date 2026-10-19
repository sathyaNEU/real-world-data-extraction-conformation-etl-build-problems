"""The two deliverables: the coordinator's workbook and the pull list note with its chart."""
import io
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
import params as P
import nodes as N
import docs
import postprocess

STATION = {c: n.replace("Mencia", "Mencía") for c, n, _, _ in P.ANALYSERS}


def workbook(path, G):
    wb = Workbook()
    ws = wb.active
    ws.title = "Pull list"
    ws.append(["June 2028 round: span of every node over the eight weeks to 31 May 2028 (6 April to 31 May, local time)"])
    ws.append(["Span read against the regional network's four analysers on the window's afternoon hours (hours starting 12:00 "
               "to 17:00 local): the spread of the node's hourly ozone over those hours against the spread of the analysers' "
               "pooled hourly ozone over the same hours. Band 0.85 to 1.15 (QA plan v3, section 4)."])
    ws.append([])
    head = ["Node", "Municipality", "Model", "Span", "June round", "Reads"]
    ws.append(head)
    for c in N.CODES:
        v = G["span"][c]
        pull = c in G["pull"]
        ws.append([c, G["town"][c], "OZN-B" if c in N.MODEL_B else "OZN-A", round(v, 2),
                   "to the bench" if pull else "clean in place", G["pull"].get(c, "")])
        if pull:
            for cell in ws[ws.max_row]:
                cell.fill = PatternFill("solid", fgColor="FBE3D6")
    ws.append([])
    ws.append(["Nodes to the bench", len(G["pull"])])
    for r in ws.iter_rows(min_row=5, min_col=4, max_col=4):
        r[0].number_format = "0.00"
    for k, w in enumerate([8, 26, 8, 8, 16, 8]):
        ws.column_dimensions[get_column_letter(k + 1)].width = w
    for c in ws[4]:
        c.font = Font(bold=True)
    ws["A1"].font = Font(bold=True, size=12)
    ws.freeze_panes = "A5"
    ws2 = wb.create_sheet("Data capture")
    ws2.append(["Hours with an accepted reading, 1 November 2027 to 31 January 2028 (local time, 2,208 hours)"])
    ws2.append([])
    ws2.append(["Node", "Municipality", "Hours", "Share of the quarter"])
    for c in N.CODES:
        ws2.append([c, G["town"][c], G["capture"][c], G["capture"][c] / 2208.0])
    tot = sum(G["capture"].values())
    ws2.append(["All nodes", "", tot, tot / (2208.0 * 36)])
    for r in ws2.iter_rows(min_row=4, min_col=3, max_col=4):
        r[0].number_format = "#,##0"
        r[1].number_format = "0.0%"
    for k, w in enumerate([10, 26, 9, 20]):
        ws2.column_dimensions[get_column_letter(k + 1)].width = w
    for c in ws2[3]:
        c.font = Font(bold=True)
    ws2["A1"].font = Font(bold=True, size=12)
    ws2.freeze_panes = "A4"
    ws4 = wb.create_sheet("Notes")
    notes = [
        "As of 1 June 2028. Node export to 31 May 2028 23:00 UTC; regional network provisional release to the same hour.",
        "Span: the node's accepted hourly ozone (OZN-B half-hours averaged into hours; records sent twice counted once; "
        "status codes read by each node's firmware) against the analysers' P-flagged hours, both in ppb (micrograms at 20 C over 1.996).",
        "Afternoon hours only (12:00 to 18:00 local): at night the hill villages stand above the plain's surface inversion and "
        "keep ozone the analysers lose, so all-hours comparisons misread their heads.",
        "Data capture: hours in local time with at least one accepted reading (QA plan section 6); OZ19B's records are OZ19's "
        "(maintenance log, 9 to 25 January 2028); before a node's firmware 4.2 date its status-1 records are the warm-up after "
        "a restart, since humidity compensation came with 4.2; records stamped in 2000 come from a node's clock counting from "
        "a restart and are placed by their received time.",
    ]
    for n in notes:
        ws4.append([n])
        ws4.cell(ws4.max_row, 1).alignment = Alignment(wrap_text=True, vertical="top")
    ws4.column_dimensions["A"].width = 120
    wb.save(path)
    postprocess.scrub(path, P.CENTRE, "2028-06-01")
    postprocess.finish_office(path, "2028-06-01T07:58:00Z", "2028-06-01T15:21:00Z", P.CENTRE)


def chart(G):
    fig, ax = plt.subplots(figsize=(7.4, 3.4), dpi=160)
    xs = list(range(36))
    v = [G["span"][c] for c in N.CODES]
    ax.axhspan(0.85, 1.15, color="#E8F0E8", zorder=0)
    ax.axhline(0.85, color="#6A8F6A", lw=0.8)
    ax.axhline(1.15, color="#6A8F6A", lw=0.8)
    col = ["#B5442B" if c in G["pull"] else "#2F5F8A" for c in N.CODES]
    ax.scatter(xs, v, c=col, s=22, zorder=3)
    hi = [c for c in N.CODES if c in G["pull"] and G["span"][c] > 1]
    for x, c, y in zip(xs, N.CODES, v):
        if c in G["pull"]:
            dx = 0 if y < 1 else (-9 if hi.index(c) % 2 == 0 and len(hi) > 1 and hi.index(c) > 0 else (9 if hi.index(c) % 2 else 0))
            ax.annotate(c, (x, y), textcoords="offset points", xytext=(dx, 6 if y > 1 else -11), ha="center", fontsize=6.5, color="#B5442B")
    ax.set_ylim(0.6, 1.42)
    ax.set_xticks(xs)
    ax.set_xticklabels([c[2:] for c in N.CODES], fontsize=6)
    ax.set_xlabel("Node (OZ01 to OZ36)", fontsize=8)
    ax.set_ylabel("Span, afternoons of 6 April to 31 May 2028", fontsize=8)
    ax.text(35.4, 1.153, "1.15", fontsize=6.5, color="#4A6F4A", va="bottom", ha="right")
    ax.text(35.4, 0.847, "0.85", fontsize=6.5, color="#4A6F4A", va="top", ha="right")
    ax.set_title("Eight nodes outside the band: five read low, three read high", fontsize=9, loc="left")
    ax.tick_params(axis="y", labelsize=7)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf


def note(path, G):
    body, h1, h2, small, cell = docs._styles()
    low = [c for c in sorted(G["pull"]) if G["pull"][c] == "low"]
    high = [c for c in sorted(G["pull"]) if G["pull"][c] == "high"]
    s = [Paragraph("Eight nodes to the bench at the June round", h1),
         Paragraph("To: Adán Ruano (%s). From: %s, network coordinator. 1 June 2028. Round of 12 June 2028." %
                   (P.CONTRACTOR, P.COORDINATOR[0]), small), Spacer(1, 4),
         Paragraph("Please take %s down for the bench: their span over the eight weeks to 31 May is outside 0.85 to 1.15. "
                   "%s read low and %s read high. The other 28 nodes stay up and get the inlet cleaning." %
                   (", ".join(sorted(G["pull"])), ", ".join(low), ", ".join(high)), body),
         Paragraph("No node sits beside an analyser between rounds, so each span is read against the regional network's "
                   "four analysers, on the afternoon hours (12:00 to 18:00) when the comarca shares one ozone. At night the "
                   "plain loses its ozone under the surface inversion while the hill villages' nodes stand above it, so over "
                   "all hours a healthy hill node reads low and a hill node drifted high reads healthy: read that way the "
                   "list would hold %d nodes and miss OZ33 and OZ34." % len(G["allh_pull"]), body)]
    rows = [["Node", "Municipality", "Span", "Reads"]]
    for c in sorted(G["pull"]):
        rows.append([c, G["town"][c], "%.2f" % G["span"][c], G["pull"][c]])
    s.append(docs._grid(rows, [18 * mm, 50 * mm, 18 * mm, 18 * mm], cell))
    s.append(Spacer(1, 6))
    s.append(Image(chart(G), width=170 * mm, height=78 * mm))
    s.append(Paragraph("Spans from the node export and the regional network's provisional release to 31 May 2028; the "
                       "node's own accepted readings only, each hour once.", small))
    d = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm, bottomMargin=18 * mm,
                          title="June 2028 round: pull list", author=P.CENTRE, creator=P.CENTRE, subject="Pull list", invariant=1)
    d.build(s, onFirstPage=docs._footer("%s - June 2028 round - pull list" % P.CENTRE_SHORT),
            onLaterPages=docs._footer("%s - June 2028 round - pull list" % P.CENTRE_SHORT))
    postprocess.scrub(path, P.CENTRE, "2028-06-01")
