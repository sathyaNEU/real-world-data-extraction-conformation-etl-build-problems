"""Writes the pack (target/) for task138 from the world's clean truth: the files the cooperative's systems, its
wholesale supplier and the airport weather feed would hand a planning engineer, each in its own system's layout."""
import os

import numpy as np
import openpyxl
import pandas as pd
from openpyxl.styles import Alignment, Font

import docs as D
import io_util as IO
import params as PR
import world as W

FILES = {
    "scada_old": "DUNRAITH_FDR_KW_2022-2023.csv",
    "scada_new": "dunraith_feeder_mw_2024-2026.csv",
    "wx": "mossford_ap_obs_2022-2026.csv",
    "criteria": "BEC_distribution_planning_criteria_rev4.pdf",
    "opplan": "BEC_2027_operating_plan.pdf",
    "testplan": "CVR_pilot_plan_Dunraith_2025.pdf",
    "reglog": "VR_event_log_DUN_2025.csv",
    "forecast": "BEC_load_forecast_2025.xlsx",
    "mdms": "mdms_xfmr_daily_kwh_20260601_20260930.csv",
    "so": "SO-2026-114_Dunraith.pdf",
    "register": "DUN_transformer_register_2026-10.xlsx",
    "mv90": "MV90_DP0417_202606-202609.csv",
    "dpsched": "WPC_Exhibit_A_delivery_points.pdf",
    "outages": "OMS_outage_events_2026.csv",
    "ties": "DUN_feeder_ties_2026.xlsx",
}

STATION = "MOSSFORD MUNI AP"


# ------------------------------------------------------------------ SCADA historian exports
def write_scada_old(path, ld):
    """The old historian (retired in spring 2024): one column a feeder, kW, each hour labelled at its end."""
    sub = ld[ld.local.dt.year.isin([2022, 2023])]
    piv = sub.pivot(index="local", columns="feeder", values="mw")
    rows = []
    for ts, r in piv.iterrows():
        end = ts + pd.Timedelta(hours=1)
        rows.append(["%d/%d/%d %d:%02d" % (end.month, end.day, end.year, end.hour, end.minute)] +
                    [int(round(float(r[f]) * 1000.0)) for f in PR.FEEDERS])
    hdr = ["Date/Time"] + ["DUNRAITH F%d KW" % (i + 1) for i in range(len(PR.FEEDERS))]
    return IO.write_csv(path, hdr, rows)


def scada_gaps():
    """Hours the new historian marks Bad (communication lost overnight, no value written)."""
    rng = np.random.default_rng(PR.OTHER_SEED + 2)
    out = set()
    for year in (2024, 2025, 2026):
        idx = W.summer_index(year)
        night = [ts for ts in idx if 1 <= ts.hour <= 4]
        for k in rng.choice(len(night), 5, replace=False):
            f = PR.FEEDERS[int(rng.integers(0, len(PR.FEEDERS)))]
            for j in range(int(rng.integers(1, 3))):
                out.add((f, night[int(k)] + pd.Timedelta(hours=j)))
    return out


def write_scada_new(path, ld):
    """The new historian: one row a point and hour, MW, each hour labelled at its start, local time."""
    sub = ld[ld.local.dt.year.isin([2024, 2025, 2026])].sort_values(["feeder", "local"])
    gaps = scada_gaps()
    rows = []
    for f, ts, mw in zip(sub.feeder.values, sub.local, sub.mw.values):
        tag = "%s.MW.H_AVG" % f
        if (f, ts) in gaps:
            rows.append([tag, ts.strftime("%Y-%m-%d %H:%M:%S"), "", "Bad"])
        else:
            rows.append([tag, ts.strftime("%Y-%m-%d %H:%M:%S"), "%.3f" % mw, "Good"])
    return IO.write_csv(path, ["TagName", "TimeStamp", "Value", "Quality"], rows)


