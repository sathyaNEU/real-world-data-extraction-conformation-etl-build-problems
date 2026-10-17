"""task158 world: one year of Slenk's serving fleet, hour by hour, and everything the capacity desk pulled on
7 December 2026. The simulation holds the truth (prompt tokens each request made its model compute, which no file
carries); records.py writes what each system would export, never the truth columns."""
from __future__ import annotations

import datetime as dt
import math

import numpy as np

import common as K

# ------------------------------------------------------------------------------------------------- profiles
DOCS_WEEKDAY = [0.050, 0.036, 0.030, 0.029, 0.034, 0.050, 0.100, 0.300, 0.720, 0.970, 1.000, 0.950, 0.800,
                0.880, 0.930, 0.910, 0.820, 0.600, 0.380, 0.250, 0.190, 0.150, 0.110, 0.075]
DOCS_WEEKEND = [0.040, 0.032, 0.028, 0.027, 0.028, 0.032, 0.045, 0.070, 0.110, 0.150, 0.175, 0.185, 0.180,
                0.175, 0.170, 0.165, 0.155, 0.140, 0.120, 0.105, 0.095, 0.085, 0.070, 0.052]
BATCH_HOUR = [0.62, 0.60, 0.58, 0.57, 0.58, 0.62, 0.70, 0.80, 0.90, 0.96, 1.00, 0.99, 0.95, 0.97, 0.98, 0.96,
              0.92, 0.86, 0.80, 0.75, 0.71, 0.68, 0.66, 0.64]
CHAT_HOUR = [0.42, 0.30, 0.22, 0.18, 0.17, 0.20, 0.30, 0.48, 0.64, 0.74, 0.80, 0.83, 0.85, 0.84, 0.82, 0.82,
             0.84, 0.86, 0.88, 0.93, 0.99, 1.00, 0.88, 0.65]
CODE_HOUR = [0.22, 0.17, 0.15, 0.14, 0.15, 0.18, 0.26, 0.45, 0.70, 0.86, 0.92, 0.93, 0.82, 0.88, 0.95, 1.00,
             0.99, 0.94, 0.80, 0.66, 0.56, 0.48, 0.38, 0.29]
AGENTS_HOUR = [0.24, 0.20, 0.18, 0.17, 0.18, 0.22, 0.30, 0.48, 0.74, 0.92, 0.99, 1.00, 0.90, 0.94, 0.98, 0.97,
               0.92, 0.80, 0.62, 0.50, 0.44, 0.40, 0.34, 0.28]
VOICE_HOUR = [0.30, 0.20, 0.15, 0.13, 0.14, 0.22, 0.45, 0.80, 0.97, 0.92, 0.84, 0.82, 0.86, 0.82, 0.78, 0.80,
              0.86, 0.96, 1.00, 0.97, 0.92, 0.84, 0.66, 0.46]


class World:
    pass


def _day_index(t):
    return (t.date() - K.ROLLUP_START.date()).days


def _local(t):
    return K.utc_to_ams(t)


def _is_off(d):
    return d.weekday() >= 5 or d in K.NL_HOLIDAYS


def _season(d):
    """Enterprise usage dips in the summer holidays and in the week after Christmas."""
    if d.month == 7:
        return 0.88
    if d.month == 8:
        return 0.84 if d.day < 22 else 0.92
    return 1.0


def _lc2_share(t):
    if t < K.LC2_START:
        return 0.0
    if t >= K.LC2_END:
        return 1.0
    return (t - K.LC2_START).total_seconds() / (K.LC2_END - K.LC2_START).total_seconds()


# ------------------------------------------------------------------------------------------------- Docs organisations
ORG_NAMES = [
    "Hollmann & Kroes Advocaten", "Wierdsma Assurantiën", "Veldkamp Aerts Accountants", "Notariskantoor Ommeren",
    "Noordkust Zorgverzekeringen", "Haverkamp Logistiek", "Brinkhorst Vastgoedbeheer", "Kuijpers Medische Groothandel",
    "Thuiszorg Achterweide", "Van Rijckevorsel Pensioenbeheer", "Gerritsma Schadeverzekeringen", "Lubbers Elzinga Advocaten",
]


def _org_ids(rng, n):
    alphabet = "23456789ABCDEFGHJKMNPQRSTVWXYZ"
    out, seen = [], set()
    while len(out) < n:
        s = "org-" + "".join(alphabet[i] for i in rng.integers(0, len(alphabet), 8))
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out


ORG_SUFFIX = ["Advocaten", "Accountants", "Notarissen", "Belastingadviseurs", "Makelaars", "Assurantiën",
              "Ingenieurs", "Adviesgroep", "Vermogensbeheer", "Juristen", "Bouwadvies", "Registeraccountants"]
ORG_STEMS = [
    "Aalders", "Alblas", "Altena", "Arendsen", "Bakhuis", "Beekman", "Bergsma", "Bierens", "Blankert", "Boelens",
    "Brakel", "Bredius", "Buitenhuis", "Callenbach", "Coenraads", "Diepenbrock", "Doornbos", "Duinkerken", "Eijsink",
    "Elshout", "Everaars", "Feenstra", "Fokkema", "Gaasbeek", "Geertsema", "Goedhart", "Haagsma", "Halbertsma",
    "Hartsuiker", "Hekman", "Hilbrink", "Hofstede", "Holtrop", "Huizinga", "IJzerman", "Jellema", "Joustra",
    "Kamphuis", "Kempenaar", "Leeuwenburgh", "Lindhout", "Looman", "Luitjes", "Maassen", "Meekes", "Meinsma", "Nauta",
    "Nijboer", "Noordhoek", "Oldenkamp", "Oosterhof", "Overdijk", "Pander", "Plomp", "Quint", "Reitsma", "Rijkens",
    "Rozema", "Schaafsma", "Siersema", "Sloots", "Smeenk", "Spanjaard", "Steenbeek", "Stuiver", "Talsma", "Terpstra",
    "Tiemersma", "Tuinstra", "Uittenbogaard", "Valkema", "Veenhoven", "Vledder", "Wassink", "Weijers", "Westerhof",
    "Wiersma", "Wijnstra", "Witteveen", "Zandstra", "Zijlstra",
]


