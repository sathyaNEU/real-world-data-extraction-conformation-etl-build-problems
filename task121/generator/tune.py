"""Centre every graded figure inside its rounding bin by moving records, never parameters.

Three kinds of move, each confined to one population:
  - drop basket-exit sessions (no order, payment or address) from a population and week, which lowers
    that week's lost orders by the population's baseline conversion per session dropped;
  - scale the net order values of one account class, which moves one population's order value;
  - re-code one payment attempt between frictionless and challenged, or add one declined attempt,
    which moves one population's challenge share."""
import datetime as dt

import numpy as np

import analysis as N
import assemble as A
import params as P

# targets for the fractional part of each population's weekly lost orders
W4_FRAC = {"P4": 0.25, "P3": 0.05, "P1": 0.0, "P2": 0.0, "P5": 0.0}
AOV_KEY = {"P1": "CP4", "P3": "XY", "P4": "MEMBER", "P2": "NV", "P5": "MIXED"}


def frac(x):
    return x - np.floor(x)


def reservoir(T, s, pop, week, removed):
    """Early-exit sessions (basket, contact, address: no order, payment or address record) of one
    population and week whose removal touches nothing else and leaves the population's accounts as
    they were."""
    sk = T["sk"].set_index("session_id")
    early = s.furthest_step.isin(["basket", "contact", "address"])
    if pop == "P5":
        x = s[(s.week == week) & s.P5 & early & (s.vtype == "NV")]
        return sorted(i for i in x.session_id if i not in removed)
    x = s[(s.week == week) & s[pop] & early & ~s.P5.astype(bool)]
    ids = [i for i in x.session_id if i not in removed]
    if pop == "P1":
        ids = [i for i in ids if not sk.p1_trigger[i]]
    if pop in ("P1", "P3", "P4"):
        col = "chain_account" if pop == "P4" else "account_id"
        win = s[s.week.isin(P.REVIEW) & s[pop]]
        cnt = win.groupby(col).size().to_dict()
        acct = dict(zip(win.session_id, win[col]))
        wk = win[win.week == week].groupby(col).size().to_dict()
        ids = [i for i in ids if cnt[acct[i]] >= 3 and wk.get(acct[i], 0) >= 2]
    return sorted(ids)


def _dev(v):
    return v - np.round(v)


def tune_losses(T, K, log):
    for rnd in range(3):
        pk = A.assemble(T, K)
        s = N.enrich(pk)
        base = N.baselines(s)
        L = N.losses(s, base)
        moved = 0
        for p in N.POPS:
            for w in ("W4", "W1", "W3", "W2"):
                if w == "W4":
                    tgt = W4_FRAC[p]
                elif w == "W2":
                    tgt = frac(-(_dev(L[p]["W1"]) + _dev(L[p]["W3"]) + _dev(L[p]["W4"])))
                else:
                    tgt = 0.0
                b = base[p]
                v = L[p][w]
                ids = reservoir(T, s, p, w, K["remove"])
                r = None
                for tol in (max(0.03, b / 2 + 1e-9), 0.1, 0.2):
                    for rr in range(0, len(ids) + 1):
                        if abs(frac(v - rr * b - tgt + 0.5) - 0.5) <= tol:
                            r = rr
                            break
                    if r is not None:
                        break
                assert r is not None, (p, w, v, len(ids))
                if r == 0:
                    continue
                K["remove"].update(ids[:r])
                L[p][w] = v - r * b
                moved += r
        log.append(f"loss round {rnd}: removed {moved} sessions")
        if moved == 0:
            break
    return K


def tune_aov(T, K, log):
    for p in ("P1", "P3", "P4", "P2", "P5"):
        key = AOV_KEY[p]
        for it in range(6):
            pk = A.assemble(T, K)
            s = N.enrich(pk)
            base = N.baselines(s)
            L = N.losses(s, base)
            av = N.aovs(pk, s)
            l3 = L[p]["W4"] * av[p]
            tgt = round(l3 / 100.0) * 100.0
            if abs(l3 - tgt) <= 12 or abs(L[p]["W4"]) < 0.4:
                break
            want = tgt / L[p]["W4"]
            f = K["scale"].get(key, 1.0) * (1 + (want - av[p]) / av[p] * (1.0 if p != "P5" else 1.6))
            assert 0.75 < f < 1.3, (p, f)
            K["scale"][key] = round(f, 4)
        log.append(f"aov {p}: scale {K['scale'].get(key, 1.0)}, sales lost {l3:.1f}")
    return K


