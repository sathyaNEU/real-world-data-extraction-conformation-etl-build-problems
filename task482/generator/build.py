"""task482 architecture 16: writes the pack into a folder from the world.

    python3 task482/generator/build.py [folder]
"""
import csv
import datetime as dt
import os
import shutil
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs as D     # noqa: E402
import params as P   # noqa: E402
import world as W    # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
ALLOY = {"BIL6063": "6063", "BIL6082": "6082", "INGLM25": "LM25"}


def rs(k):
    return np.random.default_rng([P.SEED, 7000 + k])


def write_csv(path, header, rows, eol="\r\n"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator=eol)
        wr.writerow(header)
        wr.writerows(rows)


def minute(t):
    """A logged local time: the world's instant in local wall time, to the minute."""
    x = W.loc(t)
    return (x + dt.timedelta(seconds=30)).replace(second=0, microsecond=0)


def r20(x):
    return int(round(x / 20.0)) * 20


# ------------------------------------------------------------------------------------------------ gas
def periods():
    out = []
    for k in range(len(P.READS) - 1):
        a, b = P.READS[k], P.READS[k + 1]
        out.append(dict(k=k, a=a, b=b, ua=W.utc(a), ub=W.utc(b), cv=P.CV[k]))
    return out


def gas_meter(w, path, per):
    ex = W.utc(P.METER_EXCHANGE_LOCAL)
    rows, vol = [], np.zeros(W.N)
    k = 0
    for i in range(W.N):
        t = W.T0 + i * W.STEP
        while not (per[k]["ua"] <= t < per[k]["ub"]):
            k += 1
        m3 = w["metered"][i] * 3.6 / (P.VCF * per[k]["cv"])
        stamp = t.strftime("%Y-%m-%d %H:%M")
        if t < ex:
            v = round(m3 / P.HCF_M3, 2)
            rows.append(("8804419362", P.OLD_METER, stamp, "%.2f" % v, "hcf", "A"))
        else:
            v = round(m3, 3)
            rows.append(("8804419362", P.NEW_METER, stamp, "%.3f" % v, "m3", "A"))
        vol[i] = v
    write_csv(path, ["MPRN", "Meter serial", "Interval start (UTC)", "Consumption", "Unit", "Read type"], rows)
    return vol


def gas_invoices(w, path, per, vol):
    ex = W.utc(P.METER_EXCHANGE_LOCAL)
    starts = [W.T0 + i * W.STEP for i in range(W.N)]

    def idx(t):
        return max(0, min(W.N, int((t - W.T0) / W.STEP)))

    # the gas burned outside the export: December 2025 and the first days of January 2027, shaped on 2026's
    dec = float(w["metered"][idx(W.utc(dt.datetime(2026, 12, 3, 9, 45))):].sum()) * 1.013
    jan = float(w["metered"][:idx(W.utc(dt.datetime(2026, 1, 6, 10, 15)))].sum()) * 0.987
    dec_hcf = dec * 3.6 / (P.VCF * per[0]["cv"]) / P.HCF_M3
    jan_m3 = jan * 3.6 / (P.VCF * per[-1]["cv"])
    cum = np.concatenate([[0.0], np.cumsum(vol)])
    old0, new0 = 2846213.0, 12.0

    def reg(t):
        """The register at instant t: the old meter's in hcf before the exchange, the new meter's in m3 after."""
        if t < W.T0:
            return old0
        if t <= ex:
            return old0 + dec_hcf + cum[idx(t)]
        if t >= W.T1:
            return new0 + cum[W.N] - cum[idx(ex)] + jan_m3 * min(1.0, (t - W.T1) / (W.utc(P.READS[-1]) - W.T1))
        return new0 + cum[idx(t)] - cum[idx(ex)]

    invoices = []
    for p in per:
        meters = []
        if p["ub"] <= ex:
            o, c = int(reg(p["ua"])), int(reg(p["ub"]))
            meters.append(dict(serial=P.OLD_METER, open=o, close=c, units="hcf", m3=(c - o) * P.HCF_M3,
                               **{"from": p["a"], "to": p["b"]}))
        elif p["ua"] >= ex:
            o, c = int(reg(p["ua"])), int(reg(p["ub"]))
            meters.append(dict(serial=P.NEW_METER, open=o, close=c, units="m3", m3=float(c - o),
                               **{"from": p["a"], "to": p["b"]}))
        else:
            o, c = int(reg(p["ua"])), int(reg(ex))
            meters.append(dict(serial=P.OLD_METER, open=o, close=c, units="hcf", m3=(c - o) * P.HCF_M3,
                               **{"from": p["a"], "to": P.METER_EXCHANGE_LOCAL}))
            o2, c2 = int(new0), int(reg(p["ub"]))
            meters.append(dict(serial=P.NEW_METER, open=o2, close=c2, units="m3", m3=float(c2 - o2),
                               **{"from": P.METER_EXCHANGE_LOCAL, "to": p["b"]}))
        m3 = round(sum(m["m3"] for m in meters), 2)
        kwh = int(round(m3 * P.VCF * p["cv"] / 3.6))
        rate = P.UNIT_RATE_P[p["k"]]
        days = (p["b"].date() - p["a"].date()).days
        charge = round(kwh * rate / 100.0, 2)
        standing = round(days * P.STANDING_GBP_DAY, 2)
        ccl = round(kwh * P.CCL_P_KWH / 100.0, 2)
        vat = round(0.2 * (charge + standing + ccl), 2)
        note = ""
        if p["ub"] <= ex:
            note = ("Imperial meter: the register reads in hundreds of cubic feet, converted at 2.83 cubic metres "
                    "to the unit.")
        elif p["ua"] < ex:
            note = ("Meter exchange on 14 April 2026 at 10:30: imperial meter %s removed at %d (hundreds of cubic "
                    "feet, converted at 2.83 cubic metres to the unit); metric meter %s fitted at %05d cubic metres."
                    % (P.OLD_METER, meters[0]["close"], P.NEW_METER, int(new0)))
        invoices.append(dict(no="NG-%06d" % (418273 + 61 * p["k"]), issued=p["b"] + dt.timedelta(days=4 + p["k"] % 3),
                             meters=meters, m3=m3, cv=p["cv"], kwh=kwh, rate=rate, charge=charge, days=days,
                             standing=standing, ccl=ccl, vat=vat, total=round(charge + standing + ccl + vat, 2),
                             note=note))
    D.invoices_pdf(path, invoices)
    return invoices


