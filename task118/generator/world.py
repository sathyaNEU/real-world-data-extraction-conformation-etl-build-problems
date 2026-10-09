"""Builds the world in memory: staff, articles, the test archive and the spine allocation."""
import datetime as dt
import hashlib

import numpy as np
from faker import Faker

import params as P
import archive as AR
import spine as SP

PERSONAS = {
    "Lisa Jennings": ("EDT", "Editor-in-chief", "Sydney", dt.date(2019, 3, 4)),
    "Corey Cox": ("EDT", "Managing editor", "Sydney", dt.date(2020, 8, 17)),
    "Kayla Torres": ("AUD", "Head of audience", "Sydney", dt.date(2021, 2, 1)),
    "Nina Franklin": ("AUD-EXP", "Experimentation lead", "Melbourne", dt.date(2019, 6, 10)),
    "Jason Anderson": ("AUD-HS", "Headline squad lead", "Sydney", dt.date(2018, 11, 5)),
    "Natalie Benjamin": ("AUD-DATA", "Audience data engineer", "Brisbane", dt.date(2022, 4, 19)),
}
TEAM_NAME = {"EDT": "Editorial leadership", "AUD": "Audience", "AUD-EXP": "Experimentation",
             "AUD-HS": "Headline squad", "AUD-DATA": "Audience data", "STD": "Standards"}
for _d in P.DESKS:
    TEAM_NAME[_d[0]] = _d[1] + " desk"
DESK_STAFF = {  # editing staff who can run tests (editor, deputies, senior producers, producers), reporters
    "POL-N": (1, 2, 3, 6, 14), "BUS-N": (1, 1, 3, 5, 11), "SPT-N": (1, 2, 3, 7, 15), "CUL-N": (1, 1, 1, 3, 7),
    "POL-M": (1, 1, 1, 2, 5), "SPT-M": (1, 1, 1, 3, 6), "LOC-M": (1, 1, 2, 5, 10),
    "GAM-A": (1, 0, 1, 2, 0), "PZL-A": (1, 0, 1, 3, 0), "RCP-A": (1, 1, 1, 2, 1), "WEL-A": (1, 0, 1, 2, 1)}
BASE = {"POL-N": "Canberra", "BUS-N": "Sydney", "SPT-N": "Melbourne", "CUL-N": "Melbourne", "POL-M": "Brisbane",
        "SPT-M": "Brisbane", "LOC-M": "Brisbane", "GAM-A": "Sydney", "PZL-A": "Sydney", "RCP-A": "Sydney",
        "WEL-A": "Sydney"}
SQUAD_HISTORY = [  # role, start, end (None = current); Jason Anderson is the persona lead
    ("Headline editor", dt.date(2018, 11, 19), dt.date(2021, 3, 26)),
    ("Headline editor", dt.date(2019, 1, 14), dt.date(2023, 7, 14)),
    ("Data analyst", dt.date(2018, 12, 3), dt.date(2020, 10, 2)),
    ("Producer", dt.date(2019, 2, 4), dt.date(2022, 11, 25)),
    ("Data analyst", dt.date(2020, 10, 26), dt.date(2024, 9, 13)),
    ("Headline editor", dt.date(2021, 4, 12), None),
    ("Producer", dt.date(2023, 1, 16), dt.date(2025, 6, 20)),
    ("Headline editor", dt.date(2023, 8, 7), None),
    ("Headline editor", dt.date(2024, 2, 12), None),
    ("Data analyst", dt.date(2024, 10, 8), None),
    ("Producer", dt.date(2025, 7, 21), None),
]


def sha(s, n=12):
    return hashlib.sha1(s.encode()).hexdigest()[:n]


class World:
    pass


