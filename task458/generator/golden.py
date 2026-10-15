"""The golden deliverables, computed from the shipped files only (conform.py): the board's county scorecard
(prescriber_pilot_county_scorecard_2027.xlsx) and the conformed county and eligibility-group table
(county_adult_members_2026_conformed.csv); and generator/figures.json, every figure the write-up states."""
import csv
import json
import os

import conform as CF

SCORECARD = "prescriber_pilot_county_scorecard_2027.xlsx"
CONFORMED = "county_adult_members_2026_conformed.csv"
GROUP_NAME = {"SSI-DIS": "Disabled adults (SSI-related)", "ADULT-EXP": "Expansion adults", "PARENT-CR": "Parents and caretaker relatives",
              "AGED-65": "Adults 65 and over"}
QNAME = {"2025 Q3": "Jul-Sep 2025", "2025 Q4": "Oct-Dec 2025", "2026 Q1": "Jan-Mar 2026", "2026 Q2": "Apr-Jun 2026"}


def r10(x):
    return int(round(x / 10.0)) * 10


def dollars(x):
    return int(round(x))


def figures(a):
    sc, cg = a["scorecard"], a["cg"]
    designated = [c for c in CF.COUNTIES if sc.loc[c, "designated"]]
    f = {"designated": designated, "counties": {}, "payments": {}, "conformed": {}}
    for c in CF.COUNTIES:
        x = sc.loc[c]
        # the ratios and the reach as the board's table shows them: from the counts rounded to the nearest 10 (each
        # standard is judged on the unrounded values, NP-31 3.2)
        n_smi, n_oud = r10(x["est_smi"]), r10(x["est_oud"])
        f["counties"][c] = {
            "prescribers": int(x["prescribers"]), "members": int(x["members"]),
            "smi": n_smi, "oud": n_oud, "smi_unrounded": round(float(x["est_smi"]), 2),
            "oud_unrounded": round(float(x["est_oud"]), 2), "seen": int(x["seen_smi"]),
            "s_smi": round(int(x["prescribers"]) / n_smi * 1000, 1), "s_oud": round(int(x["prescribers"]) / n_oud * 1000, 1),
            "s_reach_pct": int(round(int(x["seen_smi"]) / n_smi * 100)),
            "meets_smi": not bool(x["fail_smi"]), "meets_oud": not bool(x["fail_oud"]),
            "meets_reach": not bool(x["fail_reach"]), "fails": int(x["fails"]), "designated": bool(x["designated"])}
        f["payments"][c] = {q: dollars(a["pay"][(c, q)]) for q, _, _ in CF.QUARTERS}
    for row in cg.to_dict("records"):
        f["conformed"]["%s|%s" % (row["county"], row["group"])] = {
            "members": int(row["members"]), "paid": dollars(a["pay_group"][(row["county"], row["group"])])}
    mem = a["members"]
    f["totals"] = {"adult_members": int(len(mem)), "full_year": int(mem["full_year"].sum()),
                   "rec_smi": int(mem["rec_smi"].sum()), "rec_oud": int(mem["rec_oud"].sum()),
                   "practising": int(sum(len(v) for v in a["practising"].values()))}
    cap = a["capture"]
    f["capture_pct"] = {"smi_1": round(cap["smi"][0] * 100, 1), "smi_3": round(cap["smi"][2] * 100, 1),
                        "smi_6": round(cap["smi"][5] * 100, 1)}
    # the same window, two kinds of member: expansion adults enrolled three months against the expansion adults enrolled
    # all year within their first three months
    exp = mem[mem["group"] == "ADULT-EXP"]
    two = exp[exp["months"] == 2]
    fy = exp[exp["full_year"]]
    f["window_yield_pct"] = {"exp_two_months": round(float(two["rec_smi"].mean()) * 100, 1),
                             "exp_full_year_first_two": round(float((fy["first_smi"] <= 2).mean()) * 100, 1),
                             "exp_two_months_n": int(len(two))}
    # the reader's route and the default path: the full-year members' prevalence carried to every member, by group
    import methods as MT
    R = MT.routes(a)
    nd = MT.needs(a)
    df, st = R["full_year_group"]
    f["full_year_route"] = {"designated": list(st), "yakima_smi": r10(nd["full_year_group"][0]["Yakima"]),
                            "yakima_s_smi": round(float(df.loc["Yakima", "s_smi"]), 1),
                            "yakima_reach_pct": int(round(float(df.loc["Yakima", "s_reach"]) * 100))}
    f["identified_count_designated"] = list(R["recorded"][1])
    # what the write-up quotes from NP-31 and the prompt: the thresholds, the ratio base, the sections it cites and the
    # age that names an eligibility group
    f["stated"] = {"threshold_smi": 16.5, "threshold_oud": 23.0, "threshold_reach_pct": 68, "per_members": 1000,
                   "sections": [2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 3.1, 3.2, 4.1], "aged_group_age": 65,
                   "months": [1, 3, 12]}
    return f


