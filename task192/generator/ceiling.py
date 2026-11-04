"""The ask layer's ceiling on the cut pack. Two responses are scored figure by figure against the golden:
the cracker (lands the call, runs the hygiene battery, reads every sheet and executes every filed rule) and the
mirror (stops at the procedure's own route and the OMS as the record). A figure is kept when it sits within half a
unit of the stated rounding. Prints each ask's keep for both rows, the pair ceiling and the pack's digest."""
import collections
import hashlib
import json
import os

import golden as G

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")


def digest():
    h = hashlib.sha256()
    for root, _, fs in sorted(os.walk(T)):
        for f in sorted(fs):
            h.update(open(os.path.join(root, f), "rb").read())
    return h.hexdigest()[:16]


def oms_only(items):
    return [o for o in items if o["src"] != "scada"]


def saidi_route(res, items, child_own_times, steps_new=True, nest=False, meds=None):
    """SAIDI from the OMS: the legacy children's customers from their own Out time (the cracker) or the parent's
    whole duration for everyone (the mirror)."""
    net = res["net"]
    cmi_by_day = collections.Counter()
    per = []
    for o in items:
        n = o["oms_customers"] if o["oms_customers"] is not None else len(o["reach"])
        if o["steps"] and o["src"] == "legacy":
            if child_own_times is None:
                cmi = n * (o["restore"] - o["start"]) / G.MIN
            else:
                cmi = 0.0
                kids = o["steps"][:-1]
                for t, k in kids:
                    out_t = o["child_out"].get(t, o["start"]) if child_own_times else o["start"]
                    cmi += k * (t - out_t) / G.MIN
                t, k = o["steps"][-1]
                cmi += k * (t - o["start"]) / G.MIN
        elif o["steps"] and steps_new:
            cmi = sum(k * (t - o["start"]) / G.MIN for t, k in o["steps"])
        else:
            cmi = n * (o["restore"] - o["start"]) / G.MIN
        d = G.lday(o["start"])
        cmi_by_day[d] += cmi
        per.append((o, d, cmi))
    if meds is None:
        meds = {d for d, v in cmi_by_day.items() if d.year == 2026 and v / res["nsys"] > res["tmed"]}
    out = collections.Counter()
    for o, d, cmi in per:
        if G.REP0 <= d <= G.REP1 and d not in meds:
            out[o["feeder"]] += cmi
    return out, meds


def child_out_times(T_, items):
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(T_, G.F["oms"]), read_only=True)
    rows = [r for r in wb["Legacy tickets"].iter_rows(min_row=2, values_only=True) if r[0] and r[1]]
    wb.close()
    by = collections.defaultdict(dict)
    for r in rows:
        by[r[1]][G.from_wall(r[6], "%m/%d/%Y %H:%M")] = G.from_wall(r[5], "%m/%d/%Y %H:%M")
    for o in items:
        o["child_out"] = by.get(o["id"], {})


def maifi_route(res, ev, absorb, out_now, merge, end_tree=False):
    net = res["net"]
    meds = set(res["meds"])
    starts = sorted((o["start"], i) for i, o in enumerate(res["items"]))
    mom = collections.Counter()
    for e in ev:
        if not (G.REP0 <= e["day"] <= G.REP1) or e["day"] in meds:
            continue
        reach = net.customers(e["device"], G.REP1 if end_tree else e["day"])
        if absorb or out_now:
            drop = set()
            em = G.floor_min(e["t"])
            for o in res["items"]:
                if out_now and o["start"] < em and e["t"] < o["restore"]:
                    drop |= reach & o["dark"]
                elif absorb and em <= o["start"] < em + G.MIN:
                    drop |= reach & o["dark"]
            reach = reach - drop
        mom[e["feeder"]] += len(reach)
    return mom


def cemi_route(res, items, tree_today=True, merge=False, connect=True):
    net = res["net"]
    meds = set(res["meds"])
    per = collections.Counter()
    for o in items:
        if not (G.REP0 <= o["day"] <= G.REP1) or o["day"] in meds:
            continue
        d = o["day"] if tree_today else G.REP1
        reach = net.customers(o["device"], d) if connect else _all_below(net, o["device"], d)
        for sp in reach:
            per[sp] += 1
    out = collections.Counter()
    for sp, k in per.items():
        if k > G.CEMI_N and net.active(sp, G.REP1):
            out[net.feeder(sp, G.REP1)] += 1
    return out


