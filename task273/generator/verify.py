"""task273 architecture 4: the independent verifier. Reads only the shipped pack (the calling rules from the
methods report's own text) and recomputes the panel, every carrier frequency and the programme's couples."""
from __future__ import annotations

import csv
import json
import os
import re
import subprocess
from collections import defaultdict
from datetime import date

import numpy as np
from openpyxl import load_workbook
from scipy.stats import binom

HERE = os.path.dirname(os.path.abspath(__file__))
CENSUS = date(2026, 11, 1)


def _f(target, key):
    return os.path.join(target, [f for f in os.listdir(target) if key in f][0])


def rules(target):
    txt = subprocess.run(["pdftotext", _f(target, "methods"), "-"], capture_output=True, text=True).stdout
    txt = re.sub(r"\s+", " ", txt)
    found = re.findall(r"at least (\d+) reads carrying the alternate allele, making up at least (\d+) per cent", txt)
    assert len(found) == 2, found
    return {1: (int(found[0][0]), int(found[0][1]) / 100), 2: (int(found[1][0]), int(found[1][1]) / 100)}


def run(target, golden, quiet=False):
    F = json.load(open(os.path.join(HERE, "figures.json")))
    R = rules(target)
    ok = True
    # cohort
    cohort, phase_of, area_of = {}, {}, {}
    for r in csv.DictReader(open(_f(target, "member_register"))):
        released = r["genotype_status"] == "Released"
        active = r["consent_status"] == "Active" or date.fromisoformat(r["consent_status_date"]) > CENSUS
        phase_of[r["sample_id"]] = int(r["phase"])
        area_of[r["sample_id"]] = r["recruitment_area"]
        if released and active:
            cohort[r["sample_id"]] = int(r["phase"])
    # register on the census date
    wb = load_workbook(_f(target, "variant_register"), read_only=True)
    reg = list(wb["Register"].iter_rows(values_only=True))
    rh = reg[0]
    sites = [dict(zip(rh, x)) for x in reg[1:]]
    hist = list(wb["Change history"].iter_rows(values_only=True))
    hh = hist[0]
    klass = {s["site_id"]: s["classification"] for s in sites}
    since = {s["site_id"]: str(s["classified_on"])[:10] for s in sites}
    changes = defaultdict(list)
    for x in hist[1:]:
        h = dict(zip(hh, x))
        changes[h["site_id"]].append((str(h["effective_on"])[:10], h["to_class"]))
    def on_date(sid, day):
        if changes[sid]:
            c = None
            for d_, to in sorted(changes[sid]):
                if d_ <= day:
                    c = to
            return c
        return klass[sid] if since[sid] <= day else None

    def on_census(sid):
        return on_date(sid, CENSUS.isoformat())
    by_name = {(s["gene"], s["hgvs_c"]): s["site_id"] for s in sites}
    plp = {s["site_id"]: s["gene"] for s in sites if on_census(s["site_id"]) in ("Pathogenic", "Likely pathogenic")}
    k37 = {(str(s["chrom"]), int(s["grch37_pos"]), s["ref"], s["alt"]): s["site_id"] for s in sites}
    k38 = {(str(s["chrom"]), int(s["grch38_pos"]), s["ref"], s["alt"]): s["site_id"] for s in sites}
    # calls
    called = defaultdict(set)
    for ph, key, keymap in ((1, "phase1", k37), (2, "phase2", k38)):
        for r in csv.DictReader(open(_f(target, key)), delimiter="\t"):
            sid = keymap[(r["chrom"].replace("chr", ""), int(r["pos"]), r["ref"], r["alt"])]
            called[sid].add(r["sample_id"])
    # depth
    with open(_f(target, "depth")) as fh:
        rd = csv.reader(fh)
        head = next(rd)
        rows = [r for r in rd if r[0] in cohort]
    samples = [r[0] for r in rows]
    dep = np.array([[int(x) for x in r[1:]] for r in rows])
    col = {sid: i for i, sid in enumerate(head[1:])}
    phase = np.array([cohort[s] for s in samples])
    N = len(samples)
    def sens(d, ph):
        k, f = R[ph]
        need = np.maximum(k, np.ceil(f * d - 1e-9)).astype(int)
        return binom.sf(need - 1, d, 0.5)
    freq = defaultdict(float)
    for sid, gene in plp.items():
        d = dep[:, col[sid]]
        c = np.array([s in called[sid] for s in samples])
        for ph in (1, 2):
            m = phase == ph
            s_ = sens(d[m], ph)
            freq[gene] += c[m].sum() / s_.sum() * m.sum()
    freq = {g: v / N for g, v in freq.items()}
    for g in F["freq_per_1000"]:
        v = int(np.floor(freq.get(g, 0) * 1000 + 0.5))
        if v != F["freq_per_1000"][g]:
            ok = False
            print("VERIFY freq %s %s against %s" % (g, v, F["freq_per_1000"][g]))
    panel = sorted(g for g, v in freq.items() if v >= 1 / 200)
    if panel != sorted(F["call"]["panel"]) or N != F["cohort"]:
        ok = False
        print("VERIFY panel or cohort", panel, N)
    # the programme's couples
    by_couple = defaultdict(list)
    for r in csv.DictReader(open(_f(target, "ccsp_results"))):
        by_couple[r["couple_ref"]].append(r)
    out = defaultdict(set)
    for cpl, rs in by_couple.items():
        dates = [r["result_authorised"] for r in rs if r["result_authorised"]]
        if not dates:
            continue
        rep = max(dates)
        half = "H1" if "2025-04-01" <= rep <= "2025-09-30" else ("H2" if "2025-10-01" <= rep <= "2026-03-31" else None)
        if half is None:
            continue
        for r in rs:
            if not r["gene"]:
                continue
            # policy 4.3: the class the register gave the variant on the day the result was authorised
            k = on_date(by_name[(r["gene"], r["hgvs_c"])], r["result_authorised"])
            if k in ("Pathogenic", "Likely pathogenic"):
                out[(half, r["gene"])].add(cpl)
    for h in ("H1", "H2"):
        for g, v in F["ask_b"][h].items():
            if len(out[(h, g)]) != v:
                ok = False
                print("VERIFY ask_b %s %s %d against %d" % (h, g, len(out[(h, g)]), v))
    print("verify: %s (cohort %d, panel %d, %d frequencies, %d couple figures)" % (
        "PASS" if ok else "FAIL", N, len(panel), len(F["freq_per_1000"]), 2 * len(F["ask_b"]["H1"])))
    return ok
