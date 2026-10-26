"""The golden figures, computed forward from the shipped files under target/ (pandas): the planning figure and its
components, the frame family and the golden family, the wrong rungs, ask A (remand holds) and ask B (initial health
assessments) with their stops. Writes generator/figures.json."""
import datetime as dt
import json
import os
import sys
import warnings
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as BD   # noqa: E402

UK = ZoneInfo("Europe/London")
BIN = 250
SUITES = ["Northgate", "Eastmoor", "Southfields", "Wendle Cross"]
REMAND = "Charged - remanded in custody"
WARRANT = "Warrant, recall or breach"


def load(tgt):
    a = pd.read_csv(os.path.join(tgt, BD.F_ARR))
    t = pd.to_datetime(a.arrested_utc, utc=True).dt.tz_convert(UK)
    a["fy"] = np.where(t.dt.month >= 4, t.dt.year, t.dt.year - 1)
    a["ym"] = t.dt.strftime("%Y-%m")
    a["book_utc"] = pd.to_datetime(a.booked_in_utc, utc=True)
    hm = a.detention_hhmm.str.split(":", expand=True).astype(int)
    a["det_min"] = hm[0] * 60 + hm[1]
    a["charge_utc"] = a.book_utc + pd.to_timedelta(a.det_min, unit="m")
    p = pd.read_csv(os.path.join(tgt, BD.F_POL))
    lk = pd.read_csv(os.path.join(tgt, BD.F_LOOK))
    al = pd.read_excel(os.path.join(tgt, BD.F_ALLOC), sheet_name="Allocation")
    return a, p, lk, al


def model(byw, base, ahead, cap=0.10):
    ch = (byw[base] / byw[base - 3]) ** (1 / 3) - 1
    if cap is not None:
        ch = ch.clip(-cap, cap)
    return float((byw[base] * (1 + ch) ** ahead).sum())


def cell(x, b=BIN):
    return int(np.floor(x / b + 0.5)) * b


def edge(x, b=BIN):
    return b / 2 - abs(x - cell(x, b))


def main_call(a, p, lk, al):
    hub = sorted(al[al.suite_from_1_april_2027 == "Tanner Street"].ward)
    ah = a[a.ward.isin(hub)]
    fyt = ah.groupby("fy").size()
    byw = ah.groupby(["ward", "fy"]).size().unstack(fill_value=0)
    force_fy = a.groupby("fy").size()
    mon = ah.groupby("ym").size()
    mon = mon[(mon.index >= "2021-04") & (mon.index <= "2026-09")]
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    hw = ExponentialSmoothing(mon.values.astype(float), trend="add", damped_trend=True, seasonal="add",
                              seasonal_periods=12).fit()
    F = {"F1 the model as filed": model(byw, 2025, 2),
         "F2 2025-26 level": float(fyt[2025]),
         "F3 three-year mean": float(fyt[[2023, 2024, 2025]].mean()),
         "F4 linear trend on five years": float(np.polyval(np.polyfit(range(2021, 2026), fyt[list(range(2021, 2026))].values, 1), 2027)),
         "F5 Holt-Winters damped": float(hw.forecast(18)[6:18].sum()),
         "F6 last twelve months": float(mon[-12:].sum()),
         "F7 the model without its cap": model(byw, 2025, 2, None),
         "F8 2025-26 at the force's change": float(fyt[2025] * (force_fy[2025] / force_fy[2022]) ** (2 / 3)),
         "F9 two-year mean": float(fyt[[2024, 2025]].mean())}
    p = p.merge(lk[["lsoa21_code", "ward"]], left_on="LSOA code", right_on="lsoa21_code", how="left")
    hp = p[p["Reported by"] == "Calderwick Police"]
    bt = p[p["Reported by"] == "British Transport Police"]
    a25 = a[a.fy == 2025]
    ar_t = a25.groupby("offence_group").size()
    cr_t = hp.groupby("Crime type").size()
    rate_t = (ar_t.reindex(cr_t.index) / cr_t).fillna(0)
    warr = ar_t.get(WARRANT, 0) / ar_t.drop(WARRANT, errors="ignore").sum()
    overall = len(a25) / len(hp)
    hub_rate = len(a25[a25.ward.isin(hub)]) / len(hp[hp.ward.isin(hub)])
    bth = bt[bt.ward.isin(hub)]
    b25 = bth.groupby("Crime type").size()
    per_type = float((b25 * rate_t.reindex(b25.index).fillna(0)).sum())
    B = {"B1 per-type rates": per_type,
         "B2 per-type rates with the warrant share": per_type * (1 + warr),
         "B3 the force's overall rate": float(b25.sum() * overall),
         "B4 the six wards' overall rate": float(b25.sum() * hub_rate)}
    G = {}
    for fk in ("F1 the model as filed", "F2 2025-26 level", "F3 three-year mean", "F5 Holt-Winters damped",
               "F6 last twelve months"):
        for bk, bv in B.items():
            G["%s + %s" % (fk.split(" ")[0], bk.split(" ")[0])] = F[fk] + bv
    share = len(bt) / len(p)
    hs = bth[bth.Location.str.contains("Calderwick")]
    R = {"R0 the model as filed": F["F1 the model as filed"],
         "R1 scaled by BTP's share of the street-level file": F["F1 the model as filed"] * (1 + share),
         "R2 every BTP crime in the force area at the overall rate": F["F1 the model as filed"] + len(bt) * overall,
         "R3 Calderwick station only, per-type with the warrant share": F["F1 the model as filed"] +
         float((hs.groupby("Crime type").size() * rate_t).fillna(0).sum()) * (1 + warr)}
    golden_raw = F["F1 the model as filed"] + B["B2 per-type rates with the warrant share"]
    return dict(hub=hub, F=F, B=B, G=G, R=R, golden_raw=golden_raw, golden=cell(golden_raw),
                default_raw=F["F1 the model as filed"], default=cell(F["F1 the model as filed"]),
                fy_hub={int(k): int(v) for k, v in fyt.items() if k <= 2025}, by_ward_fy={w: {int(y): int(byw.loc[w, y]) for y in byw.columns if y <= 2025} for w in hub},
                btp_hub_crimes=int(b25.sum()), btp_hub_by_station={s: int(n) for s, n in bth.Location.value_counts().items()},
                btp_all=int(len(bt)), crime_force=int(len(hp)), share=share, overall=overall, hub_rate=hub_rate,
                warrant_share=warr, rate_t={k: float(v) for k, v in rate_t.items()}, b25={k: int(v) for k, v in b25.items()},
                own_2025=int(fyt[2025]))


