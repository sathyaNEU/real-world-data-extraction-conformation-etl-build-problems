"""task172 records: the world written out the way each system that holds it writes it.

Counsel's case-management export logs every USCIS notice and case-status event on the renewals it files, under its own
matter numbers and the team's case reference, as scanned or fed, days after the notice date. The team's register holds
each renewal case (two layouts across its April 2025 system change), its case-action log what the team itself did, HR
holds the work permits employees present and spouses upload, Benefits the dependants it covers today, the green-card
tracker every pending adjustment applicant, and the mailroom's dispatch log every packet sent to the lockbox (a new
system from 2 March 2026). Nothing here is planted: each item is how that system records the world."""
from __future__ import annotations

import datetime as dt
from collections import defaultdict

import common as C
import world as Wm

D_ = dt.timedelta

ASC = {"WA": ("Seattle ASC", "Tacoma ASC", "Yakima ASC"), "CA": ("San Jose ASC", "San Francisco ASC", "Oakland ASC"),
       "TX": ("Houston ASC", "Dallas ASC", "Irving ASC"), "NY": ("New York ASC", "Brooklyn ASC"),
       "MA": ("Boston ASC", "Lawrence ASC"), "NC": ("Charlotte ASC", "Raleigh-Durham ASC"),
       "GA": ("Atlanta ASC",), "VA": ("Alexandria ASC", "Norfolk ASC")}
LOCKBOX = {"WA": "USCIS Phoenix Lockbox", "CA": "USCIS Phoenix Lockbox", "TX": "USCIS Dallas Lockbox",
           "NY": "USCIS Chicago Lockbox", "MA": "USCIS Chicago Lockbox", "NC": "USCIS Elgin Lockbox",
           "GA": "USCIS Elgin Lockbox", "VA": "USCIS Elgin Lockbox"}
OFFICE_OF = {"IOE": "Potomac Service Center", "MSC": "National Benefits Center", "EAC": "Vermont Service Center",
             "WAC": "California Service Center", "LIN": "Nebraska Service Center", "SRC": "Texas Service Center"}
STAFF = ("BZ", "RN", "MT", "DM", "RF")       # initials of the team's coordinators (guard.py names, seed 172)
REJECT_WHY = ("Fee", "Signature missing", "Form edition", "Missing pages", "Fee payment declined")


def fy(d):
    return d.year + 1 if d.month >= 10 else d.year


_WD = {}


def workday(d):
    """USCIS's computer workday of the fiscal year: business days since 1 October"""
    if d not in _WD:
        s = dt.date(fy(d) - 1, 10, 1)
        n, x = 0, s
        while x < d:
            if C.busday(x):
                n += 1
            x += D_(days=1)
        _WD[d] = n
    return _WD[d]


class Records:
    pass


