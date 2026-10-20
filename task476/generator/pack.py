"""Everything the pack and the golden are cut from, computed once, and the CSV writers."""
import csv
import datetime as dt

import asks as K
import methods as M
import records as R
import truth as T
import world as W


def everything():
    segs = T.segments()
    lk = T.leaks(segs)
    prem = K.premises(segs)
    x = dict(segs=segs, leaks=lk, costs=K.cost_lines(lk), prem=prem)
    x["tickets"] = K.tickets(lk, prem)
    x["fig"] = figures(x)
    return x


def inventory_rows(x):
    """The 2026 leaks as the methods read them: district, how found, find time, previous survey, grade, repair."""
    rows = []
    for L in x["leaks"]:
        if L.found.year != W.YEAR:
            continue
        prev = None
        if L.how == "SURVEY":
            prev = L.seg.surveys[W.YEAR - 1] if L.seg.surveys[W.YEAR] == L.found.date() else L.seg.surveys[W.YEAR]
        rep = L.repaired if L.repaired.date() <= W.EXTRACT else None
        rows.append(dict(district=L.seg.district, how=L.how, found=L.found, prev=prev, grade=L.grade,
                         repaired=rep, lid=L.lid, true=L.start))
    return rows


def miles(x):
    out = {d: 0.0 for d in W.DISTRICTS}
    for s in x["segs"]:
        if s.material in ("CI", "BS"):
            out[s.district] += int(round(s.miles * 5280)) / 5280.0     # the GIS carries whole feet
    return out


def figures(x):
    rows = inventory_rows(x)
    prof = M.profile([L.found for L in x["leaks"] if L.how == "ODOR"])
    mi = miles(x)
    t = M.methane(rows, "golden", prof, W.RATE, W.END)
    out = []
    for d in W.DISTRICTS:
        n = sum(1 for r in rows if r["district"] == d)
        out.append(dict(district=d, leaks=n, tonnes=t.get(d, 0.0), miles=mi[d], per_mile=t.get(d, 0.0) / mi[d],
                        designated=t.get(d, 0.0) / mi[d] >= W.LINE))
    return dict(rows=out, profile=prof, designated=[r["district"] for r in out if r["designated"]],
                ask_a=K.ask_a(x["costs"]), ask_b=K.ask_b(x["tickets"], x["prem"]))


def write_csv(path, cols, rows, crlf=False):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\r\n" if crlf else "\n")
        w.writerow(cols)
        for r in rows:
            w.writerow(r)
    return len(rows)


def fmt(t):
    return t.strftime("%Y-%m-%d %H:%M")


SEG_COLS = ["segment_id", "district", "material", "length_ft", "street", "status"]


def seg_rows(x):
    return [[s.sid, s.district, {"CI": "CAST IRON", "BS": "BARE STEEL", "CS": "COATED STEEL", "PL": "PLASTIC"}[s.material],
             int(round(s.miles * 5280)), R.street(s).upper(), "IN SERVICE"] for s in sorted(x["segs"], key=lambda s: s.sid)]


SCHED_COLS = ["segment_id", "survey_year", "survey_date", "crew"]


def sched_rows(x):
    out = []
    for s in sorted(x["segs"], key=lambda s: s.sid):
        r = T.rng_for("crew", s.district)
        for y, d in sorted(s.surveys.items()):
            out.append([s.sid, y, d.strftime("%m/%d/%Y"), "LS-%02d" % (int(r.integers(1, 9)))])
    return out


FIND_COLS = ["leak_no", "found_local", "segment_id", "address", "grade", "reading_pct_lel", "crew"]


def find_rows(x):
    out = []
    for L in x["leaks"]:
        if L.how != "SURVEY":
            continue
        r = T.rng_for("find", L.lid)
        out.append([L.lid, fmt(L.found), L.seg.sid, R.address(L).upper(), R.grade_code(L.grade, L.found),
                    {1: int(r.integers(40, 100)), 2: int(r.integers(10, 40)), 3: int(r.integers(1, 10))}[L.grade],
                    "LS-%02d" % int(r.integers(1, 9))])
    return out


