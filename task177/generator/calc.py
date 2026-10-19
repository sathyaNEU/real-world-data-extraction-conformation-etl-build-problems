"""task177 calc: every graded figure computed from the shipped files alone, the way the golden reads them.

The call: rebuild each jobseeker's contacts from the two exports (a call to the claimant line keyed to the case
number entered in the IVR; a conversation in the app or on the web under the case's assistant account; an overflow
transfer is the call it came from, its outcome the voice session's end state), fit the reinforcement-learning model
of channel choice with a separate learning rate for the contacts the jobseeker did not choose, carry each jobseeker
on the register on 3 January 2027 forward from their end-of-record state through the assistant-first weeks (every
call met by release 4.0, resolving at the acceptance test's share) and the eight weeks from 1 March, and read the
share of their own contacts they start in the assistant there.

The asks: employers' conversations and the service's own staff and test conversations, by month of 2026."""
from __future__ import annotations

import datetime as dt
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import common as C   # noqa: E402
import model as M    # noqa: E402

LINE_CLAIMANT = "2049450100"
RESOLVED = {"RS", "RESOLVED"}
AF_DAYS = (C.AF_END - C.AF_START).days + 1
WIN_DAYS = (C.WIN_END - C.WIN_START).days + 1


def parse_utc(s):
    return dt.datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")


READS = (C.F_LEGS, C.F_CONV, C.F_CLAIMS, C.F_XWALK, C.F_PLAN, C.F_ACCEPT, C.F_ORDER, C.F_INVOICES)


def load(target):
    """the rows the golden reads, from the shipped files (READS, and nothing else)"""
    legs = C.read_csv(os.path.join(target, C.F_LEGS))
    sessions = []
    with open(os.path.join(target, C.F_CONV), encoding="utf-8") as fh:
        for line in fh:
            sessions.append(json.loads(line))
    claims = C.read_csv(os.path.join(target, C.F_CLAIMS))
    xwalk = C.read_csv(os.path.join(target, C.F_XWALK))
    return dict(legs=legs, sessions=sessions, claims=claims, xwalk=xwalk)


def contacts(D):
    """each jobseeker's own contacts in start order: (case, start UTC, chose the assistant, transferred, resolved)"""
    # calls to the claimant line, keyed by the case number entered on the call's first leg
    by_call = {}
    for lg in D["legs"]:
        if lg["line_dnis"] == LINE_CLAIMANT:
            by_call.setdefault(lg["interaction_id"], []).append(lg)
    calls = {}
    for iid, legs in by_call.items():
        legs.sort(key=lambda x: int(x["leg_no"]))
        if legs[0]["caller_entered"]:
            calls[iid] = dict(case=legs[0]["caller_entered"], start=legs[0]["start_utc"], legs=legs)
    voice = {}
    convs = {}
    for s in D["sessions"]:
        if s["channel"] == "voice":
            voice[s["call_ref"]] = s
        elif s["channel"] in ("app", "web"):
            convs.setdefault(s["conversation_id"], []).append(s)
    acct_case = {}
    for r in D["xwalk"]:
        if r["detail_type"] == "assistant_account":
            acct_case[r["detail_value"]] = r["case_no"]
    cases = {r["case_no"] for r in D["claims"]}
    rows = []
    for iid, c in calls.items():
        if c["case"] not in cases:
            continue
        legs = c["legs"]
        transferred = any(x["leg_result"] in ("XFR", "transferred") and x["transfer_to"] == "ASKPW-VOICE" for x in legs)
        if transferred:
            v = voice.get(iid)
            res = v is not None and v["end_state"] == "resolved"
        else:
            agent = [x for x in legs if x["leg_type"] in ("AGT", "agent")]
            res = bool(agent) and agent[-1]["disposition"] in RESOLVED
        checkin = legs[0]["menu_path"] == "1>1"
        rows.append((c["case"], parse_utc(c["start"]), False, transferred, res, checkin))
    for cid, ss in convs.items():
        ss = sorted(ss, key=lambda x: x["started"])
        case = acct_case.get(ss[0]["account_ref"])
        if case is None or case not in cases:
            continue
        start = C.to_utc(dt.datetime.fromisoformat(ss[0]["started"]))
        rows.append((case, start, True, False, ss[-1]["end_state"] == "resolved", ss[0]["intent"] == "check_in"))
    rows.sort(key=lambda r: (r[0], r[1]))
    return rows


