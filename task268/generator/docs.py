"""task268's documents: the platform reliability standard PR-SLO-3 (docx), the service catalogue (xlsx) and the two
context files the solution never reads (the Q4 capacity review and the app store reviews)."""
import datetime as dt
import os

import numpy as np
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

import common as K


def _p(doc, text, bold=False, size=10.5, italic=False, align=None, space=4):
    para = doc.add_paragraph()
    run = para.add_run(text)
    run.bold, run.italic = bold, italic
    run.font.size = Pt(size)
    para.paragraph_format.space_after = Pt(space)
    if align:
        para.alignment = align
    return para


def write_slo(path):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    _p(doc, "Rotalinha Platform Reliability", bold=True, size=9)
    _p(doc, "PR-SLO-3  Service level objectives for internal services", bold=True, size=16, space=2)
    _p(doc, "Version 3.1, in force from 1 January 2026. Owner: %s, Head of Platform Reliability. Approved by the "
            "engineering leadership group on 9 December 2025." % K.PEOPLE["head"], size=9, italic=True, space=10)

    _p(doc, "1  Purpose and scope", bold=True, size=12)
    _p(doc, "This standard sets the latency objective each internal service in the service catalogue is held to, the "
            "annual review that reads it, and the figures the annual reliability review reports beside it.")

    _p(doc, "2  The latency SLI", bold=True, size=12)
    _p(doc, "2.1  A service's latency SLI for a period is the share of the requests the service handled in that period "
            "whose server-side duration exceeded the service's latency threshold.")
    _p(doc, "2.2  A request is any call a caller sent the service, whether from the edge, from another internal service "
            "or from a scheduled job, and whether or not the tracing store kept a span for it. Every request reaches the "
            "service through its load balancer target group; the load balancer's own health probes are not requests.")
    _p(doc, "2.3  The server-side duration of a request is the duration of the span the service records for its own "
            "handling of it, from the moment the service starts handling the request to the moment it sends its "
            "response. A call the service makes to another service is that other service's request.")
    _p(doc, "2.4  A request belongs to the hour, day and period in which the service started handling it. A request "
            "that ended in an error counts like any other.")

    _p(doc, "3  The annual review", bold=True, size=12)
    _p(doc, "3.1  The annual review reads each service's latency SLI over December, in Lisbon time: the month of the "
            "heaviest traffic, and the 31 days the tracing store holds on the review date.")
    _p(doc, "3.2  A service breaches its latency objective when its latency SLI for the review period exceeds its "
            "error budget.")
    _p(doc, "3.3  Each service that breaches its latency objective in the 2026 review is assigned a reliability "
            "engineer for January to June 2027 under the reliability programme.")

    _p(doc, "4  Thresholds and error budgets", bold=True, size=12)
    tbl = doc.add_table(rows=1, cols=4)
    tbl.style = "Table Grid"
    for i, h in enumerate(["Service", "Tier", "Latency threshold (ms)", "Error budget (share of requests)"]):
        c = tbl.rows[0].cells[i]
        c.text = h
        c.paragraphs[0].runs[0].bold = True
    for s in K.SVC:
        row = tbl.add_row().cells
        row[0].text = s
        row[1].text = str(K.TIER[s])
        row[2].text = "{:,}".format(K.THRESHOLD[s])
        row[3].text = "%.1f%%" % K.BUDGET[s]
    _p(doc, "", space=4)

    _p(doc, "5  What the annual reliability review reports beside the SLI", bold=True, size=12)
    _p(doc, "5.1  Releases and rollbacks. A release is a build of a service, the code of one commit, reaching production "
            "for the first time. A rollback is production's running build being replaced by a build that was first "
            "released before it. A deployment that does not finish successfully changes nothing, and a deployment to "
            "staging is not production.")
    _p(doc, "5.2  Customer-facing incident minutes. An incident is customer-facing when it was posted on the public "
            "status page. Its minutes run from its declaration in the incident tool until the status page shows every "
            "component it affected operational again. A service's customer-facing incident minutes in a period are "
            "the minutes in which a customer-facing incident named it, counted once however many incidents named it "
            "at the time.")
    _p(doc, "5.3  Service cost. A service's cost is the cloud provider's charge for the resources that ran for it, in "
            "euros as invoiced, net of discounts and credits and before VAT, dated by the day the resource ran. "
            "Platform costs shared by every service, such as the support plan, are no service's cost.")
    _p(doc, "5.4  Periods are read in Lisbon time: the first half of 2026 runs from 1 January to 30 June, the second "
            "from 1 July to 31 December.")

    _p(doc, "6  Review of this standard", bold=True, size=12)
    _p(doc, "Platform Reliability reviews this standard every December. Thresholds are set with each owning team and "
            "move only at a review.")
    doc.save(path)


