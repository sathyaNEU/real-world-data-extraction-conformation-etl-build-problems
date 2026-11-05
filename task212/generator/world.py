"""task212 world: Brujula Paqueteria, six Spanish sortation hubs, Q3 2026 outbound cage audits.

One clean truth, every record system cut from it. Deterministic: one seed, one RNG stream per system.
"""
import datetime as dt
import numpy as np
import pandas as pd

SEED = 2120
Q3_START, Q3_END = dt.date(2026, 7, 1), dt.date(2026, 9, 30)
UTC_OFFSET_H = 2  # Spanish summer time throughout July to September

# hub key, sorter-export number (province code), audit-system name, town, heavy chute, heavy pattern
HUBS = [
    ("ZAZ", 50, "Zaragoza Plaza", "Zaragoza", False, "last"),
    ("VLC", 46, "Ribarroja", "Ribarroja del Turia", False, "first"),
    ("SVQ", 41, "Dos Hermanas", "Dos Hermanas", False, "early"),
    ("MAD", 28, "San Fernando", "San Fernando de Henares", True, None),
    ("BCN", 8, "El Prat", "El Prat de Llobregat", True, None),
    ("BIO", 48, "Basauri", "Basauri", True, None),
]
HUB_KEYS = [h[0] for h in HUBS]
HEAVY_ACCOUNT = {"ZAZ": ("C50112", "Recambios del Ebro SL", "automotive parts", 2.0, (3, 5)),
                 "VLC": ("C46087", "Ceramicas del Millars SA", "ceramic tiles", 5.0, (21, 35)),
                 "SVQ": ("C41239", "Almazara Guadaira SL", "olive oil and wine", 4.0, (23, 40))}
# heavy trunk arrival (local h, m) per hub: ZAZ last of the night, VLC first, SVQ early-to-mid wave

PARAMS = dict(base=-4.86, b_frag=0.55, b_box=0.25, b_lw=-0.10, b_nd=0.10, gamma=1.45, thr=60.0, scale=8.0,
              equip_hub="VLC", equip=0.60, hub_sd=0.04, night_sd=0.05, p_pattern=0.97,
              crush_box=1.0, crush_bag=0.45, crush_flyer=0.15, crush_heavy=0.15)


def operating_days():
    d, out = Q3_START, []
    while d <= Q3_END:
        if d.weekday() < 5:  # sorting nights start Monday to Friday evenings
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def _depots(rng):
    names = {
        "ZAZ": ["Zaragoza Norte", "Huesca", "Teruel", "Logrono", "Calatayud", "Tudela", "Soria"],
        "VLC": ["Valencia Sur", "Valencia Puerto", "Castellon", "Gandia", "Alzira", "Sagunto", "Requena"],
        "SVQ": ["Sevilla Este", "Sevilla Cartuja", "Huelva", "Jerez", "Cordoba", "Ecija", "Lebrija"],
        "MAD": ["Alcala", "Getafe", "Leganes", "Torrejon", "Mostoles", "Alcobendas", "Fuenlabrada", "Arganda"],
        "BCN": ["Hospitalet", "Badalona", "Sabadell", "Terrassa", "Mataro", "Granollers", "Martorell"],
        "BIO": ["Bilbao Zorrotza", "Getxo", "Vitoria", "Donostia", "Barakaldo", "Durango"],
    }
    rows, used = [], set()
    for h in HUB_KEYS:
        for n in names[h]:
            while True:
                code = "%s%03d" % (h[:2], int(rng.integers(101, 989)))
                if code not in used:
                    used.add(code)
                    break
            rows.append((code, n, h))
    return pd.DataFrame(rows, columns=["depot_code", "depot_name", "hub"])


