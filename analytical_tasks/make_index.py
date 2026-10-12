"""Number every unbuilt analytical-task seed, objective by objective, and write the root START_HERE.md.

Writes, from the repo root:
  START_HERE.md                                 the task-number index by lane: task, seed, call (linked to the
                                                seed note), domain. No status column: status lives in each
                                                build's pipeline.json and is printed by build-pipeline/status.py.
  analytical_tasks/08_data_quality_monitoring/  only with --dq: the DQ seed notes, their README and index rows

No task folder is written. A folder is created by /build at intake, so the repo holds real builds only.
Numbers are fixed by FIRST, BLOCK_ORDER and BUILT, so a re-run never renumbers.

  python3 analytical_tasks/make_index.py              # rewrite the root START_HERE.md
  python3 analytical_tasks/make_index.py --dry-run    # print the numbering and write nothing
"""
import csv
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AT = os.path.join(ROOT, "analytical_tasks")
INDEX = os.path.join(AT, "index.csv")
FIRST = 132

# Seeds already realised by a build (the fingerprint card's "Realises analytical_tasks note").
BUILT = {
    "FC01": "task117", "FC02": "task124", "AD01": "task119", "AD02": "task125", "DA01": "task120",
    "DA02": "task126", "OS01": "task118", "OS02": "task127", "DS01": "task122", "DS02": "task128",
    "RC01": "task121", "RC02": "task129", "ET01": "task123",
}

# (block key, Axis 1 objective, seed prefixes, default owner)
BLOCK_ORDER = [
    ("forecasting", "Forecasting & Predictive Modeling", ["FC"], "sathya8571"),
    ("anomaly", "Anomaly Detection & Diagnostics", ["AD"], "oviya13ya"),
    ("dqm", "Data Quality Monitoring & Alerting", ["DQ"], "perssathya"),
    ("descriptive", "Descriptive & Distribution Analysis", ["DA"], "sathay3012"),
    ("opportunity", "Opportunity Sizing & Decision Support", ["OS", "DS"], "unassigned"),
    ("rootcause", "Root-Cause Analysis", ["RC"], "unassigned"),
    ("etl", "Data Extraction & Conformation (ETL)", ["ET"], "oviya1301"),
]

DQ_FRAME = ("The object under analysis is the health of the data or of the pipeline that delivers it, and the "
            "committed call is a monitoring or alerting decision (what fires, what is flagged, held, reissued or "
            "escalated), forward facing by default. If the prompt could be retagged Anomaly Detection, Descriptive "
            "or Forecasting without changing a word, the tag fails.")

