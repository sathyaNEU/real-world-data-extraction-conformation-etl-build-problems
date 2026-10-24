"""The call's records from the world: the RDW register extract of 30 June 2026 (cars of the five platforms in use), the
traction-battery replacement log (the OEMs' EU-wide dealer records matched to the Dutch registration by VIN, and
Voltwerk's own fittings) and the published life curves."""
import numpy as np
import pandas as pd

import params as P
import world as Wd

LETTERS = list("BDFGHJKLNPRSTVXZ")


def _sidecode(rs, d):
    """a Dutch plate of the series issued on the day of first registration in the Netherlands (no dashes)"""
    L = lambda k: "".join(rs.choice(LETTERS, k))
    N = lambda k: str(int(rs.integers(1, 10))) + "".join(str(x) for x in rs.integers(0, 10, k - 1))
    y = d.year + (d.timetuple().tm_yday - 1) / 366.0
    if y < 2015.4:
        return L(2) + N(3) + L(1)                 # sidecode 9
    if y < 2019.6:
        return L(1) + N(3) + L(2)                 # sidecode 10
    if y < 2022.7:
        return L(3) + N(2) + L(1)                 # sidecode 11
    return L(1) + N(2) + L(3)                     # sidecode 12


def plates(W):
    """one unique plate per car ever registered in the Netherlands up to the register's date (exited cars too)"""
    rs = np.random.default_rng([P.SEED_REG, 1])
    idx = np.where((W["nl"] <= Wd.SNAP) & W["alive"])[0]
    order = idx[np.argsort(W["nl"][idx], kind="stable")]
    seen, out = set(), {}
    for i in order:
        d = Wd.date(W["nl"][i])
        while True:
            k = _sidecode(rs, d)
            if k not in seen:
                break
        seen.add(k)
        out[int(i)] = k
    return out


def register(W, plate):
    """the cars in use on 30 June 2026: registered here by then and not scrapped or exported before it"""
    rs = np.random.default_rng([P.SEED_REG, 2])
    reg = np.where(W["keep"] & (W["nl"] <= Wd.SNAP))[0]
    rows = []
    colours = ["GRIJS", "ZWART", "WIT", "BLAUW", "ROOD", "ZILVER", "GROEN", "BRUIN"]
    cw = np.array([0.27, 0.22, 0.2, 0.12, 0.07, 0.06, 0.03, 0.03])
    for i in reg:
        name = P.NAMES[W["plat"][i]]
        fu, nl = Wd.date(W["fu"][i]), Wd.date(W["nl"][i])
        tr = P.TRADE[name]
        hb = tr[rs.choice(len(tr), p=[w for _, w in tr])][0]
        # the latest change of holder: the first registration here, or a sale since
        last = nl
        if rs.random() < min(0.85, 0.12 * ((Wd.SNAP - W["nl"][i]) / 365.25)):
            span = max(1, Wd.SNAP - W["nl"][i] - 20)
            last = Wd.date(W["nl"][i] + 20 + int(rs.integers(0, span)))
        age = (P.SNAP - fu).days / 365.25
        if age < 4:
            apk = Wd.date(W["fu"][i] + int(round(4 * 365.25)))
        else:
            apk = Wd.date(Wd.SNAP + int(rs.integers(20, 700 if age < 8 else 360)))
        price = "" if W["imp"][i] and rs.random() < 0.35 else int(round(P.PRICE[name] * (1 + 0.04 * (fu.year - 2018)) / 10) * 10)
        rows.append(dict(
            kenteken=plate[int(i)],
            voertuigsoort=P.SOORT.get(name, "Personenauto"),
            merk=P.MERK[name],
            handelsbenaming=hb,
            datum_eerste_toelating=fu.strftime("%Y%m%d"),
            datum_eerste_tenaamstelling_in_nederland=nl.strftime("%Y%m%d"),
            datum_tenaamstelling=last.strftime("%Y%m%d"),
            vervaldatum_apk=apk.strftime("%Y%m%d"),
            inrichting=P.INRICHTING[name],
            eerste_kleur=colours[rs.choice(len(colours), p=cw)],
            aantal_zitplaatsen=P.SEATS[name],
            massa_rijklaar=int(P.MASS[name] + rs.integers(-25, 40)),
            catalogusprijs=price,
            europese_voertuigcategorie="N1" if name == "Tern van" else "M1",
            taxi_indicator="Ja" if (name in ("Kestrel SUV", "Plover saloon") and rs.random() < 0.035) else "Nee",
        ))
    df = pd.DataFrame(rows).sort_values("kenteken", kind="stable").reset_index(drop=True)
    return df, reg


def replacement_log(W, ev, plate):
    """every pack replacement on a car registered here by the register's date, from first admission: abroad from the
    OEMs' EU-wide dealer records, here from the dealers' and Voltwerk's own; a car scrapped or exported before the
    register's date is in the log up to its exit"""
    rs = np.random.default_rng([P.SEED_LOG, 1])
    rb = np.random.default_rng([P.SEED_LOG, 2])
    e = ev[ev.i.isin(list(plate))].copy()
    e = e[e.d.values <= np.minimum(W["exit_d"][e.i.values], Wd.SNAP)]
    e = e.sort_values(["d", "i"], kind="stable")
    rows = []
    origin = {}
    for i, d, cover in zip(e.i.values, e.d.values, e.cover.values):
        name = P.NAMES[W["plat"][i]]
        here = d >= W["nl"][i]
        if here:
            land = "NL"
        else:
            if i not in origin:
                o = P.ORIGIN[name]
                origin[i] = o[rs.choice(len(o), p=[w for _, w in o])][0]
            land = origin[i]
        if cover == 0:
            fitted, src, war = "OEM nieuw", "OEM dealer", "OEM"
        else:
            # a dealer that fits one of our packs reports it too, and the two records were matched into one
            fitted, war = "Voltwerk revisie", ("Voltwerk" if cover == 1 else "geen")
            src = "OEM dealer + Voltwerk" if rb.random() < 0.27 else "Voltwerk"
        k = plate[int(i)]
        rows.append(dict(kenteken=k,
                         vervangdatum=Wd.date(d).isoformat(), land=land, garantie=war,
                         geplaatst_pakket=fitted, bron=src))
    return pd.DataFrame(rows)


def curves():
    T = Wd.tables()
    df = pd.DataFrame({"pakketleeftijd_jaar": Wd.AGES.astype(int)})
    for k, n in enumerate(P.NAMES):
        df[n] = T[k]
    df["Voltwerk revisiepakket (alle platforms)"] = T[-1]
    return df
