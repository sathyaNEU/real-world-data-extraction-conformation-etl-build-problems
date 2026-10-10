"""Every assertion the build makes, run against the files in target/ as written.

Sections: main ladder and position; grid and convergences; census and timing; windows and boundaries;
calibration corpus; Gate G tests; ask goldens; device layer (zero counts, deltas, no-cancel, stops, battery,
necessity, pair simulation, organs, spans, vocabulary); pack gates and hygiene. run_all() prints every check
and returns True only when all hold.
"""
import bisect
import datetime as dt
import itertools
import json
import re
import shutil
import sqlite3
import tempfile
import unicodedata
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

import golden as G
import corpus as CP
import texts as T
from common import INVENTED_NAMES, AS_OF, CORPUS_REGIONS

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
CODES = G.CODES
LET = G.LETTER_OF
A, B, C, D_, E, F_, G_, H = CODES          # COR TAN BRK STN LAT ELL PRW PEL


class Checker:
    def __init__(self):
        self.results = []

    def check(self, name, ok, detail=""):
        self.results.append((name, bool(ok), detail))
        print("%s  %-62s %s" % ("PASS" if ok else "FAIL", name[:62], str(detail)[:150]))
        return ok


GOLDEN_RECORD = {A: (438, 126, 8), B: (104, 29, 0), C: (351, 104, 5), D_: (275, 80, 80), E: (559, 165, 0),
                 F_: (140, 40, 6), G_: (221, 63, 46), H: (75, 22, 3), "total": (2163, 629, 148)}
GOLDEN_Y3 = {A: (150, 44, 2), B: (36, 10, 0), C: (118, 35, 0), D_: (92, 27, 27), E: (190, 56, 0), F_: (46, 13, 0),
             G_: (74, 21, 15), H: (25, 7, 0)}
NATURAL = {A: (454, 137, 39), B: (128, 38, 0), C: (365, 115, 17), D_: (291, 93, 91), E: (632, 176, 0),
           F_: (155, 51, 0), G_: (234, 74, 57), H: (104, 36, 0), "total": (2363, 720, 204)}
# each device mishandled alone: change against the golden per trust, (3a, 3b, 3c)
DELTAS = {
    "DV1": {A: (4, 2, 11), B: (2, 2, 0), C: (2, 2, 5), D_: (2, 2, 2), E: (4, 2, 0), F_: (2, 2, 2), G_: (2, 2, 4),
            H: (2, 2, 0)},
    "DV2": {A: (1, 0, 0), B: (1, 0, 0), C: (1, 0, 0), D_: (1, 0, 0), E: (2, 0, 0), F_: (1, 0, 0), G_: (1, 0, 0),
            H: (1, 0, 0)},
    "DV3": {A: (0, 0, 0), B: (0, 0, 0), C: (0, 0, 0), D_: (0, 0, 0), E: (0, 0, 0), F_: (0, 0, -6), G_: (0, 0, 0),
            H: (0, 0, -3)},
    "DV4": {A: (2, 2, 0), B: (2, 2, 0), C: (2, 2, 0), D_: (2, 2, 2), E: (2, 2, 0), F_: (2, 2, 0), G_: (2, 2, 0),
            H: (2, 2, 2)},
    "DV5": {A: (2, 2, 0), B: (2, 0, 0), C: (2, 2, 0), D_: (4, 4, 4), E: (2, 2, 0), F_: (3, 2, 2), G_: (2, 2, 0),
            H: (3, 3, 2)},
    "DV7": {A: (3, 2, 0), B: (3, 2, 0), C: (3, 2, 0), D_: (1, 0, 0), E: (4, 2, 0), F_: (3, 2, 0), G_: (3, 2, 0),
            H: (3, 2, 0)},
    "DV8": {A: (2, 2, 24), B: (5, 3, 0), C: (2, 2, 6), D_: (2, 2, 0), E: (9, 5, 0), F_: (2, 2, 3), G_: (2, 2, 2),
            H: (4, 3, 0)},
    "DV9": {A: (0, -1, 0), B: (0, -1, 0), C: (0, -1, 0), D_: (0, -1, -1), E: (0, -3, 0), F_: (0, -1, 0),
            G_: (0, -1, -1), H: (0, -1, 0)},
    "HZ1": {A: (0, 0, 2), B: (0, 0, 0), C: (0, 0, 2), D_: (0, 0, 0), E: (0, 0, 0), F_: (0, 0, 0), G_: (0, 0, 4),
            H: (0, 0, 0)},
    "HZ2": {A: (0, 4, 0), B: (0, 4, 0), C: (0, 4, 0), D_: (0, 4, 4), E: (0, 4, 0), F_: (0, 4, 0), G_: (0, 4, 0),
            H: (0, 4, 0)},
}
PLANTED = {"DV1": CODES, "DV2": CODES, "DV3": [F_, H], "DV4": CODES, "DV5": CODES, "DV7": [A, B, C, E, F_, G_, H],
           "DV8": CODES, "DV9": CODES, "HZ1": [A, C, G_], "HZ2": CODES}
# the latest four quarters' deaths per trust under each reading of an admission the trust placed itself
# (on the census by bed assignment, round 3's own test is the referral reading; the physical readings re-time each
# held bed: the trust's own holds only (the golden), or every hold, the bureau's included)
READING_NAMES = {"referral": (G_, 15, A, 2), "audit": (G_, 15, A, 2), "local": (G_, 15, A, 2),
                 "t04": (G_, 15, A, 2), "planned": (A, 37, G_, 15), "not02": (A, 37, G_, 15),
                 "queue": (A, 37, G_, 15), "any": (A, 37, G_, 17), "decisive": (D_, 27, G_, 15),
                 "phys_any": (A, 37, D_, 27), "phys_placed": (A, 37, D_, 27)}
# eighteen cells: basis by scope by allocation reading -> the trust named (None: two wrong trusts within 1.2x)
GRID_NAMES = {}
for _al in ("ignored", "any", "placed"):
    GRID_NAMES[("none", "own", _al)] = A
    GRID_NAMES[("none", "network", _al)] = E
# a frozenset: two wrong trusts within 1.2x of each other lead the cell, D at least 1.2x behind
GRID_NAMES.update({("0800", "own", "ignored"): C, ("0800", "own", "any"): frozenset((A, C)),
                   ("0800", "own", "placed"): C, ("0800", "network", "ignored"): C,
                   ("0800", "network", "any"): frozenset((E, A)), ("0800", "network", "placed"): E,
                   ("census", "own", "ignored"): G_, ("census", "own", "any"): A, ("census", "own", "placed"): G_,
                   ("census", "network", "ignored"): G_, ("census", "network", "any"): frozenset((E, A)),
                   ("census", "network", "placed"): E,
                   ("held_own", "own", "ignored"): D_, ("held_own", "own", "any"): A, ("held_own", "own", "placed"): D_,
                   ("held_own", "network", "ignored"): D_, ("held_own", "network", "any"): frozenset((E, A)),
                   ("held_own", "network", "placed"): E,
                   ("held_all", "own", "ignored"): A, ("held_all", "own", "any"): A, ("held_all", "own", "placed"): A,
                   ("held_all", "network", "ignored"): frozenset((A, E)), ("held_all", "network", "any"): frozenset((E, A)),
                   ("held_all", "network", "placed"): frozenset((E, A))})
GRID_RULE = {("none", "own"): "own care at the hour: the wait passed with the own unit full",
             ("none", "network"): "own care: the trust holds no level-3 beds of its own",
             ("0800", "own"): "own care at the hour of the wait: the 08:00 return describes the morning",
             ("0800", "network"): "its own beds: another trust's vacancy or admission is not this trust's care",
             ("census", "own"): "the bed bureau allocates every transfer's bed (field guide): a transfer is not the "
                                "trust's own decision",
             ("census", "network"): "its own beds: another trust's vacancy or admission is not this trust's care",
             ("census", "own", "ignored"): "the methodology note: a full unit's own placements during the wait are the "
                                           "trust's decisions about the use of its own beds",
             ("census", "own", "placed"): "the theatre extract: a bed assigned to the trust's own patient still in "
                                          "theatre stood empty, kept by the trust (the methodology note)",
             ("held_own", "own"): "the bed bureau allocates every transfer's bed (field guide): a transfer is not the "
                                  "trust's own decision",
             ("held_own", "network"): "its own beds: another trust's vacancy or admission is not this trust's care",
             ("held_all", "own"): "the bed bureau allocates every transfer's bed (field guide): a bed it holds for an "
                                  "incoming transfer is not the trust's to give",
             ("held_all", "network"): "its own beds: another trust's vacancy or admission is not this trust's care"}


def run_all(S, target, meta_path, F, distractors):
    K = Checker()
    target = Path(target)
    D = G.Data(target, F)
    meta = json.loads(Path(meta_path).read_text())
    ladder_checks(K, D)
    grid_checks(K, D)
    census_checks(K, D, S, target, F)
    window_checks(K, D)
    corpus_checks(K, target, F)
    gate_g_checks(K, D, target, F)
    ask_checks(K, D)
    device_checks(K, D, S, target, F)
    pack_checks(K, D, S, target, F, meta, distractors)
    n = len(K.results)
    bad = [r for r in K.results if not r[1]]
    print("\n%d assertions, %d failed" % (n, len(bad)))
    return not bad


