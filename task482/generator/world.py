"""The world behind task482's pack: Lumenfold Learning's 58 partner districts, their 2025-26 order forms, their
students, and the spring 2026 Lumenfold Science Outcomes Assessment's design. Deterministic from SEED.

The districts are 58 of 200 design-time candidates (POOL), chosen with their guarantee benchmarks so that every
district sits at least 4 points of share from its benchmark under every member of the golden family, and each wrong
route (the contractor's plausible values averaged by district, expected a posteriori and maximum likelihood counts,
test characteristic curve inversions, the golden model's expected a posteriori count) files its own wrong set; the
measurements are in the design note and checks.py asserts them on the shipped files."""
import datetime as dt
import itertools

import numpy as np

SEED = 48211
Q = np.round(np.arange(-4.475, 4.4751, 0.05), 4)        # cell midpoints; every cut is a cell boundary
GRADES = (6, 7, 8)
GRADE_MU = np.array([-0.35, 0.05, 0.45])
CUT_THETA = np.array([0.0, 0.4, 0.8])                    # Proficient: 500, 520, 540 on the reporting scale
CUT_SCALE = (500, 520, 540)
SCALE_A, SCALE_B = 500.0, 50.0                           # scale score = 500 + 50 theta
N_MOD, N_ITEM = 8, 5
FORMS = list(itertools.combinations(range(N_MOD), 2))    # 28 forms, two modules each
STATES = ("NC", "OH", "GA", "TN", "CO", "AZ")
STATE_NAME = {"NC": "North Carolina", "OH": "Ohio", "GA": "Georgia", "TN": "Tennessee", "CO": "Colorado",
              "AZ": "Arizona"}
NPOOL = 200
VENDOR_SEED = 4826                                       # the contractor's plausible-value draws

# the 58 partner districts (candidate numbers in POOL) and each one's guarantee benchmark, per cent
SELECT = [2, 8, 19, 23, 28, 34, 39, 42, 44, 45, 48, 55, 56, 59, 60, 63, 64, 65, 66, 67, 73, 77, 81, 85, 89, 91, 92,
          98, 104, 106, 108, 110, 112, 113, 115, 116, 126, 129, 130, 132, 133, 138, 140, 141, 153, 154, 156, 160, 165,
          166, 167, 168, 169, 170, 173, 174, 190, 192]
BENCH = [25, 12, 34, 19, 28, 35, 35, 15, 33, 31, 17, 30, 30, 12, 22, 26, 27, 15, 26, 15, 28, 29, 35, 28, 34, 34, 31,
         24, 12, 23, 32, 31, 24, 14, 32, 17, 12, 13, 29, 25, 18, 26, 16, 28, 13, 27, 26, 29, 33, 17, 19, 22, 17, 20, 19,
         18, 27, 17]

NAMES = ['Malvermoor', 'Falrickwood', 'Merberstead', 'Malrowwell', 'Branlinvale', 'Calnormere', 'Peldleford',
         'Pellenwick', 'Valdlewick', 'Lorleyford', 'Lorleywell', 'Belwinwell', 'Talsenford', 'Bransenwell',
         'Malwinmont', 'Havleymoor', 'Branleymoor', 'Darmerford', 'Delrickmoor', 'Saltinmere', 'Belberbury',
         'Garterfield', 'Torlanvale', 'Dunganmere', 'Lorlenstead', 'Salnormere', 'Havwinmont', 'Merganwick',
         'Corlengate', 'Merleywick', 'Dardlestead', 'Torsenford', 'Saldledale', 'Pelrickbury', 'Dunrenmont',
         'Faldlewood', 'Havdenstead', 'Tortinfield', 'Marrickmere', 'Corrowbury', 'Alrickvale', 'Delmanwick',
         'Balrickwood', 'Dundlewood', 'Alrickwood', 'Lanmerwell', 'Valsenstead', 'Haltinmont', 'Delrowfield',
         'Fenwinmoor', 'Calleyfield', 'Corlinbury', 'Fenrickgate', 'Kelnorfield', 'Fenlenbury', 'Balterdale',
         'Alrowvale', 'Keltervale']

PEOPLE = {"requester": "Amy Hardin", "efficacy": "Robert Meyers", "controller": "Barbara Frazier"}
ORG = "Lumenfold Learning, Inc."
CONTRACTOR = "Caldrith Assessment Partners"


def items():
    r = np.random.default_rng(SEED + 1)
    a = np.round(np.clip(r.lognormal(-0.05, 0.25, (N_MOD, N_ITEM)), 0.55, 2.0), 3)
    b = np.round(np.clip(r.normal(0.30, 0.85, (N_MOD, N_ITEM)), -2.0, 2.5), 3)
    return a, b


A, B = items()


