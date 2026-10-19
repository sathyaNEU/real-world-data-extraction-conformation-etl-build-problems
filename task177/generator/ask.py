"""task177 asks: the rest of the assistant's use in 2026, outside the jobseekers' own contacts.

Employers on the employer portal's assistant widget (built by the vendor's integration partner, which writes its
start and end times in UTC although the export's other channels carry Manitoba time), and the employer line; the
service's own use: advisers in the staff console, the training team's and the digital channels team's accounts on
the claimant channels (typed claimant until the vendor's release 3.4 re-typed them as staff), and the digital
channels team's test employers on the employer portal, registered to Prairie Works Manitoba's own business number.

The truth here is what each ask's golden counts; calc.py recomputes every figure from the shipped files."""
from __future__ import annotations

import datetime as dt

import numpy as np

import common as C
import records as Rc

N_EMPLOYERS = 1600
EMP_RATE = (0.9, 1.35)         # conversations a month per employer: gamma shape and scale (mean about 1.2)
EMP_SEASON = (0.85, 0.90, 1.15, 1.30, 1.30, 1.20, 0.95, 0.85, 1.05, 1.00, 0.95, 0.60)
EMP_HOURS = (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.7, 1.4, 1.7, 1.6, 1.4, 1.1, 1.4, 1.5, 1.4, 1.1, 0.8, 0.70, 0.65,
             0.60, 0.50, 0.35, 0.15)
EMP_WEEKEND = 0.22             # weekend activity relative to a weekday
TEST_EMPLOYERS = 5             # the digital channels team's test employer accounts
TEST_PER_WEEK = 11.0           # their regression conversations a week, more in a release week
INTERNAL_ACCOUNTS = 14         # training practice and test accounts on the claimant channels
INTERNAL_PER_WEEK = 21.0
CONSOLE_PER_WEEKDAY = 52.0     # advisers' conversations in the staff console


def _bns(rng, n):
    nums = set()
    out = []
    while len(out) < n:
        x = int(rng.integers(100000000, 999999999))
        if x in nums or str(x) == C.BN:
            continue
        nums.add(x)
        out.append(str(x))
    return out


def _sessions(rng, conv, start, end_state, p_split, mk):
    dur = int(rng.integers(60, 1100))
    if rng.random() < p_split:
        e1 = start + dt.timedelta(seconds=int(rng.integers(40, 500)))
        idle = e1 + dt.timedelta(minutes=30)
        s2 = idle + dt.timedelta(minutes=int(rng.integers(3, 240)))
        return [mk(conv, 0, start, idle, "timeout"), mk(conv, 1, s2, s2 + dt.timedelta(seconds=dur), end_state)]
    return [mk(conv, 0, start, start + dt.timedelta(seconds=dur), end_state)]


def _end_state(rng):
    u = rng.random()
    return "resolved" if u < 0.62 else ("handoff" if u < 0.86 else "abandoned")


