"""task122 generator: the documents in the slot review folder.

Each load-bearing rule is stated once, in the document that owns it: the lift definition, the
reproduction clause, the cell table and the slot share in the charter; the fresh-listing floor in
the commitment; the fee basis, the cover and the change clause in the buyer terms; the tariff rows and
their effective dates in the tariff register; the R2 replacement in the analytics release log; the
cell-by-cell planning rule and the app release gating in the capacity note. Checkout 3 is named once, in
the thread, and its effect shows only in the orders and payments from 21 September 2026. People hold views
in the thread and quote no figure. The pricing committee minutes carry no rule any ask needs.
"""
import json
from datetime import date, datetime

import numpy as np
import pandas as pd
from reportlab import rl_config

rl_config.invariant = 1   # fixed document id and dates, so two builds are byte-identical

from reportlab.lib import colors  # noqa: E402
from reportlab.lib.enums import TA_LEFT  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import params as P

F_CHARTER = "experimentation_charter_home_surfaces.pdf"
F_COMMIT = "fresh_listing_commitment_2026.docx"
F_REGISTER = "ranking_policy_register.json"
F_FIELDS = "carousel_logger_field_reference.md"
F_TERMS = "buyer_protection_terms_2026-09.pdf"
F_TARIFF = "kopersbescherming_tarieven.csv"
F_MINUTES = "pricing_committee_minutes_2026-10-06.docx"
F_RELEASES = "analytics_release_log.md"
F_CAPACITY = "slot_capacity_and_release_gating.md"
F_ICS = "app_release_calendar_2026-2027.ics"
F_FINANCE = "finance_buyer_protection_fee_income_2026Q3.xlsx"
F_THREAD = "planning_thread_carousel_slot.txt"
F_SEARCH = "search_ranking_tests_2026H1.xlsx"
F_SURVEY = "seller_survey_fresh_listings_2026Q2.csv"
F_ARCHIVE = "carousel_experiment_archive.xlsx"
F_INDEX = "extract_register_slot_review.md"

STYLE = ParagraphStyle("b", fontName="Helvetica", fontSize=9.6, leading=13.2, alignment=TA_LEFT, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=STYLE, fontName="Helvetica-Bold", fontSize=14, leading=18, spaceAfter=4)
H2 = ParagraphStyle("h2", parent=STYLE, fontName="Helvetica-Bold", fontSize=10.6, leading=14, spaceBefore=6,
                    spaceAfter=3)
SMALL = ParagraphStyle("s", parent=STYLE, fontSize=8, leading=10, textColor=colors.HexColor("#555555"))


def _pdf(path, title, author, story, footer):
    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawString(18 * mm, 10 * mm, footer)
        canvas.drawRightString(192 * mm, 10 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, subject="", creator=author,
                            invariant=1)
    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)


