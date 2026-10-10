#!/usr/bin/env python3
"""November patch round, the two deliverables: november_ticket_cut.csv and
ticket_split_review.pptx. Reads only <task>/target and writes into <task>/golden.

    python3 golden.py /path/to/task128

Rules, each as the pack states it:
  exploitable    latest exploit-prediction score at least 0.10 (standard s.2; history to 22 Oct)
  cloud ticket   one package on one estate, closed in place within the month (standard s.3, s.4),
                 taking out every exploitable finding on that package
  drains         per November window: hosts in service, less the hosts the forecast peak over the
                 window's own hours needs, less one rack, times the window's drain cycles (SRE s.2)
  colocated      a drained host comes back on the current image: every open exploitable finding on
                 it goes. One ticket per estate on the package the standard's s.3 selects, carried
                 below its fixed version by every drained host; the drains go to the most exposed hosts
  the 300        two colocated tickets, then the 298 cloud tickets that take out the most
"""
import csv
import collections
import datetime as dt
import io
import json
import math
import os
import statistics
import sys
import zipfile

import openpyxl
import pyarrow.parquet as pq

ESTATES = ["payments", "checkout", "search", "media", "tools", "pipeline"]
COLO = ["payments", "checkout"]
CLOUD = ["search", "media", "tools", "pipeline"]
LABEL = {"payments": "Payments", "checkout": "Checkout", "search": "Search", "media": "Media",
         "tools": "Internal tools", "pipeline": "Data pipeline"}
TICKETS = 300
THRESH = 0.10
AS_OF = dt.date(2026, 10, 23)
ASK_A_FROM = dt.date(2026, 5, 1)
TARGET_DAYS = 35
COVER_DAYS = 14

CUT = "november_ticket_cut.csv"
DECK = "ticket_split_review.pptx"


def nearest_ten(x):
    return int(math.floor(x / 10 + 0.5) * 10)


def _csv(target, name):
    with open(os.path.join(target, name), encoding="utf-8") as f:
        return list(csv.DictReader(f))


def _sheet(target, name, sheet):
    ws = openpyxl.load_workbook(os.path.join(target, name), read_only=True)[sheet]
    rows = ws.iter_rows(values_only=True)
    hdr = next(rows)
    return [dict(zip(hdr, r)) for r in rows]


def latest_scores(target):
    t = pq.read_table(os.path.join(target, "epss_score_history_2026.parquet"),
                      columns=["cve", "score_date", "epss"]).to_pydict()
    last = {}
    for cve, d, s in zip(t["cve"], t["score_date"], t["epss"]):
        d = str(d)
        if cve not in last or d > last[cve][0]:
            last[cve] = (d, s)
    return {c: v[1] for c, v in last.items()}


def cloud_candidates(target, latest):
    """{(estate, package): (exposures, hosts)} over exploitable open findings, and the estate's open
    exploitable exposure today."""
    exp = collections.Counter()
    hosts = collections.defaultdict(set)
    for r in _csv(target, "vuln_findings_2026-10-23.csv"):
        if latest.get(r["cve"], 0.0) >= THRESH:
            k = (r["estate"], r["package"])
            exp[k] += 1
            hosts[k].add(r["host_id"])
    open_today = collections.Counter()
    for (e, _), v in exp.items():
        open_today[e] += v
    return {k: (v, len(hosts[k])) for k, v in exp.items()}, open_today


def colocated_findings(target):
    """Per colocated host, its open exploitable findings as (package, cve, score)."""
    out = collections.defaultdict(list)
    estate = {}
    with open(os.path.join(target, "colocation_managed_host_findings_2026-10-23.jsonl"),
              encoding="utf-8") as f:
        for line in f:
            o = json.loads(line)
            if o["epss"] >= THRESH:
                out[o["host_id"]].append((o["package"], o["cve"], o["epss"]))
                estate[o["host_id"]] = o["estate"]
    return out, estate


