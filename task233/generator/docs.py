"""The governing documents: the Price Collection Quality Standard and Schedule 4 of the agreement."""
import params as P
from io_util import write_pdf

ORG = "National Statistics Office"

PCQS_BLOCKS = [
    ("t", "Price Collection Quality Standard"),
    ("s", "Prices Division, National Statistics Office. Version 3.0, approved by the Head of Prices on 22 June 2026. "
          "Applies to the field collection carried out under the Price Collection Services Agreement from the quarter "
          "beginning 1 July 2026; replaces version 2.1 of March 2024."),
    ("h", "1. Purpose"),
    ("p", "This standard sets out how the Prices Division assesses the field collection of consumer price index "
          "prices carried out by Tallis Field Research Ltd under the Price Collection Services Agreement (the "
          "Agreement), and what follows from each quarter's assessment."),
    ("h", "2. Collection"),
    ("p", "2.1 Prices are collected each month on the index day, the second Tuesday of the month, and on the four "
          "working days that follow it. These five working days are the collection window. Weekends and the public "
          "holidays in the NSO collection calendar are not working days."),
    ("p", "2.2 At each outlet visit the collector records, for every quote on the outlet's quote list, the price at "
          "which the item is offered for sale in the outlet, that the item is not available, or a replacement "
          "variety and its price."),
    ("p", "2.3 The contractor's quarterly collection schedule, agreed with the Prices Division before the quarter "
          "begins, lists the outlet visits scheduled in each month of the quarter."),
    ("h", "3. Collection accuracy"),
    ("p", "3.1 A region's collection accuracy for a quarter is the share of the prices recorded by the contractor's "
          "collectors at the region's outlets during the quarter that were the price at which the item was offered "
          "for sale in the outlet at the time the collector recorded it. A price recorded for a replacement variety "
          "is a recorded price."),
    ("p", "3.2 The Prices Division estimates each region's collection accuracy from the Field Quality Team's "
          "back-checks of a monthly sample of the region's outlets, at which an officer re-collects the price of each "
          "item the collector priced. Items the officer cannot find are left out."),
    ("p", "3.3 Collection accuracy is compared with the bands in section 4 as estimated, without rounding."),
    ("h", "4. Outcomes"),
    ("table", [["Outcome", "Collection accuracy", "What follows"],
               ["Compliant", "%.1f per cent or more" % P.BAND_COMPLIANT, "None"],
               ["Corrective action", "Below %.1f per cent and at least %.1f per cent" % (P.BAND_COMPLIANT, P.BAND_CREDIT),
                "Accompanied collection in the region in every month of the following quarter"],
               ["Service credit", "Below %.1f per cent" % P.BAND_CREDIT,
                "Accompanied collection as above, and a credit of %d per cent of the region's quarterly collection fee "
                % P.CREDIT_PERCENT +
                "in Schedule 4 of the Agreement"]]),
    ("h", "5. Timeliness"),
    ("p", "5.1 A scheduled outlet visit is completed within the window when every price due at the outlet in the "
          "month is recorded within the collection window. Where an outlet has been taken over and its quotes are "
          "priced at the outlet that took it over, the visit there completes the scheduled visit."),
    ("p", "5.2 A region's timeliness for a quarter is the share of the outlet visits scheduled for the region in the "
          "quarter that were completed within the window. A scheduled visit at which no price was recorded during "
          "the month is a missed visit."),
    ("h", "6. Replacement varieties"),
    ("p", "6.1 The Prices Division's commodity analysts decide whether each replacement variety is comparable with "
          "the variety it replaces. A region's replacement acceptance for a quarter is the share of the replacements "
          "its collectors made during the quarter whose latest decision is Comparable. A replacement with no decision "
          "is not accepted."),
    ("h", "7. Reporting"),
    ("p", "7.1 The Head of Prices issues the quarterly assessment to the contractor within twenty working days of "
          "the quarter's end, with each region's outcome, timeliness, missed visits and replacement acceptance, and "
          "the quarter's service credit."),
]

FEES = {"CR01": 71480, "CR02": 63915, "CR03": 68240, "CR04": 47615, "CR05": 44380, "CR06": 46905,
        "CR07": 45270, "CR08": 49830, "CR09": 41760, "CR10": 43695, "CR11": 48155, "CR12": 42890,
        "CR13": 40575, "CR14": 46310}


def pcqs(path):
    write_pdf(path, "Price Collection Quality Standard v3.0", "Prices Division", ORG, PCQS_BLOCKS,
              "PCQS v3.0, National Statistics Office, Prices Division", "D:20260622143000+12'00'",
              "D:20260622143000+12'00'", widths={3: [32 * 2.8346, 52 * 2.8346, 86 * 2.8346]})


def fees(path, regions):
    rows = [["Region", "Region name", "Quarterly collection fee (dollars, excluding GST)"]]
    for r in regions:
        rows.append([r["code"], r["name"], "{:,}".format(FEES[r["code"]])])
    blocks = [
        ("t", "Price Collection Services Agreement"),
        ("s", "Schedule 4: Regional collection fees. Variation 3, signed 15 June 2026, effective 1 July 2026."),
        ("p", "4.1 The Contractor invoices each region's collection fee quarterly in arrears. The fee covers every "
              "outlet visit in the region's quarterly collection schedule, including accompanied collection."),
        ("p", "4.2 Service credits under the Price Collection Quality Standard are calculated on the quarterly fee "
              "below and deducted from the invoice for the quarter after the assessment."),
        ("table", rows),
        ("p", "4.3 Fees are reviewed annually at 1 July. All amounts are in dollars and exclude GST."),
    ]
    write_pdf(path, "PCSA Schedule 4 Regional collection fees", "Commercial Services", ORG, blocks,
              "Price Collection Services Agreement, Schedule 4 (Variation 3)", "D:20260615110500+12'00'",
              "D:20260615110500+12'00'", widths={3: [24 * 2.8346, 52 * 2.8346, 94 * 2.8346]})
