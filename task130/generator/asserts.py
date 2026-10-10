"""The assertion regime: every rung, rival-killer, calibration outcome, grid cell, ask stop, device
magnitude, separation count, leak sweep and input gate, asserted on the files as shipped."""
import datetime as dt
import itertools
import os
import random
import re
from decimal import Decimal

import analysis as A
from common import D, HOLIDAYS, add_months, add_workdays, bin_margin, r1, workday
from plan import SECTIONS

WATCH = sorted(s["code"] for s in SECTIONS)
ROLE = {s["code"]: s["role"] for s in SECTIONS}
CODE = {s["role"]: s["code"] for s in SECTIONS}
ANSWER = sorted(CODE[r] for r in ("A1", "A2", "A3", "A4", "Q", "U"))
EXPECT = {"R0": ("A1", "A3", "A4", "P", "O4"), "R1": ("A1", "A2", "A3", "A4", "P", "Q", "O4"),
          "R2": ("A1", "A2", "A3", "A4", "P", "S", "Q", "T"), "R3": ("A1", "A2", "A3", "A4", "P", "S", "U"),
          "R4": ("A1", "A2", "A3", "A4", "P", "U"), "R4p": ("A1", "A2", "A3", "A4", "U"),
          "R5": ("A1", "A2", "A3", "A4", "Q", "U")}


class Checks:
    def __init__(self):
        self.n = 0
        self.log = []

    def ok(self, cond, label):
        assert cond, f"ASSERTION FAILED: {label}"
        self.n += 1
        self.log.append(label)


def names(sec_list):
    return sorted(ROLE[s] for s in sec_list)


# ---- the conformance toggles, for the correction grid ------------------------------------------
def picture_toggles(ret, quarter, cutoff, cad, V, B, X, K):
    """V versions and no-change carry; B building rows expanded; X option and reservation rows
    dropped; K references repaired. Returns {key: holder} and scheduled {key: (date, buyer, price)}."""
    lod = {}
    for r in ret:
        if r["data_presentacio"] <= cutoff:
            lod.setdefault((r["nif_declarant"], r["trimestre"]), {}).setdefault(r["id_declaracio"], []).append(r)
    qorder = sorted({q for _, q in lod})
    own, sch = {}, {}
    for h in sorted({h for h, _ in lod}):
        if not V:
            if (h, quarter) not in lod:
                continue
            vs = lod[(h, quarter)]
            rows = vs[max(vs, key=lambda i: (vs[i][0]["data_presentacio"], i))]
        else:
            qs = [q for q in qorder if q <= quarter and (h, q) in lod]
            if not qs:
                continue
            vs = lod[(h, qs[-1])]
            rows = []
            for vid in sorted(vs, key=lambda i: (vs[i][0]["data_presentacio"], i)):
                rows = list(vs[vid]) if vs[vid][0]["tipus_declaracio"] in ("O", "S") else rows + list(vs[vid])
        for r in rows:
            if X and r["codi_tinenca"] != "PD":
                continue
            raw = r["referencia_cadastral"]
            s = (r["data_transmissio_prevista"], r["nif_adquirent_previst"], r["preu_convingut"]) \
                if r["data_transmissio_prevista"] else None
            if r["unitats"]:
                parcel = re.sub(r"\s", "", raw).upper() if K else raw
                if parcel not in cad.parcel_sec:
                    continue
                if B:
                    keys = [cad.by_unit[(parcel, u)] for u in A.expand_units(r["unitats"])]
                else:
                    keys = [f"{parcel}#{r['id_declaracio']}#{r['unitats']}"]
            else:
                ref = cad.repair(raw) if K else (raw if raw in cad.sec else None)
                if ref is None:
                    continue
                keys = [ref]
            for k in keys:
                if r["codi_tinenca"] != "PD":
                    k = k + "#" + r["codi_tinenca"] + h
                own[k] = h
                if s:
                    sch[k] = s
    return own, sch


def key_section(cad, k):
    base = k.split("#")[0]
    return cad.sec.get(base) or cad.parcel_sec.get(base)


def grid_counts(own, cad):
    c = {s: 0 for s in WATCH}
    for k in own:
        s = key_section(cad, k)
        if s in c:
            c[s] += 1
    return c


def roll_variant(own, sch, L, tk, variant):
    lh, deeds = L["lh"], L["deeds"]
    if variant == "none":
        return own
    if variant == "deeds":
        return A.roll(own, {}, deeds, lh, "2026-06-30", "2026-09-30", "2026-09-30", "2027-01-01")
    return A.roll(own, sch, deeds, lh, "2026-06-30", "2026-09-30", "2026-09-30", "2027-01-01", tk, variant)


def takeovers_with(L, fn):
    """Ledger commitments with a completion date computed by fn(commit_date) -> date."""
    out = {}
    for ref, (c, _) in A.ledger_takeovers(L["led"], 120).items():
        cd = dt.date.fromisoformat(c)
        out[ref] = (c, fn(cd).isoformat())
    return out


