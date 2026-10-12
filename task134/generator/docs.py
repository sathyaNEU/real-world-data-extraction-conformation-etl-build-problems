"""Strathallan's documents: the budget definitions, the charging policy, the extract notes, the draft contract offer
note, the contract rate table and the care home register."""
import datetime as dt
import os
import shutil
import tempfile

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill

import officex as OX
import postprocess as P
import world as W

PEOPLE = W.PEOPLE


def definitions_docx(path):
    P_ = lambda t: ("p", t)
    blocks = [
        ("title", "Care home budget 2027-28: definitions"),
        ("small", "Strathallan Health and Social Care Partnership  |  Finance and Planning  |  Version 1.2, 12 January 2027"),
        ("h1", "1. Purpose"),
        P_("1.1 This note defines the figures the care home line of the 2027-28 budget is built on."),
        P_("1.2 Figures are stated as the records stand at the extract, so a decision recorded after a date but effective "
           "on or before it counts on that date."),
        ("h1", "2. Residents"),
        P_("2.1 Council-funded resident: a person in a long-stay care home placement for whom the partnership pays the care "
           "home fee, less the contribution the person has been assessed to pay. A person is council-funded from the date "
           "the partnership's funding takes effect."),
        P_("2.2 Self-funding residents who receive free personal care or free nursing care payments are not council-funded "
           "residents; those payments are budgeted in a separate line."),
        P_("2.3 Long-stay: a permanent placement. Respite, short-break and interim placements are excluded."),
        P_("2.4 Council-funded residents on a date: each council-funded person with a long-stay placement in place at the "
           "end of that day, counted once, whenever they were admitted, including residents temporarily in hospital and "
           "residents placed in care homes outside Strathallan."),
        ("h1", "3. Weekly cost"),
        P_("3.1 Weekly contribution: the amount a resident has been assessed to pay each week towards the cost of their "
           "placement under the charging policy."),
        P_("3.2 Weekly fee: the weekly fee in the placement's contract, including any supplement agreed for the resident."),
        ("h1", "4. Sources"),
        P_("4.1 The figures are taken from the case management system and the finance system as extracted on 18 January "
           "2027. The extract notes of that date describe each file."),
        ("table", [["Version", "Date", "Change"],
                   ["1.0", "24 November 2026", "First issue for the budget working group"],
                   ["1.1", "9 December 2026", "2.4 extended to residents placed outside Strathallan"],
                   ["1.2", "12 January 2027", "1.2 added; 3.2 supplements"]], [1300, 2200, 5500], 18),
    ]
    props = dict(title="Care home budget 2027-28: definitions", creator=PEOPLE["analyst"], modified_by=PEOPLE["cfo"],
                 created=dt.datetime(2026, 11, 24, 10, 41), modified=dt.datetime(2027, 1, 12, 16, 8), revision=11,
                 total_time=212, company="Strathallan Council")
    OX.docx(path, blocks, ("Strathallan Health and Social Care Partnership", "OFFICIAL"),
            ("Care home budget 2027-28: definitions  |  v1.2", "Page {PAGE} of {NUMPAGES}"), props, font="Arial", size=21,
            heading_colour="1F4E79", seed=2611, sessions=6, margins=(1418, 1418, 1247, 1247))