def november_drains(target):
    """{estate: drains in November} and the per-window detail."""
    cap = {}
    for d in _sheet(target, "colocation_capacity_register_2026-10.xlsx", "Capacity"):
        if str(d["month"]) == "2026-11":
            cap[d["estate"]] = (int(d["hosts_in_service"]), float(d["per_host_tps"]),
                                int(d["failure_domain_hosts"]))
    tps = {}
    for r in _csv(target, "estate_transaction_forecast_2026.csv"):
        tps[(r["estate"], r["date"], int(r["hour"]))] = float(r["tps"])
    drains = collections.Counter()
    detail = []
    for r in _csv(target, "november_window_calendar.csv"):
        e = r["estate"]
        n, per_host, rack = cap[e]
        start = dt.datetime.fromisoformat(f"{r['window_date']}T{r['window_hours_local'][:5]}")
        end_h = int(r["window_hours_local"][6:8])
        length = (end_h - start.hour) % 24 or 24
        hours = [start + dt.timedelta(hours=k) for k in range(length)]
        peak = max(tps[(e, h.date().isoformat(), h.hour)] for h in hours)
        concurrent = n - math.ceil(peak / per_host) - rack
        drains[e] += concurrent * int(r["drain_cycles"])
        detail.append((e, r["window_date"], concurrent, int(r["drain_cycles"])))
    return dict(drains), detail


def colocated_ticket(findings, estate_of, e, drains):
    """The estate's one ticket: drain its `drains` most exposed hosts (ties by host id); the package
    is the one carried by every drained host whose highest-scoring finding there scores highest."""
    hosts = sorted((h for h in findings if estate_of[h] == e), key=lambda h: (-len(findings[h]), h))
    drained = hosts[:drains]
    cover = collections.Counter()
    top = {}
    for h in drained:
        for pkg in {p for p, _, _ in findings[h]}:
            cover[pkg] += 1
        for pkg, _, s in findings[h]:
            top[pkg] = max(top.get(pkg, 0.0), s)
    full = sorted((p for p, n in cover.items() if n == len(drained)), key=lambda p: (-top[p], p))
    if not full:
        raise SystemExit(f"no package is carried by every drained {e} host")
    return {"estate": e, "package": full[0], "hosts": len(drained),
            "exposures": sum(len(findings[h]) for h in drained)}


def ticket_cut(target):
    latest = latest_scores(target)
    cands, open_today = cloud_candidates(target, latest)
    findings, estate_of = colocated_findings(target)
    for h, e in estate_of.items():
        open_today[e] += len(findings[h])
    drains, _ = november_drains(target)
    tickets = [colocated_ticket(findings, estate_of, e, drains[e]) for e in COLO]
    rank = {e: i for i, e in enumerate(ESTATES)}
    cloud = sorted(((v, rank[e], e, p, nh) for (e, p), (v, nh) in cands.items()),
                   key=lambda x: (-x[0], x[1], x[3]))
    n_cloud = TICKETS - len(tickets)
    for v, _, e, p, nh in cloud[:n_cloud]:
        tickets.append({"estate": e, "package": p, "hosts": nh, "exposures": v})
    nxt = cloud[n_cloud]
    first_below = {"estate": nxt[2], "package": nxt[3], "hosts": nxt[4], "exposures": nxt[0]}
    tickets.sort(key=lambda t: (-t["exposures"], rank[t["estate"]], t["package"]))
    if not (cloud[n_cloud - 2][0] > cloud[n_cloud - 1][0] > nxt[0] > cloud[n_cloud + 1][0]):
        raise SystemExit("the line is not strict: the last ticket in or the first below is tied")
    split = collections.Counter(t["estate"] for t in tickets)
    taken = collections.Counter()
    for t in tickets:
        taken[t["estate"]] += t["exposures"]
    return {"tickets": tickets, "split": {e: split[e] for e in ESTATES},
            "taken": {e: taken[e] for e in ESTATES}, "total": sum(taken.values()),
            "last_in": tickets[-1], "first_below": first_below, "drains": drains,
            "open_today": {e: open_today[e] for e in ESTATES}}


def patch_pace(target):
    """Ask A: per estate, median days from the vendor's first release to the day the ticket's last
    host ran the fix successfully, over tickets completed 1 May to 23 October, and the count over
    the 35-day target."""
    runs = collections.defaultdict(list)
    for r in _csv(target, "crew_deployment_log_2026.csv"):
        runs[r["ticket_id"]].append(r)
    gaps = collections.defaultdict(list)
    for tid, rs in runs.items():
        ok = [dt.date.fromisoformat(r["run_date"]) for r in rs if r["outcome"] == "succeeded"]
        if not ok:
            continue
        done = max(ok)
        if not (ASK_A_FROM <= done <= AS_OF):
            continue
        rel = min(dt.date.fromisoformat(r["vendor_first_release"]) for r in rs)
        gaps[rs[0]["estate"]].append((done - rel).days)
    return {e: {"median_days": round(statistics.median(gaps[e]), 1),
                "missed": sum(1 for g in gaps[e] if g > TARGET_DAYS), "tickets": len(gaps[e])}
            for e in ESTATES}