def main_ladder(C, W, L, R):
    cad = L["cad"]
    sets = {m: A.designated(R["C"][m], cad, WATCH) for m in EXPECT}
    for m, exp in EXPECT.items():
        C.ok(names(sets[m]) == sorted(exp), f"rung {m} files {sorted(exp)}")
    C.ok(len({tuple(v) for v in sets.values()}) == len(sets), "every rung files a distinct set")
    C.ok([m for m in sets if sets[m] == ANSWER] == ["R5"], "only R5 files the answer set")
    pos = {}
    for m in sets:
        dist = len(set(sets[m]) ^ set(ANSWER))
        pos[m] = (len(sets[m]), dist)
    C.ok(pos == {"R0": (5, 5), "R1": (7, 3), "R2": (8, 4), "R3": (7, 3), "R4": (6, 2), "R4p": (5, 1), "R5": (6, 0)},
         f"position table {pos}")
    # bulletin and 2026 annex controls
    c2 = R["C"]["R2"]
    for m, floor_n in (("R1", 8), ("R0", 11)):
        miss = [s for s in WATCH if abs(R["C"][m][s] - c2[s]) >= 4]
        C.ok(len(miss) >= floor_n, f"{m} misses the bulletin on {len(miss)} sections by 4 or more (floor {floor_n})")
    # R3 to R5 deltas
    d35 = {s: R["C"]["R5"][s] - R["C"]["R3"][s] for s in WATCH}
    touched = [s for s in WATCH if d35[s]]
    C.ok(len(touched) == 12 and all(abs(d35[s]) >= 3 for s in touched), f"R3 to R5 moves 12 sections by 3+ {d35}")
    C.ok(all(r1(A.share(R["C"]["R5"][s], cad.N[s])) != r1(A.share(R["C"]["R3"][s], cad.N[s])) for s in touched),
         "the one-decimal share differs between R3 and R5 in every touched section")
    C.ok(sorted(ROLE[s] for s in WATCH if not d35[s]) == ["O4", "O5"], "the agency touches neither Castelló section")
    signs = sorted(ROLE[s] for s in touched if d35[s] > 0)
    C.ok(signs == ["A2", "O2", "Q"], f"the decisive move raises exactly A2, O2 and Q {signs}")
    # line clearance and bins on the answer
    sh5 = {s: A.share(R["C"]["R5"][s], cad.N[s]) for s in WATCH}
    C.ok(all(abs(sh5[s] - 25) >= Decimal("0.5") for s in WATCH), "every answer share at least 0.5 points from 25")
    C.ok(all(bin_margin(sh5[s]) >= Decimal("0.015") for s in WATCH),
         f"every answer share at least 0.015 points inside its bin (min {min(bin_margin(sh5[s]) for s in WATCH)})")
    des = [s for s in WATCH if sh5[s] >= 25]
    und = [s for s in WATCH if sh5[s] < 25]
    near_d = min(des, key=lambda s: sh5[s])
    near_u = max(und, key=lambda s: sh5[s])
    C.ok(ROLE[near_d] == "Q" and ROLE[near_u] == "P", "the nearest sections either side of the line are Q and P")
    nd2 = sorted(sh5[s] for s in des)[1]
    nu2 = sorted((sh5[s] for s in und), reverse=True)[1]
    C.ok(nd2 - sh5[near_d] >= Decimal("0.3") and sh5[near_u] - nu2 >= Decimal("0.3"),
         "the nearest sections clear the next ones by 0.3 points or more")
    for s in (near_d, near_u):
        gap = abs(sh5[s] - 25)
        C.ok(bin_margin(gap) >= Decimal("0.015") and r1(gap) == abs(r1(sh5[s]) - 25),
             f"gap for {ROLE[s]} mid-bin and equal on both rounding paths ({r1(gap)})")
    # dominance on the line
    sh3 = {s: A.share(R["C"]["R3"][s], cad.N[s]) for s in WATCH}
    for role in ("P", "S", "Q"):
        s = CODE[role]
        ratio = abs(sh5[s] - sh3[s]) / abs(sh3[s] - 25)
        C.ok(ratio >= Decimal("1.3"), f"dominance {role}: decisive move / clearance = {ratio:.2f}")
    return sets, sh5, near_d, near_u


RULE = {"V": "guidance s.4-5 (S replaces, C adds, no-change carry)", "B": "portal notice (parcel rows by lodgement date)",
        "X": "guidance field codi_tinenca (OP, RS not held)", "K": "cadastre references (control characters)"}
ROLL_RULE = {"none": "order art. 4 (holdings on 1 January)", "deeds": "returns' scheduled sales (back-test 100%)",
             "R3": "agency ledger first-offer commitments", "R4": "settled purchases: deed 120 days after commitment",
             "R4p": "settled purchases: title at the deed, not the commitment", "R5": ""}


