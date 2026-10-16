"""The district as it stands on 8 January 2027: every service line, its records, the material that is really in the
ground, and every field verification and replacement from January 2021 to December 2026.

A street's services were laid when its main went in: lead or galvanized on most of the older streets, copper (later
plastic) on the rest and after 1950. The district's tap cards record that material on the services whose cards
survive, and the 1991-92 lead survey added cards on the streets it found lead or galvanized. A line with no usable
card is a lost original or a service someone else laid, and who laid the services changed with the decades: before
1930 the district laid every service on a lead or galvanized street, in the 1930s and 1940s private plumbers laid
some of them in copper under city permit, and on the few lead or galvanized streets of 1950 to 1988 builders' plumbers
laid about half of them in copper; on a copper street the odd service built before 1950 is galvanized behind a lead
gooseneck, and none after. Each no-card line is an independent draw at the share for its kind of main and its era.
The main renewals (old mains by break history, and renewals coordinated with the lead and galvanized streets) expose
every service on a renewed main; digs for cause (sampling sites, leaks, requests, the 2024 ranking) went to the lead
and galvanized streets far more than to the copper ones, and on the copper streets mostly to the post-1950 ones after
the lead letters; within a street, which lines were verified does not depend on their own material.

Nothing here is written to disk; records.py turns these frames into the files the district's systems export. The
ground truth of unverified lines and every street's class never leave this module."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import common as K

# streets serviced in lead or galvanized (LG) by era of the main, and of those the share laid in lead
STREET_LG = {0: 0.66, 1: 0.46, 2: 0.06}
L_OF_LG = {0: 0.70, 1: 0.40, 2: 0.15}
# a line with no usable card is a lost original or a service someone else laid. On a lead or galvanized street before
# 1930 the district laid every service, so it is nearly always the original; in the 1930s and 1940s private plumbers
# laid some services under city permit in copper; on the few lead or galvanized streets of 1950 to 1988 builders'
# plumbers laid about half of them in copper. On a copper street the odd service built before 1950 is galvanized
# behind a lead gooseneck; none after. The share proving lead or GRR, by kind of main and the era the line was built:
P_HIT = {"LG": (0.994, 0.952, 0.57), "C": (0.0030, 0.0016, 0.0)}
COVER = {"LG": 1.50, "C": 0.85}   # tap card survival, relative, by street class (the 1991-92 survey on LG streets)
RENEW = 0.03               # copper renewal cards among the cards on LG streets
LEAD_OF_HIT = {"L": 0.93, "G": 0.08, "C": 0.5}   # of a no-card line proving lead or GRR, the share that is lead
DIG_RATE = 0.062           # digs for cause on a no-card line away from the renewed mains, 2021 to 2026, by kind and era
DIG_MULT = {("LG", 0): 3.6, ("LG", 1): 2.8, ("LG", 2): 2.5, ("C", 0): 0.3, ("C", 1): 0.25, ("C", 2): 1.8}
# main renewals 2021 to 2026, the chance a main is renewed by its kind and era: old mains by break history, and
# renewals coordinated with the lead and galvanized streets
SWEEP_P = {("LG", 0): 0.245, ("LG", 1): 0.295, ("LG", 2): 0.39, ("C", 0): 0.175, ("C", 1): 0.175, ("C", 2): 0.007}
DISTRICT_CREWS = ["SLV1", "SLV2", "SLV3", "SLV4", "SLV5"]
CONTRACT_CREWS = ["BRN-1", "BRN-2", "TCU-1", "TCU-2", "KPU-1"]
STREETS = [
    "ADAMS", "ALDER", "ARCH", "ASH", "BEECH", "BIRCH", "BRIDGE", "BROAD", "CANAL", "CEDAR", "CHERRY", "CHESTNUT",
    "CHURCH", "CLINTON", "COURT", "CRESCENT", "DEPOT", "DIVISION", "ELM", "EMERSON", "FERRY", "FOUNDRY", "FRANKLIN",
    "FRONT", "GARFIELD", "GRANT", "GROVE", "HARRISON", "HAWTHORNE", "HICKORY", "HIGH", "HOLLINS", "JACKSON",
    "JEFFERSON", "KITTERING", "LAKE", "LAUREL", "LINCOLN", "LINDEN", "LOCUST", "MADISON", "MAIN", "MAPLE", "MARKET",
    "MILL", "MONROE", "MULBERRY", "OAK", "ORCHARD", "PARK", "PEARL", "PINE", "PLEASANT", "POPLAR", "PROSPECT",
    "RAILROAD", "RIDGE", "RIVER", "SCHOOL", "SPRING", "SPRUCE", "STATE", "SUMMIT", "SYCAMORE", "TAYLOR", "UNION",
    "VINE", "WALNUT", "WASHINGTON", "WATER", "WILLOW", "WOODLAND", "BURKHART", "WEXLEY", "SOUTHGATE", "DARROW",
    "MEADOW", "QUARRY", "HARMON", "VALLEY", "FAIRVIEW", "GLENWOOD", "HIGHLAND", "KENWOOD", "LAWNDALE", "NORWOOD",
]
SUFFIXES = ["ST", "AVE", "ST", "ST", "AVE", "RD", "DR", "PL", "CT", "LN"]


def _segments():
    """Main segments per zone: (zone, segment id, era, base year, n lines, street, first house number)."""
    rows = []
    for zi, (zc, name, muni, n_lines, mix, rc) in enumerate(K.ZONES):
        r = K.stream("segments", zc)
        seg_no = 10000 + 6000 * zi       # the GIS numbers mains in blocks by zone
        left = n_lines
        street_pool = list(r.permutation(STREETS))
        k = 0
        while left > 0:
            size = int(r.integers(14, 41))
            if left - size < 14:
                size = left
            era = int(r.choice(4, p=mix))
            lo, hi = {0: (1884, 1929), 1: (1930, 1949), 2: (1950, 1988), 3: (1989, 2024)}[era]
            base = int(r.integers(lo, hi + 1))
            street = street_pool[k % len(street_pool)] + " " + SUFFIXES[int(r.integers(len(SUFFIXES)))]
            block = int(r.integers(1, 40)) * 100
            seg_no += int(r.integers(3, 17))
            rows.append((zc, "WM-%05d" % seg_no, era, base, size, street, block))
            left -= size
            k += 1
    segs = pd.DataFrame(rows, columns=["zone", "segment", "seg_era", "base_year", "n", "street", "block"])
    # the class of material the district laid each street's services in
    cls, sub = [], []
    for s in segs.itertuples():
        r = K.stream("street-class", s.segment)
        if s.seg_era == 3 or r.random() >= STREET_LG[s.seg_era]:
            cls.append("C"); sub.append("C")
        else:
            cls.append("LG"); sub.append("L" if r.random() < L_OF_LG[s.seg_era] else "G")
    segs["sclass"] = cls
    segs["ssub"] = sub
    return segs


def _lines(segs):
    out = []
    base = {z[0]: 1_041_000 + 31_000 * i for i, z in enumerate(K.ZONES)}   # service line ids in blocks by zone
    sl, zone = 0, None
    for seg in segs.itertuples():
        if seg.zone != zone:
            zone, sl = seg.zone, base[seg.zone]
        r = K.stream("lines", seg.segment)
        for i in range(seg.n):
            y = int(seg.base_year + r.integers(-4, 5))
            if seg.seg_era == 3:
                y = max(1989, min(2025, y))
            else:
                y = max(1882, min(1988, y))
            sl += int(r.integers(1, 4))
            house = seg.block + 2 * i + int(r.integers(0, 2))
            out.append((seg.zone, seg.segment, "SL%07d" % sl, y, house, seg.street, seg.sclass, seg.ssub))
    df = pd.DataFrame(out, columns=["zone", "segment", "sl_id", "year_built", "house_no", "street", "sclass", "ssub"])
    df["era"] = df["year_built"].map(K.era_of)
    return df


def _cards(lines):
    """Whether each line's tap card survives, and its material. Every pre-1989 street keeps at least two cards."""
    rc_of = {z[0]: z[5] for z in K.ZONES}
    lines = lines.copy()
    card, mat = [], []
    for ln in lines.itertuples():
        r = K.stream("card", ln.sl_id)
        if ln.era == 3:
            p = 0.85
        else:
            p = min(0.95, rc_of[ln.zone] * (0.8, 1.0, 1.2)[ln.era] * COVER[ln.sclass])
        has = r.random() < p
        card.append(has)
        u = r.random()
        if ln.sclass == "C" or ln.era == 3:
            plastic = (ln.era == 3 and u < 0.30) or (ln.era == 2 and u < 0.10)
            mat.append("PLASTIC" if plastic else "COPPER")
        else:
            mat.append("COPPER" if u < RENEW else ("LEAD" if ln.ssub == "L" else "GALV"))
    lines["card"] = card
    lines["card_mat"] = mat
    pre = lines.era.between(0, 2)
    for sg, idx in lines[pre].groupby("segment").groups.items():
        idx = sorted(idx, key=lambda i: lines.at[i, "sl_id"])
        have = int(lines.loc[idx, "card"].sum())
        if have < 2:
            r = K.stream("min-cards", sg)
            free = [i for i in idx if not lines.at[i, "card"]]
            for i in r.choice(free, size=min(2 - have, len(free)), replace=False):
                lines.at[i, "card"] = True
    for sg, idx in lines[pre & (lines.sclass == "LG")].groupby("segment").groups.items():
        idx = sorted(idx, key=lambda i: lines.at[i, "sl_id"])
        if not any(lines.at[i, "card"] and lines.at[i, "card_mat"] in ("LEAD", "GALV") for i in idx):
            r = K.stream("lg-card", sg)
            i = idx[int(r.integers(len(idx)))]
            lines.at[i, "card"] = True
            lines.at[i, "card_mat"] = "LEAD" if lines.at[i, "ssub"] == "L" else "GALV"
    # the 1991-92 survey carded the lead and galvanized streets more fully: a district renewal card is never as much as
    # a third of a lead or galvanized street's cards
    for sg, idx in lines[pre & (lines.sclass == "LG")].groupby("segment").groups.items():
        idx = sorted(idx, key=lambda i: lines.at[i, "sl_id"])
        r = K.stream("survey-card", sg)
        while True:
            have = [i for i in idx if lines.at[i, "card"]]
            n_cu = sum(1 for i in have if lines.at[i, "card_mat"] == "COPPER")
            free = [i for i in idx if not lines.at[i, "card"]]
            if 3 * n_cu < len(have) or not free:
                break
            i = free[int(r.integers(len(free)))]
            lines.at[i, "card"] = True
            lines.at[i, "card_mat"] = "LEAD" if lines.at[i, "ssub"] == "L" else "GALV"
    lines["record"] = np.where(lines.card, lines.card_mat, "")
    lines["no_record"] = (lines.record == "") & pre
    return lines


