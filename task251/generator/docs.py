"""task251 documents: the agency's quality manual for the NOx network (pdf), the laboratory's mail confirming the
January bench (eml), the data dictionary (md). Italian throughout, as the agency writes."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import params as P


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


def manual(path, F):
    body, h1, h2, small = _styles()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title="Manuale della qualità, rete NOx", author=P.ORG,
                            creator=P.ORG, subject="AQBP-QA-07 rev. 4", invariant=1)
    s = [Paragraph(P.ORG + ", servizio strumentazione", small), Spacer(1, 2 * mm),
         Paragraph("Manuale della qualità della rete NOx: verifica e sostituzione dei convertitori, dati orari e "
                   "statistiche annuali", h1),
         Paragraph("AQBP-QA-07, revisione 4 del 24 giugno 2026, in vigore dal 1° luglio 2026. Sostituisce la "
                   "revisione 3 del 12 novembre 2024.", small),
         Spacer(1, 3 * mm)]
    sec = [
        ("1. Scopo", [
            "Il manuale stabilisce come l'Agenzia verifica e mantiene gli analizzatori di ossidi di azoto della "
            "propria rete, come si forma il dato orario di ogni stazione e come se ne calcolano le statistiche "
            "annuali. Si applica alle sedici stazioni della rete e all'analizzatore di scorta tenuto in magazzino."]),
        ("2. Gli analizzatori", [
            "Ogni stazione ospita un analizzatore a chemiluminescenza (modelli NX4210 e CL62). L'analizzatore misura "
            "l'NO direttamente e gli NOx dopo il passaggio del campione in un convertitore al molibdeno riscaldato a "
            "circa 320 °C, che riduce l'NO2 a NO; l'NO2 è la differenza fra NOx e NO. Un convertitore che non "
            "riduce più tutto l'NO2 che riceve fa leggere alla stazione meno NO2 di quanto ce ne sia nell'aria.",
            "Quando l'analizzatore di una stazione va in officina per una riparazione, al suo posto è installato "
            "l'analizzatore di scorta fino al rientro; l'installazione e il rientro sono annotati nel registro degli "
            "interventi."]),
        ("3. La verifica del convertitore", [
            "Il rendimento del convertitore è verificato ogni trimestre dalla ditta di taratura con la titolazione in "
            "fase gassosa della UNI EN 14211: a una miscela di NO a concentrazione nota si aggiunge ozono, e l'NO2 "
            "che la reazione genera (la diminuzione di NO) è confrontato con l'aumento di NO2 letto "
            "dall'analizzatore. Il rendimento è il rapporto fra l'NO2 letto e l'NO2 generato. Un convertitore con "
            "rendimento inferiore al 95 per cento è esaurito. La titolazione è ripetuta prima e dopo ogni "
            "sostituzione del convertitore.",
            "Fino al 30 giugno 2026 le verifiche sono state eseguite da " + P.CONTRACTOR_A + ", dal 1° luglio "
            "2026 da " + P.CONTRACTOR_B + "; ciascuna ditta consegna le proprie schede nel proprio formato."]),
        ("4. La sostituzione del convertitore", [
            "Il convertitore di ogni analizzatore è sostituito alla manutenzione programmata annuale, alla data "
            "fissata nel piano di manutenzione. Quando una titolazione trova un rendimento inferiore al 95 per cento, "
            "il convertitore è sostituito entro dieci giorni, senza attendere la manutenzione programmata. Le ore "
            "misurate prima della sostituzione restano nel dato della stazione come sono state validate."]),
        ("5. Il dato orario", [
            "L'analizzatore conserva nella propria memoria le medie orarie di NO, NO2 e NOx in ppb, con l'orologio "
            "dello strumento in UTC; la ditta di taratura le scarica a ogni visita trimestrale e a fine anno e le "
            "accoda all'archivio degli analizzatori.",
            "La banca dati della rete riceve dal registratore di stazione il dato orario di NO2 in microgrammi per "
            "metro cubo a 20 °C e 101,3 kPa (1 ppb di NO2 corrisponde a 1,91 µg/m³), in ora solare, "
            "con il codice di validazione. Un'ora è valida quando l'analizzatore ha misurato l'aria della stazione "
            "per almeno 45 minuti dell'ora."]),
        ("6. Le statistiche annuali", [
            "Per ogni stazione e anno civile l'Agenzia calcola le ore valide, la media annua di NO2 sulle ore valide "
            "e il 19° valore orario valido più alto, che si confronta con il valore limite orario di 200 "
            "µg/m³ da non superare più di 18 volte nell'anno civile."]),
        ("7. Il banco convertitori di gennaio", [
            "Ogni gennaio il " + P.LAB + " apre un banco per i convertitori delle reti della regione: i suoi tecnici "
            "sostituiscono in stazione, nella settimana del banco, i convertitori che ciascuna rete ha prenotato. "
            "L'Agenzia vi prenota gli analizzatori di stazione il cui convertitore, se restasse in servizio, "
            "sarebbe sotto il 95 per cento prima della manutenzione programmata dell'analizzatore nell'anno, "
            "così che nessuna ora dell'inverno e della primavera sia misurata attraverso un convertitore esaurito. "
            "La manutenzione programmata resta alla sua data."]),
        ("8. I registri", [
            "Archivio degli analizzatori (" + F["archive"] + "); schede di titolazione (" + F["titr_a"] + ", " +
            F["titr_b"] + "); registro degli interventi (" + F["service"] + "); piano di manutenzione (" +
            F["plan"] + "); anagrafica delle stazioni (" + F["stations"] + "); banca dati validata (" +
            F["database"] + ")."]),
    ]
    for head, paras in sec:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))
    s.append(Spacer(1, 4 * mm))
    t = Table([["Revisione", "Data", "Modifica"],
               ["3", "12/11/2024", "Revisione generale della rete, nuovi convertitori (dicembre 2024)"],
               ["4", "24/06/2026", "Nuova ditta di taratura dal 1° luglio 2026"]],
              colWidths=[22 * mm, 24 * mm, 124 * mm])
    t.setStyle(TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica", 8.2),
                           ("FONT", (0, 0), (-1, 0), "Helvetica-Bold", 8.2),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    s.append(t)
    foot = _footer("AQBP-QA-07 rev. 4")
    doc.build(s, onFirstPage=foot, onLaterPages=foot)


def lab_mail(path, F):
    txt = """From: {lab_who} <p.gilardoni@labtaratura-ambiente.it>
