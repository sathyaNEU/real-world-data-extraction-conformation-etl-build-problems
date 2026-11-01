"""task145 architecture 2: the golden from target/ alone, and every route the checks price. Reads the shipped files
only (the calendars workbook, the enrolment records, both attendance exports, the grades, the behaviour incidents,
the registrar's records requests), never the generator's truth."""
import csv
import datetime as dt
import os
from collections import defaultdict

import openpyxl

import params as P

D = dt.timedelta
SCHOOL_OF_NO = {v: k for k, v in P.SCHOOL_NO.items()}
LEGACY_NAME = {"Cottonwood Plains Prep": "CPP", "Riverbend Acad": "RBA", "Mesa Vista HS": "MVH", "Sandhill Coll": "SHC"}
LEGACY_CODE = {"Excused": "EX", "Unexcused": "UX", "Medical": "MED", "Suspension": "SUS", "School activity": "ACT"}
LEAVE_CODES = {"DO", "GE", "EX", "W3", "W5", "W9"}
UNVERIFIED = {"TU", "WT"}
TRANSFER = {"TI", "TO", "TU", "W1", "W2", "WT"}
YEARS = {y[0]: y for y in P.YEARS}
_CACHE = {}


def rd(target, name):
    p = os.path.abspath(os.path.join(target, name))
    st = os.stat(p)
    k = ("csv", p, st.st_mtime_ns, st.st_size)
    if k not in _CACHE:
        with open(p, newline="", encoding="utf-8") as fh:
            _CACHE[k] = list(csv.DictReader(fh))
    return _CACHE[k]


def d8(s):
    return dt.date.fromisoformat(s) if s else None


def calendars(target):
    wb = openpyxl.load_workbook(os.path.join(target, "instructional_calendars_2023-24_to_2026-27.xlsx"), data_only=True)
    cal = {}
    for ws in wb.worksheets:
        label = ws.title
        rows = list(ws.iter_rows(values_only=True))
        hdr = [str(x) if x is not None else "" for x in rows[2]]
        cols = {}
        for i, h in enumerate(hdr):
            for s, name in P.SCHOOL_NAME.items():
                if h.strip() == name:
                    cols[s] = i
        for s in P.SCHOOLS:
            cal[(label, s)] = []
        for r in rows[3:]:
            if not r or r[0] is None:
                continue
            d = r[0].date() if isinstance(r[0], dt.datetime) else r[0]
            for s, i in cols.items():
                if str(r[i]).strip().lower() == "instructional":
                    cal[(label, s)].append(d)
    return cal


def day_total(school, d):
    if school == "MVH":
        per = P.MVH_WED if d.weekday() == 2 else P.MVH_STD
        return sum(m for _, m in per), dict(per)
    return P.AM_MIN + P.PM_MIN, {"AM": P.AM_MIN, "PM": P.PM_MIN}


def year_of(d):
    for label, first, fe, ss, last in P.YEARS:
        if first <= d <= dt.date(last.year, 6, 30):
            return label
    return None


def absences(target, half_rule=True, include_sus=True):
    """{(school_year, local_id, school): {date: code}} of the days absent under the attendance regulation (half or more of
    the day's instructional minutes missed; a school activity is not an absence)."""
    k = ("ab", os.path.abspath(target), half_rule, include_sus)
    if k in _CACHE:
        return _CACHE[k]
    out = defaultdict(dict)
    for r in rd(target, "attendance_absences_2023-24.csv"):
        code = LEGACY_CODE[r["Reason"]]
        if code == "ACT" or (code == "SUS" and not include_sus):
            continue
        s = LEGACY_NAME[r["School"]]
        d = dt.datetime.strptime(r["Absence Date"], "%m/%d/%Y").date()
        total, _ = day_total(s, d)
        if (int(r["Minutes Absent"]) * 2 >= total) if half_rule else int(r["Minutes Absent"]) > 0:
            out[("2023-24", r["Student ID"], s)][d] = code
    for r in rd(target, "attendance_absences_2024-25_to_2026-27.csv"):
        code = r["code"]
        if code == "ACT" or (code == "SUS" and not include_sus):
            continue
        s = SCHOOL_OF_NO[r["school_number"]]
        d = d8(r["absence_date"])
        total, parts = day_total(s, d)
        p = r["portion"]
        if p == "FULL":
            m = total
        elif p.startswith("PER:"):
            m = sum(parts[x] for x in p[4:].split(","))
        else:
            m = parts[p]
        if (m * 2 >= total) if half_rule else m > 0:
            out[(year_of(d), r["local_id"], s)][d] = code
    _CACHE[k] = out
    return out


