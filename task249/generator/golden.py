"""task249's goldens: the integrity desk's verification bands workbook and the note to client services."""
import io
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
import params as P
import postprocess

FMT_SHORT = {"Day-one campus drive": "Day-one drive", "First-company campus drive": "First-company drive",
             "Later campus drive": "Later drive", "Assessment centre": "Assessment centre"}


def workbook(path, G):
    wb = Workbook()
    ws = wb.active
    ws.title = "2029 bands"
    ws["A1"] = "MAT-V bands for the 2029 campus season: genuine referrals projected per client account"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Projected share of each account's genuine shortlisted candidates that MAL-IS-04 s.3.2 would refer, "
                "on the account's 2029 plan and its 2028 applicant pool. Cap 15 per cent (s.3.3).")
    ws.merge_cells("A2:K2")
    hdr = ["Code", "Client", "Selection format", "2028 applicants (pool)", "2029 expected applicants", "2029 shortlist",
           "Share shortlisted", "Days MAT-R to MAT-V (mean)", "Retest gain at that interval (logit)",
           "Projected genuine referral share", "2029 MAT-V"]
    thin = Side(style="thin", color="B7BDC6")
    for j, h in enumerate(hdr, 1):
        c = ws.cell(row=4, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="E6EAF0")
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=thin)
    r = 5
    for a in G["accounts"]:
        vals = [a["code"], a["client"], FMT_SHORT[a["fmt"]], a["pool_n"], a["expected"], a["shortlist"], a["depth"],
                round(a["mean_gap"]), a["gain_at"], a["gold"], "Extended (24 items)" if a["flag"] else "Standard (12 items)"]
        for j, v in enumerate(vals, 1):
            c = ws.cell(row=r, column=j, value=v)
            if j in (4, 5, 6):
                c.number_format = "#,##0"
            if j in (7, 10):
                c.number_format = "0.0%"
            if j == 9:
                c.number_format = "0.00"
        if a["flag"]:
            for j in range(1, 12):
                ws.cell(row=r, column=j).fill = PatternFill("solid", fgColor="FBE9E7")
        r += 1
    ws.cell(row=r + 1, column=1, value="Accounts moving to MAT-V Extended").font = Font(bold=True)
    ws.cell(row=r + 1, column=4, value=G["n_flag"])
    widths = [7, 30, 19, 13, 13, 11, 10, 13, 13, 14, 19]
    for j, wdt in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(j)].width = wdt
    ws.row_dimensions[4].height = 58
    ws.freeze_panes = "C5"
    ws.auto_filter.ref = "A4:K%d" % (r - 1)
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.print_title_rows = "4:4"
    ws.print_area = "A1:K%d" % (r + 1)
    # the asks
    w2 = wb.create_sheet("Integrity 2028")
    w2["A1"] = "2028 season: item exposure, impersonations and interrupted bookings"
    w2["A1"].font = Font(bold=True, size=12)
    row = 3
    w2.cell(row=row, column=1, value="MAT-R exposure by test week (IST, Monday to Sunday); ceiling 12 per cent (MAL-IS-04 s.4)").font = Font(bold=True)
    row += 1
    for j, h in enumerate(["Test week beginning", "Candidates", "Items over 12 per cent", "Highest exposure", "Item"], 1):
        w2.cell(row=row, column=j, value=h).font = Font(bold=True)
    for k, e in enumerate(G["exposure"]):
        row += 1
        vals = [["3 July", "10 July", "17 July", "24 July"][k], e["candidates"], e["over"], round(e["top"], 3), e["top_item"]]
        for j, v in enumerate(vals, 1):
            c = w2.cell(row=row, column=j, value=v)
            if j == 4:
                c.number_format = "0.0%"
            if j == 2:
                c.number_format = "#,##0"
    row += 1
    w2.cell(row=row, column=1, value="Items to rest for 2029 (over 12 per cent in any test week)")
    w2.cell(row=row, column=3, value=G["rested"]).font = Font(bold=True)
    row += 2
    w2.cell(row=row, column=1, value="Impersonations standing confirmed by college tier (each sitting's latest decision, "
                                     "appeal cases included; one sitting a candidate)").font = Font(bold=True)
    row += 1
    for j, h in enumerate(["Tier", "Sittings confirmed", "Candidates shortlisted", "Per thousand shortlisted"], 1):
        w2.cell(row=row, column=j, value=h).font = Font(bold=True)
    for t in G["impersonation"]:
        row += 1
        for j, v in enumerate([t["tier"], t["confirmed"], t["shortlisted"], round(t["per_thousand"], 1)], 1):
            c = w2.cell(row=row, column=j, value=v)
            if j == 3:
                c.number_format = "#,##0"
            if j == 4:
                c.number_format = "0.0"
    row += 2
    w2.cell(row=row, column=1, value="Interrupted bookings by the device the booking started on").font = Font(bold=True)
    row += 1
    for j, h in enumerate(["Device", "Bookings started", "Interrupted", "Share interrupted", "Finished on another device"], 1):
        w2.cell(row=row, column=j, value=h).font = Font(bold=True)
    for d in G["interrupted"]:
        row += 1
        for j, v in enumerate([d["device"], d["bookings"], d["interrupted"], round(d["share"] / 100, 4), d["moved"]], 1):
            c = w2.cell(row=row, column=j, value=v)
            if j == 4:
                c.number_format = "0.00%"
            if j in (2, 3):
                c.number_format = "#,##0"
    for j, wdt in enumerate([34, 16, 22, 18, 24], 1):
        w2.column_dimensions[get_column_letter(j)].width = wdt
    notes = wb.create_sheet("Notes")
    lines = [
        "Prepared by the integrity desk, 14 May 2029, for the 2029 bands (MAL-IS-04 s.3.3).",
        "Pool: candidates whose 2028 MAT-R result was shared with the account (PGL folded into NVK), at their completed "
        "MAT-R estimate; the 14 August 2028 re-send and withdrawals do not change who applied.",
        "Projection: 2029 applicants drawn from the pool's ability distribution (mean of the estimates; spread with the "
        "mean squared standard error taken out), MAT-R and MAT-V errors from Table 4.3 of the technical manual read at "
        "each applicant's ability (the error reported with a 2028 result is the error at its estimate), the "
        "retest gain fitted to the equivalence study's pairs by interval, the shortlist the top of the account's applicants "
        "on MAT-R, the referral rule of s.3.2; 1.2 million simulated applicants per account.",
        "Intervals: day-one and first-company drives sit MAT-V two days after MAT-R; later drives and assessment centres "
        "on the plan's selection days against the July 2029 test weeks.",
    ]
    for k, t in enumerate(lines, 1):
        notes.cell(row=k, column=1, value=t).alignment = Alignment(wrap_text=True, vertical="top")
    notes.column_dimensions["A"].width = 120
    wb.save(path)
    postprocess.scrub(path, P.FIRM, "2029-05-14T15:30:00")
    postprocess.finish_office(path, "2029-05-13T09:00:00Z", "2029-05-14T15:30:00Z", P.FIRM)


