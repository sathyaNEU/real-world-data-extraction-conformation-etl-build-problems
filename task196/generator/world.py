"""Kelverstone Mutual's world, as clean truth before any mess is applied or any document written.

Every quantity the pack ships derives from here. The simulation is deterministic: one RNG stream per
member and scheme year, seeded from the task number, so two runs give identical bytes.

The detection structure is the point of the build. A scam case can be sighted twice:

  channel M  the member's own case register, which holds the cases its controls caught
  channel S  the scheme's mule-account register, which holds beneficiary accounts firms have reported

A payment matches channel S when its beneficiary account is on the register. Those matches come from two
different causes, and the pack cannot tell them apart by any column:

  independent   another firm's victim reported the account, which happens whether or not this member
                ever saw its own case
  self-produced the member asked the receiving firm to return the funds after opening its own case, and
                the receiving firm registered the account because of that request

The second kind is not a second sighting of the case: it is the first sighting coming back. The only
record that attributes a registration is the member's own fund-return request log, and the data is built
so that attribution is exact: no payment carries both a fund-return request and an independent
registration dated after it (asserted in checks.py and verify.py).
"""
import datetime as dt
import math
import random

TASK_SEED = 196
AS_OF = dt.date(2027, 3, 31)          # the mutual's evidence base closes here
PULL = dt.date(2027, 7, 2)            # every extract in the pack was pulled on this date
MEETING = dt.date(2027, 7, 14)        # the trustees' meeting the review is on the agenda for

SCHEME_YEARS = ["2023/24", "2024/25", "2025/26", "2026/27"]
MEASURED = "2026/27"                  # the scheme year the index is measured over
INDEMNITY_YEAR = "1 October 2027 to 30 September 2028"

# The recall window: a member only asks for funds back while there is a chance of recovering them, so a
# case opened more than this many days after the payment produces no fund-return request. This is what
# makes the attribution exact rather than a date rule.
RECALL_WINDOW_DAYS = 30

# The least number of days a fund-return request can follow an independent registration. An account
# another firm's victim reported is on the register long before this member ever asks about it, so there
# is no band of registrations sitting a day or two ahead of a request where the two could be confused:
# either the request precedes the registration, or the registration precedes it by at least this many
# days. Asserted in checks.py and verify.py as a gap with nothing inside it.
REQUEST_GAP_DAYS = 22

# The share of independent registrations that predate the payment they match. The register is a standing
# industry list and an account stays on it, so a member's payment can land on an account already
# reported. The share is held the same among the member's own recorded cases and the cases it never
# recorded, so an analyst who reads the channel without those rows divides a smaller numerator by a
# proportionally smaller overlap and makes the same call (SF13, a C1 convergence).
PRE_PAYMENT_SHARE = 0.62

# The share of recorded cases that surface inside the recall window, and so draw a fund-return request.
# Investment and romance scams, where the victim is strung along, surface long after the window and the
# member never asks for the money back, which is what leaves a body of its own cases whose registrations
# no request of its own can explain. It is a property of the scam mix rather than of this mutual.
REQUEST_SHARE = 0.60

# ---------------------------------------------------------------------------
# Members. The review group is the third of the membership whose triennial review falls this cycle.
# Volumes for the review group are derived in build_members() so each one's index lands mid-bin.
# ---------------------------------------------------------------------------
MEMBERS = [
    # code, name, tier, joined, review group, true cases 2026/27, member coverage, scheme coverage,
    # registration rate after a request, target index (review group only)
    ("KM-104", "Castlegate Payments",  "B", dt.date(2016, 4, 1),  True,  690, 400 / 690, 270 / 690, 0.850, 30.94),
    ("KM-101", "Brindlemere Remit",    "A", dt.date(2014, 10, 1), True,  515, 0.860, 0.310, 0.780, 12.11),
    ("KM-112", "Saltmarch Pay",        "C", dt.date(2019, 4, 1),  True,  140, 0.780, 0.330, 0.800, 21.88),
    ("KM-108", "Trentmoor Money",      "B", dt.date(2017, 7, 1),  True,  300, 0.820, 0.290, 0.760, 15.07),
    ("KM-115", "Pelbury Exchange",     "C", dt.date(2020, 1, 1),  False, 96,  0.740, 0.320, 0.820, None),
    ("KM-102", "Oakhanger Transfer",   "A", dt.date(2014, 10, 1), False, 402, 0.900, 0.300, 0.720, None),
    ("KM-118", "Netherby Pay",         "C", dt.date(2021, 4, 1),  False, 131, 0.710, 0.340, 0.830, None),
    ("KM-106", "Quayfield Remit",      "B", dt.date(2016, 10, 1), False, 248, 0.845, 0.305, 0.790, None),
    ("KM-121", "Thrimby Money",        "C", dt.date(2022, 1, 1),  False, 74,  0.760, 0.325, 0.810, None),
    ("KM-110", "Vellowe Pay",          "B", dt.date(2018, 4, 1),  False, 214, 0.880, 0.295, 0.750, None),
    ("KM-124", "Garnock Exchange",     "A", dt.date(2023, 10, 17), False, 331, 0.870, 0.315, 0.770, None),
    ("KM-103", "Wrenhall Pay",         "A", dt.date(2015, 4, 1),  False, 356, 0.915, 0.300, 0.700, None),
]