def records(target, link_names=True):
    recs = [dict(r) for r in rd(target, "enrollment_records_2023-24_to_2026-27.csv")]
    for r in recs:
        r["entry"], r["exit"] = d8(r["entry_date"]), d8(r["exit_date"])
        r["school"] = SCHOOL_OF_NO[r["school_number"]]
        r["key"] = r["state_id"] or ("%s|%s|%s" % (r["last_name"].lower(), r["first_name"].lower(), r["birth_date"]))
    # a record opened while the state's id sync was behind carries no state id: the same student's earlier record
    # (same name and date of birth) supplies it
    if link_names:
        by_name = {}
        for r in recs:
            if r["state_id"]:
                by_name[(r["last_name"].lower(), r["first_name"].lower(), r["birth_date"])] = r["state_id"]
        for r in recs:
            if not r["state_id"]:
                r["key"] = by_name.get((r["last_name"].lower(), r["first_name"].lower(), r["birth_date"]), r["key"])
    else:
        for r in recs:
            if not r["state_id"]:
                r["key"] = "unlinked|" + r["local_id"]
    return recs


def resolve_overlaps(recs, overlap=True):
    """One school a day: where a student's record at one school is still open after the same student's next record
    starts at another of the network's schools, the earlier record ends the day before the later one starts."""
    if not overlap:
        for r in recs:
            r["end_eff"] = r["exit"]
        return recs
    by = defaultdict(list)
    for r in recs:
        by[(r["school_year"], r["key"])].append(r)
    for rs in by.values():
        rs.sort(key=lambda x: x["entry"])
        for a, b in zip(rs, rs[1:]):
            a["end_eff"] = min(a["exit"], b["entry"] - D(days=1)) if a["exit"] else b["entry"] - D(days=1)
        for r in rs:
            r.setdefault("end_eff", r["exit"])
    return recs


def requests(target):
    out = defaultdict(list)
    for r in rd(target, "registrar_records_requests_2023-2026.csv"):
        dob = dt.datetime.strptime(r["student_dob"], "%m/%d/%Y").date().isoformat()
        out[(r["student_last_name"].lower(), r["student_first_name"].lower(), dob)].append(d8(r["received"]))
    return out


def is_leaver(r, req, verify="literal", moved=False):
    """Policy JF-7 section 3: a dropout, an equivalency-program withdrawal or an expulsion; or a transfer for which no
    other school requested the records within 45 days of the withdrawal. A move to another of the network's schools is
    not a withdrawal. verify names the checks' variants: 'literal' checks every transfer code, 'unverified' only the
    unconfirmed ones, 'none' counts no transfer, 'all' every unconfirmed transfer."""
    c = r["exit_code"]
    if c in LEAVE_CODES:
        return True
    if c not in TRANSFER or moved:
        return False
    if verify == "none":
        return False
    if verify == "all":
        return c in UNVERIFIED
    if verify == "unverified" and c not in UNVERIFIED:
        return False
    got = req.get((r["last_name"].lower(), r["first_name"].lower(), r["birth_date"]), [])
    return not any(r["exit"] <= g <= r["exit"] + D(days=45) for g in got)


def grades_f(target):
    out = defaultdict(int)
    for r in rd(target, "course_grades_2023-24_to_2026-27.csv"):
        if r["term"] == "S1" and r["grade"] == "F":
            out[(r["school_year"], r["local_id"])] += 1
    return out


def incident_list(target, dedupe=True):
    rows = rd(target, "behavior_incidents_2023-24_to_2026-27.csv")
    if dedupe:
        # a hearing officer's amendment is a new row for the same student and suspension start, often under a
        # re-coded behaviour: the last entered stands
        last = {}
        for r in rows:
            if dedupe == "battery":
                k = (r["local_id"], r["incident_date"], r["behavior_code"], r["action"])
            else:
                k = (r["local_id"], "OSS", r["action_start"]) if r["action"] == "OSS" else (r["incident_id"],)
            if k not in last or r["entered_utc"] > last[k]["entered_utc"]:
                last[k] = r
        rows = sorted(last.values(), key=lambda x: x["incident_id"])
    return rows


