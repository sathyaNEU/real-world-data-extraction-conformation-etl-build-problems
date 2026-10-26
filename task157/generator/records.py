"""task157 records: the world and the operating layer shaped into the exports Larch Rides' systems write.

The old dispatch platform (launch to Sunday 14 July 2024): its monthly driver export by legacy driver number. The new
dispatch platform's warehouse (from Monday 15 July 2024): the monthly driver activity extract run on Sunday 3 January
2027, the migration crosswalk and the accounts register. The payments system: the 2025 main run (the old payout
report, amounts in cents), the 2026 main run, the adjustment runs, and the guarantee payouts' events; the bank's ACH
returns report for the payout account. The onboarding tool's applications from its go-live on 2 June 2025 and the
screening vendor's order export. The referral programme's 2026 bonuses and the marketplace team's Q1 2027 demand plan
(neither is read by the fund or the asks)."""
from __future__ import annotations

import datetime as dt

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import common as K
import ops as OP
import world as WD

F_LEGACY = "dispatch_legacy_driver_months_2021-05_2024-07.csv"
F_ACTIVITY = "driver_activity_monthly_2024-07_2027-01.csv"
F_CROSSWALK = "dispatch_migration_driver_crosswalk.csv"
F_ACCOUNTS = "driver_accounts_2027-01-03.csv"
F_RUN25 = "winter_guarantee_2025_payout_run.xlsx"
F_RUN26 = "winter_guarantee_2026_payout_run.csv"
F_ADJ = "guarantee_payout_adjustments_2025-2026.csv"
F_RETURNS = "ach_returns_payout_account_2025-2026.csv"
F_EVENTS = "guarantee_payout_events_2025-2026.csv"
F_APPS = "onboarding_applications_2025-06-02_2027-01-03.csv"
F_ORDERS = "background_check_orders_2025-06_2027-01.csv"
F_REFERRAL = "driver_referral_bonuses_2026.csv"
F_DEMAND = "rider_demand_plan_q1_2027.xlsx"

PROGRAM = {2025: "WG2025", 2026: "WG2026"}
BATCH_MAIN = {2025: "WG25-MAIN-0214", 2026: "WG26-MAIN-0213"}


def utc(t):
    """Naive Central time to a UTC timestamp string."""
    return K.to_utc(t).strftime("%Y-%m-%d %H:%M:%S")


def utc_z(t):
    return K.to_utc(t).strftime("%Y-%m-%dT%H:%M:%SZ")


class Shaped:
    pass


