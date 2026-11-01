"""Writes the evidence pack under target/ from the world. Every file is laid out the way its producing system
exports it; no file describes the data."""
import csv
import datetime as dt
import io
import os

import numpy as np
from openpyxl import Workbook

import world as W
from common import it_num, normalize_zip, pdf_setup, save_workbook, write_text

F_SURVEY = "mov_clienti_strutture_LV12_2025-07_2026-09_estr20261117.csv"
F_REGISTER = "registro_strutture_ricettive_LV12_20261116.xlsx"
F_CROSSWALK = "tabella_raccordo_CIR_CIN_20260504.csv"
F_CONC = "IDS_riepilogo_trimestrale_concessionario_2025_2026.xlsx"
F_PLV = "Comune_Porto_Levarna_IDS_dichiarazioni_2025_2026.csv"
F_SEM = "ids_santelvira_trimestri_2025_2026.csv"
F_LAR = "LidoArzena_riepilogo_imposta_soggiorno_2025_2026.pdf"
F_HILL = "servizio_tributi_associato_collina_IDS_2025_2026.csv"
F_POP = "popolazione_residente_1gennaio_2025_2026_LV12.csv"
F_VAR = "variazioni_amministrative_2026_estratto.txt"
F_RATES = "aliquote_imposta_soggiorno_comuni_LV12.csv"
F_REG = "Unione_Riviera_Levarna_regolamento_cofinanziamento_servizi_picco_2027.pdf"
F_AIR = "aeroporto_levarna_passeggeri_mensili_2025_2026.xlsx"
F_PARK = "parcheggi_lungomare_accessi_giornalieri_2026.csv"

CONC_COMUNI = ["MCE", "CFE", "TAL", "SMA", "ASV", "CLR", "ANM", "RFE", "MLU", "SDU", "PVE", "PFO"]
HILL_COMUNI = ["BSE", "CPI"]
UNION = "Unione dei Comuni della Riviera di Levarna"

NAME_ROOTS = {
    "albergo": ["Hotel", "Albergo", "Hotel", "Grand Hotel", "Park Hotel"],
    "campeggio": ["Camping", "Campeggio", "Villaggio Camping"],
    "casa vacanze": ["Casa Vacanze", "Residence", "Appartamenti", "Casa per Ferie"],
    "bed and breakfast": ["B&B", "Bed and Breakfast", "B&B"],
    "agriturismo": ["Agriturismo", "Agriturismo", "Azienda Agrituristica"],
    "affittacamere": ["Affittacamere", "Camere", "Guest House"],
}
NAME_WORDS = ["Miramare", "Bellavista", "Il Faro", "La Pineta", "Le Querce", "Villa Rosa", "Gabbiano", "Conchiglia",
              "Sole e Mare", "Riviera", "Panorama", "La Scogliera", "Il Poggio", "Belvedere", "Le Ginestre", "Corallo",
              "Delfino", "Stella Marina", "La Torre", "Il Mulino", "San Marco", "Oasi", "Le Palme", "Lungomare",
              "La Collina", "Il Castagno", "Approdo", "Vela Bianca", "Tramonto", "Il Glicine", "Aurora", "Mediterraneo",
              "La Baia", "I Gelsi", "Le Rondini", "Al Porto", "Il Borgo", "Ulivi", "La Fonte", "Maestrale", "Libeccio",
              "Il Carrubo", "La Lanterna", "Costa Azzurra", "Villa Ada", "Il Melograno", "La Meridiana", "Valverde"]


def names(w):
    rng = np.random.default_rng(W.SEED + 1)
    used = set()
    out = {}
    for e in w.est:
        for _ in range(20):
            nm = "%s %s" % (rng.choice(NAME_ROOTS[e["typ"]]), rng.choice(NAME_WORDS))
            if nm not in used:
                break
        if nm in used:
            nm = "%s %s" % (nm, w.comuni[e["comune0"]]["name"].split()[-1])
        k = 2
        base = nm
        while nm in used:
            nm = "%s %d" % (base, k)
            k += 1
        used.add(nm)
        out[e["idx"]] = nm
    return out


def fmt_dt(x):
    return x.strftime("%d/%m/%Y %H:%M")


