"""Renders the Kelvanna Lake world into target/: every file in the format, layout and conventions of the system that
writes it. Returns the clean truth for checks.py."""
import datetime as dt
import math
import os

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font

import params as P
import world as W
import world_ops as O
import docs
from io_util import write_csv, save_xlsx, set_mtime

F_LIMS = "gc_assays_lims_export_20261105.csv"
F_MODEL = "kl_mz_resource_model_2026R.csv"
F_DEPL = "survey_depletion_2023-01_2026-10.csv"
F_PLAN = "kelvanna_mine_plan_2027.xlsx"
F_BASIS = "budget_2027_basis_of_ore_and_gold.pdf"
F_RECON = "monthly_reconciliation_jan2023_oct2026.pdf"
F_GRID = "kelvanna_mine_grid_control.txt"
F_MILL = "mill_daily_production_2023-2026.csv"
F_BARS = "goldroom_bar_register_2025-2026.csv"
F_REF = "refinery_outturn_statements_2025-2026.csv"
F_DISP = "dispatch_loads_to_lgsp_2023-2026.csv"
F_FLEET = "haul_fleet_register_2026-10.xlsx"
F_INV = "stockpile_inventory_2022-12-31.csv"
F_DCS = "dcs_event_export_grinding_2025-2026.csv"
F_CMMS = "cmms_work_orders_grinding_2025-2026.csv"
F_EXPL = "mz_exploration_assays_2019-2022.csv"
F_GEOT = "pit_slope_review_phase5_2026.pdf"
F_PRICE = "budget_2027_price_and_fx_deck.pdf"
DISTRACTORS = [F_EXPL, F_GEOT, F_PRICE]
REFINERY_PULL = dt.date(2026, 11, 6)


def plan_scope(df):
    """The 2027 schedule: benches 1215 to 1190 and the west end of bench 1185 up to the planned face position."""
    p = df[(df["period"] == "PLAN")].copy()
    extra = df[(df["bench"] == 1185) & (df["xc"] < P.PLAN_1185_FACE_X)].copy()
    if len(extra):
        extra["period"] = "PLAN"
        xf = (extra["xc"] - P.X0) / (P.NX * P.BX)
        extra["plan_month"] = 12
    return pd.concat([p, extra]).sort_values(["plan_month", "bench", "xc", "yc"]).reset_index(drop=True)


