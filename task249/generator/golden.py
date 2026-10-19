"""The golden deliverables: the media kit's edition figures workbook and the measurement note for advertisers."""
import io
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import Image, Paragraph, Spacer
import docs as D
import params as P
import postprocess

NAMES = {e["code"]: e["name"] for e in P.EDITIONS}
HFILL = PatternFill("solid", fgColor="DDE3EA")
NOTEFILL = PatternFill("solid", fgColor="FBE3D6")


def workbook(path, G):
    res = G["res"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Digital audience"
    ws.append(["2029 media kit: digital audience by edition, October to December 2028"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Reported users: the analytics platform's distinct identifiers, average of the three months. Browsers: "
               "estimated unique browsers (audience policy, section 2). Note: reported above browsers by more than 25 per cent."])
    ws.append([])
    ws.append(["Edition", "Name", "Reported users", "Estimated browsers", "Reported above browsers", "Measurement note"])
    for c in ws[4]:
        c.font = Font(bold=True); c.fill = HFILL; c.alignment = Alignment(wrap_text=True, vertical="top")
    for code in P.CODES:
        r = res.loc[code]
        ws.append([code, NAMES[code], G["reported"][code], int(round(r["browsers"], -1)), round(float(r["golden"]) / 100, 3),
                   "Yes" if r["note"] else "No"])
        if r["note"]:
            for c in ws[ws.max_row]:
                c.fill = NOTEFILL
    for row in ws.iter_rows(min_row=5, max_row=ws.max_row):
        row[2].number_format = "#,##0"; row[3].number_format = "#,##0"; row[4].number_format = "0%"
        row[5].alignment = Alignment(horizontal="center")
    ws.append([])
    ws.append(["Editions with the note", G["n_noted"]])
    ws.cell(ws.max_row, 1).font = Font(bold=True)
    for i, w in enumerate([9, 18, 15, 18, 15, 12], 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[4].height = 30
    ws.freeze_panes = "C5"

    w2 = wb.create_sheet("Sold copies")
    w2.append(["Sold copies per publication day, fourth quarter 2028 (IVW basis; audience policy, section 5)"])
    w2["A1"].font = Font(bold=True, size=12)
    w2.append([])
    w2.append(["Edition", "Name", "Sold copies per publication day"])
    for c in w2[3]:
        c.font = Font(bold=True); c.fill = HFILL
    for code in P.CODES:
        w2.append([code, NAMES[code], G["copies"][code]])
        w2.cell(w2.max_row, 3).number_format = "#,##0"
    w2.column_dimensions["A"].width = 9; w2.column_dimensions["B"].width = 18; w2.column_dimensions["C"].width = 30
    w2.freeze_panes = "C4"

    w3 = wb.create_sheet("Newsletter")
    w3.append(["Newsletter subscribers at the end of 31 December 2028 (Berlin time; audience policy, section 6)"])
    w3["A1"].font = Font(bold=True, size=12)
    w3.append([])
    w3.append(["Edition", "Name", "Subscribers"])
    for c in w3[3]:
        c.font = Font(bold=True); c.fill = HFILL
    for code in P.CODES:
        w3.append([code, NAMES[code], G["newsletter"][code]])
        w3.cell(w3.max_row, 3).number_format = "#,##0"
    w3.append(["", "Contacts in two groups count in both.", None])
    w3.column_dimensions["A"].width = 9; w3.column_dimensions["B"].width = 34; w3.column_dimensions["C"].width = 14
    w3.freeze_panes = "C4"

    w4 = wb.create_sheet("Notes")
    for line in [
        "Prepared by audience data for the 2029 media kit, 15 January 2029; figures certified before the kit goes to advertisers on 1 February.",
        "Digital: sessions of October to December 2028 (Berlin months) without automated traffic, the newsroom's addresses and the export's re-sent rows; Hollerfeld's HKR and HOL joined.",
        "Browsers on WebKit (every iPhone and iPad browser, Safari on the Mac) are estimated: the seven-day rule replayed on other browsers' histories within edition, month and device class gives the identifiers a browser carries; print subscribers' browsers are counted from the sign-in register.",
        "Sold copies: subscriptions (print and e-paper, once each) and single copies sold, over each edition's publication days; Rhineland-Palatinate's editions did not appear on 1 November. "
        "%s subscriptions show a start between November and mid-December though their numbers were issued long before, so those dates are not their first days of delivery; they are counted from 1 October." % "{:,}".format(G["moved_subs"]),
        "Newsletter: confirmed subscribers in each edition's group at midnight on 31 December, from the platform's export taken back through its activity log and the preference centre's log; "
        "the editions added through the new year's mailing's one-click links (%s) are taken off, those added through the links before the year's end stay." % "{:,}".format(G["link_adds_after"]),
    ]:
        w4.append([line])
        w4.cell(w4.max_row, 1).alignment = Alignment(wrap_text=True, vertical="top")
    w4.column_dimensions["A"].width = 120
    wb.save(path)
    postprocess.scrub(path, P.ORG, "2029-01-16T17:45:00")
    postprocess.finish_office(path, "2029-01-15T09:10:00Z", "2029-01-16T17:45:00Z", P.ORG)


def _chart(G):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams["svg.hashsalt"] = "task249"
    res = G["res"]
    order = sorted(P.CODES, key=lambda c: -res.loc[c, "golden"])
    fig, ax = plt.subplots(figsize=(7.2, 3.9), dpi=150)
    x = np.arange(len(order))
    rep = np.array([G["reported"][c] for c in order]) / 1000
    est = np.array([res.loc[c, "browsers"] for c in order]) / 1000
    ax.bar(x - 0.2, rep, 0.4, color="#9AA7B8", label="Reported users")
    ax.bar(x + 0.2, est, 0.4, color=["#C0504D" if res.loc[c, "note"] else "#4F81BD" for c in order], label="Estimated browsers")
    ax.scatter(x - 0.2, est * 1.25, marker="_", s=260, linewidths=2.2, color="#222222", zorder=3,
               label="Estimated browsers plus 25 per cent")
    ax.set_xticks(x)
    ax.set_xticklabels(["%s%s" % (c, " *" if res.loc[c, "note"] else "") for c in order], fontsize=8)
    ax.set_ylabel("Thousands, monthly average Oct to Dec 2028", fontsize=8)
    ax.tick_params(axis="y", labelsize=8)
    ax.set_title("Reported users above the 25 per cent mark carry the note (*)", fontsize=9.5)
    ax.legend(fontsize=7.5, frameon=False, loc="upper right")
    ax.spines["top"].set_visible(False); ax.spines["right"].set_visible(False)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    buf.seek(0)
    return buf


def note(path, G):
    body, h1, h2, small, cell = D._styles()
    doc = D._doc(path, "Measurement note, 2029 media kit", P.PEOPLE["head"], "Which editions carry the note")
    noted = [c for c in P.CODES if G["res"].loc[c, "note"]]
    s = [Paragraph("Measurement note in the 2029 media kit: %d of 12 editions" % len(noted), h1),
         Paragraph("%s, audience data, for advertisers and the sales team. 16 January 2029." % P.PEOPLE["head"], small),
         Spacer(1, 4),
         Paragraph("The editions %s carry the note <i>Reported users include browsers counted more than once; see the "
                   "methods page</i> beside their digital figure for October to December 2028. Their reported users "
                   "exceed the browsers that read them by more than a quarter. %s print their figures without it."
                   % (", ".join(NAMES[c] for c in noted[:-1]) + " and " + NAMES[noted[-1]],
                      ", ".join(NAMES[c] for c in G["kept"][:-1]) + " and " + NAMES[G["kept"][-1]]), body),
         Image(_chart(G), width=170 * mm, height=92 * mm),
         Paragraph("Why reported users run above browsers", h2),
         Paragraph("Our analytics tag recognises a browser by an identifier stored in a cookie. Safari on the Mac and "
                   "every browser on an iPhone or iPad delete that cookie after seven days without a visit, so a reader "
                   "who comes back after a week away is counted again. The overcount is largest where many readers use "
                   "Apple devices and come by every week or two.", body),
         Paragraph("Methods", h2),
         Paragraph("For each edition, month and device class we replayed the seven-day rule on the visit histories of "
                   "readers whose browsers keep the cookie, and divided the Apple browsers' identifiers by the number of "
                   "identifiers a browser would carry. Print subscribers, who sign in with their subscriber number and "
                   "read us mostly on Apple devices, are counted directly from our sign-in records. Registered readers "
                   "are not set apart: on Apple devices the free-article meter is deleted with the cookie, so fewer of "
                   "those readers meet the registration wall, and the signed-in group there is not like the signed-in "
                   "group elsewhere.", body)]
    doc.build(s, onFirstPage=D._footer("%s, audience data." % P.ORG), onLaterPages=D._footer("%s, audience data." % P.ORG))
    postprocess.scrub(path, P.ORG, "2029-01-16T17:50:00")