def survey(w, root):
    rows = W.survey_rows(w)
    rows.sort(key=lambda r: (r["y"], r["m"], r["code"], r["ver"], r["country"]))
    buf = io.StringIO()
    buf.write("CODICE_STRUTTURA;ANNO;MESE;STATO;PAESE_RESIDENZA;ARRIVI;PRESENZE;DATA_INVIO;PROGR_INVIO\r\n")
    for r in rows:
        buf.write("%s;%d;%d;%s;%s;%d;%d;%s;%d\r\n" % (r["code"], r["y"], r["m"], r["state"], r["country"], r["arr"],
                                                     r["nights"], fmt_dt(r["sub"]), r["ver"]))
    write_text(os.path.join(root, F_SURVEY), buf.getvalue())
    return len(rows)


def period_text(e):
    first, last, lastday = e["season"]
    if (first, last, lastday) == (1, 12, 31):
        return "ANNUALE"
    return "01/%02d-%02d/%02d" % (first, lastday, last)


def register(w, root, nm):
    wb = Workbook()
    ws = wb.active
    ws.title = "STRUTTURE"
    ws.append(["CIN", "CIR", "DENOMINAZIONE", "COD_ISTAT_COMUNE", "COMUNE", "TIPOLOGIA", "CLASSIFICAZIONE",
               "POSTI_LETTO", "CAMERE_UNITA", "PERIODO_APERTURA", "DATA_INIZIO_ATTIVITA"])
    rng = np.random.default_rng(W.SEED + 2)
    active = [e for e in w.est if not e.get("ceased")]
    active.sort(key=lambda e: (w.comuni[e["comune"]]["istat"], e["cin"]))
    for e in active:
        c = w.comuni[e["comune"]]
        beds_now = W.beds_on(e, dt.date(2026, 11, 16))
        rooms = max(1, int(round(beds_now / float(rng.uniform(1.8, 2.6))))) if e["typ"] != "campeggio" else \
            max(10, int(round(beds_now / float(rng.uniform(3.2, 3.8)))))
        start = e.get("opened") or dt.date(int(rng.integers(1978, 2024)), int(rng.integers(1, 13)), 1)
        ws.append([e["cin"], e["cir"] or "", nm[e["idx"]], c["istat"], c["name"], e["typ"].upper(),
                   ("%d STELLE" % e["stars"]) if e["stars"] else "", beds_now, rooms, period_text(e),
                   start.strftime("%d/%m/%Y")])
    ws2 = wb.create_sheet("VARIAZIONI")
    ws2.append(["CIN", "DATA_DECORRENZA", "TIPO_VARIAZIONE", "DA", "A"])
    var = []
    for e in active:
        for (when, new) in e.get("bed_changes", []):
            var.append((e["cin"], when, "POSTI LETTO", str(e["beds"]), str(new)))
        if e.get("suspended"):
            var.append((e["cin"], dt.date(2025, 10, 1), "SOSPENSIONE TEMPORANEA", "ATTIVA", "SOSPESA"))
            var.append((e["cin"], dt.date(2025, 11, 1), "RIPRESA ATTIVITA'", "SOSPESA", "ATTIVA"))
    corr = [e for e in active if not e.get("bed_changes") and not e.get("opened") and e["cir"]]
    for j in rng.permutation(len(corr))[:34]:
        e = corr[int(j)]
        wrong = int(round(e["beds"] * float(rng.choice([.6, .7, 1.3, 1.45]))))
        when = dt.date(2026, int(rng.integers(1, 7)), int(rng.choice([3, 12, 21])))
        var.append((e["cin"], when, "RETTIFICA POSTI LETTO", str(wrong), str(e["beds"])))
    for j in rng.permutation(len(active))[:23]:
        e = active[int(j)]
        when = dt.date(int(rng.choice([2025, 2026])), int(rng.integers(1, 10)), int(rng.choice([1, 15])))
        var.append((e["cin"], when, "DENOMINAZIONE", nm[e["idx"]] + " (gestione precedente)", nm[e["idx"]]))
    var.sort(key=lambda v: (v[1], v[0], v[2]))
    for v in var:
        ws2.append([v[0], v[1].strftime("%d/%m/%Y"), v[2], v[3], v[4]])
    save_workbook(wb, os.path.join(root, F_REGISTER))
    return len(active), len(var)