def write_all(W):
    R = Records()
    rng = C.stream("records")
    r_log = C.stream("logging")
    exp = C.EXPORT
    holder_state = {}
    for e in W.emps:
        holder_state[id(e)] = e.state
        if e.spouse is not None:
            holder_state[id(e.spouse)] = e.state

    # --------------------------------------------------------------- ids: cases, matters, receipts
    cases = [cs for cs in W.cases if cs.opened <= exp and
             ((cs.received is not None and cs.received >= C.RECORD_START) or
              (cs.received is None and cs.opened >= dt.date(2023, 12, 1)))]
    cases.sort(key=lambda c: (c.opened, c.id))
    inits = initial_cases(W, R)
    year_seq = defaultdict(int)
    new_seq = [104210]
    matter_seq = defaultdict(int)
    receipt_seq = defaultdict(int)

    def receipt_for(office, received):
        if office == "IOE":
            return "IOE%010d" % int(rng.integers(9 * 10 ** 8, 10 ** 10))
        key = (office, fy(received), workday(received))
        receipt_seq[key] += int(rng.integers(1, 40))
        return "%s%02d%03d%05d" % (office, fy(received) % 100, workday(received), 10000 + receipt_seq[key] % 90000)

    items = [(cs.opened, 0, cs.id, cs) for cs in cases] + [(x["opened"], 1, k, x) for k, x in enumerate(inits)]
    items.sort(key=lambda t: t[:3])
    for opened, kind, _, obj in items:
        if kind == 0:
            cs = obj
            open_at_switch = cs.opened < C.REGISTER_SWITCH and (
                cs.received is None and cs.stop is None or
                (cs.decided is not None and cs.decided >= C.REGISTER_SWITCH and not (cs.stop and cs.stop < C.REGISTER_SWITCH)))
        else:
            open_at_switch = opened < C.REGISTER_SWITCH and (obj["decided"] is None or obj["decided"] >= C.REGISTER_SWITCH)
        legacy = new_id = None
        if opened < C.REGISTER_SWITCH:
            year_seq[opened.year] += 1 + (1 if rng.random() < 0.04 else 0)   # numbers voided at intake
            legacy = "RN-%02d-%05d" % (opened.year % 100, year_seq[opened.year])
        if opened >= C.REGISTER_SWITCH or open_at_switch:
            new_seq[0] += 1 + (1 if rng.random() < 0.02 else 0)
            new_id = "GM-%06d" % new_seq[0]
        if kind == 0:
            cs.legacy_id, cs.new_id, cs.case_ref = legacy, new_id, legacy or new_id
            if cs.filed_by == "Counsel" or cs.sends:
                first_sent = cs.sends[0]["sent"] if cs.sends else cs.opened
                matter_seq[first_sent.year] += 1 + int(rng.integers(0, 3) == 0)
                cs.matter = "SLW-%d-%05d" % (first_sent.year, matter_seq[first_sent.year])
            if cs.received is not None:
                if cs.filed_by == "Applicant":
                    office = "IOE"
                elif cs.cat == "(c)(9)" and rng.random() < 0.35:
                    office = "MSC"
                else:
                    office = str(rng.choice(["IOE", "IOE", "IOE", "IOE", "EAC", "WAC", "LIN", "SRC"]))
                cs.office = office
                cs.receipt = receipt_for(office, cs.received)
        else:
            x = obj
            x["legacy_id"], x["new_id"], x["case_ref"] = legacy, new_id, legacy or new_id
            sent = C.prev_busday(x["received"] - D_(days=int(rng.integers(1, 4)))) if x["received"] else None
            x["sent"] = sent
            ms = sent or opened
            matter_seq[ms.year] += 1 + int(rng.integers(0, 3) == 0)
            x["matter"] = "SLW-%d-%05d" % (ms.year, matter_seq[ms.year])
            if x["received"]:
                office = "MSC" if x["cat"] == "(c)(9)" and rng.random() < 0.5 else str(
                    rng.choice(["IOE", "IOE", "IOE", "EAC", "WAC", "LIN", "SRC"]))
                x["receipt"] = receipt_for(office, x["received"])
            else:
                x["receipt"] = ""
    R.cases = cases

    def logged(d, src):
        if src == "Mail scan":
            x = d + D_(days=int(r_log.integers(3, 10)))
            x = C.next_busday(x + D_(days=int(r_log.integers(0, 7)) if r_log.random() < 0.35 else 0))
            return x
        if src == "USCIS online account":
            return C.next_busday(d + D_(days=int(r_log.integers(0, 3))))
        return d + D_(days=int(r_log.integers(0, 2)))

    # --------------------------------------------------------------- counsel's notice export (the spine)
    notes = []

    def note(cs, ntype, ndate, src="Mail scan", **kw):
        if ndate is None:
            return
        lo = logged(ndate, src)
        if lo > exp:
            return
        if cs.stop and ndate > cs.stop and ntype != "Rejection notice":
            return
        notes.append(dict(cs=cs, matter=cs.matter, receipt=kw.get("receipt", cs.receipt), ntype=ntype, ndate=ndate,
                          received=kw.get("received"), appt=kw.get("appt"), site=kw.get("site", ""),
                          vf=kw.get("vf"), vt=kw.get("vt"), office=kw.get("office", OFFICE_OF.get(cs.office or "", "")),
                          logged=lo, src=src, form=kw.get("form", "I-765")))

    for cs in cases:
        if not cs.matter:
            continue
        st = holder_state.get(id(cs.holder), "WA")
        bundled = cs.cat == "(c)(26)" and rng.random() < 0.7
        for s in cs.sends:
            if s["outcome"] == "Rejected" and s["copy"] == "Counsel":
                note(cs, "Rejection notice", s["notice"], receipt="", received=s["arrive"],
                     office=LOCKBOX[st].replace("USCIS ", ""), form="I-539/I-765" if bundled else "I-765")
        if cs.received is None or cs.filed_by != "Counsel":
            continue
        rn = C.next_busday(cs.received + D_(days=max(1.0, Wm.gam(rng, 3.0, 1.5))))
        note(cs, "Receipt notice", rn, src="USCIS online account" if rng.random() < 0.8 else "Mail scan",
             received=cs.received)
        site = str(rng.choice(ASC.get(st, ("Seattle ASC",))))
        if cs.route == "appointment":
            n1 = C.next_busday(cs.received + D_(days=max(5.0, Wm.gam(rng, 12.0, 4.0))))
            n1 = min(n1, C.prev_busday(cs.appt_first - D_(days=5)))
            note(cs, "Biometrics appointment notice", n1, appt=cs.appt_first, site=site)
            if cs.resched:
                n2 = C.prev_busday(cs.appt_first - D_(days=int(rng.integers(2, 15))))
                note(cs, "Biometrics appointment notice", n2, appt=cs.appt, site=site)
            if cs.walkin:
                n3 = C.next_busday(cs.exp_req + D_(days=int(rng.integers(1, 4))))
                note(cs, "Biometrics appointment notice", n3, appt=cs.walkin, site=site,
                     src="USCIS online account")
                if cs.walkin <= cs.decided:
                    note(cs, "Fingerprints taken", cs.walkin, src="Case status feed")
            elif cs.appt <= cs.decided:
                note(cs, "Fingerprints taken", cs.appt, src="Case status feed")
        else:
            nr = C.next_busday(cs.received + D_(days=max(6.0, Wm.gam(rng, 20.0, 6.0))))
            if nr < cs.decided:
                note(cs, "Biometrics reuse notice", nr)
        start = cs.appt if cs.route == "appointment" else cs.received
        if cs.transfer:
            td = C.next_busday(start + D_(days=cs.transfer_at))
            if td < cs.decided:
                note(cs, "Case transferred", td, src="Case status feed")
        if cs.rfe:
            rd = C.next_busday(start + D_(days=cs.rfe_at))
            if rd < cs.decided:
                note(cs, "Request for evidence", rd)
                er = C.next_busday(start + D_(days=cs.rfe_resp))
                if er < cs.decided:
                    note(cs, "Evidence received", er, src="Case status feed")
        if rng.random() < 0.6:
            ur = C.prev_busday(cs.decided - D_(days=int(rng.integers(5, 41))))
            if ur > start:
                note(cs, "Case under review", ur, src="Case status feed")
        if cs.withdrawn:
            note(cs, "Withdrawal acknowledgement", cs.withdraw_ack)
            continue
        if cs.denied:
            note(cs, "Denial notice", cs.decided)
            continue
        nc = cs.new_card
        note(cs, "Approval notice", cs.decided, src="Mail scan" if rng.random() < 0.65 else "USCIS online account",
             vf=nc.valid_from, vt=nc.valid_to)
        prod = C.next_busday(cs.decided + D_(days=int(rng.integers(2, 7))))
        note(cs, "Card produced", prod, src="Case status feed")
        mail = C.next_busday(prod + D_(days=int(rng.integers(1, 5))))
        note(cs, "Card mailed", mail, src="Case status feed")
        if rng.random() < 0.025:
            back = C.next_busday(mail + D_(days=int(rng.integers(6, 13))))
            note(cs, "Card returned undeliverable", back, src="Case status feed")
            mail = C.next_busday(back + D_(days=int(rng.integers(10, 31))))
            note(cs, "Card mailed", mail, src="Case status feed")
        dl = C.next_busday(mail + D_(days=int(rng.integers(1, 6))))
        note(cs, "Card delivered", dl, src="Case status feed")
        if rng.random() < 0.04:
            note(cs, "Card delivered", dl, src="Case status feed")     # the carrier feed re-sends the scan
    notes.sort(key=lambda n: (n["logged"], n["matter"], n["ndate"], n["ntype"]))
    nid = 3100000
    for n in notes:
        nid += 1 + (1 if r_log.random() < 0.03 else 0)
        n["id"] = "NT%07d" % nid
    R.notices = notes

    # --------------------------------------------------------------- the team's register
    reg_rows_old, reg_rows_new = [], []

    def status_at(cs, when):
        """the register's view of a case at `when` (decisions reach it some days after counsel logs them)"""
        if cs.received is None:
            if cs.reject_trail and cs.reject_trail[-1] == "abandoned":
                last = cs.sends[-1]["returned"] if cs.sends else cs.opened
                return ("Rejected - not refiled", None, last + D_(days=20)) if last + D_(days=20) <= when else \
                    ("Sent", None, None)
            if cs.stop and cs.stop <= when:
                return ("Closed - no longer tracked", None, cs.stop)
            return ("Sent", None, None) if cs.sends and cs.sends[0]["sent"] <= when else ("Open", None, None)
        lag = cs.reg_lag
        if cs.stop and cs.stop <= when:
            return ("Closed - no longer tracked", None, cs.stop)
        if cs.withdrawn and cs.withdraw_ack + D_(days=lag) <= when:
            return ("Withdrawn", None, cs.withdraw_ack)
        if cs.decided + D_(days=lag) <= when and not cs.withdrawn:
            return ("Denied" if cs.denied else "Approved", cs.decided, cs.decided)
        if cs.received + D_(days=lag) <= when:
            return ("Filed", None, None)
        return ("Sent", None, None) if cs.sends and cs.sends[0]["sent"] <= when else ("Open", None, None)

    for cs in cases:
        cs.reg_lag = int(rng.integers(1, 11)) if cs.filed_by == "Counsel" else int(rng.integers(5, 31))
    for cs in cases:
        p = cs.principal
        sponsor = p.id if cs.htype == "Spouse" else ""
        sent0 = cs.sends[0]["sent"] if cs.sends else None
        row = dict(cs=cs, person=cs.holder.id, ptype=cs.htype, sponsor=sponsor, cat=cs.cat, card_exp=cs.card.valid_to,
                   opened=cs.opened, sent=sent0, matter=cs.matter or "", receipt=cs.receipt or "",
                   received=cs.received, filed_by="Marrowby Teale" if cs.filed_by == "Counsel" else "Applicant")
        if cs.legacy_id:
            when = min(exp, C.REGISTER_SWITCH - D_(days=1))
            stt, dec, closed = status_at(cs, when)
            if cs.new_id:
                stt, dec, closed = "Migrated", None, None
            r = dict(row, id=cs.legacy_id, status=stt, decided=dec, closed=closed,
                     sent=sent0 if sent0 and sent0 <= when else None,
                     received=cs.received if cs.received and cs.received + D_(days=cs.reg_lag) <= when else None,
                     new_exp=cs.new_card.valid_to if (stt == "Approved" and cs.new_card) else None)
            reg_rows_old.append(r)
        if cs.new_id:
            stt, dec, closed = status_at(cs, exp)
            r = dict(row, id=cs.new_id, legacy=cs.legacy_id or "", status=stt, decided=dec, closed=closed,
                     sent=sent0 if sent0 and sent0 <= exp else None,
                     received=cs.received if cs.received and cs.received + D_(days=cs.reg_lag) <= exp else None,
                     new_exp=cs.new_card.valid_to if (stt == "Approved" and cs.new_card) else None)
            reg_rows_new.append(r)
    for x in inits:
        p = x["principal"]
        sponsor = p.id if x["htype"] == "Spouse" else ""
        row = dict(cs=None, init=x, person=x["holder"].id, ptype=x["htype"], sponsor=sponsor, cat=x["cat"],
                   card_exp=None, opened=x["opened"], sent=x["sent"], matter=x["matter"], receipt=x["receipt"],
                   filed_by="Marrowby Teale")

        def init_status(when):
            if x["cat"] == "(c)(9)":
                # filed in the adjustment package: once USCIS has it, the case leaves the register for the green-card
                # tracker, which follows the application and its work permit from there
                if x["received"] and x["received"] + D_(days=x["lag"]) <= when:
                    return "Closed - no longer tracked", None, x["received"] + D_(days=x["lag"])
            elif x["decided"] and x["decided"] + D_(days=x["lag"]) <= when:
                return "Approved", x["decided"], x["decided"]
            if x["received"] and x["received"] + D_(days=x["lag"]) <= when:
                return "Filed", None, None
            if x["sent"] and x["sent"] <= when:
                return "Sent", None, None
            return "Open", None, None
        if x["legacy_id"]:
            when = min(exp, C.REGISTER_SWITCH - D_(days=1))
            stt, dec, closed = init_status(when)
            if x["new_id"]:
                stt, dec, closed = "Migrated", None, None
            reg_rows_old.append(dict(row, id=x["legacy_id"], status=stt, decided=dec, closed=closed,
                                     received=x["received"] if x["received"] and x["received"] + D_(days=x["lag"]) <= when else None,
                                     new_exp=x["card"].valid_to if stt == "Approved" else None))
        if x["new_id"]:
            stt, dec, closed = init_status(exp)
            reg_rows_new.append(dict(row, id=x["new_id"], legacy=x["legacy_id"] or "", status=stt, decided=dec, closed=closed,
                                     received=x["received"] if x["received"] and x["received"] + D_(days=x["lag"]) <= exp else None,
                                     new_exp=x["card"].valid_to if stt == "Approved" else None))
    reg_rows_old.sort(key=lambda r: (r["opened"], r["id"]))
    reg_rows_new.sort(key=lambda r: (r["opened"], r["id"]))
    R.reg_old, R.reg_new = reg_rows_old, reg_rows_new

    # --------------------------------------------------------------- the team's case actions
    acts = []
    r_oth = C.stream("other filings")

    # the current system registers a renewal the applicant filed herself as a case of its own, numbered when the team
    # learns of it (the next free GM number), and closes the team's case as not refiled by the team
    used = {}
    for cs in cases:
        if cs.new_id:
            used[int(cs.new_id[3:])] = cs.opened
    for x in inits:
        if x["new_id"]:
            used[int(x["new_id"][3:])] = x["opened"]
    nums = sorted(used)
    free = [(g, used[max(n for n in nums if n < g)], used[min(n for n in nums if n > g)])
            for g in range(nums[0] + 1, nums[-1]) if g not in used]
    own_case = {}
    pending = []

    # the date on each notice counsel logged, by case and notice type (the earliest of a type)
    counsel_on = defaultdict(dict)
    for n in notes:
        got = counsel_on[n["cs"].id]
        if n["ntype"] not in got or n["ndate"] < got[n["ntype"]]:
            got[n["ntype"]] = n["ndate"]
    r_cp = C.stream("notice copies")
    r_of = C.stream("other filing dates")

    def held_copy(cs, which):
        """the notice an applicant holds and forwards and the date on it: counsel's date where counsel logged the same
        notice, otherwise the date drawn as USCIS issues that notice"""
        got = counsel_on.get(cs.id, {})
        rcpt = got.get("Receipt notice") or C.next_busday(cs.received + D_(days=max(1.0, Wm.gam(r_cp, 3.0, 1.5))))
        if which == "Receipt notice":
            return "Receipt notice", rcpt
        if which == "Approval notice":
            if cs.withdrawn:
                return "Withdrawal acknowledgement", got.get("Withdrawal acknowledgement", cs.withdraw_ack)
            kind = "Denial notice" if cs.denied else "Approval notice"
            return kind, got.get(kind, cs.decided)
        if cs.route == "appointment":
            d = got.get("Biometrics appointment notice")
            if d is None:
                d = C.next_busday(cs.received + D_(days=max(5.0, Wm.gam(r_cp, 12.0, 4.0))))
                d = min(d, C.prev_busday(cs.appt_first - D_(days=5)))
            return "Biometrics appointment notice", d
        d = got.get("Biometrics reuse notice")
        if d is None:
            d = C.next_busday(cs.received + D_(days=max(6.0, Wm.gam(r_cp, 20.0, 6.0))))
            if cs.decided and d >= cs.decided:
                return "Receipt notice", rcpt         # USCIS decided before a reuse notice went out
        return "Biometrics reuse notice", d

    def other_rejection(cs, before_packet):
        """the lockbox's rejection of the applicant's own other filing, dated from that filing's own trip: sent before
        the renewal's first packet (she forwards it with her receipt notice) or after USCIS received the renewal"""
        first = cs.sends[0]["sent"]
        for _ in range(60):
            if before_packet:
                sent = first - D_(days=int(r_of.integers(8, 26)))
            else:
                sent = cs.received + D_(days=int(r_of.integers(0, 50)))
            arrive = C.next_busday(sent + D_(days=int(r_of.integers(1, 4))))
            notice = C.next_busday(arrive + D_(days=max(3.0, Wm.gam(r_of, 12.0, 4.0))))
            if (notice < first) if before_packet else (notice > cs.received):
                return notice
        return None

    def act(cs, when, action, detail="", ref="", outcome="", out_date=None, notice_date=None, by=None):
        if when is None or when > exp:
            return
        if out_date and out_date > exp:
            outcome, out_date = "", None
        acts.append(dict(cs=cs, case=cs.new_id if (cs.new_id and when >= C.REGISTER_SWITCH) else cs.case_ref,
                         person=cs.holder.id, when=when, action=action, detail=detail, ref=ref, outcome=outcome,
                         out_date=out_date, notice_date=notice_date, by=by or str(rng.choice(STAFF))))

    def sr_number(d):
        if rng.random() < 0.6:
            return "SR%s%04d" % (d.strftime("%y%m%d"), int(rng.integers(0, 10000)))
        return "ER%09d" % int(rng.integers(10 ** 8, 10 ** 9))

    for cs in cases:
        if cs.received is not None and cs.filed_by == "Counsel":
            if cs.exp_req:
                why = "Severe financial loss" if cs.htype == "Employee" or rng.random() < 0.8 else \
                    "Severe financial loss (spouse employment)"
                act(cs, cs.exp_req, "Expedite request", why, sr_number(cs.exp_req),
                    "Accepted" if cs.exp_ok else "Denied", cs.exp_out)
            elif cs.received < C.IFR and rng.random() < 0.004 and cs.decided:
                d0 = C.next_busday(cs.received + D_(days=int(rng.integers(40, 120))))
                if d0 < cs.decided:
                    act(cs, d0, "Expedite request", str(rng.choice(["USCIS error", "Urgent humanitarian"])),
                        sr_number(d0), "Denied" if rng.random() < 0.6 else "Accepted",
                        C.next_busday(d0 + D_(days=int(rng.integers(3, 12)))))
            if cs.decided and (cs.decided - cs.received).days > 150 and rng.random() < 0.5 and not cs.exp_req:
                d0 = C.next_busday(cs.received + D_(days=int(rng.integers(130, 150))))
                act(cs, d0, "Case inquiry", "Outside normal processing time", sr_number(d0), "Responded",
                    C.next_busday(d0 + D_(days=int(rng.integers(10, 30)))))
            if cs.resched == "applicant" and rng.random() < 0.85:
                act(cs, C.prev_busday(cs.appt_first - D_(days=int(rng.integers(3, 20)))), "Biometrics reschedule request",
                    str(rng.choice(["Travel", "Medical", "Work conflict", "Family emergency"])))
            if rng.random() < 0.05:
                d0 = cs.received + D_(days=int(rng.integers(5, 120)))
                act(cs, C.next_busday(d0), "Address change (AR-11)", "Moved", "AR11-%08d" % int(rng.integers(10 ** 7, 10 ** 8)))
            if cs.withdraw_req:
                act(cs, cs.withdraw_req, "Withdrawal request", "Adjustment approved", "", "Acknowledged" if cs.withdrawn
                    else "Decided first", cs.withdraw_ack if cs.withdrawn else cs.decided)
            if cs.stop:
                act(cs, cs.stop, "Stop work", "Employee separated")
            # applicants forward copies of notices they receive
            if rng.random() < 0.06:
                which = str(rng.choice(["Receipt notice", "Biometrics appointment notice", "Approval notice"]))
                nd0 = {"Receipt notice": cs.received, "Biometrics appointment notice": cs.received + D_(days=12),
                       "Approval notice": cs.decided}[which]        # the shared stream's draws turn on this date
                what, on = held_copy(cs, which)
                if which != "Approval notice" and r_oth.random() < Wm.P_OTHER_REJECT:
                    # a lockbox rejection of the applicant's own other filing (an I-539 or I-131 she sent herself),
                    # which the coordinator logs on the case she is in the team's care for: the one she forwards with
                    # the receipt notice is older than the renewal's packet, the one with the appointment letter newer
                    if which == "Receipt notice":
                        r_oth.integers(3, 21)
                    what, on = "Rejection notice", other_rejection(cs, which == "Receipt notice")
                if nd0 and nd0 <= exp:
                    lag = int(rng.integers(4, 30))
                    by = str(rng.choice(STAFF)) if C.next_busday(nd0 + D_(days=lag)) <= exp else None
                    when = C.next_busday(on + D_(days=lag)) if on else None
                    if when and when <= exp:
                        act(cs, when, "Notice forwarded by applicant", what, notice_date=on,
                            by=by or str(r_cp.choice(STAFF)))
            if cs.decided and not cs.denied and not cs.withdrawn and rng.random() < 0.02:
                act(cs, C.next_busday(cs.decided + D_(days=int(rng.integers(25, 60)))), "Card not received inquiry")
        for s in cs.sends:
            if s["outcome"] == "Rejected" and s["copy"] == "Applicant":
                act(cs, C.next_busday(s["returned"] + D_(days=int(rng.integers(0, 3)))), "Notice forwarded by applicant",
                    "Rejection notice", notice_date=s["notice"])
            elif s["outcome"] == "Rejected" and rng.random() < 0.12:
                # the applicant's own copy of a rejection counsel also holds
                act(cs, C.next_busday(s["notice"] + D_(days=int(rng.integers(6, 21)))), "Notice forwarded by applicant",
                    "Rejection notice", notice_date=s["notice"])
        if cs.filed_by == "Applicant" and cs.received is not None:
            told = C.next_busday(cs.received + D_(days=int(rng.integers(3, 15))))
            n0 = len(acts)
            act(cs, told, "Notice forwarded by applicant", "Receipt notice", notice_date=cs.received)
            if cs.new_id and told >= C.REGISTER_SWITCH and len(acts) > n0:
                pending.append((cs, acts[-1]))
    # the applicant's own filing takes the next free GM number from the day the team learns of it; the log keeps the
    # action's place (its number was given when the coordinator logged the forwarded notice)
    for cs, a in pending:
        for j, (g, o1, o2) in enumerate(free):
            if o2 >= a["when"]:
                free.pop(j)
                own_case[cs.id] = ("GM-%06d" % g, max(a["when"], o1))
                break
        else:
            raise SystemExit("no free GM number after %s" % a["when"])
    acts.sort(key=lambda a: (a["when"], a["case"], a["action"]))
    aid = 58000
    for a in acts:
        aid += 1
        a["id"] = "CA%06d" % aid
    for cs, a in pending:
        a["case"] = own_case[cs.id][0]
    R.actions = acts

    # the applicant's own filing as the current register holds it: the team's case closed as not refiled by the team,
    # and the filing as a case of its own, filed by the applicant
    by_new = {r["id"]: r for r in reg_rows_new}
    for cs in cases:
        if cs.id not in own_case:
            continue
        y_id, y_open = own_case[cs.id]
        x = by_new[cs.new_id]
        stt, dec, closed = status_at(cs, exp)
        if stt == "Sent":
            stt = "Open"                   # no packet of the team's: the receipt is not yet entered
        y = dict(x, id=y_id, legacy="", opened=y_open, sent=None, matter="", receipt=cs.receipt or "",
                 status=stt, decided=dec, closed=closed, filed_by="Applicant",
                 received=cs.received if cs.received + D_(days=cs.reg_lag) <= exp else None,
                 new_exp=cs.new_card.valid_to if (stt == "Approved" and cs.new_card) else None)
        x.update(status="Rejected - not refiled", decided=None, closed=y_open, received=None, receipt="",
                 new_exp=None, filed_by="Marrowby Teale")
        reg_rows_new.append(y)
    reg_rows_new.sort(key=lambda r: (r["opened"], r["id"]))
    R.own_case = own_case

    # --------------------------------------------------------------- the dispatch log, 2025 and 2026
    disp = []
    seq_old = defaultdict(int)
    seq_new = [0]
    for cs in cases:
        st = holder_state.get(id(cs.holder), "WA")
        bundled = cs.cat == "(c)(26)" and rng.random() < 0.7
        contents = "I-765 renewal + I-539" if bundled else "I-765 renewal"
        new_row = None
        for k, s in enumerate(cs.sends):
            if s["sent"] < dt.date(2025, 1, 1) or s["sent"] > exp:
                continue
            if s["sent"] < C.DISPATCH_SWITCH:
                seq_old[s["sent"].year] += 1
                pid = seq_old[s["sent"].year]
                status = {"Receipted": "Receipted", "Rejected": "Returned", "Courier": "Returned"}[s["outcome"]]
                ret = s["returned"] if s["outcome"] != "Receipted" else None
                if ret and ret > exp:
                    ret, status = None, "Sent"
                if status == "Receipted" and (s["arrive"] + D_(days=12) > exp or cs.received is None):
                    status = "Sent"           # no receipt notice reached the team (the matter closed on a departure)
                disp.append(dict(pid=pid, sent=s["sent"], case=cs.new_id if (cs.new_id and s["sent"] >= C.REGISTER_SWITCH)
                                 else cs.case_ref, person=cs.holder.id, contents=contents, to=LOCKBOX[st],
                                 courier="FedEx", tracking="%012d" % int(rng.integers(10 ** 11, 10 ** 12)), status=status,
                                 returned=ret, cs=cs, send=s))
            else:
                # the new system keeps one row per packet and writes a resend over it
                if new_row is None:
                    seq_new[0] += 1
                    new_row = dict(pid=seq_new[0], case=cs.new_id or cs.case_ref, person=cs.holder.id,
                                   contents=contents, to=LOCKBOX[st], courier="UPS", cs=cs)
                    disp.append(new_row)
                new_row.update(sent=s["sent"], tracking="1Z%06X%010d" % (int(rng.integers(0, 16 ** 6)),
                                                                          int(rng.integers(0, 10 ** 10))),
                               send=s)
                if s["outcome"] == "Receipted":
                    new_row.update(status="Receipted" if (s["arrive"] + D_(days=12) <= exp and cs.received is not None)
                                   else "Sent", returned=None)
                else:
                    ret = s["returned"]
                    new_row.update(status="Returned" if ret <= exp else "Sent", returned=ret if ret <= exp else None)
    # packets for other filings travel through the same mailroom
    r_o = C.stream("other-packets")
    d = dt.date(2025, 1, 2)
    while d <= exp - D_(days=1):
        for _ in range(int(r_o.poisson(4.2))):
            if not C.busday(d):
                continue
            st = str(r_o.choice(["WA"] * 6 + ["CA", "TX", "NY", "MA"]))
            kind = str(r_o.choice(["I-539", "I-539", "I-765 initial + I-485 + I-131", "I-131", "I-765 initial"]))
            if d < C.DISPATCH_SWITCH:
                seq_old[d.year] += 1
                pid, cour = seq_old[d.year], "FedEx"
                trk = "%012d" % int(r_o.integers(10 ** 11, 10 ** 12))
            else:
                seq_new[0] += 1
                pid, cour = seq_new[0], "UPS"
                trk = "1Z%06X%010d" % (int(r_o.integers(0, 16 ** 6)), int(r_o.integers(0, 10 ** 10)))
            ret = C.next_busday(d + D_(days=int(r_o.integers(12, 30)))) if r_o.random() < 0.035 else None
            status = "Returned" if ret and ret <= exp else ("Receipted" if d + D_(days=14) <= exp else "Sent")
            pref = {"I-539": "H4X", "I-765 initial + I-485 + I-131": "AOS", "I-131": "TRV", "I-765 initial": "EAD"}[kind]
            ocase = "%s-%05d" % (pref, int(r_o.integers(1000, 99999)))
            operson = "%06d" % int(r_o.integers(210000, 989999)) if r_o.random() < 0.55 else \
                ("D%07d" % int(r_o.integers(10 ** 6, 10 ** 7)))
            disp.append(dict(pid=pid, sent=d, case=ocase, person=operson, contents=kind, to=LOCKBOX[st], courier=cour,
                             tracking=trk, status=status, returned=ret if ret and ret <= exp else None, cs=None, send=None,
                             other=True))
        d += D_(days=1)
    disp.sort(key=lambda r: (r["sent"], r["courier"], r["pid"]))
    R.dispatch = disp
    return R