def _all_below(net, dev, d):
    if dev in net.sp:
        return {dev}
    return {sp for tid in net.down_transformers(dev, d) for sp in net.sp_by_t[tid]}


def keep(route, golden, unit, nt=None):
    hits = 0
    for f, g in golden.items():
        v = route.get(f, 0.0)
        if nt:
            v = v / nt[f]
        hits += abs(v - g) <= unit / 2 + 1e-9
    return hits, len(golden)


def main():
    res = G.compute(T)
    F = json.load(open(os.path.join(HERE, "figures.json")))
    nt = {f: v["nt"] for f, v in F["feeders"].items()}
    gs = {f: v["saidi"] for f, v in F["feeders"].items()}
    gm = {f: v["maifi"] for f, v in F["feeders"].items()}
    gc = {f: v["cemi"] for f, v in F["feeders"].items()}
    items = oms_only(res["items"])
    child_out_times(T, items)
    with_tc = [o for o in res["items"]]
    child_out_times(T, with_tc)
    # the cracker: every sheet read, children paired with their parents at their own Out times, steps applied,
    # the filed rules executed (DRP-04 2.7 sends it to the SCADA log for the openings the OMS never ticketed), the
    # register's dated rows used
    c_s, _ = saidi_route(res, with_tc, child_own_times=True)
    c_m = maifi_route(res, res["ev"], absorb=False, out_now=False, merge=False)
    c_c = cemi_route(res, with_tc, tree_today=True, connect=True)
    # the mirror: the OMS's parent rows at face value, the relay archive's operations, today's network
    m_s, _ = saidi_route(res, items, child_own_times=None, steps_new=False)
    m_m = maifi_route(res, [e for e in res["ev"]], absorb=False, out_now=False, merge=False, end_tree=True)
    m_c = cemi_route(res, items, tree_today=False, connect=False)
    rows = []
    for name, s, m, c in (("cracker", c_s, c_m, c_c), ("mirror", m_s, m_m, m_c)):
        ks = keep(s, gs, 0.1, nt)
        km = keep(m, gm, 0.01, nt)
        kc = keep(c, gc, 1)
        frac = (ks[0] / ks[1] + km[0] / km[1] + kc[0] / kc[1]) / 3
        rows.append((name, ks, km, kc, frac))
    cr, mi = rows
    c_score = 38 + 7 + 55 * cr[4]
    m_score = 5 + 7 + 55 * mi[4]
    print("pack digest %s" % digest())
    for name, ks, km, kc, frac in rows:
        print("%-8s SAIDI %2d of %d   MAIFI-E %2d of %d   CEMI-2 %2d of %d   ask weight kept %.1f per cent" %
              (name, ks[0], ks[1], km[0], km[1], kc[0], kc[1], 100 * frac))
    print("cracker on the call %.1f, mirror off it %.1f, pair ceiling %.1f" % (c_score, m_score, (c_score + m_score) / 2))
    # the full includer: the cracker that also finds one more device and handles it, and nothing else
    s_st, _ = saidi_route(res, with_tc, child_own_times=False)
    s_oms, _ = saidi_route(res, items, child_own_times=False)
    m_ab = maifi_route(res, res["ev"], absorb=True, out_now=False, merge=False)
    m_ab_out = maifi_route(res, res["ev"], absorb=True, out_now=True, merge=False)
    merged = [o for o in with_tc if o.get("continues") is None]
    c_mg = cemi_route(res, merged, tree_today=True, connect=True)
    c_oms = cemi_route(res, [o for o in items if o.get("continues") is None], tree_today=True, connect=True)
    for label, route, g, u, n_ in (("SAIDI, children timed from the parent", s_st, gs, 0.1, nt),
                                   ("SAIDI, children from the parent but the OMS alone", s_oms, gs, 0.1, nt),
                                   ("MAIFI-E, absorbed interruptions removed", m_ab, gm, 0.01, nt),
                                   ("MAIFI-E, absorbed and already-out customers removed", m_ab_out, gm, 0.01, nt),
                                   ("CEMI-2, continuations merged", c_mg, gc, 1, None),
                                   ("CEMI-2, continuations merged but the OMS alone", c_oms, gc, 1, None)):
        k = keep(route, g, u, n_)
        print("full includer, %s: %d of %d" % (label, k[0], k[1]))
    print("mirror leakage %.1f per cent of ask weight" % (100 * mi[4]))
    return rows


if __name__ == "__main__":
    main()
