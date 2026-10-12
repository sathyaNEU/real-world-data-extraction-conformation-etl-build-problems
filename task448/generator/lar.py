"""The Kansas HMDA loan-level file for 2024 and 2025 in the Data Browser's layout (the fields the research desk
keeps): every reporter's records in the eight counties, built from the simulated closings and the reporters' other
applications there, and the statewide records of every other county."""
import datetime as dt

import numpy as np
import pandas as pd

import world as W

COLUMNS = ["activity_year", "lei", "derived_msa-md", "state_code", "county_code", "census_tract",
           "conforming_loan_limit", "derived_loan_product_type", "derived_dwelling_category", "derived_ethnicity",
           "derived_race", "derived_sex", "action_taken", "purchaser_type", "preapproval", "loan_type", "loan_purpose",
           "lien_status", "reverse_mortgage", "open-end_line_of_credit", "business_or_commercial_purpose",
           "loan_amount", "combined_loan_to_value_ratio", "interest_rate", "rate_spread", "hoepa_status",
           "total_loan_costs", "origination_charges", "loan_term", "property_value", "construction_method",
           "occupancy_type", "total_units", "income", "debt_to_income_ratio", "applicant_age",
           "submission_of_application", "initially_payable_to_institution", "aus-1", "denial_reason-1",
           "tract_population", "tract_minority_population_percent", "ffiec_msa_md_median_family_income",
           "tract_to_msa_income_percentage", "tract_owner_occupied_units", "tract_one_to_four_family_homes",
           "tract_median_age_of_housing_units"]
LTYPE = {"CONV": 1, "FHA": 2, "VA": 3, "USDA": 4}
PRODUCT = {1: "Conventional", 2: "FHA", 3: "VA", 4: "FSA/RHS"}
CLL = {2024: 766550, 2025: 806500}
RATE = {2024: {1: 6.86, 2: 6.52, 3: 6.31, 4: 6.58}, 2025: {1: 6.71, 2: 6.38, 3: 6.17, 4: 6.44}}
PMMS = {2024: 6.72, 2025: 6.62}


def county_weights():
    w = {}
    rest = [c for c in W.KS_COUNTIES if c not in W.BIG and c not in W.REGION]
    for c in W.KS_COUNTIES:
        if c in W.REGION:
            continue
        w[c] = W.BIG.get(c, 0.0)
    left = max(0.0, 100.0 - sum(W.BIG.values()) - 5.0)
    rng = np.random.default_rng(W.SEED + 41)
    raw = rng.gamma(2.0, 1.0, len(rest))
    for c, v in zip(rest, raw / raw.sum() * left):
        w[c] = float(v)
    return w


def tracts():
    """Census tracts per county with the FFIEC tract attributes."""
    rng = np.random.default_rng(W.SEED + 42)
    cw = county_weights()
    out = {}
    for c in W.KS_COUNTIES:
        n = W.TRACTS[c] if c in W.TRACTS else max(2, int(round(cw[c] * 5.5)) if c in W.BIG else int(rng.integers(2, 5)))
        codes, k = [], 1
        while len(codes) < n:
            if rng.random() < 0.18 and len(codes) + 2 <= n:
                codes += ["%04d%02d" % (k, 1), "%04d%02d" % (k, 2)]
            else:
                codes.append("%04d00" % k)
            k += 1
        minority = {"Wyandotte": 55, "Seward": 62, "Finney": 50, "Ford": 58, "Sedgwick": 30, "Johnson": 22}.get(c, 12)
        rows = []
        for t in codes:
            rows.append(dict(tract=W.FIPS[c] + t, pop=int(rng.integers(1900, 7400)),
                             minority=round(float(np.clip(rng.normal(minority, minority * 0.35), 1.5, 92)), 2),
                             inc_pct=int(np.clip(rng.normal(100, 24), 42, 205)),
                             owner=int(rng.integers(380, 2300)), one4=int(rng.integers(560, 2900)),
                             age=int(rng.integers(9, 77))))
        out[c] = rows
    return out


def _cat(rng, n, opts, p):
    p = np.array(p, float)
    return np.array(opts, dtype=object)[rng.choice(len(opts), size=n, p=p / p.sum())]