def initial_cases(W, R):
    """the team's initial filings (a spouse's first H-4 permit, the (c)(9) permits filed with an adjustment) opened
    from December 2023, as the register holds them"""
    rng = C.stream("initials")
    out = []
    for c in W.cards:
        if c.basis != "initial" or c.valid_from > C.EXPORT + D_(days=200):
            continue
        if c.cat == "(c)(9)":
            p = c.holder if c.htype == "Employee" else c.holder.principal
            received = C.next_busday(p.gc_filed + D_(days=int(rng.integers(1, 4))))
            opened = C.prev_busday(received - D_(days=int(rng.integers(20, 61))))
        else:
            p = c.holder.principal
            received = C.prev_busday(c.valid_from - D_(days=max(30.0, Wm.gam(rng, 95.0, 25.0))))
            opened = C.prev_busday(received - D_(days=int(rng.integers(15, 41))))
        if opened < dt.date(2023, 12, 1) or opened > C.EXPORT:
            continue
        decided = c.valid_from if c.valid_from <= C.EXPORT else None
        out.append(dict(card=c, holder=c.holder, htype=c.htype, cat=c.cat, principal=p, opened=opened,
                        received=received if received <= C.EXPORT else None, decided=decided,
                        lag=int(rng.integers(1, 11))))
    out.sort(key=lambda x: (x["opened"], x["holder"].id))
    R.initials = out
    return out