def shape(W, O):
    """Everything the writers need, decided once: which accounts exist at the extract, statuses and last trips,
    cancellations, the export cut of the onboarding tool and the vendor's orders."""
    S = Shaped()
    asof_end = dt.datetime.combine(K.AS_OF, dt.time(21, 40))
    # accounts open at the extract run
    S.exists = [O.created[k] <= asof_end for k in range(O.n_acc)]
    # cancellations at each driver's own rate, cell by cell
    r = K.rng("cancel_cells", "old")
    S.C_old = r.poisson(O.T_old * O.cancel_rate[:, None]).astype(int)
    r = K.rng("cancel_cells", "new")
    S.C_new = r.poisson(O.T_new * O.cancel_rate[:, None]).astype(int)
    # last trip day on or before the run, inside the last month the extract shows trips for
    S.last_trip = {}
    end_w = K.ASOF_W[2027]
    for k in range(W.n):
        act = np.nonzero(W.has[k, :end_w + 1])[0]
        if not len(act):
            continue
        lw = int(act[-1])
        d0 = K.wdate(lw)
        days = [d0 + dt.timedelta(days=j) for j in range(7)]
        newm = np.nonzero(O.T_new[k] > 0)[0]
        oldm = np.nonzero(O.T_old[k] > 0)[0]
        mon = O.ml_new[int(newm[-1])] if len(newm) else O.ml_old[int(oldm[-1])]
        cand = [j for j in range(7) if K.ym(days[j]) == mon and days[j] <= K.AS_OF]
        if not cand:
            cand = [j for j in range(7) if days[j] <= K.AS_OF]
        rr = K.rng("lasttrip", k)
        p = WD.WEEKDAY_W[cand] / WD.WEEKDAY_W[cand].sum()
        S.last_trip[k] = days[cand[int(rr.choice(len(cand), p=p))]]
    # status at the run
    app_of = {a["acc"]: a for a in O.apps if a.get("acc") is not None and not a.get("is_prior")}
    S.status, S.closed = {}, {}
    rd = K.rng("deactivate")
    for k in range(O.n_acc):
        if not S.exists[k]:
            continue
        if k in O.merged_into:
            S.status[k] = "merged"
            S.closed[k] = O.merged_into[k][1]
            continue
        lt = S.last_trip.get(k)
        u = rd.random()
        if k < W.n and W.kind[k] in ("R", "N", "I") and lt is not None and (K.AS_OF - lt).days > 200 and u < 0.06:
            S.status[k] = "deactivated"
            S.closed[k] = min(lt + dt.timedelta(days=int(rd.integers(150, 420))), K.AS_OF - dt.timedelta(days=3))
            continue
        if lt is None:
            app = app_of.get(k)
            lapsed = app is not None and app["outcome"] == "approval_lapsed"
            S.status[k] = "inactive" if lapsed else "new"
        else:
            S.status[k] = "active" if (K.AS_OF - lt).days <= 30 else "inactive"
    # the onboarding tool as exported on the run date
    S.apps = []
    for a in O.apps:
        if a["first_sub"] > asof_end:
            continue
        b = dict(a)
        if a["resubmitted"] is not None and a["resubmitted"] <= asof_end:
            b["submitted_shown"] = a["resubmitted"]
        else:
            b["submitted_shown"] = a["first_sub"]
        if (a["resubmitted"] is not None and a["resubmitted"] > asof_end) or a["decision"] is None or \
                a["decision"] > asof_end:
            b["status"], b["decision_shown"], b["driver"] = "in_review", None, None
        else:
            b["status"] = a["outcome"]
            b["decision_shown"] = a["decision"]
            b["driver"] = O.driver_id[a["acc"]] if a["outcome"] in ("approved", "approval_lapsed") else None
        ft = a.get("first_trip_seen")
        b["first_trip_shown"] = ft if (ft is not None and b["driver"] is not None) else None
        S.apps.append(b)
    S.orders = [b for b in S.apps if b["ordered"] <= asof_end]
    return S


# ------------------------------------------------------------------------------------------------- activity
LEGACY_COLS = ["MONTH", "DRIVER_NO", "COMPLETED_TRIPS", "DRIVER_CANCELS", "ONLINE_HRS"]
ACTIVITY_COLS = ["activity_month", "driver_id", "trips_completed", "trips_cancelled_by_driver", "online_minutes"]


def legacy_rows(W, O, S):
    switch = {}
    for k, (w2, n2) in O.legacy_second.items():
        switch[k] = (K.ym(K.wdate(w2)), n2)
    out = []
    idle = O.idle["old"]
    for j, m in enumerate(O.ml_old):
        rows = []
        for k in np.nonzero((O.T_old[:, j] > 0))[0]:
            k = int(k)
            if k not in O.legacy_no:
                continue
            no = O.legacy_no[k]
            if k in switch and m >= switch[k][0]:
                no = switch[k][1]
            hrs = max(0.1, K.round_half_up(float(O.H_old[k, j]), 1))
            rows.append([K.ym_str(m), no, int(O.T_old[k, j]), int(S.C_old[k, j]), "%.1f" % hrs])
        for (k, jj), mins in idle.items():
            if jj != j or k not in O.legacy_no:
                continue
            no = O.legacy_no[k]
            if k in switch and m >= switch[k][0]:
                no = switch[k][1]
            rows.append([K.ym_str(m), no, 0, int(K.rng("idlec", "old", k, j).random() < 0.2),
                         "%.1f" % max(0.1, K.round_half_up(mins / 60.0, 1))])
        rows.sort(key=lambda x: x[1])
        out.extend(rows)
    return out


