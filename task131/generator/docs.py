"""Documents in the pack. Short, functional, in the voice of the people who own them."""
import datetime as dt
import json
import os
import shutil
import subprocess
import tempfile

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Cm
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill

import world as W


def _doc(author, title, created):
    d = docx.Document()
    st = d.styles["Normal"]
    st.font.name = "Arial"
    st.font.size = Pt(10)
    for s in d.sections:
        s.page_width, s.page_height = Cm(21.0), Cm(29.7)
        s.left_margin = s.right_margin = Cm(2.2)
        s.top_margin = Cm(1.8)
    cp = d.core_properties
    cp.author = author
    cp.last_modified_by = author
    cp.title = title
    cp.created = created
    cp.modified = created
    cp.revision = 4
    cp.comments = ""
    cp.keywords = ""
    cp.subject = ""
    cp.category = ""
    return d


def _para(d, text, bold=False, size=None, space_after=4, italic=False):
    p = d.add_paragraph()
    r = p.add_run(text)
    r.bold = bold
    r.italic = italic
    if size:
        r.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(space_after)
    return p


def standard_pdf(out_path):
    """Programme measurement standard MP-3, revision 3 (March 2026), exported to PDF."""
    created = dt.datetime(2026, 3, 18, 9, 41)
    d = _doc(W.PEOPLE["analytics"], "MP-3 Measuring member programme offers", created)
    _para(d, "Talwerk Genossenschaft  ·  Mitgliederprogramm", size=8, italic=True)
    _para(d, "Standard MP-3: measuring member programme offers", bold=True, size=14, space_after=2)
    _para(d, "Revision 3, 18 March 2026. Owner: Mirjana Felder, programme analytics. "
             "Approved by the programme steering group, 24 March 2026. Replaces revision 2 (October 2024).",
          size=8.5, space_after=10)

    sections = [
        ("1  Scope",
         "This standard says how the member programme measures an offer it has tested on member cards, "
         "and what the programme's annual budget for an offer is set on. It applies to every offer test run "
         "through the offer engine from the summer 2026 test onwards. It does not cover the base points "
         "scheme, which finance budgets separately."),
        ("2  Net margin",
         "Net margin is gross margin less reward cost, as both are booked in the card-week sales facts. "
         "Reward cost carries the base points issued, the offer's own points, and vouchers and coupons funded "
         "by the programme, in the week they are booked."),
        ("3  Baseline and run-rate weeks",
         "The baseline weeks are the eight ISO weeks before a test opens. The run-rate weeks are the final six "
         "weeks of the test. For the summer 2026 test (ST26) the baseline weeks are 2026-W15 to 2026-W22 and the "
         "run-rate weeks are 2026-W29 to 2026-W34. The first six test weeks are not used for budgeting, because "
         "offers settle after their launch."),
        ("4  Incremental net margin",
         "The incremental net margin of an offer is the change in net margin from the baseline weeks to the "
         "run-rate weeks under the offer, against the same change without it, and it is stated per active "
         "card-week. Every card allocated to the test is an active card. A week in which a card made no purchase "
         "counts as a week with zero net margin; it is not left out."),
        ("5  Annual programme value",
         "The annual programme value of an offer is its incremental net margin per active card-week, times 52, "
         "times the active cards in that year's programme plan. Figures are carried unrounded through the "
         "calculation and rounded once, in the figure reported."),
        ("6  Regional figures",
         "Regional figures use the regions of the branch network in force on 1 July 2026. A card counts in the "
         "region of its membership's home branch."),
        ("7  Reporting",
         "Per card-week figures are reported in CHF to two decimals. Annual programme values are reported in "
         "CHF thousands. The programme lead takes the offer and its value to the executive board for the budget "
         "round; the steering group sees the same figures."),
    ]
    for h, t in sections:
        _para(d, h, bold=True, size=10.5, space_after=2)
        _para(d, t, space_after=8)

    _para(d, "Revision history", bold=True, size=9, space_after=2)
    tbl = d.add_table(rows=4, cols=3)
    tbl.style = "Table Grid"
    rows = [("Rev.", "Date", "Change"),
            ("1", "Mar 2023", "First issue, after the spring 2023 coupon test."),
            ("2", "Oct 2024", "Reward cost includes programme-funded coupons; run-rate weeks set at six."),
            ("3", "Mar 2026", "Annual value set on the programme plan's active cards; regional figures added.")]
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            c = tbl.cell(i, j)
            c.text = v
            for p in c.paragraphs:
                for run in p.runs:
                    run.font.size = Pt(8.5)
                    run.bold = (i == 0)
    _para(d, "")
    _para(d, "Distribution: programme steering group; programme finance; CRM and offer engine; data platform.",
          size=8, italic=True)

    tmp = tempfile.mkdtemp()
    src = os.path.join(tmp, "MP-3_measuring_offers_rev3.docx")
    d.save(src)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, src],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.move(os.path.join(tmp, "MP-3_measuring_offers_rev3.pdf"), out_path)
    shutil.rmtree(tmp)


