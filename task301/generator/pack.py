"""Writes the pack under target/ the way each producing system exports it: the statistics institute's survey files
(semicolon-separated, decimal commas, Windows line ends), the fieldwork contractor's case export, the benefits
system's register extract (pipe-separated, with the pre-migration rows in the old system's date formats), the
quarterly incident workbook, the territorial code list, the documents and two files the decision does not need."""
import datetime as dt
import os

import numpy as np

import docs
import io_util as IO
import params as P
import register as RG

FILES = {
    "households": "ecvv2026_households.csv",
    "persons": "ecvv2026_persons.csv",
    "fieldwork": "ecvv2026_fieldwork_cases.csv",
    "register": "cfv_register_extract_20261102.csv",
    "incidents": "cfv_incidents_2025.xlsx",
    "codes": "territorial_codes.csv",
    "guidance": "appraisal_guidance_child_poverty_2027.docx",
    "proposals": "child_poverty_proposals_2027.pdf",
    "rules": "complemento_familiar_rules_2026.pdf",
    "coverage": "complemento_familiar_coverage_2025.pdf",
    "results": "ecvv2026_main_results.pdf",
    "wave2025": "ecvv2025_households.csv",
    "municipal": "municipal_poverty_estimates_2024.xlsx",
}
DISTRACTORS = ["wave2025", "municipal"]
STAMP = P.STAMP
MIGRATION = dt.date(2024, 3, 1)

TENURE = {1: "owned outright", 2: "owned with mortgage", 3: "rented at market price", 4: "rented below market price",
          5: "provided free"}
REL = {"R": "reference person", "P": "spouse or partner", "C": "son or daughter", "G": "father or mother",
       "O": "other relative"}
OUTCOME = {11: "complete interview", 12: "partial interview", 21: "refusal", 22: "no contact",
           23: "unable to interview", 31: "empty dwelling", 32: "not a dwelling", 33: "address not found"}
TYPE = {"I": "INITIAL", "R": "RENEWAL", "T": "CHANGE OF CLAIMANT", "V": "REVOCATION"}
DECISION = {"C": "GRANTED", "D": "REFUSED", "A": "WITHDRAWN", "P": "PENDING", "X": "EXTINGUISHED", "V": "REVOKED"}
INCIDENT = {"SUS": "Payment suspended (documents outstanding)", "LEV": "Suspension lifted",
            "EXT": "Award extinguished", "NAC": "Birth", "MAY": "Child reached 18", "DOM": "Change of address"}


def ids(rng, n, lo, hi):
    out = set()
    while len(out) < n:
        out.update(int(x) for x in rng.integers(lo, hi, size=n))
    return sorted(rng.choice(sorted(out), size=n, replace=False).tolist())


