"""task231 architecture 2: submission.md and metadata.json, written from the golden figures."""
import json

import analysis as A
import params as P

WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine"}


def _st(r):
    return "%s %s" % (r["site"], r["name"])


def submission(fig, rows, path):
    ret = [r for r in rows if r["retune"]]
    m = fig["method"]
    L = []
    L += ["## Tags", "",
          "**Domain:** Physical & Environmental Sciences (sensor calibration and measurement: a highway district's "
          "road weather stations and its vendor's automated air temperature quality control).",
          "**Analytical objective:** Data Quality Monitoring & Alerting.", ""]
    L += ["## 1. Final Recommendation", "",
          "**Yes. The data quality standard sends %s stations back to Quillan for a re-tuned air temperature spatial "
          "test before winter 2027/28: %s.**" % (WORD[len(ret)], ", ".join(_st(r) for r in ret)),
          "Their false-rejection shares were %s per cent of the winter's %s hours, against the standard's line of "
          "2 per cent; the highest of the other stations was %s per cent. At the basin floors the test withheld the cold "
          "pools' air on still nights, and at the three grades above the pools it withheld right readings because "
          "its estimate leaned on the cold floor stations nearby. Checked against an hourly lapse line or the HRRR "
          "forecast, the floor readings look wrong and only the three grades go on the list." % (
              ", ".join("%s" % r["share_s"] for r in ret), fig["winter_hours_s"], fig["highest_below"]), ""]
    floors = fig["pool_groups"]
    L += ["## 2. Critical Components", "",
          "1. A withheld reading is right when it agrees within %s C with the stations sharing its air that hour: "
          "a basin floor with its pool mates (%s), any other station with the free-atmosphere stations within "
          "%s km carried to its elevation at %s C per km." % (m["tau"], "; ".join(floors), m["fa_km"], m["lapse"]),
          "2. The cold floor readings the test withheld agree with their pool mates, so they count as false "
          "rejections: %s." % ", ".join("%s %s" % (r["site"], r["share_s"]) for r in ret if r["floor"]),
          "3. The grades above the pools agree with the free atmosphere around them: %s." % ", ".join(
              "%s %s" % (r["site"], r["share_s"]) for r in ret if not r["floor"]),
          "4. Withheld readings that were wrong and stay withheld: %s." % ", ".join(
              "%s %s (%s hours withheld, %s right)" % (r["site"], r["fault"], r["withheld"], r["fr"])
              for r in fig["faulted"]),
          "5. The lapse-line route (each hour's elevation fit, within 5 C) re-tunes only %s." % ", ".join(
              fig["r2_sites"]), ""]
    L += ["## 3. Step-by-Step Solution", "",
          "1. Joined the ESS export (tenths of a degree C, UTC hour-end stamps, RPU ids, re-sent rows kept once) to "
          "the site register and took the QC log's spatial-test air temperature rows, one per station and hour.",
          "2. Each hour fitted the free-atmosphere line of temperature on elevation, refitted without stations more "
          "than %s C below it." % m["below_line"],
          "3. Grouped the stations sharing a cold pool: night residuals from that line correlated above %s on the "
          "hours both readings passed the QC, within %s km and %s m of each other, both below the line on an "
          "average night." % (m["corr"], m["group_km"], m["group_m"]),
          "4. Judged each withheld reading against the median of its pool mates, or of the free-atmosphere "
          "stations within %s km carried to its elevation at %s C per km; right within %s C, and every tolerance "
          "from %s to %s C gives the same hours." % (m["fa_km"], m["lapse"], m["tau"], m["tau_lo"], m["tau_hi"]),
          "5. Share = right withheld hours / %s winter hours; re-tune above 2 per cent." % fig["winter_hours_s"],
          "6. Unavailable hours: the message log's modems to sites through the modem register with removed modems "
          "kept and the unregistered spare placed at %s by the export's observations, local times with their zone "
          "to UTC, each message's hours first to last, the earliest receipt within %s minutes of the hour's end "
          "available, hours inside a notified outage excluded." % (fig["spare_site"], m["grace_min"]),
          "7. Freezing and ice hours: the pavement export with re-sent rows once, travel-lane ports only, each "
          "serial's model (replaced sensors from the register's notes) for its units, the firmware %s code table "
          "from each serial's applied time and %s before it and for SCAN-16 sensors." % (m["fw_new"], m["fw_old"]),
          ""]
    L += ["## 4. Deliverable Answers", "", "### %s" % P.DELIVERABLES[1], "",
          "1. Re-tune the spatial test before winter 2027/28 at: %s." % ", ".join(_st(r) for r in ret),
          "2. Chart: every station's false-rejection share against the 2 per cent line, the re-tuned stations "
          "marked.", "", "### %s" % P.DELIVERABLES[0], "",
          "1. False-rejection share of winter hours (per cent) and re-tune:",
          "   - " + "; ".join("%s %s%s" % (r["site"], r["share_s"], " re-tune" if r["retune"] else "")
                              for r in rows),
          "2. Unavailable hours under Schedule B: " + "; ".join("%s %s" % (r["site"], r["unavailable"]) for r in rows)
          + ".",
          "3. Travel-lane freezing hours: " + "; ".join("%s %s" % (r["site"], r["freezing_s"]) for r in rows) + ".",
          "4. Travel-lane ice hours: " + "; ".join("%s %s" % (r["site"], r["ice"]) for r in rows) + ".", ""]
    open(path, "w", encoding="utf-8").write("\n".join(L))


