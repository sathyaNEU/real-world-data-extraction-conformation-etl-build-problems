"""Northcourt's acuity model as the vendor runs it: a 0 to 100 score on one calendar year of claims as paid by the
data cut-off, from the year's allowed claims, the chronic conditions seen, specialty drug use, admissions and
emergency visits. The 140 highest-scoring members enrolled on the stratification date make the list; fixed
score floors set the four risk tiers. The score is a ranking device, not a cost."""
import bisect
import datetime as dt
import math
import zlib
from statistics import NormalDist
from collections import Counter, defaultdict

import world as W

MODEL_SALT = 41730       # the vendor model's own fixed seed for the part of the score its inputs do not explain
ADMIT = {"admit", "admit_trauma", "admit_cardiac", "admit_surgery", "transplant", "delivery", "nicu", "joint"}
ER = {"er", "admit_trauma", "admit_cardiac"}


def paid_date(ev, comp):
    pid, d0, d1, ben, kind, comps, info = ev
    return d0 if ben == "R" else d1 + dt.timedelta(days=comp[3])


def year_slice(sim, year):
    days = [e[1] for e in sim.events]
    lo = bisect.bisect_left(days, dt.date(year, 1, 1))
    hi = bisect.bisect_right(days, dt.date(year, 12, 31))
    return sim.events[lo:hi]


def inputs(sim, year, cutoff, pids):
    """per member: medical allowed, pharmacy allowed (paid by the cut-off), chronic conditions, specialty use,
    admissions, emergency visits"""
    pids = set(pids)
    AM, AR, IP, ERV, SP = defaultdict(float), defaultdict(float), Counter(), Counter(), set()
    for ev in year_slice(sim, year):
        pid = ev[0]
        if pid not in pids:
            continue
        seen = False
        for comp in ev[5]:
            if paid_date(ev, comp) <= cutoff:
                if ev[3] == "M":
                    AM[pid] += comp[2]
                else:
                    AR[pid] += comp[2]
                seen = True
        if not seen:
            continue
        k = ev[4]
        if k in ADMIT:
            IP[pid] += 1
        if k in ER:
            ERV[pid] += 1
        if ev[3] == "R" and W.DRUGS[ev[6]["drug"]][5]:
            SP.add(pid)
    out = {}
    for pid in pids:
        cc = len(sim.cond_years.get((pid, year), ()))
        out[pid] = (AM.get(pid, 0.0), AR.get(pid, 0.0), cc, 1 if pid in SP else 0, IP.get(pid, 0), ERV.get(pid, 0))
    return out


def score(inp, noise, year):
    """the model's output; the list ranks on it and shows it to one decimal. Dollars are restated to the model's
    2023 base with its own cost index, so a score does not drift upward with prices"""
    am, ar, cc, sp, ip, er = inp
    base = 2500.0 * 1.07 ** (year - 2023)
    raw = (11.0 * math.log(1 + (am + 0.2 * ar) / base) + 1.75 * min(cc, 6) + 4.0 * sp + 5.5 * min(ip, 3)
           + 1.3 * min(er, 5) + noise)
    return min(99.94, max(0.0, raw))


def member_noise(ident, year):
    """the part of the vendor's score the inputs above do not capture: fixed for a member and a claims year, so the
    draft and the final runs on 2026 claims differ only through the claims paid in between"""
    u = (zlib.crc32(("%s|%d|%d" % (ident, year, MODEL_SALT)).encode()) + 0.5) / 2 ** 32
    return 2.4 * NormalDist().inv_cdf(u)


def tier_of(s):
    for t, floor in W.TIERS:
        if s >= floor:
            return t
    return 4


def stratify(sim, year, cutoff, elig_date, key):
    """key: 'legacy' for the bid (data book numbers) or 'member' for 2027. Returns [(rank, pid, ident, score, tier)]"""
    people = [p for p in sim.people if p.covered_on(elig_date)]
    if key == "legacy":
        # the data book's census came from Bramwell's last eligibility file, so a member first covered on
        # 1 January 2025 has no Bramwell number and is not in it
        people = [p for p in people if p.legacy is not None]
    pids = [p.pid for p in people]
    inp = inputs(sim, year, cutoff, pids)
    ids = sorted((p.legacy if key == "legacy" else p.member_id, p.pid) for p in people)
    noise = {pid: member_noise(ident, year) for ident, pid in ids}
    rows = []
    for ident, pid in ids:
        rows.append((score(inp[pid], noise[pid], year), 0, ident, pid))
    rows.sort(key=lambda x: (-x[0], x[2]))
    top = rows[:W.LIST_SIZE]
    assert rows[W.LIST_SIZE - 1][0] > rows[W.LIST_SIZE][0]
    return [(i + 1, pid, ident, round(s, 1), tier_of(round(s, 1))) for i, (s, a, ident, pid) in enumerate(top)], inp


def lists(sim):
    bid, bid_inp = stratify(sim, 2024, W.BID_PAID, W.BID_ELIG, "legacy")
    draft, d_inp = stratify(sim, 2026, W.DRAFT_PAID, W.DRAFT_ELIG, "member")
    final, f_inp = stratify(sim, 2026, W.PAID_THROUGH, W.FINAL_ELIG, "member")
    return {"bid": bid, "draft": draft, "final": final, "bid_inp": bid_inp, "final_inp": f_inp}
