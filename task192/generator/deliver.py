"""The two files the programme officer puts in front of the trustees."""
import world as W


def workbook(path, g):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    wb = Workbook()
    thin = Side(style="thin", color="BFBFBF")
    box = Border(left=thin, right=thin, top=thin, bottom=thin)
    head_fill = PatternFill("solid", fgColor="E8E8E4")

    def header(ws, row, names, widths):
        for j, h in enumerate(names):
            c = ws.cell(row=row, column=1 + j, value=h)
            c.font = Font(bold=True)
            c.fill = head_fill
            c.border = box
            c.alignment = Alignment(horizontal="left" if j == 0 else "center", wrap_text=True)
        for (col, wd) in widths:
            ws.column_dimensions[col].width = wd

    ws = wb.active
    ws.title = "Resumo"
    ws["A1"] = "Vigilancia Nacional: boletim do periodo de 1 de maio a 30 de outubro de 2026"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = ("Indicador 3 do protocolo. Registo extraido em 6 de novembro de 2026; os episodios "
                "ainda abertos pertencem a coorte do periodo.")
    ws["A2"].font = Font(size=9, italic=True)
    rows = [("Taxa de confronto do periodo", "%d por cento" % g["rate_pct"]),
            ("Episodios a que corresponde", "%d episodios" % g["episodes"]),
            ("Episodios abertos no periodo", "%d episodios" % g["cohort"]),
            ("Com acao de confronto ja registada", "%d episodios" % g["recorded"]),
            ("Encerrados sem acao de confronto", "%d episodios" % g["closed_quiet"]),
            ("Ainda abertos na extracao", "%d episodios" % g["still_open"]),
            ("Acoes registadas no periodo",
             "%d acoes" % sum(v["actions"] for v in g["a1"].values()))]
    for i, (k, v) in enumerate(rows, 4):
        a = ws.cell(row=i, column=1, value=k)
        a.font = Font(bold=(i == 4))
        b = ws.cell(row=i, column=2, value=v)
        b.font = Font(bold=(i == 4))
        b.alignment = Alignment(horizontal="right")
    ws.cell(row=12, column=1, value=("A taxa cobre toda a vida de cada episodio da coorte, pelo que "
                                     "os episodios abertos na extracao entram com o que o registo "
                                     "mostra sobre o fim dos episodios."))
    ws.cell(row=12, column=1).font = Font(size=9, italic=True)
    ws.cell(row=13, column=1, value="Preparado para o conselho de curadores de 19 de novembro de 2026.")
    ws.cell(row=13, column=1).font = Font(size=9, italic=True)
    ws.column_dimensions["A"].width = 42
    ws.column_dimensions["B"].width = 20

    q = wb.create_sheet("Quinzenas")
    q["A1"] = "Acoes, territorio e rede de parceiros, por quinzena"
    q["A1"].font = Font(bold=True, size=12)
    header(q, 3, ["Quinzena", "De", "A", "Acoes registadas", "Municipios tocados",
                  "Quota da rede de parceiros, %"],
           [("A", 12), ("B", 13), ("C", 13), ("D", 17), ("E", 18), ("F", 26)])
    r = 4
    for label, v in sorted(g["a1"].items(), key=lambda kv: int(kv[0][1:])):
        for j, val in enumerate([label, v["start"], v["end"], v["actions"], v["municipalities"],
                                 v["partner_share"]]):
            c = q.cell(row=r, column=1 + j, value=val)
            c.border = box
            if j:
                c.alignment = Alignment(horizontal="center")
            if j in (3, 4):
                c.number_format = "#,##0"
            if j == 5:
                c.number_format = "0.0"
        r += 1
    q.cell(row=r + 1, column=1, value=("Uma acao e um tema numa localidade num dia, qualquer que "
                                       "seja o numero de relatos. A quota e a parte das acoes da "
                                       "quinzena que a rede de parceiros relatou."))
    q.cell(row=r + 1, column=1).font = Font(size=9, italic=True)
    q.freeze_panes = "A4"

    v = wb.create_sheet("Vias de acesso")
    v["A1"] = "Relatos por via de acesso no periodo"
    v["A1"].font = Font(bold=True, size=12)
    header(v, 3, ["Via", "Relatos recebidos", "Sem localidade fixada", "Minutos do inicio ao relato, mediana"],
           [("A", 30), ("B", 18), ("C", 22), ("D", 34)])
    r = 4
    name = dict(W.ROUTES)
    for code, _ in W.ROUTES:
        a2 = g["a2"][code]
        for j, val in enumerate(["%s (%s)" % (name[code], code), a2["received"], a2["unplaceable"],
                                 a2["median_minutes"]]):
            c = v.cell(row=r, column=1 + j, value=val)
            c.border = box
            if j:
                c.alignment = Alignment(horizontal="center")
            if j in (1, 2):
                c.number_format = "#,##0"
            if j == 3:
                c.number_format = "0.0"
        r += 1
    v.cell(row=r + 1, column=1, value=("Relatos recebidos em hora local no periodo, incluindo os "
                                       "que o gazeteiro nao fixou."))
    v.cell(row=r + 1, column=1).font = Font(size=9, italic=True)

    p = wb.create_sheet("Parceiros")
    p["A1"] = "Organizacoes parceiras: entregas e pagamento do periodo"
    p["A1"].font = Font(bold=True, size=12)
    header(p, 3, ["Codigo", "Organizacao", "Relatos entregues", "Entregues apos o fecho",
                  "Euros pagos"],
           [("A", 10), ("B", 46), ("C", 18), ("D", 22), ("E", 14)])
    r = 4
    for code, a3 in sorted(g["a3"].items()):
        for j, val in enumerate([code, a3["name"], a3["filed"], a3["after_close"], a3["euros"]]):
            c = p.cell(row=r, column=1 + j, value=val)
            c.border = box
            if j > 1:
                c.alignment = Alignment(horizontal="center")
            if j in (2, 3):
                c.number_format = "#,##0"
            if j == 4:
                c.number_format = "#,##0"
        r += 1
    p.cell(row=r + 1, column=1, value=("Relatos contados pelas acoes do periodo. Os entregues apos "
                                       "o fecho sao pagos com o periodo em que foram entregues "
                                       "(clausula 6.2)."))
    p.cell(row=r + 1, column=1).font = Font(size=9, italic=True)
    p.cell(row=r + 2, column=1, value=("A tabela do Observatorio Rural do Alentejo Central foi "
                                       "alterada pela adenda de 24 de julho, com efeito em 1 de "
                                       "agosto."))
    p.cell(row=r + 2, column=1).font = Font(size=9, italic=True)
    p.freeze_panes = "A4"
    v.freeze_panes = "A4"

    nt = wb.create_sheet("Notas")
    nt["A1"] = "Notas do boletim"
    nt["A1"].font = Font(bold=True, size=12)
    notes = [
        ("Registo", "Vigilancia Nacional, aberta em 1 de maio de 2026; extracao de 6 de novembro de 2026."),
        ("Indicador 3", "Taxa de confronto do protocolo 3.3, em percentagem inteira, com o numero de "
                        "episodios a que corresponde."),
        ("Acao", "Um tema de disputa numa localidade num dia (protocolo 2.1). Os relatos das tres "
                 "vias e das duas edicoes do grupo Atlantico contam uma vez."),
        ("Episodio", "Um municipio e um tema, encerrado por vinte e um dias sem acao (protocolo 3.1)."),
        ("Quinzenas", "Contadas a partir de 1 de maio; a ultima tem quinze dias e termina com o "
                      "periodo (protocolo 3.4)."),
        ("Carga de agosto", "O mes de agosto da rede de parceiros foi reposto numa segunda carga; "
                            "cada relato conta uma vez (registo_importacoes)."),
        ("Relogios", "O carimbo de recepcao do monitor de imprensa vem em UTC; as horas de inicio "
                     "das acoes sao locais."),
    ]
    for i, (k, vtxt) in enumerate(notes, 3):
        a = nt.cell(row=i, column=1, value=k)
        a.font = Font(bold=True)
        c = nt.cell(row=i, column=2, value=vtxt)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    nt.column_dimensions["A"].width = 20
    nt.column_dimensions["B"].width = 104
    wb.save(path)
    return path