def network_notice_docx(out_path):
    created = dt.datetime(2026, 6, 12, 16, 5)
    d = _doc(W.PEOPLE["network"], "Branch network changes from 1 July 2026", created)
    _para(d, "Talwerk Genossenschaft  ·  Netzplanung", size=8, italic=True)
    _para(d, "Branch network changes from 1 July 2026", bold=True, size=13, space_after=2)
    _para(d, "To: branch managers, area managers, member services, CRM, finance. From: Marta Braun, network "
             "planning. 12 June 2026.", size=8.5, space_after=10)
    _para(d, "The board confirmed the following changes at its meeting of 2 June. They take effect on "
             "Wednesday 1 July 2026 unless stated otherwise.", space_after=8)

    _para(d, "Closures", bold=True, space_after=2)
    _para(d, "Degersheim (2209) trades for the last time on Tuesday 30 June. The lease is not being renewed. "
             "Members administered at Degersheim are administered from Herisau (6101) from 1 July. Two staff "
             "move to Herisau and one to Flawil.", space_after=4)
    _para(d, "Egnach (4105) trades for the last time on Tuesday 30 June. Members administered at Egnach are "
             "administered from Arbon (4101) from 1 July.", space_after=8)

    _para(d, "Regions", bold=True, space_after=2)
    _para(d, "Rorschach Hafen (3107), Goldach (3112) and Thal (3115) move from Rheintal to St. Gallen Stadt. "
             "From 1 July they report to Amelie Peter and are delivered on the St. Gallen evening route. "
             "Rheintal keeps Altstätten, Heerbrugg, Widnau and Oberriet.", space_after=8)

    _para(d, "Other", bold=True, space_after=2)
    _para(d, "Herisau extends Saturday opening to 18:00 from 4 July. The Arbon fresh counter is refitted in the "
             "week of 13 July and closes for three days; the shop stays open. Branch numbers do not change.",
          space_after=8)
    _para(d, "Questions to network planning, extension 2417.", size=8.5, italic=True)
    d.save(out_path)


