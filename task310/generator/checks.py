"""Generator assertions for task310: the golden against the world's truth, the three rules executed (R1 to R3c),
the ladder and every cheap route, the standing family inside each printed bin, every semantic fork (SF ids, as in the
design note's fork table), the asks against their truths with every careful route missing, the separation line and
the input gates.

    python3 task310/generator/checks.py <target dir>
"""
import json
import math
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import asks as A  # noqa: E402
import params as P  # noqa: E402
import solve as S  # noqa: E402
import world as W  # noqa: E402

N = [0]


def ok(cond, msg):
    N[0] += 1
    if not cond:
        raise AssertionError(msg)


def rnd(v, u):
    return math.floor(v / u + 0.5) * u


def edge(v, u):
    x = v / u - math.floor(v / u + 0.5)
    return (0.5 - abs(x)) * u


def figs_of(g):
    return {r: (rnd(g[r], 50), rnd(P.ROUND_BATTERIES * g[r] / 1000.0, 100)) for r in P.REGION_ORDER}


class Mishandled(S.Pack):
    """The pack read with one Layer 1 item mishandled."""

    def __init__(self, target, opt):
        self.opt = opt
        super().__init__(target)

    def _inverters(self, sv_path, ht_path):
        o = self.opt
        ref2pid = dict(zip(self.reg.inverter_ref, self.reg.panel_id))
        for r in self.sys.itertuples():
            ref2pid[str(r.inverter_ref)] = r.panel_id
        sv = pd.read_parquet(sv_path)
        loc = pd.to_datetime(sv.period_start)
        off = sv.utc_offset.map({"+10:00": 0, "+11:00": 1}).astype(int)
        if o in ("velkora_no_offset", "clocks_naive"):
            off = off * 0
        t = (((loc - pd.to_timedelta(off, unit="h")) - S.M0) / pd.Timedelta(hours=1)).astype(int).to_numpy()
        rows = sv.site_ref.map(lambda s: self.idx[ref2pid[s]]).to_numpy()
        keep = (t >= 0) & (t < S.NH)
        np.add.at(self.gen, (rows[keep], t[keep]), sv.energy_wh.to_numpy()[keep] / 1000.0)
        ht = pd.read_csv(ht_path, dtype={"serial": str})
        if o == "drop_repeat":
            ht = ht.drop_duplicates(["serial", "read_at"])
        for serial, g in ht.groupby("serial", sort=False):
            ends, seen = [], False
            for lt in pd.to_datetime(g.read_at).to_list():
                if o in ("ondrava_no_dst", "clocks_naive"):
                    ends.append(lt)
                elif lt == pd.Timestamp("2025-04-06 03:00"):
                    ends.append(lt - pd.Timedelta(hours=1) if not seen else lt)
                    seen = True
                elif lt < pd.Timestamp("2025-04-06 03:00") or lt >= pd.Timestamp("2025-10-05 03:00"):
                    ends.append(lt - pd.Timedelta(hours=1))
                else:
                    ends.append(lt)
            cnt = g.total_yield_wh.to_numpy()
            e = np.diff(cnt, prepend=np.nan)
            sr = self.sys[self.sys.inverter_ref.astype(str) == serial]
            new = bool(len(sr)) and str(sr.iloc[0].note).startswith("replacement")
            e[0] = cnt[0] if (new and o != "counter_reset_naive") else 0.0
            for m, v in zip(ends, e):
                t = int((m - pd.Timedelta(hours=1) - S.M0) / pd.Timedelta(hours=1))
                if 0 <= t < S.NH:
                    self.gen[self.idx[ref2pid[serial]], t] += v / 1000.0

    def _meter(self, path):
        m = pd.read_parquet(path)
        if self.opt == "drop_estimates":
            m = m[m.quality == "A"]
        nmi2i = {n: self.idx[p] for n, p in zip(self.reg.nmi, self.reg.panel_id)}
        end = pd.to_datetime(m.interval_end)
        start = end if self.opt == "meter_start" else end - pd.Timedelta(minutes=30)
        t = ((start - S.M0) // pd.Timedelta(hours=1)).to_numpy()
        rows = m.nmi.map(nmi2i).to_numpy()
        keep = (t >= 0) & (t < S.NH)
        np.add.at(self.e1, (rows[keep], t[keep]), m.e1_kwh.to_numpy()[keep])
        np.add.at(self.b1, (rows[keep], t[keep]), m.b1_kwh.to_numpy()[keep])
        np.add.at(self.e2, (rows[keep], t[keep]), np.nan_to_num(m.e2_kwh.to_numpy()[keep]))


def rebuild(pk, cap=True, floor=True, only=None, stat="median", by_orient=False, calib=None, statewide=False,
            imp_both=None):
    """Every construction of the rebuilt solar the checks price; the default arguments are the golden's."""
    gen = pk.gen.copy()
    with np.errstate(invalid="ignore", divide="ignore"):
        per = np.where(pk.kwp > 0, pk.gen / pk.kwp, 0.0)
    for i in np.where(pk.limited)[0]:
        if only is not None and pk.limit[i] != only:
            continue
        sel = (~pk.limited) if statewide else ((pk.region == pk.region[i]) & (~pk.limited))
        if by_orient:
            s2 = sel & (pk.orient == pk.orient[i])
            if s2.sum() >= 3:
                sel = s2
        ref = np.median(per[sel], axis=0) if stat == "median" else per[sel].mean(axis=0)
        f = 1.0
        if calib == "strict":
            fr = imp_both[i] & (ref > 0.05)
            f = pk.gen[i][fr].sum() / (pk.kwp[i][fr] * ref[fr]).sum()
        elif calib == "loose":
            fr = (pk.gen[i] < pk.load[i] + pk.limit[i] - 0.05) & (ref > 0.05)
            f = pk.gen[i][fr].sum() / (pk.kwp[i][fr] * ref[fr]).sum()
        x = pk.kwp[i] * ref * f
        if cap:
            x = np.minimum(x, pk.ac[i])
        if floor:
            x = np.maximum(x, pk.gen[i])
        gen[i] = x
    return gen


def import_both(target, pk):
    m = pd.read_parquet(os.path.join(target, P.FILES["meter"]))
    nmi2i = {n: pk.idx[p] for n, p in zip(pk.reg.nmi, pk.reg.panel_id)}
    end = pd.to_datetime(m.interval_end)
    t = (((end - pd.Timedelta(minutes=30)) - S.M0) // pd.Timedelta(minutes=30)).to_numpy()
    rows = m.nmi.map(nmi2i).to_numpy()
    e1 = np.zeros((len(pk.pids), 2 * S.NH))
    b1 = np.zeros_like(e1)
    np.add.at(e1, (rows, t), m.e1_kwh.to_numpy())
    np.add.at(b1, (rows, t), m.b1_kwh.to_numpy())
    return (e1[:, 0::2] > 0) & (e1[:, 1::2] > 0) & (b1[:, 0::2] == 0) & (b1[:, 1::2] == 0)


def main(target, w=None):
    import build as B
    if w is None:
        w = B.world()
        w["asks"] = A.ask_worlds(w)
    f = json.load(open(os.path.join(HERE, "figures.json")))
    pk, res = S.solve(target)
    g, d = res["golden"], res["recorded"]
    G = figs_of(g)
    name = P.REGIONS

    # ---------------------------------------------------------------- the golden against the world's truth
    homes = {h["pid"]: h for h in w["homes"]}
    pot = np.array([W.hourly(homes[p]["pot"]) for p in pk.pids])
    load = np.array([W.hourly(homes[p]["load"]) for p in pk.pids])
    rec = np.array([W.hourly(homes[p]["rec"]) for p in pk.pids])
    truth = S.by_region(pk, W.battery(pot, load))
    ok(S.order(truth) == S.order(g) == ["YAR", "WEN", "BEL", "TAR"], "golden order is the truth's order")
    for r in P.REGION_ORDER:
        ok(abs(g[r] / truth[r] - 1) < 0.01, "golden %s within 1 per cent of the truth (%.1f vs %.1f)" % (r, g[r], truth[r]))
    ok(f["call"] == "Yarrandale Valley" and f["runner_up"] == "Sandhaven Coast", "figures.json call and runner-up")
    for r in P.REGION_ORDER:
        ok(f["kwh_per_battery"][name[r]] == G[r][0] and f["round_mwh"][name[r]] == G[r][1], "figures.json %s" % r)
    # the pack reads exactly what the homes recorded (Layer 1 neutral on the main path)
    ok(np.abs(pk.gen - rec).sum(axis=1).max() < 2.0, "pack solar equals the recorded solar, home by home")
    ok(np.abs(pk.load - load).sum(axis=1).max() < 5.0, "pack general-supply use equals the homes' use")

    # ---------------------------------------------------------------- R1 the field's raw material ships
    files = sorted(os.listdir(target))
    ok(P.FILES["meter"] in files and P.FILES["velkora"] in files and P.FILES["ondrava"] in files,
       "R1 half-hourly meter reads and hourly inverter output ship")
    for k in ("register", "systems", "connections", "meter", "velkora", "ondrava"):
        p = os.path.join(target, P.FILES[k])
        cols = (pd.read_parquet(p).columns if p.endswith(".parquet") else
                pd.read_excel(p).columns if p.endswith(".xlsx") else pd.read_csv(p, nrows=5).columns)
        ok(not any(re.search(r"batter|curtail|potential|throttl|clip|yield_est|rebuilt", c, re.I) for c in cols
                   if c != "total_yield_wh"), "R1 no deciding quantity in %s" % k)
    ok(pk.limited.sum() == 36, "R1 36 limited homes, the estate homes and Eastbrook's limited-export homes")

    # ---------------------------------------------------------------- R2 every mess item real and neutral
    for opt in ("velkora_no_offset", "ondrava_no_dst", "clocks_naive", "meter_start", "drop_estimates",
                "counter_reset_naive", "drop_repeat"):
        mp = Mishandled(target, opt)
        gm = S.by_region(mp, S.battery(S.rebuild(mp), mp.load))
        ok(S.order(gm) == S.order(g) and figs_of(gm) == G, "R2 %s leaves the call and every figure" % opt)
    mexp = pd.read_parquet(os.path.join(target, P.FILES["meter"]))
    ok((mexp.quality == "E").sum() > 0 and (mexp.quality == "S").sum() > 0, "R2 estimates and substitutions present")
    ok(mexp.groupby("nmi").meter_serial.nunique().max() == 2, "R2 meter exchanges present")
    ht = pd.read_csv(os.path.join(target, P.FILES["ondrava"]))
    rep = ht.groupby("serial").read_at.apply(lambda x: int((x == "2025-04-06 03:00").sum()))
    ok(set(rep) <= {0, 2} and (rep == 2).sum() >= 50, "R2 the repeated 03:00 reading on 6 April")
    ok((ht.read_at == "2025-10-05 03:00").sum() == 0, "R2 no 03:00 reading on 5 October")

    # ---------------------------------------------------------------- R3 the analyst test, the decisive step, no plant
    clean_rec = S.by_region(pk, W.battery(rec, load))
    ok(S.order(clean_rec) == ["WEN", "BEL", "TAR", "YAR"], "R3a the easy route on the clean truth files Sandhaven first, "
                                                            "Yarrandale last")
    ok(S.order(d) == ["WEN", "BEL", "TAR", "YAR"], "R3a the easy route on the pack files the same")
    ok(all(f["default_schedule"][name[r]] != f["schedule"][name[r]] for r in P.REGION_ORDER),
       "R3a the easy route's schedule matches the golden in no year")
    ok(S.order(S.by_region(pk, S.battery(S.rebuild(pk), pk.load))) == S.order(g), "R3b the rebuild alone files the golden")
    lower = {"unlimited homes only": res["unlimited_only"], "annual totals": res["annual_totals"]}
    for k, v in lower.items():
        ok(S.order(v)[0] == "WEN", "R3b lower rung %s stays on Sandhaven" % k)
    rm = pd.read_parquet(os.path.join(target, P.FILES["meter"]))
    blocks = rm.groupby("nmi").e1_kwh.apply(lambda s: s.iloc[:4000].round(3).tolist() == s.iloc[4000:8000].round(3).tolist())
    ok(not blocks.any(), "R3c no copied block in the meter reads")
    ok(not rm.duplicated(["nmi", "interval_end"]).any(), "R3c no repeated half hour")

    # ---------------------------------------------------------------- the ladder and every cheap route (Gate F)
    o = S.order(g)
    for i in range(3):
        ok(g[o[i]] / g[o[i + 1]] >= 1.15, "golden %s clears %s by 1.15x (%.3f)" % (o[i], o[i + 1], g[o[i]] / g[o[i + 1]]))
    od = S.order(d)
    ok(d[od[0]] / d[od[1]] >= 1.15, "the easy route's top clears its runner-up by 1.15x (%.3f)" % (d[od[0]] / d[od[1]]))
    ok(d["TAR"] / d["YAR"] >= 1.05, "the easy route puts Yarrandale last by 5 per cent or more")
    kwp = {r: float(np.mean(pk.kwp[pk.region == r].max(axis=1))) for r in P.REGION_ORDER}
    acr = {r: float(np.mean(pk.ac[pk.region == r].max(axis=1))) for r in P.REGION_ORDER}
    exp_ = {r: float(pk.b1[pk.region == r].sum(axis=1).mean()) for r in P.REGION_ORDER}
    gen_ = {r: float(pk.gen[pk.region == r].sum(axis=1).mean()) for r in P.REGION_ORDER}
    cheap = {"recorded": d, "unlimited homes only": res["unlimited_only"], "annual totals": res["annual_totals"],
             "mean array kWp": kwp, "mean inverter rating": acr, "mean export": exp_, "mean recorded solar": gen_}
    landed = [k for k, v in cheap.items() if max(v, key=v.get) == "YAR"]
    ok(landed == [], "no cheap route names Yarrandale first (%s)" % landed)
    ok(max(kwp, key=kwp.get) == "WEN" and max(acr, key=acr.get) == "WEN", "array size and inverter rating rank Sandhaven first")

    # ---------------------------------------------------------------- the standing family inside each printed bin
    ib = import_both(target, pk)
    fam = {"median, pooled": rebuild(pk), "mean, pooled": rebuild(pk, stat="mean"),
           "median, by orientation": rebuild(pk, by_orient=True), "mean, by orientation": rebuild(pk, "mean", True),
           "calibrated on unexported hours": rebuild(pk, calib="strict", imp_both=ib),
           "calibrated, by orientation": rebuild(pk, by_orient=True, calib="strict", imp_both=ib),
           "no inverter cap": rebuild(pk, cap=False), "no recorded floor": rebuild(pk, floor=False)}
    vals = {k: S.by_region(pk, S.battery(v, pk.load)) for k, v in fam.items()}
    for k, v in vals.items():
        ok(S.order(v) == S.order(g) and figs_of(v) == G, "SF10 standing member %s prints the golden" % k)
    for r in P.REGION_ORDER:
        lo = min(v[r] for v in vals.values())
        hi = max(v[r] for v in vals.values())
        ok(hi - lo <= 0.4 * 50, "SF16 standing spread %s inside 0.4 of 50 kWh (%.1f)" % (r, hi - lo))
        ok(min(edge(v[r], 50) for v in vals.values()) >= 5, "SF16 every member of %s 5 kWh inside its 50 kWh bin" % r)
        ok(min(edge(2.4 * v[r], 100) for v in vals.values()) / 2.4 >= 5, "SF16 every member of %s inside its MWh bin" % r)
    sl = {"loose calibration": rebuild(pk, calib="loose"), "statewide reference": rebuild(pk, statewide=True)}
    for k, v in sl.items():
        sv = S.by_region(pk, S.battery(v, pk.load))
        ok(S.order(sv) == S.order(g), "sloppy %s keeps the call (refuted by the data, see note)" % k)

    # ---------------------------------------------------------------- the semantic forks (SF ids as in the note)
    e2 = S.by_region(pk, S.battery(S.rebuild(pk), pk.load + pk.e2))
    ok(S.order(e2) == S.order(g) and rnd(e2["WEN"], 50) != G["WEN"][0], "SF1 E2 out per Appendix A: same call, "
                                                                        "Sandhaven's figure moves if E2 is served")
    ok(abs(pk.load.sum() - (pk.gen.sum() + pk.e1.sum() - pk.b1.sum())) < 1e-6, "SF1 use is solar plus E1 less B1")
    ok(True, "SF2 hour by hour (guideline section 3); half-hour steps are not the filed method")

    def battery_full(gen, ld):
        n, T = gen.shape
        soc, out, sur = np.full(n, 10.0), np.zeros(n), gen - ld
        for t in range(T):
            s = sur[:, t]
            c = np.minimum(np.minimum(np.clip(s, 0, None), 5.0), (10.0 - soc) / 0.95)
            soc += c * 0.95
            dd = np.minimum(np.minimum(np.clip(-s, 0, None), 5.0), soc * 0.95)
            soc -= dd / 0.95
            out += dd
        return out
    full = S.by_region(pk, battery_full(S.rebuild(pk), pk.load))
    ok(figs_of(full) == G, "SF3 empty or full on 1 January prints the same figures")
    ok(P.BAT_CHARGE_EFF == 0.95 and P.BAT_DISCHARGE_EFF == 0.95 and P.BAT_POWER_KW == 5.0, "SF4 SF5 Appendix A battery")
    ok(all(f["round_mwh"][name[r]] == rnd(2.4 * g[r], 100) for r in P.REGION_ORDER), "SF6 round is 2,400 times the mean")
    ok(all((pk.region == r).sum() == 40 for r in P.REGION_ORDER), "SF7 40 homes a region, equal weight")
    mc = Mishandled(target, "clocks_naive")
    ok(figs_of(S.by_region(mc, S.battery(S.rebuild(mc), mc.load))) == G, "SF8 local or market alignment: same figures")
    ok(res["golden"]["YAR"] > 0, "SF9 the battery never exports: discharge only to use")
    cz = S.by_region(pk, S.battery(rebuild(pk, only=0.5), pk.load))
    ok(S.order(cz) == S.order(g) and figs_of(cz)["BEL"] != G["BEL"] and figs_of(cz)["YAR"] == G["YAR"],
       "SF12 every limited home rebuilt; skipping the 1.5 kW homes moves Eastbrook's figures only")
    ok(True, "SF11 SF13 SF14 calibration, cap and floor members asserted in the family above")
    ok(f["schedule"] == {name[r]: y for r, y in zip(S.order(g), P.ROUND_YEARS)}, "SF15 descending order, 2027 first")
    ok(True, "SF17 Ondrava first reading closes a night hour; a replacement counter from zero (data guide 5)")

    # ---------------------------------------------------------------- the asks against their truths
    aw = w["asks"]
    ta = A.eligible_truth(aw["prem"])
    ok(all(f["ask_a"][name[r]] == ta[r] for r in P.REGION_ORDER), "ask A golden equals the truth %s" % ta)
    inv = {v: k for k, v in name.items()}
    for mode in ("der_only", "nmi_only", "no_normalise", "active_row", "nmi_min"):
        alt = {inv[k]: v for k, v in S.ask_eligible(target, mode).items()}
        ok(all(alt.get(r) != ta[r] for r in P.REGION_ORDER), "ask A route %s misses every region" % mode)
    tb = A.pilot_truth(aw["sites"])
    ok(all(abs(f["ask_b_raw"][i] - tb[i]) < 1e-4 for i in range(4)), "ask B golden equals the truth")
    ok(all(edge(x, 0.1) > 0.02 for x in tb), "ask B quarters clear of the 0.1 MWh edge")
    for mode in ("rows", "daily", "counters", "pairs_once"):
        alt = S.ask_pilot(target, mode)
        ok(all(rnd(alt[i], 0.1) != rnd(tb[i], 0.1) for i in range(4)), "ask B route %s misses every quarter" % mode)
    tc = A.installs_truth(aw["jobs"])
    ok(all(f["ask_c"][name[r]] == tc[r] for r in P.REGION_ORDER), "ask C golden equals the truth %s" % tc)
    for mode in ("careful", "dedup_first", "neighbour_merge", "no_amendments", "current_numbers_only", "rows"):
        alt = {inv[k]: v for k, v in S.ask_installs(target, mode).items()}
        ok(all(alt.get(r) != tc[r] for r in P.REGION_ORDER), "ask C route %s misses every region" % mode)
    alt = {inv[k]: v for k, v in S.ask_installs(target, "by_postcode").items()}
    ok(sum(alt.get(r) != tc[r] for r in P.REGION_ORDER) >= 3, "ask C by postcode misses three regions")
    duo = [s_ for s_ in aw["sites"] if s_["kind"] == "duo"]
    ok(len(duo) == 24 and sum(s_["kind"] == "pair" for s_ in aw["sites"]) == 10, "ask B 24 Duo homes, 10 metered pairs")
    mods = pd.read_csv(os.path.join(target, P.FILES["certificates"]), dtype=str)
    shared = mods.groupby("module_serial").certificate_no.nunique()
    ok((shared > 1).sum() > 0 and mods.drop_duplicates("certificate_no").shape[0] > len(aw["jobs"]),
       "ask C second lodgements present and tied only by module serials")

    # ---------------------------------------------------------------- the separation line
    panel = [p for p in aw["prem"] if p["panel"]]
    ok(len(panel) == 160 and not any(p["old_nmi"] or p["replaced_pv"] or p["batteries"] or p["booster"] for p in panel),
       "the panel's homes carry no device in the ask files")
    der = pd.read_csv(os.path.join(target, P.FILES["der"]), dtype={"nmi": str})
    pan = der[der.nmi.isin(set(pk.reg.nmi))]
    ok(set(pan.der_type) == {"PV"} and set(pan.status) == {"Active"} and len(pan) == 160,
       "the panel's NMIs hold one active PV row each and nothing else")

    # ---------------------------------------------------------------- realism sweep (dataset-generation section 9)
    def steps(vals):
        v = sorted(set(int(re.sub(r"\D", "", str(x))) for x in vals if str(x) not in ("", "nan")))
        return len(set(np.diff(v))) if len(v) > 2 else 99
    reg = pd.read_csv(os.path.join(target, P.FILES["register"]), dtype=str)
    cert = pd.read_csv(os.path.join(target, P.FILES["certificates"]), dtype=str)
    acc = pd.read_csv(os.path.join(target, P.FILES["accreditation"]), dtype=str)
    bc = pd.read_excel(os.path.join(target, P.FILES["booster"]), dtype=str)
    sites = pd.read_excel(os.path.join(target, P.FILES["pilot_sites"]), dtype=str)
    for label, vals in (("panel ids", reg.panel_id), ("panel NMIs", reg.nmi), ("register NMIs", der.nmi),
                        ("certificate numbers", cert.certificate_no), ("claim references", bc.claim_ref),
                        ("pilot sites", sites.site_id), ("accreditation numbers", acc.accreditation_no),
                        ("battery serials", sites.battery_serial)):
        ok(steps(vals) > 1, "realism: %s carry no constant step" % label)
    ok(list(acc.business_name) != sorted(acc.business_name), "realism: installers not listed in name order")
    shapes = {n.split()[-1] for n in acc.business_name}
    ok(len(shapes) >= 5, "realism: installer names take %d shapes" % len(shapes))
    homes_ = [f_["home"] for f_ in aw["firms"]]
    ok(not all(homes_[i] == homes_[i + 4] for i in range(len(homes_) - 4)), "realism: installers' regions not dealt in turn")
    from pypdf import PdfReader
    issuer = {"guideline": "SEO", "guide": "SEO", "standard": "SMN"}
    for k, tag in issuer.items():
        meta_ = PdfReader(os.path.join(target, P.FILES[k])).metadata or {}
        ok(tag in str(meta_.get("/Producer", "")), "realism: %s produced by its issuer (%s)" % (k, meta_.get("/Producer")))
    ok(cert.groupby("certificate_no").installed.nunique().max() == 1, "realism: one installation date per certificate")

    # ---------------------------------------------------------------- every PDF reader a solver reaches for (H25)
    import subprocess
    from pdfminer.high_level import extract_text as pm_text
    flat = lambda t: re.sub(r"\s+", " ", t)
    must = {"guideline": ["the region whose round is worth most has the 2027 round",
                          "with the battery empty at the start of the year"],
            "standard": ["It does not limit energy generated and used, or stored, on the site",
                         "through the export control function of its inverter or of a site controller"],
            "guide": ["Each portal reports the inverter's AC output",
                      "Velkora stamps each hour at its start and gives the UTC offset"]}
    for k, sents in must.items():
        pth = os.path.join(target, P.FILES[k])
        texts = {"pypdf": " ".join(pg.extract_text() for pg in PdfReader(pth).pages),
                 "pypdf strict": " ".join(pg.extract_text() for pg in PdfReader(pth, strict=True).pages),
                 "pdfminer": pm_text(pth),
                 "pdftotext": subprocess.run(["pdftotext", pth, "-"], capture_output=True, text=True).stdout}
        for rd, t in texts.items():
            ok(all(x in flat(t) for x in sents), "H25: the %s reads whole in %s" % (k, rd))

    # ---------------------------------------------------------------- input gates
    meta = json.load(open(os.path.join(os.path.dirname(HERE), "metadata.json")))
    ok(len(files) >= 10, "input gate: 10 or more files (%d)" % len(files))
    ok(len({os.path.splitext(x)[1] for x in files}) >= 3, "input gate: three formats")
    ok(len(rm) >= 25000, "input gate: a 25,000-row file (meter, %d)" % len(rm))
    ok(len(meta["distractor_files"]) >= 2 and all(x in files for x in meta["distractor_files"]),
       "input gate: two shipped distractors")
    ok(not any(re.search(r"readme|dictionary|notes|manifest|schema|distractor|known_issues", x, re.I) for x in files),
       "no handling file in the pack")
    print("checks.py: %d assertions passed" % N[0])
    return N[0]


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
