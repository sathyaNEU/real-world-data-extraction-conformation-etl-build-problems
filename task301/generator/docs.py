"""The pack's documents: the department's appraisal guidance (DOCX), the five 2027 proposals (PDF), the Complemento
Familiar's consolidated rules (PDF), the department's 2025 coverage report (PDF) and the statistics institute's
published main results of the 2026 survey (PDF). Each states facts about the world and the organisation's own
definitions; none describes a file or a column."""
import io_util as IO
import params as P

DEPT = "Consejería de Derechos Sociales y Familias"
IEV = "Instituto de Estadística de Valdemora"


def euro(x, nd=0):
    s = "{:,.{n}f}".format(x, n=nd)
    return "€" + s


def guidance(path, line):
    paras = [
        ("title", "Appraisal of the 2027 child poverty measures"),
        ("sub", "%s, Dirección General de Planificación y Evaluación. Guidance issued 15 October 2026. English "
                "working version." % DEPT),
        ("h", "1. Purpose"),
        ("p", "The 2027 budget funds one measure from the department's proposals against child poverty. The cabinet "
              "compares the proposals on the figure set out in section 2, so that every measure is appraised on the "
              "same footing. The appraisal uses the regional living conditions survey (ECVV) of 2026, which records "
              "the incomes households received in 2025, and the department's own benefit records."),
        ("h", "2. The figure"),
        ("p", "2.1 Each measure is appraised on the number of children it brings above the poverty line in calendar "
              "2027."),
        ("h", "3. Definitions"),
        ("p", "3.1 The poverty line for 2027 is %s a year for each equivalent adult." % euro(line)),
        ("p", "3.2 A household's equivalised income is its disposable income divided by its number of equivalent "
              "adults on the modified OECD scale: 1 for the first member aged 14 or over, 0.5 for each other member "
              "aged 14 or over and 0.3 for each member under 14. A member's age is taken as 2026 less the year of "
              "birth."),
        ("p", "3.3 A household's disposable income for 2027, before any of the measures, is its 2025 disposable "
              "income in the ECVV 2026 increased by 6.1 per cent."),
        ("p", "3.4 A child is a household member born in 2009 or later."),
        ("p", "3.5 A measure brings a child above the line when the child's household has an equivalised income for "
              "2027 below the line without the measure, and at or above the line once the measure's payments that "
              "the household receives during 2027 are added."),
        ("p", "3.6 Counts of children are grossed up with the ECVV 2026 household weight; every member of a "
              "household carries its household's weight."),
        ("p", "3.7 Where a measure's eligibility turns on income per equivalent adult, the appraisal applies the "
              "test to the household: its 2025 disposable income in the ECVV 2026, less any Complemento Familiar it "
              "received in 2025, divided by its equivalent adults under 3.2."),
        ("p", "3.8 The measures' payments are counted as additional income. The Ministry has confirmed that no "
              "national benefit is reduced by them, and none of the regional benefits is reduced by another."),
        ("h", "4. What the cabinet receives"),
        ("p", "4.1 A note of no more than two pages recommending one measure, with the number of children it brings "
              "above the line in 2027 for the region and for each province."),
        ("p", "4.2 Figures of children are given to the nearest hundred."),
        ("h", "5. Contacts"),
        ("p", "Servicio de Estudios y Evaluación, Dirección General de Planificación y Evaluación."),
    ]
    IO.write_docx(path, "Appraisal of the 2027 child poverty measures", paras,
                  ("Servicio de Estudios", "Servicio de Estudios", "2026-10-15T08:30:00Z", "2026-10-15T12:05:00Z",
                   "Appraisal of the 2027 child poverty measures", DEPT))


