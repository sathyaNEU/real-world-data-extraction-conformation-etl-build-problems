"""The two asks' records: the gatelines' cumulative counters in the census week, and Cardale's Delay Repay
claims for the record's journeys. Both are generated from the world as it ran (census offs, the running
record), then written as their own systems write them."""
import datetime as dt
import numpy as np
import params as P
import world as Wd

HM = P.HM


def _local_minute(t_hm):
    return t_hm / HM


# ---------------------------------------------------------------------------------------------------------
# Gatelines
# ---------------------------------------------------------------------------------------------------------

def _station_index(name):
    for line in P.LINES:
        if name in P.STATIONS[line]:
            return line, P.STATIONS[line].index(name)
    raise KeyError(name)


def _bst(day):
    # British Summer Time runs to the last Sunday in October
    return day < P.CLOCK_CHANGE


def gate_flows(W, day, rng):
    """Exits and entries per station per 15-minute interval (local), that day."""
    trains, census = W["trains"], W["census"]
    rec = W["records"].get(day)
    flows = {}
    for st in P.GATED:
        line, idx = _station_index(st)
        ex = np.zeros(96)
        en = np.zeros(96)
        for tr in trains:
            if tr["line"] != line or idx not in tr["stops"]:
                continue
            k = tr["stops"].index(idx)
            ons, offs = census[tr["id"]]
            if rec is not None:
                a = rec[tr["id"]]["arr"][k] if k > 0 else None
                d = rec[tr["id"]]["dep"][k] if k < len(tr["stops"]) - 1 else None
            else:
                a, d = tr["barr"][k], tr["bdep"][k]
            if a is not None and offs[k] > 0:
                q = int(_local_minute(a) // 15) % 96
                walk = rng.binomial(int(offs[k]), 0.35)
                ex[q] += offs[k] - walk
                ex[(q + 1) % 96] += walk
            if d is not None and ons[k] > 0:
                q = int(max(0, _local_minute(d) - rng.integers(2, 9)) // 15) % 96
                en[q] += ons[k]
        other = P.GATE_OTHER[st]
        for q in range(96):
            hr = q / 4.0
            busy = 0.0 if hr < 5.0 else (1.0 if 6.0 <= hr < 23.5 else 0.05)    # the gatelines open at 05:00
            ex[q] += rng.poisson(other * busy * (ex[q] + 6.0))
            en[q] += rng.poisson(other * busy * (en[q] + 6.0))
        flows[st] = (ex.astype(int), en.astype(int))
    return flows


TIDAL = {"BWR-B": (16 * 60 + 30, 19 * 60), "PLG-S": (7 * 60 + 30, 9 * 60 + 30), "SLG-MKT": (7 * 60 + 15, 9 * 60 + 30)}
RESTORES = {(dt.date(2026, 10, 13), "AMP-1"): dt.time(6, 31, 7), (dt.date(2026, 10, 15), "BWR-A"): dt.time(13, 7, 42)}
BACKUP_UTC = dt.time(1, 0)      # the controllers' nightly save, 02:00 BST


def gate_readings(W):
    """Rows (station, array, reading_utc, entries_counter, exits_counter) and the true local entries and exits
    of the census day by station. Each array keeps two cumulative 16-bit counters, read every UTC quarter-hour.
    A tidal array switched to exit-only in its station's peak still counts its passages in the entries counter.
    A controller restart writes a closing reading and resumes from the counters it saved at 02:00."""
    rng = np.random.default_rng([P.SEED, 9001, P.DRAW])
    split = {"BWR-A": 0.62, "BWR-B": 0.38, "AMP-1": 1.0, "PLG-N": 0.55, "PLG-S": 0.45, "SLG-MAIN": 0.71,
             "SLG-MKT": 0.29}
    per_day = {}
    truth = {}
    for day in P.GATE_DAYS:
        flows = gate_flows(W, day, rng)
        per = {}
        for st, arrays in P.GATED.items():
            ex, en = flows[st]
            for a_ in arrays:
                per[a_] = [np.zeros(96, dtype=int), np.zeros(96, dtype=int)]
            for q in range(96):
                m0 = q * 15
                if len(arrays) == 1:
                    per[arrays[0]][0][q], per[arrays[0]][1][q] = ex[q], en[q]
                    continue
                a0, a1 = arrays
                tid = [x for x in arrays if x in TIDAL and TIDAL[x][0] <= m0 < TIDAL[x][1]]
                if tid:
                    # the tidal array takes a larger share of the peak flow in its one direction, none the other way
                    t = tid[0]
                    o = a1 if t == a0 else a0
                    et = rng.binomial(ex[q], 0.58)
                    per[t][0][q], per[o][0][q] = et, ex[q] - et
                    per[t][1][q], per[o][1][q] = 0, en[q]
                else:
                    e0 = rng.binomial(ex[q], split[a0])
                    n0 = rng.binomial(en[q], split[a0])
                    per[a0][0][q], per[a1][0][q] = e0, ex[q] - e0
                    per[a0][1][q], per[a1][1][q] = n0, en[q] - n0
            if day == P.CENSUS_DAY:
                truth[st] = {"entered": int(en.sum()), "left": int(ex.sum())}
        per_day[day] = per
    start = {"BWR-A": [41233, 39810], "BWR-B": [12907, 14455], "AMP-1": [30518, 22374], "PLG-N": [52880, 49671],
             "PLG-S": [8132, 9245], "SLG-MAIN": [21902, 0], "SLG-MKT": [27741, 25530]}
    d0, d1 = P.GATE_DAYS[0], P.CENSUS_DAY
    before = int(per_day[d0]["SLG-MAIN"][0].sum()) + int(per_day[d1]["SLG-MAIN"][0][:72].sum())
    start["SLG-MAIN"][1] = P.COUNTER_WRAP - before - 37
    counters = {a_: list(v) for a_, v in start.items()}
    saved = {}
    rows = []
    for day in P.GATE_DAYS:
        off = 60 if _bst(day) else 0
        for st, arrays in P.GATED.items():
            for a_ in arrays:
                pex, pen = per_day[day][a_]
                for q in range(96):
                    t = dt.datetime.combine(day, dt.time(0)) + dt.timedelta(minutes=(q + 1) * 15 - off)
                    rb = RESTORES.get((day, a_))
                    passages_ex, passages_en = int(pex[q]), int(pen[q])
                    if a_ in TIDAL and TIDAL[a_][0] <= q * 15 < TIDAL[a_][1]:
                        # exit-only: every passage counted in the entries counter
                        passages_en, passages_ex = passages_ex + passages_en, 0
                    if rb is not None:
                        rb_utc = dt.datetime.combine(day, rb)
                        if t - dt.timedelta(minutes=15) < rb_utc <= t:
                            frac = (rb_utc - (t - dt.timedelta(minutes=15))).total_seconds() / 900.0
                            ex_b, en_b = int(round(passages_ex * frac)), int(round(passages_en * frac))
                            counters[a_][0] = (counters[a_][0] + en_b) % P.COUNTER_WRAP
                            counters[a_][1] = (counters[a_][1] + ex_b) % P.COUNTER_WRAP
                            rows.append((st, a_, rb_utc, counters[a_][0], counters[a_][1]))
                            counters[a_] = list(saved[(day, a_)])
                            counters[a_][0] = (counters[a_][0] + passages_en - en_b) % P.COUNTER_WRAP
                            counters[a_][1] = (counters[a_][1] + passages_ex - ex_b) % P.COUNTER_WRAP
                            rows.append((st, a_, t, counters[a_][0], counters[a_][1]))
                            continue
                    counters[a_][0] = (counters[a_][0] + passages_en) % P.COUNTER_WRAP
                    counters[a_][1] = (counters[a_][1] + passages_ex) % P.COUNTER_WRAP
                    rows.append((st, a_, t, counters[a_][0], counters[a_][1]))
                    if t.time() == BACKUP_UTC:
                        saved[(day, a_)] = list(counters[a_])
    rows.sort(key=lambda r: (r[2], r[0], r[1]))
    return rows, truth


# ---------------------------------------------------------------------------------------------------------
# Delay Repay
# ---------------------------------------------------------------------------------------------------------

def fare_single(n_stops):
    return round(2.20 + 0.42 * n_stops, 1)


def band_of(minutes):
    for name, lo, hi, share in P.DR_BANDS:
        if lo <= minutes < hi:
            return name
    return None


def ask_band(minutes):
    for name, lo, hi in P.ASK_BANDS:
        if lo <= minutes < hi:
            return name
    return None


def _share(band):
    return {b[0]: b[3] for b in P.DR_BANDS}[band]


def comp(ticket, fare1, band):
    """Delay Repay 15: single fare share; a return pays on half the return fare, the whole return at 120 or more;
    a season on its daily value per journey."""
    ret = round(fare1 * 1.8, 1)
    if ticket == "Anytime Single":
        base = fare1
    elif ticket == "Anytime Return":
        base = ret if band == "120 or more" else ret / 2.0
    elif ticket == "Weekly Season":
        base = round(ret * 4.3, 1) / 10.0
    else:  # Monthly Season
        base = round(ret * 16.5, 1) / 40.0
    return round(base * _share(band), 2)


def delay_repay(W):
    """Claims for journeys whose train reached the passenger's destination 15 or more minutes late, plus claims
    for journeys outside the record window and within-line journeys, with appeals paid as top-ups."""
    rng = np.random.default_rng([P.SEED, 7001, P.DRAW])
    trains, census, days = W["trains"], W["census"], W["days"]
    claims = []
    truth = {}
    seq = [100000]

    def ref():
        seq[0] += int(rng.integers(3, 40))
        return "DR%07d" % seq[0]

    tickets = ["Anytime Single", "Anytime Return", "Weekly Season", "Monthly Season"]
    tw = [0.27, 0.36, 0.17, 0.20]
    # booked departure minutes: (station, minute) -> stations the train calls at afterwards
    onward = {}
    for t_ in trains:
        for kk, s_ in enumerate(t_["stops"]):
            if t_["bdep"][kk] is None:
                continue
            nm = Wd.station_name(t_, kk)
            key = (nm, int(t_["bdep"][kk] // HM))
            onward.setdefault(key, set()).update(Wd.station_name(t_, q) for q in range(kk + 1, len(t_["stops"])))
    # the weekdays on which each train reached each station 15 or more minutes late
    late_index = {}
    for day in days:
        for tr in trains:
            r = W["records"][day][tr["id"]]
            for k in range(1, len(tr["stops"])):
                if r["arr"][k] - tr["barr"][k] >= 15 * HM:
                    late_index.setdefault((tr["id"], k), []).append(day)
    for day in days:
        rec = W["records"][day]
        for tr in trains:
            r = rec[tr["id"]]
            ons, offs = census[tr["id"]]
            n = len(tr["stops"])
            for k in range(1, n):
                late = (r["arr"][k] - tr["barr"][k]) / HM
                if late < 15 or offs[k] == 0 or late in (29.5, 59.5):
                    continue
                band = band_of(late)
                nclaim = rng.binomial(int(offs[k]), P.DR_TAKEUP)
                # origins in proportion to boarders upstream
                up = ons[:k].astype(float)
                if up.sum() == 0:
                    continue
                for _ in range(nclaim):
                    j = int(rng.choice(np.arange(k), p=up / up.sum()))
                    o_name = Wd.station_name(tr, j)
                    d_name = Wd.station_name(tr, k)
                    tk = tickets[int(rng.choice(4, p=tw))]
                    f1 = fare_single(abs(tr["stops"][k] - tr["stops"][j]))
                    # what the passenger claims: usually the band, sometimes a band lower or higher
                    u = rng.random()
                    bnames = [b[0] for b in P.DR_BANDS]
                    bi = bnames.index(band)
                    if u < 0.16 and bi > 0:
                        claimed = bnames[bi - 1]
                    elif u < 0.22 and bi < 3:
                        claimed = bnames[bi + 1]
                    else:
                        claimed = band
                    paid_band = bnames[min(bnames.index(claimed), bi)]
                    off_peak = rng.random() < 0.08      # first assessed on the off-peak fare for that journey
                    channel = "APP" if rng.random() < 0.46 else "WEB"
                    sub = dt.datetime.combine(day, dt.time(0)) + dt.timedelta(
                        minutes=int(r["arr"][k] / HM) + int(rng.integers(40, 60 * 24 * 12)))
                    paid_on = (sub + dt.timedelta(days=int(rng.integers(3, 15)))).date()
                    full = comp(tk, f1, paid_band)
                    amt = round(full * 0.72, 2) if off_peak else full
                    cr = ref()
                    c_o, c_d = o_name, d_name
                    if tk == "Anytime Return" and tr["dir"] == "out" and rng.random() < 0.8 and \
                            o_name not in onward.get((d_name, int(tr["bdep"][j] // HM)), set()):
                        c_o, c_d = d_name, o_name     # the return leg of a ticket bought at the outer end
                    jdate = day
                    if channel == "APP" and (c_o, c_d) == (o_name, d_name) and rng.random() < 0.14:
                        stated = sub.date()
                        if stated != day and late_index.get((tr["id"], k)) == [day]:
                            jdate = stated            # the app's journey date left at its default, the day of the claim
                    method = "CARD" if rng.random() < 0.63 else "VOUCHER"
                    claims.append({"claim_ref": cr, "channel": channel, "submitted": sub, "ticket": tk,
                                   "ticket_ref": "%08d" % int(rng.integers(10 ** 7, 10 ** 8)), "journey_date": jdate,
                                   "true_date": day, "origin": P.CRS[c_o], "destination": P.CRS[c_d],
                                   "booked_dep": tr["bdep"][j], "claimed": claimed, "decision": "APPROVED",
                                   "band_paid": paid_band, "paid_on": paid_on, "amount": amt, "method": method,
                                   "line": tr["line"], "true_band": band, "true_late": late,
                                   "central": "Ravelstoke Central" in (o_name, d_name)})
                    # an appeal is paid as a top-up under the same claim: an under-claim to the train's band, an
                    # off-peak assessment to the fare the passenger paid; an appeal still open at the pull has no row
                    top = None
                    if paid_band != band and bnames.index(paid_band) < bi and rng.random() < 0.34:
                        top = (band, round(comp(tk, f1, band) - amt, 2))
                    elif off_peak and rng.random() < 0.7:
                        top = (paid_band, round(full - amt, 2))
                    if top is not None:
                        t_sub = sub + dt.timedelta(days=int(rng.integers(9, 30)))
                        t_paid = max(paid_on, t_sub.date()) + dt.timedelta(days=int(rng.integers(7, 25)))
                        if t_paid <= P.DR_EXTRACT:
                            claims.append({**claims[-1], "submitted": t_sub, "band_paid": top[0], "amount": top[1],
                                           "paid_on": t_paid, "method": method, "appeal": True})
    # rejected claims: journeys whose train reached the destination 8 to 14 minutes late
    for day in days:
        rec = W["records"][day]
        for tr in trains:
            r = rec[tr["id"]]
            ons, offs = census[tr["id"]]
            for k in range(1, len(tr["stops"])):
                late = (r["arr"][k] - tr["barr"][k]) / HM
                if not (8 <= late < 15) or offs[k] == 0:
                    continue
                for _ in range(rng.binomial(int(offs[k]), 0.012)):
                    up = ons[:k].astype(float)
                    if up.sum() == 0:
                        continue
                    j = int(rng.choice(np.arange(k), p=up / up.sum()))
                    o_name, d_name = Wd.station_name(tr, j), Wd.station_name(tr, k)
                    sub = dt.datetime.combine(day, dt.time(0)) + dt.timedelta(
                        minutes=int(r["arr"][k] / HM) + int(rng.integers(40, 60 * 24 * 9)))
                    claims.append({"claim_ref": ref(), "channel": "APP" if rng.random() < 0.46 else "WEB",
                                   "submitted": sub, "ticket": tickets[int(rng.choice(4, p=tw))],
                                   "ticket_ref": "%08d" % int(rng.integers(10 ** 7, 10 ** 8)), "journey_date": day,
                                   "origin": P.CRS[o_name], "destination": P.CRS[d_name], "booked_dep": tr["bdep"][j],
                                   "claimed": "15 to 29", "decision": "REJECTED", "band_paid": "", "paid_on": None,
                                   "amount": 0.0, "method": "", "line": tr["line"], "true_band": None,
                                   "true_late": late, "central": "Ravelstoke Central" in (o_name, d_name)})
    # claims for journeys outside the weekday record (weekends and the first days of September), paid alike
    extra_days = [dt.date(2026, 9, 1), dt.date(2026, 9, 2), dt.date(2026, 9, 3), dt.date(2026, 9, 12),
                  dt.date(2026, 10, 3), dt.date(2026, 11, 14), dt.date(2026, 11, 29), dt.date(2026, 11, 30)]
    pool = [c for c in claims if c["decision"] == "APPROVED" and not c.get("appeal")]
    for dday in extra_days:
        for _ in range(int(rng.integers(14, 44))):
            c = dict(pool[int(rng.integers(len(pool)))])
            c["claim_ref"] = ref()
            c["journey_date"] = dday
            c["submitted"] = dt.datetime.combine(dday, dt.time(0)) + dt.timedelta(minutes=int(rng.integers(1500, 9000)))
            c["paid_on"] = (c["submitted"] + dt.timedelta(days=int(rng.integers(3, 15)))).date()
            c["ticket_ref"] = "%08d" % int(rng.integers(10 ** 7, 10 ** 8))
            c["outside"] = True
            claims.append(c)
    claims.sort(key=lambda c: (c["submitted"], c["claim_ref"]))
    # truth: every in-window, to-or-from-Central approved payment, by line and the train's band at the destination
    for ln in P.LINES:
        for b in P.ASK_BANDS:
            truth[(ln, b[0])] = 0.0
    for c in claims:
        if c["decision"] != "APPROVED" or c.get("outside") or not c["central"]:
            continue
        truth[(c["line"], ask_band(c["true_late"]))] += c["amount"]
    truth = {k: round(v, 2) for k, v in truth.items()}
    return claims, truth


if __name__ == "__main__":
    W = Wd.build_world()
    rows, gt = gate_readings(W)
    print(len(rows), gt)
    cl, dt_ = delay_repay(W)
    print(len(cl), dt_)
