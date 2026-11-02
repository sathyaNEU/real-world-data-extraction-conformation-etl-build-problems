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
            o["_second_ticket"] = True
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
                o["_retrip_ticket"] = True
    allr = recs + extra
    allr.sort(key=lambda r: (r["start"], r["device_id"], r["kind"]))
    storm_retrips(allr)
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
        truth.append((oid, o["kind"], o["storm"], o["start"], o["level"], o["cause"], o["unit_id"], o["district"],
                      bool(o.get("_storm_retrip", False))))
    cols = ["ticket_no", "start_local", "level", "service_area", "circuit", "unit_id", "device_type", "device_id",
            "cause_code", "members_out", "step", "step_restored_local", "members_restored"]
    X = pd.DataFrame(rows, columns=cols)
    K = pd.DataFrame(truth, columns=["ticket_no", "kind", "storm", "start", "level", "cause", "unit_id", "district",
                                     "storm_retrip"])
    return X, K


RETRIP_DAYS = (date(2025, 6, 18), date(2025, 12, 9))       # 2025's storm days, the outage system in storm mode


def storm_retrips(allr):
    """in storm mode a device's ticket stays open until the dispatcher releases the device, so when a device the crew
    has restored trips again on the storm day the outage system logs the re-trip under the same ticket: a step whose
    members restored are negative (every member the device had restored is off again, at the time it tripped),
    then the steps that restore them. Drawn on its own stream, after every other record is final, on tickets with one
    restoration step, no second ticket and no re-trip of their own, whose device is free until the last new step; so
    nothing else in the export moves"""
    rng = np.random.default_rng(P.SEED + 97)
    held = {}
    for o in allr:
        held.setdefault(o["device_id"], []).append(o)
    for day in RETRIP_DAYS:
        for d in P.DISTRICTS:
            pool = [o for o in allr if o["start"].date() == day and o["district"] == d and o["storm"]
                    and o["level"] == "PRIMARY" and o["cause"] != "PLANNED" and o["kind"] != "duplicate"
                    and len(o["steps_min"]) == 1 and o["members"] >= 3 and o["steps_min"][0] > 10
                    and not o.get("_second_ticket") and not o.get("_retrip_ticket")]
            k = int(rng.integers(2, 5))
            for i in rng.permutation(len(pool)):
                if k == 0:
                    break
                o = pool[int(i)]
                t1 = o["steps_min"][0]
                gap = int(rng.integers(25, 181))
                if (o["start"] + timedelta(minutes=t1 + gap)).date() != day:
                    continue                                    # the re-trip falls on the storm day
                dur = int(rng.integers(35, 200))
                end = o["start"] + timedelta(minutes=t1 + gap + dur + 90)
                if any(x is not o and x["start"] <= end and o["start"] <= x["start"] + timedelta(minutes=int(x["steps_min"][-1]))
                       for x in held[o["device_id"]]):
                    continue                                    # the device is out on nothing else meanwhile
                m = int(o["members"])
                if m >= 40 and rng.random() < 0.5:
                    a = int(round(m * rng.uniform(0.35, 0.7)))
                    later = int(rng.integers(20, 90))
                    o["steps_min"] = [t1, t1 + gap, t1 + gap + dur, t1 + gap + dur + later]
                    o["steps_members"] = [m, -m, a, m - a]
                else:
                    o["steps_min"] = [t1, t1 + gap, t1 + gap + dur]
                    o["steps_members"] = [m, -m, m]
                o["_storm_retrip"] = True
                k -= 1


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
    # the work order system numbers every record it keys, completions among them, so a completion's record number
    # steps over the others (its own stream: nothing else in the pack moves)
    gaps = np.random.default_rng(P.SEED + 89).integers(1, 8, len(T))
    T["record_id"] = ["TC%07d" % (1000230 + int(c)) for c in np.cumsum(gaps)]
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


AP_FROM = date(2024, 12, 1)                  # the extract: every trimming document dated 1 December 2024 to the run
PORTAL = {P.OUTGOING: date(2025, 1, 1), P.INCOMING: date(2025, 4, 1)}   # each firm's first invoice through the portal
ITEM = {"TRIM": "Right-of-way trimming, overhead primary", "HAZ": "Hazard tree removal",
        "HERB": "Herbicide, brush regrowth", "MOB": "Crew mobilization"}
HLC_TEXT = {"TRIM": "ROW TRIM OH PRI", "HAZ": "HAZARD TREE REMOVAL", "HERB": "HERBICIDE BRUSH REGROWTH",
            "MOB": "CREW MOBILIZATION"}
