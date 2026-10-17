"""Everything the bulletin owes, computed from the shipped bundle and nothing else.

The actions are rebuilt from the three access routes the way the protocol says, the code the register
keeps for each action is taken on 2.6, and the period's confrontational actions are counted four ways:
the codes as they stand, the codes with the classifier's false marks taken out, the codes scaled by the
classifier's recall, and the count rebuilt from both of the classifier's measured error rates.
"""
import csv
import datetime as dt
import os
import statistics

import world as W

CONF = set(W.CONFRONTATIONAL)
PERIOD = (W.PERIOD_FROM, W.PERIOD_TO)


def read(target, name):
    with open(os.path.join(target, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pdate(s):
    return dt.date.fromisoformat(s[:10])


def pts(s):
    s = s.strip().rstrip("Z").replace("T", " ")
    return dt.datetime.strptime(s[:16], "%Y-%m-%d %H:%M")


def lisbon(utc_moment):
    off = 1 if (utc_moment + dt.timedelta(hours=1)).date() < W.DST_BACK else 0
    return utc_moment + dt.timedelta(hours=off)


def load(target):
    gaz, muni_of = {}, {}
    for r in read(target, "gazeteiro_localidades.csv"):
        gaz[r["nome"]] = r["codigo_localidade"]
        muni_of[r["codigo_localidade"]] = (r["codigo_municipio"], r["municipio"], r["distrito"],
                                           r["regiao"])
    reports, seen = [], set()
    for r in read(target, "registo_itens_imprensa.csv"):
        if r["estado"] != "aceite" or r["id_relato"] in seen:
            continue
        seen.add(r["id_relato"])
        reports.append(dict(route="IMP", ident=r["id_relato"], src=r["orgao"], theme=r["tema"],
                            code=r["codigo_acao"], place=r["local_texto"],
                            day=pdate(r["data_ocorrencia"]), start=pts(r["inicio_acao"]),
                            recv=lisbon(pts(r["carimbo_recepcao"]))))
    for r in read(target, "relatos_rede_parceiros.csv"):
        reports.append(dict(route="PAR", ident=r["id_relato"], src=r["codigo_parceiro"],
                            theme=r["tema"], code=r["codigo_acao"], place=r["local_texto"],
                            day=pdate(r["data_ocorrencia"]), start=pts(r["inicio_acao"]),
                            recv=lisbon(pts(r["carimbo_entrega_utc"])), load=r["id_carga"]))
    for r in read(target, "relatos_linha_publica.csv"):
        reports.append(dict(route="LIN", ident=r["id_relato"], src="LIN", theme=r["tema"],
                            code=r["codigo_acao"], place=r["local_texto"],
                            day=pdate(r["data_ocorrencia"]), start=pts(r["inicio_acao"]),
                            recv=pts(r["carimbo_recepcao"])))
    for r in reports:
        r["loc"] = gaz.get(r["place"], "")
        r["muni"] = muni_of.get(r["loc"], ("", "", "", ""))[0]
    exc = [dict(route=r["via"], ident=r["id_relato"], recv=pts(r["carimbo_recepcao"]),
                reason=r["motivo"]) for r in read(target, "excecoes_geocodificacao.csv")]
    sample = read(target, "amostra_dupla_codificacao.csv")
    return dict(reports=reports, exceptions=exc, sample=sample,
                totals=read(target, "totais_por_via.csv"))


def actions(reports):
    """The protocol's 2.1 grain, with the code 2.6 keeps: a filer's where one exists, the press
    monitor's otherwise."""
    acts = {}
    for r in reports:
        if not r["loc"]:
            continue
        k = (r["theme"], r["loc"], r["day"])
        a = acts.setdefault(k, dict(theme=r["theme"], loc=r["loc"], day=r["day"], muni=r["muni"],
                                    routes=set(), press_code="", filer_code="", reports=[]))
        a["routes"].add(r["route"])
        a["reports"].append(r)
        if r["route"] == "IMP":
            a["press_code"] = r["code"]
        elif not a["filer_code"]:
            a["filer_code"] = r["code"]
    out = []
    for a in acts.values():
        a["press_only"] = "IMP" in a["routes"]
        a["code"] = a["press_code"] if a["press_code"] else a["filer_code"]
        a["coded_conf"] = a["code"] in CONF
        out.append(a)
    return sorted(out, key=lambda a: (a["day"], a["loc"], a["theme"]))


def matrix(sample, restrict=None):
    """The classifier's two error rates, from the desk's hand coding."""
    tp = fn = fp = tn = 0
    for r in sample:
        if restrict and r["id_relato"] not in restrict:
            continue
        m, h = r["codigo_monitor"] in CONF, r["codigo_manual"] in CONF
        if h and m:
            tp += 1
        elif h and not m:
            fn += 1
        elif m:
            fp += 1
        else:
            tn += 1
    return tp, fn, fp, tn


def corrected(n, observed, tp, fn, fp, tn, continuity=0.0):
    """The count rebuilt from both error rates: the observed share less what the classifier marks
    wrongly, over the width its two rates leave."""
    se = (tp + continuity) / (tp + fn + 2 * continuity)
    sp = (tn + continuity) / (tn + fp + 2 * continuity)
    return n * (observed / n + sp - 1) / (se + sp - 1), se, sp


def compute(target):
    b = load(target)
    acts = actions(b["reports"])
    inper = [a for a in acts if PERIOD[0] <= a["day"] <= PERIOD[1]]
    press = [a for a in inper if a["press_only"]]
    human = [a for a in inper if not a["press_only"]]
    H = sum(1 for a in human if a["coded_conf"])
    N = len(press)
    O = sum(1 for a in press if a["coded_conf"])
    tp, fn, fp, tn = matrix(b["sample"])
    raw, se, sp = corrected(N, O, tp, fn, fp, tn)
    g = dict(actions_in_period=len(inper), press_only=N, filed_by_hand=len(human),
             hand_confrontational=H, press_marked=O,
             sample_rows=len(b["sample"]), tp=tp, fn=fn, fp=fp, tn=tn,
             recall=round(se, 4), false_mark=round(1 - sp, 4),
             raw_total=H + raw, total=round(H + raw),
             rung0=H + O, rung1=round(H + O * tp / (tp + fp)), raw_rung1=H + O * tp / (tp + fp),
             rung2=round(H + O / se), raw_rung2=H + O / se)
    # the variants a careful analyst tries on a correction of this kind
    cont, _, _ = corrected(N, O, tp, fn, fp, tn, continuity=0.5)
    g["variant_continuity"] = H + cont
    rounds = {}
    for r in b["sample"]:
        rounds.setdefault(r["ronda"], []).append(r["id_relato"])
    per_round, shares = 0.0, {}
    first_round = min(rounds)
    for name, ids in sorted(rounds.items()):
        t2 = matrix(b["sample"], set(ids))
        share = len(ids) / len(b["sample"])
        part, _, _ = corrected(N * share, O * share, *t2)
        per_round += part
        shares[name] = part
    g["variant_by_round"] = H + per_round
    themes = {}
    for a in press:
        themes.setdefault(a["theme"], [0, 0])
        themes[a["theme"]][0] += 1
        themes[a["theme"]][1] += 1 if a["coded_conf"] else 0
    by_theme = 0.0
    for th, (n_th, o_th) in themes.items():
        ids = {r["id_relato"] for r in b["sample"] if r["tema"] == th}
        t2 = matrix(b["sample"], ids)
        if min(t2[0] + t2[1], t2[2] + t2[3]) == 0 or (t2[0] / max(t2[0] + t2[1], 1)) + \
                (t2[3] / max(t2[3] + t2[2], 1)) <= 1:
            part = n_th * (o_th / n_th + sp - 1) / (se + sp - 1)
        else:
            part, _, _ = corrected(n_th, o_th, *t2)
        by_theme += part
    g["variant_by_theme"] = H + by_theme
    press_ids = {a["reports"][0]["ident"] for a in press for r in a["reports"]
                 if r["route"] == "IMP"}
    t3 = matrix(b["sample"], press_ids)
    if t3[0] and t3[1] and t3[3]:
        part, _, _ = corrected(N, O, *t3)
        g["variant_press_only_sample"] = H + part
    else:
        g["variant_press_only_sample"] = H + raw
    # the same correction written as the inverted confusion matrix over the observed counts
    denom = se - (1 - sp)
    g["variant_matrix_inverse"] = H + (O - N * (1 - sp)) / denom

    # ---- A1, per fortnight
    a1 = {}
    for label, a, bb in W.fortnights():
        inside = [x for x in acts if a <= x["day"] <= bb]
        par = [x for x in inside if "PAR" in x["routes"]]
        a1[label] = dict(start=a.isoformat(), end=bb.isoformat(), actions=len(inside),
                         municipalities=len({x["muni"] for x in inside}),
                         partner_share=round(100.0 * len(par) / len(inside), 1) if inside else 0.0,
                         marked=len([x for x in inside if x["coded_conf"]]))
    g["a1"] = a1

    # ---- A2, per access route
    a2 = {}
    for route, _ in W.ROUTES:
        placed, seen = [], set()
        for r in b["reports"]:
            if r["route"] != route or r["ident"] in seen:
                continue
            seen.add(r["ident"])
            placed.append(r)
        in_period = [r for r in placed if PERIOD[0] <= r["recv"].date() <= PERIOD[1]]
        exc = [e for e in b["exceptions"]
               if e["route"] == route and PERIOD[0] <= e["recv"].date() <= PERIOD[1]]
        mins = sorted((r["recv"] - r["start"]).total_seconds() / 60.0 for r in in_period)
        k = len(mins) // 2
        a2[route] = dict(received=len(in_period) + len(exc), unplaceable=len(exc),
                         median_minutes=round(statistics.median(mins), 1) if mins else 0.0,
                         placed=len(in_period),
                         median_pair_equal=bool(mins) and (len(mins) % 2 == 1 or mins[k - 1] == mins[k]))
    g["a2"] = a2

    # ---- A3, per partner organisation
    code_to = {p[0]: p[0] for p in W.PARTNERS}
    code_to[W.MERGED[1]] = W.MERGED[0]
    par_seen = {}
    for r in b["reports"]:
        if r["route"] == "PAR":
            par_seen.setdefault(r["ident"], r)
    a3 = {}
    for code, name, region, rate in W.PARTNERS:
        mine = [r for r in par_seen.values() if code_to.get(r["src"]) == code
                and PERIOD[0] <= r["day"] <= PERIOD[1]]
        late = [r for r in mine if r["recv"].date() > PERIOD[1]]
        paid = 0.0
        for r in mine:
            if r["recv"].date() > PERIOD[1]:
                continue
            use = W.AMENDED[2] if (code == W.AMENDED[0] and r["recv"].date() >= W.AMENDED[1]) else rate
            paid += use
        a3[code] = dict(name=name, filed=len(mine), after_close=len(late), euros=round(paid),
                        raw_euros=paid)
    g["a3"] = a3

    series = []
    for i, label in enumerate(["maio", "junho", "julho", "agosto", "setembro"], 5):
        inside = [x for x in acts if x["day"].month == i and x["day"].year == 2026]
        series.append((label, len(inside), len({x["muni"] for x in inside}),
                       len({x["loc"] for x in inside})))
    g["monthly"] = series
    return g
