"""task270 the asks, computed from the cut pack.

Ask A: each team's clinicians who can co-facilitate a skills group on 1 April 2027 under the DBT programme operating
standard's 4.2, and the whole-time equivalent their assignments in the team hold: a four-day DBT skills group facilitation course on the learning record (PTD-114 completed before the
catalogue rebuild of 1 April 2025, PTD-301, or the external four-day course EXT-0412), an assignment in a clinical staff
group in the team of 0.4 WTE or more on 1 April 2027, and no leaving date on or before 16 September 2027.

Ask B: the mean weeks the patients in each team's care on 31 December 2026 who were then on the DBT waiting list had
waited since the service received their referral; a referral moved over from the service's own database carries the
day the module record was created as its received date, and the day the service received it is the day of its
acknowledgement letter, the latest the correspondence log holds for the patient on or before that date."""
from __future__ import annotations

import datetime as dt
import os

import pandas as pd

import calc
import common as K

QUALIFY_OLD = "PTD-114"
QUALIFY = ("PTD-301", "EXT-0412")
ORG2TEAM = {n + " CMHT": c for c, n in K.TEAMS + K.OLD_TEAMS}


def _d(s):
    return dt.datetime.strptime(s, "%d/%m/%Y").date() if s else None


def ask_a(target=None, rule="golden"):
    """rule: golden; catalogue (the 2026 catalogue's four-day DBT courses only); every114 (every PTD-114 counted);
    no_chain (training under a previous employee number not followed)."""
    target = target or K.TARGET
    esr = pd.read_csv(os.path.join(target, K.F_ESR), dtype=str, keep_default_na=False)
    lr = pd.read_csv(os.path.join(target, K.F_LEARN), dtype=str, keep_default_na=False)
    trained = set()
    for num, code_, done in zip(lr.employee_number, lr.course_code, lr.completed_on):
        d = dt.date.fromisoformat(done)
        ok = code_ in QUALIFY
        if rule == "golden" or rule == "no_chain":
            ok = ok or (code_ == QUALIFY_OLD and d < K.CATALOGUE_REBUILD)
        elif rule == "every114":
            ok = ok or code_ == QUALIFY_OLD
        if ok:
            trained.add(num)
    out = {c: {} for c, _ in K.TEAMS}
    for r in esr.itertuples(index=False):
        if r.staff_group == "Administrative and Clerical":
            continue
        s, e, leave = _d(r.assignment_start), _d(r.assignment_end), _d(r.projected_leaving_date)
        if not (s <= K.GROUP_START and (e is None or e >= K.GROUP_START)):
            continue
        if float(r.assignment_wte) < 0.4:
            continue
        if leave is not None and leave <= K.GROUP_LAST:
            continue
        team = ORG2TEAM.get(r.organisation)
        if team not in out:
            continue
        nums = {r.employee_number} | ({r.previous_employee_number} if (r.previous_employee_number and rule != "no_chain")
                                      else set())
        if nums & trained:
            out[team][r.employee_number] = out[team].get(r.employee_number, 0) + round(float(r.assignment_wte) * 100)
    return {c: (len(v), sum(v.values()) / 100.0) for c, v in out.items()}


def ask_b(target=None, rule="golden"):
    """rule: golden; module (the module's received dates as they stand); drop (the referrals moved over left out);
    referring (the referring team instead of the team on 31 December); earliest (the patient's earliest
    acknowledgement); recorded (a removal counted only once recorded by 31 December)."""
    target = target or K.TARGET
    m = pd.read_csv(os.path.join(target, K.F_MODULE), dtype=str, keep_default_na=False)
    lt = pd.read_csv(os.path.join(target, K.F_LETTERS), dtype=str, keep_default_na=False)
    ix = pd.read_csv(os.path.join(target, K.F_INDEX), dtype=str, keep_default_na=False)
    nhs = dict(zip(ix.patient_number, ix.nhs_number))
    acks = {}
    for n, d, kind in zip(lt.nhs_number, lt.letter_date, lt.letter_type):
        if kind == "Referral acknowledgement":
            acks.setdefault(n, []).append(_d(d))
    eps = calc.episodes(target)
    waits = {c: [] for c, _ in K.TEAMS}
    for r in m.itertuples(index=False):
        if r.triage_outcome != "Accepted - DBT" or not r.dbt_list_added:
            continue
        if dt.date.fromisoformat(r.dbt_list_added) > K.CENSUS:
            continue
        if r.removed_on and dt.date.fromisoformat(r.removed_on) <= K.CENSUS:
            if not (rule == "recorded" and dt.date.fromisoformat(r.removal_recorded_on) > K.CENSUS):
                continue
        mod = dt.date.fromisoformat(r.date_received)
        first = max(d for d in acks[nhs[r.patient_number]] if d <= mod)
        if rule == "drop" and first != mod:
            continue
        rec = {"module": mod, "earliest": min(acks[nhs[r.patient_number]])}.get(rule, first)
        if rule == "referring":
            team = K.CURRENT[r.referring_team_code]
        else:
            team = K.CURRENT[calc.team_on(eps, r.patient_number, K.CENSUS)]
        waits[team].append((K.CENSUS - rec).days / 7.0)
    return {c: (len(v), (sum(v) / len(v)) if v else None) for c, v in waits.items()}
