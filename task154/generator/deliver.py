"""The golden deliverables, computed from the shipped pack through calc: the licence variation note (PDF, with the
limiting borehole's drawdown chart and line 3's water use) and the returns check (CSV). Writes figures.json, every
figure the write-up states, as the goldens state it."""
from __future__ import annotations

import datetime as dt
import io
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt                                                      # noqa: E402
from reportlab import rl_config                                                      # noqa: E402

rl_config.invariant = 1
from reportlab.lib import colors                                                     # noqa: E402
from reportlab.lib.pagesizes import A4                                               # noqa: E402
from reportlab.lib.units import mm                                                   # noqa: E402
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import calc as C                                                                     # noqa: E402
import common as K                                                                   # noqa: E402
import docs as D                                                                     # noqa: E402

G_NOTE = "bh2_licence_variation_note.pdf"
G_CSV = "bh2_returns_check.csv"
MONTHS_A = [(2026, m) for m in range(4, 10)]                                   # the returns check, April to September 2026
MONTHS_B = [(2025, m) for m in range(4, 13)] + [(2026, m) for m in range(1, 4)]  # line 3, the 2025-26 licence year
BRAND = colors.HexColor("#0b5563")


def month_label(k):
    return dt.date(k[0], k[1], 1).strftime("%B %Y")


def compute(b):
    mc = C.main_call(b)
    T, S, img = mc["T"], mc["S"], mc["img"]
    largest = C.largest_passing_round(mc["golden"], 100.0)
    assert largest == C.nearest(mc["golden"], 100.0)
    worst = mc["worst"]
    at1800 = {k: int(C.nearest(v, 1.0)) for k, v in mc["at1800"].items()}
    at_largest = {k: C.assessment(largest, xy, T, S, img) for k, xy, _ in mc["prot"]}
    series = {q: C.term_series(b, T, S, img, q, worst) for q in (largest, K.APPLIED_QD)}
    a = C.ask_a(b)
    bb = C.ask_b(b)
    res = dict(mc=mc, largest=largest, worst=worst, at1800=at1800, at_largest=at_largest, series=series,
               ask_a={k: (int(C.nearest(v[0], 100.0)), int(v[1])) for k, v in a.items()},
               ask_a_raw=a, ask_b={k: round(v, 2) for k, v in bb.items()}, ask_b_raw=bb,
               avail={n: av for n, _, av in mc["prot"]})
    return res


def chart_png(res):
    worst = res["worst"]
    avail = res["avail"][worst]
    fig, ax = plt.subplots(figsize=(7.2, 3.5), dpi=150)
    for q, col, lab in ((res["largest"], "#2a78d6", "%s m3/d from April 2027" % "{:,}".format(int(res["largest"]))),
                        (K.APPLIED_QD, "#eb6834", "1,800 m3/d from April 2027")):
        xs = [d for d, _ in res["series"][q]]
        ys = [s for _, s in res["series"][q]]
        ax.plot(xs, ys, color=col, lw=1.8, marker="o", ms=2.6, label=lab)
        ax.annotate("%s m3/d" % "{:,}".format(int(q)), (xs[-1], ys[-1]), xytext=(5, -2), textcoords="offset points",
                    fontsize=7.2, color="#333333", va="center")
    ax.axhline(avail, color="#444444", lw=1.0, ls="--")
    ax.text(dt.date(2016, 6, 1), avail + 0.18, "available drawdown %.2f m" % avail, fontsize=7.5, color="#444444")
    ax.axvline(dt.date(2027, 4, 1), color="#999999", lw=0.8, ls=":")
    ax.text(dt.date(2027, 6, 1), 0.5, "renewed licence", fontsize=7.2, color="#666666")
    ax.set_ylabel("Predicted drawdown (m)", fontsize=8)
    ax.set_title("%s: within its %.2f m at %s m3/d, over it at 1,800" % (worst, avail, "{:,}".format(int(res["largest"]))),
                 fontsize=9, loc="left")
    ax.tick_params(labelsize=7.5)
    ax.set_ylim(0, 11.5)
    ax.set_xlim(dt.date(2015, 9, 1), dt.date(2041, 9, 1))
    ax.grid(axis="y", color="#e2e2e2", lw=0.6)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(fontsize=7.3, frameon=False, loc="upper left")
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", metadata={"Software": None})
    plt.close(fig)
    return buf.getvalue()


