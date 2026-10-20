"""The records the agency keeps, built on the world: the analyzers' own hourly archive December 2024 to December 2027
(downloaded at each round), the two contractors' titrations, the service log, the 2028 plan, the station register,
and the network's validated NO2 database for 2027.

Clocks. The analyzers keep UTC. The network's database and the agency's documents use solar time (UTC+1) all year.
The contractors and the service technicians write their visit times in Italy's legal time (CET, CEST in summer).

Tecnoaria (until June 2026) put the analyzer in calibration mode for every titration, so the analyzer's status and the
database marked those hours. Delta (from July 2026) titrates without the calibration mode, so its quarterly rounds go
into the archive with status 0 and into the database as valid air; at services the service technician sets
maintenance mode and the hours are marked. BP07's analyzer spent three weeks of February 2027 in the workshop with the
store spare in its place; the data system files an analyzer's hours under its registered place, so the spare's hours
at BP07 arrived under the store's code, MAG, and BP07's own as not received. Five
stations took a new data logger early in 2027, set at the factory to 0 degrees C, until a December visit set it to
20.

    R = build(W, seed)  -> dict of DataFrames and the truth behind them
"""
import datetime as dt
import zoneinfo

import numpy as np
import pandas as pd

import params as P
import sim

ROME = zoneinfo.ZoneInfo("Europe/Rome")
SOLAR = dt.timezone(dt.timedelta(hours=1))
UTC = dt.timezone.utc
H27 = int((dt.datetime(2027, 1, 1) - sim.T0).total_seconds() // 3600)     # hour index of 2027-01-01 00:00 solar
N27 = 8760
UG20 = 1.91                 # micrograms per cubic metre per ppb of NO2 at 20 degrees C and 101.3 kPa
UGL = 2.05                  # the same at 0 degrees C, the new loggers' factory setting
NEW_LOGGERS = {             # station: logger installed (solar), set to 20 degrees C (solar)
    "BP03": (dt.datetime(2027, 1, 19, 10), dt.datetime(2027, 12, 1, 10)),
    "BP06": (dt.datetime(2027, 1, 26, 11), dt.datetime(2027, 12, 2, 11)),
    "BP09": (dt.datetime(2027, 2, 2, 9), dt.datetime(2027, 12, 3, 10)),
    "BP10": (dt.datetime(2027, 2, 9, 10), dt.datetime(2027, 12, 6, 9)),
    "BP14": (dt.datetime(2027, 2, 16, 10), dt.datetime(2027, 12, 7, 12)),
    "BP15": (dt.datetime(2027, 2, 23, 11), dt.datetime(2027, 12, 9, 9)),
}
TECH_A = ["G. Ferrandi", "M. Bellotti"]
TECH_B = ["J. Stefanelli", "R. Caimi", "D. Orlandini"]
SERVICE_TECH = ["L. Pedrazzi", "S. Marcon"]
A_END = dt.date(2026, 6, 30)


def solar(h):
    return sim.T0 + dt.timedelta(hours=int(h))


def solar_to_legal(t):
    return t.replace(tzinfo=SOLAR).astimezone(ROME).replace(tzinfo=None)


def legal_to_solar(t):
    return t.replace(tzinfo=ROME).astimezone(SOLAR).replace(tzinfo=None)


def hidx(t_solar):
    return int((t_solar - sim.T0).total_seconds() // 3600)


def code_of(i):
    return sim.STATIONS[i][0]


def station_of_serial(serial):
    for i, st in enumerate(sim.STATIONS):
        if st[5] == serial:
            return i
    return None


# ------------------------------------------------------------------ visits
def _end(start, minutes):
    """a visit's end: a technician who finishes in the first quarter of an hour stays on into it (the station's
    book is signed, the shelter shut), so the end falls on the hour or 16 minutes or more into it"""
    e = start + dt.timedelta(minutes=minutes)
    if 1 <= e.minute <= 15:
        e += dt.timedelta(minutes=15)
    return e


def visits(W, seed):
    """every titration and service visit with its window in legal time: (serial, station index, kind, contractor,
    start, end, conv index, measured efficiency, true efficiency); services carry the converter change"""
    rng = np.random.default_rng(seed + 41)
    out = []
    for (k, serial, st, D, tr, m, kind, ci) in W["titrations"]:
        d = sim.day(k)
        contractor = "A" if d <= A_END else "B"
        if kind == "trimestrale":
            start = dt.datetime(d.year, d.month, d.day, int(rng.integers(8, 11)), int(rng.choice([0, 15, 30, 40])))
            dur = int(rng.integers(150, 215))
        else:
            # titrations at a service: before the change at 11:00 solar and after it, inside the service window
            start = solar_to_legal(dt.datetime(d.year, d.month, d.day, 9, 0)) + dt.timedelta(minutes=int(
                rng.integers(0, 30)))
            if kind == "dopo la sostituzione":
                start = solar_to_legal(dt.datetime(d.year, d.month, d.day, 11, 30)) + dt.timedelta(
                    minutes=int(rng.integers(0, 15)))
            dur = int(rng.integers(95, 140))
        out.append(dict(day=k, serial=serial, st=st, kind=kind, contractor=contractor, start=start,
                        end=_end(start, dur), conv=ci, eff=m, true=tr, D=D))
    return out


def service_windows(W, seed):
    """the service technician's visits: every converter change (scheduled or early), the swaps; legal time"""
    rng = np.random.default_rng(seed + 43)
    out = []
    for serial, a in W["analyzers"].items():
        for j, c in enumerate(a["converters"]):
            if j == 0:
                continue
            d = sim.day(c["installed"])
            st = int(a["where"][c["installed"] * 24 + 11])
            s0 = solar_to_legal(dt.datetime(d.year, d.month, d.day, 8, 30)) + dt.timedelta(minutes=int(
                rng.integers(0, 15)))
            out.append(dict(day=c["installed"], serial=serial, st=st, kind=c["reason"], start=s0,
                            end=_end(s0, int(rng.integers(330, 420)))))
    # the new data loggers: installed, later set to 20 degrees C; the analyzer in maintenance mode while it is rewired
    for code, (t0, t1) in NEW_LOGGERS.items():
        i = [s[0] for s in sim.STATIONS].index(code)
        serial = sim.STATIONS[i][5]
        for t, kind, dur in ((t0, "registratore", (110, 170)), (t1, "registratore 20 C", (40, 75))):
            s0 = solar_to_legal(t) + dt.timedelta(minutes=int(rng.integers(5, 25)))
            out.append(dict(day=(t.date() - P.START).days, serial=serial, st=i, kind=kind, start=s0,
                            end=_end(s0, int(rng.integers(*dur)))))
    # the analyzer swaps: the outgoing and the incoming analyzer both in maintenance mode through the visit
    for (code, d0, d1) in (sim.SWAP_2025, sim.SWAP):
        i = [s[0] for s in sim.STATIONS].index(code)
        for d, h in ((d0, 10), (d1, 12)):
            s0 = solar_to_legal(dt.datetime(d.year, d.month, d.day, h - 1, 0)) + dt.timedelta(
                minutes=int(rng.integers(10, 40)))
            e0 = _end(s0, int(rng.integers(150, 200)))
            for serial in (sim.STATIONS[i][5], sim.SPARE):
                out.append(dict(day=(d - P.START).days, serial=serial, st=i, kind="scambio", start=s0, end=e0))
    return out


# ------------------------------------------------------------------ the analyzers' archive
GPT_PROFILE = [(20, 0.0, 0.0), (35, 0.0, 420.0), (35, 240.0, 175.0)]     # minutes, NO2 delivered, NO delivered


def minute_mix(h_solar, start_solar, end_solar, amb_no2, amb_no, eff, rng):
    """the hour's NO2 and NO as the analyzer averaged them when a titration window falls in it"""
    t0 = solar(h_solar)
    mins = []
    for mm in range(60):
        t = t0 + dt.timedelta(minutes=mm)
        if start_solar <= t < end_solar:
            el = (t - start_solar).total_seconds() / 60.0
            acc = 0
            val = (0.0, 0.0)
            for (n, no2, no) in GPT_PROFILE:
                if el < acc + n:
                    val = (no2, no)
                    break
                acc += n
            else:
                val = (0.0, 420.0)      # the NO span again until the window closes
            mins.append((val[0] * eff, val[1]))
        else:
            mins.append((amb_no2, amb_no))
    a = np.array(mins)
    return float(a[:, 0].mean()), float(a[:, 1].mean()), sum(1 for m in range(60)
                                                              if start_solar <= t0 + dt.timedelta(minutes=m) <
                                                              end_solar)


def archive(W, seed, vis, svc_win):
    """the analyzers' own hourly averages, ppb, analyzer clock (UTC), as downloaded at each round"""
    rng = np.random.default_rng(seed + 51)
    no2, no = W["no2"], W["no"]
    rows = []
    truth = {}
    win_by = {}
    for v in vis:
        win_by.setdefault(v["serial"], []).append(("T", v))
    for v in svc_win:
        win_by.setdefault(v["serial"], []).append(("S", v))
    for serial, a in W["analyzers"].items():
        loc = a["where"]
        eff = a["eff"]
        on = (loc >= 0) & (a["conv"] >= 0)
        hs = np.where(on)[0]
        amb2 = np.zeros(sim.HOURS)
        amb0 = np.zeros(sim.HOURS)
        amb2[on] = no2[loc[on], hs] / UG20
        amb0[on] = no[loc[on], hs] / sim.P.UGM3_PER_PPB_NO
        meas2 = eff * amb2 * (1 + rng.normal(0, 0.012, sim.HOURS)) + rng.normal(0, 0.35, sim.HOURS)
        meas0 = amb0 * (1 + rng.normal(0, 0.012, sim.HOURS)) + rng.normal(0, 0.35, sim.HOURS)
        status = np.zeros(sim.HOURS, dtype=int)
        gpt = np.zeros(sim.HOURS, dtype=bool)
        maint = np.zeros(sim.HOURS, dtype=bool)
        for (typ, v) in win_by.get(serial, []):
            s0, s1 = legal_to_solar(v["start"]), legal_to_solar(v["end"])
            h0, h1 = hidx(s0), hidx(s1 - dt.timedelta(minutes=1))
            for h in range(h0, h1 + 1):
                if not (0 <= h < sim.HOURS) or not on[h]:
                    continue
                if typ == "S":
                    maint[h] = True
                    status[h] = 2
                    continue
                m2, m0, n_in = minute_mix(h, s0, s1, amb2[h] * eff[h], amb0[h], eff[h], rng)
                meas2[h] = m2 + rng.normal(0, 0.35)
                meas0[h] = m0 + rng.normal(0, 0.35)
                gpt[h] = True
                if v["contractor"] == "A":
                    status[h] = 2
        # faults: hours with no value
        fault = np.zeros(sim.HOURS, dtype=bool)
        for _ in range(int(rng.integers(4, 9))):
            h0 = int(rng.integers(0, sim.HOURS - 60))
            fault[h0:h0 + int(rng.integers(2, 30))] = True
        fault &= on
        status[fault] = 8
        truth[serial] = {"gpt": gpt, "maint": maint, "fault": fault, "on": on, "meas2": meas2, "meas0": meas0}
        for h in hs:
            t = solar(h) - dt.timedelta(hours=1)          # UTC
            if fault[h]:
                rows.append((serial, t, None, None, None, 8))
            else:
                n2 = max(0.0, meas2[h])
                n0 = max(0.0, meas0[h])
                rows.append((serial, t, round(n0, 2), round(n2, 2), round(n0 + n2, 2), int(status[h])))
    df = pd.DataFrame(rows, columns=["matricola", "utc", "no_ppb", "no2_ppb", "nox_ppb", "stato"])
    # downloads at every quarterly round and at the year's close; each download starts two to four days before the
    # end of the one before, so those days come into the archive twice
    drng = np.random.default_rng(seed + 52)
    extra = []
    for serial, g in df.groupby("matricola", sort=False):
        days = sorted(set(v["day"] for v in vis if v["serial"] == serial and v["kind"] == "trimestrale"))
        for k in days:
            t1 = dt.datetime.combine(sim.day(k), dt.time(8, 0))
            back = int(drng.integers(2, 5))
            t0 = t1 - dt.timedelta(days=back)
            sel = g[(g["utc"] >= t0) & (g["utc"] < t1)]
            extra.append(sel)
    df = pd.concat([df] + extra, ignore_index=True)
    df = df.sort_values(["matricola", "utc"], kind="mergesort").reset_index(drop=True)
    df["utc"] = [t.strftime("%Y-%m-%d %H:%M") for t in df["utc"]]
    return df, truth


# ------------------------------------------------------------------ titrations
def gpt_steps(eff, rng):
    no_i = round(float(rng.normal(418, 6)), 1)
    imp = float(rng.uniform(3.0, 6.0))                   # NO2 already in the NO standard
    dno = float(rng.normal(246, 9))
    nox_i = round(no_i + imp * eff, 1)
    no_f = round(no_i - dno, 1)
    nox_f = round(no_f + (imp + dno) * eff, 1)
    e = ((nox_f - no_f) - (nox_i - no_i)) / (no_i - no_f)
    return no_i, no_f, nox_i, nox_f, e


def titrations(W, seed, vis):
    rng = np.random.default_rng(seed + 61)
    rowsA, rowsB = [], []
    names = {i: st[1] for i, st in enumerate(sim.STATIONS)}
    for v in sorted(vis, key=lambda x: (x["start"], x["serial"])):
        if v["st"] < 0:
            continue
        no_i, no_f, nox_i, nox_f, e = gpt_steps(v["eff"], rng)
        kind = {"trimestrale": "trimestrale", "prima della sostituzione": "pre-sostituzione",
                "dopo la sostituzione": "post-sostituzione"}[v["kind"]]
        if v["contractor"] == "A":
            gen = round(no_i - no_f, 1)
            mis = round((nox_f - no_f) - (nox_i - no_i), 1)
            rowsA.append((v["start"].date(), v["start"].strftime("%H:%M"), v["end"].strftime("%H:%M"), names[v["st"]],
                          v["serial"], kind, gen, mis, round(100 * mis / gen, 1),
                          "conforme" if mis / gen >= P.THRESHOLD else "NON CONFORME",
                          TECH_A[int(rng.integers(0, 2))]))
        else:
            rowsB.append((v["start"].strftime("%Y-%m-%d"), v["start"].strftime("%H:%M"), v["end"].strftime("%H:%M"),
                          code_of(v["st"]), v["serial"], kind, no_i, no_f, nox_i, nox_f, round(e, 4),
                          TECH_B[int(rng.integers(0, 3))]))
    A = pd.DataFrame(rowsA, columns=["Data", "Ora inizio", "Ora fine", "Stazione", "Matricola", "Tipo verifica",
                                     "NO2 generato (ppb)", "NO2 misurato (ppb)", "Rendimento convertitore (%)",
                                     "Esito", "Tecnico"])
    B = pd.DataFrame(rowsB, columns=["data", "ora_inizio", "ora_fine", "codice_stazione", "matricola", "tipo_verifica",
                                     "no_iniziale_ppb", "no_finale_ppb", "nox_iniziale_ppb", "nox_finale_ppb",
                                     "efficienza", "tecnico"])
    return A, B


# ------------------------------------------------------------------ service log
def service_log(W, seed, svc_win):
    rng = np.random.default_rng(seed + 71)
    rows = []
    svc = W["svc"]
    for serial, a in W["analyzers"].items():
        for j, c in enumerate(a["converters"]):
            d = sim.day(c["installed"])
            st = int(a["where"][min(sim.HOURS - 1, c["installed"] * 24 + 11)])
            stc = code_of(st) if st >= 0 else "MAG"
            if j == 0:
                what = "revisione generale: sostituzione convertitore al molibdeno, pompa, filtri e lampada ozonizzatore"
            elif c["reason"] == "manutenzione programmata":
                what = "manutenzione programmata annuale: sostituzione convertitore al molibdeno, pulizia celle, filtri"
            else:
                what = "sostituzione convertitore al molibdeno (titolazione sotto 95 %)"
            rows.append((d, stc, serial, what, SERVICE_TECH[int(rng.integers(0, 2))]))
    # repairs that leave the converter in place
    for i, st in enumerate(sim.STATIONS):
        for _ in range(int(rng.integers(1, 4))):
            k = int(rng.integers(40, sim.P.DAYS - 5))
            d = sim.day(k)
            what = ["sostituzione pompa", "sostituzione lampada ozonizzatore", "pulizia camera di reazione",
                    "sostituzione essiccatore aria ozonizzatore"][int(rng.integers(0, 4))]
            rows.append((d, st[0], st[5], what, SERVICE_TECH[int(rng.integers(0, 2))]))
    for (code, d0, d1) in (sim.SWAP_2025, sim.SWAP):
        i = [s[0] for s in sim.STATIONS].index(code)
        rows.append((d0, code, sim.STATIONS[i][5], "analizzatore in laboratorio per guasto ozonizzatore; installato "
                     "l'analizzatore di scorta " + sim.SPARE, SERVICE_TECH[0]))
        rows.append((d1, code, sim.STATIONS[i][5], "rientro analizzatore dal laboratorio; scorta " + sim.SPARE +
                     " in magazzino", SERVICE_TECH[1]))
    for code, (t0, t1) in NEW_LOGGERS.items():
        i = [s[0] for s in sim.STATIONS].index(code)
        rows.append((t0.date(), code, sim.STATIONS[i][5], "installazione nuovo registratore dati LGX-300 (sostituisce "
                     "DL-12)", SERVICE_TECH[0]))
        rows.append((t1.date(), code, sim.STATIONS[i][5], "registratore LGX-300: condizioni di riferimento impostate "
                     "a 20 °C, 101,3 kPa", SERVICE_TECH[1]))
    code, d28 = sim.POSTPONED
    i = [s[0] for s in sim.STATIONS].index(code)
    d27 = svc[code]["scheduled"][2]
    rows.append((d27, code, sim.STATIONS[i][5], "manutenzione programmata non eseguita (subentro nuovo appaltatore); "
                 "riprogrammata al " + d28.strftime("%d/%m/%Y"), SERVICE_TECH[0]))
    df = pd.DataFrame(rows, columns=["data", "stazione", "matricola", "intervento", "tecnico"])
    return df.sort_values(["data", "stazione"], kind="mergesort").reset_index(drop=True)


def plan_2028(W):
    rows = []
    for i, st in enumerate(sim.STATIONS):
        sch = W["svc"][st[0]]["scheduled"][3]
        note = ""
        if st[0] == sim.POSTPONED[0]:
            note = "manutenzione 2027 rinviata per il subentro del nuovo appaltatore"
        rows.append((st[0], st[1], st[5], "NX4210" if st[5].startswith("NX") else "CL62", sch, note))
    rows.append(("MAG", "magazzino (scorta)", sim.SPARE, "CL62", dt.date(2028, 11, 14), "analizzatore di scorta"))
    return pd.DataFrame(rows, columns=["stazione", "nome", "matricola", "modello", "manutenzione_2028", "note"])


TYPES = {"T": "traffico", "U": "fondo urbano", "S": "fondo suburbano", "I": "industriale", "R": "fondo rurale"}
COORDS = [(45.0011, 10.6582), (45.0473, 10.3916), (45.0912, 10.5207), (44.9638, 10.7834), (45.0059, 10.6497),
          (45.0442, 10.3999), (45.0827, 10.9145), (44.9915, 10.8762), (44.9579, 10.7738), (45.1384, 10.6083),
          (45.1702, 10.2864), (45.0786, 10.2713), (45.0702, 10.9431), (45.0368, 10.4255), (45.1149, 10.1528),
          (45.1537, 10.9921)]


def register(W):
    rows = []
    for i, st in enumerate(sim.STATIONS):
        logger, since = "DL-12", dt.date(2019, 5, 1)
        if st[0] in NEW_LOGGERS:
            logger, since = "LGX-300", NEW_LOGGERS[st[0]][0].date()
        rows.append((st[0], st[1], TYPES[st[2]], COORDS[i][0], COORDS[i][1], st[5],
                     "NX4210" if st[5].startswith("NX") else "CL62", logger, since))
    return pd.DataFrame(rows, columns=["codice", "nome", "tipo", "lat", "lon", "analizzatore_nox", "modello",
                                       "registratore", "registratore_dal"])


# ------------------------------------------------------------------ the network's database, 2027
def database_2027(W, seed, vis, svc_win, arch_truth):
    """hourly NO2, micrograms per cubic metre, solar time, with the validation code; the truth behind each row"""
    rng = np.random.default_rng(seed + 81 + 1000 * P.ASK_SEED)
    rows, truth = [], []
    for i, st in enumerate(sim.STATIONS):
        code = st[0]
        lg = NEW_LOGGERS.get(code)
        # data capture: short outages that leave an hour with fewer than 45 minutes
        short = set(int(x) for x in rng.choice(N27, int(rng.integers(20, 45)), replace=False))
        for j in range(N27):
            h = H27 + j
            t = solar(h)
            serial = None
            for s, a in W["analyzers"].items():
                if a["where"][h] == i and a["conv"][h] >= 0:
                    serial = s
                    break
            stamp = t.strftime("%d/%m/%Y %H:%M")
            if serial is None:
                rows.append((code, stamp, None, "F"))
                truth.append((code, j, None, None, "none"))
                continue
            at = arch_truth[serial]
            if serial == sim.SPARE:
                # the data system files an analyzer's hours under the analyzer's place in its register, and the spare
                # is registered to the store: its hours at the station arrive under MAG, the station's own as not
                # received
                rows.append((code, stamp, None, "F"))
                truth.append((code, j, None, None, "none"))
                at_s = arch_truth[serial]
                if at_s["fault"][h]:
                    rows.append(("MAG", stamp, None, "A"))
                    truth.append(("MAG", j, None, serial, "fault"))
                elif at_s["maint"][h]:
                    rows.append(("MAG", stamp, None, "M"))
                    truth.append(("MAG", j, None, serial, "maint"))
                else:
                    v = max(0.0, at_s["meas2"][h]) * UG20
                    c = "N" if j in short else ("R" if (v > 140 and rng.random() < 0.35) else "V")
                    rows.append(("MAG", stamp, round(v, 1), c))
                    kind = "spare_short" if c == "N" else ("spare_gpt" if at_s["gpt"][h] else "spare")
                    truth.append(("MAG", j, v, serial, kind))
                continue
            if at["fault"][h]:
                rows.append((code, stamp, None, "A"))
                truth.append((code, j, None, serial, "fault"))
                continue
            if at["maint"][h]:
                rows.append((code, stamp, None, "M"))
                truth.append((code, j, None, serial, "maint"))
                continue
            f = UG20
            if lg and lg[0] <= t < lg[1]:
                f = UGL
            v = max(0.0, at["meas2"][h]) * f
            v_true = max(0.0, at["meas2"][h]) * UG20
            if j in short:
                c = "N"
            else:
                c = "R" if (v > 140 and rng.random() < 0.35) else "V"
            rows.append((code, stamp, round(v, 1), c))
            kind = "short" if c == "N" else ("gpt" if at["gpt"][h] else "air")
            truth.append((code, j, v_true, serial, kind))
    df = pd.DataFrame(rows, columns=["stazione", "data_ora_solare", "no2_ugm3", "codice"])
    tr = pd.DataFrame(truth, columns=["stazione", "j", "no2_20c", "matricola", "kind"])
    # re-sent days: three stations' data for a day arrived twice
    rr = np.random.default_rng(seed + 82)
    extra = []
    for code in rr.choice([s[0] for s in sim.STATIONS], 3, replace=False):
        d0 = int(rr.integers(30, 330))
        sel = df[(df["stazione"] == code)].iloc[d0 * 24:(d0 + 1) * 24]
        extra.append(sel)
    df = pd.concat([df] + extra, ignore_index=True)
    order = df["stazione"].map({**{s[0]: k for k, s in enumerate(sim.STATIONS)}, "MAG": len(sim.STATIONS)})
    key = pd.to_datetime(df["data_ora_solare"], format="%d/%m/%Y %H:%M")
    df = df.assign(_o=order, _k=key).sort_values(["_o", "_k"], kind="mergesort").drop(columns=["_o", "_k"])
    return df.reset_index(drop=True), tr


def build(W, seed):
    vis = visits(W, seed)
    sw = service_windows(W, seed)
    arch, at = archive(W, seed, vis, sw)
    tA, tB = titrations(W, seed, vis)
    log = service_log(W, seed, sw)
    plan = plan_2028(W)
    reg = register(W)
    db, dbt = database_2027(W, seed, vis, sw, at)
    return dict(visits=vis, service_windows=sw, archive=arch, archive_truth=at, titrations_A=tA, titrations_B=tB,
                service_log=log, plan=plan, register=reg, database=db, database_truth=dbt)