# ---------------------------------------------------------------------------------------------------------------
def to_utc_local(s):
    """A UK wall-clock time 'dd/mm/yyyy HH:MM' as UTC; no shipped time sits in an ambiguous or missing hour."""
    t = dt.datetime.strptime(s, "%d/%m/%Y %H:%M")
    return pd.Timestamp(t.replace(tzinfo=UK)).tz_convert("UTC")


def fy_of(ts_utc):
    t = ts_utc.dt.tz_convert(UK)
    return np.where(t.dt.month >= 4, t.dt.year, t.dt.year - 1)


def remand_defendants(a, tgt):
    """Every defendant kept in custody for court on a remand file. A file's own detention is the remanded arrest at the
    file's suite whose charge (booking plus the detention clock) is the file's charge time: the linked arrest itself,
    or, where the linked arrest is an earlier one in the case, the arrest the person was charged on. Its co-defendants
    are the remanded arrests with no file of their own arrested in the same minute, ward and offence group, each
    charged on their own clock and handed to the escort with the file."""
    c = pd.read_csv(os.path.join(tgt, BD.F_CJU))
    c["charged_utc"] = c.charged.map(to_utc_local)
    c["hand_utc"] = c.handed_to_escort.map(to_utc_local)
    c["fy"] = fy_of(c.charged_utc)
    rem = a[a.outcome == REMAND].copy()
    lead = rem.set_index("arrest_ref")
    own = {}
    for f in c.itertuples():             # the linked arrest itself, when it is the remand charged at the file's time
        if f.linked_arrest in lead.index and lead.loc[f.linked_arrest].charge_utc == f.charged_utc \
                and lead.loc[f.linked_arrest].custody_suite == f.custody_suite:
            own[f.urn] = f.linked_arrest
    by_charge = rem[~rem.arrest_ref.isin(set(own.values()))].groupby(["custody_suite", "charge_utc"]).arrest_ref.apply(list).to_dict()
    for f in c.itertuples():             # otherwise the remand charged at the file's suite and time that no file claims
        if f.urn not in own:
            refs = by_charge.get((f.custody_suite, f.charged_utc), [])
            assert len(refs) == 1, (f.urn, refs)
            own[f.urn] = refs[0]
    c["detention"] = c.urn.map(own)
    assert c.detention.is_unique
    rest = rem[~rem.arrest_ref.isin(set(c.detention))]
    inc = rest.groupby(["arrested_utc", "ward", "offence_group"]).arrest_ref.apply(list).to_dict()
    linked = a.set_index("arrest_ref")
    defs, taken = [], set()
    for f in c.itertuples():
        L = lead.loc[f.detention]
        co = inc.get((L.arrested_utc, L.ward, L.offence_group), [])
        taken.update(co)
        for ref in [f.detention] + co:
            r = lead.loc[ref]
            defs.append(dict(urn=f.urn, ref=ref, lead=ref == f.detention, rearrest=f.linked_arrest != f.detention,
                             suite=f.custody_suite, fy=int(fy_of(pd.Series([r.charge_utc]))[0]), arrest_fy=int(r.fy),
                             book=r.book_utc, charge=r.charge_utc, file_charge=f.charged_utc,
                             linked_book=linked.loc[f.linked_arrest].book_utc, hand=f.hand_utc,
                             hand_naive=pd.Timestamp(dt.datetime.strptime(f.handed_to_escort, "%d/%m/%Y %H:%M"), tz="UTC"),
                             det_min=int(r.det_min)))
    d = pd.DataFrame(defs)
    assert d.ref.is_unique
    orphans = rest[~rest.arrest_ref.isin(taken)]
    return c, d, orphans


