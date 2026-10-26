"""metadata.json in the task folder: per shipped file its source, date, licence and rows, and the distractors."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
SYN = " (fictional, synthetic records)"
LIC = "CC0-1.0 (synthetic, generated for this task)"
VE = "Vennholt Energy Ltd., Kesmere field"
SOURCES = {
    "battery_register_20270108.csv": (VE + ", battery register", "2027-01-08"),
    "route_app_visits_20251215_20260630.csv": (VE + ", the route app (the lease operators' visit app to 30 June 2026), visit export", "2027-01-08"),
    "checkin_app_visits_20260615_20270112.jsonl": (VE + ", the check-in app (the lease operators' app from 1 July 2026), check-in export", "2027-01-13"),
    "checkin_app_sites.csv": (VE + ", the check-in app's site list", "2027-01-13"),
    "release_event_register_2026.xlsx": (VE + ", EHS office release event register", "2027-01-11"),
    "scada_alarm_journal_20251215_20270112.csv": (VE + ", SCADA host alarm and event journal", "2027-01-13"),
    "battery_daily_production_20251215_20261231.csv": (VE + ", production accounting, daily battery volumes",
                                                       "2027-01-09"),
    "tank_vapour_analyses_2025_2026.xlsx": (VE + ", production engineering, tank vapour laboratory results",
                                            "2026-11-30"),
    "maintenance_work_orders_2026.csv": (VE + ", maintenance system, work orders completed in 2026", "2027-01-08"),
    "ldar_surveys_2025_2026.csv": (VE + ", EHS office, OGI leak survey log", "2027-01-12"),
    "ldar_leak_tracker_20270112.xlsx": (VE + ", EHS office, leak tracker", "2027-01-12"),
    "hauler_load_tickets_2026.csv": ("Kesmere Fluid Haulers, load tickets for Vennholt Energy", "2027-01-06"),
    "sales_gas_meter_statements_2026.csv": (VE + ", gas marketing, sales meter monthly statements", "2027-01-11"),
    "peb_directive_17_release_event_return_2025.pdf": ("Provincial Energy Board, Directive 17, 2025 edition",
                                                       "2025-03-14"),
    "kesmere_field_data_notes.txt": (VE + ", production data team, notes on the exports", "2027-01-13"),
}
DISTRACTORS = ["target/hauler_load_tickets_2026.csv", "target/sales_gas_meter_statements_2026.csv"]


def main():
    files = []
    for n in sorted(os.listdir(T)):
        src, date = SOURCES[n]
        rows = None
        if n.endswith(".csv"):
            rows = sum(1 for _ in open(os.path.join(T, n), "rb")) - 1
        elif n.endswith(".jsonl"):
            rows = sum(1 for _ in open(os.path.join(T, n), "rb"))
        files.append(dict(file=n, source=src + SYN, date=date, license=LIC, rows=rows))
    meta = dict(task="task487", title="Vennholt Energy's 2026 release-event return and its 2027 levy under the "
                                      "Provincial Energy Board's Directive 17",
                setting="A fictional upstream oil producer's 180 tank batteries in a fictional western Canadian "
                        "province, whose energy board levies release-event methane in bands: the province, the board, "
                        "the operator, its field and its people are fictional, and every record is synthetic.",
                as_of="2027-01-14",
                deliverables=["release_events_2026.csv", "release_levy_filing_2026.xlsx"],
                distractor_files=DISTRACTORS, stated_inputs=["calendar 2026", "each half of 2026",
                                                             "Schedule B methane in tonnes to one decimal"], files=files)
    assert set(SOURCES) == set(os.listdir(T)), set(SOURCES) ^ set(os.listdir(T))
    json.dump(meta, open(os.path.join(TASK, "metadata.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