# ------------------------------------------------------------------------------------------------ process logs
def furnace_logs(w, path):
    r = rs(3)
    lot_of = {id(l["heat"]): l["lot"] for l in w["lots"] if "heat" in l}
    remarks = ["Mg addition", "hold for chemistry", "door seal checked", "fluxed", "skimmed twice",
               "burner 2 relit", "sample re-taken"]
    sheets = []
    for fur in ("M1", "M2"):
        rows = []
        for h in [x for x in w["heats"] if x["furnace"] == fur]:
            rem = remarks[int(r.integers(len(remarks)))] if r.random() < 0.06 else ""
            rows.append([h["heat"], ALLOY[h["family"]], minute(h["charged"]), minute(h["complete"]),
                         round(h["tonnes"], 2), lot_of[id(h)], rem])
        # rows keyed in twice from the shift sheets
        out = []
        dup_at = {}
        for j, row in enumerate(rows):
            out.append(row)
            if r.random() < 0.013:
                dup_at.setdefault(j + int(r.integers(1, 6)), []).append(list(row[:6]) + [
                    "re-keyed from shift sheet" if r.random() < 0.5 else ""])
            for d in dup_at.pop(j, []):
                out.append(d)
        for k in sorted(dup_at):
            out.extend(dup_at[k])
        sheets.append(("%s casthouse" % fur, ["Heat", "Alloy", "Charged", "Melted out", "Charge t", "Cast lot",
                                              "Remarks"], out))
    rows = [[c["charge"], minute(c["charged"]), int(round(c["tonnes"] * 1000)), ""] for c in w["m3"]]
    sheets.append(("M3 tower melter", ["Charge", "Charged", "Weight kg", "Remarks"], rows))
    fmt = {"M1 casthouse": {3: "dd/mm/yyyy hh:mm", 4: "dd/mm/yyyy hh:mm", 5: "0.00"},
           "M2 casthouse": {3: "dd/mm/yyyy hh:mm", 4: "dd/mm/yyyy hh:mm", 5: "0.00"},
           "M3 tower melter": {2: "dd/mm/yyyy hh:mm", 3: "#,##0"}}
    widths = {"M1 casthouse": [8, 7, 17, 17, 9, 11, 24], "M2 casthouse": [8, 7, 17, 17, 9, 11, 24],
              "M3 tower melter": [8, 17, 11, 20]}
    D.workbook(path, sheets, P.PEOPLE["works"], P.PEOPLE["works"], "2026-01-02T07:41:00Z", "2027-01-19T15:22:00Z",
               "Brackwell Alloys Ltd", widths=widths, formats=fmt)


