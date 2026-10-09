"""Referrals, patients, deaths and admitted patient care episodes, built on the simulated stays."""
import datetime as dt
from collections import defaultdict

import numpy as np

from common import (LETTERS, CODE, TRUSTS, HDU, FEED_UNITS, RECORD0, RECORD1, PARALLEL0, PARALLEL1, EXTRACT, lm,
                    day_of, to_dt, own_unit, crosses_dst, DST_WINDOWS, is_bst, rng, year_of, DAY)
from world import LEGACY_END, BST_LEGACY_END, daterange

WARDS = {
    "A": ["ED", "AMU", "W12", "W14", "W21", "W23", "SAU", "CCU", "W30", "W31"],
    "B": ["ED", "AMU", "W3", "W5", "W7", "SAU"],
    "C": ["ED", "AMU", "W6A", "W6B", "W9", "W11", "SAU", "CCU"],
    "D": ["ED", "AMU", "W2", "W4", "W8", "W10", "SAU", "SDU", "W15"],
    "E": ["ED", "AMU", "W1", "W2", "W5", "W6", "SAU", "W8"],
    "F": ["ED", "AMU", "W4", "W9", "W10", "SAU"],
    "G": ["ED", "AMU", "W1", "W3", "W5", "W7", "SAU"],
    "H": ["ED", "AMU", "W2", "W6", "SAU"],
}
PILOT_WARDS = {L: ["AMU", WARDS[L][2]] for L in LETTERS}
SPECIALTY = ["300", "300", "300", "340", "320", "100", "100", "430", "110", "101", "180", "361"]
FREE_RATES = {  # per day: stood down, died before admission (short), level-2 admitted to the trust's HDU
    "A": (1.55, 0.06, 0.0), "B": (0.55, 0.03, 1.15), "C": (1.05, 0.05, 0.0), "D": (0.95, 0.04, 0.0),
    "E": (1.3, 0.07, 2.3), "F": (0.6, 0.03, 1.25), "G": (0.75, 0.03, 0.0), "H": (0.4, 0.02, 0.85)}


def ward_for(L, r, pilot=False, avoid_pilot=False):
    if pilot:
        return str(r.choice(PILOT_WARDS[L]))
    w = [x for x in WARDS[L] if not (avoid_pilot and x in PILOT_WARDS[L])]
    p = np.array([2.6 if x == "ED" else 1.6 if x == "AMU" else 1.0 for x in w])
    return str(r.choice(w, p=p / p.sum()))


def short_wait(r, t_end, bst_legacy):
    """A wait that stays clear of four hours on every clock and of the clock changes."""
    hi = 170 if bst_legacy else 225
    for _ in range(50):
        w = int(np.clip(np.exp(r.normal(np.log(55), 0.75)), 8, hi))
        if not crosses_dst(t_end - w - 5, t_end):
            return w
    return 8


def receipt_delay(r):
    return int(np.clip(np.exp(r.normal(np.log(35), 0.7)), 4, 200))


