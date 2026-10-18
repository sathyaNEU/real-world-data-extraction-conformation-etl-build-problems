"""task167 cracker: the ask figures the strongest responses keep, measured on the cut pack.

The cracker lands the call, runs the hygiene battery (no duplicate line, every code joins the register, the
custodian's account totals tie, every cancelled notice dropped, the handover quarter counted once), executes every
filed rule (policy 3.1's qualifying list, 4.1's roll-forward and 2.5's rate, Schedule 1) and takes each file's
columns as they stand: the summary's rows and currency labels, the custodian's positions and asset classes. The mirror
stops at the pooled call schedule; the asks are decoupled from the call, so its ask route is the cracker's (the
separation assertions in checks.py prove the asks read no row the call reads, and no device row sits in the call's).

    python3 cracker.py TARGET_DIR"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as K   # noqa: E402

STRATS = ("Buyout", "Growth equity", "Venture capital", "Private credit")
A_KEYS = ["strategy:" + s for s in STRATS] + ["ccy:EUR", "ccy:USD", "band:2015-2018", "band:2019-2022", "total"]
B_KEYS = ["total", "bills", "q1", "q2", "q3", "q4"]
W_CALL, W_IF, W_ASK, W_MISS = 38.0, 7.0, 55.0, 5.0


def nav(p, t, **kw):
    rows = K.nav_year_end(p, t, **kw)
    f = K.nav_figures(rows)
    for lo, hi in ((2015, 2018), (2019, 2022)):
        f["band:%d-%d" % (lo, hi)] = sum(r["usd"] for r in rows if lo <= r["vintage"] <= hi)
    return {k: round(f.get(k, 0.0) / 1e6, 1) for k in A_KEYS}


def assets(t, **kw):
    q = K.qualifying(t, **kw)
    d = dict(total=q["total"], bills=q["bills"], q1=q["ladder"][0], q2=q["ladder"][1], q3=q["ladder"][2], q4=q["ladder"][3])
    return {k: round(v / 1e6, 1) for k, v in d.items()}


def golden(t):
    p = K.Pack(t)
    return p, nav(p, t), assets(t)


def keeps(gold, got):
    return [k for k in gold if abs(got[k] - gold[k]) < 0.05]


def measure(t):
    p, ga, gb = golden(t)
    routes = {
        "cracker": (dict(combined_seen=False, currency_from_register=False), dict(settled=False, by_description=False)),
        "A1 cracked alone (the combined statements)": (dict(combined_seen=True, currency_from_register=False),
                                                       dict(settled=False, by_description=False)),
        "A2 cracked alone (the defaulted currency)": (dict(combined_seen=False, currency_from_register=True),
                                                      dict(settled=False, by_description=False)),
        "B1 cracked alone (the unsettled ladder)": (dict(combined_seen=False, currency_from_register=False),
                                                    dict(settled=True, by_description=False)),
        "B2 cracked alone (the agency notes)": (dict(combined_seen=False, currency_from_register=False),
                                                dict(settled=False, by_description=True)),
    }
    n = len(A_KEYS) + len(B_KEYS)
    out = {}
    for name, (ka, kb) in routes.items():
        a, b = nav(p, t, **ka), assets(t, **kb)
        kept = ["A " + k for k in keeps(ga, a)] + ["B " + k for k in keeps(gb, b)]
        c = W_CALL + W_IF + W_ASK * len(kept) / n
        s = W_MISS + W_IF + W_ASK * len(keeps(ga, nav(p, t, **routes["cracker"][0])) + keeps(gb, assets(t, **routes["cracker"][1]))) / n
        out[name] = dict(kept=kept, cracker=c, mirror=s, pair=(c + s) / 2.0, a=a, b=b)
    out["_gold"] = dict(a=ga, b=gb, n=n)
    return out


def report(t):
    m = measure(t)
    g = m.pop("_gold")
    print("ask figures: %d (Ask A %d, Ask B %d)" % (g["n"], len(A_KEYS), len(B_KEYS)))
    print("golden A", g["a"])
    print("golden B", g["b"])
    for name, r in m.items():
        print("%-46s keeps %2d of %d  cracker %.1f  mirror %.1f  pair %.1f  %s" % (
            name, len(r["kept"]), g["n"], r["cracker"], r["mirror"], r["pair"], ", ".join(r["kept"]) or "-"))
    return m, g


if __name__ == "__main__":
    report(sys.argv[1])
