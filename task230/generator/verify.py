"""Independent verifier: recomputes the call and every ask figure from target/ alone, with its own joins, its own
likelihood fit (scipy) and its own parsing of the rate cards, and compares with the golden workbook."""
import datetime as dt
import json
import os
import re
import sys
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from pypdf import PdfReader
from scipy.optimize import minimize
from scipy.special import expit


def sheet(path, name, header=0):
    wb = load_workbook(path, data_only=True, read_only=True)
    rows = [r for r in wb[name].iter_rows(values_only=True)]
    return pd.DataFrame([r for r in rows[header + 1:] if any(x is not None for x in r)], columns=rows[header])


def pdf_text(path):
    return "\n".join(p.extract_text() for p in PdfReader(path).pages)


def main(target, golden_dir, quiet=False):
    f = lambda n: os.path.join(target, n)
    reg = pd.read_csv(f("stream_register.csv"))
    fam = dict(zip(reg.stream_code, reg.form_family))
    night = set(reg[(reg.queue == "NIGHT") & (reg.queue_from < "2026-07-01")].stream_code)
    sched = pdf_text(f("client_quality_schedules_2026.pdf"))
    lim = {s: float(l) for s, l in re.findall(r"([A-Z]{3}-[A-Z0-9]{3,4})\s+(\d+\.\d+)\s+\d+\.\d+%", sched)}
    pct = {s: float(p) for s, p in re.findall(r"([A-Z]{3}-[A-Z0-9]{3,4})\s+\d+\.\d+\s+\d+\.\d+%\s+(\d+(?:\.\d+)?)%", sched)}
    streams = list(lim)

    # screens of record, shift-day, verifier
    sp = pd.read_parquet(f("first_pass_verifications_2026q3.parquet"))
    sp = sp[sp.outcome == "SUBMITTED"].copy()
    isn = sp.stream_code.isin(night)
    sp["q"] = np.where(isn, "N", "D")
    sp["sd"] = (sp.opened_at - pd.to_timedelta(np.where(isn & (sp.opened_at.dt.hour < 12), 1, 0), unit="D")).dt.normalize()
    bad = sheet(f("workforce_register.xlsx"), "Badge allocation")
    bad["Valid to"] = pd.to_datetime(bad["Valid to"]).fillna(pd.Timestamp("2100-01-01"))
    m = sp[["badge_no", "sd"]].reset_index().merge(bad, left_on="badge_no", right_on="Badge")
    m = m[(m.sd >= pd.to_datetime(m["Valid from"])) & (m.sd <= m["Valid to"])]
    sp["emp"] = m.set_index("index")["Emp No"]
    emp = sheet(f("workforce_register.xlsx"), "Employees")
    hire = dict(zip(emp["Emp No"], pd.to_datetime(emp["Date of joining"])))
    sp["ten"] = (sp.sd - sp.emp.map(hire)).dt.days

    au = pd.read_parquet(f("blind_rekey_audit_2026q3.parquet"))
    kf = sheet(f("form_specifications.xlsx"), "Key fields")
    au = au.merge(kf, left_on=["stream_code", "form_version", "field_name"], right_on=["Stream", "Form version", "Field"])
    au = au.merge(sp[["document_id", "q", "sd", "emp", "ten"]], on="document_id")
    au["e"] = au.result_code.isin(["C", "R"]).astype(int)
    au["r"] = (au.result_code == "R").astype(int)
    au["v"] = (au.result_code == "V").astype(int)
    # the shift-day's OCR error rate over every stream it carried, stratified by stream
    fields = sp.groupby(["q", "sd", "stream_code"]).key_fields.sum()
    st = au.groupby(["q", "sd", "stream_code"]).agg(e=("e", "sum"), n=("e", "size")).join(fields)
    st["x"] = st.e / st.n * st.key_fields
    pr = st.groupby(["q", "sd"])[["x", "key_fields"]].sum()
    rate = (pr.x / pr.key_fields).rename("rate")
    E = au[au.e == 1].join(rate, on=["q", "sd"])
    E["fam"] = E.stream_code.map(fam)
    E["tb"] = np.where(E.ten < 90, 0, np.where(E.ten < 180, 1, 2))
    cats = {}
    cols = [np.log(E.rate.values)]
    for c in ("fam", "Field type", "emp", "tb"):
        lv = sorted(E[c].unique())
        cats[c] = lv
        for l in lv[1:]:
            cols.append((E[c].values == l).astype(float))
    X = np.column_stack([np.ones(len(E))] + cols)
    y = E.r.values

    def nll(b):
        z = X @ b
        return -(y * z - np.logaddexp(0, z)).sum()

    def grad(b):
        return -X.T @ (y - expit(X @ b))
    b = minimize(nll, np.zeros(X.shape[1]), jac=grad, method="L-BFGS-B", options={"maxiter": 5000, "gtol": 1e-8}).x
    names = ["c", "lr"] + [f"{c}={l}" for c in ("fam", "Field type", "emp", "tb") for l in cats[c][1:]]
    coef = dict(zip(names, b))
    emp_mean = np.mean([0.0] + [coef[f"emp={e}"] for e in cats["emp"][1:]])
    fa = au.v.sum() / (au.e == 0).sum()
    mix = au.groupby(["stream_code", "Field type"]).agg(e=("e", "sum"), n=("e", "size")).reset_index()
    ph = (mix.groupby("stream_code").e.sum() / mix.groupby("stream_code").n.sum()).to_dict()

    # November
    pdl = sheet(f("november_operating_plan.xlsx"), "Daily key fields")
    rt = sheet(f("november_operating_plan.xlsx"), "Routing")
    nq = dict(zip(rt.Stream, np.where(rt["Queue (November)"] == "Night", "N", "D")))
    ro = sheet(f("november_operating_plan.xlsx"), "Roster")
    long = pdl.melt(id_vars=["Shift-day", "Day"], var_name="s", value_name="kf").dropna()
    long = long[long.kf > 0]
    long["q"] = long.s.map(nq)
    long["err"] = long.kf * long.s.map(ph)
    nr = long.groupby(["q", "Shift-day"])[["err", "kf"]].sum()
    nr = (nr.err / nr.kf).to_dict()
    fc = {}
    for s in streams:
        g = long[long.s == s]
        crew = ro[ro.Queue == ("Night" if nq[s] == "N" else "Day")]["Emp No"].tolist()
        tot = 0.0
        for r in g.itertuples():
            lr = np.log(nr[(nq[s], r[1])])
            acc = 0.0
            for e in crew:
                t = (pd.Timestamp(r[1]) - hire[e]).days
                tb = 0 if t < 90 else (1 if t < 180 else 2)
                base = coef["c"] + coef["lr"] * lr + coef.get(f"fam={fam[s]}", 0) + coef.get(f"tb={tb}", 0) + coef.get(f"emp={e}", emp_mean if e not in cats["emp"] else 0.0)
                mm = mix[mix.stream_code == s]
                p = sum(row.n * row.e / row.n * expit(base + coef.get(f"Field type={row[2]}", 0)) for row in mm.itertuples()) / mm.n.sum()
                acc += p
            tot += r.kf * acc / len(crew)
        fc[s] = (tot / g.kf.sum() + fa * (1 - ph[s])) * 1000
    call = sorted(s for s in streams if fc[s] > lim[s])

    # asks
    L = pd.read_csv(f("second_pass_sessions_2026_09.csv"))
    L["fam"] = L.stream.map(fam)
    mins = L.drop_duplicates(["session_ref", "half_shift"]).groupby("fam").productive_min.sum()
    rate_f = (mins / L.groupby("fam").size()).to_dict()
    vers = sheet(f("form_specifications.xlsx"), "Versions")
    vers["eff"] = pd.to_datetime(vers.iloc[:, 2])

    def kfpd(s, d):
        g = vers[(vers.Stream == s) & (vers.eff <= pd.Timestamp(d))].sort_values("eff")
        return g.iloc[-1, 3]
    long["kfpd"] = [kfpd(s, d) for s, d in zip(long.s, long["Shift-day"])]
    long["docs"] = long.kf / long.kfpd
    hrs = {s: int(round(long[long.s == s].docs.sum() * rate_f[fam[s]] / 60)) for s in streams}
    import subprocess
    rc = subprocess.run(["pdftotext", "-layout", f("client_rate_cards_2026.pdf"), "-"], capture_output=True, text=True).stdout
    acct = {s: s.split("-")[0] for s in streams}
    docs_acct = long.assign(a=long.s.map(acct)).groupby("a").docs.sum()
    cred = {}
    blocks = re.split(r"\n(?=\s*[A-Z][A-Za-z&' ]+ \((?:USD|GBP|AUD),)", rc)
    for s in streams:
        blk = [b_ for b_ in blocks if re.search(r"\b" + re.escape(s) + r"\b", b_)][0]
        hdr = [l for l in blk.split("\n") if "Documents in month" in l][0]
        order = re.findall(r"[A-Z]{3}-[A-Z0-9]{3,4}", hdr)
        n_acct = docs_acct[acct[s]]
        price = None
        for nm, lo, hi, prices in re.findall(r"\n\s*(\S+(?: \d)?)\s+([\d,]+) (?:to ([\d,]+)|and over)((?:[ ]+\d+\.\d\d)+)", blk):
            lo_ = int(lo.replace(",", ""))
            hi_ = int(hi.replace(",", "")) if hi else 10 ** 12
            if lo_ <= n_acct <= hi_:
                price = float(prices.split()[order.index(s)])
        mi = re.search(r"Indexation: on the contract anniversary, (\d+) (\w+), unit prices rise by (\d+\.\d)%", blk.replace("\n", " "))
        g = long[long.s == s]
        amt = 0.0
        for r in g.itertuples():
            p = price
            if mi and pd.Timestamp(r[1]) >= pd.Timestamp(f"2026-{mi.group(2)}-{mi.group(1)}"):
                p = round(price * (1 + float(mi.group(3)) / 100), 4)
            amt += r.docs * p
        cred[s] = int(round(pct[s] / 100 * amt))
    # the client audits by the client's local delivery date
    tz = {"KBA": "America/New_York", "NDS": "America/Chicago", "BMC": "America/Detroit", "HPB": "America/Chicago",
          "WBH": "Australia/Brisbane", "CIP": "Australia/Sydney", "WPC": "Europe/London", "TCM": "Europe/London"}
    capt = {}
    for s_, txt in zip(re.findall(r"\n([A-Z][A-Za-z&' ]+) \(contract currency", sched), re.split(r"\n[A-Z][A-Za-z&' ]+ \(contract currency", sched)[1:]):
        mm = re.search(r"Findings coded (.+?) are capture", txt.replace("\n", " "))
        if mm:
            capt[s_.strip()] = set(x.strip() for x in re.split(r",| and ", mm.group(1)) if x.strip())
    import asks as AK
    rows = AK.normalized_client_audits(target)
    cname = {"KBA": "Kessington Benefit Administrators", "NDS": "Northgate Dental Services", "BMC": "Brightmoor Comp",
             "HPB": "Harbison Pharmacy Benefits", "WBH": "Wattlebird Health", "CIP": "Coolabah Income Protection",
             "WPC": "Whinfell Pet Cover", "TCM": "Thistlecombe Motor"}
    rows["sid"] = rows.file.str.split("_").str[1]
    rows["ld"] = [t.tz_localize("UTC").tz_convert(ZoneInfo(tz[c])).date() for t, c in zip(rows.delivered, rows.client)]
    rows = rows[(rows.ld >= dt.date(2026, 7, 1)) & (rows.ld <= dt.date(2026, 9, 30))]
    rows["kfc"] = [kfpd(s, d) for s, d in zip(rows.sid, rows.shift_day)]
    den = rows.drop_duplicates("claim").groupby("sid").kfc.sum()
    fin = rows[rows.seq > 0]
    fin = fin[fin.rnd == fin.groupby(["claim", "seq"]).rnd.transform("max")]
    fin = fin[[r in capt[cname[c]] for r, c in zip(fin.reason, fin.client)]]
    ca = {s: round(fin[fin.sid == s].shape[0] / den[s] * 1000, 1) for s in den.index}

    # against the golden workbook
    gw = sheet(os.path.join(golden_dir, "november_second_pass_plan.xlsx"), "November plan", header=3)
    gw = gw[gw.Stream.isin(streams)]
    gcall = sorted(gw[gw["Second pass in November"] == "Yes"].Stream)
    ok = gcall == call
    diffs = []
    for r in gw.itertuples(index=False):
        s = r[0]
        if r[5] != hrs[s]:
            diffs.append(("hours", s, r[5], hrs[s]))
        if r[6] != cred[s]:
            diffs.append(("credit", s, r[6], cred[s]))
        if s in ca and abs(float(r[8]) - ca[s]) > 1e-9:
            diffs.append(("client audit", s, r[8], ca[s]))
    if not quiet:
        print("verify call", call, "golden", gcall)
        print("verify ratios", {s: round(fc[s] / lim[s], 3) for s in streams})
    assert ok, (call, gcall)
    assert not diffs, diffs
    return dict(call=call, ratios={s: fc[s] / lim[s] for s in streams}, hours=hrs, credit=cred, client_audit=ca)


if __name__ == "__main__":
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    main(os.path.join(here, "target"), os.path.join(here, "golden"))
