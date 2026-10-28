"""task464 architecture 9: the golden's estimator family, measured on the cut pack.

Every form a competent analyst running patients to their review would use: the record's re-authorisation rate
pooled or by practice, from the whole record or its last fourteen months, re-authorisation counted within 60 or
90 days; stops between reviews pooled or by practice, split by time on treatment or flat; requests paced at the
record's mean interval, its median or the issue length; a review already passed without a new repeat read as
lapsed or at the record's rate. The graded figures must print the same under every member (inside 0.4 of the
printed unit, the design note's closure line).
"""
import collections, json, os, sys
import answers as A
import world as W

FIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "family.json")


def members(D=None):
    D = D or A.Data()
    pop = A.population(D)
    pool, n, f = A.reauth_rate(D)
    perp, _, _ = A.reauth_rate(D, per=True)
    recent, _, _ = A.reauth_rate(D, lo=W.ASOF - 420)
    perp_recent, _, _ = A.reauth_rate(D, lo=W.ASOF - 420, per=True)
    f90, _, _ = A.reauth_rate(D, follow=90)
    bg = A.stop_rates(D); bgp = A.stop_rates(D, per=True); bgf = A.stop_rates(D, split=False)
    pm, pmed = A.pacing(D)
    stay = A.stay_share(D)
    M = {}
    M["golden"] = A.golden(D, pop, pool, bg, pm, stay)
    M["rate by practice"] = A.golden(D, pop, perp, bg, pm, stay)
    M["rate, last 14 months"] = A.golden(D, pop, recent, bg, pm, stay)
    M["rate by practice, last 14 months"] = A.golden(D, pop, perp_recent, bg, pm, stay)
    M["re-authorised within 90 days"] = A.golden(D, pop, f90, bg, pm, stay)
    M["stops by practice"] = A.golden(D, pop, pool, bgp, pm, stay)
    M["stops flat"] = A.golden(D, pop, pool, bgf, pm, stay)
    M["stops at a 90-day gap"] = A.golden(D, pop, pool, A.stop_rates(D, gap=90), pm, stay)
    M["paced at the issue length"] = A.golden(D, pop, pool, bg, 0, stay)
    M["paced at the median"] = A.golden(D, pop, pool, bg, pmed, stay)
    M["passed review at the rate"] = A.golden(D, pop, pool, bg, pm, stay, pending="rate")
    return M


def main(write=True):
    M = members()
    codes = sorted(M["golden"], key=lambda c: -M["golden"][c])
    out = {}
    for c in codes:
        vals = [m[c] for m in M.values()]
        out[c] = dict(min=min(vals), max=max(vals), golden=M["golden"][c],
                      printed=sorted({int(round(v / W.ROUND_TO) * W.ROUND_TO) for v in vals}))
    tops = {k: max(m, key=m.get) for k, m in M.items()}
    res = dict(members={k: {c: round(v, 2) for c, v in m.items()} for k, m in M.items()}, by_practice=out, tops=tops)
    if write:
        json.dump(res, open(FIG, "w"), indent=1, sort_keys=True)
    return res


if __name__ == "__main__":
    r = main()
    nm = {p["code"]: p["name"] for p in W.PRACTICES}
    for c, v in r["by_practice"].items():
        print("%-28s golden %6.1f  family %6.1f to %6.1f  prints %s" % (nm[c], v["golden"], v["min"], v["max"], v["printed"]))
    print("top under every member:", sorted(set(r["tops"].values())))
    for k, m in r["members"].items():
        print("  %-36s" % k, " ".join("%s %5.1f" % (W.BY_CODE[c]["key"], m[c]) for c in sorted(m, key=lambda c: W.BY_CODE[c]["key"])))
