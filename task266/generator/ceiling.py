"""task266 ask layer against the careful solver's routes, on the cut pack.

    python3 task266/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The two review-profile
asks give 18 figures: each program's FTE at the fall 2026 census (Ask A, nine, kept within half a unit of one decimal)
and each program's classes of its own courses with fewer than ten students at the census (Ask B, nine, kept exactly).
Each route below is a complete pipeline over the registrations, the section schedule, the program-of-record history,
the register and the term calendar, scored figure by figure against figures.json; the golden route is the control and
has to give back figures.json exactly.

The cracker is the careful solver: it lands the call, runs the hygiene battery, reads every label column, matches every
control and executes every filed rule as worded: policy 4.1 (the program of record in effect at the census, the
history read by its effective and end terms; the credit hours a registration's section carries in the term's section
schedule, over 15), 4.3 (the registrations in place on the census date, later withdrawals kept) and 4.2 (sections
scheduled to meet together, at one campus or across campuses, one class: one instructor at the same days and begin time
in weeks the sections share). The mirror is the best response off the call (the default path, one program) on
its natural read: the extract's own program column, every registered or withdrawn row whatever its date, the schedule's
section credit hours and its enrolment column section by section.

The pair is the ask sheet's formula (38 recommendation and components, 7 instruction following, 55 over the 18 ask
figures, the chart's three form criteria to both, a response off the call keeping 5), with the chart counted inside the
ask layer (3 of 21 criteria, task170's form) printed beside it. The shortcut rows are the cracker taking a less careful
step on one ask (where the devices would have to bite) and the mirror reading the filed rules on one ask."""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A   # noqa: E402
import common as K     # noqa: E402

TASK = os.path.dirname(HERE)
CHART = 3                     # the chart's form criteria, kept by any response that draws one
N_ASK = 18
INV = {v: k for k, v in K.SIS.items()}

A_ROUTES = {
    "golden: 4.1 and 4.3 as filed, the program of record the row in effect for fall 2026": dict(),
    "the cracker (the careful solver): 4.1 and 4.3 as filed, the history's row in effect by its effective and end "
    "terms": dict(program="latest"),
    "the history's latest row begun by fall 2026, end terms not read (an as-of shortcut)": dict(program="asof"),
    "the registration column (course_credit_hours) at the census, history program": dict(credits="row"),
    "the registration column once per student and course": dict(credits="row_once"),
    "section Cr Hrs by the extract's program_code": dict(program="row"),
    "section Cr Hrs, every RE, RW and WC row whatever its date (late adds kept)": dict(census="status"),
    "section Cr Hrs, every row dated by the census (later withdrawals dropped)": dict(census="all_dates"),
    "the mirror: section Cr Hrs by the extract's program, every RE, RW and WC row": dict(program="row",
                                                                                        census="status"),
    "the natural read before 4.1 filed the source: registration column, extract's program, every row":
        dict(credits="row", program="row", census="status"),
}
B_ROUTES = {
    "golden: sections sharing an instructor and a meeting in weeks they have in common": dict(),
    "the cracker (the careful solver): one instructor, days and begin time in weeks the sections share":
        dict(group="dated"),
    "instructor, days, begin time and both dates (identical dates required)": dict(group="exact"),
    "instructor, days and begin time, whatever the weeks": dict(group="meeting"),
    "instructor, days, begin time and first day": dict(group="first"),
    "instructor, days and begin time as written, TBA included": dict(group="text"),
    "room, days and begin time": dict(group="room"),
    "census counts, section by section": dict(group="none"),
    "the golden grouping with late adds kept": dict(enrol="status"),
    "the mirror: the schedule's enrolment, section by section": dict(enrol="export", group="none"),
}
CRACKER = dict(A="the cracker (the careful solver): 4.1 and 4.3 as filed, the history's row in effect by its effective "
                 "and end terms",
               B="the cracker (the careful solver): one instructor, days and begin time in weeks the sections share")
