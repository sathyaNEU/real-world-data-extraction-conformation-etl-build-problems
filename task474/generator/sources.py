"""The clean truth: every station's and every link's daily traffic by vehicle class over the program year. Nothing
here knows about files, layouts or mess."""
import numpy as np

import world as W

ND = len(W.DAYS)
DOWS = np.array([d.weekday() for d in W.DAYS])
MONTHS = np.array([d.month for d in W.DAYS])


def daily(rng, aadt, su, cu, noise=(.045, .07, .075)):
    """{class: daily volumes over the program year}, each class's mean equal to its share of aadt."""
    shares = {"P": 1 - su - cu, "SU": su, "CU": cu}
    out = {}
    for i, c in enumerate(W.CLASSES):
        dow = np.array(W.DOW[c]) * (1 + rng.normal(0, .025, 7))
        mon = {m: v * (1 + rng.normal(0, .015)) for m, v in W.MON[c].items()}
        v = dow[DOWS] * np.array([mon[m] for m in MONTHS]) * rng.lognormal(0, noise[i], ND)
        for k, d in enumerate(W.DAYS):
            if d in W.HOLIDAYS:
                v[k] *= W.HOLIDAYS[d][0 if c == "P" else 1]
        out[c] = v / v.mean() * aadt * shares[c]
    return out


def world(rng):
    st = {s: daily(rng, a, su, cu) for s, (_, _, a, su, cu, _) in W.STATIONS.items()}
    ln = {k: daily(rng, a, su, cu) for k, (_, _, a, su, cu) in W.LINKS.items()}
    return dict(stations=st, links=ln)


def nox_per_mile(byclass):
    """tonnes of NOx per mile over the program year from {class: AADT}."""
    return sum(byclass[c] * ND * W.EF[c] for c in W.CLASSES) / 1e6


def truth(x):
    return {k: nox_per_mile({c: v[c].mean() for c in W.CLASSES}) for k, v in x["links"].items()}


def gate_world(rng):
    """The drayage trucks, their tags over the year, and every truck visit to a terminal: truck, terminal, local time
    in and out, and the container transactions it carried out (one, or two for a dual transaction)."""
    import datetime as dt
    trucks = []
    tag_pool = rng.choice(np.arange(3000000, 3999999), size=3 * W.N_TRUCKS, replace=False)
    nxt = 0
    for i in range(W.N_TRUCKS):
        my = int(rng.choice(np.arange(2008, 2025), p=np.linspace(.4, 1.6, 17) / np.linspace(.4, 1.6, 17).sum()))
        trucks.append(dict(truck="DT%05d" % (10000 + i * 7 + int(rng.integers(0, 7))), model_year=my,
                           rate=float(rng.gamma(2.0, .25)), pref=rng.dirichlet([.9, .75, .5]),
                           active=(W.DAYS[0], W.DAYS[-1])))
    # some trucks retire during the year and their tags go to a new truck; some get a replacement tag
    tags = []                       # (tag, truck, start, end)
    for t in trucks:
        tags.append([int(tag_pool[nxt]), t["truck"], W.DAYS[0], W.DAYS[-1]])
        t["tag_rows"] = [len(tags) - 1]
        nxt += 1
    extra = []
    for t in trucks:
        u = rng.random()
        if u < .05:                 # retires; its tag is reissued to a newly registered truck
            d = W.DAYS[int(rng.integers(60, 300))]
            t["active"] = (W.DAYS[0], d)
            row = tags[t["tag_rows"][0]]
            row[3] = d
            nt = dict(truck="DT%05d" % (16000 + len(extra) * 11), model_year=int(rng.integers(2019, 2026)),
                      rate=float(rng.gamma(2.0, .25)), pref=rng.dirichlet([.9, .75, .5]),
                      active=(d + dt.timedelta(int(rng.integers(3, 20))), W.DAYS[-1]))
            tags.append([row[0], nt["truck"], nt["active"][0], W.DAYS[-1]])
            nt["tag_rows"] = [len(tags) - 1]
            extra.append(nt)
        elif u < .11:               # damaged tag replaced
            d = W.DAYS[int(rng.integers(30, 330))]
            tags[t["tag_rows"][0]][3] = d - dt.timedelta(1)
            tags.append([int(tag_pool[nxt]), t["truck"], d, W.DAYS[-1]])
            t["tag_rows"].append(len(tags) - 1)
            nxt += 1
    trucks += extra
    terms = list(W.TERMINALS)
    visits = []
    for t in trucks:
        for d in W.DAYS:
            if not (t["active"][0] <= d <= t["active"][1]) or d.weekday() == 6:
                continue
            lam = t["rate"] * (.35 if d.weekday() == 5 else 1.0)
            n = int(rng.poisson(lam))
            clock = dt.datetime.combine(d, dt.time(5, 30)) + dt.timedelta(minutes=int(rng.integers(0, 240)))
            for _ in range(n):
                term = terms[int(rng.choice(3, p=t["pref"]))]
                q = (d.month - 10) % 12 // 3
                med = W.TERMINALS[term][2] * (1.0 + .08 * q if term == "B30" else 1.0 - .03 * q)
                turn = float(rng.lognormal(np.log(med), .42))
                dual = rng.random() < .27
                if dual:
                    turn *= 1.35
                tin = clock + dt.timedelta(seconds=int(rng.integers(0, 3600)))
                tout = tin + dt.timedelta(seconds=int(turn * 60))
                ramp = None
                if term == "B40" and not dual and rng.random() < .26:
                    # the truck runs to the on-dock rail ramp and back inside its stay
                    a = tin + dt.timedelta(seconds=int((tout - tin).total_seconds() * float(rng.uniform(.25, .55))))
                    b = a + dt.timedelta(minutes=int(rng.integers(8, 26)))
                    tout = tout + (b - a)
                    ramp = (a, b)
                tag = next(tags[r][0] for r in t["tag_rows"] if tags[r][2] <= d <= tags[r][3])
                visits.append(dict(truck=t["truck"], tag=tag, term=term, tin=tin, tout=tout, dual=dual, ramp=ramp))
                clock = tout + dt.timedelta(minutes=int(rng.integers(35, 160)))
                if clock.hour >= 20 or clock.date() != d:
                    break
    return dict(trucks=trucks, tags=tags, visits=visits)


def gate_truth(g):
    """{(terminal, quarter): (visits, distinct trucks, mean turn minutes)}, a visit in the quarter of its local gate-in
    date."""
    out = {}
    for v in g["visits"]:
        q = (v["tin"].month - 10) % 12 // 3 + 1
        k = (v["term"], q)
        o = out.setdefault(k, [0, set(), 0.0])
        o[0] += 1
        o[1].add(v["truck"])
        o[2] += (v["tout"] - v["tin"]).total_seconds() / 60
    return {k: (o[0], len(o[1]), o[2] / o[0]) for k, o in out.items()}
