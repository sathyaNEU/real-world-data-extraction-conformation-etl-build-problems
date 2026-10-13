"""Write the data files of the pack: the Agency's statistics in their two layouts, its revision file and workplace
extract, its data dictionary and transmittal, the bureau's municipal concordance and population estimates, and the
labour force survey's regional estimates."""
import csv
import io

import openpyxl
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

import sim as S
import world as W

FILES = W.FILES
DISTRACTORS = W.DISTRACTORS
MONTH_NAMES = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
               "November", "December")


def _csv(path, header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(header)
    for r in rows:
        w.writerow(r)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())
    return len(rows)


def write_wide(cells, path):
    """the Agency's yearly tables to 2023: a sheet a year, municipality by industry group, a column a month"""
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    n = 0
    for year in (2021, 2022, 2023):
        ws = wb.create_sheet(str(year))
        ws["A1"] = "Payroll jobs by municipality and industry group, %d" % year
        ws["A1"].font = Font(bold=True, size=12)
        ws["A2"] = ("%s, employer return statistics. Jobs on employers' monthly returns, placed at the municipality "
                    "of the employer's account address." % W.AGENCY)
        head = ["Municipality code", "Municipality", "Industry group"] + list(MONTH_NAMES)
        ws.append([])
        ws.append(head)
        for c in range(1, len(head) + 1):
            ws.cell(row=4, column=c).font = Font(bold=True)
            ws.cell(row=4, column=c).alignment = Alignment(wrap_text=True, vertical="top")
        idx = [i for i in range(S.N) if S.MONTHS[i][0] == year]
        keys = sorted({(mc, W.SECTOR_GROUP[s]) for i in idx for (mc, s), v in cells[i].items() if v > 0})
        for mc, gcode in keys:
            vals = []
            for i in idx:
                vals.append(sum(v for (m2, s), v in cells[i].items() if m2 == mc and W.SECTOR_GROUP[s] == gcode))
            if not any(vals):
                continue
            ws.append([mc, W.MUNI_NAME[mc], gcode] + vals)
            n += 1
        for c, wdt in zip(range(1, 16), (12, 18, 9) + (10,) * 12):
            ws.column_dimensions[get_column_letter(c)].width = wdt
        ws.freeze_panes = "D5"
    ws = wb.create_sheet("Industry groups")
    ws.append(["Industry group", "Description"])
    for gcode, name, _ in W.GROUPS:
        ws.append([gcode, name])
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 52
    wb.save(path)
    return n


def write_long(cells, prelim, path):
    rows = []
    for i in range(S.MONTHS.index((2024, 1)), S.N):
        cur = prelim.get(i, cells[i])
        status = "P" if i in prelim else "F"
        for (mc, s) in sorted(cur, key=lambda k: (k[0], W.SECTOR_CODES.index(k[1]))):
            v = cur[(mc, s)]
            if v > 0:
                rows.append((S.month_label(i), mc, s, v, status))
    return _csv(path, ("reference_month", "municipality_code", "naics_sector", "payroll_jobs", "status"), rows)


def write_revisions(cells, prelim, path):
    rows = []
    for i in sorted(prelim):
        for (mc, s) in sorted(cells[i], key=lambda k: (k[0], W.SECTOR_CODES.index(k[1]))):
            v = cells[i][(mc, s)]
            if v > 0:
                rows.append((S.month_label(i), mc, s, v, "R"))
    return _csv(path, ("reference_month", "municipality_code", "naics_sector", "payroll_jobs", "status"), rows)


def write_workplaces(lines, path):
    rows = []
    for month in ("2026-03", "2027-03"):
        for r in sorted(lines[month], key=lambda r: (r["payroll_account"], r["workplace_no"])):
            rows.append((month, r["payroll_account"], r["legal_name"], r["operating_name"], r["workplace_no"],
                         r["street_address"], r["municipality_code"], r["naics_sector"], r["payroll_jobs"]))
    return _csv(path, ("reference_month", "payroll_account", "legal_name", "operating_name", "workplace_no",
                       "street_address", "municipality_code", "naics_sector", "payroll_jobs"), rows)


