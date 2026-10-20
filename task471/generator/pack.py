"""The pack's tables for task471. Everything here is built from sim.world(): each person gets an educator record
(identifier, name, birth date), every attempt since 2019 goes into the Board's history, the 2024-25 completers into
the completer register, the 2026 registrations into Arcwright's files with the Board's crosswalk, and the June 2026
written-assignment reads, validity papers included, into the read file."""
import csv
import datetime as dt
import io

import numpy as np

import methods as M
import sim as S
import world as W

FILES = {
    "tr2025": "Pellmore_ELI_Technical_Report_June2025_Form25A.pdf",
    "memo": "BESL_OAR_Form26A_Assembly_Memo.pdf",
    "standard": "BESL_Program_Review_Standard_2027.pdf",
    "framework": "BESL_ELI_Framework_2024.pdf",
    "adminsum": "Arcwright_ELI_June2026_Administration_Summary.pdf",
    "maps": "ELI_item_maps_25A_26A.xlsx",
    "conv": "ELI_Form25A_raw_to_scale.csv",
    "scores25": "pellmore_ELI_June2025_scores.csv",
    "scores26": "arcwright_ELI_June2026_scores.csv",
    "items26": "arcwright_ELI_June2026_item_responses.csv",
    "reads26": "arcwright_ELI_June2026_written_assignment_reads.csv",
    "qc26": "arcwright_ELI_June2026_scoring_QC.xlsx",
    "history": "BESL_ELI_attempt_history_2019-2026.csv",
    "crosswalk": "BESL_arcwright_registration_crosswalk_2026.csv",
    "completers": "EPP_Title_II_completers_2025-26.xlsx",
    "register": "BESL_completer_register_2019-20_to_2024-25.csv",
    "directory": "BESL_EPP_directory_2026.csv",
}
W.FILES.update(FILES)

FIRST_F = ["EMILY", "SARAH", "JESSICA", "ASHLEY", "AMANDA", "BRITTANY", "SAMANTHA", "MEGAN", "LAUREN", "RACHEL",
           "HANNAH", "KAYLA", "TAYLOR", "ALYSSA", "MORGAN", "ABIGAIL", "MADISON", "OLIVIA", "EMMA", "GRACE", "KATIE",
           "ALLISON", "KATHERINE", "ELIZABETH", "MARIA", "ANA", "DANIELA", "GABRIELA", "VANESSA", "JASMINE", "AALIYAH",
           "DESTINY", "KIARA", "MONIQUE", "ALEXIS", "COURTNEY", "LINDSEY", "HALEY", "SYDNEY", "BRIANNA", "CHELSEA",
           "MOLLY", "CAITLIN", "NATALIE", "SOPHIA", "ISABEL", "LEAH", "PAIGE", "ERIN", "KELSEY", "ANDREA", "MARISOL",
           "YESENIA", "LUCIA", "PRIYA", "ANJALI", "MEI", "LINH", "THAO", "HANA", "AMINA", "FATIMA", "NADIA", "TIERRA",
           "SHANICE", "EBONY", "KENDRA", "TONYA", "RENEE", "JILL", "HOLLY", "AMBER", "CRYSTAL", "MELISSA", "STEPHANIE"]
FIRST_M = ["MICHAEL", "CHRISTOPHER", "MATTHEW", "JOSHUA", "ANDREW", "DANIEL", "JUSTIN", "TYLER", "BRANDON", "RYAN",
           "JACOB", "AUSTIN", "KEVIN", "JORDAN", "ZACHARY", "NATHAN", "ETHAN", "CALEB", "LOGAN", "ISAAC", "CARLOS",
           "JOSE", "LUIS", "MIGUEL", "DIEGO", "ADRIAN", "MARCUS", "DARNELL", "TERRELL", "ANDRE", "JAMAL", "MALIK",
           "DEVON", "TREVOR", "GARRETT", "COLIN", "SEAN", "PATRICK", "DEREK", "BRADLEY", "TRAVIS", "CODY", "DUSTIN",
           "HUNG", "MINH", "RAJ", "ARJUN", "OMAR", "SAMUEL", "ELIJAH", "GABRIEL", "MASON", "CONNOR", "BRETT"]
