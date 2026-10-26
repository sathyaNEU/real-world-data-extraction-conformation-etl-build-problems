"""The goldens from the shipped pack: Meridiano Media's plan workbook for Gota Viva (the schedule to buy, each
schedule's reach, the 2025 campaign's response and each schedule's expected first-donation bookings) and the
recommendation deck for the Executive Committee; and generator/figures.json, every figure the write-up states."""
import json
import os

import analysis as AN    # noqa: E402
import asks as AS        # noqa: E402
import common as K       # noqa: E402
import side2025 as S25   # noqa: E402

NAVY, RED, GREY, INK, LIGHT = "1D3557", "A3132B", "8A929C", "1F2328", "C9D3DE"


def r10(x):
    return int(K.r(x / 10.0) * 10)


def pt(x, n=1):
    """a number as a Portuguese reader writes it: decimal comma, thousands with a point"""
    s = ("%%.%df" % n) % x
    whole, _, dec = s.partition(".")
    whole = format(int(whole), ",").replace(",", ".")
    return whole + ("," + dec if dec else "")


def compute(target):
    P = AN.Pack(target)
    m = AN.main_call(target, pack=P)
    a = AS.all_asks(target, P)
    pb = AN.prime_bookings(P)
    bp = AN.b_places(P)
    resp = a["response"]
    cost = {s: int(sum(ln["price"] for ln in P.sched[s])) for s in K.SCHED}
    spots = {s: len(P.sched[s]) for s in K.SCHED}
    fig = {
        "call": {"schedule": m["call"], "runner_up": m["runner"], "lead_points": K.r(100 * m["lead"], 1)},
        "components": {
            "reach3_pct": {s: K.pct(m["reach3"][s]) for s in K.SCHED},
            "prime_rotation_bookings": pb["bookings"],
            "prime_rotation_bookings_aired_outside_prime": pb["elsewhere"],
            "share_aired_outside_prime_pct": K.pct(pb["share_elsewhere"]),
            "schedule_b_reference_places": bp["places"],
            "schedule_b_reference_places_outside_prime": bp["outside"],
        },
        "asks": {
            "R": {"baseline_weekly_average": K.r(resp["avg"], 1),
                  "campaign_weeks_above_baseline": [K.r(x, 1) for x in resp["above"]],
                  "campaign_weeks_total_above": K.r(resp["extra"], 1),
                  "response_per_thousand_reached3": K.r(resp["per_thousand"], 2)},
            "X": {"expected_first_donation_bookings": {s: r10(a["bookings"][s]) for s in K.SCHED}},
        },
        "context": {"spots": spots, "cost_eur": cost, "budget_eur": K.BUDGET,
                    "reach1_pct": {s: K.pct(a["reach1"][s]) for s in K.SCHED},
                    "schedule_b_reach3_in_window_rotation_places_pct": None,
                    "universe_18_34": a["universe"], "reached3_2025_thousands": AS.REPORT_REACHED3,
                    "baseline_weeks": [S25.BASELINE[0].isoformat(), S25.BASELINE[1].isoformat()],
                    "campaign_weeks_2025": [S25.CAMPAIGN[0].isoformat(), S25.CAMPAIGN[1].isoformat()]},
        "references": {"brief_clauses": ["3.2", "3.3", "3.4", "3.5"], "weight_days": 28, "age_band": [18, 34]},
    }
    easy = AN.main_call(target, route="asrun", pack=P)["reach3"]["B"]
    fig["context"]["schedule_b_reach3_in_window_rotation_places_pct"] = K.pct(easy)
    res = dict(pack=P, main=m, asks=a, prime=pb, bplaces=bp, easy_b=easy)
    return fig, res


