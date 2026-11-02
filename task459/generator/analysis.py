"""task459 analysis, from target/ alone: every rung of the ladder, the golden and its variants, and the asks.

The golden reads each covered member's 2025 as a sequence of dated places (an in-person medical service at the
rendering practice's location on that date, a retail fill at an Arizona pharmacy, an in-home visit by a regional
agency), carries each place to the days nearest it, and counts the member in the region holding the most days.

    python3 analysis.py [target_dir]
"""
import collections
import datetime as dt
import decimal
import functools
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
Y0, Y1 = dt.date(2025, 1, 1), dt.date(2025, 12, 31)
ND = 365

F = {
    "schedule": "SC_2027_IHS_Agreement_Schedule_B.pdf",
    "members": "sc_member_extract_20261009.csv",
    "addr": "sc_member_address_history_20261009.csv",
    "enroll": "sc_enrollment_spans_20261009.csv",
    "medical": "med_claims_svc2025_paid_thru_20260630.csv",
    "pbm": "pbm_claims_2025_PVHP.txt",
    "visits": "ihs_visit_claims_2025.csv",
    "directory": "provider_directory_20261001.xlsx",
    "moves": "provider_location_changes_2025.csv",
    "pharmacies": "pharmacy_network_2025.csv",
}
NOT_A_PLACE = {"81", "10", "02"}      # independent laboratory (bills from its own site), telehealth
PRIMARY_EM = {"99202", "99203", "99204", "99205", "99211", "99212", "99213", "99214", "99215", "99397", "G0439"}


def doy(d):
    return (d - Y0).days


def round_half_up(x):
    return int(decimal.Decimal(repr(x)).quantize(decimal.Decimal("1"), rounding=decimal.ROUND_HALF_UP))


# ---------------------------------------------------------------------------------------------------------
class Data:
    pass


def pdf_text(path):
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout


def read_schedule(path):
    """Regions, their county codes and agencies, and the budget, from Schedule B's text."""
    txt = pdf_text(path)
    lines = txt.splitlines()
    i0 = next(i for i, l in enumerate(lines) if re.match(r"^\s*Region\s{2,}Counties", l))
    i1 = next(i for i, l in enumerate(lines) if i > i0 and l.strip().startswith("B.2"))
    rows = []
    for l in lines[i0 + 1:i1]:
        if not l.strip():
            continue
        lead = len(l) - len(l.lstrip(" "))
        cells = re.split(r"\s{2,}", l.strip())
        if lead <= 2:
            rows.append({"region": cells[0], "counties": " ".join(cells[1:-1]) if len(cells) > 2 else cells[1],
                         "agency": cells[-1]})
        else:
            rows[-1]["counties"] += " " + l.strip()
    regions, fips_region, agency_region = [], {}, {}
    for r in rows:
        regions.append(r["region"])
        for f in re.findall(r"\((04\d{3})\)", r["counties"]):
            fips_region[f] = r["region"]
        agency_region[r["agency"]] = r["region"]
    budget = int(re.search(r"USD ([\d,]+) \(the 2027 Budget\)", txt).group(1).replace(",", ""))
    return regions, fips_region, agency_region, budget


