"""The pack's data files, cut from the truth: the paid medical claims, the plan's monthly roster, the state's
capitation remittance, the pharmacy claims (the asks), and the member experience survey (a distractor)."""
import csv
import datetime as dt
import functools

import numpy as np

import records as R
import sources as S
import world as W

ROSTER_COLS = ["roster_month", "as_of", "member_id", "medicaid_id", "rate_cell", "pcp_group_id", "county"]
REMIT_COLS = ["remittance_id", "payment_date", "medicaid_id", "rate_cell", "coverage_month", "member_count", "amount"]
CLAIM_COLS = ["claim_id", "member_id", "claim_type", "service_from", "service_to", "billing_npi", "paid_date",
              "paid_amount"]
RX_COLS = ["claim_number", "member_id", "fill_date", "ndc", "quantity", "paid_amount", "processed_at"]
SURVEY_COLS = ["response_id", "pcp_group_id", "survey_wave", "q_getting_care_quickly", "q_rating_personal_doctor",
               "q_rating_health_plan"]


@functools.lru_cache(None)
def everything():
    ms = S.members(np.random.default_rng(W.SEED))
    rec = R.build(np.random.default_rng(W.SEED + 1), ms)
    rx = R.pharmacy(np.random.default_rng(W.RX_SEED), ms)
    return dict(members=ms, rec=rec, rx=rx, ndc=ndc_map(np.random.default_rng(W.SEED + 3)),
                sid=state_ids(np.random.default_rng(W.SEED + 5), ms))


def state_ids(rng, ms):
    """The state's Medicaid recipient id for each plan member id."""
    out, seen = {}, set()
    for x in ms:
        while True:
            v = "%08d%s" % (int(rng.integers(10000000, 99999999)), "ABCDEFGHJK"[int(rng.integers(0, 10))])
            if v not in seen:
                break
        seen.add(v)
        out[x["mid"]] = v
    return out


def ndc_map(rng):
    out = {}
    for c in R.CLASSES:
        for _ in range(int(rng.integers(3, 7))):
            code = "%05d-%04d-%02d" % (int(rng.integers(100, 99999)), int(rng.integers(1, 9999)), int(rng.integers(1, 99)))
            out[code] = c
    return out


def county_of(g):
    return W.GROUPS[g][1]


def roster_rows(x):
    rows = []
    for r in x["rec"]["roster"]:
        rows.append([r["month"].strftime("%Y-%m"), (r["month"] + dt.timedelta(days=4)).isoformat(), r["mid"],
                     x["sid"][r["mid"]], r["cell"],
                     r["group"], county_of(r["group"])])
    rows.sort(key=lambda r: (r[0], r[2]))
    return rows


def remit_rows(x):
    rng = np.random.default_rng(W.SEED + 7)
    rows = []
    rid = {}
    for r in sorted(x["rec"]["remit"], key=lambda r: (r["pay"], r["mid"] == "", str(r["mid"]), r["cov"])):
        k = r["pay"]
        if k not in rid:
            rid[k] = "820-%s-%03d" % (k.strftime("%y%m%d"), int(rng.integers(100, 999)))
        rows.append([rid[k], k.isoformat(), x["sid"][r["mid"]] if r["mid"] else "", r["cell"], r["cov"].strftime("%Y-%m"), r["n"], "%.2f" % r["amt"]])
    return rows


def claim_rows(x):
    rows = [[c["cid"], c["mid"], c["ctype"], c["svc"].isoformat(), c["end"].isoformat(), c["npi"], c["paid"].isoformat(),
             "%.2f" % c["amt"]] for c in x["rec"]["claims"]]
    rows.sort(key=lambda r: (r[6], r[0]))
    return rows


def rx_rows(x):
    by_class = {}
    for code, c in sorted(x["ndc"].items()):
        by_class.setdefault(c, []).append(code)
    rng = np.random.default_rng(W.SEED + 9)
    rows = []
    pick = {}
    for r in x["rx"]:
        key = (r["claim"], r["cls"])
        if key not in pick:
            opts = by_class[r["cls"]]
            pick[key] = opts[int(rng.integers(0, len(opts)))]
        rows.append([r["claim"], r["mid"], r["fill"].isoformat(), pick[key], r["qty"], "%.2f" % r["amt"],
                     r["proc"].strftime("%Y-%m-%d %H:%M:%S")])
    rows.sort(key=lambda r: (r[6], r[0]))
    return [r for r in rows if r[6][:10] <= "2026-10-31"]


def survey_rows(x):
    rng = np.random.default_rng(W.SEED + 11)
    out = []
    n = 610000
    for g in W.GROUPS:
        for _ in range(int(rng.integers(90, 240))):
            n += int(rng.integers(1, 7))
            out.append(["S%d" % n, g, "2025-fall", int(rng.integers(1, 5)), int(rng.integers(4, 11)), int(rng.integers(3, 11))])
    return out


def write_csv(path, cols, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(cols)
        w.writerows(rows)
    return len(rows)