def scan_coverage(target):
    """Ask B: per cloud estate, running hosts on 23 October and how many of them have no
    authenticated scan on or after 9 October, joined on the stable instance id."""
    edge = AS_OF - dt.timedelta(days=COVER_DAYS)
    last = {}
    for r in _csv(target, "scanner_coverage_2026-10.csv"):
        if r["last_authenticated_scan"]:
            d = dt.date.fromisoformat(r["last_authenticated_scan"][:10])
            last[r["instance_id"]] = max(d, last.get(r["instance_id"], d))
    out = {e: {"in_service": 0, "unscanned": 0} for e in CLOUD}
    for r in _csv(target, "cloud_asset_register_2026-10-23.csv"):
        if r["power_state"] != "running":
            continue
        out[r["estate"]]["in_service"] += 1
        if r["instance_id"] not in last or last[r["instance_id"]] < edge:
            out[r["estate"]]["unscanned"] += 1
    return out


def write_cut(path, cut):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["rank", "estate", "package", "hosts_reached_nov", "exposures_taken_out_nov"])
        for i, t in enumerate(cut["tickets"], 1):
            w.writerow([i, LABEL[t["estate"]], t["package"], t["hosts"], t["exposures"]])


def chart_order(cut):
    """Estates in ticket order: most tickets first; payments and checkout, one ticket each, in the
    order their tickets sit on the cut list."""
    pos = {}
    for i, t in enumerate(cut["tickets"]):
        pos.setdefault(t["estate"], i)
    return sorted(ESTATES, key=lambda e: (-cut["split"][e], pos[e]))


def render_chart(path, cut):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.ticker import FuncFormatter
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10.5, "svg.hashsalt": "t128"})
    order = chart_order(cut)
    nov = [cut["taken"][e] for e in order]
    today = [cut["open_today"][e] for e in order]
    ink, muted, grid = "#1f2933", "#5f6b7a", "#e4e7eb"
    c_nov, c_open = "#2a78d6", "#a9c8ee"
    fig, ax = plt.subplots(figsize=(11.2, 4.9), dpi=150)
    x = list(range(len(order)))
    w = 0.38
    ax.bar([i - w / 2 for i in x], today, w, color=c_open, label="Open exploitable exposure, 23 Oct",
           zorder=2, edgecolor="white", linewidth=1.2)
    ax.bar([i + w / 2 for i in x], nov, w, color=c_nov, label="Taken out in November",
           zorder=2, edgecolor="white", linewidth=1.2)
    for i, e in enumerate(order):
        ax.text(i + w / 2, nov[i] + 70, f"{nearest_ten(nov[i]):,}", ha="center", va="bottom",
                fontsize=9.5, color=ink)
        if e in COLO:
            t = next(t for t in cut["tickets"] if t["estate"] == e)
            ax.annotate(f"1 ticket, {t['hosts']} hosts drained\nof {cut['open_today'][e]:,} open",
                        xy=(i + w / 2, nov[i] + 260), xytext=(i, today[i] + 330),
                        ha="center", fontsize=9, color=ink,
                        arrowprops={"arrowstyle": "-", "color": muted, "lw": 0.8})
    ax.set_xticks(x)
    ax.set_xticklabels([f"{LABEL[e]}\n{cut['split'][e]} ticket{'s' if cut['split'][e] != 1 else ''}"
                        for e in order], color=ink)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v):,}"))
    ax.set_ylabel("Exploitable host exposures", color=muted)
    ax.set_ylim(0, max(today + nov) * 1.22)
    ax.grid(axis="y", color=grid, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#9aa5b1")
    ax.tick_params(axis="y", length=0, colors=muted)
    ax.tick_params(axis="x", length=0)
    ax.set_title(f"November takes out {nearest_ten(cut['total']):,} exploitable host exposures",
                 loc="left", fontsize=13, color=ink, fontweight="bold", pad=14)
    ax.legend(loc="upper left", frameon=False, fontsize=9.5)
    fig.tight_layout()
    fig.savefig(path, format="png", metadata={"Software": None})
    plt.close(fig)


# ---------------------------------------------------------------- the review deck
def _deck_helpers():
    from pptx.util import Pt, Inches
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    ink, muted, rule, head = (RGBColor(0x1F, 0x29, 0x33), RGBColor(0x5F, 0x6B, 0x7A),
                              RGBColor(0xD9, 0xDE, 0xE4), RGBColor(0x24, 0x3B, 0x53))

    def text(slide, x, y, w, h, runs, size=14, color=ink, bold=False, align=None):
        box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
        tf = box.text_frame
        tf.word_wrap = True
        for i, line in enumerate(runs if isinstance(runs, list) else [runs]):
            p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
            if align:
                p.alignment = align
            p.space_after = Pt(5)
            r = p.add_run()
            r.text = line
            r.font.size, r.font.bold, r.font.color.rgb, r.font.name = Pt(size), bold, color, "Calibri"
        return box

    def table(slide, x, y, w, rows, widths, size=12, bold_last=False, left=(0,)):
        shp = slide.shapes.add_table(len(rows), len(rows[0]), Inches(x), Inches(y), Inches(w),
                                     Inches(0.36 * len(rows)))
        tbl = shp.table
        tbl.first_row = True
        for j, cw in enumerate(widths):
            tbl.columns[j].width = Inches(cw)
        for i, row in enumerate(rows):
            for j, val in enumerate(row):
                c = tbl.cell(i, j)
                c.fill.solid()
                c.fill.fore_color.rgb = head if i == 0 else RGBColor(0xFF, 0xFF, 0xFF)
                c.margin_left = c.margin_right = Inches(0.08)
                p = c.text_frame.paragraphs[0]
                p.alignment = PP_ALIGN.LEFT if j in left else PP_ALIGN.RIGHT
                r = p.add_run()
                r.text = str(val)
                r.font.name, r.font.size = "Calibri", Pt(size if i else size - 1)
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF) if i == 0 else ink
                r.font.bold = i == 0 or (bold_last and i == len(rows) - 1)
        return tbl

    def footer(slide, n):
        text(slide, 0.5, 7.05, 9.5, 0.3, "Vulnerability Management Office  |  November 2026 patch "
             "round  |  extracts as at 23 Oct 2026", 9, muted)
        text(slide, 12.2, 7.05, 0.6, 0.3, str(n), 9, muted, align=PP_ALIGN.RIGHT)

    return text, table, footer, muted


