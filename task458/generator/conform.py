"""The golden's conformance, from the shipped files only: NPPES on 1 November 2026, the adult members, the final claims,
the practising prescribers, each county's members with each condition, the three standards and the designation; and
the supporting figures (the conformed county and eligibility-group table, the fee-for-service payments).

Each county's members with each condition: a claim can identify a condition only in the months a member is enrolled, so
each member a final claim identifies counts as 1 over the share of the members enrolled all twelve months with the
condition whom a final claim identifies within their first k contract-year months, k the identified member's months
enrolled; the county's members with the condition are the sum over its identified members."""
import datetime as dt
import os

import numpy as np
import pandas as pd

D = dt.date
WINDOW_START, WINDOW_END = D(2025, 7, 1), D(2026, 6, 30)
AS_OF = D(2026, 11, 1)
MONTHS = [(2025, m) for m in range(7, 13)] + [(2026, m) for m in range(1, 7)]
FILES = {
    "claims": "bh_claims_encounters_dos_2025-07-01_2026-06-30.csv",
    "spans": "enrollment_spans_2025-07-01_2026-06-30.csv",
    "nppes": "npidata_pfile_wa_20050523-20261011.csv",
    "weeks": [("npidata_pfile_wa_20261012-20261018.csv", D(2026, 10, 18)),
              ("npidata_pfile_wa_20261019-20261025.csv", D(2026, 10, 25)),
              ("npidata_pfile_wa_20261026-20261101.csv", D(2026, 11, 1)),
              ("npidata_pfile_wa_20261102-20261108.csv", D(2026, 11, 8))],
    "deact": "NPPES_Deactivated_NPI_Report_20261110.xlsx",
    "zipcty": "ZIP_COUNTY_062026.xlsx",
}
COUNTY_FIPS = {"53001": "Adams", "53005": "Benton", "53007": "Chelan", "53017": "Douglas", "53021": "Franklin",
               "53025": "Grant", "53037": "Kittitas", "53047": "Okanogan", "53071": "Walla Walla", "53077": "Yakima"}
COUNTIES = sorted(COUNTY_FIPS.values())
GROUPS = ["SSI-DIS", "ADULT-EXP", "PARENT-CR", "AGED-65"]
THRESH = {"smi": 16.5, "oud": 23.0, "reach": 0.68}
BH_TAX = {"2084P0800X", "2084P0804X", "2084P0802X", "2084P0805X", "2084A0401X", "207QA0401X", "207RA0401X",
          "363LP0808X", "364SP0808X"}
VISITS = {"99202", "99203", "99204", "99205", "99211", "99212", "99213", "99214", "99215", "90791", "90792"}
SMI = ["F20.0", "F20.1", "F20.2", "F20.3", "F20.5", "F20.81", "F20.89", "F20.9", "F21", "F22", "F25.0", "F25.1", "F25.8",
       "F25.9", "F28", "F29", "F31.0", "F31.10", "F31.11", "F31.12", "F31.13", "F31.2", "F31.30", "F31.31", "F31.32",
       "F31.4", "F31.5", "F31.60", "F31.61", "F31.62", "F31.63", "F31.64", "F31.70", "F31.71", "F31.72", "F31.73",
       "F31.74", "F31.75", "F31.76", "F31.77", "F31.78", "F31.81", "F31.89", "F31.9", "F32.3", "F33.3"]
OUD = ["F11.10", "F11.11", "F11.120", "F11.121", "F11.122", "F11.129", "F11.13", "F11.14", "F11.150", "F11.151",
       "F11.159", "F11.181", "F11.182", "F11.188", "F11.19", "F11.20", "F11.21", "F11.220", "F11.221", "F11.222",
       "F11.229", "F11.23", "F11.24", "F11.250", "F11.251", "F11.259", "F11.281", "F11.282", "F11.288", "F11.29"]
SMI_SET = {c.replace(".", "") for c in SMI}
OUD_SET = {c.replace(".", "") for c in OUD}
QUARTERS = [("2025 Q3", D(2025, 7, 1), D(2025, 9, 30)), ("2025 Q4", D(2025, 10, 1), D(2025, 12, 31)),
            ("2026 Q1", D(2026, 1, 1), D(2026, 3, 31)), ("2026 Q2", D(2026, 4, 1), D(2026, 6, 30))]


def _date(s):
    return D(int(s[6:10]), int(s[0:2]), int(s[3:5])) if isinstance(s, str) and len(s) == 10 else None


def _iso(s):
    return D(int(s[0:4]), int(s[5:7]), int(s[8:10])) if isinstance(s, str) and len(s) == 10 else None