def _pick_sweeps(segs, lines):
    """Main renewals 2021 to 2026: the distribution renewal programme took old mains by break history and coordinated
    renewals with the lead and galvanized streets; every service on a renewed main is exposed and verified. One draw
    per main, so a zone's mains are renewed or not on their own."""
    cand = segs[(segs.seg_era < 3) & segs.zone.isin(K.PLAN_ORDER)].sort_values("segment")
    out = []
    for s in cand.itertuples():
        if K.stream("renewal", s.segment).random() < SWEEP_P[(s.sclass, int(s.seg_era))]:
            out.append(str(s.segment))
    return sorted(out)


def _digs(lines):
    """Lines with no usable card dug for cause, away from the replaced mains: the street decides, not the line."""
    dug = []
    for ln in lines.itertuples():
        if not ln.no_record or ln.swept:
            dug.append(False)
            continue
        r = K.stream("dig", ln.sl_id)
        dug.append(bool(r.random() < DIG_RATE * DIG_MULT[(ln.sclass, ln.era)]))
    return np.array(dug)


def _truth(lines):
    """Material in the ground. Carded lines are what their card says; a line with no usable card proves lead or GRR at
    the share for its kind of main and its era, an independent draw for each line."""
    lines = lines.copy()
    truth = np.array(["NON-LEAD"] * len(lines), dtype=object)
    rec = lines.record.to_numpy()
    truth[rec == "LEAD"] = "LEAD"
    truth[rec == "GALV"] = "GRR"
    nr = lines[lines.no_record]
    for i, row in zip(nr.index, nr.itertuples()):
        r = K.stream("truth", row.sl_id)
        if r.random() < P_HIT[row.sclass][row.era]:
            truth[lines.index.get_loc(i)] = "LEAD" if r.random() < LEAD_OF_HIT[row.ssub] else "GRR"
    lines["truth"] = truth
    return lines


