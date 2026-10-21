"""The pack's records from the world: the delivery vendor's results exports (release 3 to May 2027, release 4 from
August 2027), the form layouts, the item bank snapshot and the January 2027 renumbering crosswalk, the candidate
register's number changes, the results review bookings; for the asks, the session seat plan, the workstation event
log and the invigilators' incident reports, and the item review panel's decision log.   R = records.build(W)"""
import datetime as dt

import numpy as np
import pandas as pd

import params as P
import sim

IST = dt.timedelta(hours=5, minutes=30)
SESSION_START = {"AM": (9, 30), "PM": (14, 30)}
WORKSTATIONS = {"Chennai": 60, "Bengaluru": 42, "Hyderabad": 40, "Pune": 30, "Kochi": 24, "Noida": 28}
SPARES = 4
MIGRATION = dt.date(2027, 1, 11)
SNAPSHOT = dt.date(2027, 12, 31)
PANEL = {4: dt.date(2027, 4, 13), 5: dt.date(2027, 7, 13), 6: dt.date(2027, 10, 12), 7: dt.date(2027, 12, 14),
         0: dt.date(2026, 4, 14), 1: dt.date(2026, 7, 14), 2: dt.date(2026, 10, 13), 3: dt.date(2026, 12, 15)}


def window_day(w, d):
    y, m, dd = P.W_START[P.WINDOWS[w]]
    return dt.date(y, m, dd) + dt.timedelta(days=int(d))


def results_day(w):
    return window_day(w, P.RESULTS_AFTER)


def identities(W, rs):
    """item numbers (the 2026 scheme and the 2027 bank's), item model codes, keyed answers, candidate numbers"""
    B = W["B"]
    n = B["n"]
    old = ["CC-%05d" % v for v in 10000 + rs.permutation(n)]
    new = ["CCB-%06d" % v for v in 200000 + rs.choice(800000, n, replace=False)]
    mcode = ["IM-%04d" % v for v in 1000 + rs.permutation(B["nm"])]
    model = [mcode[m] for m in B["model"]]
    key = rs.choice(list("ABCD"), n)
    return dict(old=old, new=new, model=model, key=key)


def cand_no(year, serial):
    """the Institute's candidate number: the year of issue, a five-digit serial and a Luhn check digit"""
    body = "%02d%05d" % (year - 2000, 10000 + serial)
    tot = 0
    for i, ch in enumerate(reversed(body)):
        d = int(ch) * (2 if i % 2 == 0 else 1)
        tot += d - 9 if d > 9 else d
    return body + str((10 - tot % 10) % 10)


# the register's class changes, in about the mix the membership office sees
CLASS_CHANGES = ["student to associate"] * 13 + ["associate to member"] * 5 + ["overseas to resident associate"] * 2


def candidate_numbers(W, rs):
    """each candidate's number at each sitting: 26 or 27 by the year of registration, a new number when the
    candidate's membership class changed between sittings"""
    cands, rows = W["cands"], W["rows"]
    serial = {2026: 0, 2027: 0}
    first = {}
    for r in rows:
        first.setdefault(r["cand"], r["w"])
    order = sorted(first, key=lambda k: (first[k], rs.uniform()))
    base = {}
    for k in order:
        y = 2026 if first[k] < 4 else 2027
        serial[y] += 1
        base[k] = cand_no(y, serial[y])
    num, changes, current = [], [], dict(base)
    held = {k: [(dt.date.min, v)] for k, v in base.items()}      # each candidate's numbers and when each began
    for r in rows:
        k = r["cand"]
        if r["n_prev"] > 0 and r["w"] >= 4 and rs.uniform() < P.P_RENUMBER:
            prev = W["cands"][k]["hist"][r["n_prev"] - 1]
            lo = results_day(prev["w"]) + dt.timedelta(days=10)
            hi = window_day(r["w"], 0) - dt.timedelta(days=12)
            on = lo + dt.timedelta(days=int(rs.integers(0, max(1, (hi - lo).days))))
            # the new number is issued below, in the order the register made the changes
            newno = "#%06d" % len(changes)
            change = CLASS_CHANGES[(len(changes) * 7 + 3) % len(CLASS_CHANGES)]
            changes.append(dict(previous_candidate_no=current[k], candidate_no=newno, changed_on=on.isoformat(),
                                reason="membership class changed (%s)" % change))
            current[k] = newno
            held[k].append((on, newno))
        num.append(current[k])
    # a new number carries the year it was issued, serials running in the order of the changes
    issued = {}
    for c in sorted(changes, key=lambda c: (c["changed_on"], c["candidate_no"])):
        y = int(c["changed_on"][:4])
        serial[y] += 1
        issued[c["candidate_no"]] = cand_no(y, serial[y])
    num = [issued.get(n, n) for n in num]
    for c in changes:
        c["previous_candidate_no"] = issued.get(c["previous_candidate_no"], c["previous_candidate_no"])
        c["candidate_no"] = issued[c["candidate_no"]]
    held = {k: [(d, issued.get(n, n)) for d, n in v] for k, v in held.items()}
    reg = pd.DataFrame(changes)
    if len(reg):
        reg = reg.sort_values(["changed_on", "candidate_no"]).reset_index(drop=True)
    return num, reg, held