def make_staff(W):
    fk = Faker("en_AU")
    fk.seed_instance(P.SEED)
    rng = AR.rng_for(10)
    used = set(PERSONAS)
    persona_first = {n.split()[0] for n in PERSONAS}
    persona_last = {n.split()[-1] for n in PERSONAS}

    def name():
        while True:
            nm = "%s %s" % (fk.first_name(), fk.last_name())
            f, l = nm.split()[0], nm.split()[-1]
            if nm not in used and f not in persona_first and l not in persona_last and len(nm.split()) == 2:
                used.add(nm)
                return nm

    ids = set()

    def sid(start):
        block = 10000 + (start.year - 2010) * 650
        while True:
            v = block + int(rng.integers(0, 640))
            if v not in ids:
                ids.add(v)
                return "BN%05d" % v

    rows = []

    def add(nm, team, role, base, start, end=None):
        rows.append(dict(staff_id=sid(start), full_name=nm, team_code=team, team=TEAM_NAME[team], role=role,
                         base=base, start_date=start, end_date=end))
        return rows[-1]

    for nm, (team, role, base, start) in PERSONAS.items():
        add(nm, team, role, base, start)
    for role, s, e in SQUAD_HISTORY:
        add(name(), "AUD-HS", role, "Sydney", s, e)
    for team, roles in [("AUD", ["Audience editor", "Audience editor", "Social editor", "Newsletter editor"]),
                        ("AUD-DATA", ["Analytics engineer", "Data analyst", "Data analyst"]),
                        ("AUD-EXP", ["Experimentation analyst", "Experimentation analyst"]),
                        ("STD", ["Standards editor", "Standards producer", "Readers' editor"]),
                        ("EDT", ["Deputy editor", "Executive producer"])]:
        for r in roles:
            start = dt.date(2016, 1, 4) + dt.timedelta(days=int(rng.integers(0, 3300)))
            add(name(), team, r, "Sydney" if team != "AUD-DATA" else ["Sydney", "Brisbane"][int(rng.integers(2))], start)
    W.testers = {}
    for desk, (ed, dep, sp, prod, rep) in DESK_STAFF.items():
        roles = ["Desk editor"] * ed + ["Deputy editor"] * dep + ["Senior producer"] * sp + ["Producer"] * prod + \
                ["Reporter"] * rep
        W.testers[desk] = []
        for r in roles:
            start = dt.date(2014, 2, 3) + dt.timedelta(days=int(rng.integers(0, 4100)))
            if start > dt.date(2025, 9, 1):
                start = start - dt.timedelta(days=700)
            leaver = desk in P.WEB and r in ("Producer", "Senior producer", "Reporter") and rng.random() < 0.16
            end = None
            if leaver:
                end = P.WINDOW_START + dt.timedelta(days=int(rng.integers(40, 330)))
            row = add(name(), desk, r, BASE[desk], start, end)
            if r != "Reporter":
                W.testers[desk].append(row)
            if leaver and r != "Reporter":
                rs = end + dt.timedelta(days=int(rng.integers(14, 60)))
                if rs < P.WINDOW_END - dt.timedelta(days=20):
                    W.testers[desk].append(add(name(), desk, r, BASE[desk], rs))
        # earlier leavers, before the window, so the list carries its history
        for _ in range(int(rng.integers(1, 4))):
            end = dt.date(2019, 1, 18) + dt.timedelta(days=int(rng.integers(0, 2400)))
            start = end - dt.timedelta(days=int(rng.integers(300, 2500)))
            add(name(), desk, ["Producer", "Reporter"][int(rng.integers(2))], BASE[desk], start, end)
    W.staff = sorted(rows, key=lambda r: r["staff_id"])
    W.squad = [r for r in W.staff if r["team_code"] == "AUD-HS"]


def active(rows, when):
    return [r for r in rows if r["start_date"] <= when and (r["end_date"] is None or r["end_date"] >= when)]


def make_articles(W):
    W.art = {d: SP.build_articles(d) for d in P.DESK}
    for d, A in W.art.items():
        rng = AR.rng_for(300 + list(P.DESK).index(d))
        SP.scale_tested(A, rng)
        SP.build_mixes(A, rng)
    # article ids: web desks share one sequence in publication order; app items their own block
    rng = AR.rng_for(20)
    allpub = sorted((A.pub[i], d, i) for d, A in W.art.items() if d in P.WEB for i in range(len(A.pub)))
    nxt = 1184216
    for d in P.WEB:
        W.art[d].ids = np.zeros(len(W.art[d].pub), np.int64)
    for m, d, i in allpub:
        W.art[d].ids[i] = nxt
        nxt += int(rng.integers(1, 4))
    used = set()
    for d in P.WEB:
        A = W.art[d]
        start = SP.minutes(P.WINDOW_START)
        A.old_ids = np.zeros(len(A.old_pub), np.int64)
        for i, m in enumerate(A.old_pub):
            back_days = (start - m) / SP.DAY
            v = 1184216 - int(back_days * 131) - int(rng.integers(0, 120))
            while v in used:
                v -= 1
            used.add(v)
            A.old_ids[i] = v
    nxt = 30418820
    for d in P.APP:
        A = W.art[d]
        A.ids = np.zeros(len(A.pub), np.int64)
        A.old_ids = np.zeros(len(A.old_pub), np.int64)
    app_pub = sorted((A.pub[i], d, i) for d, A in W.art.items() if d in P.APP for i in range(len(A.pub)))
    for m, d, i in app_pub:
        W.art[d].ids[i] = nxt
        nxt += int(rng.integers(1, 3))
    for d in P.APP:
        A = W.art[d]
        for i, m in enumerate(A.old_pub):
            v = 30418820 - int((SP.minutes(P.WINDOW_START) - m) / SP.DAY * 9) - int(rng.integers(0, 8))
            while v in used:
                v -= 1
            used.add(v)
            A.old_ids[i] = v


