"""Answers, figures.json and submission.md for task237, drafted from the analysis so no figure is typed."""
import json
import os

import estim as E
import golden as GD
import params as P

FILES = None
SHORT = {"pa": "Punjabi", "zh-Hans": "Mandarin", "yue": "Cantonese", "tl": "Tagalog", "ar": "Arabic", "es": "Spanish",
         "ur": "Urdu", "vi": "Vietnamese", "fa": "Persian", "ko": "Korean"}


def _and(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def f2(v):
    return "%.2f" % E.round_half(v, 2)


def answers(X, files):
    global FILES
    FILES = files
    rows = []
    for v in E.ORDER:
        r = X["rel"][v]
        rows.append(dict(code=v, language=X["language"][v], short=SHORT[v], vendor=X["vendor"][v], mode=X["mode"][v],
                         decision=X["calls"][v], completes=int(X["counts"][v]), mean=float(X["means"][v]),
                         mean_raw=float(X["means_raw"][v]), alpha=float(r["alpha"]), share=float(r["golden"]),
                         one=float(r["one_factor"]), common=float(r["common"]), pos=float(r["positive_only"]),
                         n_full=int(r["n"]), wording=X["wording"][v]["p"] < 1e-3, fit=X["wording"][v]))
    by = {r["code"]: r for r in rows}
    dec = {d: [r for r in rows if r["decision"] == d] for d in ("release", "hold", "rework")}
    alpha_calls = {r["code"]: E.band(r["alpha"]) for r in rows}
    return dict(versions=rows, by=by, dec=dec, counts={d: len(x) for d, x in dec.items()},
                alpha_release=sum(1 for c in alpha_calls.values() if c == "release"), alpha_calls=alpha_calls,
                entries=X["entries"], interviews=X["interviews"])


def figures(A):
    rows = A["versions"]
    wf = [r for r in rows if r["wording"]]
    alpha_wrong = [r for r in rows if A["alpha_calls"][r["code"]] != r["decision"]]
    pos_wrong = [r for r in rows if E.band(r["pos"]) != r["decision"]]
    online = [r for r in rows if r["vendor"] == P.VENDORS["NCP"][0]]
    capi = [r for r in rows if r["vendor"] != P.VENDORS["NCP"][0]]
    return {
        "call": {d: [r["language"] for r in x] for d, x in A["dec"].items()},
        "components": {
            "wording_factor_versions": [r["language"] for r in wf],
            "single_factor_versions": [r["language"] for r in rows if not r["wording"]],
            "trait_share_band": {r["language"]: r["decision"] for r in rows},
        },
        "rivals": {
            "alpha": {r["language"]: f2(r["alpha"]) for r in rows},
            "alpha_wrong": [r["language"] for r in alpha_wrong],
            "alpha_release_count": A["alpha_release"],
            "alpha_range_released_wrongly": [f2(min(r["alpha"] for r in alpha_wrong if A["alpha_calls"][r["code"]] == "release")),
                                             f2(max(r["alpha"] for r in alpha_wrong if A["alpha_calls"][r["code"]] == "release"))],
            "positive_items_only_wrong": [r["language"] for r in pos_wrong],
        },
        "steps": {"online_entries": A["entries"], "capi_interviews": A["interviews"],
                  "online_valid": sum(r["completes"] for r in online), "capi_valid": sum(r["completes"] for r in capi),
                  "full_answerers_range": [min(r["n_full"] for r in rows), max(r["n_full"] for r in rows)]},
        "deliverables": {GD.CSV: [{"version": r["code"], "decision": r["decision"], "valid_pilot_completes": r["completes"],
                                   "pilot_mean_score": "%.2f" % r["mean"]} for r in rows]},
        "bands": ["0.70", "0.80"], "items": [12, 6], "scale_range": [12, 60], "prorate": [1, 2, 3], "age": 18,
        "versions": len(rows), "counts": A["counts"], "wave": P.WAVE, "codes": [9, -8, -9],
        "items_reversed": ["02", "04", "06", "08", "10", "12"], "decimals": 2,
    }


def submission(A):
    rows = A["versions"]
    dec = A["dec"]
    by = A["by"]
    wf = [r for r in rows if r["wording"]]
    one = [r for r in rows if not r["wording"]]
    alpha_wrong = [r for r in rows if A["alpha_calls"][r["code"]] != r["decision"]]
    up = [r for r in alpha_wrong if A["alpha_calls"][r["code"]] == "release"]
    held = [r for r in alpha_wrong if A["alpha_calls"][r["code"]] == "hold"]
    pos_rel = [r for r in rows if E.band(r["pos"]) == "release" and r["decision"] != "release"]
    pos_hold = [r for r in rows if E.band(r["pos"]) == "hold" and r["decision"] == "release"]
    under7 = [r for r in wf if r["decision"] == "rework"]
    F = FILES
    n = lambda xs: _and(r["short"] for r in xs)
    L = []
    L.append("# task237 submission\n")
    L.append("## Tags\n")
    L.append("**Domain:** Psychology & Behavioral Science (psychometric measurement and scale validation: the release gate "
             "for a survey scale's new language versions, each judged on the share of its pilot score's variance due to "
             "the trait it measures).")
    L.append("**Analytical objective:** Data Quality Monitoring & Alerting (whether each translated version's pilot data "
             "measure connectedness reliably enough to field in wave 6).\n")
    L.append("## 1. Final Recommendation\n")
    L.append("**Release the %s versions of the BCS-12 for the wave 6 fieldwork, hold the %s versions for cognitive "
             "interviews and a second pilot, and send the %s versions back for retranslation.**\n" %
             (n(dec["release"]), n(dec["hold"]), n(dec["rework"])))
    L.append("In the %s versions the six negatively worded items share a wording factor of their own, and with it "
             "separated the trait's share of the total score's variance is under 0.80 in all six and under 0.70 in the "
             "%s versions; the Urdu version is under 0.70 with no wording factor, and the %s versions are 0.80 or more. Not "
             "Cronbach's alpha, which at %s to %s would release the %s versions and hold the Cantonese one, because it "
             "counts the wording factor's variance as connectedness. Not omega from a single factor, which files the same "
             "decisions. Not omega total from the model with the wording factor, which still counts that factor's "
             "variance. Not the positively worded items alone, which release the %s versions and hold the %s one.\n" %
             (n(wf), n(under7), n(dec["release"]), f2(min(r["alpha"] for r in up)), f2(max(r["alpha"] for r in up)), n(up),
              n(pos_rel), n(pos_hold)))
    L.append("## 2. Critical Components\n")
    L.append("1. In the %s versions the six negatively worded items share a **wording factor** besides connectedness; in "
             "the %s versions they share none." % (n(wf), n(one)))
    L.append("2. The trait's share of total-score variance with the wording factor separated: **0.80 or more** in the %s "
             "versions, **0.70 to under 0.80** in the %s versions, **under 0.70** in the %s versions." %
             (n(dec["release"]), n(dec["hold"]), n(dec["rework"])))
    L.append("")
    L.append("## 3. Step-by-Step Solution\n")
    L.append("1. Built each online version's valid completes from %s under TAS-4 section 4 (%s): respondents 18 or older "
             "whose entry started within the version's pilot dates in %s in Eastern time, who reached the end of the "
             "BCS-12 module (no item blank, status complete or partial) still in the version, counted once per panel "
             "member at their first valid complete with the accounts %s shows merged taken as one member: %s valid "
             "completes across the six online versions." %
             (F["online"], F["std"], F["reg"], F["ledger"], format(sum(r["completes"] for r in rows if r["vendor"] == P.VENDORS["NCP"][0]), ",")))
    L.append("2. Built each interviewer-administered version's valid completes from %s: interviews within the version's "
             "pilot dates that reached BCS12, less those %s reports not confirmed for the interviewer whose interview was "
             "checked (a reissued case's later interview stays): %s across the four versions." %
             (F["capi"], F["bc"], format(sum(r["completes"] for r in rows if r["vendor"] != P.VENDORS["NCP"][0]), ",")))
    L.append("3. Scored the items under section 5 (BCS02, BCS04, BCS06, BCS08, BCS10 and BCS12 reversed; 9, -8 and -9 "
             "unanswered; one or two unanswered items prorated) and took each version's mean total score, from %s "
             "(%s) to %s (%s)." % ("%.2f" % min(r["mean"] for r in rows), min(rows, key=lambda r: r["mean"])["short"],
                                    "%.2f" % max(r["mean"] for r in rows), max(rows, key=lambda r: r["mean"])["short"]))
    L.append("4. Took the covariance of the twelve item scores over each version's valid completes who answered all twelve "
             "items (section 6), %d to %d respondents per version." %
             (min(r["n_full"] for r in rows), max(r["n_full"] for r in rows)))
    L.append("5. Fitted a single factor and a bifactor model (connectedness on all twelve items, a wording factor on the "
             "six negatively worded items) by maximum likelihood: the wording factor improves on the single factor in the "
             "%s versions and adds nothing in the %s versions." % (n(wf), n(one)))
    L.append("6. Took the trait's share of the total score's variance from the bifactor model (omega hierarchical: "
             "connectedness's loadings summed and squared over the total score's model variance) and compared it "
             "unrounded with the bands at 0.80 and 0.70: %s at 0.80 or more, %s from 0.70 to under 0.80, %s under 0.70." %
             (n(dec["release"]), n(dec["hold"]), n(dec["rework"])))
    L.append("7. Filed the decisions with each version's valid pilot completes and pilot mean score, and charted alpha and "
             "the trait's share for each version against the bands.\n")
    L.append("## 4. Deliverable Answers\n")
    L.append("### %s\n" % GD.CSV)
    L.append("1. One row per version in the translation register's order, valid pilot completes whole, pilot mean score "
             "to two decimals:")
    for r in rows:
        L.append("   - %s (%s): %s, %s valid pilot completes, pilot mean score %s" %
                 (r["language"], r["code"], r["decision"], format(r["completes"], ","), "%.2f" % r["mean"]))
    L.append("")
    L.append("### %s\n" % GD.PNG)
    L.append("2. Each version's reliability, the trait's share of its score variance, against the rework, hold and release "
             "bands at 0.70 and 0.80, coloured by decision.")
    return "\n".join(L) + "\n"


def write(task_dir, gen_dir, A):
    fig = figures(A)
    with open(os.path.join(gen_dir, "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1)
        fh.write("\n")
    with open(os.path.join(task_dir, "submission.md"), "w") as fh:
        fh.write(submission(A))
    return fig
