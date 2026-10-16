"""The shipped tables, from the clean truth: the two claims systems' weekly counts by region, the release of
8 October 2026, the monthly program statistics, the regions and localities, the public holidays, the industry code
list and the Statistics Office's concordance, and the two series the call never reads (the labour force survey's
regional unemployment and the online job advertisements index). File names live here; the writers are in docs.py."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K
import industry as I
import notices as N

# ---------------------------------------------------------------------------------------------------- file names
F_LEGACY = "brs_weekly_initial_claims_2013-12-29_2021-06-20.csv"
F_CURRENT = "uics_weekly_initial_claims_by_region_2021-06-27_2026-09-27.csv"
F_RELEASE = "ui_weekly_claims_release_2026-10-08.pdf"
F_PROGRAM = "ui_program_statistics_2026-09.xlsx"
F_NOTES = "ui_claims_statistics_technical_notes_2026-07.pdf"
F_REGIONS = "regions_territorial_authorities_localities.csv"
F_HOLIDAYS = "public_holidays_2014-2027.csv"
F_PORTAL = "employer_portal_notices_export_2026-10-07.csv"
F_REGISTER = "es_layoff_notice_register_2025-26.xlsx"
F_CASES = "es_case_notes_2026-07-01_2026-10-07.csv"
F_CUBE = "ic_open_data_by_industry_2023-2026.csv"
F_CODES = "uib_industry_divisions_2026.csv"
F_CONCORD = "sic_2006_sic_2023_concordance.xlsx"
F_LFS = "lfs_regional_unemployment_2014q1-2026q2.csv"
F_ADS = "online_job_ads_index_weekly_2019-2026.json"

F_LOG = "desk_data_log_2026-10-08.csv"

MAIN_FILES = [F_LEGACY, F_CURRENT, F_RELEASE, F_PROGRAM, F_NOTES, F_REGIONS, F_HOLIDAYS]
CONTEXT_FILES = [F_LOG]
ASK_A_FILES = [F_PORTAL, F_REGISTER, F_CASES, F_REGIONS, F_NOTES]
ASK_B_FILES = [F_CUBE, F_CODES, F_CONCORD, F_NOTES]
DISTRACTORS = [F_LFS, F_ADS]

LEGACY_COLS = ["WEEK_COMMENCING", "REGION_CD", "NEW_CLAIMS", "ADDL_CLAIMS", "INITIAL_CLAIMS"]
CURRENT_COLS = ["claims_week_start", "claims_week_end", "region", "new_claims", "additional_claims", "initial_claims",
                "count_status", "first_reported_initial_claims"]
CUBE_COLS = ["week", "region", "division", "claim_type", "claims"]
REGION_COLS = ["region_no", "region", "region_code", "ta_code", "territorial_authority", "locality", "postcode_from",
               "postcode_to"]

SHIP_FIRST_SUNDAY = K.FIRST_SUNDAY            # the legacy file opens with the claims week of 29 December 2013
STATS_FIRST_MONTH = (2014, 1)                 # the program statistics open with January 2014


def ship_index(T):
    """Indices of the weeks the pack carries: 29 December 2013 to 27 September 2026 (ended 3 October)."""
    return [T.idx[s] for s in T.sundays if SHIP_FIRST_SUNDAY <= s <= K.ASOF_LAST_SUNDAY]


def latest(T):
    return T.idx[K.ASOF_LAST_SUNDAY]


def week_counts(T, r, i):
    """(new, additional, initial) as the pack carries the week: revised, or at the advance count for the latest."""
    if i == latest(T):
        n, a = int(T.adv_new[r][i]), int(T.adv_add[r][i])
    else:
        n, a = int(T.new[r][i]), int(T.additional[r][i])
    return n, a, n + a


# ---------------------------------------------------------------------------------------------------- weekly files
def legacy_rows(T):
    """The Benefit Records System's weekly extract: the claims week by its Sunday, day first; regions by code, in code
    order; final counts."""
    rows = []
    order = sorted(K.REGIONS, key=lambda r: K.LEGACY_CODE[r])
    for i in ship_index(T):
        s = T.sundays[i]
        if s > K.LEGACY_LAST_SUNDAY:
            continue
        for r in order:
            n, a, ic = week_counts(T, r, i)
            rows.append([s.strftime("%d/%m/%Y"), K.LEGACY_CODE[r], n, a, ic])
    return rows


def current_rows(T):
    rows = []
    li = latest(T)
    for i in ship_index(T):
        s = T.sundays[i]
        if s < K.CURRENT_FIRST_SUNDAY:
            continue
        for r in K.REGIONS:
            n, a, ic = week_counts(T, r, i)
            rows.append([s.isoformat(), K.saturday(s).isoformat(), r, n, a, ic, "Advance" if i == li else "Revised",
                         int(T.advance[r][i])])
    return rows


def release(T):
    """The figures of the release of Thursday 8 October 2026."""
    li = latest(T)
    pi = li - 1
    yi = T.idx[K.ASOF_LAST_SUNDAY - dt.timedelta(days=364)]
    out = dict(rows=[])
    for r in K.REGIONS:
        out["rows"].append(dict(region=r, adv=int(T.advance[r][li]), prev_rev=int(T.revised[r][pi]),
                                prev_adv=int(T.advance[r][pi]), year_ago=int(T.revised[r][yi])))
    tot = lambda k: sum(x[k] for x in out["rows"])
    out.update(adv=tot("adv"), prev_rev=tot("prev_rev"), prev_adv=tot("prev_adv"), year_ago=tot("year_ago"))
    four = [sum(int(T.revised[r][j]) for r in K.REGIONS) for j in range(li - 3, li)] + [out["adv"]]
    out["avg4"] = sum(four) / 4.0
    out["weeks_claimed_prev"] = None
    return out


# ---------------------------------------------------------------------------------------------------- program data
def payments(T):
    """First payments, weeks claimed and benefits paid by claims week and region: the claimants paid from the eligible
    new claims and the additional claims, a few weeks after the claim, the stock of claimants they join, and what it is
    paid at the weekly benefit of the year and region."""
    n = len(T.sundays)
    lags = (0.46, 0.34, 0.14, 0.06)
    out = {}
    rf = {"Northern": 0.97, "Capital": 1.08, "Eastern": 0.96, "Midlands": 1.00, "Western": 0.99, "Southern": 0.95,
          "Coastal": 0.97, "Island": 0.93}
    for r in K.REGIONS:
        g = K.rng("payments", r)
        fp = np.zeros(n + 6)
        for i in range(n):
            el = int(T.new[r][i] - T.inelig[r][i])
            pay = int(g.binomial(el, 0.884)) + int(g.binomial(int(T.additional[r][i]), 0.817))
            parts = g.multinomial(pay, lags)
            for k, v in enumerate(parts):
                fp[i + 1 + k] += v
        fp = fp[:n]
        stock = np.zeros(n)
        wc = np.zeros(n, dtype=int)
        ben = np.zeros(n)
        s0 = float(np.mean(fp[8:60])) * 14.5
        st = s0
        for i in range(n):
            sun = T.sundays[i]
            doy = (sun + dt.timedelta(days=3)).timetuple().tm_yday
            ex = 0.069 * (1.0 + 0.11 * math.cos(2 * math.pi * (doy - 300) / 365.25)) * math.exp(g.normal(0, 0.035))
            st = st * (1.0 - ex) + fp[i]
            stock[i] = st
            wc[i] = int(round(st * (1.0 - 0.012 * K.working_days_lost(sun)) + g.normal(0, 0.004 * st)))
            yrs = (sun - dt.date(2014, 1, 1)).days / 365.25
            awb = 405.0 * 1.0215 ** yrs * rf[r] * math.exp(g.normal(0, 0.0035))
            ben[i] = wc[i] * awb / 1000.0
        out[r] = dict(fp=fp.astype(int), wc=wc, ben=ben)
    return out


def transitional(T, W_ind):
    """Transitional claims by claims week and region: the cube's own from 2023, the claims system's before."""
    n = len(T.sundays)
    out = {r: np.zeros(n, dtype=int) for r in K.REGIONS}
    cube_weeks = set(W_ind["weeks"])
    for r in K.REGIONS:
        g = K.rng("transitional", r)
        for i, s in enumerate(T.sundays):
            if s in cube_weeks:
                out[r][i] = sum(W_ind["cells"][(s, r, c)][2] for c in W_ind["codes"])
            else:
                out[r][i] = int(g.poisson(I.T_SHARE * T.new[r][i]))
    return out


MEASURES = ["new", "additional", "transitional", "determinations", "eligible", "ineligible", "first_payments",
            "weeks_claimed", "benefits"]


def months_of(T):
    """Claims-week months carried by the program statistics, January 2014 to September 2026, with their weeks."""
    out = {}
    for i in ship_index(T):
        s = T.sundays[i]
        key = (s.year, s.month)
        if key < STATS_FIRST_MONTH:
            continue
        out.setdefault(key, []).append(i)
    return out


def program(T, W_ind):
    """Each claims-week month and region's figures, the month's weeks summed; the latest week at its advance count."""
    pay = payments(T)
    tr = transitional(T, W_ind)
    li = latest(T)
    # a few new claims are withdrawn by the claimant (back at work) before they are determined; they come from the
    # claims that would have been found eligible, so the ineligible determinations are the world's own
    wd = {}
    for r in K.REGIONS:
        g = K.rng("withdrawn-before-determination", r)
        wd[r] = [int(g.binomial(max(0, int(T.new[r][i] - T.inelig[r][i])), 0.0031)) for i in range(len(T.sundays))]
    data = {}
    for key, idx in months_of(T).items():
        for r in K.REGIONS:
            m = dict.fromkeys(MEASURES, 0)
            ben = 0.0
            for i in idx:
                n, a, _ = week_counts(T, r, i)
                inel = int(T.adv_inelig[r][i]) if i == li else int(T.inelig[r][i])
                w = min(wd[r][i], max(0, n - inel))
                m["new"] += n
                m["additional"] += a
                m["transitional"] += int(tr[r][i])
                m["determinations"] += n - w
                m["ineligible"] += inel
                m["eligible"] += n - w - inel
                m["first_payments"] += int(pay[r]["fp"][i])
                m["weeks_claimed"] += int(pay[r]["wc"][i])
                ben += pay[r]["ben"][i]
            m["benefits"] = int(round(ben))
            data[(key, r)] = m
    return data


def fiscal_years(T):
    """The fiscal years the workbook carries, each with its months (July to June), in order."""
    out = {}
    for key in sorted(months_of(T)):
        fy = K.fiscal_year(dt.date(key[0], key[1], 1))
        out.setdefault(fy, []).append(key)
    return out


LEGACY_FY_LAST = "FY2020-21"   # the Benefit Records System's report layout runs to June 2021


# ---------------------------------------------------------------------------------------------------- lookups
def region_rows():
    rows = []
    for code, ta, reg, p0, p1, towns in N.TAS:
        for k, t in enumerate(towns):
            v = N.TOWN[t]
            rows.append([K.REGION_NO[reg], reg, K.LEGACY_CODE[reg], code, ta, t, v["pc0"], v["pc0"] + 9])
    return rows


def holiday_rows():
    rows = []
    for y in range(2014, 2028):
        for d, nm in K.holidays(y):
            rows.append([d.isoformat(), d.strftime("%A"), nm])
    return rows


def code_list_rows():
    return [[c, I.SIC2023[c][0], I.SIC2023[c][1], I.G[I.SIC2023[c][1]]] for c in sorted(I.SIC2023)]


def concordance_rows():
    """The Statistics Office's division-level concordance from SIC 2006 to SIC 2023, one row per pair."""
    rows = []
    into = {}
    for c06, (t, succ, sh) in I.SIC2006.items():
        for c23 in succ:
            into.setdefault(c23, []).append(c06)
    for c06 in sorted(I.SIC2006):
        t, succ, sh = I.SIC2006[c06]
        for c23 in succ:
            if len(succ) == 1 and len(into[c23]) == 1:
                kind = "1:1"
            elif len(succ) > 1:
                kind = "1:n (split)"
            else:
                kind = "n:1 (merged)"
            rows.append([c06, t, c23, I.SIC2023[c23][0], kind])
    return rows