def write_workbook(path, fig):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = Workbook()
    ws = wb.active
    ws.title = "Recomendação"
    head = Font(bold=True, color="FFFFFF")
    fill = PatternFill("solid", fgColor=NAVY)
    pick = PatternFill("solid", fgColor="F3E3E6")
    thin = Side(style="thin", color=LIGHT)
    c, ctx, r3 = fig["call"], fig["context"], fig["components"]["reach3_pct"]
    ws["A1"] = "Gota Viva, campanha de televisão para jovens dadores, abril de 2027"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Comprar o %s: leva o filme três ou mais vezes a %s%% dos adultos dos 18 aos 34 anos, %s pontos " \
               "acima do %s." % (K.SCHED_NAME[c["schedule"]].split(",")[0], pt(r3[c["schedule"]]),
                                 pt(c["lead_points"]), K.SCHED_NAME[c["runner_up"]].split(",")[0])
    ws["A2"].font = Font(bold=True, color=RED)
    ws["A3"] = "Meridiano Media para a Comissão Executiva da Associação Gota Viva, 2 de dezembro de 2026"
    ws["A3"].font = Font(italic=True, color=GREY)
    hdr = ["Esquema", "Descrição", "Spots", "Custo (EUR)", "Cobertura 1+ (% 18-34)", "Cobertura 3+ (% 18-34)",
           "Marcações de primeira dádiva esperadas"]
    ws.append([])
    ws.append(hdr)
    for cell in ws[5]:
        cell.font, cell.fill = head, fill
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    ws.row_dimensions[5].height = 42
    for s in K.SCHED:
        ws.append([s, K.SCHED_NAME[s].split(", ", 1)[1].capitalize(), ctx["spots"][s], ctx["cost_eur"][s],
                   ctx["reach1_pct"][s], r3[s],
                   fig["asks"]["X"]["expected_first_donation_bookings"][s]])
    for row in ws.iter_rows(min_row=6, max_row=8):
        row[3].number_format = "#,##0"
        row[4].number_format = "0.0"
        row[5].number_format = "0.0"
        row[6].number_format = "#,##0"
        for cell in row:
            cell.border = Border(bottom=thin)
        if row[0].value == c["schedule"]:
            for cell in row:
                cell.fill = pick
                cell.font = Font(bold=True)
    ws.append([])
    ws.append(["Vantagem do esquema recomendado sobre o segundo (pontos de cobertura 3+)", None, None, None, None,
               c["lead_points"]])
    ws.cell(row=ws.max_row, column=6).number_format = "0.0"
    for col, wdt in zip("ABCDEFG", (10, 46, 8, 12, 14, 14, 16)):
        ws.column_dimensions[col].width = wdt
    ws.freeze_panes = "A6"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True

    r = wb.create_sheet("Resposta 2025")
    rr = fig["asks"]["R"]
    r.append(["Resposta à campanha de abril de 2025 (Portal do Dador)"])
    r["A1"].font = Font(bold=True, size=12)
    r.append(["Marcações de primeira dádiva de pessoas dos 18 aos 34 anos, cada pessoa contada uma vez na data da "
              "primeira marcação"])
    r["A2"].font = Font(italic=True, color=GREY)
    r.append([])
    r.append(["Período", "Marcações"])
    for cell in r[4]:
        cell.font, cell.fill = head, fill
    r.append(["Média semanal, 10 de março a 6 de abril de 2025", rr["baseline_weekly_average"]])
    weeks = ["7 a 13 de abril", "14 a 20 de abril", "21 a 27 de abril", "28 de abril a 4 de maio"]
    for wk, v in zip(weeks, rr["campaign_weeks_above_baseline"]):
        r.append(["Semana de %s, menos a média" % wk, v])
    r.append(["As quatro semanas da campanha, menos a média", rr["campaign_weeks_total_above"]])
    r.append(["Resposta por mil pessoas dos 18 aos 34 anos levadas três ou mais vezes (%s mil)" % pt(AS.REPORT_REACHED3),
              rr["response_per_thousand_reached3"]])
    for row in r.iter_rows(min_row=5, max_row=10):
        row[1].number_format = "0.0"
    r.cell(row=11, column=2).number_format = "0.00"
    r.column_dimensions["A"].width = 78
    r.column_dimensions["B"].width = 12

    n = wb.create_sheet("Notas")
    for line in [
        "Cobertura: parte do universo de 2026 dos adultos dos 18 aos 34 anos (painel da Audimetria Lusa, 2.100 mil "
        "pessoas) que se espera que veja o filme o número de vezes indicado ou mais, com cada esquema lido nas "
        "quatro semanas de referência de 2 a 29 de março de 2026 (briefing, 3.1 a 3.5).",
        "Rotação: cada spot é lido em cada lugar em que passaram as reservas de rotação do mesmo canal e da mesma "
        "janela nesse dia de referência, com a parte dessas reservas que lá passou; as reservas das comerciais "
        "juntam-se à emissão publicitária pelo número de reserva.",
        "Marcações esperadas: a resposta de 2025 por mil pessoas levadas três ou mais vezes aplicada às pessoas "
        "que cada esquema leva três ou mais vezes, arredondada à dezena.",
        "Resposta de 2025: regra da Marketing de Dadores nas notas da extração do Portal do Dador de 2 de julho "
        "de 2025; uma pessoa é o seu documento de identificação, porque quem se registou de novo no Portal depois "
        "de 17 de março de 2025 tem um segundo número de dador.",
        "Custos: tabelas do 2.º trimestre de 2027, sem descontos de volume; orçamento de 230.000 euros.",
    ]:
        n.append([line])
        n.cell(row=n.max_row, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    n.column_dimensions["A"].width = 120
    wb.save(path)


def write_deck(path, fig, res):
    from pptx import Presentation
    from pptx.chart.data import CategoryChartData
    from pptx.dml.color import RGBColor
    from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
    from pptx.util import Cm, Pt
    prs = Presentation()
    prs.slide_width, prs.slide_height = Cm(33.867), Cm(19.05)
    blank = prs.slide_layouts[6]
    c, ctx, r3 = fig["call"], fig["context"], fig["components"]["reach3_pct"]

    def text(slide, x, y, w, h, s, size=14, bold=False, color=INK):
        tb = slide.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = s
        p.font.size, p.font.bold, p.font.name = Pt(size), bold, "Arial"
        p.font.color.rgb = RGBColor.from_string(color)
        return tf

    def table(slide, x, y, w, rows, widths, bold_row=None, red_row=None):
        from pptx.util import Cm as _Cm
        shp = slide.shapes.add_table(len(rows), len(rows[0]), _Cm(x), _Cm(y), _Cm(w), _Cm(0.9 * len(rows)))
        tb = shp.table
        for j, wd in enumerate(widths):
            tb.columns[j].width = _Cm(wd)
        for i, r in enumerate(rows):
            for j, v in enumerate(r):
                cell = tb.cell(i, j)
                cell.text = str(v)
                para = cell.text_frame.paragraphs[0]
                para.font.size, para.font.name = Pt(13), "Arial"
                para.font.bold = i == 0 or i == bold_row
                if j > 0:
                    from pptx.enum.text import PP_ALIGN
                    para.alignment = PP_ALIGN.RIGHT
                cell.fill.solid()
                cell.fill.fore_color.rgb = RGBColor.from_string(NAVY if i == 0 else ("F3E3E6" if i == red_row else
                                                                                     "FFFFFF"))
                para.font.color.rgb = RGBColor.from_string("FFFFFF" if i == 0 else (RED if i == red_row else INK))
        return tb

    def footer(slide, k, src):
        text(slide, 1.2, 17.9, 26, 0.8, src, 9, color=GREY)
        text(slide, 31.0, 17.9, 2, 0.8, str(k), 9, color=GREY)

    pick, run = c["schedule"], c["runner_up"]
    # 1. the call
    s1 = prs.slides.add_slide(blank)
    text(s1, 1.2, 1.0, 31, 1.2, "Campanha de televisão para jovens dadores, abril de 2027", 14, color=GREY)
    text(s1, 1.2, 2.6, 31, 3.5, "Comprar o Esquema %s: leva o filme três ou mais vezes a %s%% dos adultos dos 18 "
         "aos 34 anos, %s pontos acima do Esquema %s" % (pick, pt(r3[pick]), pt(c["lead_points"]), run),
         26, True, NAVY)
    xx = fig["asks"]["X"]["expected_first_donation_bookings"]
    rows = [["Esquema", "Spots", "Custo (euros)", "Três ou mais vezes (%)", "Pelo menos uma vez (%)",
             "Marcações esperadas"]]
    for s in K.SCHED:
        rows.append(["%s, %s" % (s, K.SCHED_NAME[s].split(", ", 1)[1]), ctx["spots"][s], pt(ctx["cost_eur"][s], 0),
                     pt(r3[s]), pt(ctx["reach1_pct"][s]), pt(xx[s], 0)])
    table(s1, 1.2, 7.4, 31.4, rows, [11.4, 2.6, 4.0, 4.6, 4.6, 4.2], red_row=1 + K.SCHED.index(pick))
    text(s1, 1.2, 12.0, 31, 1.6, "Universo: 2.100 mil adultos dos 18 aos 34 anos (painel de 2026). Cada esquema lido "
         "nas quatro semanas de referência de março de 2026, como o briefing pede (3.1 a 3.5).", 11, color=GREY)
    footer(s1, 1, "Meridiano Media para a Comissão Executiva da Associação Gota Viva, 2 de dezembro de 2026")
    # 2. the chart
    s2 = prs.slides.add_slide(blank)
    text(s2, 1.2, 0.9, 31, 2.2, "O Esquema %s leva mais jovens três ou mais vezes e traz mais marcações: %s%% da "
         "rotação do horário nobre que o Esquema B compra passa em intervalos de dia" % (
             pick, pt(fig["components"]["share_aired_outside_prime_pct"])), 20, True, NAVY)
    xx = fig["asks"]["X"]["expected_first_donation_bookings"]

    def bars(x, title, values, fmt, top):
        cd = CategoryChartData()
        cd.categories = ["Esquema %s" % s for s in K.SCHED]
        cd.add_series(title, values)
        gf = s2.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Cm(x), Cm(3.6), Cm(10.2), Cm(13.6), cd)
        ch = gf.chart
        ch.has_legend = False
        ch.has_title = True
        ch.chart_title.text_frame.text = title
        ch.chart_title.text_frame.paragraphs[0].font.size = Pt(12)
        ch.chart_title.text_frame.paragraphs[0].font.bold = True
        va = ch.value_axis
        va.maximum_scale, va.minimum_scale = top, 0.0
        va.has_major_gridlines = True
        va.major_gridlines.format.line.color.rgb = RGBColor.from_string("E3E7EC")
        va.tick_labels.font.size = Pt(10)
        ch.category_axis.tick_labels.font.size = Pt(11)
        ser = ch.series[0]
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = RGBColor.from_string(NAVY)
        ser.data_labels.show_value = True
        ser.data_labels.number_format = fmt
        ser.data_labels.number_format_is_linked = False
        ser.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
        ser.data_labels.font.size = Pt(11)
        bar = ser.points[K.SCHED.index(pick)]
        bar.format.fill.solid()
        bar.format.fill.fore_color.rgb = RGBColor.from_string(RED)

    bars(1.2, "Três ou mais vezes (% dos 18 aos 34 anos)", [r3[s] for s in K.SCHED], "0.0", 35.0)
    bars(11.6, "Marcações de primeira dádiva esperadas", [xx[s] for s in K.SCHED], "#,##0", 500.0)
    text(s2, 1.2, 17.2, 20, 0.7, "A vermelho, o esquema a comprar.", 10, color=GREY)
    pb = fig["components"]
    tf = text(s2, 22.4, 4.2, 10.4, 13, "Porque a rotação rende menos", 14, True, INK)
    for line in [
        "Nas quatro semanas de referência, as comerciais venderam %s reservas de rotação no horário nobre de "
        "Vértice, Litoral e Pulsar+; %s (%s%%) passaram em intervalos de dia, onde quase não há jovens a ver."
        % (pt(pb["prime_rotation_bookings"], 0), pt(pb["prime_rotation_bookings_aired_outside_prime"], 0),
           pt(pb["share_aired_outside_prime_pct"])),
        "Lida só nos lugares de rotação que o horário nobre mostra, o Esquema B parecia chegar a %s%% três ou mais "
        "vezes." % pt(ctx["schedule_b_reach3_in_window_rotation_places_pct"]),
        "Os primeiros lugares do Esquema A passam onde foram marcados.",
    ]:
        p = tf.add_paragraph()
        p.text = line
        p.font.size, p.font.name = Pt(12), "Arial"
        p.font.color.rgb = RGBColor.from_string(INK)
        p.space_before = Pt(8)
    footer(s2, 2, "Fonte: Audimetria Lusa, painel de 2 a 29 de março de 2026; emissão publicitária dos canais e "
               "reservas das comerciais; cálculo da Meridiano Media")
    # 3. the expected bookings
    s3 = prs.slides.add_slide(blank)
    rr = fig["asks"]["R"]
    text(s3, 1.2, 0.9, 31, 2.2, "À resposta de 2025, o Esquema %s traria cerca de %d marcações de primeira dádiva, "
         "mais %d do que o %s" % (pick, xx[pick], xx[pick] - xx[run], run), 20, True, NAVY)
    rows = [["Campanha de abril de 2025", "Marcações"],
            ["Média semanal, 10 de março a 6 de abril", pt(rr["baseline_weekly_average"])]]
    for wk, v in zip(["7 a 13 de abril", "14 a 20 de abril", "21 a 27 de abril", "28 de abril a 4 de maio"],
                     rr["campaign_weeks_above_baseline"]):
        rows.append(["%s, menos a média" % wk, pt(v)])
    rows.append(["As quatro semanas, menos a média", pt(rr["campaign_weeks_total_above"])])
    rows.append(["Por mil jovens levados três ou mais vezes (%s mil)" % pt(AS.REPORT_REACHED3), pt(rr["response_per_thousand_reached3"], 2)])
    table(s3, 1.2, 3.8, 15.6, rows, [11.6, 4.0], bold_row=len(rows) - 1)
    rows2 = [["Esquema", "Três ou mais vezes (mil pessoas)", "Marcações esperadas"]]
    for s in K.SCHED:
        rows2.append([s, pt(r3[s] * ctx["universe_18_34"] / 100000.0, 0), pt(xx[s], 0)])
    table(s3, 18.2, 3.8, 14.4, rows2, [3.0, 6.4, 5.0], red_row=1 + K.SCHED.index(pick))
    text(s3, 18.2, 8.2, 14.4, 3, "Marcações esperadas: a resposta de 2025 vezes as pessoas que cada esquema leva três "
         "ou mais vezes, arredondadas à dezena.", 11, color=GREY)
    footer(s3, 3, "Fonte: Portal do Dador, extração de 2 de julho de 2025; relatório da campanha de 2025 da "
               "Meridiano Media")
    prs.core_properties.title = "Esquema de televisão para jovens dadores, abril de 2027"
    prs.save(path)


def write(target, golden):
    os.makedirs(golden, exist_ok=True)
    fig, res = compute(target)
    write_workbook(os.path.join(golden, K.BOOK), fig)
    write_deck(os.path.join(golden, K.DECK), fig, res)
    return fig, res


def write_figures(path, fig):
    with open(path, "w") as f:
        json.dump(fig, f, indent=1, sort_keys=True, ensure_ascii=False)
        f.write("\n")
