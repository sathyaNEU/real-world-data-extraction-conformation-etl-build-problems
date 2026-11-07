"""metadata.json: the task's decision, deliverables, distractors and each file's provenance; never the method."""
import json
import os

import docs as D
import records as R

LICENCE = "Constructed for this task; no third-party data; free to use with the task."
PROV = {
    R.F_SCADA: "PS03 Riverbank Road SCADA historian export, 15-minute values, 1 January 2024 to 31 October 2026, pulled 3 November 2026",
    R.F_RAIN: "Kahuwera Regional Council hydrometric archive, climate station Rauwhero at Treatment Plant (KRC 1187), hourly rainfall 2004 to 2025",
    R.F_RAIN26: "Kahuwera Regional Council telemetry, KRC 1187, 15-minute rainfall for 2026 to 31 October, provisional",
    R.F_BORE: "Kahuwera Regional Council level export, bore 72_1043 Rauwhero Terrace, daily, 2004 to 31 October 2026",
    R.F_ASSETS: "Rauwhero District Council asset management system extract: wastewater gravity mains, manholes, pump stations and overflow monitors, 30 October 2026",
    R.F_MONITOR: "Council SMS gateway log of the engineered overflow monitors' messages, 2024 to 31 October 2026",
    R.F_OUTAGES: "Lines company outage notices for the council's ICPs, 2024 to 2026",
    R.F_ICPS: "Council electricity retailer site list, October 2026",
    R.F_READS: "Council water billing system: meter readings for the PS03 catchment's meters, October 2023 to October 2026",
    R.F_ACCOUNTS: "Council water billing system: accounts for the PS03 catchment's meters, November 2026",
    R.F_RATING: "Council rating information database snapshot, 31 October 2026",
    R.F_BC: "Council building consent register extract, 2023 to 2026",
    R.F_WWTP: "Rauwhero wastewater treatment plant operator's daily inlet meter readings, 2024 to 2026",
    R.F_WORKS: "PS03 maintenance work orders, 2024 to 2026",
    D.F_CONSENT: "Kahuwera Regional Council discharge permit AUTH-2024-0418, granted 18 March 2024",
    D.F_DATASHEET: "PS03 pump station data sheet, revision 4, 7 November 2023",
    D.F_COP: "Rauwhero District Council Code of Practice for Land Development and Subdivision, Section 5 Wastewater, July 2022",
    D.F_SERVICING: "Ngaio Road subdivision RM26-0187 wastewater servicing report, 21 September 2026",
    D.F_POLICY: "Rauwhero District Council Water Metering and Billing Policy, July 2023",
    D.F_BRIEF: "PS03 storage augmentation project brief, version 2, 12 August 2026",
}
DISTRACTORS = [R.F_WWTP, R.F_WORKS]


def write(task_dir, n=None):
    files = []
    for f in sorted(os.listdir(os.path.join(task_dir, "target"))):
        files.append(dict(file="target/" + f, source=PROV[f], licence=LICENCE, rows=(n or {}).get(f)))
    meta = dict(
        task="task156",
        decision="Whether the Ngaio Road subdivision can connect to the PS03 Riverbank Road pump station in 2027 within "
                 "the station's consented wet weather overflows, or must wait for the storage upgrade",
        deliverables=["ps03_ngaio_road_connection_2027.xlsx", "council_report_ngaio_road_2027.docx",
                      "replay_overflows_2004-2023.png"],
        domain="physical-environmental-sciences", objective="forecasting",
        distractor_files=["target/" + f for f in DISTRACTORS],
        as_of="2026-11-04", files=files)
    json.dump(meta, open(os.path.join(task_dir, "metadata.json"), "w"), indent=1)