def build_employers(rec):
    rng = C.stream("ask/employers")
    bns = _bns(rng, N_EMPLOYERS)
    users = rng.choice([1, 2, 3, 4, 5], size=N_EMPLOYERS, p=[0.70, 0.18, 0.07, 0.03, 0.02])
    rate = rng.gamma(EMP_RATE[0], EMP_RATE[1], N_EMPLOYERS)
    joined = rng.integers(-400, 330, size=N_EMPLOYERS)          # days from the launch the employer first used it
    accts = [["acc_" + Rc.hexid("employer", bns[e], u, n=10) for u in range(users[e])] for e in range(N_EMPLOYERS)]
    sessions = []
    truth = []           # (local start, kind) per conversation: kind 'employer' or 'test'
    pairs = []
    k = 0
    dl = C.days(C.REC_START, C.REC_END)
    for d in dl:
        wk = 1.0 if d.weekday() < 5 else EMP_WEEKEND
        if d in C.HOLIDAYS:
            wk *= 0.25
        season = EMP_SEASON[d.month - 1]
        dd = (d - C.REC_START).days
        lam = rate * season * wk * 12.0 / 365.25 * 7.0 / (5 + 2 * EMP_WEEKEND) * (joined <= dd)
        n = rng.poisson(lam)
        for e in np.flatnonzero(n):
            for _ in range(int(n[e])):
                h = int(rng.choice(24, p=np.array(EMP_HOURS) / sum(EMP_HOURS)))
                local = dt.datetime.combine(d, dt.time(h)) + dt.timedelta(seconds=int(rng.integers(0, 3600)))
                acct = accts[e][int(rng.integers(0, users[e]))]
                k += 1
                conv = "c_" + Rc.hexid("emp", bns[e], k)
                st = _end_state(rng)
                sessions += _sessions(rng, conv, local, st, 0.08, _emp_mk(rng, acct, bns[e]))
                truth.append((local, "employer", conv))
                if st == "abandoned" and d.weekday() < 5 and 9 <= h < 16 and rng.random() < 0.35:
                    pairs.append((bns[e], local + dt.timedelta(minutes=int(rng.integers(3, 26)))))
    # the digital channels team's regression tests of the employer portal under their own test employers, in
    # office hours and on the evening before each release
    test_accts = ["acc_" + Rc.hexid("pwtest", u, n=10) for u in range(TEST_EMPLOYERS)]
    rel_days = {t.date() for t, _ in Rc.RELEASES[1:]}
    for d in C.days(C.REC_START, C.REC_END):
        if d.weekday() >= 5 or d in C.HOLIDAYS:
            continue
        boost = 3.0 if any(0 <= (r - d).days <= 4 for r in rel_days) else 1.0
        n = rng.poisson(TEST_PER_WEEK / 5.0 * boost)
        for _ in range(n):
            local = dt.datetime.combine(d, dt.time(int(rng.integers(9, 16)))) + dt.timedelta(
                seconds=int(rng.integers(0, 3600)))
            k += 1
            conv = "c_" + Rc.hexid("pwtest", k)
            acct = test_accts[int(rng.integers(0, TEST_EMPLOYERS))]
            sessions += _sessions(rng, conv, local, _end_state(rng), 0.05, _emp_mk(rng, acct, C.BN))
            truth.append((local, "test", conv))
        if (d + dt.timedelta(days=1)) in rel_days:
            for _ in range(int(rng.integers(14, 30))):
                local = dt.datetime.combine(d, dt.time(int(rng.integers(19, 23)))) + dt.timedelta(
                    seconds=int(rng.integers(0, 3600)))
                k += 1
                conv = "c_" + Rc.hexid("pwtest", k)
                acct = test_accts[int(rng.integers(0, TEST_EMPLOYERS))]
                sessions += _sessions(rng, conv, local, _end_state(rng), 0.05, _emp_mk(rng, acct, C.BN))
                truth.append((local, "test", conv))
    rec.sessions_employer = sessions
    rec.employer_truth = truth
    rec.employer_bns = bns
    rec.legs_employer = _employer_line(rec, rng, bns, pairs)


def _emp_mk(rng, acct, bn):
    def mk(conv, j, s, e, st):
        # the partner's widget writes UTC (no zone marker), unlike every other channel in the export
        su, eu = C.to_utc(s), C.to_utc(e)
        return dict(session_id="s_" + Rc.hexid("esess", conv, j), conversation_id=conv, account_ref=acct,
                    account_type="employer", org_ref=bn, channel="employer", call_ref="",
                    started=Rc.iso_local(su), ended=Rc.iso_local(eu), user_turns=int(rng.integers(2, 12)),
                    assistant_turns=int(rng.integers(3, 14)), intent=_emp_intent(rng), end_state=st,
                    release=Rc.release_at(s))
    return mk


EMP_INTENTS = ("job_posting", "wage_subsidy", "hiring_incentive", "account_access", "other")


def _emp_intent(rng):
    return EMP_INTENTS[int(rng.choice(5, p=[0.38, 0.27, 0.15, 0.12, 0.08]))]


def _employer_line(rec, rng, bns, pairs):
    """the employer line: employers' calls, keyed by the business number they key in"""
    legs = []
    seq = [3 * 10 ** 6]
    calls = []
    for d in C.days(C.REC_START, C.REC_END):
        if d.weekday() >= 5 or d in C.HOLIDAYS:
            continue
        n = rng.poisson(46)
        for _ in range(n):
            local = dt.datetime.combine(d, dt.time(8, 30)) + dt.timedelta(seconds=int(rng.integers(0, 8 * 3600)))
            calls.append((local, bns[int(rng.integers(0, len(bns)))]))
    for bn, local in pairs:
        if local.date() <= C.REC_END:
            calls.append((local, bn))
    calls.sort()
    for local, bn in calls:
        new = local >= Rc.CUTOVER
        codes = Rc.NEW if new else Rc.LEGACY
        iid = rec._interaction_id(new, local, seq)
        base = dict(interaction_id=iid, source_system=codes["src"], line_dnis=Rc.LINE_EMPLOYER,
                    caller_ani=str(int(rng.integers(2040000000, 2049999999))), caller_entered=bn, menu_path="2")
        ivr_e = local + dt.timedelta(seconds=int(rng.integers(30, 90)))
        q_e = ivr_e + dt.timedelta(seconds=int(min(rng.exponential(200.0), 1500)) + 5)
        talk = int(rng.gamma(3.0, 110.0)) + 30
        a_e = q_e + dt.timedelta(seconds=talk)
        adviser = ("pw%04d" % (3300 + int(rng.integers(0, 20)))) if new else ("E%02d" % (40 + int(rng.integers(0, 20))))
        disp = codes["resolved"] if rng.random() < 0.88 else codes["callback"]
        if new:
            legs.append(rec._leg(base, 1, codes["ivr"], local, ivr_e, result=codes["completed"]))
            legs.append(rec._leg(base, 2, codes["queue"], ivr_e, q_e, queue=codes["q_employer"], result=codes["answered"]))
            legs.append(rec._leg(base, 3, codes["agent"], q_e, a_e, queue=codes["q_employer"], adviser=adviser,
                                 result=codes["completed"], disposition=disp, talk=talk, hold=0,
                                 wrap=int(rng.gamma(2.0, 28.0)) + 8))
        else:
            legs.append(rec._leg(base, 1, codes["ivr"], local, q_e, queue=codes["q_employer"], result=codes["answered"]))
            legs.append(rec._leg(base, 2, codes["agent"], q_e, a_e, queue=codes["q_employer"], adviser=adviser,
                                 result=codes["completed"], disposition=disp, talk=talk, hold=None,
                                 wrap=int(rng.gamma(2.0, 28.0)) + 8))
    return legs


