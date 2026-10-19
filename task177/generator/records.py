"""task177 records: the world (world.py) written the way each of Prairie Works Manitoba's systems records it.

The telephony platform's interaction-leg export (UTC; the legacy platform's history to 6 July 2026 loaded with its
own codes), the assistant vendor's session export (Manitoba local time), the case system's claims register and its
contact-details history, and around them the employers' and the service's own use of the assistant, the workforce
team's overflow log and the post-contact survey. Every random draw comes from a named stream."""
from __future__ import annotations

import datetime as dt
import hashlib

import numpy as np

import common as C
import world as W

LINE_CLAIMANT = "2049450100"
LINE_EMPLOYER = "2049450200"
VOICE_TARGET = "ASKPW-VOICE"
CUTOVER = dt.datetime(2026, 7, 6, 6, 0)          # local; legs from here are the new platform's own
LEGACY = dict(src="AVX", ivr="ACD", agent="AGT", xfer="XFR", answered="ANS", abandoned="ABN", transferred="XFR",
              completed="CMP", released="REL", resolved="RS", callback="CB",
              q_claimant="Q_CLM", q_general="Q_GEN", q_employer="Q_EMP")
NEW = dict(src="NLC", ivr="ivr", queue="queue", agent="agent", xfer="transfer", answered="answered",
           abandoned="abandoned", transferred="transferred", completed="completed", released="released",
           resolved="RESOLVED", callback="CALLBACK_BOOKED",
           q_claimant="Claimant Services", q_general="General Enquiries", q_employer="Employer Services")
OFFICES = (("Winnipeg Central", 0.30), ("Winnipeg North", 0.18), ("Winnipeg South", 0.16), ("Brandon", 0.09),
           ("Steinbach", 0.06), ("Selkirk", 0.05), ("Portage la Prairie", 0.05), ("Thompson", 0.04), ("Dauphin", 0.04),
           ("The Pas", 0.03))
PROGRAMS = (("Employment and Income Assistance", 0.62), ("Job Seeker Support", 0.38))
INTENTS = ("check_in", "payment_status", "report_earnings", "appointment", "documents", "other")
ADHOC_MIX = (0.0, 0.36, 0.22, 0.18, 0.14, 0.10)
MENU = {"check_in": "1", "payment_status": "2", "report_earnings": "3", "appointment": "4", "documents": "5",
        "other": "0"}
RELEASES = ((dt.datetime(2026, 1, 5, 0, 0), "3.1.0"), (dt.datetime(2026, 2, 23, 7, 0), "3.1.2"),
            (dt.datetime(2026, 5, 11, 7, 0), "3.2.0"), (dt.datetime(2026, 7, 13, 7, 0), "3.3.0"),
            (dt.datetime(2026, 9, 14, 7, 0), "3.4.0"), (dt.datetime(2026, 11, 16, 7, 0), "3.4.2"))


def hexid(*parts, n=12):
    return hashlib.sha256("/".join(str(p) for p in parts).encode()).hexdigest()[:n]


def release_at(local):
    r = RELEASES[0][1]
    for t, v in RELEASES:
        if local >= t:
            r = v
    return r


def minute_to_local(start_date, m):
    return dt.datetime.combine(start_date, dt.time()) + dt.timedelta(minutes=int(m))


def iso_z(t):
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def iso_local(t):
    return t.strftime("%Y-%m-%dT%H:%M:%S")


class World:
    """the clean truth of 2026, built once"""

    def __init__(self):
        self.claims = W.Claims()
        self.ct = W.Contacts(self.claims)
        self.P = dict(W.LEARN)
        self.R = W.run_learning(self.claims, self.ct, self.P)
        cl = self.claims
        self.pop = np.flatnonzero((cl.opened <= np.datetime64(C.POP_DATE)) & (cl.closed > np.datetime64(C.POP_DATE)))


