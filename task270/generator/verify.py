"""An independent recomputation of every graded figure from target/ alone, written apart from pack.py and analysis.py
(pandas, its own parsing, joins and exposure walk), compared with generator/figures.json."""
import datetime as dt
import json
import os
import sys

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
REGION_NAMES = {"NEC": "North East and Cumbria", "NWE": "North West", "YHU": "Yorkshire and the Humber",
                "EMI": "East Midlands", "WMI": "West Midlands", "EOE": "East of England", "SEA": "South East",
                "SWW": "South West and Wales"}


def load_map(t):
    m = pd.read_csv(os.path.join(t, "rating_region_postcode_map.csv"), dtype=str, keep_default_na=False)
    spans = {}
    for r in m.itertuples():
        a = dt.date.fromisoformat(r.effective_from)
        b = dt.date.fromisoformat(r.effective_to) if r.effective_to else dt.date(2100, 1, 1)
        spans.setdefault(r.postcode_district, []).append((a, b, r.rating_region_code))
    return spans


def region(spans, district, day):
    for a, b, code in spans[district]:
        if a <= day <= b:
            return code
    raise KeyError(district)


def load_terms(t):
    leg = pd.read_csv(os.path.join(t, "policy_terms_legacy_export_2023_2025.csv"), dtype=str, keep_default_na=False)
    plat = pd.read_csv(os.path.join(t, "policy_terms_platform_export_2025_2026.csv"), dtype=str, keep_default_na=False)
    p = lambda s: dt.datetime.strptime(s, "%d/%m/%Y").date()
    out = []
    for r in leg.itertuples():
        stop = p(r.EXPIRY_DATE) + dt.timedelta(days=1)
        if r.CANCELLATION_DATE:
            stop = min(stop, p(r.CANCELLATION_DATE) + dt.timedelta(days=1))
        out.append((r.POLICY_NO, int(r.TERM_NO), p(r.INCEPTION_DATE), stop, r.GARAGING_DISTRICT,
                    "COMP" if r.COVER == "COMP" else "TPFT", int(r.NCD_STEP), r.STEP_PROTECTION == "Y"))
    for r in plat.itertuples():
        stop = dt.date.fromisoformat(r.term_end)
        if r.cancellation_date:
            stop = min(stop, dt.date.fromisoformat(r.cancellation_date))
        out.append((r.policy_number, int(r.term_number), dt.date.fromisoformat(r.term_start), stop,
                    r.garaging_postcode.split()[0], "COMP" if r.cover_type == "Comprehensive" else "TPFT",
                    int(r.ncd_step), r.step_protection == "true"))
    terms = pd.DataFrame(out, columns=["pol", "seq", "start", "stop", "district", "cover", "step", "prot"])
    adj = pd.read_csv(os.path.join(t, "mid_term_adjustments_2023_2026.csv"), dtype=str, keep_default_na=False)
    changes = {}
    for r in adj.itertuples():
        d = dt.date.fromisoformat(r.effective_date)
        new_d = r.new_garaging.split()[0] if r.new_garaging else None
        new_c = {"COMP": "COMP", "TPFT": "TPFT", "Comprehensive": "COMP",
                 "Third party, fire and theft": "TPFT"}.get(r.new_cover)
        changes.setdefault((r.policy_number, int(r.term_number)), []).append((d, new_d, new_c))
    return terms, changes


def walk(term, changes, spans, lo, hi):
    """Yield (days, region, cover) for the part of a policy year inside [lo, hi)."""
    a, b = max(term.start, lo), min(term.stop, hi)
    if b <= a:
        return
    ch = sorted(changes.get((term.pol, term.seq), []), key=lambda x: x[0])
    marks = {a, b} | {d for d, _, _ in ch if a < d < b} | {dt.date(2025, 4, 1)} & {x for x in [dt.date(2025, 4, 1)] if a < x < b}
    marks = sorted(marks)
    for x, y in zip(marks, marks[1:]):
        dist, cov = term.district, term.cover
        for d, nd, nc in ch:
            if d <= x:
                dist = nd or dist
                cov = nc or cov
        yield (y - x).days, region(spans, dist, x), cov


def state(term, changes, day):
    dist = term.district
    for d, nd, nc in sorted(changes.get((term.pol, term.seq), []), key=lambda x: x[0]):
        if d <= day and nd:
            dist = nd
    return dist


