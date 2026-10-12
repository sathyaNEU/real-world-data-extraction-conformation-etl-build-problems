"""The main call's declared row population and its figures, as a frozen reference.

`snapshot(target, g, L, bt)` digests, from the files alone, every row the main call reads (Brightwater's 2024
referred services and professional services, the acquired practices' physicians' referrals in both extracts, those
members' eligibility spans) and the reference files and documents it reads whole, and collects the main-call
figures. `main_call_ref.json` holds the snapshot of the built main call, written once before the ask-layer pass;
checks.py asserts the current build reproduces it exactly, so an ask-layer pass cannot move the call.

    python3 maincall.py <target>     # rewrite the reference from a built pack (only when the call itself changes)
"""
import hashlib
import json
import os
import re
import sys

import pandas as pd
import pdfplumber

import golden as G
import pack as PK

REF = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main_call_ref.json")
WHOLE = ("tiers", "register", "reassign", "facdir", "medicare", "exhibit", "prodref", "fachist")
DOCS = ("ohccr_rule_4_preliminary_review.pdf", "N25-014_notice_of_material_change.pdf")


def _digest(lines):
    h = hashlib.sha256()
    for r in sorted(lines):
        h.update((r + "\n").encode())
    return h.hexdigest()


def _file_digest(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def population(target):
    rd = lambda k: pd.read_csv(os.path.join(target, PK.FILES[k]), dtype=str, keep_default_na=False)
    with pdfplumber.open(os.path.join(target, "N25-014_notice_of_material_change.pdf")) as pdf:
        text = " ".join(pg.extract_text() or "" for pg in pdf.pages)
    bmg_tin = re.search(r"Brightwater's number\s*\((\d{2}-\d{7})\)", text).group(1)
    ra = rd("reassign")
    bmg = set(ra.loc[ra["billing_tin"] == bmg_tin, "npi"])
    hist = rd("fachist")
    acq = set(hist["REF_NPI"])
    f24 = rd("fac24")
    p24 = rd("prof24")
    el = rd("elig")
    fmain = f24[f24["referring_provider_npi"].isin(bmg | acq)]
    pmain = p24[p24["billing_provider_tin"] == bmg_tin]
    members = set(fmain["member_id"]) | set(pmain["member_id"]) | set(hist["MEMBER_ID"])
    emain = el[el["member_id"].isin(members)]
    out = {}
    for name, df in (("fac24_main", fmain), ("prof24_main", pmain), ("elig_main", emain)):
        out[name] = [len(df), _digest(["\t".join(r) for r in df.astype(str).itertuples(index=False, name=None)])]
    for k in WHOLE:
        out[k] = _file_digest(os.path.join(target, PK.FILES[k]))
    for d in DOCS:
        out[d] = _file_digest(os.path.join(target, d))
    return out


def figures(g, L, bt):
    r = lambda x: round(float(x), 6)
    return {"total": r(g["total"]), "P": r(g["P"]), "referred": r(g["referred"]),
            "fam": {k: r(v) for k, v in sorted(g["fam"].items())}, "c1": g["c1"], "c2": g["c2"],
            "fit": {m: {k: r(v) for k, v in sorted(d.items())} for m, d in sorted(g["fit"].items())},
            "rungs": {k: r(v) for k, v in sorted(L["rungs"].items())},
            "grid": {"|".join(k): r(v) for k, v in sorted(L["grid"].items())},
            "backtest": {k: r(v[0]) for k, v in sorted(bt.items())},
            "n_prof": g["n_prof"], "n_ref": g["n_ref"], "n_elig": g["n_elig"], "call": g["call"]}


def snapshot(target, g, L, bt):
    return {"population": population(target), "figures": figures(g, L, bt)}


def load_ref():
    return json.load(open(REF, encoding="utf-8"))


if __name__ == "__main__":
    tgt = sys.argv[1]
    g = G.compute(tgt)
    L = G.ladder(tgt, g)
    bt = G.backtest(g["hist"])
    snap = snapshot(tgt, g, L, bt)
    with open(REF, "w", encoding="utf-8") as fh:
        json.dump(snap, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print("wrote", REF, snap["figures"]["total"], snap["population"]["fac24_main"][0])
