"""The generator's assertions on the shipped pack and goldens: the input gates, the three-rules block (R1 to R3c), the
main call's golden and every semantic fork row (SF1 to SF22), the rungs below it and every rival route the round 1
audit measured, the bins, the asks' goldens and every stop of their ladders, the separation of the call's files from
the asks' devices, the distractors' deletion test, the realism sweep and the container scrub. Every check prints one
line; any failure raises."""
import csv
import datetime as dt
import os
import re
import shutil
import tempfile
import zipfile

import numpy as np

import asks as A
import bundle as B
import callmodel as CM
import golden as G
import pack as PK
import world as W

N_OK = [0]


def ok(cond, msg):
    if not cond:
        raise AssertionError("CHECK FAILED: " + msg)
    N_OK[0] += 1
    print("  ok  %s" % msg)


def same_bins(a, b):
    return all(CM.round1(a[k]) == CM.round1(b[k]) for k in a)


def call_of(R):
    """The standard's choice (3.6) on a set of reproduction numbers."""
    if R["none"] < 1:
        return "none"
    below = [k for k in W.OPTION_KEYS if R[k] < 1]
    if below:
        return min(below, key=lambda k: W.OPTIONS[k]["cost"])
    return min(W.OPTION_KEYS, key=lambda k: R[k])


def pdf_text(p):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in PdfReader(p).pages))


def fmt(R):
    return " ".join("%s %.3f" % (k, v) for k, v in R.items())


