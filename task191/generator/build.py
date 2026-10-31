"""Build task191's pack under target/ from the simulation, deterministically.

    python3 task191/generator/build.py
"""
import datetime as dt
import os
import shutil
import sys

from openpyxl import Workbook
from openpyxl.styles import Font

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs                     # noqa: E402
import sim                      # noqa: E402
import sim_asks                 # noqa: E402
from common import (TARGET, TZ, UTC, days, iso_z, normalise_zip, rng, set_mtime, write_csv)   # noqa: E402
from world import DEPOTS, DEPOT_NAME, NIGHT, day_type, route_depot, to_latlon     # noqa: E402

FILES = {
    "warnings": "adas_collision_warnings_2025-10_2026-10.csv",
    "codes": "fleetview_customer_bulletin_cb-2026-04.pdf",
    "fleet": "fleet_register_2026.xlsx",
    "network": "red_paradas_recorridos_2025_2026.xlsx",
    "return": "service_return_2025-10_2026-10.csv",
    "terms": "driver_attention_programme_2027_terms.pdf",
    "notice": "red2026_service_notice.pdf",
    "etm": "etm_logons_2026-10.csv",
    "hr": "hr_depot_assignments_2026.csv",
    "payroll": "hr_hours_on_service_note.txt",
    "incidents": "incident_register_2026.xlsx",
    "bordereau": "insurer_bordereau_2026-01_2026-10.csv",
    "insurance": "broker_reporting_notes_2027_renewal.pdf",
    "diversions": "mobility_diversions_register_2026.csv",
    "annex": "contract_annex_iv_kilometres.pdf",
    "absence": "depot_absence_overtime_2026.xlsx",
    "boardings": "boardings_by_line_2026.csv",
}
VDO_LINES = {"40", "41", "44", "46"}
METRES_FROM = dt.date(2026, 7, 1)          # the new scheduling module writes these lines' kilometres in metres
FW1, FW2 = "1.9.4", "2.3.1"


def wb_save(wb, path):
    wb.save(path)
    normalise_zip(path)


def header(ws, cols):
    ws.append(cols)
    for c in ws[1]:
        c.font = Font(bold=True)


# ---------------------------------------------------------------- warnings
def write_warnings(w):
    r = rng("export")
    rows = []
    counter = {}
    for e in w.events:
        loc = e["utc"].astimezone(TZ)
        if loc.date() < sim.EXTRACT_FROM or loc.date() > sim.LAST_DAY:
            continue
        counter[e["bus"]] = counter.get(e["bus"], 0) + 1
        fw2 = w.fleet.fw2[e["bus"]]
        v2 = fw2 is not None and loc.date() >= fw2
        lat, lon = to_latlon(e["x"], e["y"])
        wt = e["wtype"]
        if v2:
            wt = {"FCW": "FWD_COLL", "PCW": "PED_COLL", "LDW": "LANE_DEP", "HMW": "HEADWAY"}[wt]
            b2 = ""
            ms = "" if e["react_ms"] is None else str(e["react_ms"])
            if e["braked"]:
                ms = str(e["react_ms"])
        else:
            b2 = "Y" if e["braked"] else "N"
            ms = ""
        delay = float(r.uniform(2, 40))
        if r.random() < 0.03:
            delay += float(r.uniform(300, 5400))          # held in the vehicle until the link came back
        recv = e["utc"] + dt.timedelta(seconds=delay)
        ev_id = "%s-%06d" % (e["bus"], 10000 + counter[e["bus"]] * 3 + int(r.integers(0, 3)))
        e["event_id"] = ev_id
        base = [ev_id, e["bus"], iso_z(e["utc"]), recv, "%.6f" % lat, "%.6f" % lon, "%.1f" % e["speed"], wt, b2, ms,
                FW2 if v2 else FW1]
        rows.append(base)
        if r.random() < 0.014:
            again = list(base)
            again[3] = recv + dt.timedelta(seconds=float(r.uniform(180, 4200)))
            rows.append(again)
    rows.sort(key=lambda x: (x[3], x[0]))
    out = []
    for i, x in enumerate(rows):
        out.append(["%09d" % (512000017 + i * 7)] + [x[0], x[1], x[2], iso_z(x[3])] + x[4:])
    write_csv(os.path.join(TARGET, FILES["warnings"]),
              ["message_id", "event_id", "fleet_no", "event_time_utc", "received_time_utc", "latitude", "longitude",
               "speed_kmh", "warning_type", "brake_2s", "brake_reaction_ms", "firmware"], out)
    return len(out)