FILES = [
    ("feed", "evidence", "synthetic: the District's ESS atmospheric export, one row per observation delivered", "2027-05-12"),
    ("qc", "evidence", "synthetic: the vendor's QC withheld log for the District's network", "2027-05-04"),
    ("register", "evidence", "synthetic: the District's RWIS site register with pavement sensors and firmware",
     "2027-05-11"),
    ("standard", "governing", "synthetic: the District's RWIS data quality standard, Revision 2", "2026-08-28"),
    ("qcconfig", "governing", "synthetic: the vendor's air temperature QC configuration document", "2027-01-13"),
    ("sla", "governing", "synthetic: Schedule B (service levels) of the operations and data services agreement",
     "2025-06-27"),
    ("messages", "evidence", "synthetic: the central server's message log", "2027-05-03"),
    ("modems", "evidence", "synthetic: the District's cellular modem register", "2027-04-28"),
    ("outages", "evidence", "synthetic: the District's planned outage notices to the vendor", "2027-04-22"),
    ("pavement", "evidence", "synthetic: the pavement sensor export, as the RPUs report it", "2027-05-12"),
    ("preseason", "evidence", "synthetic: the October 2026 pre-season air temperature checks", "2026-10-02"),
    ("nwp", "distractor", "synthetic: HRRR 2 m temperature point forecasts at the District's sites", "2027-05-02"),
    ("traffic", "distractor", "synthetic: automatic traffic recorder daily volumes, calendar 2026", "2027-01-09"),
    ("email", "voice", "synthetic: the program manager's review request", "2027-05-18"),
]


def metadata(path):
    m = {"task": "task231", "architecture": 2, "setting": P.SETTING.isoformat(),
         "files": [{"name": P.FILES[k], "role": role, "source": src, "date": d,
                    "license": "CC0 1.0 (synthetic, authored for this task)"} for k, role, src, d in FILES],
         "distractors": [
             {"name": P.FILES["nwp"], "why_unused": "a model forecast of the air, not a measurement of it; it "
              "carries little of the basins' cold pools, so it cannot say whether a station's reading was right"},
             {"name": P.FILES["traffic"], "why_unused": "traffic volumes bear on where ice matters, not on whether "
              "the test withheld a right reading or on the service and pavement hours asked"}],
         "deliverables": list(P.DELIVERABLES)}
    json.dump(m, open(path, "w"), indent=1)
    open(path, "a").write("\n")


def enrich(fig, rows, S):
    """the figures the write-up cites beyond the deliverables' own, from the same solve"""
    M, reg = S["M"], S["reg"]
    tagof = {P.SITE[t]: t for t in P.TAGS}
    groups, seen = [], set()
    for i, g in M["G"].items():
        if g and i not in seen:
            members = sorted({i, *g})
            seen.update(members)
            groups.append(", ".join(reg["sites"][k]["name"] for k in members))
    fig["pool_groups"] = groups
    floor_idx = {i for i, g in M["G"].items() if g}
    faults = {"R3": "rime", "R5": "rime", "L3": "connector", "T1": "radiation shield", "Q3": "wet filter"}
    fig["faulted"] = []
    for k, s in enumerate(reg["sites"]):
        t = tagof[s["site"]]
        if t in faults:
            fig["faulted"].append({"site": s["site"], "fault": faults[t], "withheld": int(M["withheld"][k]),
                                   "fr": int(M["fr"][k])})
    R = A.rungs(M, S["target"])
    fig["r2_sites"] = [reg["sites"][k]["site"] for k in A.retune(R["R2 hourly lapse refit within 5 C"])]
    fig["rungs"] = {k: [reg["sites"][x]["site"] for x in A.retune(v)] for k, v in R.items()}
    fig["spare_site"] = "%s %s" % (reg["sites"][list(S["A"]["placed"].values())[0]]["site"],
                                   reg["sites"][list(S["A"]["placed"].values())[0]]["name"])
    fig["method"] = {"tau": "2", "tau_lo": "1.5", "tau_hi": "4.5", "below_line": "1.5", "corr": "0.8",
                     "group_km": "25", "group_m": "80", "fa_km": "50", "lapse": "6.5", "grace_min": "20",
                     "fw_new": "4.1", "fw_old": "3.4", "lapse_tol": "5"}
    for r in rows:
        k = reg["idx"][r["site"]]
        r["floor"] = k in floor_idx
        r["share_s"] = "%.1f" % r["share"]
        r["freezing_s"] = "{:,}".format(r["freezing"])
    return fig
