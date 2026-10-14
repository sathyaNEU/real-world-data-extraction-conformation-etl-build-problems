"""Rows for the pack's flat files, in each system's own layout."""
from __future__ import annotations

import datetime as dt

import common as K
import weather as WX

# ---------------------------------------------------------------------------------------------------- id formats

def tid_orders(tid):            # the ordering system: 05-031
    return tid


def tid_book(tid):              # the riders' meter book: 5-31
    a, b = tid.split("-")
    return "%d-%d" % (int(a), int(b))


def tid_gis(tid):               # the GIS register and the meter shop: T05031
    a, b = tid.split("-")
    return "T%02d%03d" % (int(a), int(b))


# ---------------------------------------------------------------------------------------------------- weather

ST39_COLS = ["Stn Id", "Stn Name", "Region", "Date", "Jul", "ETo (mm)", "qc", "Precip (mm)", "qc", "Sol Rad (W/sq.m)",
             "qc", "Max Air Temp (C)", "qc", "Min Air Temp (C)", "qc", "Avg Rel Hum (%)", "qc", "Avg Wind Speed (m/s)",
             "qc"]


def st39_rows(W):
    r = K.rng("st39-qc")
    out = []
    for d in K.daterange(K.WEATHER_START, K.WEATHER_END):
        x = W.s39_rep[d]
        flags = ["Y" if r.random() < 0.004 else "" for _ in range(7)]
        out.append([39, K.STATION39_NAME, "San Joaquin Valley", "%d/%d/%d" % (d.month, d.day, d.year),
                    d.timetuple().tm_yday, "%.2f" % x["eto_mm"], flags[0], "%.2f" % x["precip_mm"], flags[1],
                    "%.1f" % x["sol_wm2"], flags[2], "%.1f" % x["tmax_c"], flags[3], "%.1f" % x["tmin_c"], flags[4],
                    x["rh"], flags[5], "%.1f" % x["wind"], flags[6]])
    return out


YARD_COLS = ["Date", "ETo_in", "Rain_in", "Tmax_F", "Tmin_F", "RHavg_pct", "Wind_mph", "Srad_ly", "Flag"]


def yard_rows(W):
    out = []
    absent = WX.yard_absent()
    blank = WX.yard_missing() - absent
    for d in K.daterange(K.DISTRICT_STATION_START, K.WEATHER_END):
        if d in absent:
            continue
        if d in blank:
            out.append([d.isoformat(), "", "", "", "", "", "", "", "M"])
            continue
        x = W.yard_rep[d]
        out.append([d.isoformat(), "%.2f" % x["et0_in"], "%.2f" % x["rain_in"], "%.1f" % x["tmax_f"], "%.1f" % x["tmin_f"],
                    "%.1f" % x["rh"], "%.1f" % x["wind_mph"], "%d" % x["srad_ly"], ""])
    return out


# ---------------------------------------------------------------------------------------------------- the district

REGISTER_COLS = ["field_id", "former_field_id", "apn", "turnout_id", "lateral", "soil_unit", "gis_acres",
                 "field_status", "last_edit"]


def register_rows(W):
    r = K.rng("register")
    out = []
    for f in sorted(W.fields, key=lambda f: f["id"]):
        t = W.turnout[f["turnout"]]
        edit = K.REMAP
        if t["moved"]:
            edit = dt.date(2026, 6, 16)
        elif r.random() < 0.18:
            edit = dt.date(2025, int(r.integers(4, 13)), int(r.integers(1, 28))) if r.random() < 0.6 else \
                dt.date(2026, int(r.integers(1, 12)), int(r.integers(1, 28)))
        gis = f["acres"] * float(r.uniform(0.985, 1.03))
        out.append(dict(field_id=f["id"], former_field_id=f["former"], apn=f.get("apn") or apn(r),
                        turnout_id=tid_gis(f["turnout"]), lateral=K.LATERAL_NAME[f["lateral"]], soil_unit=f["soil"],
                        gis_acres="%.2f" % gis, field_status="Active", last_edit=edit.isoformat()))
    return out


def apn(r):
    return "%03d-%03d-%03d" % (int(r.integers(100, 400)), int(r.integers(10, 990)), int(r.integers(1, 99)))


# ---------------------------------------------------------------------------------------------------- orders

ORDERS_COLS = ["order_no", "season", "turnout", "field_id", "ordered_cfs", "set_start", "set_end", "status",
               "entered_at", "entered_by"]


def orders_rows(W):
    r = K.rng("orders-file")
    out = []
    for o in W.orders:
        by = str(r.choice(["office", "office", "office", "phone", "rider"]))
        out.append(dict(order_no=o["order_no"], season=o["season"], turnout=tid_orders(o["turnout"]),
                        field_id=o["field_id"], ordered_cfs="%.1f" % o["cfs"],
                        set_start=o["start"].strftime("%Y-%m-%d %H:%M"), set_end=o["end"].strftime("%Y-%m-%d %H:%M"),
                        status=o["status"], entered_at=o["entered"].strftime("%Y-%m-%d %H:%M"), entered_by=by))
    return out


