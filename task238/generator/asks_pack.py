"""The ask files (the Scanner Code payout records and the flyer keying records) and the two distractors."""
import datetime as dt
import os

import numpy as np

import params as P
import world as W
from pack import write_csv, normalise_zip, xlsx_props, ean13, money, zstamp, STORE

DEPT_CODE = {"GROCERY": 10, "DAIRY": 20, "FROZEN": 25, "BAKERY": 30, "MEAT": 40, "DELI PACKAGED": 45, "SNACKS": 50,
             "BEVERAGES": 55, "HOUSEHOLD": 60, "HEALTH BEAUTY": 70, "PET": 80, "BABY": 85}


def code_payout(scanned, shelf):
    """PI-2 5.1: first unit free up to a correct price of 10.00, else 10.00 off the correct price."""
    pay_now = max(0.0, round(shelf - 10.00, 2))
    return round(scanned - pay_now, 2), pay_now


def write(target, w, r):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    F = P.FILES
    n = {}

    # ---------------- Scanner Code: till overrides (POS, UTC) and service desk adjustments (local) ----------------
    ov = []
    desk = []
    def recno_of(no, reg_no, txn):
        rec = r.choice(["%d-%02d-%d", "%02d-%d", "%d/%02d"])
        if rec.startswith("%d-%02d-"):
            return rec % (no, reg_no, txn)
        if rec.startswith("%02d"):
            return rec % (reg_no, txn)
        return rec % (txn, reg_no)

    for (no, t, i, sc, sh, chan, reg_no, txn, (kind, later)) in w.claim_rows:
        refund, pay_now = code_payout(sc, sh)
        if chan == "till":
            charged = sh if kind == "partial" else pay_now
            ov.append([no, reg_no, txn, zstamp(t), w.upc[i], int(round(sc * 100)), int(round(charged * 100)), "SC",
                       "OP%03d" % (int(r.integers(10, 99)))])
            if kind == "dup":       # the approving supervisor's entry for the same payout
                desk.append([STORE[no][2], later, recno_of(no, reg_no, txn), ean13(w.upc[i]), w.desc[i],
                             "Scanner Code", refund])
            elif kind == "partial":  # the rest of the Code remedy, paid at the desk on the same receipt
                desk.append([STORE[no][2], later, recno_of(no, reg_no, txn), ean13(w.upc[i]), w.desc[i],
                             "Scanner Code", round(refund - (sc - sh), 2)])
        else:
            desk.append([STORE[no][2], later, recno_of(no, reg_no, txn), ean13(w.upc[i]), w.desc[i],
                         "Scanner Code", refund])
    # ordinary overrides and desk adjustments that are not Code payouts
    keys = sorted(w.daytot)
    for _ in range(2300):
        no, d = keys[int(r.integers(len(keys)))]
        hrs = W.hours_of(d)
        t = W.local(d, r.uniform(hrs[0], hrs[-1] + 1))
        i = int(r.integers(len(w.upc)))
        p = float(w.reg[i])
        code = r.choice(["PM", "MD", "DM", "MGR"], p=[0.30, 0.38, 0.22, 0.10])
        newp = round(p * {"PM": 0.85, "MD": 0.5, "DM": 0.7, "MGR": 0.9}[code], 2)
        ov.append([no, int(r.integers(1, 9)), int(r.integers(4000, 9999)), zstamp(t), w.upc[i], int(round(p * 100)),
                   int(round(newp * 100)), code, "OP%03d" % int(r.integers(10, 99))])
    for _ in range(1500):
        no, d = keys[int(r.integers(len(keys)))]
        hrs = W.hours_of(d)
        t = W.local(d, r.uniform(hrs[0], hrs[-1] + 1))
        i = int(r.integers(len(w.upc)))
        reason = r.choice(["Return - no receipt", "Damaged", "Rain Check", "Price Match", "Coupon"],
                          p=[0.34, 0.22, 0.12, 0.2, 0.12])
        if reason == "Coupon":
            amt = [0.50, 0.75, 1.00, 1.50, 2.00][i % 5]
        else:
            amt = round(float(w.reg[i]) * {"Price Match": 0.15, "Rain Check": 0.25}.get(reason, 1.0), 2)
        desk.append([STORE[no][2], t, "%d-%02d-%d" % (no, int(r.integers(1, 9)), int(r.integers(4000, 9999))),
                     ean13(w.upc[i]), w.desc[i], reason, amt])
    ov = [x for x in ov if "2026-10-01T00:00:00Z" <= x[3] < "2027-01-01T00:00:00Z"]   # the export's UTC window
    ov.sort(key=lambda x: (x[3], x[0]))
    write_csv(os.path.join(target, F["overrides"]),
              ["store_no", "register", "transaction", "override_utc", "upc", "orig_price_cents",
               "override_price_cents", "reason_code", "operator"], ov)
    n["overrides"] = len(ov)
    wb = Workbook()
    wb.remove(wb.active)
    desk.sort(key=lambda x: x[1])
    for mth, name in ((10, "October"), (11, "November"), (12, "December")):
        ws = wb.create_sheet(name)
        ws.append(["Store", "Date / time", "Receipt #", "UPC", "Item", "Reason", "Refund $"])
        for row in desk:
            if row[1].month == mth and row[1].year == 2026:
                ws.append([row[0], row[1].replace(tzinfo=None), row[2], row[3], row[4], row[5], row[6]])
        for rr in ws.iter_rows(min_row=2):
            rr[1].number_format = "yyyy-mm-dd hh:mm"
            rr[6].number_format = "0.00"
    xlsx_props(wb, "Saltmarsh Market Customer Service", "Service desk adjustments Q4 2026")
    p = os.path.join(target, F["desk"])
    wb.save(p)
    normalise_zip(p, P.file_stamp_utc("desk"))
    n["desk"] = sum(1 for row in desk if row[1].year == 2026 and row[1].month >= 10)

    # ---------------- flyer keying: the ad plan, the two price change releases, the flyer item weekly units -----
    rows = []
    for (k, line, members, qty, price_q, lead) in w.ad_lines:
        d = w.co[k]["date"]
        txt = ("$%.2f" % price_q) if qty == 1 else ("%d/$%.2f" % (qty, price_q) if qty == 2 else
                                                     "%d for $%d" % (qty, int(round(price_q))))
        copy = w.famname[w.fam[lead]] + (", assorted" if len(members) > 1 else "")
        if len(members) == 1:
            copy = w.desc[lead]
        rows.append([d.isoformat(), "%03d" % line, w.upc[lead][:11], copy, txt])
    write_csv(os.path.join(target, F["adplan"]), ["flyer_start", "ad_line", "upc_11", "ad_copy", "ad_price"], rows)
    n["adplan"] = len(rows)

    wb = Workbook()
    wb.remove(wb.active)
    for rel in ("PRELIM", "REVISED"):
        ws = wb.create_sheet(rel)
        ws.append(["Release", "Issued", "Effective", "EAN", "Description", "Zone", "Change", "Price", "Price qty"])
        for k, c in enumerate(w.co):
            d = c["date"]
            issued = d - dt.timedelta(days=3 if rel == "PRELIM" else 2)
            relid = "PCR-%s-%s" % (d.strftime("%y%m%d"), "P" if rel == "PRELIM" else "R")
            ad_set = set(int(x) for x in c["ad_items"])
            for j, i in enumerate(c["items"]):
                i = int(i)
                for zone in (1, 2):
                    if i in ad_set:
                        qty, pq = w.keyed[(k, i, zone, rel)]
                    else:
                        qty, pq = 1, float(c["new"][j])
                    ws.append([relid, issued, d, ean13(w.upc[i]), W.abbrev(w.parts[i]), zone, c["kind"][j], pq, qty])
        for rr in ws.iter_rows(min_row=2):
            rr[1].number_format = "yyyy-mm-dd"
            rr[2].number_format = "yyyy-mm-dd"
            rr[7].number_format = "0.00"
    xlsx_props(wb, "Saltmarsh Market Pricing", "Weekly price change releases Q4 2026")
    p = os.path.join(target, F["pricefile"])
    wb.save(p)
    normalise_zip(p, P.file_stamp_utc("pricefile"))
    n["pricefile"] = sum(2 * 2 * len(c["items"]) for c in w.co)

    rows = []
    for (k, i, zone, j), u in sorted(w.ad_units.items()):
        d = w.co[k]["date"] + dt.timedelta(days=j)
        rows.append([w.co[k]["date"].isoformat(), d.isoformat(), w.upc[i], "Z%d" % zone, u])
    write_csv(os.path.join(target, F["adsales"]), ["flyer_start", "sales_date", "upc", "price_zone", "units"], rows)
    n["adsales"] = len(rows)

    rows = []
    cid = 5100
    for (k, i, zone), (j, q, pq) in sorted(w.corr.items()):
        d = w.co[k]["date"] + dt.timedelta(days=j)
        cid += int(r.integers(1, 4))
        rows.append(["PC-%d" % cid, ean13(w.upc[i]), "Zone %d" % zone, d.isoformat(), "%.2f" % pq, q,
                     (d - dt.timedelta(days=1)).isoformat()])
    for _ in range(int(r.integers(30, 45))):      # ordinary mid-week corrections to regular prices
        k = int(r.integers(len(w.co)))
        c = w.co[k]
        regs = [j for j in range(len(c["items"])) if c["kind"][j] == "REG"]
        j = regs[int(r.integers(len(regs)))]
        day = int(r.integers(1, 6))
        d = c["date"] + dt.timedelta(days=day)
        cid += int(r.integers(1, 4))
        rows.append(["PC-%d" % cid, ean13(w.upc[c["items"][j]]), "Zone %d" % int(r.integers(1, 3)), d.isoformat(),
                     "%.2f" % float(c["new"][j]), 1, (d - dt.timedelta(days=1)).isoformat()])
    rows.sort(key=lambda x: (x[3], x[0]))
    write_csv(os.path.join(target, F["corrections"]),
              ["correction_id", "ean", "zone", "effective_at_open", "price", "price_qty", "labels_sent"], rows)
    n["corrections"] = len(rows)

    # ---------------- distractors ----------------
    rows = []
    cats = ["Pricing - shelf vs till", "Pricing - flyer", "Product quality", "Availability", "Service",
            "Store cleanliness", "Parking / access", "Other"]
    cw = np.array([0.07, 0.05, 0.24, 0.22, 0.2, 0.08, 0.06, 0.08])
    alias = {101: ["Quinpool", "Saltmarsh Quinpool Rd"], 102: ["Spryfield", "Herring Cove Rd"],
             103: ["Clayton Park", "Lacewood"], 104: ["Bedford", "Bedford Place"], 105: ["Portland St", "Dartmouth"],
             106: ["Cole Harbour"], 107: ["Sackville", "Lower Sackville"], 201: ["Truro"], 202: ["New Glasgow"],
             203: ["Antigonish"], 204: ["Kentville", "New Minas"], 205: ["Bridgewater"], 206: ["Yarmouth"],
             207: ["Amherst"]}
    cid = 88000
    for s in P.STORES:
        no = s[0]
        for _ in range(int(r.poisson(s[6] / 260))):
            d = P.Q_START + dt.timedelta(days=int(r.integers(0, 92)))
            cid += int(r.integers(1, 9))
            rows.append(["CC-%d" % cid, d.isoformat(), alias[no][int(r.integers(len(alias[no])))],
                         r.choice(["Phone", "Email", "Web form", "Social"], p=[0.38, 0.22, 0.3, 0.1]),
                         cats[int(r.choice(len(cats), p=cw / cw.sum()))],
                         "Y" if r.random() < 0.86 else "N"])
    rows.sort(key=lambda x: x[1])
    write_csv(os.path.join(target, F["contacts"]),
              ["contact_id", "received", "store_mentioned", "channel", "category", "resolved"], rows)
    n["contacts"] = len(rows)

    rows = []
    for s in P.STORES:
        no = s[0]
        for d in W.days():
            if not W.hours_of(d):
                continue
            for _ in range(int(r.poisson(2.2))):
                i = int(r.integers(len(w.upc)))
                p = float(w.reg[i])
                why = r.choice(["BEST BEFORE", "DAMAGED PKG", "DISCONTINUED", "SEASONAL"], p=[0.45, 0.25, 0.2, 0.1])
                if why == "BEST BEFORE" and w.dept[i] in ("HOUSEHOLD", "HEALTH BEAUTY"):
                    why = "DISCONTINUED"     # no best-before date on paper towels or shampoo
                rows.append([no, d.isoformat(), w.upc[i], DEPT_CODE[w.dept[i]], money(round(p * 0.5, 2)), why,
                             int(r.integers(1, 7))])
    write_csv(os.path.join(target, F["markdowns"]),
              ["store_no", "printed_date", "upc", "dept", "clearance_price", "reason", "tags"], rows)
    n["markdowns"] = len(rows)
    return n
