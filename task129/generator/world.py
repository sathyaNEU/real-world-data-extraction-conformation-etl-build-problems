"""the network: districts, substations, circuits, trim units (about half a mile of overhead primary each), the poles
and spans along them, the trees standing within falling distance of each span, and the members each district serves"""
from datetime import date, timedelta

import numpy as np
import pandas as pd

import params as P


def _beta(rng, mean, conc, size=None):
    a = max(mean * conc, 0.05)
    b = max((1 - mean) * conc, 0.05)
    return rng.beta(a, b, size)


def network(rng):
    """trim units in their circuits, each with its miles, its woodland (trees within falling distance per mile) and the
    share of those trees that are ash; units grouped on circuits that share a substation and its woodland"""
    rows = []
    for d in P.DISTRICTS:
        subs = P.SUBSTATIONS[d]
        n_units = int(round(P.MILES[d] / P.UNIT_MILES))
        n_circ = int(round(n_units / P.UNITS_PER_CIRCUIT))
        sizes = rng.multinomial(n_units - 18 * n_circ, np.ones(n_circ) / n_circ) + 18
        k = 0
        for c in range(n_circ):
            sub_i = c % len(subs)
            feeder = c // len(subs) + 1
            circuit = "%s%d-%02d" % (P.DCODE[d], sub_i + 1, feeder)
            wood = float(np.exp(rng.normal(np.log(62), 0.2)))            # trees within falling distance per mile
            ash_c = float(_beta(rng, P.ASH_MEAN[d], 60.0))
            pole = 100 + int(rng.integers(0, 40))
            for s in range(sizes[c]):
                mi = float(np.clip(rng.lognormal(np.log(P.UNIT_MILES), 0.32), 0.14, 1.25))
                n_sp = max(3, int(round(mi * P.SPANS_PER_MILE + rng.normal(0, 0.8))))
                rows.append(dict(district=d, substation=subs[sub_i], circuit=circuit, seq=s + 1, miles=mi,
                                 wood=wood * float(np.exp(rng.normal(0, 0.25))),
                                 ash=float(np.clip(_beta(rng, ash_c, 3.2), 0.0, 0.92)),
                                 first_pole=pole, n_spans=n_sp))
                pole += n_sp
                k += 1
    U = pd.DataFrame(rows)
    for d in P.DISTRICTS:                     # the register's miles total each district's overhead primary
        m = U.district == d
        U.loc[m, "miles"] = U.loc[m, "miles"] * P.MILES[d] / U.loc[m, "miles"].sum()
    U["unit_id"] = [f"{c}-{s:03d}" for c, s in zip(U.circuit, U.seq)]
    U["in_service"] = date(1968, 1, 1)
    U["retired"] = None
    U["retire_reason"] = ""
    U["replaced_by"] = ""
    U["planned"] = False
    return U.reset_index(drop=True)


