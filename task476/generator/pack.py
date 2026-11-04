"""Write the pack under target/ from the simulated truth, each file the way its producing system writes it: the stage
logger's export, the hydrographer's visit log, the plant's release log, the water temperature logger, the plant's daily
generation, the powerhouse rain gauge, and the documents."""
import csv
import datetime as dt
import io
import os
import shutil

import numpy as np

import world as W


def _csv(path, header, rows, pre=None, crlf=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    buf = io.StringIO()
    end = "\r\n" if crlf else "\n"
    for line in pre or []:
        buf.write(line + end)
    wr = csv.writer(buf, lineterminator=end)
    if header:
        wr.writerow(header)
    n = 0
    for r in rows:
        wr.writerow(r)
        n += 1
    open(path, "w", newline="", encoding="utf-8").write(buf.getvalue())
    return n


def stage(path, x):
    pre = ["Site: BP-1 Tallis Creek below diversion dam", "Parameter: Gage height (ft)",
           "Instrument: vented pressure transducer, 10-minute interval", "Time zone: PST (UTC-08:00)",
           "Exported: 2026-11-04 08:12 PST", ""]
    rows = [(r["t"].strftime("%Y-%m-%d %H:%M"), "%.3f" % r["h"]) for r in x["rows"]]
    return _csv(path, ["Date Time (PST)", "Gage Height (ft)"], rows, pre=pre, crlf=True)


NOTES = ["Desiccant replaced. Logger downloaded.",
         "Measured from cableway. Staff read in surge.",
         "Trimmed willows at staff plate.",
         "Logger downloaded. Battery 12.9 V.",
         "Orifice line purged. Silt cleaned off staff plate.",
         "Logger downloaded.",
         "Pulse release under way.",
         "Logger battery replaced."]


def visits(path, x):
    rows = []
    for v, ctl, note in zip(x["visits"], W.CONTROL, NOTES):
        lt = v["t"]
        method = "cableway, current meter" if v["gh"] > 3.0 else "wading, acoustic Doppler velocimeter"
        rows.append((lt.strftime("%Y-%m-%d"), lt.strftime("%H:%M"), "%.2f" % v["staff"], "%.2f" % round(v["h"], 2),
                     v["start"].strftime("%H:%M"), v["end"].strftime("%H:%M"), "%.2f" % v["gh"], "%.1f" % v["q_meas"],
                     method, ctl, W.HYDROGRAPHER, note))
    return _csv(path, ["visit_date", "arrival_pdt", "staff_gh_ft", "logger_gh_ft", "meas_start_pdt", "meas_end_pdt",
                       "meas_mean_gh_ft", "meas_discharge_cfs", "meas_method", "control", "hydrographer", "remarks"], rows)


def release(path, x):
    ev = [(when, "Setpoint change", "%g" % v, txt) for when, v, txt in W.SETPOINTS]
    ev += [(W.UNIT_TRIP, "Unit trip", "", "Unit 1 tripped on trash rack differential during storm; spill over crest"),
           (W.UNIT_BACK, "Unit return", "54", "Trash rack cleared, unit 1 back on line; bypass gate returned to setpoint"),
           (dt.datetime(2026, 8, 19, 10, 40, tzinfo=W.PDT), "Maintenance", "", "Gate actuator greased, setpoint unchanged")]
    sp = [r for r in x["rows"] if r["spill"] and r["t"] < W.UNIT_TRIP]
    if sp:
        ev += [(sp[0]["t"].astimezone(W.PDT), "Spill", "", "Spill over crest began; bypass gate at setpoint"),
               (sp[-1]["t"].astimezone(W.PDT), "Spill", "", "Spill over crest ended")]
    off = [r for r in x["rows"] if r["turbine"] == 0 and not r["tripped"]]
    if off:
        ev += [(off[0]["t"].astimezone(W.PDT), "Unit stop", "", "Unit 1 off, inflow below minimum load with pulse release"),
               ((off[-1]["t"] + dt.timedelta(minutes=10)).astimezone(W.PDT), "Unit start", "", "Unit 1 on line after pulse")]
    ev.sort(key=lambda e: e[0])
    rows = [(when.strftime("%m/%d/%Y %H:%M"), kind, sp, txt, "KS" if i % 3 else "ops") for i, (when, kind, sp, txt)
            in enumerate(ev)]
    return _csv(path, ["timestamp_local", "event", "setpoint_cfs", "remarks", "entered_by"], rows)


def temperature(path, x):
    rows = [(t.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "%.2f" % c) for t, c in x["temp"]]
    return _csv(path, ["Date Time, GMT+00:00", "Water Temperature, C (S/N 20481716)"], rows)


def generation(path, x):
    rows = [(d.isoformat(), "%.2f" % g[0], "%.1f" % g[1]) for d, g in sorted(x["gen"].items())]
    return _csv(path, ["date", "unit1_mwh", "unit1_run_hours"], rows)


def precip(path, x):
    rows = [(d.strftime("%m/%d/%Y"), "%.2f" % r) for d, r in sorted(x["rain"].items())]
    return _csv(path, ["date", "precip_in"], rows)


def build_pack(out, x):
    import docs as D
    import postprocess as PP
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    f = lambda k: os.path.join(out, W.FILES[k])
    for k in W.FILES:
        os.makedirs(os.path.dirname(f(k)), exist_ok=True)
    n = {}
    n["stage"] = stage(f("stage"), x)
    n["visits"] = visits(f("visits"), x)
    n["release"] = release(f("release"), x)
    n["temp"] = temperature(f("temp"), x)
    n["generation"] = generation(f("generation"), x)
    n["precip"] = precip(f("precip"), x)
    D.write_register(f("register"))
    PP.normalize_ooxml(f("register"), W.HYDROGRAPHER, W.HYDROGRAPHER, "2023-10-12T17:40:00Z", "2026-05-02T16:05:00Z",
                       excel=True, company=W.CONSULTANT)
    stamps = [(D.write_rating_report, "rating_report", "D:20231012101544-07'00'"),
              (D.write_license, "license", "D:20190611143002-07'00'"),
              (D.write_plan, "plan", "D:20240318091127-07'00'"),
              (D.write_prior, "prior", "D:20260122153318-08'00'")]
    for fn, key, st in stamps:
        fn(f(key))
        PP.normalize_pdf(f(key), st.encode(), st.encode())
    return n