LAST = ["SMITH", "JOHNSON", "WILLIAMS", "BROWN", "JONES", "GARCIA", "MILLER", "DAVIS", "RODRIGUEZ", "MARTINEZ",
        "HERNANDEZ", "LOPEZ", "GONZALEZ", "WILSON", "ANDERSON", "THOMAS", "TAYLOR", "MOORE", "JACKSON", "MARTIN",
        "LEE", "PEREZ", "THOMPSON", "WHITE", "HARRIS", "SANCHEZ", "CLARK", "RAMIREZ", "LEWIS", "ROBINSON", "WALKER",
        "YOUNG", "ALLEN", "KING", "WRIGHT", "SCOTT", "TORRES", "NGUYEN", "HILL", "FLORES", "GREEN", "ADAMS", "NELSON",
        "BAKER", "HALL", "RIVERA", "CAMPBELL", "MITCHELL", "CARTER", "ROBERTS", "GOMEZ", "PHILLIPS", "EVANS", "TURNER",
        "DIAZ", "PARKER", "CRUZ", "EDWARDS", "COLLINS", "REYES", "STEWART", "MORRIS", "MORALES", "MURPHY", "COOK",
        "ROGERS", "GUTIERREZ", "ORTIZ", "MORGAN", "COOPER", "PETERSON", "BAILEY", "REED", "KELLY", "HOWARD", "RAMOS",
        "KIM", "COX", "WARD", "RICHARDSON", "WATSON", "BROOKS", "CHAVEZ", "WOOD", "BENNETT", "GRAY", "MENDOZA",
        "RUIZ", "HUGHES", "PRICE", "ALVAREZ", "CASTILLO", "SANDERS", "PATEL", "MYERS", "LONG", "ROSS", "FOSTER",
        "JIMENEZ", "POWELL", "JENKINS", "PERRY", "RUSSELL", "SULLIVAN", "BELL", "COLEMAN", "BUTLER", "HENDERSON",
        "BARNES", "GONZALES", "FISHER", "VASQUEZ", "SIMMONS", "ROMERO", "JORDAN", "PATTERSON", "ALEXANDER", "HAMILTON",
        "GRAHAM", "REYNOLDS", "GRIFFIN", "WALLACE", "MORENO", "WEST", "COLE", "HAYES", "BRYANT", "HERRERA", "GIBSON",
        "ELLIS", "TRAN", "MEDINA", "AGUILAR", "STEVENS", "MURRAY", "FORD", "CASTRO", "MARSHALL", "OWENS", "HARRISON",
        "FERNANDEZ", "MCDONALD", "WOODS", "WASHINGTON", "KENNEDY", "WELLS", "VARGAS", "HENRY", "CHEN", "FREEMAN",
        "WEBB", "TUCKER", "GUZMAN", "BURNS", "CRAWFORD", "OLSON", "SIMPSON", "PORTER", "HUNTER", "GORDON", "MENDEZ",
        "SILVA", "SHAW", "SNYDER", "MASON", "DIXON", "MUNOZ", "HUNT", "HICKS", "HOLMES", "PALMER", "WAGNER", "BLACK",
        "ROBERTSON", "BOYD", "ROSE", "STONE", "SALAZAR", "FOX", "WARREN", "MILLS", "MEYER", "RICE", "SCHMIDT",
        "GARZA", "DANIELS", "FERGUSON", "NICHOLS", "STEPHENS", "SOTO", "WEAVER", "RYAN", "GARDNER", "PAYNE", "GRANT",
        "DUNN", "KELLEY", "SPENCER", "HAWKINS", "ARNOLD", "PIERCE", "VAZQUEZ", "HANSEN", "PETERS", "SANTOS", "HART",
        "BRADLEY", "KNIGHT", "ELLIOTT", "CUNNINGHAM", "DUNCAN", "ARMSTRONG", "HUDSON", "CARROLL", "LANE", "RILEY",
        "ANDREWS", "ALVARADO", "RAY", "DELGADO", "BERRY", "PERKINS", "HOFFMAN", "JOHNSTON", "MATTHEWS", "PENA",
        "RICHARDS", "CONTRERAS", "WILLIS", "CARPENTER", "LAWRENCE", "SANDOVAL", "O'BRIEN", "O'NEAL", "MCCARTHY",
        "DELA CRUZ", "VAN DYKE", "ST. JOHN"]
CENTRES = [("C01", "Capitol City", "Northgate Learning Commons, Suite 210"), ("C02", "Harlow", "Harlow Business Park, Bldg C"),
           ("C03", "Mill Falls", "Riverside Professional Center"), ("C04", "Elkton", "Elkton Community College, Testing Office"),
           ("C05", "Port Ansel", "Bayfront Plaza, 4th Floor"), ("C06", "Granger", "Granger Career Center, Room 118")]
PATHWAYS_OTHER = ["Early Childhood", "Special Education", "Secondary English", "Secondary Mathematics"]


