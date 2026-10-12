"""task124's generator assertions, run on the built pack (target/), the goldens and the world that made them.

Every rung, partial and fork of the design note is recomputed here from the shipped files; the world (ground truth,
causes of each dig) is used only to assert facts the files cannot show (selection, the sweeps' identity)."""
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


# ------------------------------------------------------------------------------------------------- the run
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
    ok("R1 no headline count is a multiple of 100 (inventory total, zone sizes, class totals)",
       all(int(h) % 100 for h in heads), heads)
    ok("R2 zone sizes all differ", zone_n.nunique() == len(zone_n))
    co = L.change_orders(target)
    ok("R3 change order descriptions do not repeat beyond a real rate", co.Description.nunique() >= 0.85 * len(co),
       "%d of %d" % (co.Description.nunique(), len(co)))
    people = {"Andrew Wells", "Bethany Davidson", "Seth Sullivan", "William Bates"}
    named = set()
    for t in texts.values():
        for m in re.finditer(r"\b(Andrew|Bethany|Seth|William|John|Jane|Mary|Robert|Susan|Michael)\s+[A-Z][a-z]+", t):
            named.add(m.group(0))
    ok("R4 every person named in the pack is drawn on the card", named <= people, named - people)
    late = []
    for f, col, last in ((K.INVENTORY, "field_verified_on", "2027-01-08"), (K.INVENTORY, "replaced_on", "2027-01-08"),
                         (K.AGREEMENTS, "signed_on", "2027-01-08"), (K.AGREEMENTS, "status_date", "2027-01-08"),
                         (K.COMPLETIONS, "closed_on", "2027-01-08"), (K.TAP_SAMPLES, "collected_on", "2026-12-31"),
                         (K.METER_EXCHANGES, "exchanged_on", "2025-12-31")):
        v = pd.read_csv(os.path.join(target, f), dtype=str, keep_default_na=False)[col]
        if v[v != ""].max() > last:
            late.append((f, col))
    ok("R5 no extract carries a date past its extract (H16)", not late, late)
    built = [f for f, t in texts.items() if re.search(r"fictional|fictitious|constructed for|this exercise|synthetic|"
                                                      r"generated by", t, re.I)]
    ok("R6 no file says the pack was built (H24)", not built, built)
    ok("R7 no file name broadcasts the stump",
       not any(re.search(r"sweep|bias|known_issue|selection|answer|distract", f, re.I) for f in files))

    # ---------------------------------------------------------------- signposts (readability screen)
    sign = r"main replacement|mains? (was|were) replaced|sweep|project|coverage|selection|biased|representative|" \
           r"verified whole|every service line on|dug because|systematic|prompted by"
    hits = {f: m.group(0) for f, t in texts.items() if f not in (K.METER_EXCHANGES,) for m in [re.search(sign, t, re.I)]
            if m}
    ok("S1 no shipped sentence names why a line was dug, a main replacement, a project or coverage", not hits, hits)
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

    # ---------------------------------------------------------------- the main call from the shipped files
    F = DL.compute(target)
    s, whole, p, p0, z, z0, ap = F["s"], F["whole"], F["p"], F["p0"], F["z"], F["z0"], F["ap"]
    prices, mob = L.unit_costs(target)
    rem = AN.remaining(inv)
    golden_years = [2027, 2029, 2030, 2031, 2032, 2033, 2034, 2034, 2035, 2036, 2036, 2037]
    ok("M1 shares on the segments verified whole are 5/9, 6/19 and 1/12 on 792, 304 and 168 lines",
       all(abs(p[e] - x) < 1e-12 for e, x in enumerate((5 / 9, 6 / 19, 1 / 12))) and
       [F["era_n"][e] for e in range(3)] == [792, 304, 168], (p, F["era_n"]))
    ok("M2 78 segments verified whole; every other segment at 0.43 or less (SF12)",
       F["n_segments"] == 78 and cov[cov < 0.999].max() <= 0.43, (F["n_segments"], round(cov[cov < 0.999].max(), 3)))
    ok("M3 the call: last zone RZ-06 finished 2037, the twelve finish years as designed",
       finish_list(z) == golden_years and z.zone.iloc[-1] == "RZ-06", finish_list(z))
    e_repl = (abs((z.replacements / 10) % 1 - 0.5) * 10).min()
    e_cost = (abs((z.cost / 1e5) % 1 - 0.5) * 1e5).min()
    e_year = min(min(y - math.floor(y), math.ceil(y) - y) for y in z.years)
    ok("M4 margins: replacements 2.6 lines, costs $16,000, running totals 0.13 programme years from an edge",
       e_repl >= 2.6 and e_cost >= 16_000 and e_year >= 0.13,
       "%.2f lines, $%.0f, %.3f years ($%.0f)" % (e_repl, e_cost, e_year, e_year * ap))
    ok("M5 R0 default path: every verified no-record line by era, last zone 2039, 2 of 12 years right",
       int(z0.finish_year.max()) == 2039 and sum(a == b for a, b in zip(finish_list(z0), golden_years)) == 2,
       (finish_list(z0), {k: round(v, 3) for k, v in p0.items()}))
    unk = inv[inv.zone.isin(K.PLAN_ORDER) & (inv.cls == "LEAD STATUS UNKNOWN")].copy()
    unk["era"] = unk.year_built.map(K.era_of)
    r1 = sched_expected(rem, model_expected(s, unk, era=True, year=True, zone=True), ap, prices, mob)
    ok("M6 R1 a model on era, construction year and zone fitted on every verification: last zone 2039",
       int(r1.finish_year.max()) == 2039, finish_list(r1))
    cell = s.groupby(["zone", "era"]).hit.mean()
    era_all = s.groupby("era").hit.mean()
    expz = {zz: sum(n * cell.get((zz, e), era_all[e]) for e, n in unk[unk.zone == zz].era.value_counts().items())
            for zz in K.PLAN_ORDER}
    r1b = sched_expected(rem, expz, ap, prices, mob)
    ok("M7 R1 reweighting the verified lines to the unknown lines' zone and era: last zone 2039",
       int(r1b.finish_year.max()) == 2039, finish_list(r1b))
    pooled = float(s[whole].hit.mean())
    r2 = AN.zone_costs(rem, [pooled] * 3, ap, prices, mob)
    ok("M8 R2 one pooled share on the segments verified whole: last zone 2039, 7 of 12 years right",
       int(r2.finish_year.max()) == 2039 and sum(a == b for a, b in zip(finish_list(r2), golden_years)) == 7,
       (round(pooled, 4), finish_list(r2)))
    ok("M9 R2's pool leans old: 792 of the 1,264 whole-segment no-record lines built before 1930",
       F["era_n"][0] == 792 and sum(F["era_n"].values()) == 1264)
    cause = AN.zone_costs(rem, AN.shares(s, ~whole), ap, prices, mob)
    allpool = AN.zone_costs(rem, [float(s.hit.mean())] * 3, ap, prices, mob)
    rec0 = AN.zone_costs(rem, [0, 0, 0], ap, prices, mob)
    lead1 = AN.zone_costs(rem, [1, 1, 1], ap, prices, mob)
    ok("M10 partials: digs for cause by era 2040, every verification pooled 2041, records only 2033, every unknown "
       "lead 2045", [int(x.finish_year.max()) for x in (cause, allpool, rec0, lead1)] == [2040, 2041, 2033, 2045],
       [int(x.finish_year.max()) for x in (cause, allpool, rec0, lead1)])
    sw = s[whole].assign(decade=(s[whole].year_built // 10) * 10)
    dec = sw.groupby("decade").agg(era=("era", "first"), share=("hit", "mean"))
    ok("M11 C1 every construction decade on the whole segments carries its era's share exactly",
       all(abs(r.share - p[r.era]) < 1e-12 for r in dec.itertuples()), dec.round(4).to_dict())
    gold_exp = {r.zone: r.replacements - r.lgrr for r in z.itertuples()}
    ey = model_expected(s[whole], unk, era=True, year=True)
    ok("M12 C1 an era and construction-year model on the whole segments returns the era shares within 0.15 line",
       max(abs(ey[zz] - gold_exp[zz]) for zz in K.PLAN_ORDER) < 0.15,
       max(abs(ey[zz] - gold_exp[zz]) for zz in K.PLAN_ORDER))
    ze = model_expected(s[whole], unk, era=True, year=False, zone=True)
    rz = sched_expected(rem, ze, ap, prices, mob)
    dz = {zz: ze[zz] - gold_exp[zz] for zz in K.PLAN_ORDER}
    ok("M13 C4 a model with zone effects on the whole segments keeps the finish years and moves zone counts by up to "
       "200 lines", finish_list(rz) == golden_years and 195 <= max(abs(v) for v in dz.values()) <= 205,
       {k: round(v, 1) for k, v in dz.items()})
    yo = model_expected(s[whole], unk, era=False, year=True)
    dy = {zz: yo[zz] - gold_exp[zz] for zz in K.PLAN_ORDER}
    over = sorted(round(v) for v in dy.values() if v > 0)
    ok("M14 C4 a construction-year logistic on the whole segments overstates eleven zones by 5 to 150 lines",
       len(over) == 11 and over[0] >= 5 and over[-1] <= 150, {k: round(v, 1) for k, v in dy.items()})
    rr = rem.copy()
    zr = []
    cum = 0.0
    for r in rr.itertuples():
        u = r.u0 + r.u1 + r.u2
        e = round(r.u0 * p[0] + r.u1 * p[1] + r.u2 * p[2])
        uf, ud = prices[r.zone]
        cum += (r.lgrr + e) * uf + (u - e) * ud + mob
        zr.append(K.FIRST_YEAR + math.ceil(cum / ap - 1e-9) - 1)
    ok("M15 axis 10 rounding expected lines to whole lines first moves no finish year", zr == golden_years, zr)
    rng = np.random.default_rng(124)
    inv_s = inv.sample(frac=1.0, random_state=rng.integers(1 << 31)).reset_index(drop=True)
    ver_s = ver.sample(frac=1.0, random_state=rng.integers(1 << 31)).reset_index(drop=True)
    s_s = AN.sample(inv_s, ver_s)
    z_s = AN.zone_costs(AN.remaining(inv_s), AN.shares(s_s, s_s.coverage >= 0.999), ap, prices, mob)
    ok("M16 axis 14 shuffled rows give the same schedule", finish_list(z_s) == golden_years and
       abs(z_s.cum_cost.iloc[-1] - z.cum_cost.iloc[-1]) < 1e-3)
    first_whole = vv[vv.whole].groupby("sl_id").date.min()
    ver23 = ver[ver.date >= dt.date(2023, 1, 1)]
    s23 = AN.sample(inv, ver23)
    p23 = AN.shares(s23, s23.coverage >= 0.999)
    ok("M17 axis 8 every whole-segment verification is from May 2023, so a 2023-on window gives the same shares",
       first_whole.min() >= dt.date(2023, 5, 1) and all(abs(p23[e] - p[e]) < 1e-12 for e in range(3)),
       first_whole.min())
    s_w = AN.sample(inv, ver[ver.source == "WMS"])
    p_w = AN.shares(s_w, s_w.coverage >= 0.999)
    ok("M18 axis 16 dropping every customer-system row (legacy keys) leaves the golden shares (mess neutral)",
       all(abs(p_w[e] - p[e]) < 1e-12 for e in range(3)))
    multi = ver.groupby("sl_id").result.nunique()
    ok("M19 SF11 every re-verified line has one result on every visit", int(multi.max()) == 1 and
       int((ver.groupby("sl_id").size() > 1).sum()) > 100, int((ver.groupby("sl_id").size() > 1).sum()))
    first_res = ver.sort_values(["date", "sl_id"]).groupby("sl_id").result.first()
    tc = inv[inv.segment.isin(whole_seg) & inv.record.isin(["LEAD", "GALV"])]
    ok("SF9 every lead or galvanized tap card line on a whole segment proved lead or GRR",
       len(tc) > 50 and tc.sl_id.map(first_res).isin(["LEAD", "GRR"]).all(), len(tc))
    verified = set(ver.sl_id)
    ok("SF8 no verified line is still Lead Status Unknown", not inv[inv.sl_id.isin(verified)].cls.eq(
        "LEAD STATUS UNKNOWN").any())
    nr = inv[(inv.record == "") & (inv.year_built > 0) & (inv.year_built < 1989)].copy()
    nr["era"] = nr.year_built.map(K.era_of)
    alt = rem.copy()
    for e, col in enumerate(("u0", "u1", "u2")):
        alt[col] = alt.zone.map(nr[nr.era == e].groupby("zone").size()).fillna(0).astype(int)
    z8 = AN.zone_costs(alt, p, ap, prices, mob)
    ok("SF8 counting every no-record line as unknown, verified ones included, gives a later schedule",
       int(z8.finish_year.max()) > 2037, finish_list(z8))
    first = ver.sort_values(["date", "sl_id"]).groupby("sl_id", as_index=False).first()
    sa = first.merge(inv[["sl_id", "year_built"]], on="sl_id")
    sa = sa[(sa.year_built > 0) & (sa.year_built < 1989)].assign(era=lambda d: d.year_built.map(K.era_of),
                                                                  hit=lambda d: d.result.isin(["LEAD", "GRR"]))
    z10 = AN.zone_costs(rem, {e: float(sa[sa.era == e].hit.mean()) for e in range(3)}, ap, prices, mob)
    ok("SF10 shares from every verified line, tap card lines included: 2039 or later",
       int(z10.finish_year.max()) >= 2039, finish_list(z10))
    same = True
    for t in (0.45, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 1.0):
        pt = AN.shares(s, s.coverage >= t - 1e-9)
        same &= finish_list(AN.zone_costs(rem, pt, ap, prices, mob)) == golden_years
    ok("SF12 any coverage threshold from 0.45 to 1.00 selects the same segments and the same schedule", same)
    before = z.cum_cost.iloc[-2]
    ok("SF2 the last zone starts in 2036 and finishes in 2037: a start-year reading files the same call",
       K.FIRST_YEAR + math.floor(before / ap) == 2036)
    ok("SF3 no shipped document states an escalation rate", not any(re.search(r"escalat|inflat", t, re.I)
                                                                     for t in texts.values()))
    lead_only_p = {e: float(s[whole & (s.era == e)].result.eq("LEAD").mean()) for e in range(3)}
    rem_l = rem.copy()
    rem_l["lgrr"] = rem_l.zone.map(inv[inv.cls == "LEAD"].groupby("zone").size()).fillna(0).astype(int)
    zl = AN.zone_costs(rem_l, lead_only_p, ap, prices, mob)
    ok("SF4 lead only, GRR left out, gives a different, earlier schedule",
       finish_list(zl) != golden_years and int(zl.finish_year.max()) < 2037, finish_list(zl))
    ok("SF5 every unknown line taken as lead: 2045", int(lead1.finish_year.max()) == 2045)
    ok("SF6 the plan files the season close that makes a 2037 finish meet the deadline",
       "finished by 31 October of that year" in re.sub(r"\s+", " ", plan))
    comp = L.completions(target)
    latest = comp.sort_values(["site_id", "closed_on", "row_status"]).drop_duplicates("site_id", keep="last")
    paid26 = (latest.paid_base + latest.paid_extra_ft + latest.paid_restoration).sum() + co["Amount ($)"].sum()
    avg26 = paid26 / len(latest)
    z7 = AN.zone_costs(rem, p, ap, {zz: (avg26, prices[zz][1]) for zz in prices}, mob)
    ok("SF7 costing at what a 2026 replacement was paid gives a different, later schedule",
       finish_list(z7) != golden_years and int(z7.finish_year.max()) > 2037, (round(avg26), finish_list(z7)))
    ok("SF7 the plan files the 2027 unit cost schedule as the cost basis",
       "2027 unit cost schedule" in re.sub(r"\s+", " ", plan))
    # SF13 mobilisation in each programme year a zone is worked
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
    unk_all = inv_raw[inv_raw.sl_class == "LEAD STATUS UNKNOWN"].year_built.astype(int)
    ok("M20 axis 9 no unknown line is built in or after 1989 or has no year", unk_all.between(1, 1988).all())
    ok("M21 axis 2 one row per service line", inv_raw.sl_id.is_unique)
    zero = inv_raw[inv_raw.year_built == "0"]
    ok("M25 the assessor's zero years all sit on tap card lines, outside both estimates",
       len(zero) > 100 and (zero.tap_card_material != "").all(), len(zero))
    t26 = AN.sample(inv, ver[ver.date >= dt.date(2026, 1, 1)])
    z26 = AN.zone_costs(rem, AN.shares(t26), ap, prices, mob)
    ok("M22 Gate G first move: the 2026 verifications alone file 2039 or later", int(z26.finish_year.max()) >= 2039,
       (finish_list(z26), {k: round(v, 3) for k, v in AN.shares(t26).items()}))
    ok("M23 separation: the default path's last zone two years past the answer, 10 of 12 finish years apart",
       int(z0.finish_year.max()) - 2037 == 2 and sum(a != b for a, b in zip(finish_list(z0), golden_years)) == 10)
    if world is not None:
        lines, ev = world["lines"], world["ev"]
        sweeps = set(world["sweeps"])
        ok("W1 the segments verified whole are exactly the main replacement projects' segments", whole_seg == sweeps)
        cause_of = ev[~ev.cause.str.startswith("main")]
        nrl = lines[(lines.record == "") & lines.era.between(0, 2)]
        dug = nrl[nrl.sl_id.isin(set(cause_of.sl_id))]
        ok("W2 selection: lines dug for cause are lead or GRR far more often than the population share",
           (dug.truth != "NON-LEAD").groupby(dug.era).mean().min() > 0.2 and
           (dug.truth != "NON-LEAD").groupby(dug.era).mean()[0] > p[0] + 0.25)
        tr = lines.set_index("sl_id").truth
        res_ok = (ver.result == ver.sl_id.map(tr).map({"LEAD": "LEAD", "GRR": "GRR", "NON-LEAD": "NON-LEAD"})).all()
        ok("M24 clean-data (instrument): every recorded result is the material in the ground", res_ok)
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
    ok("C2 the first quarter's replacements were all found in the 2025 season",
       q1.site_id.map(first_any).map(lambda d: d.year == 2025).all())
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
    main_cols = set(inv_raw.columns) | set(ver_raw.columns)
    ok("A9 no ask device or hazard column sits in the main call's files",
       not main_cols & {"co_amount", "co_no", "zone_on_form", "completed_utc", "vendor_no", "status"})

    # ---------------------------------------------------------------- ask B: access agreements
    ag = L.agreements(target)
    zone_of = dict(zip(inv.sl_id, inv.zone))
    gold_b = F["agree"]
    ok("B1 twelve agreement counts equal figures.json", gold_b == fig["agreements_signed"])
    if world is not None:
        import asks as AS
        ok("B2 the shipped files reproduce the world's agreement counts", AS.agreements_answer(world["ag"]) == gold_b)
    sig = ag[ag.status == "SIGNED"]
    b1 = sig.zone_on_form.value_counts().to_dict()
    b2 = sig.drop_duplicates("line").zone_on_form.value_counts().to_dict()
    leg = sig[sig.sl_id != ""]
    b3 = leg.drop_duplicates("sl_id").sl_id.map(zone_of).value_counts().to_dict()
    for name, st_ in (("S1 rows by the form's zone", b1), ("S2 distinct lines by the form's zone (the cracker)", b2),
                      ("S3 inventory zone, legacy forms dropped", b3)):
        off = sum(1 for zz in K.PLAN_ORDER if st_.get(zz, 0) != gold_b[zz])
        ok("B3 stop %s is off on at least 10 of 12 zones" % name, off >= 10, off)
    ok("B4 the cracker's count misses all twelve zones", all(b2.get(zz, 0) != gold_b[zz] for zz in K.PLAN_ORDER))
    moved = sig[sig.zone_on_form != sig.line.map(zone_of)]
    pairs = {(a, b) for a, b in zip(moved.zone_on_form, moved.line.map(zone_of))}
    ok("B5 the redraw moved lines inside six pairs of zones and no form signed after 20 October 2026 carries an old "
       "zone", pairs == set(K.REDRAW_PAIRS) and (moved.signed_on < K.REV2_DATE.isoformat()).all(), pairs)
    ok("B6 no shipped text states the zone redraw", not any(re.search(r"redr[ae]w|realign|boundar", t, re.I)
                                                            for t in texts.values()))
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
    other = 1 - float(whole.mean())
    ok("F3 'three in four' of the verified no-tap-card lines sit off the segments verified whole (board paper)",
       0.70 <= other <= 0.78 and "Three in four of the lines with no tap card" in gp, round(other, 3))
    ok("F2 the board paper commits to the call in its first paragraph",
       "The last zone, RZ-06 Wexley, is finished in programme year 2037" in gp)

    n_fail = sum(1 for _, c, _ in RESULTS if not c)
    print("checks: %d assertions, %d failed" % (len(RESULTS), n_fail))
    if n_fail:
        raise SystemExit("checks failed")
    return RESULTS
