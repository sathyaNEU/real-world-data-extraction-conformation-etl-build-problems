"""task458 ask layer against the careful solver's routes, on the cut pack.

    python3 task458/generator/ceiling.py [pack]

pack is target.zip (the default, the archive that ships) or a folder holding the pack's files. The script reads only
the pack and generator/figures.json, modifies nothing and never runs inside the build.

Every route is a complete pipeline over the cut pack, scored figure by figure against figures.json; a figure is kept
only when it is exact at the prompt's rounding (members and counts exactly, dollars to the whole dollar).

The calls. The cracker lands the call: NPPES on 1 November 2026 (the monthly file updated record by record by the weekly
files through that day), NP-31 2.6 and 2.7's practising prescribers, persons by client identifier in the county and group
of the span covering the last enrolled day, final claim versions, the Appendix A codes in any position, and each
identified member counted as 1 over the share of the full-year members identified within the member's own months
enrolled. The mirror stops at the default path: the full-year members' prevalence carried to every member, eligibility
group by group (rung 3), which designates six counties.

The asks, as the prompt words them, block 4 of submission.md less blocks 1 and 2: the four counties outside the
critical components (Benton, Chelan, Kittitas, Walla Walla) with their practising prescribers and need counts, the
scorecard's forty quarterly figures (Ask A: net fee-for-service payments for services behavioral-health prescribers
rendered to each county's adult members, by the quarter of the service date) and the conformed file's adult members and
Ask A's payments by county and eligibility group. Each figure carries one share of the 55, as the ask sheet prices it.
Ask A's device (D6, the claim's paid amount repeated on each of its lines) is the battery's header-to-items check: the
script prints what that check finds in the claims file before any payment is summed.

The cracker takes every ask on its natural read with the whole hygiene battery run first (supplemental-stumping 1.1c)
and every filed rule executed as worded; the mirror takes the asks on the same natural read without the battery; the
full includer handles every device and has to give back figures.json exactly, the route code's control (exit 1 when it
does not). The pair is the sheet's formula: 38 recommendation and components, 7 instruction following, 55 asks; a
response off the call keeps r = 5 of the 38."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
REC, INS, ASK, OFF = 38.0, 7.0, 55.0, 5.0
D = dt.date
W0, W1 = D(2025, 7, 1), D(2026, 6, 30)
NAMES = {"53001": "Adams", "53005": "Benton", "53007": "Chelan", "53017": "Douglas", "53021": "Franklin", "53025": "Grant",
         "53037": "Kittitas", "53047": "Okanogan", "53071": "Walla Walla", "53077": "Yakima"}
COUNTIES = sorted(NAMES.values())
CRITICAL = ("Adams", "Douglas", "Franklin", "Grant", "Okanogan", "Yakima")      # submission.md block 2's six counties
GROUPS = ["SSI-DIS", "ADULT-EXP", "PARENT-CR", "AGED-65"]
QUARTERS = [("2025 Q3", D(2025, 7, 1), D(2025, 9, 30)), ("2025 Q4", D(2025, 10, 1), D(2025, 12, 31)),
            ("2026 Q1", D(2026, 1, 1), D(2026, 3, 31)), ("2026 Q2", D(2026, 4, 1), D(2026, 6, 30))]
BH = {"2084P0800X", "2084P0804X", "2084P0802X", "2084P0805X", "2084A0401X", "207QA0401X", "207RA0401X", "363LP0808X",
      "364SP0808X"}
VISIT = {"99202", "99203", "99204", "99205", "99211", "99212", "99213", "99214", "99215", "90791", "90792"}
SMI = {x.replace(".", "") for x in (
    "F20.0 F20.1 F20.2 F20.3 F20.5 F20.81 F20.89 F20.9 F21 F22 F25.0 F25.1 F25.8 F25.9 F28 F29 F31.0 F31.10 F31.11 "
    "F31.12 F31.13 F31.2 F31.30 F31.31 F31.32 F31.4 F31.5 F31.60 F31.61 F31.62 F31.63 F31.64 F31.70 F31.71 F31.72 "
    "F31.73 F31.74 F31.75 F31.76 F31.77 F31.78 F31.81 F31.89 F31.9 F32.3 F33.3").split()}
OUD_PREFIX = ("F1110", "F1111", "F1112", "F1113", "F1114", "F1115", "F1118", "F1119", "F1120", "F1121", "F1122", "F1123",
              "F1124", "F1125", "F1128", "F1129")
THRESH = (16.5, 23.0, 0.68)
FILES = {"claims": "bh_claims_encounters_dos_2025-07-01_2026-06-30.csv",
         "spans": "enrollment_spans_2025-07-01_2026-06-30.csv",
         "nppes": ["npidata_pfile_wa_20050523-20261011.csv", "npidata_pfile_wa_20261012-20261018.csv",
                   "npidata_pfile_wa_20261019-20261025.csv", "npidata_pfile_wa_20261026-20261101.csv"],
         "zip": "ZIP_COUNTY_062026.xlsx"}


def pack_dir(arg):
    """The pack as a folder: target.zip unpacked into a scratch folder (removed after), or the folder given."""
    src = arg or os.path.join(TASK, "target.zip")
    if os.path.isdir(src):
        files = sorted(os.listdir(src))
        h = hashlib.sha256("".join(hashlib.sha256(open(os.path.join(src, f), "rb").read()).hexdigest()
                                   for f in files).encode()).hexdigest()
        return src, None, "folder %s (%d files, sha256 of the file digests %s)" % (src, len(files), h[:16])
    tmp = tempfile.mkdtemp(prefix="ceiling458-")
    with zipfile.ZipFile(src) as z:
        z.extractall(tmp)
    md5 = hashlib.md5(open(src, "rb").read()).hexdigest()
    return tmp, tmp, "%s (%d files, md5 %s)" % (src, len(os.listdir(tmp)), md5)


# ------------------------------------------------------------------ the conformance every route shares

def read(folder):
    t = lambda f: os.path.join(folder, f)
    rec, live = {}, {}
    for f in FILES["nppes"]:
        for r in pd.read_csv(t(f), dtype=str, keep_default_na=False).to_dict("records"):
            rec[r["NPI"]] = r
            if r["Entity Type Code"] in ("1", "2"):
                live[r["NPI"]] = r
    z = pd.read_excel(t(FILES["zip"]), dtype={"ZIP": str, "COUNTY": str})
    zc = z.sort_values(["ZIP", "BUS_RATIO"], ascending=[True, False]).drop_duplicates("ZIP").set_index("ZIP")["COUNTY"]

    def prim(r):
        for k in range(1, 5):
            if r["Healthcare Provider Primary Taxonomy Switch_%d" % k] == "Y":
                return r["Healthcare Provider Taxonomy Code_%d" % k]
        return ""
    bh, place = set(), {}
    for npi, r in rec.items():
        src = r if r["Entity Type Code"] else live.get(npi)      # NP-31 2.6: a deactivated NPI's last record
        if src is None or src["Entity Type Code"] != "1" or prim(src) not in BH:
            continue
        bh.add(npi)
        if r["Entity Type Code"] and r["Provider Business Practice Location Address State Name"] == "WA":
            place[npi] = zc.get(r["Provider Business Practice Location Address Postal Code"][:5])
    s = pd.read_csv(t(FILES["spans"]), dtype=str, keep_default_na=False)
    s["a"] = s["span_start_dt"].map(lambda x: max(D.fromisoformat(x), W0))
    s["b"] = s["span_end_dt"].map(lambda x: min(D.fromisoformat(x) if x else W1, W1))
    s = s[s["a"] <= s["b"]]
    per = {}
    for r in s.to_dict("records"):
        p = per.setdefault(r["client_id"], {"months": set(), "end": None, "start": None})
        y, m = r["a"].year, r["a"].month
        while (y, m) <= (r["b"].year, r["b"].month):
            p["months"].add((y, m))
            y, m = (y + 1, 1) if m == 12 else (y, m + 1)
        if p["end"] is None or (r["b"], r["a"]) > (p["end"], p["start"]):
            p["end"], p["start"], p["fips"], p["grp"] = r["b"], r["a"], r["res_county_fips"], r["elig_group_cd"]
    mem = pd.DataFrame([{"cid": k, "county": NAMES[v["fips"]], "grp": v["grp"], "m": len(v["months"]),
                         "full": len(v["months"]) == 12} for k, v in per.items()]).set_index("cid")
    to_cid = dict(zip(s["mbr_id"], s["client_id"]))
    c = pd.read_csv(t(FILES["claims"]), dtype=str, keep_default_na=False)
    c["cid"] = c["mbr_id"].map(to_cid)
    return {"bh": bh, "place": place, "mem": mem, "claims": c, "to_cid": to_cid}


def final(c):
    """NP-31 2.4 and the battery's latest-version rule: a replaced claim and a voided claim drop with the void."""
    gone = set(c.loc[c["clm_freq_cd"].isin(["7", "8"]), "orig_icn"])
    return c[(c["clm_freq_cd"] != "8") & ~c["clm_icn"].isin(gone)].copy()


