"""The Orari Bank world (task133 architecture 3): the region's register, the business banking book, every
borrower's customers, and the year of credits into the borrowers' operating accounts. Clean truth only:
pack.py writes the files and their Layer 1 mess from what this module returns."""
import datetime as dt
import numpy as np

import params as P
import taxonomy as T
from names import Namer, PLACES, bank_party

CITIES = ["Timaru", "Christchurch", "Dunedin", "Invercargill", "Oamaru", "Ashburton", "Queenstown", "Wanaka",
          "Gore", "Alexandra", "Cromwell", "Geraldine", "Waimate", "Rangiora", "Rolleston", "Mosgiel", "Balclutha",
          "Te Anau", "Twizel", "Temuka"]
CITY_W = np.array([16, 22, 14, 9, 6, 7, 6, 4, 3, 2, 3, 2, 1.5, 2, 2, 1.5, 1, 1, .5, 1.5])
BRANCHES = ["Timaru", "Christchurch", "Dunedin", "Invercargill", "Oamaru", "Ashburton", "Queenstown", "Gore"]

GOV = [  # name, BIC
    ("Opuha District Council", "O753010"), ("Waitaha Plains District Council", "O753010"),
    ("Moeraki Coast District Council", "O753010"), ("Mataura Valley District Council", "O753010"),
    ("Lakes and Basin District Council", "O753010"), ("Aoraki District Council", "O753010"),
    ("Taieri City Council", "O753010"), ("Southland Plains District Council", "O753010"),
    ("Ministry of Education", "O751010"), ("Department of Conservation", "O751010"),
    ("Ministry of Social Development", "O751010"), ("Fire and Emergency New Zealand", "O771310"),
    ("Accident Compensation Corporation", "K633010"), ("Health New Zealand", "Q840110"),
]
ACQUIRERS = [("Kahu Merchant Services Limited", "K641920", "KAHU MERCHANT SVCS"),
             ("Tussock Payments Limited", "K641920", "TUSSOCK PAYMENTS")]
INSURERS = [("Kotare Insurance Limited", "K632210"), ("Tasman Mutual Insurance Limited", "K632210"),
            ("Kea General Insurance Limited", "K632210")]


def nzbn(rng, used):
    while True:
        body = "94290" + "".join(str(d) for d in rng.integers(0, 10, 7))
        s = sum(int(c) * (3 if i % 2 else 1) for i, c in enumerate(body))
        chk = (10 - s % 10) % 10
        n = body + str(chk)
        if n not in used:
            used.add(n)
            return n


def bdays(start, end):
    d, out = start, []
    while d <= end:
        if d.weekday() < 5:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def month_starts():
    out, y, m = [], P.WIN_START.year, P.WIN_START.month
    for _ in range(12):
        out.append(dt.date(y, m, 1))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


def month_end(d):
    nx = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
    return nx - dt.timedelta(days=1)


class World:
    pass


