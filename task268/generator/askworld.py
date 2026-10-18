"""The two ask files: the buyers' sales notes for 2026 as the organisation's landings system exports them, and the
organisation's 2026 haddock quota ledger. Both are cut from the members' own trips (askworld never touches the
survey), with their own stream of chance.

Sales notes: every member landing is sold at its port's auction or to merchants there, lot by lot; most landings in
one session, some over two, each buyer issuing a note per session. When a buyer corrects a price after the sale its
system issues a fresh note under a new number, and the export keeps both. Non-members' landings at the same ports are in
the export too. Quota ledger: each licence's allocation on 1 January and each pool's as well; the 2025 carry-in and
three pools' swaps with other organisations, booked to the pool; leases between licences; each licence's landings
for a month as one entry dated the month's last day, posted when the month's statement comes in."""
import datetime as dt
import math

import numpy as np

import common as K
import world as W

GRADE_PRICE = {1: 2.95, 2: 2.62, 3: 2.18, 4: 1.71}
OTHER = {"COD": (3.35, "GUT", 1.17), "WHG": (1.62, "GUT", 1.18), "POK": (1.38, "GUT", 1.19),
         "MON": (5.20, "TAL", 3.00), "LEM": (6.10, "WHL", 1.00), "HKE": (2.45, "GUT", 1.11)}
BUYERS = {
    "Eastquay": [("RB4127", "Eastquay Fish Selling Co"), ("RB4185", "Quayside Seafoods Ltd"), ("RB4203", "Harbour Fresh Ltd")],
    "Kelmoor": [("RB3361", "Kelmoor Fishmarket Ltd"), ("RB3390", "North Shore Seafoods Ltd"), ("RB3412", "Seaward Foods Ltd")],
    "Tolsetter": [("RB5018", "Tolsetter Auction Co"), ("RB5046", "Tidewater Seafoods Ltd"), ("RB5077", "Tolsetter Fish Merchants Ltd")],
    "Haldness": [("RB2274", "Haldness Fish Sales Ltd"), ("RB2290", "Pierhead Seafoods Ltd"), ("RB2311", "Haldness Smokehouse Ltd")],
}
EXPORT_FROM, EXPORT_TO = dt.date(2026, 1, 1), dt.date(2026, 11, 2)


def _rng(T, k):
    return np.random.default_rng([T["seed"], 100 + k])


def member_landings(T):
    """Each member trip that ends from 27 December 2025 to 31 October 2026 lands its catch: the port, the boat's port
    letters that day, and the landed weights by species and presentation."""
    from records import landing_port
    V = {v["rss"]: v for v in T["vessels"]}
    out = []
    for t in T["trips"]:
        if not (dt.date(2025, 12, 27) <= t["end"] <= W.ELOG_END):
            continue
        v = V[t["vessel"]]
        hs = [T["hauls"][i] for i in t["hauls"]]
        live = {"HAD": sum(h["had"] for h in hs), "COD": sum(h["cod"] for h in hs), "WHG": sum(h["whg"] for h in hs),
                "POK": sum(h["pok"] for h in hs)}
        out.append(dict(trip=t["id"], rss=v["rss"], pln=W.pln_on(v, t["end"]), port=landing_port(T, t, 17),
                        date=t["end"], whole=v["pool"] == "I", live=live, member=True))
    return out


def other_landings(T, rng, members):
    """Landings at the same ports by boats outside the organisation, scaled on the members' own landings."""
    used = {pln for v in T["vessels"] for pln, *_ in v["history"]}
    boats = []
    letters = [K.PORT_LETTERS[p] for p in K.PORT_NAMES] + ["BK", "WY"]
    while len(boats) < 26:
        pln = "%s %d" % (letters[int(rng.integers(len(letters)))], int(rng.integers(5, 520)))
        if pln not in used:
            used.add(pln)
            boats.append((pln, K.PORT_NAMES[len(boats) % 4]))
    out = []
    for k in range(int(len(members) * 0.85)):
        pln, home = boats[int(rng.integers(len(boats)))]
        ref = members[int(rng.integers(len(members)))]
        day = dt.date(2025, 12, 28) + dt.timedelta(days=int(rng.integers(0, 308)))
        f = float(np.exp(rng.normal(-0.25, 0.45)))
        port = home if rng.random() < 0.85 else K.PORT_NAMES[int(rng.integers(4))]
        out.append(dict(trip=None, rss=None, pln=pln, port=port, date=day, whole=rng.random() < 0.2,
                        live={s: x * f for s, x in ref["live"].items()}, member=False))
    return out