def rng(seed, part):
    return np.random.default_rng([seed, 100 + part])


def birth_date(r, age):
    """a birth date for someone of the given age on the June 2026 administration"""
    days = int(age * 365.25) + int(r.integers(0, 365))
    return W.ADMIN[2026] - dt.timedelta(days=days)


# ----------------------------------------------------------------------------------------------- the population
def people(x):
    """give every simulated candidate an educator record and add the people the Board's files hold beside them:
    the 2024-25 completers who first tested in June 2024 or had not tested by June 2025, the earlier program
    years' completers in the register, and earlier candidates in the history"""
    r = rng(x["seed"], 1)
    rows = x["rows"]
    used = set()

    def new_id():
        while True:
            v = "E%07d" % int(r.integers(1000000, 9999999))
            if v not in used:
                used.add(v)
                return v

    def name():
        f = (FIRST_F if r.random() < 0.78 else FIRST_M)
        return f[int(r.integers(len(f)))], LAST[int(r.integers(len(LAST)))]
    for p in rows:
        p["eid"] = new_id()
        p["first_name"], p["last_name"] = name()
        age = 23 + r.gamma(2.0, 2.2) if p["group"] in ("completer", "earlier") else 26 + r.gamma(2.0, 3.5)
        p["dob"] = birth_date(r, age)
    # 2024-25 completers: the ones the simulation already tests first in June 2025 ("earlier"), plus those who
    # tested first in June 2024 and those not yet tested by June 2025, in each program's proportions
    cohort = [p for p in rows if p["group"] == "earlier"]
    by_prog = {}
    for p in cohort:
        by_prog.setdefault(p["program"], []).append(p)
    extra = []
    for k, (nm, code, kind, n, s1, s2, early, untested) in enumerate(W.PROGRAMS):
        n25 = len(by_prog.get(k, []))
        n24 = int(round(n25 * early / (1 - early - untested)))
        nun = int(round(n25 * untested / (1 - early - untested)))
        for j in range(n24 + nun):
            t1 = r.normal(s1, 0.95)
            p = dict(group="earlier24" if j < n24 else "earlier_untested", program=k, cohort="pre", t1=t1,
                     t2=W.RHO * (t1 - s1) + np.sqrt(1 - W.RHO ** 2) * r.normal(0, 0.95) + s2, first=2024 if j < n24 else None,
                     history=[], sits=[])
            p["eid"] = new_id()
            p["first_name"], p["last_name"] = name()
            p["dob"] = birth_date(r, 23 + r.gamma(2.0, 2.2))
            extra.append(p)
    # a June 2024 first attempt passes with the chance its ability gives at the 2024 standard
    for p in extra:
        if p["group"] == "earlier24":
            p["result24"] = "PASS" if r.random() < 1 / (1 + np.exp(-1.9 * (0.55 * p["t1"] + 0.45 * p["t2"] + 0.95))) else "FAIL"
    x["extra"] = extra
    # completion dates: 2025-26 completers in the program year, 2024-25 completers in theirs
    for p in rows + extra:
        if p["group"] == "completer":
            p["completed"] = completion_date(r, 2025, W.PROGRAMS[p["program"]][2])
        elif p["group"] in ("earlier", "earlier24", "earlier_untested"):
            p["completed"] = completion_date(r, 2024, W.PROGRAMS[p["program"]][2])
    # earlier program years for the register (2019-20 to 2023-24): completers and their attempts
    x["older"] = older_completers(x, r, new_id, name)
    # the repeat candidates' earlier attempts get dates and results
    return x


def completion_date(r, start_year, kind):
    """university programs complete at the end of fall (December) or spring (May), a few in summer; alternative
    routes at the end of the residency year (June) or in the summer"""
    u = r.random()
    if kind == "alternative":
        d = dt.date(start_year + 1, 6, 1) + dt.timedelta(days=int(r.integers(0, 29))) if u < 0.7 else \
            dt.date(start_year, 7, 15) + dt.timedelta(days=int(r.integers(0, 40)))
    elif u < 0.24:
        d = dt.date(start_year, 12, 5) + dt.timedelta(days=int(r.integers(0, 16)))
    elif u < 0.93:
        d = dt.date(start_year + 1, 5, 2) + dt.timedelta(days=int(r.integers(0, 18)))
    else:
        d = dt.date(start_year, 7, 20) + dt.timedelta(days=int(r.integers(0, 30)))
    return d


