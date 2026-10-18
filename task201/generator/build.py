#!/usr/bin/env python3
"""task201 pack builder. Writes target/ from world.py, then goldens.py writes the deliverables.

    python3 generator/build.py            # from the task folder or the generator folder

Everything is seeded from params.SEED. Two consecutive runs give byte-identical target/ bytes.
"""
import os, sys, shutil, datetime, time
import numpy as np, pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")

import params as P
import world, drill

EXPORT_TS = datetime.datetime(2026, 11, 16, 6, 0, 0)
MTIME = time.mktime(EXPORT_TS.timetuple())

CAUSES = ["wiatr - galaz na przewodzie", "wiatr - zlamany slup", "przepiecie atmosferyczne",
          "uszkodzenie izolatora", "zwierzyna / ptak", "uszkodzenie kabla", "nieustalona",
          "zadzialanie zabezpieczenia", "uszkodzenie glowicy", "wilgoc w mufie"]


def fmt_local(s):
    return pd.to_datetime(s).dt.strftime("%Y-%m-%d %H:%M").fillna("")


def unpad(key, flag):
    """The pre-2024 identifier form: no zero padding on the feeder, district or device number."""
    out = []
    for k, f in zip(key, flag):
        if not f:
            out.append(k); continue
        br, rest = k.split("-", 1)
        dist, rest2 = rest.split("-", 1)
        fid, tail = rest2.split("/", 1)
        cls, num = tail.split("/")
        out.append("%s-%s-%s/%s/%s" % (br, int(dist), int(fid), cls, int(num)))
    return out


def stamp_workbook(xl):
    """Fix the workbook's own properties, so the build clock never reaches the shipped container."""
    p = xl.book.properties
    p.creator = "Borowiecka Energia Operator"
    p.lastModifiedBy = "Borowiecka Energia Operator"
    p.created = EXPORT_TS
    p.modified = EXPORT_TS
    p.title = None
    p.description = None


def normalise_containers(d):
    """Repack every OOXML container with fixed entry timestamps, so a rebuild is byte-identical.
    openpyxl and python-docx stamp zip entries with the build clock."""
    import zipfile
    if not os.path.isdir(d):
        return
    for f in sorted(os.listdir(d)):
        if not f.endswith((".xlsx", ".docx", ".pptx")):
            continue
        p = os.path.join(d, f)
        import re as _re
        with zipfile.ZipFile(p) as z:
            items = []
            for i in z.infolist():
                data = z.read(i.filename)
                if i.filename.startswith("docProps/"):
                    data = _re.sub(rb"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ",
                                   b"2026-11-16T06:00:00Z", data)
                items.append((i, data))
        tmp = p + ".tmp"
        with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
            for info, data in items:
                ni = zipfile.ZipInfo(info.filename, date_time=(2026, 11, 16, 6, 0, 0))
                ni.compress_type = info.compress_type
                ni.external_attr = info.external_attr
                z.writestr(ni, data)
        shutil.move(tmp, p)


