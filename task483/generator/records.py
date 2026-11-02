"""task483 records: the clean truth's consultations turned into the rows each producing system writes.

Every issue is one the practice's clinical system records (issuing organisation, registered practice, product as
prescribed, quantity, dosage, acute or repeat, the problem it was linked to); every specimen is one the pathology
network's laboratory registered (requesting location, registered practice, specimen type, collection, receipt and
authorisation, the culture result and each organism's susceptibilities). Children, men, older women, pregnant women,
the antenatal clinic's screening urines and the hospital's own requests are drawn here too, each from its own stream,
so the women's core simulation in world.py is untouched by them.
"""
import datetime as dt
from collections import defaultdict

import numpy as np

import world as W

D = dt.date
TD = dt.timedelta

# products as the two clinical systems name them (EMIS, SystmOne); quantities in tablets, capsules, sachets or ml
PRODUCTS = {
    "NIT": [("Nitrofurantoin 100mg modified-release capsules", "Nitrofurantoin 100mg modified-release capsules", 0.70, "MR"),
            ("Macrobid 100mg modified-release capsules", "Macrobid 100mg modified-release capsules (Advanz Pharma)", 0.12, "MR"),
            ("Nitrofurantoin 50mg tablets", "Nitrofurantoin 50mg tablets", 0.12, "IR"),
            ("Nitrofurantoin 50mg capsules", "Nitrofurantoin 50mg capsules", 0.06, "IR")],
    "TMP": [("Trimethoprim 200mg tablets", "Trimethoprim 200mg tablets", 1.0, "")],
    "MEC": [("Pivmecillinam 200mg tablets", "Pivmecillinam 200mg tablets", 0.82, ""),
            ("Selexid 200mg tablets", "Selexid 200mg tablets (Karo Pharma)", 0.18, "")],
    "CEX": [("Cefalexin 500mg capsules", "Cefalexin 500mg capsules", 0.88, ""),
            ("Cefalexin 500mg tablets", "Cefalexin 500mg tablets", 0.12, "")],
    "AMC": [("Co-amoxiclav 500mg/125mg tablets", "Co-amoxiclav 500mg/125mg tablets", 1.0, "")],
    "FOS": [("Fosfomycin 3g granules sachets", "Fosfomycin 3g granules sachets sugar free", 0.74, ""),
            ("Monuril 3g granules sachets", "Monuril 3g granules sachets (Zambon)", 0.26, "")],
    "AMX": [("Amoxicillin 500mg capsules", "Amoxicillin 500mg capsules", 1.0, "")],
    "CIP": [("Ciprofloxacin 500mg tablets", "Ciprofloxacin 500mg tablets", 1.0, "")],
}
CHILD_PRODUCTS = {
    "TMP": ("Trimethoprim 50mg/5ml oral suspension sugar free", 100),
    "NIT": ("Nitrofurantoin 25mg/5ml oral suspension", 300),
    "CEX": ("Cefalexin 250mg/5ml oral suspension", 100),
    "AMC": ("Co-amoxiclav 250mg/62mg/5ml oral suspension", 100),
}
# per-day units, and dosage texts in the styles the practices type
DAILY = {"NIT/MR": 2, "NIT/IR": 4, "TMP": 2, "CEX": 2, "AMC": 3, "AMX": 3, "FOS": 1, "CIP": 2}
DOSE_TEXT = {
    "NIT/MR": ["ONE capsule twice a day", "1 BD", "Take one capsule twice daily", "one twice a day with food"],
    "NIT/IR": ["ONE tablet four times a day", "1 QDS", "Take one four times daily with food"],
    "TMP": ["ONE tablet twice a day", "1 BD", "Take one tablet twice daily"],
    "MEC": ["TWO tablets immediately then ONE three times a day", "2 stat then 1 TDS",
            "Take two straight away then one three times daily"],
    "CEX": ["ONE capsule twice a day", "1 BD", "Take one twice daily"],
    "AMC": ["ONE tablet three times a day", "1 TDS", "Take one tablet three times daily"],
    "AMX": ["ONE capsule three times a day", "1 TDS", "Take one three times daily"],
    "FOS": ["Dissolve ONE sachet in water and take as a single dose", "one sachet stat", "ONE sachet at night"],
    "CIP": ["ONE tablet twice a day", "1 BD"],
}
PROBLEMS_W = [("Urinary tract infection", 0.38), ("Cystitis", 0.24), ("Lower urinary tract infection", 0.16),
              ("Acute cystitis", 0.13), ("Recurrent urinary tract infection", 0.09)]
