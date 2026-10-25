"""The shipped records, row by row, as each system exports them."""
import csv
import datetime as dt
import numpy as np
import common as K
import world as W

GROUP_NAME = {g: K.GROUPS[g]["name"] for g in K.GROUP_ORDER}
DAYS_LABEL = {"WD": "MO-FR", "SA": "SAT", "SU": "SUN"}
WAVE_LABEL = {2025: "Spring 2025", 2026: "Spring 2026"}


def write_csv(path, head, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f, lineterminator="\r\n")
        wr.writerow(head)
        for r in rows:
            wr.writerow(["" if v is None else v for v in r])


def surveyed_uids(sv):
    return {(b["date"], b["uid"]) for b in sv.batches}


# ------------------------------------------------------------------ survey
def responses(sv):
    head = ["serial", "wave", "batch_id", "return_mode", "received", "q1_overall"] + [q for q, _ in K.ITEMS] + \
           ["q5k", "board_station_written", "board_station_code", "alight_station_written", "alight_station_code",
            "ticket_type", "journey_purpose", "travel_frequency", "age_band", "weight"]
    rows = []
    for wave in (2025, 2026):
        rs = [x for x in sv.resp if x["wave"] == wave]
        rg = W.rng_for("serials", wave)
        order = rg.permutation(len(rs))
        base = 410000 if wave == 2025 else 530000
        for n, idx in enumerate(order):
            x = rs[idx]
            x["serial"] = "%d-%06d" % (wave % 100, base + 3 * n + int(rg.integers(0, 3)))
            r2 = W.rng_for("resp", wave, x["batch"], x["k"])
            lag = int(r2.integers(2, 19)) if x["mode"] == "post" else int(r2.integers(0, 6))
            rec = x["date"].toordinal() + lag
            import datetime as dt
            rec = dt.date.fromordinal(rec)
            code_b = x["board"] if r2.random() > 0.12 else ""
            code_a = x["alight"] if r2.random() > 0.12 else ""
            R = x["R"]
            rows.append([x["serial"], WAVE_LABEL[wave], x["batch"], "Post" if x["mode"] == "post" else "Online",
                         rec.isoformat(), x["overall"]] + [R.get(q) for q, _ in K.ITEMS] + [R.get("q5k")] +
                        [x["board_text"], code_b, x["alight_text"], code_a, x["ticket"], x["purpose"], x["freq"], x["age"],
                         "%.4f" % x["weight"]])
    rows.sort(key=lambda r: (r[1], r[0]))
    return head, rows


def fieldwork(sv):
    head = ["batch_id", "wave", "fieldwork_date", "train_headcode", "origin_station", "origin_dep", "service_group",
            "time_band", "fieldworker_on", "fieldworker_off", "units_covered", "questionnaires_issued",
            "returned_post", "returned_online"]
    rows = []
    for b in sorted(sv.batches, key=lambda b: b["batch"]):
        rows.append([b["batch"], WAVE_LABEL[b["wave"]], b["date"].isoformat(), b["headcode"], b["origin"],
                     W.hm(b["dep"]), GROUP_NAME[b["group"]], K.TIME_BANDS[b["band"]], b["fw_board"], b["fw_alight"],
                     b["units_covered"], b["issued"], b["post"], b["online"]])
    return head, rows


# ------------------------------------------------------------------ operations
def timetable(w):
    head = ["timetable", "train_uid", "headcode", "service_group", "days_run", "call_seq", "station", "arr", "dep"]
    rows = []
    for label in ("Dec24", "Dec25"):
        for t in sorted(w.tt[label].trains, key=lambda t: (t["group"], t["daytype"], t["dir"], t["start"])):
            for j, (st, a, d) in enumerate(t["calls"]):
                rows.append([label, t["uid"], t["headcode"], t["group"], DAYS_LABEL[t["daytype"]], j + 1, st,
                             W.hm(a) if a is not None else "", W.hm(d) if d is not None else ""])
    return head, rows


def movements(w):
    head = ["run_date", "train_uid", "headcode", "station", "event_type", "wtt_time", "recorded_time"]
    rows = []
    for r in sorted(w.runs, key=lambda r: (r["date"], r["t"]["start"], r["uid"])):
        if r["cancel"] == "full":
            continue
        calls = r["t"]["calls"]
        for j, (st, a, d) in enumerate(r["acts"]):
            pa, pd = calls[j][1], calls[j][2]
            if a is not None:
                rows.append([r["date"].isoformat(), r["uid"], r["headcode"], st, "ARRIVAL", W.hm(pa), W.hm(a)])
            if d is not None:
                rows.append([r["date"].isoformat(), r["uid"], r["headcode"], st, "DEPARTURE", W.hm(pd), W.hm(d)])
    return head, rows


