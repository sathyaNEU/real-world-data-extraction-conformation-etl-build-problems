"""The pack's documents for task270: Gota Viva's campaign brief, Audimetria Lusa's methodology note and the sales
houses' second-quarter 2027 price lists (PDF), and the data dictionary (CSV)."""
from __future__ import annotations

import csv
import datetime as dt

from reportlab import rl_config

rl_config.invariant = 1
from reportlab.lib import colors                                                    # noqa: E402
from reportlab.lib.pagesizes import A4                                              # noqa: E402
from reportlab.lib.styles import ParagraphStyle                                     # noqa: E402
from reportlab.lib.units import cm                                                  # noqa: E402
from reportlab.pdfbase import pdfmetrics                                            # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont                                        # noqa: E402
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

import common as K   # noqa: E402

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
for nm, f in (("Sans", "LiberationSans-Regular"), ("Sans-B", "LiberationSans-Bold"), ("Sans-I", "LiberationSans-Italic")):
    pdfmetrics.registerFont(TTFont(nm, FONT_DIR + f + ".ttf"))
pdfmetrics.registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans-I", boldItalic="Sans-B")
INK, GREY, RULE = colors.HexColor("#1f2328"), colors.HexColor("#5b6470"), colors.HexColor("#c3c9d0")
RED = colors.HexColor("#a3132b")
NAVY = colors.HexColor("#1d3557")
TEAL = colors.HexColor("#00606b")
MONTHS = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro",
          "novembro", "dezembro"]
CAMPAIGN_END = K.CAMPAIGN_START + dt.timedelta(days=27)


def pt_date(d):
    return "%d de %s de %d" % (d.day, MONTHS[d.month - 1], d.year)


def low(s):
    return s[:1].lower() + s[1:]


def eur(x):
    return ("%s €" % format(int(x), ",")).replace(",", ".")


def styles(accent):
    body = ParagraphStyle("b", fontName="Sans", fontSize=9.6, leading=13.2, textColor=INK, spaceAfter=5)
    return dict(
        body=body,
        h1=ParagraphStyle("h1", fontName="Sans-B", fontSize=14.0, leading=17.5, textColor=accent, spaceAfter=2),
        h2=ParagraphStyle("h2", fontName="Sans-B", fontSize=10.4, leading=14, textColor=INK, spaceBefore=8,
                          spaceAfter=2, keepWithNext=1),
        meta=ParagraphStyle("m", fontName="Sans", fontSize=8.3, leading=11, textColor=GREY, spaceAfter=9),
        cell=ParagraphStyle("c", fontName="Sans", fontSize=7.9, leading=9.9, textColor=INK),
        cellb=ParagraphStyle("cb", fontName="Sans-B", fontSize=7.9, leading=9.9, textColor=INK),
        clause=ParagraphStyle("p", parent=body, leftIndent=26, firstLineIndent=-26),
        note=ParagraphStyle("n", fontName="Sans", fontSize=7.8, leading=10.2, textColor=GREY, spaceBefore=4))


def _frame(left, right):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFillColor(GREY)
        canvas.setFont("Sans", 7.3)
        canvas.drawString(2.0 * cm, A4[1] - 1.25 * cm, left)
        canvas.drawRightString(A4[0] - 2.0 * cm, A4[1] - 1.25 * cm, right)
        canvas.drawRightString(A4[0] - 2.0 * cm, 1.1 * cm, "%d" % doc.page)
        canvas.restoreState()
    return draw


def _table(S, rows, widths, right=()):
    data = [[Paragraph(str(c), S["cellb"] if i == 0 else S["cell"]) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * cm for w in widths], repeatRows=1, hAlign="LEFT")
    st = [("LINEBELOW", (0, 0), (-1, 0), .6, INK), ("LINEBELOW", (0, -1), (-1, -1), .4, RULE),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 1.6),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)]
    for c in right:
        st.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(st))
    return t


