"""Every owed figure, computed from the shipped pack alone (the files under target/), as a solver would.

The main call: each candidate county's 2027 annual expected loss under the vendor's event set, and the loss a
FORTIFIED re-roof of its modeled portfolio removes, the roof's cut read from the company's own claims since 2012
class by class of local peak gust (the vendor's hazard classes), the adjustment tested storm by storm under MG-04.
The ladder's other rungs and the rival adjustments are computed here too, for checks.py and the design note.
"""
import os
import re

import numpy as np
import pandas as pd

import params as P

KT = 1.150779


def _p(target, k):
    return os.path.join(target, P.FILES[k])


def load_footprints(target):
    """Peak gust by storm and ZIP in mph: the older sheets are in knots under a title block."""
    xl = pd.ExcelFile(_p(target, "footprints"))
    out = []
    for sh in xl.sheet_names:
        raw = xl.parse(sh, header=None)
        hdr = raw.index[raw.iloc[:, 0].astype(str).str.lower().isin(["zip", "zip_code"])][0]
        df = xl.parse(sh, header=hdr)
        col = [c for c in df.columns if "gust" in str(c).lower()][0]
        mph = df[col].astype(float) * (KT if "kt" in str(col).lower() else 1.0)
        zc = [c for c in df.columns if str(c).lower().startswith("zip")][0]
        out.append(pd.DataFrame({"sheet": sh, "zip_code": df[zc].astype(str).str.zfill(5), "gust_mph": mph}))
    return pd.concat(out, ignore_index=True)


def storm_table(target):
    reg = pd.read_csv(_p(target, "storms"), dtype=str).fillna("")
    reg["sheet"] = [n.split()[-1] + " " + d[:4] for n, d in zip(reg.storm_name, reg.landfall_date)]
    return reg


def cells(target, since=P.MG04_FROM_YEAR):
    """Storm x ZIP x roof: Coverage A in force at landfall (USD), net paid on the storm's claims (USD), local gust."""
    reg = storm_table(target)
    reg = reg[reg.landfall_date.str[:4].astype(int) >= since]
    cl = pd.read_csv(_p(target, "claims"), dtype={"zip_code": str, "catastrophe_code": str}, keep_default_na=False)
    cl = cl[cl.catastrophe_code.isin(reg.claims_catastrophe_code)]
    cl["fort"] = cl.mitigation_credit.str.contains("FORT-R").astype(int)
    paid = cl.groupby(["catastrophe_code", "zip_code", "fort"]).amount_usd.sum().rename("paid").reset_index()
    paid = paid.merge(reg[["claims_catastrophe_code", "storm_id"]], left_on="catastrophe_code",
                      right_on="claims_catastrophe_code").drop(columns=["claims_catastrophe_code", "catastrophe_code"])
    inf = pd.read_parquet(_p(target, "inforce"))
    inf = inf[inf.storm_id.isin(reg.storm_id)].copy()
    inf["tiv"] = np.where(inf.coverage_unit == "USD thousands", inf.coverage_a * 1000.0, inf.coverage_a)
    inf["fort"] = (inf.roof_designation == "FORTIFIED Roof").astype(int)
    inf = inf.groupby(["storm_id", "zip_code", "fort"]).agg(tiv=("tiv", "sum"), pols=("policies_in_force", "sum")).reset_index()
    c = inf.merge(paid, on=["storm_id", "zip_code", "fort"], how="left").fillna({"paid": 0.0})
    fp = load_footprints(target).merge(reg[["sheet", "storm_id"]], on="sheet")
    c = c.merge(fp[["storm_id", "zip_code", "gust_mph"]], on=["storm_id", "zip_code"], how="left")
    c["cls"] = (np.floor(c.gust_mph / 10.0) * 10).astype(int)
    return c


def _ratio(d):
    s, f = d[d.fort == 0], d[d.fort == 1]
    if f.tiv.sum() == 0 or s.paid.sum() == 0:
        return np.nan
    return 1.0 - (f.paid.sum() / f.tiv.sum()) / (s.paid.sum() / s.tiv.sum())


def _ratio_matched(d):
    s = d[d.fort == 0].set_index(["storm_id", "zip_code"])
    f = d[d.fort == 1].set_index(["storm_id", "zip_code"])
    j = f.join(s, lsuffix="_f", rsuffix="_s", how="inner")
    j = j[j.tiv_s > 0]
    den = (j.paid_s / j.tiv_s * j.tiv_f).sum()
    return np.nan if den == 0 else 1.0 - j.paid_f.sum() / den


