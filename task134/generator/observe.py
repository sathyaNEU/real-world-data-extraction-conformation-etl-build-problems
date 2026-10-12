"""What the partnership's systems hold on Monday 18 January 2027: the case system's placements, the finance system's
free personal and nursing care payment lines and charging assessments, the client crosswalk from the 2023 case system
replacement, the National Records of Scotland death linkage, the care home register and the postcode lookup.

Every frame is built from the true timeline (sim.py) and the attributes drawn here on their own random streams, so
the call's timeline never moves when an ask-side attribute is redrawn."""
import datetime as dt

import numpy as np
import pandas as pd

import world as W

D = dt.date
MONTH = W.MONTH
INF = np.inf


def ds(day):
    return W.dd(day).isoformat() if np.isfinite(day) else ""


class Obs:
    pass


# ------------------------------------------------------------------------------------------------ identities

def identities(S, rng):
    """client numbers (the 2023 system's, and the old system's for anyone known before the go-live), debtor
    references, and the merged duplicate records"""
    n = S.n
    order = np.argsort(S.admit, kind="stable")
    cid = np.empty(n, object)
    nxt = 4001873
    for i in order:
        nxt += int(rng.integers(1, 9))
        cid[i] = "%08d" % (40000000 + nxt)
    legacy = np.empty(n, object)
    used = set()
    for i in range(n):
        if S.admit[i] < W.GOLIVE:
            while True:
                v = "SWS%06d" % int(rng.integers(100000, 699999))
                if v not in used:
                    used.add(v)
                    break
            legacy[i] = v
        else:
            legacy[i] = ""
    debtor = np.empty(n, object)
    used = set()
    for i in order:
        while True:
            v = "30%07d" % int(rng.integers(1000000, 9999999))
            if v not in used:
                used.add(v)
                break
        debtor[i] = v
    return cid, legacy, debtor, used


# ------------------------------------------------------------------------------------------------ homes

def service_numbers(S, rng):
    """Care Inspectorate service numbers: CS + registration year + six digits"""
    svc = {}
    used = set()
    for k, h in enumerate(S.H):
        if h["ooa"]:
            yr = int(rng.integers(2002, 2006))
        else:
            yr = W.dd(h["opened"]).year if h["opened"] > 0 else 2003
            reg = [x for x in W.HOMES if x[0] == h["name"]][0][5]
            yr = int(reg[:4])
        while True:
            v = "CS%d%06d" % (yr, int(rng.integers(300000, 399999)))
            if v not in used:
                used.add(v)
                break
        svc[k] = v
    new = {}
    for name, (prov, day) in W.REREG.items():
        while True:
            v = "CS%d%06d" % (W.dd(day).year, int(rng.integers(370000, 399999)))
            if v not in used:
                used.add(v)
                break
        new[name] = v
    return svc, new


def postcodes(rng):
    """the partnership's postcode units by locality, and one unit for each home"""
    letters = "ABDEFGHJLNPQRSTUWXYZ"
    rows = []
    seen = set()
    for loc in W.LOCS:
        for dist in W.DISTRICTS[loc]:
            sectors = sorted(rng.choice(np.arange(1, 10), size=int(rng.integers(3, 6)), replace=False))
            for sec in sectors:
                for _ in range(int(rng.integers(70, 150))):
                    pc = "%s %d%s%s" % (dist, sec, letters[rng.integers(20)], letters[rng.integers(20)])
                    if pc not in seen:
                        seen.add(pc)
                        rows.append((pc, loc))
    return rows


# ------------------------------------------------------------------------------------------------ the observation