# id, client domain, task type, pattern id, layer2 family, title, pitfall, shortcut, pin, call
DQ_SEEDS = [
    ("DQ01", "product-analytics", "metric-definition-measurement-science", "product-analytics/metric-definition-measurement-science/1", "estimation_fit",
     "Which guardrail metric the experiment platform's automated alert watches",
     "A candidate alert metric is scored on past launches with known outcomes: how often it detects a real regression and agrees in direction, against its own variance. The metric that moved most is usually the noisiest.",
     "Pick the candidate with the largest percent movement across past launches.",
     "A labelled set of past launches with known regressions, and the alert standard naming sensitivity at a stated false-alert rate as the criterion.",
     "The metric the platform's auto-alert is wired to for next quarter, with its threshold."),
    ("DQ02", "product-analytics", "metric-definition-measurement-science", "product-analytics/metric-definition-measurement-science/2", "estimation_fit",
     "Whether the release-health alert fires on this week's build, when the metric is the average user's rate",
     "A per-user rate and a pooled ratio answer different questions, and a pooled ratio is carried by heavy users. The alert metric follows the stated unit of analysis, and its control limits follow from that choice.",
     "Divide total crashes by total sessions for the build and compare with the pooled limit.",
     "The release-health standard defines the metric on the average user, with its limit method.",
     "Fire or hold the release-health alert for each build in the current train."),
    ("DQ03", "product-analytics", "metric-definition-measurement-science", "product-analytics/metric-definition-measurement-science/3", "estimand_identification",
     "Whether an event-volume drop is an instrumentation incident or a mix shift toward a new client version",
     "A topline events-per-user metric can fall while every client segment is flat, because the user mix moved toward a low-baseline client. Decompose into within-segment rate and composition before calling an instrumentation loss.",
     "Read the topline drop as lost events and open the incident.",
     "Segment sizes and rates are filed for both periods, and the incident policy defines an instrumentation loss as a within-segment fall.",
     "Which of the monitored event streams get an instrumentation incident opened this week."),
    ("DQ04", "general-statistics-data-science", "missing-data-censoring-measurement-error", "general-statistics-data-science/missing-data-censoring-measurement-error/1", "estimation_fit",
     "Whether the network-total shortfall alert fires when the missing reads are multiply imputed",
     "Multiply imputed totals are pooled with Rubin's rules, within and between imputation variance added. Averaging the imputations into one file and testing once understates the variance and fires the alert too often.",
     "Average the imputed reads into one dataset and test the total against the tolerance once.",
     "The pipeline ships every imputation, and the alert standard defines the test on the pooled estimate and its variance.",
     "Which reporting zones raise a shortfall alert for the closing period."),
    ("DQ05", "general-statistics-data-science", "missing-data-censoring-measurement-error", "general-statistics-data-science/missing-data-censoring-measurement-error/2", "estimation_fit",
     "The upstream-lag threshold for a feed SLA alert, when lag is itself measured with error",
     "Random error in a covariate attenuates its slope toward zero. Setting an alert on upstream lag from a naive regression of downstream error on measured lag understates how much lag matters and puts the threshold too high.",
     "Treat the logged lag as exact and read the threshold off the naive fit.",
     "Replicate lag measurements give the error variance, and the SLA standard sets the threshold at a stated downstream error rate.",
     "The lag threshold at which the feed SLA alert pages, per feed."),
    ("DQ06", "general-statistics-data-science", "missing-data-censoring-measurement-error", "general-statistics-data-science/missing-data-censoring-measurement-error/3", "estimation_fit",
     "Whether a register statistic keeps its quality flag when the missing field may not be missing at random",
     "Imputation assumes missing at random. A tipping-point analysis shifts imputed values by stated offsets and finds the shift that breaks the quality tolerance; agreement between complete-case and imputed results is not robustness.",
     "Compare complete-case and imputed figures and call the statistic robust when they agree.",
     "The quality framework names the delta grid and the tolerance the published statistic must hold.",
     "Publish with the standard flag, publish with a caution flag, or suppress, for each statistic in the release."),
    ("DQ07", "epidemiology-public-health", "disease-surveillance-outbreak-anomaly-detection", "epidemiology-public-health/disease-surveillance-outbreak-anomaly-detection/1", "forecast_uncertainty",
     "Which laboratory feeds get a volume-drop alert, against the seasonal baseline",
     "Incoming report volume moves with the season. The expected count comes from the same weeks in prior seasons with trend, past anomalies downweighted; comparing with recent weeks flags a normal seasonal fall as a feed failure.",
     "Compare this week's volume with the mean of the last four weeks.",
     "The feed-monitoring standard names the baseline method and the number of prior seasons, and the alert threshold.",
     "Which feeds are escalated to the laboratory liaison this week."),
    ("DQ08", "epidemiology-public-health", "disease-surveillance-outbreak-anomaly-detection", "epidemiology-public-health/disease-surveillance-outbreak-anomaly-detection/2", "forecast_uncertainty",
     "Which reporting areas get a completeness alert, when recent weeks are still filling in",
     "Notifications arrive with delay, so the latest weeks are undercounted in every area. Completeness is judged against what the empirical delay distribution says should have arrived by now, not against final counts.",
     "Flag every area whose latest weeks sit below the area's usual weekly count.",
     "Report dates are in the extract so the delay distribution is estimable, and the completeness standard defines the expected share received by each lag.",
     "Which areas receive a completeness alert in this week's run."),
    ("DQ09", "epidemiology-public-health", "disease-surveillance-outbreak-anomaly-detection", "epidemiology-public-health/disease-surveillance-outbreak-anomaly-detection/3", "estimand_identification",
     "Whether a step in the case series is flagged as a series break caused by testing volume",
     "Counts rise when testing rises, for example when a new laboratory joins the network. A series break is diagnosed on tests performed and positivity, not on raw counts.",
     "Treat the step in confirmed cases as real and publish it unflagged.",
     "The stream carries tests performed, and the publication standard defines a series break on testing effort.",
     "Which series carry a break flag in the next publication."),
    ("DQ10", "psychology-behavioral-science", "psychometric-measurement-scale-validation", "psychology-behavioral-science/psychometric-measurement-scale-validation/1", "field_method",
     "Whether a translated questionnaire passes the release gate on reliability",
     "Alpha assumes equal loadings and says nothing about dimensionality. The gate is model-based reliability, omega from the fitted congeneric structure.",
     "Report alpha above the cutoff and pass the version.",
     "The release standard names omega under a congeneric model as the gate, with its threshold.",
     "Release, hold or rework each language version in the wave."),
    ("DQ11", "psychology-behavioral-science", "psychometric-measurement-scale-validation", "psychology-behavioral-science/psychometric-measurement-scale-validation/2", "field_method",
     "Whether a new survey mode's data can be pooled into the tracker",
     "Five-point items are ordinal. Invariance across modes is tested with polychoric correlations and a categorical estimator; Pearson-based ML fit attenuates loadings and misjudges invariance.",
     "Run ML CFA on Pearson correlations of the items and compare fit by mode.",
     "Items are filed as ordinal, and the tracker's quality standard names the categorical estimator and the invariance criterion.",
     "Pool, pool with a mode adjustment flag, or keep the mode separate, for each tracked index."),
    ("DQ12", "psychology-behavioral-science", "psychometric-measurement-scale-validation", "psychology-behavioral-science/psychometric-measurement-scale-validation/3", "field_method",
     "Which items leave a dashboard index after the structure check",
     "The eigenvalue-over-one rule keeps too many factors, which changes which items cross-load and which get dropped. Parallel analysis sets the factor count before any item decision.",
     "Keep every factor with an eigenvalue above one and drop cross-loaders from that solution.",
     "The production QA standard names parallel analysis and the item-retention rule.",
     "The list of items that stay in the index for the next cycle."),
    ("DQ13", "survey-research-official-statistics", "nonresponse-calibration-measurement-error-adjustment", "survey-research-official-statistics/nonresponse-calibration-measurement-error-adjustment/1", "field_method",
     "Whether this wave's estimate trips the weighting-pipeline quality alert",
     "Nonresponse adjustment is computed within the named weighting cells on base weights. One overall unweighted factor leaves differential nonresponse in the estimate and moves it across the alert band.",
     "Inflate every respondent weight by the inverse of the overall unweighted response rate.",
     "The weighting specification names the cells and the base-weighted adjustment; the alert band is filed.",
     "Which published domains are flagged in this wave's quality report."),
    ("DQ14", "survey-research-official-statistics", "nonresponse-calibration-measurement-error-adjustment", "survey-research-official-statistics/nonresponse-calibration-measurement-error-adjustment/2", "field_method",
     "Which domain estimates fail the calibration margin check and are reissued",
     "Raking cycles through every margin until all match within tolerance. One pass matches only the last margin, so earlier margins and the domain estimates built on them drift.",
     "Treat one ratio pass per margin as calibrated.",
     "Marginal control totals for several variables and a stated convergence tolerance are filed.",
     "The reissue list for the release."),
    ("DQ15", "survey-research-official-statistics", "nonresponse-calibration-measurement-error-adjustment", "survey-research-official-statistics/nonresponse-calibration-measurement-error-adjustment/3", "estimation_fit",
     "Whether an item's published prevalence carries a misclassification flag",
     "With sensitivity and specificity from a record check, the corrected proportion is (p + Sp - 1) / (Se + Sp - 1). Ignoring false positives, or dividing by sensitivity alone, badly biases a rare trait.",
     "Report the observed proportion, or divide it by sensitivity alone.",
     "The record-check study gives both error rates, and the quality standard sets the tolerance between published and corrected figures.",
     "Which items are flagged in the next release."),
    ("DQ16", "survey-research-official-statistics", "census-register-administrative-data-quality", "survey-research-official-statistics/census-register-administrative-data-quality/1", "field_method",
     "Which local areas' register counts breach the undercoverage alert",
     "Dual-system estimates are computed within post-strata where capture is homogeneous, after removing erroneous enumerations. A pooled Lincoln-Petersen estimate carries correlation bias and counts duplicates.",
     "One pooled estimate from raw register and survey counts.",
     "Matched counts and erroneous enumeration rates by post-stratum are filed, and the alert defines net undercoverage.",
     "The areas flagged for the register-improvement programme."),
    ("DQ17", "survey-research-official-statistics", "census-register-administrative-data-quality", "survey-research-official-statistics/census-register-administrative-data-quality/2", "estimand_identification",
     "Which coding categories trip the reinterview quality alert",
     "Net difference rate measures bias in a category's total; gross difference rate measures how many units are misclassified. Offsetting errors make net small while gross is large.",
     "Report the net change in category totals as the misclassification rate.",
     "The quality standard defines the alert on the gross rate, or on the net rate, and says which.",
     "The categories sent back to coding review."),
    ("DQ18", "physical-environmental-sciences", "environmental-monitoring-exceedance", "own:data-capture-before-exceedance", "field_method",
     "Which monitoring sites' annual compliance statistic is reportable",
     "A daily or annual statistic is valid only when the data capture rule is met (a stated share of valid hours per day, of valid days per quarter). Counting exceedances over whatever readings arrived biases the compliance figure and hides gaps.",
     "Count exceedances and compute annual means over the readings that exist.",
     "The network's QA standard states the capture thresholds and the averaging periods.",
     "Report, report with a data-capture flag, or withhold, for each site."),
    ("DQ19", "physical-environmental-sciences", "environmental-monitoring-exceedance", "own:standard-averaging-period-alerts", "field_method",
     "How many public alerts the network should have issued, and the alert configuration that follows",
     "An exceedance is assessed on the standard's averaging period and rounding rule (a rolling 8-hour mean, a 24-hour mean), not on hourly values. Alerts configured on hourly readings over-fire.",
     "Count hours above the limit value as exceedances.",
     "The standard names the averaging period, the data rule for a valid average and the reporting rounding.",
     "The corrected alert configuration and next season's expected alert count per site."),
    ("DQ20", "physical-environmental-sciences", "environmental-monitoring-exceedance", "own:alert-scored-on-ratified-data", "forecast_uncertainty",
     "Whether the provisional-data alert rule is kept, retuned or retired",
     "Alerts run on provisional data, and ratification later applies calibration corrections. An alert rule's hit and false-alarm rates are scored against ratified concentrations, aligned on the episode the alert claimed.",
     "Score the rule against the provisional stream it ran on.",
     "Ratified datasets are published with their ratification dates, and the alert policy states the target hit and false-alarm rates.",
     "Keep, retune (with the new threshold) or retire the rule for next season."),
    ("DQ21", "physical-environmental-sciences", "environmental-monitoring-exceedance", "own:episodes-not-hours", "estimation_fit",
     "How many alert episodes the duty desk should plan for",
     "Consecutive exceedance hours are one episode under the alert policy's gap rule. Treating hours as independent events inflates alert volume and the desk's staffing need.",
     "Count exceedance hours, or per-hour alerts, as events.",
     "The alert policy defines an episode and the question asks episodes per site per season.",
     "The desk rota for next season, sized on episodes."),
    ("DQ22", "physical-environmental-sciences", "sensor-calibration-measurement", "own:calibration-direction", "estimation_fit",
     "Which low-cost sensors fail the drift tolerance and are pulled for recalibration",
     "A sensor is calibrated by regressing its reading on the co-located reference (the known value) and inverting; regressing the reference on the sensor gives a different correction and a different drift verdict.",
     "Regress the reference on the sensor reading and apply that line as the correction.",
     "The calibration protocol names the reference as the known value and the drift tolerance on the corrected scale.",
     "The pull list for the next maintenance round."),
    ("DQ23", "physical-environmental-sciences", "sensor-calibration-measurement", "own:network-false-alarm-budget", "forecast_uncertainty",
     "The per-station drift-alert threshold that meets the network's false-alert budget",
     "A two-sigma rule at every one of many stations fires several false alerts a week. The threshold is set for the network: a stated false-alert budget per month across all stations, from the stations' in-control behaviour.",
     "Apply a per-station two-sigma rule.",
     "The operations standard states the acceptable false alerts per month across the network.",
     "The threshold, and the expected alerts per month it produces."),
    ("DQ24", "physical-environmental-sciences", "sensor-calibration-measurement", "own:errors-in-both-instruments", "estimation_fit",
     "Which instruments' calibration factor breaches tolerance when both instruments are noisy",
     "When the comparison instrument also has measurement error, the OLS slope between the two is attenuated. An errors-in-variables fit (Deming with the known error ratio) gives the calibration factor.",
     "Use the OLS slope of one instrument on the other as the factor.",
     "Both instruments' precision is filed from repeatability tests, and the protocol calls for an errors-in-variables fit.",
     "The instruments flagged for recalibration."),
    ("DQ25", "physical-environmental-sciences", "sensor-calibration-measurement", "own:detection-limit-censoring", "estimation_fit",
     "Which low-level channels trip the drift alert when readings sit below the detection limit",
     "Readings below the limit of detection are censored. Substituting half the limit biases the channel mean and its drift; a censored-data estimator gives the level the alert compares.",
     "Substitute LOD/2 for censored readings and compute the mean.",
     "The laboratory flags censored readings and the alert standard defines the level on the censored-data estimator.",
     "The channels escalated to the laboratory this quarter."),
]