# ---------------------------------------------------------------------------------------------------- the ask paths

BOOK_COLS = ["route", "turnout", "meter", "read_date", "read_time", "reading", "reg_units", "rider", "note"]


def book_rows(W):
    r = K.rng("book-file")
    riders = {lat: "DR-%02d" % (k + 3) for k, lat in enumerate(K.LATERALS)}
    out = []
    for x in sorted(W.reads, key=lambda x: (x["when"].date(), x["route"], x["turnout"])):
        lat = x["route"]
        note = ""
        if r.random() < 0.012:
            note = str(r.choice(["gate leaking", "meter fogged, read through lens", "no water", "turnout locked",
                                 "lid replaced"]))
        reading = ("%.2f" % x["value"]) if x["units"] == "AF" else "%d" % x["value"]
        out.append(dict(route="Route %s" % lat[1:], turnout=tid_book(x["turnout"]), meter=x["serial"],
                        read_date=x["when"].strftime("%m/%d/%Y"), read_time=x["when"].strftime("%H:%M"),
                        reading=reading, reg_units="AF" if x["units"] == "AF" else "CCF", rider=riders[lat],
                        note=note))
    return out


HEAD_COLS = ["date", "lateral", "structure", "volume_af"]
HEAD_STRUCT = {"L1": "Replogle flume", "L2": "Replogle flume", "L3": "Parshall flume", "L4": "Replogle flume",
               "L5": "Replogle flume", "L6": "Parshall flume", "L7": "Replogle flume", "L8": "Replogle flume",
               "L9": "Parshall flume"}


def heading_rows(W):
    out = []
    for h in sorted(W.headings, key=lambda h: (h["date"], h["lateral"])):
        out.append(dict(date=h["date"].isoformat(), lateral=K.LATERAL_NAME[h["lateral"]],
                        structure="%s heading %s" % (K.LATERAL_NAME[h["lateral"]], HEAD_STRUCT[h["lateral"]]),
                        volume_af="%.2f" % h["af"]))
    return out


WEIR_COLS = ["sheet_date", "lateral", "weir", "read_time", "gauge_ft", "remarks"]


def weir_rows(W):
    out = []
    for x in sorted(W.weir_rows, key=lambda x: (x["date"], x["lateral"])):
        out.append(dict(sheet_date=x["date"].strftime("%m/%d/%Y"), lateral=K.LATERAL_NAME[x["lateral"]],
                        weir="%s tail weir" % K.LATERAL_NAME[x["lateral"]], read_time=x["time"],
                        gauge_ft="%.2f" % x["gauge"], remarks=x["remarks"]))
    return out


# ---------------------------------------------------------------------------------------------------- distractors

GW_COLS = ["well_id", "measured", "depth_to_water_ft", "method", "qa_code", "comment"]


def groundwater_rows(W):
    r = K.rng("groundwater")
    out = []
    wells = ["KB-MW-%02d" % k for k in range(1, 25)]
    for w in wells:
        base = float(r.uniform(38, 118))
        trend = float(r.uniform(0.6, 2.4))
        for y in range(2016, 2027):
            for season, (m, lo, hi) in (("spring", (2, 10, 27)), ("fall", (10, 12, 28))):
                d = dt.date(y, m, int(r.integers(lo, hi)))
                depth = base + trend * (y - 2016) + (7.0 if season == "fall" else 0.0) + float(r.normal(0, 2.2))
                qa = "Q1" if r.random() < 0.05 else ""
                out.append(dict(well_id=w, measured=d.isoformat(), depth_to_water_ft="%.1f" % depth,
                                method=str(r.choice(["electric sounder", "steel tape"])), qa_code=qa,
                                comment="nearby well pumping" if qa else ""))
    return out


CROP_REPORT_COLS = ["field_id", "turnout", "crop_code", "crop", "irrigated_acres", "irrigation_method", "reported"]


def crop_report_rows(W):
    r = K.rng("crop-report")
    out = []
    for f in sorted(W.fields, key=lambda f: f["id"]):
        method = f.get("method_2026", f["method"])
        acres = f.get("acres_2026", f["acres"])
        out.append(dict(field_id=f["id"], turnout=tid_orders(f["turnout"]), crop_code=f["crop"], crop=K.CROP_NAME[f["crop"]],
                        irrigated_acres="%.1f" % acres, irrigation_method=method,
                        reported=(dt.date(2026, 6, 1) + dt.timedelta(days=int(r.integers(0, 45)))).isoformat()))
    return out


MANIFEST_COLS = ["file", "what it holds", "system or source", "extracted or issued", "rows", "owner"]