def read_nppes(path):
    return pd.read_csv(path, dtype=str, keep_default_na=False)


DEFAULTS = {"key": "client", "county_rule": "last", "dx_positions": 4, "versions": "final", "weeks": "through_asof",
            "zip_basis": "BUS_RATIO", "taxonomy": "primary", "require_service": True, "location": "practice",
            "deact_rule": "last_record", "deact_report": False}


_NPPES = {}


def nppes_on(target, day=AS_OF, weeks="through_asof"):
    """NPI -> (latest record on the day, the last record that was not a deactivation), the monthly file updated by the
    weekly files whose week ended by the day, record by record."""
    key = (target, day, weeks)
    if key not in _NPPES:
        _NPPES[key] = _nppes_on(target, day, weeks)
    return _NPPES[key]


def _nppes_on(target, day, weeks):
    latest, last_live = {}, {}
    frames = [read_nppes(os.path.join(target, FILES["nppes"]))]
    for name, end in FILES["weeks"]:
        if weeks == "all" or weeks == "through_asof" and end <= day:
            frames.append(read_nppes(os.path.join(target, name)))
    for df in frames:
        for rec in df.to_dict("records"):
            latest[rec["NPI"]] = rec
            if rec["Entity Type Code"]:
                last_live[rec["NPI"]] = rec
    return latest, last_live


def primary(rec):
    for k in range(1, 5):
        if rec.get("Healthcare Provider Primary Taxonomy Switch_%d" % k) == "Y":
            return rec["Healthcare Provider Taxonomy Code_%d" % k]
    return ""


def taxonomies(rec):
    return {rec.get("Healthcare Provider Taxonomy Code_%d" % k, "") for k in range(1, 5)} - {""}


def zip_county(target, basis="BUS_RATIO"):
    z = pd.read_excel(os.path.join(target, FILES["zipcty"]), dtype={"ZIP": str, "COUNTY": str})
    out = {}
    for zp, g in z.groupby("ZIP"):
        out[zp] = g.sort_values([basis, "COUNTY"], ascending=[False, True]).iloc[0]["COUNTY"]
    return out


def prescribers(target, opt=None):
    """The behavioral-health prescribers (NPI -> practice county FIPS on 1 November, or None) and the active flag."""
    o = dict(DEFAULTS, **(opt or {}))
    latest, last_live = nppes_on(target, weeks=o["weeks"])
    zc = zip_county(target, o["zip_basis"])
    report = {}
    if o["deact_report"]:
        d = pd.read_excel(os.path.join(target, FILES["deact"]), dtype=str, skiprows=3)
        report = {n: _date(v) for n, v in zip(d["NPI"], d["NPPES Deactivation Date"])}
    bh, county, active = {}, {}, {}
    for npi, rec in latest.items():
        live = rec["Entity Type Code"] != ""
        if npi in report:
            live = False
        src = rec if rec["Entity Type Code"] != "" else (last_live.get(npi) if o["deact_rule"] == "last_record" else None)
        if src is None or src["Entity Type Code"] != "1":
            continue
        if o["taxonomy"] == "primary" and primary(src) not in BH_TAX:
            continue
        if o["taxonomy"] == "any" and not taxonomies(src) & BH_TAX:
            continue
        bh[npi] = True
        active[npi] = live
        pre = "Provider Business Practice Location Address" if o["location"] == "practice" else "Provider Business Mailing Address"
        zp = src[pre + " Postal Code"][:5]
        st = src[pre + " State Name"]
        county[npi] = zc.get(zp) if st == "WA" and live else None
    return bh, county, active


_MEMBERS = {}


def members(target, opt=None):
    """One row per person (client_id): county (FIPS) and group on the last enrolled day, months enrolled."""
    o = dict(DEFAULTS, **(opt or {}))
    key = (target, o["key"], o["county_rule"])
    if key not in _MEMBERS:
        _MEMBERS[key] = _members(target, o)
    mem, mbr = _MEMBERS[key]
    return mem.copy(), dict(mbr)