def clean(s):
    s = s.replace(" — ", ", ").replace("—", ", ")
    return s


def slug(s, n=60):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:n].rstrip("-")


def write_dq():
    d = os.path.join(AT, "08_data_quality_monitoring")
    os.makedirs(d, exist_ok=True)
    rows = []
    for (i, dom, tt, pat, fam, title, pit, short, pin, call) in DQ_SEEDS:
        fn = "%s_%s.md" % (i, slug(title, 55))
        body = (
            "# %s, %s\n\n"
            "| Field | Value |\n|---|---|\n"
            "| Objective | Data Quality Monitoring & Alerting |\n"
            "| Client domain / task type | `%s` / `%s` |\n"
            "| Layer 2 pattern | `%s` |\n"
            "| Layer 2 family | `%s` |\n"
            "| Committed call | %s |\n\n"
            "## The pitfall\n\n%s\n\n"
            "## The tempting shortcut\n\n%s\n\n"
            "## What pins the rigorous method\n\n%s\n\n"
            "## Making it a monitoring task\n\n%s\n\n"
            "## Layer 1\n\nDraw the data work from `.claude/skills/dataset-generation/references/layer1-messiness.md` "
            "(the universal techniques and the domain's own): the pipeline's deliveries, check results, incident register "
            "and alert routing beside what was published, every piece of mess something the real system would produce.\n"
        ) % (i, title, dom, tt, pat, fam, call, pit, short, pin, DQ_FRAME)
        open(os.path.join(d, fn), "w").write(body)
        rows.append((i, title, fn, dom, tt, pat, fam, call, pit))
    lines = ["# Data Quality Monitoring & Alerting: %d tasks (DQ01 to DQ%02d)\n" % (len(rows), len(rows)),
             "Seeds for the objective the other seven folders do not cover. Each pairs a client task type that serves "
             "Data Quality Monitoring (`.claude/skills/fingerprint/vocab.json`) with one Layer 2 pattern: seventeen from "
             "`.claude/skills/stumping/references/client/layer2-rigor-patterns.md`, eight `own:` patterns for the "
             "physical and environmental task types the library does not cover. Patterns, not scenarios: the build "
             "makes its own setting and data.\n",
             "| ID | Call | Client domain / task type | Pattern |", "|---|---|---|---|"]
    for (i, title, fn, dom, tt, pat, fam, call, pit) in rows:
        lines.append("| %s | [%s](%s) | %s / %s | `%s` |" % (i, title, fn, dom, tt, pat))
    open(os.path.join(d, "README.md"), "w").write("\n".join(lines) + "\n")
    # index rows, appended once
    with open(INDEX, newline="") as f:
        r = list(csv.reader(f))
    head, have = r[0], {x[0] for x in r[1:]}
    add = []
    for (i, title, fn, dom, tt, pat, fam, call, pit) in rows:
        if i in have:
            continue
        row = dict.fromkeys(head, "")
        row.update(id=i, category="Data Quality Monitoring & Alerting", title=title,
                   file="analytical_tasks/08_data_quality_monitoring/" + fn,
                   objective="Data Quality Monitoring & Alerting", domain="%s · %s" % (dom, tt),
                   committed_call=call, driving_force=pit, technique=pat)
        add.append([row[h] for h in head])
    if add:
        with open(INDEX, "a", newline="") as f:
            csv.writer(f).writerows(add)


