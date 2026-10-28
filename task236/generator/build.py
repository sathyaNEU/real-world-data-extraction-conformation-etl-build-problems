"""Write the task236 pack into a target folder and return the clean truth for the checks."""
import os

import asks
import docs
import params as P
import records as RC
import sim

FILES = {
    "res": "gateway_influenza_results_2027-04-05_to_2027-09-12.csv",
    "ret": "sentinel_gp_weekly_returns_2027_wk14-36.csv",
    "sw": "sentinel_gp_protocol_swabs_2027_wk14-36.csv",
    "reg": "testing_change_register_2027.xlsx",
    "conc": "postcode_health_region_concordance.csv",
    "pop": "postcode_erp_30_june_2026.csv",
    "svc": "reporting_services.csv",
    "prot": "influenza_report_data_quality_protocol_CDB-FLU-03.pdf",
    "sprot": "sentinel_gp_network_protocol_SGP-2027.pdf",
    "vac": "influenza_vaccine_doses_by_region_2027_wk14-36.csv",
    "tat": "laboratory_turnaround_by_week_2027.csv",
    "dict": "DATA_DICTIONARY.md",
    "readme": "README.md",
}
DISTRACTORS = ["vac", "tat"]


def run(target):
    os.makedirs(target, exist_ok=True)
    W = sim.make()
    R = RC.Records(W)
    res0 = R.results()
    res, man = asks.apply(res0, R, P.ASK_PLAN)
    ret = R.sentinel_returns()
    sw = R.sentinel_swabs()
    p = lambda k: os.path.join(target, FILES[k])
    csv = lambda df, k: df.to_csv(p(k), index=False, lineterminator="\n")
    csv(res, "res")
    csv(ret, "ret")
    csv(sw, "sw")
    csv(R.concordance(), "conc")
    csv(R.population(), "pop")
    csv(docs.services(), "svc")
    csv(R.vaccine_doses(), "vac")
    csv(R.turnaround(res), "tat")
    reg = R.register()
    docs.register(p("reg"), reg)
    docs.protocol(p("prot"))
    docs.sentinel_protocol(p("sprot"))
    with open(p("dict"), "w") as fh:
        fh.write(docs.dictionary(FILES))
    with open(p("readme"), "w") as fh:
        fh.write(docs.readme(FILES))
    return dict(W=W, R=R, res=res, res0=res0, man=man, ret=ret, sw=sw, reg=reg)
