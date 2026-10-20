"""task251 documents: the trust's procedure for the bedside glucose meters (pdf), the laboratory's note on the
analyzer change (pdf), the manufacturer's 2027 service report (pdf), the manufacturer's mail fixing the January 2028
visit (eml), the data dictionary (md). Italian throughout, as the trust writes."""
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P
import sim

MESI = ["gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre",
        "novembre", "dicembre"]


def it_date(d):
    return "%d %s %d" % (d.day, MESI[d.month - 1], d.year)


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.4, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.0, leading=16.5,
                        spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8, leading=10.5, textColor=colors.HexColor("#444444"))
    return body, h1, h2, small


def _footer(text):
    def foot(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#555555"))
        canvas.drawString(20 * mm, 10 * mm, text)
        canvas.drawRightString(A4[0] - 20 * mm, 10 * mm, "pag. %d" % d.page)
        canvas.restoreState()
    return foot


def _table(rows, widths, size=8.2):
    t = Table(rows, colWidths=[w * mm for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", size),
                           ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", size),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def procedure(path, F):
    body, h1, h2, small = _styles()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title="POCT-GLU-02 Gestione dei glucometri", author=P.ORG,
                            creator=P.ORG, subject="POCT-GLU-02 rev. 3", invariant=1)
    s = [Paragraph(P.ORG + ", " + P.POCT_OFFICE, small), Spacer(1, 2 * mm),
         Paragraph("Gestione dei glucometri per uso professionale nei reparti", h1),
         Paragraph("Procedura POCT-GLU-02, revisione 3 del 14 aprile 2026, in vigore dal 1° maggio 2026. Redatta "
                   "dall'Ufficio POCT, verificata dal direttore della SC Medicina di Laboratorio, approvata dalla "
                   "Direzione sanitaria.", small),
         Spacer(1, 3 * mm)]
    sec = [
        ("1. Scopo e campo di applicazione", [
            "La procedura regola l'uso dei glucometri " + P.METER + " nei tredici reparti dei presidi di "
            "Castelmarne, Rivobello e Valdarena: il controllo di qualità quotidiano, gli abbinamenti con il "
            "laboratorio, i valori critici, la trasmissione dei risultati alla cartella clinica e il ritiro dei "
            "glucometri da ritarare."]),
        ("2. Responsabilità", [
            "L'Ufficio POCT tiene l'anagrafica dei glucometri, il piano degli abbinamenti e il gestionale " + P.DMS +
            ". I coordinatori infermieristici garantiscono che il personale esegua i controlli e riponga i "
            "glucometri sulla stazione di collegamento. Il laboratorio del presidio di Castelmarne esegue la "
            "glicemia sui campioni venosi di tutti e tre i presidi (provette con fluoruro)."]),
        ("3. Il glucometro e il gestionale", [
            "Il glucometro misura la glicemia su sangue capillare e la riporta come glicemia plasmatica in mg/dL, "
            "fra 20 e 600 mg/dL; sotto e sopra questo intervallo mostra LO e HI. Conserva ogni risultato con un "
            "numero progressivo di memoria, la data e l'ora del proprio orologio, l'operatore e il paziente.",
            "Riposto sulla stazione di collegamento, il glucometro trasmette al gestionale " + P.DMS + " i risultati "
            "registrati dal collegamento precedente; il gestionale inoltra subito i risultati dei pazienti alla "
            "cartella clinica elettronica. Un risultato è disponibile in cartella dal momento in cui il gestionale "
            "lo riceve."]),
        ("4. Controllo di qualità", [
            "All'inizio del turno del mattino ogni glucometro esegue il controllo con le soluzioni di livello 1 e "
            "2. Le soluzioni di controllo verificano il funzionamento del glucometro e delle strisce, non "
            "l'esattezza sul sangue, che si stabilisce soltanto per confronto con il laboratorio."]),
        ("5. Abbinamenti con il laboratorio", [
            "Quando l'infermiere legge sul glucometro il codice a barre di una provetta inviata al laboratorio, il "
            "gestionale abbina il risultato del glucometro al risultato del laboratorio su quella provetta. Ogni "
            "glucometro è abbinato almeno nei giorni del piano dell'Ufficio POCT: al giro dei prelievi del mattino "
            "(dalle 6:00 alle 7:30), al momento del prelievo venoso di un paziente, l'infermiere esegue la "
            "glicemia capillare con il glucometro e legge sul glucometro il codice a barre della provetta. Se il "
            "giorno del "
            "piano è festivo, l'abbinamento si fa il primo giorno feriale successivo."]),
        ("6. Valori critici", [
            "Un risultato del glucometro inferiore a 50 mg/dL o superiore a 400 mg/dL, LO e HI compresi, è "
            "comunicato subito al medico e confermato con un prelievo venoso inviato al laboratorio entro 30 "
            "minuti; l'infermiere legge sul glucometro il codice a barre della provetta di conferma."]),
        ("7. Errore sistematico e ritiro", [
            "Il glucometro legge il valore del laboratorio moltiplicato per (1 + e), dove e, l'errore sistematico "
            "del glucometro, è lo stesso a ogni concentrazione e si esprime in percentuale; si stima come media dei "
            "rapporti fra il valore del glucometro e quello del laboratorio, meno uno; le letture LO e HI, che non "
            "hanno un valore, non entrano nella stima. L'errore sistematico si "
            "riferisce alla taratura in corso del glucometro, cioè ai risultati successivi all'ultima taratura "
            "eseguita dal fornitore, e al metodo del laboratorio in uso alla data della valutazione.",
            "Un glucometro con errore sistematico oltre il 5 per cento, in più o in meno, è ritirato e ritarato "
            "alla visita annuale del fornitore prevista dal contratto di assistenza; gli altri restano in reparto."]),
        ("8. Indicatori annuali", [
            "In gennaio l'Ufficio POCT trasmette al fornitore l'elenco dei glucometri da ritarare e alla Direzione "
            "sanitaria gli indicatori dell'anno precedente: per presidio e trimestre, la quota dei risultati dei "
            "pazienti pervenuti alla cartella clinica più di due ore dopo il test; per reparto, il numero dei test "
            "eseguiti sui pazienti nel reparto."]),
        ("9. Registri", [
            "Risultati ricevuti dal gestionale (" + F["export"] + "); abbinamenti con il laboratorio (" +
            F["pairs"] + "); piano degli abbinamenti (" + F["plan"] + "); anagrafica dei glucometri (" +
            F["register"] + ")."]),
    ]
    for head, paras in sec:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))
    s.append(Spacer(1, 4 * mm))
    s.append(_table([["Revisione", "Data", "Modifica"],
                     ["1", "03/06/2019", "Prima emissione"],
                     ["2", "20/02/2023", "Valori critici a 50 e 400 mg/dL; provette con fluoruro"],
                     ["3", "14/04/2026", "Gestionale " + P.DMS + "; piano degli abbinamenti per glucometro"]],
                    [22, 24, 124]))
    foot = _footer("POCT-GLU-02 rev. 3")
    doc.build(s, onFirstPage=foot, onLaterPages=foot)


