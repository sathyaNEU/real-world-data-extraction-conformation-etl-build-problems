"""The generator's assertions on the built pack (architecture 5): the input gates; the pack read back against the
simulation; the call, its rungs, the golden's readings and the slipped paths; the three-rules block (R1 the field's raw
material, R2 each mess item neutral, R3a the analyst test on the clean truth, R3b the decisive step alone, R3c no plant);
every row of the semantic fork table; the asks against the generator's truth with their stops and the separation line;
the distractors; the documents' dates; figures.json against the golden files."""
import collections
import copy
import csv
import datetime as dt
import itertools
import json
import os
import shutil
import subprocess
import tempfile

import docx
import openpyxl

import bundle as B
import calibrate as C
import methods as M
import pack as P
import world as W

NAMES = [W.NAME[c] for c in W.CODES]
GOLD = dict(zip(NAMES, [27, 20, 25, 26, 29, 5, 11, 12, 7, 5, 4, 8, 6, 3, 8, 4]))
DEFAULT = dict(zip(NAMES, [26, 20, 26, 28, 31, 4, 11, 12, 6, 4, 4, 8, 6, 3, 8, 3]))
R0 = dict(zip(NAMES, [17, 17, 26, 31, 38, 5, 12, 19, 2, 3, 7, 7, 5, 3, 5, 3]))
R1 = dict(zip(NAMES, [22, 19, 24, 26, 30, 7, 11, 16, 5, 5, 7, 8, 6, 4, 6, 4]))
CHANGED = ["Ardenmere", "Westerby", "Larchfield", "Glenwhite", "Hawksridge", "Corran Valley", "Drumlea", "Nethermoor"]
FACTORS = (1.036, 1.040, 1.048)


class Checker:
    def __init__(self):
        self.ok = True
        self.n = 0
        self.failed = 0

    def __call__(self, cond, msg):
        self.n += 1
        if not cond:
            self.ok = False
            self.failed += 1
            print("FAIL:", msg)


def named(alloc):
    return {W.NAME[c]: alloc[c] for c in W.CODES}


def off(a, b):
    return sum(1 for k in a if a[k] != b[k])


def alloc_of(d, adults):
    return named(C.allocation(d, adults)[0])


def hits(a, b):
    return sum(1 for c in W.CODES if a[c] == b[c])


# ------------------------------------------------------------------ the documents, read the way the verifier reads them
def pdf_text(path):
    return " ".join(subprocess.run(["pdftotext", "-raw", path, "-"], capture_output=True, text=True,
                                   check=True).stdout.split())


def docx_text(path):
    return " ".join(" ".join(p.text for p in docx.Document(path).paragraphs).split())


def xlsx_text(path):
    wb = openpyxl.load_workbook(path, read_only=True)
    out = []
    for ws in wb.worksheets:
        for r in ws.iter_rows(values_only=True):
            out.extend(str(v) for v in r if v is not None)
    return " ".join(" ".join(out).split())


def truth_asks(x):
    """the generator's truth for the two asks, from the simulated transactions by what the simulation made them, at
    their simulated local times and in the region of their electorate as simulated: a new elector is an accepted
    residential enrolment of a person the simulation created in the window (not a move, a re-enrolment or an enrolment
    that put right a removal made in error); a death is a removal the death loop wrote, less those put right"""
    rows = x["log"]
    back = {r[12] for r in rows if r[15] == "death_rev" and r[5] == "A"}
    first = W.CENSUS_DAY + dt.timedelta(days=1)
    new, died = collections.Counter(), collections.Counter()
    for r in rows:
        if not first <= r[13].date() <= W.LOG_END or r[5] != "A":
            continue
        reg = W.ELECTORATE_REGION[r[16]]
        if r[15] == "new" and r[9] == "R":
            new[reg] += 1
        elif r[15] == "death" and r[0] not in back:
            died[reg] += 1
    return new, died


def raked(d, est, groups):
    """men and women of each group raked to demographic analysis's totals"""
    da = M.demographic(d)
    ad = M.adults(est)
    for g in groups:
        for s in ("M", "F"):
            e = sum(v for (c, ss, gg), v in est.items() if ss == s and gg == g)
            t = sum(da.get((s, a), 0) for a in range(g[0], min(g[1], 100) + 1))
            for c in W.CODES:
                ad[c] += est[(c, s, g)] * (t / e - 1)
    return ad