def build(seed=P.SEED):
    rng = np.random.default_rng(seed)
    W = World()
    namer = Namer(rng, seed)
    used_nzbn = set()
    reg = []          # register rows: dict
    party_key = {}    # bank_party string -> register index (uniqueness guard)

    def add_entity(name, bic, status="Registered", trading=None, city=None, kind="business"):
        key = bank_party(name)
        tkey = bank_party(trading) if trading else None
        if key in party_key or (tkey and tkey in party_key):
            return None
        e = dict(idx=len(reg), name=name, bic=bic, div=bic[0], status=status, trading=trading,
                 city=city or str(rng.choice(CITIES, p=CITY_W / CITY_W.sum())), nzbn=nzbn(rng, used_nzbn),
                 kind=kind, registered=dt.date(int(rng.integers(1985, 2025)), int(rng.integers(1, 13)),
                                               int(rng.integers(1, 28))))
        reg.append(e)
        party_key[key] = e["idx"]
        if tkey:
            party_key[tkey] = e["idx"]
        return e

    def new_firm(bic, **kw):
        for _ in range(50):
            nm = namer.business(bic)
            trading = None
            if rng.random() < 0.10:
                t_act = nm.split(" Limited")[0].split(" (")[0]
                trading = f"{PLACES[rng.integers(len(PLACES))]} {t_act.split()[-1]}"
            e = add_entity(nm, bic, trading=trading, **kw)
            if e:
                return e
        raise RuntimeError("could not place a firm " + bic)

    # government, acquirers, insurers
    gov = [add_entity(n, b, kind="gov") for n, b in GOV]
    acq = [add_entity(n, b, kind="acquirer") for n, b, _ in ACQUIRERS]
    ins = [add_entity(n, b, kind="insurer") for n, b in INSURERS]

    # payer firms by division
    payers = {}
    for d, (classes, n) in T.PAYER_CLASSES.items():
        if d in ("O",):
            payers[d] = [g for g in gov if g["div"] == "O"]
            continue
        if d == "K":
            payers[d] = ins
            continue
        lst = []
        for i in range(n):
            lst.append(new_firm(classes[int(rng.integers(len(classes)))], kind="payer"))
        payers[d] = lst
    # payer size weights (Zipf-like) so a few buyers are large
    for d, lst in payers.items():
        for j, e in enumerate(lst):
            e["w"] = float(rng.pareto(1.6) + 0.35)
    for e in gov:
        e.setdefault("w", float(rng.pareto(1.6) + 0.35))

    # borrowers
    borrowers = []
    used_cust = set()
    for tname, t in T.TYPES.items():
        for i in range(t["n"]):
            bic = t["own"][int(rng.integers(len(t["own"])))]
            firm = new_firm(bic, kind="borrower")
            while True:
                c = str(int(rng.integers(7100000, 7999999)))
                if c not in used_cust:
                    used_cust.add(c)
                    break
            keys = list(t["mix"])
            alpha = np.array([t["mix"][k] for k in keys]) * 14 + 0.12
            w = rng.dirichlet(alpha)
            mix = {k: float(x) for k, x in zip(keys, w)}
            ead_total = float(np.exp(np.log(t["ead"] * 1000) + rng.normal(0, 0.62)))
            ratio = {"accommodation": 0.9, "food_service": 2.2, "retail": 3.4, "health": 1.6, "recreation": 1.4,
                     "plant_hire": 1.1, "tour_transport": 1.2, "freight": 1.9, "education": 1.5}.get(tname, 2.8)
            sales = ead_total * ratio * float(np.exp(rng.normal(0, 0.25)))
            g = int(np.clip(np.round(rng.normal(4.4, 1.45)), 1, 9))
            b = dict(cust=c, type=tname, firm=firm, bic=bic, div=bic[0], mix=mix, ead_total=ead_total,
                     sales=sales, grade=g, branch=str(rng.choice(BRANCHES, p=[.24, .22, .16, .1, .07, .08, .08, .05])))
            borrowers.append(b)

    # each borrower's payers and the split of its sales across them
    for b in borrowers:
        alloc = []   # (kind, entity or None, annual amount)
        for k, share in b["mix"].items():
            amt = share * b["sales"]
            if amt <= 0:
                continue
            if k == "HH":
                alloc.append(("HH", None, amt))
                continue
            if k == "GOV":
                pool = gov
            else:
                pool = payers[k]
            npay = int(np.clip(1 + rng.poisson(0.4 + 3.2 * share), 1, len(pool)))
            wts = np.array([e["w"] for e in pool])
            idx = rng.choice(len(pool), size=npay, replace=False, p=wts / wts.sum())
            ws = rng.dirichlet(np.ones(npay) * 0.9)
            for j, s in zip(idx, ws):
                alloc.append(("B2B", pool[int(j)], amt * float(s)))
        b["alloc"] = alloc

    # filler register entities so the extract reads as the region's register, not the bank's payer list
    filler_target = 26300 - len(reg)
    all_classes = [c for c in T.BIC if c[0] not in "O"]
    removed_n = 0
    for i in range(filler_target):
        bic = all_classes[int(rng.integers(len(all_classes)))]
        status = "Registered"
        if rng.random() < 0.035:
            status = "Removed"
            removed_n += 1
        try:
            new_firm(bic, kind="filler", status=status)
        except RuntimeError:
            continue

    W.reg = reg
    W.used_cust = used_cust
    W.gov, W.acq, W.ins, W.payers = gov, acq, ins, payers
    W.borrowers = borrowers
    W.rng = rng
    W.namer = namer
    W.party_key = party_key
    _facilities(W)
    _credits(W)
    return W


