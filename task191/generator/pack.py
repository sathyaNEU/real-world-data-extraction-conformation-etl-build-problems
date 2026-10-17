"""Write the bundle the platform's network planning desk would hand over."""
import csv
import datetime as dt
import os
import random

import panel
import sim
import world as W

FILES = {
    "panel": "panel_throughput_minutes.csv",
    "rollup": "evening_quality_daily.csv",
    "register": "interconnect_register.csv",
    "maint": "maintenance_windows.csv",
    "health": "collector_health_log.csv",
    "edge": "edge_traffic_5min.csv",
    "commit": "peering_commitments.csv",
    "amend": "commitment_amendments.csv",
    "credits": "invoice_credits.csv",
    "sessions": "client_sdk_sessions.csv",
    "releases": "sdk_release_log.json",
    "rebuffer": "rebuffer_events_daily.csv",
    "incidents": "incident_log.csv",
    "restored": "incident_restoration_extract.csv",
    "plan": "peering_capacity_plan.xlsx",
    "catalogue": "content_catalogue_hours.csv",
    "cache": "cdn_cache_hit_by_pop.csv",
    "manifest": "telemetry_handover_inventory.csv",
}


def _csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return path


def recorded_port(code, day):
    """the port code the record carries: one port was renamed inside the quarter"""
    old, new, when = W.RENAMED
    return old if code == new and day < when else code


def write_panel(target, minutes):
    """one row per interconnect per minute of the two retained bands, with the collector's losses.

    A collector loss takes a whole band for a whole day on one port, which is what an outage does,
    so the bands the collector did capture are whole and their medians are the standard's own.
    """
    rng = random.Random(W.SEED + 11)
    lost = set()
    kept, dropped = [], {}
    for stamp, code, sessions, med, p10, reb, sday in minutes:
        local = stamp + dt.timedelta(hours=panel.offset(stamp.date()))
        band = "evening" if local.hour >= W.EVENING_BAND[0] else "day"
        key = (code, local.date(), band)
        if key not in lost:
            lost.add(key)
            if rng.random() < 0.0118:
                dropped[key] = True
        if dropped.get(key):
            continue
        kept.append((stamp, code, local, sessions, med, p10, reb, sday, band))
    rows = [[k[0].strftime("%Y-%m-%dT%H:%M:%SZ"), recorded_port(k[1], k[2].date()),
             k[3], k[4], k[5], k[6]] for k in kept]
    rows.sort(key=lambda r: (r[0], r[1]))
    _csv(os.path.join(target, FILES["panel"]),
         ["measured_at_utc", "port_code", "sessions", "median_kbps", "p10_kbps",
          "rebuffer_events"], rows)
    return kept, sorted(dropped)


def rollup_from_panel(kept):
    """the pipeline's daily band medians, read off the minutes the collector captured"""
    by = {}
    for stamp, code, local, sessions, med, p10, reb, sday, band in kept:
        by.setdefault((code, local.date()), {}).setdefault(band, {}) \
          .setdefault(local.hour, []).append(med)
        by[(code, local.date())]["sessions"] = sday
    out = []
    for (code, day), bands in sorted(by.items()):
        if "day" not in bands or "evening" not in bands:
            continue                     # the pipeline summarises a day it captured both bands on
        ref = [v for h in bands["day"] for v in bands["day"][h]]
        if len(ref) < 180:
            continue
        refmed = panel.median_of(ref)
        for _, hour in W.WINDOWS:
            vals = bands["evening"].get(hour)
            if not vals or len(vals) < 60:
                continue
            out.append(("2027Q1", code, day, hour, panel.median_of(vals), refmed,
                        bands["sessions"]))
    return out


def write_rollup(target, rollup):
    """the pipeline's own daily summary, kept for two years where the minutes are kept for ninety"""
    rows = []
    for label, code, day, hour, ev, dayb, sess in rollup:
        rows.append([day.isoformat(), recorded_port(code, day), "%02d:00" % hour,
                     "%.0f" % ev, "%.0f" % dayb, sess, label])
    rows.sort(key=lambda r: (r[0], r[1], r[2]))
    return _csv(os.path.join(target, FILES["rollup"]),
                ["evening_date_local", "port_code", "window_from", "evening_median_kbps",
                 "reference_median_kbps", "sessions", "reporting_quarter"], rows)


