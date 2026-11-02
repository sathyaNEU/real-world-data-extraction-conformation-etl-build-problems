"""task454 ask layer against the careful solver's routes, on the cut pack.

    python3 task454/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The ask is the FY2026
workbook: for each of the twelve candidate classes, its claims (net of reversals), units dispensed and ingredient cost
paid over fills from April 2025 to March 2026 (36 figures). Every route below is a complete pipeline over the cut pack,
scored figure by figure against figures.json; a figure is kept only when it equals the golden at the prompt's rounding
(claims and units whole, money to the dollar).

The cracker is the careful solver. It lands the call (each unpriced NDC costed from the priced NDCs of its product and
package type), runs the hygiene battery on the ask's path (exact duplicate rows, one row per claim id, every reversal
matched to its claim or found an orphan, the summary's stored class labels checked against the finer key, the
summary's control totals tied to its detail, every summary NDC through the drug file, both clocks on every claim row),
executes every filed rule (C.6's twelve months of fills before the window, the request letter's class list in force
from 1 January 2027, the prompt's claims paid through 20 April 2027) and reads every document in the pack, the
administrator's data delivery note included, which states what each file holds and to which paid date. The mirror is
the best response off the call (the default path, the product's rate for every unpriced NDC) on the ask's natural read,
without the battery: the summary as delivered, by its own class column. The full includer is the golden's route and
has to give back figures.json exactly (the route code's control). The stops are the ask sheet's other wrong paths.

The pair is the ask sheet's formula: 38 recommendation and components, 7 instruction following, 55 asks over 52 ask
criteria (the twelve spreads to the nearest thousand, the chart's four criteria and the 36 FY2026 figures), a response
off the call keeping r = 5 of the 38. The chart's criteria follow the call: one bar per class and a labelled axis go to
both, the bars at the golden's spreads and the proposed class marked only to the response on the call."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C    # noqa: E402  (the pack readers the golden and the checks share)
import world as W   # noqa: E402

TASK = os.path.dirname(HERE)
REC, INS, ASK, OFF = 38.0, 7.0, 55.0, 5.0
CHART = 4                      # one bar per class, the bars at the spreads, the proposed class marked, the axis
CHART_OFF = 2                  # what a response off the call keeps of the chart (the bars and the axis)
FY = (dt.date(2025, 4, 1), dt.date(2026, 3, 31))


def pack_dir(arg):
    """The pack as a folder: target.zip unpacked into a scratch folder (removed after), or the folder given."""
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling454-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    md5 = hashlib.md5(open(src, "rb").read()).hexdigest()
    return tmp, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(tmp)), md5)


def doc_text(path):
    if path.endswith(".docx"):
        import docx
        d = docx.Document(path)
        return " ".join([p.text for p in d.paragraphs] + [c.text for t in d.tables for r in t.rows for c in r.cells])
    from pypdf import PdfReader
    return " ".join(" ".join((p.extract_text() or "").split()) for p in PdfReader(path).pages)


def filed(folder):
    """What the pack's documents state about the ask's path, read the way a careful solver reads them."""
    out = {}
    req = doc_text(os.path.join(folder, W.FILES["request"]))
    out["list_rule"] = "in force from 1 January 2027" in req
    terms = doc_text(os.path.join(folder, W.FILES["terms"]))
    out["c6"] = "twelve months of fills before those" in terms
    note = os.path.join(folder, W.FILES["trans"]) if W.FILES.get("trans") else None
    out["summary_cut"] = out["extract_from"] = None
    if note and os.path.exists(note):
        t = doc_text(note)
        m = re.search(r"transactions paid through (\d{1,2} \w+ \d{4})", t)
        if m:
            out["summary_cut"] = dt.datetime.strptime(m.group(1), "%d %B %Y").date()
        m = re.search(r"paid (\d{1,2} \w+ \d{4}) to (\d{1,2} \w+ \d{4}), whatever the fill date", t)
        if m:
            out["extract_from"] = dt.datetime.strptime(m.group(1), "%d %B %Y").date()
    return out


def battery(folder):
    """The hygiene battery a careful analyst runs on the ask's path: (check, passed, detail)."""
    cl = C.claims(folder)
    dr, cls = C.drugs(folder), C.classes(folder)
    sm = C.summary(folder)
    out = []
    raw = pd.read_csv(os.path.join(folder, W.FILES["claims"]), dtype=str, keep_default_na=False)
    out.append(("exact duplicate rows in the extract", not raw.duplicated().any(), "%d" % int(raw.duplicated().sum())))
    out.append(("one row per claim id", raw.claim_id.is_unique, "%d rows" % len(raw)))
    rev = cl[cl.transaction_code == "B2"]
    found = rev.original_claim_id.isin(set(cl.claim_id))
    orphans = rev[~found]
    out.append(("every reversal matched to a claim in the extract, or an orphan whose claim was paid before the extract",
                bool((orphans.fill < W.WINDOW[0]).all()),
                "%d reversals, %d orphans, every orphan an FY2026 fill" % (len(rev), len(orphans))))
    gpc = dr.set_index("ndc").GPC
    cur = sm.NDC.map(gpc).map(cls)
    stale = sm[cur != sm["Drug class"]]
    out.append(("the summary's stored class label checked against the NDC's class on the current list",
                True, "%d rows (%d NDCs) carry another class; %d labels are not on the current list" % (
                    len(stale), stale.NDC.nunique(), len(set(sm["Drug class"]) - set(cls.values())))))
    tot = pd.read_excel(os.path.join(folder, W.FILES["summary"]), sheet_name="Control totals")
    det = sm.groupby("Fill month")[["Claims", "Ingredient cost paid"]].sum()
    tie = all(det.loc[r["Fill month"], "Claims"] == r["Claims"] and
              abs(det.loc[r["Fill month"], "Ingredient cost paid"] - r["Ingredient cost paid"]) < 0.05
              for _, r in tot.iterrows())
    out.append(("the summary's control totals tie to its detail", tie, "%d months" % len(tot)))
    out.append(("every summary NDC through the drug file", bool(sm.NDC.isin(set(dr.ndc)).all()), "%d NDCs" % sm.NDC.nunique()))
    early = cl[cl.fill < W.WINDOW[0]]
    out.append(("both clocks on every claim row: FY2026 fills in the extract, paid from its first day",
                len(early) > 0, "%d transactions, paid %s to %s" % (len(early), early.paid.min(), early.paid.max())))
    return out


