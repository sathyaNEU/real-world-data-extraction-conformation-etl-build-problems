"""Independent verifier: reads only the shipped bundle (target.zip, or an unzipped target dir) and submission.md,
recomputes every graded figure with its own code, and fails on any disagreement or on a figure printed at the
wrong precision.

    python3 task310/generator/verify.py <target.zip | target dir> <submission.md>
"""
import math
import os
import re
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd
from pypdf import PdfReader

T0 = pd.Timestamp("2025-01-01 00:00")          # market time, UTC+10
HOURS = 8760
REGIONS = ["Sandhaven Coast", "Eastbrook Metro", "Yarrandale Valley", "Tarrock Highlands"]


def find(d, pat):
    hits = [f for f in os.listdir(d) if re.search(pat, f)]
    assert len(hits) == 1, (pat, hits)
    return os.path.join(d, hits[0])


def pdf_text(path):
    t = " ".join((pg.extract_text() or "") for pg in PdfReader(path).pages)
    return re.sub(r"\s+", " ", t)


def guideline(d):
    t = pdf_text(find(d, r"^home_battery_programme_guideline"))
    n = int(re.search(r"funds ([\d,]+) home batteries a year", t).group(1).replace(",", ""))
    cap = float(re.search(r"Usable energy ([\d.]+) kWh", t).group(1))
    kw = float(re.search(r"Power ([\d.]+) kW charging", t).group(1))
    ec = float(re.search(r"charging stores (\d+) per cent", t).group(1)) / 100
    ed = float(re.search(r"discharging delivers (\d+) per cent", t).group(1)) / 100
    assert "hour by hour" in t and "empty at the start of the year" in t and "not connected to a controlled-load" in t
    return n, cap, kw, ec, ed


def local_to_market(ts, dst):
    return ts - pd.to_timedelta(dst.astype(int), unit="h")


def sim(gen, use, cap, kw, ec, ed):
    soc = np.zeros(gen.shape[0])
    out = np.zeros(gen.shape[0])
    for t in range(gen.shape[1]):
        net = gen[:, t] - use[:, t]
        ch = np.minimum(np.minimum(np.maximum(net, 0), kw), (cap - soc) / ec)
        soc += ch * ec
        dis = np.minimum(np.minimum(np.maximum(-net, 0), kw), soc * ed)
        soc -= dis / ed
        out += dis
    return out


