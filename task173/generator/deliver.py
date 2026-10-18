"""task173 goldens from the shipped pack: the 2027 deadline-fortnight plan workbook (the booking and its working, the
check of the outsourcer's 2026 hours, the check of the 2026 waits) and generator/figures.json (every figure the
write-up states, as it states it). Everything is computed by calc.py and asks.py from the pack.

    python3 task173/generator/deliver.py <target> <golden dir> <figures.json>"""
from __future__ import annotations

import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as AS           # noqa: E402
import calc as C            # noqa: E402
import common as K          # noqa: E402
import postprocess as PP    # noqa: E402

F_BOOK = "deadline_fortnight_plan_2027.xlsx"
DAY3 = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MON3 = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def r1(x):
    return K.round_half_up(x, 1)


def week_label(wk):
    e = wk + dt.timedelta(6)
    if wk.month == e.month:
        return "%d to %d %s %d" % (wk.day, e.day, MON3[e.month], e.year)
    return "%d %s to %d %s %d" % (wk.day, MON3[wk.month], e.day, MON3[e.month], e.year)


def r0(x):
    return int(K.round_half_up(x, 0))


def compute(target):
    P = C.Pack(target)
    E = C.Est(P)
    g = C.golden(P, E)
    bt = C.backtest(P, E)
    f0, f1 = K.fortnight(K.SEASON_PLAN)
    days = [f0 + dt.timedelta(k) for k in range(14)]
    # the 2027 mix: the bench's contacts by group and the share of first contacts each group takes
    Kr = P.returning27 * C.H_EXPERT * 60 / E.aR
    Kn = sum(n * (C.H_EXPERT / 14) * 60 / C.expo((d - gl).days / 7.0, *E.ca) for d in days for gl, n in P.classes27)
    kO = C.H_BILLED * 60 / E.aO
    Kv = g["B"] * kO
    Ct = Kr + Kn + Kv
    pn = sum(n * (C.H_EXPERT / 14) * 60 / C.expo((d - gl).days / 7.0, *E.ca) * C.expo((d - gl).days / 7.0, *E.cp)
             for d in days for gl, n in P.classes27) / Kn
    classes = []
    for gl, n in P.classes27:
        xs = [(d - gl).days / 7.0 for d in days]
        classes.append(dict(golive=gl, seats=n, weeks_from=xs[0], weeks_to=xs[-1],
                            follow=sum(C.expo(x, *E.cp) for x in xs) / 14, handle=sum(C.expo(x, *E.ca) for x in xs) / 14))
    a = AS.ask_a(target)
    rows, crm = AS.ask_b_rows(target)
    b = AS.ask_b(target, rows, crm)
    rv, _ = C.rivals(P, E)
    default_order = K.ceil_to(rv["last season's contacts per new case, handle time by weeks on queue"], K.ORDER_BLOCK)
    rival_orders = {k: K.ceil_to(rv[k], K.ORDER_BLOCK) for k in (
        "first-contact rate by group, new hires at their season average",
        "bench's follow-ups only, vendor hours taken as pure capacity", "vendor agents at the returning rate")}
    return dict(P=P, E=E, g=g, bt=bt, Kr=Kr, Kn=Kn, Kv=Kv, Ct=Ct, pn=pn, classes=classes, a=a, b=b,
                default_order=default_order, rival_orders=rival_orders)


