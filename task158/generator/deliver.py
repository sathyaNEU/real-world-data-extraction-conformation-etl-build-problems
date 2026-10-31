"""task158 goldens: stopgap_q1_2027.xlsx and pool_out_of_service_nov2026.png, generator/figures.json and
submission.md, every figure computed from the shipped pack by calc.py and emitted, never typed."""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calc as C            # noqa: E402
import common as K          # noqa: E402
import postprocess as PP    # noqa: E402

F_XLSX = "stopgap_q1_2027.xlsx"
F_PNG = "pool_out_of_service_nov2026.png"


def figures(target):
    M = C.main_call(target)
    P = C.pilot(M, target)
    gh, lo = C.ask_a(target)
    acc, held = C.ask_b(target)
    F = {}
    F["pick"] = M["pick"]
    F["shortfall"] = K.nearest(M["docs_peak"], 10)
    F["shortfall_exact"] = M["docs_peak"]
    F["peak_week"] = M["docs_week"]
    F["a_ms"] = round(M["a"] * 1000, 3)
    F["b_ms"] = round(M["b"] * 1000, 2)
    F["reports_full"] = K.nearest(M["reports_full"], 10)
    F["reports_full_exact"] = M["reports_full"]
    F["alloc_w13"] = M["plan"]["docs-prod"][12]
    F["docs_gpr"] = M["gpr"]["docs-prod"]
    devs = [abs(1 - C.pilot_ratio(M, target, u, g)[0]) for u in (False, True) for g in (None, M["gpr"]["docs-prod"])]
    F["pilot_within_pct"] = int(math.ceil(max(devs) * 100 + 0.5))       # the bound holds on every day and rate basis
    F["runner_up"] = sorted((p for p in K.POOLS if p != M["pick"]), key=lambda p: -M["sf"][p]["peak"])[0]
    F["runner_up_shortfall"] = K.nearest(M["sf"][F["runner_up"]]["peak"], 10)
    F["pilot_req_fifth"] = P["ratio"]["Docs GPU-seconds per request"]
    F["pilot_pack_share"] = P["ratio"]["the pack computed once a report"]
    F["pilot_calls"] = P["calls"]
    F["gh"] = {p: K.nearest(gh[p], 10) for p in K.POOLS}
    F["gh_exact"] = gh
    F["longest"] = {p: round(lo[p], 1) for p in K.POOLS}
    F["longest_exact"] = lo
    F["accepted"] = acc
    F["held"] = held
    F["accepted_total"] = sum(acc.values())
    F["eleven"] = len(M["live"])
    F["M"], F["P"] = M, P
    return F


def held_by_rack(target, held):
    import csv
    inv = list(csv.DictReader(open(os.path.join(target, C.F_HANDOVER), encoding="utf-8")))
    rack = {x["node"]: x["rack"] for x in inv}
    out = {r: [] for r in ("R11", "R12", "R13", "R14")}
    for n in held:
        out[rack[n]].append(n)
    return out


# ------------------------------------------------------------------------------------------------- the workbook
THIN = Side(style="thin", color="B4BCC8")
HEAD = PatternFill("solid", fgColor="E6EBF2")


def _head(ws, row):
    for c in ws[row]:
        if c.value is not None:
            c.font = Font(bold=True)
            c.fill = HEAD
            c.border = Border(bottom=THIN)
            c.alignment = Alignment(wrap_text=True, vertical="top")


