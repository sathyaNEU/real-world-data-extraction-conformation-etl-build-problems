"""Prototype of task184 architecture 2: offences with occurrence windows, and the five slates."""
import datetime as dt
import numpy as np

SEED = 184
SLOT_H = 4
SLOTS = [(d, h) for d in range(7) for h in range(0, 24, SLOT_H)]        # 42 candidates
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
CAP = 8
SEASONS = [(dt.date(2025, 4, 1), dt.date(2025, 9, 30)), (dt.date(2026, 4, 1), dt.date(2026, 9, 30))]

# class: (per-season count, window kind, weekday weights Mon..Sun)
# window kinds: point, evening_park, commute_park, overnight, daytime_absence, lockup, multiday
CLASSES = {
    "Theft from a motor vehicle": (2600, "mixed_park",  [1.15, 1.10, 1.32, 1.20, 1.35, 1.25, 0.85]),
    "Theft of a pedal cycle":     (2100, "lockup",      [1.20, 1.20, 1.15, 1.20, 1.30, 0.95, 0.70]),
    "Criminal damage":            (3800, "closed_hours",[0.76, 0.76, 1.0, 1.281, 3.125, 4.95, 1.978]),
    "Burglary business":          (2660, "closed_hours",[1.281, 1.281, 1.281, 1.281, 1.786, 1.0, 0.396]),
    "Burglary residential":       (1350, "absence",     [1.20, 1.20, 1.15, 1.10, 1.20, 0.90, 0.80]),
    "Theft from the person":      (780,  "point_day",   [1.10, 1.05, 1.05, 1.15, 1.35, 1.45, 0.75]),
    "Assault without injury":     (1180, "point_night", [0.90, 0.80, 1.00, 1.30, 2.20, 2.70, 1.30]),
    "Public order":              (1460, "point_night", [0.80, 0.80, 1.00, 1.20, 2.30, 2.80, 1.30]),
    "Shoplifting":               (2240, "point_day",   [1.20, 1.10, 1.10, 1.20, 1.40, 1.50, 0.60]),
}

# the tasking contract covers the acquisitive classes whose occurrence time is recorded as a window
CONTRACTED = {"Theft from a motor vehicle", "Theft of a pedal cycle", "Criminal damage", "Burglary business",
              "Burglary residential"}


def rng(k):
    return np.random.default_rng([SEED, 2, k])


def window(kind, g, n):
    """Return (start_hour, length_hours) arrays, start measured from midnight of the window's first day."""
    if kind == "point_night":
        s = 20.0 + 9.0 * g.beta(2.0, 2.4, n)            # 20:00 to 05:00, the taxi rank clearing last
        return s, np.zeros(n)
    if kind == "point_day":
        market = g.random(n) < 0.34                     # the fish market trades from 04:00
        s = np.where(market, 4.0 + 3.5 * g.random(n), 9.0 + 11.0 * g.beta(2.0, 2.0, n))
        return s, np.zeros(n)
    if kind == "mixed_park":
        night = g.random(n) < 0.46
        s = np.where(night, 18.5 + 3.0 * g.random(n), 7.0 + 2.5 * g.random(n))
        ln = np.where(night, 2.5 + 5.0 * g.random(n), 6.5 + 4.5 * g.random(n))
        return s, ln
    if kind == "lockup":
        evening = g.random(n) < 0.40
        s = np.where(evening, 16.5 + 3.0 * g.random(n), 8.0 + 4.0 * g.random(n))
        return s, np.where(evening, 2.0 + 7.0 * g.random(n), 2.0 + 6.0 * g.random(n))
    if kind == "closed_hours":
        s = 19.5 + 2.5 * g.random(n)                    # closed or last seen, 19:30 to 22:00
        end = 30.5 + 4.0 * g.random(n)                  # opened or found, 06:30 to 10:30 next day
        return s, end - s
    if kind == "absence":
        long_trip = g.random(n) < 0.18
        s = np.where(long_trip, 7.0 + 3.0 * g.random(n), 7.5 + 1.5 * g.random(n))
        ln = np.where(long_trip, 24.0 + 48.0 * g.random(n), 8.0 + 3.0 * g.random(n))
        return s, ln
    raise ValueError(kind)


