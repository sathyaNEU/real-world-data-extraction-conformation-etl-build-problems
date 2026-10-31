"""submission.md and metadata.json, every figure emitted from figures.json."""
import json
import os

import pack as P
import world as W

NAME = {r[0]: r[2] for r in W.RU}
ALLOC = {r[0]: r[5] for r in W.RU}


def submission(fig, path):
    L = fig["loads_whole"]
    over = fig["call"]["over"]
    within = fig["call"]["within"]
    lines = ["## Tags", "",
             "**Domain:** Physical & Environmental Sciences (environmental monitoring and exceedance: a catchment "
             "agency's sulfate load allocations for coal-mine drainage).",
             "**Analytical objective:** Anomaly Detection & Diagnostics.", "",
             "## 1. Final Recommendation", "",
             "**Direct the mines of four resource units in 2027: Khambule (KH1), Mzimela at Ngwelezane Drift (MZ4), "
             "Ntsheketshe (NT1) and Nyathi at Mabhokweni (NY2); every other unit is within its allocation.**",
             "MZ4 and NY2 carried %d and %d t/d against allocations of %d and %d, although their boundary samples, "
             "taken on the bank the mine stream does not run along, read low. Not Mzimela at Esikhotheni (MZ2) or "
             "Nyathi at Siphethu (NY3), whose boundary samples sit in a mine stream's unmixed plume: their water "
             "carried %d and %d t/d against %d and %d." % (L["MZ4"], L["NY2"], ALLOC["MZ4"], ALLOC["NY2"],
                                                        L["MZ2"], L["NY3"], ALLOC["MZ2"], ALLOC["NY3"]), "",
             "## 2. Critical Components", "",
             "1. Over their allocations (May to September 2026 runs): KH1 **%d**, MZ4 **%d**, NT1 **%d** and NY2 "
             "**%d** t/d of sulfate." % (L["KH1"], L["MZ4"], L["NT1"], L["NY2"]),
             "2. MZ2 and NY3 carried **%d** and **%d** t/d, within %d and %d." % (L["MZ2"], L["NY3"], ALLOC["MZ2"],
                                                                                ALLOC["NY3"]),
             "3. The boundary samples at MZ2, MZ4, NY2 and NY3 do not balance with the loads their inflows carry "
             "in or with the next mixed weir downstream; each of those units' loads is what its inflows carry in.",
             "", "## 3. Step-by-Step Solution", "",
             "1. Kept each sample's reported sulfate (a re-run, suffix -R, replaces the first result) and each weir's "
             "daily mean flow, and took the routine runs from 1 May to 30 September 2026 (schedule section 3).",
             "2. Computed every unit's run load as boundary sulfate times boundary flow times 0.0864 and compared "
             "loads along each river with the register's upstream units.",
             "3. Found that at MZ2, MZ4, NY2 and NY3, the four weirs a short reach below a mine stream's "
             "confluence, the boundary load breaks the balance on every run, while the units above and the mixed "
             "weirs below balance.",
             "4. Took each unit's load as the sum of its inflows' loads, carried down from the headwater and "
             "mine-stream units measured at their own weirs, and averaged the season's runs.",
             "5. Compared each mean with Table 2 of the allocation schedule.",
             "6. Discharges: differenced each point's month-end totaliser readings (the latest return for a month "
             "stands; Silwane's February from the inspection's final reading), restated the November 2025 to "
             "September 2026 sulfate of the three mines whose laboratory reported it as S (x 2.996, their EC "
             "unchanged), and summed volume times composite by quarter.",
             "7. Loggers: SAST months, fouling drift removed linearly between service visits, telemetry gaps "
             "filled from the memory downloads, hours above each logger's trigger counted.", "",
             "## 4. Deliverable Answers", "", "### %s" % "sulfate_load_directives_2027.pdf", "",
             "1. Over their allocations, to be directed: %s." % ", ".join(over),
             "2. Within their allocations: %s." % ", ".join(within),
             "3. Bar chart of each unit's dry-season load against its allocation, the units over their allocations "
             "in red.", "",
             "### %s" % "umzimela_sulfate_loads_2025_26.xlsx", "",
             "1. Sulfate as SO4 discharged by each licensed point, tonnes to the nearest ten:"]
    pts = sorted({k.split()[0] for k in fig["ask_a_tonnes"]})
    for pt in pts:
        lines.append("   - %s: Q1 %s, Q2 %s, Q3 %s, Q4 %s" % tuple(
            [pt] + ["{:,}".format(fig["ask_a_tonnes"]["%s %s" % (pt, q)]) for q in ("Q1", "Q2", "Q3", "Q4")]))
    lines.append("2. Hours each logger read the river's EC above its trigger, whole hours, November 2025 to April 2026:")
    months = ["2025-11", "2025-12", "2026-01", "2026-02", "2026-03", "2026-04"]
    for lid, site in P.LOGGERS:
        lines.append("   - %s (trigger %d uS/cm): %s" % (lid, P.TRIGGERS[lid], ", ".join(
            "%s %d" % (m, fig["ask_b_hours"]["%s %s" % (lid, m)]) for m in months)))
    lines.append("3. Each unit's dry-season load, whole tonnes a day: %s." % ", ".join(
        "%s %d" % (c, L[c]) for c in [r[0] for r in W.RU]))
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")


def metadata(path):
    src = {"lab": "a catchment agency's laboratory results export, one row per analyte",
           "runs": "the field teams' routine sampling run log", "ec": "telemetry from continuous EC loggers",
           "service": "the loggers' service visit log", "memory": "the loggers' memory downloads for telemetry gaps",
           "gauges": "a gauging network's daily mean stage and flow", "register": "the monitoring network register",
           "schedule": "the agency's sulfate load allocation schedule",
           "returns": "mines' monthly water use licence discharge returns",
           "wul": "the water use licence register for mine discharges",
           "inspections": "the agency's compliance inspection log", "rain": "rain gauges' daily totals",
           "wtw": "a water treatment works' daily raw water log"}
    meta = {"task": "task125", "architecture": 3,
            "files": [{"name": P.FILES[k], "role": "distractor" if k in P.DISTRACTORS else "evidence",
                       "source": "synthetic: " + src[k], "license": "CC0 (synthetic, authored for this task)",
                       "date": "2026-10-09"} for k in P.FILES],
            "distractors": [P.FILES[k] for k in P.DISTRACTORS],
            "deliverables": ["sulfate_load_directives_2027.pdf", "umzimela_sulfate_loads_2025_26.xlsx"]}
    json.dump(meta, open(path, "w"), indent=1)
