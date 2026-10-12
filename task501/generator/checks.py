"""The generator's assertions on the shipped pack and goldens: the input gates, the main call's golden and every
semantic fork row (SF1 to SF17), the rungs below it, the bins, the asks' goldens and every stop of their ladders, the
separation of the call's files from the asks' devices, the distractors' deletion test, the realism sweep and the
container scrub. Every check prints one line; any failure raises."""
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


def pdf_text(p):
    from pypdf import PdfReader
    return re.sub(r"\s+", " ", " ".join(pg.extract_text() for pg in PdfReader(p).pages))


def run(target, golden_dir, w, c):
    print("CHECKS task501")
    files = sorted(os.listdir(target))
    # ---------------------------------------------------------------- input gates
    ok(len(files) >= 10, "input gate: %d files" % len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(fmts) >= 3, "input gate: %d formats %s" % (len(fmts), sorted(fmts)))
    with open(os.path.join(target, PK.FILES["events"]), encoding="utf-8") as f:
        n_events = sum(1 for _ in f) - 1
    ok(n_events >= 25000, "input gate: the events extract has %d rows" % n_events)
    ok(set(files) == set(PK.FILES.values()), "the pack is exactly the declared file list")
    with open(os.path.join(target, PK.FILES["transmittal"]), encoding="utf-8") as f:
        listed = {r["file"] for r in csv.DictReader(f)}
    ok(listed == set(files) - {PK.FILES["transmittal"]}, "H9: the transmittal list names every other shipped file")
    ok(len(PK.DISTRACTORS) >= 2, "two distractors declared")
    # ---------------------------------------------------------------- the main call
    inp = c["inp"]
    R = c["R"]
    ok(R["none"] > 1.0, "golden: the reproduction number with no catch-up is %.4f, above one" % R["none"])
    ok([k for k in W.OPTION_KEYS if R[k] < 1.0] == ["B"], "golden: B is the only option below one (%.4f)" % R["B"])
    for k in ["none"] + W.OPTION_KEYS:
        ok(CM.edge_distance(R[k]) >= 0.03, "SF15 bin: %s %.4f is %.3f from a rounding edge" % (k, R[k], CM.edge_distance(R[k])))
    ok(min(abs(R[k] - 1.0) for k in R) >= 0.09, "SF11: no scenario within 0.09 of one (nearest %.3f)" %
       min(abs(R[k] - 1.0) for k in R))
    ok(c["r1"]["none"] == 1.3 and c["r1"]["B"] == 0.9 and all(c["r1"][k] == 1.3 for k in "ACDE"),
       "graded figures: 1.3, 1.3, 0.9, 1.3, 1.3, 1.3")
    # SF1: the mean-contacts scaling contradicts the standard's R0 and still names B
    full = {a: 0.0 for a in inp.ages}
    q_cbar = W.R0 / ((inp.P.sum(axis=1) * inp.N()).sum() / inp.N().sum())
    r_full_cbar = CM.spectral_radius(q_cbar * inp.P.T)
    ok(r_full_cbar > 18, "SF1: scaled by mean contacts, a wholly susceptible region gives %.1f, not 15" % r_full_cbar)
    cb = {k: CM.R_eigen(inp, None if k == "none" else k, norm="cbar") for k in R}
    ok(min(W.OPTION_KEYS, key=lambda k: cb[k]) == "B" and cb["B"] > 1.0,
       "SF1: under that scaling no option is below one and B is lowest (%.2f), the fallback names B" % cb["B"])
    q = W.R0 / CM.spectral_radius(inp.P)
    ok(abs(CM.spectral_radius(q * inp.P.T) - 15.0) < 1e-9, "SF1: the golden scaling gives 15 at full susceptibility")
    # SF4: the projection's year of birth
    with open(os.path.join(target, PK.FILES["projection"]), encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    ok(all((r["age_at_1_january_2028"].startswith("100") and r["year_of_birth"].startswith("1927")) or
           int(r["year_of_birth"]) == 2027 - int(r["age_at_1_january_2028"]) for r in rows),
       "SF4: every projection row carries year of birth = 2027 - age")
    ok(len(rows) == len(W.COUNTIES) * 101 and len({(r["county"], r["age_at_1_january_2028"]) for r in rows}) == len(rows),
       "axis 15: one projection row per county and age")
    # SF5, SF6, SF7, SF9: the golden family
    fam = CM.family(inp)
    for name, res in fam.items():
        ok(same_bins(res, R) and [k for k in W.OPTION_KEYS if res[k] < 1] == ["B"],
           "SF5-SF9 family %s: same call and the same one-decimal figures" % (name,))
    worst = min(min(CM.edge_distance(res[k]) for k in res) for res in fam.values())
    ok(worst >= 0.025, "bins: every family member at least %.3f from a rounding edge" % worst)
    spread = max(max(abs(res[k] - R[k]) for k in R) for res in fam.values())
    ok(spread <= 0.01, "SF6/SF7: the family's largest move is %.4f" % spread)
    ok(abs(CM.R_eigen(inp, None, P=inp.P.T) - R["none"]) < 0.002, "SF5: the transposed matrix gives the same eigenvalue")
    # SF8: the 70+ group dropped
    d70 = {k: CM.R_eigen(inp, None if k == "none" else k, drop_70=True) for k in R}
    ok(max(abs(d70[k] - R[k]) for k in R) < 0.01 and same_bins(d70, R), "SF8: dropping 70+ keeps every figure in its bin")
    # SF13: infants born 2027 wholly susceptible
    prof2 = dict(inp.profile)
    prof2[2027] = 0.0
    inp2 = CM.CallInputs(prof2, inp.persons, inp.yob, inp.P, inp.natpop, inp.options)
    r13 = CM.golden(inp2)
    ok(same_bins(r13, R) and [k for k in W.OPTION_KEYS if r13[k] < 1] == ["B"], "SF13: infants wholly susceptible, same call and bins")
    # SF3 corridor: the 2018-2025 births' immunity moved 1.5 points either way
    for dlt in (-1.5, 1.5):
        prof3 = dict(inp.profile)
        for y in range(2018, 2026):
            prof3[y] = prof3[y] + dlt
        r3 = CM.golden(CM.CallInputs(prof3, inp.persons, inp.yob, inp.P, inp.natpop, inp.options))
        ok([k for k in W.OPTION_KEYS if r3[k] < 1] == ["B"] and r3["none"] > 1,
           "SF3 corridor: the young cohorts' immunity %+.1f points keeps the call" % dlt)
    # SF10, SF12, SF14: the shipped sentences
    opt_text = pdf_text(os.path.join(target, PK.FILES["options"]))
    std_text = pdf_text(os.path.join(target, PK.FILES["standard"]))
    ok("doses given to people already immune do not count" in opt_text, "SF10: the options paper defines people made immune")
    ok("if nobody in it were immune" in std_text, "SF1: standard 3.2 defines R0 at full susceptibility")
    ok("where more than one does, the one with the lowest cost" in std_text, "SF14: standard 3.6 tie-break")
    ok("1 January of the winter's second year" in std_text, "SF2: standard 3.3 assessment date")
    ok("latest measles immunity profile" in std_text, "SF3: standard 3.4 immunity source")
    ok("counts for the people the options paper expects it to make immune" in std_text, "SF9: standard 3.5")
    ok("If the reproduction number without a catch-up is below one, the department runs none" in std_text, "SF12: standard 3.6")
    ok(sum(inp.persons.values()) == sum(int(r["persons"]) for r in rows), "SF16: the region is the projection's four counties")
    # options paper read back equals what was written
    for k in W.OPTION_KEYS:
        ok([(p["years"], p["made"]) for p in inp.options[k]] == [(p["years"], p["made"]) for p in w["opts"][k]],
           "the options paper's %s reads back as written" % k)
    # ---------------------------------------------------------------- rungs below the golden
    r_avg = {k: CM.R_average(inp, None if k == "none" else k) for k in R}
    r_cw = {k: CM.R_contact_weighted(inp, None if k == "none" else k) for k in R}
    ok(all(v < 1 for v in r_avg.values()), "rung 0: R0 x susceptible share is below one everywhere (%.3f without)" % r_avg["none"])
    ok(CM.round1(r_avg["none"]) == 0.8 and CM.edge_distance(r_avg["none"]) >= 0.02, "rung 0 files 0.8 mid-bin")
    ok(all(v < 1 for v in r_cw.values()), "rung 1: the contact-weighted share is below one everywhere (%.3f without)" % r_cw["none"])
    ok(min(W.OPTION_KEYS, key=lambda k: r_avg[k]) == "E", "rung 0 ranking: E lowest (most people made immune)")
    ok(min(W.OPTION_KEYS, key=lambda k: r_cw[k]) == "E", "rung 1 ranking: E lowest")
    ok(sorted(W.OPTION_KEYS, key=lambda k: r_avg[k]).index("B") >= 2, "position: B third or lower on rung 0")
    imm = {k: np.mean([inp.profile[y] for y in range(W.OPTIONS[k]["years"][0], W.OPTIONS[k]["years"][1] + 1)])
           for k in W.OPTION_KEYS}
    ok(min(imm, key=imm.get) == "D", "rung 2: D is the least immune cohort (%.1f against B %.1f)" % (imm["D"], imm["B"]))
    ok(max(c["made"], key=c["made"].get) == "E", "rung 2: E makes the most people immune (%d)" % c["made"]["E"])
    ok(c["made"]["D"] > c["made"]["B"], "rung 2: D makes more people immune than B")
    ok(CM.round1(r_avg["B"]) != CM.round1(R["B"]) and CM.round1(r_cw["B"]) != CM.round1(R["B"]),
       "no rung below the golden files B's graded 0.9")
    flip = CM.flip_people(inp, "B")
    ok(flip < 0.8 * c["made"]["B"], "flip: B reaches one at %.0f people made immune against %d" % (flip, c["made"]["B"]))
    own = inp.P[3, 3] / inp.P[3].sum()
    popshare = inp.N()[3] / inp.N().sum()
    ok(0.45 <= own <= 0.6 and own > 5 * popshare, "Table 2: 15-19 own-group contact share %.2f against population share %.3f"
       % (own, popshare))
    Nn = inp.natpop
    T = inp.P * Nn[:, None]
    tol = 0.005 * (Nn[:, None] + Nn[None, :]) + 1e-6
    ok(bool(np.all(np.abs(T - T.T) <= tol)), "Table 2 is reciprocal on Table 1's population to its two-decimal rounding")
    ratio = (Nn % 1000) / (Nn // 1000)
    ok(len(set(Nn.tolist())) == len(Nn) and float(np.ptp(ratio)) > 0.5,
       "realism: Table 1's populations are distinct and their last three digits follow no fixed share of the thousands "
       "(spread %.2f)" % float(np.ptp(ratio)))
    ok(abs(c["immune_pct"] - 94.6) < 0.05, "the region is %.2f per cent immune" % c["immune_pct"])
    # ---------------------------------------------------------------- the asks
    f = B.ask_frames(target)
    a1 = c["ask1"]
    for how in ("current", "old", "all"):
        st = A.ask1(f["people"], how)
        ok(all(st[k] != a1[k] for k in a1), "ask 1 stop %s moves every figure" % how)
    rec = f["people"].loc[f["people"]["lho_code"] == "LH27", "lho_recorded"]
    ok(not rec.between("2024-06-24", "2024-07-08").any(), "ask 1 C1: no LH27 recorded within a week of 1 July 2024")
    a2 = c["ask2"]
    stops = {"no merges": dict(merge_how="none"), "one hop": dict(merge_how="one_hop"), "every loaded event": dict(ev_how="all"),
             "every queried line dropped": dict(ev_how="drop_queried"), "current code list": dict(pop="current"),
             "the cracker (loaded events, no merges)": dict(ev_how="all", merge_how="none")}
    for name, kw in stops.items():
        st = A.ask2(f["people"], f["events"], f["log"], f["merges"], **kw)
        moved = sum(st[k][x] != a2[k][x] for k in a2 for x in ("none", "one"))
        need = 3 if name == "one hop" else 10
        ok(moved >= need, "ask 2 stop %s moves %d of 10 figures" % (name, moved))
    log = f["log"]
    reps = set(log.loc[log["outcome"] == "Replaced by corrected line", "replaced_by"])
    ext = set(f["events"]["source_ref"])
    lines_in = set(log["line_ref"]) & ext
    reps_needed = set(log.loc[log["line_ref"].isin(lines_in) & (log["outcome"] == "Replaced by corrected line"), "replaced_by"])
    ok(reps_needed <= ext, "ask 2 fairness: every replaced line in the extract has its corrected line loaded")
    # SF17: a GP return line under a query the office had not closed. The register chased every query still open when
    # the 30 June extract was prepared, so each carries its outcome and closing date by then, and reading an unresolved
    # query as not standing selects the same doses (C1).
    ok(set(log["outcome"]) == {"Confirmed as sent", "Replaced by corrected line", "Withdrawn by practice"},
       "SF17: every query in the log has an outcome, none open")
    ok(bool((log["closed_on"] != "").all()) and bool((log["raised_on"] < log["closed_on"]).all())
       and log["closed_on"].max() <= W.AS_AT.isoformat(),
       "SF17: every query closed after it was raised and by 30 June 2027 (latest %s)" % log["closed_on"].max())
    q_in = log[log["line_ref"].isin(ext)]
    ok(len(q_in) > 500 and bool((q_in["closed_on"] <= W.AS_AT.isoformat()).all()),
       "SF17: the %d queries on lines in the events extract all closed by 30 June 2027" % len(q_in))
    st = A.ask2(f["people"], f["events"], log, f["merges"], ev_how="drop_unresolved")
    ok(st == a2, "SF17: lines under a query not closed as confirmed by 30 June 2027 dropped, every ask 2 figure unchanged")
    chased = [r for r in w["log"] if r.get("chased")]
    on_ext = sorted(r["line_ref"] for r in chased if r["line_ref"] in ext)
    ok(len(chased) == 6 and on_ext == ["GPR-202704-GP3925-001", "GPR-202704-GP4195-001", "GPR-202704-GP4595-001"],
       "SF17: %d confirmed queries still open at the extract were chased and closed, %d of them on extract lines (%s)"
       % (len(chased), len(on_ext), ", ".join(on_ext)))
    gone = A.ask2(f["people"], f["events"][~f["events"]["source_ref"].isin(set(on_ext))], log, f["merges"])
    moved = {"%s %s" % (k, x): gone[k][x] - a2[k][x] for k in a2 for x in ("none", "one") if gone[k][x] != a2[k][x]}
    ok(moved == {"C none": 1, "C one": -1, "D one": 2, "E one": 2},
       "SF17: had those three stayed open and been dropped, ask 2 would move by %s; closed as confirmed, they stand" % moved)
    m = dict(zip(f["merges"]["retired_number"], f["merges"]["surviving_number"]))
    ok(not (set(m) & set(f["people"]["person_id"])), "ask 2: no retired registration is active")
    ok(all(len({m.get(x)}) == 1 for x in m), "ask 2: every retired registration has one surviving registration")
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
    # the guidelines' 12.5.2 read from the previous valid dose or from the previous dose of any kind: the same counts
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
    for how in ("none", "dob_sex", "dob_sex_onset", "window14"):
        st = A.ask3(f["cases"], how)
        moved = sum(st[k][x] != a3[k][x] for k in a3 for x in ("confirmed", "imported"))
        ok(moved == 10, "ask 3 stop %s moves all 10 figures" % how)
    st = A.ask3(f["cases"], "lab", f["lab"])
    ok(sum(st[k]["confirmed"] != a3[k]["confirmed"] for k in a3) == 5, "ask 3 stop lab-confirmed only moves every confirmed figure")
    cs = f["cases"]
    held = dict(zip(cs["legacy_ref"], range(len(cs))))
    refs = cs["comments"].str.extract(A.LEGACY_IN_COMMENT)[0].dropna()
    ok(all(r in held for r in refs), "ask 3 fairness: every back-entered legacy number is held by one migrated record")
    pairs = 0
    for i, r in refs.items():
        a, b = cs.loc[i], cs.iloc[held[r]]
        ok(a["classification"] == b["classification"] and a["date_of_birth"][:4] == b["date_of_birth"][:4]
           and a["importation"] == b["importation"], "ask 3: back-entry %s agrees with %s on classification, year of birth "
           "and importation" % (a["case_id"], b["case_id"]))
        pairs += 1
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
        ok(all(abs(R_only[k] - R[k]) < 1e-12 for k in R), "separation: the call computes from its five files alone")
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
              "random mixing", "contact-adjusted"]
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
        ok(not any(b in low for b in banned), "leak sweep: %s names no method word" % fn)
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
              "stock": {"counted_on": "2027-06-30"}}
    for key, cols in bounds.items():
        with open(os.path.join(target, PK.FILES[key]), encoding="utf-8") as fh:
            rd = list(csv.DictReader(fh))
        for col, lim in cols.items():
            mx = max(r[col] for r in rd if r[col])
            ok(mx <= lim, "H16: %s %s runs to %s, not past %s" % (PK.FILES[key], col, mx, lim))
    cs_ = f["cases"]
    ok(cs_["notified"].max() <= "2027-07-06" and cs_["onset_date"].max() <= "2027-06-30",
       "H16: the case export's dates stop at its run")
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