def older_completers(x, r, new_id, name):
    out = []
    for yr in range(2019, 2024):
        for k, pr in enumerate(W.PROGRAMS):
            n = int(round(pr[3] * (0.84 + 0.05 * (yr - 2019)) * r.uniform(0.9, 1.1)))
            for _ in range(n):
                p = dict(group="older", program=k, year=yr, eid=new_id())
                p["first_name"], p["last_name"] = name()
                p["dob"] = birth_date(r, 23 + (2026 - yr - 1) + r.gamma(2.0, 2.2))
                p["completed"] = completion_date(r, yr, pr[2])
                # first attempt: the June after completion mostly, the June before for some; most pass at once
                fy = yr + 1 if r.random() < 0.86 else yr
                tries = [fy]
                passed = r.random() < 0.80
                while not passed and tries[-1] < 2024 and r.random() < 0.6:
                    tries.append(tries[-1] + 1)
                    passed = r.random() < 0.55
                p["attempts"] = [(y, "PASS" if (i == len(tries) - 1 and passed) else "FAIL") for i, y in enumerate(tries)]
                out.append(p)
    return out


# ----------------------------------------------------------------------------------------------- the conversion
def scale_of(raw):
    """Form 25A's raw-to-scale conversion: 240 at raw 56"""
    c = W.PASS_RAW_25A - 14 * np.log(7 / 3)
    return int(np.floor(100 + 200 / (1 + np.exp(-(raw - c) / 14)) + 0.5))


def conversion_rows():
    return [[raw, scale_of(raw)] for raw in range(W.MAX_RAW + 1)]


# ------------------------------------------------------------------------------------------------- item identity
def item_maps(x):
    """item identifiers and positions: the shared items carry the same identifier on both forms"""
    r = rng(x["seed"], 2)
    ids = r.choice(np.arange(10000, 99999), W.N_SHARED + 2 * (W.N_MC - W.N_SHARED), replace=False)
    shared = ["ELI-%05d" % v for v in ids[:W.N_SHARED]]
    own25 = ["ELI-%05d" % v for v in ids[W.N_SHARED:W.N_MC]]
    own26 = ["ELI-%05d" % v for v in ids[W.N_MC:]]
    sub = lambda n: [("Foundational Reading Skills", "Comprehension and Vocabulary", "Assessment and Instruction",
                      "Writing and Language")[int(v)] for v in r.integers(0, 4, n)]
    sub_sh, sub25, sub26 = sub(W.N_SHARED), sub(W.N_MC - W.N_SHARED), sub(W.N_MC - W.N_SHARED)
    keys = {i: "ABCD"[int(v)] for i, v in zip(shared + own25 + own26, r.integers(0, 4, len(shared) + 2 * len(own25)))}
    maps = {}
    for yr, own, sb in ((2025, own25, sub25), (2026, own26, sub26)):
        items = shared + own                      # simulation order: shared first
        subs = sub_sh + sb
        pos = x["f25" if yr == 2025 else "f26"]["pos"]   # pos[i] = position (0-based) of simulation item i
        rows = [None] * W.N_MC
        for i in range(W.N_MC):
            rows[pos[i]] = (pos[i] + 1, items[i], subs[i])
        maps[yr] = rows
    x["maps"], x["keys"] = maps, keys
    x["wa_ids"] = {2025: ["WA-25-1", "WA-25-2", "WA-25-3"], 2026: ["WA-26-1", "WA-25-2", "WA-26-3"]}
    return maps


# --------------------------------------------------------------------------------------------- 2026 registrations
def registrations(x):
    r = rng(x["seed"], 3)
    s26 = x["scored"][2026]
    regs = []
    used = set()
    for j, i in enumerate(s26["idx"]):
        p = x["rows"][i]
        while True:
            reg = "AW26-%06d" % int(r.integers(100000, 999999))
            if reg not in used:
                used.add(reg)
                break
        u = r.random()
        if u < 0.035:
            typed = ""
        elif u < 0.055:                           # two digits typed the wrong way round
            d = list(p["eid"])
            k = int(r.integers(2, 7))
            d[k], d[k + 1] = d[k + 1], d[k]
            typed = "".join(d)
        else:
            typed = p["eid"] if r.random() < 0.8 else p["eid"][1:]
        how = "ID on registration" if typed == p["eid"] or typed == p["eid"][1:] else \
            ("Name and birth date" if r.random() < 0.85 else "Manual review")
        regs.append(dict(reg=reg, j=j, i=i, typed=typed, how=how, centre=CENTRES[int(r.integers(len(CENTRES)))][0]))
    x["regs"] = regs
    return regs