@functools.lru_cache(maxsize=4)
def load(target):
    d = Data()
    d.target = target
    d.regions, d.fips_region, d.agency_region, d.budget = read_schedule(os.path.join(target, F["schedule"]))
    d.ridx = {r: i for i, r in enumerate(d.regions)}
    d.agency_of_region = {v: k for k, v in d.agency_region.items()}
    rd = lambda name, **kw: pd.read_csv(os.path.join(target, F[name]), dtype=str, keep_default_na=False, **kw)
    d.members = rd("members")
    d.addr = rd("addr")
    d.enroll = rd("enroll")
    d.moves = rd("moves")
    d.pharm = rd("pharmacies")
    wb = load_workbook(os.path.join(target, F["directory"]), read_only=True)
    ws = wb["Directory"]
    it = ws.iter_rows(values_only=True)
    hdr = next(it)
    d.directory = pd.DataFrame([list(r) for r in it], columns=hdr).fillna("").astype(str)
    wb.close()
    # provider locations: current county from the directory, earlier counties from the change log
    d.npi_fips = dict(zip(d.directory["NPI"], d.directory["PRACTICE_COUNTY_FIPS"]))
    d.npi_type = dict(zip(d.directory["NPI"], d.directory["PROVIDER_TYPE"]))
    d.npi_agency = {n: a for n, a in zip(d.directory["NPI"], d.directory["AGENCY_NAME"]) if a}
    ch = collections.defaultdict(list)
    for r in d.moves.itertuples(index=False):
        ch[r.NPI].append((dt.date.fromisoformat(r.EFFECTIVE_DATE), r.PRIOR_COUNTY_FIPS, r.NEW_COUNTY_FIPS))
    d.changes = {k: sorted(v) for k, v in ch.items()}
    d.ph_region = {n: d.fips_region.get(f, "") for n, f in zip(d.pharm["NCPDP_ID"], d.pharm["COUNTY_FIPS"])}
    d.ph_type = dict(zip(d.pharm["NCPDP_ID"], d.pharm["PHARMACY_TYPE"]))
    # claims
    d.med = rd("medical")
    d.med["d"] = pd.to_datetime(d.med["SVC_FROM_DT"], format="%Y%m%d").dt.date
    d.pbm = rd("pbm", sep="|")
    d.pbm["MEMBER_ID"] = "PVS" + d.pbm["CARDHOLDER_ID"].str[2:]
    d.pbm["d"] = pd.to_datetime(d.pbm["DATE_FILLED"], format="%m/%d/%Y").dt.date
    d.vis = rd("visits")
    d.vis["d"] = pd.to_datetime(d.vis["DATE_OF_SERVICE"], format="%Y-%m-%d").dt.date
    # members: age and enrollment
    d.dob = dict(zip(d.members["MEMBER_ID"], d.members["DATE_OF_BIRTH"]))
    d.status = dict(zip(d.members["MEMBER_ID"], d.members["MEMBER_STATUS"]))
    d.record_region = {m: d.fips_region.get(f, "") for m, f in zip(d.members["MEMBER_ID"], d.members["ADDR_OF_RECORD_COUNTY_FIPS"])}
    d.pcp_npi = dict(zip(d.members["MEMBER_ID"], d.members["PCP_NPI"]))
    spans = collections.defaultdict(list)
    for r in d.enroll.itertuples(index=False):
        spans[r.MEMBER_ID].append((dt.date.fromisoformat(r.SPAN_START),
                                   dt.date.fromisoformat(r.SPAN_END) if r.SPAN_END else None))
    d.spans = spans
    hist = collections.defaultdict(list)
    for r in d.addr.itertuples(index=False):
        hist[r.MEMBER_ID].append((dt.date.fromisoformat(r.EFFECTIVE_DATE), d.fips_region.get(r.COUNTY_FIPS, "")))
    d.hist = {k: sorted(v) for k, v in hist.items()}
    return d


def region_on(d, npi, day):
    f = d.npi_fips.get(npi, "")
    for eff, prior, new in d.changes.get(npi, ()):
        if day < eff:
            f = prior
            break
    return d.fips_region.get(f, "")


def region_now(d, npi):
    return d.fips_region.get(d.npi_fips.get(npi, ""), "")


def age_end_2025(dob):
    y, m, dd = map(int, dob.split("-"))
    return 2025 - y - ((12, 31) < (m, dd))


def every_day_2025(spans):
    """Enrolled on every day of 2025: the spans, merged, cover 1 January to 31 December."""
    cur = Y0
    for s, e in sorted(spans):
        if s > cur:
            return False
        if e is None or e >= Y1:
            return True
        cur = max(cur, e + dt.timedelta(days=1))
    return False


def covered(d, variant="golden"):
    out = []
    for m, sp in d.spans.items():
        if age_end_2025(d.dob[m]) < 75:
            continue
        if variant == "pop_ends":       # enrolled on 1 January and on 31 December, gaps ignored
            ok = any(s <= Y0 and (e is None or e >= Y0) for s, e in sp) and any(s <= Y1 and (e is None or e >= Y1) for s, e in sp)
        else:
            ok = every_day_2025(sp)
        if variant == "pop_active":     # status at the extract (not the Schedule's population)
            ok = ok and d.status[m] == "ACTIVE"
        if ok:
            out.append(m)
    return sorted(out)