def _org_names(rng, n):
    """The rest of Docs' enterprise customers: two partners' names and a line of business, the way Dutch firms and
    practices are named."""
    names, seen = list(ORG_NAMES), set(ORG_NAMES)
    while len(names) < n:
        a, b = rng.choice(len(ORG_STEMS), size=2, replace=False)
        suffix = ORG_SUFFIX[int(rng.integers(0, len(ORG_SUFFIX)))]
        joint = " & " if rng.random() < 0.45 else " "
        nm = ORG_STEMS[a] + joint + ORG_STEMS[b] + " " + suffix
        if nm not in seen:
            seen.add(nm)
            names.append(nm)
    return names


def build_orgs(rng, n=160):
    O = World()
    O.n = n
    O.ids = _org_ids(rng, n)
    O.names = _org_names(rng, n)
    w = np.exp(rng.normal(0.0, 1.05, n))
    O.weight = w / w.sum()
    O.doc = np.clip(np.exp(rng.normal(math.log(17000), 0.33, n)), 5200, 52000)
    O.turns = rng.uniform(4.2, 5.9, n)
    O.answer = rng.uniform(300, 385, n)
    O.question = rng.uniform(95, 150, n)
    O.api_share = np.clip(rng.beta(1.6, 4.0, n), 0.02, 0.85)
    O.start = np.zeros(n, dtype=int)          # day index the org's usage begins (a few join during the year)
    late = rng.choice(np.arange(12, n), size=14, replace=False)
    O.start[late] = rng.integers(20, 300, size=14)
    O.sys = 1100.0
    return O


# ------------------------------------------------------------------------------------------------- the simulation
def simulate():
    rng = np.random.default_rng(K.SEED)
    W = World()
    W.hours = K.hours()
    H = len(W.hours)
    W.H = H
    W.local = [_local(t) for t in W.hours]
    W.lc2 = np.array([_lc2_share(t) for t in W.hours])
    days = np.array([_day_index(t) for t in W.hours])
    W.day = days

    # --- Docs interactive, organisation by organisation
    O = build_orgs(np.random.default_rng(K.SEED + 1))
    W.orgs = O
    prof = np.array([(DOCS_WEEKEND if _is_off(l.date()) else DOCS_WEEKDAY)[l.hour] for l in W.local])
    seas = np.array([_season(l.date()) for l in W.local])
    growth = np.exp(0.00128 * days)
    base_sessions = 128800.0
    org_rng = np.random.default_rng(K.SEED + 2)
    S = np.zeros((O.n, H))
    R = np.zeros((O.n, H))
    C = np.zeros((O.n, H))
    P = np.zeros((O.n, H))
    Q = np.zeros((O.n, H))
    for o in range(O.n):
        active = (days >= O.start[o]).astype(float)
        jitter = np.exp(org_rng.normal(0.0, 0.035, H))
        s = base_sessions * O.weight[o] * prof * seas * growth * active * jitter
        k = O.turns[o] * np.exp(org_rng.normal(0.0, 0.012, H))
        docv = O.doc[o] * np.exp(org_rng.normal(0.0, 0.03, H))
        r = s * k
        first = O.sys + docv + O.question[o]
        C[o] = s * first + (r - s) * O.question[o]
        P[o] = s * (k * first + (O.question[o] + O.answer[o]) * k * (k - 1) / 2.0)
        Q[o] = r * O.answer[o] * np.exp(org_rng.normal(0.0, 0.01, H))
        S[o], R[o] = s, r
    W.docs_org = dict(S=S, R=R, C=C, P=P, Q=Q)

    # --- the early-access tenant's report calls (organisation 10 in the list: Gerritsma Schadeverzekeringen)
    W.pilot_org = 10
    pr = np.random.default_rng(K.SEED + 3)
    rep = np.zeros(H)
    for i, l in enumerate(W.local):
        d = l.date()
        if d < K.PILOT_START or _is_off(d) or d in K.PILOT_PAUSE or not (7 <= l.hour < 19):
            continue
        wk = (d - K.PILOT_START).days // 7
        ramp = 0.24 if wk == 0 else (0.62 if wk == 1 else 1.0)
        shape = [0.70, 0.92, 1.08, 1.18, 1.16, 0.96, 1.02, 1.12, 1.10, 1.00, 0.86, 0.66][l.hour - 7]
        rep[i] = 112.0 * ramp * shape * math.exp(pr.normal(0.0, 0.05))
    reports = np.floor(rep + pr.random(H))
    calls = reports * 6
    # each call's prompt is its own source pack plus the section brief; completion grows a little with the pack
    p_call = np.where(calls > 0, 19800 * np.exp(pr.normal(0.0, 0.012, H)), 0.0)
    q_call = np.where(calls > 0, 1350 * (p_call / 19800) ** 0.35 * np.exp(pr.normal(0.0, 0.004, H)), 0.0)
    W.pilot = dict(reports=reports, calls=calls, prompt=calls * p_call, completion=calls * q_call)

    # --- Batch API (lc1, then lc2), every request one call
    br = np.random.default_rng(K.SEED + 4)
    bprof = np.array([BATCH_HOUR[l.hour] * (0.74 if l.weekday() >= 5 else 1.0) for l in W.local])
    bgrowth = np.exp(0.00095 * days)
    breq = 118000.0 * bprof * bgrowth * np.exp(br.normal(0.0, 0.03, H))
    day_p = np.exp(br.normal(0.0, 0.06, days.max() + 1))[days]
    day_q = np.exp(br.normal(0.0, 0.10, days.max() + 1))[days]
    hp = np.array([8600 if 7 <= l.hour < 19 else 6100 for l in W.local], dtype=float)
    hq = np.array([430 if 7 <= l.hour < 19 else 360 for l in W.local], dtype=float)
    bp = hp * day_p * np.exp(br.normal(0.0, 0.04, H))
    bq = hq * day_q * np.exp(br.normal(0.0, 0.05, H))
    W.batch = dict(R=breq, P=breq * bp, Q=breq * bq)

    # --- the other pools: requests, sessions, prompt sent and computed, completion
    W.other = {}
    spec = {   # pool: hour profile, base requests at the busiest hour in January, daily growth, turns per session,
        #          prompt sent, share computed, completion, weekend factor
        "chat-prod": (CHAT_HOUR, 5.10e6, 0.00105, 6.1, 2900, 0.36, 310, 1.06),
        "code-prod": (CODE_HOUR, 1.72e6, 0.00142, 38.0, 6500, 0.18, 95, 0.42),
        "agents-prod": (AGENTS_HOUR, 1.144e6, 0.00118, 14.0, 21000, 0.11, 420, 0.55),
        "voice-prod": (VOICE_HOUR, 4.15e6, 0.00098, 9.0, 1600, 0.50, 85, 0.93),
    }
    for k_, (hp_, base, gr, turns, sent, share, comp, wkend) in spec.items():
        rr = np.random.default_rng(K.SEED + 10 + K.POOLS.index(k_))
        pr_ = np.array([hp_[l.hour] * (wkend if _is_off(l.date()) else 1.0) for l in W.local])
        req = base * pr_ * np.exp(gr * days) * np.exp(rr.normal(0.0, 0.025, H))
        if k_ == "code-prod":   # the IDE agent preview from 14 September lifts code requests
            req = req * np.where(days >= (dt.date(2026, 9, 14) - K.ROLLUP_START.date()).days, 1.10, 1.0)
        sv = sent * np.exp(rr.normal(0.0, 0.03, H))
        sh = share * np.exp(rr.normal(0.0, 0.02, H))
        cv = comp * np.exp(rr.normal(0.0, 0.03, H))
        W.other[k_] = dict(R=req, S=req / (turns * np.exp(rr.normal(0.0, 0.02, H))), P=req * sv, C=req * sv * sh,
                           Q=req * cv)

    # --- busy GPU-seconds, the truth of what each pool's GPUs did
    nr = np.random.default_rng(K.SEED + 20)
    W.busy = {}
    a = (1 - W.lc2) * K.A_LC1 + W.lc2 * K.A_LC2
    b = (1 - W.lc2) * K.B_LC1 + W.lc2 * K.B_LC2
    docs_C = C.sum(axis=0) + W.pilot["prompt"]
    docs_Q = Q.sum(axis=0) + W.pilot["completion"]
    W.busy["docs-prod"] = (a * docs_C + b * docs_Q) * np.exp(nr.normal(0.0, 0.004, H))
    W.busy["batch-prod"] = (a * W.batch["P"] + b * W.batch["Q"]) * np.exp(nr.normal(0.0, 0.004, H))
    model = {"chat-prod": "l3", "agents-prod": "l3", "code-prod": "c2", "voice-prod": "s2rt"}
    for k_, d_ in W.other.items():
        ca, cb = K.COST[model[k_]]
        W.busy[k_] = (ca * d_["C"] + cb * d_["Q"]) * np.exp(nr.normal(0.0, 0.004, H))
    W.docs_C, W.docs_Q = docs_C, docs_Q
    return W


