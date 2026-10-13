"""The district as it stands on 8 January 2027: every service line, its records, the material that is really in the
ground, and every field verification and replacement from January 2021 to December 2026.

Nothing here is written to disk; records.py turns these frames into the files the district's systems export.
The ground truth of unverified lines never leaves this module."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

import common as K

# population shares of lead or GRR among lines with no usable record, by era
P_LGRR = (14 / 25, 8 / 25, 2 / 25)
# on the swept segments the share is exact in every construction decade: 5 in 9, 6 in 19, 1 in 12
SWEPT_DEN = (9, 19, 12)
SWEPT_HIT = (5, 6, 1)
P_SWEPT = tuple(h / d for h, d in zip(SWEPT_HIT, SWEPT_DEN))
LEAD_OF_LGRR = (0.84, 0.52, 0.12)                    # of the lead or GRR lines, the share whose service is lead
SELECTION_RATIO = 4.2                                # odds a lead or GRR line is dug for cause, against a non-lead one
RECORD_MIX = {                                       # tap card material by era, among lines with a usable card
    0: (("LEAD", 0.55), ("GALV", 0.25), ("COPPER", 0.20)),
    1: (("LEAD", 0.25), ("GALV", 0.35), ("COPPER", 0.40)),
    2: (("LEAD", 0.02), ("GALV", 0.10), ("COPPER", 0.80), ("PLASTIC", 0.08)),
    3: (("COPPER", 0.70), ("PLASTIC", 0.30)),
}
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
    seg_no = 10000
    for zc, name, muni, n_lines, mix, rc in K.ZONES:
        r = K.stream("segments", zc)
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
    return pd.DataFrame(rows, columns=["zone", "segment", "seg_era", "base_year", "n", "street", "block"])


def _lines(segs):
    out = []
    sl = 1_041_000
    for seg in segs.itertuples():
        r = K.stream("lines", seg.segment)
        for i in range(seg.n):
            y = int(seg.base_year + r.integers(-4, 5))
            if seg.seg_era == 3:
                y = max(1989, min(2025, y))
            else:
                y = max(1882, min(1988, y))
            sl += int(r.integers(1, 4))
            house = seg.block + 2 * i + int(r.integers(0, 2))
            out.append((seg.zone, seg.segment, "SL%07d" % sl, y, house, seg.street))
    df = pd.DataFrame(out, columns=["zone", "segment", "sl_id", "year_built", "house_no", "street"])
    df["era"] = df["year_built"].map(K.era_of)
    return df


def _records(lines):
    """Tap card material for each line, blank where no usable card survives."""
    rc_of = {z[0]: z[5] for z in K.ZONES}
    rec = []
    for row in lines.itertuples():
        r = K.stream("record", row.sl_id)
        e = row.era
        if e == 3:
            p_rec = 0.85
        else:
            p_rec = min(0.95, rc_of[row.zone] * (0.8, 1.0, 1.2)[e])
        if r.random() < p_rec:
            mats, ps = zip(*RECORD_MIX[e])
            rec.append(str(r.choice(mats, p=np.array(ps) / sum(ps))))
        else:
            rec.append("")
    lines = lines.copy()
    lines["record"] = rec
    return lines


def _pick_sweeps(segs, lines):
    """Main replacement projects 2023 to 2026: segments whose every service was exposed and verified. Old cast iron
    mains are replaced first, so the projects lean to the oldest segments; every construction decade from the 1880s
    to the 1980s carries at least 30 no-record lines on a replaced main."""
    r = K.stream("sweeps")
    cand = segs[(segs.seg_era < 3) & segs.zone.isin(K.PLAN_ORDER)].copy()
    cand = cand.sort_values("segment").reset_index(drop=True)
    nr = lines[lines.no_record]
    nr_dec = nr.assign(dec=(nr.year_built // 10) * 10).groupby(["segment", "dec"]).size()
    seg_dec = {}
    for (seg, d), n in nr_dec.items():
        seg_dec.setdefault(seg, {})[d] = n
    chosen = []

    def counts():
        c = {}
        for seg in chosen:
            for d, n in seg_dec.get(seg, {}).items():
                c[d] = c.get(d, 0) + n
        return c

    for d in range(1880, 1990, 10):
        tries = 0
        while counts().get(d, 0) < 30:
            pool = [sg for sg in cand.segment if sg not in chosen and seg_dec.get(sg, {}).get(d, 0) >= 6]
            chosen.append(str(r.choice(sorted(pool))))
            tries += 1
            assert tries < 40
    w = cand.seg_era.map({0: 5.0, 1: 1.8, 2: 0.7}).to_numpy()
    w = w / w.sum()
    while len(chosen) < 78:
        sg = str(r.choice(cand.segment.to_numpy(), p=w))
        if sg not in chosen:
            chosen.append(sg)
    return chosen


def _trim_sweep_sample(lines):
    """On swept segments, give a tap card to just enough no-record lines that each decade's no-record count is a
    multiple of its era's denominator, so the swept share is exactly the era's share in every decade."""
    lines = lines.copy()
    sw = lines[lines.swept & lines.no_record]
    dec = (sw.year_built // 10) * 10
    for d, idx in sw.groupby(dec).groups.items():
        idx = sorted(idx, key=lambda i: lines.at[i, "sl_id"])
        den = SWEPT_DEN[K.era_of(int(d))]
        excess = len(idx) % den
        if len(idx) - excess < 2 * den:
            raise AssertionError("decade %d has %d swept no-record lines" % (d, len(idx)))
        r = K.stream("trim", d)
        drop = list(r.choice(idx, size=excess, replace=False)) if excess else []
        for i in drop:
            e = int(lines.at[i, "era"])
            mats, ps = zip(*RECORD_MIX[e])
            lines.at[i, "record"] = str(r.choice(mats, p=np.array(ps) / sum(ps)))
            lines.at[i, "no_record"] = False
    return lines


def _truth(lines):
    """Material in the ground: LEAD, GRR or NON-LEAD. Exact era shares on the swept no-record lines, decade by
    decade; independent draws everywhere else; records-known lines are what their card says."""
    lines = lines.copy()
    truth = np.array(["NON-LEAD"] * len(lines), dtype=object)
    rec = lines.record.to_numpy()
    truth[rec == "LEAD"] = "LEAD"
    truth[rec == "GALV"] = "GRR"
    # swept no-record lines: exact counts per decade
    sw = lines[lines.swept & lines.no_record]
    dec = (sw.year_built // 10) * 10
    for d, idx in sw.groupby(dec).groups.items():
        idx = sorted(idx, key=lambda i: lines.at[i, "sl_id"])
        e = int(lines.at[idx[0], "era"])
        den, per_block = SWEPT_DEN[e], SWEPT_HIT[e]
        assert len(idx) % den == 0
        k = len(idx) // den * per_block
        r = K.stream("truth-swept", d)
        # spread the hits evenly over the decade's years (blocks of den lines in year order, the era's share in each
        # block), so no year inside an era carries a share of its own
        order = sorted(idx, key=lambda i: (lines.at[i, "year_built"], lines.at[i, "sl_id"]))
        hit = []
        for b in range(0, len(order), den):
            block = order[b:b + den]
            hit.extend(r.choice(block, size=per_block, replace=False))
        assert len(hit) == k
        for i in hit:
            truth[lines.index.get_loc(i)] = "LEAD" if r.random() < LEAD_OF_LGRR[e] else "GRR"
    # every other no-record line
    other = lines[lines.no_record & ~lines.swept]
    for i, row in zip(other.index, other.itertuples()):
        r = K.stream("truth", row.sl_id)
        if r.random() < P_LGRR[row.era]:
            truth[lines.index.get_loc(i)] = "LEAD" if r.random() < LEAD_OF_LGRR[row.era] else "GRR"
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


TARGET_BASE = 0.0455
ERA_TARGET = (1.30, 1.00, 0.75)


def _verifications(lines, sweeps):
    """Field verification events. Returns (events, sweep projects). Each event: sl_id, date, cause (never shipped),
    method, crew. A line verified twice gets a pothole, then an excavation."""
    ev = []
    # 1. digs for cause on no-record lines away from the swept segments
    cand = lines[lines.no_record & ~lines.swept]
    for row in cand.itertuples():
        r = K.stream("target", row.sl_id)
        hit = row.truth != "NON-LEAD"
        p = TARGET_BASE * ERA_TARGET[row.era] * (SELECTION_RATIO if hit else 1.0)
        if r.random() >= p:
            continue
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
    while i < len(order):
        k = int(r.integers(2, 5))
        group = order[i:i + k]
        i += k
        pno += 1
        year = int(r.choice([2023, 2024, 2025, 2026], p=[0.22, 0.26, 0.26, 0.26]))
        lo = dt.date(year, 5, 1) if year == 2023 else dt.date(year, 4, 6)
        start = _season_date(r, year=year, lo=lo, hi=dt.date(year, 9, 25))
        weeks = int(r.integers(3, 9))
        end = min(start + dt.timedelta(days=7 * weeks), dt.date(year, 11, 20))
        projects.append((pno, year, start, end, tuple(group)))
        for seg in group:
            segl = lines[lines.segment == seg]
            for row in segl.itertuples():
                rr = K.stream("sweep-day", row.sl_id)
                d = start + dt.timedelta(days=int(rr.integers(0, (end - start).days + 1)))
                while d.weekday() >= 5:
                    d += dt.timedelta(days=1)
                ev.append((row.sl_id, min(d, end), "main"))
    evdf = pd.DataFrame(ev, columns=["sl_id", "date", "cause"]).sort_values(["date", "sl_id"]).reset_index(drop=True)
    # methods and crews: drawn from overlapping mixes so neither separates a main project from a dig for cause
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


# the 2026 records search as it was run: its picks were drawn against the 2026 engineer's prices and mobilisation
SEARCH_PRICES = {
    "RZ-07": (11_400, 2_420), "RZ-02": (13_800, 2_540), "RZ-11": (12_400, 2_540), "RZ-04": (12_500, 2_540),
    "RZ-09": (12_400, 2_420), "RZ-01": (12_400, 2_390), "RZ-05": (12_400, 2_390), "RZ-12": (12_400, 2_390),
    "RZ-03": (12_400, 2_390), "RZ-08": (12_400, 2_420), "RZ-10": (12_400, 2_390), "RZ-06": (12_400, 2_420),
}
SEARCH_MOBILISATION = 185_000


def _tune_records(lines):
    """A tap card turns up for a handful of unverified no-record lines in some zones (a records search the district
    ran in 2026)."""
    import itertools
    lines = lines.copy()
    p = P_SWEPT
    for z in K.OUTREACH_ORDER:
        t = lines[(lines.zone == z) & lines.no_record & ~lines.swept & lines.verified.isna()]
        uf, ud = SEARCH_PRICES[z]
        zl = lines[lines.zone == z]
        lgrr = int(zl.cls.isin(["LEAD", "GRR"]).sum())
        unk = zl[zl.cls == "LEAD STATUS UNKNOWN"]
        u = [int((unk.era == e).sum()) for e in range(3)]
        best = None
        for k in itertools.product(range(0, 13), repeat=3):
            uu = [u[e] - k[e] for e in range(3)]
            exp_u = sum(uu[e] * p[e] for e in range(3))
            repl = lgrr + exp_u
            cost = repl * uf + (sum(uu) - exp_u) * ud + SEARCH_MOBILISATION
            e_repl = abs((repl / 10) % 1 - 0.5) * 10
            e_cost = abs((cost / 1e5) % 1 - 0.5) * 1e5
            if e_repl >= 2.6 and e_cost >= 16000:
                if best is None or sum(k) < sum(best):
                    best = k
        assert best is not None, z
        r = K.stream("records-search", z)
        for e in range(3):
            pool = sorted(t[t.era == e].sl_id)
            for sl in r.choice(pool, size=best[e], replace=False) if best[e] else []:
                i = lines.index[lines.sl_id == sl][0]
                lines.at[i, "record"] = "COPPER"
                lines.at[i, "no_record"] = False
                lines.at[i, "cls"] = "NON-LEAD"
                lines.at[i, "basis"] = "RECORDS"
                lines.at[i, "truth"] = "NON-LEAD"
    return lines


def _never_built(lines):
    """Lots platted with a tap but never built on, or merged into a neighbour, leave no service line: a few dozen
    in each zone, all of them on records-known or new-build streets nobody has dug."""
    cov = lines.groupby("segment").verified.apply(lambda s: s.notna().mean())
    out = []
    for z in [x[0] for x in K.ZONES]:
        r = K.stream("never-built", z)
        t = lines[(lines.zone == z) & (lines.cls == "NON-LEAD") & lines.basis.isin(["RECORDS", "CONSTRUCTION DATE"]) &
                  lines.verified.isna() & ~lines.swept & (lines.segment.map(cov) <= 0.25)]
        out.extend(r.choice(sorted(t.sl_id), size=int(r.integers(13, 78)), replace=False))
        if z not in K.PLAN_ORDER:
            # services abandoned when lots were merged, galvanized by the tap card, in the two zones outside the plan
            g = lines[(lines.zone == z) & (lines.cls == "GRR") & (lines.basis == "RECORDS") & lines.verified.isna()]
            out.extend(r.choice(sorted(g.sl_id), size=int(r.integers(1, 4)), replace=False))
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
    """The inventory's view of the tap cards: in six zones a few lines no crew has dug carry a lead card where the
    world's draw gave a copper one (cards from before 1950), so each zone's expected replacements sit clear of their
    rounding edges. Nothing else reads these lines: they have no verification, completion or agreement."""
    lines = lines.copy()
    for z, k in sorted(K.LEAD_CARDS_ADDED.items()):
        pool = sorted(lines[(lines.zone == z) & (lines.record == "COPPER") & lines.era.isin([0, 1]) & ~lines.swept &
                            lines.verified.isna() & lines.replaced.isna()].sl_id)
        r = K.stream("lead-cards", z)
        for sl in r.choice(pool, size=k, replace=False):
            i = lines.index[lines.sl_id == sl][0]
            lines.at[i, "record"] = "LEAD"
            lines.at[i, "cls"] = "LEAD"
            lines.at[i, "basis"] = "RECORDS"
    return lines

def build():
    segs = _segments()
    lines = _lines(segs)
    lines = _records(lines)
    lines["no_record"] = (lines.record == "") & (lines.era.between(0, 2))
    sweeps = _pick_sweeps(segs, lines)
    lines["swept"] = lines.segment.isin(sweeps)
    lines = _trim_sweep_sample(lines)
    lines = _truth(lines)
    ev, projects = _verifications(lines, sweeps)
    lines = lines.set_index("sl_id", drop=False)
    rep = _replacements(lines, ev)
    first = ev.sort_values("date").groupby("sl_id").date.first()
    lines["verified"] = lines.sl_id.map(first)
    lines["replaced"] = lines.sl_id.map(rep)
    cls, basis = [], []
    for row in lines.itertuples():
        if row.era == 3:
            cls.append("NON-LEAD"); basis.append("CONSTRUCTION DATE")
        elif isinstance(row.replaced, dt.date):
            cls.append("NON-LEAD"); basis.append("REPLACED")
        elif isinstance(row.verified, dt.date):
            cls.append(row.truth); basis.append("FIELD VERIFIED")
        elif row.record in ("LEAD",):
            cls.append("LEAD"); basis.append("RECORDS")
        elif row.record == "GALV":
            cls.append("GRR"); basis.append("RECORDS")
        elif row.record in ("COPPER", "PLASTIC"):
            cls.append("NON-LEAD"); basis.append("RECORDS")
        else:
            cls.append("LEAD STATUS UNKNOWN"); basis.append("")
    lines["cls"] = cls
    lines["basis"] = basis
    lines = _tune_records(lines.reset_index(drop=True))
    lines = _never_built(lines)
    lines["legacy_premise"] = _premises(lines)
    lines["address"] = addresses(segs, lines)
    return segs, lines, sweeps, ev, projects


if __name__ == "__main__":
    segs, lines, sweeps, ev, projects = build()
    print(len(ev), "events", ev.cause.value_counts().to_dict())
    print(lines.cls.value_counts().to_dict())
    print(len(segs), "segments", len(lines), "lines")
    print(lines.groupby("zone").size())
    sw = lines[lines.swept & lines.no_record]
    sw = sw.assign(decade=(sw.year_built // 10) * 10, hit=sw.truth != "NON-LEAD")
    print(sw.groupby("decade").hit.agg(["size", "mean"]))
    nr = lines[lines.no_record & ~lines.swept]
    print("non-swept no-record by era:", nr.groupby("era").size().to_dict(), (nr.truth != "NON-LEAD").groupby(nr.era).mean().round(3).to_dict())
