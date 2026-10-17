"""The cooperative's own records: its member roster, the 2027 cover enrolment from its member portal, its elevators'
scale tickets and inter-site transfer log for 2016 to 2020, its prior covers' statements, and the drought-monitor
extract its agronomy desk keeps. Computed forward from the world and the service's estimates."""
import datetime as dt

import numpy as np

import methods as M
import sim as S
import world as W

UTC = dt.timezone.utc
CENTRAL = dt.timezone(dt.timedelta(hours=-5))       # daylight time, in force on 30 October 2026


def rng(*k):
    return np.random.default_rng([W.STREAM, 700] + list(k))


# ---------------------------------------------------------------- members
HOME_SHARE = {"Ardley": 0.19, "Corvin": 0.31, "Elster": 0.16, "Pallard": 0.19, "Tresham": 0.15}
ENTITY = ["Individual", "Individual", "Individual", "Partnership", "Family LLC", "Family LLC", "Trust"]


def roster():
    r = rng(1)
    out = []
    no = 10400
    for c in W.MEMBERS:
        n = int(round(205 * HOME_SHARE[c]))
        for k in range(n):
            no += int(r.integers(3, 17))
            joined = int(r.integers(1962, 2025))
            status = "Active"
            if r.random() < 0.07:
                status = "Inactive"
            out.append(dict(member_no=str(no), entity=ENTITY[int(r.integers(0, len(ENTITY)))], home_county=c,
                            joined=joined, status=status, irrigates=bool(c == "Corvin" and r.random() < 0.35)))
    out.sort(key=lambda m: m["member_no"])
    return out


# ---------------------------------------------------------------- the 2027 enrolment
ENROL_DRY = {"Ardley": 3640, "Corvin": 9760, "Elster": 2910, "Pallard": 3880, "Tresham": 2570}
FIELD_CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def _field_id(r):
    return "".join(FIELD_CHARS[int(i)] for i in r.integers(0, len(FIELD_CHARS), 4)) + "-" + "%02d" % int(r.integers(1, 40))


def _stamp(t):
    return t.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def enrolment(members):
    """Rows of the portal export: one submission per row. Fields enrolled on time, amendments before the close,
    and a few submissions after the 5:00 p.m. Central close on 30 October, some of them still dated 30 October in UTC."""
    r = rng(2)
    active = [m for m in members if m["status"] == "Active"]
    close = dt.datetime(2026, 10, 30, 17, 0, tzinfo=CENTRAL)
    opened = dt.datetime(2026, 9, 8, 8, 0, tzinfo=CENTRAL)
    subs = []
    sid = 50311
    used = set()

    def new_id():
        while True:
            f = _field_id(r)
            if f not in used:
                used.add(f)
                return f

    def when_on_time():
        span = (close - opened).total_seconds()
        # most members enrol in the last three weeks
        u = 1 - r.beta(1.0, 2.6)
        t = opened + dt.timedelta(seconds=float(u * span))
        return min(t, close - dt.timedelta(minutes=int(r.integers(3, 600))))

    for c in W.MEMBERS:
        ms = [m for m in active if m["home_county"] == c]
        target = ENROL_DRY[c]
        acres = 0.0
        while acres < target:
            m = ms[int(r.integers(0, len(ms)))]
            a = round(float(np.clip(r.gamma(3.0, 45.0), 18, 640)), 1)
            # a field across the county line now and then
            fc = c
            if r.random() < 0.06:
                fc = W.MEMBERS[int(r.integers(0, 5))]
            subs.append(dict(sid=sid, t=when_on_time(), member=m["member_no"], field=new_id(), county=fc,
                             practice="Non-irrigated", acres=a, action="NEW"))
            sid += 1
            if fc == c:
                acres += a
        # irrigated fields enrolled through the same portal by members who irrigate
        for m in [m for m in ms if m["irrigates"]]:
            for _ in range(int(r.integers(1, 3))):
                subs.append(dict(sid=sid, t=when_on_time(), member=m["member_no"], field=new_id(), county=c,
                                 practice="Irrigated", acres=round(float(np.clip(r.gamma(4.0, 30.0), 40, 400)), 1),
                                 action="NEW"))
                sid += 1
    subs.sort(key=lambda s: s["t"])
    # amendments before the close: a field's acres corrected after a re-measure
    on_time = [s for s in subs if s["practice"] == "Non-irrigated"]
    for s in [on_time[int(i)] for i in r.choice(len(on_time), 26, replace=False)]:
        t = s["t"] + dt.timedelta(hours=float(r.uniform(2, 240)))
        if t >= close:
            t = close - dt.timedelta(minutes=int(r.integers(10, 300)))
        if t <= s["t"]:
            continue
        subs.append(dict(sid=None, t=t, member=s["member"], field=s["field"], county=s["county"],
                         practice=s["practice"], acres=round(s["acres"] * float(r.uniform(0.86, 1.12)), 1),
                         action="AMEND"))
    # late: after 5:00 p.m. Central on 30 October; before 7:00 p.m. they are still dated 30 October in UTC
    late_specs = [("Ardley", 2), ("Corvin", 3), ("Elster", 2), ("Pallard", 2), ("Tresham", 2)]
    for c, n in late_specs:
        ms = [m for m in active if m["home_county"] == c]
        for k in range(n):
            t = close + dt.timedelta(minutes=int(r.integers(4, 118)))
            m = ms[int(r.integers(0, len(ms)))]
            subs.append(dict(sid=None, t=t, member=m["member_no"], field=new_id(), county=c, practice="Non-irrigated",
                             acres=round(float(np.clip(r.gamma(3.0, 55.0), 40, 520)), 1), action="NEW"))
    # two late amendments inside the same two hours, and a few stragglers after 7:00 p.m. Central
    dry = [s for s in subs if s["practice"] == "Non-irrigated" and s["action"] == "NEW" and s["t"] < close]
    for s in [dry[int(i)] for i in r.choice(len(dry), 2, replace=False)]:
        subs.append(dict(sid=None, t=close + dt.timedelta(minutes=int(r.integers(20, 110))), member=s["member"],
                         field=s["field"], county=s["county"], practice=s["practice"],
                         acres=round(s["acres"] * 1.35, 1), action="AMEND"))
    for k in range(4):
        c = W.MEMBERS[int(r.integers(0, 5))]
        ms = [m for m in active if m["home_county"] == c]
        m = ms[int(r.integers(0, len(ms)))]
        subs.append(dict(sid=None, t=close + dt.timedelta(minutes=int(r.integers(130, 900))), member=m["member_no"],
                         field=new_id(), county=c, practice="Non-irrigated",
                         acres=round(float(np.clip(r.gamma(3.0, 50.0), 30, 480)), 1), action="NEW"))
    subs.sort(key=lambda s: s["t"])
    n = 50311
    for s in subs:
        s["sid"] = "P%06d" % n
        n += int(rng(3, n).integers(1, 4))
        s["stamp"] = _stamp(s["t"])
    return subs