def _split(total, rng, lo=3, hi=16):
    lots = []
    while total > 0:
        n = min(total, int(rng.integers(lo, hi + 1)))
        if 0 < total - n < lo:
            n = total
        lots.append(n)
        total -= n
    return lots


def sales_notes(T):
    """Every line of every note issued from 1 January to 2 November 2026, as dicts; and the re-issued pairs."""
    rng = _rng(T, 1)
    mem = member_landings(T)
    allx = mem + other_landings(T, rng, mem)
    allx.sort(key=lambda x: (x["date"], x["port"], x["pln"]))
    day_factor = {}
    notes = []
    for x in allx:
        if x["date"] not in day_factor:
            day_factor[x["date"]] = float(np.exp(rng.normal(0, 0.07)))
        mkt = day_factor[x["date"]] * (1 + 0.08 * math.cos(2 * math.pi * (x["date"].month - 1) / 12))
        lots = []
        pres = "WHL" if x["whole"] else "GUT"
        w = x["live"]["HAD"] * (1.0 if x["whole"] else 1 / 1.17) * float(np.exp(rng.normal(0, 0.02)))
        boxes = max(1, int(round(w / 40)))
        shares = rng.dirichlet([2.5, 6, 7.5, 4])
        per = np.floor(shares * boxes).astype(int)
        for i in np.argsort(-(shares * boxes - per))[: boxes - per.sum()]:
            per[i] += 1
        for g in range(4):
            for n in _split(int(per[g]), rng, 6, 26):
                lots.append(["HAD", pres, str(g + 1), n, 40 * n, round(GRADE_PRICE[g + 1] * mkt * float(np.exp(rng.normal(0, 0.05))), 2)])
        for sp, (price, p2, fac) in OTHER.items():
            if sp in x["live"]:
                kg = x["live"][sp] / fac * float(np.exp(rng.normal(0, 0.03)))
            elif rng.random() < 0.35:
                kg = float(rng.gamma(1.5, 60.0))
            else:
                continue
            nb = max(1, int(round(kg / 40)))
            for n in _split(nb, rng, 4, 18):
                lots.append([sp, "WHL" if (p2 == "GUT" and x["whole"]) else p2, "", n, 40 * n,
                             round(price * mkt * float(np.exp(rng.normal(0, 0.06))), 2)])
        two = rng.random() < 0.09
        buyers = BUYERS[x["port"]]
        groups = {}
        for k, lot in enumerate(lots):
            b = buyers[int(rng.choice(3, p=[0.5, 0.3, 0.2]))]
            sess = 2 if (two and k % 2 == 1) else 1
            groups.setdefault((b, sess), []).append(lot)
        for (b, sess), ls in sorted(groups.items(), key=lambda kv: (kv[0][1], kv[0][0][0])):
            issued = x["date"] + dt.timedelta(days=(0 if b == buyers[0] else 1) + (sess - 1))
            notes.append(dict(buyer=b, issued=issued, port=x["port"], landing=x["date"], pln=x["pln"],
                              member=x["member"], rss=x["rss"], lines=ls, session=sess, reissue_of=None))
    # corrected notes: a fresh note with the same lots at the corrected prices; the first stays in the export
    out = []
    for port in K.PORT_NAMES:
        cand = [n for n in notes if n["port"] == port and n["member"] and n["landing"].month <= 9
                and n["landing"].year == 2026 and sum(1 for l in n["lines"] if l[0] == "HAD") >= 2]
        k = 2 + int(rng.integers(0, 2))
        for j in rng.choice(len(cand), size=k, replace=False):
            out.append(cand[int(j)])
    cand = [n for n in notes if not n["member"] and n["landing"].year == 2026 and n["landing"].month <= 9
            and any(l[0] == "HAD" for l in n["lines"])]
    for j in rng.choice(len(cand), size=3, replace=False):
        out.append(cand[int(j)])
    for n in out:
        lines = [list(l) for l in n["lines"]]
        had = [i for i, l in enumerate(lines) if l[0] == "HAD"]
        for i in rng.choice(had, size=min(len(had), 1 + int(rng.random() < 0.4)), replace=False):
            lines[int(i)][5] = round(lines[int(i)][5] + float(rng.choice([-1, 1])) * float(rng.uniform(0.05, 0.22)), 2)
        notes.append(dict(n, lines=lines, issued=n["issued"] + dt.timedelta(days=int(rng.integers(2, 10))),
                          reissue_of=id(n)))
    notes = [n for n in notes if EXPORT_FROM <= n["issued"] <= EXPORT_TO]
    # note numbers: each buyer's own sequence in the order it issued them
    seq = {}
    for n in sorted(notes, key=lambda n: (n["issued"], n["landing"], n["pln"], n["session"], n["reissue_of"] is not None)):
        code = n["buyer"][0]
        seq.setdefault(code, int(rng.integers(1200, 8800)))
        seq[code] += 1
        n["no"] = "%s-%06d" % (code[2:], seq[code])
    ids = {id(n): n["no"] for n in notes}
    for n in notes:
        n["replaces"] = ids.get(n["reissue_of"]) if n["reissue_of"] else None
    return notes


