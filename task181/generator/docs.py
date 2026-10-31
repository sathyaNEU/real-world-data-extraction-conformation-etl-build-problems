"""The pack's documents and lookup files: the dengue plan, the CBMS 2025 tables, the barangay register,
the vector control unit's operations log, the city's rain gauge and the health zone's bulletin."""
import datetime as dt
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.lib import colors

from common import rng, write_csv, normalise_zip, set_mtime, mw_start, TRIGGER, scrub_pdf
from world import NAMES, N, BARANGAYS, IDX, SR, SPLIT_FROM, SPLIT_NEW, SPLIT_DATE, past_outbreaks

PDF_DATE = "D:20271011093000+08'00'"


def _pdf(path, story, title, author):
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, subject="", creator=author,
                            producer=author, invariant=1)
    doc.build(story)
    _fix_pdf_dates(path)
    scrub_pdf(path)
    set_mtime(path)


def _fix_pdf_dates(path):
    data = open(path, "rb").read()
    import re
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (" + PDF_DATE.encode() + b")", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (" + PDF_DATE.encode() + b")", data)
    open(path, "wb").write(data)


ST = {
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13, leading=16, spaceAfter=4),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5, leading=13, spaceBefore=8, spaceAfter=3),
    "p": ParagraphStyle("p", fontName="Helvetica", fontSize=9.5, leading=12.5, spaceAfter=4),
    "small": ParagraphStyle("small", fontName="Helvetica", fontSize=8, leading=10, textColor=colors.HexColor("#444444")),
}


def plan_pdf(path):
    s = []
    s.append(Paragraph("CITY HEALTH OFFICE, DALISAY CITY, LAGUNA", ST["small"]))
    s.append(Paragraph("Dengue Prevention and Control Plan 2027", ST["h1"]))
    s.append(Paragraph("Section 4. Surveillance and the barangay hotspot response &nbsp;&nbsp; Revision 2, 3 June 2027",
                       ST["small"]))
    s.append(Spacer(1, 6))
    s.append(Paragraph("4.1 The line list", ST["h2"]))
    s.append(Paragraph(
        "The City Epidemiology and Surveillance Unit (CESU) keeps the line list of dengue cases among the city's "
        "residents, notified through the online notification system by the disease reporting units: Dalisay "
        "Medical Center, Dalisay Doctors' Hospital, City Health Centers I to VI and the private clinics. A patient "
        "notified by two units is one case. A notification the CESU has classified Not a case is not a case. Cases "
        "among residents of other cities and municipalities are forwarded to their own health offices and are not "
        "the city's cases; they stay on the export until the CESU forwards them.", ST["p"]))
    s.append(Paragraph("4.2 Morbidity weeks", ST["h2"]))
    s.append(Paragraph(
        "The city counts in the morbidity weeks of the national calendar. Each week runs from Sunday to Saturday, "
        "and week 1 of 2027 began on Sunday 3 January 2027. A case belongs to the week of its onset of fever; a case "
        "whose onset is not recorded is dated by its first consultation.", ST["p"]))
    s.append(Paragraph("4.3 The hotspot response", ST["h2"]))
    s.append(Paragraph(
        "On the Monday after a window of four morbidity weeks closes, the CESU counts, from the cases notified by "
        "08:00 that day, the cases with onset in those four weeks. A barangay is placed under the hotspot response "
        "for the next four morbidity weeks when %d or more of those cases were infected in that barangay." % TRIGGER,
        ST["p"]))
    s.append(Paragraph(
        "A barangay under the hotspot response receives search-and-destroy of breeding sites by its Barangay Health "
        "Emergency Response Team with the Vector Control Unit (VCU), larviciding of water-storage containers, "
        "targeted space spraying where cases cluster, house-to-house fever case finding with NS1 testing, and a "
        "clean-up drive with the barangay council.", ST["p"]))
    s.append(Paragraph("4.4 Hospital admissions", ST["h2"]))
    s.append(Paragraph(
        "Dalisay Medical Center and Dalisay Doctors' Hospital keep dengue fast lanes in their emergency rooms from "
        "June to November and send the CESU their dengue admission records every Monday, residents of other towns "
        "included, for the city's bed planning. An admission is counted in the morbidity week the patient was "
        "admitted; a patient moved from one of the two hospitals to the other is one admission, at the hospital "
        "that admitted the patient first.", ST["p"]))
    s.append(Paragraph("4.5 Laboratory", ST["h2"]))
    s.append(Paragraph(
        "The City Health Office laboratory tests specimens from City Health Centers I to VI and the private clinics: "
        "the NS1 antigen ELISA on specimens taken within five days of the onset of fever, and the IgM capture ELISA "
        "on specimens taken later. The hospitals test their own patients. A result belongs to the morbidity week "
        "its specimen was collected.", ST["p"]))
    s.append(Paragraph("4.6 Larval surveys", ST["h2"]))
    s.append(Paragraph(
        "The VCU and the barangay health workers survey households for Aedes larvae each month in the barangays on "
        "the survey schedule. The house index of a barangay in a monthly round is the per cent of the houses "
        "inspected in that round where larvae or pupae were found in at least one container.", ST["p"]))
    s.append(Spacer(1, 10))
    t = Table([["Approved", "John Figueroa, MD, City Health Officer"],
               ["Prepared", "Tammy Orozco, RN, Head, City Epidemiology and Surveillance Unit"],
               ["Revision", "2 (3 June 2027): section 4.3 window moved to four weeks; 4.6 added"]],
              colWidths=[28 * mm, 130 * mm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.5), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LINEABOVE", (0, 0), (-1, 0), 0.5, colors.grey)]))
    s.append(t)
    _pdf(path, s, "Dengue Prevention and Control Plan 2027, Section 4", "City Health Office, Dalisay City")


AGE_GROUPS = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54",
              "55-59", "60-64", "65 and over"]


