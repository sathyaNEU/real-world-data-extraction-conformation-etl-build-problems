"""submission.md and figures.json, written from the computed answers (no figure is typed)."""
import json
import os
from datetime import datetime

import estim as E

MONTH = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
         "December"]


def day(s):
    d = datetime.strptime(s, "%Y-%m-%d %H:%M")
    return "%d %s" % (d.day, MONTH[d.month - 1])


def figures(A):
    rec = A["recs"]["delta"]
    pick, ok, cap = A["picks"]["delta"]
    f = {
        "call": E.NAMES[pick], "line": "%.2f" % A["line"], "runner_up": E.NAMES[ok[1]],
        "record": {E.NAMES[m]: {"incidents": rec[m]["incidents"], "none": rec[m]["none"]} for m in E.CHECKS},
        "experiments": len(A["inc"]) + len(A["none"]), "with_incident": len(A["inc"]), "without": len(A["none"]),
        "allowance": cap, "allowance_pct": "2", "level_pct": "1", "z": "2.576", "standard_installs": "10,000",
        "run_days": "14",
        "review": {t: {"flagged": A["review"][t][0], "never": A["review"][t][1]} for t in E.TYPES},
        "app_wide": {a["incident"]: {"gap": "{:,}".format(a["gap"]), "share": "%.2f" % a["share"],
                                     "sessions": "{:,}".format(a["sessions"]), "opened": day(a["opened"])}
                     for a in A["app_wide"]},
        "default_path": {"check": E.NAMES[A["picks"]["naive"][0]],
                         "record": {E.NAMES[m]: {"incidents": A["recs"]["naive"][m]["incidents"],
                                                 "none": A["recs"]["naive"][m]["none"]} for m in E.CHECKS},
                         "line": "%.2f" % A["line_naive_late"]},
        "per_install_mean": {"check": E.NAMES[A["picks"]["mor"][0]],
                             "record": {E.NAMES[m]: {"incidents": A["recs"]["mor"][m]["incidents"],
                                                     "none": A["recs"]["mor"][m]["none"]} for m in E.CHECKS}},
        "moved_most": E.NAMES[A["moved_most"]],
    }
    return f