SEASON = [(dt.date(y, 4, 1), dt.date(y, 11, 20)) for y in range(2021, 2027)]


def _season_date(r, year=None, lo=K.LOG_START, hi=K.LOG_END):
    """A working day inside a construction season (April to late November), between lo and hi."""
    seasons = [(a, b) for a, b in SEASON if b >= lo and a <= hi and (year is None or a.year == year)]
    a, b = seasons[int(r.integers(len(seasons)))]
    a, b = max(a, lo), min(b, hi)
    d = a + dt.timedelta(days=int(r.integers(0, (b - a).days + 1)))
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return min(d, hi)


def _any_date(r, lo=K.LOG_START, hi=K.LOG_END):
    d = lo + dt.timedelta(days=int(r.integers(0, (hi - lo).days + 1)))
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return min(d, hi)


def _verifications(lines, sweeps):
    """Field verification events. Returns (events, sweep projects). Each event: sl_id, date, cause (never shipped),
    method, crew. A line verified twice gets a pothole, then an excavation."""
    ev = []
    # 1. digs for cause on no-card lines away from the replaced mains
    for row in lines[lines.dug].itertuples():
        r = K.stream("target", row.sl_id)
        cause = str(r.choice(["customer", "leak", "ranked", "sampling"], p=[0.55, 0.20, 0.15, 0.10]))
        if cause == "ranked":
            d = _season_date(r, lo=dt.date(2024, 4, 1), hi=dt.date(2025, 11, 20))
        elif cause == "sampling":
            d = _season_date(r, lo=K.LOG_START, hi=dt.date(2022, 11, 20))
        elif cause == "leak":
            d = _any_date(r)
        else:
            d = _season_date(r)
        ev.append((row.sl_id, d, cause))
        if r.random() < 0.06:
            d2 = d + dt.timedelta(days=int(r.integers(7, 57)))
            if d2 <= K.LOG_END:
                ev.append((row.sl_id, d2, cause + "-confirm"))
    # 2. digs for cause on lines with a tap card (sampling sites on lead cards, leaks on galvanized, requests)
    rk = lines[(lines.record != "") & lines.era.between(0, 2) & ~lines.swept]
    for row in rk.itertuples():
        r = K.stream("target-rec", row.sl_id)
        p = {"LEAD": 0.060, "GALV": 0.035, "COPPER": 0.006, "PLASTIC": 0.004}[row.record]
        if r.random() < p:
            cause = {"LEAD": "sampling", "GALV": "leak"}.get(row.record, "customer")
            d = _season_date(r, hi=dt.date(2022, 11, 20)) if cause == "sampling" else _any_date(r)
            ev.append((row.sl_id, d, cause))
    # 3. requests in the newer subdivisions (built 1989 on), never before the house was built
    nw = lines[lines.era == 3]
    for row in nw.itertuples():
        r = K.stream("target-new", row.sl_id)
        if r.random() < 0.0075:
            lo = max(K.LOG_START, dt.date(row.year_built + 1, 4, 1))
            if lo <= K.LOG_END:
                ev.append((row.sl_id, _season_date(r, lo=lo), "customer"))
    # 4. water main replacement projects: every service on the segment, inside the project window
    r = K.stream("projects")
    order = list(r.permutation(sorted(sweeps)))
    projects = []
    i = 0
    pno = 0
    by_seg = {sg: t for sg, t in lines[lines.segment.isin(sweeps)].groupby("segment")}
    while i < len(order):
        k = int(r.integers(2, 5))
        group = order[i:i + k]
        i += k
        pno += 1
        year = int(r.choice([2021, 2022, 2023, 2024, 2025, 2026], p=[0.15, 0.16, 0.17, 0.18, 0.18, 0.16]))
        lo = dt.date(year, 4, 6)
        start = _season_date(r, year=year, lo=lo, hi=dt.date(year, 9, 25))
        weeks = int(r.integers(3, 9))
        end = min(start + dt.timedelta(days=7 * weeks), dt.date(year, 11, 20))
        projects.append((pno, year, start, end, tuple(group)))
        for seg in group:
            for row in by_seg[seg].itertuples():
                rr = K.stream("sweep-day", row.sl_id)
                d = start + dt.timedelta(days=int(rr.integers(0, (end - start).days + 1)))
                while d.weekday() >= 5:
                    d += dt.timedelta(days=1)
                ev.append((row.sl_id, min(d, end), "main"))
    evdf = pd.DataFrame(ev, columns=["sl_id", "date", "cause"]).sort_values(["date", "sl_id"]).reset_index(drop=True)
    meth, crew = [], []
    for row in evdf.itertuples():
        r = K.stream("method", row.sl_id, row.date.isoformat(), row.cause)
        if row.cause.endswith("-confirm"):
            meth.append("EXCAVATION")
        elif row.cause == "main":
            meth.append(str(r.choice(["EXCAVATION", "POTHOLE", "CURB BOX CAMERA"], p=[0.52, 0.36, 0.12])))
        else:
            meth.append(str(r.choice(["EXCAVATION", "POTHOLE", "CURB BOX CAMERA", "METER PIT VISUAL"],
                                     p=[0.47, 0.37, 0.12, 0.04])))
        pool = DISTRICT_CREWS + CONTRACT_CREWS
        w = np.array([0.13] * 5 + [0.07] * 5) if row.cause == "main" else np.array([0.11] * 5 + [0.09] * 5)
        crew.append(str(r.choice(pool, p=w / w.sum())))
    evdf["method"] = meth
    evdf["crew"] = crew
    return evdf, projects