# ---------------------------------------------------------------------------------------------------------
def med_regions(d, asof=True):
    """Region of each medical claim line's rendering practice on the service date."""
    key = "_reg_asof" if asof else "_reg_now"
    if key not in d.med:
        base = d.med["RENDERING_NPI"].map(lambda n: region_now(d, n))
        if asof:
            moved = d.med["RENDERING_NPI"].isin(list(d.changes))
            base = base.copy()
            base[moved] = [region_on(d, n, x) for n, x in zip(d.med.loc[moved, "RENDERING_NPI"], d.med.loc[moved, "d"])]
        d.med[key] = base
    return d.med[key]


def pbm_kept(d, keep_reversed=False):
    """Paid fills: a B1 claim not reversed by a B2 (a reversed claim re-billed the same day is a new B1)."""
    p = d.pbm
    rev = set(p.loc[p["TRANS_TYPE"] == "B2", "ORIG_RX_CLAIM_NBR"])
    b1 = p[p["TRANS_TYPE"] == "B1"]
    if keep_reversed:
        return b1
    return b1[~b1["RX_CLAIM_NBR"].isin(rev)]


def visits_net(d):
    """Visit claims net of adjustments: a void cancels the claim it names, a replacement takes the place of the
    claim it names."""
    v = d.vis
    voided = set(v.loc[v["FREQ_CD"] == "8", "ORIG_CLAIM_NO"])
    replaced = set(v.loc[v["FREQ_CD"] == "7", "ORIG_CLAIM_NO"])
    keep = v[(v["FREQ_CD"] != "8") & ~v["CLAIM_NO"].isin(voided) & ~v["CLAIM_NO"].isin(replaced)]
    return keep


def events(d, variant="golden"):
    """Dated places per member: DataFrame (mid, t, r) with t the day of 2025 and r the region index."""
    ck = "_ev_" + variant
    if hasattr(d, ck):
        return getattr(d, ck)
    parts = []
    if variant != "no_medical":
        m = d.med
        reg = med_regions(d, asof=(variant != "now_location"))
        mask = pd.Series(True, index=m.index)
        if variant != "with_lab_tele":
            mask &= ~m["PLACE_OF_SVC"].isin(NOT_A_PLACE)
        if variant == "no_denied":
            mask &= m["LINE_STATUS"] != "D"
        if variant == "net_claims":
            voided = set(m.loc[m["CLAIM_FREQ_CD"] == "8", "ORIG_CLAIM_ID"])
            mask &= (m["CLAIM_FREQ_CD"] != "8") & ~m["CLAIM_ID"].isin(voided)
        parts.append(pd.DataFrame({"mid": m.loc[mask, "MEMBER_ID"], "d": m.loc[mask, "d"], "reg": reg[mask],
                                   "src": "med"}))
    if variant not in ("no_rx", "medical_only"):
        p = pbm_kept(d, keep_reversed=(variant == "rx_all"))
        reg = p["SVC_PROV_ID"].map(d.ph_region)
        parts.append(pd.DataFrame({"mid": p["MEMBER_ID"], "d": p["d"], "reg": reg, "src": "rx"}))
    if variant not in ("no_visits", "medical_only"):
        v = visits_net(d)
        reg = v["AGENCY_NPI"].map(lambda n: d.agency_region.get(d.npi_agency.get(n, ""), ""))
        parts.append(pd.DataFrame({"mid": v["MEMBER_ID"], "d": v["d"], "reg": reg, "src": "visit"}))
    ev = pd.concat(parts, ignore_index=True)
    ev = ev[ev["reg"] != ""]
    ev = ev[(ev["d"] >= Y0) & (ev["d"] <= Y1)]
    ev["t"] = ev["d"].map(doy).astype(int)
    ev["r"] = ev["reg"].map(d.ridx).astype(int)
    ev = ev[["mid", "t", "r", "src"]]
    setattr(d, ck, ev)
    return ev