def _accounts(rng):
    sectors = ["fashion and footwear", "electronics", "cosmetics", "books and media", "home and garden",
               "sports", "pharmacy and health", "toys", "food and drink", "pet supplies", "jewellery", "office"]
    frag_by_sector = {"electronics": 0.45, "cosmetics": 0.5, "food and drink": 0.35, "jewellery": 0.3,
                      "pharmacy and health": 0.3, "home and garden": 0.25}
    rows, used = [], set()
    for i in range(240):
        while True:
            acc = "C%02d%03d" % (int(rng.choice([8, 28, 41, 46, 48, 50, 3, 29, 30, 15])), int(rng.integers(100, 999)))
            if acc not in used:
                used.add(acc)
                break
        sec = sectors[int(rng.integers(0, len(sectors)))]
        default = float(rng.choice([0.5, 1.0, 1.0, 2.0, 0.0]))  # 0.0: sender keys an estimate per parcel
        rows.append((acc, sec, frag_by_sector.get(sec, 0.12), default, float(rng.lognormal(0, 0.9))))
    acc = pd.DataFrame(rows, columns=["account", "sector", "p_fragile", "declared_default_kg", "volume_weight"])
    for h, (code, name, sec, dflt, _) in HEAVY_ACCOUNT.items():
        acc = pd.concat([acc, pd.DataFrame([(code, sec, 0.0, dflt, 0.0)], columns=acc.columns)])
    return acc.reset_index(drop=True)


def _barcode(rng, used):
    while True:
        b = "BQ%02d%08d%02d" % (int(rng.integers(10, 99)), int(rng.integers(0, 10 ** 8)), int(rng.integers(0, 100)))
        if b not in used:
            used.add(b)
            return b