def build(out):
    os.makedirs(out, exist_ok=True)
    rngp = W._rng("pack")
    df = W.blocks()
    edge = W.edge_blocks(df)
    df = W.sequence(df)
    hd = W.holes(df, edge)
    lab = O.lab_stream(hd)
    truth = {}

    # ---------------- laboratory export ----------------
    lab = lab.sort_values(["received", "batch"], kind="stable").reset_index(drop=True)
    mig = dt.date(2025, 7, 1)
    hole_ids = _hole_ids(hd)
    leg_no, new_no, job_no = 104_116, {}, {}
    rows = []
    for _, r in lab.iterrows():
        legacy = r["received"] < mig
        if legacy:
            sid = "BH%06d" % leg_no
            leg_no += 1 + (1 if rngp.random() < 0.012 else 0)
            job = ""
        else:
            yy = r["received"].year % 100
            new_no[yy] = new_no.get(yy, 0) + 1 + (1 if rngp.random() < 0.012 else 0)
            sid = "KS%02d-%06d" % (yy, new_no[yy] + (4000 if yy == 25 else 100))
            bkey = (yy, int(r["batch"]))
            if bkey not in job_no:
                job_no[bkey] = sum(1 for k in job_no if k[0] == yy) + (412 if yy == 25 else 1)
            job = "KLAB-%02d-%04d" % (yy, job_no[bkey])
        kind = r["kind"]
        stype = {"BH": ("BH", "BLASTHOLE"), "FD": ("DUP", "FIELD DUP"), "CRM": ("STD", "CRM"),
                 "BLK": ("BLK", "BLANK")}[kind][0 if legacy else 1]
        fmt = (lambda d: d.strftime("%d/%m/%Y")) if legacy else (lambda d: d.isoformat())
        if kind in ("BH", "FD"):
            h = hd.loc[int(r["hole"])]
            e, n = W.mine_to_utm(h["mx"], h["my"])
            hole, bench, east, north = hole_ids[int(r["hole"])], str(int(h["bench"])), "%.3f" % e, "%.3f" % n
        else:
            hole, bench, east, north = "", "", "", ""
        ppb = r["au"] * 1000.0
        grav = ""
        if ppb < 5:
            au = "<5"
        elif ppb > 10000:
            au = ">10000"
            grav = "%.2f" % r["au"]
        else:
            au = "%d" % int(round(ppb))
        crm = ""
        if kind == "CRM":
            c = [c_ for c_ in O.CRMS if c_[0] == r["crm"]][0]
            crm = c[3] if legacy else c[0]
        rows.append([sid, job, stype, hole, bench, east, north, fmt(r["drilled"]), fmt(r["received"]),
                     fmt(r["reported"]), au, grav, crm, "LEGACY-LIMS" if legacy else "LIMS"])
    write_csv(os.path.join(out, F_LIMS),
              ["SAMPLE_ID", "LAB_JOB", "SAMPLE_TYPE", "HOLE_ID", "BENCH", "EASTING_UTM17", "NORTHING_UTM17",
               "DATE_DRILLED", "DATE_RECEIVED", "DATE_REPORTED", "AU_PPB", "AU_GRAV_GPT", "CRM_ID", "SOURCE_SYSTEM"],
              rows)
    truth["lims_rows"] = len(rows)

    # grade control's block grades as the GC system computes them (primary assays, half detection limit)
    bh = lab[lab["kind"] == "BH"].copy()
    bh["au_rep"] = [0.0025 if a * 1000 < 5 else (round(a, 2) if a * 1000 > 10000 else round(a * 1000) / 1000.0)
                    for a in bh["au"]]
    bh["ijk"] = [int(hd.loc[int(h), "ijk"]) for h in bh["hole"]]
    gc_by_block = bh[bh["ijk"] >= 0].groupby("ijk")["au_rep"].mean()
    truth["gc_by_block"] = gc_by_block

    # ---------------- resource model ----------------
    rng = W._rng("modelmeta")
    mdl = df.sort_values(["k", "j", "i"])
    rows = []
    for _, b in mdl.iterrows():
        npass = int(rng.choice([1, 2, 3], p=[0.62, 0.30, 0.08]))
        nsamp = int(rng.integers(18, 33)) if npass == 1 else (int(rng.integers(10, 22)) if npass == 2 else
                                                              int(rng.integers(4, 12)))
        rows.append([int(b["ijk"]), "%.1f" % b["xc"], "%.1f" % b["yc"], "%.1f" % b["zc"], "10", "10", "5", "MZ",
                     b["rock"], "%.2f" % b["density"], "%.3f" % b["model"], npass, nsamp])
    write_csv(os.path.join(out, F_MODEL),
              ["IJK", "XC", "YC", "ZC", "DX", "DY", "DZ", "DOMAIN", "ROCK", "DENSITY", "AU_OK", "PASS", "NSAMP"], rows,
              preamble=["# KELVANNA LAKE MINE  MAIN ZONE RESOURCE MODEL 2026R",
                        "# Estimate AU_OK: ordinary kriging, 1.5 m composites, top cut 25 g/t; parent blocks 10 x 10 x 5,"
                        " no sub-blocks",
                        "# Coordinate system: KELVANNA MINE GRID",
                        "# Export: domain MZ only; 2026-03-18 B.Peck"], lineterminator="\n")

    # ---------------- survey depletion ----------------
    hist = df[df["period"] == "HIST"].copy()
    rows = []
    for _, b in hist.sort_values(["month_idx", "bench", "ijk"]).iterrows():
        m = W.month_start(int(b["month_idx"]))
        rows.append([int(b["ijk"]), int(b["bench"]), m.strftime("%Y-%m"), "EOM%s" % m.strftime("%y%m")])
    write_csv(os.path.join(out, F_DEPL), ["IJK", "BENCH", "MONTH", "SURVEY"], rows)

    # ---------------- 2027 plan ----------------
    plan = plan_scope(df)
    truth["plan"] = plan
    _write_plan(os.path.join(out, F_PLAN), plan)

    # ---------------- mill, gold room, refinery ----------------
    stops, outages = O.ball_mill_stops()
    mm = O.mill_months(hist, gc_by_block)
    md = O.mill_daily(mm, stops)
    truth["mill_daily"] = md
    rows = [[d.isoformat(), "%.0f" % r_wet, "%.1f" % mo, "%.3f" % h, "%.3f" % tl]
            for d, r_wet, mo, h, tl in zip(md["day"], md["wet_t"], md["moist"], md["head"], md["tails"])]
    write_csv(os.path.join(out, F_MILL), ["PROD_DAY_0600", "WET_TONNES", "H2O_PCT", "HEAD_AU_GPT", "TAILS_AU_GPT"],
              rows)
    bars, ships, lots, pieces = O.gold_room(md)
    truth["bars"], truth["lots"], truth["pieces"] = bars, lots, pieces
    _write_goldroom(out, bars, ships, lots, pieces)

    # ---------------- dispatch, fleet, inventory ----------------
    loads = O.lg_loads(hist, gc_by_block)
    truth["loads"] = loads
    open_t = _opening(loads)
    truth["lgsp_open_t"] = open_t
    _write_dispatch(out, loads)
    _write_fleet(os.path.join(out, F_FLEET))
    write_csv(os.path.join(out, F_INV), ["STOCKPILE", "TONNES", "AU_GPT", "CONTAINED_OZ", "BASIS"],
              [["ROM PAD", "61,880", "1.06", "2,109", "2022 year-end survey, grade by dispatch"],
               ["LGSP (low-grade stockpile)", "%s" % format(open_t, ","), "%.2f" % P.LGSP_OPEN_G,
                format(int(round(open_t * P.LGSP_OPEN_G / P.TROY)), ","), "2022 year-end survey, grade by dispatch"],
               ["MW DUMP (mineralised waste)", "3,412,960", "0.19", "20,849", "2022 year-end survey"]])

    # ---------------- DCS and CMMS ----------------
    truth["stops"], truth["outages"] = stops, outages
    _write_dcs(os.path.join(out, F_DCS), stops, outages)
    _write_cmms(os.path.join(out, F_CMMS), stops)

    # ---------------- documents ----------------
    docs.grid_control(os.path.join(out, F_GRID))
    docs.budget_basis(os.path.join(out, F_BASIS), F_PLAN)
    recon = docs.reconciliation_table(df, gc_by_block, md)
    truth["recon"] = recon
    docs.reconciliation_pdf(os.path.join(out, F_RECON), recon)
    docs.slope_review(os.path.join(out, F_GEOT))
    docs.price_deck(os.path.join(out, F_PRICE))
    _write_exploration(os.path.join(out, F_EXPL), df)

    for f in os.listdir(out):
        set_mtime(os.path.join(out, f))
    truth["blocks"] = df
    truth["holes"] = hd
    truth["lab"] = lab
    return truth


