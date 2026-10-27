"""task270 checks: the three rules on the generator's clean truth, the call on the cut pack, the standing family and
the ladder's wrong rungs, every semantic fork, the Layer 1 mess on the call's path, the asks' fairness, devices and
stops, the separation of the asks from the call, the invented names, the realism sweep and the pack's gates.
Exit 1 on any failure.

    python3 task270/generator/checks.py [TARGET]"""
from __future__ import annotations

import datetime as dt
import json
import math
import os
import re
import sys
import zipfile

import numpy as np
import openpyxl
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A        # noqa: E402
import calc as C        # noqa: E402
import common as K      # noqa: E402
import cracker as CR    # noqa: E402
import docs as D        # noqa: E402
import hub as H         # noqa: E402
import staff as S       # noqa: E402
import world as W       # noqa: E402

ROWS = []
# real places a screen of the reference list misses, read from a gazetteer by hand: each sits within two edits of a
# name this build once used, or of a distinctive word it uses now
EXTRA_PLACES = ["quenby", "rushmere", "overgate", "pendle", "hollinsmere", "fennacre", "skelton", "lowfield",
                "brindle", "wendover", "dunnerdale", "drayton", "cressage", "rennington", "ashwater", "bramwith",
                "garthorpe", "hesketh", "torrington", "wynford", "fordwich", "wrabness", "hartwick", "sedgefield",
                "skelwith", "borrowdale"]


def row(label, ok, detail=""):
    ROWS.append((label, bool(ok), detail))


def names(codes):
    return ", ".join(K.TEAM_NAME[c] for c, _n in K.TEAMS if c in codes)


def na_of(vals, version):
    items = np.clip(np.round(vals * 10), 0, 100) / 10.0 if version == 3 else np.clip(np.round(vals), 0, 10)
    return float(items.mean())


def clean_truth(patients):
    """Each patient's latest completed fortnight read straight from the world (no export, no join, no clock): the
    easy route's change between adjacent prompts and the three-hour change, and the world's own long-run three-hour
    instability."""
    out = []
    for p in patients:
        kind, first, c, swap, c2, rows = [z for z in p.fortnight_rows if z[0] == "latest"][0]
        ans = [(k, b, a, na_of(v, 3 if a.date() < K.V4_FROM else 4)) for k, b, s, a, v in rows if a is not None]
        by = {}
        for k, b, a, y in ans:
            by.setdefault(k, []).append((b, a, y))
        adj, w = [], []
        for xs in by.values():
            xs.sort()
            for i in range(len(xs)):
                for j in range(i + 1, len(xs)):
                    g = (xs[j][1] - xs[i][1]).total_seconds() / 3600
                    if xs[j][0] == xs[i][0] + 1:
                        adj.append((xs[j][2] - xs[i][2]) ** 2)
                    if 2.5 <= g <= 3.5:
                        w.append((xs[j][2] - xs[i][2]) ** 2)
        out.append(dict(team=p.team, R1=math.sqrt(np.mean(adj)), W=math.sqrt(np.mean(w)), T=W.truth_rmssd(p)))
    return out


def set_of(res, route):
    teams = [c for c, _ in K.TEAMS]
    sh = {c: [o[route] >= K.HIGH for o in res if o["team"] == c] for c in teams}
    return sorted(c for c in teams if 100 * np.mean(sh[c]) >= K.LINE)


def pct(sh):
    return {c: 100 * v["share"] for c, v in sh.items()}


