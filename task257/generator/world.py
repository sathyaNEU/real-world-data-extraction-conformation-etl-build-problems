"""The world of task257: Brackenmere's sites and people, their HR history, the survey's distribution list, how each
employee answered (web link, store kiosk or printed form), the answers themselves and the records each channel
leaves. Everything here is the clean truth the pack is written from; records.py writes the files."""
from __future__ import annotations

import datetime as dt

import numpy as np
from scipy.special import ndtri

import common as K

FMT_SIZE = {"U": (158, 238), "S": (108, 184), "T": (50, 98), "X": (34, 64)}
STORE_DEPTS = [("GRO", 110, "Grocery", 0.27), ("PRD", 120, "Produce", 0.11), ("MTS", 130, "Meat and Seafood", 0.09),
               ("DEL", 140, "Deli", 0.08), ("BAK", 150, "Bakery", 0.07), ("FRT", 160, "Front End", 0.27),
               ("RCV", 170, "Receiving", 0.05), ("MGT", 190, "Store Management", 0.06)]
DC_DEPTS = [("RCV", 510, "Inbound", 0.24), ("PCK", 520, "Order Picking", 0.38), ("SHP", 530, "Outbound", 0.18),
            ("TRN", 540, "Transport", 0.12), ("OFF", 590, "Site Office", 0.08)]
HO_DEPTS = [("FIN", 810, "Finance", 0.16), ("MER", 820, "Merchandising", 0.19), ("PPL", 830, "People", 0.12),
            ("TEC", 840, "Technology", 0.17), ("MKT", 850, "Marketing", 0.10), ("SCM", 860, "Supply Chain", 0.12),
            ("OPS", 870, "Store Operations", 0.14)]

# Latent model: loadings by topic, factor correlations, five-point category shares before item-level variation
LOAD = {"W": (0.60, 0.80), "M": (0.60, 0.80), "T": (0.85, 0.92), "G": (0.85, 0.92), "B": (0.46, 0.56),
        "R": (0.46, 0.56)}
PHI = np.array([[1.0, 0.20, 0.30], [0.20, 1.0, 0.45], [0.30, 0.45, 1.0]])
YES = {"W": (0.45, 0.60), "T": (0.93, 0.955), "M": (0.40, 0.55), "G": (0.045, 0.07), "B": (0.50, 0.65),
       "R": (0.35, 0.50)}
A5_SHARE = np.array([0.05, 0.12, 0.20, 0.40, 0.23])
DNA_RATE = {"T3": 0.034, "G6": 0.022, "M5": 0.013, "G5": 0.011}

PROPENSITY = {"email": 0.70, "sms": 0.52, "kiosk": 0.71, "printed form": 0.76}
WEB_DAY_W = [18, 10, 6, 4, 3, 2, 2, 12, 6, 4, 3, 10, 7, 13]
KIOSK_DAY_W = [11, 9, 8, 7, 6, 5, 5, 9, 8, 7, 6, 8, 6, 5]


def _rng(k):
    return np.random.default_rng(K.SEED + 1000 * k)


def _day(i):
    return K.OPEN_DAY + dt.timedelta(days=int(i))


# ------------------------------------------------------------------ sites

def build_sites():
    r = _rng(1)
    legacy = r.choice(np.arange(101, 699), size=148, replace=False)
    sites = []
    n = 0
    for d, (dcode, dname, stores) in enumerate(K.DISTRICTS):
        for i, (name, city, prov, fmt) in enumerate(stores):
            lo, hi = FMT_SIZE[fmt]
            size = int(r.integers(lo, hi))
            tz = "America/Winnipeg" if name in K.CENTRAL_TIME else ("America/Moncton" if prov == "NB" else
                                                                     "America/Toronto")
            opened = dt.date(int(r.integers(1976, 2022)), int(r.integers(1, 13)), int(r.integers(1, 29)))
            sites.append(dict(site_no=1000 + 100 * (d + 1) + i + 1, legacy_no=int(legacy[n]),
                              name="Brackenmere %s" % name, city=city, province=prov, type="store",
                              format={"U": "urban", "S": "suburban", "T": "town", "X": "express"}[fmt],
                              tz=tz, district=dcode, district_name=dname, size=size, kiosk=fmt in ("U", "S"),
                              opened=opened))
            n += 1
    sizes = {9001: 612, 9002: 527, 9003: 384, 9100: 743}
    for (no, leg, name, city, prov, typ, tz) in K.OTHER_SITES:
        sites.append(dict(site_no=no, legacy_no=leg, name=name, city=city, province=prov, type=typ,
                          format="", tz=tz, district="", district_name="", size=sizes[no],
                          kiosk=typ == "distribution centre", opened=dt.date(1994 if no == 9100 else 2003 + no % 9001 * 4,
                                                                              4, 1)))
    return sites