# ---------------------------------------------------------------- fleet and network
def write_fleet(w):
    wb = Workbook()
    ws = wb.active
    ws.title = "Fleet"
    header(ws, ["fleet_no", "model", "camera_firmware_2x_from"])
    for b in w.fleet.buses:
        f2 = w.fleet.fw2[b]
        ws.append([int(b), w.fleet.model[b], f2.strftime("%d/%m/%Y") if f2 else ""])
    ws2 = wb.create_sheet("Allocations")
    header(ws2, ["fleet_no", "depot", "from", "to"])
    for b in w.fleet.buses:
        for a, e, d in w.fleet.alloc[b]:
            ws2.append([int(b), DEPOT_NAME[d], a.strftime("%d/%m/%Y"), "" if e.year == 2099 else e.strftime("%d/%m/%Y")])
    ws3 = wb.create_sheet("Registrations")
    header(ws3, ["fleet_no", "plate", "from", "to"])
    for b in w.fleet.buses:
        for a, e, p in w.fleet.plates[b]:
            ws3.append([int(b), p, a.strftime("%d/%m/%Y"), "" if e.year == 2099 else e.strftime("%d/%m/%Y")])
    wb_save(wb, os.path.join(TARGET, FILES["fleet"]))


def write_network(w):
    net = w.net
    wb = Workbook()
    ws = wb.active
    ws.title = "Paradas"
    header(ws, ["codigo_2026", "codigo_2025", "nombre", "latitud", "longitud"])
    for k in sorted(net.stops, key=lambda k: net.stops[k].code26):
        s = net.stops[k]
        lat, lon = to_latlon(s.x, s.y)
        ws.append([s.code26, s.code25 or "", s.name, round(lat, 6), round(lon, 6)])
    ws2 = wb.create_sheet("Recorridos Red 2026")
    header(ws2, ["linea", "sentido", "orden", "codigo_parada", "vigente_desde", "vigente_hasta"])
    ws3 = wb.create_sheet("Recorridos Red 2025")
    header(ws3, ["linea", "sentido", "orden", "codigo_parada", "vigente_hasta"])
    from world import ROUTES
    order = [rt for d, _ in DEPOTS for rt in ROUTES[d]] + sorted(NIGHT)
    for route in order:
        for dr in ("IDA", "VUELTA"):
            for a, b, seq in net.seq[(route, dr)]:
                if b >= sim.NETWORK_2026:
                    frm = max(a, sim.NETWORK_2026)
                    for i, k in enumerate(seq):
                        ws2.append([route, dr, i + 1, net.stops[k].code26, frm.strftime("%d/%m/%Y"),
                                    "" if b.year == 2099 else b.strftime("%d/%m/%Y")])
                if a < sim.NETWORK_2026:
                    for i, k in enumerate(seq):
                        ws3.append([route, dr, i + 1, net.stops[k].code25, "13/12/2025"])
    wb_save(wb, os.path.join(TARGET, FILES["network"]))


def write_return(w):
    rows = []
    for day in days(sim.EXTRACT_FROM, dt.date(2026, 10, 31)):
        for route in sim.all_routes():
            for dr in ("IDA", "VUELTA"):
                n = w.scheduled.get((day, route, dr), 0)
                if n == 0:
                    continue
                op = len(w.trips.get((day, route, dr), []))
                km = op * round(w.net.route_km(route, dr, day), 1)
                dep = route_depot(route, day)
                centre = DEPOT_NAME["QUI"] if route == "25" else DEPOT_NAME[dep]
                if route in VDO_LINES and day >= METRES_FROM:
                    kmv = "%d" % round(km * 1000)
                else:
                    kmv = "%.1f" % km
                rows.append([day.strftime("%d/%m/%Y"), route, dr, centre, n, op, kmv])
    write_csv(os.path.join(TARGET, FILES["return"]),
              ["fecha", "linea", "sentido", "centro", "expediciones_programadas", "expediciones_realizadas",
               "km_realizados"], rows, delimiter=";")
    return len(rows)


