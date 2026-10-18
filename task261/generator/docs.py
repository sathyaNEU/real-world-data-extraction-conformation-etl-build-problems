"""The pack's documents: the survey's public-use user guide and results bulletin, Kelvane Life's brief for the 2027
retirement range, the Retirement Income Account PDS, the lifetime annuity key facts sheet, the data dictionary for the
retirement book extracts and the 2026 customer research summary."""
from __future__ import annotations

import datetime as dt

import numpy as np
from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                   # noqa: E402
from reportlab.lib.pagesizes import A4                                             # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                    # noqa: E402
from reportlab.lib.units import mm                                                 # noqa: E402
from reportlab.pdfbase import pdfmetrics                                           # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                       # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K   # noqa: E402
import est as E      # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
for nm, f in (("Serif", "LiberationSerif-Regular"), ("Serif-B", "LiberationSerif-Bold"), ("Serif-I", "LiberationSerif-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif-I", boldItalic="Serif-B")
INK, GREY, RULE = colors.HexColor("#1c2228"), colors.HexColor("#5a646d"), colors.HexColor("#b3bcc4")


def styles(font, accent):
    body = ParagraphStyle("b", fontName=font, fontSize=9.6, leading=13.4, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName=font + "-B", fontSize=15.5, leading=19.5, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName=font + "-B", fontSize=10.6, leading=14, textColor=INK, spaceBefore=8,
                          spaceAfter=3),
        meta=ParagraphStyle("m", fontName=font, fontSize=8.3, leading=11, textColor=GREY, spaceAfter=9),
        note=ParagraphStyle("n", fontName=font, fontSize=7.8, leading=10, textColor=GREY, spaceBefore=6),
        cell=ParagraphStyle("c", fontName=font, fontSize=8.6, leading=11.2, textColor=INK),
        cellb=ParagraphStyle("cb", fontName=font + "-B", fontSize=8.6, leading=11.2, textColor=INK),
        indent=ParagraphStyle("i", parent=body, leftIndent=14))


def _doc(path, title, author):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=21 * mm, rightMargin=21 * mm, topMargin=22 * mm,
                             bottomMargin=19 * mm, title=title, author=author, subject="", creator="", producer="")


def _frame(left, right, font="Sans"):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont(font, 7.4)
        canvas.drawString(21 * mm, A4[1] - 12 * mm, left)
        canvas.drawRightString(A4[0] - 21 * mm, A4[1] - 12 * mm, right)
        canvas.drawRightString(A4[0] - 21 * mm, 10.5 * mm, "Page %d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, align_right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], hAlign="LEFT")
    style = [("LINEBELOW", (0, 0), (-1, 0), 0.7, INK), ("LINEBELOW", (0, 1), (-1, -1), 0.25, RULE),
             ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 2.6),
             ("BOTTOMPADDING", (0, 0), (-1, -1), 2.6)]
    t.setStyle(TableStyle(style))
    return t


def money(x):
    return "{:,.0f}".format(x)


# ---------------------------------------------------------------------------------------------- the survey
def bulletin_figures(d):
    """The survey's own published estimates (by the reference person's age, by state, by tenure), on the public file."""
    sv = E.Survey(d["nw"], d["wgt"], d["repw"])
    out = {"age": [], "state": [], "tenure": []}
    # the bulletin's own age groups (the centre's ten-year bands from 30), by the reference person's age
    ref = np.minimum(d["ref"], 85)
    for name, lo, hi in (("Under 30", 0, 29), ("30 to 39", 30, 39), ("40 to 49", 40, 49), ("50 to 59", 50, 59),
                         ("60 to 69", 60, 69), ("70 and over", 70, 120)):
        m = (ref >= lo) & (ref <= hi)
        est, rep = sv.median(m)
        th, u, b, t, se = sv.combine(est, rep)
        out["age"].append((name, th, se / th, float(d["wgt"][m].sum())))
    for code in ("NSW", "VIC", "QLD", "WA", "SA", "TAS", "ACT", "NT"):
        m = d["state"] == code
        est, rep = sv.median(m)
        th, u, b, t, se = sv.combine(est, rep)
        out["state"].append((code, th, se / th, float(d["wgt"][m].sum())))
    for ten in ("Owner without a mortgage", "Owner with a mortgage", "Renter, private landlord",
                "Renter, state housing authority"):
        m = d["tenure"] == ten
        est, rep = sv.median(m)
        th, u, b, t, se = sv.combine(est, rep)
        out["tenure"].append((ten, th, se / th, float(d["wgt"][m].sum())))
    est, rep = sv.median(d["state"] == "QLD")
    out["example"] = dict(est=est, rep=rep, comb=sv.combine(est, rep))
    est, rep = sv.median(np.ones(len(d["wgt"]), bool))
    out["all"] = sv.combine(est, rep)
    return out


