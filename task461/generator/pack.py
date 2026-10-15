"""Write the data files of the pack: MPI's day-ahead price archive for the North Hub (2019 onward, the operator's
date and hour formats changing with its 2022 archive) and for Redrock Draw's node, the settlement point list, the hub's
2026 real-time prices and the 2026 ancillary service clearing prices, Cordell's BMS hourly export, the revenue meter's
fifteen-minute data and the day-ahead settlement statement lines."""
import csv
import datetime as dt
import io

import numpy as np

import market as MK
import ops as O
import world as W


def write_csv(path, cols, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(cols)
    n = 0
    for r in rows:
        w.writerow(r)
        n += 1
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write(buf.getvalue())
    return n


def money(x):
    return "%.2f" % x


# ------------------------------------------------------------------------------------------------ day-ahead prices
PRICE_COLS = ["DeliveryDate", "HourEnding", "RepeatedHourFlag", "SettlementPoint", "SettlementPointPrice"]


def _fmt_hour(d, hr):
    he, rep = hr[0], hr[1]
    if d.year < 2022:
        return d.strftime("%m/%d/%Y"), "%02d:00" % he, "Y" if rep else "N"
    return d.isoformat(), str(he), "true" if rep else "false"


def hub_rows(days):
    for x in days:
        d = x["day"]
        for hr, p in zip(x["hours"], x["hub"]):
            a, b, c = _fmt_hour(d, hr)
            yield [a, b, c, W.HUB, money(p)]


def node_rows(days):
    for x in days:
        d = x["day"]
        if d < W.NODE_CREATED:
            continue
        name = W.NODE if d >= W.NODE_RENAME else W.NODE_OLD
        for hr, p in zip(x["hours"], x["node_pub"]):
            a, b, c = _fmt_hour(d, hr)
            yield [a, b, c, name, money(p)]


POINT_COLS = ["settlement_point", "point_type", "zone", "first_operating_day", "last_operating_day", "predecessor",
              "note"]


def point_rows():
    rows = [
        ["MP_HUB_AVG", "HUB", "SYSTEM", "2016-04-01", "", "", "Simple average of the four zone hubs"],
        ["MP_NORTH_HUB", "HUB", "NORTH", "2016-04-01", "", "", "Trading hub: average of the North zone's hub buses"],
        ["MP_SOUTH_HUB", "HUB", "SOUTH", "2016-04-01", "", "", "Trading hub: average of the South zone's hub buses"],
        ["MP_WEST_HUB", "HUB", "WEST", "2016-04-01", "", "", "Trading hub: average of the West zone's hub buses"],
        ["MP_CENTRAL_HUB", "HUB", "CENTRAL", "2018-06-01", "", "", "Trading hub: average of the Central zone's hub buses"],
        ["LZ_NORTH", "LZ", "NORTH", "2016-04-01", "", "", "Load zone"],
        ["LZ_SOUTH", "LZ", "SOUTH", "2016-04-01", "", "", "Load zone"],
        ["LZ_WEST", "LZ", "WEST", "2016-04-01", "", "", "Load zone"],
        ["LZ_CENTRAL", "LZ", "CENTRAL", "2018-06-01", "", "", "Load zone"],
        ["ASHMORE_CC1_RN", "RN", "NORTH", "2016-04-01", "", "", ""],
        ["BLUESTEM_WND_RN", "RN", "NORTH", "2019-08-14", "", "", ""],
        ["CALLOWAY_SLR_RN", "RN", "NORTH", "2023-05-09", "", "", ""],
        ["DENHOLM_GT_RN", "RN", "NORTH", "2016-04-01", "", "", ""],
        ["FAIRLEA_ESS_RN", "RN", "WEST", "2018-10-16", "", "", ""],
        ["GRANBY_WND2_RN", "RN", "WEST", "2021-10-05", "", "", ""],
        ["HOLLISTER_SLR_RN", "RN", "SOUTH", "2022-03-15", "", "", ""],
        ["KITTERING_CC_RN", "RN", "CENTRAL", "2018-06-01", "", "", ""],
        ["MARLOWE_ESS_RN", "RN", "NORTH", "2017-08-29", "", "", ""],
        ["OXBOW_WND_RN", "RN", "NORTH", "2020-11-17", "2025-05-31", "", "Retired with the unit"],
        ["OXBOW_WND_RN2", "RN", "NORTH", "2025-06-01", "", "OXBOW_WND_RN", "Repowered unit"],
        [W.NODE_OLD, "RN", "NORTH", W.NODE_CREATED.isoformat(), (W.NODE_RENAME - dt.timedelta(days=1)).isoformat(), "",
         "Priced at %s through operating day %s (resource not yet in the network model)" % (
             W.HUB, (W.NODE_PROVISIONAL_END - dt.timedelta(days=1)).isoformat())],
        [W.NODE, "RN", "NORTH", W.NODE_RENAME.isoformat(), "", W.NODE_OLD, "NMU-2026-03 rename"],
        ["SPRUCEDALE_ESS_RN", "RN", "SOUTH", "2018-03-20", "", "", ""],
        ["TALLMADGE_GT_RN", "RN", "SOUTH", "2016-04-01", "", "", ""],
        ["WYNDHAM_SLR_RN", "RN", "WEST", "2024-07-30", "", "", ""],
    ]
    return rows


# ---------------------------------------------------------------------------------------------- the distractors
RT_COLS = ["DeliveryDate", "DeliveryHour", "DeliveryInterval", "RepeatedHourFlag", "SettlementPointName",
           "SettlementPointType", "SettlementPointPrice"]


def rt_rows(rt):
    for d, hr, q, p in rt:
        yield [d.isoformat(), str(hr[0]), str(q), "true" if hr[1] else "false", W.HUB, "HU", money(p)]


AS_COLS = ["DeliveryDate", "HourEnding", "RepeatedHourFlag", "AncillaryType", "MCPC"]


def as_rows(asp):
    for d, hr, ru, rd, rrs, ns in asp:
        for code, v in (("REGUP", ru), ("REGDN", rd), ("RRS", rrs), ("NSPIN", ns)):
            yield [d.isoformat(), str(hr[0]), "true" if hr[1] else "false", code, money(v)]


# ------------------------------------------------------------------------------------------------- the BMS export
BMS_COLS = ["interval_start_utc", "site_id", "operating_mode", "dc_charge_kwh", "dc_discharge_kwh", "pcs_ac_charge_kwh",
            "pcs_ac_discharge_kwh", "soc_pct", "avg_cell_temperature_c"]


def cell_temp(phys, seed=W.SEED + 31):
    rng = np.random.default_rng(seed)
    n = O.H
    doy = np.array([(O.UTC0 + dt.timedelta(hours=k)).timetuple().tm_yday for k in range(n)])
    hour = np.array([(O.UTC0 + dt.timedelta(hours=k)).hour for k in range(n)])
    base = 23.4 + 2.6 * np.cos(2 * np.pi * (doy - 205) / 365) + 0.6 * np.cos(2 * np.pi * (hour - 21) / 24)
    work = (phys["dc_chg"] + phys["dc_dis"]) / 100.0
    heat = np.zeros(n)
    for k in range(n):
        heat[k] = (heat[k - 1] * 0.55 if k else 0.0) + 2.1 * work[k]
    return base + heat + MK.ar1(rng, n, 0.7, 0.12)


def bms_rows(view, temp):
    t0 = O.UTC0
    held = None
    for k in range(O.H):
        t = t0 + dt.timedelta(hours=k)
        tc = temp[k]
        if view["lost"][k]:
            tc = held
        else:
            held = tc
        yield [t.strftime("%Y-%m-%dT%H:%M:%SZ"), "RDRW-BESS-01", view["mode"][k],
               "%d" % round(view["dc_chg"][k] * 1000), "%d" % round(view["dc_dis"][k] * 1000),
               "%d" % round(view["ac_chg"][k] * 1000), "%d" % round(view["ac_dis"][k] * 1000),
               "%.1f" % view["soc"][k], "%.1f" % tc]


# ----------------------------------------------------------------------------------------------- the revenue meter
METER_COLS = ["meter_id", "interval_ending_utc", "mwh_delivered", "mwh_received"]


def meter_quarters(phys):
    """Each UTC hour's delivered and received energy split into its four fifteen-minute intervals: discharge and
    charge at constant power through the hour (a capacity test's short last hour falls in its first minutes), the
    station load evenly."""
    out = []
    for k in range(O.H):
        dl, rc = phys["delivered"][k], phys["received"][k]
        aux = phys["aux"][k]
        frac = phys["dc_dis"][k] / 100.0 if 0 < phys["dc_dis"][k] < 99.0 and phys["test_dis"][k] > 0 else 1.0
        if frac < 1.0:
            # the battery delivers at full power for `frac` of the hour, then the station load returns
            q_on = [min(1.0, max(0.0, frac * 4 - i)) for i in range(4)]
            gross = phys["ac_dis"][k]
            dq = [gross * q / max(frac * 4, 1e-9) - aux / 4.0 * q for q in q_on]
            rq = [aux / 4.0 * (1 - q) for q in q_on]
            out.append((dq, rq))
        else:
            out.append(([dl / 4.0] * 4, [rc / 4.0] * 4))
    return out


METER_END = dt.datetime(2026, 11, 2, 6, 0)          # posted for operating days to 1 November (UTC end, CST)


def meter_rows(phys):
    t0 = O.UTC0
    for k, (dq, rq) in enumerate(meter_quarters(phys)):
        for i in range(4):
            t = t0 + dt.timedelta(hours=k, minutes=15 * (i + 1))
            if t > METER_END:
                return
            yield ["RDRW-POI-M1", t.strftime("%Y-%m-%dT%H:%M:%SZ"), "%.3f" % max(dq[i], 0.0), "%.3f" % max(rq[i], 0.0)]


# ------------------------------------------------------------------------------------ the settlement statement lines
SETTLE_COLS = ["statement_id", "statement_type", "issue_date", "operating_date", "hour_ending", "repeated_hour",
               "qse", "resource", "settlement_point", "charge_type", "bill_determinant_mwh", "price_usd_per_mwh",
               "amount_usd"]


def settle_rows(lines):
    order = {"DAEP": 0, "DAES": 1, "DAAF": 2}
    for r in sorted(lines, key=lambda r: (r["issue_date"], r["operating_date"], r["statement_type"], r["hour_ending"],
                                           r["repeated_hour"], order[r["charge_type"]])):
        yield [r["statement_id"], r["statement_type"], r["issue_date"].isoformat(), r["operating_date"].isoformat(),
               str(r["hour_ending"]), "Y" if r["repeated_hour"] else "N", "BARROWFIELD", r["resource"],
               r["settlement_point"], r["charge_type"], "%.1f" % r["mwh"], "%.4f" % r["price"] if r["charge_type"] == "DAAF"
               else money(r["price"]), money(r["amount"])]
