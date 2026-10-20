"""The golden files: adjusted_population_supplement_2027.csv in the ministry's delivery layout and the chart of the
adjusted resident populations against the 5,000 line; and generator/figures.json, every figure the write-up states."""
import csv
import io
import json
import os

import bundle as B
import methods as M
import world as W

CSV_NAME = "adjusted_population_supplement_2027.csv"
PNG_NAME = "adjusted_population_supplement_2027.png"
COLS = ["MUNICIPALITY_CODE", "MUNICIPALITY", "REGISTERED_20260101", "NOT_RESIDENT_ESTIMATE", "ADJUSTED_POPULATION",
        "QUALIFIES", "DEPARTURES_ABROAD_2025", "DEATHS_2025"]


def cells(pk):
    """the audit's absence rate in each stratum of the golden: current stay band by earlier departure"""
    out = {}
    key = M.RUNGS[M.GOLDEN]
    for f, a in pk.audit:
        k = key(f)
        n, x = out.get(k, (0, 0))
        out[k] = (n + 1, x + a)
    label = {None: "never settled from abroad", 0: "under 1 year", 1: "1 to 4 years", 2: "5 to 9 years",
             3: "10 years or more"}
    rows = []
    for (b, left), (n, x) in sorted(out.items(), key=lambda kv: (-1 if kv[0][0] is None else kv[0][0], kv[0][1])):
        rows.append(dict(stay=label[b], left_before=bool(left), sampled=n, absent=x, rate=round(x / n, 6)))
    return rows


def compute(target):
    pk = B.Pack(target)
    g = pk.golden()
    dep, dth = pk.departures(), pk.deaths()
    munis = []
    for m in sorted(pk.codes):
        munis.append(dict(code=m, gm="GM" + m, name=W.NAME[m], registered=g[m]["registered"],
                          not_resident=g[m]["not_resident"], adjusted=g[m]["rounded"],
                          adjusted_exact=round(g[m]["adjusted"], 3), qualifies=g[m]["qualifies"],
                          departures=dep[m], deaths=dth[m]))
    q = sorted(x["name"] for x in munis if x["qualifies"])
    absent = sum(a for _, a in pk.audit)
    rungs = {}
    for name in list(M.RUNGS):
        s = pk.qualifying(name)
        rungs[name] = dict(count=len(s), names=sorted(W.NAME[m] for m in s))
    reg_only = sorted(W.NAME[m] for m in pk.codes if len(pk.pops[m]) < M.LINE)
    rungs["R0 register count"] = dict(count=len(reg_only), names=reg_only)
    career = {"never": [0, 0], "stayed": [0, 0], "returned": [0, 0]}
    for f, x in pk.audit:
        k = "never" if f["stay"] is None else "returned" if f["left"] else "stayed"
        career[k][0] += 1
        career[k][1] += x
    towns = []
    for m in sorted(pk.codes, key=lambda m: W.NAME[m]):
        if W.TYPE[m] == "T":
            continue
        mig = [f for f in pk.pops[m] if f["stay"] is not None]
        towns.append(dict(name=W.NAME[m], type=W.TYPE[m], registered=len(pk.pops[m]), settled=len(mig),
                          left=sum(f["left"] for f in mig), stay_1_4=sum(1 for f in mig if 1 <= f["stay"] <= 4)))
    fig = dict(
        call=dict(names=q, count=len(q)),
        municipalities=munis,
        audit=dict(sampled=len(pk.audit), absent=absent, share_pct=round(100.0 * absent / len(pk.audit), 2),
                   cells=cells(pk), by_career=career,
                   by_career_pct={k: round(100.0 * v[1] / v[0], 2 if k == "never" else 1) for k, v in career.items()},
                   result_codes=dict(absent=[20, 30, 40], present_left=50, no_contact=91)),
        career_towns=towns,
        asks=dict(departures={x["name"]: x["departures"] for x in munis}, deaths={x["name"]: x["deaths"] for x in munis}),
        totals=dict(registered=sum(x["registered"] for x in munis), not_resident=sum(x["not_resident"] for x in munis),
                    departures=sum(x["departures"] for x in munis), deaths=sum(x["deaths"] for x in munis)),
        rungs=rungs,
        line=M.LINE,
        nearest=dict(below=max((x for x in munis if x["qualifies"]), key=lambda x: x["adjusted"])["name"],
                     above=min((x for x in munis if not x["qualifies"]), key=lambda x: x["adjusted"])["name"]),
    )
    return fig


def write_csv(path, fig):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(COLS)
    for x in fig["municipalities"]:
        w.writerow([x["gm"], x["name"], x["registered"], x["not_resident"], x["adjusted"], "Y" if x["qualifies"] else "N",
                    x["departures"], x["deaths"]])
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(buf.getvalue())


def write_chart(path, fig):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    rcParams["font.family"] = "Liberation Sans"
    rcParams["svg.hashsalt"] = "task471"
    xs = sorted(fig["municipalities"], key=lambda x: x["adjusted"])
    fig_, ax = plt.subplots(figsize=(9.0, 7.4), dpi=150)
    colors = ["#b5523b" if x["qualifies"] else "#8a9aab" for x in xs]
    y = range(len(xs))
    ax.barh(list(y), [x["adjusted"] for x in xs], color=colors, height=0.68, zorder=2)
    ax.set_yticks(list(y))
    ax.set_yticklabels([x["name"] for x in xs], fontsize=8.5)
    ax.set_xlim(4300, 6000)
    ax.set_ylim(-0.7, len(xs) + 0.4)
    ax.axvline(M.LINE, color="#1f3a5f", linewidth=1.3, zorder=3)
    ax.text(M.LINE + 10, len(xs) - 0.15, "5,000: the supplement line", color="#1f3a5f", fontsize=8.5, va="center")
    for i, x in enumerate(xs):
        if x["qualifies"]:
            ax.text(x["adjusted"] - 10, i, "{:,}".format(x["adjusted"]), va="center", ha="right", fontsize=7.4,
                    color="white", zorder=4)
        else:
            ax.text(x["adjusted"] + 8, i, "{:,}".format(x["adjusted"]), va="center", fontsize=7.4, color="#30363d",
                    zorder=4)
    ax.set_xlabel("Adjusted resident population, 1 January 2026 (persons)", fontsize=9)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: "{:,}".format(int(v))))
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="x", color="#e3e6ea", zorder=0)
    n = fig["call"]["count"]
    ax.set_title("%s of the 24 municipalities in play fall below 5,000 adjusted residents" % (
        {9: "Nine", 8: "Eight", 10: "Ten", 7: "Seven"}.get(n, str(n))), fontsize=11.5, loc="left", pad=12)
    ax.text(0, -0.085, "Bars in red qualify for the 2027 small-municipality supplement (Municipal Fund Regulation 2027, "
            "Article 14). Register count at the start of 1 January 2026 less the registered persons estimated from "
            "the Register Coverage Audit 2026 not to have been living there.", transform=ax.transAxes, fontsize=7.2,
            color="#5b6067", wrap=True, va="top")
    fig_.tight_layout()
    fig_.savefig(path, metadata={"Software": None, "Creation Time": None})
    plt.close(fig_)


def main(target, gdir, fig_path):
    os.makedirs(gdir, exist_ok=True)
    fig = compute(target)
    write_csv(os.path.join(gdir, CSV_NAME), fig)
    write_chart(os.path.join(gdir, PNG_NAME), fig)
    with open(fig_path, "w", encoding="utf-8") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")
    return fig