# ---------------------------------------------------------------------------------------------------- the two series
# the call never reads
def lfs_rows(T):
    """The labour force survey's quarterly regional unemployment, January to March 2014 to April to June 2026 (the
    July to September survey is published in November)."""
    g = K.rng("lfs")
    rows = []
    lf0 = {"Northern": 642.0, "Capital": 1398.0, "Eastern": 566.0, "Midlands": 829.0, "Western": 531.0,
           "Southern": 418.0, "Coastal": 331.0, "Island": 181.0}
    off = {"Northern": 0.35, "Capital": -0.55, "Eastern": 0.45, "Midlands": 0.05, "Western": 0.2, "Southern": 0.6,
           "Coastal": 0.4, "Island": 0.75}
    q = (2014, 1)
    k = 0
    noise = {r: 0.0 for r in K.REGIONS}
    while q <= (2026, 2):
        y, n_ = q
        mid = dt.date(y, 3 * n_ - 1, 15)
        lvl = sum(K.REGION_SHARE[r] for r in K.REGIONS)
        idx = [i for i, s in enumerate(T.sundays) if K.quarter_of(s) == q]
        claims = float(np.mean([T.nat_revised[i] for i in idx]))
        base = 3.1 + 0.000165 * claims
        for r in K.REGIONS:
            noise[r] = 0.6 * noise[r] + g.normal(0, 0.16)
            lf = lf0[r] * (1.0 + 0.0105 * k / 4.0) * math.exp(g.normal(0, 0.004))
            seas = 0.18 * math.cos(2 * math.pi * (n_ - 3) / 4.0)
            rate = max(2.1, base + off[r] + seas + noise[r])
            un = lf * rate / 100.0
            rate_sa = rate - seas + g.normal(0, 0.03)
            rows.append(["%dQ%d" % q, r, "%.1f" % lf, "%.1f" % un, "%.1f" % (100.0 * un / lf), "%.1f" % rate_sa])
        q = K.next_quarter(q)
        k += 1
    return rows


