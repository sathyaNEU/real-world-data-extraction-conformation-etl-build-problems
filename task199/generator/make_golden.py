"""task199 golden deliverables and figures.json.

    python3 task199/generator/make_golden.py

Writes golden/nota_vigilancia_2026S2.xlsx and golden/grafico_vigilancia_2026S2.png from the drawn
rows, and generator/figures.json with every figure the write-up states. verify.py recomputes the same
quantities from the shipped bundle on its own code path, so the two agree or the build fails.
"""
import json
import os
import sys
from datetime import date, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import core            # noqa: E402
import build_pack as B  # noqa: E402
import postprocess     # noqa: E402

TASK = os.path.dirname(HERE)
GOLD = os.path.join(TASK, "golden")
PANEL = [m[0] for m in core.PANEL]
OUTSIDE = [c for c, _ in core.OUTSIDE]
TYPE_OF = {o[0]: o[2] for o in B.OUTLETS}
TYPE_LABEL = {"diario": "Prensa diaria", "radio": "Radio", "digital": "Portales",
              "agencia": "Agencias"}
ELIG_FLOOR = 70


def watch_note(d, pops):
    r = B.rungs(d)
    rows = []
    for c in PANEL:
        rows.append(dict(city=c, win=r[c]["aw"], base=r[c]["ab"],
                         rate=round(r[c]["aw"] / pops[c] * 1e5, 1),
                         eligible=r[c]["aw"] >= ELIG_FLOOR,
                         designated=False, dec=r[c]["rung3"]))
    best = max([x for x in rows if x["eligible"]], key=lambda x: x["dec"])
    best["designated"] = True
    rows.sort(key=lambda x: -x["dec"])
    return rows, best


def ask_a(d):
    """Items the service delivered against items its invoices bill, 2025, the twelve municipalities
    outside the panel, by quarter and outlet type, with a line for each difference."""
    cells = {}
    for row in d["deliveries"]:
        if row["city"] in PANEL or row["date"].year != 2025:
            continue
        q = (row["date"].month - 1) // 3 + 1
        t = TYPE_OF[row["outlet"]]
        cells[(q, t)] = cells.get((q, t), 0) + row["delivered"]
    billed = {}
    for seat, m, items, val in B.invoice_lines(d):
        q = (m - 1) // 3 + 1
        billed[q] = billed.get(q, 0) + items
    amounts = {}
    for seat, m, items, val in B.invoice_lines(d):
        q = (m - 1) // 3 + 1
        amounts[q] = round(amounts.get(q, 0.0) + val, 1)
    # the three differences between what 2025's rows hold and what 2025's invoice bills
    dec24 = sum(r["delivered"] for r in d["deliveries"]
                if r["city"] not in PANEL and r["date"].year == 2025
                and B.publication_period(r["city"], r["date"]).year == 2024)
    dec25 = sum(r["delivered"] for r in d["deliveries"]
                if r["city"] not in PANEL and r["date"].year == 2026
                and B.publication_period(r["city"], r["date"]).year == 2025)
    rejected = sum(r["delivered"] for r in d["deliveries"]
                   if r["city"] not in PANEL and r["date"] == B.REJECTED_LOTE[1]
                   and B.desk_seat(r["city"]) == B.REJECTED_LOTE[0])
    return cells, billed, amounts, dict(publicado_2024=dec24, publicado_2025_remitido_2026=dec25,
                                        lote_rechazado=rejected)


def ask_b(d):
    """What the register holds for each municipality outside the panel in 2025, and in how many
    months of that year it holds none. Each action is credited to the municipality its own code
    names on its action date."""
    held, months_with = {}, {}
    for x in d["actions"]:
        if x["city"] in PANEL:
            continue
        for k in range(x["days"]):
            dt = x["date"] + timedelta(days=k)
            if dt.year != 2025:
                continue
            held[x["city"]] = held.get(x["city"], 0) + 1
            months_with.setdefault(x["city"], set()).add(dt.month)
    return [dict(city=c, held=held.get(c, 0), empty=12 - len(months_with.get(c, ())))
            for c in sorted(OUTSIDE)]


def ask_c(d):
    """Participants per action and in total by actor sector, 2025, the municipalities outside the
    panel. A reported range is read at its midpoint, as the manual's central estimate; an unreported
    figure is excluded. Both figures move under the numeric column's own lower bounds, measured."""
    tot, n, mx = {}, {}, {}
    for x in d["actions"]:
        if x["city"] in PANEL:
            continue
        if x["truth_participants"] is None:
            continue
        # the 2025 export holds one entry per gathering-day, which is what the dictionary calls a
        # row and what the ask counts, so a prolonged action enters once for each of its days
        for k in range(x["days"]):
            if (x["date"] + timedelta(days=k)).year != 2025:
                continue
            v = x["truth_participants"]
            s = x["sector"]
            tot[s] = tot.get(s, 0) + v
            n[s] = n.get(s, 0) + 1
            mx[s] = max(mx.get(s, 0), v)
    return [dict(sector=s, per_action=round(tot[s] / n[s], 1), total=tot[s], actions=n[s])
            for s in sorted(tot)]