def catalogue_json(out_path):
    cat = {
        "test_code": "ST26",
        "name": "Sommertest 2026",
        "engine_release": "OE 4.2.1",
        "allocated_on": "2026-05-26",
        "eligible_cards": "every member card with at least one purchase from 6 April 2026",
        "allocation": {"unit": "card", "method": "bucket 0-99 from a hash of the card number",
                       "cells": {"K": [0, 19], "A": [20, 39], "B": [40, 59], "C": [60, 79], "D": [80, 99]}},
        "runs": {"opens": "2026-06-01", "closes": "2026-08-23"},
        "cells": [
            {"cell": "K", "name": "Kontrolle", "offer": None,
             "mechanics": "base points only (1 point per whole franc, CHF 0.01 a point)"},
            {"cell": "A", "name": W.OFFER_NAME["A"], "offer": "fresh bonus",
             "mechanics": "5 per cent back in points on fruit, vegetables, bread and dairy bought with the card",
             "funded_by": "programme"},
            {"cell": "B", "name": W.OFFER_NAME["B"], "offer": "triple points",
             "mechanics": "triple base points on every basket of CHF 50 or more paid with the card",
             "funded_by": "programme"},
            {"cell": "C", "name": W.OFFER_NAME["C"], "offer": "monthly target",
             "mechanics": "a CHF 15 voucher in the week the card's spend in a calendar month reaches CHF 250",
             "funded_by": "programme"},
            {"cell": "D", "name": W.OFFER_NAME["D"], "offer": "weekly picks",
             "mechanics": "three app coupons a week, 20 per cent off a category chosen from the card's purchases",
             "funded_by": "programme"},
        ],
        "rewards_credited_to": "the card used at the till",
        "contact": "crm-offers@talwerk.ch",
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cat, f, indent=2, ensure_ascii=False)
        f.write("\n")


