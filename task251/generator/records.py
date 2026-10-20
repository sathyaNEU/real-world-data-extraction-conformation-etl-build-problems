"""The trust's records, cut from the world: the data manager's export of every result received, the pairings with
the laboratory, the pairing plan, the meter register with its location history, the analyzer parallel run, the 2027
service list and two files nobody needs for the list (strip deliveries, the laboratory's external quality scheme).

    build(W, seed) -> dict of DataFrames and lists"""
import datetime as dt

import numpy as np
import pandas as pd

import params as P
import sim

DAYNAMES = ["lunedì", "martedì", "mercoledì", "giovedì", "venerdì", "sabato", "domenica"]


def hosp_of(ward):
    return P.SIM_HOSP[sim.W_[ward][2]]


LETTERS = "ACDEFHJKLMNPRSTUVWXY"


def serials(W, seed):
    """the meters' serials as the manufacturer prints them (a letter, three digits, a letter) and the trust's
    inventory numbers"""
    rng = np.random.default_rng(seed + 11)
    seen, out = set(), []
    inv = rng.choice(np.arange(10200, 19999), size=len(W["meters"]), replace=False)
    for m, i in zip(W["meters"], inv):
        while True:
            s = "GX2-%s%03d%s" % (LETTERS[int(rng.integers(20))], int(rng.integers(100, 1000)),
                                  LETTERS[int(rng.integers(20))])
            if s not in seen and s[5:8] not in {x[5:8] for x in seen}:
                seen.add(s)
                break
        out.append((s, "INV-%05d" % i))
    return out


def solar_str(u, sec=None):
    t = sim.utc_to_solar(u)
    return t.strftime("%d/%m/%Y %H:%M") if sec is None else (t + dt.timedelta(seconds=int(sec))).strftime(
        "%d/%m/%Y %H:%M:%S")


def civil_str(u):
    return sim.utc_to_civil(u).strftime("%d/%m/%Y %H:%M")


def lots(seed):
    """Strip lots per hospital and control lots for the whole trust, each with the day it came into use."""
    rng = np.random.default_rng(seed + 13)
    strips = {}
    for h in ("CM", "RV", "VD"):
        d, out = sim.START - dt.timedelta(days=int(rng.integers(5, 40))), []
        while d <= sim.END:
            out.append((d, "S%d%04d" % (int(rng.integers(6, 8)), int(rng.integers(1000, 9999)))))
            d += dt.timedelta(days=int(rng.integers(45, 75)))
        strips[h] = out
    d, ctrl = sim.START - dt.timedelta(days=20), []
    while d <= sim.END:
        ctrl.append((d, "C%04d" % int(rng.integers(1000, 9999))))
        d += dt.timedelta(days=int(rng.integers(80, 110)))
    return strips, ctrl


def _lot_on(lst, d):
    cur = lst[0][1]
    for a, x in lst:
        if a <= d:
            cur = x
    return cur


def operators(seed):
    rng = np.random.default_rng(seed + 17)
    used, out = set(), {}
    for w in sim.WARDS:
        pool = []
        while len(pool) < int(rng.integers(18, 34)):
            b = "%06d" % int(rng.integers(1000, 99999))
            if b not in used:
                used.add(b)
                pool.append(b)
        out[w[0]] = pool
    return out


def dms(W, R, seed):
    """One row per result the server received, copies included, in the order the server received them."""
    rng = np.random.default_rng(seed + 19)
    ser = serials(W, seed)
    strips, ctrl = lots(seed)
    ops = operators(seed)
    T = W["tests"]
    # each meter's memory numbers, in the order the meter took its results
    nmem = {}
    by = {}
    for i, t in enumerate(T):
        by.setdefault(t["m"], []).append(i)
    start_mem = rng.integers(2000, 60000, size=len(W["meters"]))
    for m_i, idx in by.items():
        idx.sort(key=lambda i: (T[i]["utc"], i))
        for k, i in enumerate(idx):
            nmem[i] = int(start_mem[m_i]) + k
    srng = np.random.default_rng(seed + 43)
    for t in T:
        t["sec"] = int(srng.integers(0, 60))
    first = {}
    for i, rec_s, cp in R:
        first[i] = min(first.get(i, rec_s), rec_s)
    for i, rec_s in first.items():           # no result reaches the record exactly two hours after its test
        t = T[i]
        if rec_s - (t["utc"] * 60 + t["sec"]) == 7200:
            t["sec"] += 1 if t["sec"] < 59 else -1
    order = sorted(range(len(R)), key=lambda r: (R[r][1], r))
    first_id = {}
    rows = []
    id0 = 4_810_000 + int(rng.integers(0, 90000))
    op_of = {}
    for k, r in enumerate(order):
        i, rec_u, copy = R[r]
        t = T[i]
        m = W["meters"][t["m"]]
        rid = id0 + k
        if i not in first_id:
            first_id[i] = rid
        if i not in op_of:
            op_of[i] = ops[t["ward"]][int(rng.integers(len(ops[t["ward"]])))]
        d_civ = sim.utc_to_civil(t["utc"]).date()
        if t["kind"] == "P":
            v = t["M"]
            res = "LO" if v < sim.LO else ("HI" if v > sim.HI else str(int(round(v))))
            tipo, liv, lc = "PAZIENTE", "", ""
        else:
            res = str(int(round(t["M"])))
            tipo, liv, lc = "CONTROLLO", t["kind"][1], _lot_on(ctrl, d_civ)
        cur = sim.ward_on(m, sim.END)
        rows.append((rid, ser[t["m"]][0], nmem[i], solar_str(t["utc"], t["sec"]), tipo, liv, lc,
                     _lot_on(strips[sim.W_[t["ward"]][2]], d_civ), t["pid"], op_of[i], res,
                     hosp_of(cur), cur,
                     (sim.T0 + dt.timedelta(seconds=int(rec_u))).strftime("%Y-%m-%dT%H:%M:%SZ")))
    df = pd.DataFrame(rows, columns=["id_risultato", "matricola", "n_memoria", "data_ora_test", "tipo", "livello",
                                     "lotto_controllo", "lotto_strisce", "id_paziente", "operatore", "risultato",
                                     "presidio", "reparto", "data_ora_ricezione"])
    return df, first_id, nmem