def _french_share(s):
    if s["province"] == "QC":
        return 0.87
    if s["province"] == "NB":
        return 0.34
    if s["city"] in ("Hawkesbury",):
        return 0.66
    if s["city"] in ("Clarence-Rockland",):
        return 0.48
    if s["city"] in ("Cornwall", "Kapuskasing", "Timmins"):
        return 0.24
    if s["city"] in ("Ottawa", "Greater Sudbury", "North Bay"):
        return 0.11
    return 0.025


# ------------------------------------------------------------------ people and HR history

def build_people(sites):
    r = _rng(2)
    total = sum(s["size"] for s in sites)
    ids = r.choice(np.arange(10000, 999999), size=total + 900, replace=False)
    people = []
    k = 0
    for s in sites:
        depts = STORE_DEPTS if s["type"] == "store" else (DC_DEPTS if s["type"] == "distribution centre" else HO_DEPTS)
        w = np.array([d[3] for d in depts])
        fr = _french_share(s)
        for _ in range(s["size"]):
            d = depts[int(r.choice(len(depts), p=w / w.sum()))]
            yrs = min(r.exponential(5.5), 27.5)
            hire = dt.date(2026, 6, 30) - dt.timedelta(days=int(yrs * 365.25))
            if s["type"] == "head office" or d[0] in ("MGT", "OFF"):
                contact = "email"
            else:
                contact = "sms" if r.random() < (0.42 if s["type"] == "store" else 0.36) else ""
            people.append(dict(emp=int(ids[k]), site=s["site_no"], dept=d, hire=hire,
                               lang="FR" if r.random() < fr else "EN", contact=contact,
                               night=(d[0] in ("GRO", "RCV") and r.random() < 0.22), history=[]))
            k += 1
    # new hires in September (1 to 12 September), stores only
    stores = [s for s in sites if s["type"] == "store"]
    for _ in range(140):
        s = stores[int(r.integers(len(stores)))]
        w = np.array([x[3] for x in STORE_DEPTS])
        d = STORE_DEPTS[int(r.choice(len(STORE_DEPTS), p=w / w.sum()))]
        hire = dt.date(2026, 9, int(r.integers(1, 13)))
        people.append(dict(emp=int(ids[k]), site=s["site_no"], dept=d, hire=hire,
                           lang="FR" if r.random() < _french_share(s) else "EN",
                           contact="sms" if r.random() < 0.3 else "", night=False, history=[], new_hire=True))
        k += 1
    return people