def write_xlsx(path, F, hb):
    wb = Workbook()
    ws = wb.active
    ws.title = "Stopgap Q1 2027"
    ws.append(["Stopgap cluster to %s: %d GPUs short in its peak week, 2027-W%02d"
               % (F["pick"], F["shortfall"], F["peak_week"])])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Fleet capacity, 7 December 2026. Assigned under the stopgap policy of 16 November 2026, sections 2 to 5."])
    ws["A2"].font = Font(italic=True, color="52514E")
    ws.merge_cells("A2:D2")
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[2].height = 30
    ws.append([])
    ws.append(["Pool", "Product", "Q1 peak-week shortfall (GPUs, nearest 10)", "Peak week"])
    _head(ws, 4)
    ws.append([F["pick"], K.PRODUCT[F["pick"]], F["shortfall"], "2027-W%02d" % F["peak_week"]])
    ws.cell(row=5, column=3).number_format = "#,##0"
    ws.cell(row=5, column=4).alignment = Alignment(horizontal="center")
    ws.cell(row=4, column=4).alignment = Alignment(horizontal="center", vertical="top")
    ws.append([])
    ws.append(["Basis"])
    ws["A7"].font = Font(bold=True)
    basis = [
        ("Traffic", "Q1 2027 capacity intake, each week's busiest-hour figure as filed (Voice's requests per second "
                    "times 3,600)."),
        ("Interactive cost", "Each pool's Q3 2026 GPU-seconds per request as the close-out of 16 October reports it "
                             "(policy section 3)."),
        ("Report service", "The %s signed contracts in the commitments export of 4 December, each at its contracted "
                           "peak from its go-live Monday, at its tier's calls, prompt and completion limits."
                           % F["eleven"]),
        ("Report call cost", "lc2 at %.3f GPU-ms per prompt token computed and %.2f per completion token, fitted on "
                             "batch-prod's lc2-2026.05 hours; every report call is its own session."
                             % (F["a_ms"], F["b_ms"])),
        ("Allocation", "Fleet plan Q1 2027, issue v3 of 1 December, the week's allocation."),
        ("Rounding", "Shortfalls compared unrounded and reported to the nearest 10 GPUs."),
    ]
    for k, v in basis:
        ws.append([k, v])
        r = ws.max_row
        ws.cell(row=r, column=1).font = Font(color="52514E")
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
        ws.cell(row=r, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.cell(row=r, column=1).alignment = Alignment(vertical="top")
        ws.row_dimensions[r].height = 15 * math.ceil(len(v) / 70.0)
    for col, w in zip("ABCD", (18, 12, 30, 22)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "A5"

    o = wb.create_sheet("Out of service Nov 2026")
    top = max(K.POOLS, key=lambda p: F["gh"][p])
    o.append(["%s lost the most GPU-hours to cordoned nodes in November 2026" % top])
    o["A1"].font = Font(bold=True, size=12)
    o.append(["UTC. A node's eight GPUs are out from its cordon to its uncordon, in fleetctl or the ops console, once "
              "while cordoned; hours go to the pool the node was in at the time."])
    o["A2"].font = Font(italic=True, color="52514E")
    o.merge_cells("A2:C2")
    o["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    o.row_dimensions[2].height = 45
    o.append(["Pool", "GPU-hours out of service (nearest 10)", "Longest stay out, one node (hours)"])
    _head(o, 3)
    for p in K.POOLS:
        o.append([p, F["gh"][p], F["longest"][p]])
        o.cell(row=o.max_row, column=2).number_format = "#,##0"
        o.cell(row=o.max_row, column=3).number_format = "0.0"
    for col, w in zip("ABC", (16, 24, 24)):
        o.column_dimensions[col].width = w
    o.freeze_panes = "A4"

    a = wb.create_sheet("Stopgap acceptance")
    a.append(["Acceptance review of 4 December 2026: %d of the cluster's 240 GPUs accepted" % F["accepted_total"]])
    a["A1"].font = Font(bold=True, size=12)
    a.append(["Lease Schedule 3 on the results reported by the review; racks as in Noordermeer's handover inventory."])
    a["A2"].font = Font(italic=True, color="52514E")
    a.merge_cells("A2:C2")
    a["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    a.row_dimensions[2].height = 30
    a.append(["Rack", "GPUs accepted", "Nodes held back (node ids)"])
    _head(a, 3)
    for r in ("R11", "R12", "R13", "R14"):
        a.append([r, F["accepted"][r], ", ".join(hb[r]) if hb[r] else "none"])
        a.cell(row=a.max_row, column=2).alignment = Alignment(horizontal="center")
    a.append(["Cluster", F["accepted_total"], ""])
    a.cell(row=a.max_row, column=2).alignment = Alignment(horizontal="center")
    a.cell(row=a.max_row, column=1).font = Font(bold=True)
    a.cell(row=a.max_row, column=2).font = Font(bold=True)
    a.cell(row=a.max_row, column=1).border = Border(top=THIN)
    a.cell(row=a.max_row, column=2).border = Border(top=THIN)
    for col, w in zip("ABC", (12, 16, 34)):
        a.column_dimensions[col].width = w
    a.freeze_panes = "A4"
    wb.save(path)
    PP.normalize_ooxml(path, K.PEOPLE["analyst"], K.PEOPLE["analyst"], "2026-12-07T08:05:00Z", "2026-12-07T15:42:00Z",
                       excel=True, company=K.ORG_LEGAL)


# ------------------------------------------------------------------------------------------------- the chart
def write_png(path, F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    matplotlib.rcParams["svg.hashsalt"] = "task158"
    pools = sorted(K.POOLS, key=lambda p: F["gh"][p])
    vals = [F["gh"][p] for p in pools]
    fig, ax = plt.subplots(figsize=(8.0, 4.2), dpi=120)
    fig.patch.set_facecolor("#fcfcfb")
    ax.set_facecolor("#fcfcfb")
    ax.barh(range(len(pools)), vals, height=0.55, color="#2a78d6")
    for i, v in enumerate(vals):
        ax.text(v + max(vals) * 0.012, i, "{:,}".format(v), va="center", ha="left", fontsize=9.5, color="#0b0b0b")
    ax.set_yticks(range(len(pools)))
    ax.set_yticklabels(pools, fontsize=9.5, color="#52514e")
    ax.set_xlim(0, max(vals) * 1.16)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: "{:,.0f}".format(x)))
    ax.tick_params(axis="x", labelsize=8.5, colors="#52514e")
    ax.grid(axis="x", color="#e4e3df", linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#c9c8c3")
    ax.set_xlabel("GPU-hours out of service, November 2026 (UTC)", fontsize=9, color="#52514e")
    top = max(K.POOLS, key=lambda p: F["gh"][p])
    fig.text(0.02, 0.955, "%s lost the most GPU-hours to cordoned nodes in November" % top, ha="left", va="top",
             fontsize=12, fontweight="bold", color="#0b0b0b")
    fig.text(0.02, 0.895, "From each node's cordon to its uncordon, by the pool the node was in; nearest 10 GPU-hours",
             ha="left", va="top", fontsize=9, color="#52514e")
    fig.tight_layout(rect=(0, 0, 1, 0.86))
    fig.savefig(path, dpi=120, facecolor=fig.get_facecolor(), metadata={"Software": None})
    plt.close(fig)


# ------------------------------------------------------------------------------------------------- figures.json and the write-up
def figures_json(F, hb):
    G = {
        "call": {"pool": F["pick"], "shortfall": "%d" % F["shortfall"], "week": "W%02d" % F["peak_week"],
                 "runner_up": F["runner_up"], "runner_up_shortfall": "%d" % F["runner_up_shortfall"]},
        "components": {"a_ms": "%.3f" % F["a_ms"], "b_ms": "%.2f" % F["b_ms"], "reports_full": "%d" % F["reports_full"],
                       "alloc_w13": "%d" % F["alloc_w13"]},
        "steps": {"carry": "2,520", "busy": "70", "rps": "3,600", "docs_gpr": "%.4f" % F["docs_gpr"],
                  "pilot_within_pct": "%d" % F["pilot_within_pct"], "pilot_calls": K.fmt_int(F["pilot_calls"]),
                  "gbit": "8", "bw_floor": "360", "eleven": "11", "six": "6", "review_local": "14:00",
                  "review_utc": "13:00"},
        "answers": {
            "out_of_service": {p: {"gpu_hours": K.fmt_int(F["gh"][p]), "longest": "%.1f" % F["longest"][p]}
                               for p in K.POOLS},
            "acceptance": {r: {"accepted": "%d" % F["accepted"][r], "held": hb[r]} for r in ("R11", "R12", "R13", "R14")},
            "accepted_total": "%d" % F["accepted_total"],
            "stopgap_gpus": "240",
        },
    }
    return G


def submission(F, hb):
    pick = F["pick"]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** General Statistics & Data Science (regression and classification model diagnostics: GPU busy "
             "time regressed on the prompt tokens a model computes and the tokens it generates, the specification chosen "
             "on its out-of-sample fit to an early-access tenant).")
    L.append("**Analytical objective:** Forecasting & Predictive Modeling.")
    L.append("")
    L.append("## 1. Final Recommendation")
    L.append("")
    L.append("**Give the stopgap cluster to docs-prod (Docs): its Q1 peak-week shortfall is %d GPUs, in 2027-W%02d.**"
             % (F["shortfall"], F["peak_week"]))
    L.append("Docs' eleven signed report-service contracts need about %d GPUs at their contracted peaks once all are "
             "live, because each report call is its own session and lc2 computes its whole prompt. Not %s (%s, %d GPUs "
             "short), which leads only when report calls are priced at Docs' GPU-seconds per request, a rate set by "
             "follow-up turns that re-send a document their session already holds. Not a costing at Docs' own rates "
             "per token, per session or per new session, or at the early-access tenant's cost per call or per report: "
             "each under-prices the report prompts and leaves %s first. Not a source pack shared across a report's "
             "calls either: each call opens its own session, and the tenant's busy time matches every call computing "
             "its whole prompt."
             % (F["reports_full"], F["runner_up"], K.PRODUCT[F["runner_up"]], F["runner_up_shortfall"],
                K.PRODUCT[F["runner_up"]]))
    L.append("")
    L.append("## 2. Critical Components")
    L.append("")
    L.append("1. lc2 costs **%.3f** GPU-milliseconds per prompt token it computes and **%.2f** per completion token."
             % (F["a_ms"], F["b_ms"]))
    L.append("2. The eleven signed report-service contracts at their contracted peaks need about **%d** GPUs once all "
             "are live." % F["reports_full"])
    L.append("3. docs-prod's shortfall peaks in **2027-W%02d**, against the **%d** GPUs the fleet plan allocates it "
             "that week." % (F["peak_week"], F["alloc_w13"]))
    L.append("")
    L.append("## 3. Step-by-Step Solution")
    L.append("")
    L.append("1. Read stopgap_assignment_policy_2026-11.pdf: a week's requirement is the busiest hour's busy GPU-seconds "
             "over 2,520 (70 per cent busy), signed contracts count at contracted peak from the go-live Monday at their "
             "tier's calls and limits, and the cluster goes to the largest Q1 peak-week shortfall against the fleet plan.")
    L.append("2. Costed every pool's busiest-hour requests in q1_2027_capacity_intake.xlsx (Voice's requests per second "
             "times 3,600) at its Q3 GPU-seconds per request in capacity_closeout_2026Q3.pdf, as the policy files "
             "(Docs %.4f)." % F["docs_gpr"])
    L.append("3. Fitted gpu_busy_s on prompt_tokens and completion_tokens over the batch-prod hours tagged lc2-2026.05 "
             "in fleet_rollup_hourly_2026-01-01_2026-12-06.csv, where every request is one call and nothing is reused: "
             "%.3f and %.2f GPU-milliseconds." % (F["a_ms"], F["b_ms"]))
    L.append("4. Checked those rates on the early-access tenant's %s report calls in "
             "docs_usage_by_org_daily_2026-09-01_2026-12-06.csv (5 October to 4 December; on those days the rollup's "
             "sessions_new exceeds billing's app and API sessions by one per call): on Amsterdam or UTC days, at the "
             "close-out's %.4f or the exact Q3 rate, they come within %d per cent of the busy GPU-seconds docs-prod ran "
             "on those days above its other requests, where Docs' rate per request predicts about a fifth."
             % (K.fmt_int(F["pilot_calls"]), F["docs_gpr"], F["pilot_within_pct"]))
    L.append("5. Priced each signed contract in report_service_commitments_2026-12-04.xlsx at its tier's calls per "
             "report times its prompt and completion limits per call at those rates, from its go-live week: about %d "
             "GPUs once all eleven are live." % F["reports_full"])
    L.append("6. Subtracted each week's allocation in fleet_plan_2027Q1.xlsx: docs-prod's largest weekly shortfall "
             "is %d GPUs, in 2027-W%02d, the largest of the six pools." % (F["shortfall"], F["peak_week"]))
    L.append("7. For the out-of-service table, joined fleetctl's cordon and uncordon steps with the console's cordons, "
             "uncordons and hand-completed jobs (Europe/Amsterdam times converted to UTC), counted eight GPUs per node "
             "from cordon to uncordon in November and gave each hour to the node's pool at the time "
             "(fleet_nodes_2026-12-06.csv), as the stopgap policy's section 6 counts them.")
    L.append("8. For acceptance, applied lease_schedule3_acceptance.pdf to the latest burn-in run of each fitted GPU "
             "serial and each node's latest all-reduce in nx7_fabric_results.csv finished before the 14:00 Amsterdam "
             "review (13:00 UTC), Gbit/s runs divided by 8 before the 360 GB/s line, racks as in "
             "nx7_handover_inventory_2026-12-04.csv.")
    L.append("")
    L.append("## 4. Deliverable Answers")
    L.append("")
    L.append("### stopgap_q1_2027.xlsx")
    L.append("")
    L.append("1. The stopgap goes to docs-prod (Docs), Q1 peak-week shortfall %d GPUs (2027-W%02d)."
             % (F["shortfall"], F["peak_week"]))
    L.append("2. Out of service in November 2026, GPU-hours to the nearest 10 and the longest stay in hours:")
    for p in K.POOLS:
        L.append("   - %s: %s GPU-hours, longest %.1f hours" % (p, K.fmt_int(F["gh"][p]), F["longest"][p]))
    L.append("3. Accepted at the 4 December review, whole GPUs, with the node ids of any nodes held back:")
    for r in ("R11", "R12", "R13", "R14"):
        L.append("   - %s: %d GPUs accepted; nodes held back: %s" % (r, F["accepted"][r],
                                                                    ", ".join(hb[r]) if hb[r] else "none"))
    L.append("")
    L.append("### pool_out_of_service_nov2026.png")
    L.append("")
    L.append("4. A bar for each of the six pools, its November GPU-hours out of service labelled at the bar's end, "
             "%s the longest bar, titled with the pool that lost the most." % max(K.POOLS, key=lambda p: F["gh"][p]))
    L.append("")
    return "\n".join(L)


def main(target, golden, figures_path, submission_path):
    F = figures(target)
    hb = held_by_rack(target, F["held"])
    os.makedirs(golden, exist_ok=True)
    write_xlsx(os.path.join(golden, F_XLSX), F, hb)
    write_png(os.path.join(golden, F_PNG), F)
    G = figures_json(F, hb)
    with open(figures_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(G, f, indent=2, ensure_ascii=False)
        f.write("\n")
    with open(submission_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(submission(F, hb))
    return F


if __name__ == "__main__":
    T = os.path.dirname(HERE)
    main(os.path.join(T, "target"), os.path.join(T, "golden"), os.path.join(HERE, "figures.json"),
         os.path.join(T, "submission.md"))