def _ok_share(k, n):
    v = 1000.0 * k / n
    fr = frac(v)
    return (fr <= 0.3 or fr >= 0.7) and abs(v - round(v)) > 1e-9


def tune_shares(T, K, log):
    pk = A.assemble(T, K)
    s = N.enrich(pk)
    sk = T["sk"]
    att = T["attempts"]
    sid_of = dict(zip(sk.session_id, sk.index))
    for p in N.POPS:
        x = s[(s.week == "W4") & s[p]]
        if p == "P5":
            x = x[~x.P1 & ~x.P3]
        else:
            x = x[~x.P5]
        idx = {sid_of[i] for i in x.session_id}
        a = att[att.sidx.isin(idx)].sort_values(["sidx", "seq"])
        sh = N.challenge_shares(pk, s)[p]
        k, n = sh[1], sh[2]
        if _ok_share(k, n):
            log.append(f"share {p}: {k}/{n} kept")
            continue
        up = a[(a.authorised == "Y") & a.outcome.isin(["Y", "I"]) & ~a.attempt_ref.isin(K["flip"])]
        dn = a[(a.authorised == "Y") & a.outcome.isin(["C", "D"]) & ~a.attempt_ref.isin(K["flip"])]
        best = None
        for dk in range(-3, 4):
            for dn_ in range(0, 6):
                for ce in range(0, dn_ + 1):
                    kk, nn = k + dk + ce, n + dn_
                    if (dk > 0 and dk > len(up)) or (dk < 0 and -dk > len(dn)):
                        continue
                    if _ok_share(kk, nn):
                        cost = abs(dk) + dn_
                        dist = abs(frac(1000.0 * kk / nn + 0.5) - 0.5)
                        cand = (cost, dist, dk, dn_, ce)
                        if best is None or cand < best:
                            best = cand
        assert best, (p, k, n, len(up), len(dn))
        _, _, dk, dn_, ce = best
        if dk > 0:
            for r in up.attempt_ref[:dk]:
                iss = a.issuer[a.attempt_ref == r].iloc[0]
                K["flip"][r] = "D" if iss == P.ISSUER_X else "C"
        elif dk < 0:
            for r in dn.attempt_ref[:-dk]:
                K["flip"][r] = "Y"
        hosts = sorted(set(a.sidx))
        for j in range(dn_):
            h = hosts[j % len(hosts)]
            iss = a.issuer[a.sidx == h].iloc[0]
            code = ("D" if iss == P.ISSUER_X else "C") if j < ce else "N"
            K["extra"][f"PA{(0x5a3c00 + h * 7 + j):012x}"[:14]] = (int(h), code)
        log.append(f"share {p}: {k}/{n} -> dk {dk}, extra {dn_} ({ce} challenged)")
    return K


def tune_cohorts(T, K, log):
    pk = A.assemble(T, K)
    s = N.enrich(pk)
    sk = T["sk"].set_index("session_id")
    cs = N.cohort_sheet(s)
    for c in range(1, 13):
        n, v = cs[c]
        conv = round(v / 100 * n)
        pool = s[s.week.isin(["W2", "W3"]) & s.signed_in & (s.cohort == c) & (s.furthest_step == "basket")
                 & ~s.P1 & ~s.P3 & ~s.P5]
        pool = [i for i in pool.session_id if sk.klass[i] == "OTHER" and i not in K["remove"]]
        for r in range(0, 60):
            val = 10000.0 * conv / (n - r)
            if abs(frac(val + 0.5) - 0.5) <= 0.2:
                break
        K["remove"].update(sorted(pool)[:r])
        log.append(f"cohort {c}: removed {r}")
    return K


def tune(T):
    K = A.empty_knobs()
    log = []
    tune_losses(T, K, log)
    tune_aov(T, K, log)
    tune_shares(T, K, log)
    tune_cohorts(T, K, log)
    return K, log
