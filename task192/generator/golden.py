"""Everything the bulletin owes, computed from the shipped bundle and nothing else.

The actions are rebuilt from the three access routes the way the protocol says, the code the register
keeps for each action is taken on 2.6, and the period's confrontational actions are counted every way
the record leaves open: the codes as they stand, the codes with the classifier's false marks taken
out, the codes scaled by its recall, the audited reports' own confrontational shares carried onto the
record, and the count rebuilt from the classifier's two measured error rates.
"""
import csv
import datetime as dt
import os
import statistics

import world as W

CONF = set(W.CONFRONTATIONAL)
PERIOD = (W.PERIOD_FROM, W.PERIOD_TO)
GRAIN = 50                                  # the bulletin states the indicator to the nearest 50


def read(target, name):
    with open(os.path.join(target, name), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def pdate(s):
    return dt.date.fromisoformat(s[:10])


def pts(s):
    s = s.strip().rstrip("Z").replace("T", " ")
    return dt.datetime.strptime(s[:16], "%Y-%m-%d %H:%M")


def offset(district, local_day):
    summer = local_day < W.DST_BACK
    pair = W.OFFSET_AZORES if district == W.AZORES_DISTRICT else W.OFFSET_MAINLAND
    return pair[0] if summer else pair[1]


def to_lisbon(utc_moment):
    return utc_moment + dt.timedelta(hours=offset("Lisboa", utc_moment.date()))


def grain(x):
    return int(round(x / float(GRAIN))) * GRAIN


def load(target):
    gaz, muni_of = {}, {}
    for r in read(target, "gazeteiro_localidades.csv"):
        gaz[r["nome"]] = r["codigo_localidade"]
        muni_of[r["codigo_localidade"]] = (r["codigo_municipio"], r["municipio"], r["distrito"],
                                           r["regiao"])
    reports, first_item = [], {}
    for r in read(target, "registo_itens_imprensa.csv"):
        if r["estado"] != "aceite":
            continue
        m = pts(r["carimbo_recepcao"])
        if r["id_relato"] in first_item:
            first_item[r["id_relato"]] = min(first_item[r["id_relato"]], m)
            continue
        first_item[r["id_relato"]] = m
        reports.append(dict(route="IMP", ident=r["id_relato"], src=r["orgao"], theme=r["tema"],
                            code=r["codigo_acao"], place=r["local_texto"],
                            day=pdate(r["data_ocorrencia"]), start=pts(r["inicio_acao"]),
                            recv_utc=None))
    for r in reports:
        r["recv_utc"] = first_item[r["ident"]]
    for r in read(target, "relatos_rede_parceiros.csv"):
        reports.append(dict(route="PAR", ident=r["id_relato"], src=r["codigo_parceiro"],
                            theme=r["tema"], code=r["codigo_acao"], place=r["local_texto"],
                            day=pdate(r["data_ocorrencia"]), start=pts(r["inicio_acao"]),
                            recv_utc=pts(r["carimbo_entrega_utc"]), load=r["id_carga"]))
    for r in read(target, "relatos_linha_publica.csv"):
        local = pts(r["carimbo_recepcao"])
        reports.append(dict(route="LIN", ident=r["id_relato"], src="LIN", theme=r["tema"],
                            code=r["codigo_acao"], place=r["local_texto"],
                            day=pdate(r["data_ocorrencia"]), start=pts(r["inicio_acao"]),
                            recv_utc=local - dt.timedelta(hours=offset("Lisboa", local.date()))))
    for r in reports:
        r["loc"] = gaz.get(r["place"], "")
        info = muni_of.get(r["loc"], ("", "", "", ""))
        r["muni"], r["district"] = info[0], info[2]
        r["recv"] = to_lisbon(r["recv_utc"])
        if r["loc"]:
            start_utc = r["start"] - dt.timedelta(hours=offset(r["district"], r["start"].date()))
            r["lag"] = (r["recv_utc"] - start_utc).total_seconds() / 60.0
        else:
            r["lag"] = None
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
                                    district=r["district"], routes=set(), press_code="",
                                    filer_code="", idents=set(), reports=[]))
        a["routes"].add(r["route"])
        a["reports"].append(r)
        if r["route"] == "IMP":
            a["press_code"] = r["code"]
            a["idents"].add(r["ident"])
        elif not a["filer_code"]:
            a["filer_code"] = r["code"]
    out = []
    for a in acts.values():
        a["press_only"] = "IMP" in a["routes"]
        a["code"] = a["press_code"] if a["press_code"] else a["filer_code"]
        a["coded_conf"] = a["code"] in CONF
        out.append(a)
    return sorted(out, key=lambda a: (a["day"], a["loc"], a["theme"]))


