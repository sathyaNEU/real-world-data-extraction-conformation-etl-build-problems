"""Filed documents: the programme order, the return guidance, the portal notice, the register, the
exchange note, the bulletins, the 2026 annex, Celestina Gallart's note and the file index."""
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from plan import SECTIONS

OBS = "Observatori del Parc Residencial"
DG = "Direcció General d'Habitatge"
DIST_NAME = {"4625001": "Ciutat Vella", "4625002": "l'Eixample", "4625005": "la Saïdia",
             "4625011": "Poblats Marítims", "4625012": "Camins al Grau", "4625013": "Algirós",
             "0301401": "districte 1", "0301402": "districte 2", "0301405": "districte 5",
             "1204001": "districte 1", "1204003": "districte 3"}
MUNI_NAME = {"46250": "València", "03014": "Alacant", "12040": "Castelló de la Plana"}


def where(code):
    return MUNI_NAME[code[:5]], DIST_NAME[code[:7]]


def parts(code):
    """A section as the printed lists carry it: municipality, district name, INE municipality code, district, section."""
    return [MUNI_NAME[code[:5]], DIST_NAME[code[:7]], code[:5], code[5:7], code[7:]]


PARTS_HEAD = ["Municipi", "Districte", "Codi INE", "Dte.", "Secció"]
CODE_NOTE = ("El codi de secció censal de 10 xifres que fan servir el Cadastre i el padró encadena el codi INE "
             "del municipi, el districte i la secció.")


def _styles():
    ss = getSampleStyleSheet()
    base = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=12.5,
                          alignment=TA_LEFT, spaceAfter=5)
    return {"b": base,
            "h1": ParagraphStyle("h1", parent=base, fontName="Helvetica-Bold", fontSize=12.5, leading=15, spaceAfter=8),
            "h2": ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold", fontSize=10, leading=13, spaceBefore=6),
            "small": ParagraphStyle("s", parent=base, fontSize=8, leading=10, textColor=colors.HexColor("#444444")),
            "cell": ParagraphStyle("c", parent=base, fontSize=8, leading=9.5, spaceAfter=0)}


def pdf(path, title, author, blocks, subject=""):
    st = _styles()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=22 * mm, rightMargin=22 * mm, topMargin=18 * mm,
                            bottomMargin=18 * mm, title=title, author=author, subject=subject, creator=author,
                            invariant=1)
    story = []
    for kind, val in blocks:
        if kind == "sp":
            story.append(Spacer(1, val))
        elif kind == "table":
            rows, widths = val
            data = [[Paragraph(str(c), st["cell"]) for c in r] for r in rows]
            t = Table(data, colWidths=[w * mm for w in widths], repeatRows=1)
            t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#999999")),
                                   ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E4E8EC")),
                                   ("VALIGN", (0, 0), (-1, -1), "TOP")]))
            story.append(t)
            story.append(Spacer(1, 6))
        else:
            story.append(Paragraph(val, st[kind]))
    doc.build(story)


