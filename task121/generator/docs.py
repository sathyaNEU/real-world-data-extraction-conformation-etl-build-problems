"""The pack's documents: short, functional, in the voices of the people who would write them."""
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
import writers as WR


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=13, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=body, fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=body, fontName="Helvetica-Bold", fontSize=10, leading=13, spaceBefore=6,
                        spaceAfter=3)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10.5, textColor=colors.HexColor("#4a4a4a"))
    return body, h1, h2, small


def _pdf(path, title, story, author, footer, when, producer):
    def on_page(c, d):
        c.saveState()
        c.setFont("Helvetica", 7.2)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(18 * mm, 11 * mm, footer)
        c.drawRightString(192 * mm, 11 * mm, f"{d.page}")
        c.restoreState()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=17 * mm,
                            bottomMargin=19 * mm, title=title, author=author, subject="", creator=producer,
                            invariant=1)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    WR.normalize_pdf(path, when, producer=producer)


def _tbl(rows, widths, head=True, size=8.5):
    t = Table(rows, colWidths=[w * mm for w in widths])
    st = [("FONT", (0, 0), (-1, -1), "Helvetica", size), ("VALIGN", (0, 0), (-1, -1), "TOP"),
          ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.HexColor("#9a9a9a")),
          ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
    if head:
        st.append(("FONT", (0, 0), (-1, 0), "Helvetica-Bold", size))
    t.setStyle(TableStyle(st))
    return t


def write_agreement(path):
    body, h1, h2, small = _styles()
    Pp = lambda t, s=body: Paragraph(t, s)
    st = [Pp("Clube Desportivo Monteralto  /  Ventania Merch, Lda.", small),
          Pp("Store partnership agreement 2026/27: extract", h1),
          Pp("Signed in Monteralto on 14 July 2026. Extract prepared for internal use by the Store's partnerships "
             "team: recitals, Schedule 2 (Shop tab) and Schedule 4 (invoicing). Schedules 1, 3 and 5 omitted.", small),
          Spacer(1, 4),
          Pp("Recitals", h2),
          Pp("A. The Club publishes the official members' app, Monteralto+, to its members."),
          Pp("B. In the 2025/26 season members took 10% off licensed kits on the Store's website by entering at "
             "checkout the code printed on their membership card: SOCIO followed by their seven-digit member number."),
          Pp("C. From the 2026/27 season the members' price is offered through the app and the website discount "
             "ends on 30 August 2026."),
          Pp("Schedule 2: Shop tab", h2),
          Pp("2.1 From 31 August 2026 the app carries a Shop tab with links to the Store's members' pages."),
          Pp("2.2 Each link opened from the Shop tab carries a members'-price token in the parameter <i>mpt</i>. The "
             "Club issues one token for each tap. A token is valid for 24 hours from issue."),
          Pp("2.3 The members' price applies to licensed Club kits in stock. Pre-order items and other merchandise "
             "are not listed in the Shop tab."),
          Pp("2.4 The Club does not pass members' names, contact details or app account data to the Store through "
             "the Shop tab."),
          Pp("2.5 The Store may refuse the members' price on a token that is expired or used from more than one "
             "device."),
          Pp("Schedule 4: Invoicing", h2),
          Pp("4.1 The Club invoices the Store monthly in arrears a fee of EUR 0.04 for each token issued in the month, "
             "plus VAT."),
          Pp("4.2 Each invoice is supported by a token report listing every token issued in the month, with the "
             "member number it was issued to and its issue time (Lisbon time)."),
          Pp("4.3 The first invoice covers 31 August 2026 only. Invoices are payable within 30 days."),
          Pp("4.4 Either party may query a token report within 60 days of the invoice date."),
          Spacer(1, 6),
          Pp("For the Club: Henrique Valadares, commercial director.   For the Store: Júlia Machado, head of product; "
             "Lia Neto, club partnerships.", small)]
    _pdf(path, "Store partnership agreement 2026/27 extract", st, "Lia Neto",
         "CD Monteralto / Ventania Merch  |  Partnership agreement 2026/27  |  Extract, internal",
         dt.datetime(2026, 7, 16, 11, 20), "Ventania Merch")