def cbms_tables(grp, W, workers):
    """The CBMS 2025 tables as integers: residents by 5-year group, persons 15+ by status, workers by place."""
    r = rng("cbms_tables")
    by_age = np.zeros((N, len(AGE_GROUPS)), dtype=int)
    for i in range(N):
        dorm = BARANGAYS[i][1] == "dorm"
        c = r.dirichlet([30, 33, 32])
        a_w = np.array([9, 13, 14, 12, 10, 9, 8, 7, 6, 5]) if not dorm else np.array([7, 18, 21, 17, 12, 8, 6, 5, 3, 3])
        a = r.dirichlet(a_w * 4.0)
        parts = list(grp[i, 0] * c) + list((grp[i, 1] + grp[i, 2]) * a) + [grp[i, 3]]
        by_age[i] = np.round(parts).astype(int)
        # keep the band totals equal to the simulated groups exactly
        by_age[i, 2] += int(grp[i, 0]) - by_age[i, 0:3].sum()
        by_age[i, 6] += int(grp[i, 1] + grp[i, 2]) - by_age[i, 3:13].sum()
        by_age[i, 13] = int(grp[i, 3])
    persons15 = by_age[:, 3:].sum(1)
    employed = grp[:, 1].astype(int)
    unemployed = np.round(employed * r.uniform(0.04, 0.09, N)).astype(int)
    nilf = persons15 - employed - unemployed
    wk = workers.astype(int)
    # rounding: rows of the place-of-work table add to the employed count
    for i in range(N):
        wk[i, -1] += employed[i] - wk[i].sum()
    return by_age, persons15, employed, unemployed, nilf, wk


def _dash(v):
    return "-" if int(v) == 0 else int(v)


