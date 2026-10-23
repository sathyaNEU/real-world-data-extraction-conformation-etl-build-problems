"""metadata.json for task171 (outside target/): the distractors and the portal's keys."""
import json
import os

import common as C


def write():
    m = {
        "task": "task171",
        "title": "Sablewood Electric Cooperative's optional overnight rate R-ON: services moved by the end of 2027 and the revenue they give up",
        "domain": "Economics & Econometrics",
        "client_domain": "Economics & Econometrics",
        "subdomain": "discrete choice and limited dependent variable modeling (take-up of an optional rate as a binary choice on the member's own bill saving, carried from the 2024 evening-peak rate to the 2027 overnight rate)",
        "objective": "Forecasting & Predictive Modeling",
        "prompt_shape": "two committed figures; R-TOU services, tenure and 4 to 9 p.m. kWh by district; R-TOU requests by district and month",
        "as_of": "2026-10-31",
        "deliverables": ["r-on_2027_forecast.xlsx"],
        "distractor_files": [C.F_EV, C.F_HDD, C.F_BILL, C.F_EXCH],
        "distractors": [
            {"file": C.F_EV, "wrong_basis": False, "why_relevant": "EV charger rebates name services likely to charge overnight",
             "why_unused": "no figure reads it; the services' own metered use already carries any overnight charging", "ruled_out_by": "its header: rebates paid, not use"},
            {"file": C.F_HDD, "wrong_basis": False, "why_relevant": "daily degree days for the territory over the record",
             "why_unused": "the forecast is at test-year use as filed; weather enters only through the metered use", "ruled_out_by": "the committee paper's test-year basis"},
            {"file": C.F_BILL, "wrong_basis": False, "why_relevant": "the billing system's residential totals by office and month for the test year",
             "why_unused": "office totals of all residential schedules; no figure reads it", "ruled_out_by": "its own columns (billing office, class totals)"},
            {"file": C.F_EXCH, "wrong_basis": False, "why_relevant": "the meter exchanges behind the extract's split read periods",
             "why_unused": "the extract already carries both meters' rows under the service account", "ruled_out_by": "the extract's service_acct on both rows"},
        ],
        "stated_inputs": ["R-ON", "R-TOU", "R-1", "October 31, 2026", "December 31, 2027"],
        "field_terms": [],
    }
    json.dump(m, open(os.path.join(C.TASK, "metadata.json"), "w"), indent=1)