def proposals(path, line, costs):
    rows = [["Measure", "Who it covers", "Amount", "How families receive it", "Cost in 2027 if every family "
             "covered received it (€ million)"],
            ["A. Prestación Infancia Directa",
             "Families with children whose household gross income on their 2025 personal income tax returns was "
             "below %s" % euro(P.A_INCOME_LIMIT),
             "%s a month per child" % euro(P.A_RATE),
             "Paid automatically from January 2027 by the Agencia Tributaria de Valdemora into the account on the "
             "family's 2025 return; no application. Families who filed no 2025 return are not reached in 2027.",
             "%.1f" % costs["A"]],
            ["B. Ayuda a la Crianza",
             "Families with children whose computable income per equivalent adult, measured as for the Complemento "
             "Familiar, is below the 2027 poverty line",
             "%s a month per child" % euro(P.B_RATE),
             "Families apply on the department's portal from 1 January 2027. The Complemento Familiar's rules on "
             "decisions and payment apply.",
             "%.1f" % costs["B"]],
            ["C. Complemento Familiar: higher limit",
             "Raises the Complemento Familiar's income limit from %s to %s of computable income per "
             "equivalent adult from 1 January 2027" % (euro(P.CFV_LIMIT), euro(P.C_LIMIT)),
             "€100 a month per child, as now",
             "Families newly within the limit claim the Complemento in the usual way.",
             "%.1f" % costs["C"]],
            ["D. Suplemento de Alquiler con Hijos",
             "Families with children who rent their home, at market or reduced rent, whose computable income per "
             "equivalent adult is below the 2027 poverty line",
             "%s a month per child" % euro(P.D_RATE),
             "Families apply on the department's portal from 1 January 2027. The Complemento Familiar's rules on "
             "decisions and payment apply.",
             "%.1f" % costs["D"]],
            ["E. Complemento Familiar: higher amount",
             "Families receiving the Complemento Familiar",
             "%s a month more per child" % euro(P.E_RATE),
             "Paid automatically with the Complemento from January 2027.",
             "%.1f" % costs["E"]]]
    from reportlab.lib.units import mm
    blocks = [
        ("title", "Measures against child poverty for the 2027 budget: proposals to the cabinet"),
        ("sub", "%s. 28 October 2026. English working version." % DEPT),
        ("p", "The cabinet has asked the department for one new measure against child poverty in the 2027 budget. "
              "The department proposes the five measures below. Each would start in January 2027 and run for the "
              "whole year. Costs are the department's usual costing: the payments if every family a measure covers "
              "received it for all of 2027, grossed up from the ECVV 2026."),
        ("table", rows),
        ("h", "Notes on the measures"),
        ("p", "A. The regional tax agency already holds each family's 2025 return and bank account, so the payment "
              "can start in January without a claim. The income test is on gross income, before tax."),
        ("p", "B. A new payment open to every family with children below the poverty line, administered by the "
              "staff who run the Complemento Familiar."),
        ("p", "C. The Complemento Familiar is the department's established payment for families with children on "
              "low incomes. The higher limit brings families up to %s of computable income per equivalent adult "
              "within it." % euro(P.C_LIMIT)),
        ("p", "D. Families renting their home carry the highest housing costs; the supplement is paid per child and "
              "follows the same income test as B."),
        ("p", "E. A higher amount for the families the Complemento already reaches."),
        ("p", "In every measure a child is a member of the family born in 2009 or later, as in the appraisal "
              "guidance."),
        ("p", "Computable income per equivalent adult is defined in the Complemento Familiar's rules. The 2027 "
              "poverty line is the one in the department's appraisal guidance of 15 October 2026 (%s a year for "
              "each equivalent adult)." % euro(line)),
    ]
    IO.write_pdf(path, "Measures against child poverty for the 2027 budget", DEPT, "Servicio de Estudios", blocks,
                 "%s - Proposals 2027" % DEPT, "D:20261028101500+01'00'", "D:20261028101500+01'00'",
                 colw={5: [32 * mm, 42 * mm, 24 * mm, 50 * mm, 22 * mm]})


def rules(path):
    blocks = [
        ("title", "Complemento Familiar Valdemorense: rules"),
        ("sub", "Consolidated text as in force on 1 October 2026 (Decree 118/2022, as amended). %s. English working "
                "version." % DEPT),
        ("h", "1. Purpose"),
        ("p", "The Complemento Familiar supports families with children on low incomes who live in the Comunidad de "
              "Valdemora."),
        ("h", "2. Who is entitled"),
        ("p", "2.1 A family is entitled when at least one child under 18 lives with it in the Comunidad de Valdemora "
              "and its computable income per equivalent adult is below €8,400 a year."),
        ("p", "2.2 A family is the claimant, the claimant's spouse or partner and the children who live with them."),
        ("h", "3. Computable income"),
        ("p", "3.1 Computable income is the family's net income in the latest tax year whose returns have closed when "
              "the claim or review is decided, excluding the Complemento Familiar itself."),
        ("p", "3.2 It is divided by the family's equivalent adults on the modified OECD scale (1 for the first member "
              "aged 14 or over, 0.5 for each other member aged 14 or over, 0.3 for each member under 14)."),
        ("h", "4. Amount"),
        ("p", "€100 a month for each child under 18."),
        ("h", "5. Claims and decisions"),
        ("p", "5.1 Families claim on the department's portal or at any of its provincial offices in Valdemora, "
              "Cuenca del Arlés and Albadía."),
        ("p", "5.2 A provincial office decides each claim. A refusal may be appealed within one month of the "
              "decision."),
        ("h", "6. Payment"),
        ("p", "6.1 The Complemento is paid monthly from the month after the month in which the claim is decided. It "
              "is not paid for any earlier month."),
        ("p", "6.2 A claim granted on appeal is paid from the month after the month of the appeal decision."),
        ("p", "6.3 One Complemento is paid to each family."),
        ("h", "7. Reviews"),
        ("p", "7.1 Every award is reviewed twelve months after its first month of payment, on the latest closed tax "
              "year. A renewal takes effect from the review month."),
        ("p", "7.2 Where documents asked for at a review have not arrived, payment is suspended from the review "
              "month. If they arrive within three months the suspension is lifted and the suspended months are paid "
              "with the next monthly payment; if not, the award is extinguished from the review month."),
        ("h", "8. Changes of circumstances"),
        ("p", "Families report a birth, a child reaching 18 and a change of address within one month. A birth raises "
              "the amount and a child reaching 18 lowers it from the month after the change; a change of address "
              "takes effect from the month after it is reported."),
        ("h", "9. History"),
        ("p", "The Complemento opened for claims on 1 October 2022 with a limit of €7,200 of computable income per "
              "equivalent adult and €90 a month per child. Order SOC/41/2024 raised the limit to €8,400 from 1 April "
              "2024. The amount rose to €95 from 1 January 2024 and to €100 from 1 July 2025."),
    ]
    IO.write_pdf(path, "Complemento Familiar Valdemorense: rules", DEPT, "Secretaría General Técnica", blocks,
                 "%s - Complemento Familiar, consolidated rules" % DEPT, "D:20261001090000+02'00'",
                 "D:20261001090000+02'00'")