def observe(S, seed=W.SEED):
    O = Obs()
    rng = np.random.default_rng(seed + 101)
    O.cid, O.legacy, O.debtor, debtor_used = identities(S, rng)
    used_c = set(O.cid)
    used_l = set(x for x in O.legacy if x)
    rng_a = np.random.default_rng(seed + 111)

    def alloc(st, en):
        while True:
            c = "%08d" % (40000000 + int(rng_a.integers(4001000, 4990000)))
            if c not in used_c:
                used_c.add(c)
                break
        leg = ""
        if st < W.GOLIVE:
            while True:
                leg = "SWS%06d" % int(rng_a.integers(100000, 699999))
                if leg not in used_l:
                    used_l.add(leg)
                    break
        return c, leg
    O.alloc = alloc
    rng_h = np.random.default_rng(seed + 202)
    O.svc, O.svc_new = service_numbers(S, rng_h)
    O.pcs = postcodes(rng_h)
    by_loc = {}
    for pc, loc in O.pcs:
        by_loc.setdefault(loc, []).append(pc)
    O.home_pc = {}
    for k, h in enumerate(S.H):
        if not h["ooa"]:
            lst = by_loc[h["loc"]]
            O.home_pc[k] = lst[int(rng_h.integers(len(lst)))]
    O.rereg_idx = {k: W.REREG[h["name"]] for k, h in enumerate(S.H) if h["name"] in W.REREG}
    # which residents' placements were moved to the new registration (the rest stay on the old service number)
    rng_r = np.random.default_rng(seed + 303)
    O.rereg_updated = rng_r.random(S.n) < 0.55
    O.ask = ask_attributes(S, O, np.random.default_rng(seed + 404))
    O.placements, O.stays_meta = placements(S, O, np.random.default_rng(seed + 505))
    O.short = short_placements(S, O, np.random.default_rng(seed + 606))
    O.lines = payment_lines(S, O, np.random.default_rng(seed + 707))
    O.merged = merged_duplicates(S, O, np.random.default_rng(seed + 808), debtor_used)
    O.assess = assessments(S, O, np.random.default_rng(seed + 909))
    O.crosswalk = crosswalk(S, O)
    O.deaths = death_linkage(S, O, np.random.default_rng(seed + 1010))
    return O


def home_at(S, i, day):
    h = int(S.home[i])
    for t, nh in S.moves.get(i, []):
        if t <= day:
            h = nh
    return h


def svc_for(S, O, i, h, day, episode_start):
    """the service number the case system holds on an episode: a re-registered home's new number from the date of
    the new registration for placements the contracts team updated, and for any episode opened after that date"""
    k = h
    if k in O.rereg_idx:
        prov, rday = O.rereg_idx[k]
        # a placement that began after the new registration carries its number; an older one carries it only if the
        # contracts team updated it (later episodes copy the service number from the episode before)
        began = S.conv[i] if (S.kind[i] == 1 and np.isfinite(S.conv[i])) else S.admit[i]
        moved_in = max([t for t, nh in S.moves.get(i, []) if nh == k and t <= day] or [began])
        if moved_in >= rday or (O.rereg_updated[i] and day >= rday):
            return O.svc_new[S.H[k]["name"]]
    return O.svc[k]


# ------------------------------------------------------------------------------------------------ ask attributes

def ask_attributes(S, O, rng):
    """fee supplements by stay and home, and the charging history: the contribution assessed at funding start and the
    change at each annual review"""
    A = Obs()
    n = S.n
    # a supplement agreed for the resident, about one placement in ten, likelier in the larger provider groups
    A.supp_p = np.array([0.20 if h["prov"] in ("Kingsbrae Healthcare Ltd", "Larchgrove Living Ltd", "Pinewell Care Homes Ltd")
                         else 0.13 if h["ooa"] else 0.06 for h in S.H])
    A.supp_draw = rng.random((n, 4))
    A.supp_amt = np.round(rng.uniform(16, 150, (n, 4)) / 0.5) * 0.5
    # contribution at funding start: pension income less the personal expenses allowance; residents from the
    # Allanvale and Dunmorrow teams have larger occupational pensions on average
    team_mean = np.array([268.0, 214.0, 202.0, 249.0, 226.0])
    base = team_mean[S.team] + rng.normal(0, 48, n)
    conv_extra = rng.uniform(8, 52, n)          # tariff income on capital between the limits, for a conversion
    A.c0 = np.clip(np.where(S.kind == 1, base + conv_extra, base), 0, 470)
    nil = rng.random(n) < 0.018
    A.c0[nil] = 0.0
    A.review_ch = rng.normal(0.035, 0.03, (n, 30))       # proportional change at each annual review
    A.review_jump = np.where(rng.random((n, 30)) < 0.12, rng.normal(0, 30, (n, 30)), 0.0)
    A.lead = rng.uniform(7, 36, (n, 30))                 # days a review is completed before it takes effect
    A.lag0 = rng.uniform(9, 58, n)                       # days after funding starts that the first assessment completes
    return A