def order_pdf(path):
    sec_rows = [PARTS_HEAD]
    for s in sorted(SECTIONS, key=lambda x: x["code"]):
        sec_rows.append(parts(s["code"]))
    b = [("small", f"{DG}. Text consolidat a 3 de setembre de 2025"),
         ("h1", "Ordre per la qual es regula la designació anual de seccions censals amb concentració "
                "d'habitatges en mans de grans tenidors"),
         ("b", "La concentració de la propietat residencial en determinades seccions censals condiciona l'accés a "
               "l'habitatge en lloguer. Esta ordre establix com es designen cada any, d'entre les seccions de la "
               "llista de seguiment, aquelles en què els grans tenidors concentren una part substancial del parc. "
               "La designació determina les actuacions del programa durant l'any: les visites prioritàries de la "
               "inspecció d'habitatge, la notificació als grups titulars i les comunicacions sobre habitatges buits."),
         ("h2", "Article 1. Objecte"),
         ("b", "Esta ordre regula la designació anual de seccions censals amb concentració d'habitatges en mans de "
               "grans tenidors i el contingut de l'annex que l'acompanya."),
         ("h2", "Article 2. Definicions"),
         ("b", "1. Gran tenidor: la persona física o jurídica, o el grup de societats vinculades, titular de deu o més "
               "habitatges situats en la Comunitat Valenciana, inscrita en el Registre de Grans Tenidors. Les "
               "administracions públiques i les entitats del sector públic no tenen la consideració de gran tenidor."),
         ("b", "2. Grup de societats vinculades: el conjunt de declarants vinculats a un mateix codi de grup en el "
               "Registre de Grans Tenidors."),
         ("b", "3. Habitatge: la unitat cadastral d'ús residencial. El nombre d'habitatges d'una secció és el que hi "
               "consta en el Cadastre."),
         ("b", "4. Titularitat en una data: un habitatge pertany en una data al titular que n'és propietari en virtut "
               "de les escriptures atorgades fins a eixa data, inclosa."),
         ("h2", "Article 3. Llista de seguiment"),
         ("b", "Formen la llista de seguiment les seccions censals que figuren en l'annex d'esta ordre."),
         ("h2", "Article 4. Designació"),
         ("b", "Queden designades per a un any de programa les seccions de la llista de seguiment en què els grans "
               "tenidors són titulars del 25 per cent o més dels habitatges el dia 1 de gener d'eixe any."),
         ("h2", "Article 5. Annex de designació"),
         ("b", "L'ordre de designació de cada any va acompanyada d'un annex amb una fila per a cada secció de la llista "
               "de seguiment, que recull: a) els habitatges de què són titulars els grans tenidors el dia 1 de gener i "
               "el percentatge que representen sobre els habitatges de la secció, amb un decimal; b) el grup o titular "
               "gran tenidor amb més habitatges en la secció, amb el nom que consta en el Registre de Grans Tenidors, i "
               "el nombre d'habitatges que en té; c) el nombre d'habitatges de grans tenidors en què no hi ha cap "
               "persona empadronada segons l'últim lliurament del padró municipal."),
         ("h2", "Article 6. Procediment"),
         ("b", f"L'{OBS} elabora la proposta de designació i l'annex i els tramet a la persona titular de la "
               "direcció general competent en matèria d'habitatge abans del 15 de novembre de l'any anterior al de "
               "programa. L'ordre de designació es publica abans de l'1 de gener."),
         ("h2", "Disposició addicional única"),
         ("b", "La primera designació correspon a l'any de programa 2026."),
         ("h2", "Annex. Llista de seguiment"),
         ("table", (sec_rows, [40, 40, 22, 14, 18])),
         ("small", CODE_NOTE)]
    pdf(path, "Ordre de designació de seccions censals amb concentració de grans tenidors", DG, b)


GUIDE_FIELDS = [
    ("id_declaracio", "Identificador de la declaració assignat pel portal."),
    ("nif_declarant / nom_declarant", "NIF i nom del titular inscrit en el Registre de Grans Tenidors."),
    ("trimestre", "Trimestre declarat (AAAAT1 a AAAAT4). La data de referència és l'últim dia del trimestre."),
    ("tipus_declaracio", "O, original; C, complementària; S, substitutiva (apartat 5)."),
    ("declaracio_referida", "En les declaracions C i S, identificador de la declaració que complementen o substituïxen."),
    ("data_presentacio", "Data en què el portal registra la declaració."),
    ("codi_grup", "Codi del grup de societats vinculades al qual pertany el declarant en la data de presentació; "
                  "en blanc si no en pertany a cap."),
    ("referencia_cadastral / unitats", "Immoble declarat (apartat 6)."),
    ("codi_tinenca", "PD, ple domini del declarant; OP, opció de compra a favor del declarant; RS, reserva o arres a "
                     "favor del declarant. Les línies OP i RS no corresponen a habitatges de titularitat del declarant."),
    ("data_transmissio_prevista", "En els habitatges amb contracte de compravenda signat i escriptura pendent en la "
                                  "data de referència, data d'atorgament prevista en el contracte."),
    ("nif_adquirent_previst / preu_convingut", "NIF del comprador i preu fixats en el contracte, en euros."),
]