def the_call(L, route):
    """The designation a route files: 'window' (the golden's estimate) or 'full_year_group' (rung 3)."""
    mem = L["mem"].copy()
    c = final(L["claims"])
    dx = c[["dx_cd_1", "dx_cd_2", "dx_cd_3", "dx_cd_4"]]
    hs = dx.isin(SMI).any(axis=1)
    ho = dx.apply(lambda col: col.str.startswith(OUD_PREFIX)).any(axis=1)
    mon = (c["svc_from_dt"].str[:4].astype(int) - 2025) * 12 + c["svc_from_dt"].str[5:7].astype(int) - 6
    seen = set(c.loc[c["proc_cd"].isin(VISIT) & c["rendering_npi"].isin(L["bh"]), "cid"])
    rendering = set(c["rendering_npi"])
    pres = {k: 0 for k in COUNTIES}
    for npi in L["bh"]:
        if npi in L["place"] and L["place"][npi] in NAMES and npi in rendering:
            pres[NAMES[L["place"][npi]]] += 1
    est = {}
    for cond, h in (("smi", hs), ("oud", ho)):
        mem[cond] = mem.index.isin(set(c.loc[h, "cid"]))
        first = mon[h].groupby(c.loc[h, "cid"]).min()
        if route == "window":
            f = first.reindex(mem.index[mem["full"] & mem[cond]])
            share = [float((f <= k).mean()) for k in range(1, 13)]
            w = np.where(mem[cond], 1.0 / np.array(share)[mem["m"].values - 1], 0.0)
            est[cond] = pd.Series(w, index=mem.index).groupby(mem["county"]).sum()
        else:
            out = {}
            for cty, g in mem.groupby("county"):
                tot = 0.0
                for grp, gg in g.groupby("grp"):
                    fy = gg[gg["full"]]
                    tot += (fy[cond].mean() if len(fy) else 0.0) * len(gg)
                out[cty] = tot
            est[cond] = pd.Series(out)
    seen_smi = (mem["smi"] & mem.index.isin(seen)).groupby(mem["county"]).sum()
    rows = {}
    for cty in COUNTIES:
        e1, e2 = float(est["smi"][cty]), float(est["oud"][cty])
        s1, s2, s3 = pres[cty] / e1 * 1000, pres[cty] / e2 * 1000, float(seen_smi.get(cty, 0)) / e1
        fails = int(s1 < THRESH[0]) + int(s2 < THRESH[1]) + int(s3 < THRESH[2])
        rows[cty] = {"prescribers": pres[cty], "smi": int(round(e1 / 10.0)) * 10, "oud": int(round(e2 / 10.0)) * 10,
                     "meets": (s1 >= THRESH[0], s2 >= THRESH[1], s3 >= THRESH[2]), "designated": fails >= 2}
    return rows, mem