def fill(D, rng, T, exempt):
    """D: a frame with activity_year, lei, county, action_taken, loan_purpose, lien_status, loan_type, amount, value,
    occupancy_type, total_units, construction_method, business. Fill every public field the way the Data Browser
    writes it. exempt: set of LEIs that report under the partial exemption."""
    n = len(D)
    out = pd.DataFrame(index=D.index)
    out["activity_year"] = D.activity_year.values
    out["lei"] = D.lei.values
    out["derived_msa-md"] = [W.MSA.get(c, "99999") for c in D.county]
    out["state_code"] = "KS"
    out["county_code"] = [W.FIPS[c] for c in D.county]
    tr = [T[c][int(rng.integers(len(T[c])))] if t is None else t for c, t in zip(D.county, D.get("tract", [None] * n))]
    out["census_tract"] = [x["tract"] for x in tr]
    orig = (D.action_taken == 1).values
    first = (D.lien_status == 1).values
    yrs = D.activity_year.values
    amt = D.amount.values.astype(float)
    val = D.value.values.astype(float)
    out["conforming_loan_limit"] = np.where(amt <= np.array([CLL[y] for y in yrs]), "C", "NC")
    out["derived_loan_product_type"] = ["%s:%s" % (PRODUCT[t], "First Lien" if l == 1 else "Subordinate Lien")
                                        for t, l in zip(D.loan_type, D.lien_status)]
    out["derived_dwelling_category"] = ["Single Family (1-4 Units):%s" % ("Site-Built" if c == 1 else "Manufactured")
                                        if u <= 4 else "Multifamily:Site-Built"
                                        for c, u in zip(D.construction_method, D.total_units)]
    out["derived_ethnicity"] = _cat(rng, n, ["Not Hispanic or Latino", "Hispanic or Latino", "Ethnicity Not Available",
                                             "Joint"], [80, 8, 9, 3])
    out["derived_race"] = _cat(rng, n, ["White", "Race Not Available", "Black or African American", "Asian", "Joint",
                                        "American Indian or Alaska Native", "2 or more minority races",
                                        "Native Hawaiian or Other Pacific Islander"], [79, 11, 3.6, 2.2, 2.4, 1.2, 0.4,
                                                                                       0.2])
    out["derived_sex"] = _cat(rng, n, ["Joint", "Male", "Female", "Sex Not Available"], [37, 34, 21, 8])
    out["action_taken"] = D.action_taken.values
    pt = np.zeros(n, int)
    sold = orig & first
    lt = D.loan_type.values
    gov = np.isin(lt, [2, 3, 4])
    r = rng.random(n)
    pt[sold & gov] = 2
    conv_sold = sold & ~gov
    pt[conv_sold & (r < 0.30)] = 1
    pt[conv_sold & (r >= 0.30) & (r < 0.52)] = 3
    pt[conv_sold & (r >= 0.52) & (r < 0.58)] = 71
    pt[conv_sold & (r >= 0.58) & (r < 0.61)] = 6
    pt[conv_sold & (r >= 0.61)] = 0
    port = D.portfolio.values
    pt[orig & port & (r < 0.78)] = 0
    pt[(D.action_taken == 6).values] = 0
    out["purchaser_type"] = pt
    out["preapproval"] = np.where((D.loan_purpose == 1).values & orig & (rng.random(n) < 0.07), 1, 2)
    out["loan_type"] = lt
    out["loan_purpose"] = D.loan_purpose.values
    out["lien_status"] = D.lien_status.values
    out["reverse_mortgage"] = 2
    out["open-end_line_of_credit"] = np.where((D.lien_status == 2).values & (D.loan_purpose != 1).values &
                                              (rng.random(n) < 0.45), 1, 2)
    out["business_or_commercial_purpose"] = D.business.values
    out["loan_amount"] = (np.floor(amt / 10000) * 10000 + 5000).astype(int)
    cltv = np.round(np.clip(amt / np.maximum(val, 1) * 100 + rng.normal(0, 0.4, n), 8, 104), 3)
    out["combined_loan_to_value_ratio"] = ["%g" % v for v in cltv]
    base = np.array([RATE[y][t] for y, t in zip(yrs, lt)]) + np.where(first, 0.0, 1.9)
    rate = np.round(base + rng.normal(0, 0.33, n), 3)
    rate = np.round(np.round(rate * 8) / 8, 3)
    out["interest_rate"] = ["%g" % v for v in rate]
    spread = np.round(rate - np.array([PMMS[y] for y in yrs]) + rng.normal(-0.05, 0.12, n), 3)
    out["rate_spread"] = ["%.3f" % v for v in spread]
    out["hoepa_status"] = np.where(orig, 2, 3)
    tlc = np.round(np.clip(rng.normal(4200, 1300, n) + np.where(lt == 2, 2400, 0) + amt * 0.004, 900, 22000), 2)
    out["total_loan_costs"] = ["%g" % v for v in tlc]
    oc = np.round(np.clip(rng.normal(1350, 650, n), 0, 9000), 2)
    out["origination_charges"] = ["%g" % v for v in oc]
    term = np.where(port & (rng.random(n) < 0.35), _cat(rng, n, [180, 240, 300], [3, 3, 2]).astype(int),
                    np.where(rng.random(n) < 0.08, 180, 360))
    term = np.where(first, term, _cat(rng, n, [120, 180, 240, 360], [3, 4, 2, 1]).astype(int))
    out["loan_term"] = term
    out["property_value"] = (np.floor(val / 10000) * 10000 + 5000).astype(int)
    out["construction_method"] = D.construction_method.values
    out["occupancy_type"] = D.occupancy_type.values
    out["total_units"] = [str(u) if u <= 4 else ("5-24" if u <= 24 else "25-49") for u in D.total_units]
    inc = np.round(np.clip(amt / rng.uniform(2.4, 4.4, n) / 1000, 14, 900)).astype(int)
    out["income"] = inc
    out["debt_to_income_ratio"] = _cat(rng, n, ["20%-<30%", "30%-<36%", "<20%", "36", "37", "38", "39", "40", "41",
                                                "42", "43", "44", "45", "46", "47", "48", "49", "50%-60%", ">60%"],
                                       [15, 14, 7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3, 3, 6, 1])
    out["applicant_age"] = _cat(rng, n, ["<25", "25-34", "35-44", "45-54", "55-64", "65-74", ">74"],
                                [9, 33, 22, 14, 11, 8, 3])
    out["submission_of_application"] = _cat(rng, n, [1, 2], [88, 12]).astype(int)
    out["initially_payable_to_institution"] = _cat(rng, n, [1, 2], [91, 9]).astype(int)
    aus = np.where(lt == 2, 3, np.where(lt == 4, 4, np.where(port, 6, _cat(rng, n, [1, 2], [62, 38]).astype(int))))
    out["aus-1"] = aus
    den = (D.action_taken.values == 3) | (D.action_taken.values == 7)
    out["denial_reason-1"] = np.where(den, _cat(rng, n, [1, 2, 3, 4, 5, 6, 7, 9], [26, 11, 33, 9, 7, 4, 6, 4]).astype(int),
                                      10)
    out["tract_population"] = [x["pop"] for x in tr]
    out["tract_minority_population_percent"] = [x["minority"] for x in tr]
    out["ffiec_msa_md_median_family_income"] = [W.MSA_INCOME[m][0 if y == 2024 else 1]
                                                for m, y in zip(out["derived_msa-md"], yrs)]
    out["tract_to_msa_income_percentage"] = [x["inc_pct"] for x in tr]
    out["tract_owner_occupied_units"] = [x["owner"] for x in tr]
    out["tract_one_to_four_family_homes"] = [x["one4"] for x in tr]
    out["tract_median_age_of_housing_units"] = [x["age"] for x in tr]
    # what is not reported for records that did not close, and for purchased loans
    for col in COLUMNS:
        if col in out.columns:
            out[col] = out[col].astype(object)
    na = ~orig
    for col in ("interest_rate", "rate_spread", "total_loan_costs", "origination_charges"):
        out.loc[na, col] = "NA"
    out.loc[na, "loan_term"] = np.where(rng.random(int(na.sum())) < 0.6, "360", "NA")
    out.loc[~first, ["total_loan_costs"]] = "NA"
    out.loc[(~first) & orig, "rate_spread"] = "NA"
    bought = (D.action_taken == 6).values
    out.loc[bought, ["submission_of_application", "initially_payable_to_institution"]] = 3
    out.loc[bought, "aus-1"] = 6
    out.loc[bought, ["derived_ethnicity", "derived_race", "derived_sex"]] = ["Ethnicity Not Available",
                                                                              "Race Not Available", "Sex Not Available"]
    out.loc[bought, "applicant_age"] = "8888"
    out.loc[bought, "hoepa_status"] = 3
    ex = D.lei.isin(exempt).values
    for col in ("interest_rate", "rate_spread", "total_loan_costs", "origination_charges", "loan_term",
                "property_value", "combined_loan_to_value_ratio", "debt_to_income_ratio"):
        out[col] = out[col].astype(object)
        out.loc[ex, col] = "Exempt"
    for col in ("submission_of_application", "initially_payable_to_institution", "aus-1", "denial_reason-1",
                "reverse_mortgage", "open-end_line_of_credit", "business_or_commercial_purpose"):
        out[col] = out[col].astype(object)
        out.loc[ex, col] = 1111
    return out[COLUMNS]