# A contribution tier is set at a member's triennial review and holds until the next one, so a member
# whose volumes have moved since is carried at the tier its last review set, in either direction:
# Wrenhall's book has fallen out of Tier A and Netherby's has grown past the Tier C ceiling, and both
# are carried where their last review put them. The register's own triennial-review field says whose
# review falls this cycle, so a held tier names a review year from an earlier cycle year.
TIER_HELD_FROM = {"KM-103": "2025", "KM-118": "2026"}

# Payments sent, as a factor on the member's base volume, year by year. Each member's book moves on its
# own terms: Wrenhall has been losing a corporate corridor for three years, Trentmoor and Pelbury each
# gave a year back, Garnock joined part way through 2023/24 and is still scaling, and Thrimby's growth
# has stopped on a repricing. The four review-group members end on 1.000 because their base volume is
# solved back from the index their review is read at (build_members, world), so the measured year is the
# anchor and the earlier years are the member's own path to it.
VOLUME_PATH = {
    "KM-101": (0.845, 0.898, 0.951, 1.000),
    "KM-102": (1.021, 0.994, 0.978, 1.013),
    "KM-103": (1.286, 1.174, 1.062, 0.973),
    "KM-104": (0.780, 0.860, 0.930, 1.000),
    "KM-106": (0.871, 0.916, 0.958, 1.006),
    "KM-108": (0.905, 0.962, 0.934, 1.000),
    "KM-110": (0.688, 0.809, 0.896, 1.019),
    "KM-112": (0.642, 0.751, 0.884, 1.000),
    "KM-115": (0.734, 0.952, 0.911, 1.034),
    "KM-118": (0.766, 0.842, 0.931, 0.994),
    "KM-121": (0.613, 0.785, 0.968, 0.991),
    "KM-124": (0.690, 0.869, 0.942, 1.011),
}

# The quarter a payment institution sends most of its volume in. The industry shape is the same for
# everybody (the run-up to Christmas is the peak), but a member's own mix moves it: a payroll-heavy
# book is flat, a marketplace book is steeper. Each member's shape is drawn once around the industry
# one and holds across the four years, so no two members report the same quarterly pattern.
INDUSTRY_SHAPE = (0.238, 0.244, 0.263, 0.255)

# A member files a quarter at a time and the year is whatever its four quarters add up to, so the
# generator draws the quarters and sums them rather than fixing a year and dividing it. These are the
# member-years the review reads an index off and which therefore cannot move: each review-group
# member's measured year, which its index is a rate on, and the two earlier revised years of the
# member whose walk the trustees read. There and only there the shape's own rounding is carried by
# the member's largest quarter, so the four sum to the total the review quotes.
PINNED_YEARS = {("KM-104", "2024/25"), ("KM-104", "2025/26"),
                ("KM-104", "2026/27"), ("KM-101", "2026/27"),
                ("KM-108", "2026/27"), ("KM-112", "2026/27")}

# The member whose ladder is measured: the date-only rungs and the whole window sweep read the days
# between a case's own recorded date and the registration of the account it paid, for this member and
# the measured year alone (golden.window_index, golden.post_case_index).
LADDER_SUBJECT = "KM-104"

TIER_NAMES = {"A": "Tier A, over 25 million payments a year",
              "B": "Tier B, 10 to 25 million payments a year",
              "C": "Tier C, under 10 million payments a year"}

