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


def pending_lets(df, k):
    """Lets offered and accepted before the cut whose tenancies start in October: the first k_s
    households of each size's list on 30 September."""
    A = W.ASOF
    o = df[df["main"] & (df["duty"] <= A) & (df["exit"].isna() | (df["exit"] > A))].copy()
    o["cur"] = S.need_at(o, A)
    rows = []
    for s in W.SIZES:
        q = o[o["cur"] == s].sort_values(["duty", "case_ref"], kind="mergesort").head(k[s])
        for j, (i, r) in enumerate(q.iterrows()):
            rows.append((i, s, j))
    return rows


def cases_frame(df, rng):
    A, B = W.ASOF, W.START
    keep = (df["app"] <= A) & (df["exit"].isna() | (df["exit"] >= B) | (df["exit"] > A))
    c = df[keep].copy()
    open_ = c["exit"].isna() | (c["exit"] > A)
    hh_type = np.where(c["need"] == 1, np.where(rng.random(len(c)) < 0.8, "Single person", "Couple, no children"),
                       np.where(rng.random(len(c)) < 0.62, "Single parent with children", "Couple with children"))
    out = pd.DataFrame({
        "case_ref": c["case_ref"],
        "household_ref": c["hh"],
        "application_date": c["app"].map(d),
        "household_type": hh_type,
        "decision": np.where(c["main"], "Main duty accepted", "Main duty not owed"),
        "decision_date": c["decision"].map(lambda x: d(x) if x <= A else ""),
        "bedrooms_needed_at_decision": np.where(c["decision"] <= A, c["need"].astype(str), ""),
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
    r = df[df["reassess"].notna() & (df["reassess"] <= A) & (df["need"] < 4)]
    r = r[r["exit"].isna() | (r["reassess"] <= r["exit"])]
    reasons = ["Birth", "Child joined the household", "Adult child returned", "Medical assessment: separate bedroom"]
    out = pd.DataFrame({
        "case_ref": r["case_ref"],
        "review_date": r["reassess"].map(d),
        "bedrooms_before": r["need"].astype(int),
        "bedrooms_after": r["need_after"].astype(int),
        "reason": [reasons[(int(x[-3:]) * 7) % 4] for x in r["case_ref"]],
    })
    return out.sort_values(["review_date", "case_ref"], kind="mergesort").reset_index(drop=True)


def lets_frame(df, lt, pend, rng):
    A, B = W.ASOF, W.START
    w = lt[(lt["tenancy_start"] >= B) & (lt["tenancy_start"] <= A)].copy()
    land = np.where(w["kind"].str.startswith("Settled: social"),
                    np.array(LANDLORDS)[rng.integers(0, len(LANDLORDS), len(w))], PRIVATE)
    rows = pd.DataFrame({
        "case_ref": df.loc[w["row"].values, "case_ref"].values,
        "bedrooms": w["size"].values,
        "landlord": land,
        "offer_date": w["offer_date"].map(d).values,
        "tenancy_start": w["tenancy_start"].map(d).values,
        "let_status": "Tenancy started",
        "_seq": np.arange(len(w)),
    })
    prow = []
    for i, s, j in pend:
        start = pd.Timestamp("2026-10-01") + pd.Timedelta(days=int(3 + 4 * j + (s % 3)))
        offer = pd.Timestamp("2026-09-14") + pd.Timedelta(days=int(2 * j + s))
        social = (j + s) % 4 != 0
        prow.append(dict(case_ref=df.at[i, "case_ref"], bedrooms=s,
                         landlord=LANDLORDS[(j + 2 * s) % len(LANDLORDS)] if social else PRIVATE,
                         offer_date=d(offer), tenancy_start=d(start), let_status="Accepted, tenancy to start",
                         _seq=10 ** 6 + len(prow)))
    rows = pd.concat([rows, pd.DataFrame(prow)], ignore_index=True)
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
    rea = df.loc[p["row"].values, "reassess"].values
    n0 = df.loc[p["row"].values, "need"].values
    n1 = df.loc[p["row"].values, "need_after"].values
    st = p["start"].values
    sizes = np.where(~pd.isna(rea) & (rea <= st), n1, n0)
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
                             provider=W.PROVIDER, contract="Block lease 2021-2026 (notice served 15 Sep 2026)"))
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