def guide_pdf(path):
    rows = [["Camp", "Contingut"]] + [[a, b] for a, b in GUIDE_FIELDS]
    b = [("small", f"{OBS}. Servei de Declaracions"),
         ("h1", "Declaració trimestral d'habitatges de grans tenidors. Guia de presentació (versió 3, gener de 2024)"),
         ("h2", "1. Qui ha de declarar"),
         ("b", "Cada titular inscrit en el Registre de Grans Tenidors, identificat pel seu NIF. Les societats d'un grup "
               "declaren cadascuna els seus habitatges."),
         ("h2", "2. Què es declara"),
         ("b", "Els habitatges de què és titular el declarant l'últim dia del trimestre i les opcions de compra i "
               "reserves a favor seu en eixa data."),
         ("h2", "3. Termini"),
         ("b", "Dins dels 30 dies naturals següents a la fi del trimestre."),
         ("h2", "4. Declaracions sense variacions"),
         ("b", "El declarant la declaració del qual tindria el mateix contingut que l'última que ha presentat no està "
               "obligat a presentar-ne una de nova. L'última declaració presentada manté la vigència per als "
               "trimestres següents."),
         ("h2", "5. Tipus de declaració"),
         ("b", "O, original: la primera declaració del trimestre. C, complementària: afig les línies que s'han omés en "
               "la declaració a què es referix, sense repetir-ne cap. S, substitutiva: substituïx íntegrament la "
               "declaració a què es referix. Una declaració C o S pot presentar-se en qualsevol moment posterior a "
               "l'original."),
         ("h2", "6. Referència cadastral i unitats"),
         ("b", "Cada línia declara una parcel·la cadastral (referència de 14 posicions). En el camp unitats s'indiquen "
               "els càrrecs cadastrals declarats dins de la parcel·la, separats per comes o en intervals (per exemple, "
               "0001-0006,0009). Les unitats amb una tinença diferent o amb una compravenda pendent es declaren en "
               "línies separades."),
         ("h2", "7. Camps del fitxer de declaració"),
         ("table", (rows, [48, 118])),
         ("small", "Consultes: declaracions.gt@oprcv.internal")]
    pdf(path, "Guia de la declaració trimestral de grans tenidors v3", OBS, b)


def notice_eml():
    return """Return-Path: <declaracions.gt@oprcv.internal>
Message-ID: <20260316094512.4F2A1C0@oprcv.internal>
Date: Mon, 16 Mar 2026 09:45:12 +0100
From: Servei de Declaracions de Grans Tenidors <declaracions.gt@oprcv.internal>
To: declarants-gt@llistes.oprcv.internal
Cc: Jose Nevado <j.nevado@oprcv.internal>
Subject: Canvi de format de les declaracions trimestrals a partir de l'1 d'abril de 2026
MIME-Version: 1.0
Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 8bit

Benvolguts declarants,

A partir de l'1 d'abril de 2026 el portal de declaracions de grans tenidors recull una
línia per habitatge. Cada línia porta la referència cadastral completa de 20 posicions
(parcel·la, càrrec i caràcters de control) i el camp unitats queda en blanc.

Les declaracions presentades fins al 31 de març de 2026 conserven el format de la guia
(versió 3): una línia per parcel·la, amb la referència de 14 posicions i, en el camp
unitats, els càrrecs declarats. El canvi s'aplica per data de presentació, siga quin
siga el trimestre declarat; per tant, la declaració del primer trimestre de 2026 i
qualsevol complementària o substitutiva que presenteu des de l'1 d'abril, encara que es
referisca a un trimestre anterior, ja s'ha de fer amb una línia per habitatge.

La resta de camps i els codis de tinença no canvien. El 30 de març el portal estarà
tancat de 8.00 a 14.00 per a la posada en marxa.

Per a qualsevol dubte, responeu a este correu o telefoneu al 961 000 418.

Jose Nevado
Servei de Declaracions
Observatori del Parc Residencial
"""


EXCHANGE_NOTE = """OBSERVATORI DEL PARC RESIDENCIAL
Intercanvi de dades del padró municipal (seccions de la llista de seguiment)
Nota de protocol, revisió 2 (10 de març de 2025)

1. Abast
   Els ajuntaments de València, Alacant i Castelló de la Plana lliuren a l'Observatori,
   cada trimestre, les inscripcions padronals dels habitatges situats en les seccions
   censals de la llista de seguiment del programa de grans tenidors.

2. Calendari
   Els lliuraments es fan en març, juny, setembre i desembre. La data de referència de
   cada lliurament és el dia 1 del mes en què es fa.

3. Substitució
   Cada lliurament substituïx l'anterior per als districtes que conté.

4. Format (CSV, UTF-8, separador coma)
   codi_municipi          codi INE del municipi
   districte              districte municipal (dues xifres)
   seccio_censal          codi de secció de 10 xifres
   referencia_cadastral   referència cadastral de 20 posicions de l'habitatge
   id_inscripcio          identificador seudonimitzat de la inscripció
   tipus_document         DNI, NIE, TIE-P (residència permanent), TIE-T (residència
                          temporal) o PAS (passaport)
   nacionalitat           codi ISO 3166-1 alfa-3
   data_alta              data d'alta en l'habitatge
   data_ultima_renovacio  última renovació de la inscripció, si n'hi ha
   persones               persones inscrites en l'habitatge, quan el lliurament es fa
                          per habitatge

   València i Alacant lliuren una fila per persona inscrita (persones en blanc).
   Castelló de la Plana lliura una fila per habitatge de la secció, inclosos els que no
   tenen cap persona inscrita (id_inscripcio, tipus_document, nacionalitat i dates en
   blanc).

5. Renovació de les inscripcions
   Les inscripcions de persones estrangeres no comunitàries sense autorització de
   residència permanent (tipus de document TIE-T o PAS) s'han de renovar cada dos anys,
   comptats des de l'alta o des de l'última renovació. La inscripció no renovada dins del
   termini caduca, encara que continue en els lliuraments fins que l'ajuntament en
   tramita la baixa.

6. Contactes
   València: Flor Segarra, Servei d'Estadística
   Alacant: Rosaura Rodrigo, Estadística i Padró
   Castelló de la Plana: Negociat de Població

Les dades són personals i seudonimitzades. Ús restringit a les finalitats del programa.
"""


