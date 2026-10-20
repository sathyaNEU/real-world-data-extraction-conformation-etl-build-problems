"""The asks' world: the plan's expansion members on 1 October 2026 and their households.

The plan's enrollment system exports its active roster on 19 October (each member's current county, birth date and
the start of the member's current enrollment), and its enrollment change log for 1 to 19 October (adds, terminations
with the last covered day, reinstatements and address changes, each line with the member's birth date and county). The state's household composition extract of
15 October lists each case's members, their roles and birth dates, and the case's children under 14 on the extract
date. The truth is each member's coverage, age and county on 1 October and the case's members on that day."""
import csv
import datetime as dt

import numpy as np

import common as K

D1 = K.ROSTER_DATE                       # 1 October 2026
EXTRACT = dt.date(2026, 10, 15)          # the household extract
ROSTER_AT = dt.date(2026, 10, 19)        # the active roster export
SIZE = {"GRV": 4287, "GCO": 8734, "KNG": 21362, "NCE": 3318, "NSD": 11566, "PRC": 12839, "SAL": 4121, "SWR": 7874,
        "SPK": 9931, "TMA": 4618}
NEIGHBOUR = {"GRV": ["SWR", "TMA", "SAL"], "GCO": ["SPK", "NCE"], "KNG": ["PRC", "NSD", "SAL"],
             "NCE": ["GCO", "SPK", "NSD"], "NSD": ["KNG", "SAL"], "PRC": ["KNG", "TMA", "SAL"],
             "SAL": ["KNG", "PRC", "TMA"], "SWR": ["GRV"], "SPK": ["GCO", "NCE"], "TMA": ["PRC", "GRV", "SAL"]}
COUNTY_WEIGHTS = {
    "GRV": [2.6, 1.6, 1.8, 0.5, 0.1], "GCO": [0.6, 3.0, 0.2, 1.6, 0.1, 0.8, 1.0, 0.7, 4.5], "KNG": [1.0],
    "NCE": [1.6, 0.8, 2.2, 1.0], "NSD": [1.0, 0.3, 1.6, 5.5, 2.4], "PRC": [1.0], "SAL": [1.4, 0.6, 3.0],
    "SWR": [7.0, 0.5, 0.3], "SPK": [0.4, 0.2, 0.3, 0.3, 6.0, 0.8], "TMA": [1.0, 3.2]}
REGION_OF = {cty: code for code, _, cs in K.REGIONS for cty in cs}
PARENT_ROLES = ("HOH", "SPOUSE", "CARETAKER_RELATIVE")


def age_on(born, on):
    return on.year - born.year - ((on.month, on.day) < (born.month, born.day))


def _birth(r, lo_age, hi_age, on=D1):
    """A birth date giving an age between lo_age and hi_age on `on`."""
    start = dt.date(on.year - hi_age - 1, on.month, on.day) + dt.timedelta(days=1)
    end = dt.date(on.year - lo_age, on.month, on.day)
    return start + dt.timedelta(days=int(r.integers(0, (end - start).days + 1)))


def _county(r, code):
    w = np.array(COUNTY_WEIGHTS[code])
    return K.COUNTIES[code][int(r.choice(len(w), p=w / w.sum()))]


