"""task464 architecture 12: metadata.json, written from the built pack so it never drifts from it."""
import json
import os

import world as W

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QW = W.BOARD_LTD

FILES = [
    ("sponsored_clicks_by_mailbox_daily.csv", "spine",
     "Quaywork's data warehouse: sponsored clicks per day by mailbox group, audience and channel, with the "
     "jobseekers in each audience, 1 January 2025 to 8 November 2026.", "%s, data warehouse extract" % QW, "2026-11-09"),
    ("postvane_daily_by_domain_group.csv", "operating extract",
     "Postvane's daily campaign statistics by domain group from the March 2025 migration: job alerts, the weekly "
     "digest and the restart pilot's sends.", "%s, email platform export (Postvane)" % QW, "2026-11-09"),
    ("inkrelay_export_2025-01-01_to_2025-03-16.csv", "operating extract",
     "The previous email platform's daily statistics by ISP up to the migration.",
     "%s, email platform export (Inkrelay)" % QW, "2025-03-17"),
    ("postvane_clicks_restart_series_2026.csv", "operating extract",
     "Postvane's click events on the six restart emails of 2026, timed in UTC.",
     "%s, email platform export (Postvane)" % QW,
     "2026-11-09"),
    ("alert_restarts_pilot_pool_2026.csv", "operating extract",
     "The alert system's restart log for the jobseekers in the 2026 restart pilot's pool, from 1 April 2026, on the "
     "UK clock.",
     "%s, alerts service log" % QW, "2026-11-09"),
    ("restarted_jobseekers_sponsored_clicks.csv", "operating extract",
     "The CRM team's pull of every sponsored click by jobseekers whose alerts a restart email's link restarted, "
     "from the date of that send to 8 November 2026, on the UK clock.", "%s, CRM team" % QW, "2026-11-10"),
    ("jobseeker_email_plan_2027.docx", "governing document",
     "The 2027 jobseeker email plan, draft for the leadership team.", "%s, Jobseeker Engagement" % QW, "2026-11-16"),
    ("restart_pilot_brief_2026.pdf", "governing document", "The restart pilot's design brief.",
     "%s, CRM team" % QW, "2026-03-16"),
    ("crm_send_calendar_2026.xlsx", "reference", "The CRM team's calendar of 2026 email sends.",
     "%s, CRM team" % QW, "2026-11-12"),
    ("crm_mailbox_domain_groups.csv", "reference",
     "The CRM team's table of email domains by mailbox group in each system.", "%s, CRM team" % QW, "2026-02-03"),
    ("sponsored_revenue_by_sector_2026.xlsx", "distractor",
     "Finance's month-end view of sponsored clicks and revenue by job sector, January to October 2026.",
     "%s, Finance" % QW, "2026-11-06"),
    ("alerts_feedback_survey_2026-06.csv", "distractor",
     "Responses to the June 2026 survey of jobseekers who paused or unsubscribed from alerts.",
     "%s, Insight team" % QW, "2026-06-30"),
]


def main():
    f = json.load(open(os.path.join(BASE, "generator", "figures.json")))
    names = sorted(os.listdir(os.path.join(BASE, "target")))
    listed = sorted(n for n, *_ in FILES)
    assert names == listed, (names, listed)
    meta = {
        "task": "task464",
        "domain": "product-analytics",
        "subdomain": "churn-propensity-uplift-modeling",
        "objective": "opportunity-sizing-decision",
        "prompt_shape": "09",
        "as_of": W.ASOF.isoformat(),
        "extract_to": W.END.isoformat(),
        "currency": "GBP",
        "compiled_by": QW,
        "compiled_on": "2026-11-24",
        "licence": ("Synthetic records compiled for %s's 2027 jobseeker email plan. Every file is constructed, "
                    "describes no real company or person, and is released for this task's use." % W.BOARD),
        "files": [{"path": "target/" + n, "role": role, "covers": cov, "source": src, "date": d,
                   "licence": "synthetic, constructed for this task, free to use"}
                  for n, role, cov, src, d in FILES],
        "distractor_files": ["target/sponsored_revenue_by_sector_2026.xlsx", "target/alerts_feedback_survey_2026-06.csv"],
        "deliverables": ["restart_series_2027.xlsx", "restart_series_2027.docx"],
        "portal": {"call": "whether the restart-your-alerts email stays in the 2027 jobseeker email plan",
                   "answer": "drop the series"},
    }
    json.dump(meta, open(os.path.join(BASE, "metadata.json"), "w"), indent=2)
    print("  metadata.json, %d files" % len(FILES))


if __name__ == "__main__":
    main()
