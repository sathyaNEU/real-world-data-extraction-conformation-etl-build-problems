"""task464 architecture 9: the independent verifier.

Reads every shipped format back (CSV and JSON lines with pandas, the workbooks with openpyxl, the PDFs' text with
pypdf) and recomputes the graded figures by its own code, without importing answers.py: each practice's
population, the pooled share of statin repeats not re-authorised, each practice's expected number and the
ranking, and the two return measures. Exit 1 on any disagreement with figures.json or the goldens.
"""
import json, os, sys, csv, datetime as dt
import pandas as pd
import openpyxl
from pypdf import PdfReader

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = os.path.join(BASE, "target")
G = os.path.join(BASE, "golden")
D0 = dt.date(2019, 1, 1)
FAIL = []


def day(s):
    return (dt.date.fromisoformat(s) - D0).days


def ukday(s):
    d, m, y = s.split("/")
    return (dt.date(int(y), int(m), int(d)) - D0).days


def ok(label, cond, detail=""):
    print("%s %-70s %s" % ("PASS" if cond else "FAIL", label, detail))
    if not cond:
        FAIL.append(label)


def per_day(text):
    s = text.lower()
    n = 1.0
    for w, v in (("half", 0.5), ("two", 2), ("2", 2), ("one", 1), ("1", 1)):
        if (" %s " % w) in (" %s " % s.replace(",", " ")):
            n = v
            break
    if "twice" in s or " bd" in (" " + s):
        n *= 2
    return n


def anniv(t):
    d = D0 + dt.timedelta(days=int(t))
    try:
        a = d.replace(year=d.year + 1)
    except ValueError:
        a = d.replace(year=d.year + 1, day=28)
    return (a - D0).days