def per_member(ev, high=False):
    """mid -> (days sorted unique, region per day, events per region, n same-day conflicts). A day holding places in
    two regions takes the region with more places that day (ties to the first region in Schedule B's order, or the
    last with high=True)."""
    out = {}
    for mid, g in ev.groupby("mid", sort=False):
        t = g["t"].to_numpy()
        r = g["r"].to_numpy()
        order = np.lexsort((r, t))
        t, r = t[order], r[order]
        days, start = np.unique(t, return_index=True)
        reg = np.empty(len(days), dtype=int)
        conflicts = 0
        for k, s in enumerate(start):
            e = start[k + 1] if k + 1 < len(start) else len(t)
            vals = r[s:e]
            if len(set(vals.tolist())) > 1:
                conflicts += 1
                cnt = np.bincount(vals, minlength=8)
                reg[k] = int(np.argmax(cnt)) if not high else int(7 - np.argmax(cnt[::-1]))
            else:
                reg[k] = int(vals[0])
        out[mid] = (days, reg, np.bincount(r, minlength=8), conflicts)
    return out


TT = np.arange(ND)
AN_DAY = [Y0 + dt.timedelta(days=i) for i in range(ND)]


def day_regions(days, reg, mode="nearest"):
    """Region carried to every day of 2025 from the dated places."""
    n = len(days)
    if mode == "forward":
        i = np.searchsorted(days, TT, side="right") - 1
        i[i < 0] = 0
        return reg[i]
    if mode == "backward":
        i = np.searchsorted(days, TT, side="left")
        i[i >= n] = n - 1
        return reg[i]
    pos = np.searchsorted(days, TT, side="left")
    nxt = np.minimum(pos, n - 1)
    prv = np.maximum(pos - 1, 0)
    dn = np.where(pos < n, days[nxt] - TT, 10 ** 6)
    dp = np.where(pos > 0, TT - days[prv], 10 ** 6)
    if mode == "nearest_tie_next":
        choose_next = dn <= dp
    else:
        choose_next = dn < dp
    return np.where(choose_next, reg[nxt], reg[prv])


def address_days_region(d, mid):
    h = d.hist.get(mid, [])
    if not h:
        return d.record_region.get(mid, "")
    cnt = collections.Counter()
    for i, (eff, reg) in enumerate(h):
        nxt = h[i + 1][0] if i + 1 < len(h) else dt.date(2100, 1, 1)
        lo, hi = max(eff, Y0), min(nxt - dt.timedelta(days=1), Y1)
        if hi >= lo:
            cnt[reg] += (hi - lo).days + 1
    if not cnt:
        # every address took effect after 2025: the first one held
        return h[0][1]
    return max(sorted(cnt), key=lambda k: cnt[k])


def address_on_region(d, mid, day):
    h = d.hist.get(mid, [])
    reg = h[0][1] if h else d.record_region.get(mid, "")
    for eff, r in h:
        if eff <= day:
            reg = r
    return reg


# ---------------------------------------------------------------------------------------------------------
RUNGS = ["address", "address_dec31", "address_days", "pcp", "pcp_visits", "claim_majority", "event_days",
         "address_override"]
DAY_VARIANTS = ["golden", "forward", "backward", "nearest_tie_next", "conflict_high", "no_denied", "no_rx",
                "no_visits", "medical_only", "rx_all", "net_claims", "fallback_record", "now_location",
                "pop_ends", "with_lab_tele", "pop_active"]
COMPLIANT = DAY_VARIANTS[:-2]        # every reading the filed text licenses
LAYER1_SLIPS = ["with_lab_tele", "pop_active"]   # mishandlings the filed text does not license (asserted neutral)