MIRROR = dict(A="the mirror: section Cr Hrs by the extract's program, every RE, RW and WC row",
              B="the mirror: the schedule's enrolment, section by section")


def across_campuses(target):
    """Ask B keyed on instructor, days and begin time with only sections at different campuses merged: the reading of
    4.2's "across campuses" that leaves every same-campus pair apart without looking at the weeks."""
    pk, regs, secs, hist = A.fall26(target)
    n = Counter(r["crn"] for r in A.census_rows(regs, A.day(pk.census[K.FALL26]), "date"))
    run = [s for s in secs if s["Status"] == "Active" and pk.owner.get(s["Subj"]) in pk.programs]
    groups = defaultdict(list)
    for s in run:
        groups[str(s["CRN"]) if s["Days"] == "TBA" else (s["Instructor"], s["Days"], s["Begin"])].append(s)
    classes = []
    for lst in groups.values():
        if len(lst) > 1 and len({s["Camp"] for s in lst}) == len(lst):
            classes.append(lst)
        else:
            classes += [[s] for s in lst]
    out = Counter()
    for lst in classes:
        if sum(n[str(s["CRN"])] for s in lst) < K.SMALL:
            for p in {pk.owner[s["Subj"]] for s in lst}:
                out[p] += 1
    return {p: out[p] for p in pk.programs}


def video_rooms(target):
    """Ask B keyed on instructor, days and begin time among the sections in rooms ending in V, every other section a
    class of its own: the reading that takes a V room for a video link."""
    pk, regs, secs, hist = A.fall26(target)
    n = Counter(r["crn"] for r in A.census_rows(regs, A.day(pk.census[K.FALL26]), "date"))
    run = [s for s in secs if s["Status"] == "Active" and pk.owner.get(s["Subj"]) in pk.programs]
    groups = defaultdict(list)
    for s in run:
        v = str(s["Room"]).endswith("V") and s["Days"] != "TBA"
        groups[(s["Instructor"], s["Days"], s["Begin"]) if v else str(s["CRN"])].append(s)
    out = Counter()
    for lst in groups.values():
        if sum(n[str(s["CRN"])] for s in lst) < K.SMALL:
            for p in {pk.owner[s["Subj"]] for s in lst}:
                out[p] += 1
    return {p: out[p] for p in pk.programs}


def r1(x):
    return int(x * 10 + 0.5) / 10.0


def kept_a(got, gold):
    return sum(abs(r1(got[p]) - gold[K.NAME[INV[p]]]) < .05 for p in got)


def kept_b(got, gold):
    return sum(got[p] == gold[K.NAME[INV[p]]] for p in got)


def pair(kc, km):
    """(ask sheet, chart inside the ask layer): each a (cracker, mirror, pair) triple."""
    c1, s1 = 38 + 7 + CHART + 55.0 * kc / N_ASK, 5 + 7 + CHART + 55.0 * km / N_ASK
    tot = N_ASK + CHART
    c2, s2 = 38 + 7 + 55.0 * (kc + CHART) / tot, 5 + 7 + 55.0 * (km + CHART) / tot
    return (c1, s1, (c1 + s1) / 2), (c2, s2, (c2 + s2) / 2)


def pack_dir(arg):
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        return src, None, "folder %s (%d files)" % (src, len(os.listdir(src)))
    tmp = tempfile.mkdtemp(prefix="ceiling266-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    folder = os.path.join(tmp, "target") if os.path.isdir(os.path.join(tmp, "target")) else tmp
    md5 = hashlib.md5(open(src, "rb").read()).hexdigest()
    return folder, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(folder)), md5)