def write_deck(path, cut, pace, cover, chart_png):
    from pptx import Presentation
    from pptx.util import Inches
    text, table, footer, muted = _deck_helpers()
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    sp, tk = cut["split"], cut["taken"]
    pay = next(t for t in cut["tickets"] if t["estate"] == "payments")
    chk = next(t for t in cut["tickets"] if t["estate"] == "checkout")

    s = prs.slides.add_slide(blank)
    text(s, 0.5, 0.35, 12.3, 0.8, "November split: one ticket each to payments and checkout, "
         f"{TICKETS - 2} to cloud", 24, bold=True)
    text(s, 0.5, 1.1, 12.3, 0.5, f"Takes out {nearest_ten(cut['total']):,} exploitable host "
         "exposures in November. Crews cut on Monday 2 November.", 15, muted)
    rows = [["Estate", "Tickets", "Exposures taken out in Nov (nearest 10)"]]
    rows += [[LABEL[e], sp[e], f"{nearest_ten(tk[e]):,}"] for e in ESTATES]
    rows += [["Total", TICKETS, f"{nearest_ten(cut['total']):,}"]]
    table(s, 0.5, 1.9, 7.4, rows, [2.4, 1.3, 3.7], 13, bold_last=True)
    text(s, 8.3, 1.9, 4.5, 3.2, [
        f"Payments and checkout get one {pay['package']} ticket each.",
        f"The provider can drain {pay['hosts']} payments hosts and {chk['hosts']} checkout hosts in "
        "our November windows, keeping one rack above each window's forecast peak. A drained host "
        "comes back on the current platform image, so each drain clears everything open on it. The "
        "ticket names the most exposed hosts; a second ticket there buys no extra drains.",
        "Payments does carry the worst exposure per host, but the drains, not the ticket count, "
        "set what it can give up in November.",
    ], 12)
    li, fb = cut["last_in"], cut["first_below"]
    rows = [["At the line", "Estate", "Package update", "Hosts", "Takes out"],
            [f"Last in (rank {TICKETS})", LABEL[li["estate"]], li["package"], li["hosts"],
             li["exposures"]],
            ["First below the line", LABEL[fb["estate"]], fb["package"], fb["hosts"],
             fb["exposures"]]]
    table(s, 0.5, 5.15, 7.4, rows, [2.1, 1.5, 1.6, 0.9, 1.3], 12, left=(0, 1, 2))
    text(s, 8.3, 5.2, 4.5, 1.4, "Drains per window: SRE maintenance standard s.2, against the "
         "hourly forecast and the Guadalhorce capacity register. Exploitable: latest score of at "
         "least 0.10 (vulnerability management standard v3, s.2).", 10, muted)
    footer(s, 1)

    s = prs.slides.add_slide(blank)
    s.shapes.add_picture(chart_png, Inches(0.5), Inches(0.45), width=Inches(12.3))
    text(s, 0.5, 6.35, 12.3, 0.5, "Estates in ticket order. Open exposure counts every exploitable "
         "finding open on 23 Oct (latest score of at least 0.10).", 11, muted)
    footer(s, 2)

    s = prs.slides.add_slide(blank)
    text(s, 0.5, 0.35, 12.3, 0.8, "Estate card: checkout is slowest to patch, media has the most "
         "hosts without a recent scan", 24, bold=True)
    rows = [["Estate", "Median days, first fix release to last host",
             f"Tickets over {TARGET_DAYS}-day target", "Hosts in service 23 Oct",
             "No authenticated scan in 14 days"]]
    for e in ESTATES:
        rows.append([LABEL[e], f"{pace[e]['median_days']:.1f}", pace[e]["missed"],
                     f"{cover[e]['in_service']:,}" if e in cover else "provider managed",
                     f"{cover[e]['unscanned']:,}" if e in cover else "provider managed"])
    table(s, 0.5, 1.3, 12.3, rows, [2.3, 2.9, 2.2, 2.4, 2.5], 13)
    text(s, 0.5, 4.15, 12.3, 0.9, [
        "Patch pace: tickets completed 1 May to 23 Oct, crew deployment log; a rolled-back run "
        "does not count as the fix landing.",
        "Coverage: running instances only, matched to the scanner on instance ID; covered means an "
        "authenticated scan on or after 9 Oct.",
    ], 11, muted)
    footer(s, 3)

    cp = prs.core_properties
    cp.author = cp.last_modified_by = "Reina Guzmán"
    cp.title = "November patch round, ticket split"
    cp.subject, cp.keywords, cp.comments, cp.category = "", "", "", ""
    cp.created = cp.modified = dt.datetime(2026, 10, 23, 17, 40)
    cp.revision = 3
    buf = io.BytesIO()
    prs.save(buf)
    _stable_zip(buf.getvalue(), path)