def write_user_guide(path, d, fig):
    S = styles("Serif", colors.HexColor("#3b4d2a"))
    ex = fig["example"]
    th, u, b, t, se = ex["comb"]
    n_hh = len(d["hhid"])
    n_p = len(d["persons"])
    story = [Paragraph("National Household Wealth Survey 2025: public-use file user guide", S["h1"]),
             Paragraph("%s. Release 1.0, %s. Contact: data services, %s." % (
                 K.CENTRE, K.RELEASE_DATE.strftime("%-d %B %Y"), K.CENTRE), S["meta"])]
    sec = [
        ("1. The survey", [
            "The 2025 wave of the National Household Wealth Survey interviewed %s households in private dwellings in "
            "every state and territory between 3 March and 31 October 2025. The sample was selected in two stages: the "
            "country is divided into 60 strata by state and area type, two areas were selected in each stratum with "
            "probability proportional to their number of dwellings, and about 50 households were interviewed in each "
            "selected area. Households in non-private dwellings (aged care, hostels, prisons) are out of scope." % (
                money(n_hh))]),
        ("2. The release", [
            "The public-use release has three files, joined on the household identifier <i>hhid</i>: the household "
            "summary extract (one row for each household on each of five implicates, %s rows); the person file (one "
            "row for each person, %s rows); and the replicate weight file (one row for each household with its 200 "
            "replicate weights). Stratum and area codes are not released. Ages are top-coded at 85, and the household's "
            "location is released as the state only." % (money(5 * n_hh), money(n_p))]),
        ("3. Households and persons", [
            "The reference person (relationship code 1) is the household member with the highest personal income "
            "from all sources, the elder where incomes tie. The person file gives each member's relationship to the "
            "reference person: 1 reference person; 2 husband, wife or registered partner; 3 de facto partner; 4 child "
            "under 15; 5 dependent student aged 15 to 24; 6 non-dependent child; 7 parent of the reference person; 8 "
            "other relative; 9 unrelated person. <i>hrp_age</i> and <i>hrp_sex</i> on the summary extract are the "
            "reference person's; <i>couple</i> is Y where the reference person has a partner (code 2 or 3) in the "
            "household."]),
        ("4. Wealth", [
            "<i>assets</i> is the value of the household's owner-occupied home and other property, superannuation, "
            "deposits, shares and other financial assets, business interests, vehicles and contents; <i>debts</i> is "
            "the balance of every mortgage, property loan, personal loan, credit card and study debt owed by a member. "
            "<i>networth</i> is assets less debts and is negative where debts exceed assets. <i>house</i> is the "
            "owner-occupied home's value and <i>super</i> the superannuation balances of all members. All amounts are "
            "in Australian dollars at the date of interview, whole dollars."]),
        ("5. Imputation", [
            "Where a household did not report the value of a wealth item, the value was imputed from households alike "
            "in age, income, tenure and state, five times over. The summary extract carries the five implicates "
            "(<i>imp</i> 1 to 5): a reported item is the same on every implicate and an imputed one differs. About a "
            "quarter of households have at least one imputed wealth item. Use all five implicates for every estimate."]),
        ("6. Weights", [
            "<i>wgt</i> is the household's final weight, the number of households it represents, benchmarked to %s "
            "households in private dwellings at 30 June 2025. It is the same on a household's five implicate rows. "
            "Every estimate must be weighted." % money(K.POPULATION_HOUSEHOLDS)]),
        ("7. Estimates and their standard errors", [
            "7.1 An estimate is computed with <i>wgt</i> on each of the five implicates; the five are averaged.",
            "7.2 Its standard error has two parts. The sampling variance: on implicate 1, compute the estimate again "
            "with each of the 200 replicate weights in place of <i>wgt</i>; the sampling variance is the average of "
            "the 200 squared differences between the replicate estimates and the implicate-1 estimate. The imputation "
            "variance: the variance (divisor 4) of the five implicate estimates. The total variance is the sampling "
            "variance plus 1.2 times the imputation variance, and the standard error is its square root. The relative "
            "standard error (RSE) is the standard error divided by the estimate.",
            "7.3 Each replicate keeps one of the two selected areas in every stratum, chosen at random, and doubles "
            "the weights of its households; households in the other area have weight zero in that replicate.",
            "7.4 Estimates with an RSE of 25 per cent or more are subject to high sampling variability and should be "
            "used with caution."]),
    ]
    for head, paras in sec:
        story.append(Paragraph(head, S["h2"]))
        for p in paras:
            story.append(Paragraph(p, S["body"]))
    story.append(Paragraph("Worked example: median net worth of households in Queensland", S["h2"]))
    rows = [["Step", "Result"]] + [["Median on implicate %d" % (m + 1), "$" + money(ex["est"][m])] for m in range(5)]
    rows += [["Estimate (average of the five)", "$" + money(th)],
             ["Sampling variance (200 replicates, implicate 1)", "%.4g" % u],
             ["Imputation variance (divisor 4)", "%.4g" % b],
             ["Total variance (sampling + 1.2 x imputation)", "%.4g" % t],
             ["Standard error", "$" + money(se)], ["Relative standard error", "%.1f per cent" % (100 * se / th)]]
    story.append(_table(S, rows, [95, 45]))
    story.append(Paragraph("A median is the value at which the cumulative weight of households, in ascending order of "
                           "net worth, first reaches half the total weight.", S["note"]))
    doc = _doc(path, "NHWS 2025 public-use file user guide", K.CENTRE)
    doc.build(story, onFirstPage=_frame(K.CENTRE, "NHWS 2025 user guide", "Serif"),
              onLaterPages=_frame(K.CENTRE, "NHWS 2025 user guide", "Serif"))