def grid(C, W, L, R):
    cad = L["cad"]
    tk = R["tk"]
    cells = {}
    for V, B, X, K in itertools.product((0, 1), repeat=4):
        own, sch = picture_toggles(L["ret"], "2026T2", "2026-08-31", cad, V, B, X, K)
        for variant in ("none", "deeds", "R3", "R4", "R4p", "R5"):
            o = roll_variant(own, sch, L, tk, variant)
            c = grid_counts(o, cad)
            st = A.designated(c, cad, WATCH)
            cells[(V, B, X, K, variant)] = st
    good = (1, 1, 1, 1, "R5")
    C.ok(cells[good] == ANSWER, "the all-correct grid cell files the answer")
    wrong = {k: v for k, v in cells.items() if k != good}
    C.ok(all(v != ANSWER for v in wrong.values()), f"each of the other {len(wrong)} grid cells files a wrong set")
    mapping = {}
    for k in wrong:
        missing = [RULE[t] for t, b in zip("VBXK", k[:4]) if not b] + ([ROLL_RULE[k[4]]] if k[4] != "R5" else [])
        mapping["".join(str(b) for b in k[:4]) + "/" + k[4]] = (names(wrong[k]), missing)
        assert missing
    C.ok(len(mapping) == 95, "every losing grid cell mapped to the shipped rule it violates")
    C.ok(cells[(1, 1, 1, 1, "R3")] == R_SETS["R3"] and cells[(1, 1, 1, 1, "none")] == R_SETS["R2"],
         "the grid's R2 and R3 cells agree with the ladder")
    C.ok(names(cells[(1, 1, 1, 1, "deeds")]) == ["A1", "A2", "A3", "A4", "P", "Q", "S", "U"],
         f"the deeds-only cell files eight sections {names(cells[(1, 1, 1, 1, 'deeds')])}")
    # partial cells on the decisive rung
    own, sch = R["own"], R["sch"]
    agr = {}
    for ref, (d, b, p) in sch.items():
        agr[ref] = (d, b in L["lh"])

    def partial(pred):
        t = {}
        for ref, (c, comp) in tk.items():
            if ref in agr and pred(ref, c, agr[ref]):
                t[ref] = (c, comp)
        o = A.roll(own, sch, L["deeds"], L["lh"], "2026-06-30", "2026-09-30", "2026-09-30", "2027-01-01", t, "R5")
        return A.designated(A.section_counts(o, cad, WATCH), cad, WATCH), A.section_counts(o, cad, WATCH)
    partials = {
        "clock only for large-holder buyers": partial(lambda r, c, a: a[1]),
        "clock only for private buyers": partial(lambda r, c, a: not a[1]),
        "clock only for agreements dated before 1 January": partial(lambda r, c, a: a[0] < "2027-01-01"),
        "clock only for commitments before 1 September": partial(lambda r, c, a: c < "2026-09-01"),
        "clock only in the sections that cross the line": partial(lambda r, c, a: cad.sec.get(r) in (CODE["P"], CODE["S"], CODE["Q"])),
    }
    for k, (st, cnt) in partials.items():
        if k.startswith("clock only in the sections"):
            C.ok(st == ANSWER and sum(cnt[s] != R["C"]["R5"][s] for s in WATCH) >= 8,
                 "taking over only in P, S and Q files the answer set but misses nine sections' counts")
        else:
            C.ok(st != ANSWER, f"partial cell '{k}' files {names(st)}")
    wd = takeovers_with(L, lambda c: add_workdays(c, 120))
    o = A.roll(own, sch, L["deeds"], L["lh"], "2026-06-30", "2026-09-30", "2026-09-30", "2027-01-01", wd, "R5")
    C.ok(A.designated(A.section_counts(o, cad, WATCH), cad, WATCH) != ANSWER, "120 working days files a wrong set")
    # the corridor: 110 to 132 calendar days and four calendar months all land on the answer
    for n in list(range(110, 133)) + ["4m"]:
        t = takeovers_with(L, (lambda c, n=n: add_months(c, 4)) if n == "4m" else (lambda c, n=n: c + dt.timedelta(days=n)))
        o = A.roll(own, sch, L["deeds"], L["lh"], "2026-06-30", "2026-09-30", "2026-09-30", "2027-01-01", t, "R5")
        assert A.section_counts(o, cad, WATCH) == R["C"]["R5"], n
    C.ok(True, "corridor: every day count 110 to 132 and four calendar months give the answer's counts")
    return cells, mapping, partials


R_SETS = {}


