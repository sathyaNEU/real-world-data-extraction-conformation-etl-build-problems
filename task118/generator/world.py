"""The board's hypnotic users and their records: each patient's true start, the repeat-template chains (one
practice's split at its July 2026 system move), and the items dispensed April to September 2026."""
import datetime as dt
import hashlib

import numpy as np

import params as P

D = dt.timedelta


def rid(*key, n=10, alpha="ABCDEFGHJKLMNPQRSTUVWXYZ23456789"):
    h = hashlib.sha1("|".join(str(k) for k in key).encode()).digest()
    return "".join(alpha[b % len(alpha)] for b in h[:n])


def day(rs, a, b):
    return a + D(days=int(rs.integers(0, (b - a).days + 1)))


STREETS = ["Station Road", "Church Lane", "Market Street", "Mill Road", "High Street", "Park View", "Bridge Street",
           "Orchard Way", "Castle Hill", "Green Lane", "Quay Street", "Abbey Road", "Victoria Road", "North Street",
           "The Green", "Priory Lane", "West End", "Harbour Road", "Elm Grove", "School Lane"]
KINDS = ["Surgery", "Medical Centre", "Health Centre", "Medical Practice", "Family Practice", "Group Practice"]


def practices():
    """the register: code, name, locality, the code it took over (Fenmarsh Health Centre took Marsh Lane Surgery's list
    on 1 October 2025) and its share of the locality's patients"""
    rs = np.random.default_rng(P.SEED + 1)
    out, used, s = [], {P.MERGED[0]}, 0
    for code, name, _, _ in P.LOCALITIES:
        k = P.PRACTICES[code]
        w = rs.dirichlet(np.full(k, 4.0))
        for j in range(k):
            while True:
                pc = "Q8%04d" % int(rs.integers(100, 9999))
                if pc not in used:
                    used.add(pc)
                    break
            town = name.split()[0]
            out.append(dict(code=pc, name="%s %s" % (STREETS[s % len(STREETS)], KINDS[(s * 7) % len(KINDS)]),
                            town=town, locality=code, predecessor="", weight=float(w[j])))
            s += 1
    fm = [p for p in out if p["locality"] == "FM"]
    fm[1]["name"] = "Fenmarsh Health Centre"
    fm[1]["predecessor"] = P.MERGED[0]
    return out


def migrated_practice(prs):
    """the Quenford Rise practice that moved clinical system in July 2026"""
    return sorted([p for p in prs if p["locality"] == P.MIGRATED], key=lambda p: p["weight"])[0]


def _age(rs):
    return int(min(99, 65 + rs.gamma(2.0, 6.0)))


def _drug(rs):
    sh = np.array([d[5] for d in P.DRUGS])
    return P.DRUGS[int(rs.choice(len(P.DRUGS), p=sh / sh.sum()))]


def users(prs):
    """every patient in the extract: the current users aged 65 or over by when they first started, the patients who
    stopped before July 2026, and the current users aged under 65 on 1 January 2027"""
    rs = np.random.default_rng(P.SEED)
    by_loc = {}
    for p in prs:
        by_loc.setdefault(p["locality"], []).append(p)
    out = []
    windows = {"long": (dt.date(2008, 1, 1), dt.date(2025, 3, 31)), "mid": (dt.date(2025, 4, 1), dt.date(2026, 3, 31)),
               "new": (dt.date(2026, 4, 1), dt.date(2026, 9, 20))}

    def practice(code):
        ps = by_loc[code]
        w = np.array([p["weight"] for p in ps])
        return ps[int(rs.choice(len(ps), p=w / w.sum()))]["code"]

    for code, name, n, shares in P.LOCALITIES:
        k_mid, k_new = int(round(n * shares[1])), int(round(n * shares[2]))
        k_long = n - k_mid - k_new
        for i in range(n):
            cls = "long" if i < k_long else ("mid" if i < k_long + k_mid else "new")
            start = day(rs, *windows[cls])
            age = _age(rs)
            out.append(dict(pid="P" + rid("pt", code, i, n=9), loc=code, practice=practice(code), start=start,
                            yob=2026 - age, sex="F" if rs.random() < 0.66 else "M", drug=_drug(rs), cls=cls,
                            current=True, stop=None))
        for i in range(int(round(n * P.STOPPED_SHARE))):
            if i % 3 == 0:     # a short course started in April or May 2026, one or two packs
                start = day(rs, dt.date(2026, 4, 1), dt.date(2026, 5, 8))
                stop = start + D(days=int(rs.choice([20, 48])))
            else:
                start = day(rs, dt.date(2010, 1, 1), dt.date(2025, 12, 31))
                stop = day(rs, dt.date(2026, 4, 20), dt.date(2026, 6, 26))
            age = _age(rs)
            out.append(dict(pid="P" + rid("ex", code, i, n=9), loc=code, practice=practice(code), start=start,
                            yob=2026 - age, sex="F" if rs.random() < 0.66 else "M", drug=_drug(rs), cls="stopped",
                            current=False, stop=stop))
        for i in range(int(round(n * P.UNDER_65_SHARE))):
            yob = int(rs.integers(1962, 1967))
            # the 1962-born (64 on 1 January 2027, 65 during the year) have all been on the drug for years
            start = day(rs, dt.date(2015, 1, 1), dt.date(2023, 12, 31) if yob == 1962 else dt.date(2026, 8, 31))
            out.append(dict(pid="P" + rid("yg", code, i, n=9), loc=code, practice=practice(code), start=start,
                            yob=yob, sex="F" if rs.random() < 0.6 else "M", drug=_drug(rs),
                            cls="under65", current=True, stop=None))
    return out


