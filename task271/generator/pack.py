"""The cut pack read back as the golden reads it: the three layouts of the consortium's discharge files and the two
2026 releases on one footing, the death linkage, the hospital directory and the plan's claims."""
import csv
import datetime as dt
import os

import pandas as pd

import common as K


def _d(s, fmt):
    s = s.strip()
    return dt.datetime.strptime(s, fmt).date() if s else None


def _dot(c):
    c = c.strip()
    return c if (not c or "." in c or len(c) <= 3) else c[:3] + "." + c[3:]


def directory(target):
    x = pd.read_excel(os.path.join(target, K.FILES["hospitals"]), sheet_name="Hospitals", header=2, dtype=str)
    by_name = {v: k for k, v in K.NAME.items()}
    m = {}
    for _, r in x.iterrows():
        code = by_name[r["Hospital"]]
        m[str(r["Hospital no. (to 2022)"]).zfill(4)] = code
        m[str(r["Hospital ID (from 2023)"])] = code
    npi = {str(r["NPI (facility)"]): by_name[r["Hospital"]] for _, r in x.iterrows()}
    return m, npi


def _fixed(path, year, hmap):
    out = []
    shift = 2 if year == 2018 else 0
    with open(path, encoding="ascii") as f:
        for line in f:
            line = line.rstrip("\r\n")
            g = lambda a, b: line[a - 1:b]
            rec = dict(rec_id=g(1, 10).strip(), hosp=hmap[g(11, 14)], key=g(15, 30).strip(), sex=g(31, 31),
                       age=int(g(32, 34)), admit=_d(g(35, 42), "%Y%m%d"), discharge=_d(g(43, 50), "%Y%m%d"),
                       atype=g(51, 51), asrc=g(52, 52), disp=g(53, 54).strip(), pcat=g(55, 55), file=str(year))
            p = 56 + shift
            dx = []
            for i in range(9):
                c, poa = line[p - 1:p + 6].strip(), line[p + 6:p + 7].strip()
                p += 8
                if c:
                    dx.append((_dot(c), poa))
            px = []
            for i in range(6):
                c = line[p - 1:p + 6].strip()
                p += 7
                if c:
                    px.append(c)
            d0 = _d(line[p - 1:p + 7], "%Y%m%d")
            rec["dx"] = dx
            rec["px"] = [(c, d0 if i == 0 else None) for i, c in enumerate(px)]
            out.append(rec)
    return out


def _csv(path, era, hmap, fname):
    out = []
    with open(path, encoding="utf-8", newline="") as f:
        rd = csv.reader(f)
        head = next(rd)
        ix = {h: i for i, h in enumerate(head)}
        fmt = "%m/%d/%Y" if era == 2 else "%Y-%m-%d"
        pre = ("dx%02d", "poa%02d", "px%02d", "pxdate%02d") if era == 2 else ("diag_%d", "poa_%d", "proc_%d", "proc_date_%d")
        base = (["record_id", "hospital_no", "person_key", "sex", "age", "admit_date", "discharge_date", "admit_type",
                 "admit_source", "discharge_status", "payer_cat", "payer_name"] if era == 2 else
                ["rec_no", "hosp_id", "link_key", "sex", "age_years", "admission_date", "discharge_date", "adm_type",
                 "adm_source", "dsch_disposition", "payer_group", "payer"])
        for row in rd:
            v = lambda k: row[ix[k]]
            rec = dict(rec_id=v(base[0]), hosp=hmap[v(base[1])], key=v(base[2]), sex=v(base[3]), age=int(v(base[4])),
                       admit=_d(v(base[5]), fmt), discharge=_d(v(base[6]), fmt), atype=v(base[7]), asrc=v(base[8]),
                       disp=v(base[9]), pcat=v(base[10]), payer=v(base[11]), file=fname)
            dx, px = [], []
            for i in range(1, 26):
                c = v(pre[0] % i)
                if c:
                    dx.append((_dot(c), v(pre[1] % i)))
                c = v(pre[2] % i)
                if c:
                    px.append((c, _d(v(pre[3] % i), fmt)))
            rec["dx"], rec["px"] = dx, px
            out.append(rec)
    return out


def load(target):
    f = lambda k: os.path.join(target, K.FILES[k])
    hmap, npimap = directory(target)
    P = {"hmap": hmap, "npimap": npimap}
    recs = []
    for y in (2016, 2017, 2018):
        recs += _fixed(f("d%d" % y), y, hmap)
    recs += _csv(f("d2019_2022"), 2, hmap, "2019-2022")
    recs += _csv(f("d2023_2025"), 3, hmap, "2023-2025")
    P["discharges"] = recs
    P["prelim"] = _csv(f("prelim"), 3, hmap, "2026p")
    P["revised"] = _csv(f("revised"), 3, hmap, "2026r")
    deaths = pd.read_csv(f("deaths"), dtype=str, keep_default_na=False)
    deaths = deaths[deaths.death_record_found == "Y"]
    P["deaths"] = {k: dt.date.fromisoformat(d) for k, d in zip(deaths.link_key, deaths.date_of_death)}
    P["deaths_imputed"] = set(deaths.link_key[deaths.dod_day_imputed == "Y"])
    cl = pd.read_csv(f("claims"), dtype=str, keep_default_na=False)
    cl["allowed"] = cl.allowed_amount.astype(float)
    cl["hosp"] = cl.billing_npi.map(npimap)
    P["claims"] = cl
    return P