def charging_policy_pdf(path):
    fpc, fnc = W.FPNC[2026]
    lo, hi = W.CAPITAL[2026]
    P_ = lambda t: ("p", t)
    blocks = [
        ("title", "Charging for care home placements: policy and rates 2026-27"),
        ("small", "Strathallan Health and Social Care Partnership  |  Financial Assessment Team  |  April 2026"),
        ("h1", "1. Introduction"),
        P_("This policy explains how the partnership charges for long-stay care home placements arranged or funded by "
           "Strathallan. It follows the national guidance on charging for residential accommodation and the rates set by "
           "the Scottish Government for 2026-27. It replaces the 2025-26 policy from 6 April 2026."),
        ("h1", "2. Free personal and nursing care"),
        P_("Everyone aged 65 or over assessed as needing personal care receives free personal care, and residents assessed "
           "as needing nursing care also receive free nursing care. In a care home these are paid as weekly amounts "
           "towards the fee. From 1 April 2026 the rates are:"),
        ("table", [["Payment", "Weekly rate from 1 April 2026"],
                   ["Free personal care", "£%.2f" % fpc], ["Free nursing care", "£%.2f" % fnc]], [4600, 4400], 19),
        P_("For a resident who pays the full fee these amounts are paid by the partnership to the care home every four "
           "weeks in arrears, and the home reduces the resident's bill by the same amount."),
        ("h1", "3. Financial assessment"),
        P_("3.1 A resident who asks the partnership to arrange or fund a placement has a financial assessment of their "
           "income and capital. The assessment sets the weekly contribution the resident pays towards the fee; the "
           "partnership pays the rest."),
        P_("3.2 Capital limits from 1 April 2026: capital below £%s is disregarded; capital between £%s and £%s is "
           "treated as giving a tariff income of £1 a week for every £250, or part of £250, above the lower limit; a "
           "resident with capital above £%s pays the full fee, less any free personal and nursing care payments."
           % (format(lo, ","), format(lo, ","), format(hi, ","), format(hi, ","))),
        P_("3.3 Income counted includes state and occupational pensions and most social security benefits. The resident "
           "keeps a personal expenses allowance of £%.2f a week." % W.PEA[2026]),
        P_("3.4 The value of the resident's home is disregarded for the first 12 weeks of a long-stay placement and while "
           "a partner or qualifying relative lives there. A deferred payment agreement can be offered where the home is "
           "counted."),
        ("h1", "4. Residents paying the full fee"),
        P_("4.1 A resident whose capital is above the upper limit arranges their own placement and pays the care home "
           "directly. The partnership pays free personal care and free nursing care as in section 2."),
        P_("4.2 A resident paying the full fee whose capital falls to the upper limit should contact the Financial "
           "Assessment Team. Where the partnership agrees to fund the placement, its funding takes effect from the date "
           "the resident's capital reached the upper limit, and the contribution is assessed from that date. The "
           "placement continues in the same home where the fee is within the partnership's usual rate or a supplement "
           "is agreed."),
        ("h1", "5. Reviews"),
        P_("5.1 Contributions are reviewed each year, around the anniversary of the date the partnership's funding began, "
           "and whenever the resident's circumstances change. The resident is told the new contribution in writing."),
        P_("5.2 A resident who disagrees with an assessment can ask for it to be looked at again within 28 days of the "
           "letter, and then use the partnership's complaints procedure."),
        ("h1", "6. Contacts"),
        P_("Financial Assessment Team, Strathallan Council, Finance Services. Team leader: %s." % PEOPLE["finance"]),
    ]
    props = dict(title="Charging for care home placements: policy and rates 2026-27", creator=PEOPLE["finance"],
                 modified_by=PEOPLE["finance"], created=dt.datetime(2026, 3, 17, 9, 22),
                 modified=dt.datetime(2026, 4, 2, 14, 51), revision=8, total_time=164, company="Strathallan Council")
    tmp = tempfile.mkdtemp()
    src = os.path.join(tmp, "policy.docx")
    OX.docx(src, blocks, ("Strathallan Health and Social Care Partnership", "Charging policy 2026-27"),
            ("Financial Assessment Team  |  April 2026", "Page {PAGE} of {NUMPAGES}"), props, font="Arial", seed=2603,
            sessions=5, margins=(1418, 1418, 1247, 1247))
    OX.pdf_from_docx(src, path)
    shutil.rmtree(tmp)
    P.normalize_pdf(path, dt.datetime(2026, 4, 2, 15, 5), doc_id=b"9A41C27E0B3D58F16E2A7C49D05B1F83")


