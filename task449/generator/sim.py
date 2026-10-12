"""Simulate the desk's year: every matter the case system opened from go-live to the pull (channel, code, account,
how the account was found), each matter's open and closed spells, the social care desk's post records, Meridel's
affected-payment file and the portfolio, and the time Fenwright analysts and both agencies worked. The eight-week
window is built to exact category totals; everything else is drawn."""
import datetime as dt
import math

import numpy as np

import world as W

ET = dt.timezone(dt.timedelta(hours=-4))       # Eastern daylight time
EST = dt.timezone(dt.timedelta(hours=-5))
HOLIDAYS = {dt.date(2025, 11, 27), dt.date(2025, 12, 25), dt.date(2026, 1, 1), dt.date(2026, 5, 25),
            dt.date(2026, 7, 3), dt.date(2026, 9, 7)}
WEEKDAY_W = {
    "Phone": [0.200, 0.190, 0.180, 0.170, 0.150, 0.110, 0.0],
    "Digital": [0.170, 0.160, 0.150, 0.150, 0.140, 0.110, 0.120],
    "CFPB": [0.220, 0.200, 0.195, 0.195, 0.190, 0.0, 0.0],
    "State": [0.220, 0.200, 0.195, 0.195, 0.190, 0.0, 0.0],
    "Executive": [0.220, 0.200, 0.195, 0.195, 0.190, 0.0, 0.0],
    "Social": [0.150, 0.145, 0.145, 0.140, 0.140, 0.140, 0.140],
}
CUTOFF = dt.datetime.combine(W.LAST_DAY, dt.time(23, 59, 59))


def eastern_offset(d):
    """Eastern time: daylight from 8 March to 1 November 2026 (and to 2 November 2025)."""
    if dt.date(2025, 3, 9) <= d < dt.date(2025, 11, 2) or dt.date(2026, 3, 8) <= d < dt.date(2026, 11, 1):
        return dt.timedelta(hours=-4)
    return dt.timedelta(hours=-5)


def mondays():
    m = W.GO_LIVE - dt.timedelta(days=W.GO_LIVE.weekday())
    out = []
    while m <= W.LAST_DAY:
        out.append(m)
        m += dt.timedelta(days=7)
    return out


def in_win(d):
    return W.WIN[0] <= d <= W.WIN[1]


def day_weights(ch, monday):
    days = [monday + dt.timedelta(days=i) for i in range(7)]
    w = np.array(WEEKDAY_W[ch], dtype=float)
    for i, d in enumerate(days):
        if d < W.GO_LIVE or d > W.LAST_DAY or (ch != "Social" and ch != "Digital" and d in HOLIDAYS):
            w[i] = 0.0
    return days, w


class Accounts:
    """Account references: BCF and twelve digits. The affected set is Meridel's posted-late accounts; the
    returned-only accounts appear in Meridel's file but posted nothing late; every other reference is drawn fresh."""

    def __init__(self, rng):
        self.rng = rng
        n = W.AFFECTED_ACCOUNTS + W.RETURNED_ONLY
        nums = set()
        while len(nums) < n:
            nums.update(int(x) for x in rng.integers(10 ** 9, 10 ** 12 - 1, n - len(nums) + 50))
        nums = sorted(nums)[:n]
        order = rng.permutation(len(nums))
        nums = [nums[i] for i in order]
        self.affected = ["BCF%012d" % x for x in nums[:W.AFFECTED_ACCOUNTS]]
        self.returned_only = ["BCF%012d" % x for x in nums[W.AFFECTED_ACCOUNTS:]]
        self.used = set(nums)

    def fresh(self):
        while True:
            x = int(self.rng.integers(10 ** 9, 10 ** 12 - 1))
            if x not in self.used:
                self.used.add(x)
                return "BCF%012d" % x

    def some_affected(self):
        return self.affected[int(self.rng.integers(0, len(self.affected)))]


def draw_code(rng, mix):
    keys = list(mix)
    p = np.array([mix[k] for k in keys])
    return keys[int(rng.choice(len(keys), p=p / p.sum()))]