def h1_log(w, path):
    rows = []
    for ld in w["h1"]:
        rows.append([ld["load"], ALLOY[ld["family"]], minute(ld["start"]).strftime("%d/%m/%Y %H:%M"),
                     minute(ld["end"]).strftime("%d/%m/%Y %H:%M"), "%.2f" % ld["tonnes"],
                     "; ".join("%s %.2f" % (lot, t) for lot, t in ld["lots"])])
    write_csv(path, ["Load", "Alloy", "Door closed", "Door opened", "Billet t", "Lots (t)"], rows, eol="\n")


def t1_log(w, path):
    rows = []
    for b in w["t1"]:
        rows.append([b["batch"], minute(b["start"]).strftime("%Y-%m-%dT%H:%M"),
                     minute(b["end"]).strftime("%Y-%m-%dT%H:%M"), b["pieces"], int(round(b["tonnes"] * 1000)),
                     " ".join(lot for lot, _ in b["lots"])])
    write_csv(path, ["Batch", "Start", "End", "Pieces", "Net kg", "Cast lots"], rows, eol="\n")


def lots_file(w, path):
    rows = []
    for lot in w["lots"]:
        for res, when in lot["inspections"]:
            rows.append((when, lot["lot"], [lot["lot"], P.FAM_NAME[lot["family"]],
                                            W.loc(lot["cast"]).strftime("%Y-%m-%d"), int(round(lot["tonnes"] * 1000)),
                                            minute(when).strftime("%d/%m/%Y %H:%M"), res]))
    rows.sort(key=lambda x: (x[0], x[1]))
    write_csv(path, ["Lot", "Product", "Cast date", "Net kg", "Inspected", "Result"], [x[2] for x in rows])


def weather(w, path):
    r = rs(5)
    rows = []
    for d, m in zip(w["days"], w["tmean"]):
        lo = m - 3.1 - abs(r.normal(0, 0.9))
        hi = m + 3.1 + abs(r.normal(0, 0.9))
        rain = max(0.0, r.gamma(0.7, 3.2) - 0.8) if r.random() < 0.55 else 0.0
        rows.append([d.strftime("%Y-%m-%d"), "%.1f" % m, "%.1f" % lo, "%.1f" % hi, "%.1f" % rain])
    write_csv(path, ["Date", "Mean C", "Min C", "Max C", "Rain mm"], rows, eol="\n")


# ------------------------------------------------------------------------------------------------ Velden
def calloffs(path):
    r = rs(6)
    parts = [("AL-BIL-6063-178", "Extrusion billet EN AW-6063, 178 mm", "BIL6063", 4320),
             ("AL-BIL-6063-254", "Extrusion billet EN AW-6063, 254 mm", "BIL6063", 2880),
             ("AL-BIL-6082-203", "Extrusion billet EN AW-6082, 203 mm", "BIL6082", 3000),
             ("AL-ING-42000", "Foundry ingot EN AC-42000 (LM25)", "INGLM25", 1800),
             ("CS-77140-TF", "Sand casting, rear subframe bracket, EN AC-42000 T6 (LM25-TF)", "CSTLM25", 650)]
    for f in P.FAM_CODES:
        assert sum(p[3] for p in parts if p[2] == f) == P.CALLOFF_2027[f]
    rows = []
    for code, desc, fam, tot in parts:
        wts = np.clip(r.normal(1.0, 0.11, 12), 0.7, 1.3)
        wts[7] *= 0.55
        wts[11] *= 0.8
        raw = tot * wts / wts.sum()
        q = np.floor(raw).astype(int)
        for j in np.argsort(-(raw - q))[:tot - q.sum()]:
            q[j] += 1
        rows.append([code, desc, "t"] + [int(x) for x in q] + [tot])
    head = ["Velden part", "Description", "Unit"] + [dt.date(2027, m, 1).strftime("%b") for m in range(1, 13)] + \
        ["Total 2027"]
    notes = [["Call-off schedule for contract year 2027, supplier Brackwell Alloys Ltd (supplier no. 70-44183)."],
             ["Quantities are tonnes delivered to Velden's Kassel and Wolfsfeld plants in the month."],
             ["Issued by Purchasing, light metals, 14 December 2026. Revision 0."]]
    D.workbook(path, [("Call-offs 2027", head, rows), ("Notes", ["Notes"], notes)], P.PEOPLE["buyer"],
               P.PEOPLE["buyer"], "2026-11-27T13:05:00Z", "2026-12-14T08:47:00Z", "Velden Automobil AG",
               widths={"Call-offs 2027": [17, 52, 6] + [7] * 12 + [11], "Notes": [90]})