def _replacements(lines, ev):
    """Replace-on-find: a lead or GRR line found is replaced inside the main project, or months after a dig for
    cause. Lines found late in 2026 wait for the plan."""
    first = ev.sort_values("date").groupby("sl_id").first()
    rep = {}
    for sl, row in first.iterrows():
        tr = lines.at[sl, "truth"]
        if tr == "NON-LEAD":
            continue
        r = K.stream("replace", sl)
        if row.cause == "main":
            d = row.date + dt.timedelta(days=int(r.integers(0, 21)))
        else:
            d = row.date + dt.timedelta(days=int(r.integers(20, 261)))
        while d.weekday() >= 5:
            d += dt.timedelta(days=1)
        if d <= K.LOG_END:
            rep[sl] = d
    return rep


def _never_built(lines):
    """Lots platted with a tap but never built on, or merged into a neighbour, leave no service line: a few dozen
    in each zone on records-known or new-build lines nobody has dug, and in the plan zones a few lots on the copper
    streets of 1950 to 1988 (K.NEVER_BUILT_C2)."""
    out = []
    for z in [x[0] for x in K.ZONES]:
        r = K.stream("never-built", z)
        t = lines[(lines.zone == z) & (lines.cls == "NON-LEAD") & lines.basis.isin(["RECORDS", "CONSTRUCTION DATE"]) &
                  lines.verified.isna() & ~lines.swept]
        out.extend(r.choice(sorted(t.sl_id), size=int(r.integers(13, 78)), replace=False))
        if z not in K.PLAN_ORDER:
            g = lines[(lines.zone == z) & (lines.cls == "GRR") & (lines.basis == "RECORDS") & lines.verified.isna()]
            if len(g):
                out.extend(r.choice(sorted(g.sl_id), size=min(len(g), int(r.integers(1, 4))), replace=False))
        k = K.NEVER_BUILT_C2.get(z, 0)
        if k:
            c2 = lines[(lines.zone == z) & (lines.cls == "LEAD STATUS UNKNOWN") & (lines.sclass == "C") &
                       (lines.era == 2)]
            out.extend(K.stream("never-built-c2", z).choice(sorted(c2.sl_id), size=k, replace=False))
    return lines[~lines.sl_id.isin(set(out))].reset_index(drop=True)