# ------------------------------------------------------------------ airport observations
def obs_rows(wx):
    """Routine observations at 53 minutes past each hour and the specials issued between them, UTC, deg C."""
    rng = np.random.default_rng(PR.OTHER_SEED + 1)
    rows = []
    for year in PR.SUMMERS:
        s = wx[wx.local.dt.year == year].set_index("local")["temp_f"]
        idx, vals = s.index, s.values
        for k in range(len(idx)):
            nxt = vals[k + 1] if k + 1 < len(idx) else vals[k]
            t53 = vals[k] + (nxt - vals[k]) * 53.0 / 60.0
            ts = idx[k] + pd.Timedelta(minutes=53)
            spread = 8.0 + 6.0 * abs(np.sin(k / 37.0)) + rng.normal(0, 1.2)
            c = (t53 - 32.0) * 5.0 / 9.0
            dc = (t53 - spread - 32.0) * 5.0 / 9.0
            missing = (1 <= idx[k].hour <= 4) and rng.random() < 0.004
            rows.append((ts, "FM-15", None if missing else round(c, 1), None if missing else round(dc, 1)))
            if rng.random() < 0.035:
                # a special: a thunderstorm's outflow or a wind shift, cooler than the hour either side
                m = int(rng.integers(5, 50))
                low = min(vals[k], nxt) - abs(rng.normal(0.8, 0.6))
                rows.append((idx[k] + pd.Timedelta(minutes=m), "FM-16", round((low - 32.0) * 5.0 / 9.0, 1),
                             round((low - spread - 32.0) * 5.0 / 9.0, 1)))
    rows.sort(key=lambda r: r[0])
    return rows


def write_wx(path, wx):
    """The airport's observations as the climate data service exports them: local standard time all year."""
    out = []
    for ts, kind, c, dc in obs_rows(wx):
        lst = ts - pd.Timedelta(hours=1)
        out.append([STATION, lst.strftime("%Y-%m-%dT%H:%M:%S"), kind, "" if c is None else "%.1f" % c,
                    "" if dc is None else "%.1f" % dc])
    return IO.write_csv(path, ["STATION", "DATE_LST", "REPORT_TYPE", "DRY_BULB_C", "DEW_POINT_C"], out)


# ------------------------------------------------------------------ the pilot's regulator controller log
def write_reglog(path, log):
    rng = np.random.default_rng(PR.OTHER_SEED + 3)
    rows = []
    for f, ts, act in zip(log.feeder, log.local, log.action):
        late = ts.minute != 0 or ts.hour != 0
        if late:
            planned = ts.normalize()
            rows.append((planned, "%s VR" % f, "COMM FAIL", "", "SCADA"))
            rows.append((planned + pd.Timedelta(hours=6, minutes=12), "%s VR" % f, "COMM OK", "", "SCADA"))
        bc = "119.2" if act == "ON" else "123.5"
        rows.append((ts, "%s VR" % f, "CVR %s" % act, bc, "LOCAL" if late else "SCADA"))
    for (f, when) in W.MISSED:
        rows.append((pd.Timestamp(when), "%s VR" % f, "CMD NOT EXECUTED", "", "SCADA"))
    # the spring maintenance leaves every regulator at the normal setting, one crew visit at a time
    visit = pd.Timestamp("2025-05-12 08:40")
    for f in PR.FEEDERS:
        visit = visit + pd.Timedelta(minutes=int(rng.integers(26, 95)), seconds=int(rng.integers(0, 60)))
        if visit.hour >= 15:
            visit = visit.normalize() + pd.Timedelta(days=1, hours=8, minutes=int(rng.integers(5, 40)))
        rows.append((visit, "%s VR" % f, "BANDCENTER CONFIRMED", "123.5", "LOCAL"))
    # the other regulators' routine events over the same months
    t = pd.Timestamp("2025-05-20 08:00")
    while t < pd.Timestamp("2025-10-10"):
        t = t + pd.Timedelta(hours=float(rng.exponential(70)))
        f = PR.FEEDERS[int(rng.integers(0, len(PR.FEEDERS)))]
        ev = rng.choice(["TAP COUNTER RESET", "COMM FAIL", "BANDCENTER CONFIRMED", "DRAG HAND RESET",
                         "REVERSE POWER BLOCK"], p=[0.15, 0.25, 0.35, 0.15, 0.10])
        val = ""
        tt = t.round("s")
        if ev == "BANDCENTER CONFIRMED":
            val = "119.2" if W.cvr_state(log, f, pd.DatetimeIndex([tt]))[0] else "123.5"
        rows.append((tt, "%s VR" % f, str(ev), val, "SCADA"))
        if ev == "COMM FAIL":
            rows.append((tt + pd.Timedelta(minutes=int(rng.integers(4, 140))), "%s VR" % f, "COMM OK", "", "SCADA"))
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    out = [[ts.strftime("%Y-%m-%d %H:%M:%S"), dev, ev, val, src] for ts, dev, ev, val, src in rows]
    return IO.write_csv(path, ["EventTime", "Equipment", "Event", "Bandcenter_V", "Source"], out)