def calibration(C, W, L, R):
    led, deeds, cad = L["led"], L["deeds"], L["cad"]
    tk = A.ledger_takeovers(led, 120)
    deed_by_ref = {}
    for d in deeds:
        deed_by_ref.setdefault(d["referencia_cadastral"], []).append(d)
    notified = {}
    for r in led:
        m = A.TK_RE.search(r["concepte"])
        if r["programa"] == "PPO" and r["fase"] == "D" and m:
            notified[m.group(1)] = D(int(m.group(4)), int(m.group(3)), int(m.group(2)))
    settled = []
    for ref, (c, _) in sorted(tk.items()):
        later = [d for d in deed_by_ref.get(ref, []) if d["data_atorgament"] > c]
        if later:
            settled.append((ref, dt.date.fromisoformat(c), dt.date.fromisoformat(later[0]["data_atorgament"]),
                            later[0]["nif_adquirent"]))
    C.ok(len(settled) == 23, f"23 settled first-offer purchases recovered by joining the ledger to the deeds ({len(settled)})")
    agency = {s[3] for s in settled}
    C.ok(len(agency) == 1 and not agency & L["lh"], "every settled purchase was bought by one buyer that is not on the register")
    C.ok(all((dd - c).days == 120 for _, c, dd, _ in settled), "the deed falls 120 calendar days after the commitment in 23 of 23")
    misses = {"notified": [abs((notified[r] - dd).days) for r, c, dd, _ in settled],
              "commitment": [(dd - c).days for r, c, dd, _ in settled],
              "4 months": [abs((add_months(c, 4) - dd).days) for r, c, dd, _ in settled],
              "120 working days": [abs((add_workdays(c, 120) - dd).days) for r, c, dd, _ in settled]}
    C.ok(min(misses["notified"]) >= 9, f"the notified date misses 23 of 23 by 9 days or more (min {min(misses['notified'])})")
    C.ok(all(x == 120 for x in misses["commitment"]), "the commitment date misses 23 of 23 by 120 days")
    n4 = sum(1 for x in misses["4 months"] if x >= 1)
    C.ok(n4 >= 18, f"four calendar months misses {n4} of 23 by at least a day")
    C.ok(min(misses["120 working days"]) > 40, "120 working days misses 23 of 23 by more than 40 days")
    sellers = {deed_by_ref[r][-1]["nif_transmitent"] for r, *_ in settled}
    C.ok(not sellers & L["lh"], "no settled purchase's seller is on the register")
    # large-holder commitments: dates and the gap the corridor needs
    lh_refs = {ref for ref in tk if ref in R["sch"]}
    cds = sorted(dt.date.fromisoformat(tk[r][0]) for r in lh_refs)
    C.ok(cds and cds[0] > D(2026, 6, 30), "every commitment on a large holder's scheduled sale is after 30 June 2026")
    C.ok(not [d for d in cds if D(2026, 8, 22) <= d <= D(2026, 9, 13)], "no large-holder commitment from 22 August to 13 September")
    C.ok(all(d.weekday() < 4 for d in cds), "every large-holder commitment falls Monday to Thursday")
    comps = [dt.date.fromisoformat(tk[r][1]) for r in lh_refs]
    C.ok(all(workday(d) for d in comps), "no completion on a weekend or a Valencian holiday")
    C.ok(not [d for d in comps if D(2026, 12, 28) <= d <= D(2027, 1, 4)], "no completion from 28 December to 4 January")
    C.ok(not [r for r in lh_refs if R["sch"][r][0] <= "2026-09-30"], "no taken-over agreement has an agreed date on or before 30 September")
    # back-test: every scheduled sale in any return with an agreed date to 30 September completed as agreed
    seen = {}
    for r in L["ret"]:
        if not r["data_transmissio_prevista"] or r["data_transmissio_prevista"] > "2026-09-30":
            continue
        if r["unitats"]:
            parcel = re.sub(r"\s", "", r["referencia_cadastral"]).upper()
            refs = [cad.by_unit[(parcel, u)] for u in A.expand_units(r["unitats"])]
        else:
            refs = [cad.repair(r["referencia_cadastral"])]
        for ref in refs:
            seen[(ref, r["data_transmissio_prevista"])] = r["nif_adquirent_previst"]
    hits = sum(1 for (ref, d), b in seen.items()
               if any(x["data_atorgament"] == d and x["nif_adquirent"] == b for x in deed_by_ref.get(ref, [])))
    C.ok(hits == len(seen) and len(seen) >= 400, f"back-test: {hits} of {len(seen)} scheduled sales completed on the agreed date to the agreed buyer")
    C.ok(not [r for r in L["led"] if r["programa"] == "PPO" and r["data_comptable"] < "2026-01-01"]
         and not [d for d in deeds if d["nif_adquirent"] in agency and d["data_atorgament"] < "2026-01-01"],
         "no first-offer commitment or agency purchase before 2026")
    return {"settled": len(settled), "backtest": len(seen), "misses": {k: (min(v), max(v)) for k, v in misses.items()},
            "n4": n4}


def closeout(C, W, L, R, Dd):
    cad = L["cad"]
    annex = {row[0]: row for row in Dd["annex26"]}
    C.ok(all(R["c25"][s] == annex[s][2] for s in WATCH), "R3 on the 2025 data reproduces the 2026 annex on 14 of 14")
    snap = A.counts(A.picture(L["ret"], "2025T2", "2025-08-31", cad, "R2"), WATCH)
    miss_snap = sum(1 for s in WATCH if snap[s] != annex[s][2])
    deeds_only = A.section_counts(A.roll(R["own25"], {}, L["deeds"], L["lh"], "2025-06-30", "2025-09-30", "2025-09-30",
                                         "2026-01-01"), cad, WATCH)
    miss_deeds = sum(1 for s in WATCH if deeds_only[s] != annex[s][2])
    C.ok(miss_snap >= 9, f"the 30 June 2025 snapshot misses the 2026 annex on {miss_snap} sections")
    C.ok(miss_deeds >= 4, f"the deeds-only roll misses the 2026 annex on {miss_deeds} sections")
    r5_25 = A.roll(R["own25"], R["sch25"], L["deeds"], L["lh"], "2025-06-30", "2025-09-30", "2025-09-30", "2026-01-01",
                   R["tk"], "R5")
    C.ok(A.section_counts(r5_25, cad, WATCH) == R["c25"], "R5 on the 2025 data equals R3 case for case (no takeover before 2026)")
    # actual holdings on 1 January 2026 (deeds to 31 December) agree with the annex too
    act = A.section_counts(A.roll(R["own25"], {}, L["deeds"], L["lh"], "2025-06-30", "2025-12-31", "2026-09-30",
                                  "2026-01-01"), cad, WATCH)
    C.ok(act == R["c25"], "the 2026 annex matches the holdings the deeds show on 1 January 2026")
    big26 = Dd["big26"]
    olds = {"Grup Ampit", "Grup Golfa"}
    C.ok(not [s for s in WATCH if big26[s][0] in olds], "no group whose code was later reissued leads any section in 2026")
    stored25 = A.stored_codes(L["ret"], "2025T2", "2025-08-31")
    naive = A.largest(R["roll25"], cad, WATCH, {h: c for h, (c, d) in stored25.items()}, L["codes"], L["names"])
    C.ok(all(naive[s][:2] == big26[s][:2] for s in WATCH), "the stored-code reading reproduces the 2026 annex's group columns (no referee leak)")
    return {"snap_miss": miss_snap, "deeds_miss": miss_deeds}