def write_psp_report(path, weekly):
    body, h1, h2, small = _styles()
    Pp = lambda t, s=body: Paragraph(t, s)
    rows = [["Week", "Card payment attempts", "Frictionless (Y, A, I)", "Challenged (C, D)",
             "Not authenticated (N, U)"]]
    for w in weekly:
        rows.append([w["label"], f"{w['attempts']:,}", f"{w['frictionless']:,}", f"{w['challenged']:,}",
                     f"{w['failed']:,}"])
    tot = {k: sum(w[k] for w in weekly) for k in ("attempts", "frictionless", "challenged", "failed")}
    rows.append(["Total", f"{tot['attempts']:,}", f"{tot['frictionless']:,}", f"{tot['challenged']:,}",
                 f"{tot['failed']:,}"])
    codes = [["Status", "Meaning"],
             ["Y", "Authenticated by the issuer without a challenge"],
             ["A", "Attempted: issuer or card not enrolled, authentication proof issued"],
             ["I", "Exemption requested by the merchant and accepted by the issuer, no authentication"],
             ["C", "Challenge: cardholder authenticated on a page shown by the issuer"],
             ["D", "Challenge, decoupled: cardholder approved the payment in the issuer's banking app"],
             ["N", "Not authenticated, or declined by the issuer"],
             ["U", "Authentication could not be performed"]]
    st = [Pp(f"{P.PSP}, Lda.  |  Merchant 448-21907 Ventania Merch", small),
          Pp("3-D Secure authentication: monthly merchant report", h1),
          Pp("Settlement weeks 36 to 39: 31 August to 27 September 2026. Card payments on loja.ventania.pt. "
             "Issued 29 September 2026.", small), Spacer(1, 4),
          Pp("Summary by week", h2), _tbl(rows, [36, 34, 36, 32, 36]), Spacer(1, 4),
          Pp("Weeks run Monday to Sunday, Lisbon time, by the time the authentication request was sent."),
          Pp("Status codes", h2), _tbl(codes, [18, 150]), Spacer(1, 6),
          Pp("Exemptions are requested by the merchant and decided by the issuer. An issuer may stop accepting an "
             "exemption type at any time; we publish issuer notices in the merchant portal when we receive them.",
             small),
          Pp("Questions: merchant support, suporte@tagus-payments.pt", small)]
    _pdf(path, "3-D Secure monthly merchant report, weeks 36 to 39 2026", st, P.PSP,
         f"{P.PSP}  |  Merchant report  |  Confidential to the merchant",
         dt.datetime(2026, 9, 29, 7, 15), "Tagus Payments")


def write_carrier_notice(path):
    body, h1, h2, small = _styles()
    Pp = lambda t, s=body: Paragraph(t, s)
    st = [Pp("Lusolog Expresso  |  Business customers", small),
          Pp("Full postcodes on parcel labels from 1 September 2026", h1),
          Pp("Notice to contract customers, 15 July 2026", small), Spacer(1, 4),
          Pp("From 1 September 2026 our sorting hubs read the full seven-digit postcode (CP7, for example 4710-357) "
             "from every parcel label. Labels that carry only the four-digit postcode area will be held at the first "
             "hub and returned to the sender's collection point within two working days."),
          Pp("What changes", h2),
          Pp("1. Labels must show the postcode as nnnn-nnn. The locality line must match the postcode's locality."),
          Pp("2. Parcels already in the network on 1 September are delivered on the old rules."),
          Pp("3. Our label API rejects a request without a valid CP7 from 1 September with error 4221."),
          Pp("What you can do now", h2),
          Pp("Check the postcodes your customers have saved. Our address validation service returns the CP7 and "
             "street for a typed address and is free for contract customers until 31 December 2026."),
          Pp("Account managers will contact customers with more than 2,000 parcels a month.", small)]
    _pdf(path, "Full postcodes on parcel labels from 1 September 2026", st, "Lusolog Expresso",
         "Lusolog Expresso  |  Notice to business customers  |  July 2026", dt.datetime(2026, 7, 15, 9, 0),
         "Lusolog Expresso")


