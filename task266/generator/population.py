"""Every admission the extracts hold, around the review's three entering classes: the earlier students still on the
books, the spring and summer entrants, the fall 2026 and spring 2027 entrants, certificate, dual-enrolment and
non-degree students, readmissions and second programs; then the student numbers in both systems, the program-of-record
history and the associate degrees conferred. Each part draws on its own random stream."""
import datetime as dt

import numpy as np

import common as K
import world as W

CERT_RATES = dict(gr=(0, .30, .22, .25, .2), wd=.20, to=.02)


def rng_for(seed, *keys):
    return np.random.default_rng([seed, 7] + [int(k) for k in keys])


def fs_after(code, k):
    """The k-th fall or spring term after code."""
    later = [c for c in K.CODES_IN_ORDER if c > code and W.is_fs(c)]
    return later[k - 1] if len(later) >= k else None


def add_adm(T, sid, admit, kind, prog, campus, reason, exit_, pt, switches=(), cls=None, rec=None, cert=False):
    a = dict(sid=sid, admit=admit, type=kind, prog=prog, campus=campus, reason=reason, exit=exit_, pt=pt,
             switches=list(switches), cls=cls, rec=rec, cert=cert)
    T["adm"].append(a)
    return a


def new_ids(T, rng, n, legacy):
    out = []
    for _ in range(n):
        while True:
            sid = "A0%07d" % int(rng.integers(1200000, 9900000))
            if sid not in T["used"]:
                break
        T["used"].add(sid)
        lid = None
        if legacy:
            while True:
                lid = "%07d" % int(rng.integers(2100000, 3999999))
                if lid not in T["used_legacy"]:
                    break
            T["used_legacy"].add(lid)
        out.append((sid, lid))
    return out


def follow_cert(rng, admit):
    """A certificate admission: the certificate, a withdrawal or a transfer at the fall and spring censuses."""
    t, code = 1, admit
    while True:
        if t >= 2 and W.is_fs(code):
            u = rng.random()
            if u < CERT_RATES["wd"]:
                return "WD", code
            if u < CERT_RATES["wd"] + CERT_RATES["to"]:
                return "TO", code
        if t <= len(CERT_RATES["gr"]) and rng.random() < CERT_RATES["gr"][t - 1]:
            return "GR", code
        if code >= K.LAST:
            return None, None
        code, t = K.nth(code, 1), t + 1