ODOR_COLS = ["call_id", "received_utc", "address", "outcome", "leak_no", "segment_id", "grade"]


def odor_rows(x):
    """Every odor call: the confirmed leaks with their leak number, and the calls that found no utility leak."""
    out = []
    n = 0
    for L in x["leaks"]:
        if L.how != "ODOR":
            continue
        n += 1
        out.append([n, L.found, R.address(L).upper(), "LEAK CONFIRMED", L.lid, L.seg.sid,
                    R.grade_code(L.grade, L.found)])
    rng = T.rng_for("noleak")
    k = len(out)
    for i in range(int(k * 1.7)):
        d = dt.datetime(2016, 1, 1) + dt.timedelta(minutes=int(rng.integers(0, 11 * 365 * 24 * 60)))
        out.append([0, d, "%d %s %s" % (int(rng.integers(1, 2400)), R.STREETS[int(rng.integers(0, 30))],
                                        R.SFX[int(rng.integers(0, 6))]),
                    str(rng.choice(["NO GAS FOUND", "CUSTOMER APPLIANCE", "CUSTOMER PIPING", "SEWER GAS"])), "", "", ""])
    out.sort(key=lambda r: r[1])
    rows = []
    for i, r in enumerate(out):
        u = R.to_utc(r[1])
        rows.append(["OC%07d" % (1000000 + i * 3), u.strftime("%Y-%m-%dT%H:%M:%SZ"), r[2].upper(), r[3], r[4], r[5],
                     r[6]])
    return rows


REP_COLS = ["order_no", "leak_no", "visit_local", "action", "grade", "crew"]


def repair_rows(x):
    out = []
    for L in x["leaks"]:
        r = T.rng_for("rep", L.lid)
        for k, (t, act, g) in enumerate(R.visits(L)):
            out.append(["RO-%s-%d" % (L.lid[1:], k + 1), L.lid, fmt(t), act, R.grade_code(g, t),
                        "RC-%02d" % int(r.integers(1, 7))])
    out.sort(key=lambda r: (r[2], r[0]))
    return out


COST_COLS = ["wo_no", "leak_no", "cost_center", "cost_type", "posted", "amount"]


def cost_rows(x):
    return [[c["wo"], c["leak"], c["cc"], c["type"], c["posted"].isoformat(), "%.2f" % c["amount"]] for c in x["costs"]]


TIX_COLS = ["ticket_no", "opened_local", "service_address", "cause", "leak_no", "restored_local"]


def ticket_rows(x):
    return [[t["ticket"], fmt(t["opened"]), t["addr"].upper(), "LEAK REPAIR SHUTOFF", t["leak"], fmt(t["restored"])]
            for t in x["tickets"]]


PREM_COLS = ["premise_id", "service_address", "district", "meters", "segment_id", "service_line_id"]


def prem_rows(x):
    return [[p["premise"], p["addr"].upper(), p["district"], p["meters"], p["seg"], p["service"]] for p in x["prem"]]


CLOSE_COLS = ["wo_no", "leak_no", "closed", "total_cost"]


def close_rows(x):
    """Work orders whose leak was repaired in 2025 or 2026: the closing date (the cost lines' last posting) and the
    total, the sum over types of each type's cost to date at its last posting."""
    last = {}
    for c in x["costs"]:
        k = (c["wo"], c["type"])
        last[k] = c
    rep = {L.lid: L.repaired for L in x["leaks"]}
    out = {}
    for (wo, ty), c in last.items():
        if rep[c["leak"]].year not in (2025, 2026) or rep[c["leak"]].date() > W.EXTRACT:
            continue
        o = out.setdefault(wo, [wo, c["leak"], c["posted"], 0.0])
        o[2] = max(o[2], c["posted"])
        o[3] += c["amount"]
    return [[o[0], o[1], o[2].isoformat(), "%.2f" % o[3]] for o in sorted(out.values(), key=lambda o: (o[2], o[0]))]
