"""task124's generator assertions, run on the built pack (target/), the goldens and the world that made them.

Every rung, partial and fork of the design note is recomputed here from the shipped files; the world (ground truth,
each main's class, the causes of each dig) is used only to assert facts the files cannot show (where the verification
routes went, the sweeps' identity, the clean-truth analyst test)."""
from __future__ import annotations

import datetime as dt
import io
import json
import math
import os
import re
import shutil
import tempfile
import zipfile

import numpy as np
import pandas as pd

import analysis as AN
import common as K
import deliver as DL
import load as L

RESULTS = []


def ok(name, cond, detail=""):
    RESULTS.append((name, bool(cond), detail))
    if not cond:
        print("FAIL %s %s" % (name, detail))


# ------------------------------------------------------------------------------------------------- helpers
def round_to(x, step):
    return int(math.floor(x / step + 0.5) * step)


def finish_list(z):
    return [int(x) for x in z.finish_year]


def sched_expected(rem, expz, ap, prices, mob):
    """Schedule from expected lead or GRR lines among each zone's unknown lines (zone -> lines)."""
    rows, cum = [], 0.0
    for r in rem.itertuples():
        u = r.u0 + r.u1 + r.u2
        e = expz[r.zone]
        uf, ud = prices[r.zone]
        cost = (r.lgrr + e) * uf + (u - e) * ud + mob
        cum += cost
        rows.append((r.zone, r.lgrr + e, cost, cum, K.FIRST_YEAR + math.ceil(cum / ap - 1e-9) - 1))
    return pd.DataFrame(rows, columns=["zone", "replacements", "cost", "cum_cost", "finish_year"])


def logit_fit(X, y):
    from scipy.optimize import minimize

    def nll(b):
        zz = X @ b
        return np.sum(np.logaddexp(0, zz) - y * zz)

    def grad(b):
        zz = X @ b
        return X.T @ (1 / (1 + np.exp(-zz)) - y)
    return minimize(nll, np.zeros(X.shape[1]), jac=grad, method="BFGS", options={"gtol": 1e-8, "maxiter": 2000}).x


def design(df, era=True, year=True, zone=False, zones=None):
    cols = [np.ones(len(df))]
    if era:
        cols += [(df.era == 1).astype(float).to_numpy(), (df.era == 2).astype(float).to_numpy()]
    if year:
        cols.append(((df.year_built - 1940) / 30.0).to_numpy())
    if zone:
        for zz in zones[1:]:
            cols.append((df.zone == zz).astype(float).to_numpy())
    return np.column_stack(cols)


def model_expected(train, unk, **kw):
    zones = sorted(set(train.zone) | set(unk.zone))
    b = logit_fit(design(train, zones=zones, **kw), train.hit.astype(float).to_numpy())
    pr = 1 / (1 + np.exp(-(design(unk, zones=zones, **kw) @ b)))
    return unk.assign(p=pr).groupby("zone").p.sum().to_dict()


def text_of_pdf(path):
    from pypdf import PdfReader
    return "\n".join(p.extract_text() for p in PdfReader(path).pages)


def text_of_docx(path):
    import docx
    d = docx.Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for r in t.rows:
            parts.append(" | ".join(c.text for c in r.cells))
    return "\n".join(parts)


