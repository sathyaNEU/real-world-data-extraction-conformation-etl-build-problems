"""Build task135's evidence pack into <out>/ (default: task135/target), then metadata.json and target.zip."""
import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import world as W
import sim as SM
import book as BK
import tune as T
import grants as GR
import observe as O
import files as FL
import docs as D
import postprocess as PP
import officex as OX
import estimators as E

TASK = os.path.dirname(HERE)
REPO = os.path.dirname(TASK)
INDEX_YIELD = 0.0362          # the FTSE All-Share's dividend yield, for its total return in Fernside's report
SCRUB = os.path.join(REPO, ".claude/skills/reduce-house-fixes/scripts/scrub_producer_metadata.py")
MTIMES = {
    "val": (2026, 12, 2, 6, 44), "moves": (2026, 12, 2, 6, 44), "events": (2026, 12, 2, 6, 45), "ent": (2026, 12, 2, 6, 45),
    "static": (2026, 12, 2, 6, 45), "notes": (2026, 12, 2, 6, 46), "kest": (2026, 12, 2, 8, 15),
    "keyfacts": (2026, 9, 14, 11, 20), "cal": (2026, 12, 2, 9, 3), "policy": (2025, 12, 10, 9, 41),
    "proc": (2026, 10, 19, 16, 37), "budget": (2026, 11, 24, 17, 12), "reg": (2026, 12, 1, 8, 31),
    "inst": (2026, 12, 1, 8, 31), "pays": (2026, 12, 1, 8, 47), "index": (2026, 12, 2, 9, 10),
    "factsheets": (2026, 10, 16, 14, 2), "fernside": (2026, 10, 21, 10, 26),
}


def running_costs():
    rc = [(n, v + (W.RUNNING_ADJ if n == "Staff salaries" else 0)) for n, v in W.RUNNING_COSTS]
    return rc


def world():
    M, fp, B, X, dates, drift = T.build_world(W.MARKET_SEED, iters=3, keep_rows=True, start_total=W.START_TOTAL,
                                              knobs=W.BOOK_KNOBS)
    g, i = GR.make(W.GRANT_SEED, {"scale": W.GRANT_SCALE})
    p = GR.settle(g, i, W.GRANT_SEED, {})
    return M, fp, B, X, dates, g, i, p


# ------------------------------------------------------------------------------------------------ distractor figures

def month_ends(days):
    out = []
    for k, d in enumerate(days):
        if k + 1 == len(days) or days[k + 1].month != d.month:
            out.append(k)
    return out


def factsheet_figures(M, fp):
    days = M["days"]
    me = month_ends(days)
    idx = {d: k for k, d in enumerate(days)}
    out = {}
    meta = {"NAEF": (412.6, "3 April 2009", "FTSE World North America", 287,
                     [("Technology", 31.8), ("Financials", 13.2), ("Health care", 11.6), ("Consumer discretionary", 10.9),
                      ("Industrials", 9.9), ("Communication services", 8.4), ("Other", 14.2)]),
            "EUEF": (188.3, "3 April 2009", "FTSE World Europe ex UK", 96,
                     [("Financials", 21.4), ("Industrials", 18.7), ("Health care", 14.2), ("Consumer staples", 9.8),
                      ("Technology", 9.1), ("Consumer discretionary", 8.6), ("Other", 18.2)]),
            "JPEF": (121.7, "1 October 2012", "TOPIX", 118,
                     [("Industrials", 24.3), ("Consumer discretionary", 17.1), ("Technology", 14.8), ("Financials", 12.6),
                      ("Communication services", 8.2), ("Materials", 6.9), ("Other", 16.1)]),
            "GILT": (263.9, "3 April 2009", "FTSE Actuaries UK Conventional Gilts All Stocks", 41,
                     [("Up to 5 years", 27.5), ("5 to 10 years", 24.9), ("10 to 15 years", 14.1), ("Over 15 years", 31.6),
                      ("Cash", 1.9)]),
            "CORP": (204.4, "3 April 2009", "iBoxx GBP Non-Gilts", 236,
                     [("AAA", 6.2), ("AA", 15.8), ("A", 38.9), ("BBB", 36.4), ("Cash", 2.7)])}
    for f in W.FUNDS:
        acc = fp[f]["acc"]
        k26 = idx[dt.date(2026, 9, 30)]
        k25 = idx[dt.date(2025, 9, 30)]
        k24 = idx[dt.date(2024, 9, 30)]
        k23 = idx[dt.date(2023, 9, 29)]
        perf = [100 * (acc[k24] / acc[k23] - 1), 100 * (acc[k25] / acc[k24] - 1), 100 * (acc[k26] / acc[k25] - 1)]
        mk = [k for k in me if k23 <= k <= k26]
        mr = np.array([acc[b] / acc[a] - 1 for a, b in zip(mk[:-1], mk[1:])])
        size, launch, bench, n, sectors = meta[f]
        out[f] = dict(size_m=size, launch=launch, bench=bench, n=n, perf=perf, cum3=100 * (acc[k26] / acc[k23] - 1),
                      vol3=float(mr.std(ddof=1) * np.sqrt(12) * 100), sectors=sectors,
                      label="Sector breakdown (%)" if f in ("NAEF", "EUEF", "JPEF") else
                      ("Maturity breakdown (%)" if f == "GILT" else "Credit rating breakdown (%)"))
    return out