def build_referrals(world, P, stays):
    r = rng("referrals")
    refs = []
    stay_of = defaultdict(list)
    for i, s in enumerate(stays):
        stay_of[s["pid"]].append(i)

    def add(**kw):
        kw["rid"] = len(refs)
        kw.setdefault("tags", set())
        kw.setdefault("wid", None)
        kw.setdefault("stay", None)
        kw["legacy"] = day_of(kw["dta"]) < dt.date(2024, 4, 2)
        refs.append(kw)
        return kw

    # designed waits
    for w in sorted(world.waits, key=lambda w: w["dta"]):
        L = w["letter"]
        bst = w["dta"] < lm(BST_LEGACY_END, 23, 59) and is_bst(w["dta"])
        rec = w["dta"] - receipt_delay(r)
        stay = None
        if w["outcome"] == "admitted":
            cand = [i for i in stay_of[w["pid"]] if stays[i]["admit"] == w["end"] and stays[i]["unit"] == w["unit"]]
            assert len(cand) == 1, ("stay for wait", w["wid"], cand)
            stay = cand[0]
        pilot = "HZ2" in w["tags"]
        in_par = PARALLEL0 <= day_of(w["dta"]) <= PARALLEL1
        add(pid=w["pid"], letter=L, ward=ward_for(L, r, pilot, avoid_pilot=in_par and not pilot), received=rec, dta=w["dta"], level_req=w["level_req"],
            level_dec=w["level_dec"], outcome="admitted" if w["outcome"] == "admitted" else "died",
            end=w["end"], unit=w["unit"], wid=w["wid"], tags=set(w["tags"]), stay=stay, pilot=pilot)
    # background admissions at the feed units
    designed_pids = {w["pid"] for w in world.waits}
    for i, s in enumerate(stays):
        p = P.p[s["pid"]]
        if p["kind"] != "bg":
            continue
        L = p["letter"]
        t = s["admit"]
        bst = t < lm(dt.date(2024, 4, 2)) and is_bst(t)
        wt = short_wait(r, t, bst)
        dta = t - wt
        rec = dta - receipt_delay(r)
        add(pid=s["pid"], letter=L, ward=ward_for(L, r), received=rec, dta=dta, level_req=p["level"],
            level_dec=p["level"], outcome="admitted", end=t, unit=s["unit"], stay=i, pilot=False)
    # free rows: stood down, died before admission (short), level-2 admitted to the trust's high dependency unit
    for L in LETTERS:
        rs = rng("free", L)
        sd, dw, hdu = FREE_RATES[L]
        for d in daterange(RECORD0, RECORD1):
            hdu_rate = hdu
            if L == "F" and own_unit("F", d) is not None:
                hdu_rate = 0.0          # Ellerdyke's level-2 patients use its own combined unit while it is level 3
            for kind, rate in (("stood_down", sd), ("died", dw), ("hdu", hdu_rate)):
                for _ in range(int(rs.poisson(rate))):
                    for attempt in range(20):
                        h = int(rs.choice(24, p=HOUR_P))
                        dta = lm(d) + h * 60 + int(rs.integers(0, 60))
                        if kind == "hdu":
                            wt = int(np.clip(np.exp(rs.normal(np.log(90), 0.8)), 10, 520))
                            if 225 <= wt <= 255:
                                continue
                        else:
                            wt = int(rs.integers(15, 226))
                        if crosses_dst(dta - 210, dta + wt + 5):
                            continue
                        break
                    else:
                        continue
                    lvl = 2 if kind == "hdu" else (3 if (kind == "died" or rs.random() < 0.55) else 2)
                    pid = P.new(kind="free", letter=L, level=lvl)
                    add(pid=pid, letter=L, ward=ward_for(L, rs), received=dta - receipt_delay(rs), dta=dta,
                        level_req=lvl, level_dec=lvl, outcome={"stood_down": "stood_down", "died": "died",
                                                               "hdu": "admitted"}[kind],
                        end=dta + wt, unit=HDU.get(L) if kind == "hdu" else None, pilot=False)
    # the genuine same-day referral before each HZ2oc wait: referred, stood down, referred again later
    for ref in [x for x in refs if "HZ2oc" in x["tags"]]:
        rs = rng("hz2oc", ref["rid"])
        first_dta = ref["received"] - int(rs.integers(160, 300))
        sd_at = first_dta + int(rs.integers(40, 110))
        assert sd_at < ref["received"] - 20 and day_of(first_dta) == day_of(ref["dta"])
        add(pid=ref["pid"], letter=ref["letter"], ward=ref["ward"], received=first_dta - receipt_delay(rs),
            dta=first_dta, level_req=3, level_dec=3, outcome="stood_down", end=sd_at, unit=None,
            tags={"HZ2oc_first"}, pilot=False)
    # the extract holds decisions to admit inside the record; stays admitted earlier keep their referral number
    refs = [x for x in refs if RECORD0 <= day_of(x["dta"]) <= RECORD1]
    refs.sort(key=lambda x: (x["received"], x["rid"]))
    for i, x in enumerate(refs):
        x["rid"] = x["rid"]
    return refs