def note_docx(path):
    from docx import Document
    from docx.shared import Pt
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    doc.add_paragraph("Notes sobre l'annex de 2026").runs[0].bold = True
    doc.add_paragraph("Celestina Gallart, 24 de setembre de 2026")
    paras = [
        "Aurora, et deixe ací com vaig muntar l'annex de 2026, per si et servix per a la proposta de 2027.",
        "Vaig partir de les declaracions del segon trimestre de 2025, amb tot el que s'havia presentat fins al 31 "
        "d'agost. Les substitutives en lloc de l'original, les complementàries sumades a l'original, i els "
        "declarants que no havien presentat el trimestre amb l'última declaració que tenien vigent. Les línies per "
        "parcel·la, desplegades amb el Cadastre; fora les opcions i les reserves; i les referències mal escrites, "
        "quadrades amb el Cadastre una a una.",
        "Per a passar del 30 de juny a l'1 de gener vaig aplicar les escriptures inscrites fins al 30 de setembre i, "
        "per a la resta de l'any, les compravendes pendents que porten les declaracions, en la data i al comprador "
        "que hi consten. Abans de fer-ho vaig comprovar contra el registre totes les compravendes declarades amb data "
        "anterior al 30 de setembre, i totes s'havien escripturat el dia previst i al comprador previst. Ni una "
        "desviació.",
        "El grup amb més habitatges de cada secció el vaig traure del codi de grup que porten les declaracions, i "
        "els habitatges sense ningú empadronat, del lliurament de setembre del padró.",
        "Per a 2027 no hi veig res a canviar. L'única novetat és que des d'abril el portal ja dona una línia per "
        "habitatge, i això ens estalvia desplegar parcel·les.",
        "Si vols, en parlem dijous abans de la reunió amb Amaro.",
    ]
    for p in paras:
        doc.add_paragraph(p)
    doc.save(path)


def fmt1(x):
    return f"{x:.1f}".replace(".", ",")


def bulletin_pdf(path, title_q, ref_text, cutoff_text, rows, prev_label, issue):
    """rows: list of (code, N, lh, share1, delta1 or None) with share1 and delta1 Decimals rounded to one decimal."""
    tab = [PARTS_HEAD + ["Habitatges", f"Habitatges de grans tenidors a {ref_text}",
                         "% sobre habitatges", f"Variació respecte a {prev_label} (punts)"]]
    tot_n = tot_lh = 0
    for code, N, lh, sh, dl in rows:
        tab.append(parts(code) + [f"{N:,}".replace(",", "."), f"{lh:,}".replace(",", "."), fmt1(sh),
                    ("+" if dl > 0 else "") + fmt1(dl) if dl is not None else "-"])
        tot_n += N
        tot_lh += lh
    b = [("small", f"{OBS}. Butlletí del Parc Residencial, núm. {issue}"),
         ("h1", f"Seccions de la llista de seguiment. {title_q}"),
         ("b", f"Tinença a {ref_text} segons les declaracions trimestrals de grans tenidors presentades fins al "
               f"{cutoff_text}, amb les declaracions complementàries i substitutives aplicades i el nombre "
               f"d'habitatges de cada secció segons el Cadastre. Les xifres descriuen la situació en la data de "
               f"referència del trimestre."),
         ("table", (tab, [20, 22, 13, 10, 14, 17, 25, 17, 28])),
         ("b", "Les catorze seccions de la llista sumen " + f"{tot_n:,}".replace(",", ".") + " habitatges segons el "
               "Cadastre."),
         ("small", "Font: declaracions trimestrals de grans tenidors; Cadastre. Elaboració: Observatori del Parc "
                   "Residencial. Les xifres poden revisar-se si es presenten declaracions posteriors. " + CODE_NOTE)]
    pdf(path, f"Butlletí del Parc Residencial {title_q}", OBS, b)