def write_shortlist(path):
    import docx
    from docx.shared import Pt, Cm
    d = docx.Document()
    sty = d.styles["Normal"]
    sty.font.name = "Calibri"
    sty.font.size = Pt(10.5)
    d.add_heading("Q4 engineering sprint: shortlist", level=1)
    p = d.add_paragraph()
    p.add_run("Owner: ").bold = True
    p.add_run("Júlia Machado, head of product.  ")
    p.add_run("Circulated: ").bold = True
    p.add_run("28 September 2026, to the conversion incident review.")
    d.add_paragraph("We have one engineering sprint in Q4: both checkout squads, 12 October to 6 November. Five fixes "
                    "came out of the incident channel and each of them needs the whole sprint, so one goes ahead and "
                    "the other four wait for Q1 planning.")
    d.add_paragraph("The sprint goes to the fix whose cause is costing us the most orders now: the latest complete "
                    "week, each cause's customers against what those same customers converted at over the four weeks "
                    "before the fall, and a lost order valued at what those customers' orders averaged then.")
    rows = [("Fix", "Owner", "Who it is for", "What it is"),
            ("1. Inline postcode lookup at the address step", "Duarte Cunha",
             "Accounts whose saved address the new check rejects",
             "Type-ahead on the full postcode that fills in the street, so the address passes the check first time."),
            ("2. Club landing page", "Lia Neto", "Fans who are new to the store and land from the club app",
             "A members' page that takes fans to kits in stock in their size before they reach the basket."),
            ("3. Card SDK upgrade with in-page 3-D Secure", "Cristiano Soares",
             "Saved-card payments that Bankora and Finvo began challenging",
             "Tagus SDK 5, with the challenge shown inside our payment page instead of a redirect."),
            ("4. One-time-code sign-in at checkout", "Jaime Jesus",
             "Customers with an account who check out without signing in",
             "A six-digit code by text or email at the contact step, no password. Parked in April when password "
             "resets were flat."),
            ("5. Split dispatch", "Raquel Pires", "Baskets that mix pre-order and in-stock lines",
             "In-stock lines ship now and pre-order lines on release, on one payment.")]
    t = d.add_table(rows=len(rows), cols=4)
    t.style = "Table Grid"
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            cell = t.cell(i, j)
            cell.text = v
            for para in cell.paragraphs:
                for run in para.runs:
                    run.font.size = Pt(9)
                    run.bold = i == 0
    for j, w in enumerate((4.2, 2.6, 4.4, 6.2)):
        for c in t.columns[j].cells:
            c.width = Cm(w)
    d.add_paragraph("")
    d.add_paragraph("Owners: one paragraph each in the review folder by Wednesday if you want to add anything. The "
                    "call is made at the review on Friday 2 October.")
    f = d.add_paragraph("Internal. Product team and incident review only.")
    f.runs[0].font.size = Pt(8)
    cp = d.core_properties
    cp.author = "Júlia Machado"
    cp.last_modified_by = "Júlia Machado"
    cp.title = "Q4 engineering sprint: shortlist"
    cp.revision = 4
    cp.comments = ""
    d.save(path)
    WR.normalize_ooxml(path, "Júlia Machado", dt.datetime(2026, 9, 25, 16, 40), dt.datetime(2026, 9, 28, 8, 52),
                       app="Microsoft Office Word")


