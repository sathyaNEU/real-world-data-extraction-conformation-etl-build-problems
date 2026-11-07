"""Write the task234 pack into a target folder and return the clean truth for the checks."""
import os

import docs
import params as P
import records as RC
import sim

FILES = {
    "results": "elr_respiratory_results_extract_2027-01-25.csv",
    "agg": "lab_weekly_aggregate_reports.csv",
    "reg": "respiratory_stream_register.xlsx",
    "codes": "elr_result_codes.csv",
    "fcp": "FCP-2_feed_completeness_protocol.pdf",
    "log": "surveillance_platform_change_log.csv",
    "ili": "ed_syndromic_ili_weekly.csv",
    "state": "state_respiratory_positivity_by_region.csv",
    "adm": "county_respiratory_admissions_weekly.csv",
    "vax": "county_influenza_vaccination_coverage_2026-27.csv",
}
DISTRACTORS = ["ili", "state", "adm", "vax"]


def run(target):
    os.makedirs(target, exist_ok=True)
    W = sim.World().build()
    R = RC.Records(W)
    res = R.results()
    res = R.cancelled(res)
    stored = R.as_stored(res)
    agg = R.aggregate_reports()
    labs, streams = R.register()
    p = lambda k: os.path.join(target, FILES[k])
    stored.to_csv(p("results"), index=False, lineterminator="\n")
    agg.to_csv(p("agg"), index=False, lineterminator="\n")
    RC.Records.code_list().to_csv(p("codes"), index=False, lineterminator="\n")
    R.ed_ili().to_csv(p("ili"), index=False, lineterminator="\n")
    R.state_positivity().to_csv(p("state"), index=False, lineterminator="\n")
    R.admissions().to_csv(p("adm"), index=False, lineterminator="\n")
    R.vaccination().to_csv(p("vax"), index=False, lineterminator="\n")
    docs.change_log().to_csv(p("log"), index=False, lineterminator="\n")
    docs.register(p("reg"), labs, streams)
    docs.protocol(p("fcp"))
    return dict(W=W, R=R, res=res)