def household_rows(W, rng):
    hh = W["hh"]
    urb = {}
    for m in W["munis"]:
        urb[m["code"]] = 1 if m["share"] > 0.12 else (2 if m["share"] > 0.03 else 3)
    hid = ids(rng, len(hh), 260100000, 260999999)
    order = rng.permutation(len(hh))
    hrows, prows = [], []
    for k, i in enumerate(order):
        h = hh[int(i)]
        h["hid"] = hid[k]
        disp, cfv = h["disp25"], h["cfv_recv25"]
        rest = round(disp - cfv, 2)
        pens = unemp = mini = other = 0.0
        if h["type"] in ("pens1", "pens2"):
            pens = round(rest * float(rng.uniform(0.86, 0.99)), 2)
            other = 0.0
        else:
            if h["inc_eq25"] < 7500 and rng.random() < 0.62:
                mini = round(rest * float(rng.uniform(0.35, 0.80)), 2)
            if rng.random() < 0.16:
                unemp = round(min(rest - mini, rest * float(rng.uniform(0.10, 0.45))), 2)
            if h["type"] == "multi_kids":
                pens = round((rest - mini - unemp) * float(rng.uniform(0.15, 0.35)), 2)
        other = round(max(0.0, (rest - pens - unemp - mini) * float(rng.uniform(0.0, 0.05))), 2)
        earn = round(rest - pens - unemp - mini - other, 2)
        h["components"] = (earn, pens, unemp, mini, other)
        h["urb"] = urb[h["dwelling"]["muni"]]
        h["tenure"] = (3 if rng.random() < 0.78 else 4) if h["renting"] else int(rng.choice([1, 2, 5], p=[.47, .48, .05]))
        hrows.append([h["hid"], h["prov"], h["urb"], IO.comma(h["w"], 4), int(rng.integers(2, 7)), TENURE[h["tenure"]],
                      IO.comma(disp), IO.comma(earn), IO.comma(pens), IO.comma(unemp), IO.comma(mini), IO.comma(cfv),
                      IO.comma(other), 1 if h["cfv_now"] else 0, 1 if h["filed"] else 0,
                      IO.comma(h["gross25"]) if h["filed"] else ""])
        # members
        lines = []
        for j, (age, role) in enumerate(h["members"], start=1):
            lines.append((j, age, role))
        sexes = {}
        for j, age, role in lines:
            if role == "R":
                sexes[j] = "M" if rng.random() < 0.52 else "H"
            elif role == "P":
                sexes[j] = "H" if sexes.get(1) == "M" else "M"
            else:
                sexes[j] = "M" if rng.random() < 0.49 else "H"
        father = mother = ""
        for j, age, role in lines:
            if role in ("R", "P"):
                if sexes[j] == "H":
                    father = j
                else:
                    mother = j
        lone = h["type"] == "lone"
        earners = [j for j, a, r in lines if 18 <= a <= 66]
        if not earners:
            earners = [j for j, a, r in lines if a >= 18]
        wts = np.array([1.0 if r in ("R", "P") else 0.4 for j, a, r in lines if j in earners])
        wts = wts / wts.sum()
        amounts = {j: [0.0, 0.0, 0.0] for j, a, r in lines}
        acc = 0.0
        for q, (j, s) in enumerate(zip(earners, wts)):
            v = round(earn * float(s), 2) if q < len(earners) - 1 else round(earn - acc, 2)
            acc += v
            amounts[j][0] = v
        if unemp > 0:
            amounts[earners[int(rng.integers(0, len(earners)))]][2] = unemp
        olds = [j for j, a, r in lines if a >= 66] or [earners[0]]
        accp = 0.0
        for q, j in enumerate(olds):
            v = round(pens / len(olds), 2) if q < len(olds) - 1 else round(pens - accp, 2)
            accp += v
            amounts[j][1] = v
        for j, age, role in lines:
            if age < 16:
                act = "not applicable (under 16)"
            elif role == "C" and age < 25 and rng.random() < 0.7:
                act = "student"
            elif age >= 66:
                act = "retired"
            elif amounts[j][2] > 0:
                act = "unemployed"
            elif amounts[j][0] > 0:
                act = "employed" if rng.random() < 0.88 else "self-employed"
            else:
                act = "other inactive"
            f_line = father if role == "C" and father != j else ""
            m_line = mother if role == "C" and mother != j else ""
            if lone and role == "C":
                f_line = father if father else ""
            if role != "C":
                f_line = m_line = ""
            am = amounts[j]
            prows.append(["%d%02d" % (h["hid"], j), h["hid"], j, P.AGE_BASE_YEAR - age, sexes[j], REL[role],
                          f_line, m_line, act, IO.comma(am[0]), IO.comma(am[1]), IO.comma(am[2])])
    hrows.sort(key=lambda r: r[0])
    prows.sort(key=lambda r: (r[1], r[2]))
    return hrows, prows


def write_survey(W, rng, target):
    hrows, prows = household_rows(W, rng)
    IO.write_csv(os.path.join(target, FILES["households"]),
                 ["household_id", "province", "urbanisation", "household_weight", "interview_month", "tenure",
                  "disposable_income_2025", "net_earnings_2025", "net_pensions_2025", "unemployment_benefits_2025",
                  "minimum_income_2025", "complemento_familiar_2025", "other_benefits_2025", "complemento_familiar_now",
                  "irpf_return_2025", "irpf_gross_income_2025"], hrows, delimiter=";")
    IO.write_csv(os.path.join(target, FILES["persons"]),
                 ["person_id", "household_id", "line", "birth_year", "sex", "relationship", "father_line",
                  "mother_line", "activity", "net_earnings_2025", "net_pension_2025", "unemployment_benefit_2025"],
                 prows, delimiter=";")
    return len(hrows), len(prows)


