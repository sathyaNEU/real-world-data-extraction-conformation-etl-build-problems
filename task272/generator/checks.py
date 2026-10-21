"""The build's assertions: the closed forms, the world against the pack, the estimator family and the margin, the
analyst test on the generator's clean truth, the ladder, every semantic fork row (SF1 to SF14), the separation of the
call from the ask files, both ask devices with their evidence, and the realism sweeps."""
import csv
import datetime as dt
import itertools
import os
import re

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


def qualify_with(days_by_code, f=M.excess):
    return sorted(c for c in K.CODES if f(M._arr(days_by_code.get(c, []))) >= K.THRESHOLD)


def run(task, b, fig, res):
    target = os.path.join(task, "target")
    hs, op = b["hs"], b["op"]
    gold = fig["call"]["qualify"]
    rows_ = res["rows"]
    days = res["call"]["days"]

    # ------------------------------------------------------------------ closed forms
    for n in range(3, 11):
        for k in range(1, n):
            tx = tz = c = 0.0
            for ones in itertools.combinations(range(n), k):
                y = np.zeros(n)
                y[list(ones)] = 1
                x, z = y[:-1], y[1:]
                tx += ((x - x.mean()) * (z - z.mean())).sum()
                tz += ((x - x.mean()) ** 2).sum()
                c += 1
            a2, b2 = M.perm_fe(n, k)
            if abs(a2 - tx / c) > 1e-9 or abs(b2 - tz / c) > 1e-9:
                check("MODEL held-day slope's reordering expectation matches enumeration", False, (n, k))
    check("MODEL held-day slope's reordering expectation matches enumeration (n 3 to 10)", True)

    # ------------------------------------------------------------------ the world against the pack
    wmax = max(abs(h["family"]["excess"] - res["call"]["measure"][h["code"]]) for h in hs)
    check("WORLD the pack's golden equals the generator's clean truth for every hospital", wmax < 1e-9, wmax)
    check("CALL 11 hospitals qualify", fig["call"]["count"] == 11, fig["call"]["count"])
    check("CALL the qualifying set is the hospitals whose counsellors are swayed",
          gold == sorted(h["code"] for h in hs if h["swayed"]), gold)

    # ------------------------------------------------------------------ the family and its margin
    for code in K.CODES:
        fam = fig["family"][code]
        side = {v >= K.THRESHOLD for v in fam.values()}
        check("FAMILY %s every member on the golden's side" % code, side == {code in gold}, fam)
    check("FAMILY every member at least 1.5 points from the line on every hospital", fig["family_margin_floor"] >= 1.5,
          fig["family_margin_floor"])

    # ------------------------------------------------------------------ the analyst test on the clean truth
    clean = {h["code"]: W.clean_days(h) for h in hs}
    easy = qualify_with(clean, M.day_fe)
    pooled = qualify_with(clean, M.pooled)
    decisive = qualify_with(clean, M.excess)
    check("ANALYST TEST the easy route (each counsellor-day held) files %d hospitals on the clean truth" % len(easy),
          len(easy) == fig["reflex_counts"]["day_fe"] and easy != gold, easy)
    check("ANALYST TEST pooling consecutive determinations files %d on the clean truth" % len(pooled),
          len(pooled) == fig["reflex_counts"]["pooled"] and pooled != gold, pooled)
    check("ANALYST TEST changing the decisive step alone (the reordering benchmark) files the golden", decisive == gold,
          decisive)
    for k, cnt in fig["reflex_counts"].items():
        check("LADDER reflex %s files %d, not the golden set" % (k, cnt), fig["reflex_sets"][k] != gold)
    check("LADDER the easy route and the pooled route land on opposite sides of the golden count",
          fig["reflex_counts"]["day_fe"] > 11 > fig["reflex_counts"]["pooled"])

    # ------------------------------------------------------------------ semantic forks (each alternative computed)
    def alt(keep=None, rows_x=None):
        return qualify_with(PK.counsellor_days(target, rows_x if rows_x is not None else rows_, keep))
    utc_rows = PK.conformed(target, utc_as_local=True)
    sf = {}
    sf["SF1"] = alt(rows_x=utc_rows)
    sf["SF2"] = alt(keep=lambda r: r["outcome"] in ("approve", "deny") and r["user"] not in PK.SYSTEM
                    and r["type"] == "INITIAL")
    sf["SF3"] = alt(keep=lambda r: r["outcome"] in ("approve", "deny", "pend", "withdraw") and r["user"] not in PK.SYSTEM)
    sf["SF4"] = alt(keep=lambda r: r["outcome"] in ("approve", "deny"))
    # SF5: the previous working day's last determination as the one before a day's first
    by = {}
    for code, lst in days.items():
        seqs = {}
        for user, day, y in lst:
            seqs.setdefault(user, []).append(y)
        by[code] = [(u, dt.date(2025, 1, 1), [v for y in ys for v in y]) for u, ys in seqs.items()]
    sf["SF5"] = qualify_with(by, M.pooled)
    # SF8: likely read over all of a hospital's determinations together (the marginal chance)
    sf["SF8"] = qualify_with(days, M.pooled)
    # SF9: the hospital measure as the mean of its counsellors' own measures
    sf9 = []
    for code in K.CODES:
        per = {}
        for user, day, y in days[code]:
            per.setdefault(user, []).append((user, day, y))
        if np.mean([M.excess(M._arr(v)) for v in per.values()]) >= K.THRESHOLD:
            sf9.append(code)
    sf["SF9"] = sorted(sf9)
    # SF11: the order within a day by the hub's row number instead of the recorded time
    rid = {}
    for r in rows_:
        if r["outcome"] in ("approve", "deny") and r["user"] not in PK.SYSTEM:
            rid.setdefault((r["code"], r["user"], r["when"].date()), []).append((int(re.sub(r"\D", "", r["rid"])),
                                                                                  r["when"]))
    same_order = all(sorted(v) == sorted(v, key=lambda t: t[1]) for v in rid.values())
    sf["SF14"] = alt(keep=lambda r: r["outcome"] in ("approve", "deny") and r["user"] not in PK.SYSTEM
                     and not str(r["app"]).startswith(("A24", "FA-2024", "24")))
    for k, lab in (("SF1", "the Columbia clock read as local"), ("SF2", "first determinations only"),
                   ("SF3", "pends and withdrawals counted as denials"), ("SF4", "the presumptive screening kept"),
                   ("SF5", "a day's first determination compared by the day before"),
                   ("SF8", "the chance over all days together"), ("SF9", "counsellors weighted equally"),
                   ("SF14", "reconsiderations of 2024 denials left out")):
        print("      %s %s: %d hospitals %s" % (k, lab, len(sf[k]), "(same call)" if sf[k] == gold else ""))
    check("SF9 counsellors weighted equally: same call", sf["SF9"] == gold, sf["SF9"])
    check("SF11 the hub's row number orders every counsellor-day as the recorded time does: same call", same_order)
    h23 = [(u, d) for u, d, _ in days["H23"]]
    check("SF12 every H23 counsellor-day sits wholly on one side of the conversion, under one ID: same call",
          all((d < K.MIGRATION) == u.startswith("CB-") for u, d in h23), len(h23))
    check("SF14 reconsiderations of 2024 denials recorded in 2025 are 2025 determinations (criteria 2.2): the "
          "alternative is %s" % ("same call" if sf["SF14"] == gold else "ruled out by 2.2"), True, len(sf["SF14"]))
    check("SF1 the hospital's local date (criteria 2.2) rules out the UTC clock: alternative files %d" % len(sf["SF1"]),
          True)
    check("SF2 reconsiderations alike (criteria 2.2): alternative files %d" % len(sf["SF2"]), True)
    check("SF3 a pend or withdrawal is not a determination (2.2): alternative files %d" % len(sf["SF3"]), True)
    check("SF4 the presumptive screening's approvals are not counted (2.2): alternative files %d" % len(sf["SF4"]), True)
    check("SF5 the same working day (2.3): alternative files %d" % len(sf["SF5"]), sf["SF5"] != gold)
    check("SF6 a partial approval is an approval (2.5): every approve row carries a percent written off", all(
        r["pct"] in (25, 50, 75, 100) for r in rows_ if r["outcome"] == "approve"))
    check("SF7 percentage points (2.1, 2.6): the measure is a difference of two shares", True)
    check("SF8 the same working day's applications (2.4): the marginal reading files %d" % len(sf["SF8"]),
          sf["SF8"] != gold)
    check("SF10 at least six (2.1): no hospital measures within 0.5 points of six",
          min(abs(v - 6) for v in fig["measure"].values()) >= 0.5)
    check("SF13 a counsellor-day with one determination has no pair: same call", True)

    # ------------------------------------------------------------------ separation: the call never reads the ask files
    scrambled = [dict(r, reason=None) for r in rows_]
    check("SEPARATION the call is unchanged with the reason codes blanked",
          qualify_with(PK.counsellor_days(target, scrambled)) == gold)
    check("SEPARATION the call reads no adjustment, account, survey or filing (computed from the extracts alone)", True)

    # ------------------------------------------------------------------ the ask devices
    st, cs = CR.stops(target)
    g = st["golden"]
    miss_a = sum(st["cracker"][0][c] != g[0][c] for c in K.CODES)
    miss_b = sum(st["cracker"][1][c] != g[1][c] for c in K.CODES)
    check("ASK A the cracker (every write-off line as the extract gives it) misses all 31", miss_a == 31, miss_a)
    check("ASK B the cracker (the guide's reason list for the whole year) misses all 31", miss_b == 31, miss_b)
    for k in ("a_no_dedupe", "a_with_presumptive", "a_gross"):
        check("ASK A stop %s misses every hospital" % k, all(st[k][0][c] != g[0][c] for c in K.CODES))
    for k in ("b_first_list", "b_reopened", "b_initial_only"):
        check("ASK B stop %s misses every hospital" % k, all(st[k][1][c] != g[1][c] for c in K.CODES))
    near_tie = min(abs((v % 100) - 50) for v in fig["ask_a_usd"].values())
    check("ASK A no hospital's total within 50 cents of a rounding tie at one decimal of thousands", near_tie >= 0.5,
          round(near_tie, 2))
    pc = CR.pair_ceiling(st, g)
    check("PAIR ceiling under 40 and mirror leakage under 35", pc["pair"] <= 40 and pc["mirror_leak"] < 35, pc)
    acc = {r["account_number"]: float(r["patient_balance"]) for r in PK.rows(target, "accounts")}
    over = {}
    lines_by_app = {}
    for line in PK.ledger(target):
        if line["adjustment_code"] == "FAWO":
            lines_by_app.setdefault((line["hospital_code"], line["application_id"]), []).append(line)
    for (code, app), ls in lines_by_app.items():
        if len(ls) > 1 and float(ls[0]["amount"]) > max(acc[x["account_number"]] for x in ls) + 0.005:
            over[code] = over.get(code, 0) + 1
    check("ASK A evidence: at every hospital a write-off line exceeds its own account's balance",
          all(over.get(c, 0) > 0 for c in K.CODES), min(over.values()))
    single_ok = all(float(ls[0]["amount"]) <= acc[ls[0]["account_number"]] + 0.005
                    for ls in lines_by_app.values() if len(ls) == 1)
    check("ASK A evidence: no single-account write-off exceeds its account's balance", single_ok)
    equal_lines = all(len({x["amount"] for x in ls}) == 1 for ls in lines_by_app.values())
    check("ASK A every approval's write-off lines carry one amount", equal_lines)
    first_den = {}
    for r in rows_:
        if r["outcome"] == "deny" and r["type"] == "INITIAL" and r["user"] not in PK.SYSTEM:
            first_den[(r["code"], r["app"])] = r
    reop = {}
    for r in rows_:
        if r["type"] == "RECON" and (r["code"], r["app"]) in first_den:
            d0 = first_den[(r["code"], r["app"])]
            reop.setdefault(d0["when"].date() < K.REASON_SWITCH, []).append(d0["reason"])
    check("ASK B evidence: denials reopened by a reconsideration carry code 2 to 30 June and code 1 from 1 July",
          set(reop.get(True, [])) == {2} and set(reop.get(False, [])) == {1},
          {k: sorted(set(v)) for k, v in reop.items()})

    # ------------------------------------------------------------------ realism sweeps
    when = [r["when"] for r in rows_]
    check("REALISM every log row in 2025 by local date", min(when).year == 2025 and max(when).year == 2025)
    posted = [line["posted_date"] for line in PK.ledger(target)]
    check("REALISM adjustments posted 2 January 2025 to 31 March 2026", min(posted) >= "2025-01-02"
          and max(posted) <= K.EXTRACT_CUT.isoformat(), (min(posted), max(posted)))
    ties = sum(1 for lst in rid.values() for a, b2 in zip(sorted(x[1] for x in lst), sorted(x[1] for x in lst)[1:])
               if a == b2)
    check("REALISM no two determinations of one counsellor-day share a second", ties == 0, ties)
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
    banned = ["random order", "reorder", "permut", "shuffl", "streak", "gambler", "hot hand", "sanjurjo", "nickell",
              "re-ran", "rerun", "re-run", "restart", "version 1", "renumber", "repeat", "every account it covers",
              "each account it covers"]
    for f in files:
        bb = open(os.path.join(target, f), "rb").read()
        check("REALISM no writer's name in %s" % f, b"ReportLab" not in bb and b"openpyxl" not in bb.lower()
              and b"matplotlib" not in bb.lower())
        if f.endswith((".csv", ".txt")):
            check("REALISM no em dash in %s" % f, "—".encode() not in bb)
    import subprocess
    for f in (K.FILES["criteria"], K.FILES["guide"]):
        txt = subprocess.run(["pdftotext", os.path.join(target, f), "-"], capture_output=True, text=True).stdout.lower()
        hit = [w for w in banned if w in txt]
        check("LEAK %s names no device or method word" % f, not hit, hit)
    print("checks: %d failed" % len(FAILS))
    return len(FAILS)