def matrix(sample, keep=None):
    """The classifier's four cells, from the desk's hand coding."""
    tp = fn = fp = tn = 0
    for r in sample:
        if keep is not None and not keep(r):
            continue
        m, h = r["codigo_monitor"] in CONF, r["codigo_manual"] in CONF
        if h and m:
            tp += 1
        elif h:
            fn += 1
        elif m:
            fp += 1
        else:
            tn += 1
    return tp, fn, fp, tn


def rogan_gladen(n, marked, cells, continuity=0.0):
    """The count rebuilt from both error rates: the marked count less what the classifier marks
    wrongly, over the width its two rates leave."""
    tp, fn, fp, tn = cells
    if (tp + fn) == 0 or (fp + tn) == 0:
        return None, None, None
    se = (tp + continuity) / (tp + fn + 2 * continuity)
    fmr = (fp + continuity) / (fp + tn + 2 * continuity)
    if se - fmr <= 0:
        return None, se, fmr
    return (marked - fmr * n) / (se - fmr), se, fmr


def predictive(n, marked, cells):
    """The audited reports' own confrontational shares, by what the classifier said, carried onto
    the record."""
    tp, fn, fp, tn = cells
    if (tp + fp) == 0 or (fn + tn) == 0:
        return None
    return marked * tp / float(tp + fp) + (n - marked) * fn / float(fn + tn)


def strata(press, sample, key_action, key_row, fun, fallback=None):
    """A stratified estimate. Returns None when any stratum of the population the correction applies
    to has no rate the sample can give it."""
    groups = {}
    for a in press:
        k = key_action(a)
        groups.setdefault(k, [0, 0])
        groups[k][0] += 1
        groups[k][1] += 1 if a["coded_conf"] else 0
    total, broken = 0.0, []
    for k, (n, marked) in sorted(groups.items(), key=lambda kv: str(kv[0])):
        cells = matrix(sample, lambda r: key_row(r) == k)
        v = fun(n, marked, cells)
        if isinstance(v, tuple):
            v = v[0]
        if v is None or v < 0 or v > n:
            broken.append(str(k))
            if fallback is None:
                continue
            v = fallback(n, marked)
            if isinstance(v, tuple):
                v = v[0]
        total += v
    if broken and fallback is None:
        return None, broken
    return total, broken


