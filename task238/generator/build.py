"""Write the task238 pack into a target folder and return the clean truth for the checks."""
import os

import docs
import records as RC
import sim

FILES = {
    "standard": "mso_ms14_tracker_continuity_standard.pdf",
    "plan": "mwt_cst27_plan.pdf",
    "close": "mwt_cst27_close_out.docx",
    "issued": "mwt_cst27_issued_addresses.csv",
    "web": "mwt_cst27_web_returns.csv",
    "cati": "mwt_cst27_cati_interviews.csv",
    "calls": "mwt_cst27_cati_call_records.csv",
    "codebook": "mwt_questionnaire_codebook_v9.xlsx",
    "published": "mwt_published_indexes_2019q1_2027q2.csv",
    "regions": "mso_regions_2027.csv",
    "dict": "DATA_DICTIONARY.md",
    "readme": "README.md",
}
DISTRACTORS = ["calls", "published"]
ISSUED_SALT = 4


def run(target):
    os.makedirs(target, exist_ok=True)
    W = sim.make()
    R = RC.Records(W)
    p = lambda k: os.path.join(target, FILES[k])
    csv = lambda df, k: df.to_csv(p(k), index=False, lineterminator="\n")
    issued = R.issued(ISSUED_SALT)
    web = R.web_export()
    cati = R.cati_export()
    csv(issued, "issued")
    csv(web, "web")
    csv(cati, "cati")
    csv(R.call_log(), "calls")
    csv(R.published(), "published")
    csv(R.regions(), "regions")
    a = web[(web["last_section"] == 6) & (web["opened_by"] == "respondent")]
    docs.standard(p("standard"))
    docs.plan(p("plan"))
    docs.close_out(p("close"), dict(sevenths="six"))
    docs.codebook(p("codebook"))
    with open(p("dict"), "w") as fh:
        fh.write(docs.dictionary(FILES))
    with open(p("readme"), "w") as fh:
        fh.write(docs.readme(FILES))
    return dict(W=W, R=R, issued=issued, web=web, cati=cati)