def draw_k(rng):
    """A display-name-and-city search's result count outside the window: one result a quarter of the time."""
    u = rng.random()
    if u < 0.25:
        return 1
    acc = 0.25
    for (lo, hi), share in W.K_BANDS:
        acc += share
        if u < acc:
            return int(rng.integers(lo, hi + 1))
    return 60


def open_time(rng, ch, day):
    """Time of day the case system opened the matter, Eastern local."""
    if ch == "Phone":
        lo, hi = (8.0, 21.0) if day.weekday() < 5 else (9.0, 17.0)
        h = rng.triangular(lo, 13.0, hi)
    elif ch == "Digital":
        h = rng.choice([rng.uniform(0, 7), rng.triangular(7, 13, 24)], p=[0.08, 0.92])
    elif ch == "Social":
        h = rng.triangular(7.0, 15.0, 23.0)
    else:
        h = rng.uniform(8.5, 17.0)
    sec = int(h * 3600)
    sec = min(max(sec, 0), 86399)
    return dt.datetime.combine(day, dt.time(sec // 3600, (sec % 3600) // 60, sec % 60))


def spread_exact(rng, total, weights):
    """Spread an exact total over slots in proportion to weights (multinomial, seeded)."""
    w = np.asarray(weights, dtype=float)
    if total == 0 or w.sum() == 0:
        return np.zeros(len(w), dtype=int)
    return rng.multinomial(total, w / w.sum())


def incident_week(monday, ch):
    base = W.INCIDENT_PHONE.get(monday, 0.0)
    if ch == "CFPB":
        base = W.INCIDENT_PHONE.get(monday - dt.timedelta(days=7 * W.CFPB_LAG_WEEKS), 0.0)
    if monday == dt.date(2026, 5, 4):                      # the failure started on Friday 8 May
        base = base if ch != "CFPB" else 0.0
    return base * W.INCIDENT_SCALE[ch]


def week_plan(rng, monday):
    """Expected matters this week by (channel, kind) outside the window."""
    season = W.SEASON[monday.month]
    plan = {}
    for ch, (other, routine) in W.BASE.items():
        plan[(ch, "other")] = other * season
        plan[(ch, "routine")] = routine * season
        inc = incident_week(monday, ch)
        if ch == "Social":
            inc = inc if monday >= W.SOCIAL_PRACTICE - dt.timedelta(days=7) else inc * 0.25
        plan[(ch, "aff")] = inc
    if monday >= W.SOCIAL_PRACTICE - dt.timedelta(days=6):
        inc_nc = W.INCIDENT_PHONE.get(monday, 0.0) * W.NAME_CITY_SCALE
        plan[("NameCity", "aff")] = inc_nc
        plan[("NameCity", "routine")] = W.NAME_CITY_ROUTINE + W.SURGE_NAME_CITY_ROUTINE * inc_nc
        plan[("NameCity", "other")] = W.NAME_CITY_OTHER * season
        plan[("Social", "other")] = plan[("Social", "other")] * 1.6   # verified posters, more of them once posts open matters
    return plan


def simulate():
    rng = np.random.default_rng(W.SEED)
    acc = Accounts(rng)
    b = W.AFFECTED_ACCOUNTS / W.PORTFOLIO_OPEN[dt.date(2026, 4, 30)]
    rows = []            # one dict per matter, before numbering

    def add(ch, kind, opened, affected, basis="VERIFIED", k=None, right=None, other_aff=None):
        four = kind in ("aff", "routine", "four")
        if four:
            code = draw_code(rng, W.FOUR_MIX_INCIDENT if affected else W.FOUR_MIX_ROUTINE)
        else:
            code = draw_code(rng, W.OTHER_MIX)
        true_acc = acc.some_affected() if affected else acc.fresh()
        if basis == "VERIFIED":
            attached = true_acc
        elif right:
            attached = true_acc
        else:
            attached = acc.some_affected() if other_aff else acc.fresh()
        rows.append(dict(channel="Social" if ch == "NameCity" else ch, kind=kind, opened=opened, code=code,
                         affected=bool(affected), basis=basis, k=k, right=right, true_acc=true_acc, account=attached))

    # ---------------------------------------------------------------------------------------------------- weeks
    for monday in mondays():
        days = [monday + dt.timedelta(days=i) for i in range(7)]
        if in_win(monday):
            continue
        plan = week_plan(rng, monday)
        for (ch, kind), mu in plan.items():
            src = "Social" if ch == "NameCity" else ch
            dd, w = day_weights(src, monday)
            if w.sum() == 0 or mu <= 0:
                continue
            n = int(rng.poisson(mu * w.sum() / sum(WEEKDAY_W[src])))
            per_day = spread_exact(rng, n, w)
            for d, m in zip(dd, per_day):
                for _ in range(int(m)):
                    if d < W.FAILURE[0] and kind == "aff":
                        continue
                    t = open_time(rng, src, d)
                    if ch == "NameCity":
                        if d < W.SOCIAL_PRACTICE:
                            continue
                        if kind == "other":
                            k = draw_k(rng)
                            right = rng.random() < 1.0 / k
                            add("NameCity", "other", t, False, "NAME_CITY", k, right, rng.random() < b)
                        else:
                            aff = kind == "aff"
                            k = draw_k(rng)
                            right = rng.random() < 1.0 / k
                            add("NameCity", "four", t, aff, "NAME_CITY", k, right, rng.random() < b)
                    else:
                        add(ch, kind, t, kind == "aff")

    # --------------------------------------------------------------------------------- the window, built exactly
    win_days = [W.WIN[0] + dt.timedelta(days=i) for i in range(56)]
    win_mondays = [W.WIN[0] + dt.timedelta(days=7 * i) for i in range(8)]

    def profile(ch, kind):
        """Slot weights over the 56 days: the weekday pattern times the week's level for the category."""
        src = "Social" if ch == "NameCity" else ch
        out = []
        for monday in win_mondays:
            dd, w = day_weights(src, monday)
            if kind in ("aff",) or (ch == "NameCity" and kind == "four"):
                lvl = W.INCIDENT_PHONE[monday] / 120.0
                lvl = 0.75 * lvl + 0.25 if ch == "NameCity" else lvl
            else:
                lvl = W.SEASON[monday.month] * (1.0 + 0.04 * math.sin(monday.toordinal() / 3.0))
            out.extend(list(w * lvl))
        return np.array(out)

    nc_four = None
    for (ch, kind), total in W.WIN_TOTALS.items():
        counts = spread_exact(rng, total, profile(ch, kind))
        stamps = []
        for d, m in zip(win_days, counts):
            src = "Social" if ch == "NameCity" else ch
            stamps.extend(open_time(rng, src, d) for _ in range(int(m)))
        if ch == "NameCity" and kind == "four":
            nc_four = stamps
            continue
        if ch == "NameCity":
            for t in stamps:
                k = draw_k(rng)
                add("NameCity", "other", t, False, "NAME_CITY", k, rng.random() < 1.0 / k, rng.random() < b)
            continue
        if ch == "Social":
            for t in stamps:
                add("Social", kind, t, kind == "aff")
            continue
        for t in stamps:
            add(ch, kind, t, kind == "aff")

    # the window's name-and-city four-code matters: k by band, the failure's share exact within each band and the
    # same mix of k among the affected and the unaffected; right attachments in proportion to 1/k in each group,
    # wrong ones attached to another cardholder at the portfolio's affected rate
    n_all = len(nc_four)
    n1, a1 = W.WIN_K1
    rest = n_all - n1
    shares = [s_ for _, s_ in W.K_BANDS]
    alloc = [int(round(rest * s_ / sum(shares))) for s_ in shares]
    alloc[-1] += rest - sum(alloc)
    bands = [((1, 1), n1, a1)] + [(band, c, int(round(W.T_NAMECITY * c))) for (band, _), c in zip(W.K_BANDS, alloc)]
    order = [int(x) for x in rng.permutation(n_all)]
    pos = 0
    for (lo, hi), cnt, n_aff in bands:
        idx = order[pos:pos + cnt]
        pos += cnt
        ks = sorted(lo + (j % (hi - lo + 1)) for j in range(cnt))
        step = cnt / float(n_aff)
        aff_pos = {min(cnt - 1, int(j * step)) for j in range(n_aff)}
        j = 0
        while len(aff_pos) < n_aff:
            aff_pos.add(j)
            j += 1
        aff = [i in aff_pos for i in range(cnt)]
        perm = [int(x) for x in rng.permutation(cnt)]
        ks = [ks[p_] for p_ in perm]
        aff = [aff[p_] for p_ in perm]
        right = [False] * cnt
        for grp in (True, False):
            members = [i for i in range(cnt) if aff[i] == grp]
            if not members:
                continue
            want = min(len(members), int(round(sum(1.0 / ks[i] for i in members))))
            pw = np.array([1.0 / ks[i] for i in members])
            for q in rng.choice(len(members), size=want, replace=False, p=pw / pw.sum()):
                right[members[int(q)]] = True
        wrong = [i for i in range(cnt) if not right[i]]
        other_aff = set()
        if wrong:
            other_aff = {wrong[int(q)] for q in rng.choice(len(wrong), size=int(round(b * len(wrong))), replace=False)}
        for j2, i in enumerate(idx):
            add("NameCity", "four", nc_four[i], aff[j2], "NAME_CITY", int(ks[j2]), right[j2], j2 in other_aff)

    # ------------------------------------------------------------------------------------------------- numbering
    rows.sort(key=lambda r: (r["opened"], r["channel"], r["account"]))
    for i, r in enumerate(rows):
        r["matter_no"] = "M%07d" % (2500001 + i)
        r["product"] = W.PRODUCTS[int(rng.choice(len(W.PRODUCTS), p=np.array([p for _, p in W.PRODUCTS]) /
                                                 sum(p for _, p in W.PRODUCTS)))][0]
    lifecycle(rng, rows)
    tune_month_ends(rng, rows)
    social = social_records(rng, rows)
    payments = meridel_file(rng, acc)
    time_rows, marlowby, treadwell = timesheets(rng)
    return dict(rows=rows, acc=acc, b=b, social=social, payments=payments, time=time_rows, marlowby=marlowby,
                treadwell=treadwell)


def surge_multiplier(rows):
    """Handling slows with the week's arrivals: one at 900 a week, up to 3.4."""
    per_week = {}
    for r in rows:
        m = r["opened"].date() - dt.timedelta(days=r["opened"].weekday())
        per_week[m] = per_week.get(m, 0) + 1
    return {m: min(3.4, max(1.0, 1.0 + 0.0011 * (n - 900))) for m, n in per_week.items()}


def work_time(rng, t):
    """Move a time into working hours (08:00 to 20:00, Monday to Saturday)."""
    while True:
        if t.weekday() == 6 or t.date() in HOLIDAYS:
            t = dt.datetime.combine(t.date() + dt.timedelta(days=1), dt.time(8, 0)) + dt.timedelta(
                minutes=int(rng.integers(5, 240)))
            continue
        if t.hour < 8:
            t = dt.datetime.combine(t.date(), dt.time(8, 0)) + dt.timedelta(minutes=int(rng.integers(5, 180)))
            continue
        if t.hour >= 20:
            t = dt.datetime.combine(t.date() + dt.timedelta(days=1), dt.time(8, 0)) + dt.timedelta(
                minutes=int(rng.integers(5, 240)))
            continue
        return t


def lifecycle(rng, rows):
    """Each matter's spells: opened, closed, perhaps reopened and closed again; a few merged as duplicates."""
    mult = surge_multiplier(rows)
    for r in rows:
        m = r["opened"].date() - dt.timedelta(days=r["opened"].weekday())
        ev = [(r["opened"], "OPENED")]
        if rng.random() < W.MERGED:
            t = work_time(rng, r["opened"] + dt.timedelta(hours=float(rng.uniform(4, 60))))
            if t <= CUTOFF:
                ev.append((t, "MERGED"))
            r["events"] = ev
            continue
        med = W.HANDLE_DAYS[r["channel"]] * mult.get(m, 1.0)
        t = r["opened"] + dt.timedelta(days=float(rng.lognormal(math.log(med), 0.75)))
        t = work_time(rng, t)
        rounds = 0
        while t <= CUTOFF:
            ev.append((t, "CLOSED"))
            p = W.REOPEN if rounds == 0 else W.REOPEN_TWICE
            if rng.random() >= p:
                break
            g = float(np.clip(rng.lognormal(math.log(11.0), 0.7), 1.0, 75.0))
            t2 = t + dt.timedelta(days=g, minutes=int(rng.integers(0, 600)))
            if t2 > CUTOFF:
                break
            ev.append((t2, "REOPENED"))
            rounds += 1
            t = work_time(rng, t2 + dt.timedelta(days=float(rng.lognormal(math.log(W.HANDLE_DAYS[r["channel"]] * 0.8),
                                                                           0.7))))
        r["events"] = ev


PLATFORMS = [("X", 0.55), ("Facebook", 0.30), ("Instagram", 0.15)]
COMMON_LAST = W.LAST[:70]
RARE_LAST = W.LAST[-60:]


def display_name(rng, k):
    first = W.FIRST[int(rng.integers(0, len(W.FIRST)))]
    if k >= 11:
        return "%s %s." % (first, W.LAST[int(rng.integers(0, len(W.LAST)))][0])
    if k >= 4:
        return "%s %s" % (first, COMMON_LAST[int(rng.integers(0, len(COMMON_LAST)))])
    if k >= 2:
        return "%s %s" % (first, W.LAST[int(rng.integers(0, len(W.LAST)))])
    if rng.random() < 0.35:
        return "%s %s. %s" % (first, "ABCDEFGHJKLMNPRSTW"[int(rng.integers(0, 18))],
                              RARE_LAST[int(rng.integers(0, len(RARE_LAST)))])
    return "%s %s" % (first, RARE_LAST[int(rng.integers(0, len(RARE_LAST)))])


def city_for(rng, k):
    cities = W.CITIES if k < 11 else [c for c in W.CITIES if c[2] >= 0.05]
    w = np.array([c[2] for c in cities])
    c = cities[int(rng.choice(len(cities), p=w / w.sum()))]
    return c[0], c[1]


def to_utc(t):
    return (t - eastern_offset(t.date())).replace(tzinfo=None)


def social_records(rng, rows):
    """One record per complaint post the social care desk opened a matter for."""
    out = []
    plat_w = np.array([p for _, p in PLATFORMS])
    for r in rows:
        if r["channel"] != "Social":
            continue
        k = r["k"] if r["k"] is not None else draw_k(rng)
        plat = PLATFORMS[int(rng.choice(len(PLATFORMS), p=plat_w / plat_w.sum()))][0]
        lag = dt.timedelta(minutes=int(rng.integers(2, 360)))
        posted = r["opened"] - lag
        if plat == "X":
            pid = "%d" % int(rng.integers(1_800_000_000_000_000_000, 1_999_999_999_999_999_999))
        elif plat == "Facebook":
            pid = "fb_%d_%d" % (int(rng.integers(10 ** 14, 10 ** 15)), int(rng.integers(10 ** 15, 10 ** 16)))
        else:
            pid = "ig_%d" % int(rng.integers(10 ** 17, 10 ** 18))
        name = display_name(rng, k)
        city, state = city_for(rng, k)
        handle = "@" + "".join(ch for ch in name.lower() if ch.isalpha())[:11] + "%d" % int(rng.integers(1, 9999))
        verified = r["basis"] == "VERIFIED"
        out.append(dict(post_id=pid, platform=plat, created_at=to_utc(posted).strftime("%Y-%m-%dT%H:%M:%SZ"),
                        handle=handle, display_name=name, city=city, state=state,
                        search=dict(name=name, city="%s, %s" % (city, state), results_returned=int(k)),
                        account=dict(basis=r["basis"], ref=r["account"]),
                        dm=dict(requested=bool(verified or rng.random() < 0.83), verified=verified),
                        matter_no=r["matter_no"], agent="SC-%02d" % int(rng.integers(1, 23))))
        r["source_ref"] = pid
        r["k"] = k
    return out


def business_days_after(d, n):
    out = d
    while n > 0:
        out += dt.timedelta(days=1)
        if out.weekday() < 5 and out not in HOLIDAYS:
            n -= 1
    return out


def meridel_file(rng, acc):
    """Meridel's file of the payments it received on 8 to 10 May 2026 that did not post on time."""
    rows = []
    seq = [0]

    def ref(day):
        seq[0] += 1
        return "MPS%s%06d" % (day.strftime("%y%m%d"), seq[0] * 7 % 1000003)

    days = [dt.date(2026, 5, 8), dt.date(2026, 5, 9), dt.date(2026, 5, 10)]
    dayp = np.array([0.55, 0.25, 0.20])
    for a in acc.affected:
        npay = 2 if rng.random() < W.TWO_PAYMENTS else 1
        for _ in range(npay):
            d = days[int(rng.choice(3, p=dayp))]
            due = business_days_after(d if d.weekday() < 5 else dt.date(2026, 5, 8), 1)
            amt = round(float(np.clip(rng.lognormal(math.log(165), 0.75), 25, 4000)), 2)
            if rng.random() < 0.012:
                r0 = ref(d)
                rows.append(dict(payment_ref=r0, account=a, received=d, due=due, posted=None, late=None, amount=amt,
                                 status="RETURNED", return_code="R01", original_ref=""))
                posted = business_days_after(due, int(rng.integers(5, 9)))
                rows.append(dict(payment_ref=ref(d), account=a, received=d, due=due, posted=posted,
                                 late=None, amount=amt, status="REPRESENTED", return_code="", original_ref=r0))
                continue
            posted = business_days_after(due, int(rng.choice([2, 3, 4, 5], p=[0.30, 0.38, 0.22, 0.10])))
            rows.append(dict(payment_ref=ref(d), account=a, received=d, due=due, posted=posted, late=None,
                             amount=amt, status="POSTED_LATE", return_code="", original_ref=""))
    for a in acc.returned_only:
        d = days[int(rng.choice(3, p=dayp))]
        due = business_days_after(d if d.weekday() < 5 else dt.date(2026, 5, 8), 1)
        amt = round(float(np.clip(rng.lognormal(math.log(140), 0.7), 25, 3000)), 2)
        rows.append(dict(payment_ref=ref(d), account=a, received=d, due=due, posted=None, late=None, amount=amt,
                         status="RETURNED", return_code=["R01", "R01", "R01", "R02", "R03", "R16"][int(rng.integers(0, 6))],
                         original_ref=""))
    for r in rows:
        if r["posted"] is not None:
            n, d = 0, r["due"]
            while d < r["posted"]:
                d += dt.timedelta(days=1)
                if d.weekday() < 5 and d not in HOLIDAYS:
                    n += 1
            r["late"] = n
    order = rng.permutation(len(rows))
    return [rows[int(i)] for i in order]


def hhmm(minutes):
    return minutes // 60, minutes % 60


def base_time(rng):
    """Fenwright's time on the Bellcroft site (dedicated analysts and five floaters who also work the Wrexley
    program), Marlowby Staffing's surge temps (decimal hours) and Treadwell & Oake's evening associates (hours and
    minutes after a point), 1 January to 30 September 2026."""
    days = [dt.date(2026, 1, 1) + dt.timedelta(days=i) for i in range((dt.date(2026, 9, 30) - dt.date(2026, 1, 1)).days + 1)]
    shifts = {"early": ((7, 0), (11, 0), (11, 30), (15, 30)), "day": ((8, 30), (12, 30), (13, 0), (17, 0)),
              "late": ((12, 30), (16, 30), (17, 0), (21, 0))}
    emps = [("FW%05d" % (20100 + 37 * i), "BCF", ["early", "day", "late"][i % 3], i % 5 == 4)
            for i in range(W.TEAM_2026)]
    emps += [("FW%05d" % (31300 + 53 * i), "CLW", "day", False) for i in range(5)]
    time_rows = []
    fmt = lambda h, m: "%02d:%02d" % (h, m)
    workday = {}
    for eid, prog, shift, sat in emps:
        for d in days:
            wd = d.weekday()
            works = (wd < 5) if not sat else (1 <= wd <= 5)
            if not works:
                continue
            if d in HOLIDAYS:
                time_rows.append(dict(emp=eid, date=d, start="", end="", code="HOL", program="", hours=8.0))
                continue
            if rng.random() < 0.055:
                time_rows.append(dict(emp=eid, date=d, start="", end="", code="PTO", program="", hours=8.0))
                continue
            a, b_, c, e = shifts[shift]
            p = "BCF-CMP" if prog == "BCF" else "WXE-CS"
            time_rows.append(dict(emp=eid, date=d, start=fmt(*a), end=fmt(*b_), code="REG", program=p, hours=4.0))
            time_rows.append(dict(emp=eid, date=d, start=fmt(*c), end=fmt(*e), code="REG", program=p, hours=4.0))
            workday.setdefault((prog, d.month), []).append((eid, d, e))
    # overtime: quarter-hour segments after the shift, to each month's total (the Bellcroft totals are set after the
    # agencies' hours are known, so each month's flex hours sit inside their rounding bin)
    targets = [(("BCF", m), v) for m, v in W.OT_BCF.items()] + [(("CLW", m), v) for m, v in W.OT_OTHER.items()]
    return_later = (shifts, emps, workday, time_rows, fmt, targets)
    return time_rows, return_later


def overtime(rng, state, agency_hours):
    shifts, emps, workday, time_rows, fmt, targets = state
    ends_at = {}
    for (prog, month), target in targets:
        if prog == "BCF":
            total = target + agency_hours[month]
            want = 10 * math.floor(total / 10.0) + 1.25 + 0.25 * (month % 3)
            target = want - agency_hours[month]
        pool = workday.get((prog, month), [])
        got = 0.0
        while got < target - 0.01:
            eid, d, (eh, em) = pool[int(rng.integers(0, len(pool)))]
            q = int(min(rng.choice([3, 4, 6, 8, 9, 10, 12]), round((target - got) * 4)))
            if q <= 0:
                break
            start = ends_at.get((eid, d), eh * 60 + em)
            end = start + 15 * q
            if end > 23 * 60 + 45:
                continue
            ends_at[(eid, d)] = end
            time_rows.append(dict(emp=eid, date=d, start=fmt(*hhmm(start)), end=fmt(*hhmm(end)), code="OT",
                                  program="BCF-CMP" if prog == "BCF" else "WXE-CS", hours=q / 4.0))
            got += q / 4.0
    time_rows.sort(key=lambda r: (r["date"], r["emp"], r["start"]))
    return time_rows


def agencies(rng, days, fmt):
    # Marlowby Staffing: surge temps, decimal hours, weekly exports
    marlowby = []
    temps = ["MS-%04d" % (4100 + 13 * i) for i in range(16)]
    for d in days:
        if not (W.MARLOWBY[0] <= d <= W.MARLOWBY[1]) or d.weekday() == 6 or d in HOLIDAYS:
            continue
        heads = W.MARLOWBY_HEADS[d.month]
        on = temps[:heads]
        for t in on:
            if rng.random() < (0.12 if d.weekday() < 5 else 0.55):
                continue
            if d.weekday() == 5:
                tin, tout, brk = (9, 0), (13, 30), 0
            else:
                tin, tout, brk = [((8, 0), (16, 30), 30), ((12, 0), (20, 30), 30), ((9, 0), (17, 45), 45)][
                    int(rng.integers(0, 3))]
            mins = (tout[0] * 60 + tout[1]) - (tin[0] * 60 + tin[1]) - brk
            we = d + dt.timedelta(days=(5 - d.weekday()) % 7)
            marlowby.append(dict(worker=t, date=d, tin=fmt(*tin), tout=fmt(*tout), brk=brk, hours=round(mins / 60.0, 2),
                                 week_ending=we, export="MSX-%s" % (we + dt.timedelta(days=7)).strftime("%Y%m%d")))
    resent = [dict(r) for r in marlowby if r["week_ending"] == W.MARLOWBY_RESENT_WEEK]
    marlowby.extend(resent)
    marlowby.sort(key=lambda r: (r["export"], r["date"], r["worker"]))
    # Treadwell & Oake: evening associates, hours and minutes after a point
    treadwell = []
    assoc = ["TO-%03d" % (211 + 7 * i) for i in range(8)]
    starts = [(15, 0), (15, 30), (16, 0), (16, 30), (17, 0)]
    ends = [(21, 15), (21, 45), (22, 30), (23, 0), (23, 15), (23, 45)]
    for d in days:
        heads = W.TREADWELL_HEADS[d.month]
        for a_ in assoc[:heads]:
            if rng.random() < 0.30:
                continue
            s_ = starts[int(rng.integers(0, len(starts)))]
            e_ = ends[int(rng.integers(0, len(ends)))]
            brk = [30, 30, 45][int(rng.integers(0, 3))]
            mins = (e_[0] * 60 + e_[1]) - (s_[0] * 60 + s_[1]) - brk
            h, m = hhmm(mins)
            treadwell.append(dict(assoc=a_, date=d, start=fmt(*s_), end=fmt(*e_), brk=brk, minutes=mins,
                                  hhmm=float("%d.%02d" % (h, m)), approver=["SF", "CS", "JM", "RT"][int(rng.integers(0, 4))]))
    return marlowby, treadwell


def timesheets(rng):
    time_rows, state = base_time(rng)
    days = [dt.date(2026, 1, 1) + dt.timedelta(days=i) for i in range((dt.date(2026, 9, 30) - dt.date(2026, 1, 1)).days + 1)]
    marlowby, treadwell = agencies(rng, days, state[4])
    hours = {m: 0.0 for m in range(1, 10)}
    seen = set()
    for r in marlowby:
        key = (r["worker"], r["date"], r["tin"])
        if key not in seen:
            seen.add(key)
            hours[r["date"].month] += r["hours"]
    for r in treadwell:
        hours[r["date"].month] += r["minutes"] / 60.0
    time_rows = overtime(rng, state, hours)
    return time_rows, marlowby, treadwell


def month_ends():
    import calendar
    return [dt.datetime(2026, m, calendar.monthrange(2026, m)[1], 23, 59, 59) for m in range(1, 10)]


def open_at(r, T):
    if r["events"][0][0] > T:
        return False
    state = None
    for t, e in r["events"]:
        if t <= T:
            state = e
    return state in ("OPENED", "REOPENED")


def tune_month_ends(rng, rows):
    """Place each month end's open count inside its rounding bin: move a few single-spell closures from just after
    the month end to just before it (or back), never across another month end."""
    goal = [1, 8, 2, 9, 0, 1, 9, 2, 8]
    for i, T in enumerate(month_ends()):
        n = sum(1 for r in rows if open_at(r, T))
        r10 = n % 10
        if r10 not in (8, 9, 0, 1, 2):
            g = goal[i]
            shift = (g - r10) if g <= 2 else (g - r10)        # down to x0 to x2, or up to x8 or x9
        else:
            continue
        cands = []
        for r in rows:
            ev = r["events"]
            if len(ev) != 2 or ev[1][1] != "CLOSED" or ev[0][0] > T - dt.timedelta(days=3):
                continue
            c = ev[1][0]
            if shift < 0 and T < c <= T + dt.timedelta(days=3):
                cands.append(r)
            if shift > 0 and T - dt.timedelta(days=3) < c <= T:
                cands.append(r)
        cands.sort(key=lambda r: r["matter_no"] if "matter_no" in r else r["opened"].isoformat())
        pick = [cands[int(i)] for i in rng.choice(len(cands), size=abs(shift), replace=False)]
        for r in pick:
            o, c = r["events"][1]
            if shift < 0:
                newc = dt.datetime.combine(T.date() - dt.timedelta(days=1), dt.time(int(rng.integers(9, 18)),
                                                                                    int(rng.integers(0, 60))))
                while newc.weekday() == 6 or newc.date() in HOLIDAYS:
                    newc -= dt.timedelta(days=1)
            else:
                newc = dt.datetime.combine(T.date() + dt.timedelta(days=1), dt.time(int(rng.integers(9, 18)),
                                                                                    int(rng.integers(0, 60))))
                while newc.weekday() == 6 or newc.date() in HOLIDAYS:
                    newc += dt.timedelta(days=1)
            if newc <= r["events"][0][0]:
                continue
            r["events"][1] = (newc, "CLOSED")
