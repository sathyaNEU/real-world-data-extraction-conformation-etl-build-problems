"""task156: the records the asks read and the call never does: the councils' payroll remittance advices with the
shared bureau's statements (dues), the organisers' diary export with the regional forums' sign-in sheets (organiser
hours), and two files the solution never uses (the councils' workforce returns, the 2024 member survey)."""
import datetime as dt
import functools

import numpy as np

import population as PO
import world as W

FY0, FY1 = dt.date(2025, 7, 1), dt.date(2026, 6, 30)
RATE = {"Full time": 27.40, "Part time": 20.60, "Casual": 13.80}     # per fortnight, 2025-26
# councils on the regional payroll platform from January 2026: its advices date each run by the pay day
PLATFORM = ["ARD", "DAR", "HAL", "OAK", "NOR", "VAL", "WES", "GLE", "BUR", "DEN", "ASH", "STA"]
PLATFORM_FROM = dt.date(2026, 1, 1)
RESENT = ("LIN", dt.date(2026, 3, 8))          # an advice the council's payroll sent twice
ORGANISERS = ["ORG01", "ORG02", "ORG03", "ORG04", "ORG05", "ORG06", "ORG07"]


def ppe_anchor(code):
    """Each council's pay period end: Sundays fortnightly from 13 July 2025 ('late') or 6 July 2025 ('early')."""
    late = code in PLATFORM or W.CODES.index(code) % 2 == 0
    return dt.date(2025, 6, 29) if late else dt.date(2025, 7, 6)


def ppes(code):
    a = ppe_anchor(code)
    out = []
    d = a
    while d <= dt.date(2026, 7, 12):
        out.append(d)
        d += dt.timedelta(days=14)
    return out


@functools.lru_cache(maxsize=None)
def remittances():
    """(council, true period end, members deducted, amount) for every run, July 2025 to July 2026."""
    P = PO.build()
    out = []
    for code in W.CODES:
        mem = [m for m in P.members if m["council"] == code and m["pay"] == "payroll"]
        for ppe in ppes(code):
            ded = [m for m in mem if PO.active(m, ppe)]
            amt = round(sum(RATE[m["emp"]] for m in ded), 2)
            out.append((code, ppe, len(ded), amt))
    return out


def remit_rows():
    rng = np.random.default_rng([W.SEED, 500])
    rows = []
    bureau = {}
    for code, ppe, n, amt in remittances():
        if code in W.BUREAU_CLIENTS:
            b = bureau.setdefault(ppe, [0, 0.0])
            b[0] += n
            b[1] += amt
            continue
        shown = ppe + dt.timedelta(days=4) if (code in PLATFORM and ppe >= PLATFORM_FROM) else ppe
        paid = ppe + dt.timedelta(days=int(rng.integers(5, 9)))
        rows.append([paid, W.NAME[code], shown, n, "%.2f" % amt])
        if (code, ppe) == RESENT:
            rows.append([paid + dt.timedelta(days=2), W.NAME[code], shown, n, "%.2f" % amt])
    for ppe, (n, amt) in sorted(bureau.items()):
        paid = ppe + dt.timedelta(days=6)
        rows.append([paid, W.BUREAU, ppe, n, "%.2f" % round(amt, 2)])
    rows.sort(key=lambda r: (r[0], r[1]))
    out = []
    seq = 41870
    seen = {}
    for r in rows:
        key = (r[1], r[2])
        if key in seen:          # the re-sent advice keeps its advice number
            out.append([seen[key]] + [r[0].isoformat(), r[1], r[2].isoformat(), r[3], r[4]])
            continue
        seq += int(rng.integers(1, 6))
        seen[key] = "RA%06d" % seq
        out.append([seen[key], r[0].isoformat(), r[1], r[2].isoformat(), r[3], r[4]])
    return out


REMIT_COLS = ["advice_no", "received", "employer", "period_end", "members_deducted", "amount"]


def bureau_lines():
    """The bureau's statement lines: (period end, client council, members, amount)."""
    return [(ppe, code, n, amt) for code, ppe, n, amt in remittances() if code in W.BUREAU_CLIENTS]


# ---- organiser diary ----

def _patches():
    """Each organiser's councils (a patch), every council in exactly one patch."""
    codes = list(W.CODES)
    return {o: codes[i::len(ORGANISERS)] for i, o in enumerate(ORGANISERS)}


