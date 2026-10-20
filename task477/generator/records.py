"""The board's own records and the state's employer and wage-record extracts behind the two asks: program exits,
the wage-record match return, the employer accounts and the professional employer organizations' client
registrations (ask A); the training provider list, the individual training account ledger and the fiscal agent's
check register (ask B)."""
import datetime as dt

import numpy as np

import world as W

ELIG = ["23", "31-33", "42", "44-45", "48-49", "51", "52", "53", "54", "56", "61", "62", "71", "72", "81"]
OTHER = ["11", "22", "55", "92"]
# where the board's exiters go to work (weights) and the NAICS-6 codes their employers carry
JOBS_W = {"23": 6, "31-33": 13, "42": 4, "44-45": 14, "48-49": 9, "51": 1.5, "52": 3, "53": 1.5, "54": 3.5, "56": 7,
          "61": 2.5, "62": 21, "71": 2, "72": 9, "81": 3, "11": .8, "22": .3, "55": .4, "92": 3}
NAICS6 = {"23": ["236118", "236220", "237310", "238210", "238220", "238910"], "31-33": ["311612", "326199", "332710",
          "333111", "336390"], "42": ["423830", "424410", "423690"], "44-45": ["441110", "444110", "445110", "455211",
          "447110", "459510"], "48-49": ["484121", "493110", "492110"], "51": ["517111", "518210", "519290"],
          "52": ["522110", "524210", "523150"], "53": ["531110", "532120"], "54": ["541330", "541211", "541512"],
          "56": ["561320", "561720", "562111"], "61": ["611519", "611310"], "62": ["621111", "622110", "623110",
          "624120", "621610"], "71": ["713940", "711310"], "72": ["722511", "722513", "721110"], "81": ["811111",
          "812112", "813110"], "11": ["111421"], "22": ["221122"], "55": ["551114"], "92": ["921140", "922120"]}
SEC6 = {"31": "31-33", "32": "31-33", "33": "31-33", "44": "44-45", "45": "44-45", "48": "48-49", "49": "48-49"}

STEMS = ["Tallis", "Valley", "Ridgeway", "Harbin", "Oak Bend", "Cedar Run", "Millrace", "Fairmount", "Kessler",
         "Brookfield", "Summit", "Larch", "Pioneer", "Riverside", "Hollins", "Whitmore", "Ashgrove", "Benton",
         "Carver", "Delmar", "Eastgate", "Foxhall", "Granger", "Hartwell", "Ironside", "Juniper", "Kendall",
         "Lowell", "Mason", "Northfield", "Overlook", "Parkline", "Quinlan", "Redstone", "Stanfield", "Tremont"]
KIND = {"23": ["Builders", "Construction", "Paving", "Electric", "Mechanical", "Roofing"],
        "31-33": ["Foods", "Plastics", "Machine", "Equipment", "Components"],
        "42": ["Supply", "Distributors", "Wholesale"], "44-45": ["Motors", "Hardware", "Market", "Foods", "Fuel",
                                                                 "Outlet"],
        "48-49": ["Freight", "Logistics", "Transport", "Warehousing"], "51": ["Communications", "Data", "Media"],
        "52": ["Bank", "Credit Union", "Insurance", "Financial"], "53": ["Properties", "Realty", "Rentals"],
        "54": ["Engineering", "Accounting", "Consulting", "Design"], "56": ["Staffing", "Facility Services",
                                                                          "Disposal"],
        "61": ["Learning Center", "Academy"], "62": ["Family Practice", "Medical Center", "Health Care Center",
                                                     "Home Care", "Pediatrics"],
        "71": ["Fitness", "Recreation"], "72": ["Grill", "Diner", "Pizza", "Inn", "Cafe"],
        "81": ["Auto Repair", "Salon", "Services"], "11": ["Farms"], "22": ["Power"], "55": ["Holdings"],
        "92": ["County", "City"]}
SUFFIX = ["Inc", "LLC", "Co", "Inc.", "LLC", "Corp", "Group"]
PEOS = [("Keystone Employer Services LLC", "0479113"), ("Prairie HR Partners Inc", "0480260"),
        ("Unity Workforce Solutions LLC", "0483377"), ("Summit PEO Group Inc", "0486612")]


