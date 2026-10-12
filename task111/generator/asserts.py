"""The assertion regime. Every check fails the build loudly."""
import datetime as dt
from collections import Counter, defaultdict
from pathlib import Path

import golden as G
import sample
from world import MOVES

D = dt.date
N = 0
# the main call's files as shipped with its determinism verdict (2026-10-06): the ask layer may not move a byte
FROZEN = {
    "field_appointments_2025-07_2026-09.csv": "9dfc4b7cba3c987fd757f817f19962f6d4742d193b74fde23922ec2e6bd43659",
    "engineer_day_log_2025-07_2026-09.csv": "bd13f95e586fae4b27154a2e5fb6b3bd6e23dd3c86681d4f4ee61b0142f0b3cf",
    "ooh_desk_callouts_2025-07_2026-10.xlsx": "abf2cc5f37c40b4edf333d659ee1ddb556d0f8a50e812e301e82d3521f42be05",
    "field_workforce_register.xlsx": "ce1a71d6d11c0e873b1e54e694cfe82786595697d779e295470c1679993dc9cb",
    "rota_2025-07_2026-09.csv": "4cb68f5c4a7e9efc491071dd03bbcee86d0dd10efc426016b5042d676b7fd00a",
    "missed_appointment_verification_jan-may_2026.csv":
        "6a1ed002c26d252e2fc8d228facbc7af63ae2334b9358f513f69f71f8054cda7",
    "missed_appointment_review_procedure_FS-07.pdf":
        "4ca1c28929b3833ebf8a81c13d55829432f2a1f774c13331c88f01664040228c",
    "field_working_time_policy_HR-FS-03.pdf": "386088b80e30c13997e6e4183d8de08dfd36502796da2ef4a1778ff03dd99949",
    "pathline_4.2_release_note.pdf": "0524b6e99f001d9b1da29ccf9992e2dae5d1ec4c1ae6e729654cd0a6e0ffec49",
    "field_review_2026-07-23_notes.docx": "765aee1e78d5353e838d200213f52180f139948e801902b6935717864008b184",
    "customer_service_standards_2026_extract.pdf":
        "08ae0d99dddfa4bf756c5f3b969fbb045a61ccb38457bb37529fe8cd0d59da0b",
    "postcode_district_patches.csv": "30407753a41f8bf8ca21c4311ae5a84e560d222ddda60205e01e799280f15705",
}
CREDIT_PATHS = {"direct": 0.05, "all_lines": 0.02, "single_hit": 0.02, "first_hit": 0.02, "one_per_acct_day": 0.0,
                "first_line": 0.0, "split": 0.0, "policy": 0.0, "runs_q3": 0.02}
COMPLAINT_PATHS = {"rows_direct": 0.0, "refs_direct": 0.0, "rows_resolved": 0.0, "refs_resolved": 0.025,
                   "drop_reopened": 0.0, "dedup_copies": 0.0, "dedup_acct_visit": 0.0, "closed_only": 0.0,
                   "label_only": 0.0, "received_q3": 0.0, "dedup_hhday": 0.0}


def ok(cond, msg):
    global N
    if not cond:
        raise AssertionError(msg)
    N += 1