def schedule(W, rs):
    """centre, day, session and workstation of every sitting, and its booking reference"""
    rows = W["rows"]
    out = [None] * len(rows)
    by_w = {}
    for i, r in enumerate(rows):
        by_w.setdefault(r["w"], []).append(i)
    used = set()
    for w, idx in by_w.items():
        cen = rs.choice(len(P.CENTRES), len(idx), p=P.CENTRE_W)
        for c, cname in enumerate(P.CENTRES):
            mine = [idx[q] for q in np.flatnonzero(cen == c)]
            mine = [mine[q] for q in rs.permutation(len(mine))]
            slots = [(d, s) for d in range(P.WINDOW_DAYS) for s in ("AM", "PM")]
            cap = WORKSTATIONS[cname]
            per = int(np.ceil(len(mine) / len(slots)))
            assert per <= cap, (cname, per, cap)
            for q, i in enumerate(mine):
                d, s = slots[q % len(slots)]
                out[i] = dict(centre=cname, day=d, session=s)
            for (d, s) in slots:
                here = [i for i in mine if out[i]["day"] == d and out[i]["session"] == s]
                ws = rs.choice(cap, len(here), replace=False) + 1
                for i, k in zip(here, ws):
                    out[i]["workstation"] = "WS%02d" % k
    for i in range(len(rows)):
        while True:
            b = "BK%08d" % rs.integers(10 ** 7, 10 ** 8)
            if b not in used:
                used.add(b)
                break
        out[i]["booking_ref"] = b
        out[i]["date"] = window_day(rows[i]["w"], out[i]["day"])
    return out


def response_strings(W, ids, rs):
    """the response letter (or '-') and the milliseconds on every delivered position"""
    key = ids["key"]
    resp, ms = [], []
    for r in W["rows"]:
        letters = []
        for j, xv, rc in zip(r["seq"], r["x"], r["reach"]):
            if not rc:
                letters.append("-")
            elif xv:
                letters.append(key[j])
            else:
                letters.append(rs.choice([c for c in "ABCD" if c != key[j]]))
        resp.append("".join(letters))
        ms.append(np.where(r["reach"], r["ms"].astype(int), -1))
    return resp, ms


def exports(W, ids, nums, sched, resp, ms):
    """release 3 (February 2026 to May 2027): seconds, names; release 4 (August 2027 on): milliseconds, codes"""
    rows = W["rows"]
    a, b = [], []
    for i, r in enumerate(rows):
        s = sched[i]
        if r["w"] < 6:
            secs = "|".join("" if v < 0 else str(int(round(v / 1000))) for v in ms[i])
            a.append(dict(candidate_no=nums[i], booking_ref=s["booking_ref"], window=P.WINDOWS[r["w"]],
                          sitting_date=s["date"].isoformat(), centre=s["centre"], form=r["form"],
                          responses=resp[i], item_seconds=secs,
                          end="submitted" if r["reach"][-1] else "time expired", score=r["raw"],
                          result="Pass" if r["passed"] else "Fail"))
        else:
            lat = "|".join("" if v < 0 else str(int(v)) for v in ms[i])
            b.append(dict(cand_no=nums[i], booking_ref=s["booking_ref"], exam_window=P.WINDOWS[r["w"]],
                          sat_on=s["date"].strftime("%d-%m-%Y"), test_centre=P.CENTRE_CODE[s["centre"]],
                          form_code=r["form"], response_string=resp[i], latency_ms=lat,
                          end_reason="SUBMITTED" if r["reach"][-1] else "TIME_EXPIRED", raw_score=r["raw"],
                          outcome="P" if r["passed"] else "F"))
    A = pd.DataFrame(a)
    Bx = pd.DataFrame(b)
    return A, Bx


def layouts(W, ids):
    out = []
    for w, win in enumerate(P.WINDOWS):
        for fi in P.W_FORMS[w]:
            f = sim.FORMS[fi]
            seq, kind = sim.layout(W["forms"], W["trial"], f, w)
            code = ids["old"] if w < 4 else ids["new"]
            for p, (j, k) in enumerate(zip(seq, kind), 1):
                out.append(dict(window=win, form=f, position=p, item_id=code[j], slot="scored" if k == "S" else "trial"))
    return pd.DataFrame(out)