# ---------------------------------------------------------------------------------------------------------------

STOCK_ENDS = (dt.datetime(2024, 1, 1), dt.datetime(2025, 1, 1), dt.datetime(2026, 1, 1), dt.datetime(2026, 11, 1))


def stock_truth(loads, open_t):
    out = []
    for end in STOCK_ENDS:
        s = loads[loads["time_local"] < end]
        t = open_t + s["payload"].sum()
        au = (open_t * P.LGSP_OPEN_G + (s["payload"] * s["grade"]).sum()) / P.TROY
        out.append((t, au))
    return out


def _opening(loads):
    """The 2022 year-end survey tonnage of the low-grade stockpile, the first candidate that keeps every year-end
    figure clear of its rounding line."""
    for k in range(200):
        t0 = P.LGSP_OPEN_T + 137 * k
        ok = all(80 <= abs((t % 1000) - 500) and 8 <= abs((au % 100) - 50) for t, au in stock_truth(loads, t0))
        if ok:
            return t0
    raise AssertionError("no opening tonnage clears the rounding lines")


def _hole_ids(hd):
    """Hole ids as the drill-and-blast system numbers them: bench, pattern (one per bench and drilling week), hole."""
    ids = {}
    key = hd["bench"].astype(str) + "|" + hd["drilled"].map(lambda d: "%d-%02d" % d.isocalendar()[:2])
    pat_no = {}
    n = 400
    rg = W._rng("patterns")
    for k in sorted(set(key), key=lambda s: (s.split("|")[1], -int(s.split("|")[0]))):
        n += int(rg.integers(1, 5))
        pat_no[k] = n
    counter = {}
    for idx, k in zip(hd.index, key):
        counter[k] = counter.get(k, 0) + 1
        b = k.split("|")[0]
        ids[idx] = "%s-%04d-%03d" % (b, pat_no[k], counter[k])
    return ids