def write_register(target):
    rows = []
    for code, peer, kind, cap, load, spread in W.PATHS:
        rows.append([code, peer, kind, cap, "2023-04-01", "", "in service", code])
    old, new, when = W.RENAMED
    rows.append([old, dict((p[0], p[1]) for p in W.PATHS)[new], "cable", 100, "2023-04-01",
                 (when - dt.timedelta(days=1)).isoformat(), "renamed", new])
    rows.append(["BRK-01", "Brakveld Net", "cable", 100, "2023-04-01", "2026-05-31",
                 "decommissioned", ""])
    rows.append(["TRN-A1", "Noordlijn Transit", "transit", 400, "2023-04-01", "", "in service",
                 "TRN-A1"])
    rows.append(["TRN-A2", "Noordlijn Transit", "transit", 400, "2025-09-01", "", "in service",
                 "TRN-A2"])
    rows.append(["TRN-B1", "Grensweg Carrier", "transit", 200, "2023-04-01", "", "in service",
                 "TRN-B1"])
    rows.append(["TRN-B2", "Grensweg Carrier", "transit", 200, "2026-02-01", "", "in service",
                 "TRN-B2"])
    rows.append(["TRN-C1", "Zandpoort IX", "transit", 100, "2024-11-01", "", "in service",
                 "TRN-C1"])
    return _csv(os.path.join(target, FILES["register"]),
                ["port_code", "peer", "port_type", "capacity_gbps", "in_service_from",
                 "in_service_to", "status", "current_port_code"], rows)


def write_maintenance(target):
    """the planned work the network operations team books, with the evenings it covers"""
    rng = random.Random(W.SEED + 17)
    rows = []
    code, lo, hi = W.MAINTENANCE
    d = lo
    while d <= hi:
        rows.append([recorded_port(code, d), d.isoformat(), "19:00", "23:30",
                     "line card replacement, port running on one card", "CHG-20412"])
        d += dt.timedelta(days=1)
    # earlier planned work, outside the evening band, which the framework does not reach
    for i, (c, day, frm, to, what, ref) in enumerate([
            ("KZD-01", dt.date(2027, 1, 14), "02:00", "05:00", "optics clean", "CHG-20287"),
            ("VSN-01", dt.date(2027, 1, 28), "03:00", "06:00", "firmware", "CHG-20331"),
            ("DLF-01", dt.date(2027, 3, 4), "02:30", "04:30", "cross connect move", "CHG-20498"),
            ("OPL-01", dt.date(2027, 3, 18), "01:00", "04:00", "optics clean", "CHG-20536")]):
        rows.append([recorded_port(c, day), day.isoformat(), frm, to, what, ref])
    rows.sort(key=lambda r: (r[1], r[0]))
    return _csv(os.path.join(target, FILES["maint"]),
                ["port_code", "work_date_local", "window_from", "window_to", "work", "change_ref"],
                rows)


def write_health(target, dropped):
    """the collector's own record of what it captured, by day and port"""
    by = {}
    for code, day, band in dropped:
        by[(day, code)] = by.get((day, code), 0) + 180
    rows = []
    for label, lo, hi in sim.quarters():
        if label != "2027Q1":
            continue
        for day in sim.evenings(lo, hi):
            for code, peer, kind, cap, load, spread in W.PATHS:
                miss = by.get((day, code), 0)
                rows.append([day.isoformat(), recorded_port(code, day), 360, 360 - miss, miss])
    return _csv(os.path.join(target, FILES["health"]),
                ["collection_date_local", "port_code", "minutes_scheduled", "minutes_captured",
                 "minutes_missing"], rows)


