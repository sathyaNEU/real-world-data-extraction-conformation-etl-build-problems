"""Turns the simulated truth into the housing needs service's extracts, cut at 30 September 2026."""
import heapq

import numpy as np
import pandas as pd

import world as W
import sim as S

LANDLORDS = ["Medway Valley Homes", "Orchard Vale Housing Association", "Kentish Weald Homes",
             "Larkmoor Homes", "Saxon Gate Housing Trust", "Downsview Housing"]
PRIVATE = "Larkmoor Lettings (private sector)"


def d(x):
    return "" if pd.isna(x) else pd.Timestamp(x).strftime("%Y-%m-%d")


def cases_frame(df, rng):
    A, B = W.ASOF, W.START
    keep = (df["app"] <= A) & (df["exit"].isna() | (df["exit"] >= B) | (df["exit"] > A))
    c = df[keep].copy()
    open_ = c["exit"].isna() | (c["exit"] > A)
    need_dec = np.array([a[0][1] for a in c["assess"]])
    out = pd.DataFrame({
        "case_ref": c["case_ref"],
        "household_ref": c["hh"],
        "application_date": c["app"].map(d),
        "household_type": c["hh_type"],
        "decision": np.where(c["main"], "Main duty accepted", "Main duty not owed"),
        "decision_date": c["decision"].map(lambda x: d(x) if x <= A else ""),
        "bedrooms_needed_at_decision": np.where(c["decision"] <= A, need_dec.astype(str), ""),
        "case_status": np.where(open_, "Open", "Closed"),
        "closed_date": np.where(open_, "", c["exit"].map(d)),
        "closure_reason": np.where(open_, "", c["exit_reason"].fillna("")),
    })
    # cases still at the relief stage on the cut have no decision yet
    und = c["decision"] > A
    out.loc[und.values, "decision"] = "Awaiting decision"
    return out.sort_values("case_ref", kind="mergesort").reset_index(drop=True)


def reviews_frame(df):
    A = W.ASOF
    rows = []
    for ref, ex, a in zip(df["case_ref"], df["exit"], df["assess"]):
        last = pd.Timestamp(A) if pd.isna(ex) else min(ex, A)
        for (t0, n0, _), (t1, n1, why) in zip(a, a[1:]):
            if t1 > last:
                break
            if n1 != n0:
                rows.append((ref, d(t1), n0, n1, why))
    out = pd.DataFrame(rows, columns=["case_ref", "review_date", "bedrooms_before", "bedrooms_after", "reason"])
    return out.sort_values(["review_date", "case_ref"], kind="mergesort").reset_index(drop=True)


REL = {"Applicant": "Applicant", "Partner": "Partner", "Other adult": "Other relative"}


def members_frame(df):
    """the people in the household of every case open on the cut, as the housing register lists them"""
    A = W.ASOF
    o = df[(df["app"] <= A) & (df["exit"].isna() | (df["exit"] > A))]
    rows = []
    for ref, mem in zip(o["case_ref"], o["members"]):
        lead = [m for m in mem if m[0] in ("Applicant", "Partner")]
        rest = sorted((m for m in mem if m[0] not in ("Applicant", "Partner") and m[2] <= A), key=lambda m: m[2])
        for k, (rel, sex, dob) in enumerate(lead + rest, 1):
            r = REL.get(rel) or ("Daughter" if sex == "F" else "Son")
            rows.append((ref, k, r, sex, d(dob)))
    out = pd.DataFrame(rows, columns=["case_ref", "member_no", "relationship", "sex", "date_of_birth"])
    return out.sort_values(["case_ref", "member_no"], kind="mergesort").reset_index(drop=True)


def lets_frame(df, lt, rng):
    A, B = W.ASOF, W.START
    w = lt[lt["tenancy_start"] >= B].copy()
    land = np.where(w["kind"].str.startswith("Settled: social"),
                    np.array(LANDLORDS)[rng.integers(0, len(LANDLORDS), len(w))], PRIVATE)
    rows = pd.DataFrame({
        "case_ref": df.loc[w["row"].values, "case_ref"].values,
        "bedrooms": w["size"].values,
        "landlord": land,
        "offer_date": w["offer_date"].map(d).values,
        "tenancy_start": w["tenancy_start"].map(d).values,
        "let_status": np.where(w["tenancy_start"] <= A, "Tenancy started", "Accepted, tenancy to start"),
        "_seq": np.arange(len(w)),
    })
    rows = rows.sort_values(["tenancy_start", "_seq"], kind="mergesort").drop(columns="_seq").reset_index(drop=True)
    rows.insert(0, "let_ref", ["ML%05d" % (k + 1) for k in range(len(rows))])
    import zlib
    rows.insert(3, "property_ref", ["P%06d" % (100000 + zlib.crc32(("prop|%s" % r).encode()) % 900000)
                                    for r in rows["case_ref"]])
    return rows


