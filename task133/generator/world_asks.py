"""The ask worlds: realised credit losses (write-offs and recoveries) and the 2025 risk-grade back-test.
Clean truth; pack_asks.py renders the files."""
import datetime as dt
import numpy as np

import params as P
import taxonomy as T


BANDS = [(1, 3), (4, 4), (5, 5), (6, 6), (7, 9)]
BAND_LABEL = ["Grades 1 to 3", "Grade 4", "Grade 5", "Grade 6", "Grades 7 to 9"]


def rdate(rng, a, b):
    if b < a:
        return a
    return a + dt.timedelta(days=int(rng.integers(0, (b - a).days + 1)))


def half_of(d):
    if P.H1[0] <= d <= P.H1[1]:
        return "H1"
    if P.H2[0] <= d <= P.H2[1]:
        return "H2"
    return None


def _cust_maker(rng, used):
    def make():
        while True:
            c = str(int(rng.integers(7100000, 7999999)))
            if c not in used:
                used.add(c)
                return c
    return make


def build_losses(W):
    """Former business customers written off, their recoveries and the guarantors pursued for them."""
    rng = np.random.default_rng(P.SEED + 101)
    used_c = W.used_cust
    cust_no = _cust_maker(rng, used_c)
    used_f = {r["fac"] for r in W.facs}

    def fac_no():
        while True:
            n = "F" + str(int(rng.integers(30000000, 39999999)))
            if n not in used_f:
                used_f.add(n)
                return n

    seg_types = {
        "Construction": (["trades", "home_builder", "civil"], [5, 4, 1]),
        "Manufacturing": (["building_mfr", "other_mfr", "food_mfr", "machinery_mfr"], [3, 2, 2, 1]),
        "Trade and logistics": (["freight", "foodservice_wh", "courier", "building_wh"], [3, 2, 1, 1]),
        "Hospitality, retail and leisure": (["food_service", "retail", "accommodation", "recreation"], [4, 3, 2, 1]),
        "Business and property services": (["labour_hire", "engineering", "cleaning", "plant_hire", "it_marketing"], [2, 2, 2, 1, 1]),
        "Health, education and personal services": (["auto_repair", "personal", "health"], [2, 2, 1]),
    }
    fillers = [e for e in W.reg if e["kind"] == "filler" and e["status"] == "Registered"]
    by_bic = {}
    for e in fillers:
        by_bic.setdefault(e["bic"], []).append(e)
    cos, taken = [], set()
    for segname, (tl, tw) in seg_types.items():
        tw = np.array(tw, float)
        n_seg = 11
        k = 0
        while k < n_seg:
            t = tl[int(rng.choice(len(tl), p=tw / tw.sum()))]
            bic = T.TYPES[t]["own"][int(rng.integers(len(T.TYPES[t]["own"])))]
            cands = [e for e in by_bic.get(bic, []) if e["idx"] not in taken]
            if not cands:
                continue
            e = cands[int(rng.integers(len(cands)))]
            taken.add(e["idx"])
            e["kind"] = "former"
            if rng.random() < 0.5:
                e["status"] = "Removed"
            # write-offs spread so that every segment has some in each half of the year and some before it
            slot = k % 4
            if slot == 3 and segname in ("Construction", "Hospitality, retail and leisure"):
                slot = 1     # failures in the two hardest-hit segments ran on into the second half
            if slot == 0:
                wo = rdate(rng, dt.date(2025, 10, 6), dt.date(2026, 3, 27))
            elif slot == 1:
                wo = rdate(rng, dt.date(2026, 4, 2), dt.date(2026, 9, 25))
            else:
                wo = rdate(rng, dt.date(2023, 11, 1), dt.date(2025, 9, 26))
            dflt = wo - dt.timedelta(days=int(rng.integers(150, 480)))
            nf = 1 if rng.random() < 0.6 else 2
            med = P.WO_MEDIAN * P.WO_SEG_FACTOR.get(segname, 1.0)
            facs = [dict(fac=fac_no(), wo=round(float(np.exp(rng.normal(np.log(med), 0.8))), 2)) for _ in range(nf)]
            e["default"], e["wo"] = dflt, wo
            if e["registered"] > dflt - dt.timedelta(days=400):
                # an older company: registration well before the lending relationship soured
                e["registered"] = dflt - dt.timedelta(days=400 + int(e["nzbn"][-4:]) % 3300)
            cos.append(dict(cust=cust_no(), ent=e, type=t, seg=segname, default=dflt, wo_date=wo, facs=facs))
            k += 1
    wo_rows = []
    for c in cos:
        for f in c["facs"]:
            wo_rows.append(dict(fac=f["fac"], cust=c["cust"], date=c["wo_date"], amount=f["wo"]))
            if rng.random() < 0.16:
                later = c["wo_date"] + dt.timedelta(days=int(rng.integers(40, 220)))
                if later <= P.WIN_END:
                    wo_rows.append(dict(fac=f["fac"], cust=c["cust"], date=later,
                                        amount=round(f["wo"] * float(rng.uniform(.05, .22)), 2)))
    cases, gcases, receipts, guarantees, persons, realis = [], [], [], [], [], []
    used_case = set()

    def case_no(d):
        while True:
            n = f"COL-{d.year % 100:02d}-{int(rng.integers(1000, 9999)):04d}"
            if n not in used_case:
                used_case.add(n)
                return n
    for c in cos:
        c["case"] = case_no(c["default"])
        cases.append(dict(case=c["case"], cust=c["cust"], opened=c["default"]))
        tot = sum(f["wo"] for f in c["facs"])
        # before the write-off: instalments under arrangements, and a realised security for some
        for k in range(int(rng.integers(0, 4))):
            d = rdate(rng, c["default"], c["wo_date"] - dt.timedelta(days=1))
            receipts.append(dict(case=c["case"], date=d, amount=round(float(rng.uniform(1500, 24000)), 2),
                                 type=str(rng.choice(["Instalment", "Arrangement payment"])), ref="",
                                 owner=c["cust"], counts=False))
        if rng.random() < 0.4:
            d = rdate(rng, c["default"] + dt.timedelta(days=20), c["wo_date"] - dt.timedelta(days=5))
            gross = float(rng.uniform(30000, 160000))
            costs = gross * float(rng.uniform(.03, .07))
            pref = f"PROP {int(rng.integers(1000, 9999))}"
            realis.append(dict(pref=pref, date=d, gross=round(gross, 2), costs=round(costs, 2),
                               net=round(gross - costs, 2), fac=c["facs"][0]["fac"]))
            receipts.append(dict(case=c["case"], date=d, amount=round(gross - costs, 2), type="Security realisation",
                                 ref=pref, owner=c["cust"], counts=False))
        # after the write-off: the customer's or a director's instalments for a few months, a liquidator's
        # dividend for some, then the collection agency's remittances once the debt is placed with it
        wo = c["wo_date"]
        horizon = P.WIN_END + dt.timedelta(days=60)
        for k in range(int(rng.integers(0, 3))):
            d = rdate(rng, wo + dt.timedelta(days=3), wo + dt.timedelta(days=120))
            if d <= horizon:
                receipts.append(dict(case=c["case"], date=d, amount=round(tot * float(rng.uniform(.01, .04)), 2),
                                     type="Instalment", ref="", owner=c["cust"], counts=True))
        if rng.random() < 0.35:
            d = rdate(rng, wo + dt.timedelta(days=150), wo + dt.timedelta(days=420))
            if d <= horizon:
                receipts.append(dict(case=c["case"], date=d, amount=round(tot * float(rng.uniform(.02, .08)), 2),
                                     type="Liquidator dividend", ref="", owner=c["cust"], counts=True))
        if rng.random() < 0.8:
            placed = wo + dt.timedelta(days=int(rng.integers(90, 200)))
            commission = float(rng.choice([0.18, 0.20, 0.22, 0.25]))
            d = placed + dt.timedelta(days=int(rng.integers(25, 70)))
            while d <= min(placed + dt.timedelta(days=700), horizon):
                gross = round(tot * float(rng.uniform(.003, .014)), 2)
                # the agency's statement upload carries the debtor's payment gross of commission, on the day paid;
                # the remittance the bank receives is net of commission, some days later
                d0 = d - dt.timedelta(days=int(rng.integers(6, 26)))
                receipts.append(dict(case=c["case"], date=d0, amount=gross, type="Agency collection",
                                     ref="WMA STMT", owner=c["cust"], counts=False))
                receipts.append(dict(case=c["case"], date=d, amount=round(gross * (1 - commission), 2),
                                     type="Agency remittance", ref="", owner=c["cust"], counts=True))
                d = d + dt.timedelta(days=int(rng.integers(28, 95)))
    # guarantors pursued on their own cases, opened against their personal customer numbers
    for c in cos:
        if rng.random() >= P.GUARANTOR_SHARE:
            continue
        fn, ln = W.namer.person()
        pc = cust_no()
        persons.append(dict(cust=pc, name=f"{fn} {ln}"))
        gno = f"G{int(rng.integers(40000, 69999))}"
        tot = sum(f["wo"] for f in c["facs"])
        limit = round(tot * float(rng.uniform(.6, 1.3)), -3)
        signed = c["default"] - dt.timedelta(days=int(rng.integers(500, 2400)))
        guarantees.append(dict(gno=gno, guarantor=pc, company=c["cust"], fac=c["facs"][0]["fac"],
                               limit=limit, signed=signed))
        if c["ent"]["registered"] > signed - dt.timedelta(days=90):
            c["ent"]["registered"] = signed - dt.timedelta(days=90 + int(c["ent"]["nzbn"][-4:]) % 1500)
        opened = c["wo_date"] + dt.timedelta(days=int(rng.integers(5, 40)))
        gc = case_no(opened)
        gcases.append(dict(case=gc, cust=pc, opened=opened))
        for k in range(int(rng.integers(2, 5))):
            lo = max(opened + dt.timedelta(days=10), P.WIN_START)
            d = rdate(rng, lo, lo + dt.timedelta(days=330))
            if d > P.WIN_END + dt.timedelta(days=60):
                continue
            receipts.append(dict(case=gc, date=d, amount=round(tot * float(rng.uniform(.03, .10)), 2),
                                 type="Instalment", ref="", owner=c["cust"], counts=True))
    W.loss_cos, W.wo_rows, W.cases, W.gcases = cos, wo_rows, cases, gcases
    W.coll_receipts, W.guarantees, W.persons, W.realis = receipts, guarantees, persons, realis
    # truth: net loss by segment and half
    first_wo = {}
    for r in wo_rows:
        first_wo[r["cust"]] = min(first_wo.get(r["cust"], r["date"]), r["date"])
    seg_of = {c["cust"]: c["seg"] for c in cos}
    net = {(s, h): 0.0 for s, _ in P.SEGMENTS for h in ("H1", "H2")}
    for r in wo_rows:
        h = half_of(r["date"])
        if h:
            net[(seg_of[r["cust"]], h)] += r["amount"]
    for r in receipts:
        h = half_of(r["date"])
        if h and r["counts"] and r["date"] >= first_wo[r["owner"]]:
            net[(seg_of[r["owner"]], h)] -= r["amount"]
    W.ask_a_truth = net