def write_bulletin(path, d, fig):
    import openpyxl
    from openpyxl.styles import Alignment, Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Notes"
    notes = [
        "National Household Wealth Survey 2025: results bulletin tables",
        "%s, released %s." % (K.CENTRE, K.RELEASE_DATE.strftime("%-d %B %Y")),
        "",
        "Table 1 gives household net worth by the age of the household reference person (user guide, section 3).",
        "Medians are in thousands of dollars, rounded to the nearest thousand. RSE: relative standard error (user guide, 7.2).",
        "Households: weighted number of households, thousands. Estimates with an RSE of 25 per cent or more should be used with caution.",
        "Estimates are from the public-use release.",
    ]
    for i, t in enumerate(notes, 1):
        if t:
            ws.cell(row=i, column=1, value=t)
    ws["A1"].font = Font(bold=True, size=12)
    ws.column_dimensions["A"].width = 118
    for title, key, label in (("Table 1 By age", "age", "Age of reference person"), ("Table 2 By state", "state", "State"),
                              ("Table 3 By tenure", "tenure", "Tenure")):
        s = wb.create_sheet(title)
        s.append(["Median household net worth, 2025, by %s" % label.lower()])
        s["A1"].font = Font(bold=True)
        s.append([])
        s.append([label, "Households ('000)", "Median net worth ($'000)", "RSE (%)"])
        for c in s[3]:
            c.font = Font(bold=True)
            c.alignment = Alignment(wrap_text=True, vertical="top")
        for name, th, rse, hh in fig[key]:
            s.append([name, round(hh / 1000, 1), int(round(th / 1000)), round(100 * rse, 1)])
        th, u, b, t, se = fig["all"]
        s.append(["All households", round(float(d["wgt"].sum()) / 1000, 1), int(round(th / 1000)), round(100 * se / th, 1)])
        s.column_dimensions["A"].width = 34
        for col in "BCD":
            s.column_dimensions[col].width = 16
        for row in s.iter_rows(min_row=4, max_row=s.max_row):
            row[1].number_format = "#,##0.0"
            row[2].number_format = "#,##0"
            row[3].number_format = "0.0"
        s.freeze_panes = "A4"
    wb.save(path)


