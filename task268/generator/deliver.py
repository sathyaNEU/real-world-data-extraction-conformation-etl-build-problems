"""task268's golden deliverables, drawn from one figure set: reliability_review_2026.docx, the annual reliability
review's latency note (the services that breached, every service's December SLI beside its budget, the chart of each
SLI against its own budget line, how the SLI was read), and service_sli_2026.csv, a row per service with its SLI,
budget, verdict, releases and rollbacks, and customer-facing incident minutes and cloud cost in each half."""
import csv
import io
from decimal import Decimal, ROUND_HALF_UP

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
from docx import Document               # noqa: E402
from docx.enum.text import WD_ALIGN_PARAGRAPH   # noqa: E402
from docx.shared import Cm, Pt, RGBColor        # noqa: E402

import common as K   # noqa: E402

matplotlib.rcParams["svg.hashsalt"] = "task268"
matplotlib.rcParams["font.family"] = "DejaVu Sans"


def whole(x):
    return int(Decimal(repr(float(x))).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def names(lst):
    return ", ".join(lst[:-1]) + " and " + lst[-1] if len(lst) > 1 else lst[0]


def figures(R):
    m = R["main"]
    F = {"over": list(R["over"]), "over_count": len(R["over"]),
         "sli": {s: "%.1f" % m[s]["sli1"] for s in K.SVC},
         "budget": {s: "%.1f" % K.BUDGET[s] for s in K.SVC},
         "threshold_ms": {s: "{:,}".format(K.THRESHOLD[s]) for s in K.SVC},
         "ran_over": {s: "yes" if m[s]["over"] else "no" for s in K.SVC},
         "pg_service_hour": "%.1f" % K.r1(m["partner-gateway"]["by_service_hour"]),
         "kept_share": {s: "%.1f" % K.r1(m[s]["unweighted"]) for s in K.SVC},
         "pg_kept_mix_pct": {k: "%d" % whole(100 * v) for k, v in m["partner-gateway"]["root_mix_kept"].items() if k},
         "pg_weighted_mix_pct": {k: "%d" % whole(100 * v) for k, v in m["partner-gateway"]["root_mix_weighted"].items()
                                 if k},
         "releases": {s: R["deploys"][s]["releases"] for s in K.SVC},
         "rollbacks": {s: R["deploys"][s]["rollbacks"] for s in K.SVC},
         "minutes": {s: [whole(v) for v in R["incidents"][s]] for s in K.SVC},
         "cost_eur": {s: [whole(v) for v in R["costs"][s]] for s in K.SVC},
         "cost_eur_text": {s: ["{:,}".format(whole(v)) for v in R["costs"][s]] for s in K.SVC},
         "minutes_text": {s: ["{:,}".format(whole(v)) for v in R["incidents"][s]] for s in K.SVC}}
    return F


def chart_png(F):
    fig, ax = plt.subplots(figsize=(7.2, 4.1), dpi=150)
    svcs = list(K.SVC)[::-1]
    y = range(len(svcs))
    vals = [float(F["sli"][s]) for s in svcs]
    cols = ["#c0392b" if F["ran_over"][s] == "yes" else "#7f8c8d" for s in svcs]
    ax.barh(list(y), vals, color=cols, height=0.62)
    for i, s in enumerate(svcs):
        b = float(F["budget"][s])
        ax.plot([b, b], [i - 0.42, i + 0.42], color="#1f2d3d", linewidth=2.2)
        ax.text(max(vals[i], b) + 0.06, i, F["sli"][s], va="center", fontsize=8.5, color="#1f2d3d")
    ax.set_yticks(list(y))
    ax.set_yticklabels(["%s (budget %s%%)" % (s_, F["budget"][s_]) for s_ in svcs], fontsize=8.5)
    i_pg = svcs.index("partner-gateway")
    ax.annotate("%s%% against %s%%" % (F["sli"]["partner-gateway"], F["budget"]["partner-gateway"]),
                xy=(float(F["sli"]["partner-gateway"]), i_pg), xytext=(float(F["sli"]["partner-gateway"]) - 1.15, i_pg + 1.2),
                fontsize=8, color="#c0392b", arrowprops=dict(arrowstyle="-", color="#c0392b", lw=0.8))
    ax.set_title("%s services over their own error budget, December 2026" % ("Five" if len(F["over"]) == 5 else
                 str(len(F["over"]))), fontsize=10, loc="left", color="#1f2d3d")
    ax.set_xlabel("Latency SLI, December 2026 (% of requests slower than the threshold)", fontsize=8.5)
    ax.set_xlim(0, max(vals) + 0.6)
    ax.tick_params(axis="x", labelsize=8)
    for sp_ in ("top", "right"):
        ax.spines[sp_].set_visible(False)
    from matplotlib.lines import Line2D
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(color="#c0392b", label="over budget"), Patch(color="#7f8c8d", label="within budget"),
                       Line2D([0], [0], color="#1f2d3d", linewidth=2.2, label="error budget")],
              fontsize=8, frameon=False, loc="upper right")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def _p(doc, text, bold=False, size=10.5, italic=False, space=4, color=None):
    para = doc.add_paragraph()
    run = para.add_run(text)
    run.bold, run.italic = bold, italic
    run.font.size = Pt(size)
    if color:
        run.font.color.rgb = RGBColor(*color)
    para.paragraph_format.space_after = Pt(space)
    return para