def fernside_figures(B, M, F):
    days = B.days
    r = B.r_mand
    idx = {d: k for k, d in enumerate(days)}

    def cum(a, b):
        return 100 * (np.prod(1 + r[idx[a]:idx[b]]) - 1)
    q = (dt.date(2026, 6, 30), dt.date(2026, 9, 30))
    ytd = (dt.date(2025, 12, 31), dt.date(2026, 9, 30))
    y1 = (dt.date(2025, 9, 30), dt.date(2026, 9, 30))
    ix = F["index"]
    s = ix[ix["index_name"] == "FTSE All-Share"].set_index("date")["close"]

    def icum(a, b):
        """the index's total return: the price index with its dividend yield accrued day by day"""
        return 100 * ((s[b.isoformat()] / s[a.isoformat()]) * (1 + INDEX_YIELD) ** ((b - a).days / 365.0) - 1)
    a, b = idx[y1[0]], idx[y1[1]]
    rp = r[a:b]
    lv = s.loc[y1[0].isoformat():y1[1].isoformat()].values
    ri = lv[1:] / lv[:-1] - 1
    n = min(len(rp), len(ri))
    beta = float(np.cov(rp[:n], ri[:n])[0, 1] / ri[:n].var(ddof=1))
    te = float((rp[:n] - ri[:n]).std(ddof=1) * np.sqrt(252) * 100)
    v = F["val"]
    v30 = v[(v["valuation_date"] == "2026-09-30") & (v["asset_class"].isin(["Equity - UK", "Cash"]))].copy()
    v30["market_value_gbp"] = v30["market_value_gbp"].astype(float)
    tot = v30["market_value_gbp"].sum()
    top = v30[v30["asset_class"] == "Equity - UK"].groupby("security_name")["market_value_gbp"].sum().sort_values(ascending=False)
    top = [(nm, 100 * x / tot) for nm, x in top.head(10).items()]
    # what the book did with the takeover cash between 21 July and the September rebalancing
    tk = sum(m[3] for m in B.moves if m[2] == "Takeover consideration")
    bought = sorted({m[5] for m in B.moves if m[2] == "Purchase" and dt.date(2026, 7, 21) <= m[0] <= dt.date(2026, 9, 30)})
    sep = {m[1]: m[2] for m in B.moves if m[0] == dt.date(2026, 9, 30) and m[2] in ("Contribution", "Withdrawal")}
    if bought:
        use = ("Part of it was invested in %s at the September rebalancing and the rest stays in the portfolio's cash."
               % " and ".join(B.info[c]["name"] for c in bought))
    elif set(sep.values()) == {"Withdrawal"}:
        use = ("It was held in the portfolio's cash until the September rebalancing and went to the trust with the "
               "quarterly transfer.")
    else:
        use = "It is held in the portfolio's cash."
    letter = [
        "The portfolio returned %.1f%% in the third quarter against %.1f%% for the FTSE All-Share. Over twelve months it "
        "returned %.1f%% against %.1f%% for the index." % (cum(*q), icum(*q), cum(*y1), icum(*y1)),
        "Glenrothes Distillers' scheme of arrangement completed on 21 July and the cash consideration, %s, was received "
        "the same day. %s" % ("GBP {:,.0f}".format(tk), use),
        "We continue to favour companies with strong balance sheets and growing dividends. Trading in the quarter was "
        "limited to the September rebalancing.",
    ]
    return dict(port=[cum(*q), cum(*ytd), cum(*y1)], index=[icum(*q), icum(*ytd), icum(*y1)],
                vol=[float(rp.std(ddof=1) * np.sqrt(252) * 100), float(ri.std(ddof=1) * np.sqrt(252) * 100)],
                beta=beta, te=te, top=top, letter=letter)


# ------------------------------------------------------------------------------------------------ the pack

def build(out):
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    O.fix_isins()
    M, fp, B, X, dates, g, i, p = world()
    F = FL.frames(M, fp, B, g, i, p, W.GRANT_SEED)
    pth = lambda k: os.path.join(out, FL.FILES[k])
    for k in ("val", "moves", "events", "ent", "static", "cal", "index", "reg", "inst", "pays"):
        FL.write_csv(F[k], pth(k), O.INDEX_HEAD if k == "index" else None)
    D.export_notes(pth("notes"), None)
    D.kestwick_xlsx(pth("kest"), F["kest"])
    D.key_facts_pdf(pth("keyfacts"))
    D.policy_pdf(pth("policy"))
    D.procedure_docx(pth("proc"))
    D.budget_xlsx(pth("budget"), running_costs(), W.CAPITAL_CHARGES)
    D.factsheets_pdf(pth("factsheets"), factsheet_figures(M, fp))
    D.fernside_pdf(pth("fernside"), fernside_figures(B, M, F))
    pdf_producers = {"keyfacts": ("Adobe PDF Library 17.0", (2026, 9, 14, 11, 20)),
                     "factsheets": ("Adobe PDF Library 17.0", (2026, 10, 16, 14, 2)),
                     "fernside": ("Microsoft: Print To PDF", (2026, 10, 21, 10, 26)),
                     "policy": ("Microsoft\xae Word for Microsoft 365", (2025, 12, 10, 9, 41))}
    for k, (prod, when) in pdf_producers.items():
        fix_pdf(pth(k), prod, dt.datetime(*when), "Microsoft\xae Word for Microsoft 365" if k == "policy" else "")
    for k in FL.FILES:
        ts = W.posix(dt.datetime(*MTIMES[k]))
        os.utime(pth(k), (ts, ts))
    return M, fp, B, F


