"""Design aid, run once: the expected build-up by month in use, and each ward's settled stock sized so that the
default route (the 2026 register plus the trajectory's dwellings at the settled ratio by type) lands each ward at its
TARGET_DEFAULT variance. Prints the ladder on expected values. Its output is pasted into world.SETTLED."""
import json
import numpy as np
import world as W


def curves(seed=2, n_settled=30000, n_new=3000):
    rng = np.random.default_rng(seed)
    out = {}
    for typ in ["house", "flat"]:
        st = np.mean([W.count_on(W.history(rng, typ, W.mindex(1980, 1), 2012), 2012) for _ in range(n_settled)])
        cv = {}
        for mm in range(1, 13):
            cs = np.zeros(24)
            for _ in range(n_new):
                hh = W.history(rng, typ, W.mindex(2000, mm), 2023)
                cs += np.array([W.count_on(hh, Y) for Y in range(2000, 2024)])
            cv[mm] = cs / n_new / st
        out[typ] = (st, cv)
    return out


def site_months(phasing):
    """(year, month, share of the site) for each month of each monitoring year, spread evenly"""
    rows = []
    for my, share in phasing.items():
        for (y, m) in W.months_of(my):
            rows.append((y, m, share / 12.0))
    return rows


NEWBUILD = {}


def expected(cur, settled, method, Y=W.HORIZON):
    S = {t: cur[t][0] for t in cur}
    out = {}
    for code, name, cl, role, npd in W.WARDS:
        base = sum(settled[code][t] * S[t] for t in ("house", "flat"))
        e = base
        for (wc, sname, nh, nf, ph) in W.all_sites():
            if wc != code:
                continue
            for (y, m, sh) in site_months(ph):
                for t, n in (("house", nh), ("flat", nf)):
                    d = n * sh
                    built = (y, m) <= W.CUT
                    in_by = (y, m) <= (Y, 10)
                    def cov(Yr):
                        i = Yr - y
                        return 0.0 if i < 0 else float(cur[t][1][m][min(i, 23)])
                    on_reg = (y, m) <= (2025, 10)
                    if method == "golden":
                        if in_by:
                            e += d * S[t] * cov(Y)
                    elif method == "default":
                        if on_reg:
                            e += d * S[t] * cov(2025)
                        elif in_by:
                            e += d * S[t]
                    elif method == "catchup":
                        if in_by:
                            e += d * S[t]
                    elif method == "future_only":
                        if on_reg:
                            e += d * S[t] * cov(2025)
                        elif in_by:
                            e += d * S[t] * cov(Y)
                    elif method == "newbuild":
                        if on_reg:
                            e += d * S[t] * cov(2025)
                        elif in_by:
                            e += d * NEWBUILD[t]
                    elif method == "register2025":
                        if on_reg:
                            e += d * S[t] * cov(2025)
        out[code] = (cl, e)
    return out


def variances(fig):
    tot = sum(e for cl, e in fig.values())
    avg = tot / W.COUNCIL_SIZE
    return {w: 100.0 * (e / cl / avg - 1.0) for w, (cl, e) in fig.items()}, avg, tot


if __name__ == "__main__":
    cur = curves()
    S = {t: cur[t][0] for t in cur}
    print("settled electors per dwelling", {t: round(v, 3) for t, v in S.items()})
    settled = {code: {"house": 1000, "flat": 300} for code, *_ in W.WARDS}
    for it in range(40):
        v, avg, tot = variances(expected(cur, settled, "default"))
        for code, name, cl, role, npd in W.WARDS:
            fig = expected(cur, settled, "default")[code][1]
            base = sum(settled[code][t] * S[t] for t in S)
            sites = fig - base
            need = (1 + W.TARGET_DEFAULT[code] / 100.0) * 2700.0 * cl - sites
            fs = W.FLAT_SHARE[code]
            per = (1 - fs) * S["house"] + fs * S["flat"]
            n = need / per
            settled[code] = {"house": int(round(n * (1 - fs))), "flat": int(round(n * fs))}
    # the ratio a reader reads off dwellings completed in the five years to 30 September 2026, on the 2026 register
    for t in ("house", "flat"):
        num = den = 0.0
        for (wc, sname, nh, nf, ph) in W.all_sites():
            n = nh if t == "house" else nf
            for (y, m, sh) in site_months(ph):
                if (2020, 10) <= (y, m) <= (2025, 10):
                    num += n * sh * S[t] * float(cur[t][1][m][2025 - y]); den += n * sh
        NEWBUILD[t] = num / den
    print("new-build ratio", {t: round(v, 3) for t, v in NEWBUILD.items()})
    for m in ["register2025", "default", "newbuild", "catchup", "future_only", "golden"]:
        v, avg, tot = variances(expected(cur, settled, m, 2025 if m == "register2025" else W.HORIZON))
        print(m.ljust(13), "total %6.0f avg %5.0f outside %s" % (tot, avg, sorted(w for w, x in v.items() if abs(x) > 10)))
    vd, _, _ = variances(expected(cur, settled, "default"))
    vg, _, _ = variances(expected(cur, settled, "golden"))
    v26, _, _ = variances(expected(cur, settled, "register2025", 2025))
    for code, name, cl, role, npd in W.WARDS:
        print("%s %-19s %d %-2s 2025 %+6.1f default %+6.1f golden %+6.1f  settled %s" % (
            code, name, cl, role, v26[code], vd[code], vg[code], settled[code]))
    json.dump(settled, open("settled_tuned.json", "w"), indent=1)