def build(seed):
    r = np.random.default_rng(seed + 61)
    mid_pool = r.choice(np.arange(200_000_000, 999_999_999), size=140_000, replace=False)
    p1_pool = r.choice(np.arange(100_000_000, 299_999_999), size=140_000, replace=False)
    nxt = [0]

    def person(code, kind, begin=None, end=None):
        i = nxt[0]
        nxt[0] += 1
        if begin is None:
            begin = dt.date(int(r.choice([2022, 2023, 2024, 2025, 2026], p=[.18, .22, .24, .22, .14])),
                            int(r.integers(1, 13)), 1)
            begin = min(begin, dt.date(2026, 9, 1))
        return dict(member_id="P%09d" % mid_pool[i], p1="%09dWA" % p1_pool[i], born=_birth(r, 19, 64),
                    sex="F" if r.random() < 0.53 else "M", county1=_county(r, code), region1=code, begin=begin,
                    end=end, kind=kind)

    members = [person(code, "covered") for code in K.CODES for _ in range(SIZE[code])]
    n = len(members)
    # left after 1 October: covered that day, last covered day 1 to 18 October, not on the 19 October roster
    for j in r.choice(n, size=int(0.0075 * n), replace=False):
        members[j]["end"] = D1 + dt.timedelta(days=int(r.integers(0, 18)))
        members[j]["kind"] = "left"
    stay = np.array([j for j in range(n) if members[j]["kind"] == "covered"])
    for j in r.choice(stay, size=int(0.003 * n), replace=False):
        # covered on 1 October, terminated in October, enrolled again before the roster export after a gap
        end = D1 + dt.timedelta(days=int(r.integers(1, 12)))
        members[j]["end"] = end
        members[j]["rebegin"] = end + dt.timedelta(days=int(r.integers(4, 19 - (end - D1).days)))
        members[j]["kind"] = "churn"
    stay = np.array([j for j in range(n) if members[j]["kind"] == "covered"])
    pick = r.permutation(stay)
    cut = np.cumsum([int(0.0035 * n), int(0.004 * n), int(0.0006 * n), int(0.0006 * n), int(0.0006 * n)])
    moved, sched, rein, over65, turns65 = np.split(pick[:cut[-1]], cut[:-1])
    for j in moved:                     # moved to another region after 1 October
        to = NEIGHBOUR[members[j]["region1"]][int(r.integers(0, len(NEIGHBOUR[members[j]["region1"]])))]
        members[j]["county_now"] = _county(r, to)
        members[j]["moved_on"] = D1 + dt.timedelta(days=int(r.integers(1, 18)))
    for j in sched:                     # a termination keyed for 31 October: covered and still on the roster
        members[j]["end"] = dt.date(2026, 10, 31)
    for j in rein:                      # terminated in error on 6 October, reinstated on 8 October
        members[j]["reinstated"] = True
    for j in over65:                    # 65 on or before 1 October, coverage still open
        members[j]["born"] = dt.date(1961, 10, 1) - dt.timedelta(days=int(r.integers(0, 150)))
    for j in turns65:                   # 65 between 2 and 19 October: 64 on 1 October
        members[j]["born"] = dt.date(1961, 10, 2) + dt.timedelta(days=int(r.integers(0, 18)))
    retro = [person(code, "retro", begin=dt.date(2025, int(r.integers(1, 13)), 1),
                    end=dt.date(2026, 9, int(r.choice([30, 30, 30, 15]))))
             for code in K.CODES for _ in range(int(SIZE[code] * 0.004))]
    joined = [person(code, "joined", begin=D1 + dt.timedelta(days=int(r.integers(1, 19))))
              for code in K.CODES for _ in range(int(SIZE[code] * 0.005))]
    return dict(members=members, retro=retro, joined=joined)


def households(A, seed):
    """Each member's case. A parent (case head or spouse) with children, a caretaker relative of a child, an adult in a
    relative's case with children who is not their carer, or an adult alone. Some adults have two segment rows in
    their case after a role change. Children carry birth dates and their days in the case."""
    r = np.random.default_rng(seed + 71)
    case_no = iter(r.choice(np.arange(10_000_000, 99_999_999), size=200_000, replace=False))
    kid_no = iter(r.choice(np.arange(300_000_000, 399_999_999), size=200_000, replace=False))
    cases = []
    for m in A["members"] + A["retro"] + A["joined"]:
        u = r.random()
        kids = []
        if u < 0.24:
            role = "HOH" if r.random() < 0.8 else "SPOUSE"
            for _ in range(int(r.choice([1, 2, 3], p=[.52, .33, .15]))):
                kids.append(_birth(r, 0, 17, on=EXTRACT))
        elif u < 0.27:
            role = "CARETAKER_RELATIVE"
            kids.append(_birth(r, 0, 15, on=EXTRACT))
        elif u < 0.31:
            role = "OTHER_ADULT"
            kids.append(_birth(r, 0, 15, on=EXTRACT))
        else:
            role = "HOH"
        kid_rows = []
        for b in kids:
            begin = max(dt.date(b.year, b.month, 1), dt.date(2018, 1, 1))
            kid_rows.append(dict(p1="%09dWA" % next(kid_no), born=b, begin=begin, end=None))
        m["case"], m["role"], m["kids"] = "C%08d" % next(case_no), role, kid_rows
        cases.append(m)
    parents = [m for m in cases if m["role"] in PARENT_ROLES and m["kids"] and m["kind"] in ("covered", "left")]
    pick = r.permutation(len(parents))[: int(0.024 * len(parents))]
    half = len(pick) // 2
    for ix in pick[:half]:             # the only child under 14 turns 14 between 2 and 15 October
        m = parents[ix]
        m["kids"] = [dict(p1=m["kids"][0]["p1"], born=dt.date(2012, 10, 2) + dt.timedelta(days=int(r.integers(0, 14))),
                          begin=dt.date(2018, 1, 1), end=None)]
    for ix in pick[half:]:             # the only child joined the case after 1 October (a birth, or a move in)
        m = parents[ix]
        if r.random() < 0.5:
            b = D1 + dt.timedelta(days=int(r.integers(1, 14)))
            m["kids"] = [dict(p1=m["kids"][0]["p1"], born=b, begin=b, end=None)]
        else:
            b = _birth(r, 2, 12, on=EXTRACT)
            m["kids"] = [dict(p1=m["kids"][0]["p1"], born=b, begin=D1 + dt.timedelta(days=int(r.integers(1, 14))),
                              end=None)]
    seg = r.permutation(len(parents))[: int(0.03 * len(parents))]
    for ix in seg:                     # a role change: spouse to case head, two segment rows
        parents[ix]["role_change"] = dt.date(2026, int(r.integers(1, 10)), 1)
    return cases