def pool_totals(W):
    """The rollup's counters for every pool and hour (requests, new sessions, prompt and completion tokens), as floats."""
    S, R, P, Q = (W.docs_org[x].sum(axis=0) for x in ("S", "R", "P", "Q"))
    out = {"docs-prod": dict(R=R + W.pilot["calls"], S=S + W.pilot["calls"], P=P + W.pilot["prompt"],
                             Q=Q + W.pilot["completion"]),
           "batch-prod": dict(R=W.batch["R"], S=W.batch["R"], P=W.batch["P"], Q=W.batch["Q"])}
    for k_, d_ in W.other.items():
        out[k_] = dict(R=d_["R"], S=d_["S"], P=d_["P"], Q=d_["Q"])
    return out


# ------------------------------------------------------------------------------------------------- Q1 intake and plan
def q1_intake():
    """Busiest-hour requests per ISO week, 2027-W01 to W13, as each product team filed them (thousands; Voice files
    requests per second at the busiest hour). The teams' own paths, not a formula: steps where they expect them."""
    return {
        "chat-prod": [7690, 7735, 7790, 7820, 7845, 7880, 7905, 7930, 7955, 7975, 7990, 8020, 8041],
        "code-prod": [3240, 3275, 3530, 3640, 3725, 3790, 3850, 3905, 3960, 4010, 4055, 4090, 4122],
        "agents-prod": [1905, 1930, 1955, 1985, 2010, 2035, 2060, 2080, 2100, 2120, 2140, 2155, 2168],
        "docs-prod": [1024.7, 1033.7, 1045.5, 1056.4, 1067.2, 1078.6, 1089.5, 1100.3, 1111.2, 1121.6, 1131.5, 1141.9,
                      1152.6],
        "batch-prod": [176.0, 177.5, 179.5, 181.0, 182.5, 184.0, 185.5, 187.0, 188.5, 190.0, 191.0, 192.0, 193.0],
        "voice-prod": [1676, 1680, 1684, 1687, 1690, 1693, 1696, 1699, 1701, 1703, 1705, 1707, 1708],
    }


# ------------------------------------------------------------------------------------------------- report contracts
def contracts():
    """The commitments ledger: eleven signed report-service contracts for Q1 2027, the early-access agreement and one
    proposal. Peak reports per hour are the contracted rates; Q1 reports are the volumes the customers committed."""
    rows = [
        # ref, account index, tier, contracted peak reports per hour, go-live (Monday), status, signed
        ("RC-2026-014", 0, "RL-12", 300, dt.date(2027, 1, 11), "Signed", dt.date(2026, 9, 24)),
        ("RC-2026-019", 1, "RL-12", 240, dt.date(2027, 1, 18), "Signed", dt.date(2026, 10, 8)),
        ("RC-2026-022", 2, "RL-12", 180, dt.date(2027, 2, 1), "Signed", dt.date(2026, 10, 19)),
        ("RC-2026-025", 3, "RL-12", 150, dt.date(2027, 2, 15), "Signed", dt.date(2026, 10, 27)),
        ("RC-2026-017", 4, "RM-8", 900, dt.date(2027, 1, 11), "Signed", dt.date(2026, 10, 2)),
        ("RC-2026-023", 5, "RM-8", 700, dt.date(2027, 1, 25), "Signed", dt.date(2026, 10, 21)),
        ("RC-2026-027", 6, "RM-8", 650, dt.date(2027, 2, 1), "Signed", dt.date(2026, 11, 3)),
        ("RC-2026-029", 11, "RM-8", 500, dt.date(2027, 3, 8), "Signed", dt.date(2026, 11, 12)),
        ("RC-2026-021", 7, "RS-6", 2000, dt.date(2027, 1, 11), "Signed", dt.date(2026, 10, 14)),
        ("RC-2026-030", 8, "RS-6", 1200, dt.date(2027, 2, 15), "Signed", dt.date(2026, 11, 18)),
        ("RC-2026-031", 10, "RS-6", 400, dt.date(2027, 1, 4), "Signed", dt.date(2026, 11, 24)),
        ("EA-2026-007", 10, "RS-6", 150, dt.date(2026, 10, 5), "Early access, ends 18 Dec 2026", dt.date(2026, 9, 9)),
        ("RP-2026-033", 9, "RM-8", 300, dt.date(2027, 3, 1), "Proposal sent", None),
    ]
    out = []
    for ref, acc, tier, peak, golive, status, signed in rows:
        n, pmax, qmax, price = K.TIERS[tier]
        if ref.startswith("RC"):
            wk = sum(1 for m in K.Q1_WEEKS if m >= golive)
            q1 = int(round(peak * 11.0 * 5 * wk * 0.52, -2))       # committed volume, about half the contracted peak
        elif ref.startswith("EA"):
            q1 = 0
        else:
            q1 = int(round(peak * 11.0 * 5 * 5 * 0.5, -2))
        out.append(dict(ref=ref, acc=acc, tier=tier, peak=peak, golive=golive, status=status, signed=signed,
                        q1_reports=q1, q1_calls=q1 * n))
    return out