def ask_route(folder, label="current", late_from=None):
    """The 36 FY2026 figures a route gives: the summary's rows by class (`label`: 'current' places each NDC through
    the drug file and the current list, 'stored' takes the summary's own class column), plus, when `late_from` is a
    date, the extract's FY2026 fills paid on or after it (reversals netted)."""
    sm, dr, cls = C.summary(folder), C.drugs(folder), C.classes(folder)
    gpc = dr.set_index("ndc").GPC
    sm = sm.assign(cls=sm["Drug class"] if label == "stored" else sm.NDC.map(gpc).map(cls))
    g = sm.groupby("cls")[["Claims", "Units", "Ingredient cost paid"]].sum()
    out = {c: [int(g.loc[c, "Claims"]) if c in g.index else 0, float(g.loc[c, "Units"]) if c in g.index else 0.0,
               float(g.loc[c, "Ingredient cost paid"]) if c in g.index else 0.0] for c in W.SHORTLIST_NAMES}
    if late_from is not None:
        cl = C.claims(folder)
        x = cl[(cl.fill >= FY[0]) & (cl.fill <= FY[1]) & (cl.paid >= late_from)].copy()
        x["cls"] = x.ndc.map(gpc).map(cls)
        x["n"] = np.where(x.transaction_code == "B2", -1, 1)
        h = x.groupby("cls")[["n", "quantity_dispensed", "ingredient_cost_paid"]].sum()
        for c in W.SHORTLIST_NAMES:
            if c in h.index:
                out[c][0] += int(h.loc[c, "n"])
                out[c][1] += float(h.loc[c, "quantity_dispensed"])
                out[c][2] += float(h.loc[c, "ingredient_cost_paid"])
    return {c: (v[0], int(round(v[1])), int(round(v[2]))) for c, v in out.items()}


def kept(route, figs):
    n = 0
    for c in W.SHORTLIST_NAMES:
        f = figs["classes"][c]
        n += sum(a == b for a, b in zip(route[c], (f["claims_fy26"], f["units_fy26"], f["ingredient_fy26"])))
    return n


def spreads_kept(sp, figs):
    return sum(int(round(sp[c] / 1000.0)) * 1000 == figs["classes"][c]["spread"] for c in W.SHORTLIST_NAMES)


def pair(kc, km, n):
    c, s = REC + INS + ASK * kc / n, OFF + INS + ASK * km / n
    return c, s, (c + s) / 2.0


def main(arg=None):
    folder, scratch, stamp = pack_dir(arg)
    try:
        return run(folder, stamp)
    finally:
        if scratch:
            shutil.rmtree(scratch)


