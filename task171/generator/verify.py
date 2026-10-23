"""Independent verifier for task171: reads only target/ (the extract, the CIS files, the CRM workbook, the rate
schedules PDF and the committee paper), on its own code path, and recomputes the two call figures and every ask
figure, then compares them with generator/figures.json. Prices are read from the PDF, not from the generator."""
from __future__ import annotations

import json
import os
import re
import sys
import warnings

import numpy as np
import pandas as pd
import pyarrow.parquet as pq
import statsmodels.api as sm
from pypdf import PdfReader

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
bad = []


def check(label, cond, detail=""):
    print("%-4s %-55s %s" % ("OK" if cond else "BAD", label, detail))
    if not cond:
        bad.append(label)


files = os.listdir(T)
f_ami = [f for f in files if f.endswith(".parquet")][0]
f_pdf = [f for f in files if f.endswith(".pdf")][0]
f_svc = [f for f in files if f.startswith("cis_service")][0]
f_rate = [f for f in files if f.startswith("cis_rate")][0]
f_crm = [f for f in files if f.startswith("crm_")][0]
f_doc = [f for f in files if f.endswith(".docx")][0]

# prices from the schedules
txt = "\n".join(p.extract_text() for p in PdfReader(os.path.join(T, f_pdf)).pages).replace("\n", " ")
check("PDF read back", len(txt) > 1500 and "Schedule R-ON" in txt)


def cents(pattern):
    m = re.search(pattern, txt)
    return float(m.group(1)) / 100


r1_24 = cents(r"Effective January 1, 2024: customer charge \$[\d.]+; energy charge ([\d.]+) cents")
r1_27 = cents(r"Effective January 1, 2027: customer charge \$[\d.]+; energy charge ([\d.]+) cents")
tou_pk = cents(r"Effective March 1, 2024: customer charge \$[\d.]+; on-peak energy ([\d.]+) cents")
tou_op = cents(r"Effective March 1, 2024: customer charge \$[\d.]+; on-peak energy [\d.]+ cents per kWh; off-peak energy ([\d.]+) cents")
on_off = cents(r"Effective January 1, 2027: customer charge \$[\d.]+; off-peak energy ([\d.]+) cents")
on_pk = cents(r"Effective January 1, 2027: customer charge \$[\d.]+; off-peak energy [\d.]+ cents per kWh; on-peak energy ([\d.]+) cents")
cc = re.findall(r"Effective January 1, 2027: customer charge \$([\d.]+)", txt)
check("PDF 2027 customer charges equal on R-1 and R-ON", len(cc) == 2 and cc[0] == cc[1], str(cc))
import docx  # noqa: E402
paper = " ".join(p.text for p in docx.Document(os.path.join(T, f_doc)).paragraphs)
check("DOCX read back with the population and revenue sentences", "billed for all twelve billing months November 2025 to October 2026" in paper and "counted in full" in paper)

ami = pq.read_table(os.path.join(T, f_ami)).to_pandas()
svc = pd.read_csv(os.path.join(T, f_svc), dtype=str, keep_default_na=False)
rate = pd.read_csv(os.path.join(T, f_rate), dtype=str, keep_default_na=False)
svc["s"] = pd.to_datetime(svc.service_start, format="%m/%d/%Y")
svc["e"] = pd.to_datetime(svc.service_end.where(svc.service_end != ""), format="%m/%d/%Y")
rate["a"] = pd.to_datetime(rate.eff_from)
rate["b"] = pd.to_datetime(rate.eff_to.where(rate.eff_to != ""))
end_of = svc.set_index("service_acct").e

pre = [m for m in sorted(ami.bill_month.unique()) if "2023-03" <= m <= "2024-02"]
ty = [m for m in sorted(ami.bill_month.unique()) if "2025-11" <= m <= "2026-10"]
check("billing months", len(pre) == 12 and len(ty) == 12)
P = ["kwh_2300_0600", "kwh_0600_1600", "kwh_1600_2100", "kwh_2100_2300"]


def period_sums(months):
    x = ami[ami.bill_month.isin(months)]
    pair = x.duplicated(["meter_no", "service_acct", "bill_month", "read_from"], keep=False)
    x = x[~(pair & (x.read_type == "EST"))]
    return x.groupby("service_acct")[P].sum(), x.groupby("service_acct").bill_month.nunique()


# rate in effect on a date: a row covers it, an open R-TOU row ending at the service's final read
rate["b2"] = rate.b.fillna(rate.service_acct.map(end_of))


def on_rate(code, day):
    r = rate[(rate.rate_code == code) & (rate.a <= day) & (rate.b2.isna() | (rate.b2 >= day))]
    return set(r.service_acct)