def structure(C, W, L, R):
    cad, ret = L["cad"], L["ret"]
    # twins: two of Q's taken-over December sales and two of T's not taken over
    t2 = [r for r in ret if r["trimestre"] == "2026T2" and r["data_transmissio_prevista"] == "2026-12-10"]
    secs = {cad.sec[cad.repair(r["referencia_cadastral"])] for r in t2}
    C.ok(len(t2) == 4 and secs == {CODE["Q"], CODE["T"]}, "four twin rows, two in Q and two in T")
    cols = [c for c in t2[0] if c not in ("referencia_cadastral", "nif_adquirent_previst")]
    C.ok(all(all(r[c] == t2[0][c] for c in cols) for r in t2),
         "the twin rows agree on every return column except the reference and the buyer's NIF")
    tk = R["tk"]
    qtw = [cad.repair(r["referencia_cadastral"]) for r in t2 if cad.sec[cad.repair(r["referencia_cadastral"])] == CODE["Q"]]
    ttw = [cad.repair(r["referencia_cadastral"]) for r in t2 if cad.sec[cad.repair(r["referencia_cadastral"])] == CODE["T"]]
    C.ok(all(x in tk for x in qtw) and not any(x in tk for x in ttw), "only the ledger separates the twins")
    C.ok(all(x in R["rolls"]["R5"] for x in qtw) and not any(x in R["rolls"]["R5"] for x in ttw),
         "on 1 January Q's twins are still with the seller and T's have left the large-holder count")
    # threshold convergence: every registered holder at ten or more on both dates under every rung
    full_own, _ = A.holdings(A.picture(ret, "2026T2", "2026-08-31", cad, "R2"))
    tot = {}
    for ref, h in full_own.items():
        tot[h] = tot.get(h, 0) + 1
    C.ok(min(tot.values()) >= 10, f"every holder holds ten or more dwellings on 30 June 2026 (min {min(tot.values())})")
    for m, o in R["rolls"].items():
        t = {}
        for ref, h in o.items():
            t[h] = t.get(h, 0) + 1
        assert min(t.values()) >= 10, m
    C.ok(True, "every holder holds ten or more dwellings on 1 January 2027 under R3, R4, R4' and R5")
    nonlh = {}
    for d in sorted(L["deeds"], key=lambda d: d["data_atorgament"]):
        for nif, sgn in ((d["nif_adquirent"], 1), (d["nif_transmitent"], -1)):
            if nif not in L["lh"]:
                nonlh[nif] = nonlh.get(nif, 0) + sgn
    C.ok(max(v for k, v in nonlh.items() if not k.startswith("Q")) <= 3,
         "no owner off the register acquires more than three dwellings in the deed extract")
    # dates: nothing executed, scheduled or completed from 28 December to 4 January
    bad = [d for d in L["deeds"] if d["data_atorgament"][5:] >= "12-28" or d["data_atorgament"][5:] <= "01-04"]
    bad += [r for r in ret if r["data_transmissio_prevista"] and (r["data_transmissio_prevista"][5:] >= "12-28"
                                                                  or r["data_transmissio_prevista"][5:] <= "01-04")]
    C.ok(not bad, "no deed or agreed date from 28 December to 4 January")
    C.ok(all(d["data_inscripcio"] <= "2026-09-30" for d in L["deeds"]) and
         not [d for d in L["deeds"] if "09-21" <= d["data_atorgament"][5:] <= "09-30"],
         "every deed in the extract is registered by 30 September and none is executed in the last ten days of September")
    plan_n = {s["code"]: s["N"] for s in SECTIONS}
    C.ok(all(cad.N[s] == plan_n[s] for s in WATCH), "cadastre dwellings per section as built (no unit added or removed)")
    allunits = {s: sum(1 for r, x in cad.sec.items() if x == s) for s in WATCH}
    C.ok(sum(1 for s in WATCH if allunits[s] > cad.N[s]) >= 12, "counting every cadastral unit, not dwellings, overstates the denominator")
    # row shape follows the lodgement date
    shape_ok = all((bool(r["unitats"]) == (r["data_presentacio"] < "2026-04-01")) for r in ret)
    C.ok(shape_ok, "every return row's shape (parcel and units, or dwelling) follows its lodgement date")
    late = {r["id_declaracio"] for r in ret if r["trimestre"] < "2026T1" and r["data_presentacio"] >= "2026-04-01"}
    C.ok(len(late) >= 2, "returns for earlier quarters lodged after 1 April carry dwelling rows")
    # malformed references each resolve to exactly one cadastre dwelling
    malformed = [r["referencia_cadastral"] for r in ret if not r["unitats"] and r["referencia_cadastral"] not in cad.sec]
    C.ok(malformed and all(cad.repair(x) for x in malformed), f"{len(malformed)} malformed references, each with one candidate")
    mal_w = {s: 0 for s in WATCH}
    own_eff = R["own"]
    for r in ret:
        if r["trimestre"] == "2026T2" and not r["unitats"] and r["referencia_cadastral"] not in cad.sec:
            ref = cad.repair(r["referencia_cadastral"])
            if cad.sec[ref] in mal_w and own_eff.get(ref) == r["nif_declarant"]:
                mal_w[cad.sec[ref]] += 1
    C.ok(all(mal_w[s["code"]] == s["mal"] for s in SECTIONS), "malformed references on the 30 June picture as planned")
    # step order and row order
    base = A.counts(A.picture(ret, "2026T2", "2026-08-31", cad, "R2"), WATCH)
    lod = {}
    for r in ret:
        if r["data_presentacio"] <= "2026-08-31":
            lod.setdefault((r["nif_declarant"], r["trimestre"]), {}).setdefault(r["id_declaracio"], []).append(r)
    rows0 = [dict(r) for r in ret if r["data_presentacio"] <= "2026-08-31" and r["trimestre"] <= "2026T2"]

    def st_V(rows):
        keep = set()
        for h in {h for h, _ in lod}:
            qs = sorted(q for (hh, q) in lod if hh == h and q <= "2026T2")
            vs = lod[(h, qs[-1])]
            ids = []
            for vid in sorted(vs, key=lambda i: (vs[i][0]["data_presentacio"], i)):
                ids = [vid] if vs[vid][0]["tipus_declaracio"] in ("O", "S") else ids + [vid]
            keep.update(ids)
        return [r for r in rows if r["id_declaracio"] in keep]

    def st_B(rows):
        out = []
        for r in rows:
            if r["unitats"]:
                parcel = re.sub(r"\s", "", r["referencia_cadastral"]).upper()
                for u in A.expand_units(r["unitats"]):
                    out.append(dict(r, referencia_cadastral=cad.by_unit[(parcel, u)], unitats=""))
            else:
                out.append(r)
        return out

    def st_X(rows):
        return [r for r in rows if r["codi_tinenca"] == "PD"]

    def st_K(rows):
        return [dict(r, referencia_cadastral=cad.repair(r["referencia_cadastral"]) or r["referencia_cadastral"])
                if not r["unitats"] else dict(r, referencia_cadastral=re.sub(r"\s", "", r["referencia_cadastral"]).upper())
                for r in rows]
    steps = {"V": st_V, "B": st_B, "X": st_X, "K": st_K}
    for perm in itertools.permutations("VBXK"):
        rows = rows0
        for k in perm:
            rows = steps[k](rows)
        c = {s_: 0 for s_ in WATCH}
        for r in rows:
            x = cad.sec.get(r["referencia_cadastral"])
            if x in c:
                c[x] += 1
        assert c == base, perm
    C.ok(True, "the four conformance steps commute: every order gives the bulletin's picture")
    for k in range(3):
        sh = list(ret)
        random.Random(1000 + k).shuffle(sh)
        o, s2 = A.holdings(A.picture(sh, "2026T2", "2026-08-31", cad, "R2"))
        r5 = A.roll(o, s2, L["deeds"], L["lh"], "2026-06-30", "2026-09-30", "2026-09-30", "2027-01-01", R["tk"], "R5")
        assert A.section_counts(r5, cad, WATCH) == R["C"]["R5"]
    C.ok(True, "three row shuffles of the returns give the answer's counts")
    # clean-data test: the 30 June picture consolidated into one complete original return per holder
    fill = []
    for (h, ref, sec, s, code) in A.picture(ret, "2026T2", "2026-08-31", cad, "R2"):
        fill.append({"id_declaracio": "FILL-" + h, "nif_declarant": h, "trimestre": "2026T2", "tipus_declaracio": "O",
                     "data_presentacio": "2026-07-30", "referencia_cadastral": ref, "unitats": "", "codi_tinenca": "PD",
                     "data_transmissio_prevista": s[0] if s else "", "nif_adquirent_previst": s[1] if s else "",
                     "preu_convingut": s[2] if s else ""})
    o, s2 = A.holdings(A.picture(fill, "2026T2", "2026-08-31", cad, "R2"))
    f3 = A.section_counts(A.roll(o, s2, L["deeds"], L["lh"], "2026-06-30", "2026-09-30", "2026-09-30", "2027-01-01"), cad, WATCH)
    f5 = A.section_counts(A.roll(o, s2, L["deeds"], L["lh"], "2026-06-30", "2026-09-30", "2026-09-30", "2027-01-01",
                                 R["tk"], "R5"), cad, WATCH)
    C.ok(f3 == R["C"]["R3"] and f5 == R["C"]["R5"] and A.designated(f5, cad, WATCH) != A.designated(f3, cad, WATCH),
         "clean-data test: the filled returns give the same R3 and answer, and they differ")
    C.ok(all(r["data_atorgament"] <= "2026-09-30" for r in L["deeds"]) and
         all(r["data_comptable"] <= "2026-09-30" for r in L["led"]), "deeds and ledger complete to their own cut and no further")


