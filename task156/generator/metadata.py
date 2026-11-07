"""metadata.json: the task's decision, deliverables, distractors and each file's provenance; never the method."""
import json
import os

import docs as D
import records as R

LICENCE = "Constructed for this task; no third-party data; free to use with the task."
PROV = {
    R.F_REG: "LSU Victoria Branch membership system: every member since 1 July 2019 with employer, worksite and dates, extract of 2 November 2026",
    R.F_INV: "The branch's online voting service: invitations and votes for the branch's online votes, March 2022 to October 2025",
    R.F_VOTES: "The branch's online voting service: the votes' titles and voting windows, 2022 to 2025",
    R.F_SITES: "LSU Victoria Branch worksite list with the codes in use before the July 2024 membership system migration, November 2026",
    R.F_DELEG: "LSU Victoria Branch delegate register: workplace delegates by term, 2018-20 to 2024-26, kept by the organising coordinator",
    R.F_RETURN: "LSU Victoria Branch returning officer's return of the July 2026 worksite delegate elections",
    R.F_ROUND: "LSU Victoria Branch 2027 bargaining round tracker, 31 October 2026",
    R.F_REMIT: "LSU Victoria Branch finance: council payroll remittance advices for union dues received July 2025 to July 2026",
    R.F_DIARY: "LSU Victoria Branch organisers' shared calendar export, July 2025 to June 2026",
    R.F_SIGNIN: "LSU Victoria Branch regional delegates' forum sign-in sheets, 2025-26",
    R.F_WORKFORCE: "Councils' workforce returns to the branch under the agreements' information clauses, 30 June 2026",
    R.F_SURVEY: "LSU Victoria Branch member survey, September 2024: results by council",
    D.F_PAB21: "Tallyhouse Ballot Services Pty Ltd, declarations of protected action ballot results, 2021 round",
    D.F_PAB24: "Tallyhouse Ballot Services Pty Ltd, declarations of protected action ballot results, 2023-24 round",
    D.F_GUIDE: "LSU Victoria Branch, Protected action ballots: a guide for branch officials, March 2025",
    D.F_FINANCE: "LSU Victoria Branch, Dues and remittances: finance procedure FP-04, revised July 2025",
    D.F_BUREAU: "Western Shires Payroll Services, statements of union deductions by client council, 2025-26",
}
DISTRACTORS = [R.F_WORKFORCE, R.F_SURVEY]


def write(task_dir, n=None):
    files = []
    for f in sorted(os.listdir(os.path.join(task_dir, "target"))):
        files.append(dict(file="target/" + f, source=PROV[f], licence=LICENCE, rows=(n or {}).get(f)))
    meta = dict(
        task="task156",
        decision="The councils in the 2027 bargaining round at which the branch applies for protected action ballot "
                 "orders, for ballots opening 1 March 2027, a ballot authorising action only if half the roll votes",
        deliverables=["pab_2027_turnout_forecast.xlsx", "pab_2027_recommendation_bcom.docx"],
        domain="political-science-public-policy", objective="forecasting",
        distractor_files=["target/" + f for f in DISTRACTORS],
        as_of="2026-11-03", files=files)
    json.dump(meta, open(os.path.join(task_dir, "metadata.json"), "w"), indent=1)
