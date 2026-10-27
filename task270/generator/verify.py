"""task270 independent verifier: every graded figure recomputed from the cut pack alone with its own readers and its own
arithmetic (the csv module and openpyxl, no pandas, no generator module), then compared with generator/figures.json.
The call: each patient's latest 2026 fortnight with at least 56 of its 112 prompts answered, the team on its first
day, negative affect as the mean of four items on 0 to 10, instability as the root mean square change between same-day
ratings 2.5 to 3.5 hours apart, a team funded at 30 per cent or more at 2.0. Ask A: the DBT programme standard's 4.2
with PTD-114 counted as the four-day course before the catalogue gave the code to the refresher. Ask B: the module's
waiting list on 31 December 2026, each referral dated by the service's acknowledgement letter, the latest for the
patient on or before the module's received date. Exit 1 on any difference.

    python3 task270/generator/verify.py [TARGET]"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import os
import sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
TARGET = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
CENSUS = dt.date(2026, 12, 31)
GROUP_START, GROUP_LAST = dt.date(2027, 4, 1), dt.date(2027, 9, 16)
MERGED = {"BW-CM14": "BW-CM31", "BW-CM15": "BW-CM31"}
FAIL = []


def check(label, ok, detail=""):
    print("%s  %s%s" % ("ok  " if ok else "FAIL", label, ("  [%s]" % detail) if detail else ""))
    if not ok:
        FAIL.append(label)


def find(prefix):
    hits = [f for f in os.listdir(TARGET) if f.startswith(prefix)]
    assert len(hits) == 1, (prefix, hits)
    return os.path.join(TARGET, hits[0])


def rows(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def last_sunday(year, month):
    d = dt.date(year, month + 1, 1) - dt.timedelta(days=1)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def uk(t):
    """A UTC time as UK wall time: summer time from 01:00 UTC on the last Sunday of March to 01:00 UTC on the last
    Sunday of October."""
    on = dt.datetime.combine(last_sunday(t.year, 3), dt.time(1))
    off = dt.datetime.combine(last_sunday(t.year, 10), dt.time(1))
    return t + dt.timedelta(hours=1) if on <= t < off else t


def team(code):
    return MERGED.get(code, code)


# ------------------------------------------------------------------------------------------------------ the call
def ratings():
    code2pt = {r["participant_code"]: r["patient_number"] for r in rows(find("mood_app_enrolments"))}
    out = []                       # (patient, sent local, answered local or None, negative affect or None)
    v3 = rows(find("mood_app_export_v3"))
    top = max(float(r[k]) for r in v3 if r["responded_local"] for k in ("na_down_vas", "na_anxious_vas"))
    check("control: version 3's sliders run above 10 (a 0 to 100 scale)", top > 10, "%g" % top)
    for r in v3:
        sent = dt.datetime.strptime(r["scheduled_local"], "%d/%m/%Y %H:%M")
        if r["responded_local"]:
            ans = dt.datetime.strptime(r["responded_local"], "%d/%m/%Y %H:%M:%S")
            na = sum(float(r[k]) for k in ("na_down_vas", "na_anxious_vas", "na_irritable_vas", "na_ashamed_vas")) / 40
        else:
            ans, na = None, None
        out.append((code2pt[r["participant_id"]], sent, ans, na))
    v4 = rows(find("mood_app_export_v4"))
    seen, dup = set(), 0
    for r in v4:
        if r["prompt_id"] in seen:
            dup += 1
            continue
        seen.add(r["prompt_id"])
        sent = uk(dt.datetime.strptime(r["sent_at_utc"], "%Y-%m-%dT%H:%M:%SZ"))
        if r["status"] == "answered":
            ans = uk(dt.datetime.strptime(r["answered_at_utc"], "%Y-%m-%dT%H:%M:%SZ"))
            na = sum(float(r[k]) for k in ("down", "anxious", "irritable", "ashamed")) / 4
        else:
            ans, na = None, None
        out.append((code2pt[r["participant"]], sent, ans, na))
    check("control: version 4 resends a prompt's answer (repeated prompt ids)", dup > 0, "%d repeats" % dup)
    hours = [a.hour for _p, _s, a, _n in out if a is not None]
    check("control: every answer in UK time falls between 9:00 and 22:00", min(hours) >= 9 and max(hours) <= 21,
          "%d to %d" % (min(hours), max(hours)))
    return out


def episodes():
    out = {}
    for r in rows(find("cmht_care_episodes")):
        e = dt.date.fromisoformat(r["episode_end"]) if r["episode_end"] else None
        out.setdefault(r["patient_number"], []).append((r["team_code"], dt.date.fromisoformat(r["episode_start"]), e))
    return out


def team_on(eps, pt, day):
    for t, s, e in eps.get(pt, []):
        if s <= day and (e is None or e >= day):
            return team(t)
    return None


def call():
    R = ratings()
    by_pt = {}
    for p, s, a, na in R:
        by_pt.setdefault(p, []).append((s, a, na))
    wb = openpyxl.load_workbook(find("assessment_fortnights_register"), read_only=True)
    reg = list(wb.active.iter_rows(values_only=True))
    head = list(reg[0])
    ip, i0, i1 = head.index("Patient number"), head.index("First day"), head.index("Last day")
    eps = episodes()
    latest = {}
    for r in reg[1:]:
        pt, f, l = str(r[ip]), r[i0].date(), r[i1].date()
        if not (dt.date(2026, 1, 1) <= f <= dt.date(2026, 12, 31)):
            continue
        n = sum(1 for s, a, _na in by_pt.get(pt, []) if a is not None and f <= s.date() <= l)
        if n >= 56 and (pt not in latest or f > latest[pt][0]):
            latest[pt] = (f, l)
    res = {}
    for pt, (f, l) in latest.items():
        days = {}
        for s, a, na in by_pt[pt]:
            if a is not None and f <= s.date() <= l:
                days.setdefault(s.date(), []).append((a, na))
        sq = []
        for d, xs in days.items():
            xs.sort()
            for i in range(len(xs)):
                for j in range(i + 1, len(xs)):
                    g = (xs[j][0] - xs[i][0]).total_seconds() / 3600
                    if 2.5 <= g <= 3.5:
                        sq.append((xs[j][1] - xs[i][1]) ** 2)
        res[pt] = (team_on(eps, pt, f), math.sqrt(sum(sq) / len(sq)))
    teams = sorted({t for t, _v in res.values()})
    sh = {t: (sum(1 for tt, v in res.values() if tt == t and v >= 2.0), sum(1 for tt, _v in res.values() if tt == t))
          for t in teams}
    return res, sh


# ------------------------------------------------------------------------------------------------------- Ask A
def ask_a():
    wb = openpyxl.load_workbook(find("learning_catalogue"), read_only=True)
    cat = {r[0]: r for r in list(wb.active.iter_rows(values_only=True))[1:]}
    cut = cat["PTD-114"][3].date()
    check("control: the 2026 catalogue gives PTD-114 to a one-day refresher first offered on the rebuild",
          cat["PTD-114"][2] == 1 and cut == dt.date(2025, 4, 1), str(cut))
    trained = set()
    for r in rows(find("learning_records")):
        d = dt.date.fromisoformat(r["completed_on"])
        if r["course_code"] in ("PTD-301", "EXT-0412") or (r["course_code"] == "PTD-114" and d < cut):
            trained.add(r["employee_number"])
    out = {}
    for r in rows(find("esr_clinical_assignments")):
        if r["staff_group"] == "Administrative and Clerical" or float(r["assignment_wte"]) < 0.4:
            continue
        s = dt.datetime.strptime(r["assignment_start"], "%d/%m/%Y").date()
        e = dt.datetime.strptime(r["assignment_end"], "%d/%m/%Y").date() if r["assignment_end"] else None
        lv = dt.datetime.strptime(r["projected_leaving_date"], "%d/%m/%Y").date() if r["projected_leaving_date"] else None
        if s > GROUP_START or (e is not None and e < GROUP_START) or (lv is not None and lv <= GROUP_LAST):
            continue
        if not r["organisation"].endswith(" CMHT"):
            continue
        if {r["employee_number"], r["previous_employee_number"]} & trained:
            team_ = out.setdefault(r["organisation"][:-5], {})
            team_[r["employee_number"]] = team_.get(r["employee_number"], 0) + int(r["assignment_wte"].replace(".", ""))
    return {k: (len(v), sum(v.values())) for k, v in out.items()}


# ------------------------------------------------------------------------------------------------------- Ask B
def ask_b():
    nhs = {r["patient_number"]: r["nhs_number"] for r in rows(find("patient_index_extract"))}
    acks = {}
    for r in rows(find("cen_correspondence_log")):
        if r["letter_type"] == "Referral acknowledgement":
            acks.setdefault(r["nhs_number"], []).append(dt.datetime.strptime(r["letter_date"], "%d/%m/%Y").date())
    eps = episodes()
    waits = {}
    moved = 0
    for r in rows(find("cen_referrals_module_export")):
        if r["triage_outcome"] != "Accepted - DBT" or not r["dbt_list_added"]:
            continue
        if dt.date.fromisoformat(r["dbt_list_added"]) > CENSUS:
            continue
        if r["removed_on"] and dt.date.fromisoformat(r["removed_on"]) <= CENSUS:
            continue
        mod = dt.date.fromisoformat(r["date_received"])
        rec = max(d for d in acks[nhs[r["patient_number"]]] if d <= mod)
        moved += rec != mod
        waits.setdefault(team_on(eps, r["patient_number"], CENSUS), []).append((CENSUS - rec).days)
    check("control: some waiting patients' referrals were keyed in from the service's database", moved > 30,
          "%d" % moved)
    return {t: (len(v), sum(v) / len(v) / 7) for t, v in waits.items()}


def half_up(x):
    return math.floor(x * 10 + 0.5 + 1e-9) / 10


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    names = {}
    for r in rows(find("cmht_care_episodes")):
        names[team(r["team_code"])] = r["team_name"][:-5] if r["team_code"] not in MERGED else "Haddersley"
    res, sh = call()
    check("population: patients counted", len(res) == F["patients_assessed"], "%d" % len(res))
    funded = sorted(names[t] for t, (h, n) in sh.items() if 100.0 * h / n >= 30)
    check("call: the funded teams", funded == sorted(F["funded"]), ", ".join(funded))
    for t, (h, n) in sh.items():
        check("call: %s assessed patients" % names[t], n == F["assessed_" + t], "%d" % n)
        check("call: %s group" % names[t], ("Yes" if 100.0 * h / n >= 30 else "No") == F["group_" + t],
              "%.1f per cent" % (100.0 * h / n))
    A = ask_a()
    for t in sh:
        n, w = A.get(names[t], (0, 0))
        check("Ask A: %s co-facilitators and their whole-time equivalent" % names[t],
              n == F["cofacilitators_" + t] and "%d.%02d" % divmod(w, 100) == F["wte_" + t], "%d, %d hundredths" % (n, w))
    B = ask_b()
    for t in sh:
        n, m = B[t]
        check("Ask B: %s mean weeks" % names[t], "%.1f" % half_up(m) == F["mean_weeks_" + t] and n == F["waiting_" + t],
              "%d waiting, %.3f weeks" % (n, m))
    print("verify: %d failed" % len(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
