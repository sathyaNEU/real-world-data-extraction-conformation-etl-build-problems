"""Write the task239 pack into a target folder and return the clean truth for the checks."""
import os

import docs
import estim as E
import exports as XP
import plans as PL
import records as RC
import sim

FILES = {
    "standard": "lfp_wi_sv03_measurement_standard_2027.pdf",
    "note": "lfp_staff_voice_2027_dashboard_methodology.docx",
    "close": "lfp_staff_voice_2027_fieldwork_closeout.docx",
    "sessions": "lfp_sv27_platform_sessions.csv",
    "answers": "lfp_sv27_platform_responses.csv",
    "paper": "lfp_sv27_paper_scans.csv",
    "packs": "lfp_sv27_paper_packs.csv",
    "register": "lfp_hr_team_register_2027-11-15.csv",
    "reorg": "lfp_hr_reorganisation_map_2027-09-01.csv",
    "tablets": "lfp_sv27_site_tablet_log.csv",
    "plans": "lfp_sv27_dashboard_plans_2027-11-19.xlsx",
    "staff": "lfp_hr_staff_in_post_2027-09-01.csv",
    "items26": "lfp_sv26_dashboard_items.csv",
}
DISTRACTORS = ["staff", "items26"]
CALL_FILES = ["standard", "sessions", "answers", "paper", "packs", "register", "reorg", "tablets"]


def run(target):
    os.makedirs(target, exist_ok=True)
    W = sim.make()
    R = RC.Records(W)
    p = lambda k: os.path.join(target, FILES[k])
    csv = lambda df, k: df.to_csv(p(k), index=False, lineterminator="\n")
    S, A = R.online_sessions(), R.online_answers()
    paper = R.paper()
    csv(S, "sessions")
    csv(XP.platform(A), "answers")
    csv(XP.bureau(paper), "paper")
    csv(R.packs(), "packs")
    reg = R.register()
    csv(reg, "register")
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
    # the dashboard's team pages, made from the returns that count, and the plans team leaders set on them
    _, Rr, rep, _, _ = E.call(target, FILES)
    pages = PL.team_pages(Rr, rep)
    plans = PL.simulate(pages)
    PL.write(p("plans"), plans, pages, dict(zip(reg["team_code"], reg["team_name"])))
    return dict(W=W, R=R, S=S, A=A, paper=paper, approx=approx, pages=pages, plans=plans)