FIELD_REFERENCE = """# Warehouse field reference: checkout and trading extracts

Maintained by Noah Coelho (analytics engineering). Last edited 28 September 2026. Covers the extracts in the
conversion review folder; it describes fields and how each export is cut, not how to analyse them.

## Trading metrics

- Conversion is orders over basket sessions. A basket session is a storefront session in which at least one item
  was added to the basket.
- Sessions that the edge service flags as automated are excluded from every conversion figure, from the count of
  basket sessions and from orders.
- Weeks run Monday 00:00 to Sunday 23:59, Lisbon time.

## basket_sessions (parquet)

| field | meaning |
|---|---|
| session_id | storefront session key, unique |
| started_at | session start, Lisbon local time |
| device | device class from the user agent: mobile, desktop, tablet |
| traffic_source | channel of the landing page, from the referrer and the query string |
| landing_url | first page of the session, with its query string |
| signed_in | true when an account was signed in during the session |
| account_id | the account signed in during the session; empty otherwise |
| new_visitor | true when the session carried no store cookie from an earlier visit |
| furthest_step | last checkout step reached: basket, contact, address, delivery, payment, confirmation |
| basket_skus | SKUs in the basket at the furthest step, semicolon separated |
| order_id | order placed in the session; an order is always placed inside its basket session |
| address_fp | fingerprint of the delivery address submitted at the address step (normalised street, number and postcode); empty if no address was submitted |

## edge_bot_verdicts

One row per session the edge service scored as automated, with the rule that fired. Covers every storefront
session, not only basket sessions.

## Club token reports (cdm_token_billing_YYYY-MM)

The club's monthly token reports as received with its invoices, unedited. member_no is the club member number.

## loyalty_profiles

One row per account enrolled in the loyalty scheme. club_member_no is the member number the customer entered on
the profile.

## promo_redemptions

One row per promotion code redeemed at checkout in the 2025/26 season. promo_code is the code as entered,
upper-cased; account_id is empty for a guest checkout.

## address_book_history

Every change to a saved delivery address since the address was created. is_default marks the address used to
prefill checkout. address_fp is computed as in basket_sessions.

## checkout_flags_export

Export of the feature-flag service for one flag. assignments is the cohort each account is in at extract;
assignment_moves lists accounts moved between cohorts, with the time of the move.

## saved_cards and saved_card_events

saved_cards lists every saved card with its issuer, BIN and fingerprint; saved_card_events lists changes to saved
cards.

## tagus_3ds_log

Authentication messages exchanged with the payment provider for card payments. three_ds_status is the status
returned by the provider; card_fp is the provider's card fingerprint, the same fingerprint saved_cards carries.

## finance_order_export

Daily export from the finance system. order_id is the storefront order; order_total_eur is in euros.

## catalogue_status_history

Status of each SKU (pre_order, in_stock) with the time it took effect.
"""


THREAD = """#inc-0914-checkout-conversion  (channel export, 30 Sep 2026 10:05 WEST)

[Mon 28 Sep 09:04] Júlia Machado: Shortlist for the Q4 sprint is in the review folder. Five fixes, one sprint. I want the call settled at Friday's review.
[Mon 28 Sep 09:11] Duarte Cunha: The address check is still what is hurting us. Address step exits jumped the week it went live and they have not come back down. The postcode lookup fixes it at the root.
[Mon 28 Sep 09:15] Raquel Pires: Carrier rule is not optional though, the check stays whatever we pick.
[Mon 28 Sep 09:16] Duarte Cunha: Nobody is asking to switch it off. The lookup makes it pass first time.
[Mon 28 Sep 09:30] Lia Neto: The Shop tab is the big new thing this month and those fans convert far below everyone else. Most of them have never bought from us before. A landing page that gets them to kits in their size is the obvious fix.
[Mon 28 Sep 09:41] Luciana Castro: Partner traffic always converts lower. We book it as new-fan dilution in every close-out and it has never cost us an order. I'll take the club app to the review on the same basis.
[Mon 28 Sep 10:02] Cristiano Soares: Bankora and Finvo both wrote to us: they stopped accepting our card-on-file exemption in the first week of September. Challenges are up, approvals are flat. The SDK upgrade puts the challenge inside our page and it's what Tagus recommends.
[Mon 28 Sep 10:20] Jaime Jesus: For the record, the one-time-code sign-in is still parked. Password resets have been flat all year and I don't see what reopening it buys us this quarter.
[Mon 28 Sep 10:24] Raquel Pires: Mixed pre-order baskets convert at about half the rest and they're a steady slice of the store. Split dispatch has been on the list for a year.
[Mon 28 Sep 11:02] Noah Coelho: Extracts for the review are in the warehouse folder, cut this morning, field reference updated. Shout if something is missing.
[Tue 29 Sep 08:47] Noah Coelho: Edge team's verdict file landed overnight, added it to the folder. Session export unchanged.
[Tue 29 Sep 09:30] Júlia Machado: Thanks. I'll read the numbers myself, please don't post rankings in here.
[Wed 30 Sep 09:58] Duarte Cunha: Checkout squad will want the cohort view of the address check before Friday.
[Wed 30 Sep 10:01] Júlia Machado: Noted.

-- internal, do not forward outside Ventania --
"""