def main():
    F = json.load(open(os.path.join(BASE, "generator", "figures.json")))
    look = pd.read_csv(os.path.join(T, "cvd_product_lookup.csv"))
    la = look.set_index("system_a_drug")[["vtm", "strength", "form", "bnf_class"]].to_dict("index")
    lb = look.set_index("system_b_product")[["vtm", "strength", "form", "bnf_class"]].to_dict("index")
    ia = pd.read_csv(os.path.join(T, "repeat_issues_system_a_2024-01_to_2026-11.csv"), dtype=str, keep_default_na=False)
    ib = pd.read_json(os.path.join(T, "repeat_issues_system_b_2024-01_to_2026-11.jsonl"), lines=True, dtype=False)
    iss = pd.DataFrame({
        "code": list(ia["Practice Code"]) + list(ib["org"]),
        "pid": list(ia["Patient Ref"]) + list(ib["patient_pseudo"]),
        "t": [ukday(x) for x in ia["Issue Date"]] + [day(x) for x in ib["issued"]],
        "vtm": [la[x]["vtm"] for x in ia["Drug"]] + [lb[x]["vtm"] for x in ib["product"]],
        "strength": [la[x]["strength"] for x in ia["Drug"]] + [lb[x]["strength"] for x in ib["product"]],
        "form": [la[x]["form"] for x in ia["Drug"]] + [lb[x]["form"] for x in ib["product"]],
        "cls": [la[x]["bnf_class"] for x in ia["Drug"]] + [lb[x]["bnf_class"] for x in ib["product"]],
        "qty": [int(x.split()[0]) for x in ia["Quantity"]] + [int(x) for x in ib["qty"]],
        "acute": [x == "Acute" for x in ia["Course"]] + [x == "acute" for x in ib["course"]],
        "ref": [x or None for x in ia["Repeat Ref"]] + [x if isinstance(x, str) else None for x in ib["authorisation"]],
        "eps": list(ia["EPS Prescription ID"]) + list(ib["eps_id"]),
    })
    canc = pd.read_csv(os.path.join(T, "eps_item_cancellations_2024-2026.csv"), dtype=str)
    cset = set(canc["prescription_id"])
    inv = {(r["vtm"], r["strength"], r["form"]): k for k, r in la.items()}
    citem = set(zip(canc["prescription_id"], canc["item"]))
    iss["cancelled"] = [(e in cset) and ((e, inv.get((v, s, f))) in citem)
                        for e, v, s, f in zip(iss["eps"], iss["vtm"], iss["strength"], iss["form"])]
    ta = pd.read_csv(os.path.join(T, "repeat_authorisations_system_a.csv"), dtype=str, keep_default_na=False)
    tb = pd.read_csv(os.path.join(T, "repeat_authorisations_system_b.csv"), dtype=str, keep_default_na=False)
    tpl = {}
    for _, r in ta.iterrows():
        q = int(r["Quantity"].split()[0])
        tpl[r["Repeat Ref"]] = dict(pid=r["Patient Ref"], code=r["Practice Code"], cls=la[r["Drug"]]["bnf_class"],
                                    M=int(r["Authorised Issues"]), start=ukday(r["Authorised Date"]),
                                    L=int(round(q / per_day(r["Dosage"]))), dose=r["Dosage"], qty=q)
    for _, r in tb.iterrows():
        q = int(r["qty_per_issue"])
        tpl[r["authorisation"]] = dict(pid=r["patient_pseudo"], code=r["org"], cls=lb[r["product"]]["bnf_class"],
                                       M=int(r["issues_authorised"]), start=day(r["start_date"]),
                                       L=int(round(q / per_day(r["directions"]))), dose=r["directions"], qty=q)
    reg = pd.read_csv(os.path.join(T, "patient_register_2026-12-01.csv"), dtype=str, keep_default_na=False)
    episodes = {}
    for _, r in reg.iterrows():
        episodes.setdefault(r["patient_ref"], []).append((r["practice_code"], day(r["registered"]),
                                                          day(r["deregistered"]) if r["deregistered"] else None))

    def registered(pid, code, t):
        return any(c == code and a <= t and (b is None or t < b) for c, a, b in episodes.get(pid, []))

    ASOF, POP0, W0 = day("2026-11-30"), day("2026-09-01"), day("2027-03-01")
    st = iss[(iss["cls"] == "Statin") & (~iss["cancelled"])].sort_values(["pid", "t", "ref"], na_position="first")
    by = {pid: g for pid, g in st.groupby("pid")}
    pop = {}
    for pid, g in by.items():
        for code in sorted(set(g["code"])):
            w = g[(g["code"] == code) & (g["t"] >= POP0) & (g["t"] <= ASOF)]
            if len(w) and registered(pid, code, ASOF):
                pop[pid] = code
    npop = pd.Series(pop).value_counts().to_dict()
    ok("V1 each practice's population", npop == F["population"], str(sorted(npop.items())))

    # the pooled share of statin repeats that ran out and were not re-authorised within 60 days
    made = st[st["ref"].notna()].groupby("ref")["t"].agg(["count", "max"])
    stpl = {}
    for ref, tp in tpl.items():
        if tp["cls"] == "Statin":
            stpl.setdefault(tp["pid"], []).append((tp["start"], ref))
    n = f = 0
    for pid, lst in stpl.items():
        lst.sort()
        for i, (s0, ref) in enumerate(lst):
            tp = tpl[ref]
            if s0 < day("2024-01-01") or ref not in made.index or made.loc[ref, "count"] < tp["M"]:
                continue
            last = made.loc[ref, "max"]
            if not (day("2024-01-01") <= last <= ASOF - 150):
                continue
            end = last + tp["L"]
            if not registered(pid, tp["code"], end + 60):
                continue
            n += 1
            nxt = [s for s, r2 in lst[i + 1:] if s >= last]
            if not (nxt and nxt[0] <= end + 60):
                f += 1
    rate = f / n
    ok("V2 the pooled share not re-authorised", abs(100 * rate - F["reauth_fail_pct"]) < 0.05,
       "%.2f%% of %d against %.1f%%" % (100 * rate, n, F["reauth_fail_pct"]))

    # each practice's expected number, run forward on the figures' rates
    e0, e1 = F["stop_rate_early_per_28d"], F["stop_rate_late_per_28d"]
    pace, stay = F["pace_mean"], F["stay"]
    exp = {}
    for pid, code in pop.items():
        g = by[pid]
        g = g[(g["code"] == code) & (g["t"] <= ASOF)]
        lastrow = g.iloc[-1]
        p = 0.0; alive = 1.0
        if lastrow["acute"]:
            t = lastrow["t"]
            while True:
                req = t + 28 + pace
                if t < W0: p += alive * e0
                alive *= 1 - e0
                if req >= W0: break
                t = req
        else:
            tp = tpl[lastrow["ref"]]
            left = tp["M"] - int((g["ref"] == lastrow["ref"]).sum())
            first = g.iloc[0]
            new = bool(first["acute"]) and first["t"] >= day("2024-01-01") + 30
            t = lastrow["t"]
            while True:
                req = t + tp["L"] + pace
                q = (e0 if (new and t - first["t"] < 182) else e1) * tp["L"] / 28
                if t < W0: p += alive * q
                alive *= 1 - q
                if left <= 0:
                    if req <= ASOF - 21:
                        p += alive
                    elif t < W0:
                        p += alive * rate
                    break
                if req >= W0: break
                t = req; left -= 1
        exp[code] = exp.get(code, 0.0) + min(p, 1.0) * stay
    rank = sorted(exp, key=lambda c: -exp[c])
    ok("V3 the ranking", rank == F["ranking"], " > ".join(rank))
    top = rank[0]
    ok("V4 the top practice's figure to the nearest 10", int(round(exp[top] / 10) * 10) == F["call_expected"],
       "%.1f" % exp[top])

    # R1 with each issue's dosage walked back through the change log
    chg = pd.read_csv(os.path.join(T, "repeat_changes_2024-01_to_2026-11.csv"), dtype=str, keep_default_na=False)
    chg = chg[chg["field"] == "Dosage"]
    hist = {}
    for _, r in chg.iterrows():
        hist.setdefault(r["repeat_ref"], []).append((day(r["changed_on"]), r["old_value"]))
    y0, y1 = day("2025-01-01"), day("2025-12-31")
    qs = [(day("2025-01-01"), day("2025-03-31")), (day("2025-04-01"), day("2025-06-30")),
          (day("2025-07-01"), day("2025-09-30")), (day("2025-10-01"), day("2025-12-31"))]
    raas = iss[iss["cls"].isin(["ACE inhibitor", "Angiotensin II receptor antagonist"]) & (~iss["cancelled"]) & (iss["t"] <= y1)]
    r1 = {}
    for (pid, code), g in raas.groupby(["pid", "code"]):
        if not any(c == code and a <= y0 and (b is None or b > y1) for c, a, b in episodes.get(pid, [])):
            continue
        if not all(((g["t"] >= lo) & (g["t"] <= hi)).any() for lo, hi in qs):
            continue
        cov = set(); run = {}
        for _, r in g.sort_values(["t", "eps"]).iterrows():
            dose = tpl[r["ref"]]["dose"] if r["ref"] in tpl else "ONE daily"
            for when, old in sorted(hist.get(r["ref"], []), reverse=True):
                if when > r["t"]:
                    dose = old
            days = int(round(r["qty"] / per_day(dose)))
            s0 = max(r["t"], run.get(r["vtm"], r["t"]))
            run[r["vtm"]] = s0 + days
            cov.update(range(max(s0, y0), min(s0 + days, y1 + 1)))
        a, k = r1.get(code, (0, 0))
        r1[code] = (a + 1, k + (len(cov) >= 0.8 * 365))
    for code, (a, k) in sorted(r1.items()):
        v = float(pd.Series([100 * k / a]).round(1).iloc[0])
        ok("V5 R1 percentage, %s" % code, abs(100 * k / a - F["ask_a"][code]["pct"]) < 0.05 + 1e-9,
           "%d of %d, %.2f against %.1f" % (k, a, 100 * k / a, F["ask_a"][code]["pct"]))

    # R2 from the discharge summaries' coded starts
    ev = pd.read_csv(os.path.join(T, "cvd_clinical_events_2023-2026.csv"), dtype=str, keep_default_na=False)
    ev["t"] = [day(x) for x in ev["event_date"]]
    mi = ev[ev["snomed_concept_id"] == "22298006"].groupby("patient_ref")["t"].apply(list).to_dict()
    tic = iss[(iss["vtm"] == "Ticagrelor") & (iss["strength"] == "90mg") & (~iss["cancelled"])].groupby("pid")["t"].apply(list).to_dict()
    r2 = {}
    for _, r in ev[ev["snomed_concept_id"] == "1290071000000109"].iterrows():
        t = r["t"]
        near = [m for m in mi.get(r["patient_ref"], []) if abs(t - m) <= 3]
        if not (day("2024-07-01") <= t <= day("2025-06-30")) or not near or not (day("2024-07-01") <= near[0] <= day("2025-06-30")):
            continue
        a, k = r2.get(r["practice_code"], (0, 0))
        r2[r["practice_code"]] = (a + 1, k + any(x > anniv(t) for x in tic.get(r["patient_ref"], [])))
    for code, (a, k) in sorted(r2.items()):
        ok("V6 R2 percentage, %s" % code, int((200 * k + a) // (2 * a)) == F["ask_b"][code]["pct"],
           "%d of %d against %d" % (k, a, F["ask_b"][code]["pct"]))

    # every format reads back, and the goldens carry the same figures
    wb = openpyxl.load_workbook(os.path.join(T, "pcn_practice_profiles_2026.xlsx"), read_only=True)
    ok("V7 the profiles workbook reads back", len(list(wb.active.iter_rows(values_only=True))) >= 10)
    brief = " ".join(p.extract_text() for p in PdfReader(os.path.join(T, "statin_continuity_sessions_brief.pdf")).pages)
    brief = " ".join(brief.split())
    ok("V8 the brief files the window and the rounding", "1 March to 30 June 2027" in brief and "nearest 10" in brief)
    spec = " ".join(p.extract_text() for p in PdfReader(os.path.join(T, "icb_cvd_repeat_return_2025_spec.pdf")).pages)
    spec = " ".join(spec.split())
    ok("V9 the specification defines both measures", "80 per cent" in spec and "first anniversary" in spec)
    gw = openpyxl.load_workbook(os.path.join(G, "statin_sessions_2027.xlsx"))
    ws = gw["Placement"]
    rows = [r for r in ws.iter_rows(min_row=5, max_row=11, values_only=True)]
    ok("V10 the golden workbook's placement, runner-up and populations", rows[0][0] == "Sessions" and rows[0][2] == F["call"]
       and rows[1][0] == "Next" and rows[1][2] == F["runner_up"] and all(r[3] == F["population"][r[2]] for r in rows))
    gc = list(csv.DictReader(open(os.path.join(G, "cvd_repeat_returns_2025.csv"), encoding="utf-8")))
    ok("V11 the golden return carries the figures", all(float(r["r1_percent"]) == F["ask_a"][r["ods_code"]]["pct"]
                                                        and int(r["r2_percent"]) == F["ask_b"][r["ods_code"]]["pct"] for r in gc))
    print("%d failed" % len(FAIL))
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