# ------------------------------------------------------------------ the asks as they stand: the payments

def battery(c):
    """The hygiene battery on the claims, before any payment is summed: (check, finding, detail)."""
    out = []
    dup = int(c.duplicated().sum())
    out.append(("exact duplicate rows", dup == 0, "%d" % dup))
    key = c[["clm_icn", "clm_line_num"]].duplicated().sum()
    out.append(("one row per claim and line", key == 0, "%d repeats" % key))
    adj = c[c["clm_freq_cd"] != "1"]
    out.append(("each replacement and void names a claim in the extract (latest version kept, void removes its claim)",
                adj["orig_icn"].isin(set(c["clm_icn"])).all(), "%d adjustments" % len(adj)))
    ffs = c[c["fin_arrangement_cd"] == "FFS"]
    multi = ffs.groupby("clm_icn").filter(lambda g: len(g) > 1)
    same = multi.groupby("clm_icn")["paid_amt"].nunique().eq(1)
    over = (ffs["paid_amt"].astype(float) > ffs["billed_amt"].astype(float) + 0.005).sum()
    repeated = bool(len(same)) and bool(same.all()) and over > 0
    out.append(("a header amount repeated on its item rows (one paid amount on every line of a claim, lines paid above "
                "their own charge)", not repeated,
                "%d multi-line claims, %d with one paid amount on every line; %d lines paid above their charge" % (
                    len(same), int(same.sum()), int(over))))
    return out, repeated