def write_plan(target):
    """the capacity plan as the planning desk keeps it, one wide sheet a month"""
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font
    rng = random.Random(W.SEED + 43)
    wb = Workbook()
    first = True
    for mon, name in ((1, "Jan 2027"), (2, "Feb 2027"), (3, "Mar 2027")):
        ws = wb.active if first else wb.create_sheet()
        ws.title = name
        first = False
        ws["A1"] = "%s: interconnect capacity plan, %s" % (W.PLATFORM, name)
        ws["A1"].font = Font(bold=True, size=12)
        ws["A2"] = "Committed and planned capacity in gigabits a second. Planning desk working copy."
        ws["A3"] = "Prepared by the network planning desk."
        head = ["Measure"] + [p[0] for p in W.PATHS] + ["Transit"]
        for j, h in enumerate(head):
            c = ws.cell(row=5, column=1 + j, value=h)
            c.font = Font(bold=True)
            if j:
                c.alignment = Alignment(horizontal="center")
        for i, (label, scale) in enumerate((("Committed capacity", 1.0),
                                            ("Busy hour load", 0.58),
                                            ("Headroom", 0.42),
                                            ("Planned capacity next quarter", 1.0))):
            ws.cell(row=6 + i, column=1, value=label)
            for j, p in enumerate(W.PATHS):
                v = p[3] * scale * (0.97 + 0.06 * rng.random())
                if label == "Planned capacity next quarter":
                    v = p[3] * (1.0 if rng.random() < 0.7 else 1.5)
                ws.cell(row=6 + i, column=2 + j, value=round(v, 1))
            ws.cell(row=6 + i, column=2 + len(W.PATHS),
                    value=round(1100 * scale * (0.97 + 0.06 * rng.random()), 1))
        ws.cell(row=11, column=1, value="Headroom is committed capacity less busy hour load and "
                                        "carries no quality measure.").font = Font(size=9,
                                                                                   italic=True)
        ws.column_dimensions["A"].width = 30
    path = os.path.join(target, FILES["plan"])
    wb.save(path)
    return path


def write_manifest(target):
    """what the data platform handed over, each file with its own rows and range"""
    import csv as _c
    spans = {
        FILES["panel"]: ("measured_at_utc", "measured_at_utc",
                         "one row per interconnect per minute of the two retained bands"),
        FILES["rollup"]: ("evening_date_local", "evening_date_local",
                          "the pipeline's daily band medians, kept for two years"),
        FILES["health"]: ("collection_date_local", "collection_date_local",
                          "what the collector was due to record and what it did"),
        FILES["edge"]: ("sampled_at_utc", "sampled_at_utc",
                        "the edge's five-minute traffic samples for every port it bills"),
        FILES["maint"]: ("work_date_local", "work_date_local",
                         "work the network operations team booked"),
        FILES["sessions"]: ("session_date_local", "session_date_local",
                            "client sessions by day and version string"),
        FILES["rebuffer"]: ("session_date_local", "session_date_local",
                            "sessions that rebuffered, by day and version string"),
        FILES["incidents"]: ("opened_at_utc", "opened_at_utc",
                             "every incident the duty desk opened in the quarter"),
        FILES["restored"]: ("service_restored_at_utc", "service_restored_at_utc",
                            "the restoration times the duty engineers recorded"),
    }
    rows = []
    for name in sorted(spans):
        lo_col, hi_col, scope = spans[name]
        with open(os.path.join(target, name), encoding="utf-8") as fh:
            rd = list(_c.DictReader(fh))
        lo = min(r[lo_col] for r in rd if r[lo_col])[:10]
        hi = max(r[hi_col] for r in rd if r[hi_col])[:10]
        rows.append([name, str(len(rd)), lo, hi, W.AS_OF.isoformat(), scope])
    for name, scope in ((FILES["register"], "every interconnect and transit port the platform holds"),
                        (FILES["commit"], "the peering and transit commitments in force"),
                        (FILES["amend"], "amendments to those commitments"),
                        (FILES["credits"], "service credits issued to peers"),
                        (FILES["catalogue"], "titles and hours added, by genre"),
                        (FILES["cache"], "cache hit ratio and egress by point of presence")):
        with open(os.path.join(target, name), encoding="utf-8") as fh:
            n = sum(1 for _ in fh) - 1
        rows.append([name, str(n), "", "", W.AS_OF.isoformat(), scope])
    return _csv(os.path.join(target, FILES["manifest"]),
                ["extract", "rows_handed_over", "covers_from", "covers_to", "pulled_on",
                 "what_it_holds"], rows)