def activity_rows(W, O, S):
    out = []
    idle = O.idle["new"]
    for j, m in enumerate(O.ml_new):
        rows = []
        for k in np.nonzero(O.T_new[:, j] > 0)[0]:
            k = int(k)
            rows.append([K.ym_str(m) + "-01", O.driver_id[k], int(O.T_new[k, j]), int(S.C_new[k, j]),
                         int(K.round_half_up(float(O.H_new[k, j]) * 60))])
        for (k, jj), mins in idle.items():
            if jj != j:
                continue
            rows.append([K.ym_str(m) + "-01", O.driver_id[k], 0, int(K.rng("idlec", "new", k, j).random() < 0.2),
                         int(mins)])
        rows.sort(key=lambda x: x[1])
        out.extend(rows)
    return out


CROSSWALK_COLS = ["legacy_driver_no", "driver_id", "migrated_on", "migration_note"]


def crosswalk_rows(W, O, S):
    out = []
    for k, no in O.legacy_no.items():
        out.append([no, O.driver_id[k], K.MIGRATION.isoformat(), ""])
    for k, (w2, n2) in O.legacy_second.items():
        out.append([n2, O.driver_id[k], K.MIGRATION.isoformat(), "second registration, merged at migration"])
    out.sort(key=lambda x: x[0])
    return out


ACCOUNT_COLS = ["driver_id", "account_opened", "signup_channel", "home_city", "vehicle", "account_status",
                "last_trip_on", "closed_on", "merged_into"]


def account_rows(W, O, S):
    out = []
    for k in range(O.n_acc):
        if not S.exists[k]:
            continue
        lt = S.last_trip.get(k)
        cl = S.closed.get(k)
        mi = O.driver_id[O.merged_into[k][0]] if k in O.merged_into else ""
        out.append([O.driver_id[k], O.created[k].date().isoformat(), O.channel[k], O.home[k], O.vehicle[k],
                    S.status[k], lt.isoformat() if lt else "", cl.isoformat() if cl else "", mi])
    out.sort(key=lambda x: (x[1], x[0]))
    return out


# ------------------------------------------------------------------------------------------------- payments
RUN26_COLS = ["payout_id", "driver_id", "program_code", "amount_usd", "currency", "created_at_utc", "batch_id"]
ADJ_COLS = ["batch_id", "run_date", "line_id", "driver_id", "program_code", "adjustment_type", "amount_usd",
            "payout_id", "reverses_payout_id"]
RETURN_COLS = ["return_date", "settlement_date", "return_ref", "individual_id", "company_entry_description", "amount",
               "return_reason_code", "return_reason"]
EVENT_COLS = ["payout_id", "event_at_utc", "event", "detail"]


def _created(P, pid):
    return next(e[1] for e in P.payouts[pid]["events"] if e[0] == "created")


def write_run25(path, W, O):
    P = O.pay[2025]
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Payouts"
    head = ["Payout ID", "Driver ID", "Program", "Amount (cents)", "Currency", "Created (UTC)", "Batch"]
    for c, h in enumerate(head, start=1):
        cell = ws.cell(row=1, column=c, value=h)
        cell.font = Font(name="Calibri", size=11, bold=True)
    rows = sorted(P.main_ids.items(), key=lambda kv: kv[1])
    for i, (k, pid) in enumerate(rows, start=2):
        vals = [pid, O.driver_id[k], PROGRAM[2025], K.AMOUNT * 100, "USD", utc(_created(P, pid)), BATCH_MAIN[2025]]
        for c, v in enumerate(vals, start=1):
            ws.cell(row=i, column=c, value=v)
    widths = [22, 12, 10, 15, 10, 21, 17]
    for c, w in enumerate(widths, start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(c)].width = w
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:G%d" % (len(rows) + 1)
    wb.save(path)


def run26_rows(W, O):
    P = O.pay[2026]
    out = []
    for k, pid in sorted(P.main_ids.items(), key=lambda kv: kv[1]):
        out.append([pid, O.driver_id[k], PROGRAM[2026], "%.2f" % K.AMOUNT, "USD", utc(_created(P, pid)),
                    BATCH_MAIN[2026]])
    return out