def estimate_alloc(target, pk):
    """the 2018-base estimates at 30 June 2024 (the wrong-basis distractor) read as the adults: 25 and over, plus seven
    tenths of 15 to 24"""
    adults = {c: 0.0 for c in W.CODES}
    for r in B.rows(os.path.join(target, P.FILES["estimates_2024"])):
        n = int(r["ESTIMATED_RESIDENT_POPULATION"])
        if r["AGE_GROUP"] == "15-24":
            adults[r["REGION"]] += 0.7 * n
        elif r["AGE_GROUP"] not in ("0-14",):
            adults[r["REGION"]] += n
    return named(M.allocate(pk.gap(adults))[0])


def run(target, gdir, x=None, meta_path=None, fig_path=None):
    ck = Checker()
    x = x or P.everything()
    pk = B.Pack(target)
    d = pk.d
    f = lambda k: os.path.join(target, P.FILES[k])
    # ------------------------------------------------------------------------------------------- input gates
    files = sorted(os.listdir(target))
    ck(len(files) >= 10, "ten or more files (%d)" % len(files))
    ck(len({fn.rsplit(".", 1)[1] for fn in files}) >= 3, "three or more formats")
    ck(len(pk.log) >= 25000 and len(B.rows(f("pes_people"))) >= 25000, "a file of 25,000 or more rows (the log %d)" % len(
        pk.log))
    ck(set(files) == set(P.FILES.values()), "the pack is exactly the files the generator names")
    if meta_path:
        meta = json.load(open(meta_path, encoding="utf-8"))
        ck(len(meta["distractor_files"]) >= 2 and all(fn in files for fn in meta["distractor_files"]),
           "two or more distractors named in metadata.json")
        ck(all("distractor" not in fn.lower() for fn in files), "no file name says distractor")
    # ------------------------------------------------------------------------------- the documents and controls
    plan = docx_text(f("plan"))
    report = pdf_text(f("pes_report"))
    notes = pdf_text(f("series_notes"))
    migration = pdf_text(f("migration"))
    spec = xlsx_text(f("spec"))
    dictionary = xlsx_text(f("dictionary"))
    workbook = xlsx_text(f("census"))
    for name, text, control in (
            ("the plan", plan, "2027 Enrolment Campaign: field plan"),
            ("the methods report", report, "2025 Post-Enumeration Survey"),
            ("the series notes", notes, "Vital and border series"),
            ("the migration notes", migration, "Roll platform migration"),
            ("the specification", spec, "Enrolment-gap file for the Electoral Commission"),
            ("the dictionary", dictionary, "Roll transactions extract: data dictionary"),
            ("the census workbook", workbook, "2025 Census of Population and Dwellings")):
        ck(len(text) > 200 and control in text, "positive control: %s reads back (%d characters)" % (name, len(text)))
    # --------------------------------------------------------------- the pack read back against the simulation
    d0 = C.data_from(x["nat"], x["cnt"], x["roll_counts"])
    ck(d["census"] == d0["census"], "the census workbook reads back to the simulated counts and imputed records")
    ck({k: list(v) for k, v in d["e"].items()} == {k: list(v) for k, v in d0["e"].items()},
       "the survey's census records read back to the simulated sample by cell")
    ck({k: list(v) for k, v in d["p"].items()} == {k: list(v) for k, v in d0["p"].items()},
       "the survey's people read back to the simulated sample by cell")
    ck(d["roll"] == d0["roll"], "the roll at the close of census day reads back by region")
    ck(d["births"] == {k: int(v) for k, v in d0["births"].items()}, "the births read back")
    ck(d["deaths"] == {k: int(v) for k, v in d0["deaths"].items() if v}, "the deaths read back from both layouts")
    for key in ("departures", "arrivals"):
        want = {k: int(v) for k, v in d0[key].items() if v}
        ck(d[key] == want, "the %s read back from 1925" % key)
    people = B.rows(f("pes_people"))
    records = B.rows(f("pes_records"))
    rec_status = {r["CENSUS_RECORD"]: r["STATUS"] for r in records}
    ck(len(rec_status) == len(records) and len({p["PES_PERSON"] for p in people}) == len(people),
       "no survey key twice")
    ck(all(p["CENSUS_RECORD"] in rec_status and rec_status[p["CENSUS_RECORD"]] == "C" for p in people if p["MATCH"] == "M")
       and all(p["CENSUS_RECORD"] == "" for p in people if p["MATCH"] == "N"),
       "SF9 every matched person's census record is in the records file, counted correctly; no unmatched one has one")
    ck({p["MATCH"] for p in people} == {"M", "N"} and {r["STATUS"] for r in records} == set("CDVOW"),
       "SF8 SF9 the match and enumeration codes are those the methods report files")
    # -------------------------------------------------------------------------------------- the call and rungs
    rg = C.rungs(d)
    est = M.dse_cells(d)
    fac = M.factors(d, est)
    gold_alloc, quota = M.allocate(pk.gap(rg["R3 golden"]))
    gold = named(gold_alloc)
    ck(gold == GOLD, "the call: %s" % gold)
    ck(sum(gold.values()) == 200 and min(quota.values()) > W.FLOOR,
       "200 organisers; no region's share under two, so the floor never binds (smallest %.2f)" % min(quota.values()))
    mg = M.margin(quota, gold_alloc)
    ck(mg > 0.2, "the largest-remainder cut clears its neighbours by %.3f of an organiser" % mg)
    for nm, want, n in (("R0 census counts", R0, 14), ("R1 one national ratio", R1, 10), ("R2 dual-system cells", DEFAULT, 8)):
        got = alloc_of(d, rg[nm])
        ck(got == want and off(got, GOLD) == n, "rung %s files %s, %d regions off" % (nm, got, off(got, GOLD)))
    ck(sorted(k for k in GOLD if GOLD[k] != DEFAULT[k]) == sorted(CHANGED), "the default path's eight changed regions")
    var = C.variants(d)
    for nm, a in var.items():
        ck(alloc_of(d, a) == GOLD, "the golden's reading files the golden: %s" % nm)
    for sf in ("SF11", "SF12", "SF13", "SF14", "SF15"):
        ks = [k for k in var if sf in k]
        ck(ks and all(alloc_of(d, var[k]) == GOLD for k in ks), "%s every reading files the golden: %s" % (sf, ks))
    for nm, a in C.wrong_paths(d).items():
        k = off(alloc_of(d, a), GOLD)
        ck(k >= 2, "a slipped path stays off the golden: %s (%d regions off)" % (nm, k))
    near = off(alloc_of(d, C.wrong_paths(d)["cells pooled by region and sex, corrected"]), GOLD)
    ck(near == 2 and "region by sex by age group" in report,
       "SF10 the nearest slipped path (cells pooled by region and sex, corrected) is 2 off and the methods report files "
       "the cells")
    ck(tuple(round(fac[g], 3) for g in W.YOUNG_GROUPS) == FACTORS, "the factors %s" % [fac[g] for g in W.YOUNG_GROUPS])
    for kw in ({"born_before": 0.0}, {"born_before": 0.5}, {"born_before": 1.0}, {"to_census_day": False}):
        fk = M.factors(d, est, **kw)
        ck(tuple(round(100 * (fk[g] - 1)) for g in W.YOUNG_GROUPS) == (4, 4, 5),
           "the men raised by about 4, 4 and 5 per cent under %s: %s" % (kw, [round(fk[g], 4) for g in W.YOUNG_GROUPS]))
    da = M.demographic(d)
    for g in W.ADULT_GROUPS:
        m_e = sum(v for (c, s, gg), v in est.items() if s == "M" and gg == g)
        f_e = sum(v for (c, s, gg), v in est.items() if s == "F" and gg == g)
        m_d = sum(da.get(("M", a), 0) for a in range(g[0], min(g[1], 100) + 1))
        f_d = sum(da.get(("F", a), 0) for a in range(g[0], min(g[1], 100) + 1))
        if g in W.YOUNG_GROUPS:
            ck(abs(f_e / f_d - 1) < 0.007 and m_e / m_d < 0.975,
               "%s: the women's estimates within %.2f per cent of demographic analysis, the men's %.1f per cent short" % (
                   W.group_label(g), 100 * (f_e / f_d - 1), 100 * (1 - m_e / m_d)))
        else:
            ck(abs(m_e / f_e - m_d / f_d) < 0.005, "SF14 %s: the sex ratios agree (%.3f against %.3f)" % (
                W.group_label(g), m_e / f_e, m_d / f_d))
    ratios = {}
    for nm, kw in (("golden", {}), ("born before 0", {"born_before": 0.0}), ("born before 0.5", {"born_before": 0.5}),
                   ("born before 1", {"born_before": 1.0}), ("end 2024", {"to_census_day": False})):
        pop = M.demographic(d, **kw)
        m_e = sum(v for (c, s, g), v in est.items() if s == "M" and g in W.YOUNG_GROUPS)
        m_d = sum(pop.get(("M", a), 0) for a in range(18, 50))
        r = M.da_ratio(d, **kw)
        ratios[nm] = (round(100 * (1 - m_e / m_d)), tuple(round(r[g], 2) for g in W.YOUNG_GROUPS))
    ck(len(set(ratios.values())) == 1 and ratios["golden"] == (4, (1.04, 1.03, 1.02)),
       "the men's shortfall (4 per cent) and the demographic sex ratios at two places agree under every convention: %s" % (
           ratios,))
    truth = {c: sum(int(x["reg"]["pop"][c][s][18:].sum()) for s in ("M", "F")) for c in W.CODES}
    t_alloc = alloc_of(d, truth)
    ck(off(t_alloc, GOLD) < off(t_alloc, DEFAULT),
       "the golden is nearer the simulated truth's allocation than the default path (%d against %d regions off)" % (
           off(t_alloc, GOLD), off(t_alloc, DEFAULT)))
    # --------------------------------------------------------------------- R1: the field's raw material ships
    ck(len(d["census"]) == 16 * 2 * 101 and len(d["births"]) >= 200 and len(d["deaths"]) > 5000,
       "R1 the census by single year of age and sex, births and deaths by year of birth ship")
    ck(len(people) > 100000 and len(records) > 100000, "R1 the survey's person-level files ship (%d people, %d records)" % (
        len(people), len(records)))
    banned = ("COVER", "DSE", "DUAL", "RATIO", "FACTOR", "UNDERCOUNT", "GAP", "ORGANIS", "ADULT")
    heads = {}
    for fn in files:
        if fn.endswith(".csv"):
            with open(os.path.join(target, fn), encoding="utf-8") as fh:
                heads[fn] = next(csv.reader(fh))
    bad = [(fn, h) for fn, hs in heads.items() for h in hs if any(b in h.upper() for b in banned)]
    ck(not bad, "R1 no shipped column holds a coverage figure, sex ratio, gap or allocation (%s)" % bad)
    # ------------------------------------------------------------------------- R2: each mess item neutral
    d1 = copy.deepcopy(d)
    for k in d1["census"]:
        if k[2] == 100:
            d1["census"][k] = (0, 0)
    ck(alloc_of(d1, C.rungs(d1)["R3 golden"]) == GOLD, "R2 the census row for 100 and over dropped: the call unchanged")
    d2 = copy.deepcopy(d)
    d2["deaths"] = {k: v for k, v in d["deaths"].items() if k[0] == "2025Q" or k[0] >= 1945}
    for nm, groups in (("18 to 49", W.YOUNG_GROUPS), ("18 to 64", W.ADULT_GROUPS[:-1]), ("every adult age", W.ADULT_GROUPS)):
        for mode in ("ratio", "total"):
            ck(alloc_of(d, M.adults(est, M.factors(d2, est, groups=groups, mode=mode))) == GOLD,
               "R2 the deaths read from the 1945 to 2025 file alone (the workbook missed), %s by %s: the call unchanged" % (
                   nm, mode))
        ck(alloc_of(d, raked(d2, est, groups)) == GOLD,
           "R2 the workbook missed, both sexes raked to demographic analysis at %s: the call unchanged" % nm)
    for nm, groups in (("18 to 64", W.ADULT_GROUPS[:-1]), ("every adult age", W.ADULT_GROUPS)):
        ck(alloc_of(d, raked(d, est, groups)) == GOLD, "SF13 both sexes raked to demographic analysis at %s: the golden" % nm)
    d3 = copy.deepcopy(d)
    for key in ("births", "deaths", "departures", "arrivals"):
        d3[key] = {k: v for k, v in d[key].items() if k[0] != "2025Q"}
    ck(alloc_of(d3, C.rungs(d3)["R3 golden"]) == GOLD, "R2 the 2025 provisional period ignored: the call unchanged")
    concord = {r["ELECTORATE"]: r for r in B.rows(f("electorates"))}
    ck(all(concord[r["ELECTORATE"]]["ELECTORATE_NAME"] == r["ELECTORATE_NAME"] for r in pk.snapshot),
       "R2 the renamed electorates: the roll and the concordance carry the same current names, so a join by name or "
       "code gives the same regions")
    ck(sum(1 for r in concord.values() if r["NAME_BEFORE_2024_REVIEW"]) == 8, "eight electorates renamed in 2024")
    ck(sorted(r["NUMBER_BEFORE_2024_REVIEW"] for r in concord.values()) == sorted(concord) == ["%02d" % i for i in
                                                                                              range(1, 48)],
       "both reviews number the 47 electorates 01 to 47, so every 2020 number is also a current number")
    # ------------------------------------------------------- R3: the analyst test on the clean truth, and no plant
    r0 = C.rungs(d0)
    ck(alloc_of(d0, r0["R2 dual-system cells"]) == DEFAULT,
       "R3a analyst test: on the clean truth the dual-system estimates within the survey's cells file the default path")
    ck(alloc_of(d0, r0["R3 golden"]) == GOLD,
       "R3b the decisive step alone (the men raised to demographic analysis's sex ratio) files the golden")
    wp0 = C.wrong_paths(d0)
    for nm in ("census counts, corrected", "one national ratio, corrected"):
        ck(alloc_of(d0, wp0[nm]) != GOLD, "R3b a lower rung with the correction stays wrong: %s" % nm)
    ck(alloc_of(d0, r0["R1 one national ratio"]) == R1 and alloc_of(d0, r0["R0 census counts"]) == R0,
       "R3b each lower rung's own answer on the clean truth")
    sheets = {}
    wb = openpyxl.load_workbook(f("census"), read_only=True)
    for c in W.CODES:
        sheets[c] = tuple(tuple(r) for r in wb["%s %s" % (c, W.NAME[c])].iter_rows(min_row=5, max_row=105,
                                                                                  values_only=True))
    ck(len(set(sheets.values())) == 16, "R3c no region's census sheet repeats another's")
    win = collections.Counter()
    keyf = ("PROCESSED", "TXN_TYPE", "REASON", "SOURCE", "STATUS", "ELECTORATE", "ADDRESS_TYPE", "SEX", "BIRTH_YEAR")
    for i in range(len(pk.log) - 5):
        win[hash(tuple(tuple(pk.log[i + j][k] for k in keyf) for j in range(5)))] += 1
    ck(max(win.values()) == 1, "R3c no block of five transactions repeats in the log")
    ck(len({r["TXN_ID"] for r in pk.log}) == len(pk.log), "R3c every transaction id once")
    nos = collections.Counter(r["ELECTOR_NO"] for r in pk.log if r["TXN_TYPE"] == "NEW" and r["STATUS"] == "A")
    ck(max(nos.values()) == 1, "R3c every accepted enrolment a new elector number")
    # ----------------------------------------------------------------------------- the semantic fork table
    ck("aged 18 or over usually resident in the region on census day, 4 March 2025, whether or not the census counted "
       "them" in plan, "SF1 SF2 SF3 plan 2.1 files the population, the day and the people the census missed")
    ad16 = dict(rg["R3 golden"])
    for (c, s, g), v in est.items():
        if g == (15, 17):
            ad16[c] += v * (2 / 3.0) * (fac.get(g, 1.0) if s == "M" else 1.0)
    ck(off(alloc_of(d, ad16), GOLD) >= 6, "SF1 adults at the plan's date (16 and 17 added) file another allocation")
    ck(off(alloc_of(d, rg["R0 census counts"]), GOLD) == 14, "SF2 the census counts as they stand: 14 regions off")
    ck("Census day: Tuesday 4 March 2025" in workbook, "SF3 the census workbook names census day")
    roll_o = {c: 0 for c in W.CODES}
    for r in pk.snapshot:
        roll_o[pk.region_of[r["ELECTORATE"]]] += int(r["ELECTORS"])
    ov = named(M.allocate({c: rg["R3 golden"][c] - roll_o[c] for c in W.CODES})[0])
    ck(off(ov, GOLD) >= 6 and "Overseas electors are not counted in any region." in plan,
       "SF4 the overseas electors counted move %d regions; plan 2.2 rules them out" % off(ov, GOLD))
    rounded = {c: round(v) for c, v in rg["R3 golden"].items()}
    ck(alloc_of(d, rounded) == GOLD and "by largest remainders" in plan and "takes two" in plan,
       "SF5 each region's adults rounded first: the same call; plan 3.1 files the sharing")
    ck(len(concord) == 47 and all(r["REGION"] in W.CODES for r in concord.values())
       and {r["ELECTORATE"] for r in pk.snapshot} <= set(concord),
       "SF6 every electorate on the roll in one of the 16 regions")
    for nm in ("imputed kept", "imputed kept, corrected"):
        ck(alloc_of(d, C.wrong_paths(d)[nm]) != GOLD, "SF7 %s: off the golden" % nm)
    ck("except the records the census imputed" in report, "SF7 methods report 3.3 says the records file has no imputed "
                                                           "record")
    for status in ("W", "D"):
        d4 = copy.deepcopy(d)
        d4["e"] = {}
        for r in records:
            e = d4["e"].setdefault((r["REGION"], r["SEX"], min(int(r["AGE"]), 100)), [0, 0])
            e[0] += 1
            e[1] += int(r["STATUS"] in ("C", status))
        ck(alloc_of(d4, C.rungs(d4)["R3 golden"]) != GOLD, "SF8 %s counted as correct: off the golden" % status)
    ck("counted correctly: usually resident in the meshblock on census day" in report,
       "SF8 the methods report's table files C as the only correct count")
    for nm in ("cells pooled by region", "cells pooled by region and sex", "cells pooled by region and age"):
        ck(alloc_of(d, C.wrong_paths(d)[nm]) != GOLD, "SF10 %s: off the golden" % nm)
    ck("2025-01-01/2025-03-03" in notes and "the day before the 2025 census" in notes,
       "SF12 the series notes file the provisional period to the day before census day")
    ck("Dates and times are the country's time." in spec and "to the end of 30 June 2026" in spec
       and "the old platform's in the country's time, the new platform's in UTC" in dictionary,
       "SF16 specification 2 files the window and the country's time; the dictionary files each platform's time basis")
    ck("The TXN_ID of the earlier transaction this one completes or reverses" in dictionary
       and "electorate codes are those of the 2024 boundary review" not in migration,
       "SF17 SF18 the dictionary files REF_TXN; nothing files which review numbered the old platform's electorates")
    ck("each person once" in spec and "not on the roll at the close of census day" in spec,
       "SF17 specification 3 files new electors")
    ck("A removal later reversed was not a removal." in spec and "11 Deceased" in dictionary.replace(":", "")
       and "01 deceased" in migration, "SF18 the death codes: the dictionary's 11 and 12, the migration notes' legacy 01")
    # ----------------------------------------------------------------------------------------------- the asks
    tn, td = truth_asks(x)
    ga, gb = pk.new_electors(), pk.removed_dead()
    ck(all(ga[c] == tn[c] for c in W.CODES), "ask A equals the generator's truth in every region")
    ck(all(gb[c] == td[c] for c in W.CODES), "ask B equals the generator's truth in every region")
    ck(all(ga[c] > 0 and gb[c] > 0 for c in W.CODES), "every region has new electors and deaths")
    stops_a = {"SF19 every electorate number read as the 2024 review's": pk.new_electors(vintage=False),
               "SF17 each person reference once, REF_TXN not followed": pk.new_electors(link=False),
               "SF17 a person whose first transaction is a removal was on the roll": pk.new_electors(prior="first"),
               "SF17 both, as the round-1 readers took it": pk.new_electors(link=False, prior="first"),
               "SF16 the stamps as written": pk.new_electors(utc=False),
               "census day included": pk.new_electors(census_day=True),
               "overseas addresses included": pk.new_electors(overseas=True),
               "rejected applications included": pk.new_electors(rejected=True)}
    for k, v in stops_a.items():
        ck(hits(v, ga) <= 1, "ask A stop misses 15 or 16: %s (%d kept)" % (k, hits(v, ga)))
    stops_b = {"SF19 every electorate number read as the 2024 review's": pk.removed_dead(vintage=False),
               "SF18 only reinstatements reverse a removal": pk.removed_dead(reversals="rei"),
               "SF18 no reversal netted": pk.removed_dead(reversals=None),
               "SF16 the stamps as written": pk.removed_dead(utc=False),
               "SF18 the current codes only": pk.removed_dead(codes="current"),
               "SF18 01 as a death throughout": pk.removed_dead(codes="all")}
    for k, v in stops_b.items():
        ck(hits(v, gb) <= 3, "ask B stop misses 13 or more: %s (%d kept)" % (k, hits(v, gb)))
    ck(hits(pk.removed_dead(census_day=True), gb) <= 10, "ask B: census day included keeps 10 or fewer")
    best_a = max(hits(pk.new_electors(vintage=v, link=lk, prior=pr, utc=u), ga)
                 for v, lk, pr, u in itertools.product((True, False), (True, False), ("record", "first"), (True, False))
                 if (v, lk, pr, u) != (True, True, "record", True))
    best_b = max(hits(pk.removed_dead(vintage=v, reversals=rv, utc=u, codes=co), gb)
                 for v, rv, u, co in itertools.product((True, False), ("all", "rei", None), (True, False),
                                                       ("platform", "current", "all"))
                 if (v, rv, u, co) != (True, "all", True, "platform"))
    ck(best_a <= 1 and best_b <= 3, "the strongest mishandled reading keeps %d of ask A and %d of ask B" % (best_a, best_b))
    ck(hits(pk.new_electors(vintage=False, link=False), ga) == 0 and hits(pk.removed_dead(vintage=False, reversals="rei"),
                                                                         gb) <= 1,
       "the cracker's reading (every filed rule, the current numbers, reinstatements, one person a reference) misses")
    # the evidence a grader verifies: the links and the numbering, record by record
    by_id = {r["TXN_ID"]: r for r in pk.log}
    moves = [(r, by_id.get(r["REF_TXN"])) for r in pk.log if r["TXN_TYPE"] == "DEL" and r["REASON"] == "05"]
    ck(moves and all(n is not None and n["TXN_TYPE"] == "NEW" and n["SEX"] == r["SEX"] and n["BIRTH_YEAR"] ==
                     r["BIRTH_YEAR"] and n["PERSON_REF"] != r["PERSON_REF"] and n["ELECTORATE"] != r["ELECTORATE"]
                     and 0 < (M.local_time(r) - M.local_time(n)).total_seconds() <= 90 for r, n in moves),
       "SF17 every old-platform removal for a move points at the enrolment at the new address seconds before it, another "
       "person reference, the same sex and year of birth (%d)" % len(moves))
    revs = [(r, by_id.get(r["REF_TXN"])) for r in pk.log if r["TXN_TYPE"] == "NEW" and r["REF_TXN"]]
    ck(revs and all(d_ is not None and d_["TXN_TYPE"] == "DEL" and d_["REASON"] == "01" and M.old_platform(d_)
                    and M.old_platform(r) and d_["ELECTORATE"] == r["ELECTORATE"] for r, d_ in revs),
       "SF18 every enrolment pointing at a removal puts right an old-platform death removal in the same electorate (%d)"
       % len(revs))
    cross = [(r, by_id[r["REF_TXN"]]) for r in pk.log if r["TXN_TYPE"] == "REI" and M.old_platform(by_id[r["REF_TXN"]])]
    same_now = sum(1 for a, b in cross if pk.region_of[a["ELECTORATE"]] == pk.region_of[b["ELECTORATE"]])
    same_then = sum(1 for a, b in cross if pk.region_2020[b["ELECTORATE"]] == pk.region_of[a["ELECTORATE"]])
    ck(len(cross) >= 40 and same_then == len(cross) and same_now < 0.6 * len(cross),
       "SF19 the %d reinstatements of old-platform removals restore the same region under the 2020 numbers (%d) and not "
       "under the current ones (%d)" % (len(cross), same_then, same_now))
    olds = {r["ELECTORATE"] for r in pk.log if M.old_platform(r)}
    ck(olds <= set(pk.region_of), "SF19 every old-platform electorate number is also a current one: nothing fails to join")
    stamps = [r["PROCESSED"] for r in pk.log]
    ck(min(stamps) >= "2025-03-04 00:00:00" and max(stamps) <= "2026-06-30 23:59:59",
       "the log's stamps lie between census day and the extract's close (%s to %s)" % (min(stamps), max(stamps)))
    late = sum(1 for r in pk.log if not M.old_platform(r) and M.local_time(r).date() > W.LOG_END)
    ck(late > 500, "the extract's close in UTC carries %d transactions of the country's 1 July" % late)
    first_new = min(int(r["ELECTOR_NO"]) for r in pk.log if r["TXN_TYPE"] == "NEW" and r["STATUS"] == "A")
    ck(first_new % 1000 and first_new > max(int(r["ELECTOR_NO"]) for r in pk.log if r["TXN_TYPE"] == "DEL" and
                                            r["ELECTOR_NO"] and int(r["ELECTOR_NO"]) < first_new),
       "elector numbers run on from the census-day counter, not from a round number (%d)" % first_new)
    # --------------------------------------------------------------------------- separation and distractors
    pk2 = copy.copy(pk)
    pk2.log = []
    ck(named(pk2.allocation()[0]) == GOLD, "separation: the call reads no transaction-log row")
    tmp = tempfile.mkdtemp(prefix="sep", dir=os.path.dirname(os.path.abspath(target)))
    try:
        for k in P.FILES:
            if k not in ("dictionary", "migration", "spec", "plan") + tuple(P.DISTRACTORS):
                shutil.copy2(f(k), os.path.join(tmp, P.FILES[k]))
        pk3 = B.Pack(tmp)
        ck(named(pk3.allocation()[0]) == GOLD and pk3.new_electors() == ga and pk3.removed_dead() == gb,
           "the golden and both asks unchanged with both distractors and the documents deleted")
    finally:
        shutil.rmtree(tmp)
    ea = estimate_alloc(target, pk)
    ck(off(ea, GOLD) >= 6 and off(ea, R0) >= 6, "the 2024 estimates (wrong-basis distractor) file neither the golden nor "
                                                "R0 (%d and %d regions off)" % (off(ea, GOLD), off(ea, R0)))
    # ----------------------------------------------------------------------------------- dates and realism
    ck("Updated 14 April 2025" in notes and "by 14 April 2025" in notes, "the series notes dated after the period they hold")
    ck("September 2025" in report and "27 June 2025" in report, "the methods report dated after its fieldwork")
    ck("9 September 2025" in migration and "4 August 2025" in migration, "the migration notes dated after the move")
    ck("22 September 2026" in plan and "Version 1.2, 30 September 2026" in spec, "the plan and the specification dated "
                                                                                 "before the deliverable, after the log")
    ck("Released 18 November 2025" in workbook, "the census workbook released after the survey's fieldwork")
    ck(len(set(d["roll"].values())) == 16 and len(set(ga.values())) == 16 and len(set(gb.values())) == 16,
       "realism: no two regions share an elector count, a new-elector count or a death count")
    by_year = [d["births"][(y, s)] for (y, s) in d["births"] if y != "2025Q"]
    ck(len(set(by_year)) > 0.95 * len(by_year), "realism: the births series is not a constant stream")
    snap = [int(r["ELECTORS"]) for r in pk.snapshot if r["ADDRESS_TYPE"] == "R"]
    ck(len(set(snap)) > 0.5 * len(snap), "realism: the roll snapshot's electorate counts vary (%d distinct of %d)" % (
        len(set(snap)), len(snap)))
    ck(W.PEOPLE["commission"] in plan and all(p in ("Chelsea Buckley", "Bryan Tapp") for p in W.PEOPLE.values()),
       "realism: the personas are the guard's draw (%s)" % sorted(W.PEOPLE.values()))
    nat_count = sum(v[0] for v in d["census"].values())
    ck(nat_count % 100 and sum(d["roll"].values()) % 100 and all(d["roll"][c] % 1000 for c in W.CODES)
       and sum(1 for c in W.CODES if d["roll"][c] % 10 == 0) <= 5, "no round totals in the census or the roll")
    # ----------------------------------------------------------------------------------------- figures.json
    sub_path = os.path.join(os.path.dirname(os.path.abspath(target)), "submission.md")
    if os.path.exists(sub_path):
        import re
        cited = set(re.findall(r"[a-z0-9_]+\.(?:csv|xlsx|pdf|docx)", open(sub_path, encoding="utf-8").read()))
        cited -= {"enrolment_gap_allocation_2027.csv"}
        ck(cited and cited <= set(files), "every file submission.md cites ships in the pack (%s)" % sorted(cited - set(files)))
    if fig_path and gdir:
        fig = json.load(open(fig_path, encoding="utf-8"))
        ck(fig["call"]["organisers"] == GOLD and fig["call"]["total"] == 200, "figures.json: the call")
        ck(fig["default"]["organisers"] == DEFAULT and sorted(fig["default"]["changed"]) == sorted(CHANGED),
           "figures.json: the default path")
        with open(os.path.join(gdir, "enrolment_gap_allocation_2027.csv"), encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        ck([r["REGION_CODE"] for r in rows] == list(W.CODES) and list(rows[0]) == ["REGION_CODE", "REGION", "ORGANISERS",
                                                                                   "NEW_ELECTORS", "REMOVED_DIED"],
           "the CSV: 16 rows in region code order in the specification's layout")
        for r in rows:
            c = r["REGION_CODE"]
            ck(r["REGION"] == W.NAME[c] and int(r["ORGANISERS"]) == GOLD[W.NAME[c]] and int(r["NEW_ELECTORS"]) == ga[c]
               and int(r["REMOVED_DIED"]) == gb[c], "the CSV row %s agrees" % c)
    print("checks: %d of %d passed" % (ck.n - ck.failed, ck.n))
    return ck.ok


if __name__ == "__main__":
    import sys
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    sys.exit(0 if run(os.path.join(task, "target"), os.path.join(task, "golden"),
                      meta_path=os.path.join(task, "metadata.json"), fig_path=os.path.join(here, "figures.json")) else 1)
