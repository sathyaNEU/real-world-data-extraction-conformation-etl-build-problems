"""Write task270/metadata.json from the built pack: the distractors, the input gates and every shipped file's source,
date and licence."""
import json
import os

import common as K

SOURCES = {
    K.F_LOG: "Ostrevale Fire and Rescue Service mobilising system, resource log 2026 (UTC): each engine's status "
             "messages with their four-hourly re-sends, and the location reports its vehicle tracking unit sends while "
             "it is out of base",
    K.F_FLEET: "Ostrevale Fire and Rescue Service fleet list: stations and appliances, 2026",
    K.F_NODES: "Ostrevale Fire and Rescue Service routing network used by the mobilising system: nodes",
    K.F_LINKS: "Ostrevale Fire and Rescue Service routing network used by the mobilising system: links, drive times and "
               "one-way links",
    K.F_ADDR: "Address register extract for Ostrevale (residential and commercial address points with 2021 output areas)",
    K.F_OALOOK: "Output area lookups: 2021 output areas to districts, 2011 to 2021 output areas",
    K.F_STANDARD: "Ostrevale Fire and Rescue Service emergency cover standard OFRS-RS-03 issue 1 (2 November 2026)",
    K.F_CABINET: "Ostrevale County Council, report to Cabinet on the Community Risk Management Plan 2027 to 2031 "
                 "(23 February 2027)",
    K.F_BOOK: "Ostrevale Fire and Rescue Service on-call availability system, bookings entered for 2026",
    K.F_CREW: "Ostrevale Fire and Rescue Service on-call crew register with 2026 role changes",
    K.F_POLICY: "Ostrevale Fire and Rescue Service operational policy OP-14 issue 4, on-call duty system (1 April 2025)",
    K.F_INC: "Ostrevale Fire and Rescue Service incident recording system, incidents 2022 to 2026",
    K.F_CODES: "Ostrevale Fire and Rescue Service incident classification codes before and from 1 April 2024",
    K.F_POP: "Population estimates by 2021 output area, mid-2025",
    K.F_ESTAB: "Ostrevale Fire and Rescue Service station establishment, 1 January 2026",
}
TITLE = ("Which of a county's seven districts kept a free fire engine within ten minutes of fewer than three quarters "
         "of their homes across 2026, for its 2027 to 2031 community risk management plan, read from where each free "
         "engine stood minute by minute; with the rural on-call stations' crewed-but-off-the-run hours and each "
         "district's false alarms from fire alarm apparatus at non-domestic premises")


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".xlsx"):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True)
        n = sum(max(ws.max_row - 1, 0) for ws in wb.worksheets)
        wb.close()
        return n
    return None


def write(task_dir):
    target = os.path.join(task_dir, "target")
    out = []
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        out.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows_of(p),
                    "source": "Constructed: " + SOURCES[f], "date": K.AS_OF.isoformat(),
                    "license": "CC0-1.0 (original work, constructed for this task)"})
    big = max((x for x in out if x["rows"]), key=lambda x: x["rows"])
    meta = {
        "task": "task270",
        "title": TITLE,
        "domain": "Urban & Regional Science",
        "client_domain": "Urban & Regional Science",
        "subdomain": "network-analysis (a fire and rescue service's emergency cover over its road network: the share "
                     "of homes a free engine could reach within the attendance standard, averaged over a year)",
        "objective": "Descriptive & Distribution Analysis",
        "prompt_shape": "scorecard against a threshold: each of seven districts' 2026 cover against the 75 per cent line "
                        "and whether it is named, beside each rural on-call station's hours off the run with four or "
                        "more firefighters booked (and of those with no crew or watch commander), each district's "
                        "false-alarm actuations at non-domestic premises 2022 to 2026 and their rate, and a chart",
        "as_of": K.AS_OF.isoformat(),
        "deliverables": [K.G_BOOK, K.G_CHART],
        "distractor_files": K.DISTRACTORS,
        "field_terms": [],
        "stated_inputs": [],
        "input_gates": {"files": len(out), "formats": sorted({x["format"] for x in out}),
                        "largest_file": big["path"], "largest_file_rows": big["rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task by task270/generator/build.py (seeded, deterministic) around a "
                               "fictional English county fire and rescue service, in the layouts of a mobilising "
                               "system's resource log with its vehicle location reports, a routing network, an address register "
                               "extract and output area lookups, an on-call availability system's bookings and crew "
                               "register, an incident recording extract and code list, PDF policy, standard and "
                               "cabinet report documents; no real organisation's records or person is depicted.",
                     "date": K.AS_OF.isoformat(), "license": "CC0-1.0 (original work)"}],
        "created": "2026-10-28",
        "generator": "task270/generator/build.py",
        "files": out,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    return meta