def seeds():
    with open(INDEX, newline="") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def numbering(idx):
    out, n = [], FIRST
    for key, obj, prefixes, owner in BLOCK_ORDER:
        for p in prefixes:
            for sid in sorted(k for k in idx if k.startswith(p)):
                if sid in BUILT:
                    continue
                out.append(("task%d" % n, sid, key, obj, owner))
                n += 1
    return out


def demote(md):
    out, fence = [], False
    for line in md.split("\n"):
        if line.startswith("```"):
            fence = not fence
        out.append("#" + line if (not fence and line.startswith("#")) else line)
    return "\n".join(out)


def read_root_state(path):
    state = {}
    if not os.path.exists(path):
        return state
    for line in open(path):
        m = re.match(r"\| (task\d+) \| (\w+) \|[^|]*\|[^|]*\| ([^|]*) \| ([^|]*) \|$", line.strip())
        if m:
            state[m.group(1)] = (m.group(3).strip(), m.group(4).strip())
    return state


FIELDS = ["title", "objective", "domain", "mirrors", "decision_shape", "committed_call", "gap_pattern",
          "gate_g_mechanism", "measured_traps_engaged", "calibration_form", "driving_force", "technique", "trap", "sources"]


def start_here(task, sid, obj, owner, block, row):
    lo, hi = block
    note = clean(open(os.path.join(ROOT, row["file"])).read())
    fields = "\n".join("- **%s:** %s" % (k, clean(row[k])) for k in FIELDS if row.get(k))
    return (
        "# %s: start here\n\n"
        "| | |\n|---|---|\n"
        "| Task | %s |\n"
        "| Objective (Axis 1) | %s |\n"
        "| Block | %s to %s |\n"
        "| Lane owner | %s (current owner and status: the root `START_HERE.md` on main) |\n"
        "| Seed | %s, `%s` |\n\n"
        "## Before you build\n\n"
        "1. This file is the seed, not the design. Build with `/build` (`build-pipeline`) from stage 0; the design "
        "goes in `DESIGN_NOTE.md`, and this file is not edited once the build starts.\n"
        "2. Keep the objective and the number. If `guard.py` blocks the seed's driver or pairing, redraw inside the "
        "same objective and keep `%s`.\n"
        "3. Seeds in folders 01 to 07 were written before the client's two-layer standard. Their calibration corpus, "
        "twin pair, licensed wrong basis, colleague voices and withheld rule are idea material, never a build plan. "
        "Re-root the stump as a Layer 2 analytical pitfall (`stumping` Part 2, "
        "`stumping/references/client/layer2-rigor-patterns.md`) and keep Layer 1 to realistic mess "
        "(`dataset-generation/references/layer1-messiness.md`). `official_decoy` and `validated_decoy` are blocked.\n"
        "4. A seed that names a house domain gets the client domain it sits in on its card "
        "(`guide-to-prompt/references/domains/README.md`).\n"
        "5. Branch under your prefix (`.claude/authors/`), `<prefix>/%s-<slug>`, and set the task's Status in the "
        "root `START_HERE.md` on main when you start and when you ship.\n\n"
        "## Seed index fields\n\n%s\n\n"
        "## Seed note\n\n%s"
    ) % (task, task, obj, lo, hi, owner, sid, row["file"], task, task, fields, demote(note))


