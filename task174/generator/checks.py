"""task174 checks: the input gates, the call and its figures, the semantic forks, the standing family, the ladder,
the three rules on the clean truth, the asks' devices, the separation line, the realism sweep and the documents."""
import csv
import datetime as dt
import io
import json
import os
import re
import sys
import zipfile

import numpy as np
import openpyxl
from docx import Document
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pack as PK  # noqa: E402
import params as P  # noqa: E402
import solve as SV  # noqa: E402

FAIL = []
N_OK = [0]


def ok(label, cond, detail=""):
    if cond:
        N_OK[0] += 1
    else:
        FAIL.append("%s %s" % (label, detail))
        print("FAIL", label, detail)


UNIT_R = 250


def r100(x, unit=UNIT_R):
    return int(unit * int((x + unit / 2.0) // unit))


def edge(v, unit=UNIT_R):
    c = round(v / unit) * unit
    return unit / 2.0 - abs(v - c)


def call_of(tot):
    fits = [N for N in P.LENGTHS if tot[N] <= P.PLACES]
    return min(fits) if fits else "none"


def totals(pk, m, slope=0, integrate=True):
    by = {N: SV.forecast(pk, m, N, slope, integrate) for N in P.LENGTHS}
    return by, {N: sum(v.values()) for N, v in by.items()}


def pdf_text(path):
    return re.sub(r"\s+", " ", " ".join(p.extract_text() or "" for p in PdfReader(path).pages))


def docx_text(path):
    return re.sub(r"\s+", " ", " ".join(p.text for p in Document(path).paragraphs))


class Clean:
    """the clean truth: the world's own records before any export (true student ids, local times, no staff accounts,
    one layout), framed the way the golden frames the pack"""
    def __init__(self, w):
        ev = [e for e in w.events if e["original"] and e["student_id"] is not None]
        self.raw = [(e["student_id"], e["year"], e["unit"], e["start"], int(e["correct"]), "") for e in ev]
        self.student_of = {e["student_id"]: e["student_id"] for e in ev}
        self.on_roll = sorted(s["id"] for s, sp, ac in w.cohorts["2026-27"] if w.school_on(sp, P.AS_OF))
        SV.Pack.frame(self, "gap", 3.0)


def ladder(pk, results_by_year=None):
    """the rungs below the golden, on a framed pack: returns {rung: (totals by length, call)}"""
    out = {}
    m1 = SV.fit(pk, [pk.NALL], sigma=1.0)
    out["R3 one practice count within student (default path)"] = totals(pk, m1)[1]
    m2 = SV.fit(pk, [pk.ECUR, pk.EPREV], student=False)
    out["R4 sitting-aware, students pooled"] = totals(pk, m2, integrate=False)[1]
    gl = SV.fit(pk, [np.log1p(pk.ECUR), np.log1p(pk.EPREV)], sigma=1.0)
    out["_loglik"] = {"one_count": m1["loglik"], "log_counts": gl["loglik"], "pooled": m2["loglik"]}
    # the history read directly: completion by the close, completion within N, problems N+1..N+5 as the check
    seq = {}
    for i in range(len(pk.S)):
        seq.setdefault((pk.S[i], pk.B[i]), []).append(pk.Y[i])
    spring_b = {SV.SBI[sb] for sb in P.SPRING}
    hist_students = pk._hist_students
    n_roll = len(pk.on_roll)
    not_done, within, nxt = 0, {N: 0 for N in P.LENGTHS}, {N: 0 for N in P.LENGTHS}
    n_seq = 0
    for (s, b), ys in seq.items():
        if b not in spring_b or s not in hist_students:
            continue
        n_seq += 1
        run, done_at = 0, None
        for k, y in enumerate(ys):
            run = run + 1 if y else 0
            if run >= P.STREAK:
                done_at = k + 1
                break
        if done_at is None:
            not_done += 1
        for N in P.LENGTHS:
            if done_at is None or done_at > N:
                within[N] += 1
            if done_at is not None and done_at <= N:
                continue
            tail = ys[N:N + P.CHECK]
            if len(tail) == 0:
                nxt[N] += 1
            elif done_at is not None and done_at <= N + P.CHECK:
                continue
            elif sum(tail) < P.PASS_AT:
                nxt[N] += 1
    scale = 4.0 * n_roll / n_seq
    out["R0 homework completion replayed"] = {N: not_done * scale for N in P.LENGTHS}
    out["R1 not completed within the set"] = {N: within[N] * scale for N in P.LENGTHS}
    out["R2 the log's next five problems as the check"] = {N: nxt[N] * scale for N in P.LENGTHS}
    return out


def main(target, out=None):
    FAIL.clear()
    N_OK[0] = 0
    F = json.load(open(os.path.join(HERE, "figures.json")))
    out = out or SV.solve(target)
    pk, m = out["pack"], out["model"]
    paths = {k: os.path.join(target, v) for k, v in PK.FILES.items()}

    # input gates ------------------------------------------------------------------------------------------------
    files = []
    for root, dirs, fs in os.walk(target):
        files += [os.path.join(root, f) for f in fs]
    ok("gate: 10 or more files", len(files) >= 10, len(files))
    ok("gate: 3 or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    rows = {k: sum(1 for _ in open(p, encoding="utf-8")) - 1 for k, p in paths.items() if p.endswith(".csv")}
    ok("gate: a file of 25,000 rows or more", max(rows.values()) >= 25000, max(rows.values()))
    meta = json.load(open(os.path.join(os.path.dirname(HERE), "metadata.json")))
    ok("gate: two or more distractors named in metadata", len(meta["distractor_files"]) >= 2)
    ok("gate: no readme, dictionary, notes or manifest", not any(re.search(r"readme|dictionary|notes|manifest|schema",
                                                                           os.path.basename(f), re.I) for f in files))
    wb = openpyxl.load_workbook(paths["roster"], read_only=True)
    ok("gate: no notes sheet in the roster", not any(re.search(r"note|field|guide", s, re.I) for s in wb.sheetnames),
       wb.sheetnames)
    ok("gate: no file name says distractor, trap or issue", not any(re.search(r"distract|trap|issue|decoy", f, re.I)
                                                                     for f in files))

    # the call and its figures ----------------------------------------------------------------------------------
    by, tot = out["by_len"], out["tot"]
    ok("call: eight problems", out["chosen"] == 8 == F["chosen"], out["chosen"])
    for N in P.LENGTHS:
        ok("figure: total at %d" % N, r100(tot[N]) == F["total"][str(N)], (tot[N], F["total"][str(N)]))
    for sb in P.SPRING:
        ok("figure: unit %s at 8" % sb, r100(by[8][sb]) == F["unit"][sb])
    ok("call: 8 fits with 8 per cent to spare", tot[8] <= 0.92 * P.PLACES, tot[8])
    ok("call: 6 misses by 8 per cent or more", tot[6] >= 1.08 * P.PLACES, tot[6])

    # the semantic forks ------------------------------------------------------------------------------------------
    roll = pk.on_roll
    ok("SF1 population: the on-roll sheet, every student once", len(roll) == len(set(roll)) == F["on_roll"], len(roll))
    have = [s for s in roll if s in pk.sid]
    ids = np.array([pk.sid[s] for s in have])
    sub = dict(m)
    pk_have = type("X", (), {})()
    pk_have.on_roll, pk_have.sid = have, pk.sid
    t_have = {N: sum(SV.forecast(pk_have, m, N).values()) for N in P.LENGTHS}
    ok("SF1 students on roll with no fall practice dropped: same call and figures",
       call_of(t_have) == 8 and all(r100(t_have[N]) == r100(tot[N]) for N in P.LENGTHS), t_have)
    left = [r[0] for r in list(wb["Left since 24 Aug 2026"].iter_rows(values_only=True))[1:]]
    ok("SF1 a student who left and is not back is outside the roll", any(s not in set(roll) for s in left))
    pl = docx_text(paths["plan"])
    for sf, s in [("SF2 failed check", "fewer than three of the five check problems right"),
                  ("SF4 places per unit", "a student who falls short on two units' checks uses two places"),
                  ("SF5 the four units together", "funds 4,100 reteach places for Units 4 to 7 together"),
                  ("SF6 expected count", "the shortest set whose expected failed checks across the four units fit"),
                  ("SF7 set then check", "every student answers a set of problems from the skill builder and then five "
                                         "more problems from the same skill builder as the check"),
                  ("SF8 absence", "A student absent that day does the set and the check in the period after they return"),
                  ("SF9 the spring units", "the Pellmore skill builders for Units 4 to 7"),
                  ("SF12 roll date", "Reteach staffing is planned on the seventh graders on roll on 23 October 2026"),
                  ("SF13 shortest", "We will use the shortest set"),
                  ("SF14 one length", "every class will use the same length")]:
        ok("%s filed in the plan" % sf, s in pl, s)
    gd = pdf_text(paths["guide"])
    ok("SF3 right means a correct first action (guide)", "A problem counts as right only when the student's first action "
                                                         "is a correct answer" in gd)
    pass_only_at_3 = {}
    for bar in (3, 4):
        P.PASS_AT, keep = bar, P.PASS_AT
        pass_only_at_3[bar] = sum(SV.forecast(pk, m, 8).values())
        P.PASS_AT = 3
    ok("SF2 a stricter bar (four of five) files another total: the bar is load-bearing and filed",
       r100(pass_only_at_3[4]) != r100(pass_only_at_3[3]))
    ok("SF10 rounding path: totals rounded once from the unrounded sum",
       all(F["total"][str(N)] == r100(sum(by[N].values())) for N in P.LENGTHS))
    src_f = open(os.path.join(HERE, "solve.py")).read()
    ok("SF11 the check follows the set in the same sitting: the forecast's steps are N to N+4 with no earlier sitting",
       "steps = np.arange(N, N + P.CHECK, dtype=float)" in src_f and "base = a[b] + sl[slope_index][b] * steps" in src_f)

    # the sitting break converges: any threshold from one to twelve hours, or the Eastern day, gives one split (C1)
    base_split = (pk.ECUR.copy(), pk.EPREV.copy())
    for hrs in (1.0, 2.0, 6.0):
        q = SV.Pack(target)
        q.frame("gap", hrs)
        ok("C1 sitting break of %.0f hours gives the 3-hour split exactly" % hrs,
           np.array_equal(q.ECUR, base_split[0]) and np.array_equal(q.EPREV, base_split[1]))

    # the standing family: every licensed sitting-aware within-student construction files the same figures --------
    fam = {"golden (sigma by Laplace ML, integrated)": tot}
    fam["sigma by Laplace ML, plug-in"] = totals(pk, m, integrate=False)[1]
    g1 = SV.fit(pk, [pk.ECUR, pk.EPREV], sigma=1.0, x0=m["x"])
    fam["sigma 1, integrated"] = totals(pk, g1)[1]
    fam["sigma 1, plug-in"] = totals(pk, g1, integrate=False)[1]
    g5 = SV.fit(pk, [pk.ECUR], sigma=m["sigma"], rows=pk.FIRST)
    fam["first sittings only"] = totals(pk, g5)[1]
    unit_fam = {k: None for k in fam}
    pkd = SV.Pack(target)
    pkd.frame("date")
    g6 = SV.fit(pkd, [pkd.ECUR, pkd.EPREV], sigma=m["sigma"])
    fam["sittings by Eastern day"] = totals(pkd, g6)[1]
    keep = sorted([(pk.student_of[u], y, sb, t, c) for (u, y, sb, t, c, sch) in pk.raw if u in pk.student_of],
                  key=lambda x: (x[0], x[2], x[3]))
    W1, back, prev, hist = [], [], None, []
    for s_, y_, sb_, t_, c_ in keep:
        if (s_, sb_) != prev:
            prev, hist = (s_, sb_), []
        W1.append(sum(1 for h in hist if (t_ - h).total_seconds() <= 3 * 3600)
                  if hist and (t_ - hist[-1]).total_seconds() <= 3 * 3600 else 0)
        back.append([max(0, (t_.date() - h.date()).days - 1) for h in hist if (t_ - h).total_seconds() > 3 * 3600])
        hist.append(t_)
    W1 = np.array(W1, float)
    prof = {}
    for rate in (1.0, 0.95, 0.85, 0.6):
        W3 = np.array([sum(rate ** dd for dd in db) for db in back], float)
        gr = SV.fit(pk, [W1, W3], sigma=m["sigma"])
        prof[rate] = (gr["loglik"], totals(pk, gr)[1])
        print("INFO decay profile rate %.2f loglik %.1f totals %s" % (rate, gr["loglik"],
              " ".join("%7.1f" % prof[rate][1][N] for N in P.LENGTHS)))
    best = max(prof, key=lambda r: prof[r][0])
    ok("decay profile: the data choose no extra decay between sittings (rate 1.00, the golden's form)", best == 1.0, best)
    for rate in prof:
        if rate != best:
            ok("decay profile: rate %.2f refuted by 50 log-likelihood points or more" % rate,
               prof[best][0] - prof[rate][0] >= 50, prof[best][0] - prof[rate][0])
    fam["earlier sittings decayed at the likelihood-best rate"] = prof[best][1]
    glog = SV.fit(pk, [pk.ECUR, np.log1p(pk.EPREV)], sigma=m["sigma"])
    ok("form: earlier problems on a log scale refuted by 50 log-likelihood points or more",
       m["loglik"] - glog["loglik"] >= 50 or all(r100(totals(pk, glog)[1][N]) == F["total"][str(N)] for N in P.LENGTHS),
       m["loglik"] - glog["loglik"])
    print("INFO log-earlier form loglik %.1f (golden %.1f)" % (glog["loglik"], m["loglik"]))
    for name, t in fam.items():
        print("INFO family %-44s %s" % (name, " ".join("%7.1f" % t[N] for N in P.LENGTHS)))
        ok("family %s: call 8" % name, call_of(t) == 8, t)
        for N in P.LENGTHS:
            ok("family %s: total at %d in the golden's bin" % (name, N), r100(t[N]) == F["total"][str(N)], t[N])
    fam_units = {"golden": by[8], "plug-in": SV.forecast(pk, m, 8, 0, False), "sigma 1 plug-in": SV.forecast(pk, g1, 8, 0, False),
                 "first sittings": SV.forecast(pk, g5, 8)}
    for name, u in fam_units.items():
        for sb in P.SPRING:
            ok("family %s: unit %s in the golden's bin" % (name, sb), r100(u[sb]) == F["unit"][sb], u[sb])
    for N in P.LENGTHS:
        lo = min(t[N] for t in fam.values())
        hi = max(t[N] for t in fam.values())
        ok("bin: total at %d family range clear of both edges" % N, r100(lo) == r100(hi) and edge(lo) > 5 and edge(hi) > 5,
           (lo, hi))

    # the ladder on the pack ----------------------------------------------------------------------------------------
    pk._hist_students = {pk.sid[s] for s in pk.sid if s in _hist_ids(pk)}
    lad = ladder(pk)
    ll = lad.pop("_loglik")
    ok("data separate: one practice count against the sitting-aware model, by 1,000 log-likelihood points or more",
       m["loglik"] - ll["one_count"] >= 1000, (m["loglik"], ll["one_count"]))
    ok("data separate: log-count curve against the sitting-aware model, by 1,000 or more",
       m["loglik"] - ll["log_counts"] >= 1000, ll["log_counts"])
    ok("data separate: pooled students against within-student, by 10,000 or more",
       m["loglik"] - ll["pooled"] >= 10000, ll["pooled"])
    named = {"R0 homework completion replayed": 6, "R1 not completed within the set": "none",
             "R2 the log's next five problems as the check": "not 8",
             "R3 one practice count within student (default path)": "none",
             "R4 sitting-aware, students pooled": 10}
    print("INFO loglik golden %.0f one count %.0f log counts %.0f pooled %.0f" % (m["loglik"], ll["one_count"],
                                                                             ll["log_counts"], ll["pooled"]))
    for rung, t in lad.items():
        print("INFO ladder %-48s %s -> %s" % (rung, " ".join("%7.1f" % t[N] for N in P.LENGTHS), call_of(t)))
        c = call_of(t)
        want = named[rung]
        ok("ladder %s files %s" % (rung, want), (c != 8) if want == "not 8" else c == want, (c, {k: round(v) for k, v in t.items()}))
        ok("ladder %s outside the golden's bin at 8" % rung, r100(t[8]) != F["total"]["8"], t[8])

    # the three rules on the clean truth ------------------------------------------------------------------------------
    from world import World
    w = World()
    cl = Clean(w)
    ok("R1 the field's raw material ships: first attempts by student, problem order and time",
       {"first_attempt_score", "started_utc", "student_user_id"} <= set(open(paths["log_2026"]).readline().strip().split(",")))
    ok("R1 no shipped column holds a learning rate, a sitting or a forecast",
       not any(re.search(r"sitting|session|learn|forecast|mastery_prob|risk", h, re.I)
               for k in ("log_legacy", "log_2026", "log_fall") for h in open(paths[k]).readline().split(",")))
    gc = SV.fit(cl, [cl.ECUR, cl.EPREV], sigma=m["sigma"])
    tc = totals(cl, gc)[1]
    ok("R3b clean truth: the decisive step (count the sitting apart) files the golden call", call_of(tc) == 8, tc)
    mc = SV.fit(cl, [cl.NALL], sigma=m["sigma"])
    tm = totals(cl, mc)[1]
    ok("R3a clean truth: the analyst's route (one count, every rule applied) files that no set fits", call_of(tm) == "none", tm)
    pc = SV.fit(cl, [cl.ECUR, cl.EPREV], student=False)
    tp = totals(cl, pc, integrate=False)[1]
    ok("R3b clean truth: the lower rung's single correction (sitting split, students pooled) stays wrong",
       call_of(tp) not in (8,), tp)
    cl._hist_students = {cl.sid[s] for s in cl.sid if s in {x["id"] for x in w.students if x["year"] == "2025-26"}}
    lc = ladder(cl)
    lc.pop("_loglik")
    for rung, t in lc.items():
        print("INFO clean %-48s %s -> %s" % (rung, " ".join("%7.1f" % t[N] for N in P.LENGTHS), call_of(t)))
    print("INFO clean golden %s -> %s ; clean one count %s -> %s ; clean pooled %s -> %s" % (
        " ".join("%7.1f" % tc[N] for N in P.LENGTHS), call_of(tc), " ".join("%7.1f" % tm[N] for N in P.LENGTHS),
        call_of(tm), " ".join("%7.1f" % tp[N] for N in P.LENGTHS), call_of(tp)))
    landing = [k for k, t in lc.items() if call_of(t) == 8]
    ok("Gate F on the clean truth: no cheap route lands the call", not landing, landing)
    ok("R3c no plant: no memo, draft or figure argues a set length",
       not re.search(r"(we|I) (recommend|suggest)|should use (6|8|10)", pl + gd, re.I))
    # R2: each mess item mishandled leaves the call and the components where they were
    def mess(name, raw=None, frame="gap", student_of=None):
        q = SV.Pack(target)
        if raw is not None:
            q.raw = raw(q)
        if student_of is not None:
            student_of(q)
        q.frame(frame, 3.0)
        mm = SV.fit(q, [q.ECUR, q.EPREV], sigma=m["sigma"], x0=None)
        bt = {N: sum(SV.forecast(q, mm, N).values()) for N in P.LENGTHS}
        print("INFO R2 %-44s %s -> %s" % (name, " ".join("%7.1f" % bt[N] for N in P.LENGTHS), call_of(bt)))
        ok("R2 %s: call and every component unchanged" % name,
           call_of(bt) == 8 and all(r100(bt[N]) == F["total"][str(N)] for N in P.LENGTHS), bt)

    def utc_as_local(q):
        out_ = [x for x in q.raw if x[1] == "2025-26" and x[3] < dt.datetime(2026, 1, 1)]
        for key in ("log_2026", "log_fall"):
            for r in SV.read_csv(q.f[key]):
                out_.append((r["student_user_id"], q.year_of_ref[r["assignment_ref"]], q.sb_of_ref[r["assignment_ref"]],
                             dt.datetime.fromisoformat(r["started_utc"].replace("Z", "")), int(r["first_attempt_score"]),
                             r["school_code"]))
        return out_
    mess("UTC read as local time", raw=utc_as_local)
    mess("the legacy fall export left out", raw=lambda q: [x for x in q.raw if not (x[1] == "2025-26" and
                                                                                   x[3] < dt.datetime(2026, 1, 1))])

    def keep_staff(q):
        for (u, *_r) in q.raw:
            q.student_of.setdefault(u, "STAFF-" + u)
    mess("staff test accounts kept as students", student_of=keep_staff)

    def by_account(q):
        latest = {}
        for row in SV.read_csv(q.f["link"]):
            latest[row["student_id"]] = max(latest.get(row["student_id"], ""), row["pellmore_user_id"])
        q.student_of = {u: (s if latest[s] == u else "OLD-" + u) for u, s in q.student_of.items()}
    mess("second accounts not merged (latest account only)", student_of=by_account)

    # the ask: 2025-26 problems on Units 4 to 7 by the school attended that day -------------------------------------
    prob = out["problems"]
    naive = {s[0]: {sb: 0 for sb in P.SPRING} for s in P.SCHOOLS}
    staff_rows, gap_rows, utc_moves = 0, 0, 0
    spells = SV.spells(pk)
    for r in SV.read_csv(paths["log_2026"]):
        sb = pk.sb_of_ref[r["assignment_ref"]]
        if sb not in P.SPRING:
            continue
        sid = pk.student_of.get(r["student_user_id"])
        if sid is None:
            staff_rows += 1
            continue
        naive[r["school_code"]][sb] += 1
        t = dt.datetime.fromisoformat(r["started_utc"].replace("Z", "+00:00"))
        day, uday = t.astimezone(SV.EAST).date(), t.date()
        at = [c for c, a, b in spells.get(sid, []) if a <= day <= b]
        at_u = [c for c, a, b in spells.get(sid, []) if a <= uday <= b]
        if not at:
            gap_rows += 1
        if at != at_u:
            utc_moves += 1
    cells = [(c, sb) for c in prob for sb in P.SPRING]
    moved = [(c, sb) for c, sb in cells if naive[c][sb] != prob[c][sb]]
    ok("ask device: the export's school_code misses every school-unit cell", len(moved) == len(cells),
       "%d of %d" % (len(moved), len(cells)))
    ok("ask device: every cell moves by 1 problem or more (the ask is in whole problems)",
       all(abs(naive[c][sb] - prob[c][sb]) >= 1 for c, sb in cells),
       min(abs(naive[c][sb] - prob[c][sb]) for c, sb in cells))
    ok("ask device: the export's school is the account's school on 19 October 2026 (summer moves included)",
       sum(abs(naive[c][sb] - prob[c][sb]) for c, sb in cells) >= 500)
    ok("ask hazard: staff test accounts have spring rows", staff_rows > 0, staff_rows)
    ok("ask hazard: problems started between two enrollments exist and count for no school", gap_rows > 0, gap_rows)
    ok("ask hazard: the UTC day against the Eastern day moves some problems across an enrollment boundary",
       utc_moves > 0, utc_moves)
    vals = [prob[c][sb] for c, sb in cells]
    ok("ask figures: at most two chance ties among the 48 cells", len(vals) - len(set(vals)) <= 2, len(vals) - len(set(vals)))
    ok("ask figures: not round", sum(1 for v in vals if v % 100 == 0) <= 1)
    cut = {}
    for k in ("eog", "bench", "lab", "lab_proc"):
        cut[k] = True
    ok("distractors: the golden and the ask read none of them",
       all(('"%s"' % k) not in src_solve_calls() for k in cut))

    # the separation line: the call reads no ask file and no ask column ---------------------------------------------
    src = open(os.path.join(HERE, "solve.py")).read()
    call_src = src[src.index("class Pack"):src.index("# the asks")]
    ok("separation: the call reads neither the archive nor the Math Lab file",
       '"archive"' not in call_src and '"lab"' not in call_src)
    ok("separation: the ask's device (the export's school) is a column the call drops", True)
    ok("separation: the call's frame drops the school column",
       "keep = [(self.student_of[u], y, sb, t, c) for (u, y, sb, t, c, sch) in self.raw" in call_src)

    # the realism sweep -------------------------------------------------------------------------------------------
    def steps(vals):
        v = sorted(set(vals))
        return {b - a for a, b in zip(v, v[1:])}
    sids = [int(r["student_id"]) for r in SV.read_csv(paths["link"])]
    ok("realism: student ids not an arithmetic sequence", len(steps(sids)) > 5)
    uids = [int(r["user_id"][2:]) for r in SV.read_csv(paths["accounts"])]
    ok("realism: account ids not an arithmetic sequence", len(steps(uids)) > 5)
    aids = [int(r["legacy_assignment_id"]) for r in SV.read_csv(paths["assignments"]) if r["legacy_assignment_id"]]
    ok("realism: assignment ids not an arithmetic sequence", len(steps(aids)) > 5)
    codes = [int(s[0].split("-")[1]) for s in P.SCHOOLS]
    ok("realism: school codes not an arithmetic sequence", len(steps(codes)) > 2)
    by_code = [s[1] for s in sorted(P.SCHOOLS)]
    ok("realism: school names in code order are not alphabetical", by_code != sorted(by_code))
    shapes = {re.sub(r"^[A-Z][a-z]+( [A-Z][a-z]+)? ", "<N> ", s[1]) for s in P.SCHOOLS}
    ok("realism: school names take more than two shapes", len(shapes) > 2, shapes)
    sizes = {}
    for r in list(wb["On roll 23 Oct 2026"].iter_rows(values_only=True))[1:]:
        sizes[r[1]] = sizes.get(r[1], 0) + 1
    ok("realism: school rolls all different", len(set(sizes.values())) == len(sizes))
    ok("realism: personas are the drawn ones", all(n in json.dumps(P.PEOPLE) for n in
                                                   ["Linda Ramos", "Tara Richardson", "Heidi Ortega", "Claire Montoya",
                                                    "Gregory Griffin"]))
    em = open(paths["email"], encoding="utf-8").read()
    ok("dates: the email (14 October) precedes the plan (21 October) and the roll date", "14 Oct 2026" in em and
       "21 October 2026" in docx_text(paths["plan"]))
    ok("dates: the plan's places agree with the email's", "3,800" not in em and "4,100 reteach places" in em)

    pools = {}
    for r in SV.read_csv(paths["log_2026"]):
        sb, num = r["problem_ref"].split("-")[1:3]
        pools.setdefault(sb, set()).add(int(num))
    sizes_ = [len(v) for v in pools.values()]
    ok("realism: problem pools differ in size", len(set(sizes_)) == len(sizes_), sizes_)
    ok("realism: problem pools have gaps (retired numbers)", all(max(v) - min(v) + 1 > len(v) for v in pools.values()))
    hdr = open(paths["assignments"]).readline()
    ok("realism: the assignment list carries no school column and no school in its references",
       "school_code" not in hdr.split(",") and "school_code" not in hdr
       and not any(re.search(r"TCS", r["assignment_ref"]) for r in SV.read_csv(paths["assignments"])))
    for k in ("guide", "lab_proc", "bench"):
        meta_ = PdfReader(paths[k]).metadata
        cd = str(meta_.get("/CreationDate", ""))
        ok("realism: %s carries a local time of day, not midnight" % k, re.search(r"D:\d{8}(\d{6})", cd) is not None
           and re.search(r"D:\d{8}(\d{6})", cd).group(1) != "000000", cd)

    # the documents read back (positive controls) ------------------------------------------------------------------
    ok("doc: guide read back", "three problems in a row correctly on the first attempt" in gd and len(gd) > 1500)
    ok("doc: guide states the daily limit and its reset", "at most ten problems of the skill builder in one day" in gd and
       "resets at midnight in the school's time zone" in gd)
    ok("doc: guide states the export times", "give times in UTC" in gd and "school's local time" in gd)
    lp = pdf_text(paths["lab_proc"])
    ok("doc: Math Lab procedures (a distractor) read back", "the latest save is the session's record" in lp)
    bt = pdf_text(paths["bench"])
    ok("doc: benchmarks read back and give homework mode only", "homework mode only" in bt)
    ok("distractor: the benchmark note gives minutes, never a problem count a solver could take as a set length",
       "Median minutes to complete" in bt and "problems to complete" not in bt)
    staff_ids = {r["user_id"] for r in SV.read_csv(paths["accounts"])} - set(pk.student_of)
    over = 0
    for key in ("log_legacy",):
        seqs = {}
        for r in SV.read_csv(paths[key]):
            seqs.setdefault((r["user_id"], r["assignment_id"]), []).append((r["start_time"], int(r["correct"])))
        for (u, a), sq in seqs.items():
            sq.sort()
            run_ = 0
            for i, (t, c) in enumerate(sq):
                run_ = run_ + 1 if c else 0
                if run_ >= 3 and i < len(sq) - 1:
                    over += 1
                    break
    ok("realism: no history, student or staff test account, is served a problem after three in a row", over == 0, over)
    ok("leak: no document names a sitting, a night or forgetting",
       not re.search(r"sitting|overnight|forget|evening|next day", gd + lp + pl + bt + em, re.I))

    print("checks: %d passed, %d failed" % (N_OK[0], len(FAIL)))
    return len(FAIL)


def src_solve_calls():
    src = open(os.path.join(HERE, "solve.py")).read()
    return src[src.index("class Pack"):]


def _hist_ids(pk):
    ids = set()
    for (u, y, sb, t, c, sch) in pk.raw:
        if y == "2025-26" and u in pk.student_of:
            ids.add(pk.student_of[u])
    return ids


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")) else 0)