def _chart(G):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    acc = sorted(G["accounts"], key=lambda a: a["gold"])
    fig, ax = plt.subplots(figsize=(7.2, 5.4), dpi=150)
    y = np.arange(len(acc))
    col = ["#B5442F" if a["flag"] else "#5A7896" for a in acc]
    ax.barh(y, [100 * a["gold"] for a in acc], color=col, height=0.7)
    ax.scatter([100 * a["study_rate"] for a in acc], y, marker="|", color="#222222", s=60, zorder=3,
               label="equivalence study's rate at the account's interval")
    ax.axvline(100 * P.CAP, color="#222222", lw=1, ls="--")
    ax.text(100 * P.CAP + 0.4, len(acc) - 0.6, "15 per cent cap", fontsize=7.5)
    ax.set_yticks(y)
    ax.set_yticklabels([a["code"] for a in acc], fontsize=7)
    ax.set_xlabel("Projected share of genuine shortlisted candidates referred, 2029 (per cent)", fontsize=8)
    ax.set_title("15 accounts' checks would refer more than the cap", fontsize=10)
    ax.tick_params(axis="x", labelsize=7.5)
    ax.legend(fontsize=7, loc="lower right", frameon=False)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def note(path, G):
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.3, leading=12.8, spaceAfter=5)
    h1 = ParagraphStyle("h", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.5, leading=15.5, spaceAfter=3)
    small = ParagraphStyle("s", parent=body, fontSize=7.8, leading=10, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("c", fontName="Helvetica", fontSize=7.8, leading=9.4)
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=19 * mm, rightMargin=19 * mm, topMargin=16 * mm,
                            bottomMargin=16 * mm, title="2029 verification bands", author=P.PEOPLE["head"],
                            creator=P.PEOPLE["head"], subject="MAT-V bands for client accounts", invariant=1)
    flag = [a for a in G["accounts"] if a["flag"]]
    keep = [a for a in G["accounts"] if not a["flag"]]
    s = [Paragraph("15 client accounts move to MAT-V Extended for the 2029 season", h1),
         Paragraph("To: %s, client services. From: %s, Head of Assessment Integrity. 14 May 2029. Ref: MAL-IS-04 s.3.3."
                   % (P.PEOPLE["client"], P.PEOPLE["head"]), small), Spacer(1, 3)]
    s.append(Paragraph(
        "On their 2029 plans, the verification check would refer more than 15 per cent of the genuine candidates at "
        "%s; they sit MAT-V Extended (24 items) at their selection days. The other %d accounts stay on the standard "
        "MAT-V." % (", ".join(a["code"] for a in flag), len(keep)), body))
    s.append(Paragraph(
        "The equivalence study's referral rates (%.1f per cent within three days of MAT-R, %.1f per cent at six weeks "
        "or more) are not what these accounts will see: its volunteers sat both tests without being shortlisted. An "
        "account shortlists on MAT-R, so the candidates it invites are those whose online estimate ran high, the more "
        "so the smaller the share it shortlists and where MAT-R's standard error widens above +1 logit; their MAT-V falls short of "
        "MAT-R by that margin and the rule reads the shortfall. MAT-V sat two days after MAT-R runs about 0.3 logit "
        "higher, which keeps the mid-sized day-one accounts (NVK, UJB, OJS) under the cap, though not the day-one "
        "accounts that shortlist most selectively (KSP, VRD, ABH)." % (100 * G["study_short"], 100 * G["study_long"]), body))
    s.append(Image(_chart(G), width=150 * mm, height=112 * mm))
    s.append(Paragraph("Source: integrity desk projection, 14 May 2029 (workbook verification_bands_2029.xlsx). "
                       "Bars: projected share; ticks: the study's own rate at the account's interval.", small))
    s.append(Spacer(1, 3))
    s.append(Paragraph("NVK's pool includes the former Paisaghar Lending campuses (PGL until the merger of 2 September "
                       "2028). VRD moves from assessment centres to day-one campus drives in 2029, so its candidates sit "
                       "MAT-V two days after MAT-R.", small))
    doc.build(s)
    postprocess.scrub(path, P.PRODUCER, "2029-05-14T15:40:00")