def enrolled_acres(subs, local_close=True, keep_irrigated=False, latest=True):
    """Acres per county under a handling: the golden is local_close, dryland only, the latest on-time submission
    per field."""
    if local_close:
        ok = [s for s in subs if s["stamp"] < W.CLOSE_UTC]
    else:
        ok = [s for s in subs if s["stamp"][:10] <= W.CLOSE_UTC[:10]]
    by_field = {}
    for s in sorted(ok, key=lambda s: s["stamp"]):
        if not latest and s["field"] in by_field:
            continue
        by_field[s["field"]] = s
    out = {c: 0.0 for c in W.MEMBERS}
    for s in by_field.values():
        if s["practice"] != "Non-irrigated" and not keep_irrigated:
            continue
        out[s["county"]] += s["acres"]
    return out


# ---------------------------------------------------------------- elevator receipts 2016 to 2020
RECEIPT_SHARE = {"Ardley": 0.312, "Corvin": 0.218, "Elster": 0.381, "Pallard": 0.268, "Tresham": 0.343}
SITE_OF = {"Ardley": "ARD", "Corvin": "MAIN", "Elster": "ELS", "Pallard": "PAL", "Tresham": "TRE"}
TRANSFER_SHARE = {"SORGHUM": 0.19, "WHEAT": 0.12, "CORN": 0.08}