def write_text(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


# --------------------------------------------------------------------------- workbooks

def _wb():
    import openpyxl
    wb = openpyxl.Workbook()
    return wb


def _font(bold=False, size=10, color="000000", italic=False):
    from openpyxl.styles import Font
    return Font(name="Calibri", size=size, bold=bold, color=color, italic=italic)


def _save(wb, path, author, created, modified):
    wb.properties.creator = author
    wb.properties.lastModifiedBy = author
    wb.properties.created = created
    wb.properties.modified = modified
    wb.save(path)
    WR.normalize_ooxml(path, author, created, modified, app="Microsoft Excel")


def _widths(ws, widths):
    from openpyxl.utils import get_column_letter
    for i, w in enumerate(widths):
        ws.column_dimensions[get_column_letter(i + 1)].width = w


def write_dashboard(path, weekly, by_source, steps):
    wb = _wb()
    ws = wb.active
    ws.title = "Weekly"
    ws["A1"] = "Ventania Merch: weekly trading dashboard"
    ws["A1"].font = _font(True, 13)
    ws["A2"] = "Refreshed Mon 28 Sep 2026 07:30. Owner Noah Coelho. Distribution: product, growth, checkout squads."
    ws["A3"] = ("Trading view of conversion and checkout step completion as they were each week. It reports what "
                "happened; it does not size causes.")
    ws["A3"].font = _font(italic=True, size=9, color="555555")
    hdr = ["Week starting", "Basket sessions", "Orders", "Conversion %"]
    ws.append([])
    ws.append(hdr)
    for c in ws[5]:
        c.font = _font(True)
    for r in weekly:
        ws.append([r["week"], r["sessions"], r["orders"], r["conversion"]])
    for row in ws.iter_rows(min_row=6, max_row=5 + len(weekly)):
        row[3].number_format = "0.00"
    _widths(ws, [16, 16, 10, 14])
    w2 = wb.create_sheet("By source")
    srcs = sorted({k for r in by_source for k in r if k != "week"})
    w2.append(["Conversion % by traffic source"])
    w2["A1"].font = _font(True, 11)
    w2.append(["Week starting"] + srcs)
    for c in w2[2]:
        c.font = _font(True)
    for r in by_source:
        w2.append([r["week"]] + [r.get(s) for s in srcs])
    for row in w2.iter_rows(min_row=3, max_row=2 + len(by_source)):
        for c in row[1:]:
            c.number_format = "0.00"
    _widths(w2, [16] + [14] * len(srcs))
    w3 = wb.create_sheet("Checkout steps")
    w3.append(["Basket sessions reaching each checkout step"])
    w3["A1"].font = _font(True, 11)
    w3.append(["Week starting", "Basket", "Contact", "Address", "Delivery", "Payment", "Confirmation"])
    for c in w3[2]:
        c.font = _font(True)
    for r in steps:
        w3.append([r["week"]] + r["reach"])
    w3.append([])
    w3.append(["Step completion %: share of sessions reaching a step that reached the next one"])
    w3.cell(row=w3.max_row, column=1).font = _font(True, 11)
    w3.append(["Week starting", "Basket", "Contact", "Address", "Delivery", "Payment"])
    for c in w3[w3.max_row]:
        c.font = _font(True)
    for r in steps:
        w3.append([r["week"]] + r["completion"])
        for c in w3[w3.max_row][1:]:
            c.number_format = "0.0"
    _widths(w3, [16, 11, 11, 11, 11, 11, 13])
    _save(wb, path, "Noah Coelho", dt.datetime(2026, 2, 2, 9, 0), dt.datetime(2026, 9, 28, 6, 30))


def write_closeout(path, key, cfg, df, book):
    wb = _wb()
    ws = wb.active
    ws.title = "Close-out"
    end = cfg["start"] + dt.timedelta(days=7 * cfg["weeks"] - 1)
    lines = [
        ("Partner campaign close-out", None),
        ("Partner", cfg["partner"]),
        ("Campaign weeks", f"{cfg['start'].isoformat()} to {end.isoformat()}"),
        ("Pre-campaign weeks", f"{cfg['pre_start'].isoformat()} to {(cfg['start'] - dt.timedelta(days=1)).isoformat()}"),
        ("Partner basket sessions", book["partner_sessions"]),
        ("Partner orders", book["partner_orders"]),
        ("Incremental orders (partner new visitors)", book["incremental"]),
        ("Orders lost to the campaign", 0),
        ("Closed by", "Luciana Castro, growth lead"),
    ]
    for k, v in lines:
        ws.append([k, v])
    ws["A1"].font = _font(True, 13)
    if key == "kaiju":
        ws.append([])
        ws.append(["Note added September 2026"])
        ws.cell(row=ws.max_row, column=1).font = _font(True)
        ws.append(["Partner traffic is new-fan dilution. A partner sends people who are new to us, they convert lower "
               "than our own customers, and that costs us no orders. Every close-out is booked on that basis and I "
               "will present the club app to the incident review the same way. (L.C.)"])
        ws.cell(row=ws.max_row, column=1).font = _font(italic=True, size=9)
    _widths(ws, [42, 34])
    w2 = wb.create_sheet("Weekly")
    w2.append(list(df.columns))
    for c in w2[1]:
        c.font = _font(True)
    for r in df.itertuples(index=False):
        w2.append(list(r))
    _widths(w2, [13, 10, 16, 15, 16, 8])
    closed = cfg["start"] + dt.timedelta(days=7 * cfg["weeks"] + 16)
    _save(wb, path, "Luciana Castro", dt.datetime(closed.year, closed.month, closed.day, 10, 0),
          dt.datetime(2026, 9, 28, 17, 45))


def write_release_log(path, recs, effects):
    import calib as C
    wb = _wb()
    ws = wb.active
    ws.title = "Releases"
    ws.append(["Release", "Title", "Flag", "Owner", "Rollout", "Follow-on window",
               "Measured effect on basket conversion (points)", "Notes"])
    for c in ws[1]:
        c.font = _font(True)
    for k, r in C.RELEASES.items():
        w0 = r["start"] + dt.timedelta(days=28)
        ws.append([k, r["title"], r["flag"], r["owner"],
                   "Twelve cohorts in four waves of three, a week apart, from " + w0.isoformat(),
                   f"{w0.isoformat()} to {(w0 + dt.timedelta(days=55)).isoformat()}",
                   round(effects[k]["cohort"], 3), "Measured by flag cohort; closed"])
    ws.append(["R-2026-09", "Full-postcode check at the address step", "checkout.address.full_postcode",
               "Duarte Cunha", "Twelve cohorts in three waves of four: 1, 3 and 8 September 2026",
               "2026-09-01 to 2026-10-26", None, "Measurement open"])
    _widths(ws, [11, 42, 30, 15, 52, 26, 22, 30])
    for k, df in recs.items():
        w = wb.create_sheet(f"{k} cohorts")
        w.append(list(df.columns))
        for c in w[1]:
            c.font = _font(True)
        for r in df.itertuples(index=False):
            w.append(list(r))
        _widths(w, [13, 8, 9, 16, 8])
    _save(wb, path, "Duarte Cunha", dt.datetime(2026, 1, 20, 9, 30), dt.datetime(2026, 9, 1, 9, 10))