def supplement(S, O, i, h, k):
    A = O.ask
    if A.supp_draw[i, k % 4] < A.supp_p[h]:
        return float(A.supp_amt[i, k % 4])
    return 0.0


# ------------------------------------------------------------------------------------------------ placements

def cf_stays(S):
    """council-funded long-stay stays: (person, entry, route)"""
    out = []
    for i in range(S.n):
        if S.kind[i] == 0:
            out.append((i, S.admit[i], "DIRECT"))
        elif np.isfinite(S.conv[i]):
            out.append((i, S.conv[i], "CONV"))
    return out


def death_key_lag(rng):
    return float(np.ceil(rng.exponential(9.0)))


def placements(S, O, rng):
    rows = []
    meta = {}
    cut = W.ASOF
    for i, entry, route in cf_stays(S):
        ex = S.exit[i]
        if route == "CONV" and entry + O.ask.lag0[i] > W.EXTRACT:
            continue                                  # the funding decision is not yet recorded
        if entry > cut or (np.isfinite(ex) and ex <= W.HIST_START - 400):
            continue
        # every episode of a stay in place at any time from 1 April 2021
        if np.isfinite(ex) and ex <= W.HIST_START:
            continue
        bounds = [entry]
        y = W.fy(entry) + 1
        while W.fy_start(y) < min(ex, cut + 1):
            bounds.append(float(W.fy_start(y)))
            y += 1
        mv = [t for t, nh in S.moves.get(i, []) if entry < t < min(ex, cut + 1)]
        reg_split = []
        for k, (prov, rday) in O.rereg_idx.items():
            if entry < rday < min(ex, cut + 1) and O.rereg_updated[i] and home_at(S, i, rday) == k:
                reg_split.append(float(rday))
        cuts = sorted(set(bounds + mv + reg_split))
        lag = death_key_lag(rng) if S.why[i] == 1 else float(rng.integers(1, 9))
        keyed = np.isfinite(ex) and ex <= cut and ex + lag <= W.EXTRACT
        for j, st in enumerate(cuts):
            en_next = cuts[j + 1] if j + 1 < len(cuts) else None
            h = home_at(S, i, st)
            if en_next is not None:
                end = en_next - 1
                reason = "MOVE" if en_next in mv else ("SVC" if en_next in reg_split else "FEE")
            elif keyed:
                end = ex
                reason = "DIED" if S.why[i] == 1 else "DISCH"
            else:
                end = INF
                reason = ""
            nmov = sum(1 for t in mv if t <= st)
            fee = W.NCHC[W.fy(st)][S.care[i]] + supplement(S, O, i, h, nmov)
            client = O.legacy[i] if (np.isfinite(end) and end < W.GOLIVE and O.legacy[i]) else O.cid[i]
            rows.append(dict(_i=i, _st=st, client_id=client, service_no=svc_for(S, O, i, h, st, st),
                             placement_type="PERM", route=route, care_type="Nursing" if S.care[i] else "Residential",
                             admitted=ds(S.admit[i]), start_date=ds(st), end_date=ds(end), end_reason=reason,
                             weekly_fee=round(fee, 2), locality=W.LOCS[S.team[i]], _end=end, _h=h))
        meta[i] = dict(keyed=keyed, lag=lag)
    return rows, meta