def member_regions(target, method="golden"):
    """mid -> region name for every covered member, under the golden, a variant or a rung."""
    d = load(target)
    pop = covered(d, method if method in ("pop_active", "pop_ends") else "golden")
    out = {}
    if method in ("address",):
        return {m: d.record_region[m] for m in pop}
    if method == "address_dec31":
        return {m: address_on_region(d, m, Y1) for m in pop}
    if method == "address_days":
        return {m: address_days_region(d, m) for m in pop}
    if method == "pcp":
        return {m: region_now(d, d.pcp_npi[m]) for m in pop}
    if method == "pcp_visits":
        m_ = d.med
        reg = med_regions(d)
        mask = m_["PROC_CD"].isin(PRIMARY_EM) & m_["RENDERING_NPI"].map(lambda n: d.npi_type.get(n) == "PRIMARY CARE") \
            & (m_["CLAIM_FREQ_CD"] == "1")
        sub = pd.DataFrame({"mid": m_.loc[mask, "MEMBER_ID"], "reg": reg[mask], "cid": m_.loc[mask, "CLAIM_ID"]}).drop_duplicates()
        cnt = sub.groupby(["mid", "reg"]).size()
        best = {}
        for (mid, r), n in cnt.items():
            best.setdefault(mid, []).append((n, r))
        for m in pop:
            own = region_now(d, d.pcp_npi[m])
            if m in best:
                top = max(n for n, r in best[m])
                regs = sorted(r for n, r in best[m] if n == top)
                out[m] = own if own in regs else regs[0]
            else:
                out[m] = own
        return out
    var = method if method in DAY_VARIANTS else "golden"
    ev_var = var if var in ("with_lab_tele", "no_denied", "no_rx", "no_visits", "medical_only", "rx_all",
                            "net_claims", "now_location") else "golden"
    if not hasattr(d, "_pm_" + ev_var):
        setattr(d, "_pm_" + ev_var, per_member(events(d, ev_var)))
    pm = getattr(d, "_pm_" + ev_var)
    if var == "conflict_high":
        if not hasattr(d, "_pm_high"):
            d._pm_high = per_member(events(d, "golden"), high=True)
        pm = d._pm_high
    mode = {"forward": "forward", "backward": "backward", "nearest_tie_next": "nearest_tie_next"}.get(var, "nearest")
    for m in pop:
        if m not in pm:
            out[m] = d.record_region[m] if var == "fallback_record" else address_days_region(d, m)
            continue
        days, reg, per_region, _ = pm[m]
        if method == "claim_majority":
            c = per_region
        elif method == "event_days":
            c = np.bincount(reg, minlength=8)
        elif method == "address_override":
            # home (the address held that day) on every day without a place, the place on days with one
            base = np.array([d.ridx.get(address_on_region(d, m, AN_DAY[t]), 0) for t in range(ND)]) \
                if len(d.hist.get(m, [])) > 1 else np.full(ND, d.ridx.get(address_on_region(d, m, Y1), 0))
            base[days] = reg
            c = np.bincount(base, minlength=8)
        else:
            c = np.bincount(day_regions(days, reg, mode), minlength=8)
        out[m] = d.regions[int(np.argmax(c[:len(d.regions)]))]
    return out


def counts_of(target, regions_by_member):
    d = load(target)
    c = collections.Counter(regions_by_member.values())
    return {r: c.get(r, 0) for r in d.regions}


def allocation(target, counts):
    d = load(target)
    n = sum(counts.values())
    return {r: round_half_up(d.budget * counts[r] / n) for r in d.regions}


def main_call(target, method="golden"):
    regs = member_regions(target, method)
    counts = counts_of(target, regs)
    return {"counts": counts, "alloc": allocation(target, counts), "regions": regs}


def margins(target, method="golden"):
    """Each covered member's lead in days of its region over the next region, under a day-reading."""
    d = load(target)
    pm = getattr(d, "_pm_golden", None) or per_member(events(d, "golden"))
    d._pm_golden = pm
    mode = {"forward": "forward", "backward": "backward", "nearest_tie_next": "nearest_tie_next"}.get(method, "nearest")
    out = {}
    for m in covered(d):
        if m not in pm:
            continue
        days, reg, _, _ = pm[m]
        c = np.sort(np.bincount(day_regions(days, reg, mode), minlength=8))[::-1]
        out[m] = int(c[0] - c[1])
    return out


# ---------------------------------------------------------------------------------------------------------
# Asks: members aged 65 to 74 on 31 December 2025.
def young(d):
    return {m for m, b in d.dob.items() if 65 <= age_end_2025(b) <= 74}


def hm(s):
    h, m = s.split(":")
    return int(h) * 60 + int(m)