def lab_note(path, F):
    body, h1, h2, small = _styles()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title="Cambio analizzatore glicemia", author=P.ORG, creator=P.ORG,
                            subject="Nota ai reparti e all'Ufficio POCT", invariant=1)
    s = [Paragraph(P.ORG + ", " + P.LAB, small), Spacer(1, 2 * mm),
         Paragraph("Glicemia: dal 13 settembre 2027 il " + P.ANALYZER_B + " sostituisce il " + P.ANALYZER_A, h1),
         Paragraph("Nota del 7 settembre 2027 ai direttori e ai coordinatori dei reparti e all'Ufficio POCT. Firma: " +
                   P.PEOPLE["director"] + ", direttore della SC.", small), Spacer(1, 3 * mm),
         Paragraph("Dal 13 settembre 2027 la glicemia su plasma è eseguita sull'analizzatore " + P.ANALYZER_B +
                   ", che sostituisce il " + P.ANALYZER_A + " in servizio fino al 12 settembre. Dal 30 agosto al "
                   "10 settembre 312 campioni di routine sono stati analizzati su entrambi gli analizzatori.", body),
         Paragraph("Sul confronto il " + P.ANALYZER_A + " dà risultati più alti del " + P.ANALYZER_B + " del 3,5 "
                   "per cento, in proporzione al valore, a ogni concentrazione. I risultati refertati prima del 13 "
                   "settembre non sono stati ricalcolati. Chi confronta risultati anteriori al 13 settembre con "
                   "risultati successivi, o con il metodo in uso, divida i valori del " + P.ANALYZER_A + " per "
                   "1,035.", body),
         Paragraph("Gli intervalli di riferimento e i valori critici non cambiano.", body)]
    foot = _footer("SC Medicina di Laboratorio, nota 2027/41")
    doc.build(s, onFirstPage=foot, onLaterPages=foot)


def service_report(path, F, svc):
    body, h1, h2, small = _styles()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title="Rapporto di intervento", author=P.VENDOR,
                            creator=P.VENDOR, subject="Visita annuale di taratura 2027", invariant=1)
    s = [Paragraph(P.VENDOR + ", assistenza tecnica", small), Spacer(1, 2 * mm),
         Paragraph("Rapporto di intervento: visita annuale di taratura dei glucometri " + P.METER, h1),
         Paragraph("Cliente: " + P.ORG + ". Visita dal 18 al 22 gennaio 2027, contratto di assistenza 2025-2028. "
                   "Tecnico: " + P.PEOPLE["vendor"] + ".", small), Spacer(1, 3 * mm),
         Paragraph("Su ciascun glucometro: aggiornamento del firmware alla versione 3.6.1, taratura del canale di "
                   "misura sul sangue con il kit di taratura del fornitore, verifica con le soluzioni di controllo "
                   "di livello 1 e 2. Tutti i glucometri elencati sono stati tarati e riconsegnati al reparto lo "
                   "stesso giorno.", body), Spacer(1, 2 * mm)]
    rows = [["Matricola", "Inventario", "Presidio", "Reparto", "Data", "Esito"]]
    for r in svc.itertuples(index=False):
        rows.append([r.matricola, r.inventario, r.presidio.replace("Presidio di ", ""), r.reparto,
                     r.data.strftime("%d/%m/%Y"), "tarato"])
    s.append(_table(rows, [26, 24, 30, 22, 24, 20], size=8.0))
    s.append(Spacer(1, 4 * mm))
    s.append(Paragraph("Firmato: " + P.PEOPLE["vendor"] + " (" + P.VENDOR + "); per il cliente: " +
                       P.PEOPLE["poct"] + ", Ufficio POCT.", small))
    foot = _footer(P.VENDOR + ", rapporto 2027-0118")
    doc.build(s, onFirstPage=foot, onLaterPages=foot)