def write_fieldwork(W, rng, target):
    cases = W["cases"]
    nums = ids(rng, len(cases), 100000, 999999)
    order = sorted(range(len(cases)), key=lambda i: (cases[i]["closed"], cases[i]["ref"], cases[i]["issue"]))
    case_id = {id(cases[i]): "C26-%06d" % nums[k] for k, i in enumerate(order)}
    first_of = {id(c["dwelling"]): case_id[id(c)] for c in cases if c["issue"] == 1}
    rows = []
    for k, i in enumerate(order):
        c = cases[i]
        rows.append([case_id[id(c)], c["ref"], c["dwelling"]["office"], c["interviewer"], c["issue"],
                     first_of[id(c["dwelling"])] if c["issue"] > 1 else "", OUTCOME[c["outcome"]], c["visits"],
                     c["closed"].strftime("%d/%m/%Y")])
    IO.write_csv(os.path.join(target, FILES["fieldwork"]),
                 ["case", "dwelling", "office", "interviewer", "issue", "reissue_of", "result", "visits", "closed"],
                 rows)
    return len(rows)


def ym(t, legacy):
    y, m = RG.ym_of(t)
    return ("%02d/%d" % (m, y)) if legacy else ("%d-%02d" % (y, m))


def write_register(R, W, rng, target):
    munis = {m["code"]: m for m in W["munis"]}
    office = {"VAL": "81", "CUE": "82", "SIE": "83"}
    fids = sorted(set(a["fid"] for a in R["awards"]))
    fnum = dict(zip(fids, ids(rng, len(fids), 1000000, 9999999)))
    R["fnum"] = fnum
    rows = []
    for a in sorted(R["awards"], key=lambda a: (a["ex"], a["dec"] or dt.date(2099, 1, 1))):
        legacy = a["claim"] < MIGRATION and (a["dec"] is None or a["dec"] < MIGRATION)
        dfmt = (lambda d: d.strftime("%d/%m/%Y")) if legacy else (lambda d: d.isoformat())
        inc = "" if a.get("inc") is None else (IO.comma(a["inc"]) if legacy else "%.2f" % a["inc"])
        amt = ""
        if a["res"] == "C" and a["first"] is not None:
            amt = ("%.2f" % (a["rate"] * a["kids"])).replace(".", "," if legacy else ".")
        rows.append([a["ex"], "UF%07d" % fnum[a["fid"]], TYPE[a["tipo"]], dfmt(a["claim"]),
                     dfmt(a["dec"]) if a["dec"] is not None else "", "REVOKED" if a.get("revoked") else DECISION[a["res"]],
                     a["ejercicio"], inc, a["kids"],
                     a["muni"], office[munis[a["muni"]]["office"]],
                     ym(a["first"], legacy) if a["first"] is not None else "",
                     ym(a["last"], legacy) if a["last"] is not None else "", amt])
    IO.write_csv(os.path.join(target, FILES["register"]),
                 ["case_number", "family_number", "claim_type", "claim_date", "decision_date", "decision", "tax_year",
                  "computable_income_per_eq_adult", "children", "municipality", "province", "first_month_paid",
                  "last_month_paid", "monthly_amount"], rows, delimiter="|")
    return len(rows)


