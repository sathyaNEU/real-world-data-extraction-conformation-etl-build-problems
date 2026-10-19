"""The ask layer's pair arithmetic on the built target: each ask figure under the golden path and under the paths a
careful response takes (the cracker lands the call, the mirror does not; both run the hygiene battery and read
every filed sentence). A figure is hit within half a unit of its stated rounding.

    python3 pair.py [target]"""
import os
import sys
import numpy as np
import pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B

UNIT = {"over": 1, "confirmed": 1, "per_thousand": 0.1, "share": 0.01, "moved": 1}


def load(tgt):
    p = lambda k: os.path.join(tgt, B.FILES[k])
    att = pd.read_parquet(p("attempts"))
    ex = pd.read_parquet(p("exposure"))
    reg = pd.read_csv(p("register"))
    cases = pd.read_excel(p("cases"), sheet_name="Case log")
    sl = pd.read_csv(p("shortlists"))
    col = pd.read_csv(p("colleges"))
    return att, ex, reg, cases, sl, col


def exposure(att, ex, reg, registered=True, any_attempt=True, ist=True, per_candidate=True, ceiling=0.12):
    a = att[att["candidate_id"].isin(set(reg["candidate_id"]))] if registered else att
    if not any_attempt:
        a = a[a["attempt_status"] == "completed"]
    t = pd.to_datetime(a["started_utc"]) + (pd.Timedelta(hours=5, minutes=30) if ist else pd.Timedelta(0))
    a = a.assign(week=(t.dt.normalize() - pd.Timestamp("2028-07-03")).dt.days // 7)
    e = ex.merge(a[["booking_ref", "attempt_no", "candidate_id", "week"]], on=["booking_ref", "attempt_no"])
    out, rested = [], set()
    for k in range(4):
        aa, ee = a[a["week"] == k], e[e["week"] == k]
        den = aa["candidate_id"].nunique() if per_candidate else len(aa)
        num = ee.groupby("item_id")["candidate_id"].nunique() if per_candidate else ee.groupby("item_id").size()
        x = num / den
        rested |= set(x.index[x > ceiling])
        out.append(("A_w%d_over" % (k + 1), "over", int((x > ceiling).sum())))
    out.append(("A_rested", "over", len(rested)))
    return out


def impersonation(cases, sl, reg, col, latest="candidate", key="candidate_id", den_rows=False,
                  confirmed=("confirmed impersonation", "confirmed on appeal")):
    """latest: 'candidate' (a sitting's latest decision across its cases), 'case' (each case's latest row) or
    None (every row)"""
    tier = reg.set_index("candidate_id")["college_code"].map(col.set_index("college_code")["tier"])
    c = cases.copy()
    if latest == "candidate":
        c = c.sort_values(["candidate_id", "decided", "case_ref"], kind="stable").groupby("candidate_id").tail(1)
    elif latest == "case":
        c = c.sort_values(["case_ref", "decided"], kind="stable").groupby("case_ref").tail(1)
    conf = c[c["finding"].isin(confirmed)].copy()
    conf["tier"] = conf["candidate_id"].map(tier)
    if key == "booking_ref":
        conf = conf[conf["booking_ref"].notna() & (conf["booking_ref"].astype(str) != "")]
        n = conf.groupby("tier")["booking_ref"].nunique()
    elif key == "rows":
        n = conf.groupby("tier").size()
    else:
        n = conf.groupby("tier")["candidate_id"].nunique()
    s = sl.assign(tier=sl["candidate_id"].map(tier))
    den = s.groupby("tier").size() if den_rows else s.groupby("tier")["candidate_id"].nunique()
    out = []
    for t in ("T1", "T2", "T3", "T4"):
        out += [("B_%s_n" % t, "confirmed", int(n.get(t, 0))), ("B_%s_rate" % t, "per_thousand", round(1000 * n.get(t, 0) / den[t], 1))]
    return out


def interrupted(att, reg, registered=True, device_of="first", by="candidate"):
    a = att[att["candidate_id"].isin(set(reg["candidate_id"]))] if registered else att
    key = "candidate_id" if by == "candidate" else "booking_ref"
    a = a.sort_values([key, "started_utc"], kind="stable")
    first = a.groupby(key).head(1).set_index(key)
    last = a.groupby(key).tail(1).set_index(key)
    inter = a[a["attempt_status"] == "interrupted"].set_index(key)
    base = first if device_of == "first" else last
    out = []
    for d in ("desktop", "laptop", "tablet"):
        b = base[base["device"] == d]
        k = inter[base["device"].reindex(inter.index) == d]
        moved = int((last["device"].reindex(k.index) != first["device"].reindex(k.index)).sum())
        out += [("C_%s_share" % d, "share", round(100 * len(k) / len(b), 2)), ("C_%s_moved" % d, "moved", moved)]
    return out


def score(path, gold):
    g = {k: v for k, _, v in gold}
    hit = 0
    for k, u, v in path:
        if abs(v - g[k]) <= UNIT[u] / 2 + 1e-9:
            hit += 1
    return hit


def run(tgt, quiet=False):
    att, ex, reg, cases, sl, col = load(tgt)
    gold = exposure(att, ex, reg) + impersonation(cases, sl, reg, col) + interrupted(att, reg)
    paths = {
        # the call-landing response: hygiene battery (keys, duplicates, unmatched joins, fan-out, ties) and every filed
        # rule its path points at; nothing on the exposure path joins the register, a decision log is read at each
        # case's latest row, and s.6 puts a restart under its booking
        "cracker (battery and filed rules)":
            exposure(att, ex, reg, registered=False) + impersonation(cases, sl, reg, col, latest="case")
            + interrupted(att, reg, registered=False, by="booking"),
        # the miss on the call, as careful on the asks and also checking every identity against the register
        "mirror (register checked, latest row per case, sittings by booking)":
            exposure(att, ex, reg) + impersonation(cases, sl, reg, col, latest="case")
            + interrupted(att, reg, by="booking"),
        "careful on identities, completed attempts only":
            exposure(att, ex, reg, any_attempt=False) + impersonation(cases, sl, reg, col, latest="case")
            + interrupted(att, reg, by="booking"),
        "sittings by candidate, confirmed impersonation as the only confirming finding":
            exposure(att, ex, reg, registered=False) + impersonation(cases, sl, reg, col, confirmed=("confirmed impersonation",))
            + interrupted(att, reg, registered=False),
        "UTC weeks, per attempt, every confirmed row":
            exposure(att, ex, reg, registered=False, ist=False, per_candidate=False) + impersonation(cases, sl, reg, col, latest=None)
            + interrupted(att, reg, registered=False, by="booking"),
    }
    n = len(gold)
    if not quiet:
        print("ask figures", n)
        for k, v in paths.items():
            h = score(v, gold)
            print("  %-82s %2d of %d (%.0f per cent)" % (k, h, n, 100 * h / n))
    return gold, paths


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