def make_tests(W):
    """Simulate every concluded test, pair web tests with tested articles, set times and owners."""
    W.tests = []          # dicts: test_id, engine, desk, article_id, owner, start(UTC), end(UTC), ns, cs, ship, group
    for d in P.WEB:
        c = P.WEB_TESTS[d]
        inst = P.DESK[d][5]
        sub = P.CUL_SUBSEED if d == "CUL-N" else 0
        sim = AR.simulate_tests(AR.rng_for(100 + P.WEB.index(d), sub), c["n"], c["kp"], c["npk"], c["ctr"], P.GATE[inst])
        A = W.art[d]
        rng = AR.rng_for(400 + P.WEB.index(d))
        tidx = np.where(A.tested)[0]
        early = A.w[tidx] * (A.src[tidx, :5] * A.age[tidx, :5, 0]).sum(1)
        a_order = tidx[np.argsort(-(early * rng.lognormal(0, 0.15, len(tidx))), kind="stable")]
        t_order = np.argsort(-np.array([t["cs"].sum() for t in sim]), kind="stable")
        for rank, ti in enumerate(t_order):
            t = sim[ti]
            ai = a_order[rank]
            pub_aest = SP.to_dt(A.pub[ai])
            start = pub_aest - P.AEST + dt.timedelta(minutes=int(rng.integers(4, 19)))
            end = start + dt.timedelta(minutes=int(rng.integers(c["dur"][0], c["dur"][1] + 1)))
            owners = active(W.testers[d], pub_aest.date())
            prob = np.array([3.0 if r["role"] == "Producer" else 2.0 if r["role"] == "Senior producer" else 1.0
                             for r in owners])
            owner = owners[int(rng.choice(len(owners), p=prob / prob.sum()))]
            W.tests.append(dict(engine="web", desk=d, art_index=int(ai), article_id=int(A.ids[ai]),
                                owner=owner["staff_id"], start=start, end=end, group="web", **t))
    # the squad: seven closed embeddings and the open one
    W.emb_tests = {}
    rng = AR.rng_for(30)
    used = set(int(x) for d in P.APP for x in W.art[d].old_ids) | set(int(x) for d in P.APP for x in W.art[d].ids)
    for e in P.EMBEDDINGS:
        sim = AR.simulate_tests(AR.rng_for(900 + e["no"], P.EMBED_SUBSEED[e["no"]]), e["n"], P.APP_KP, e["npk"],
                                P.APP_CTR, P.GATE["app"])
        y = e["year"]
        A = W.art[e["desk"]]
        tidx = np.where(A.tested)[0] if e["no"] == 7 else np.array([], int)
        n_in = len(tidx)
        last = 360 if y < 2025 else (dt.date(2025, 9, 30) - dt.date(2025, 1, 1)).days
        days = sorted(rng.choice(np.arange(5, last), size=len(sim) - n_in, replace=False))
        by_size = np.argsort(-np.array([t["cs"].sum() for t in sim]), kind="stable")
        in_tests = list(by_size[:n_in])
        if n_in:
            early = A.w[tidx] * (A.src[tidx, :5] * A.age[tidx, :5, 0]).sum(1)
            items = list(tidx[np.argsort(-early, kind="stable")])
        out = []
        k_out = 0
        for k, t in enumerate(sim):
            if k in in_tests:
                ai = items[in_tests.index(k)]
                pub_aest = SP.to_dt(A.pub[ai])
                start = pub_aest - P.AEST + dt.timedelta(minutes=int(rng.integers(3, 15)))
                art_index, aid = int(ai), int(A.ids[ai])
                when = pub_aest.date()
            else:
                day = dt.date(y, 1, 1) + dt.timedelta(days=int(days[k_out]))
                k_out += 1
                start = dt.datetime(day.year, day.month, day.day, int(rng.integers(19, 23)), int(rng.integers(0, 60))) \
                    - dt.timedelta(days=1)
                aid = 30418820 - int((dt.date(2025, 10, 1) - day).days * 9) - int(rng.integers(0, 9))
                while aid in used:
                    aid -= 1
                art_index, when = -1, day
            used.add(aid)
            end = start + dt.timedelta(minutes=int(rng.integers(25, 70)))
            owners = [r for r in active(W.squad, when) if r["role"] != "Data analyst"]
            owner = owners[int(rng.integers(len(owners)))]
            rec = dict(engine="app", desk=e["desk"], art_index=art_index, article_id=aid, owner=owner["staff_id"],
                       start=start, end=end, group="emb%d" % e["no"], **t)
            out.append(rec)
            W.tests.append(rec)
        W.emb_tests[e["no"]] = out
    o = P.OPEN_EMBEDDING
    sim = AR.simulate_tests(AR.rng_for(990, 0), o["n"], P.APP_KP, o["npk"], P.APP_CTR, P.GATE["app"])
    A = W.art[o["desk"]]
    tidx = np.where(A.tested)[0]
    rng2 = AR.rng_for(31)
    for k, t in enumerate(sim):
        ai = tidx[k]
        pub_aest = SP.to_dt(A.pub[ai])
        start = pub_aest - P.AEST + dt.timedelta(minutes=int(rng2.integers(3, 15)))
        end = start + dt.timedelta(minutes=int(rng2.integers(25, 70)))
        owners = [r for r in active(W.squad, pub_aest.date()) if r["role"] != "Data analyst"]
        owner = owners[int(rng2.integers(len(owners)))]
        W.tests.append(dict(engine="app", desk=o["desk"], art_index=int(ai), article_id=int(A.ids[ai]),
                            owner=owner["staff_id"], start=start, end=end, group="open", **t))
    W.tests.sort(key=lambda t: t["start"])
    # ids: app engine APP-<year>-<seq>, web tool W<yymm>-<seq>
    seq = {}
    rng3 = AR.rng_for(40)
    for t in W.tests:
        if t["engine"] == "app":
            key = ("app", t["start"].year)
            seq[key] = seq.get(key, 0) + int(rng3.integers(1, 4))
            t["test_id"] = "APP-%d-%05d" % (t["start"].year, seq[key])
        else:
            st = t["start"] + P.AEST
            key = ("web", st.year, st.month)
            seq[key] = seq.get(key, 0) + 1
            t["test_id"] = "W%02d%02d-%04d" % (st.year % 100, st.month, seq[key])


