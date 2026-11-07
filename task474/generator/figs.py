"""Every owed figure, computed from the cut pack under target/ the way the golden reads it."""
import csv
import datetime as dt
import json
import os
from collections import defaultdict

import numpy as np

import pack as K
import params as P
import routes as R


def _rows(target, key):
    with open(os.path.join(target, K.FILES[key]), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def uk_date(stamp):
    t = dt.datetime.strptime(stamp, "%Y-%m-%dT%H:%M:00Z")
    return (t + dt.timedelta(hours=K.uk_offset(t.date()))).date()


def load(target, identity="name_dob", held="dedupe", zone="uk"):
    """the conformed record: person -> sittings, each {date, vendor, status, score, board}"""
    reg = _rows(target, "register")
    person = {}
    if identity == "name_dob":
        key = {}
        for g in reg:
            k = (g["surname"], g["initials"], g["date_of_birth"])
            person[g["board_number"]] = key.setdefault(k, len(key))
    else:
        for i, g in enumerate(reg):
            person[g["board_number"]] = i
    by_br = {g["brindle_candidate_id"]: g["board_number"] for g in reg if g["brindle_candidate_id"]}
    by_hg = {g["harrowgate_candidate_id"]: g["board_number"] for g in reg if g["harrowgate_candidate_id"]}
    people = defaultdict(list)
    for r in _rows(target, "brindle"):
        if r["status"] != "SAT":
            continue
        b = by_br[r["candidate_id"]]
        people[person[b]].append({"date": dt.datetime.strptime(r["sitting_date"], "%d/%m/%Y").date(), "vendor": "old",
                                  "status": "sat", "score": int(r["scaled_score"]), "board": b})
    hg = json.load(open(os.path.join(target, K.FILES["harrowgate"]), encoding="utf-8"))["sittings"]
    seen = {}
    for s in hg:
        if s["review"] not in ("cleared", "released", "held") or s["raw_mark"] is None:
            if not (held == "count" and s["review"] == "held"):
                continue
        if held == "dedupe" and s["sitting_ref"] in seen:
            continue
        seen[s["sitting_ref"]] = 1
        b = by_hg[s["candidate_id"]]
        d = uk_date(s["started_at"]) if zone == "uk" else dt.datetime.strptime(s["started_at"][:10], "%Y-%m-%d").date()
        people[person[b]].append({"date": d, "vendor": "new", "status": "sat",
                                  "score": s["raw_mark"] if s["raw_mark"] is not None else -1, "board": b})
    return {k: sorted(v, key=lambda s: (s["date"], s["vendor"])) for k, v in people.items()}, reg


def provider_of(reg, merged=True):
    """each board number's provider on its person's latest registration, merged providers mapped to their successor"""
    import world as W
    out = {}
    for g in reg:
        p = g["training_provider"]
        if merged and p in W.MERGED:
            p = W.MERGED[p][0]
        out[g["board_number"]] = p
    return out


def call(att):
    mark, p = R.r_matched(att)
    cs = [y for _, y in R.cross_switch(att)]
    a = np.array(cs)
    out = {"pass_mark": mark, "p_equivalent": round(float(p), 4), "n_cross_switch": len(cs),
           "share_at_mark": round(float((a >= mark).mean()), 4),
           "share_below_mark": round(float((a >= mark - 1).mean()), 4)}
    for k in ("p_equivalent", "share_at_mark", "share_below_mark"):
        out[k + "_pct"] = round(100 * out[k], 1)
    out.update({"standard": P.OLD_PASS, "items": P.NEW_ITEMS, "year": 2026, "mark_below": mark - 1})
    return out


def ask_a(people):
    """each month of 2026: candidates sitting the paper for the first time, and candidates resitting it"""
    out = {}
    for m in range(1, 10):
        out["2026-%02d" % m] = [0, 0]
    for ss in people.values():
        for i, s in enumerate(ss):
            if s["date"].year == 2026 and s["date"] <= P.LAST_DAY:
                k = "2026-%02d" % s["date"].month
                out[k][0 if i == 0 else 1] += 1
    return out


def ask_b2(people):
    """each year 2021 to 2025: candidates who first sat Brindle's paper that year, and how many passed at it"""
    out = {}
    for y in range(2021, 2026):
        firsts = [ss[0]["score"] >= P.OLD_PASS for ss in people.values()
                  if ss and ss[0]["vendor"] == "old" and ss[0]["date"].year == y]
        out[str(y)] = [len(firsts), int(sum(firsts))]
    return out


def ask_b(people, reg, merged=True, latest=True):
    prov = provider_of(reg, merged)
    boards_of = defaultdict(list)
    for g in reg:
        boards_of[g["board_number"]] = g
    out = defaultdict(int)
    for ss in people.values():
        new = [s for s in ss if s["vendor"] == "new"]
        if not new:
            continue
        b = new[0]["board"] if latest else ss[0]["board"]
        out[prov[b]] += 1
    import world as W
    return {code: out.get(code, 0) for code, _, _ in W.PROVIDERS if code not in W.MERGED or not merged}


def ask_c(people):
    out = {}
    for y in range(2021, 2026):
        firsts = [ss[0]["score"] >= P.OLD_PASS for ss in people.values()
                  if ss and ss[0]["vendor"] == "old" and ss[0]["date"].year == y]
        out[str(y)] = 100.0 * np.mean(firsts)
    return out


def chart_series(att):
    a = np.array([s["score"] for ss in att.values() for s in ss if s["vendor"] == "new"])
    return {y: round(100.0 * float((a >= y).mean()), 1) for y in range(20, 56)}


def compute(target):
    people, reg = load(target)
    att = R.attempts(people)
    c = call(att)
    ladder = {"same months a year earlier": R.r_same_months(att)[0], "the half before the switch": R.r_adjacent(att)[0],
              "retakes, first scores not matched": R.r_unmatched(att)[0], "both results side by side": R.r_side_by_side(att)[0],
              "first-timers, the winter halves' shift": R.r_did(att)[0], "retakes matched on the first score": c["pass_mark"]}
    a = ask_a(people)
    b = ask_b2(people)
    return {"call": c, "ladder": ladder,
            "ask_a": {k: {"first_time": v[0], "resitting": v[1]} for k, v in a.items()},
            "ask_b": {k: {"first_time": v[0], "passed": v[1]} for k, v in b.items()},
            "chart": {str(k): v for k, v in chart_series(att).items()}}