To: {head} <l.saracino@{dom}>
Cc: Ufficio rete <rete@{dom}>
Subject: Banco convertitori NOx, gennaio 2028
Date: Tue, 04 Jan 2028 09:12:31 +0100
Message-ID: <20280104091231.4417@labtaratura-ambiente.it>
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 8bit

Gentile dott.ssa Saracino,

le confermo il banco convertitori NOx per la vostra rete dal 17 al 21 gennaio:
i nostri tecnici passeranno nelle stazioni che ci indicherete e sostituiranno il
convertitore sul posto, con la titolazione prima e dopo la sostituzione.

Ci serve la lista degli analizzatori da prenotare, con stazione e matricola,
entro lunedì 10 gennaio, per organizzare i giri. Quest'anno possiamo prendere
fino a dieci convertitori della vostra rete.

Cordiali saluti

Patrizio Gilardoni
{lab_role}
{lab}
""".format(lab_who=P.LAB_CONTACT[0], lab_role=P.LAB_CONTACT[1][0].upper() + P.LAB_CONTACT[1][1:], lab=P.LAB,
           head=P.HEAD[0], dom=P.DOMAIN)
    with open(path, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(txt)


def dictionary(path, F):
    md = f"""# Dizionario dei dati della rete NOx

{P.ORG}, servizio strumentazione. Aggiornato al 3 gennaio 2028.

## {F['archive']}

Archivio degli analizzatori: le medie orarie che ogni analizzatore conserva nella propria memoria, scaricate dalla
ditta di taratura a ogni visita trimestrale e a fine anno, e accodate all'archivio. Una riga per analizzatore e ora.

| campo | contenuto |
|---|---|
| matricola | matricola dell'analizzatore |
| data_ora_utc | inizio dell'ora, orologio dello strumento (UTC) |
| no_ppb, no2_ppb, nox_ppb | medie orarie in ppb; vuote quando lo strumento era in guasto |
| stato | 0 misura, 2 strumento in modo taratura o manutenzione, 8 guasto |

## {F['titr_a']}

Schede di titolazione di {P.CONTRACTOR_A}, gennaio 2025 - giugno 2026, foglio Titolazioni.

| campo | contenuto |
|---|---|
| Data, Ora inizio, Ora fine | giorno, inizio e fine della verifica, ora italiana |
| Stazione | nome della stazione |
| Matricola | matricola dell'analizzatore |
| Tipo verifica | trimestrale, pre-sostituzione, post-sostituzione |
| NO2 generato (ppb), NO2 misurato (ppb) | NO2 generato dalla titolazione e aumento di NO2 letto dall'analizzatore |
| Rendimento convertitore (%) | NO2 misurato su NO2 generato |
| Esito | conforme, NON CONFORME (sotto il 95 %) |

## {F['titr_b']}

Schede di titolazione di {P.CONTRACTOR_B}, da luglio 2026.

| campo | contenuto |
|---|---|
| data, ora_inizio, ora_fine | giorno, inizio e fine della verifica, ora italiana |
| codice_stazione, matricola | stazione e analizzatore |
| tipo_verifica | trimestrale, pre-sostituzione, post-sostituzione |
| no_iniziale_ppb, nox_iniziale_ppb | letture dell'analizzatore sulla miscela di NO, prima dell'ozono |
| no_finale_ppb, nox_finale_ppb | letture dopo l'aggiunta dell'ozono |
| efficienza | rendimento del convertitore, come frazione |

## {F['service']}

Registro degli interventi, foglio Interventi: data, stazione (MAG per il magazzino), matricola dell'analizzatore,
intervento, tecnico.

## {F['plan']}

Piano di manutenzione 2028, foglio Piano: per ogni analizzatore la data della manutenzione programmata del 2028.

## {F['stations']}

Anagrafica delle stazioni, foglio Stazioni: codice, nome, tipo, coordinate, analizzatore di NOx in stazione al 31
dicembre 2027, modello, registratore dati e data della sua installazione.

## {F['database']}

Banca dati validata della rete, NO2 orario del 2027. Separatore punto e virgola, virgola decimale.

| campo | contenuto |
|---|---|
| stazione | codice della stazione |
| data_ora_solare | inizio dell'ora, ora solare (UTC+1) |
| no2_ugm3 | NO2 in µg/m³ a 20 °C e 101,3 kPa |
| codice | V valido; R valido, rivalidato dall'operatore dopo il controllo automatico; N misura per meno di 45 minuti; M strumento in taratura o manutenzione; A anomalia strumentale; F dato non pervenuto |

## {F['met']}

Dati meteorologici orari 2027 di tre stazioni della rete: temperatura, umidità relativa, velocità e direzione del
vento, altezza dello strato di rimescolamento stimata dal preprocessore meteorologico. Ora solare.

## {F['pm10']}

PM10 giornaliero gravimetrico 2027 delle sei stazioni con campionatore sequenziale, in µg/m³.
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(md)