def slot_rmssd(g, mode, w):
    """The collaborative's schedule laid over one patient fortnight's ratings: for each day and each of its times
    (9:00 to 21:00), the trust rating nearest the time within w minutes (mode near) or answered in the w minutes
    after it (mode after), and the root mean square change between adjacent times both filled."""
    sq = []
    for _day, d in g.groupby("day"):
        t = (d.answered.dt.hour + d.answered.dt.minute / 60 + d.answered.dt.second / 3600).to_numpy()
        y = d.na.to_numpy()
        vals = []
        for T in K.COLLAB_TIMES:
            m = ((t >= T) & (t <= T + w / 60)) if mode == "after" else (np.abs(t - T) <= w / 60)
            vals.append(y[np.where(m)[0][np.argmin(np.abs(t[m] - T))]] if m.any() else None)
        sq.extend((b - a) ** 2 for a, b in zip(vals, vals[1:]) if a is not None and b is not None)
    return (math.sqrt(np.mean(sq)) if sq else float("nan")), len(sq)


def _ed(a, b):
    if abs(len(a) - len(b)) > 2:
        return 9
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        prev = cur
    return prev[-1]


def main(target=K.TARGET):
    patients, extra = W.build()
    # ---------------------------------------------------------------------------------- the three rules, clean truth
    ct = clean_truth(patients)
    truth = set_of(ct, "T")
    easy, dec = set_of(ct, "R1"), set_of(ct, "W")
    row("R3a ANALYST the easy route on the clean truth (the change between adjacent prompts) names another set",
        easy != truth, "%s against %s" % (names(easy), names(truth)))
    row("R3a ANALYST the easy route funds the two hub teams alone and every team it funds is in the golden set",
        easy == ["BW-CM02", "BW-CM05"] and set(easy) <= set(truth), names(easy))
    row("R3b DECISIVE the three-hour change on the clean truth names the world's own set", dec == truth, names(dec))
    row("R3b DECISIVE the world's own three-hour instability funds five teams", len(truth) == 5, names(truth))
    row("R2 LAYER the decisive step flips the call with every file clean (no export, join, clock or scale to read)",
        easy != dec, "")
    heads = []
    for f in os.listdir(target):
        if f.endswith(".csv"):
            with open(os.path.join(target, f), encoding="utf-8") as fh:
                heads.append(fh.readline().lower())
    row("R1 RAW the pack ships the momentary ratings at the prompt grain and no instability figure for any patient",
        not any(re.search(r"instab|rmssd|mssd|variab", h) for h in heads), "")
    # ------------------------------------------------------------------------------------------------ the call
    allp, reg, eps, pop, res = C.main_call(target)
    row("R1 RAW the exports carry 25,000 or more prompts with their send and answer times",
        len(allp) >= 25000, "%d prompts" % len(allp))
    sh = {r: C.shares(res, r) for r in C.ROUTES}
    gold = C.funded(sh["W"])
    row("CALL the golden route on the pack names the clean truth's set", gold == truth, names(gold))
    n_pack = {c: v["n"] for c, v in sh["W"].items()}
    n_world = {c: sum(1 for p in patients if p.team == c) for c, _ in K.TEAMS}
    row("CALL every team's assessed patients on the pack equal the world's", n_pack == n_world,
        ", ".join("%s %d" % (K.TEAM_NAME[c], n_pack[c]) for c, _ in K.TEAMS))
    fam = ("W", "W2", "K2", "E", "ET")
    lo_in = min(pct(sh[r])[c] for r in fam for c in gold)
    hi_out = max(pct(sh[r])[c] for r in fam for c, _ in K.TEAMS if c not in gold)
    row("CALL every funded team at 38 per cent or more and every other at 20 or less under every standing member",
        lo_in >= 38 and hi_out <= 20, "lowest funded %.1f, highest left out %.1f" % (lo_in, hi_out))
    for r in fam:
        row("FAMILY %s names the golden set" % r, C.funded(sh[r]) == gold,
            " ".join("%.1f" % pct(sh[r])[c] for c, _ in K.TEAMS))
    tw = {c: 100 * np.mean([o["T"] >= K.HIGH for o in ct if o["team"] == c]) for c, _ in K.TEAMS}
    row("FAMILY the world's own three-hour instability names the golden set, every share 10 points or more from 30",
        min(abs(v - K.LINE) for v in tw.values()) >= 10, " ".join("%.1f" % tw[c] for c, _ in K.TEAMS))
    by_pt = {pt: g for pt, g in allp[allp.answered.notna()].groupby("patient")}
    for mode, w in (("near", 45), ("near", 60), ("near", 90), ("after", 45)):
        got, none = {c: [] for c, _ in K.TEAMS}, 0
        npairs = []
        for pt, f, l, team in pop:
            g = by_pt[pt]
            v, n = slot_rmssd(g[(g.day >= f) & (g.day <= l)], mode, w)
            npairs.append(n)
            if n:
                got[team].append(v >= K.HIGH)
            else:
                none += 1
        shs = {c: 100 * np.mean(v) for c, v in got.items()}
        fs = sorted(c for c, v in shs.items() if v >= K.LINE)
        detail = "%s; a median of %d pairs a patient, %d patients with none" % (
            " ".join("%.1f" % shs[c] for c, _ in K.TEAMS), int(np.median(npairs)), none)
        if mode == "near":
            row("FAMILY the trust rating nearest each of the collaborative's times, within %d minutes, names the golden "
                "set" % w, fs == gold, detail)
        else:
            row("RECORD only the ratings answered in the 45 minutes after each of the collaborative's times cannot "
                "measure every counted patient (the trust app sends nothing after 21:00), so it is no standing member; "
                "it names %s" % names(fs), none > 0 and fs != gold, detail)
    added = [c for c in gold if c not in ("BW-CM02", "BW-CM05")]
    spread = {c: max(pct(sh[r])[c] for r in fam) - min(pct(sh[r])[c] for r in fam) for c in added}
    row("FAMILY the standing family's spread on the three teams the step adds (points of share)", True,
        ", ".join("%s %.1f" % (K.TEAM_NAME[c], v) for c, v in spread.items()))
    shw = sh["W"]
    row("CALL no team's golden share is a round figure", all(abs(100 * v["share"] - round(100 * v["share"])) > 0.04
                                                             or round(100 * v["share"]) % 5 for v in shw.values()), "")
    # ------------------------------------------------------------------------------------------- the rungs, Gate F
    for r in ("R0", "R1", "R2"):
        row("RUNG %s names another set (%s)" % (r, names(C.funded(sh[r]))), C.funded(sh[r]) != gold,
            " ".join("%.1f" % pct(sh[r])[c] for c, _ in K.TEAMS))
    row("RUNG R1 and R2 fund the two hub teams alone", C.funded(sh["R1"]) == C.funded(sh["R2"]) == ["BW-CM02", "BW-CM05"],
        "")
    row("RUNG R1, the default path, leaves every added team at 25 per cent or less",
        max(pct(sh["R1"])[c] for c in added) <= 25, " ".join("%.1f" % pct(sh["R1"])[c] for c in added))
    rounded = {}
    for r in ("R1", "R2", "R0"):
        res_r = [dict(o, **{r: K.round_half_up(o[r], 1)}) for o in res]
        rounded[r] = C.funded(C.shares(res_r, r))
        row("RUNG %s with each patient's figure first rounded to one decimal (standard 4.1) names another set" % r,
            rounded[r] != gold, names(rounded[r]))
    land = sum(C.funded(sh[r]) == gold for r in ("R0", "R1", "R2")) + sum(v == gold for v in rounded.values())
    row("GATE F cheap routes landing the call on the pack (adjacent, successive, across the fortnight, each rounded)",
        land == 0, "%d of 6" % land)
    row("RECORD R3 (each adjacent change stretched to three hours in proportion) takes the decisive step crudely and "
        "names the golden set", C.funded(sh["R3"]) == gold, " ".join("%.1f" % pct(sh["R3"])[c] for c, _ in K.TEAMS))
    m1, n1 = C.pooled_change(allp, pop, 1.0, 1.75)
    m3, n3 = C.pooled_change(allp, pop, 2.5, 3.5)
    row("RECORD the mean squared change grows with the time between same-day ratings", m3 > 1.5 * m1,
        "%.2f at 1 to 1.75 hours (%d pairs), %.2f at 2.5 to 3.5 hours (%d pairs)" % (m1, n1, m3, n3))
    row("RECORD the trust app's adjacent prompts sat about 90 minutes apart (median, both answered)",
        80 <= C.adjacent_gap_median(allp, pop) <= 95, "%.1f minutes" % C.adjacent_gap_median(allp, pop))
    # ------------------------------------------------------------------------------------------- semantic forks
    paper = D.text_of_sections(D.PAPER)
    std = D.text_of_sections(D.STANDARD)
    dbt = D.text_of_sections(D.DBT_STANDARD)

    def funded_with(rule="latest", completion="answered", team_day="first", **load):
        ap = C.load(target, **load) if load else allp
        pp = C.population(ap, reg, eps, rule, completion, team_day)
        return C.funded(C.shares(C.instability(ap, pp, fits=False), "W")), len(pp)

    raw = {}
    for pt, f, l, t in pop:
        raw.setdefault(C.team_on(eps, pt, f), []).append(pt)
    row("SF1 teams as they stand from 1 October 2026, the two Haddersley teams as one (paper, section 2)",
        "Haddersley North and Haddersley South as one team" in paper and {"BW-CM14", "BW-CM15"} <= set(raw),
        "%d and %d patients on a first day before the merger" % (len(raw["BW-CM14"]), len(raw["BW-CM15"])))
    for rule in ("every", "earliest"):
        f2, n2 = funded_with(rule=rule)
        row("SF2 each patient once on their latest completed fortnight (paper, section 2); %s instead, same call" % rule,
            "latest assessment fortnight of 2026 that was completed" in paper and f2 == gold, "%d fortnights" % n2)
    f3, n3_ = funded_with(completion="status")
    row("SF3 completed as half or more of the 112 prompts answered (paper, section 2); the register's status instead, "
        "same call", "answered at least half of its 112 prompts" in paper and f3 == gold, "%d patients" % n3_)
    regd = reg[(reg["First day"] >= K.YEAR0) & (reg["First day"] <= K.YEAR1)]
    row("SF4 every 2026 fortnight begins and ends inside the year", (regd["Last day"] <= K.YEAR1).all(), "")
    for td in ("enrolled", "census"):
        f5, _n5 = funded_with(team_day=td)
        row("SF5 the team holding the patient's care on the fortnight's first day (paper, section 2); on the %s day "
            "instead, same call" % td, "that held their care on the fortnight's first day" in paper and f5 == gold,
            names(f5))
    f6, _n6 = funded_with(scale_v3=1.0)
    row("SF6 every item on 0 to 10 (standard 2.2), version 3's sliders read divided by ten; unscaled, every team "
        "is funded (refuted by the scale)", "scored from 0 (not at all) to 10" in std and f6 != gold, names(f6))
    row("SF7 adjacent prompts on the same day where both were answered (standard 3.2)",
        "between adjacent prompts on the same day where both were answered" in std, "")
    ans = allp[allp.answered.notna()]
    lt = ans.answered.dt.hour + ans.answered.dt.minute / 60.0
    row("SF8 the same day in UK or UTC time: no answer within an hour of midnight in either", lt.min() >= 9 and
        lt.max() < 22.5, "%.2f to %.2f local" % (lt.min(), lt.max()))
    row("SF9 as the collaborative's app will measure it: every standing reading names the golden set (FAMILY rows)",
        all(C.funded(sh[r]) == gold for r in fam), "")
    res1 = [dict(o, W=K.round_half_up(o["W"], 1)) for o in res]
    row("SF10 2.0 or more (standard 3.3) on the unrounded figure; rounded to one decimal first, or more than 2.0, "
        "same call", C.funded(C.shares(res1, "W")) == gold and
        C.funded(C.shares([dict(o, W=o["W"] - 1e-9) for o in res], "W")) == gold,
        "%d patients between 1.95 and 2.0" % sum(1 for o in res if 1.95 <= o["W"] < 2.0))
    row("SF11 30 per cent or more (paper, section 2): no team within 8 points of 30 under any standing reading",
        min(abs(pct(sh[r])[c] - K.LINE) for r in fam for c, _ in K.TEAMS) >= 8, "")
    f12, _n12 = funded_with(drop_second_codes=True)
    en = pd.read_csv(os.path.join(target, K.F_ENROL), dtype=str)
    two = en.groupby("patient_number").participant_code.nunique()
    row("SF12 a patient re-enrolled on a new phone is one patient across both codes (the enrolment log); the second "
        "code's ratings dropped instead, same call", f12 == gold, "%d patients with two codes in a fortnight"
        % int((en.end_reason == "replaced phone").sum()))
    f13, _n13 = funded_with(keep_resends=True)
    row("SF13 an answer version 4 sent twice is one rating; kept twice, same call", f13 == gold, "")
    f14, _n14 = funded_with(scheduled_clock=True)
    row("SF14 a rating at its answer time; at its prompt's send time instead, same call", f14 == gold, names(f14))
    # ------------------------------------------------------------------------------------------- Layer 1, the call
    v3 = pd.read_csv(os.path.join(target, K.F_V3), dtype=str, keep_default_na=False)
    v4 = pd.read_csv(os.path.join(target, K.F_V4), dtype=str, keep_default_na=False)
    row("L1 the app's version 4 export changed layout, scale and clock on 15 June 2026",
        "na_down_vas" in v3.columns and "down" in v4.columns and v4.sent_at_utc.str.endswith("Z").all()
        and v3.scheduled_local.str.contains("/").all(), "")
    split = 0
    for r in regd.itertuples(index=False):
        if r[3] < K.V4_FROM <= r[4]:
            split += 1
    row("L1 fortnights split across the two exports", split >= 5, "%d fortnights" % split)
    bst = sum(1 for r in regd.itertuples(index=False) if r[3] <= K.BST_END.date() <= r[4]
              or r[3] <= K.BST_START.date() <= r[4])
    row("L1 fortnights across a clock change", bst >= 5, "%d fortnights" % bst)
    row("L1 version 4 resent some answers (exact repeated rows)", int(v4.duplicated().sum()) >= 100,
        "%d repeated rows" % int(v4.duplicated().sum()))
    E_ = pd.read_csv(os.path.join(target, K.F_EPISODES), dtype=str, keep_default_na=False)
    row("L1 Haddersley North and South episodes close on 30 September 2026 at the merger",
        ((E_.team_code.isin(["BW-CM14", "BW-CM15"])) & (E_.end_reason == "Team merger")
         & (E_.episode_end == "2026-09-30")).sum() >= 20, "")
    allp_st = C.load(target)
    stat = C.register(target)
    cnt = allp_st[allp_st.answered.notna()].groupby("patient").day.apply(list).to_dict()
    bad = 0
    for r in stat.itertuples(index=False):
        n = sum(1 for d in cnt.get(r[1], []) if r[3] <= d <= r[4])
        bad += (r[6] == "Completed") and n < K.COMPLETE
    row("L1 the register marks some fortnights Completed that fall short of half the prompts answered", bad >= 10,
        "%d fortnights" % bad)
    # ------------------------------------------------------------------------------------------- the asks
    people = S.build()
    truth_a = {c: [0, 0] for c, _ in K.TEAMS}
    four = {"old114", "old114_rehired", "leaver_old114", "hub_trained", "new301", "split_new301", "ext", "starter_ext",
            "late_starter_ext"}
    for e, prev, an, org, pos, grp, wte, s, en_, lv in S.assignments(people):
        p = [q for q in people if q.emp == e][0]
        code = [c for c, n in S.ORG.items() if n == org][0]
        if code not in truth_a or p.kind not in four or grp == "Administrative and Clerical" or wte < 0.4:
            continue
        if s <= K.GROUP_START and (en_ is None or en_ >= K.GROUP_START) and (lv is None or lv > K.GROUP_LAST):
            truth_a[code][0] += 1
            truth_a[code][1] += round(wte * 100)
    gold_a = A.ask_a(target)
    row("ASK A fair: the golden's reading of the pack equals the world's own count and whole-time equivalent in every "
        "team", all(gold_a[c][0] == truth_a[c][0] and abs(gold_a[c][1] - truth_a[c][1] / 100.0) < 1e-9
                    for c, _ in K.TEAMS), " ".join("%d/%.2f" % gold_a[c] for c, _ in K.TEAMS))
    acs = A.ask_a(target)
    row("SF15 Ask A, the DBT programme standard's 4.2 is filed; Additional Clinical Services hold no trained clinician",
        "completed DBT skills group facilitation training of four days or more" in dbt and acs == gold_a, "")
    two_teams = {}
    for e, prev, an, org, pos, grp, wte, s, en_, lv in S.assignments(people):
        if org.endswith(" CMHT") and wte >= 0.4 and (en_ is None or en_ >= K.GROUP_START) and s <= K.GROUP_START:
            two_teams.setdefault(e, set()).add(org)
    row("SF16 Ask A, nobody holds a 0.4 WTE assignment in two teams on 1 April 2027, so a clinician counts once",
        all(len(v) == 1 for v in two_teams.values()), "")
    hub_pts, refs = H.build({p.number for p in patients + extra})
    cen_t = H.census(refs, True)
    gold_b = A.ask_b(target)
    row("ASK B fair: the golden's reading of the pack equals the service's own waiting list and waits in every team",
        all(gold_b[c][0] == len(cen_t[c]) and abs(gold_b[c][1] - np.mean(cen_t[c])) < 1e-9 for c, _ in K.TEAMS), "")
    edge = min(abs((gold_b[c][1] * 10) % 1 - 0.5) for c, _ in K.TEAMS)
    row("ASK B no team's mean sits within 0.12 of a step of a rounding edge", edge >= 0.12, "%.2f" % edge)
    row("SF17 Ask B, the waiting list is filed (DBT standard 3.1)", "is on the waiting list from the day they are "
        "added until the day they are removed" in dbt, "")
    row("SF18 Ask B, a wait counts the days since the day received, none on that day (DBT standard 3.2)",
        "so a referral received that day has waited none" in dbt, "")
    for rule, label in (("referring", "SF19 Ask B, the team holding the patient's care on 31 December (the prompt); "
                                      "the referring team instead moves"),
                        ("recorded", "SF20 Ask B, a removal off the list on its removed date (3.1); counted only once "
                                     "recorded instead moves")):
        alt = A.ask_b(target, rule=rule)
        moved = [c for c, _ in K.TEAMS if K.round_half_up(alt[c][1], 1) != K.round_half_up(gold_b[c][1], 1)]
        row("%s %d teams" % (label, len(moved)), len(moved) >= 2, names(moved))
    gold_a2, gold_b2, out = CR.run(target)
    for ask, rule, desc, got, hits in out:
        of = 22 if ask == "A" else 11
        if rule in ("catalogue", "module"):
            row("ASK %s the cracker (%s) keeps none of the %d figures" % (ask, desc, of), not hits, "%d kept" % len(hits))
        else:
            row("ASK %s route %s (%s) keeps %d of %d" % (ask, rule, desc, len(hits), of), len(hits) <= 0.75 * of, "")
    M = pd.read_csv(os.path.join(target, K.F_MODULE), dtype=str, keep_default_na=False)
    win = M[(M.date_received >= "2026-06-22") & (M.date_received <= "2026-07-10")]
    row("ASK B device: the module's receipts in its first three weeks run several times its usual rate, with no single "
        "day holding more than a dozen", len(win) / 15 > 3 * len(M[M.date_received > "2026-07-10"]) / 120
        and win.date_received.value_counts().max() <= 12, "%d in the window, top day %d"
        % (len(win), win.date_received.value_counts().max()))
    row("ASK B every patient has at most one module referral", M.patient_number.value_counts().max() == 1, "")
    same = M[(M.date_received == M.triage_date) & (M.triage_date == M.dbt_list_added)]
    row("ASK B device: the referrals keyed in were stamped received, triaged and listed on one day; no referral the "
        "module received was triaged the day it arrived", len(same) >= 30 and all(
            M.loc[M.date_received == M.triage_date, "date_received"].between("2026-06-22", "2026-07-10")),
        "%d stamped" % len(same))
    LT = pd.read_csv(os.path.join(target, K.F_LETTERS), dtype=str, keep_default_na=False)
    ack = LT[LT.letter_type == "Referral acknowledgement"]
    twice = int((ack.nhs_number.value_counts() >= 2).sum())
    row("ASK B hazard: patients the service acknowledged twice (an earlier referral)", twice >= 20, "%d" % twice)
    row("ASK B fair: every referral the service received has its acknowledgement letter on that day",
        len(ack) == len(refs) and not ack.duplicated(["nhs_number", "letter_date"]).any(), "%d letters" % len(ack))
    cat = openpyxl.load_workbook(os.path.join(target, K.F_CATALOGUE), read_only=True)
    crow = {r[0]: r for r in list(cat.active.iter_rows(values_only=True))[1:]}
    lr = pd.read_csv(os.path.join(target, K.F_LEARN), dtype=str)
    old114 = lr[(lr.course_code == "PTD-114") & (lr.completed_on < "2025-04-01")]
    row("ASK A device: PTD-114 completions before the catalogue's first-offered date, the four-day course the "
        "annual report lists by title", crow["PTD-114"][1] == "DBT skills refresher" and len(old114) >= 25
        and "DBT skills group facilitation" in " ".join(" ".join(r) for r in D.ld_course_table(people)), "%d" % len(old114))
    yrs = D.ld_course_table(people)
    fac = [r for r in yrs if r[0] == "DBT skills group facilitation"][0]
    by_year = [int(fac[k].split()[0]) for k in (2, 3, 4)]
    rec_year = [int(((lr.course_code == "PTD-114") & (lr.completed_on >= "%d-04-01" % y)
                     & (lr.completed_on <= "%d-03-31" % (y + 1))).sum()) for y in (2022, 2023, 2024)]
    row("ASK A fair: the report's yearly facilitation completions equal the records' PTD-114 completions",
        by_year == rec_year, "%s" % by_year)
    # ------------------------------------------------------------------------------------------- separation
    src = open(os.path.join(HERE, "calc.py"), encoding="utf-8").read()
    row("SEP the call reads none of the asks' files", not re.search(r"F_ESR|F_LEARN|F_CATALOGUE|F_LDREPORT|F_DBTSTD|"
                                                                     r"F_MODULE|F_LETTERS|F_INDEX", src), "")
    hubn = {p.number for p in hub_pts}
    row("SEP no patient on the service's referrals is in the mood app's population", not (hubn & set(en.patient_number)),
        "")
    # ------------------------------------------------------------------------------------------- names, dashes, gates
    places = [x.strip().lower() for x in open(os.path.join(HERE, "h21_reference_places.txt")) if x.strip()]
    places += EXTRA_PLACES
    invented = sorted({n for _c, n in K.TEAMS} | {"Wynmoor", "Fordwyke", "Wraybeck", "Brindholm", "Wendholt",
                                                    "Sallowdene"})
    near = ["%s (%s)" % (nm, p) for nm in invented for p in places
            if _ed(nm.lower(), p) <= 2 or (len(p) >= 5 and (p in nm.lower() or nm.lower() in p))]
    row("H21 every invented place and organisation name (%d) is three or more edits from every reference place"
        % len(invented), not near, ", ".join(near[:8]))
    text = " ".join(D.text_of_sections(s) for s in (D.STANDARD, D.DBT_STANDARD, D.PILOT, D.PAPER))
    row("no em or en dash in the documents", "\u2014" not in text and "\u2013" not in text, "")
    files = sorted(os.listdir(target))
    row("GATE files", len(files) >= 10, str(len(files)))
    row("GATE formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3, str(sorted({f.rsplit('.', 1)[1] for f in files})))
    row("GATE a file of 25,000 rows or more", max(len(v3), len(v4)) >= 25000, "%d" % len(v4))
    row("GATE no file or sheet describes the data (readme, dictionary, notes, manifest)",
        not any(re.search(r"readme|dictionar|notes|manifest|schema|codebook", f.lower()) for f in files) and not any(
            re.search(r"readme|dictionar|notes|manifest|schema", ws.lower())
            for f in files if f.endswith(".xlsx")
            for ws in openpyxl.load_workbook(os.path.join(target, f), read_only=True).sheetnames), "")
    row("H16 nothing in an export after its pull", v4.answered_at_utc.replace("", np.nan).dropna().max() < "2026-12-28"
        and M.removal_recorded_on.replace("", np.nan).dropna().max() <= K.PULL_HUB.isoformat()
        and E_.episode_start.max() <= K.PULL_EPR.isoformat(), "")
    for f in files:
        if f.endswith(".pdf"):
            b = open(os.path.join(target, f), "rb").read()
            row("H1 %s carries no generator signature" % f, b"ReportLab" not in b and b"reportlab" not in b, "")
            import warnings
            from pypdf import PdfReader
            with warnings.catch_warnings(record=True) as warned:
                warnings.simplefilter("always")
                strict = " ".join(pg.extract_text() for pg in PdfReader(os.path.join(target, f), strict=True).pages)
            lenient = " ".join(pg.extract_text() for pg in PdfReader(os.path.join(target, f), strict=False).pages)
            row("H25 %s reads the same under a strict and a lenient reader, with no parser warning" % f,
                re.sub(r"\s+", " ", strict) == re.sub(r"\s+", " ", lenient) and not warned and len(strict) > 1500, "")
        if f.endswith((".docx", ".xlsx")):
            z = zipfile.ZipFile(os.path.join(target, f))
            app = z.read("docProps/app.xml").decode()
            row("H1 %s is stamped by Microsoft Office" % f, "Microsoft" in app and "openpyxl" not in app
                and "python-docx" not in z.read("docProps/core.xml").decode(), "")
    counts = list(n_pack.values())
    row("REALISM no assessed-patient count shared by three or more teams", max(counts.count(x) for x in counts) <= 2, "")
    meta = os.path.join(os.path.dirname(HERE), "metadata.json")
    if os.path.exists(meta):
        Mj = json.load(open(meta))
        dis = Mj.get("distractor_files", [])
        row("GATE two or more distractors named in metadata.json, each shipped and none in a graded computation",
            len(dis) >= 2 and all(f in files for f in dis) and not any(
                re.search(r"F_PHQ|F_PILOT", open(os.path.join(HERE, m), encoding="utf-8").read())
                for m in ("calc.py", "asks.py")), ", ".join(dis))
        row("GATE metadata.json lists every shipped file", sorted(f["path"] for f in Mj.get("files", [])) == files, "")
    bad_rows = [r for r in ROWS if not r[1]]
    for label, ok, detail in ROWS:
        print("%s  %s%s" % ("PASS" if ok else "FAIL", label, ("  [%s]" % detail) if detail else ""))
    print("checks: %d run, %d failed" % (len(ROWS), len(bad_rows)))
    return 1 if bad_rows else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else K.TARGET))