# ===================================================================================== main ladder
def ladder_checks(K, D):
    R, cl = G.ladder(D)
    want = [(E, 1.20), (C, 1.20), (G_, 1.20), (A, 1.20), (D_, 1.50)]
    leaders = []
    for k, (who, m) in enumerate(want):
        l, v1, l2, v2, ratio = G.leader(R[k])
        leaders.append(l)
        K.check("rung %d (%s) leader %s, margin >= %.2f" % (k, G.RUNGS[k], LET[who], m), l == who and ratio >= m,
                "%s %d over %s %d (%.2fx)" % (LET[l], v1, LET[l2], v2, ratio))
    K.check("rung figures exactly as designed",
            (R[0][E], R[0][A], R[1][C], R[1][G_], R[2][G_], R[2][A], R[3][A], R[3][G_], R[3][D_], R[4][D_],
             R[4][G_]) == (56, 44, 34, 4, 15, 2, 37, 17, 0, 27, 15),
            [R[k][x] for k, x in ((0, E), (1, C), (2, G_), (3, A), (4, D_))])
    K.check("five distinct rung leaders", len(set(leaders)) == 5, [LET[x] for x in leaders])
    r0 = sorted(R[0].items(), key=lambda kv: -kv[1])
    rank = [t for t, v in r0].index(D_) + 1
    K.check("D 4th on rung 0, behind the leader by >= 1.5x", rank == 4 and R[0][E] / R[0][D_] >= 1.5,
            "rank %d, %.2fx" % (rank, R[0][E] / R[0][D_]))
    pos, second = [], []
    ok = True
    for k in (1, 2, 3):
        s_ = sorted(R[k].items(), key=lambda kv: (-kv[1], kv[0]))
        order = [t for t, v in s_ if t in (A, C, D_, G_)]
        rk = order.index(D_) + 1
        pos.append(rk)
        if rk == 1 and R[k][D_] > 0:
            ok = False
        if rk == 2 and R[k][D_] > 0:
            second.append((k, R[k][order[0]] / R[k][D_]))
    K.check("D leads no intermediate rung; second on none, at zero on rungs 1 to 3",
            ok and not second,
            "ranks %s, D counts %s, second %s" % (pos, [R[k][D_] for k in (1, 2, 3)], second))
    margins = [G.leader(R[k])[4] for k in range(5)]
    K.check("no rung margin under 1.15x; thinnest stated", min(margins) >= 1.15, "thinnest %.3f (rung %d)" %
            (min(margins), margins.index(min(margins))))
    # discriminator dominance: D's decisive edge against each decoy's carried advantage
    edge_g = R[4][D_] / R[4][G_]
    raw_g = R[0][G_] / R[0][D_]
    K.check("dominance over G: decisive edge >= 1.2 x carried raw advantage", edge_g >= 1.2 * max(raw_g, 1.0),
            "edge %.2f, G raw %.2f of D" % (edge_g, raw_g))
    # against A on the physical, every-hold reading (A 37 over D 27): the share each keeps on the decisive axis
    RD = G.readings(D)
    ph = RD["phys_any"]
    carried_a = ph[A] / ph[D_]
    edge_a = (R[4][D_] / ph[D_]) / (R[4][A] / ph[A])
    K.check("dominance over A (every hold read empty): share edge >= 1.2 x A's carried advantage",
            edge_a >= 1.2 * carried_a,
            "A carried %.2fx; shares %.3f vs %.3f, edge %.1f" % (carried_a, R[4][D_] / ph[D_], R[4][A] / ph[A], edge_a))
    K.check("round 3's own test (empty bed by assignment, or an own placement) names G 15 over A 2; D 0",
            G.leader(RD["referral"])[:4] == (G_, 15, A, 2) and RD["referral"][D_] == 0,
            G.leader(RD["referral"])[:4])
    for t in (E, A, C):
        adv = R[0][t] / R[0][D_]
        share_d = R[4][D_] / R[0][D_]
        share_t = R[4][t] / R[0][t] if R[0][t] else 0
        edge = share_d / share_t if share_t else float("inf")
        K.check("dominance over %s: share edge >= 1.2 x raw advantage" % LET[t], edge >= 1.2 * adv,
                "raw %.2fx, shares %.3f vs %.3f" % (adv, share_d, share_t))


# ===================================================================================== grid
def grid_checks(K, D):
    cells = G.grid(D)
    named_d = []
    for key, want in GRID_NAMES.items():
        l, v1, l2, v2, ratio = G.leader(cells[key])
        if isinstance(want, frozenset):
            dd = cells[key][D_]
            K.check("grid cell %s/%s/%s names %s, D at least 1.2x behind" % (key + ("".join(sorted(LET[t] for t in want)),)),
                    l in want and (l2 in want or ratio >= 1.2) and v1 >= 1.2 * dd,
                    "%s %d, %s %d, D %d; violates: %s" % (LET[l], v1, LET[l2], v2, dd, GRID_RULE.get(key, GRID_RULE[key[:2]])))
        else:
            K.check("grid cell %s/%s/%s names %s (>= 1.2x)" % (key + (LET[want],)), l == want and ratio >= 1.2,
                    "%s %d over %s %d (%.2fx)%s" % (LET[l], v1, LET[l2], v2, ratio,
                                                     "" if l == D_ else "; violates: " + GRID_RULE.get(key, GRID_RULE[key[:2]])))
        if l == D_:
            named_d.append(key)
    K.check("only the held-own basis names D (own unit, placement read or ignored; network, ignored: C1)",
            sorted(named_d) == sorted([("held_own", "own", "ignored"), ("held_own", "own", "placed"),
                                       ("held_own", "network", "ignored")]), named_d)
    K.check("held-own cells naming D agree per trust (no own placement and no other unit's vacancy decides one)",
            cells[("held_own", "own", "ignored")] == cells[("held_own", "own", "placed")]
            and all(cells[("held_own", "own", "placed")][t] == cells[("held_own", "network", "ignored")][t]
                    for t in (A, C, D_, G_)))
    eq = all(cells[("census", "own", "ignored")][t] == cells[("census", "network", "ignored")][t] for t in (A, C, D_, G_))
    K.check("own-unit and network scope equal per trust at the census basis, allocation ignored (C1)", eq)
    # the mixed 08:00 reading: network for trusts holding no level-3 beds
    ws = G.waits(D)
    own = {x["id"]: x for x in G.classify(D, ws, scope="own") if x["year"] == 3 and x["died"]}
    net = {x["id"]: x for x in G.classify(D, ws, scope="network") if x["year"] == 3 and x["died"]}
    cnt = defaultdict(set)
    for i, x in own.items():
        y = x if x["has_own"] else net[i]
        if y["v0800"]:
            cnt[x["trust"]].add(x["person"])
    mixed = {t: len(cnt[t]) for t in CODES}
    l, v1, l2, v2, ratio = G.leader(mixed)
    K.check("mixed 08:00 reading (network for trusts without beds) names C", l == C and ratio >= 1.2,
            "%s %d over %s %d" % (LET[l], v1, LET[l2], v2))