def holds(x, hand="hand", book="book", charge="charge", clock=False):
    """Per suite: cell hours from charge to handover (to the nearest hour), and how many were held more than 24 hours
    from booking in (or, with clock=True, whose detention clock ran past 24 hours)."""
    out = {}
    for s in SUITES:
        y = x[x.suite == s]
        hrs = float(((y[hand] - y[charge]).dt.total_seconds() / 3600).sum())
        n24 = int((y.det_min > 24 * 60).sum()) if clock else int(((y[hand] - y[book]).dt.total_seconds() / 3600 > 24).sum())
        out[s] = dict(cell_hours_raw=hrs, cell_hours=int(round(hrs)), over_24=n24, defendants=int(len(y)),
                      codefendants=int((~y.lead).sum()), rearrests=int(y.rearrest.sum()))
    return out


def ask_a(a, tgt):
    c, d, orphans = remand_defendants(a, tgt)
    d25 = d[d.fy == 2025]
    out = holds(d25)
    # the file's own rows only, each at the linked arrest's booking and the file's charge time
    fl = d[d.lead & (d.file_charge.map(lambda t: fy_of(pd.Series([t]))[0]) == 2025)]
    stops = {"each file's linked arrest": holds(fl, book="linked_book", charge="file_charge"),
             "files with co-defendants at the file's charge time": holds(d25, book="linked_book", charge="file_charge"),
             "co-defendants on their own clocks, linked arrest's booking": holds(d25, book="linked_book"),
             "the case's own detentions, co-defendants left out": holds(d25[d25.lead]),
             "detention clock for the 24 hours": holds(d25, clock=True),
             "remand file times read as UTC": holds(d25, hand="hand_naive"),
             "defendants arrested in 2025-26": holds(d[d.arrest_fy == 2025]),
             "every file in the extract": holds(d)}
    info = dict(files_2025=int((c.fy == 2025).sum()), files_all=int(len(c)), defendants_2025=int(len(d25)),
                codefendants_2025=int((~d25.lead).sum()), rearrest_files_2025=int((d25.lead & d25.rearrest).sum()),
                orphans=int(len(orphans)), orphans_in_window=int(((orphans.charge_utc >= pd.Timestamp("2025-04-01", tz="UTC"))
                                                                  & (orphans.charge_utc < pd.Timestamp("2026-04-01", tz="UTC"))).sum()))
    return out, stops, info, d


# ---------------------------------------------------------------------------------------------------------------
def quarter(ts):
    return ((ts.dt.month - 4) % 12) // 3 + 1


def closures(a, al):
    """Every stretch of more than three days with no detainee booked into a suite, from the arrest records: the last
    booking before it, the first after it (both as UK times), and the suite the closed suite's own wards were booked
    into meanwhile."""
    home = dict(zip(al.ward, al.suite_to_31_march_2027))
    out = {}
    for s in SUITES:
        b = a[a.custody_suite == s].book_utc.sort_values().reset_index(drop=True)
        gaps = b.diff()
        for j in gaps.index[gaps > pd.Timedelta(days=3)]:
            lo, hi = b[j - 1], b[j]
            inn = a[(a.book_utc > lo) & (a.book_utc < hi) & (a.ward.map(home) == s)]
            host = inn.custody_suite.value_counts().index[0]
            out[s] = dict(last=lo.tz_convert(UK).tz_localize(None), first=hi.tz_convert(UK).tz_localize(None), host=host,
                          own_wards_in_gap=int(len(inn)), at_host=int((inn.custody_suite == host).sum()))
    return out


SHIFTS = ("day", "night")


def shift(ts):
    return np.where((ts.dt.hour >= 7) & (ts.dt.hour < 19), "day", "night")


