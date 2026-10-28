"""The build's assertions, on the cut pack (target/) and the world's own forward run (truth.json).

    python3 task305/generator/checks.py [target]

The call and its margins, the ladder, the standing family and the adjustments the data supports, the response's
flatness, every semantic fork (SF1 to SF18), each Layer 1 item's neutrality (R2), the separation of the bridge from the
call, the input gates and the analyst test on the world's clean truth. Exit 1 on the first failure."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import solve as S

FLOOR = 1.15
BIN = 50000


def rounds(x):
    return int(BIN * round(float(x) / BIN))


def lead(v):
    o = np.argsort(-v)
    return S.APPS[o[0]], float(v[o[0]] / v[o[1]]) if v[o[1]] > 0 else 99.0


def main(target):
    fails = []

    def ok(cond, msg):
        print(("ok    " if cond else "FAIL  ") + msg)
        if not cond:
            fails.append(msg)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    g, c = S.golden_call(target)
    app, mg = lead(g)
    ok(app == "Ledgerline" and mg >= FLOOR, "call: %s, x%.2f over the next app" % (app, mg))
    ok(rounds(g[2]) == 100000, "the addition rounds to GBP 100,000 (as built %.0f)" % g[2])
    ok(fig["call"]["app"] == app and fig["call"]["addition"] == int(round(g[2])), "figures.json carries the call")
    # the ladder: every rung that skips the stopped accounts' response lands another app by the floor
    rt, info = S.routes(target)
    for k, want in (("L0", "Tracewood"), ("L1", "Tracewood"), ("L2", "Tracewood"), ("L3", "Formbox")):
        name = [n for n in rt if n.startswith(k + " ")][0]
        a, m = lead(rt[name])
        lv = rt[name][S.APPS.index(a)] / rt[name][2]
        ok(a == want and lv >= FLOOR, "%s files %s, x%.2f over Ledgerline" % (name, a, lv))
    # the routes that read the stopped accounts keep the call
    for k in ("S1", "S2", "S3"):
        name = [n for n in rt if n.startswith(k + " ")][0]
        a, m = lead(rt[name])
        ok(a == "Ledgerline", "%s keeps the call (x%.2f)" % (name, m))
    s3 = [n for n in rt if n.startswith("S3 ")][0]
    ok(rounds(rt[s3][2]) == 100000, "SF7: the response then carried as unstopped rounds to the same figure (%.0f)" % rt[s3][2])
    s1 = [n for n in rt if n.startswith("S1 ")][0]
    s2 = [n for n in rt if n.startswith("S2 ")][0]
    ok(rounds(rt[s1][2]) != 100000 and rounds(rt[s2][2]) != 100000,
       "SF1: nothing set against the stopped accounts gives another figure (%.0f, %.0f)" % (rt[s1][2], rt[s2][2]))
    # the standing family and the adjustments the data supports
    fam = dict(S.standing(target))
    fam.update(S.adjusted(target))
    for k, v in fam.items():
        a, m = lead(v)
        ok(a == "Ledgerline" and m >= FLOOR and rounds(v[2]) == 100000,
           "standing: %s, %s x%.2f, %.0f" % (k, a, m, v[2]))
    ok(all(k in fam for k in ("every stop, not the first",)), "SF9: every stop as well as the first")
    ok(any("2,000" in k for k in fam) and any("2,047" in k for k in fam), "SF6: the allowance read at several thresholds")
    ok(any("every unstopped" in k for k in fam), "SF8: every unstopped free account as the comparison")
    ok(any("own stopped" in k for k in fam) and any("four or more" in k for k in fam),
       "SF17: each app's own response and the four-or-more accounts alone")
    # the response is flat by app, project count and age
    by = S.response_by(target)
    up1, fr1, gone1 = S.response(target)
    for cut, d in by.items():
        for v, (n, p, gn) in d.items():
            ok(abs(gn - gone1) <= 0.03 and abs(p - up1) <= 0.015,
               "flat: %s %s, n %d, Plus %.3f, gone %.3f" % (cut, v, n, p, gn))
    # without the year's arrivals, and with the stock projected, the call holds
    D = S.panel(target)
    heavy, light, _ = S.kpi(target)
    v = S.addition(target, c["P1"] - c["P0"], c["F0"] - c["F1"], c["fr"], light=light * 0)
    ok(lead(v)[0] == "Ledgerline", "SF4: the accounts over the limit on 1 January alone keep the call (%.0f)" % v[2])
    v = S.addition(target, c["P1"] - c["P0"], c["F0"] - c["F1"], c["fr"], heavy=heavy * 1.01)
    ok(lead(v)[0] == "Ledgerline" and rounds(v[2]) == 100000, "SF5: the September count grown to January keeps it")
    # Layer 1, each item mishandled on its own (R2)
    S.MODE["rename"] = False
    v = S.golden_call(target)[0]
    S.MODE["rename"] = True
    ok(lead(v)[0] == "Ledgerline" and lead(v)[1] >= FLOOR, "R2 SF18: Leafnote's months dropped, %s x%.2f" % lead(v))
    S.MODE["drop_merged"] = True
    v = S.golden_call(target)[0]
    S.MODE["drop_merged"] = False
    ok(lead(v)[0] == "Ledgerline" and rounds(v[2]) == 100000, "R2: merged accounts left out, %s %.0f" % (lead(v)[0], v[2]))
    v = S.golden_call(target, thr=2000.0 * 1e6 / 1048576.0)[0]
    ok(lead(v)[0] == "Ledgerline", "R2: the allowance read as 2,000 MB (1,907 MiB), %s x%.2f" % lead(v))
    # the semantic forks with no golden construction of their own
    price, free = S.paper_table(target)
    ok(list(price) == [20.0, 8.0, 28.0, 13.0, 6.0], "SF2: a month on Plus at the paper's Plus monthly price")
    ok(abs(sum(fig["response"]["stopped_free"]) - c["F1"].sum()) < 1e-3, "SF3: a month of free use is a month with a row")
    ok(fig["call"]["addition_rounded"] == 100000, "SF10: the addition to the nearest GBP 50,000")
    # the bridge: its handlings and its separation from the call
    gb = S.bridge(target)
    for k, kw in (("SF11 customer record", dict(key="customer")), ("SF11 account", dict(key="account")),
                  ("SF12 cancelled at the request", dict(cancel="request")), ("SF13 opening at 2025/26 rates", dict(fx_open="2025/26")),
                  ("SF14 past due left out", dict(past_due=False))):
        x = S.bridge(target, **kw)
        miss = sum(1 for kk in S.ASK_KEYS if abs(x[kk] - gb[kk]) > 0.5)
        ok(miss >= 10, "%s moves %d of 20 bridge figures" % (k, miss))
    ok(all(abs(fig["ask"][k] - gb[k]) <= 0.5 for k in S.ASK_KEYS), "figures.json carries the bridge")
    for a in S.APPS:
        o, n, e, ct, ch, cl = (gb["%s %s" % (a, k)] for k in ("opening", "new", "expansion", "contraction", "churned", "closing"))
        ok(abs(o + n + e - ct - ch - cl) <= 3, "SF16: %s bridge ties (%d)" % (a, o + n + e - ct - ch - cl))
    src = open(os.path.join(HERE, "solve.py")).read()
    call_src = src[src.index("def golden_call"):src.index("# --- the recurring revenue bridge")]
    ok("billing" not in call_src and "fx_plan" not in call_src, "separation: the call reads no billing file")
    disc = S.bridge(target)
    ok(disc == gb, "SF15: discounts of twelve months or more only (the bridge as built)")
    # the input gates
    files = sorted(os.listdir(target))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok(len(files) >= 10 and len(fmts) >= 3, "gates: %d files, formats %s" % (len(files), sorted(fmts)))
    big = sum(1 for _ in open(os.path.join(target, "research_panel_account_months_2023_2026.csv"))) - 1
    ok(big >= 25000, "gates: the panel's account months, %d rows" % big)
    meta = json.load(open(os.path.join(os.path.dirname(HERE), "metadata.json")))
    ok(len(meta.get("distractor_files", [])) >= 2 and all(d in files for d in meta["distractor_files"]),
       "gates: distractors %s" % meta.get("distractor_files"))
    for d in meta["distractor_files"]:
        ok(d.split(".")[0] not in src, "distractor %s unread by solve.py" % d)
    # the world's forward run and the analyst test on the clean truth
    tj = os.path.join(HERE, "truth.json")
    if os.path.exists(tj):
        t = json.load(open(tj))
        tv = np.array([t["add"][a] for a in S.APPS])
        a, m = lead(tv)
        ok(a == "Ledgerline" and m >= FLOOR, "truth: %s x%.2f (%.0f)" % (a, m, tv[2]))
        ok(rounds(tv[2]) == 100000 and abs(g[2] / tv[2] - 1) < 0.25, "truth rounds as the golden (%.0f against %.0f)" % (tv[2], g[2]))
        cl = np.array([t["analyst_test"][a] for a in S.APPS])
        ok(lead(cl)[0] == "Tracewood", "analyst test on the clean truth: the own-upgrade route files %s" % lead(cl)[0])
    print("%d failures" % len(fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