# ------------------------------------------------------------------------------------------------ the weighbridge
def weighbridge(w, wb_path, gi_path):
    """Scrap in (one or two grades a load, a two-grade load weighed between its tips), product despatches, and
    Midland's dross lifts (some bringing returned metal, unloaded and weighed before the skip is lifted)."""
    r = rs(7)
    letters = "ABCDEFGHJKLMNOPRSTUVWXY"

    def reg_no():
        return "%s%s%02d %s%s%s" % (letters[r.integers(23)], letters[r.integers(23)], int(r.choice([16, 66, 17, 67,
                                    18, 68, 19, 69, 70, 21, 71, 22, 72])), letters[r.integers(23)],
                                    letters[r.integers(23)], letters[r.integers(23)])

    fleets = {}
    for name, _, _ in P.SUPPLIERS:
        fleets[name] = [(reg_no(), float(r.uniform(14200, 16500))) for _ in range(int(r.integers(2, 5)))]
    for name, _ in P.CUSTOMERS:
        fleets[name] = [(reg_no(), float(r.uniform(14300, 16200))) for _ in range(int(r.integers(3, 7)))]
    fleets[P.DROSS_HAULIER] = [(reg_no(), float(r.uniform(12850, 13450))) for _ in range(2)]
    fleets["MDR flatbed"] = [(reg_no(), float(r.uniform(11800, 12600)))]
    hauliers = {"Velden Automobil AG (Rhenus Logistics)": "Rhenus Logistics", "Kestrel Extrusions Ltd": "Kestrel",
                "Albion Profiles Ltd": "Albion", "Hallam Castings Ltd": "Hallam", "Severn Diecast Ltd": "Severn"}
    sup_w = np.array([s[2] for s in P.SUPPLIERS])
    sup_w = sup_w / sup_w.sum()
    cus_w = np.array([c[1] for c in P.CUSTOMERS])
    cus_w = cus_w / cus_w.sum()
    load_range = {"UBC": (17000, 23500), "EXT": (11000, 22000), "CST": (13000, 24500), "TRN": (15000, 26000)}
    rejects = ["free iron in load", "wet swarf", "plastics and rubber", "magnesium contamination", "lead present"]
    SKIP = 2180.0
    visits = []
    d = dt.date(P.YEAR, 1, 5)
    while d <= dt.date(P.YEAR, 12, 23):
        if d.weekday() < 5 and d not in P.SHUT_DAYS:
            day = []
            for _ in range(int(r.poisson(8.2))):
                s = P.SUPPLIERS[int(r.choice(len(P.SUPPLIERS), p=sup_w))]
                veh, tare = fleets[s[0]][int(r.integers(len(fleets[s[0]])))]
                tare += float(r.normal(0, 60))
                two = len(s[1]) > 1 and r.random() < 0.30
                if two:
                    g = list(r.choice(s[1], 2, replace=False))
                    total = float(r.uniform(15000, 25000))
                    share = float(r.uniform(0.62, 0.80))
                    first_big = r.random() < 0.5
                    parts = [share * total, (1 - share) * total] if first_big else [(1 - share) * total, share * total]
                    tips = list(zip(g, parts))                       # in the order tipped
                    decl_total = total * (1 + float(r.normal(0.003, 0.011)))
                    # the merchant's note splits the load by eye, to the nearest twentieth and the nearest tonne
                    big_est = float(np.clip(share + r.normal(0, 0.07), 0.55, 0.9))
                    lines = []
                    for gg, amt in tips:
                        est = big_est if amt == max(parts) else 1 - big_est
                        lines.append(dict(grade=gg, declared=int(round(decl_total * round(est * 20) / 20, -3)),
                                          status="Accepted", remark="", bales=int(round(amt / r.uniform(330, 370)))
                                          if gg == "UBC" else "", actual=amt))
                    weights = [tare + total, tare + parts[1], tare + float(r.normal(0, 25))]
                    kind = "scrap2"
                else:
                    gg = s[1][int(r.integers(len(s[1])))]
                    amt = float(r.uniform(*load_range[gg]))
                    rej = r.random() < 0.016
                    if gg == "UBC":
                        bw = float(r.normal(352, 18))
                        bales = int(round(amt / bw))
                        decl = bales * 360
                    else:
                        bales = ""
                        decl = int(round(amt * (1 + float(r.normal(0.003, 0.011))), -1))
                    lines = [dict(grade=gg, declared=decl, status="Rejected - returned to supplier" if rej else
                                  "Accepted", remark=rejects[int(r.integers(len(rejects)))] if rej else "",
                                  bales=bales)]
                    weights = [tare + amt, tare + (amt - float(r.uniform(0, 60)) if rej else float(r.normal(0, 25)))]
                    kind = "scrap1"
                day.append(dict(kind=kind, supplier=s[0], vehicle=veh, haulier=s[0], movement="Goods in",
                                lines=lines, weights=[r20(x) for x in weights],
                                order=[gg for gg, _ in tips] if two else None))
            for _ in range(int(r.poisson(7.4))):
                c = P.CUSTOMERS[int(r.choice(len(P.CUSTOMERS), p=cus_w))]
                veh, tare = fleets[c[0]][int(r.integers(len(fleets[c[0]])))]
                tare += float(r.normal(0, 60))
                day.append(dict(kind="despatch", supplier=c[0], vehicle=veh, haulier=hauliers[c[0]],
                                movement="Despatch", lines=[], weights=[r20(tare), r20(tare + r.uniform(19000, 26000))]))
            if d.weekday() in (0, 2, 4):
                veh, truck = fleets[P.DROSS_HAULIER][int(r.integers(2))]
                truck += float(r.normal(0, 40))
                dross = float(r.uniform(5600, 9400))
                if r.random() < 0.35:
                    sows = float(r.uniform(1000, 2400))
                    weights = [truck + SKIP + sows, truck + SKIP, truck + float(r.normal(0, 20)) + SKIP + dross]
                    lines = [dict(grade=P.TOLL[0], declared=int(round(sows * (1 + float(r.normal(0, 0.004))), -1)),
                                  status="Accepted", remark="", bales="", supplier=P.DROSS_HAULIER)]
                    kind = "dross2"
                else:
                    weights = [truck + SKIP, truck + float(r.normal(0, 20)) + SKIP + dross]
                    lines, kind = [], "dross1"
                day.append(dict(kind=kind, supplier=P.DROSS_HAULIER, vehicle=veh, haulier="Midland Dross Recovery",
                                movement="Waste out", lines=lines, weights=[r20(x) for x in weights]))
            if d.weekday() == 3 and r.random() < 0.8:
                veh, tare = fleets["MDR flatbed"][0]
                sows = float(r.uniform(7600, 14800))
                day.append(dict(kind="toll", supplier=P.DROSS_HAULIER, vehicle=veh, haulier="Midland Dross Recovery",
                                movement="Goods in", lines=[dict(grade=P.TOLL[0], declared=int(round(
                                    sows * (1 + float(r.normal(0, 0.004))), -1)), status="Accepted", remark="",
                                    bales="")], weights=[r20(tare + sows), r20(tare + r.normal(0, 25))]))
            # the day's visits in arrival order, each with its own weighing times
            arr = sorted(float(x) for x in r.uniform(6.5, 16.75, len(day)))
            order = r.permutation(len(day))
            for a, j in zip(arr, order):
                v = day[int(j)]
                t = dt.datetime.combine(d, dt.time()) + dt.timedelta(hours=a)
                times = [t]
                for _ in v["weights"][1:]:
                    t = t + dt.timedelta(minutes=float(r.uniform(13, 38)))
                    times.append(t)
                v["times"] = [x.replace(microsecond=0) for x in times]
                v["day"] = d
                visits.append(v)
        d += dt.timedelta(days=1)
    visits.sort(key=lambda v: (v["times"][0], v["vehicle"]))
    # no quarter's tonnes may sit on a half tonne: the last ordinary load in such a cell weighs in a little heavier
    def quarter_of(v):
        return (v["day"].month - 1) // 3

    cells = {}
    for v in visits:
        q = quarter_of(v)
        ws = v["weights"]
        if v["kind"] == "scrap1" and v["lines"][0]["status"] == "Accepted":
            cells.setdefault((v["lines"][0]["grade"], q), [0, None])[0] += ws[0] - ws[-1]
            cells[(v["lines"][0]["grade"], q)][1] = (v, 0)
        elif v["kind"] == "scrap2":
            for k, gg in enumerate(v["order"]):
                cells.setdefault((gg, q), [0, None])[0] += ws[k] - ws[k + 1]
        elif v["kind"] in ("dross1", "dross2"):
            cells.setdefault(("dross", q), [0, None])[0] += ws[-1] - ws[-2]
            cells[("dross", q)][1] = (v, len(ws) - 1)
    for key in sorted(cells, key=str):
        kg, last = cells[key]
        rem = kg % 1000
        if 440 <= rem <= 560:
            v, j = last
            v["weights"][j] += 600 - rem if rem >= 500 else 400 - rem
    no = 0
    reset_done = False
    for v in visits:
        if not reset_done and v["day"] >= P.WB_RESET:
            no, reset_done = 0, True
        no += 1
        v["ticket"] = no
    # the weighbridge export: one row per weighing, stamped in UTC
    rows = []
    for v in visits:
        for k, (t, kg) in enumerate(zip(v["times"], v["weights"])):
            rows.append([v["ticket"], k + 1, W.utc(t).strftime("%Y-%m-%d %H:%M:%S"), kg, v["vehicle"], v["haulier"],
                         v["movement"]])
    write_csv(wb_path, ["Ticket", "Weighing", "Weighed (UTC)", "Weight kg", "Vehicle", "Haulier", "Movement"], rows)
    # the goods-in register: one line per grade, the lines of a load entered in grade order
    gl, grn = [], 0
    names = dict(P.GRADES + [P.TOLL])
    for v in visits:
        for ln in sorted(v["lines"], key=lambda x: x["grade"]):
            grn += 1
            gl.append(["GRN-%05d" % (26000 + grn), v["day"].strftime("%d/%m/%Y"), v["supplier"], ln["grade"],
                       names[ln["grade"]], ln["bales"], ln["declared"], v["ticket"], ln["status"], ln["remark"]])
    write_csv(gi_path, ["GRN", "Date", "Supplier", "Grade", "Description", "Bales", "Declared kg", "WB ticket",
                        "Status", "Remarks"], gl)
    return visits