def _members(target, o):
    s = pd.read_csv(os.path.join(target, FILES["spans"]), dtype=str, keep_default_na=False)
    s["start"] = s["span_start_dt"].map(_iso)
    s["end"] = s["span_end_dt"].map(lambda x: _iso(x) if x else WINDOW_END)
    s = s[(s["start"] <= WINDOW_END) & (s["end"] >= WINDOW_START)].copy()
    s["a"] = s["start"].map(lambda d: max(d, WINDOW_START))
    s["b"] = s["end"].map(lambda d: min(d, WINDOW_END))
    key = "client_id" if o["key"] == "client" else "mbr_id"
    rows = {}
    for rec in s.sort_values([key, "b", "a"]).to_dict("records"):
        p = rows.setdefault(rec[key], {"client_id": rec[key], "months": set(), "last": None, "first": None, "spans": []})
        p["spans"].append(rec)
        if p["first"] is None or rec["a"] < p["first"]["a"]:
            p["first"] = rec
        for y, m in MONTHS:
            first = D(y, m, 1)
            last = D(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)
            if rec["a"] <= last and rec["b"] >= first:
                p["months"].add((y, m))
        if p["last"] is None or rec["b"] > p["last"]["b"] or rec["b"] == p["last"]["b"] and rec["a"] >= p["last"]["a"]:
            p["last"] = rec
    out = []
    for cid, p in rows.items():
        pick = p["last"]
        if o["county_rule"] == "first":
            pick = p["first"]
        elif o["county_rule"] == "most":
            days = {}
            for sp in p["spans"]:
                days[sp["res_county_fips"]] = days.get(sp["res_county_fips"], 0) + (sp["b"] - sp["a"]).days + 1
            fips = max(sorted(days), key=lambda k: days[k])
            pick = dict(p["last"], res_county_fips=fips)
        iv = sorted((sp["a"], sp["b"]) for sp in p["spans"])
        days, cur = 0, None
        for a_, b_ in iv:
            if cur is None or a_ > cur[1] + dt.timedelta(days=1):
                if cur is not None:
                    days += (cur[1] - cur[0]).days + 1
                cur = [a_, b_]
            else:
                cur[1] = max(cur[1], b_)
        days += (cur[1] - cur[0]).days + 1
        out.append({"client_id": cid, "county": COUNTY_FIPS[pick["res_county_fips"]], "group": p["last"]["elig_group_cd"],
                    "months": len(p["months"]), "full_year": len(p["months"]) == 12, "days": days})
    mbr = dict(zip(s["mbr_id"], s["client_id"] if key == "client_id" else s["mbr_id"]))
    return pd.DataFrame(out).set_index("client_id"), mbr


def final_claims(target, versions="final"):
    c = pd.read_csv(os.path.join(target, FILES["claims"]), dtype=str, keep_default_na=False)
    if versions == "all":
        return c, c.copy()
    gone = set(c.loc[c["clm_freq_cd"].isin(["7", "8"]), "orig_icn"])
    f = c[(c["clm_freq_cd"] != "8") & (~c["clm_icn"].isin(gone))].copy()
    return c, f


_CACHE = {}


