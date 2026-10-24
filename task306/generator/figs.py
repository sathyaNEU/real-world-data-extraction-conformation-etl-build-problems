"""Compute every figure the goldens and the write-up state, from the pack alone, and write figures.json."""
import datetime as dt
import json
from collections import defaultdict

import params as P
import solve as S


def compute(target):
    pk = S.Pack(target, P.FILES)
    c = pk.call()
    L = c["lots"]
    fc = c["forecast"]
    total = sum(fc.values())
    reg_only = S.lots(c["base"])
    win = pk.imports(12)
    mira = [x for x in win if x["n"] == "Mira city car"]
    ln = S.Line(target, P.FILES)
    a, b, cc = ln.ask_a(), ln.ask_b(), ln.ask_c()
    # details for the workbook's per-lot sheet
    ships = ln.shipped()
    bp = ln.batch_picks()
    seen, mods = set(), defaultdict(int)
    for r in ln.stores:
        if not S.in_fy(S.stamp(r["geboekt_op"]).date()):
            continue
        key = (r["picklijst"], r["partij"], r["aantal"])
        if r["soort"] == "UITGIFTE" and key in bp:
            if key in seen:
                continue
            seen.add(key)
        n = S.CODE[ln.wo[r["werkorder"]]["platformcode"]]
        mods[n] += int(r["aantal"]) * int(ln.parts[r["artikelnummer"]]["modules_per_eenheid"])
    wo_of = {r["bms_serienummer"]: r["werkorder"] for r in ln.bms}
    first = {}
    for r in sorted(ln.eol, key=lambda r: (r["start"], r["run_id"])):
        if r["resultaat"] != "ABORT":
            first.setdefault(wo_of[r["pakket_id"]], r)
    bdet = {}
    for n in P.NAMES:
        xs = [r for r in first.values() if S.CODE[r["programma"].split("-")[1]] == n and S.in_fy(S.stamp(r["start"]).date())]
        bdet[n] = dict(packs=len(xs), passed=sum(r["resultaat"] == "PASS" for r in xs))
    cdet = ln.ask_c("detail")
    fig = dict(
        slots=L["slots"], margin=round(L["margin"], 3),
        lots_exact={n: round(L["raw"][n], 2) for n in P.NAMES}, floors=L["floors"], extra_lots=L["extra"],
        extra_lot={n: L["slots"][n] // P.LOT > L["floors"][n] for n in P.NAMES},
        remainders={n: round(L["raw"][n] - L["floors"][n], 2) for n in P.NAMES},
        share={n: round(fc[n] / total, 4) for n in P.NAMES},
        base={n: int(round(c["base"][n])) for n in P.NAMES}, base_total=int(round(sum(c["base"].values()))),
        base_exact={n: round(c["base"][n], 2) for n in P.NAMES},
        arrivals_exact={n: round(c["arrivals"].get(n, 0.0), 2) for n in P.NAMES},
        arrivals={n: int(round(c["arrivals"].get(n, 0.0))) for n in P.NAMES},
        arrivals_total=int(round(sum(c["arrivals"].values()))),
        forecast={n: dict(exact=round(fc[n], 1), whole=int(round(fc[n]))) for n in P.NAMES},
        total_exact=round(total, 1), total=int(round(total / 100.0) * 100),
        register_only=dict(slots=reg_only["slots"], total=int(round(sum(c["base"].values()) / 100.0) * 100)),
        window_imports={n: sum(1 for x in win if x["n"] == n) for n in P.NAMES},
        mira_imports_month=int(round(len(mira) / 12.0)),
        mira_import_age=round(sum((x["nl"] - x["fu"]).days / 365.25 for x in mira) / len(mira), 1),
        ask_a={n: int(round(a[n])) for n in P.NAMES}, ask_a_exact={n: round(a[n], 2) for n in P.NAMES},
        ask_b={n: round(b[n], 1) for n in P.NAMES}, ask_b_exact={n: round(b[n], 3) for n in P.NAMES},
        ask_c={n: round(cc[n], 1) for n in P.NAMES}, ask_c_exact={n: round(cc[n], 3) for n in P.NAMES},
        ask_a_detail={n: dict(modules=mods[n], ships=ships[n]) for n in P.NAMES},
        ask_b_detail=bdet, ask_c_detail=cdet,
        warranty=pk.war, slots_total=P.SLOTS, lots_total=P.SLOTS // P.LOT, lot=P.LOT, year_days=365.25,
    )
    return fig


def write(fig, path):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")
