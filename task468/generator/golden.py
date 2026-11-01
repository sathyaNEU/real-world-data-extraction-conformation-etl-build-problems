"""The two golden deliverables: the Investment Committee note (PDF, with the chart drawn by matplotlib) and the ward
index workbook (XLSX). Every figure comes from figs.compute; nothing is typed."""
import datetime as dt
import io
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.units import mm  # noqa: E402
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import pack as K  # noqa: E402
import figs as FG  # noqa: E402

PDF = "harrowmere_pressured_wards_2027-28.pdf"
XLSX = "harrowmere_ward_index_2026.xlsx"
CODE = {name: code for code, name, *_ in __import__("params").WARDS}


def chart(fig, path):
    wards = sorted(FG.WARDS, key=lambda w: fig["change"][w])
    vals = [fig["change"][w] for w in wards]
    press = set(fig["call"]["pressured"])
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8.5, "svg.hashsalt": "468"})
    f, ax = plt.subplots(figsize=(6.6, 3.5), dpi=150)
    cols = ["#1f5f8b" if w in press else "#b7c3cc" for w in wards]
    ax.barh(range(len(wards)), vals, color=cols, height=0.62)
    ax.axvline(5.0, color="#b23a2e", lw=1.1)
    ax.text(5.06, len(wards) - 0.55, "5.0% line", color="#b23a2e", fontsize=7.5, va="center")
    for k, v in enumerate(vals):
        ax.text(v + 0.08, k, "%.1f" % v, va="center", fontsize=7.5, color="#2b3238")
    ax.set_yticks(range(len(wards)))
    ax.set_yticklabels(wards)
    ax.set_xlim(0, max(vals) + 1.1)
    ax.set_xlabel("Ward House Price Index, change 2025 to 2026 (%)")
    ax.set_title("Three wards rose more than 5.0% in 2026", loc="left", fontsize=9.5, color="#2b3238")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    f.tight_layout()
    f.savefig(path, format="png", metadata={"Software": None})
    plt.close(f)


