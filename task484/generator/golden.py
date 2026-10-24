"""The golden determinations from the world's own objects: each area's 2025-26 inventory, its 2014 base year rebuilt
for the stock that burned then (the survey's cords for each appliance's class, the changed-out units at the cords for
their recorded heat status), the reduction against the commitment; and the ladder's rungs on the same objects."""
import numpy as np

import world as W

LB_PER_TON = 2000.0


def cells(resp):
    """Survey means by area and class, by area, class and heat status, and by area and class over the respondents
    whose appliance was in place by 2014 (weights are equal inside a stratum, so these are the weighted means)."""
    m, ms, mo = {}, {}, {}
    for code in W.CODES:
        for cl in W.CL:
            rs = [x for x in resp if x["dev"].area == code and x["dev"].cl == cl]
            m[code, cl] = float(np.mean([x["use"] for x in rs]))
            for st in (True, False):
                k = [x["use"] for x in rs if x["dev"].primary == st]
                ms[code, cl, st] = float(np.mean(k)) if k else m[code, cl]
            k = [x["use"] for x in rs if x["dev"].installed <= 2014]
            mo[code, cl] = float(np.mean(k)) if k else m[code, cl]
    return m, ms, mo


def pm(cl, use_total, factor=None):
    """Tons of PM2.5 from a total of wood burned (cords, or tons of pellets)."""
    return W.tons_of(cl, use_total) * (factor if factor is not None else W.CLASSES[cl][6]) / LB_PER_TON


def evaluate(devs, apps, resp):
    m, ms, mo = cells(resp)
    out = {}
    for code, name, county, scale, prog, srate, commit, vf in W.AREAS:
        row = dict(name=name, county=county, commit=commit, cls={})
        e26 = b_gold = b_mean = b_dflt = b_surv = b_allp = b_true = e26_true = 0.0
        for cl in W.CL:
            stock = W.base_stock(devs, code, cl)
            n14 = len(stock)
            co = [a["old"] for a in apps if a["old"].area == code and a["old"].cl == cl]
            assert all(d in stock for d in co)
            n26 = sum(1 for d in devs if d.area == code and d.cl == cl and W.in_season(d))
            a26 = n26 * m[code, cl]
            if cl in W.CHANGED:
                ncp = sum(1 for d in co if d.primary)
                g = (n14 - len(co)) * m[code, cl] + ncp * ms[code, cl, True] + (len(co) - ncp) * ms[code, cl, False]
                allp = (n14 - len(co)) * m[code, cl] + len(co) * ms[code, cl, True]
                surv = (n14 - len(co)) * m[code, cl]
            else:
                g = allp = n14 * mo[code, cl]
                surv = n14 * m[code, cl]
            row["cls"][cl] = dict(n14=n14, n26=n26, co=len(co), a14=g, a26=a26, pm14=pm(cl, g), pm26=pm(cl, a26),
                                  dflt=pm(cl, n14 * W.CLASSES[cl][8], W.CLASSES[cl][7]))
            e26 += pm(cl, a26)
            b_gold += pm(cl, g)
            b_allp += pm(cl, allp)
            b_mean += pm(cl, n14 * m[code, cl])
            b_surv += pm(cl, surv)
            b_dflt += pm(cl, n14 * W.CLASSES[cl][8], W.CLASSES[cl][7])
            b_true += pm(cl, sum(d.use for d in stock))
            e26_true += pm(cl, sum(d.use for d in devs if d.area == code and d.cl == cl and W.in_season(d)))
        red = lambda b, e=e26: 100.0 * (b - e) / b
        row.update(pm26=e26, pm14=b_gold, reduction=red(b_gold), trigger=red(b_gold) < commit,
                   rungs=dict(golden=red(b_gold), allprimary=red(b_allp), classmean=red(b_mean), survivors=red(b_surv),
                              default=red(b_dflt), truth=red(b_true, e26_true)))
        out[code] = row
    return out


def ask_a(devs):
    """The registry's appliances in place in the 2014 season by area and class on the 2020 boundaries, each appliance
    once (a split's re-registration is the same appliance), with the plan's count and the two items between them."""
    out = {}
    for code in W.CODES:
        for cl in W.CL:
            plan = W.base_stock(devs, code, cl)
            reg = [d for d in devs if d.area == code and d.cl == cl and d.replaces is None and d.installed <= 2014
                   and not d.moved]
            late = [d for d in reg if d.late]
            left = [d for d in plan if d.moved]
            assert len(reg) == len(plan) - len(left) + len(late)
            out[code, cl] = dict(plan=len(plan), registry=len(reg), late=len(late), left=len(left),
                                 split=sum(1 for d in reg if d.split))
    return out


def ask_b(bgs):
    """Each county's remainder outside the areas on the state tool: the 2019-2023 release's main-heat households
    of each block group times its housing units' share outside the areas, the tool's secondary ratio, shares and use."""
    import pack as P
    out = {}
    for county in W.COUNTIES:
        for cl in W.CL:
            wood = 0.0
            for b in bgs:
                if b["county"] != county:
                    continue
                hu_in = int(round(b["hu"] * b["inside"]))
                share_out = (b["hu"] - hu_in) / b["hu"]
                main = b["acs1923"] * share_out
                use = main * P.TOOL_SHARE[True][cl] * P.TOOL_USE[True][cl] + \
                    main * P.TOOL_SECONDARY * P.TOOL_SHARE[False][cl] * P.TOOL_USE[False][cl]
                wood += W.tons_of(cl, use)
            out[county, cl] = dict(wood=wood, pm=wood * W.CLASSES[cl][6] / LB_PER_TON)
    return out


if __name__ == "__main__":
    devs, apps = W.build()
    resp = W.survey(devs)
    ev = evaluate(devs, apps, resp)
    print("devices %d, applications %d, respondents %d" % (len(devs), len(apps), len(resp)))
    keys = ["truth", "golden", "allprimary", "classmean", "survivors", "default"]
    print("area commit | " + " ".join("%-12s" % k for k in keys))
    for code, x in ev.items():
        print("%s  %2d | " % (code, x["commit"]) + " ".join("%5.1f %-6s" % (x["rungs"][k], "TRIG" if x["rungs"][k] < x["commit"] else "")
                                                       for k in keys))
    for k in keys:
        print("%-11s %s" % (k, ",".join(c for c, x in ev.items() if x["rungs"][k] < x["commit"]) or "none"))
    print("golden margins", " ".join("%.1f" % abs(x["reduction"] - x["commit"]) for x in ev.values()))