def plan_xlsx(out_path, planned_by_region, active_2026_by_region):
    wb = openpyxl.Workbook()
    wb.properties.creator = W.PEOPLE["finance"]
    wb.properties.lastModifiedBy = W.PEOPLE["finance"]
    wb.properties.created = dt.datetime(2026, 8, 31, 14, 20)
    wb.properties.modified = dt.datetime(2026, 9, 9, 10, 2)
    wb.properties.title = "Mitgliederprogramm Plan 2027"
    ws = wb.active
    ws.title = "Active cards"
    ws["A1"] = "Member programme plan 2027: active cards"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Average active cards in the year, by region (regions as from 1 July 2026). Version 2, 9 Sep 2026."
    ws["A2"].font = Font(italic=True, size=9)
    hdr = ["Region code", "Region", "2026 average to August", "2027 plan"]
    for j, h in enumerate(hdr, 1):
        c = ws.cell(row=4, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE4EC")
    r = 5
    for code, name in W.REGIONS:
        ws.cell(row=r, column=1, value=code)
        ws.cell(row=r, column=2, value=name)
        ws.cell(row=r, column=3, value=int(active_2026_by_region[code]))
        ws.cell(row=r, column=4, value=int(planned_by_region[code]))
        r += 1
    ws.cell(row=r, column=2, value="Total").font = Font(bold=True)
    ws.cell(row=r, column=3, value=int(sum(active_2026_by_region.values())))
    ws.cell(row=r, column=4, value=int(sum(planned_by_region.values())))
    ws.cell(row=r, column=3).font = Font(bold=True)
    ws.cell(row=r, column=4).font = Font(bold=True)
    for col, wdt in zip("ABCD", (12, 22, 22, 12)):
        ws.column_dimensions[col].width = wdt
    for row in ws.iter_rows(min_row=5, max_row=r, min_col=3, max_col=4):
        for c in row:
            c.number_format = "#,##0"

    b = wb.create_sheet("Budget 2027")
    lines = [
        ("Line", "CHF thousands", "Owner", "Note"),
        ("Base points issued", 2961, "Norah Burri", "1 point per whole franc"),
        ("Member offer (programme value)", None, "Patrice Keller", "set in the budget round on the selected offer"),
        ("App and offer engine", 412, "Hansjürg Wolf", "licences and hosting"),
        ("Member services", 688, "member services", ""),
        ("Print and post", 157, "member services", "statements, card reissues"),
    ]
    for i, ln in enumerate(lines, 1):
        for j, v in enumerate(ln, 1):
            c = b.cell(row=i, column=j, value=v)
            if i == 1:
                c.font = Font(bold=True)
    for col, wdt in zip("ABCD", (34, 16, 18, 44)):
        b.column_dimensions[col].width = wdt

    n = wb.create_sheet("Notes")
    n["A1"] = "Active cards: cards with at least one purchase in the period, averaged over the year."
    n["A2"] = "2027 plan: 2026 average to August, with the member growth target of the strategy 2025-2028."
    n["A3"] = "Questions: Norah Burri, programme finance."
    n.column_dimensions["A"].width = 100
    wb.save(out_path)


FIELD_NOTES = """# CRM extracts: field notes

Data platform, member programme marts. Maintained by Francis Amrein. Last edited 11 September 2026.

These notes cover the extracts the data platform hands to programme analytics. Every file is UTF-8.
Card numbers and membership numbers are identifiers, not quantities: keep them as text (older cards
start with a zero).

## card_week_sales_2026w15_w34.parquet

One row per card and ISO week in which the card was presented at a till (at least one basket).
Weeks run Monday to Sunday. A card with no purchase in a week has no row for that week.

| Field | Meaning |
|---|---|
| card_no | 13-digit card number |
| iso_week | ISO week, `YYYY-Www` |
| week_start | Monday of the ISO week |
| baskets | baskets paid with the card in the week |
| gross_sales_chf | sales paid with the card, after till discounts and before reward cost, excluding VAT |
| gross_margin_chf | gross sales less cost of goods, at the week's standard cost |
| reward_cost_chf | points issued (CHF 0.01 a point) plus programme-funded vouchers and coupons booked in the week |

Facts are final for weeks closed before the extract; nothing in 2026-W15 to 2026-W34 is still open.

## st26_offer_allocation.csv

The offer engine's allocation register for the summer 2026 test (ST26), one row per card allocated.
`cell` is K, A, B, C or D as in the test catalogue. `bucket` is the engine's 0-99 bucket for the card.
`allocated_at` is the engine's timestamp (Europe/Zurich).

## member_cards.csv

One row per member card. `card_type` is main or additional; a membership has one main card and up to
three additional cards. `issued_on` is the date the current card number was issued (a reissued card
gets a new date, not a new number). `app_linked` says whether the card is linked to the Talwerk app.

## memberships.csv

One row per membership. `home_branch` is the branch the membership is administered at. `postcode`
and `canton` are the correspondence address. `share_certificates` is the number of co-operative
shares held.

## branch_footfall_2026w15_w34.csv

Door-counter visits by branch and ISO week, from the store systems. `door_count` counts entries
through the main door, members and non-members alike. `counter_status` is partial where a counter
dropped out for part of the week. Closed branches have no rows after their last trading week.

## branches_2026-01.csv

The branch register as issued in January 2026: number, name, town, region, format (S, M, L) and
area manager.
"""


def field_notes_md(out_path):
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(FIELD_NOTES)


def extract_log_txt(out_path, counts):
    lines = [
        "TALWERK DATA PLATFORM  extract log  job=mp_analytics_handover  requested_by=Mirjana Felder",
        "",
    ]
    stamp = {
        "card_week_sales_2026w15_w34.parquet": "2026-09-14 06:12:44",
        "st26_offer_allocation.csv": "2026-09-14 06:14:02",
        "member_cards.csv": "2026-09-14 06:14:31",
        "memberships.csv": "2026-09-14 06:14:49",
        "branches_2026-01.csv": "2026-09-14 06:15:03",
        "branch_footfall_2026w15_w34.csv": "2026-09-14 06:15:20",
    }
    src = {
        "card_week_sales_2026w15_w34.parquet": "mart.mp_card_week (weeks 2026-W15..2026-W34)",
        "st26_offer_allocation.csv": "offer_engine.allocation (test_code = ST26)",
        "member_cards.csv": "crm.card",
        "memberships.csv": "crm.membership",
        "branches_2026-01.csv": "ref.branch (edition 2026-01)",
        "branch_footfall_2026w15_w34.csv": "stores.door_counter_week",
    }
    for k, t in stamp.items():
        lines.append(f"{t}  OK   {k:<40} rows={counts[k]:>8}  source={src[k]}  run_by=f.amrein")
    lines += ["",
              "2026-09-14 06:15:31  INFO  handover folder sealed; next scheduled refresh 2026-10-12",
              ""]
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