def write_scorecard(a, f, path):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    wb = Workbook()
    ws = wb.active
    ws.title = "Designation 2027"
    navy = "1F4E5A"
    thin = Side(style="thin", color="9AA5AB")
    ws["A1"] = "%s qualify for the 2027 Prescriber Service Award Pilot under NP-31" % (
        ", ".join(f["designated"][:-1]) + " and " + f["designated"][-1])
    ws["A1"].font = Font(name="Calibri", size=14, bold=True, color=navy)
    ws["A2"] = ("Contract year 1 July 2025 to 30 June 2026. Practising prescribers as of 1 November 2026. Network Analytics "
                "for the Board of Directors, meeting of 19 November 2026.")
    ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="5B6268")
    hdr = ["County", "Adult members", "Practising behavioral-health prescribers",
           "Adult members with a serious mental illness", "Adult members with an opioid use disorder",
           "Prescribers per 1,000 with a serious mental illness (16.5)", "Meets",
           "Prescribers per 1,000 with an opioid use disorder (23.0)", "Meets",
           "Reach: share with a serious mental illness seen by a prescriber (68%)", "Meets", "Standards failed",
           "Designated"]
    ws.append([])
    ws.append(hdr)
    hr = ws.max_row
    for k, h in enumerate(hdr, start=1):
        cell = ws.cell(row=hr, column=k)
        cell.font = Font(name="Calibri", size=9.5, bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=navy)
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center" if k > 1 else "left")
    ws.row_dimensions[hr].height = 58
    yes, no = "Yes", "No"
    for c in CF.COUNTIES:
        x = f["counties"][c]
        sc = a["scorecard"].loc[c]
        ws.append([c, x["members"], x["prescribers"], x["smi"], x["oud"], x["s_smi"], yes if x["meets_smi"] else no,
                   x["s_oud"], yes if x["meets_oud"] else no, x["s_reach_pct"] / 100, yes if x["meets_reach"] else no,
                   x["fails"], yes if x["designated"] else no])
        r = ws.max_row
        for k in range(1, 14):
            cell = ws.cell(row=r, column=k)
            cell.font = Font(name="Calibri", size=10, bold=bool(x["designated"]) and k in (1, 13))
            cell.border = Border(bottom=thin)
            if k > 1:
                cell.alignment = Alignment(horizontal="right" if k not in (7, 9, 11, 13) else "center")
        for k in (7, 9, 11):
            if ws.cell(row=r, column=k).value == no:
                ws.cell(row=r, column=k).font = Font(name="Calibri", size=10, bold=True, color="A12A2A")
        if x["designated"]:
            for k in range(1, 14):
                ws.cell(row=r, column=k).fill = PatternFill("solid", fgColor="F3E6D8")
        ws.cell(row=r, column=2).number_format = "#,##0"
        ws.cell(row=r, column=4).number_format = "#,##0"
        ws.cell(row=r, column=5).number_format = "#,##0"
        ws.cell(row=r, column=6).number_format = "0.0"
        ws.cell(row=r, column=8).number_format = "0.0"
        ws.cell(row=r, column=10).number_format = "0%"
    last = ws.max_row
    ws.append([])
    ws.append(["Designated: %s (each fails at least two of the three standards)." % ", ".join(f["designated"])])
    ws.cell(row=ws.max_row, column=1).font = Font(name="Calibri", size=10, bold=True)
    ws.append(["Members with a condition are rounded to the nearest 10, and the ratios and the reach shown are computed "
               "from those counts; each standard is judged on the unrounded values (NP-31 3.2). See Notes."])
    ws.cell(row=ws.max_row, column=1).font = Font(name="Calibri", size=9, italic=True, color="5B6268")
    widths = [13, 10, 13, 14, 14, 15, 7, 15, 7, 17, 7, 9, 10]
    for k, wdt in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(k)].width = wdt
    ws.freeze_panes = ws.cell(row=hr + 1, column=2)
    ws.print_title_rows = "%d:%d" % (hr, hr)
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.print_area = "A1:M%d" % (last + 3)

    ws2 = wb.create_sheet("FFS payments")
    ws2["A1"] = "Net fee-for-service payments for services behavioral-health prescribers rendered to each county's adult members"
    ws2["A1"].font = Font(name="Calibri", size=12, bold=True, color=navy)
    ws2["A2"] = ("Claims with a service date in the quarter, as paid through 31 October 2026, net of replacements and voids; "
                 "each claim's paid amount once. US dollars.")
    ws2["A2"].font = Font(name="Calibri", size=9, italic=True, color="5B6268")
    ws2.append([])
    hdr2 = ["County"] + ["%s (%s)" % (q, QNAME[q]) for q, _, _ in CF.QUARTERS]
    ws2.append(hdr2)
    h2 = ws2.max_row
    for k in range(1, len(hdr2) + 1):
        cell = ws2.cell(row=h2, column=k)
        cell.font = Font(name="Calibri", size=9.5, bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=navy)
        cell.alignment = Alignment(wrap_text=True, horizontal="center" if k > 1 else "left", vertical="center")
    ws2.row_dimensions[h2].height = 30
    for c in CF.COUNTIES:
        ws2.append([c] + [f["payments"][c][q] for q, _, _ in CF.QUARTERS])
        for k in range(2, 6):
            ws2.cell(row=ws2.max_row, column=k).number_format = "$#,##0"
            ws2.cell(row=ws2.max_row, column=k).border = Border(bottom=thin)
        ws2.cell(row=ws2.max_row, column=1).border = Border(bottom=thin)
    for k, wdt in enumerate([14, 18, 18, 18, 18], start=1):
        ws2.column_dimensions[get_column_letter(k)].width = wdt
    ws2.freeze_panes = ws2.cell(row=h2 + 1, column=2)

    ws3 = wb.create_sheet("Notes")
    notes = [
        ("Standards", "NP-31 section 3: practising behavioral-health prescribers per 1,000 adult members with a serious mental "
         "illness (16.5) and with an opioid use disorder (23.0), and the share of adult members with a serious mental illness "
         "who had a visit with a behavioral-health prescriber (68 per cent). A county is designated when it fails two or more."),
        ("Adult members", "Persons enrolled on at least one day of the contract year, by client identifier, each in the "
         "county and eligibility group of the enrollment span covering their last enrolled day."),
        ("Members with a condition", "Claims identify a serious mental illness or an opioid use disorder only through the "
         "services billed while a member is enrolled, and in Adams, Franklin, Grant and Yakima many expansion adults and "
         "parents are enrolled for a few months at a season. Those seasonal members have the conditions less often than "
         "the members enrolled all year, so the full-year members' prevalence is not carried to them. Each member a final "
         "claim or encounter identifies (NP-31 Appendix A codes in any position) counts as 1 over the share of the members "
         "enrolled all twelve months with the condition whom a claim identifies within the same number of months; a "
         "county's members with a condition are the sum over its identified members."),
        ("Reach", "Members with a serious mental illness who had an Appendix C service from a behavioral-health prescriber "
         "(every such member is among those a claim identifies), over the county's members with a serious mental illness."),
        ("Rounding", "Members with a condition are shown to the nearest 10, and the ratios (one decimal) and the reach (whole "
         "per cent) in the table are computed from the counts as shown. Whether a county meets a standard is decided on "
         "the unrounded estimates, as NP-31 3.2 requires; no county lies within 7 per cent of a threshold."),
        ("Practising prescribers", "NPPES monthly file of October 2026 updated by the weekly files through 1 November 2026; "
         "primary taxonomy in Appendix B; NPI active on 1 November; practice location ZIP code assigned to the county holding "
         "the larger share of its business addresses (HUD-USPS, second quarter 2026); rendering provider of a final claim or "
         "encounter for an adult member in the contract year."),
        ("Payments", "Final fee-for-service claims (frequency 7 replacements in place of the claims they replace, voided "
         "claims removed) whose rendering provider is a behavioral-health prescriber, each claim's paid amount once (it "
         "repeats on each line of the claim), by the member's county and the quarter of the service date. Sub-capitated "
         "encounters carry no payment."),
        ("Sources", "enrollment_spans_2025-07-01_2026-06-30.csv; bh_claims_encounters_dos_2025-07-01_2026-06-30.csv; "
         "npidata_pfile_wa_20050523-20261011.csv and the weekly files to 1 November 2026; ZIP_COUNTY_062026.xlsx; NP-31."),
    ]
    ws3.append(["Item", "Note"])
    for c in ws3[1]:
        c.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=navy)
    for k, v in notes:
        ws3.append([k, v])
        ws3.cell(row=ws3.max_row, column=1).font = Font(name="Calibri", size=10, bold=True)
        ws3.cell(row=ws3.max_row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws3.cell(row=ws3.max_row, column=1).alignment = Alignment(vertical="top")
    ws3.column_dimensions["A"].width = 22
    ws3.column_dimensions["B"].width = 120
    wb.save(path)


def write_conformed(a, f, path):
    cols = ["county_fips", "county", "elig_group_cd", "elig_group", "adult_members", "ffs_paid_bh_prescriber_usd"]
    fips = {v: k for k, v in CF.COUNTY_FIPS.items()}
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(cols)
        for c in CF.COUNTIES:
            for g in CF.GROUPS:
                x = f["conformed"]["%s|%s" % (c, g)]
                w.writerow([fips[c], c, g, GROUP_NAME[g], x["members"], x["paid"]])


def main(target, out, figures_path):
    os.makedirs(out, exist_ok=True)
    a = CF.analysis(target)
    f = figures(a)
    write_scorecard(a, f, os.path.join(out, SCORECARD))
    write_conformed(a, f, os.path.join(out, CONFORMED))
    with open(figures_path, "w") as fh:
        json.dump(f, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return {"analysis": a, "figures": f}