# ---------------------------------------------------------------------------------------------- Kelvane Life
def write_brief(path):
    import docx
    from docx.shared import Pt
    doc = docx.Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    head = doc.add_paragraph()
    r = head.add_run("Kelvane Life | Retirement Products")
    r.bold = True
    r.font.size = Pt(12)
    for k, v in (("To", "Insights and Analytics"), ("From", "%s, Head of Retirement Products" % K.PEOPLE["head"]),
                 ("Copy", "%s, Chair, Retirement Product Committee" % K.PEOPLE["chair"]),
                 ("Date", K.BRIEF_DATE.strftime("%-d %B %Y")),
                 ("Subject", "2027 retirement range: segment structure for the committee on 27 January")):
        p = doc.add_paragraph()
        a = p.add_run(k + ": ")
        a.bold = True
        p.add_run(v)
        p.paragraph_format.space_after = Pt(0)
    doc.add_paragraph()
    paras = [
        "The retirement product committee meets on %s to set the structure of the 2027 retirement range. As agreed in "
        "November, the range will have one product for each segment, and each segment is a run of neighbouring age "
        "groups. I need a recommended structure and the evidence for every boundary in it." % (
            K.COMMITTEE.strftime("%-d %B")),
        "The age groups are the six we used in the strategy paper: under 35, 35 to 44, 45 to 54, 55 to 64, 65 to 74, and "
        "75 and over. A household is placed by the age of the older of its reference person and partner; a household "
        "with no partner is placed by its reference person.",
        "The committee's rule: two neighbouring age groups stay in separate segments only where the difference between "
        "their median household net worth is more than 1.96 times the standard error of that difference. Where it is "
        "not, they share a segment, and a segment runs across every neighbouring group no such difference separates.",
        "The evidence is the public-use release of the National Household Wealth Survey 2025 (the %s, September 2026), "
        "which is in the folder with its user guide and results bulletin. Medians are weighted, and standard errors are "
        "estimated as the survey's user guide sets out." % K.CENTRE,
        "The committee will also want to see our own retirement income customers in the three groups from 55, placed "
        "the same way. The client register, the Retirement Income Account and annuity extracts and the data dictionary "
        "are in the folder; the PDS and the annuity key facts sheet are there for the product terms.",
        "Please send the paper, the workbook behind it and the chart by %s so I can circulate them with the committee "
        "papers." % (K.COMMITTEE - dt.timedelta(days=6)).strftime("%-d %B"),
    ]
    for t in paras:
        p = doc.add_paragraph(t)
        p.paragraph_format.space_after = Pt(6)
    p = doc.add_paragraph(K.PEOPLE["head"])
    p.paragraph_format.space_before = Pt(8)
    doc.core_properties.author = K.PEOPLE["head"]
    doc.save(path)