def pairings(W, first_id, seed):
    rng = np.random.default_rng(seed + 23)
    ser = serials(W, seed)
    T = W["tests"]
    seq = {}
    rows = []
    for p in sorted(W["pairs"], key=lambda p: p["draw"]):
        t = T[p["test"]]
        m = W["meters"][t["m"]]
        civ = sim.utc_to_civil(p["draw"])
        key = civ.strftime("%y%m%d")
        seq[key] = seq.get(key, int(rng.integers(100, 400))) + int(rng.integers(1, 9))
        v = t["M"]
        res = "LO" if v < sim.LO else ("HI" if v > sim.HI else str(int(round(v))))
        cur = sim.ward_on(m, sim.END)
        rows.append((first_id[p["test"]], ser[t["m"]][0], solar_str(t["utc"], t["sec"]), res,
                     "%s%05d" % (key, seq[key]),
                     civ.strftime("%d/%m/%Y %H:%M"), int(round(p["L"])), hosp_of(cur), cur))
    return pd.DataFrame(rows, columns=["id_risultato", "matricola", "data_ora_test", "glucometro_mg_dl",
                                       "n_accettazione", "data_ora_prelievo", "laboratorio_mg_dl", "presidio",
                                       "reparto"])


def plan(W, seed):
    ser = serials(W, seed)
    rows = []
    for m_i, m in enumerate(W["meters"]):
        for wd, a, b in sim.plan_rows(m):
            rows.append((ser[m_i][0], " e ".join(DAYNAMES[x] for x in wd) if len(wd) == 2 else
                         ", ".join(DAYNAMES[x] for x in wd[:-1]) + " e " + DAYNAMES[wd[-1]], a, b))
    pl = pd.DataFrame(rows, columns=["matricola", "giorni", "dal", "al"])
    names = {dt.date(2026, 8, 15): "Assunzione", dt.date(2026, 11, 1): "Ognissanti",
             dt.date(2026, 12, 8): "Immacolata Concezione", dt.date(2026, 12, 25): "Natale",
             dt.date(2026, 12, 26): "Santo Stefano", dt.date(2027, 1, 1): "Capodanno",
             dt.date(2027, 1, 6): "Epifania", dt.date(2027, 3, 29): "Lunedì dell'Angelo",
             dt.date(2027, 4, 25): "Festa della Liberazione", dt.date(2027, 5, 1): "Festa del lavoro",
             dt.date(2027, 6, 2): "Festa della Repubblica", dt.date(2027, 8, 15): "Assunzione",
             dt.date(2027, 11, 1): "Ognissanti", dt.date(2027, 12, 8): "Immacolata Concezione",
             dt.date(2027, 12, 25): "Natale", dt.date(2027, 12, 26): "Santo Stefano"}
    fe = pd.DataFrame([(d, names[d]) for d in sim.HOLIDAYS], columns=["data", "festività"])
    return pl, fe


