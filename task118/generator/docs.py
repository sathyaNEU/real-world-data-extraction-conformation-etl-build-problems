"""In-fiction documents for the task118 pack: texts and their PDF, DOCX, EML, MD and TXT writers."""
import datetime as dt
import io
import re
import zipfile

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P

MID = "·"


# ---------------------------------------------------------------------------------- writers

def _styles():
    ss = getSampleStyleSheet()
    base = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.2,
                          spaceAfter=5, alignment=TA_LEFT)
    return {
        "title": ParagraphStyle("t", parent=base, fontName="Helvetica-Bold", fontSize=15, leading=19, spaceAfter=4),
        "meta": ParagraphStyle("m", parent=base, fontSize=8.4, leading=11, textColor=colors.HexColor("#444444"),
                               spaceAfter=2),
        "h": ParagraphStyle("h", parent=base, fontName="Helvetica-Bold", fontSize=10.6, leading=14, spaceBefore=8,
                            spaceAfter=3),
        "p": base,
        "small": ParagraphStyle("s", parent=base, fontSize=8, leading=10.5, textColor=colors.HexColor("#555555")),
        "cell": ParagraphStyle("c", parent=base, fontSize=8.6, leading=11, spaceAfter=0),
    }


def write_pdf(path, title, blocks, footer, when, author="Bightline News", subject=""):
    """blocks: list of (kind, payload): title/meta/h/p/small/bullets/table/space."""
    st = _styles()
    flow = []
    for kind, payload in blocks:
        if kind in ("title", "meta", "h", "p", "small"):
            flow.append(Paragraph(payload, st[kind]))
        elif kind == "bullets":
            for b in payload:
                flow.append(Paragraph(b, st["p"], bulletText="•"))
        elif kind == "space":
            flow.append(Spacer(1, payload * mm))
        elif kind == "table":
            rows, widths = payload
            data = [[Paragraph(str(c), st["cell"]) for c in r] for r in rows]
            t = Table(data, colWidths=[w * mm for w in widths], hAlign="LEFT")
            t.setStyle(TableStyle([
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#333333")),
                ("LINEBELOW", (0, -1), (-1, -1), 0.4, colors.HexColor("#999999")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eeeeee")),
            ]))
            flow.append(t)
            flow.append(Spacer(1, 3 * mm))

    def on_page(canv, doc):
        canv.saveState()
        canv.setFont("Helvetica", 7.5)
        canv.setFillColor(colors.HexColor("#555555"))
        canv.drawString(18 * mm, 10 * mm, footer)
        canv.drawRightString(A4[0] - 18 * mm, 10 * mm, "Page %d" % doc.page)
        canv.restoreState()

    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title=title, author=author, subject=subject or title,
                            creator="Bightline News", producer="Bightline News", keywords="", invariant=1)
    doc.build(flow, onFirstPage=on_page, onLaterPages=on_page)
    # invariant mode stamps 2000-01-01; give the file its own date, at equal length so the xref holds
    b = open(path, "rb").read()
    stamp = when.strftime("D:%Y%m%d%H%M%S") + "+10'00'"
    old = b"D:20000101000000+00'00'"
    assert len(stamp.encode()) == len(old)
    assert old in b
    b = b.replace(old, stamp.encode())
    open(path, "wb").write(b)


def write_docx(path, paras, when, author="Bightline News", title=""):
    import docx
    from docx.shared import Pt
    d = docx.Document()
    style = d.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10.5)
    for kind, text in paras:
        if kind == "title":
            d.add_heading(text, level=1)
        elif kind == "h":
            d.add_heading(text, level=2)
        elif kind == "p":
            d.add_paragraph(text)
        elif kind == "small":
            p = d.add_paragraph()
            r = p.add_run(text)
            r.font.size = Pt(8.5)
    cp = d.core_properties
    cp.author = author
    cp.last_modified_by = author
    cp.title = title
    cp.comments = ""
    cp.subject = ""
    cp.keywords = ""
    cp.category = ""
    cp.revision = 3
    cp.created = when
    cp.modified = when + dt.timedelta(hours=2)
    d.save(str(path))
    repack_ooxml(path, when)