def write_pds(path):
    S = styles("Sans", colors.HexColor("#0f4c5c"))
    story = [Paragraph("Retirement Income Account: Product Disclosure Statement", S["h1"]),
             Paragraph("Issued by %s as trustee of the Kelvane Super Fund. Issue date 1 July 2026." % K.TRUSTEE,
                       S["meta"])]
    sec = [
        ("1. About the Retirement Income Account", [
            "The Retirement Income Account is an account-based pension: you roll your superannuation into it and we pay "
            "you a regular income from your account balance, which stays invested. Its value moves with the returns on "
            "your investment option, the payments you take and the fees we deduct.",
            "If you have reached your preservation age but are still working, you can open it as a transition to "
            "retirement pension. A transition to retirement pension is paid within a maximum of 10 per cent of your "
            "balance each year."]),
        ("2. Your payments", [
            "You choose how much you are paid each financial year, at least the minimum the law sets for your age, and "
            "how often (fortnightly, monthly, quarterly or annually). We set the amount on 1 July each year."]),
    ]
    for head, paras in sec:
        story.append(Paragraph(head, S["h2"]))
        for p in paras:
            story.append(Paragraph(p, S["body"]))
    rows = [["Your age on 1 July", "Minimum payment, per cent of your balance"], ["Under 65", "4"], ["65 to 74", "5"],
            ["75 to 79", "6"], ["80 to 84", "7"], ["85 to 89", "9"], ["90 to 94", "11"], ["95 and over", "14"]]
    story.append(_table(S, rows, [55, 75]))
    sec = [
        ("3. Investment options", [
            "Balanced (the default), Growth, Conservative and Cash. You can switch at any time; switches are processed at "
            "the next unit price."]),
        ("4. Fees and costs", [
            "Administration fee: $78 a year plus 0.18 per cent of your balance, capped at $900 a year. Investment fees "
            "and costs depend on the option, from 0.05 per cent (Cash) to 0.74 per cent (Growth) a year."]),
        ("5. Nominating beneficiaries", [
            "You can nominate a reversionary beneficiary: your spouse, or a child who is your dependant. If you do, your "
            "pension continues to them automatically when you die, from the date of your death, on the same terms. You "
            "can change or remove a reversionary nomination at any time while you are alive.",
            "If you have not nominated a reversionary beneficiary, your pension stops when you die and your account "
            "balance is paid as a death benefit: to the people in your binding nomination if it is valid, or otherwise "
            "as the trustee decides among your dependants and your estate."]),
        ("6. Tax", [
            "Investment earnings on a pension in the retirement phase are tax-free. Payments are tax-free from age 60; "
            "before 60, part of each payment may be taxed and we withhold tax as the law requires."]),
        ("7. Contact", ["Through your financial adviser, or the member centre in Kelvane Online."]),
    ]
    for head, paras in sec:
        story.append(Paragraph(head, S["h2"]))
        for p in paras:
            story.append(Paragraph(p, S["body"]))
    doc = _doc(path, "Retirement Income Account PDS", K.TRUSTEE)
    doc.build(story, onFirstPage=_frame(K.TRUSTEE, "Retirement Income Account PDS, 1 July 2026"),
              onLaterPages=_frame(K.TRUSTEE, "Retirement Income Account PDS, 1 July 2026"))


def write_key_facts(path):
    S = styles("Sans", colors.HexColor("#5b2a4a"))
    story = [Paragraph("Lifetime Annuity: key facts", S["h1"]),
             Paragraph("%s. This sheet summarises the product; the policy document governs. Updated 1 November 2026."
                       % K.INSURER_LEGAL, S["meta"])]
    sec = [
        ("What it is", [
            "A lifetime annuity pays you a regular income for the rest of your life in exchange for a single purchase "
            "amount, which you can pay from your superannuation or your own savings."]),
        ("When payments start", [
            "Your income starts on the start date and is paid in arrears, monthly, quarterly, half-yearly or yearly as "
            "you choose. With a deferred start, your income starts at age 80 or 85 instead; nothing is paid before then."]),
        ("Indexation", [
            "Choose CPI-linked payments, a fixed increase of 2.5 per cent a year, or level payments. Increases apply from "
            "each anniversary of the start date. CPI-linked payments rise by the change in the Consumer Price Index over "
            "the twelve months to the latest quarter published before the anniversary."]),
    ]
    for head, paras in sec:
        story.append(Paragraph(head, S["h2"]))
        for p in paras:
            story.append(Paragraph(p, S["body"]))
    rows = [["Anniversaries falling", "CPI-linked", "Fixed"],
            ["1 August to 31 October 2026", "3.4 per cent", "2.5 per cent"],
            ["1 November 2026 to 31 January 2027", "3.1 per cent", "2.5 per cent"]]
    story.append(_table(S, rows, [70, 35, 35]))
    sec = [
        ("A reversionary annuitant", [
            "You can name your spouse or partner as a reversionary annuitant and choose a reversion percentage from 50 to "
            "90 per cent. After your death, payments continue to your reversionary annuitant at that percentage of the "
            "amount you were being paid, for the rest of their life, with indexation as before."]),
        ("If you die", [
            "Without a reversionary annuitant, payments stop when you die. If you die within 15 years of the start date "
            "we pay a lump sum death benefit to your estate, reducing each year to nil at 15 years."]),
        ("Cooling off and withdrawal", [
            "You have 14 days from the start date to cancel and receive the purchase amount back. After that, the annuity "
            "cannot be withdrawn except during the death benefit period."]),
    ]
    for head, paras in sec:
        story.append(Paragraph(head, S["h2"]))
        for p in paras:
            story.append(Paragraph(p, S["body"]))
    doc = _doc(path, "Lifetime Annuity key facts", K.INSURER_LEGAL)
    doc.build(story, onFirstPage=_frame(K.INSURER_LEGAL, "Lifetime Annuity: key facts"),
              onLaterPages=_frame(K.INSURER_LEGAL, "Lifetime Annuity: key facts"))