def tickets(members, x):
    """Inbound scale tickets 2016 to 2020 for sorghum, wheat and corn, with the terminal's tickets for grain moved
    in from the satellite sites written to the member of record, and the satellite sites' transfer log."""
    r = rng(4)
    cty, _ = S.current(x)
    active = [m for m in members if m["joined"] <= 2016]
    rows, transfers = [], []
    tno = set()

    def ref():
        while True:
            v = int(r.integers(4100000, 4999999))
            if v not in tno:
                tno.add(v)
                return str(v)
    ticket = 210000
    for y in range(2016, 2021):
        i = y - W.Y0
        for c in W.MEMBERS:
            ms = [m for m in active if m["home_county"] == c]
            prod = float(cty[(c, "SORGHUM", "ALL")]["production"][i])
            targets = {"SORGHUM": RECEIPT_SHARE[c] * prod * float(r.uniform(0.94, 1.06))}
            wprod = float(cty[(c, "WHEAT", "ALL")]["production"][i])
            targets["WHEAT"] = 0.18 * wprod * float(r.uniform(0.9, 1.1))
            cprod = float(cty[(c, "CORN", "ALL")]["production"][i])
            targets["CORN"] = 0.12 * cprod * float(r.uniform(0.9, 1.1))
            for crop, tgt in targets.items():
                got = 0.0
                if crop == "SORGHUM":
                    season = (dt.date(y, 9, 25), dt.date(y, 11, 25))
                    mlo, mhi = 12.2, 17.6
                elif crop == "WHEAT":
                    season = (dt.date(y, 6, 18), dt.date(y, 7, 22))
                    mlo, mhi = 10.8, 14.2
                else:
                    season = (dt.date(y, 9, 15), dt.date(y, 11, 10))
                    mlo, mhi = 13.5, 19.5
                while got < tgt:
                    m = ms[int(r.integers(0, len(ms)))]
                    net = int(round(float(r.uniform(41000, 62000)) / 20) * 20)
                    moist = round(float(r.uniform(mlo, mhi)), 1)
                    bu = net * (100 - moist) / (100 - W.STANDARD_MOISTURE) / W.BUSHEL_LB
                    got += bu
                    d = season[0] + dt.timedelta(days=int(r.integers(0, (season[1] - season[0]).days + 1)))
                    u = r.random()
                    if c == "Corvin":         # Corvin's members near the county line also haul to the Elster site
                        site = "MAIN" if u < 0.8 else "ELS"
                    else:
                        site = SITE_OF[c] if u < 0.88 else "MAIN"
                    gross = net + int(round(float(r.uniform(29000, 33500)) / 20) * 20)
                    ticket += int(r.integers(1, 4))
                    t = dict(ticket=str(ticket), site=site, date=d, account=m["member_no"], crop=crop, origin=c,
                             gross=gross, tare=gross - net, net=net, moisture=moist,
                             tw=round(float(r.uniform(55.0, 60.5) if crop != "CORN" else r.uniform(54.0, 58.5)), 1),
                             reference=ref(), transfer=False)
                    rows.append(t)
                    if site != "MAIN" and r.random() < TRANSFER_SHARE[crop]:
                        ship = d + dt.timedelta(days=int(r.integers(2, 21)))
                        tn = ref()
                        shipped = int(round(net * float(1 + r.normal(0, 0.003)) / 20) * 20)
                        transfers.append(dict(transfer=tn, date=ship, frm=site, to="MAIN", crop=crop, net=shipped,
                                              carrier="Cooperative truck" if r.random() < 0.7 else "Hired carrier"))
                        rn = int(round(shipped * float(1 + r.normal(0, 0.002)) / 20) * 20)
                        rg = rn + int(round(float(r.uniform(29000, 33500)) / 20) * 20)
                        ticket += int(r.integers(1, 4))
                        rows.append(dict(ticket=str(ticket), site="MAIN", date=ship + dt.timedelta(days=int(r.integers(0, 2))),
                                         account=m["member_no"], crop=crop, origin=c, gross=rg, tare=rg - rn, net=rn,
                                         moisture=round(max(moist - float(r.uniform(0.0, 0.4)), 10.0), 1),
                                         tw=t["tw"], reference=tn, transfer=True))
    # ticket numbers in date order within each site, as the scale software issues them
    rows.sort(key=lambda t: (t["date"], t["site"], t["ticket"]))
    seq = {}
    for t in rows:
        seq[t["site"]] = seq.get(t["site"], {"MAIN": 300000, "ARD": 410000, "ELS": 520000, "PAL": 630000, "TRE": 740000}[t["site"]]) + 1
        t["ticket"] = "%s-%d" % (t["site"], seq[t["site"]])
    transfers.sort(key=lambda t: (t["date"], t["transfer"]))
    return rows, transfers


def receipts_share(rows, x, drop_transfers=True, shrink=True, crop="SORGHUM", vintage="new"):
    """The cooperative's 2016 to 2020 receipts from each county as a share of the county's production, per cent."""
    cty = x["cty_new"] if vintage == "new" else x["cty_old"]
    out = {}
    for c in W.MEMBERS:
        bu = 0.0
        for t in rows:
            if t["origin"] != c or (crop and t["crop"] != crop):
                continue
            if drop_transfers and t["transfer"]:
                continue
            if shrink:
                bu += t["net"] * (100 - t["moisture"]) / (100 - W.STANDARD_MOISTURE) / W.BUSHEL_LB
            else:
                bu += t["net"] / W.BUSHEL_LB
        prod = sum(float(cty[(c, "SORGHUM", "ALL")]["production"][y - W.Y0]) for y in range(2016, 2021))
        out[c] = 100.0 * bu / prod
    return out