def ads_series(T):
    """The online job advertisements index by week and region, from the week ending 6 January 2019 (2019 = 100)."""
    g = K.rng("job-ads")
    first = dt.date(2019, 1, 6)
    weeks = [first + dt.timedelta(days=7 * k) for k in range(0, 2000) if first + dt.timedelta(days=7 * k) <= dt.date(2026, 10, 4)]
    out = []
    level = {r: 0.0 for r in K.REGIONS}
    trend = {"Western": 0.010, "Coastal": 0.012, "Island": 0.009, "Capital": 0.004, "Midlands": 0.006,
             "Northern": 0.003, "Eastern": 0.002, "Southern": 0.004}
    raw = {r: [] for r in K.REGIONS}
    for w in weeks:
        yrs = (w - first).days / 365.25
        doy = w.timetuple().tm_yday
        for r in K.REGIONS:
            level[r] = 0.92 * level[r] + g.normal(0, 0.018)
            shock = 0.0
            if dt.date(2020, 3, 22) <= w <= dt.date(2020, 9, 30):
                shock = -0.42 * math.exp(-((w - dt.date(2020, 4, 26)).days / 60.0) ** 2) - 0.08
            boom = 0.0
            if r in ("Western", "Coastal", "Island") and w >= dt.date(2024, 9, 1):
                boom = 0.16 * min(1.0, (w - dt.date(2024, 9, 1)).days / 200.0)
                if w >= dt.date(2026, 4, 1):
                    boom -= 0.30 * min(1.0, (w - dt.date(2026, 4, 1)).days / 120.0)
            x = trend[r] * yrs + 0.07 * math.cos(2 * math.pi * (doy - 40) / 365.25) + shock + boom + level[r]
            raw[r].append(math.exp(x))
    for r in K.REGIONS:
        base = float(np.mean([v for w, v in zip(weeks, raw[r]) if w.year == 2019]))
        for w, v in zip(weeks, raw[r]):
            out.append(dict(week_ending=w.isoformat(), region=r, index=round(100.0 * v / base, 1)))
    return out


