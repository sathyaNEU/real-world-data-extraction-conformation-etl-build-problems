"""task270 referral world (Ask B): the community teams' referrals to the Complex Emotional Needs Service's DBT
programme in 2025 and 2026, its waiting list, and the move of its referrals from the service's own database into the
patient record's referral module.

The module went live on Monday 22 June 2026. The legacy database's final export was taken on Friday 19 June; the
service's administrators keyed every referral still open in it into the module over the next three weeks, and the
module stamps a record's received date (and, for one already triaged and listed, its triage and listing dates) with
the day the record was created. The legacy database is not in the pack: the date the service first received each
referral moved over survives in the trust's correspondence log, as the acknowledgement letter the service sends on the
day it receives a referral, keyed by NHS number."""
from __future__ import annotations

import csv
import datetime as dt
import os

import numpy as np

import common as K

TEAM_CODES = [c for c, _ in K.TEAMS]
# relative referral volume to the DBT programme by current team
VOLUME = {"BW-CM02": 1.5, "BW-CM05": 1.35, "BW-CM11": 1.0, "BW-CM31": 1.1, "BW-CM17": 0.95, "BW-CM03": 0.8,
          "BW-CM08": 0.85, "BW-CM20": 0.75, "BW-CM09": 0.8, "BW-CM22": 0.7, "BW-CM12": 0.85}
COHORTS = [dt.date(2025, 2, 3), dt.date(2025, 4, 7), dt.date(2025, 6, 9), dt.date(2025, 9, 8), dt.date(2025, 11, 10),
           dt.date(2026, 1, 12), dt.date(2026, 3, 9), dt.date(2026, 5, 11), dt.date(2026, 7, 13), dt.date(2026, 9, 14),
           dt.date(2026, 11, 9), dt.date(2027, 1, 11)]
PLACES = 11
MIGRATION = [K.HUB_GOLIVE + dt.timedelta(days=i) for i in range(19) if (K.HUB_GOLIVE + dt.timedelta(days=i)).weekday() < 5]


class Pt:
    pass


class Ref:
    pass


def workday(d):
    while d.weekday() >= 5:
        d += dt.timedelta(days=1)
    return d


def team_code_on(team, day):
    if team == "BW-CM31" and day < K.MERGER:
        return None
    return team