def build():
    if os.path.isdir(TARGET):
        shutil.rmtree(TARGET)
    os.makedirs(TARGET)
    rng = np.random.default_rng(P.SEED + 101)

    fd, dv, ev = world.build_world()
    nl = world.notification_log(ev)
    sc = world.scada_log(ev)

    # ------------------------------------------------------------------ 1-2 dispatch exports
    ev = ev.copy()
    # the dispatcher types the work order's own scope into a planned outage's cause field
    ev["przyczyna"] = np.where(ev.rodzaj.values == "planowane",
                               ev.przyczyna_planowa.fillna("prace planowane").values,
                               np.array(CAUSES)[rng.integers(0, len(CAUSES), len(ev))])
    ev["urzadzenie_eksport"] = unpad(ev.urzadzenie_id.values, ev.klucz_bez_zer.values)
    ev["czas_trwania_min"] = ((ev.t_zalaczenie - ev.t_poczatek_oms).dt.total_seconds() / 60.0).round(0)

    legacy_cols = ["zdarzenie_id", "oddzial", "rejon", "linia_sn", "urzadzenie", "rodzaj",
                   "ts_poczatek", "ts_zalaczenie", "czas_trwania_min", "przyczyna", "epizod"]
    current_cols = ["id_zdarzenia", "oddzial", "rejon", "id_linii", "id_urzadzenia",
                    "rodzaj_wylaczenia", "poczatek_lokalny", "zalaczenie_lokalne",
                    "czas_trwania_min", "przyczyna", "epizod_pogodowy"]
    base = pd.DataFrame(dict(
        a=ev.zdarzenie_id, b=ev.oddzial, c=ev.rejon, d=ev.feeder_id, e=ev.urzadzenie_eksport,
        f=ev.rodzaj, g=fmt_local(ev.t_poczatek_oms), h=fmt_local(ev.t_zalaczenie),
        i=ev.czas_trwania_min.map(lambda x: "" if pd.isna(x) else "%d" % x),
        j=ev.przyczyna, k=ev.epizod, start=ev.t_poczatek_oms))

    def write_export(path, cols, lo, hi, note):
        sub = base[(base.start >= np.datetime64(lo)) & (base.start < np.datetime64(hi) + np.timedelta64(1, "D"))]
        out = sub.drop(columns=["start"]).copy(); out.columns = cols
        with open(path, "w", encoding="utf-8", newline="") as fh:
            fh.write("# %s\n" % note)
            out.to_csv(fh, index=False)
        return len(out)

    n_leg = write_export(os.path.join(TARGET, "awarie_oms_2026-10-01_2026-11-07.csv"), legacy_cols,
                         "2026-10-01", "2026-11-07",
                         "BEO SD-OMS eksport wylaczen | okres 2026-10-01..2026-11-07 | "
                         "pobrano 2026-11-16 06:00 | modul raportowy 3.4 (uklad do 2026-10-31)")
    n_cur = write_export(os.path.join(TARGET, "awarie_oms_2026-11-01_2026-11-15.csv"), current_cols,
                         "2026-11-01", "2026-11-15",
                         "BEO SD-OMS eksport wylaczen | okres 2026-11-01..2026-11-15 | "
                         "pobrano 2026-11-16 06:00 | modul raportowy 4.0 (nowy uklad kolumn)")

    # ------------------------------------------------------------------ 3 notification log (spine)
    nl = nl.copy()
    nl["id_urzadzenia"] = unpad(nl.urzadzenie_id.values,
                                nl.zdarzenie_id.map(dict(zip(ev.zdarzenie_id, ev.klucz_bez_zer))).fillna(False).values)
    # genuine orphans: a neighbour's supply, the customer's own installation, a planned switching
    norph = P.ORPHAN_N
    pick = rng.integers(0, len(dv), norph)
    orph = pd.DataFrame(dict(
        zgloszenie_id=["ZG26%08d" % (9100003 + 3 * i) for i in range(norph)],
        zdarzenie_id="", oddzial=dv.oddzial.values[pick], rejon=dv.rejon.values[pick],
        id_urzadzenia=dv.urzadzenie_id.values[pick],
        kanal=np.where(rng.random(norph) < 0.30, "IVR", np.where(rng.random(norph) < 0.5, "aplikacja", "telefon")),
        t_przyjecia=(np.datetime64("2026-10-01T00:00") +
                     rng.integers(0, 46 * 24 * 60, norph).astype("timedelta64[m]")),
        nr_odbiorcy=["PPE%09d" % v for v in rng.integers(100000000, 999999999, norph)],
        opis=np.where(rng.random(norph) < 0.5, "brak zasilania u sasiada",
                      np.where(rng.random(norph) < 0.5, "zadzialal bezpiecznik w mieszkaniu",
                               "pytanie o wylaczenie planowane"))))
    nl_pre = nl
    nl = pd.concat([nl[["zgloszenie_id", "zdarzenie_id", "oddzial", "rejon", "id_urzadzenia",
                        "kanal", "t_przyjecia", "nr_odbiorcy", "opis"]], orph], ignore_index=True)
    nl = nl.sort_values("t_przyjecia").reset_index(drop=True)
    # A2 device: an IVR prompt change between 9 and 19 October left the device and the branch unwritten
    gap = ((nl.t_przyjecia >= np.datetime64(P.IVR_GAP[0] + "T00:00")) &
           (nl.t_przyjecia < np.datetime64(P.IVR_GAP[1] + "T00:00")) & (nl.kanal == "IVR"))
    ivr_blank = nl.index[gap]
    nl.loc[ivr_blank, "ivr_luka"] = True
    nl["ivr_luka"] = nl.ivr_luka.fillna(False)
    out = nl.copy()
    # a realistic background of blanks elsewhere, so the span is not the only gap in the column
    other = out.index[(~out.ivr_luka) & (rng.random(len(out)) < 0.004)]
    blanked = list(ivr_blank) + list(other)
    ppe_map = dict(zip(nl.loc[blanked, "nr_odbiorcy"], nl.loc[blanked, "id_urzadzenia"]))
    ppe_branch = dict(zip(nl.loc[blanked, "nr_odbiorcy"], nl.loc[blanked, "oddzial"]))
    ppe_rejon = dict(zip(nl.loc[blanked, "nr_odbiorcy"], nl.loc[blanked, "rejon"]))
    out.loc[ivr_blank, ["id_urzadzenia", "oddzial", "rejon"]] = ""
    out.loc[other, "id_urzadzenia"] = ""
    resave = out.index[rng.random(len(out)) < 0.041]
    rep = out.loc[resave].copy()
    rep["zgloszenie_id"] = ["ZG26%08d" % (6500001 + 3 * i) for i in range(len(rep))]
    out = pd.concat([out, rep], ignore_index=True).sort_values("t_przyjecia").reset_index(drop=True)
    nlw = out[["zgloszenie_id", "t_przyjecia", "kanal", "oddzial", "rejon", "id_urzadzenia",
               "nr_odbiorcy", "zdarzenie_id", "opis"]].copy()
    nlw.columns = ["zgloszenie_id", "ts_przyjecia", "kanal", "oddzial", "rejon", "id_urzadzenia",
                   "nr_ppe", "id_zdarzenia", "opis"]
    nlw["ts_przyjecia"] = fmt_local(nlw.ts_przyjecia)
    with open(os.path.join(TARGET, "zgloszenia_klientow_2026.csv"), "w", encoding="utf-8", newline="") as fh:
        fh.write("# BEO Centrum Zgloszen | zgloszenia o braku zasilania | 2026-10-01..2026-11-15 | "
                 "pobrano 2026-11-16 06:00 | czas lokalny Europe/Warsaw\n")
        nlw.to_csv(fh, index=False)

    # ------------------------------------------------------------------ 4 telemetry archive (UTC)
    scw = sc.rename(columns=dict(urzadzenie_id="id_urzadzenia", feeder_id="id_linii"))
    scw["ts_utc"] = pd.to_datetime(scw.ts_utc).dt.strftime("%Y-%m-%dT%H:%M:%SZ")
    scw = scw[["rekord_id", "ts_utc", "id_urzadzenia", "id_linii", "operacja", "jakosc_sygnalu"]]
    with open(os.path.join(TARGET, "telemetria_operacje_lacznikow_utc.csv"), "w", encoding="utf-8", newline="") as fh:
        fh.write("# BEO SCADA historian | operacje lacznikow i wskaznikow zwarciowych | "
                 "znaczniki czasu UTC | 2026-10-01..2026-11-15 | pobrano 2026-11-16 06:00\n")
        scw.to_csv(fh, index=False)

    # ------------------------------------------------------------------ 5 device register
    reg = dv.rename(columns=dict(urzadzenie_id="id_urzadzenia", feeder_id="id_linii")).copy()
    reg = reg.merge(fd[["feeder_id", "stacja_gpz"]].rename(columns={"feeder_id": "id_linii"}), on="id_linii")
    reg["rok_zabudowy"] = 1968 + rng.integers(0, 56, len(reg))
    reg = reg[["id_urzadzenia", "id_linii", "stacja_gpz", "oddzial", "rejon", "klasa_odcinka",
               "odbiorcy_za_urzadzeniem", "rok_zabudowy", "telemetria_linii"]]
    reg = reg.sort_values("id_urzadzenia").reset_index(drop=True)
    served_by = reg[reg.klasa_odcinka == "SN-magistrala"].groupby("oddzial").odbiorcy_za_urzadzeniem.sum()
    summary = pd.DataFrame([dict(oddzial=b, nazwa=P.BRANCH[b]["name"],
                                 odbiorcy_tys=round(float(served_by[b]) / 1000.0, 1),
                                 linie_sn=int((fd.oddzial == b).sum()),
                                 stacje_sn_nn=int(((reg.oddzial == b) & (reg.klasa_odcinka == "SN/nN-stacja")).sum()))
                            for b in P.BRANCH])
    with pd.ExcelWriter(os.path.join(TARGET, "rejestr_urzadzen_sn_nn.xlsx"), engine="openpyxl") as xl:
        reg.to_excel(xl, sheet_name="urzadzenia", index=False)
        summary.to_excel(xl, sheet_name="podsumowanie_odbiorcy", index=False)

    # ------------------------------------------------------------------ 6 telemetry programme
    prog = fd[fd.telemetria_linii].copy()
    stage = rng.integers(1, 4, len(prog))
    acc = (np.datetime64("2022-06-01") + rng.integers(0, 1450, len(prog)).astype("timedelta64[D]"))
    prog = pd.DataFrame(dict(id_linii=prog.feeder_id.values, oddzial=prog.oddzial.values,
                             rejon=prog.rejon.values, etap="etap %d" % 0,
                             data_odbioru=acc, typ_urzadzenia=np.where(rng.random(len(prog)) < 0.6,
                             "reklozer linii z telemetria", "wskaznik zwarciowy z modemem")))
    prog["etap"] = ["etap %d" % s for s in stage]
    prog["data_zalaczenia_telemetrii"] = prog.data_odbioru + rng.integers(9, 64, len(prog)).astype("timedelta64[D]")
    prog["status"] = np.where(prog.data_zalaczenia_telemetrii <= np.datetime64("2026-09-30"),
                              "w eksploatacji", "w rozruchu")
    nf = fd[~fd.telemetria_linii].sample(min(26, int((~fd.telemetria_linii).sum())), random_state=P.SEED + 7)
    planned_rows = pd.DataFrame(dict(id_linii=nf.feeder_id.values, oddzial=nf.oddzial.values,
                                     rejon=nf.rejon.values, etap="etap 4",
                                     data_odbioru=pd.NaT,
                                     typ_urzadzenia="reklozer linii z telemetria",
                                     data_zalaczenia_telemetrii=pd.NaT,
                                     status="w przygotowaniu"))
    prog = pd.concat([prog, planned_rows], ignore_index=True).sort_values(["oddzial", "id_linii"])
    for c in ["data_odbioru", "data_zalaczenia_telemetrii"]:
        prog[c] = pd.to_datetime(prog[c]).dt.strftime("%Y-%m-%d").fillna("")
    prog["rok_planowany"] = np.where(prog.status == "w przygotowaniu", "2027", "")
    with pd.ExcelWriter(os.path.join(TARGET, "program_telemetrii_linii.xlsx"), engine="openpyxl") as xl:
        prog.to_excel(xl, sheet_name="linie_objete_programem", index=False)

    # ------------------------------------------------------------------ 7 planned-work schedule
    pl = ev[ev.rodzaj == "planowane"].copy().reset_index(drop=True)
    # One scheduled job may switch out several sections of the same feeder in one visit, so the
    # grafik holds one row per job while the dispatch export holds one row per interruption.
    pl = pl.sort_values(["feeder_id", "t_utrata"]).reset_index(drop=True)
    job, k, used = [], 0, 0
    for i in range(len(pl)):
        if i == 0:
            k, used = 1, 1
        else:
            same_feeder = pl.feeder_id[i] == pl.feeder_id[i - 1]
            close = (pl.t_utrata[i] - pl.t_utrata[i - 1]).total_seconds() < 9 * 3600
            if same_feeder and close and used < 3:
                used += 1
            else:
                k += 1; used = 1
        job.append("WP-2026-%04d" % (120 + 3 * k))
    pl["id_pracy"] = job
    # the published window: the executed switching sits inside it, except where the job overran
    over = rng.random(len(pl)) < 0.17
    slack_before = rng.integers(10, 55, len(pl))
    win_len = pl.naprawa_min.values + slack_before + rng.integers(20, 150, len(pl))
    win_len = np.where(over, pl.naprawa_min.values + slack_before - rng.integers(25, 180, len(pl)), win_len)
    win_len = np.maximum(win_len, 45)
    pl["okno_od"] = pl.t_utrata - pd.to_timedelta(slack_before, unit="m")
    pl["okno_do"] = pl.okno_od + pd.to_timedelta(win_len, unit="m")
    # the published window is the job's: it opens before its first section and closes after the last
    # section was switched out, so every one of the job's starts falls inside it
    anchor = pl.groupby("id_pracy").t_utrata.min()
    jend = pl.groupby("id_pracy").t_zalaczenie.max()
    jids = list(anchor.index)
    # the window's close is dimensioned on the job's content, over the planner's standard
    # twenty-minute allowance for the first switching
    jo = anchor - pd.Timedelta(minutes=20)
    fac = pd.Series(rng.uniform(0.66, 1.72, len(jids)), index=jids)
    span = (jend - jo).dt.total_seconds() / 60.0
    jd = jo + pd.to_timedelta((span * fac).round(0), unit="m")
    # the window opens on the lead-in notified for that job, which the planner sets per job; it is
    # drawn on its own stream so the programme's content does not move with it
    rngw = np.random.default_rng(P.SEED + 211)
    lead = pd.Series(rngw.choice([10, 15, 20, 25, 30, 40, 45, 60], size=len(jids),
                                 p=[0.07, 0.22, 0.24, 0.09, 0.18, 0.07, 0.08, 0.05]), index=jids)
    pl["okno_od"] = pl.id_pracy.map(anchor - pd.to_timedelta(lead, unit="m"))
    pl["okno_do"] = pl.id_pracy.map(jd)
    pl["przekroczenie_min"] = ((pl.t_zalaczenie - pl.okno_do).dt.total_seconds() / 60.0).clip(lower=0).round(0)
    # A1 device: the November sheet was issued, then revised; the issued windows are the earlier ones
    nov = pl.index[pl.t_utrata >= np.datetime64("2026-11-01")]
    moved = nov[: min(41, len(nov))]
    pl["okno_od_wydanie"] = pl.okno_od; pl["okno_do_wydanie"] = pl.okno_do
    shift = pd.to_timedelta(rng.integers(95, 320, len(moved)), unit="m")
    pl.loc[moved, "okno_od_wydanie"] = pl.loc[moved, "okno_od"] + shift
    pl.loc[moved, "okno_do_wydanie"] = pl.loc[moved, "okno_do"] + shift

    def sheet(df, col_od, col_do, status):
        g = df.groupby("id_pracy")
        out = pd.DataFrame(dict(
            id_pracy=g.id_pracy.first(), oddzial=g.oddzial.first(), rejon=g.rejon.first(),
            id_linii=g.feeder_id.first(), odcinkow=g.size(),
            zakres=g.zakres_pracy.first(),
            okno_od=pd.to_datetime(g[col_od].min()).dt.strftime("%Y-%m-%d %H:%M"),
            okno_do=pd.to_datetime(g[col_do].max()).dt.strftime("%Y-%m-%d %H:%M"),
            status=status))
        return out.reset_index(drop=True).sort_values(["okno_od", "id_pracy"]).reset_index(drop=True)

    okt = pl[pl.t_utrata < np.datetime64("2026-11-01")]
    nov_df = pl.loc[nov]
    with pd.ExcelWriter(os.path.join(TARGET, "harmonogram_wylaczen_planowanych.xlsx"), engine="openpyxl") as xl:
        sheet(okt, "okno_od", "okno_do", "wykonane").to_excel(xl, sheet_name="pazdziernik_wydanie_1", index=False)
        sheet(nov_df, "okno_od_wydanie", "okno_do_wydanie", "wydane").to_excel(
            xl, sheet_name="listopad_wydanie_1", index=False)
        sheet(nov_df, "okno_od", "okno_do", "wydane").to_excel(
            xl, sheet_name="listopad_wydanie_2", index=False)
        pd.DataFrame([
            dict(arkusz="pazdziernik_wydanie_1", wydano="2026-09-24", uwaga="harmonogram miesieczny"),
            dict(arkusz="listopad_wydanie_1", wydano="2026-10-23", uwaga="harmonogram miesieczny"),
            dict(arkusz="listopad_wydanie_2", wydano="2026-11-04",
                 uwaga="korekta okien po naradzie ruchowej; zastepuje wydanie 1"),
        ]).to_excel(xl, sheet_name="wydania", index=False)

    # ------------------------------------------------------------------ 8 customer to device map
    need_ppe = sorted(set(ppe_map))
    extra_dev = dv.sample(min(4200, len(dv)), random_state=P.SEED + 13)
    extra = pd.DataFrame(dict(nr_ppe=["PPE%09d" % v for v in rng.integers(100000000, 999999999, len(extra_dev))],
                              id_urzadzenia=extra_dev.urzadzenie_id.values,
                              oddzial=extra_dev.oddzial.values, rejon=extra_dev.rejon.values))
    core = pd.DataFrame(dict(nr_ppe=need_ppe,
                             id_urzadzenia=[ppe_map[k] for k in need_ppe],
                             oddzial=[ppe_branch[k] for k in need_ppe],
                             rejon=[ppe_rejon[k] for k in need_ppe]))
    ppe = pd.concat([core, extra], ignore_index=True).drop_duplicates("nr_ppe")
    ppe["taryfa"] = np.where(rng.random(len(ppe)) < 0.78, "G11", np.where(rng.random(len(ppe)) < 0.6, "G12", "C11"))
    ppe = ppe.sort_values("nr_ppe").reset_index(drop=True)
    with open(os.path.join(TARGET, "odbiorcy_ppe.csv"), "w", encoding="utf-8", newline="") as fh:
        fh.write("# BEO rejestr punktow poboru energii | wyciag dla sluzb ruchowych | "
                 "stan 2026-11-16 | jeden wiersz na PPE\n")
        ppe.to_csv(fh, index=False)

    # ------------------------------------------------------------------ 12-13 distractors
    nq = 2600
    qp = rng.integers(0, len(dv), nq)
    q = pd.DataFrame(dict(
        id_zgloszenia=["JE26%06d" % (4100 + 7 * i) for i in range(nq)],
        ts_przyjecia=(np.datetime64("2026-07-01T00:00") +
                      rng.integers(0, 138 * 24 * 60, nq).astype("timedelta64[m]")),
        oddzial=dv.oddzial.values[qp], rejon=dv.rejon.values[qp],
        id_urzadzenia=dv.urzadzenie_id.values[qp],
        kategoria=np.array(["zapad napiecia", "migotanie", "napiecie ponizej normy",
                            "napiecie powyzej normy", "wyzsze harmoniczne", "asymetria"])[
            rng.integers(0, 6, nq)],
        wynik_pomiaru=np.where(rng.random(nq) < 0.42, "w normie PN-EN 50160", "poza norma"),
        czas_reakcji_dni=rng.integers(1, 34, nq)))
    q["ts_przyjecia"] = fmt_local(q.ts_przyjecia)
    with open(os.path.join(TARGET, "rejestr_zgloszen_jakosci_energii.csv"), "w", encoding="utf-8", newline="") as fh:
        fh.write("# BEO rejestr zgloszen jakosci energii | 2026-07-01..2026-11-15 | "
                 "pobrano 2026-11-16 06:00\n")
        q.to_csv(fh, index=False)

    nv = len(fd) * 4
    vp = rng.integers(0, len(fd), nv)
    veg = pd.DataFrame(dict(
        id_zlecenia=["WY26%05d" % (310 + 4 * i) for i in range(nv)],
        id_linii=fd.feeder_id.values[vp], oddzial=fd.oddzial.values[vp], rejon=fd.rejon.values[vp],
        rodzaj=np.where(rng.random(nv) < 0.55, "wycinka podstawowa", np.where(
            rng.random(nv) < 0.5, "przeglad linii z ziemi", "ogladziny z powietrza")),
        data_zakonczenia=(np.datetime64("2025-11-01") +
                          rng.integers(0, 380, nv).astype("timedelta64[D]")),
        km_trasy=(rng.gamma(3.0, 1.1, nv) + 0.3).round(2),
        koszt_pln=(rng.gamma(4.0, 2600, nv) + 1800).round(0).astype(int)))
    veg["data_zakonczenia"] = pd.to_datetime(veg.data_zakonczenia).dt.strftime("%Y-%m-%d")
    veg = veg.sort_values("data_zakonczenia").reset_index(drop=True)
    with open(os.path.join(TARGET, "wycinka_i_przeglady_linii_2026.csv"), "w", encoding="utf-8", newline="") as fh:
        fh.write("# BEO Zarzadzanie Majatkiem | wycinka i przeglady linii SN | rok gospodarczy 2026 | "
                 "pobrano 2026-11-16 06:00\n")
        veg.to_csv(fh, index=False)

    # ------------------------------------------------------------------ 11 concession returns 2026
    pl_all = ev[ev.rodzaj == "planowane"].copy()
    pl_all["mies"] = pd.to_datetime(pl_all.t_utrata).dt.strftime("%Y-%m")
    pl_all["cm"] = pl_all.odbiorcy * (pl_all.t_zalaczenie - pl_all.t_utrata).dt.total_seconds() / 60.0
    un = ev[(ev.rodzaj == "awaryjne") & ev.t_zalaczenie.notna()].copy()
    un["mies"] = pd.to_datetime(un.t_poczatek_oms).dt.strftime("%Y-%m")
    un["cm"] = un.odbiorcy * (un.t_zalaczenie - un.t_poczatek_oms).dt.total_seconds() / 60.0
    served = int(served_by.sum())
    rows = []
    # SAIDI is interrupted customer-minutes over customers supplied, SAIFI interrupted customers
    # over customers supplied. Both are reported per network level and both carry the level's share.
    for m in sorted(set(un.mies) | set(pl_all.mies)):
        rows.append(dict(miesiac=m, poziom="SN",
                         saidi_awaryjne_min_na_odb=round(un[un.mies == m].cm.sum() * 0.63 / served, 2),
                         saidi_planowane_min_na_odb=round(pl_all[pl_all.mies == m].cm.sum() * 0.71 / served, 2),
                         saifi_awaryjne_na_odb=round(un[un.mies == m].odbiorcy.sum() * 0.63 / served, 4)))
        rows.append(dict(miesiac=m, poziom="nN",
                         saidi_awaryjne_min_na_odb=round(un[un.mies == m].cm.sum() * 0.37 / served, 2),
                         saidi_planowane_min_na_odb=round(pl_all[pl_all.mies == m].cm.sum() * 0.29 / served, 2),
                         saifi_awaryjne_na_odb=round(un[un.mies == m].odbiorcy.sum() * 0.37 / served, 4)))
    ret = pd.DataFrame(rows)
    # The preliminary submission divided by the customer count at 30 September; the revised one by the
    # count at 31 October, which the concession grew between. Every row therefore moves by one
    # constant ratio, and October's unplanned minutes move by that ratio and by the correction.
    prelim = ret.copy()
    DEN = 1.0 / 0.9605
    for c in ["saidi_awaryjne_min_na_odb", "saidi_planowane_min_na_odb", "saifi_awaryjne_na_odb"]:
        prelim[c] = (prelim[c] * DEN).round(2 if c != "saifi_awaryjne_na_odb" else 4)
    oct_sn = (prelim.miesiac == "2026-10") & (prelim.poziom == "SN")
    oct_nn = (prelim.miesiac == "2026-10") & (prelim.poziom == "nN")
    prelim.loc[oct_sn, "saidi_awaryjne_min_na_odb"] = (
        prelim.loc[oct_sn, "saidi_awaryjne_min_na_odb"] * 0.868).round(2)
    prelim.loc[oct_nn, "saidi_awaryjne_min_na_odb"] = (
        prelim.loc[oct_nn, "saidi_awaryjne_min_na_odb"] * 0.904).round(2)
    with pd.ExcelWriter(os.path.join(TARGET, "sprawozdanie_URE_2026_wstepne_i_korekta.xlsx"),
                        engine="openpyxl") as xl:
        prelim.to_excel(xl, sheet_name="wstepne_2026", index=False)
        ret.to_excel(xl, sheet_name="korekta_1_2026", index=False)
        pd.DataFrame([
            dict(arkusz="wstepne_2026", zlozono="2026-11-10",
                 uwaga="dane wstepne koncesji, bez podzialu na oddzialy; listopad narastajaco "
                       "do 15 listopada, przed zamknieciem miesiaca"),
            dict(arkusz="korekta_1_2026", zlozono="2026-11-14",
                 uwaga="korekta pazdziernika po zamknieciu zdarzen; zastepuje dane wstepne"),
        ]).to_excel(xl, sheet_name="wydania", index=False)

    raw = pd.concat([base.e])
    lost = int((~base.e.map(lambda k: k).isin(set(reg.id_urzadzenia))).sum())
    counts = dict(legacy=n_leg, current=n_cur, notifications=len(nlw), scada=len(scw),
                  devices=len(reg), feeders=len(fd), programme=len(prog), planned=len(pl),
                  planned_jobs=int(pl.id_pracy.nunique()),
                  ppe=len(ppe), quality=len(q), vegetation=len(veg))
    return dict(fd=fd, dv=dv, ev=ev, nl=nl, sc=sc, reg=reg, prog=prog, pl=pl, ppe=ppe,
                returns=ret, prelim=prelim, counts=counts, ivr_blank=ivr_blank, orph=orph,
                raw_join_lost=lost,
                nl_shipped=out, resave=len(rep),
                served=dict(served_by.astype(int)))