def coverage_on(m, day):
    if m["kind"] in ("retro",):
        return False
    if m["begin"] > day:
        return False
    return m["end"] is None or m["end"] >= day


def truth(A, H=None):
    """Ask A: members covered on 1 October, aged 19 to 64 that day, by the region of their county that day. Ask B: of
    them, case heads, spouses and caretaker relatives with a child under 14 in the case on 1 October."""
    a = {c: 0 for c in K.CODES}
    b = {c: 0 for c in K.CODES}
    for m in A["members"] + A["retro"] + A["joined"]:
        if not coverage_on(m, D1) or not (19 <= age_on(m["born"], D1) <= 64):
            continue
        code = REGION_OF[m["county1"]]
        a[code] += 1
        if H is not None and m.get("role") in PARENT_ROLES:
            if any(age_on(k["born"], D1) < 14 and k["born"] <= D1 and k["begin"] <= D1 and
                   (k["end"] is None or k["end"] >= D1) for k in m["kids"]):
                b[code] += 1
    return a, b


def _us(d):
    return "%02d/%02d/%04d" % (d.month, d.day, d.year)


def write_roster(path, A):
    """The plan's active expansion roster as exported on 19 October."""
    rows = []
    for m in A["members"] + A["joined"]:
        if m["kind"] == "left":
            continue
        county = m.get("county_now") if m.get("moved_on") and m["moved_on"] <= ROSTER_AT else m["county1"]
        if m["kind"] == "churn":
            begin, end = m["rebegin"], None
        else:
            begin, end = m["begin"], m["end"]
        rows.append((m["member_id"], m["p1"], _us(m["born"]), m["sex"], county, REGION_OF[county], "N05",
                     begin.isoformat(), "" if end is None else end.isoformat()))
    rows.sort()
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\r\n")
        wr.writerow(["member_id", "p1_client_id", "birth_date", "sex", "county", "region", "coverage_group",
                     "enrollment_begin", "scheduled_end"])
        wr.writerows(rows)
    return len(rows)