def coverage(path, take_up, shares_by_kids):
    rows = [["Children in the family", "Share of families paid, average month of 2025 (%)"]]
    for k, v in shares_by_kids:
        rows.append([k, "%.1f" % v])
    blocks = [
        ("title", "Complemento Familiar: coverage report 2025"),
        ("sub", "%s, Servicio de Estudios y Evaluación. 16 March 2026. English working version." % DEPT),
        ("h", "1. Families paid"),
        ("p", "Families with two children were the largest group the Complemento Familiar paid in 2025."),
        ("table", rows),
        ("h", "2. Coverage"),
        ("p", "The department's coverage rate compares the families the Complemento was paying at the end of the "
              "year with the families entitled to it, estimated from the regional living conditions survey. At the "
              "end of 2025 the Complemento reached %.1f per cent of entitled families." % take_up),
        ("p", "Entitled families who do not receive the Complemento are mostly families who have not claimed it. "
              "The department wrote in 2025 to families known to its social services and to schools' family "
              "liaison officers."),
        ("h", "3. Method"),
        ("p", "Families paid are counted from the payment runs. Entitled families are estimated from the ECVV, "
              "applying the Complemento's income test to the households the survey interviewed."),
    ]
    IO.write_pdf(path, "Complemento Familiar: coverage report 2025", DEPT, "Servicio de Estudios", blocks,
                 "%s - Complemento Familiar coverage 2025" % DEPT, "D:20260316120000+01'00'",
                 "D:20260316120000+01'00'")


def results(path, med25, thr25, rates):
    """rates: dict of (province name or 'Comunidad de Valdemora') -> (all, children, 18-64, 65+) in per cent."""
    rows = [["", "All persons", "Children under 18", "Aged 18 to 64", "Aged 65 and over"]]
    for k in ["Comunidad de Valdemora"] + [n for _, n in P.PROVINCES]:
        r = rates[k]
        rows.append([k] + ["%.1f" % x for x in r])
    blocks = [
        ("title", "Encuesta de Condiciones de Vida de Valdemora 2026: main results"),
        ("sub", "%s. Published 24 September 2026. English summary. This summary reports incomes and poverty in "
                "2025; it does not appraise policy measures." % IEV),
        ("h", "Incomes in 2025"),
        ("p", "The median equivalised disposable income of the region's residents was %s in 2025. The "
              "at-risk-of-poverty threshold, 60 per cent of the median, was %s a year for one adult."
              % (euro(med25), euro(thr25))),
        ("h", "At-risk-of-poverty rate, 2025 incomes (per cent)"),
        ("table", rows),
        ("h", "About the survey"),
        ("p", "The ECVV 2026 interviewed households between 2 February and 30 June 2026 about their incomes in 2025. "
              "The sample is drawn from the regional dwelling register in three provincial strata, and results are "
              "published by the province in which the dwelling is located."),
        ("p", "A household interview is complete when the household questionnaire and the individual questionnaire "
              "of every member aged 16 or over are obtained. The response rate is the share of eligible sample "
              "dwellings in which a complete interview was obtained; dwellings found empty, used for something "
              "other than living in, or not found at the address are not eligible."),
        ("p", "Results are weighted to the region's population. Incomes are disposable incomes after tax and social "
              "contributions, including benefits, equivalised on the modified OECD scale."),
    ]
    IO.write_pdf(path, "ECVV 2026: main results", IEV, "Instituto de Estadística de Valdemora", blocks,
                 "%s - ECVV 2026 main results" % IEV, "D:20260924100000+02'00'", "D:20260924100000+02'00'")