def crosswalk(w, root):
    rows = [e for e in w.est if e["cir"] and e["cin"]]
    rows.sort(key=lambda e: e["cir"])
    buf = io.StringIO()
    buf.write("CIR;CIN;DATA_ATTRIBUZIONE\r\n")
    for e in rows:
        buf.write("%s;%s;%s\r\n" % (e["cir"], e["cin"], "04/05/2026"))
    write_text(os.path.join(root, F_CROSSWALK), buf.getvalue())
    return len(rows)


def decl_records(w):
    """Every declaration row as filed, amended ones twice (the first filing and its correction)."""
    rng = np.random.default_rng(W.SEED + 3)
    recs = []
    prot = 1000
    for key in sorted(w.decl, key=lambda k: (k[1], k[2], k[0], k[3])):
        com, y, q, cat = key
        d = w.decl[key]
        qend = dt.date(y, 3 * q, 30 if 3 * q in (6, 9) else 31)
        due = qend + dt.timedelta(days=16)
        filed_on = due - dt.timedelta(days=int(rng.integers(0, 12)))
        prot += int(rng.integers(3, 40))
        if key in w.decl_supp:
            # the first filing left some establishments out; a later filing adds their nights
            sp = w.decl_supp[key]
            recs.append(dict(com=com, y=y, q=q, cat=cat, total=d["total"] - sp["total"], exempt=d["exempt"] - sp["exempt"],
                             liable=d["liable"] - sp["liable"], prot=prot, date=filed_on))
            prot += int(rng.integers(3, 40))
            recs.append(dict(com=com, y=y, q=q, cat=cat, total=sp["total"], exempt=sp["exempt"], liable=sp["liable"],
                             prot=prot + 400, date=filed_on + dt.timedelta(days=int(rng.integers(40, 90)))))
            continue
        if key in w.decl_amend:
            a = w.decl_amend[key]
            recs.append(dict(com=com, y=y, q=q, cat=cat, total=a["total"], exempt=a["exempt"], liable=a["liable"],
                             prot=prot, date=filed_on))
            prot += int(rng.integers(3, 40))
            second = min(filed_on + dt.timedelta(days=int(rng.integers(35, 70))), dt.date(2026, 10, 29))
            if second <= filed_on:
                second = filed_on + dt.timedelta(days=9)
            recs.append(dict(com=com, y=y, q=q, cat=cat, total=d["total"], exempt=d["exempt"], liable=d["liable"],
                             prot=prot + 400, date=second))
        else:
            recs.append(dict(com=com, y=y, q=q, cat=cat, total=d["total"], exempt=d["exempt"], liable=d["liable"],
                             prot=prot, date=filed_on))
    return recs