def _write_plan(path, plan):
    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"
    months = ["Jan-27", "Feb-27", "Mar-27", "Apr-27", "May-27", "Jun-27", "Jul-27", "Aug-27", "Sep-27", "Oct-27",
              "Nov-27", "Dec-27"]
    ws.append(["Kelvanna Lake Mine - 2027 mine plan v3 (resource model 2026R, ore at 0.90 g/t)"])
    ws.append(["Month", "Main Zone t", "Ore t", "Ore Au g/t", "Ore Au oz", "Low grade t (0.50-0.90)",
               "Mineralised waste t (0.30-0.50)", "Waste t (<0.30)"])
    for c in ws[2]:
        c.font = Font(bold=True)
    tot = np.zeros(6)
    for mi, mname in enumerate(months, start=1):
        g = plan[plan["plan_month"] == mi]
        t = g["tonnes"]
        ore = g["model"] >= P.NEW_ORE_CUT
        lg = (g["model"] >= P.OLD_ORE_CUT) & ~ore
        mw = (g["model"] >= P.LG_LOW_CUT) & (g["model"] < P.OLD_ORE_CUT)
        wst = g["model"] < P.LG_LOW_CUT
        ore_t, ore_au = t[ore].sum(), (t * g["model"])[ore].sum()
        row = [mname, round(t.sum()), round(ore_t), round(ore_au / ore_t, 2) if ore_t else 0,
               round(ore_au / P.TROY), round(t[lg].sum()), round(t[mw].sum()), round(t[wst].sum())]
        ws.append(row)
        tot += np.array([t.sum(), ore_t, ore_au, t[lg].sum(), t[mw].sum(), t[wst].sum()])
    ws.append(["2027", round(tot[0]), round(tot[1]), round(tot[2] / tot[1], 2), round(tot[2] / P.TROY),
               round(tot[3]), round(tot[4]), round(tot[5])])
    for c in ws[ws.max_row]:
        c.font = Font(bold=True)
    ws.column_dimensions["A"].width = 12
    for col in "BCDEFGH":
        ws.column_dimensions[col].width = 16
    sc = wb.create_sheet("Schedule")
    sc.append(["MONTH", "PHASE", "BENCH", "IJK", "XC", "YC", "ZC", "AU_OK", "TONNES", "DEST"])
    for c in sc[1]:
        c.font = Font(bold=True)
    for _, b in plan.iterrows():
        dest = "ORE" if b["model"] >= P.NEW_ORE_CUT else ("LG" if b["model"] >= P.OLD_ORE_CUT else
                                                         ("MW" if b["model"] >= P.LG_LOW_CUT else "WASTE"))
        phase = "P5" if b["xc"] < P.X0 + 640 else "P6"
        sc.append([months[int(b["plan_month"]) - 1], phase, int(b["bench"]), int(b["ijk"]), round(b["xc"], 1),
                   round(b["yc"], 1), round(b["zc"], 1), round(float(b["model"]), 3), round(float(b["tonnes"]), 0),
                   dest])
    asm = wb.create_sheet("Assumptions")
    for r in [["Item", "Value", "Source"],
              ["Ore cut-off (g/t Au)", 0.90, "Board approval 27 Oct 2026"],
              ["Low-grade stockpile band (g/t Au)", "0.50 to 0.90", "Board approval 27 Oct 2026"],
              ["Mineralised waste band (g/t Au)", "0.30 to 0.50", "Waste management plan rev 4"],
              ["Mill throughput target (dry t/day)", 7600, "Mill budget 2027"],
              ["Mill availability (%)", 92.0, "Mill budget 2027"],
              ["Mining rate, Main Zone (t/month)", "1.15 to 1.30 M", "Fleet plan 2027"],
              ["Block model", "2026R (AU_OK)", "Geology, March 2026"],
              ["Prepared", "9 Nov 2026", "J. Russell"]]:
        asm.append(r)
    for c in asm[1]:
        c.font = Font(bold=True)
    asm.column_dimensions["A"].width = 38
    asm.column_dimensions["B"].width = 16
    asm.column_dimensions["C"].width = 30
    save_xlsx(wb, path, "2027 mine plan v3", "Jeffrey Russell", "2026-11-09T21:12:00Z")


