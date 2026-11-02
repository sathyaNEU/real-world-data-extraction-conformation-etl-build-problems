"""Two files a statistician would weigh and the solution does not use: the Labour Force Survey's employment by broad
occupational category, and an aggregator's index of online job postings. Named in metadata.json only."""
import datetime as dt
import os

import numpy as np

import common as C

BROAD = [
    ("0", "Legislative and senior management occupations", 0.075),
    ("1", "Business, finance and administration occupations", 0.152),
    ("2", "Natural and applied sciences and related occupations", 0.087),
    ("3", "Health occupations", 0.094),
    ("4", "Occupations in education, law and social, community and government services", 0.118),
    ("5", "Occupations in art, culture, recreation and sport", 0.029),
    ("6", "Sales and service occupations", 0.241),
    ("7", "Trades, transport and equipment operators and related occupations", 0.143),
    ("8", "Natural resources, agriculture and related production occupations", 0.031),
    ("9", "Occupations in manufacturing and utilities", 0.030),
]
SEAS = {"0": [1, 1, 1, 1, 1], "1": [1, 1.01, 0.99, 1, 1], "2": [1, 1, 1, 1.01, 1], "3": [1, 1, 1, 1, 1.01],
        "4": [0.95, 1.03, 1.02, 1.01, 0.96], "5": [1.06, 0.97, 0.94, 1.0, 1.07], "6": [1.03, 1.0, 0.96, 0.99, 1.04],
        "7": [1.06, 1.0, 0.91, 1.0, 1.07], "8": [1.22, 0.95, 0.78, 0.98, 1.24], "9": [1.01, 1.0, 0.98, 1.0, 1.01]}


def write_lfs(tgt, rng):
    quarters = ["2025-07", "2025-10", "2026-01", "2026-04", "2026-07"]
    total = [641.8, 636.2, 622.9, 633.5, 646.1]
    rows = []
    for qi, q in enumerate(quarters):
        vals = []
        for code, title, share in BROAD:
            v = total[qi] * share * SEAS[code][qi] * (1.0 + rng.normal(0.0, 0.012))
            vals.append((code, title, round(v, 1)))
        tot = round(sum(v for _, _, v in vals), 1)
        rows.append([q, "Laurentide", "Employment", "Total, all occupations", "Persons in thousands", "%.1f" % tot, ""])
        for code, title, v in vals:
            status = "E" if code in ("5", "8", "9") else ""
            rows.append([q, "Laurentide", "Employment", "%s %s" % (code, title), "Persons in thousands", "%.1f" % v,
                         status])
    C.write_csv(os.path.join(tgt, "lfs_employment_by_occupation_laurentide_quarterly.csv"),
                ["REF_DATE", "GEO", "Labour force characteristics", "National Occupational Classification (NOC)",
                 "UOM", "VALUE", "STATUS"], rows)


def write_postings_index(tgt, rng):
    months = []
    d = dt.date(2025, 1, 1)
    while d <= dt.date(2026, 10, 1):
        months.append(d)
        d = dt.date(d.year + (d.month == 12), d.month % 12 + 1, 1)
    rows = []
    for code, title, _ in BROAD:
        level = 112.0 + rng.normal(0, 9)
        drift = -0.55 + rng.normal(0, 0.25)
        for k, m in enumerate(months):
            v = level + drift * k + rng.normal(0, 1.6)
            rows.append([m.strftime("%Y-%m"), code, title, "%.1f" % v])
    C.write_csv(os.path.join(tgt, "online_job_postings_index_laurentide_2025-2026.csv"),
                ["month", "noc_broad_category", "category_title", "postings_index_sa_feb2020_100"], rows, crlf=False)


def write_distractors(tgt, seed):
    write_lfs(tgt, np.random.default_rng(seed))
    write_postings_index(tgt, np.random.default_rng(seed + 1))
    return ["lfs_employment_by_occupation_laurentide_quarterly.csv", "online_job_postings_index_laurentide_2025-2026.csv"]