HOUR_W = np.array([0.45, 0.35, 0.3, 0.3, 0.3, 0.35, 0.5, 0.8, 1.2, 1.5, 1.6, 1.6, 1.5, 1.5, 1.5, 1.5, 1.4, 1.3,
                   1.2, 1.1, 1.0, 0.85, 0.7, 0.55])
HOUR_P = HOUR_W / HOUR_W.sum()


# ------------------------------------------------------------------------------------------ identities
def hexkey(r):
    return "".join("0123456789ABCDEF"[int(x)] for x in r.integers(0, 16, size=12))


def assign_identities(world, P, refs, death):
    """Verified keys; a few repeat patients among background referrals (never a patient holding a long
    wait, never one who died before the later referral); temporary keys on some migrated ED referrals."""
    r = rng("keys")
    used = set()
    for pid in sorted(P.p):
        while True:
            k = hexkey(r)
            if k not in used:
                used.add(k)
                break
        P.p[pid]["key"] = k
        P.p[pid]["person"] = pid
    by_trust = defaultdict(list)
    for ref in refs:
        if ref["wid"] is None and not ref["tags"] and P.p[ref["pid"]]["kind"] in ("bg", "free"):
            by_trust[ref["letter"]].append(ref)
    taken = set()
    for L in LETTERS:
        lst = sorted(by_trust[L], key=lambda x: (x["dta"], x["rid"]))
        for i in range(80, len(lst)):
            if r.random() >= 0.055:
                continue
            later = lst[i]
            j = int(r.integers(max(0, i - 900), i - 60))
            earlier = lst[j]
            a, b = earlier["pid"], later["pid"]
            if a in taken or b in taken or later["dta"] - earlier["dta"] < 45 * DAY:
                continue
            if death.get(a) is not None:
                continue
            taken.add(a)
            taken.add(b)
            P.p[b]["person"] = a
            P.p[b]["key"] = P.p[a]["key"]
            if death.get(b) is not None:
                death[a] = death[b]
    # temporary identities on migrated legacy referrals from the emergency department
    temp = {}
    picked = [ref for ref in refs if ref["tags"] & {"DV2a", "DV2b1"}]
    benign = [ref for ref in refs if ref["legacy"] and ref["wid"] is None and not ref["tags"]
              and P.p[ref["pid"]]["kind"] in ("bg", "free") and ref["ward"] == "ED"
              and P.p[ref["pid"]]["person"] == ref["pid"] and ref["pid"] not in taken]
    r.shuffle(benign)
    nums = set()
    for ref in sorted(picked + benign[:150], key=lambda x: x["rid"]):
        while True:
            k = "U%09d" % int(r.integers(100000000, 999999999))
            if k not in nums:
                nums.add(k)
                break
        temp[ref["rid"]] = k
        ref["ward"] = "ED"
    return temp


# ------------------------------------------------------------------------------------------ deaths
def assign_deaths(world, P, refs, stays):
    """Date of death per patient, or None. Long-wait deaths fall on days 0 to 24 after the decision;
    long-wait survivors live past day 35. 'where' says how the death is recorded."""
    r = rng("deaths")
    death, where = {}, {}
    wref = {ref["wid"]: ref for ref in refs if ref["wid"] is not None}
    for w in world.waits:
        ref = wref[w["wid"]]
        pid = w["pid"]
        dta_day = day_of(w["dta"])
        if w["tags"] & {"DV2b1", "DV2b2"}:
            continue
        if not w["died"]:
            if r.random() < 0.12:
                death[pid] = dta_day + dt.timedelta(days=int(r.integers(36, 91)))
                where[pid] = "later"
            continue
        if w["outcome"] == "died_waiting":
            death[pid] = day_of(w["end"])
            where[pid] = "waiting"
            continue
        s = stays[ref["stay"]]
        off = (day_of(s["discharge"]) - dta_day).days
        assert off <= 20, ("designed death after the deadline", w["wid"], off)
        if "DV2a" in w["tags"]:
            death[pid], where[pid] = None, "readmission"
            continue
        u = r.random()
        if u < 0.55 or off >= 19:
            death[pid], where[pid] = day_of(s["discharge"]), "icu"
        elif u < 0.78:
            death[pid] = day_of(s["discharge"]) + dt.timedelta(days=int(r.integers(1, 5)))
            where[pid] = "ward"
        else:
            death[pid], where[pid] = None, "after_discharge"
    for ref in refs:
        pid = ref["pid"]
        if P.p[pid]["kind"] not in ("bg", "free") or pid in where:
            continue
        if ref["outcome"] == "died":
            death[pid], where[pid] = day_of(ref["end"]), "waiting"
            continue
        q = ({3: 0.21, 2: 0.08}[ref["level_dec"]]) if ref["outcome"] == "admitted" else 0.06
        if r.random() < q:
            death[pid] = day_of(ref["dta"]) + dt.timedelta(days=int(r.integers(0, 75)))
            where[pid] = "bg"
    return death, where