def roster(W, R):
    """HR's work-permit roster: the cards employees present at hire and at I-9 reverification, every card of a spouse
    the team took into its care (entered at onboarding), and the later cards spouses upload to the benefits portal"""
    rng = C.stream("roster")
    rows = []
    first_label = {}
    by_holder = defaultdict(list)
    for c in W.cards:
        by_holder[id(c.holder)].append(c)
    R.label_rule = {}
    for hid, cl in by_holder.items():
        cl.sort(key=lambda c: (c.valid_from, c.valid_to))
        stale = rng.random() < Wm.P_STALE_LABEL
        label0 = None
        R.label_rule[hid] = (stale, cl[0].cat)
        for k, c in enumerate(cl):
            c.roster, c.roster_cat, c.entered_on, c.entered_via = False, None, None, None
            c.roster_holder = None
            if c.valid_from > C.EXPORT:
                continue
            if c.htype == "Employee":
                prev = cl[k - 1] if k else None
                base = max(c.valid_from, prev.valid_to - D_(days=int(rng.integers(0, 11)))) if prev else c.valid_from
                ent = C.next_busday(base + D_(days=int(rng.integers(0, 6))))
                via = "I-9 reverification" if prev else "I-9 at hire"
                present = True
            else:
                in_record = c.case is not None and c.case.received is not None and c.case.received >= C.RECORD_START
                if k == 0:
                    present, via = True, "Onboarding"
                    ent = C.next_busday(max(c.valid_from, dt.date(2021, 1, 4)) + D_(days=int(rng.integers(1, 30))))
                elif c.case is not None and c.case.filed_by == "Applicant":
                    present, via = True, "Portal upload"
                    ent = C.next_busday(c.valid_from + D_(days=int(rng.integers(10, 60))))
                elif not in_record and c.cat == "(c)(26)":
                    present, via = True, "Portal upload"
                    ent = C.next_busday(c.valid_from + D_(days=int(rng.integers(5, 90))))
                else:
                    p_up = Wm.P_UPLOAD_C9 if (c.cat == "(c)(9)" and c.basis == "initial") else Wm.P_UPLOAD_RENEWAL
                    present, via = rng.random() < p_up, "Portal upload"
                    ent = C.next_busday(c.valid_from + D_(days=int(rng.integers(5, 90))))
            if label0 is None:
                label0 = c.cat
            if not present or ent > C.EXPORT:
                continue
            lab = c.cat
            if c.htype == "Spouse" and via == "Portal upload" and label0 == "(c)(26)" and c.cat == "(c)(9)" and stale:
                lab = "(c)(26)"          # the upload form carries the category of the holder's first entry
            c.roster, c.roster_cat, c.entered_on, c.entered_via = True, lab, ent, via
            sp_id = c.holder.principal.id if (c.htype == "Spouse" and via == "Onboarding") else ""
            hid = c.holder.id
            if c.htype == "Spouse" and via == "Portal upload" and c.holder.late_enroll and ent >= c.holder.late_enroll:
                hid = c.holder.dep_id              # the portal knows a spouse on the plan by her dependant ID
            c.roster_holder = hid
            rows.append(dict(card=c, holder=hid, htype=c.htype, cat=lab, number=c.number, vf=c.valid_from,
                             vt=c.valid_to, ent=ent, via=via, sponsor=sp_id))
    rows.sort(key=lambda r: (r["ent"], r["holder"], r["vf"]))
    R.roster = rows
    return rows