def fix_pdf(path, producer, when, creator=""):
    """the PDF's producer and creator as the writing application leaves them, its dates in local time, a fixed id"""
    import re
    b = open(path, "rb").read()
    b = re.sub(rb"/Producer ?(?:\((?:[^()\\]|\\.)*\)|<[0-9A-Fa-f]*>)", b"/Producer (" + producer.encode("latin-1") + b")", b)
    b = re.sub(rb"/Creator ?(?:\((?:[^()\\]|\\.)*\)|<[0-9A-Fa-f]*>)", b"/Creator (" + creator.encode("latin-1") + b")", b)
    b = re.sub(rb"(\n%[\x80-\xff]{4})[^\n]*ReportLab[^\n]*", rb"\1", b)        # keep the binary marker, drop the writer
    b = re.sub(rb"\n% ReportLab generated PDF document[^\n]*", b"", b)
    open(path, "wb").write(b)
    fix_xref(path)
    PP.normalize_pdf(path, when)


def fix_xref(path):
    """rebuild the cross-reference offsets after an edit changed object lengths"""
    import re
    b = open(path, "rb").read()
    offs = {}
    for m in re.finditer(rb"(?m)^(\d+) 0 obj", b):
        offs[int(m.group(1))] = m.start()
    x = b.rfind(b"\nxref\n") + 1
    m = re.search(rb"xref\n0 (\d+)\n", b[x:])
    n = int(m.group(1))
    head = b[:x]
    body = b[x + m.end():]
    lines = body.split(b"\n")
    entries = lines[:n]
    rest = b"\n".join(lines[n:])
    new = [entries[0]]
    for k in range(1, n):
        e = entries[k]
        if e.endswith(b"n ") or e.endswith(b"n"):
            new.append(b"%010d 00000 n " % offs[k])
        else:
            new.append(e)
    out = head + b"xref\n0 %d\n" % n + b"\n".join(new) + b"\n" + rest
    out = re.sub(rb"startxref\s+\d+", b"startxref\n%d" % x, out)
    open(path, "wb").write(out)


def write_metadata():
    meta = {
        "task": "task135",
        "title": "The Wrexford Trust: the 2027 growth share under the investment policy's volatility cap",
        "domain": "Quantitative Finance",
        "subdomain": "volatility-derivatives-pricing",
        "objective": "Forecasting & Predictive Modeling",
        "as_of": "2026-12-02",
        "deliverables": ["growth_share_2027.xlsx", "income_cost_by_step_2027.svg"],
        "input_files": [{"path": FL.FILES[k], "format": FL.FILES[k].rsplit(".", 1)[1]} for k in sorted(FL.FILES, key=lambda k: FL.FILES[k])],
        "distractors": [FL.FILES[k] for k in FL.DISTRACTORS],
        "distractor_notes": {
            FL.FILES["index"]: "declared wrong-basis distractor: the benchmark indices, which investment policy 4.2 "
                               "refuses ('each measured from the holding's own prices')",
        },
        "provenance": "Fully constructed pack (dataset-generation section 2): every extract is generated by "
                      "task135/generator from a simulated market and a simulated book for a fictional English grant-making "
                      "charity; documents written for the fiction. Index names are used as benchmark labels only and the "
                      "levels are simulated; no real company's, fund's or charity's data.",
        "license": "Constructed data, released with the task (CC BY 4.0).",
        "created": "2026-10-12",
    }
    with open(os.path.join(TASK, "metadata.json"), "w") as f:
        json.dump(meta, f, indent=2)
        f.write("\n")


ZIP_TIME = (2026, 12, 2, 10, 30, 0)


def zip_target(src, path):
    import zipfile
    with zipfile.ZipFile(path, "w") as z:
        for name in sorted(os.listdir(src)):
            zi = zipfile.ZipInfo(name, date_time=ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.create_system = 3
            zi.external_attr = 0o644 << 16
            with open(os.path.join(src, name), "rb") as f:
                z.writestr(zi, f.read())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(TASK, "target"))
    ap.add_argument("--zip", default=None)
    a = ap.parse_args()
    build(a.out)
    if a.out == os.path.join(TASK, "target"):
        write_metadata()
        zip_target(a.out, os.path.join(TASK, "target.zip"))
    elif a.zip:
        zip_target(a.out, a.zip)
    print("built", a.out)