def ask_b(a, al, tgt):
    """Each suite's initial health assessments in 2025-26, begun in the day (07:00 to 19:00) and at night: one
    assessment per line, except a line that continues the episode's previous assessment at the 07:00 or 19:00
    handover, placed at the suite the clinician's team was working in (a closed suite's team at its host)."""
    h = pd.read_csv(os.path.join(tgt, BD.F_HC))
    h["start"] = pd.to_datetime(h.started)
    h["end"] = pd.to_datetime(h.ended)
    iha = h[h.contact_type == "Initial health assessment"].sort_values(["episode_ref", "start"]).copy()
    prev_end = iha.groupby("episode_ref").end.shift()
    iha["cont"] = (prev_end == iha.start) & iha.start.dt.minute.eq(0) & iha.start.dt.hour.isin([7, 19])
    cl = closures(a, al)

    def placed(x, which=None):
        p = x.suite.copy()
        for s, c in cl.items():
            if which is None or s in which:
                m = (x.suite == s) & (x.start >= c["last"]) & (x.start < c["first"])
                p[m] = c["host"]
        return p

    def grid(x, place):
        g = x.assign(place=place, sh=shift(x.start)).groupby(["place", "sh"]).size()
        return {s: {k: int(g.get((s, k), 0)) for k in SHIFTS} for s in SUITES}

    kept = iha[~iha.cont]
    out = grid(kept, placed(kept))
    first = iha.groupby("episode_ref").head(1)
    stops = {"every line by its suite": grid(iha, iha.suite),
             "handover lines joined, suite as labelled": grid(kept, kept.suite),
             "closures moved, handover lines kept": grid(iha, placed(iha)),
             "one assessment an episode, closures moved": grid(first, placed(first)),
             "one assessment an episode, suite as labelled": grid(first, first.suite),
             "only the Wendle Cross refit moved": grid(kept, placed(kept, {"Wendle Cross"})),
             "only the Eastmoor closure moved": grid(kept, placed(kept, {"Eastmoor"}))}
    info = dict(lines=int(len(iha)), continuations=int(iha.cont.sum()), episodes=int(iha.episode_ref.nunique()),
                repeats=int(len(kept) - kept.episode_ref.nunique()),
                closures={s: {k: str(v) for k, v in c.items()} for s, c in cl.items()},
                moved=int((placed(kept) != kept.suite).sum()))
    return out, stops, info


def figures(tgt):
    a, p, lk, al = load(tgt)
    M = main_call(a, p, lk, al)
    A, A_stops, A_info, _ = ask_a(a, tgt)
    Bq, B_stops, B_info = ask_b(a, al, tgt)
    return dict(M=M, A=A, A_stops=A_stops, A_info=A_info, B=Bq, B_stops=B_stops, B_info=B_info)


def flat(R):
    M = R["M"]
    f = {"call.planning_figure": M["golden"], "call.planning_figure_unrounded": round(M["golden_raw"], 1),
         "components.own_arrests_model": round(M["F"]["F1 the model as filed"], 1),
         "components.own_arrests_2025_26": M["own_2025"],
         "components.btp_crimes_hub_2025_26": M["btp_hub_crimes"],
         "components.btp_detentions": round(M["B"]["B2 per-type rates with the warrant share"], 1),
         "components.default_answer": M["default"],
         "components.warrant_share_pct": round(100 * M["warrant_share"], 1)}
    for st, n in M["btp_hub_by_station"].items():
        f["components.btp_crimes.%s" % st.replace("On or near ", "").replace(" (station)", "")] = n
    for y, n in M["fy_hub"].items():
        f["chart.six_wards_arrests.%d-%02d" % (y, (y + 1) % 100)] = n
    for s in SUITES:
        f["ask_a.%s.cell_hours" % s] = R["A"][s]["cell_hours"]
        f["ask_a.%s.over_24_hours" % s] = R["A"][s]["over_24"]
    f["steps.remand_defendants_2025_26"] = sum(R["A"][s]["defendants"] for s in SUITES)
    for s in SUITES:
        f["steps.remand_defendants.%s" % s] = R["A"][s]["defendants"]
    for s in SUITES:
        for k in SHIFTS:
            f["ask_b.%s.%s" % (s, k)] = R["B"][s][k]
    return f


def main(argv):
    tgt = argv[0] if argv else BD.TARGET
    R = figures(tgt)
    f = flat(R)
    with open(os.path.join(HERE, "figures.json"), "w") as fh:
        json.dump(f, fh, indent=1)
    if len(argv) > 1:                       # the full working, for the author's own reading
        with open(argv[1], "w") as fh:
            json.dump(R, fh, indent=1, default=str)
    return f


if __name__ == "__main__":
    print(json.dumps(main(sys.argv[1:]), indent=1))