def make():
    rows = []
    for k, (cls, (per_season, kind, dow_w)) in enumerate(CLASSES.items()):
        g = rng(k + 1)
        w = np.array(dow_w, float)
        for si, (d0, d1) in enumerate(SEASONS):
            n = int(round(per_season * (1.0 + 0.03 * (si * 2 - 1))))
            ndays = (d1 - d0).days + 1
            # pick the window's first day with the class's weekday weights
            dows = np.array([(d0 + dt.timedelta(days=int(i))).weekday() for i in range(ndays)])
            p = w[dows] / w[dows].sum()
            di = g.choice(ndays, size=n, p=p)
            s, ln = window(kind, g, n)
            for j in range(n):
                start = dt.datetime.combine(d0 + dt.timedelta(days=int(di[j])), dt.time()) + \
                        dt.timedelta(hours=float(s[j]))
                end = start + dt.timedelta(hours=float(ln[j]))
                true_at = start + dt.timedelta(hours=float(ln[j]) * float(g.random()))
                rows.append({"cls": cls, "season": si, "from": start, "to": end, "true": true_at})
    return rows


def contracted(rows):
    return [r for r in rows if r["cls"] in CONTRACTED]


def slot_of(ts):
    return (ts.weekday(), (ts.hour // SLOT_H) * SLOT_H)


def point_slate(rows, key):
    w = {s: 0.0 for s in SLOTS}
    for r in rows:
        w[slot_of(r[key])] += 1.0
    return w


def mid_slate(rows):
    w = {s: 0.0 for s in SLOTS}
    for r in rows:
        w[slot_of(r["from"] + (r["to"] - r["from"]) / 2)] += 1.0
    return w


def precise_slate(rows, max_h=1.0):
    w = {s: 0.0 for s in SLOTS}
    for r in rows:
        if (r["to"] - r["from"]).total_seconds() / 3600.0 <= max_h:
            w[slot_of(r["from"])] += 1.0
    return w


def aoristic(rows, step_min=15):
    w = {s: 0.0 for s in SLOTS}
    step = dt.timedelta(minutes=step_min)
    for r in rows:
        a, b = r["from"], r["to"]
        if b <= a:
            w[slot_of(a)] += 1.0
            continue
        n = max(1, int(round((b - a).total_seconds() / step.total_seconds())))
        share = 1.0 / n
        t = a
        for _ in range(n):
            w[slot_of(t + step / 2)] += share
            t += step
    return w


def top(w, cap=CAP):
    return [s for s in sorted(w, key=lambda s: -w[s])[:cap]]


def cover(w_basis, slate):
    return sum(w_basis[s] for s in slate)


def act_weighted_from(rows, allrows, step_min=15):
    """The aoristic refinement: spread each window across its steps in proportion to the quarter's own
    distribution of precisely timed offences across the clock hour, rather than uniformly."""
    prof = np.ones(24)
    for r in allrows:
        if r["to"] <= r["from"]:                      # the precisely timed classes, none of them contracted
            prof[r["from"].hour] += 1.0
    prof = prof / prof.mean()
    import datetime as _dt
    w = {s: 0.0 for s in SLOTS}
    step = _dt.timedelta(minutes=step_min)
    for r in rows:
        a, b = r["from"], r["to"]
        if b <= a:
            w[slot_of(a)] += 1.0
            continue
        n = max(1, int(round((b - a).total_seconds() / step.total_seconds())))
        ts = [a + step * k + step / 2 for k in range(n)]
        ws = np.array([prof[t.hour] for t in ts])
        ws = ws / ws.sum()
        for t, x in zip(ts, ws):
            w[slot_of(t)] += float(x)
    return w


if __name__ == "__main__":
    allrows = make()
    rows = contracted(allrows)
    print("offences", len(allrows), "contracted", len(rows), "per season", len(rows) // 2)
    bases = {"from": point_slate(rows, "from"), "to": point_slate(rows, "to"), "mid": mid_slate(rows),
             "precise": precise_slate(rows), "aoristic": aoristic(rows),
             "aoristic_1h": aoristic(rows, 60), "activity": act_weighted_from(rows, allrows),
             "truth": point_slate(rows, "true")}
    gold = bases["aoristic"]
    gslate = top(gold)
    tslate = top(bases["truth"])
    print("\ngolden slate (aoristic):")
    for s in gslate:
        print("   %-9s %02d:00-%02d:00  %7.1f" % (DAYS[s[0]], s[1], s[1] + SLOT_H, gold[s] / 2))
    print("truth slate equals golden slate:", gslate == tslate)
    print("\nslate members shared with the golden, and coverage on the golden basis:")
    for name, b in bases.items():
        sl = top(b)
        print("  %-9s shared %d/%d  coverage %8.1f  (%.3f of the golden's)" % (
            name, len(set(sl) & set(gslate)), CAP, cover(gold, sl) / 2, cover(gold, sl) / cover(gold, gslate)))
