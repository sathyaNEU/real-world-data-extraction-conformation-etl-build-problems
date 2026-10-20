"""task251 goldens: the bench workbook (each station analyzer's converter, the NO2 it has reduced and will have reduced
by its 2028 service, its efficiency then and the verdict; each station's 2027 NO2 record; the titrations the curve
was fitted on) and the chart of each converter's efficiency at its 2028 service against the 95 per cent line."""
import datetime as dt
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import params as P
import postprocess
import sim
import writeup as WU

XLSX = "turno_banco_convertitori_2028.xlsx"
PNG = "rendimento_convertitori_2028.png"
ORG = P.ORG
AUTHOR = "Servizio strumentazione, " + P.ORG_SHORT
BENCH = "#eb6834"          # categorical slot 2: on the bench
STAYS = "#2a78d6"          # categorical slot 1: stays to its service
INK, INK2 = "#0b0b0b", "#52514e"
TIPO = {"T": "traffico", "U": "fondo urbano", "S": "fondo suburbano", "I": "industriale", "R": "fondo rurale"}


def _head(ws, row, head, height=42):
    thin = Side(style="thin", color="A6ADB8")
    for j, h in enumerate(head, 1):
        c = ws.cell(row=row, column=j, value=h)
        c.font = Font(bold=True, size=9.5)
        c.fill = PatternFill("solid", fgColor="E4E9F0")
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        c.border = Border(bottom=thin)
    ws.row_dimensions[row].height = height


def _widths(ws, widths):
    from openpyxl.utils import get_column_letter
    for k, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(k)].width = w


def _title(ws, title, sub):
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = sub
    ws["A2"].font = Font(italic=True, size=9, color="52514E")