def _write_goldroom(out, bars, ships, lots, pieces):
    ship_name = {s: "SH-%s-%03d" % (str(d.year)[2:], k) for k, (s, d) in enumerate(zip(ships["ship"], ships["date"]), start=1)}
    rows = []
    for _, b in bars.sort_values(["pour_day", "pour_time"]).iterrows():
        rows.append(["%s-%04d" % (str(b["year"])[2:], b["seq"]), b["pour_day"].isoformat(), b["pour_time"].strftime("%H:%M"),
                     "%.2f" % b["gross"], ship_name[int(b["ship"])]])
    write_csv(os.path.join(out, F_BARS), ["BAR_NO", "POUR_DATE", "POUR_TIME", "GROSS_OZT", "SHIPMENT"], rows)
    lt = lots.set_index("lot")
    rng = W._rng("outturn")
    stmt_no = {}
    rows = []
    lot_name = {}
    for lot_id in sorted(lt.index, key=lambda x: (lt.loc[x, "received"], x)):
        L = lt.loc[lot_id]
        lot_name[lot_id] = "L%s%05d" % (str(L["received"].year)[2:], 11000 + len(lot_name) + 1)
    for _, pce in pieces.iterrows():
        L = lt.loc[int(pce["lot"])]
        b = bars.loc[int(pce["bar"])]
        st = L["settled"]
        if st > REFINERY_PULL:
            continue                       # not yet settled when the statements were pulled
        if st not in stmt_no:
            stmt_no[st] = None
        rows.append([st, lot_name[int(pce["lot"])], "KL %d" % b["seq"], L["received"].isoformat(), "%.3f" % L["gross_rec"],
                     "%.1f" % (L["fineness"] * 1000.0), "%.3f" % L["fine"], "%.3f" % L["ag"]])
    for k, st in enumerate(sorted(stmt_no)):
        stmt_no[st] = "RS-%d" % (40812 + k * 3 + int(rng.integers(0, 3)))
    rows = [[stmt_no[r[0]], r[0].isoformat()] + r[1:] for r in rows]
    rows.sort(key=lambda r: (r[1], r[2], r[3]))
    write_csv(os.path.join(out, F_REF), ["STATEMENT_NO", "STATEMENT_DATE", "LOT_NO", "CLIENT_REF", "RECEIVED_DATE",
                                         "LOT_GROSS_RECEIVED_OZT", "LOT_AU_FINENESS", "LOT_FINE_AU_OZT",
                                         "LOT_FINE_AG_OZT"], rows)


