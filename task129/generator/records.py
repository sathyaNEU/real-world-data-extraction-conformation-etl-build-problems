"""the cooperative's records as its systems export them: the outage system at restoration-step grain (storm-mode
tickets included), the trim-unit register, the trimming completions, the forester's survey, the stations' daily
summaries, the member counts and accounts payable's trimming invoices"""
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd

import params as P

FT_PER_MI = 5280


def _fmt(t):
    return t.strftime("%Y-%m-%d %H:%M")


def device_id(o, rng):
    c = o["circuit"]
    pole = int(rng.integers(100, 9000))
    return {"FUSE": "FU-%s-%04d" % (c, pole), "RECLOSER": "RC-%s-%d" % (c, 1 + pole % 4),
            "BREAKER": "CB-%s" % c, "SWITCH": "SW-%s-%04d" % (c, pole),
            "TRANSFORMER": "TX-%s-%04d" % (c, pole), "SERVICE": "SV-%s-%05d" % (c, pole * 7 % 99991)}[o["device"]]


def free_devices(recs):
    """a device that has opened stays open until it is restored, so two outages never hold one device at once: an outage
    whose drawn device is already out takes another recloser on the circuit, or a fuse (its own stream, so nothing
    else in the export moves)"""
    rng = np.random.default_rng(P.SEED + 79)
    order = sorted(range(len(recs)), key=lambda i: (recs[i]["start"], i))
    held = {}

    def free(dev, s):
        return held.get(dev) is None or held[dev] < s

    for i in order:
        o = recs[i]
        s = o["start"]
        e = s + timedelta(minutes=int(o["steps_min"][-1]))
        dev = o["device_id"]
        if not free(dev, s):
            c = o["circuit"]
            options = ["RC-%s-%d" % (c, k) for k in range(1, 5)] if o["device"] in ("RECLOSER", "BREAKER") else []
            options = [x for x in options if free(x, s)]
            if options:
                dev, o["device"] = options[0], "RECLOSER"
            else:
                while True:
                    pole = int(rng.integers(100, 9000))
                    cand = {"TRANSFORMER": "TX-%s-%04d" % (c, pole), "SERVICE": "SV-%s-%05d" % (c, pole * 7 % 99991),
                            "SWITCH": "SW-%s-%04d" % (c, pole)}.get(o["device"], "FU-%s-%04d" % (c, pole))
                    if free(cand, s):
                        break
                if cand.startswith("FU-"):
                    o["device"] = "FUSE"
                dev = cand
            o["device_id"] = dev
        held[dev] = max(held.get(dev, e), e) if held.get(dev) is not None and held[dev] >= s else e
    return recs


def outage_export(O, rng):
    """one row per restoration step; storm-mode tickets: on a storm day the system opens a ticket for each cluster
    of member calls, and some device outages carry a second ticket with its own number and the same restoration;
    on any day a device can trip again after it is restored (a second outage of its own)"""
    O = O.copy()
    O["device_id"] = [device_id(o, rng) for o in O.to_dict("records")]
    recs = free_devices(O.to_dict("records"))
    busy = {}
    for o in recs:
        busy.setdefault(o["device_id"], []).append((o["start"], o["start"] + timedelta(minutes=int(o["steps_min"][-1]))))
    extra = []
    for o in recs:
        sustained = sum(o["steps_min"]) > 5 if o["steps_min"] else False
        if o["storm"] and o["level"] == "PRIMARY" and o["cause"] != "PLANNED" and rng.random() < 0.16:
            d = dict(o)
            shift = int(rng.integers(-22, 23))
            if (o["start"] + timedelta(minutes=shift)).date() != o["start"].date():
                shift = -shift                          # the second ticket is opened the same day
            d["start"] = o["start"] + timedelta(minutes=shift)
            d["steps_min"] = [m - shift for m in o["steps_min"]]
            d["kind"] = "duplicate"
            extra.append(d)
        if o["level"] == "PRIMARY" and o["cause"] not in ("PLANNED",) and rng.random() < 0.018 and sustained:
            d = dict(o)
            gap = o["steps_min"][-1] + int(rng.integers(20, 300))
            d["start"] = o["start"] + timedelta(minutes=gap)
            d["steps_min"] = [int(rng.integers(40, 160))]
            d["steps_members"] = [o["members"]]
            d["kind"] = "retrip_" + o["kind"]
            end = d["start"] + timedelta(minutes=d["steps_min"][-1])
            if not any(a <= end and d["start"] <= b for a, b in busy[o["device_id"]] if (a, b) != (o["start"], o["start"] + timedelta(minutes=int(o["steps_min"][-1])))):
                extra.append(d)                                 # a device already out on another outage cannot re-trip
    allr = recs + extra
    allr.sort(key=lambda r: (r["start"], r["device_id"], r["kind"]))
    rows = []
    seq = {}
    truth = []
    for o in allr:
        y = o["start"].year
        seq[y] = seq.get(y, 0) + 1
        oid = "OUT%d%06d" % (y, seq[y])
        for k, (m, mem) in enumerate(zip(o["steps_min"], o["steps_members"])):
            rows.append((oid, _fmt(o["start"]), o["level"], o["district"], o["circuit"], o["unit_id"], o["device"],
                         o["device_id"], o["cause"], o["members"], k + 1, _fmt(o["start"] + timedelta(minutes=int(m))),
                         int(mem)))
        truth.append((oid, o["kind"], o["storm"], o["start"], o["level"], o["cause"], o["unit_id"], o["district"]))
    cols = ["outage_id", "start_local", "level", "service_area", "circuit", "unit_id", "device_type", "device_id",
            "cause_code", "members_out", "step", "step_restored_local", "members_restored"]
    X = pd.DataFrame(rows, columns=cols)
    K = pd.DataFrame(truth, columns=["outage_id", "kind", "storm", "start", "level", "cause", "unit_id", "district"])
    return X, K