class Records:
    def __init__(self, world):
        self.w = world
        self._minute_ids = {}
        self._claims()
        self._claimant_contacts()
        self._general_calls()
        self._employers()
        self._internal()
        self._survey()

    # ------------------------------------------------------------------------------------------------ the register
    def _claims(self):
        cl = self.w.claims
        rng = C.stream("records/claims")
        nums = rng.choice(np.arange(41000000, 49999999), size=cl.n, replace=False)
        self.case_no = np.array(["%08d" % x for x in nums])
        offices = [o for o, _ in OFFICES]
        self.office = rng.choice(len(offices), size=cl.n, p=[p for _, p in OFFICES])
        self.program = rng.choice(len(PROGRAMS), size=cl.n, p=[p for _, p in PROGRAMS])
        self.offices = offices
        rows = []
        order = np.lexsort((self.case_no, cl.opened))
        for k, i in enumerate(order):
            closed = cl.closed[i]
            closed_d = closed.astype(dt.date)
            shown = "" if closed_d > C.REC_END else (closed_d - dt.timedelta(days=1)).isoformat()   # last open day
            rows.append(dict(case_no=self.case_no[i], claim_id="CLM-%s-%05d" % (str(cl.opened[i])[:4], k + 1),
                             program=PROGRAMS[self.program[i]][0], office=offices[self.office[i]],
                             opened=str(cl.opened[i]), closed=shown))
        self.register = rows

    # --------------------------------------------------------------------------------- jobseekers' own contacts
    def _claimant_contacts(self):
        w = self.w
        ct, R, cl = w.ct, w.R, w.claims
        rng = C.stream("records/claimant_contacts")
        m = ct.m
        intents = np.where(ct.kind, 0, rng.choice(len(INTENTS), size=m, p=ADHOC_MIX))
        self.intent = intents
        legs, sessions = [], []
        accounts = {}
        acct_first = {}
        xfer_rows = []
        p_unres_abandon = W.P_ABANDON / (1 - W.P_PHONE)
        p_unres_handoff = W.OLD_ASST["handoff"] / (1 - W.OLD_ASST["resolved"])
        ani = self._phones(rng)
        legacy_seq = [0]
        for k in range(m):
            i = ct.who[k]
            start = minute_to_local(C.REC_START, R["start"][k]) + dt.timedelta(seconds=int(rng.integers(0, 60)))
            intent = INTENTS[intents[k]]
            if R["choice"][k]:
                # a conversation the jobseeker opened in the app or on the web
                if i not in accounts:
                    accounts[i] = "acc_" + hexid("claimant", self.case_no[i], n=10)
                    acct_first[i] = start
                channel = "app" if ct.u_split[k] < 0.58 else "web"
                end_state = "resolved" if R["res"][k] else (
                    "handoff" if ct.u_kind[k] < p_unres_handoff else "abandoned")
                conv = "c_" + hexid("conv", self.case_no[i], k)
                parts = self._chat_sessions(rng, start, end_state, ct.u_split[k], intent)
                for j, (s, e, st, ut, at) in enumerate(parts):
                    sessions.append(dict(session_id="s_" + hexid("sess", conv, j), conversation_id=conv,
                                         account_ref=accounts[i], account_type="claimant", org_ref="",
                                         channel=channel, call_ref="", started=iso_local(s), ended=iso_local(e),
                                         user_turns=ut, assistant_turns=at, intent=intent, end_state=st,
                                         release=release_at(s)))
            else:
                # a call to the claimant line
                when = start
                new = when >= CUTOVER
                codes = NEW if new else LEGACY
                iid = self._interaction_id(new, when, legacy_seq)
                caller = ani(i, when.date())
                ivr_s = when
                ivr_len = int(rng.integers(35, 115))
                ivr_e = ivr_s + dt.timedelta(seconds=ivr_len)
                base = dict(interaction_id=iid, source_system=codes["src"], line_dnis=LINE_CLAIMANT, caller_ani=caller,
                            caller_entered=self.case_no[i], menu_path="1>" + MENU[intent])
                if R["red"][k]:
                    # the queue is in overflow: the platform transfers the call to the assistant's voice service
                    q_s, q_e = ivr_e, ivr_e + dt.timedelta(seconds=int(rng.integers(2, 9)))
                    if new:
                        legs.append(self._leg(base, 1, codes["ivr"], ivr_s, ivr_e, result=codes["completed"]))
                        legs.append(self._leg(base, 2, codes["queue"], q_s, q_e, queue=codes["q_claimant"],
                                              result=codes["transferred"], transfer_to=VOICE_TARGET))
                    else:
                        legs.append(self._leg(base, 1, codes["ivr"], ivr_s, q_e, queue=codes["q_claimant"],
                                              result=codes["transferred"], transfer_to=VOICE_TARGET))
                    v_s = q_e + dt.timedelta(seconds=int(rng.integers(3, 8)))
                    end_state = "resolved" if R["res"][k] else (
                        "handoff" if ct.u_kind[k] < p_unres_handoff else "abandoned")
                    dur = int(rng.integers(70, 420)) if end_state != "abandoned" else int(rng.integers(15, 120))
                    v_e = v_s + dt.timedelta(seconds=dur)
                    conv = "c_" + hexid("voice", iid)
                    sessions.append(dict(session_id="s_" + hexid("vsess", iid), conversation_id=conv, account_ref="",
                                         account_type="caller", org_ref="", channel="voice", call_ref=iid,
                                         started=iso_local(v_s), ended=iso_local(v_e),
                                         user_turns=int(rng.integers(2, 9)), assistant_turns=int(rng.integers(3, 11)),
                                         intent=intent, end_state=end_state, release=release_at(v_s)))
                    xfer_rows.append(k)
                else:
                    resolved = bool(R["res"][k])
                    abandon = (not resolved) and ct.u_kind[k] < p_unres_abandon
                    wait = int(min(rng.exponential(260.0), 1700)) + 5
                    q_s = ivr_e
                    if abandon:
                        q_e = q_s + dt.timedelta(seconds=int(min(rng.exponential(330.0), 1700)) + 20)
                        if new:
                            legs.append(self._leg(base, 1, codes["ivr"], ivr_s, ivr_e, result=codes["completed"]))
                            legs.append(self._leg(base, 2, codes["queue"], q_s, q_e, queue=codes["q_claimant"],
                                                  result=codes["abandoned"]))
                        else:
                            legs.append(self._leg(base, 1, codes["ivr"], ivr_s, q_e, queue=codes["q_claimant"],
                                                  result=codes["abandoned"]))
                    else:
                        q_e = q_s + dt.timedelta(seconds=wait)
                        talk = int(rng.gamma(4.0, 95.0)) + 40
                        hold = int(rng.exponential(25.0)) if rng.random() < 0.35 else 0
                        wrap = int(rng.gamma(2.0, 30.0)) + 10
                        a_e = q_e + dt.timedelta(seconds=talk + hold)
                        adviser = self._adviser(rng, new)
                        disp = codes["resolved"] if resolved else codes["callback"]
                        if new:
                            legs.append(self._leg(base, 1, codes["ivr"], ivr_s, ivr_e, result=codes["completed"]))
                            legs.append(self._leg(base, 2, codes["queue"], q_s, q_e, queue=codes["q_claimant"],
                                                  result=codes["answered"]))
                            legs.append(self._leg(base, 3, codes["agent"], q_e, a_e, queue=codes["q_claimant"],
                                                  adviser=adviser, result=codes["completed"], disposition=disp,
                                                  talk=talk, hold=hold, wrap=wrap))
                        else:
                            legs.append(self._leg(base, 1, codes["ivr"], ivr_s, q_e, queue=codes["q_claimant"],
                                                  result=codes["answered"]))
                            legs.append(self._leg(base, 2, codes["agent"], q_e, a_e, queue=codes["q_claimant"],
                                                  adviser=adviser, result=codes["completed"], disposition=disp,
                                                  talk=talk + hold, hold=None, wrap=wrap))
        self.legs_claimant = legs
        self.sessions_claimant = sessions
        self.accounts = accounts
        self.acct_first = acct_first
        self.xfer_rows = xfer_rows

    def _interaction_id(self, new, when, legacy_seq):
        """legacy: AVX, the month and day, then the platform's running sequence; new: the platform's contact id,
        climbing with time (a block of numbers a minute)"""
        legacy_seq[0] += 1
        if new:
            mins = int((when - CUTOVER).total_seconds() // 60)
            used = self._minute_ids.setdefault(mins, 0)
            self._minute_ids[mins] = used + 1
            return "6%011d" % (40818000000 + mins * 400 + used * 7 + int(hexid("cid", mins, used, n=2), 16) % 7)
        return "AVX%02d%02d%07d" % (when.month, when.day, legacy_seq[0])

    def _leg(self, base, n, ltype, s, e, queue="", adviser="", result="", disposition="", talk=None, hold=None,
             wrap=None, transfer_to=""):
        if n > 1:
            base = dict(base, caller_ani="", caller_entered="", menu_path="")
        return dict(base, leg_no=n, leg_type=ltype, start_utc=iso_z(C.to_utc(s)), end_utc=iso_z(C.to_utc(e)),
                    queue=queue, adviser_id=adviser, leg_result=result, disposition=disposition,
                    talk_sec="" if talk is None else talk, hold_sec="" if hold is None else hold,
                    wrap_sec="" if wrap is None else wrap, transfer_to=transfer_to)

    def _adviser(self, rng, new):
        k = int(rng.integers(0, 96))
        return ("pw%04d" % (3100 + k)) if new else ("A%03d" % (210 + k))

    def _chat_sessions(self, rng, start, end_state, u_split, intent):
        """one session, or two when the conversation timed out and the jobseeker came back to it"""
        def turns():
            return int(rng.integers(2, 10)), int(rng.integers(3, 12))
        dur = int(rng.integers(60, 900))
        if rng.random() < W.P_SPLIT:
            e1 = start + dt.timedelta(seconds=int(rng.integers(40, 400)))
            idle_end = e1 + dt.timedelta(minutes=30)
            s2 = idle_end + dt.timedelta(minutes=int(rng.integers(4, 360)))
            e2 = s2 + dt.timedelta(seconds=dur)
            u1, a1 = turns()
            u2, a2 = turns()
            return [(start, idle_end, "timeout", u1, a1), (s2, e2, end_state, u2, a2)]
        u, a = turns()
        return [(start, start + dt.timedelta(seconds=dur), end_state, u, a)]

    def _phones(self, rng):
        """each case's phone numbers over time; a few households share one; numbers change now and then"""
        cl = self.w.claims
        n = cl.n
        base = rng.choice(np.arange(2040000000, 2049999999), size=n, replace=False).astype(np.int64)
        share = rng.random(n) < 0.02
        partner = rng.integers(0, n, size=n)
        base = np.where(share, base[partner], base)
        change = rng.random(n) < 0.07
        when = rng.integers(0, 360, size=n)
        newnum = rng.choice(np.arange(4310000000, 4319999999), size=n, replace=False).astype(np.int64)
        self.phone_rows = []
        for i in range(n):
            opened = cl.opened[i].astype(dt.date)
            if change[i]:
                cd = C.REC_START + dt.timedelta(days=int(when[i]))
                if cd > opened:
                    self.phone_rows.append((i, str(base[i]), opened, cd - dt.timedelta(days=1)))
                    self.phone_rows.append((i, str(newnum[i]), cd, None))
                    continue
            self.phone_rows.append((i, str(base[i]), opened, None))
        cur = {}
        for i, num, a, b in self.phone_rows:
            cur.setdefault(i, []).append((num, a, b))

        def ani(i, d):
            for num, a, b in cur[i]:
                if a <= d and (b is None or d <= b):
                    return num
            return cur[i][-1][0]
        return ani

    # ------------------------------------------------------------------------------- callers with no case
    def _general_calls(self):
        """people without a case on the claimant line's general-enquiries option (applying, a relative, an agency)"""
        rng = C.stream("records/general")
        legs = []
        seq = [10 ** 6]
        for d in C.days(C.REC_START, C.REC_END):
            if not W.phone_open(d):
                continue
            n = rng.poisson(38 * W.DOW[d.weekday()] / 1.25)
            for _ in range(n):
                o, c = W.PHONE_HOURS[d.weekday()]
                when = dt.datetime.combine(d, dt.time(o)) + dt.timedelta(seconds=int(rng.integers(0, (c - o) * 3600)))
                new = when >= CUTOVER
                codes = NEW if new else LEGACY
                iid = self._interaction_id(new, when, seq)
                base = dict(interaction_id=iid, source_system=codes["src"], line_dnis=LINE_CLAIMANT,
                            caller_ani=str(int(rng.integers(2040000000, 2049999999))), caller_entered="",
                            menu_path="9")
                ivr_e = when + dt.timedelta(seconds=int(rng.integers(25, 80)))
                if rng.random() < 0.18:      # heard the recorded information and hung up
                    legs.append(self._leg(base, 1, codes["ivr"], when, ivr_e, result=codes["released"]))
                    continue
                q_e = ivr_e + dt.timedelta(seconds=int(min(rng.exponential(300.0), 1700)) + 5)
                talk = int(rng.gamma(3.0, 90.0)) + 30
                a_e = q_e + dt.timedelta(seconds=talk)
                adviser = self._adviser(rng, new)
                disp = codes["resolved"] if rng.random() < 0.9 else codes["callback"]
                if new:
                    legs.append(self._leg(base, 1, codes["ivr"], when, ivr_e, result=codes["completed"]))
                    legs.append(self._leg(base, 2, codes["queue"], ivr_e, q_e, queue=codes["q_general"],
                                          result=codes["answered"]))
                    legs.append(self._leg(base, 3, codes["agent"], q_e, a_e, queue=codes["q_general"], adviser=adviser,
                                          result=codes["completed"], disposition=disp, talk=talk,
                                          hold=0, wrap=int(rng.gamma(2.0, 25.0)) + 8))
                else:
                    legs.append(self._leg(base, 1, codes["ivr"], when, q_e, queue=codes["q_general"],
                                          result=codes["answered"]))
                    legs.append(self._leg(base, 2, codes["agent"], q_e, a_e, queue=codes["q_general"],
                                          adviser=adviser, result=codes["completed"], disposition=disp, talk=talk,
                                          hold=None, wrap=int(rng.gamma(2.0, 25.0)) + 8))
        self.legs_general = legs

    # ------------------------------------------------------------------------------------------------ employers
    def _employers(self):
        """employers on the employer portal's assistant and the employer line; built in ask.py"""
        import ask
        ask.build_employers(self)

    def _internal(self):
        import ask
        ask.build_internal(self)

    def _survey(self):
        """a sample of contacts sent the post-contact survey, with the answers that came back"""
        rng = C.stream("records/survey")
        rows = []
        by_iid = {}
        for lg in self.legs_claimant:
            by_iid.setdefault(lg["interaction_id"], lg)
        k = 0
        for iid, lg in by_iid.items():
            if rng.random() < 0.06:
                k += 1
                sent = dt.datetime.fromisoformat(lg["end_utc"][:-1]) + dt.timedelta(minutes=int(rng.integers(20, 300)))
                if rng.random() < 0.31:
                    score = int(rng.choice([1, 2, 3, 4, 5], p=[0.07, 0.08, 0.15, 0.32, 0.38]))
                    rows.append(("SV%06d" % k, "phone", iid, iso_z(sent), score))
                else:
                    rows.append(("SV%06d" % k, "phone", iid, iso_z(sent), ""))
        convs = {}
        for s in self.sessions_claimant:
            convs[s["conversation_id"]] = s
        for cid, s in convs.items():
            if rng.random() < 0.06:
                k += 1
                sent = C.to_utc(dt.datetime.fromisoformat(s["ended"])) + dt.timedelta(minutes=int(rng.integers(5, 120)))
                ch = "assistant_voice" if s["channel"] == "voice" else "assistant_chat"
                good = s["end_state"] == "resolved"
                if rng.random() < 0.27:
                    p = [0.03, 0.05, 0.12, 0.35, 0.45] if good else [0.30, 0.25, 0.22, 0.15, 0.08]
                    rows.append(("SV%06d" % k, ch, cid, iso_z(sent), int(rng.choice([1, 2, 3, 4, 5], p=p))))
                else:
                    rows.append(("SV%06d" % k, ch, cid, iso_z(sent), ""))
        # the export holds the surveys sent by the end of the record's last day, Manitoba time
        cutoff = iso_z(C.to_utc(dt.datetime.combine(C.REC_END + dt.timedelta(days=1), dt.time())))
        rows = [r for r in rows if r[3] < cutoff]
        rows.sort(key=lambda r: (r[3], r[0]))
        self.survey = rows