def energised(U):
    """the date each circuit was energised, from the cooperative's construction records, and the later extensions
    that lengthened a circuit (drawn apart from the network so nothing downstream moves)"""
    rng = np.random.default_rng(P.SEED + 73)
    U = U.copy()
    built = {}
    for c in sorted(U.circuit.unique()):
        y = int(rng.integers(1946, 1993))
        built[c] = date(y, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
    dates = []
    for c, seq in zip(U.circuit, U.seq):
        d = built[c]
        if rng.random() < 0.15:                                 # an extension built after the circuit
            y = min(d.year + int(rng.integers(2, 26)), 2009)
            d = date(y, int(rng.integers(1, 13)), int(rng.integers(1, 29)))
        dates.append(d)
    U["in_service"] = dates
    return U


def changes(U, rng):
    """lines rebuilt in 2024 (the old unit retired, a new unit number in service weeks later), units converted to
    underground from 2021 to 2025, and conversions already scheduled for 2026"""
    U = U.copy()
    n = len(U)
    order = rng.permutation(n)
    rebuilt = order[:int(0.016 * n)]
    conv = order[int(0.016 * n):int(0.028 * n)]
    plan26 = order[int(0.028 * n):int(0.036 * n)]
    new_rows = []
    for i in rebuilt:
        r = U.loc[i]
        out_d = date(2024, 2, 1) + timedelta(days=int(rng.integers(0, 280)))
        in_d = out_d + timedelta(days=int(rng.integers(12, 55)))
        new_seq = 500 + int(r.seq)
        new_id = f"{r.circuit}-{new_seq:03d}"
        U.at[i, "retired"] = out_d
        U.at[i, "retire_reason"] = "REBUILT"
        U.at[i, "replaced_by"] = new_id
        nr = r.copy()
        nr["seq"] = new_seq
        nr["unit_id"] = new_id
        nr["miles"] = float(r.miles * rng.uniform(0.96, 1.04))
        nr["in_service"] = in_d
        nr["retired"] = None
        nr["retire_reason"] = ""
        nr["replaced_by"] = ""
        nr["first_pole"] = int(r.first_pole) + 7000
        new_rows.append(nr)
    for i in conv:
        U.at[i, "retired"] = date(2021, 1, 15) + timedelta(days=int(rng.integers(0, 1780)))
        U.at[i, "retire_reason"] = "UNDERGROUND"
    for i in plan26:
        U.at[i, "retired"] = date(2026, 3, 1) + timedelta(days=int(rng.integers(0, 240)))
        U.at[i, "retire_reason"] = "UNDERGROUND"
        U.at[i, "planned"] = True
    U = pd.concat([U, pd.DataFrame(new_rows)], ignore_index=True)
    return U


def members(rng):
    """members served at the end of each year, by district"""
    rows = []
    for d in P.DISTRICTS:
        for y in range(2015, 2026):
            m = P.MEMBERS_2025[d] / (1 + P.MEMBER_GROWTH) ** (2025 - y) * float(np.exp(rng.normal(0, 0.002)))
            rows.append(dict(district=d, year=y, members=int(round(m))))
    return pd.DataFrame(rows)


SPECIES_2023 = {"ash": "FRAX", "maple": "ACER", "oak": "QUER", "pine": "PINU", "other": "OTHR"}
SPECIES_2024 = {"ash": "ASH", "maple": "MAPLE", "oak": "OAK", "pine": "PINE", "other": "OTHER"}


def survey(U, rng):
    """the forester's span survey of trees within falling distance: the 2023 survey of every unit then in service,
    and the 2024 re-survey of the rebuilt lines' new spans in the new survey app's species list"""
    rows = []
    srv_start = date(2023, 4, 3)
    for _, u in U.iterrows():
        if u.in_service > date(2023, 9, 30) and u.in_service.year < 2024:
            continue
        resurvey = u.in_service.year == 2024
        if not resurvey and u.retired is not None and u.retired < date(2023, 4, 1):
            continue
        sdate = (date(2024, 10, 7) + timedelta(days=int(rng.integers(0, 45)))) if resurvey else \
            (srv_start + timedelta(days=int(rng.integers(0, 170))))
        codes = SPECIES_2024 if resurvey else SPECIES_2023
        per_span_mi = u.miles / u.n_spans
        mix = {"ash": u.ash}
        rest = 1 - u.ash
        w = rng.dirichlet([3.0, 2.2, 2.6, 1.6])
        for k, sp in enumerate(("maple", "oak", "pine", "other")):
            mix[sp] = rest * w[k]
        prefix = u.circuit
        for s in range(u.n_spans):
            span = f"{prefix}-P{u.first_pole + s:04d}"
            lam = u.wood * per_span_mi
            for sp in ("ash", "maple", "oak", "pine", "other"):
                n = int(rng.poisson(lam * mix[sp]))
                if n:
                    rows.append((span, u.unit_id, sdate, codes[sp], n))
    S = pd.DataFrame(rows, columns=["span_id", "unit_id", "survey_date", "species_code", "trees_within_falling_distance"])
    return S


def ash_density(S, U):
    """ash trees within falling distance per mile of each unit, from its latest survey (the truth the hazard uses)"""
    ash = S[S.species_code.isin(["FRAX", "ASH"])].groupby("unit_id").trees_within_falling_distance.sum()
    allt = S.groupby("unit_id").trees_within_falling_distance.sum()
    mi = U.set_index("unit_id").miles
    return (ash.reindex(mi.index).fillna(0) / mi), (allt.reindex(mi.index).fillna(0) / mi)