# ------------------------------------------------------------------------------------------------ distractors
def electricity(w, path):
    r = rs(9)
    act = {k: (w["comp"][k] > 0).astype(float) for k in ("melt", "m3", "h1", "t1")}
    kw = 410 + 1150 * act["melt"] + 520 * act["m3"] + 140 * act["h1"] + 95 * act["t1"]
    kw = kw * (1 + r.normal(0, 0.035, W.N))
    hh = kw.reshape(-1, 2).mean(axis=1) * 0.5           # kWh in each UTC half hour
    rows = []
    d = dt.date(P.YEAR, 1, 1)
    while d.year == P.YEAR:
        a = W.utc(dt.datetime.combine(d, dt.time()))
        b = W.utc(dt.datetime.combine(d + dt.timedelta(days=1), dt.time()))
        i0, i1 = int((a - W.T0) / dt.timedelta(minutes=30)), int((b - W.T0) / dt.timedelta(minutes=30))
        for k, i in enumerate(range(i0, min(i1, len(hh)))):
            rows.append(["1580061423376", d.strftime("%d/%m/%Y"), k + 1, "%.1f" % hh[i], "A"])
        d += dt.timedelta(days=1)
    write_csv(path, ["MPAN", "Settlement date", "Settlement period", "Import kWh", "Status"], rows)