def people(W, R):
    """HR's program roster (employees active at the export or separated since January 2024), Benefits' dependants
    covered today, and the green-card tracker"""
    rng = C.stream("people")
    exp = C.EXPORT
    emps = []
    for e in W.emps:
        if e.term and e.term < C.RECORD_START:
            continue
        if e.hire > exp:
            continue
        active = e.term is None or e.term > exp
        if e.gc_approved and e.gc_approved <= exp:
            basis = "Permanent resident"
        elif e.gc_filed and e.gc_filed <= exp:
            basis = "I-485 pending"
        else:
            basis = e.basis if e.basis != "I-485 pending" else "H-1B"
        emps.append(dict(emp=e, id=e.id, hire=e.hire, status="Active" if active else "Terminated",
                         term=None if active else e.term, state=e.state, family=e.family, basis=basis, enroll=e.enroll))
    emps.sort(key=lambda r: r["id"])
    R.employees = emps
    deps = []
    for s in W.spouses:
        e = s.principal
        if s.late_enroll and not s.enrolled:
            if e.hire <= exp and (e.term is None or e.term > exp):
                deps.append(dict(id=s.dep_id, enroll=e.enroll, rel="Spouse", start=s.late_enroll, birth=s.dob_year,
                                 sp=s))
            continue
        if not s.enrolled or e.hire > exp:
            continue
        active = e.term is None or e.term > exp
        if active and not s.dropped:
            covered = True
        elif not active and s.cobra and e.term >= exp - D_(days=540):
            covered = True
        else:
            covered = False
        if covered:
            start = min(max(e.hire, dt.date(2019, 1, 1)) + D_(days=int(rng.integers(0, 60))),
                        exp - D_(days=int(rng.integers(1, 20))))
            deps.append(dict(id=s.id, enroll=e.enroll, rel="Spouse" if rng.random() < 0.97 else "Domestic partner",
                             start=start, birth=s.dob_year, sp=s))
    r_k = C.stream("children")
    r_kid = C.stream("children ids")
    spouse_ids = {x.id for x in W.spouses} | {x.dep_id for x in W.spouses if x.dep_id}
    for e in W.emps:
        if e.spouse is None or not (e.term is None or e.term > exp) or e.hire > exp:
            continue
        for _ in range(int(r_k.choice([0, 0, 1, 1, 1, 2, 2, 3]))):
            birth = int(r_k.integers(2008, 2026))
            first = max(e.hire, dt.date(2019, 1, 1), dt.date(birth, 1, 1) + D_(days=int(r_k.integers(0, 330))))
            start = min(first + D_(days=int(r_k.integers(0, 45))), exp - D_(days=int(r_k.integers(1, 30))))
            cid = "D%07d" % int(r_k.integers(10 ** 6, 10 ** 7))
            while cid in spouse_ids:                  # Benefits never reuses a dependant ID
                cid = "D%07d" % int(r_kid.integers(10 ** 6, 10 ** 7))
            deps.append(dict(id=cid, enroll=e.enroll, rel="Child",
                             start=start, birth=birth, sp=None))
    seen = set()
    deps2 = []
    for d in deps:
        if d["id"] in seen:
            continue
        seen.add(d["id"])
        deps2.append(d)
    deps2.sort(key=lambda d: (d["enroll"], d["id"]))
    R.dependants = deps2
    trk = []
    by_holder = defaultdict(list)
    for c in W.cards:
        by_holder[id(c.holder)].append(c)
    pd_rng = C.stream("priority")
    for e in W.emps:
        if not e.gc_filed or e.gc_filed > exp:
            continue
        if e.term and e.term < C.RECORD_START:
            continue
        if e.country == "India":
            pdate = dt.date(2012, 1, 1) + D_(days=int(pd_rng.integers(0, 1400)))
        elif e.country == "China":
            pdate = dt.date(2019, 6, 1) + D_(days=int(pd_rng.integers(0, 600)))
        else:
            pdate = e.gc_filed - D_(days=int(pd_rng.integers(300, 700)))
        i140 = pdate + D_(days=int(pd_rng.integers(60, 200)))
        members = [(e, "Principal")] + ([(e.spouse, "Spouse")] if e.spouse is not None and
                                        (e.spouse.derivative or e.spouse.switch) else [])
        for who, rel in members:
            cards = sorted([c for c in by_holder.get(id(who), ()) if c.cat == "(c)(9)" and c.valid_from <= exp],
                           key=lambda c: c.valid_from)
            last = cards[-1] if cards else None
            if e.gc_approved and e.gc_approved <= exp:
                st, dec = "Approved", e.gc_approved
            elif e.term and e.term <= exp:
                st, dec = "Abandoned", None
            else:
                st, dec = "Pending", None
            trk.append(dict(applicant=who.id, principal=e.id, rel=rel, country=e.country, pd=pdate, i140=i140,
                            i485=e.gc_filed, status=st, decided=dec, ead_from=last.valid_from if last else None,
                            ead_to=last.valid_to if last else None, who=who))
    trk.sort(key=lambda t: (t["i485"], t["principal"], t["rel"] != "Principal"))
    R.tracker = trk
    return R