# ---------------------------------------------------------------------------------------------------- the history
def history_rows(x):
    """every ELI attempt the Board's licensing system holds, 2019 to June 2026, one row per attempt"""
    r = rng(x["seed"], 4)
    out = []

    def row(p, yr, result, scale=""):
        out.append([p["eid"], p["last_name"], p["first_name"], p["dob"].strftime("%m/%d/%Y"),
                    W.ADMIN[yr].isoformat(), W.FORMS[yr], W.OLD_CO if yr <= 2025 else W.NEW_CO, result, scale])
    for p in x["older"]:
        for yr, res in p["attempts"]:
            row(p, yr, res, str(int(np.clip(r.normal(258 if res == "PASS" else 221, 12), 241 if res == "PASS" else 150,
                                            298 if res == "PASS" else 239))))
    for p in x["extra"]:
        if p["group"] == "earlier24":
            res = p["result24"]
            row(p, 2024, res, str(int(np.clip(r.normal(258 if res == "PASS" else 224, 11), 241 if res == "PASS" else 160,
                                             298 if res == "PASS" else 239))))
    for p in x["rows"]:
        for yr in p["history"]:
            row(p, yr, "FAIL", str(int(np.clip(r.normal(222, 10), 160, 239))))
    s25 = x["scored"][2025]
    for j, i in enumerate(s25["idx"]):
        p = x["rows"][i]
        raw = int(s25["raw"][j])
        row(p, 2025, "PASS" if raw >= W.PASS_RAW_25A else "FAIL", str(scale_of(raw)))
    for reg in x["regs"]:
        row(x["rows"][reg["i"]], 2026, "", "")
    out.sort(key=lambda v: (v[4], v[0]))
    return out


HISTORY_COLS = ["EDUCATOR_ID", "LAST_NAME", "FIRST_NAME", "BIRTH_DATE", "TEST_DATE", "FORM", "CONTRACTOR", "RESULT",
                "SCALE_SCORE"]


# ---------------------------------------------------------------------------------------------------- the register
REGISTER_COLS = ["EDUCATOR_ID", "LAST_NAME", "FIRST_NAME", "BIRTH_DATE", "PROGRAM_CODE", "PATHWAY", "PROGRAM_YEAR",
                 "COMPLETION_DATE"]


def register_rows(x):
    """the Board's completer register, program years 2019-20 to 2024-25. In 2024-25 a program could open a new
    educator record when its lookup missed the candidate, so some 2024-25 completers sit in the register under a
    record other than the one their attempts carry (the same person, name and birth date)"""
    r = rng(x["seed"], 5)
    out = []
    used = {p["eid"] for p in x["rows"]} | {p["eid"] for p in x["extra"]} | {p["eid"] for p in x["older"]}

    def fresh():
        while True:
            v = "E%07d" % int(r.integers(1000000, 9999999))
            if v not in used:
                used.add(v)
                return v
    cohort = [p for p in x["rows"] if p["group"] == "earlier"] + x["extra"]
    tested = {}
    for p in cohort:
        p["reg_eid"] = p["eid"]
        p["pathway"] = "Elementary" if r.random() < 0.9 else "Elementary and Special Education"
        if p["group"] in ("earlier", "earlier24"):
            tested.setdefault(p["program"], []).append(p)
    for k, ps in sorted(tested.items()):
        n = max(2, int(round(len(ps) * x["p"].get("dup_rate", 0.055))))
        for q in r.choice(len(ps), n, replace=False):
            ps[q]["reg_eid"] = fresh()
            ps[q]["dup"] = True
    for p in x["older"]:
        out.append([p["eid"], p["last_name"], p["first_name"], p["dob"].isoformat(), W.PROGRAMS[p["program"]][1],
                    "Elementary" if r.random() < 0.9 else "Elementary and Special Education",
                    "%d-%02d" % (p["year"], (p["year"] + 1) % 100), p["completed"].isoformat()])
    for p in cohort:
        out.append([p["reg_eid"], p["last_name"], p["first_name"], p["dob"].isoformat(), W.PROGRAMS[p["program"]][1],
                    p["pathway"], "2024-25", p["completed"].isoformat()])
    # the programs' other pathways, which take other tests
    for yr in range(2019, 2025):
        for k, pr in enumerate(W.PROGRAMS):
            if pr[2] == "alternative" and r.random() < 0.5:
                continue
            for _ in range(int(pr[3] * r.uniform(0.12, 0.3))):
                f = (FIRST_F if r.random() < 0.75 else FIRST_M)
                out.append([fresh(), LAST[int(r.integers(len(LAST)))], f[int(r.integers(len(f)))],
                            birth_date(r, 23 + (2026 - yr - 1) + r.gamma(2.0, 2.2)).isoformat(), pr[1],
                            PATHWAYS_OTHER[int(r.integers(len(PATHWAYS_OTHER)))], "%d-%02d" % (yr, (yr + 1) % 100),
                            completion_date(r, yr, pr[2]).isoformat()])
    out.sort(key=lambda v: (v[6], v[4], v[1], v[2]))
    return out