def register(W, seed):
    ser = serials(W, seed)
    rng = np.random.default_rng(seed + 29)
    cur, hist = [], []
    for m_i, m in enumerate(W["meters"]):
        since = dt.date(2024, 1, 1) + dt.timedelta(days=int(rng.integers(0, 700)))
        w_end = sim.ward_on(m, sim.END)
        cur.append((ser[m_i][0], ser[m_i][1], P.METER, P.HOSPITALS[hosp_of(w_end)], w_end, since, m["svc"],
                    "in uso"))
        if m["move"] is None:
            hist.append((ser[m_i][0], hosp_of(m["ward"]), m["ward"], since, None))
        else:
            hist.append((ser[m_i][0], hosp_of(m["ward"]), m["ward"], since, m["move"] - dt.timedelta(days=1)))
            hist.append((ser[m_i][0], hosp_of(m["ward2"]), m["ward2"], m["move"], None))
    c = pd.DataFrame(cur, columns=["matricola", "inventario", "modello", "presidio", "reparto", "in_uso_dal",
                                  "ultima_taratura", "stato"])
    h = pd.DataFrame(hist, columns=["matricola", "presidio", "reparto", "dal", "al"])
    return c.sort_values(["presidio", "reparto", "matricola"]), h.sort_values(["matricola", "dal"])


def parallel(W, seed):
    rng = np.random.default_rng(seed + 31)
    days = [sim.PARALLEL[0] + dt.timedelta(days=k) for k in range((sim.PARALLEL[1] - sim.PARALLEL[0]).days + 1)]
    days = [d for d in days if d.weekday() < 6]
    rows = []
    for n, (t, a, b) in enumerate(W["parallel"], 1):
        d = days[int(rng.integers(len(days)))]
        rows.append((n, d, "%s%05d" % (d.strftime("%y%m%d"), int(rng.integers(20000, 29999))), int(round(a)),
                     int(round(b))))
    df = pd.DataFrame(rows, columns=["n", "data", "n_accettazione", "A_" + P.ANALYZER_A.replace(" ", "_") + "_mg_dl",
                                     "B_" + P.ANALYZER_B.replace(" ", "_") + "_mg_dl"])
    return df.sort_values(["data", "n_accettazione"]).reset_index(drop=True).assign(n=lambda x: range(1, len(x) + 1))


def service_list(W, seed):
    ser = serials(W, seed)
    rows = []
    for m_i, m in enumerate(W["meters"]):
        rows.append((ser[m_i][0], ser[m_i][1], P.HOSPITALS[hosp_of(m["ward"])], m["ward"], m["svc"]))
    return pd.DataFrame(rows, columns=["matricola", "inventario", "presidio", "reparto", "data"]).sort_values(
        ["data", "presidio", "reparto", "matricola"])


def strips_delivered(W, seed):
    rng = np.random.default_rng(seed + 37)
    cnt = {}
    for t in W["tests"]:
        d = sim.utc_to_civil(t["utc"]).date()
        if d.year == 2027:
            cnt[(t["ward"], d.month)] = cnt.get((t["ward"], d.month), 0) + 1
    rows = []
    for w in sim.WARDS:
        stock = int(rng.integers(2, 8))
        for mo in range(1, 13):
            need = cnt.get((w[0], mo), 0) * 1.06 / 50
            boxes = max(0, int(round(need + rng.normal(0, max(1.0, need * 0.12)) - (stock - 4) * 0.4)))
            stock += boxes - need
            rows.append((P.HOSPITALS[hosp_of(w[0])], w[0], "%04d-%02d" % (2027, mo), boxes, 50))
    return pd.DataFrame(rows, columns=["presidio", "reparto", "mese", "confezioni", "strisce_per_confezione"])


def veq(seed):
    rng = np.random.default_rng(seed + 41)
    rows = []
    for k, (d, lev) in enumerate([(dt.date(2027, 2, 9), 88), (dt.date(2027, 4, 13), 251), (dt.date(2027, 6, 8), 64),
                                  (dt.date(2027, 8, 10), 173), (dt.date(2027, 10, 12), 312),
                                  (dt.date(2027, 12, 7), 121)], 1):
        an = P.ANALYZER_A if d < sim.SWITCH else P.ANALYZER_B
        target = lev * (1 + rng.normal(0, 0.01))
        res = lev * (1 + (sim.LAB_A if d < sim.SWITCH else 0) * 0.3 + rng.normal(0, 0.015))
        sd = target * 0.035
        rows.append(("2027-%d" % k, d, "GLU-%d" % (700 + 3 * k), an, round(target, 1), int(round(res)),
                     round((res - target) / sd, 2)))
    return pd.DataFrame(rows, columns=["giro", "data", "campione", "analizzatore", "valore_assegnato_mg_dl",
                                       "risultato_mg_dl", "z_score"])


def build(W, seed):
    R = sim.receptions(W, seed)
    d, first_id, nmem = dms(W, R, seed)
    pl, fe = plan(W, seed)
    cur, hist = register(W, seed)
    return dict(dms=d, pairs=pairings(W, first_id, seed), plan=pl, holidays=fe, register=cur, history=hist,
                parallel=parallel(W, seed), service=service_list(W, seed), strips=strips_delivered(W, seed),
                veq=veq(seed), receptions=R, first_id=first_id, nmem=nmem, serials=serials(W, seed))