def note_rows(notes):
    rows = []
    for n in sorted(notes, key=lambda n: (n["issued"], n["no"])):
        for k, (sp, pres, grade, boxes, kg, price) in enumerate(n["lines"], 1):
            rows.append([n["no"], n["buyer"][0], n["buyer"][1], n["issued"].isoformat(), n["port"], n["landing"].isoformat(),
                         n["pln"], k, sp, pres, grade, boxes, kg, "%.2f" % price, "%.2f" % round(kg * price, 2)])
    return rows


# ---------------------------------------------------------------------------------------------- the quota ledger
def licences(T):
    rng = _rng(T, 2)
    out = []
    used = set()
    for v in T["vessels"]:
        while True:
            no = "%05d" % int(rng.integers(20100, 48999))
            if no not in used:
                used.add(no)
                break
        out.append(dict(no=no, holder=v["name"] + " Fishing Ltd", vessel=v["rss"], pool=v["pool"]))
    for holder, pool in (("Holdfast Fishing Ltd", "N"), ("Kelmoor Quota Holdings Ltd", "E"), ("Steadfast Partners", "S")):
        while True:
            no = "%05d" % int(rng.integers(20100, 48999))
            if no not in used:
                used.add(no)
                break
        out.append(dict(no=no, holder=holder, vessel=None, pool=pool))
    return out