DICT = {
    K.CRM: ("Client register, pulled 12 January 2027: one row per client record, everyone who holds or has held a Kelvane "
            "product or is a life on one.", [
                ("client_id", "Kelvane client number"),
                ("household_id", "Household number; clients who are partners share one. A household's partners at "
                                 "any date, our clients or not, are those alive on that date"),
                ("date_of_birth", "Date of birth"),
                ("sex", "M or F"),
                ("state", "State of the postal address"),
                ("marital_status", "As the client last told us"),
                ("client_since", "Date the client record was opened"),
                ("status", "Active; Deceased (we have been told of the client's death); Merged (a duplicate record retired into another)"),
                ("date_of_death", "Date of death, where we have been told"),
                ("merged_into", "For a merged record, the client number it was merged into")]),
    K.RIA: ("Retirement Income Account pensions open in the fund's administration system at 31 December 2026, from the "
            "period-end run: one row per pension account.", [
                ("account_no", "Pension account number"),
                ("member_id", "The member's client number as the administration system holds it"),
                ("pension_type", "ABP (account-based pension) or TTR (transition to retirement pension)"),
                ("commenced", "Date the pension started"),
                ("investment_option", "Balanced, Growth, Conservative or Cash"),
                ("payment_frequency", "Fortnightly, Monthly, Quarterly or Annually"),
                ("annual_payment_2026_27", "Annual payment set for the 2026-27 financial year, dollars"),
                ("balance_31_12_2026", "Balance at 31 December 2026, dollars")]),
    K.NOMS: ("Nominations current on each Retirement Income Account pension at 31 December 2026: one row per nominee. "
             "A member's spouse or de facto partner who is not our client is known to us only from these nominations, "
             "whatever their type. "
             "Nominee details are as the member gave them; the fund does not update them, and a nomination stays current "
             "until the member replaces or revokes it.", [
                ("account_no", "Pension account number"),
                ("nomination_type", "Reversionary, Binding, Non-lapsing binding or Non-binding"),
                ("nominee_name", "As written on the nomination"),
                ("nominee_date_of_birth", "As written on the nomination; blank for the legal personal representative"),
                ("relationship", "The nominee's relationship to the member, as the member gave it: Spouse (the member's "
                                 "husband or wife), De facto partner (a person the member lives with as a couple), Child, "
                                 "or Legal personal representative"),
                ("share_percent", "Share of the benefit nominated"),
                ("effective_from", "Date the nomination took effect")]),
    K.ANN: ("Lifetime annuity lives in the 31 December 2026 valuation, with contracts that began since: one row per life "
            "on each contract, pulled 12 January 2027. Amounts and statuses are as at the pull.", [
                ("contract_no", "Annuity contract number"),
                ("life_no", "1 for the annuitant; 2 for a reversionary annuitant"),
                ("client_id", "The life's client number"),
                ("date_of_birth", "The life's date of birth, as verified at purchase"),
                ("sex", "M or F"),
                ("commenced", "The annuity's start date"),
                ("payments_start", "The date the annuity's income starts; later than the start date for a deferred annuity"),
                ("indexation", "CPI, Fixed 2.5% or Level"),
                ("payment_frequency", "Monthly, Quarterly, Half-yearly or Yearly"),
                ("reversion_percent", "For a contract with a reversionary annuitant, the reversion percentage"),
                ("annual_amount", "Annual amount of annuity for the life, dollars"),
                ("life_status", "Alive or Deceased"),
                ("date_of_death", "Date of death, where we have been told")]),
}