def _auths(rs, u):
    """the authorisation dates of the patient's repeat templates: twelve packs each, re-authorised as the last runs out"""
    span = 12 * u["drug"][3]
    last = u["stop"] or P.TEMPLATES_AS_AT - D(days=1)
    a = [u["start"]]
    while True:
        nxt = a[-1] + D(days=span + int(rs.integers(-10, 16)))
        if nxt > last:
            return a
        a.append(nxt)


DIRECTIONS = {"Z-drug": ["ONE to be taken at night", "ONE at night when required", "ONE to be taken at bedtime"],
              "benzodiazepine": ["ONE to be taken at night", "ONE at night when required", "ONE to be taken at bedtime",
                                 "ONE to be taken at night as directed"]}


def templates(us, prs):
    """the current system's export (every template active on or after 1 April 2024, as at 1 October 2026) and the
    previous system's export for the practice that moved in July 2026 (taken on its last day on the old system)"""
    rs = np.random.default_rng(P.SEED + 2)
    move = {migrated_practice(prs)["code"]: P.MIGRATION}
    cur, leg = [], []
    for u in us:
        auths = _auths(rs, u)
        mv = move.get(u["practice"])
        if mv is not None:     # no re-authorisation in the days the practice was moving
            auths = [a if (j == 0 or not (mv - D(days=3) <= a <= mv + D(days=3))) else mv + D(days=4)
                     for j, a in enumerate(auths)]
        directions = DIRECTIONS[u["drug"][2]][int(rs.integers(0, len(DIRECTIONS[u["drug"][2]])))]
        prev_cur, prev_leg = "", ""
        legacy_active = None
        for j, a0 in enumerate(auths):
            review = a0 + D(days=364)
            nxt = auths[j + 1] if j + 1 < len(auths) else None
            ended = (nxt - D(days=1)) if nxt else (u["stop"] if u["stop"] else None)
            reason = "Reauthorised" if nxt else ("Stopped" if u["stop"] else "")
            in_window = (ended or review) >= P.TEMPLATES_ACTIVE_SINCE
            if mv is not None and a0 < mv:
                ref = "%s/%d" % (u["practice"][-4:], int(rid("lt", u["pid"], j, n=7, alpha="0123456789")))
                if in_window:
                    if ended is not None and ended >= mv:
                        ended_leg, reason_leg = None, ""
                    else:
                        ended_leg, reason_leg = ended, reason
                    leg.append(dict(template_ref=ref, patient_pseudo_id=u["pid"], practice_code=u["practice"],
                                    drug=u["drug"][1].upper(), directions=directions.upper(),
                                    qty=u["drug"][3], issues=12, start_date=a0, review_date=review, end_date=ended_leg,
                                    end_reason=reason_leg.upper(), superseded_ref=prev_leg))
                prev_leg = ref
                if ended is None or ended >= mv:
                    legacy_active = (ref, review, ended, reason)
            else:
                if legacy_active is not None and not prev_cur:
                    # the move re-created the active template on the new system, dated the day of the move
                    ref, rv, en, rsn = legacy_active
                    tid = "T" + rid("mv", u["pid"], n=9)
                    en2 = (a0 - D(days=1))
                    cur.append(dict(template_id=tid, patient_pseudo_id=u["pid"], practice_code=u["practice"],
                                    product=u["drug"][1], directions=directions, quantity=u["drug"][3], issues=12,
                                    authorised_from=mv, review_date=rv, ended_on=en2, end_reason="Reauthorised",
                                    replaces_template_id="", migration_source_ref=ref))
                    prev_cur = tid
                tid = "T" + rid("tp", u["pid"], j, n=9)
                if in_window:
                    cur.append(dict(template_id=tid, patient_pseudo_id=u["pid"], practice_code=u["practice"],
                                    product=u["drug"][1], directions=directions, quantity=u["drug"][3], issues=12,
                                    authorised_from=a0, review_date=review, ended_on=ended, end_reason=reason,
                                    replaces_template_id=prev_cur, migration_source_ref=""))
                prev_cur = tid
        if legacy_active is not None and not prev_cur:
            ref, rv, en, rsn = legacy_active
            tid = "T" + rid("mv", u["pid"], n=9)
            cur.append(dict(template_id=tid, patient_pseudo_id=u["pid"], practice_code=u["practice"],
                            product=u["drug"][1], directions=directions, quantity=u["drug"][3], issues=12,
                            authorised_from=mv, review_date=rv, ended_on=en, end_reason=rsn,
                            replaces_template_id="", migration_source_ref=ref))
    return cur, leg, move


def dispensing(us):
    """items dispensed 1 April to 30 September 2026: a pack every 28 days (30 for lormetazepam) from the start, or from
    the first collection after 1 April, to the stop or the extract's end; the first pack of a new start is dispensed the
    day it is authorised"""
    rs = np.random.default_rng(P.SEED + 3)
    rows = []
    for u in us:
        step = u["drug"][3]
        if u["start"] >= P.EXTRACT_FROM:
            d = u["start"]
        else:
            d = P.EXTRACT_FROM + D(days=int(rs.integers(0, step)))
        last = u["stop"] or P.EXTRACT_TO
        while d <= min(last, P.EXTRACT_TO):
            rows.append(dict(dispensed_date=d, patient_pseudo_id=u["pid"], practice_code=u["practice"],
                             product=u["drug"][1], quantity=u["drug"][3], nic_gbp=u["drug"][4], year_of_birth=u["yob"],
                             sex=u["sex"]))
            d = d + D(days=step + int(rs.integers(-3, 5)))
    rows.sort(key=lambda r: (r["dispensed_date"], r["practice_code"], r["patient_pseudo_id"]))
    return rows