# ===================================================================================== census and timing
def census_checks(K, D, S, target, F):
    ws = G.waits(D)
    cl_all = G.classify(D, ws)
    cl3 = [x for x in cl_all if x["year"] == 3]
    adm_planned = defaultdict(list)
    st = D.stays
    for r in st.itertuples(index=False):
        if r.admission_type == "04":
            adm_planned[r.unit_code].append(G.mins(r.admitted_at.to_pydatetime()))
    for v in adm_planned.values():
        v.sort()
    first_row = {}
    for r in st.sort_values("admitted_at").itertuples(index=False):
        first_row.setdefault((r.unit_code, r.patient_key, G.mins(r.admitted_at.to_pydatetime())), r)
    audit = pd.read_csv(Path(target) / F["transfers"], dtype=str, keep_default_na=False)
    audit_keys = {(r.patient_key, r.to_unit, r.bed_confirmed_at) for r in audit.itertuples(index=False)}
    ref_by = {r["id"]: r for r in D.refs}

    def inside(lst, a, b):
        i = bisect.bisect_right(lst, a)
        return i < len(lst) and lst[i] < b

    # what fills a referring trust's own unit during its long waits (merged islands), and who placed each patient
    adm = defaultdict(list)
    own_place = defaultdict(list)       # every admission the unit's own trust placed
    own_planned = defaultdict(list)     # of them, the planned ones (03 from the trust's own recovery, 04, 05)
    for u, k, a, b, typ, rid in D.merged:
        adm[u].append((a, k, typ, rid))
        if not D.is_transfer_op(u, rid):
            own_place[u].append(a)
            if typ in ("03", "04", "05"):
                own_planned[u].append(a)
    for u in adm:
        adm[u].sort()
    for v in list(own_place.values()) + list(own_planned.values()):
        v.sort()
    src_of = {r.referral_id: r.source_location for r in st.itertuples(index=False) if r.referral_id}
    kinds_y3, kinds_rec, queue_bad = Counter(), Counter(), []
    audit_miss, own_in_audit = 0, 0
    pairs = {"own": set(), "bureau": set()}
    wards = {"own": set(), "bureau": set()}
    a_deaths_planned, a_deaths = 0, 0
    for x in cl_all:
        if not x["has_own"] or x["id"] in D.copies:
            continue
        u = D.own_units(x["trust"], x["dta"].date())[0]
        lst = adm[u]
        i = bisect.bisect_left(lst, (x["a"] + 1,))
        planned_bureau = False
        while i < len(lst) and lst[i][0] < x["b"]:
            a, k, typ, rid = lst[i]
            when = (G.EPOCH + dt.timedelta(minutes=a)).strftime("%Y-%m-%d %H:%M")
            in_audit = (D.temp.get(k, k), u, when) in audit_keys or (k, u, when) in audit_keys
            q = D.ref_dta_local.get(rid) if rid else None
            if D.is_transfer_op(u, rid):
                kind = "bureau"
                audit_miss += not in_audit
                planned_bureau |= typ == "03"
                # unplanned transfers were referred before the waiting patient, planned ones after
                if (typ == "03") != (q is not None and q > x["a"]):
                    queue_bad.append((LET[x["trust"]], typ, when))
            else:
                kind = "own"
                own_in_audit += in_audit
                if rid and not (q is not None and q > x["a"]):
                    queue_bad.append((LET[x["trust"]], "own " + typ, when))
            kinds_rec[(kind, typ)] += 1
            if x["year"] == 3:
                kinds_y3[(LET[x["trust"]], kind, typ)] += 1
                pairs[kind].add((typ, src_of.get(rid, "")))
                if rid:
                    wards[kind].add(ref_by[rid]["ward"])
            i += 1
        if x["year"] == 3 and x["trust"] == A and x["died"] and not x["empty"] and x["alloc_any"]:
            a_deaths += 1
            a_deaths_planned += planned_bureau
    K.check("(Y3) inside every long wait the own unit admitted only bureau transfers (A coded 02 and 03, C and G 02); "
            "nothing is admitted to Stennock's unit during any Stennock long wait",
            set(kinds_y3) == {("A", "bureau", "02"), ("A", "bureau", "03"), ("C", "bureau", "02"),
                              ("G", "bureau", "02")}, dict(kinds_y3))
    K.check("(record) inside long waits own placements are coded 03 (D's legacy months) or 04 (planned own-theatre at "
            "A, C and G), bureau transfers 02, 03 or the legacy feed's 01",
            set(kinds_rec) <= {("own", "03"), ("own", "04"), ("bureau", "01"), ("bureau", "02"), ("bureau", "03")}
            and ("own", "03") in kinds_rec and ("bureau", "03") in kinds_rec, dict(kinds_rec))
    K.check("a bureau placement coded planned (03) inside every A death-wait the unit filled (Y3)",
            a_deaths and a_deaths_planned == a_deaths, "%d of %d A death-waits" % (a_deaths_planned, a_deaths))
    K.check("queue: own placements and planned bureau transfers referred after the waiting patient, unplanned ones "
            "before (record)", not queue_bad, queue_bad[:4])
    K.check("every bureau transfer inside a long wait is in the transfer audit at its bed time; no own placement is",
            audit_miss == 0 and own_in_audit == 0, (audit_miss, own_in_audit))
    rd = G.readings(D)
    bad = {}
    for k, (l1, v1, l2, v2) in READING_NAMES.items():
        got = G.leader(rd[k])
        if got[:4] != (l1, v1, l2, v2):
            bad[k] = got[:4]
    K.check("readings on the latest four quarters: by assignment, own placement read by referral, audit, type local "
            "or 04 G 15 over A 2 (round 3's test); planned, not 02, queue, any admission A 37 over G; every held bed "
            "empty A 37 over D 27; the trust's own holds empty D 27 over G 15", not bad,
            bad or {k: "%s %d" % (LET[v[0]], v[1]) for k, v in READING_NAMES.items()})
    K.check("referral and audit readings select the same deaths per trust (C1), on the record too",
            rd["referral"] == rd["audit"] and G.asks(D, construction="audit") == G.asks(D, construction="workorder"))
    K.check("any admission and the trust's own placements (by assignment) part only at A, C and G (Y3 deaths)",
            all(rd["any"][t] == rd["referral"][t] for t in (B, D_, E, F_, H))
            and all(rd["any"][t] > rd["referral"][t] for t in (A, C, G_)),
            {LET[t]: (rd["any"][t], rd["referral"][t]) for t in CODES})
    first4 = True
    for x in cl3:
        own = D.own_units(x["trust"], x["dta"].date())
        if not own or x["empty"] or not x["alloc"]:
            continue
        u = own[0]
        if not inside(own_place[u], x["a"], min(x["b"], x["a"] + 240)):
            first4 = False
    K.check("every own-placement wait holds an own placement inside its first four hours (Y3)", first4)
    ok_own, ok_cap, n_own, n_cap = True, True, 0, 0
    for x in cl3:
        own = D.own_units(x["trust"], x["dta"].date())
        if not own:
            continue
        u = own[0]
        thr = D.empty_during(u, x["a"], x["b"], mode="all")
        anyt = D.empty_during(u, x["a"], x["b"], mode="any")
        hourly = D.hourly_empty(u, x["a"], x["b"])
        at_dta = D.empty_during(u, x["a"], x["a"] + 1, mode="any")
        if anyt:
            n_own += 1
            ok_own &= thr and at_dta and (hourly or (x["b"] - x["a"]) < 60)
        else:
            n_cap += 1
            ok_cap &= not hourly and not at_dta
    K.check("own-empty waits hold the empty bed from decision to assignment (all readings agree)", ok_own,
            "%d own-empty waits" % n_own)
    K.check("no capacity wait shows an empty staffed bed at minute grain or hourly snapshot", ok_cap,
            "%d waits at full own units" % n_cap)
    # trusts without level-3 beds: no unit empty and no own placement anywhere during their waits
    ok = True
    for x in cl3:
        if x["has_own"]:
            continue
        for u in D.l3_units(x["dta"].date()):
            if D.empty_during(u, x["a"], x["b"]) or inside(own_planned[u], x["a"], x["b"]):
                ok = False
    K.check("no long wait at a trust without level-3 beds overlaps an empty bed or a planned own placement (Y3)", ok)
    ok = True
    for x in cl3:
        for u in D.l3_units(x["dta"].date()):
            if inside(own_planned[u], x["a"], x["b"]):
                ok = False
    K.check("no planned own placement at any unit inside any year-3 long wait", ok)
    hold_checks(K, D, cl_all, target, F)
    # D's long waits fall on weekdays during the lists; G's own-empty waits at weekends
    d_days = {x["dta"].weekday() for x in cl3 if x["trust"] == D_}
    K.check("every D long wait falls on a weekday", d_days <= {0, 1, 2, 3, 4}, sorted(d_days))
    # the 08:00 returns reproduce the census, and D's and A's units never report a vacancy in the record
    bad = 0
    for (u, d), occ in D.occ0800.items():
        t = G.mins(dt.datetime.combine(dt.date.fromisoformat(d), dt.time(8, 0)))
        ts, vs = D.census[u]
        i = bisect.bisect_right(ts, t) - 1
        if (vs[i] if i >= 0 else 0) != occ:
            bad += 1
    K.check("08:00 returns equal the census rebuilt from the unit feed", bad == 0, "%d mismatches" % bad)
    vac = {u: sum(1 for (x, d), o in D.occ0800.items() if x == u and o < D.beds_on[(x, d)]) for u in D.units}
    K.check("D's unit full at every 08:00 return; A's too", vac.get("STN-ACC", 0) == 0 and vac.get("RIS-ACC", 0) == 0,
            vac)
    # platform outcome times equal the unit feed's assignment minute
    mism = 0
    for r in D.refs:
        if not r["legacy"] and r["outcome"] == "Admitted" and r["unit"] in D.units and r["id"] in D.assign_of:
            if G.mins(r["out"]) != D.assign_of[r["id"]][1]:
                mism += 1
    K.check("platform outcome_at equals the feed's bed assignment for every admission", mism == 0, mism)