def _clause(S, num, text):
    return Paragraph("<b>%s</b>&nbsp;&nbsp;%s" % (num, text), S["clause"])


def _doc(path, title, author, subject):
    return SimpleDocTemplate(path, pagesize=A4, leftMargin=2.0 * cm, rightMargin=2.0 * cm, topMargin=2.0 * cm,
                             bottomMargin=1.8 * cm, title=title, author=author, subject=subject, creator=author,
                             producer=author)


def write_brief(path):
    S = styles(RED)
    doc = _doc(path, "Briefing: campanha de televisão para jovens dadores 2027", K.ORG, "Briefing de meios")
    st = [Paragraph("Campanha de televisão para jovens dadores, abril de 2027", S["h1"]),
          Paragraph("Briefing à %s &middot; %s, Marketing de Dadores &middot; %s &middot; ref. GV-MKT-2027-04" %
                    (K.AGENCY, K.REQUESTER, pt_date(K.BRIEF_DATE)), S["meta"]),
          Paragraph("1. Porque fazemos esta campanha", S["h2"]),
          Paragraph("Os dadores com menos de 35 anos foram 45 por cento das inscrições novas em 2025, mas só 31 por "
                    "cento das dádivas regulares. A campanha de abril de 2027 pede aos adultos dos 18 aos 34 anos que "
                    "marquem a primeira dádiva. Os nossos estudos de 2024 e 2025 mostram que um jovem que vê a "
                    "mensagem uma ou duas vezes raramente marca; a partir da terceira vez a marcação sobe de forma "
                    "clara, por isso o objetivo de meios é a cobertura com frequência de três ou mais.", S["body"]),
          Paragraph("2. O que pedimos à agência", S["h2"])]
    rows = [["Item", "Pedido"],
            ["Público", "Adultos dos 18 aos 34 anos (universo do painel de 2026)"],
            ["Período", "Quatro semanas, de segunda-feira %s a domingo %s" % (pt_date(K.CAMPAIGN_START),
                                                                             pt_date(CAMPAIGN_END))],
            ["Orçamento", "%s, preços das tabelas do 2.º trimestre de 2027, sem descontos de volume" % eur(K.BUDGET)],
            ["Filme", "Um filme de 30 segundos"],
            ["Esquemas", "Três esquemas alternativos ao mesmo orçamento, para decisão da Comissão Executiva"]]
    st.append(_table(S, rows, [3.2, 13.6]))
    st.append(Paragraph("3. Como vamos escolher", S["h2"]))
    st.append(_clause(S, "3.1", "Compramos o esquema que leva o filme a mais adultos dos 18 aos 34 anos três ou "
                                "mais vezes."))
    st.append(_clause(S, "3.2", "Cada esquema é lido como o painel o teria medido se tivesse ido para o ar nas quatro "
                                "semanas de referência de 2026, de 2 a 29 de março: a semana n da campanha é lida na "
                                "semana n de referência, cada spot no mesmo dia da semana do painel em que está "
                                "marcado."))
    st.append(_clause(S, "3.3", "Um membro do painel vê um spot quando está a ver o canal em direto durante pelo "
                                "menos metade dos segundos do lugar em que o spot passa, somados todos os seus "
                                "registos nesse canal, com o início e a duração que esse lugar teve na emissão de "
                                "referência. Contam os membros do painel com o seu peso de 28 dias; não contam "
                                "convidados nem visionamento diferido."))
    st.append(_clause(S, "3.4", "Cada spot é lido onde teria passado: um spot com lugar marcado, no seu lugar; um spot "
                                "cujo lugar fica com o canal, em cada lugar com a probabilidade de lá ter passado."))
    st.append(_clause(S, "3.5", "A cobertura é a parte do universo dos 18 aos 34 anos que se espera que veja o filme o "
                                "número de vezes indicado ou mais, com os spots tomados como independentes entre si."))
    st.append(Paragraph("4. Calendário", S["h2"]))
    st.append(Paragraph("A agência entrega os três esquemas até meados de novembro. A Comissão Executiva decide a %s; "
                        "as reservas de abril fecham nos canais a %s." % (pt_date(K.DECISION_DATE),
                                                                     pt_date(K.BOOKING_DEADLINE)), S["body"]))
    st.append(Spacer(1, 6))
    st.append(Paragraph("Contacto: %s, Marketing de Dadores, %s." % (K.REQUESTER, K.ORG), S["note"]))
    f = _frame(K.ORG, "Briefing de meios 2027")
    doc.build(st, onFirstPage=f, onLaterPages=f)


