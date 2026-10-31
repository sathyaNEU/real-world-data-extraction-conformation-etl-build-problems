"""Every construction the build grades or prices, computed from the shipped files only: the call (each counted
dwelling's occupancy in the fortnight) and its rungs, the two annex tables and their stops."""
import datetime as dt
import os

import numpy as np
import pandas as pd

import world as W

REF = pd.Timestamp("2026-11-01")
CUT = 0.5          # a household's day: the morning or evening hours above the same day's night hours, in kWh
_CACHE = {}


def load(target):
    if target in _CACHE:
        return _CACHE[target]
    f = lambda k: os.path.join(target, W.FILES[k])
    rd = lambda k, **kw: pd.read_csv(f(k), sep=";", dtype=str, keep_default_na=False, **kw)
    d = {"cad": rd("cadastre"), "mun": rd("municipalities"), "mp": rd("meterpoints"), "reg": rd("register"),
         "ev": rd("events"), "tit": rd("titles"), "trf": rd("transfers"), "ent": rd("entities"), "sh": rd("shareholders")}
    d["hourly"] = pd.read_parquet(f("hourly"))
    _CACHE[target] = d
    return d


def _date(s):
    return pd.to_datetime(s, format="%d.%m.%Y", errors="coerce")


def norm_addr(a):
    return " ".join(str(a).upper().replace(".", " ").split())


def norm_unit(u):
    return str(u).replace(" ", "").upper()


# ---------------------------------------------------------------------------------------------- the call
def counted(d):
    c = d["cad"]
    use = _date(c["tatt_i_bruk"])
    keep = (c["bruksenhetstype"] == "Bolig") & use.notna() & (use <= REF)
    return c[keep].copy()


def meters_of(d):
    """Each household metering point's counted dwelling: by the cadastre's unit id where the point carries it, else
    by the address (the points without an id are single-unit houses)."""
    cnt = counted(d)
    ids = set(cnt["bruksenhet_id"])
    byadr = {}
    for r in cnt.itertuples():
        byadr.setdefault((r.kommunenr, norm_addr("%s %s%s" % (r.adressenavn, r.husnr, r.bokstav))), []).append(r)
    out = {}
    for r in d["mp"].itertuples():
        if r.kundekategori != "Husholdning":
            continue
        if r.bruksenhet_id:
            if r.bruksenhet_id in ids:
                out[int(r.malepunkt_id)] = r.bruksenhet_id
            continue
        cands = byadr.get((r.kommunenr, norm_addr(r.adresse)), [])
        if len(cands) == 1:
            out[int(r.malepunkt_id)] = cands[0].bruksenhet_id
    return out


_MEMO = {}


def series(d, dedupe="latest", clock="local"):
    """Hourly kWh per counted dwelling over the fortnight, a dwelling's metering points summed hour by hour."""
    key = ("series", id(d["hourly"]), id(d["mp"]), id(d["cad"]), dedupe, clock)
    if key not in _MEMO:
        _MEMO[key] = _series(d, dedupe, clock)
    return _MEMO[key]


def _series(d, dedupe, clock):
    h = d["hourly"]
    if dedupe == "latest":
        h = h.sort_values(["malepunkt_id", "fra_tidspunkt_utc", "leveranse"]).drop_duplicates(
            ["malepunkt_id", "fra_tidspunkt_utc"], keep="last")
    elif dedupe == "first":
        h = h.sort_values(["malepunkt_id", "fra_tidspunkt_utc", "leveranse"]).drop_duplicates(
            ["malepunkt_id", "fra_tidspunkt_utc"], keep="first")
    m2d = meters_of(d)
    h = h[h["malepunkt_id"].isin(list(m2d))].copy()
    h["dw"] = h["malepunkt_id"].map(m2d)
    t = h["fra_tidspunkt_utc"].dt.tz_convert(None)
    if clock == "local":
        t = t + pd.Timedelta(hours=W.UTC_OFFSET)
    start = pd.Timestamp(W.FORTNIGHT_START)
    h["hix"] = ((t - start) / pd.Timedelta(hours=1)).astype(int)
    h = h[(h["hix"] >= 0) & (h["hix"] < W.HOURS)]
    g = h.groupby(["dw", "hix"])["forbruk_kwh"].sum().unstack("hix")
    g = g.reindex(columns=range(W.HOURS))
    return g