# ------------------------------------------------------------------------------------------ episodes
ADM_METHOD_WARD = ["21", "21", "22", "28", "21", "11", "12"]
LAST_LINKED_DEATH = dt.date(2026, 7, 31)


def build_episodes(world, P, refs, stays, death, where, temp):
    """Admitted patient care episodes for every person with a referral. Returns rows and the verified
    key of every person; finalises the deaths recorded after discharge or in a readmission."""
    r = rng("episodes")
    persons = defaultdict(list)
    for ref in refs:
        persons[P.p[ref["pid"]]["person"]].append(ref)
    rows = []
    counter = [0]
    end_cap = EXTRACT - dt.timedelta(days=1)
    feed = ("RIS-ACC", "BRK-ACC", "STN-ACC", "PRW-ACC", "ELL-ACC", "PEL-W3")

    def spell(person, key, prov, a_date, a_method, d_date, d_method, d_dest):
        counter[0] += 1
        sid = "%s%07d" % (CODE[prov], 2000000 + counter[0] * 7 + int(r.integers(0, 7)))
        open_ = d_date is None or d_date > end_cap
        last = end_cap if open_ else d_date
        span = (last - a_date).days
        k = 1 if span < 2 else int(r.choice([1, 2, 3], p=[0.45, 0.4, 0.15]))
        cuts = sorted(set(int(x) for x in r.integers(1, span, size=k - 1))) if (span >= 2 and k > 1) else []
        bounds = [a_date] + [a_date + dt.timedelta(days=c) for c in cuts] + [last]
        for i in range(len(bounds) - 1):
            final = i == len(bounds) - 2
            rows.append({"person": person, "key": key, "provider": prov, "spell": sid, "admission_date": a_date,
                         "admission_method": a_method, "episode_order": i + 1, "episode_start": bounds[i],
                         "episode_end": None if (final and open_) else bounds[i + 1],
                         "main_specialty": str(r.choice(SPECIALTY)),
                         "discharge_date": (None if open_ else d_date) if final else None,
                         "discharge_method": (None if open_ else d_method) if final else None,
                         "discharge_destination": (None if open_ else d_dest) if final else None})
        return sid

    def trust_of_unit(u):
        return [k for k, v in CODE.items() if u.startswith(v)][0]

    verified = {}
    for person in sorted(persons):
        lst = sorted(persons[person], key=lambda x: (x["dta"], x["rid"]))
        vkey = P.p[person]["key"]
        verified[person] = vkey
        dday, how = death.get(person), where.get(person)
        for ref in lst:
            if ref["pid"] in where:
                dday, how = death.get(ref["pid"]), where[ref["pid"]]
        groups = []
        for ref in lst:
            if groups and day_of(groups[-1][-1]["dta"]) == day_of(ref["dta"]):
                groups[-1].append(ref)
            else:
                groups.append([ref])
        last_out, first_in = None, None
        for gi, grp in enumerate(groups):
            first, ref = grp[0], grp[-1]          # the day's last referral decides the spell
            L = ref["letter"]
            dta_day = day_of(ref["dta"])
            key = temp.get(first["rid"], temp.get(ref["rid"], vkey))
            a_date = dta_day if first["ward"] == "ED" else dta_day - dt.timedelta(days=int(r.integers(0, 10)))
            if last_out is not None and a_date <= last_out:
                a_date = last_out + dt.timedelta(days=1)
            if a_date > dta_day:
                a_date = dta_day
            first_in = first_in or a_date
            a_method = "21" if first["ward"] == "ED" else str(r.choice(ADM_METHOD_WARD))
            is_last = gi == len(groups) - 1
            died_here = is_last and dday is not None and how in ("icu", "ward", "waiting")
            if ref["outcome"] == "admitted" and ref["stay"] is not None:
                st = stays[ref["stay"]]
                icu_out = day_of(st["discharge"])
                transfer = own_unit(L, dta_day) != st["unit"]
                hosp_out = icu_out + dt.timedelta(days=int(r.integers(2, 13)))
                if died_here:
                    hosp_out = dday
                elif is_last and how == "after_discharge":
                    lim = dta_day + dt.timedelta(days=23)
                    hosp_out = max(icu_out + dt.timedelta(days=1), min(hosp_out, lim - dt.timedelta(days=1)))
                    dday = hosp_out + dt.timedelta(days=int(r.integers(1, max(2, (lim - hosp_out).days + 1))))
                elif is_last and how == "readmission":
                    hosp_out = icu_out + dt.timedelta(days=int(r.integers(2, 5)))
                if transfer:
                    moved = day_of(st["admit"])
                    spell(person, key, L, a_date, a_method, moved, "1", "49")
                    spell(person, key, trust_of_unit(st["unit"]), moved, "2B", hosp_out, "4" if died_here else "1",
                          "79" if died_here else "19")
                else:
                    spell(person, key, L, a_date, a_method, hosp_out, "4" if died_here else "1",
                          "79" if died_here else "19")
                last_out = hosp_out
                if is_last and how == "readmission":
                    r_in = hosp_out + dt.timedelta(days=int(r.integers(1, 4)))
                    dday = min(r_in + dt.timedelta(days=int(r.integers(0, 4))), dta_day + dt.timedelta(days=24))
                    spell(person, vkey, L, r_in, "21", dday, "4", "79")
                    last_out = dday
            else:
                if ref["outcome"] == "died":
                    out = day_of(ref["end"])
                    spell(person, key, L, a_date, a_method, out, "4", "79")
                else:
                    out = dta_day + dt.timedelta(days=int(r.integers(1, 15)))
                    if died_here:
                        out = max(dday, dta_day)
                    spell(person, key, L, a_date, a_method, out, "4" if died_here else "1",
                          "79" if died_here else "19")
                last_out = out
        if dday is not None:
            death[person] = dday
            for x in lst:
                death[x["pid"]] = dday
        # a death recorded after the last discharge, sometimes in a later admission
        if dday is not None and last_out is not None and dday > last_out + dt.timedelta(days=3) and how in ("later", "bg"):
            if r.random() < 0.5:
                a = last_out + dt.timedelta(days=int(r.integers(1, (dday - last_out).days)))
                spell(person, vkey, lst[-1]["letter"], a, "21", dday, "4", "79")
                last_out = dday
        # earlier and later admissions for texture
        if r.random() < 0.3 and first_in is not None:
            b = first_in - dt.timedelta(days=int(r.integers(25, 400)))
            a = b - dt.timedelta(days=int(r.integers(1, 9)))
            if a >= dt.date(2022, 4, 1):
                spell(person, vkey, lst[0]["letter"], a, str(r.choice(["21", "22", "11"])), b, "1", "19")
        if r.random() < 0.25 and last_out is not None and dday is None:
            a = last_out + dt.timedelta(days=int(r.integers(20, 300)))
            if a < end_cap - dt.timedelta(days=10):
                b = a + dt.timedelta(days=int(r.integers(1, 9)))
                spell(person, vkey, lst[-1]["letter"], a, str(r.choice(["21", "22", "11"])), b, "1", "19")
    # the date of death is linked to every episode carried under the verified key
    for row in rows:
        dd = death.get(row["person"])
        linked = dd is not None and dd <= LAST_LINKED_DEATH and row["key"] == verified[row["person"]]
        row["date_of_death"] = dd if linked else None
    return rows, verified