def _write_dispatch(out, loads):
    rng = W._rng("phantom")
    recs = []
    for _, l in loads.iterrows():
        recs.append((l["time_utc"], l, False))
        if rng.random() < P.PHANTOM_RATE:
            recs.append((l["time_utc"] + dt.timedelta(seconds=int(rng.integers(60, 360))), l, True))
    recs.sort(key=lambda x: (x[0], x[1]["truck"]))
    rows = []
    lid = 2_310_000
    for n, (t, l, ph) in enumerate(recs):
        u = t
        lid += int(rng.integers(3, 19))
        rows.append(["%07d" % lid, u.strftime("%Y-%m-%dT%H:%M:%SZ"), l["truck"],
                     l["shovel"], l["poly"], "LGSP", "LG", "%.2f" % l["grade"]])
    write_csv(os.path.join(out, F_DISP), ["LOAD_ID", "TIME_UTC", "TRUCK", "LOADER", "SOURCE", "DESTINATION",
                                          "MATERIAL", "SOURCE_AU_GPT"], rows)


def _write_fleet(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Fleet"
    ws.append(["UNIT", "MAKE_MODEL", "SERIAL", "NOMINAL_PAYLOAD_T", "IN_SERVICE", "STATUS"])
    serials = {"T-%02d" % i: "TWM%05d" % (1200 + i * 37) for i in range(1, 13)}
    new_ser = {"T-04": "LAJ01822", "T-09": "LAJ01907", "T-13": "LAJ02044", "T-14": "LAJ02051"}
    for i in range(1, 15):
        no = "T-%02d" % i
        if no in new_ser:
            ins = {"T-04": dt.date(2024, 5, 21), "T-09": dt.date(2024, 8, 19), "T-13": dt.date(2025, 2, 10),
                   "T-14": dt.date(2025, 2, 24)}[no]
            ws.append([no, O.NEW_MODEL, new_ser[no], O.NEW_PAYLOAD, ins, "ACTIVE"])
        else:
            ws.append([no, "CAT 777G", serials[no], 90.7, dt.date(2019, 6, 3) if i <= 8 else dt.date(2020, 4, 14),
                       "ACTIVE"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for row in ws.iter_rows(min_row=2, min_col=5, max_col=5):
        for c in row:
            c.number_format = "yyyy-mm-dd"
    dsp = wb.create_sheet("Disposals")
    dsp.append(["UNIT", "MAKE_MODEL", "SERIAL", "NOMINAL_PAYLOAD_T", "IN_SERVICE", "DISPOSED", "DISPOSAL_REF"])
    dsp.append(["T-04", "CAT 777G", serials["T-04"], 90.7, dt.date(2019, 6, 3), dt.date(2024, 5, 6), "AD-2024-017"])
    dsp.append(["T-09", "CAT 777G", serials["T-09"], 90.7, dt.date(2020, 4, 14), dt.date(2024, 8, 2), "AD-2024-031"])
    dsp.append(["LV-22", "Toyota Hilux", "MR0HA3CD5K0118", "", dt.date(2018, 2, 1), dt.date(2025, 1, 15),
                "AD-2025-002"])
    for c in dsp[1]:
        c.font = Font(bold=True)
    for row in dsp.iter_rows(min_row=2, min_col=5, max_col=6):
        for c in row:
            c.number_format = "yyyy-mm-dd"
    for s in (ws, dsp):
        for col, wdt in zip("ABCDEFG", (8, 14, 14, 20, 12, 12, 14)):
            s.column_dimensions[col].width = wdt
    save_xlsx(wb, path, "Haul fleet register", "Emily Schmitt", "2026-10-30T13:05:00Z")


def _write_dcs(path, stops, outages):
    """Ball mill and SAG mill run states and the cyclone feed pumps' duty changes, as the historian stored them."""
    rng = W._rng("dcsrender")
    t0 = dt.datetime(2025, 1, 1, 5, 0)        # export window, UTC
    t1 = dt.datetime(2026, 11, 1, 4, 0)

    switch = outages[O.TAG_SWITCH_OUTAGE][1]

    def tag(old, new, t):
        return old if t < switch else new
    TAGS = {"BM": ("BM101.RUNNING", "GRD.BM01.RUN_STS", "Ball mill 101 running", "Ball mill 1 run status"),
            "SAG": ("SAG101.RUNNING", "GRD.SAG01.RUN_STS", "SAG mill 101 running", "SAG mill 1 run status"),
            "PA": ("PP301A.RUNNING", "GRD.CYC_PP01A.RUN_STS", "Cyclone feed pump 301A running",
                   "Cyclone feed pump 1A run status"),
            "PB": ("PP301B.RUNNING", "GRD.CYC_PP01B.RUN_STS", "Cyclone feed pump 301B running",
                   "Cyclone feed pump 1B run status")}
    ev = []
    s = stops.copy()
    s["su"] = [O.local_to_utc(x) for x in s["start"]]
    s["eu"] = [O.local_to_utc(x) for x in s["end"]]
    s = s[(s["eu"] > t0) & (s["su"] < t1)]
    for _, r in s.iterrows():
        ev.append((r["su"], "BM", 0))
        ev.append((r["eu"], "BM", 1))
        ev.append((r["su"] - dt.timedelta(seconds=int(rng.integers(20, 240))), "SAG", 0))
        ev.append((r["eu"] - dt.timedelta(seconds=int(rng.integers(300, 900))), "SAG", 1))
    # pump duty swaps every 6 to 11 hours while the circuit runs
    t = t0 + dt.timedelta(hours=3)
    duty = "PA"
    while t < t1:
        other = "PB" if duty == "PA" else "PA"
        ev.append((t, other, 1))
        ev.append((t + dt.timedelta(seconds=int(rng.integers(30, 150))), duty, 0))
        duty = other
        t += dt.timedelta(hours=float(rng.uniform(6, 11)))
    rows = []
    bm0 = 0 if ((s["su"] <= t0) & (s["eu"] > t0)).any() else 1
    state = {"BM": bm0, "SAG": bm0, "PA": 1, "PB": 0}
    for k in ("BM", "SAG", "PA", "PB"):
        rows.append((t0, TAGS[k][0], TAGS[k][2], state[k], "INITIAL"))
    for t, k, v in sorted(ev, key=lambda x: x[0]):
        if not (t0 < t < t1):
            continue
        if t >= switch and "switched" not in state:
            state["switched"] = True
            for kk in ("BM", "SAG", "PA", "PB"):
                rows.append((switch, TAGS[kk][1], TAGS[kk][3], state[kk], "INITIAL"))
        state[k] = v
        if any(a <= t <= b for a, b in outages):
            continue
        old, new = TAGS[k][0], TAGS[k][1]
        rows.append((t, tag(old, new, t), TAGS[k][2] if t < switch else TAGS[k][3], v, "GOOD"))
    # the historian re-sends a few events after collector restarts
    dup = [r for r in rows if r[4] == "GOOD" and rng.random() < 0.006]
    rows += dup
    rows.sort(key=lambda r: (r[0], r[1]))
    write_csv(path, ["TAG", "DESCRIPTION", "TIME_UTC", "VALUE", "QUALITY"],
              [[r[1], r[2], r[0].strftime("%Y-%m-%d %H:%M:%S"), r[3], r[4]] for r in rows])


def _write_cmms(path, stops):
    rng = W._rng("cmms")
    rows = []
    n = 0
    wo_rng = W._rng("wonumbers")
    s = stops[(stops["end"] > dt.datetime(2025, 1, 1)) & (stops["start"] < dt.datetime(2026, 11, 1))]
    for _, r in s.iterrows():
        if r["kind"] in ("SHUTDOWN", "RELINE"):
            n += 1
            desc = ("BM-101 liner change and mill shutdown" if r["kind"] == "RELINE" else
                    "Grinding circuit planned shutdown - BM-101 isolated")
            # the crew's isolation runs from a few minutes after the mill stops to a few minutes before it starts
            rows.append([r["start"], "WO-%d" % 0, "BM-101", "GRD-BM", "SD", desc, r["iso_start"], r["iso_end"],
                         "CLOSED"])
        elif rng.random() < 0.45:
            n += 1
            a = r["start"] + dt.timedelta(minutes=int(rng.integers(8, 35)))
            b = r["end"] - dt.timedelta(minutes=int(rng.integers(2, 12)))
            if b <= a:
                b = a + dt.timedelta(minutes=5)
            desc = rng.choice(["BM-101 trip - lube oil pressure low", "BM-101 trip - motor overload",
                               "BM-101 trip - mill discharge chute blocked", "BM-101 trip - trunnion bearing temp"])
            rows.append([r["start"], "WO-%d" % 0, "BM-101", "GRD-BM", "CM", str(desc), a, b,
                         "CLOSED"])
    # weekly lube routes and inspections done with the mill running
    d = dt.datetime(2025, 1, 7, 9, 0)
    while d < dt.datetime(2026, 10, 31):
        n += 1
        rows.append([d, "WO-%d" % 0, "BM-101", "GRD-BM", "PM",
                     "Weekly lube route and walk-down (mill running)", d, d + dt.timedelta(minutes=int(rng.integers(50, 110))),
                     "CLOSED"])
        d += dt.timedelta(days=7, minutes=int(rng.integers(-90, 90)))
    rows.sort(key=lambda x: x[0])
    wo = 250_870
    for r in rows:
        wo += int(wo_rng.integers(6, 41))
        r[1] = "WO-%d" % wo
    write_csv(path, ["WONUM", "ASSETNUM", "LOCATION", "WORKTYPE", "DESCRIPTION", "ACTSTART",
                     "ACTFINISH", "STATUS"],
              [[r[1], r[2], r[3], r[4], r[5], r[6].strftime("%Y-%m-%d %H:%M"), r[7].strftime("%Y-%m-%d %H:%M"), r[8]]
               for r in rows])


def _write_exploration(path, df):
    rng = W._rng("expl")
    rows = []
    for h in range(1, 91):
        x = P.X0 + rng.uniform(60, 1060)
        y = P.Y0 + rng.uniform(160, 420)
        e, n = W.mine_to_utm(x, y)
        hole = "KL%02d-%03d" % (19 + (h - 1) // 23, 100 + h * 3)
        depth = rng.uniform(140, 320)
        frm = 0.0
        while frm < depth:
            to = round(frm + 1.5, 1)
            au = float(np.exp(rng.normal(math.log(0.12), 1.4)))
            rows.append([hole, "%.2f" % e, "%.2f" % n, "%.1f" % (310 + rng.normal(0, 1.5)), "%.1f" % frm, "%.1f" % to,
                         "%.3f" % au if au >= 0.005 else "<0.005", "FA-AAS"])
            frm = to
    write_csv(path, ["HOLE_ID", "COLLAR_E", "COLLAR_N", "COLLAR_ELEV", "FROM_M", "TO_M", "AU_GPT", "METHOD"], rows)