def ledger(T, notes, lic):
    """The 2026 haddock ledger as exported on 3 November 2026."""
    rng = _rng(T, 3)
    by_rss = {l["vessel"]: l for l in lic if l["vessel"]}
    # each licence's landings by month, in live weight, from its notes (each landing once) plus landings elsewhere
    land = {}
    seen = set()
    for n in notes:
        if not n["member"] or n["landing"].year != 2026 or n["replaces"]:
            continue
        key = (n["rss"], n["landing"], n["buyer"][0], n["session"])
        if key in seen:
            continue
        seen.add(key)
        for sp, pres, grade, boxes, kg, price in n["lines"]:
            if sp == "HAD":
                f = 1.0 if pres == "WHL" else 1.17
                land[(n["rss"], n["landing"].month)] = land.get((n["rss"], n["landing"].month), 0.0) + kg * f / 1000
    year_use = {}
    for (rss, m), t in land.items():
        year_use[rss] = year_use.get(rss, 0.0) + t
    rows = []

    def add(eff, posted, pool, licence, typ, tonnes, ref):
        rows.append([eff, posted, pool, licence, typ, round(tonnes, 3), ref])

    alloc = {}
    for l in lic:
        if l["vessel"]:
            base = year_use.get(l["vessel"], 60.0) * 12 / 10 * float(rng.uniform(1.12, 1.42))
        else:
            base = float(rng.uniform(38, 92))
        alloc[l["no"]] = round(base, 1)
    jan1, posted1 = dt.date(2026, 1, 1), dt.date(2026, 1, 6)
    for pool in K.POOL_CODES:
        ls = sorted((l for l in lic if l["pool"] == pool), key=lambda l: l["no"])
        for l in ls:
            add(jan1, posted1, pool, l["no"], "allocation", alloc[l["no"]], "2026 allocation")
        add(jan1, posted1 + dt.timedelta(days=1), pool, "", "allocation", sum(alloc[l["no"]] for l in ls), "2026 allocation")
    for pool in K.POOL_CODES:
        tot = sum(alloc[l["no"]] for l in lic if l["pool"] == pool)
        d = dt.date(2026, 2, int(rng.integers(9, 27)))
        add(d, d + dt.timedelta(days=int(rng.integers(0, 4))), pool, "", "carry_in",
            round(tot * float(rng.uniform(0.035, 0.075)), 1), "Banked from 2025")
    swaps = [("N", dt.date(2026, 5, 14), 24.0, "Swap SW26/03 with Ardvoran FPO"),
             ("T", dt.date(2026, 7, 2), -11.5, "Swap SW26/07 with Brimwell FPO"),
             ("I", dt.date(2026, 8, 19), 7.5, "Swap SW26/09 with Ardvoran FPO")]
    for pool, d, t, ref in swaps:
        add(d, d + dt.timedelta(days=int(rng.integers(1, 5))), pool, "", "swap", t, ref)
    # leases between licences: (from, to, tonnes, effective)
    vessel_lic = [l for l in lic if l["vessel"]]
    leases = []
    months = [3, 4, 4, 5, 6, 6, 7, 8, 8, 9]
    for k, m in enumerate(months, 1):
        a, b = rng.choice(len(lic), size=2, replace=False)
        leases.append((lic[int(a)], lic[int(b)], round(float(rng.uniform(4, 28)), 1),
                       dt.date(2026, m, int(rng.integers(2, 28))), "Lease L26/%02d" % (10 + k)))
    for la, lb, t, d, ref in leases:
        p = d + dt.timedelta(days=int(rng.integers(0, 3)))
        add(d, p, la["pool"], la["no"], "lease", -t, ref)
        add(d, p, lb["pool"], lb["no"], "lease", t, ref)
    # the last September lease, cancelled in October between licences in two pools
    sept = [x for x in leases if x[3].month == 9 and x[0]["pool"] != x[1]["pool"]]
    if not sept:
        la = next(l for l in vessel_lic if l["pool"] == "E")
        lb = next(l for l in vessel_lic if l["pool"] == "T")
        sept = [(la, lb, 16.0, dt.date(2026, 9, 21), "Lease L26/21")]
        p = sept[0][3] + dt.timedelta(days=1)
        add(sept[0][3], p, la["pool"], la["no"], "lease", -16.0, "Lease L26/21")
        add(sept[0][3], p, lb["pool"], lb["no"], "lease", 16.0, "Lease L26/21")
    la, lb, t, d, ref = sept[-1]
    c = dt.date(2026, 10, 6)
    add(c, c, la["pool"], la["no"], "lease", t, ref + " cancelled")
    add(c, c, lb["pool"], lb["no"], "lease", -t, ref + " cancelled")
    # landings: one entry a licence a month, dated the month's last day, posted with the month's statement
    for m in range(1, 10):
        last = (dt.date(2026, m + 1, 1) - dt.timedelta(days=1))
        post = dt.date(2026, m + 1, int(rng.integers(5, 13)))
        for l in vessel_lic:
            t = land.get((l["vessel"], m), 0.0)
            if t <= 0:
                continue
            t *= float(rng.uniform(1.02, 1.12))
            add(last, post, l["pool"], l["no"], "landings", -t, "Uptake %s 2026" % last.strftime("%b"))
    rows.sort(key=lambda r: (r[1], r[0], r[2], r[3], r[4]))
    out = []
    e = int(rng.integers(26100, 26400)) * 100
    for r in rows:
        e += 1
        out.append([str(e), r[0].isoformat(), r[1].isoformat(), r[2], r[3], r[4], "%.3f" % r[5], r[6]])
    return out, dict(alloc=alloc, lease_cancelled=(la["no"], lb["no"], t))
