"""Write the target/ pack from the simulated world. Every file is written the way its system exports it."""
import csv, io, json, os, datetime as dt, math, zipfile
import numpy as np
from zoneinfo import ZoneInfo
import params as P
import world as W
import docs

CHI = ZoneInfo(P.TZ)
UTC = dt.timezone.utc
EPOCH16 = dt.datetime(2016, 1, 1, 0, 0, 0)
LABEL = {"REC90": "REC 90", "E10": "E10 UNL", "DSL": "DIESEL"}
POS_PROD = {"REC90": "REC-90 NE", "E10": "E10 87", "DSL": "MARINE DSL"}
BOL_PROD = {"REC90": "NE90", "E10": "E10-87", "DSL": "ULSD-MAR"}
PRICE = {"REC90": 5.29, "E10": 4.49, "DSL": 4.89}


def utc_str(naive_local):
    return naive_local.replace(tzinfo=CHI).astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def ids(rng):
    """structured identifiers, drawn once"""
    site = {}
    used = set()
    for m in P.MARINAS:
        while True:
            v = "S%05d" % int(rng.integers(10000, 99999))
            if v not in used:
                used.add(v); site[m] = v; break
    console = {}
    for m in P.MARINAS:
        console[m] = "TLS4-%06d" % int(rng.integers(100000, 999999))
    console_new_dh = "TLS4-%06d" % int(rng.integers(100000, 999999))
    store = dict(zip(P.MARINAS, [104, 101, 107, 102, 108, 103, 106, 105]))
    newsite = dict(zip(P.MARINAS, ["HBM03", "HBM07", "HBM01", "HBM05", "HBM02", "HBM08", "HBM04", "HBM06"]))
    acct = {m: "%d-%04d" % (int(rng.integers(41, 49)), int(rng.integers(1000, 9999))) for m in P.MARINAS}
    return {"site": site, "console": console, "console_new_dh": console_new_dh, "store": store,
            "newsite": newsite, "acct": acct}


def console_of(o, idm, m, t_local):
    if m == P.CONSOLE_SWAP[0] and t_local >= o["swap_at"]:
        return idm["console_new_dh"]
    return idm["console"][m]


def tank_no(o, tid, t_local):
    m = P.TANKS[tid][0]
    order = [k for k in P.TANKS if P.TANKS[k][0] == m]
    n = order.index(tid) + 1
    if m == P.CONSOLE_SWAP[0] and t_local >= o["swap_at"]:
        n = {1: 2, 2: 1}[n]
    return n


def console_stamp(o, m, t_local):
    """the console's own clock: wrong between a storm restore and the technician's visit"""
    if m in o["resets"]:
        c0, c1, c2 = o["resets"][m]
        if c1 <= t_local < c2:
            return EPOCH16 + (t_local - c1)
    return t_local


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)