# ------------------------------------------------------------------------------------------ 2025-26 submissions
LAYOUTS = {
    "A": ["Educator ID", "Last Name", "First Name", "Date of Birth", "Pathway", "Completion Date"],
    "B": ["STATE ID", "NAME", "DOB", "PROGRAM AREA", "TERM", "DATE COMPLETED"],
    "C": ["Candidate", "Educator #", "Birthdate", "Licensure Area", "Residency Exit", "Recommended (Y/N)"],
}
LAYOUT_OF = {0: "A", 1: "B", 2: "A", 3: "B", 4: "A", 5: "B", 6: "A", 7: "A", 8: "B", 9: "A", 10: "B", 11: "A",
             12: "C", 13: "C", 14: "C", 15: "B"}
AREA_WORDS = {"A": ("Elementary", "Elementary/SPED Dual"), "B": ("ELEM ED", "ELEM ED + SPED"),
              "C": ("Elementary (K-6)", "Elementary (K-6) and Special Ed")}


def term_of(d):
    if d.month in (12, 1):
        return "Fall %d" % (d.year if d.month == 12 else d.year - 1)
    if d.month in (4, 5, 6):
        return "Spring %d" % d.year
    return "Summer %d" % d.year


def submission_sheets(x):
    """each program's Title II completer list for 2025-26 in its own layout: its 2025-26 completers in every
    pathway, a few of the previous year's late-spring completers carried on, a few summer 2026 completers, and the
    odd row pasted twice"""
    r = rng(x["seed"], 6)
    sheets = {}
    prev = {}
    for p in [q for q in x["rows"] if q["group"] == "earlier"] + x["extra"]:
        if p["completed"].month in (5, 6):
            prev.setdefault(p["program"], []).append(p)
    for k, pr in enumerate(W.PROGRAMS):
        lay = LAYOUT_OF[k]
        rows = []
        mine = [p for p in x["rows"] if p["group"] == "completer" and p["program"] == k]
        for p in mine:
            p["pathway"] = "Elementary" if r.random() < 0.9 else "Elementary and Special Education"
            rows.append(dict(eid=p["eid"], last=p["last_name"], first=p["first_name"], dob=p["dob"],
                             path=0 if p["pathway"] == "Elementary" else 1, done=p["completed"]))
        for p in (r.choice(prev.get(k, []), min(len(prev.get(k, [])), int(r.integers(1, 4))), replace=False)
                  if prev.get(k) else []):
            rows.append(dict(eid=p["eid"], last=p["last_name"], first=p["first_name"], dob=p["dob"], path=0,
                             done=p["completed"]))
        for _ in range(int(r.integers(1, 5)) if pr[2] != "alternative" else 0):
            f = (FIRST_F if r.random() < 0.78 else FIRST_M)
            rows.append(dict(eid="E%07d" % int(r.integers(1000000, 9999999)), last=LAST[int(r.integers(len(LAST)))],
                             first=f[int(r.integers(len(f)))], dob=birth_date(r, 23 + r.gamma(2.0, 2.2)), path=0,
                             done=dt.date(2026, 7, 10) + dt.timedelta(days=int(r.integers(0, 25)))))
        for _ in range(int(len(mine) * r.uniform(0.10, 0.25))):
            f = (FIRST_F if r.random() < 0.75 else FIRST_M)
            rows.append(dict(eid="E%07d" % int(r.integers(1000000, 9999999)), last=LAST[int(r.integers(len(LAST)))],
                             first=f[int(r.integers(len(f)))], dob=birth_date(r, 23 + r.gamma(2.0, 2.2)), path=2,
                             other=PATHWAYS_OTHER[int(r.integers(len(PATHWAYS_OTHER)))],
                             done=completion_date(r, 2025, pr[2])))
        order = r.permutation(len(rows))
        rows = [rows[i] for i in order]
        if r.random() < 0.4:
            rows.insert(int(r.integers(len(rows))), dict(rows[int(r.integers(len(rows)))]))
        out = []
        for q in rows:
            area = q.get("other") if q["path"] == 2 else AREA_WORDS[lay][q["path"]]
            if lay == "A":
                out.append([q["eid"], q["last"].title(), q["first"].title(), q["dob"].strftime("%m/%d/%Y"), area,
                            q["done"].strftime("%m/%d/%Y")])
            elif lay == "B":
                out.append([q["eid"][1:], "%s, %s" % (q["last"], q["first"]), q["dob"].isoformat(), area,
                            term_of(q["done"]), q["done"].isoformat()])
            else:
                out.append(["%s %s" % (q["first"].title(), q["last"].title()), "E-" + q["eid"][1:],
                            q["dob"].strftime("%B %d, %Y").replace(" 0", " "), area,
                            q["done"].strftime("%B %d, %Y").replace(" 0", " "), "Y" if q["path"] != 2 or True else "Y"])
        sheets[k] = (lay, out)
    return sheets


