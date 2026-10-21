"""The golden analysis, from the cut pack alone.

The call: for each hospital, the counsellors' approvals and denials of 2025 by counsellor and local working day in the
order recorded; the pooled contrast over consecutive pairs within a day (the share approved right after a denial less
the share approved right after an approval) less the same contrast's expectation when each day's determinations are
put in every order, its approvals held. A hospital qualifies at six points or more.

Ask A: each hospital's write-offs on its counsellors' 2025 approvals, net of reversals. A write-off line carries the
approval's whole write-off on every account the approval covers (a line exceeds its own account's balance wherever an
approval covers several accounts), so each approval's write-off is taken once; a reversal posts on one account at that
account's amount and each is taken.

Ask B: each hospital's counsellor denials of 2025 for documents not received. The data guide's reason list is the
collaborative's version from 1 July 2025; before then documents not received was code 2 and income above the limit code
1 (the denials that reconsiderations reopen carry code 2 to 30 June and code 1 from 1 July)."""
import common as K
import models as M
import pack as PK


def days_by_hospital(target, rows_=None):
    return PK.counsellor_days(target, rows_)


def call(target, rows_=None):
    days = days_by_hospital(target, rows_)
    measure = {c: M.excess(M._arr(days[c])) for c in K.CODES}
    qualify = [c for c in K.CODES if measure[c] >= K.THRESHOLD]
    return dict(measure=measure, qualify=qualify, count=len(qualify), days=days)


def counsellor_approvals(rows_):
    return {(r["code"], r["app"]) for r in rows_
            if r["outcome"] == "approve" and r["user"] not in PK.SYSTEM and r["when"].year == K.YEAR}


def ask_a(target, rows_):
    approved = counsellor_approvals(rows_)
    wo, rev = {}, {}
    for line in PK.ledger(target):
        key = (line["hospital_code"], line["application_id"])
        if key not in approved:
            continue
        if line["adjustment_code"] == "FAWO":
            wo.setdefault(key, float(line["amount"]))
        else:
            rev[key] = rev.get(key, 0.0) + float(line["amount"])
    out = {c: 0.0 for c in K.CODES}
    for (c, _), v in wo.items():
        out[c] += v
    for (c, _), v in rev.items():
        out[c] -= v
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