def build_backtest(W):
    """Business borrowers graded at 30 September 2025 and their defaults over the following year."""
    rng = np.random.default_rng(P.SEED + 202)
    snap = []
    for b in W.borrowers:
        if rng.random() < 0.95:
            g = int(np.clip(b["grade"] + rng.choice([-1, 0, 0, 0, 1]), 1, 9))
            snap.append(dict(cust=b["cust"], name=b["firm"]["name"], nzbn=b["firm"]["nzbn"], model=g, left=None, b=b))
    fillers = [e for e in W.reg if e["kind"] == "filler" and e["status"] == "Registered" and e["bic"][0] in "CEFGHILMNPQS"]
    cust_no = _cust_maker(rng, W.used_cust)
    taken = set()
    for i in range(P.LEAVERS):
        e = fillers[int(rng.integers(len(fillers)))]
        if e["idx"] in taken:
            continue
        taken.add(e["idx"])
        e["kind"] = "leaver"
        g = int(np.clip(np.round(rng.normal(5.0, 1.6)), 1, 9))
        why = str(rng.choice(["repaid", "refinanced", "rural", "failed"], p=[.40, .32, .16, .12]))
        snap.append(dict(cust=cust_no(), name=e["name"], nzbn=e["nzbn"], model=g, left=why, b=None))
    # customers later written off: in default already at 30 September 2025 (grade D), or graded then and
    # defaulting in the year
    asof = dt.date(2025, 9, 30)
    for c in W.loss_cos:
        if c["wo_date"] <= asof:
            continue
        if c["default"] <= asof:
            snap.append(dict(cust=c["cust"], name=c["ent"]["name"], nzbn=c["ent"]["nzbn"], model="D", left="wo", b=None,
                             loss=c))
        else:
            g = int(np.clip(np.round(rng.normal(6.0, 1.3)), 2, 9))
            snap.append(dict(cust=c["cust"], name=c["ent"]["name"], nzbn=c["ent"]["nzbn"], model=g, left="wo", b=None,
                             loss=c))
    graded = [i for i, s in enumerate(snap) if s["model"] != "D"]
    overrides = []
    for i in rng.choice(graded, size=84, replace=False):
        s = snap[int(i)]
        appr = rdate(rng, dt.date(2024, 4, 1), dt.date(2026, 6, 30))
        removed = appr + dt.timedelta(days=int(rng.integers(90, 600))) if rng.random() < 0.45 else None
        og = int(np.clip(s["model"] + rng.choice([-2, -1, 1, 1, 2]), 1, 9))
        if og == s["model"]:
            og = min(9, og + 1)
        overrides.append(dict(cust=s["cust"], model=s["model"], override=og, approved=appr, removed=removed,
                              reason=str(rng.choice(["Management accounts since review", "Security strengthened",
                                                     "Key customer loss", "Director guarantee added",
                                                     "Industry outlook", "Covenant breach waived"]))))
    for s in snap:
        s["grade"] = s["model"]
    for o in overrides:
        if o["approved"] <= asof and (o["removed"] is None or o["removed"] > asof):
            for s in snap:
                if s["cust"] == o["cust"]:
                    s["grade"] = o["override"]
    # connected groups among current borrowers: a group defaults together under cross-default.
    # Members are drawn across the grade bands so every band holds members of groups that defaulted.
    cur = [s for s in snap if s["b"] is not None]
    band = lambda g: 0 if g <= 3 else (1 if g == 4 else (2 if g == 5 else (3 if g == 6 else 4)))
    by_band = {k: [s for s in cur if band(s["grade"]) == k] for k in range(5)}
    for k in by_band:
        rng.shuffle(by_band[k])
    groups, member_of = [], {}
    forced = []
    for gi in range(P.GROUPS):
        size = 2 if rng.random() < 0.65 else 3
        mem = []
        for j in range(size):
            k = (gi + 2 * j) % 5
            while by_band[k] and by_band[k][-1]["cust"] in member_of:
                by_band[k].pop()
            if by_band[k]:
                mem.append(by_band[k].pop())
        if len(mem) < 2:
            continue
        while True:
            gid = f"CG{int(rng.integers(1000, 9999))}"
            if not any(g["gid"] == gid for g in groups):
                break
        groups.append(dict(gid=gid, members=[m["cust"] for m in mem]))
        for m in mem:
            member_of[m["cust"]] = gid
        if gi < P.FORCED_GROUPS:
            forced.append(mem[0]["cust"])
    defaulted = set()
    for s in snap:
        if s["model"] == "D":
            continue
        if s["left"] == "wo":
            defaulted.add(s["cust"])
            continue
        p = P.GRADE_PD[s["grade"]] / 100.0 * P.YEAR_PD_FACTOR
        if s["left"] == "failed":
            p = 0.92
        elif s["left"] in ("repaid", "refinanced"):
            p *= 0.25
        elif s["left"] == "rural":
            p *= 1.8
        if rng.random() < p:
            defaulted.add(s["cust"])
    defaulted |= set(forced)
    gdef = []
    for g in groups:
        if any(m in defaulted for m in g["members"]):
            gdef.append(g)
            defaulted |= set(g["members"])
    by = {s["cust"]: s for s in snap}
    for c in sorted(defaulted):
        if by[c]["left"] == "wo":
            by[c]["dflt_date"] = by[c]["loss"]["default"]
        else:
            by[c]["dflt_date"] = rdate(rng, dt.date(2025, 10, 6), dt.date(2026, 9, 24))
    # merged customer numbers from the March 2026 clean-up of duplicate customer records
    merge = []
    for c in sorted(defaulted):
        if by[c]["b"] is None and by[c]["left"] != "wo" and rng.random() < 0.3:
            merge.append(dict(retired=c, surviving=cust_no(), date=dt.date(2026, 3, 14)))
    remap = {m["retired"]: m["surviving"] for m in merge}
    events_b, events_r = [], []
    done = set()
    rng_t = np.random.default_rng(P.SEED + 207)   # default triggers as the register records them
    ordinary = ["90 days past due", "Unlikely to pay", "Receivership", "Liquidation", "Cross-default"]
    for c in sorted(defaulted, key=lambda x: (by[x]["dflt_date"], x)):
        if c in done:
            continue
        s = by[c]
        gid = member_of.get(c)
        if gid and any(g["gid"] == gid for g in gdef):
            g = [g for g in gdef if g["gid"] == gid][0]
            lead = g["members"][0]
            first = min(g["members"], key=lambda m: (by[m]["dflt_date"] if m in by and "dflt_date" in by[m] else dt.date(2100, 1, 1), m))
            d = by[first]["dflt_date"]
            trig0 = str(rng_t.choice(ordinary[:3]))
            for m in g["members"]:
                for f in by[m]["b"]["facs"]:
                    events_b.append(dict(lead=lead, true=m, fac=f["fac"], date=d,
                                         trigger=trig0 if m == first else "Cross-default"))
            done |= set(g["members"])
            continue
        done.add(c)
        # a borrower in default with another lender is in default here under the cross-default clause
        trig = str(rng_t.choice(ordinary, p=[.34, .22, .15, .15, .14]))
        if s["b"]:
            facs = [f["fac"] for f in s["b"]["facs"]]
        elif s["left"] == "wo":
            facs = [f["fac"] for f in s["loss"]["facs"]]
            trig = str(rng_t.choice(["90 days past due", "Receivership", "Liquidation"]))
        else:
            facs = ["F" + str(int(rng.integers(30000000, 39999999))) for _ in range(int(rng.integers(1, 3)))]
        shown = remap.get(c, c) if s["dflt_date"] >= dt.date(2026, 3, 14) else c
        for f in facs:
            ev = dict(lead=shown, true=c, fac=f, date=s["dflt_date"], trigger=trig)
            (events_r if s["left"] == "rural" else events_b).append(ev)
    rural_own = []
    for i in range(40):
        rural_own.append(dict(lead=cust_no(), true=None, fac="F" + str(int(rng.integers(30000000, 39999999))),
                              date=rdate(rng, dt.date(2025, 10, 3), dt.date(2026, 9, 28)),
                              trigger=str(rng_t.choice(ordinary, p=[.4, .25, .15, .1, .1]))))
    # current borrowers that defaulted in the year: most still in default at the book date, a few cured
    for s in snap:
        if s["b"] is not None:
            s["b"]["in_default"] = s["cust"] in defaulted and rng.random() < 0.72
    for b in W.borrowers:
        b.setdefault("in_default", False)
    # business borrowers moved to the rural book during the year whose defaults the rural team recorded (the dairy
    # downturn reached the agricultural contractors and suppliers among them)
    rng_r = np.random.default_rng(P.SEED + P.RURAL_SEED_OFFSET)
    moved = sorted(s["cust"] for s in snap if s["left"] == "rural" and s["cust"] not in defaulted)
    for c in sorted(rng_r.choice(moved, size=min(P.RURAL_DEFAULTS, len(moved)), replace=False).tolist()):
        defaulted.add(c)
        by[c]["dflt_date"] = rdate(rng_r, dt.date(2025, 11, 3), dt.date(2026, 9, 18))
        trig = str(rng_r.choice(["90 days past due", "Unlikely to pay", "Receivership"]))
        for k in range(int(rng_r.integers(1, 3))):
            events_r.append(dict(lead=c, true=c, fac="F" + str(int(rng_r.integers(30000000, 39999999))),
                                 date=by[c]["dflt_date"], trigger=trig))
    # coherence of dates the bank's systems carry: a borrower graded at 30 September 2025 held a facility then,
    # and every borrower was incorporated before its first facility was drawn (no draws consumed here)
    for s in snap:
        if s["b"] is not None:
            first = min(s["b"]["facs"], key=lambda f: (f["start"], f["fac"]))
            if first["start"] > asof:
                first["start"] = first["start"] - dt.timedelta(days=365)
    for b in W.borrowers:
        start = min(f["start"] for f in b["facs"])
        if b["firm"]["registered"] > start - dt.timedelta(days=60):
            b["firm"]["registered"] = start - dt.timedelta(days=60 + int(b["firm"]["nzbn"][-4:]) % 2500)
    W.snap, W.overrides, W.events_b, W.events_r, W.rural_own = snap, overrides, events_b, events_r, rural_own
    W.groups, W.merge, W.defaulted = groups, merge, defaulted
    # truth: by grade in force at 30 Sep 2025, borrowers and defaults
    W.ask_b_truth = {}
    for k, (lo, hi) in enumerate(BANDS):
        n = sum(1 for s in snap if s["grade"] != "D" and lo <= s["grade"] <= hi)
        d = sum(1 for s in snap if s["grade"] != "D" and lo <= s["grade"] <= hi and s["cust"] in defaulted)
        W.ask_b_truth[k] = (n, d)