# ------------------------------------------------------------------------------------------------ the 2025 file
SCORES25_COLS = ["CAND_ID", "LAST_NAME", "FIRST_NAME", "BIRTH_DATE", "TEST_DATE", "FORM", "CENTER", "ITEM_SCORES",
                 "MC_RAW", "WA1_R1", "WA1_R2", "WA1_R3", "WA2_R1", "WA2_R2", "WA2_R3", "WA3_R1", "WA3_R2", "WA3_R3",
                 "WA_WEIGHTED", "TOTAL_RAW", "SCALE_SCORE", "RESULT"]


def scores25_rows(x):
    r = rng(x["seed"], 7)
    s = x["scored"][2025]
    pos = x["f25"]["pos"]
    out = []
    for j, i in enumerate(s["idx"]):
        p = x["rows"][i]
        string = ["0"] * W.N_MC
        for k in range(W.N_MC):
            string[pos[k]] = str(int(s["mc"][j, k]))
        row = [p["eid"], p["last_name"], p["first_name"], p["dob"].strftime("%m/%d/%Y"), "06/14/2025", "25A",
               CENTRES[int(r.integers(len(CENTRES)))][0], "".join(string), int(s["mc"][j].sum())]
        for a in range(W.N_WA):
            row += [int(s["r1"][j, a]), int(s["r2"][j, a]), int(s["res"][j, a]) if s["res"][j, a] else ""]
        raw = int(s["raw"][j])
        row += [W.WA_WEIGHT * int(s["wa"][j].sum()), raw, scale_of(raw), "PASS" if raw >= W.PASS_RAW_25A else "FAIL"]
        out.append(row)
    out.sort(key=lambda v: v[0])
    return out


# ------------------------------------------------------------------------------------------------ the 2026 files
SCORES26_COLS = ["REG_ID", "EDUCATOR_ID", "LAST_NAME", "FIRST_NAME", "DOB", "TEST_DATE", "FORM", "CENTRE_CODE",
                 "MC_SCORE", "WA1_SCORE", "WA2_SCORE", "WA3_SCORE", "RAW_TOTAL", "STATUS"]
ITEMS26_COLS = ["REG_ID", "ITEM_POSITION", "ITEM_ID", "RESPONSE", "ITEM_SCORE"]
READ_COLS = ["READ_ID", "RESPONSE_ID", "ASSIGNMENT", "READ_TYPE", "READER_ID", "SCORE", "READ_TIME_UTC"]


def scores26_rows(x):
    s = x["scored"][2026]
    out = []
    for g in x["regs"]:
        j = g["j"]
        p = x["rows"][g["i"]]
        out.append([g["reg"], g["typed"], p["last_name"], p["first_name"], p["dob"].isoformat(), "2026-06-13", "26A",
                    g["centre"], int(s["mc"][j].sum()), int(s["wa"][j, 0]), int(s["wa"][j, 1]), int(s["wa"][j, 2]),
                    int(s["raw"][j]), "SCORED"])
    out.sort(key=lambda v: v[0])
    return out


def items26_rows(x):
    r = rng(x["seed"], 8)
    s = x["scored"][2026]
    pos, items = x["f26"]["pos"], x["maps"][2026]
    out = []
    for g in sorted(x["regs"], key=lambda v: v["reg"]):
        j = g["j"]
        for k in np.argsort(pos):
            iid = items[pos[k]][1]
            key = x["keys"][iid]
            if s["mc"][j, k]:
                resp, sc = key, 1
            elif r.random() < 0.006:
                resp, sc = "", 0
            else:
                resp, sc = "ABCD".replace(key, "")[int(r.integers(3))], 0
            out.append([g["reg"], int(pos[k]) + 1, iid, resp, sc])
    return out