def signature(g):
    a = g.to_numpy().reshape(len(g), W.DAYS, 24)
    with np.errstate(invalid="ignore"):
        night = np.nanmean(a[:, :, 1:5], axis=2)
        morn = np.nanmean(a[:, :, 6:9], axis=2)
        eve = np.nanmean(a[:, :, 16:22], axis=2)
        rise = np.fmax(morn, eve) - night
    return pd.Series(np.nanmax(np.where(np.isnan(rise), -9, rise), axis=1), index=g.index)


def level(g):
    return pd.Series(np.nansum(g.to_numpy(), axis=1) / W.DAYS, index=g.index)


def registered_nov1(d, handling="golden"):
    """Persons the population register held in each dwelling on 1 November 2026 (ask A's construction, also the
    register rung's input)."""
    key = ("reg", id(d["ev"]), id(d["reg"]), handling)
    if key not in _MEMO:
        _MEMO[key] = persons_nov1(d, handling).groupby("dw").size()
    return _MEMO[key]


def call(d, rule="golden", floor=None):
    """Each municipality's counted dwellings, vacant dwellings and share under one occupancy rule."""
    cnt = counted(d)
    g = series(d)
    s = signature(g).reindex(cnt["bruksenhet_id"]).fillna(-9)
    lv = level(g).reindex(cnt["bruksenhet_id"]).fillna(0.0)
    if rule in ("register", "reg_and_shape", "reg_and_level"):
        reg = registered_nov1(d).reindex(cnt["bruksenhet_id"]).fillna(0)
    if rule == "golden":
        vac = s < CUT
    elif rule == "level":
        vac = lv < floor
    elif rule == "register":
        vac = reg == 0
    elif rule == "reg_and_shape":
        vac = (reg == 0) & (s < CUT)
    elif rule == "reg_and_level":
        vac = (reg == 0) & (lv < floor)
    else:
        raise ValueError(rule)
    cnt = cnt.assign(vacant=vac.to_numpy())
    out = {}
    for nr, name, *_r in W.MUNICIPALITIES:
        sub = cnt[cnt["kommunenr"] == nr]
        v = int(sub["vacant"].sum())
        out[nr] = {"name": name, "counted": len(sub), "vacant": v, "share": round(100.0 * v / len(sub), 1),
                   "raw": 100.0 * v / len(sub)}
    return out, cnt


def designated(res):
    return sorted(nr for nr, r in res.items() if r["share"] >= W.THRESHOLD)


# ---------------------------------------------------------------------------------------------- ask A
def _key(nr, street, no, letter, unit):
    return (str(nr), norm_addr("%s %s%s" % (street, no, letter)), norm_unit(unit))


def renumberings(d):
    """Same-address events on one day that move two or more residents of a building to new unit numbers: the
    cadastre relabelling the block, not anyone moving. Returns the events and, per old label, the new label and the
    day the numbering changed."""
    ev = d["ev"]
    same = ev[(ev["hendelse"] == "Flytting") & (ev["fra_adressenavn"] == ev["til_adressenavn"]) &
              (ev["fra_husnr"] == ev["til_husnr"]) & (ev["fra_bokstav"] == ev["til_bokstav"]) &
              (ev["fra_kommunenr"] == ev["til_kommunenr"]) & (ev["fra_bruksenhetsnr"] != ev["til_bruksenhetsnr"])]
    grp = ["fra_kommunenr", "fra_adressenavn", "fra_husnr", "fra_bokstav", "hendelsesdato"]
    cnt = same.groupby(grp).size()
    blocks = set(i for i, n in cnt.items() if n >= 2)
    rows = same[[tuple(x) in blocks for x in same[grp].itertuples(index=False)]]
    relabel = {}
    for r in rows.itertuples():
        relabel[_key(r.fra_kommunenr, r.fra_adressenavn, r.fra_husnr, r.fra_bokstav, r.fra_bruksenhetsnr)] = (
            _key(r.til_kommunenr, r.til_adressenavn, r.til_husnr, r.til_bokstav, r.til_bruksenhetsnr),
            _date(pd.Series([r.hendelsesdato])).iloc[0])
    return set(rows.index), relabel


