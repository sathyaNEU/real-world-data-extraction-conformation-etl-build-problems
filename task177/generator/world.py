"""The joint-liability book, simulated meeting by meeting.

Each centre meets every fourteen days on its own weekday. A member falls short and recovers on her own clock; at a
meeting her co-members pay a short member's instalment, and the group can carry one member at a meeting but rarely
two: carrying two (or more) it stops paying at a high rate, and every loan in a stopped group then runs unpaid. A
stopped group's place in the centre is taken by a new group a few meetings later. The cyclone of 16 October 2026
raises the coastal branches' onsets for a few meetings.

simulate() returns plain tables (numpy and lists); pack.py writes the shipped files from them and nothing in the
shipped files is read back from the truth beyond the cut-off."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import params as P

HOLIDAYS = {
    dt.date(2024, 1, 26), dt.date(2024, 3, 25), dt.date(2024, 6, 14), dt.date(2024, 8, 15), dt.date(2024, 10, 11),
    dt.date(2024, 10, 31), dt.date(2024, 12, 25), dt.date(2025, 1, 26), dt.date(2025, 3, 14), dt.date(2025, 6, 14),
    dt.date(2025, 8, 15), dt.date(2025, 10, 1), dt.date(2025, 10, 20), dt.date(2025, 12, 25), dt.date(2026, 1, 26),
    dt.date(2026, 3, 4), dt.date(2026, 6, 15), dt.date(2026, 8, 15), dt.date(2026, 10, 20), dt.date(2026, 11, 9),
    dt.date(2026, 12, 25), dt.date(2027, 1, 26), dt.date(2027, 3, 22), dt.date(2027, 6, 15),
}
BURN = 30  # meetings simulated before the data room opens, never recorded


def fortnight_instalment(amount):
    r = P.RATE_PA / 26.0
    return amount * r / (1 - (1 + r) ** (-P.INSTALMENTS))


def meeting_date(anchor, t):
    d = anchor + dt.timedelta(days=14 * t)
    while d in HOLIDAYS or d.weekday() == 6:
        d += dt.timedelta(days=1)
    return d


def simulate(seed=P.SEED):
    rng = np.random.default_rng(seed)
    # centres and group slots
    centres = []          # dicts: code, branch, district, anchor (date of meeting index 0), weekday
    slots = []            # dicts: centre index, slot number within centre
    base = P.HIST_START
    for bcode, bname, dist, ngroups, peak in P.BRANCHES:
        made, ci = 0, 0
        while made < ngroups:
            k = int(rng.integers(P.GROUPS_PER_CENTRE[0], P.GROUPS_PER_CENTRE[1] + 1))
            k = min(k, ngroups - made)
            off = int(rng.integers(0, 12))
            if (base + dt.timedelta(days=off)).weekday() == 6:
                off += 1
            ci += 1
            centres.append(dict(code="%s%03d" % (bcode, ci), branch=bcode, branch_name=bname, district=dist,
                                peak=peak, anchor=base + dt.timedelta(days=off)))
            for s in range(k):
                slots.append(dict(centre=len(centres) - 1, slot=s + 1))
            made += k
    NC, NS = len(centres), len(slots)
    # the meeting index runs from -BURN; index 0 is each centre's first meeting on or after the anchor
    T_END = 0
    while True:
        if base + dt.timedelta(days=14 * T_END) > P.SIM_END:
            break
        T_END += 1
    cdates = [[meeting_date(c["anchor"], t) for t in range(-BURN, T_END + 1)] for c in centres]
    TT = BURN + T_END + 1
    cyc_add = np.zeros((TT, NC))
    for ci, c in enumerate(centres):
        if c["peak"] <= 0:
            continue
        n = 0
        for ti in range(TT):
            d = cdates[ci][ti]
            if d >= P.CYCLONE:
                if n < P.CYCLONE_SPAN:
                    cyc_add[ti, ci] = c["peak"] * math.exp(-n / P.CYCLONE_DECAY)
                n += 1
    slot_centre = np.array([s["centre"] for s in slots])
    # positions: NS * 5; each position holds one member at a time
    NP_ = NS * P.GROUP_SIZE
    pos_slot = np.repeat(np.arange(NS), P.GROUP_SIZE)
    pos_centre = slot_centre[pos_slot]
    # registers
    members = []          # dicts: id, slot, group, joined ti, left ti (or None)
    groups = []           # dicts: id, slot, formed ti, stopped ti (or None)
    loans = []            # dicts: id, member, group, cycle, disb ti, amount, inst, first ti
    rows = []             # ledger rows: (ti, centre, group, member, loan, inst_no, due, posting, payer)
    # per position state
    mem = np.full(NP_, -1)
    loan = np.full(NP_, -1)
    nxt = np.zeros(NP_, dtype=int)        # next instalment number due (1..24); 0 = no loan running
    cycle = np.zeros(NP_, dtype=int)
    short = np.zeros(NP_, dtype=bool)
    wait_renew = np.full(NP_, -1)         # ti at which a renewal disburses
    grp = np.full(NS, -1)
    gstate = np.zeros(NS, dtype=int)      # 0 active, 1 stopped, 2 empty awaiting a new group
    reform_at = np.full(NS, -1)
    stop_ti = np.full(NS, -1)
    # loans of stopped groups keep running unpaid until written off: tracked as a list of open debts
    debts = []            # dicts: loan, member, group, centre, next inst, first unpaid ti

    def new_member(p, ti):
        members.append(dict(id=len(members), slot=int(pos_slot[p]), group=int(grp[pos_slot[p]]), joined=ti,
                            left=None))
        mem[p] = len(members) - 1

    def disburse(p, ti, cyc):
        lo, hi = P.CYCLE_AMOUNTS[min(cyc, 3)]
        amt = int(round(rng.uniform(lo, hi) / 1000.0)) * 1000
        loans.append(dict(id=len(loans), member=int(mem[p]), group=int(grp[pos_slot[p]]), cycle=int(cyc), disb=ti,
                          amount=amt, inst=round(fortnight_instalment(amt), 0), first=ti + 1))
        loan[p] = len(loans) - 1
        nxt[p] = 1
        cycle[p] = cyc

    def form_group(s, ti, initial=False):
        groups.append(dict(id=len(groups), slot=int(s), formed=ti, stopped=None))
        grp[s] = len(groups) - 1
        gstate[s] = 0
        for p in range(s * P.GROUP_SIZE, (s + 1) * P.GROUP_SIZE):
            new_member(p, ti)
            short[p] = False
            wait_renew[p] = -1
            if initial:
                cyc = int(rng.integers(1, 5))
                disburse(p, ti, cyc)
                nxt[p] = int(rng.integers(1, P.INSTALMENTS + 1))      # mid-loan at the start of the burn-in
                loans[loan[p]]["first"] = ti + 1 - (nxt[p] - 1)
                loans[loan[p]]["disb"] = loans[loan[p]]["first"] - 1
            else:
                disburse(p, ti, 1)

    for s in range(NS):
        form_group(s, 0, initial=True)
    for ti in range(TT):
        rec = ti >= BURN
        # renewals and re-forming
        for s in np.where((gstate == 2) & (reform_at == ti))[0]:
            form_group(s, ti)
        due_renew = np.where(wait_renew == ti)[0]
        for p in due_renew:
            wait_renew[p] = -1
            if gstate[pos_slot[p]] != 0:
                continue
            if rng.random() < P.RENEW:
                disburse(p, ti, cycle[p] + 1)
            else:
                members[mem[p]]["left"] = ti
                new_member(p, ti)
                short[p] = False
                disburse(p, ti, 1)
        # the shortfall clocks of members in active groups
        act = gstate[pos_slot] == 0
        h = P.ONSET + cyc_add[ti, pos_centre]
        u = rng.random(NP_)
        v = rng.random(NP_)
        newly = act & ~short & (u < h)
        recov = act & short & (v < P.RECOVER)
        short = (short | newly) & ~recov
        # who has an instalment due at this meeting
        due = act & (nxt >= 1) & (nxt <= P.INSTALMENTS) & (loan >= 0)
        due &= np.array([loans[l]["first"] <= ti if l >= 0 else False for l in loan])
        need = due & short
        k = np.bincount(pos_slot[need], minlength=NS)
        w = rng.random(NS)
        n_due = np.bincount(pos_slot[due], minlength=NS)
        stop = (gstate == 0) & (((k == 1) & (w < P.STOP_ONE)) | ((k == 2) & (w < P.STOP_TWO))
                                | ((k >= 3) & (w < P.STOP_MORE)) | ((k > 0) & (k >= n_due)))
        for s in np.where(stop)[0]:
            gstate[s] = 1
            stop_ti[s] = ti
            groups[grp[s]]["stopped"] = ti
        # postings for active groups; a group stopping at this meeting pays nothing from this meeting on
        for s in np.where(stop)[0]:
            for p in range(s * P.GROUP_SIZE, (s + 1) * P.GROUP_SIZE):
                l = loan[p]
                if l >= 0 and 1 <= nxt[p] <= P.INSTALMENTS:
                    n = int(nxt[p])
                    due_ti = loans[l]["first"] + n - 1
                    debts.append(dict(loan=int(l), member=int(mem[p]), group=int(grp[s]), centre=int(pos_centre[p]),
                                      nxt=n, first_unpaid=max(due_ti, ti)))
        for p in np.where(due & ~stop[pos_slot])[0]:
            s = pos_slot[p]
            l = loan[p]
            if short[p]:
                mates = [q for q in range(s * P.GROUP_SIZE, (s + 1) * P.GROUP_SIZE)
                         if q != p and not short[q] and mem[q] >= 0]
                payer = int(mem[mates[int(rng.integers(0, len(mates)))]]) if mates else int(mem[p])
                code = "GS"
            else:
                payer = int(mem[p])
                code = "SELF"
            if rec:
                rows.append((ti - BURN, int(pos_centre[p]), int(grp[s]), int(mem[p]), int(l), int(nxt[p]),
                             loans[l]["inst"], code, payer))
            nxt[p] += 1
            if nxt[p] > P.INSTALMENTS:
                nxt[p] = 0
                wait_renew[p] = ti + 1
        # stopped groups: members leave the active book; the slot re-forms later
        for s in np.where(stop)[0]:
            for p in range(s * P.GROUP_SIZE, (s + 1) * P.GROUP_SIZE):
                if mem[p] >= 0:
                    members[mem[p]]["left"] = ti
                mem[p] = -1
                loan[p] = -1
                nxt[p] = 0
                short[p] = False
                wait_renew[p] = -1
            gstate[s] = 2
            reform_at[s] = ti + int(rng.integers(P.REFORM_GAP[0], P.REFORM_GAP[1] + 1))
        # stopped groups' loans: each instalment falls due unpaid at its own meeting until the schedule ends or the
        # loan is written off at 360 days past due
        keep = []
        for d in debts:
            c = d["centre"]
            l = d["loan"]
            if d["first_unpaid"] >= TT:
                continue
            fu = cdates[c][d["first_unpaid"]]
            while d["nxt"] <= P.INSTALMENTS and loans[l]["first"] + d["nxt"] - 1 == ti:
                if (cdates[c][ti] - fu).days < P.WRITE_OFF_DPD and rec:
                    rows.append((ti - BURN, c, d["group"], d["member"], l, d["nxt"], loans[l]["inst"], "NP", -1))
                d["nxt"] += 1
            if (cdates[c][ti] - fu).days < P.WRITE_OFF_DPD + 14 and d["nxt"] <= P.INSTALMENTS + 1:
                keep.append(d)
        debts = keep
    return dict(centres=centres, slots=slots, members=members, groups=groups, loans=loans, rows=rows,
                cdates=[cd[BURN:] for cd in cdates], burn=BURN)


if __name__ == "__main__":
    import time
    t0 = time.time()
    w = simulate()
    print("centres", len(w["centres"]), "groups", len(w["groups"]), "members", len(w["members"]), "loans",
          len(w["loans"]), "rows", len(w["rows"]), "%.1fs" % (time.time() - t0))