def build(used_numbers):
    r = K.rng("hub")
    pts, refs = [], []
    day = dt.date(2024, 9, 2)
    w = np.array([VOLUME[c] for c in TEAM_CODES])
    w = w / w.sum()
    while day <= dt.date(2026, 12, 18):
        if day.weekday() < 5 and not (dt.date(2026, 6, 19) < day <= K.HUB_GOLIVE):
            for _ in range(int(r.poisson(0.62))):
                team = TEAM_CODES[int(r.choice(len(TEAM_CODES), p=w))]
                p = Pt()
                while True:
                    num = str(int(r.integers(1000000, 1999999)))
                    if num not in used_numbers:
                        used_numbers.add(num)
                        break
                p.number = num
                p.team = team
                p.half = "BW-CM14" if r.random() < 0.5 else "BW-CM15"
                ref = Ref()
                ref.pt = p
                ref.received = day
                u = r.random()
                ref.outcome = ("Accepted - DBT" if u < 0.6 else "Accepted - MBT" if u < 0.7 else
                               "Not accepted" if u < 0.9 else "Returned to referrer")
                ref.triaged = workday(day + dt.timedelta(days=int(r.integers(9, 40))))
                ref.listed = workday(ref.triaged + dt.timedelta(days=int(r.integers(0, 6)))) \
                    if ref.outcome == "Accepted - DBT" else None
                ref.removed, ref.reason, ref.recorded = None, "", None
                ref.offers = []
                pts.append(p)
                refs.append(ref)
        day += dt.timedelta(days=1)
    # offers at each cohort in order of the service receiving the referral; some decline or leave the list
    for cohort in COHORTS:
        waiting = sorted([f for f in refs if f.listed and f.listed < cohort - dt.timedelta(days=14) and f.removed is None],
                         key=lambda f: (f.received, f.pt.number))
        taken = 0
        for f in waiting:
            if taken >= PLACES:
                break
            f.offers.append(cohort)
            # the January 2027 offers went out before Christmas, and more were turned down over the holidays
            if r.random() < (0.13 if cohort.year < 2027 else 0.34):
                f.removed = cohort - dt.timedelta(days=int(r.integers(7, 15) if cohort.year < 2027 else r.integers(11, 21)))
                f.reason = "Declined offer"
                continue
            f.removed, f.reason = cohort, "Started programme"
            taken += 1
    for f in refs:
        if f.listed and f.removed is None and r.random() < 0.0045 * max(1, (K.CENSUS - f.listed).days / 30):
            d = f.listed + dt.timedelta(days=int(r.integers(20, 400)))
            if d <= dt.date(2027, 1, 6) and d != K.CENSUS:
                f.removed = d
                f.reason = "Discharged by team" if r.random() < 0.6 else "Moved out of area"
    for f in refs:
        if f.removed and f.removed > dt.date(2027, 1, 6):
            f.removed, f.reason = None, ""
        if f.removed:
            if f.removed >= dt.date(2026, 12, 21) and r.random() < 0.8:
                f.recorded = workday(dt.date(2027, 1, 4) + dt.timedelta(days=int(r.integers(0, 3))))
            else:
                f.recorded = workday(f.removed + dt.timedelta(days=int(r.integers(0, 4))))
            if f.recorded > K.PULL_HUB:
                f.removed, f.reason, f.recorded = None, "", None
    # patients the service had seen before: an earlier referral, closed well before the one open at the move
    r2 = K.rng("hub earlier")
    for f in list(refs):
        if r2.random() >= (0.2 if f.received < K.HUB_GOLIVE else 0.15):
            continue
        e = Ref()
        e.pt = f.pt
        e.received = f.received - dt.timedelta(days=int(r2.integers(120, 480)))
        while e.received.weekday() >= 5:
            e.received -= dt.timedelta(days=1)
        u = r2.random()
        e.outcome = "Not accepted" if u < 0.35 else "Returned to referrer" if u < 0.6 else "Accepted - DBT"
        e.triaged = workday(e.received + dt.timedelta(days=int(r2.integers(9, 40))))
        e.listed, e.removed, e.reason, e.recorded = None, None, "", None
        e.offers = []
        if e.outcome == "Accepted - DBT":
            e.listed = workday(e.triaged + dt.timedelta(days=int(r2.integers(0, 6))))
            span = (f.received - e.listed).days
            e.removed = e.listed + dt.timedelta(days=int(r2.integers(min(25, span // 3), max(26, span - 30))))
            e.reason = "Discharged by team"
            e.recorded = workday(e.removed + dt.timedelta(days=int(r2.integers(0, 4))))
        if (e.removed or e.triaged) > K.LEGACY_EXPORT - dt.timedelta(days=10):
            continue
        refs.append(e)
    # care episodes: some patients moved team after their referral
    by_pt = {}
    for f in refs:
        by_pt.setdefault(f.pt.number, []).append(f)
    for num, fs in by_pt.items():
        p = fs[0].pt
        last = max(fs, key=lambda z: z.received)
        rp = K.rng("hub episodes", p.number)
        start = min(z.received for z in fs) - dt.timedelta(days=int(rp.integers(60, 1500)))
        segs = [[p.team, start, None, ""]]
        if rp.random() < 0.11 and last.received < dt.date(2026, 11, 1):
            other = [c for c in TEAM_CODES if c != p.team][int(rp.integers(0, 10))]
            move = last.received + dt.timedelta(days=int(rp.integers(20, max(21, (dt.date(2026, 12, 20) -
                                                                                   last.received).days))))
            if move < dt.date(2026, 12, 20):
                segs[-1][2], segs[-1][3] = move - dt.timedelta(days=1), "Transfer"
                segs.append([other, move, None, ""])
        p.referring_team = p.team
        p.episodes = []
        for team, s, e, why in segs:
            if team == "BW-CM31" and s < K.MERGER:
                if e is not None and e < K.MERGER:
                    p.episodes.append([p.half, s, e, why])
                else:
                    p.episodes.append([p.half, s, K.MERGER - dt.timedelta(days=1), "Team merger"])
                    p.episodes.append(["BW-CM31", K.MERGER, e, why])
            else:
                p.episodes.append([team, s, e, why])
    # the move into the module
    used = set()
    for f in refs:
        f.migrated = False
        if f.received < K.HUB_GOLIVE:
            open_at = (f.removed is None or f.removed > K.LEGACY_EXPORT) and (
                f.outcome == "Accepted - DBT" or f.triaged > K.LEGACY_EXPORT)
            f.migrated = open_at
            if f.migrated:
                hi = len(MIGRATION)
                if f.removed is not None:
                    hi = max(1, sum(1 for d in MIGRATION if d < f.removed))
                f.mig_date = MIGRATION[int(r.integers(0, hi))]
        if f.received >= K.HUB_GOLIVE or f.migrated:
            while True:
                rid = "REF%08d" % int(r.integers(10_000_000, 99_999_999))
                if rid not in used:
                    used.add(rid)
                    break
            f.module_id = rid
        else:
            f.module_id = None
    # keep every team's mean wait clear of a rounding edge and apart from the module-date reading
    for _ in range(60):
        moved = False
        tru, mod = census(refs, True), census(refs, False)
        for team, v in tru.items():
            mean = sum(v) / len(v)
            mm = sum(mod[team]) / len(mod[team])
            edge = abs((mean * 10) % 1 - 0.5) < 0.12 or abs(round(mean, 1) - round(mm, 1)) < 0.05
            if edge:
                cands = sorted([f for f in refs if f.outcome == "Accepted - DBT" and f.listed and f.listed <= K.CENSUS
                                and not (f.removed and f.removed <= K.CENSUS)
                                and (f.migrated or f.received >= K.HUB_GOLIVE + dt.timedelta(days=7))
                                and f.received.timetuple().tm_yday > 7
                                and K.CURRENT[episode_team(f.pt, K.CENSUS)] == team], key=lambda f: f.pt.number)
                if cands:
                    f = cands[0]
                    f.received -= dt.timedelta(days=1)
                    while f.received.weekday() >= 5:
                        f.received -= dt.timedelta(days=1)
                    moved = True
        if not moved:
            break
    return pts, refs


def episode_team(p, day):
    for team, s, e, _ in p.episodes:
        if s <= day and (e is None or e >= day):
            return team
    return None


def module_rows(refs):
    rows = []
    for f in refs:
        if not f.module_id:
            continue
        team_at = episode_team(f.pt, min(f.received, K.HUB_GOLIVE) if f.migrated else f.received)
        if f.migrated:
            received = f.mig_date
            triaged = f.mig_date if f.triaged <= K.LEGACY_EXPORT else max(f.triaged, f.mig_date)
            listed = f.listed
            if f.listed:
                listed = f.mig_date if f.listed <= K.LEGACY_EXPORT else max(f.listed, f.mig_date)
        else:
            received, triaged, listed = f.received, f.triaged, f.listed
        rows.append([f.module_id, f.pt.number, team_at, received.isoformat(),
                     triaged.isoformat() if triaged <= K.PULL_HUB else "",
                     f.outcome if triaged <= K.PULL_HUB else "",
                     listed.isoformat() if listed and listed <= K.PULL_HUB else "",
                     f.removed.isoformat() if f.removed else "", f.reason,
                     f.recorded.isoformat() if f.recorded else ""])
    rows.sort(key=lambda z: (z[3], z[0]))
    return rows


UPDATES = [dt.date(2025, 3, 3), dt.date(2025, 9, 1), dt.date(2026, 3, 2), dt.date(2026, 9, 1)]


def letter_rows(refs, nhs):
    """The service's letters to the patients it was referred, as the trust's correspondence log holds them: the
    acknowledgement on the day a referral is received, the triage outcome, each offer of a place, the six-monthly
    waiting list update, a removal from the list. Letters held back while referrals were keyed into the module."""
    out = []
    for f in refs:
        rl = K.rng("letters", f.pt.number, f.received.isoformat())
        n = nhs[f.pt.number]
        how = "email" if rl.random() < 0.38 else "post"
        out.append((f.received, n, "Referral acknowledgement", how))
        if f.triaged <= K.PULL_HUB:
            out.append((workday(f.triaged + dt.timedelta(days=int(rl.integers(0, 3)))), n, "Triage outcome", how))
        for cohort in f.offers:
            out.append((cohort - dt.timedelta(days=int(rl.integers(21, 29))), n, "Offer of a place", how))
        for d in UPDATES:
            if f.listed and f.listed < d and not (f.removed and f.removed <= d):
                out.append((d, n, "Waiting list update", how))
        if f.reason in ("Discharged by team", "Moved out of area") and f.recorded:
            out.append((workday(f.recorded + dt.timedelta(days=int(rl.integers(0, 3)))), n, "Removal from waiting list",
                        how))
    out = [z for z in out if z[0] <= K.PULL_HUB]
    out.sort(key=lambda z: (z[0], z[1], z[2]))
    r = K.rng("letter ids")
    ids = sorted(int(x) for x in r.choice(np.arange(410_000, 499_999), size=len(out), replace=False))
    return [["L%07d" % i, n, d.strftime("%d/%m/%Y"), kind, how] for i, (d, n, kind, how) in zip(ids, out)]


def write_all(out_dir, refs, nhs):
    m = module_rows(refs)
    with open(os.path.join(out_dir, K.F_MODULE), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["referral_id", "patient_number", "referring_team_code", "date_received", "triage_date",
                    "triage_outcome", "dbt_list_added", "removed_on", "removal_reason", "removal_recorded_on"])
        w.writerows(m)
    lt = letter_rows(refs, nhs)
    with open(os.path.join(out_dir, K.F_LETTERS), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["letter_id", "nhs_number", "letter_date", "letter_type", "method"])
        w.writerows(lt)
    return {K.F_MODULE: len(m), K.F_LETTERS: len(lt)}


def census(refs, true_dates=True):
    """The truth the generator holds: each team's patients on the DBT list on 31 December 2026 and their waits in
    weeks since the service received the referral."""
    out = {}
    for f in refs:
        if f.outcome != "Accepted - DBT" or not f.listed or f.listed > K.CENSUS:
            continue
        if f.removed and f.removed <= K.CENSUS:
            continue
        team = K.CURRENT[episode_team(f.pt, K.CENSUS)]
        rec = f.received if (true_dates or not f.migrated) else f.mig_date
        out.setdefault(team, []).append((K.CENSUS - rec).days / 7.0)
    return out