# Year factors on the true case count, so the panel has a baseline and a shape rather than one year.
YEAR_FACTOR = {"2023/24": 0.71, "2024/25": 0.83, "2025/26": 0.92, "2026/27": 1.00}
# Castlegate's own coverage fell as its book grew: this is the finding, not a planted defect.
COVERAGE_BY_YEAR = {"2023/24": 1.26, "2024/25": 1.18, "2025/26": 1.08, "2026/27": 1.00}

# How long the receiving firm takes to register the account after a fund-return request, in days, by the
# kind of firm that received the money. A clearing bank raises the report from the request itself the same
# day; an e-money institution batches its mule reporting fortnightly; a building society or an overseas
# correspondent reports when its own investigation closes, about six weeks out. The three cadences are why
# the date-window family steps across the golden's printed bin instead of resting in it (DESIGN_NOTE.md,
# Grid), and they are a property of the receiving side rather than anything this mutual arranges.
REGISTRATION_CADENCE = {"clearing bank": (1, 2), "e-money institution": (14, 15),
                        "building society": (38, 40), "overseas correspondent": (38, 40)}

QUARTERS = {"2026/27": [(dt.date(2026, 4, 1), dt.date(2026, 6, 30)),
                        (dt.date(2026, 7, 1), dt.date(2026, 9, 30)),
                        (dt.date(2026, 10, 1), dt.date(2026, 12, 31)),
                        (dt.date(2027, 1, 1), dt.date(2027, 3, 31))]}

ROUTES = ["beneficiary recall", "repatriation", "insurer contribution"]
SCAM_TYPES = ["purchase", "investment", "impersonation", "advance fee", "romance", "invoice"]
CHANNELS = ["faster payment", "same day value", "international transfer", "card to account"]
DEST_FIRM = ["clearing bank", "e-money institution", "building society", "overseas correspondent"]


def year_bounds(y):
    a = int(y.split("/")[0])
    return dt.date(a, 4, 1), dt.date(a + 1, 3, 31)


def rng(*parts):
    h = TASK_SEED
    for p in parts:
        h = (h * 1000003 + sum(ord(c) * (i + 7) for i, c in enumerate(str(p)))) % (2 ** 61 - 1)
    return random.Random(h)


def account_ref(r):
    """A sort code and account number pair, structured the way the register holds it."""
    return "%02d-%02d-%02d/%08d" % (r.randint(10, 89), r.randint(10, 99), r.randint(10, 99),
                                    r.randrange(0, 10 ** 8))


def lognormal_amount(r, mu=math.log(1250.0), sigma=1.55, cap=480000.0):
    v = r.lognormvariate(mu, sigma)
    return round(min(v, cap), 2)


class Case:
    """One scam case the member's customers suffered, recorded or not."""
    __slots__ = ("member", "year", "idx", "payment_date", "amount", "scam_type", "channel", "dest_firm",
                 "account", "recorded", "case_ref", "open_date", "report_lag", "independent_reg",
                 "independent_reg_date", "request_date", "self_reg_date", "reimbursed", "closed_date",
                 "legs", "recovery_route", "recovery_amount", "recovery_date")

    def __init__(self, **kw):
        for k, v in kw.items():
            setattr(self, k, v)

    @property
    def matched(self):
        return self.independent_reg or self.self_reg_date is not None

    @property
    def registration_date(self):
        if self.independent_reg:
            return self.independent_reg_date
        return self.self_reg_date


def build_members():
    """Members with their derived payment volumes. The volume is set from the two-source estimate the
    member's own counts produce, so each review-group index lands mid-bin on a non-round value."""
    out = []
    for code, name, tier, joined, review, n_true, p_m, p_s, q, target in MEMBERS:
        n_m = round(n_true * p_m)
        n_s = round(n_true * p_s)
        both = round(n_true * p_m * p_s)
        petersen = n_m * n_s / both
        if target is not None:
            vol = petersen / target * 1e6          # payments in the measured year
        else:
            # a member outside the review group needs a volume, not a target index: take it from the
            # build's own stream rather than from hash(), which is randomised per process
            vol = n_true / (8.0 + rng("vol", code).randrange(23)) * 1e6
            vol = round(vol / 1e5) * 1e5
        out.append(dict(code=code, name=name, tier=tier, joined=joined, review=review, n_true=n_true,
                        p_m=p_m, p_s=p_s, q=q, target=target, volume=vol, n_m=n_m, n_s=n_s, both=both,
                        petersen=petersen))
    return out