# ---------------------------------------------------------------- ETM and HR
def write_etm(w, emp, assign):
    sess = sim_asks.etm_sessions(w, emp, assign)
    r = rng("etm_export")
    rows = []
    sid = 7_300_000
    for s in sess:
        if not (sim_asks.OCT0 - dt.timedelta(days=1) <= s["on"].date() <= sim_asks.OCT1):
            continue
        sid += int(r.integers(1, 4))
        s["sid"] = sid
        line = s["route"]
        row = [sid, int(s["fleet"]), s["emp"], line, s["on"].strftime("%Y-%m-%d %H:%M:%S"),
               s["off"].strftime("%Y-%m-%d %H:%M:%S")]
        rows.append(row)
        if r.random() < 0.008:
            rows.append(list(row))
    write_csv(os.path.join(TARGET, FILES["etm"]),
              ["sesion", "coche", "empleado", "linea", "inicio_local", "fin_local"], rows, delimiter=";")
    return sess


def write_hr(emp, assign):
    rows = []
    for e in emp:
        for a, b, d in assign[e]:
            rows.append([e, DEPOT_NAME[d], a.strftime("%d/%m/%Y"), "" if b.year == 2099 else b.strftime("%d/%m/%Y")])
    write_csv(os.path.join(TARGET, FILES["hr"]), ["empleado", "cochera", "desde", "hasta"], rows, delimiter=";")


# ---------------------------------------------------------------- incidents and claims
def write_incidents(w, inc, claims, dups):
    r = rng("incident_export")
    reports = []
    for i, x in enumerate(inc):
        reports.append(dict(x, src="Conductor", idx=i))
    for y in dups:
        reports.append(dict(y, src="Inspector", idx=y["dup_of"]))
    reports.sort(key=lambda x: (x["t"], x["fleet"], x["src"]))
    wb = Workbook()
    ws = wb.active
    ws.title = "Partes 2026"
    header(ws, ["parte", "fecha", "hora_local", "coche", "lugar", "tipo", "culpa", "comunicado_por"])
    n_pd = n_in = 0
    for x in reports:
        if x["src"] == "Conductor":
            n_pd += 1
            ref = "PD-26-%04d" % (n_pd * 3 + 101)
            place = "%s %d" % (x["street"], x["num"])
        else:
            n_in += 1
            ref = "IN-26-%04d" % (n_in * 7 + 55)
            place = "%s, frente al nº %d" % (x["street"].replace("Calle ", "C/ ").replace("Avenida ", "Avda. "), x["num"])
        ws.append([ref, x["t"].strftime("%d/%m/%Y"), x["t"].strftime("%H:%M"), int(x["fleet"]), place, x["kind"],
                   x["fault"], x["src"]])
    wb_save(wb, os.path.join(TARGET, FILES["incidents"]))
    # The insurer's month-end bordereau.
    snaps = [dt.date(2026, m + 1, 1) - dt.timedelta(days=1) for m in range(1, 10)] + [dt.date(2026, 10, 31)]
    sched = {}
    for c in claims:
        k = int(r.integers(1, 4))
        lag = sorted(int(v) for v in r.integers(5, 120, k))
        parts = r.dirichlet([2.0] * k)
        sched[c["no"]] = [(c["notified"] + dt.timedelta(days=lg), round(c["total"] * float(p), 2))
                          for lg, p in zip(lag, parts)]
    by_no = {c["no"]: c for c in claims}
    rows = []
    for snap in snaps:
        for c in claims:
            if c["notified"] > snap:
                continue
            x = inc[c["inc"]]
            paid = round(sum(a for d, a in sched[c["no"]] if d <= snap), 2)
            full = round(sum(a for _, a in sched[c["no"]]), 2)
            carried = 0.0
            if c["reopen"]:
                carried = round(sum(a for _, a in sched[c["reopen"]]), 2)
            closed = all(d <= snap for d, _ in sched[c["no"]])
            # A claim reopened later still shows its own payments; the reopening claim carries them forward.
            status = "CLOSED" if closed else ("REOPENED" if c["reopen"] else "OPEN")
            reserve = 0.0 if closed else round(max(full - paid, 0) * 1.15, 2)
            plate = w.fleet.plate_on(x["fleet"], c["notified"])
            ctype = "OD" if x["fault"] == "N" else ("TP_INJ" if x["kind"] == "Contacto con peatón" else "TP_PROP")
            itime = (x["t"] + dt.timedelta(minutes=int(r.integers(-6, 7)))).strftime("%H:%M")
            rows.append([snap.strftime("%Y-%m-%d"), c["no"], c["reopen"] or "", x["day"].strftime("%Y-%m-%d"), itime,
                         plate, ctype, status, "%.2f" % (paid + carried), "%.2f" % reserve])
    write_csv(os.path.join(TARGET, FILES["bordereau"]),
              ["snapshot", "claim_no", "reopened_from", "incident_date", "incident_time_local", "vehicle_plate", "claim_type",
               "status", "paid_to_date_eur", "reserve_eur"], rows)
    return sched