def population(D, closed_is_first_closed_day=False):
    """jobseekers with a claim open on 3 January 2027, and when each claim opened"""
    pop = {}
    for r in D["claims"]:
        opened = dt.date.fromisoformat(r["opened"])
        closed = dt.date.fromisoformat(r["closed"]) if r["closed"] else None
        if closed_is_first_closed_day and closed is not None:
            closed = closed - dt.timedelta(days=1)
        if opened <= C.POP_DATE and (closed is None or closed >= C.POP_DATE):
            pop[r["case_no"]] = opened
    return pop


def schedule(opened, cycle=14):
    """check-ins due in the assistant-first weeks and in the window, every cycle days from the claim's opening"""
    af = win = 0
    k = 1
    while True:
        due = opened + dt.timedelta(days=cycle * k)
        if due > C.WIN_END:
            break
        if C.AF_START <= due <= C.AF_END:
            af += 1
        elif C.WIN_START <= due <= C.WIN_END:
            win += 1
        k += 1
    return af, win


def inputs(D, rows=None):
    rows = contacts(D) if rows is None else rows
    cid = np.array([r[0] for r in rows])
    choice = np.array([r[2] for r in rows])
    red = np.array([r[3] for r in rows])
    res = np.array([r[4] for r in rows], float)
    S = M.Seq(cid, choice, red, res)
    phone_exp = (~choice) & (~red)
    p_phone = float(res[phone_exp].mean())
    p_over = float(red.sum() / (~choice).sum())
    return S, dict(p_phone=p_phone, p_over=p_over, rows=rows, adhoc_day=adhoc_rate(D, rows))


def adhoc_rate(D, rows):
    """contacts a day per jobseeker other than check-ins, pooled over every claim's open days in the record"""
    n = sum(1 for r in rows if not r[5])
    days = 0
    for r in D["claims"]:
        a = max(dt.date.fromisoformat(r["opened"]), C.REC_START)
        b = min(dt.date.fromisoformat(r["closed"]) if r["closed"] else C.REC_END, C.REC_END)
        days += max((b - a).days + 1, 0)
    return n / days


def forecast(D, spec="split", reps=200, seed=17, S=None, aux=None, P=None, fit_on=None, pop=None):
    """the share of the population's own contacts started in the assistant in the window"""
    if S is None:
        S, aux = inputs(D)
    sp = M.SPECS[spec]
    if P is None:
        P, ll, _ = M.fit(S if fit_on is None else fit_on, sp)
    _, st = M.run(P, S, sp, want_ll=False)
    pop = population(D) if pop is None else pop
    keys = sorted(pop)
    qb = np.array([st["qb"][S.index[k]] if k in S.index else P["q0b"] for k in keys])
    qp = np.array([st["qp"][S.index[k]] if k in S.index else P["q0p"] for k in keys])
    la = np.array([st["last"][S.index[k]] if k in S.index else 0.0 for k in keys])
    sch = np.array([schedule(pop[k], aux.get("cycle", 14)) for k in keys])
    rate = aux.get("adhoc_day", 0.0)
    out = M.simulate(P, sp, qb, qp, la, np.full(len(keys), rate), AF_DAYS, WIN_DAYS, aux["p_new"], aux["p_phone"],
                     aux["p_over"], reps=reps, seed=seed, sched_af=sch[:, 0], sched_free=sch[:, 1],
                     p_chat=aux.get("p_chat"), p_sent_free=aux.get("p_sent_free"))
    out["P"] = P
    out["n_pop"] = len(keys)
    return out


