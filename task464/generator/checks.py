"""task464 architecture 9: the generator's assertions, run on the cut pack after every build.

Blocks: input gates; the call and its estimator family (closure, edges, separation, the reflexes); the semantic
fork rows SF1 to SF22; the three rules executed (R1 to R3); Layer 1 mess neutrality (L1); the separation line
between the asks and the call; the ask devices; the realism sweep. Exit 1 on any failure.
"""
import collections, copy, csv, json, os, re, sys, zipfile
import world as W
import answers as A
import family as FAM

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(BASE, "target")
RES = []


SHIPPED = "cd164874"   # the commit that shipped this build, the separation line's reference


def check(label, ok, detail=""):
    RES.append((label, bool(ok), detail))


def edge(v, u):
    c = round(v / u) * u
    return u / 2 - abs(v - c)


def printed(v):
    return A.rnd(v)


def rows_of(path):
    if path.endswith(".csv"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh) - 1
    if path.endswith(".jsonl"):
        with open(path, encoding="utf-8") as fh:
            return sum(1 for _ in fh)
    return 0


def main():
    D = A.Data()
    F = A.figures(D, write=False)
    M = FAM.members(D)
    name = {p["code"]: p["name"] for p in W.PRACTICES}
    call = F["call"]
    pop = A.population(D)
    stay = A.stay_share(D)

    # ------------------------------------------------------------------ input gates
    names = sorted(os.listdir(T))
    exts = {os.path.splitext(n)[1] for n in names}
    check("G1 ten or more files", len(names) >= 10, "%d files" % len(names))
    check("G2 three or more formats", len(exts) >= 3, ", ".join(sorted(exts)))
    big = max(rows_of(os.path.join(T, n)) for n in names)
    check("G3 a file of 25,000 rows or more", big >= 25000, "largest %d rows" % big)
    meta = json.load(open(os.path.join(BASE, "metadata.json")))
    dis = meta.get("distractor_files", [])
    check("G4 two or more distractors declared", len(dis) >= 2 and all(os.path.exists(os.path.join(BASE, d)) for d in dis),
          ", ".join(dis))
    bad = [n for n in names if re.search(r"readme|dictionar|manifest|notes|schema|codebook|field", n, re.I)]
    check("G5 no file describes the data", not bad, ", ".join(bad) or "none")
    sheets = []
    for n in names:
        if n.endswith(".xlsx"):
            with zipfile.ZipFile(os.path.join(T, n)) as z:
                wbx = z.read("xl/workbook.xml").decode()
            sheets += re.findall(r'<sheet [^>]*name="([^"]+)"', wbx)
    check("G6 no notes or readme sheet", not [s for s in sheets if re.search(r"note|readme|about|dictionary", s, re.I)],
          ", ".join(sheets))
    check("G7 every shipped file is in metadata.json", sorted(f["path"][7:] for f in meta["files"]) == names)

    # ------------------------------------------------------------------ the call and its family
    comp = {k: m for k, m in M.items() if k != "passed review at the rate"}
    check("C1 the golden places the sessions at Marrick House", name[call] == "Marrick House Surgery", name[call])
    tops = {k: max(m, key=m.get) for k, m in M.items()}
    check("C2 Marrick House is largest under every member of the family", set(tops.values()) == {call},
          str(sorted(set(tops.values()))))
    dv = [m[call] for m in comp.values()]
    check("C3 Marrick House's competent family spread under 0.4 of the printed unit", max(dv) - min(dv) < 4.0,
          "%.1f to %.1f" % (min(dv), max(dv)))
    allv = [m[call] for m in M.values()]
    check("C4 Marrick House prints the same under every member", len({printed(v) for v in allv}) == 1,
          str(sorted({printed(v) for v in allv})))
    check("C5 the golden's edge distance at least 2 patients", edge(F["expected"][call], 10) >= 2.0,
          "%.2f from the nearest edge" % edge(F["expected"][call], 10))
    check("C6 every member clear of the edge by 1 patient", min(edge(v, 10) for v in allv) >= 1.0,
          "tightest %.2f" % min(edge(v, 10) for v in allv))
    orders = {k: tuple(sorted(m, key=lambda c: -m[c])) for k, m in M.items()}
    check("C7 the full ranking is identical under every member", len(set(orders.values())) == 1,
          " > ".join(W.BY_CODE[c]["key"] for c in orders["golden"]))
    g = F["expected"]
    sec = F["runner_up"]
    check("C8 the call's margin over the runner-up at least 1.2x", g[call] / g[sec] >= 1.2, "%.2fx" % (g[call] / g[sec]))
    check("C9 the call's weakest member clears the runner-up's strongest by 1.15x",
          min(allv) / max(m[sec] for m in M.values()) >= 1.15,
          "%.2fx" % (min(allv) / max(m[sec] for m in M.values())))
    for k in ("default_km", "last_year", "trailing"):
        pick = max(F[k], key=F[k].get)
        check("C10 reflex '%s' names another practice" % k, pick != call, name[pick])
    km = F["default_km"]
    pos = sorted(km, key=lambda c: -km[c]).index(call) + 1
    check("C11 Marrick House sits fourth or lower on the persistence curve", pos >= 4, "position %d of 7" % pos)
    r_full, n_full, _ = A.reauth_rate(D, per=True)
    r_rec, n_rec, _ = A.reauth_rate(D, lo=W.ASOF - 420, per=True)
    spread = max(list(r_full.values()) + list(r_rec.values())) - min(list(r_full.values()) + list(r_rec.values()))
    check("C12 the re-authorisation rate agrees by practice and window within 0.8 points", spread < 0.008,
          "%.2f points" % (100 * spread))
    check("C13 the pooled rate prints 12 per cent", F["reauth_fail_whole"] == 12, "%.2f" % F["reauth_fail_pct"])
    # C15: the forecast's open choices swept wide, the call and the runner-up identical across the whole grid
    import itertools
    pm_, pmed_ = A.pacing(D); stay_ = A.stay_share(D)
    rts = {(f, k): A.reauth_rate(D, follow=f, per=(k == "practice"))[0] for f in (30, 45, 60, 90, 120) for k in ("pooled", "practice")}
    bgs_ = {(gp, k): A.stop_rates(D, gap=gp, split=(k == "split")) for gp in (60, 90, 122, 150, 180) for k in ("split", "flat")}
    pairs = collections.Counter(); m1 = m2 = 9.0
    for rk, bk, pc, st, pend in itertools.product(rts, bgs_, (0, pmed_, pm_, pm_ + 7), (stay_, 1.0), ("lapsed", "rate")):
        e = A.golden(D, pop, rts[rk], bgs_[bk], pc, st, pending=pend)
        o = sorted(e, key=lambda c: -e[c]); pairs[(o[0], o[1])] += 1
        m1 = min(m1, e[o[0]] / e[o[1]]); m2 = min(m2, e[o[1]] / e[o[2]])
    check("C15 the placement and the runner-up hold across 1,600 settings of the forecast's open choices (share window "
          "30 to 120 days pooled or by practice, stop gap 60 to 180 days, pacing, leavers, a passed review)",
          list(pairs) == [(call, sec)] and sum(pairs.values()) == 1600 and m1 > 1.15 and m2 > 1.15,
          "%d settings, tightest margins %.3fx and %.3fx" % (sum(pairs.values()), m1, m2))
    # SF30: critical component 2 counts the patients whose latest statin issue is on such a repeat, not every
    # patient who has held one
    fm = (W.day("2026-02-01"), W.day("2026-03-31"))
    six = lambda tp: tp["cls"] == "Statin" and tp["M"] == 6 and tp["L"] == 56 and fm[0] <= tp["start"] <= fm[1] and tp["code"] == call
    held = sum(1 for pid, c in pop.items() if c == call and any(six(tp) for tp in D.statin_tpl.get(pid, [])))
    on = sum(1 for pid, c in pop.items() if c == call and
             six(D.tpl[[r for r in D.statin_by[pid] if r["code"] == c and r["t"] <= W.ASOF][-1]["ref"]] if
                 not [r for r in D.statin_by[pid] if r["code"] == c and r["t"] <= W.ASOF][-1]["acute"] else {"cls": ""}))
    check("SF30 critical component 2 counts the patients whose latest statin issue is on such a repeat (%d), the wording "
          "the write-up gives, not every patient who has held one (%d)" % (on, held),
          on == F["six_56day_feb_mar_2026"][call] and "latest statin issue on a repeat of six 56-day issues" in
          open(os.path.join(BASE, "submission.md"), encoding="utf-8").read())

    # ------------------------------------------------------------------ semantic fork rows
    reg = D.reg
    on_edge = [pid for pid, c in pop.items() for (cc, a, b, why) in reg[pid] if cc == c and b == W.ASOF]
    check("SF1 nobody's registration ends on 30 November 2026 itself", not on_edge, "%d" % len(on_edge))
    anyp = {}
    for pid, rows in D.statin_by.items():
        if any(W.POP_FROM <= r["t"] <= W.ASOF for r in rows):
            for c in W.BY_CODE:
                if A.registered_at(reg, pid, c, W.ASOF):
                    anyp[pid] = c
    def call_and_print(p2):
        g2 = A.golden(D, p2, rate, bg, pm, stay)
        return max(g2, key=g2.get), printed(g2[call])
    rate, _, _ = A.reauth_rate(D); bg = A.stop_rates(D); pm, _ = A.pacing(D)
    check("SF2 the brief's 'issued a statin by it' against 'by any practice': the call and its figure hold",
          call_and_print({p: c for p, c in anyp.items() if any(r["code"] == c for r in D.statin_by[p])}) == (call, F["call_expected"])
          and len(anyp) - len(pop) <= 5, "%d against %d patients" % (len(anyp), len(pop)))
    acute_only = sum(1 for pid in pop if all(r["acute"] for r in D.statin_by[pid] if r["t"] <= W.ASOF))
    check("SF3 the brief's 'acute or repeat' keeps the new starts not yet on a repeat", acute_only > 0,
          "%d patients on acute issues only" % acute_only)
    ez = sum(1 for r in D.issues if r["vtm"] == "Ezetimibe")
    check("SF4 no ezetimibe issue enters the population", ez == 0 or all(r["cls"] != "Statin" for r in D.issues if r["vtm"] == "Ezetimibe"),
          "%d ezetimibe issues" % ez)
    g_nostay = A.golden(D, pop, rate, bg, pm, 1.0)
    check("SF5 ignoring leavers keeps the call and its printed figure",
          max(g_nostay, key=g_nostay.get) == call and printed(g_nostay[call]) == F["call_expected"],
          "%.1f" % g_nostay[call])
    last_any = max(r["t"] for r in D.statin)
    check("SF6 no statin issue dated after the searches' cover", last_any <= W.ASOF, W.iso(last_any))
    check("SF7 the call's figure is clear of a rounding half, so half up and half even agree", edge(g[call], 10) > 0.5,
          "%.2f" % g[call])
    check("SF8 no tie for the largest", g[call] / g[sec] > 1.05, "%.2fx" % (g[call] / g[sec]))
    only_edge = sum(1 for pid, c in pop.items()
                    if {r["t"] for r in D.statin_by[pid] if r["code"] == c and W.POP_FROM <= r["t"] <= W.ASOF} <= {W.POP_FROM, W.ASOF})
    strict = {pid: c for pid, c in pop.items()
              if any(r["code"] == c and W.POP_FROM < r["t"] < W.ASOF for r in D.statin_by[pid])}
    check("SF9 'from 1 September to 30 November' read without its end days keeps the call and its figure",
          call_and_print(strict) == (call, F["call_expected"]),
          "%d patients whose only issue in the window is on its first or last day" % only_edge)
    moved = [pid for pid, c in pop.items() if len({e[0] for e in reg[pid]}) > 1]
    check("SF10 patients who moved inside the network are counted once, at their practice on 30 November",
          len(set(pop)) == len(pop) and all(A.registered_at(reg, p, pop[p], W.ASOF) for p in moved), "%d moved" % len(moved))
    canc_statin = sum(1 for r in D.issues if r["cls"] == "Statin" and r["cancelled"])
    check("SF11 no statin item was cancelled, so 'issued' reads one way", canc_statin == 0, "%d" % canc_statin)
    deaths = sum(1 for pid in pop for e in reg[pid] if e[3] == "Death")
    check("SF12 deaths leave the register like any other leaver", stay < 1.0, "stay %.4f" % stay)
    check("SF13 a patient first issued after 30 November is outside the figure",
          all(any(W.POP_FROM <= r["t"] <= W.ASOF for r in D.statin_by[p]) for p in pop))
    # asks
    y0, y1 = W.day("2025-01-01"), W.day("2025-12-31")
    raas_pids = {r["pid"] for r in D.issues if r["cls"] in ("ACE inhibitor", "Angiotensin II receptor antagonist")
                 and y0 <= r["t"] <= y1}
    edge_reg = sum(1 for pid in raas_pids for c, a, b, why in reg.get(pid, [])
                   if a in (y0, y0 + 1) or b in (y1, y1 + 1))
    a_strict = A.ask_a(D)
    check("SF14 R1's 'throughout 2025' read inclusively or strictly gives one denominator", edge_reg == 0,
          "%d registrations of R1 patients start or end on the year's edge" % edge_reg)
    ch = A.load_changes(D)
    dpd = lambda text, ref: A.doses_per_day(text, D.tpl[ref]["strength"])
    dose_edits = sum(1 for ref, v in ch.items() for (t, o, n) in v if dpd(o, ref) != dpd(n, ref))
    check("SF15 R1's directions on the prescription differ from the authorisation's for some issues", dose_edits > 0,
          "%d dose edits" % dose_edits)
    a_cur = A.ask_a(D, use_history=False)
    check("SF16 R1 under the directions the repeat lists show misses every practice",
          all(a_cur[c][1] != a_strict[c][1] for c in a_strict))
    a_canc = A.ask_a(D, drop_cancelled=False)
    tot = lambda x: (sum(v[1] for v in x.values()), sum(v[0] for v in x.values()))
    check("SF17 R1 reading a cancelled item as issued moves the network's figure", tot(a_canc) != tot(a_strict),
          "%s against %s" % (tot(a_canc), tot(a_strict)))
    b_h = A.ask_b(D); b_gp = A.ask_b(D, anchor="gp")
    check("SF18 R2's 'the day they started it' and the first GP issue differ at every practice",
          all(A.pct(b_h[c][1], b_h[c][0], 0) != A.pct(b_gp.get(c, (1, 0))[1], b_gp.get(c, (1, 0))[0], 0) for c in b_h))
    tic = collections.defaultdict(list)
    for r in D.issues:
        if r["vtm"] == "Ticagrelor" and r["strength"] == "90mg" and not r["cancelled"]:
            tic[r["pid"]].append(r["t"])
    ev = A.load_events()
    on_anniv = 0
    for pid, rows in ev.items():
        for (t, c, code, term) in rows:
            if code == "1290071000000109" and any(x == A.anniversary(t) for x in tic.get(pid, [])):
                on_anniv += 1
    check("SF19 'on a day later than the first anniversary' is what the golden counts (issues on the day itself: %d)" % on_anniv,
          "> anniversary(t)" in open(os.path.join(BASE, "generator", "answers.py")).read())
    lo, hi = W.day("2024-07-01"), W.day("2025-06-30")
    straddle = 0
    for pid, rows in ev.items():
        mi = [t for (t, c, code, term) in rows if code in W.MI_FAMILY]
        for (t, c, code, term) in rows:
            if code != "1290071000000109": continue
            m = [x for x in mi if abs(t - x) <= 3]
            if m and (lo <= t <= hi) != (lo <= m[0] <= hi):
                straddle += 1
    check("SF20 the specification's 'both between' leaves out the starts whose infarction falls before the window",
          straddle <= 3 and sum(v[0] for v in b_h.values()) > 0, "%d straddling" % straddle)
    ties1 = [c for c in a_strict if abs((1000 * a_strict[c][1] / a_strict[c][0]) % 1 - 0.5) < 1e-9]
    ties2 = [c for c in b_h if abs((100 * b_h[c][1] / b_h[c][0]) % 1 - 0.5) < 1e-9]
    check("SF21 no R1 or R2 percentage sits on a rounding half", not ties1 and not ties2, str(ties1 + ties2))
    mv_tic = [pid for pid in tic if len({e[0] for e in reg.get(pid, [])}) > 1]
    coded_ok = all(A.registered_at(reg, pid, c, t) for pid, rows in ev.items() for (t, c, code, term) in rows
                   if code == "1290071000000109" and lo <= t <= hi)
    check("SF22 each start is coded at the practice the patient was registered with that day, the specification's attribution",
          coded_ok, "%d ticagrelor patients changed practice" % len(mv_tic))

    from pypdf import PdfReader
    brief = " ".join(" ".join((pg.extract_text() or "") for pg in PdfReader(os.path.join(T, "statin_continuity_sessions_brief.pdf")).pages).split())
    g_nostop = A.golden(D, pop, rate, {k: (0.0, 0.0) for k in bg}, pm, stay)
    check("SF23 the brief's 'for whatever reason' keeps stops between reviews in the figure (left out it prints %d)"
          % printed(g_nostop[call]), "for whatever reason" in brief and printed(g[call]) == F["call_expected"])

    spec = " ".join(" ".join((pg.extract_text() or "") for pg in PdfReader(os.path.join(T, "icb_cvd_repeat_return_2025_spec.pdf")).pages).split())
    same_practice = {}
    for pid, rows in ev.items():
        for (t, cc, code, term) in rows:
            if code == "1290071000000109" and lo <= t <= hi:
                mi_t = [x for (x, c2, code2, term2) in rows if code2 in W.MI_FAMILY and abs(x - t) <= 3]
                if not mi_t or not (lo <= mi_t[0] <= hi): continue
                a0, k0 = same_practice.get(cc, (0, 0))
                own = any(r["t"] > A.anniversary(t) and r["code"] == cc for r in D.issues
                          if r["pid"] == pid and r["vtm"] == "Ticagrelor" and r["strength"] == "90mg" and not r["cancelled"])
                same_practice[cc] = (a0 + 1, k0 + own)
    moved_pct = [c for c in b_h if A.pct(b_h[c][1], b_h[c][0], 0) != A.pct(*same_practice.get(c, (1, 0))[::-1], 0)]
    check("SF24 R2's numerator counts 90mg issues at any practice, as the specification says ('at any practice'); the "
          "starting practice alone would move %d practices" % len(moved_pct), "at any practice" in spec)
    check("SF25 practices are compared before rounding, as the brief says; the order is the golden's unrounded order",
          "compared on their figures before rounding" in brief and order_ok if (order_ok := (F["ranking"][0] == call)) else False)

    # SF27: an issue made the same day as a dose change to its repeat, read before the change or after it
    saved = A.directions_at
    def after_issue(D_, changes, ref, t):
        rows = changes.get(ref)
        if not rows: return D_.tpl[ref]["directions"]
        cur = rows[0][1]
        for (when, old, new) in rows:
            if when < t: cur = new
        return cur
    A.directions_at = after_issue
    try:
        a_after = A.ask_a(D)
    finally:
        A.directions_at = saved
    same_day = sum(1 for ref, v in ch.items() for (when, o, n) in v for r in D.issues if r["ref"] == ref and r["t"] == when
                   and dpd(o, ref) != dpd(n, ref)) if False else None
    check("SF27 an issue on the day of a dose change to its repeat, read before or after the change, gives the same R1 figures",
          all(a_after[c][:2] == a_strict[c][:2] for c in a_strict))
    concepts = collections.Counter(code for rows in ev.values() for (t, c, code, term) in rows)
    terms = {term for rows in ev.values() for (t, c, code, term) in rows if code == "22298006"}
    check("SF28 R2's heart attack is the diagnosis however the hospital coded it: STEMI, NSTEMI and 'Heart attack' are "
          "infarctions, unstable angina and an old infarction are not",
          set(W.MI_FAMILY) == {"22298006", "401303003", "401314000"} and all(concepts[c] > 0 for c in
          ("401303003", "401314000", "4557003", "1755008")) and "Heart attack" in terms,
          ", ".join("%s %d" % (c, concepts[c]) for c in ("22298006", "401303003", "401314000", "4557003", "1755008")))
    check("SF29 a changed repeat's directions on a day are the change log's own history, whichever way its system "
          "lists the repeat", all(len(v) == len({x[0] for x in v}) for v in ch.values()) and len(ch) > 500,
          "%d changed repeats" % len(ch))

    npop_c = collections.Counter(pop.values())
    seasons = [A.season_share(D, pop, y) for y in (2024, 2025)]
    carried = {}
    for label, parts in (("2024-25", seasons[:1]), ("2025-26", seasons[1:]), ("both seasons", seasons)):
        num = collections.Counter(); den = collections.Counter()
        for nm_, dn_ in parts: num.update(nm_); den.update(dn_)
        carried[label] = {c: num[c] / den[c] * npop_c[c] for c in den}
    picks = {k: max(v, key=v.get) for k, v in carried.items()}
    check("SF26 the brief's 'each patient's own chance, on what that patient's record shows at the searches' rules "
          "out a practice's earlier-year share carried to its patients, which names another practice in every season",
          "each patient's own chance, on what that patient's record shows at the searches" in brief
          and all(p_ != call for p_ in picks.values()),
          "; ".join("%s %s" % (k, name[v]) for k, v in picks.items()))
    grp = A.reauth_groups(D)
    pooled = F["reauth_fail_pct"] / 100
    dev = max(abs(v[1] - pooled) for v in grp.values())
    check("C14 the share not re-authorised agrees by earlier reviews passed and by issue length within 1.5 points",
          dev < 0.015 and min(v[0] for v in grp.values()) >= 1000,
          ", ".join("%s %s %.1f%% of %d" % (k[0], k[1], 100 * v[1], v[0]) for k, v in sorted(grp.items())))

    # ------------------------------------------------------------------ the three rules, executed
    issue_rows = rows_of(os.path.join(T, "repeat_issues_system_a_2024-01_to_2026-11.csv")) + \
        rows_of(os.path.join(T, "repeat_issues_system_b_2024-01_to_2026-11.jsonl"))
    check("R1 the record ships issue by issue with each repeat's authorised issues", issue_rows > 50000 and
          all(tp["M"] > 0 for tp in D.tpl.values()), "%d issue rows" % issue_rows)
    txt = " ".join(open(os.path.join(T, n), encoding="utf-8", errors="ignore").read()[:200000]
                   for n in names if n.endswith((".csv", ".jsonl")))
    check("R1 no file ships an expected count, a persistence figure or a ranking of the practices",
          not re.search(r"expected|persisten|rank|kaplan|survival", txt, re.I))
    check("R2 the easy route, a persistence curve on months since starting, files another practice",
          max(km, key=km.get) != call, name[max(km, key=km.get)])
    check("R3 changing only the clock, to each patient's own re-authorisation, files Marrick House",
          max(g, key=g.get) == call and max(km, key=km.get) != call)

    # ------------------------------------------------------------------ Layer 1 mess neutrality
    def call_on(Dx):
        popx = A.population(Dx); rx, _, _ = A.reauth_rate(Dx); bx = A.stop_rates(Dx); px, _ = A.pacing(Dx)
        gx = A.golden(Dx, popx, rx, bx, px, A.stay_share(Dx))
        return max(gx, key=gx.get), gx
    Dm = copy.copy(D)
    Dm.reg = {pid: [e for e in eps] for pid, eps in D.reg.items()}
    for pid, eps in Dm.reg.items():
        if len({e[0] for e in eps}) > 1:
            Dm.reg[pid] = eps[-1:]
    c1, g1 = call_on(Dm)
    check("L1 reading moved patients at their current practice only keeps the call", c1 == call, "%.1f" % g1[call])
    act = collections.Counter(tp["pid"] for tp in D.tpl.values() if tp["cls"] == "Statin" and tp["end"] is None
                              and tp["pid"] in pop and tp["code"] == pop[tp["pid"]])
    two = [p for p, k in act.items() if k > 1]
    stale = sum(1 for p in pop if D.statin_by[p][-1]["acute"] and act.get(p, 0) >= 1)
    evx = A.load_events()
    recent_mi = {p for p, rows in evx.items() for (t, cc, code, term) in rows if code == "22298006" and t >= W.ASOF - 60}
    off = [p for p in pop if not D.statin_by[p][-1]["acute"] and D.tpl[D.statin_by[p][-1]["ref"]]["end"] is not None]
    check("L1 every patient's latest statin issue sits on their one active repeat, except a repeat a filed discharge summary ended",
          not two and all(p in recent_mi for p in off),
          "%d with two active; %d ended by a heart attack in the last 60 days; %d restarted on an acute issue with the "
          "stopped repeat still listed" % (len(two), len(off), stale))
    canc_tokens = {e for (e, item) in A.load_cancellations()}
    Dc = copy.copy(D)
    Dc.statin = [r for r in D.statin if r["eps"] not in canc_tokens]
    byc = collections.defaultdict(list)
    for r in Dc.statin:
        byc[r["pid"]].append(r)
    Dc.statin_by = byc
    Dc.made = collections.Counter(r["ref"] for r in Dc.statin if r["ref"])
    c2, g2 = call_on(Dc)
    hit = len(D.statin) - len(Dc.statin)
    check("L1 dropping every item on a prescription with a cancelled item keeps the call and its figure",
          c2 == call and printed(g2[call]) == F["call_expected"], "%d statin items dropped, %.1f" % (hit, g2[call]))
    late = sum(1 for pid, eps in D.reg.items() for (c, a, b, why) in eps
               if b is not None and pid in D.statin_by and b - max(r["t"] for r in D.statin_by[pid]) > 28)
    check("L1 deregistrations dated weeks after the last issue are present and neutral", late > 0, "%d" % late)
    sys_a = sum(1 for r in D.statin if W.BY_CODE[r["code"]]["system"] == "A")
    sys_b = sum(1 for r in D.statin if W.BY_CODE[r["code"]]["system"] == "B")
    check("L1 both clinical systems' layouts carry the call's rows", sys_a > 0 and sys_b > 0, "%d and %d" % (sys_a, sys_b))
    dirs = collections.Counter(tp["directions"] for tp in D.tpl.values() if tp["cls"] == "Statin")
    check("L1 statin dose text is free text in several forms, one dose each", len(dirs) >= 6 and
          all(A.doses_per_day(d) == 1 for d in dirs), "%d forms" % len(dirs))

    # ------------------------------------------------------------------ separation
    statin_refs = {ref for ref, tp in D.tpl.items() if tp["cls"] == "Statin"}
    dose_on_statin = sum(1 for ref, v in ch.items() if ref in statin_refs for (t, o, n) in v
                         if dpd(o, ref) != dpd(n, ref))
    check("S1 no dose edit sits on a statin repeat", dose_on_statin == 0, "%d" % dose_on_statin)
    check("S2 no cancelled item is a statin", canc_statin == 0)
    with open(os.path.join(T, "cvd_product_lookup.csv"), encoding="utf-8") as fh:
        look = list(csv.DictReader(fh))
    check("S3 the asks' medicines are no statin", all(r["bnf_class"] != "Statin" for r in look
                                                         if r["vtm"] in ("Ticagrelor", "Ramipril", "Losartan")))
    check("S4 the call reads no change log, no clinical event and no cancellation of a statin",
          "load_changes" not in A.golden.__code__.co_names and "load_events" not in A.golden.__code__.co_names)

    # ------------------------------------------------------------------ the ask devices
    import ceiling
    rs = ceiling.rows(D)
    check("D1 the cracker misses every asked figure", all(not r[3] for r in rs),
          "keeps " + ", ".join(r[0] for r in rs if r[3]) if any(r[3] for r in rs) else "%d of %d missed" % (len(rs), len(rs)))
    gap_a = min(abs(F["ask_a"][c]["pct"] - A.pct(a_cur[c][1], a_cur[c][0], 1)) for c in a_strict)
    check("D2 the repeat lists' own directions move every practice's R1 by a point or more", gap_a >= 1.0,
          "smallest %.1f" % gap_a)
    sysa = {p["code"] for p in W.PRACTICES if p["system"] == "A"}; sysb = set(a_strict) - sysa
    miss = lambda v, cs, places=1, key="ask_a": [c for c in cs if A.pct(v[c][1], v[c][0], places) == F[key][c]["pct"]]
    by_ref = A.ask_a(D, join="ref", walk="log")
    check("D4 system A's changes read against the repeat each log row names miss every system A practice",
          not miss(by_ref, sysa), "lands " + ", ".join(miss(by_ref, sysa)) if miss(by_ref, sysa) else
          ", ".join("%s %.1f" % (c, A.pct(by_ref[c][1], by_ref[c][0], 1)) for c in sorted(sysa)))
    back = A.ask_a(D, walk="back")
    check("D5 system B's current repeats walked back from their listed directions miss every system B practice",
          not miss(back, sysb), ", ".join("%s %d against %d" % (c, back[c][1], a_strict[c][1]) for c in sorted(sysb)))
    words = A.ask_a(D, parse="words")
    check("D6 doses written in milligrams read as tablets a day miss every practice", not miss(words, a_strict),
          "smallest gap %d patients" % min(abs(words[c][1] - a_strict[c][1]) for c in a_strict))
    cr = A.ask_a(D, join="ref", walk="back")
    check("D7 the walk back by repeat reference (the careful route) misses every practice", not miss(cr, a_strict),
          ", ".join("%s %d" % (c, cr[c][1] - a_strict[c][1]) for c in sorted(a_strict)))
    for mi in ("code", "term", "none"):
        v = A.ask_b(D, mi=mi)
        lands = [c for c in b_h if c in v and v[c][0] and A.pct(v[c][1], v[c][0], 0) == F["ask_b"][c]["pct"]]
        check("D8 R2 with the infarction read as '%s' misses every practice" % {"code": "the one concept 22298006",
              "term": "any term naming a myocardial infarction", "none": "any ticagrelor start"}[mi], not lands,
              ", ".join("%s %s" % (c, A.pct(v[c][1], v[c][0], 0) if c in v and v[c][0] else "-") for c in sorted(b_h)))
    # fair: the change log's history, attached to the repeat held on the day, is the simulator's own dose on every
    # issue the return reads
    import sim as S
    w = S.simulate(S.SEED)
    truth = {}
    for r in w.issues:
        if r["slot"] == "raas":
            truth[(r["pid"], r["t"], r["eps"], r["drug"], r["strength"])] = r["doses"]
    bad = n_iss = 0
    for r in D.issues:
        if r["cls"] in ("ACE inhibitor", "Angiotensin II receptor antagonist") and W.day("2024-01-01") <= r["t"] <= y1:
            k = (r["pid"], r["t"], r["eps"], r["vtm"], r["strength"])
            if k not in truth: continue
            n_iss += 1
            d = A.directions_at(D, ch, r["ref"], r["t"])
            bad += abs(A.doses_per_day(d, r["strength"]) - truth[k]) > 1e-9
    own = A.ask_a(D, per_issue=lambda r, per: truth.get((r["pid"], r["t"], r["eps"], r["vtm"], r["strength"]), per))
    check("D9 the golden's dose is the simulator's own on every 2024-25 ACE inhibitor and ARB issue but the re-sent and "
          "duplicate copies dated across a change, and R1 is the same either way",
          bad <= 5 and n_iss > 50000 and all(own[c][:2] == a_strict[c][:2] for c in a_strict),
          "%d of %d issues differ, every figure the same" % (bad, n_iss))
    # the call's files: byte-identical to the shipped commit, bar the brief's one filed sentence (the determinism
    # repair); the shared repeat lists keep every statin row
    import subprocess, io
    shipped = zipfile.ZipFile(io.BytesIO(subprocess.run(["git", "show", "%s:task464/target.zip" % SHIPPED],
                                                       cwd=BASE, capture_output=True, check=True).stdout))
    same = [n for n in ("repeat_issues_system_a_2024-01_to_2026-11.csv", "repeat_issues_system_b_2024-01_to_2026-11.jsonl",
                        "patient_register_2026-12-01.csv", "cvd_product_lookup.csv")
            if shipped.read(n) == open(os.path.join(T, n), "rb").read()]
    check("S5 the issue extracts, the register and the lookup are byte-identical to the shipped pack", len(same) == 4,
          "%d of 4" % len(same))
    kept = True
    for n, key, prod, cls_of in (("repeat_authorisations_system_a.csv", "Repeat Ref", "Drug", "system_a_drug"),
                                 ("repeat_authorisations_system_b.csv", "authorisation", "product", "system_b_product")):
        cls = {r[cls_of]: r["bnf_class"] for r in look}
        old_rows = [r for r in csv.DictReader(io.StringIO(shipped.read(n).decode("utf-8"))) if cls[r[prod]] == "Statin"]
        new_rows = [r for r in csv.DictReader(open(os.path.join(T, n), encoding="utf-8")) if cls[r[prod]] == "Statin"]
        kept = kept and old_rows == new_rows and len(old_rows) > 1000
    check("S6 both repeat lists keep every statin row as shipped, and no column", kept)
    pdc_twin = sum(1 for r in D.issues if r["cls"] in ("ACE inhibitor", "Angiotensin II receptor antagonist")
                   and not r["cancelled"])
    check("D3 R1 reads more than a few thousand issues", pdc_twin > 20000, "%d" % pdc_twin)

    # ------------------------------------------------------------------ realism sweep
    npop = collections.Counter(pop.values())
    check("Z1 no two practices share a population count", len(set(npop.values())) == len(npop), str(sorted(npop.values())))
    check("Z2 the headline figure is not round", abs(g[call] - round(g[call])) > 0.01 or g[call] % 10 != 0)
    tok = collections.defaultdict(set)
    for r in D.issues:
        tok[r["eps"]].add((r["pid"], r["t"]))
    multi = sum(1 for v in tok.values() if len(v) > 1)
    check("Z3 an EPS prescription id belongs to one patient on one day", multi == 0, "%d ids, %d shared" % (len(tok), multi))
    refs = sorted(int(r[1:]) for r in D.tpl if r.startswith("R"))
    steps = collections.Counter(b - a for a, b in zip(refs, refs[1:]))
    check("Z4 repeat references are not an arithmetic sequence", steps.most_common(1)[0][1] < 0.2 * len(refs),
          "most common step %s" % (steps.most_common(1),))
    people = set(W.PEOPLE.values())
    check("Z5 the personas are the drawn names", people == {"Dorothy Mitchell", "Hollie Kirk", "Stuart Newman"})
    last_reg = max(a for eps in reg.values() for (c, a, b, why) in eps)
    check("Z6 no registration starts after the searches", last_reg <= W.ASOF, W.iso(last_reg))

    fails = [r for r in RES if not r[1]]
    for label, ok, detail in RES:
        print("%s %-96s %s" % ("PASS" if ok else "FAIL", label, detail))
    print("%d checks, %d failed" % (len(RES), len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
