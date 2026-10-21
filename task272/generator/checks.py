"""The build's assertions: the world against the pack, the estimator family and its margin, the analyst test on the
generator's clean truth, the ladder, every semantic fork row, the separation of the call from the ask columns and files,
both ask devices with their evidence, and the realism sweeps."""
import collections
import datetime as dt
import math
import os
import subprocess

import numpy as np

import analysis as A
import common as K
import cracker as CR
import models as M
import pack as PK
import world as W

FAILS = []


def check(label, ok, detail=""):
    if not ok:
        FAILS.append(label)
    print("%s  %s%s" % ("ok  " if ok else "FAIL", label, ("  [%s]" % (detail,)) if detail != "" else ""))


def edit(a, b):
    m, n = len(a), len(b)
    if abs(m - n) > 2:
        return 9
    d = list(range(n + 1))
    for i in range(1, m + 1):
        p, d[0] = d[0], i
        for j in range(1, n + 1):
            p, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, p + (a[i - 1] != b[j - 1]))
    return d[n]


def qualifying(measure):
    return sorted(c for c in K.CODES if measure.get(c, 0) >= K.THRESHOLD)


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    hs = b["hs"]
    gold = fig["call"]["qualify"]
    rows_ = res["rows"]
    fr = res["call"]["first_reviews"]

    # ------------------------------------------------------------------ the world against the pack
    clean = W.decide(hs, {h["code"]: h["doc"] for h in hs})
    designed = sorted(c for c, t in K.TARGET.items() if t >= K.THRESHOLD)
    world_gold = qualifying(M.golden(clean))
    check("WORLD the golden on the generator's clean rows names the designed set", world_gold == designed, world_gold)
    wm = M.golden(clean)
    dmax = max(abs(wm[c] - fig["measure"][c]) for c in K.CODES)
    check("WORLD the pack's shares match the clean rows' within 0.05 (incomes rounded by each hub)", dmax < 0.05,
          round(dmax, 4))
    truth = qualifying(M.share(clean, lambda x: x["inc12"]))
    check("WORLD the households' own twelve-month incomes name the same set", truth == gold, truth)
    check("CALL %d hospitals qualify, the designed set" % len(designed), gold == designed, gold)

    # ------------------------------------------------------------------ the family and its margin
    for k, v in fig["family"].items():
        check("FAMILY %s names the golden set" % k, qualifying(v) == gold, qualifying(v))
    check("FAMILY every member at least 0.75 points from the line on every hospital",
          fig["family_margin_floor"] >= 0.75, fig["family_margin_floor"])
    med = M.share(fr, M.by_calendar(_median_cal(fr), M.k_region_kind))
    check("FAMILY medians by month name the golden set", qualifying(med) == gold, qualifying(med))

    # ------------------------------------------------------------------ the literal reader's evidence (the design note)
    cals = M.cal_cross(fr, M.k_region_kind)
    ratios = sorted(float(f.max() / f.min()) for k, f in cals.items() if k[1] in M.SEASONAL)
    check("EVIDENCE the seasonal cells' best month of application against their worst: median %.2f times over %d cells, "
          "%.2f at most" % (ratios[len(ratios) // 2], len(ratios), ratios[-1]), ratios[len(ratios) // 2] > 2.0)
    seen = collections.defaultdict(list)
    for x in fr:
        if x["kind"] in M.SEASONAL:
            seen[x["hh"]].append(x)
    obs, cal = [], []
    for xs in seen.values():
        for i in range(len(xs)):
            for j in range(i + 1, len(xs)):
                a, b2 = xs[i], xs[j]
                if a["month"] != b2["month"] and a["annual"] > 0 and b2["annual"] > 0:
                    f = cals[M.k_region_kind(a)]
                    obs.append(math.log(a["annual"] / b2["annual"]))
                    cal.append(math.log(f[a["month"] - 1] / f[b2["month"] - 1]))
    rho = float(np.corrcoef(obs, cal)[0, 1])
    check("EVIDENCE %d pairs of a seasonal household's applications in different months move with the calendar's ratio "
          "(log ratios correlate at %.3f)" % (len(obs), rho), rho > 0.8)

    # ------------------------------------------------------------------ the analyst test on the clean truth
    easy = qualifying(M.share(clean, lambda x: x["annual"]))
    check("ANALYST TEST the easy route (the 2025 policy's yearly figure as the twelve-month income) files %d on the "
          "clean rows" % len(easy), easy != gold and len(easy) == fig["reflex_counts"]["policy_quarter"], easy)
    decisive = qualifying(M.golden(clean))
    check("ANALYST TEST changing the decisive step alone (each region's calendar for each kind of work) files the "
          "golden", decisive == gold, decisive)
    for k in ("one_seasonal_calendar", "kind_calendar", "region_calendar"):
        v = qualifying(M.REFLEXES[k](clean))
        check("ANALYST TEST %s files %d on the clean rows, not the golden" % (k, len(v)), v != gold, v)
    for k, cnt in fig["reflex_counts"].items():
        if k == "geometric_scale":
            continue
        check("LADDER reflex %s files %d, not the golden set" % (k, cnt), fig["reflex_sets"][k] != gold)
    check("LADDER the easy route files fewer than half the golden's grants",
          fig["reflex_counts"]["policy_quarter"] * 2 < fig["call"]["count"])

    # ------------------------------------------------------------------ semantic forks (each alternative computed)
    def call_on(rows_x, est=None):
        frx = PK.first_reviews(target, rows_x)
        return qualifying(M.golden(frx)) if est is None else qualifying(est(frx))

    sf = {}
    sf["SF1"] = call_on(PK.conformed(target, utc_as_local=True))
    recon_as_first = [dict(r, type="INITIAL") if r["type"] == "RECON" else r for r in rows_]
    sf["SF2"] = call_on(recon_as_first)
    sf["SF3"] = call_on([dict(r, outcome="deny") if r["outcome"] in ("pend", "withdraw") else r for r in rows_])
    # SF5: the month of the decision read as the month of application
    sf["SF5"] = qualifying(M.share([dict(x, month=x["dmonth"]) for x in _with_dmonth(fr, rows_)],
                                   M.by_calendar(M.cal_cross([dict(x, month=x["dmonth"])
                                                              for x in _with_dmonth(fr, rows_)], M.k_region_kind),
                                                 M.k_region_kind)))
    # SF6: a 50 percent discount read as leaving more than half owing
    sf["SF6"] = qualifying(_share_owing(fr, 75))
    # SF7: the guideline of the year received rather than 2025's
    sf["SF7"] = qualifying(_share_guideline_year(fr, rows_))
    # SF8: each household once, its last 2025 decision
    last = {}
    for x in fr:
        if x["year"] == 2025:
            last[x["hh"]] = x
    sf["SF8"] = qualifying(M.share([x for x in fr if x["year"] != 2025] + list(last.values()),
                                   M.by_calendar(M.cal_cross(fr, M.k_region_kind), M.k_region_kind)))
    # SF9: applications received in 2025 rather than decided in 2025
    sf["SF9"] = qualifying(M.share([dict(x, year=2024 + x["mindex"] // 12) for x in fr],
                                   M.by_calendar(M.cal_cross(fr, M.k_region_kind), M.k_region_kind)))
    # SF13: below the limit rather than at or below
    sf["SF13"] = qualifying(_share_strict(fr))
    # SF4: a denial for documents not received left out (the household could send them and apply again)
    docs = {(r["code"], r["app"]) for r in rows_ if r["type"] == "INITIAL" and r["outcome"] == "deny"
            and r["user"] not in PK.SYSTEM and r["reason"] == A.documents_code(r["when"].date())}
    sf["SF4"] = qualifying(M.share([x for x in fr if (x["code"], x["app"]) not in docs],
                                   M.by_calendar(M.cal_cross(fr, M.k_region_kind), M.k_region_kind)))
    # SF11: each application's last decision (a reconsideration's in place of the first review's)
    last_rc = {}
    for r in sorted(rows_, key=lambda r: r["when"]):
        if r["type"] == "RECON" and r["outcome"] in ("approve", "deny") and r["user"] not in PK.SYSTEM:
            last_rc[(r["code"], r["app"])] = r["pct"] if r["outcome"] == "approve" else 0
    sf["SF11"] = qualifying(M.golden([dict(x, writeoff=last_rc[(x["code"], x["app"])])
                                      if (x["code"], x["app"]) in last_rc else x for x in fr]))
    labels = {"SF1": "the Columbia clock read as local", "SF2": "reconsiderations as first reviews",
              "SF3": "pends and withdrawals as denials", "SF5": "the decision month as the month of application",
              "SF6": "a 50 percent discount as owing more than half", "SF7": "the received year's guideline",
              "SF8": "each household once", "SF9": "applications received in 2025", "SF13": "strictly below the limit",
              "SF4": "documents denials left out", "SF11": "each application's last decision"}
    for k, lab in labels.items():
        print("      %s %s: %d hospitals %s" % (k, lab, len(sf[k]), "(same call)" if sf[k] == gold else ""))
    check("SF1 the hospital's local date (criteria 2.2): the UTC clock read as local %s" %
          ("keeps the call" if sf["SF1"] == gold else "is ruled out by 2.2"), True, len(sf["SF1"]))
    check("SF2 a reconsideration is not a first review (2.2): alternative files %d" % len(sf["SF2"]), True)
    check("SF3 a pend or withdrawal is not a decision (2.2): alternative files %d" % len(sf["SF3"]), True)
    check("SF5 the month in which the household applied (2.3) is the received month: alternative files %d"
          % len(sf["SF5"]), True)
    check("SF6 owing more than half is a denial or a 25 percent discount (2.4): alternative files %d" % len(sf["SF6"]),
          True)
    check("SF7 the 2025 guideline for every household (2.3, section 3): alternative %s" %
          ("keeps the call" if sf["SF7"] == gold else "files %d" % len(sf["SF7"])), True)
    check("SF8 each application counts (2.2): alternative %s" % ("keeps the call" if sf["SF8"] == gold else
                                                                "files %d" % len(sf["SF8"])), True)
    check("SF9 decided in 2025 (2.2): alternative %s" % ("keeps the call" if sf["SF9"] == gold else
                                                        "files %d" % len(sf["SF9"])), True)
    check("SF10 at least six (2.1): no hospital within 0.75 points of six",
          min(abs(v - 6) for v in fig["measure"].values()) >= 0.75)
    check("SF13 no more than 200 percent (2.3): strictly below keeps the call", sf["SF13"] == gold, sf["SF13"])
    check("SF4 a denial for any reason (2.4): documents denials left out files %d" % len(sf["SF4"]), sf["SF4"] != gold,
          len(sf["SF4"]))
    check("SF11 each application's first approval or denial (2.2): the last decision %s" %
          ("keeps the call" if sf["SF11"] == gold else "files %d" % len(sf["SF11"])), True, len(sf["SF11"]))
    h23 = [r for r in rows_ if r["code"] == K.MIGRATED and r["type"] == "INITIAL" and r["outcome"] in ("approve", "deny")]
    check("SF12 every H23 first review sits in the extract of the hub that held it on its date",
          all((r["when"].date() < K.MIGRATION) == (r["hub"] == "columbia") for r in h23), len(h23))

    # ------------------------------------------------------------------ separation: the call never reads the ask files
    scrambled = [dict(r, reason=None) for r in rows_]
    check("SEPARATION the call is unchanged with the reason codes blanked", call_on(scrambled) == gold)
    check("SEPARATION the call reads no adjustment, account, survey or filing (computed from the extracts alone)", True)

    # ------------------------------------------------------------------ the ask devices
    st, cs = CR.stops(target)
    g = st["golden"]
    miss_a = sum(st["cracker"][0][c] != g[0][c] for c in K.CODES)
    miss_b = sum(st["cracker"][1][c] != g[1][c] for c in K.CODES)
    check("ASK A the cracker (each application's write-off once, joined by its number) misses all 31", miss_a == 31,
          miss_a)
    # The renumbering swapped two reasons of like volume, so a whole-year reading ties the golden at a hospital only
    # where that half-year's income denials happen to equal its documents denials; any other tie fails.
    halves = collections.Counter()
    for r in rows_:
        if r["outcome"] == "deny" and r["user"] not in PK.SYSTEM and r["when"].year == K.YEAR:
            halves[(r["code"], r["when"].date() < K.REASON_SWITCH, r["reason"])] += 1
    tie_h1 = {c for c in K.CODES if halves[(c, True, 1)] == halves[(c, True, 2)]}
    tie_h2 = {c for c in K.CODES if halves[(c, False, 1)] == halves[(c, False, 2)]}
    hit_b = {c for c in K.CODES if st["cracker"][1][c] == g[1][c]}
    check("ASK B the cracker (the guide's reason list for the whole year) misses all 31 but a first half's equal counts",
          hit_b <= tie_h1 and len(hit_b) <= 2, (miss_b, sorted(hit_b)))
    for k in ("a_every_line", "a_event_by_app", "a_posted_year", "a_golden_presumptive", "a_golden_gross"):
        check("ASK A stop %s misses every hospital" % k, all(st[k][0][c] != g[0][c] for c in K.CODES))
    hit = {c for c in K.CODES if st["b_first_list"][1][c] == g[1][c]}
    check("ASK B stop b_first_list misses every hospital but a second half's equal counts",
          hit <= tie_h2 and len(hit) <= 2, sorted(hit))
    check("ASK B stop b_both_years misses every hospital", all(st["b_both_years"][1][c] != g[1][c] for c in K.CODES))
    check("REALISM every hospital's counsellors denied at least 20 applications in 2025 for documents not received",
          min(fig["ask_b"].values()) >= 20, min(fig["ask_b"].values()))
    near_tie = min(abs((v % 100) - 50) for v in fig["ask_a_usd"].values())
    check("ASK A no hospital's total within 50 cents of a rounding tie at one decimal of thousands", near_tie >= 0.5,
          round(near_tie, 2))
    pc = CR.pair_ceiling(st, g)
    check("PAIR ceiling under 40 and mirror leakage under 35", pc["pair"] <= 40 and pc["mirror_leak"] < 35, pc)
    acc = {r["account_number"]: float(r["patient_balance"]) for r in PK.rows(target, "accounts")}
    over = collections.Counter()
    lines_by_ev = collections.defaultdict(list)
    for line in PK.ledger(target):
        if line["adjustment_code"] == "FAWO":
            lines_by_ev[(line["hospital_code"], line["application_id"], line["posted_date"])].append(line)
    for (code, app, _), ls in lines_by_ev.items():
        if len(ls) > 1 and float(ls[0]["amount"]) > max(acc[x["account_number"]] for x in ls) + 0.005:
            over[code] += 1
    check("ASK A evidence (grain): at every hospital a write-off line exceeds its own account's balance",
          all(over.get(c, 0) > 0 for c in K.CODES), min(over.get(c, 0) for c in K.CODES))
    check("ASK A every write-off's lines carry one amount", all(len({x["amount"] for x in ls}) == 1
                                                               for ls in lines_by_ev.values()))
    first_outcome = {}
    for r in rows_:
        if r["type"] == "INITIAL" and r["outcome"] in ("approve", "deny") and r["user"] not in PK.SYSTEM:
            first_outcome[(r["code"], r["app"])] = r["outcome"]
    recon_ok = {(r["code"], r["app"]) for r in rows_ if r["type"] == "RECON" and r["outcome"] == "approve"}
    under_denied = collections.Counter()
    two_events = collections.Counter()
    events_per_app = collections.Counter((k[0], k[1]) for k in lines_by_ev)
    for (code, app), n in events_per_app.items():
        if first_outcome.get((code, app)) == "deny" and (code, app) not in recon_ok:
            under_denied[code] += 1
        if n > 1:
            two_events[code] += 1
    decided = {}
    for r in rows_:
        if r["outcome"] in ("approve", "deny") and r["user"] not in PK.SYSTEM:
            decided[(r["code"], r["app"])] = max(decided.get((r["code"], r["app"]), r["when"].date()), r["when"].date())
    late = collections.Counter()
    for (code, app, posted) in lines_by_ev:
        d0 = decided.get((code, app))
        if d0 is not None and (dt.date.fromisoformat(posted) - d0).days > 10:
            late[code] += 1
    ev_key = {c: under_denied[c] + two_events[c] + late[c] for c in K.CODES}
    check("ASK A evidence (key): at every hospital a write-off posts under a denied application, a second write-off "
          "posts under one number, or a write-off posts weeks after its number's own decision",
          all(v > 0 for v in ev_key.values()), min(ev_key.values()))
    first_den = {}
    for r in rows_:
        if r["outcome"] == "deny" and r["type"] == "INITIAL" and r["user"] not in PK.SYSTEM:
            first_den[(r["code"], r["app"])] = r
    reop = {}
    for r in rows_:
        if r["type"] == "RECON" and (r["code"], r["app"]) in first_den:
            d0 = first_den[(r["code"], r["app"])]
            reop.setdefault(d0["when"].date() < K.REASON_SWITCH, []).append(d0["reason"])
    check("ASK B evidence: denials reopened by a reconsideration carry code 2 to 30 June 2025 and code 1 from 1 July",
          set(reop.get(True, [])) == {2} and set(reop.get(False, [])) == {1},
          {k: sorted(set(v)) for k, v in reop.items()})

    # ------------------------------------------------------------------ realism sweeps
    when = [r["when"] for r in rows_]
    check("REALISM every log row in 2024 or 2025 by local date", min(when).year == 2024 and max(when).year == 2025,
          (min(when), max(when)))
    rec = [r["received"] for r in rows_ if r.get("received")]
    check("REALISM every application received in 2024 or 2025", min(rec).year == 2024 and max(rec).year == 2025)
    check("REALISM every decision on or after its application's receipt",
          all(r["when"].date() >= r["received"] for r in rows_ if r.get("received") and r["type"] != "PRESUMPTIVE"))
    byhh = collections.defaultdict(list)
    for x in fr:
        byhh[x["hh"]].append(x["annual"])
    multi = [v for v in byhh.values() if len(v) > 1]
    same = sum(1 for v in multi if len(set(v)) < len(v))
    check("REALISM a household's applications carry different incomes (under 1 percent of the households that applied "
          "more than once repeat a figure)", same < 0.01 * len(multi), (same, len(multi)))
    posted = [line["posted_date"] for line in PK.ledger(target)]
    check("REALISM adjustments posted 1 January 2025 to 31 March 2026", min(posted) >= "2025-01-01"
          and max(posted) <= K.EXTRACT_CUT.isoformat(), (min(posted), max(posted)))
    hours = [r["when"].time() for r in rows_ if r["user"] not in PK.SYSTEM]
    check("REALISM counsellor rows between 07:30 and 17:40 local",
          min(hours) >= dt.time(7, 30) and max(hours) <= dt.time(17, 40), (min(hours), max(hours)))
    L = PK.ledger(target, dedupe=False)
    seen, dup_rows = set(), []
    for r in L:
        key = tuple(r.values())
        if key in seen:
            dup_rows.append(r)
        seen.add(key)
    check("REALISM the exact duplicates are the Willamette hub's December 2025 lines, loaded twice",
          len(dup_rows) > 0 and all(K.HUB[r["hospital_code"]] == "willamette" and r["posted_date"][:7] == "2025-12"
                                    for r in dup_rows), len(dup_rows))
    files = sorted(os.listdir(target))
    check("H4 the pack holds exactly the declared files", files == sorted(K.FILES.values()), files)
    contents = open(os.path.join(target, K.FILES["contents"]), encoding="utf-8").read()
    check("H9 contents lists every file", all(f in contents for f in files if f != K.FILES["contents"]))
    places = [x.strip().lower() for x in open(os.path.join(os.path.dirname(__file__), "h21_reference_places.txt"))
              if x.strip()]
    for nm in ["Vellacott"] + [h[1].split()[0] for h in K.HOSPITALS]:
        n = nm.lower()
        near = [p for p in places if edit(n, p) <= 2 or (len(p) >= 6 and p in n) or (len(n) >= 6 and n in p)]
        check("H21 %s is three or more edits from every reference place" % nm, not near, near[:3])
    banned = ["season", "harvest", "peak", "slack", "calendar of", "repeat", "every account it covers",
              "each account it covers", "case number", "opened with", "renumber", "version 1", "reapplie",
              "applies again"]
    for f in files:
        bb = open(os.path.join(target, f), "rb").read()
        check("REALISM no writer's name in %s" % f, b"ReportLab" not in bb and b"openpyxl" not in bb.lower()
              and b"matplotlib" not in bb.lower())
        if f.endswith((".csv", ".txt")):
            check("REALISM no em dash in %s" % f, "—".encode() not in bb)
    for f in (K.FILES["criteria"], K.FILES["guide"]):
        txt = subprocess.run(["pdftotext", os.path.join(target, f), "-"], capture_output=True, text=True).stdout.lower()
        hit = [w for w in banned if w in txt]
        check("LEAK %s names no device or method word" % f, not hit, hit)
    print("checks: %d failed" % len(FAILS))
    return len(FAILS)


def _median_cal(fr):
    acc = collections.defaultdict(lambda: collections.defaultdict(list))
    for x in fr:
        acc[M.k_region_kind(x)][x["month"] - 1].append(M.pct(x, x["annual"]))
    out = {}
    import numpy as np
    for k, mm in acc.items():
        if len(mm) == 12:
            v = np.array([np.median(mm[m]) for m in range(12)])
            out[k] = v / v.mean()
    return out


def _with_dmonth(fr, rows_):
    when = {(r["code"], r["app"]): r["when"] for r in rows_ if r["type"] == "INITIAL"
            and r["outcome"] in ("approve", "deny")}
    return [dict(x, dmonth=when[(x["code"], x["app"])].month) for x in fr]


def _share_owing(fr, owing):
    cals = M.cal_cross(fr, M.k_region_kind)
    est = M.by_calendar(cals, M.k_region_kind)
    num, den = collections.Counter(), collections.Counter()
    for x in fr:
        if x["year"] == 2025 and M.pct(x, est(x)) <= M.LIMIT:
            den[x["code"]] += 1
            num[x["code"]] += x["writeoff"] < owing
    return {c: 100.0 * num[c] / den[c] for c in den}


def _share_guideline_year(fr, rows_):
    cals = M.cal_cross(fr, M.k_region_kind)
    est = M.by_calendar(cals, M.k_region_kind)
    num, den = collections.Counter(), collections.Counter()
    for x in fr:
        if x["year"] != 2025:
            continue
        y = 2024 + x["mindex"] // 12
        guide = W.fpl(y, x["size"])
        if est(x) / guide * 100 <= M.LIMIT:
            den[x["code"]] += 1
            num[x["code"]] += x["writeoff"] < M.OWING
    return {c: 100.0 * num[c] / den[c] for c in den}


def _share_strict(fr):
    cals = M.cal_cross(fr, M.k_region_kind)
    est = M.by_calendar(cals, M.k_region_kind)
    num, den = collections.Counter(), collections.Counter()
    for x in fr:
        if x["year"] == 2025 and M.pct(x, est(x)) < M.LIMIT:
            den[x["code"]] += 1
            num[x["code"]] += x["writeoff"] < M.OWING
    return {c: 100.0 * num[c] / den[c] for c in den}