def write_method(path, n_members, n_homes):
    S = styles(NAVY)
    doc = _doc(path, "Painel de audiometria: nota metodológica para clientes", K.PANEL_CO, "Nota metodológica")
    st = [Paragraph("Painel de audiometria: nota metodológica para clientes", S["h1"]),
          Paragraph("%s &middot; para a %s &middot; edição de fevereiro de 2026 &middot; contacto: %s" %
                    (K.PANEL_CO, K.JIC, K.PANEL_CONTACT), S["meta"])]
    th = lambda n: format(n, ",").replace(",", ".")
    paras = [
        ("1. O painel", "O ficheiro de clientes de março de 2026 tem %s lares e %s indivíduos com 18 ou mais anos. "
                        "Cada televisor do lar tem um audímetro que identifica o canal por marca de áudio; cada "
                        "pessoa regista a presença no comando." % (th(n_homes), th(n_members))),
        ("2. Os registos de visionamento", "Cada linha do ficheiro de visionamentos é um período contínuo em que "
                                           "uma pessoa esteve presente diante de um canal. As horas estão em UTC. "
                                           "O dia de televisão vai das 02:00 às 26:00, hora legal de Portugal "
                                           "continental. O modo indica se o visionamento foi em direto ou "
                                           "diferido (gravações e televisão de recuperação vistas até sete dias "
                                           "depois da emissão, à velocidade normal; o avanço rápido não é "
                                           "registado). O início e o fim são as horas do visionamento; a hora de "
                                           "emissão identifica, pelo som, o que estava a ser visto."),
        ("3. Convidados", "As pessoas de fora do lar registam-se como convidados; aparecem com o código do lar "
                          "seguido de -C1 e não pertencem à amostra."),
        ("4. Pesos", "O peso de 28 dias é dado a quem esteve em amostra nos 28 dias do período e projeta a amostra "
                     "no universo de 2026 por escalão etário, sexo e região. Quem falhou algum dia tem peso zero no "
                     "período."),
        ("5. Canais", "Os códigos de canal seguem a lista de códigos em vigor em cada dia; um canal que muda de "
                      "nome muda também de código a partir da data indicada na lista."),
        ("6. Dados de publicidade", "Com o ficheiro de clientes seguem a emissão publicitária dos canais (cada spot "
                                    "emitido, com o seu lugar no intervalo) e as reservas das comerciais para os mesmos "
                                    "dias de televisão, com os anunciantes codificados."),
    ]
    for h, t in paras:
        st.append(Paragraph(h, S["h2"]))
        st.append(Paragraph(t, S["body"]))
    f = _frame(K.PANEL_CO, "Nota metodológica")
    doc.build(st, onFirstPage=f, onLaterPages=f)


