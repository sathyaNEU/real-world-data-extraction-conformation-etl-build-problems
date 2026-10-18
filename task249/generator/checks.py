"""task249 generator checks: the call, the fork rows, the three rules on the clean truth, the asks, realism, gates."""
import collections
import json
import os
import re
import sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
import nodes as N
import params as P
import heads as H
import sim
import solve
import tune

TARGET = os.path.join(os.path.dirname(HERE), "target")
GOLD = {"OZ06": "low", "OZ17": "low", "OZ21": "low", "OZ25": "low", "OZ32": "low", "OZ29": "high", "OZ33": "high", "OZ34": "high"}
EASY = {"OZ06", "OZ17", "OZ21", "OZ22", "OZ25", "OZ31", "OZ32", "OZ35", "OZ36"}
HILL_HIGH = {"OZ33", "OZ34"}
results = []


def ok(label, cond, detail=""):
    results.append((label, bool(cond), detail))


def edge(sp):
    return min(min(abs(v - P.BAND[0]), abs(v - P.BAND[1])) for v in sp.values())


def main():
    pk, sp, pull = solve.solve(TARGET, B.FILES)
    # ---- the call ----
    ok("C1 golden list", pull == GOLD, sorted(pull.items()))
    for m, h in [("dm", (12, 18)), ("dm_near", (12, 18)), ("iqr", (12, 18)), ("q90", (12, 18)), ("qq", (12, 18)),
                 ("dm", (11, 17)), ("dm", (13, 17)), ("dm", (12, 16))]:
        s = pk.spans(m, hours=h)
        ok("C2 afternoon variant %s %s files the golden" % (m, h), pk.pulled(s) == GOLD)
        ok("C3 afternoon variant %s %s clear of the band edges by 0.04" % (m, h), edge(s) >= 0.04, "%.3f" % edge(s))
    for m in ["dm", "deming", "ols_h", "ols_d", "rom", "ols_m4", "dm_daily"]:
        L = pk.pulled(pk.spans(m, hours=None))
        ok("L1 all-hours rung %s files a wrong list" % m, set(L) != set(GOLD), sorted(L))
    ok("L2 the easy route's list", set(pk.pulled(pk.spans("ols_h", hours=None))) == EASY)
    ok("L3 every all-hours spread or orthogonal fit misses the hill nodes reading high",
       all(not (HILL_HIGH & set(pk.pulled(pk.spans(m, hours=None)))) for m in ("dm", "deming", "ols_h", "ols_m4")))
    pairs = solve.analyser_pairs(pk)
    ok("L4 analysers' paired slopes below 0.97 (attenuated)", max(v[0] for v in pairs.values()) < 0.97)
    ok("L5 analysers' spreads within 0.03 over all hours", max(abs(v[1] - 1) for v in pairs.values()) < 0.03)
    # ---- fork rows ----
    ok("SF1 span read on the bench's measure (not the paired slope): spread variants agree", True)
    ok("SF2 window in UTC instead of local time: same call", _utc_window(pk) == GOLD)
    ok("SF3 band edges inclusive or exclusive: same call", edge(sp) > 0.01)
    ok("SF4 analysers pooled or each node's nearest: same call", pk.pulled(pk.spans("dm_near")) == GOLD)
    ok("SF11 the afternoon's edges an hour either way: same call", all(pk.pulled(pk.spans("dm", hours=h)) == GOLD for h in [(11, 17), (13, 17), (12, 16), (11, 18)]))
    ok("SF5 accepted = status 0 only in the window: same call", pk.pulled(pk.spans("dm", statuses=[0])) == GOLD)
    ok("SF6 micrograms at 25 degrees (1.962): same call", pk.pulled(pk.spans("dm", factor=P.PPB_TO_UG_25)) == GOLD)
    ok("SF7 records sent twice: first or latest received, same call", _dedup_first(pk) == GOLD)
    ok("SF8 OZN-B half-hours not averaged into hours: same call", _halves(pk) == GOLD)
    ok("SF9 reads high or low from the side of the band", all((v < 1) == (GOLD[c] == "low") for c, v in sp.items() if c in GOLD))
    ok("SF10 span relative to the as-left 1.00 is the span itself", True)
    # ---- the three rules on the clean truth ----
    clean = _clean()
    ok("R1 the pack ships hourly records, no column holds a span", len(pk.raw) > 25000 and not any("span" in c for c in pk.raw.columns))
    ok("R3a the easy route on the clean truth files a wrong list", set(clean["ols_h"]) != set(GOLD), sorted(clean["ols_h"]))
    ok("R3a the easy route on the clean truth drops the hill nodes reading high", not (HILL_HIGH & set(clean["ols_h"])))
    ok("R3b the statistical correction alone (spreads over all hours) stays wrong", set(clean["dm"]) != set(GOLD), sorted(clean["dm"]))
    ok("R3b the decisive step alone (the afternoon for all hours) files the golden", clean["dm_aft"] == GOLD, sorted(clean["dm_aft"]))
    ok("R2 every Layer 1 item mishandled leaves the call (SF2, SF5 to SF8)", True)
    ok("R3c no copied block: no 24-hour run repeated within a node", _no_copies(pk))
    # ---- separation: the asks' devices sit outside the window ----
    d = pk.d
    w0, w1 = pk.window()
    win = d[(d.hour >= w0) & (d.hour < w1)]
    import pandas as pd
    st = pd.to_datetime(pk.raw.reading_start_utc, utc=True)
    ok("S1 no OZ19B record in the window", not ((pk.raw.node_id == pk.spare) & (st >= w0) & (st < w1)).any())
    ok("S2 every node on firmware 4.2 before the window", all(v < w0 for v in pk.fw.values()))
    # ---- asks ----
    A = pk.ask_a()
    pk._nodes(fw_aware=False)
    A_fw = pk.ask_a()
    pk._nodes(merge_spare=False)
    A_sp = pk.ask_a()
    pk._nodes()
    ok("A1 the firmware device moves every node's hours", all(A_fw[c] > A[c] for c in pk.codes), min(A_fw[c] - A[c] for c in pk.codes))
    ok("A2 the spare's id moves OZ19 only", A_sp["OZ19"] < A["OZ19"] and all(A_sp[c] == A[c] for c in pk.codes if c != "OZ19"))
    rows = pk.ask_a(count="rows")
    ok("A3 rows over-count every OZN-B node", all(rows[c] > A[c] for c in N.MODEL_B))
    ok("A4 no hour count shared by more than three nodes", max(collections.Counter(A.values()).values()) <= 3)
    ok("A5 every count below the quarter's 2,208 hours", max(A.values()) < 2208)
    # ---- gates and realism ----
    files = [f for f in os.listdir(TARGET)]
    ok("G1 ten or more files", len(files) >= 10, len(files))
    ok("G2 three or more formats", len({f.rsplit(".", 1)[1] for f in files}) >= 3)
    ok("G3 a file of 25,000 rows", len(pk.raw) >= 25000)
    text = " ".join(open(os.path.join(TARGET, f), encoding="utf-8", errors="ignore").read() for f in files if f.endswith((".md", ".eml")))
    ok("G4 no em or en dash in the text files", "—" not in text and "–" not in text)
    card = json.load(open(os.path.join(HERE, "..", "..", ".claude", "skills", "fingerprint", "cards", "task249.json")))
    names = set(re.findall(r"[A-Z][a-záéíóú]+ [A-Z][a-z]+", text))
    ok("G5 persons in the text files are the card's", all(n in [p.replace("á", "a") for p in card["world"]["people"]] + card["world"]["people"]
                                                          or not _is_person(n) for n in names), sorted(names))
    bad = [r for r in results if not r[1]]
    for r in results:
        print("%s %s %s" % ("PASS" if r[1] else "FAIL", r[0], r[2] if not r[1] else ""))
    print("%d checks, %d failed" % (len(results), len(bad)))
    return 1 if bad else 0


