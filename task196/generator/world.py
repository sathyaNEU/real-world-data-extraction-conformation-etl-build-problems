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

# ---------------------------------------------------------------------------
# Members. The review group is the third of the membership whose triennial review falls this cycle.
# Volumes for the review group are derived in build_members() so each one's index lands mid-bin.
# ---------------------------------------------------------------------------
MEMBERS = [
    # code, name, tier, joined, review group, true cases 2026/27, member coverage, scheme coverage,
    # registration rate after a request, target index (review group only)
    ("KM-104", "Castlegate Payments",  "B", dt.date(2016, 4, 1),  True,  690, 400 / 690, 207 / 690, 0.850, 30.94),
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
            s_set = set(order[:n_s])                      # independently registered accounts
            rest = order[n_s:]
            in_both = order[:both]                        # recorded and independently registered
            m_set = set(in_both) | set(rest[:n_m - both])  # recorded
            # report lag: a case is opened when the customer or the monitoring finds it. Cases on
            # already-reported accounts are found the same way as any other.
            for i in sorted(m_set):
                c = group[i]
                c.recorded = True
                # most cases surface inside the recall window, the slow ones (investment and romance
                # scams, where the victim is strung along) long after it
                room = max(RECALL_WINDOW_DAYS + 3, (PULL - c.payment_date).days - 4)
                if r.random() < 0.72:
                    c.report_lag = r.randint(1, RECALL_WINDOW_DAYS - 1)
                else:
                    c.report_lag = r.randint(RECALL_WINDOW_DAYS + 2, min(190, room))
                c.open_date = c.payment_date + dt.timedelta(days=c.report_lag)
            for i in sorted(s_set):
                group[i].independent_reg = True
            # fund-return requests come first, because where a member asked for the money back the
            # request is what the receiving firm's own registration answers. A request is only sent
            # while there is a chance of recovering the funds.
            requested = [i for i in sorted(m_set)
                         if group[i].report_lag is not None and group[i].report_lag < RECALL_WINDOW_DAYS]
            for i in requested:
                c = group[i]
                # the fraud team works a queue, so the request goes days after the case is opened
                c.request_date = c.open_date + dt.timedelta(days=r.randint(1, 5))
            # independent registration dates. An account another firm's victim reported is on the
            # register before this member ever asks about it: for a case inside the recall window the
            # registration lands before the member's own request, either before the case was opened or
            # in the days between the case and the request going out.
            for i in sorted(s_set):
                c = group[i]
                if c.request_date is not None:
                    room = (c.request_date - c.open_date).days
                    if room >= 2 and r.random() < 0.45:
                        c.independent_reg_date = c.open_date + dt.timedelta(days=r.randint(0, room - 1))
                    else:
                        c.independent_reg_date = c.open_date - dt.timedelta(days=r.randint(1, 95))
                elif c.recorded:
                    ahead = max(1, min(190, (PULL - c.open_date).days - 2))
                    if r.random() < 0.62:
                        c.independent_reg_date = c.open_date + dt.timedelta(days=r.randint(1, ahead))
                    else:
                        c.independent_reg_date = c.open_date - dt.timedelta(days=r.randint(1, 120))
                else:
                    ahead = max(2, min(210, (PULL - c.payment_date).days - 2))
                    c.independent_reg_date = c.payment_date + dt.timedelta(days=r.randint(2, ahead))
            # the receiving firm registers the account because of the request, for a share of the
            # requests on accounts nobody else had reported
            candidates = [i for i in requested if not group[i].independent_reg]
            r.shuffle(candidates)
            want = round((n_m - both) * m["q"])
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


def volumes(members):
    """Payments sent per member per scheme year, in whole payments."""
    out = {}
    for m in members:
        for y in SCHEME_YEARS:
            growth = {"2023/24": 0.78, "2024/25": 0.86, "2025/26": 0.93, "2026/27": 1.00}[y]
            v = m["volume"] * growth
            if m["joined"] > year_bounds(y)[0]:
                lo, hi = year_bounds(y)
                v *= (hi - m["joined"]).days / (hi - lo).days
            out[(m["code"], y)] = int(round(v / 100.0) * 100)
    return out


def quarter_volumes(members, vols):
    """The quarterly split the member returns report, with a real seasonal shape."""
    shape = [0.238, 0.244, 0.263, 0.255]
    out = {}
    for m in members:
        for y in SCHEME_YEARS:
            tot = vols[(m["code"], y)]
            r = rng("qv", m["code"], y)
            parts = []
            for i, s in enumerate(shape):
                jitter = 1.0 + (r.random() - 0.5) * 0.04
                parts.append(int(round(tot * s * jitter / 10.0) * 10))
            parts[-1] = tot - sum(parts[:-1])
            for i, (a, b) in enumerate(_quarters(y)):
                out[(m["code"], y, i + 1)] = parts[i]
    return out


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
    vols = volumes(members)
    qvols = quarter_volumes(members, vols)
    unauth = pack.unauthorised_cases(members)
    return dict(members=members, cases=cases, volumes=vols, quarter_volumes=qvols, unauth=unauth,
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