def chart(rows, best, path):
    """One bar per panel city: the half year's recorded actions per 1,000 items the monitor received
    from the city, against the same figure for the twenty-four months of comparison. The designated
    city is the one whose bar clears the line of no change once what reached the monitor is held
    level."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    ordered = sorted(rows, key=lambda r: r["dec"])
    names = [r["city"] for r in ordered]
    vals = [r["dec"] for r in ordered]
    fig, ax = plt.subplots(figsize=(8.8, 5.2), dpi=150)
    colors = ["#1b3a5c" if r is best else "#aebecd" for r in ordered]
    bars = ax.barh(names, vals, color=colors, height=0.62, zorder=3)
    ax.axvline(1.0, color="#6d8196", linewidth=1.1, zorder=4)
    ax.annotate("1,00 sin cambio", (1.0, len(names) - 0.35), fontsize=8, color="#6d8196",
                ha="center", annotation_clip=False)
    for r, b in zip(ordered, bars):
        ax.annotate("%.2f" % r["dec"], (b.get_width() + 0.03, b.get_y() + b.get_height() / 2),
                    va="center", fontsize=8, color="#44586c")   # values wear text ink
    ax.annotate("%d acciones-dia en el semestre, %.1f por 100.000 habitantes"
                % (best["win"], best["rate"]),
                (best["dec"] - 0.04, names.index(best["city"])), ha="right", va="center",
                fontsize=8.5, color="#ffffff", zorder=5)
    ax.set_xlabel("Acciones-dia por 1.000 items recibidos, semestre contra los 24 meses de comparacion",
                  fontsize=9)
    ax.set_title("Tibu es el municipio designado: su registro sube %.2f veces con el material "
                 "recibido sin cambio" % best["dec"], fontsize=11, color="#13263c")
    ax.set_xlim(0, max(vals) * 1.22)
    ax.tick_params(axis="y", length=0, labelsize=9)
    ax.tick_params(axis="x", labelsize=8)
    ax.grid(True, axis="x", color="#eef2f6", linewidth=0.8)
    ax.set_axisbelow(True)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    fig.savefig(path, metadata={"Software": None})
    plt.close(fig)


def main():
    d = B.draw()
    pops = json.load(open(os.path.join(HERE, "populations.json")))["populations"]
    rows, best = watch_note(d, pops)
    cells, billed, amounts, diffs = ask_a(d)
    bee = ask_b(d)
    cee = ask_c(d)
    if os.path.isdir(GOLD):
        import shutil
        shutil.rmtree(GOLD)
    os.makedirs(GOLD)

    import openpyxl
    from openpyxl.styles import Font, Alignment
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Nota de vigilancia"
    bold = Font(bold=True)
    ws["A1"] = "Nota de vigilancia semestral, 1 de abril al 30 de septiembre de 2026"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = ("Municipio designado: %s. Tasa publicada: %.1f acciones registradas por 100.000 "
                "habitantes." % (best["city"], best["rate"]))
    ws["A3"] = ("La mision de verificacion del semestre viaja a %s." % best["city"])
    hdr = ["Municipio del panel", "Acciones-dia abr-sep 2026", "Acciones-dia 2024-2025",
           "Tasa por 100.000 habitantes", "Cumple la condicion", "Designado"]
    for j, h in enumerate(hdr, start=1):
        c = ws.cell(row=5, column=j, value=h)
        c.font = bold
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, r in enumerate(rows, start=6):
        ws.cell(row=i, column=1, value=r["city"])
        ws.cell(row=i, column=2, value=r["win"])
        ws.cell(row=i, column=3, value=r["base"])
        ws.cell(row=i, column=4, value=r["rate"])
        ws.cell(row=i, column=5, value="si" if r["eligible"] else "no")
        ws.cell(row=i, column=6, value="si" if r["designated"] else None)
    ws.cell(row=6 + len(rows) + 1, column=1,
            value="Las acciones-dia cuentan concentraciones por dia y lugar, extracto definitivo "
                  "del 5 de noviembre de 2026.")
    ws.column_dimensions["A"].width = 22
    for col in "BCDEF":
        ws.column_dimensions[col].width = 15
    for i in range(6, 6 + len(rows)):
        ws.cell(row=i, column=2).number_format = "#,##0"
        ws.cell(row=i, column=3).number_format = "#,##0"
        ws.cell(row=i, column=4).number_format = "0.0"
    ws.freeze_panes = "A6"
    ws.auto_filter.ref = "A5:F%d" % (5 + len(rows))
    ws.print_area = "A1:F%d" % (6 + len(rows) + 1)
    ws.print_title_rows = "5:5"

    ws2 = wb.create_sheet("Remisiones y facturacion")
    ws2["A1"] = "Municipios fuera del panel, 2025: items remitidos por el servicio y facturados"
    ws2["A1"].font = bold
    ws2.append([])
    ws2.append(["Trimestre"] + [TYPE_LABEL[t] for t in ("diario", "radio", "digital", "agencia")]
               + ["Remitido total", "Facturado", "Valor facturado (miles COP)"])
    for j in range(1, 8):
        ws2.cell(row=3, column=j).font = bold
    for q in (1, 2, 3, 4):
        tot = sum(cells.get((q, t), 0) for t in ("diario", "radio", "digital", "agencia"))
        ws2.append(["T%d" % q] + [cells.get((q, t), 0) for t in
                                  ("diario", "radio", "digital", "agencia")]
                   + [tot, billed.get(q, 0), amounts.get(q, 0.0)])
    ws2.append([])
    ws2.append(["Diferencias entre lo remitido en 2025 y lo facturado en 2025", "Items"])
    ws2.cell(row=ws2.max_row, column=1).font = bold
    ws2.append(["Items publicados en diciembre de 2024 y remitidos en enero de 2025",
                diffs["publicado_2024"]])
    ws2.append(["Items publicados en diciembre de 2025 y remitidos en enero de 2026",
                diffs["publicado_2025_remitido_2026"]])
    ws2.append(["Lote del 11 de agosto de 2025 rechazado y acreditado", diffs["lote_rechazado"]])
    for row in ws2.iter_rows(min_row=4, max_row=7, min_col=2, max_col=6):
        for c in row:
            c.number_format = "#,##0"
    for row in ws2.iter_rows(min_row=4, max_row=7, min_col=7, max_col=7):
        for c in row:
            c.number_format = "#,##0.0"
    ws2.freeze_panes = "A4"
    ws2.column_dimensions["A"].width = 62
    for col in "BCDEFG":
        ws2.column_dimensions[col].width = 16

    ws3 = wb.create_sheet("Fuera del panel 2025")
    ws3["A1"] = "Registro de 2025 en los municipios fuera del panel"
    ws3["A1"].font = bold
    ws3.append([])
    ws3.append(["Municipio", "Acciones-dia 2025", "Meses sin accion registrada"])
    for j in (1, 2, 3):
        ws3.cell(row=3, column=j).font = bold
    for x in bee:
        ws3.append([x["city"], x["held"], x["empty"]])
    ws3.freeze_panes = "A4"
    ws3.column_dimensions["A"].width = 20
    ws3.column_dimensions["B"].width = 18
    ws3.column_dimensions["C"].width = 26
    for i in range(4, 4 + len(bee)):
        ws3.cell(row=i, column=2).number_format = "#,##0"

    ws4 = wb.create_sheet("Participantes por sector")
    ws4["A1"] = "Participantes por accion y en total, 2025, municipios fuera del panel"
    ws4["A1"].font = bold
    ws4.append([])
    ws4.append(["Sector del actor", "Participantes por accion", "Participantes en total"])
    for j in (1, 2, 3):
        ws4.cell(row=3, column=j).font = bold
    for x in cee:
        ws4.append([x["sector"], x["per_action"], x["total"]])
    ws4.freeze_panes = "A4"
    ws4.column_dimensions["A"].width = 22
    ws4.column_dimensions["B"].width = 22
    ws4.column_dimensions["C"].width = 18
    for i in range(4, 4 + len(cee)):
        ws4.cell(row=i, column=2).number_format = "0.0"
        ws4.cell(row=i, column=3).number_format = "#,##0"

    ws5 = wb.create_sheet("Notas")
    ws5["A1"] = "Notas de la nota de vigilancia"
    ws5["A1"].font = bold
    for i, line in enumerate([
            "Extracto definitivo del registro, 5 de noviembre de 2026.",
            "Acciones-dia: concentraciones contadas por dia y lugar, manual de codificacion 1.2.",
            "Semestre evaluado: 1 de abril a 30 de septiembre de 2026, ambos dias incluidos.",
            "Periodo de comparacion: veinticuatro meses terminados el 31 de diciembre de 2025.",
            "Condicion del protocolo 4.3: al menos setenta acciones en el semestre. Hacari no la cumple "
            "con 56 y por eso figura sin designar.",
            "Poblacion: proyeccion municipal vigente para 2026, en unidades.",
            "Las hojas de remisiones, municipios fuera del panel y participantes cubren 2025 y no "
            "entran en la designacion.",
            "El lote del 11 de agosto de 2025 de la mesa de Rio de Oro fue rechazado y acreditado; "
            "aparece remitido y no facturado."], start=3):
        ws5.cell(row=i, column=1, value=line)
    ws5.column_dimensions["A"].width = 100

    path = os.path.join(GOLD, "nota_vigilancia_2026S2.xlsx")
    wb.save(path)
    postprocess.normalize_ooxml(path, creator="yamaya", last_by="yamaya",
                                created="2026-11-16T08:40:00Z", modified="2026-11-16T08:40:00Z",
                                excel=True)
    chart(rows, best, os.path.join(GOLD, "grafico_vigilancia_2026S2.png"))

    figures = {
        "call": {"city": best["city"], "rate_per_100k": best["rate"],
                 "window_action_days": best["win"], "baseline_action_days": best["base"]},
        "components": {
            "window_action_days": best["win"],
            "baseline_action_days": best["base"],
            "window_delivered_items": B.rungs(d)[best["city"]]["vw"],
            "baseline_delivered_items": B.rungs(d)[best["city"]]["vb"],
            "population": pops[best["city"]],
        },
        "runner_up": {"city": rows[1]["city"], "rate_per_100k": rows[1]["rate"],
                      "ratio": round(rows[1]["dec"], 2)},
        "decisive_ratio": {r["city"]: round(r["dec"], 2) for r in rows},
        "eligibility": {"floor": ELIG_FLOOR,
                        "below": [r["city"] for r in rows if not r["eligible"]]},
        "default_path_rival": {
            "city": max(rows, key=lambda r: (r["win"] / 6.0) / (r["base"] / 24.0))["city"],
            "window_action_days": max(rows, key=lambda r: (r["win"] / 6.0) / (r["base"] / 24.0))["win"],
            "baseline_action_days": max(rows, key=lambda r: (r["win"] / 6.0) / (r["base"] / 24.0))["base"],
            "window_delivered_items": B.rungs(d)[max(rows, key=lambda r: (r["win"] / 6.0) / (r["base"] / 24.0))["city"]]["vw"],
            "baseline_delivered_items": B.rungs(d)[max(rows, key=lambda r: (r["win"] / 6.0) / (r["base"] / 24.0))["city"]]["vb"]},
        "citation_rival": {"city": "Teorama",
                           "ratio": round([r for r in rows if r["city"] == "Teorama"][0]["dec"], 2)},
        "default_path": {"city": max(rows, key=lambda r: (r["win"] / 6.0) / (r["base"] / 24.0))["city"],
                         "rate_per_100k": max(rows, key=lambda r: (r["win"] / 6.0) / (r["base"] / 24.0))["rate"]},
        "watch_note": [{"city": r["city"], "window": r["win"], "baseline": r["base"],
                        "rate": r["rate"], "eligible": "si" if r["eligible"] else "no",
                        "designated": "si" if r["designated"] else "no"} for r in rows],
        "ask_a_cells": {"T%d|%s" % (q, t): cells.get((q, t), 0)
                        for q in (1, 2, 3, 4) for t in ("diario", "radio", "digital", "agencia")},
        "ask_a_totals": {"T%d" % q: sum(cells.get((q, t), 0) for t in
                                        ("diario", "radio", "digital", "agencia"))
                         for q in (1, 2, 3, 4)},
        "ask_a_billed": {"T%d" % q: billed.get(q, 0) for q in (1, 2, 3, 4)},
        "ask_a_amounts": {"T%d" % q: amounts.get(q, 0.0) for q in (1, 2, 3, 4)},
        "ask_a_differences": diffs,
        "ask_b": [{"city": x["city"], "held": x["held"], "empty_months": x["empty"]} for x in bee],
        "ask_c": [{"sector": x["sector"], "per_action": x["per_action"], "total": x["total"]}
                  for x in cee],
        # the units and clause references the write-up names, emitted rather than typed
        "units": {"rate_per_residents": 100000, "items_per": 1000, "population_vintage": 2026,
                  "protocol_clause_outcome": 4.1, "protocol_clause_estimand": 4.2,
                  "protocol_clause_eligibility": 4.3},
    }
    json.dump(figures, open(os.path.join(HERE, "figures.json"), "w"), indent=1, ensure_ascii=False)

    ts = 1763282400   # 2026-11-16 08:40 UTC, when the note was saved
    for f in sorted(os.listdir(GOLD)):
        os.utime(os.path.join(GOLD, f), (ts, ts))
    print("golden written: %s" % ", ".join(sorted(os.listdir(GOLD))))
    print("designated %s, rate %.1f per 100,000, %d action-days in the window against %d in the baseline"
          % (best["city"], best["rate"], best["win"], best["base"]))
    print("default path would name %s at %.1f" % (figures["default_path"]["city"],
                                                  figures["default_path"]["rate_per_100k"]))


if __name__ == "__main__":
    main()
