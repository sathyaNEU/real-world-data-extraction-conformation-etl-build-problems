"""The golden deliverables from the shipped pack (bundle.py): enrolment_gap_allocation_2027.csv, the organisers chart,
and generator/figures.json with every figure submission.md states."""
import csv
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt   # noqa: E402

import bundle as B      # noqa: E402
import calibrate as C   # noqa: E402
import methods as M     # noqa: E402
import world as W       # noqa: E402

CSV_NAME = "enrolment_gap_allocation_2027.csv"
PNG_NAME = "enrolment_gap_allocation_2027.png"
COLS = ["REGION_CODE", "REGION", "ORGANISERS", "NEW_ELECTORS", "REMOVED_DIED"]


def r1(v, k=1):
    return round(float(v), k)


def figures(pk):
    d = pk.d
    est = M.dse_cells(d)
    fac = M.factors(d, est)
    rg = C.rungs(d)
    gold_adults, dse_adults = rg["R3 golden"], rg["R2 dual-system cells"]
    alloc, quota = M.allocate(pk.gap(gold_adults))
    dse_alloc, _ = M.allocate(pk.gap(dse_adults))
    census_alloc, _ = M.allocate(pk.gap(rg["R0 census counts"]))
    national_alloc, _ = M.allocate(pk.gap(rg["R1 one national ratio"]))
    da = M.demographic(d)
    groups = {}
    for g in W.ADULT_GROUPS:
        lo, hi = g
        m_dse = sum(v for (c, s, gg), v in est.items() if s == "M" and gg == g)
        f_dse = sum(v for (c, s, gg), v in est.items() if s == "F" and gg == g)
        m_da = sum(da.get(("M", a), 0) for a in range(lo, min(hi, 100) + 1))
        f_da = sum(da.get(("F", a), 0) for a in range(lo, min(hi, 100) + 1))
        groups[W.group_label(g)] = {
            "men_dse": int(round(m_dse)), "women_dse": int(round(f_dse)), "men_da": int(round(m_da)),
            "women_da": int(round(f_da)), "ratio_dse": round(m_dse / f_dse, 2), "ratio_da": round(m_da / f_da, 2),
            "factor": round(fac[g], 3) if g in fac else None}
    m_dse = sum(v for (c, s, g), v in est.items() if s == "M" and g in W.YOUNG_GROUPS)
    m_da = sum(da.get(("M", a), 0) for a in range(18, 50))
    young = {"short_pct": int(round(100 * (1 - m_dse / m_da)))}
    factors_pct = [int(round(100 * (fac[g] - 1))) for g in W.YOUNG_GROUPS]
    ne, rd = pk.new_electors(), pk.removed_dead()
    regions = []
    for c in W.CODES:
        regions.append({"code": c, "name": W.NAME[c], "organisers": alloc[c], "default_organisers": dse_alloc[c],
                        "new_electors": ne[c], "removed_died": rd[c]})
    changed = [c for c in W.CODES if alloc[c] != dse_alloc[c]]
    fig = {
        "call": {"organisers": {W.NAME[c]: alloc[c] for c in W.CODES}, "total": sum(alloc.values())},
        "default": {"organisers": {W.NAME[c]: dse_alloc[c] for c in W.CODES},
                    "changed": [W.NAME[c] for c in changed], "n_changed": len(changed)},
        "census_only": {"n_changed": sum(1 for c in W.CODES if census_alloc[c] != alloc[c])},
        "national_ratio": {"n_changed": sum(1 for c in W.CODES if national_alloc[c] != alloc[c])},
        "national": {
            "electors": int(sum(d["roll"].values())),
            "dse_adults": int(round(sum(dse_adults.values()))),
            "dse_adults_million": round(sum(dse_adults.values()) / 1e6, 2),
            "golden_adults_million": round(sum(gold_adults.values()) / 1e6, 2),
        },
        "groups": groups,
        "young_men": young,
        "factors_pct": factors_pct,
        "regions": regions,
        "asks": {"new_electors": {W.NAME[c]: ne[c] for c in W.CODES}, "removed_died": {W.NAME[c]: rd[c] for c in W.CODES},
                 "new_total": sum(ne.values()), "died_total": sum(rd.values())},
        "margin": round(M.margin(quota, alloc), 3),
        "stated": {"age_groups": [18, 24, 25, 34, 35, 49], "plan_sections": ["2.2", "3.1"],
                   "new_platform_transfer_stamps_utc": ["18:00", "17:00"], "window": "5 March 2025 to 30 June 2026"},
    }
    return fig


def write_csv(fig, path):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(COLS)
        for r in fig["regions"]:
            w.writerow([r["code"], r["name"], r["organisers"], r["new_electors"], r["removed_died"]])


def write_png(fig, path):
    regions = fig["regions"]
    names = [r["name"] for r in regions]
    vals = [r["organisers"] for r in regions]
    plt.rcParams["font.family"] = "DejaVu Sans"
    f, ax = plt.subplots(figsize=(10.5, 5.6), dpi=110)
    bars = ax.bar(range(len(names)), vals, color="#3d6b8c", width=0.66)
    for b, v in zip(bars, vals):
        ax.text(b.get_x() + b.get_width() / 2, v + 0.4, str(v), ha="center", va="bottom", fontsize=9, color="#1b1d1f")
    ax.set_xticks(range(len(names)))
    ax.set_xticklabels(names, rotation=40, ha="right", fontsize=9)
    ax.set_ylabel("Field organisers")
    ax.set_ylim(0, max(vals) * 1.15)
    ax.set_title("2027 enrolment campaign: the 200 field organisers by region", fontsize=12, loc="left")
    ax.text(0, -0.36, "Shared on each region's adults not on the roll on census day, 4 March 2025 (field plan, section "
            "3).", transform=ax.transAxes, fontsize=8.2, color="#5b6067")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.yaxis.grid(True, color="#e3e6ea", linewidth=0.8)
    ax.set_axisbelow(True)
    f.tight_layout()
    f.savefig(path, metadata={"Software": None, "Creation Time": None})
    plt.close(f)


def main(target, gdir, fig_path):
    pk = B.Pack(target)
    fig = figures(pk)
    os.makedirs(gdir, exist_ok=True)
    write_csv(fig, os.path.join(gdir, CSV_NAME))
    write_png(fig, os.path.join(gdir, PNG_NAME))
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return fig
