"""task158 documents: the stopgap assignment policy, the Q3 capacity close-out (computed from the shipped rollup),
the lease's acceptance schedule, the lease terms, the capacity desk's notes on the pull, and the pull log. Their
text is kept here as data so checks.py can quote and execute it."""
from __future__ import annotations

import datetime as dt
import os

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                      # noqa: E402
from reportlab.lib.pagesizes import A4, landscape                                                # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                       # noqa: E402
from reportlab.lib.units import mm                                                    # noqa: E402
from reportlab.pdfbase import pdfmetrics                                              # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                          # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K          # noqa: E402
import postprocess as PP    # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/"
for _n, _f in (("Carlito", "crosextra/Carlito-Regular.ttf"), ("Carlito-Bold", "crosextra/Carlito-Bold.ttf"),
               ("LibSans", "liberation/LiberationSans-Regular.ttf"), ("LibSans-Bold", "liberation/LiberationSans-Bold.ttf")):
    pdfmetrics.registerFont(TTFont(_n, FONT_DIR + _f))
INK = colors.HexColor("#1b1f24")
GREY = colors.HexColor("#5a6270")
ACCENT = colors.HexColor("#1f4e79")
RULE = colors.HexColor("#b4bcc8")
HEAD = colors.HexColor("#e6ebf2")

F_POLICY = "stopgap_assignment_policy_2026-11.pdf"
F_CLOSEOUT = "capacity_closeout_2026Q3.pdf"
F_SCHEDULE = "lease_schedule3_acceptance.pdf"
F_LEASE = "stopgap_lease_terms_2026-11-13.pdf"
F_NOTES = "capacity_desk_notes.md"
F_LOG = "capacity_pull_2026-12-07.log"


def styles(font="Carlito", bold="Carlito-Bold", size=10.4):
    return dict(
        body=ParagraphStyle("b" + font, fontName=font, fontSize=size, leading=size * 1.34, textColor=INK, spaceAfter=5),
        h1=ParagraphStyle("h1" + font, fontName=bold, fontSize=15.5, leading=19.5, textColor=ACCENT, spaceAfter=2),
        sub=ParagraphStyle("s" + font, fontName=font, fontSize=9.0, leading=11.6, textColor=GREY, spaceAfter=10),
        h2=ParagraphStyle("h2" + font, fontName=bold, fontSize=11.0, leading=14.0, textColor=ACCENT, spaceBefore=7,
                          spaceAfter=3),
        cell=ParagraphStyle("c" + font, fontName=font, fontSize=8.4, leading=10.2, textColor=INK),
        cellr=ParagraphStyle("cr" + font, fontName=font, fontSize=8.4, leading=10.2, textColor=INK, alignment=2),
        cellb=ParagraphStyle("cb" + font, fontName=bold, fontSize=8.4, leading=10.2, textColor=INK),
        small=ParagraphStyle("sm" + font, fontName=font, fontSize=8.2, leading=10.4, textColor=GREY, spaceAfter=3))


def _doc(path, title, author, pagesize=A4):
    return SimpleDocTemplate(path, pagesize=pagesize, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=20 * mm,
                             bottomMargin=19 * mm, title=title, author=author, subject="", creator="", producer="")


def _footer(left, font="Carlito", pagesize=A4):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont(font, 7.6)
        canvas.setFillColor(GREY)
        canvas.drawString(22 * mm, 11 * mm, left)
        canvas.drawRightString(pagesize[0] - 22 * mm, 11 * mm, "%d" % doc.page)
        canvas.restoreState()
    return draw


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pdf_stamp(d, hh=9, mi=0):
    return ("D:%04d%02d%02d%02d%02d00+01'00'" % (d.year, d.month, d.day, hh, mi)).encode()