def workbook(path, G):
    T, Pts, a = G["table"], G["points"], G["asks"]
    F = G["fig"]
    stn = {s[0]: s for s in sim.STATIONS}
    wb = Workbook()
    ws = wb.active
    ws.title = "Banco gennaio 2028"
    _title(ws, "Sette convertitori al banco del 17-21 gennaio 2028: %s" % ", ".join(F["call"]["bench"]),
           "Rendimento del convertitore stimato alla manutenzione programmata 2028, dalla curva di tutte le titolazioni "
           "2025-2027 in funzione dell'NO2 convertito; al banco gli analizzatori sotto il 95 % prima della "
           "manutenzione (AQBP-QA-07, par. 7). Dati al 31/12/2027, lista al laboratorio entro il 10/01/2028.")
    head = ["Stazione", "Nome", "Tipo", "Matricola", "Convertitore in servizio dal", "Manutenzione 2028",
            "NO2 convertito al 31/12/2027 (ppm·h)", "NO2 convertito alla manutenzione (ppm·h)",
            "Rendimento al 31/12/2027", "Rendimento alla manutenzione", "Esito"]
    _head(ws, 4, head)
    fill = PatternFill("solid", fgColor="FBE3D6")
    r = 5
    for s in WU.STATIONS:
        x = T.loc[s]
        row = [s, stn[s][1], TIPO[stn[s][2]], x["serial"], x["installed"], x["service"], round(x["D_now"], 0),
               round(x["D_service"], 0), round(x["eta_now"], 3), round(x["eta_service"], 3),
               "al banco" if x["goes"] else "resta"]
        for j, v in enumerate(row, 1):
            c = ws.cell(row=r, column=j, value=v)
            c.font = Font(size=9.5, bold=(j == 11 and bool(x["goes"])))
            if x["goes"]:
                c.fill = fill
        ws.cell(row=r, column=5).number_format = "dd/mm/yyyy"
        ws.cell(row=r, column=6).number_format = "dd/mm/yyyy"
        ws.cell(row=r, column=7).number_format = "0"
        ws.cell(row=r, column=8).number_format = "0"
        ws.cell(row=r, column=9).number_format = "0.0%"
        ws.cell(row=r, column=10).number_format = "0.0%"
        for j in (7, 8, 9, 10):
            ws.cell(row=r, column=j).alignment = Alignment(horizontal="right")
        r += 1
    ws.cell(row=r + 1, column=1, value="Al banco").font = Font(bold=True, size=9.5)
    ws.cell(row=r + 1, column=11, value="%d di 16" % F["call"]["count"]).font = Font(bold=True, size=9.5)
    ws.cell(row=r + 3, column=1, value=(
        "BP01: manutenzione programmata il 20/01/2028, nella settimana del banco; il convertitore è già sotto il 95 % "
        "a fine 2027 e va al banco come ogni altro (par. 7, la manutenzione resta alla sua data). BP08: manutenzione "
        "2027 rinviata al 15/02/2028, convertitore in servizio dal 13/10/2026.")).font = Font(size=8.5, italic=True)
    ws.cell(row=r + 4, column=1, value=(
        "Fonti: archivio degli analizzatori (NO2 orario, ogni ora una volta), registro degli interventi, schede di "
        "titolazione Tecnoaria e Delta, piano di manutenzione 2028.")).font = Font(size=8.5, italic=True)
    ws.freeze_panes = "B5"
    _widths(ws, [9, 30, 15, 13, 13, 13, 14, 14, 12, 12, 10])
    ws.print_title_rows = "4:4"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1

    w2 = wb.create_sheet("NO2 2027")
    _title(w2, "Dato orario NO2 2027 per stazione: ore valide, media annua e 19° valore orario",
           "Ore valide: l'analizzatore ha misurato l'aria della stazione per almeno 45 minuti (par. 5). Valori in "
           "µg/m³ a 20 °C e 101,3 kPa; valore limite orario 200 µg/m³, da non superare più di 18 volte (par. 6).")
    _head(w2, 4, ["Stazione", "Nome", "Ore valide", "Media annua (µg/m³)", "19° valore orario (µg/m³)", "Note"])
    notes = {"BP07": "comprese le ore della scorta CL62-0466 dall'08/02 all'01/03, registrate in banca dati sotto MAG"}
    for s in ("BP03", "BP06", "BP09", "BP10", "BP14", "BP15"):
        notes[s] = "registratore LGX-300 a 0 °C fino alla visita di dicembre: valori riportati a 20 °C (1,91 / 2,05)"
    r = 5
    for s in WU.STATIONS:
        row = [s, stn[s][1], F["asks"]["valid_hours_2027"][s], F["asks"]["mean_2027_ugm3"][s],
               F["asks"]["p19_2027_ugm3"][s], notes.get(s, "")]
        for j, v in enumerate(row, 1):
            c = w2.cell(row=r, column=j, value=v)
            c.font = Font(size=9.5)
        w2.cell(row=r, column=3).number_format = "#,##0"
        w2.cell(row=r, column=4).number_format = "0.0"
        w2.cell(row=r, column=5).number_format = "0"
        r += 1
    w2.cell(row=r + 1, column=1, value=(
        "Escluse le ore di cui le titolazioni Delta hanno occupato più di 15 minuti (orari delle schede, ora italiana, "
        "riportati all'ora solare): la banca dati le aveva validate come aria della stazione.")).font = Font(size=8.5,
                                                                                                             italic=True)
    w2.freeze_panes = "C5"
    _widths(w2, [9, 30, 11, 12, 13, 80])

    w3 = wb.create_sheet("Titolazioni")
    _title(w3, "Le titolazioni 2025-2027 su cui è stimata la curva",
           "Rendimento della titolazione e NO2 convertito dal cambio del convertitore all'inizio della titolazione.")
    _head(w3, 4, ["Data", "Stazione", "Matricola", "Tipo verifica", "Ditta", "NO2 convertito (ppm·h)", "Rendimento"])
    r = 5
    for p in Pts.sort_values(["start", "serial"]).itertuples(index=False):
        row = [p.start.date(), p.station, p.serial, p.kind, "Tecnoaria" if p.who == "A" else "Delta", round(p.D, 1),
               round(p.eta, 4)]
        for j, v in enumerate(row, 1):
            w3.cell(row=r, column=j, value=v).font = Font(size=9)
        w3.cell(row=r, column=1).number_format = "dd/mm/yyyy"
        w3.cell(row=r, column=6).number_format = "0.0"
        w3.cell(row=r, column=7).number_format = "0.00%"
        r += 1
    w3.freeze_panes = "A5"
    w3.auto_filter.ref = "A4:G%d" % (r - 1)
    _widths(w3, [11, 9, 13, 17, 10, 13, 11])

    w4 = wb.create_sheet("Note")
    pr = G["curve"].params
    lines = [
        ("Dati al", "31/12/2027 (archivio degli analizzatori); lista al laboratorio entro il 10/01/2028"),
        ("Rendimento", "NO2 letto dall'analizzatore su NO2 generato dalla titolazione in fase gassosa (UNI EN 14211)"),
        ("NO2 convertito", "somma dell'NO2 orario dell'analizzatore (ppb, ogni ora una volta) dal cambio del "
                           "convertitore, in ppm·h"),
        ("Curva", ("rendimento = %.4f - %.6f x NO2 convertito, meno %.7f x (NO2 convertito - %.0f)² oltre %.0f "
                   "ppm·h; stimata su %d titolazioni" % (pr["c"][0], -pr["c"][1], -pr["c"][2], pr["knee"], pr["knee"],
                                                         len(Pts))).replace(".", ",")),
        ("Carico futuro", "NO2 della stazione dal 1° gennaio alla manutenzione 2028: media degli stessi giorni del "
                          "2025, 2026 e 2027"),
        ("Regola", "al banco gli analizzatori di stazione il cui convertitore sarebbe sotto il 95 % prima della "
                   "manutenzione programmata 2028 (AQBP-QA-07, par. 7); la scorta in magazzino è esclusa"),
        ("Ore valide 2027", "codici V e R della banca dati, meno le ore occupate per più di 15 minuti dalle titolazioni "
                            "Delta; BP07 con le ore della scorta (MAG); sei registratori LGX-300 riportati a 20 °C"),
    ]
    for i, (k, v) in enumerate(lines, 1):
        w4.cell(row=i, column=1, value=k).font = Font(bold=True, size=9.5)
        c = w4.cell(row=i, column=2, value=v)
        c.font = Font(size=9.5)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        w4.row_dimensions[i].height = 28
    _widths(w4, [18, 110])
    wb.save(path)
    postprocess.scrub(path, AUTHOR, "2028-01-05")
    postprocess.finish_office(path, "2028-01-04T16:10:00Z", "2028-01-05T09:35:00Z", ORG)