def unit_register(U):
    R = U[["unit_id", "district", "substation", "circuit", "miles", "in_service", "retired", "retire_reason",
           "replaced_by"]].copy()
    R["miles"] = R.miles.round(3)
    R["in_service"] = R.in_service.map(lambda d: d.isoformat())
    R["retired"] = R.retired.map(lambda d: d.isoformat() if d is not None else "")
    R = R.rename(columns={"in_service": "in_service_date", "retired": "retired_date"})
    return R.sort_values(["district", "circuit", "unit_id"]).reset_index(drop=True)


def completions(T, rng):
    T = T.copy().sort_values(["completed", "work_order", "unit_id", "status"]).reset_index(drop=True)
    T["record_id"] = ["TC%07d" % (1000231 + 3 * i + i % 3) for i in range(len(T))]
    T["completed_date"] = T.completed.map(lambda d: d.isoformat())
    late = T.accepted.map(lambda d: d is not None and d > P.EXPORT)       # not yet audited when the extract was taken
    T["accepted_date"] = [("" if lt or d is None else d.isoformat()) for lt, d in zip(late, T.accepted)]
    T["audit_status"] = np.where(late, "PENDING", T.status)
    return T[["record_id", "work_order", "unit_id", "contractor", "crew", "completed_date", "audit_status",
              "accepted_date"]]


def survey_rows(S):
    S = S.copy()
    S["survey_date"] = S.survey_date.map(lambda d: d.isoformat())
    return S.sort_values(["unit_id", "span_id", "species_code"]).reset_index(drop=True)


def weather_rows(Wx):
    names = {"North": ("VSY01", "Alder Flats airfield"), "East": ("VSY02", "Holloway Mill"),
             "South": ("VSY03", "Lyle Junction")}
    rows = []
    for d in P.DISTRICTS:
        sid, nm = names[d]
        for r in Wx[d].itertuples():
            rows.append((sid, nm, r.date.date().isoformat(), int(r.gust), "%.2f" % r.rain))
    return pd.DataFrame(rows, columns=["station_id", "station_name", "date_utc", "peak_gust_mph", "precipitation_in"])