PROBLEM_PREG = "Urinary tract infection in pregnancy"
PROBLEM_ASB = "Asymptomatic bacteriuria in pregnancy"

EMIS = {pr["code"]: pr["system"] for pr in W.practices()}
EMIS[W.HUB] = "EMIS"


def pseudo(pid):
    h = 2166136261
    for ch in "HHF-ICB-LINK-%d" % pid:
        h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    g = 2166136261
    for ch in "%d-LINK-HHF" % pid:
        g = ((g ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    return ("%08X%04X" % (h, g & 0xFFFF))[:11]


def registered(code, day):
    """The practice a patient of `code` is registered with on `day` (Stanbridge Road merged into Hollin Lane)."""
    if code == W.MERGE_FROM and day >= W.MERGE_DAY:
        return W.MERGE_INTO
    return code


def _pick(rng, options):
    return options[int(rng.integers(0, len(options)))]


def product_row(rng, drug, system, days, child_ml=None):
    """(product, quantity, dosage) for a course of `days` days."""
    if child_ml is not None:
        name, vol = CHILD_PRODUCTS[drug]
        dose_ml = child_ml
        per_day = 2 if drug in ("TMP", "CEX") else (4 if drug == "NIT" else 3)
        qty = vol if dose_ml * per_day * days <= vol else 2 * vol
        txt = "%sml %s" % (("%g" % dose_ml), {2: "twice a day", 3: "three times a day", 4: "four times a day"}[per_day])
        return name, qty, txt
    opts = PRODUCTS[drug]
    k = int(rng.choice(len(opts), p=np.array([o[2] for o in opts]) / sum(o[2] for o in opts)))
    emis_name, s1_name, _, form = opts[k]
    name = emis_name if system == "EMIS" else s1_name
    key = "NIT/" + form if drug == "NIT" else drug
    if drug == "MEC":
        qty = 2 + 3 * days - 1 if days > 1 else 2
        qty = 10 if days == 3 else (22 if days == 7 else qty)
    elif drug == "FOS":
        qty = 1
    else:
        qty = DAILY[key] * days
    txt = _pick(rng, DOSE_TEXT[key if drug != "MEC" else "MEC"])
    if drug not in ("FOS",):
        if rng.random() < 0.55:
            txt = txt + (" for %d days" % days if rng.random() < 0.7 else " x %d/7" % days)
    return name, qty, txt


def course_days(group, pregnant, drug):
    if drug == "FOS":
        return 1
    if pregnant or group == "M":
        return 7
    return 3


def received_at(rng, collected, requester):
    """When the courier's run brings a specimen in (GP couriers do not run at weekends)."""
    hub = requester == W.HUB
    if rng.random() < (0.35 if hub else 0.55):
        day, t = collected, int(rng.integers(13 * 60, 18 * 60 + 30))
    else:
        day, t = collected + TD(days=1), int(rng.integers(7 * 60, 11 * 60))
    while day.weekday() >= 5:
        day = day + TD(days=1)
        t = int(rng.integers(7 * 60, 11 * 60))
    return dt.datetime(day.year, day.month, day.day, t // 60, t % 60)


def authorised_at(rng, received, result):
    lag = int(rng.choice([1, 2, 3], p=[0.50, 0.38, 0.12])) if result == "POS" else int(rng.choice([1, 2], p=[0.8, 0.2]))
    a = received + TD(days=lag)
    t = int(rng.integers(8 * 60, 19 * 60 + 45))
    return dt.datetime(a.year, a.month, a.day, t // 60, t % 60)


def specimen(rng, pid, sex, birth, gp, requester, spec_type, collected, result, orgs):
    rec = received_at(rng, collected, requester)
    return {"pid": pid, "sex": sex, "age": W.age_on(birth, collected), "gp": registered(gp, collected),
            "requester": registered(requester, collected), "type": spec_type, "collected": collected,
            "received": rec, "authorised": authorised_at(rng, rec, result), "result": result, "orgs": orgs}


def build():
    """Every issue and every specimen, 2024 to 2026, with the episodes behind them."""
    issues, specs = [], []
    eps_w = W.women_episodes()
    eps_o = W.older_episodes()
    eps_m = W.men_episodes()
    for e in eps_w + eps_o + eps_m:
        _issue_and_culture(e, issues, specs)
    _children(issues, specs)
    _prophylaxis(eps_o, eps_m, issues)
    _antenatal(eps_w, issues, specs)
    _hospital(specs)
    _second_pots(specs)
    issues = [i for i in issues if W.START <= i["day"] <= W.END]
    specs = [s for s in specs if W.START <= s["collected"] <= W.END]
    issues.sort(key=lambda r: (r["day"], r["issuer"], r["pid"], r["seq"]))
    specs.sort(key=lambda r: (r["received"], r["requester"], r["pid"]))
    return {"women": eps_w, "older": eps_o, "men": eps_m, "issues": issues, "specimens": specs}


def _issue_and_culture(e, issues, specs):
    rng = W.rng_for("detail", e["group"], e["practice"], e["patient"], e["day"].toordinal())
    gp = e["practice"]
    first_by = W.HUB if e["hub"] else gp
    sysname = EMIS.get(registered(first_by, e["day"]), "EMIS")
    days = course_days(e["group"], e["pregnant"], e["drug"])
    if e["group"] == "W":
        prob = PROBLEM_PREG if e["pregnant"] else W.draw(rng, dict(PROBLEMS_W))
    elif e["group"] == "O":
        prob = W.draw(rng, {"Urinary tract infection": 0.52, "Cystitis": 0.18, "Lower urinary tract infection": 0.14,
                            "Recurrent urinary tract infection": 0.10, "Pyelonephritis": 0.03,
                            "Catheter-associated urinary tract infection": 0.03})
    else:
        prob = W.draw(rng, {"Urinary tract infection": 0.70, "Lower urinary tract infection": 0.16, "Cystitis": 0.06,
                            "Prostatitis": 0.05, "Pyelonephritis": 0.03})
    if prob == "Prostatitis":
        days = 14
    seq = 0

    def add_issue(day, drug, issuer, n_days, problem, course_no):
        nonlocal seq
        name, qty, txt = product_row(rng, drug, EMIS.get(registered(issuer, day), "EMIS"), n_days)
        issues.append({"pid": e["patient"], "sex": e["sex"], "birth": e["birth"], "gp": registered(gp, day),
                       "issuer": registered(issuer, day), "day": day, "drug": drug, "product": name, "qty": qty,
                       "dosage": txt, "type": "Acute", "problem": problem, "group": e["group"],
                       "pregnant": e["pregnant"], "course": course_no, "seq": seq})
        seq += 1

    add_issue(e["day"], e["drug"], first_by, days, prob, 1)
    orgs = [(e["org"], e["res"])] if e["org"] else []
    result = e["outcome"]
    if e["cult_pres"]:
        lag = e["cult_pres_lag"]
        if rng.random() < 0.09:
            lag = -1
        if e["group"] == "W":
            lag = 0          # the practice dates the request form at the consultation
        stype = "MSU" if rng.random() < 0.86 else "Urine"
        if e["group"] == "O" and prob == "Catheter-associated urinary tract infection":
            stype = "CSU"
        specs.append(specimen(rng, e["patient"], e["sex"], e["birth"], gp, first_by, stype,
                              e["day"] + TD(days=lag), result, orgs))
    if e["failed"]:
        back = e["day"] + TD(days=e["recon_gap"])
        add_issue(back, e["second"], gp, course_days(e["group"], e["pregnant"], e["second"]), prob, 2)
        if e["cult_fail"]:
            stype = "MSU" if rng.random() < 0.88 else "Urine"
            if e["group"] == "O" and prob == "Catheter-associated urinary tract infection":
                stype = "CSU"
            specs.append(specimen(rng, e["patient"], e["sex"], e["birth"], gp, gp, stype,
                                  back + TD(days=e["cult_fail_lag"]), result, orgs))
        if e["third"]:
            add_issue(back + TD(days=int(rng.integers(3, 6))), e["third"], gp,
                      course_days(e["group"], e["pregnant"], e["third"]), prob, 3)


def _children(issues, specs):
    """Children under 16: a culture at nearly every under-3 consultation and at most others; suspensions by weight."""
    pid = 900000
    for pr in W.practices():
        rng = W.rng_for("children", pr["code"])
        n = int(pr["women"] * 0.58)
        for i in range(n):
            pid += 1
            girl = rng.random() < 0.5
            lam = 0.030 if girl else 0.009
            by = int(rng.integers(2009, 2027))
            birth = D(by, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
            for day in W._episode_dates(rng, lam):
                age = W.age_on(birth, day)
                if age < 0 or age >= 16 or day < birth + TD(days=90):
                    continue
                drug = W.draw(rng, {"TMP": 0.30, "NIT": 0.18, "CEX": 0.30, "AMC": 0.22})
                small = age < 6
                ml = {"TMP": 5 if not small else 2.5, "NIT": 10 if not small else 5, "CEX": 5 if not small else 2.5,
                      "AMC": 5 if not small else 2.5}[drug]
                name, qty, txt = product_row(rng, drug, EMIS.get(registered(pr["code"], day), "EMIS"), 3, child_ml=ml)
                issues.append({"pid": pid, "sex": "F" if girl else "M", "birth": birth, "gp": registered(pr["code"], day),
                               "issuer": registered(pr["code"], day), "day": day, "drug": drug, "product": name,
                               "qty": qty, "dosage": txt + " for %d days" % (3 if age >= 3 else 7), "type": "Acute",
                               "problem": "Urinary tract infection", "group": "C", "pregnant": False, "course": 1,
                               "seq": 0})
                if rng.random() < (0.95 if age < 3 else 0.72):
                    oc = W.draw(rng, {"POS": 0.55, "MIX": 0.17, "NSG": 0.28})
                    orgs = []
                    if oc == "POS":
                        org = W.draw(rng, {"ECOL": 0.80, "KPNE": 0.04, "PMIR": 0.09, "EFAE": 0.03, "ECLO": 0.02,
                                           "KOXY": 0.01, "PAER": 0.01})
                        orgs = [(org, W.susceptibility(rng, org))]
                    stype = "Bag urine" if age < 2 and rng.random() < 0.6 else "Clean catch"
                    specs.append(specimen(rng, pid, "F" if girl else "M", birth, pr["code"], pr["code"], stype,
                                          day + TD(days=int(rng.random() < 0.2)), oc, orgs))


def _prophylaxis(eps_o, eps_m, issues):
    """Repeat templates for recurrent UTI prophylaxis in older women and a few men: a 28-day supply at night."""
    by_pat = defaultdict(list)
    for e in eps_o + eps_m:
        by_pat[(e["group"], e["practice"], e["patient"])].append(e)
    for (g, code, pid), es in sorted(by_pat.items()):
        es.sort(key=lambda x: x["day"])
        start = None
        for a, b in zip(es, es[2:]):
            if (b["day"] - a["day"]).days <= 365:
                start = b["day"] + TD(days=10)
                break
        if start is None:
            continue
        rng = W.rng_for("prophylaxis", code, pid)
        if rng.random() > (0.55 if g == "O" else 0.25):
            continue
        drug = "NIT" if rng.random() < 0.62 else "TMP"
        name = "Nitrofurantoin 50mg tablets" if drug == "NIT" else "Trimethoprim 100mg tablets"
        n = int(rng.integers(4, 14))
        for k in range(n):
            day = start + TD(days=28 * k + int(rng.integers(-2, 3)))
            issues.append({"pid": pid, "sex": es[0]["sex"], "birth": es[0]["birth"], "gp": registered(code, day),
                           "issuer": registered(code, day), "day": day, "drug": drug, "product": name, "qty": 28,
                           "dosage": "ONE at night" if rng.random() < 0.6 else "1 ON", "type": "Repeat",
                           "problem": "Recurrent urinary tract infection", "group": g, "pregnant": False,
                           "course": 0, "seq": 0})


def _antenatal(eps_w, issues, specs):
    """The maternity unit's booking urines (requested by the antenatal clinic), and the few treated bacteriurias."""
    pid = 700000
    for pr in W.practices():
        rng = W.rng_for("antenatal", pr["code"])
        n = int(pr["women"] * 0.039)
        for i in range(n):
            pid += 1
            age = int(rng.integers(18, 44))
            day = W.START + TD(days=int(rng.integers(0, (W.END - W.START).days + 1)))
            birth = D(day.year - age, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
            oc = W.draw(rng, {"NSG": 0.83, "MIX": 0.12, "POS": 0.05})
            orgs = []
            if oc == "POS":
                org = W.draw(rng, {"ECOL": 0.62, "SAGA": 0.24, "EFAE": 0.06, "KPNE": 0.04, "PMIR": 0.04})
                orgs = [(org, W.susceptibility(rng, org))]
            specs.append(specimen(rng, pid, "F", birth, pr["code"], "RHB01", "MSU", day, oc, orgs))
            if oc == "POS" and rng.random() < 0.85:
                drug = W.draw(rng, {"CEX": 0.45, "NIT": 0.35, "AMX": 0.20})
                iday = day + TD(days=int(rng.integers(3, 7)))
                name, qty, txt = product_row(rng, drug, EMIS.get(registered(pr["code"], iday), "EMIS"), 7)
                issues.append({"pid": pid, "sex": "F", "birth": birth, "gp": registered(pr["code"], iday),
                               "issuer": registered(pr["code"], iday), "day": iday, "drug": drug, "product": name,
                               "qty": qty, "dosage": txt, "type": "Acute", "problem": PROBLEM_ASB, "group": "P",
                               "pregnant": True, "course": 1, "seq": 0})


HOSPITAL = ["RHB02", "RHB03", "RHB05", "RHB08"]     # Hollinbrook General: ED, assessment unit, two wards


def _hospital(specs):
    """The hospital's own urine requests for the federation's patients (the emergency department, admissions)."""
    pid = 600000
    for pr in W.practices():
        rng = W.rng_for("hospital", pr["code"])
        n = int(pr["women"] * 0.026)
        for i in range(n * 3):
            pid += 1
            sex = "F" if rng.random() < 0.58 else "M"
            age = int(rng.choice([int(rng.integers(16, 65)), int(rng.integers(65, 98))], p=[0.32, 0.68]))
            day = W.START + TD(days=int(rng.integers(0, (W.END - W.START).days + 1)))
            birth = D(day.year - age, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
            oc = W.draw(rng, {"POS": 0.52, "MIX": 0.18, "NSG": 0.30})
            orgs = []
            if oc == "POS":
                young_w = sex == "F" and age < 65
                mix = W.ORG_OLDER                     # urines the hospital sends are mostly complicated infections
                org = W.draw(rng, mix)
                orgs = [(org, W.susceptibility(rng, org, older=True))]
                if not young_w and rng.random() < 0.06:
                    o2 = W.draw(rng, W.ORG_OLDER)
                    if o2 != org:
                        orgs.append((o2, W.susceptibility(rng, o2, older=True)))
            stype = "CSU" if (age >= 65 and rng.random() < 0.3) else "MSU"
            req = _pick(rng, HOSPITAL)
            s = specimen(rng, pid, sex, birth, pr["code"], req, stype, day, oc, orgs)
            s["received"] = dt.datetime(day.year, day.month, day.day, int(rng.integers(0, 24)), int(rng.integers(0, 60)))
            s["authorised"] = authorised_at(rng, s["received"], oc)
            specs.append(s)


def _second_pots(specs):
    """A practice sometimes sends two pots from one consultation; the laboratory registers each."""
    rng = W.rng_for("second-pots")
    extra = []
    for s in specs:
        if s["requester"] in HOSPITAL or s["requester"] == "RHB01":
            continue
        if rng.random() < 0.004:
            t = dict(s)
            t["received"] = s["received"] + TD(minutes=int(rng.integers(0, 4)))
            t["second_pot"] = True
            extra.append(t)
    specs.extend(extra)
