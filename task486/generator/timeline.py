"""The island's records over time, cut from the world's two Marches: every premises' address, postcode, UARN and
billing reference; its entries in the 2017 and 2023 valuation lists; who was liable for it day by day from before April
2017 to the end of April 2026 (an occupier's account, or its owner's while it stood empty); every employer's PAYE
schemes and the employees each paid in March 2022 and March 2026; and the companies register.

Billing follows Torvasay's rules: an occupier is liable; an empty premises' owner is liable, with three months'
empty property relief for a shop (six for industrial premises); a trader with no employees in a premises below
8,000 pounds of rateable value has full small trader relief and so no liability at all. Each district publishes the
accounts that carried a liability, so those traders' premises carry no account."""
import datetime as dt
import re
import string

import numpy as np

import names as N
import world as W

D0 = dt.date(2017, 4, 1)
L23 = dt.date(2023, 4, 1)
END = dt.date(2026, 4, 30)
LIST17_AT = dt.date(2022, 4, 4)
LIST23_AT = dt.date(2026, 4, 13)
STR_CEILING = 8000
INDUSTRIAL = ("W1", "W2", "W3")
DAY = dt.timedelta(days=1)


def _date_between(rng, a, b):
    n = (b - a).days
    return a + dt.timedelta(days=int(rng.integers(0, max(n, 1))))


class Namer:
    """people's names drawn freely, kept unique where a ratepayer is matched to its employer on initial and
    surname, and company names kept unique as a register keeps them"""
    def __init__(self, rng):
        self.rng = rng
        self.keys = set()
        self.companies = set()
        self.used = set()

    def person(self, unique_key=False, avoid=False):
        """unique_key: a retail employer matched on initial and surname, kept unique; avoid: anyone else, kept off
        those keys so no trader or other sole trader reads as a retail employer"""
        for _ in range(400):
            f = N.FIRST_NAMES[int(self.rng.integers(0, len(N.FIRST_NAMES)))]
            s = N.SURNAMES[int(self.rng.integers(0, len(N.SURNAMES)))]
            if (unique_key or avoid) and (f[0], s) in self.keys:
                continue
            if unique_key:
                self.keys.add((f[0], s))
            return f, s
        raise RuntimeError("names exhausted")

    @staticmethod
    def norm(name):
        s = re.split(r"\s+T/A\s+", name.upper())[0].replace("LIMITED", "LTD")
        return " ".join(re.sub(r"[^A-Z0-9& ]", " ", s).split())

    def company(self, name, alternatives=()):
        """a company name no other company's name, current or previous, reads as once normalised"""
        for cand in (name,) + tuple(alternatives):
            cand = " ".join(cand.split())
            if self.norm(cand) not in self.companies:
                self.companies.add(self.norm(cand))
                return cand
        i = 2
        while True:
            cand = name.replace(" Limited", " (%d) Limited" % i) if " Limited" in name else "%s %d" % (name, i)
            if self.norm(cand) not in self.companies:
                self.companies.add(self.norm(cand))
                return cand
            i += 1

    def unique(self, make):
        for _ in range(200):
            x = make()
            if x not in self.used:
                self.used.add(x)
                return x
        raise RuntimeError("names exhausted")