def _premises(lines):
    """The customer system's premise number for every line in service at the March 2023 migration (in sl_id order),
    six or seven digits; lines built since have none."""
    r = K.stream("premises")
    exist = (lines.year_built <= 2022).to_numpy()
    nums = r.choice(np.arange(104_000, 2_990_000), size=int(exist.sum()), replace=False)
    out = np.full(len(lines), np.nan)
    out[exist] = nums
    return out


def addresses(segs, lines):
    """Street address of each line: a segment's block moves up the street when another segment in the same
    municipality already holds it, so no address repeats."""
    muni = {z[0]: z[2] for z in K.ZONES}
    used, block = set(), {}
    for s in segs.sort_values("segment").itertuples():
        b = s.block
        while (muni[s.zone], s.street, b) in used:
            b = b + 100 if b < 7900 else 100
        used.add((muni[s.zone], s.street, b))
        block[s.segment] = (b, s.block)
    out = []
    for ln in lines.itertuples():
        b, b0 = block[ln.segment]
        out.append("%d %s" % (b + (ln.house_no - b0), ln.street))
    return pd.Series(out, index=lines.index)


def lead_cards(lines):
    """On a few lead or galvanized streets per zone, a card read as a copper renewal is the street's original material
    after all (K.LEAD_CARDS_ADDED), so each zone's expected replacements and cost sit clear of their rounding edges.
    Only lines no crew has dug and nobody has replaced: nothing else reads them before the plan."""
    lines = lines.copy()
    for z, k in sorted(K.LEAD_CARDS_ADDED.items()):
        if not k:
            continue
        pool = sorted(lines[(lines.zone == z) & (lines.record == "COPPER") & (lines.sclass == "LG") &
                            lines.era.between(0, 2) & ~lines.swept & lines.verified.isna() &
                            lines.replaced.isna()].sl_id)
        r = K.stream("lead-cards", z)
        for sl in r.choice(pool, size=k, replace=False):
            i = lines.index[lines.sl_id == sl][0]
            mat = "LEAD" if lines.at[i, "ssub"] == "L" else "GALV"
            lines.at[i, "record"] = mat
            lines.at[i, "card_mat"] = mat
            lines.at[i, "truth"] = "LEAD" if mat == "LEAD" else "GRR"
            lines.at[i, "cls"] = "LEAD" if mat == "LEAD" else "GRR"
            lines.at[i, "basis"] = "RECORDS"
    return lines