def repack_ooxml(path, when):
    """Rewrite an OOXML zip with fixed entry times and the in-fiction application name."""
    zin = zipfile.ZipFile(path)
    infos = zin.infolist()
    data = {i.filename: zin.read(i.filename) for i in infos}
    zin.close()
    if "docProps/app.xml" in data:
        data["docProps/app.xml"] = re.sub(rb"<Application>[^<]*</Application>", b"<Application>Microsoft Office Word</Application>",
                                          data["docProps/app.xml"])
    if "docProps/core.xml" in data:
        data["docProps/core.xml"] = re.sub(rb"<dc:description>[^<]*</dc:description>", b"<dc:description></dc:description>",
                                           data["docProps/core.xml"])
    stamp = (when.year, when.month, when.day, when.hour, when.minute, 0)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zout:
        for i in infos:
            zi = zipfile.ZipInfo(i.filename, date_time=stamp)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o600 << 16
            zi.create_system = 0
            zout.writestr(zi, data[i.filename])


# ---------------------------------------------------------------------------------- the charter (governing)

def charter_blocks():
    rows = [["Desk", "Desk code", "Vertical", "Edition"]]
    for code in P.SHORTLIST:
        d = P.DESK[code]
        rows.append([d[1], code, d[2], "Brisbane" if d[3] == "Brisbane" else "National"])
    return [
        ("title", "Headline squad: 2027 placement brief"),
        ("meta", "Bightline News | Newsroom planning | For the planning meeting on Wednesday 4 November 2026"),
        ("meta", "Owner: Corey Cox, Managing editor | Version 2, 12 October 2026 | Internal"),
        ("space", 3),
        ("h", "What the squad is for"),
        ("p", "The headline squad is six people: a squad lead, three headline editors, a producer and a data analyst. "
              "Each January it moves to one desk for the calendar year, tests that desk's headlines and ships each "
              "winning headline. The squad is judged on incremental article clicks in the twelve months after it "
              "embeds, counted at the owning desk."),
        ("h", "Where it has been"),
        ("p", "Since 2019 the squad has worked with the app desks: Games, Wellness, Puzzles and Recipes. Its 2026 "
              "year with Puzzles finishes on Friday 18 December. Experimentation keeps the change log of closed "
              "embeddings."),
        ("h", "2027 shortlist"),
        ("table", (rows, [52, 26, 30, 30])),
        ("p", "The shortlist was agreed at the September editors' meeting. Politics" + MID + "metro and the app desks "
              "are not being considered for 2027."),
        ("h", "How the decision is made"),
        ("p", "The planning meeting takes one recommendation from the managing editor: the desk, and the clicks the "
              "squad is expected to add there in 2027. The editor-in-chief's office reviews squad placement on the "
              "experimentation dashboard's average winning lift by vertical, and Lisa Jennings's office will present "
              "that view at the meeting. It is the view the room will have in front of it."),
        ("p", "Papers: a short paper and its workbook to Corey Cox by Friday 30 October, for circulation with the "
              "agenda on Monday 2 November."),
        ("h", "Moving in January"),
        ("bullets", [
            "The squad moves on Monday 11 January 2027 and sits with the desk for the year.",
            "The desk editor names a liaison editor by Tuesday 1 December.",
            "Weekly stand-up with the desk editor; monthly report to the managing editor.",
            "Desk access and hardware requests go to the newsroom systems team by Friday 4 December.",
        ]),
        ("space", 2),
        ("small", "Distribution: Lisa Jennings, Kayla Torres, Nina Franklin, Jason Anderson; editors of the six "
                  "shortlisted desks."),
    ]


# ---------------------------------------------------------------------------------- the field reference (dictionary)