# ------------------------------------------------------------------------------------------------- fleet nodes
NODE_COUNTS = {"chat-prod": 182, "code-prod": 83, "agents-prod": 64, "docs-prod": 76, "batch-prod": 41,
               "voice-prod": 34}


def nodes(rng):
    """The fleet's 480 nodes with their hall, rack and pool memberships through 2026. Docs gained four nodes on
    6 July, Code three on 7 September, and four Agents nodes joined Chat on 16 November."""
    out = []
    serial = 401
    halls = {"chat-prod": "ams3", "code-prod": "ams2", "agents-prod": "ams3", "docs-prod": "ams2",
             "batch-prod": "ams2", "voice-prod": "ams3"}
    rack_no = {"ams2": 3, "ams3": 2}
    for pool in K.POOLS:
        hall = halls[pool]
        for i in range(NODE_COUNTS[pool]):
            if i % 8 == 0:
                rack_no[hall] += 1
            name = "%s-g%04d" % (hall, serial + int(rng.integers(0, 3)))
            serial = int(name[-4:]) + 1
            out.append(dict(node=name, hall=hall, rack="%s-R%02d" % (hall.upper(), rack_no[hall]),
                            pool=pool, joined=dt.date(2025, 11, 3)))
    # dated changes: Docs +4 (6 Jul), Code +3 (7 Sep): those nodes joined then
    docs_nodes = [n for n in out if n["pool"] == "docs-prod"]
    for n in docs_nodes[-4:]:
        n["joined"] = dt.date(2026, 7, 6)
    code_nodes = [n for n in out if n["pool"] == "code-prod"]
    for n in code_nodes[-3:]:
        n["joined"] = dt.date(2026, 9, 7)
    for n in out:
        n["memberships"] = [(n["pool"], dt.datetime.combine(n["joined"], dt.time(9, 0)), None)]
    moved = [n for n in out if n["pool"] == "agents-prod"][-4:]
    for n in moved:
        n["memberships"] = [("agents-prod", dt.datetime.combine(n["joined"], dt.time(9, 0)), K.AGENTS_TO_CHAT),
                            ("chat-prod", K.AGENTS_TO_CHAT, None)]
        n["pool"] = "chat-prod"
    return out


def pool_of(node, t):
    for pool, start, end in node["memberships"]:
        if t >= start and (end is None or t < end):
            return pool
    return None


# ------------------------------------------------------------------------------------------------- maintenance
WAVES = {   # pool: the nights (UTC dates) of its driver rollout, nodes per night
    "batch-prod": [dt.date(2026, 10, 27), dt.date(2026, 10, 28), dt.date(2026, 10, 29), dt.date(2026, 11, 3),
                   dt.date(2026, 11, 4), dt.date(2026, 11, 7)],
    "agents-prod": [dt.date(2026, 11, 3), dt.date(2026, 11, 4), dt.date(2026, 11, 5), dt.date(2026, 11, 7),
                    dt.date(2026, 11, 10), dt.date(2026, 11, 11)],
    "chat-prod": [dt.date(2026, 11, 3), dt.date(2026, 11, 4), dt.date(2026, 11, 5), dt.date(2026, 11, 10),
                  dt.date(2026, 11, 11), dt.date(2026, 11, 12), dt.date(2026, 11, 17), dt.date(2026, 11, 18),
                  dt.date(2026, 11, 19), dt.date(2026, 11, 21), dt.date(2026, 11, 24), dt.date(2026, 11, 25),
                  dt.date(2026, 11, 26)],
    "code-prod": [dt.date(2026, 11, 10), dt.date(2026, 11, 11), dt.date(2026, 11, 12), dt.date(2026, 11, 13),
                  dt.date(2026, 11, 15)],
    "docs-prod": [dt.date(2026, 11, 10), dt.date(2026, 11, 11), dt.date(2026, 11, 12), dt.date(2026, 11, 14),
                  dt.date(2026, 11, 17), dt.date(2026, 11, 18), dt.date(2026, 11, 19)],
    "voice-prod": [dt.date(2026, 11, 24), dt.date(2026, 11, 25), dt.date(2026, 11, 26), dt.date(2026, 11, 28)],
}
# weekend-night waves (the extra night each pool's change window allowed): the first job of each failed, and its
# node waited for Monday morning
WEEKEND_FAIL = {("docs-prod", dt.date(2026, 11, 14)), ("agents-prod", dt.date(2026, 11, 7)),
                ("chat-prod", dt.date(2026, 11, 21)), ("code-prod", dt.date(2026, 11, 15)),
                ("batch-prod", dt.date(2026, 11, 7)), ("voice-prod", dt.date(2026, 11, 28))}
ENGINEERS = ["a.schrant", "m.bosch", "j.claesner", "t.groenendaal", "n.vertooren", "l.rietveld", "a.kleibrink",
             "s.cammel"]
FAIL_DETAIL = ["exit 2: nvidia-fabricmanager did not start", "exit 1: dkms build failed for 580.95.05",
               "exit 3: GPU 5 fell off the bus after reboot (Xid 79)", "exit 2: nvidia-persistenced timed out",
               "exit 1: nccl health check below floor after upgrade"]


def _next_working_morning(rng, t_utc):
    """When an engineer gets to a node an automated job left cordoned: the next working morning in Amsterdam."""
    loc = K.utc_to_ams(t_utc)
    d = loc.date()
    if loc.hour >= 8:
        d = d + dt.timedelta(days=1) if loc.hour >= 15 else d
    while d.weekday() >= 5 or d in K.NL_HOLIDAYS:
        d += dt.timedelta(days=1)
    minutes = int(rng.integers(8 * 60 + 25, 11 * 60 + 50))
    t_loc = dt.datetime.combine(d, dt.time(0, 0)) + dt.timedelta(minutes=minutes, seconds=int(rng.integers(0, 60)))
    if t_loc <= loc:
        t_loc = loc + dt.timedelta(minutes=int(rng.integers(50, 160)))
    return t_loc