def draft_offer_pdf(path):
    r27, n27 = W.NCHC_DRAFT_2027
    r26, n26 = W.NCHC[2026]
    P_ = lambda t: ("p", t)
    blocks = [
        ("title", "National Care Home Contract 2027-28: draft rate offer"),
        ("small", "Briefing note for the commissioning management team  |  Contracts and Commissioning  |  8 December 2026"),
        P_("The national negotiators have circulated a draft offer for the 2027-28 National Care Home Contract rates. "
           "The offer has not been agreed. Providers' representatives are consulting their members and a response is "
           "expected in February 2027; in previous years the agreed rate has differed from the first offer."),
        ("table", [["Weekly rate", "2026-27 (current)", "2027-28 draft offer", "Change"],
                   ["Residential", "£%.2f" % r26, "£%.2f" % r27, "%.1f%%" % (100 * (r27 / r26 - 1))],
                   ["Nursing", "£%.2f" % n26, "£%.2f" % n27, "%.1f%%" % (100 * (n27 / n26 - 1))]],
         [2400, 2200, 2400, 2000], 19),
        P_("Until a new rate is agreed, placements continue to be paid at the 2026-27 rates, with any increase backdated "
           "to 1 April 2027 once agreed. Supplements agreed for individual residents are not part of the national "
           "rate and are reviewed separately with each home."),
        P_("For budget purposes Finance has asked that the draft offer is not treated as agreed. The contracts team will "
           "update the rate table when the national rate is confirmed."),
        P_("%s, Care Home Contracts Officer" % PEOPLE["contracts"]),
    ]
    props = dict(title="NCHC 2027-28 draft rate offer", creator=PEOPLE["contracts"], modified_by=PEOPLE["contracts"],
                 created=dt.datetime(2026, 12, 7, 15, 12), modified=dt.datetime(2026, 12, 8, 11, 37), revision=4,
                 total_time=58, company="Strathallan Council")
    tmp = tempfile.mkdtemp()
    src = os.path.join(tmp, "offer.docx")
    OX.docx(src, blocks, ("Strathallan Council", "Contracts and Commissioning"),
            ("NCHC 2027-28 draft offer  |  OFFICIAL", "Page {PAGE} of {NUMPAGES}"), props, font="Calibri", seed=2612,
            sessions=3, margins=(1418, 1418, 1247, 1247))
    OX.pdf_from_docx(src, path)
    shutil.rmtree(tmp)
    P.normalize_pdf(path, dt.datetime(2026, 12, 8, 11, 40), doc_id=b"3C7E19A02F64B85D1E09A3C7F2B64D18")


