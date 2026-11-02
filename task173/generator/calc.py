"""The golden's computation and the routes beside it, read from the shipped pack only."""
from __future__ import annotations

import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
BANDS = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59",
         "60-64", "65-69", "70-74", "75-79", "80-84", "85-89", "90+"]
GALL = re.compile(r"^(K80|K81|K830|K851)")
FY_START = {fy: pd.Timestamp(fy, 4, 1) for fy in range(2021, 2028)}


def fy_of(d):
    d = pd.to_datetime(d)
    return np.where(d.dt.month >= 4, d.dt.year, d.dt.year - 1)


def band(age):
    return np.minimum(np.asarray(age) // 5, 18)


class Pack:
    def __init__(self, tgt=None):
        t = tgt or os.path.join(TASK, "target")
        self.t = t
        self.ep = pd.read_csv(os.path.join(t, "pas_inpatient_episodes_2021_2026.csv"), dtype=str, keep_default_na=False)
        self.cw = pd.read_csv(os.path.join(t, "fennick_pas_to_epr_number_map.csv"), dtype=str)
        self.ptl = pd.read_parquet(os.path.join(t, "admitted_ptl_snapshots_2021_2026.parquet"))
        self.ers = pd.read_csv(os.path.join(t, "ers_referrals_general_surgery_2019_2026.csv"), dtype=str, keep_default_na=False)
        self.est = {d: pd.read_excel(os.path.join(t, "population_mid_year_estimates_2018_2025.xlsx"), sheet_name=d) for d in ("Marlstead", "Coldvale")}
        self.proj = {d: pd.read_excel(os.path.join(t, "population_projections_2022_based.xlsx"), sheet_name=d) for d in ("Marlstead", "Coldvale")}
        m = dict(zip(self.cw.fennick_pas_number, self.cw.epr_hospital_number))
        self.ep["patient"] = self.ep.hospital_number.map(lambda x: m.get(x, x))
        self.ptl["patient"] = self.ptl.hospital_number.map(lambda x: m.get(x, x))
        self.ptl["site2"] = self.ptl.site.replace({"FENH": "FEN"})

    def pop(self, year, kind="mixed"):
        """Two-district population by sex and band at mid-year (estimates to 2025, the 2022-based projection after)."""
        out = np.zeros((2, 19))
        for d in ("Marlstead", "Coldvale"):
            src = self.est[d] if (year <= 2025 and kind != "proj") else self.proj[d]
            for i, s in enumerate(("Females", "Males")):
                out[i] += src[(src.mid_year == year) & (src.sex == s)][BANDS].values[0]
        return out


def spells(P):
    ep = P.ep
    first = ep[ep.episode_no == "1"].copy()
    first["admit"] = pd.to_datetime(first.admission_date)
    meth = first.admission_method
    first["emergency"] = meth.str.match(r"^(2[1-9A-D]|Emergency)")
    dx = first.primary_diagnosis.str.replace(".", "", regex=False).str.replace(r"[^A-Z0-9]", "", regex=True).str[:4]
    first["dx4"] = dx
    first["gall"] = dx.str.match(GALL)
    first["site"] = first.site_code.map({"MGH01": "MGH", "FEN01": "FEN", "FENH": "FEN"})
    first["sexi"] = np.where(first.sex.isin(["2", "Female"]), 0, 1)
    first["band"] = band(first.age_on_admission.astype(int))
    first["fy"] = fy_of(first.admit)
    first["mi"] = (first.admit.dt.year - 2021) * 12 + first.admit.dt.month - 4
    return first


def line(P):
    s = spells(P)
    return s[s.emergency & s.gall].copy()


def months_observed(fy):
    return 7 if fy == 2026 else 12


def rate_forecast(L, P, years=(2024, 2025, 2026), target=2027):
    """Age-sex rates per head over the years given (FY2026/27 to date annualised) on the projected mid-year population."""
    num = np.zeros((2, 19))
    den = np.zeros((2, 19))
    for fy in years:
        sub = L[L.fy == fy]
        c = np.zeros((2, 19))
        np.add.at(c, (sub.sexi.values, sub.band.values), 1)
        num += c
        den += P.pop(fy) * months_observed(fy) / 12
    rate = np.divide(num, den, out=np.zeros_like(num), where=den > 0)
    return float((rate * P.pop(target, "proj")).sum())


def chole_list(P):
    c = P.ptl[P.ptl.opcs_code == "J183"].copy()
    c["snap"] = pd.to_datetime(c.snapshot_date)
    c["mi"] = (c.snap.dt.year - 2021) * 12 + c.snap.dt.month - 4
    c["added"] = pd.to_datetime(c.date_added)
    return c


def link(L, P):
    """Each line spell against the cholecystectomy list: on it at admission when a pathway added before the admission is
    on the month-end list of the admission month or of the month before."""
    c = chole_list(P)
    key = c[["patient", "mi", "added"]]
    on = set()
    g = {k: v for k, v in key.groupby("patient")}
    flags = []
    for pat, adm, mi in zip(L.patient, L.admit, L.mi):
        v = g.get(pat)
        ok = False
        if v is not None:
            w = v[(v.added < adm) & (v.mi.isin([mi, mi - 1]))]
            ok = len(w) > 0
        flags.append(ok)
    L = L.copy()
    L["listed"] = flags
    pm = c.groupby("mi").size()
    return L, pm


def plan_traj(tgt=None):
    """The planned cholecystectomy list at each month end, read from the capacity plan's table (text extraction)."""
    import pdfplumber
    t = tgt or os.path.join(TASK, "target")
    out = {}
    with pdfplumber.open(os.path.join(t, "elective_capacity_plan_2027_28_general_surgery.pdf")) as pdf:
        for page in pdf.pages:
            for tb in page.extract_tables():
                head = [re.sub(r"\s+", " ", c or "") for c in tb[0]]
                if head[0] != "Month end":
                    continue
                for r in tb[1:]:
                    if re.sub(r"\s+", " ", r[0] or "").startswith("Laparoscopic"):
                        out.update({h: int(v.replace(",", "")) for h, v in zip(head[1:], r[1:])})
    return out


def golden(P, hz_years=(2022, 2023, 2024, 2025, 2026), fp_years=(2024, 2025, 2026), pm_mode="month_end"):
    L = line(P)
    L, pm = link(L, P)
    conv = L[L.listed & L.fy.isin(hz_years)]
    months = [m for m in pm.index if 2021 + (m + 3) // 12 - (0 if (m + 3) % 12 >= 3 else 1) in hz_years] if False else \
        [m for m in pm.index if (m // 12 + 2021) in hz_years]
    hz = len(conv) / pm.loc[months].sum()
    first = rate_forecast(L[~L.listed], P, fp_years)
    tr = plan_traj(P.t)
    fy = [v for k, v in tr.items() if (k.split()[1] == "2027" and k.split()[0] not in ("Jan", "Feb", "Mar")) or (k.split()[1] == "2028" and k.split()[0] in ("Jan", "Feb", "Mar"))]
    if pm_mode == "month_end":
        pmf = sum(fy)
    else:
        prev = tr["Mar 2027"]
        seq = [prev] + fy
        pmf = sum((a + b) / 2 for a, b in zip(seq[:-1], seq[1:]))
    return {"first": first, "hazard": hz, "pm_plan": pmf, "listed_part": hz * pmf, "total": first + hz * pmf,
            "share_listed": float(L[L.fy.isin(hz_years)].listed.mean()), "default": rate_forecast(L, P, fp_years)}


if __name__ == "__main__":
    P = Pack()
    L = line(P)
    print(L.groupby("fy").size().to_dict())
    g = golden(P)
    print({k: round(v, 4) for k, v in g.items()})


QDATES = ["2025-06-30", "2025-09-30", "2025-12-31", "2026-03-31"]
HERNIA = ("T202", "T204", "T241")


def stale_moved(snap):
    """Rows of a pathway the other hospital now holds: the same patient and operation open at Marlstead, added later."""
    s = snap.copy()
    s["added"] = pd.to_datetime(s.date_added)
    mg = s[s.site2 == "MGH"][["patient", "opcs_code", "added"]].rename(columns={"added": "m_added"})
    j = s.reset_index().merge(mg, on=["patient", "opcs_code"], how="left")
    bad = j[(j.site2 == "FEN") & j.m_added.notna() & (j.m_added > j.added)]["index"].unique()
    return s.index.isin(bad)


def true_clocks(P):
    """Each pathway's clock start: the e-RS referral where the pathway carries one; a pathway opened when an operation
    was cancelled carries the clock of the pathway it replaced; otherwise the PTL's own."""
    ers = dict(zip(P.ers.ubrn, pd.to_datetime(P.ers.referral_received)))
    t = P.ptl.copy()
    t["snap"] = pd.to_datetime(t.snapshot_date)
    t["added"] = pd.to_datetime(t.date_added)
    t["clock"] = pd.to_datetime(t.rtt_clock_start)
    # one record per pathway life: (patient, opcs, added) is stable across the migration's renumbering
    life = t.groupby(["patient", "opcs_code", "added"]).agg(first=("snap", "min"), last=("snap", "max"), ubrn=("ubrn", "first"),
                                                            clock=("clock", "first")).reset_index()
    life = life.sort_values(["patient", "opcs_code", "added"]).reset_index(drop=True)
    tc = {}
    for (pat, op), g in life.groupby(["patient", "opcs_code"], sort=False):
        prev = None
        for r in g.itertuples():
            if r.ubrn:
                c = ers.get(r.ubrn, r.clock)
            elif prev is not None and (r.added - prev.last).days <= 40:   # re-listed, or moved to the other hospital
                c = tc[(pat, op, prev.added)]
            else:
                c = r.clock
            tc[(pat, op, r.added)] = c
            prev = r
    return tc


def ask_tables(P, mode="golden"):
    """Ask A (52 weeks or more from referral) and Ask B (hernia pathways) at each 2025/26 quarter end, by hospital."""
    tc = true_clocks(P) if mode in ("golden", "clock_only") else None
    out = {}
    for d in QDATES:
        s = P.ptl[P.ptl.snapshot_date == d].copy()
        if mode in ("golden", "stale_only", "dedup_patient"):
            if mode == "dedup_patient":
                h = s[s.opcs_code.isin(HERNIA)]
                keep = h.sort_values("date_added").drop_duplicates(["patient"], keep="last").index
                s = pd.concat([s[~s.opcs_code.isin(HERNIA)], s.loc[keep]])
            else:
                s = s[~stale_moved(s)]
        D = pd.Timestamp(d)
        if tc is not None:
            clk = [tc[(p, o, pd.Timestamp(a))] for p, o, a in zip(s.patient, s.opcs_code, s.date_added)]
        elif mode == "ers_only":
            ers = dict(zip(P.ers.ubrn, pd.to_datetime(P.ers.referral_received)))
            clk = [ers.get(u, pd.Timestamp(c)) if u else pd.Timestamp(c) for u, c in zip(s.ubrn, s.rtt_clock_start)]
        else:
            clk = pd.to_datetime(s.rtt_clock_start).tolist()
        wait = np.array([(D - c).days for c in clk])
        for site in ("MGH", "FEN"):
            mk = (s.site2 == site).values
            out[("A", d, site)] = int(((wait >= 364) & mk).sum())
            out[("B", d, site)] = int((s.opcs_code.isin(HERNIA).values & mk).sum())
    return out