def payments(L, mem, once=True, versions="final", by="rendering_npi"):
    c = final(L["claims"]) if versions == "final" else L["claims"][L["claims"]["clm_freq_cd"] != "8"].copy()
    ffs = c[c["fin_arrangement_cd"] == "FFS"]
    keep = set(ffs.loc[ffs[by].isin(L["bh"]), "clm_icn"])
    d = ffs[ffs["clm_icn"].isin(keep)].sort_values(["clm_icn", "clm_line_num"])
    if once:
        d = d.drop_duplicates("clm_icn")
    d = d.assign(county=d["cid"].map(mem["county"]), grp=d["cid"].map(mem["grp"]), paid=d["paid_amt"].astype(float),
                 dos=d["svc_from_dt"].map(D.fromisoformat))
    q = {(cty, qn): int(round(float(d.loc[(d["county"] == cty) & (d["dos"] >= a) & (d["dos"] <= b), "paid"].sum())))
         for cty in COUNTIES for qn, a, b in QUARTERS}
    g = {(cty, grp): int(round(float(d.loc[(d["county"] == cty) & (d["grp"] == grp), "paid"].sum())))
         for cty in COUNTIES for grp in GROUPS}
    return q, g


def members_by_group(mem):
    return {(cty, grp): int(((mem["county"] == cty) & (mem["grp"] == grp)).sum()) for cty in COUNTIES for grp in GROUPS}