def persons_nov1(d, handling="golden"):
    """The register rolled back from the 5 January snapshot to 1 November 2026: each person with the counted
    dwelling they were registered in that day.

    handling: golden (every event after 1 November undone; a block's relabelling kept as a relabelling, and an
    address written before a block's relabelling read in the old numbering); snapshot (the 5 January register as it
    stands); book (every event undone as written, the relabellings as moves); no_deaths (moves undone, the dead and
    emigrated not added back)."""
    reg = d["reg"]
    ev = d["ev"].copy()
    ev["dt"] = _date(ev["hendelsesdato"])
    ev["rdt"] = _date(ev["registrert_dato"])
    snap = pd.Timestamp(W.SNAPSHOT_DAY)
    state = {r.person_lopenr: (_key(r.kommunenr, r.adressenavn, r.husnr, r.bokstav, r.bruksenhetsnr), snap)
             for r in reg.itertuples()}
    renum_idx, relabel = renumberings(d)
    if handling != "snapshot":
        after = ev[ev["dt"] > REF].sort_values(["dt", "rdt", "person_lopenr"], ascending=False)
        for i, r in zip(after.index, after.itertuples()):
            pid = r.person_lopenr
            frm = _key(r.fra_kommunenr, r.fra_adressenavn, r.fra_husnr, r.fra_bokstav, r.fra_bruksenhetsnr)
            if r.hendelse == "Flytting":
                if handling != "book" and i in renum_idx:
                    continue
                if r.fra_adressenavn:
                    state[pid] = (frm, r.dt)
                else:
                    state.pop(pid, None)
            elif r.hendelse in ("Dødsfall", "Utvandring"):
                if handling == "no_deaths":
                    continue
                state[pid] = (frm, r.dt)
            elif r.hendelse in ("Fødsel", "Innvandring"):
                state.pop(pid, None)
    cnt = counted(d)
    idx = {_key(r.kommunenr, r.adressenavn, r.husnr, r.bokstav, r.bruksenhetsnr): r.bruksenhet_id
           for r in cnt.itertuples()}
    rows = []
    for pid, (k, when) in state.items():
        if handling != "book" and k in relabel and when < relabel[k][1]:
            k = relabel[k][0]
        if k in idx:
            rows.append((pid, idx[k], k[0]))
    return pd.DataFrame(rows, columns=["pid", "dw", "nr"])


def birth_dates(d):
    b = dict(zip(d["reg"]["person_lopenr"], _date(d["reg"]["fodselsdato"])))
    ev = d["ev"]
    extra = ev[~ev["person_lopenr"].isin(b.keys())].drop_duplicates("person_lopenr")
    b.update(dict(zip(extra["person_lopenr"], _date(extra["fodselsdato"]))))
    return b


def _age(born, ref):
    if pd.isna(born):
        return -1
    return ref.year - born.year - ((ref.month, ref.day) < (born.month, born.day))


def ask_a(d, handling="golden", age_on="nov1"):
    p = persons_nov1(d, handling)
    born = birth_dates(d)
    ref = REF if age_on == "nov1" else pd.Timestamp(W.SNAPSHOT_DAY)
    p["age"] = [_age(born.get(x), ref) for x in p["pid"]]
    out = {}
    for nr, *_r in W.MUNICIPALITIES:
        a = p[p["nr"] == nr]["age"]
        out[nr] = {"u18": int(((a >= 0) & (a <= 17)).sum()), "18-66": int(((a >= 18) & (a <= 66)).sum()),
                   "67+": int((a >= 67).sum())}
    return out


