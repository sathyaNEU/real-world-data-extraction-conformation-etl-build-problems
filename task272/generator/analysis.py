"""The golden analysis, from the cut pack alone.

The call: each hospital's 2025 first-review decisions, and among those on households within the free-care limit on
their income over the twelve months before applying, the share that left the household owing more than half its
balance (a denial or a 25 percent discount). The extracts record only the 2025 policy's yearly figure, the three months
before the month of application times four; each household's twelve-month income is that figure divided by the factor
of its month of application on the calendar of its kind of work in its region, read from every first-review decision of
2024 and 2025 in that region and kind of work. A hospital qualifies at six percent or more.

Ask A: each hospital's write-offs on its counsellors' 2025 approvals, net of reversals posted by 31 March 2026. A
write-off posts one line on every account an approval covers, each carrying the approval's whole write-off, and posts
under the number the case was opened with, so a household's approval on a later application posts under its first
application's number: each write-off is one amount per number and posting date, credited to the approval of that
household decided last on or before the posting date; a reversal posts on one account at that account's own amount and
is charged to the approval whose write-off on the account it reverses.

Ask B: each hospital's counsellor denials of 2025 for documents not received. The data guide's reason list is the
collaborative's version from 1 July 2025; before then documents not received was code 2 and income above the limit code
1 (the denials that reconsiderations reopen carry code 2 to 30 June and code 1 from 1 July)."""
import collections
import datetime as dt

import common as K
import models as M
import pack as PK


def call(target, rows_=None):
    fr = PK.first_reviews(target, rows_)
    measure = M.golden(fr)
    qualify = [c for c in K.CODES if measure[c] >= K.THRESHOLD]
    return dict(measure=measure, qualify=qualify, count=len(qualify), first_reviews=fr)


def counsellor_approvals(rows_):
    """Every approval a counsellor recorded, first review or reconsideration, keyed (hospital, application), with its
    local decision date and guarantor."""
    out = {}
    for r in rows_:
        if r["outcome"] == "approve" and r["user"] not in PK.SYSTEM:
            out[(r["code"], r["app"])] = dict(when=r["when"].date(), guarantor=r["guarantor"])
    return out


def all_approvals_by_guarantor(rows_):
    by = collections.defaultdict(list)
    for r in rows_:
        if r["outcome"] == "approve":
            by[(r["code"], r["guarantor"])].append((r["when"].date(), r["app"], r["user"] in PK.SYSTEM))
    for v in by.values():
        v.sort()
    return by


def guarantor_of(rows_):
    out = {}
    for r in rows_:
        out[(r["code"], r["app"])] = r["guarantor"]
    return out


def attribute(target, rows_, lines=None):
    """Each write-off event (number, posting date) and each reversal line, credited to the approval that made it."""
    lines = PK.ledger(target) if lines is None else lines
    gof = guarantor_of(rows_)
    gmap = PK.guarantor_map(target)
    inv = {v: k for k, v in gmap.items()}
    byg = all_approvals_by_guarantor(rows_)

    def approvals_for(code, app):
        g = gof.get((code, app))
        if g is None:
            return []
        keys = {g, gmap.get(g, g), inv.get(g, g)} if code == K.MIGRATED else {g}
        out = []
        for k in keys:
            out += byg.get((code, k), [])
        return sorted(out)

    events = {}
    for line in lines:
        if line["adjustment_code"] != "FAWO":
            continue
        key = (line["hospital_code"], line["application_id"], line["posted_date"])
        if key in events:
            continue
        posted = dt.date.fromisoformat(line["posted_date"])
        cands = [a for a in approvals_for(line["hospital_code"], line["application_id"]) if a[0] < posted]
        events[key] = dict(amount=float(line["amount"]), approval=(line["hospital_code"], cands[-1][1]) if cands else None)
    by_account = collections.defaultdict(list)
    for line in lines:
        if line["adjustment_code"] == "FAWO":
            by_account[(line["hospital_code"], line["account_number"])].append(
                (line["posted_date"], events[(line["hospital_code"], line["application_id"], line["posted_date"])]))
    reversals = []
    for line in lines:
        if line["adjustment_code"] != "FAWR":
            continue
        prior = sorted(x for x in by_account[(line["hospital_code"], line["account_number"])]
                       if x[0] < line["posted_date"])
        reversals.append(dict(amount=float(line["amount"]), approval=prior[-1][1]["approval"] if prior else None))
    return events, reversals


def ask_a(target, rows_):
    approved = {k for k, v in counsellor_approvals(rows_).items() if v["when"].year == K.YEAR}
    events, reversals = attribute(target, rows_)
    out = {c: 0.0 for c in K.CODES}
    for e in events.values():
        if e["approval"] in approved:
            out[e["approval"][0]] += e["amount"]
    for v in reversals:
        if v["approval"] in approved:
            out[v["approval"][0]] -= v["amount"]
    return {c: round(v, 2) for c, v in out.items()}


def documents_code(day):
    return 2 if day < K.REASON_SWITCH else 1


def ask_b(target, rows_):
    out = {c: 0 for c in K.CODES}
    for r in rows_:
        if r["outcome"] != "deny" or r["user"] in PK.SYSTEM or r["when"].year != K.YEAR:
            continue
        if r["reason"] == documents_code(r["when"].date()):
            out[r["code"]] += 1
    return out


def run(target):
    rows_ = PK.conformed(target)
    c = call(target, rows_)
    return dict(call=c, ask_a=ask_a(target, rows_), ask_b=ask_b(target, rows_), rows=rows_)