def classify(lines):
    cls, basis = [], []
    for row in lines.itertuples():
        if row.era == 3:
            cls.append("NON-LEAD"); basis.append("CONSTRUCTION DATE")
        elif isinstance(row.replaced, dt.date):
            cls.append("NON-LEAD"); basis.append("REPLACED")
        elif isinstance(row.verified, dt.date):
            cls.append(row.truth); basis.append("FIELD VERIFIED")
        elif row.record == "LEAD":
            cls.append("LEAD"); basis.append("RECORDS")
        elif row.record == "GALV":
            cls.append("GRR"); basis.append("RECORDS")
        elif row.record in ("COPPER", "PLASTIC"):
            cls.append("NON-LEAD"); basis.append("RECORDS")
        else:
            cls.append("LEAD STATUS UNKNOWN"); basis.append("")
    lines = lines.copy()
    lines["cls"] = cls
    lines["basis"] = basis
    return lines


def build():
    segs = _segments()
    lines = _lines(segs)
    lines = _cards(lines)
    sweeps = _pick_sweeps(segs, lines)
    lines["swept"] = lines.segment.isin(sweeps)
    lines["dug"] = _digs(lines)
    lines = _truth(lines)
    ev, projects = _verifications(lines, sweeps)
    lines = lines.set_index("sl_id", drop=False)
    rep = _replacements(lines, ev)
    first = ev.sort_values("date").groupby("sl_id").date.first()
    lines["verified"] = lines.sl_id.map(first)
    lines["replaced"] = lines.sl_id.map(rep)
    lines = classify(lines.reset_index(drop=True))
    lines = _never_built(lines)
    lines["legacy_premise"] = _premises(lines)
    lines["address"] = addresses(segs, lines)
    return segs, lines, sweeps, ev, projects


if __name__ == "__main__":
    segs, lines, sweeps, ev, projects = build()
    print(len(ev), "events", ev.cause.value_counts().to_dict())
    print(lines.cls.value_counts().to_dict())
    print(len(segs), "segments", len(lines), "lines")