# ===================================================================================== windows
def hold_checks(K, D, cl_all, target, F):
    """The trust's own held beds: the morning bookings at Stennock's unit and the theatre extract that dates them."""
    holds = D.own_hold                        # (unit, key, assigned minute) -> left recovery minute
    K.check("own holds sit only at STN-ACC, in the platform months, assigned 08:10 or later on a weekday",
            holds and all(u == "STN-ACC" and a >= G.GO_MIN and 8 * 60 + 10 <= a % 1440 and
                          (G.EPOCH + dt.timedelta(minutes=a)).weekday() < 5 for (u, k, a) in holds),
            "%d holds" % len(holds))
    K.check("no hold spans 08:00 (the 08:00 return is untouched) and each patient leaves recovery the same day",
            all(((a // 1440) == (left // 1440)) and a % 1440 >= 8 * 60 for (u, k, a), left in holds.items()))
    # every platform-era Stennock long wait passes beside a hold whose patient leaves recovery inside the wait's first
    # four hours, at least ten minutes after the decision; no other wait anywhere meets a hold or an own empty bed it
    # did not already have
    iv = defaultdict(list)
    for (u, k, a), left in holds.items():
        iv[u].append((a, left))
    d_ok, d_n, other_bad = True, 0, []
    for x in cl_all:
        if not x["has_own"]:
            continue
        u = D.own_units(x["trust"], x["dta"].date())[0]
        hs = [(a, l) for a, l in iv.get(u, []) if a < x["a"] and l > x["a"]]
        if x["trust"] == D_ and x["a"] >= G.GO_MIN:
            d_n += 1
            d_ok &= bool(hs) and all(x["a"] + 10 <= l <= x["a"] + 240 and l < x["b"] for a, l in hs)
        elif hs:
            other_bad.append((LET[x["trust"]], x["id"]))
    K.check("every platform-era Stennock long wait passes beside an own hold, its patient leaving recovery 10 to 240 "
            "minutes after the decision (the four-hour counterfactual converges)", d_ok and d_n > 0, "%d waits" % d_n)
    K.check("no other long wait at a unit holding beds meets an own hold", not other_bad, other_bad[:4])
    nonD = all(not x["empty_own"] or x["empty"] for x in cl_all if x["trust"] != D_)
    K.check("the held-own census changes no wait outside Stennock's (every other own-empty wait is empty by "
            "assignment too)", nonD)
    d_plat = [x for x in cl_all if x["trust"] == D_ and x["a"] >= G.GO_MIN and x["has_own"]]
    K.check("by assignment Stennock's unit is full at every minute of every platform-era Stennock long wait and admits "
            "no one", d_plat and not any(x["empty"] or x["alloc_any"] for x in d_plat), len(d_plat))
    # the theatre extract against the feed
    th = pd.read_parquet(Path(target) / F["theatre"])
    th_cc = th[th["recovery_destination"] == "Critical care unit"]
    st = D.stays
    st2 = st.sort_values(["unit_code", "patient_key", "admitted_at"]).reset_index(drop=True)
    prev_end = st2.groupby(["unit_code", "patient_key"])["discharged_at"].shift(1)
    first = st2[~(prev_end == st2["admitted_at"])]          # a bed move continues the stay before it
    theatre_stays = first[first["source_location"].isin(["01", "02"])]
    res = lambda k: D.temp.get(k, k)
    by_key = defaultdict(list)
    for r in th_cc.itertuples(index=False):
        by_key[res(r.patient_key)].append((r.provider_code, G.mins(r.left_recovery_at.to_pydatetime())))
    dep = {}
    for r in D.tx.itertuples(index=False):
        dep[(r.to_unit, res(r.patient_key))] = dep.get((r.to_unit, res(r.patient_key)), []) + [G.mins(G.p_ts(r.departed_at))]
    missing, late = 0, 0
    for r in theatre_stays.itertuples(index=False):
        a = G.mins(r.admitted_at.to_pydatetime())
        cs = [(p, l) for p, l in by_key.get(res(r.patient_key), []) if a - 2880 < l < a + 18 * 60]
        if not cs:
            missing += 1
            continue
        ut = D.unit_trust[r.unit_code]
        if (r.unit_code, res(r.patient_key), a) in holds:
            continue
        for p, l in cs:
            if p == ut and l > a:
                late += 1
            if p != ut and not any(l <= d for d in dep.get((r.unit_code, res(r.patient_key)), [])):
                late += 1
    K.check("every unit stay from theatre has its theatre case; outside the holds every patient left recovery before "
            "the bed was assigned (own trust) or before the transfer departed (bureau)", missing == 0 and late == 0,
            "%d stays, %d missing, %d late" % (len(theatre_stays), missing, late))
    n_cc = len(th_cc)
    K.check("every critical care destination in the theatre extract meets a unit stay from theatre",
            n_cc == len(theatre_stays), "%d cases, %d stays" % (n_cc, len(theatre_stays)))
    # booked beds: requested from the surgical day unit before the list, assigned within minutes
    booked_refs = [r for r in D.refs if not r["legacy"] and r["id"] in D.assign_of and
                   (D.assign_of[r["id"]][0], res(r["key"]), D.assign_of[r["id"]][1]) in holds]
    K.check("every hold's bed was requested from the surgical day unit and assigned within 15 minutes of the decision",
            len(booked_refs) == len(holds) and all(r["ward"] == "SDU" and r["level"] == 3 and
                                                   0 <= G.mins(r["out"]) - G.mins(r["dta"]) <= 15 for r in booked_refs),
            "%d of %d" % (len(booked_refs), len(holds)))
    wo = G.asks(D, construction="workorder")
    gold = G.asks(D)
    K.check("record 3c: round 3's test keeps Stennock's legacy months only; every other trust as the golden",
            wo[D_][2] < gold[D_][2] and all(wo[t] == gold[t] for t in CODES if t != D_),
            "D %d against %d" % (wo[D_][2], gold[D_][2]))


def window_checks(K, D):
    ws = G.waits(D)
    cl = G.classify(D, ws)
    y3 = [x for x in cl if x["year"] == 3]
    # every referral wait in Y3 clear of four hours by five minutes
    near = 0
    for w in ws:
        if w["end"] is None or w["dta"] is None:
            continue
        if G.year_of(w["dta"].date()) != 3:
            continue
        m = G.mins(w["end"]) - G.mins(w["dta"])
        if 235 <= m <= 245:
            near += 1
    K.check("no wait in the latest four quarters within five minutes of four hours", near == 0, near)
    bad = [x for x in cl if D.death(x["person"]) is not None and 25 <= (D.death(x["person"]) - x["dta"].date()).days <= 35]
    K.check("no long-wait death between day 25 and day 35 after its decision (record)", not bad, len(bad))
    # decision-dated and death-dated windows select the same deaths
    straddle = 0
    for x in cl:
        if x["died"]:
            dd = D.death(x["person"])
            if G.year_of(dd) != x["year"]:
                straddle += 1
    K.check("no long-wait death straddles a four-quarter window edge", straddle == 0, straddle)
    # patients and referrals agree in Y3; in the record only the designed identity rows repeat
    per = Counter(x["person"] for x in y3)
    K.check("no patient holds two long waits in the latest four quarters", max(per.values()) == 1)
    perr = Counter(x["person"] for x in cl)
    rep = [p for p, n in perr.items() if n > 1]
    hz2 = {x["person"] for x in cl if x["id"] in D.copies}
    temp = {x["person"] for x in cl if x["key"] in D.temp}
    dv7 = []
    st_out = dict(zip(D.stays["referral_id"], D.stays["discharged_at"]))
    for p in rep:
        if p in hz2 or p in temp:
            continue
        xs = sorted((x for x in cl if x["person"] == p), key=lambda x: x["dta"])
        out1 = st_out.get(xs[0]["id"])
        ok = (len(xs) == 2 and xs[0]["trust"] == xs[1]["trust"] and {x["year"] for x in xs} == {2}
              and 8 <= (xs[1]["dta"].date() - xs[0]["dta"].date()).days <= 13 and all(x["died"] for x in xs)
              and D.death(p) is not None and (D.death(p) - xs[0]["dta"].date()).days <= 21
              and out1 is not None and not pd.isna(out1) and out1 < xs[1]["dta"])
        dv7.append((p, ok))
    per_trust = Counter(next(x["trust"] for x in cl if x["person"] == p) for p, ok in dv7)
    K.check("repeat long-wait patients are identity-device rows, parallel-run copies or the designed repeat patients "
            "(two at each trust but D, year 2, discharged alive, referred again 8 to 13 days after, dead inside 21 days)",
            all(ok for p, ok in dv7) and set(per_trust.values()) == {2} and len(per_trust) == 7 and D_ not in per_trust,
            "%d repeat persons, %d designed repeats" % (len(rep), len(dv7)))
    # register static through Y3; staffed equals commissioned beds at the four units
    ch = [r for r in D.reg_rows if (r[4] > dt.date(2025, 7, 1) and r[4] <= dt.date(2026, 6, 30)) or
          (r[5] is not None and dt.date(2025, 7, 1) <= r[5] < dt.date(2026, 6, 30))]
    K.check("unit register static through the latest four quarters", not ch, ch)
    ok = all(D.beds_on[(u, d)] == D.reg_beds(u) for (u, d) in D.beds_on if u in ("RIS-ACC", "BRK-ACC", "STN-ACC",
                                                                                  "PRW-ACC"))
    K.check("staffed beds in every return equal the register's commissioned beds (four units)", ok)
    # the latest four quarters stand for 2027-28: D leads the decisive construction in each year
    res = {}
    for y in (1, 2, 3):
        a = G.asks(D, years=(y,))
        l, v1, l2, v2, ratio = G.leader({t: a[t][2] for t in CODES})
        res[y] = (LET[l], v1, LET[l2], v2, round(ratio, 2))
    K.check("D leads the decisive construction in each four-quarter year by >= 1.2x",
            all(v[0] == "D" and v[4] >= 1.2 for v in res.values()), res)
    a8 = G.asks(D, years=(2, 3))
    arec = G.asks(D)
    n8 = G.leader({t: a8[t][2] for t in CODES})
    nr = G.leader({t: arec[t][2] for t in CODES})
    K.check("the name converges across four quarters, eight quarters and the record", n8[0] == D_ and nr[0] == D_,
            "8q %s %d over %s %d; record %s %d over %s %d" % (LET[n8[0]], n8[1], LET[n8[2]], n8[3], LET[nr[0]],
                                                              nr[1], LET[nr[2]], nr[3]))
    # long-wait mortality 25 to 33 per cent at every trust
    tab = G.year_table(D)
    mort = {LET[t]: round(100 * tab[t][1] / tab[t][0], 1) for t in CODES}
    mrec = {LET[t]: round(100 * arec[t][1] / arec[t][0], 1) for t in CODES}
    K.check("long-wait mortality between 25 and 33 per cent at every trust (Y3 and record)",
            all(25 <= v <= 33 for v in list(mort.values()) + list(mrec.values())), mort)
    # stand-downs within four hours; no wait crosses a clock change
    sd = [w for w in ws if w["outcome"] == "Stood down" and w["end"] is not None and
          (G.mins(w["end"]) - G.mins(w["dta"])) > 230]
    K.check("every stand-down falls within four hours of the decision", not sd, len(sd))
    dst = [dt.datetime(2023, 10, 29, 1, 0), dt.datetime(2024, 3, 31, 1, 0), dt.datetime(2024, 10, 27, 1, 0),
           dt.datetime(2025, 3, 30, 1, 0), dt.datetime(2025, 10, 26, 1, 0), dt.datetime(2026, 3, 29, 1, 0)]
    cross = []
    for w in ws:
        if w["end"] is None:
            continue
        for t in dst:
            if w["dta"] <= t <= w["end"]:
                night = (w["dta"] - dt.timedelta(hours=12)).date().isoformat()     # the evening the night began
                cross.append((w["id"], night, G.wait_minutes(w, set()) - G.wait_minutes(w, set(G.DEVICES))))
    days = Counter(c[1] for c in cross)
    K.check("the only waits across a clock change are the designed spring-night waits (11 on 30 March 2024, 9 on "
            "29 March 2025), none in the latest four quarters, each an hour longer on the clock than elapsed",
            days == Counter({"2024-03-30": 11, "2025-03-29": 9}) and all(c[2] == 60 for c in cross),
            dict(days))
    long_cross = [c for c in cross if c[0] in {x["id"] for x in cl}]
    K.check("no wait across a clock change is a long wait (elapsed 3h10 to 3h50)", not long_cross, len(long_cross))
    # the 08:00 return read on the decision's date equals the latest return before the decision
    night = [x for x in cl if x["dta"].hour < 8]
    K.check("no long-wait decision between 00:00 and 08:00 (decision-date and latest 08:00 return readings converge)",
            not night, len(night))
    # maturity: every long-wait death in the record registered before the extract
    late = [x for x in cl if x["died"] and D.death(x["person"]) > dt.date(2026, 7, 31)]
    K.check("every 30-day death after a long wait is registered before the extract (14-day lag)", not late)


# ===================================================================================== corpus
def corpus_load(target, F):
    con = sqlite3.connect(str(Path(target) / F["reviewdb"]))
    refs = pd.read_sql("SELECT * FROM referrals", con)
    outc = pd.read_sql("SELECT * FROM patient_outcomes", con)
    stays = pd.read_sql("SELECT * FROM unit_stays", con)
    rets = pd.read_sql("SELECT * FROM bed_returns", con)
    revs = pd.read_sql("SELECT * FROM reviews", con)
    con.close()
    log = pd.read_excel(Path(target) / F["reviewlog"], sheet_name="Reviews")
    att = pd.read_excel(Path(target) / F["reviewlog"], sheet_name="Attempts")
    return refs, outc, stays, rets, revs, log, att


def corpus_patients(refs, outc):
    m = refs.merge(outc, on=["review_ref", "referral_ref"], how="left")
    pats = defaultdict(list)
    for r in m.itertuples(index=False):
        tm = lambda s: None if s is None or (isinstance(s, float)) else CP.minute(
            dt.date.fromisoformat(s[:10]), int(s[11:13]), int(s[14:16]))
        out = {"admitted": "admitted", "died before admission": "died", "stood down": "stood_down"}[r.outcome]
        p = {"level_req": int(r.level_requested), "level_dec": int(r.level_decided), "received": tm(r.received_at),
             "dta": tm(r.decision_at), "outcome": out, "assigned": tm(r.bed_assigned_at), "arrived": tm(r.arrived_at),
             "end": tm(r.outcome_at),
             "death": dt.date.fromisoformat(r.date_of_death) if isinstance(r.date_of_death, str) else None,
             "hosp_out": dt.date.fromisoformat(r.hospital_discharge_date)}
        pats[r.review_ref].append(p)
    return pats


def corpus_checks(K, target, F):
    refs, outc, stays, rets, revs, log, att = corpus_load(target, F)
    pats = corpus_patients(refs, outc)
    log = log.set_index("Review ref")
    conf = log["Deaths confirmed avoidable"].to_dict()
    filed = {k: CP.rule_count(v, CP.FILED) for k, v in pats.items()}
    K.check("corpus: the filed rule reproduces 34 of 34 reviews exactly", len(conf) == 34 and
            all(filed[k] == conf[k] for k in conf), "total %d" % sum(filed.values()))
    K.check("corpus: 34 reviews, 41 attempts, 412 confirmed, 7 confirmed nothing",
            len(log) == 34 and len(att) == 41 and sum(conf.values()) == 412 and sum(1 for v in conf.values() if v == 0) == 7)
    rules = CP.all_rules()
    worst_miss, worst_rule, near = 99, None, None
    one_dir_min = 9.0
    ups = {"receipt_to_bed", "decision_to_arrival", "90d", "decided_2_or_3", 180}
    downs = {"7d", "dropped", 360}
    for rule in rules:
        if rule == CP.FILED:
            continue
        cnt = {k: CP.rule_count(v, rule) for k, v in pats.items()}
        miss = sum(1 for k in conf if cnt[k] != conf[k])
        if miss < worst_miss:
            worst_miss, worst_rule = miss, rule
        changed = {x for x, f in zip(rule, CP.FILED) if x != f}
        if changed <= ups or changed <= downs:
            rel = abs(sum(cnt.values()) - 412) / 412
            one_dir_min = min(one_dir_min, rel)
    K.check("corpus: 216 rules swept; every rival misses at least 4 reviews", len(rules) == 216 and worst_miss >= 4,
            "nearest rival %s misses %d reviews" % (worst_rule, worst_miss))
    K.check("corpus: every one-directional rival misses the 412 total by >= 10 per cent", one_dir_min >= 0.10,
            "smallest miss %.1f%%" % (100 * one_dir_min))
    # blindness: no long wait with the reviewed unit full at any time; every rung construction reproduces
    full = 0
    rung_ok = True
    stays["a"] = stays["admitted_at"]
    for ref, ps in pats.items():
        rv = revs.set_index("review_ref").loc[ref]
        beds = int(rv["level3_beds"])
        s = stays[stays.review_ref == ref]
        ev = defaultdict(int)
        for r in s.itertuples(index=False):
            ev[CP.minute(dt.date.fromisoformat(r.admitted_at[:10]), int(r.admitted_at[11:13]), int(r.admitted_at[14:16]))] += 1
            ev[CP.minute(dt.date.fromisoformat(r.discharged_at[:10]), int(r.discharged_at[11:13]), int(r.discharged_at[14:16]))] -= 1
        c, mx = 0, 0
        for t in sorted(ev):
            c += ev[t]
            mx = max(mx, c)
        if mx >= beds:
            full += 1
        rr = rets[rets.review_ref == ref]
        if (rr["beds_occupied_0800"] >= rr["beds_open"]).any():
            rung_ok = False
    K.check("corpus blind: no reviewed unit was ever full (so every long wait passed beside an empty bed)", full == 0,
            "%d reviews with a full unit" % full)
    K.check("corpus blind: raw, structural, 08:00, census and decisive constructions equal the rule on all 34",
            rung_ok and full == 0)
    # the twin pair
    cols = ["Trust type", "Level 3 beds", "Referrals in year", "Level 3 referrals waiting over 4h from receipt",
            "Mean beds occupied at 08:00", "Level 3 referrals: deaths within 30 days (all causes)"]
    ta = log[(log["Trust"] == "Ormerleby") & (log["Year reviewed"] == 2022)].iloc[0]
    tb = log[(log["Trust"] == "Selarwell") & (log["Year reviewed"] == 2023)].iloc[0]
    same = all(ta[c] == tb[c] for c in cols)
    ka, kb = ta.name, tb.name
    rc = ("receipt_to_bed", "30d", "decided_3", "kept", 240)
    K.check("twin pair identical on every column the log shows, confirmed 24 and 11",
            same and conf[ka] == 24 and conf[kb] == 11, [ta[c] for c in cols])
    K.check("twin pair: the rule reproduces both from records; the receipt clock gives both the same",
            filed[ka] == 24 and filed[kb] == 11 and CP.rule_count(pats[ka], rc) == CP.rule_count(pats[kb], rc),
            "receipt clock %d and %d" % (CP.rule_count(pats[ka], rc), CP.rule_count(pats[kb], rc)))
    # the retry log
    zeros = [k for k, v in conf.items() if v == 0]
    retried = att.groupby("Review ref")["Attempt"].max()
    ok = all(retried[k] == 2 for k in zeros) and all(filed[k] == 0 for k in zeros) and \
        (att[att["Attempt"] == 2]["Deaths confirmed avoidable"] == 0).all()
    sup = [("receipt_to_bed", "30d", "decided_3", "kept", 240), ("decision_to_arrival", "30d", "decided_3", "kept", 240),
           ("decision_to_bed", "90d", "decided_3", "kept", 240), ("decision_to_bed", "30d", "decided_2_or_3", "kept", 240),
           ("decision_to_bed", "30d", "decided_3", "kept", 180)]
    nz = {r[0] + "/" + r[1] + "/" + r[2] + "/" + str(r[4]): sum(1 for k in zeros if CP.rule_count(pats[k], r) > 0)
          for r in sup}
    K.check("retry log: 7 zero reviews retried on a doubled sample, zero again; each widening rival non-zero on >= 4",
            ok and min(nz.values()) >= 4, nz)
    # every rule exercised: the window case, deaths before assignment, level, threshold
    fw = log[(log["Trust"] == "Feningby") & (log["Year reviewed"] == 2021)].index[0]
    pf = pats[fw]
    post30 = sum(1 for p in pf if p["level_dec"] == 3 and p["death"] and p["outcome"] == "admitted" and
                 p["death"] > p["hosp_out"] and (p["death"] - CP.to_date(p["dta"])).days <= 30 and
                 (p["assigned"] - p["dta"]) > 240)
    late = sum(1 for p in pf if p["level_dec"] == 3 and p["death"] and p["outcome"] != "stood_down" and
               31 <= (p["death"] - CP.to_date(p["dta"])).days <= 60 and
               ((p["assigned"] if p["assigned"] else p["end"]) - p["dta"]) > 240)
    K.check("rule exercised: Feningby 2021 counts 3 post-discharge deaths inside 30 days, not 5 between days 31 and 60",
            post30 == 3 and late == 5, (post30, late))
    dw = max(sum(1 for p in v if p["outcome"] == "died" and p["level_dec"] == 3 and p["end"] - p["dta"] > 240 and p["death"])
             for v in pats.values())
    l2 = max(sum(1 for p in v if p["level_dec"] == 2 and p["outcome"] != "stood_down" and p["death"] and
                 ((p["assigned"] if p["assigned"] else p["end"]) - p["dta"]) > 240 and
                 (p["death"] - CP.to_date(p["dta"])).days <= 30) for v in pats.values())
    K.check("rule exercised: a review counting 4 deaths while waiting; one with 6 level-2 long-wait deaths left out",
            dw >= 4 and l2 >= 6, (dw, l2))


# ===================================================================================== Gate G
def gate_g_checks(K, D, target, F):
    # clean-data test: replace the 08:00 return with an hourly return of occupancy against staffed beds
    ws = G.waits(D)
    cl = [x for x in G.classify(D, ws) if x["year"] == 3 and x["died"]]
    r2h = defaultdict(set)
    for x in cl:
        if not x["has_own"]:
            continue
        u = D.own_units(x["trust"], x["dta"].date())[0]
        if D.hourly_empty(u, x["a"], x["b"]):
            r2h[x["trust"]].add(x["person"])
    hourly = {t: len(r2h[t]) for t in CODES}
    R, _ = G.ladder(D)
    ans = G.leader(R[4])[0]
    naive = G.leader(R[0])[0]
    K.check("clean-data test (hourly return in place of 08:00): rung names G, answer D, naive E, D differs from E",
            G.leader(hourly)[0] == G_ and ans == D_ and naive == E and ans != naive, hourly)
    # deleting the context artifact moves nothing
    with tempfile.TemporaryDirectory() as tmp:
        t2 = Path(tmp) / "t"
        shutil.copytree(target, t2)
        (t2 / F["capacity"]).unlink()
        D2 = G.Data(t2, F)
        same = G.ladder(D2)[0] == R and G.asks(D2) == G.asks(D)
    K.check("capacity report deleted: every rung and every ask figure unchanged", same)
    # lens swap: no referral-log column or pair of columns reproduces the confirmable counts
    conf = {t: v[2] for t, v in G.year_table(D).items()}
    rows = [x for x in cl]
    cols = ["ward", "unit", "outcome"]
    feats = {"ward": lambda x: x.get("ward"), "unit": lambda x: x["unit"], "outcome": lambda x: x["outcome"],
             "hour": lambda x: x["dta"].hour, "weekday": lambda x: x["dta"].weekday() >= 5}
    ref_by_id = {r["id"]: r for r in D.refs}
    for x in rows:
        x["ward"] = ref_by_id[x["id"]]["ward"]
    hit = []
    vals = {k: sorted({str(f(x)) for x in rows}) for k, f in feats.items() if k in ("ward", "unit", "outcome")}
    combos = [(k, v) for k in vals for v in vals[k]]
    for (k1, v1), (k2, v2) in itertools.combinations_with_replacement(combos, 2):
        sel = defaultdict(set)
        for x in rows:
            if str(feats[k1](x)) == v1 and str(feats[k2](x)) == v2:
                sel[x["trust"]].add(x["person"])
        vec = {t: len(sel[t]) for t in CODES}
        if all(abs(vec[t] - conf[t]) <= 0.08 * max(conf[t], 1) for t in CODES):
            hit.append((k1, v1, k2, v2))
    K.check("lens swap: no referral-log column or pair reproduces every trust's confirmable count within 8%",
            not hit, hit[:3])
    # no shipped artifact orders the trusts on the decision question
    cap = pd.read_excel(Path(target) / F["capacity"], sheet_name="Referral waits")
    first = cap[cap["Month"] == cap["Month"].iloc[0]]["Referring trust"].tolist()
    K.check("capacity report lists trusts in code order, never ranked; no file ranks deaths a review could confirm",
            first == ["RIS", "TAN", "BRK", "STN", "LAT", "ELL", "PRW", "PEL"])
    # the capacity report reproduces from the returns and the referral log
    import extracts
    returns = pd.read_csv(Path(target) / F["returns"]).to_dict("records")
    ref = pd.read_csv(Path(target) / F["referrals"], dtype=str, keep_default_na=False).to_dict("records")
    for r in ref:
        r["level_of_care"] = int(r["level_of_care"])
    occ_rows, wait_rows = extracts.capacity_figures(returns, ref)
    occ = pd.read_excel(Path(target) / F["capacity"], sheet_name="Occupancy 0800")
    ok1 = [round(float(x), 1) for x in occ["Occupied at 08:00 (mean)"]] == [r["occupied_0800_mean"] for r in occ_rows]
    ok2 = cap["Waiting over 4 hours from receipt"].tolist() == [r["over_4h_from_receipt"] for r in wait_rows]
    K.check("capacity report reproduces to the last digit from the returns and the referral log", ok1 and ok2)
    # the licensed wrong basis: the programme's screen (from receipt) ranks E first and is not the answer
    scr = cap.groupby("Referring trust")["Waiting over 4 hours from receipt"].sum()
    K.check("the licensed screen (waits over four hours from receipt) leads with E, not D", scr.idxmax() == "LAT",
            scr.to_dict())


# ===================================================================================== asks
def ask_checks(K, D):
    a = G.asks(D)
    K.check("golden record: 24 trust figures and 3 totals as designed", a == GOLDEN_RECORD, a["total"])
    ys = {y: G.asks(D, years=(y,))["total"] for y in (1, 2, 3)}
    K.check("yearly series: patients 695/737/731, deaths 204/212/213, confirmable 54/50/44",
            ys == {1: (695, 204, 54), 2: (737, 212, 50), 3: (731, 213, 44)}, ys)
    dg = {y: (G.asks(D, years=(y,))[D_][2], G.asks(D, years=(y,))[G_][2]) for y in (1, 2, 3)}
    K.check("D 25/28/27 and G 14/17/15 confirmable by year", dg == {1: (25, 14), 2: (28, 17), 3: (27, 15)}, dg)
    K.check("latest four quarters per trust exactly as designed", G.year_table(D) == GOLDEN_Y3)
    flat = [v for t in CODES for v in a[t]] + list(a["total"])
    K.check("every graded figure is an integer count", all(isinstance(v, int) for v in flat))
    tots = [a["total"][0], a["total"][1], a["total"][2]]
    K.check("generation tells: no headline total on a round boundary", all(v % 10 != 0 and v % 25 != 0 for v in tots), tots)
    split = defaultdict(lambda: [set(), set()])
    ws = G.waits(D)
    for x in G.classify(D, ws):
        if x["died"] and (x["empty"] or x["alloc"]):
            split[x["trust"]][0 if x["empty"] else 1].add(x["person"])
    sp = {LET[t]: (len(v[0]), len(v[1])) for t, v in split.items()}
    K.check("confirmable split: empty-bed waits A6 C1 F6 G45 H3, allocation waits A2 C4 D80 G1",
            sp == {"A": (6, 2), "C": (1, 4), "D": (0, 80), "F": (6, 0), "G": (45, 1), "H": (3, 0)}, sp)
    # E also leads the deaths before a bed was assigned
    dw = defaultdict(set)
    for w in ws:
        if w["outcome"] == "Died before admission" and G.year_of(w["dta"].date()) == 3:
            dw[w["trust"]].add(w["person"])
    dwc = {LET[t]: len(v) for t, v in dw.items()}
    K.check("E leads deaths after long waits and deaths before a bed was assigned (Y3)", max(dwc, key=dwc.get) == "E",
            dwc)


# ===================================================================================== device layer
def subsets(items):
    for k in range(len(items) + 1):
        for c in itertools.combinations(items, k):
            yield c


def device_checks(K, D, S, target, F):
    nat = G.asks(D, handle=())
    K.check("natural path (every device mishandled) lands on the designed stop 1 for 3a, 3b, 3c", nat == NATURAL,
            nat["total"])
    gold = G.asks(D)
    # each device alone
    alone = {}
    ok = True
    for dv in G.DEVICES:
        h = tuple(x for x in G.DEVICES if x != dv)
        v = G.asks(D, handle=h)
        alone[dv] = v
        for t in CODES:
            delta = tuple(v[t][i] - gold[t][i] for i in range(3))
            if delta != DELTAS[dv][t]:
                ok = False
                print("      delta %s %s %s want %s" % (dv, LET[t], delta, DELTAS[dv][t]))
    K.check("each device alone moves exactly its designed deltas per trust per figure", ok)
    cover = {}
    for t in CODES:
        for i, nm in enumerate(("3a", "3b", "3c")):
            n = sum(1 for dv in G.DEVICES if DELTAS[dv][t][i] != 0)
            cover[(LET[t], nm)] = n
    thin = {k: v for k, v in cover.items() if v < 3 and not (k[1] == "3c" and k[0] in ("B", "E"))}
    K.check("at least three devices on every graded figure but B's and E's 3c", not thin, thin)
    # necessity: every device moves a figure at every trust it is planted at
    ok = all(any(DELTAS[dv][t][i] != 0 for i in range(3)) for dv, ts in PLANTED.items() for t in ts)
    K.check("necessity matrix: each device moves a figure at every trust it is planted at", ok)
    # no-cancel over every subset of mishandlings, per trust and figure and per total
    cache = {}

    def run(mish, construction="decisive"):
        key = (tuple(sorted(mish)), construction)
        if key not in cache:
            cache[key] = G.asks(D, handle=tuple(x for x in G.DEVICES if x not in mish), construction=construction)
        return cache[key]

    land = []
    for sub in subsets(G.DEVICES):
        if not sub:
            continue
        v = run(sub)
        for t in CODES + ["total"]:
            for i in range(3):
                if t == "total":
                    touched = any(DELTAS[dv][x][i] != 0 for dv in sub for x in CODES)
                else:
                    touched = any(DELTAS[dv][t][i] != 0 for dv in sub)
                if touched and v[t][i] == gold[t][i]:
                    land.append((sub, t, i))
    K.check("no-cancel: no subset of mishandled devices lands any touched figure on its golden (511 subsets)",
            not land, land[:3])
    # each wrong reading of own care: no subset of mishandlings lands its 3c on the golden where the reading differs
    for m in MIRRORS:
        base_m = run((), m)
        differ = [t for t in CODES if base_m[t][2] != gold[t][2]]
        landm = []
        for sub in subsets(G.DEVICES):
            v = run(sub, m)
            for t in differ:
                if v[t][2] == gold[t][2]:
                    landm.append((sub, LET[t]))
        K.check("%s path: no subset of mishandlings lands on the golden 3c where the reading differs (%s)"
                % (m, "".join(LET[t] for t in differ)), bool(differ) and not landm, landm[:3])
    # over-corrections: each a distinct stop off the golden
    overs = {}
    for dv in G.DEVICES:
        v = G.asks(D, over=dv)
        overs[dv] = v
        moved = [(LET[t], i) for t in CODES for i in range(3) if v[t][i] != gold[t][i]]
        K.check("over-correction of %s lands off the golden" % dv, bool(moved) and v["total"] != gold["total"],
                "total %s vs %s" % (v["total"], gold["total"]))
    # the main call with every device mishandled, and on the record window
    R, _ = G.ladder(D)
    ws = G.waits(D, handle=())
    cl = [x for x in G.classify(D, ws, handle=()) if x["year"] == 3 and x["died"]]
    r4 = defaultdict(set)
    for x in cl:
        if x["empty"] or x["alloc"]:
            r4[x["trust"]].add(x["person"])
    r4n = {t: len(r4[t]) for t in CODES}
    K.check("main call identical with every device mishandled (D 27 over G 15)", r4n == R[4], r4n)
    K.check("on the whole record D leads with devices handled or not",
            G.leader({t: gold[t][2] for t in CODES})[0] == D_ and G.leader({t: nat[t][2] for t in CODES})[0] == D_)
    # zero device and hazard rows inside the main call's declared population
    y3 = [r for r in D.refs if G.year_of(r["dta"].date()) == 3 if not r["legacy"]]
    legacy_y3 = [r for r in D.refs if r["legacy"] and r["dta"] and r["dta"].date() >= dt.date(2025, 7, 1)]
    temp_y3 = [r for r in D.refs if r["key"] in D.temp and r["dta"].date() >= dt.date(2025, 6, 1)]
    lev_y3 = D.lev[D.lev["referral_id"].isin({r["id"] for r in y3})]
    lb = D.stays[D.stays["stay_id"].str.startswith("LB") & (D.stays["discharged_at"] >= pd.Timestamp("2025-06-01"))]
    par = [r for r in D.refs if r["id"][:5] in ("R2402", "R2403") and r["dta"].date() >= dt.date(2025, 6, 1)]
    multi = D.stays[D.stays["admitted_at"] >= pd.Timestamp("2025-06-01")].groupby(["unit_code", "patient_key"]).size()
    dst_y3 = [w for w in G.waits(D) if w["end"] is not None and G.year_of(w["dta"].date()) == 3 and
              G.wait_minutes(w, set()) != G.wait_minutes(w, set(G.DEVICES))]
    rep_y3 = [p for p, n in Counter(x["person"] for x in G.classify(D, G.waits(D)) if x["year"] == 3).items() if n > 1]
    starts = {(r.unit_code, D.temp.get(r.patient_key, r.patient_key), r.admitted_at.strftime("%Y-%m-%d %H:%M"))
              for r in D.stays.itertuples(index=False)}
    tx = D.tx
    held_y3 = sum(1 for r in tx.itertuples(index=False) if r.bed_confirmed_at >= "2025-06-01" and
                  (r.to_unit, D.temp.get(r.patient_key, r.patient_key), r.bed_confirmed_at) not in starts)
    never_y3 = [r for r in D.refs if r["key"].startswith("U") and r["key"] not in D.temp and
                r["dta"].date() >= dt.date(2025, 6, 1)]
    counts = {"DV1/DV4 legacy rows": len(legacy_y3), "DV2 temporary keys": len(temp_y3), "DV4 level entries": len(lev_y3),
              "DV5 waits across a clock change": len(dst_y3), "DV7 repeat long-wait patients": len(rep_y3),
              "DV8 stays dated from the arrival": held_y3, "DV9 unlinked temporary keys": len(never_y3),
              "HZ1 bed-episode rows": len(lb), "HZ2 copies": len(par)}
    K.check("zero device and hazard rows inside the main call's declared population, per device",
            all(v == 0 for v in counts.values()), counts)
    # DV8: the legacy bed list dates a transfer's stay from the arrival, the platform from the bed's allocation
    leg = tx[tx["bed_confirmed_at"] < "2024-04-02"]
    plat = tx[tx["bed_confirmed_at"] >= "2024-04-02"]
    res = lambda k: D.temp.get(k, k)
    on_arr = sum(1 for r in leg.itertuples(index=False) if (r.to_unit, res(r.patient_key), r.arrived_at) in starts)
    on_conf = sum(1 for r in plat.itertuples(index=False) if (r.to_unit, res(r.patient_key), r.bed_confirmed_at) in starts)
    span8 = 0
    for r in leg.itertuples(index=False):
        a_, b_ = G.p_ts(r.bed_confirmed_at), G.p_ts(r.arrived_at)
        t8 = dt.datetime.combine(a_.date(), dt.time(8, 0))
        if a_ < t8 < b_ or a_ < t8 + dt.timedelta(days=1) < b_:
            span8 += 1
    K.check("DV8: every legacy transfer's stay begins at the arrival, every platform transfer's at the allocation; no "
            "held bed spans 08:00", on_arr == len(leg) and on_conf == len(plat) and span8 == 0,
            "legacy %d of %d, platform %d of %d, spanning 08:00 %d" % (on_arr, len(leg), on_conf, len(plat), span8))
    n8 = sum(DELTAS["DV8"][t][0] for t in CODES)
    K.check("DV8: only the designed legacy transfers read past four hours at the arrival (18 near misses, 8 summer "
            "clock rows, 2 clock-change-night rows); held beds sit only inside the designed capacity waits",
            n8 == 28 and sum(DELTAS["DV8"][t][2] for t in CODES) == 35, (n8, sum(DELTAS["DV8"][t][2] for t in CODES)))
    # DV9: temporary identities never resolved; the death is only on the temporary-key spell's discharge method
    never = [r for r in D.refs if r["key"].startswith("U") and r["key"] not in D.temp]
    gcl = {x["id"]: x for x in G.classified(D, G.DEVICES)}
    epkeys = set(D.ep["patient_key"])
    ok9 = (len(never) == 10 and all(r["id"] in gcl and gcl[r["id"]]["died"] for r in never)
           and all(D.dod.get(r["key"]) is None and r["key"] in D.dmeth and r["key"] in epkeys for r in never))
    K.check("DV9: ten long waits under temporary keys the links never resolve, each death recorded only as a spell "
            "ending in death under that key (no date of death); the referral-to-episode join still matches",
            ok9, "%d unresolved keys" % len(never))
    # hygiene battery on the natural path
    ref = D.ref
    st = D.stays
    exact_dupes = int(ref.duplicated(subset=[c for c in ref.columns if c != "referral_id"]).sum())
    leg_adm = [r for r in D.refs if r["legacy"] and r["outcome"] == "Admitted" and r["unit"] in D.l3_units(r["dta"].date())]
    unmatched = sum(1 for r in leg_adm if r["id"] not in D.assign_of)
    fan = int(st[st["referral_id"] != ""].groupby("referral_id").size().max())
    keys = D.reg[D.reg["valid_to"] == ""].groupby("unit_code").size().max()
    K.check("hygiene battery clean on the natural path (unique keys, no exact duplicates, no unmatched or fanned joins)",
            ref["referral_id"].is_unique and st["stay_id"].is_unique and exact_dupes == 0 and unmatched == 0 and
            fan == 1 and keys == 1, (exact_dupes, unmatched, fan, keys))
    # the pair simulation at planning weights: 38 / 7 / 55 over 32 ask criteria
    pair, singles, doubles, prof = pair_simulation(D, gold, run)
    K.check("pair simulation at or under 40 with every device missed (best mirror of seven readings)", pair <= 40,
            "%.1f" % pair)
    K.check("every single device catch leaves the pair at or under 40; the worst double reported",
            max(singles.values()) <= 40, "max single %.1f (%s); worst double %.1f %s" % (
                max(singles.values()), max(singles, key=singles.get), doubles[0][0], doubles[0][1]))
    K.check("round 2's own profile (every earlier device caught, DV8 and DV9 missed) leaves the pair at or under 40",
            prof["round 2's catches (every device before loop 2)"] <= 40,
            "; ".join("%s %.1f" % kv for kv in prof.items()))
    # the referee: byte-clean, transfers only, local decision times, verified keys
    tx = pd.read_csv(Path(target) / F["transfers"], dtype=str, keep_default_na=False)
    own_ok = all(not t.startswith(f[:3]) for f, t in zip(tx["from_trust"], tx["to_unit"]))
    clean = tx["transfer_ref"].is_unique and not tx.duplicated().any() and not (tx == "").any().any()
    shareall = len(tx) / max(1, len(D.refs))
    tempkeys = tx["patient_key"].isin(D.temp.keys()).sum()
    refkeys = {(r["key"], r["trust"]) for r in D.refs} | {(D.temp.get(r["key"], r["key"]), r["trust"]) for r in D.refs}
    keyed = all((k, f) in refkeys for k, f in zip(tx["patient_key"], tx["from_trust"]))
    K.check("referee: transfer audit byte-clean, transfers between trusts only, keys as the referral's patient, "
            "no merged temporary key, no deaths or levels",
            own_ok and clean and tempkeys == 0 and keyed and not {"level_of_care", "date_of_death"} & set(tx.columns),
            "%d transfers (%.0f%% of referrals)" % (len(tx), 100 * shareall))
    lw = [x for x in G.classify(D, G.waits(D))]
    tr = sum(1 for x in lw if x["unit"] and not x["unit"].startswith(x["trust"]))
    K.check("referee covers a minority of long waits (hands over no column)", tr / len(lw) < 0.5,
            "%.0f%% of long waits are transfers" % (100 * tr / len(lw)))
    # organs: two files per device, neither a main-path document; one primary's documentary organ per file
    docs_txt = doc_texts(target, F)
    organs = {"DV4": ("levels", "legacyspec", "requested by the referring team"),
              "DV1": ("transfers", "legacyspec", "held in UTC"),
              "DV2": ("links", "apcspec", "temporary registration"),
              "DV3": ("register", "boardpaper", "level 2 care only"),
              "DV5": ("capacity", "legacyspec", "records local time"),
              "DV7": ("referrals", "apcspec", "verified key"),
              "DV8": ("transfers", "legacyspec", "placed in the bed"),
              "DV9": ("episodes", "apcspec", "carry no date of death"),
              "HZ1": ("stays", "legacyspec", "one row per bed episode"),
              "HZ2": ("referrals", "thread", "on both CCRS and the platform")}
    main_docs = ("remit", "guide", "capacity")
    ok = True
    bad_org = []
    for dv, (struct, doc, phrase) in organs.items():
        if struct == doc or doc in main_docs or phrase.lower() not in docs_txt[doc].lower():
            ok = False
            bad_org.append(dv)
    prim = {"DV8": "legacyspec", "DV9": "apcspec", "DV3": "boardpaper"}
    K.check("each device's two organs in two files, the documentary one off the main path; one primary per file",
            ok and len(set(prim.values())) == 3, bad_org)
    vocab = ["UTC", "requested by", "temporary", "bed episode", "both CCRS", "pilot ward", "parallel run",
             "level 2 care only", "winter bank", "moved to another bed", "clock change", "clocks", "summer time",
             "BST", "GMT", "daylight", "repatriat", "placed in the bed", "discharge method", "elective centre"]
    prompt = (HERE.parent / "prompt.md").read_text()
    def has(w, t):
        return re.search(r"\b" + re.escape(w) + r"\b", t, re.I) is not None
    found = [(w, k) for k in main_docs for w in vocab if has(w, docs_txt[k])]
    found += [(w, "prompt") for w in vocab if has(w, prompt)]
    K.check("device vocabulary absent from every main-path document and the prompt", not found, found)
    # spans counted from the golden's code path (data files read plus the documents that adjudicate)
    spans = {"3a": ["referrals", "stays", "levels", "links", "transfers", "legacyspec", "apcspec", "remit", "guide"],
             "3b": ["referrals", "stays", "levels", "links", "transfers", "legacyspec", "apcspec", "remit", "guide",
                    "episodes"],
             "3c": ["referrals", "stays", "levels", "links", "transfers", "legacyspec", "apcspec", "remit", "guide",
                    "episodes", "register", "returns", "boardpaper"]}
    cols = {"3a": ["referral_id", "received_at", "referring_trust", "patient_key", "dta_at", "level_of_care", "outcome",
                   "outcome_at", "stays.referral_id", "stays.admitted_at", "stays.unit_code", "stays.patient_key",
                   "levels.entry", "levels.level", "links.temporary_key", "links.verified_key",
                   "transfers.patient_key", "transfers.to_unit", "transfers.bed_confirmed_at",
                   "transfers.arrived_at"],
            "3b": ["+3a", "episodes.patient_key", "episodes.date_of_death", "episodes.discharge_method",
                   "episodes.discharge_date"],
            "3c": ["+3b", "stays.discharged_at", "register.trust_code", "register.valid_from", "register.valid_to",
                   "register.care_level", "returns.beds_open"]}
    ncol = {"3a": len(cols["3a"]), "3b": len(cols["3a"]) + 4, "3c": len(cols["3a"]) + 4 + 6}
    K.check("span: 3a, 3b, 3c each touch >= 8 files and >= 10 columns on the golden's code path",
            all(len(v) >= 8 for v in spans.values()) and all(v >= 10 for v in ncol.values()),
            {k: (len(v), ncol[k]) for k, v in spans.items()})


MIRRORS = ("census", "any", "planned", "not02", "queue", "local", "t04")
OLD8 = ("DV1", "DV2", "DV3", "DV4", "DV5", "DV7", "HZ1", "HZ2")
PROFILES = {"round 1's catches (six stage-2 devices and the discharge-method fallback)":
            ("DV1", "DV2", "DV3", "DV4", "HZ1", "HZ2", "DV9"),
            "round 2's catches (every device before loop 2)": OLD8,
            "round 2's catches and DV9": OLD8 + ("DV9",),
            "round 2's catches and DV8": OLD8 + ("DV8",),
            "every device": None}


def pair_simulation(D, gold, run):
    """The pair at planning weights 38 / 7 / 55 over 32 ask criteria: the cracker files D on the decisive
    construction, the mirror misses the call on the reading that scores best for it (census, any admission, the
    admission-type readings, the queue reading). Both make the same device catches."""
    w_rec, w_if, w_ask, n_ask = 38.0, 7.0, 55.0, 32
    per = w_ask / n_ask
    fig = [(t, i) for t in CODES for i in range(3)] + [("total", i) for i in range(3)]

    def score(v, cracker):
        hits = sum(1 for t, i in fig if v[t][i] == gold[t][i])
        chart = 5 if cracker else 1
        return (w_rec if cracker else 5.0) + w_if + per * (hits + chart)

    def pair_for(handled):
        mish = tuple(x for x in G.DEVICES if x not in handled)
        vc = score(run(mish, "decisive"), True)
        vm = max(score(run(mish, m), False) for m in MIRRORS)
        return (vc + vm) / 2

    base = pair_for(())
    singles = {dv: pair_for((dv,)) for dv in G.DEVICES}
    doubles = sorted(((pair_for(c), c) for c in itertools.combinations(G.DEVICES, 2)), reverse=True)
    prof = {k: pair_for(G.DEVICES if h is None else h) for k, h in PROFILES.items()}
    return base, singles, doubles, prof


def doc_texts(target, F):
    from pypdf import PdfReader
    import docx
    out = {}
    for k, name in F.items():
        p = Path(target) / name
        if p.suffix == ".pdf":
            out[k] = "\n".join(pg.extract_text() or "" for pg in PdfReader(str(p)).pages)
            out[k] = re.sub(r"\s+", " ", out[k])
        elif p.suffix == ".docx":
            d = docx.Document(str(p))
            out[k] = " ".join([x.text for x in d.paragraphs] + [c.text for t in d.tables for row in t.rows for c in row.cells])
        elif p.suffix in (".txt", ".eml"):
            out[k] = re.sub(r"\s+", " ", p.read_text())
        elif p.suffix == ".xlsx":
            import openpyxl
            wb = openpyxl.load_workbook(p, read_only=True)
            out[k] = " ".join(str(c) for ws in wb.worksheets for row in ws.iter_rows(values_only=True) for c in row
                              if c is not None and isinstance(c, str))
        else:
            out[k] = ""
    return out


# ===================================================================================== pack gates and hygiene
def norm_name(s):
    gen = set("""the and of on upon in by at under over st saint north south east west great little upper lower new old
nhs trust trusts foundation hospital hospitals university teaching general district royal county city town
network region regional health board care critical adult unit units review clinical services service ltd limited
llp bridge vale hill hills green park street road lane cross heath common end wood moor dale mere water infirmary""".split())
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z ]", " ", s)
    return "".join(w for w in s.split() if w not in gen)


def lev2(a, b):
    if abs(len(a) - len(b)) > 2:
        return 3
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        prev = cur
    return prev[-1]


def pack_checks(K, D, S, target, F, meta, distractors):
    files = sorted(p.name for p in Path(target).iterdir() if p.is_file())
    fmts = sorted({Path(x).suffix.lstrip(".") for x in files})
    K.check("input gate: 10 or more files", len(files) >= 10, len(files))
    K.check("input gate: 3 or more distinct formats", len(fmts) >= 3, fmts)
    nref = len(D.ref)
    K.check("input gate: a file of 25,000 or more rows (and a real database file)", nref >= 25000 and
            Path(target, F["reviewdb"]).stat().st_size > 5_000_000, "referral log %d rows" % nref)
    dfiles = meta.get("distractor_files", [])
    K.check("input gate: two or more distractors named in metadata.json", len(dfiles) >= 2 and
            all(x in files for x in dfiles), dfiles)
    alltext = ""
    for p in Path(target).iterdir():
        try:
            alltext += p.read_bytes().decode("latin-1").lower()
        except Exception:
            pass
    K.check("the word 'distractor' appears nowhere under target/", "distractor" not in alltext and
            not any("distractor" in x for x in files))
    # distractors unused: the golden recomputes unchanged with each removed
    R, _ = G.ladder(D)
    a = G.asks(D)
    for k in distractors:
        with tempfile.TemporaryDirectory() as tmp:
            t2 = Path(tmp) / "t"
            shutil.copytree(target, t2)
            (t2 / F[k]).unlink()
            D2 = G.Data(t2, F)
            same = G.ladder(D2)[0] == R and G.asks(D2) == a
        K.check("distractor %s unused: every figure unchanged with it deleted" % F[k], same)
    K.check("metadata.json lists exactly the shipped files", sorted(f["path"] for f in meta["files"]) == files)
    K.check("metadata.json names domain, objective and the three deliverables, and carries no answer",
            meta["domain"] == "Policy & Education" and meta["objective"] == "Anomaly Detection & Diagnostics" and
            len(meta["deliverables"]) == 3 and "STN" not in json.dumps(meta) and "Stennock" not in json.dumps(meta))
    # the field guide registers every other file by name
    txt = doc_texts(target, F)
    guide = txt["guide"].replace(" ", "")
    missing = [x for x in files if x != F["guide"] and x.replace(" ", "") not in guide]
    K.check("field guide lists every other shipped file by name (H9)", not missing, missing)
    # single-statement rule for every pin
    pins = {"more than four hours from the decision to admit to the assignment of a bed": "remit",
            "within 30 days of the decision to admit": "remit",
            "own care": "remit",
            "latest four complete quarters": "remit",
            "the minute the bed was assigned": "guide",
            "valid_from to valid_to inclusive": "guide",
            "within 14 days of a death": "guide",
            "held in UTC": "legacyspec",
            "requested by the referring team": "legacyspec",
            "one row per bed episode": "legacyspec",
            "temporary registration": "apcspec",
            "on both CCRS and the platform": "thread",
            "level 2 care only": "boardpaper",
            "bed bureau allocated the bed": "guide",
            "records local time": "legacyspec",
            "placed in the bed": "legacyspec",
            "carry no date of death": "apcspec"}
    bad = []
    for phrase, home in pins.items():
        where = [k for k, t in txt.items() if phrase.lower() in t.lower()]
        if where != [home]:
            bad.append((phrase, where))
    K.check("single-statement rule: every pin stated in exactly one shipped file", not bad, bad)
    # producer metadata and timestamps (H1, H7)
    import writers
    flagged = []
    for p in sorted(Path(target).iterdir()):
        r = writers.SCRUB.audit(str(p), "2023-06-01", "2026-10-02")
        if r is not None and (r[0] or r[1]):
            flagged.append((p.name, r))
    K.check("no writer name and no out-of-band timestamp in any shipped binary", not flagged, flagged)
    pq_meta = []
    import pyarrow.parquet as pq
    for p in Path(target).glob("*.parquet"):
        md = pq.ParquetFile(str(p)).metadata
        if md.metadata:
            pq_meta.append(p.name)
    K.check("parquet files carry no schema metadata", not pq_meta, pq_meta)
    mt = {round(p.stat().st_mtime) for p in Path(target).iterdir()}
    K.check("file times normalised to one in-fiction export time", len(mt) == 1,
            dt.datetime.fromtimestamp(list(mt)[0]).isoformat() if len(mt) == 1 else mt)
    # ISO dates after the as-of date anywhere in the shipped text
    late = []
    for p in Path(target).iterdir():
        if p.suffix in (".csv", ".txt", ".eml"):
            t = p.read_text(errors="ignore")
            hits = [m for m in re.findall(r"\b(20\d\d-\d\d-\d\d)\b", t) if m > AS_OF.isoformat()]
            if hits:
                late.append((p.name, len(hits)))
    K.check("no ISO date after the as-of date in any shipped text file", not late, late)
    # column names and nulls
    flag = re.compile(r"(^|_)(true|truth|actual|hidden|trap|flag|is_|seed|synthetic|gen_|generated|golden|answer|"
                      r"correct|naive|rung|device|hazard|planted|debug|tmp|temp|internal)(_|$)", re.I)
    badcols = []
    for p in Path(target).glob("*.csv"):
        head = p.read_text().split("\n", 1)[0].split(",")
        badcols += [(p.name, c) for c in head if flag.search(c)]
        first = "\n".join(p.read_text().split("\n")[:60])
        if re.search(r"\b(nan|NaN|None|NULL|True|False)\b", first):
            badcols.append((p.name, "python null"))
    for p in Path(target).glob("*.parquet"):
        badcols += [(p.name, c) for c in pq.ParquetFile(str(p)).schema.names if flag.search(c)]
    K.check("no generator-style column names and no Python nulls in the data files", not badcols, badcols)
    # author vocabulary and em dashes in every shipped document
    bad_words = re.compile(r"\b(trap|decoy|rung|stump|golden|determinis\w*|synthetic|generator|distractor|ladder|"
                           r"answer key|solver)\b|\u2014", re.I)
    hits = [(k, m.group(0)) for k, t in txt.items() for m in [bad_words.search(t)] if m]
    K.check("no author vocabulary or em dash in any shipped document", not hits, hits)
    # invented names: clear of real places and organisations (H21) and of every other card's invented names
    ref = [l.strip() for l in open(HERE / "h21_reference_places.txt") if l.strip()]
    ref += [l.strip() for l in open(HERE / "h21_reference_nhs.txt") if l.strip()]
    rems = [(r, norm_name(r)) for r in ref]
    rems = [(r, m) for r, m in rems if len(m) >= 4]
    cards = []
    for p in sorted((REPO / ".claude/skills/fingerprint/cards").glob("*.json")):
        if p.stem == "task119":
            continue
        c = json.loads(p.read_text())
        cards += [(n, norm_name(n)) for n in ((c.get("world") or {}).get("invented_names") or []) if len(norm_name(n)) >= 4]
    clash = []
    for name in INVENTED_NAMES:
        m = norm_name(name)
        if len(m) < 4:
            continue
        for r, rm in rems + cards:
            if lev2(m, rm) <= 2 or (len(rm) >= 5 and rm in m) or (len(m) >= 5 and m in rm):
                clash.append((name, r))
                break
    K.check("invented names clear of real places and NHS organisations and of other cards' names (H21)", not clash,
            clash[:5])
    # no uniform row counts across the data files
    rows = [f["rows"] for f in meta["files"] if f.get("rows")]
    K.check("generation tells: no two data files share a row count", len(rows) == len(set(rows)), rows)