def loadweigh(w, sv):
    """Passengers estimated from each unit's suspension weight at departure: class 166 units report each of their
    three vehicles, the two-car classes the unit. Units on a few late-evening and weekend runs that no survey
    batch rode lost their recorder data."""
    head = ["run_date", "headcode", "unit_no", "vehicle", "station", "departed", "passengers_est"]
    rows = []
    surv = surveyed_uids(sv)
    for r in sorted(w.runs, key=lambda r: (r["date"], r["t"]["start"], r["uid"])):
        if r["cancel"] == "full":
            continue
        rg = W.rng_for("lw", r["date"].isoformat(), r["uid"])
        band = W.time_band(r["date"], r["t"]["start"], True)
        gap = (r["date"], r["uid"]) not in surv and band in (3, 4) and rg.random() < 0.025
        if gap:
            continue
        seats = [K.CLASSES[w.unit_class(u, r["date"])][1] for u in r["units"]]
        for x, (st, a, d) in enumerate(r["acts"]):
            if d is None:
                continue
            tot = r["load"][x]
            if len(r["units"]) == 1:
                split = [tot]
            else:
                sh = seats[0] / sum(seats) * float(np.clip(rg.normal(1.0, 0.07), 0.8, 1.2))
                first = int(round(tot * min(0.95, max(0.05, sh))))
                split = [first, tot - first]
            for u, n in zip(r["units"], split):
                # from the fleet system's move in May 2026 an attached unit reports the headcode it was attached
                # under for every train of its strengthening turn
                hc = r.get("tag", {}).get(u, r["headcode"]) if r["date"] >= K.CREW_SYSTEM_MOVE else r["headcode"]
                if w.unit_class(u, r["date"]) == "166":
                    p = rg.dirichlet([6, 7, 6])
                    v = rg.multinomial(n, p)
                    if r["date"] >= K.CREW_SYSTEM_MOVE:
                        v = [n, n, n]       # the new feed writes the unit's estimate on each vehicle's row
                    for k, nv in enumerate(v):
                        rows.append([r["date"].isoformat(), hc, u, "%s-%d" % (u, k + 1), st, W.hm(d), int(nv)])
                else:
                    rows.append([r["date"].isoformat(), hc, u, "", st, W.hm(d), int(n)])
    return head, rows


def formations(w):
    head = ["run_date", "train_uid", "headcode", "position", "unit_no"]
    rows = []
    for r in sorted(w.runs, key=lambda r: (r["date"], r["t"]["start"], r["uid"])):
        for k, u in enumerate(r["units"]):
            rows.append([r["date"].isoformat(), r["uid"], r["headcode"], k + 1, u])
    return head, rows


def crew_as_worked(w):
    """The as-worked archive: one row per train a member of on-board staff worked. A train nobody worked has no
    row."""
    head = ["work_date", "headcode", "diagram", "grade", "staff_ref"]
    rows = []
    days = set(K.WINDOWS["w2025"]) | set(K.WINDOWS["w2026"])
    for r in sorted(w.runs, key=lambda r: (r["date"], r["t"]["start"], r["uid"])):
        if r["date"] in days and r["staffed"] and r["cancel"] != "full":
            rows.append([r["date"].isoformat(), r["headcode"], r["diagram"], r["role"], r["staff_ref"]])
    return head, rows


def crew_live(w):
    """The new rostering platform: a turn per diagram with its workings, its status on the day, and the
    amendments that put a spare on a turn whose member of staff went sick or was never filled."""
    head = ["roster_date", "diagram", "grade", "staff_ref", "status", "workings"]
    amend_head = ["amend_date", "diagram", "original_staff_ref", "cover_staff_ref", "reason", "logged"]
    rows, amends = [], []
    days = K.WINDOWS["latest"]
    for d in days:
        diags = {}
        for r in w.runs:
            if r["date"] == d:
                diags.setdefault(r["diagram"], []).append(r)
        for dg in sorted(diags):
            rs = sorted(diags[dg], key=lambda r: r["t"]["start"])
            turn = rs[0].get("turn")
            if not turn:
                continue
            rows.append([d.isoformat(), dg, turn["grade"], turn["staff"], turn["status"],
                         ";".join(r["headcode"] for r in rs)])
            if turn["cover"]:
                on = d - dt.timedelta(days=1) if turn["logged_day_before"] else d
                amends.append([on.isoformat(), dg, turn["staff"], turn["cover"], turn["reason"], turn["logged"]])
    amends.sort(key=lambda a: (a[0], a[5], a[1]))
    return (head, rows), (amend_head, amends)


def fares(w):
    head = ["from_station", "to_station", "ticket_type", "fare_before_pence", "fare_from_04jan2026_pence"]
    rows = [[key[0], key[1], tt, before, after] for (key, tt), (before, after) in W.FARES.items()]
    return head, rows


def stations():
    head = ["crs_code", "station_name", "service_groups"]
    rows = []
    for code in sorted(K.STATIONS):
        gs = [K.GROUPS[g]["name"] for g in K.GROUP_ORDER if code in [c for c, _ in K.GROUPS[g]["calls"]]]
        rows.append([code, K.STATIONS[code], "; ".join(gs)])
    return head, rows
