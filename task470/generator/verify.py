"""An independent recomputation of every graded figure from target/ alone, written without methods.py: each counted
dwelling's household day in the fortnight, the municipalities' vacant dwellings, shares and designation, the persons
registered on 1 November by age, and the dwellings the municipalities held on the land register that day. Compared
with generator/figures.json.

    python3 task470/generator/verify.py [target] [figures.json]
"""
import csv
import datetime as dt
import json
import os
import re
import sys

import numpy as np
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
REF = dt.date(2026, 11, 1)
START = dt.datetime(2026, 11, 9)


def rows(target, pattern):
    name = [f for f in os.listdir(target) if re.match(pattern, f)][0]
    with open(os.path.join(target, name), encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh, delimiter=";"))


def day(s):
    return dt.datetime.strptime(s, "%d.%m.%Y").date() if s else None


def addr(a):
    return " ".join(a.upper().replace(".", " ").split())


def main(target, fig_path):
    F = json.load(open(fig_path, encoding="utf-8"))
    ok = True
    cad = rows(target, r"matrikkel_bruksenheter_")
    counted = [r for r in cad if r["bruksenhetstype"] == "Bolig" and r["tatt_i_bruk"] and day(r["tatt_i_bruk"]) <= REF]
    by_id = {r["bruksenhet_id"]: r for r in counted}
    adr_index = {}
    for r in counted:
        adr_index.setdefault((r["kommunenr"], addr("%s %s%s" % (r["adressenavn"], r["husnr"], r["bokstav"]))), []).append(
            r["bruksenhet_id"])
    mp = rows(target, r"elhub_malepunkter_")
    meter = {}
    for r in mp:
        if r["kundekategori"] != "Husholdning":
            continue
        if r["bruksenhet_id"]:
            if r["bruksenhet_id"] in by_id:
                meter[int(r["malepunkt_id"])] = r["bruksenhet_id"]
        else:
            c = adr_index.get((r["kommunenr"], addr(r["adresse"])), [])
            if len(c) == 1:
                meter[int(r["malepunkt_id"])] = c[0]
    hp = [f for f in os.listdir(target) if f.endswith(".parquet")][0]
    t = pq.read_table(os.path.join(target, hp)).to_pandas()
    t = t.sort_values(["malepunkt_id", "fra_tidspunkt_utc", "leveranse"]).drop_duplicates(
        ["malepunkt_id", "fra_tidspunkt_utc"], keep="last")
    t = t[t["malepunkt_id"].isin(list(meter))]
    local = t["fra_tidspunkt_utc"].dt.tz_convert("Europe/Oslo").dt.tz_localize(None)
    hix = ((local - START).dt.total_seconds() // 3600).astype(int).to_numpy()
    keep = (hix >= 0) & (hix < 336)
    dw = t["malepunkt_id"].map(meter).to_numpy()[keep]
    ids = sorted(set(dw))
    pos = {k: i for i, k in enumerate(ids)}
    tot = np.zeros((len(ids), 336))
    cnt = np.zeros((len(ids), 336))
    np.add.at(tot, ([pos[x] for x in dw], hix[keep]), t["forbruk_kwh"].to_numpy()[keep])
    np.add.at(cnt, ([pos[x] for x in dw], hix[keep]), 1)
    a = np.where(cnt > 0, tot, np.nan).reshape(len(ids), 14, 24)
    lived = {}
    for i, k in enumerate(ids):
        best = -1.0
        for dd in range(14):
            h = a[i, dd]
            night = h[1:5][~np.isnan(h[1:5])]
            if len(night) == 0:
                continue
            for win in (h[6:9], h[16:22]):
                win = win[~np.isnan(win)]
                if len(win):
                    best = max(best, win.mean() - night.mean())
        lived[k] = best > 0.5
    res = {}
    for r in counted:
        n, v = res.get(r["kommunenr"], (0, 0))
        res[r["kommunenr"]] = (n + 1, v + (0 if lived.get(r["bruksenhet_id"], False) else 1))
    for m in F["municipalities"]:
        n, v = res[m["nr"]]
        share = "%.1f" % (round(1000.0 * v / n) / 10.0)
        good = (str(n) == m["counted"].replace(",", "") and v == m["vacant"] and share == m["share"] and
                (float(share) >= 5.0) == m["qualifies"])
        ok &= good
        print("%s  verify %s %s: %d counted, %d vacant, %s per cent" % ("ok  " if good else "FAIL", m["nr"], m["name"], n,
                                                                     v, share))
    # ---------------------------------------------------------------- table A
    reg = rows(target, r"folkeregister_bosatte_")
    ev = rows(target, r"folkeregister_hendelser_")
    key = lambda nr, s, no, b, u: (nr, addr("%s %s%s" % (s, no, b)), u.replace(" ", "").upper())
    where = {r["person_lopenr"]: [key(r["kommunenr"], r["adressenavn"], r["husnr"], r["bokstav"], r["bruksenhetsnr"]),
                                  dt.date(2027, 1, 5)] for r in reg}
    born = {r["person_lopenr"]: day(r["fodselsdato"]) for r in reg}
    for e in ev:
        born.setdefault(e["person_lopenr"], day(e["fodselsdato"]))
    # a block's renumbering: on one day every resident of an address moves to another unit number at the same address
    groups = {}
    for i, e in enumerate(ev):
        if e["hendelse"] == "Flytting" and e["fra_adressenavn"] and all(
                e["fra_" + c] == e["til_" + c] for c in ("kommunenr", "adressenavn", "husnr", "bokstav")) and \
                e["fra_bruksenhetsnr"] != e["til_bruksenhetsnr"]:
            groups.setdefault((e["fra_kommunenr"], e["fra_adressenavn"], e["fra_husnr"], e["fra_bokstav"],
                               e["hendelsesdato"]), []).append(i)
    relabel_rows = set()
    relabel = {}
    for g, idx in groups.items():
        if len(idx) >= 2:
            for i in idx:
                e = ev[i]
                relabel_rows.add(i)
                relabel[key(e["fra_kommunenr"], e["fra_adressenavn"], e["fra_husnr"], e["fra_bokstav"],
                            e["fra_bruksenhetsnr"])] = (key(e["til_kommunenr"], e["til_adressenavn"], e["til_husnr"],
                                                            e["til_bokstav"], e["til_bruksenhetsnr"]),
                                                        day(e["hendelsesdato"]))
    order = sorted(range(len(ev)), key=lambda i: (day(ev[i]["hendelsesdato"]), day(ev[i]["registrert_dato"]),
                                                  ev[i]["person_lopenr"]), reverse=True)
    for i in order:
        e = ev[i]
        when = day(e["hendelsesdato"])
        if when <= REF or i in relabel_rows:
            continue
        p = e["person_lopenr"]
        frm = key(e["fra_kommunenr"], e["fra_adressenavn"], e["fra_husnr"], e["fra_bokstav"], e["fra_bruksenhetsnr"])
        if e["hendelse"] in ("Fødsel", "Innvandring"):
            where.pop(p, None)
        elif e["hendelse"] == "Flytting" and not e["fra_adressenavn"]:
            where.pop(p, None)
        else:
            where[p] = [frm, when]
    dkey = {key(r["kommunenr"], r["adressenavn"], r["husnr"], r["bokstav"], r["bruksenhetsnr"]): r for r in counted}
    tab = {}
    for p, (k, when) in where.items():
        if k in relabel and when < relabel[k][1]:
            k = relabel[k][0]
        r = dkey.get(k)
        if r is None:
            continue
        b = born[p]
        age = REF.year - b.year - ((REF.month, REF.day) < (b.month, b.day))
        band = 0 if age < 18 else (1 if age < 67 else 2)
        tab.setdefault(r["kommunenr"], [0, 0, 0])[band] += 1
    for x in F["ask_a"]:
        want = [int(x[k].replace(",", "")) for k in ("under_18", "age_18_66", "age_67")]
        good = tab.get(x["nr"]) == want
        ok &= good
        print("%s  verify table A %s: %s" % ("ok  " if good else "FAIL", x["nr"], tab.get(x["nr"])))
    # ---------------------------------------------------------------- table B
    ent = rows(target, r"enhetsregisteret_")
    sh = rows(target, r"aksjonaerregisteret_")
    kom = {r["kommunenavn"].upper(): r["kommunenr"] for r in rows(target, r"kommuner_")}
    names = {r["kommunenr"]: r["kommunenavn"].upper() for r in rows(target, r"kommuner_")}
    owned = {}
    for o in ent:
        if o["organisasjonsform"] != "KOMM":
            continue
        nr = kom[o["navn"].rsplit(" ", 1)[0]]
        s = {o["organisasjonsnummer"]} | {x["organisasjonsnummer"] for x in ent if x["organisasjonsform"] == "KF" and
                                         x["overordnet_enhet"] == o["organisasjonsnummer"]}
        grew = True
        while grew:
            held = {}
            total = {}
            for r in sh:
                if r["aksjonaer_id"] in s:
                    held[r["orgnr_selskap"]] = held.get(r["orgnr_selskap"], 0) + int(r["antall_aksjer"])
                    total[r["orgnr_selskap"]] = int(r["antall_aksjer_selskap"])
            new = {c for c in held if held[c] >= total[c]} - s
            grew = bool(new)
            s |= new
        owned[nr] = s
    tit = {(r["kommunenr"], r["gardsnr"], r["bruksnr"], r["seksjonsnr"]): (r["hjemmelshaver_id"], r["hjemmelshaver_navn"])
           for r in rows(target, r"grunnbok_hjemmel_")}
    trf = rows(target, r"grunnbok_overdragelser_")
    for r in sorted(trf, key=lambda r: day(r["tinglyst_dato"]), reverse=True):
        if day(r["tinglyst_dato"]) > REF:
            tit[(r["kommunenr"], r["gardsnr"], r["bruksnr"], r["seksjonsnr"])] = (r["avgiver_id"], r["avgiver_navn"])
    held = {}
    for r in counted:
        k = (r["kommunenr"], r["gardsnr"], r["bruksnr"], r["seksjonsnr"])
        hid, hn = tit.get(k) or tit.get(k[:3] + ("",), ("", ""))
        mine = hid in owned[r["kommunenr"]] if hid else bool(
            re.match(r"^%s (BY|HERREDS)?KOMMUNE\b" % re.escape(names[r["kommunenr"]]), hn.upper()))
        held[r["kommunenr"]] = held.get(r["kommunenr"], 0) + mine
    for x in F["ask_b"]:
        good = held.get(x["nr"], 0) == int(x["held"].replace(",", ""))
        ok &= good
        print("%s  verify table B %s: %d" % ("ok  " if good else "FAIL", x["nr"], held.get(x["nr"], 0)))
    q = sorted(m["nr"] for m in F["municipalities"] if m["qualifies"])
    print("%s  verify: %d municipalities qualify (%s)" % ("ok  " if ok else "FAIL", len(q), " ".join(q)))
    return ok


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(TASK, "target"),
         sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "figures.json"))