def declarations(w, root):
    recs = decl_records(w)
    # the provincial concessionaire's workbook, one sheet per comune it collects for
    wb = Workbook()
    wb.remove(wb.active)
    for key in CONC_COMUNI:
        rows = [r for r in recs if r["com"] == key]
        if not rows:
            continue
        ws = wb.create_sheet(w.comuni[key]["name"][:31])
        ws.append(["Comune", w.comuni[key]["name"], "Codice ISTAT", w.comuni[key]["istat"]])
        ws.append([])
        ws.append(["Anno", "Trimestre", "Categoria struttura", "Pernottamenti totali", "di cui esenti",
                   "Pernottamenti soggetti", "N. protocollo", "Data presentazione"])
        for r in sorted(rows, key=lambda r: (r["y"], r["q"], r["cat"], r["date"])):
            ws.append([r["y"], "%d° trimestre" % r["q"], r["cat"], r["total"], r["exempt"], r["liable"],
                       "%d/%d" % (r["y"] if r["date"].year == r["y"] else r["date"].year, r["prot"]),
                       r["date"].strftime("%d/%m/%Y")])
    save_workbook(wb, os.path.join(root, F_CONC), creator="Concessionario riscossione tributi")
    # Porto Levarna's own office: semicolons, Italian dates
    buf = io.StringIO()
    buf.write("PERIODO;TIPOLOGIA;PRESENZE_TOTALI;PRESENZE_ESENTI;PRESENZE_IMPONIBILI;DATA_RICEZIONE;ID_DICHIARAZIONE\r\n")
    for r in sorted([r for r in recs if r["com"] == "PLV"], key=lambda r: (r["y"], r["q"], r["cat"], r["date"])):
        buf.write("%d-T%d;%s;%d;%d;%d;%s;PL%d\r\n" % (r["y"], r["q"], r["cat"].upper(), r["total"], r["exempt"],
                                                     r["liable"], r["date"].strftime("%d/%m/%Y"), r["prot"]))
    write_text(os.path.join(root, F_PLV), buf.getvalue())
    # Sant'Elvira a Mare: commas, ISO dates
    buf = io.StringIO()
    wr = csv.writer(buf, lineterminator="\n")
    wr.writerow(["anno", "trimestre", "categoria", "notti_totali", "notti_esenti", "notti_imponibili", "protocollo",
                 "data_protocollo"])
    for r in sorted([r for r in recs if r["com"] == "SEM"], key=lambda r: (r["y"], r["q"], r["cat"], r["date"])):
        wr.writerow([r["y"], r["q"], r["cat"], r["total"], r["exempt"], r["liable"], "SE-%d" % r["prot"],
                     r["date"].isoformat()])
    write_text(os.path.join(root, F_SEM), buf.getvalue())
    # the hill comuni's shared tax office: one file, comune name in a column, quarters as text
    buf = io.StringIO()
    buf.write("Ente;Periodo di riferimento;Tipologia;Presenze dichiarate;Presenze esenti;Presenze soggette;Prot.;Data\r\n")
    qtext = {1: "gen-mar", 2: "apr-giu", 3: "lug-set", 4: "ott-dic"}
    for r in sorted([r for r in recs if r["com"] in HILL_COMUNI], key=lambda r: (r["com"], r["y"], r["q"], r["cat"], r["date"])):
        buf.write("Comune di %s;%s %d;%s;%d;%d;%d;%d;%s\r\n" % (w.comuni[r["com"]]["name"], qtext[r["q"]], r["y"],
                                                              r["cat"], r["total"], r["exempt"], r["liable"], r["prot"],
                                                              r["date"].strftime("%d/%m/%Y")))
    write_text(os.path.join(root, F_HILL), buf.getvalue())
    # Lido di Arzena publishes a pdf summary
    lar_pdf(w, [r for r in recs if r["com"] == "LAR"], os.path.join(root, F_LAR))
    return recs


def lar_pdf(w, rows, path):
    pdf_setup()
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    st = getSampleStyleSheet()
    doc = SimpleDocTemplate(path, pagesize=A4, title="Imposta di soggiorno - riepilogo dichiarazioni",
                            author="Comune di Lido di Arzena - Ufficio Tributi", leftMargin=50, rightMargin=50)
    el = [Paragraph("COMUNE DI LIDO DI ARZENA", st["Title"]),
          Paragraph("Ufficio Tributi - Imposta di soggiorno", st["Heading3"]),
          Paragraph("Riepilogo delle dichiarazioni trimestrali dei gestori delle strutture ricettive, "
                    "anni 2025 e 2026 (dichiarazioni pervenute al 31/10/2026).", st["Normal"]), Spacer(1, 12)]
    data = [["Anno", "Trim.", "Categoria", "Pernott. totali", "Esenti", "Soggetti", "Prot.", "Ricevuta il"]]
    for r in sorted(rows, key=lambda r: (r["y"], r["q"], r["cat"], r["date"])):
        data.append([str(r["y"]), "%d" % r["q"], r["cat"], "{:,}".format(r["total"]).replace(",", "."),
                     "{:,}".format(r["exempt"]).replace(",", "."), "{:,}".format(r["liable"]).replace(",", "."),
                     str(r["prot"]), r["date"].strftime("%d/%m/%Y")])
    t = Table(data, repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8), ("FONT", (0, 1), (-1, -1), "Helvetica", 8),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("ALIGN", (3, 1), (5, -1), "RIGHT")]))
    el.append(t)
    el.append(Spacer(1, 14))
    el.append(Paragraph("Il Responsabile del Servizio Tributi - Martino Zamengo", st["Normal"]))
    doc.build(el)


