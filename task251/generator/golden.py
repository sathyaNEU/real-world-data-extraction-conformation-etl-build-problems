"""task251 goldens: the recalibration workbook (the meters to send, every meter's systematic error with the pairings
it rests on, the two 2027 indicators of POCT-GLU-02 section 8, the notes) and the chart of every meter's systematic
error against the 5 per cent band."""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

import params as P
import postprocess
import writeup as WU

XLSX = "ritiro_glucometri_gennaio_2028.xlsx"
PNG = "errore_sistematico_glucometri_2027.png"
SEND = "#eb6834"          # categorical slot 2: to the recalibration
STAY = "#2a78d6"          # categorical slot 1: stays on the ward
INK, INK2 = "#0b0b0b", "#52514e"
WARD_NAME = {"TIN": "Terapia intensiva neonatale", "NIDO": "Nido", "TI": "Terapia intensiva", "DIAB": "Diabetologia",
             "PS": "Pronto soccorso", "MED": "Medicina generale", "CHIR": "Chirurgia generale", "PED": "Pediatria",
             "OST": "Ostetricia e ginecologia", "MEDR": "Medicina", "PSR": "Pronto soccorso", "MEDV": "Medicina",
             "LUN": "Lungodegenza"}
HOSP_ORDER = ["Presidio di Castelmarne", "Presidio di Rivobello", "Presidio di Valdarena"]


def _head(ws, row, head, height=32):
    thin = Side(style="thin", color="A6ADB8")
    for j, h in enumerate(head, 1):
        c = ws.cell(row=row, column=j, value=h)
        c.font = Font(bold=True, size=9.5)
        c.fill = PatternFill("solid", fgColor="E4E9F0")
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        c.border = Border(bottom=thin)
    ws.row_dimensions[row].height = height


def _widths(ws, widths):
    for k, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(k)].width = w


def _title(ws, title, sub):
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = sub
    ws["A2"].font = Font(italic=True, size=9, color="52514E")


def _order(G):
    reg = G["reg"]
    wards = WU.WARD_ORDER
    return sorted(G["errors"], key=lambda m: (HOSP_ORDER.index(reg.loc[m, "presidio"]),
                                              wards.index(reg.loc[m, "reparto"]), m))


