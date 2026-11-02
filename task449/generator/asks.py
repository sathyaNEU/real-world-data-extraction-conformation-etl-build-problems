"""The three asks, computed from target/ alone, with the handling stops the ceiling script scores.

For each quarter from July 2025 to June 2026: the Workshore clients who started a job in a Schedule A occupation that
Employer Services referred them to (ask 1), how many of them were still working for that employer 90 days after
their start (ask 2), and the average number of days from their referral to their start (ask 3).

Golden handling: a referral's job is its posting's (the old platform's posting number, or the new platform's job id
traced to its legacy posting through the board's migration records); a hire started on the first job_start report
for that client at that employer on or after the referral (a consultant report by employer number, a portal report by
the employer's operating or legal name as typed, compared without case or spacing), and did not start when a
consultant recorded it so; a start was not retained when a job_end report or a Record of Employment (the latest
version of each, the employer read from the business number) shows the job ending before the 90th day; the referral
date of a referral carried to the new platform at go-live is the old platform's.
"""
import datetime as dt
import json
import os
import re
from collections import defaultdict

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
QUARTERS = [(dt.date(2025, 7, 1), dt.date(2025, 9, 30)), (dt.date(2025, 10, 1), dt.date(2025, 12, 31)),
            (dt.date(2026, 1, 1), dt.date(2026, 3, 31)), (dt.date(2026, 4, 1), dt.date(2026, 6, 30))]
QLABEL = ["Jul-Sep 2025", "Oct-Dec 2025", "Jan-Mar 2026", "Apr-Jun 2026"]
RETAIN_DAYS = 90


def norm_name(s):
    return re.sub(r"\s+", " ", str(s)).strip().casefold()


def quarter_of(d):
    for k, (a, b) in enumerate(QUARTERS):
        if a <= d <= b:
            return k
    return None