def adjustments(c):
    """The rival adjustments: name -> function(gust mph) -> cut."""
    out = {}
    out["one ratio, pooled"] = (lambda r: (lambda g: r))(_ratio(c))
    out["one ratio, ZIP-matched"] = (lambda r: (lambda g: r))(_ratio_matched(c))
    for name, fn in (("10-mph classes, pooled", _ratio), ("10-mph classes, ZIP-matched", _ratio_matched)):
        tab = {k: fn(v) for k, v in c.groupby("cls")}
        tab = {k: v for k, v in tab.items() if not np.isnan(v)}
        out[name] = _class_fn(tab, 10)
    tab20 = {k: _ratio(v) for k, v in c.groupby((c.gust_mph // 20 * 20).astype(int))}
    out["20-mph classes, pooled"] = _class_fn({k: v for k, v in tab20.items() if not np.isnan(v)}, 20)
    lo, hi = _ratio(c[c.gust_mph < 130]), _ratio(c[c.gust_mph >= 130])
    out["two classes at 130 mph"] = lambda g, lo=lo, hi=hi: lo if g < 130 else hi
    return out


def _class_fn(tab, width):
    ks = sorted(tab)

    def f(g):
        k = int(g // width * width)
        if k in tab:
            return tab[k]
        return tab[ks[0]] if k < ks[0] else tab[ks[-1]]
    f.table = tab
    return f


def class_table(c):
    return {k: _ratio(v) for k, v in c.groupby("cls")}


def backtest(c, adj):
    """MG-04: each storm since 2012 with at least the threshold paid on FORTIFIED homes, its paid on those homes
    reproduced from the paid per dollar of the standard homes in the same ZIP and storm, times the adjustment."""
    out = []
    for sid, d in c.groupby("storm_id"):
        f = d[d.fort == 1]
        act = f.paid.sum()
        if act < P.MG04_MIN_PAID:
            continue
        s = d[d.fort == 0].set_index("zip_code")
        pred = 0.0
        for z, tf, g in zip(f.zip_code, f.tiv, f.gust_mph):
            if z in s.index and s.loc[z, "tiv"] > 0:
                pred += s.loc[z, "paid"] / s.loc[z, "tiv"] * tf * (1.0 - adj(g))
        out.append((sid, act, pred, pred / act - 1.0))
    return out


def passes(bt):
    return all(abs(e) <= P.MG04_TOL for _, _, _, e in bt)


def vendor(target):
    elt = pd.read_parquet(_p(target, "elt"))
    haz = pd.read_csv(_p(target, "hazard"))
    haz["event_id"] = haz.event_ref.str.replace("HU27-", "", regex=False).astype(int)
    code = {v: k for k, v in P.PORTFOLIO_CODE.items()}
    elt["county"] = elt.portfolio_id.map(code).map(P.COUNTY_NAME)
    m = elt.merge(haz[["event_id", "county", "peak_gust_class"]], on=["event_id", "county"], how="left")
    m["cls_lo"] = m.peak_gust_class.str.extract(r"(\d+)-").astype(int)
    m["aal"] = m.annual_rate * m.mean_loss_usd
    return m


def county_figures(target, c=None):
    c = cells(target) if c is None else c
    m = vendor(target)
    adj = adjustments(c)
    res = {}
    for name, f in adj.items():
        cut = m.cls_lo.map(lambda lo: f(lo + 5.0))
        res[name] = (m.aal * cut).groupby(m.county).sum()
    aal = m.groupby("county").aal.sum()
    return aal, res, adj


GOLDEN = "10-mph classes, pooled"
DEFAULT = "one ratio, pooled"


def main_call(target):
    c = cells(target)
    aal, res, adj = county_figures(target, c)
    g = res[GOLDEN].sort_values(ascending=False)
    bt = {k: backtest(c, f) for k, f in adj.items()}
    return dict(aal=aal, removed=res, golden=g, call=g.index[0], runner=g.index[1], adj=adj, bt=bt, cells=c)


# ---------------------------------------------------------------- the asks
ABBR = {"ROAD": "RD", "DRIVE": "DR", "LANE": "LN", "STREET": "ST", "COURT": "CT", "AVENUE": "AVE", "CIRCLE": "CIR",
        "WAY": "WAY"}


def norm_addr(a):
    """Upper case, street types abbreviated, the second building on a parcel as one token."""
    s = str(a).upper().replace(",", " ")
    s = re.sub(r"\bBLDG 2\b", "COTTAGE", s)
    toks = [ABBR.get(t, t) for t in s.split()]
    return " ".join(toks)


def asof_inforce(target, day=P.ASOF):
    pm = pd.read_csv(_p(target, "policies"), dtype=str, keep_default_na=False)
    pm["coverage_a_usd"] = pm.coverage_a_usd.astype(float)
    live = pm[(pm.inception_date <= day) & ((pm.cancellation_date == "") | (pm.cancellation_date > day))].copy()
    live["key"] = live.parcel_id + "|" + live.site_address.map(norm_addr)
    return pm, live


def split_addr(a):
    """(house number, street with its type, second-building flag) from any of the three address forms."""
    t = norm_addr(a).split()
    cot = t[-1] == "COTTAGE"
    if cot:
        t = t[:-1]
    return t[0], " ".join(t[1:]), cot


def ask_a(target, route="golden"):
    """Insured homes holding a valid FORTIFIED Roof certificate on 30 September 2026, by candidate county: homes and
    Coverage A. A certificate stays with the building, not with the policy it was issued under, and keeps the address
    the building had when it was issued."""
    ce = pd.read_csv(_p(target, "certs"), dtype=str, keep_default_na=False)
    voided = set(ce[ce.event == "VOIDED"].certificate_number) if route != "no_voids" else set()
    iss = ce[ce.event == "ISSUED"]
    valid = iss[(iss.event_date <= P.ASOF) & (iss.expiry_date > P.ASOF) & ~iss.certificate_number.isin(voided)].copy()
    parts = valid.property_address.map(split_addr)
    valid["parcel"] = valid.parcel_ref.str.replace("-", "", regex=False)
    valid["key"] = valid.parcel + "|" + parts.map(lambda t: "B2" if t[2] else "B1")
    valid["akey"] = valid.parcel + "|" + valid.property_address.map(norm_addr)
    pm, live = asof_inforce(target)
    lp = live.site_address.map(split_addr)
    live["bkey"] = live.parcel_id + "|" + lp.map(lambda t: "B2" if t[2] else "B1")
    if route == "by_policy":       # join on the policy the certificate was issued under
        hit = live[live.policy_number.isin(valid.policy_number_at_issue)]
    elif route == "by_parcel":     # one building per parcel
        hit = live[live.parcel_id.isin(set(valid.parcel))].drop_duplicates("parcel_id")
    elif route == "parcel_address":   # parcel and the address as written
        hit = live[live.key.isin(set(valid.akey))]
    elif route == "cert_rows":     # count certificates, not homes
        m = valid.merge(live[["bkey", "county", "coverage_a_usd"]], left_on="key", right_on="bkey")
        out = m.groupby("county").agg(homes=("key", "size"), cov=("coverage_a_usd", "sum"))
        return out.reindex([P.COUNTY_NAME[c] for c in P.CANDIDATES])
    else:
        hit = live[live.bkey.isin(set(valid.key))]
    out = hit.groupby("county").agg(homes=("bkey" if "bkey" in hit else "key", "size"), cov=("coverage_a_usd", "sum"))
    return out.reindex([P.COUNTY_NAME[c] for c in P.CANDIDATES])


LEGACY_STORMS = ["2008-03", "2009-02", "2011-04"]


def ask_b(target, route="golden"):
    """The three storms before the 2012 system change: each storm's net paid to date, and the part of it paid after
    31 December 2011 (USD). A claim still open at the cut-over was carried into the new system with its paid-to-date
    posted as the first line on 1 January 2012, the same money the legacy valuations already hold."""
    reg = storm_table(target)
    lv = pd.read_csv(_p(target, "legacy"), dtype={"zip": str})
    lv["d"] = pd.to_datetime(lv.valuation_date, format="%m/%d/%Y")
    last = lv.sort_values(["legacy_claim_no", "d"]).groupby("legacy_claim_no").tail(1).set_index("legacy_claim_no")
    cl = pd.read_csv(_p(target, "claims"), dtype=str, keep_default_na=False)
    cl["amount_usd"] = cl.amount_usd.astype(float)
    car = cl[cl.legacy_claim_ref != ""]
    newsum = car.groupby("legacy_claim_ref").amount_usd.sum()
    conv = car[car.payment_date == "2012-01-01"].groupby("legacy_claim_ref").amount_usd.sum()
    conv = conv[(conv - last.paid_to_date.reindex(conv.index)).abs() < 0.005]
    after = (newsum - conv.reindex(newsum.index).fillna(0.0))
    if route == "golden":
        total = last.paid_to_date.copy()
        total.loc[newsum.index] = last.paid_to_date.reindex(newsum.index) + after
    elif route == "legacy_plus_new":      # legacy paid to date plus every new-system line
        total = last.paid_to_date.copy()
        total.loc[newsum.index] = total.loc[newsum.index] + newsum
        after = newsum
    elif route == "legacy_only":          # the legacy valuations alone
        total = last.paid_to_date.copy()
        after = newsum * 0.0
    elif route == "sum_valuations":       # cumulative valuations summed as if payments
        total = lv.groupby("legacy_claim_no").paid_to_date.sum()
        total.loc[newsum.index] = total.loc[newsum.index] + newsum
        after = newsum
    out = {}
    for sid in LEGACY_STORMS:
        lcode = reg.set_index("storm_id").loc[sid, "legacy_catastrophe_code"]
        ids = last.index[last.storm == lcode]
        out[sid] = (float(total.reindex(ids).fillna(0.0).sum()), float(after.reindex(ids).fillna(0.0).sum()))
    return out


def _name(street):
    """A street's name without its type (TRAM AVE -> TRAM)."""
    t = street.split()
    return " ".join(t[:-1]) if len(t) > 1 and t[-1] in ABBR.values() else street


def street_pairs(ce, pm):
    """Old and new street names, paired by the parcels the certificate register lists under one name and the policy
    master under another at the same house number. Returns {(county, old name): new name}."""
    iss = ce[ce.event == "ISSUED"]
    ca = iss.property_address.map(split_addr)
    a = pd.DataFrame({"parcel": iss.parcel_ref.str.replace("-", "", regex=False), "num": ca.str[0],
                      "old": ca.str[1].map(_name)})
    pa = pm.site_address.map(split_addr)
    b = pd.DataFrame({"parcel": pm.parcel_id, "county": pm.county, "num": pa.str[0], "new": pa.str[1].map(_name)})
    j = a.merge(b.drop_duplicates(), on=["parcel", "num"])
    j = j[j.old != j.new]
    return {(c, o): n for (c, o, n), _ in j.groupby(["county", "old", "new"])}


def street_map(pe, pm, ce):
    """Each permit street carrying an old name, read under the new name with its own street type."""
    pairs = street_pairs(ce, pm)
    out = {}
    for c, st in set(zip(pe.county, pe.address.map(lambda a: split_addr(a)[1]))):
        nm = _name(st)
        if (c, nm) in pairs:
            out[(c, st)] = pairs[(c, nm)] + st[len(nm):]
    return out


def street_map_by_number(pe, pm):
    """The same pairing found another way: a street the policy master does not know in that county, whose house
    numbers in each ZIP sit on one street the policy master does know (a check on street_pairs, not the golden)."""
    pmp = pm.site_address.map(split_addr)
    known = pd.DataFrame({"county": pm.county, "zip": pm.zip_code, "num": pmp.str[0], "street": pmp.str[1]})
    pp = pe.address.map(split_addr)
    per = pd.DataFrame({"county": pe.county, "zip": pe.zip, "num": pp.str[0], "street": pp.str[1]})
    ks = set(zip(known.county, known.street))
    out = {}
    for (cty, st), d in per[[(c, s) not in ks for c, s in zip(per.county, per.street)]].groupby(["county", "street"]):
        m = d.merge(known[known.county == cty], on=["zip", "num"], suffixes=("", "_now"))
        if len(m):
            out[(cty, st)] = m.street_now.value_counts().index[0]
    return out


def ask_c(target, route="golden"):
    """Each county's portfolio homes whose roof will be 15 or more years old on 1 June 2027 (roof year 2012 or
    earlier), and their Coverage A. A re-roof permit since the underwriting record replaces the roof year; a permit
    issued before a street was renamed carries the old name."""
    pf = pd.read_csv(_p(target, "portfolios"), dtype={"zip_code": str})
    pe = pd.read_csv(_p(target, "permits"), dtype={"zip": str})
    pe = pe[pe.issue_date <= P.ASOF].copy()
    if route == "golden" or route == "any_roof_permit":
        pm = pd.read_csv(_p(target, "policies"), dtype=str, keep_default_na=False)
        ce = pd.read_csv(_p(target, "certs"), dtype=str, keep_default_na=False)
        mp = street_map(pe, pm, ce)
        pp = pe.address.map(split_addr)
        pe["address"] = [("%s %s%s" % (t[0], mp.get((c, t[1]), t[1]), " COTTAGE" if t[2] else ""))
                         for c, t in zip(pe.county, pp)]
    if route == "any_roof_permit":
        rr = pe[pe.work_class.isin(["RE-ROOF", "ROOF REPAIR"])]
    else:
        rr = pe[pe.work_class == "RE-ROOF"]
    rr = rr.assign(key=rr.address.map(norm_addr) + "|" + rr.zip, yr=rr.issue_date.str[:4].astype(int))
    if route == "ignore_building":
        rr = rr.assign(key=rr.address.str.replace(" BLDG 2", "", regex=False).map(norm_addr) + "|" + rr.zip)
    last = rr.groupby("key").yr.max()
    pf["key"] = pf.site_address.map(norm_addr) + "|" + pf.zip_code
    yr = pf.roof_year_on_record
    if route != "record":
        yr = np.maximum(yr, pf.key.map(last).fillna(0).astype(int))
    old = pf[yr <= 2012]
    out = old.groupby("county").agg(homes=("key", "size"), cov=("coverage_a_usd", "sum"))
    return out.reindex([P.COUNTY_NAME[c] for c in P.CANDIDATES])