def vendor_mail(path, F):
    txt = """From: {v} <a.gori@corvenzamedical.it>
To: {p} <lorenzo.carfagna@asst-pianuraorientale.it>
Cc: Ufficio POCT <poct@asst-pianuraorientale.it>
Subject: Visita annuale di taratura glucometri, gennaio 2028
Date: Tue, 04 Jan 2028 10:41:09 +0100
Message-ID: <20280104104109.2291@corvenzamedical.it>
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 8bit

Gentile dott. Carfagna,

le confermo la visita annuale di taratura prevista dal contratto di assistenza
dal 17 al 21 gennaio 2028, nei tre presidi.

Come lo scorso anno ritariamo in laboratorio i glucometri che ci indicherete e li
riconsegniamo in reparto entro la giornata. Per organizzare i turni ci serve
l'elenco dei glucometri da ritarare, con matricola e reparto, entro lunedì 10
gennaio. Se l'elenco fosse vuoto ce lo scriva comunque, così liberiamo i giorni.

Cordiali saluti

Adelmo Gori
Responsabile assistenza tecnica
{vendor}
""".format(v=P.PEOPLE["vendor"], p=P.PEOPLE["poct"], vendor=P.VENDOR)
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(txt)


def dictionary(path, F):
    md = f"""# Dizionario dei dati POCT glicemia

{P.ORG}, {P.POCT_OFFICE}. Aggiornato al 3 gennaio 2028.

## {F['export']}

Risultati ricevuti dal gestionale {P.DMS} dal 1° luglio 2026 al 31 dicembre 2027, nell'ordine in cui il server li ha
ricevuti. Una riga per risultato ricevuto. Separatore punto e virgola.

| campo | contenuto |
|---|---|
| id_risultato | identificativo assegnato dal server alla ricezione |
| matricola | matricola del glucometro |
| n_memoria | numero progressivo del risultato nella memoria del glucometro |
| data_ora_test | data e ora del test, orologio del glucometro |
| tipo | PAZIENTE oppure CONTROLLO (soluzione di controllo) |
| livello | livello della soluzione di controllo, 1 o 2 |
| lotto_controllo, lotto_strisce | lotti della soluzione di controllo e delle strisce |
| id_paziente | codice del ricovero o dell'accesso in pronto soccorso |
| operatore | matricola dell'operatore |
| risultato | glicemia in mg/dL; LO sotto 20, HI sopra 600 |
| presidio, reparto | presidio e reparto a cui il glucometro è assegnato nell'anagrafica del gestionale |
| data_ora_ricezione | istante in cui il server ha ricevuto il risultato, UTC |

## {F['pairs']}

Abbinamenti fra glucometro e laboratorio dal 1° luglio 2026 al 31 dicembre 2027, foglio Abbinamenti. Una riga per
provetta abbinata.

| campo | contenuto |
|---|---|
| id_risultato | identificativo del risultato del glucometro (vedi sopra) |
| matricola | matricola del glucometro |
| data_ora_test | data e ora del test, orologio del glucometro |
| glucometro_mg_dl | risultato del glucometro; LO sotto 20, HI sopra 600 |
| n_accettazione | numero di accettazione della provetta in laboratorio |
| data_ora_prelievo | data e ora del prelievo registrate dal laboratorio, ora italiana |
| laboratorio_mg_dl | glicemia su plasma del laboratorio |
| presidio, reparto | come sopra |

## {F['plan']}

Piano degli abbinamenti, foglio Piano: per ogni glucometro i giorni della settimana del piano e il periodo in cui
valgono. Foglio Festività: le festività del periodo.

## {F['register']}

Anagrafica dei glucometri: foglio Glucometri (matricola, inventario, modello, presidio e reparto di assegnazione,
data di entrata in uso, stato) e foglio Storico ubicazioni (per ogni glucometro i reparti in cui è stato e da
quando).

## {F['strips']}

Confezioni di strisce consegnate dalla farmacia ai reparti nel 2027, per mese.

## {F['veq']}

Valutazione esterna di qualità della glicemia del laboratorio nel 2027: valore assegnato, risultato e z-score di
ogni giro.
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
