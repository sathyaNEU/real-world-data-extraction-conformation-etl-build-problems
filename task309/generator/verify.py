"""Independent verifier: reads only the shipped bundle (target.zip, or an unzipped target dir) and submission.md,
recomputes every graded figure with its own code, and fails on any disagreement or on a figure printed at the
wrong precision.

    python3 task309/generator/verify.py <target.zip | target dir> <submission.md>
"""
import io
import os
import re
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd
from pypdf import PdfReader

KTS = 1.150779
STD = {"ROAD": "RD", "DRIVE": "DR", "LANE": "LN", "STREET": "ST", "COURT": "CT", "AVENUE": "AVE", "CIRCLE": "CIR"}


def find(d, pat):
    hits = [f for f in os.listdir(d) if re.search(pat, f)]
    assert len(hits) == 1, (pat, hits)
    return os.path.join(d, hits[0])


def addr(a):
    t = [STD.get(x, x) for x in str(a).upper().replace(",", " ").split()]
    s = " ".join(t).replace("BLDG 2", "COTTAGE")
    return s


def pdf_text(path):
    t = " ".join((pg.extract_text() or "") for pg in PdfReader(path).pages)
    t = re.sub(r"\s+", " ", t)
    assert len(t) > 400, (path, len(t))
    return t


def mg04(d):
    """The reproduction test's filed numbers, read from the standard itself (positive control first)."""
    t = pdf_text(find(d, r"^MG-04"))
    assert "The reproduction test" in t and "Before an adjustment is used" in t, "MG-04 text not read"
    yr = int(re.search(r"named storm from the (\d{4}) season on", t).group(1))
    mn = float(re.search(r"paid at least USD (\d+) million", t).group(1)) * 1e6
    tol = float(re.search(r"within (\d+) percent of what the company actually paid", t).group(1)) / 100
    return yr, mn, tol


def brief(d):
    t = pdf_text(find(d, r"_board_brief\.pdf$"))
    assert "The decision" in t and "How the counties are compared" in t, "brief text not read"
    n = int(re.search(r"for ([\d,]+) homes we insure in one county", t).group(1).replace(",", ""))
    assert "less its 2027 annual expected loss with every home on the portfolio carrying a FORTIFIED Roof" in t
    return n


