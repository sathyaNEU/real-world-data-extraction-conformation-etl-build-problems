"""figures.json: every owed figure, computed from the pack by solve.py."""
import datetime as dt
import json

import params as P
import solve as SV


def whole(x):
    return int(x + 0.5) if x >= 0 else -int(-x + 0.5)


def compute(target):
    c = SV.call(target)
    a = SV.asks(target)
    names = {k: n for k, n, _, _ in P.LOCALITIES}
    g = c["routes"]["golden"]
    since = P.OFF_FROM.replace(year=P.OFF_FROM.year - 2)
    recent = {k: sum(1 for p in c["users"] if c["where"][p] == k and c["starts"]["golden"][p] >= since)
              for k in names}
    w, r = c["winner"], c["runner"]
    reg, _ = SV.register(target)
    moved = sorted({t["practice_code"] for t in SV.read(SV.os.path.join(target, P.FILES["templates"]))
                    if t["migration_source_ref"]})
    assert len(moved) == 1, moved
    mrow = [x for x in reg if x["Practice code"] == moved[0]][0]
    mcode, mname, mloc = moved[0], mrow["Practice name"], mrow["Locality code"]
    fig = dict(
        winner=w, winner_name=names[w], avoided=round(g[w], 4), avoided_r=whole(g[w]),
        runner=r, runner_name=names[r], runner_avoided=round(g[r], 4), runner_avoided_r=whole(g[r]),
        gap=round(g[w] - g[r], 4), gap_r=whole(g[w] - g[r]),
        others_max_r=max(whole(g[k]) for k in g if k not in (w, r)),
        n_users=len(c["users"]), stop_pct=int(P.STOP * 100), base=P.BASE,
        rr=[[m, v] for m, v in P.RR], recent_since=since.isoformat(),
        localities={k: dict(name=names[k], users=c["n_users"][k], recent=recent[k], avoided=round(g[k], 4),
                            avoided_r=whole(g[k])) for k in names},
        routes={k: {l: round(v, 4) for l, v in rt.items()} for k, rt in c["routes"].items()},
        asks=a,
        ask_totals={f: sum(a[k][f] for k in a) for f in ("falls_65_79", "falls_80", "bed_days", "readmitted")},
        migrated=mloc, migrated_name=names[mloc], migrated_practice=mcode, migrated_practice_name=mname,
        winner_mid=sum(1 for p in c["users"] if c["where"][p] == w and since <= c["starts"]["golden"][p] < P.EXTRACT_FROM),
        extract_from=P.EXTRACT_FROM.isoformat(), off_from=P.OFF_FROM.isoformat(), off_to=P.OFF_TO.isoformat(),
        constants=dict(age_min=65, age_band_top=79, age_band_80=80, readmit_days=30, days_in_year=365, per_100=100,
                       destination_another_hospital=51, transfer_method=81, months_bands=[6, 24]),
    )
    return fig


def write(fig, path):
    with open(path, "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
        fh.write("\n")