def oss_days(target, cal, recs, dedupe=True, enrolled_only=True, label=None):
    """{(school_year, local_id, school): {dates}} of out-of-school suspension days served: each suspension (the
    last-entered row for a student, date and behaviour) runs over the school's instructional days from its start for
    its days, while the student is enrolled there."""
    lid_rec = {(r["school_year"], r["local_id"]): r for r in recs}
    out = defaultdict(set)
    for r in incident_list(target, dedupe):
        if r["action"] != "OSS":
            continue
        d0 = d8(r["action_start"])
        lab = year_of(d0)
        if label is not None and lab != label:
            continue
        sc = SCHOOL_OF_NO[r["school_number"]]
        rc = lid_rec.get((lab, r["local_id"]))
        for x in [x for x in cal[(lab, sc)] if x >= d0][:int(r["action_days"])]:
            if enrolled_only and rc is not None and rc["end_eff"] is not None and x > rc["end_eff"]:
                continue
            out[(lab, r["local_id"], sc)].add(x)
    return out


def fall_features(target, cal, run_min=P.RUN_MIN, half_rule=True, include_sus=True, overlap=True, add_oss=False,
                  ux_only=False, link_names=True, dedupe=True):
    """Per (school_year, student key): the fall semester's runs of days missed, the longest, days missed, days
    enrolled, F grades and incidents. Each instructional day the student was enrolled anywhere in the network is
    read once, in date order, and is missed only when the student was absent at every school enrolled that day."""
    recs = resolve_overlaps(records(target, link_names), overlap)
    ab = absences(target, half_rule, include_sus)
    od = oss_days(target, cal, recs, dedupe) if add_oss else {}
    fs = grades_f(target)
    inc = defaultdict(int)
    for r in incident_list(target, dedupe):
        d = d8(r["incident_date"])
        lab = year_of(d)
        if d <= YEARS[lab][2]:
            inc[(lab, r["local_id"])] += 1
    feat = {}
    for r in sorted(recs, key=lambda x: (x["school_year"], x["key"], x["entry"])):
        label = r["school_year"]
        fe = YEARS[label][2]
        days = [d for d in cal[(label, r["school"])] if d >= r["entry"] and d <= fe and
                (r["end_eff"] is None or d <= r["end_eff"])]
        a = ab.get((label, r["local_id"], r["school"]), {})
        if ux_only:
            miss = {d for d, c in a.items() if c == "UX"}
        else:
            miss = set(a) | od.get((label, r["local_id"], r["school"]), set())
        f = feat.setdefault((label, r["key"]), dict(runs=0, longest=0, rundays=0, absent=0, enrolled=0, fails=0,
                                                    inc=0, grade=int(r["grade"]), rec=[], day={}))
        f["rec"].append(r)
        for d in days:
            f["day"][d] = f["day"].get(d, True) and d in miss
        f["fails"] += fs.get((label, r["local_id"]), 0)
        f["inc"] += inc.get((label, r["local_id"]), 0)
    for f in feat.values():
        seq = [f["day"][d] for d in sorted(f["day"])]
        del f["day"]
        f["enrolled"], f["absent"] = len(seq), sum(seq)
        run = 0
        for x in seq + [False]:
            if x:
                run += 1
                continue
            if run >= run_min:
                f["runs"] += 1
                f["rundays"] += run
            f["longest"] = max(f["longest"], run)
            run = 0
    return feat, recs


def spring_roll(recs, label, day):
    """Student keys with a record open on the spring semester's first day."""
    out = {}
    for r in recs:
        if r["school_year"] != label:
            continue
        if r["entry"] <= day and (r["end_eff"] is None or r["end_eff"] >= day):
            out[r["key"]] = r
    return out