def simulate(seed=SEED, P=PARAMS):
    """Return dict of truth tables. Every record system is cut from these."""
    rng = np.random.default_rng(seed)
    r_par = np.random.default_rng(seed + 1)
    r_dmg = np.random.default_rng(seed + 2)
    days = operating_days()
    depots = _depots(np.random.default_rng(seed + 3))
    accounts = _accounts(np.random.default_rng(seed + 4))
    ecom = accounts[accounts.volume_weight > 0].reset_index(drop=True)
    acc_p = (ecom.volume_weight / ecom.volume_weight.sum()).values
    hub_eff = {h: float(rng.normal(0, P["hub_sd"])) for h in HUB_KEYS}
    used = set()
    cage_rows, parcel_rows = [], []
    cage_serial = {h: int(rng.integers(1200, 4800)) for h in HUB_KEYS}
    for (h, hub_no, hub_name, town, chute, pattern) in HUBS:
        dep = depots[depots.hub == h].depot_code.tolist()
        for d in days:
            night_eff = float(rng.normal(0, P["night_sd"]))
            n_cages = int(np.clip(rng.poisson(10), 7, 14))
            chosen = rng.choice(dep, size=n_cages, replace=True)
            for depot in chosen:
                cage_serial[h] += int(rng.integers(3, 41))
                cage_label = "%02d%s%04d" % (hub_no, d.strftime("%m%d"), cage_serial[h] % 10000)
                nl = max(18, int(r_par.poisson(36)))
                nh = 0 if chute else int(7 + r_par.binomial(2, 0.5))
                lw = np.clip(r_par.lognormal(np.log(0.6), 0.7, nl), 0.08, 9.5)
                hw = r_par.uniform(15, 21, nh)
                lpack = r_par.choice(["BOX", "BAG", "FLYER"], nl, p=[0.55, 0.27, 0.18])
                lacc = r_par.choice(ecom.account.values, nl, p=acc_p)
                pf = ecom.set_index("account").p_fragile.reindex(lacc).values
                lfrag = r_par.random(nl) < pf
                lserv = r_par.choice(["24H", "48H", "ECO"], nl, p=[0.6, 0.3, 0.1])
                order = list(range(nl)); r_par.shuffle(order)
                seq = [("L", i) for i in order]
                hv = [("H", j) for j in range(nh)]
                mode = pattern
                if mode is not None and r_par.random() > P["p_pattern"]:
                    mode = "rand"
                if mode == "last":
                    seq = seq + hv
                elif mode == "first":
                    seq = hv + seq
                elif mode == "early":
                    k = int(round(len(seq) * r_par.uniform(0.62, 0.76))); seq = seq[:k] + hv + seq[k:]
                elif mode == "rand":
                    for item in hv:
                        seq.insert(int(r_par.integers(0, len(seq) + 1)), item)
                # scan times (local), strictly increasing within the cage
                start = dt.datetime.combine(d, dt.time(21, 0)) + dt.timedelta(minutes=int(r_par.integers(0, 50)))
                n = len(seq)
                if pattern == "last" and mode == "last":
                    g = r_par.exponential(1, nl); g = g / g.sum() * r_par.uniform(320, 350) * 60
                    secs = list(np.cumsum(g).astype(int))
                    t0 = int((dt.datetime.combine(d + dt.timedelta(days=1), dt.time(3, 6)) - start).total_seconds()) + int(r_par.integers(0, 600))
                    secs += [t0 + int(s) for s in np.cumsum(r_par.integers(14, 45, nh))]
                else:
                    span = r_par.uniform(360, 410) * 60
                    g = r_par.exponential(1, n); g = g / g.sum() * span
                    secs = list(np.cumsum(g).astype(int))
                    hidx = [k for k, (t, _) in enumerate(seq) if t == "H"]
                    if hidx and mode in ("first", "early"):
                        b0 = secs[hidx[0]]
                        for m, k in enumerate(hidx):
                            secs[k] = b0 + int(m * int(r_par.integers(14, 45)) + m)
                        for k in range(1, n):
                            if secs[k] <= secs[k - 1]:
                                secs[k] = secs[k - 1] + int(r_par.integers(9, 30))
                times = [start + dt.timedelta(seconds=int(x)) for x in secs]
                # force unique, increasing seconds
                for k in range(1, n):
                    if times[k] <= times[k - 1]:
                        times[k] = times[k - 1] + dt.timedelta(seconds=7)
                w = np.array([lw[i] if t == "L" else hw[i] for t, i in seq])
                wabove = np.concatenate([np.cumsum(w[::-1])[::-1][1:], [0.0]])
                cage_rows.append((cage_label, h, d, depot, n, nh, mode or "none", float(w.sum())))
                for k, (t, i) in enumerate(seq):
                    bc = _barcode(r_par, used)
                    if t == "L":
                        parcel_rows.append((bc, cage_label, h, d, depot, k, n, times[k], float(w[k]), str(lpack[i]),
                                            bool(lfrag[i]), str(lserv[i]), str(lacc[i]), False, float(wabove[k]), night_eff))
                    else:
                        parcel_rows.append((bc, cage_label, h, d, depot, k, n, times[k], float(w[k]), "BOX", False, "48H",
                                            HEAVY_ACCOUNT[h][0], True, float(wabove[k]), night_eff))
    cages = pd.DataFrame(cage_rows, columns=["cage_label", "hub", "build_date", "depot", "n_parcels", "n_heavy",
                                             "mode", "cage_kg"])
    par = pd.DataFrame(parcel_rows, columns=["barcode", "cage_label", "hub", "build_date", "depot", "pos", "n",
                                             "scan_local", "weight_kg", "pack", "fragile", "service", "account",
                                             "heavy", "wabove_kg", "night_eff"])
    # damage, the clean truth
    crush = np.select([par.pack == "BOX", par.pack == "BAG"], [P["crush_box"], P["crush_bag"]], P["crush_flyer"])
    crush = np.where(par.heavy, P["crush_heavy"], crush)
    sig = 1 / (1 + np.exp(-(par.wabove_kg - P["thr"]) / P["scale"]))
    lin0 = (P["base"] + P["b_frag"] * par.fragile + P["b_box"] * (par.pack == "BOX") + P["b_lw"] * np.log(par.weight_kg)
            + P["b_nd"] * (par.service == "24H") + P["gamma"] * crush * sig + par.night_eff)
    equip = np.where(par.hub == P["equip_hub"], P["equip"], 0.0)
    heff = par.hub.map(hub_eff).values
    p = 1 / (1 + np.exp(-(lin0 + heff + equip)))
    p_noequip = 1 / (1 + np.exp(-(lin0 + heff)))
    par["p_true"], par["p_noequip"] = p, p_noequip
    par["damaged"] = (r_dmg.random(len(par)) < p)
    return dict(days=days, depots=depots, accounts=accounts, cages=cages, parcels=par, hub_eff=hub_eff)


if __name__ == "__main__":
    w = simulate()
    par = w["parcels"]
    print(len(par), par.damaged.mean().round(4))
    print((par.groupby("hub").damaged.mean() * 1e4).round(1).to_dict())
