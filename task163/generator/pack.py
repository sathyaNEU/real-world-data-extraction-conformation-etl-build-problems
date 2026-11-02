"""task163 pack: the files Lathmor's and Aubrine's systems hold on 30 October 2026, written from the world's truth.
No file describes the data; each carries its own conventions in its own labels, and provenance sits in metadata.json."""
from __future__ import annotations

import datetime as dt
import os
from collections import defaultdict

import numpy as np

import common as K
import world as W

F_VEL = "pick_velocity_by_week.csv"
F_LOC = "location_master.csv"
F_ITEM = "item_master.csv"
F_PLAN = "slotting_plan_2027.xlsx"
F_CLAIMS = "aubrine_claims_register.xlsx"
F_HOLDS = "checkweigh_holds.csv"
F_SCHED = "schedule3_service_levels.pdf"
F_PBSOP = "pack_bench_procedure.pdf"
F_RBSOP = "returns_grading_procedure.pdf"
F_AGENCY = "corsley_invoice_lines.csv"
F_RET = "returns_grading_log.csv"
F_RAV = "ravelrig_invoices_2025-26.pdf"
F_TRAIN = "picker_training_log.xlsx"
F_PROMO = "aubrine_promotions_2027.csv"
DISTRACTORS = [F_TRAIN, F_PROMO]


