"""The golden deliverable, fy2026_hospice_cap_accrual.xlsx, and the figures it states."""
import datetime as dt

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import world as W
import records as R
import golden as Gd

GROUP = {"C": "Cancer", "D": "Dementia", "P": "Heart and lung", "O": "Other"}


def payments_by_ccn(remit):
    pay = {}
    for r in remit:
        if r["record"] == "CLP":
            pay[r["provider_number"]] = pay.get(r["provider_number"], 0.0) + r["paid"] + r["sequestration"]
    return {k: round(v, 2) for k, v in pay.items()}


def inpatient(P):
    paid = R.paid_versions(P["claims"])
    out = {}
    for code in W.CODES:
        ccn = R.CCN[code]
        g = sum(R.paid_units(c, "G") for c in paid if c["code"] == code)
        i = sum(R.paid_units(c, "I") for c in paid if c["code"] == code)
        days = P["days"][ccn]
        out[ccn] = dict(gip=g, irc=i, days=days, share=100.0 * (g + i) / days)
    return out


def m1(x):
    return round(x / 1e6 + 1e-12, 1)


def write(P, path):
    est, cohort = P["est"], P["cohort"]
    pay = payments_by_ccn(P["remit"])
    counts = P["gold"]
    sched = Gd.schedule(cohort, est, **Gd.RUNGS["G"])
    inp = inpatient(P)
    order = [R.CCN[c] for c in W.CODES]
    inv = {v: k for k, v in R.CCN.items()}
    rep = {ccn: Gd.repayment(pay[ccn], counts[ccn]) for ccn in order}
    total = sum(rep.values())

    wb = openpyxl.Workbook()
    thin = Side(style="thin", color="999999")
    bold = Font(bold=True)
    head_fill = PatternFill("solid", fgColor="DDE4EE")

    ws = wb.active
    ws.title = "Summary"
    owing = [ccn for ccn in order if rep[ccn] > 0]
    ws["A1"] = "Wendleglen Hospice & Palliative Care"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("FY2026 Medicare hospice aggregate cap: accrue USD %.1f million at 31 December 2026, %s" % (
        m1(total), "all at %s (%s)" % (R.PROGRAM[inv[owing[0]]], owing[0]) if len(owing) == 1 else "at %d provider numbers" % len(owing)))
    ws["A2"].font = Font(bold=True)
    ws["A3"] = "Cap year 1 October 2025 to 30 September 2026; proportional method; policy FIN-14 (18 November 2026)."
    hdr = ["Provider number", "Program", "FY2026 payments before sequestration (USD)", "Beneficiaries counted",
           "Aggregate cap (USD)", "Payments / cap", "Estimated repayment (USD)", "Accrual (USD millions)"]
    ws.append([])
    ws.append(hdr)
    for c in ws[5]:
        c.font = bold
        c.fill = head_fill
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for ccn in order:
        cnt = counts[ccn]
        ws.append([ccn, R.PROGRAM[inv[ccn]], pay[ccn], round(cnt, 2), round(cnt * W.CAP, 2), round(pay[ccn] / (cnt * W.CAP), 4),
                   round(rep[ccn], 2), m1(rep[ccn])])
    ws.append(["Total", None, round(sum(pay.values()), 2), None, None, None, round(total, 2), m1(total)])
    for c in ws[ws.max_row]:
        c.font = bold
    ws.append([])
    ws.append(["Cap amount USD 35,361.44 per beneficiary (FY2026 rate sheet). Repayment is 98 per cent of the payments less the "
               "cap where the payments exceed it (FIN-14 section 3.2); each accrual is rounded from its unrounded repayment and "
               "the total from the sum of the unrounded repayments."])
    ws.append(["Fallowmere Hospice: provider agreement assigned to Wendleglen on 1 March 2025; its cap years before and after "
               "that date are one provider number's (FIN-14 section 1)."])
    for col, w in zip("ABCDEFGH", (15, 20, 22, 14, 18, 12, 18, 14)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "C6"
    ws.print_title_rows = "5:5"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    for row in ws.iter_rows(min_row=6, max_row=6 + len(order), min_col=3, max_col=8):
        for c in row:
            if c.column in (3, 5, 7):
                c.number_format = "#,##0.00"
            elif c.column == 6:
                c.number_format = "0.0000"
            elif c.column == 8:
                c.number_format = "0.0"
            elif c.column == 4:
                c.number_format = "0.00"

    ws2 = wb.create_sheet("Cap schedule")
    hdr2 = ["MBI", "Provider number", "Program", "Diagnosis group", "State at 31 Dec 2026", "FY2026 days at provider number",
            "Hospice days to 31 Dec 2026 (every hospice)", "Days expected after 31 Dec 2026", "Share of a beneficiary counted"]
    ws2.append(hdr2)
    for c in ws2[1]:
        c.font = bold
        c.fill = head_fill
        c.alignment = Alignment(wrap_text=True, vertical="top")
    state = {r["mbi"]: r for r in cohort}
    label = {"open": "On service", "out": "Discharged alive", "dead": "Died"}
    for s in sorted(sched, key=lambda s: (order.index(s["ccn"]), s["mbi"])):
        r = state[s["mbi"]]
        ws2.append([s["mbi"], s["ccn"], R.PROGRAM[inv[s["ccn"]]], GROUP[r["g"]] if r["g"] in GROUP else r["g"],
                    label[r["state"][0]], s["fy_days"], s["known"], round(s["expected_after"], 1), round(s["share"], 4)])
    for col, w in zip("ABCDEFGHI", (14, 11, 18, 14, 16, 12, 14, 12, 12)):
        ws2.column_dimensions[col].width = w
    for row in ws2.iter_rows(min_row=2, max_row=ws2.max_row, min_col=6, max_col=9):
        for c in row:
            c.number_format = {6: "#,##0", 7: "#,##0", 8: "#,##0.0", 9: "0.0000"}[c.column]
    ws2.freeze_panes = "B2"
    ws2.auto_filter.ref = "A1:I%d" % ws2.max_row
    ws2.print_title_rows = "1:1"

    ws3 = wb.create_sheet("Inpatient cap")
    hdr3 = ["Provider number", "Program", "General inpatient days paid", "Inpatient respite days paid",
            "FY2026 days of care", "Inpatient share (%)", "Limit (%)", "Over the limit"]
    ws3.append(hdr3)
    for c in ws3[1]:
        c.font = bold
        c.fill = head_fill
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for ccn in order:
        x = inp[ccn]
        ws3.append([ccn, R.PROGRAM[inv[ccn]], x["gip"], x["irc"], x["days"], round(x["share"], 1), 20, "No"])
    for row in ws3.iter_rows(min_row=2, max_row=ws3.max_row, min_col=3, max_col=7):
        for c in row:
            c.number_format = {3: "#,##0", 4: "#,##0", 5: "#,##0", 6: "0.0", 7: "0"}[c.column]
    ws3.append([])
    ws3.append(["Days paid: units at revenue codes 0656 and 0655 on the version of each FY2026 claim the remittance register "
                "shows paid and not reversed, less the days the contractor paid at the routine home care rate (each payment "
                "repriced from the FY2026 rates and the provider number's wage index). Days "
                "of care: each FY2026 day at the provider number once, at any level of care (benefit periods extract); "
                "continuous home care lines (0652) are in 15-minute units. Limit: 42 CFR 418.302(f)."])
    for col, w in zip("ABCDEFGH", (15, 20, 14, 14, 14, 12, 9, 10)):
        ws3.column_dimensions[col].width = w
    ws3.freeze_panes = "C2"

    ws4 = wb.create_sheet("Basis")
    n_bens = len({s["mbi"] for s in sched})
    lines = [
        "Basis of the estimate",
        "As of 31 December 2026. Population: %s Medicare beneficiaries with a day of care at one of the eight provider numbers "
        "in FY2026, %s schedule rows (a beneficiary cared for by two provider numbers has a row at each)." % (
            format(n_bens, ","), format(len(sched), ",")),
        "Days on file: Medicare benefit periods extract run 5 January 2027, data through 31 December 2026, every hospice and year; "
        "the benefit periods of one election chained into one stay.",
        "Expected days after the close, from the experience since 1 October 2016 of the provider number that cared for the "
        "beneficiary last, by diagnosis group:",
        "  On service: the further days of the provider number's stays of the group that had run as long (Kaplan-Meier), plus "
        "the chance such a stay ends alive times the chance of a later election times the days a later election brings.",
        "  Discharged alive: the chance of a later election at any hospice among the provider number's live discharges still "
        "alive and not back after as many days out (Aalen-Johansen), times the days a later election brings (Kaplan-Meier "
        "mean of those elections).",
        "  Died: none.",
        "Payments: remittance register, FY2026 statement months, reversals netted, sequestration added back, interest excluded.",
        "Inpatient days: the claim versions the remittance register shows paid and not reversed, each repriced from the "
        "FY2026 rates and the provider number's wage index; days paid at the routine home care rate are not inpatient days "
        "paid.",
        "Records: medicare_hospice_benefit_periods_20270105.txt, wendleglen_emr_admissions.csv, "
        "fallowmere_census_register_20250228.xlsx, hicn_mbi_crosswalk.csv, diagnosis_groups.csv, "
        "wendleglen_claim_lines_fy2026.csv, remittance_register_fy2026.csv; policy FIN-14.",
    ]
    for ln in lines:
        ws4.append([ln])
    ws4["A1"].font = bold
    ws4.column_dimensions["A"].width = 150

    wb.properties.creator = "B. Graham"
    wb.properties.lastModifiedBy = "B. Graham"
    wb.properties.created = dt.datetime(2027, 1, 8, 10, 20)
    wb.properties.modified = dt.datetime(2027, 1, 11, 17, 2)
    wb.save(path)

    figs = {"call": {"total_musd": m1(total), "total_usd": round(total, 2), "owing": [inv[c] for c in order if rep[c] > 0]},
            "repayment_usd": {inv[c]: round(rep[c], 2) for c in order},
            "repayment_musd": {inv[c]: m1(rep[c]) for c in order},
            "payments_usd": {inv[c]: pay[c] for c in order},
            "count": {inv[c]: round(counts[c], 4) for c in order},
            "cap_usd": {inv[c]: round(counts[c] * W.CAP, 2) for c in order},
            "ratio": {inv[c]: round(pay[c] / (counts[c] * W.CAP), 4) for c in order},
            "wage_index": P["wi"],
            "ask_a": {inv[c]: {"gip_days": inp[c]["gip"], "respite_days": inp[c]["irc"], "days_of_care": inp[c]["days"],
                               "share_pct": round(inp[c]["share"], 1), "share_exact": round(inp[c]["share"], 4)} for c in order},
            "schedule_rows": len(sched)}
    fal = R.CCN["FAL"]
    fal_rows = [r for r in cohort if fal in r["fy"]]
    figs["cohort_n"] = len(cohort)
    figs["fal_n"] = len(fal_rows)
    figs["fal_states"] = {k: sum(1 for r in fal_rows if r["state"][0] == k) for k in ("open", "out", "dead")}
    figs["fal_fy_days"] = sum(r["fy"][fal] for r in fal_rows)
    figs["cap_amount"] = W.CAP
    figs["extract_stays"] = sum(len(v) for v in P["book"].stays.values())
    figs["provider_numbers"] = {c: R.CCN[c] for c in W.CODES}
    figs["history"] = history(P)
    figs["policy"] = {"sections": [2.1, 2.3, 2.4, 3.2], "repayment_share_pct": 98, "sequestration_pct": 2}
    figs["revenue_codes"] = {"general_inpatient": "0656", "respite": "0655"}
    figs["dates"] = {"close": [31, "December", 2026], "experience_from": [1, "October", 2016]}
    return figs


def history(P):
    """The history the stump and the write-up describe, measured on the pack's own experience tables: the share of
    elections that ended alive, how often and how soon a live discharge comes back, where Fallowmere's returns went, and
    the return chance at discharge and after 90 days out for Fallowmere's dementia beneficiaries."""
    book, est = P["book"], P["est"]
    fal = R.CCN["FAL"]
    alive = {}
    for code in W.CODES:
        ccn = R.CCN[code]
        rows = [x for (c, g), v in book.stay_rows.items() if c == ccn for x in v if x[1] != "cen"]
        alive[code] = sum(1 for x in rows if x[1] == "live") / len(rows)
    seven = [x for (c, g), v in book.stay_rows.items() if c != fal for x in v if x[1] != "cen"]
    lv = [x for v in book.live_rows.values() for x in v]
    rets = [t for t, k, fu in lv if k == "ret"]
    tot = out = 0
    for m, lst in book.stays.items():
        for k, st in enumerate(lst):
            if st["open"] or st["death"] or st["last"] != fal or st["end"] > W.CLOSE:
                continue
            nx = lst[k + 1] if k + 1 < len(lst) and lst[k + 1]["start"] < W.CLOSE else None
            if nx:
                tot += 1
                out += nx["first"] not in book.wendleglen
    p, finf = est.get("aj", (fal, "Dementia"))
    return {"alive_share": {c: round(v, 4) for c, v in alive.items()},
            "seven_alive_share": round(sum(1 for x in seven if x[1] == "live") / len(seven), 4),
            "live_return_share": round(len(rets) / len(lv), 4),
            "returns_within_30": round(sum(1 for t in rets if t <= 30) / len(rets), 4),
            "fal_returns_outside": round(out / tot, 4),
            "fal_dementia_return_at_0": round(p(0), 4), "fal_dementia_return_at_90": round(p(90), 4)}


def in_words(x):
    """A share as the plain fraction a finance note would use (two in five), the nearest with a denominator to five."""
    best = min(((n, d) for d in (2, 3, 4, 5) for n in range(1, d)), key=lambda nd: (abs(x - nd[0] / nd[1]), nd[1]))
    words = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five"}
    return "%s in %s" % (words[best[0]], words[best[1]])