RATERS = ["R%04d" % v for v in range(4101, 4173)]
LEADERS = ["SL%03d" % v for v in (204, 211, 217, 226, 238, 245)]


def reads_rows(x):
    """every read of the June 2026 written assignments: the two operational reads, a scoring leader's resolution
    read where they differ by more than one point, leaders' back-reads of a sample, and the seeded validity papers"""
    r = rng(x["seed"], 9)
    s = x["scored"][2026]
    out = []
    start = dt.datetime(2026, 6, 22, 13, 0)

    def ts():
        day = int(r.integers(0, 24))
        return (start + dt.timedelta(days=day, minutes=int(r.integers(0, 600)), seconds=int(r.integers(0, 60))))
    rid = [0]

    def add(resp, wa, typ, reader, score, when):
        rid[0] += 1
        out.append([None, resp, wa, typ, reader, int(score), when])
    for g in x["regs"]:
        j = g["j"]
        p = x["rows"][g["i"]]
        for a in range(W.N_WA):
            resp = "%s-%d" % (g["reg"], a + 1)
            wa = "WA%d" % (a + 1)
            t0 = ts()
            ra, rb = r.choice(len(RATERS), 2, replace=False)
            add(resp, wa, "FIRST", RATERS[ra], s["r1"][j, a], t0)
            add(resp, wa, "SECOND", RATERS[rb], s["r2"][j, a], t0 + dt.timedelta(hours=float(r.uniform(1, 70))))
            if s["res"][j, a]:
                add(resp, wa, "RESOLUTION", LEADERS[int(r.integers(len(LEADERS)))], s["res"][j, a],
                    t0 + dt.timedelta(hours=float(r.uniform(72, 120))))
            if r.random() < W.BACKREAD_RATE:
                base = p["t2"] - x["f26"]["wa"][a]
                v = S.rating(base + x["p"]["sev"][2026] + r.normal(0, W.LEADER_SD))
                add(resp, wa, "BACKREAD", LEADERS[int(r.integers(len(LEADERS)))], v,
                    t0 + dt.timedelta(hours=float(r.uniform(2, 90))))
    papers = x["papers"]
    for pi, v in x["vreads"]:
        pp = papers[pi]
        add(pp["id"], pp["wa"], "VALIDITY", RATERS[int(r.integers(len(RATERS)))], v, ts())
    out.sort(key=lambda v: (v[6], v[1], v[3]))
    for n, row in enumerate(out):
        row[0] = "RD%07d" % (1000001 + n)
        row[6] = row[6].strftime("%Y-%m-%dT%H:%M:%SZ")
    return out


def paper_ids(x):
    r = rng(x["seed"], 10)
    count = {}
    for pp in x["papers"]:
        count[pp["wa"]] = count.get(pp["wa"], 0) + 1
        pp["id"] = "VP-%s-%s-%03d" % (pp["src"][2:], pp["wa"], count[pp["wa"]])
    return x["papers"]


def crosswalk_rows(x):
    out = []
    for g in x["regs"]:
        out.append([g["reg"], x["rows"][g["i"]]["eid"], g["how"], "2026-07-%02d" % (6 + int(g["reg"][-1]) % 9)])
    out.sort(key=lambda v: v[0])
    return out


CROSSWALK_COLS = ["REG_ID", "EDUCATOR_ID", "MATCH_METHOD", "MATCHED_ON"]
DIRECTORY_COLS = ["PROGRAM_CODE", "PROGRAM_NAME", "PROVIDER_TYPE", "APPROVED_SINCE", "REGION"]


def directory_rows():
    regions = ["North", "Central", "Central", "South", "Central", "East", "South", "West", "East", "Central", "West",
               "North", "Statewide", "Central", "South", "East"]
    since = [1987, 1994, 1991, 2002, 1985, 1998, 1996, 2009, 1989, 1999, 2004, 2011, 2016, 2013, 2018, 2006]
    return [[pr[1], pr[0], "Institution of higher education" if pr[2] == "university" else "Alternative route provider",
             "%d-07-01" % since[k], regions[k]] for k, pr in enumerate(W.PROGRAMS)]


def write_csv(path, cols, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(cols)
        w.writerows(rows)
    return len(rows)


def everything(seed=W.SEED, **kw):
    x = S.world(seed, **kw)
    x["sim"] = S.world(seed, **kw)          # an untouched copy for the clean-truth checks
    people(x)
    item_maps(x)
    registrations(x)
    paper_ids(x)
    return x
