"""The ask layer measured on the cut pack: asks A and B under the golden's handling and under the handlings a
response is likely to take, scored figure by figure against the golden (a hit is an exact count), and the pair
ceiling those keeps imply.

    python3 task486/generator/ceiling.py

Every handling reads the shop premises in force on the day in the centres, takes a premises with no account as in
occupation (the accounts' contents note says so) and an account on empty property relief as an owner's, and checks
the twelve months day by day; they differ only in how they tell an owner's account from an occupier's when the
account carries no relief. The golden takes the companies register's class: letting its own real estate (68209) or
developing building projects (41100). The cracker reads the register too but takes letting companies only; the
names handling takes a liable party whose name says property, estates, real estate or investments; the class-68
handling takes every real estate class, the agencies included; the relief-learned handling takes a party seen on
empty property relief anywhere as an owner everywhere."""
import datetime as dt
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import golden as G  # noqa: E402

TARGET = os.path.join(os.path.dirname(HERE), "target")
PROPERTY_WORDS = re.compile(r"\b(property|properties|real estate|estates|investments|land and)\b", re.I)


def owner_rule(P, kind):
    relief_parties = {(a["crn"] or G.norm(a["name"])) for a in P.accounts if a["relief"] == "EPR"}

    def sic_of(a):
        num = a["crn"] or P.co_by_name.get(G.norm(a["name"]))
        c = P.companies.get(num) if num else None
        return set(c["sic"]) if c else set()

    def owner(a):
        if a["relief"] == "EPR":
            return True
        if kind == "golden":
            return bool(sic_of(a) & G.OWNER_SIC)
        if kind == "letting_only":
            return "68209" in sic_of(a)
        if kind == "class_68":
            return any(x.startswith("68") for x in sic_of(a))
        if kind == "names":
            return bool(PROPERTY_WORDS.search(re.split(r"\s+t/a\s+", a["name"] or "", flags=re.I)[0]))
        if kind == "relief_learned":
            return (a["crn"] or G.norm(a["name"])) in relief_parties
        raise ValueError(kind)
    return owner


def handled(P, kind, chain=True):
    owner = owner_rule(P, kind)
    by_uarn = {}
    for a in P.accounts:
        by_uarn.setdefault(a["uarn"], []).append(a)
    for v in by_uarn.values():
        v.sort(key=lambda a: a["frm"])
    out = {}
    for yr in ("22", "26"):
        day = G.DAY[yr]
        empty, long = {}, {}
        for uarn, e in P.entries[yr].items():
            c = P.centre_of(e["pc"])
            if e["d"] != "R1" or not c:
                continue
            d = P.centres[c][1]
            empty.setdefault(d, 0)
            long.setdefault(d, 0)
            acc = by_uarn.get(uarn, [])
            cur = [j for j, a in enumerate(acc) if a["frm"] <= day and (a["to"] is None or a["to"] >= day)]
            if not cur or not owner(acc[cur[0]]):
                continue
            empty[d] += 1
            i = cur[0]
            start = acc[i]["frm"]
            if chain:
                while i > 0 and acc[i - 1]["to"] is not None and acc[i - 1]["to"] + dt.timedelta(days=1) == acc[i]["frm"] \
                        and owner(acc[i - 1]):
                    i -= 1
                    start = acc[i]["frm"]
            if start <= dt.date(day.year - 1, 4, 1):
                long[d] += 1
        out[yr] = (empty, long)
    return out


def figures(v):
    """the 24 graded ask figures, keyed as figures.json keys them"""
    f = {}
    for yr, (empty, long) in v.items():
        for d in sorted(empty):
            f["ask_a.%s.20%s" % (d, yr)] = empty[d]
            f["ask_b.%s.20%s" % (d, yr)] = long[d]
    return f


def measure(P=None):
    P = P or G.Pack(TARGET)
    gold = figures(G.vacancy(P))
    rows = {"golden": figures(handled(P, "golden")),
            "cracker": figures(handled(P, "letting_only")),
            "names": figures(handled(P, "names")),
            "class_68": figures(handled(P, "class_68")),
            "relief_learned": figures(handled(P, "relief_learned")),
            "golden_no_chain": figures(handled(P, "golden", chain=False))}
    keeps = {}
    for k, f in rows.items():
        keeps[k] = {ask: sum(1 for x in gold if x.startswith(ask) and f[x] == gold[x]) for ask in ("ask_a", "ask_b")}
    return gold, rows, keeps


def pair(keep_c, keep_m, total, call=45.0, miss=12.0):
    """the pair ceiling: the cracker on the call, the mirror off it, each keeping its share of 55 ask points"""
    return ((call + 55.0 * keep_c / total) + (miss + 55.0 * keep_m / total)) / 2


if __name__ == "__main__":
    gold, rows, keeps = measure()
    n = len(gold)
    print("graded ask figures:", n)
    for k, kp in keeps.items():
        print("  %-24s ask A %2d of 12, ask B %2d of 12" % (k, kp["ask_a"], kp["ask_b"]))
    kc = keeps["cracker"]["ask_a"] + keeps["cracker"]["ask_b"]
    print("cracker keeps %.1f per cent of ask weight; mirror the same; pair ceiling %.1f" % (100.0 * kc / n, pair(kc, kc, n)))
    worst = max(sum(v.values()) for k, v in keeps.items() if not k.startswith("golden"))
    print("the best non-golden handling keeps %d of %d (%.1f per cent)" % (worst, n, 100.0 * worst / n))