def write_pdf(fig, path, png):
    st = K._styles()
    call = fig["call"]
    press = call["pressured"]
    order = sorted(press, key=lambda w: -call["shares"][w])
    pb = fig["pellbury"]

    def page(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#5b6670"))
        canvas.drawString(20 * mm, 10 * mm, "%s. Investment Committee, 17 March 2027. Paper IC/27/09" % K.AGENCY)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "Page %d" % d.page)
        canvas.restoreState()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=16 * mm,
                            bottomMargin=18 * mm, title="Pressured Wards Uplift 2027-28", author="Housing Market Analysis",
                            creator="Housing Market Analysis", producer="Housing Market Analysis", invariant=1)
    names = ", ".join(order[:-1]) + " and " + order[-1]
    s = []  # the story
    s.append(Paragraph("Investment Committee, 17 March 2027. Paper IC/27/09. For decision.", st["s"]))
    s.append(Paragraph("Pressured Wards Uplift 2027-28: %s qualify; Pellbury does not" % names, st["t"]))
    s.append(Paragraph("From the Director of Investment. Prepared by Housing Market Analysis, 3 March 2027.", st["s"]))
    s.append(Paragraph("Recommendation", st["h"]))
    s.append(Paragraph(
        "The Committee is asked to confirm %s as the pressured wards for 2027-28 and to share the %s uplift "
        "among them as set out below. Each rose by more than 5.0 per cent from 2025 to 2026 on the Ward House "
        "Price Index; no other ward did." % (names, call["pot_text"]), st["p"]))
    rows = [["Ward", "Index change 2025 to 2026", "Homes due to start, 2027-28", "Share of the uplift"]]
    for w in order:
        rows.append([w, "%.1f%%" % fig["change"][w], "%d" % call["homes"][w], call["shares_text"][w]])
    rows.append(["Total", "", "%d" % call["homes_total"], call["pot_text"]])
    t = Table([[Paragraph(str(c), st["cell"]) for c in r] for r in rows],
              colWidths=[44 * mm, 40 * mm, 46 * mm, 40 * mm], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#8a949c")),
                           ("LINEABOVE", (0, -1), (-1, -1), 0.4, colors.HexColor("#8a949c")),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    s += [t, Spacer(1, 2)]
    s.append(Paragraph("Source: Ward House Price Index 2026 (price paid data as updated in January 2027); Affordable "
                       "Homes Programme pipeline, 22 January 2027. Shares rounded to the nearest pound.", st["s"]))
    s.append(Paragraph("Three wards over the line in 2026", st["h"]))
    s.append(Image(png, width=166 * mm, height=88 * mm))
    s.append(Paragraph(
        "Pellbury needs a word. Taken on every pair of its sales, its index rose %.1f per cent. A good part of its "
        "2026 resales were terraces that small developers bought in 2024 and 2025, fitted with a loft room and a "
        "rear extension under building regulations and sold on, so their second sale prices a larger house than "
        "the first. The index measures the price of the same dwelling at the same quality, and with the pairs "
        "whose dwelling had building work completed between its two sales set aside, Pellbury rose %.1f per "
        "cent. It is not a pressured ward." % (pb["every_pair"], pb["golden"]), st["p"]))
    s.append(Paragraph("Note: the index is estimated afresh each year on the full record, so the 2025 changes "
                       "published last March can revise (methodology, section 4); only the 2025 to 2026 change is "
                       "used here.", st["s"]))
    s.append(Paragraph("How the index was compiled", st["h"]))
    s.append(Paragraph(
        "From the price paid data for 2015 to 2026 with the January 2027 update applied: standard entries for "
        "dwellings, each dwelling's consecutive sales paired by address, each pair placed in its May 2023 ward "
        "by postcode, and each ward's index fitted to its pairs as the methodology (third edition) sets out. "
        "Building work was found by matching the council's building control completions, in both of its "
        "systems' exports, to the sale addresses; a pair is set aside when a completion certificate on the "
        "dwelling falls between its two sales.", st["p"]))
    s.append(Paragraph("Supply and activity, 2026", st["h"]))
    s.append(Paragraph(
        "Net additional dwellings from building work completed in 2026, additional price paid entries for "
        "dwellings (company buyers, repossessions and portfolio sales), and affordable homes started on site "
        "are given ward by ward in the workbook (harrowmere_ward_index_2026.xlsx). Across the city: %d net "
        "additional dwellings, %d additional entries carrying GBP {:,} paid, and %d affordable homes started."
        .format(fig["ask_b_money_total"]) % (fig["ask_a_total"], fig["ask_b_count_total"], fig["ask_c_total"]),
        st["p"]))
    doc.build(s, onFirstPage=page, onLaterPages=page)
    data = open(path, "rb").read()
    import re
    data = re.sub(rb"/CreationDate \(D:[^)]*\)", b"/CreationDate (D:20270303161200+00'00')", data)
    data = re.sub(rb"/ModDate \(D:[^)]*\)", b"/ModDate (D:20270303174500+00'00')", data)
    for sig in (b"ReportLab Generated PDF document (opensource)", b"ReportLab generated PDF document -- digest (opensource)"):
        data = data.replace(sig, b" " * len(sig))
    open(path, "wb").write(data)


def write_xlsx(fig, path):
    call = fig["call"]
    press = set(call["pressured"])
    idx = [["Ward", "Ward code (May 2023)", "Index change 2025 to 2026 (%)", "Pressured ward", "Homes due to start 2027-28",
            "Share of uplift (GBP)"]]
    for w in FG.WARDS:
        idx.append([w, CODE[w], fig["change"][w], "Yes" if w in press else "No", fig["homes"][w],
                    call["shares"][w] if w in press else 0])
    idx.append(["Total", "", None, "", sum(call["homes"][w] for w in press), call["pot"]])
    sup = [["Ward", "Net additional dwellings, completed 2026"]] + [[w, fig["ask_a"][w]] for w in FG.WARDS] + \
          [["Total", fig["ask_a_total"]]]
    ent = [["Ward", "Additional price paid entries, dwellings, 2026", "Money paid (GBP)"]] + \
          [[w, fig["ask_b_count"][w], fig["ask_b_money"][w]] for w in FG.WARDS] + \
          [["Total", fig["ask_b_count_total"], fig["ask_b_money_total"]]]
    sts = [["Ward", "Affordable homes started on site, 2026"]] + [[w, fig["ask_c"][w]] for w in FG.WARDS] + \
          [["Total", fig["ask_c_total"]]]
    notes = [["Ward House Price Index 2026 and the 2027-28 Pressured Wards Uplift"],
             ["Prepared by Housing Market Analysis for the Investment Committee of 17 March 2027."],
             ["Index: price paid data 2015 to 2026 with the January 2027 update; standard entries for dwellings; "
              "consecutive sales of one address paired; pairs with a building control completion on the dwelling "
              "between the two sales set aside; ward of the May 2023 boundaries by postcode; methodology third edition."],
             ["Uplift: pressured if the index rose more than 5.0 per cent; GBP 12,000,000 shared by homes in approved "
              "or in-contract schemes due to start on site from 1 April 2027 to 31 March 2028; shares to the nearest pound."],
             ["Supply: building control completions certified in 2026, dwellings created less dwellings lost, each "
              "application once, by the ward of the site's postcode."],
             ["Additional entries: category B entries for dwellings transferred in 2026; a portfolio transfer's price, "
              "shown on each of its titles, counted once."],
             ["Starts: providers' start-on-site claims with a start date in 2026, paid or approved, each start once."]]
    K._xlsx(path, [("Ward index 2026", idx, [1], {"C": "0.0", "F": "#,##0"}), ("Supply 2026", sup, [1], None),
                   ("Additional entries 2026", ent, [1], {"C": "#,##0"}), ("Starts on site 2026", sts, [1], None),
                   ("Notes", notes, [1], None)],
            "Jodie Khan", dt.datetime(2027, 2, 24, 9, 3), dt.datetime(2027, 3, 3, 16, 58),
            widths=[18, 22, 30, 16, 26, 22])


def write_all(target, golden, fig):
    os.makedirs(golden, exist_ok=True)
    png = os.path.join(golden, "_chart.png")
    chart(fig, png)
    write_pdf(fig, os.path.join(golden, PDF), png)
    os.remove(png)
    write_xlsx(fig, os.path.join(golden, XLSX))