# ---------------------------------------------------------------------------------------------------- the policy
POLICY = [
    ("1. The cluster", [
        "Noordermeer Compute hands over 30 nodes of eight H100 SXM5 80GB GPUs, 240 GPUs in all, at its NX7 site on "
        "Monday 4 January 2027, on the lease of 13 November 2026, for thirteen weeks. The cluster goes whole to one of "
        "the six product pools in the fleet plan (chat-prod, code-prod, agents-prod, docs-prod, batch-prod, "
        "voice-prod) for ISO weeks 2027-W01 to 2027-W13. It is not split between pools.",
    ]),
    ("2. Requirement", [
        "A pool's requirement for a week is the number of GPUs that carries the pool's busiest hour that week at 70 "
        "per cent busy: the busy GPU-seconds of that hour, as the fleet rollup counts them, divided by 2,520.",
    ]),
    ("3. Traffic in the busiest hour", [
        "The busiest hour's traffic is the product team's figure for that week in the Q1 capacity intake, plus the "
        "pool's committed report-service volume. The product team's figure is converted to busy GPU-seconds at the "
        "pool's GPU-seconds per request in the latest quarterly capacity close-out.",
        "A signed report-service contract counts on the pool of the product that sold it, at its contracted peak "
        "reports per hour in every hour from the Monday of its go-live week, each report at its tier's calls per report "
        "and its tier's prompt and completion limits per call. Proposals and ended agreements do not count.",
    ]),
    ("4. Shortfall", [
        "A pool's shortfall for a week is its requirement less the GPUs the Q1 fleet plan allocates the pool that week. "
        "Its Q1 peak-week shortfall is the largest of its thirteen weekly shortfalls.",
    ]),
    ("5. Assignment", [
        "The cluster goes to the pool with the largest Q1 peak-week shortfall. Shortfalls are compared as computed and "
        "reported to the nearest 10 GPUs.",
    ]),
    ("6. What this does not cover", [
        "A pool that does not receive the cluster works its shortfall through its product's capacity runbook "
        "(admission limits, queueing for asynchronous traffic). The AMS-3 hall extension planned for the second "
        "quarter is outside this policy.",
    ]),
]


def write_policy(out):
    st = styles()
    path = os.path.join(out, F_POLICY)
    doc = _doc(path, "Stopgap capacity, Q1 2027", K.PEOPLE["capacity_lead"])
    flow = [Paragraph("Stopgap capacity, Q1 2027: assigning the leased cluster", st["h1"]),
            Paragraph("Fleet capacity, %s. Issued 16 November 2026. Owner: %s." % (K.ORG, K.PEOPLE["capacity_lead"]),
                      st["sub"])]
    for head, paras in POLICY:
        flow.append(Paragraph(head, st["h2"]))
        for p in paras:
            flow.append(Paragraph(esc(p), st["body"]))
    doc.build(flow, onFirstPage=_footer("Slenk fleet capacity: stopgap policy, Q1 2027"),
              onLaterPages=_footer("Slenk fleet capacity: stopgap policy, Q1 2027"))
    PP.normalize_pdf(path, pdf_stamp(K.POLICY_DATE, 10, 12), pdf_stamp(K.POLICY_DATE, 10, 12))


# ---------------------------------------------------------------------------------------------------- the close-out
def closeout_table(rows_by_pool):
    """rows_by_pool: per pool a dict with alloc, busy_h, share, req, sess, ptok, ctok, gpr, peak_hour, peak_gpus."""
    return rows_by_pool


