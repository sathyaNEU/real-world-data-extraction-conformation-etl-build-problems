"""The pack's data files, written from the truth in world.py: the business register extract, the risk screen's
referral list, the summer 2026 quality audit, the regional code crosswalk, the gazette's third-quarter notices and the
distractors."""
import csv
import datetime as dt

import numpy as np

import world as W

FILES = {
    "register": "sar_business_register_extract_2026-09-30.csv",
    "screen": "sar_register_risk_screen_referrals_2026-05.csv",
    "audit": "sar_register_quality_audit_summer_2026.csv",
    "codes": "sar_region_code_crosswalk_2025.csv",
    "gazette": "ardmuir_gazette_company_notices_2026q3.csv",
    "paper": "sar_quality_board_paper_register_revalidation_2027.pdf",
    "costs": "sar_revalidation_cost_estimates_2027.xlsx",
    "survey": "sar_register_user_survey_2025.csv",
    "returns": "sar_annual_return_compliance_2025.csv",
    "dictionary": "sar_data_dictionary.csv",
    "manifest": "sar_extract_manifest_2026-10-08.csv",
}
COMPANY = "Statistics Ardmuir"
REG_COLS = ["record_id", "region", "legal_form", "status", "created_at_utc", "employees_band", "last_updated"]
SCREEN_COLS = ["record_id", "screen_run", "risk_score", "referred"]
AUDIT_COLS = ["audit_id", "record_id", "region_old", "auditor", "audit_date", "outcome"]
CODES_COLS = ["region_old", "region", "region_name", "effective"]
GAZ_COLS = ["notice_id", "record_id", "notice_type", "gazette_date", "company_status_after"]
OLD = {c: "R%02d" % (31 + 3 * i) for i, c in enumerate(W.IDS)}
BAND = {0: "0", 1: "1", 2: "2-4", 5: "5-9", 10: "10-19", 25: "20-49", 50: "50-99", 100: "100+"}


def write_csv(path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])
    return len(rows)


def ids(x):
    rng = np.random.default_rng(W.SEED + 1)
    order = rng.permutation(len(x["recs"]))
    for i, j in enumerate(order):
        x["recs"][j]["rid"] = "SC%07d" % (1204417 + 7 * i)


def utc(t):
    """Ardmuir local time to UTC: British Summer Time from the last Sunday of March to the last Sunday of October."""
    y = t.year
    start = max(dt.datetime(y, 3, d) for d in range(25, 32) if dt.date(y, 3, d).weekday() == 6) + dt.timedelta(hours=1)
    end = max(dt.datetime(y, 10, d) for d in range(25, 32) if dt.date(y, 10, d).weekday() == 6) + dt.timedelta(hours=1)
    return t - dt.timedelta(hours=1) if start <= t < end else t


def register_rows(x):
    rng = np.random.default_rng(W.SEED + 2)
    rows = []
    for r in sorted(x["recs"], key=lambda r: r["rid"]):
        st = "dissolved" if r.get("dissolved") and not r.get("restored") else "active"
        upd = r["created"] + dt.timedelta(days=int(rng.integers(0, max(1, (dt.date(2026, 9, 30) - r["created"]).days + 1))))
        rows.append((r["rid"], r["region"], r["form"], st, utc(r["created_local"]).strftime("%Y-%m-%dT%H:%M:%SZ"),
                     BAND[r["employees"]], upd.isoformat()))
    return rows


def screen_rows(x):
    """The risk screen's May 2026 referral list: the records it flagged, with their scores."""
    rng = np.random.default_rng(W.SEED + 3)
    rows = []
    for r in sorted((r for r in x["recs"] if r["flag"]), key=lambda r: r["rid"]):
        rows.append((r["rid"], "2026-05-04", "%.3f" % float(rng.uniform(0.70, 0.99)), "Y"))
    return rows


AUDITORS = ["SP", "SW", "JT", "LJ", "VO", "AP"]
TYPES = ["1", "2", "3", "4"]       # name, legal form, address, status or activity code