def _table(rows, widths, header=True):
    t = Table(rows, colWidths=widths)
    st = [("FONT", (0, 0), (-1, -1), "Helvetica", 8.8), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 4)]
    if header:
        st += [("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.8),
               ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EEEEEE"))]
    t.setStyle(TableStyle(st))
    return t


# ------------------------------------------------------------------ the charter (PDF)

def charter(path):
    s = [Paragraph("Experimentation charter: home surfaces", H1),
         Paragraph("Version 4, in force from 1 June 2026. Owner: Saar Dries, Marketplace Science. Approved by the "
                   "product leadership team on 19 May 2026; replaces version 3 (January 2025).", SMALL),
         Spacer(1, 6),
         Paragraph("1. Purpose and scope", H2),
         Paragraph("This charter sets how ranking policies for the home surfaces of the Vouwlijn app and website are "
                   "screened offline, tested online and launched. It covers the home carousel and the home feed. "
                   "Search ranking has its own charter.", STYLE),
         Paragraph("2. Definitions", H2),
         Paragraph("2.1 A <b>carousel session</b> is a logged-in session in which the home carousel rendered at "
                   "least once.", STYLE),
         Paragraph("2.2 <b>Lift</b> is the change in orders placed by the arm's buyers during the test, per 1,000 "
                   "carousel sessions, against the incumbent.", STYLE),
         Paragraph("2.3 The <b>incumbent</b> is the ranker in production on the home carousel when the test "
                   "starts.", STYLE),
         Paragraph("2.4 An arm's <b>carousel order rate</b> in a cell is the number of orders placed from the "
                   "carousel tiles it served, per 1,000 of its carousel sessions in that cell.", STYLE),
         Paragraph("3. Cells", H2),
         Paragraph("Every guardrail on the home surfaces is read in the eight cells below: platform by the buyer's "
                   "tenure at the start of the session, as the account service reports it.", STYLE),
         _table([["Platform", "Tenure 0 to 29 days", "30 to 179 days", "180 to 729 days", "730 days and over"],
                 ["App", "app 0-29", "app 30-179", "app 180-729", "app 730+"],
                 ["Web", "web 0-29", "web 30-179", "web 180-729", "web 730+"]],
                [22 * mm, 37 * mm, 37 * mm, 37 * mm, 41 * mm]),
         Spacer(1, 6),
         Paragraph("4. Launch conditions for a slot test", H2),
         Paragraph("A registered policy may take a test slot only if, on the offline screen:", STYLE),
         Paragraph("(a) its lift is at least 2.0;", STYLE),
         Paragraph("(b) in no cell of the table in section 3 is its carousel order rate more than 1.5 per cent "
                   "below the incumbent's; and", STYLE),
         Paragraph("(c) it meets every commitment to sellers that applies to the home carousel.", STYLE),
         Paragraph("The conditions are applied to point estimates. The offline screen is not a significance test; "
                   "the online test decides whether a policy launches.", STYLE),
         Paragraph("5. Offline screen", H2),
         Paragraph("5.1 Policies are scored on the most recent logged window.", STYLE),
         Paragraph("5.2 An offline estimator may be cited against condition (a) only if, run on each archived "
                   "test's logged sessions, it returns that test's realised lift within 0.25 extra orders per 1,000 "
                   "carousel sessions.", STYLE),
         Paragraph("5.3 Every completed home-carousel test is archived with the logged sessions of its logging "
                   "window and its realised lift.", STYLE),
         Paragraph("6. Test slots", H2),
         Paragraph("The home carousel runs one slot test per quarter. A slot test takes 10 per cent of logged-in "
                   "carousel sessions on each platform for twelve weeks.", STYLE),
         Paragraph("7. Ownership and review", H2),
         Paragraph("Marketplace Science owns this charter and reviews it each January. Ranking Engineering owns the "
                   "carousel logger and the ranking policy register. Changes to sections 2 to 6 need the approval "
                   "of the product leadership team.", STYLE)]
    _pdf(path, "Experimentation charter: home surfaces (v4)", "Saar Dries", s,
         "Vouwlijn  |  Internal  |  Experimentation charter, home surfaces, version 4")


# ------------------------------------------------------------------ buyer terms (PDF)

def terms(path):
    s = [Paragraph("Vouwlijn Buyer Protection: terms for buyers", H1),
         Paragraph("Version September 2026, in force from 1 September 2026.", SMALL), Spacer(1, 6),
         Paragraph("1. What Buyer Protection covers", H2),
         Paragraph("Buyer Protection covers items you pay for through Vouwlijn checkout, in the app or on the "
                   "website. If an item does not arrive, or arrives significantly not as described, report it within "
                   "two days of delivery and we refund the item price, the shipping and the Buyer Protection fee.",
                   STYLE),
         Paragraph("2. When it does not apply", H2),
         Paragraph("If you collect an item in person and pay the seller directly, the purchase is not covered and no "
                   "Buyer Protection fee is charged. Pickup orders paid through checkout are covered.", STYLE),
         Paragraph("3. The fee", H2),
         Paragraph("Every covered purchase carries a Buyer Protection fee: a fixed amount plus a percentage of the "
                   "price you pay for the item, after any accepted offer. Shipping is charged separately and carries "
                   "no fee. The amounts in force are listed in our tariff overview.", STYLE),
         Paragraph("4. Changes to the fee", H2),
         Paragraph("We change the fee only after the change has been approved by the Vouwlijn pricing committee, "
                   "and we announce it at least 30 days before it applies.", STYLE),
         Paragraph("5. Refunds and disputes", H2),
         Paragraph("Refunds go back to the payment method you used: your card, your bank account or your Vouwlijn "
                   "balance. If you and the seller disagree, our support team decides on the evidence both of you "
                   "provide. Reports made after the two-day window are handled as goodwill cases.", STYLE),
         Paragraph("6. Contact", H2),
         Paragraph("Questions about Buyer Protection go to Vouwlijn support through the Help Centre in the app.",
                   STYLE)]
    _pdf(path, "Vouwlijn Buyer Protection: terms for buyers (September 2026)", "Vouwlijn Legal", s,
         "Vouwlijn B.V.  |  Buyer Protection terms  |  September 2026")


# ------------------------------------------------------------------ commitment and minutes (DOCX)

def _docx(path, author, created, paragraphs, title):
    from docx import Document
    from docx.shared import Pt
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for kind, text in paragraphs:
        if kind == "title":
            p = doc.add_paragraph()
            r = p.add_run(text)
            r.bold = True
            r.font.size = Pt(14)
        elif kind == "h":
            p = doc.add_paragraph()
            r = p.add_run(text)
            r.bold = True
        elif kind == "small":
            p = doc.add_paragraph()
            r = p.add_run(text)
            r.font.size = Pt(9)
        else:
            doc.add_paragraph(text)
    cp = doc.core_properties
    cp.author = author
    cp.last_modified_by = author
    cp.title = title
    cp.comments = ""
    cp.subject = ""
    cp.keywords = ""
    cp.category = ""
    cp.revision = 3
    cp.created = created
    cp.modified = created
    doc.save(path)


def commitment(path):
    paras = [
        ("title", "Fresh listings on the home carousel: our commitment to private sellers (2026)"),
        ("small", "Owner: Amélie Middelkoop, Seller Experience. Agreed with the product leadership team on "
                  "3 February 2026 and published to sellers in the Help Centre on 10 February 2026."),
        ("h", "Why we made it"),
        ("p", "Private sellers told us through 2025 that a new listing could go a whole weekend without being seen. "
              "Most of our sellers list a handful of items a month, and the first two days decide whether an item "
              "sells. In February we promised sellers that the home carousel keeps room for new listings."),
        ("h", "The commitment"),
        ("p", "Whatever ranker serves the home carousel, at least 12 of every 100 tiles it serves go to listings "
              "under 48 hours old. We count per served ranking: each ranking the carousel serves counts once, "
              "however many times the app or the website renders it again in the same session."),
        ("h", "Where it applies"),
        ("p", "The commitment applies to the ranker in production and to every test arm on the home carousel. It "
              "does not apply to search, the home feed or category pages."),
        ("h", "How we check it"),
        ("p", "Seller Experience reviews compliance every quarter from the carousel logger and reports to the "
              "product leadership team. A breach in production is fixed in the next release; a test arm that "
              "cannot meet the commitment does not run."),
        ("h", "Contact"),
        ("p", "Questions about the commitment go to Amélie Middelkoop or to the seller experience channel."),
    ]
    _docx(path, "Amélie Middelkoop", datetime(2026, 2, 3, 10, 12), paras,
          "Fresh listings on the home carousel: commitment to private sellers")


def minutes(path):
    paras = [
        ("title", "Pricing committee: minutes of the meeting of 6 October 2026"),
        ("small", "Present: Rik Breugelensis (chair), Esila Stichter, Livia Verhaar, Amélie Middelkoop, Stef "
                  "Steenbakkers. Minutes: Zoey Joosten."),
        ("h", "1. Buyer-protection fee income, third quarter"),
        ("p", "Esila Stichter took the committee through the Q3 statement. Income moved with the September tariff "
              "change as planned. Refund costs were flat on the second quarter. No action."),
        ("h", "2. Seller listing promotions"),
        ("p", "No change to the price of listing bumps. Stef Steenbakkers will bring bump take-up by category to "
              "the January meeting."),
        ("h", "3. Bundle shipping from January"),
        ("p", "Approved: bundles of three or more items from one seller ship at the single-parcel rate from "
              "11 January 2027. Seller Experience will brief sellers in December."),
        ("h", "4. Any other business"),
        ("p", "None. Next meeting: 12 January 2027."),
    ]
    _docx(path, "Zoey Joosten", datetime(2026, 10, 6, 16, 40), paras, "Pricing committee minutes, 6 October 2026")


# ------------------------------------------------------------------ register (JSON)

def register(path):
    pol = [
        dict(policy_id="HC-24", name="Blend v7", status="production", owner="Tygo Knoers", registered="2025-03-17",
             build="blend-7.4", family="Blended popularity and personal relevance",
             inputs=["listing popularity (views, favourites, orders)", "buyer category and size affinity"],
             serving="Six tiles ranked by blended score from the candidate pool."),
        dict(policy_id="HC-31", name="Two-tower personaliser", status="registered", owner="Jasmijn Zijlemans",
             registered="2026-04-20", build="tt-3.2", family="Two-tower retrieval and ranking",
             inputs=["buyer and listing embeddings from views, orders and searches"],
             serving="Six tiles by predicted order probability."),
        dict(policy_id="HC-33", name="Velocity boost", status="registered", owner="Fabian Stoffel",
             registered="2026-06-01", build="vb-2026.2", family="Boost on the production blend",
             inputs=["category order velocity by size, trailing 24 hours", "buyer sizes", "buyer listing saves"],
             serving="Tiles 1 and 2: two fast-selling listings in the buyer's sizes. Tiles 3 to 6: Blend v7."),
        dict(policy_id="HC-34", name="Session-sequence model", status="registered", owner="Tycho Feenstra",
             registered="2026-05-11", build="seq-1.6", family="Sequence model",
             inputs=["in-session sequence of listing views"],
             serving="Six tiles re-ranked after every render from the views so far in the session."),
        dict(policy_id="HC-36", name="Local pickup boost", status="registered", owner="Yasmine Billung",
             registered="2026-05-25", build="lpb-1.1", family="Boost on the production blend",
             inputs=["buyer region", "seller pickup settings"],
             serving="Listings offered for pickup within 15 km of the buyer ranked up by one to three places."),
        dict(policy_id="HC-37", name="Sequence ranker with fresh-listing interleave", status="registered",
             owner="Kayleigh Zeemans", registered="2026-06-15", build="seqi-2.0", family="Sequence model",
             inputs=["in-session sequence of listing views", "listing age"],
             serving="Tiles 3 and 6 go to a listing under 48 hours old when the candidate pool holds one; the "
                     "other tiles follow the sequence model."),
        dict(policy_id="HC-39", name="Seller-diversity re-ranker", status="registered", owner="Ali Maas",
             registered="2026-03-30", build="sdr-1.3", family="Re-ranker on the production blend",
             inputs=["seller id"], serving="At most one tile per seller; the blend's order otherwise."),
    ]
    doc = {"register": "Home surfaces ranking policy register", "surface": "home carousel",
           "maintained_by": "Tygo Knoers, Ranking Engineering", "updated": "2026-10-05",
           "note": "A policy is registered once its build has passed ranking review and the carousel logger can "
                   "serve it. The register records what each policy is and what it reads, not how it performs.",
           "policies": pol}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write("\n")


# ------------------------------------------------------------------ field reference (MD)

FIELDS = """# Field reference: carousel logger and the extracts read with it

Maintained by Tygo Knoers (Ranking Engineering) with Marketplace Science. Logger release 4.3, in use since
8 June 2026. Times are local (Europe/Amsterdam) unless a field says otherwise.

## home_carousel_render_log

One row per render of the home carousel in a logged session. The logger enrols one home-carousel session per
buyer from its buyer slice and draws one ranker for that session.

| field | meaning |
|---|---|
| session_id | The logged session. |
| render_seq | 1 for the first render of the session, then 2, 3 and so on. |
| rendered_at | When the carousel rendered. |
| platform | app or web. |
| buyer_tenure_days | Days since the buyer's account was created, as the account service reports it at the start of the session. |
| pool_id | The candidate pool the session's ranking was drawn from. |
| ranker | Policy id of the ranker drawn for the session (see the ranking policy register). |
| propensity | Probability with which the logger draws that ranker for a session in the session's cell. |
| ordered_tiles | Positions (1 to 6) of the session's tiles the buyer ordered from in the session, space separated; blank if none. |

The session is the draw unit: one ranker and one propensity per session. Every render repeats the session's
ranking, so ordered_tiles is the same on every row of a session. The logger fills each cell's quota for each
ranker exactly over the window, in the proportions of its allocation table.

## home_carousel_served_rankings

One row per logged session.

| field | meaning |
|---|---|
| session_id | As in the render log. |
| buyer_id | The buyer. A buyer has one logged session in the window. |
| started_at, ended_at | First render; end of the session (30 minutes without activity closes a session). |
| buyer_region | Province code of the buyer's address. |
| tile_1 to tile_6 | Listing ids of the ranking served, by position. A listing shown on a buyer's carousel is kept off it in their later sessions for seven days. |
| tile_1_age_h to tile_6_age_h | Hours since each listing went live, when the ranking was served. |
| watchlist_at_start | Listing ids on the buyer's watch list when the session started (live listings only), space separated. |

## orders_enrolled_buyers

Every order placed by the buyers in the logger slice from 1 June to 11 October 2026, in every channel.

| field | meaning |
|---|---|
| order_id, buyer_id, listing_id | One row per order; one listing per order. |
| ordered_at | When the order was placed. |
| channel | Where the buyer placed it: carousel (a home carousel tile), search, favourites (the watch list tab), alerts (a price-drop or almost-gone alert), shop (a seller's shop page or a shared link). |
| home_session_id | For carousel orders, the home session the order was placed in, logged or not. Blank for other channels. |
| platform | app or web. |
| category | Listing category. |
| asking_price_eur | The listing's price as shown when the order was placed. |
| delivery | shipped or pickup. |

## payments_buyer_protection

Every card and iDEAL payment the payment provider captured for those orders, 1 June to 11 October 2026.

| field | meaning |
|---|---|
| payment_id, order_id | The capture and the order it pays; an order has at most one. |
| captured_at | When the payment was captured. |
| amount_eur | What the card or bank account was charged: the item price paid, shipping and the buyer-protection fee. |
| shipping_eur | Shipping charged; 0 for pickup. |
| buyer_protection_fee_eur | The fee charged, at the tariff in force on the capture date. |

## offers_accepted

Offers those buyers made that the seller accepted.

| field | meaning |
|---|---|
| offer_id, listing_id, buyer_id | The offer. |
| offered_at, accepted_at | When the buyer offered and when the seller accepted. |
| offer_eur | The accepted price. |
| expires_at | An accepted offer can be paid at the offer price until this time, 48 hours after acceptance. |

## home_carousel_sessions_weekly

Logged-in home-carousel sessions by ISO week (week_start is the Monday), platform and tenure band. How each
release bands tenure is in the analytics release log.
"""


def field_reference(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(FIELDS)


# ------------------------------------------------------------------ release log, capacity note (MD)

RELEASES = """# Analytics release log: home surfaces tables

Maintained by Lindsey Mudden, Analytics Engineering. Newest first.

## 2026-08-14: home_carousel_sessions_weekly, restatement R2 (2026-W01 to 2026-W26)

Tenure is recomputed from the oldest account merged into each buyer's account, matching the account service.
Sessions move between tenure bands; every platform-week total is unchanged. R2 replaces the first release for
those weeks and ships as its own export, home_carousel_sessions_weekly_R2_2026W01_2026W26.

## 2026-07-03: home_carousel_sessions_weekly, tenure source

From 2026-W27 the table takes tenure from the account service (the oldest merged account). Weeks before
2026-W27 keep the band from each account's own creation date until they are restated.

## 2026-04-21: home tables, bot filter v3

Sessions from flagged automation are removed from the home tables from 2026-W17, about 0.4 per cent of web
sessions. Earlier weeks are not restated.

## 2026-02-02: home_carousel_sessions_weekly, warehouse move

Table moved to the new warehouse. No change to definitions; counts reconciled to the old table within 0.01 per
cent for 2025-W01 to 2026-W04.

## 2025-11-10: logged-in definition

Web sessions with a remembered login count as logged in from 2025-W46, as they already did on the app. Web
counts rise by about 3 per cent from that week.

## 2025-03-03: home_carousel_sessions_weekly, first publication

Weekly logged-in home-carousel sessions by platform and tenure band, from 2025-W01.
"""

CAPACITY = """# Home carousel: test capacity and release gating

Owner: Britt Tins, Experimentation Programme. Last updated 22 September 2026.

## Slots

The home carousel takes one slot test per quarter. The Q1 2027 slot runs from 4 January to 28 March 2027,
twelve weeks. The product leadership team fixes the Q1 test calendar at its planning meeting on 28 October
2026.

## Traffic planning

Plan a slot test's traffic cell by cell, in the cells of the experimentation charter, on the same ISO weeks one
year before the slot, from the weekly sessions table.

## Release gating

A web arm starts on the test's start date. An app arm begins with the first app release on or after the test's
start date, because test assignment ships inside the app build. Release dates are in the app release calendar
kept by Mobile Platform.

## Overlaps

No other home-carousel test runs during a slot. Search tests may run alongside a slot.

## Ramp and stop rules

Arms start at full share; there is no ramp on the home carousel. A slot test stops early only on a guardrail
breach in production monitoring or an incident, and the stop goes to the product leadership team the same
day.
"""


def release_log(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(RELEASES)


def capacity_note(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(CAPACITY)


# ------------------------------------------------------------------ tariffs (CSV)

def tariff_register(path):
    rows = [
        ("KB-2024-01", "2024-03-01", "0.70", "5.0", "Rik Breugelensis", "2024-02-14", "PC 2024-02-13"),
        ("KB-2026-02", "2026-09-01", "0.80", "5.0", "Esila Stichter", "2026-07-09", "PC 2026-07-07"),
        ("KB-2027-01", "2027-04-05", "0.95", "5.0", "Esila Stichter", "2026-09-22", ""),
    ]
    df = pd.DataFrame(rows, columns=["tarief_id", "ingangsdatum", "vast_bedrag_eur", "percentage_van_artikelprijs",
                                     "ingevoerd_door", "ingevoerd_op", "besluit"])
    df.to_csv(path, index=False, lineterminator="\n")


# ------------------------------------------------------------------ thread (TXT)

THREAD = """Subject: Q1 home carousel slot: inputs before 28 October
Thread exported from #carousel-slot-q1 on 14 October 2026

----------------------------------------------------------------------
From: Saar Dries
Date: Mon 5 Oct 2026, 09:12 CEST

Morning all. I take one name for the Q1 home carousel slot to the planning meeting on the 28th. The logger
window closed on 20 September and the extracts are in the review folder. If you have a view on which of the
six registered policies should have it, now is the time; I'll put it in front of the numbers.

----------------------------------------------------------------------
From: Fabian Stoffel
Date: Mon 5 Oct 2026, 10:41 CEST

The velocity boost puts the strongest tiles we have ever had on the carousel. Look at what buyers do with
tiles 1 and 2 when they are pinned; the log bears it out. I'd want the slot.

----------------------------------------------------------------------
From: Tygo Knoers
Date: Mon 5 Oct 2026, 11:05 CEST

Logger and register are final as of this morning. Reminder for whoever runs the screen: the archive has never
missed with session weights. Everything else we have pointed at it drifts.

----------------------------------------------------------------------
From: Kayleigh Zeemans
Date: Tue 6 Oct 2026, 08:57 CEST

Honest view from the interleave side: it gives up two tiles on most rankings to listings nobody has seen yet,
and I would not put it up against the velocity boost for this slot. Happy to wait for Q2.

----------------------------------------------------------------------
From: Amélie Middelkoop
Date: Tue 6 Oct 2026, 09:30 CEST

Whatever goes in, the fresh-listing commitment holds for test arms as well. Sellers have had Checkout 3 to get
used to this autumn; please don't make me explain to them in January why we dropped the commitment for twelve
weeks.

----------------------------------------------------------------------
From: Livia Verhaar
Date: Wed 7 Oct 2026, 18:02 CEST

One name on the 28th, please, and what the quarter buys us. Finance books the Q1 plan off the slot, so I want
buyer-protection fee income next to orders, cell by cell, the way we read the guardrail.

----------------------------------------------------------------------
Vouwlijn internal. Do not forward outside the product organisation.
"""


def thread(path):
    with open(path, "w", encoding="utf-8") as f:
        f.write(THREAD)


# ------------------------------------------------------------------ workbooks (XLSX)

def _workbook(path, author, created):
    import xlsxwriter
    wb = xlsxwriter.Workbook(path, {"strings_to_numbers": False})
    wb.set_properties({"author": author, "company": "Vouwlijn", "created": created, "comments": ""})
    return wb


def finance_statement(path, PROT):
    """Fee income booked on the logger slice's protected purchases, by month and order platform:
    provider captures at their capture time, balance purchases at the order time, excluding VAT."""
    import params as P
    df = PROT.copy()
    df["month"] = [str(np.datetime64("2025-01-01T00:00:00") + np.timedelta64(int(x), "s"))[:7] for x in df.booked]
    df = df[df.month.isin(["2026-07", "2026-08", "2026-09"])]
    g = df.groupby(["month", "platform"]).agg(orders=("order_id", "size"), item=("paid", "sum"),
                                               fee=("fee_cents", "sum")).reset_index()
    wb = _workbook(path, "Esila Stichter", datetime(2026, 10, 9, 14, 5))
    ws = wb.add_worksheet("Q3 2026")
    b = wb.add_format({"bold": True})
    money = wb.add_format({"num_format": "#,##0.00"})
    num = wb.add_format({"num_format": "#,##0"})
    ws.write(0, 0, "Buyer-protection fee income, July to September 2026", b)
    ws.write(1, 0, "Purchases covered by Buyer Protection, placed by buyers in the home-carousel logger slice, every "
                   "payment method; booked by month of payment and the platform the order was placed on. Ledger "
                   "account 8120.")
    ws.write(2, 0, "Fee income excl. VAT. The fee buyers pay includes 21 per cent VAT, which is booked to account 1630.")
    ws.write(3, 0, "Prepared for Marketplace Science by Esila Stichter, Finance, 9 October 2026.")
    hdr = ["Month", "Platform", "Protected orders", "Item value paid (EUR)", "Fee income excl. VAT (EUR)"]
    for j, h in enumerate(hdr):
        ws.write(5, j, h, b)
    r = 6
    names = {"2026-07": "July 2026", "2026-08": "August 2026", "2026-09": "September 2026"}
    vat = 1.0 + P.VAT_RATE
    for _, row in g.iterrows():
        ws.write(r, 0, names[row.month])
        ws.write(r, 1, row.platform)
        ws.write_number(r, 2, int(row.orders), num)
        ws.write_number(r, 3, float(row["item"]), money)
        ws.write_number(r, 4, round(row.fee / 100.0 / vat, 2), money)
        r += 1
    ws.write(r, 0, "Total", b)
    ws.write_number(r, 2, int(g.orders.sum()), num)
    ws.write_number(r, 3, float(g["item"].sum()), money)
    ws.write_number(r, 4, round(g.fee.sum() / 100.0 / vat, 2), money)
    ws.set_column(0, 0, 16)
    ws.set_column(1, 1, 10)
    ws.set_column(2, 4, 24)
    wb.close()
    return g


def search_tests(path):
    rows = [
        ("S-26-01", "Spelling correction v4", "2026-01-12", "2026-02-08", 10, 1.4, 0.2, 2.6, "launched"),
        ("S-26-02", "Velocity boost on search results", "2026-02-16", "2026-03-15", 10, 3.1, 1.6, 4.6, "launched"),
        ("S-26-03", "Two-tower retrieval for search", "2026-03-23", "2026-04-19", 10, 2.4, 0.9, 3.9,
         "not launched (latency)"),
        ("S-26-04", "Freshness boost (listings under 48 hours)", "2026-04-27", "2026-05-24", 10, -0.6, -2.0, 0.8,
         "not launched"),
        ("S-26-05", "Size filter defaults from purchase history", "2026-06-01", "2026-06-28", 5, 1.9, -0.1, 3.9,
         "not launched (inconclusive)"),
    ]
    wb = _workbook(path, "Evy Mathieu", datetime(2026, 7, 3, 11, 20))
    ws = wb.add_worksheet("tests")
    b = wb.add_format({"bold": True})
    hdr = ["test_id", "change", "start", "end", "traffic_share_pct", "search_orders_lift_per_1000_searches",
           "interval_low_90", "interval_high_90", "decision"]
    for j, h in enumerate(hdr):
        ws.write(0, j, h, b)
    for i, row in enumerate(rows, start=1):
        for j, v in enumerate(row):
            if isinstance(v, (int, float)):
                ws.write_number(i, j, v)
            else:
                ws.write(i, j, v)
    ws2 = wb.add_worksheet("about")
    ws2.write(0, 0, "Search ranking tests, first half of 2026. Lift is search orders per 1,000 searches against "
                    "the production search ranker, from the online test. Owner: Evy Mathieu, Search Relevance.")
    ws.set_column(0, 0, 10)
    ws.set_column(1, 1, 44)
    ws.set_column(2, 8, 16)
    wb.close()


def archive_workbook(path, tests_df, sessions_df):
    wb = _workbook(path, "Saar Dries", datetime(2026, 6, 2, 9, 30))
    b = wb.add_format({"bold": True})
    ws = wb.add_worksheet("tests")
    cols = list(tests_df.columns)
    for j, h in enumerate(cols):
        ws.write(0, j, h, b)
    for i, row in enumerate(tests_df.itertuples(index=False), start=1):
        for j, v in enumerate(row):
            if isinstance(v, (int, float, np.integer, np.floating)) and not isinstance(v, bool):
                ws.write_number(i, j, float(v))
            else:
                ws.write(i, j, str(v))
    ws.set_column(0, len(cols) - 1, 16)
    ws2 = wb.add_worksheet("logged_sessions")
    cols2 = list(sessions_df.columns)
    for j, h in enumerate(cols2):
        ws2.write(0, j, h, b)
    arr = sessions_df.to_numpy(dtype=object)
    for i in range(len(arr)):
        for j, v in enumerate(arr[i]):
            if isinstance(v, (int, float, np.integer, np.floating)) and not isinstance(v, bool):
                ws2.write_number(i + 1, j, float(v))
            else:
                ws2.write_string(i + 1, j, str(v))
    ws3 = wb.add_worksheet("notes")
    notes = [
        "Home carousel test archive. Maintained by Marketplace Science; one row per completed test on the tests sheet.",
        "realised_lift: the test's lift as the experimentation charter defines it, from the online test; "
        "realised_lift_low90 and realised_lift_high90 bound its 90 per cent interval.",
        "offline_estimate_published: the offline estimate published before the test, computed by replay over the "
        "logging window's renders, the method then in use.",
        "logged_sessions: every session of each test's logging window. arm is control (the incumbent of the time) "
        "or test; propensity is the logger's probability for that arm in the session's cell; in_session_orders "
        "counts the orders the buyer placed from the session's carousel tiles in the session.",
    ]
    for i, n in enumerate(notes):
        ws3.write(i, 0, n)
    ws3.set_column(0, 0, 120)
    wb.close()


# ------------------------------------------------------------------ survey (CSV)

def seller_survey(path):
    rng = P.stream("survey")
    n = 1612
    tenure = rng.choice(["under 6 months", "6 to 24 months", "over 2 years"], size=n, p=[0.22, 0.38, 0.40])
    listings = np.clip(np.round(np.exp(rng.normal(np.log(9), 0.9, n))), 1, 400).astype(int)
    cat = rng.choice(P.CATEGORIES, size=n, p=P.CAT_P)
    q1 = np.clip(np.round(rng.normal(2.6, 1.1, n)), 1, 5).astype(int)
    q2 = np.clip(np.round(rng.normal(3.7, 1.0, n)), 1, 5).astype(int)
    q3 = rng.choice(["yes", "no"], size=n, p=[0.31, 0.69])
    region = rng.choice(["NH", "ZH", "UT", "NB", "GE", "OV", "LI", "GR", "FR", "DR", "FL", "ZE"], size=n,
                        p=[0.17, 0.21, 0.08, 0.15, 0.12, 0.07, 0.06, 0.03, 0.04, 0.03, 0.03, 0.01])
    days = rng.integers(0, 30, size=n)
    dates = [(date(2026, 5, 4) + pd.Timedelta(days=int(d)).to_pytimedelta()).isoformat() for d in days]
    rid = 50_000 + np.cumsum(rng.integers(1, 9, size=n))
    df = pd.DataFrame(dict(respondent_id=rid, response_date=dates, seller_tenure=tenure,
                           listings_last_90_days=listings, main_category=cat,
                           q1_new_listings_seen_in_first_two_days=q1, q2_would_list_more_if_seen_sooner=q2,
                           q3_offers_pickup=q3, region=region))
    df = df.sort_values(["response_date", "respondent_id"], kind="stable")
    df.to_csv(path, index=False, lineterminator="\n")


# ------------------------------------------------------------------ the folder index (MD)

def folder_index(path, rows):
    lines = ["# Slot review folder: what is in it and where it came from", "",
             "Compiled by Saar Dries, Marketplace Science, 14 October 2026, for the Q1 2027 home carousel slot "
             "recommendation. Every extract was pulled for this review from the system named; documents are the "
             "current versions of record.", "",
             "| file | what it is | covers | from | pulled |", "|---|---|---|---|---|"]
    for r in rows:
        lines.append("| " + " | ".join(r) + " |")
    lines += ["", "Extracts carry only the logged-in buyers in the carousel logger's slice unless the row says "
                  "otherwise. Nothing in the folder has been edited after export.", ""]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
