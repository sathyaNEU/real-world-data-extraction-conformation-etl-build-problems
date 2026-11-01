"""task146 architecture 2: the golden and its rungs, computed from target/ alone.

money=True follows each closing payment into the instant-access opening it funded the same local day at the same
amount (the golden); money=False measures each account on its own (the account cohort, the field's method); bonds=True
also keeps a closing payment that funded a fixed-rate bond the same day (a rung the policy's 'in instant-access savings'
rules out). share='pooled' takes the kept balances over the start balances taken together across start dates.
"""
import collections
import csv
import datetime as dt
import os
from zoneinfo import ZoneInfo

from openpyxl import load_workbook

LONDON = ZoneInfo("Europe/London")
FAMILY = {"ES01": "Easy Saver", "IS01": "Easy Access Cash ISA", "YS01": "Young Saver"}
FAMILIES = ("Easy Saver", "Loyalty Saver", "Easy Access Cash ISA", "Young Saver")
RECODE = dt.date(2025, 7, 1)
HORIZONS = (12, 24, 36)


def family(code, day):
    if code.startswith("LS"):
        return "Loyalty Saver"
    if code == "ES02":
        return "Easy Saver" if day < RECODE else "Young Saver"
    return FAMILY[code]


def load(target):
    F = lambda n: os.path.join(target, n)
    bal = collections.defaultdict(dict)       # month index -> {account: pounds}
    fam_at = {}                               # (account, month index) -> family
    months = []
    with open(F("ia_month_end_balances_2021-2026.csv")) as fh:
        rows = list(csv.DictReader(fh))
    keys = sorted({(dt.date.fromisoformat(r["month_end"]).year, dt.date.fromisoformat(r["month_end"]).month)
                   for r in rows})
    idx = {k: i for i, k in enumerate(keys)}
    for r in rows:
        d = dt.date.fromisoformat(r["month_end"])
        i = idx[(d.year, d.month)]
        a = int(r["account_no"])
        bal[i][a] = float(r["balance_gbp"])
        fam_at[(a, i)] = family(r["product_code"], d)
    ev = []
    with open(F("ia_account_events_2021-2026.csv")) as fh:
        for r in csv.DictReader(fh):
            t = dt.datetime.strptime(r["event_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=dt.timezone.utc)
            ev.append((t.astimezone(LONDON).date(), r["event"], int(r["account_no"]), r["product_code"],
                       int(r["amount_pence"])))
    return {"bal": bal, "fam": fam_at, "keys": keys, "events": ev, "target": target}


def links(D, bonds=False):
    """Successor of each account: the instant-access account opened the same local day with the closing amount."""
    opens = collections.defaultdict(list)
    closes = []
    for day, e, a, code, p in D["events"]:
        if e == "OPEN":
            opens[(day, p)].append(a)
        else:
            closes.append((day, a, p))
    succ = {}
    used = set()
    for day, a, p in closes:
        cand = [b for b in opens.get((day, p), []) if b != a and b not in used]
        if len(cand) == 1:
            succ[a] = cand[0]
            used.add(cand[0])
    bond_kept = {}
    if bonds:
        with open(os.path.join(D["target"], "fixed_rate_bond_openings_2021-2026.csv")) as fh:
            bo = collections.Counter()
            for r in csv.DictReader(fh):
                d = dt.datetime.strptime(r["opened"], "%d/%m/%Y").date()
                bo[(d, int(round(float(r["principal_gbp"]) * 100)))] += 1
        for day, a, p in closes:
            if a not in succ and bo.get((day, p)):
                bond_kept[a] = p / 100.0
    return succ, bond_kept


def stable(D, money=True, bonds=False, share="pooled"):
    bal, keys = D["bal"], D["keys"]
    n = len(keys)
    succ, bond_kept = links(D, bonds) if money else ({}, {})
    out = {}
    for k in HORIZONS:
        kept = collections.Counter()
        held = collections.Counter()
        ratios = collections.defaultdict(list)
        for s in range(0, n - k, 12):
            kk = collections.Counter()
            hh = collections.Counter()
            for a, b0 in bal[s].items():
                if b0 <= 0:
                    continue
                f = D["fam"][(a, s)]
                low = b0
                cur = a
                ended = False
                for t in range(s + 1, s + k + 1):
                    v = bal[t].get(cur, 0.0)
                    while cur in succ and cur not in bal[t]:
                        cur = succ[cur]
                        v = bal[t].get(cur, 0.0)
                    if v == 0.0 and cur in succ:
                        nxt = succ[cur]
                        if bal[t].get(nxt, 0.0) > 0:
                            cur = nxt
                            v = bal[t][nxt]
                    if v == 0.0 and cur in bond_kept:
                        v = min(b0, bond_kept[cur])
                    low = min(low, v)
                kk[f] += low
                hh[f] += b0
            for f in FAMILIES:
                kept[f] += kk[f]
                held[f] += hh[f]
                if hh[f]:
                    ratios[f].append(kk[f] / hh[f])
        out[k] = {f: (kept[f] / held[f] if share == "pooled" else sum(ratios[f]) / len(ratios[f])) for f in FAMILIES}
    now = collections.Counter()
    for a, b in bal[n - 1].items():
        now[D["fam"][(a, n - 1)]] += b
    res = {"now": dict(now), "share": out, "stable": {}}
    for k in HORIZONS:
        res["stable"][k] = {f: now[f] * out[k][f] for f in FAMILIES}
        res["stable"][k]["total"] = sum(res["stable"][k][f] for f in FAMILIES)
    res["book"] = sum(now.values())
    return res


def total_ratio(D):
    """R0: the total book a year on over the book at each start date (new money included)."""
    bal, n = D["bal"], len(D["keys"])
    out = {}
    for k in HORIZONS:
        num = sum(sum(bal[s + k].values()) for s in range(0, n - k, 12))
        den = sum(sum(bal[s].values()) for s in range(0, n - k, 12))
        out[k] = num / den
    return out


def to1m(x):
    return int(round(x / 1e6)) * 1000000


def call(D, swaps_after_jan=None):
    g = stable(D, money=True)
    hedge = to1m(g["stable"][12]["total"])
    wb = load_workbook(os.path.join(D["target"], "structural_hedge_swap_register_2026-12.xlsx"), read_only=True)
    ws = wb["Swaps"]
    sw = [(r[3], r[4]) for r in ws.iter_rows(min_row=2, values_only=True) if r and r[0]]
    after = sum(n for mat, n in sw if mat > "2027-01-29")
    held_now = sum(n for mat, n in sw)
    new = hedge - after
    return {"hedge": hedge, "swaps_now": held_now, "after_january": after, "new_swap": new, "golden": g}


if __name__ == "__main__":
    import sys
    D = load(sys.argv[1])
    c = call(D)
    g = c["golden"]
    print("book %.2fm hedge %.1fm new swap %.1fm (swaps now %.1fm, after January %.1fm)" % (
        g["book"] / 1e6, c["hedge"] / 1e6, c["new_swap"] / 1e6, c["swaps_now"] / 1e6, c["after_january"] / 1e6))
    for k in HORIZONS:
        print(k, "total %.2fm" % (g["stable"][k]["total"] / 1e6),
              " ".join("%s %.3f" % (f.split()[0], g["share"][k][f]) for f in FAMILIES))
    a = stable(D, money=False)
    b = stable(D, money=True, bonds=True)
    m = stable(D, money=True, share="mean")
    print("R1 account cohort 1y %.2fm, R2 with bonds %.2fm, mean-of-ratios %.2fm, R0 ratio %.3f" % (
        a["stable"][12]["total"] / 1e6, b["stable"][12]["total"] / 1e6, m["stable"][12]["total"] / 1e6,
        total_ratio(D)[12]))