def build_internal(rec):
    rng = C.stream("ask/internal")
    sessions = []
    truth = []
    k = 0
    # advisers in the staff console
    advisers = ["acc_" + Rc.hexid("console", a, n=10) for a in range(118)]
    for d in C.days(C.REC_START, C.REC_END):
        if d.weekday() >= 5 or d in C.HOLIDAYS:
            continue
        for _ in range(rng.poisson(CONSOLE_PER_WEEKDAY)):
            local = dt.datetime.combine(d, dt.time(8)) + dt.timedelta(seconds=int(rng.integers(0, 10 * 3600)))
            k += 1
            conv = "c_" + Rc.hexid("console", k)
            acct = advisers[int(rng.integers(0, len(advisers)))]
            sessions += _sessions(rng, conv, local, "resolved" if rng.random() < 0.8 else "abandoned", 0.02,
                                  _local_mk(rng, acct, "staff", "console"))
            truth.append((local, "console", conv))
    # training practice accounts and the digital team's test accounts on the claimant app and web
    internal = ["acc_" + Rc.hexid("internal", a, n=10) for a in range(INTERNAL_ACCOUNTS)]
    retype = dt.datetime.combine(C.RETYPE, dt.time(7))
    for d in C.days(C.REC_START, C.REC_END):
        if d.weekday() >= 5 or d in C.HOLIDAYS:
            continue
        # training sessions on Tuesdays and Thursdays, tests through the week
        lam = INTERNAL_PER_WEEK / 5.0 * (2.2 if d.weekday() in (1, 3) else 0.45)
        for _ in range(rng.poisson(lam)):
            local = dt.datetime.combine(d, dt.time(9)) + dt.timedelta(seconds=int(rng.integers(0, 7 * 3600)))
            k += 1
            conv = "c_" + Rc.hexid("internal", k)
            acct = internal[int(rng.integers(0, INTERNAL_ACCOUNTS))]
            atype = "staff" if local >= retype else "claimant"
            chan = "app" if rng.random() < 0.5 else "web"
            st = ("resolved", "handoff", "abandoned")[int(rng.choice(3, p=[0.55, 0.30, 0.15]))]
            sessions += _sessions(rng, conv, local, st, 0.06, _local_mk(rng, acct, atype, chan))
            truth.append((local, "internal", conv))
    rec.sessions_internal = sessions
    rec.internal_truth = truth


def _local_mk(rng, acct, atype, chan):
    def mk(conv, j, s, e, st):
        return dict(session_id="s_" + Rc.hexid("isess", conv, j), conversation_id=conv, account_ref=acct,
                    account_type=atype, org_ref="", channel=chan, call_ref="", started=Rc.iso_local(s),
                    ended=Rc.iso_local(e), user_turns=int(rng.integers(1, 10)), assistant_turns=int(rng.integers(2, 12)),
                    intent=Rc.INTENTS[int(rng.integers(0, len(Rc.INTENTS)))], end_state=st, release=Rc.release_at(s))
    return mk


def golden_counts(rec):
    """the truth the asks owe: per month of 2026 (Manitoba time, a conversation in the month its first session
    starts), employers' conversations, and the service's own staff and test conversations"""
    emp = [0] * 12
    own = [0] * 12
    for local, kind, _ in rec.employer_truth:
        if local.year != 2026:
            continue
        if kind == "employer":
            emp[local.month - 1] += 1
        else:
            own[local.month - 1] += 1
    for local, kind, _ in rec.internal_truth:
        if local.year == 2026:
            own[local.month - 1] += 1
    return emp, own
