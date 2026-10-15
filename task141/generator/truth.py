"""The clean truth's own answers, from the world before any export is written: each score's safety rate had every
eligible defendant been released, and the three asks' figures. checks.py holds the pack's golden to these."""
from __future__ import annotations

import datetime as dt

import common as K
import world as WD

DAY = dt.timedelta(days=1)


def _offs(W):
    offs = {}
    for a in W.arrests:
        if a["type"] == "NEW":
            offs.setdefault(a["pid"], []).append(a["offence_date"])
    for v in offs.values():
        v.sort()
    return offs


def history_eps(W):
    """The eligible, screened first appearances whose windows close inside the extract."""
    return [e for e in W.eps if e["eligible"] and e["screened"] and K.HIST_START <= e["fa_t"].date() <= K.HIST_LAST]


def safety_truth(W):
    """Each score's share with no new-offence arrest in the window had every one been released: the released
    defendants' own outcomes and, for the held, the outcome drawn for release at first appearance (an arrest within
    the window, the warrant share taken out as the extract's typing takes it)."""
    offs = _offs(W)
    num, den, sel = {}, {}, {}
    for e in history_eps(W):
        s = e["nca"]
        den[s] = den.get(s, 0) + 1
        if e["released24"]:
            a = e["rel_t"].date()
            b = min(a + dt.timedelta(days=K.WINDOW_DAYS), e["last_disp"])
            y = float(any(a < o <= b for o in offs.get(e["pid"], [])))
            sel[s] = sel.get(s, 0.0) + y
        else:
            y = float(e["cf"]) * (1 - WD.P_WARRANT)
        num[s] = num.get(s, 0.0) + y
    return {s: 1 - num[s] / den[s] for s in sorted(den)}


def selection_by_score(W):
    """The share of each score's eligible defendants with the trait the magistrate sees, overall and among the
    released."""
    out = {}
    for e in history_eps(W):
        d = out.setdefault(e["nca"], [0, 0, 0, 0])
        d[0] += 1
        d[1] += int(e["D"])
        if e["released24"]:
            d[2] += 1
            d[3] += int(e["D"])
    return {s: (v[1] / v[0], v[3] / v[2]) for s, v in sorted(out.items())}


def ask_a_truth(W):
    """Bed-days in custody to the count at 00:00 on 30 September 2026 of the eligible defendants held after a first
    appearance in the year, by score: every Eastern midnight from booking to release, at Dorrance or at Halsey."""
    end_t = K.d2dt(K.EXTRACT_END + DAY)
    res = {}
    for e in W.eps:
        if not (K.FY26_START <= e["fa_t"].date() <= K.EXTRACT_END) or not e["eligible"] or not e["screened"]:
            continue
        if e["released24"]:
            continue
        a, b = e["stays"][0]["start"], min(e["stays"][-1]["end"], end_t)
        n = sum(1 for d in K.midnights(a, b) if d <= K.EXTRACT_END)
        res[e["nca"]] = res.get(e["nca"], 0) + n
    return res


def ask_b_truth(W):
    """Releases at first appearances from 1 October 2025 to 30 June 2026 followed within 90 days by a missed court
    date in any of the appearance's cases, the superior court case an indictment opens included: (missed, releases)
    by failure-to-appear score."""
    by_eid = {}
    for cd in W.court:
        if cd["fta"]:
            by_eid.setdefault(cd["eid"], []).append(cd["date"])
    res = {}
    for e in W.eps:
        if not (K.FY26_START <= e["fa_t"].date() <= K.ASKB_LAST) or not e["released24"] or not e["screened"]:
            continue
        a = e["rel_t"].date()
        b = a + dt.timedelta(days=90)
        hit = any(a <= d <= b for d in by_eid.get(e["eid"], []))
        n, m = res.get(e["fta"], (0, 0))
        res[e["fta"]] = (n + int(hit), m + 1)
    return res


def ask_c_truth(W):
    """Calendar days on electronic monitoring to 30 September 2026 of the defendants released at a first appearance
    in the year, by score: the union of each release's enrollments, every day a unit was on the defendant."""
    days = {}
    for m in W.em:
        e = W.eps[m["eid"]]
        if not e["screened"]:
            continue
        end = m["end"] or K.EXTRACT_END
        s = days.setdefault(m["eid"], set())
        d = m["start"]
        while d <= end:
            s.add(d)
            d += DAY
    res = {}
    for eid, s in days.items():
        sc = W.eps[eid]["nca"]
        res[sc] = res.get(sc, 0) + len(s)
    return res