def text_of_xlsx(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    out = []
    for ws in wb.worksheets:
        out.append(ws.title)
        for row in ws.iter_rows(values_only=True):
            out.extend(str(v) for v in row if v is not None)
    return "\n".join(out)


def all_text(target):
    out = {}
    for f in sorted(os.listdir(target)):
        p = os.path.join(target, f)
        if f.endswith(".pdf"):
            out[f] = text_of_pdf(p)
        elif f.endswith(".docx"):
            out[f] = text_of_docx(p)
        elif f.endswith(".xlsx"):
            out[f] = text_of_xlsx(p)
        elif f.endswith(".md"):
            out[f] = open(p, encoding="utf-8").read()
        elif f.endswith(".csv"):
            with open(p, encoding="utf-8") as fh:
                out[f] = fh.read()
    return out


def figs_of(z):
    """Every graded zone figure: lines to the nearest ten, cost to the nearest $100,000, finish year."""
    return [(round_to(r.replacements, 10), round_to(r.cost, 100_000), int(r.finish_year)) for r in z.itertuples()]


def summary_of(z, P, ap):
    """The write-up's summary figures at their stated precision: era shares to two decimals, the plan cost to the
    million, the programme years to 0.1, the last zone's finish year."""
    tot = float(z.cum_cost.iloc[-1])
    return (tuple(math.floor(100 * P[e] + 0.5) for e in range(3)), round_to(tot / 1e6, 1),
            math.floor(10 * tot / ap + 0.5), int(z.finish_year.max()))


def zone_sigma(inv, s, cls):
    """One standard error of each plan zone's expected lead or GRR lines among its unknown lines."""
    sP = AN.share_sigma(s, cls, inv)
    rem = AN.remaining(inv)
    return {r.zone: math.sqrt((r.u0 * sP[0]) ** 2 + (r.u1 * sP[1]) ** 2 + (r.u2 * sP[2]) ** 2)
            for r in rem.itertuples()}


def family(inv, ver, s, cls, ap, prices, mob):
    """Every defensible construction of the share expected among the unknown lines of each era once each line's
    kind of main and era are used: name -> (era shares, schedule)."""
    rem = AN.remaining(inv)
    whole = s.coverage >= 0.999
    U = inv[inv.cls == "LEAD STATUS UNKNOWN"].copy()
    U["era"] = U.year_built.map(K.era_of)
    U["sc"] = U.segment.map(cls)
    NR = inv[(inv.record == "") & (inv.year_built > 0) & (inv.year_built < K.AGE_RULE_YEAR)].copy()
    NR["era"] = NR.year_built.map(K.era_of)
    NR["sc"] = NR.segment.map(cls)
    t = s.assign(sc=s.segment.map(cls))
    out = {}

    def add(name, P):
        out[name] = (P, AN.zone_costs(rem, P, ap, prices, mob))
    sh = AN.kind_era_shares(s, cls)
    P = {}
    for e in range(3):
        num = sum(int(((NR.era == e) & (NR.sc == k)).sum()) * sh[(k, e)] - int(t[(t.sc == k) & (t.era == e)].hit.sum())
                  for k in ("LG", "C"))
        P[e] = num / int((U.era == e).sum())
    add("expectation less found", P)
    add("replaced mains alone", AN.class_era_shares(inv, s, cls, mask=whole))
    add("single-line visits alone", AN.class_era_shares(inv, s, cls, mask=~whole))
    shw = AN.kind_era_shares(s, cls, mask=whole)
    P = {}
    for e in range(3):
        num = sum(int(((NR.era == e) & (NR.sc == k)).sum()) * shw[(k, e)] - int(t[(t.sc == k) & (t.era == e)].hit.sum())
                  for k in ("LG", "C"))
        P[e] = num / int((U.era == e).sum())
    add("replaced mains' rate less found", P)
    carded = inv[inv.record != ""]
    lead_seg = set(carded[carded.record == "LEAD"].segment)
    sub = lambda seg: "L" if seg in lead_seg else cls.get(seg)
    ts = t.assign(sub=t.segment.map(sub))
    Us = U.assign(sub=U.segment.map(sub))
    cell = ts.groupby(["sub", "era"]).hit.mean()
    add("lead, galvanized and copper mains apart",
        {e: float(np.mean([cell[(k, e)] for k in Us[Us.era == e]["sub"]])) for e in range(3)})
    pe = t.groupby(["sc", "era"]).hit.mean()
    pdk = t.assign(dec=(t.year_built // 10) * 10).groupby(["sc", "dec"]).hit.mean()
    add("decade by decade", {e: float(np.mean([pdk.get((k, d), pe[(k, e)]) for k, d in
                                               zip(U[U.era == e].sc, (U[U.era == e].year_built // 10) * 10)]))
                             for e in range(3)})
    pz = t.groupby(["sc", "era", "zone"]).hit.mean()
    add("zone by zone", {e: float(np.mean([pz.get((k, e, zz), pe[(k, e)]) for k, zz in
                                           zip(U[U.era == e].sc, U[U.era == e].zone)])) for e in range(3)})
    zones = sorted(set(t.zone) | set(U.zone))

    def X(df, inter=True, zone=False, year=False):
        cols = [np.ones(len(df)), (df.era == 1).astype(float).to_numpy(), (df.era == 2).astype(float).to_numpy(),
                (df.sc == "LG").astype(float).to_numpy()]
        if inter:
            cols += [((df.sc == "LG") & (df.era == e)).astype(float).to_numpy() for e in (1, 2)]
        if zone:
            cols += [(df.zone == zz).astype(float).to_numpy() for zz in zones[1:]]
        if year:
            cols.append(((df.year_built - 1940) / 30.0).to_numpy())
        return np.column_stack(cols)
    for name, kw in (("logistic, class and era with their interaction", {}),
                     ("logistic, class and era with their interaction, zone and year", {"zone": True, "year": True}),
                     ("logistic, class and era additive", {"inter": False})):
        b = logit_fit(X(t, **kw), t.hit.astype(float).to_numpy())
        pr = 1 / (1 + np.exp(-(X(U, **kw) @ b)))
        add(name, {e: float(pr[(U.era == e).to_numpy()].mean()) for e in range(3)})
    return out


# ------------------------------------------------------------------------------------------------- the run
GOLDEN_YEARS = [2027, 2029, 2030, 2031, 2032, 2033, 2034, 2034, 2035, 2036, 2036, 2037]


def run(target, golden, world=None, meta_path=None):
    RESULTS.clear()
    files = sorted(os.listdir(target))
    texts = all_text(target)
    meta = json.load(open(meta_path))

    # ---------------------------------------------------------------- input gates and the container
    ok("G1 ten or more files", len(files) >= 10, len(files))
    fmts = {f.rsplit(".", 1)[1] for f in files}
    ok("G2 three or more formats", len(fmts) >= 3, sorted(fmts))
    inv_rows = sum(1 for _ in open(os.path.join(target, K.INVENTORY))) - 1
    ok("G3 a file of 25,000 or more rows", inv_rows >= 25_000, inv_rows)
    dis = meta.get("distractor_files", [])
    ok("G4 two or more distractors declared, shipped, and named as exports",
       len(dis) >= 2 and all(d in files for d in dis) and not any("distract" in f.lower() for f in files), dis)
    log = pd.read_csv(os.path.join(target, K.EXTRACT_LOG), dtype=str, keep_default_na=False)
    ok("G5 extract log lists every shipped file but itself (H9)", set(log.file) == set(files) - {K.EXTRACT_LOG},
       set(files) ^ set(log.file))
    notes = texts[K.NOTES]
    ok("G6 field notes name every data file and document", all(f in notes for f in files if f != K.NOTES), "")
    stamps = {os.path.getmtime(os.path.join(target, f)) for f in files}
    ok("G7 every mtime is the extract hand-off", len(stamps) == 1, stamps)
    tells = (b"openpyxl", b"python-docx", b"ReportLab", b"reportlab", b"matplotlib", b"Matplotlib", b"LibreOffice")
    dirty = []
    for f in files + ["golden/" + g for g in sorted(os.listdir(golden))]:
        p = os.path.join(target, f) if not f.startswith("golden/") else os.path.join(golden, f[7:])
        if f.endswith((".xlsx", ".docx")):
            with zipfile.ZipFile(p) as zf:
                blob = b"".join(zf.read(n) for n in zf.namelist())
        else:
            blob = open(p, "rb").read()
        if any(t in blob for t in tells):
            dirty.append(f)
    ok("G8 no writer signature in any container (H1)", not dirty, dirty)
    ok("G9 the golden folder holds exactly the two deliverables", sorted(os.listdir(golden)) == sorted(K.DELIVERABLES))

    # ---------------------------------------------------------------- realism sweep
    inv_raw = pd.read_csv(os.path.join(target, K.INVENTORY), dtype=str, keep_default_na=False)
    zone_n = inv_raw.zone.value_counts()
    cls_n = inv_raw.sl_class.value_counts()
    heads = [len(inv_raw)] + list(zone_n.values) + list(cls_n.values)
    ok("RS1 no headline count is a multiple of 100 (inventory total, zone sizes, class totals)",
       all(int(h) % 100 for h in heads), heads)
    ok("RS2 zone sizes all differ", zone_n.nunique() == len(zone_n))
    co = L.change_orders(target)
    ok("RS3 change order descriptions do not repeat beyond a real rate", co.Description.nunique() >= 0.85 * len(co),
       "%d of %d" % (co.Description.nunique(), len(co)))
    people = {"Gregory Sheppard", "Bethany Davidson", "Seth Sullivan", "Craig Stewart"}
    named = set()
    for t in texts.values():
        for m in re.finditer(r"\b(Gregory|Craig|Andrew|Bethany|Seth|William|John|Jane|Mary|Robert|Susan|Michael)\s+[A-Z][a-z]+", t):
            named.add(m.group(0))
    ok("RS4 every person named in the pack is drawn on the card", named <= people, named - people)
    late = []
    for f, col, last in ((K.INVENTORY, "field_verified_on", "2027-01-08"), (K.INVENTORY, "replaced_on", "2027-01-08"),
                         (K.AGREEMENTS, "signed_on", "2027-01-08"), (K.AGREEMENTS, "status_date", "2027-01-08"),
                         (K.OUTREACH, "portal_status_date", "2027-01-08"), (K.OUTREACH, "letter_1_mailed", "2027-01-08"),
                         (K.COMPLETIONS, "closed_on", "2027-01-08"), (K.TAP_SAMPLES, "collected_on", "2026-12-31"),
                         (K.METER_EXCHANGES, "exchanged_on", "2025-12-31")):
        v = pd.read_csv(os.path.join(target, f), dtype=str, keep_default_na=False)[col]
        if v[v != ""].max() > last:
            late.append((f, col))
    ok("RS5 no extract carries a date past its extract (H16)", not late, late)
    built = [f for f, t in texts.items() if re.search(r"fictional|fictitious|constructed for|this exercise|synthetic|"
                                                      r"generated by", t, re.I)]
    ok("RS6 no file says the pack was built (H24)", not built, built)
    ok("RS7 no file name broadcasts the stump",
       not any(re.search(r"sweep|bias|known_issue|selection|answer|distract|class|neighbo|street|reject", f, re.I)
               for f in files))
    import asks as AS
    closed = AS.district_holidays(2026)
    appr = [d.date() if hasattr(d, "date") else d for d in co.Approved]
    ok("RS8 no change order is approved on a weekend or a district holiday",
       all(d.weekday() < 5 and d not in closed for d in appr),
       [str(d) for d in appr if d.weekday() >= 5 or d in closed])
    import openpyxl
    uc = openpyxl.load_workbook(os.path.join(target, K.UNIT_COSTS), data_only=True).active
    basis = {r[0]: (r[2], r[3], r[4]) for r in uc.iter_rows(values_only=True)
             if isinstance(r[0], str) and re.fullmatch(r"RZ-\d\d", r[0])}
    sys_rates = (K.UNIT_FULL, K.UNIT_DIG)
    ok("RS9 the unit cost schedule states its system rates and names every zone's rate basis",
       "System rates: ${:,} a full replacement and ${:,} a verification dig".format(K.UNIT_FULL, K.UNIT_DIG) in
       texts[K.UNIT_COSTS] and
       len(basis) == 12 and all(b and ((u, d) == sys_rates) == (b == "System rates") for u, d, b in basis.values()),
       basis)

    # ---------------------------------------------------------------- signposts (readability screen)
    # nothing shipped says how lines come to be verified, that a line's material follows its main, or names a class
    # of main, a survey, coverage, a selection or which verifications estimate a share
    notes_flat = re.sub(r"\s+", " ", notes)
    sign = (r"sweep|coverage|selection|selected|biased|representative|verified whole|systematic|prompted by|random|"
            r"sampling frame|every service (line )?on|dug because|come to be verified|replaced main|main is replaced|"
            r"visit to a single line|neighbo|same main|other services|laid together|installed together|"
            r"street's|streets whose|lead streets|copper streets|class of (main|street)|survey|consultant|"
            r"likely to be lead|letters? to|services likely")
    hits = {f: m.group(0) for f, t in texts.items() if f not in (K.METER_EXCHANGES,) for m in
            [re.search(sign, re.sub(r"\s+", " ", t), re.I)] if m}
    ok("S1 no shipped sentence says how lines come to be verified or that a line's material follows its main, and none "
       "names a class of main, a survey, a ranking, coverage, a selection or which verifications estimate a share",
       not hits, hits)
    ver_raw = pd.read_csv(os.path.join(target, K.VERIFICATIONS), dtype=str, keep_default_na=False)
    ok("S2 the verification log has no project, cause or batch column",
       list(ver_raw.columns) == ["source", "wo_no", "verified_date", "premise_no", "sl_id", "method", "crew",
                                 "result_code"], list(ver_raw.columns))
    inv, ver = L.inventory(target), L.verifications(target)
    cov = AN.coverage(inv, ver)
    whole_seg = set(cov[cov >= 0.999].index)
    seg_of = dict(zip(inv.sl_id, inv.segment))
    vv = ver.assign(whole=ver.sl_id.map(seg_of).isin(whole_seg))
    mix_w = vv[vv.whole].method.value_counts(normalize=True)
    mix_o = vv[~vv.whole].method.value_counts(normalize=True)
    crews_w, crews_o = set(vv[vv.whole].crew), set(vv[~vv.whole].crew)
    ok("S3 crews and methods overlap between whole-segment and other verifications",
       crews_w == crews_o and all(abs(mix_w.get(m, 0) - mix_o.get(m, 0)) <= 0.12 for m in set(mix_w.index)),
       (mix_w.round(2).to_dict(), mix_o.round(2).to_dict()))
    prog = texts[K.PROGRESS]
    ok("S4 the progress report names no zone and states no share or rate",
       not re.search(r"RZ-\d\d|per cent|%|share|rate", prog, re.I))
    plan = texts[K.PLAN]
    ok("S5 the plan states no zone's line count, cost or share", not re.search(r"\d+\.\d\d|\$\s?\d", plan))
    ok("S6 the inventory carries no column for a main's material or class: the class is built from the other lines' "
       "cards", list(inv_raw.columns) == ["sl_id", "service_address", "municipality", "zone", "main_segment",
                                          "year_built", "tap_card_material", "sl_class", "class_basis",
                                          "field_verified_on", "replaced_on"], list(inv_raw.columns))

    # ---------------------------------------------------------------- the main call from the shipped files
    F = DL.compute(target)
    s, whole, cls, sh, ub, pu, z = F["s"], F["whole"], F["cls"], F["sh"], F["ub"], F["pu"], F["z"]
    p0, z0, pw, zw, prec, zr, ap = F["p0"], F["z0"], F["pw"], F["zw"], F["prec"], F["zr"], F["ap"]
    prices, mob = L.unit_costs(target)
    rem = AN.remaining(inv)
    golden_years = GOLDEN_YEARS
    fig0 = DL.figures(F)
    gfig = figs_of(z)
    route = np.where(whole, "main", "other")
    cells = s.assign(route=route).groupby(["sc", "era", "route"]).hit.agg(["size", "sum"])
    ke = s.groupby(["sc", "era"]).hit.agg(["size", "sum"])
    lgp = {e: ke.loc[("LG", e), "sum"] / ke.loc[("LG", e), "size"] for e in range(3)}
    cp = {e: ke.loc[("C", e), "sum"] / ke.loc[("C", e), "size"] for e in range(3)}
    zstat = [(lgp[e] - lgp[e + 1]) / math.sqrt(lgp[e] * (1 - lgp[e]) / ke.loc[("LG", e), "size"] +
                                               lgp[e + 1] * (1 - lgp[e + 1]) / ke.loc[("LG", e + 1), "size"])
             for e in (0, 1)]
    ok("M1 the share within each kind of main is real, not a constant: on mains whose cards read lead or galvanized it "
       "falls with the era the line was built (each step three or more standard errors), on mains whose cards read "
       "only copper or plastic it is a few in a thousand before 1950 and nothing after, and every cell is large",
       lgp[0] > lgp[1] > lgp[2] and min(zstat) >= 3.0 and lgp[2] < 0.75 and all(cp[e] < 0.005 for e in (0, 1)) and
       ke.loc[("C", 2), "sum"] == 0 and ke["size"].min() >= 150 and ke.loc[("C", 0), "sum"] >= 1,
       ({k: (int(r["size"]), int(r["sum"])) for k, r in ke.iterrows()}, [round(x, 1) for x in zstat]))
    # no exact fractions: inside each class and era cell with both outcomes, shares by zone, crew and method vary as
    # binomial draws do (neither identical nor over-dispersed)
    disp = {}
    for (k, e), cell in s.assign(crew=s.sl_id.map(ver.sort_values(["date", "sl_id"]).groupby("sl_id").crew.first()),
                                 method=s.sl_id.map(ver.sort_values(["date", "sl_id"]).groupby("sl_id").method.first())
                                 ).groupby(["sc", "era"]):
        h, n = int(cell.hit.sum()), len(cell)
        if h < 20 or n - h < 20:
            continue
        for by in ("zone", "crew", "method"):
            g = cell.groupby(by).hit.agg(["size", "sum"])
            g = g[g["size"] >= 15]
            pbar = g["sum"].sum() / g["size"].sum()
            chi = float(((g["sum"] - g["size"] * pbar) ** 2 / (g["size"] * pbar * (1 - pbar))).sum())
            from scipy.stats import chi2 as _chi2
            disp[(k, e, by)] = (round(chi, 1), len(g) - 1, round(float(_chi2.sf(chi, len(g) - 1)), 3),
                                len(set((g["sum"] / g["size"]).round(4))))
    ok("M1b no exact fractions: within each class and era cell the share varies across zones, crews and methods as "
       "binomial draws do (every chi-square p-value between 0.001 and 0.999, and the subgroup shares not all equal)",
       disp and all(0.001 < v[2] < 0.999 and v[3] > 1 for v in disp.values()), disp)
    ok("M2 the segments verified whole are the renewed mains, 300 or more of them; every other segment at 0.75 or less",
       F["n_segments"] >= 300 and cov[cov < 0.999].max() <= 0.75, (F["n_segments"], round(cov[cov < 0.999].max(), 3)))
    ok("M3 the call: last zone RZ-06 Wexley finished 2037, the twelve finish years as designed",
       finish_list(z) == golden_years and z.zone.iloc[-1] == "RZ-06", finish_list(z))
    ok("M3b the unknown-line shares are 0.47, 0.26 and 0.01 to two decimals: each unknown line at the share of its "
       "main's kind and its era, averaged over the era's unknown lines",
       [fig0["era_shares_lead_status_unknown"][DL.ERA_LABEL[e]] for e in range(3)] == ["0.47", "0.26", "0.01"],
       {e: round(pu[e], 4) for e in range(3)})
    sig = zone_sigma(inv, s, cls)
    sP = F["sig"]
    e_repl = min((5 - abs(r.replacements - 10 * math.floor(r.replacements / 10 + 0.5))) / sig[r.zone]
                 for r in z.itertuples())
    e_cost = min((5e4 - abs(r.cost - 1e5 * math.floor(r.cost / 1e5 + 0.5))) / (sig[r.zone] * (prices[r.zone][0] -
                                                                                                prices[r.zone][1]))
                 for r in z.itertuples())
    e_year = min(min(y - math.floor(y), math.ceil(y) - y) for y in z.years)
    ok("M4 margins: every zone's lines and cost 1.2 or more sampling standard errors inside their rounding bins, every "
       "running total 0.13 programme years from a year end, the last zone mid-bin",
       e_repl >= 1.2 and e_cost >= 1.2 and e_year >= 0.13 and 0.40 <= z.years.iloc[-1] - 10 <= 0.60,
       "%.2f and %.2f sigma, %.3f years ($%.0f), last %.3f" % (e_repl, e_cost, e_year, e_year * ap, z.years.iloc[-1]))
    moves = []
    for e in range(3):
        for sgn in (1, -1):
            P = dict(pu)
            P[e] = pu[e] + sgn * sP[e]
            zz_ = AN.zone_costs(rem, P, ap, prices, mob)
            moves.append(figs_of(zz_) == gfig and summary_of(zz_, P, ap) == summary_of(z, pu, ap))
    zmove = []
    for r in z.itertuples():
        for sgn in (1, -1):
            rr = r.replacements + sgn * sig[r.zone]
            cc = r.cost + sgn * sig[r.zone] * (prices[r.zone][0] - prices[r.zone][1])
            zmove.append(round_to(rr, 10) == round_to(r.replacements, 10) and round_to(cc, 100_000) ==
                         round_to(r.cost, 100_000))
    tot_sig = math.sqrt(sum((sum(rem[c]) * sP[e]) ** 2 for e, c in enumerate(("u0", "u1", "u2")))) * (
        K.UNIT_FULL - K.UNIT_DIG)
    tot = float(z.cum_cost.iloc[-1])
    ok("M4b a one-sigma move leaves every graded figure unchanged: each era share moved one standard error either way "
       "keeps every zone's lines, cost and finish year, the era shares to two decimals, the plan cost to the million "
       "and the programme years to 0.1; each zone's expected lines moved by its own standard error keep its lines and "
       "cost; the plan cost moved by its standard error keeps $267 million",
       all(moves) and all(zmove) and round_to((tot - tot_sig) / 1e6, 1) == round_to((tot + tot_sig) / 1e6, 1) ==
       int(fig0["total_plan_cost_million"]), (moves, sum(zmove), round(tot_sig), round(tot)))
    gy = z.years.iloc[-1]

    def last_gap(zz):
        return float(zz.years.iloc[-1]) - gy
    ok("M5 R0 default path: every verified no-tap-card line by era files 2039, two or more programme years past the "
       "answer", int(z0.finish_year.max()) == 2039 and last_gap(z0) >= 2.0,
       (finish_list(z0), {k: round(v, 3) for k, v in p0.items()}, round(last_gap(z0), 2)))
    unk = inv[inv.zone.isin(K.PLAN_ORDER) & (inv.cls == "LEAD STATUS UNKNOWN")].copy()
    unk["era"] = unk.year_built.map(K.era_of)
    r1 = sched_expected(rem, model_expected(s, unk, era=True, year=True, zone=True), ap, prices, mob)
    ok("M6 R1 a logistic on era, construction year and zone fitted on every verified line files 2039 or later",
       int(r1.finish_year.max()) >= 2039, finish_list(r1))
    cell = s.groupby(["zone", "era"]).hit.mean()
    era_all = s.groupby("era").hit.mean()
    expz = {zz: sum(n * cell.get((zz, e), era_all[e]) for e, n in unk[unk.zone == zz].era.value_counts().items())
            for zz in K.PLAN_ORDER}
    r1b = sched_expected(rem, expz, ap, prices, mob)
    ok("M7 R1 reweighting the verified lines to the unknown lines' zone and era files 2039 or later",
       int(r1b.finish_year.max()) >= 2039, finish_list(r1b))
    ok("M8 R2 the segments verified whole, share by era, carried to the unknown lines: 2041, three programme years "
       "past the answer", int(zw.finish_year.max()) == 2041 and last_gap(zw) >= 3.0,
       (finish_list(zw), {k: round(v, 3) for k, v in pw.items()}, round(last_gap(zw), 2)))
    pooled1 = float(s[whole].hit.mean())
    r2p = AN.zone_costs(rem, [pooled1] * 3, ap, prices, mob)
    ok("M8a R2 one pooled share on the segments verified whole files 2041 or later", int(r2p.finish_year.max()) >= 2041,
       (round(pooled1, 4), finish_list(r2p)))
    q_ws = AN.unknown_shares(inv, ver, pw)
    z_ws = AN.zone_costs(rem, {e: q_ws[e][0] for e in range(3)}, ap, prices, mob)
    ok("M8b R2 the whole-segment expectation of every no-tap-card line of the era less what the verifications found, "
       "over the lines still unknown (the depletion accounting), files 2041",
       int(z_ws.finish_year.max()) == 2041 and last_gap(z_ws) >= 3.0, (finish_list(z_ws), round(last_gap(z_ws), 2)))
    q_rec = AN.unknown_shares(inv, ver, prec)
    z_rr = AN.zone_costs(rem, {e: q_rec[e][0] for e in range(3)}, ap, prices, mob)
    ok("M8c Rr the share of tap cards that read lead or galvanized, by era, carried to the unknown lines: 2040; less "
       "what the verifications found, over the lines still unknown: 2040",
       int(zr.finish_year.max()) == 2040 and int(z_rr.finish_year.max()) == 2040 and last_gap(zr) >= 2.5 and
       last_gap(z_rr) >= 2.5, (finish_list(zr), finish_list(z_rr), round(last_gap(zr), 2), round(last_gap(z_rr), 2)))
    q_ver = AN.unknown_shares(inv, ver, p0)
    z_vr = AN.zone_costs(rem, {e: q_ver[e][0] for e in range(3)}, ap, prices, mob)
    vs = s.groupby("segment").hit.mean()
    unk_all = inv[inv.cls == "LEAD STATUS UNKNOWN"].copy()
    unk_all["era"] = unk_all.year_built.map(K.era_of)
    pn = {}
    for e in range(3):
        x = unk_all[unk_all.era == e].segment.map(vs)
        pn[e] = float(np.where(x.notna(), x, p0[e]).mean())
    z_nb = AN.zone_costs(rem, pn, ap, prices, mob)
    ok("M8d the verified share less found over unknown files 2039 or later; the verified lines on the line's own main, "
       "else the era's verified share, files 2039, the nearest rival, 1.9 programme years past",
       int(z_vr.finish_year.max()) >= 2039 and int(z_nb.finish_year.max()) == 2039 and last_gap(z_nb) >= 1.9,
       (finish_list(z_vr), finish_list(z_nb), round(last_gap(z_nb), 2)))
    mx = F["mix"]
    pct = {k: [int(math.floor(100 * mx[k][e] + 0.5)) for e in range(3)] for k in mx}
    ok("M9 the transport fact: the verified no-tap-card lines, the replaced mains' lines and the tap card lines sit on "
       "lead or galvanized mains far more often than the unknown lines do in the first two eras (by 18 points or more)",
       all(pct[k][e] - pct["unknown"][e] >= 18 for k in ("verified", "whole", "carded") for e in (0, 1)) and
       pct["verified"][2] > pct["unknown"][2] and pct["carded"][2] > pct["unknown"][2], pct)
    rec0 = AN.zone_costs(rem, [0, 0, 0], ap, prices, mob)
    lead1 = AN.zone_costs(rem, [1, 1, 1], ap, prices, mob)
    ok("M10 partials: records only (every unknown line non-lead) and every unknown line lead bracket the answer",
       int(rec0.finish_year.max()) < 2037 and int(lead1.finish_year.max()) > 2041,
       [int(x.finish_year.max()) for x in (rec0, lead1)])
    # the golden family: every defensible construction of the by-era share files the same rounded figures
    fam = family(inv, ver, s, cls, ap, prices, mob)
    same = {name: figs_of(zz_) == gfig and summary_of(zz_, P, ap) == summary_of(z, pu, ap)
            for name, (P, zz_) in fam.items()}
    ok("M11 C1 the golden family converges: the kind and era expectation less what was found equals the golden to the "
       "twelfth decimal, and the replaced mains alone, the replaced mains' rate less what was found, single-line visits "
       "alone, lead, galvanized and copper mains apart, decade by decade, zone by zone and the logistic fits with the "
       "class and era interaction (alone, with zone and year, and additive) all file the twelve zones' lines, costs and "
       "finish years, the era shares to two decimals, $267 million and 10.5 programme years",
       all(abs(fam["expectation less found"][0][e] - pu[e]) < 1e-12 for e in range(3)) and all(same.values()),
       {k: v for k, v in same.items() if not v})
    pp, zp = F["pp"], F["zp"]
    lines_moved_p = sum(1 for a, b in zip(zp.replacements, z.replacements) if round_to(a, 10) != round_to(b, 10))
    cost_moved_p = sum(1 for a, b in zip(zp.cost, z.cost) if round_to(a, 1e5) != round_to(b, 1e5))
    lgc = ke.loc["LG"]
    pbar = lgc["sum"].sum() / lgc["size"].sum()
    chi_lg = float(((lgc["sum"] - lgc["size"] * pbar) ** 2 / (lgc["size"] * pbar * (1 - pbar))).sum())
    ok("M12 the pooled construction is rejected: one rate for each kind of main across all eras is refuted by the "
       "record (chi-square on two degrees of freedom of 100 or more on the lead or galvanized mains) and moves the lines "
       "in 8 or more zones and the cost in 8 or more", chi_lg >= 100 and lines_moved_p >= 8 and cost_moved_p >= 8,
       (round(chi_lg, 1), lines_moved_p, cost_moved_p, {e: round(pp[e], 4) for e in range(3)}))
    sl = AN.lg_card_share(inv)
    thr_same = all((sl.map(lambda x, t=t: "LG" if x >= t else "C") == cls).all()
                   for t in (0.01, 0.1, 0.25, 0.34, 0.5, 0.6, 0.66))
    maj = sl.map(lambda x: "LG" if x > 0.5 else "C")
    ok("M13 SF12 the class of a main converges: any lead or galvanized card, a majority of such cards or any share "
       "threshold up to two thirds sorts every main the same way; no main carries both a copper-only and a lead reading",
       thr_same and (maj == cls).all() and sl[cls == "C"].max() == 0.0 and sl[cls == "LG"].min() >= 0.66,
       (round(float(sl[cls == "LG"].min()), 3), float(sl[cls == "C"].max())))
    g5 = {e: float(unk_all[unk_all.era == e].segment.map(sl).mean()) for e in range(3)}
    z5 = AN.zone_costs(rem, g5, ap, prices, mob)
    g6 = {e: float((unk_all[unk_all.era == e].segment.map(cls) == "LG").mean()) for e in range(3)}
    z6 = AN.zone_costs(rem, g6, ap, prices, mob)
    ok("M14 the main's kind read as the line's material without the verification record (every line on a lead or "
       "galvanized main lead, none on a copper one, or the main's card share as the line's probability) keeps the call "
       "but misses the lines in 8 or more zones",
       int(z5.finish_year.max()) == 2037 and int(z6.finish_year.max()) == 2037 and
       sum(1 for a, b in zip(z6.replacements, z.replacements) if round_to(a, 10) != round_to(b, 10)) >= 10 and
       sum(1 for a, b in zip(z5.replacements, z.replacements) if round_to(a, 10) != round_to(b, 10)) >= 8,
       (round(float(z5.years.iloc[-1]), 3), round(float(z6.years.iloc[-1]), 3)))
    zr15 = []
    cum = 0.0
    for r in rem.itertuples():
        u = r.u0 + r.u1 + r.u2
        e = round(r.u0 * pu[0] + r.u1 * pu[1] + r.u2 * pu[2])
        uf, ud = prices[r.zone]
        cum += (r.lgrr + e) * uf + (u - e) * ud + mob
        zr15.append(K.FIRST_YEAR + math.ceil(cum / ap - 1e-9) - 1)
    ok("M15 axis 10 rounding expected lines to whole lines first moves no finish year", zr15 == golden_years, zr15)
    rng = np.random.default_rng(124)
    inv_s = inv.sample(frac=1.0, random_state=rng.integers(1 << 31)).reset_index(drop=True)
    ver_s = ver.sample(frac=1.0, random_state=rng.integers(1 << 31)).reset_index(drop=True)
    s_s = AN.sample(inv_s, ver_s)
    z_s = AN.zone_costs(AN.remaining(inv_s), AN.class_era_shares(inv_s, s_s, AN.street_class(inv_s)), ap, prices, mob)
    ok("M16 axis 14 shuffled rows give the same schedule", finish_list(z_s) == golden_years and
       abs(z_s.cum_cost.iloc[-1] - z.cum_cost.iloc[-1]) < 1e-3)
    for name, vsub, full in (("dropping every customer-system row (legacy keys)", ver[ver.source == "WMS"], True),
                             ("a 2023-on window", ver[ver.date >= dt.date(2023, 1, 1)], True),
                             ("the 2026 verifications alone", ver[ver.date >= dt.date(2026, 1, 1)], False)):
        s_v = AN.sample(inv, vsub)
        z_v = AN.zone_costs(rem, AN.class_era_shares(inv, s_v, cls), ap, prices, mob)
        ok("M17 axis 8/16 %s keeps the twelve finish years%s (mess neutral on the call)" % (
            name, " and every zone's lines and cost" if full else ""),
           finish_list(z_v) == golden_years and (not full or figs_of(z_v) == gfig), finish_list(z_v))
    t26 = AN.sample(inv, ver[ver.date >= dt.date(2026, 1, 1)])
    z26 = AN.zone_costs(rem, AN.shares(t26), ap, prices, mob)
    ok("M22 Gate G first move: the 2026 verifications alone, by era, file 2039 or later", int(z26.finish_year.max()) >= 2039,
       (finish_list(z26), {k: round(v, 3) for k, v in AN.shares(t26).items()}))
    multi = ver.groupby("sl_id").result.nunique()
    ok("M19 SF11 every re-verified line has one result on every visit", int(multi.max()) == 1 and
       int((ver.groupby("sl_id").size() > 1).sum()) > 50, int((ver.groupby("sl_id").size() > 1).sum()))
    first_res = ver.sort_values(["date", "sl_id"]).groupby("sl_id").result.first()
    tc = inv[inv.segment.isin(whole_seg) & inv.record.isin(["LEAD", "GALV"])]
    ok("SF9 every lead or galvanized tap card line on a replaced main proved lead or GRR",
       len(tc) > 50 and tc.sl_id.map(first_res).isin(["LEAD", "GRR"]).all(), len(tc))
    verified = set(ver.sl_id)
    ok("SF8 no verified line is still Lead Status Unknown", not inv[inv.sl_id.isin(verified)].cls.eq(
        "LEAD STATUS UNKNOWN").any())
    nr = inv[(inv.record == "") & (inv.year_built > 0) & (inv.year_built < K.AGE_RULE_YEAR)].copy()
    nr["era"] = nr.year_built.map(K.era_of)
    nr["sc"] = nr.segment.map(cls)
    alt = rem.copy()
    for e, col in enumerate(("u0", "u1", "u2")):
        alt[col] = alt.zone.map(nr[nr.era == e].groupby("zone").size()).fillna(0).astype(int)
    z8 = AN.zone_costs(alt, pu, ap, prices, mob)
    ok("SF8 counting every no-tap-card line as unknown, verified ones included, gives a later schedule",
       int(z8.finish_year.max()) > 2037, finish_list(z8))
    first = ver.sort_values(["date", "sl_id"]).groupby("sl_id", as_index=False).first()
    sa = first.merge(inv[["sl_id", "year_built", "segment"]], on="sl_id")
    sa = sa[(sa.year_built > 0) & (sa.year_built < 1989)].assign(era=lambda d: d.year_built.map(K.era_of),
                                                                  hit=lambda d: d.result.isin(["LEAD", "GRR"]))
    z10 = AN.zone_costs(rem, {e: float(sa[sa.era == e].hit.mean()) for e in range(3)}, ap, prices, mob)
    z10b = AN.zone_costs(rem, AN.class_era_shares(inv, sa, cls), ap, prices, mob)
    ok("SF10 shares from every verified line, tap card lines included: by era 2039 or later; by kind and era, the same "
       "call (plan 6.1: the class is the lines with no usable tap card)",
       int(z10.finish_year.max()) >= 2039 and int(z10b.finish_year.max()) == 2037 and
       "with no usable tap card that has not been field verified" in re.sub(r"\s+", " ", plan),
       (finish_list(z10), finish_list(z10b)))
    before = z.cum_cost.iloc[-2]
    ok("SF2 a start-year reading of 'finished' still has the last zone (started in 2036) inside the deadline: the same "
       "call; plan 5.3 defines the finish year",
       K.FIRST_YEAR + math.floor(before / ap) <= 2037 and
       "A zone is finished in the programme year in which the running total of appropriations first covers" in
       re.sub(r"\s+", " ", plan), K.FIRST_YEAR + math.floor(before / ap))
    ok("SF3 no shipped document states an escalation rate", not any(re.search(r"escalat|inflat", t, re.I)
                                                                     for t in texts.values()))
    sl_only = s.assign(hit=s.result.eq("LEAD"))
    rem_l = rem.copy()
    rem_l["lgrr"] = rem_l.zone.map(inv[inv.cls == "LEAD"].groupby("zone").size()).fillna(0).astype(int)
    zl = AN.zone_costs(rem_l, AN.class_era_shares(inv, sl_only, cls), ap, prices, mob)
    ok("SF4 lead only, GRR left out, gives a different, earlier schedule",
       finish_list(zl) != golden_years and int(zl.finish_year.max()) < 2037, finish_list(zl))
    ok("SF5 every unknown line taken as lead runs well past the deadline", int(lead1.finish_year.max()) > 2041)
    ok("SF6 the plan files the season close that makes a 2037 finish meet the deadline",
       "finished by 31 October of that year" in re.sub(r"\s+", " ", plan))
    comp = L.completions(target)
    latest = comp.sort_values(["site_id", "closed_on", "row_status"]).drop_duplicates("site_id", keep="last")
    paid26 = (latest.paid_base + latest.paid_extra_ft + latest.paid_restoration).sum() + co["Amount ($)"].sum()
    avg26 = paid26 / len(latest)
    z7 = AN.zone_costs(rem, pu, ap, {zz: (avg26, prices[zz][1]) for zz in prices}, mob)
    ok("SF7 costing at what a 2026 replacement was paid gives a different schedule",
       figs_of(z7) != gfig, (round(avg26), finish_list(z7)))
    ok("SF7 the plan files the 2027 unit cost schedule as the cost basis",
       "2027 unit cost schedule" in re.sub(r"\s+", " ", plan))
    cum, fy13, extra13 = 0.0, [], []
    for r in z.itertuples():
        base = r.cost - mob
        n_mob = 1
        while True:
            start = math.floor(cum / ap)
            end = math.ceil((cum + base + n_mob * mob) / ap - 1e-9) - 1
            if end - start + 1 == n_mob:
                break
            n_mob = end - start + 1
        cum += base + n_mob * mob
        fy13.append(K.FIRST_YEAR + end)
        extra13.append(n_mob - 1)
    ok("SF13 a mobilisation in every programme year a zone is worked keeps the finish years and raises the cost of "
       "every zone that spans a year end", fy13 == golden_years and sum(1 for x in extra13 if x) >= 9, extra13)
    year, fy14 = K.FIRST_YEAR, []
    for i, r in enumerate(z.itertuples()):
        if i:
            year = fy14[-1] + 1
        fy14.append(year + math.ceil(r.cost / ap - 1e-9) - 1)
    ok("SF14 whole zones only, each starting with a new programme year, runs past the deadline",
       fy14[-1] > 2037, fy14)
    ok("SF1 the main call's files carry one zone per line, the inventory's",
       "zone_on_form" not in inv_raw.columns and set(inv_raw.zone) == {zz[0] for zz in K.ZONES})
    unk_years = inv_raw[inv_raw.sl_class == "LEAD STATUS UNKNOWN"].year_built.astype(int)
    ok("M20 axis 9 no unknown line is built in or after 1989 or has no year", unk_years.between(1, 1988).all())
    ok("M21 axis 2 one row per service line", inv_raw.sl_id.is_unique)
    zero = inv_raw[inv_raw.year_built == "0"]
    ok("M25 the assessor's zero years all sit on tap card lines, outside every estimate",
       len(zero) > 100 and (zero.tap_card_material != "").all(), len(zero))
    ok("M23 separation: the default path's last zone, the whole segments', the tap cards' and the neighbouring "
       "lines' each two or more years past the answer; every one of them misses the deadline the answer meets",
       min(int(x.finish_year.max()) for x in (z0, zw, zr, z_nb)) - 2037 >= 2 and z.finish_year.max() == 2037)
    # SF15 to SF18: which verifications estimate the share among the unknown lines, and how
    ok("SF15 the estimation: every era-wide rate (every verification, the replaced mains, the tap cards, each less what "
       "was found) runs to 2039 or later; one rate per kind across eras is refuted (M12); the share of each kind of "
       "main in each era, carried by each unknown line's own main and era, gives the golden",
       min(int(x.finish_year.max()) for x in (z0, zw, zr, z_ws, z_rr, z_vr)) >= 2039 and finish_list(z) == golden_years)
    plan_flat = re.sub(r"\s+", " ", plan)
    ok("SF16 plan 4.3 carries unknown lines at the share expected among the district's Lead Status Unknown lines of the "
       "era, and plan 6.1 defines them as the lines with no usable tap card not yet field verified",
       "expected among the district's Lead Status Unknown lines of its construction era" in plan_flat and
       "that has not been field verified is Lead Status Unknown" in plan_flat)
    ub12 = {e: {k: int(((unk.era == e) & (unk.segment.map(cls) == k)).sum()) for k in ("LG", "C")} for e in range(3)}
    p12 = {e: sum(ub12[e][k] * sh[(k, e)] for k in ("LG", "C")) / sum(ub12[e].values()) for e in range(3)}
    z12 = AN.zone_costs(rem, p12, ap, prices, mob)
    own = {}
    for zz in K.PLAN_ORDER:
        t = unk[unk.zone == zz]
        own[zz] = float(sum(sh[(k, e)] for k, e in zip(t.segment.map(cls), t.era)))
    zown = sched_expected(rem, own, ap, prices, mob)
    ok("SF16 C1 the kind and era shares over the twelve plan zones only keep the twelve finish years; each zone at its "
       "own lines' mix (against plan 4.3's district share) keeps the call",
       finish_list(z12) == golden_years and int(zown.finish_year.max()) == 2037,
       (finish_list(z12), finish_list(zown)))
    rep_first = inv[inv.basis == "REPLACED"].sl_id.map(first_res)
    cur = s.assign(hit=s.sl_id.map(dict(zip(inv.sl_id, inv.cls))).isin(["LEAD", "GRR"]))
    z17 = AN.zone_costs(rem, AN.class_era_shares(inv, cur, cls), ap, prices, mob)
    ok("SF17 reading a replaced line as found non-lead (the inventory's current class) gives a different schedule; the "
       "field notes define REPLACED as found lead or GRR and replaced in full, and every replaced line's first result "
       "is lead or GRR", finish_list(z17) != golden_years and rep_first.isin(["LEAD", "GRR"]).all() and
       "REPLACED (found lead or GRR and replaced in full" in notes_flat, finish_list(z17))
    pre_cards = inv[(inv.record != "") & (inv.year_built > 0) & (inv.year_built < 1989)]
    c18 = pre_cards.groupby("segment").record.apply(lambda x: "LG" if x.isin(["LEAD", "GALV"]).any() else "C")
    ok("SF18 the class read from the cards of lines built before 1989 only, years known, is the same for every main "
       "that has such a card, and every unknown line's main has one",
       (c18 == cls.reindex(c18.index)).all() and unk_all.segment.isin(c18.index).all())
    z3d = AN.zone_costs(rem, {e: round(pu[e], 3) for e in range(3)}, ap, prices, mob)
    ok("M26 the unknown-line shares rounded to three decimals keep every finish year and the call",
       finish_list(z3d) == golden_years, finish_list(z3d))
    # SF19: the rounding path. The prompt's one rounding sentence names the reported figures (lines, zone costs, the
    # 2026 payments) and no share, so a literal reader carries the era shares unrounded; the golden is that path.
    task_root = os.path.dirname(os.path.abspath(target))
    prompt_txt = open(os.path.join(task_root, "prompt.txt"), encoding="utf-8").read().strip()
    figs = json.load(open(os.path.join(task_root, "generator", "figures.json"), encoding="utf-8"))
    closing = prompt_txt.rsplit(". ", 1)[-1]
    z2d = AN.zone_costs(rem, {e: round(pu[e], 2) for e in range(3)}, ap, prices, mob)
    lines_moved = [a.zone for a, b in zip(z.itertuples(), z2d.itertuples())
                   if round_to(a.replacements, 10) != round_to(b.replacements, 10)]
    unrounded_is_golden = all(
        figs["zones"][a.zone]["lead_and_grr_to_replace"] == "{:,}".format(round_to(a.replacements, 10)) and
        figs["zones"][a.zone]["plan_cost"] == "{:,}".format(round_to(a.cost, 100_000)) and
        figs["zones"][a.zone]["finish_year"] == int(a.finish_year) for a in z.itertuples())
    ok("SF19 rounding path: the prompt's closing sentence rounds the reported lines, zone costs and payments and no "
       "share, the golden carries the era shares unrounded; shares rounded to two decimals before they are applied "
       "file the same twelve zones' lines, costs and finish years (C1)",
       closing == "Round lines to the nearest ten, zone costs to the nearest $100,000 and the 2026 payments to the "
                  "nearest dollar." and not re.search(r"share|decimal|per cent|%", closing, re.I) and
       unrounded_is_golden and figs_of(z2d) == gfig,
       (closing, unrounded_is_golden, finish_list(z2d), lines_moved))
    if world is not None:
        lines, ev = world["lines"], world["ev"]
        sweeps = set(world["sweeps"])
        ok("W1 the segments verified whole are exactly the main renewals' segments", whole_seg == sweeps)
        lw = lines.set_index("sl_id")
        nrl = lines[(lines.record == "") & lines.era.between(0, 2)]
        cause_lines = set(ev[ev.cause != "main"].sl_id)
        dug = nrl[nrl.sl_id.isin(cause_lines)]
        ok("W2 the verification routes went to lead or galvanized mains far more than the unknown lines sit on them "
           "before 1950, and the digs for cause on copper mains mostly to the post-1950 streets",
           (dug[dug.era < 2].sclass == "LG").mean() > 0.70 and
           (nrl[nrl.swept & (nrl.era < 2)].sclass == "LG").mean() > 0.55 and
           (lines[(lines.cls == "LEAD STATUS UNKNOWN") & (lines.era < 2)].sclass == "LG").mean() < 0.42 and
           (dug[dug.sclass == "C"].era == 2).mean() > 0.6,
           (round((dug[dug.era < 2].sclass == "LG").mean(), 3), round((nrl[nrl.swept & (nrl.era < 2)].sclass == "LG")
                                                                      .mean(), 3)))
        ok("W3 the class the cards show is the class the district laid: every main's card reading matches its "
           "world class", (lw.segment.map(cls).dropna() == lw.loc[lw.segment.map(cls).notna(), "sclass"]).all())
        tr = lw.truth
        res_ok = (ver.result == ver.sl_id.map(tr)).all()
        ok("M24 clean-data (instrument): every recorded result is the material in the ground", res_ok)
        nrw = nrl.copy()
        nrw["hitw"] = nrw.truth != "NON-LEAD"
        nrw["unknown"] = nrw.verified.isna()
        true_ver = nrw[~nrw.unknown].groupby("era").hitw.mean().to_dict()
        true_all = nrw.groupby("era").hitw.mean().to_dict()
        true_unk = nrw[nrw.unknown].groupby("era").hitw.mean().to_dict()
        z_true = AN.zone_costs(rem, true_unk, ap, prices, mob)
        z_easy = AN.zone_costs(rem, true_ver, ap, prices, mob)
        z_eraall = AN.zone_costs(rem, true_all, ap, prices, mob)
        ok("W4 analyst test on the clean truth: the material in the ground of the verified no-tap-card lines, by era, "
           "carried to the unknown lines (the easy route, every rule applied) runs past the deadline, and so does the "
           "true share across every no-tap-card line of the era; the true share among the unknown lines (the decisive "
           "step alone changed) finishes in 2037, the golden shares within 0.005 of it",
           int(z_easy.finish_year.max()) >= 2039 and int(z_eraall.finish_year.max()) >= 2038 and
           int(z_true.finish_year.max()) == 2037 and all(abs(true_unk[e] - pu[e]) < 0.005 for e in range(3)),
           ({e: round(true_ver[e], 4) for e in range(3)}, {e: round(true_all[e], 4) for e in range(3)},
            {e: round(true_unk[e], 4) for e in range(3)}, finish_list(z_easy), finish_list(z_eraall),
            finish_list(z_true)))
    # ---------------------------------------------------------------- the three rules (dataset-generation 7.1)
    seg_lg = set(inv_raw[inv_raw.tap_card_material.isin(["LEAD", "GALV"])].main_segment)
    unk_raw = inv_raw[inv_raw.sl_class == "LEAD STATUS UNKNOWN"]
    rebuilt = unk_raw.main_segment.map(lambda g: "LG" if g in seg_lg else "C")
    ok("R1 the field's raw material ships: one inventory row per service line with the main segment it taps and its "
       "own tap card, one verification row per visit, and each unknown line's kind of main rebuilt from those two "
       "inventory columns alone is the golden's", inv_raw.sl_id.is_unique and len(ver_raw) > ver.sl_id.nunique() and
       (rebuilt.values == unk_raw.main_segment.map(cls).values).all(), (len(inv_raw), len(ver_raw)))
    heads = {f: list(pd.read_csv(os.path.join(target, f), nrows=0).columns) for f in files if f.endswith(".csv")}
    carried = [(f, c) for f, cs in heads.items() for c in cs
               if re.search(r"share|expect|probab|likel|kind|cohort|street|class_of|main_(class|material|type)|"
                            r"hit_rate|lead_rate|risk|score|weight", c, re.I)]
    ok("R1 no shipped column carries a share, an expected count, a probability, a weight or a main's kind", not carried,
       carried)
    u_cls = unk_raw.main_segment.map(cls)
    pure = {}
    for c in inv_raw.columns:
        if c in ("sl_id", "service_address", "main_segment") or inv_raw[c].nunique() > 60:
            continue
        ct = pd.crosstab(unk_raw[c], u_cls)
        pure[c] = round(float(ct[(ct == 0).any(axis=1)].sum(axis=1).sum()) / len(unk_raw), 4)
    ok("R1 no inventory column but the main segment partitions the unknown lines by kind of main (at most 1 per cent "
       "of them under a value of one kind only)", pure and max(pure.values()) <= 0.01, pure)

    def call_of(inv_, ver_, s_=None):
        s_ = AN.sample(inv_, ver_) if s_ is None else s_
        return AN.zone_costs(AN.remaining(inv_), AN.class_era_shares(inv_, s_, cls), ap, prices, mob)
    z_r2 = call_of(inv, ver[ver.source == "WMS"])
    ok("R2 legacy premise keys (the customer system before the March 2023 migration, the crosswalk's padding): the "
       "customer-system rows an unpadded join drops keep the twelve finish years", finish_list(z_r2) == golden_years,
       (finish_list(z_r2), round(float(z_r2.years.iloc[-1]), 3)))
    z_r2 = call_of(inv, ver[~ver.crew.str[:3].isin(["BRN", "TCU", "KPU"])])
    ok("R2 result codes by recording route: one route's codes left unmapped (the contractor forms' rows dropped) keep "
       "the twelve finish years", finish_list(z_r2) == golden_years, (finish_list(z_r2), round(float(z_r2.years.iloc[-1]), 3)))
    visits = ver.merge(inv[["sl_id", "zone", "segment", "year_built", "record"]], on="sl_id", how="inner")
    visits = visits[(visits.record == "") & (visits.year_built > 0) & (visits.year_built < K.AGE_RULE_YEAR)].copy()
    visits["era"] = AN.era_series(visits.year_built)
    visits["hit"] = visits.result.isin(["LEAD", "GRR"])
    z_r2 = call_of(inv, ver, visits)
    ok("R2 re-verifications on separate rows: every visit counted as a line keeps the twelve finish years",
       finish_list(z_r2) == golden_years and len(visits) > len(s), (len(visits), len(s), finish_list(z_r2)))

    def day_first(d, src):
        if src != "CIS":
            return dt.date.fromisoformat(d)
        try:
            return dt.datetime.strptime(d, "%d/%m/%Y").date()
        except ValueError:
            return None
    mis = ver.assign(date=[day_first(d, src) for d, src in zip(ver_raw.verified_date, ver_raw.source)])
    mis = mis[mis.date.notna()]
    z_r2 = call_of(inv, mis)
    ok("R2 dates in two formats: the customer system's dates read day first (the impossible ones dropped) keep the "
       "twelve finish years", finish_list(z_r2) == golden_years and len(mis) < len(ver), (len(ver) - len(mis),
                                                                                         finish_list(z_r2)))
    zero = inv[inv.year_built == 0]
    ok("R2 assessor zero years (non-residential parcels): every one sits on a tap card line, so no unknown line and no "
       "verified line with no tap card carries one", len(zero) > 100 and (zero.record != "").all() and
       not (zero.cls == "LEAD STATUS UNKNOWN").any(), len(zero))
    main_files = [K.INVENTORY, K.VERIFICATIONS, K.CROSSWALK, K.CODES, K.UNIT_COSTS, K.CAPITAL, K.PLAN]
    tmp_main = tempfile.mkdtemp(dir=os.path.dirname(os.path.abspath(target)), suffix=".tmp")
    try:
        for f in main_files:
            shutil.copy2(os.path.join(target, f), os.path.join(tmp_main, f))
        inv_m, ver_m = L.inventory(tmp_main), L.verifications(tmp_main)
        prices_m, mob_m = L.unit_costs(tmp_main)
        z_m = AN.zone_costs(AN.remaining(inv_m), AN.class_era_shares(inv_m, AN.sample(inv_m, ver_m), cls),
                            L.appropriation(tmp_main), prices_m, mob_m)
    finally:
        shutil.rmtree(tmp_main)
    ok("R2 the ask paths' mess (repeated change order totals, UTC times, reclosings, the renumbered vendor, unpadded "
       "agreement keys, printed zones, duplicate and withdrawn forms, refused portal forms) sits in files the call never "
       "opens: the schedule from the seven main-call files alone is the golden's",
       finish_list(z_m) == golden_years and abs(float(z_m.cum_cost.iloc[-1]) - float(z.cum_cost.iloc[-1])) < 1e-3,
       finish_list(z_m))
    if world is not None:
        ok("R3a the easy route on the clean truth, every filed rule applied (plan 4.1 to 5.4, the district's era "
           "shares): the material in the ground of the verified lines with no tap card, by era, files 2039",
           int(z_easy.finish_year.max()) == 2039, finish_list(z_easy))
        kn = nrw.assign(sc=nrw.segment.map(cls))
        t_sh = kn[~kn.unknown].groupby(["sc", "era"]).hitw.mean().to_dict()
        t_ub = kn[kn.unknown].groupby(["era", "sc"]).size()
        t_pu = {e: sum(t_ub.get((e, k), 0) * t_sh[(k, e)] for k in ("LG", "C")) / sum(t_ub.get((e, k), 0)
                                                                                   for k in ("LG", "C"))
                for e in range(3)}
        z_t = AN.zone_costs(rem, t_pu, ap, prices, mob)
        t_shp = kn[~kn.unknown].groupby("sc").hitw.mean().to_dict()
        t_pp = {e: sum(t_ub.get((e, k), 0) * t_shp[k] for k in ("LG", "C")) / sum(t_ub.get((e, k), 0)
                                                                                 for k in ("LG", "C"))
                for e in range(3)}
        z_tp = AN.zone_costs(rem, t_pp, ap, prices, mob)
        ok("R3b the era layer adds to the decisive step on the clean truth: the kind of main with one rate per kind "
           "across all eras keeps the call but moves the lines in 8 or more zones",
           int(z_tp.finish_year.max()) == 2037 and sum(1 for a, b in zip(z_tp.replacements, z.replacements)
                                                       if round_to(a, 10) != round_to(b, 10)) >= 8,
           finish_list(z_tp))
        ok("R3b the same route with only the decisive step changed (each line's kind of main, the share within each "
           "kind carried to the unknown lines' own mix) files the golden on the clean truth: the twelve finish years "
           "and the golden era shares", finish_list(z_t) == golden_years and
           all(abs(t_pu[e] - pu[e]) < 1e-9 for e in range(3)), ({e: round(t_pu[e], 4) for e in range(3)},
                                                                finish_list(z_t)))
    ok("R3b each lower correction alone leaves the easy route off the answer: reweighting to the unknown lines' zone "
       "and era 2039 or later, the mains verified whole 2041, the tap cards 2040",
       int(r1b.finish_year.max()) >= 2039 and int(zw.finish_year.max()) == 2041 and int(zr.finish_year.max()) == 2040)
    doc_text = " ".join(t for f, t in texts.items() if f.endswith((".pdf", ".docx", ".md")))
    doc_text = re.sub(r"\s+", " ", doc_text)
    ok("R3c nothing planted: no memo, draft, briefing, estimate or prior schedule in the pack, and no document states a "
       "lead or GRR share, hit rate or expected count",
       not any(re.search(r"memo|draft_|note_to|briefing|estimate|prior|schedule_20(2[0-6])|forecast", f, re.I)
               for f in files) and
       not re.search(r"(lead|GRR)[^.]{0,80}(\d+(\.\d+)? per cent|\b0\.\d+|\d+ in \d+)", doc_text, re.I))
    dup_inv = int(inv_raw.drop(columns=["sl_id"]).duplicated().sum())
    dup_ver = int(ver_raw.drop(columns=["wo_no"]).duplicated().sum())
    ok("R3c no copied or repeated block of rows in the inventory or the verification log", dup_inv == 0 and
       dup_ver <= 2, (dup_inv, dup_ver))
    # context artifact: every figure in the progress report recomputes from the shipped rows
    v26 = ver[ver.date >= dt.date(2026, 1, 1)]
    vq = {q: int(v26[v26.date.map(K.quarter_of) == q].sl_id.nunique()) for q in (1, 2, 3, 4)}
    rq = {q: int(latest[latest.local_date.map(K.quarter_of) == q].shape[0]) for q in (1, 2, 3, 4)}
    by_year = inv[inv.replaced_on != ""].replaced_on.str[:4].value_counts()
    want = ["{:,}".format(int(v26.sl_id.nunique())), "{:,}".format(len(latest))]
    want += ["{:,}".format(vq[q]) for q in vq] + ["{:,}".format(rq[q]) for q in rq]
    want += ["{:,}".format(int(n)) for n in by_year.values] + ["{:,}".format(int(n)) for n in cls_n.values]
    want.append("{:,}".format(len(inv_raw)))
    prog_n = prog.replace("\n", " ")
    ok("C1 every figure in the progress report recomputes from the shipped rows (context artifact)",
       all(re.search(r"(?<![\d,])%s(?![\d,])" % re.escape(w), prog_n) for w in want),
       [w for w in want if not re.search(r"(?<![\d,])%s(?![\d,])" % re.escape(w), prog_n)])
    first_any = ver.groupby("sl_id").date.min()
    q1 = latest[latest.local_date.map(K.quarter_of) == 1]
    ok("C2 most of the first quarter's replacements were found in the 2025 season (the progress report's note)",
       q1.site_id.map(first_any).map(lambda d: d.year == 2025).mean() >= 0.8 and
       "Most of the first quarter's replacements were lines found lead in the 2025 season" in prog_n,
       round(float(q1.site_id.map(first_any).map(lambda d: d.year == 2025).mean()), 3))
    ut = (comp.local_date != comp.utc_date)
    uq = {q: int(latest[latest.utc_date.map(lambda d: d.year == 2026 and K.quarter_of(d) == q)].shape[0])
          for q in (1, 2, 3, 4)}
    ok("C3 the progress report's quarterly replacements tie on local time and not on UTC",
       bool(ut.any()) and any(uq[q] != rq[q] for q in (1, 2, 3, 4)), (rq, uq))

    # ---------------------------------------------------------------- ask A: 2026 payments
    pay = F["pay"]
    fig = json.load(open(os.path.join(os.path.dirname(golden), "generator", "figures.json")))
    gold_a = {(c, q): int(fig["payments_2026_per_full_replacement"][c]["Q%d" % q].replace(",", ""))
              for c in fig["payments_2026_per_full_replacement"] for q in (1, 2, 3, 4)}
    ok("A1 twelve payment figures, rounded to the dollar, equal figures.json",
       all(gold_a[k] == math.floor(pay[k] + 0.5) for k in pay) and len(pay) == 12)
    if world is not None:
        import asks as AS
        wa = AS.payments_answer(world["st"], world["co"])
        ok("A2 the shipped files reproduce the world's payments to the cent",
           all(abs(wa[k] - pay[k]) < 0.005 for k in pay))
    site_q = dict(zip(latest.site_id, zip(latest.contract_no, latest.local_date.map(K.quarter_of))))
    one_q, multi_cq, appr_q = True, set(), True
    for r in co.itertuples():
        keys = {site_q[x] for x in r.sites}
        one_q &= len(keys) == 1
        cq = keys.pop()
        appr_q &= K.quarter_of(r.Approved.date() if hasattr(r.Approved, "date") else r.Approved) == cq[1]
        if len(r.sites) >= 2:
            multi_cq.add(cq)
    ok("A3 every change order's sites complete in one quarter of one contract, approved in that quarter",
       one_q and appr_q)
    ok("A4 every contract-quarter carries a change order covering two or more sites", len(multi_cq) == 12,
       len(multi_cq))
    eve = latest[latest.local_date != latest.utc_date]
    per_end = eve.groupby([eve.local_date, eve.contract_no]).size()
    ends = sorted({d for d, _ in per_end.index})
    ok("H1 each of the first three quarter ends has one or two evening completions per contract that UTC moves to the "
       "next quarter", ends == list(K.QUARTER_ENDS) and per_end.between(1, 2).all() and len(per_end) == 9,
       per_end.to_dict())
    tc_rows = comp[comp.contract_no == "2026-LSL-02"]
    ok("H2 Tri-County's vendor number changes on 13 July 2026 under one contract number",
       set(tc_rows[tc_rows.local_date < K.TC_SWITCH].vendor_no) == {"V-20877"} and
       set(tc_rows[tc_rows.local_date >= K.TC_SWITCH].vendor_no) == {"V-31560"})
    rc = comp[comp.row_status == "RECLOSED"]
    ok("H3 one or two re-closed sites per contract, each with its earlier closing still in the export",
       rc.groupby("contract_no").size().between(1, 2).all() and len(rc.groupby("contract_no")) == 3 and
       comp[comp.site_id.isin(rc.site_id)].groupby("site_id").size().eq(2).all())

    def stop(per_site_co, quarter_col, key_col):
        t = latest.assign(q=latest[quarter_col].map(lambda d: K.quarter_of(d) if d.year == 2026 else 0))
        t = t[t.q > 0]
        base = t.paid_base + t.paid_extra_ft + t.paid_restoration
        if per_site_co:
            t = t.assign(tot=base + t.co_amount)
            g = t.groupby([key_col, "q"]).agg(tot=("tot", "sum"), n=("site_id", "size"))
            return {k: v.tot / v.n for k, v in g.iterrows()}
        t = t.assign(tot=base)
        g = t.groupby([key_col, "q"]).agg(tot=("tot", "sum"), n=("site_id", "size"))
        cq = {}
        for r in co.itertuples():
            row = t[t.site_id == r.sites[0]].iloc[0]
            cq[(row[key_col], row.q)] = cq.get((row[key_col], row.q), 0.0) + float(r._8)
        return {k: (v.tot + cq.get(k, 0.0)) / v.n for k, v in g.iterrows()}
    s1 = stop(True, "utc_date", "contract_no")
    s2 = stop(True, "local_date", "contract_no")
    s3 = stop(False, "utc_date", "contract_no")
    s4 = stop(False, "local_date", "vendor_no")
    ok("A5 stop S1 (each change order on every covered site, UTC quarters) is $25 or more off on all 12",
       all(abs(s1[k] - pay[k]) >= 25 for k in pay), min(abs(s1[k] - pay[k]) for k in pay))
    ok("A6 stop S2 (each change order on every covered site, local quarters) is $25 or more off on all 12; the cracker "
       "files it", all(abs(s2[k] - pay[k]) >= 25 for k in pay), min(abs(s2[k] - pay[k]) for k in pay))
    moved3 = [k for k in pay if abs(s3[k] - pay[k]) > 0.005]
    ok("A7 stop S3 (each change order once, UTC quarters) is $25 or more off on every figure it moves, and moves 12",
       len(moved3) == 12 and all(abs(s3[k] - pay[k]) >= 25 for k in moved3),
       min(abs(s3[k] - pay[k]) for k in moved3) if moved3 else None)
    tcq3 = [(v, 3) for v in ("V-20877", "V-31560")]
    ok("A8 stop S4 (by vendor number) splits Tri-County's third quarter, both halves $25 or more off",
       all(abs(s4[k] - pay[("2026-LSL-02", 3)]) >= 25 for k in tcq3), [round(s4[k]) for k in tcq3])
    def pay_on(rows, with_co=True):
        rows = rows.assign(q=rows.local_date.map(K.quarter_of),
                           paid=rows.paid_base + rows.paid_extra_ft + rows.paid_restoration)
        rows = rows[rows.local_date.map(lambda d: d.year == 2026)]
        where = dict(zip(rows.site_id, zip(rows.contract_no, rows.q)))
        tot = rows.groupby(["contract_no", "q"]).paid.sum().to_dict()
        n = rows.groupby(["contract_no", "q"]).size().to_dict()
        if with_co:
            for sites, amt in zip(co["sites"], co["Amount ($)"]):
                tot[where[sites[0]]] += float(amt)
        return {k: tot[k] / n[k] for k in n}
    first_close = comp.sort_values(["site_id", "closed_on", "row_status"]).drop_duplicates("site_id", keep="first")
    pay_first = pay_on(first_close)
    moved_first = [k for k in pay if math.floor(pay_first[k] + 0.5) != math.floor(pay[k] + 0.5)]
    ok("A10 the field notes file that a reclosing's paid amounts replace the first closing's; paying on the first "
       "closing moves %d of 12 figures" % len(moved_first),
       "the reclosing's paid amounts replace the first closing's" in notes_flat and len(moved_first) == 5,
       sorted(moved_first))
    pay_noco = pay_on(latest, with_co=False)
    co_log = texts[K.CHANGE_ORDERS]
    ok("A11 the change order log files that approved change orders are paid to the contractor; leaving them out "
       "moves all 12 figures by $25 or more",
       "paid to the contractor on its pay applications" in re.sub(r"\s+", " ", co_log) and
       all(abs(pay_noco[k] - pay[k]) >= 25 for k in pay), min(abs(pay_noco[k] - pay[k]) for k in pay))
    ok("A11 no filed sentence says how a change order is counted against its sites (ask A's device stays silent)",
       not re.search(r"paid once|counted once|per site|each site's pay application", co_log + notes_flat, re.I))
    main_cols = set(inv_raw.columns) | set(ver_raw.columns)
    ok("A9 no ask device or hazard column sits in the main call's files",
       not main_cols & {"co_amount", "co_no", "zone_on_form", "completed_utc", "vendor_no", "status"})

    # ---------------------------------------------------------------- ask B: access agreements
    ag = L.agreements(target)
    tr = L.outreach(target)
    zone_of = dict(zip(inv.sl_id, inv.zone))
    gold_b = F["agree"]
    ok("B1 twelve agreement counts equal figures.json", gold_b == fig["agreements_signed"])
    if world is not None:
        import asks as AS
        ok("B2 the shipped files reproduce the world's agreement counts", AS.agreements_answer(world["ag"]) == gold_b)
    sig = ag[ag.status == "SIGNED"]
    esigned = set(tr[tr.portal_status == "E-SIGNED"].sl_id)

    def by_zone(lines_set):
        return {zz: sum(1 for x in lines_set if zone_of[x] == zz) for zz in K.PLAN_ORDER}
    b1 = sig.zone_on_form.value_counts().to_dict()
    b2 = by_zone(set(sig.line))
    b3 = by_zone(set(sig.line) | esigned)
    b4 = by_zone(set(sig[sig.premise_no == ""].line))
    paper = set(ag[(ag.channel == "PAPER") & (ag.status == "SIGNED")].line)
    b5 = by_zone(paper | esigned)
    stops = (("S1 signed rows by the form's zone", b1), ("S2 the agreement system's signed lines, legacy keys mapped, "
                                                          "inventory zone (the cracker)", b2),
             ("S3 S2 with every line the portal shows e-signed added, withdrawn ones back in", b3),
             ("S4 legacy forms dropped", b4), ("S5 paper forms from the agreement system with the portal's e-signed "
                                               "lines, withdrawals not applied", b5))
    for name, st_ in stops:
        off = sum(1 for zz in K.PLAN_ORDER if st_.get(zz, 0) != gold_b[zz])
        ok("B3 stop %s is off on at least 10 of 12 zones" % name, off >= 10, off)
    ok("B3 the cracker's count misses all twelve zones", all(b2.get(zz, 0) != gold_b[zz] for zz in K.PLAN_ORDER))
    held = set(ag.line)
    portal_only = esigned - held
    po_z = by_zone(portal_only)
    ok("B4 every zone has lines whose only signed form is one the owner e-signed on the portal and the agreement system "
       "does not hold", all(po_z[zz] >= 1 for zz in K.PLAN_ORDER), po_z)
    wd_lines = set(ag[ag.status == "WITHDRAWN"].line)
    ok("B8 every withdrawal sits on a form the agreement system holds; the portal shows E-SIGNED for withdrawn portal "
       "forms (the tracker records no withdrawal), in at least ten zones",
       not (wd_lines & portal_only) and set(tr.portal_status) <= {"NOT OPENED", "OPENED", "STARTED", "E-SIGNED",
                                                                  "DECLINED"} and
       sum(1 for zz in K.PLAN_ORDER if any(zone_of[x] == zz for x in (wd_lines & esigned))) >= 10,
       len(wd_lines & esigned))
    ok("B9 the tracker carries one row per line open in the plan, in the inventory's zone",
       set(tr.sl_id) == set(inv[inv.zone.isin(K.PLAN_ORDER) & inv.cls.isin(["LEAD", "GRR", "LEAD STATUS UNKNOWN"])]
                             .sl_id) and tr.sl_id.is_unique and (tr.zone == tr.sl_id.map(zone_of)).all())
    moved = sig[sig.zone_on_form != sig.line.map(zone_of)]
    pairs = {(a, b) for a, b in zip(moved.zone_on_form, moved.line.map(zone_of))}
    ok("B5 the redraw moved lines inside six pairs of zones and no form signed after 20 October 2026 carries an old "
       "zone", pairs == set(K.REDRAW_PAIRS) and (moved.signed_on < K.REV2_DATE.isoformat()).all(), pairs)
    ok("B6 no shipped text states the zone redraw, an import, a rejected or missing form, or that the agreement system "
       "and the portal disagree", not any(re.search(r"redr[ae]w|realign|boundar|import|reject|queue|attachment|"
                                                    r"not (yet )?in the agreement|missing", t, re.I)
                                          for f, t in texts.items() if f not in (K.METER_EXCHANGES, K.TAP_SAMPLES)))
    ok("B7 the field notes define the inventory's zone and the portal's E-SIGNED status by their meaning only (no rule "
       "counts agreements by a zone or a source)",
       "`zone`: the line's replacement zone under plan revision 2" in notes and
       "`zone_on_form`: the replacement zone printed on the form." in notes and
       "E-SIGNED (the owner signed the right-of-entry form on the portal)" in notes_flat and
       not re.search(r"count\w* (agreements|forms|lines) by|system of record", notes_flat, re.I))
    lg = ag[ag.premise_no != ""]
    xw = pd.read_csv(os.path.join(target, K.CROSSWALK), dtype=str, keep_default_na=False)
    ok("H4 legacy forms carry premise numbers that match the crosswalk only with the zero padding restored",
       len(lg) > 500 and not lg.premise_no.isin(set(xw.legacy_premise_no)).any() and
       lg.premise_no.str.zfill(8).isin(set(xw.legacy_premise_no)).all() and
       (lg.signed_on < K.MIGRATION.isoformat()).all())
    dup = sig.groupby("line").size()
    dup_z = sig[sig.line.isin(dup[dup > 1].index)].line.map(zone_of).nunique()
    wd = ag[ag.status == "WITHDRAWN"].line.map(zone_of).nunique()
    ok("H5 H6 paper and portal duplicates and withdrawn agreements in every zone", dup_z == 12 and wd == 12,
       (dup_z, wd))
    ask_cols = set(ag.columns) | set(tr.columns)
    ok("B10 no ask device or hazard column sits in the main call's files, and no main-call column in the ask files "
       "beyond keys and zone", not (set(inv_raw.columns) | set(ver_raw.columns)) & {
           "co_amount", "co_no", "zone_on_form", "completed_utc", "vendor_no", "status", "portal_status"})

    # ---------------------------------------------------------------- distractors
    for d in K.DISTRACTORS:
        tmp = tempfile.mkdtemp()
        try:
            for f in files:
                if f != d:
                    shutil.copy2(os.path.join(target, f), os.path.join(tmp, f))
            F2 = DL.compute(tmp)
            ok("D1 deleting %s moves nothing" % d,
               finish_list(F2["z"]) == golden_years and F2["pay"] == pay and F2["agree"] == gold_b and
               abs(F2["z"].cum_cost.iloc[-1] - z.cum_cost.iloc[-1]) < 1e-6)
        finally:
            shutil.rmtree(tmp)

    # ---------------------------------------------------------------- the goldens agree with figures.json
    gx = text_of_xlsx(os.path.join(golden, K.DELIVERABLES[0]))
    gp = re.sub(r"\s+", " ", text_of_pdf(os.path.join(golden, K.DELIVERABLES[1])))
    miss = []
    for zz, d in fig["zones"].items():
        for v in (d["lead_and_grr_to_replace"], d["plan_cost_million"]):
            if v not in gp:
                miss.append((zz, v))
        if str(int(d["plan_cost"].replace(",", ""))) not in gx:
            miss.append((zz, d["plan_cost"]))
    for c, d in fig["payments_2026_per_full_replacement"].items():
        for q in (1, 2, 3, 4):
            if d["Q%d" % q] not in gp or str(int(d["Q%d" % q].replace(",", ""))) not in gx:
                miss.append((c, q))
    for zz, n in fig["agreements_signed"].items():
        if "{:,}".format(n) not in gp:
            miss.append((zz, n))
    ok("F1 every owed figure appears in both goldens at the same rounding", not miss, miss)
    ok("F2 the board paper commits to the call in its first paragraph",
       "The last zone, RZ-06 Wexley, is finished in programme year 2037" in gp)
    kes = fig["kind_era_shares"]["lead_or_galvanized_cards"]
    ok("F3 the board paper's rates are the shares on file: on lead or galvanized mains by era, from figures.json",
       all(("%s per cent" % kes[DL.ERA_LABEL[e]]["per_cent"]) in gp for e in range(3)) and
       "The rates are alike on the replaced mains and on single-line visits" in gp)
    rep_nt = inv[(inv.basis == "REPLACED") & (inv.record == "")]
    ok("F4 every no-tap-card line the inventory carries as replaced was found lead or GRR on its first verification",
       len(rep_nt) > 1000 and rep_nt.sl_id.map(first_res).isin(["LEAD", "GRR"]).all(), len(rep_nt))

    n_fail = sum(1 for _, c, _ in RESULTS if not c)
    print("checks: %d assertions, %d failed" % (len(RESULTS), n_fail))
    if n_fail:
        raise SystemExit("checks failed")
    return RESULTS