def build_history(sites, people):
    """Effective-dated assignment rows for 2026: the pre-July row under the legacy site number and department code,
    the reorganisation row of 6 July, transfers, leavers. Returns the people with 'history' filled and with the site
    each held on key dates."""
    r = _rng(3)
    by_no = {s["site_no"]: s for s in sites}
    stores = [s for s in sites if s["type"] == "store"]
    by_tz = {}
    for s in stores:
        by_tz.setdefault(s["tz"], []).append(s)
    year0 = dt.date(2026, 1, 1)
    for p in people:
        s = by_no[p["site"]]
        old_dept = "%s-%s" % (p["dept"][0], {"store": "S", "distribution centre": "D", "head office": "H"}[s["type"]])
        if p["hire"] < K.REORG_DAY:
            p["history"].append(dict(site=s["legacy_no"], dept=old_dept, dept_name=p["dept"][2],
                                     start=p["hire"],
                                     end=K.REORG_DAY - dt.timedelta(days=1),
                                     action="hire" if p["hire"] >= year0 else "assignment"))
            p["history"].append(dict(site=s["site_no"], dept=str(p["dept"][1]), dept_name=p["dept"][2],
                                     start=K.REORG_DAY, end=None, action="reorganisation"))
        else:
            p["history"].append(dict(site=s["site_no"], dept=str(p["dept"][1]), dept_name=p["dept"][2],
                                     start=p["hire"], end=None, action="hire"))
        p["leave"] = None
    # transfers between stores in the same time zone: windows (7 Jul-31 Aug), (1-13 Sep), (15-25 Sep)
    movers = [p for p in people if by_no[p["site"]]["type"] == "store" and p["contact"] and not p.get("new_hire")
              and p["dept"][0] != "MGT"]
    pick = r.choice(len(movers), size=560, replace=False)
    windows = [(dt.date(2026, 7, 7), dt.date(2026, 8, 31), 300), (dt.date(2026, 9, 1), dt.date(2026, 9, 13), 150),
               (dt.date(2026, 9, 15), dt.date(2026, 9, 25), 110)]
    j = 0
    for (a, b, cnt) in windows:
        span = (b - a).days + 1
        for _ in range(cnt):
            p = movers[int(pick[j])]
            j += 1
            s = by_no[p["site"]]
            same = [x for x in by_tz[s["tz"]] if x["site_no"] != s["site_no"]]
            if s["tz"] != "America/Toronto":
                same = [x for x in same if x["tz"] == s["tz"]]
            local = [x for x in same if x["district"] == s["district"]]
            pool = local if (r.random() < 0.68 and local) else same
            t = pool[int(r.integers(len(pool)))]
            day = a + dt.timedelta(days=int(r.integers(span)))
            last = p["history"][-1]
            last["end"] = day - dt.timedelta(days=1)
            p["history"].append(dict(site=t["site_no"], dept=last["dept"], dept_name=last["dept_name"], start=day,
                                     end=None, action="transfer"))
            p["site"] = t["site_no"]
    # leavers: July to September
    stay = [p for p in people if not p.get("new_hire") and p["dept"][0] not in ("MGT", "OFF")
            and len(p["history"]) == 2]
    pick = r.choice(len(stay), size=470, replace=False)
    for i, q in enumerate(pick):
        p = stay[int(q)]
        if i < 330:
            day = dt.date(2026, 7, 10) + dt.timedelta(days=int(r.integers(52)))
        elif i < 400:
            day = dt.date(2026, 9, 1) + dt.timedelta(days=int(r.integers(13)))
        else:
            day = dt.date(2026, 9, 15) + dt.timedelta(days=int(r.integers(26)))
        p["history"][-1]["end"] = day - dt.timedelta(days=1)
        p["history"].append(dict(site=p["history"][-1]["site"], dept=p["history"][-1]["dept"],
                                 dept_name=p["history"][-1]["dept_name"], start=day, end=None, action="termination"))
        p["leave"] = day
    return people


def site_on(p, day):
    """The site an employee was assigned to on a day (None when not employed)."""
    if p["leave"] is not None and day >= p["leave"]:
        return None
    if day < p["hire"]:
        return None
    for h in p["history"]:
        if h["action"] == "termination":
            continue
        if h["start"] <= day and (h["end"] is None or day <= h["end"]):
            return h["site"]
    return None


def new_site(sites, no):
    """Legacy numbers resolve to the 2026 site number."""
    for s in sites:
        if s["legacy_no"] == no:
            return s["site_no"]
    return no


# ------------------------------------------------------------------ items and the latent model