def write_diversions(dvs):
    rows = []
    for d in dvs:
        rows.append([d["id"], "/".join(d["routes"]), "/".join(d["dirs"]), d["start"].strftime("%d/%m/%Y"),
                     d["end"].strftime("%d/%m/%Y"), ("%+.1f" % d["km"]).replace(".", ","), d["reason"]])
    write_csv(os.path.join(TARGET, FILES["diversions"]),
              ["desvio", "lineas", "sentidos", "desde", "hasta", "km_por_expedicion", "motivo"], rows, delimiter=";")


# ---------------------------------------------------------------- distractors
def write_distractors(w):
    r = rng("distractors")
    wb = Workbook()
    ws = wb.active
    ws.title = "2026"
    header(ws, ["cochera", "mes", "conductores_plantilla", "dias_baja", "horas_extra"])
    for dep, name in DEPOTS:
        for m in range(1, 11):
            staff = 128 if dep not in ("QUI", "TEN") else 118
            ws.append([name, "%04d-%02d" % (2026, m), staff, int(r.integers(90, 260)), int(r.integers(300, 1400))])
    wb_save(wb, os.path.join(TARGET, FILES["absence"]))
    rows = []
    for route in sim.all_routes():
        for m in range(1, 11):
            base = 9000 if route in NIGHT else 52000
            rows.append([route, "%04d-%02d" % (2026, m), int(base * float(r.uniform(0.7, 1.3)))])
    write_csv(os.path.join(TARGET, FILES["boardings"]), ["linea", "mes", "viajeros"], rows, delimiter=";")


def build():
    if os.path.isdir(TARGET):
        shutil.rmtree(TARGET)
    os.makedirs(TARGET)
    w = sim.World()
    n_warn = write_warnings(w)
    write_fleet(w)
    write_network(w)
    n_ret = write_return(w)
    emp, assign, moved = sim_asks.staff(w)
    sess = write_etm(w, emp, assign)
    write_hr(emp, assign)
    inc, claims, dups = sim_asks.incidents(w)
    write_incidents(w, inc, claims, dups)
    write_diversions(sim_asks.diversions())
    write_distractors(w)
    docs.terms_pdf(os.path.join(TARGET, FILES["terms"]))
    docs.codes_pdf(os.path.join(TARGET, FILES["codes"]))
    docs.notice_pdf(os.path.join(TARGET, FILES["notice"]))
    docs.payroll_txt(os.path.join(TARGET, FILES["payroll"]))
    docs.insurance_pdf(os.path.join(TARGET, FILES["insurance"]))
    docs.annex_pdf(os.path.join(TARGET, FILES["annex"]))
    for n in os.listdir(TARGET):
        set_mtime(os.path.join(TARGET, n))
    print("built target/: %d files, %d warning rows, %d return rows, %d sessions" %
          (len(os.listdir(TARGET)), n_warn, n_ret, len(sess)))
    return w


if __name__ == "__main__":
    build()