def write_book(path, X):
    import openpyxl
    from openpyxl.styles import Alignment, Font, PatternFill
    P, E, g = X["P"], X["E"], X["g"]
    bold = Font(bold=True)
    head_fill = PatternFill("solid", fgColor="DDE7EA")
    wb = openpyxl.Workbook()

    ws = wb.active
    ws.title = "2027 booking"
    f0, f1 = K.fortnight(K.SEASON_PLAN)
    ws["A1"] = "Hillsborough booking for the 2027 deadline fortnight: %s agent hours" % "{:,}".format(g["order"])
    ws["A1"].font = Font(bold=True, size=14)
    ws["A2"] = "Deadline fortnight %d %s to %d %s %d, English expert queue. Prepared %s for the %s leadership meeting." % (
        f0.day, MON3[f0.month], f1.day, MON3[f1.month], f1.year, K.short_date(K.AS_OF), K.short_date(K.MEETING))
    rows = [
        ("Order (whole blocks of 1,000 agent hours)", g["order"], "#,##0"),
        ("Billed agent hours the load needs", r0(g["B"]), "#,##0"),
        ("New expert cases in the fortnight (demand plan)", P.F27, "#,##0"),
        ("Forecast contacts on those cases", r0(g["contacts"]), "#,##0"),
        ("  of which follow-ups", r0(g["followups"]), "#,##0"),
        ("Contacts the in-house bench carries", r0(g["inhouse_contacts"]), "#,##0"),
        ("Contacts Hillsborough's agents carry", r0(g["vendor_contacts"]), "#,##0"),
        ("Contacts per new case, 2027 fortnight (forecast)", round(g["contacts"] / P.F27, 3), "0.000"),
        ("Contacts per new case, 2026 fortnight (CRM)", round(1 + X["bt"]["rate26"], 3), "0.000"),
    ]
    for k, (lab, val, fmt) in enumerate(rows):
        c = ws.cell(row=4 + k, column=1, value=lab)
        v = ws.cell(row=4 + k, column=2, value=val)
        v.number_format = fmt
        if k == 0:
            c.font = bold
            v.font = bold
    r = 14
    ws.cell(row=r, column=1, value="Who takes the fortnight's contacts").font = bold
    r += 1
    for j, h in enumerate(["Group", "Experts or hours", "Contacts", "Share of contacts",
                           "Chance a case they open needs a follow-up", "Handle minutes"]):
        c = ws.cell(row=r, column=j + 1, value=h)
        c.font = bold
        c.fill = head_fill
    lines = [("Returning experts", "%d experts" % P.returning27, X["Kr"], E.pR, E.aR),
             ("2027 classes (4 x 60 seats)", "%d seats" % sum(n for _, n in P.classes27), X["Kn"], X["pn"],
              X["Kn"] and sum(c["seats"] for c in X["classes"]) * C.H_EXPERT * 60 / X["Kn"]),
             ("Hillsborough agents", "%s billed hours" % "{:,}".format(r0(g["B"])), X["Kv"], E.pO, E.aO)]
    for lab, who, kc, p, aht in lines:
        r += 1
        ws.cell(row=r, column=1, value=lab)
        ws.cell(row=r, column=2, value=who)
        ws.cell(row=r, column=3, value=r0(kc)).number_format = "#,##0"
        ws.cell(row=r, column=4, value=round(kc / X["Ct"], 3)).number_format = "0.0%"
        ws.cell(row=r, column=5, value=round(p, 3)).number_format = "0.0%"
        ws.cell(row=r, column=6, value=round(aht, 1)).number_format = "0.0"
    r += 1
    ws.cell(row=r, column=1, value="A follow-up's own chance of another follow-up, whoever takes it")
    ws.cell(row=r, column=5, value=round(E.q, 3)).number_format = "0.0%"
    r += 2
    ws.cell(row=r, column=1, value="2027 classes in the fortnight").font = bold
    r += 1
    for j, h in enumerate(["Goes live", "Seats", "Weeks on queue in the fortnight", "Follow-up chance (average)",
                           "Handle minutes (average)"]):
        c = ws.cell(row=r, column=j + 1, value=h)
        c.font = bold
        c.fill = head_fill
    for c in X["classes"]:
        r += 1
        ws.cell(row=r, column=1, value=c["golive"]).number_format = "d mmm yyyy"
        ws.cell(row=r, column=2, value=c["seats"])
        ws.cell(row=r, column=3, value="%.1f to %.1f" % (c["weeks_from"], c["weeks_to"]))
        ws.cell(row=r, column=4, value=round(c["follow"], 3)).number_format = "0.0%"
        ws.cell(row=r, column=5, value=round(c["handle"], 1)).number_format = "0.0"
    r += 2
    ws.cell(row=r, column=1, value="Back-test of the follow-up model on the old ticketing system").font = bold
    r += 1
    for j, h in enumerate(["Season", "Deadline fortnight: follow-ups per new ticket", "Model", "Last season's rate",
                           "Whole season: follow-ups per new ticket", "Model", "Last season's rate"]):
        c = ws.cell(row=r, column=j + 1, value=h)
        c.font = bold
        c.fill = head_fill
    for fn, se in zip(X["bt"]["fortnight"], X["bt"]["season"]):
        r += 1
        ws.cell(row=r, column=1, value=fn["season"])
        for j, v in enumerate([fn["observed"], fn["model"], fn["rate26"], se["observed"], se["model"], se["rate26"]]):
            ws.cell(row=r, column=2 + j, value=round(v, 3)).number_format = "0.000"
    r += 2
    notes = [
        "Load as the capacity standard defines it: every contact on the cases that open in the fortnight, follow-ups "
        "included whenever they come. In-house experts at 90 scheduled hours, 12% shrinkage and 85% occupancy "
        "(67.32 handle hours each); a billed Hillsborough hour gives 0.85 handle hours.",
        "Whether a case comes back is set by who takes its first contact: returning experts, a new class by its weeks "
        "on the queue, or Hillsborough's agents. Follow-ups are routed to whoever is free and come back at about one "
        "rate whoever takes them.",
        "The more hours Hillsborough carries, the more first contacts its agents take and the more follow-ups come "
        "back, so the booking is the one that carries the load it creates.",
        "Rates from the 2026 CRM (cases followed through to their last contact); handle time is talk plus "
        "after-contact work.",
    ]
    for t in notes:
        ws.cell(row=r, column=1, value=t).alignment = Alignment(wrap_text=False)
        r += 1
    ws.column_dimensions["A"].width = 52
    for col in "BCDEFG":
        ws.column_dimensions[col].width = 18

    # the outsourcer's hours
    ws2 = wb.create_sheet("2026 Hillsborough hours")
    ws2["A1"] = "Hillsborough's 2026 deadline fortnight: billable hours in our ACD and hours invoiced without support"
    ws2["A1"].font = Font(bold=True, size=13)
    ws2["A2"] = ("Billable time as Schedule B defines it (Available, On Contact, After-Contact Work), each agent's "
                 "time counted once across logins and sessions, by Eastern date.")
    for j, h in enumerate(["Date", "Day", "Billable hours (ACD)"]):
        c = ws2.cell(row=4, column=j + 1, value=h)
        c.font = bold
        c.fill = head_fill
    for k, d in enumerate(AS.fortnight_days()):
        ws2.cell(row=5 + k, column=1, value=d).number_format = "d mmm yyyy"
        ws2.cell(row=5 + k, column=2, value=DAY3[d.weekday()])
        ws2.cell(row=5 + k, column=3, value=r1(X["a"]["daily"][d])).number_format = "#,##0.0"
    tot = ws2.cell(row=5 + 14, column=1, value="Fortnight")
    tot.font = bold
    v = ws2.cell(row=5 + 14, column=3, value=r1(sum(X["a"]["daily"].values())))
    v.number_format = "#,##0.0"
    v.font = bold
    ws2.freeze_panes = "A5"
    rr = 5 + 14 + 2
    for j, h in enumerate(["Invoice week", "Invoice", "Hours invoiced, not supported (agent by agent)"]):
        c = ws2.cell(row=rr, column=j + 1, value=h)
        c.font = bold
        c.fill = head_fill
    for k, wk in enumerate(AS.weeks()):
        ws2.cell(row=rr + 1 + k, column=1, value=week_label(wk))
        ws2.cell(row=rr + 1 + k, column=2, value=X["a"]["invoices"][wk])
        ws2.cell(row=rr + 1 + k, column=3, value=r1(X["a"]["unsupported"][wk])).number_format = "#,##0.0"
    ws2.cell(row=rr + 4, column=1, value="The week of 27 April is checked against invoice HCS-26-0478 of 19 May, which "
                                         "replaced HCS-26-0446. Team leads' time and every Not Ready state are left out, "
                                         "per Schedule B.2.")
    ws2.column_dimensions["A"].width = 22
    ws2.column_dimensions["B"].width = 14
    ws2.column_dimensions["C"].width = 44

    # the waits
    ws3 = wb.create_sheet("2026 waits")
    ws3["A1"] = "English queue, 2026 deadline fortnight: waits of the customers an expert answered"
    ws3["A1"].font = Font(bold=True, size=13)
    ws3["A2"] = ("Wait from first joining the queue to the start of the conversation (CRM), counted on the Eastern "
                 "date the customer joined.")
    for j, h in enumerate(["Date", "Day", "Customers answered", "Average wait (seconds)"]):
        c = ws3.cell(row=4, column=j + 1, value=h)
        c.font = bold
        c.fill = head_fill
    for k, d in enumerate(AS.fortnight_days()):
        ws3.cell(row=5 + k, column=1, value=d).number_format = "d mmm yyyy"
        ws3.cell(row=5 + k, column=2, value=DAY3[d.weekday()])
        ws3.cell(row=5 + k, column=3, value=X["b"]["per_day"][d]).number_format = "#,##0"
        ws3.cell(row=5 + k, column=4, value=r0(X["b"]["daily"][d])).number_format = "0"
    tot = ws3.cell(row=5 + 14, column=1, value="Fortnight")
    tot.font = bold
    v = ws3.cell(row=5 + 14, column=3, value=sum(X["b"]["per_day"].values()))
    v.number_format = "#,##0"
    v.font = bold
    ws3.freeze_panes = "A5"
    ws3.cell(row=5 + 16 + 4, column=1, value="Customers who left the queue before an expert answered are not in either "
                                             "figure; a customer who came back later is counted on the later visit.")
    rr = 5 + 14 + 2
    for j, h in enumerate(["Week", "Customers answered", "Answered within three minutes"]):
        c = ws3.cell(row=rr, column=j + 1, value=h)
        c.font = bold
        c.fill = head_fill
    for k, wk in enumerate(AS.weeks()):
        ws3.cell(row=rr + 1 + k, column=1, value=week_label(wk))
        ws3.cell(row=rr + 1 + k, column=2, value=X["b"]["answered"][wk]).number_format = "#,##0"
        ws3.cell(row=rr + 1 + k, column=3, value=round(r1(X["b"]["share"][wk]) / 100, 4)).number_format = "0.0%"
    ws3.column_dimensions["A"].width = 22
    for col in "BCD":
        ws3.column_dimensions[col].width = 26

    ws4 = wb.create_sheet("Notes")
    notes = [
        ("Prepared", "%s, Workforce Planning, from the files pulled on 29 and 30 October 2026" % K.short_date(K.AS_OF)),
        ("Standard", "Expert capacity planning standard v3.2 (14 September 2026): the fortnight, the load, capacity, "
                     "the order blocks and the service-level definition"),
        ("Bench", "Roster recall answers to 23 October 2026; training calendar of 26 October 2026, seats as filled"),
        ("Demand", "Demand plan of 16 October 2026, the fortnight's 14 days"),
        ("2026 rates", "CRM interaction export, English queue, 12 January to 31 May 2026; each case followed from its "
                       "opening interaction to its last"),
        ("Back-test", "Old ticketing system weekly agent reports, 2021 to 2025, linked to the HR seasonal history"),
        ("Hillsborough hours", "ACD agent state detail for the HCS Moncton team; invoices HCS-26-0431 and HCS-26-0478; "
                               "Schedule B as amended 2 March 2026"),
        ("Waits", "ACD contact detail, English queue, customers joining 20 April to 3 May 2026; conversation start "
                  "from the CRM"),
        ("Dates", "Eastern Time throughout; the ACD and CRM export UTC"),
    ]
    ws4["A1"] = "Notes and sources"
    ws4["A1"].font = Font(bold=True, size=13)
    for k, (a_, b_) in enumerate(notes):
        ws4.cell(row=3 + k, column=1, value=a_).font = bold
        ws4.cell(row=3 + k, column=2, value=b_)
    ws4.column_dimensions["A"].width = 22
    ws4.column_dimensions["B"].width = 110
    for w in (ws, ws2, ws3):
        w.page_setup.orientation = "landscape"
        w.page_setup.fitToWidth = 1
        w.sheet_properties.pageSetUpPr.fitToPage = True
    wb.save(path)