def region_rows(w, rng, T, LX):
    """The reporters' records in the eight counties: each simulated home-purchase first lien that closed in 2024 or
    2025 where its lender's geocoding put it, the piggyback seconds, the loans the aggregator bought, and the reporters'
    other applications there."""
    M = w["M"]
    by = {x["id"]: x for x in LX}
    inwin = M.close.map(lambda d: 2024 <= d.year <= 2025)
    rep = M.lender.map(lambda i: by[i]["kind"] == "R")
    A = M[inwin & rep]
    rows = []
    for r in A.itertuples():
        x = by[r.lender]
        base = dict(activity_year=r.close.year, lei=x["lei"], county=r.hmda_county, loan_type=LTYPE[r.ltype],
                    value=r.price, occupancy_type=r.occ, total_units=r.units, construction_method=r.cons,
                    business=1 if (r.occ == 3 and "LLC" in r.buyer) else 2, portfolio=x["ch"] in ("CB", "CU"))
        rows.append(dict(base, action_taken=1, loan_purpose=1, lien_status=1, amount=r.amount))
        if r.second_amt:
            rows.append(dict(base, action_taken=1, loan_purpose=1, lien_status=2, amount=r.second_amt, loan_type=1))
    # the aggregator's purchases from the credit unions and the mortgage company that sell their loans
    sellers = M[inwin & M.lender.isin(["N4", "N10"])].sort_values(["close", "rid"])
    bought = sellers.iloc[np.sort(rng.choice(len(sellers), size=by["AGG"]["buy"], replace=False))]
    for r in bought.itertuples():
        rows.append(dict(activity_year=r.close.year, lei=by["AGG"]["lei"], county=r.hmda_county, loan_type=LTYPE[r.ltype],
                         value=r.price, occupancy_type=r.occ, total_units=r.units, construction_method=r.cons, business=2,
                         portfolio=False, action_taken=6, loan_purpose=1, lien_status=1, amount=r.amount))
    # everything else each reporter books in the eight counties: applications that did not close, refinances,
    # cash-out refinances, home improvement and other purposes
    mix = [((1, 1, 2), 0.020), ((1, 1, 3), 0.115), ((1, 1, 4), 0.090), ((1, 1, 5), 0.012), ((1, 1, 7), 0.008),
           ((31, 1, 1), 0.140), ((31, 1, 3), 0.045), ((31, 1, 4), 0.040), ((32, 1, 1), 0.105), ((32, 1, 3), 0.050),
           ((32, 1, 4), 0.035), ((2, 2, 1), 0.050), ((2, 2, 3), 0.030), ((2, 1, 1), 0.012), ((4, 2, 1), 0.030),
           ((4, 2, 3), 0.015), ((5, 1, 1), 0.004)]
    for x in LX:
        if x["kind"] != "R":
            continue
        home = x["home"] or W.COUNTY_W
        cs = list(home)
        p = np.array([home[c] for c in cs], float)
        p /= p.sum()
        for y in (2024, 2025):
            npur = int(((A.lender == x["id"]) & (A.close.map(lambda d: d.year) == y)).sum())
            for (purpose, lien, action), share in mix:
                k = int(rng.poisson(share * npur * (1.4 if x["ch"] in ("CB", "CU") and purpose in (2, 4) else 1.0)))
                for _ in range(k):
                    c = cs[rng.choice(len(cs), p=p)]
                    v = float(np.exp(rng.normal(np.log(W.PRICE[c] * 1.08), 0.4)))
                    a = v * (rng.uniform(0.55, 0.95) if lien == 1 else rng.uniform(0.05, 0.22))
                    lt = 1 if (lien == 2 or x["ch"] in ("CB", "CU") or rng.random() < 0.6) else int(rng.choice([2, 3, 4]))
                    rows.append(dict(activity_year=y, lei=x["lei"], county=c, loan_type=lt, value=round(v, -2),
                                     occupancy_type=1 if rng.random() < 0.9 else 3, total_units=1, construction_method=1,
                                     business=2, portfolio=x["ch"] in ("CB", "CU"), action_taken=action,
                                     loan_purpose=purpose, lien_status=lien, amount=round(a, -3)))
    D = pd.DataFrame(rows)
    D["tract"] = None
    return D