def h1b_calendar(W, R):
    """the immigration team's 2027 H-1B extension calendar (a distractor: no figure reads it)"""
    rng = C.stream("h1b")
    rows = []
    exp = C.EXPORT
    by_holder = defaultdict(list)
    for c in W.cards:
        by_holder[id(c.holder)].append(c)
    for e in W.emps:
        if not (e.term is None or e.term > exp) or e.gc_approved and e.gc_approved <= exp:
            continue
        if e.basis not in ("H-1B",) and not (e.spouse and not e.gc_filed):
            continue
        end = None
        if e.spouse is not None and not e.spouse.switch:
            cur = [c for c in by_holder.get(id(e.spouse), ()) if c.cat == "(c)(26)" and c.valid_from <= exp]
            if cur:
                end = max(c.valid_to for c in cur)
        if end is None:
            end = dt.date(2026, 6, 1) + D_(days=int(rng.integers(0, 1100)))
        if end.year != 2027:
            continue
        h4 = (1 if e.spouse is not None else 0) + int(rng.choice([0, 0, 1, 1, 2]))
        plan = end - D_(days=int(rng.choice([150, 165, 180])))
        rows.append(dict(id=e.id, end=end, plan="%d-%02d" % (plan.year, plan.month),
                         kind="Extension" if rng.random() < 0.88 else "Amendment and extension", h4=h4,
                         premium="Yes" if rng.random() < 0.62 else "No"))
    rows.sort(key=lambda r: (r["end"], r["id"]))
    R.h1b = rows
    return rows