def build(target, o):
    rng = np.random.default_rng(P.SEED + 99)
    idm = ids(rng)
    tanks = o["tanks"]
    os.makedirs(target, exist_ok=True)
    seq_new = {}

    # ---- automatic tank gauge inventory export (remote monitoring service) ----
    rows = []
    newbase = {1: int(rng.integers(1000, 3000)), 2: int(rng.integers(1000, 3000))}
    for r in o["readings_kept"]:
        tid, m, t = r["tank"], r["marina"], r["local"]
        cs = console_of(o, idm, m, t)
        tn = tank_no(o, tid, t)
        seq = r["seq"]
        if cs == idm["console_new_dh"]:
            seq_new.setdefault(tn, newbase[tn])
            seq_new[tn] += 1
            seq = seq_new[tn]
        stamp = console_stamp(o, m, t)
        cap = tanks[tid].cap
        ull = round(0.9 * cap - r["gross"], 1)
        rows.append((utc_str(stamp), idm["site"][m], P.MARINAS[m][0], cs, tn, LABEL[tanks[tid].product], seq,
                     "%.3f" % r["h"], "%.2f" % r["water"], "%.1f" % r["T"], "%.1f" % r["gross"], "%.1f" % r["tc"],
                     "%.1f" % ull))
    rows.sort(key=lambda x: (x[1], x[3], x[4], x[6]))
    write_csv(os.path.join(target, "atg_inventory_2026.csv"),
              ["reading_utc", "site_id", "site_name", "console_sn", "tank", "product", "record_seq", "height_in",
               "water_in", "temp_f", "gross_gal", "tc_gal_60f", "ullage_90_gal"], rows)

    # ---- delivery reports ----
    rows = []
    dseq = {}
    for d in o["deliveries"]:
        tid, m = d["tank"], d["marina"]
        cs = console_of(o, idm, m, d["start"])
        tn = tank_no(o, tid, d["start"])
        dseq[cs] = dseq.get(cs, int(rng.integers(300, 700))) + 1
        s0 = console_stamp(o, m, d["start"]); s1 = console_stamp(o, m, d["end"])
        rows.append((idm["site"][m], P.MARINAS[m][0], cs, tn, LABEL[tanks[tid].product], dseq[cs],
                     utc_str(s0), utc_str(s1), "%.3f" % d["h0"], "%.3f" % d["h1"], "%.1f" % d["T0"], "%.1f" % d["T1"],
                     "%.1f" % d["g0"], "%.1f" % d["g1"], "%.1f" % d["n0"], "%.1f" % d["n1"],
                     "%.1f" % (d["g1"] - d["g0"]), "%.1f" % (d["n1"] - d["n0"])))
    rows.sort(key=lambda x: (x[6], x[0]))
    write_csv(os.path.join(target, "atg_deliveries_2026.csv"),
              ["site_id", "site_name", "console_sn", "tank", "product", "delivery_no", "start_utc", "end_utc",
               "start_height_in", "end_height_in", "start_temp_f", "end_temp_f", "start_gross_gal", "end_gross_gal",
               "start_tc_gal_60f", "end_tc_gal_60f", "increase_gross_gal", "increase_tc_gal_60f"], rows)

    # ---- leak test results (as logged by the monitoring service) ----
    rows = []
    for x in sorted(o["tests_exported"], key=lambda x: x["print_at"]):
        tid, m = x["tank"], x["marina"]
        cs = console_of(o, idm, m, x["start"])
        tn = tank_no(o, tid, x["start"])
        stamp = console_stamp(o, m, x["print_at"]) if not x["reprint"] else x["print_at"]
        rows.append([utc_str(stamp), idm["site"][m], cs, tn, LABEL[tanks[tid].product], x["test_no"], "0.20 GPH",
                     x["result"], "" if x["rate"] is None else "%.3f" % x["rate"]])
    rows.sort(key=lambda r: r[0])
    rec = int(rng.integers(500000, 600000))
    out_rows = []
    for r in rows:
        rec += int(rng.integers(1, 9))
        out_rows.append([rec] + r)
    write_csv(os.path.join(target, "atg_leak_tests_2026.csv"),
              ["rec_id", "logged_utc", "site_id", "console_sn", "tank", "product", "test_no", "test", "result",
               "leak_rate_gph"], out_rows)

    # ---- console tank setup ----
    rows = []
    for m in P.MARINAS:
        order = [k for k in P.TANKS if P.TANKS[k][0] == m]
        for i, tid in enumerate(order):
            t = tanks[tid]
            if m == P.CONSOLE_SWAP[0]:
                rows.append((idm["site"][m], idm["console"][m], i + 1, LABEL[t.product], t.chart_no, t.cap, "%.0f" % t.D,
                             tid, "2014-05-20", "2026-02-17"))
                rows.append((idm["site"][m], idm["console_new_dh"], {1: 2, 2: 1}[i + 1], LABEL[t.product], t.chart_no,
                             t.cap, "%.0f" % t.D, tid, "2026-02-17", ""))
            else:
                rows.append((idm["site"][m], idm["console"][m], i + 1, LABEL[t.product], t.chart_no, t.cap, "%.0f" % t.D,
                             tid, "2014-05-20" if m in ("AH", "BP", "CF") else "2016-04-11", ""))
    write_csv(os.path.join(target, "atg_tank_setup.csv"),
              ["site_id", "console_sn", "tank", "product_label", "chart_no", "capacity_gal", "diameter_in",
               "marina_tank_ref", "in_service_from", "in_service_to"], rows)

    # ---- dock sales: legacy point of sale (local time) to go-live, new system (UTC) from the shadow week ----
    legacy, newpos = [], []
    txn_l = {m: int(rng.integers(300000, 400000)) for m in P.MARINAS}
    txn_n = 7_100_000 + int(rng.integers(0, 50000))
    grade_tab = docs.pos_grades()
    rev_grade = {(m, prod): g for (m, g), prod in grade_tab.items()}
    shadow0 = W.local(P.POS_SHADOW[0], 6.0); golive = P.POS_GOLIVE
    sales_sorted = sorted(o["sales"], key=lambda s: s["local"])
    for s in sales_sorted:
        m, t = s["marina"], s["local"]
        prod = s["product"]
        tender = rng.choice(["CARD", "CARD", "CARD", "CASH", "SLIP ACCT"], p=[0.3, 0.25, 0.2, 0.15, 0.10])
        amt = round(round(s["gal_reg"], 2) * PRICE[prod], 2)
        if t < golive:
            txn_l[m] += int(rng.integers(1, 4))
            legacy.append((P.MARINAS[m][0], idm["store"][m], txn_l[m], t.strftime("%m/%d/%Y %H:%M:%S"), s["hose"],
                           POS_PROD[prod], "%.2f" % s["gal_reg"], "%.2f" % PRICE[prod], "%.2f" % amt, tender))
        if t >= shadow0 and (t >= golive or tender == "CARD"):
            txn_n += int(rng.integers(1, 3))
            lag = int(rng.integers(8, 95)) if t < golive else int(rng.integers(30, 160))
            newpos.append({"site": idm["newsite"][m], "txn": "T%d" % txn_n,
                           "ts": (t + dt.timedelta(seconds=lag)).replace(tzinfo=CHI).astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
                           "pump": int(s["hose"][0]), "hose": "ABCD".index(s["hose"][1]) + 1,
                           "grade": rev_grade[(m, prod)], "gal": round(s["gal_reg"], 3), "ppg": PRICE[prod],
                           "amt": amt, "tender": "CARD" if tender == "CARD" else ("ACCT" if tender == "SLIP ACCT" else "CASH")})
    write_csv(os.path.join(target, "dock_sales_legacy_2026.csv"),
              ["store_name", "store_no", "txn_no", "sale_time", "disp_hose", "product", "gallons", "price", "amount",
               "tender"], legacy)
    with open(os.path.join(target, "dock_sales_2026-11-09_2026-12-31.jsonl"), "w", encoding="utf-8", newline="\n") as f:
        for rec_ in newpos:
            f.write(json.dumps(rec_, separators=(",", ":")) + "\n")
    write_csv(os.path.join(target, "pos_grades.csv"), ["site", "grade", "description"],
              [(idm["newsite"][m], g, POS_PROD[p]) for (m, g), p in sorted(grade_tab.items(), key=lambda kv: (idm["newsite"][kv[0][0]], kv[0][1]))])

    # ---- bills of lading (the distributor's export) ----
    rows = []
    bol = int(rng.integers(2600000, 2700000))
    for b in sorted(o["bols"], key=lambda b: b["local"]):
        bol += int(rng.integers(3, 40))
        tid = b["tank"]
        rows.append(("BL%d" % bol, idm["acct"][b["marina"]], P.MARINAS[b["marina"]][0].upper(), "TK%s" % tid.split("-")[1],
                     BOL_PROD[b["product"]], b["local"].strftime("%m/%d/%Y %H:%M"), b["gross"], b["net"], "%.1f" % b["temp"],
                     docs.TRUCKS[int(rng.integers(0, len(docs.TRUCKS)))]))
    write_csv(os.path.join(target, "bols_2026.csv"),
              ["bol_no", "ship_to_acct", "ship_to", "tank_ref", "product", "drop_time", "gross_gal", "net_gal_60f",
               "product_temp_f", "truck"], rows)

    # ---- charts ----
    rows = []
    seen = set()
    for tid, t in tanks.items():
        if t.chart_no in seen:
            continue
        seen.add(t.chart_no)
        q, tab = t.chart_table()
        for h, g in zip(q, tab):
            rows.append((t.chart_no, "%.2f" % h, "%.1f" % g))
    write_csv(os.path.join(target, "tank_charts.csv"), ["chart_no", "height_in", "gallons"], rows)

    # ---- lake levels (Corps daily pool elevations) ----
    rows = []
    rl = np.random.default_rng(P.SEED + 5)
    for lake, base in (("Lake Wenning", 723.0), ("Tolliver Lake", 651.0)):
        lvl = base
        for i in range(365):
            d = dt.date(2026, 1, 1) + dt.timedelta(days=i)
            target_ = base + (6.5 if 120 <= i <= 245 else 0.0) * min(1.0, abs(i - 100) / 40.0 if i < 140 else 1.0)
            lvl += 0.12 * (target_ - lvl) + rl.normal(0, 0.08)
            rows.append((lake, d.isoformat(), "%.2f" % lvl, "%.0f" % max(0, rl.normal(4200 if i % 7 else 6100, 900))))
    write_csv(os.path.join(target, "lake_levels_2026.csv"), ["lake", "date", "pool_elev_ft_ngvd", "outflow_cfs"], rows)

    docs.write_documents(target, o, idm)
    return idm