def _facilities(W):
    rng = W.rng
    facs = []
    used = set()

    def fno():
        while True:
            n = "F" + str(int(rng.integers(30000000, 39999999)))
            if n not in used:
                used.add(n)
                return n
    for b in W.borrowers:
        E = b["ead_total"]
        t = b["type"]
        big = E > 2.2e6
        rows = []
        od_share = float(rng.uniform(0.18, 0.42))
        od_limit = round(E * od_share / 0.75 / 1000) * 1000
        prod = "Revolving credit facility" if big and rng.random() < 0.5 else "Business overdraft"
        util = float(np.clip(rng.beta(2.4, 2.0), 0.05, 0.98))
        sec_od = str(rng.choice(["GSA", "RM1", "UNS"], p=[.72, .2, .08]))
        rows.append(dict(product=prod, limit=od_limit, drawn=round(od_limit * util, 2), security=sec_od))
        rest = max(E - od_limit * (util + (1 - util) * 0.5), 0.15 * E)
        if t in ("freight", "plant_hire", "tour_transport", "civil", "machinery_mfr") and rng.random() < 0.75:
            eq = rest * float(rng.uniform(0.35, 0.7))
            rows.append(dict(product="Equipment finance", limit=round(eq, -2), drawn=round(eq * float(rng.uniform(.55, .95)), 2), security="EQP"))
            rest -= eq
        if rest > 40000:
            sec_tl = str(rng.choice(["CM1", "RM1", "GSA"], p=[.5, .28, .22]))
            lim = round(rest / float(rng.uniform(.75, .98)), -3)
            rows.append(dict(product="Business term loan", limit=lim, drawn=round(rest, 2), security=sec_tl))
        sc = P.EXPOSURE_SCALE[P.SEG_OF[b["div"]]]
        for r in rows:
            r["limit"] = round(r["limit"] * sc, -2)
            r["drawn"] = round(min(r["drawn"] * sc, r["limit"] * 1.02), 2)
            r.update(fac=fno(), cust=b["cust"],
                     start=dt.date(int(rng.integers(2014, 2026)), int(rng.integers(1, 13)), int(rng.integers(1, 28))))
            if r["start"] > P.BOOK_DATE:
                r["start"] = dt.date(2026, 3, 2)
            facs.append(r)
        b["facs"] = rows
    W.facs = facs