def run(folder, stamp):
    print("pack: " + stamp)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    cl, dr, cls = C.frame(folder)
    gold = C.spreads(folder, "golden", cl, dr, cls)[0]
    dflt = C.spreads(folder, "default", cl, dr, cls)[0]
    rk, drk = C.ranking(gold), C.ranking(dflt)
    on_call = rk[0] == figs["call"] and rk[1] == figs["runner_up"] and \
        round(gold[rk[0]] / gold[rk[1]], 2) == figs["golden_margin"]
    off_call = drk[0] != figs["call"]
    ksp, msp = spreads_kept(gold, figs), spreads_kept(dflt, figs)
    print("cracker's call: %s, %.2f times %s, %d of 12 spreads at the golden's thousand (%s)" % (
        rk[0], gold[rk[0]] / gold[rk[1]], rk[1], ksp, "lands the golden" if on_call else "MISSES"))
    print("mirror's call (the default path): %s, %.2f times %s, %d of 12 spreads at the golden's thousand (%s)" % (
        drk[0], dflt[drk[0]] / dflt[drk[1]], drk[1], msp, "off the call" if off_call else "ON THE CALL"))
    if not (on_call and off_call):
        print("the rows below assume the cracker on the call and the mirror off it: they are not")
        return 1

    print("\nwhat the pack files on the ask's path (read from the documents):")
    f = filed(folder)
    print("  request letter, the class list in force from 1 January 2027: %s" % f["list_rule"])
    print("  Attachment C, C.6, the twelve months of fills before the window: %s" % f["c6"])
    print("  data delivery note, the summary's last paid date: %s; the extract's first paid date: %s" % (
        f["summary_cut"], f["extract_from"]))

    print("\nthe cracker's hygiene battery on the ask's path:")
    bat = battery(folder)
    for check, passed, detail in bat:
        print("  %-4s %s (%s)" % ("ok" if passed else "FAIL", check, detail))

    n_fy = 3 * len(W.SHORTLIST_NAMES)
    full = ask_route(folder, "current", W.SUMMARY_PAID_THROUGH + dt.timedelta(days=1))
    kf = kept(full, figs)
    if kf != n_fy:
        print("CONTROL FAILED: the full includer gives %d of %d, the route code does not reproduce figures.json" % (
            kf, n_fy))
        return 1
    # the careful solver: the request letter's list for every row, and the extract's FY2026 payments from the day
    # after the summary's stated cut (the delivery note); with no stated cut it would have nothing to cut on
    cut = f["summary_cut"]
    crk = ask_route(folder, "current", cut + dt.timedelta(days=1) if cut else None)
    mir = ask_route(folder, "stored", None)
    stops = {
        "the summary as delivered, by its stored class (the natural read)": ask_route(folder, "stored", None),
        "the summary alone, every NDC through the current list": ask_route(folder, "current", None),
        "the stored class with the later payments": ask_route(folder, "stored", W.SUMMARY_PAID_THROUGH + dt.timedelta(days=1)),
        "the extract's FY2026 payments added from its first paid date (1 to 20 April 2026 twice)":
            ask_route(folder, "current", W.EXTRACT_FROM),
    }
    kc, km = kept(crk, figs), kept(mir, figs)
    a = "Anticonvulsants"
    print("\nFY2026 workbook, %s (claims, units, ingredient cost paid; figures.json %s):" % (
        a, (figs["classes"][a]["claims_fy26"], figs["classes"][a]["units_fy26"], figs["classes"][a]["ingredient_fy26"])))
    print("  cracker  %s" % (crk[a],))
    print("  mirror   %s" % (mir[a],))
    print("\nper route, FY2026 figures kept of %d:" % n_fy)
    print("  %-92s %d" % ("cracker (call landed, battery run, every filed rule, every document read)", kc))
    print("  %-92s %d" % ("mirror (default path, the ask's natural read)", km))
    for nm, st in stops.items():
        print("  %-92s %d" % ("stop: " + nm, kept(st, figs)))
    print("  %-92s %d  (control, figures.json reproduced)" % ("full includer", kf))

    n = 12 + CHART + n_fy
    kc_all = ksp + CHART + kc
    km_all = msp + CHART_OFF + km
    c, s, p = pair(kc_all, km_all, n)
    print("\nthe sheet's formula (38, 7, 55 over %d ask criteria: 12 spreads, %d chart, %d FY2026; r = 5):" % (
        n, CHART, n_fy))
    print("  cracker keeps %d (%d spreads, %d chart, %d FY2026): %.1f" % (kc_all, ksp, CHART, kc, c))
    print("  mirror keeps %d (%d spreads, %d chart, %d FY2026): %.1f" % (km_all, msp, CHART_OFF, km, s))
    print("  pair %.1f" % p)
    km_b = msp + CHART_OFF + kc
    print("  if the mirror runs the cracker's ask path (the ask needs nothing from the call): mirror %.1f, pair %.1f" % (
        pair(kc_all, km_b, n)[1], pair(kc_all, km_b, n)[2]))
    print("  two careful responses on the call: %.1f each" % c)
    print("\nCracker keeps: %d of %d FY2026 figures" % (kc, n_fy))
    print("Mirror leakage: %.1f per cent of ask weight (%.1f if the mirror runs the battery on the ask)" % (
        100.0 * km_all / n, 100.0 * km_b / n))
    print("Pair ceiling: %.1f (the sheet's formula on the measured keeps; %.1f with the mirror on the cracker's ask "
          "path)" % (p, pair(kc_all, km_b, n)[2]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