def adj_rows(W, O):
    lines = []
    for y in (2025, 2026):
        P = O.pay[y]
        for k, pid in P.late_ids.items():
            lines.append(dict(date=P.payouts[pid]["date"], k=k, type="late_credit", amount=K.AMOUNT, pid=pid, rev=""))
        for rc in P.recoveries:
            lines.append(dict(date=rc["date"], k=rc["k"], type=rc["reason"], amount=-K.AMOUNT, pid="",
                              rev=rc["reverses"]))
    out = []
    for i, ln in enumerate(sorted(lines, key=lambda x: (x["date"], x["type"] != "late_credit", x["k"]))):
        prog = PROGRAM[2025] if ln["date"] < dt.date(2025, 12, 1) else PROGRAM[2026]
        batch = "%s-ADJ-%02d%02d" % (prog.replace("WG20", "WG"), ln["date"].month, ln["date"].day)
        lid = "adj_" + K.token("adjline", ln["date"].isoformat(), ln["k"], ln["type"], n=12,
                               alphabet="0123456789abcdefghjkmnpqrstvwxyz")
        out.append([batch, ln["date"].isoformat(), lid, O.driver_id[ln["k"]], prog, ln["type"],
                    "%.2f" % ln["amount"], ln["pid"], ln["rev"]])
    return out


def return_rows(W, O):
    """The bank's returns report for the payout account: the guarantee's returns among the weekly earnings payouts'."""
    out = []
    for y in (2025, 2026):
        P = O.pay[y]
        for rt in P.returns:
            out.append(dict(date=rt["date"], settle=rt["settle"], pid=rt["pid"], desc="GUARANTEE",
                            amount=float(K.AMOUNT), code=rt["code"]))
    r = K.rng("returns", "earnings")
    d = dt.date(2025, 1, 2)
    while d <= dt.date(2026, 12, 31):
        if d.weekday() < 5 and d not in OP.FED_HOLIDAYS:
            n = int(r.poisson(2.4 if d.weekday() in (1, 2) else 0.9))
            for _ in range(n):
                amt = float(np.round(np.clip(r.lognormal(5.9, 0.62), 18, 2400), 2))
                pid = "po_" + K.token("earnret", d.isoformat(), _, r.integers(1 << 30), n=14,
                                      alphabet="0123456789abcdefghjkmnpqrstvwxyz")
                settle = d
                for _k in range(int(r.integers(1, 3))):
                    settle -= dt.timedelta(days=1)
                    while settle.weekday() >= 5 or settle in OP.FED_HOLIDAYS:
                        settle -= dt.timedelta(days=1)
                out.append(dict(date=d, settle=settle, pid=pid, desc="DRIVER PAY", amount=amt,
                                code=OP._pick(r, OP.RETURN_CODES)))
        d += dt.timedelta(days=1)
    out.sort(key=lambda x: (x["date"], x["pid"]))
    rows = []
    for i, x in enumerate(out):
        ref = "RTN%s%05d" % (x["date"].strftime("%y%m"), 1 + i % 99991)
        rows.append([x["date"].isoformat(), x["settle"].isoformat(), ref, x["pid"], x["desc"], "%.2f" % x["amount"],
                     x["code"][0], x["code"][1]])
    return rows


def event_rows(W, O):
    out = []
    for y in (2025, 2026):
        P = O.pay[y]
        for pid, po in P.payouts.items():
            for ev, t, det in po["events"]:
                out.append([pid, utc(t), ev, det])
    out.sort(key=lambda x: (x[1], x[0]))
    return out


# ------------------------------------------------------------------------------------------------- onboarding
APP_COLS = ["application_id", "submitted_at_utc", "vehicle_source", "status", "decision_at_utc", "driver_id",
            "first_trip_at_utc"]
ORDER_COLS = ["order_id", "candidate_id", "client_reference", "package", "ordered_at", "completed_at", "result"]


def app_rows(S):
    out = []
    for b in S.apps:
        out.append([b["app_id"], utc(b["submitted_shown"]), b["vehicle"], b["status"],
                    utc(b["decision_shown"]) if b["decision_shown"] else "", b["driver"] or "",
                    utc(b["first_trip_shown"]) if b["first_trip_shown"] else ""])
    out.sort(key=lambda x: (x[1], x[0]))
    return out


def order_rows(S):
    asof_end = dt.datetime.combine(K.AS_OF, dt.time(21, 40))
    out = []
    for b in S.orders:
        done = b["check_done"] if (b["check_done"] is not None and b["check_done"] <= asof_end) else None
        res = b["check_result"] if done is not None or b["check_result"] == "canceled" else "pending"
        out.append([b["order_id"], b["candidate"], b["app_id"], "DRV-STD-MVR", utc_z(b["ordered"]),
                    utc_z(done) if done else "", res])
    out.sort(key=lambda x: (x[4], x[0]))
    return out