def maintenance(NODES):
    """The driver rollout and the engineers' hardware work, 26 October to 6 December 2026. Returns the fleetctl job
    log, the console audit (local times), and each node's true stays out of service (UTC)."""
    rng = np.random.default_rng(K.SEED + 30)
    jobs, console, stays = [], [], []
    by_pool = {p: [n for n in NODES if n["pool"] == p or any(m[0] == p for m in n["memberships"])] for p in K.POOLS}
    job_no = 0
    for pool, nights in WAVES.items():
        members = [n for n in by_pool[pool] if pool_of(n, dt.datetime.combine(nights[0], dt.time(1, 0))) == pool
                   or pool_of(n, dt.datetime.combine(nights[-1], dt.time(1, 0))) == pool]
        order = list(rng.permutation(len(members)))
        per_night = int(math.ceil(len(members) / len(nights)))
        for k_, night in enumerate(nights):
            todo = [members[i] for i in order[k_ * per_night:(k_ + 1) * per_night]]
            todo = [n for n in todo if pool_of(n, dt.datetime.combine(night, dt.time(1, 0))) == pool]
            for j, n in enumerate(todo):
                job_no += 1
                jid = "drv580-%s-%s-%02d" % (night.strftime("%y%m%d"), pool.split("-")[0], j + 1)
                t0 = dt.datetime.combine(night, dt.time(0, 40)) + dt.timedelta(
                    minutes=int(25 * (j // 6) + rng.integers(0, 14)), seconds=int(rng.integers(0, 60)))
                ev = [dict(ts=t0, job=jid, node=n["node"], pool=pool, step="cordon", result="ok", detail="")]
                t = t0 + dt.timedelta(seconds=int(rng.uniform(180, 540)))
                if rng.random() < 0.035:
                    ev.append(dict(ts=t, job=jid, node=n["node"], pool=pool, step="drain", result="failed",
                                   detail="timeout evicting 2 pods"))
                    t = t + dt.timedelta(seconds=int(rng.uniform(60, 180)))
                    ev.append(dict(ts=t, job=jid, node=n["node"], pool=pool, step="cordon", result="ok",
                                   detail="retry"))
                    t = t + dt.timedelta(seconds=int(rng.uniform(180, 420)))
                ev.append(dict(ts=t, job=jid, node=n["node"], pool=pool, step="drain", result="ok", detail=""))
                fail = rng.random() < 0.042 or ((pool, night) in WEEKEND_FAIL and j == 0)
                if fail:
                    t = t + dt.timedelta(seconds=int(rng.uniform(540, 1800)))
                    ev.append(dict(ts=t, job=jid, node=n["node"], pool=pool, step="upgrade", result="failed",
                                   detail=FAIL_DETAIL[int(rng.integers(0, len(FAIL_DETAIL)))]))
                    back_loc = _next_working_morning(rng, t)
                    back = K.ams_to_utc(back_loc)
                    console.append(dict(local=back_loc, user=ENGINEERS[int(rng.integers(0, len(ENGINEERS)))],
                                        action="fleetctl.job.complete", obj=jid,
                                        detail="completed by hand; ran remaining step: uncordon %s" % n["node"],
                                        ticket="OPS-%05d" % int(rng.integers(48200, 49900))))
                    stays.append(dict(node=n["node"], start=t0, end=back, kind="rescue"))
                else:
                    t = t + dt.timedelta(seconds=int(rng.uniform(1080, 2040)))
                    ev.append(dict(ts=t, job=jid, node=n["node"], pool=pool, step="upgrade", result="ok",
                                   detail="580.95.05"))
                    t = t + dt.timedelta(seconds=int(rng.uniform(36, 144)))
                    ev.append(dict(ts=t, job=jid, node=n["node"], pool=pool, step="uncordon", result="ok", detail=""))
                    stays.append(dict(node=n["node"], start=t0, end=t, kind="upgrade"))
                jobs.extend(ev)
    # hardware work from the console: cordon, then uncordon once the part or the fault is dealt with
    hw = []
    for pool in K.POOLS:
        n_hw = {"chat-prod": 6, "code-prod": 3, "agents-prod": 3, "docs-prod": 4, "batch-prod": 3, "voice-prod": 3}[pool]
        for i in range(n_hw):
            day = K.NOV[0] + dt.timedelta(days=float(rng.uniform(0.6, 28.5)))
            loc = K.utc_to_ams(day).replace(hour=int(rng.integers(8, 17)), minute=int(rng.integers(0, 60)),
                                           second=int(rng.integers(0, 60)), microsecond=0)
            hours_out = float(np.exp(rng.normal(math.log(9.0), 0.75)))
            hw.append((pool, loc, hours_out))
    # two stays that run across a month end, worked by on-call
    hw.append(("voice-prod", dt.datetime(2026, 10, 31, 21, 38, 12), 9.21))
    hw.append(("code-prod", dt.datetime(2026, 11, 30, 15, 21, 40), 19.40))
    for pool, loc, h_out in hw:
        start = K.ams_to_utc(loc)
        end_loc = loc + dt.timedelta(seconds=int(round(h_out * 3600)))
        end = K.ams_to_utc(end_loc)
        busy = {s["node"] for s in stays if s["start"] < end + dt.timedelta(hours=3) and s["end"] > start - dt.timedelta(hours=3)}
        cands = [n for n in by_pool[pool] if pool_of(n, start) == pool and pool_of(n, end) == pool and n["node"] not in busy]
        n = cands[int(rng.integers(0, len(cands)))]
        u1, u2 = ENGINEERS[int(rng.integers(0, len(ENGINEERS)))], ENGINEERS[int(rng.integers(0, len(ENGINEERS)))]
        tk = "OPS-%05d" % int(rng.integers(48200, 49900))
        why = ["Xid 48 double-bit ECC on GPU %d" % int(rng.integers(0, 8)), "PSU 2 failed, replacing",
               "IB port mlx5_%d flapping" % int(rng.integers(0, 8)), "GPU %d thermal throttle, fan tray" % int(rng.integers(0, 8)),
               "NVSwitch tray reseat"][int(rng.integers(0, 5))]
        console.append(dict(local=loc, user=u1, action="node.cordon", obj=n["node"], detail=why, ticket=tk))
        console.append(dict(local=end_loc, user=u2, action="node.uncordon", obj=n["node"], detail="", ticket=tk))
        stays.append(dict(node=n["node"], start=start, end=end, kind="hardware"))
    # console noise: reboots, labels and annotations that move nothing in or out of service
    for i in range(140):
        n = NODES[int(rng.integers(0, len(NODES)))]
        loc = K.utc_to_ams(K.MAINT_WINDOW[0] + dt.timedelta(seconds=int(rng.uniform(3600, 41 * 86400))))
        act = ["node.annotate", "node.label", "node.describe", "fleetctl.job.view"][int(rng.integers(0, 4))]
        console.append(dict(local=loc, user=ENGINEERS[int(rng.integers(0, len(ENGINEERS)))], action=act,
                            obj=n["node"], detail={"node.annotate": "note added", "node.label": "label updated",
                                                   "node.describe": "", "fleetctl.job.view": ""}[act], ticket=""))
    jobs.sort(key=lambda e: (e["ts"], e["node"]))
    console.sort(key=lambda e: (e["local"], e["obj"]))
    return dict(jobs=jobs, console=console, stays=stays)


def random_cordons(NODES, rng):
    """Cordons outside the pulled window (1 January to 25 October): only the rollup's hourly samples show them."""
    out = []
    for n in NODES:
        t = K.ROLLUP_START
        while True:
            t = t + dt.timedelta(days=float(rng.exponential(55.0)))
            if t >= K.MAINT_WINDOW[0]:
                break
            t = t.replace(microsecond=0)
            d = float(np.exp(rng.normal(math.log(3.0), 1.0)))
            end = min(t + dt.timedelta(seconds=int(d * 3600)), K.MAINT_WINDOW[0] - dt.timedelta(minutes=1))
            out.append(dict(node=n["node"], start=t, end=end, kind="history"))
    return out


def in_service(NODES, stays, hours_):
    """GPUs on each pool's schedulable nodes when each hour closed (the rollup's sample)."""
    idx = {n["node"]: n for n in NODES}
    H = len(hours_)
    out = {p: np.zeros(H, dtype=int) for p in K.POOLS}
    t0 = hours_[0]
    for i, t in enumerate(hours_):
        close = t + dt.timedelta(minutes=59, seconds=59)
        for p in K.POOLS:
            out[p][i] = K.alloc_at(p, close)
    by_node = {}
    for s in stays:
        by_node.setdefault(s["node"], []).append(s)
    for node, ss in by_node.items():
        n = idx[node]
        for s in ss:
            i0 = max(0, int((s["start"] - t0).total_seconds() // 3600))
            i1 = min(H - 1, int((s["end"] - t0).total_seconds() // 3600) + 1)
            for i in range(i0, i1 + 1):
                close = hours_[i] + dt.timedelta(minutes=59, seconds=59)
                if s["start"] <= close < s["end"]:
                    p = pool_of(n, close)
                    if p:
                        out[p][i] -= 8
    return out


def stays_from_events(jobs, console, utc_of_local=K.ams_to_utc):
    """Each node's stays out of service from the two logs, as the fleet notes define them: out from a cordon until an
    uncordon (a job's uncordon step, a console uncordon, or a job completed by hand); a cordon while out is out once."""
    ev = []
    job_node = {}
    for e in jobs:
        job_node[e["job"]] = e["node"]
        if e["step"] == "cordon" and e["result"] == "ok":
            ev.append((e["ts"], e["node"], 1))
        elif e["step"] == "uncordon" and e["result"] == "ok":
            ev.append((e["ts"], e["node"], 0))
    for c in console:
        t = utc_of_local(c["local"])
        if c["action"] == "node.cordon":
            ev.append((t, c["obj"], 1))
        elif c["action"] == "node.uncordon":
            ev.append((t, c["obj"], 0))
        elif c["action"] == "fleetctl.job.complete":
            ev.append((t, job_node[c["obj"]], 0))
    ev.sort()
    state, out = {}, []
    for t, node, kind in ev:
        if kind == 1 and node not in state:
            state[node] = t
        elif kind == 0 and node in state:
            out.append(dict(node=node, start=state.pop(node), end=t))
    for node, t in state.items():       # still out when the logs end
        out.append(dict(node=node, start=t, end=K.MAINT_WINDOW[1]))
    return out


def ask_a(NODES, stays):
    """November GPU-hours out of service and the longest stay, by pool (hours in November UTC, the node's pool at the
    time). Stays across a month end count their November hours; the longest stay is taken over stays inside November."""
    idx = {n["node"]: n for n in NODES}
    gh = {p: 0.0 for p in K.POOLS}
    longest = {p: 0.0 for p in K.POOLS}
    for s in stays:
        n = idx[s["node"]]
        a, b = max(s["start"], K.NOV[0]), min(s["end"], K.NOV[1])
        if b <= a:
            continue
        cuts = sorted({a, b} | {m[1] for m in n["memberships"] if a < m[1] < b})
        for x, y in zip(cuts[:-1], cuts[1:]):
            p = pool_of(n, x)
            gh[p] += 8 * (y - x).total_seconds() / 3600.0
        if s["start"] >= K.NOV[0] and s["end"] <= K.NOV[1]:
            p = pool_of(n, s["start"])
            longest[p] = max(longest[p], (s["end"] - s["start"]).total_seconds() / 3600.0)
    return gh, longest


def center_ask_a(M, NODES):
    """Put every graded Ask A figure clear of its rounding edge, by moving console times by whole minutes:
    a pool's longest November stay ends within 0.02 h of the 0.1-hour grid (its uncordon or hand completion moved by at
    most three minutes), then a pool whose November GPU-hours sit within 2.5 of an edge has its last other November
    hardware uncordon moved towards an offset within 2 of the bin centre (a quarter of an hour at most)."""
    rng = np.random.default_rng(K.SEED + 31)
    idx = {n["node"]: n for n in NODES}
    job_node = {e["job"]: e["node"] for e in M["jobs"]}

    def closer(c):
        return c["obj"] if c["action"] == "node.uncordon" else job_node.get(c["obj"])

    used = set()
    for p in K.POOLS:
        stays = stays_from_events(M["jobs"], M["console"])
        inside = [s for s in stays if s["start"] >= K.NOV[0] and s["end"] <= K.NOV[1]
                  and pool_of(idx[s["node"]], s["start"]) == p]
        top = max(inside, key=lambda s: s["end"] - s["start"])
        h = (top["end"] - top["start"]).total_seconds() / 3600.0
        g0 = int(math.floor(h * 10 + 0.5))
        if g0 in used:                   # another pool already ends on this tenth: the engineer came a few minutes later
            g0 = min((g for g in (g0 - 1, g0 + 1, g0 + 2) if g not in used), key=lambda g: abs(g / 10.0 - h))
        used.add(g0)
        grid = g0 / 10.0 + float(rng.uniform(-0.015, 0.015))
        shift = dt.timedelta(seconds=int(round((grid - h) * 3600)))
        c = [c for c in M["console"] if c["action"] in ("node.uncordon", "fleetctl.job.complete")
             and closer(c) == top["node"] and K.ams_to_utc(c["local"]) == top["end"]][0]
        c["local"] = c["local"] + shift
    for p in K.POOLS:
        stays = stays_from_events(M["jobs"], M["console"])
        gh, longest = ask_a(NODES, stays)
        x = gh[p]
        centre = K.nearest(x, 10)
        if abs(x - centre) <= 2.5:
            continue
        target = centre + float(rng.uniform(-2.0, 2.0))
        delta = dt.timedelta(minutes=int(round((target - x) * 60 / 8.0)))
        ups = [c for c in M["console"] if c["action"] == "node.uncordon"
               and K.NOV[0] + dt.timedelta(hours=2) < K.ams_to_utc(c["local"]) < K.NOV[1] - dt.timedelta(hours=2)
               and pool_of(idx[c["obj"]], K.ams_to_utc(c["local"])) == p]
        ups.sort(key=lambda c: c["local"])
        for c in reversed(ups):
            st = [s for s in stays if s["node"] == c["obj"] and s["end"] == K.ams_to_utc(c["local"])]
            if st and (st[0]["end"] - st[0]["start"] + delta).total_seconds() / 3600 < longest[p] - 0.5:
                c["local"] = c["local"] + delta
                break
    M["console"].sort(key=lambda e: (e["local"], e["obj"]))
    M["stays"] = stays_from_events(M["jobs"], M["console"])
    return M


# ------------------------------------------------------------------------------------------------- the stopgap's acceptance
def acceptance():
    """The provider's burn-in and fabric results for the 30 nodes of the leased cluster, and its handover inventory.
    Three nodes were re-racked after burn-in and before their fabric runs (two from R11 to R14, one from R12 to R11);
    the fabric harness release of 1 December reports bandwidth in Gbit/s where the earlier release reported GB/s, says
    so in the export's unit column, and numbers each node's runs from 1 again."""
    rng = np.random.default_rng(K.SEED + 40)
    racks = {"R11": 8, "R12": 8, "R13": 7, "R14": 7}
    names, serial = [], {}
    tag = 2630
    node_rack = {}
    for r, n in racks.items():
        for i in range(n):
            tag += int(rng.integers(1, 4))
            nm = "nx7-%04d" % tag
            names.append(nm)
            node_rack[nm] = r
    moved = [nm for nm in names if node_rack[nm] == "R11"][6:8]       # the last two of R11, to R14
    moved_r12 = [nm for nm in names if node_rack[nm] == "R12"][7]     # the last of R12, to R11
    hand_rack = {nm: ("R14" if nm in moved else ("R11" if nm == moved_r12 else node_rack[nm])) for nm in names}
    used = set()

    def new_serial():
        while True:
            s = "16529240%05d" % int(rng.integers(10000, 99999))
            if s not in used:
                used.add(s)
                return s
    for nm in names:
        serial[nm] = [new_serial() for _ in range(8)]
    # burn-in windows by rack (local dates of the runs), fabric runs after burn-in
    burn_day = {"R11": dt.datetime(2026, 11, 24, 8, 0), "R12": dt.datetime(2026, 11, 27, 8, 0),
                "R13": dt.datetime(2026, 11, 28, 8, 0), "R14": dt.datetime(2026, 11, 23, 8, 0)}
    fab_day = {"R11": dt.datetime(2026, 11, 27, 9, 0), "R12": dt.datetime(2026, 12, 1, 9, 0),
               "R13": dt.datetime(2026, 12, 2, 9, 0), "R14": dt.datetime(2026, 11, 25, 9, 0)}
    tests = [("dcgm_diag_r3", 0.6), ("gemm_soak_4h", 4.3), ("hbm_memtest", 1.4)]
    burn, fabric, swaps = [], [], []
    fail_gpu = {(names[8 + 1], 3): ("dcgm_diag_r3", "Xid 79 GPU has fallen off the bus", "swap"),     # R12 node 2
                (names[16 + 2], 6): ("hbm_memtest", "row remap failure, bank 11", "swap"),          # R13 node 3
                (names[23 + 4], 1): ("gemm_soak_4h", "thermal slowdown at 87C, fan tray reseated", "rerun")}  # R14 node 5
    for k_, nm in enumerate(names):
        r = node_rack[nm]
        start = burn_day[r] + dt.timedelta(minutes=30 * int(rng.integers(0, 26)))
        for slot in range(8):
            t = start + dt.timedelta(minutes=int(rng.integers(0, 9)))
            for test, hrs in tests:
                end = t + dt.timedelta(hours=hrs, minutes=int(rng.integers(-6, 7)), seconds=int(rng.integers(0, 60)))
                res, note = "PASS", ""
                fg = fail_gpu.get((nm, slot))
                if fg and fg[0] == test:
                    res, note = "FAIL", fg[1]
                burn.append(dict(rack=r, node=nm, slot=slot, serial=serial[nm][slot], run=1, test=test,
                                 start=t, end=end, result=res, note=note))
                t = end + dt.timedelta(minutes=int(rng.integers(1, 5)))
            fg = fail_gpu.get((nm, slot))
            if fg:
                t2 = t + dt.timedelta(seconds=int(rng.uniform(20, 30) * 3600))
                if fg[2] == "swap":
                    old = serial[nm][slot]
                    serial[nm][slot] = new_serial()
                    swaps.append(dict(node=nm, slot=slot, old=old, new=serial[nm][slot], at=t2 - dt.timedelta(hours=3)))
                for test, hrs in tests:
                    end = t2 + dt.timedelta(hours=hrs, minutes=int(rng.integers(-6, 7)), seconds=int(rng.integers(0, 60)))
                    burn.append(dict(rack=r, node=nm, slot=slot, serial=serial[nm][slot], run=2, test=test,
                                     start=t2, end=end, result="PASS", note=""))
                    t2 = end + dt.timedelta(minutes=int(rng.integers(1, 5)))
    # fabric: one run per node, a few re-runs; bus bandwidth in GB/s before the harness release, Gbit/s after
    true_bw = {nm: float(rng.normal(371.5, 3.2)) for nm in names}
    held = {names[3]: 355.2, names[8 + 4]: 333.9, names[8 + 5]: 336.8, names[16 + 2]: 358.3, moved[1]: 354.8}
    true_bw.update(held)
    rerun_fail = names[23 + 1]           # R14 node 2: two runs below the line on 25 November, clear on 2 December
    for nm in names:
        r = hand_rack[nm] if (nm in moved or nm == moved_r12) else node_rack[nm]
        if nm in moved or nm == moved_r12:
            t = dt.datetime(2026, 12, 2, 10, 0) + dt.timedelta(minutes=int(rng.integers(0, 300)))
        elif nm == names[3]:             # R11 node 4: its leaf port was down until 1 December
            t = dt.datetime(2026, 12, 2, 13, 0) + dt.timedelta(minutes=int(rng.integers(0, 90)))
        else:
            t = fab_day[r] + dt.timedelta(minutes=int(rng.integers(0, 420)))
        runs = []
        if nm == names[8 + 2]:           # R12 node 3: started on 30 November, two runs short, clear on 1 December
            t0 = dt.datetime(2026, 11, 30, 14, 5)
            runs.append((t0, 351.8))
            runs.append((t0 + dt.timedelta(minutes=97), 353.9))
        if nm == rerun_fail:
            runs.append((t, 349.6))
            t = t + dt.timedelta(seconds=int(rng.uniform(4, 7) * 3600))
            runs.append((t, 352.3))      # cable reseated, still short; the transceiver was replaced on 1 December
            t = dt.datetime(2026, 12, 2, 15, 26)
        final_bw = true_bw[nm]
        if nm in (names[3], names[16 + 2]):    # repaired on 4 December and run again, after the 14:00 review
            runs.append((t, true_bw[nm]))
            t = {names[3]: dt.datetime(2026, 12, 4, 13, 34), names[16 + 2]: dt.datetime(2026, 12, 4, 13, 41)}[nm]
            final_bw = {names[3]: 370.9, names[16 + 2]: 368.2}[nm]
        runs.append((t, final_bw))
        seq = {}
        for tt, bw in runs:
            new_release = tt >= K.HARNESS_CHANGE
            rel = K.HARNESS_NEW if new_release else K.HARNESS_OLD
            seq[rel] = seq.get(rel, 0) + 1          # each harness release numbers a node's runs from 1
            fabric.append(dict(rack=r, node=nm, harness=rel, run=seq[rel], start=tt,
                               end=tt + dt.timedelta(minutes=int(rng.integers(11, 19)), seconds=int(rng.integers(0, 60))),
                               busbw=round(bw * 8, 1) if new_release else round(bw, 1),
                               unit="Gbit/s" if new_release else "GB/s", algbw=None, true_gbs=bw))
    for f in fabric:
        f["algbw"] = round(f["busbw"] * 8 / 14, 1)     # all-reduce over 8 ranks: algbw = busbw * n / (2 (n - 1))
    inventory = []
    for nm in names:
        for slot in range(8):
            inventory.append(dict(rack=hand_rack[nm], node=nm, slot=slot, serial=serial[nm][slot]))
    inventory.sort(key=lambda x: (x["rack"], x["node"], x["slot"]))
    A = World()
    A.names, A.node_rack, A.hand_rack, A.moved = names, node_rack, hand_rack, moved + [moved_r12]
    A.burn, A.fabric, A.swaps, A.inventory = burn, fabric, swaps, inventory
    A.held_truth = sorted(held)
    return A


# ------------------------------------------------------------------------------------------------- incidents (distractor)
def incidents():
    rng = np.random.default_rng(K.SEED + 50)
    rows = []
    kinds = [("SEV3", "elevated time to first token", 0.6), ("SEV2", "partial outage: replicas crash-looping after config push", 1.4),
             ("SEV3", "request errors from upstream auth service", 0.9), ("SEV2", "regional network degradation", 2.1),
             ("SEV3", "slow autoscaling after node drain", 0.7), ("SEV1", "full outage of the gateway in AMS3", 0.8)]
    t = dt.datetime(2026, 7, 2, 0, 0)
    n = 0
    while True:
        t = t + dt.timedelta(hours=float(rng.exponential(130.0)))
        if t >= dt.datetime(2026, 12, 6, 12, 0):
            break
        sev, what, dur = kinds[int(rng.integers(0, len(kinds)))]
        if sev == "SEV1" and rng.random() < 0.7:
            sev, what = "SEV3", "elevated time to first token"
        n += 1
        pools = list(rng.choice(K.POOLS, size=int(rng.integers(1, 3)), replace=False))
        opened = t.replace(second=int(rng.integers(0, 60)), microsecond=0)
        resolved = opened + dt.timedelta(minutes=int(max(8, rng.exponential(dur * 60))))
        rows.append(dict(id="INC-%04d" % (2140 + n), opened=opened, resolved=resolved, sev=sev,
                         pools=";".join(sorted(pools)), summary=what))
    return rows


# ------------------------------------------------------------------------------------------------- time to first token
def ttft(W, T):
    """The gateway's time to first token, p50 and p95 by pool and hour (milliseconds)."""
    rng = np.random.default_rng(K.SEED + 60)
    out = {}
    for p in K.POOLS:
        R = T[p]["R"]
        load = R / np.maximum(R.max(), 1.0)
        if p == "docs-prod":
            frac_new = T[p]["S"] / np.maximum(R, 1.0)
            p50 = 150 + 70 * load + 30 * rng.standard_normal(len(R)) * 0.2
            p95 = 900 + 3400 * frac_new + 500 * load + 60 * rng.standard_normal(len(R))
        elif p == "batch-prod":
            p50 = 1900 + 1300 * load + 120 * rng.standard_normal(len(R))
            p95 = 6200 + 3900 * load + 300 * rng.standard_normal(len(R))
        else:
            base = {"chat-prod": (210, 690), "code-prod": (95, 310), "agents-prod": (420, 2300),
                    "voice-prod": (75, 190)}[p]
            p50 = base[0] * (1 + 0.35 * load) + 6 * rng.standard_normal(len(R))
            p95 = base[1] * (1 + 0.45 * load) + 20 * rng.standard_normal(len(R))
        out[p] = (np.round(p50).astype(int), np.round(p95).astype(int))
    return out