def analysis(target, **opt):
    o = dict(DEFAULTS, **opt)
    mem, mbr = members(target, o)
    ck = (target, o["versions"])
    if ck not in _CACHE:
        _CACHE.clear()
        _CACHE[ck] = final_claims(target, o["versions"])
    raw, fin = _CACHE[ck]
    fin = fin.copy()
    fin["client_id"] = fin["mbr_id"].map(mbr)
    assert fin["client_id"].notna().all()
    dx = fin[["dx_cd_1", "dx_cd_2", "dx_cd_3", "dx_cd_4"][:o["dx_positions"]]].values
    fin["smi"] = np.isin(dx, list(SMI_SET)).any(axis=1)
    fin["oud"] = np.isin(dx, list(OUD_SET)).any(axis=1)
    bh, pcounty, active = prescribers(target, o)
    fin["visit"] = fin["proc_cd"].isin(VISITS) & fin["rendering_npi"].map(lambda n: n in bh)
    mem["rec_smi"] = mem.index.isin(set(fin.loc[fin["smi"], "client_id"]))
    mem["rec_oud"] = mem.index.isin(set(fin.loc[fin["oud"], "client_id"]))
    mem["seen"] = mem.index.isin(set(fin.loc[fin["visit"], "client_id"]))
    rendered = set(fin["rendering_npi"])
    practising = {c: sorted(n for n in bh if active[n] and pcounty.get(n) == f and (n in rendered or not o["require_service"]))
                  for f, c in COUNTY_FIPS.items()}
    # the contract-year month (1 = July 2025) of each member's first final claim or encounter carrying each condition;
    # the share of the members enrolled all year with the condition identified within their first k months; and each
    # identified member's weight, 1 over that share at their own months enrolled
    first_month(fin, mem)
    cap = capture_shares(mem)
    for cond in ("smi", "oud"):
        mem["w_" + cond] = np.where(mem["rec_" + cond], 1.0 / np.array(cap[cond])[mem["months"].values - 1], 0.0)
    rows = []
    for c in COUNTIES:
        for g in GROUPS:
            m = mem[(mem["county"] == c) & (mem["group"] == g)]
            full = m[m["full_year"]]
            row = {"county": c, "group": g, "members": len(m), "full_year": len(full),
                   "rec_smi": int(m["rec_smi"].sum()), "rec_oud": int(m["rec_oud"].sum()),
                   "full_rec_smi": int(full["rec_smi"].sum()), "full_rec_oud": int(full["rec_oud"].sum()),
                   "seen_smi": int((m["rec_smi"] & m["seen"]).sum()),
                   "est_smi": float(m["w_smi"].sum()), "est_oud": float(m["w_oud"].sum())}
            rows.append(row)
    cg = pd.DataFrame(rows)
    sc = []
    for c in COUNTIES:
        x = cg[cg["county"] == c]
        n_pres = len(practising[c])
        est_smi, est_oud = x["est_smi"].sum(), x["est_oud"].sum()
        seen = x["seen_smi"].sum()
        v = {"county": c, "prescribers": n_pres, "members": int(x["members"].sum()), "est_smi": est_smi,
             "est_oud": est_oud, "seen_smi": int(seen), "s_smi": n_pres / est_smi * 1000, "s_oud": n_pres / est_oud * 1000,
             "s_reach": seen / est_smi}
        v["fail_smi"] = v["s_smi"] < THRESH["smi"]
        v["fail_oud"] = v["s_oud"] < THRESH["oud"]
        v["fail_reach"] = v["s_reach"] < THRESH["reach"]
        v["fails"] = int(v["fail_smi"]) + int(v["fail_oud"]) + int(v["fail_reach"])
        v["designated"] = v["fails"] >= 2
        sc.append(v)
    sc = pd.DataFrame(sc).set_index("county")
    # fee-for-service payments for the services behavioral-health prescribers rendered, by member county and quarter:
    # each final claim's paid amount once (it repeats on every line of the claim)
    ffs = fin[(fin["fin_arrangement_cd"] == "FFS")].copy()
    bh_claims = set(ffs.loc[ffs["rendering_npi"].map(lambda n: n in bh), "clm_icn"])
    first = ffs[ffs["clm_icn"].isin(bh_claims)].sort_values(["clm_icn", "clm_line_num"]).drop_duplicates("clm_icn")
    first["county"] = first["client_id"].map(mem["county"])
    first["dos"] = first["svc_from_dt"].map(_iso)
    first["paid"] = first["paid_amt"].astype(float)
    first["group"] = first["client_id"].map(mem["group"])
    pay, pay_group = {}, {}
    for c in COUNTIES:
        for q, a, b in QUARTERS:
            sel = first[(first["county"] == c) & (first["dos"] >= a) & (first["dos"] <= b)]
            pay[(c, q)] = round(float(sel["paid"].sum()), 2)
        for g in GROUPS:
            sel = first[(first["county"] == c) & (first["group"] == g)]
            pay_group[(c, g)] = round(float(sel["paid"].sum()), 2)
    return {"members": mem, "cg": cg, "scorecard": sc, "practising": practising, "pay": pay, "pay_group": pay_group,
            "final": fin, "raw": raw, "bh": bh, "pcounty": pcounty, "active": active, "pay_claims": first, "capture": cap}


def first_month(fin, mem):
    """mem['first_smi'], mem['first_oud']: the contract-year month (1 = July 2025) of the member's first final claim or
    encounter carrying the condition (NaN when none does)."""
    for cond in ("smi", "oud"):
        h = fin.loc[fin[cond], ["client_id", "svc_from_dt"]]
        k = (h["svc_from_dt"].str[:4].astype(int) - 2025) * 12 + h["svc_from_dt"].str[5:7].astype(int) - 6
        mem["first_" + cond] = k.groupby(h["client_id"]).min().reindex(mem.index)
        d = h["svc_from_dt"].map(lambda x: (_iso(x) - WINDOW_START).days + 1)
        mem["first_day_" + cond] = d.groupby(h["client_id"]).min().reindex(mem.index)
    return mem


def capture_shares(mem, by=None):
    """cond -> [F(1) .. F(12)]: among the members enrolled all twelve months whom a claim identifies with the condition,
    the share first identified within the first k contract-year months (by=None: the plan; else a dict of group keys)."""
    out = {}
    for cond in ("smi", "oud"):
        fy = mem[mem["full_year"] & mem["rec_" + cond]]
        out[cond] = [float((fy["first_" + cond] <= k).mean()) for k in range(1, 13)]
    return out


if __name__ == "__main__":
    import sys
    a = analysis(sys.argv[1])
    pd.set_option("display.width", 200)
    print(a["scorecard"].round(3))
    print(sorted(a["scorecard"].index[a["scorecard"]["designated"]]))