def write_rates(path, rate, ros_rate, prog_window):
    S = styles(TEAL)
    doc = _doc(path, "Tabelas de preços de publicidade, 2.º trimestre de 2027", K.AGENCY, "Tabelas de preços")
    st = [Paragraph("Tabelas de preços de televisão, 2.º trimestre de 2027", S["h1"]),
          Paragraph("Compilação de %s a partir das tabelas publicadas pelas comerciais dos canais em %s; preços por "
                    "spot de 30 segundos, em euros, sem IVA e sem descontos de volume." %
                    (K.AGENCY, pt_date(K.RATES_ISSUED)), S["meta"]),
          Paragraph("Colocação", S["h2"]),
          Paragraph("Os preços abaixo são de spot fixo num intervalo de um programa. O primeiro lugar no intervalo "
                    "custa mais 15 por cento e o último lugar mais 10 por cento. A rotação é vendida por janela "
                    "horária, sem programa nem lugar garantidos.", S["body"])]
    order = {"day": 0, "access": 1, "prime": 2, "late": 3}
    for ch in ("VRT", "LIT", "PLS", "ARN", "FAR1"):
        st.append(Paragraph("%s (%s)" % (K.CH_NAME[ch] if ch != "PLS" else "Pulsar+", K.SALES[ch]), S["h2"]))
        rows = [["Programa", "Janela", "Spot fixo", "1.º lugar", "Último lugar"]]
        items = sorted([(t, v) for (c, t), v in rate.items() if c == ch],
                       key=lambda x: (order[prog_window[(ch, x[0])]], x[0]))
        for t, v in items:
            rows.append([t, low(K.WINDOW_NAME[prog_window[(ch, t)]]), eur(v), eur(K.r(v * 1.15)), eur(K.r(v * 1.10))])
        for w in ("day", "access", "prime", "late"):
            if (ch, w) in ros_rate:
                rows.append(["Rotação", low(K.WINDOW_NAME[w]), eur(ros_rate[(ch, w)]), "", ""])
        st.append(_table(S, rows, [5.4, 4.6, 2.2, 2.2, 2.4], right=(2, 3, 4)))
    f = _frame(K.AGENCY, "Tabelas 2T2027")
    doc.build(st, onFirstPage=f, onLaterPages=f)


def write_notes_2025(path):
    """the Portal do Dador team's notes that travel with the booking extract"""
    import side2025 as S
    lines = [
        "Portal do Dador: extração de marcações",
        "Associação Gota Viva, Sistemas de Informação",
        "Extraído a %s para a Marketing de Dadores (pedido de %s)" % (pt_date(S.EXTRACTED), K.REQUESTER),
        "",
        "Âmbito",
        "Todas as marcações para sessões de colheita de %s a %s nos doze centros do continente, qualquer que seja a"
        % (pt_date(S.SESSIONS[0]), pt_date(S.SESSIONS[1])),
        "data em que foram feitas e o seu desfecho. Uma linha por marcação.",
        "",
        "Sistema",
        "O Portal do Dador entrou em produção a %s. As marcações e os registos de dadores do sistema anterior foram"
        % pt_date(S.GO_LIVE),
        "importados com as suas datas e números.",
        "",
        "Campos",
        "id_marcacao           número da marcação",
        "criada_em             data e hora em que a marcação foi feita, hora legal",
        "canal                 portal, telefone (linha do dador) ou presencial (no centro)",
        "id_dador              número de dador: provisório (P) até à primeira dádiva, definitivo (D) depois dela",
        "documento_hash        documento de identificação indicado no registo, cifrado",
        "data_nascimento       como indicada no registo",
        "sexo                  como indicado no registo",
        "distrito              distrito de residência indicado no registo",
        "centro                centro de colheita da sessão",
        "data_sessao           dia da sessão marcada",
        "tipo_dadiva           primeira (quem ainda não deu sangue) ou regular",
        "data_primeira_dadiva  dia da primeira dádiva do dador",
        "estado                realizada, falta ou cancelada",
        "",
        "Avaliação de campanhas (Marketing de Dadores)",
        "A resposta a uma campanha conta as pessoas dos 18 aos 34 anos, com a idade no dia da marcação, que marcaram",
        "a primeira dádiva. Cada pessoa conta uma vez, na data da primeira marcação de primeira dádiva que fez,",
        "qualquer que tenha sido o desfecho. A referência é a média semanal das quatro semanas anteriores à campanha,",
        "de segunda-feira a domingo; a resposta é o que as semanas da campanha somam acima dessa média, por mil",
        "pessoas dos 18 aos 34 anos que a campanha levou três ou mais vezes, como o relatório da agência as dá.",
        "",
    ]
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))