def write_note(path, res):
    st = D.styles("Carlito", "Carlito-Bold", BRAND, 9.9)
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=17 * mm,
                            bottomMargin=17 * mm, title="BH2 licence renewal and variation", author=K.PEOPLE["lead"],
                            subject="", creator="", producer="")
    mc = res["mc"]
    L = int(res["largest"])
    worst = res["worst"]
    flow = [Paragraph("Borehole 2 renewal: apply for %s cubic metres a day, not 1,800" % "{:,}".format(L), st["h1"]),
            Paragraph(D.esc("%s, %s. Licence MA/28/15/0042. For the application due %s." % (
                K.PEOPLE["lead"], K.long_date(K.NOTE_DATE), K.long_date(K.APPLICATION_DUE))), st["sub"]),
            Paragraph("<b>Apply for %s cubic metres a day.</b> The 1,800 a day line 5 needs fails the licensing "
                      "team's derogation test at all three protected boreholes. %s limits the quantity: %.1f m "
                      "predicted at %s a day against its %.2f m available drawdown." % (
                          "{:,}".format(L), worst, res["at_largest"][worst], "{:,}".format(L), res["avail"][worst]),
                      st["body"])]
    flow.append(Paragraph("Derogation test at 31 March 2039", st["h2"]))
    rows = [["Protected borehole", "Available drawdown (m)", "Predicted at 1,800 (m)", "Predicted at %s (m)" % "{:,}".format(L),
             "Passes at 1,800"]]
    for name, _, av in mc["prot"]:
        rows.append([name, "%.2f" % av, "%d" % res["at1800"][name], "%.1f" % res["at_largest"][name],
                     "no" if mc["at1800"][name] > av else "yes"])
    flow.append(D.grid(rows, [46 * mm, 30 * mm, 30 * mm, 30 * mm, 26 * mm], st, right_from=1))
    flow.append(Paragraph(D.esc("Available drawdowns as tabled in the licensing team's letter of 22 September 2026. "
                                "Drawdowns at 1,800 to the nearest metre, at %s to one decimal." % "{:,}".format(L)),
                          st["small"]))
    flow.append(Spacer(1, 5))
    flow.append(Paragraph(D.esc(
        "Basis: Borehole 2 at 1,200 m3/d from 1 April 2015 and at the applied quantity from 1 April 2027, drawdowns "
        "from each borehole's April 2015 rest level (the letter's test). Aquifer: transmissivity %d m2/d and storage "
        "coefficient %.5f from the June 2014 constant-rate test (all three observation boreholes), with the "
        "Coldharbour Fault as a no-flow boundary: it throws the Sherwood Sandstone against Mercia Mudstone, so the "
        "cone is held at the fault and each protected borehole also carries the drawdown of an image of Borehole 2 "
        "across it. The 72-hour test never reached the fault; the observation boreholes' record from 2015 to March "
        "2026 (OB2 read from its raised casing top from March 2020), less the regional movement at Windle Cross and "
        "under the returned abstraction, matches this model to %.2f m (rms) against %.2f m for an unbounded aquifer, "
        "and Windle Cross, beyond the fault, shows no response." % (round(mc["T"]), round(mc["S"], 5), res["verdict"]["closed by the fault, test T and S"],
                                res["verdict"]["unbounded, test T and S"])), st["small"]))
    png = chart_png(res)
    flow.append(Image(io.BytesIO(png), width=170 * mm, height=170 * mm * 3.5 / 7.2))
    flow.append(Paragraph(D.esc("%s's predicted drawdown at each 31 March under the two quantities, against its "
                                "available drawdown." % worst), st["small"]))
    flow.append(Paragraph("Need: line 3 water use, 2025-26", st["h2"]))
    flow.append(Paragraph(D.esc("Line 5 copies line 3, so the application's need is sized on line 3's water use "
                                "per litre packed, its cleans included (meter FM-L3, packed output from the MES at "
                                "the bottle sizes filled that year: the 75cl still glass was still 750 ml until "
                                "April 2026)."), st["body"]))
    rows = [["Month", "Litres of water per litre packed"]]
    for k in MONTHS_B:
        rows.append([month_label(k), "%.2f" % res["ask_b"][k]])
    flow.append(D.grid(rows, [50 * mm, 52 * mm], st, right_from=1))
    flow.append(Paragraph(D.esc("FM-L3's register from the site telemetry by local month, over the good bottles in "
                                "the MES orders at the size filled."), st["small"]))
    flow.append(Spacer(1, 5))
    flow.append(Paragraph("Returns check", st["h2"]))
    flow.append(Paragraph(D.esc(
        "The bulk bay that opened for the Ferncastle Foods contract in April 2026 draws off the raw main upstream "
        "of FM-1, so the tanker loads are taken from Borehole 2 without passing the licence meter and FM-1 "
        "understates this year's abstraction. Each load is matched to its pump run in the wellhead log (the haulier "
        "dates its tickets by the night shift). Monthly volumes and days over 1,200 m3 from April to September 2026 "
        "are in bh2_returns_check.csv; the 2026-27 return will need the bulk loads added."), st["body"]))
    doc.build(flow, onFirstPage=D._footer("Brackenholt Spring Water", "Carlito"),
              onLaterPages=D._footer("Brackenholt Spring Water", "Carlito"))