def population(w, root):
    rng = np.random.default_rng(W.SEED + 4)
    buf = io.StringIO()
    buf.write("Codice comune;Comune;Data;Maschi;Femmine;Totale\r\n")
    for when, field in ((dt.date(2025, 1, 1), "res2025"), (dt.date(2026, 1, 1), "res2026")):
        for key in sorted(w.comuni, key=lambda k: w.comuni[k]["istat"]):
            c = w.comuni[key]
            tot = c[field]
            if tot is None:
                continue
            males = int(round(tot * float(rng.uniform(.478, .498))))
            buf.write("%s;%s;%s;%d;%d;%d\r\n" % (c["istat"], c["name"], when.strftime("%d/%m/%Y"), males, tot - males, tot))
    write_text(os.path.join(root, F_POP), buf.getvalue())


def variations(w, root):
    lines = ["ISTAT - Variazioni amministrative e territoriali dei comuni - estratto provincia 112",
             "Elaborazione del 15/01/2026", "",
             "%-10s %-12s %-24s %-12s %-24s %-10s" % ("TIPO", "COD_ORIGINE", "DENOMINAZIONE_ORIGINE", "COD_ESITO",
                                                      "DENOMINAZIONE_ESITO", "DECORRENZA"),
             "%-10s %-12s %-24s %-12s %-24s %-10s" % ("ES", "112006", "Torre Alvea", "112020", "Alvea Salvina", "01/01/2026"),
             "%-10s %-12s %-24s %-12s %-24s %-10s" % ("ES", "112007", "Salvina Marina", "112020", "Alvea Salvina", "01/01/2026"),
             "%-10s %-12s %-24s %-12s %-24s %-10s" % ("CS", "", "", "112020", "Alvea Salvina", "01/01/2026"),
             "", "Riferimento: legge regionale di fusione n. 31 del 18/11/2025.", ""]
    write_text(os.path.join(root, F_VAR), "\r\n".join(lines))


def rates(w, root):
    buf = io.StringIO()
    buf.write("COMUNE;COD_ISTAT;CATEGORIA;EURO_PER_PERNOTTAMENTO;IN_VIGORE_DAL;IN_VIGORE_AL\r\n")
    for r in sorted(w.rates, key=lambda r: (w.comuni[r["comune"]]["istat"], r["cat"], r["start"])):
        c = w.comuni[r["comune"]]
        buf.write("%s;%s;%s;%s;%s;%s\r\n" % (c["name"], c["istat"], r["cat"], it_num(r["rate"], 2),
                                             r["start"].strftime("%d/%m/%Y"),
                                             r["end"].strftime("%d/%m/%Y") if r["end"] else ""))
    write_text(os.path.join(root, F_RATES), buf.getvalue())