def score(call_rows, q, g, mem_g, gold):
    """Figures kept, ask block by ask block: (kept, of)."""
    out = {}
    four = [c for c in COUNTIES if c not in CRITICAL]
    out["the four counties' prescribers and need counts"] = (
        sum((call_rows[c]["prescribers"] == gold["counties"][c]["prescribers"]) + (call_rows[c]["smi"] == gold["counties"][c]["smi"])
            + (call_rows[c]["oud"] == gold["counties"][c]["oud"]) for c in four), 3 * len(four))
    out["scorecard: the quarterly figures"] = (sum(q[(c, qn)] == gold["payments"][c][qn] for c in COUNTIES
                                                   for qn, _, _ in QUARTERS), 40)
    out["conformed: adult members by county and group"] = (
        sum(mem_g[(c, grp)] == gold["conformed"]["%s|%s" % (c, grp)]["members"] for c in COUNTIES for grp in GROUPS), 40)
    out["conformed: the second quantity by county and group"] = (
        sum(g[(c, grp)] == gold["conformed"]["%s|%s" % (c, grp)]["paid"] for c in COUNTIES for grp in GROUPS), 40)
    return out


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
    gold = json.load(open(os.path.join(HERE, "figures.json")))
    L = read(folder)
    crow, cmem = the_call(L, "window")
    mrow, mmem = the_call(L, "full_year_group")
    c_des = [c for c in COUNTIES if crow[c]["designated"]]
    m_des = [c for c in COUNTIES if mrow[c]["designated"]]
    on_call = c_des == gold["designated"]
    off_call = m_des != gold["designated"]
    print("cracker's call (each identified member over the full-year share at its own months): designates %s (%s)" % (
        ", ".join(c_des), "lands the golden" if on_call else "MISSES"))
    print("mirror's call (rung 3, the full-year prevalence carried group by group): designates %s (%s)" % (
        ", ".join(m_des), "off the call" if off_call else "ON THE CALL"))
    if not (on_call and off_call):
        print("the rows below assume the cracker on the call and the mirror off it: they are not")
        return 1
    print("\nthe cracker's hygiene battery on the claims:")
    bat, repeated = battery(L["claims"])
    for check, clean, detail in bat:
        print("  %-5s %s (%s)" % ("ok" if clean else "FOUND", check, detail))
    mem_g = members_by_group(cmem)
    routes = {
        "cracker (the battery run: final versions, the rendering NPI, each claim's paid amount once)":
            (crow, payments(L, cmem, once=repeated)),
        "mirror (rung 3; the natural read without the battery: every line's paid amount summed)":
            (mrow, payments(L, mmem, once=False)),
        "full includer (control)": (crow, payments(L, cmem, once=True)),
        "stop: every line summed, on the call": (crow, payments(L, cmem, once=False)),
        "stop: every version, on the call": (crow, payments(L, cmem, once=True, versions="all")),
        "stop: the billing provider's taxonomy, on the call": (crow, payments(L, cmem, once=True, by="billing_npi")),
        "mirror with the battery (rung 3, the cracker's ask path)": (mrow, payments(L, mmem, once=True)),
    }
    res = {}
    for nm, (rows, (q, g)) in routes.items():
        res[nm] = score(rows, q, g, members_by_group(cmem if rows is crow else mmem), gold)
    n = sum(v[1] for v in next(iter(res.values())).values())
    full = res["full includer (control)"]
    if sum(v[0] for v in full.values()) != n:
        print("CONTROL FAILED: the full includer keeps %d of %d, the route code does not reproduce figures.json" % (
            sum(v[0] for v in full.values()), n))
        return 1
    print("\nper route, ask figures kept (of %d):" % n)
    blocks = list(full)
    for nm, sc in res.items():
        print("  %-92s %3d   %s" % (nm, sum(v[0] for v in sc.values()), "; ".join("%d/%d" % sc[b] for b in blocks)))
    print("  (blocks: %s)" % "; ".join(blocks))
    kc = sum(v[0] for v in res[next(k for k in res if k.startswith("cracker"))].values())
    km = sum(v[0] for v in res[next(k for k in res if k.startswith("mirror (rung 3; the natural"))].values())
    km_b = sum(v[0] for v in res["mirror with the battery (rung 3, the cracker's ask path)"].values())
    c, s, p = pair(kc, km, n)
    print("\nthe sheet's formula (38, 7, 55 over the %d ask figures; r = 5): cracker %.1f, mirror %.1f, pair %.1f" % (n, c, s, p))
    print("  if the mirror runs the battery too: pair %.1f" % pair(kc, km_b, n)[2])
    print("  two careful responses on the call (both the cracker): %.1f" % c)
    print("\nCracker keeps: %d of %d ask figures" % (kc, n))
    print("Mirror leakage: %.1f per cent of ask weight" % (100.0 * km / n))
    print("Pair ceiling: %.1f (the sheet's formula on the measured keeps)" % max(p, pair(kc, km_b, n)[2]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