def write_csv(path, res):
    rows = []
    for k in MONTHS_A:
        v, n = res["ask_a"][k]
        rows.append(["%04d-%02d" % k, v, n])
    K.write_csv(path, ["month", "volume_taken_m3", "days_over_1200_m3"], rows)


def write_all(gdir, gendir, b):
    res = compute(b)
    res["verdict"], (Ta, Sa), _ = C.long_record_verdict(b, res["mc"]["T"], res["mc"]["S"], res["mc"]["img"])
    res["apparent"] = (Ta, Sa)
    write_note(os.path.join(gdir, G_NOTE), res)
    write_csv(os.path.join(gdir, G_CSV), res)
    import postprocess as PP
    PP.normalize_pdf(os.path.join(gdir, G_NOTE), b"D:20261113161400+00'00'", b"D:20261113161400+00'00'")
    figs = figures(res)
    with open(os.path.join(gendir, "figures.json"), "w") as fh:
        json.dump(figs, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return res, figs


def figures(res):
    mc = res["mc"]
    f = {
        "call_largest_m3d": int(res["largest"]),
        "call_applied_m3d": int(K.APPLIED_QD),
        "call_limiting": res["worst"],
        "T_m2d": int(round(mc["T"])),
        "S_e4": round(mc["S"] * 1e4, 1),
        "S": round(mc["S"], 5),
        "limiting_avail_m": res["avail"][res["worst"]],
        "licensed_m3d": int(K.LICENSED_QD),
    }
    for name, _, av in mc["prot"]:
        key = name.split()[0].lower()
        f["at1800_%s_m" % key] = res["at1800"][name]
        f["avail_%s_m" % key] = av
    for k in MONTHS_A:
        lab = "%04d_%02d" % k
        f["askA_volume_%s" % lab] = res["ask_a"][k][0]
        f["askA_days_%s" % lab] = res["ask_a"][k][1]
    for k in MONTHS_B:
        f["askB_l3_%04d_%02d" % k] = res["ask_b"][k]
    f["fault_throw_m"] = 260
    f["rms_closed_m"] = round(res["verdict"]["closed by the fault, test T and S"], 2)
    f["rms_unbounded_m"] = round(res["verdict"]["unbounded, test T and S"], 2)
    f["size_bsg1101_window_ml"] = 750
    f["size_bsg1101_export_ml"] = 700
    f["test_hours"] = 72
    return f