def short_placements(S, O, rng):
    """interim placements from hospital and respite breaks, from 1 April 2021"""
    rows = []
    homes = [k for k, h in enumerate(S.H) if not h["ooa"]]
    w = np.array([S.H[k]["places"] for k in homes], float)
    d = W.HIST_START
    k = 0
    people = []
    while d < W.ASOF + 1:
        for ptype, lam, lo, hi in (("INT", 23.5, 14, 84), ("RESP", 19.0, 7, 28)):
            for _ in range(rng.poisson(lam * 7 / MONTH)):
                st = float(d + rng.integers(0, 7))
                if st > W.ASOF:
                    continue
                dur = float(rng.integers(lo, hi + 1))
                care = int(rng.random() < (0.55 if ptype == "INT" else 0.3))
                hk = homes[rng.choice(len(homes), p=w / w.sum())]
                if care and not S.H[hk]["nursing"]:
                    cands = [x for x in homes if S.H[x]["nursing"]]
                    hk = cands[int(rng.integers(len(cands)))]
                if S.H[hk]["opened"] > st:
                    continue
                team = int(rng.choice(5, p=W.TEAM_W))
                people.append((st, st + dur, ptype, care, hk, team))
        d += 7
    people.sort()
    O.short_people = []
    for st, en, ptype, care, hk, team in people:
        cid, leg = O.alloc(st, en)
        O.short_people.append((cid, leg))
        if leg and en < W.GOLIVE:
            cid = leg
        end = en if en <= W.ASOF else INF
        if np.isfinite(end) and en + 5 > W.EXTRACT:
            end = INF
        fee = W.NCHC[W.fy(st)][care]
        rows.append(dict(_i=-1, _st=st, client_id=cid, service_no=O.svc[hk] if hk not in O.rereg_idx or st < O.rereg_idx[hk][1]
                         else O.svc_new[S.H[hk]["name"]], placement_type=ptype, route="",
                         care_type="Nursing" if care else "Residential", admitted=ds(st), start_date=ds(st),
                         end_date=ds(end), end_reason="ENDED" if np.isfinite(end) else "", weekly_fee=round(fee, 2),
                         locality=W.LOCS[team], _end=end, _h=hk))
    return rows


# ------------------------------------------------------------------------------------------------ payment lines

PERIOD0 = W.dn(D(2021, 4, 1))


def periods():
    out = []
    t = PERIOD0
    while t + 27 <= W.ASOF:
        y = W.fy(t + 3)
        out.append((t, t + 27, y))
        t += 28
    lab = []
    count = {}
    for s, e, y in out:
        count[y] = count.get(y, 0) + 1
        lab.append((s, e, "%d-%02d P%02d" % (y, (y + 1) % 100, count[y])))
    return lab


LATE_UPRATING = {2022: 3, 2024: 3}       # financial years whose new rates were paid from the third period, with arrears