def _pick_at(u, table):
    acc = 0.0
    for v, p in table:
        acc += p
        if u < acc:
            return v
    return table[-1][0]


def dual_roles(W, R):
    """spouses in the team's care who took a job at Sallowmere during the life of their current card: HR's program
    roster holds each as an employee of her own, her I-9 at hire records the card she presented, and she uploads the
    same card on the spouse side too, so one card sits on HR's work permit roster under two IDs"""
    rng = C.stream("dual role")
    exp = C.EXPORT
    taken = {r["id"] for r in R.employees} | {e.id for e in W.emps}
    enrolls = {r["enroll"] for r in R.employees} | {e.enroll for e in W.emps}
    by_holder = defaultdict(list)
    for c in W.cards:
        by_holder[id(c.holder)].append(c)
    R.dual = []
    for s in W.spouses:
        u, h_off, fam = rng.random(), rng.random(), rng.random()
        ent_off, up_off = int(rng.integers(0, 5)), int(rng.integers(1, 21))
        e = s.principal
        if not (e.hire <= exp and (e.term is None or e.term > exp)):
            continue
        cl = sorted((c for c in by_holder.get(id(s), ()) if c.valid_from <= exp), key=lambda c: (c.valid_from, c.valid_to))
        if not cl or cl[-1].valid_to <= exp:
            continue
        cur = cl[-1]
        lo = max(cur.valid_from + D_(days=15), dt.date(2023, 6, 1))
        hi = exp - D_(days=20)
        if u >= Wm.P_DUAL[cur.cat] or hi < lo:
            continue
        hire = C.next_busday(lo + D_(days=int(h_off * (hi - lo).days)))
        eid = "%06d" % int(rng.integers(210000, 989999))
        while eid in taken:
            eid = "%06d" % int(rng.integers(210000, 989999))
        taken.add(eid)
        ben = "BEN%08d" % int(rng.integers(10 ** 7, 10 ** 8))
        while ben in enrolls:
            ben = "BEN%08d" % int(rng.integers(10 ** 7, 10 ** 8))
        enrolls.add(ben)
        if s.gc_approved and s.gc_approved <= exp:
            basis = "Permanent resident"
        else:
            basis = "I-485 pending" if cur.cat == "(c)(9)" else "H-4 EAD"
        R.employees.append(dict(emp=None, id=eid, hire=hire, status="Active", term=None, state=e.state,
                                family=_pick_at(fam, Wm.FAMILIES), basis=basis, enroll=ben, dual=s))
        R.roster.append(dict(card=cur, holder=eid, htype="Employee", cat=cur.cat, number=cur.number, vf=cur.valid_from,
                             vt=cur.valid_to, ent=C.next_busday(hire + D_(days=ent_off)), via="I-9 at hire",
                             sponsor=""))
        if not cur.roster:
            stale, label0 = R.label_rule[id(s)]
            lab = "(c)(26)" if (label0 == "(c)(26)" and cur.cat == "(c)(9)" and stale) else cur.cat
            up = C.next_busday(hire + D_(days=up_off))
            hid = s.dep_id if (s.late_enroll and up >= s.late_enroll) else s.id
            cur.roster, cur.roster_cat, cur.entered_on, cur.entered_via, cur.roster_holder = True, lab, up, \
                "Portal upload", hid
            R.roster.append(dict(card=cur, holder=hid, htype="Spouse", cat=lab, number=cur.number, vf=cur.valid_from,
                                 vt=cur.valid_to, ent=up, via="Portal upload", sponsor=""))
        R.dual.append((s, eid, cur, hire))
    R.roster.sort(key=lambda r: (r["ent"], r["holder"], r["vf"]))
    R.employees.sort(key=lambda r: r["id"])
    return R.dual