# ---------------------------------------------------------------- prior covers 2019 to 2025 (a distractor)
def prior_covers(x):
    """The cooperative's earlier one-year covers on Corvin's and Tresham's dryland sorghum yields, 2019 to 2025, as
    the reinsurer's annual statements gave them: the year's expected yield, trigger at 85 per cent, the published
    yield, liability and indemnity."""
    cty, _ = S.current(x)
    pub = x["pub"]
    r = rng(5)
    out = []
    for c in ("Corvin", "Tresham"):
        py = M.published_yield(cty, pub, c)
        for y in range(2019, 2026):
            exp_y = round(np.mean([py[k] for k in range(y - 10, y) if k in py]) * 1.04, 1)
            trig = round(0.85 * exp_y, 1)
            liab = int(round(float(r.uniform(1.1, 1.5)) * (2.2e6 if c == "Corvin" else 0.62e6), -2))
            share = max(0.0, (trig - py[y]) / trig)
            out.append(dict(county=c, year=y, expected=exp_y, trigger=trig, final=py[y], liability=liab,
                            indemnity=int(round(liab * share, 0)), rate=round(float(r.uniform(4.0, 6.5)), 2)))
    return out


# ---------------------------------------------------------------- drought monitor extract (a distractor)
def drought_weeks(x):
    """Weekly share of each member county's area in each drought category, 2000 to 2025, cumulative as the drought
    monitor publishes it (D0 includes D1 and worse)."""
    out = []
    for c in W.MEMBERS:
        d = W.COUNTIES[c][1]
        w = x["weather"][d]
        r = rng(6, int(W.COUNTIES[c][0]))
        day = dt.date(2000, 1, 4)
        while day <= dt.date(2025, 12, 30):
            y = day.year
            sev = float(np.clip((1 - w[y - W.Y0]) * 3.2, 0, 1.6))
            season = np.exp(-((day.timetuple().tm_yday - 200) / 70.0) ** 2)
            level = sev * (0.35 + 0.65 * season) + float(r.normal(0, 0.06))
            cats = []
            for k in range(5):
                share = float(np.clip((level - 0.18 * k) / 0.25, 0, 1)) * 100
                cats.append(round(share, 2))
            for k in range(1, 5):
                cats[k] = min(cats[k], cats[k - 1])
            out.append(dict(date=day, county=c, none=round(100 - cats[0], 2), d=cats))
            day += dt.timedelta(days=7)
    return out


# ---------------------------------------------------------------- figures placed inside their rounding bins
def _mid(v, step):
    """1.0 at the middle of v's rounding bin, 0.0 on its edge."""
    k = v / step
    return abs((k - np.floor(k)) - 0.5) / 0.5


def center_enrolment(subs, terms, quotes, floor=0.6):
    """Move one field's acres in each county by a few tenths, so that each county's liability and premium sit inside
    their $100 bins (the field: the county's largest dryland field enrolled on time and never amended)."""
    price = W.PRICE_CWT * W.BUSHEL_LB / 100.0
    amended = {s["field"] for s in subs if s["action"] == "AMEND"}
    for c in W.MEMBERS:
        base = enrolled_acres(subs)[c]
        cand = [s for s in subs if s["county"] == c and s["practice"] == "Non-irrigated" and s["action"] == "NEW"
                and s["stamp"] < W.CLOSE_UTC and s["field"] not in amended]
        f = max(cand, key=lambda s: (s["acres"], s["field"]))
        best = None
        for k in range(0, 61):
            for sgn in (1, -1):
                d = sgn * k / 10.0
                acres = base + d
                lia = acres * terms[c]["expected"] * W.COVERAGE * price
                prem = lia * quotes[c] / 100.0
                score = min(_mid(lia, 100), _mid(prem, 100))
                if score >= floor:
                    best = d
                    break
            if best is not None:
                break
        assert best is not None, c
        f["acres"] = round(f["acres"] + best, 1)
    return subs


def center_tickets(rows, x, floor=0.6, n=14):
    """Move the county's last ordinary 2020 sorghum loads by up to a few thousand pounds each, so that each county's
    receipts share sits inside its 0.1-point bin."""
    for c in W.MEMBERS:
        cand = [t for t in rows if t["origin"] == c and t["crop"] == "SORGHUM" and not t["transfer"]
                and t["date"].year == 2020 and t["site"] == SITE_OF[c]]
        cand = sorted(cand, key=lambda t: (t["date"], t["ticket"]))[-n:]
        base = {id(t): t["net"] for t in cand}
        done = False
        for k in range(0, 300):
            for sgn in (1, -1):
                d = sgn * 20 * k
                if any(not 38000 <= base[id(t)] + d <= 60000 for t in cand):
                    continue
                for t in cand:
                    t["net"] = base[id(t)] + d
                if _mid(receipts_share(rows, x)[c], 0.1) >= floor:
                    done = True
                    break
            if done:
                break
        assert done, c
        for t in cand:
            t["gross"] = t["net"] + t["tare"]
    return rows