def write_concordance(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Municipalities"
    ws.append(["Municipal code", "Municipality", "Census division", "Economic region code", "Economic region",
               "In force from", "In force to", "Note"])
    for c in range(1, 9):
        ws.cell(row=1, column=c).font = Font(bold=True)
    for mc, nm, cd, w, vf, vt in W.MUNIS:
        er = W.MUNI_REGION[mc]
        note = ""
        if mc in W.AMALGAMATED:
            note = "Amalgamated with %s as %s (%s) on 1 January 2025" % (
                W.MUNI_NAME["0806" if mc == "0803" else "0803"], W.MUNI_NAME["0814"], "0814")
        if mc == "0814":
            note = "Formed on 1 January 2025 by the amalgamation of Wexleigh (0803) and Dorran (0806)"
        ws.append([mc, nm, cd, er, W.RNAME[er], vf or "2016-01-01", vt or None, note or None])
    for c, wdt in zip("ABCDEFGH", (15, 18, 15, 20, 18, 14, 14, 66)):
        ws.column_dimensions[c].width = wdt
    ws.freeze_panes = "A2"
    ws2 = wb.create_sheet("Economic regions")
    ws2.append(["Economic region code", "Economic region", "Census divisions"])
    for c in range(1, 4):
        ws2.cell(row=1, column=c).font = Font(bold=True)
    for code, name, cds, *_ in W.REGIONS:
        ws2.append([code, name, ", ".join(cds)])
    for c, wdt in zip("ABC", (20, 18, 18)):
        ws2.column_dimensions[c].width = wdt
    wb.save(path)
    return len(W.MUNIS)


def write_lfs(rows, path):
    return _csv(path, ("reference_month", "economic_region_code", "economic_region", "employment_thousands",
                       "unemployment_rate", "participation_rate"), rows)


def write_population(rows, path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Population"
    ws["A1"] = "Population estimates by municipality, 1 July 2024 to 2026"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("%s, demographic estimates. Postcensal estimates; 2026 preliminary, 2024 and 2025 updated." % W.BUREAU)
    ws.append([])
    ws.append(["Municipal code", "Municipality", "Reference date", "Population", "Population aged 15 to 64"])
    for c in range(1, 6):
        ws.cell(row=4, column=c).font = Font(bold=True)
    for mc, nm, year, p, p15 in rows:
        ws.append([mc, nm, "%d-07-01" % year, p, p15])
    for c, wdt in zip("ABCDE", (15, 18, 15, 12, 22)):
        ws.column_dimensions[c].width = wdt
    ws.freeze_panes = "A5"
    wb.save(path)
    return len(rows)


DICTIONARY = [
    (FILES["wide"], "(sheets 2021 to 2023)", "One row per municipality and industry group; a column per month. Payroll jobs on employers' monthly returns for the month, placed at the municipality of the employer's account address."),
    (FILES["wide"], "Industry group", "The Agency's industry group of the employer's activity code (sheet Industry groups). Used to December 2023."),
    (FILES["long"], "reference_month", "The month the returns report (YYYY-MM)."),
    (FILES["long"], "municipality_code", "The bureau's municipal code of the municipality the Agency's statistics place the jobs in."),
    (FILES["long"], "naics_sector", "NAICS 2022 sector of the activity code. Used from January 2024."),
    (FILES["long"], "payroll_jobs", "Jobs on employers' monthly returns for the month: employees paid in the month's pay periods."),
    (FILES["long"], "status", "F: final. P: preliminary; the months the Agency had not yet closed when the file was produced."),
    (FILES["rev"], "status", "R: revised. The file holds every cell of the months it covers, as revised."),
    (FILES["work"], "(file)", "One row per workplace on each payroll account's return for the month."),
    (FILES["work"], "payroll_account", "Payroll program account: the business number (nine digits) of the employer that holds the account, the program identifier RP and a four-digit reference number."),
    (FILES["work"], "legal_name", "Legal name recorded on the payroll account."),
    (FILES["work"], "operating_name", "Operating name recorded on the payroll account."),
    (FILES["work"], "workplace_no", "The workplace's sequence number on the account's workplace schedule."),
    (FILES["work"], "street_address", "The workplace's street address, as the Agency standardises it."),
    (FILES["work"], "municipality_code", "The bureau's municipal code of the workplace's municipality."),
    (FILES["work"], "naics_sector", "NAICS 2022 sector of the workplace's activity."),
    (FILES["work"], "payroll_jobs", "Jobs on the return at the workplace for the month: employees paid in the month's pay periods. Zero where the return lists the workplace with no employees paid."),
]


def write_dictionary(path):
    return _csv(path, ("file", "field", "description"), DICTIONARY)


def write_transmittal(path, counts):
    lines = [
        "%s - Revenue Statistics Unit" % W.AGENCY.upper(),
        "Transmittal to the %s" % W.BUREAU,
        "",
        "Date: 7 May 2027",
        "From: %s, %s" % W.PEOPLE["liaison"],
        "To: %s, %s" % W.PEOPLE["manager"],
        "Re: Employer return statistics for the first quarter of 2027",
        "",
        "Files delivered on 23 April 2027",
        "  %s  ({:,} rows; January 2024 to March 2027; January to March 2027 preliminary)".format(counts["long"]) % FILES["long"],
        "",
        "Files delivered today",
        "  %s  ({:,} rows; January to March 2027 as revised)".format(counts["rev"]) % FILES["rev"],
        "  %s  ({:,} rows; March 2026 and March 2027 workplace schedules)".format(counts["work"]) % FILES["work"],
        "  %s  (field descriptions for the files above and the yearly tables)" % FILES["dict"],
        "",
        "The revision file brings in returns for January to March 2027 received after 23 April and replaces those",
        "three months in the April file. March 2026 and March 2027 in the workplace file are as of today's date.",
        "",
        "Yearly tables for 2021 to 2023 (%s) are as published; the" % FILES["wide"],
        "statistics have been produced in the monthly layout since January 2024.",
        "",
        "Questions on these files: Revenue Statistics Unit, extension 4471.",
        "",
    ]
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write("\r\n".join(lines))
    return len(lines)