CATALOG = {
    "23": [("Electrical Pre-Apprenticeship", "46.0399"), ("HVAC Technician Certificate", "47.0201"),
           ("Construction Craft Laborer", "46.0000")],
    "31-33": [("CNC Machining Certificate", "48.0510"), ("Industrial Maintenance Technician", "47.0303"),
              ("Welding Technology", "48.0508")],
    "42": [("Distribution and Inside Sales Certificate", "52.1804"), ("Parts Specialist", "47.0699")],
    "44-45": [("Retail Management Certificate", "52.1803"), ("Pharmacy Clerk and Retail Operations", "52.1899")],
    "48-49": [("Commercial Driver License Class A", "49.0205"), ("Diesel Technician", "47.0605"),
              ("Forklift and Warehouse Operations", "52.0203")],
    "51": [("Network Support Technician", "11.0901"), ("Cloud Computing Fundamentals", "11.0902")],
    "52": [("Bank Teller and Member Services", "52.0803"), ("Insurance Producer Licensing", "52.1701")],
    "53": [("Property Management Certificate", "52.1501"), ("Real Estate Salesperson Prelicensing", "52.1501")],
    "54": [("Bookkeeping and Payroll", "52.0302"), ("Drafting and CAD Technician", "15.1301"),
           ("Cybersecurity Analyst", "11.1003")],
    "56": [("Building Maintenance Technician", "46.0401"), ("Environmental Technician (HAZWOPER)", "15.0507")],
    "61": [("Instructional Aide Certificate", "13.1501"), ("Tutor and Learning Support", "13.1599")],
    "62": [("Certified Nursing Assistant", "51.3902"), ("Practical Nursing (LPN)", "51.3901"),
           ("Medical Assistant", "51.0801"), ("Phlebotomy Technician", "51.1009")],
    "71": [("Fitness Trainer Certification", "31.0507"), ("Recreation Program Leader", "31.0101")],
    "72": [("Culinary Arts Certificate", "12.0503"), ("Hospitality Management", "52.0901")],
    "81": [("Automotive Service Technician", "47.0604"), ("Cosmetology", "12.0401")]}
PROVIDERS = {"23": ["Tallis Valley Community College", "Ridgeway Technical Institute"],
             "31-33": ["Ridgeway Technical Institute", "Millrace Welding School", "Tallis Valley Community College"],
             "42": ["Tallis Valley Community College"], "44-45": ["Tallis Valley Community College"],
             "48-49": ["Harbin Truck Driving School", "Ridgeway Technical Institute"],
             "51": ["Pioneer IT Training Center", "Tallis Valley Community College"],
             "52": ["Tallis Valley Community College", "Fairmount Career Institute"],
             "53": ["Fairmount Career Institute"], "54": ["Tallis Valley Community College", "Pioneer IT Training Center"],
             "56": ["Ridgeway Technical Institute"], "61": ["Tallis Valley Community College"],
             "62": ["North Star Healthcare Academy", "Tallis Valley Community College"],
             "71": ["Fairmount Career Institute"], "72": ["Tallis Valley Community College"],
             "81": ["Ridgeway Technical Institute", "Cedar Run Beauty Academy"]}


def sector_of(n6):
    return SEC6.get(n6[:2], n6[:2]) if n6[:2] != "92" else "92"