def write_docx(path, R, F):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for sec in doc.sections:
        sec.left_margin = sec.right_margin = Cm(2.2)
        sec.top_margin = sec.bottom_margin = Cm(2.0)
    _p(doc, "Rotalinha Platform Reliability", bold=True, size=9, color=(0x55, 0x55, 0x55))
    _p(doc, "To: Engineering leadership group    From: %s, Platform Reliability    Date: 8 January 2027"
       % K.PEOPLE["head"], size=9, space=0)
    _p(doc, "Ref: PR-SLO-3 annual review 2026, latency objectives, read over December 2026 in Lisbon time", size=9,
       space=10)
    _p(doc, "%s services ran over their latency budget in 2026" % ("Five" if len(F["over"]) == 5 else
       str(len(F["over"]))), bold=True, size=16, space=8)
    footer = doc.sections[0].footer.paragraphs[0]
    footer.text = "PR-SLO-3 annual review 2026    page "
    footer.runs[0].font.size = Pt(8)
    _page_field(footer)
    over = F["over"]
    _p(doc, "%s services ran over their 2026 latency error budget and get a reliability engineer for January to June "
            "2027: %s." % ("Five" if len(over) == 5 else str(len(over)), names(over)), bold=True, size=11.5, space=8)
    pg = "partner-gateway"
    _p(doc, "Partner-gateway is the one a quick read misses: its SLI is %s%% against a %s%% budget, where the share "
            "of its spans the tracing store kept would put it at %s%% and a reweighting of its own spans hour by hour "
            "at %s%%. Journey-search, places and seat-map breach their 1.0%% budgets at %s%%, %s%% and %s%%, and "
            "notifications at %s%%."
       % (F["sli"][pg], F["budget"][pg], F["kept_share"][pg], F["pg_service_hour"], F["sli"]["journey-search"],
          F["sli"]["places"], F["sli"]["seat-map"], F["sli"]["notifications"]), space=8)

    tbl = doc.add_table(rows=1, cols=5)
    tbl.style = "Table Grid"
    for i, h in enumerate(["Service", "Threshold (ms)", "Latency SLI (%)", "Error budget (%)", "Ran over"]):
        c = tbl.rows[0].cells[i]
        c.text = h
        c.paragraphs[0].runs[0].bold = True
        _shade(c, "DCE6F0")
    for s in K.SVC:
        row = tbl.add_row().cells
        for i, v in enumerate([s, F["threshold_ms"][s], F["sli"][s], F["budget"][s], F["ran_over"][s]]):
            row[i].text = v
            if i:
                row[i].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    _p(doc, "Source: trace_spans_2026-12.parquet and lb_target_group_requests_2026-H2.csv; thresholds and budgets from "
            "PR-SLO-3 section 4.", italic=True, size=8, space=8)
    doc.add_picture(io.BytesIO(chart_png(F)), width=Cm(16.0))
    _p(doc, "Each bar is the service's December SLI; the dark mark on it is the service's own error budget.",
       italic=True, size=8.5, space=10)

    _p(doc, "How the SLI was read", bold=True, size=12, space=4)
    kept, wtd = F["pg_kept_mix_pct"], F["pg_weighted_mix_pct"]
    _p(doc, "The tracing store keeps a trace whole or not at all, and the decision is taken where the trace starts: "
            "each edge service keeps about the same number of traces every hour whatever its traffic, so a busy hour "
            "is kept thinly. Each kept server span therefore counts for the requests its "
            "trace's edge service handled that hour over the traces it kept, from the load balancer's hourly counts; "
            "the SLI is the weighted slow spans over the service's December requests (PR-SLO-3 sections 2 and 3).")
    _p(doc, "For an internal service the weight belongs to the edge request that started the trace, not to the "
            "service itself. Partner-gateway's kept spans come %s%% from journey-search's traces, %s%% from "
            "seat-map's and %s%% from booking's, while journey-search's searches make %s%% of its requests, and those "
            "availability lookups are the slow ones; weighting its spans by its own hourly keep share under-counts "
            "them." % (kept.get("journey-search", "0"), kept.get("seat-map", "0"), kept.get("booking", "0"),
                       wtd.get("journey-search", "0")))
    _p(doc, "Releases and rollbacks, customer-facing incident minutes and cloud cost by half are in "
            "service_sli_2026.csv, under PR-SLO-3 section 5.", space=10)
    _p(doc, "Notes: SLIs are per cents to one decimal and are compared with the budget as rounded (PR-SLO-3 3.2). "
            "December in Lisbon time is UTC throughout. The load balancer's health probes are not requests "
            "(PR-SLO-3 2.2) and the trace export's re-sent spans are counted once.", italic=True, size=8.5)
    doc.save(path)


def _shade(cell, fill):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    tc = cell._tc.get_or_add_tcPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), fill)
    tc.append(sh)


def _page_field(par):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    run = par.add_run()
    run.font.size = Pt(8)
    for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            fc = OxmlElement("w:fldChar")
            fc.set(qn("w:fldCharType"), kind)
            run._r.append(fc)
        else:
            it = OxmlElement("w:instrText")
            it.set(qn("xml:space"), "preserve")
            it.text = text
            run._r.append(it)


def write_csv(path, R, F):
    with open(path, "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["service", "latency_sli_pct", "error_budget_pct", "ran_over", "releases_2026", "rollbacks_2026",
                     "incident_minutes_h1", "incident_minutes_h2", "cost_eur_h1", "cost_eur_h2"])
        for s in K.SVC:
            wr.writerow([s, F["sli"][s], F["budget"][s], F["ran_over"][s], F["releases"][s], F["rollbacks"][s],
                         F["minutes"][s][0], F["minutes"][s][1], F["cost_eur"][s][0], F["cost_eur"][s][1]])