def main_call(d):
    yr, mn, tol = mg04(d)
    reg = pd.read_csv(find(d, r"^named_storm_register"), dtype=str).fillna("")
    reg = reg[reg.landfall_date >= str(yr)]
    cl = pd.read_csv(find(d, r"^claims_payment_lines"), dtype=str, keep_default_na=False)
    cl["amt"] = cl.amount_usd.astype(float)
    cl = cl[cl.catastrophe_code.isin(reg.claims_catastrophe_code)]
    cl["f"] = cl.mitigation_credit.str.split(";").map(lambda t: "FORT-R" in t).astype(int)
    code2id = dict(zip(reg.claims_catastrophe_code, reg.storm_id))
    cl["sid"] = cl.catastrophe_code.map(code2id)
    paid = cl.groupby(["sid", "zip_code", "f"]).amt.sum()
    inf = pd.read_parquet(find(d, r"^inforce_at_landfall"))
    inf = inf[inf.storm_id.isin(reg.storm_id)]
    inf = inf.assign(tiv=inf.coverage_a * np.where(inf.coverage_unit.str.contains("thousand"), 1000.0, 1.0),
                     f=(inf.roof_designation.str.startswith("FORTIFIED")).astype(int))
    tiv = inf.groupby(["storm_id", "zip_code", "f"]).tiv.sum()
    xl = pd.read_excel(find(d, r"^storm_peak_gust"), sheet_name=None, header=None)
    gust = {}
    name2id = {n.split()[-1] + " " + dte[:4]: s for n, dte, s in zip(reg.storm_name, reg.landfall_date, reg.storm_id)}
    for sh, raw in xl.items():
        if sh not in name2id:
            continue
        i = [k for k in range(len(raw)) if str(raw.iloc[k, 0]).strip().lower() in ("zip", "zip_code")][0]
        hdr = [str(x) for x in raw.iloc[i]]
        body = raw.iloc[i + 1:]
        k = 1 if "kt" in hdr[1] else 0
        for z, g in zip(body.iloc[:, 0], body.iloc[:, 1]):
            gust[(name2id[sh], str(z).zfill(5))] = float(g) * (KTS if k else 1.0)
    rows = []
    for (sid, z, f), t in tiv.items():
        rows.append((sid, z, f, t, paid.get((sid, z, f), 0.0), gust[(sid, z)]))
    c = pd.DataFrame(rows, columns=["sid", "z", "f", "tiv", "paid", "g"])
    c["k"] = (c.g // 10 * 10).astype(int)
    cut = {}
    for k, v in c.groupby("k"):
        s, fo = v[v.f == 0], v[v.f == 1]
        if fo.tiv.sum() > 0 and s.paid.sum() > 0:
            cut[k] = 1 - (fo.paid.sum() / fo.tiv.sum()) / (s.paid.sum() / s.tiv.sum())
    ks = sorted(cut)

    def cutk(k):
        return cut[k] if k in cut else cut[min(ks, key=lambda x: abs(x - k))]
    # MG-04 on the class cuts
    worst = 0.0
    nstorm = 0
    for sid, v in c.groupby("sid"):
        fo = v[v.f == 1]
        if fo.paid.sum() < mn:
            continue
        nstorm += 1
        s = v[v.f == 0].set_index("z")
        pred = sum(s.loc[z, "paid"] / s.loc[z, "tiv"] * t * (1 - cutk(k)) for z, t, k in zip(fo.z, fo.tiv, fo.k)
                   if z in s.index and s.loc[z, "tiv"] > 0)
        worst = max(worst, abs(pred / fo.paid.sum() - 1))
    elt = pd.read_parquet(find(d, r"^corvane_hu27_elt"))
    hz = pd.read_csv(find(d, r"^corvane_hu27_event_hazard"))
    hz["event_id"] = hz.event_ref.str[5:].astype(int)
    hz["lo"] = hz.peak_gust_class.str.split("-").str[0].astype(int)
    pf = pd.read_csv(find(d, r"^retrofit_2027_modeled"))
    code2c = dict(zip(pf.portfolio, pf.county))
    elt["county"] = elt.portfolio_id.map(code2c)
    e = elt.merge(hz[["event_id", "county", "lo"]], on=["event_id", "county"])
    assert len(e) == len(elt)
    e["cut"] = e.lo.map(cutk)
    e["aal"] = e.annual_rate * e.mean_loss_usd
    aal = e.groupby("county").aal.sum()
    rem = (e.aal * e.cut).groupby(e.county).sum()
    n_round = brief(d)
    assert (pf.groupby("county").size() == n_round).all(), "portfolio size against the brief's round"
    return aal, rem, worst, nstorm, tol


def ask_a(d):
    ce = pd.read_csv(find(d, r"^fortified_certificate_register"), dtype=str, keep_default_na=False)
    void = set(ce[ce.event == "VOIDED"].certificate_number)
    v = ce[(ce.event == "ISSUED") & (ce.event_date <= "2026-09-30") & (ce.expiry_date > "2026-09-30")
           & ~ce.certificate_number.isin(void)]
    keys = set(v.parcel_ref.str.replace("-", "") + "|" + v.property_address.map(lambda a: "C" if addr(a).endswith("COTTAGE") else "M"))
    pm = pd.read_csv(find(d, r"^policy_master"), dtype=str, keep_default_na=False)
    live = pm[(pm.inception_date <= "2026-09-30") & ((pm.cancellation_date == "") | (pm.cancellation_date > "2026-09-30"))]
    live = live.assign(k=live.parcel_id + "|" + live.site_address.map(lambda a: "C" if addr(a).endswith("COTTAGE") else "M"))
    h = live[live.k.isin(keys)]
    return h.groupby("county").agg(n=("k", "size"), cov=("coverage_a_usd", lambda s: s.astype(float).sum()))


def ask_b(d):
    lv = pd.read_csv(find(d, r"^legacy_claims_valuations"))
    lv["dt"] = pd.to_datetime(lv.valuation_date, format="%m/%d/%Y")
    last = lv.sort_values("dt").groupby("legacy_claim_no").agg(st=("storm", "last"), p=("paid_to_date", "last"))
    cl = pd.read_csv(find(d, r"^claims_payment_lines"), dtype=str, keep_default_na=False)
    cl = cl[cl.legacy_claim_ref != ""].copy()
    cl["amt"] = cl.amount_usd.astype(float)
    cl["p_last"] = cl.legacy_claim_ref.map(last.p)
    conv = (cl.payment_date == "2012-01-01") & ((cl.amt - cl.p_last).abs() < 0.005)
    after = cl[~conv].groupby("legacy_claim_ref").amt.sum()
    last["after"] = after.reindex(last.index).fillna(0.0)
    last["tot"] = last.p + last.after
    return last.groupby("st")[["tot", "after"]].sum()


def ask_c(d):
    pf = pd.read_csv(find(d, r"^retrofit_2027_modeled"), dtype={"zip_code": str})
    pe = pd.read_csv(find(d, r"^county_building_permits"), dtype={"zip": str})
    pm = pd.read_csv(find(d, r"^policy_master"), dtype=str, keep_default_na=False)
    pe = pe[pe.issue_date <= "2026-09-30"]

    def parts(a):
        t = addr(a).split()
        cot = t[-1] == "COTTAGE"
        t = t[:-1] if cot else t
        return t[0], " ".join(t[1:]), cot
    kp = pm.site_address.map(parts)
    known = pd.DataFrame({"county": pm.county, "zip": pm.zip_code, "num": kp.str[0], "street": kp.str[1]})
    ks = set(zip(known.county, known.street))
    pp = pe.address.map(parts)
    pe = pe.assign(num=pp.str[0], street=pp.str[1], cot=pp.str[2])
    remap = {}
    for (cty, st), g in pe[[(a, b) not in ks for a, b in zip(pe.county, pe.street)]].groupby(["county", "street"]):
        m = g.merge(known[known.county == cty], left_on=["zip", "num"], right_on=["zip", "num"], suffixes=("", "_k"))
        remap[(cty, st)] = m.street_k.value_counts().index[0]
    pe["street"] = [remap.get((a, b), b) for a, b in zip(pe.county, pe.street)]
    rr = pe[pe.work_class == "RE-ROOF"]
    last = rr.groupby(["zip", "num", "street", "cot"]).issue_date.max().str[:4].astype(int)
    fp = pf.site_address.map(parts)
    yrs = [max(r, last.get((z, t[0], t[1], t[2]), 0)) for r, z, t in zip(pf.roof_year_on_record, pf.zip_code, fp)]
    old = pf[np.array(yrs) <= 2012]
    return old.groupby("county").agg(n=("policy_number", "size"), cov=("coverage_a_usd", "sum"))


def nums(line):
    return [float(x.replace(",", "")) for x in re.findall(r"-?\d[\d,]*\.?\d*", line)]


def main(bundle, sub):
    tmp = None
    if bundle.endswith(".zip"):
        tmp = tempfile.mkdtemp(prefix="v309_")
        with zipfile.ZipFile(bundle) as z:
            z.extractall(tmp)
        d = tmp
        inner = [os.path.join(tmp, x) for x in os.listdir(tmp)]
        if len(inner) == 1 and os.path.isdir(inner[0]):
            d = inner[0]
    else:
        d = bundle
    text = open(sub).read()
    block4 = text.split("## 4. Deliverable Answers")[1]
    aal, rem, worst, nstorm, tol = main_call(d)
    call = rem.idxmax()
    bad = []
    if "county for the 2027 round: %s." % call.lower() not in block4.lower():
        bad.append("call %s" % call)
    m = re.search(r"removes there: USD ([\d.]+) million", block4)
    if not m or abs(float(m.group(1)) - round(rem[call] / 1e6, 1)) > 1e-9 or len(m.group(1).split(".")[1]) != 1:
        bad.append("loss removed %.3f" % (rem[call] / 1e6))
    if "Runner-up: %s." % rem.sort_values().index[-2] not in block4:
        bad.append("runner-up")
    if not (worst <= tol and nstorm == 5):
        bad.append("MG-04 %.3f on %d storms" % (worst, nstorm))
    lines = block4.splitlines()

    def item(prefix, county):
        for l in lines:
            if l.strip().startswith("- %s:" % county):
                yield l

    sect = {}
    cur = None
    for l in lines:
        mm = re.match(r"^(\d+)\. ", l)
        if mm:
            cur = int(mm.group(1))
        elif l.strip().startswith("- ") and cur:
            k, v = l.strip()[2:].split(":", 1)
            sect.setdefault(cur, {})[k] = nums(v)
    for county, v in sect[4].items():
        if abs(v[0] - round(aal[county] / 1e6, 2)) > 1e-9:
            bad.append("aal %s" % county)
    a = ask_a(d)
    for county, v in sect[5].items():
        if v[0] != a.loc[county, "n"] or v[1] != round(a.loc[county, "cov"] / 1e3):
            bad.append("ask A %s" % county)
    b = ask_b(d)
    lcode = {"Hurricane Corwin": "L0803", "Tropical Storm Della": "L0902", "Hurricane Evander": "L1104"}
    for storm, v in sect[6].items():
        t = b.loc[lcode[storm]]
        if v[0] != round(t.tot / 1e3) or v[1] != round(t.after / 1e3):
            bad.append("ask B %s" % storm)
    c = ask_c(d)
    for county, v in sect[7].items():
        if v[0] != c.loc[county, "n"] or v[1] != round(c.loc[county, "cov"] / 1e3):
            bad.append("ask C %s" % county)
    if bad:
        print("verify: FAIL", bad)
        return 1
    print("verify: PASS (call %s, %.1f; MG-04 worst %.3f on %d storms; %d ask figures)" %
          (call, rem[call] / 1e6, worst, nstorm, 2 * (len(sect[5]) + len(sect[6]) + len(sect[7]))))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