def workbook(path, fig):
    G = fig["_golden"]
    reg, e, listed, n = G["reg"], G["errors"], G["listed"], G["pairs_used"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Ritiro gennaio 2028"
    _title(ws, "Glucometri da ritarare alla visita Corvenza del 17-21 gennaio 2028: %d su %d" % (len(listed), len(e)),
           "Errore sistematico oltre il 5 per cento, in più o in meno (POCT-GLU-02, sezione 7). Ufficio POCT, "
           "5 gennaio 2028.")
    head = ["Matricola", "Presidio", "Reparto", "Errore sistematico (%)", "Abbinamenti del piano usati"]
    _head(ws, 4, head)
    r = 5
    for m in sorted(listed, key=lambda m: (HOSP_ORDER.index(reg.loc[m, "presidio"]),
                                           WU.WARD_ORDER.index(reg.loc[m, "reparto"]), m)):
        ws.append([m, reg.loc[m, "presidio"], reg.loc[m, "reparto"], round(e[m], 1), int(n[m])])
        ws.cell(row=r, column=4).number_format = "+0.0;-0.0;0.0"
        r += 1
    _widths(ws, [13, 24, 10, 14, 14])
    ws.freeze_panes = "A5"

    ws2 = wb.create_sheet("Tutti i glucometri")
    _title(ws2, "Errore sistematico di ogni glucometro sulla taratura in corso",
           "Abbinamenti del piano (giro del mattino 6:00-7:30) successivi all'ultima taratura; laboratorio sulla "
           "scala del Kelvar C900.")
    _head(ws2, 4, ["Matricola", "Presidio", "Reparto", "Ultima taratura", "Abbinamenti del piano usati",
                   "Errore sistematico (%)", "Esito"])
    r = 5
    for m in _order(G):
        ws2.append([m, reg.loc[m, "presidio"], reg.loc[m, "reparto"], reg.loc[m, "ultima_taratura"].date(), int(n[m]),
                    round(e[m], 1), "da ritarare" if m in listed else "resta in reparto"])
        ws2.cell(row=r, column=4).number_format = "dd/mm/yyyy"
        ws2.cell(row=r, column=6).number_format = "+0.0;-0.0;0.0"
        if m in listed:
            for j in range(1, 8):
                ws2.cell(row=r, column=j).font = Font(bold=True)
        r += 1
    _widths(ws2, [13, 24, 10, 14, 14, 14, 16])
    ws2.freeze_panes = "A5"
    ws2.auto_filter.ref = "A4:G%d" % (r - 1)

    ws3 = wb.create_sheet("Indicatori 2027")
    a = fig["asks"]
    _title(ws3, "Indicatori 2027 (POCT-GLU-02, sezione 8)",
           "Risultati dei pazienti, uno per test; reparto e presidio in cui il glucometro si trovava il giorno del "
           "test; ora italiana.")
    _head(ws3, 4, ["Presidio", "1° trimestre", "2° trimestre", "3° trimestre", "4° trimestre"])
    ws3.cell(row=3, column=1, value="Quota dei risultati pervenuti in cartella clinica più di due ore dopo il test (%)"
             ).font = Font(bold=True, size=9.5)
    r = 5
    for h, name in WU.HOSP.items():
        ws3.append([name] + [a["late_share_pct"][h][str(q)] for q in (1, 2, 3, 4)])
        for j in range(2, 6):
            ws3.cell(row=r, column=j).number_format = "0.0"
        r += 1
    r += 1
    ws3.cell(row=r, column=1, value="Test eseguiti sui pazienti nel 2027, per reparto").font = Font(bold=True, size=9.5)
    r += 1
    for j, h in enumerate(["Reparto", "Presidio", "Test"], 1):
        c = ws3.cell(row=r, column=j, value=h)
        c.font = Font(bold=True, size=9.5)
        c.fill = PatternFill("solid", fgColor="E4E9F0")
    r += 1
    hosp_of = {"TIN": "CM", "NIDO": "CM", "TI": "CM", "DIAB": "CM", "PS": "CM", "MED": "CM", "CHIR": "CM",
               "PED": "RB", "OST": "RB", "MEDR": "RB", "PSR": "RB", "MEDV": "VD", "LUN": "VD"}
    tot = 0
    for w in WU.WARD_ORDER:
        ws3.cell(row=r, column=1, value="%s (%s)" % (w, WARD_NAME[w]))
        ws3.cell(row=r, column=2, value=WU.HOSP[hosp_of[w]])
        c = ws3.cell(row=r, column=3, value=a["tests_2027"][w])
        c.number_format = "#,##0"
        tot += a["tests_2027"][w]
        r += 1
    ws3.cell(row=r, column=1, value="Totale").font = Font(bold=True)
    c = ws3.cell(row=r, column=3, value=tot)
    c.number_format = "#,##0"
    c.font = Font(bold=True)
    _widths(ws3, [34, 24, 13, 13, 13])

    ws4 = wb.create_sheet("Note")
    notes = [
        "Note",
        "Errore sistematico: il fattore e per cui il glucometro legge il valore del laboratorio moltiplicato per (1 + e) "
        "(POCT-GLU-02, sezione 7), stimato come media dei rapporti glucometro / laboratorio meno uno.",
        "Abbinamenti usati: quelli del piano dell'Ufficio POCT, nel giorno del glucometro con il prelievo del "
        "laboratorio fra le 6:00 e le 7:30, successivi all'ultima taratura. Le conferme dei valori critici (sezione 6) "
        "nascono dal risultato stesso del glucometro e non ne misurano l'errore sistematico.",
        "Laboratorio: i valori del Kelvar C600, fino al 12 settembre 2027, divisi per 1,035 (nota del laboratorio del "
        "7 settembre 2027).",
        "Indicatori: ogni test contato una volta (matricola e numero di memoria, alla prima ricezione); l'ora del test "
        "è quella del glucometro meno un'ora, perché gli orologi dei glucometri restano sull'ora solare.",
        "Dati al 3 gennaio 2028: GlyLink_risultati_2026-2027.csv, GlyLink_abbinamenti_laboratorio_2026-2027.xlsx, "
        "piano_abbinamenti_glucometri_2026-2027.xlsx, anagrafica_glucometri.xlsx.",
    ]
    for k, t in enumerate(notes, 1):
        c = ws4.cell(row=k, column=1, value=t)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if k == 1:
            c.font = Font(bold=True, size=12)
    ws4.column_dimensions["A"].width = 120
    wb.properties.creator = "Ufficio POCT, " + P.ORG
    wb.save(path)


def chart(path, fig):
    G = fig["_golden"]
    reg, e, listed = G["reg"], G["errors"], G["listed"]
    order = _order(G)
    nrow = len(order)
    plt.rcParams["font.family"] = "DejaVu Sans"
    f, ax = plt.subplots(figsize=(8.6, 11.2), dpi=150)
    ax.axvspan(-5, 5, color="#EEF1F5", zorder=0)
    for x in (-5, 5):
        ax.axvline(x, color=INK2, lw=1.0, ls=(0, (4, 3)), zorder=1)
    ax.text(5.15, nrow - 0.2, "+5 %", fontsize=7.4, color=INK2, va="bottom")
    ax.text(-5.15, nrow - 0.2, "−5 %", fontsize=7.4, color=INK2, va="bottom", ha="right")
    ax.axvline(0, color="#C9CDD3", lw=0.8, zorder=1)
    ylab = []
    prev = None
    for i, m in enumerate(order):
        y = nrow - 1 - i
        h = reg.loc[m, "presidio"]
        if prev is not None and h != prev:
            ax.axhline(y + 0.5, color="#B9BEC6", lw=0.7, zorder=1)
        prev = h
        col = SEND if m in listed else STAY
        ax.plot([0, e[m]], [y, y], color=col, lw=1.4, alpha=0.55, zorder=2, solid_capstyle="round")
        ax.plot([e[m]], [y], "o", ms=6.5, color=col, mec="white", mew=1.0, zorder=3)
        if m in listed:
            ax.text(e[m] + (0.45 if e[m] > 0 else -0.45), y, ("%+.1f" % e[m]).replace("-", "\u2212"), va="center",
                    ha="left" if e[m] > 0 else "right", fontsize=7.0, color=INK, fontweight="bold")
        ylab.append("%s  %s" % (reg.loc[m, "reparto"], m))
    ax.set_yticks(range(nrow - 1, -1, -1))
    ax.set_yticklabels(ylab, fontsize=6.6, color=INK2)
    for lab, m in zip(ax.get_yticklabels(), order):
        if m in listed:
            lab.set_color(INK)
            lab.set_fontweight("bold")
    ax.set_xlim(-14, 14)
    ax.set_ylim(-0.8, nrow - 0.2 + 1.0)
    ax.set_xticks([-12, -8, -5, 0, 5, 8, 12])
    ax.set_xticklabels(["−12 %", "−8 %", "−5 %", "0", "+5 %", "+8 %", "+12 %"], fontsize=7.4, color=INK2)
    ax.set_xlabel("errore sistematico rispetto al laboratorio (scala Kelvar C900), %", fontsize=7.6, color=INK2)
    ax.grid(axis="x", color="#E6E6E4", lw=0.6, zorder=0)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color("#B9BEC6")
    # hospital names at the left of each block
    starts = {}
    for i, m in enumerate(order):
        starts.setdefault(reg.loc[m, "presidio"], []).append(nrow - 1 - i)
    for h, ys in starts.items():
        ax.text(13.8, max(ys) + 0.1, h.replace("Presidio di ", ""), ha="right", va="top", fontsize=7.6, color=INK2,
                fontstyle="italic")
    f.suptitle("Otto glucometri su %d oltre il 5 per cento: da ritarare a gennaio 2028" % nrow, x=0.04, ha="left",
               fontsize=11.5, fontweight="bold", color=INK, y=0.985)
    f.text(0.04, 0.957, "Errore sistematico sugli abbinamenti del piano (giro del mattino 6:00-7:30) dall'ultima "
           "taratura, gennaio 2027", fontsize=7.8, color=INK2, ha="left")
    leg = [Line2D([0], [0], marker="o", color=SEND, ls="-", lw=1.4, label="da ritarare (%d)" % len(listed),
                  markersize=6.5, mec="white"),
           Line2D([0], [0], marker="o", color=STAY, ls="-", lw=1.4, label="resta in reparto (%d)" % (nrow - len(listed)),
                  markersize=6.5, mec="white")]
    ax.legend(handles=leg, loc="upper left", fontsize=7.2, frameon=False, bbox_to_anchor=(-0.02, -0.045), ncol=2)
    f.text(0.04, 0.008, "Fonte: GlyLink, abbinamenti glucometro-laboratorio luglio 2026 - dicembre 2027; Ufficio POCT, "
           + P.ORG + ", 5 gennaio 2028.", fontsize=5.9, color=INK2, va="bottom")
    f.subplots_adjust(left=0.2, right=0.97, top=0.94, bottom=0.095)
    f.savefig(path, dpi=150, metadata={"Software": None})
    plt.close(f)


def write(outdir, fig):
    os.makedirs(outdir, exist_ok=True)
    x, p = os.path.join(outdir, XLSX), os.path.join(outdir, PNG)
    workbook(x, fig)
    postprocess.scrub(x, "Ufficio POCT", "2028-01-05")
    postprocess.finish_office(x, "2028-01-04T15:20:00Z", "2028-01-05T09:42:00Z", P.ORG)
    chart(p, fig)
    return x, p