def trial_decisions(W, rs):
    """the item review panel's decision on each tried item (accept, revise, reject), by the item's statistics among
    the window's first-time candidates, and later reversals"""
    B, rows = W["B"], W["rows"]
    dec = {}
    for (w, f), items in W["trial"].items():
        ft = [r for r in rows if r["w"] == w and r["form"] == f and r["n_prev"] == 0]
        for q, j in enumerate(items):
            pos = P.TRIAL_SLOTS[q] - 1
            xs = np.array([r["x"][pos] for r in ft if r["reach"][pos]], float)
            tot = np.array([r["raw"] for r in ft if r["reach"][pos]], float)
            pv = xs.mean() if len(xs) else 0.0
            rp = float(np.corrcoef(xs, tot)[0, 1]) if len(xs) > 2 and xs.std() > 0 else 0.0
            if 0.30 <= pv <= 0.90 and rp >= 0.15:
                d = "accept"
            elif rp >= 0.10:
                d = "revise"
            else:
                d = "reject"
            dec[j] = dict(w=w, form=f, decision=d, p=pv, r=rp)
    promoted = set(j for f in P.F27 for j in W["forms"][f]) & set(dec)
    for j in promoted:
        dec[j]["decision"] = "accept"
    return dec


def bank_snapshot(W, ids, dec, logged):
    """the item bank as at 31 December 2027: every item, its model, format, content area, key and status"""
    B = W["B"]
    on_form = set(j for f in W["forms"] for j in W["forms"][f])
    out = []
    for j in range(B["n"]):
        if j in on_form:
            st = "operational"
        elif j in dec:
            lg = logged.get(j)
            if lg is None or lg[1] > SNAPSHOT:
                st = "pretest"
            else:
                st = {"accept": "operational", "revise": "returned to writer", "reject": "retired",
                      "withdraw": "retired"}[lg[0]]
        else:
            st = "draft"
        out.append(dict(item_id=ids["new"][j], item_model=ids["model"][j], item_format="case" if B["case"][j] else "single",
                        content_area=P.AREAS[B["area"][j]], key=ids["key"][j], status=st))
    return pd.DataFrame(out).sort_values("item_id").reset_index(drop=True)


def crosswalk(W, ids, rs):
    B = W["B"]
    out = [dict(previous_item_id=ids["old"][j], item_id=ids["new"][j], migrated_on=MIGRATION.isoformat())
           for j in range(B["n"])]
    return pd.DataFrame(out).sort_values("previous_item_id").reset_index(drop=True)


EXTRACTED = dt.date(2028, 1, 14)               # the review bookings extract, the Friday before the request


def number_on(held, k, day):
    """the candidate's number in force on a day"""
    return [n for d, n in held[k] if d <= day][-1]


def reviews(W, held, rs):
    """results review bookings: a failing candidate books within eight weeks of the result; held, cancelled or not
    attended"""
    out = []
    serial = 0
    for i, r in enumerate(W["rows"]):
        if not r["review_booked"]:
            continue
        serial += 1
        res = results_day(r["w"])
        booked = res + dt.timedelta(days=int(rs.integers(1, 30)))
        on = booked + dt.timedelta(days=int(rs.integers(4, 25)))
        if r["review_held"]:
            st = "held"
        else:
            st = "cancelled" if rs.uniform() < 0.55 else "did not attend"
        if on > EXTRACTED:
            st = "booked"                       # still to come when the bookings were extracted
        out.append(dict(review_no="RV%06d" % (300000 + serial * 13 % 600000 + serial),
                        candidate_no=number_on(held, r["cand"], booked),
                        sitting_window=P.WINDOWS[r["w"]], booked_on=booked.isoformat(), review_date=on.isoformat(),
                        status=st))
    df = pd.DataFrame(out)
    return df.sort_values(["booked_on", "review_no"]).reset_index(drop=True)


def build(W, seed=P.SEED):
    ss = np.random.SeedSequence(seed + 101)
    r_id, r_num, r_sch, r_resp, r_rev, r_dec = [np.random.default_rng(s) for s in ss.spawn(6)]
    ids = identities(W, r_id)
    nums, changes, held = candidate_numbers(W, r_num)
    sched = schedule(W, r_sch)
    resp, ms = response_strings(W, ids, r_resp)
    exp_a, exp_b = exports(W, ids, nums, sched, resp, ms)
    lay = layouts(W, ids)
    dec = trial_decisions(W, r_dec)
    return dict(ids=ids, nums=nums, changes=changes, held=held, sched=sched, resp=resp, ms=ms, exp_a=exp_a, exp_b=exp_b,
                layouts=lay, dec=dec, crosswalk=crosswalk(W, ids, r_id), reviews=reviews(W, held, r_rev))
