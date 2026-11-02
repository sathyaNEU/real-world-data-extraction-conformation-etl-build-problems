"""Golden deliverables from target/ alone: the conformed section file, the chart and the network workbook."""
import datetime as dt
import os

import numpy as np

import analysis as AN
import common as C
import est


def r1(v):
    return float("%.1f" % (np.floor(v * 10 + 0.5) / 10))


def r10(v):
    return int(np.floor(v / 10.0 + 0.5) * 10)


def rthou(v):
    return int(np.floor(v / 1000.0 + 0.5))


def compute(tgt):
    R = AN.compute(tgt)
    out = {"sections": []}
    for r in sorted(R["secs"], key=lambda r: r["road"]):
        ann = est.bin01(r["gold_aadf"])
        basis = ("section's own detector %s, counted day" % ", ".join(r["dets"])) if r["dets"] else \
            "%s permanent counters, counted day" % r["setting"]
        out["sections"].append({"cp": r["cp"], "road": r["road"], "from": r["from"], "to": r["to"], "length": r["length"],
                                "date": r["date"].isoformat(), "annual": r1(ann), "annual_raw": ann,
                                "over": ann > 3.0, "basis": basis, "default": est.bin01(r["default_aadf"])})
    out["over"] = [s["road"] for s in out["sections"] if s["over"]]
    out["n_over"] = len(out["over"])
    out["default_over"] = sorted(s["road"] for s in out["sections"] if s["default"] > 3.0)
    P = R["P"]
    out["counters"] = []
    for sid in sorted(P["sites"]):
        s = P["sites"][sid]
        out["counters"].append({"site": sid, "road": s["road"], "setting": s["setting"],
                                "hgv": r10(R["askA"]["switch"][sid]), "hgv_raw": R["askA"]["switch"][sid]})
    out["approaches"] = []
    for (jn, arm), v in sorted(R["askB"]["remap"].items()):
        out["approaches"].append({"junction": jn, "approach": arm, "thousands": rthou(v), "raw": v})
    out["switch"] = R["sw"].isoformat()
    out["R"] = R
    return out


def write_golden(tgt, gld):
    os.makedirs(gld, exist_ok=True)
    G = compute(tgt)
    C.write_csv(os.path.join(gld, "noise_round_sections_2025.csv"),
                ["count_point_id", "road", "start_junction", "end_junction", "length_km", "count_date",
                 "annual_traffic_2025_millions", "over_three_million", "expansion_basis"],
                [[s["cp"], s["road"], s["from"], s["to"], "%.2f" % s["length"], s["date"], "%.1f" % s["annual"],
                  "yes" if s["over"] else "no", s["basis"]] for s in G["sections"]])
    chart(G, os.path.join(gld, "section_traffic_2025.png"))
    workbook(G, os.path.join(gld, "traffic_network_2025.xlsx"))
    return G


def chart(G, path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams["svg.hashsalt"] = "t484"
    secs = sorted(G["sections"], key=lambda s: s["annual_raw"])
    fig, ax = plt.subplots(figsize=(8.6, 6.2), dpi=110)
    y = np.arange(len(secs))
    cols = ["#b5462f" if s["over"] else "#7d8b99" for s in secs]
    ax.barh(y, [s["annual"] for s in secs], color=cols, height=0.66)
    ax.axvline(3.0, color="#222222", lw=1.1, ls="--")
    ax.text(3.02, len(secs) - 0.4, "3.0 million vehicle passages", fontsize=8, va="top")
    ax.set_yticks(y)
    ax.set_yticklabels(["%s (%d)" % (s["road"], s["cp"]) for s in secs], fontsize=8)
    for yi, s in zip(y, secs):
        ax.text(s["annual"] + 0.04, yi, "%.1f" % s["annual"], va="center", fontsize=7.5)
    ax.set_xlabel("2025 annual traffic, millions of motor vehicles (both directions)")
    ax.set_xlim(0, max(s["annual"] for s in secs) + 0.6)
    ax.set_title("Sections counted in 2025: %d over three million vehicles" % G["n_over"], fontsize=10.5, loc="left")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def workbook(G, path):
    import openpyxl
    from openpyxl.styles import Font
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Counters"
    ws.append(["Permanent counters: average daily heavy goods vehicles, 2025"])
    ws["A1"].font = Font(bold=True)
    ws.append(["site_id", "road", "setting", "hgv_per_day_2025"])
    for c in G["counters"]:
        ws.append([c["site"], c["road"], c["setting"], c["hgv"]])
    ws2 = wb.create_sheet("Junction approaches")
    ws2.append(["Vehicles recorded by each approach's detectors in 2025 (thousands)"])
    ws2["A1"].font = Font(bold=True)
    ws2.append(["junction", "approach", "vehicles_recorded_2025_thousands"])
    for a in G["approaches"]:
        ws2.append([a["junction"], a["approach"], a["thousands"]])
    for w in (ws, ws2):
        w.column_dimensions["A"].width = 30
        w.column_dimensions["B"].width = 22
        w.column_dimensions["C"].width = 22
        w.column_dimensions["D"].width = 18
    C.save_workbook(wb, path, dt.datetime(2026, 3, 23, 15, 10), "Irene Griffiths")


def figures(G):
    f = {"n_over": G["n_over"], "threshold_m": "3.0", "threshold_passages": "3,000,000"}
    for s in G["sections"]:
        f["annual_%d" % s["cp"]] = "%.1f" % s["annual"]
        f["cp_%d" % s["cp"]] = s["cp"]
        f["length_%d" % s["cp"]] = "%.2f" % s["length"]
    for c in G["counters"]:
        f["hgv_%s" % c["site"]] = c["hgv"]
    for a in G["approaches"]:
        f["appr_%s_%s" % (a["junction"], a["approach"])] = "{:,}".format(a["thousands"])
    f["switch_date"] = G["switch"]
    return f


if __name__ == "__main__":
    import sys
    G = write_golden(sys.argv[1], sys.argv[2])
    for s in G["sections"]:
        print(s["road"], s["annual"], s["over"], round(s["default"], 2))
    print(G["n_over"], G["over"])
    print(G["counters"])
    print(G["approaches"])