def write_closeout(out, C):
    """C: the close-out figures computed from the shipped rollup (calc.closeout)."""
    st = styles()
    path = os.path.join(out, F_CLOSEOUT)
    doc = _doc(path, "Fleet capacity close-out, Q3 2026", K.PEOPLE["analyst"], pagesize=landscape(A4))
    flow = [Paragraph("Fleet capacity close-out, Q3 2026", st["h1"]),
            Paragraph("1 July to 30 September 2026 (UTC). Fleet capacity, %s. Prepared by %s, 16 October 2026."
                      % (K.ORG, K.PEOPLE["analyst"]), st["sub"])]
    flow.append(Paragraph("Summary", st["h2"]))
    flow.append(Paragraph(esc(
        "The fleet ran %s busy GPU-hours in the quarter, %s per cent of the GPU-hours allocated. Docs added four nodes "
        "on 6 July and Code three on 7 September; Code's agent preview has been live since 14 September."
        % (K.fmt_int(C["fleet_busy_h"]), "%.1f" % C["fleet_share"])), st["body"]))
    flow.append(Paragraph("Table 1. Pools in Q3 2026", st["h2"]))
    head = ["Pool", "GPUs, 30 Sep", "GPU-hours busy (k)", "Busy share", "Requests (m)", "Sessions (m)",
            "Prompt tokens (bn)", "Completion tokens (bn)", "GPU-seconds per request", "Busiest hour (UTC)",
            "Busy GPUs, busiest hour"]
    data = [[Paragraph(h, st["cellb"]) for h in head]]
    for p in K.POOLS:
        r = C["pools"][p]
        data.append([Paragraph(p, st["cell"])] + [Paragraph(x, st["cellr"]) for x in (
            K.fmt_int(r["alloc"]), "%.1f" % (r["busy_h"] / 1000.0), "%.1f%%" % r["share"], "%.1f" % (r["req"] / 1e6),
            "%.2f" % (r["sess"] / 1e6), "%.1f" % (r["ptok"] / 1e9), "%.2f" % (r["ctok"] / 1e9), "%.4f" % r["gpr"],
            r["peak_hour"], K.fmt_int(r["peak_gpus"]))])
    t = Table(data, colWidths=[24 * mm, 17 * mm, 20 * mm, 16 * mm, 19 * mm, 19 * mm, 21 * mm, 23 * mm, 22 * mm,
                               26 * mm, 22 * mm], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), HEAD), ("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE),
                           ("LINEBELOW", (0, -1), (-1, -1), 0.6, RULE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                           ("LEFTPADDING", (0, 0), (-1, -1), 2.5), ("RIGHTPADDING", (0, 0), (-1, -1), 2.5)]))
    flow.append(t)
    flow.append(Spacer(1, 4))
    flow.append(Paragraph(esc(
        "Busy GPU-hours are the rollup's gpu_busy_s summed over the quarter. Busy share is busy GPU-hours over the "
        "GPU-hours allocated. GPU-seconds per request is the quarter's busy GPU-seconds over its completed requests. "
        "The busiest hour is the hour with the most busy GPU-seconds."), st["small"]))
    flow.append(Paragraph("Table 2. Busy GPU-hours by month (thousands)", st["h2"]))
    head2 = ["Pool", "July", "August", "September", "Quarter"]
    data2 = [[Paragraph(h, st["cellb"]) for h in head2]]
    for p in K.POOLS:
        m = C["pools"][p]["months"]
        data2.append([Paragraph(p, st["cell"])] + [Paragraph("%.1f" % (x / 1000.0), st["cellr"]) for x in m + [sum(m)]])
    t2 = Table(data2, colWidths=[30 * mm, 24 * mm, 24 * mm, 24 * mm, 24 * mm], repeatRows=1)
    t2.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), HEAD), ("LINEBELOW", (0, 0), (-1, 0), 0.6, RULE),
                            ("LINEBELOW", (0, -1), (-1, -1), 0.6, RULE), ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]))
    flow.append(t2)
    flow.append(Paragraph("Looking ahead", st["h2"]))
    flow.append(Paragraph(esc(
        "The Q1 2027 capacity intake opens on 2 November and closes on 27 November; the Q1 fleet plan follows on 1 "
        "December."), st["body"]))
    doc.build(flow, onFirstPage=_footer("Slenk fleet capacity: Q3 2026 close-out", pagesize=landscape(A4)),
              onLaterPages=_footer("Slenk fleet capacity: Q3 2026 close-out", pagesize=landscape(A4)))
    PP.normalize_pdf(path, pdf_stamp(K.CLOSEOUT_DATE, 15, 40), pdf_stamp(K.CLOSEOUT_DATE, 15, 40))