@functools.lru_cache(maxsize=None)
def diary_raw():
    """Diary rows: dict(entry, uid, org, date, start, end, council, site, activity, updated_utc) and the forums."""
    P = PO.build()
    rng = np.random.default_rng([W.SEED, 600])
    patches = _patches()
    sites = {c: [s["code"] for s in P.site_by_c[c]] for c in W.CODES}
    rows = []
    forums = []
    d = FY0 - dt.timedelta(days=3)
    uid_n = [0]

    def uid():
        uid_n[0] += 1
        return "%08x-%04x" % (int(rng.integers(0, 2 ** 32)), uid_n[0])

    weekly = {}   # (org, council) -> uid of a weekly delegates' meeting series
    for o in ORGANISERS:
        for c in patches[o]:
            if rng.uniform() < 0.6:
                weekly[(o, c)] = (uid(), int(rng.integers(0, 5)), int(rng.integers(8, 15)))
    end = FY1 + dt.timedelta(days=3)
    while d <= end:
        wd = d.weekday()
        if wd < 5:
            for o in ORGANISERS:
                if rng.uniform() < 0.09:      # leave, training, office day
                    continue
                t = 8.5 + float(rng.choice([0, 0.25, 0.5]))
                for c in patches[o]:
                    w = weekly.get((o, c))
                    if w and w[1] == wd:
                        rows.append(dict(uid=w[0], org=o, date=d, start=w[2], end=w[2] + 1.0, council=c, site="",
                                         activity="Delegates meeting"))
                nvis = int(rng.integers(1, 4))
                for k in range(nvis):
                    c = patches[o][int(rng.integers(0, len(patches[o])))]
                    trav = float(rng.choice([0.5, 0.75, 1.0, 1.5]))
                    rows.append(dict(uid=uid(), org=o, date=d, start=t, end=t + trav, council="", site="",
                                     activity="Travel"))
                    t += trav
                    dur = float(rng.choice([1.0, 1.5, 2.0, 2.5, 3.0]))
                    kind = "Worksite visit" if rng.uniform() < 0.72 else ("Bargaining meeting" if rng.uniform() < 0.5
                                                                          else "Member meeting")
                    st = sites[c][int(rng.integers(0, len(sites[c])))] if kind != "Bargaining meeting" else ""
                    rows.append(dict(uid=uid(), org=o, date=d, start=t, end=t + dur, council=c, site=st,
                                     activity=kind))
                    # a colleague from another patch joins about one visit in nine on the same invitation
                    if kind != "Travel" and rng.uniform() < 0.11:
                        o2 = ORGANISERS[(ORGANISERS.index(o) + int(rng.integers(1, len(ORGANISERS)))) % len(ORGANISERS)]
                        rows.append(dict(uid=rows[-1]["uid"], org=o2, date=d, start=t, end=t + dur, council=c, site=st,
                                         activity=kind))
                    t += dur + float(rng.choice([0.25, 0.5, 0.75]))
                if rng.uniform() < 0.5:
                    rows.append(dict(uid=uid(), org=o, date=d, start=t, end=t + 1.0, council="", site="",
                                     activity="Administration"))
            # the regional delegates' forum: second Thursday of each month
            if wd == 3 and 8 <= d.day <= 14 and FY0 <= d <= FY1:
                u = uid()
                hosts = sorted(rng.choice(len(ORGANISERS), size=int(rng.integers(2, 4)), replace=False))
                for h in hosts:
                    rows.append(dict(uid=u, org=ORGANISERS[h], date=d, start=17.5, end=20.5, council="",
                                     site="", activity="Regional delegates forum"))
                forums.append((d, u))
        d += dt.timedelta(days=1)
    # rescheduled bookings: the calendar sync keeps the superseded row (same organiser, invitation and day)
    ghosts = []
    for r in rows:
        if r["activity"] in ("Travel", "Administration"):
            continue
        if rng.uniform() < 0.07:
            g = dict(r)
            shift = float(rng.choice([-1.0, -0.5, 0.5, 1.0]))
            g["start"] = r["start"] + shift
            g["end"] = g["start"] + max(0.5, (r["end"] - r["start"]) + float(rng.choice([-0.5, 0.0, 0.5])))
            g["ghost"] = True
            ghosts.append(g)
    allrows = rows + ghosts
    # updated stamps: a superseded row was last touched before its replacement
    base = {}
    for r in allrows:
        local = dt.datetime.combine(r["date"], dt.time(7, 0)) - dt.timedelta(days=int(rng.integers(1, 12)))
        r["updated"] = local
    for g in ghosts:
        pass
    keymap = {}
    for r in rows:
        keymap[(r["uid"], r["org"], r["date"])] = r
    for g in ghosts:
        live = keymap[(g["uid"], g["org"], g["date"])]
        g["updated"] = live["updated"] - dt.timedelta(hours=int(rng.integers(5, 60)))
    allrows.sort(key=lambda r: (r["date"], r["org"], r["start"], r.get("ghost", False)))
    return allrows, forums


