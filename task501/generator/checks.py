"""The generator's assertions on the shipped pack and goldens: the input gates, the three-rules block (R1 to R3c), the
main call's golden and every semantic fork row (SF1 to SF31), the rungs below it and every rival route the round 1
audit measured, the bins, the ask's golden with both its devices' forcing, every rival reading and every stop of its
ladder, the separation of the call's files from the ask's devices, the distractors' deletion test, the realism sweep
and the container scrub. Every check prints one line; any failure raises."""
import csv
import datetime as dt
import os
import re
import shutil
import tempfile
import zipfile

import numpy as np
import pandas as pd

import asks as A
import bundle as B
import callmodel as CM
import golden as G
import pack as PK
import sim as S
import verify as V
import world as W

N_OK = [0]

# A file or sheet whose job is to tell the analyst what the data is (dataset-generation section 3, house fix H9): the
# names leak.py's first sweep refuses, plus a transmittal or file list, which is a manifest by another name.
DESCRIBE_NAME = re.compile(
    r"(?<![a-z])(read_?me|data_?dictionar\w*|dictionar(y|ies)|codebook|field_?notes|field_?guide|"
    r"fields?_(guide|notes|list|descriptions?)|\w*_fields|manifest|extract_contents|file_list|file_layout|glossary|"
    r"column_(notes|descriptions?)|data_?notes|how_to_read|about_this|export_notes|extract_notes|feed_notes|desk_notes|"
    r"data_team_notes|definitions|schema|layouts?_notes|handling_notes|release_notes|transmittal\w*)(?![a-z])", re.I)
DESCRIBE_SHEET = re.compile(r"^(read ?me|notes?|dictionary|data dictionary|definitions|glossary|fields|field notes|"
                            r"about|about this (file|workbook)|how to (read|use)( this)?|columns?|participants file|"
                            r"contacts file|files?)$", re.I)


def shipped_columns(target, files):
    """Each data file's header as the verifier reads it (csv), or a workbook's first row on every sheet."""
    import openpyxl
    out = {}
    for fn in files:
        if fn.endswith(".csv"):
            with open(os.path.join(target, fn), encoding="utf-8", newline="") as f:
                out[fn] = list(next(csv.reader(f)))
        elif fn.endswith(".xlsx"):
            wb = openpyxl.load_workbook(os.path.join(target, fn), read_only=True)
            out[fn] = [str(c) for ws in wb.worksheets for c in next(ws.iter_rows(max_row=1, values_only=True)) if c]
    return out


def identifier_columns(target, files):
    """The data files' column names written as identifiers (snake_case, a digit or interior capitals), what a
    dictionary lists; a plain word heading a column is what any document says."""
    return {c for cs in shipped_columns(target, files).values() for c in cs
            if len(c) >= 4 and ("_" in c or re.search(r"\d", c) or re.search(r"[a-z][A-Z]", c))}


def columns_named(text, ident):
    return {c for c in ident if re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % re.escape(c), text)}


def files_named(text, files, own=None):
    return [o for o in files if o != own and o in text]