def assets(path):
    gas = [["M1", "Reverberatory melting furnace, 50 t, two regenerative burner pairs", "Casthouse", "Natural gas",
            4200, 2009, "2026-07-14"],
           ["M2", "Reverberatory melting furnace, 50 t, two regenerative burner pairs", "Casthouse", "Natural gas",
            4200, 2012, "2026-08-06"],
           ["M3", "Tower melter, 1.5 t/h, with holding chamber", "Foundry", "Natural gas", 1350, 2017, "2026-08-11"],
           ["H1", "Homogenizing furnace, 50 t billet, six recuperative burners", "Billet shop", "Natural gas", 2400,
            2014, "2026-08-10"],
           ["T1", "Solution treatment and ageing oven, 7 t", "Foundry", "Natural gas", 900, 2019, "2026-08-12"],
           ["LP1", "Ladle preheater", "Casthouse", "Natural gas", 250, 2015, "2026-03-02"],
           ["LP2", "Ladle preheater", "Foundry", "Natural gas", 250, 2018, "2026-03-03"],
           ["LH1-3", "Launder heaters (three)", "Casthouse", "Natural gas", 180, 2012, "2026-08-04"],
           ["RT1-26", "Radiant tube heaters (26)", "Works", "Natural gas", 1040, 2011, "2026-09-21"],
           ["B1", "Office boiler", "Offices", "Natural gas", 120, 2016, "2026-09-08"]]
    elec = [["CM1", "Vertical DC billet casting machine", "Casthouse", "Electricity", 310, 2009, "2026-08-05"],
            ["SW1", "Billet saw line", "Billet shop", "Electricity", 160, 2014, "2026-08-10"],
            ["AC1-3", "Air compressors (three)", "Works", "Electricity", 330, 2020, "2026-05-18"],
            ["SM1", "Sand mixer and reclamation plant", "Foundry", "Electricity", 220, 2017, "2026-08-11"],
            ["CR1-4", "Overhead cranes (four)", "Works", "Electricity", 180, 2009, "2026-04-20"],
            ["F1", "Fume extraction fans and baghouse", "Casthouse", "Electricity", 260, 2013, "2026-08-04"]]
    head = ["Asset", "Description", "Location", "Energy", "Rated input kW", "Installed", "Last service"]
    D.workbook(path, [("Gas plant", head, gas), ("Electrical plant", head, elec)], P.PEOPLE["works"],
               P.PEOPLE["works"], "2019-03-11T10:02:00Z", "2026-09-22T14:36:00Z", "Brackwell Alloys Ltd",
               widths={"Gas plant": [9, 62, 12, 12, 14, 10, 12], "Electrical plant": [9, 62, 12, 12, 14, 10, 12]})