# ------------------------------------------------------------------ load forecast
def write_forecast(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "System"
    ws.append(["Year", "Energy purchases (MWh)", "Members (avg)", "Non-coincident peak (MW)"])
    e, m, p = 1418200.0, 21940, 331.0
    for y in range(2025, 2035):
        ws.append([y, round(e), round(m), round(p, 1)])
        e *= 1.0118
        m *= 1.0071
        p *= 1.0102
    ws2 = wb.create_sheet("Substations")
    ws2.append(["Substation", "Weather station", "Base case growth (%/yr)", "High case growth (%/yr)",
                "Low case growth (%/yr)", "Comment"])
    for r in (["Carrow Creek", "Mossford AP", 0.60, 1.10, 0.15, ""],
              ["Dunraith", "Mossford AP", 0.95, 1.55, 0.35, "east Mossford residential growth"],
              ["Lindell", "Harrow Co AP", 0.20, 0.55, -0.20, ""],
              ["Ostby", "Mossford AP", 1.30, 2.05, 0.60, "irrigation conversions"],
              ["Tessaly", "Harrow Co AP", 0.45, 0.90, 0.05, ""]):
        ws2.append(r)
    ws3 = wb.create_sheet("Assumptions")
    for r in (["Base year", "2024"],
              ["Cases", "Base: county population and housing starts per state demographer, 2024 series. High and "
                        "low: plus and minus one standard error of the housing-start model."],
              ["Growth rates", "Compound annual rates applied to each substation's own summer peak, 2025 to 2034."],
              ["Prepared by", "Hollis & Brandt Utility Consulting for Breckwater Electric Cooperative"],
              ["Board acceptance", "June 2025"]):
        ws3.append(r)
    for w_, widths in ((ws, (8, 24, 15, 24)), (ws2, (14, 16, 24, 24, 24, 34)), (ws3, (18, 110))):
        for c, wd in zip("ABCDEF", widths):
            w_.column_dimensions[c].width = wd
        for cell in w_[1]:
            cell.font = Font(bold=True)
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    IO.repack_ooxml(path, "Hollis & Brandt", "Julie Gibbs", "2025-03-27T14:05:00Z", "2025-06-24T19:41:00Z",
                    "BEC load forecast 2025", "Breckwater Electric Cooperative")


# ------------------------------------------------------------------ members' meters, the register, the supplier
def write_mdms(path, md, tx):
    """The meter data system's daily energy by transformer, the feeder as the GIS holds it on the day of export."""
    now = dict(zip(tx.tx, tx.feeder_now))
    md = md.sort_values(["tx", "date"]).reset_index(drop=True)
    rows = [[t, now[t], d.strftime("%m/%d/%Y"), "%.2f" % k]
            for t, d, k in zip(md.tx.values, md.date, md.kwh_held.values)]
    return IO.write_csv(path, ["XFMR_ID", "FEEDER", "READ_DATE", "KWH"], rows)


CLASS_NAME = {"R-1": "R-1 Residential", "GS-1": "GS-1 General service", "IR-1": "IR-1 Irrigation (secondary)",
              "LP-3": "LP-3 Large power, CT metered"}


def write_register(path, tx, dv):
    """The GIS export: transformers with their tap fuse and meter, and the protective devices as built, each with
    the feeder that energises it today and its normal state."""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Transformers"
    ws.append(["XFMR_ID", "FEEDER", "PROTECTIVE_DEVICE", "KVA", "PHASE", "RATE_CLASS", "METER_NO", "METER_MULT",
               "METER_SET"])
    for r in tx.sort_values("tx").itertuples():
        phase = "3PH" if r.kva >= 100 else "1PH"
        ws.append([r.tx, r.feeder_now, r.fuse, int(r.kva), phase, CLASS_NAME[r.cls], r.meter, int(r.mult),
                   r.meter_set.strftime("%Y-%m-%d")])
    for c, wd in zip("ABCDEFGHI", (10, 8, 12, 6, 7, 30, 11, 11, 11)):
        ws.column_dimensions[c].width = wd
    for cell in ws[1]:
        cell.font = Font(bold=True)
    ws.freeze_panes = "A2"
    wd_ = wb.create_sheet("Devices")
    wd_.append(["DEVICE_ID", "TYPE", "FEEDER", "UPSTREAM_DEVICE", "NORMAL_STATE"])
    moved_dev = {}
    for a, b in W.RECONFIG_PAIRS:
        for d in W.beyond(dv, W.MOVED_SWITCH[a]):
            moved_dev[d] = b
    for r in dv.itertuples():
        state = "Open" if r.device in W.MOVED_SWITCH.values() else "Closed"
        wd_.append([r.device, r.type, moved_dev.get(r.device, r.feeder_built), r.upstream, state])
    for c, wdt in zip("ABCDE", (11, 10, 8, 20, 14)):
        wd_.column_dimensions[c].width = wdt
    for cell in wd_[1]:
        cell.font = Font(bold=True)
    wd_.freeze_panes = "A2"
    wb.save(path)
    IO.repack_ooxml(path, "GIS export", "Bailey Becker", "2026-10-09T13:12:00Z", "2026-10-09T13:20:00Z",
                    "Dunraith transformer register", "Breckwater Electric Cooperative")


def write_mv90(path, gt):
    rng = np.random.default_rng(PR.GT_SEED + 5)
    rows = []
    for meter in ("41-2207", "41-2208", "41-2391"):
        g = gt[gt.meter == meter]
        est = set()
        if meter != "41-2391":
            # a recorder outage overnight, filled by the supplier's estimation
            start = int(rng.integers(5, 115)) * 96 + int(rng.integers(3, 12))
            est = set(range(start, start + int(rng.integers(3, 9))))
        for k, (ts, v) in enumerate(zip(g.end_utc, g.kwh.values)):
            rows.append([meter, "1", "KWH", ts.strftime("%Y-%m-%d %H:%M"), "%.1f" % v, "E" if k in est else ""])
    return IO.write_csv(path, ["RECORDER", "CHANNEL", "UOM", "INTERVAL_END_UTC", "VALUE", "STATUS"], rows)


# ------------------------------------------------------------------ distractors
def write_outages(path, ou):
    rows = [[n, s.strftime("%Y-%m-%d %H:%M"), f, c, m, k] for n, s, f, c, m, k in ou.itertuples(index=False)]
    return IO.write_csv(path, ["EVENT_NO", "START_LOCAL", "FEEDER", "CAUSE", "MINUTES", "MEMBERS_OUT"], rows)


def write_ties(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Ties"
    ws.append(["Tie switch", "From feeder", "To feeder", "Normally", "Conductor limit (A)",
               "Transferable at summer peak (MW)", "Last operated"])
    for r in (["TS-2207", "DUN-1", "CC-3 (Carrow Creek)", "Open", 530, 3.4, "2024-08-14"],
              ["TS-2231", "DUN-3", "OST-2 (Ostby)", "Open", 655, 4.1, "2025-07-30"],
              ["TS-2240", "DUN-5", "OST-4 (Ostby)", "Open", 340, 1.8, "2023-06-02"],
              ["TS-2258", "DUN-7", "CC-1 (Carrow Creek)", "Open", 530, 2.9, "2022-09-19"],
              ["TS-2263", "DUN-8", "LIN-2 (Lindell)", "Open", 230, 1.3, ""],
              ["TS-2269", "DUN-2", "CC-4 (Carrow Creek)", "Open", 340, 2.2, "2021-07-08"]):
        ws.append(r)
    for c, wd in zip("ABCDEFG", (11, 11, 20, 10, 18, 30, 13)):
        ws.column_dimensions[c].width = wd
    for cell in ws[1]:
        cell.font = Font(bold=True)
    wb.save(path)
    IO.repack_ooxml(path, "Julie Gibbs", "Julie Gibbs", "2026-08-03T15:30:00Z", "2026-08-03T16:02:00Z",
                    "Dunraith feeder ties", "Breckwater Electric Cooperative")


def write_pack(S, out):
    os.makedirs(out, exist_ok=True)
    p = {k: os.path.join(out, v) for k, v in FILES.items()}
    n = {}
    n["scada_old"] = write_scada_old(p["scada_old"], S["ld"])
    n["scada_new"] = write_scada_new(p["scada_new"], S["ld"])
    n["wx"] = write_wx(p["wx"], S["wx"])
    n["reglog"] = write_reglog(p["reglog"], S["log"])
    write_forecast(p["forecast"])
    n["mdms"] = write_mdms(p["mdms"], S["mdms"], S["tx"])
    write_register(p["register"], S["tx"], S["dv"])
    n["mv90"] = write_mv90(p["mv90"], S["gt"])
    n["outages"] = write_outages(p["outages"], S["outages"])
    write_ties(p["ties"])
    D.criteria(p["criteria"])
    D.operating_plan(p["opplan"])
    D.test_plan(p["testplan"])
    D.switching_order(p["so"])
    D.delivery_points(p["dpsched"])
    return n
