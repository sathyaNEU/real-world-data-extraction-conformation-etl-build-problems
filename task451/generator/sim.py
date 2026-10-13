"""Simulate the Laurelford Fund's world from world.py: the families and their Fund member ids, the hour-bank
eligibility with its late postings, the primary care attribution, the medical claims (every version, both date
clocks, the administrator's two processes), the 2026 pharmacy fills as Corvane keys them, and the partners'
clinicians with the moves of 2026. Deterministic for a seed."""
import datetime as dt

import numpy as np

import world as W

D = dt.date
DAY = dt.timedelta(days=1)


def mkey(d):
    return d.year * 12 + d.month - 1


def mstart(k):
    return D(k // 12, k % 12 + 1, 1)


def mend(k):
    return mstart(k + 1) - DAY


def bday_on_or_after(d):
    while d.weekday() >= 5 or d in W.HOLIDAYS:
        d += DAY
    return d


def next_bday(d):
    return bday_on_or_after(d + DAY)


def thursday_run(d):
    """the weekly run on or after d: Thursday, or the business day before when Thursday is a holiday"""
    t = d + dt.timedelta(days=(3 - d.weekday()) % 7)
    if t in W.HOLIDAYS:
        t -= DAY
        if t < d:
            t += dt.timedelta(days=7)
    return t


def npi(rng, used):
    """a ten-digit NPI with its Luhn check digit (prefix 80840)"""
    while True:
        body = "1" + "".join(str(x) for x in rng.integers(0, 10, 8))
        digits = [int(c) for c in "80840" + body]
        tot = 0
        for i, dgt in enumerate(reversed(digits)):
            if i % 2 == 0:
                dgt *= 2
                if dgt > 9:
                    dgt -= 9
            tot += dgt
        chk = (10 - tot % 10) % 10
        v = body + str(chk)
        if v not in used:
            used.add(v)
            return v


# --------------------------------------------------------------------------------------------------- the people
def families(rng):
    fams, members = [], []
    used = set()
    for f in range(W.SUBSCRIBERS):
        while True:
            sid = "LB%07d" % rng.integers(1000000, 9999999)
            if sid not in used:
                used.add(sid)
                break
        p_age = int(np.clip(rng.normal(43, 11), 21, 66))
        p_dob = D(2026 - p_age, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
        p_gen = "M" if rng.random() < 0.88 else "F"
        # the participant's first eligible month: most before the window, some newly eligible in it
        if rng.random() < 0.88:
            enroll = D(int(rng.integers(2008, 2025)), int(rng.integers(1, 13)), 1)
        else:
            enroll = mstart(int(rng.integers(mkey(D(2025, 2, 1)), mkey(D(2026, 11, 1)))))
        fam = dict(sid=sid, enroll=enroll, members=[])
        people = [dict(rel="P", dob=p_dob, gender=p_gen, enroll=enroll)]
        if rng.random() < W.SPOUSE_SHARE:
            s_age = int(np.clip(p_age + rng.normal(-1.5, 4), 20, 70))
            s_dob = D(2026 - s_age, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
            late = rng.random() < 0.16       # married after the participant enrolled the children
            s_en = enroll if not late else mstart(mkey(enroll) + int(rng.integers(6, 90)))
            people.append(dict(rel="S", dob=s_dob, gender="F" if p_gen == "M" else "M", enroll=s_en))
        nkid = rng.poisson(W.CHILDREN_MEAN) if p_age < 58 else rng.poisson(0.3)
        for _ in range(int(nkid)):
            k_age = int(rng.integers(0, min(26, max(1, p_age - 19))))
            k_dob = D(2026 - k_age, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
            k_en = max(enroll, mstart(mkey(k_dob)))
            if rng.random() < 0.05:          # a stepchild added with a later spouse
                k_en = mstart(mkey(enroll) + int(rng.integers(12, 100)))
            people.append(dict(rel="D", dob=k_dob, gender="M" if rng.random() < 0.51 else "F", enroll=k_en))
        # the Fund numbers members in order of enrollment (the participant first)
        order = sorted(range(len(people)), key=lambda i: (people[i]["rel"] != "P", people[i]["enroll"], people[i]["rel"] != "S", people[i]["dob"]))
        for seq, i in enumerate(order, 1):
            people[i]["mid"] = "%s-%02d" % (sid, seq)
        # Corvane numbers the cardholder 01, the spouse 02 and dependents from 03 by date of birth
        deps = sorted([p for p in people if p["rel"] == "D"], key=lambda p: p["dob"])
        for p in people:
            if p["rel"] == "P":
                p["pc"] = "01"
            elif p["rel"] == "S":
                p["pc"] = "02"
        for j, p in enumerate(deps):
            p["pc"] = "%02d" % (3 + j)
        for p in people:
            p["sid"] = sid
            p["fam"] = f
            members.append(p)
            fam["members"].append(p)
        fams.append(fam)
    return fams, members


def age_on(p, d):
    return d.year - p["dob"].year - ((d.month, d.day) < (p["dob"].month, p["dob"].day))


def eligibility(rng, fams):
    """each family's covered months from the hour bank, with the late postings: months reinstated when an employer's
    late contributions post (RI), and months terminated after the fact (RT)"""
    k0, k1 = mkey(W.SERVICE_FROM), mkey(W.SERVICE_TO)
    for fam in fams:
        start = max(mkey(fam["enroll"]), k0)
        cov = {k: True for k in range(start, k1 + 1)}
        # a family that left the trade
        if rng.random() < 0.06:
            stop = int(rng.integers(start + 1, k1 + 2))
            for k in range(stop, k1 + 1):
                cov[k] = False
        # winter hour-bank gaps
        for yr in (2025, 2026):
            if rng.random() < 0.10:
                g0 = mkey(D(yr, int(rng.integers(1, 4)), 1))
                for k in range(g0, g0 + int(rng.integers(1, 3))):
                    if k in cov:
                        cov[k] = False
        fam["cov"] = cov
        # late postings: a gap month reinstated later, a covered month terminated later
        fam["ri"], fam["rt"] = {}, {}
        for k, c in cov.items():
            if not c and rng.random() < 0.18:
                fam["ri"][k] = mend(k) + dt.timedelta(days=int(rng.integers(20, 80)))
            elif c and rng.random() < 0.006:
                fam["rt"][k] = mend(k) + dt.timedelta(days=int(rng.integers(15, 100)))
        for k in fam["ri"]:
            cov[k] = True
        for k in fam["rt"]:
            cov[k] = False


def member_cover(p, fam):
    """the member's covered months (final), within the family's"""
    out = {}
    for k, c in fam["cov"].items():
        if not c:
            continue
        if k < mkey(p["enroll"]):
            continue
        if p["rel"] == "D" and mend(k) > D(p["dob"].year + 26, p["dob"].month, 1) + dt.timedelta(days=27):
            continue
        out[k] = True
    return out


def span_rows(rng, fams):
    """the eligibility export: one row per version of a coverage span (the latest version stands)"""
    rows = []
    for fam in fams:
        for p in fam["members"]:
            cov = member_cover(p, fam)
            # months known at the time (the original postings): RT months were covered, RI months were not
            orig = {k for k in cov} | {k for k in fam["rt"] if k >= mkey(p["enroll"])}
            orig -= set(fam["ri"])
            orig = {k for k in orig if not (p["rel"] == "D" and mend(k) > D(p["dob"].year + 26, p["dob"].month, 28))}
            spans, run = [], []
            for k in sorted(orig):
                if run and k == run[-1] + 1:
                    run.append(k)
                else:
                    if run:
                        spans.append(run)
                    run = [k]
            if run:
                spans.append(run)
            for j, sp in enumerate(spans, 1):
                sid = "%s-E%02d" % (p["mid"], j)
                start, end = mstart(sp[0]), mend(sp[-1])
                posted = start - dt.timedelta(days=int(rng.integers(5, 25)))
                reason = "NE" if (p["enroll"] >= W.SERVICE_FROM and mstart(sp[0]) == mstart(mkey(p["enroll"]))) else "HB"
                end_out = "" if sp[-1] == mkey(W.SERVICE_TO) else end.isoformat()
                rows.append([p["mid"], p["sid"], p["rel"], p["dob"].isoformat(), p["gender"], sid, 1,
                             start.isoformat(), end_out, posted.isoformat(), reason])
                # a retroactive termination inside the span shortens it (version 2) and may reopen it (a new span)
                rts = sorted(k for k in fam["rt"] if k in sp)
                if rts:
                    k = rts[0]
                    v2_end = mend(k - 1) if k > sp[0] else None
                    if v2_end is None:
                        rows.append([p["mid"], p["sid"], p["rel"], p["dob"].isoformat(), p["gender"], sid, 2,
                                     start.isoformat(), (start - DAY).isoformat(), fam["rt"][k].isoformat(), "RT"])
                    else:
                        rows.append([p["mid"], p["sid"], p["rel"], p["dob"].isoformat(), p["gender"], sid, 2,
                                     start.isoformat(), v2_end.isoformat(), fam["rt"][k].isoformat(), "RT"])
                    if k < sp[-1]:
                        rows.append([p["mid"], p["sid"], p["rel"], p["dob"].isoformat(), p["gender"], sid + "R", 1,
                                     mstart(k + 1).isoformat(), end_out, fam["rt"][k].isoformat(), "HB"])
            for k, posted in sorted(fam["ri"].items()):
                if k < mkey(p["enroll"]) or k not in cov:
                    continue
                rows.append([p["mid"], p["sid"], p["rel"], p["dob"].isoformat(), p["gender"], "%s-RI%d" % (p["mid"], k),
                             1, mstart(k).isoformat(), mend(k).isoformat(), posted.isoformat(), "RI"])
    return rows


# ------------------------------------------------------------------------------------------- clinicians, attribution
def clinicians(rng):
    used = set()
    out = {"pcp": {}, "spec": {}, "outside": [], "facilities": []}
    for code, name, kind, npcp, nspec, style, *_ in W.PARTNERS:
        out["pcp"][code] = [npi(rng, used) for _ in range(npcp)]
        out["spec"][code] = [npi(rng, used) for _ in range(nspec)]
    out["outside"] = [npi(rng, used) for _ in range(420)]
    out["facilities"] = [npi(rng, used) for _ in range(38)]
    # each partner group bills its clinicians' professional claims under its own group NPI; outside clinicians bill
    # under their practice's NPI, or their own
    out["group"] = {code: npi(rng, used) for code in W.CODES}
    ogroups = [npi(rng, used) for _ in range(64)]
    out["outside_bill"] = {n: (ogroups[int(rng.integers(0, len(ogroups)))] if rng.random() < 0.72 else n) for n in out["outside"]}
    # the moves of 2026: every partner loses one specialist to a practice outside the network during the year, and
    # about half take on a new specialist from outside, who starts with a smaller practice
    moves = []
    codes = W.CODES
    for code in codes:
        pool = out["spec"][code]
        who = pool[int(rng.integers(0, len(pool)))]
        when = mstart(int(rng.integers(mkey(D(2026, 6, 1)), mkey(D(2026, 11, 1)))))
        moves.append(dict(npi=who, to=None, frm=code, date=when))
        if rng.random() < 0.5:
            new = npi(rng, used)
            out["spec"][code].append(new)
            when = mstart(int(rng.integers(mkey(D(2026, 3, 1)), mkey(D(2026, 7, 1)))))
            moves.append(dict(npi=new, to=code, frm=None, date=when))
    out["moves"] = moves
    return out


def partner_of(npi_, d, C):
    """the partner a clinician belonged to on date d"""
    if "_home" not in C:
        C["_home"] = {n: code for code in W.CODES for n in C["pcp"][code] + C["spec"][code]}
        C["_move"] = {m["npi"]: m for m in C["moves"]}
    m = C["_move"].get(npi_)
    if m is None:
        return C["_home"].get(npi_)
    if m["to"] is not None:          # joined m["to"] on m["date"]; before then with m["frm"]
        return m["to"] if d >= m["date"] else m["frm"]
    return None if d >= m["date"] else m["frm"]


def assign_pcp(rng, members, C):
    adult_w = np.array([0.0 if W.KIND[c] == "pediatric" else (0.8 if W.KIND[c] == "family" else 1.0) for c in W.CODES])
    adult_w /= adult_w.sum()
    for p in members:
        child = p["rel"] == "D" and age_on(p, D(2026, 1, 1)) < 18
        if child:
            r = rng.random()
            code = "SPP" if r < 0.42 else ("CFP" if r < 0.52 else ("KRH" if r < 0.60 else ("BCN" if r < 0.68 else None)))
        else:
            code = W.CODES[int(rng.choice(len(W.CODES), p=adult_w))] if rng.random() < 0.88 else None
        p["pcp_code"] = code
        p["pcp"] = C["pcp"][code][int(rng.integers(0, len(C["pcp"][code])))] if code else None
    # spouses mostly share the participant's practice
    byfam = {}
    for p in members:
        byfam.setdefault(p["fam"], []).append(p)
    for f, ps in byfam.items():
        part = [p for p in ps if p["rel"] == "P"][0]
        for p in ps:
            if p["rel"] == "S" and part["pcp_code"] and rng.random() < 0.6:
                p["pcp_code"], p["pcp"] = part["pcp_code"], C["pcp"][part["pcp_code"]][int(rng.integers(0, len(C["pcp"][part["pcp_code"]])))]


def roster(rng, fams, C):
    """the monthly attribution roster for 2026, run on the first of each month from the eligibility then posted:
    members whose month was later terminated are on it, members whose month was reinstated later are not"""
    rows = []
    switch = {}
    for fam in fams:
        for p in fam["members"]:
            code, doc = p["pcp_code"], p["pcp"]
            for k in range(mkey(D(2026, 1, 1)), mkey(D(2026, 12, 1)) + 1):
                if rng.random() < 0.010:      # a change of primary care provider of record
                    if code is None or rng.random() < 0.7:
                        child = p["rel"] == "D" and age_on(p, mstart(k)) < 18
                        opts = ["SPP", "CFP", "KRH", "BCN"] if child else [c for c in W.CODES if W.KIND[c] != "pediatric"]
                        code = opts[int(rng.integers(0, len(opts)))]
                        doc = C["pcp"][code][int(rng.integers(0, len(C["pcp"][code])))]
                    else:
                        code, doc = None, None
                p.setdefault("att", {})[k] = code
                known = (k in member_cover(p, fam) and k not in fam["ri"]) or (k in fam["rt"] and k >= mkey(p["enroll"]))
                if code and known:
                    rows.append([mstart(k).isoformat(), p["mid"], doc, code])
    return rows


# -------------------------------------------------------------------------------------------------- medical claims
def paid_on(rng, recv, pend):
    """the administrator's payment date for a claim received on recv"""
    if recv < W.GOLIVE:
        ready = recv + dt.timedelta(days=int(rng.gamma(*W.OLD_REVIEW)) + (int(rng.uniform(*W.OLD_PEND_DAYS)) if pend else 0))
        if ready < W.GOLIVE:
            p = thursday_run(ready)
            if p < W.GOLIVE:
                return p, "L"
            return bday_on_or_after(W.GOLIVE + dt.timedelta(days=int(rng.integers(0, 10)))), "T"
        if not pend:          # pending at go-live: adjudicated on Tallis in the first two weeks
            return bday_on_or_after(W.GOLIVE + dt.timedelta(days=int(rng.integers(0, (W.BACKLOG_END - W.GOLIVE).days + 1)))), "T"
        return bday_on_or_after(ready), "T"
    if pend:
        return bday_on_or_after(recv + dt.timedelta(days=int(rng.uniform(*W.NEW_PEND_DAYS)))), "T"
    return next_bday(recv), "T"


def claims(rng, fams, C):
    rows = []
    seqno = [0]
    risk = {}
    for fam in fams:
        for p in fam["members"]:
            a = age_on(p, D(2026, 1, 1))
            base = 0.55 if a < 5 else (0.35 if a < 18 else (0.7 if a < 35 else (1.0 if a < 50 else 1.6)))
            r = base * rng.lognormal(-0.32, 0.8)
            if rng.random() < 0.04:
                r *= rng.uniform(3, 6)
            risk[p["mid"]] = r
    cat = set()
    allp = [p for fam in fams for p in fam["members"] if p.get("pcp_code")]
    for i in rng.choice(len(allp), 7, replace=False):
        cat.add(allp[i]["mid"])

    def add(p, k, t, amt, rendering, billing, sfrom, sto, admit=None):
        seqno[0] += 1
        lam_shape, smean, late, lmean = W.CLAIM_TYPES[t][3], W.CLAIM_TYPES[t][4], W.CLAIM_TYPES[t][5], W.CLAIM_TYPES[t][6]
        lag = rng.gamma(lam_shape, smean / lam_shape) if rng.random() > late else rng.exponential(lmean) + 20
        recv = bday_on_or_after(sto + dt.timedelta(days=int(lag) + 1))
        if recv > W.CUT + dt.timedelta(days=400):
            return
        pend = rng.random() < (W.OLD_PEND if recv < W.GOLIVE else W.NEW_PEND)
        ri = p["fam_ri"].get(k)
        if ri and recv < ri:      # waits for the late contributions to post
            recv_eff, pend = ri, False
        else:
            recv_eff = recv
        paid, system = paid_on(rng, recv_eff, pend)
        deny = rng.random() < W.DENY_SHARE
        rt = p["fam_rt"].get(k)
        if rt is not None and recv >= rt:     # received after the termination posted: denied
            deny = True
        allowed = amt / (0.86 if t == "P" else 0.91)
        billed = allowed * rng.uniform(1.6, 2.9)
        rows.append(dict(seq=seqno[0], mid=p["mid"], k=k, t=t, sfrom=sfrom, sto=sto, admit=admit, recv=recv, paid=paid,
                         sys=system, amt=0.0 if deny else amt, allowed=0.0 if deny else allowed, billed=billed,
                         deny=deny, rendering=rendering, billing=billing, rt=None if deny else rt))

    for fam in fams:
        for p in fam["members"]:
            p["fam_ri"], p["fam_rt"] = fam["ri"], fam["rt"]
            cov = member_cover(p, fam)
            for k in sorted(cov):
                if mstart(k) > W.SERVICE_TO:
                    continue
                code = p.get("att", {}).get(k, p.get("pcp_code"))
                style = W.STYLE.get(code, 1.0) if code else 1.0
                r = risk[p["mid"]] * style
                nd = (mend(k) - mstart(k)).days + 1
                for t, (lam, mean, sig, *_rest) in W.CLAIM_TYPES.items():
                    n = rng.poisson(lam * r)
                    mu = np.log(mean) - sig ** 2 / 2
                    for _ in range(int(n)):
                        sfrom = mstart(k) + dt.timedelta(days=int(rng.integers(0, nd)))
                        amt = float(rng.lognormal(mu, sig))
                        if t == "I":
                            los = int(max(1, rng.gamma(1.6, 2.6)))
                            sto = sfrom + dt.timedelta(days=los)
                            add(p, k, t, amt, None, C["facilities"][int(rng.integers(0, len(C["facilities"])))], sfrom, sto, admit=sfrom)
                        elif t == "O":
                            add(p, k, t, amt, None, C["facilities"][int(rng.integers(0, len(C["facilities"])))], sfrom, sfrom)
                        else:
                            # the rendering clinician: the member's own practice, its specialists, or outside
                            u = rng.random()
                            leak = 0.24 + 0.18 * (W.STYLE.get(code, 1.0) - 0.88) / 0.24 if code else 1.0
                            if code and u < (1 - leak) * 0.6 and p.get("pcp"):
                                rend = p["pcp"]
                            elif code and u < (1 - leak):
                                pool = C["spec"][code] + C["pcp"][code]
                                rend = pool[int(rng.integers(0, len(pool)))]
                            else:
                                rend = C["outside"][int(rng.integers(0, len(C["outside"])))]
                            at = partner_of(rend, sfrom, C)
                            bill = C["group"][at] if at else C["outside_bill"].get(rend, rend)
                            add(p, k, t, amt, rend, bill, sfrom, sfrom)
                # the catastrophic stays of 2026, paid well before the cut
                if p["mid"] in cat and mstart(k).year == 2026 and 2 <= mstart(k).month <= 7 and rng.random() < 0.55:
                    sfrom = mstart(k) + dt.timedelta(days=int(rng.integers(0, 20)))
                    add(p, k, "I", float(rng.uniform(95000, 260000)), None, C["facilities"][int(rng.integers(0, 6))],
                        sfrom, sfrom + dt.timedelta(days=int(rng.integers(8, 40))), admit=sfrom)
    return rows


def versions(rng, crow):
    """every version of every claim as the extract carries it: the original, then a replacement or a void for some,
    each paid on the run of its own processing date by whichever system was adjudicating then"""
    out = []
    for c in crow:
        out.append(dict(c, ver=1, kind="orig", vpaid=c["paid"], vamt=c["amt"], vallowed=c["allowed"], vsys=c["sys"]))
        if c["deny"]:
            continue
        u = rng.random()
        if c.get("rt") is not None:
            # paid while the month was covered, voided once the termination posted
            vd = max(c["paid"], c["rt"]) + dt.timedelta(days=int(rng.integers(3, 25)))
            sysv = "T" if vd >= W.GOLIVE else "L"
            vd = thursday_run(vd) if sysv == "L" else bday_on_or_after(vd)
            out.append(dict(c, ver=2, kind="void", vpaid=vd, vamt=0.0, vallowed=0.0, vsys=sysv))
        elif u < W.REPLACE_SHARE:
            vd = c["paid"] + dt.timedelta(days=int(rng.integers(25, 110)))
            sysv = "T" if vd >= W.GOLIVE else "L"
            vd = thursday_run(vd) if sysv == "L" else bday_on_or_after(vd)
            f = float(np.clip(rng.normal(1.0, 0.18), 0.55, 1.6))
            out.append(dict(c, ver=2, kind="repl", vpaid=vd, vamt=c["amt"] * f, vallowed=c["allowed"] * f, vsys=sysv))
        elif u < W.REPLACE_SHARE + W.VOID_SHARE:
            vd = c["paid"] + dt.timedelta(days=int(rng.integers(20, 90)))
            sysv = "T" if vd >= W.GOLIVE else "L"
            vd = thursday_run(vd) if sysv == "L" else bday_on_or_after(vd)
            out.append(dict(c, ver=2, kind="void", vpaid=vd, vamt=0.0, vallowed=0.0, vsys=sysv))
    return out


# ------------------------------------------------------------------------------------------------------ pharmacy
def ndc_for(cost, u):
    """the package dispensed: products sit at their price level (a package code per 4 per cent of cost per fill), a
    few products per level, so the common generics repeat across the file as they do in a pharmacy benefit manager's
    claims"""
    level = int(round(np.log(max(cost, 1.0)) / np.log(1.04)))
    k = 1 + level % 5
    j = u % k
    return "%05d-%04d-%02d" % (10000 + (level * 7919 + j * 104729) % 89989, 1000 + (level * 313 + j * 17) % 8999,
                               1 + (level + 3 * j) % 97)


def pharmacy(rng, fams):
    rows = []
    rxn = [7000000]
    for fam in fams:
        for p in fam["members"]:
            cov = set(member_cover(p, fam)) - set(fam["ri"]) | {k for k in fam["rt"] if k >= mkey(p["enroll"])}
            for k in sorted(cov):
                if mstart(k).year != 2026:
                    continue
                a = age_on(p, mstart(k))
                rate = W.RX_RATE["child"] if a < 18 else (W.RX_RATE["adult"] if a < 55 else W.RX_RATE["older"])
                nd = (mend(k) - mstart(k)).days + 1
                for _ in range(int(rng.poisson(rate))):
                    rxn[0] += int(rng.integers(1, 40))
                    fill = mstart(k) + dt.timedelta(days=int(rng.integers(0, nd)))
                    if rng.random() < W.SPECIALTY_SHARE:
                        cost = float(rng.uniform(*W.SPECIALTY_RANGE))
                    else:
                        cost = float(rng.lognormal(np.log(W.RX_MEAN) - W.RX_SIGMA ** 2 / 2, W.RX_SIGMA))
                    copay = float(min(cost * 0.25, rng.choice([5.0, 10.0, 15.0, 25.0, 40.0])))
                    fee = round(float(rng.choice([0.85, 1.10, 1.50, 1.75])), 2)
                    ing = round(cost - fee, 2) if cost > fee + 1 else round(cost, 2)
                    plan = round(ing + fee - copay, 2)
                    ds = int(rng.choice([30, 30, 30, 90, 14, 7]))
                    qty = float(ds * rng.choice([1, 1, 2, 0.5]))
                    pick = (int(rng.integers(10000, 99999)), int(rng.integers(1000, 9999)), int(rng.integers(1, 99)))
                    row = dict(p=p, rx="%07d" % rxn[0], fill=fill, ing=ing, fee=fee, copay=round(copay, 2), plan=plan,
                               ds=ds, qty=qty, ndc=ndc_for(cost, pick[0]))
                    rows.append(dict(row, tc="B1", adj=fill))
                    if rng.random() < W.RX_REVERSAL:
                        rd = fill + dt.timedelta(days=int(rng.integers(0, 12)))
                        rows.append(dict(row, tc="B2", adj=rd))
                        if rng.random() < 0.55:
                            f2 = float(np.clip(rng.normal(1.0, 0.15), 0.6, 1.4))
                            r3 = dict(row, tc="B3", adj=rd + dt.timedelta(days=int(rng.integers(0, 3))))
                            r3["ing"] = round(row["ing"] * f2, 2)
                            r3["plan"] = round(r3["ing"] + row["fee"] - row["copay"], 2)
                            rows.append(r3)
    return rows


def simulate(seed=W.SEED):
    rng = np.random.default_rng(seed)
    fams, members = families(rng)
    eligibility(rng, fams)
    C = clinicians(rng)
    assign_pcp(rng, members, C)
    rost = roster(rng, fams, C)
    elig = span_rows(rng, fams)
    crow = claims(rng, fams, C)
    vers = versions(rng, crow)
    rx = pharmacy(rng, fams)
    return dict(fams=fams, members=members, C=C, roster=rost, elig=elig, claims=crow, versions=vers, rx=rx, rng=rng)