def write_incidents(R, target):
    fnum = R["fnum"]
    q_names = {1: "first", 2: "second", 3: "third", 4: "fourth"}
    sheets = []
    for q in range(1, 5):
        rows = []
        for r in R["incidents"]:
            if (r["date"].month - 1) // 3 + 1 == q and r["date"].year == 2025:
                rows.append([r["date"], "UF%07d" % fnum[r["fid"]], r["ex"], INCIDENT[r["type"]], r["dato"]])
        sheets.append(("Q%d 2025" % q, ["Date", "Family", "Case", "Incident", "Detail"], rows,
                       ["Complemento Familiar: incidents recorded in the %s quarter of 2025" % q_names[q], ""]))
    IO.write_xlsx(os.path.join(target, FILES["incidents"]), sheets,
                  ("Diego Hervia", "Diego Hervia", "2026-01-12T08:00:00Z", "2026-11-02T07:40:00Z",
                   "Complemento Familiar incidents 2025", docs.DEPT), widths={"Incident": 44, "Date": 12})
    return sum(len(s[2]) for s in sheets)


def write_codes(W, target):
    rows = sorted([[m["code"], m["name"], m["prov"], dict(P.PROVINCES)[m["prov"]]] for m in W["munis"]])
    IO.write_csv(os.path.join(target, FILES["codes"]), ["municipality_code", "municipality", "province_code", "province"],
                 rows)
    return len(rows)


def write_wave2025(W, rng, target):
    """The 2025 wave (2024 incomes) in the old layout, released a year earlier."""
    rows = []
    hh = W["hh"]
    n = int(len(hh) * 0.965)
    pick = rng.choice(len(hh), size=n, replace=False)
    hid = ids(rng, n, 250100000, 250999999)
    for k, i in enumerate(sorted(pick.tolist())):
        h = hh[int(i)]
        disp = h["disp25"] * float(np.exp(rng.normal(-0.035, 0.09)))
        fam = h["cfv_recv25"] * float(rng.uniform(0.85, 1.0)) if h["cfv_recv25"] else 0.0
        rows.append([hid[k], "ES4X", h["prov"], IO.comma(h["w"] * float(np.exp(rng.normal(0, 0.05))), 4),
                     int(rng.integers(2, 7)), {1: 1, 2: 2, 3: 3, 4: 4, 5: 5}[h.get("tenure", 1)], IO.comma(disp),
                     IO.comma(fam), len(h["ages"])])
    rows.sort(key=lambda r: r[0])
    IO.write_csv(os.path.join(target, FILES["wave2025"]),
                 ["DB030", "DB040", "PROV", "DB090", "HB050", "HH021", "HY020", "HY050N", "HX040"], rows, delimiter=";")
    return len(rows)


def write_municipal(W, rng, target):
    rows = []
    for m in sorted(W["munis"], key=lambda m: m["code"]):
        pop = int(round(P.TARGET_PERSONS * dict(zip([p for p, _ in P.PROVINCES], P.PROV_SHARE))[m["prov"]] * m["share"]))
        rate = float(np.clip(rng.normal(19.5, 4.2) + {"81": -2.0, "82": 0.8, "83": 2.4}[m["prov"]], 8, 36))
        cv = float(np.clip(9.0 + 160000.0 / max(pop, 800) ** 0.85, 6, 38))
        lo, hi = rate * (1 - 1.96 * cv / 100), rate * (1 + 1.96 * cv / 100)
        rows.append([m["code"], m["name"], pop, round(rate, 1), round(cv, 1), round(lo, 1), round(hi, 1)])
    IO.write_xlsx(os.path.join(target, FILES["municipal"]),
                  [("2024", ["Municipality code", "Municipality", "Population 1 Jan 2024", "At-risk-of-poverty rate (%)",
                             "Coefficient of variation (%)", "95% interval, lower", "95% interval, upper"], rows,
                    ["Small-area estimates of the at-risk-of-poverty rate, 2024 (experimental statistics)",
                     "Instituto de Estadística de Valmesura. Model-based estimates; not comparable with survey "
                     "direct estimates.", ""])],
                  ("IEV", "IEV", "2025-12-10T09:00:00Z", "2025-12-10T09:00:00Z",
                   "Municipal poverty estimates 2024", docs.IEV))
    return len(rows)