# ---------------------------------------------------------------------------------------------- ask B
def municipal_holders(d, chain="all", kf=True):
    """Each municipality's organisation numbers under the assignment's definition: the municipality, its municipal
    enterprises, and the companies whose shares it holds all of, itself or through such a company.

    chain: all (the shares the municipality and the companies already in the set hold between them, all of them);
    single (one holder in the set holding all the shares); none (the municipality and its enterprises only)."""
    ent = d["ent"]
    mun = dict(zip(d["mun"]["kommunenavn"].str.upper(), d["mun"]["kommunenr"]))
    sh = d["sh"].assign(n=d["sh"]["antall_aksjer"].astype(int), tot=d["sh"]["antall_aksjer_selskap"].astype(int))
    out = {}
    for r in ent[ent["organisasjonsform"] == "KOMM"].itertuples():
        nr = mun[r.navn[:-len(" KOMMUNE")]]
        held = {r.organisasjonsnummer}
        if kf:
            held |= set(ent[(ent["organisasjonsform"] == "KF") & (ent["overordnet_enhet"] == r.organisasjonsnummer)]
                        ["organisasjonsnummer"])
        while chain != "none":
            mine = sh[sh["aksjonaer_id"].isin(held)]
            if chain == "all":
                g = mine.groupby("orgnr_selskap").agg(n=("n", "sum"), tot=("tot", "first"))
                new = set(g[g["n"] >= g["tot"]].index) - held
            else:
                new = set(mine[mine["n"] >= mine["tot"]]["orgnr_selskap"]) - held
            if not new:
                break
            held |= new
        out[nr] = held
    return out


def own_name(name, muni):
    """A title holder's name that is the municipality itself (the titles from before the business register carry it
    in the form of their day, without an organisation number)."""
    import re
    return re.match(r"^%s (?:BY|HERREDS)?KOMMUNE\b" % re.escape(muni.upper()), name.upper()) is not None


def holders_nov1(d, basis="tinglyst"):
    """Each title's holder (id, name) on 1 November 2026: the 5 January titles with the transfers registered after
    the register day undone (basis tinglyst); by the deed's date instead (dokument); or the titles as they stand
    (snapshot)."""
    t = d["tit"]
    hold = {(r.kommunenr, r.gardsnr, r.bruksnr, r.seksjonsnr): (r.hjemmelshaver_id, r.hjemmelshaver_navn)
            for r in t.itertuples()}
    if basis == "snapshot":
        return hold
    trf = d["trf"].copy()
    trf["dt"] = _date(trf["tinglyst_dato" if basis == "tinglyst" else "dokumentdato"])
    trf["reg"] = _date(trf["tinglyst_dato"])
    for r in trf.sort_values(["reg", "dt"], ascending=False).itertuples():
        if r.dt > REF:
            hold[(r.kommunenr, r.gardsnr, r.bruksnr, r.seksjonsnr)] = (r.avgiver_id, r.avgiver_navn)
    return hold


def ask_b(d, basis="tinglyst", chain="all", kf=True, names="golden", unit="dwelling"):
    """Each municipality's counted dwellings held on the land register on 1 November 2026 by the municipality or a
    company it owns.

    names: golden (a title without an organisation number counts where its holder's name is the municipality's
    own); none (titles matched by organisation number only); exact (a title without a number matched to the
    business register by its exact name); startswith (every holder, with or without a number, whose name begins
    with the municipality's name). unit: dwelling (the counted dwellings) or title (the titles they sit under)."""
    cnt = counted(d)
    hold = holders_nov1(d, basis)
    mh = municipal_holders(d, chain=chain, kf=kf)
    ent_names = dict(zip(d["ent"]["organisasjonsnummer"], d["ent"]["navn"]))
    by_name = {v: k for k, v in ent_names.items()}
    mname = dict(zip(d["mun"]["kommunenr"], d["mun"]["kommunenavn"]))
    out = {}
    for nr, *_r in W.MUNICIPALITIES:
        sub = cnt[cnt["kommunenr"] == nr]
        seen = set()
        n = 0
        for r in sub.itertuples():
            k = (r.kommunenr, r.gardsnr, r.bruksnr, r.seksjonsnr)
            if k not in hold:
                k = (r.kommunenr, r.gardsnr, r.bruksnr, "")
            hid, hname = hold.get(k, ("", ""))
            if names == "startswith":
                full = ent_names.get(hid, hname) if hid else hname
                ok = full.upper().startswith(mname[nr].upper() + " ")
            elif hid:
                ok = hid in mh.get(nr, set())
            elif names == "golden":
                ok = own_name(hname, mname[nr])
            elif names == "exact":
                ok = by_name.get(hname) in mh.get(nr, set())
            else:
                ok = False
            if ok:
                if unit == "title":
                    if k in seen:
                        continue
                    seen.add(k)
                n += 1
        out[nr] = n
    return out