def fit(W):
    L, S2 = AR.pooled(W.tests)
    W.prior_mom = AR.prior_mom(L, S2)
    W.prior = AR.prior_ml(L, S2, W.prior_mom)        # the golden prior: maximum likelihood on every package
    W.prior_dl = AR.prior_dl(L, S2)
    W.n_packages = len(L)
    W.raw, W.shr = {}, {}
    for d in P.WEB:
        ts = [t for t in W.tests if t["desk"] == d]
        W.raw[d] = AR.desk_lift(ts, shrink=False)
        W.shr[d] = AR.desk_lift(ts, W.prior)


def solve_totals(W):
    W.total = {}
    for d in P.DESK:
        A = W.art[d]
        win, old = SP.expected_fractions(A)
        if d in P.F_TARGET:
            u = win[~A.tested, :5, :].sum() + old[:, :5, :].sum()
            W.total[d] = int(round(P.F_TARGET[d] / (W.shr[d] * u)))
        else:
            W.total[d] = int(round(P.P_GUIDE[d] * (1 + AR.rng_for(50, list(P.DESK).index(d)).uniform(-0.004, 0.004))))
        SP.allocate(A, W.total[d])


def build():
    W = World()
    make_staff(W)
    make_articles(W)
    make_tests(W)
    fit(W)
    solve_totals(W)
    return W