def outcomes(target, recs, verify="literal", years=P.HIST):
    req = requests(target)
    by = defaultdict(list)
    for x in recs:
        by[(x["school_year"], x["key"])].append(x)
    out = {}
    for label in years:
        ss = YEARS[label][3]
        end = dt.date(int(label[:4]) + 1, 6, 30)
        for k in spring_roll(recs, label, ss):
            rs = sorted(by[(label, k)], key=lambda x: x["entry"])
            left = False
            for i, x in enumerate(rs):
                if not (x["exit"] and ss <= x["exit"] <= end):
                    continue
                moved = any(y["entry"] >= x["exit"] and y["school"] != x["school"] for y in rs[i + 1:])
                left = left or is_leaver(x, req, verify, moved)
            out[(label, k)] = left
    return out


def cell_forecast(feat, out, cur_keys, key):
    num, den = defaultdict(int), defaultdict(int)
    for (label, k), left in out.items():
        c = key(feat[(label, k)])
        num[c] += left
        den[c] += 1
    total, missing = 0.0, 0
    for k in cur_keys:
        c = key(feat[(P.CUR, k)])
        if den[c]:
            total += num[c] / den[c]
        else:
            missing += 1
    return total, dict(num), dict(den), missing


def logistic(xs, ys, iters=80):
    """A plain Newton fit with an intercept, enough for a handful of features."""
    import numpy as np
    X = np.column_stack([np.ones(len(xs)), np.array(xs, dtype=float)])
    y = np.array(ys, dtype=float)
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ b))
        g = X.T @ (y - p)
        H = (X * (p * (1 - p))[:, None]).T @ X + 1e-6 * np.eye(X.shape[1])
        step = np.linalg.solve(H, g)
        b += step
        if np.max(np.abs(step)) < 1e-10:
            break
    return b


def logit_forecast(feat, out, cur_keys, fn):
    import numpy as np
    ks = sorted(out)
    b = logistic([fn(feat[k]) for k in ks], [out[k] for k in ks])
    X = np.column_stack([np.ones(len(cur_keys)), np.array([fn(feat[(P.CUR, k)]) for k in cur_keys], dtype=float)])
    return float((1 / (1 + np.exp(-X @ b))).sum())


def tier_for(n):
    for name, seats, price in P.TIERS:
        if n <= seats:
            return name
    return "above Tier 3"


def golden_key(f):
    return min(f["runs"], 2), min(f["fails"], 2)


def solve(target, verify="literal", years=P.HIST, **kw):
    cal = calendars(target)
    feat, recs = fall_features(target, cal, **kw)
    out = outcomes(target, recs, verify, years)
    cur = sorted(spring_roll(recs, P.CUR, P.SPRING_START))
    exp_, num, den, missing = cell_forecast(feat, out, cur, golden_key)
    hist_leavers = {y: sum(v for (lab, k), v in out.items() if lab == y) for y in years}
    with_run = sum(1 for k in cur if feat[(P.CUR, k)]["runs"] > 0)
    hist_with_run = {y: sum(1 for (lab, k) in out if lab == y and feat[(lab, k)]["runs"] > 0) for y in years}
    return dict(cal=cal, feat=feat, recs=recs, out=out, cur=cur, expected=exp_, num=num, den=den, missing=missing,
                tier=tier_for(exp_), hist_leavers=hist_leavers, with_run=with_run, hist_with_run=hist_with_run)


def chronic(f):
    return f["absent"] * 10 >= f["enrolled"]


