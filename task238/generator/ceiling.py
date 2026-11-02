"""The cracker and mirror sheets, scored on the cut pack (target/).

The cracker lands the call, runs the hygiene battery and executes every filed rule it points at: register overrides
converted from UTC, reason SC only, the payout taken as the original less the override price, every desk refund
that matches a register override on the same receipt line dropped as a cross-system duplicate; the revised price
release, multi-buys per unit, each zone's own units, a correction file applied as the latest version, an assorted
line's other UPCs found by the lead's keyed price. The full includer handles every device it can see. The mirror
stops at the first attractive reading: both payout logs added, the lead UPC of each flyer line only, the release
price all week. Scores on 38 (call and components) + 7 (instruction following) + 55 (asks), each ask figure
weighted equally and hit within half a dollar or exactly for a count.

    python3 task238/generator/ceiling.py [target]
"""
import datetime as dt
import hashlib
import json
import os
import re
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402


def payouts_variant(target, by_name, mode="golden"):
    ov = A.rows(os.path.join(target, A.FILES["overrides"]))
    till = {}
    pay = defaultdict(float)
    for r in ov:
        if r["reason_code"] != "SC":
            continue
        u = dt.datetime.strptime(r["override_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=A.UTC)
        if mode == "utc_date":
            inq = dt.date(2026, 10, 1) <= u.date() <= dt.date(2026, 12, 31)
        else:
            t = u.astimezone(A.TZ)
            inq = A.Q0 <= t < A.Q1
        if not inq:
            continue
        s = int(r["store_no"])
        amt = (int(r["orig_price_cents"]) - int(r["override_price_cents"])) / 100.0
        if mode == "override_as_payout":
            amt = int(r["override_price_cents"]) / 100.0
        if mode != "desk_only":
            pay[s] += amt
        till[(s, int(r["register"]), int(r["transaction"]), r["upc"])] = amt
    if mode == "till_only":
        return dict(pay)
    for r in A.xlsx_rows(os.path.join(target, A.FILES["desk"])):
        if r.get("Reason") != "Scanner Code":
            continue
        t = r["Date / time"]
        if not (dt.datetime(2026, 10, 1) <= t < dt.datetime(2027, 1, 1)):
            continue
        s = by_name[r["Store"]]
        rec = str(r["Receipt #"])
        parts = re.split(r"[-/]", rec)
        if "/" in rec:
            txn, reg = int(parts[0]), int(parts[1])
        elif len(parts) == 3:
            reg, txn = int(parts[1]), int(parts[2])
        else:
            reg, txn = int(parts[0]), int(parts[1])
        upc = str(r["UPC"])[1:]
        amt = float(r["Refund $"])
        key = (s, reg, txn, upc)
        if mode in ("golden", "utc_date", "override_as_payout") and key in till and abs(till[key] - amt) < 0.005:
            continue
        if mode == "key_dedup" and key in till:
            continue
        pay[s] += amt
    return dict(pay)


def score(fig, ref, tol):
    keys = sorted(ref)
    return sum(1 for k in keys if abs(fig.get(k, 0) - ref[k]) <= tol), len(keys)


def main(target=None):
    target = target or os.path.join(TASK, "target")
    F = json.load(open(os.path.join(HERE, "figures.json")))
    pk = A.Pack(target)
    gold_pay = {int(k): v for k, v in F["payouts"].items()}
    gold_cnt = F["flyer_count"]
    gold_over = F["flyer_over"]

    def ask_hits(pay_mode, flyer_kw):
        p = payouts_variant(target, pk.by_name, pay_mode)
        pr = {s: round(p.get(s, 0.0)) for s in gold_pay}
        a = score(pr, gold_pay, 0.5)
        c, o = A.ask_flyer(target, **flyer_kw)
        b1 = score(c, gold_cnt, 0)
        b2 = score({d: round(v) for d, v in o.items()}, gold_over, 0.5)
        return a, b1, b2

    rows = {
        "cracker (battery route)": ("key_dedup", {"corr": "whole", "match": "price"}),
        "full includer": ("golden", {"corr": "dated", "match": "family"}),
        "mirror (first reading)": ("union", {"lead_only": True, "corr": "none"}),
    }
    out = {}
    for name, (pm, fk) in rows.items():
        a, b1, b2 = ask_hits(pm, fk)
        hits = a[0] + b1[0] + b2[0]
        total = a[1] + b1[1] + b2[1]
        out[name] = (a, b1, b2, hits / total)
        print("%-26s ask A %2d/%d  ask B counts %2d/%d  ask B dollars %2d/%d  kept %.1f%%" %
              (name, a[0], a[1], b1[0], b1[1], b2[0], b2[1], 100 * hits / total))
    lc = out["cracker (battery route)"][3]
    ls = out["mirror (first reading)"][3]
    on_call = 38 + 7 + 55 * lc
    # the mirror files the audit route's call (no store), so of the call's 38 it keeps only the stores it
    # rightly leaves off: nine of fourteen verdicts at about half the component weight
    n_stores = len(F["accuracy"])
    n_off = n_stores - F["n_watch"]
    r_off = 38 * 0.5 * (n_off / float(n_stores)) * 0.4
    off_call = r_off + 7 + 55 * ls
    pair = (on_call + off_call) / 2
    print("cracker on the call  %.1f" % on_call)
    print("mirror off the call  %.1f" % off_call)
    print("Pair ceiling: %.1f" % pair)
    print("Mirror leakage: %.1f per cent of ask weight" % (100 * ls))
    full = out["full includer"][3]
    print("full includer keeps %.1f%% of ask weight" % (100 * full))
    # every ask stop the design note's ask sheet quotes, each a complete pipeline scored on the cut pack
    for mode, what in (("union", "both payout logs added"), ("key_dedup", "every desk entry on a register-paid line "
                       "dropped"), ("desk_only", "desk refunds only"), ("till_only", "register overrides only"),
                       ("utc_date", "the override export's UTC date"), ("override_as_payout", "the override price "
                       "read as the payout")):
        p = payouts_variant(target, pk.by_name, mode)
        miss = sum(1 for st in gold_pay if abs(round(p.get(st, 0.0)) - gold_pay[st]) > 0.5)
        print("stop A  %-45s misses %2d of %d stores" % (what, miss, len(gold_pay)))
    for what, kw in (("each flyer line's lead UPC only", {"lead_only": True}),
                     ("varieties matched by the lead's keyed price", {"match": "price"}),
                     ("the release price all week", {"corr": "none"}),
                     ("the correction taken for the whole week", {"corr": "whole"}),
                     ("the Monday preliminary release", {"release": "PRELIM"}),
                     ("a multi-buy compared as its line price", {"qty_aware": False}),
                     ("the two zones' units averaged", {"zone_units": False})):
        c, o = A.ask_flyer(target, **kw)
        mc = sum(1 for d in gold_cnt if c.get(d, 0) != gold_cnt[d])
        mo = sum(1 for d in gold_over if abs(round(o.get(d, 0.0)) - gold_over[d]) > 0.5)
        print("stop B  %-45s misses %2d counts, %2d dollar figures of %d weeks" % (what, mc, mo, len(gold_cnt)))
    h = hashlib.sha256()
    for name in sorted(os.listdir(target)):
        h.update(name.encode())
        h.update(open(os.path.join(target, name), "rb").read())
    print("measured on the cut pack target/ (sha256 over its files %s)" % h.hexdigest()[:8])
    return pair, 100 * ls, out


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None)