def roster(path):
    rows = []
    d = dt.date(2025, 12, 29)
    k = 0
    while d.year <= P.YEAR:
        if d.year == P.YEAR or d + dt.timedelta(days=6) >= dt.date(P.YEAR, 1, 1):
            shut_week = all((d + dt.timedelta(days=j)) in P.SHUT_DAYS or j >= 5 for j in range(7))
            crews = "ABCD"
            if shut_week:
                rows.append([d.strftime("%d/%m/%Y"), "Casthouse", "", "", "", "shutdown"])
                rows.append([d.strftime("%d/%m/%Y"), "Foundry", "", "", "", "shutdown"])
            else:
                rot = [crews[(k + j) % 4] for j in range(4)]
                rows.append([d.strftime("%d/%m/%Y"), "Casthouse", rot[0], rot[1], rot[2], rot[3]])
                rows.append([d.strftime("%d/%m/%Y"), "Foundry", "EF"[k % 2], "EF"[(k + 1) % 2], "", ""])
                k += 1
        d += dt.timedelta(days=7)
    write_csv(path, ["Week commencing", "Area", "Early 06-14", "Late 14-22", "Night 22-06", "Rest crew"], rows)


# ------------------------------------------------------------------------------------------------ the pack
def build(folder=TARGET):
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    os.makedirs(folder)
    F = {k: os.path.join(folder, v) for k, v in P.FILES.items()}
    w = W.simulate()
    per = periods()
    vol = gas_meter(w, F["meter"], per)
    inv = gas_invoices(w, F["invoices"], per, vol)
    furnace_logs(w, F["furnaces"])
    h1_log(w, F["h1"])
    t1_log(w, F["t1"])
    lots_file(w, F["lots"])
    weather(w, F["weather"])
    D.scr2_pdf(F["scr2"])
    calloffs(F["calloff"])
    visits = weighbridge(w, F["weighbridge"], F["goodsin"])
    electricity(w, F["elec"])
    assets(F["assets"])
    roster(F["roster"])
    D.email(F["email"], [P.FILES[k] for k in ("meter", "invoices", "furnaces", "h1", "t1", "lots", "weather",
                                               "elec", "weighbridge", "goodsin", "assets", "roster")])
    t = dt.datetime(2027, 1, 21, 16, 12).timestamp()
    for f in os.listdir(folder):
        os.utime(os.path.join(folder, f), (t, t))
    return dict(world=w, invoices=inv, visits=visits)


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else TARGET
    build(out)
    print("built", len(os.listdir(out)), "files in", out)