def payment_lines(S, O, rng):
    P = periods()
    rows = []
    award = {}
    for i in range(S.n):
        if S.kind[i] != 1:
            continue
        a = S.admit[i]
        ast = a + float(rng.integers(0, 43))
        end_ev = min(S.conv[i], S.exit[i])
        if ast >= end_ev:
            continue
        if np.isfinite(S.conv[i]) and S.conv[i] < S.exit[i]:
            aend, why = S.conv[i] - 1, "CF"
        else:
            aend, why = S.exit[i], ("DIED" if S.why[i] == 1 else "LEFT")
        if aend < W.HIST_START:
            continue
        if ast > P[-1][1]:
            continue
        lag = death_key_lag(rng) if why == "DIED" else float(rng.integers(2, 12))
        if why == "CF":
            lag = float(O.ask.lag0[i]) + 1          # the award is ended when the funding decision is recorded
        known = np.isfinite(aend) and aend <= W.ASOF and aend + lag <= W.EXTRACT
        shown_end = aend if known else INF
        award[i] = dict(start=ast, end=aend, why=why if known else "", shown=shown_end, lag=lag)
        for ps, pe, lab in P:
            lo, hi = max(ps, ast, W.HIST_START), min(pe, aend if np.isfinite(aend) else pe)
            if hi < lo:
                continue
            # a line is paid for the period once the period ends; days after an exit not yet notified are paid and
            # recovered later
            paid_to = pe if (not np.isfinite(aend) or aend + lag > pe + 3) and aend >= ps else hi
            paid_to = min(paid_to, pe)
            y = W.fy(ps + 3)
            for comp, k in (("FPC", 0), ("FNC", 1)):
                if comp == "FNC" and not S.care[i]:
                    continue
                days = paid_to - lo + 1
                if days <= 0:
                    continue
                rate_y = y
                if y in LATE_UPRATING and int(lab[-2:]) < LATE_UPRATING[y]:
                    rate_y = y - 1
                amt = round(W.FPNC[rate_y][k] * days / 7.0, 2)
                h = home_at(S, i, lo)
                svc = O.svc_new[S.H[h]["name"]] if (h in O.rereg_idx and lo >= O.rereg_idx[h][1]) else O.svc[h]
                rows.append((i, O.debtor[i], svc, ds(S.admit[i]), ds(ast), lab, ds(ps), ds(pe), comp, amt))
                if paid_to > hi and np.isfinite(aend) and known:
                    rec = round(-W.FPNC[rate_y][k] * (paid_to - hi) / 7.0, 2)
                    rows.append((i, O.debtor[i], svc, ds(S.admit[i]), ds(ast), lab, ds(ps), ds(pe), "ADJ", rec))
            # hospital absences: a reduction for days in hospital
            if rng.random() < 0.025 and paid_to - lo > 10:
                k = int(rng.integers(3, 15))
                rows.append((i, O.debtor[i], O.svc[home_at(S, i, lo)] if home_at(S, i, lo) not in O.rereg_idx or lo < O.rereg_idx[home_at(S, i, lo)][1]
                             else O.svc_new[S.H[home_at(S, i, lo)]["name"]], ds(S.admit[i]), ds(ast), lab, ds(ps), ds(pe),
                             "HOSP", round(-W.FPNC[y][0] * k / 7.0, 2)))
        # arrears for a late uprating, paid in the third period of the year
        for y, pnum in LATE_UPRATING.items():
            ys = [p for p in P if p[2].startswith("%d-" % y)]
            if len(ys) < pnum:
                continue
            ps, pe, lab = ys[pnum - 1]
            early = [p for p in ys[:pnum - 1]]
            for comp, k in (("FPC", 0), ("FNC", 1)):
                if comp == "FNC" and not S.care[i]:
                    continue
                days = 0
                for qs, qe, _ in early:
                    lo, hi = max(qs, ast, W.HIST_START), min(qe, aend if np.isfinite(aend) else qe)
                    days += max(0, hi - lo + 1)
                if days <= 0 or (np.isfinite(aend) and aend < ps):
                    continue
                arr = round((W.FPNC[y][k] - W.FPNC[y - 1][k]) * days / 7.0, 2)
                h = home_at(S, i, ps)
                svc = O.svc_new[S.H[h]["name"]] if (h in O.rereg_idx and ps >= O.rereg_idx[h][1]) else O.svc[h]
                rows.append((i, O.debtor[i], svc, ds(S.admit[i]), ds(ast), lab, ds(ps), ds(pe), "ADJ", arr))
    df = pd.DataFrame(rows, columns=["_i", "debtor_ref", "service_no", "admitted", "award_start", "period", "period_start",
                                     "period_end", "line_type", "amount"])
    df["award_end"] = [ds(award[i]["shown"]) for i in df["_i"]]
    df["end_reason"] = [award[i]["why"] for i in df["_i"]]
    O.award = award
    return df


# ------------------------------------------------------------------------------------------------ crosswalk, merges