def field_reference_md():
    src_rows = "\n".join("| `%s` | %s |" % (k, P.SOURCE_DESC[k]) for k in P.SOURCES)
    return """# Audience warehouse: field reference

Maintained by Audience data (Natalie Benjamin). Revised 2 October 2026.

This reference covers the warehouse tables the audience team extracts for planning work. Each extract
in the planning folder carries the fields described here, in the same names.

## Articles

| Field | Meaning |
|---|---|
| `article_id` | Bightline article number. One per published article or live blog. Web articles share one sequence across both editions; app items are numbered in their own block. |
| `desk_code` | The owning desk, recorded at publication. An article has one owning desk. Codes are listed in the desk register. |
| `published_date` | Date the article was first published, Australian Eastern Standard Time. |
| `canonical_headline` | The headline stored with the article at publication. It is the headline carried in the article's RSS and partner feeds, its search and social metadata, newsletters and alerts. Not included in the pageview extracts. |

## Pageviews by source and age

One row per article, source surface and age band with at least one pageview in the period.

| Field | Meaning |
|---|---|
| `article_id`, `desk_code`, `published_date` | As above. |
| `source_code` | The surface the reader clicked to reach the article (codes below). Every article pageview carries one source code. A typed or bookmarked visit lands on a home page, which is not an article pageview. |
| `age_band` | The article's age when the pageview happened: `0-2h`, `2-6h`, `6-24h`, `1-3d`, `3-7d`, `7d+`. |
| `pageviews` | Article pageviews. A click on a link to an article counts when the article page loads; in planning papers clicks and pageviews are the same measure. |

| Source code | Surface |
|---|---|
""" + src_rows + """

## Headline tests

One row per package of each concluded test. A package is one headline shown in the test: the control or a
variant.

| Field | Meaning |
|---|---|
| `test_id` | Test reference. |
| `engine` | `app`: the app testing engine, in use since 2019. `web`: the web CMS testing engine, whose history begins at the CMS migration on 1 October 2025. |
| `desk_code`, `article_id` | The article the test ran on and its owning desk. |
| `owner_staff_id` | Staff id of the person who created the test. |
| `started_at`, `concluded_at` | UTC. |
| `package_id`, `variant` | `control` is the headline the article was published with; `B` to `E` are the alternatives. |
| `impressions` | Times the package's headline was shown in a test slot. |
| `clicks` | Clicks on the package's headline in the test. |
| `shipped` | `Y` on the one package whose headline stayed live after the test; that is the control when no variant was shipped. |

Winning lift, as reported on the experimentation dashboard, is the shipped package's click-through rate over the
control's, minus one, and zero when the control is kept. The archive holds concluded tests only.

## Desk register

| Field | Meaning |
|---|---|
| `desk_code`, `desk_name` | Desk code and name. |
| `vertical` | The dashboard vertical the desk reports under. |
| `edition` | `national`, `Brisbane` or `app`. |
| `distribution` | `web and app`, or `app only`. App-only items have no web URL, feed entry, search listing, alert or newsletter. |
"""


# ---------------------------------------------------------------------------------- standards (ask path)

def policy_blocks():
    return [
        ("title", "Corrections"),
        ("meta", "Bightline News editorial standards, section 7 | Version 3.2, effective 1 February 2025 | "
                 "Owner: Standards editor"),
        ("space", 3),
        ("h", "7.1 Principle"),
        ("p", "We correct errors of fact promptly, openly and where the error appeared. A correction says what was "
              "wrong in plain words. We do not quietly change a published fact."),
        ("h", "7.2 What needs a correction"),
        ("p", "Any error of fact in a headline, standfirst, body text, caption, chart or byline, once it is "
              "confirmed by the desk editor or the duty editor. Changes of style, spelling of common words or "
              "updates to a developing story are not corrections."),
        ("h", "7.3 How a correction is made"),
        ("p", "The editor making the correction fixes the error and adds a correction note in the CMS. The note "
              "appears at the foot of the article. Where a second error is found later, a further note is added "
              "above the first."),
        ("h", "7.4 Headlines"),
        ("p", "A headline correction is logged on the revision that publishes the corrected headline."),
        ("h", "7.5 Live blogs"),
        ("p", "An error in a live blog entry is fixed in the entry and the correction note is added to the live blog."),
        ("h", "7.6 Speed"),
        ("p", "Headline errors are fixed as soon as they are confirmed. Duty editors aim to confirm a reported "
              "headline error within the hour."),
        ("h", "7.7 Removing a note"),
        ("p", "Correction notes stay with an article. The standards editor can agree to remove a note, for example "
              "after a legal settlement or where the note itself was wrong."),
        ("h", "7.8 Reporting"),
        ("p", "The standards desk reports corrections to the editor-in-chief each month in the standards bulletin, "
              "and to the board each quarter."),
    ]


