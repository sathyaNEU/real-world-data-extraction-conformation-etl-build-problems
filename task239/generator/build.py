"""Write the task239 pack into a target folder and return the clean truth for the checks."""
import os

import docs
import records as RC
import sim

FILES = {
    "standard": "lfp_wi_sv03_measurement_standard_2027.pdf",
    "note": "lfp_staff_voice_2027_dashboard_methodology.docx",
    "close": "lfp_staff_voice_2027_fieldwork_closeout.docx",
    "codebook": "lfp_staff_voice_2027_codebook.xlsx",
    "sessions": "lfp_sv27_platform_sessions.csv",
    "answers": "lfp_sv27_platform_responses.csv",
    "paper": "lfp_sv27_paper_scans.csv",
    "packs": "lfp_sv27_paper_packs.csv",
    "register": "lfp_hr_team_register_2027-11-15.csv",
    "reorg": "lfp_hr_reorganisation_map_2027-09-01.csv",
    "tablets": "lfp_sv27_site_tablet_log.csv",
    "staff": "lfp_hr_staff_in_post_2027-09-01.csv",
    "items26": "lfp_sv26_dashboard_items.csv",
    "dict": "DATA_DICTIONARY.md",
    "readme": "README.md",
}
DISTRACTORS = ["staff", "items26"]


def run(target):
    os.makedirs(target, exist_ok=True)
    W = sim.make()
    R = RC.Records(W)
    p = lambda k: os.path.join(target, FILES[k])
    csv = lambda df, k: df.to_csv(p(k), index=False, lineterminator="\n")
    S, A = R.online_sessions(), R.online_answers()
    paper = R.paper()
    csv(S, "sessions")
    csv(A, "answers")
    csv(paper, "paper")
    csv(R.packs(), "packs")
    csv(R.register(), "register")
    csv(R.reorg_map(), "reorg")
    csv(R.tablet_log(), "tablets")
    staff = R.staff_in_post()
    csv(staff, "staff")
    csv(R.items_2026(), "items26")
    received = int((S["status"] == "submitted").sum() + len(paper))
    approx = dict(approx_returns="{:,}".format(int(round(received, -2))),
                  approx_rate="%d" % int(round(100.0 * received / staff["staff_in_post"].sum())))
    docs.standard(p("standard"))
    docs.dashboard_note(p("note"))
    docs.close_out(p("close"), approx)
    docs.codebook(p("codebook"))
    with open(p("dict"), "w") as fh:
        fh.write(docs.dictionary(FILES))
    with open(p("readme"), "w") as fh:
        fh.write(docs.readme(FILES))
    return dict(W=W, R=R, S=S, A=A, paper=paper, approx=approx)