def visit_table(target, variant="golden"):
    """One row per Visit (golden: consecutive claims chained into one continuous attendance)."""
    d = load(target)
    yg = young(d)
    if variant == "rows":            # every claim row that is not a void
        v = d.vis[d.vis["FREQ_CD"] != "8"].copy()
    else:
        v = visits_net(d).copy()
    v = v[v["MEMBER_ID"].isin(yg)]
    v["agency"] = v["AGENCY_NPI"].map(d.npi_agency)
    v["s"] = v["PERIOD_START"].map(hm)
    v["u"] = v["UNITS"].astype(int)
    v["e"] = v["s"] + 15 * v["u"]
    v = v.sort_values(["MEMBER_ID", "agency", "d", "s", "CLAIM_NO"]).reset_index(drop=True)
    if variant in ("golden",):
        new = [True] * len(v)
        mid, ag, dd, ss, ee = (v[c].tolist() for c in ("MEMBER_ID", "agency", "d", "s", "e"))
        for i in range(1, len(v)):
            if mid[i] == mid[i - 1] and ag[i] == ag[i - 1] and dd[i] == dd[i - 1] and ss[i] == ee[i - 1]:
                new[i] = False
        v["visit"] = np.cumsum(new)
        g = v.groupby("visit").agg(agency=("agency", "first"), d=("d", "first"), minutes=("u", lambda x: 15 * int(x.sum())))
    elif variant == "starts":        # one visit per member, agency, date and start time
        g = v.groupby(["MEMBER_ID", "agency", "d", "s"]).agg(u=("u", "sum")).reset_index()
        g["minutes"] = 15 * g["u"]
    else:                            # one visit per claim row
        g = v.assign(minutes=15 * v["u"])[["agency", "d", "minutes"]]
    g = g.reset_index(drop=True)
    g["q"] = g["d"].map(lambda x: (x.month - 1) // 3 + 1)
    return g


def ask_a(target, variant="golden"):
    d = load(target)
    g = visit_table(target, variant)
    c = g.groupby(["agency", "q"]).size()
    return {(a, q): int(c.get((a, q), 0)) for a in [d.agency_of_region[r] for r in d.regions] for q in (1, 2, 3, 4)}


def ask_b(target, variant="golden"):
    d = load(target)
    g = visit_table(target, variant)
    out = {}
    for r in d.regions:
        a = d.agency_of_region[r]
        x = g[g["agency"] == a]["minutes"]
        out[a] = float(x.sum()) / len(x)
    return out


def ask_c(target, variant="golden"):
    """Plan-paid medical spend in 2025 for members aged 65 to 74, by the region of the rendering practice's location
    on the date of service, net of replacements and voids (USD)."""
    d = load(target)
    yg = young(d)
    m = d.med
    reg = med_regions(d, asof=(variant not in ("now_location", "mirror")))
    mask = m["MEMBER_ID"].isin(yg)
    if variant not in ("gross", "mirror"):
        voided = set(m.loc[m["CLAIM_FREQ_CD"] == "8", "ORIG_CLAIM_ID"])
        replaced = set(m.loc[m["CLAIM_FREQ_CD"] == "7", "ORIG_CLAIM_ID"])
        mask &= (m["CLAIM_FREQ_CD"] != "8") & ~m["CLAIM_ID"].isin(voided) & ~m["CLAIM_ID"].isin(replaced)
    paid = m.loc[mask, "PAID_AMT"].astype(float)
    s = paid.groupby(reg[mask]).sum()
    return {r: float(s.get(r, 0.0)) for r in d.regions}


def k1(x):
    """USD to thousands, one decimal, half up."""
    return float(decimal.Decimal(repr(x / 1000.0)).quantize(decimal.Decimal("0.1"), rounding=decimal.ROUND_HALF_UP))


def m1(x):
    return float(decimal.Decimal(repr(x)).quantize(decimal.Decimal("0.1"), rounding=decimal.ROUND_HALF_UP))


def main(argv):
    target = argv[1] if len(argv) > 1 else os.path.join(TASK, "target")
    d = load(target)
    gold = main_call(target)
    print("covered members", sum(gold["counts"].values()))
    print("%-16s" % "rung" + "".join("%18s" % r[:16] for r in d.regions))
    for meth in ["golden"] + RUNGS + DAY_VARIANTS[1:]:
        c = main_call(target, meth)
        print("%-16s" % meth + "".join("%8d %9d" % (c["counts"][r], c["alloc"][r]) for r in d.regions))
    print("ask A", ask_a(target))
    print("ask B", {k: m1(v) for k, v in ask_b(target).items()})
    print("ask C", {k: k1(v) for k, v in ask_c(target).items()})
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