def run(W, out, Gd, q3, T: Path):
    global N
    N = 0
    fc = out["family_counts"]
    rank = sorted(fc.items(), key=lambda x: -x[1])
    # ---------------------------------------------------------------- input gates
    files = [p for p in T.iterdir() if p.is_file()]
    ok(len(files) >= 10, "file count")
    ok(len({p.suffix for p in files}) >= 3, "format count")
    ok(len(Gd["apps"]) > 10000, "one dataset over 10,000 rows")
    ok(not any(p.name.startswith(".") for p in files), "no hidden files")
    import hashlib
    for name, digest in FROZEN.items():
        ok(hashlib.sha256((T / name).read_bytes()).hexdigest() == digest, "main-path file unchanged: " + name)
    # ---------------------------------------------------------------- the ladder by name
    # rung 3, the cross-day trace of the closed quarter: Rota & cover leads, the answer is a distant second
    ok(rank[0][0] == "Rota & cover", "rung 3 names Rota & cover for Q3")
    ok(rank[1][0] == "Parts & van stock", "Parts & van stock is second on the Q3 cross-day trace")
    ok(rank[0][1] >= 1.25 * rank[1][1], "rung 3 margin over the answer at least 1.25x")
    # rung 4, the window the decision buys: the causes that carry into January to March
    fw = out["forward"]
    ok(fw["answer"] == "Parts & van stock", "forward answer is Parts & van stock")
    ok(fw["ranking"][0][1] >= 1.25 * fw["ranking"][1][1], "forward answer at least 1.25x the next carrying cause")
    ok(fw["ranking"][1][0] == "Engineer attendance & punctuality", "forward runner-up is punctuality")
    ok(fw["ranking"][1][1] >= 1.15 * fw["ranking"][2][1], "forward runner-up clear of third")
    # the C4 grid of forward methods, each cell mapped to the rule it violates
    g = fw["grid"]
    ok(g["q3_carry_all"] == "Rota & cover", "carrying Q3 forward whole names Rota & cover (ignores the winter panel)")
    ok(g["q3_carry_winter"] == "Parts & van stock", "Q3 less what the winter panel removes names the answer")
    ok(g["seasonal_ratio"] == "Parts & van stock", "last year's per-family seasonal ratio converges on the answer")
    ok(g["last_winter_as_is"] != "Parts & van stock", "last winter as it stood names another cause (ignores July's changes)")
    ok(g["same_day_carry"] == "Engineer attendance & punctuality", "the same-day reading carried forward names punctuality")
    # the winter: no Rota & cover in any month from October to May, and why
    w = fw["winter"]
    ok(all(v == 0 for v in w["rota_cover_by_month"].values()), "no Rota & cover miss in any month October to May")
    ok(len(w["rota_cover_by_month"]) == 8, "eight winter months checked")
    ok(w["latest_list_clear"] <= "20:40", "no day-roster call-out clear after 20:40 from October to May")
    ok(all(v > 0 for v in w["panel_by_month"].values()), "the contractor panel attends in every winter month")
    ok(w["october_2026_panel"] > 0, "the panel is back on the October 2026 nights")
    ok(w["summer_list_late"] > 0, "summer call-out-list clears do run past 21:00")
    sd = out["same_day_q3"]
    sdr = sorted(sd.items(), key=lambda x: -x[1])
    ok(sdr[0][0] == "Engineer attendance & punctuality", "rung 2 names punctuality")
    ok(sdr[0][1] >= 1.5 * sdr[1][1], "rung 2 margin")
    ok(sd.get("Rota & cover", 0) == 0, "rung 2 has no Rota & cover")
    oh = out["one_hop_q3"]
    ohr = sorted(oh.items(), key=lambda x: -x[1])
    ok(ohr[0][0] == "Job duration & standards", "rung 1 names job duration")
    ok(ohr[0][1] >= 2 * ohr[1][1], "rung 1 margin")
    # rung 0: the July step and the travel rise
    mon = defaultdict(lambda: [0, 0])
    for a in Gd["apps"]:
        if G.attended(a):
            k = a["appointment_date"][:7]
            mon[k][1] += 1
            mon[k][0] += G.is_missed(a)
    rate = {k: v[0] / v[1] for k, v in mon.items()}
    ok(rate["2026-07"] > 1.35 * rate["2026-06"], "July steps up on June")
    ok(min(rate["2026-07"], rate["2026-08"], rate["2026-09"]) > max(rate[m] for m in
                                                                      ["2026-01", "2026-02", "2026-03",
                                                                       "2026-04", "2026-05"]), "Q3 above H1")
    h1 = G.trace(Gd, D(2026, 1, 1), D(2026, 6, 30))
    h1c = Counter(f for f, _ in h1.values())
    ok(fc["Travel & routing"] > 1.4 * h1c["Travel & routing"] / 2, "travel origin rises after the go-live")
    ok(fc["Travel & routing"] < 0.25 * sum(fc.values()), "travel origin is a minority of Q3")
    # ---------------------------------------------------------------- trace equals the world's truth
    truth = {a["appointment_ref"]: sample.FAMILY[a["day"]["event"][0]] for a in W.appointments
             if a["missed"] and D(2026, 7, 1) <= a["date"] <= D(2026, 9, 30)}
    ok(len(truth) == len(q3), "trace finds every Q3 miss")
    ok(all(q3[r][0] == f for r, f in truth.items()), "trace family equals truth on every Q3 miss")
    # ---------------------------------------------------------------- single origin and margins
    n_multi = 0
    for r in W.day_records:
        if r["missed"]:
            ok(r["event"] is not None, "every missed day has one event")
        for j, a in zip(r["jobs"], r["acts"]):
            late = a["arr"] - j["window"][1]
            if 0 < late < 15 or -3 < late <= 0:
                n_multi += 1
    ok(n_multi == 0, "no arrival within 3 min before or 15 min after a window end")
    # ---------------------------------------------------------------- rest identification
    gap = [c for c in W.calls if c["cover"] == "Call-out list" and 20 * 60 + 40 < c["cleared_m"] <= 21 * 60 + 10]
    ok(not gap, "no call-out-list clear between 20:41 and 21:10")
    for (eid, d), clr in W.rest_days.items():
        r = [x for x in W.day_records if x["engineer_id"] == eid and x["date"] == d][0]
        ok(660 <= r["logon"] - clr <= 664, "rest-forced log-on at clear plus 11h00 to 11h04")
    for r in W.day_records:
        if r["event"] and r["event"][0] == "late":
            ok((r["engineer_id"], r["date"]) not in W.rest_days, "no genuine late log-on on a rest day")
    # L1: the verification window is blind
    for c in W.calls:
        n = c["night"]
        if c["cover"] == "Call-out list" and D(2025, 10, 1) <= n <= D(2026, 5, 31):
            ok(c["cleared_m"] <= 20 * 60 + 40, "no late call-out-list clear from October to May")
    # ---------------------------------------------------------------- calibration corpus
    ver = Gd["verified"]
    ok(len(ver) == 200, "200 verified cases")
    apps_by_ref = {a["appointment_ref"]: a for a in Gd["apps"]}
    jan_may = G.trace(Gd, D(2026, 1, 1), D(2026, 5, 31))
    hits = sum(1 for v in ver if jan_may[v["appointment_ref"]][0] == v["cause_family"])
    ok(hits == 200, "same-day trace reproduces 200 of 200 verified families")
    ok(not any(v["cause_family"] == "Rota & cover" for v in ver), "no verified case is Rota & cover")
    same = G.trace(Gd, D(2026, 1, 1), D(2026, 5, 31), cross_day=False)
    ok(sum(1 for v in ver if same[v["appointment_ref"]][0] == v["cause_family"]) == 200,
       "verified sample cannot tell the two traces apart (L1)")
    # one-hop and direct readings against the corpus
    oh_fam = {}
    by_day = defaultdict(list)
    for a in Gd["apps"]:
        if G.attended(a):
            by_day[(a["engineer_id"], a["appointment_date"])].append(a)
    for v in ver:
        a = apps_by_ref[v["appointment_ref"]]
        day = sorted(by_day[(a["engineer_id"], a["appointment_date"])], key=lambda x: G.ts(x["en_route_at"]))
        i = [x["appointment_ref"] for x in day].index(a["appointment_ref"])
        er, on = G.ts(a["en_route_at"]), G.ts(a["on_site_at"])
        if a["travel_mode"] == "Via merchant":
            f = "Parts & van stock"
        elif a["travel_mode"] == "Vehicle recovery":
            f = "Other"
        elif G.mins_between(er, on) - int(a["planned_travel_min"]) > 14:
            f = "Travel & routing"
        elif i == 0:
            f = "Engineer attendance & punctuality"
        else:
            f = "Job duration & standards"
        oh_fam[v["case_ref"]] = f == v["cause_family"]
    oh_hits = sum(oh_fam.values())
    ok(oh_hits <= 150, "one hop reproduces at most 150 of 200")
    out["corpus"] = {"same_day": hits, "one_hop": oh_hits}
    # twin pair
    r1, r2 = W.twin
    ok(r1["date"] < D(2026, 6, 1) <= D(2026, 7, 1) <= r2["date"], "twin dates either side")
    ok(r1["logon"] == r2["logon"], "twin log-on minute identical")
    ok([a["arr"] for a in r1["acts"]] == [a["arr"] for a in r2["acts"]], "twin on-site times identical")
    ok([j["window"] for j in r1["jobs"]] == [j["window"] for j in r2["jobs"]], "twin windows identical")
    ok(r1["missed"] == r2["missed"] and len(r1["missed"]) >= 2, "twin misses identical")
    ok(r1["event"][0] == "late" and r2["event"][0] == "rest", "twin origins differ")
    tw_ref = [a for a in W.appointments if a["day"] is r1 and a["missed"]][0]["appointment_ref"]
    ok(any(v["appointment_ref"] == tw_ref for v in ver), "spring twin is in the verified sample")
    # Q3 2025 stays near baseline
    q325 = G.trace(Gd, D(2025, 7, 1), D(2025, 9, 30))
    c25 = Counter(f for f, _ in q325.values())
    ok(c25["Rota & cover"] < 0.12 * sum(c25.values()), "Q3 2025 Rota & cover share small")
    # ---------------------------------------------------------------- ask devices: every path misses every family
    import askpaths
    cred = out["credits_by_family"]
    comp = out["complaints_by_family"]
    ok(set(cred) == set(G.FAMILIES) and set(comp) == set(G.FAMILIES), "credits and complaints in every family")
    allq = G.trace(Gd, D(2026, 6, 1), D(2026, 9, 30))
    CP = askpaths.credit_paths(Gd, q3, allq)
    ok(dict(CP["golden"]) == cred, "the credit paths' golden is the golden")
    for p, floor in CREDIT_PATHS.items():
        for f in G.FAMILIES:
            gap = abs(CP[p].get(f, 0) - cred[f])
            ok(gap >= max(20, floor * cred[f]), "credit path %s misses %s by %d" % (p, f, gap))
    QP = askpaths.complaint_paths(Gd, q3)
    ok(dict(QP["golden"]) == comp, "the complaint paths' golden is the golden")
    ok(QP["any_category"] == QP["golden"], "every complaint about a missed household-day is in one of the two "
                                           "missed-appointment categories (the category cannot move the count)")
    import math
    for p, floor in COMPLAINT_PATHS.items():
        for f in G.FAMILIES:
            gap = abs(QP[p].get(f, 0) - comp[f])
            ok(gap >= max(1, math.ceil(floor * comp[f])), "complaint path %s misses %s by %d" % (p, f, gap))
    # the guards that keep each device forced
    acc = Gd["accounts"]
    props = defaultdict(list)
    for k, v in acc.items():
        if v["bill_payer_account"]:
            props[v["bill_payer_account"]].append(k)
    hhk = lambda a: acc[a]["merged_into"] or a
    miss_day = {(hhk(a["account_ref"]), a["appointment_date"]) for f, a in q3.values()}
    import accounts as A
    ma = defaultdict(list)
    for c in Gd["credits"]:
        if c["reason_code"] == "MA" and c["account_ref"] in acc:
            ma[(c["account_ref"], c["visit_date"])].append(int(float(c["amount_gbp"])))
    wide = set()
    for (acct, day), amts in ma.items():
        if not ("2026-07-01" <= day <= "2026-09-30"):
            continue
        if acc[acct]["account_type"] == "Landlord":
            hits = [p for p in props[acct] if (p, day) in miss_day]
            if len(amts) > len(hits):
                wide.add(acct)
        else:
            ok(len(amts) == 1 and (hhk(acct), day) in miss_day, "a household's credit line is its own miss")
    ok(wide == set(W.portfolio), "only the letting agents' accounts carry other regions' lines")
    for l in W.portfolio:
        for h in props[l]:
            a = acc[h]
            ok(not a["cancelled_on"] and not a["merged_into"], "letting-agent property never cancelled or merged")
            ok(not a["priority_register_from"] or a["priority_register_from"] <= "2025-06-30",
               "letting-agent property's register status fixed across the window")
    ok(not any(c["account_ref"] in W.portfolio for c in Gd["complaints"]), "letting agents log no complaints")
    q3_days = [k for k in miss_day if "2026-07-01" <= k[1] <= "2026-09-30"]
    for (h, day) in q3_days:
        l = acc[h]["bill_payer_account"]
        if l in W.portfolio:
            run = A.run_date_for(D.fromisoformat(day)).isoformat()
            ok((l, day) in ma, "every let household's missed day carries a line on its agent's account")
    first = {}
    for c in Gd["complaints"]:
        r = c["complaint_ref"]
        if r not in first or c["received_at"] < first[r]["received_at"]:
            first[r] = c
    def household(acct, day):
        if acct not in acc:
            return None
        if acc[acct]["account_type"] == "Landlord":
            hs = [p for p in props[acct] if (p, day) in miss_day]
            return hs[0] if len(hs) == 1 else None
        return hhk(acct)
    canon_of, held = {}, {}
    for r, c in sorted(first.items(), key=lambda x: (x[1]["received_at"], x[0])):
        canon_of[r] = held.setdefault((c["account_ref"], c["received_at"], c["about_visit_date"]), r)
    n_new = 0
    for r, c in first.items():
        if c["status"] != "Reopened":
            continue
        ok(c["received_at"] >= "2026-09-01", "a reopening under a new reference only after the platform move")
        if c["account_ref"] not in acc or not c["about_visit_date"]:
            continue
        h = household(c["account_ref"], c["about_visit_date"])
        same = {canon_of[x["complaint_ref"]] for x in first.values() if x["about_visit_date"] == c["about_visit_date"]
                and x["complaint_ref"] != r and x["status"] in ("Closed", "Open") and x["received_at"] < "2026-09-01"
                and household(x["account_ref"], x["about_visit_date"]) == h}
        ok(h is not None and len(same) == 1, "a reopening under a new reference reopens exactly one earlier complaint")
        ok(not any(canon_of[x] != x for x in [r]), "a reopening under a new reference is never itself a carried record")
        n_new += 1
    ok(all((c["category"] in A.NEW_CATEGORY.values()) == (c["received_at"] >= "2026-09-01") for c in Gd["complaints"]),
       "the platform's category list from 1 September, the old list before it")
    # records carried across the move: two references, one record (same account, moment received, visit)
    carried = defaultdict(list)
    for r, c in first.items():
        carried[(c["account_ref"], c["received_at"], c["about_visit_date"])].append(c)
    pairs = [v for v in carried.values() if len(v) > 1]
    ok(all(len(v) == 2 for v in pairs), "a carried record appears on exactly two references")
    ok(all(all(x["received_at"] < "2026-09-01" for x in v) and any(x["status"] == "Open" for x in v) for v in pairs),
       "carried records were received before the move and the old platform's copy stands open")
    ok(all(v[0]["channel"] == v[1]["channel"] and v[0]["category"] == v[1]["category"] for v in pairs),
       "a carried record keeps its channel and category")
    out["carried_pairs"] = len(pairs)
    ok(out["reopened_as_new"] >= 7, "reopenings under a new reference in every family")
    # the priority-register joiners: the run reads the register on the run date
    joiners = 0
    for (h, day) in q3_days:
        p = acc[h]["priority_register_from"]
        run = A.run_date_for(D.fromisoformat(day)).isoformat()
        if p and day < p <= run:
            joiners += 1
    ok(joiners >= 7, "households joined the register between a missed visit and its run")
    days_elsewhere = Counter(acct for (acct, day), amts in ma.items() if "2026-07-01" <= day <= "2026-09-30"
                             and acc[acct]["account_type"] == "Landlord"
                             and not [p for p in props[acct] if (p, day) in miss_day])
    ok(set(days_elsewhere) == set(W.portfolio), "only the letting agents carry lines on days nothing here was missed")
    out["device_mass"] = {"credit_paths": {p: dict(CP[p]) for p in CP}, "complaint_paths": {p: dict(QP[p]) for p in QP},
                          "agent_days_elsewhere_q3": dict(days_elsewhere),
                          "letting_agents": len(W.portfolio), "let_by_agents": sum(len(props[l]) for l in W.portfolio),
                          "register_joiners_q3": joiners, "reopened_as_new_scotland": n_new}
    grid = out["patch_family"]
    team, cur = defaultdict(Counter), defaultdict(Counter)
    for f, a in q3.values():
        team[a["patch"]][f] += 1
        cur[Gd["map"][a["postcode_district"]]][f] += 1
    def moved_cells(x):
        return sum(1 for p in grid for f in G.FAMILIES if grid[p].get(f, 0) != x[p].get(f, 0))
    ok(moved_cells(team) >= 8, "stored-patch path moves 8+ cells of the full grid")
    ok(moved_cells(cur) >= 25, "current-map path moves 25+ cells of the full grid")
    pf = "Parts & van stock"
    ok(sum(1 for p in grid if grid[p].get(pf, 0) != team[p].get(pf, 0)) >= 4, "stored-patch path moves 4+ of the six asked cells")
    ok(sum(1 for p in grid if grid[p].get(pf, 0) != cur[p].get(pf, 0)) >= 5, "current-map path moves 5+ of the six asked cells")
    out["device_mass"].update({"patch_team_moves": moved_cells(team), "patch_current_moves": moved_cells(cur)})
    # weekly device
    wk = {k: sum(v.values()) for k, v in out["weekly"].items() if k >= "2026-01-01"}
    top = max(wk, key=wk.get)
    allm = G.trace(Gd, D(2025, 12, 29), D(2026, 9, 30))
    iso = Counter()
    for f, a in allm.values():
        d = D.fromisoformat(a["appointment_date"])
        iso[d - dt.timedelta(days=d.weekday())] += 1
    itop = max(iso, key=iso.get)
    ok(iso[itop] != wk[top] or itop.isoformat() != top, "ISO weeks give a different worst week")
    out["worst_week"] = {"start": top, "count": wk[top], "iso_start": itop.isoformat(), "iso_count": iso[itop]}
    second = sorted(wk.values())[-2]
    ok(wk[top] - second >= 4, "worst week clear of the next")
    alt = {}
    for sd in range(7):
        t, n = askpaths.weekly_worst(Gd, sd)
        alt[["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][sd]] = [t.isoformat(), n]
        if sd != 3:
            ok(n != wk[top], "weeks starting on another day give another worst-week count")
    ok(alt["Thu"] == [top, wk[top]], "planning weeks (Thursday to Wednesday) give the golden worst week")
    out["worst_week"]["by_week_start"] = alt
    # ---------------------------------------------------------------- separation: main call ignores the device columns
    import copy
    G2 = dict(Gd)
    G2["apps"] = [dict(a, patch="X", account_ref="HC0000000", postcode_district="ZZ1") for a in Gd["apps"]]
    q3b = G.trace(G2, D(2026, 7, 1), D(2026, 9, 30))
    ok(Counter(f for f, _ in q3b.values()) == Counter(fc), "main call untouched by patch, account and district")
    # ---------------------------------------------------------------- lens swap: no day-app column separates the two log-on kinds
    rest_late = sorted(r["logon"] - 480 for r in W.day_records if r["event"] and r["event"][0] == "rest"
                       and r["missed"] and r["date"] >= D(2026, 7, 1))
    gen_late = sorted(r["logon"] - 480 for r in W.day_records if r["event"] and r["event"][0] == "late"
                      and r["missed"] and r["date"] >= D(2026, 7, 1))
    overlap = sum(1 for x in rest_late if gen_late[0] <= x <= gen_late[-1]) / len(rest_late)
    ok(overlap >= 0.5, "late-minute ranges overlap for rest-forced and genuine log-ons")
    out["lens_overlap"] = round(overlap, 3)
    # ---------------------------------------------------------------- clean-data test: repair the day app to carry call-out work
    # repaired instrument: the day log shows each engineer's last work of the previous evening; the answer and
    # the same-day reading do not move, because neither uses the log-off column
    ok(Counter(f for f, _ in G.trace(Gd, D(2026, 7, 1), D(2026, 9, 30), cross_day=False).values()) ==
       Counter(out["same_day_q3"]), "same-day reading stable")
    return N