def costs(W):
    line = W["line"]
    out = {"A": 0.0, "B": 0.0, "C": 0.0, "D": 0.0, "E": 0.0}
    for h in W["hh"]:
        if not h["kids"]:
            continue
        k, w = h["kids"], h["w"]
        if h["filed"] and h["gross25"] < P.A_INCOME_LIMIT:
            out["A"] += w * 12 * P.A_RATE * k
        if h["comp_eq"] < line:
            out["B"] += w * 12 * P.B_RATE * k
        if P.CFV_LIMIT <= h["comp_eq"] < P.C_LIMIT and not h["cfv_now"]:
            out["C"] += w * 12 * P.CFV_RATE_2027 * k
        if h["renting"] and h["comp_eq"] < line:
            out["D"] += w * 12 * P.D_RATE * k
        if h["cfv_now"]:
            out["E"] += w * 12 * P.E_RATE * k
    return {k: v / 1e6 for k, v in out.items()}


def coverage_figures(W, R):
    tD = RG.t_of(2025, 12)
    paid_dec = set(a["fid"] for a in R["awards"] if a["res"] == "C" and a["first"] is not None and a["first"] <= tD
                   and (a["last"] is None or a["last"] >= tD) and a["dec"] <= RG.YEAR_END)
    entitled = sum(h["w"] for h in W["hh"] if h["kids"] and h["assessed"] < P.CFV_LIMIT)
    take_up = 100.0 * len(paid_dec) / entitled
    monthly = []
    kidsmix = {1: [], 2: [], 3: []}
    for t in range(RG.T25A, RG.T25B + 1):
        fams = {}
        for a in R["awards"]:
            if a["res"] == "C" and a["first"] is not None and a["first"] <= t and (a["last"] is None or a["last"] >= t):
                fams[a["fid"]] = a["kids"]
        monthly.append(len(fams))
        for k in (1, 2, 3):
            kidsmix[k].append(sum(1 for v in fams.values() if (v == k if k < 3 else v >= 3)))
    tot = float(sum(monthly))
    shares = [("One", 100.0 * sum(kidsmix[1]) / tot), ("Two", 100.0 * sum(kidsmix[2]) / tot),
              ("Three or more", 100.0 * sum(kidsmix[3]) / tot)]
    return take_up, shares


def results_figures(W):
    line_med = W["median25"]
    thr = 0.6 * line_med
    rates = {}
    groups = [("Comunidad de Valmesura", None)] + [(n, p) for p, n in P.PROVINCES]
    for name, pc in groups:
        acc = {"all": [0.0, 0.0], "c": [0.0, 0.0], "w": [0.0, 0.0], "o": [0.0, 0.0]}
        for h in W["hh"]:
            if pc and h["prov"] != pc:
                continue
            poor = h["disp25"] / h["eq"] < thr
            for a in h["ages"]:
                g = "c" if a <= 17 else ("w" if a <= 64 else "o")
                for key in ("all", g):
                    acc[key][0] += h["w"] * poor
                    acc[key][1] += h["w"]
        rates[name] = tuple(100.0 * acc[k][0] / acc[k][1] for k in ("all", "c", "w", "o"))
    return line_med, thr, rates


def build_all(W, R, target, seed):
    rng = np.random.default_rng(seed + 501)
    counts = {}
    counts["households"], counts["persons"] = write_survey(W, rng, target)
    counts["fieldwork"] = write_fieldwork(W, rng, target)
    counts["register"] = write_register(R, W, rng, target)
    counts["incidents"] = write_incidents(R, target)
    counts["codes"] = write_codes(W, target)
    counts["wave2025"] = write_wave2025(W, rng, target)
    counts["municipal"] = write_municipal(W, rng, target)
    docs.guidance(os.path.join(target, FILES["guidance"]), W["line"])
    docs.proposals(os.path.join(target, FILES["proposals"]), W["line"], costs(W))
    docs.rules(os.path.join(target, FILES["rules"]))
    take_up, shares = coverage_figures(W, R)
    W["take_up_published"] = round(take_up, 1)
    docs.coverage(os.path.join(target, FILES["coverage"]), take_up, shares)
    med, thr, rates = results_figures(W)
    docs.results(os.path.join(target, FILES["results"]), med, thr, rates)
    stamp = STAMP.timestamp()
    for fn in os.listdir(target):
        os.utime(os.path.join(target, fn), (stamp, stamp))
    return counts