def load_claims(t):
    leg = pd.read_csv(os.path.join(t, "claims_legacy_export_2023_2025.csv"), dtype=str, keep_default_na=False)
    plat = pd.read_csv(os.path.join(t, "claims_platform_export_2025_2026.csv"), dtype=str, keep_default_na=False)
    p = lambda s: dt.datetime.strptime(s, "%d/%m/%Y").date()
    rows = []
    kind = {"ACC": "ACC", "WSC": "WSC", "THF": "THF", "FIR": "FIR", "Accident": "ACC", "Windscreen": "WSC",
            "Theft": "THF", "Fire": "FIR"}
    for r in leg.itertuples():
        rows.append((r.CLAIM_NO, r.POLICY_NO, p(r.LOSS_DATE), p(r.NOTIFIED_DATE), kind[r.CLAIM_TYPE],
                     (int(r.PAID_AMT) + int(r.OS_AMT)) / 100.0, r.POLICE_REF.replace("/", ""), r.SUPPLIER, "L"))
    bst = {2025: (dt.date(2025, 3, 30), dt.date(2025, 10, 26)), 2026: (dt.date(2026, 3, 29), dt.date(2026, 10, 25))}
    for r in plat.itertuples():
        u = dt.datetime.strptime(r.notified_at, "%Y-%m-%dT%H:%M:%SZ")
        loc = u + dt.timedelta(hours=1)
        a, b = bst[u.year]
        day = loc.date() if a <= loc.date() < b else u.date()
        rows.append((r.claim_number, r.policy_number, dt.date.fromisoformat(r.loss_date), day, kind[r.claim_type],
                     round(float(r.paid_gbp) + float(r.outstanding_gbp), 2), r.police_reference, r.supplier, "P"))
    return pd.DataFrame(rows, columns=["no", "pol", "loss", "notified", "kind", "incurred", "police", "supplier", "sys"])


