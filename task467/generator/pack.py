"""The pack's data files, each in its producing system's own layout: the centre's two goods-in exports (the scanner
software changed on 1 January 2026, with a new layout and format), the returns processing log, the refund ledger, the
order extract, the customer cases, the goodwill vouchers and their redemptions, and the centre's daily operations
workbook and shift rota (the last two distractors). Layer 1 lives here and only here, and on the main call's path it is
neutral by construction: the two goods-in layouts, prepaid labels on the 2025 records and on parcels still arriving on
them in January 2026, failed card refunds reissued as store credit in the same month and on the same side of day 15,
the refund ledger's UTC stamps (its 18:00 runs fall on the same date either way), the finance system's pence column from
April. The ask files carry their own: UTC stamps, partial redemptions, statuses as at the extract, cases with no order.
Nothing here carries the main call's step or an ask's handling."""
import csv
import datetime as dt

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

import sim as S
import world as W

UTC = dt.timezone.utc


def to_utc(local_naive):
    return local_naive.replace(tzinfo=W.local_tz()).astimezone(UTC)


def iso_offset(local_naive):
    return local_naive.replace(tzinfo=W.local_tz()).isoformat()


def z(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(r)
    return len(rows)


def write_parquet(path, table):
    pq.write_table(table, path, compression="snappy", use_dictionary=True, write_statistics=False,
                   version="2.6", data_page_version="1.0")
    return table.num_rows


# ----------------------------------------------------------------------------------------------- goods-in scans
def goods_events(x):
    """Every goods-in scan: each return parcel once, at its delivery."""
    p = x["parcels"]
    ev = [{"t": int(s), "barcode": p["barcode"][i], "carrier": p["carrier"][i], "door": str(p["door"][i]), "cls": "RET"}
          for i, s in enumerate(p["deliv"])]
    ev.sort(key=lambda e: (e["t"], e["barcode"]))
    ops = ["GI%03d" % k for k in (11, 12, 14, 17, 21, 23, 26, 31, 32, 38)]
    for k, e in enumerate(ev):
        e["user"] = ops[(e["t"] // 3600 + k % 3) % len(ops)]
    return ev


def id_run(start, n, name):
    """An identifier run with the gaps a live system leaves (cancelled and test events)."""
    r = S.rng(name)
    return list(start + np.cumsum(r.choice([1, 1, 1, 1, 1, 1, 2, 2, 3, 5], size=n)))


OLD_TYPE = {"RET": "RETURN"}
NEW_CARRIER = {"Tarnwell": "TWL", "Ambrell Post": "AMB", "Kestrix": "KSX", "Vellum Parcels": "VLP"}


def write_goods(x, path25, path26):
    ev = goods_events(x)
    cut = S.sec(dt.datetime(2026, 1, 1))
    old = [e for e in ev if e["t"] < cut]
    new = [e for e in ev if e["t"] >= cut]
    rows = []
    ids = id_run(100_000, len(old), "scan_ids")
    for k, e in enumerate(old):
        rows.append([int(ids[k]), S.at(e["t"]).strftime("%Y-%m-%d %H:%M:%S"), e["door"], e["barcode"], e["carrier"],
                     OLD_TYPE[e["cls"]], e["user"]])
    n25 = write_csv(path25, ["scan_id", "scanned_at_uk", "door", "barcode", "carrier", "item_type", "scanned_by"], rows)
    ts = [S.at(e["t"]) for e in new]
    tbl = pa.table({
        "event_id": pa.array([int(v) for v in id_run(7_400_001, len(new), "event_ids")], pa.int64()),
        "event_ts_uk": pa.array(ts, pa.timestamp("s")),
        "dock_door": pa.array([int(e["door"][1]) for e in new], pa.int8()),
        "parcel_barcode": pa.array([e["barcode"] for e in new], pa.string()),
        "carrier_code": pa.array([NEW_CARRIER[e["carrier"]] for e in new], pa.string()),
        "parcel_class": pa.array([e["cls"] for e in new], pa.string()),
        "handheld_user": pa.array([e["user"].lower() for e in new], pa.string()),
    })
    n26 = write_parquet(path26, tbl)
    return n25, n26


# ------------------------------------------------------------------------------------------------- processing
OUTCOME = {"REFUND": "REFUND", "REJECT_RETURNED": "REJECTED - RETURNED TO CUSTOMER",
           "REJECT_DISPOSED": "REJECTED - DISPOSED"}


def processing_rows(x):
    """One record per parcel opened, at the moment it was opened, with the order read from the returns note and the
    prepaid label where the parcel had one."""
    p = x["parcels"]
    r = S.rng("processing_noise")
    benches = ["B%02d" % k for k in range(1, 15)]
    ops = ["RC%03d" % k for k in (104, 107, 109, 112, 118, 121, 125, 126, 130, 133, 137, 141, 142, 150, 151, 158)]
    recs = []
    for t, i in x["opened"]:
        recs.append({"t": t, "bench": benches[int(r.integers(0, len(benches)))], "op": ops[int(r.integers(0, len(ops)))],
                     "order": p["order_ref"][i], "label": p["label"][i], "outcome": OUTCOME[p["outcome"][i]]})
    recs.sort(key=lambda d: d["t"])
    return recs


def write_processing(x, path):
    recs = processing_rows(x)
    ids = id_run(31_000_000, len(recs), "process_ids")
    rows = [["P%08d" % ids[k], S.at(d["t"]).strftime("%Y-%m-%d %H:%M:%S"), d["bench"], d["op"], d["order"], d["label"],
             d["outcome"]] for k, d in enumerate(recs)]
    return write_csv(path, ["process_id", "processed_at_uk", "bench", "operator", "order_ref", "return_label", "outcome"],
                     rows)


# ---------------------------------------------------------------------------------------------------- refunds
def refund_rows(x):
    """The refund ledger: each return refund in the 18:00 payment run after its parcel was opened (a card refund that
    fails is reissued as store credit in a later run), and the refunds that are not for returns."""
    p = x["parcels"]
    r = S.rng("refund_rows")
    site = x["cust_site"]
    recs = []
    for i in range(len(p["deliv"])):
        if p["refund_day"][i] is None:
            continue
        cur = "EUR" if site[int(p["cust"][i])] == "IE" else "GBP"
        tender = str(r.choice(["CARD", "PAYPAL", "GIFT CARD"], p=[0.82, 0.12, 0.06]))
        amt = round(float(p["total"][i]) * (1.0 if cur == "GBP" else 1.16), 2)
        t0 = dt.datetime.combine(p["refund_day"][i], dt.time(18, 0)) + dt.timedelta(seconds=int(r.integers(4, 2400)))
        if p["failed"][i]:
            recs.append({"t": t0, "order": p["order_ref"][i], "reason": "RETURN", "tender": "CARD", "cur": cur,
                         "amt": amt, "status": "FAILED", "of": None, "key": i})
            t1 = dt.datetime.combine(p["reissue_day"][i], dt.time(18, 0)) + dt.timedelta(seconds=int(r.integers(4, 2400)))
            recs.append({"t": t1, "order": p["order_ref"][i], "reason": "RETURN", "tender": "STORE CREDIT", "cur": cur,
                         "amt": amt, "status": "PAID", "of": i, "key": None})
        else:
            recs.append({"t": t0, "order": p["order_ref"][i], "reason": "RETURN", "tender": tender, "cur": cur,
                         "amt": amt, "status": "PAID", "of": None, "key": None})
    # refunds that are not for returns, against the customers' other orders (never an order a refund-delay voucher's
    # own order field holds: that order had no refund of any kind)
    o = x["other"]
    held = {v["auto_key"][1] for v in x["vouchers"] if v["auto_key"] is not None and v["auto_key"][0] == "O"}
    for d in W.days():
        if not S.payment_run_day(d):
            continue
        for reason, rate in (("CANCELLATION", 34), ("PRICE MATCH", 6), ("GOODWILL", 3), ("NOT DELIVERED", 5)):
            for _ in range(r.poisson(rate)):
                k = int(r.integers(0, len(o["cust"])))
                if k in held:
                    continue
                cur = "EUR" if site[o["cust"][k]] == "IE" else "GBP"
                amt = round(o["total"][k] * (1.16 if cur == "EUR" else 1.0) * (1.0 if reason in ("CANCELLATION", "NOT DELIVERED")
                                                                                else r.uniform(0.05, 0.3)), 2)
                t = dt.datetime.combine(d, dt.time(18, 0)) + dt.timedelta(seconds=int(r.integers(4, 2400)))
                recs.append({"t": t, "order": o["order_ref"][k], "reason": reason,
                             "tender": str(r.choice(["CARD", "PAYPAL"], p=[0.86, 0.14])), "cur": cur, "amt": amt,
                             "status": "PAID", "of": None, "key": None})
    recs.sort(key=lambda d: (d["t"], d["order"]))
    ids = {}
    for k, d in enumerate(recs):
        d["id"] = "RF%08d" % (60_000_000 + 3 * k + int(r.integers(0, 3)))
        if d["key"] is not None:
            ids[d["key"]] = d["id"]
    for d in recs:
        d["of_id"] = ids[d["of"]] if d["of"] is not None else None
    return recs


def write_refunds(x, path):
    recs = refund_rows(x)
    cut = dt.datetime(2026, 4, 1)
    tbl = pa.table({
        "refund_id": pa.array([d["id"] for d in recs], pa.string()),
        "order_ref": pa.array([d["order"] for d in recs], pa.string()),
        "reason": pa.array([d["reason"] for d in recs], pa.string()),
        "tender": pa.array([d["tender"] for d in recs], pa.string()),
        "currency": pa.array([d["cur"] for d in recs], pa.string()),
        "amount": pa.array([d["amt"] if d["t"] < cut else None for d in recs], pa.float64()),
        "amount_pence": pa.array([int(round(d["amt"] * 100)) if d["t"] >= cut else None for d in recs], pa.int64()),
        "initiated_at_utc": pa.array([to_utc(d["t"]) for d in recs], pa.timestamp("us", tz="UTC")),
        "status": pa.array([d["status"] for d in recs], pa.string()),
        "reissue_of": pa.array([d["of_id"] for d in recs], pa.string()),
    })
    return write_parquet(path, tbl)


# ------------------------------------------------------------------------------------- orders, cases, vouchers
def extract_customers(x):
    """The order extract's scope: customers with a parcel delivered from 1 December 2025 or a 2026 case."""
    p = x["parcels"]
    cut = S.sec(dt.datetime(2025, 12, 1))
    keep = set(int(c) for c, s in zip(p["cust"], p["deliv"]) if s >= cut)
    keep |= set(cs["cust"] for cs in x["cases"])
    return keep


def write_orders(x, path):
    p, o = x["parcels"], x["other"]
    keep = extract_customers(x)
    since = S.sec(dt.datetime(2025, 10, 1))
    site, cid = x["cust_site"], x["cust_ids"]
    rows = []
    for i in range(len(p["deliv"])):
        c = int(p["cust"][i])
        if c in keep and p["ordered"][i] >= since:
            rows.append((int(p["ordered"][i]), p["order_ref"][i], c, float(p["total"][i]), p["category"][i]))
    for k in range(len(o["cust"])):
        c = o["cust"][k]
        if c in keep and o["ordered"][k] >= since:
            rows.append((o["ordered"][k], o["order_ref"][k], c, o["total"][k], o["category"][k]))
    rows.sort(key=lambda r: r[1])
    eur = [site[r[2]] == "IE" for r in rows]
    tot = [round(r[3] * (1.16 if e else 1.0), 2) for r, e in zip(rows, eur)]
    tbl = pa.table({
        "order_ref": pa.array([r[1] for r in rows], pa.string()),
        "customer_ref": pa.array(["C%07d" % cid[r[2]] for r in rows], pa.string()),
        "site": pa.array(["wrenfieldholt.ie" if e else "wrenfieldholt.co.uk" for e in eur], pa.string()),
        "currency": pa.array(["EUR" if e else "GBP" for e in eur], pa.string()),
        "ordered_at_utc": pa.array([to_utc(S.at(r[0])) for r in rows], pa.timestamp("us", tz="UTC")),
        "order_total": pa.array(tot, pa.float64()),
        "order_total_gbp": pa.array([round(t * W.EUR_RATE, 2) if e else t for t, e in zip(tot, eur)], pa.float64()),
        "main_category": pa.array([r[4] for r in rows], pa.string()),
    })
    return write_parquet(path, tbl)


def write_cases(x, path):
    cid = x["cust_ids"]
    rows = []
    for cs in x["cases"]:
        ref = x["ref"][cs["key"]] if cs["key"] is not None else ""
        rows.append([cs["case_ref"], "C%07d" % cid[cs["cust"]], z(to_utc(S.at(cs["opened"]))), cs["channel"],
                     cs["topic"], ref, z(to_utc(S.at(cs["closed"]))) if cs["closed"] <= S.sec(dt.datetime(2026, 10, 30)) else ""])
    return write_csv(path, ["case_ref", "customer_ref", "opened_at_utc", "channel", "topic", "order_ref", "closed_at_utc"],
                     rows)


def voucher_status(x, v, asof):
    used = sum(d["applied"] for d in x["redemptions"] if d["voucher"] is v)
    if used >= v["value"] - 0.005:
        return "REDEEMED"
    if used > 0:
        return "PART REDEEMED" if v["expires"] >= asof else "EXPIRED"
    return "ACTIVE" if v["expires"] >= asof else "EXPIRED"


def write_vouchers(x, path):
    cid = x["cust_ids"]
    asof = dt.date.fromisoformat(W.AS_OF)
    rows = []
    for v in sorted(x["vouchers"], key=lambda v: v["code"]):
        rows.append([v["code"], "C%07d" % cid[v["cust"]], x["ref"][v["auto_key"]] if v["auto_key"] else "", v["case"],
                     v["reason"], v["value"], z(to_utc(S.at(v["issued"]))), v["expires"].isoformat(),
                     voucher_status(x, v, asof)])
    return write_csv(path, ["voucher_code", "customer_ref", "order_ref", "case_ref", "reason", "value", "issued_at",
                            "expires_on", "status"], rows)


def write_redemptions(x, path):
    rows = []
    for d in sorted(x["redemptions"], key=lambda d: d["id"]):
        rows.append([d["id"], d["voucher"]["code"], x["ref"][d["order_key"]], z(to_utc(S.at(d["t"]))),
                     "%.2f" % d["applied"]])
    return write_csv(path, ["redemption_id", "voucher_code", "order_ref", "redeemed_at", "amount_applied"], rows)


# --------------------------------------------------------------------------------- the centre's operating records
def daily_ops(x):
    """The supervisor's end-of-day sheet: parcels booked in at goods-in (every delivery the dock took), parcels opened,
    refunds triggered, parcels waiting at close by the bay count, and the team on shift."""
    p = x["parcels"]
    ev = goods_events(x)
    r = S.rng("dailyops")
    booked, opened, trig = {}, {}, {}
    for e in ev:
        booked[S.day_of(e["t"])] = booked.get(S.day_of(e["t"]), 0) + 1
    for t, i in x["opened"]:
        d = S.day_of(t)
        opened[d] = opened.get(d, 0) + 1
        if p["outcome"][i] == "REFUND":
            trig[d] = trig.get(d, 0) + 1
    waiting = 0
    rows = []
    rets = {}
    for s in p["deliv"]:
        rets[S.day_of(s)] = rets.get(S.day_of(s), 0) + 1
    for d in W.days():
        waiting += rets.get(d, 0) - opened.get(d, 0)
        team = 0 if opened.get(d, 0) == 0 else int(round(opened.get(d, 0) / r.uniform(52, 61)))
        rows.append([d, booked.get(d, 0), opened.get(d, 0), trig.get(d, 0), waiting + int(r.integers(-6, 7)) if waiting > 40 else waiting,
                     team])
    return rows


def rota_rows(x):
    r = S.rng("rota")
    rows = []
    for d in W.days():
        if d < dt.date(2026, 1, 1):
            continue
        cap = S.capacity_base(d)
        if d.weekday() == 6 or d in W.BANK_HOLIDAYS:
            shifts = [("Weekend", 0.6 * cap / 55)]
        elif d.weekday() == 5:
            shifts = [("Weekend", 0.85 * cap / 55)]
        else:
            shifts = [("Early", 0.55 * cap / 55), ("Late", 0.45 * cap / 55)]
        for name, need in shifts:
            agency = 0 if d < dt.date(2026, 2, 16) else int(max(0, round(need * r.uniform(0.15, 0.3))))
            rows.append([d.isoformat(), name, max(1, int(round(need)) - agency), agency])
    return rows