# ---------------------------------------------------------------------------------------------------- the lease's acceptance schedule
SCHEDULE = [
    ("3.1 Tests", [
        "Before handover the Provider burns in every GPU of the Cluster (DCGM diagnostics at level 3, a four-hour GEMM "
        "soak and an HBM memory test) and runs an eight-GPU all-reduce on every node (all_reduce_perf, 8 GB messages). "
        "The Provider reports each run in its burn-in and fabric exports, by node and GPU serial.",
    ]),
    ("3.2 Acceptance", [
        "A node passes acceptance when each of its eight GPUs has passed burn-in and the node's eight-GPU all-reduce has "
        "reached 360 GB/s bus bandwidth on its last run. A node that does not is held back, and none of its GPUs counts "
        "as accepted.",
        "Burn-in counts on the GPU fitted at the review: a GPU replaced after its burn-in is burned in again.",
    ]),
    ("3.3 Review", [
        "The parties review acceptance at 14:00 on Friday 4 December 2026, Amsterdam time, on the results reported by "
        "then. The Provider repairs and presents again any node held back; a node accepted later is handed over on its "
        "acceptance.",
    ]),
    ("3.4 Handover", [
        "The Provider hands over the accepted nodes on Monday 4 January 2027 with its handover inventory (rack, "
        "position, node and the serial of each GPU fitted). Fees for a node start on its handover.",
    ]),
]


def write_schedule(out):
    st = styles("LibSans", "LibSans-Bold", 9.8)
    path = os.path.join(out, F_SCHEDULE)
    doc = _doc(path, "Schedule 3: Acceptance", K.PEOPLE["infra"])
    flow = [Paragraph("Schedule 3: Acceptance", st["h1"]),
            Paragraph("Lease of GPU capacity between Noordermeer Compute B.V. (the Provider) and Slenk B.V., 13 November "
                      "2026. Cluster: 30 nodes, NX7 site.", st["sub"])]
    for head, paras in SCHEDULE:
        flow.append(Paragraph(head, st["h2"]))
        for p in paras:
            flow.append(Paragraph(esc(p), st["body"]))
    doc.build(flow, onFirstPage=_footer("Noordermeer Compute / Slenk: GPU lease, Schedule 3", "LibSans"),
              onLaterPages=_footer("Noordermeer Compute / Slenk: GPU lease, Schedule 3", "LibSans"))
    PP.normalize_pdf(path, pdf_stamp(K.LEASE_DATE, 14, 5), pdf_stamp(K.LEASE_DATE, 14, 5))


LEASE = [
    ("1. Cluster and term", [
        "30 nodes, each with eight NVIDIA H100 SXM5 80GB GPUs, 2 TB of system memory and eight 400 Gb/s InfiniBand "
        "ports, at the Provider's NX7 site, connected to the Customer's AMS-3 hall over two 400 Gb/s links. The term is "
        "thirteen weeks from handover on Monday 4 January 2027, extendable by four-week periods on 30 days' notice.",
    ]),
    ("2. Fees", [
        "EUR 2.41 per GPU-hour for each node handed over, billed monthly in arrears; a node held back under Schedule 3 is "
        "not billed until its handover. Power, cooling and remote hands are included.",
    ]),
    ("3. Service", [
        "The Provider keeps 98.5 per cent of handed-over nodes in service in each calendar month, measured from its "
        "monitoring. A node out of service for more than 24 hours is credited for the day.",
    ]),
    ("4. Acceptance", ["Schedule 3."]),
    ("5. Termination", [
        "Either party may end the lease for material breach not remedied within 14 days of notice. The Customer may end "
        "it at any extension date without cause.",
    ]),
]


def write_lease(out):
    st = styles("LibSans", "LibSans-Bold", 9.8)
    path = os.path.join(out, F_LEASE)
    doc = _doc(path, "Lease of GPU capacity", K.PEOPLE["infra"])
    flow = [Paragraph("Lease of GPU capacity: principal terms", st["h1"]),
            Paragraph("Noordermeer Compute B.V. and Slenk B.V. Signed 13 November 2026.", st["sub"])]
    for head, paras in LEASE:
        flow.append(Paragraph(head, st["h2"]))
        for p in paras:
            flow.append(Paragraph(esc(p), st["body"]))
    doc.build(flow, onFirstPage=_footer("Noordermeer Compute / Slenk: GPU lease", "LibSans"),
              onLaterPages=_footer("Noordermeer Compute / Slenk: GPU lease", "LibSans"))
    PP.normalize_pdf(path, pdf_stamp(K.LEASE_DATE, 13, 50), pdf_stamp(K.LEASE_DATE, 13, 50))