def build(rng):
    # employers: about 900 accounts the exiters work for
    emps, used = [], set()
    for sec, w in JOBS_W.items():
        for i in range(int(round(w * 4.2)) + 3):
            while True:
                nm = "%s %s %s" % (STEMS[int(rng.integers(0, len(STEMS)))], KIND[sec][int(rng.integers(0, len(KIND[sec])))],
                                   SUFFIX[int(rng.integers(0, len(SUFFIX)))])
                if sec == "92":
                    nm = "%s of %s" % (KIND[sec][i % 2], STEMS[int(rng.integers(0, len(STEMS)))])
                if nm not in used:
                    used.add(nm)
                    break
            acct = "%07d" % int(rng.integers(100000, 4790000))
            n6 = NAICS6[sec][int(rng.integers(0, len(NAICS6[sec])))]
            emps.append(dict(acct=acct, name=nm, naics=n6, sec=sec, peo_client=False,
                             county=W.COUNTY_FIPS if rng.random() < .82 else W.COUNTIES[int(rng.integers(0, 23))][1]))
    # PEO clients: some small businesses in every eligible sector lease their staff through a PEO and report under it
    peo_regs = []
    for sec in ELIG:
        ks = [e for e in emps if e["sec"] == sec]
        n = 2 + int(rng.integers(0, 3))
        for e in rng.choice(len(ks), size=min(n, len(ks)), replace=False):
            ks[int(e)]["peo_client"] = True
    unit = {}
    for e in emps:
        if e["peo_client"]:
            p = PEOS[int(rng.integers(0, len(PEOS)))]
            unit[p[1]] = unit.get(p[1], 0) + 1
            e["peo"], e["unit"] = p[1], "%03d" % (unit[p[1]] + int(rng.integers(0, 3)) * 0)
            start = dt.date(2019, 1, 1) + dt.timedelta(int(rng.integers(0, 1900)))
            peo_regs.append(dict(peo_account=p[1], peo_name=p[0], rpt_unit=e["unit"], client_account=e["acct"],
                                 client_name=e["name"], client_fein="%02d-%07d" % (int(rng.integers(10, 99)),
                                                                                   int(rng.integers(0, 9999999))),
                                 effective=start, ended=None))
    # registrations that ended before the window (former clients) and other PEOs' clients elsewhere in the state
    for i in range(38):
        p = PEOS[i % 4]
        unit[p[1]] = unit.get(p[1], 0) + 1
        st = dt.date(2016, 1, 1) + dt.timedelta(int(rng.integers(0, 2200)))
        peo_regs.append(dict(peo_account=p[1], peo_name=p[0], rpt_unit="%03d" % unit[p[1]],
                             client_account="%07d" % int(rng.integers(100000, 4790000)),
                             client_name="%s %s %s" % (STEMS[i % len(STEMS)], ["Dental", "Builders", "Supply",
                                                                                "Consulting"][i % 4], "LLC"),
                             client_fein="%02d-%07d" % (int(rng.integers(10, 99)), int(rng.integers(0, 9999999))),
                             effective=st, ended=(st + dt.timedelta(int(rng.integers(200, 900))))
                             if i % 3 else None))
    for p in PEOS:
        emps.append(dict(acct=p[1], name=p[0], naics="561330", sec="56", peo_client=False, county="52005", peo_self=True))
    byacct = {e["acct"]: e for e in emps}

    # exits: one row per program enrollment
    persons, exits = [], []
    for i in range(1084):
        pid = "TV%07d" % (3100000 + i * 7 + int(rng.integers(0, 7)))
        d = dt.date(2025, 1, 2) + dt.timedelta(int(rng.integers(0, 363)))
        progs = [["ADULT", "DW", "YOUTH"][int(rng.choice(3, p=[.5, .32, .18]))]]
        if progs[0] != "YOUTH" and rng.random() < .09:
            progs.append("DW" if progs[0] == "ADULT" else "ADULT")
        dates = [d]
        if rng.random() < .04 and d < dt.date(2025, 6, 1):
            dates.append(d + dt.timedelta(int(rng.integers(120, 200))))
        for k, dd in enumerate(dates):
            for pg in progs:
                exits.append(dict(enroll="E%06d" % (len(exits) * 3 + 17 + int(rng.integers(0, 3))), pid=pid,
                                  program=pg, exit_date=dd))
        persons.append(dict(pid=pid, last=max(dates)))

    def q_after(d, n):
        y, q = d.year, (d.month - 1) // 3 + 1
        q += n
        while q > 4:
            q -= 4
            y += 1
        return y, q

    window = [(2025, 3), (2025, 4), (2026, 1), (2026, 2)]
    secs = list(JOBS_W)
    wts = np.array([JOBS_W[s] for s in secs], float)
    wts /= wts.sum()
    wage_rows = []
    for p in persons:
        if rng.random() > .71:
            p["employer"] = None
        else:
            sec = secs[int(rng.choice(len(secs), p=wts))]
            cands = [e for e in emps if e["sec"] == sec and not e.get("peo_self")]
            if sec in ELIG and rng.random() < .16:
                cands = [e for e in cands if e["peo_client"]] or cands
            p["employer"] = cands[int(rng.integers(0, len(cands)))]
        target = q_after(p["last"], 2)
        for (y, q) in window:
            if (y, q) <= q_after(p["last"], 0):
                continue
            jobs = []
            if p["employer"] is not None and (rng.random() < .93 or (y, q) == target):
                jobs.append((p["employer"], float(rng.uniform(2900, 11800))))
            if p["employer"] is not None and rng.random() < .14:
                sec2 = secs[int(rng.choice(len(secs), p=wts))]
                c2 = [e for e in emps if e["sec"] == sec2 and not e.get("peo_self")]
                e2 = c2[int(rng.integers(0, len(c2)))]
                jobs.append((e2, float(rng.uniform(300, 2600))))
            if p["employer"] is None and rng.random() < .1:
                c2 = [e for e in emps if not e.get("peo_self")]
                jobs.append((c2[int(rng.integers(0, len(c2)))], float(rng.uniform(150, 2400))))
            for e, w in jobs:
                if e.get("peo_client"):
                    acct, u = e["peo"], e["unit"]
                else:
                    acct, u = e["acct"], "000"
                wage_rows.append(dict(pid=p["pid"], acct=acct, unit=u, y=y, q=q, wages=round(w, 2)))

    # duplicate registrations: a returning customer registered again under a new participant ID; both IDs carry
    # enrollments and the state's match return answers each ID it was sent with the same wage records
    r2 = np.random.default_rng(W.SEED + 2000)
    for p in persons:
        p["dob"] = dt.date(1958, 1, 1) + dt.timedelta(int(r2.integers(0, 16000)))
        p["zip"] = "%05d" % int(r2.choice([52101, 52103, 52104, 52107, 52110, 52112, 52115, 52118, 52120]))
    by = {}
    for p in persons:
        if p["employer"] is not None and p["employer"]["sec"] in ELIG:
            by.setdefault(p["employer"]["sec"], []).append(p)
    dups = []
    for sec in ELIG:
        ps = by.get(sec, [])
        for k in r2.choice(len(ps), size=min(2, len(ps)), replace=False):
            dups.append(ps[int(k)])
    rest = [p for p in persons if p not in dups]
    for k in r2.choice(len(rest), size=14, replace=False):
        dups.append(rest[int(k)])
    first_prog = {}
    for e in exits:
        first_prog.setdefault(e["pid"], e["program"])
    used_p = {p["pid"] for p in persons}
    used_e = {e["enroll"] for e in exits}
    top_p = max(int(p["pid"][2:]) for p in persons)
    top_e = max(int(e["enroll"][1:]) for e in exits)
    for i, p in enumerate(dups):
        while True:
            pid2 = "TV%07d" % int(r2.integers(3100000, top_p))
            if pid2 not in used_p:
                used_p.add(pid2)
                break
        while True:
            en2 = "E%06d" % int(r2.integers(17, top_e))
            if en2 not in used_e:
                used_e.add(en2)
                break
        p["dup"] = pid2
        exits.append(dict(enroll=en2, pid=pid2,
                          program=first_prog[p["pid"]], exit_date=p["last"], dob=p["dob"], zip=p["zip"]))
        for r in [r for r in wage_rows if r["pid"] == p["pid"]]:
            wage_rows.append(dict(r, pid=pid2))
    # different people who share a birth date and home ZIP code
    emp_p = [p for p in persons if p["employer"] is not None and "dup" not in p]
    for k in range(5):
        a_, b_ = emp_p[int(r2.integers(0, len(emp_p)))], emp_p[int(r2.integers(0, len(emp_p)))]
        if a_ is not b_:
            b_["dob"], b_["zip"] = a_["dob"], a_["zip"]
    for e in exits:
        if "dob" not in e:
            pp = next(p for p in persons if p["pid"] == e["pid"])
            e["dob"], e["zip"] = pp["dob"], pp["zip"]

    # training: the provider list and the individual training accounts
    programs = []
    pid_n = 4100
    for sec in ELIG:
        for j in range(2 + int(rng.integers(0, 3))):
            pid_n += int(rng.integers(3, 40))
            cat = CATALOG[sec][j % len(CATALOG[sec])]
            prov = PROVIDERS[sec][j % len(PROVIDERS[sec])]
            programs.append(dict(program_id="P%05d" % pid_n, sec=sec, j=j, name=cat[0], cip=cat[1], provider=prov,
                                 approved=dt.date(2021, 7, 1) + dt.timedelta(int(rng.integers(0, 1200)))))
    vouchers, ledger, register = [], [], []
    ex_pids = [p["pid"] for p in persons]
    for prog in programs:
        for v in range(3 + int(rng.integers(0, 6))):
            amt = float(rng.choice([1850, 2400, 3200, 3975, 4500, 5200, 6000, 7400])) + float(rng.integers(0, 40)) * 25 \
                + float(rng.choice([0, 0, 0, .35, .6, .85, 1.2, 4.15]))
            n = int(rng.choice([1, 2, 3, 4], p=[.25, .35, .3, .1]))
            if v == 0:
                n = max(n, 2)
            start = dt.date(2024, 9, 1) + dt.timedelta(int(rng.integers(0, 420)))
            vid = "V%02d-%05d" % (start.year % 100, len(vouchers) * 4 + 1031 + int(rng.integers(0, 4)))
            vouchers.append(dict(vid=vid, pid=ex_pids[int(rng.integers(0, len(ex_pids)))], prog=prog["program_id"],
                                 amount=amt, n=n))
            parts = [round(amt / n, 2)] * (n - 1)
            parts.append(round(amt - sum(parts), 2))
            for i in range(n):
                due = start + dt.timedelta(int(i * rng.integers(55, 100)))
                ledger.append(dict(vid=vid, pid=vouchers[-1]["pid"], prog=prog["program_id"], inst=i + 1, n=n,
                                   amount=amt, part=parts[i], due=due, check=None, provider=prog["provider"]))
    # the fiscal agent pays providers in a run every other Thursday: one check per provider per run covers every
    # installment that fell due since the previous run
    runs = []
    d = dt.date(2024, 9, 5)
    while d <= dt.date(2026, 6, 30):
        runs.append(d)
        d += dt.timedelta(14)
    chk = 208400
    for i, run in enumerate(runs):
        prev = runs[i - 1] if i else dt.date(2024, 1, 1)
        due = [l for l in ledger if prev < l["due"] <= run]
        for prov in sorted({l["provider"] for l in due}):
            lines = [l for l in due if l["provider"] == prov]
            chk += int(rng.integers(1, 6))
            issue = run
            amount = round(sum(l["part"] for l in lines), 2)
            if rng.random() < .04:
                register.append(dict(check=str(chk), payee=prov, issue=issue, amount=amount, status="VOID",
                                     void=issue + dt.timedelta(int(rng.integers(4, 20)))))
                chk += int(rng.integers(1, 6))
                issue = runs[min(i + 1, len(runs) - 1)] + dt.timedelta(1)
            register.append(dict(check=str(chk), payee=prov, issue=issue, amount=amount, status="ISSUED", void=None))
            for l in lines:
                l["check"] = str(chk)
    # program IDs reissued: a withdrawn program's ID goes to the next program the state approves; the withdrawn
    # record keeps its listing under a new archive ID, and the ledger line carries the program's title
    r3 = np.random.default_rng(W.SEED + 3000)
    for p in programs:
        p["status"], p["withdrawn"] = "Active", None
    for l in ledger:
        l["desc"] = "ITA tuition - " + next(p["name"] for p in programs if p["program_id"] == l["prog"])
    paid25 = {}
    for l in ledger:
        if l["check"] and any(r["check"] == l["check"] and r["issue"].year == 2025 and r["status"] != "VOID"
                              for r in register):
            paid25[l["prog"]] = paid25.get(l["prog"], 0) + l["part"]
    arch = 9100
    new_programs = []
    order = list(ELIG)
    while True:
        perm = [ELIG[int(k)] for k in r3.permutation(len(ELIG))]
        if all(a != b for a, b in zip(order, perm)):
            break
    for i, sec in enumerate(ELIG):
        nxt = perm[i]
        cands = sorted([p for p in programs if p["sec"] == sec and p["program_id"] in paid25],
                       key=lambda p: paid25[p["program_id"]])
        old = cands[0]
        old_id = old["program_id"]
        arch += int(r3.integers(3, 30))
        old["program_id"] = "P%05d" % arch
        old["status"], old["withdrawn"] = "Withdrawn", dt.date(2025, 12, 1) + dt.timedelta(int(r3.integers(5, 60)))
        cat = CATALOG[nxt][(len(CATALOG[nxt]) - 1 + i) % len(CATALOG[nxt])]
        new_programs.append(dict(program_id=old_id, sec=nxt, j=9, name=cat[0], cip=cat[1],
                                 provider=old["provider"],
                                 approved=old["withdrawn"] + dt.timedelta(int(r3.integers(20, 90))),
                                 status="Active", withdrawn=None))
    programs += new_programs
    # the list carries each program's latest annual re-approval (subsequent eligibility), not its first approval
    for p in programs:
        if p["status"] == "Active":
            p["approved"] = dt.date(2025, 7, 1) + dt.timedelta(int(r3.integers(0, 340)))
        else:
            p["approved"] = dt.date(2024, 7, 1) + dt.timedelta(int(r3.integers(0, 330)))

    return dict(emps=emps, byacct=byacct, peo_regs=peo_regs, exits=exits, persons=persons, wage_rows=wage_rows,
                programs=programs, vouchers=vouchers, ledger=ledger, register=register)