def _credits(W):
    """A year of credits into each borrower's operating account (truth, before any rendering)."""
    rng = W.rng
    ms = month_starts()
    days = bdays(P.WIN_START, P.WIN_END)
    trend = {d: v[-1] / 100.0 for d, v in T.YOY_PATH.items()}
    # seasonal shape of household spending and of visitor-heavy hospitality (Oct..Sep)
    hh_season = np.array([0.97, 1.0, 1.12, 1.08, 1.02, 0.98, 0.96, 0.93, 0.96, 1.0, 0.99, 0.99])
    h_season = np.array([0.95, 1.0, 1.16, 1.18, 1.10, 1.0, 0.88, 0.84, 0.9, 1.02, 1.04, 0.93])
    rows = []
    for b in W.borrowers:
        acct = f"84-{int(rng.integers(2200, 2290))}-{int(rng.integers(100000, 9999999)):07d}-00"
        b["acct"] = acct
        acq = W.acq[int(rng.integers(len(W.acq)))]
        b["acq"] = acq
        settle_daily = acq["name"].startswith("Kahu") and b["sales"] > 4.0e6
        for kind, ent, amt in b["alloc"]:
            if kind == "B2B":
                d = ent["div"]
                g = trend.get(d, 0.0)
                f = np.array([1 + g * (m - 5.5) / 12 for m in range(12)])
                if d == "H":
                    f = f * h_season
                f = f / f.mean()
                monthly = amt / 12.0 * f
                cadence = 2 if rng.random() < 0.12 else 1
                payday = int(rng.integers(5, 26))
                p_active = float(rng.uniform(0.7, 1.0))
                active = rng.random(12) < p_active
                active[int(rng.integers(12))] = True
                monthly = monthly * 12.0 / float((f * active).sum()) * f.sum() / 12.0
                for m, mstart in enumerate(ms):
                    if not active[m]:
                        continue
                    for c in range(cadence):
                        if monthly[m] * (1 + rng.normal(0, .18)) <= 0:
                            continue
                        day = min(payday + 14 * c, 28)
                        dte = dt.date(mstart.year, mstart.month, day)
                        while dte.weekday() >= 5:
                            dte += dt.timedelta(days=1)
                        a = monthly[m] / cadence * float(np.exp(rng.normal(0, 0.22)))
                        if a < 40:
                            continue   # an occasional buyer with nothing to pay that month
                        rows.append(dict(cust=b["cust"], date=dte, src="B2B", ent=ent["idx"], amount=round(a, 2)))
            else:   # households: card settlements, private payers, cash
                is_card = b["type"] in ("retail", "accommodation", "food_service", "recreation", "tour_transport",
                                        "personal", "auto_repair", "health", "education") or rng.random() < 0.45
                card_share = {"retail": .86, "accommodation": .78, "food_service": .9, "recreation": .82,
                              "tour_transport": .85, "personal": .8, "auto_repair": .45, "health": .5,
                              "education": .25}.get(b["type"], .55) if is_card else 0.0
                cash_share = {"retail": .05, "food_service": .06, "personal": .1}.get(b["type"], 0.0)
                priv_share = max(0.0, 1 - card_share - cash_share)
                seas = (h_season if b["div"] == "H" else hh_season)
                seas = seas / seas.mean()
                if card_share > 0:
                    yearly = amt * card_share
                    if settle_daily:
                        dlist = days
                    else:
                        dlist = [d for d in days if d.weekday() == 1]
                    mi = np.array([(d.year - P.WIN_START.year) * 12 + d.month - P.WIN_START.month for d in dlist])
                    wts = seas[mi] * np.exp(rng.normal(0, 0.25, len(dlist)))
                    vals = yearly * wts / wts.sum()
                    for dte, v in zip(dlist, vals):
                        rows.append(dict(cust=b["cust"], date=dte, src="CARD", ent=acq["idx"], amount=round(float(v), 2)))
                if priv_share > 0:
                    yearly = amt * priv_share
                    n = int(np.clip(rng.poisson(10 + yearly / 40000), 5, 70))
                    dsel = sorted(rng.choice(len(days), size=n, replace=True))
                    wts = np.exp(rng.normal(0, 0.7, n))
                    vals = yearly * wts / wts.sum()
                    for j, v in zip(dsel, vals):
                        fn, ln = W.namer.person()
                        rows.append(dict(cust=b["cust"], date=days[int(j)], src="PRIV", ent=None,
                                         payer=(fn, ln), amount=round(float(v), 2)))
                if cash_share > 0:
                    yearly = amt * cash_share
                    dlist = [d for d in days if d.weekday() == 0 and d.isocalendar()[1] % 2 == 0]
                    wts = np.exp(rng.normal(0, 0.3, len(dlist)))
                    vals = yearly * wts / wts.sum()
                    for dte, v in zip(dlist, vals):
                        rows.append(dict(cust=b["cust"], date=dte, src="CASH", ent=None, amount=round(float(v), 2)))
        # credits that are not sales
        nonrev = []
        if rng.random() < 0.55:
            for k in range(int(rng.integers(1, 5))):
                nonrev.append(("TFR", b["sales"] * float(rng.uniform(.002, .012))))
        if rng.random() < 0.35:
            for k in range(int(rng.integers(1, 4))):
                nonrev.append(("IRD", b["sales"] * float(rng.uniform(.001, .008))))
        if rng.random() < 0.18:
            nonrev.append(("LOAN", b["ead_total"] * float(rng.uniform(.05, .2))))
        if rng.random() < 0.07 and b["type"] != "auto_repair":
            nonrev.append(("CLAIM", b["sales"] * float(rng.uniform(.004, .02))))
        for kind, v in nonrev:
            rows.append(dict(cust=b["cust"], date=days[int(rng.integers(len(days)))], src=kind, ent=None, amount=round(v, 2)))
        interest_bearing = rng.random() < 0.45
        for m, mstart in enumerate(ms):
            if interest_bearing:
                rows.append(dict(cust=b["cust"], date=month_end(mstart), src="INT", ent=None,
                                 amount=round(float(rng.uniform(0.4, 60.0)), 2)))
    W.credits = rows


# ---------------------------------------------------------------- truth for the main call
def own_change(b):
    return P.SCENARIO_CHANGE[b["div"]]


def payer_change(b, W, hh_rule="own"):
    """The borrower's sales change under the scenario read through who pays it (truth: from the allocation)."""
    tot = 0.0
    s = 0.0
    for kind, ent, amt in b["alloc"]:
        if kind == "HH":
            ch = P.SCENARIO_CHANGE[b["div"]]
        else:
            ch = P.SCENARIO_CHANGE[ent["div"]]
        s += amt * ch
        tot += amt
    return s / tot


def ead(r):
    if r["product"] in P.REVOLVING:
        return r["drawn"] + P.CCF_REVOLVING * max(0.0, r["limit"] - r["drawn"])
    return r["drawn"]


def stressed_loss(W, change_of):
    tot = 0.0
    for b in W.borrowers:
        if b["in_default"]:
            continue
        ch = change_of(b)
        m = P.multiplier(-ch)
        pd = min(1.0, P.GRADE_PD[b["grade"]] / 100.0 * m)
        for r in b["facs"]:
            tot += pd * P.LGD[r["security"]] * ead(r)
    return tot


def make(seed=P.SEED):
    """The whole world: the main call's truth and both ask worlds (which also set who is in default)."""
    import world_asks
    W = build(seed)
    world_asks.build_losses(W)
    world_asks.build_backtest(W)
    return W