def regulation(w, root):
    pdf_setup()
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer
    st = getSampleStyleSheet()
    path = os.path.join(root, F_REG)
    doc = SimpleDocTemplate(path, pagesize=A4, title="Regolamento cofinanziamento servizi di picco 2027",
                            author=UNION, leftMargin=60, rightMargin=60)
    P = lambda t, s="Normal": Paragraph(t, st[s])
    el = [P(UNION.upper(), "Title"),
          P("Regolamento per il cofinanziamento dei servizi del mese di picco, anno 2027", "Heading2"),
          P("Approvato con deliberazione dell'Assemblea dell'Unione n. 14 del 29/09/2026"), Spacer(1, 10),
          P("Art. 1 - Oggetto", "Heading4"),
          P("L'Unione cofinanzia, nel mese di agosto 2027, il potenziamento dei servizi associati di raccolta dei "
            "rifiuti, di salvamento a mare e di polizia locale nei comuni membri nei quali la presenza turistica "
            "del mese di picco grava in misura rilevante sui servizi dimensionati per i residenti."),
          P("Art. 2 - Comuni beneficiari", "Heading4"),
          P("Accede al cofinanziamento ogni comune membro nel quale i pernottamenti trascorsi nel mese di agosto "
            "2026 negli esercizi ricettivi del proprio territorio raggiungono almeno 30 per ciascun residente "
            "iscritto in anagrafe al 1 gennaio 2026 secondo il bilancio demografico ISTAT."),
          P("Art. 3 - Pernottamenti", "Heading4"),
          P("Sono pernottamenti tutte le notti trascorse da tutti gli ospiti negli esercizi ricettivi iscritti al "
            "registro regionale delle strutture ricettive, siano esse soggette all'imposta di soggiorno o esenti. "
            "Le rilevazioni mensili della Regione sul movimento dei clienti negli esercizi ricettivi e le "
            "dichiarazioni trimestrali dei gestori ai fini dell'imposta di soggiorno registrano gli stessi "
            "pernottamenti."),
          P("Art. 4 - Comuni membri", "Heading4"),
          P("Sono comuni membri, ai fini del presente regolamento, i comuni facenti parte dell'Unione al 1 gennaio "
            "2026. Il comune di Alvea Salvina, istituito a tale data, partecipa come un unico comune."),
          P("Art. 5 - Misura del cofinanziamento", "Heading4"),
          P("A ciascun comune beneficiario e' riconosciuto un contributo di 38.000 euro per il potenziamento dei "
            "servizi di cui all'art. 1, erogato in due rate entro il 30 giugno e il 30 settembre 2027."),
          P("Art. 6 - Istruttoria", "Heading4"),
          P("L'Ufficio di piano dei servizi associati predispone l'elenco dei comuni beneficiari sulla base dei "
            "dati disponibili al 20 novembre 2026 e lo sottopone all'Assemblea dell'Unione entro il 15 dicembre "
            "2026. L'elenco approvato non e' soggetto a revisione."), Spacer(1, 14),
          P("Il Presidente dell'Unione - Goffredo Canil")]
    doc.build(el)


def distractors(w, root):
    rng = np.random.default_rng(W.SEED + 5)
    wb = Workbook()
    ws = wb.active
    ws.title = "Traffico"
    ws.append(["Anno", "Mese", "Passeggeri arrivi", "Passeggeri partenze", "Movimenti aerei"])
    base = [11, 10, 13, 18, 24, 31, 38, 41, 33, 21, 12, 12]
    for (y, m) in W.MONTHS:
        g = 1.0 if y == 2025 else 1.06
        arr = int(base[m - 1] * 1000 * g * float(rng.uniform(.93, 1.07)))
        dep = int(arr * float(rng.uniform(.96, 1.04)))
        ws.append([y, m, arr, dep, int((arr + dep) / float(rng.uniform(118, 132)))])
    save_workbook(wb, os.path.join(root, F_AIR), creator="Aeroporto di Levarna - statistiche di traffico")
    buf = io.StringIO()
    buf.write("data;parcheggio;ingressi_auto;ingressi_moto\r\n")
    lots = ["P1 Lungomare Nord", "P2 Porto Turistico", "P3 Lido Centrale", "P4 Pineta", "P5 Scogliera"]
    d = dt.date(2026, 6, 1)
    while d <= dt.date(2026, 9, 30):
        season = {6: .62, 7: .86, 8: 1.0, 9: .55}[d.month]
        wkend = 1.25 if d.weekday() >= 5 else 1.0
        for j, lot in enumerate(lots):
            cars = int(season * wkend * [820, 640, 910, 530, 380][j] * float(rng.uniform(.82, 1.12)))
            bikes = int(cars * float(rng.uniform(.08, .16)))
            buf.write("%s;%s;%d;%d\r\n" % (d.strftime("%d/%m/%Y"), lot, cars, bikes))
        d += dt.timedelta(days=1)
    write_text(os.path.join(root, F_PARK), buf.getvalue())


def write_pack(root):
    w = W.build()
    nm = names(w)
    os.makedirs(root, exist_ok=True)
    stats = {}
    stats["survey_rows"] = survey(w, root)
    stats["register_rows"], stats["variation_rows"] = register(w, root, nm)
    stats["crosswalk_rows"] = crosswalk(w, root)
    declarations(w, root)
    population(w, root)
    variations(w, root)
    rates(w, root)
    regulation(w, root)
    distractors(w, root)
    return w, stats


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "/tmp/t123_pack"
    w, stats = write_pack(out)
    print(stats)
    for f in sorted(os.listdir(out)):
        print(f, os.path.getsize(os.path.join(out, f)))