def audit_rows(x):
    """The summer audit: each drawn record checked against its source documents. Outcomes were PASS or FAIL until 30
    June and a numeric code from July (0 no error, 1 to 4 the first field in error)."""
    rng = np.random.default_rng(W.SEED + 4)
    rows = []
    drawn = [r for r in x["recs"] if r["drawn"]]
    order = rng.permutation(len(drawn))
    for i, j in enumerate(order):
        r = drawn[j]
        d = dt.date(2026, 5, 18) + dt.timedelta(days=int(rng.integers(0, 105)))
        if d <= dt.date(2026, 6, 30):
            out = "FAIL" if r["err"] else "PASS"
        else:
            out = TYPES[int(rng.integers(0, 4))] if r["err"] else "0"
        rows.append(("QA26-%05d" % (10011 + 3 * i), r["rid"], OLD[r["region"]], AUDITORS[int(rng.integers(0, 6))],
                     d.isoformat(), out))
    rows.sort(key=lambda t: (t[4], t[0]))
    return rows


def codes_rows():
    return [(OLD[c], c, n, "2025-04-01") for c, n, *_ in W.REGIONS]


def gazette_rows(x):
    """Company notices of the third quarter: a first notice of a proposal to strike off, and two months later the
    notice that the company is struck off and dissolved; a struck-off company dissolved in the quarter usually had its
    first notice in the spring; a few struck off were restored to the register within the quarter."""
    rng = np.random.default_rng(W.SEED + 5)
    rows = []
    x["diss_truth"] = {c: 0 for c in W.IDS}
    for r in sorted((r for r in x["recs"] if r.get("dissolved")), key=lambda r: r["rid"]):
        d2 = r["dissolved"]
        d1 = d2 - dt.timedelta(days=int(rng.integers(56, 70)))
        if d1 >= dt.date(2026, 7, 1):
            rows.append((None, r["rid"], "first notice", d1.isoformat(), "active (proposal to strike off)"))
        rows.append((None, r["rid"], "struck off and dissolved", d2.isoformat(), "dissolved"))
        if d2 <= dt.date(2026, 8, 31) and rng.random() < 0.16:
            # restored to the register on application by a director or creditor
            d3 = d2 + dt.timedelta(days=int(rng.integers(14, 30)))
            rows.append((None, r["rid"], "restored to the register", d3.isoformat(), "active"))
            r["restored"] = True
        else:
            x["diss_truth"][r["region"]] += 1
    # first notices in the quarter for companies to be struck off after it
    pool = [r for r in x["recs"] if not r.get("dissolved") and r["created"] < dt.date(2026, 1, 1)]
    for j in rng.permutation(len(pool))[:int(len(pool) * 0.006)]:
        r = pool[j]
        d1 = dt.date(2026, 8, 1) + dt.timedelta(days=int(rng.integers(0, 60)))
        rows.append((None, r["rid"], "first notice", d1.isoformat(), "active (proposal to strike off)"))
    rows.sort(key=lambda t: (t[3], t[1]))
    return [("GZ-%06d" % (300101 + 4 * i),) + t[1:] for i, t in enumerate(rows)]


SURVEY_COLS = ["user_group", "respondents", "mean_satisfaction", "would_recommend_pct"]
RETURNS_COLS = ["region", "returns_due", "returns_filed", "late_pct"]


def survey_rows():
    return [("statistical producers", 41, "4.1", "61"), ("government departments", 58, "3.8", "54"),
            ("researchers", 112, "3.6", "48"), ("businesses", 203, "3.2", "39")]


def returns_rows(x):
    rng = np.random.default_rng(W.SEED + 6)
    out = []
    for c in W.IDS:
        due = sum(1 for r in x["recs"] if r["region"] == c and r["created"] < dt.date(2025, 1, 1))
        out.append((c, due, int(due * float(rng.uniform(0.82, 0.94))), "%.1f" % float(rng.uniform(11, 34))))
    return out