def write_report_2025(path):
    """Meridiano Media's report on the April 2025 campaign"""
    import side2025 as S
    St = styles(NAVY)
    doc = _doc(path, "Gota Viva: campanha de televisão para jovens dadores, abril de 2025", K.AGENCY,
               "Relatório de campanha")
    end = S.CAMPAIGN[1]
    st = [Paragraph("Campanha de televisão para jovens dadores, abril de 2025: relatório", St["h1"]),
          Paragraph("%s para a %s &middot; %s &middot; ref. MM-GV-2025-RC" % (K.AGENCY, K.ORG, pt_date(S.REPORT_DATE)),
                    St["meta"]),
          Paragraph("1. A campanha", St["h2"]),
          Paragraph("Quatro semanas, de segunda-feira %s a domingo %s: %d spots de 30 segundos em primeiro lugar no "
                    "intervalo, no horário nobre de Vértice, Litoral e Pulsar, ao preço das tabelas do 2.º trimestre "
                    "de 2025." % (pt_date(S.CAMPAIGN[0]), pt_date(end), S.SPOTS_2025), St["body"]),
          Paragraph("2. Cobertura e frequência", St["h2"]),
          Paragraph("Lida no painel da %s, em direto, com os pesos do período e o universo de 2025 dos adultos dos 18 "
                    "aos 34 anos (%s mil pessoas)." % (K.PANEL_CO, format(S.UNIVERSE_2025 // 1000, ",").replace(",", ".")),
                    St["body"])]
    rows = [["Vezes que viu o filme", "Cobertura (% do universo)", "Pessoas (milhares)"]]
    for k, r in enumerate(S.REACH_2025, start=1):
        rows.append(["%d ou mais" % k, ("%.1f" % (100 * r)).replace(".", ","),
                     ("%.1f" % (S.UNIVERSE_2025 * r / 1000)).replace(".", ",")])
    st.append(_table(St, rows, [5.0, 5.0, 4.0], right=(1, 2)))
    st.append(Paragraph("Fonte: %s, painel de abril e maio de 2025; cálculo da %s." % (K.PANEL_CO, K.AGENCY), St["note"]))
    st.append(Paragraph("3. Notas", St["h2"]))
    st.append(Paragraph("Os spots passaram todos no lugar reservado. A resposta em marcações é medida pela %s a partir "
                        "do Portal do Dador." % K.ORG_SHORT, St["body"]))
    f = _frame(K.AGENCY, "Relatório de campanha 2025")
    doc.build(st, onFirstPage=f, onLaterPages=f)


DICTIONARY = [
    ("audimetria_visionamentos_2026-03.csv", "id_lar", "Código do lar do painel"),
    ("audimetria_visionamentos_2026-03.csv", "id_individuo", "Código da pessoa; convidados com o código do lar seguido de -C1"),
    ("audimetria_visionamentos_2026-03.csv", "dia_tv", "Dia de televisão (02:00 a 26:00, hora legal)"),
    ("audimetria_visionamentos_2026-03.csv", "canal", "Código do canal em vigor no dia"),
    ("audimetria_visionamentos_2026-03.csv", "inicio_utc", "Início do período de presença diante do canal, UTC"),
    ("audimetria_visionamentos_2026-03.csv", "fim_utc", "Fim do período de presença diante do canal, UTC"),
    ("audimetria_visionamentos_2026-03.csv", "emissao_utc", "Hora de emissão do que a pessoa estava a ver no início do "
                                                         "período, UTC; em direto, igual ao início"),
    ("audimetria_visionamentos_2026-03.csv", "modo", "AO VIVO ou DIFERIDO"),
    ("audimetria_visionamentos_2026-03.csv", "convidado", "S para convidados, N para membros do painel"),
    ("audimetria_individuos_2026-03.csv", "peso_28d", "Peso do período de 28 dias (zero para quem falhou algum dia)"),
    ("audimetria_individuos_2026-03.csv", "dias_em_amostra", "Dias do período em que a pessoa esteve em amostra"),
    ("emissao_publicitaria_2026-03.csv", "dia_tv", "Dia de televisão do intervalo"),
    ("emissao_publicitaria_2026-03.csv", "data", "Data civil da emissão do spot"),
    ("emissao_publicitaria_2026-03.csv", "hora_inicio", "Hora de início do spot, hora legal"),
    ("emissao_publicitaria_2026-03.csv", "id_intervalo", "Intervalo: canal, data do dia de televisão e número de ordem no dia"),
    ("emissao_publicitaria_2026-03.csv", "intervalo_no_programa", "Número de ordem do intervalo dentro do programa"),
    ("emissao_publicitaria_2026-03.csv", "posicao", "Lugar do spot no intervalo, a contar do início"),
    ("emissao_publicitaria_2026-03.csv", "colocacao", "Tipo de reserva: 1.º LUGAR, ÚLTIMO LUGAR, FIXO (spot fixo no "
                                                     "intervalo), ROTAÇÃO (spot vendido por janela horária) ou "
                                                     "AUTOPROMOÇÃO (promoção do próprio canal, sem reserva)"),
    ("emissao_publicitaria_2026-03.csv", "id_reserva", "Número da reserva na comercial do canal"),
    ("reservas_publicidade_2026-03.csv", "casa_comercial", "Comercial que vendeu o spot"),
    ("reservas_publicidade_2026-03.csv", "id_reserva", "Número da reserva, atribuído pela comercial"),
    ("reservas_publicidade_2026-03.csv", "data_reserva", "Data em que a reserva foi feita"),
    ("reservas_publicidade_2026-03.csv", "canal", "Código do canal em vigor no dia de televisão da reserva"),
    ("reservas_publicidade_2026-03.csv", "dia_tv", "Dia de televisão para que o spot foi vendido"),
    ("reservas_publicidade_2026-03.csv", "colocacao", "Tipo de reserva, nos termos da emissão publicitária"),
    ("reservas_publicidade_2026-03.csv", "programa", "Programa reservado; vazio na rotação"),
    ("reservas_publicidade_2026-03.csv", "intervalo_no_programa", "Intervalo reservado dentro do programa; vazio na "
                                                                  "rotação"),
    ("reservas_publicidade_2026-03.csv", "janela", "Janela horária vendida na rotação; vazio nas outras reservas"),
    ("grelha_programacao_2026-03.csv", "inicio", "Início do programa, hora legal"),
    ("audiencias_programas_semanais_2026-03.csv", "audiencia_media_18_34_milhares",
     "Audiência média do programa (média das emissões da semana), adultos 18-34, milhares"),
    ("esquemas_campanha_2027.xlsx", "Colocação", "1.º lugar no intervalo, último lugar no intervalo ou rotação"),
    ("universo_2026.csv", "populacao", "Universo de 2026, pessoas com 18 ou mais anos"),
    ("marcacoes_portal_dador_2025.csv", "id_dador", "Número de dador: provisório (P) até à primeira dádiva"),
    ("marcacoes_portal_dador_2025.csv", "documento_hash", "Documento de identificação indicado no registo, cifrado"),
    ("marcacoes_portal_dador_2025.csv", "criada_em", "Data e hora da marcação, hora legal"),
    ("marcacoes_portal_dador_2025.csv", "tipo_dadiva", "primeira ou regular"),
    ("marcacoes_portal_dador_2025.csv", "data_primeira_dadiva", "Dia da primeira dádiva do dador"),
]


def write_dictionary(path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["ficheiro", "campo", "descricao"])
        w.writerows(DICTIONARY)