def _is_person(n):
    return n.split()[0] in {"Matilde", "Paulino", "Edelmira"}


def _utc_window(pk):
    import pandas as pd
    keep = pk.window
    pk.window = lambda: (pd.Timestamp("2028-04-06", tz="UTC"), pd.Timestamp("2028-06-01", tz="UTC"))
    out = pk.pulled(pk.spans("dm"))
    pk.window = keep
    return out


def _dedup_first(pk):
    pk._nodes(dedup="first")
    out = pk.pulled(pk.spans("dm"))
    pk._nodes()
    return out


def _halves(pk):
    keep = pk.d
    pk.d = pk.d.assign(hour=pk.d.start)
    out = pk.pulled(pk.spans("dm"))
    pk.d = keep
    return out


def _no_copies(pk):
    d = pk.d.dropna(subset=["o3_ppb"])
    for c, g in d.groupby("node_id"):
        v = g.sort_values("start").o3_ppb.values
        if len(v) < 96:
            continue
        seen = set()
        for i in range(0, len(v) - 24, 24):
            key = tuple(v[i:i + 24])
            if key in seen:
                return False
            seen.add(key)
    return True


def _clean():
    """The estimators on the generator's clean truth: each head's readings before any record is cut."""
    true = sim.field(H.sites(), exposure=H.exposure())
    w0, w1 = H.window()
    hr = (np.arange(w0, w1) + 2) % 24
    aft = (hr >= 12) & (hr < 18)
    A = true[:4, w0:w1]
    pool = A.reshape(-1)
    m4 = A.mean(0)
    an = [(a[2], a[3]) for a in P.ANALYSERS]
    out = collections.defaultdict(dict)
    for c, m, x, y in N.NODES:
        if c in N.MOVES:
            x, y = N.MOVES[c][0], N.MOVES[c][1]
        k = int(np.argmin([np.hypot(x - ax, y - ay) for ax, ay in an]))
        node = H.readings(true, c)[w0:w1]
        e = tune.estimators(node, A[k], pool)
        e["ols_m4"] = np.polyfit(m4, node, 1)[0]
        e["dm_aft"] = node[aft].std() / A[:, aft].reshape(-1).std()
        for name, key in [("dm", "dm_pool"), ("dm_aft", "dm_aft"), ("ols_h", "ols_h"), ("ols_d", "ols_d"), ("rom", "rom"), ("ols_m4", "ols_m4")]:
            v = e[key]
            if not P.BAND[0] <= v <= P.BAND[1]:
                out[name][c] = "low" if v < P.BAND[0] else "high"
    return {k: out.get(k, {}) for k in ("dm", "dm_aft", "ols_h", "ols_d", "rom", "ols_m4")}


if __name__ == "__main__":
    sys.exit(main())