def describing_files(target, files):
    """The shipped files that describe the data, by name, by sheet name or by content: a document naming four or more
    of the data files' columns written as identifiers, or any file naming three or more of the other shipped files."""
    import openpyxl
    hits = [("name", fn) for fn in files if DESCRIBE_NAME.search(os.path.splitext(fn)[0])]
    for fn in files:
        if fn.endswith(".xlsx"):
            for sh in openpyxl.load_workbook(os.path.join(target, fn), read_only=True).sheetnames:
                if DESCRIBE_SHEET.match(sh.strip()):
                    hits.append(("sheet %s" % sh, fn))
    ident = identifier_columns(target, files)
    texts = {fn: V.pdf_text(target, fn) for fn in files if fn.endswith(".pdf")}
    for fn in files:
        if fn.endswith(".csv"):
            texts[fn] = open(os.path.join(target, fn), encoding="utf-8").read()
    for fn, t in texts.items():
        if fn.endswith(".pdf"):
            named = columns_named(t, ident)
            if len(named) >= 4:
                hits.append(("columns %s" % sorted(named)[:6], fn))
        others = files_named(t, files, fn)
        if len(others) >= 3:
            hits.append(("lists %d other files" % len(others), fn))
    return hits, texts, ident


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
    # H9 (dataset-generation section 3): no shipped file describes the data. Positive controls first, through the same
    # patterns and the same extractor: the patterns refuse the describing files this pack used to ship, and the
    # verifier's PDF and csv reads find text known to be there, so an empty search cannot pass for a clean one.
    for old in ("nds_case_export_fields", "nscs_2023_public_file_codebook", "register_extract_notes_2027-07",
                "transmittal_list_2027-07-12"):
        ok(bool(DESCRIBE_NAME.search(old)), "H9 control: the name pattern refuses %s" % old)
    ok(bool(DESCRIBE_SHEET.match("About")) and bool(DESCRIBE_SHEET.match("Contacts file"))
       and not DESCRIBE_SHEET.match("Population"), "H9 control: the sheet pattern refuses About and Contacts file")
    hits, h9_texts, h9_ident = describing_files(target, files)
    ok(all(len(h9_texts[fn]) > 200 for fn in files if fn.endswith(".pdf"))
       and "the average number of people one case infects" in h9_texts[PK.FILES["standard"]]
       and "made immune" in h9_texts[PK.FILES["options"]],
       "H9 control: the verifier's extractor reads every shipped PDF's text (the standard's 3.1 found)")
    probe = "%s %s %s" % (PK.FILES["people"], PK.FILES["events"], PK.FILES["merges"])
    ok(len(files_named(probe, files)) == 3, "H9 control: the file-list search finds three file names in a list")
    old_notes = "person_number, date_of_birth, sex, lho_code, lho_recorded, postcode and date_given"
    ok(columns_named(old_notes, h9_ident) == {"person_number", "date_of_birth", "lho_code", "lho_recorded", "date_given"},
       "H9 control: the column search finds the five identifier columns in a line of the extract notes once shipped "
       "(sex and postcode are plain words it leaves alone)")
    ok(not hits, "H9: no shipped file describes the data, by name, sheet or content (no dictionary, field notes, "
       "extract notes, codebook, manifest or transmittal list): %s" % (hits or "none of %d" % len(files)))
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
    # SF25: the school regime the winter runs in, a premise of the window that no file states as a calendar (a pin naming
    # term would file the decisive step): the survey's own at_school field separates its two periods, the options paper
    # puts the school team in schools from 15 September, and standard 3.1 binds the figure throughout December to February
    band_of = {lab: k for k, lab in enumerate(W.GROUP_LABELS)}
    n_all, n_sch, n_1519, s_1519, phys = {True: 0, False: 0}, {True: 0, False: 0}, {True: 0, False: 0}, \
        {True: 0, False: 0}, []
    with open(os.path.join(target, PK.FILES["contacts"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            t = CM.term_diary(pdate[r["part_id"]])
            n_all[t] += 1
            n_sch[t] += r["at_school"] == "Y"
            if pband[r["part_id"]] == 3:
                n_1519[t] += 1
                s_1519[t] += r["at_school"] == "Y"
            if r["physical"] == "Y":
                phys.append((r["part_id"], band_of.get(r["contact_age_band"], -1)))
    sh = {t: n_sch[t] / n_all[t] for t in (True, False)}
    sh15 = {t: s_1519[t] / n_1519[t] for t in (True, False)}
    ok(0.170 < sh[True] < 0.180 and 0.017 < sh[False] < 0.027 and 0.59 < sh15[True] and sh15[False] < 0.015,
       "SF25 closure in the data: at-school contacts are %.1f per cent of all contacts in the May diaries against %.1f "
       "in July and August (15 to 19-year-olds %.1f against %.1f)" % (100 * sh[True], 100 * sh[False], 100 * sh15[True],
                                                                       100 * sh15[False]))
    ok("between 15 September and 20 November" in opt_text and "stays below one throughout" in std_text,
       "SF25: the options paper's school sessions run from 15 September and standard 3.1 binds the figure throughout "
       "December to February")
    ok(not re.search(r"term time|term-time|school term|school holiday|summer holiday|school calendar|school year",
                     (std_text + " " + opt_text).lower()),
       "SF25: no call document names term, the holidays or a school calendar (the pin refused, Tried and rejected)")
    # SF26: a contact is a row the contacts file lists, physical or not (the producing system carries it: physical is a
    # Y or N attribute of each listed contact, never a second file), and standard 3.1's reproduction number counts the
    # people one case infects; physical contacts alone keep the call. Asserted through the verifier's csv and PDF reads.
    v_parts = V.rows(target, PK.FILES["participants"])
    v_cont = V.rows(target, PK.FILES["contacts"])
    v_pids = {r["part_id"] for r in v_parts}
    v_phys = {}
    for r in v_cont:
        v_phys[r["physical"]] = v_phys.get(r["physical"], 0) + 1
    ok(len(v_cont) == counts["contacts"] and len(v_parts) == 7560 and all(r["part_id"] in v_pids for r in v_cont),
       "SF26 control (verifier's csv read): %d contact rows, each listed by one of the %d diaries" % (len(v_cont),
                                                                                                    len(v_parts)))
    ok(set(v_phys) == {"Y", "N"} and v_phys["N"] > 0.2 * len(v_cont) and v_phys["Y"] > 0.2 * len(v_cont),
       "SF26 closure in the data: physical is Y on %d and N on %d of the listed contacts, an attribute of a contact "
       "and not its definition" % (v_phys["Y"], v_phys["N"]))
    std_v = V.pdf_text(target, PK.FILES["standard"])
    ok("the reproduction number, the average number of people one case infects, stays below one throughout" in std_v,
       "SF26 closure (verifier's PDF read): standard 3.1 defines the reproduction number by the people one case infects")
    rph = CM.scenarios(inp, P=CM.survey_matrix(parts, phys, CM.term_diary).T)
    ok(call_of(rph) == "B" and rph["none"] > R["none"] and not same_bins(rph, R),
       "SF26: physical contacts alone on the term diaries keep the call with other figures (%s), refused by the "
       "literal reading (every contact a diary lists) and standard 3.1" % fmt(rph))
    # closure axis 8 (window length): the survey's two periods are its diaries' own dates, nothing between them
    v_dates = sorted({r["diary_date"] for r in v_parts})
    v_may = [d for d in v_dates if "2023-05-02" <= d <= "2023-05-26"]
    v_sum = [d for d in v_dates if "2023-07-03" <= d <= "2023-08-18"]
    ok(len(v_may) + len(v_sum) == len(v_dates) and v_may[0] == "2023-05-02" and v_may[-1] == "2023-05-26"
       and v_sum[0] == "2023-07-03" and v_sum[-1] == "2023-08-18"
       and sum(1 for r in v_parts if r["diary_date"] <= "2023-05-26") == 2520,
       "closure 8 in the data (verifier's csv read): every diary is dated 2 to 26 May or 3 July to 18 August 2023, "
       "nothing between, 2,520 in May")
    # SF6: the survey's population table reads back (fifteen bands, the all-ages row their sum) for the reciprocity
    # treatment, the same call under every basis
    import openpyxl
    pop_rows = list(openpyxl.load_workbook(os.path.join(target, PK.FILES["population"]), read_only=True)["Population"]
                    .iter_rows(values_only=True))
    ok([r[0] for r in pop_rows[1:-1]] == W.GROUP_LABELS and pop_rows[-1][0] == "All ages"
       and pop_rows[-1][1] == sum(r[1] for r in pop_rows[1:-1]) and np.allclose(inp.natpop, [r[1] for r in pop_rows[1:-1]]),
       "SF6: the survey's population table reads back, %d bands summing to its all-ages row %d" % (len(pop_rows) - 2,
                                                                                                pop_rows[-1][1]))
    ok(abs(c["immune_pct"] - 95.17) < 0.02, "the region is %.2f per cent immune" % c["immune_pct"])
    # ---------------------------------------------------------------- the ask
    f = B.ask_frames(target)
    a1 = c["ask1"]
    a2 = c["ask2"]
    ppl = f["people"]
    people_w = {p_.pid: p_ for p_ in w["people"]}
    v_ppl = V.rows(target, PK.FILES["people"])
    v_ev = V.merged_events(target)
    v_dob = V.born(target, v_ev)
    # The ask's first device (D-alpha): dates of birth the register holds ten years early. Its two signatures, each on
    # the child's own records, read through the verifier's csv path; the generator's keyed-early records the control.
    keyed = {p_.pid for p_ in w["people"] if p_.dob_rec is not None}
    by_both = A.decade_early(f)
    by_reg = A.decade_early(f, rule="registration")
    by_dose = A.decade_early(f, rule="first_dose")
    v_moved = {r_["person_number"] for r_ in v_ppl if v_dob[r_["person_number"]].isoformat() != r_["date_of_birth"]}
    ok(len(keyed) > 60 and by_both == by_reg == by_dose == keyed == v_moved,
       "D-alpha control: the %d dates of birth held ten years early are exactly the registrations made 6 to 45 days "
       "after the date ten years on (%d), exactly those whose first GP dose came 12 to 17 months after it (%d), and the "
       "verifier's own reading (%d)" % (len(keyed), len(by_reg), len(by_dose), len(v_moved)))
    ok(all(V.born(target, v_ev, rule) == v_dob for rule in ("registration", "first_dose")),
       "SF31 C1 (verifier's csv read): either signature alone reads the same dates of birth as both together")
    tenth = pd.to_datetime(A._plus_years(ppl["date_of_birth"], 10))
    lag = (pd.to_datetime(ppl["registered_on"]) - tenth).dt.days
    near = set(ppl.loc[lag.between(0, 60), "person_id"])
    ok(near == keyed, "SF31 C1: no other registration falls within 60 days after the tenth anniversary of the date of "
       "birth it holds (%d registrations there, all the keyed-early ones)" % len(near))
    first_gp = {}
    for p_, d_, ref_ in v_ev:
        if ref_.startswith("GPR-") and (p_ not in first_gp or d_ < first_gp[p_]):
            first_gp[p_] = d_
    late = {r_["person_number"] for r_ in v_ppl if r_["person_number"] in first_gp
            and 3650 <= (first_gp[r_["person_number"]] - dt.date.fromisoformat(r_["date_of_birth"])).days <= 4400}
    ok(late == keyed, "SF31 C1: no other registration had its first GP dose ten years and 12 to 17 months after the date "
       "of birth it holds (%d such registrations, all the keyed-early ones)" % len(late))
    born_rec = {p_.pid: (p_.dob, p_.registered) for p_ in w["people"] if p_.pid in keyed}
    ok(all(6 <= (reg - dob).days <= 45 for dob, reg in born_rec.values()),
       "D-alpha realism: every keyed-early child was registered from its birth notification")
    sit = [(p_, d_, ref_) for p_, d_, ref_ in v_ev if ref_.startswith("SIT-") and p_ in v_dob]
    held = {r_["person_number"]: r_ for r_ in v_ppl}
    sess_years = {}
    for p_, d_, ref_ in sit:
        sess_years.setdefault(ref_, []).append((p_, int(held[p_]["date_of_birth"][:4])))
    older, seen = set(), set()
    for p_, d_, ref_ in sit:
        mates = [y_ for q_, y_ in sess_years[ref_] if q_ != p_]
        if mates:
            seen.add(p_)
            if float(np.median(mates)) - int(held[p_]["date_of_birth"][:4]) >= 8:
                older.add(p_)
    ok(older <= keyed and older == seen & keyed and len(older) > 50,
       "SF31 C1: dating a child by its school session's other pupils (a session one programme's, on one day in one "
       "area) moves no registration the golden leaves, and moves every keyed-early child that has classmates at a "
       "session (%d of %d; the rest hold no school dose with classmates)" % (len(older), len(keyed)))
    p_any = A.people_as_born(f, "any_birthday")
    any_dob = dict(zip(p_any["person_id"], p_any["date_of_birth"]))
    moved_any = {p_ for p_, d_ in any_dob.items() if d_ != held[p_]["date_of_birth"]} - keyed
    ev_all = {}
    for p_, d_, ref_ in v_ev:
        ev_all.setdefault(p_, []).append((d_, ref_))

    def refuted_any(p_):
        b_ = dt.date.fromisoformat(any_dob[p_])
        evs = ev_all.get(p_, [])
        early = any(d_ < b_ for d_, _ in evs)
        sched = any(ref_.startswith("GPR-") and 365 <= (d_ - b_).days <= 525 for d_, ref_ in evs)
        return early or not sched
    ok(len(moved_any) > 1000 and all(refuted_any(p_) for p_ in moved_any),
       "SF31 rival ruled out: reading every registration made 6 to 45 days after any birthday as a birth registration "
       "would move %d more registrations, and each of them holds a dose dated before such a birth or no GP first dose "
       "at the schedule's age after it" % len(moved_any))
    # The ask's second device (D-beta): same-sex twins at a practice whose returns carry no register number, both
    # twins' GP lines loaded to the first registration of the pair. Read through the verifier's csv path.
    loaders = {p_.pid for p_ in w["people"] if p_.loader_twin}
    lower = {p_ for p_ in loaders if people_w[p_].twin.pid > p_}
    days = {}
    for p_, d_, ref_ in v_ev:
        if ref_.startswith("GPR-"):
            days.setdefault((p_, d_), set()).add(ref_)
    dbl = {k_: v_ for k_, v_ in days.items() if len(v_) > 1}
    days_of = {}
    for (p_, d_) in days:
        days_of.setdefault(p_, set()).add(d_)
    holders = {p_ for p_, _ in dbl}
    gp_owners = {e_.owner for e_ in w["events"] if e_.given_by == "GP" and e_.kind == "dose"}
    with_gp = {p_ for p_ in lower if p_ in gp_owners or people_w[p_].twin.pid in gp_owners}
    ok(len(holders) > 150 and holders == with_gp and all(len(v_) == 2 for v_ in dbl.values()),
       "D-beta control (verifier's csv read): the %d registrations holding two GP lines on one day are exactly the first "
       "registrations of the same-sex twin pairs at the practices whose returns carry no register number that had a GP "
       "dose (%d day pairs, two lines each)" % (len(holders), len(dbl)))
    given, n_moved = V.twins_given_back(target, v_ev)
    co = {}
    for (p_, d_), refs in dbl.items():
        moved_to = {q_ for q_, dd_, rr_ in given if dd_ == d_ and rr_ in refs and q_ != p_}
        co.setdefault(p_, set()).update(moved_to)
    ok(n_moved == len(dbl) and all(len(v_) == 1 and next(iter(v_)) == people_w[p_].twin.pid for p_, v_ in co.items()),
       "SF30 C1: every doubled day's second line goes to the holder's twin, the one other registration of its household "
       "with no GP line that day (%d lines given back)" % n_moved)
    for key in (("date_of_birth", "sex", "gp_practice"), ("date_of_birth", "sex", "registered_on"),
                ("date_of_birth", "sex", "gp_practice", "registered_on")):
        alt, n_alt = V.twins_given_back(target, v_ev, key)
        ok(n_alt == n_moved and sorted(alt) == sorted(given),
           "SF30 C1: the co-twin read by %s finds the same child on every doubled day" % ", ".join(key))
    co_gp = {q_ for q_ in (people_w[p_].twin.pid for p_ in holders) if q_ in days_of}
    ok(not co_gp, "SF30: no co-twin of a doubled registration holds a GP line of its own")
    pairs = [(p_.pid, p_.twin.pid) for p_ in w["people"] if p_.twin is not None and p_.pid < p_.twin.pid]
    refs_ok = 0
    split_ok = True
    for x_, y_ in pairs:
        if x_ in loaders:
            continue
        dx, dy = days_of.get(x_, set()), days_of.get(y_, set())
        if dx or dy:
            refs_ok += 1
            split_ok &= dx == dy and all(len(days[(x_, d_)]) == 1 and len(days[(y_, d_)]) == 1 for d_ in dx)
    ok(refs_ok > 500 and split_ok,
       "SF30 referee: the other %d twin pairs with a GP dose (boy and girl at any practice, same-sex at the practices "
       "whose returns carry the register number) hold one line each on every day the GP vaccinated them" % refs_ok)
    sess_of = {}
    for p_, d_, ref_ in v_ev:
        if ref_.startswith("SIT-"):
            sess_of.setdefault(p_, set()).add((d_, ref_))
    both_sess = sum(1 for p_ in holders if sess_of.get(p_) and sess_of.get(p_) == sess_of.get(people_w[p_].twin.pid))
    ok(both_sess > 100, "SF30: %d doubled registrations and their twins each hold their own dose at the same school "
       "sessions (two pupils' doses at one session)" % both_sess)
    held_gp = {}
    for p_, d_, ref_ in v_ev:
        if ref_.startswith("GPR-"):
            held_gp.setdefault(ref_, set()).add(p_)
    ok(all(len(h_) == 1 for h_ in held_gp.values()),
       "SF29 retired: no GP return line sits on two registrations once the merges are followed (%d lines)" % len(held_gp))
    # the ask's stops (each a complete pipeline), every figure against the golden
    stops = {
        "the current code list, dates as held, lines as loaded (the natural path)":
            dict(how="current", dob_how="held", twins="loaded"),
        "the circular read, dates as held, lines as loaded, merges and queries handled (the cracker)":
            dict(dob_how="held", twins="loaded"),
        "the cracker with twins merged as one child (household key)": dict(dob_how="held", twins="loaded",
                                                                          link="household"),
        "every device handled but the dates of birth (D-beta cracked alone)": dict(dob_how="held"),
        "every device handled but the twins' lines (D-alpha cracked alone)": dict(twins="loaded"),
        "a registration 6 to 45 days after any birthday read as a birth registration (over-cleaning)":
            dict(dob_how="any_birthday"),
        "every LH27 read as Monaghan West": dict(how="old"),
        "every active registration": dict(how="all"),
        "a person key on date of birth, sex and area code": dict(link="dob_sex_area"),
        "a person key on date of birth, sex and postcode": dict(link="dob_sex_postcode"),
        "records joined by any shared source reference": dict(link="any_ref"),
        "registrations no practice lists left out": dict(unlisted="drop"),
    }
    moved_by = {}
    for name, kw in stops.items():
        k1 = {x: kw[x] for x in ("how", "link", "unlisted", "dob_how") if x in kw}
        k2 = {("pop" if x == "how" else x): v for x, v in kw.items()}
        s1, s2 = A.ask1(f, **k1), A.ask2(f, **k2)
        hit = sum(s1[k] == a1[k] for k in a1) + sum(s2[k][x] == a2[k][x] for k in a2 for x in ("none", "one"))
        moved_by[name] = 15 - hit
        print("      %-100s %2d of 15 figures off" % (name, 15 - hit))
    ok(moved_by["the circular read, dates as held, lines as loaded, merges and queries handled (the cracker)"] == 15,
       "ask: the cracker (circular, merges, queries, interval rule, dates of birth as held, lines as loaded) files all 15 "
       "figures wrong")
    ok(moved_by["the current code list, dates as held, lines as loaded (the natural path)"] == 15
       and moved_by["the cracker with twins merged as one child (household key)"] == 15,
       "ask: the natural path and the twin-merging over-clean each file all 15 figures wrong")
    ok(moved_by["every device handled but the dates of birth (D-beta cracked alone)"] >= 9
       and moved_by["every device handled but the twins' lines (D-alpha cracked alone)"] >= 10,
       "ask: each device alone leaves at least nine figures wrong (dates as held %d, lines as loaded %d)" % (
           moved_by["every device handled but the dates of birth (D-beta cracked alone)"],
           moved_by["every device handled but the twins' lines (D-alpha cracked alone)"]))
    held_r = A.ask1(f, dob_how="held")
    ok(all(held_r[k] != a1[k] for k in a1), "D-alpha moves every option's people (%s)" % ", ".join(
        "%s %+d" % (k, held_r[k] - a1[k]) for k in a1))
    loaded = A.ask2(f, twins="loaded")
    ok(all(loaded[k]["none"] != a2[k]["none"] and loaded[k]["one"] != a2[k]["one"] for k in a2),
       "D-beta moves every option's no-dose and one-dose figures (%s)" % ", ".join(
           "%s %+d/%+d" % (k, loaded[k]["none"] - a2[k]["none"], loaded[k]["one"] - a2[k]["one"]) for k in a2))
    # SF23 retired: the register gives a record at an address outside the State no area code, so the code and the
    # address agree such a record is not in the region (C1); nothing about it is filed
    bt = ppl["postcode"].fillna("").str.startswith("BT")
    ni_pids = {p_.pid for p_ in w["people"] if p_.status == "ni"}
    ok(set(ppl.loc[bt, "person_id"]) == ni_pids, "SF23 retired: the UK postcodes are exactly the pupils living in "
       "Northern Ireland")
    v_bt = {r_["person_number"] for r_ in v_ppl if r_["postcode"].strip().upper().startswith("BT")}
    v_blank = {r_["person_number"] for r_ in v_ppl if not r_["lho_code"].strip()}
    ok(len(v_bt) == int(bt.sum()) > 900 and v_bt == v_blank,
       "SF23 retired (verifier's csv read): the %d registrations with a UK postcode are the %d with no area code"
       % (len(v_bt), len(v_blank)))
    ok(bool((A.in_region(ppl, "lh27") == A.in_region(ppl, "golden")).all()),
       "SF23 retired, C1: read by its area code alone or by its address as well, the region holds the same registrations")
    with open(os.path.join(target, PK.FILES["lho"]), encoding="utf-8") as fh:
        lho_rows = list(csv.DictReader(fh))
    ok(all(r["county"] in set(W.COUNTIES) | {v[1] for v in W.OTHER_LHO.values()} for r in lho_rows)
       and not any(r["county"] in ("Armagh", "Down", "Fermanagh", "Tyrone", "Antrim", "Londonderry") for r in lho_rows),
       "SF23 retired: the national code list holds no office outside the State")
    pcs = ppl["postcode"].fillna("")
    eircode = pcs.str.fullmatch(r"(?:[AC-FHKNPRTV-Y][0-9]{2}|D6W) [0-9AC-FHKNPRTV-Y]{4}")
    ukpc = pcs.str.fullmatch(r"BT[0-9]{1,2} [0-9][A-Z]{2}")
    ok(bool((eircode | ukpc | (pcs == "")).all()) and int(ukpc.sum()) == int(bt.sum()),
       "SF23 retired: every recorded postcode is an Eircode or a BT postcode (%d)" % int(ukpc.sum()))
    rec = ppl.loc[ppl["lho_code"] == "LH27", "lho_recorded"]
    ok(not rec.between("2024-06-24", "2024-07-08").any(), "ask C1: no LH27 recorded within a week of 1 July 2024")
    lh27 = ppl[(ppl["lho_code"] == "LH27") & (ppl["postcode"].fillna("") != "")]
    rk = lh27["postcode"].str[:3]
    old_rk, new_rk = set(W.ROUTING_KEYS["LH27_old"]), set(W.ROUTING_KEYS["LH27"])
    ok(bool((rk[lh27["lho_recorded"] < W.CUTOVER.isoformat()].isin(old_rk)).all())
       and bool((rk[lh27["lho_recorded"] >= W.CUTOVER.isoformat()].isin(new_rk)).all()),
       "ask C1: every LH27 Eircode agrees with the code's date (Monaghan West routing keys before 1 July 2024, "
       "Portlaoise's after; %d LH27 records with a postcode)" % len(lh27))
    nat = A.ask1(f, how="current")
    ok(all(nat[k] != a1[k] for k in a1), "ask hazard: the current code list moves every option's people (%s)" % ", ".join(
        "%s %+d" % (k, nat[k] - a1[k]) for k in a1))
    log = f["log"]
    ext = set(f["events"]["source_ref"])
    lines_in = set(log["line_ref"]) & ext
    reps_needed = set(log.loc[log["line_ref"].isin(lines_in) & (log["outcome"] == "Replaced by corrected line"), "replaced_by"])
    ok(reps_needed <= ext, "ask fairness: every replaced line in the extract has its corrected line loaded")
    # SF17: a GP return line under a query the office had not closed
    ok(set(log["outcome"]) == {"Confirmed as sent", "Replaced by corrected line", "Withdrawn by practice"},
       "SF17: every query in the log has an outcome, none open")
    ok(bool((log["closed_on"] != "").all()) and bool((log["raised_on"] < log["closed_on"]).all())
       and log["closed_on"].max() <= W.AS_AT.isoformat(),
       "SF17: every query closed after it was raised and by 30 June 2027 (latest %s)" % log["closed_on"].max())
    st = A.ask2(f, ev_how="drop_unresolved")
    ok(st == a2, "SF17: lines under a query not closed as confirmed by 30 June 2027 dropped, every dose figure unchanged")
    for name, kw in {"no merges": dict(merge_how="none"), "one hop": dict(merge_how="one_hop"),
                     "every loaded event": dict(ev_how="all"), "every queried line dropped": dict(ev_how="drop_queried")
                     }.items():
        st = A.ask2(f, **kw)
        moved = sum(st[k][x] != a2[k][x] for k in a2 for x in ("none", "one"))
        ok(moved >= (3 if name == "one hop" else 8), "ask hazard %s moves %d of 10 dose figures" % (name, moved))
    # SF28 closed by the prompt as filed: the doses are those had by 30 June 2027 ("by that date"), a dose had on the
    # day it was given (date_given); counting every row the extract holds, or the rows loaded by 30 June, moves figures
    prompt_txt = open(os.path.join(os.path.dirname(target), "prompt.txt"), encoding="utf-8").read()
    ok(prompt_txt.count("the register holds as living in the region at 30 June 2027, how many of those have had no "
                        "valid MMR dose by that date and how many exactly one") == 1,
       "SF28 closed by the prompt as filed: \"how many of those have had no valid MMR dose by that date\", the date the "
       "residents are counted at")
    ev_all = f["events"]
    late_ld = ev_all[(ev_all["date_given"] <= W.AS_AT.isoformat()) & (ev_all["loaded_on"] > W.AS_AT.isoformat())]
    after = ev_all[ev_all["date_given"] > W.AS_AT.isoformat()]
    by_load = A.ask2(f, events=ev_all[ev_all["loaded_on"] <= W.AS_AT.isoformat()])
    moved_load = sum(by_load[k][x] != a2[k][x] for k in a2 for x in ("none", "one"))
    keep_asat, A.AS_AT = A.AS_AT, pd.Timestamp("2099-12-31")
    try:
        every_row = A.ask2(f)
    finally:
        A.AS_AT = keep_asat
    moved_rows = sum(every_row[k][x] != a2[k][x] for k in a2 for x in ("none", "one"))
    ok(len(late_ld) > 0 and len(after) > 0 and moved_load > 0 and moved_rows > 0,
       "SF28: %d doses given by 30 June 2027 were loaded after it and %d were given after it; counted by load date %d of "
       "10 figures move, counting every row %d" % (len(late_ld), len(after), moved_load, moved_rows))
    chased = [r for r in w["log"] if r.get("chased")]
    on_ext = sorted(r["line_ref"] for r in chased if r["line_ref"] in ext)
    ok(len(chased) >= 3, "SF17: %d confirmed queries still open at the extract were chased and closed, %d on extract "
       "lines" % (len(chased), len(on_ext)))
    m = dict(zip(f["merges"]["retired_number"], f["merges"]["surviving_number"]))
    ok(not (set(m) & set(f["people"]["person_id"])), "ask: no retired registration is active")
    born_ = A.people_as_born(f)
    ev = A.resolve_merges(f["events"], f["merges"]).copy()
    ev = A.clean_events(ev, log)
    ev = A.reattribute(f["people"], ev)
    ev = ev[ev["person_id"].isin(set(f["people"]["person_id"]))]
    dob = dict(zip(born_["person_id"], born_["date_of_birth"]))
    d = np.array([dt.date.fromisoformat(x).toordinal() for x in ev["date_given"]])
    fb = np.array([dt.date(int(dob[p][:4]) + 1, int(dob[p][5:7]), int(dob[p][8:10])).toordinal() for p in ev["person_id"]])
    ok(int(np.sum(np.abs(d - fb) <= 3)) == 0, "ask C1: no dose within three days of a first birthday")
    ev = ev.assign(o=d).sort_values(["person_id", "o"])
    gaps = ev.groupby("person_id")["o"].diff().dropna()
    ok(int(((gaps >= 24) & (gaps <= 32)).sum()) == 0, "ask C1: no two of a person's doses 24 to 32 days apart")
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
    ok(differ == 0, "ask C1: the interval counted from the previous valid dose or from any previous dose gives the "
       "same count for every person")
    ok(f["people"]["person_id"].is_unique and f["events"]["event_number"].is_unique, "keys: person and event numbers unique")
    # the golden against the simulation's own truth: each child's own doses (owner), as born
    truth = {}
    live = {p_.pid: p_ for p_ in w["people"] if p_.status in S.ACTIVE}
    reg_here = dict(zip(ppl["person_id"], A.in_region(ppl, "golden")))
    own = {}
    for e_ in w["events"]:
        if e_.kind == "dose":
            own.setdefault(e_.owner, []).append(e_.date)
    for k, (lo_, hi_) in A.OPTION_YEARS.items():
        ids = [p_ for p_, q_ in live.items() if reg_here[p_] and lo_ <= q_.dob.year <= hi_]
        cnt = {}
        for p_ in ids:
            q_ = live[p_]
            fb_ = dt.date(q_.dob.year + 1, q_.dob.month, q_.dob.day)
            n_, pv_ = 0, None
            for d_ in sorted(own.get(p_, [])):
                if d_ > W.AS_AT or d_ < fb_ or (pv_ is not None and (d_ - pv_).days < 28):
                    continue
                n_, pv_ = n_ + 1, d_
            cnt[p_] = n_
        truth[k] = (len(ids), sum(1 for p_ in ids if cnt[p_] == 0), sum(1 for p_ in ids if cnt[p_] == 1))
    ok(not any(fn.startswith(("nds_", "nmrl_")) for fn in files),
       "SF24 and SF27 retired: the case ask is cut, and no case export or laboratory file ships")
    ok(all(truth[k] == (a1[k], a2[k]["none"], a2[k]["one"]) for k in a1),
       "ask fairness: the golden equals the simulation's truth (each child's own doses, from the date it was born) for "
       "all 15 figures")
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
        ok(c2["r1"] == c["r1"] and c2["ask1"] == c["ask1"] and c2["ask2"] == c["ask2"],
           "distractors: the golden and every ask figure unchanged with both deleted")
    finally:
        shutil.rmtree(tmp)
    ok(not (set(PK.CALL_FILES) & set(PK.ASK_FILES)), "separation: no file is read by both the call and an ask")
    # ---------------------------------------------------------------- realism and leaks
    ok(len({a1[k] for k in a1}) == 5 and len({a2[k]["none"] for k in a2}) == 5, "realism: no identical counts across options")
    ok(all(a1[k] % 100 and a2[k]["none"] % 100 and a2[k]["one"] % 100 for k in a1), "realism: no round ask counts")
    banned = ["eigen", "next-generation", "next generation", "herd immunity", "mixing matrix", "assortativ", "well-mixed",
              "random mixing", "contact-adjusted", "term time", "term-time", "school term", "school holiday",
              "summer holiday", "northern ireland", "twin", "loader", "date of birth", "birth notification", "decade"]
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
    for fn in files:
        if not fn.endswith((".docx", ".xlsx")):
            continue
        with zipfile.ZipFile(os.path.join(target, fn)) as z:
            names = z.namelist()
            ct = z.read("[Content_Types].xml").decode()
            targets = []
            for rel in (n for n in names if n.endswith(".rels")):
                base = rel.replace("_rels/", "").rsplit(".rels", 1)[0]
                folder = base.rsplit("/", 1)[0] + "/" if "/" in base else ""
                for t in re.findall(r'Target="([^"]+)"', z.read(rel).decode()):
                    p_ = t[1:] if t.startswith("/") else folder + t
                    targets.append(os.path.normpath(p_).replace("\\", "/"))
            app = z.read("docProps/app.xml").decode()
        ok(not any(n.startswith("customXml/") or "thumbnail" in n for n in names) and "customXml" not in ct
           and "savePreviewPicture" not in texts.get(fn, ""),
           "scrub: %s carries no template thumbnail, bibliography store or preview setting" % fn)
        ok(all(t in names for t in targets) and app.count("<Company") == 1,
           "scrub: every relationship in %s points at a part it holds, and one Company" % fn)
    allnames = " ".join(texts.values())
    import json as _json
    card = os.path.join(os.path.dirname(os.path.dirname(target)), ".claude", "skills", "fingerprint", "cards", "task501.json")
    people = _json.load(open(card, encoding="utf-8"))["world"]["people"]
    ok(sorted(people) == sorted(W.PEOPLE.values()), "personas are the card's people (guard.py names, seed 501)")
    ok(W.PEOPLE["manager"] in allnames and W.PEOPLE["director"] in allnames,
       "personas appear in their documents (the options paper's author, the standard's owner)")
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