def asks(C, W, L, R):
    cad = L["cad"]
    gold = R["rolls"]["R5"]
    stored = A.stored_codes(L["ret"], "2026T2", "2026-08-31")
    B = {m: A.largest(gold, cad, WATCH, A.ask_b_members(L["links"], stored, L["codes"], m), L["codes"], L["names"])
         for m in ("golden", "stored", "stored_valid", "reissued_stored", "links_else_stored", "latest_links")}
    B["no_roll"] = A.largest(R["own"], cad, WATCH, A.ask_b_members(L["links"], stored, L["codes"], "golden"),
                             L["codes"], L["names"])
    for m in ("R3", "R4", "R4p"):
        B[m] = A.largest(R["rolls"][m], cad, WATCH, A.ask_b_members(L["links"], stored, L["codes"], "golden"),
                         L["codes"], L["names"])
    g = B["golden"]
    C.ok(all(g[s][1] - g[s][2] >= 3 for s in WATCH), "the largest group leads the next by 3 or more in every section")
    mv = {m: [s for s in WATCH if B[m][s][:2] != g[s][:2]] for m in B}
    C.ok(len(mv["stored_valid"]) >= 8, f"ask B primary alone (stored codes, reissue handled) moves {len(mv['stored_valid'])}")
    C.ok(len(mv["reissued_stored"]) >= 5, f"ask B hazard alone (reissued codes) moves {len(mv['reissued_stored'])}")
    C.ok(len(mv["stored"]) >= 11, f"ask B natural stop (stored codes) moves {len(mv['stored'])}")
    C.ok(len(mv["latest_links"]) >= 1 and len(mv["links_else_stored"]) >= 5 and len(mv["no_roll"]) >= 8,
         f"ask B over-cleaned, half-handled and no-roll stops move {len(mv['latest_links'])}, "
         f"{len(mv['links_else_stored'])}, {len(mv['no_roll'])}")
    for m in ("stored", "stored_valid", "reissued_stored", "links_else_stored", "latest_links", "no_roll"):
        assert all(B[m][s][0] != g[s][0] or abs(B[m][s][1] - g[s][1]) >= 3 for s in mv[m]), m
    C.ok(True, "every ask B stop that moves a figure moves it by a name or by 3 dwellings or more")
    C.ok(all(B[m] == g for m in ("R3", "R4", "R4p")), "ask B is identical under R3, R4, R4' and R5")
    # ask C
    occ = {m: A.occupied(L["jun"], L["sep"], m) for m in
           ("golden", "sept_only", "sept_only_right", "lapsed_counted", "noneu_empty", "castello_rows")}
    V = {m: A.vacancy(gold, cad, WATCH, occ[m]) for m in occ}
    V["no_roll"] = A.vacancy(R["own"], cad, WATCH, occ["golden"])
    for m in ("R3", "R4", "R4p"):
        V[m] = A.vacancy(R["rolls"][m], cad, WATCH, occ["golden"])
    gv = V["golden"]
    plan = {s["code"]: sum(s["vac"]) for s in SECTIONS}
    C.ok(gv == plan, "ask C golden as built")
    prim = [s for s in WATCH if V["sept_only_right"][s] - gv[s] >= 6]
    C.ok(len(prim) >= 4, f"ask C primary (absent districts read as empty) moves {names(prim)} by 6 or more")
    hz2 = [s for s in WATCH if gv[s] - V["lapsed_counted"][s] >= 2]
    C.ok(len(hz2) >= 9, f"ask C lapsed registrations move {len(hz2)} sections by 2 or more")
    hz3 = [s for s in WATCH if gv[s] - V["castello_rows"][s] >= 5]
    C.ok(sorted(ROLE[s] for s in hz3) == ["O4", "O5"], "ask C per-dwelling rows counted as people move O4 and O5")
    C.ok(all(V["noneu_empty"][s] > gv[s] for s in WATCH if s[:5] != "12040"), "ask C over-cleaned stop overstates every section it can see")
    C.ok(all(V[m] != gv for m in ("sept_only", "lapsed_counted", "noneu_empty", "castello_rows", "no_roll")),
         "every ask C stop differs from the golden")
    C.ok(all(V["sept_only"][s] != gv[s] for s in WATCH), "the natural ask C stop misses all fourteen sections")
    C.ok(all(V[m] == gv for m in ("R3", "R4", "R4p")), "ask C is identical under R3, R4, R4' and R5")
    # lapse dates clear of the window from the June delivery to 1 January 2027
    for rows in (L["jun"], L["sep"]):
        for r in rows:
            if r["tipus_document"] in ("TIE-T", "PAS"):
                ref = r["data_ultima_renovacio"] or r["data_alta"]
                dl = f"{int(ref[:4]) + 2}{ref[4:]}"
                assert not ("2026-06-01" <= dl <= "2027-01-31"), r
    C.ok(True, "no renewal deadline falls between the June delivery and 31 January 2027")
    touched = set(R["tk"])
    C.ok(all(x in occ["golden"] for x in touched if cad.sec.get(x) in WATCH), "every dwelling the agency committed to is occupied")
    return B, V, mv


