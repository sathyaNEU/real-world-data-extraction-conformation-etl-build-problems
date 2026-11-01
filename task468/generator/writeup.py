"""task468 architecture 6: figures.json, submission.md and metadata.json, every figure from the solved pack."""
import json

import golden as GD

SOURCES = {
    "lims_old": "synthetic: a water utility laboratory's legacy LIMS export of trade waste results, January 2025 to "
                "February 2026, local times",
    "lims_new": "synthetic: the laboratory's LabWare export of trade waste results from February 2026, UTC",
    "telemetry": "synthetic: hourly cumulative register reads of the trade waste flow meters, UTC",
    "register": "synthetic: the trade waste agreements register with each agreement's COD limit",
    "policy": "synthetic: the utility's trade waste policy, version 4",
    "lab_notice": "synthetic: the laboratory's notice of the move from COD to TOC",
    "crosswalk": "synthetic: the legacy site codes to LabWare sampling points",
    "jobs": "synthetic: the field service job log with the meter exchanges",
    "request": "synthetic: the Trade Waste Manager's request email",
    "rain": "synthetic: daily rainfall at the utility's gauge",
    "returns": "synthetic: customers' quarterly production returns",
    "inspections": "synthetic: the trade waste officers' inspection visits",
    "receival": "synthetic: the treatment plant's liquid waste receival station log",
    "manifests": "synthetic: the state waste tracking system's manifests for loads delivered to the plant",
}
TYPE_NAMES = {"GT": "grease trap waste", "SE": "septage", "PL": "portable toilet waste", "LL": "landfill leachate"}
WHY = {"rain": "rainfall says how wet the catchment was, not what a customer discharged through its meter",
       "returns": "production returns are the customers' own activity figures; the policy measures mass from the "
                  "utility's meters and samples"}


def figures(R):
    custs = R["D"]["custs"]
    return {"over": R["over"],
            "verdict": {c: ("over" if c in R["over"] else "within") for c in custs},
            "ask_a": {t: [int(round(x)) for x in R["liquid"][t]] for t in R["liquid"]},
            "ask_b": {c: "%.1f" % R["ss"][c] for c in custs},
            "cod_t_shown": {c: round(R["cod"][c], 1) for c in custs},
            "limit_t": {c: R["D"]["limit"][c] for c in custs},
            "fit": [round(float(x), 4) for x in R["fit"]], "n_parallel": R["n_parallel"],
            "stated": {"ss_reporting_limit": 5, "ss_below_limit_counts_at": 2.5,
                       "chloride_per_mg_2dp": round(float(R["fit"][2]), 2), "toc_per_mg_1dp": round(float(R["fit"][1]), 1),
                       "second_pass_window_hours": 2}}


def t(x):
    return "{:,}".format(x)


def submission(fig, path):
    S = GD.SHORT
    over = [S[c] for c in fig["over"]]
    within = [S[c] for c in fig["verdict"] if fig["verdict"][c] == "within"]
    L = ["## Tags", "",
         "**Domain:** Physical & Environmental Sciences (emissions inventory: a water utility's releases to sewer, "
         "trade waste chemical oxygen demand on the agreements' reference method).",
         "**Analytical objective:** Data Extraction & Conformation (ETL).", "",
         "## 1. Final Recommendation", "",
         "**%s exceeded their agreements' 2026 COD limits and go on the annual return with a notice of agreement "
         "review; no other customer did.**" % (", ".join(over[:-1]) + " and " + over[-1]),
         "The dichromate COD the agreements limit also reads chloride, which TOC does not, so each 2026 TOC sample is "
         "converted on its own chloride; Mt Edwin Cheese's chloride fell after its brine recovery started in May and "
         "Tallowood Tannery's rose from March, so the ratios their 2025 parallel samples carried misstate both.", "",
         "## 2. Critical Components", "",
         "1. The COD equivalent of a TOC sample carries the sample's chloride: fitted on the parallel samples, COD "
         "rises **about 0.23 mg/L per mg/L of chloride** beside about 2.8 per mg/L of TOC.",
         "2. Customers over their limits: **%s**." % ", ".join(over),
         "3. Within their limits: %s." % ", ".join(within), "",
         "## 3. Step-by-Step Solution", "",
         "1. Laboratory: the legacy LIMS (local times, site codes through the crosswalk) and LabWare (UTC to "
         "Queensland time, point identifiers), duplicates (-D) dropped, re-issued results (-R) replacing the "
         "originals, suspended solids below 5 mg/L at 2.5.",
         "2. Conversion: COD regressed on TOC and chloride over the samples tested both ways in October to December "
         "2025, with a constant, applied to each 2026 TOC sample with its own chloride.",
         "3. Volume: each meter's hourly register read in Queensland time over the local year; across an exchange "
         "the removed meter to its final read and the installed meter from its opening read, both from the field "
         "job log.",
         "4. Mass: the year's volume times the volume-weighted mean concentration of the year's compliance samples "
         "(24-hour composites; the inspection grabs, which carry suspended solids and pH only, are not compliance "
         "samples), each weighted by its day's metered volume, January on the measured COD.",
         "5. Exceedance: each COD mass against the register's limit (kilograms read as such).",
         "6. Tankered waste: accepted receival dockets of 2026 by local receival date, each docket's waste code from "
         "the manifest that carries it, a second pass of a load (the same truck within two hours, no manifest of its "
         "own) taking the code of the pass before it.", "",
         "## 4. Deliverable Answers", "",
         "### %s" % GD.MEMO, "",
         "1. Customers that exceeded their 2026 COD limit: %s." % ", ".join(over),
         "2. Customers within their limit: %s." % ", ".join(within),
         "3. Chart of each customer's 2026 COD mass as a share of its limit, the exceeders marked.", "",
         "### %s" % GD.BOOK, "",
         "1. Tankered liquid waste received at the treatment plant by quarter of 2026, kL:"]
    for c in fig["ask_a"]:
        q = fig["ask_a"][c]
        L.append("   - %s: Q1 %s, Q2 %s, Q3 %s, Q4 %s" % ((TYPE_NAMES[c],) + tuple(t(x) for x in q)))
    L.append("2. Suspended solids discharged in 2026, t:")
    L.append("   - " + "; ".join("%s %s" % (S[c], fig["ask_b"][c]) for c in fig["ask_b"]))
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")


def metadata(path, files, distractors):
    out = {"task": "task468", "architecture": 6, "setting": "2027-01-12",
           "files": sorted([{"name": n, "role": "distractor" if k in distractors else "evidence",
                             "source": SOURCES[k], "date": "2027-01-12",
                             "license": "CC0 1.0 (synthetic, authored for this task)"} for k, n in files.items()],
                           key=lambda f: f["name"]),
           "distractors": [files[k] for k in distractors],
           "distractor_reasons": {files[k]: WHY[k] for k in distractors},
           "deliverables": [GD.MEMO, GD.BOOK]}
    json.dump(out, open(path, "w"), indent=1)