# ------------------------------------------------------------------------------------------------- distractors
REFERRAL_COLS = ["referral_id", "referrer_driver_id", "referred_driver_id", "referred_first_trip_on", "qualified_on",
                 "bonus_usd", "paid_on"]


def referral_rows(W, O):
    out = []
    for x in sorted(O.referrals, key=lambda x: (x["qualified"], x["referred"])):
        rid = "REF-" + K.token("refid", x["referred"], n=7, alphabet="0123456789")
        out.append([rid, O.driver_id[x["referrer"]], O.driver_id[x["referred"]], x["first_trip"].isoformat(),
                    x["qualified"].isoformat(), "250.00", x["paid"].isoformat()])
    return out


def write_demand(path, W):
    """The marketplace team's weekly rider demand plan for the first quarter of 2027 (issued 4 December 2026): rider
    requests from the same weeks of 2026 grown at the plan's assumption, and the driver hours that would serve them."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Q1 2027 weekly"
    ws["A1"] = "Larch Rides: rider demand plan, Q1 2027"
    ws["A1"].font = Font(name="Calibri", size=13, bold=True)
    ws["A2"] = ("Marketplace planning, issued 4 December 2026. Weeks Monday to Sunday, Central time. Requests are rider "
                "trip requests; hours are the driver online hours that serve the requests at the plan's 1.85 completed "
                "trips per online hour and 91.5% fill.")
    ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="5F6670")
    head = ["Week starting", "Requests, 2026 same week", "Growth assumption", "Requests, plan", "Completed trips, plan",
            "Driver online hours, plan"]
    fill = PatternFill("solid", fgColor="DDE7DA")
    thin = Side(style="thin", color="AEB8AB")
    for c, h in enumerate(head, start=1):
        cell = ws.cell(row=4, column=c, value=h)
        cell.font = Font(name="Calibri", size=10, bold=True)
        cell.fill = fill
        cell.alignment = Alignment(wrap_text=True, vertical="top")
        cell.border = Border(bottom=thin)
    ws.row_dimensions[4].height = 30
    r = K.rng("demand")
    w0 = K.widx(dt.date(2027, 1, 4))
    # The plan's growth assumption, one figure a month as marketplace planning states it. The autumn ran
    # about a fifth ahead of the year before and December nearly two fifths ahead, and the plan carries that
    # through the new year before lapping itself by March. It is set so the hours the plan asks of supply
    # cover the requests the quarter turns out to bring; the headroom is asserted in checks.py.
    growth = [0.58, 0.58, 0.58, 0.58, 0.42, 0.42, 0.42, 0.42, 0.10, 0.10, 0.10, 0.10, 0.10]
    tot = [0, 0, 0]
    for i in range(13):
        wk = K.wdate(w0 + i)
        last = int(W.trips[:, w0 + i - 52].sum())
        req = int(round(last / 0.917 * float(r.normal(1.0, 0.012))))
        plan = int(round(req * (1 + growth[i]), -1))
        comp = int(round(plan * 0.915, -1))
        hrs = int(round(comp / 1.85, -1))
        vals = [wk, req, growth[i], plan, comp, hrs]
        for c, v in enumerate(vals, start=1):
            cell = ws.cell(row=5 + i, column=c, value=v)
            cell.font = Font(name="Calibri", size=10)
            if c == 1:
                cell.number_format = "d mmm yyyy"
            elif c == 3:
                cell.number_format = "0.0%"
            else:
                cell.number_format = "#,##0"
        tot[0] += plan
        tot[1] += comp
        tot[2] += hrs
    ws.cell(row=18, column=1, value="Quarter").font = Font(name="Calibri", size=10, bold=True)
    for c, v in zip((4, 5, 6), tot):
        cell = ws.cell(row=18, column=c, value=v)
        cell.font = Font(name="Calibri", size=10, bold=True)
        cell.number_format = "#,##0"
    for c, w in enumerate([14, 16, 12, 14, 14, 16], start=1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(c)].width = w
    wb.save(path)