def wms_loc(run, p):
    zone, aisle, level = run
    return "%s%02d-%02d-%d-%d" % (zone, aisle, p // 3 + 1, level, p % 3 + 1)


def plan_loc(run, p):
    zone, aisle, level = run
    return "%s.%02d.%02d.%d.%02d" % (zone, aisle, p // 3 + 1, level, p % 3 + 1)


def order_ref(*keys):
    return "AU%s" % K.token("order", *keys, n=9, alphabet="0123456789")


# ------------------------------------------------------------------------------------------------- picking files
def write_velocity(out, w):
    skus, dd, lines, units, cur = w["skus"], w["dd"], w["lines"], w["units"], w["cur"]
    weeks = defaultdict(list)
    for j, d in enumerate(dd):
        weeks[K.monday(d)].append(j)
    rows = []
    for mon in sorted(weeks):
        idx = weeks[mon]
        for s in sorted(skus, key=lambda s: s["item"]):
            ln = int(lines[s["sku"], idx].sum())
            if ln == 0:
                continue
            rows.append([K.iso_week(mon), mon.isoformat(), s["item"], wms_loc(*cur[s["sku"]]), ln,
                         int(units[s["sku"], idx].sum())])
    return K.write_csv(os.path.join(out, F_VEL), ["iso_week", "week_commencing", "item_code", "location",
                                                  "lines_picked", "units_picked"], rows)


def write_locations(out, w):
    rows = []
    at = {v: k for k, v in w["cur"].items()}
    by = {s["sku"]: s for s in w["skus"]}
    for zone in "ABCD":
        for run in W.runs_of(zone):
            for p in range(W.RUN_LEN):
                sku = at.get((run, p))
                rows.append([wms_loc(run, p), zone, "%s%02d" % (zone, run[1]), p // 3 + 1, run[2], p % 3 + 1,
                             "Carton flow" if zone == "A" else "Shelf",
                             by[sku]["item"] if sku is not None else "", "Active" if sku is not None else "Spare"])
    return K.write_csv(os.path.join(out, F_LOC), ["location", "zone", "aisle", "bay", "level", "position",
                                                  "face_type", "item_code", "status"], rows)


def write_items(out, w):
    rows = []
    for s in sorted(w["skus"], key=lambda s: s["item"]):
        wt, uom = "%d" % s["w"], "g"
        rows.append([s["item"], s["aub"], s["desc"], s["family"], wt, uom, s["size_class"], "%.2f" % s["cost"],
                     "Active"])
    return K.write_csv(os.path.join(out, F_ITEM), ["item_code", "aubrine_code", "description", "family",
                                                   "unit_weight", "weight_uom", "size_class", "std_cost_gbp",
                                                   "status"], rows)


# ------------------------------------------------------------------------------------------------- claims and holds
def claims_rows(w):
    """Aubrine's claims export: every claim lodged from 1 September 2025 to the extract."""
    g = K.rng("claims")
    by = {s["sku"]: s for s in w["skus"]}
    rows = []
    extract = dt.datetime(2026, 10, 30, 17, 0)

    def stamp(d, k):
        return dt.datetime.combine(d, dt.time(0, 0)) + dt.timedelta(minutes=int(g.integers(7 * 60, 23 * 60)) + 1440 * k)

    def add(desp, reason, ordered, received, status, resolution, ln=1):
        lodged = stamp(desp, 2 + int(g.integers(0, 24)))
        if lodged > extract:
            return
        if lodged < dt.datetime(2025, 9, 1):
            return
        if status == "Validated" and (extract - lodged).days < 4:
            status, resolution = "Open", ""
        rows.append(dict(lodged=lodged, despatched=desp, reason=reason, ordered=ordered, received=received,
                         status=status, resolution=resolution, line=ln))

    for e in w["events"]:
        if e["reported"]:
            add(e["day"], "Wrong item received", by[e["sku"]]["aub"], by[e["wrong"]]["aub"], "Validated",
                "Replacement sent" if g.random() < 0.83 else "Refund")
    for e in w["others"]:
        if e["reported"]:
            add(e["day"], "Item missing", by[e["sku"]]["aub"], "", "Validated",
                "Replacement sent" if g.random() < 0.8 else "Refund")
    # claims that are not Lathmor's picking: damage, loss, lateness, and customer error; duplicates and withdrawals
    dd = w["dd"]
    vol = w["lines"].sum(axis=0)
    p = np.array([s["vel"] for s in w["skus"]])
    p = p / p.sum()
    for j, d in enumerate(dd):
        orders = vol[j] / 1.6
        for reason, rate, status in (("Damaged in transit", 1 / 5200.0, "Validated"),
                                     ("Not received", 1 / 7800.0, "Validated"),
                                     ("Late delivery", 1 / 9400.0, "Validated"),
                                     ("Wrong item received", 1 / 1500000.0, "Rejected"),
                                     ("Item missing", 1 / 90000.0, "Rejected")):
            for _ in range(int(g.poisson(orders * rate))):
                sku = w["skus"][int(g.choice(len(p), p=p))]
                rec = sku["aub"] if reason == "Wrong item received" else ""
                add(d, reason, sku["aub"], rec, status,
                    "" if status == "Rejected" else ("Refund" if reason != "Damaged in transit" else "Replacement sent"))
    # duplicates (a second contact logged as its own claim) and withdrawals
    base = list(rows)
    for r in base:
        u = g.random()
        if u < 0.0025:
            d2 = dict(r)
            d2["lodged"] = r["lodged"] + dt.timedelta(hours=int(g.integers(2, 60)))
            if d2["lodged"] <= extract:
                d2["status"], d2["resolution"] = "Duplicate", ""
                rows.append(d2)
        elif u < 0.014 and r["status"] == "Validated" and r["reason"] != "Wrong item received":
            r["status"], r["resolution"] = "Withdrawn", ""
    rows.sort(key=lambda r: (r["lodged"], r["ordered"]))
    out = []
    for k, r in enumerate(rows):
        ln = int(g.choice([1, 2, 3, 4, 5], p=[0.62, 0.22, 0.09, 0.05, 0.02]))
        out.append(dict(r, line=ln, ref="CLM-%06d" % (184000 + k * 3 + int(g.integers(0, 3))),
                        order=order_ref("c", k, r["despatched"].isoformat()),
                        channel=["Email", "Chat", "Phone", "Web form"][int(g.choice(4, p=[0.31, 0.38, 0.11, 0.20]))]))
    return out


def write_claims(out, w):
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment
    rows = claims_rows(w)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Claims"
    head = ["Claim ref", "Lodged", "Channel", "Order ref", "Order line", "Despatched", "Reason", "Product ordered",
            "Product received", "Status", "Resolution"]
    ws.append(head)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="5B2C6F")
        c.alignment = Alignment(vertical="center")
    for r in rows:
        ws.append([r["ref"], r["lodged"], r["channel"], r["order"], r["line"], r["despatched"], r["reason"],
                   r["ordered"], r["received"] or None, r["status"], r["resolution"] or None])
    for row in ws.iter_rows(min_row=2):
        row[1].number_format = "dd/mm/yyyy hh:mm"
        row[5].number_format = "dd/mm/yyyy"
    for col, wd in zip("ABCDEFGHIJK", (12, 17, 10, 13, 10, 12, 22, 16, 16, 11, 17)):
        ws.column_dimensions[col].width = wd
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = "A1:K%d" % (len(rows) + 1)
    path = os.path.join(out, F_CLAIMS)
    wb.save(path)
    return len(rows)


def holds_rows(w):
    g = K.rng("holds")
    by = {s["sku"]: s for s in w["skus"]}
    rows = []
    tare = {"S": 38, "L": 96}
    for e in w["events"]:
        if not e["caught"]:
            continue
        s, x = by[e["sku"]], by[e["wrong"]]
        extra = int(g.integers(0, 3)) * by[e["sku"]]["w"] if g.random() < 0.3 else 0
        exp_g = int(round(s["w"] + extra + tare[s["size_class"]]))
        meas = int(round(exp_g - s["w"] + x["w"] + float(g.integers(-2, 3))))
        rows.append(dict(day=e["day"], minute=e["minute"], cause="MISPICK", exp=exp_g, meas=meas,
                         item_exp=s["item"], item_found=x["item"], outcome="Corrected and re-weighed"))
    for e in w["others"]:
        if not e["caught"]:
            continue
        s = by[e["sku"]]
        exp_g = int(round(s["w"] + tare[s["size_class"]] + (int(g.integers(0, 3)) * 40)))
        meas = exp_g - int(s["w"]) if e["kind"] == "SHORT" else exp_g + int(s["w"])
        meas += int(g.integers(-2, 3))
        rows.append(dict(day=e["day"], minute=e["minute"], cause=e["kind"], exp=exp_g, meas=meas,
                         item_exp=s["item"], item_found="" if e["kind"] == "SHORT" else s["item"],
                         outcome="Corrected and re-weighed"))
    dd = w["dd"]
    vol = w["lines"].sum(axis=0)
    for j, d in enumerate(dd):
        parcels = vol[j] / 1.6
        for cause, rate in (("PACKAGING", 1 / 3100.0), ("NO FAULT FOUND", 1 / 5600.0)):
            for _ in range(int(g.poisson(parcels * rate))):
                exp_g = int(g.integers(60, 900))
                off = int(g.choice([-1, 1])) * int(g.integers(16, 40))
                rows.append(dict(day=d, minute=int(g.integers(6 * 60, 22 * 60)), cause=cause, exp=exp_g,
                                 meas=exp_g + off, item_exp="", item_found="",
                                 outcome="Re-packed and re-weighed" if cause == "PACKAGING" else "Re-weighed, released"))
    rows = [r for r in rows if K.EXPORT_FROM <= r["day"] <= K.EXPORT_TO]
    rows.sort(key=lambda r: (r["day"], r["minute"], str(r["item_exp"])))
    out = []
    seq = 3018400
    for k, r in enumerate(rows):
        t = dt.datetime.combine(r["day"], dt.time(0, 0)) + dt.timedelta(minutes=r["minute"])
        seq += 1 + int(g.geometric(0.55)) - 1 + (int(g.integers(0, 4)) if g.random() < 0.2 else 0)
        out.append([("H%07d" % seq), "PB%02d" % int(g.integers(1, 15)), t.strftime("%Y-%m-%d %H:%M"),
                    order_ref("h", k), r["exp"], r["meas"], r["cause"], r["item_exp"], r["item_found"], r["outcome"]])
    return out


def write_holds(out, w):
    rows = holds_rows(w)
    return K.write_csv(os.path.join(out, F_HOLDS), ["hold_id", "bench", "held_at", "order_ref", "expected_g",
                                                    "measured_g", "cause", "item_expected", "item_found", "outcome"],
                       rows)


# ------------------------------------------------------------------------------------------------- the agency
def agency_rows(w):
    lines = sorted(w["agency"], key=lambda l: (l["date"], l["shift"], l["worker"]))
    by_week = defaultdict(list)
    for l in lines:
        by_week[K.monday(l["date"])].append(l)
    prem = {}
    for a, b in w["periods"]:
        amt = sum(l["night"] * W.U_NIGHT + l["sunday"] * W.U_SUNDAY for l in lines if a <= l["date"] <= b)
        prem[b + dt.timedelta(days=9)] = round(amt, 2)       # the Tuesday invoice of the week after the period
    rows = []
    g = K.rng("invoice_numbers")
    n = 48210
    for mon in sorted(by_week):
        inv_date = mon + dt.timedelta(days=8)
        n += int(g.integers(19, 61))
        inv = "CSI-%06d" % n
        for l in by_week[mon]:
            rows.append([inv, inv_date.isoformat(), mon.isoformat(), "Hours", l["worker"], l["grade"],
                         l["date"].isoformat(), l["shift"], "%.2f" % l["hours"], "%.2f" % l["night"],
                         "%.2f" % l["rate"], "%.2f" % round(l["hours"] * l["rate"], 2)])
        if inv_date in prem:
            rows.append([inv, inv_date.isoformat(), mon.isoformat(), "Premium reconciliation", "", "", "", "", "",
                         "", "", "%.2f" % prem[inv_date]])
    return rows, prem


def write_agency(out, w):
    rows, _ = agency_rows(w)
    return K.write_csv(os.path.join(out, F_AGENCY), ["invoice_no", "invoice_date", "week_commencing", "line_type",
                                                     "worker_no", "grade", "shift_start_date", "shift", "hours",
                                                     "night_hours", "rate_gbp", "amount_gbp"], rows)


# ------------------------------------------------------------------------------------------------- returns
def returns_rows(w):
    g = K.rng("returns_rows")
    by = {s["sku"]: s for s in w["skus"]}
    rows = []
    for k, r in enumerate(w["returns"]):
        t = dt.datetime.combine(r["day"], dt.time(0, 0)) + dt.timedelta(minutes=r["minute"])
        ref = "RTN-%07d" % (5100000 + 3 * k + int(g.integers(0, 3)))
        cap = "Bench sheet" if r["day"] < K.APP_LIVE else "Handheld"
        op = "OP%03d" % int(g.integers(11, 29))
        if g.random() < 0.011:
            # a unit graded, then corrected minutes later at the same station: the later grade stands
            first = int(g.choice([c for c in (1, 2, 3) if c != r["code"]]))
            rows.append([ref, t.strftime("%Y-%m-%d %H:%M"), by[r["sku"]]["item"], first, r["station"], cap, op])
            t = t + dt.timedelta(minutes=int(g.integers(2, 25)))
        rows.append([ref, t.strftime("%Y-%m-%d %H:%M"), by[r["sku"]]["item"], r["code"], r["station"], cap, op])
    rows.sort(key=lambda x: (x[1], x[0]))
    return rows


def write_returns(out, w):
    return K.write_csv(os.path.join(out, F_RET), ["return_ref", "graded_at", "item_code", "grade", "station",
                                                  "captured_by", "operator"], returns_rows(w))


def ravelrig_bills(w):
    by = {s["sku"]: s for s in w["skus"]}
    m = defaultdict(float)
    for r in w["returns"]:
        if r["fate"] == "repack":
            m[(r["day"].year, r["day"].month)] += W.REPACK_PRICE[by[r["sku"]]["size_class"]]
    return {k: round(v, 2) for k, v in sorted(m.items()) if k <= (2026, 9)}


# ------------------------------------------------------------------------------------------------- distractors
def write_promotions(out):
    g = K.rng("promos")
    rows = []
    mech = ["3 for 2", "20% off", "Gift with purchase", "Free delivery over GBP 25", "Bundle price"]
    start = dt.date(2027, 1, 8)
    k = 0
    while start < dt.date(2027, 12, 20):
        fam = W.FAMILIES[int(g.integers(0, len(W.FAMILIES)))]
        length = int(g.integers(5, 15))
        rows.append(["P27-%03d" % (k + 1), start.isoformat(), (start + dt.timedelta(length - 1)).isoformat(), fam,
                     mech[int(g.integers(0, len(mech)))], "%d" % int(g.integers(8, 45))])
        start += dt.timedelta(int(g.integers(9, 24)))
        k += 1
    return K.write_csv(os.path.join(out, F_PROMO), ["promo_id", "start", "end", "family", "mechanic",
                                                    "planned_uplift_pct"], rows)


def write_training(out, w):
    """Lathmor's training record for pickers on the account: Corsley's workers are inducted before their first shift
    and assessed while on assignment; Lathmor's own pickers over their years on site. No date passes the log's own."""
    import openpyxl
    from openpyxl.styles import Font
    g = K.rng("training")
    log_date = dt.date(2026, 10, 22)
    span = {}
    for l in w["agency"]:
        a, b = span.get(l["worker"], (l["date"], l["date"]))
        span[l["worker"]] = (min(a, l["date"]), max(b, l["date"]))
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Training record"
    ws.append(["Person", "Employer", "Role", "Induction", "Pick accuracy refresher", "Manual handling", "Last assessed"])
    for c in ws[1]:
        c.font = Font(bold=True)
    rows = []
    for p_ in sorted(span):
        first, last = span[p_]
        ind = first - dt.timedelta(int(g.integers(1, 12)) if first > K.AGENCY_FROM + dt.timedelta(13)
                                    else int(g.integers(20, 420)))
        rows.append((p_, "Corsley Staffing", ind, min(last, log_date)))
    for k in range(64):
        ind = dt.date(2019, 3, 4) + dt.timedelta(int(g.integers(0, 2700)))
        rows.append(("U%04d" % (2100 + 7 * k + int(g.integers(0, 5))), "Lathmor", ind, dt.date(2026, 10, 16)))
    for person, emp, ind, end_ in rows:
        mh = ind + dt.timedelta(int(g.integers(0, 4)))
        ref = ind + dt.timedelta(int(g.integers(180, 420)))
        ref = ref if ref <= end_ else None
        lo = ref or mh
        last = lo + dt.timedelta(int(g.uniform(0, max(1, (end_ - lo).days)))) if end_ > lo else lo
        ws.append([person, emp, "Picker", ind, ref, mh, last])
    for row in ws.iter_rows(min_row=2):
        for c in row[3:]:
            c.number_format = "dd/mm/yyyy"
    for col, wd in zip("ABCDEFG", (10, 18, 10, 12, 22, 16, 14)):
        ws.column_dimensions[col].width = wd
    wb.save(os.path.join(out, F_TRAIN))
    return len(rows)


def write_all(out, w):
    os.makedirs(out, exist_ok=True)
    n = {}
    n[F_VEL] = write_velocity(out, w)
    n[F_LOC] = write_locations(out, w)
    n[F_ITEM] = write_items(out, w)
    n[F_CLAIMS] = write_claims(out, w)
    n[F_HOLDS] = write_holds(out, w)
    n[F_AGENCY] = write_agency(out, w)
    n[F_RET] = write_returns(out, w)
    n[F_PROMO] = write_promotions(out)
    n[F_TRAIN] = write_training(out, w)
    import docs
    n.update(docs.write_all(out, w))
    return n