def rungs(target, S=None):
    """The ladder's routes on the pack: the default path's routes and the decisive one."""
    S = S or solve(target)
    feat, out, cur = S["feat"], S["out"], S["cur"]
    late = {k: v for k, v in out.items() if k[0] == "2025-26"}
    rate = lambda f: f["absent"] / max(1, f["enrolled"])
    R = {}
    R["R0 trailing mean of the three springs' leavers"] = sum(S["hist_leavers"].values()) / len(S["hist_leavers"])
    R["R0b the largest spring's leavers"] = max(S["hist_leavers"].values())
    R["R1 early-warning cells (chronic absence, F grades, two or more incidents)"] = cell_forecast(
        feat, out, cur, lambda f: (chronic(f), min(f["fails"], 2), f["inc"] >= 2))[0]
    R["R1b early-warning cells (chronic absence, F grades)"] = cell_forecast(
        feat, out, cur, lambda f: (chronic(f), min(f["fails"], 2)))[0]
    R["R1c early-warning cells (severe and moderate chronic absence, F grades)"] = cell_forecast(
        feat, out, cur, lambda f: (rate(f) >= 0.20, chronic(f), min(f["fails"], 2)))[0]
    R["R2 logistic on the absence rate, F grades and incidents"] = logit_forecast(
        feat, out, cur, lambda f: [rate(f), min(f["fails"], 4), min(f["inc"], 4)])
    R["R2b logistic on days absent, F grades and incidents"] = logit_forecast(
        feat, out, cur, lambda f: [min(f["absent"], 40), min(f["fails"], 4), min(f["inc"], 4)])
    R["R2c logistic on the absence rate, F grades and incidents, fit on 2025-26"] = logit_forecast(
        feat, late, cur, lambda f: [rate(f), min(f["fails"], 4), min(f["inc"], 4)])
    R["R3 runs cells (decisive)"] = S["expected"]
    R["R3b logistic on runs, F grades and incidents"] = logit_forecast(
        feat, out, cur, lambda f: [min(f["runs"], 3), min(f["fails"], 4), min(f["inc"], 4)])
    return R


def family(target, S=None):
    """Every defensible variant of the decisive route (the run threshold from four to ten days, the cells, the model,
    the closed years used, the codes, the suspension days) and the routes the data refute."""
    S = S or solve(target)
    feat, out, cur = S["feat"], S["out"], S["cur"]
    rate = lambda f: f["absent"] / max(1, f["enrolled"])
    V = {"golden": S["expected"]}
    for k in (4, 6, 7, 8, 10):
        V["runs of %d or more days" % k] = solve(target, run_min=k)["expected"]
    V["unexcused runs only"] = solve(target, ux_only=True)["expected"]
    V["suspension days from the behaviour file added"] = solve(target, add_oss=True)["expected"]
    V["suspension rows dropped"] = solve(target, include_sus=False)["expected"]
    V["cells any run x F"] = cell_forecast(feat, out, cur, lambda f: (f["runs"] > 0, min(f["fails"], 2)))[0]
    V["cells runs to 3 x F to 3"] = cell_forecast(feat, out, cur, lambda f: (min(f["runs"], 3), min(f["fails"], 3)))[0]
    V["cells runs only"] = cell_forecast(feat, out, cur, lambda f: min(f["runs"], 2))[0]
    V["cells runs x F x incidents"] = cell_forecast(feat, out, cur, lambda f: golden_key(f) + (f["inc"] >= 2,))[0]
    V["logistic runs, F, incidents"] = logit_forecast(
        feat, out, cur, lambda f: [min(f["runs"], 3), min(f["fails"], 4), min(f["inc"], 4)])
    V["logistic runs, F, incidents, absence rate"] = logit_forecast(
        feat, out, cur, lambda f: [min(f["runs"], 3), min(f["fails"], 4), min(f["inc"], 4), rate(f)])
    V["logistic any run, F, incidents"] = logit_forecast(
        feat, out, cur, lambda f: [f["runs"] > 0, min(f["fails"], 4), min(f["inc"], 4)])
    V["cells on 2025-26 only"] = solve(target, years=("2025-26",))["expected"]
    V["cells on 2024-25 and 2025-26"] = solve(target, years=("2024-25", "2025-26"))["expected"]
    X = {}
    X["runs of 3 or more days (refuted: three-day spells carry no added risk)"] = solve(target, run_min=3)["expected"]
    X["logistic linear in the longest spell (refuted: misses the closed years' run students by half)"] = \
        logit_forecast(feat, out, cur, lambda f: [min(f["longest"], 30), min(f["fails"], 4), min(f["inc"], 4)])
    X["logistic linear in days inside runs (refuted: the same misfit)"] = logit_forecast(
        feat, out, cur, lambda f: [min(f["rundays"], 40), min(f["fails"], 4), min(f["inc"], 4)])
    L = {}
    L["no overlap rule"] = solve(target, overlap=False)["expected"]
    L["no half-day rule"] = solve(target, half_rule=False)["expected"]
    L["only unconfirmed transfers checked"] = solve(target, verify="unverified")["expected"]
    L["no transfer counted as leaving"] = solve(target, verify="none")["expected"]
    L["every unconfirmed transfer counted as leaving"] = solve(target, verify="all")["expected"]
    L["records without a state id left unlinked"] = solve(target, link_names=False)["expected"]
    L["amended suspensions not collapsed"] = solve(target, dedupe=False)["expected"]
    return V, X, L