def compute(target):
    b = load(target)
    acts = actions(b["reports"])
    inper = [a for a in acts if PERIOD[0] <= a["day"] <= PERIOD[1]]
    press = [a for a in inper if a["press_only"]]
    human = [a for a in inper if not a["press_only"]]
    H = sum(1 for a in human if a["coded_conf"])
    N = len(press)
    O = sum(1 for a in press if a["coded_conf"])
    sample = b["sample"]
    cells = matrix(sample)
    tp, fn, fp, tn = cells
    raw, se, fmr = rogan_gladen(N, O, cells)
    g = dict(actions_in_period=len(inper), press_only=N, filed_by_hand=len(human),
             hand_confrontational=H, press_marked=O,
             sample_rows=len(sample), tp=tp, fn=fn, fp=fp, tn=tn,
             recall=round(se, 4), false_mark=round(fmr, 4),
             raw_total=H + raw, total=grain(H + raw), grain=GRAIN)

    # ---- the routes the record leaves standing, each one a complete pipeline on the same rows
    pv = predictive(N, O, cells)
    sid = {r["id_relato"] for r in sample}
    hand_true = sum(1 for r in sample if r["codigo_manual"] in CONF)
    unsampled_marked = sum(1 for a in press if a["coded_conf"] and not (a["idents"] & sid))
    cont, _, _ = rogan_gladen(N, O, cells, continuity=0.5)
    uns = [a for a in press if not (a["idents"] & sid)]
    hyb, _, _ = rogan_gladen(len(uns), sum(1 for a in uns if a["coded_conf"]), cells)
    g["raw_rung0"] = float(H + O)
    g["raw_rung1"] = H + O * tp / float(tp + fp)
    g["raw_rung1b"] = H + O - fmr * N
    g["raw_rung2"] = H + O / se
    g["raw_rung3"] = H + pv
    g["raw_rung4"] = H + (tp + fn) / float(len(sample)) * N
    g["raw_rung5"] = float(H + hand_true + unsampled_marked)
    g["rung0"] = grain(g["raw_rung0"])
    g["rung1"] = grain(g["raw_rung1"])
    g["rung2"] = grain(g["raw_rung2"])
    g["rung3"] = grain(g["raw_rung3"])
    g["rung4"] = grain(g["raw_rung4"])
    g["rung5"] = grain(g["raw_rung5"])
    g["variant_continuity"] = H + cont
    g["variant_matrix_inverse"] = H + (O - N * fmr) / (se - fmr)
    g["variant_hybrid"] = H + hand_true + hyb

    # the stratified families: the autumn has no audited report in it, so none of them has a rate
    # for every stratum of the population it is applied to
    month_a = lambda a: a["day"].month
    month_r = lambda r: pdate(r["data_ocorrencia"]).month
    theme_a = lambda a: a["theme"]
    theme_r = lambda r: r["tema"]
    rg_only = lambda n, m, c: rogan_gladen(n, m, c)[0]
    pooled_rg = lambda n, m: rogan_gladen(n, m, cells)[0]
    pooled_pv = lambda n, m: predictive(n, m, cells)
    g["dead"] = {}
    for name, ka, kr, fun in (("rg_by_month", month_a, month_r, rg_only),
                              ("rg_by_theme", theme_a, theme_r, rg_only),
                              ("pv_by_month", month_a, month_r, predictive),
                              ("pv_by_theme", theme_a, theme_r, predictive)):
        v, broken = strata(press, sample, ka, kr, fun)
        g["dead"][name] = dict(value=v, broken=broken)
    for name, ka, kr, fun, fb in (("rg_fb_month", month_a, month_r, rg_only, pooled_rg),
                                  ("rg_fb_theme", theme_a, theme_r, rg_only, pooled_rg),
                                  ("pv_fb_month", month_a, month_r, predictive, pooled_pv),
                                  ("pv_fb_theme", theme_a, theme_r, predictive, pooled_pv)):
        v, broken = strata(press, sample, ka, kr, fun, fb)
        g["variant_" + name] = H + v

    # what a solver sees in the record and in the audit
    marked_by_month, audit_by_month = {}, {}
    for a in press:
        m = a["day"].month
        marked_by_month.setdefault(m, [0, 0])
        marked_by_month[m][0] += 1
        marked_by_month[m][1] += 1 if a["coded_conf"] else 0
    for r in sample:
        m = pdate(r["data_ocorrencia"]).month
        audit_by_month.setdefault(m, [0, 0])
        audit_by_month[m][0] += 1
        audit_by_month[m][1] += 1 if r["codigo_manual"] in CONF else 0
    g["marked_by_month"] = marked_by_month
    g["audit_by_month"] = audit_by_month
    g["audit_rounds"] = {}
    for name in sorted({r["ronda"] for r in sample}):
        rows = [r for r in sample if r["ronda"] == name]
        c = matrix(rows, None)
        g["audit_rounds"][name] = dict(rows=len(rows), cells=c,
                                       prevalence=(c[0] + c[1]) / float(len(rows)),
                                       recall=c[0] / float(c[0] + c[1]) if (c[0] + c[1]) else None,
                                       false_mark=c[2] / float(c[2] + c[3]) if (c[2] + c[3]) else None)
    g["audit_covers"] = sorted(audit_by_month)
    inside = [m for m in marked_by_month if m in audit_by_month]
    outside = [m for m in marked_by_month if m not in audit_by_month]
    g["marked_rate_inside"] = (sum(marked_by_month[m][1] for m in inside)
                               / float(sum(marked_by_month[m][0] for m in inside)))
    g["marked_rate_outside"] = (sum(marked_by_month[m][1] for m in outside)
                                / float(sum(marked_by_month[m][0] for m in outside)))
    g["audit_prevalence"] = (tp + fn) / float(len(sample))
    g["record_prevalence"] = (H + raw) / float(len(inper))

    # ---- A1, per fortnight
    a1 = {}
    for label, a, bb in W.fortnights():
        inside = [x for x in acts if a <= x["day"] <= bb]
        par = [x for x in inside if "PAR" in x["routes"]]
        a1[label] = dict(start=a.isoformat(), end=bb.isoformat(), actions=len(inside),
                         municipalities=len({x["muni"] for x in inside}),
                         partner_share=round(100.0 * len(par) / len(inside), 1) if inside else 0.0,
                         partner_actions=len(par),
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
        mins = sorted(r["lag"] for r in in_period if r["lag"] is not None)
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