def measure(target):
    """Every route's figures kept, the cracker's and the mirror's, and the pairs. Raises when the golden routes do not
    give back figures.json (the route code's control)."""
    F = json.load(open(os.path.join(HERE, "figures.json")))
    ga, gb = F["ask_a"], F["ask_b"]
    ha = {nm: kept_a(A.ask_a(target, **kw), ga) for nm, kw in A_ROUTES.items()}
    hb = {nm: kept_b(A.ask_b(target, **kw), gb) for nm, kw in B_ROUTES.items()}
    hb["instructor, days and begin time, only sections at different campuses merged"] = kept_b(across_campuses(target),
                                                                                                gb)
    hb["instructor, days and begin time, only sections in rooms ending in V merged"] = kept_b(video_rooms(target), gb)
    if ha[list(A_ROUTES)[0]] != 9 or hb[list(B_ROUTES)[0]] != 9:
        raise AssertionError("CONTROL FAILED: the golden routes give A %d and B %d of 9"
                             % (ha[list(A_ROUTES)[0]], hb[list(B_ROUTES)[0]]))
    cr = dict(A=ha[CRACKER["A"]], B=hb[CRACKER["B"]])
    mi = dict(A=ha[MIRROR["A"]], B=hb[MIRROR["B"]])
    asof = "the history's latest row begun by fall 2026, end terms not read (an as-of shortcut)"
    exact = "instructor, days, begin time and both dates (identical dates required)"
    cracks = {
        "the cracker took the as-of shortcut on the history": (ha[asof] + cr["B"], mi["A"] + mi["B"]),
        "the cracker required identical section dates": (cr["A"] + hb[exact], mi["A"] + mi["B"]),
        "the cracker took both shortcuts": (ha[asof] + hb[exact], mi["A"] + mi["B"]),
        "the mirror read 4.1 and 4.3 as filed on Ask A": (cr["A"] + cr["B"], ha[CRACKER["A"]] + mi["B"]),
        "the mirror read 4.2 and 4.3 as filed on Ask B": (cr["A"] + cr["B"], mi["A"] + hb[CRACKER["B"]]),
    }
    return dict(ha=ha, hb=hb, cr=cr, mi=mi, cracks=cracks)


def run(target, stamp):
    print("pack: " + stamp)
    m = measure(target)
    print("Ask A (FTE at the fall 2026 census), figures kept of 9:")
    for nm, h in m["ha"].items():
        print("  %-100s %d" % (nm, h))
    print("Ask B (classes under ten at the census), figures kept of 9:")
    for nm, h in m["hb"].items():
        print("  %-100s %d" % (nm, h))
    kc, km = m["cr"]["A"] + m["cr"]["B"], m["mi"]["A"] + m["mi"]["B"]
    (c1, s1, p1), (c2, s2, p2) = pair(kc, km)
    print("cracker (on the call, executes 4.1 to 4.3): A %d of 9, B %d of 9" % (m["cr"]["A"], m["cr"]["B"]))
    print("mirror (default path, one program; natural reads): A %d of 9, B %d of 9" % (m["mi"]["A"], m["mi"]["B"]))
    print("ask sheet weights: cracker %.1f, mirror %.1f, pair %.1f" % (c1, s1, p1))
    print("chart inside the ask layer: cracker %.1f, mirror %.1f, pair %.1f" % (c2, s2, p2))
    worst = max(p1, p2)
    for nm, (k1, k2) in m["cracks"].items():
        (_, _, q1), (_, _, q2) = pair(k1, k2)
        worst = max(worst, q1, q2)
        print("  if %s: cracker %d, mirror %d of %d, pair %.1f (ask sheet), %.1f (chart inside)" % (nm, k1, k2, N_ASK,
                                                                                                q1, q2))
    print("  (both top responses on the call and careful: pair %.1f)" % max(pair(18, 18)[0][2], pair(18, 18)[1][2]))
    print("Cracker keeps: %d of %d ask figures (A %d, B %d)" % (kc, N_ASK, m["cr"]["A"], m["cr"]["B"]))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * km / N_ASK))
    print("Pair ceiling: %.1f (the measured pair, the worse weighting)" % max(p1, p2))
    print("Worst single crack: %.1f" % worst)
    return 0


def main(arg=None):
    folder, scratch, stamp = pack_dir(arg)
    try:
        return run(folder, stamp)
    finally:
        if scratch:
            shutil.rmtree(scratch)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