def build_items():
    r = _rng(4)
    items = []
    for key, topic, kind, rev, en, fr in K.ITEMS:
        f = K.TOPIC_FACTOR[topic]
        lam = float(r.uniform(*LOAD[topic]))
        if kind == "yn":
            p = float(r.uniform(*YES[topic]))
            th = np.array([ndtri(1 - p)])
        else:
            pr = A5_SHARE * np.exp(r.normal(0, 0.25, 5))
            pr = pr / pr.sum()
            th = ndtri(np.cumsum(pr)[:-1])
            p = None
        dna = DNA_RATE.get(key, float(r.uniform(0.002, 0.009)))
        items.append(dict(key=key, topic=topic, factor=f, kind=kind, rev=rev, en=en, fr=fr, lam=lam, th=th, p=p,
                          dna=dna, skip=float(r.uniform(0.002, 0.007))))
    for it in items:
        it["en_code"] = "Q%02d" % (K.EN_ORDER.index(it["key"]) + 1)
        it["fr_code"] = "F%02d" % (K.FR_ORDER.index(it["key"]) + 1)
        it["library"] = "KL-%04d" % int(r.integers(1100, 9800))
    return items


def answers_for(items, n, seed_k):
    """Latent views and answer codes for n respondents. Codes: five-point 1-5 as given (negatively worded items as
    the employee answered the statement), yes/no 1 yes 2 no. Returns (codes n x 30, Z n x 30, F n x 3, enps n)."""
    r = _rng(seed_k)
    lam = np.zeros((len(items), 3))
    for j, it in enumerate(items):
        lam[j, it["factor"]] = it["lam"]
    F = r.standard_normal((n, 3)) @ np.linalg.cholesky(PHI).T
    uniq = np.sqrt(1 - (lam @ PHI * lam).sum(1))
    Z = F @ lam.T + r.standard_normal((n, len(items))) * uniq
    codes = np.zeros((n, len(items)), dtype=int)
    for j, it in enumerate(items):
        if it["kind"] == "yn":
            codes[:, j] = np.where(Z[:, j] > it["th"][0], 1, 2)
        else:
            z = -Z[:, j] if it["rev"] else Z[:, j]
            # the threshold set describes the favourable direction; a negatively worded statement mirrors it
            th = -it["th"][::-1] if it["rev"] else it["th"]
            codes[:, j] = np.searchsorted(th, z) + 1
    e = 0.55 * F[:, 0] + 0.45 * F[:, 1] + 0.45 * F[:, 2] + r.standard_normal(n) * 0.62
    enps = np.clip(np.round(7.1 + 2.0 * e), 0, 10).astype(int)
    return codes, Z, F, enps


# ------------------------------------------------------------------ the survey

def _local_to_utc(day, seconds, tz):
    return dt.datetime(day.year, day.month, day.day) + dt.timedelta(seconds=float(seconds)) - \
        dt.timedelta(hours=K.TZ_OFFSET[tz])


