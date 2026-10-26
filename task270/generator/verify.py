"""The independent verifier: reads only the shipped bundle (target/ and figures.json) and recomputes the call, the
critical components and every ask figure with its own code (pandas joins, interval sums per member, a Poisson-binomial
by convolution), then compares with figures.json."""
import json
import os
import sys
from decimal import Decimal, ROUND_HALF_UP

import numpy as np
import pandas as pd

YOUNG = ("18-24", "25-34")
PRIME = (20 * 3600, 24 * 3600 + 30 * 60)


def rnd(x, n):
    return float(Decimal(repr(float(x))).quantize(Decimal(1).scaleb(-n), rounding=ROUND_HALF_UP))


def local_seconds(ts, t0):
    return ((ts - t0).dt.total_seconds()).astype(np.int64)


def run(task):
    T = os.path.join(task, "target")
    fig = json.load(open(os.path.join(task, "generator", "figures.json")))
    out = []

    def ok(label, a, b):
        out.append((label, a == b, "%s | %s" % (a, b)))

    t0 = pd.Timestamp("2026-03-02 00:00:00")
    switch = pd.Timestamp("2026-03-29 01:00:00")
    chans = pd.read_csv(os.path.join(T, "canais_codigos.csv"), dtype=str)
    byname = {"Farol": "FAR1", "Farol 2": "FAR2", "Vértice": "VRT", "Litoral": "LIT", "Pulsar": "PLS",
              "Pulsar+": "PLS", "Arena": "ARN"}
    canon = {c: byname[n] for c, n in zip(chans["codigo"], chans["nome"])}

    # ---- the members who count and their live viewing on the panel's local clock
    pan = pd.read_csv(os.path.join(T, "audimetria_individuos_2026-03.csv"), dtype={"id_individuo": str})
    young = pan[pan["escalao_etario"].isin(YOUNG) & (pan["peso_28d"] > 0)].set_index("id_individuo")["peso_28d"]
    v = pd.read_csv(os.path.join(T, "audimetria_visionamentos_2026-03.csv"), dtype=str)
    v = v[(v["modo"] == "AO VIVO") & (v["convidado"] == "N") & v["id_individuo"].isin(young.index)].copy()
    for c in ("inicio_utc", "fim_utc"):
        u = pd.to_datetime(v[c].str.rstrip("Z"))
        v[c] = local_seconds(u + pd.to_timedelta(np.where(u >= switch, 3600, 0), unit="s"), t0)
    v["ch"] = v["canal"].map(canon)
    view = {c: g.sort_values("inicio_utc")[["inicio_utc", "fim_utc", "id_individuo"]].to_numpy() for c, g in
            v.groupby("ch")}

    # ---- the as-run places and the bookings behind them
    ar = pd.read_csv(os.path.join(T, "emissao_publicitaria_2026-03.csv"), dtype=str)
    ar["ch"] = ar["canal"].map(canon)
    s0 = local_seconds(pd.to_datetime(ar["data"] + " " + ar["hora_inicio"]), t0)
    ar["s0"], ar["s1"] = s0, s0 + ar["duracao_s"].astype(int)
    ar["clock"] = ar["s0"] - local_seconds(pd.to_datetime(ar["dia_tv"]), t0)
    bk = pd.read_csv(os.path.join(T, "reservas_publicidade_2026-03.csv"), dtype=str)
    bk["ch_b"] = bk["canal"].map(canon)
    sold = ar.merge(bk[["id_reserva", "ch_b", "dia_tv", "colocacao", "janela"]].rename(
        columns={"dia_tv": "dia_reserva", "colocacao": "tipo"}), on="id_reserva", how="inner")
    sold = sold[sold["tipo"] == "ROTAÇÃO"]

    # ---- the three schedules on their reference days
    lines = []
    for s in "ABC":
        sh = pd.read_excel(os.path.join(T, "esquemas_campanha_2027.xlsx"), sheet_name="Esquema %s" % s)
        sh = sh[sh["Semana"] != "Total"]
        for _, r in sh.iterrows():
            d = pd.Timestamp(r["Data"])
            ref = (pd.Timestamp("2026-03-02") + pd.Timedelta(days=7 * (int(r["Semana"]) - 1) + d.weekday()))
            lines.append(dict(s=s, ch=byname[r["Canal"]], ref=ref.strftime("%Y-%m-%d"), prog=r["Programa ou janela"],
                              brk=r["Intervalo no programa"], place=r["Colocação"]))

    def seen(ch, a, b):
        arr = view[ch]
        lo = np.searchsorted(arr[:, 0].astype(np.int64), a - 6 * 3600)
        hi = np.searchsorted(arr[:, 0].astype(np.int64), b)
        acc = {}
        for x0, x1, mm in arr[lo:hi]:
            o = min(int(x1), b) - max(int(x0), a)
            if o > 0:
                acc[mm] = acc.get(mm, 0) + o
        return {mm for mm, sec in acc.items() if sec >= (b - a) / 2}

    probs = {s: {} for s in "ABC"}
    in_window_b = {}
    for ln in lines:
        if ln["place"] == "Rotação":
            win = ln["prog"].replace("Rotação ", "").lower()
            pl = sold[(sold["ch_b"] == ln["ch"]) & (sold["dia_reserva"] == ln["ref"]) &
                      (sold["janela"].str.lower() == win)]
            iw = ar[(ar["ch"] == ln["ch"]) & (ar["dia_tv"] == ln["ref"]) & (ar["colocacao"] == "ROTAÇÃO") &
                    (ar["clock"] >= PRIME[0]) & (ar["clock"] < PRIME[1])]
            in_window_b.setdefault(ln["ref"] + ln["ch"], iw)
        else:
            br = ar[(ar["ch"] == ln["ch"]) & (ar["dia_tv"] == ln["ref"]) & (ar["programa"] == ln["prog"]) &
                    (ar["intervalo_no_programa"].astype(int) == int(ln["brk"]))].sort_values("posicao", key=lambda x:
                                                                                           x.astype(int))
            pl = br.head(1) if ln["place"].startswith("1.") else br.tail(1)
        cnt = {}
        for _, a in pl.iterrows():
            for mm in seen(a["ch"], int(a["s0"]), int(a["s1"])):
                cnt[mm] = cnt.get(mm, 0) + 1
        for mm, c in cnt.items():
            probs[ln["s"]].setdefault(mm, []).append(c / len(pl))

    def reach(P, k):
        tot = young.sum()
        acc = 0.0
        for mm, ps in P.items():
            d = np.array([1.0])
            for q in ps:
                d = np.convolve(d, [1 - q, q])
            acc += young[mm] * d[k:].sum()
        return acc / tot

    r3 = {s: reach(probs[s], 3) for s in "ABC"}
    r1 = {s: reach(probs[s], 1) for s in "ABC"}
    best = sorted("ABC", key=lambda s: -r3[s])
    ok("call", best[0], fig["call"]["schedule"])
    ok("runner-up", best[1], fig["call"]["runner_up"])
    ok("lead", rnd(100 * (r3[best[0]] - r3[best[1]]), 1), fig["call"]["lead_points"])
    for s in "ABC":
        ok("3+ %s" % s, rnd(100 * r3[s], 1), fig["components"]["reach3_pct"][s])
        ok("1+ %s" % s, rnd(100 * r1[s], 1), fig["context"]["reach1_pct"][s])
    pr = sold[sold["ch_b"].isin(["VRT", "LIT", "PLS"]) & (sold["janela"].str.startswith("Horário nobre"))]
    inside = ((pr["clock"] >= PRIME[0]) & (pr["clock"] < PRIME[1]) & (pr["dia_tv"] == pr["dia_reserva"])).sum()
    ok("prime rotation bookings", int(len(pr)), fig["components"]["prime_rotation_bookings"])
    ok("aired outside prime", int(len(pr) - inside), fig["components"]["prime_rotation_bookings_aired_outside_prime"])
    ok("share outside prime", rnd(100 * (len(pr) - inside) / len(pr), 1),
       fig["components"]["share_aired_outside_prime_pct"])

    # ---- the 2025 response: a person is an identity document, and a booking of a first donation is one made before
    # that person's first donation, the earliest on any of their donor records (the extract's donor fields are the
    # record on the extraction day)
    po = pd.read_csv(os.path.join(T, "marcacoes_portal_dador_2025.csv"), dtype=str, keep_default_na=False)
    po["t"] = pd.to_datetime(po["criada_em"])
    given = po[po["data_primeira_dadiva"] != ""]
    gave = pd.to_datetime(given["data_primeira_dadiva"]).groupby(given["documento_hash"]).min()
    po["gave"] = po["documento_hash"].map(gave)
    po = po[po["gave"].isna() | (po["t"].dt.normalize() < po["gave"])].copy()
    first = po.sort_values("t").groupby("documento_hash").head(1).copy()
    born = pd.to_datetime(first["data_nascimento"])
    made = first["t"].dt.normalize()
    age = made.dt.year - born.dt.year - ((made.dt.month * 100 + made.dt.day) < (born.dt.month * 100 + born.dt.day))
    first = first[(age >= 18) & (age <= 34)]
    d = first["t"].dt.normalize()
    base = [int(((d >= pd.Timestamp("2025-03-10") + pd.Timedelta(days=7 * k)) &
                 (d < pd.Timestamp("2025-03-17") + pd.Timedelta(days=7 * k))).sum()) for k in range(4)]
    camp = [int(((d >= pd.Timestamp("2025-04-07") + pd.Timedelta(days=7 * k)) &
                 (d < pd.Timestamp("2025-04-14") + pd.Timedelta(days=7 * k))).sum()) for k in range(4)]
    avg = sum(base) / 4.0
    ok("2025 baseline weekly average", rnd(avg, 1), fig["asks"]["R"]["baseline_weekly_average"])
    ok("2025 weeks above", [rnd(c - avg, 1) for c in camp], fig["asks"]["R"]["campaign_weeks_above_baseline"])
    ok("2025 weeks total above", rnd(sum(camp) - 4 * avg, 1), fig["asks"]["R"]["campaign_weeks_total_above"])
    per = (sum(camp) - 4 * avg) / 543.7
    ok("2025 response", rnd(per, 2), fig["asks"]["R"]["response_per_thousand_reached3"])
    uni = pd.read_csv(os.path.join(T, "universo_2026.csv"))
    U = int(uni[uni["escalao_etario"].isin(YOUNG)]["populacao"].sum())
    for s in "ABC":
        ok("expected bookings %s" % s, int(rnd(per * r3[s] * U / 1000 / 10, 0) * 10),
           fig["asks"]["X"]["expected_first_donation_bookings"][s])
    bad = [o for o in out if not o[1]]
    for label, good, detail in out:
        print("%s  verify %s  [%s]" % ("PASS" if good else "FAIL", label, detail))
    print("verify: %d figures, %d differ" % (len(out), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