def rates_xlsx(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "NCHC rates"
    ws.append(["National Care Home Contract weekly rates paid by Strathallan"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Contracts and Commissioning. Rates as agreed nationally; supplements for individual residents are recorded on the placement."])
    ws.append([])
    hdr = ["Financial year", "Care type", "Weekly rate (£)", "Effective from"]
    ws.append(hdr)
    for j in range(1, 5):
        c = ws.cell(row=4, column=j)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDEBF7")
    for y in range(2021, 2027):
        for k, ct in enumerate(("Residential", "Nursing")):
            ws.append(["%d-%02d" % (y, (y + 1) % 100), ct, W.NCHC[y][k], dt.date(y, 4, 1)])
    for r in range(5, ws.max_row + 1):
        ws.cell(row=r, column=3).number_format = "#,##0.00"
        ws.cell(row=r, column=4).number_format = "dd/mm/yyyy"
    for col, w in zip("ABCD", [15, 13, 16, 14]):
        ws.column_dimensions[col].width = w
    OX.xlsx_from_openpyxl(wb, path, PEOPLE["contracts"], PEOPLE["contracts"], dt.datetime(2021, 5, 4, 10, 2),
                          dt.datetime(2026, 5, 11, 14, 26), seed=3101)


def register_xlsx(df, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Register"
    cols = ["service_no", "service_name", "provider", "postcode", "service_type", "registered_places", "registered",
            "cancelled", "previous_service_no"]
    ws.append(cols)
    for j in range(1, len(cols) + 1):
        c = ws.cell(row=1, column=j)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="E2EFDA")
        c.alignment = Alignment(vertical="top")
    for r in df.itertuples(index=False):
        ws.append([r.service_no, r.service_name, r.provider, r.postcode, r.service_type, int(r.registered_places),
                   dt.date.fromisoformat(r.registered), dt.date.fromisoformat(r.cancelled) if r.cancelled else None,
                   r.previous_service_no or None])
    for r in range(2, ws.max_row + 1):
        for j in (7, 8):
            ws.cell(row=r, column=j).number_format = "dd/mm/yyyy"
    for col, w in zip("ABCDEFGHI", [15, 28, 27, 10, 38, 10, 12, 12, 16]):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:I%d" % ws.max_row
    OX.xlsx_from_openpyxl(wb, path, PEOPLE["contracts"], PEOPLE["contracts"], dt.datetime(2024, 2, 19, 9, 14),
                          dt.datetime(2026, 12, 21, 15, 47), seed=3102)


def extract_notes(path, n):
    t = """STRATHALLAN HEALTH AND SOCIAL CARE PARTNERSHIP
Performance and Information: care home extracts for the 2027-28 budget
Run: Monday 18 January 2027. Records to 31 December 2026.
Contact: %(analyst)s, Planning and Performance

Files
  care_home_placements_2021-2026.csv     case management system, %(pl)s rows
  fpnc_payment_lines_2021-2026.csv        finance system (care payments), %(li)s rows
  charging_assessments_2021-2026.csv      finance system (financial assessment), %(fa)s rows
  client_id_crosswalk_2023.csv            case management system, %(cw)s rows
  nrs_death_linkage_2027-01-15.tsv        NRS deaths matched to client records (tab-separated), %(dl)s rows

The cut
  Each extract holds what the system recorded by the run date for events up to 31 December 2026. Admissions,
  placement starts and ends, payment periods and deaths dated after 31 December 2026 are not included; a date after
  31 December 2026 shows as blank.

Case management system
  The case management system was replaced on 3 July 2023. Clients were given new client numbers. Placement episodes
  that ended before 3 July 2023 were loaded from the old system's archive and keep the old client number
  (SWS followed by six digits). client_id_crosswalk_2023.csv lists every client number with the old number, the
  finance system debtor reference and, where two records were found to be the same person, the client number the
  record was merged into.

care_home_placements_2021-2026.csv
  Every placement episode of a long-stay placement in place at any time from 1 April 2021, from the start of the
  placement, and every interim and respite placement from 1 April 2021. A placement is split into a new episode when
  the weekly fee changes, when the resident moves home, and when the home's service number changes.
  placement_id      episode number
  client_id         client number (see above)
  service_no        Care Inspectorate service number of the home
  placement_type    PERM permanent (long-stay); INT interim; RESP respite or short break
  route             PERM placements only: DIRECT council-funded from admission; CONV council funding following a
                    period of paying the full fee in the home
  care_type         Residential or Nursing
  admitted          date of admission to the care home
  start_date        first day of the episode (for CONV, the date council funding took effect)
  end_date          last day of the episode; blank if open
  end_reason        FEE new weekly fee; MOVE moved to another home; SVC home re-registered; DIED; DISCH discharged
                    from care home; ENDED interim or respite placement ended
  weekly_fee        contracted weekly fee for the episode (GBP)
  locality          the partnership locality recorded on the placement

fpnc_payment_lines_2021-2026.csv
  Free personal care and free nursing care paid to care homes for residents paying the full fee, by four-weekly
  payment period, from period 1 of 2021-22.
  debtor_ref        finance system debtor reference
  service_no        Care Inspectorate service number of the home
  admitted          date of admission to the care home
  award_start       date the free personal care award started
  period            payment period (financial year and period number)
  period_start, period_end
  line_type         FPC free personal care; FNC free nursing care; ADJ adjustment (arrears or recovery);
                    HOSP reduction for a hospital stay
  amount            GBP; adjustments and reductions can be negative
  award_end         last day of the award; blank if open
  end_reason        CF council funding agreed; DIED; LEFT left the care home

charging_assessments_2021-2026.csv
  Financial assessments in force on or after 1 April 2021.
  assessment_no     assessment number
  debtor_ref        finance system debtor reference
  completed         date the assessment was completed
  effective_from    date the contribution applies from
  weekly_contribution  GBP; blank for SELF
  outcome           ASSESSED contribution assessed; NIL no contribution; SELF capital above the upper limit,
                    resident pays the full fee

nrs_death_linkage_2027-01-15.tsv
  Deaths registered with National Records of Scotland by 15 January 2027, dated 1 April 2021 to 31 December 2026,
  matched to client records on 15 January 2027.
  match_status      EXACT matched on CHI number; PROBABLE matched on name, date of birth and postcode

Other files supplied with this run
  care_home_budget_definitions_2027-28.docx  budget definitions, version 1.2 (Finance and Planning)
  charging_policy_2026-27.pdf             charging policy and rates for 2026-27 (Financial Assessment Team)
  care_home_register_2026-12.xlsx         Care Inspectorate register of care homes for older people in Strathallan
  postcode_locality_lookup.csv            postcode to partnership locality
  nchc_rates_2021-22_to_2026-27.xlsx      contract rates (Contracts and Commissioning)
  nchc_draft_offer_2027-28.pdf            briefing note on the draft 2027-28 contract rates (Contracts and Commissioning)
  care_at_home_hours_2024-2026.csv        care at home hours by locality (Performance and Information)
  care_inspectorate_grades_2026.csv       latest inspection grades for Strathallan's care homes
""" % dict(analyst=PEOPLE["analyst"], **{k: format(v, ",") for k, v in n.items()})
    with open(path, "w", newline="\r\n") as f:
        f.write(t)