def submission(A, f):
    rec = A["recs"]["delta"]
    pick, ok, cap = A["picks"]["delta"]
    run = ok[1]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Product Analytics (metric definition and measurement science).  ")
    L.append("**Analytical objective:** Data Quality Monitoring & Alerting.\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**The scorecard service should hold experiments on the gap-sessions check from January 2027, at a hold line "
             "of %s percentage points for a standard experiment.**\n" % f["line"])
    L.append("Tested at the install, the unit the platform assigns to arms, gap sessions would have held %d of the %d "
             "experiments of 2026 with a confirmed data incident and %d of the %d without one. Not late sessions, which "
             "holds %d and leads only when every session is treated as an independent draw, a test that understates the "
             "variance of the gap-session share and pushes that check over the allowance. Not duplicate sessions or the "
             "treatment share, %d each. Not events per install, which would have held %d experiments without an incident "
             "against an allowance of %d.\n"
             % (rec[pick]["incidents"], f["with_incident"], rec[pick]["none"], f["without"], rec[run]["incidents"],
                rec["dup"]["incidents"], rec["epu"]["none"], cap))
    L.append("## 2. Critical Components\n")
    L.append("1. Gap sessions would have held **%d** of the %d experiments with a confirmed data incident and **%d** of the "
             "%d without one." % (rec[pick]["incidents"], f["with_incident"], rec[pick]["none"], f["without"]))
    L.append("2. Late sessions, the next best check within the allowance, would have held **%d** of %d."
             % (rec[run]["incidents"], f["with_incident"]))
    L.append("3. Events per install would have held **%d** experiments without a confirmed incident, over the allowance "
             "of **%d** in %d." % (rec["epu"]["none"], cap, f["without"]))
    L.append("4. The hold line for a standard experiment (%s installs in each arm, %s days) is **%s** percentage points.\n"
             % (f["standard_installs"], f["run_days"], f["line"]))
    L.append("## 3. Step-by-Step Solution\n")
    steps = [
        "Labelled the %d experiments of 2026 from the incident register's confirmed experiment entries, matched to the "
        "registry by title: %d with a confirmed data incident, %d without one (withdrawn suspicions count as none)."
        % (f["experiments"], f["with_incident"], f["without"]),
        "Stacked install_summary_2026q1.csv, install_summary_2026q2.parquet and install_summary_2026q3.parquet, mapping "
        "service 1's columns and its arms A (control) and B (treatment) onto service 2's.",
        "Compared each experiment's arms on its full run at the two-sided %s per cent level in each check's hold "
        "direction (DH-3 section 4): each session share with its variance taken over installs, the unit DH-3 section 2 "
        "assigns to arms (delta method on per-install sums of the check's sessions and all sessions); events per install "
        "with Welch's t test; the treatment share against the registry's design share." % f["level_pct"],
        "Counted each check's holds over the %d experiments: gap sessions %d and %d, late sessions %d and %d, duplicate "
        "sessions %d and %d, treatment share %d and %d, events per install %d and %d (with a confirmed incident and "
        "without one)." % (f["experiments"], rec["gap"]["incidents"], rec["gap"]["none"], rec["late"]["incidents"],
                           rec["late"]["none"], rec["dup"]["incidents"], rec["dup"]["none"], rec["share"]["incidents"],
                           rec["share"]["none"], rec["epu"]["incidents"], rec["epu"]["none"]),
        "Applied DH-3 section 5: at most %s per cent of %d, so at most %d, rules out events per install; of the rest, gap "
        "sessions holds the most experiments with a confirmed incident." % (f["allowance_pct"], f["without"], cap),
        "Took the per-install variance of the gap-session share over both arms of the %d experiments without an "
        "incident and set the line at %s standard errors of the difference for %s installs an arm: %s percentage points."
        % (f["without"], f["z"], f["standard_installs"], f["line"]),
        "Weekly review: an incident counts as flagged when weekly_review_log_2026.csv holds any flag against its "
        "experiment, and each incident takes the cause established in reconciliation_summary_2026.pdf.",
        "App-wide incidents: took each incident's gap sessions once (data_incident_register_2026.xlsx repeats the "
        "incident's figure on every platform row) and divided by the sum of its rows' sessions in the window.",
    ]
    for i, s in enumerate(steps, start=1):
        L.append("%d. %s" % (i, s))
    L.append("")
    L.append("## 4. Deliverable Answers\n")
    L.append("### auto_hold_check_scorecard_2027.xlsx\n")
    L.append("1. The check and its line: %s, hold line %s percentage points for a standard experiment." % (f["call"], f["line"]))
    L.append("2. Experiments with a confirmed data incident each check would have held, of %d:" % f["with_incident"])
    for m in E.CHECKS:
        L.append("   - %s: %d" % (E.NAMES[m], rec[m]["incidents"]))
    L.append("3. The weekly review, by type of confirmed incident (flagged; never flagged):")
    for t in E.TYPES:
        L.append("   - %s: %d; %d" % (t.capitalize(), A["review"][t][0], A["review"][t][1]))
    L.append("4. Incidents the register logged against the whole app (gap sessions; share of the sessions in the window on "
             "the platforms hit):")
    for a in A["app_wide"]:
        g = f["app_wide"][a["incident"]]
        L.append("   - %s, opened %s: %s; %s per cent" % (a["incident"], g["opened"], g["gap"], g["share"]))
    L.append("")
    return "\n".join(L)


def write(task_dir, gen_dir, A):
    f = figures(A)
    with open(os.path.join(gen_dir, "figures.json"), "w") as fh:
        json.dump(f, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    with open(os.path.join(task_dir, "submission.md"), "w") as fh:
        fh.write(submission(A, f))
    return f
