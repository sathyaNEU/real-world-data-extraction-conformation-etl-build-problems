"""The golden deliverables: the case to the Director of Pharmacy (PDF with its chart) and the unit's 2026 review
table (CSV), both from figures.json and the cut pack."""
import csv
import datetime as dt
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import Image  # noqa: E402

import pack as K  # noqa: E402
import params as P  # noqa: E402
import world as W  # noqa: E402

PDF = "gravimetric_verification_2027.pdf"
CSV = "compounding_review_2026.csv"


def _fmt(v):
    return ("%.1f" % v) if v >= 0.05 else "under 0.1"


def _ci(ci):
    if ci["hi"] < 0.05:
        return "under 0.1"
    return "%s to %s" % (_fmt(ci["lo"]), _fmt(ci["hi"]))


def chart(path_png, fig):
    cands = sorted(fig["golden"], key=lambda c: fig["golden"][c]["rate"])
    names = [W.product(c)["name"] for c in cands]
    floor = 0.05
    vals = [max(fig["golden"][c]["rate"], floor) for c in cands]
    lo = [max(fig["interval"][c]["lo"], floor) for c in cands]
    hi = [max(fig["interval"][c]["hi"], floor) for c in cands]
    red = set(fig["call"]["products"])
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "svg.hashsalt": "task272"})
    f, ax = plt.subplots(figsize=(7.4, 4.6), dpi=150)
    for i, c in enumerate(cands):
        col = "#c0392b" if c in red else "#7f8c97"
        ax.plot([lo[i], hi[i]], [i, i], color=col, lw=2.2, solid_capstyle="butt")
        ax.plot([lo[i], lo[i]], [i - 0.18, i + 0.18], color=col, lw=1.0)
        ax.plot([hi[i], hi[i]], [i - 0.18, i + 0.18], color=col, lw=1.0)
        ax.plot([vals[i]], [i], marker="o", ms=5.2, color=col, mec="white", mew=0.8)
        g = fig["golden"][c]["rate"]
        ci = fig["interval"][c]
        lab = "under 0.1" if ci["hi"] < 0.05 else "%s (%s)" % (_fmt(g), _ci(ci))
        ax.text(hi[i] * 1.15, i, lab, va="center", fontsize=7.0, color="#333333")
    ax.set_xscale("log")
    ax.set_xlim(floor, 40000)
    ax.set_ylim(-0.7, len(cands) - 0.3)
    ax.axvline(P.LIMIT_PER_100K, color="#1f2d3a", lw=1.1, ls="--")
    ax.text(P.LIMIT_PER_100K * 1.08, len(cands) - 0.45, "PH-QP-07 limit: 10", fontsize=7.8, color="#1f2d3a",
            va="top")
    ax.set_yticks(range(len(cands)))
    ax.set_yticklabels(names, fontsize=7.6)
    ax.set_xlabel("Out-of-tolerance doses per 100,000 doses made (log scale)")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_title("Estimated 2026 out-of-tolerance rate and 90% interval", fontsize=9.5, loc="left")
    f.tight_layout()
    f.savefig(path_png, metadata={"Software": None})
    plt.close(f)


BAGS = ("P0610", "P0614", "P0618")


def _sorts_line(fig):
    n = fig["sorts"]["P0412"]["sorts"] + fig["sorts"]["P0507"]["sorts"]
    if n == 0:
        return "no quarantine sort was opened on either"
    return "only %d quarantine sort%s was opened on them" % (n, "" if n == 1 else "s")


def _bag_loss(fig):
    vals = []
    for c in BAGS:
        p = W.product(c)
        vals.append(-fig["fits"][c]["loss_per_litre"] * p["vol"] * sum(p["size"]) / 2.0 / 1000.0)
    return sum(vals) / len(vals)