def load(tgt, cache=None):
    c = cache if cache is not None else {}
    if "ref_old" in c:
        return c
    import openpyxl
    import sys
    sys.path.insert(0, HERE)
    import analysis as A
    # referral logs
    wb = openpyxl.load_workbook(os.path.join(tgt, "workshore_referrals_2025-04-01_2026-02-01.xlsx"), read_only=True)
    rows = list(wb["Referrals"].iter_rows(values_only=True))
    hdr = rows[0]
    old = pd.DataFrame(rows[1:], columns=hdr)
    for col in ("Referred", "Status date", "Start date"):
        old[col] = old[col].map(lambda v: v.date() if hasattr(v, "date") else v)
    c["ref_old"] = old
    new = pd.read_csv(os.path.join(tgt, "workshore_referrals_2026-02-02_2026-11-14.csv"), dtype=str,
                      keep_default_na=False)
    for col in ("referred_on", "status_date", "expected_start"):
        new[col] = new[col].map(lambda v: dt.date.fromisoformat(v) if v else None)
    c["ref_new"] = new
    # postings: employer and occupation for each number on either platform, and the migration crosswalk
    conc = A.read_concordance(tgt)
    o = pd.read_csv(os.path.join(tgt, "workshore_board_events_2025-10-01_2026-02-01.csv"), dtype=str,
                    keep_default_na=False)
    post_emp, post_occ = {}, {}
    for pno, ev, emp, nc in zip(o["posting_no"], o["event"], o["employer_no"], o["noc_2016"]):
        post_emp.setdefault(pno, emp)
        if ev == "PUBLISHED":
            post_occ[pno] = conc[nc]
    legacy = {}
    with open(os.path.join(tgt, "workshore_board_events_2026-02-02_2026-11-14.jsonl"), encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            post_emp.setdefault(r["job_id"], r["employer"])
            if "noc" in r:
                post_occ[r["job_id"]] = r["noc"]
            if r["type"] == "migrated":
                legacy[r["job_id"]] = r["legacy_ref"]
    # postings published before the board events begin: the snapshots and the case workbook carry them
    so = pd.read_csv(os.path.join(tgt, "workshore_live_postings_2025-07_2026-01.csv"), dtype=str)
    for pno, emp, nc in zip(so["posting_no"], so["employer_no"], so["noc_2016"]):
        post_emp.setdefault(pno, emp)
        post_occ.setdefault(pno, conc[nc])
    wb2 = openpyxl.load_workbook(os.path.join(tgt, "employer_services_vacancy_cases.xlsx"), read_only=True)
    for ws in wb2.worksheets:
        for r in ws.iter_rows(min_row=5, values_only=True):
            if not r or r[0] is None:
                continue
            post_emp.setdefault(str(r[1]), str(r[2]))
            post_occ.setdefault(str(r[1]), str(r[3]))
    c["post_emp"], c["post_occ"], c["legacy"] = post_emp, post_occ, legacy
    # employers
    e = pd.read_csv(os.path.join(tgt, "workshore_employer_accounts.csv"), dtype=str)
    c["emp_names"] = {r.employer_number: {norm_name(r.legal_name), norm_name(r.operating_name)} for r in e.itertuples()}
    c["emp_bn"] = dict(zip(e["employer_number"], e["business_number"]))
    # job reports
    jr = []
    with open(os.path.join(tgt, "workshore_client_job_reports_2025-04_2026-11.jsonl"), encoding="utf-8") as f:
        for line in f:
            jr.append(json.loads(line))
    by_client = defaultdict(list)
    for r in jr:
        by_client[r["client_no"]].append(r)
    c["reports"] = by_client
    # ROEs
    wb3 = openpyxl.load_workbook(os.path.join(tgt, "roe_received_workshore_clients_2025-04-01_2026-11-14.xlsx"),
                                 read_only=True)
    rr = list(wb3["ROE"].iter_rows(min_row=5, values_only=True))
    roe = pd.DataFrame([r for r in rr if r and r[0]], columns=["serial", "amends", "client", "bn15", "first", "last",
                                                               "reason", "issued"])
    for col in ("first", "last", "issued"):
        roe[col] = roe[col].map(lambda v: v.date() if hasattr(v, "date") else v)
    roe["amends"] = roe["amends"].fillna("")
    c["roe"] = roe
    c["sched"] = set(A.schedule_a(tgt))
    return c


def hires(c):
    """Every hire on either platform: client, posting (legacy number where it has one), employer, occupation, the
    referral date (ref: the old platform's date for a referral carried at go-live; ref_record: the date on the
    record that shows the hire), the start date the referral records."""
    old, new, legacy = c["ref_old"], c["ref_new"], c["legacy"]
    pending = {}
    for r in old.itertuples(index=False):
        if r[4] == "Referred":
            pending[(r[2], r[1])] = r[3]
    out = []
    for r in old.itertuples(index=False):
        if r[4] == "Hired":
            out.append({"client": r[2], "post": r[1], "ref": r[3], "ref_record": r[3], "planned": r[6],
                        "hired": r[5]})
    for r in new.itertuples(index=False):
        if r.status != "Hired":
            continue
        post = legacy.get(r.job_id, r.job_id)
        ref = pending.get((r.client_id, post), r.referred_on)
        out.append({"client": r.client_id, "post": post, "job_id": r.job_id, "ref": ref, "ref_record": r.referred_on,
                    "planned": r.expected_start, "hired": r.status_date})
    for h in out:
        h["emp"] = c["post_emp"].get(h["post"]) or c["post_emp"].get(h.get("job_id"))
        h["occ"] = c["post_occ"].get(h["post"]) or c["post_occ"].get(h.get("job_id"))
    return out


def report_matches(c, client, emp, kind, names=True):
    out = []
    nm = c["emp_names"].get(emp, set())
    for r in c["reports"].get(client, []):
        if r["event"] != kind:
            continue
        if "employer_no" in r:
            ok = r["employer_no"] == emp
        elif not names:
            ok = False
        else:
            ok = norm_name(r["employer_name"]) in nm
        if ok:
            out.append(dt.date.fromisoformat(r["date"]))
    return sorted(out)


def starts(c, route="golden", carry="original"):
    """The starts that count, one per hire: (client, emp, start date, referral date).

    route 'golden' reads the job reports (both channels); 'referral' takes every hire at the start date its referral
    records; 'consultant_only' reads only the reports that carry an employer number. carry 'original' dates a referral
    carried at go-live from the old platform, 'record' from the record that shows the hire."""
    out = []
    for h in hires(c):
        if h["occ"] not in c["sched"]:
            continue
        ref = h["ref"] if carry == "original" else h["ref_record"]
        if route == "referral":
            if h["planned"] is not None:
                out.append((h["client"], h["emp"], h["planned"], ref))
            continue
        names = route != "consultant_only"
        st = [d for d in report_matches(c, h["client"], h["emp"], "job_start", names=names) if d >= h["ref"]]
        if st:
            out.append((h["client"], h["emp"], st[0], ref))
    return out


def separated_before(c, client, emp, start, sources=("reports", "roe"), roe_versions="latest", roe_key="employer"):
    limit = start + dt.timedelta(days=RETAIN_DAYS - 1)
    if "reports" in sources:
        for d in report_matches(c, client, emp, "job_end"):
            if start <= d <= limit:
                return True
    if "roe" in sources:
        roe = c["roe"]
        if "roe_by_client" not in c:
            g = defaultdict(list)
            superseded = set(roe["amends"][roe["amends"] != ""])
            for r in roe.itertuples(index=False):
                g[r.client].append((r, r.serial in superseded))
            c["roe_by_client"] = g
        bn = c["emp_bn"].get(emp)
        for r, sup in c["roe_by_client"].get(client, []):
            if roe_versions == "latest" and sup:
                continue
            if roe_key == "employer" and str(r.bn15)[:9] != bn:
                continue
            if roe_key == "employer" and r.first < start:
                continue
            if start <= r.last <= limit:
                return True
    return False


def compute(tgt, cache=None, start_route="golden", sep_sources=("reports", "roe"), roe_versions="latest",
            roe_key="employer", carry="original"):
    c = load(tgt, cache)
    st = starts(c, start_route, carry)
    n = [0] * 4
    kept = [0] * 4
    days = [[] for _ in range(4)]
    for cl, e, s, r in st:
        q = quarter_of(s)
        if q is None:
            continue
        n[q] += 1
        days[q].append((s - r).days)
        if not separated_before(c, cl, e, s, sep_sources, roe_versions, roe_key):
            kept[q] += 1
    avg = [sum(x) / len(x) if x else float("nan") for x in days]
    return {"starts": n, "retained": kept, "avg_days": avg}


def golden(tgt, cache=None):
    return compute(tgt, cache)


if __name__ == "__main__":
    import sys
    tgt = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    cache = {}
    g = golden(tgt, cache)
    print("golden", g)
    for name, kw in [("referral route", dict(start_route="referral", sep_sources=("reports",), carry="record")),
                     ("consultant only", dict(start_route="consultant_only")),
                     ("reports-only separations", dict(sep_sources=("reports",))),
                     ("roe-only separations", dict(sep_sources=("roe",))),
                     ("roe originals", dict(roe_versions="all")),
                     ("roe by client", dict(roe_key="client")),
                     ("record referral dates", dict(carry="record"))]:
        print(name, compute(tgt, cache, **kw))
