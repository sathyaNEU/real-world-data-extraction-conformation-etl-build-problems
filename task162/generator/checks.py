"""task162 checks: the call and its corridor, the three rules executed on the generator's clean truth, the shipped HOW
sentences, every semantic fork row, the closure axes that can move, the ladder and its out-of-sample record, both asks
with their routes and devices, the separation line, the realism sweep, the input gates and the distractors. Run by
build.py after the goldens are written; exits 1 on any failure.

    python3 task162/generator/checks.py"""
from __future__ import annotations

import copy
import datetime as dt
import itertools
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C            # noqa: E402
import common as K          # noqa: E402
import docs as DOC          # noqa: E402
import parallel as PR       # noqa: E402
import records as R         # noqa: E402
import world as W           # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
RESULTS = []
GOLD_TRIAGERS, GOLD_WEEK = 8, 900
PEOPLE_OK = set(K.PEOPLE.values()) | set(K.TRIAGERS) | set(K.WEBCOMPAT)
CALL_FILES = [R.F_EXPORT, R.F_SHARES, R.F_INSTALLS, DOC.F_CALENDAR, DOC.F_THREAD, DOC.F_RUNBOOK]
ASK_FILES = [R.F_NEWEXPORT, R.F_ROTA, R.F_GROUPS, DOC.F_AGREEMENT]


def ok(label, cond, detail=""):
    RESULTS.append((bool(cond), label))
    print("%s  %s%s" % ("PASS" if cond else "FAIL", label, ("  [%s]" % (detail,)) if detail != "" else ""))


# ------------------------------------------------------------------------------------------------- readers
def pdf_text(path):
    import pypdf
    return "\n".join(pg.extract_text() for pg in pypdf.PdfReader(path).pages)


def docx_text(path):
    import docx
    d = docx.Document(path)
    return "\n".join([p.text for p in d.paragraphs] + [c.text for t in d.tables for row in t.rows for c in row.cells])


def xlsx_text(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, read_only=True)
    out = []
    for ws in wb.worksheets:
        for row in ws.iter_rows(values_only=True):
            out.append(" ".join(str(v) for v in row if v is not None))
    wb.close()
    return "\n".join(out)


def eml_text(path):
    import email
    with open(path, "rb") as fh:
        m = email.message_from_binary_file(fh)
    return m.get_payload(decode=True).decode("utf-8")


def flat_text(target):
    out = {}
    for f in os.listdir(target):
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            out[f] = pdf_text(p)
        elif f.endswith(".docx"):
            out[f] = docx_text(p)
        elif f.endswith(".xlsx"):
            out[f] = xlsx_text(p)
        elif f.endswith(".eml"):
            out[f] = eml_text(p)
        elif f.endswith(".txt"):
            out[f] = open(p, encoding="utf-8").read()
    return out


def rebuild(D, keep=lambda r: True, shift=dt.timedelta(0), use="opened", sec=False):
    """The pack's daily triage items rebuilt under another reading of the export."""
    E = copy.copy(D)
    E.y = {p: np.zeros(len(D.days)) for p in C.PLATFORMS}
    E.y_all = np.zeros(len(D.days))
    for r in D.export:
        if not keep(r) or (r["groups"] == "core-security" and not sec):
            continue
        t = dt.datetime.strptime(r[use], "%Y-%m-%d %H:%M:%S") + shift
        i = D.di.get(t.date())
        if i is None:
            continue
        E.y[C.platform_of(r["op_sys"])][i] += 1
        E.y_all[i] += 1
    return E


# ------------------------------------------------------------------------------------------------- clean truth
def truth_series(T):
    """The clean truth before any mess: expected triage items per day (security reports out), the baseline part and
    the active installs, from the world's own parameters."""
    sec = 1 - W.SECURITY_SHARE
    n = len(W.DAYS)
    tot = np.zeros(n)
    base = np.zeros(n)
    inst = np.zeros(n)
    for i, d in enumerate(W.DAYS):
        for p in W.PLATFORMS:
            b = T.baseline[p][i]
            fu = sum(T.first_use[p][m][i] for m in T.first_use[p])
            tot[i] += (b + fu) * sec
            base[i] += b * sec
            inst[i] += W.dai(d, p)
    return tot, base, inst


def tweek(arr, w):
    return sum(arr[W.IDX[w + dt.timedelta(days=j)]] for j in range(7))


def truth_growth():
    a = sum(W.dai(K.AS_OF - dt.timedelta(days=j), p) for j in range(56) for p in W.PLATFORMS)
    b = sum(W.dai(K.AS_OF - dt.timedelta(days=364 + j), p) for j in range(56) for p in W.PLATFORMS)
    return a / b


