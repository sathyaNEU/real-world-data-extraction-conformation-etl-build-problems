"""The main call's declared row population and its figures, as a frozen reference.

`snapshot(target, g)` digests, from the files alone, every row the main call reads on the columns it reads
(DESIGN_NOTE, ask sheet: the declared population) and collects the main-call figures. `main_call_ref.json`
holds the snapshot of the loop 2 main call, written once from the first pack that asserted it; checks.py asserts
the current build reproduces it exactly, so an ask-layer pass cannot move the call.
"""
import hashlib
import json
import os

import pandas as pd

import golden as G

REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main_call_ref.json")
FIL_COLS = ["CIK", "PERIODOFREPORT", "REPORTCALENDARORQUARTER", "FILING_DATE", "SUBMISSIONTYPE", "REPORTTYPE",
            "ISAMENDMENT", "AMENDMENTNO", "AMENDMENTTYPE"]
LINE_COLS = ["CUSIP", "SSHPRNAMT", "SSHPRNAMTTYPE", "PUTCALL", "TITLEOFCLASS"]
FIGS = ("dec_io", "sep_io", "jun_io", "type_change", "type_change_allsec", "type_change3", "dec_onfile_shares",
        "sponsor_change_name",
        "backtest", "flag")


def _digest(rows):
    h = hashlib.sha256()
    for r in sorted(rows):
        h.update(("\t".join(str(x) for x in r) + "\n").encode())
    return h.hexdigest()


def population(target, cusips):
    f, inf = G.load(target)
    reg = G.register(target)
    mtype = dict(zip(reg.cik, reg.manager_type))
    P = G.PERIOD
    q4 = f[(f.period == P["Q4"]) & (f.fdate <= G.EXTRACT)]
    hold3 = set(f[(f.period == P["Q3"]) & (f.REPORTTYPE != "13F NOTICE")].CIK)
    due = hold3 - set(q4.CIK)
    q3due = f[(f.period == P["Q3"]) & f.CIK.isin(due)]
    types = {mtype[k] for k in due}
    hold = set(f[f.period.isin([P["Q3"], P["Q4"]]) & (f.REPORTTYPE != "13F NOTICE")].CIK)
    peers = {k for k in hold if mtype[k] in types}
    pf = f[f.period.isin([P["Q2"], P["Q3"], P["Q4"]]) & f.CIK.isin(peers)]
    fil = f.set_index("ACCESSION_NUMBER")

    def rows(accs, twelve):
        e = inf[inf.ACCESSION_NUMBER.isin(set(accs))]
        if twelve:
            e = e[e.CUSIP.isin(cusips) & (e.PUTCALL == "") & (e.SSHPRNAMTTYPE == "SH")]
        out = []
        for r in e.itertuples(index=False):
            a = fil.loc[r.ACCESSION_NUMBER]
            out.append(tuple(str(a[c]) for c in FIL_COLS) + tuple(str(getattr(r, c)) for c in LINE_COLS))
        return out

    pops = {"dec_twelve": rows(q4.ACCESSION_NUMBER, True), "due_sep_twelve": rows(q3due.ACCESSION_NUMBER, True),
            "peer_all": rows(pf.ACCESSION_NUMBER, False)}
    filings = [tuple(str(r[c]) for c in FIL_COLS) for _, r in pd.concat([q4, q3due, pf]).drop_duplicates("ACCESSION_NUMBER").iterrows()]
    pops["filings"] = filings
    pops["register"] = [(int(k), t) for k, t in mtype.items() if t in types]
    sub = pd.read_csv(os.path.join(target, "fsds_cover_extract", "sub.txt"), sep="\t", dtype=str)
    num = pd.read_csv(os.path.join(target, "fsds_cover_extract", "num.txt"), sep="\t", dtype=str)
    n = num[num.tag == "EntityCommonStockSharesOutstanding"].merge(sub[["adsh", "cik", "form"]], on="adsh")
    pops["counts"] = [(r.cik, r.form, r.ddate, r.value) for r in n.itertuples() if r.ddate <= "20221231"]
    return {k: dict(n=len(v), sha256=_digest(v)) for k, v in pops.items()}, due


def figures(g):
    out = {}
    for k in FIGS:
        v = g["backtest"] if k == "backtest" else g[k]
        out[k] = {str(a): (bool(b) if isinstance(b, (bool,)) or str(type(b)).endswith("bool_'>") else float(b)) for a, b in v.items()}
    out["rungs"] = {k: {c: float(x) for c, x in v.items()} for k, v in g["rungs"].items()}
    out["variants"] = {k: {c: float(x) for c, x in v.items()} for k, v in g["dec_variants"].items()}
    out["grid"] = {f"{a}|{b}": {c: float(x) for c, x in v.items()} for (a, b), v in g["grid"].items()}
    out["sponsor_stake_change"] = float(g["sponsor_stake_change"])
    out["due_ciks"] = [int(x) for x in g["due_ciks"]]
    return out


def snapshot(target, g):
    pops, due = population(target, g["cusips"])
    return {"populations": pops, "figures": figures(g)}


if __name__ == "__main__":
    import sys
    t = sys.argv[1]
    g = G.compute(t)
    with open(REF, "w", encoding="utf-8") as fh:
        json.dump(snapshot(t, g), fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("written", REF)
