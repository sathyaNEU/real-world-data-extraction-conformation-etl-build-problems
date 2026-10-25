"""Cut the task303 pack from the record: the two outage exports, the storm crews' statuses, the accepted major event
days, the inventory, the plan's valuation guidance, the export notes, the commission's order and two distractors."""
import csv
import os

import docs
import params as P
import postprocess
import records as R

FILES = P.FILES
PACK = list(FILES)
DISTRACTORS = ("veg", "settings")
CONTEXT = ("order",)


def _csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


def build(target):
    os.makedirs(target, exist_ok=True)
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    rc = R.Record()
    _csv(F["legacy"], ["TKT_NO", "FDR", "SUB_CD", "OUT_DT", "OUT_TM", "DUR_MIN", "CUST_OUT", "CAUSE_CD", "DEV_TYP",
                       "DEV_ID"], rc.legacy_rows())
    _csv(F["current"], ["interruption_id", "feeder", "substation", "interruption_start_utc", "restoration_utc",
                        "customers_interrupted", "cause_category", "protective_device_type", "protective_device"],
         rc.current_rows())
    _csv(F["crews"], ["job_id", "oms_interruption_id", "job_type", "feeder", "device", "crew_id", "crew_type",
                      "status", "status_time_local"], rc.crew_rows())
    _csv(F["meds"], ["event_date", "event", "system_t_med_minutes", "accepted_in"], rc.med_rows())
    docs.notes(F["notes"])
    docs.crew_notes(F["crew_notes"])
    docs.vegetation(F["veg"])
    docs.inventory(F["inventory"], rc.taps)
    postprocess.scrub(F["inventory"], P.ORG, "2026-09-21")
    postprocess.finish_office(F["inventory"], "2024-02-12T14:05:00Z", "2026-09-21T10:44:00Z", P.ORG)
    docs.recloser_settings(F["settings"])
    postprocess.scrub(F["settings"], P.ORG, "2026-07-30")
    postprocess.finish_office(F["settings"], "2023-05-08T09:12:00Z", "2026-07-30T16:20:00Z", P.ORG)
    docs.plan(F["plan"])
    postprocess.scrub(F["plan"], P.ORG, "2026-10-06")
    postprocess.finish_office(F["plan"], "2026-09-24T08:02:00Z", "2026-10-06T16:47:00Z", P.ORG,
                              person=P.PLANNER, revision=7)
    docs.order(F["order"])
    postprocess.scrub(F["order"], "Microsoft Word 2016", "2024-03-14T15:10:00")
    return rc