def build_cases(members):
    """Every true case in every scheme year, with its sightings. Counts are design parameters; which
    case falls in which set is drawn."""
    cases = []
    for m in members:
        for y in SCHEME_YEARS:
            lo, hi = year_bounds(y)
            if m["joined"] > lo:
                lo = m["joined"]
            span = (hi - lo).days
            n_true = int(round(m["n_true"] * YEAR_FACTOR[y]))
            p_m = min(0.97, m["p_m"] * COVERAGE_BY_YEAR[y] if m["code"] == "KM-104" else m["p_m"])
            p_s = m["p_s"]
            n_m = round(n_true * p_m)
            n_s = round(n_true * p_s)
            both = round(n_true * p_m * p_s)
            r = rng("cases", m["code"], y)
            # the cases themselves
            group = []
            for i in range(n_true):
                # a seasonal shape: more cases in the run-up to Christmas and in January
                w = r.random()
                day = int(span * (w ** 0.92))
                pd = lo + dt.timedelta(days=min(span, day))
                group.append(Case(member=m["code"], year=y, idx=i, payment_date=pd,
                                  amount=lognormal_amount(r), scam_type=r.choice(SCAM_TYPES),
                                  channel=r.choices(CHANNELS, weights=[55, 18, 19, 8])[0],
                                  dest_firm=r.choices(DEST_FIRM, weights=[34, 48, 10, 8])[0],
                                  account=account_ref(r), recorded=False, case_ref=None, open_date=None,
                                  report_lag=None, independent_reg=False, independent_reg_date=None,
                                  request_date=None, self_reg_date=None, reimbursed=None,
                                  closed_date=None, legs=1, recovery_route=None, recovery_amount=0.0,
                                  recovery_date=None))
            order = list(range(n_true))
            r.shuffle(order)
            m_set = set(order[:n_m])                      # recorded by the member
            # report lag: a case is opened when the customer or the monitoring finds it. Cases on
            # already-reported accounts are found the same way as any other.
            for i in sorted(m_set):
                c = group[i]
                c.recorded = True
                # most cases surface inside the recall window, the slow ones (investment and romance
                # scams, where the victim is strung along) long after it
                room = max(RECALL_WINDOW_DAYS + 3, (PULL - c.payment_date).days - 4)
                if r.random() < REQUEST_SHARE:
                    c.report_lag = r.randint(1, RECALL_WINDOW_DAYS - 1)
                else:
                    c.report_lag = r.randint(RECALL_WINDOW_DAYS + 2, min(190, room))
                c.open_date = c.payment_date + dt.timedelta(days=c.report_lag)
            # fund-return requests come first, because where a member asked for the money back the
            # request is what the receiving firm's own registration answers. A request is only sent
            # while there is a chance of recovering the funds.
            requested = [i for i in sorted(m_set)
                         if group[i].report_lag is not None and group[i].report_lag < RECALL_WINDOW_DAYS]
            for i in requested:
                c = group[i]
                # the fraud team works a queue, so the request goes days after the case is opened
                c.request_date = c.open_date + dt.timedelta(days=r.randint(1, 5))
            never = [i for i in sorted(m_set) if group[i].request_date is None]
            unrec = [i for i in order if i not in m_set]
            # The independent capture: another firm's victim reports the receiving account, which has
            # nothing to do with whether this member asked for its money back. The rate is therefore
            # held the same inside every subset an analyst can cut, the cases the member asked about and
            # the cases it never asked about alike, so the capture probability is one number however it
            # is read off the member's own register (SF12's sixth form).
            k_req = round(len(requested) * p_s)
            k_never = both - k_req
            req_sh, never_sh, unrec_sh = list(requested), list(never), list(unrec)
            r.shuffle(req_sh)
            r.shuffle(never_sh)
            r.shuffle(unrec_sh)
            assert 0 <= k_req <= len(req_sh) and 0 <= k_never <= len(never_sh), (
                "stratified capture does not fit: %s %s" % (m["code"], y))
            s_set = set(req_sh[:k_req]) | set(never_sh[:k_never]) | set(unrec_sh[:n_s - both])
            for i in sorted(s_set):
                group[i].independent_reg = True
            # Independent registration dates. The register is a standing list, so some of these accounts
            # were reported before the member's payment ever landed on them and the rest were reported
            # after. Two properties are built here and asserted in checks.py and verify.py. First, where
            # the member did send a request, the registration precedes it by at least REQUEST_GAP_DAYS,
            # so there is no band of registrations sitting a day or two ahead of a request that a reading
            # could attribute either way. Second, the share that predates the payment is the same among
            # the member's own cases and the cases it never recorded, so dropping them is the same call.
            rec_ind = [i for i in sorted(s_set) if i in m_set]
            unrec_ind = [i for i in sorted(s_set) if i not in m_set]
            # a request this close behind the payment leaves no room for a registration in front of it
            forced = [i for i in rec_ind if group[i].request_date is not None
                      and (group[i].request_date - group[i].payment_date).days - REQUEST_GAP_DAYS < 1]
            want_pre = max(len(forced), round(len(rec_ind) * PRE_PAYMENT_SHARE))
            spare = [i for i in rec_ind if i not in set(forced)]
            r.shuffle(spare)
            pre = set(forced) | set(spare[:want_pre - len(forced)])
            unrec_pre = list(unrec_ind)
            r.shuffle(unrec_pre)
            # the same share, so the ratio the estimate divides is untouched by dropping these rows
            share = len(pre) / len(rec_ind) if rec_ind else 0.0
            pre |= set(unrec_pre[:round(len(unrec_ind) * share)])
            for i in sorted(s_set):
                c = group[i]
                if i in pre:
                    # reported before this member's payment landed on the account
                    back = min(150, max(20, (c.payment_date - dt.date(2022, 10, 1)).days - 1))
                    c.independent_reg_date = c.payment_date - dt.timedelta(
                        days=r.randint(min(20, back), back))
                elif c.request_date is not None:
                    room = (c.request_date - c.payment_date).days - REQUEST_GAP_DAYS
                    c.independent_reg_date = c.payment_date + dt.timedelta(days=r.randint(1, room))
                elif c.recorded:
                    # the member never asked for the money back, and another firm's victim reported the
                    # account later, after this member had already opened its own case
                    ahead = max(2, min(210, (PULL - c.open_date).days - 2))
                    c.independent_reg_date = c.open_date + dt.timedelta(days=r.randint(1, ahead))
                else:
                    ahead = max(2, min(210, (PULL - c.payment_date).days - 2))
                    c.independent_reg_date = c.payment_date + dt.timedelta(days=r.randint(2, ahead))
            # the receiving firm registers the account because of the request, for a share of the
            # requests on accounts nobody else had reported
            candidates = [i for i in requested if not group[i].independent_reg]
            r.shuffle(candidates)
            want = round(len(candidates) * m["q"])
            for i in candidates[:want]:
                c = group[i]
                lo_b, hi_b = REGISTRATION_CADENCE[c.dest_firm]
                c.self_reg_date = c.request_date + dt.timedelta(days=r.randint(lo_b, hi_b))
            # reimbursement, closure and recoveries, which the ask layer runs on
            for i in sorted(m_set):
                c = group[i]
                c.reimbursed = round(c.amount * (1.0 if r.random() < 0.83 else r.uniform(0.35, 0.9)), 2)
                # a case opened close to the extract has not closed yet: the register carries it open
                room = (PULL - c.open_date).days - 1
                c.closed_date = (c.open_date + dt.timedelta(days=r.randint(12, min(150, room)))
                                 if room >= 12 else None)
                c.legs = 1 if r.random() < 0.82 else 2
                c.recovery_route = None
                c.recovery_amount = 0.0
                c.recovery_date = None
                if c.closed_date and r.random() < 0.46:
                    room_r = (PULL - c.closed_date).days - 1
                    if room_r >= 3:
                        c.recovery_route = r.choices(ROUTES, weights=[58, 27, 15])[0]
                        c.recovery_amount = round(c.reimbursed * r.uniform(0.05, 0.62), 2)
                        c.recovery_date = c.closed_date + dt.timedelta(
                            days=r.randint(3, min(120, room_r)))
            cases.extend(group)
    return cases