def chart(path, g):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    labels = sorted(g["a1"], key=lambda k: int(k[1:]))
    total = [g["a1"][k]["actions"] for k in labels]
    conf = [g["a1"][k]["confrontational"] for k in labels]
    rest = [t - c for t, c in zip(total, conf)]
    fig, ax = plt.subplots(figsize=(8.6, 4.3), dpi=150)
    ax.bar(labels, rest, color="#9fb0c4", edgecolor="#ffffff", linewidth=1.1,
           label="acoes sem acao de confronto")
    ax.bar(labels, conf, bottom=rest, color="#8c2f2f", edgecolor="#ffffff", linewidth=1.1,
           label="acoes de confronto")
    for i, t in enumerate(total):
        ax.annotate("%d" % t, xy=(i, t), xytext=(0, 3), textcoords="offset points",
                    ha="center", fontsize=8.5)
    ax.set_ylabel("Acoes registadas")
    ax.set_title("Acoes registadas por quinzena, 1 de maio a 30 de outubro de 2026")
    ax.legend(frameon=False, fontsize=8.5, loc="upper left")
    ax.set_ylim(0, max(total) * 1.18)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(axis="x", labelsize=9)
    ax.grid(axis="y", color="#dcdfe4", linewidth=0.6)
    ax.set_axisbelow(True)
    fig.text(0.012, 0.012, "Vigilancia Nacional, registo extraido em 6 de novembro de 2026. A "
                           "ultima quinzena do periodo tem seis dias.", fontsize=7.6,
             color="#55606b")
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    fig.savefig(path, metadata={"Software": None, "Creation Time": None})
    plt.close(fig)
    return path
