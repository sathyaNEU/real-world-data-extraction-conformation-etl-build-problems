"""The ask layer measured on the cut pack: the cracker, every single-device crack, and the mirror, each run as code
over target/ and scored against the golden ask tables figure by figure (a hit is the exact count, or the wages to the
cent). Prints the cracker sheet, the pair ceiling under each path and the mirror's leakage.

    python3 task163/generator/cracker.py [target]

The cracker lands the call, reads the dictionary and the counting notes and executes every rule they point at: it
normalises EINs and takes a business's accounts as one (a returning client under its old EIN, a successor through
the payroll tax team's register, as the counting notes' re-formed entity rule asks), counts each business in the
state of its earliest registration, maps states to territories, converts the legacy cents and joins the legacy client
numbers through the crosswalk, and sums the rows of a quarter across files. It trusts what no rule tells it to doubt:
the onboarding answer, every wage row of the quarter, every row of a legacy client quarter, and the signup channel on
the account. A single-device crack repairs one of those four. The mirror stops at the default path on the call and
reads the asks the plain way: flagged accounts by their own first pay date, the address state, the account's own
fourth-quarter row."""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as CA   # noqa: E402

TASK = os.path.dirname(HERE)
W_REC, W_INSTR, W_ASK = 38.0, 7.0, 55.0
R_KEEP = 5.0          # recommendation weight a response off the call keeps
CHART_STRUCT = 2      # chart criteria every response that draws the chart earns (a bar pair per territory, labels)


def wq_variant(B, rollup_right=True):
    """Wages by (account, year, quarter) in cents; the plain sum of a legacy client quarter adds group 00 to its
    parts."""
    wq = {}
    for r in B.leg:
        if rollup_right and r["pay_group"] != "00":
            continue
        a = B.acct_of_legacy[r["client_no"]]
        k = (a, int(r["tax_year"]), int(r["tax_qtr"]))
        wq[k] = wq.get(k, 0) + int(r["gross_wages"])
    for r in B.cur:
        y, q = r["quarter"].split("-Q")
        k = (r["account_id"], int(y), int(q))
        wq[k] = wq.get(k, 0) + int(round(float(r["gross_wages"]) * 100))
    return wq


def path(B, inhouse=False, taxonly=False, rollup=False, channel=False, successors=True, mirror=False,
         taxonly_any=False):
    """One solver's ask tables. Each flag set True repairs that device."""
    wq = B.wq if rollup else wq_variant(B, rollup_right=False)
    T = {t: {"signed": 0, "still": 0, "wages_cents": 0, "wages_2024_cents": 0} for t in sorted(set(B.terr.values()))}
    ch = {}
    if mirror:
        for a in B.acc:
            if a["first_time_employer"] != "Y" or not a["first_pay_date"].startswith("2024"):
                continue
            t = B.terr.get(a["address_state"])
            if t is None:
                continue
            T[t]["signed"] += 1
            if wq.get((a["account_id"], 2025, 4), 0) > 0:
                T[t]["still"] += 1
            y, q = CA.quarter_of(a["first_pay_date"])
            T[t]["wages_cents"] += wq.get((a["account_id"], y, q), 0)
            T[t]["wages_2024_cents"] += sum(wq.get((a["account_id"], 2024, qq), 0) for qq in (1, 2, 3, 4))
            ch[a["signup_channel"]] = ch.get(a["signup_channel"], 0) + 1
        return T, ch
    for e, accts in sorted(B.by_ein.items()):
        first = min(accts, key=lambda r: (r["first_pay_date"], r["account_id"]))
        if not first["first_pay_date"].startswith("2024") or first["first_time_employer"] != "Y":
            continue
        if successors and e in B.successor_eins:
            continue
        if inhouse and B.liable_before(accts, first["first_pay_date"]):
            continue
        allacc = B.business_accounts(first) if successors else accts
        st = B.first_state(accts)
        t = B.terr.get(st)
        if t is None:
            continue
        T[t]["signed"] += 1
        if any(wq.get((a["account_id"], 2025, 4), 0) > 0 and (not taxonly or CA.paid_by_us(a, 2025, 4)) and
               not (taxonly_any and a["product"] == "Tax filing only") for a in allacc):
            T[t]["still"] += 1
        y, q = CA.quarter_of(first["first_pay_date"])
        T[t]["wages_cents"] += sum(wq.get((a["account_id"], y, q), 0) for a in allacc)
        T[t]["wages_2024_cents"] += sum(wq.get((a["account_id"], 2024, qq), 0) for a in allacc for qq in (1, 2, 3, 4)
                                        if (not taxonly or CA.paid_by_us(a, 2024, qq)))
        code = B.code_of.get(first["account_id"]) if channel else None
        c = CA.CODE_CHANNEL[code] if code else first["signup_channel"]
        ch[c] = ch.get(c, 0) + 1
    return T, ch