def background_rows(rng, LX, region):
    """Statewide records outside the eight counties: the service-area reporters' business elsewhere, and every other
    reporter in Kansas (identified by LEI only)."""
    cw = county_weights()
    cs = list(cw)
    p = np.array([cw[c] for c in cs])
    p /= p.sum()
    lenders = []
    for x in LX:
        if x["kind"] == "R":
            n_reg = {y: int(((region.lei == x["lei"]) & (region.activity_year == y)).sum()) for y in (2024, 2025)}
            lenders.append((x["lei"], x["ch"], x["hq"], {y: max(6, int(x["rows"] * 0.45) - n_reg[y]) for y in n_reg}))
    others = rng.pareto(1.25, 265) * 22 + 18
    kinds = rng.choice(["NB", "CB", "CU", "RB"], size=len(others), p=[0.30, 0.45, 0.17, 0.08])
    lrng = np.random.default_rng(W.SEED + 43)
    for v, k in zip(others, kinds):
        lenders.append((W.lei(lrng), str(k), None, {2024: int(v * 0.95), 2025: int(v * 1.05)}))
    rows = []
    for lei, ch, hq, per in lenders:
        local = None
        if hq is not None and hq[1] == "KS":
            local = {"Wichita": "Sedgwick", "Topeka": "Shawnee", "Hutchinson": "Reno", "Junction City": "Geary",
                     "Overland Park": "Johnson", "Salina": None, "Peabody": None, "Emporia": "Lyon",
                     "Hays": "Ellis"}.get(hq[0])
        elif hq is None and ch in ("CB", "CU"):
            local = cs[rng.choice(len(cs), p=p)]
        for y, k in per.items():
            if local:
                cty = np.where(rng.random(k) < 0.62, local, np.array(cs, dtype=object)[rng.choice(len(cs), size=k, p=p)])
            else:
                cty = np.array(cs, dtype=object)[rng.choice(len(cs), size=k, p=p)]
            purpose = _cat(rng, k, [1, 31, 32, 2, 4, 5], [52, 13, 17, 9, 8, 1]).astype(int)
            lien = np.where(np.isin(purpose, [2, 4]) & (rng.random(k) < 0.7), 2, 1)
            lien = np.where((purpose == 1) & (rng.random(k) < 0.03), 2, lien)
            action = _cat(rng, k, [1, 2, 3, 4, 5, 6, 7], [57, 2, 16, 12, 4, 8, 1]).astype(int)
            if ch == "CU" or ch == "CB":
                action = np.where(action == 6, 1, action)
            lt = np.where((lien == 2) | (rng.random(k) < 0.64), 1, _cat(rng, k, [2, 3, 4], [55, 30, 15]).astype(int))
            val = np.exp(rng.normal(np.log(245000), 0.48, k))
            amt = val * np.where(lien == 1, rng.uniform(0.55, 0.97, k), rng.uniform(0.05, 0.2, k))
            units = np.where(rng.random(k) < 0.985, 1, _cat(rng, k, [2, 3, 4, 8, 30], [5, 2, 2, 1, 0.3]).astype(int))
            for j in range(k):
                rows.append((y, lei, cty[j], int(lt[j]), round(float(val[j]), -2), 1 if rng.random() < 0.9 else 3,
                             int(units[j]), 1 if rng.random() < 0.97 else 2, 2, ch in ("CB", "CU"), int(action[j]),
                             int(purpose[j]), int(lien[j]), round(float(amt[j]), -3)))
    D = pd.DataFrame(rows, columns=["activity_year", "lei", "county", "loan_type", "value", "occupancy_type",
                                    "total_units", "construction_method", "business", "portfolio", "action_taken",
                                    "loan_purpose", "lien_status", "amount"])
    D["tract"] = None
    return D


def build(w):
    LX = w["LX"]
    rng = np.random.default_rng(W.SEED + 44)
    T = tracts()
    region = region_rows(w, rng, T, LX)
    region["lei"] = region.lei.astype(str)
    bg = background_rows(rng, LX, region)
    D = pd.concat([region, bg], ignore_index=True)
    exempt = {x["lei"] for x in LX if x["kind"] == "R" and x["ch"] in ("CB", "CU", "RB") and x["rows"] < 700}
    lrng = np.random.default_rng(W.SEED + 45)
    others = [lei for lei in D.lei.unique() if lei not in {x["lei"] for x in LX}]
    exempt |= set(lrng.choice(others, size=len(others) // 3, replace=False))
    out = fill(D, np.random.default_rng(W.SEED + 46), T, exempt)
    # the Data Browser sorts by year, then as the filings came in; we keep the download's order
    order = np.random.default_rng(W.SEED + 47).permutation(len(out))
    out = out.iloc[order]
    out = out.sort_values("activity_year", kind="mergesort").reset_index(drop=True)
    return out, exempt, T