if __name__ == "__main__":
    st = build()
    import documents, goldens
    documents.write_all(st)
    goldens.write_all(st)
    import subprocess
    scrub = os.path.join(os.path.dirname(TASK), ".claude", "skills",
                         "reduce-house-fixes", "scripts", "scrub_producer_metadata.py")
    for d in (TARGET, os.path.join(TASK, "golden")):
        r = subprocess.run([sys.executable, scrub, d, "--apply",
                            "--producer", "Borowiecka Energia Operator", "--stamp", "2026-11-16"],
                           capture_output=True, text=True)
        if r.returncode != 0:
            print(r.stdout[-1500:]); print(r.stderr[-1500:])
            raise SystemExit("metadata scrub failed on %s" % d)
    normalise_containers(TARGET)
    normalise_containers(os.path.join(TASK, "golden"))
    for root, _, files in os.walk(TARGET):
        for f in files:
            os.utime(os.path.join(root, f), (MTIME, MTIME))
    for root, _, files in os.walk(os.path.join(TASK, "golden")):
        for f in files:
            os.utime(os.path.join(root, f), (MTIME, MTIME))
    print("target/: %d files" % sum(len(f) for _, _, f in os.walk(TARGET)))
    for k, v in st["counts"].items():
        print("  %-14s %d" % (k, v))
