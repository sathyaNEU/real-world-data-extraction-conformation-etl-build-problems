"""The cracker and the mirror, run as code on the cut pack, and the pair ceiling they imply.

The cracker lands the call (the queue replay), runs the hygiene battery and executes every filed rule: euro and
dollar lines at the month's rate, fund codes through Schedule 2, packages shared by KBART titles on each
faculty's essential lists, coverage by C3.4's edition rule, the 40-loan meter replayed under Shelfmark 3.2 from
the status report with each re-licence started when a licence's fortieth loan ended. Where it has to resolve an
identity no filed rule covers it takes the careful solver's route: an item's ISBN normalised (hyphens, ISBN-10)
and followed through the links its own catalogue row carries, then a normalised title match; a re-licence that
reaches the register with no fund code takes the fund its title's own licences carry.

The mirror stops at the most attractive wrong rung on the call (the survival estimate with cancellations
censored, per faculty) and does the asks the natural way: the same filed rules, an item's ISBN matched to the
catalogue and its related record only, and the 40-loan meter counted against the earliest-purchased licence
with loans left.

    python3 ceiling.py [target_dir]
"""
import collections
import datetime as dt
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as AN

W_REC, W_HOLDS, W_HW, W_FILES, W_ASKS = 18.0, 10.0, 10.0, 7.0, 55.0


def b100(x):
    return int(math.floor(x / 100.0 + 0.5))


def norm_title(s):
    s = re.sub(r"\s*\(\d+\w*\s+edn\)\s*$", "", s.strip())
    return re.sub(r"\s+", " ", s.replace("&", "and")).lower()


def cracker_work(d, it, by_title, by_prefix):
    rec = d.cat_by_isbn.get(AN.norm_isbn(it["isbn"]))
    seen = 0
    while rec is not None and seen < 4:
        seen += 1
        if rec["platform"]:
            return rec["platform"], it["edition"]
        if rec["linked"] and d.cat.get(rec["linked"], {}).get("platform"):
            return d.cat[rec["linked"]]["platform"], it["edition"]
        rec = d.cat.get(rec["prev"]) if rec["prev"] else None
        if rec is not None and rec["platform"]:
            return rec["platform"], it["edition"]
    nt = norm_title(it["title"])
    if nt in by_title:
        return by_title[nt], it["edition"]
    if len(by_prefix.get(nt, [])) == 1:
        return by_prefix[nt][0], it["edition"]
    return None, it["edition"]


def title_maps(d):
    by_title, by_prefix = {}, collections.defaultdict(list)
    for v in d.cat.values():
        if v["platform"]:
            nt = norm_title(v["title"])
            by_title[nt] = v["platform"]
            by_prefix[nt.split(": ")[0]].append(v["platform"])
    return by_title, by_prefix


def asks_with(target, resolver, meter_variant):
    """A and B with a given identity resolver, C with a given meter variant"""
    d = AN.load_admin(target)
    saved = AN.item_work
    AN.item_work = lambda dd, it, variant="golden": resolver(dd, it)
    try:
        a, b = AN.ask_a(target), AN.ask_b(target)
    finally:
        AN.item_work = saved
    c = AN.ask_c(target, meter_variant)
    return a, b, c


def score(call, a, b, c, gold):
    g_call, g_a, g_b, g_c = gold
    rec = sum(b100(call["amount"][f]) == b100(g_call["amount"][f]) for f in AN.FAC_ORDER) / 8.0
    holds = sum(call["n"][f] == g_call["n"][f] for f in AN.FAC_ORDER) / 8.0
    hw = sum(b100(call["hw"][f]) == b100(g_call["hw"][f]) for f in AN.FAC_ORDER) / 8.0
    ka = sum(b100(a[f]) == b100(g_a[f]) for f in AN.FAC_ORDER)
    kb = sum(b[f] == g_b[f] for f in AN.FAC_ORDER)
    kc = sum(c[f] == g_c[f] for f in AN.FAC_ORDER)
    kept = (ka + kb + kc) / 24.0
    pts = W_REC * rec + W_HOLDS * holds + W_HW * hw + W_FILES + W_ASKS * kept
    return dict(pts=pts, kept=kept, ka=ka, kb=kb, kc=kc, rec=rec, holds=holds, hw=hw)


def run(target):
    gold = (AN.main_call(target), AN.ask_a(target), AN.ask_b(target), AN.ask_c(target))
    d = AN.load_admin(target)
    bt, bp = title_maps(d)
    cr_call = AN.main_call(target, "simple")
    ca, cb, cc = asks_with(target, lambda dd, it: cracker_work(dd, it, bt, bp), "title_majority")
    mi_call = AN.main_call(target, "km_fac")
    ma, mb, mc = asks_with(target, _no_chain, "ignore_busy")
    cr = score(cr_call, ca, cb, cc, gold)
    mi = score(mi_call, ma, mb, mc, gold)
    return cr, mi


def _no_chain(d, it):
    rec = d.cat_by_isbn.get(AN.norm_isbn(it["isbn"]))
    if rec is None:
        return None, it["edition"]
    if rec["platform"]:
        return rec["platform"], it["edition"]
    o = d.cat.get(rec["linked"])
    return (o["platform"] if o and o["platform"] else None), it["edition"]


def main(argv):
    target = argv[1] if len(argv) > 1 else os.path.join(TASK, "target")
    cr, mi = run(target)
    print("cracker (on the call): kept spend %d/8, lists %d/8, licences %d/8; ask weight kept %.1f%%; %.1f points"
          % (cr["ka"], cr["kb"], cr["kc"], 100 * cr["kept"], cr["pts"]))
    print("mirror (survival estimate): amounts %d/8, holds %d/8, hold-weeks %d/8; kept spend %d/8, lists %d/8, "
          "licences %d/8; ask weight kept %.1f%%; %.1f points"
          % (8 * mi["rec"], 8 * mi["holds"], 8 * mi["hw"], mi["ka"], mi["kb"], mi["kc"], 100 * mi["kept"], mi["pts"]))
    print("pair ceiling %.1f" % ((cr["pts"] + mi["pts"]) / 2.0))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