def pool():
    """Candidate districts: state, size (rostered students), background shares, prior level, district effect.
    Types: ordinary; strong background with weak implementation (A); weak background with strong implementation (B);
    very low achievement (C)."""
    r = np.random.default_rng(SEED + 2)
    kinds = np.array(["ord"] * 90 + ["A"] * 40 + ["B"] * 40 + ["C"] * 30)
    n = len(kinds)
    st = np.array([STATES[i] for i in r.integers(0, 6, n)])
    rostered = np.round(np.exp(r.uniform(np.log(300), np.log(1010), n))).astype(int)
    ed = r.uniform(0.15, 0.90, n); el = r.uniform(0.02, 0.30, n)
    prior = r.normal(0, 0.40, n) - 0.7 * (ed - 0.5)
    delta = r.normal(0, 0.30, n)
    a = kinds == "A"; b = kinds == "B"; c = kinds == "C"
    ed[a] = r.uniform(0.10, 0.35, a.sum()); prior[a] = r.uniform(0.35, 0.85, a.sum()); delta[a] = r.uniform(-0.75, -0.50, a.sum())
    ed[b] = r.uniform(0.65, 0.92, b.sum()); prior[b] = r.uniform(-0.85, -0.35, b.sum()); delta[b] = r.uniform(0.50, 0.75, b.sum())
    ed[c] = r.uniform(0.70, 0.95, c.sum()); prior[c] = r.uniform(-1.00, -0.50, c.sum()); delta[c] = r.uniform(-0.35, 0.05, c.sum())
    return dict(state=st, rostered=rostered, ed=ed, el=el, prior=prior, delta=delta, kind=kinds)


POOL = pool()


def students(d):
    """Every rostered student of candidate district d with their true achievement and eligibility."""
    r = np.random.default_rng(SEED * 10 + d)
    n = POOL["rostered"][d]
    g = r.integers(0, 3, n)
    ed = (r.random(n) < POOL["ed"][d]).astype(np.int8)
    el = (r.random(n) < POOL["el"][d]).astype(np.int8)
    iep = (r.random(n) < 0.13).astype(np.int8)
    z = POOL["prior"][d] + r.normal(0, 1, n)
    band = np.digitize(z, [-0.8, 0.0, 0.8]).astype(np.int8)
    band = np.where(r.random(n) < 0.05, 4, band).astype(np.int8)        # 4 = no prior score
    theta = GRADE_MU[g] + 0.55 * z - 0.20 * ed - 0.30 * el - 0.40 * iep + POOL["delta"][d] + r.normal(0, 0.50, n)
    eligible = r.random(n) < 0.88
    tested = r.random(n) < np.where(eligible, 0.92, 0.80)
    form = r.integers(0, len(FORMS), n)
    u = r.random((n, 2, N_ITEM))
    return dict(g=g, ed=ed, el=el, iep=iep, z=z, band=band, theta=theta, eligible=eligible, tested=tested,
                form=form, u=u)


def responses(s):
    """Scored responses (n x 2 x 5) for the student's two modules, from the shipped parameters."""
    mods = np.array([FORMS[f] for f in s["form"]])
    aa = A[mods]; bb = B[mods]
    p = 1.0 / (1.0 + np.exp(-aa * (s["theta"][:, None, None] - bb)))
    return (s["u"] < p).astype(np.int8), mods


def _districts():
    """The partner districts' identities and order-form terms."""
    r = np.random.default_rng(SEED + 7)
    out = []
    style = {"NC": ("{} County Schools", "{} City Schools"),
             "OH": ("{} Local School District", "{} City School District", "{} Exempted Village School District"),
             "GA": ("{} County School District", "{} City Schools"),
             "TN": ("{} County Schools", "{} City Schools", "{} Special School District"),
             "CO": ("{} School District RE-{}", "{} School District {}"),
             "AZ": ("{} Unified School District", "{} Elementary School District")}
    numbers = r.permutation(np.arange(1012, 1012 + 3 * len(SELECT)))[:len(SELECT)]
    accounts = r.permutation(np.arange(204100, 204100 + 40 * len(SELECT), 7))[:len(SELECT)]
    for j, d in enumerate(SELECT):
        st = POOL["state"][d]
        forms = style[st]
        f = forms[int(r.integers(len(forms)))]
        name = f.format(NAMES[j], int(r.integers(1, 12))) if "{}" in f[3:] else f.format(NAMES[j])
        rostered = int(POOL["rostered"][d])
        seats = int(np.ceil(rostered * r.uniform(1.05, 1.25) / 50.0) * 50)
        price = float(np.round(r.uniform(14.0, 22.0) * 2) / 2)     # whole half dollars: every credit a whole cent
        aug = r.random() < 0.35
        out.append(dict(
            j=j, pool=d, partner_id="LD-%d" % numbers[j], name=name, short=NAMES[j], state=st,
            rostered=rostered, seats=seats, seat_price=price, fee=round(seats * price, 2),
            term_start=dt.date(2025, 8, 1) if aug else dt.date(2025, 7, 1),
            term_end=dt.date(2026, 7, 31) if aug else dt.date(2026, 6, 30),
            billing="Two semester instalments" if r.random() < 0.4 else "Annual",
            pd_hours=int(r.choice([6, 9, 12, 12, 15, 18, 24])),
            benchmark=float(BENCH[j]),
            credit_pct=int(r.choice([10, 10, 15, 15, 20], p=[0.2, 0.2, 0.2, 0.2, 0.2])),
            account="C-%d" % accounts[j],
            order_form="OF-2526-%04d" % (3101 + 7 * j),
            signed=dt.date(2025, 3, 3) + dt.timedelta(days=int(r.integers(0, 110))),
        ))
    # a second customer account (the district's virtual academy) for six districts
    for j in sorted(r.choice(len(SELECT), 6, replace=False)):
        out[j]["va_account"] = "C-%d" % (int(out[j]["account"][2:]) + 100000)
    return out


DISTRICTS = _districts()