def score(gold, got):
    """Per-figure hits against the golden tables: (hits, total, rows)."""
    GT, GC = gold
    T, Ch = got
    rows = []
    for t in sorted(GT):
        for k in ("signed", "still", "wages_cents", "wages_2024_cents"):
            rows.append(("%s %s" % (t, k), GT[t][k], T.get(t, {}).get(k), GT[t][k] == T.get(t, {}).get(k)))
    for c in sorted(GC):
        rows.append(("channel %s" % c, GC[c], Ch.get(c, 0), GC[c] == Ch.get(c, 0)))
    return rows


def ask_share(rows, chart_value_hits):
    """Share of the ask weight kept: the figures, two chart criteria every response earns and two that hold only when
    every territory's signed and still figures are right."""
    n = len(rows) + CHART_STRUCT + 2
    kept = sum(1 for r in rows if r[3]) + CHART_STRUCT + chart_value_hits
    return kept / n


def chart_hits(rows):
    signed = all(r[3] for r in rows if r[0].endswith(" signed"))
    still = all(r[3] for r in rows if r[0].endswith(" still"))
    return int(signed) + int(still)


def measure(target):
    B = CA.Book(target)
    GT, GC, _ = CA.asks(B)
    gold = (GT, GC)
    paths = {
        "cracker": dict(),
        "cracker + prior liability": dict(inhouse=True),
        "cracker + tax filing only": dict(taxonly=True),
        "cracker + every tax filing only account dropped": dict(taxonly_any=True),
        "cracker + prior liability + tax filing only": dict(inhouse=True, taxonly=True),
        "cracker + group 00": dict(rollup=True),
        "cracker + legacy source code": dict(channel=True),
        "every device": dict(inhouse=True, taxonly=True, rollup=True, channel=True),
    }
    out = {}
    for name, kw in paths.items():
        rows = score(gold, path(B, **kw))
        L = ask_share(rows, chart_hits(rows))
        out[name] = (rows, L)
    mrows = score(gold, path(B, mirror=True))
    Ls = ask_share(mrows, chart_hits(mrows))
    S = R_KEEP + W_INSTR + W_ASK * Ls
    res = {"paths": {}, "mirror_leakage": 100.0 * Ls, "mirror_score": S}
    for name, (rows, L) in out.items():
        Cs = W_REC + W_INSTR + W_ASK * L
        res["paths"][name] = {"ask_share": L, "score": Cs, "pair": (Cs + S) / 2.0,
                              "hits": [r[0] for r in rows if r[3]]}
    res["cracker_rows"] = [(r[0], r[1], r[2], "hit" if r[3] else "miss") for r in out["cracker"][0]]
    res["mirror_rows"] = [(r[0], r[1], r[2], "hit" if r[3] else "miss") for r in mrows]
    return res


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target")
    res = measure(target)
    print("cracker sheet (golden, cracker, verdict):")
    for name, g, c, v in res["cracker_rows"]:
        print("  %-36s %14s %14s %s" % (name, g, c, v))
    print("mirror: leakage %.1f per cent of ask weight, score %.1f" % (res["mirror_leakage"], res["mirror_score"]))
    for name, p in res["paths"].items():
        print("  %-30s ask share %.3f  score %.1f  pair %.1f  hits %d" % (name, p["ask_share"], p["score"], p["pair"],
                                                                       len(p["hits"])))
    worst_single = max(v["pair"] for k, v in res["paths"].items() if k.count("+") <= 1 and k != "every device")
    print("pair ceiling: cracker %.1f, strongest single crack %.1f" % (res["paths"]["cracker"]["pair"], worst_single))
    with open(os.path.join(HERE, "cracker.json"), "w") as fh:
        json.dump({k: v for k, v in res.items() if k != "mirror_rows"}, fh, indent=1, default=str)
        fh.write("\n")


if __name__ == "__main__":
    main()