offer = pd.Timestamp("2024-03-01"); asof = pd.Timestamp("2026-10-31")
c = svc[svc.service_acct.isin(on_rate("R-1", offer)) & (svc.s < offer) & (svc.e.isna() | (svc.e > offer))].copy()
first_tou = rate[rate.rate_code == "R-TOU"].groupby("service_acct").a.min()
c["mo"] = c.service_acct.map(first_tou).pipe(lambda d: (d.dt.year - 2024) * 12 + d.dt.month - 3).fillna(999)
c["last"] = c.e.pipe(lambda d: (d.dt.year - 2024) * 12 + d.dt.month - 3).fillna(99)
u, _ = period_sums(pre)
u = u.reindex(c.service_acct).fillna(0.0)
c["x"] = (u.sum(1) * r1_24 - (u.kwh_1600_2100 * tou_pk + (u.sum(1) - u.kwh_1600_2100) * tou_op)).values

b = svc[svc.service_acct.isin(on_rate("R-1", asof)) & svc.e.isna()].copy()
v, n = period_sums(ty)
b = b[b.service_acct.map(n).fillna(0) == 12]
v = v.reindex(b.service_acct)
b["x"] = (v.sum(1) * r1_27 - (v.kwh_2300_0600 * on_off + (v.sum(1) - v.kwh_2300_0600) * on_pk)).values

# discrete-time hazard, month-since-offer dummies, risk set ends at the final read
rows, ys = [], []
for k in range(12):
    at = (c.mo.values >= k) & (c["last"].values >= k)
    d = np.zeros((at.sum(), 12)); d[:, k] = 1.0
    rows.append(np.column_stack([c.x.values[at], d])); ys.append((c.mo.values[at] == k).astype(float))
fit = sm.Logit(np.concatenate(ys), np.vstack(rows)).fit(disp=0)
s = np.ones(len(b))
for k in range(12):
    d = np.zeros((len(b), 12)); d[:, k] = 1.0
    s *= 1 - fit.predict(np.column_stack([b.x.values, d]))
p = 1 - s
members, short = p.sum(), (p * b.x.values).sum()
fig = json.load(open(os.path.join(HERE, "figures.json")))
check("call members to the nearest 250", round(members / 250) * 250 == fig["call_members_2027"], "%.1f" % members)
check("call shortfall to the nearest 25,000", round(short / 25000) * 25000 == fig["call_shortfall_2027_usd"], "%.0f" % short)
check("unrounded figures agree with the generator", abs(members - fig["members_unrounded"]) < 0.5 and abs(short - fig["shortfall_unrounded"]) < 2)

# ask A
tou_now = svc[svc.service_acct.isin(on_rate("R-TOU", asof)) & svc.e.isna()].copy()
r = rate[rate.rate_code == "R-TOU"].sort_values(["service_acct", "a"])
start = {}
for acct, grp in r.groupby("service_acct"):
    a0, b0 = None, None
    for row in grp.itertuples():
        if a0 is None or b0 is None or row.a != b0 + pd.Timedelta(days=1):
            a0 = row.a
        b0 = row.b2
    start[acct] = a0
tou_now["long"] = tou_now.service_acct.map(start) <= pd.Timestamp("2025-11-01")
w, _ = period_sums(ty)
tou_now = tou_now.join(w, on="service_acct")
for dname, grp in tou_now.groupby("district"):
    k = {"Sedge Flats": "SF", "Brisco Bend": "BB", "Kessel Mill": "KM", "Pike Ridge": "PR", "Tamsey": "TY"}[dname]
    check("ask A %s" % dname, (int(grp.long.sum()), int(round(grp.kwh_1600_2100.sum())), int(round(grp.kwh_2300_0600.sum()))) ==
          (fig["a_%s_twelve_months" % k], fig["a_%s_kwh_4to9pm" % k], fig["a_%s_kwh_11pmto6am" % k]))

# ask B
crm = pd.read_excel(os.path.join(T, f_crm), dtype=str)
loc = pd.to_datetime(crm.received_utc, utc=True).dt.tz_convert("America/Chicago")
crm = crm[(crm.request == "Enrol R-TOU") & (loc >= pd.Timestamp("2024-03-01", tz="America/Chicago")) & (loc < pd.Timestamp("2024-06-01", tz="America/Chicago")) & (crm.status != "Closed - duplicate")]
members_of = svc.groupby("membership_no").service_acct.apply(list)
mem = svc.set_index("service_acct").membership_no
dist = svc.set_index("service_acct").district


def put_on(row):
    if row.status != "Completed":
        return row.service_acct
    done = pd.Timestamp(row.completed_on)
    for sacct in [row.service_acct] + [x for x in members_of[mem[row.service_acct]] if x != row.service_acct]:
        f = first_tou.get(sacct)
        if f is not None and 0 <= (f - done).days <= 45:
            return sacct
    return row.service_acct


crm["d"] = crm.apply(put_on, axis=1).map(dist)
for dname, grp in crm.groupby("d"):
    k = {"Sedge Flats": "SF", "Brisco Bend": "BB", "Kessel Mill": "KM", "Pike Ridge": "PR", "Tamsey": "TY"}[dname]
    check("ask B %s" % dname, (len(grp), int((grp.channel == "Web form").sum())) == (fig["b_%s_requests" % k], fig["b_%s_web" % k]))
print("verify: %d problems" % len(bad))
sys.exit(1 if bad else 0)
