"""Writes the pack under target/ from the clean truth, with the operator's and the concessionaire's own export
conventions (Layer 1)."""
import datetime as dt
import os
import random

import io_util as IO
import params as P
import world as W

FILES = {
    "journeys": "RVB_metro_ritten_20261001_20261104.csv",
    "network": "RVB_metronet_planningsmodel_2026.xlsx",
    "products": "RVB_productcodes.csv",
    "rate_card": "Spoorbeeld_tariefkaart_2027.pdf",
    "terms": "Spoorbeeld_algemene_voorwaarden_2026.pdf",
    "register": "schermregister_2026-11-12.xlsx",
    "cms": "cms_player_status_20261001_20261104.csv",
    "bookings": "boekingen_najaar_2026.xlsx",
    "legacy": "facturen_oud_systeem_2026.csv",
    "billing": "billing_export_2026-10-15_2026-11-12.xlsx",
    "statements": "bureaucommissie_najaar_2026.pdf",
    "ridership": "RVB_instappers_per_halte_2026.xlsx",
    "survey": "reizigersonderzoek_2026_q3.xlsx",
    "benchmark": "ooh_benchmark_2026.pdf",
}
DISTRACTORS = ["ridership", "survey", "benchmark"]
UPDATED_STOPS = ("CEN", "KST", "GHP", "OSP")      # gate firmware updated on 19 October 2026
FIRMWARE_DAY = dt.date(2026, 10, 19)
XMETA_RVB = ("Datawarehouse RVB", "Daphne Riem", "2026-11-05T07:14:00Z", "2026-11-05T07:14:00Z")
XMETA_SB = ("Brent Velderman", "Brent Velderman", "2026-11-12T16:02:00Z", "2026-11-12T16:40:00Z")