# ---------------------------------------------------------------------------------------------------- the desk's notes
def notes_text():
    return """# Capacity desk: notes on the 7 December pull

Casper Heijmans, fleet capacity. Pulled Monday 7 December 2026, 07:40 Amsterdam time. Times are UTC unless a file says
otherwise.

## Fleet rollup (`fleet_rollup_hourly_2026-01-01_2026-12-06.csv`)

One row per pool per hour, 1 January to 6 December 2026, from the capacity rollup (GPU busy time from the node
exporters, counters from the gateway).

- `hour_start_utc`: start of the hour.
- `pool`, `model`: the deployment and the model build it served; both builds, joined by `+`, while a rolling upgrade
  ran.
- `gpus_in_service`: GPUs on the pool's schedulable nodes when the hour closed.
- `gpu_busy_s`: GPU-seconds the pool's GPUs spent running kernels in the hour, summed over its GPUs.
- `requests`: requests completed in the hour. `sessions_new`: sessions opened in the hour.
- `prompt_tokens`, `completion_tokens`: prompt and completion tokens of the hour's completed requests.
- `ttft_p50_ms`, `ttft_p95_ms`: time to first token at the gateway.

A few hours are missing where the collector was down (chat-prod on the morning of 14 August, voice-prod one hour on
3 March).

## Docs usage (`docs_usage_by_org_daily_2026-09-01_2026-12-06.csv`)

Docs usage as billed: one row per organisation, channel and Amsterdam business day, 1 September to 6 December.
Channels: `app` (the web app), `api` (the enterprise API), `report` (the report service). Input tokens are prompt
tokens as billed.

## Maintenance exports

- `fleetctl_jobs_2026-10-26_2026-12-06.jsonl`: every step fleetctl logged for its jobs, one line per step.
- `ops_console_audit_2026-10-26_2026-12-06.csv`: actions taken in the ops console, with the console's own times.
- `fleet_nodes_2026-12-06.csv`: every node with its hall, rack and pool memberships (from, to).

Out of service: a node's GPUs are out of service from the node's cordon until its uncordon. A node cordoned again while
it is cordoned is out once. Hours fall in the month (UTC) they are spent in, and go to the pool the node belonged to at
the time.

## Stopgap cluster (Noordermeer, NX7)

The provider's burn-in and fabric exports (`nx7_burnin_results.csv`, `nx7_fabric_results.csv`) as received on 4
December, and its handover inventory (`nx7_handover_inventory_2026-12-04.csv`). Acceptance is Schedule 3 of the lease.

## Also in the folder

Q3 close-out, Q1 capacity intake, Q1 fleet plan (issue v3), report service commitments (export of 4 December), the stopgap
policy, the lease terms, the H2 incident log and the GPU spec register.
"""


def write_notes(out):
    with open(os.path.join(out, F_NOTES), "w", encoding="utf-8", newline="\n") as f:
        f.write(notes_text())


def write_log(out, rows):
    """rows: [(file, rows, query window)] in pull order."""
    t = dt.datetime(2026, 12, 7, 7, 40, 6)
    lines = ["%s capdesk-pull 2.4.1 start user=c.heijmans profile=q1-2027-stopgap" % t.strftime("%Y-%m-%d %H:%M:%S")]
    for i, (f, n, window) in enumerate(rows):
        t = t + dt.timedelta(seconds=7 + ((n or 17) % 61) // 3 + 4 * (i % 3))
        lines.append("%s wrote %s rows=%s %s" % (t.strftime("%Y-%m-%d %H:%M:%S"), f, n if n is not None else "-",
                                                    window))
    t = t + dt.timedelta(seconds=11)
    lines.append("%s capdesk-pull done files=%d" % (t.strftime("%Y-%m-%d %H:%M:%S"), len(rows)))
    with open(os.path.join(out, F_LOG), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