def run(task):
    t = os.path.join(task, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    spans = load_map(t)
    terms, changes = load_terms(t)
    xw = pd.read_csv(os.path.join(t, "policy_number_crosswalk_2025.csv"), dtype=str)
    other = dict(zip(xw.platform_policy_number, xw.legacy_policy_no))
    other.update(dict(zip(xw.legacy_policy_no, xw.platform_policy_number)))
    by_pol = {}
    for tm in terms.itertuples():
        by_pol.setdefault(tm.pol, []).append(tm)

    def cover_term(pol, day):
        for q in (pol, other.get(pol)):
            for tm in by_pol.get(q, []):
                if tm.start <= day < tm.stop:
                    return tm
        return None

    E, E25, E25c = {}, {}, {}
    for tm in terms.itertuples():
        for days, reg, cov in walk(tm, changes, spans, dt.date(2024, 1, 1), dt.date(2026, 1, 1)):
            E[reg] = E.get(reg, 0) + days
        for days, reg, cov in walk(tm, changes, spans, dt.date(2025, 1, 1), dt.date(2026, 1, 1)):
            E25[reg] = E25.get(reg, 0) + days
            if cov == "COMP":
                E25c[reg] = E25c.get(reg, 0) + days
    E = {k: v / 365.0 for k, v in E.items()}
    E25 = {k: v / 365.0 for k, v in E25.items()}
    E25c = {k: v / 365.0 for k, v in E25c.items()}
    cl = load_claims(t)
    acc = cl[(cl.kind == "ACC") & (cl.incurred > 0) & cl.loss.map(lambda d: d.year in (2024, 2025))]
    recs = []
    for r in acc.itertuples():
        tm = cover_term(r.pol, r.loss)
        recs.append((region(spans, state(tm, changes, r.loss), r.loss), tm.step == 0 or tm.prot, r.incurred))
    a = pd.DataFrame(recs, columns=["region", "full", "incurred"])
    bad = []
    rep = a.groupby("region").size()
    for c in REGION_NAMES:
        if rep[c] != fig["components"]["reported_claims"][REGION_NAMES[c]]:
            bad.append(("reported claims", c))
        if round(E[c]) != fig["components"]["vehicle_years"][REGION_NAMES[c]]:
            bad.append(("vehicle-years", c))
        if round(100 * rep[c] / E[c], 1) != fig["components"]["reported_frequency"][REGION_NAMES[c]]:
            bad.append(("reported frequency", c))
    for T in (1500, 2000, 2500, 3000):
        share = (a[a.full].incurred > T).mean()
        est = {c: 100 * (a[(a.region == c)].incurred > T).sum() / share / E[c] for c in REGION_NAMES}
        top = sorted(est, key=lambda c: -est[c])
        if sorted(top[:3]) != sorted(fig["call"]["band"]) or top[3] != fig["call"]["below"]:
            bad.append(("band at", T, top[:4]))
        if T == 2500:
            for c in REGION_NAMES:
                if round(est[c], 1) != fig["basis_2027"]["frequency"][REGION_NAMES[c]]:
                    bad.append(("2027 frequency", c, round(est[c], 2)))
    # windscreen: the partner's jobs billed to the Society and the claims that are not those jobs on the platform
    gl = pd.read_csv(os.path.join(t, "glass_partner_jobs_2025.csv"), dtype=str, keep_default_na=False)
    gl = gl[gl.billed_to == "Fennacre Mutual"].copy()
    gl["net"] = gl.net_amount.astype(float)
    gl["gross"] = gl.net + gl.vat_amount.astype(float)
    gl["day"] = gl.booked.map(lambda s: dt.datetime.strptime(s[:10], "%d/%m/%Y").date())
    gl["work"] = gl.description.isin(["Windscreen replacement", "Windscreen repair"])
    jobs = gl.groupby("job_ref").agg(pol=("insurer_policy_ref", "first"), day=("day", "first"), net=("net", "sum"),
                                     gross=("gross", "sum"), work=("work", "any")).reset_index()
    seen = set(zip(jobs.pol, jobs.day, jobs.net.round(2)))
    ws = cl[(cl.kind == "WSC") & (cl.incurred > 0)]
    own = ws[[not (r.sys == "P" and (r.pol, r.notified, round(r.incurred, 2)) in seen) for r in ws.itertuples()]].copy()
    # a partner job that is a camera recalibration alone: the recalibration of the screen another repairer fitted,
    # part of that repairer's claim on the same policy (the last one dated on or before the job)
    own["person"] = [other.get(p, p) if p.startswith("FNM") else p for p in own.pol]
    add = {}
    for r in jobs[~jobs.work].itertuples():
        person = other.get(r.pol, r.pol) if r.pol.startswith("FNM") else r.pol
        cand = own[(own.person == person) & (own.loss <= r.day)].sort_values(["loss", "notified", "no"])
        if cand.empty:
            bad.append(("recalibration with no replacement", r.job_ref))
            continue
        add[cand.no.iloc[-1]] = add.get(cand.no.iloc[-1], 0.0) + r.gross
    own = own[own.notified.map(lambda d: d.year == 2025)]
    n, cost = {}, {}
    for r in jobs[jobs.work].itertuples():
        reg = region(spans, state(cover_term(r.pol, r.day), changes, r.day), r.day)
        n[reg] = n.get(reg, 0) + 1
        cost[reg] = cost.get(reg, 0) + r.gross
    for r in own.itertuples():
        reg = region(spans, state(cover_term(r.pol, r.notified), changes, r.notified), r.notified)
        n[reg] = n.get(reg, 0) + 1
        cost[reg] = cost.get(reg, 0) + r.incurred + add.get(r.no, 0.0)
    for c in REGION_NAMES:
        if round(100 * n[c] / E25c[c], 1) != fig["ask_a"]["frequency"][REGION_NAMES[c]]:
            bad.append(("windscreen frequency", c))
        if round(cost[c] / n[c]) != fig["ask_a"]["average"][REGION_NAMES[c]]:
            bad.append(("windscreen average", c, cost[c] / n[c]))
    # theft: a theft's claims share a crime reference
    sal = pd.concat(pd.read_excel(os.path.join(t, "salvage_sales_statements_2025_2026.xlsx"), sheet_name=None).values())
    proceeds = sal.groupby("Client claim ref")["Net proceeds remitted (GBP)"].sum().to_dict()
    th = cl[cl.kind == "THF"]
    n, cost = {}, {}
    for ref, g in th.groupby("police"):
        g = g.sort_values(["loss", "notified", "no"])
        first = g.iloc[0]
        if first.loss.year != 2025 or g.incurred.sum() <= 0:
            continue
        reg = region(spans, state(cover_term(first.pol, first.loss), changes, first.loss), first.loss)
        n[reg] = n.get(reg, 0) + 1
        cost[reg] = cost.get(reg, 0) + g.incurred.sum() - sum(proceeds.get(x, 0.0) for x in g.no)
    for c in REGION_NAMES:
        if round(1000 * n[c] / E25[c], 1) != fig["ask_b"]["frequency"][REGION_NAMES[c]]:
            bad.append(("theft frequency", c))
        if round(cost[c] / n[c]) != fig["ask_b"]["average"][REGION_NAMES[c]]:
            bad.append(("theft average", c, cost[c] / n[c]))
    print("verify: %s" % ("clean, every graded figure recomputed" if not bad else "MISMATCH %s" % bad[:12]))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(run(os.path.dirname(HERE)))