def run(target, golden_dir, w, c):
    print("CHECKS task501")
    files = sorted(os.listdir(target))
    # ---------------------------------------------------------------- input gates
    ok(len(files) >= 10, "input gate: %d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(fmts) >= 3, "input gate: %d formats %s" % (len(fmts), sorted(fmts)))
    counts = {}
    for key in ("events", "contacts"):
        with open(os.path.join(target, PK.FILES[key]), encoding="utf-8") as f:
            counts[key] = sum(1 for _ in f) - 1
    ok(counts["events"] >= 25000 and counts["contacts"] >= 25000,
       "input gate: the events extract has %d rows and the survey's contacts file %d" % (counts["events"], counts["contacts"]))
    ok(set(files) == set(PK.FILES.values()), "the pack is exactly the declared file list")
    with open(os.path.join(target, PK.FILES["transmittal"]), encoding="utf-8") as f:
        listed = {r["file"] for r in csv.DictReader(f)}
    ok(listed == set(files) - {PK.FILES["transmittal"]}, "H9: the transmittal list names every other shipped file")
    ok(len(PK.DISTRACTORS) >= 2, "two distractors declared")

    inp = c["inp"]
    R = c["R"]
    parts, contacts = inp.survey
    pool = inp.with_matrix(inp.matrix(None))
    R_all = CM.golden(pool)
    Ps = inp.matrix(CM.summer_diary)
    R_sum = CM.golden(inp.with_matrix(Ps))
    # ---------------------------------------------------------------- the three rules, executed (dataset-generation 7.1)
    std_text = pdf_text(os.path.join(target, PK.FILES["standard"]))
    opt_text = pdf_text(os.path.join(target, PK.FILES["options"]))
    ok(len(parts) == 7560 and len(contacts) == counts["contacts"],
       "R1: the survey's microdata ship (%d diaries, %d contacts), the raw material the next-generation matrix is "
       "built from" % (len(parts), len(contacts)))
    ok(np.allclose(inp.P, CM.survey_matrix(parts, contacts, CM.term_diary).T),
       "R1: the golden's matrix is computed from the contacts file's rows, not read from a table")
    texts_call = std_text + opt_text
    ok(not re.search(r"reproduction number (?:is|of) \d", texts_call) and "matrix" not in texts_call.lower(),
       "R1: no shipped document states a reproduction number or a contact matrix")
    ok(call_of(R_all) == "none" and R_all["none"] < 0.93,
       "R3a analyst test: the next-generation matrix on every diary, every filed rule applied, files no catch-up "
       "(%.3f)" % R_all["none"])
    r_avg = {k: CM.R_average(inp, None if k == "none" else k) for k in R}
    ok(call_of(r_avg) == "none", "R3a: R0 x the susceptible share files no catch-up (%.3f)" % r_avg["none"])
    ok(call_of(R) == "B", "R3b: the same route with only the diaries changed to those kept in term files option B")
    lower = {"every diary": R_all, "summer diaries": R_sum,
             "every diary, reciprocal on the national population": CM.scenarios(
                 inp, P=CM.matrix_variants(inp, inp.matrix(None))["reciprocal national"]),
             "every diary, density-adjusted to the region": CM.scenarios(
                 inp, P=CM.matrix_variants(inp, inp.matrix(None))["density region"]),
             "every diary, transposed": CM.scenarios(inp, P=inp.matrix(None).T),
             "every diary, unknown ages spread": CM.scenarios(inp, P=inp.matrix(None, "spread")),
             "the two periods averaged": CM.scenarios(inp, P=0.5 * inp.P + 0.5 * Ps)}
    for name, res in lower.items():
        ok(call_of(res) == "none", "R3b: %s files no catch-up (%.3f without one)" % (name, res["none"]))
    ok(not os.path.exists(os.path.join(target, "memo")) and not any("draft" in f.lower() for f in files),
       "R3c: no memo, draft or voice ships; no stakeholder figure argues an option or a method")
    # mess items on the call's path, each mishandled, leave the call and the critical components (R2)
    share_all = inp.groups(inp.sus_age()) / inp.N()
    ok(abs(share_all[3] - c["share_1519"]) < 1e-12, "R2: the 15 to 19 susceptible share does not depend on the survey")
    # ---------------------------------------------------------------- the main call
    ok(R["none"] > 1.0, "golden: the reproduction number with no catch-up is %.4f, above one" % R["none"])
    ok([k for k in W.OPTION_KEYS if R[k] < 1.0] == ["B"], "golden: B is the only option below one (%.4f)" % R["B"])
    for k in ["none"] + W.OPTION_KEYS:
        ok(CM.edge_distance(R[k]) >= 0.03, "SF15 bin: %s %.4f is %.3f from a rounding edge" % (k, R[k], CM.edge_distance(R[k])))
    ok(min(abs(R[k] - 1.0) for k in R) >= 0.09, "SF11: no scenario within 0.09 of one (nearest %.3f)" %
       min(abs(R[k] - 1.0) for k in R))
    ok(c["r1"]["none"] == 1.3 and c["r1"]["B"] == 0.9 and all(c["r1"][k] == 1.3 for k in "ACDE"),
       "graded figures: 1.3, 1.3, 0.9, 1.3, 1.3, 1.3")
    # SF1: R0 at full susceptibility, and the mean-contacts scaling it refuses
    q = W.R0 / CM.spectral_radius(inp.P)
    ok(abs(CM.spectral_radius(q * inp.P.T) - 15.0) < 1e-9, "SF1: the golden scaling gives 15 at full susceptibility")
    cbar = (inp.P.sum(axis=1) * inp.N()).sum() / inp.N().sum()
    r_full_cbar = CM.spectral_radius((W.R0 / cbar) * inp.P.T)
    ok(r_full_cbar > 16.5, "SF1: scaled by mean contacts, a wholly susceptible region gives %.1f, not 15" % r_full_cbar)
    cb = CM.scenarios(inp, norm="cbar")
    ok(call_of(cb) == "B" and not same_bins(cb, R), "SF1: under that scaling the call is B with other figures (%s), "
       "refused by standard 3.2" % fmt(cb))
    ok("if nobody in it were immune" in std_text, "SF1: standard 3.2 defines R0 at full susceptibility")
    # SF22: R0 fixed on every diary's contacts and carried to term contacts (per-contact rate from the survey as a whole)
    ratio = CM.spectral_radius(inp.P) / CM.spectral_radius(inp.matrix(None))
    qp = {k: v * ratio for k, v in R.items()}
    ok(15 * ratio > 16.5 and call_of(qp) == "B", "SF22: R0 set on every diary implies %.1f over the winter, against "
       "standard 3.2's 15 over the winter; the call would stay B (%s)" % (15 * ratio, fmt(qp)))
    ok("over the winter if nobody in it were immune" in std_text, "SF22: standard 3.2 sets R0 over the winter")
    # SF2: the winter's term weeks against an average with its holiday weeks
    wint = CM.scenarios(inp, P=(10 / 13) * inp.P + (3 / 13) * Ps)
    ok(call_of(wint) == "B" and wint["none"] < R["none"], "SF2: an average over ten term and three holiday weeks keeps "
       "the call (%.3f without one), refused by standard 3.1 (below one throughout)" % wint["none"])
    ok("stays below one throughout" in std_text and "December to February" in std_text,
       "SF2: standard 3.1 needs the figure below one throughout the winter, December to February")
    ok("1 January of the winter's second year" in std_text, "SF2: standard 3.3 assessment date for population and immunity")
    # SF20: term weekdays only
    wk = [(p, b, d) for p, b, d in parts if CM.term_diary(d) and dt.date.fromisoformat(d).weekday() < 5]
    ids = {p for p, b, d in wk}
    Pw = CM.survey_matrix(wk, [x for x in contacts if x[0] in ids]).T
    rw = CM.scenarios(inp, P=Pw)
    ok(call_of(rw) == "B" and rw["none"] > R["none"], "SF20: term weekdays alone keep the call (%.3f), refused by "
       "standard 3.1's reproduction number (people one case infects over its infection, weekends included)" % rw["none"])
    ok("the average number of people one case infects" in std_text, "SF20: standard 3.1 defines the reproduction number")
    # SF19: diary days balanced over the week in each band and period, so weighting by day of the week moves nothing
    per = {}
    for p, b, d in parts:
        key = (b, CM.term_diary(d), dt.date.fromisoformat(d).weekday())
        per[key] = per.get(key, 0) + 1
    ok(all(v == (24 if k[1] else 48) for k, v in per.items()) and len(per) == W.NG * 2 * 7,
       "SF19: every band carries 24 term and 48 summer diaries on each day of the week (C1: day weights neutral)")
    # SF4: the projection's year of birth
    with open(os.path.join(target, PK.FILES["projection"]), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    ok(all((r["age_at_1_january_2028"].startswith("100") and r["year_of_birth"].startswith("1927")) or
           int(r["year_of_birth"]) == 2027 - int(r["age_at_1_january_2028"]) for r in rows),
       "SF4: every projection row carries year of birth = 2027 - age")
    ok(len(rows) == len(W.COUNTIES) * 101 and len({(r["county"], r["age_at_1_january_2028"]) for r in rows}) == len(rows),
       "axis 15: one projection row per county and age")
    # SF5, SF6, SF7, SF9, SF18: the golden family
    fam = CM.family(inp)
    for name, res in fam.items():
        ok(same_bins(res, R) and call_of(res) == "B", "SF5-SF9, SF18 family %s: same call and the same one-decimal "
           "figures" % (name,))
    worst = min(min(CM.edge_distance(res[k]) for k in res) for res in fam.values())
    ok(worst >= 0.025, "bins: every family member at least %.3f from a rounding edge" % worst)
    spread = max(max(abs(res[k] - R[k]) for k in R) for res in fam.values())
    ok(spread <= 0.025, "SF6/SF7/SF18: the family's largest move is %.4f" % spread)
    # the default's family: every treatment of every diary files no catch-up
    dfam = CM.family(inp, None)
    ok(all(call_of(res) == "none" for res in dfam.values()), "default family: every treatment of every diary files no "
       "catch-up (highest %.3f)" % max(res["none"] for res in dfam.values()))
    ok(all(CM.round1(res["none"]) == 0.9 for res in dfam.values()), "default family: every member files 0.9 without "
       "a catch-up")
    # SF8: the 70+ group dropped
    d70 = CM.scenarios(inp, drop_70=True)
    ok(max(abs(d70[k] - R[k]) for k in R) < 0.015 and same_bins(d70, R), "SF8: dropping 70+ keeps every figure in its bin")
    # SF13: infants born 2027 wholly susceptible
    prof2 = dict(inp.profile)
    prof2[2027] = 0.0
    inp2 = CM.CallInputs(prof2, inp.persons, inp.yob, inp.P, inp.natpop, inp.options)
    r13 = CM.golden(inp2)
    ok(call_of(r13) == "B", "SF13: infants wholly susceptible keep the call (B %.3f), refused by standard 3.4: the "
       "profile gives the 2027 births 50.0 per cent" % r13["B"])
    with open(os.path.join(target, PK.FILES["profile"]), encoding="utf-8") as fh:
        p27 = [r for r in csv.DictReader(fh) if r["year_of_birth"] == "2027"]
    ok(len(p27) == 1 and p27[0]["per_cent_immune"] == "50.0", "SF13: the profile states the 2027 births' share")
    # SF3 corridor: the 2018-2025 births' immunity moved 1.5 points either way
    for dlt in (-1.5, 1.5):
        prof3 = dict(inp.profile)
        for y in range(2018, 2026):
            prof3[y] = prof3[y] + dlt
        r3 = CM.golden(CM.CallInputs(prof3, inp.persons, inp.yob, inp.P, inp.natpop, inp.options))
        ok(call_of(r3) == "B", "SF3 corridor: the young cohorts' immunity %+.1f points keeps the call" % dlt)
    # SF10, SF12, SF14: the shipped sentences
    ok("doses given to people already immune do not count" in opt_text, "SF10: the options paper defines people made immune")
    ok("where more than one does, the one with the lowest cost" in std_text, "SF14: standard 3.6 tie-break")
    ok("latest measles immunity profile" in std_text, "SF3: standard 3.4 immunity source")
    ok("counts for the people the options paper expects it to make immune" in std_text, "SF9: standard 3.5")
    ok("If the reproduction number without a catch-up is below one, the department runs none" in std_text, "SF12: standard 3.6")
    ok(sum(inp.persons.values()) == sum(int(r["persons"]) for r in rows), "SF16: the region is the projection's four counties")
    # SF21: the survey's bands are the only grain it releases
    with open(os.path.join(target, PK.FILES["participants"]), encoding="utf-8") as f:
        pb = {r["age_band"] for r in csv.DictReader(f)}
    with open(os.path.join(target, PK.FILES["contacts"]), encoding="utf-8") as f:
        cbands = {r["contact_age_band"] for r in csv.DictReader(f)}
    ok(pb == set(W.GROUP_LABELS) and cbands == set(W.GROUP_LABELS) | {"Unknown"},
       "SF21: ages ship in the survey's fifteen five-year bands only (and Unknown for contacts)")
    # options paper read back equals what was written
    for k in W.OPTION_KEYS:
        ok([(p["years"], p["made"]) for p in inp.options[k]] == [(p["years"], p["made"]) for p in w["opts"][k]],
           "the options paper's %s reads back as written" % k)
    # ---------------------------------------------------------------- rungs below the golden
    r_cw = {k: CM.R_contact_weighted(inp, None if k == "none" else k, P=inp.matrix(None)) for k in R}
    ok(all(v < 1 for v in r_avg.values()), "rung 0: R0 x susceptible share is below one everywhere (%.3f without)" % r_avg["none"])
    ok(CM.round1(r_avg["none"]) == 0.7 and CM.edge_distance(r_avg["none"]) >= 0.02, "rung 0 files 0.7 mid-bin")
    ok(all(v < 1 for v in r_cw.values()), "rung 1: the contact-weighted share is below one everywhere (%.3f without)" % r_cw["none"])
    ok(CM.round1(R_all["none"]) == 0.9 and CM.edge_distance(R_all["none"]) >= 0.03,
       "rung 2 (every diary) files 0.9 mid-bin (%.3f)" % R_all["none"])
    ok(lower["the two periods averaged"]["none"] < 0.98, "rung 2: the two periods averaged stay below one (%.3f)"
       % lower["the two periods averaged"]["none"])
    pcb = CM.scenarios(pool, norm="cbar")
    ok(call_of(pcb) == "none", "rung 2: every diary with the mean-contacts scaling files no catch-up (%.3f)" % pcb["none"])
    imm = {k: 100 - 100 * sum(p["susceptible"] for p in w["opts"][k]) / sum(p["people"] for p in w["opts"][k])
           for k in W.OPTION_KEYS}
    ok(min(imm, key=imm.get) == "D", "rung 2: the options paper shows D least immune (%.1f against B %.1f)" % (imm["D"], imm["B"]))
    ok(max(c["made"], key=c["made"].get) == "E", "rung 2: E makes the most people immune (%d)" % c["made"]["E"])
    ok(min(W.OPTION_KEYS, key=lambda k: r_avg[k]) == "E" and min(W.OPTION_KEYS, key=lambda k: R_all[k]) == "E",
       "position: E is lowest on rung 0 and on every diary; B is not")
    for name, x in (("rung 0", r_avg), ("rung 1", r_cw), ("every diary", R_all),
                    ("the two periods averaged", lower["the two periods averaged"]), ("summer diaries", R_sum)):
        same = [k for k in R if CM.round1(x[k]) == CM.round1(R[k])]
        ok(not same, "mirror: %s files none of the six graded reproduction numbers (B %.3f against %.3f)" %
           (name, x["B"], R["B"]))
    flip = CM.flip_people(inp, "B")
    ok(flip < 0.75 * c["made"]["B"], "flip: B reaches one at %.0f people made immune against %d" % (flip, c["made"]["B"]))
    own_t = inp.P[3, 3] / inp.P[3].sum()
    own_s = Ps[3, 3] / Ps[3].sum()
    Pt_u = inp.matrix(CM.term_diary, "spread")
    Ps_u = inp.matrix(CM.summer_diary, "spread")
    own_t2 = Pt_u[3, 3] / (Pt_u[3].sum())
    own_s2 = Ps_u[3, 3] / (Ps_u[3].sum())
    ok(min(own_t, own_t2) > 0.52 and max(own_s, own_s2) < 0.19, "the data: 15 to 19-year-olds' contacts with their own "
       "band %.3f in term, %.3f in the summer diaries (more than half, under a fifth, with unknown ages dropped or "
       "spread)" % (own_t, own_s))
    sch = {}
    with open(os.path.join(target, PK.FILES["contacts"]), encoding="utf-8") as f:
        pdate = {p: d for p, b, d in parts}
        pband = {p: b for p, b, d in parts}
        for r in csv.DictReader(f):
            if r["at_school"] == "Y" and 1 <= pband[r["part_id"]] <= 3:
                t = CM.term_diary(pdate[r["part_id"]])
                sch[t] = sch.get(t, 0) + 1
    ok(sch.get(True, 0) > 4000 and sch.get(False, 0) < 0.05 * sch.get(True, 0), "the data: school contacts of 5 to "
       "19-year-olds %d in May, %d in July and August" % (sch.get(True, 0), sch.get(False, 0)))
    ok(abs(c["immune_pct"] - 95.17) < 0.02, "the region is %.2f per cent immune" % c["immune_pct"])
    # ---------------------------------------------------------------- the asks
    f = B.ask_frames(target)
    a1 = c["ask1"]
    for how in ("current", "lh27", "state", "old", "all"):
        st = A.ask1(f["people"], how)
        ok(all(st[k] != a1[k] for k in a1), "ask 1 stop %s moves every figure (%s)" % (how, st))
    ppl = f["people"]
    bt = ppl["postcode"].fillna("").str.startswith("BT")
    ok(bool(ppl.loc[bt, "lho_code"].isin(set(W.REGION_LHO_NEW) | {"LH27"}).all()) and int(bt.sum()) > 900,
       "ask 1 device: %d records with a UK postcode, every one with a regional area code" % int(bt.sum()))
    ni_pids = {p.pid for p in w["people"] if p.status == "ni"}
    ok(set(ppl.loc[bt, "person_id"]) == ni_pids, "SF23 ask 1 fairness: the UK postcodes are exactly the pupils living "
       "in Northern Ireland")
    with open(os.path.join(target, PK.FILES["lho"]), encoding="utf-8") as fh:
        lho_rows = list(csv.DictReader(fh))
    ok(all(r["county"] in set(W.COUNTIES) | {v[1] for v in W.OTHER_LHO.values()} for r in lho_rows)
       and not any(r["county"] in ("Armagh", "Down", "Fermanagh", "Tyrone", "Antrim", "Londonderry") for r in lho_rows),
       "SF23: the national code list holds no office outside the State, so no area code places a UK address")
    notes = zipfile.ZipFile(os.path.join(target, PK.FILES["notes"])).read("word/document.xml").decode("utf-8")
    ok("Local health office of the person's address" in notes, "SF23: the extract notes define lho_code by the address")
    y = A._yob(ppl)
    for k, (lo, hi) in A.OPTION_YEARS.items():
        n = int((bt & (y >= lo) & (y <= hi)).sum())
        ok(n >= 100, "ask 1 device: option %s holds %d records with a UK postcode" % (k, n))
    rec = ppl.loc[ppl["lho_code"] == "LH27", "lho_recorded"]
    ok(not rec.between("2024-06-24", "2024-07-08").any(), "ask 1 C1: no LH27 recorded within a week of 1 July 2024")
    a2 = c["ask2"]
    stops = {"no merges": dict(merge_how="none"), "one hop": dict(merge_how="one_hop"), "every loaded event": dict(ev_how="all"),
             "every queried line dropped": dict(ev_how="drop_queried"), "current code list": dict(pop="current"),
             "UK postcodes kept": dict(pop="lh27"),
             "the cracker (loaded events, no merges)": dict(ev_how="all", merge_how="none")}
    for name, kw in stops.items():
        st = A.ask2(f["people"], f["events"], f["log"], f["merges"], **kw)
        moved = sum(st[k][x] != a2[k][x] for k in a2 for x in ("none", "one"))
        need = 3 if name == "one hop" else 10
        ok(moved >= need, "ask 2 stop %s moves %d of 10 figures" % (name, moved))
    log = f["log"]
    ext = set(f["events"]["source_ref"])
    lines_in = set(log["line_ref"]) & ext
    reps_needed = set(log.loc[log["line_ref"].isin(lines_in) & (log["outcome"] == "Replaced by corrected line"), "replaced_by"])
    ok(reps_needed <= ext, "ask 2 fairness: every replaced line in the extract has its corrected line loaded")
    # SF17: a GP return line under a query the office had not closed
    ok(set(log["outcome"]) == {"Confirmed as sent", "Replaced by corrected line", "Withdrawn by practice"},
       "SF17: every query in the log has an outcome, none open")
    ok(bool((log["closed_on"] != "").all()) and bool((log["raised_on"] < log["closed_on"]).all())
       and log["closed_on"].max() <= W.AS_AT.isoformat(),
       "SF17: every query closed after it was raised and by 30 June 2027 (latest %s)" % log["closed_on"].max())
    st = A.ask2(f["people"], f["events"], log, f["merges"], ev_how="drop_unresolved")
    ok(st == a2, "SF17: lines under a query not closed as confirmed by 30 June 2027 dropped, every ask 2 figure unchanged")
    chased = [r for r in w["log"] if r.get("chased")]
    on_ext = sorted(r["line_ref"] for r in chased if r["line_ref"] in ext)
    ok(len(chased) >= 3, "SF17: %d confirmed queries still open at the extract were chased and closed, %d on extract "
       "lines" % (len(chased), len(on_ext)))
    m = dict(zip(f["merges"]["retired_number"], f["merges"]["surviving_number"]))
    ok(not (set(m) & set(f["people"]["person_id"])), "ask 2: no retired registration is active")
    ev = A.resolve_merges(f["events"], f["merges"]).copy()
    ev = A.clean_events(ev, log)
    ev = ev[ev["person_id"].isin(set(f["people"]["person_id"]))]
    dob = dict(zip(f["people"]["person_id"], f["people"]["date_of_birth"]))
    d = np.array([dt.date.fromisoformat(x).toordinal() for x in ev["date_given"]])
    fb = np.array([dt.date(int(dob[p][:4]) + 1, int(dob[p][5:7]), int(dob[p][8:10])).toordinal() for p in ev["person_id"]])
    ok(int(np.sum(np.abs(d - fb) <= 3)) == 0, "ask 2 C1: no dose within three days of a first birthday")
    ev = ev.assign(o=d).sort_values(["person_id", "o"])
    gaps = ev.groupby("person_id")["o"].diff().dropna()
    ok(int(((gaps >= 24) & (gaps <= 32)).sum()) == 0, "ask 2 C1: no two doses 24 to 32 days apart")
    first = {p_: dt.date(int(v[:4]) + 1, int(v[5:7]), int(v[8:10])).toordinal() for p_, v in dob.items()}
    differ = 0
    asat = dt.date(2027, 6, 30).toordinal()
    for pid, grp in ev[ev["o"] <= asat].groupby("person_id"):
        pv = pa = None
        na = nb = 0
        for o in grp["o"]:
            if o >= first[pid] and (pv is None or o - pv >= 28):
                na, pv = na + 1, o
            if o >= first[pid] and (pa is None or o - pa >= 28):
                nb += 1
            pa = o
        differ += na != nb
    ok(differ == 0, "ask 2 C1: the interval counted from the previous valid dose or from any previous dose gives the "
       "same count for every person")
    ok(f["people"]["person_id"].is_unique and f["events"]["event_number"].is_unique, "keys: person and event numbers unique")
    a3 = c["ask3"]
    for how in ("none", "legacy", "key", "dob_sex", "window14"):
        st = A.ask3(f["cases"], how)
        moved = sum(st[k][x] != a3[k][x] for k in a3 for x in ("confirmed", "imported"))
        ok(moved == 10, "ask 3 stop %s moves all 10 figures" % how)
    st = A.ask3(f["cases"], "lab", f["lab"])
    ok(sum(st[k]["confirmed"] != a3[k]["confirmed"] for k in a3) == 5, "ask 3 stop lab-confirmed only moves every confirmed figure")
    cs = f["cases"]
    held = dict(zip(cs["legacy_ref"], range(len(cs))))
    refs = cs["comments"].str.extract(A.LEGACY_IN_COMMENT)[0].dropna()
    ok(all(r in held for r in refs), "ask 3 fairness: every back-entered legacy number is held by one migrated record")
    for i, r in refs.items():
        a, b = cs.loc[i], cs.iloc[held[r]]
        ok(a["classification"] == b["classification"] and a["date_of_birth"][:4] == b["date_of_birth"][:4]
           and a["importation"] == b["importation"], "ask 3: back-entry %s agrees with %s on classification, year of birth "
           "and importation" % (a["case_id"], b["case_id"]))
    conf = cs[cs["classification"] == "Confirmed"]
    dup = conf[conf.duplicated(["date_of_birth", "sex", "onset_date"], keep=False)]
    legacy_pairs = set(refs.index) | {held[r] for r in refs}
    renot = dup[~dup.index.isin(legacy_pairs)]
    ok(len(renot) == 2 * 6, "SF24 ask 3 device: six illnesses notified twice outside the 2019 back-entry (%d records)"
       % len(renot))
    for _, grp in renot.groupby(["date_of_birth", "sex", "onset_date"]):
        ok(len(grp) == 2 and grp["importation"].nunique() == 1 and grp["county"].nunique() == 1
           and not (set(grp["epi_link"]) & set(grp["case_id"])),
           "SF24 ask 3 fairness: %s notified twice agrees on importation and county, neither linked to the other"
           % "/".join(grp["case_id"]))
    twins = conf[conf.duplicated(["date_of_birth", "sex"], keep=False) & ~conf.index.isin(dup.index)
                 & ~conf.index.isin(legacy_pairs)]
    ok(len(twins) == 2 and twins["onset_date"].nunique() == 2 and (twins["epi_link"] != "").sum() == 1,
       "SF24 ask 3 over-cleaning: the 2024 twins share date of birth and sex, onsets apart, the second epi-linked")
    on = cs["onset_date"]
    ok(not on.between("2018-12-25", "2019-01-07").any() and not on.between("2027-06-23", "2027-07-07").any(),
       "ask 3 C1: no onset within a week of the window's ends")
    # ---------------------------------------------------------------- separation and distractors
    tmp = tempfile.mkdtemp(prefix="t501sep")
    try:
        for fn in files:
            key = [k for k, v in PK.FILES.items() if v == fn][0]
            if key in PK.CALL_FILES:
                shutil.copy(os.path.join(target, fn), tmp)
        R_only = CM.golden(B.call_inputs(tmp))
        ok(all(abs(R_only[k] - R[k]) < 1e-12 for k in R), "separation: the call computes from its seven files alone")
    finally:
        shutil.rmtree(tmp)
    tmp = tempfile.mkdtemp(prefix="t501dis")
    try:
        for fn in files:
            if fn not in [PK.FILES[k] for k in PK.DISTRACTORS]:
                shutil.copy(os.path.join(target, fn), tmp)
        c2 = G.compute(tmp)
        ok(c2["r1"] == c["r1"] and c2["ask1"] == c["ask1"] and c2["ask2"] == c["ask2"] and c2["ask3"] == c["ask3"],
           "distractors: the golden and every ask unchanged with both deleted")
    finally:
        shutil.rmtree(tmp)
    ok(not (set(PK.CALL_FILES) & set(PK.ASK_FILES)), "separation: no file is read by both the call and an ask")
    # ---------------------------------------------------------------- realism and leaks
    ok(len({a1[k] for k in a1}) == 5 and len({a2[k]["none"] for k in a2}) == 5, "realism: no identical counts across options")
    ok(all(a1[k] % 100 and a2[k]["none"] % 100 and a2[k]["one"] % 100 for k in a1), "realism: no round ask counts")
    banned = ["eigen", "next-generation", "next generation", "herd immunity", "mixing matrix", "assortativ", "well-mixed",
              "random mixing", "contact-adjusted", "term time", "term-time", "school term", "school holiday",
              "summer holiday", "northern ireland"]
    texts = {}
    for fn in files:
        p = os.path.join(target, fn)
        if fn.endswith(".pdf"):
            texts[fn] = pdf_text(p)
        elif fn.endswith((".csv", ".txt")):
            texts[fn] = open(p, encoding="utf-8").read()
        elif fn.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(p) as z:
                texts[fn] = " ".join(z.read(n).decode("utf-8", "replace") for n in z.namelist() if n.endswith(".xml"))
    for fn, t in texts.items():
        low = t.lower()
        ok(not any(b in low for b in banned), "leak sweep: %s names no method or device word" % fn)
        ok("\u2014" not in t and "\u2013" not in t, "no em or en dash in %s" % fn)
    for fn in files:
        raw = open(os.path.join(target, fn), "rb").read()
        ok(b"ReportLab" not in raw and b"reportlab" not in raw and b"openpyxl" not in raw and b"python-docx" not in raw,
           "scrub: no library name in %s" % fn)
    allnames = " ".join(texts.values())
    import json as _json
    card = os.path.join(os.path.dirname(os.path.dirname(target)), ".claude", "skills", "fingerprint", "cards", "task501.json")
    people = _json.load(open(card, encoding="utf-8"))["world"]["people"]
    ok(sorted(people) == sorted(W.PEOPLE.values()), "personas are the card's people (guard.py names, seed 501)")
    ok(W.PEOPLE["manager"] in allnames and W.PEOPLE["director"] in allnames and W.PEOPLE["register"] in allnames,
       "personas appear in their documents")
    for g in os.listdir(golden_dir):
        raw = open(os.path.join(golden_dir, g), "rb").read()
        ok(b"python-pptx" not in raw and b"openpyxl" not in raw and b"Matplotlib" not in raw, "scrub: golden %s" % g)
    # H16: no record dated past its extract; forward-looking columns on an allow-list (stock expiry)
    bounds = {"people": {"registered_on": "2027-06-30", "lho_recorded": "2027-06-30"},
              "events": {"date_given": "2027-07-02", "loaded_on": "2027-07-03"},
              "merges": {"merged_on": "2027-06-30"},
              "queries": {"raised_on": "2027-07-03", "closed_on": "2027-07-03"},
              "stock": {"counted_on": "2027-06-30"},
              "participants": {"diary_date": "2023-08-18"}}
    for key, cols in bounds.items():
        with open(os.path.join(target, PK.FILES[key]), encoding="utf-8") as fh:
            rd = list(csv.DictReader(fh))
        for col, lim in cols.items():
            mx = max(r[col] for r in rd if r[col])
            ok(mx <= lim, "H16: %s %s runs to %s, not past %s" % (PK.FILES[key], col, mx, lim))
    cs_ = f["cases"]
    ok(cs_["notified"].max() <= "2027-07-06" and cs_["onset_date"].max() <= "2027-06-30",
       "H16: the case export's dates stop at its run")
    # realism: the survey's counts are not uniform and no participant id block reveals the fieldwork order
    with open(os.path.join(target, PK.FILES["participants"]), encoding="utf-8") as fh:
        prs = list(csv.DictReader(fh))
    first_half = [r["diary_date"] < "2023-06-01" for r in prs[:600]]
    ok(0.2 < sum(first_half) / 600 < 0.5, "realism: participant numbers run in release order, not by fieldwork period "
       "(%.0f per cent of the first 600 in May)" % (100 * sum(first_half) / 600))
    # H8: every file the write-up names ships, in the pack or as a golden
    sub_path = os.path.join(os.path.dirname(target), "submission.md")
    if os.path.exists(sub_path):
        sub = open(sub_path, encoding="utf-8").read()
        named = set(re.findall(r"[\w-]+\.(?:csv|xlsx|pdf|docx|txt|pptx)", sub))
        ok(named <= set(files) | {G.XLSX, G.PPTX}, "H8: every file the write-up names ships (%d names)" % len(named))
        ok("\u2014" not in sub and "\u2013" not in sub, "no em or en dash in submission.md")
    prompt = open(os.path.join(os.path.dirname(target), "prompt.txt"), encoding="utf-8").read()
    ok(G.XLSX in prompt and G.PPTX in prompt and set(os.listdir(golden_dir)) == {G.XLSX, G.PPTX},
       "the goldens are the two files the prompt names")
    print("CHECKS PASSED: %d assertions" % N_OK[0])