def main_call(d):
    n_bat, cap, kw, ec, ed = guideline(d)
    reg = pd.read_csv(find(d, r"^hemp_panel_register"), dtype=str)
    sysr = pd.read_excel(find(d, r"^hemp_solar_systems"), dtype={"panel_id": str, "inverter_ref": str})
    conn = pd.read_csv(find(d, r"^southmark_connection_register"), dtype={"nmi": str})
    homes = list(reg.panel_id)
    ix = {p: i for i, p in enumerate(homes)}
    owner = dict(zip(sysr.inverter_ref, sysr.panel_id))
    gen = np.zeros((len(homes), HOURS))
    sv = pd.read_parquet(find(d, r"^velkora_portal"))
    start = pd.to_datetime(sv.period_start) - pd.to_timedelta(sv.utc_offset.str[1:3].astype(int) - 10, unit="h")
    h = ((start - T0) / pd.Timedelta(hours=1)).astype(int).to_numpy()
    r = sv.site_ref.map(lambda s: ix[owner[s]]).to_numpy()
    k = (h >= 0) & (h < HOURS)
    np.add.at(gen, (r[k], h[k]), sv.energy_wh.to_numpy()[k] / 1000)
    ht = pd.read_csv(find(d, r"^ondrava_cloud"), dtype={"serial": str})
    for s, g in ht.groupby("serial", sort=False):
        lt = pd.to_datetime(g.read_at).reset_index(drop=True)
        rep = lt == pd.Timestamp("2025-04-06 03:00")
        first_rep = rep & (rep.cumsum() == 1)
        dst = (lt < pd.Timestamp("2025-04-06 03:00")) | first_rep | (lt >= pd.Timestamp("2025-10-05 03:00"))
        end = local_to_market(lt, dst)
        e = g.total_yield_wh.diff().to_numpy().copy()
        note = str(sysr[sysr.inverter_ref == s].note.iloc[0])
        e[0] = g.total_yield_wh.iloc[0] if note.startswith("replacement") else 0.0
        hh = ((end - pd.Timedelta(hours=1) - T0) / pd.Timedelta(hours=1)).astype(int).to_numpy()
        k = (hh >= 0) & (hh < HOURS)
        np.add.at(gen, (np.full(k.sum(), ix[owner[s]]), hh[k]), e[k] / 1000)
    m = pd.read_parquet(find(d, r"^southmark_meter_halfhours"))
    nmi = dict(zip(reg.nmi, reg.panel_id))
    hh = (((pd.to_datetime(m.interval_end) - pd.Timedelta(minutes=30)) - T0) // pd.Timedelta(hours=1)).to_numpy()
    rr = m.nmi.map(lambda x: ix[nmi[x]]).to_numpy()
    e1, b1 = np.zeros_like(gen), np.zeros_like(gen)
    np.add.at(e1, (rr, hh), m.e1_kwh.to_numpy())
    np.add.at(b1, (rr, hh), m.b1_kwh.to_numpy())
    use = gen + e1 - b1
    last = sysr.sort_values("valid_from").groupby("panel_id").tail(1).set_index("panel_id")
    kwp = np.array([float(last.loc[p, "array_kwp"]) for p in homes])
    ac = np.array([float(last.loc[p, "inverter_ac_kw"]) for p in homes])
    lim = conn.set_index("nmi").export_limit_kw.to_dict()
    limit = np.array([float(lim[n]) for n in reg.nmi])
    region = reg.region.to_numpy()
    held = limit < ac
    re_gen = gen.copy()
    per = gen / kwp[:, None]
    for i in np.where(held)[0]:
        ref = per[(region == region[i]) & ~held].mean(axis=0)
        re_gen[i] = np.maximum(np.minimum(kwp[i] * ref, ac[i]), gen[i])
    got = sim(re_gen, use, cap, kw, ec, ed)
    rec = sim(gen, use, cap, kw, ec, ed)
    val = {g_: float(got[region == g_].mean()) for g_ in REGIONS}
    raw = {g_: float(rec[region == g_].mean()) for g_ in REGIONS}
    return n_bat, val, raw


def ask_a(d):
    der = pd.read_csv(find(d, r"^southmark_der_register"), dtype={"nmi": str})
    sd = pd.read_csv(find(d, r"^southmark_nmi_standing"), dtype={"nmi": str, "postcode": str, "previous_nmi": str})
    bc = pd.read_excel(find(d, r"^battery_booster_claims"), dtype={"nmi": str, "postcode": str})
    der["commissioned"] = pd.to_datetime(der.commissioned)
    pv = der[der.der_type == "PV"]
    first = pv.groupby("nmi").commissioned.min()
    prev = sd.set_index("nmi").previous_nmi.fillna("").to_dict()
    nxt = {v: k for k, v in prev.items() if v}
    def since(n):
        out = [first.get(n)]
        while prev.get(n):
            n = prev[n]
            out.append(first.get(n))
        return min(x for x in out if x is not None)
    live = pv[(pv.status == "Active") & (pv.customer_class == "RES")]
    bat = set(der[(der.der_type == "BESS") & (der.status == "Active")].nmi)
    cand = set(live.nmi) - bat
    cand = {n for n in cand if since(n) <= pd.Timestamp("2025-09-30")}
    paid = bc[bc.status == "Paid"]
    gone = set()
    for n in paid.nmi.dropna():
        while n in nxt:
            n = nxt[n]
        gone.add(n)
    act = sd[sd.nmi_status == "Active"]
    st = {"STREET": "ST", "ROAD": "RD", "AVENUE": "AVE", "CRESCENT": "CRES", "PLACE": "PL", "DRIVE": "DR", "COURT": "CT",
          "PARADE": "PDE", "CLOSE": "CL"}
    def clean(a):
        w = re.sub(r"^UNIT (\d+),?\s+", r"\1/", str(a).upper()).replace(",", " ").split()
        return " ".join(st.get(x, x) for x in w)
    where = {(a, s, p): n for a, s, p, n in zip(act.address, act.suburb, act.postcode, act.nmi)}
    for a, s, p in zip(paid.premises_address[paid.nmi.isna()], paid.suburb[paid.nmi.isna()], paid.postcode[paid.nmi.isna()]):
        n = where.get((clean(a), str(s).upper(), p))
        if n:
            gone.add(n)
    cand -= gone
    reg = live.drop_duplicates("nmi").set_index("nmi").network_region
    return {g_: sum(1 for n in cand if reg[n] == g_) for g_ in REGIONS}


def ask_b(d):
    t = pd.read_parquet(find(d, r"^norvane_pilot_battery_telemetry"))
    sites = pd.read_excel(find(d, r"^pilot_round_2024_sites"), dtype=str).fillna("")
    t = t.drop_duplicates(["battery_serial", "date"]).sort_values(["battery_serial", "date"])
    t["date"] = pd.to_datetime(t.date)
    fresh = set(sites.battery_serial[sites.note == "replacement unit"])
    q_end = [pd.Timestamp("2025-03-31"), pd.Timestamp("2025-06-30"), pd.Timestamp("2025-09-30"), pd.Timestamp("2025-12-31")]
    energy = {}
    counters = {}
    for s, g in t.groupby("battery_serial"):
        base = 0.0 if s in fresh else float(g.lifetime_discharged_wh.iloc[0] - g.discharged_wh.iloc[0])
        marks = [base] + [float(g.lifetime_discharged_wh[g.date <= q].iloc[-1]) if (g.date <= q).any() else np.nan
                          for q in q_end]
        vals, prevv = [], base
        for x in marks[1:]:
            if np.isnan(x):
                vals.append(0.0)
            else:
                vals.append(x - prevv)
                prevv = x
        energy[s] = vals
        counters[s] = g.set_index("date").lifetime_discharged_wh
    skip = set()
    for _, g in sites[sites.note != "replacement unit"].groupby("site_id"):
        if len(g) == 2:
            a, b = list(g.battery_serial)
            ca, cb = counters[a], counters[b]
            common = ca.index.intersection(cb.index)
            if (ca[common] == cb[common]).all():
                skip.add(b)
    return [sum(v[i] for s, v in energy.items() if s not in skip) / 1e6 for i in range(4)]


def ask_c(d):
    cert = pd.read_csv(find(d, r"^battery_installation_certificates_2025"), dtype=str)
    am = pd.read_csv(find(d, r"^battery_installation_certificate_amendments"), dtype=str).sort_values(
        ["amended_on", "certificate_no"])
    acc = pd.read_csv(find(d, r"^installer_accreditation_register"), dtype=str)
    sd = pd.read_csv(find(d, r"^southmark_nmi_standing"), dtype={"nmi": str, "postcode": str})
    der = pd.read_csv(find(d, r"^southmark_der_register"), dtype={"nmi": str}, usecols=["nmi", "network_region"])
    place = sd.merge(der.drop_duplicates("nmi"), on="nmi").drop_duplicates(["suburb", "postcode"]).set_index(
        ["suburb", "postcode"]).network_region.to_dict()
    head = cert.groupby("certificate_no").agg(installed=("installed", "first"), lodged=("lodged", "first"),
                                              suburb=("suburb", "first"), postcode=("postcode", "first"),
                                              acc=("installer_accreditation", "first"))
    mods = cert.groupby("certificate_no").module_serial.apply(frozenset)
    for r in am.itertuples():
        if r.amendment == "withdrawn":
            head = head.drop(index=r.certificate_no, errors="ignore")
        else:
            head.loc[r.certificate_no, "acc"] = r.new_value
    # an installation is a set of modules: certificates sharing any module are one, the latest lodgement stands
    seen, keep = {}, []
    for c in head.sort_values(["lodged"], kind="mergesort").index[::-1]:
        if any(m in seen for m in mods[c]):
            continue
        for m in mods[c]:
            seen[m] = c
        keep.append(c)
    head = head.loc[keep]
    good = acc[(acc.status == "Current") & (pd.to_datetime(acc.expires) >= pd.Timestamp("2027-12-31"))]
    ids = set(good.accreditation_no) | set(good.previous_no.dropna())
    head = head[head.acc.isin(ids)]
    regs = [place[(s.upper(), p)] for s, p in zip(head.suburb, head.postcode)]
    return {g_: sum(1 for x in regs if x == g_) for g_ in REGIONS}


def rnd(v, u):
    return math.floor(v / u + 0.5) * u


def nums(line):
    return [float(x.replace(",", "")) for x in re.findall(r"-?\d[\d,]*\.?\d*", line)]


def main(bundle, sub):
    tmp = None
    if bundle.endswith(".zip"):
        tmp = tempfile.mkdtemp(prefix="v310_")
        zipfile.ZipFile(bundle).extractall(tmp)
        d = tmp
    else:
        d = bundle
    n_bat, val, raw = main_call(d)
    order = sorted(REGIONS, key=lambda g_: -val[g_])
    text = open(sub).read()
    b4 = text.split("## 4. Deliverable Answers")[1]
    bad = []

    def want(label, got, printed):
        if got != printed:
            bad.append("%s: recomputed %s, printed %s" % (label, got, printed))
    lines = b4.splitlines()

    def block(start):
        i = [j for j, l in enumerate(lines) if l.startswith(start)][0]
        out = []
        for l in lines[i + 1:]:
            if not l.startswith("   - "):
                break
            k, v = l[5:].split(": ")
            out.append((k, v))
        return dict(out)
    years = dict((n, int(y)) for y, n in re.findall(r"(20\d\d) ([A-Z][a-z]+ [A-Z][a-z]+)", [l for l in lines if l.startswith("1. Round years")][0]))
    for i, g_ in enumerate(order):
        want("year %s" % g_, 2027 + i, years.get(g_))
    kwh = block("2. Energy a programme battery")
    mwh = block("3. Each round's yearly energy")
    for g_ in REGIONS:
        want("kWh %s" % g_, int(rnd(val[g_], 50)), int(nums(kwh[g_])[0]))
        want("MWh %s" % g_, int(rnd(n_bat * val[g_] / 1000, 100)), int(nums(mwh[g_])[0]))
    a = ask_a(d)
    ea = block("4. Homes eligible")
    for g_ in REGIONS:
        want("ask A %s" % g_, a[g_], int(nums(ea[g_])[0]))
    b = ask_b(d)
    eb = block("5. Energy the 2024 pilot")
    for i, q in enumerate(["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025"]):
        want("ask B %s" % q, "%.1f" % rnd(b[i], 0.1), eb[q])
    c = ask_c(d)
    ec_ = block("6. Batteries installed in 2025")
    for g_ in REGIONS:
        want("ask C %s" % g_, c[g_], int(nums(ec_[g_])[0]))
    first = text.split("## 2.")[0]
    if order[0] not in first.split("## 1. Final Recommendation")[1]:
        bad.append("the recommendation does not name %s" % order[0])
    raw_order = sorted(REGIONS, key=lambda g_: -raw[g_])
    if raw_order[0] == order[0]:
        bad.append("the recorded readings already name the call")
    for m in bad:
        print("VERIFY FAIL", m)
    print("verify.py: %d graded figures recomputed, %d disagreements" % (12 + 12, len(bad)))
    return len(bad)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