def build(seed=W.SEED):
    T = dict(adm=[], used=set(), used_legacy=set(), legacy_of={}, person={})
    recs = W.entering(seed)
    T["entering"] = recs
    # ---------------------------------------------------------------- the review's three entering classes
    for i, r in enumerate(recs):
        rng = rng_for(seed, 1, i)
        (sid, lid), = new_ids(T, rng, 1, legacy=r["cls"] == 2023)
        r["sid"], r["lid"] = sid, lid
        if lid:
            T["legacy_of"][sid] = lid
        kind = "T" if r["tr_in"] else "N"
        a = add_adm(T, sid, K.fall(r["cls"]), kind, r["prog"], r["campus"], r["reason"], r["exit"], r["pt"],
                    r["switches"], cls=r["cls"], rec=i)
        r["adm"] = a
        ra = r["readmit"]
        if ra:
            add_adm(T, sid, ra["term"], "R", ra["prog"], r["campus"], ra["reason"], ra["exit"], r["pt"], ra["switches"])
    # ---------------------------------------------------------------- earlier students (admitted fall 2020 to summer 2023)
    early = [c for c in K.CODES_IN_ORDER if "202110" <= c <= "202330"]
    for j, adm in enumerate(early):
        season = K.TERM[adm]["season"]
        share = {"FA": 1.0, "SP": .21, "SU": .06}[season]
        for prog in K.CODES:
            rng = rng_for(seed, 2, j, K.CODES.index(prog))
            n = int(round(W.P[prog]["n"] * share * rng.uniform(.9, 1.08)))
            for sid, lid in new_ids(T, rng, n, legacy=True):
                T["legacy_of"][sid] = lid
                pt = rng.random() < W.P[prog]["pt"] + .06
                tr_in = rng.random() < W.P[prog]["tr"]
                campus = ["QNL", "TRV", "HOL"][int(rng.choice(3, p=W.P[prog]["camp"]))]
                reason, code, sw = W.follow(rng, prog, None, pt, tr_in, 1, adm, K.LAST)
                a = add_adm(T, sid, adm, "T" if tr_in else "N", prog, campus, reason, code, pt, sw)
                if reason == "WD" and code >= "202310" and rng.random() < W.P_READMIT:
                    back = fs_after(code, int(rng.integers(1, 4)))
                    if back and "202410" <= back <= K.LAST:
                        rp = prog if rng.random() < .65 else "GS"
                        t0 = K.index_of(adm, code)
                        rr, rc, rs = W.follow(rng, rp, None, pt, tr_in, max(t0, 2), back, K.LAST, readmitted=True)
                        add_adm(T, sid, back, "R", rp, campus, rr, rc, pt, rs)
    # ---------------------------------------------------------------- spring and summer entrants, fall 2026 and spring 2027 entrants
    later = [c for c in K.CODES_IN_ORDER if "202420" <= c <= K.LAST and c not in (K.fall(2024), K.fall(2025))]
    for j, adm in enumerate(later):
        season = K.TERM[adm]["season"]
        share = {"FA": 1.075, "SP": .21, "SU": .06}[season]
        for prog in K.CODES:
            rng = rng_for(seed, 3, j, K.CODES.index(prog))
            n = int(round(W.P[prog]["n"] * share * rng.uniform(.92, 1.08)))
            for sid, lid in new_ids(T, rng, n, legacy=adm <= "202430"):
                if lid:
                    T["legacy_of"][sid] = lid
                pt = rng.random() < W.P[prog]["pt"] + (.08 if season != "FA" else 0)
                tr_in = rng.random() < W.P[prog]["tr"] + (.06 if season != "FA" else 0)
                campus = ["QNL", "TRV", "HOL"][int(rng.choice(3, p=W.P[prog]["camp"]))]
                reason, code, sw = W.follow(rng, prog, None, pt, tr_in, 1, adm, K.LAST)
                add_adm(T, sid, adm, "T" if tr_in else "N", prog, campus, reason, code, pt, sw)
    # ---------------------------------------------------------------- certificates, dual enrolment, non-degree study
    terms = [c for c in K.CODES_IN_ORDER if "202410" <= c <= K.LAST]
    for j, adm in enumerate(terms):
        season = K.TERM[adm]["season"]
        rng = rng_for(seed, 4, j)
        for k, cert in enumerate(K.CERTS):
            n = int(round({"FA": 26, "SP": 11, "SU": 4}[season] * (1.6 if cert == "CERT.WELD" else 1)
                          * rng.uniform(.75, 1.25)))
            for sid, lid in new_ids(T, rng, n, legacy=adm <= "202430"):
                if lid:
                    T["legacy_of"][sid] = lid
                reason, code = follow_cert(rng, adm)
                campus = ["QNL", "TRV", "HOL"][int(rng.choice(3, p=(.4, .4, .2)))]
                add_adm(T, sid, adm, "N", cert, campus, reason, code, rng.random() < .6, cert=True)
        if season != "SU":
            n = int(round((540 + 22 * j) * (1 if season == "FA" else .13) * rng.uniform(.95, 1.05)))
            for sid, lid in new_ids(T, rng, n, legacy=adm <= "202430"):
                if lid:
                    T["legacy_of"][sid] = lid
                nxt = fs_after(adm, 1 if season == "SP" else 2)
                nxt = [c for c in K.CODES_IN_ORDER if c > adm and K.TERM[c]["season"] == "FA"]
                close = nxt[0] if nxt and nxt[0] <= K.LAST else None
                reason = (("TO" if rng.random() < .42 else "WD") if close else None)
                campus = ["QNL", "TRV", "HOL"][int(rng.choice(3, p=(.45, .3, .25)))]
                add_adm(T, sid, adm, "D", "DE.HSDE", campus, reason, close, True)
        n = int(round({"FA": 74, "SP": 52, "SU": 61}[season] * rng.uniform(.85, 1.15)))
        for sid, lid in new_ids(T, rng, n, legacy=adm <= "202430"):
            if lid:
                T["legacy_of"][sid] = lid
            close = fs_after(adm, 1)
            close = close if close and close <= K.LAST else None
            reason = ("TO" if rng.random() < .3 else "WD") if close else None
            add_adm(T, sid, adm, "V", "ND.NDEG", "QNL", reason, close, True)
    # ---------------------------------------------------------------- second programs after a degree
    for i, a in enumerate(list(T["adm"])):
        if a["reason"] == "GR" and not a["cert"] and a["prog"] in K.CODES:
            rng = rng_for(seed, 5, i)
            nxt = fs_after(a["exit"], 1)
            if nxt and nxt <= K.LAST and rng.random() < .055:
                cur = a["switches"][-1][1] if a["switches"] else a["prog"]
                new = {"BIO": "NUR", "MA": "NUR", "GS": "BUS", "PSY": "ECE", "BUS": "GS", "CJ": "PSY", "ECE": "PSY",
                       "HVR": "BUS", "NUR": "BIO"}[cur]
                rr, rc, rs = W.follow(rng, new, None, a["pt"], True, 4, nxt, K.LAST, readmitted=True)
                add_adm(T, a["sid"], nxt, "S", new, a["campus"], rr, rc, a["pt"], rs)
    T["adm"].sort(key=lambda a: (a["admit"], a["sid"]))
    # ---------------------------------------------------------------- filler: students who left before 2021 (conversion map only)
    rng = rng_for(seed, 6)
    T["converted_only"] = new_ids(T, rng, 7300, legacy=True)
    return T


