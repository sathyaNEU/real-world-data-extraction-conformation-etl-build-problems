"""Write task147/metadata.json from the built pack."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as BD      # noqa: E402
import calc as C        # noqa: E402
import deliver as DL    # noqa: E402
import distract as DS   # noqa: E402
import docs as DOC      # noqa: E402
import records as R     # noqa: E402

TASK = os.path.dirname(HERE)
SOURCES = {
    R.F_EXTRACT: "The Weighhouse Hotel property management system, reservation extract of 06:12 on 1 July 2027, one "
                 "row per room reserved for arrivals from 1 January 2022",
    R.F_AMEND: "The Weighhouse Hotel property management system, amendment log of date and guest-count changes",
    R.F_NOTES: "The Weighhouse Hotel property management system, notes on the reservation extract",
    R.F_CODES: "The Weighhouse Hotel property management system, rate, channel and market code lists",
    R.F_AUDIT: "The Weighhouse Hotel night audit, daily statistics 1 January 2022 to 30 June 2027",
    R.F_FEST: "Callowfort Festival of Arts, programme history (festival dates by edition), 2015 to 2027",
    R.F_DIARY: "The Weighhouse Hotel sales office, events diary 2022 to 2027",
    DOC.F_HK04: "The Weighhouse Hotel Rooms Division, standard HK-04 issue 3, housekeeping staffing for the festival "
                "season",
    C.TASKS_F: "The Weighhouse Hotel housekeeping app, task log 27 July to 30 August 2026",
    C.USERS_F: "The Weighhouse Hotel housekeeping app, user list as at 28 June 2027",
    C.HR_F: "The Weighhouse Hotel HR system, housekeeping staff list as at 28 June 2027",
    C.TS_F: "Brennock Hospitality Staffing, timesheet summaries for the Weighhouse, weeks ending 26 July to 6 September "
            "2026",
    C.PAY_F: "The Weighhouse Hotel payroll, room attendants' overtime lines, pay periods 14 to 19 of 2026",
    C.ACCESS_F: "The Weighhouse Hotel staff access system, badge events at the staff entrance and loading bay, August "
                "2026",
    C.BADGE_F: "The Weighhouse Hotel reception, day badges issued, August 2026",
    DOC.F_INVOICE: "Brennock Hospitality Staffing, invoice BHS-INV-2026-0833 for the 2026 block",
    DOC.F_AGREEMENT: "Framework agreement between the Weighhouse Hotel and Brennock Hospitality Staffing, March 2025",
    DS.F_SHOP: "Rate shopping service, competitors' lowest public rates shopped on 30 June 2027",
    DS.F_SURVEY: "Callowfort Tourism, monthly hotel occupancy survey 2019 to 2026",
    BD.F_MANIFEST: "The executive housekeeper's folder index for the 2027 block confirmation",
}
DISTRACTORS = [DS.F_SHOP, DS.F_SURVEY]


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    return None


def write(target, out_path):
    files = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                      "source": "Constructed: " + SOURCES[f], "date": "2027-07-01",
                      "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in files if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task147",
        "title": "Which 2027 festival roster week gets the staffing agency's block of temporary room attendants at a "
                 "480-room city hotel, forecast on the 1 July book with two concert nights already full",
        "domain": "Supply Chain & Logistics",
        "client_domain": "General Statistics & Data Science",
        "subdomain": "resampling-simulation-monte-carlo-methods (the bookings still to come simulated on the booking "
                     "process's independent unit, the stay, a block of consecutive nights taken only if every night "
                     "has a room: each past season's later bookings replayed whole against this year's book, the "
                     "seasons the replicates)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "pick one of five roster weeks with its forecast room-nights above capacity to the nearest "
                        "hundred and the next week with its own figure, a one-page note with the nightly forecast "
                        "chart, and two tables from August 2026 (services and overtime by roster week; the block's "
                        "billable hours and charge by day)",
        "as_of": "2027-07-01",
        "deliverables": [DL.GOLD_BOOK, DL.GOLD_NOTE],
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["380"],
        "input_gates": {"files": len(files), "formats": sorted({x["format"] for x in files}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task147/generator/build.py (seeded, deterministic) around "
                               "a fictional hotel in a fictional Irish city, its festival, its staffing agency and "
                               "their systems; no real organisation, person or system is depicted.",
                     "date": "2027-07-01", "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-16",
        "generator": "task147/generator/build.py",
        "files": files,
    }
    with open(out_path, "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta


if __name__ == "__main__":
    write(os.path.join(TASK, "target"), os.path.join(TASK, "metadata.json"))