# ------------------------------------------------------------------------------------------------------------ asks
def ask_counts(D, bn, own_bn=True, employer_utc=True, retyped=True, vendor_bn=None):
    """for each month of 2026 (Manitoba time, a conversation in the month its first session started): conversations
    employers held, and conversations the service's own staff and test accounts held. The switches are the handlings
    the golden takes: an employer account registered to the service's own business number is a test account; the
    employer portal's widget records UTC; an account the vendor re-typed as staff was staff before; a staff-console
    account registered to the vendor's business number (vendor_bn, from its invoices) is the vendor's, not ours."""
    first = {}
    for s in D["sessions"]:
        cid = s["conversation_id"]
        if cid not in first or s["started"] < first[cid]["started"]:
            first[cid] = s
    staff_accounts = {s["account_ref"] for s in D["sessions"] if s["account_type"] == "staff"}
    emp = [0] * 12
    own = [0] * 12
    for cid, s in first.items():
        t = dt.datetime.fromisoformat(s["started"])
        if s["channel"] == "employer" and employer_utc:
            t = C.to_local(t)
        if t.year != 2026:
            continue
        mth = t.month - 1
        if s["channel"] == "employer":
            if own_bn and s["org_ref"] == bn:
                own[mth] += 1
            else:
                emp[mth] += 1
        elif s["channel"] == "console":
            if vendor_bn and s["org_ref"] == vendor_bn:
                continue
            own[mth] += 1
        elif s["channel"] in ("app", "web"):
            if s["account_type"] == "staff" or (retyped and s["account_ref"] in staff_accounts):
                own[mth] += 1
    return emp, own


# ------------------------------------------------------------------------------------------- the filed inputs
def pdf_text(path):
    """the text of a shipped PDF, page by page, through one extractor"""
    from pypdf import PdfReader
    r = PdfReader(path)
    return "\n".join(p.extract_text() or "" for p in r.pages)


def filed_inputs(target):
    """the acceptance test's resolved share and the plan's check-in cycle, read from the shipped PDFs"""
    import re
    acc = pdf_text(os.path.join(target, C.F_ACCEPT))
    m = re.search(r"All intents\s+([\d,]+)\s+([\d,]+)\s+([\d.]+)%", acc)
    n, r = int(m.group(1).replace(",", "")), int(m.group(2).replace(",", ""))
    plan = pdf_text(os.path.join(target, C.F_PLAN))
    plan_flat = " ".join(plan.split())
    cyc = re.search(r"checks in every (\d+) days, counted from the day the claim opened", plan_flat)
    order = " ".join(pdf_text(os.path.join(target, C.F_ORDER)).split())
    bn = re.search(r"Business number\s+(\d{9})", order).group(1)
    rel = re.search(r"Ask Prairie Works release (\d+\.\d+)", " ".join(acc.split())).group(1)
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(target, C.F_INVOICES), read_only=True).worksheets[0]
    head = None
    vendor = set()
    for row in ws.iter_rows(values_only=True):
        if head is None:
            head = list(row)
            continue
        vendor.add(str(row[head.index("supplier_gst_hst")]).split()[0][:9])
    return dict(p_new=r / n, accept_n=n, accept_resolved=r, cycle=int(cyc.group(1)), plan_text=plan_flat,
                accept_text=" ".join(acc.split()), order_text=order, bn=bn, release=rel, vendor_bn=vendor.pop())