def separation(C, W, L, R, F):
    main_files = {F[k] for k in ("returns", "cadastre", "deeds", "ledger", "register", "bull2", "annex26", "order",
                                 "guide", "notice")}
    device_files = {F["padro06"], F["padro09"], F["codes"], F["xnote"]}
    C.ok(not main_files & device_files, "no device file is among the main call's files")
    dev_links = [r for r in L["links"] if r["data_anotacio"] >= "2026-02-27"]
    C.ok(len(dev_links) >= 9, f"{len(dev_links)} device rows in the register's link sheet, none in its holder sheet")
    # the main call reads the holder sheet only; deleting every device file leaves R3 and the answer unchanged
    L2 = {k: v for k, v in L.items() if k not in ("links", "codes", "codes_rows", "jun", "sep")}
    import build
    R2_ = build.compute(L2)
    C.ok(R2_["C"]["R3"] == R["C"]["R3"] and R2_["C"]["R5"] == R["C"]["R5"],
         "deleting every device (link sheet, code table, padró) moves neither R3 nor the answer")
    # hygiene battery on the ask paths: keys unique, joins land, no fan-out
    C.ok(len({r["codi_grup"] for r in L["codes_rows"]}) == len(L["codes_rows"]), "code table: one row per code (no fan-out)")
    stored_codes = {r["codi_grup"] for r in L["ret"] if r["codi_grup"]}
    C.ok(stored_codes <= {r["codi_grup"] for r in L["codes_rows"]}, "every stored group code joins the code table (no orphan)")
    C.ok(len({(r["nif"], r["data_efecte_inici"]) for r in L["links"]}) == len(L["links"]), "link sheet keys unique")
    ids = [r["id_inscripcio"] for rows in (L["jun"], L["sep"]) for r in rows if r["id_inscripcio"]]
    C.ok(all(r["referencia_cadastral"] in L["cad"].sec for rows in (L["jun"], L["sep"]) for r in rows),
         "every padró row joins the cadastre")
    C.ok(len(set(ids)) == len(ids), "padró inscription ids unique")