def invoices(T, U, rng):
    """accounts payable's trimming invoices for service in December 2024 to December 2025: the outgoing firm bills
    each work order monthly in miles, the new firm twice a month in linear feet; some long work orders run two
    progress invoices in a month; a disputed invoice is voided by a credit memo that names the invoice it reverses,
    and re-issued under a new number"""
    T = T[(T.measured > 0)].copy()
    T["svc"] = T.completed.map(lambda d: "%d-%02d" % (d.year, d.month))
    T = T[(T.svc >= "2024-12") & (T.svc <= "2025-12")]
    T["half"] = T.completed.map(lambda d: 1 if d.day <= 15 else 2)
    vendors = {P.OUTGOING: ("HLC", "MI", 1.0, 2740.0), P.INCOMING: ("GVS", "LF", FT_PER_MI, 0.59)}
    rows = []
    num = {P.OUTGOING: 40211, P.INCOMING: 7105}
    lines = []
    sizes = T[T.contractor == P.OUTGOING].groupby(["work_order", "svc"]).size()
    force = set()
    for q in (1, 2, 3, 4):
        cand = sizes[[k[1].startswith("2025") and (int(k[1][5:]) - 1) // 3 + 1 == q for k in sizes.index]]
        cand = cand[cand >= 2]
        if len(cand):
            force.add(cand.idxmax())
    for (con, wo, svc), g in T.groupby(["contractor", "work_order", "svc"], sort=True):
        code, uom, mult, price = vendors[con]
        y, m = int(svc[:4]), int(svc[5:])
        if con == P.INCOMING:
            parts = [g[g.half == 1], g[g.half == 2]]
        elif (wo, svc) in force or (len(g) > 12 and rng.random() < 0.6):
            cut = len(g) // 2
            parts = [g.iloc[:cut], g.iloc[cut:]]
        else:
            parts = [g]
        for pi, part in enumerate(parts):
            if part.empty:
                continue
            miles = float(part.measured.sum())
            qty = round(miles * mult, 2) if uom == "MI" else float(int(round(miles * mult)))
            inv_date = (date(y, m, 15) if (pi == 0 and len(parts) > 1) else
                        (date(y + (m == 12), m % 12 + 1, 1) + timedelta(days=int(rng.integers(2, 12)))))
            num[con] += 1
            inv = "%s-%06d" % (code, num[con])
            body = [("TRIM-" + uom, "Right-of-way trimming, overhead primary", qty, uom, price)]
            if rng.random() < 0.35:
                body.append(("HAZ-EA", "Hazard tree removal", float(int(rng.integers(1, 9))), "EA", 315.0))
            if rng.random() < 0.25:
                body.append(("HERB-AC", "Herbicide, brush regrowth", round(float(rng.uniform(2, 30)), 1), "AC", 96.0))
            if pi == 0 and rng.random() < 0.12:
                body.append(("MOB-LS", "Crew mobilization", 1.0, "LS", 1850.0))
            lines.append(dict(vendor=con, invoice_no=inv, invoice_date=inv_date, doc_type="INVOICE", applies_to="",
                              work_order=wo, service_month=svc, body=body))
    room = lambda l: (P.EXPORT - l["invoice_date"]).days - 2            # days a credit memo has before the extract
    disputed = [i for i, l in enumerate(lines) if rng.random() < 0.13 and room(l) >= 20]
    cells = {}
    for i, l in enumerate(lines):
        if l["service_month"].startswith("2025") and room(l) >= 8:
            q = (int(l["service_month"][5:]) - 1) // 3 + 1
            cells.setdefault((l["vendor"], q), []).append(i)
    for key in sorted(cells):
        if not any(i in disputed for i in cells[key]):
            disputed.append(cells[key][int(rng.integers(0, len(cells[key])))])
    disputed = sorted(set(disputed))
    for i in disputed:
        l = lines[i]
        cd = l["invoice_date"] + timedelta(days=int(rng.integers(15 if room(l) >= 20 else 5, min(41, room(l) + 1))))
        con = l["vendor"]
        code = vendors[con][0]
        num[con] += 1
        cm = "%s-CM%05d" % (code, num[con])
        num[con] += 1
        ri = "%s-%06d" % (code, num[con])
        neg = [(c, d_, -q, u, p) for c, d_, q, u, p in l["body"]]
        lines.append(dict(vendor=con, invoice_no=cm, invoice_date=cd, doc_type="CREDIT MEMO",
                          applies_to=l["invoice_no"], work_order=l["work_order"], service_month="", body=neg))
        fixed = [(c, d_, q, u, round(p * (0.97 if c.startswith("TRIM") else 1.0), 4)) for c, d_, q, u, p in l["body"]]
        lines.append(dict(vendor=con, invoice_no=ri, invoice_date=cd, doc_type="INVOICE", applies_to="",
                          work_order=l["work_order"], service_month=l["service_month"], body=fixed))
    for l in lines:
        for k, (c, d_, q, u, p) in enumerate(l["body"]):
            rows.append((l["vendor"], l["invoice_no"], l["invoice_date"].isoformat(), l["doc_type"], l["applies_to"],
                         l["work_order"], l["service_month"], k + 1, c, d_, q, u, p, round(q * p, 2)))
    cols = ["vendor", "invoice_no", "invoice_date", "doc_type", "applies_to_invoice", "work_order", "service_month",
            "line_no", "item_code", "description", "quantity", "uom", "unit_price", "amount"]
    X = pd.DataFrame(rows, columns=cols).sort_values(["invoice_date", "vendor", "invoice_no", "line_no"])
    return X.reset_index(drop=True)