def write_catalogue(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Services"
    head = ["Service", "Team", "Tier", "Tracing service name", "Load balancer target group (from 1 Jul 2026)",
            "Load balancer target group (to 30 Jun 2026)", "Status page component", "Cost tag (service=)",
            "Team tag (team=)", "On-call rota"]
    ws.append(head)
    for s in K.SVC:
        ws.append([s, K.TEAM[s], K.TIER[s], K.TRACE_NAME[s], K.TG_H2[s], K.TG_H1[s], K.COMPONENT[s], K.COST_TAG[s],
                   K.OLD_TAG[s], "%s-primary" % K.TEAM[s].lower().replace(" & ", "-").replace(" ", "-")])
    for c in ws[1]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE7F0")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for col, wdt in zip("ABCDEFGHIJ", [18, 20, 6, 18, 24, 24, 26, 22, 18, 28]):
        ws.column_dimensions[col].width = wdt
    wb.save(path)


CAP_ROWS = {
    "journey-search": ("63%", "58%", "Index rebuild moved to 03:00 in November"),
    "fares": ("68%", "41%", ""),
    "places": ("46%", "47%", "Cache warm-up added after the October release"),
    "seat-map": ("41%", "52%", "Hold timeouts raised from 8 to 10 minutes"),
    "booking": ("33%", "39%", ""),
    "payments": ("29%", "36%", "Second card processor connected in September"),
    "tickets": ("26%", "61%", "PDF rendering on a separate pool from March"),
    "accounts": ("61%", "33%", ""),
    "partner-gateway": ("31%", "49%", "Two ferry operators moved to the new availability API"),
    "notifications": ("22%", "28%", ""),
}


def write_capacity(path, w):
    import world as W
    lines = ["# Capacity review, Q4 2026", "",
             "Prepared by Platform Infrastructure for the January planning round. Figures are December peaks unless "
             "stated.", "",
             "| Service | Pods (Dec peak) | Peak CPU per pod | Peak memory per pod | Autoscaling | Notes |",
             "|---|---|---|---|---|---|"]
    for s in K.SVC:
        lo, hi, per = K.AUTOSCALE[s]
        n = w.N[s][W.DEC0:W.DEC0 + K.REVIEW_HOURS]
        peak = int(np.clip(np.ceil(n / per), lo, hi).max())
        cpu, mem, note = CAP_ROWS[s]
        lines.append("| %s | %d | %s | %s | %d to %d | %s |" % (s, peak, cpu, mem, lo, hi, note))
    lines += ["", "Planned for 2027: the search index moves to dedicated nodes in February; the partner gateway's "
              "connection pools are reviewed with Supply Integration in March.", ""]
    with open(path, "w") as fh:
        fh.write("\n".join(lines))


REVIEW_WORDS = {
    "en": {5: (["Bought my ferry ticket in two minutes", "Easy to change my booking", "Seat choice works well now",
                "Best way to book the {route} coach", "Boarding pass straight into my wallet, very handy",
                "Clear prices and no surprises at checkout", "Used it all summer for the {route} bus",
                "Refund came through in three days", "Much better than buying at the station"],
               ["", " Great app.", " Recommended.", " Will use again.", " Thanks!", " Five stars."]),
           4: (["Good prices, search could be quicker at busy times", "Works fine, sign-in sometimes slow",
                "Handy for the {route} coach", "Does the job, the seat map takes a while to load",
                "Nice app but I wish it remembered my passengers", "Booked {route} without issues, a bit slow on wifi"],
               ["", ".", " Otherwise great.", " Mostly happy."]),
           3: (["Search took ages before Christmas", "Ticket email came late but arrived",
                "Fine, but the seat map kept spinning", "The {route} times were wrong once",
                "Okay app, too many steps to pay"], ["", ".", " Could be better.", " Needs work."]),
           2: (["Payment failed twice, worked on the third try", "Could not find my stop in the list",
                "Search results kept timing out for {route}", "Had to call support to get my ticket"],
               ["", ".", " Frustrating.", " Not great."]),
           1: (["App froze on the booking page", "Never got my ticket by email", "Charged twice for one trip",
                "Search for {route} never loaded"], ["", ".", " Avoid.", " Uninstalled."])},
    "pt": {5: (["Comprei o bilhete do ferry em dois minutos", "Muito fácil mudar a reserva", "Ótima app para o {route}",
                "Preços claros, sem surpresas", "O cartão de embarque fica logo no telemóvel",
                "Reembolso rápido, sem complicações", "Muito melhor do que comprar na estação", "Uso sempre para ir a {route}"],
               ["", ". Recomendo.", "!", ". Excelente."]),
           4: (["Boa app, a pesquisa às vezes é lenta", "Funciona bem para o {route}", "Bons preços, falta pouco",
                "Gosto, mas o login às vezes demora", "Cumpre, o mapa de lugares é lento", "Prática para o {route}, com wifi fraco demora"],
               ["", ".", ". No geral bom."]),
           3: (["A pesquisa demorou muito antes do Natal", "O e-mail do bilhete chegou tarde",
                "O mapa de lugares não carregava", "Os horários do {route} estavam errados", "Demasiados passos para pagar"], ["", ".", ". Pode melhorar."]),
           2: (["O pagamento falhou duas vezes", "Não encontrei a minha paragem", "A pesquisa do {route} dava sempre erro",
                "Tive de ligar para o apoio para ter o bilhete"], ["", ".", ". Fraco."]),
           1: (["A app bloqueou na reserva", "Nunca recebi o bilhete", "Cobraram duas vezes a mesma viagem"], ["", ".", ". Péssimo."])},
    "es": {5: (["Compré el billete en dos minutos", "Muy cómoda para el {route}", "Precios claros, sin sorpresas",
                "Cambiar la reserva fue muy fácil", "Reembolso rápido y sin líos", "La tarjeta de embarque va directa al móvil"], ["", ". Recomendada.", "!", ". Genial."]),
           4: (["Buena app, la búsqueda a veces va lenta", "Funciona bien para el {route}", "Buenos precios, le falta poco",
                "Cumple, el mapa de asientos tarda"], ["", ".", ". Bien."]),
           3: (["La búsqueda tardó mucho en Navidad", "El billete llegó tarde por correo", "Los horarios del {route} estaban mal"], ["", ".", ". Mejorable."]),
           2: (["El pago falló dos veces", "No encontraba mi parada", "La búsqueda del {route} daba error"], ["", ".", ". Regular."]),
           1: (["La app se colgó al pagar", "Nunca recibí el billete", "Me cobraron dos veces el mismo viaje"], ["", ".", ". Fatal."])},
}
OPENERS = {"en": ["Honestly, ", "Second trip with it. ", "Travelled with the kids. ", "Used it for work. ", "Update: ",
                   "First time using it. "],
           "pt": ["Sinceramente, ", "Segunda viagem. ", "Viajei com os miúdos. ", "Uso para o trabalho. "],
           "es": ["La verdad, ", "Segundo viaje. ", "Viajé con los niños. ", "La uso para el trabajo. "]}
DETAILS = {"en": [" on my phone", " on the way back", " this weekend", " last week", " in August", " at the station"],
           "pt": [" no telemóvel", " no regresso", " este fim de semana", " na semana passada", " em agosto"],
           "es": [" en el móvil", " a la vuelta", " este fin de semana", " la semana pasada", " en agosto"]}
SHORT = {"en": {5: "Great", 4: "Good", 3: "Ok", 2: "Meh", 1: "Bad"}, "pt": {5: "Muito bom", 4: "Bom", 3: "Razoável",
         2: "Fraco", 1: "Mau"}, "es": {5: "Muy buena", 4: "Bien", 3: "Normal", 2: "Regular", 1: "Mala"}}
ROUTES = ["Lisbon to Porto", "Porto to Vigo", "Faro to Seville", "Lisbon to Faro", "Lagos", "Coimbra", "Braga",
          "Madrid to Lisbon", "Setúbal ferry", "Tróia ferry", "Évora", "Aveiro"]


def write_feedback(path):
    r = np.random.default_rng(K.SEED + 606)
    wb = Workbook()
    ws = wb.active
    ws.title = "Reviews"
    ws.append(["review_date", "store", "app_version", "rating", "text", "country"])
    d0 = dt.date(2026, 7, 1)
    rows = []
    for i in range(1480):
        day = d0 + dt.timedelta(days=int(r.integers(0, 184)))
        rating = int(r.choice([5, 4, 3, 2, 1], p=[0.46, 0.24, 0.13, 0.08, 0.09]))
        country = str(r.choice(["PT", "PT", "PT", "ES", "ES", "FR", "GB"]))
        store = str(r.choice(["App Store", "Google Play"]))
        lang = {"PT": "pt", "ES": "es"}.get(country, "en")
        mains, ends = REVIEW_WORDS[lang][rating]
        if r.random() < 0.08:
            text = SHORT[lang][rating]
        else:
            body = str(r.choice(mains)).replace("{route}", str(r.choice(ROUTES)))
            if r.random() < 0.4:
                body += str(r.choice(DETAILS[lang]))
            if r.random() < 0.3:
                op = str(r.choice(OPENERS[lang]))
                body = op + (body[0].lower() + body[1:] if op.endswith(", ") else body)
            text = body + str(r.choice(ends))
        if store == "Google Play" and r.random() < 0.3:
            text = None                                # a rating left without a review: an empty cell
        rows.append([day, store, "6.%d.%d" % (int(r.integers(10, 19)), int(r.integers(0, 6))), rating, text, country])
    rows.sort(key=lambda x: (x[0], x[3], x[4] or ""))
    for row in rows:
        ws.append(row)
    for c in ws[1]:
        c.font = Font(bold=True)
    ws.column_dimensions["A"].width = 12
    ws.column_dimensions["E"].width = 60
    for row in ws.iter_rows(min_row=2):
        row[0].number_format = "yyyy-mm-dd"
    wb.save(path)


def write_docs(out, w):
    write_slo(os.path.join(out, K.FILES["slo"]))
    write_catalogue(os.path.join(out, K.FILES["catalogue"]))
    write_capacity(os.path.join(out, K.FILES["capacity"]), w)
    write_feedback(os.path.join(out, K.FILES["feedback"]))
