"""Two sources the eligibility test does not use: the Department's footfall counters' daily counts in the centres,
a genuine indicator of a centre's health, and Torvasay Statistics' Labour Force Survey estimates of residents in
employment by industry and district of residence, a genuine employment measure on another basis. Both are weighed
and set aside (metadata.json names them)."""
import csv
import datetime as dt

import numpy as np
import openpyxl
from openpyxl.styles import Font

import names as N
import timeline as T

D_START, D_END = dt.date(2021, 4, 1), dt.date(2026, 3, 31)
HOLIDAYS = {dt.date(2021, 5, 3), dt.date(2021, 5, 31), dt.date(2021, 8, 30), dt.date(2021, 12, 27), dt.date(2021, 12, 28),
            dt.date(2022, 1, 3), dt.date(2022, 4, 15), dt.date(2022, 4, 18), dt.date(2022, 5, 2), dt.date(2022, 6, 2),
            dt.date(2022, 6, 3), dt.date(2022, 8, 29), dt.date(2022, 9, 19), dt.date(2022, 12, 26), dt.date(2022, 12, 27),
            dt.date(2023, 1, 2), dt.date(2023, 4, 7), dt.date(2023, 4, 10), dt.date(2023, 5, 1), dt.date(2023, 5, 8),
            dt.date(2023, 5, 29), dt.date(2023, 8, 28), dt.date(2023, 12, 25), dt.date(2023, 12, 26), dt.date(2024, 1, 1),
            dt.date(2024, 3, 29), dt.date(2024, 4, 1), dt.date(2024, 5, 6), dt.date(2024, 5, 27), dt.date(2024, 8, 26),
            dt.date(2024, 12, 25), dt.date(2024, 12, 26), dt.date(2025, 1, 1), dt.date(2025, 4, 18), dt.date(2025, 4, 21),
            dt.date(2025, 5, 5), dt.date(2025, 5, 26), dt.date(2025, 8, 25), dt.date(2025, 12, 25), dt.date(2025, 12, 26),
            dt.date(2026, 1, 1)}
SITES = ["High Street", "Market Place", "Bridge Street", "Church Street", "The Square", "Station Road", "King Street",
         "Fore Street", "Queen Street", "Arcade Walk"]


def footfall(w, path, seed):
    rng = np.random.default_rng(seed)
    rows = []
    week = np.array([0.93, 0.95, 0.97, 1.0, 1.12, 1.38, 0.66])
    for c in w.centres:
        n = 3 if c["tier"] == "city" else (2 if c["tier"] in ("large", "district") else 1)
        base = 2600 * (w.size[c["k"]] / 60) ** 0.9
        trend = rng.normal(-0.01, 0.025)
        for j in range(n):
            cid = "FC%s%02d" % (c["code"][2:], j + 1)
            site = "%s, %s" % (SITES[(c["k"] + j * 3) % len(SITES)], c["name"].replace(" City Centre", ""))
            level = base * rng.uniform(0.6, 1.2)
            installed = D_START if rng.random() > 0.15 else D_START + dt.timedelta(days=int(rng.integers(60, 500)))
            outages = []
            for _ in range(int(rng.integers(0, 4))):
                a = D_START + dt.timedelta(days=int(rng.integers(0, 1700)))
                outages.append((a, a + dt.timedelta(days=int(rng.integers(2, 25)))))
            d = installed
            while d <= D_END:
                if not any(a <= d <= b for a, b in outages):
                    yrs = (d - D_START).days / 365.25
                    recovery = 1 - 0.22 * np.exp(-yrs / 0.6)
                    season = 1 + 0.08 * np.cos(2 * np.pi * (d.timetuple().tm_yday - 350) / 365.25)
                    dec = 1.25 if (d.month == 12 and d.day >= 8 and d.day <= 23) else 1.0
                    hol = 0.75 if d in HOLIDAYS else 1.0
                    mu = level * recovery * (1 + trend) ** yrs * season * week[d.weekday()] * dec * hol
                    rows.append([cid, c["code"], site, d.isoformat(), int(max(0, rng.normal(mu, 0.06 * mu)))])
                d += dt.timedelta(days=1)
    rows.sort(key=lambda r: (r[0], r[3]))
    with open(path, "w", newline="", encoding="utf-8") as fh:
        cw = csv.writer(fh)
        cw.writerow(["counter_id", "centre_code", "location", "count_date", "footfall"])
        cw.writerows(rows)
    return len(rows)


def lfs(w, path, seed):
    """the Labour Force Survey's residents in employment by industry section and district of residence, January
    to March 2022 and 2026, in thousands with 95 per cent confidence intervals: residents, not jobs, by where people
    live, sections not classes"""
    rng = np.random.default_rng(seed)
    sections = [("A", "Agriculture, forestry and fishing", 0.012), ("B-E", "Production", 0.071), ("F", "Construction", 0.083),
                ("G", "Wholesale and retail trade; repair of motor vehicles", 0.142), ("H", "Transportation and storage", 0.046),
                ("I", "Accommodation and food service activities", 0.071), ("J", "Information and communication", 0.039),
                ("K", "Financial and insurance activities", 0.068), ("L-N", "Real estate, professional and administrative", 0.121),
                ("O", "Public administration and defence", 0.074), ("P", "Education", 0.087), ("Q", "Human health and social work", 0.139),
                ("R-U", "Other services", 0.047)]
    pop = dict(RKG=146.0, DOR=61.0, GLN=52.0, ING=47.0, NSH=40.0, SKL=31.0)
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Employment by industry"
    ws.append(["Labour Force Survey: residents aged 16 and over in employment by industry of main job and district of residence (thousands)"])
    ws.append(["Torvasay Statistics. January to March. Estimates from a sample of households; confidence intervals at 95 per cent."])
    ws.append([])
    ws.append(["District", "Section", "Industry", "Jan-Mar 2022", "95% CI +/-", "Jan-Mar 2026", "95% CI +/-"])
    for code, name in N.DISTRICTS_NAMES:
        for sec, title, sh in sections:
            a = pop[code] * sh * float(rng.normal(1, 0.06))
            b = a * float(rng.normal(1.02, 0.05))
            ci = lambda x: 1.96 * np.sqrt(x * (1 - x / pop[code]) / (pop[code] * 0.9)) * 2.4
            ws.append([name, sec, title, round(a, 1), round(ci(a), 1), round(b, 1), round(ci(b), 1)])
    ws["A1"].font = Font(bold=True)
    for cell in ws[4]:
        cell.font = Font(bold=True)
    ws.freeze_panes = "D5"
    for col, wd in zip("ABCDEFG", [12, 8, 52, 12, 11, 12, 11]):
        ws.column_dimensions[col].width = wd
    ws.append([])
    ws.append(["Industry is that of the respondent's main job (SIC 2007 sections). Estimates under 1.0 thousand are less reliable."])
    wb.save(path)
    return len(N.DISTRICTS_NAMES) * len(sections)
