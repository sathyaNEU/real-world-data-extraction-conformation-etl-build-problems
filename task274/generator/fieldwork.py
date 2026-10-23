"""The survey's fieldwork around the examined adults: the dwellings screened and their rosters, every sample person
and how their case ended, the interview weights, and the dietary supplements each interviewed adult reported.

Some dwellings were screened twice: an interviewer's screenings that never finished syncing were re-released and the
dwelling screened again by another interviewer weeks later. The first screening's roster and its sample persons stayed
in the case management export, each closed at the end of the field period as no contact, and the same people were
selected again at the second screening under new numbers."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as K
import world as W

INT_DONE = ("COMPLETE", "PARTIAL", "COMPLETE - PROXY")
INELIGIBLE = ("INELIGIBLE - MOVED OUT OF DISTRICT", "INELIGIBLE - DECEASED", "INELIGIBLE - INSTITUTIONALIZED")
NONRESP = ("REFUSED", "NO CONTACT", "OTHER NONINTERVIEW")
RELS = ["SPOUSE/PARTNER", "PARENT", "SIBLING", "OTHER RELATIVE", "NONRELATIVE"]


def _age(r):
    return int(min(85, max(20, round(r.gamma(4.2, 11.5) + 12))))


def _supp_iu(r, age, sex):
    pr = 0.30 + (0.18 if age >= 60 else 0.0) + (0.06 if sex == "F" else 0.0)
    if r.random() >= pr:
        return 0.0
    iu = float(r.choice([400, 600, 800, 1000, 1000, 2000, 2000, 5000], p=[.16, .1, .1, .24, .1, .16, .08, .06]))
    return iu * float(r.choice([1.0, 1.0, 1.0, 0.5, 0.8]))


def fieldwork(seed, P):
    r = W.rng(seed, "disp")
    rr = W.rng(seed, "roster")
    SP, screenings, rosters = [], [], []
    pseq = sorted(p["seqn"] for p in P)
    first = {}
    for p in P:
        first[p["county"]] = min(first.get(p["county"], 10 ** 9), p["seqn"])
    used = set(pseq)
    for c, (code, name) in enumerate(K.COUNTIES):
        ex = [p for p in P if p["county"] == c]
        n = len(ex)
        exam_rr = float(r.uniform(0.60, 0.70))
        int_rr = float(r.uniform(max(0.76, exam_rr + 0.08), 0.87))
        E = int(round(n / exam_rr))
        I = max(int(round(E * int_rr)), n + 40)
        inel = int(round(0.022 * E * float(r.uniform(0.6, 1.4))))
        mix = W.RACE_MIX[c]
        people = [dict(kind="EX", p=p, age=p["age"] - int(r.random() < 0.12), sex=p["sex"], race=p["race"])
                  for p in ex]
        for k in range(E - n + inel):
            kind = "INT" if k < I - n else ("NR" if k < E - n else "INEL")
            a = _age(r)
            people.append(dict(kind=kind, p=None, age=a, sex=("M" if r.random() < 0.49 else "F"),
                               race=W.RACES[int(r.choice(4, p=mix))]))
        people = [people[i] for i in r.permutation(len(people))]
        stand0, stand1 = K.STANDS[c]
        groups, i = [], 0
        while i < len(people):
            k = int(r.choice([1, 2, 3], p=[0.66, 0.29, 0.05]))
            groups.append(people[i:i + k])
            i += k
        void_rate = float(r.uniform(0.015, 0.05))
        sc_seq = 1
        new_sel = []
        for j, members in enumerate(groups):
            did = "D%s%05d" % (code, 1000 + 7 * j + int(r.integers(0, 7)))
            exams = [m["p"]["exam"] for m in members if m["p"] is not None]
            if exams:
                sdate = min(exams) - dt.timedelta(days=int(r.integers(12, 55)))
            else:
                sdate = stand1 - dt.timedelta(days=int(r.integers(14, 75)))
            sdate = max(sdate, stand0 - dt.timedelta(days=80))
            void = bool(r.random() < void_rate)
            if void:
                # a re-released dwelling goes to one of the senior interviewers, who turn most refusals round
                for m in members:
                    if m["kind"] == "NR" and r.random() < 0.65:
                        m["kind"] = "INT"
            others = [dict(age=int(r.integers(20, 82)), sex=("M" if r.random() < .5 else "F"), m=None)
                      for _ in range(int(r.choice([0, 1, 2], p=[.45, .45, .10])))]
            kids = [dict(age=int(r.integers(0, 20)), sex=("M" if r.random() < .5 else "F"), m=None)
                    for _ in range(int(r.choice([0, 1, 2, 3], p=[.55, .2, .17, .08])))]
            house = [dict(age=m["age"], sex=m["sex"], m=m) for m in members] + others + kids
            house = [house[q] for q in rr.permutation(len(house))]
            ref = max(range(len(house)), key=lambda q: (house[q]["age"] >= 20, -q))
            house = [house[ref]] + house[:ref] + house[ref + 1:]
            rels = ["REFERENCE PERSON"] + [("CHILD" if h["age"] < 20 else str(rr.choice(RELS, p=[.5, .12, .12, .14, .12])))
                                          for h in house[1:]]
            screens = []
            if void:
                screens.append(("S%s%04d" % (code, sc_seq), sdate - dt.timedelta(days=int(r.integers(16, 46))), True,
                                "FI%03d" % int(r.integers(101, 130))))
                sc_seq += 1
            screens.append(("S%s%04d" % (code, sc_seq), sdate, False, "FI%03d" % int(r.integers(130, 170))))
            sc_seq += 1
            for sid, sd, isvoid, fi in screens:
                screenings.append(dict(id=sid, dwelling=did, county=c, date=sd, void=isvoid, interviewer=fi))
                for line, (h, rel) in enumerate(zip(house, rels), 1):
                    row = dict(screener=sid, dwelling=did, county=c, line=line, age=h["age"], sex=h["sex"],
                               rel=rel, selected=h["m"] is not None, seqn=None, date=sd)
                    rosters.append(row)
                    if h["m"] is None:
                        continue
                    m = h["m"]
                    sp = dict(county=c, screener=sid, dwelling=did, line=line, age=h["age"], sex=h["sex"],
                              race=m["race"], kind=("VOID" if isvoid else m["kind"]), sdate=sd, p=m["p"])
                    if not isvoid and m["p"] is not None:
                        sp["seqn"] = m["p"]["seqn"]
                        row["seqn"] = sp["seqn"]
                    else:
                        new_sel.append((sp, row))
                    SP.append(sp)
        # numbers for the sample persons the examination file does not hold, from the county's free numbers
        lo = first[c]
        hi = first.get(c + 1, max(pseq) + 3 * n)
        free = [q for q in range(lo, hi) if q not in used]
        new_sel.sort(key=lambda t: (t[0]["sdate"], t[0]["screener"], t[0]["line"]))
        if len(free) < len(new_sel):
            raise ValueError("county %d: %d free numbers for %d sample persons" % (c, len(free), len(new_sel)))
        step = len(free) / len(new_sel)
        for k, (sp, row) in enumerate(new_sel):
            q = free[int(k * step)]
            sp["seqn"] = q
            row["seqn"] = q
            used.add(q)
    _outcomes(seed, SP)
    return dict(SP=SP, screenings=screenings, rosters=rosters)


def _outcomes(seed, SP):
    r = W.rng(seed, "dsq2")
    for sp in SP:
        c = sp["county"]
        stand0, stand1 = K.STANDS[c]
        close = stand1 + dt.timedelta(days=7)
        sp["closed"] = close
        sp["exam_date"] = None
        sp["exam_status"] = ""
        sp["int_date"] = None
        sp["wtint"] = None
        k = sp["kind"]
        if k == "VOID":
            sp["int_status"] = "NO CONTACT"
        elif k == "EX":
            p = sp["p"]
            sp["int_status"] = str(r.choice(INT_DONE, p=[.95, .03, .02]))
            lo = sp["sdate"] + dt.timedelta(days=int(r.integers(0, 4)))
            hi = p["exam"] - dt.timedelta(days=3)
            span = max(0, (hi - lo).days)
            sp["int_date"] = lo + dt.timedelta(days=int(r.integers(0, span + 1))) if span else min(lo, hi)
            sp["exam_status"] = "EXAMINED"
            sp["exam_date"] = p["exam"]
            sp["supp_iu"] = p["supp_iu"]
            sp["closed"] = p["exam"]
        elif k == "INT":
            sp["int_status"] = str(r.choice(INT_DONE, p=[.93, .04, .03]))
            d = sp["sdate"] + dt.timedelta(days=int(r.integers(0, 22)))
            sp["int_date"] = min(d, stand1 - dt.timedelta(days=2))
            sp["exam_status"] = "NOT EXAMINED"
            sp["supp_iu"] = _supp_iu(r, sp["age"], sp["sex"])
        elif k == "NR":
            sp["int_status"] = str(r.choice(NONRESP, p=[.55, .30, .15]))
        else:
            sp["int_status"] = str(r.choice(INELIGIBLE, p=[.6, .15, .25]))
    # interview weights, raked to each county's adults
    for c in range(len(K.COUNTIES)):
        ids = [sp for sp in SP if sp["county"] == c and sp["int_date"] is not None]
        for sp in ids:
            adj = (0.55 if sp["race"] in ("NHB", "HSP") else 1.0) * (0.75 if sp["age"] >= 60 else 1.0)
            sp["w_raw"] = adj * float(np.exp(r.normal(0, 0.33)))
        tot = sum(sp["w_raw"] for sp in ids)
        for sp in ids:
            sp["wtint"] = round(sp["w_raw"] * K.ADULTS[c] / tot, 2)


# ---------------------------------------------------------------- dietary supplements
BRANDS = ["Northpine", "Purevane", "Everhale", "Kestra Naturals", "Oakbriar", "Lumivita", "Dawnmere", "Sollenra",
          "Vitamora", "Teskara"]


def catalog(seed):
    """The label database extract: products, serving sizes and their vitamin D per serving, one row an ingredient."""
    r = W.rng(seed, "dsq2")
    r = np.random.default_rng(int(r.integers(1 << 30)) + 5)
    prods = []
    pid = 21043
    def add(brand, name, form, serv, unit_word, vd, vunit, vname, extra):
        nonlocal pid
        pid += int(r.integers(3, 40))
        prods.append(dict(id="DS%06d" % pid, brand=brand, name=name, form=form, serving=serv, serving_unit=unit_word,
                          vd=vd, vunit=vunit, vname=vname, extra=extra))
    for b in BRANDS:
        new = r.random() < 0.6
        for iu, form in ((1000, "Tablet"), (2000, "Softgel"), (5000, "Softgel"), (400, "Tablet")):
            if r.random() < 0.75:
                if new:
                    add(b, "Vitamin D3 %s mcg (%s IU)" % (iu // 40, format(iu, ",")), form, 1, form.lower(), iu // 40,
                        "mcg", str(r.choice(["Vitamin D3 (as cholecalciferol)", "Vitamin D3", "Cholecalciferol"])), [])
                else:
                    add(b, "Vitamin D3 %s IU" % format(iu, ","), form, 1, form.lower(), iu, "IU",
                        str(r.choice(["Vitamin D3", "Vitamin D (as cholecalciferol)"])), [])
        if r.random() < 0.6:
            per = int(r.choice([1000, 2000]))
            add(b, "Vitamin D3 Gummies", "Gummy", 2, "gummies", per // 40, "mcg", "Vitamin D3 (as cholecalciferol)",
                [("Sugar", 3, "g")])
        if r.random() < 0.5:
            add(b, "Daily Multivitamin", "Tablet", 1, "tablet", int(r.choice([10, 15, 20, 25])), "mcg", "Vitamin D3",
                [("Vitamin C", 90, "mg"), ("Vitamin B12", 2.4, "mcg"), ("Zinc", 11, "mg")])
        if r.random() < 0.4:
            add(b, "Calcium 600 + D3", "Tablet", int(r.choice([1, 2])), "tablets", int(r.choice([400, 800])), "IU",
                "Vitamin D3", [("Calcium", 600, "mg")])
        if r.random() < 0.3:
            add(b, "Liquid Vitamin D3 Drops", "Liquid", 1, "drop", 10, "mcg", "Vitamin D3 (as cholecalciferol)", [])
    for nm, ing in (("Fish Oil 1000 mg", ("EPA", 180, "mg")), ("Magnesium Glycinate", ("Magnesium", 120, "mg")),
                    ("Vitamin B12 1000 mcg", ("Vitamin B12", 1000, "mcg")), ("Probiotic 10 Billion", ("Lactobacillus", 10, "billion CFU")),
                    ("Iron 65 mg", ("Iron", 65, "mg")), ("Melatonin 3 mg", ("Melatonin", 3, "mg")),
                    ("Turmeric Curcumin", ("Curcumin", 500, "mg")), ("Glucosamine Chondroitin", ("Glucosamine", 1500, "mg")),
                    ("Biotin 5000 mcg", ("Biotin", 5000, "mcg")), ("Zinc 50 mg", ("Zinc", 50, "mg"))):
        for b in r.choice(BRANDS, size=2, replace=False):
            add(str(b), nm, "Capsule", 1, "capsule", None, None, None, [ing])
    return prods


def _iu_per_unit(p):
    if p["vd"] is None:
        return 0.0
    amt = p["vd"] * (40.0 if p["vunit"] == "mcg" else 1.0)
    return amt / p["serving"]


def products(seed, SP, cat):
    """Each interviewed adult's reported products; the 30-day average from what they took is near their supp_iu."""
    r = W.rng(seed, "dsq2")
    r = np.random.default_rng(int(r.integers(1 << 30)) + 9)
    vd = [p for p in cat if p["vd"] is not None]
    single = [p for p in vd if "Vitamin D3" in p["name"] and "Gumm" not in p["name"] and "Drops" not in p["name"]]
    rows = []
    for sp in sorted(SP, key=lambda s: s["seqn"]):
        if sp.get("int_date") is None:
            continue
        lines = []
        target = sp.get("supp_iu", 0.0)
        if target > 0:
            # the vitamin D product closest to the target, taken daily or on fewer days
            best = None
            for p in vd:
                u = _iu_per_unit(p)
                for qty in (1, 2):
                    if p["serving"] == 2 and qty == 1:
                        continue
                    per_day = u * qty
                    days = int(round(30 * target / per_day))
                    if 1 <= days <= 30:
                        err = abs(per_day * days / 30 - target)
                        key = (err, -days, r.random())
                        if best is None or key < best[0]:
                            best = (key, p, qty, days)
            if best is None:
                p = single[int(r.integers(len(single)))]
                best = (None, p, 1, 30)
            _, p, qty, days = best
            lines.append(dict(p=p, qty=qty, days=days))
            if r.random() < 0.18:
                mv = [q for q in vd if q["name"] in ("Daily Multivitamin", "Calcium 600 + D3")]
                if mv:
                    q = mv[int(r.integers(len(mv)))]
                    dd = int(r.choice([30, 30, 20, 15]))
                    # never the same strength, number and days as the first product, which only a duplicate shares
                    while (_iu_per_unit(q) * q["serving"], q["serving"], dd) == (_iu_per_unit(p) * qty, qty, days):
                        dd -= 1
                    lines.append(dict(p=q, qty=q["serving"], days=dd))
        nonvd = [p for p in cat if p["vd"] is None]
        k_non = int(r.choice([0, 0, 1, 1, 2]))
        for q in [nonvd[int(i)] for i in r.choice(len(nonvd), size=k_non, replace=False)]:
            lines.append(dict(p=q, qty=1, days=int(r.choice([30, 30, 28, 20, 10]))))
        lines = [lines[i] for i in r.permutation(len(lines))]
        for k, ln in enumerate(lines, 1):
            p = ln["p"]
            generic = p["vd"] is not None and p["serving"] == 1 and p["form"] in ("Tablet", "Softgel") \
                and r.random() < 0.20
            rows.append(dict(seqn=sp["seqn"], county=sp["county"], line=k, p=p, qty=ln["qty"], days=ln["days"],
                             generic=generic, dup=False, int_date=sp["int_date"]))
    # processing matched some generic reports to the label database and appended the matched product as a new line,
    # leaving the generic line where it was
    out = []
    by = {}
    for row in rows:
        by.setdefault(row["seqn"], []).append(row)
    for seqn in sorted(by):
        rs = by[seqn]
        out.extend(rs)
        nxt = max(x["line"] for x in rs) + 1
        for x in rs:
            if x["generic"] and r.random() < 0.55:
                d = dict(x)
                d.update(line=nxt, generic=False, dup=True)
                nxt += 1
                out.append(d)
    return out


def avg_iu(rows, drop_dups=True):
    """Each adult's 30-day average vitamin D from supplements, IU a day."""
    tot = {}
    for x in rows:
        if drop_dups and x["dup"]:
            continue
        tot[x["seqn"]] = tot.get(x["seqn"], 0.0) + _iu_per_unit(x["p"]) * x["qty"] * x["days"] / 30.0
    return tot