def entity_transfers(W, R):
    """H-1B employees of the H-4 households moved in 2026 to another Sallowmere entity: HR's program roster ends the
    employee's ID the day before the move and opens a new one from it, the benefits enrollment carried over; the
    team's records, all made before the move, keep the ID it knew"""
    rng = C.stream("entity moves")
    exp = C.EXPORT
    taken = {r["id"] for r in R.employees} | {e.id for e in W.emps}
    rows = {r["id"]: r for r in R.employees}
    last = defaultdict(lambda: dt.date(2000, 1, 1))
    for cs in R.cases:
        last[id(cs.holder)] = max(last[id(cs.holder)], cs.opened)
    for x in R.initials:
        last[id(x["holder"])] = max(last[id(x["holder"])], x["opened"])
    for r in R.roster:
        if r["via"] == "Onboarding":
            last[id(r["card"].holder)] = max(last[id(r["card"].holder)], r["ent"])
    by_holder = defaultdict(list)
    for c in W.cards:
        by_holder[id(c.holder)].append(c)
    R.moves = []
    for e in W.emps:
        u, t_off = rng.random(), rng.random()
        s = e.spouse
        if s is None or e.gc_filed or s.switch or e.id not in rows or rows[e.id]["status"] != "Active":
            continue
        cl = sorted((c for c in by_holder.get(id(s), ()) if c.valid_from <= exp), key=lambda c: (c.valid_from, c.valid_to))
        if not cl or cl[-1].valid_to <= exp or cl[-1].cat != "(c)(26)":
            continue
        lo = max(last[id(s)] + D_(days=30), dt.date(2026, 4, 1))
        hi = exp - D_(days=15)
        if u >= Wm.P_ENTITY_MOVE or hi < lo:
            continue
        move = C.next_busday(lo + D_(days=int(t_off * (hi - lo).days)))
        nid = "%06d" % int(rng.integers(210000, 989999))
        while nid in taken:
            nid = "%06d" % int(rng.integers(210000, 989999))
        taken.add(nid)
        old = rows[e.id]
        R.employees.append(dict(old, id=nid, hire=move, status="Active", term=None, moved_from=e.id))
        old.update(status="Terminated", term=C.prev_busday(move - D_(days=1)), moved_to=nid)
        for h in R.h1b:
            if h["id"] == e.id:
                h["id"] = nid
        R.moves.append((e, e.id, nid, move))
    R.employees.sort(key=lambda r: r["id"])
    R.h1b.sort(key=lambda r: (r["end"], r["id"]))
    return R.moves


def posted_times(R):
    """the team's monthly capture of the processing time USCIS posts for Form I-765 (constructed; a distractor)"""
    rng = C.stream("posted")
    rows = []
    v9, v26 = 4.5, 3.5
    d = dt.date(2024, 1, 8)
    while d <= dt.date(2026, 11, 30):
        v9 = min(6.5, max(3.0, v9 + float(rng.normal(0, 0.18))))
        v26 = min(5.5, max(2.5, v26 + float(rng.normal(0, 0.15))))
        cap = C.next_busday(d + D_(days=int(rng.integers(0, 5))))
        if cap < dt.date(2025, 7, 1):
            rows.append(dict(cap=cap, line="I-765 based on a pending I-485 (c)(9)", office="National Benefits Center",
                             months=round(v9 * 2) / 2, inquiry=cap - D_(days=int(round(v9 * 30.4)) + int(rng.integers(0, 9)))))
            rows.append(dict(cap=cap, line="I-765 all other applications", office="Potomac Service Center",
                             months=round(v26 * 2) / 2, inquiry=cap - D_(days=int(round(v26 * 30.4)) + int(rng.integers(0, 9)))))
        else:
            for off, adj in (("Potomac Service Center", 0.0), ("Vermont Service Center", 0.5), ("Nebraska Service Center", -0.5)):
                rows.append(dict(cap=cap, line="I-765 all other applications", office=off,
                                 months=max(2.0, round((v26 + adj + float(rng.normal(0, 0.2))) * 2) / 2), inquiry=None))
            rows.append(dict(cap=cap, line="I-765 based on a pending I-485 (c)(9)", office="National Benefits Center",
                             months=round(v9 * 2) / 2, inquiry=None))
        m = d.month + 1
        d = dt.date(d.year + (m > 12), (m - 1) % 12 + 1, 8)
    R.posted = rows
    return rows