def leave_by_longest(S):
    """The closed years' spring leaving rate by the fall's longest spell of days missed."""
    by = defaultdict(lambda: [0, 0])
    for k, left in S["out"].items():
        L = S["feat"][k]["longest"]
        b = str(L) if L < 5 else ("5-9" if L < 10 else "10+")
        by[b][0] += left
        by[b][1] += 1
    return dict(by)


FALL_FIRST, FALL_LAST = YEARS[P.CUR][1], YEARS[P.CUR][2]
MONTHS = [(2026, 8), (2026, 9), (2026, 10), (2026, 11), (2026, 12)]


def ask_b(target, S=None, dedupe=True):
    S = S or solve(target)
    od = oss_days(target, S["cal"], S["recs"], dedupe, label=P.CUR)
    cells = {(s, m): 0 for s in P.SCHOOLS for m in MONTHS}
    for (lab, lid, sc), days in od.items():
        for x in days:
            if (sc, (x.year, x.month)) in cells and x <= FALL_LAST:
                cells[(sc, (x.year, x.month))] += 1
    return cells


def ask_a(target, S=None, link_names=True, overlap=True, add_oss=True, dedupe=True, half_rule=True, label=P.CUR):
    """Each school's fall chronic absence rate by grade (Regulation JH-R section 3): students enrolled ten or more
    instructional days at the school in the fall semester, absent on 10 per cent or more of them. A student's record
    at the school they left ends the day before their entry at the next school; suspension days count as absent."""
    cal = calendars(target)
    fe = YEARS[label][2]
    recs = resolve_overlaps(records(target, link_names), overlap)
    ab = absences(target, half_rule, True)
    od = oss_days(target, cal, recs, dedupe, label=label) if add_oss else {}
    per = defaultdict(lambda: dict(enrolled=0, absent=0, grade=None))
    for r in recs:
        if r["school_year"] != label:
            continue
        sc = r["school"]
        days = [d for d in cal[(label, sc)] if d >= r["entry"] and d <= fe and
                (r["end_eff"] is None or d <= r["end_eff"])]
        a = set(ab.get((label, r["local_id"], sc), {}))
        a |= od.get((label, r["local_id"], sc), set())
        k = (sc, r["key"])
        per[k]["enrolled"] += len(days)
        per[k]["absent"] += sum(1 for d in days if d in a)
        per[k]["grade"] = int(r["grade"])
    cells = {}
    for sc in P.SCHOOLS:
        for g in P.GRADES:
            pop = [v for (s, k), v in per.items() if s == sc and v["grade"] == g and v["enrolled"] >= 10]
            ch = sum(1 for v in pop if v["absent"] * 10 >= v["enrolled"])
            cells[(sc, g)] = (100.0 * ch / len(pop) if pop else 0.0, ch, len(pop))
    return cells


def chronic_network(target, S=None, label=P.CUR):
    """The network's fall chronic absence rate: chronically absent student-school enrolments over all of them."""
    c = ask_a(target, S, label=label)
    return 100.0 * sum(v[1] for v in c.values()) / sum(v[2] for v in c.values())


if __name__ == "__main__":
    import sys
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                           "target")
    S = solve(t)
    print("historical spring leavers", S["hist_leavers"], "on roll", len(S["cur"]), "with a run", S["with_run"],
          "closed years with a run", S["hist_with_run"])
    print("expected %.1f -> %s (missing cells %d)" % (S["expected"], S["tier"], S["missing"]))
    print("leaving by longest spell", leave_by_longest(S))
    for k, v in rungs(t, S).items():
        print("  %-82s %7.1f %s" % (k, v, tier_for(v)))
    if "--family" in sys.argv:
        V, X, L = family(t, S)
        for name, grp in (("family", V), ("refuted", X), ("layer 1 slips", L)):
            print(name)
            for k, v in grp.items():
                print("  %-82s %7.1f %s" % (k, v, tier_for(v)))