def chart(path, G):
    T = G["table"].copy()
    T = T.sort_values("eta_service", ascending=False)
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, ax = plt.subplots(figsize=(7.2, 5.8), dpi=200)
    y = np.arange(len(T))
    ax.axvline(95.0, color=INK2, lw=1.1, ls=(0, (4, 3)), zorder=1)
    ax.text(94.8, -0.95, "95 % (UNI EN 14211)", ha="right", va="center", fontsize=7.2, color=INK2)
    for yy, (s, x) in zip(y, T.iterrows()):
        col = BENCH if x["goes"] else STAYS
        e0, e1 = 100 * x["eta_now"], 100 * x["eta_service"]
        ax.plot([e0, e1], [yy, yy], color=col, lw=2.0, zorder=2, solid_capstyle="round")
        ax.plot([e0], [yy], "o", ms=6.5, mfc="white", mec=col, mew=1.6, zorder=3)
        ax.plot([e1], [yy], "o", ms=7.5, color=col, mec="white", mew=1.0, zorder=4)
        ax.text(min(e0, e1) - 0.45, yy, "%.1f" % e1, va="center", ha="right", fontsize=6.8, color=INK)
    ax.set_yticks(y)
    ax.set_yticklabels(["%s  %s  (%s)" % (s, x["serial"], x["service"].strftime("%d/%m")) for s, x in T.iterrows()],
                       fontsize=7.2, color=INK)
    ax.set_ylim(len(T) - 0.4, -1.5)
    ax.set_xlim(76, 101.5)
    ax.set_xticks([80, 85, 90, 95, 100])
    ax.set_xticklabels(["80 %", "85 %", "90 %", "95 %", "100 %"], fontsize=7.5, color=INK2)
    ax.set_xlabel("Rendimento al 31/12/2027 (cerchio vuoto) e alla manutenzione 2028 (pieno, con il valore)",
                  fontsize=7.4, color=INK2)
    ax.set_ylabel("stazione, matricola (manutenzione 2028)", fontsize=7.2, color=INK2)
    ax.set_title("Sette convertitori sotto il 95 % prima della manutenzione 2028", fontsize=9.6, loc="left",
                 fontweight="bold", color=INK)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.grid(axis="x", color="#E6E6E4", lw=0.6, zorder=0)
    from matplotlib.lines import Line2D
    leg = [Line2D([0], [0], marker="o", color=BENCH, ls="-", lw=2, label="al banco del 17-21 gennaio 2028",
                  mec="white"),
           Line2D([0], [0], marker="o", color=STAYS, ls="-", lw=2, label="resta alla manutenzione programmata",
                  mec="white")]
    ax.legend(handles=leg, loc="upper left", fontsize=7, frameon=False, bbox_to_anchor=(0.0, 0.93))
    fig.text(0.01, 0.012, "Curva di tutte le titolazioni 2025-2027 in funzione dell'NO2 convertito; carico della "
                          "stazione: media degli stessi giorni 2025-2027.\n" + P.ORG_SHORT +
                          ", servizio strumentazione, 5 gennaio 2028.", fontsize=5.9, color=INK2, va="bottom")
    fig.tight_layout(rect=(0, 0.045, 1, 1))
    fig.savefig(path, format="png", metadata={"Software": None})
    plt.close(fig)


def write(folder, G):
    os.makedirs(folder, exist_ok=True)
    workbook(os.path.join(folder, XLSX), G)
    chart(os.path.join(folder, PNG), G)