def postcodes(w, rng):
    """postcode units: each centre's streets carry its units; the rest of each district carries its own"""
    letters = "ABDEFGHJLNPQRSTUWXYZ"
    taken = set()
    dist = {d[0]: d for d in N.DISTRICTS}

    def unit(district):
        nums = list(dist[district][2])
        while True:
            pc = "LW%d %d%s%s" % (nums[int(rng.integers(0, len(nums)))], int(rng.integers(1, 10)),
                                  letters[int(rng.integers(0, 20))], letters[int(rng.integers(0, 20))])
            if pc not in taken:
                taken.add(pc)
                return pc
    w.pc_unit = unit
    w.centre_units = {}
    for c in w.centres:
        n_prem = sum(1 for p in w.P if p["centre"] == c["k"])
        n_units = max(6, int(round(n_prem / 11)))
        streets = list(rng.choice(N.CENTRE_STREETS, size=min(len(N.CENTRE_STREETS), max(4, n_units // 3)), replace=False))
        w.centre_units[c["k"]] = [(unit(c["district"]), streets[i % len(streets)]) for i in range(n_units)]
    w.unit_centre_k = {pc: k for k, units in w.centre_units.items() for pc, st in units}
    # three centres had units recoded in 2023: the 2017 list keeps the old code, the 2023 list the new
    w.recoded = {}
    w.recoded = {}


def district_of(w, p, rng):
    if p["centre"] is not None:
        return w.centres[p["centre"]]["district"]
    if "district" not in p:
        p["district"] = N.DISTRICTS[int(rng.choice(6, p=[0.36, 0.17, 0.14, 0.13, 0.11, 0.09]))][0]
    return p["district"]


def addresses(w, rng):
    """every premises' address, postcode in each list, UARN and billing reference"""
    seen = set()
    uarns = rng.choice(np.arange(10_000_000, 99_999_999), size=len(w.P) + 4000, replace=False)
    w.next_uarn = iter(int(x) for x in uarns)
    estates = {}
    ba_counter = {d[0]: int(rng.integers(10_000, 40_000)) for d in N.DISTRICTS}
    for p in w.P:
        d = district_of(w, p, rng)
        p["district"] = d
        p["uarn"] = next(w.next_uarn)
        ba_counter[d] += int(rng.integers(1, 9))
        p["ba_n"] = ba_counter[d]
        if p["centre"] is not None:
            pc, st = w.centre_units[p["centre"]][int(rng.integers(0, len(w.centre_units[p["centre"]])))]
            num = int(rng.integers(1, 140))
            while (st, num, p["centre"]) in seen:
                num = int(rng.integers(1, 220))
            seen.add((st, num, p["centre"]))
            p["street"], p["number"], p["locality"] = st, str(num), w.centres[p["centre"]]["name"]
            p["pc17"] = p["pc23"] = pc
        else:
            loc = N.LOCALITIES[d][int(rng.integers(0, len(N.LOCALITIES[d])))]
            z = p["zone"]
            if z in ("park", "ind", "biz", "edge"):
                key = (d, z, loc)
                if key not in estates:
                    kind = {"park": "park", "edge": "park", "ind": "ind", "biz": "biz"}[z]
                    name = "%s %s" % (loc, N.ESTATES[kind][int(rng.integers(0, len(N.ESTATES[kind])))])
                    estates[key] = (name, w.pc_unit(d))
                name, pc = estates[key]
                p["street"], p["number"], p["locality"] = name, "Unit %d" % int(rng.integers(1, 60)), loc
            else:
                p["street"] = N.OTHER_STREETS[int(rng.integers(0, len(N.OTHER_STREETS)))]
                p["number"], p["locality"] = str(int(rng.integers(1, 260))), loc
                pc = w.pc_unit(d)
            p["pc17"] = p["pc23"] = pc


def recode(w, rng):
    """two postcode units recoded by the postal administration in 2023, each holding shop units but no retail
    employer: the 2017 list keeps the old code, the 2023 list the new, and the schedule lists both"""
    by_unit = {}
    for p in w.P:
        if p["centre"] is not None:
            by_unit.setdefault(p["pc17"], []).append(p)
    cand = []
    for pc, ps in sorted(by_unit.items()):
        retail = any((p["o22"] is not None and w.E[p["o22"]]["kind"] in W.RETAIL_KINDS) or
                     (p["o26"] is not None and w.E[p["o26"]]["kind"] in W.RETAIL_KINDS) for p in ps)
        if not retail and sum(1 for p in ps if p["d"] == "R1") >= 2:
            cand.append(pc)
    chosen = []
    for i in rng.permutation(len(cand)):
        c = w.unit_centre_k[cand[i]]
        if c not in [w.unit_centre_k[x] for x in chosen]:
            chosen.append(cand[i])
        if len(chosen) == 2:
            break
    for old in chosen:
        new = w.pc_unit(w.centres[w.unit_centre_k[old]]["district"])
        w.recoded[old] = new
        for p in by_unit[old]:
            p["pc23"] = new


def lists(w, rng):
    """the valuation list entries: each premises' compiled entry, alterations with a later effective date (value
    only), new entries for premises built after a list was compiled, and premises deleted from a list"""
    w.entries17, w.entries23 = [], []
    for p in w.P:
        base = dict(uarn=p["uarn"], district=p["district"], ba_n=p["ba_n"], d=p["d"], a=p["a"], street=p["street"],
                    number=p["number"], locality=p["locality"])
        if p["built"]:
            f17 = D0 if rng.random() > 0.05 else _date_between(rng, D0, dt.date(2021, 12, 1))
            p["f17"] = f17
            if rng.random() < 0.05:
                t = _date_between(rng, f17 + dt.timedelta(days=200), dt.date(2022, 2, 1))
                w.entries17.append(dict(base, pc=p["pc17"], rv=p["rv17"] * rng.uniform(1.04, 1.15), frm=f17, to=t - DAY))
                w.entries17.append(dict(base, pc=p["pc17"], rv=p["rv17"], frm=t, to=None))
            else:
                w.entries17.append(dict(base, pc=p["pc17"], rv=p["rv17"], frm=f17, to=None))
            f23 = L23
        else:
            p["opened_on"] = _date_between(rng, dt.date(2023, 6, 1), dt.date(2025, 12, 1))
            f23 = p["opened_on"]
        p["in23_from"] = f23
        if rng.random() < 0.05 and f23 < dt.date(2025, 1, 1):
            t = _date_between(rng, f23 + dt.timedelta(days=180), dt.date(2026, 1, 15))
            w.entries23.append(dict(base, pc=p["pc23"], rv=p["rv23"] * rng.uniform(1.04, 1.12), frm=f23, to=t - DAY))
            w.entries23.append(dict(base, pc=p["pc23"], rv=p["rv23"], frm=t, to=None))
        else:
            w.entries23.append(dict(base, pc=p["pc23"], rv=p["rv23"], frm=f23, to=None))
    # premises demolished or merged: in the 2017 list until a date before its extract, or in the 2023 list until a
    # date before 31 March 2026, held empty by their owners until then
    w.deleted = []
    w.ba_extra = {d: max(p["ba_n"] for p in w.P if p["district"] == d) for d in set(p["district"] for p in w.P)}
    for i in range(int(len(w.P) * 0.025)):
        src = w.P[int(rng.integers(0, len(w.P)))]
        in23 = rng.random() < 0.45
        d = src["d"]
        a = float(src["a"] * rng.uniform(0.6, 1.3))
        rv = src["rv17"] if src["rv17"] else src["rv23"]
        if rv is None:
            continue
        w.ba_extra[src["district"]] += int(rng.integers(1, 9))
        q = dict(pid=None, uarn=next(w.next_uarn), district=src["district"], ba_n=w.ba_extra[src["district"]], d=d, a=a,
                 street=src["street"], number=str(int(rng.integers(1, 300))), locality=src["locality"],
                 centre=src["centre"], zone=src["zone"], pc17=src["pc17"], pc23=src["pc23"])
        if in23:
            gone = _date_between(rng, dt.date(2023, 9, 1), dt.date(2026, 2, 15))
            w.entries17.append(dict(q, pc=q["pc17"], rv=rv * rng.uniform(0.8, 1.2), frm=D0, to=None))
            w.entries23.append(dict(q, pc=q["pc23"], rv=rv * 0.9 * rng.uniform(0.8, 1.2), frm=L23, to=gone - DAY))
        else:
            gone = _date_between(rng, dt.date(2018, 6, 1), dt.date(2022, 2, 15))
            w.entries17.append(dict(q, pc=q["pc17"], rv=rv * rng.uniform(0.8, 1.2), frm=D0, to=gone - DAY))
        q["gone"] = gone
        q["in23"] = in23
        w.deleted.append(q)


def in_force(entries, uarn, day):
    for e in entries:
        if e["uarn"] == uarn and e["frm"] <= day and (e["to"] is None or e["to"] >= day):
            return e
    return None


def parties(w, rng):
    """names, company numbers, incorporation, trading names; landlords; PAYE agents"""
    nm = Namer(rng)
    w.namer = nm
    orng = np.random.default_rng(getattr(w, "tl_seed", 0) + 7001)
    cn = iter(int(x) for x in rng.choice(np.arange(100_000, 999_999), size=60_000, replace=False))
    w.companies = []

    def company(name, sic, inc_year=None, psc=None, prev=None, status="Active", dissolved=None):
        num = "LC%06d" % next(cn)
        w.companies.append(dict(number=num, name=name, sic=sic, incorporated=dt.date(inc_year or int(rng.integers(1978, 2024)),
                                int(rng.integers(1, 13)), int(rng.integers(1, 28))), psc=psc, prev=prev or [],
                                status=status, dissolved=dissolved))
        return num
    w.company = company
    with_premises = set(p["o22"] for p in w.P if p["o22"] is not None) | set(p["o26"] for p in w.P if p["o26"] is not None)
    # retail employers first, so their name keys are taken before anyone else is named
    for e, E in sorted(w.E.items(), key=lambda kv: (kv[1]["kind"] not in W.RETAIL_KINDS, kv[0])):
        k = E["kind"]
        if k == "chain":
            kind, brand, reg, sic = E["brand"]
            if kind == "small":
                f, s = nm.person()
                trade = sic
                word = [t for t in N.SHOP_TRADES if t[0] == trade][0][1][0]
                brand = "%s's %s" % (s, word) if rng.random() < 0.6 else "%s %s" % (s, word)
                reg = "%s %s Limited" % (s, word)
            E.update(name=nm.company(reg), brand_name=brand, sic=sic, incorporated=True)
        elif k in ("ind", "ind_out", "single"):
            pool = N.SHOP_TRADES if k != "single" else (N.RW_TRADES + [("47910", [x]) for x in N.ONLINE_TRADES])
            sic, words = pool[int(rng.integers(0, len(pool)))]
            word = words[int(rng.integers(0, len(words)))]
            inc = rng.random() < (0.55 if k != "single" else 0.9)
            f, s = nm.person(unique_key=not inc)
            style = rng.random()
            if style < 0.4:
                trading = "%s's %s" % (s, word) if not word.startswith("The") else word
            elif style < 0.7:
                trading = "The %s %s" % (["Corner", "Village", "Market", "Little", "Old", "Bay", "Harbour", "Square"][int(rng.integers(0, 8))], word)
            else:
                loc = w.centres[E["hq"]]["name"] if isinstance(E.get("hq"), int) else N.LOCALITIES["RKG"][int(rng.integers(0, 8))]
                trading = "%s %s" % (loc.split()[0], word)
            if inc:
                reg = "%s %s Limited" % (s, word) if rng.random() < 0.5 else "%s %s Limited" % (trading.replace("'s", "s").replace("The ", ""), "")
                reg = nm.company(" ".join(reg.split()), ("%s %s %s Limited" % (s, word, E.get("hq") and "Torvasay" or "Island"),))
                E.update(name=reg, incorporated=True)
            else:
                if rng.random() < 0.3:
                    f2, _ = nm.person()
                    E.update(name="%s & %s %s" % (f[0], f2[0], s), person=(f, s), partnership=True)
                else:
                    E.update(name="%s %s" % (f, s), person=(f, s))
                E["incorporated"] = False
            E.update(sic=sic, trading=trading)
        elif k == "nonretail":
            sic = E.get("sic") or ["69201", "62020", "70229", "71129", "66220", "68310", "96020", "52103", "46900",
                                   "46390", "93130", "96090"][int(rng.integers(0, 12))]
            if E.get("group") == "bookmaker":
                sic = "92000"
            elif E.get("group") == "estate_agent":
                sic = "68310"
            elif E.get("group") == "charity":
                sic = "88990"
            E["sic"] = sic
            if E.get("public"):
                E.update(name=E["public"], incorporated=False, public_body=True)
                continue
            f, s = nm.person(avoid=True)
            words = {"56101": "Restaurant", "56102": "Cafe", "56103": "Takeaway", "56302": "Inn", "55100": "Hotel",
                     "64191": "Bank", "64192": "Building Society", "45200": "Motors", "46710": "Fuels",
                     "92000": "Bookmakers", "68310": "Estate Agents", "88990": "Trust", "69201": "Accountants",
                     "69202": "Payroll Services", "69102": "Solicitors", "86210": "Medical Practice",
                     "86230": "Dental Practice", "87300": "Care Home", "93130": "Fitness", "96020": "Hair Studio"}
            word = words.get(sic, ["Services", "Engineering", "Contractors", "Consulting", "Logistics", "Solutions",
                                   "Associates", "Group"][int(rng.integers(0, 8))])
            if sic == "68310":
                word = N.AGENT_WORDS[int(orng.integers(0, len(N.AGENT_WORDS)))]
            if sic in ("64191", "64192"):
                reg = nm.company("%s %s plc" % (["Island", "Harbour", "Castle", "Torvasay", "Northern", "Mercantile"][int(rng.integers(0, 6))], word))
                inc = True
            elif sic == "88990":
                reg = nm.company("%s %s" % (["Hospice", "Lifeboat", "Animal", "Children's", "Hearing", "Heart"][int(rng.integers(0, 6))], "Trust Torvasay"))
                inc = True
            else:
                inc = rng.random() < 0.72 or e in with_premises
                reg = nm.company("%s %s Limited" % (s, word), ("%s %s Torvasay Limited" % (s, word), "%s %s (Island) Limited" % (s, word))) if inc else "%s %s" % (f, s)
            E.update(name=reg, incorporated=inc, trading="%s %s" % (s, word))
    # company numbers and previous names
    for e, E in w.E.items():
        if E.get("incorporated"):
            prev = []
            if rng.random() < 0.07 and E["kind"] != "chain" and E["name"].endswith(" Limited"):
                base = E["name"][:-len(" Limited")]
                old = nm.company(base + (" (Torvasay) Limited" if rng.random() < 0.5 else " Trading Limited"),
                                 (base + " Holdings Limited", base + " Group Limited"))
                prev = [(old, _date_between(rng, dt.date(2018, 1, 1), dt.date(2025, 6, 1)))]
            if E["kind"] == "chain" and E["brand"][1] == "Tidemark":
                prev = [(nm.company("Tidemark Retail Limited"), dt.date(2023, 5, 12))]
            E["prev"] = prev
            E["company_no"] = company(E["name"], E["sic"], prev=prev)
    # the grocer whose stores are rated to its property company
    w.groupprop = {}
    for e in w.chains:
        if w.E[e]["brand"][1] == "Kestle":
            parent = company(nm.company("Kestle Group Limited"), "70100")
            w.E[e]["psc"] = parent
            for c in w.companies:
                if c["number"] == w.E[e]["company_no"]:
                    c["psc"] = parent
            w.groupprop[e] = company(nm.company("Kestle Properties Limited"), "68209", psc=parent)
    # landlords: the companies that own premises and are liable while they stand empty: property companies, some under
    # names that say so and some under nominee, holding or numbered names, and developers holding premises bought for
    # schemes
    w.landlords = []
    for i in range(240):
        root = N.LANDLORD_ROOTS[int(rng.integers(0, len(N.LANDLORD_ROOTS)))]
        word = N.LANDLORD_WORDS[int(rng.integers(0, len(N.LANDLORD_WORDS)))]
        r = N.OWNER_ROOTS[int(orng.integers(0, len(N.OWNER_ROOTS)))]
        surname = N.SURNAMES[int(orng.integers(0, len(N.SURNAMES)))]
        u = orng.random()
        if u < 0.16:
            sic = "41100"
            dw = N.DEVELOPER_WORDS[int(orng.integers(0, len(N.DEVELOPER_WORDS)))]
            base = "%s %s" % (surname if orng.random() < 0.5 else r, dw)
        elif u < 0.50:
            sic = "68209"
            base = "%s %s" % (r if orng.random() < 0.7 else root, word)
        else:
            sic = "68209"
            v = orng.random()
            if v < 0.55:
                base = "%s %s" % (r, N.OWNER_WORDS_PLAIN[int(orng.integers(0, len(N.OWNER_WORDS_PLAIN)))])
            elif v < 0.7:
                base = "%s (No. %d)" % (r, int(orng.integers(2, 10)))
            elif v < 0.85:
                base = "%s %d" % (r, int(orng.integers(2009, 2023)))
            else:
                base = "%s Family Holdings" % surname
        name = nm.company("%s Limited" % base, ("%s (Torvasay) Limited" % base, "%s (Island) Limited" % base))
        w.landlords.append(dict(lid=i, name=name, company_no=company(name, sic), sic=sic))
    # payroll agents: bureaus on the business parks and in the City, and the accountants in the centres
    w.agents = [e for e, E in w.E.items() if E.get("sic") in ("69201", "69202") and E["kind"] == "nonretail"]


def _owner(w, p, rng):
    if "owner" not in p:
        p["owner"] = int(rng.integers(0, len(w.landlords)))
    return p["owner"]


def spells(w, rng):
    """who was liable for each premises from before April 2017 to the end of April 2026, consistent with the two
    Marches; an owner's empty spell may change hands when the premises is sold"""
    for p in w.P:
        st22 = ("e", p["o22"]) if p["o22"] is not None else (("t", p["n22"]) if p.get("n22") is not None else ("x", None))
        st26 = ("e", p["o26"]) if p["o26"] is not None else (("t", p["n26"]) if p.get("n26") is not None else ("x", None))
        start_min = p.get("in23_from") if not p["built"] else None
        S = []
        if start_min is not None:            # built after March 2022: one occupier from completion
            S.append([p["in23_from"], None, st26])
        else:
            if st22 == st26:
                if st22[0] == "x":
                    first = M22_minus(rng, long=True)
                else:
                    first = _date_between(rng, dt.date(2004, 1, 1), dt.date(2021, 9, 1))
                S.append([first, None, st22])
            else:
                # an occupier's leaving date, weighted to the later years as the centres' closures were
                back = dt.timedelta(days=int(46 + rng.exponential(14) * 30.4))
                t1 = max(W.M22 + dt.timedelta(days=17), W.M26 - back) if rng.random() < 0.85 else \
                    _date_between(rng, W.M22 + dt.timedelta(days=17), W.M26 - dt.timedelta(days=45))
                first = M22_minus(rng, long=st22[0] == "x") if st22[0] == "x" else _date_between(rng, dt.date(2004, 1, 1), dt.date(2021, 9, 1))
                S.append([first, t1 - DAY, st22])
                if st22[0] != "x" and st26[0] != "x" and rng.random() < 0.7:
                    gap = int(rng.integers(20, 330))
                    t2 = min(t1 + dt.timedelta(days=gap), W.M26 - dt.timedelta(days=16))
                    S.append([t1, t2 - DAY, ("x", None)])
                    S.append([t2, None, st26])
                else:
                    S.append([t1, None, st26])
            # before the first spell, from April 2017 at the latest
            if S[0][0] > D0:
                prev = ("x", None) if (S[0][2][0] != "x" and rng.random() < 0.55) else ("p", None)
                S.insert(0, [_date_between(rng, dt.date(2008, 1, 1), D0 - dt.timedelta(days=30)), S[0][0] - DAY, prev])
        # an occupier spell running on into April 2026 sometimes ends after the March
        if S[-1][2][0] in ("e", "t") and S[-1][1] is None and rng.random() < 0.03:
            t = _date_between(rng, W.M26 + dt.timedelta(days=16), END - dt.timedelta(days=3))
            S[-1][1] = t - DAY
            S.append([t, None, ("x", None)])
        p["spells"] = [dict(frm=a, to=b, who=s) for a, b, s in S]
        # sales of premises standing empty, the new owner liable from the sale
        for sp in p["spells"]:
            if sp["who"][0] == "x":
                sp["owner"] = _owner(w, p, rng)
        out = []
        for sp in p["spells"]:
            end = sp["to"] or END
            cuts = []
            if sp["who"][0] == "x":
                # a premises standing empty may be sold: often in the year before a March it stood empty through, so
                # the account current that March is the new owner's while the emptiness runs back to the first
                for march in (W.M22, W.M26):
                    since = dt.date(march.year - 1, 4, 1)
                    if sp["frm"] <= since and end >= march and rng.random() < 0.35:
                        cuts.append(_date_between(rng, since + dt.timedelta(days=15), march - dt.timedelta(days=20)))
                if not cuts and (end - sp["frm"]).days > 420 and rng.random() < 0.15:
                    cuts.append(_date_between(rng, sp["frm"] + dt.timedelta(days=120), end - dt.timedelta(days=60)))
            if not cuts:
                out.append(sp)
                continue
            frm = sp["frm"]
            for cut in sorted(cuts):
                out.append(dict(sp, frm=frm, to=cut - DAY))
                frm = cut
                p["owner"] = int(rng.integers(0, len(w.landlords)))
            out.append(dict(sp, frm=frm, owner=p["owner"], sold=True))
        f17 = p.get("f17")
        if p["built"] and f17 is not None and f17 > D0:
            out = [sp for sp in out if sp["to"] is None or sp["to"] >= f17]
            out[0] = dict(out[0], frm=max(out[0]["frm"], f17))
        p["spells"] = out
    for q in w.deleted:
        frm = dt.date(2012, 1, 1) + dt.timedelta(days=int(rng.integers(0, 1500)))
        q["spells"] = [dict(frm=frm, to=q["gone"] - DAY, who=("x", None), owner=int(rng.integers(0, len(w.landlords))))]


def M22_minus(rng, long=False):
    """the start of an empty spell running at 31 March 2022"""
    months = float(rng.exponential(20 if long else 9))
    return W.M22 - dt.timedelta(days=int(30 + months * 30.4))


def schemes(w, rng):
    """each employer's PAYE schemes in each March, the employees each paid, and the address each is held at: its own
    premises, its head office, a payroll bureau, its accountant, or for an employer with no rated premises a home"""
    occ = {"22": {}, "26": {}}
    for p in w.P:
        for yr in ("22", "26"):
            if p["o" + yr] is not None:
                occ[yr].setdefault(p["o" + yr], []).append(p)
    # the agents: office firms in the calibration pool given the agents' trades, accountants in the centres and
    # payroll bureaus on the business parks
    offices = [e for e, E in w.E.items() if E["kind"] == "nonretail" and E.get("cal")
               and any(p["d"] == "O1" for p in occ["22"].get(e, []) + occ["26"].get(e, []))]
    in_centre = [e for e in offices if any(p["centre"] is not None for p in occ["22"].get(e, []) + occ["26"].get(e, []))]
    out_centre = [e for e in offices if e not in in_centre]
    acc = [in_centre[i] for i in rng.choice(len(in_centre), size=150, replace=False)]
    bur = [out_centre[i] for i in rng.choice(len(out_centre), size=14, replace=False)]
    for e in acc:
        w.E[e].update(sic="69201", agent_kind="accountant")
    for e in bur:
        w.E[e].update(sic="69202", agent_kind="bureau")
    w.accountants, w.bureaus = acc, bur

    def agent_pc(kind, yr):
        pool = acc if kind == "accountant" else bur
        for _ in range(50):
            a = pool[int(rng.integers(0, len(pool)))]
            ps = occ[yr].get(a) or occ["26" if yr == "22" else "22"].get(a)
            if ps:
                return ps[0]["pc17" if yr == "22" else "pc23"], a
        raise RuntimeError("no agent premises")
    w.schemes = []
    used = set()

    def new_ref():
        while True:
            r = "%s%s%05d" % ("ABCDEFGHJKLMNPRSTW"[int(rng.integers(0, 18))], "ABCDEFGHJKLMNPRSTW"[int(rng.integers(0, 18))],
                              int(rng.integers(0, 100000)))
            if r not in used:
                used.add(r)
                return r
    for e, E in w.E.items():
        staff = {}
        for yr in ("22", "26"):
            s = sum(p["s" + yr] for p in occ[yr].get(e, []))
            own = E.get("own_staff")
            if own:
                s += own[0 if yr == "22" else 1]
            staff[yr] = s
        if staff["22"] == 0 and staff["26"] == 0 and not (E.get("nil22") or E.get("nil26")):
            continue
        allp = occ["22"].get(e, []) + occ["26"].get(e, [])
        r = rng.random()
        hold = {}
        for yr in ("22", "26"):
            mine = occ[yr].get(e, []) or allp
            key = "pc17" if yr == "22" else "pc23"
            if E["kind"] == "chain":
                hq = [p for p in mine if p["d"] == "O1"] or mine
                hold[yr] = (hq[0][key], None) if r > 0.25 else agent_pc("bureau", yr)
            elif E.get("public_body"):
                hold[yr] = ([p for p in mine if p["d"] == "O1"][0][key], None)
            elif mine:
                if r < 0.74:
                    hold[yr] = (mine[0][key], None)
                elif r < 0.9:
                    hold[yr] = agent_pc("accountant", yr)
                else:
                    hold[yr] = agent_pc("bureau", yr)
            else:
                if "home_pc" not in E:
                    E["home_pc"] = w.pc_unit(N.DISTRICTS[int(rng.choice(6, p=[0.36, 0.17, 0.14, 0.13, 0.11, 0.09]))][0])
                hold[yr] = (E["home_pc"], None) if r > 0.3 else agent_pc("accountant" if r < 0.22 else "bureau", yr)
        E["held"] = hold
        n = 2 if (E["kind"] == "chain" and rng.random() < 0.5) else 1
        refs = [new_ref() for _ in range(n)]
        refs26 = [new_ref() for _ in range(n)] if rng.random() < 0.04 else refs
        share0 = float(rng.uniform(0.7, 0.85))
        E["schemes"] = []
        for i in range(n):
            if n == 1:
                s22, s26 = staff["22"], staff["26"]
            elif i == 0:
                s22, s26 = int(round(staff["22"] * share0)), int(round(staff["26"] * share0))
            else:
                s22, s26 = staff["22"] - E["schemes"][0]["s22"], staff["26"] - E["schemes"][0]["s26"]
            sc = dict(eid=e, ref22=refs[i], ref26=refs26[i], s22=s22, s26=s26, office="961" if rng.random() < 0.7 else "962",
                      pay="weekly" if (n == 2 and i == 0) else "monthly",
                      in22=s22 > 0 or bool(E.get("nil22")), in26=s26 > 0 or bool(E.get("nil26")))
            E["schemes"].append(sc)
            w.schemes.append(sc)
    # the centre each employer's PAYE address sits in, March by March (the postcode route)
    unit_centre = {}
    for k, units in w.centre_units.items():
        for pc, st in units:
            unit_centre[pc] = k
            if pc in w.recoded:
                unit_centre[w.recoded[pc]] = k
    w.unit_centre = unit_centre
    for e, E in w.E.items():
        if "held" in E:
            E["hq22"] = unit_centre.get(E["held"]["22"][0])
            E["hq26"] = unit_centre.get(E["held"]["26"][0])


def build(w, seed=W.SEED + 2):
    rng = np.random.default_rng(seed)
    w.tl_seed = seed
    postcodes(w, rng)
    addresses(w, rng)
    recode(w, rng)
    lists(w, rng)
    parties(w, rng)
    spells(w, rng)
    schemes(w, rng)
    return w