def cbms_xlsx(path, grp, W, workers):
    by_age, persons15, employed, unemployed, nilf, wk = cbms_tables(grp, W, workers)
    wb = Workbook()
    order = sorted(range(N), key=lambda i: _register_order(i))
    # Table 1
    ws = wb.active
    ws.title = "Table 1"
    ws["A1"] = "Table 1. Household population by barangay and age group, Dalisay City: 2025"
    ws["A1"].font = Font(bold=True)
    ws["A2"] = "Community-Based Monitoring System 2025"
    ws.append([])
    ws.append(["Barangay", "Total"] + ["Age group"] + [""] * (len(AGE_GROUPS) - 1))
    ws.merge_cells(start_row=4, start_column=3, end_row=4, end_column=2 + len(AGE_GROUPS))
    ws.append(["", ""] + AGE_GROUPS)
    for i in order:
        ws.append([NAMES[i] if NAMES[i] != "Santo Nino" else "Santo Niño", int(by_age[i].sum())] + [_dash(v) for v in by_age[i]])
    ws.append(["Dalisay City", int(by_age.sum())] + [int(v) for v in by_age.sum(0)])
    ws.append([])
    ws.append(["Household population excludes persons in institutional living quarters."])
    ws.append(["Santo Tomas Norte was created in March 2025; its residents were enumerated under it."])
    # Table 3
    ws3 = wb.create_sheet("Table 3")
    ws3["A1"] = "Table 3. Household population 15 years old and over by barangay and employment status, Dalisay City: 2025"
    ws3["A1"].font = Font(bold=True)
    ws3["A2"] = "Community-Based Monitoring System 2025"
    ws3.append([])
    ws3.append(["Barangay", "Persons 15 years old and over", "In the labor force", "", "Not in the labor force"])
    ws3.merge_cells(start_row=4, start_column=3, end_row=4, end_column=4)
    ws3.append(["", "", "Employed", "Unemployed", ""])
    for i in order:
        ws3.append([NAMES[i] if NAMES[i] != "Santo Nino" else "Santo Niño", int(persons15[i]), int(employed[i]),
                    int(unemployed[i]), int(nilf[i])])
    ws3.append(["Dalisay City", int(persons15.sum()), int(employed.sum()), int(unemployed.sum()), int(nilf.sum())])
    ws3.append([])
    ws3.append(["Employed persons include those with a job or business during the reference week."])
    # Table 4
    ws4 = wb.create_sheet("Table 4")
    ws4["A1"] = ("Table 4. Employed persons by barangay of residence and place of work of the primary job, "
                 "Dalisay City: 2025")
    ws4["A1"].font = Font(bold=True)
    ws4["A2"] = "Community-Based Monitoring System 2025"
    ws4.append([])
    names = [NAMES[i] if NAMES[i] != "Santo Nino" else "Santo Niño" for i in order]
    ws4.append(["Barangay of residence", "Total employed", "Place of work"] + [""] * N)
    ws4.merge_cells(start_row=4, start_column=3, end_row=4, end_column=3 + N)
    ws4.append(["", ""] + names + ["Outside Dalisay City"])
    for i in order:
        ws4.append([names[order.index(i)], int(employed[i])] + [_dash(wk[i, j]) for j in order] + [_dash(wk[i, N])])
    ws4.append([])
    ws4.append(["Persons working at home are counted under their own barangay."])
    ws4.append(["Place of work as reported by the respondent for the primary job."])
    for wsx in (ws, ws3, ws4):
        wsx.column_dimensions["A"].width = 24
    wb.properties.creator = "Dalisay City Planning and Development Office"
    wb.properties.lastModifiedBy = "Dalisay City Planning and Development Office"
    fixed = dt.datetime(2026, 4, 30, 10, 0, 0)
    wb.properties.created = fixed
    wb.properties.modified = fixed
    wb.save(path)
    normalise_zip(path)
    return by_age, persons15, employed, wk, order


# the register's order: code order, which follows the barangays' creation, not the alphabet
_REG = None


def _register_order(i):
    global _REG
    if _REG is None:
        r = rng("register")
        perm = list(r.permutation([j for j in range(N) if j != SPLIT_NEW]))
        perm.append(SPLIT_NEW)
        _REG = {j: k for k, j in enumerate(perm)}
    return _REG[i]


def register_csv(path):
    r = rng("register_rows")
    rows = []
    for i in sorted(range(N), key=_register_order):
        k = _register_order(i)
        code = "0434190%02d" % (k + 1) if i != SPLIT_NEW else "043419037"
        area = round(float(r.uniform(38, 640)), 2)
        dist = "District 1" if (k % 5) < 3 else "District 2"
        puroks = int(r.integers(5, 12)) if i not in (SPLIT_FROM, SPLIT_NEW) else 4
        if i == SPLIT_NEW:
            rem = "Created 17/03/2025 under City Ordinance No. 2025-014 from Puroks 5 to 8 of Santo Tomas"
        elif i == SPLIT_FROM:
            rem = "Puroks 5 to 8 transferred to Santo Tomas Norte 17/03/2025 (City Ordinance No. 2025-014)"
        elif i == SR:
            rem = "Includes the Dalisay Industrial Estate (PEZA-registered special economic zone)"
        else:
            rem = ""
        nm = NAMES[i] if NAMES[i] != "Santo Nino" else "Santo Niño"
        rows.append([code, nm, dist, area, puroks, rem])
    write_csv(path, ["psgc_code", "barangay", "district", "land_area_ha", "puroks", "remarks"], rows)