def solve(target, reps=400):
    """every figure the goldens carry"""
    D = load(target)
    fi = filed_inputs(target)
    rows = contacts(D)
    S, aux = inputs(D, rows)
    aux["p_new"] = fi["p_new"]
    aux["cycle"] = fi["cycle"]
    pop = population(D)
    out = dict(filed=fi, aux=aux, n_pop=len(pop), n_contacts=len(rows))
    fits = {}
    for name in ("split", "one_rate", "teach_nothing", "split_no_persev", "split_persev_exp", "split_q0", "one_rate_q0"):
        P, ll, _ = M.fit(S, M.SPECS[name])
        fits[name] = dict(P=P, ll=ll)
    out["fits"] = fits
    # the gain over one rate that every defensible form of the split model shares (starting values fixed or estimated)
    gains = (fits["split"]["ll"] - fits["one_rate"]["ll"], fits["split_q0"]["ll"] - fits["one_rate_q0"]["ll"])
    out["ll_gain_floor"] = int(min(gains) // 100 * 100)
    g = forecast(D, spec="split", reps=reps, S=S, aux=aux, P=fits["split"]["P"])
    out["share"] = g["share"]
    out["share_af"] = g["share_af"]
    r0 = forecast(D, spec="one_rate", reps=reps // 2, S=S, aux=aux, P=fits["one_rate"]["P"])
    out["share_one_rate"] = r0["share"]
    out["share_af_one_rate"] = r0["share_af"]
    tn = forecast(D, spec="teach_nothing", reps=reps // 2, S=S, aux=aux, P=fits["teach_nothing"]["P"])
    out["share_teach_nothing"] = tn["share"]
    for name in ("split_no_persev", "split_persev_exp"):
        out["share_" + name] = forecast(D, spec=name, reps=reps // 2, S=S, aux=aux, P=fits[name]["P"])["share"]
    # the record: own contacts started in the assistant, by month of 2026 (all jobseekers), and the last eight weeks
    # of the record for the planning population
    by_m = {}
    for r in rows:
        loc = C.to_local(r[1])
        if loc.year != 2026:
            continue
        a = by_m.setdefault(loc.month, [0, 0])
        a[0] += int(r[2]); a[1] += 1
    out["monthly_share"] = {m: a[0] / a[1] for m, a in sorted(by_m.items())}
    cut = C.to_utc(dt.datetime.combine(C.REC_END - dt.timedelta(days=55), dt.time()))
    last = [r for r in rows if r[0] in pop and r[1] >= cut]
    out["share_last8"] = sum(r[2] for r in last) / len(last)
    out["n_redirects"] = int(sum(r[3] for r in rows))
    out["n_calls"] = int(sum(1 for r in rows if not r[2]))
    out["n_conversations"] = int(sum(1 for r in rows if r[2]))
    # what a transfer does to the next choice, against a chosen conversation (the record's own evidence)
    nxt = {}
    prev = None
    for r in rows:
        if prev is not None and prev[0] == r[0]:
            if prev[3]:
                k = "after_transfer_" + ("resolved" if prev[4] else "unresolved")
            elif prev[2]:
                k = "after_chosen_" + ("resolved" if prev[4] else "unresolved")
            else:
                k = "after_call_" + ("resolved" if prev[4] else "unresolved")
            a = nxt.setdefault(k, [0, 0])
            a[0] += int(r[2]); a[1] += 1
        prev = r
    out["next_choice"] = {k: (a[0] / a[1], a[1]) for k, a in nxt.items()}
    out["backtest"] = backtest(D, rows)
    emp, own = ask_counts(D, bn=fi["bn"], vendor_bn=fi["vendor_bn"])
    out["ask_employers"] = emp
    out["ask_own"] = own
    return out


def backtest(D, rows, cut=None):
    """fit each model to the contacts before 1 November 2026 and score the November and December choices"""
    cut = C.to_utc(dt.datetime(2026, 11, 1)) if cut is None else cut
    early = [r for r in rows if r[1] < cut]
    S_e, _ = inputs(D, early)
    S, _ = inputs(D, rows)
    when = np.zeros((S.N, S.L), dtype=bool)
    pos = {}
    for r in rows:
        pos.setdefault(r[0], []).append(r[1] >= cut)
    for k, flags in pos.items():
        i = S.index[k]
        when[i, :len(flags)] = flags
    out = {}
    for name in ("split", "one_rate"):
        P, _, _ = M.fit(S_e, M.SPECS[name])
        ll, st = M.run(P, S, M.SPECS[name], mask=when)
        out[name] = dict(ll=ll, pred=st["pred"] / st["n"], obs=st["obs"] / st["n"], n=int(st["n"]))
    return out