LEAK_TERMS = ["primera oferta", "first offer", "first-offer", "120 dies", "120 days", "desplaça", "distractor",
              "displace"]


def sweeps(C, T, F, meta, info):
    import writers as WR
    texts = {f: WR.file_text(os.path.join(T, f)) for f in sorted(os.listdir(T))}
    for f, t in texts.items():
        low = t.lower()
        for term in LEAK_TERMS:
            assert term not in low, (f, term)
    C.ok(True, "leak sweep: no shipped file names the first-offer mechanics, a day count or a distractor")
    C.ok(all(("tempteig" not in t.lower() and "PPO" not in t) for f, t in texts.items() if f != F["ledger"]),
         "tempteig and the programme code PPO appear only in the agency's ledger")
    led = [l for l in texts[F["ledger"]].splitlines()[1:]]
    C.ok(all(l.split(",")[5] == "PPO" for l in led if "tempteig" in l.lower()), "tempteig only in first-offer concept lines")
    C.ok(sum("25 per cent" in t for t in texts.values()) == 1, "the 25 per cent line is stated in exactly one file")
    C.ok(sum("1 de gener d'eixe any" in t for t in texts.values()) == 1, "the 1 January basis is stated in exactly one file")
    files = sorted(os.listdir(T))
    fmts = {os.path.splitext(f)[1] for f in files}
    C.ok(len(files) >= 10, f"input gate: {len(files)} files")
    C.ok(len(fmts) >= 3, f"input gate: {len(fmts)} formats {sorted(fmts)}")
    C.ok(info["returns_rows"] >= 25000, f"input gate: the returns file has {info['returns_rows']} rows")
    C.ok(len(meta["distractor_files"]) >= 2 and all(d in files for d in meta["distractor_files"]),
         "input gate: two or more distractors named in metadata.json and present")
    C.ok(not any("distractor" in f.lower() for f in files), "no file name says distractor")
    C.ok(len(meta["deliverables"]) == 3, "three deliverables")
    import importlib.util
    spec = importlib.util.spec_from_file_location("scrub", WR.SCRUB)
    sc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sc)
    for f in files:
        r = sc.audit(os.path.join(T, f), "2024-01-01", "2026-10-10")
        assert r is None or (not r[0] and not r[1]), (f, r)
    C.ok(True, "no writer signature and no out-of-band timestamp in any shipped container")


def bridge(C, L, R, s):
    out = []
    prev = R["C"]["R2"][s]
    start = prev
    for m in range(7, 13):
        end = D(2026, m + 1, 1) - dt.timedelta(days=1) if m < 12 else D(2026, 12, 31)
        ed = min(end, D(2026, 9, 30)).isoformat()
        o = A.roll(R["own"], R["sch"], L["deeds"], L["lh"], "2026-06-30", ed, "2026-09-30", end.isoformat(), R["tk"], "R5")
        c = A.section_counts(o, L["cad"], WATCH)[s]
        out.append(c - prev)
        prev = c
    C.ok(start + sum(out) == R["C"]["R5"][s], f"bridge {ROLE[s]}: bulletin {start} + months {out} = annex {R['C']['R5'][s]}")
    return start, out


def run(W, T, L, R, Dd, F, meta, info, touched):
    C = Checks()
    sets, sh5, near_d, near_u = main_ladder(C, W, L, R)
    R_SETS.update(sets)
    C.ok(all(Dd["bull2"][i][2] == R["C"]["R2"][s] for i, s in enumerate(WATCH)), "the 30 June bulletin is R2, 14 of 14")
    cells, mapping, partials = grid(C, W, L, R)
    cal = calibration(C, W, L, R)
    clo = closeout(C, W, L, R, Dd)
    structure(C, W, L, R)
    B, V, mv = asks(C, W, L, R)
    separation(C, W, L, R, F)
    sweeps(C, T, F, meta, info)
    br = {ROLE[s]: bridge(C, L, R, s) for s in (near_u, near_d)}
    C.ok(set(br) == {"P", "Q"}, "the bridge sections are P and Q")
    golden = {}
    for s in WATCH:
        golden[s] = {"role": ROLE[s], "N": L["cad"].N[s], "lh": R["C"]["R5"][s], "share": str(r1(sh5[s])),
                     "share_raw": str(sh5[s]), "group": B["golden"][s][0], "group_n": B["golden"][s][1],
                     "empty": V["golden"][s], "designated": s in ANSWER}
    rec = {"n_assert": C.n, "checks": C.log, "golden": golden, "answer": ANSWER,
           "rungs": {m: {s: R["C"][m][s] for s in WATCH} for m in R["C"]},
           "sets": {m: names(v) for m, v in sets.items()},
           "nearest": {"designated": [ROLE[near_d], str(r1(sh5[near_d])), str(r1(abs(sh5[near_d] - 25)))],
                       "undesignated": [ROLE[near_u], str(r1(sh5[near_u])), str(r1(abs(sh5[near_u] - 25)))]},
           "bridge": br, "grid": {k: v for k, v in mapping.items()}, "calibration": cal, "closeout": clo,
           "askB_moved": {m: names(v) for m, v in mv.items()},
           "askB_stops": {m: {ROLE[s]: list(B[m][s][:2]) for s in WATCH} for m in B},
           "askC_stops": {m: {ROLE[s]: V[m][s] for s in WATCH} for m in V},
           "annex26": {s: [str(x) for x in row[1:]] for s, *_ in [(r[0],) for r in Dd["annex26"]]
                       for row in Dd["annex26"] if row[0] == s},
           "info": info}
    assert C.n >= 40, C.n
    return rec