def write_pdf(path, fig, tmpdir):
    png = os.path.join(tmpdir, "chart.png")
    chart(png, fig)
    call = fig["call"]["products"]
    rows = [["Product", "Station", "Doses made, 2026", "Out-of-tolerance rate (per 100,000)", "90% interval",
             "Limit of 10", "PH-QP-07 3.1"]]
    where = {"below": "Below the interval", "above": "Above the interval", "inside": "Inside the interval"}
    for c in sorted(fig["golden"], key=lambda c: -fig["golden"][c]["rate"]):
        p = W.product(c)
        g = fig["golden"][c]
        ci = fig["interval"][c]
        rows.append([p["name"], p["station"], "{:,}".format(g["doses"]), _fmt(g["rate"]),
                     _ci(ci), where[ci["limit"]],
                     "In: verify every dose" if c in call else "Out: SC-SOP-12 checks"])
    names = [W.product(c)["name"] for c in sorted(call, key=lambda c: -fig["golden"][c]["rate"])]
    blocks = [
        ("t", "Gravimetric verification at the IV workflow cutover: batch-compounded products"),
        ("s", "To: %s, Director of Pharmacy. From: %s, quality pharmacist, Sterile Compounding Unit. Cc: %s, IV "
              "Workflow Project Lead. 8 February 2027." % (P.PEOPLE["director"], P.PEOPLE["quality"], P.PEOPLE["project"])),
        ("h", "Recommendation"),
        ("p", "Configure %d batch-compounded products for gravimetric verification of every dose at the 5 April 2027 "
              "cutover: %s. Each made more than 10 out-of-tolerance doses per 100,000 doses in 2026 (PH-QP-07 3.1). "
              "The other %d batch products stay on the in-process checks of SC-SOP-12; potassium chloride and "
              "norepinephrine stay on GC-1 (3.2)." % (len(call), ", ".join(names[:-1]) + " and " + names[-1],
                                                     len(fig["golden"]) - len(call))),
        ("h", "How the 2026 rate was estimated"),
        ("p", "PH-QP-07 counts every dose made outside tolerance, weighed or not, and SC-SOP-12 weighs the first dose "
              "of a batch and then one syringe in a hundred or one bag in twenty, so the rate has to come from a model "
              "of the delivered volume. On the peristaltic stations each set "
              "delivers less the more it has pumped: across every set, a product's weighed doses fall in a straight "
              "line with the litres the set had pumped since its set-up, about a start that varies from set to set. "
              "For each product we fitted that start and the loss per litre on the weighed doses (the check register "
              "tied to each dose in the server's dose log, each dose placed on its set from the compounders' set-up "
              "events), took every completed dose at the litres its set had pumped, and added up each dose's chance of "
              "lying outside the product's tolerance."),
        ("p", "The 90 per cent interval on each rate comes from refitting the line on the product's sets drawn again "
              "with replacement, a thousand times, and adding up its 2026 doses each time. The limit sits below the "
              "interval of every product on the list (midazolam's lower bound is %s) and above the interval of every "
              "other product (the highest upper bound is %s), so the list does not turn on where in its interval a "
              "rate falls." % (
                  _fmt(fig["interval"]["P0702"]["lo"]),
                  _fmt(max(fig["interval"][c]["hi"] for c in fig["golden"] if c not in call)))),
        ("p", "The rate is driven by the sets that carried extra batches. Cefazolin 2 g and phenylephrine sets that ran "
              "three batches ended near the bottom of the band after the batch's last weighed dose, so almost none of "
              "their low doses were weighed and %s. Cefoxitin's large batches cross the limit inside a second batch "
              "and its checks caught part of them. Midazolam does not move on PC-4 but sits %.1f per cent under target, "
              "so a small share of every batch falls outside." % (
                  _sorts_line(fig), -fig["fits"]["P0702"]["start"])),
        ("p", "A normal fit to each product's weighed doses (the usual capability figure) would put ampicillin, "
              "piperacillin-tazobactam and vancomycin bags on the list: their sets start %.1f to %.1f per cent high and "
              "lose about %.1f per cent over a batch, so the weights spread wide, but no set comes near the limit "
              "before it is changed." % (min(fig["fits"][c]["start"] for c in BAGS),
                                         max(fig["fits"][c]["start"] for c in BAGS), _bag_loss(fig))),
        ("table", rows),
        ("img", Image(png, width=170 * mm, height=105.7 * mm)),
        ("s", "Sources: compounder dose log and event export (pharmacy server, exported 18 January 2027); gravimetric "
              "check register and quarantine register, 2026; compounded product master; equipment register. Weights "
              "converted to volume with each product's specific gravity; gross weights before 1 July less the "
              "container tare."),
    ]
    K.pdf(path, blocks, "Gravimetric verification at cutover: batch products", P.PEOPLE["quality"],
          K._pdfdate(dt.datetime(2027, 2, 5, 16, 22, 41)), K._pdfdate(dt.datetime(2027, 2, 8, 9, 3, 18)),
          "%s Pharmacy Services   Sterile Compounding Unit" % P.ORG, first_col=0.25,
          subject="Gravimetric verification of batch-compounded products at the April 2027 IV workflow cutover")


def review_rows(fig):
    rows = []
    for k, v in fig["ask_a"].items():
        st, m = k.split()
        rows.append(["doses made", st, "2026-%s" % m, v, "doses"])
    for c, v in fig["ask_b"].items():
        rows.append(["sets used", "%s %s" % (c, W.product(c)["name"]), "2026", v, "sets"])
    return rows


def write_csv(path, fig):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(["measure", "compounder_or_product", "period", "value", "unit"])
    w.writerows(review_rows(fig))
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(buf.getvalue())


def write_all(target, golden, fig, tmpdir):
    os.makedirs(golden, exist_ok=True)
    write_pdf(os.path.join(golden, PDF), fig, tmpdir)
    write_csv(os.path.join(golden, CSV), fig)