def figures(X):
    P, E, g, bt = X["P"], X["E"], X["g"], X["bt"]
    fj = {
        "call": "Book %s agent hours with Hillsborough Contact Services for the 2027 deadline fortnight" % "{:,}".format(
            g["order"]),
        "booking_blocks": g["order"],
        "billed_hours_needed": r0(g["B"]),
        "new_cases_2027": P.F27,
        "new_cases_2026": P.F26,
        "growth_pct": K.round_half_up(100 * K.GROWTH_2027, 1),
        "forecast_contacts": r0(g["contacts"]),
        "forecast_followups": r0(g["followups"]),
        "inhouse_contacts": r0(g["inhouse_contacts"]),
        "vendor_contacts": r0(g["vendor_contacts"]),
        "returning_2027": P.returning27,
        "class_seats": sum(n for _, n in P.classes27),
        "handle_hours_per_expert": K.HANDLE_PER_EXPERT,
        "handle_per_billed": K.HANDLE_PER_BILLED,
        "follow_returning_pct": K.round_half_up(100 * E.pR, 1),
        "follow_vendor_pct": K.round_half_up(100 * E.pO, 1),
        "follow_new_2027_pct": K.round_half_up(100 * X["pn"], 1),
        "follow_q_pct": K.round_half_up(100 * E.q, 1),
        "aht_returning": K.round_half_up(E.aR, 1),
        "aht_vendor": K.round_half_up(E.aO, 1),
        "contacts_per_case_2027": K.round_half_up(g["contacts"] / P.F27, 3),
        "contacts_per_case_2027_2dp": K.round_half_up(g["contacts"] / P.F27, 2),
        "contacts_per_case_2026_2dp": K.round_half_up(1 + bt["rate26"], 2),
        "forecast_contacts_thousand": int(K.round_half_up(g["contacts"] / 1000) * 1000),
        "follow_new_week1_pct": K.round_half_up(100 * C.expo(1.0, *E.cp), 1),
        "follow_new_week10_pct": K.round_half_up(100 * C.expo(10.0, *E.cp), 1),
        "aht_new_week1": K.round_half_up(C.expo(1.0, *E.ca), 1),
        "aht_new_week10": K.round_half_up(C.expo(10.0, *E.ca), 1),
        "block_hours": K.ORDER_BLOCK,
        "class_size": K.CLASS_SEATS,
        "schedule_hours": K.SCHEDULE_HOURS,
        "shrinkage_pct": round(100 * K.SHRINKAGE),
        "occupancy_pct": round(100 * K.OCCUPANCY),
        "default_order": X["default_order"],
        "rival_orders": X["rival_orders"],
        "contacts_per_case_2026_fortnight": K.round_half_up(1 + bt["rate26"], 3),
        "backtest": [dict(season=f["season"], fortnight_observed=K.round_half_up(f["observed"], 3),
                          fortnight_model=K.round_half_up(f["model"], 3),
                          season_observed=K.round_half_up(s["observed"], 3), season_model=K.round_half_up(s["model"], 3))
                     for f, s in zip(bt["fortnight"], bt["season"])],
        "backtest_rate26": K.round_half_up(bt["rate26"], 3),
        "backtest_max_err_model_fortnight": K.round_half_up(max(abs(f["err_model"]) for f in bt["fortnight"]), 1),
        "backtest_max_err_rate_fortnight": K.round_half_up(max(abs(f["err_rate"]) for f in bt["fortnight"]), 1),
        "backtest_max_err_model_season": K.round_half_up(max(abs(s["err_model"]) for s in bt["season"]), 1),
        "backtest_max_err_rate_season": K.round_half_up(max(abs(s["err_rate"]) for s in bt["season"]), 1),
        "ask_a_daily": {d.isoformat(): r1(v) for d, v in X["a"]["daily"].items()},
        "ask_a_unsupported": {wk.isoformat(): r1(v) for wk, v in X["a"]["unsupported"].items()},
        "ask_a_invoices": {wk.isoformat(): v for wk, v in X["a"]["invoices"].items()},
        "ask_b_daily_wait": {d.isoformat(): r0(v) for d, v in X["b"]["daily"].items()},
        "ask_b_share": {wk.isoformat(): r1(v) for wk, v in X["b"]["share"].items()},
        "ask_b_answered": {wk.isoformat(): v for wk, v in X["b"]["answered"].items()},
    }
    return fj


def main(target, golden, fig_path):
    os.makedirs(golden, exist_ok=True)
    X = compute(target)
    p = os.path.join(golden, F_BOOK)
    write_book(p, X)
    P = K.PEOPLE
    PP.normalize_ooxml(p, P["wfm"], P["wfm"], "2026-10-27T13:05:00Z", "2026-10-30T20:48:00Z", excel=True,
                       company=K.COMPANY)
    with open(fig_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(figures(X), fh, indent=1, ensure_ascii=False, sort_keys=False)
        fh.write("\n")
    return X


if __name__ == "__main__":
    main(*sys.argv[1:4])