def build_survey():
    sites = build_sites()
    by_no = {s["site_no"]: s for s in sites}
    people = build_history(sites, build_people(sites))
    items = build_items()
    r = _rng(5)
    rt = _rng(6)
    # the distribution list: everyone employed on 31 August with an email or SMS contact, and every employee of a
    # store without a kiosk who has neither (a printed form)
    invite = []
    for p in people:
        s31 = site_on(p, K.INVITE_EXTRACT)
        if s31 is None or p["hire"] > K.INVITE_EXTRACT:
            continue
        site = by_no[s31]
        if p["contact"]:
            ch = p["contact"]
        elif site["type"] == "store" and not site["kiosk"]:
            ch = "printed form"
        else:
            continue
        invite.append(dict(emp=p["emp"], site=s31, lang=p["lang"], channel=ch))
        p["invite"] = invite[-1]
    # tokens
    alphabet = np.array(list("ACDEFGHJKLMNPQRTUVWXY34679"))
    used = set()

    def token():
        while True:
            t = "".join(alphabet[r.integers(len(alphabet), size=9)])
            if t not in used:
                used.add(t)
                return t
    for inv in invite:
        inv["token"] = token()
    # who answers, and how
    resp = []
    for p in people:
        open_site = site_on(p, K.OPEN_DAY)
        if open_site is None:
            continue
        s = by_no[open_site]
        if "invite" in p:
            ch = p["invite"]["channel"]
        elif s["kiosk"] and p["hire"] <= dt.date(2026, 9, 13):
            ch = "kiosk"
        else:
            continue
        if r.random() >= PROPENSITY[ch]:
            continue
        resp.append(dict(p=p, channel=ch, open_site=open_site))
    codes, Z, F, enps = answers_for(items, len(resp), 7)
    for i, x in enumerate(resp):
        x["codes"] = codes[i].copy()
        x["z"] = Z[i]
        x["enps"] = int(enps[i])
        x["idx"] = i
    # does not apply and skipped items (clean truth: the employee's final answers; 0 = left blank)
    for j, it in enumerate(items):
        for x in resp:
            u = r.random()
            if u < it["dna"]:
                x["codes"][j] = 6
            elif u < it["dna"] + it["skip"] * (2.2 if x["channel"] == "printed form" else 1.0):
                x["codes"][j] = 0
    # paper returns: each store without a kiosk sends its forms in two envelopes, one at the courier's mid-survey
    # pickup and one at the end; Kestrava keys each envelope when it arrives
    paper_sites = sorted(s["site_no"] for s in sites if s["type"] == "store" and not s["kiosk"])
    envelopes = {}
    for no in paper_sites:
        e1 = dt.date(2026, 9, 21) + dt.timedelta(days=int(rt.integers(0, 2)))
        r1 = e1 + dt.timedelta(days=int(rt.integers(2, 4)))
        k1 = min(r1 + dt.timedelta(days=int(rt.integers(0, 2))), dt.date(2026, 9, 25))
        e2 = dt.date(2026, 9, 27) - dt.timedelta(days=int(rt.choice(2, p=[0.7, 0.3])))
        r2 = dt.date(2026, 9, 29) + dt.timedelta(days=int(rt.integers(0, 4)))
        k2 = r2 + dt.timedelta(days=int(rt.integers(2, 6)))
        if k2.weekday() >= 5:
            k2 += dt.timedelta(days=7 - k2.weekday())
        envelopes[(no, 1)] = dict(site=no, n=1, sealed=e1, received=r1, keyed=k1, forms=[], blank=0)
        envelopes[(no, 2)] = dict(site=no, n=2, sealed=e2, received=r2, keyed=k2, forms=[], blank=0)
    sub = []        # submissions: token, submission, channel, lang, status, answers [(item j, code, utc)], enps
    kiosk_log = []
    late = []
    for x in resp:
        p = x["p"]
        s = by_no[x["open_site"]]
        tz = s["tz"]
        order = K.FR_ORDER if p["lang"] == "FR" else K.EN_ORDER
        seq = [next(j for j, it in enumerate(items) if it["key"] == key) for key in order]
        close = K.local_close_utc(tz)
        if x["channel"] in ("email", "sms"):
            night = p["night"]
            leave_idx = (p["leave"] - K.OPEN_DAY).days if p["leave"] is not None else None
            start = None
            for _ in range(40):
                day = int(rt.choice(14, p=np.array(WEB_DAY_W) / sum(WEB_DAY_W)))
                if leave_idx is not None and day >= leave_idx:
                    continue
                if night:
                    sec = (rt.uniform(22.4, 27.2) if rt.random() < 0.62 else rt.uniform(5.5, 8.0)) * 3600
                else:
                    u = rt.random()
                    sec = (rt.uniform(6.2, 9.0) if u < 0.30 else (rt.uniform(11.8, 15.2) if u < 0.62 else
                                                                  rt.uniform(17.5, 23.7))) * 3600
                start = _local_to_utc(_day(day), sec, tz)
                if start < K.LINKS_CLOSED_UTC:
                    break
                start = None
            if start is None:
                continue
            dwell = rt.uniform(5, 32, size=31)
            stamps = [start + dt.timedelta(seconds=float(v)) for v in np.cumsum(dwell)]
            if start <= close < stamps[-1]:
                shift = (stamps[-1] - close).total_seconds() + rt.uniform(60, 1800)
                start -= dt.timedelta(seconds=shift)
                stamps = [t - dt.timedelta(seconds=shift) for t in stamps]
            if stamps[-1] > K.LINKS_CLOSED_UTC:
                continue
            breakoff = int(rt.integers(1, 30)) if rt.random() < 0.05 else None
            ans = []
            for pos, j in enumerate(seq):
                if breakoff is not None and pos >= breakoff:
                    break
                c = int(x["codes"][j])
                if c:
                    ans.append((j, c, stamps[pos]))
            if not ans:
                continue
            e = x["enps"] if breakoff is None and rt.random() > 0.03 else None
            first = dict(token=p["invite"]["token"], n=1, channel="web", lang=p["lang"],
                         status="saved" if breakoff is not None else "submitted", answers=ans,
                         enps=(e, stamps[30]) if e is not None else None, x=x)
            if start > close:
                late.append(x)
                x["late"] = True
            sub.append(first)
            x["subs"] = [first]
            if breakoff is None and start < close and rt.random() < 0.026:
                gap = rt.uniform(1.5, 70) * 3600
                if stamps[-1] + dt.timedelta(seconds=gap + 900) < close:
                    st2 = stamps[-1] + dt.timedelta(seconds=gap)
                    dw2 = rt.uniform(2, 9, size=31)
                    s2 = [st2 + dt.timedelta(seconds=float(v)) for v in np.cumsum(dw2)]
                    changed = set(rt.choice(30, size=2, replace=False).tolist())
                    ans2 = []
                    for pos, j in enumerate(seq):
                        c = int(x["codes"][j])
                        if c:
                            ans2.append((j, c, s2[pos]))
                    # the first submission held the employee's earlier answers on two items
                    old = []
                    for (j, c, t) in ans:
                        if j in changed and items[j]["kind"] == "a5" and c in (2, 3, 4):
                            c = c + (1 if rt.random() < 0.5 else -1)
                        elif j in changed and items[j]["kind"] == "yn" and c in (1, 2):
                            c = 3 - c
                        old.append((j, c, t))
                    first["answers"] = old
                    second = dict(token=p["invite"]["token"], n=2, channel="web", lang=p["lang"], status="submitted",
                                  answers=ans2, enps=(x["enps"], s2[30]) if e is not None else None, x=x)
                    sub.append(second)
                    x["subs"].append(second)
        elif x["channel"] == "kiosk":
            leave_idx = (p["leave"] - K.OPEN_DAY).days if p["leave"] is not None else None
            start = None
            for _ in range(40):
                day = int(rt.choice(14, p=np.array(KIOSK_DAY_W) / sum(KIOSK_DAY_W)))
                if leave_idx is not None and day >= leave_idx:
                    continue
                sec = rt.uniform(7.0, 22.6) * 3600
                start = _local_to_utc(_day(day), sec, tz)
                if start + dt.timedelta(minutes=40) < close:
                    break
                start = None
            if start is None:
                continue
            sessions = []
            pos = 0
            t = start
            timeouts = 0
            while pos < 31:
                sess_start = t
                dwell = rt.uniform(5, 28, size=31 - pos)
                stamps = [sess_start + dt.timedelta(seconds=float(v)) for v in np.cumsum(dwell)]
                stop = None
                reason = "submitted"
                if timeouts < 2 and rt.random() < (0.093 if timeouts == 0 else 0.05) and 31 - pos > 4:
                    stop = int(rt.integers(2, 31 - pos - 1))
                    reason = "timed out"
                elif pos == 0 and rt.random() < 0.018:
                    stop = int(rt.integers(3, 25))
                    reason = "signed out"
                end_pos = 31 if stop is None else pos + stop
                ans = []
                e = None
                for k2, q in enumerate(range(pos, end_pos)):
                    if q == 30:
                        if rt.random() > 0.05:
                            e = (x["enps"], stamps[k2])
                        continue
                    j = seq[q]
                    c = int(x["codes"][j])
                    if c:
                        ans.append((j, c, stamps[k2]))
                last_t = stamps[end_pos - pos - 1]
                closed = last_t + (dt.timedelta(minutes=20) if reason == "timed out" else
                                   dt.timedelta(seconds=float(rt.uniform(3, 40))))
                if closed > close:
                    closed = close
                sessions.append(dict(token=token(), n=1, channel="kiosk", lang=p["lang"],
                                     status="submitted" if end_pos == 31 else "saved", answers=ans, enps=e, x=x,
                                     signed_in=sess_start - dt.timedelta(seconds=float(rt.uniform(15, 70))),
                                     closed=closed, reason=reason))
                if reason != "timed out":
                    break
                timeouts += 1
                if rt.random() >= 0.68:
                    break
                back = rt.uniform(0.5, 30) * 3600 if rt.random() < 0.6 else rt.uniform(18, 80) * 3600
                t = closed + dt.timedelta(seconds=back)
                local_hour = ((t + dt.timedelta(hours=K.TZ_OFFSET[tz])).hour)
                if local_hour < 7 or local_hour >= 23:
                    t += dt.timedelta(hours=9)
                if t + dt.timedelta(minutes=25) >= close:
                    break
                pos = end_pos
            sessions = [z for z in sessions if z["answers"] or z["enps"]]
            if not sessions:
                continue
            for z in sessions:
                sub.append(z)
                kiosk_log.append(dict(session=z["token"], store=by_no[x["open_site"]]["legacy_no"],
                                      kiosk="K%d" % (1 + int(rt.integers(2 if s["size"] >= 190 else 1))),
                                      emp=p["emp"], emp_typed=p["emp"], signed_in=z["signed_in"], closed=z["closed"],
                                      reason=z["reason"], tz=tz))
            x["subs"] = sessions
        else:   # printed form, keyed by Kestrava from the store's envelope
            leave_idx = (p["leave"] - K.OPEN_DAY).days if p["leave"] is not None else 14
            fill = int(rt.choice(14, p=np.array(KIOSK_DAY_W) / sum(KIOSK_DAY_W)))
            fill = min(fill, max(leave_idx - 1, 0))
            first_env = envelopes[(x["open_site"], 1)]
            env = first_env if _day(fill) < first_env["sealed"] else envelopes[(x["open_site"], 2)]
            ans = [(j, int(x["codes"][j]), None) for j in seq if int(x["codes"][j])]
            if not ans:
                env["blank"] += 1
                continue
            z = dict(token=p["invite"]["token"], n=1, channel="paper", lang=p["lang"], status="submitted",
                     answers=ans, enps=(x["enps"], None) if rt.random() > 0.11 else None, x=x)
            env["forms"].append(z)
            sub.append(z)
            x["subs"] = [z]
    # blank forms and keying times
    for key in sorted(envelopes):
        env = envelopes[key]
        env["blank"] += int(rt.integers(0, 3))
        t = dt.datetime(env["keyed"].year, env["keyed"].month, env["keyed"].day, 13, 5) + \
            dt.timedelta(minutes=float(rt.uniform(0, 240)))
        for z in env["forms"]:
            t += dt.timedelta(seconds=float(rt.uniform(55, 130)))
            z["answers"] = [(j, c, t) for (j, c, _) in z["answers"]]
            if z["enps"] is not None:
                z["enps"] = (z["enps"][0], t)
    # Kestrava's pre-launch test tokens
    tests = []
    for i in range(36):
        lang = "FR" if i % 3 == 2 else "EN"
        day = K.TEST_DAYS[i // 18]
        t0 = dt.datetime(day.year, day.month, day.day, 14, 0) + dt.timedelta(minutes=float(rt.uniform(0, 330)))
        ans = []
        for q, key in enumerate(K.FR_ORDER if lang == "FR" else K.EN_ORDER):
            j = next(jj for jj, it in enumerate(items) if it["key"] == key)
            c = int(rt.integers(1, 6)) if items[j]["kind"] == "a5" else int(rt.integers(1, 3))
            ans.append((j, c, t0 + dt.timedelta(seconds=4 * (q + 1))))
        z = dict(token=token(), n=1, channel="web", lang=lang, status="test", answers=ans,
                 enps=(int(rt.integers(0, 11)), t0 + dt.timedelta(seconds=128)), x=None)
        tests.append(z)
        sub.append(z)
    resp = [x for x in resp if x.get("subs")]
    return dict(sites=sites, people=people, items=items, invite=invite, resp=resp, sub=sub, kiosk=kiosk_log,
                envelopes=envelopes, tests=tests)