def operations_log(path):
    """The VCU's activities: monthly search-and-destroy rounds everywhere and the hotspot responses the
    office assigned in earlier seasons."""
    r = rng("vcu_ops")
    rows = []
    ob = past_outbreaks()
    for y in range(2022, 2028):
        for m in range(1, 13):
            if y == 2027 and m > 8:
                break
            for i in r.choice(N, size=int(r.integers(6, 11)), replace=False):
                d = dt.date(y, m, int(r.integers(1, 28)))
                rows.append([d.strftime("%d/%m/%Y"), NAMES[int(i)], "Search and destroy", "VCU Team %d" % r.integers(1, 5),
                             int(r.integers(60, 260)), int(r.integers(20, 180)), ""])
        for (oy, i, pw, pm) in ob:
            if oy != y or oy == 2027:
                continue
            start = mw_start(y, pw + 1)
            for k, act in enumerate(["Search and destroy", "Larviciding", "Space spraying", "Case finding",
                                     "Clean-up drive"]):
                d = start + dt.timedelta(days=int(1 + 2 * k + r.integers(0, 2)))
                rows.append([d.strftime("%d/%m/%Y"), NAMES[i], act, "Hotspot Team %d" % r.integers(1, 5),
                             int(r.integers(120, 420)) if act != "Space spraying" else "",
                             int(r.integers(80, 400)) if act in ("Search and destroy", "Larviciding") else "",
                             "Hotspot response, morbidity weeks %d to %d" % (pw + 1, pw + 4)])
    rows.sort(key=lambda x: (dt.datetime.strptime(x[0], "%d/%m/%Y"), x[1], x[2]))
    write_csv(path, ["activity_date", "barangay", "activity", "team", "households_covered",
                     "containers_destroyed", "note"], rows)


def rainfall_csv(path):
    r = rng("rain")
    rows = []
    d = dt.date(2022, 1, 1)
    while d <= dt.date(2027, 10, 10):
        wet = 5 <= d.month <= 11
        p = 0.62 if wet else 0.18
        mm_ = round(float(r.gamma(0.8, 18.0 if wet else 6.0)), 1) if r.random() < p else 0.0
        if r.random() < 0.012:
            rows.append([d.isoformat(), "", "gauge maintenance"])
        else:
            rows.append([d.isoformat(), mm_, ""])
        d += dt.timedelta(days=1)
    write_csv(path, ["date", "rainfall_mm", "remarks"], rows)


def bulletin_pdf(path, city_cases_2027, city_cases_2026):
    r = rng("bulletin")
    towns = [("Dalisay City", city_cases_2027, city_cases_2026)]
    for t in ["Pinagbuklod", "Kalinaw", "Sinagtala", "Masilaw"]:
        a = int(r.integers(380, 1900))
        b = int(a / r.uniform(0.7, 1.5))
        towns.append((t, a, b))
    s = []
    s.append(Paragraph("LAGUNA BAY INTER-LOCAL HEALTH ZONE", ST["small"]))
    s.append(Paragraph("Dengue situation update, morbidity weeks 1 to 39, 2027", ST["h1"]))
    s.append(Paragraph("Issued 4 October 2027 by the zone's epidemiology desk, from the member offices' line lists "
                       "as received on 1 October 2027.", ST["small"]))
    s.append(Spacer(1, 6))
    data = [["Member LGU", "Cases MW 1-39, 2027", "Same period 2026", "Change"]]
    for (t, a, b) in towns:
        data.append([t, f"{a:,}", f"{b:,}", "%+.0f%%" % (100.0 * (a - b) / b)])
    tot_a = sum(x[1] for x in towns)
    tot_b = sum(x[2] for x in towns)
    data.append(["Zone", f"{tot_a:,}", f"{tot_b:,}", "%+.0f%%" % (100.0 * (tot_a - tot_b) / tot_b)])
    t = Table(data, colWidths=[50 * mm, 38 * mm, 38 * mm, 25 * mm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 9), ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 9),
                           ("GRID", (0, 0), (-1, -1), 0.3, colors.grey), ("ALIGN", (1, 1), (-1, -1), "RIGHT")]))
    s.append(t)
    s.append(Spacer(1, 8))
    s.append(Paragraph("Serotyping at the zone's sentinel hospitals found DENV-2 in most typed specimens since July, "
                       "with DENV-3 in the remainder. Member offices are reminded to keep their dengue fast lanes "
                       "open until the end of November.", ST["p"]))
    _pdf(path, s, "Dengue situation update MW 1-39 2027", "Laguna Bay Inter-Local Health Zone")