def cms_fields_txt():
    return """Web CMS revision export: field notes
File: cms_revisions_web_desks_2025-10_2026-09.csv
Prepared by Audience data at the request of Standards, 16 October 2026

Scope
One row per saved revision of each web-desk document that first went live between 1 October 2025 and
30 September 2026 (AEST), and of documents first saved in that period that never went live. Web desks:
Politics·national, Business·national, Sport·national, Culture·national, Politics·metro,
Sport·metro and Local·metro. The national and Brisbane CMS instances are combined. Saves after
30 September 2026 are not included.

Fields
doc_id             CMS document id.
desk_code          Owning desk (desk register codes).
doc_type           story, liveblog or post. A post is an entry in the live blog named in parent_doc,
                   with a headline of its own.
parent_doc         For posts, the doc_id of the live blog.
revision           Revision number within the document, from 1.
saved_at           Time of the save, UTC, to the minute.
status             Status recorded with the save: draft, scheduled, live or withdrawn.
publish_at         On a scheduled revision, the time set for the CMS to publish the document, UTC.
headline_sha1      First 12 characters of the SHA-1 of the headline text at that revision.
correction_note    Text of the correction notice shown with the document at that revision. The CMS copies the
                   note to every later revision until an editor clears it.
restored_from_doc  Set on documents recreated when the Brisbane instance was restored on 14 November 2025;
                   holds the doc_id of the document it was recreated from.
migrated_from      Set on documents moved from the previous CMS at the migration on 1 October 2025; holds the
                   previous system's document id.

Headline and body text are not part of this export.
"""


def bulletin_paras(h, b):
    return [
        ("title", "Standards bulletin"),
        ("small", "April 2026 | Issue 31 | From the standards desk to the editor-in-chief and desk editors"),
        ("h", "March in numbers"),
        ("p", "The web desks logged %d headline corrections and %d corrections to article text in March. Both "
              "figures cover the seven web desks, national and Brisbane." % (h, b)),
        ("h", "Titles and names"),
        ("p", "Several of March's corrections were to a person's title or role. The house style list of current "
              "titles was updated on 2 April and is linked from the CMS help page."),
        ("h", "Readers' editor"),
        ("p", "The quarterly readers' editor report is due on 20 April. Desk editors will get their section a week "
              "before."),
        ("small", "Internal. Standards desk."),
    ]


# ---------------------------------------------------------------------------------- the syndication agreement

def agreement_blocks():
    return [
        ("title", "Content syndication agreement"),
        ("meta", "Between Bightline News Pty Ltd (Bightline) and Newsfold Pty Ltd (Newsfold)"),
        ("meta", "Dated 1 July 2024 | Variation 1, 1 July 2025"),
        ("space", 3),
        ("h", "1. Definitions"),
        ("p", "<b>Articles</b> means the articles Bightline publishes on its national edition, and Brisbane edition "
              "sport and politics articles from 1 July 2025 (Variation 1). <b>Feed</b> means the structured feed of "
              "Articles described in Schedule 1. <b>Partner App</b> means the Newsfold news app on iOS, Android and "
              "the web."),
        ("h", "2. Licence"),
        ("p", "Bightline grants Newsfold a non-exclusive licence to display Articles from the Feed in the Partner "
              "App in Australia and New Zealand for the Term. Newsfold may not edit an Article, except to fit its "
              "layout, and may not display an Article after Bightline withdraws it from the Feed."),
        ("h", "3. Exclusions"),
        ("p", "Brisbane edition local news, app-only products (including Games, Puzzles, Recipes and Wellness) and "
              "any Article marked for subscribers only are excluded from the Feed."),
        ("h", "4. Attribution"),
        ("p", "Each Article shows the Bightline masthead and byline and links to the Article on Bightline's site."),
        ("h", "5. Commercial terms"),
        ("p", "Newsfold pays Bightline 50 per cent of net advertising revenue earned on Article pages in the Partner "
              "App, with a minimum guarantee of A$185,000 a year, paid quarterly in arrears."),
        ("h", "6. Reporting"),
        ("p", "Newsfold provides a monthly report of Article views and outbound clicks to Bightline's site, by "
              "Article, within ten business days of month end."),
        ("h", "7. Term and termination"),
        ("p", "The Term is three years from 1 July 2024. Either party may end the agreement on 90 days' written "
              "notice after 30 June 2026."),
        ("h", "8. General"),
        ("p", "This agreement is governed by the law of New South Wales. Each party keeps the terms confidential."),
        ("h", "Schedule 1: the Feed"),
        ("p", "Bightline makes the Feed available at an address it notifies to Newsfold. Newsfold polls the Feed at "
              "least every five minutes and removes withdrawn Articles within one hour."),
        ("space", 4),
        ("small", "Signed for Bightline News Pty Ltd by Lisa Jennings, Editor-in-chief, under delegation. "
                  "Signed for Newsfold Pty Ltd by its director."),
    ]