def write_dictionary(path):
    import openpyxl
    from openpyxl.styles import Alignment, Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "About"
    ws.append(["Retirement book extracts: data dictionary"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Insights and Analytics, %s. Owner of the annuity valuation listing: %s, Senior Actuary, Valuations." % (
        K.INSURER, K.PEOPLE["actuary"])])
    ws.append([])
    ws.append(["File", "What it holds"])
    for c in ws[4]:
        c.font = Font(bold=True)
    for f, (about, _) in DICT.items():
        ws.append([f, about])
    ws.column_dimensions["A"].width = 40
    ws.column_dimensions["B"].width = 110
    for row in ws.iter_rows(min_row=5):
        row[1].alignment = Alignment(wrap_text=True, vertical="top")
    for f, (about, cols) in DICT.items():
        s = wb.create_sheet(f.replace(".csv", "")[:31])
        s.append(["Column", "Meaning"])
        for c in s[1]:
            c.font = Font(bold=True)
        for c, m in cols:
            s.append([c, m])
        s.column_dimensions["A"].width = 26
        s.column_dimensions["B"].width = 100
        s.freeze_panes = "A2"
    wb.save(path)


def write_research(path):
    S = styles("Sans", colors.HexColor("#2f4858"))
    story = [Paragraph("What our retirement customers told us: 2026 research summary", S["h1"]),
             Paragraph("%s, Customer Insights. Online survey of 1,214 Retirement Income Account and Lifetime Annuity "
                       "customers aged 55 and over, 4 to 22 August 2026; weighted to the customer base by age and product." %
                       K.INSURER, S["meta"])]
    story.append(Paragraph("What customers want from a retirement product", S["h2"]))
    story.append(Paragraph("Customers chose up to three features as most important. The ordering is the same in every "
                           "age group; the gap between income certainty and access to capital widens with age.", S["body"]))
    rows = [["Feature (per cent choosing it)", "55 to 64", "65 to 74", "75 and over"],
            ["An income guaranteed for life", "47", "58", "66"],
            ["Access to my capital when I need it", "61", "52", "38"],
            ["Income continuing to my partner after I die", "39", "44", "41"],
            ["Help with aged care costs", "12", "24", "45"],
            ["Low fees", "44", "37", "29"],
            ["Choice of investments", "33", "21", "11"]]
    story.append(_table(S, rows, [76, 26, 26, 26]))
    story.append(Paragraph("Who answered", S["h2"]))
    story.append(Paragraph("Respondents by age group: 55 to 64, 298; 65 to 74, 571; 75 and over, 345. Two in three held a "
                           "Retirement Income Account only, one in five a Lifetime Annuity only and the rest both.",
                           S["body"]))
    story.append(Paragraph("Notes", S["h2"]))
    story.append(Paragraph("Percentages are rounded and do not sum to 100 because customers could choose up to three "
                           "features. The survey asked about preferences, not about customers' finances.", S["body"]))
    doc = _doc(path, "Retirement customer research 2026", K.INSURER)
    doc.build(story, onFirstPage=_frame(K.INSURER + " Customer Insights", "Research summary, September 2026"),
              onLaterPages=_frame(K.INSURER + " Customer Insights", "Research summary, September 2026"))