class Units:
    """Unit references for placements that never overlap in one unit."""

    def __init__(self, prefix, beds=True):
        self.prefix, self.beds, self.pool, self.n = prefix, beds, {}, 0
        self.meta = []

    def take(self, start, end, size):
        key = size if self.beds else 0
        h = self.pool.setdefault(key, [])
        if h and h[0][0] <= start:
            free, ref = heapq.heappop(h)
        else:
            self.n += 1
            ref = "%s-%04d" % (self.prefix, self.n)
            self.meta.append((ref, key))
        heapq.heappush(h, (end + pd.Timedelta(days=2), ref))
        return ref


def placements_frame(df, pl):
    A, B = W.ASOF, W.START
    far = pd.Timestamp("2099-12-31")
    p = pl[(pl["start"] <= A) & (pl["end"] >= B)].copy()
    p = p.sort_values(["start", "row"], kind="mergesort").reset_index(drop=True)
    units = {"Private sector lease": Units("PSL"), "Nightly-paid self-contained": Units("NPS"),
             "Bed and breakfast": Units("BB", beds=False), "Hostel": Units("HOS", beds=False)}
    # units occupied by placements that ended before the window still exist; the window opens clean
    refs = []
    sizes = np.minimum(S.need_on(df, p["row"].values, p["start"].values), 4)
    for (_, r), size in zip(p.iterrows(), sizes):
        if r["type"] == "Tenter House":
            refs.append(r["unit"])
            continue
        refs.append(units[r["type"]].take(r["start"], r["end"] if r["end"] < far else far, int(size)))
    reason_map = {
        "Settled: social housing let": "Left TA: social housing let",
        "Settled: private let (Larkmoor Lettings)": "Left TA: private let through Larkmoor Lettings",
    }
    end_reason = []
    for _, r in p.iterrows():
        if r["end"] > A:
            end_reason.append("")
        elif r["end_kind"] == "move":
            end_reason.append("Moved to other TA")
        elif r["end_kind"] == "away":
            end_reason.append("Left TA: duty continues, staying with family or friends")
        else:
            why = df.at[r["row"], "exit_reason"]
            end_reason.append(reason_map.get(why, "Left TA: " + str(why).lower()))
    out = pd.DataFrame({
        "case_ref": df.loc[p["row"].values, "case_ref"].values,
        "accommodation_type": p["type"].values,
        "unit_ref": refs,
        "placement_start": p["start"].map(d).values,
        "placement_end": [d(x) if x <= A else "" for x in p["end"]],
        "end_reason": end_reason,
    })
    out.insert(0, "placement_ref", ["TA%06d" % (k + 1) for k in range(len(out))])
    return out, units


def register_frame(units):
    rows = []
    th = 0
    for s in W.SIZES:
        for q in range(W.TH_UNITS[s]):
            th += 1
            rows.append(dict(unit_ref="TH-%d%02d" % (s, q + 1), accommodation_type="Tenter House",
                             block_or_address="Tenter House, 2 Wharf Road, Larkmoor", bedrooms=s,
                             provider=W.PROVIDER, contract="Block lease from 1 Apr 2021 (notice served 15 Sep 2026, ends 31 Mar 2027)"))
    provs = {"Private sector lease": ["Larkmoor Lettings PSL scheme", "Harbourside Property Partners", "Greystone Residential"],
             "Nightly-paid self-contained": ["Bridgeway Accommodation Ltd", "Kestrel Housing Solutions", "Northfleet Lodgings"],
             "Bed and breakfast": ["Station Hotel Larkmoor", "The Anchor Guest House", "Riverside Inn"],
             "Hostel": ["Larkmoor Family Hostel", "St Mildred's House"]}
    for typ, u in units.items():
        for k, (ref, size) in enumerate(u.meta):
            rows.append(dict(unit_ref=ref, accommodation_type=typ,
                             block_or_address=("Room %d, %s" % (k % 40 + 1, provs[typ][k % len(provs[typ])])) if not u.beds
                             else "Unit %s, Larkmoor district" % ref[-4:],
                             bedrooms="" if not u.beds else int(size),
                             provider=provs[typ][k % len(provs[typ])],
                             contract="Lot 2 nightly rate" if typ == "Nightly-paid self-contained" else
                             ("Lease" if typ == "Private sector lease" else "Spot booking")))
    return pd.DataFrame(rows)
