"""Assemble the world and write target/ (one entry point, called by build.py)."""
import datetime as dt
import os
import shutil

import numpy as np

import params as P
import world_net as N
import world_events as E
import world_other as O
import pack_data as D
import docs

FILE_TIME = dt.datetime(2026, 5, 15, 9, 0, 0).timestamp()


class World:
    pass


def make_world():
    w = World()
    rng = np.random.default_rng(P.SEED)
    w.trips = N.build_timetable(rng)
    w.ev = E.make_events(w.trips)
    w.other = O.make_other(np.random.default_rng(P.SEED + 11))
    w.entries = O.make_entries(np.random.default_rng(P.SEED + 13))
    return w


def write_pack(w, target):
    if os.path.exists(target):
        shutil.rmtree(target)
    os.makedirs(target)
    rms, index = D.rms_rows(w)
    w.rms_index = index
    D.write_csv(os.path.join(target, "rms_occurrence_extract_20260511.csv"), D.RMS_HEADER, rms)
    tpo = D.tpo_rows(w, index)
    D.write_tpo_xlsx(os.path.join(target, "tpo_occurrence_log_2025_2026.xlsx"), tpo)
    D.write_codes_xlsx(os.path.join(target, "carvale_transit_codes.xlsx"))
    D.write_csv(os.path.join(target, "fare_gate_entries_hourly_2026.csv"), ["gate_code", "hour_start_utc", "entries"],
                D.entries_rows(w))
    D.gtfs_files(w, os.path.join(target, "gtfs"))
    D.write_geojson(os.path.join(target, "patrol_districts_2026.geojson"), P.D26, "2026-01-01", None)
    D.write_geojson(os.path.join(target, "patrol_districts_2025.geojson"), P.D25, "2019-01-01", "2025-12-31")
    D.write_csv(os.path.join(target, "secondhand_dealer_phone_returns_2026q1.csv"),
                ["dealer_licence", "purchase_date", "make", "model", "imei_masked", "seller_id_ref", "price_paid_cad"],
                D.pawn_rows())
    docs.directive_pdf(os.path.join(target, "ops41_series_crime_response_directive.pdf"))
    docs.station_reference_pdf(os.path.join(target, "cau_lrt_station_reference_2026.pdf"))
    docs.school_calendar_pdf(os.path.join(target, "cpsd_school_year_calendar_2025_26.pdf"))
    docs.planning_note_docx(os.path.join(target, "summer_deployment_planning_note.docx"))
    for root, dirs, files in os.walk(target):
        for f in files:
            os.utime(os.path.join(root, f), (FILE_TIME, FILE_TIME))
        for dd in dirs:
            os.utime(os.path.join(root, dd), (FILE_TIME, FILE_TIME))
    os.utime(target, (FILE_TIME, FILE_TIME))
    return {"rms_rows": len(rms), "tpo_rows": len(tpo)}