def _stable_zip(data, path):
    zin = zipfile.ZipFile(io.BytesIO(data))
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zout:
        for i in zin.infolist():
            zi = zipfile.ZipInfo(i.filename, date_time=(2026, 10, 23, 17, 40, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = i.external_attr
            zout.writestr(zi, zin.read(i.filename))


def build(task):
    target, golden = os.path.join(task, "target"), os.path.join(task, "golden")
    os.makedirs(golden, exist_ok=True)
    cut = ticket_cut(target)
    pace = patch_pace(target)
    cover = scan_coverage(target)
    write_cut(os.path.join(golden, CUT), cut)
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        png = os.path.join(tmp, "chart.png")
        render_chart(png, cut)
        write_deck(os.path.join(golden, DECK), cut, pace, cover, png)
    return cut, pace, cover


def report(cut, pace, cover):
    print(f"November drains: payments {cut['drains']['payments']}, checkout {cut['drains']['checkout']}")
    for t in cut["tickets"][:2]:
        print(f"  {LABEL[t['estate']]}: one {t['package']} ticket, {t['hosts']} most exposed hosts, "
              f"{t['exposures']:,} exposures")
    print("Split (tickets / exposures taken out in November, nearest ten):")
    for e in ESTATES:
        print(f"  {LABEL[e]:<14} {cut['split'][e]:>3}  {cut['taken'][e]:>6,}  ~{nearest_ten(cut['taken'][e]):,}")
    print(f"  Total          {TICKETS}  {cut['total']:>6,}  ~{nearest_ten(cut['total']):,}")
    li, fb = cut["last_in"], cut["first_below"]
    print(f"Last in: {LABEL[li['estate']]} {li['package']} {li['exposures']}; "
          f"first below: {LABEL[fb['estate']]} {fb['package']} {fb['exposures']}")
    for e in ESTATES:
        line = f"  {LABEL[e]:<14} median {pace[e]['median_days']:.1f} d, {pace[e]['missed']} over target"
        if e in cover:
            line += f"; {cover[e]['in_service']} in service, {cover[e]['unscanned']} unscanned"
        print(line)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    report(*build(sys.argv[1]))
