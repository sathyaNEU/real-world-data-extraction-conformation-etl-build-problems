"""task447 ask layer against the careful solver's routes, on the cut pack.

    python3 task447/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The asks are the
review's two lakeshore patient exhibits (rule 4.07, appendix A2 and A3), 20 whole numbers: Exhibit 1, the commercial
patients living in Manitowoc and Kewaunee counties whom Ledgestone's and Kinnickinnic's physicians saw in person in
2024 in each of four specialties (8) and whom each independent practice's physicians saw (5); Exhibit 2, the patients
each independent practice referred for outpatient imaging, and the gastroenterology and orthopaedic practices for
endoscopy and arthroscopy (7). A figure is kept when it equals figures.json's.

The devices: three in four of the members covered twice were not linked by the database's person index, so their
second plan's spans and office claims carry another member key (Exhibit 1); some members hold a second record at their
own carrier, opened at a re-enrolment, with one facility service billed under both (Exhibit 2). No field says so; the
claims force it (the second plan's claim priced on the first's member liability, or one carrier's two claims for one
service, with one birth year, sex and ZIP).

The cracker is the careful solver, never a narrowed one: it lands the call (R5), runs the hygiene battery and executes
every filed rule as worded: rule 4.02(b), (c) and (e), A1's service lines, A2 (residence on the span covering the
date, an in-person office visit at a location in the two counties, a physician's own taxonomy as the carriers'
provider files record it, a person seen more than once one patient), A3 (the latest version net of voids, the
referring physician's practice on the date), A4 (physicians only, the register's control) and A6's counties; it
counts the people the database's member keys name, and its natural cleanup of duplicate records (one carrier, birth
year, sex and ZIP) and a person key on birth year, sex and ZIP are printed beside it. Its handling is written here,
apart from golden.py. The mirror stops at the default path (R4, the product-by-product share, close) and, the asks
being decoupled from the call, reads both exhibits as the cracker does. The full includer is golden.py's route with
every key linked and has to give back figures.json exactly (the route code's control). The reconstruction that finds
the people (one birth year, sex and ZIP with one service under two keys, any carrier) is printed as what it is.

The pair is the ask sheet's formula: 38 recommendation and components, 7 instruction following, 55 asks over the 20
figures, the response off the call keeping r = 3 of the 38 (the professional part, right on every rung); the same with
r = 5 is printed beside it. Pair ceiling is the worse of the two. Exit 0 when the gate holds (the cracker keeps no ask
figure, the pair at or under 60, the mirror under half the ask weight, and two careful responses on the call under
70), 2 when it does not, 1 when a control fails."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile
from collections import defaultdict

import pdfplumber

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as G     # noqa: E402

TASK = os.path.dirname(HERE)
PAIR_GATE = 60.0
WEIGHTS = {"ask sheet (38, 7, 55; off the call keeps 3)": (38.0, 7.0, 55.0, 3.0),
           "comparable (38, 7, 55; off the call keeps 5)": (38.0, 7.0, 55.0, 5.0)}
PHYSICIAN = {"MD", "DO", "M.D.", "D.O."}        # A4: a doctor of medicine or of osteopathic medicine
A2_SPECIALTY = {"207Q00000X": "primary care", "207R00000X": "primary care", "208000000X": "primary care",
                "207RG0100X": "gastroenterology", "207X00000X": "orthopaedic surgery",
                "207RC0000X": "cardiovascular disease"}
OFFICE = {str(c) for c in range(99202, 99216)}
LINES = {"IMG": "imaging", "ENDO": "endoscopy", "ARTH": "arthroscopy"}


# ------------------------------------------------------------------ the pack
def pack_dir(arg):
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling447-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    md5 = hashlib.md5(open(src, "rb").read()).hexdigest()
    return tmp, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(tmp)), md5)


def context(folder):
    X = G.load(folder)
    zc = G.zip_county(folder)                       # appendix A6
    spans = G.billing_spans(X["reassign"])
    ctrl = G.Control(X["register"])
    with pdfplumber.open(os.path.join(folder, "N25-014_notice_of_material_change.pdf")) as pdf:
        text = " ".join(pg.extract_text() or "" for pg in pdf.pages)
    bmg = re.search(r"Brightwater's number\s*\((\d{2}-\d{7})\)", text).group(1)
    return X, zc, spans, ctrl, bmg


# ------------------------------------------------------------------ the people, by the reading
def readings(X):
    """Each way a solver may take the person behind a member key: a function of (member key, date)."""
    el = X["elig"]
    demo = defaultdict(list)
    for m, s_, e_, by, sx, z in zip(el["member_id"], el["start"], el["end"], el["birth_year"], el["sex"],
                                    el["member_zip"]):
        demo[m].append((s_, e_, (by, sx, z)))
    on = lambda m, d: next((v for s_, e_, v in demo.get(m, ()) if s_ <= d <= e_), None)
    car = el.groupby("member_id")["submitter_code"].first().to_dict()

    def linked(any_carrier):
        parent = {}

        def find(m):
            while parent.get(m, m) != m:
                m = parent[m]
            return m
        for df, cols in ((X["fac"], ["procedure_code", "procedure_modifier_1", "service_facility_npi", "referring_provider_npi"]),
                         (X["prof"], ["procedure_code", "procedure_modifier_1", "rendering_provider_npi", "billing_provider_tin"])):
            f = df[(df["dos"].dt.year == 2024) & (df["claim_frequency_code"] == "1")]
            groups = defaultdict(list)
            for t, sub, m in zip(zip(f["dos"], *[f[c] for c in cols], f["qty"]), f["submitter_code"], f["member_id"]):
                groups[t].append((sub, m))
            for t, lst in groups.items():
                for i in range(len(lst)):
                    for j in range(i + 1, len(lst)):
                        (s1, m1), (s2, m2) = lst[i], lst[j]
                        if m1 != m2 and (any_carrier or s1 != s2) and on(m1, t[0]) is not None and on(m1, t[0]) == on(m2, t[0]):
                            a, b = find(m1), find(m2)
                            if a != b:
                                parent[max(a, b)] = min(a, b)
        return lambda m, d: find(m)
    return {
        "keys": lambda m, d: m,
        "records": lambda m, d: ("p", car.get(m)) + on(m, d) if on(m, d) else m,
        "demographics": lambda m, d: ("p",) + on(m, d) if on(m, d) else m,
        "service, two carriers": linked(False),
        "service, any carrier": linked(True),
    }


# ------------------------------------------------------------------ the careful solver's own code, apart from golden.py
def _latest(df):
    """4.02(c) and A3: the latest version, net of voids; a replacement whose reference names no claim replaces the one
    original for the same carrier, member, date, code and physician (or facility)."""
    named = set(df.loc[df["claim_frequency_code"].isin(["7", "8"]), "original_claim_control_number"])
    cnos = set(df["payer_claim_control_number"])
    k = ["submitter_code", "member_id", "service_from_date", "procedure_code"] + (
        ["rendering_provider_npi"] if "rendering_provider_npi" in df.columns else ["service_facility_npi"])
    orig = df[(df["claim_frequency_code"] == "1") & ~df["payer_claim_control_number"].isin(named)]
    by = defaultdict(list)
    for t, c in zip(zip(*[orig[c] for c in k]), orig["payer_claim_control_number"]):
        by[t].append(c)
    r7 = df[(df["claim_frequency_code"] == "7") & ~df["original_claim_control_number"].isin(cnos)]
    for t in zip(*[r7[c] for c in k]):
        if len(by.get(t, ())) == 1:
            named.add(by[t][0])
    return df[df["claim_frequency_code"].isin(["1", "7"]) & ~df["payer_claim_control_number"].isin(named)]


def _county(X, zc):
    idx = defaultdict(list)
    el = X["elig"]
    for m, p_, s_, e_, z in zip(el["member_id"], el["product_id"], el["start"], el["end"], el["member_zip"]):
        idx[(m, p_)].append((s_, e_, z))
    return lambda m, p_, d: zc.get(next((z for s_, e_, z in idx.get((m, p_), ()) if s_ <= d <= e_), None))


def _independents(X, zc, ctrl, bmg):
    p = X["prof"]
    p = p[(p["dos"].dt.year == 2024) & p["procedure_code"].isin(OFFICE) & p["service_facility_zip"].map(zc).isin(G.EX_COUNTIES)]
    tins = {t for t, d in zip(p["billing_provider_tin"], p["dos"]) if t != bmg and ctrl.system_of(t, d) is None}
    pv = X["provfile"]
    out = {}
    for t in sorted(tins):
        names = sorted(set(pv.loc[pv["billing_tin"] == t, "practice_name"]), key=lambda n: (n.isupper(), len(n), n))
        out[t] = names[0]
    return out


def natural_seen(ctx, who):
    X, zc, spans, ctrl, bmg = ctx
    commercial = set(X["prodref"].loc[X["prodref"]["line_of_business"] == "Commercial", "product_id"])   # 4.02(b)
    p = X["prof"]
    p = p[(p["dos"].dt.year == 2024) & p["product_id"].isin(commercial) & p["procedure_code"].isin(OFFICE)]
    p = p[p["service_facility_zip"].map(zc).isin(G.EX_COUNTIES)]
    p = p[(p["place_of_service"] != "10") & (p["procedure_modifier_1"] != "95") & (p["procedure_modifier_2"] != "95")]
    p = _latest(p)
    county = _county(X, zc)
    pv = X["provfile"]
    own_tax = pv.groupby("provider_npi")["primary_taxonomy"].agg(lambda s: sorted(set(s))[0]).to_dict()
    cred = pv.groupby("provider_npi")["credential"].agg(lambda s: sorted(set(s))[0]).to_dict()
    ind = _independents(X, zc, ctrl, bmg)
    cells = defaultdict(set)
    for r in p.itertuples(index=False):
        if county(r.member_id, r.product_id, r.dos) not in G.EX_COUNTIES:
            continue
        npi = r.rendering_provider_npi
        if cred.get(npi) not in PHYSICIAN:
            continue
        sysn = ctrl.system_of(r.billing_provider_tin, r.dos)
        if sysn in ("Ledgestone Health", "Kinnickinnic Health"):
            sp = A2_SPECIALTY.get(own_tax.get(npi))
            if sp:
                cells["%s|%s" % (sysn, sp)].add(who(r.member_id, r.dos))
        elif r.billing_provider_tin in ind:
            cells[ind[r.billing_provider_tin]].add(who(r.member_id, r.dos))
    return {k: len(v) for k, v in cells.items()}


def natural_referred(ctx, who):
    X, zc, spans, ctrl, bmg = ctx
    commercial = set(X["prodref"].loc[X["prodref"]["line_of_business"] == "Commercial", "product_id"])
    f = X["fac"]
    f = f[(f["dos"].dt.year == 2024) & f["product_id"].isin(commercial)]
    f = f[f["procedure_code"].map(G.family).isin(G.EX1_LINES)]
    f = _latest(f)
    county = _county(X, zc)
    ind = _independents(X, zc, ctrl, bmg)
    cells = defaultdict(set)
    for r in f.itertuples(index=False):
        if county(r.member_id, r.product_id, r.dos) not in G.EX_COUNTIES:
            continue
        prac = {ind[t] for t, s_, e_ in spans.get(r.referring_provider_npi, ()) if s_ <= r.dos <= e_ and t in ind}
        if len(prac) == 1:
            cells["%s|%s" % (prac.pop(), G.family(r.procedure_code))].add(who(r.member_id, r.dos))
    return {k: len(v) for k, v in cells.items()}


def without_member(ctx, payment=True):
    """A duplicate check run without the member key: claim lines identical but for the member key, the claim number and
    the paid date (payment False: and the plan's and the member's shares), the first paid kept."""
    X, zc, spans, ctrl, bmg = ctx
    Y = dict(X)
    drop = {"member_id", "payer_claim_control_number", "paid_date", "paid", "dos", "qty", "allowed"}
    if not payment:
        drop |= {"plan_paid_amount", "member_liability_amount"}
    for k in ("fac", "prof"):
        df = X[k].sort_values(["paid", "payer_claim_control_number"], kind="mergesort")
        cols = [c for c in df.columns if c not in drop]
        Y[k] = df[~df.duplicated(cols, keep="first")].sort_index()
    return (Y, zc, spans, ctrl, bmg)


def route(ctx, who):
    out = {("ex1", k): v for k, v in natural_seen(ctx, who).items()}
    out.update({("ex2", k): v for k, v in natural_referred(ctx, who).items()})
    return out


def golden_route(ctx, link=True):
    X, zc, spans, ctrl, bmg = ctx
    cell = lambda c: c[0] if c[1] is None else "%s|%s" % c
    out = {("ex1", cell(c)): v for c, v in G.patients_seen(X, zc, ctrl, bmg, link=link).items()}
    out.update({("ex2", cell(c)): v for c, v in G.patients_referred(X, zc, ctrl, spans, bmg, link=link).items()})
    return out


# ------------------------------------------------------------------ scoring against figures.json
def gold_figures():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    out = {("ex1", k): v for k, v in figs["ex1"].items()}
    out.update({("ex2", k): v for k, v in figs["ex2"].items()})
    return figs, out


def stated(k, v):
    return "{:,}".format(int(v))


def kept(k, v, gold):
    return v is not None and stated(k, v) == gold


BLOCKS = [("Exhibit 1, Ledgestone's and Kinnickinnic's patients by specialty", lambda k: k[0] == "ex1" and "|" in k[1]),
          ("Exhibit 1, each independent practice's patients", lambda k: k[0] == "ex1" and "|" not in k[1]),
          ("Exhibit 2, the independent practices' referred patients", lambda k: k[0] == "ex2")]


def score(fig, gold):
    by = {name: sum(kept(k, fig.get(k), gold[k]) for k in gold if sel(k)) for name, sel in BLOCKS}
    return by, sum(by.values())


def pair(kc, km, n, w):
    rec, ins, ask, off = w
    c = rec + ins + ask * kc / n
    s = off + ins + ask * km / n
    return c, s, (c + s) / 2.0


def show(name, fig, gold):
    by, k = score(fig, gold)
    print("  %-84s %2d of %d  (%s)" % (name, k, len(gold), ", ".join("%d" % by[b] for b, _ in BLOCKS)))
    return k


# ------------------------------------------------------------------ the run
def main(arg=None):
    folder, scratch, stamp = pack_dir(arg)
    try:
        return run(folder, stamp)
    finally:
        if scratch:
            shutil.rmtree(scratch)


def run(folder, stamp):
    print("pack: " + stamp)
    figs, gold = gold_figures()
    n = len(gold)
    g = G.compute(folder)
    L = G.ladder(folder, g)
    c_call, c_total = g["call"], "%.1f" % (g["total"] / 1e6)
    r4 = L["rungs"]["R4 product by product"]
    m_call, m_total = ("proceed" if r4 >= G.THRESHOLD else "close"), "%.1f" % (r4 / 1e6)
    on_call = (c_call, c_total) == (figs["call"], figs["total_m"])
    print("cracker's call (R5, the tier in the projection year): %s at %s million (%s the golden's %s at %s)"
          % (c_call, c_total, "lands" if on_call else "MISSES", figs["call"], figs["total_m"]))
    print("mirror's call (R4, product by product, the default path): %s at %s million (%s)"
          % (m_call, m_total, "off the call" if m_call != figs["call"] else "ON THE CALL"))
    if not on_call or m_call == figs["call"]:
        print("CONTROL FAILED: the rows below assume the cracker on the call and the mirror off it")
        return 1
    ctx = context(folder)
    full = golden_route(ctx)
    bad = [k for k in gold if stated(k, full.get(k, -1)) != gold[k]]
    if bad:
        print("CONTROL FAILED: the full includer does not reproduce figures.json at %s" % bad)
        return 1
    print("full includer (golden.py's route, every key linked): reproduces figures.json exactly, %d of %d" % (n, n))
    R = readings(ctx[0])
    print("\nroutes, figures kept of %d (blocks: %s):" % (n, "; ".join(b for b, _ in BLOCKS)))
    cracker = route(ctx, R["keys"])
    kc = show("cracker: R5, the battery, every filed rule as worded, the people the member keys name", cracker, gold)
    mirror = route(ctx, R["keys"])
    km = show("mirror: R4, the same reading of A2 and A3", mirror, gold)
    print("  the careful solver's own cleanups of the people:")
    show("    duplicate records cleaned on one carrier, birth year, sex and ZIP", route(ctx, R["records"]), gold)
    show("    a person key on birth year, sex and ZIP", route(ctx, R["demographics"]), gold)
    k_rows = max(show("    claim lines identical but for the member key, claim number and paid date, one kept",
                      route(without_member(ctx), R["keys"]), gold),
                 show("    the same, the plan's and the member's shares left out too",
                      route(without_member(ctx, False), R["keys"]), gold))
    print("  the reconstruction (one birth year, sex and ZIP with one service under two keys):")
    k2 = show("    across two carriers only", route(ctx, R["service, two carriers"]), gold)
    k_any = show("    under any carrier (the people the claims force)", route(ctx, R["service, any carrier"]), gold)
    agree = all(stated(k, golden_route(ctx, link=False).get(k, 0)) == stated(k, cracker.get(k, 0)) for k in gold)
    print("  the two implementations agree on the cracker's read: %s" % ("yes" if agree else "NO"))
    if not agree:
        print("CONTROL FAILED: golden.py's route and the cracker's own code differ on the cracker's read")
        return 1
    print("\nthe cracker's figures against figures.json (stated, golden):")
    for k in gold:
        print("  %-52s %-8s %-8s %s" % (" ".join(k), stated(k, cracker.get(k, 0)), gold[k],
                                         "kept" if kept(k, cracker.get(k), gold[k]) else "miss"))
    worst = []
    both = []
    for wname, w in WEIGHTS.items():
        c, s, p = pair(kc, km, n, w)
        worst.append(p)
        both.append(c)
        print("\n%s: cracker %.1f, mirror %.1f, pair %.1f; two careful responses on the call %.1f" % (wname, c, s, p, c))
        print("  (on the call beside the mirror: the people reconstructed under any carrier, %d of %d, %.1f and pair %.1f; "
              "across two carriers only, %d of %d, %.1f and pair %.1f; the stronger duplicate check without the "
              "member key, %d of %d, %.1f and pair %.1f)" % (k_any, n, pair(k_any, km, n, w)[0], pair(k_any, km, n, w)[2], k2, n,
                                                 pair(k2, km, n, w)[0], pair(k2, km, n, w)[2], k_rows, n,
                                                 pair(k_rows, km, n, w)[0], pair(k_rows, km, n, w)[2]))
    leak = 100.0 * km / n
    pc = max(worst)
    print("\nCracker keeps: %d of %d ask figures" % (kc, n))
    print("Mirror leakage: %.1f per cent of ask weight" % leak)
    print("Pair ceiling: %.1f (the worse of the measured pair on either weighting)" % pc)
    ok = kc == 0 and pc <= PAIR_GATE and leak < 50.0 and max(both) < 70.0
    print("gate %s: it needs the cracker to keep no ask figure, the pair at or under %.0f, the mirror's leakage under 50 "
          "per cent and two careful responses on the call under 70" % ("HOLDS" if ok else "FAILS", PAIR_GATE))
    return 0 if ok else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