def _council_hours(rows):
    P = PO.build()
    tot = {c: 0.0 for c in W.CODES}
    fh = {}
    for r in rows:
        if r.get("ghost") or r["activity"] in ("Travel", "Administration") or not (FY0 <= r["date"] <= FY1):
            continue
        if r["activity"] == "Regional delegates forum":
            fh[r["date"]] = fh.get(r["date"], 0.0) + r["end"] - r["start"]
        else:
            tot[r["council"]] += r["end"] - r["start"]
    by = {}
    for d, no, _ in signins():
        c = P.by_no[no]["council"]
        by.setdefault(d, {}).setdefault(c, 0)
        by[d][c] += 1
    for d, h in fh.items():
        n = sum(by[d].values())
        for c, k in by[d].items():
            tot[c] += h * k / n
    return tot


@functools.lru_cache(maxsize=None)
def diary():
    """The diary with each council's year kept clear of a half hour: a visit that lands a council's total within
    two minutes of a half hour ends five minutes later."""
    rows, forums = diary_raw()
    rows = [dict(r) for r in rows]
    ghosted = {(g["uid"], g["org"], g["date"]) for g in rows if g.get("ghost")}
    for _ in range(20):
        tot = _council_hours(rows)
        near = [c for c, v in sorted(tot.items()) if abs((v % 1) - 0.5) <= 0.04]
        if not near:
            break
        for c in near:
            for r in rows:
                if (r["council"] == c and r["activity"] == "Worksite visit" and not r.get("ghost")
                        and (r["uid"], r["org"], r["date"]) not in ghosted and FY0 <= r["date"] <= FY1):
                    r["end"] = r["end"] + 5.0 / 60
                    break
    return rows, forums


def hhmm(x):
    h = int(x)
    m = int(round((x - h) * 60))
    return "%02d:%02d" % (h, m)


def _utc(local):
    off = 11 if (local.date() >= dt.date(2025, 10, 5) and local.date() < dt.date(2026, 4, 5)) else 10
    return (local - dt.timedelta(hours=off)).strftime("%Y-%m-%dT%H:%M:%SZ")


def diary_rows():
    rows, _ = diary()
    out = []
    for i, r in enumerate(rows):
        out.append(["E%06d" % (200000 + i * 3), r["uid"], r["org"], r["date"].isoformat(), hhmm(r["start"]),
                    hhmm(r["end"]), W.NAME[r["council"]] if r["council"] else "", r["site"], r["activity"],
                    _utc(r["updated"])])
    return out


DIARY_COLS = ["entry_id", "invitation_uid", "organiser", "date", "starts", "ends", "council", "worksite", "activity",
              "last_updated_utc"]


@functools.lru_cache(maxsize=None)
def signins():
    """Delegates signing in at each forum: current delegates (term in force) drawn from every council."""
    P = PO.build()
    rng = np.random.default_rng([W.SEED, 700])
    _, forums = diary_raw()
    out = []
    for d, u in forums:
        term = W.term_of(d)
        pool = sorted({no for (t, s), nos in P.dsites.items() if t == term for no in nos
                       if PO.active(P.by_no[no], d)})
        k = int(rng.integers(22, 48))
        picks = rng.choice(len(pool), size=min(k, len(pool)), replace=False)
        for j, pi in enumerate(sorted(picks)):
            out.append((d, pool[pi], "%02d:%02d" % (17, int(rng.integers(5, 50)))))
    return out


SIGNIN_COLS = ["forum_date", "member_no", "signed_in"]


def signin_rows():
    return [[d.isoformat(), no, t] for d, no, t in signins()]


def workforce_rows():
    """The councils' 30 June 2026 workforce returns (headcount and FTE by employment type): unused by the solution."""
    P = PO.build()
    rng = np.random.default_rng([W.SEED, 800])
    out = []
    for code in W.CODES:
        mem = sum(1 for m in P.members if m["council"] == code and PO.active(m, FY1))
        density = float(rng.uniform(0.32, 0.58))
        hc = int(mem / density)
        ft = int(hc * float(rng.uniform(0.55, 0.68)))
        pt = int(hc * float(rng.uniform(0.2, 0.3)))
        cas = hc - ft - pt
        out.append([W.NAME[code], "2026-06-30", ft, pt, cas, hc, "%.1f" % (ft + 0.55 * pt + 0.18 * cas)])
    return out


WORKFORCE_COLS = ["council", "as_at", "full_time_headcount", "part_time_headcount", "casual_headcount",
                  "total_headcount", "total_fte"]