def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="print the numbering and write nothing")
    ap.add_argument("--dq", action="store_true", help="also rewrite the DQ seed notes from DQ_SEEDS")
    a = ap.parse_args(argv)
    if a.dq and not a.dry_run:
        write_dq()
    idx = seeds()
    plan = numbering(idx)
    blocks = {}
    for t, sid, key, obj, owner in plan:
        blocks.setdefault(key, []).append(t)
    if a.dry_run:
        print("dry run: %d task numbers, %s to %s; START_HERE.md not written" % (len(plan), plan[0][0], plan[-1][0]))
        return 0
    L = ["# Start here: task numbers by lane", "",
         "Every unbuilt seed in `analytical_tasks/` has a fixed task number, numbered objective by objective. "
         "A developer works the lane (block) assigned in their `.claude/authors/<handle>.md`, two builds at a time, "
         "lowest open number first, and starts one with `/build taskNN`. The folder is created at intake. "
         "Status is never edited here: it lives in `taskNN/pipeline.json`, and "
         "`python3 .claude/skills/build-pipeline/status.py` prints the board (`status.py taskNN` prints one seed).", "",
         "A seed is an idea, not a design: keep its world, decision and quantity, and re-find the pitfall from the data "
         "(`stumping`). Read only the seed's header table and its Situation section. If the guard blocks a seed's "
         "driver, redraw inside the same objective and keep the number.", "",
         "Seeds already built (not renumbered): " + ", ".join("%s as %s" % (k, v) for k, v in sorted(BUILT.items())) + ". "
         "Experiment & Causal Analysis has no seed block yet.", "",
         "Regenerate with `python3 analytical_tasks/make_index.py`; numbers never move.", "",
         "| Objective | Tasks | Count | Lane owner |", "|---|---|---|---|"]
    for key, obj, prefixes, owner in BLOCK_ORDER:
        b = blocks.get(key, [])
        if b:
            L.append("| %s | %s to %s | %d | %s |" % (obj, b[0], b[-1], len(b), owner))
    for key, obj, prefixes, owner in BLOCK_ORDER:
        b = blocks.get(key, [])
        if not b:
            continue
        L += ["", "## %s (%s to %s)" % (obj, b[0], b[-1]), "",
              "| Task | Seed | Call | Domain |", "|---|---|---|---|"]
        for t, sid, k, o, ow in plan:
            if k != key:
                continue
            row = idx[sid]
            title = clean(row["title"]).replace("|", "/")
            dom = clean(row["domain"]).replace("|", "/")
            L.append("| %s | %s | [%s](%s) | %s |" % (t, sid, title, row["file"], dom))
    open(os.path.join(ROOT, "START_HERE.md"), "w").write("\n".join(L) + "\n")
    print("START_HERE.md: %d task numbers, %s to %s" % (len(plan), plan[0][0], plan[-1][0]))


if __name__ == "__main__":
    main()