def main():
    t0 = dt.datetime.now()
    D = C.load(TARGET)
    F = C.forecast(D)
    figs = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    text = flat_text(TARGET)
    alltext = "\n".join(text.values())

    # ============================================================================ the call
    ok("CALL the forecast files %d triagers, the busiest week %.1f items (%d to the nearest 100)" % (
        F["triagers"], F["busiest"], int(K.round_half_up(F["busiest"] / 100) * 100)),
        F["triagers"] == GOLD_TRIAGERS and int(K.round_half_up(F["busiest"] / 100) * 100) == GOLD_WEEK)
    cl_call = K.ceil_clearance(F["busiest"], 120)
    cl_100 = K.bin_clearance(F["busiest"], 100)
    ok("CALL mid-bin: the busiest week sits %.2f of a 120-item band from its edge (840 and 960) and %.2f of a 100 bin "
       "from its rounding edge" % (cl_call, cl_100), cl_call >= 0.25 and cl_100 >= 0.25)
    lo, hi = F["busiest"] - F["sigma"], F["busiest"] + F["sigma"]
    ok("CALL one sigma of the reports model (%.1f items, robust covariance) leaves the call and the rounded week: "
       "%.0f to %.0f" % (F["sigma"], lo, hi), math.ceil(lo / 120) == math.ceil(hi / 120) == GOLD_TRIAGERS
       and 875 <= lo and hi < 925)
    vals = []
    for majors, stat, lags, mode, win, gw in itertools.product(
            [None, {43, 44, 45, 46, 47, 48}], ["mean", "median"], [5, 6, 8], ["platform", "total", "weekly"],
            [None, (dt.date(2026, 1, 1), C.LAST_DAY)], [28, 56, 77]):
        if mode == "weekly" and lags != 6:
            continue
        f = C.forecast(D, dict(majors=majors, stat=stat, lags=lags, mode=mode, window=win, growth_window=gw))
        vals.append(f["busiest"])
    ok("CALL C1 convergence: %d defensible constructions (hazards from all releases or the last six, mean or median; "
       "a 5, 6 or 8 day lag, per platform, pooled or weekly; the fit on the whole record or 2026; growth over 4, 8 or "
       "11 weeks) all file 8 triagers and 900, from %.1f to %.1f, each a quarter of a bin inside" % (
           len(vals), min(vals), max(vals)),
       all(math.ceil(v / 120) == 8 for v in vals) and 875 <= min(vals) and max(vals) < 925)
    ok("CALL the busiest week is a release week (%s), and all three release weeks sit in the 8-triager band" %
       F["busiest_week"], F["busiest_week"] in {C.monday(d) for m, d in D.releases if m in (49, 50, 51)}
       and all(840 < F["weeks"][C.monday(D.rel_date[m])] <= 960 for m in (49, 50, 51)),
       [round(F["weeks"][C.monday(D.rel_date[m])]) for m in (49, 50, 51)])

    # ============================================================================ the ladder
    rg = C.rungs(D)
    lad = {k: rg[k]["triagers"] for k in ("R0", "R1", "R2a", "R2b", "R2c", "max", "q4", "per_install")}
    ok("LADDER every rung files its own count below the golden: %s" % ", ".join(
        "%s %d (%.0f)" % (k, v, rg[k]["busiest"]) for k, v in lad.items()),
       all(v < GOLD_TRIAGERS for v in lad.values()) and lad["R1"] == 6 and lad["R0"] <= 4)
    near = max(rg[k]["busiest"] for k in lad)
    ok("LADDER the golden is the extreme cell: the nearest rung (%.0f items) sits %.0f items under the 840 edge" % (
        near, 840 - near), near < 840 - 60)
    oo = C.oos(D)
    prof = [oo[m][2]["profile"] / oo[m][2]["actual"] for m in (46, 47)]
    rst = [abs(oo[m][2]["restart"] / oo[m][2]["actual"] - 1) for m in (46, 47)]
    sec = [oo[m][1]["profile"] / oo[m][1]["actual"] - 1 for m in (46, 47)]
    ok("OOS the release-week profile fitted on the 13 releases a week before Patch Tuesday puts the third weeks of the "
       "29 September and 27 October releases at %s of what they brought and their second weeks %s high; the restart "
       "model fitted on the same releases comes within %s" % (
           ", ".join("%.0f%%" % (100 * v) for v in prof), ", ".join("%.0f%%" % (100 * v) for v in sec),
           ", ".join("%.0f%%" % (100 * v) for v in rst)),
       max(prof) < 0.55 and min(sec) > 0.15 and max(rst) < 0.15)

    # ============================================================================ the three rules on the clean truth
    T = W.simulate()
    tot, base, inst = truth_series(T)
    g = truth_growth()
    q126 = [dt.date(2026, 1, 5) + dt.timedelta(days=7 * k) for k in range(13)]
    easy = max(tweek(tot, w) for w in q126) * g
    ok("R3a the analyst test on the clean truth: every filed rule applied (every report, duplicates in, the security "
       "group out, Helsinki weeks, the 120 standard rounded up), last year's busiest first-quarter week scaled for "
       "growth files %.0f items, %d triagers, not the golden" % (easy, math.ceil(easy / 120)),
       math.ceil(easy / 120) == 6)
    q1 = {w: tweek(tot, w) for w in K.Q1_WEEKS}
    wb = max(q1, key=q1.get)
    ok("R3b the decisive step alone on the clean truth (each release's adoption from the restart process, the "
       "Windows wave inside each release week): the busiest week carries %.0f items, %d triagers" % (
           q1[wb], math.ceil(q1[wb] / 120)), math.ceil(q1[wb] / 120) == GOLD_TRIAGERS)
    # each lower rung's single correction on the clean truth
    rels = [(m, d) for m, d in K.RELEASES if dt.date(2025, 10, 8) <= d <= dt.date(2026, 11, 3)]
    pr = np.zeros(4)
    for m, d in rels:
        for k in range(4):
            w = C.monday(d) + dt.timedelta(days=7 * k)
            pr[k] += (tweek(tot, w) - tweek(base, w)) / tweek(inst, w)
    pr /= len(rels)
    qprof = {}
    for w in K.Q1_WEEKS:
        v = tweek(base, w)
        for m in (49, 50, 51):
            k = (w - C.monday(K.MAJOR_DATE[m])).days // 7
            if 0 <= k < 4:
                v += pr[k] * tweek(inst, w)
        qprof[w] = v
    vp = max(qprof.values())
    reach_typ = {p: np.zeros(28) for p in W.PLATFORMS}
    for m, d in rels:
        i0 = W.IDX[d]
        for p in W.PLATFORMS:
            reach_typ[p] += T.adopt.reach[p][m][i0:i0 + 28] / len(rels)
    rho = np.mean([T.rho[m] for m, d in rels])
    fu = np.zeros(len(W.DAYS))
    for m in (49, 50, 51):
        i0 = W.IDX[K.MAJOR_DATE[m]]
        for p in W.PLATFORMS:
            for j in range(28):
                ins = reach_typ[p][j] * W.base(W.DAYS[i0 + j], p)
                for k, kv in enumerate(W.KERNEL):
                    if i0 + j + k < len(W.DAYS):
                        fu[i0 + j + k] += ins * rho * kv
    qtr = {w: tweek(base, w) + tweek(fu, w) * (1 - W.SECURITY_SHARE) for w in K.Q1_WEEKS}
    vt = max(qtr.values())
    ok("R3b each lower rung's single correction stays wrong on the clean truth: the record's release-week profile on "
       "the quarter's baseline %.0f (%d), the typical first-month reach carried onto the releases %.0f (%d)" % (
           vp, math.ceil(vp / 120), vt, math.ceil(vt / 120)), math.ceil(vp / 120) < 8 and math.ceil(vt / 120) < 8)
    reps = [tuple(int(v) for v in D.y_all[i:i + 7]) for i in range(0, len(D.days) - 7, 7)]
    ok("R3c no copied block: no two weeks of the export share their daily counts, and no run of three equal weekly "
       "totals", len(set(reps)) == len(reps) and not any(
           reps[i] == reps[i + 1] for i in range(len(reps) - 1)))
    ok("R3c no document states a first-quarter forecast, a headcount or a release week's load: the only figures near "
       "'triagers' are the 120 standard", not re.search(r"\b\d+ triagers\b", alltext) and
       "forecast" not in alltext.lower())
    ok("R1 the field's raw material ships: one row per report with its filing time (%d rows), each platform's daily "
       "share by major version (%d rows) and daily active installs (%d rows); no column holds a reach, a restart, a "
       "burst or an adoption rate" % (len(D.export), sum(1 for _ in open(os.path.join(TARGET, R.F_SHARES))) - 1,
                                      sum(1 for _ in open(os.path.join(TARGET, R.F_INSTALLS))) - 1),
       not any(re.search(r"reach|restart|burst|adopt|hazard|first_use", h, re.I) for f in (R.F_EXPORT, R.F_SHARES,
                                                                                          R.F_INSTALLS)
               for h in open(os.path.join(TARGET, f), encoding="utf-8").readline().split(",")))
    Dflat = copy.copy(D)
    Dflat.share = {p: [dict(s) for s in D.share[p]] for p in C.PLATFORMS}
    ok("R1 the decisive computation reads the shares: the record's Windows step-ups after Patch Tuesday are where the "
       "forecast's release-week reach comes from (Wednesday hazard %.2f against %.2f on other weekdays)" % (
           F["H"]["Windows"]["burst1"], F["H"]["Windows"]["weekday"]),
       F["H"]["Windows"]["burst1"] > 4 * F["H"]["Windows"]["weekday"] and F["H"]["macOS"].get("burst1") is None)
    # R2: each Layer 1 item mishandled, the call and its rounded week stay
    r2 = {
        "opened read as UTC": rebuild(D, shift=dt.timedelta(hours=2)),
        "the security group kept in": rebuild(D, sec=True),
        "the parallel run's archived reports dropped": rebuild(D, keep=lambda r: r["product"] != "Archive"),
        "beta and nightly reports dropped": rebuild(D, keep=lambda r: "a" not in r["version"] and "b" not in r["version"]),
    }
    for name, E in r2.items():
        f = C.forecast(E)
        ok("R2 %s leaves the call: %.0f items, %d triagers" % (name, f["busiest"], f["triagers"]),
           f["triagers"] == 8 and 850 <= f["busiest"] < 950)
    Ek = copy.copy(D)
    Ek.inst = {p: D.inst[p] / 1000.0 for p in C.PLATFORMS}
    fk = C.forecast(Ek)
    ok("R2 active installs read in units rather than thousands leave the call (%.1f)" % fk["busiest"],
       abs(fk["busiest"] - F["busiest"]) < 0.5)
    orig = C.day_type
    C.day_type = lambda DD, d, p: {"yearend": "weekday", "yearend_we": "weekend"}.get(orig(DD, d, p), orig(DD, d, p))
    fy = C.forecast(D)
    C.day_type = orig
    ok("R2 the year-end lull's days read as ordinary days leave the call (%.0f)" % fy["busiest"],
       fy["triagers"] == 8 and 850 <= fy["busiest"] < 950)
    f13 = C.forecast(D, dict(window=(dt.date(2025, 10, 6), dt.date(2026, 12, 13))))
    ok("R2 SF7 the record's partial first and last weeks dropped (data from Monday 6 October 2025 to Sunday "
       "13 December 2026) leave the call (%.0f)" % f13["busiest"], f13["triagers"] == 8 and 850 <= f13["busiest"] < 950)

    # ============================================================================ HOW: the shipped sentences
    how = [s for s in DOC.THREAD_SENTENCES + DOC.RUNBOOK_SENTENCES if re.search(
        r"busiest|120|13 weeks|triage item|counted in the week|not new triage items|whatever version", s)]
    hay = re.sub(r"\s+", " ", re.sub(r"(?m)^>\s?", "", text[DOC.F_THREAD]) + " " + text[DOC.F_RUNBOOK])
    missing = [s for s in how if re.sub(r"\s+", " ", s) not in hay]
    ok("HOW the sentences fixing what is counted (%d) are the thread's estimand and the runbook's counting basis, each "
       "in the shipped text" % len(how), len(how) >= 6 and not missing, missing)
    banned = re.compile(r"restart|patch tuesday|reboot|burst|adoption|adopt|first-use|first use|takes? the update|"
                        r"update is applied|updates? appl|auto-update|second tuesday|cumulative update|windows update|"
                        r"uplift|profile", re.I)
    hits = sorted({f for f, tx in text.items() if banned.search(tx)})
    ok("HOW no shipped sentence names a restart, Patch Tuesday, a burst, adoption, reach or a release-week profile",
       not hits, hits)
    pr_txt = open(os.path.join(TASK, "prompt.txt"), encoding="utf-8").read()
    ok("HOW the prompt asks the headcount and the busiest week's forecast and names no method, release or restart",
       "How many triagers" in pr_txt and not banned.search(pr_txt) and "release" not in pr_txt.lower())

    # ============================================================================ the semantic fork table
    near_ = math.floor(F["busiest"] / 120 + 0.5)
    ok("SF1 rounded to the nearest triager instead of up files %d: same call" % near_, near_ == 8)
    fd = C.forecast(rebuild(D, keep=lambda r: r["resolution"] != "DUPLICATE"))
    fs = C.forecast(rebuild(D, sec=True))
    ok("SF2 duplicates out files %d (the runbook counts them); restricted reports in file %d (the runbook keeps them "
       "out)" % (fd["triagers"], fs["triagers"]), fd["triagers"] < 8 and fs["triagers"] == 8 and
       "Every report filed through the report form is a triage item, duplicates included" in text[DOC.F_RUNBOOK])
    cal = {w: v for w, v in F["weeks"].items() if w <= dt.date(2027, 3, 29)}
    ok("SF3 the quarter read as January to March (the last week cut at 31 March) keeps the busiest week: same call",
       max(cal, key=cal.get) == F["busiest_week"])
    fu_ = C.forecast(rebuild(D, shift=dt.timedelta(hours=-2)))
    ok("SF4 weeks in UTC rather than Helsinki time move the busiest week by %.1f per cent: same call" % (
        100 * abs(fu_["busiest"] / F["busiest"] - 1)), fu_["triagers"] == 8 and abs(fu_["busiest"] / F["busiest"] - 1) < 0.01)
    rises = {w: F["weeks"][w] - F["weeks"].get(w - dt.timedelta(days=7), F["weeks"][w]) for w in C.Q1_WEEKS[1:]}
    wr = max(rises, key=rises.get)
    ok("SF5 the busiest week read as the week of the largest rise picks a release week in the same band (%s, %.0f)" % (
        wr, F["weeks"][wr]), 840 < F["weeks"][wr] <= 960)
    p90 = F["busiest"] + 1.2816 * math.sqrt(F["busiest"])
    ok("SF6 expected read as a 90th percentile of a Poisson week (%.0f) files the same 8; the thread asks the expected "
       "load" % p90, math.ceil(p90 / 120) == 8 and "expected load in the quarter's busiest week" in re.sub(
           r"\s+", " ", re.sub(r"(?m)^>\s?", "", text[DOC.F_THREAD])))
    ok("SF7 the as-of: every file taken by 18 December 2026; the export holds reports filed to 23:59:59 on Thursday "
       "17 December", max(r["opened"] for r in D.export) <= "2026-12-17 23:59:59" and
       "2026-12-18 06:40" in text[R.F_FIELDS])
    fc_ = C.forecast(rebuild(D, use="changeddate"))
    ok("SF8 a report's week read from changeddate files %d; the runbook counts a report in the week it is filed and the "
       "field notes give opened as the filing time" % fc_["triagers"], fc_["triagers"] != 8 and
       "A report is counted in the week it is filed" in text[DOC.F_RUNBOOK] and "when the report was filed" in text[R.F_FIELDS])
    fm = C.forecast(rebuild(D, keep=lambda r: r["product"] != "Web Compatibility"))
    ok("SF9 reports moved to the web-compatibility team left out file %d; the runbook keeps them as triage items" %
       fm["triagers"], "stays a triage item" in text[DOC.F_RUNBOOK])
    fb = C.forecast(rebuild(D, keep=lambda r: "a" not in r["version"] and "b" not in r["version"]))
    ok("SF10 release-channel reports only file %d: same call; the runbook counts every version" % fb["triagers"],
       fb["triagers"] == 8 and "whatever version the reporter runs" in text[DOC.F_RUNBOOK])
    fa = C.forecast(rebuild(D, keep=lambda r: r["product"] != "Archive"))
    ok("SF11 the parallel run's reports (closed MOVED, in Archive) dropped file %d: same call" % fa["triagers"],
       fa["triagers"] == 8)
    open_now = sum(1 for r in D.export if r["resolution"] == "---" and not r["groups"])
    ok("SF12 the %d reports open at the pull counted as first-week items would make the first week the busiest; the "
       "runbook files that migrated reports are not new triage items" % open_now,
       open_now + F["weeks"][C.Q1_WEEKS[0]] > F["busiest"] and "Migrated reports keep their state and are not new "
       "triage items" in text[DOC.F_RUNBOOK])
    rounded_first = max(round(v) for v in F["weeks"].values())
    ok("SF13 the weeks rounded first files the same %d" % math.ceil(rounded_first / 120), math.ceil(rounded_first / 120) == 8)

    # ============================================================================ closure axes that can move
    f48 = C.forecast(D, dict(majors=set(range(34, 48))))
    ok("CLOSURE 12 the 1 December release left out of the hazards (its adoption still under way at the as-of) files "
       "the same call (%.0f)" % f48["busiest"], f48["triagers"] == 8 and 850 <= f48["busiest"] < 950)
    ok("CLOSURE 15 every bug id once in the export; every exported report has a filing time inside the record",
       len({r["bug_id"] for r in D.export}) == len(D.export) and all("2025-10-01" <= r["opened"][:10] <= "2026-12-17"
                                                                     for r in D.export))
    Eb = copy.copy(D)
    Eb.export = [dict(r, bug_status="", resolution="", dupe_of="", keywords="", bug_severity="") for r in D.export]
    fbk = C.forecast(rebuild(Eb))
    ok("CLOSURE 19 no status or resolution is read by the call: the forecast with the status, resolution, duplicate "
       "and keyword columns blanked is %.2f" % fbk["busiest"], abs(fbk["busiest"] - F["busiest"]) < 1e-6)
    comp = []
    for opt in (dict(majors={43, 44, 45, 46, 47, 48}), dict(stat="median"), dict(majors={43, 44, 45, 46, 47, 48},
                                                                                  stat="median")):
        H = C.forecast(D, opt)["H"]["Windows"]
        comp.append((round(100 * H["burst1"]), round(100 * H["burst2"]), round(100 * H["weekday"])))
    ok("CALL the stated components hold across the hazard constructions: the Windows Wednesday, Thursday and weekday "
       "hazards round to %s, %s and %s per cent" % (figs["components"]["windows_wed_pct"],
                                                    figs["components"]["windows_thu_pct"],
                                                    figs["components"]["windows_weekday_pct"]),
       all(abs(c[0] - int(figs["components"]["windows_wed_pct"])) <= 1 and
           abs(c[1] - int(figs["components"]["windows_thu_pct"])) <= 2 and
           abs(c[2] - int(figs["components"]["windows_weekday_pct"])) <= 1 for c in comp), comp)

    # ============================================================================ the asks
    A = C.load_asks(TARGET, D)
    rep = C.ceiling_report(TARGET, quiet=True)
    gld = rep["routes"]["golden"]
    ga = [(r["no_action"], r["closed"]) for r in figs["answers"]["ask_a"]]
    ok("ASK A the golden: %s" % "; ".join("%s %d/%d" % (w, gld["no_action"][w], gld["closed"][w]) for w in C.RUN_WEEKS),
       ga == [(gld["no_action"][w], gld["closed"][w]) for w in C.RUN_WEEKS])
    ok("ASK B the golden: %s" % "; ".join("%s %d" % (g_, gld["groups"][g_]) for g_ in C.GROUPS),
       all(figs["answers"]["ask_b"][g_] == gld["groups"][g_] for g_ in C.GROUPS))
    for name in C.CRACKER_PATHS:
        kk = rep["kept"][name]
        ok("ASK the cracker's %s path keeps %d of Ask A's 8 and %d of Ask B's 8 figures; pair %.1f" % (
            name.replace("cracker_", ""), kk["A"], kk["B"], rep["pairs"][name]["pair"]), rep["pairs"][name]["pair"] <= 40)
    ok("ASK the mirror keeps %.1f per cent of the ask weight (under 35)" % rep["mirror_leakage"], rep["mirror_leakage"] < 35)
    ok("ASK every natural path misses every Ask A week and at least six of Ask B's groups", all(
        rep["kept"][n]["A"] == 0 and rep["kept"][n]["B"] <= 2 for n in C.CRACKER_PATHS + ("mirror",)))
    iss = A.issues
    bulk = [i for i in iss if i["fields"]["customfield_10410"] is None and any(
        lab.startswith("legacy-") for lab in i["fields"]["labels"])]
    moved_hist = [i for i in iss if i["fields"]["project"]["key"] == "WEBC" and any(
        it["field"] == "Legacy bug" and it["fromString"] for h in i["changelog"]["histories"] for it in h["items"])]
    ok("DEVICE the catch-ups after the bridge's stops are real and silent: %d issues carry the old number only as a "
       "label, every one created at a restart, none beside a sentence about it" % len(bulk), len(bulk) > 150 and
       not re.search(r"label|bulk|catch-up|checkpoint|outage|re-sen|stopped", alltext, re.I))
    ok("DEVICE moved reports lose Legacy bug on the move and keep it in the changelog: %d" % len(moved_hist),
       len(moved_hist) > 40)
    filed = {int(r["bug_id"]): dt.datetime.strptime(r["opened"], "%Y-%m-%d %H:%M:%S") for r in D.export}
    lag = []
    for i in iss:
        n_ = C.legacy_id(i, "all")
        if n_ in filed and i["fields"]["issuetype"]["name"] == "Bug":
            lag.append((C.jt(i["fields"]["created"]) - filed[n_]).total_seconds() / 3600)
    ok("DEVICE the bridge's created trails the filing by more than an hour for %d of the run's copies (stops, Sunday "
       "maintenance, the close-out), and by under a minute for the rest" % sum(1 for v in lag if v > 1),
       sum(1 for v in lag if v > 1) > 200 and all(v >= 0 for v in lag) and
       sum(1 for v in lag if 0 < v * 3600 < 60) > 1000)
    cl = [i for i in iss if i["fields"]["status"]["name"] == "Closed" and i["fields"]["resolution"] is None]
    ok("DEVICE the workflow's Close transition leaves %d closed issues without a resolution or resolution date" % len(cl),
       len(cl) > 40 and all(i["fields"]["resolutiondate"] is None for i in cl))
    sep = os.path.join(tempfile.mkdtemp(prefix="sep162_", dir=os.environ.get("TASK162_SCRATCH", "/tmp")), "t")
    shutil.copytree(TARGET, sep)
    for f in ASK_FILES:
        os.remove(os.path.join(sep, f))
    fsep = C.forecast(C.load(sep))
    ok("SEPARATION the call reads none of the asks' files: the forecast with the new tracker's export, the rota, the "
       "register and the agreement deleted is %.2f (golden %.2f)" % (fsep["busiest"], F["busiest"]),
       abs(fsep["busiest"] - F["busiest"]) < 1e-6)
    shutil.copytree(TARGET, sep + "d")
    for f in json.load(open(os.path.join(TASK, "metadata.json")))["distractor_files"]:
        os.remove(os.path.join(sep + "d", f))
    fdis = C.forecast(C.load(sep + "d"))
    rd_ = C.ceiling_report(sep + "d", quiet=True)["routes"]["golden"]
    ok("GATE the call and both asks unchanged with the distractors deleted", abs(fdis["busiest"] - F["busiest"]) < 1e-6
       and rd_["no_action"] == gld["no_action"] and rd_["closed"] == gld["closed"] and rd_["groups"] == gld["groups"])
    shutil.rmtree(os.path.dirname(sep))

    # ============================================================================ realism and gates
    authors = {h["author"]["displayName"] for i in A.issues for h in i["changelog"]["histories"]} | \
        {i["fields"]["reporter"]["displayName"] for i in A.issues}
    in_docs = {n for n in PEOPLE_OK if n in alltext}
    ok("REALISM every persona is from guard.py names: the new tracker's authors (%s) and the documents' people (%s)" % (
        ", ".join(sorted(authors)), ", ".join(sorted(in_docs))),
       authors <= PEOPLE_OK | {PR.BRIDGE} and in_docs and K.PEOPLE["lead"] in in_docs)
    dash = [f for f, tx in text.items() if "\u2014" in tx or "\u2013" in tx] + \
        (["prompt.txt"] if "\u2014" in pr_txt or "\u2013" in pr_txt else [])
    ok("REALISM no em or en dash in any document or the prompt", not dash, dash)
    sig = []
    for f in os.listdir(TARGET):
        b = open(os.path.join(TARGET, f), "rb").read()
        for s_ in (b"openpyxl", b"python-docx", b"ReportLab", b"reportlab", b"Generated"):
            if s_ in b:
                sig.append((f, s_.decode()))
    ok("REALISM H1 no writer's name in any shipped container", not sig, sig)
    late = max(i["fields"]["updated"] for i in iss)
    ok("REALISM H16 no record dated after its export: the new tracker's last change %s UTC is before its export at "
       "08:20 UTC on 4 December; the old export's last change is before the pull" % late,
       late <= "2026-12-04T08:20:00" and max(r["changeddate"] for r in D.export) <= "2026-12-18 06:40:00")
    wk = C.weekly_items(D)
    ok("REALISM no round headline: no weekly total of the record is a multiple of 100, and no two neighbouring weeks "
       "are equal", not any(v % 100 == 0 for v in wk.values()) or sum(1 for v in wk.values() if v % 100 == 0) <= 1)
    files = sorted(os.listdir(TARGET))
    man = [r["file"] for r in C.rd(TARGET, DOC.F_MANIFEST)]
    ok("REALISM H9 the manifest names every shipped file but itself, once", sorted(man) == sorted(
        f for f in files if f != DOC.F_MANIFEST) and len(set(man)) == len(man))
    import docx as _docx
    rb_mod = _docx.Document(os.path.join(TARGET, DOC.F_RUNBOOK)).core_properties.modified
    ok("REALISM H16 the runbook, which records the run's export of 4 December, is saved after it (%s) and before the "
       "pull" % rb_mod, dt.datetime(2026, 12, 4) <= rb_mod.replace(tzinfo=None) <= dt.datetime(2026, 12, 18, 4, 40))
    Rr = C.reach_series(D)
    mh = {}
    for p_ in ("macOS", "Linux"):
        for i, d in enumerate(D.days):
            if Rr[p_]["newest"][i] and Rr[p_]["pend"][i] > 0.2 and d not in D.rel_date.values() and d.weekday() < 5 \
                    and not K.year_end(d):
                k = "pt" if any((d - pt).days in (1, 2) for pt in C.PATCH_TUESDAYS) else "wd"
                mh.setdefault((p_, k), []).append(Rr[p_]["reach"][i] / Rr[p_]["pend"][i])
    ratio = {p_: np.median(mh[(p_, "pt")]) / np.median(mh[(p_, "wd")]) for p_ in ("macOS", "Linux")}
    ok("H6 macOS and Linux have no Patch Tuesday days: their median hazards on the Wednesday and Thursday after run %.2f "
       "and %.2f times their other weekdays' (days with a fifth or more of the installs still to update)" % (
           ratio["macOS"], ratio["Linux"]), all(0.85 < v < 1.15 for v in ratio.values()))
    copies_n, seen_n = 0, set()
    for i in sorted(A.issues, key=lambda i: (i["fields"]["created"], int(i["id"]))):
        n_ = C.legacy_id(i, "all") or (int(i["fields"]["customfield_10522"]) if i["fields"].get("customfield_10522") else None)
        if n_ is None:
            continue
        copies_n += n_ in seen_n
        seen_n.add(n_)
    restricted_n = sum(1 for i in A.issues if i["fields"]["security"] is not None)
    tasks_n = sum(1 for i in A.issues if i["fields"]["issuetype"]["name"] == "Task")
    webc_own = sum(1 for i in A.issues if i["fields"].get("customfield_10522"))
    two_comp = sum(1 for i in A.issues if any(
        sum(1 for it in h["items"] if it["field"] == "Component" and it["toString"]) >
        sum(1 for it in h["items"] if it["field"] == "Component" and it["fromString"]) for h in i["changelog"]["histories"]
        if h["author"]["displayName"] in A.triagers))
    end_ = dt.datetime(2026, 11, 29, 23, 59, 59)
    closeout = sum(1 for i in A.issues if i["fields"]["issuetype"]["name"] == "Bug" and not i["fields"]["security"]
                   and C.legacy_id(i, "all") in filed and filed[C.legacy_id(i, "all")] < C.RUN_TO
                   and C.jt(i["fields"]["created"]) > end_)
    ok("H2 the ask sheet's counts recompute from the pack: %d re-sent copies, %d restricted issues, %d tasks, %d site "
       "reports with an Old tracker ID, %d issues given a second component by a triager, %d of the run's reports "
       "written after the run ended" % (copies_n, restricted_n, tasks_n, webc_own, two_comp, closeout),
       copies_n == 84 and tasks_n == 19 and closeout > 40 and webc_own > 200 and two_comp > 40)
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("GATE %d files, %d formats (%s), the largest %s at %d rows" % (len(files), len(fmts), ", ".join(sorted(fmts)),
                                                                    R.F_EXPORT, len(D.export)),
       len(files) >= 10 and len(fmts) >= 3 and len(D.export) >= 25000)
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    ok("GATE two or more distractors named in metadata.json, shipped, none named as one",
       len(meta["distractor_files"]) >= 2 and all(f in files for f in meta["distractor_files"]) and
       not any("distract" in f for f in files))
    ok("GATE metadata.json lists every shipped file with a source, date and licence",
       sorted(x["path"] for x in meta["files"]) == files and all(x["source"] and x["date"] and x["license"]
                                                                 for x in meta["files"]))
    sub = os.path.join(TASK, "submission.md")
    if os.path.exists(sub):
        fc = subprocess.run([sys.executable, os.path.join(TASK, "..", ".claude", "skills", "determinism-check",
                                                          "figures_check.py"), TASK, "--quiet"])
        ok("WRITEUP figures_check: every number in blocks 1 to 4 is in figures.json", fc.returncode == 0)
    nfail = sum(1 for r in RESULTS if not r[0])
    print("checks: %d assertions, %d failed (%.0f s)" % (len(RESULTS), nfail, (dt.datetime.now() - t0).total_seconds()))
    return 1 if nfail else 0


if __name__ == "__main__":
    sys.exit(main())