def program_at(a, code):
    """The program of record of admission a in term code."""
    cur = a["prog"]
    for c, p in a["switches"]:
        if c <= code:
            cur = p
    return cur


def ends_open(a):
    return a["reason"] is None


def enrolled_fall26(a):
    """An admission whose student is enrolled at the fall 2026 census."""
    if a["admit"] > K.FALL26:
        return False
    if a["reason"] is None:
        return True
    if a["exit"] > K.FALL26:
        return True
    return a["exit"] == K.FALL26 and a["reason"] == "GR"


def stamp(T, seed=W.SEED):
    """Dates on the admission records: when an ending was recorded, and when a withdrawal was recoded as a transfer
    out once the exchange's match came back."""
    for i, a in enumerate(T["adm"]):
        rng = rng_for(seed, 8, i)
        a["recorded"] = a["changed"] = None
        if a["reason"] is None:
            continue
        t = K.TERM[a["exit"]]
        if a["reason"] == "GR":
            a["recorded"] = t["confer"] + dt.timedelta(days=int(rng.integers(1, 9)))
        elif a["reason"] in ("WD", "TO"):
            a["recorded"] = t["census"] + dt.timedelta(days=int(rng.integers(1, 5)))
            if a["reason"] == "TO":
                # the exchange's match runs each quarter; the recode follows the next run after the census
                runs = [dt.date(y, m, 1) + dt.timedelta(days=int(d)) for y in range(2023, 2028) for m, d in
                        ((1, 20), (4, 18), (7, 17), (10, 16))]
                nxt = [r for r in runs if r > a["recorded"] + dt.timedelta(days=12)][0]
                a["changed"] = min(nxt + dt.timedelta(days=int(rng.integers(2, 12))), K.EXTRACT - dt.timedelta(days=3))
        else:
            a["recorded"] = t["start"] + dt.timedelta(days=int(rng.integers(5, 90)))
    return T