def write_changes(path, A, seed):
    """The enrollment change log, 1 to 19 October, one line per change the system applied."""
    r = np.random.default_rng(seed + 83)
    ev = []
    days = [D1 + dt.timedelta(days=i) for i in range(19)]

    def stamp(day):
        return dt.datetime.combine(day, dt.time(int(r.integers(5, 7)), int(r.integers(0, 60)), int(r.integers(0, 60))))

    for m in A["members"]:
        if m["kind"] in ("left", "churn"):
            keyed = max(D1, m["end"] - dt.timedelta(days=int(r.integers(0, 10))))
            ev.append((stamp(keyed), m, "TERM", m["end"], m["county1"], ""))
        if m["kind"] == "churn":
            ev.append((stamp(m["rebegin"]), m, "ADD", m["rebegin"], "", m["county1"]))
        if m.get("moved_on"):
            ev.append((stamp(m["moved_on"]), m, "ADDRESS", m["moved_on"], m["county1"], m["county_now"]))
        if m["end"] == dt.date(2026, 10, 31):
            ev.append((stamp(days[int(r.integers(0, 19))]), m, "TERM", m["end"], m["county1"], ""))
        if m.get("reinstated"):
            ev.append((stamp(dt.date(2026, 10, 6)), m, "TERM", dt.date(2026, 9, 30), m["county1"], ""))
            ev.append((stamp(dt.date(2026, 10, 8)), m, "REINSTATE", m["begin"], "", m["county1"]))
    for m in A["retro"]:
        ev.append((stamp(days[int(r.integers(0, 19))]), m, "TERM", m["end"], m["county1"], ""))
    for m in A["joined"]:
        ev.append((stamp(min(m["begin"], days[int(r.integers(0, 19))])), m, "ADD", m["begin"], "", m["county1"]))
    ev.sort(key=lambda e: (e[0], e[1]["member_id"], e[2]))
    with open(path, "w", newline="", encoding="utf-8") as f:
        f.write("logged_at|member_id|p1_client_id|birth_date|change|effective_date|county_before|county_after\n")
        for when, m, kind, eff, before, after in ev:
            f.write("|".join([when.strftime("%Y-%m-%d %H:%M:%S"), m["member_id"], m["p1"], m["born"].strftime("%Y%m%d"),
                              kind, eff.strftime("%Y%m%d"), before, after]) + "\n")
    return len(ev)


def write_households(path, cases):
    """The state's household composition extract of 15 October for cases with a plan expansion member."""
    rows = []
    for m in cases:
        kids = [k for k in m["kids"] if k["begin"] <= EXTRACT]
        n14 = sum(1 for k in kids if age_on(k["born"], EXTRACT) < 14 and (k["end"] is None or k["end"] >= EXTRACT))
        if m.get("role_change"):
            rows.append((m["case"], m["p1"], "SPOUSE", _us(m["born"]), "2020-01-01",
                         (m["role_change"] - dt.timedelta(days=1)).isoformat(), n14))
            rows.append((m["case"], m["p1"], "HOH", _us(m["born"]), m["role_change"].isoformat(), "", n14))
        else:
            rows.append((m["case"], m["p1"], m["role"], _us(m["born"]), "2020-01-01", "", n14))
        for k in kids:
            rows.append((m["case"], k["p1"], "CHILD", _us(k["born"]), k["begin"].isoformat(),
                         "" if k["end"] is None else k["end"].isoformat(), n14))
    rows.sort()
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\n")
        wr.writerow(["case_id", "p1_client_id", "case_role", "birth_date", "member_begin", "member_end",
                     "children_under_14_in_case"])
        wr.writerows(rows)
    return len(rows)


def link_sample(w, A, seed):
    """The survey's sampled members are the plan's: each sampled case takes the member ID of an enrolled member of its
    region, sex and age on 1 March 2026 whose enrollment began by then, so most sampled members are found again in the
    October files; the rest (about one in seven) had left the plan before October and keep an ID no October file
    holds."""
    r = np.random.default_rng(seed + 91)
    frame = K.FRAME_DATE
    pool = {}
    for m in A["members"] + A["retro"]:
        if m["begin"] > frame:
            continue
        a = age_on(m["born"], frame)
        if 19 <= a <= 64:
            pool.setdefault((REGION_OF[m["county1"]], m["sex"], a), []).append(m["member_id"])
    for key in pool:
        pool[key] = list(r.permutation(pool[key]))
    taken = {m["member_id"] for m in A["members"] + A["retro"] + A["joined"]}
    det = w["det"]
    linked = 0
    for c in w["cases"]:
        cid = int(c[0])
        key = (K.CODES[int(c[1])], "F" if int(c[3]) == 0 else "M", int(det["age"][cid]))
        if r.random() < 0.86 and pool.get(key):
            det["member"][cid] = pool[key].pop()
            linked += 1
        elif det["member"][cid] in taken:
            raise RuntimeError("an unlinked sampled member's ID belongs to an October member: case %d" % cid)
    assert len(set(det["member"])) == len(det["member"])
    return linked