def hhmmss(minutes):
    s = int(round(minutes * 60))
    s %= 24 * 3600
    return "%02d:%02d:%02d" % (s // 3600, (s // 60) % 60, s % 60)


GATES_IN_HALL = {"CEN-HN": 12, "CEN-HZ": 9}


def device_code(rng, hall, day):
    stop = hall.split("-")[0]
    h = hall.split("-")[1]
    n = rng.randint(1, GATES_IN_HALL.get(hall, 3 + sum(ord(c) * (i + 1) for i, c in enumerate(stop)) % 6))
    if stop in UPDATED_STOPS and day >= FIRMWARE_DAY:
        return "%s.%s.%02d" % (stop, h, n), (stop, h, n)
    tag = {"H": "", "HN": "N", "HZ": "Z"}[h]
    return "PZ-%s-%s%02d" % (stop, tag, n), (stop, h, n)


def stop_name(net, code, day):
    nm = net.st[code]["name"]
    if code in UPDATED_STOPS and day >= FIRMWARE_DAY:
        return "Ravelmond " + nm if code == "CEN" else "%s (Ravelmond)" % nm
    return nm


def fare(net, j):
    if j["product"] in ("MND", "PER", "SRV"):
        return "0.00"
    if not j["checked_out"]:
        return "4.00"
    legs = net.line_map_route(j["o"], j["d"])
    stops = sum(abs(net.pos[ln][b] - net.pos[ln][a]) for ln, a, b in legs)
    f = 1.08 + 0.172 * stops
    if j["product"] in ("STU", "OUD"):
        f *= 0.6 if j["product"] == "OUD" else 1.0
    return "%.2f" % f


def write_journeys(w, path, rng):
    net = w.net
    rows = []
    devices = {}
    for j in w.journeys:
        din, kin = device_code(rng, j["h_in"], j["day"])
        devices[din] = j["h_in"]
        t_out = j["t_in"] + j["dur"]
        if j["checked_out"]:
            out_day = j["day"] + dt.timedelta(days=int(t_out // 1440))
            dout, kout = device_code(rng, j["h_out"], out_day)
            devices[dout] = j["h_out"]
            co = [hhmmss(t_out), j["d"], stop_name(net, j["d"], out_day), dout]
        else:
            co = ["", "", "", ""]
        rows.append([j["card"], j["product"], j["day"].isoformat(), hhmmss(j["t_in"]), j["o"],
                     stop_name(net, j["o"], j["day"]), din] + co + [fare(net, j)])
    header = ["card_id", "product_code", "travel_date", "check_in_time", "check_in_stop", "check_in_stop_name",
              "check_in_gate", "check_out_time", "check_out_stop", "check_out_stop_name", "check_out_gate",
              "fare_eur"]
    n = IO.write_csv(path, header, rows)
    return n, devices


def write_network(w, path, devices):
    net = w.net
    stops = []
    for c, nm, br in P.STATIONS:
        stops.append([c, nm, ";".join(net.lines_of[c]), {"P": "1998", "W": "1983", "E": "1983"}.get(br, "1979")])
    runs = []
    for ln, seq in P.LINES.items():
        for a, b in zip(seq, seq[1:]):
            runs.append([ln, a, b, net.run[(ln, a, b)]])
    halls = []
    for h in sorted(net.halls):
        v = net.halls[h]
        halls.append([h, v["station"], v["name"], v["walk"].get("M1", ""), v["walk"].get("M2", ""),
                      v["walk"].get("M3", "")])
    inter = []
    for c, lines in sorted(P.INTERCHANGES.items()):
        inter.append([c, c + "-OV", "Overstap " + net.st[c]["name"], "/".join(lines), P.PASSAGE_WALK[c]])
    gates = []
    for d in sorted(devices):
        h = devices[d]
        new = "." in d
        gates.append([d, h, FIRMWARE_DAY.isoformat() if new else "2014-06-02",
                      "" if (new or h.split("-")[0] not in UPDATED_STOPS) else (FIRMWARE_DAY - dt.timedelta(days=1)).isoformat()])
    freq = []
    for ln in ("M1", "M2"):
        for a, b, h in P.WEEKDAY_BANDS:
            freq.append([ln, "ma-vr", hhmmss(a)[:5], hhmmss(b)[:5], round(60.0 / h, 1)])
        for a, b, h in P.SAT_BANDS:
            freq.append([ln, "za", hhmmss(a)[:5], hhmmss(b)[:5], round(60.0 / h, 1)])
        for a, b, h in P.SUN_BANDS:
            freq.append([ln, "zo", hhmmss(a)[:5], hhmmss(b)[:5], round(60.0 / h, 1)])
    for dtp, bands in (("ma-vr", [(345, 390, 7.5), (390, 600, 5.0), (600, 930, 7.5), (930, 1140, 5.0),
                                  (1140, 1320, 7.5), (1320, 1470, 10.0)]),
                       ("za", [(390, 1470, 10.0)]), ("zo", [(420, 1470, 10.0)])):
        for a, b, h in bands:
            freq.append(["M3", dtp, hhmmss(a)[:5], hhmmss(b)[:5], round(60.0 / h, 1)])
    IO.write_xlsx(path, [
        ("Stops", ["stop_code", "stop_name", "lines", "in_service_since"], stops, None),
        ("Run times", ["line", "from_stop", "to_stop", "run_min"], runs, None),
        ("Halls", ["hall_code", "stop_code", "hall_name", "walk_to_M1_min", "walk_to_M2_min", "walk_to_M3_min"],
         halls, None),
        ("Interchanges", ["stop_code", "passage_code", "passage_name", "lines", "walk_min"], inter, None),
        ("Gates", ["gate_code", "hall_code", "in_use_from", "in_use_to"], gates, None),
        ("Frequencies", ["line", "days", "from", "to", "trains_per_hour"], freq, None),
    ], XMETA_RVB[:2] + XMETA_RVB[2:] + ("Planningsmodel metronet 2026", "Ravelmondse Vervoerbedrijf"))
    return len(runs)


def build_pack(w, target):
    os.makedirs(target, exist_ok=True)
    rng = random.Random(P.SEED * 10 + 5)
    n = {}
    n["journeys"], devices = write_journeys(w, os.path.join(target, FILES["journeys"]), rng)
    n["network"] = write_network(w, os.path.join(target, FILES["network"]), devices)
    IO.write_csv(os.path.join(target, FILES["products"]), ["product_code", "product", "card_class"],
                 [[k, v, {"PER": "personeel", "SRV": "service"}.get(k, "reiziger")] for k, v in W.PRODUCTS.items()])
    n["products"] = len(W.PRODUCTS)
    return n


# ---------------------------------------------------------------- documents
RC_CREATED = "D:20261110094500+01'00'"
RC_MOD = "D:20261110094500+01'00'"


def annex_rows(net):
    rows = [["Package", "Code", "Halls and interchange passages"]]
    for code in P.PACKAGE_ORDER:
        name, locs = P.PACKAGES[code]
        parts = []
        for l in locs:
            if l.endswith("-OV"):
                parts.append("%s (Overstap %s)" % (l, net.st[l[:3]]["name"]))
            elif l.startswith("CEN-"):
                parts.append("%s (Centraal %s)" % (l, net.halls[l]["name"]))
            else:
                parts.append("%s (%s, stationshal)" % (l, net.st[l[:3]]["name"]))
        rows.append([name, code, "; ".join(parts)])
    return rows


PRICE = {"CEN": 268, "BNS": 181, "OVP": 244, "NRD": 146, "OST": 157, "WST": 122, "ZDT": 151, "RNG": 112, "EIN": 131}


def write_rate_card(w, path):
    net = w.net
    blocks = [
        ("t", "Tariefkaart 2027 · Metro Ravelmond"),
        ("s", "Spoorbeeld Media B.V. · concessie reclame metro Ravelmond (RVB) · versie 1.0, vastgesteld door de "
              "commercieel directeur op 10 november 2026 · eigenaar: afdeling Sales"),
        ("h", "1. Packages"),
        ("p", "Spoorbeeld Media sells the digital screens of the Ravelmond metro in packages. A package is the set of "
              "station halls and interchange passages listed for it in Annex A; a booking buys one slot in the "
              "loop on every screen the package has in those places, for whole weeks from Monday to Sunday."),
        ("h", "2. Prices 2027"),
        ("p", "Prices are per screen per week, excluding VAT. Tier G carries a surcharge of 22 per cent on the "
              "package price. Bookings placed by a recognised agency carry the agency commission agreed in that "
              "agency's own contract; the standard commission is 15 per cent."),
        ("table", [["Package", "Code", "EUR per screen-week"]] +
         [[P.PACKAGES[c][0], c, "%d" % PRICE[c]] for c in P.PACKAGE_ORDER]),
        ("h", "3. Tier G (guaranteed reach)"),
        ("p", "3.1 From 1 January 2027 a package is sold in Tier G, with a guaranteed reach, when its effective reach "
              "in the audience window is 40 per cent or more."),
        ("p", "3.2 The audience window is the four weeks from Monday 5 October to Sunday 1 November 2026, measured on "
              "the operator's OV-chipkaart journeys on the metro."),
        ("p", "3.3 A regular rider is a passenger card, not a staff or service card, with at least one metro journey "
              "in each of the window's four calendar weeks (Monday to Sunday). A journey counts on the date of its "
              "check-in."),
        ("p", "3.4 A journey passes a package's screens each time it takes the rider through a hall or interchange "
              "passage listed for the package in Annex A: the hall where the journey is checked in, the hall where "
              "it is checked out, and the interchange passage of any station where the rider changes trains on the "
              "way. A journey without a check-out passes the hall where it was checked in and nothing else."),
        ("p", "3.5 A package's effective reach is the share of regular riders whose journeys in the window passed its "
              "screens three times or more."),
        ("p", "3.6 Tier G packages carry a reach guarantee for 2027 bookings; shortfalls are made good in kind under "
              "the general terms."),
        ("h", "Annex A. Package composition 2027"),
        ("table", annex_rows(net)),
    ]
    IO.write_pdf(path, "Tariefkaart 2027 Metro Ravelmond", "Spoorbeeld Media B.V.", "Spoorbeeld Media B.V.",
                 blocks, "Spoorbeeld Media B.V. · Tariefkaart 2027 · versie 1.0", RC_CREATED, RC_MOD,
                 colw={3: [100, 40, 330]})


def write_terms(path):
    blocks = [
        ("t", "Algemene voorwaarden 2026 · schermreclame metro Ravelmond"),
        ("s", "Spoorbeeld Media B.V. · geldig voor boekingen met looptijd in 2026 · gedeponeerd 2 januari 2026"),
        ("h", "Article 6. Delivery and make-good"),
        ("p", "6.1 The booked screen-hours of a booking are its booked screens times the station opening hours on each "
              "day of the flight: Monday to Friday 05:45 to 00:30, Saturday 06:30 to 00:30 and Sunday 07:00 to 00:30, "
              "local time in Ravelmond."),
        ("p", "6.2 A booked screen is dark while the media player it is connected to is offline in the content "
              "management system, and while the screen is not hanging in its place."),
        ("p", "6.3 Dark hours above 0.5 per cent of a booking's booked screen-hours are made good in kind in the first "
              "quarter of the following year, in whole hours; part of an hour counts as an hour."),
        ("h", "Article 8. Invoicing and agency commission"),
        ("p", "8.1 Bookings are invoiced on confirmation. A credit note reverses all or part of one invoice."),
        ("p", "8.2 Agency commission is due to the placing agency on the value invoiced for its bookings excluding VAT, "
              "net of credit notes, at the rate in the agency's contract, and is settled on the agency's own "
              "statement."),
        ("p", "8.3 The net revenue of a booking is the value invoiced for it excluding VAT, less any credit note "
              "issued against its invoice, less the agency commission due on it."),
    ]
    IO.write_pdf(path, "Algemene voorwaarden 2026", "Spoorbeeld Media B.V.", "Spoorbeeld Media B.V.", blocks,
                 "Spoorbeeld Media B.V. · Algemene voorwaarden 2026", "D:20260102100000+01'00'",
                 "D:20260102100000+01'00'")


def fmt_dt(x):
    return x.strftime("%Y-%m-%d %H:%M") if x else ""


def write_register(w, path):
    A = w.asks
    import asks_world as AW
    rows = AW.register_rows(A)
    screens = [[r["tag"], r["loc"], r["pos"], r["pkg"], r["hung"].isoformat(),
                r["down"].isoformat() if r["down"] else "", r["status"]]
               for r in sorted(rows, key=lambda r: (r["loc"], r["pos"], r["hung"], r["tag"]))]
    players = [[p, loc, "2023-03-01"] for p, loc in sorted(A.players.items())]
    cab = [[t, p, fmt_dt(a), fmt_dt(b)] for t, p, a, b in sorted(A.cabling_register, key=lambda c: (c[0], c[2]))]
    IO.write_xlsx(path, [
        ("Schermen", ["asset_tag", "location_code", "position", "package", "hung", "taken_down", "status"], screens,
         None),
        ("Players", ["player_id", "location_code", "installed"], players, None),
        ("Bekabeling", ["asset_tag", "player_id", "connected_from", "connected_to"], cab, None),
    ], XMETA_SB + ("Schermregister metro", "Spoorbeeld Media B.V."))
    return len(screens)


def write_cms(w, path):
    import asks_world as AW
    A = w.asks
    rows = []
    t_end = dt.datetime.combine(P.EXTRACT_END + dt.timedelta(days=1), dt.time(0, 0))
    for when, p, ev, k in A.cms:
        if when >= t_end:
            continue
        rows.append([p, ev, k, AW.to_utc(when).strftime("%Y-%m-%dT%H:%M:00Z")])
    rows.sort(key=lambda r: (r[3], r[0], r[1]))
    return IO.write_csv(path, ["player_id", "event", "displays", "event_time_utc"], rows)


def write_bookings(w, path):
    A = w.asks
    bk = [[b["ref"], b["advertiser"], b["agency"] or "", P.PACKAGES[b["package"]][0], b["start"].isoformat(),
           b["end"].isoformat(), "%.2f" % b["booked_hours"], "%.2f" % b["net_value"]] for b in A.bookings]
    lines = [[b["ref"], t] for b in A.bookings for t in b["tags"]]
    IO.write_xlsx(path, [
        ("Boekingen", ["booking_ref", "advertiser", "agency", "package", "flight_start", "flight_end",
                       "booked_screen_hours", "net_value_eur"], bk, None),
        ("Geboekte schermen", ["booking_ref", "asset_tag"], lines, None),
    ], ("Evie Hondeveld", "Evie Hondeveld", "2026-10-02T09:10:00Z", "2026-10-21T13:55:00Z",
        "Boekingen najaar 2026", "Spoorbeeld Media B.V."))
    return len(bk)


def nl_money(x):
    s = "%.2f" % x
    whole, frac = s.split(".")
    neg = whole.startswith("-")
    whole = whole.lstrip("-")
    parts = []
    while len(whole) > 3:
        parts.insert(0, whole[-3:])
        whole = whole[:-3]
    parts.insert(0, whole)
    return ("-" if neg else "") + ".".join(parts) + "," + frac


def write_legacy(w, path):
    A = w.asks
    rows = [[r["no"], r["date"].strftime("%d-%m-%Y"), r["ref"], r["debtor"], nl_money(r["gross"])] for r in A.legacy]
    return IO.write_csv(path, ["factuurnummer", "factuurdatum", "boekingsnummer", "debiteur", "bedrag_incl_btw"],
                        rows, delimiter=";")


def write_billing(w, path):
    A = w.asks
    rows = []
    for r in A.new_invoices:
        rows.append([r["no"], r["date"].isoformat(), "invoice", r["ref"], r["debtor"], r["net"], r["vat"], "",
                     "Schermreclame %s" % r["ref"]])
    for r in A.credits:
        rows.append([r["no"], r["date"].isoformat(), "credit note", "", r["debtor"], r["net"], r["vat"],
                     r["reference"], r["why"]])
    rows.sort(key=lambda r: (r[1], r[0]))
    IO.write_xlsx(path, [("Documents", ["document_no", "document_date", "document_type", "booking_ref", "debtor",
                                        "net_eur", "vat_eur", "reference", "description"], rows, None)],
                  ("Finance Spoorbeeld", "Finance Spoorbeeld", "2026-11-12T17:05:00Z", "2026-11-12T17:05:00Z",
                   "Billing export", "Spoorbeeld Media B.V."))
    return len(rows)


def write_statements(w, path):
    A = w.asks
    blocks = []
    for s in A.statements:
        refs = ", ".join(b["ref"] for b in A.bookings if b["agency"] == s["agency"])
        blocks += [("t", "%s · Commissienota" % s["agency"]),
                   ("s", "Aan: Spoorbeeld Media B.V., crediteurenadministratie · datum 31 oktober 2026"),
                   ("p", "Betreft: bureaucommissie op uw najaarsboekingen 2026 (%s), conform ons raamcontract." % refs),
                   ("table", [["Omschrijving", "Bedrag (EUR)"],
                              ["Commissie najaarsboekingen 2026", nl_money(s["commission"])]]),
                   ("s", "Gelieve het bedrag binnen 30 dagen te voldoen onder vermelding van het notanummer.")]
    IO.write_pdf(path, "Commissienota's najaar 2026", "Crediteurenadministratie", "Spoorbeeld Media B.V.",
                 blocks, "Ontvangen commissienota's · gescand 3 november 2026", "D:20261103111200+01'00'",
                 "D:20261103111200+01'00'", colw={2: [300, 120]})


def write_distractors(w, target, rng):
    net = w.net
    # the operator's published boarding figures by stop and month (January to September 2026)
    rows = []
    for c, nm, br in P.STATIONS:
        base = rng.uniform(38000, 260000) * (2.6 if c == "CEN" else 1.0)
        for m in range(1, 10):
            season = {7: 0.78, 8: 0.81, 1: 0.94, 12: 0.97}.get(m, 1.0)
            rows.append([c, nm, "2026-%02d" % m, int(base * season * rng.uniform(0.95, 1.05))])
    IO.write_xlsx(os.path.join(target, FILES["ridership"]),
                  [("Instappers", ["stop_code", "stop_name", "month", "check_ins"], rows,
                    ["RVB Informatievoorziening · maandelijkse instappers metro per halte, gepubliceerd "
                     "op ravelmondsevervoerbedrijf.nl · stand 14 oktober 2026"])],
                  ("RVB Informatievoorziening", "RVB Informatievoorziening", "2026-10-14T08:00:00Z",
                   "2026-10-14T08:00:00Z", "Instappers per halte 2026", "Ravelmondse Vervoerbedrijf"))
    # the operator's passenger survey, third quarter 2026
    srows = []
    for c, nm, br in P.STATIONS:
        srows.append([c, nm, int(rng.uniform(55, 240)), round(rng.uniform(6.4, 8.1), 1), round(rng.uniform(5.6, 7.9), 1),
                      round(rng.uniform(1.5, 7.5), 1), round(rng.uniform(18, 46), 0)])
    IO.write_xlsx(os.path.join(target, FILES["survey"]),
                  [("Q3 2026", ["stop_code", "stop_name", "respondents", "score_overall", "score_cleanliness",
                                "avg_wait_reported_min", "pct_notice_screens"], srows,
                    ["Reizigersonderzoek metro Ravelmond, derde kwartaal 2026 (veldwerk 1 juli tot 30 september), "
                     "steekproef op het perron"])],
                  ("Onderzoeksbureau Peilstok", "Onderzoeksbureau Peilstok", "2026-10-09T12:00:00Z",
                   "2026-10-09T12:00:00Z", "Reizigersonderzoek Q3 2026", "Onderzoeksbureau Peilstok"))
    blocks = [("t", "OOH-benchmark 2026: digitale schermen in OV-knooppunten"),
              ("s", "Brancheoverzicht · Stichting Buitenreclame Benchmark · september 2026"),
              ("p", "The benchmark collects published rate cards and audited contacts of digital transit screens in "
                    "six Dutch cities. Net prices per thousand contacts in 2026 ranged from 4.10 to 9.80 euro; screens "
                    "in interchange passages fetched the highest prices per screen and the lowest per contact."),
              ("table", [["City network", "Screens", "Median EUR per screen-week", "EUR per 1,000 contacts"],
                         ["Network A", "412", "212", "6.40"], ["Network B", "186", "158", "7.95"],
                         ["Network C", "97", "131", "9.80"], ["Network D", "264", "174", "5.75"],
                         ["Network E", "140", "149", "4.10"], ["Network F", "75", "118", "8.60"]]),
              ("p", "Contacts are counted by each network's own method and are not comparable between networks.")]
    IO.write_pdf(os.path.join(target, FILES["benchmark"]), "OOH-benchmark 2026", "Stichting Buitenreclame Benchmark",
                 "Stichting Buitenreclame Benchmark", blocks, "OOH-benchmark 2026 · vertrouwelijk voor deelnemers",
                 "D:20260918140000+02'00'", "D:20260918140000+02'00'", colw={4: [120, 70, 140, 140]})


def build_all(w, target):
    rng = random.Random(P.SEED * 10 + 5)
    n = build_pack(w, target)
    write_rate_card(w, os.path.join(target, FILES["rate_card"]))
    write_terms(os.path.join(target, FILES["terms"]))
    n["register"] = write_register(w, os.path.join(target, FILES["register"]))
    n["cms"] = write_cms(w, os.path.join(target, FILES["cms"]))
    n["bookings"] = write_bookings(w, os.path.join(target, FILES["bookings"]))
    n["legacy"] = write_legacy(w, os.path.join(target, FILES["legacy"]))
    n["billing"] = write_billing(w, os.path.join(target, FILES["billing"]))
    write_statements(w, os.path.join(target, FILES["statements"]))
    write_distractors(w, target, rng)
    stamp = dt.datetime(2026, 11, 13, 8, 20).timestamp()
    for fn in os.listdir(target):
        os.utime(os.path.join(target, fn), (stamp, stamp))
    return n