def merged_duplicates(S, O, rng, used):
    """people the old system held twice: both records migrated and were merged in the new system; the finance system
    kept both debtor references, and later assessments were raised under the second"""
    out = {}
    cand = [i for i in range(S.n) if (S.kind[i] == 0 or np.isfinite(S.conv[i])) and S.admit[i] < W.GOLIVE - 200
            and S.exit[i] > W.ASOF]
    pick = rng.choice(cand, size=int(round(len(cand) * 0.075)), replace=False)
    nxt = 4900000
    for i in sorted(pick):
        while True:
            v = "30%07d" % int(rng.integers(1000000, 9999999))
            if v not in used:
                used.add(v)
                break
        nxt += int(rng.integers(3, 60))
        out[int(i)] = dict(debtor2=v, legacy2="SWS%06d" % int(rng.integers(700000, 799999)), cid2="%08d" % (40000000 + nxt),
                           switch=float(W.GOLIVE + rng.integers(30, 900)))
    return out


def crosswalk(S, O):
    rows = []
    seen = set()
    for i in range(S.n):
        # everyone with a placement, a payment line or an assessment in the extracts
        rows.append(dict(_i=i, legacy_client_no=O.legacy[i], client_id=O.cid[i], debtor_ref=O.debtor[i], merged_into=""))
        if i in O.merged:
            m = O.merged[i]
            rows.append(dict(_i=i, legacy_client_no=m["legacy2"], client_id=m["cid2"], debtor_ref=m["debtor2"],
                             merged_into=O.cid[i]))
    for cid, leg in O.short_people:
        rows.append(dict(_i=-1, legacy_client_no=leg, client_id=cid, debtor_ref="", merged_into=""))
    return rows


# ------------------------------------------------------------------------------------------------ assessments

def assessments(S, O, rng):
    A = O.ask
    rows = []
    for i in range(S.n):
        if S.kind[i] == 1:
            aw = O.award.get(i)
            if aw is not None and S.admit[i] >= W.HIST_START - 400:
                c = aw["start"] + float(rng.integers(3, 30))
                if c <= W.EXTRACT:
                    rows.append(dict(_i=i, _ref=O.debtor[i], completed=c, effective=aw["start"], amount=np.nan, outcome="SELF"))
        if S.kind[i] == 0:
            entry = S.admit[i]
        elif np.isfinite(S.conv[i]):
            entry = S.conv[i]
        else:
            continue
        ex = S.exit[i]
        if np.isfinite(ex) and ex < W.HIST_START:
            continue
        amt = float(A.c0[i])
        k = 0
        eff = entry
        comp = entry + A.lag0[i]
        if S.kind[i] == 0 and entry <= W.ASOF and comp > W.EXTRACT - 2:
            comp = W.EXTRACT - 2 - (i % 5)          # a December admission is assessed before the extract
        while True:
            ref = O.debtor[i]
            if i in O.merged and comp >= O.merged[i]["switch"]:
                ref = O.merged[i]["debtor2"]
            if comp <= W.EXTRACT and eff < ex and eff >= W.HIST_START - 370:
                rows.append(dict(_i=i, _ref=ref, completed=comp, effective=eff, amount=round(amt, 2),
                                 outcome="NIL" if amt == 0 else "ASSESSED"))
            k += 1
            eff = float(W.dn(_anniv(W.dd(entry), k)))
            if eff >= ex or eff > W.EXTRACT + 60:
                break
            comp = eff - A.lead[i, k % 30]
            if amt > 0:
                amt = max(0.0, amt * (1 + A.review_ch[i, k % 30]) + A.review_jump[i, k % 30])
    return rows


def _anniv(d, k):
    try:
        return D(d.year + k, d.month, d.day)
    except ValueError:
        return D(d.year + k, 3, 1)


# ------------------------------------------------------------------------------------------------ deaths

def death_linkage(S, O, rng):
    rows = []
    for i in range(S.n):
        if S.why[i] != 1 or not np.isfinite(S.exit[i]):
            continue
        dd_ = S.exit[i]
        if dd_ < W.HIST_START:
            continue
        reg = dd_ + float(rng.integers(1, 9))
        if reg > W.NRS_CUT:
            continue
        if dd_ > W.ASOF:
            continue
        status = "EXACT" if rng.random() < 0.93 else "PROBABLE"
        rows.append(dict(_i=i, client_id=O.cid[i], date_of_death=ds(dd_), date_registered=ds(reg), match_status=status))
    return rows