def months_of(y):
    """The twelve calendar months of a scheme year, April first."""
    a = int(y.split("/")[0])
    return [(a + (4 + i - 1) // 12, (4 + i - 1) % 12 + 1) for i in range(12)]


def self_produced(c):
    """A registration the member's own fund-return request produced: the request went first."""
    return (c.registration_date is not None and c.request_date is not None
            and c.request_date <= c.registration_date and c.self_reg_date is not None)


def realised_estimate(cases, code):
    """The two-source estimate on the cases as built, which is what the index is read off. The member's
    payment volume is set from this rather than from the design's own counts, so the printed index lands
    where the design put it instead of drifting by the rounding of the counts."""
    cs = [c for c in cases if c.member == code and c.year == MEASURED]
    rec = [c for c in cs if c.recorded]
    ind = [c for c in cs if c.matched and not self_produced(c)]
    both = [c for c in ind if c.recorded]
    return len(rec) * len(ind) / len(both)


def build_adjustments(members, unauth):
    """Where the recoveries team closes an earlier quarter off, a month's settlement advice carries a
    further payment on an unauthorised-fraud case that settled in an earlier quarter. It is one of the
    advice's own detail lines, so the advice total ties to the sum of its lines; what the two readings of
    the ask differ on is the quarter the line belongs to, which is its own settlement month rather than
    the advice's. It falls on roughly a third of the unauthorised-fraud advices, across every month and
    every tier, because that is how often the team closes an earlier quarter off."""
    out = []
    for m in members:
        for (yy, mm) in months_of(MEASURED):
            r = rng("resid", m["code"], yy, mm)
            if r.random() >= 0.34:
                continue
            q_here = quarter_of(dt.date(yy, mm, 15), MEASURED)
            earlier = [u for u in unauth
                       if u["member"] == m["code"]
                       and (u["closed_date"].year, u["closed_date"].month) < (yy, mm)
                       and quarter_of(u["closed_date"], MEASURED) is not None
                       and quarter_of(u["closed_date"], MEASURED) != q_here]
            if not earlier:
                continue
            src = earlier[r.randrange(len(earlier))]
            out.append(dict(member=m["code"], advice_month=(yy, mm), cover="unauthorised fraud",
                            own_month=(src["closed_date"].year, src["closed_date"].month),
                            own_date=src["closed_date"], ref=src["ref"],
                            amount=round(r.uniform(2400.0, 31000.0), 2)))
    return out


# Closures, notifications and settlement runs are things people do at a desk, so they fall on working
# days: an out-of-hours rota closes a handful at a weekend and nothing else does. A date drawn with no
# regard to the calendar is moved inside a one-week window to the day of the week the work lands on,
# which leaves the month and the quarter it falls in exactly where they were.
WEEKDAY_WEIGHT = (1.00, 1.05, 1.02, 1.00, 1.12, 0.07, 0.05)   # Monday to Sunday


def month_bounds(d):
    first = d.replace(day=1)
    return first, (first + dt.timedelta(days=31)).replace(day=1) - dt.timedelta(days=1)


def on_a_working_day(d, r, lo=None, hi=None, span=3, keep_month=True):
    """Move d to the day of the week the work lands on, inside plus or minus span days, inside [lo, hi]
    and, where keep_month is set, inside d's own calendar month so nothing attributed by month or
    quarter moves. The window spans a whole week, so the weekday profile the move returns is
    WEEKDAY_WEIGHT itself rather than the flat one a bare date draw gives."""
    if keep_month:
        a, b = month_bounds(d)
    else:
        a, b = d - dt.timedelta(days=span), d + dt.timedelta(days=span)
    a, b = max(a, d - dt.timedelta(days=span)), min(b, d + dt.timedelta(days=span))
    if lo is not None:
        a = max(a, lo)
    if hi is not None:
        b = min(b, hi)
    if b < a:
        return d
    days = [a + dt.timedelta(days=i) for i in range((b - a).days + 1)]
    return r.choices(days, weights=[WEEKDAY_WEIGHT[x.weekday()] for x in days])[0]


def settle_closures(cases, unauth):
    """Put every case closure on the working day the handler closed it, without moving the month. The
    ask layer attributes a settled line by the month and the quarter its case closed in, so nothing it
    computes moves; the recovery credit still values strictly after the closure it belongs to, and the
    unauthorised credit stays on the same side of the pull date as it was, so no credit row appears or
    disappears. The nudge runs on its own RNG streams, so no other draw in the build shifts."""
    for c in cases:
        if c.closed_date is None:
            continue
        hi = PULL - dt.timedelta(days=1)
        if c.recovery_date is not None:
            hi = min(hi, c.recovery_date - dt.timedelta(days=1))
        c.closed_date = on_a_working_day(c.closed_date, rng("close", c.member, c.year, c.idx),
                                         lo=c.open_date + dt.timedelta(days=1), hi=hi)
    for u in unauth:
        before = u["closed_date"]
        posts = (bool(u["recovery_route"])
                 and before + dt.timedelta(days=u["recovery_offset"]) <= PULL)
        d = on_a_working_day(before, rng("uclose", u["member"], u["year"], u["idx"]),
                             lo=u["open_date"] + dt.timedelta(days=1),
                             hi=PULL - dt.timedelta(days=1))
        if (bool(u["recovery_route"])
                and (d + dt.timedelta(days=u["recovery_offset"]) <= PULL) != posts):
            d = before
        u["closed_date"] = d


def settle_notifications(cases, unauth):
    """Put the date the member recorded the case on the working day a handler recorded it. The register's
    notified date is a desk action, so it carries the working week the way the closures and the
    notification feed do. The nudge is held inside the case's own calendar month, so every month and
    quarter the returns and the ask layer attribute by is untouched, and it is clamped to sit on or
    after the payment, strictly before the case's own closure, and strictly before the fund-return
    request the fraud team raised off it.

    One set of rows keeps the date it was drawn on: a case of the ladder's own member and measured year
    whose beneficiary account was registered on or after the day the case was recorded. The date-only
    rungs and the whole window sweep read which side of a day count that difference falls on, so moving
    those rows would move rung 1, rung 2 and the sweep, and a realism pass may not buy its realism with
    the ladder. Every other row is free: a registration dated before the case is on the far side of the
    rung's test however the recorded date moves inside the month, because the nudge never takes it back
    past the payment, and no other member or year is measured.

    Each nudge runs on its own RNG stream, so no amount, lag, reference or count in the build shifts."""
    for c in cases:
        if not c.recorded or c.open_date is None:
            continue
        if (c.member == LADDER_SUBJECT and c.year == MEASURED
                and c.registration_date is not None and c.registration_date >= c.open_date):
            continue
        hi = PULL - dt.timedelta(days=1)
        if c.closed_date is not None:
            hi = min(hi, c.closed_date - dt.timedelta(days=1))
        if c.request_date is not None:
            hi = min(hi, c.request_date - dt.timedelta(days=1))
        c.open_date = on_a_working_day(c.open_date, rng("notified", c.member, c.year, c.idx),
                                       lo=c.payment_date, hi=hi)
    for u in unauth:
        u["open_raw"] = u["open_date"]
        hi = min(PULL - dt.timedelta(days=1), u["closed_date"] - dt.timedelta(days=1))
        u["open_date"] = on_a_working_day(u["open_date"],
                                          rng("unotified", u["member"], u["year"], u["idx"]),
                                          lo=u["payment_date"], hi=hi)


def volume_targets(members):
    """The level a member's book sits at in each scheme year, on its own growth path (VOLUME_PATH).
    This is where the book is, not what the return says: the return's figure is the sum of the four
    quarters the member filed (quarter_volumes), so nothing here is rounded to anything. A book's
    level is not a round number of payments either, so each year sits a little either side of the
    path, which is the measurement noise in a growth rate rather than a designed step; the six years
    the review reads an index off sit on the path itself."""
    out = {}
    for m in members:
        path = VOLUME_PATH[m["code"]]
        for i, y in enumerate(SCHEME_YEARS):
            v = m["volume"] * path[i]
            if m["joined"] > year_bounds(y)[0]:
                lo, hi = year_bounds(y)
                v *= (hi - m["joined"]).days / (hi - lo).days
            if (m["code"], y) not in PINNED_YEARS:
                v *= 1.0 + (rng("level", m["code"], y).random() - 0.5) * 0.0004
            out[(m["code"], y)] = v
    return out


def member_shape(code):
    """The member's own quarterly shape, drawn once around the industry one and held across the years."""
    r = rng("shape", code)
    raw = [s * (1.0 + (r.random() - 0.5) * 0.17) for s in INDUSTRY_SHAPE]
    tot = sum(raw)
    return [s / tot for s in raw]


def quarter_volumes(members, targets):
    """The quarters the member returns report and the year they add up to. Each quarter is drawn in
    whole payments on the member's own seasonal shape, and the annual figure is the sum of the four:
    no year is rounded and divided, so a year carries no rounding of its own and the roundness of a
    quarter is the roundness of a drawn whole number. The six PINNED_YEARS are the exception, because
    the review reads an index off them: there the member's largest quarter carries the difference, at
    most a few tens of payments, so the four still sum to the total the review quotes."""
    qout, annual = {}, {}
    for m in members:
        shape = member_shape(m["code"])
        for y in SCHEME_YEARS:
            target = targets[(m["code"], y)]
            r = rng("qv", m["code"], y)
            weights = [s * (1.0 + (r.random() - 0.5) * 0.04) for s in shape]
            scale = target / sum(weights)
            parts = [int(round(x * scale)) for x in weights]
            if (m["code"], y) in PINNED_YEARS:
                pin = int(round(target / 100.0) * 100)
                parts[parts.index(max(parts))] += pin - sum(parts)
            for i, (a, b) in enumerate(_quarters(y)):
                qout[(m["code"], y, i + 1)] = parts[i]
            annual[(m["code"], y)] = sum(parts)
    return qout, annual


def _quarters(y):
    a = int(y.split("/")[0])
    return [(dt.date(a, 4, 1), dt.date(a, 6, 30)), (dt.date(a, 7, 1), dt.date(a, 9, 30)),
            (dt.date(a, 10, 1), dt.date(a, 12, 31)), (dt.date(a + 1, 1, 1), dt.date(a + 1, 3, 31))]


def quarter_of(d, y):
    for i, (a, b) in enumerate(_quarters(y)):
        if a <= d <= b:
            return i + 1
    return None


def world():
    import pack
    members = build_members()
    cases = build_cases(members)
    # case references: the claims system allocates one per case from its own block per member and
    # scheme year, so they are unique. Drawn without replacement rather than at random, because a
    # duplicate reference would merge two cases in every file that joins on it.
    for m in members:
        for y in SCHEME_YEARS:
            mine = [c for c in cases if c.member == m["code"] and c.year == y and c.recorded]
            r = rng("ref", m["code"], y)
            for c, n in zip(mine, r.sample(range(10000, 99999), len(mine))):
                c.case_ref = "%s-%s-%05d" % (m["code"].split("-")[1], y.replace("/", ""), n)
    for m in members:
        if m["target"] is not None:
            est = realised_estimate(cases, m["code"])
            m["volume"] = round(est / m["target"] * 1e6 / 100.0) * 100
    targets = volume_targets(members)
    qvols, vols = quarter_volumes(members, targets)
    unauth = pack.unauthorised_cases(members)
    # closures land on the working day the handler closed them, inside their own month, before the
    # prior-period adjustments are keyed off the closure months; the recorded dates follow, clamped
    # against the closures the step above has just set
    settle_closures(cases, unauth)
    settle_notifications(cases, unauth)
    adjustments = build_adjustments(members, unauth)
    return dict(members=members, cases=cases, volumes=vols, quarter_volumes=qvols, unauth=unauth,
                adjustments=adjustments,
                by_code={m["code"]: m for m in members})


if __name__ == "__main__":
    w = world()
    cg = [c for c in w["cases"] if c.member == "KM-104" and c.year == MEASURED]
    rec = [c for c in cg if c.recorded]
    ind = [c for c in cg if c.independent_reg]
    both = [c for c in cg if c.independent_reg and c.recorded]
    selfreg = [c for c in cg if c.self_reg_date is not None]
    matched = [c for c in cg if c.matched]
    print("Castlegate %s: true %d, recorded %d, independent %d, both %d, self-produced %d, matched %d"
          % (MEASURED, len(cg), len(rec), len(ind), len(both), len(selfreg), len(matched)))
    vol = w["volumes"][("KM-104", MEASURED)]
    naive = len(rec) * len(matched) / len([c for c in matched if c.recorded])
    gold = len(rec) * len(ind) / len(both)
    print("volume %d, naive %.2f cases %.2f per million, golden %.2f cases %.2f per million"
          % (vol, naive, naive / vol * 1e6, gold, gold / vol * 1e6))