def annex_xlsx(path, rows):
    """rows: (code, N, lh, share1, designated, group_name, group_n, empty)."""
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment
    wb = Workbook()
    ws = wb.active
    ws.title = "Annex 2026"
    ws["A1"] = "Annex de l'ordre de designació per a l'any de programa 2026"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Situació a 1 de gener de 2026. Proposta de l'Observatori del Parc Residencial, 12 de novembre de 2025."
    head = ["Secció censal", "Municipi", "Districte", "Habitatges", "Habitatges de grans tenidors",
            "% grans tenidors", "Designada", "Grup o titular amb més habitatges", "Habitatges del grup o titular",
            "Habitatges de grans tenidors sense persones empadronades"]
    ws.append([])
    ws.append(head)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for code, N, lh, sh, des, gname, gn, empty in rows:
        m, d = where(code)
        ws.append([code, m, d, N, lh, float(sh), "Sí" if des else "No", gname, gn, empty])
        ws.cell(ws.max_row, 6).number_format = "0.0"
    for col, w in zip("ABCDEFGHIJ", [14, 20, 18, 11, 14, 10, 10, 32, 12, 18]):
        ws.column_dimensions[col].width = w
    ws.row_dimensions[4].height = 45
    wb.save(path)


REG_DICT = [
    ("Titulars", "nif", "NIF del titular inscrit."),
    ("Titulars", "nom", "Nom o raó social del titular, tal com consta en el Registre."),
    ("Titulars", "tipus_persona", "F, persona física; J, persona jurídica."),
    ("Titulars", "data_inscripcio", "Data d'inscripció en el Registre."),
    ("Titulars", "data_baixa", "Data de baixa en el Registre, si n'hi ha."),
    ("Vinculacions", "nif", "NIF del declarant vinculat."),
    ("Vinculacions", "codi_grup", "Codi del grup de societats vinculades (vegeu codis_grup.csv)."),
    ("Vinculacions", "data_efecte_inici", "Primer dia en què el declarant pertany al grup."),
    ("Vinculacions", "data_efecte_fi", "Últim dia en què el declarant pertany al grup; en blanc si la vinculació "
                                       "continua."),
    ("Vinculacions", "data_anotacio", "Data en què la vinculació, o el seu canvi, s'anota en el Registre. Pot ser "
                                      "anterior a la data d'efecte."),
    ("Vinculacions", "(fitxa)", "La pertinença a un grup es registra per declarant, amb les dates d'efecte. Un "
                                "declarant pot tindre diverses vinculacions successives."),
    ("codis_grup.csv", "codi_grup", "Codi de grup. Els codis que queden lliures en dissoldre's un grup poden "
                                    "assignar-se a un grup nou."),
    ("codis_grup.csv", "nom_grup", "Nom del grup en el Registre."),
]


def register_xlsx(path, titulars, links, extract_day):
    from openpyxl import Workbook
    from openpyxl.styles import Font
    wb = Workbook()
    ws = wb.active
    ws.title = "Titulars"
    ws.append(["nif", "nom", "tipus_persona", "data_inscripcio", "data_baixa"])
    for r in titulars:
        ws.append(r)
    ws2 = wb.create_sheet("Vinculacions")
    ws2.append(["nif", "codi_grup", "data_efecte_inici", "data_efecte_fi", "data_anotacio"])
    for r in links:
        ws2.append(r)
    ws3 = wb.create_sheet("Diccionari")
    ws3.append([f"Registre de Grans Tenidors. Extracció de {extract_day}."])
    ws3.append([])
    ws3.append(["full", "camp", "descripció"])
    for r in REG_DICT:
        ws3.append(list(r))
    for w in (ws, ws2, ws3):
        for c in w[1]:
            c.font = Font(bold=True)
    ws.column_dimensions["B"].width = 38
    ws3.column_dimensions["C"].width = 90
    wb.save(path)
