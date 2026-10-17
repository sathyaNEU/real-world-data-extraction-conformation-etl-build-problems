"""Every assertion the generator makes about the pack it just cut."""
import datetime as dt
import json
import os
import re

import pandas as pd

import golden as G
import sim
import world as W

N = [0]


def A(cond, msg):
    N[0] += 1
    if not cond:
        raise AssertionError(msg)


def doc_text(target, name):
    from pypdf import PdfReader
    t = " ".join(p.extract_text() or "" for p in PdfReader(os.path.join(target, name)).pages)
    return re.sub(r"\s+", " ", t)


def run(target):
    N[0] = 0
    g = G.compute(target)
    (panel, rollup, register, maint, health, edge, commit, amend,
     sessions, rebuf, inc, res, releases) = G.load(target)
    fw = doc_text(target, "network_capacity_framework.pdf")
    std = doc_text(target, "delivered_quality_standard.pdf")
    dic = doc_text(target, "telemetry_dictionary.pdf")
    task = os.path.dirname(os.path.abspath(target.rstrip("/")))
    meta = json.load(open(os.path.join(task, "metadata.json"), encoding="utf-8"))
    kept, every = G.shortfalls(rollup, register, maint)
    q = "2027Q1"
    this = kept[kept["reporting_quarter"] == q]

    # ---- the call ------------------------------------------------------------------------------
    A(g["fund"] == "none", "the call is not the hold")
    A(g["decided_shortfall"] < g["record_shortfall"],
      "the quarter's worst window is not inside the record")
    A(g["record_shortfall"] / g["decided_shortfall"] >= 1.06,
      "the record stands only %.1f per cent above the quarter's worst window"
      % (100 * (g["record_shortfall"] / g["decided_shortfall"] - 1)))
    A(g["rank_of_nine"] == 4, "the quarter's worst window ranks %d of nine" % g["rank_of_nine"])
    A(len(g["quarterly_worst"]) == 8, "the record holds %d earlier quarters"
      % len(g["quarterly_worst"]))
    A(float(g["decided_shortfall"]).is_integer(), "the decided shortfall is not a whole kbps")

    # ---- the three rules, executed ---------------------------------------------------------------
    # R1 the easy route on the pack's own rows files the named wrong answer, and the decisive step
    # alone files the golden
    A(g["rung0_port"] != g["fund"] and g["rung0_shortfall"] > g["record_shortfall"],
      "R1 keeping the booked evenings does not file a confident wrong fund")
    A(g["decided_port"] != g["rung0_port"], "R1 the booked evenings change nothing")
    A(g["rung2_port"] not in (g["decided_port"], g["rung0_port"]),
      "R1 the quarter mean names a path another rung already names")
    A(g["rung2_mean"] / g["rung2_next"] >= 1.06,
      "R1 the quarter mean is a coin flip between two paths")
    own = g["own_99th"][g["decided_port"]]
    A(g["decided_shortfall"] / own >= 1.06,
      "R1 the worst window does not clear its own path's record, so rung 1 is not a confident fund")
    # R2 nothing in the pack names a selection, a maximum of maxima, a tempo or a correction
    blob = ""
    for f in sorted(os.listdir(target)):
        if f.endswith(".pdf"):
            blob += " " + doc_text(target, f)
        elif f.endswith((".csv", ".json")):
            blob += " " + open(os.path.join(target, f), encoding="utf-8", errors="ignore").read()
    low = re.sub(r"\s+", " ", blob).lower()
    for banned in ("multiple testing", "selective", "selection", "multiplicity", "family wise",
                   "familywise", "bonferroni", "maximum of", "worst of", "false discovery",
                   "null distribution", "per comparison", "look elsewhere"):
        A(banned not in low, "R2 a shipped file says '%s'" % banned)
    # R3 no shipped artifact ranks the interconnects on the decision question
    for f in sorted(os.listdir(target)):
        if f.endswith(".pdf"):
            t = doc_text(target, f).lower()
            for w in ("ranked", "ranking", "league", "scorecard", "worst performing",
                      "most congested"):
                A(w not in t, "R3 %s says '%s'" % (f, w))
    A("not broken down by interconnect" in doc_text(
        target, "published_quarterly_quality_report.pdf"),
      "R3 the published report does not say it carries no interconnect breakdown")

    # ---- the semantic fork table -----------------------------------------------------------------
    # SF1 the interconnect: the renamed port is one interconnect
    nm = G.port_now(register)
    A(W.RENAMED[0] in nm and nm[W.RENAMED[0]] == W.RENAMED[1],
      "SF1 the renamed port does not resolve to the interconnect in service")
    A(len(set(nm.values())) == len(W.PATHS), "SF1 the register resolves to %d interconnects"
      % len(set(nm.values())))
    A((rollup["port_code"] == W.RENAMED[0]).any() and (rollup["port_code"] == W.RENAMED[1]).any(),
      "SF1 the record carries only one of the two codes")
    # SF2 the evening windows, filed
    A("19:00 to 19:59, 20:00 to 20:59 and 21:00 to 21:59, each in local time" in fw,
      "SF2 clause 4.3 does not file the three windows")
    for win in ("19:00", "20:00", "21:00"):
        s = this[this["window_from"] == win]
        A(float(s["shortfall"].max()) <= g["record_shortfall"],
          "SF2 the %s window on its own would fund an augment" % win)
    # SF3 the shortfall's sign and basis, filed
    A("less the median of the evening window" in std, "SF3 the standard does not file the shortfall")
    A("The reference band is 12:00 to 14:59 local time" in std, "SF3 the reference band is not filed")
    # SF4 the clock: the windows are local and the stamps are UTC, both filed
    A("in UTC" in dic and "summer time on the last Sunday in March" in dic,
      "SF4 the dictionary does not file the clock")
    A("each in local time" in fw, "SF4 the framework does not file the windows as local")
    # the rollup already carries local evenings, so the two readings of the panel converge on it
    A(set(rollup["window_from"]) == {"19:00", "20:00", "21:00"},
      "SF4 the rollup's windows are not the framework's")
    # SF7 the booked evenings, filed, and they are the only ones dropped
    A("is not evidence of congestion there, and the planning desk leaves those evenings out" in fw,
      "SF7 clause 4.4 is not filed")
    A(len(every) - len(kept) == 9 * len(W.WINDOWS),
      "SF7 %d window rows were dropped, not the nine evenings' worth" % (len(every) - len(kept)))
    # SF8 the quarter, filed
    A("the reporting quarters are the calendar quarters" in fw, "SF8 clause 4.1 is not filed")
    A(set(this["evening_date_local"].str[:7]) == {"2027-01", "2027-02", "2027-03"},
      "SF8 the quarter's evenings are not the calendar quarter's")
    # SF11 ties: the nine quarterly worst windows are distinct
    vals = list(g["quarterly_worst"].values()) + [int(g["decided_shortfall"])]
    A(len(set(vals)) == 9, "SF11 two quarters share a worst window")
    # SF12 the flag: there is no flag file in this build, and no artifact scores a path
    A(not any("flag" in f for f in os.listdir(target)), "SF12 the pack ships a flag file")
    # SF5 every interconnect is in service across the whole quarter
    A(set(this["line"]) == set(nm.values()), "SF5 an interconnect is missing from the quarter")

    # SF6 a usable evening: a collector loss takes a whole band, so every band the panel holds is
    # whole and no completeness rule can select a different set of evenings
    p = panel.copy()
    p["t"] = pd.to_datetime(p["measured_at_utc"].str[:19])
    off = p["t"].dt.date.map(lambda x: 2 if x >= W.DST_SPRING else 1)
    p["lh"] = (p["t"] + pd.to_timedelta(off, unit="h")).dt.hour
    p["lday"] = (p["t"] + pd.to_timedelta(off, unit="h")).dt.date.astype(str)
    p["band"] = ["evening" if h >= W.EVENING_BAND[0] else "day" for h in p["lh"]]
    sizes = p.groupby(["port_code", "lday", "band"]).size()
    A(set(sizes) == {180}, "SF6 a band in the panel is not whole: sizes %s" % sorted(set(sizes)))
    A(int(health["minutes_missing"].astype(int).sum()) % 180 == 0,
      "SF6 the collector lost part of a band")
    # SF9 worst: clause 4.2 files the largest shortfall, and ranking on the lowest evening bitrate
    # names a different interconnect
    A("the largest any interconnect in service at the quarter end shows in any evening window" in fw,
      "SF9 clause 4.2 does not file which figure the decision is taken on")
    low = this.loc[this["evening_median_kbps"].astype(float).idxmin()]
    A(low["line"] != g["decided_port"],
      "SF9 the lowest evening bitrate names the same interconnect as the largest shortfall")
    # SF10 comes closest: the mean reading names another interconnect, which clause 4.2 rules out
    A(g["rung2_port"] != g["closest_port"],
      "SF10 the quarter mean names the interconnect that comes closest anyway")
    # SF13 the earlier quarters: the record is the eight whole quarters before this one, and the
    # trailing eight ending with this one give the same call
    qs = sorted(set(rollup["reporting_quarter"]))
    A(len(qs) == 9 and qs[-1] == q, "SF13 the rollup covers %d quarters" % len(qs))
    trailing = kept[kept["reporting_quarter"].isin(qs[1:])]
    tw = trailing.groupby("reporting_quarter")["shortfall"].max()
    A(float(tw.drop(q).max()) > g["decided_shortfall"],
      "SF13 the trailing eight quarters move the call")
    # SF14 the reference band: the panel retains nothing outside the two bands, so the wider
    # reading cannot be computed at all
    A(set(p["lh"]) == set(range(W.DAY_BAND[0], W.DAY_BAND[1])) |
      set(range(W.EVENING_BAND[0], W.EVENING_BAND[1])),
      "SF14 the panel retains a minute outside the two bands")
    A("The reference band is 12:00 to 14:59 local time" in std,
      "SF14 the standard does not name the reference band")

    # ---- the asks --------------------------------------------------------------------------------
    # A1 the percentile rank and the accepted commitment are filed
    A("the 1,296th highest sample of the quarter" in fw, "A1 clause 7.1 does not file the rank")
    A("an amendment the peer has not accepted is not billed on" in fw,
      "A1 clause 7.2 does not file which commitment is billed")
    A("taken over the peer's traffic and not over one port of it" in fw,
      "A1 clause 7.1 does not file the grain")
    A(len(g["a1_peers"]) == 7, "A1 covers %d peers" % len(g["a1_peers"]))
    A(sum(1 for v in g["a1_peers"].values() if v["overage_eur"] > 0) >= 5,
      "A1 too few peers run over their commitment")
    two = [p for p in set(register["peer"]) if
           len([r for r in register.itertuples() if r.peer == p and r.status == "in service"]) > 1]
    A(len(two) == 2, "A1 %d peers hold more than one port" % len(two))
    A((amend["status"] == "delivered, not accepted").any(),
      "A1 no amendment is unaccepted, so the version device is absent")
    # A2 one version number covers two builds
    vs = [b["build_version"] for b in releases["builds"]]
    A(len(vs) != len(set(vs)), "A2 no version number is reissued")
    A(len(g["a2_builds"]) == len(releases["builds"]), "A2 does not cover every build")
    A(len(set(sessions["build_version"])) < len(releases["builds"]),
      "A2 the sessions file already separates the builds")
    # A3 the restoration standard and the causes are filed
    A("four hours from the time an incident was opened to the time service was restored" in fw,
      "A3 clause 5.1 does not file the standard")
    A("an incident for which no restoration time was recorded is not counted as restored" in fw,
      "A3 clause 5.1 does not file the absent restoration")
    A("sit outside the platform" in dic, "A3 the dictionary does not say which causes are outside")
    A(len(res) < len(inc), "A3 every incident carries a restoration time")
    for k, v in g["a3_incidents"].items():
        A(0 < v["restored_inside_standard"] < v["opened"], "A3 %s is degenerate" % k)
        A(0 < v["cause_outside_platform"] < v["opened"], "A3 %s has no split of causes" % k)

    # ---- closure axes ----------------------------------------------------------------------------
    for perm in (1, 2, 3):
        sh = rollup.sample(frac=1.0, random_state=perm).reset_index(drop=True)
        k2, _ = G.shortfalls(sh, register, maint)
        A(len(k2) == len(kept), "axis 14 row order changes the population")
        A(float(k2[k2["reporting_quarter"] == q]["shortfall"].max()) == g["decided_shortfall"],
          "axis 14 row order changes the decided figure")
    A((pd.to_numeric(rollup["evening_median_kbps"]) % 1 == 0).all(),
      "axis 10 a band median is not a whole kbps")
    A(not panel["measured_at_utc"].duplicated().any() or True, "axis 15 placeholder")
    A(len(panel.drop_duplicates(subset=["measured_at_utc", "port_code"])) == len(panel),
      "axis 15 the panel holds a repeated minute for one port")
    A(W.AS_OF > W.Q_TO and W.COMMITTEE > W.AS_OF, "axis 4 the dates do not run extract then board")
    A(int(health["minutes_missing"].astype(int).sum()) > 0,
      "axis 12 the collector lost nothing, so the panel has no gaps")
    A(int(health["minutes_captured"].astype(int).sum()) == len(panel),
      "axis 12 the health log and the panel disagree on what was captured")

    # ---- input gates -----------------------------------------------------------------------------
    files = sorted(os.listdir(target))
    A(len(files) >= 10, "input gate: %d files" % len(files))
    exts = {os.path.splitext(f)[1] for f in files}
    A(len(exts) >= 3, "input gate: %d formats" % len(exts))
    A(len(panel) >= W.TARGET_ROWS, "input gate: the largest file holds %d rows" % len(panel))
    A(len(meta["distractor_files"]) >= 2, "input gate: too few declared distractors")
    for d in meta["distractor_files"]:
        A(d["file"] in files, "input gate: declared distractor %s is not in the pack" % d["file"])
    return N[0]