# ---------------------------------------------------------------------------------- the planning thread

def thread_eml():
    hdr = """From: Corey Cox <corey.cox@bightline.com.au>
To: Kayla Torres <kayla.torres@bightline.com.au>, Nina Franklin <nina.franklin@bightline.com.au>,
 Jason Anderson <jason.anderson@bightline.com.au>, Natalie Benjamin <natalie.benjamin@bightline.com.au>
Cc: Lisa Jennings <lisa.jennings@bightline.com.au>
Subject: Re: Squad placement 2027
Date: Thu, 15 Oct 2026 17:42:10 +1000
Message-ID: <CAB7q2kx4Lr8T@mail.bightline.com.au>
In-Reply-To: <CAB7q2kx3Vn1P@mail.bightline.com.au>
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 8bit

"""
    body = """Thanks all. Natalie, that folder is what I'll work from. I'll take one recommendation to the 4 November
meeting with a number against it. Lisa's office is bringing the dashboard view as usual.

Corey Cox
Managing editor

On Thu, 15 Oct 2026 at 16:05, Natalie Benjamin <natalie.benjamin@bightline.com.au> wrote:
> Exports are in the 2027 planning folder: pageviews by source and age band for October to September,
> the full headline test archive (app engine since 2019, web since the migration), the staff list as at
> Monday, the 2027 plan, the squad change log, the panel monthly file with its reference workbook, and
> the CMS revision export for the web desks that Standards asked for last month. The field reference is
> updated. The pageview extract is article pageviews only, so home pages are not in it.
>
> Natalie
>
> On Wed, 14 Oct 2026 at 11:20, Jason Anderson <jason.anderson@bightline.com.au> wrote:
>> Happy to go anywhere on the list, but the squad does its best work where tests run big and steady.
>> Business reminds me of our Puzzles year: big samples, clean reads. A small desk like Culture would
>> waste the year.
>>
>> Jason
>>
>> On Wed, 14 Oct 2026 at 09:02, Nina Franklin <nina.franklin@bightline.com.au> wrote:
>>> Every winner the squad ships clears 95 per cent. A winner is a winner. The dashboard is the honest
>>> record of what testing does for us.
>>>
>>> Nina
>>>
>>> On Tue, 13 Oct 2026 at 16:48, Kayla Torres <kayla.torres@bightline.com.au> wrote:
>>>> Same view as last year: it goes where the readers are. The panel numbers are in the folder.
>>>>
>>>> Kayla
>>>>
>>>> On Tue, 13 Oct 2026 at 08:31, Corey Cox <corey.cox@bightline.com.au> wrote:
>>>>> We place the squad for 2027 at the 4 November planning meeting. I want a recommendation I can
>>>>> defend: the desk, and what the squad adds there in clicks. Send me whatever you think matters.
>>>>>
>>>>> Corey

--
Bightline News | Internal correspondence. Please do not forward outside the newsroom.
"""
    return hdr + body