GVS_TEXT = {"TRIM": "Trimming OH primary ROW", "HAZ": "Hazard tree removal", "HERB": "Herbicide - brush regrowth",
            "MOB": "Mobilization"}
MON = ("JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC")


def _last_day(y, m):
    return (date(y + (m == 12), m % 12 + 1, 1) - timedelta(days=1)).day


def vendor_text(con, kind, wo, svc, half):
    """the line as the firm types it into the supplier portal: the item, the work order and the period of the work"""
    y, m = int(svc[:4]), int(svc[5:])
    if con == P.OUTGOING:
        return "%s, %s, %s %d" % (HLC_TEXT[kind], wo, MON[m - 1], y)
    d0, d1 = (1, 15) if half == 1 else (16, _last_day(y, m))
    return "%s | %s | %02d/%02d/%d-%02d/%02d/%d" % (GVS_TEXT[kind], wo, m, d0, y, m, d1, y)


def invoices(T, U, rng):
    """accounts payable's trimming documents dated from 1 December 2024 to the run: the outgoing firm bills each work
    order monthly in miles, the new firm each half month in linear feet; some long work orders run two progress
    invoices in a month; a disputed invoice is voided by a credit memo that names the invoice it reverses, and
    re-issued under a new number. AP keys a paper invoice with the month of the work as its service month; the supplier
    portal, which each firm used from its first invoice dated on or after its go-live, fills the service month from the
    document's own date when the firm leaves the service period blank, and the firm types the work order and the period
    of the work into the line"""
    T = T[(T.measured > 0)].copy()
    T["svc"] = T.completed.map(lambda d: "%d-%02d" % (d.year, d.month))
    T = T[(T.svc >= "2024-11") & (T.svc <= "2025-12")]
    T["half"] = T.completed.map(lambda d: 1 if d.day <= 15 else 2)
    vendors = {P.OUTGOING: ("HLC", "MI", 1.0, 2740.0), P.INCOMING: ("GVS", "LF", FT_PER_MI, 0.59)}
    rows = []
    lines = []
    sizes = T[T.contractor == P.OUTGOING].groupby(["work_order", "svc"]).size()
    force = set()
    for q in (1, 2, 3, 4):
        cand = sizes[[k[1].startswith("2025") and (int(k[1][5:]) - 1) // 3 + 1 == q for k in sizes.index]]
        cand = cand[cand >= 2]
        if len(cand):
            force.add(cand.idxmax())
    portal = lambda con, d: d >= PORTAL[con]

    def describe(con, kind, wo, svc, half, on_portal, credit_of=None):
        if not on_portal:
            return ITEM[kind]
        t = vendor_text(con, kind, wo, svc, half)
        if credit_of:
            t = ("CR INV %s, " % credit_of + t) if con == P.OUTGOING else ("Credit to %s | " % credit_of + t)
        return t

    for (con, wo, svc), g in T.groupby(["contractor", "work_order", "svc"], sort=True):
        code, uom, mult, price = vendors[con]
        y, m = int(svc[:4]), int(svc[5:])
        if con == P.INCOMING:
            parts = [(1, g[g.half == 1]), (2, g[g.half == 2])]
        elif (wo, svc) in force or (len(g) > 12 and rng.random() < 0.6):
            cut = len(g) // 2
            parts = [(0, g.iloc[:cut]), (0, g.iloc[cut:])]
        else:
            parts = [(0, g)]
        for pi, (half, part) in enumerate(parts):
            if part.empty:
                continue
            miles = float(part.measured.sum())
            qty = round(miles * mult, 2) if uom == "MI" else float(int(round(miles * mult)))
            inv_date = (date(y, m, 15) if (pi == 0 and len(parts) > 1) else
                        (date(y + (m == 12), m % 12 + 1, 1) + timedelta(days=int(rng.integers(2, 12)))))
            inv = None
            body = [("TRIM", qty, uom, price)]
            if rng.random() < 0.35:
                body.append(("HAZ", float(int(rng.integers(1, 9))), "EA", 315.0))
            if rng.random() < 0.25:
                body.append(("HERB", round(float(rng.uniform(2, 30)), 1), "AC", 96.0))
            if pi == 0 and rng.random() < 0.12:
                body.append(("MOB", 1.0, "LS", 1850.0))
            lines.append(dict(vendor=con, invoice_no=inv, invoice_date=inv_date, doc_type="INVOICE", applies_to="",
                              work_order=wo, svc=svc, half=half, body=body))
    lines = [l for l in lines if AP_FROM <= l["invoice_date"] <= P.EXPORT]
    room = lambda l: (P.EXPORT - l["invoice_date"]).days - 2            # days a credit memo has before the extract
    disputed = [i for i, l in enumerate(lines) if rng.random() < 0.13 and room(l) >= 20]
    cells = {}
    for i, l in enumerate(lines):
        if l["svc"].startswith("2025") and room(l) >= 8:
            q = (int(l["svc"][5:]) - 1) // 3 + 1
            cells.setdefault((l["vendor"], q), []).append(i)
    for key in sorted(cells):
        if not any(i in disputed for i in cells[key]):
            disputed.append(cells[key][int(rng.integers(0, len(cells[key])))])
    disputed = sorted(set(disputed))
    for i in disputed:
        l = lines[i]
        cd = l["invoice_date"] + timedelta(days=int(rng.integers(15 if room(l) >= 20 else 5, min(41, room(l) + 1))))
        con = l["vendor"]
        l["invoice_no"] = l["invoice_no"] or ("#%d" % i)
        cm, ri = "CM#%d" % i, "RI#%d" % i
        neg = [(c, -q, u, p) for c, q, u, p in l["body"]]
        lines.append(dict(vendor=con, invoice_no=cm, invoice_date=cd, doc_type="CREDIT MEMO", applies_to=l["invoice_no"],
                          work_order=l["work_order"], svc=l["svc"], half=l["half"], body=neg))
        fixed = [(c, q, u, round(p * (0.97 if c == "TRIM" else 1.0), 4)) for c, q, u, p in l["body"]]
        lines.append(dict(vendor=con, invoice_no=ri, invoice_date=cd, doc_type="INVOICE", applies_to="",
                          work_order=l["work_order"], svc=l["svc"], half=l["half"], body=fixed))
    # each firm numbers its own documents in date order; the cooperative is one of its customers, so the series steps
    # over the documents the firm sends elsewhere (its own stream, so nothing above moves)
    nrng = np.random.default_rng(P.SEED + 83)
    num = {P.OUTGOING: 40211, P.INCOMING: 7105}
    name = {}
    for i, l in enumerate(lines):
        if l["invoice_no"] is None:
            l["invoice_no"] = "#%d" % i
    order = sorted(range(len(lines)), key=lambda i: (lines[i]["invoice_date"], lines[i]["vendor"],
                                                      lines[i]["doc_type"] != "CREDIT MEMO", lines[i]["invoice_no"]))
    for i in order:
        l = lines[i]
        con = l["vendor"]
        num[con] += int(nrng.integers(1, 10))
        code = vendors[con][0]
        name[l["invoice_no"]] = ("%s-CM%05d" % (code, num[con])) if l["doc_type"] == "CREDIT MEMO" else \
            ("%s-%06d" % (code, num[con]))
    for l in lines:
        l["invoice_no"] = name[l["invoice_no"]]
        if l["applies_to"]:
            l["applies_to"] = name[l["applies_to"]]
    truth = []
    for l in lines:
        con, d = l["vendor"], l["invoice_date"]
        on = portal(con, d)
        credit = l["doc_type"] == "CREDIT MEMO"
        service = "%d-%02d" % (d.year, d.month) if on else ("" if credit else l["svc"])
        for k, (c, q, u, p) in enumerate(l["body"]):
            text = describe(con, c, l["work_order"], l["svc"], l["half"], on, l["applies_to"] if credit else None)
            rows.append((con, l["invoice_no"], d.isoformat(), l["doc_type"], l["applies_to"], l["work_order"], service,
                         k + 1, "%s-%s" % (c, u), text, q, u, p, round(q * p, 2)))
            truth.append((l["invoice_no"], k + 1, l["svc"], on))
    cols = ["vendor", "invoice_no", "invoice_date", "doc_type", "applies_to_invoice", "work_order", "service_month",
            "line_no", "item_code", "description", "quantity", "uom", "unit_price", "amount"]
    X = pd.DataFrame(rows, columns=cols).sort_values(["invoice_date", "vendor", "invoice_no", "line_no"])
    # the month of the work each line bills and whether it came through the portal: the generator's truth for the
    # checks, never shipped
    Y = pd.DataFrame(truth, columns=["invoice_no", "line_no", "work_month", "portal"])
    return X.reset_index(drop=True), Y