# ---------------------------------------------------------------------------------------------------- the desk's log
LOG_COLS = ["file", "from", "received", "covers", "note"]
IR = "UIB Employer Services, information request IR 26/0412"


def log_rows():
    """The economics desk's working record of where each file in the folder came from, kept as files came in (by the
    desk's economist, with the odd entry by the senior economist)."""
    return [
        [F_LEGACY, "UIB open data archive", "2021-07-09", "claims wks 29/12/2013-20/06/2021, region codes",
         "saved after the BRS switch-off"],
        [F_CURRENT, "UIB open data", "2026-10-08", "claims wks 27/06/2021-27/09/2026", "TH 08:41, after the release"],
        [F_RELEASE, "UIB website", "2026-10-08", "wk ended 3 Oct", "printed for the morning meeting"],
        [F_PROGRAM, "UIB website", "2026-10-08", "Jan 2014-Sep 2026", "Sept provisional"],
        [F_NOTES, "UIB website", "2026-07-22", "", "July 2026 rev"],
        [F_REGIONS, "UIB open data", "2025-02-11", "", ""],
        [F_HOLIDAYS, "govt holidays page", "2026-01-12", "2014-2027", "observed dates"],
        [F_PORTAL, IR, "2026-10-07", "portal notices at 7/10", "came through 4.50pm, ES ran the export"],
        [F_REGISTER, "IR 26/0412", "2026-10-07", "email notices Jul 2025-Jun 2026", ""],
        [F_CASES, "IR 26/0412", "2026-10-07", "1/7-7/10/2026", "officers by initials only"],
        [F_CUBE, "UIB open data", "2026-10-08", "claims wks from 1 Jan 2023", "same pull as the uics file"],
        [F_CODES, "UIB open data", "2026-02-03", "divisions and groups", ""],
        [F_CONCORD, "Statistics Office", "2025-11-20", "divisions", "v1.2"],
        [F_LFS, "Statistics Office", "2026-08-12", "2014Q1-2026Q2", "Jul-Sep qtr out 11 Nov"],
        [F_ADS, "Stats Office", "2026-10-08", "wks ending 6/1/2019-4/10/2026", "experimental. SB wanted it in the folder"],
    ]
