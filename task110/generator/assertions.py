"""Every check the build must pass, run against the world in memory. File-level checks live in
verify_pack.py, which reads only the shipped bytes."""
import datetime as dt
from collections import defaultdict
from decimal import Decimal

import ledger as L
import solution as S
import world as W
from params import ACCOUNTS, COUNT_CUTOFF_LOCAL, MAP_V2, MAP_V3, SITES

D = Decimal
Z = D("0")
RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    if not ok:
        raise AssertionError("FAILED: %s %s" % (name, detail))


def pct(a, b):
    return float(a / b - 1) * 100


# ------------------------------------------------------------------ replay and balances
def replay_cells(eng, assets):
    c = defaultdict(lambda: Z)
    for a in assets:
        for m in L.REPLAY:
            x = eng.posting(a, m)
            if x:
                c[(ACCOUNTS[a["category"]][2], m)] += x
    return c


def accum_by_account(eng, assets, m):
    b = defaultdict(lambda: Z)
    for a in assets:
        if L.mdate(a["acquired"]) > m or (a["disposed"] and L.mdate(a["disposed"]) <= m):
            continue
        b[ACCOUNTS[a["category"]][1]] += eng.accumulated(a, m)
    return b


def ladder(w):
    LA = w.ledger_assets()
    T = L.Engine(LA)
    tc = replay_cells(T, LA)
    tj = accum_by_account(T, LA, L.JUN25)
    ts = accum_by_account(T, LA, L.SEP26)
    check("replay: 90 account-month cells under the truth", len(tc) == 90, len(tc))
    truth = S.solve(w)
    H = truth["h2"]
    cells = {}

    def run(name, variant, assets=None, clean=True):
        x = S.solve(w, variant) if clean else _solve_raw(w, variant)
        cells[name] = x["h2"]
        return x

    lure = run("R2 five-year", dict(upgrade="five"))
    endh = run("R3 end with host", dict(upgrade="endhost"))
    ten = run("ten-year", dict(upgrade="ten"))
    less1 = run("host remaining less one", dict(upgrade="host_less1"))
    run("five years unless the system runs out sooner", dict(upgrade="min60"))
    run("host remaining in whole years (down)", dict(upgrade="host_years_floor"))
    run("host remaining in whole years (nearest)", dict(upgrade="host_years_round"))
    check("rival: five years unless the system runs out sooner lands at least 3 per cent from the answer",
          abs(pct(cells["five years unless the system runs out sooner"], H)) >= 3, pct(cells["five years unless the system runs out sooner"], H))
    r1 = run("R1 cleaned, rules unapplied", dict(upgrade="five", it="retro48", impair=False, transfer="new"))
    r0 = _solve_raw(w, dict(upgrade="five", it="retro48", impair=False, transfer="new"))
    cells["R0 raw register"] = r0
    check("ladder: R0 > R1 > R2 > R3 > answer (each correction walks down)",
          r0 > cells["R1 cleaned, rules unapplied"] > cells["R2 five-year"] > cells["R3 end with host"] > H,
          {k: str(v) for k, v in cells.items()})
    check("ladder: the five-year path at least 15 per cent above the answer", pct(cells["R2 five-year"], H) >= 15, pct(cells["R2 five-year"], H))
    check("ladder: end-with-host at least 5 per cent above the answer", pct(cells["R3 end with host"], H) >= 5, pct(cells["R3 end with host"], H))
    check("ladder: R1 at least 15 per cent above the answer", pct(cells["R1 cleaned, rules unapplied"], H) >= 15)
    # the replay under each path
    for name, var, must_fail in (("five", dict(upgrade="five"), False), ("ten", dict(upgrade="ten"), True),
                                 ("endhost", dict(upgrade="endhost"), False), ("host_less1", dict(upgrade="host_less1"), True),
                                 ("host_full", dict(upgrade="host_full"), True), ("min60", dict(upgrade="min60"), True),
                                 ("host_years_floor", dict(upgrade="host_years_floor"), True),
                                 ("host_years_round", dict(upgrade="host_years_round"), True)):
        E = L.Engine(LA, var)
        c = replay_cells(E, LA)
        miss = [k for k in tc if tc[k] != c.get(k, Z)]
        check("replay: %s %s" % (name, "misses at least one cell" if must_fail else "reproduces every cell"), (len(miss) > 0) == must_fail, len(miss))
    # the replay and the balances certify the five-year path, every account-month and every balance date, to the cent
    E5 = L.Engine(LA, dict(upgrade="five"))
    EH = L.Engine(LA, dict(upgrade="endhost"))
    c5 = replay_cells(E5, LA)
    check("certify: the five-year path reproduces all 90 account-months to the cent", all(tc[k] == c5.get(k, Z) for k in tc))
    for lab, m in (("30 June 2024", L.mi(2024, 6)), ("30 June 2025", L.JUN25), ("30 September 2026", L.SEP26)):
        check("certify: the five-year path carries every account's balance at %s to the cent" % lab,
              accum_by_account(E5, LA, m) == accum_by_account(T, LA, m))
    for nm, e in (("host", T), ("five-year", E5), ("end-with-host", EH)):
        ends = {a["id"]: (min(e.end_month(a), T.host_end(a)) if nm == "end-with-host" else e.end_month(a))
                for a in LA if a["kind"] == "upgrade"}
        bad = [i for i, x in ends.items() if x in L.REPLAY or min(e.schedule(e.by_id[i])) in L.REPLAY]
        check("window: no upgrade schedule starts or ends inside the replay on the %s reading" % nm, not bad, bad)
    # the published controls: note 9 of the FY2025 report, the 2025 year and its 2024 comparative, by class, in whole dollars
    import docs as _docs
    pub = {y: _docs.ppe_note(w, T, y) for y in (2024, 2025)}

    def note_misses(e):
        out = []
        for y in (2024, 2025):
            g = _docs.ppe_note(w, e, y)
            for f in ("cost", "acc", "dep"):
                for c in _docs.PPE_CATS:
                    if S.rnd(g[f][c]) != S.rnd(pub[y][f][c]):
                        out.append((y, f, c, g[f][c] - pub[y][f][c]))
        return out
    for nm, e in (("five-year", E5), ("end-with-host", EH)):
        nm_ = note_misses(e)
        check("pin: the %s path misses note 9 only on the 2024 imaging depreciation" % nm,
              [(y, f, c) for y, f, c, _ in nm_] == [(2024, "dep", "Medical imaging equipment")], nm_)
        check("pin: the %s path misses it by $5,000 or more" % nm, bool(nm_) and abs(nm_[0][3]) >= 5000, [str(x[3]) for x in nm_])
    cells["pin: FY2024 imaging depreciation, five-year less published"] = note_misses(E5)[0][3]
    for nm, var in (("ten", dict(upgrade="ten")), ("host_less1", dict(upgrade="host_less1")), ("host_full", dict(upgrade="host_full")),
                    ("min60", dict(upgrade="min60")), ("host_years_floor", dict(upgrade="host_years_floor")),
                    ("host_years_round", dict(upgrade="host_years_round"))):
        e = L.Engine(LA, var)
        ce = replay_cells(e, LA)
        rmiss = sum(1 for k in tc if tc[k] != ce.get(k, Z))
        bmiss = sum(1 for m in (L.mi(2024, 6), L.JUN25, L.SEP26) if accum_by_account(e, LA, m) != accum_by_account(T, LA, m))
        check("back-test: %s fails at least one shipped control (replay, balances or note 9)" % nm,
              rmiss or bmiss or note_misses(e), (rmiss, bmiss))
    for nm in ("R2 five-year", "R3 end with host"):
        check("tolerance: %s, which the replay and the balances certify, lands 5 per cent or more from the answer" % nm,
              abs(pct(cells[nm], H)) >= 5, pct(cells[nm], H))
    # no single life reproduces the imaging account; sixty months is the best single life
    best = None
    for life in range(24, 121):
        def sch(a, life=life):
            return L.sl(a["cost"], life, L.mdate(a["acquired"]))
        tot = defaultdict(lambda: Z)
        for a in LA:
            s = sch(a) if a["kind"] == "upgrade" else T.schedule(a)
            if a["disposed"]:
                s = {k: x for k, x in s.items() if k <= L.mdate(a["disposed"])}
            for m in L.REPLAY:
                if ACCOUNTS[a["category"]][2] == "6-2110" and m in s:
                    tot[m] += s[m]
        err = sum((abs(tc[("6-2110", m)] - tot[m]) for m in L.REPLAY), Z)
        if best is None or err < best[1]:
            best = (life, err)
        if life == 60:
            check("sweep: a single upgrade life of 60 months reproduces the imaging account to the cent", err == 0, str(err))
        else:
            check("sweep: a single upgrade life of %d months does not reproduce the imaging account" % life, err > 0, str(err))
    check("sweep: sixty months is the only single life that reproduces it", best[0] == 60 and best[1] == 0, best)
    return truth, lure, endh, ten, less1, cells


def _solve_raw(w, variant):
    """The register as delivered: tracked items and repeated lines included."""
    eng = L.Engine([a for a in w.assets], variant)
    return sum((eng.h2(a) for a in w.assets if not a["disposed"]), Z)


# ------------------------------------------------------------------ construction layer and devices
def construction_layer(truth, lure):
    for s in SITES:
        for k in ("nbv_sep", "q4", "nbv_load", "h2"):
            d_ = abs(truth["sites"][s][k] - lure["sites"][s][k])
            check("construction: %s %s differs between the five-year path and the answer by $1,000 or more" % (s, k), d_ >= 1000, str(d_))
    for s in ("CHA", "MAI"):
        check("construction: %s nil-book-value count differs on the five-year path" % s,
              truth["sites"][s]["nil_count"] != lure["sites"][s]["nil_count"])
    check("construction: imaging class book value differs on the five-year path",
          abs(truth["classes"]["Imaging equipment"] - lure["classes"]["Imaging equipment"]) >= 1000)


def naive_seen(w, clock="dst", serial=True, sheet=True, move=True, start="local", trust_clock=False, plate_first=True):
    """A reading of the sightings. The defaults are the truth's; each keyword turns one device's wrong path on.
    start: 'local' the window opens at midnight Sydney time, 'utcdate' it opens on the UTC date, 'none' no start.
    trust_clock: take HH-07's Thursday times as written. plate_first False: the tag wins where both were read."""
    v = w.verification
    seen = {}
    by_tag = {a["tag"]: a for a in w.assets if a["tag"]}
    by_ser = {a["serial"]: a for a in w.assets if a["serial"] and a["kind"] != "duplicate"}
    start_utc = {"local": W.utc_from_local(W.WINDOW_START_LOCAL), "utcdate": dt.datetime(2026, 9, 28), "none": dt.datetime(1900, 1, 1)}[start]
    for a, site, t, tag, ser in v["scans"]:
        if trust_clock:
            t = v["clock"].get((a["id"] if a else None, t), t)
        if t < start_utc:
            continue
        if clock == "dst":
            local = t + dt.timedelta(hours=11) if t >= dt.datetime(2026, 10, 3, 16) else t + dt.timedelta(hours=10)
        elif clock == "aest":
            local = t + dt.timedelta(hours=10)
        else:
            local = t
        if local >= COUNT_CUTOFF_LOCAL:
            continue
        if plate_first and serial and ser in by_ser:
            hit = by_ser[ser]
        else:
            hit = by_tag.get(tag) if tag else (by_ser.get(ser) if serial else None)
        if hit is not None:
            seen[hit["id"]] = site if move else hit["site"]
    if sheet:
        for a, site in v["sheet"]:
            seen[a["id"]] = site if move else a["site"]
    return seen


def devices(w, truth):
    H = truth["h2"]
    tbl = {}
    for name, kw in (("clock AEST", dict(clock="aest")), ("clock UTC", dict(clock="utc")), ("tag-only join", dict(serial=False)),
                     ("no count sheet", dict(sheet=False)), ("register site", dict(move=False))):
        x = S.solve(w, seen=naive_seen(w, **kw))
        check("separation: device '%s' leaves the main call unchanged" % name, x["h2"] == H)
        moved = {}
        for s in SITES:
            for k in truth["sites"][s]:
                if x["sites"][s][k] != truth["sites"][s][k]:
                    moved["%s.%s" % (s, k)] = x["sites"][s][k] - truth["sites"][s][k]
        tbl[name] = moved
        check("device: '%s' moves at least one ask figure" % name, len(moved) > 0, moved)
    x = S.solve(w, mapping=MAP_V3_FULL())
    check("separation: mapping v3 leaves the main call unchanged", x["h2"] == H)
    tbl["mapping v3"] = {k: x["classes"].get(k, Z) - truth["classes"].get(k, Z) for k in set(x["classes"]) | set(truth["classes"])
                         if x["classes"].get(k, Z) != truth["classes"].get(k, Z)}
    check("device: mapping v3 moves at least three class figures", len(tbl["mapping v3"]) >= 3, tbl["mapping v3"])
    x = S.solve(w, reclass=False)
    check("separation: the September reclass leaves the main call unchanged", x["h2"] == H)
    tbl["first TB run"] = {k: x["classes"].get(k, Z) - truth["classes"].get(k, Z) for k in truth["classes"]
                           if x["classes"].get(k, Z) != truth["classes"].get(k, Z)}
    check("device: the first TB run moves the furniture and leasehold class figures", len(tbl["first TB run"]) == 2, tbl["first TB run"])
    x = S.solve(w, dict(transfer="new"))
    check("separation: the Bremer transfer read as a new asset leaves the committed whole-dollar figure unchanged",
          S.rnd(x["h2"]) == S.rnd(H), str(x["h2"] - H))
    wo = truth["written_off"]
    check("walk: every written-off asset is already at nil on 30 September and charges nothing in October to December",
          all(truth["eng"].nbv(a, L.SEP26) == 0 and truth["eng"].q4(a) == 0 for a in wo), [a["id"] for a in wo])
    tbl["transfer as new"] = {k: x["classes"].get(k, Z) - truth["classes"].get(k, Z) for k in truth["classes"]
                              if x["classes"].get(k, Z) != truth["classes"].get(k, Z)}
    # every site's nil count is hit by at least one verification device
    for s in SITES:
        hit = [n for n in ("clock AEST", "tag-only join", "no count sheet", "register site") if "%s.nil_count" % s in tbl[n]]
        check("device: %s nil count moves under at least one verification device" % s, len(hit) >= 1, hit)
    for s in SITES:
        check("device: %s Jan-Jun charge moves when sites are left on the register" % s, "%s.h2" % s in tbl["register site"])
    return tbl


def scan_devices(w, truth):
    """The handheld export's two devices. Each wrong reading leaves the committed figure where it is and costs
    whole rubric blocks: the label read by its tag moves the walk at two sites; the window read with no start loads
    an asset at nil that was only seen on trial day; the window read on HH-07's clock as written drops an asset at
    nil that loads and leaves a moved one at its register site."""
    v = w.verification
    d = v["scan_devices"]
    H = truth["h2"]
    check("scan devices: truth equals the reading with every default", naive_seen(w) == S.sighting(w))
    # the shapes the generator planted
    b, a_ = d["label_on"], d["label_off"]
    rows_b = [s for s in v["scans"] if s[0] is b]
    check("label: the moved unit is scanned once, wearing the other unit's tag with its own plate keyed",
          len(rows_b) == 1 and rows_b[0][3] == a_["tag"] and rows_b[0][4] == b["serial"], rows_b)
    check("label: the unit whose tag it wears is sighted on its own plate at its own site",
          all(s[3] == "" and s[4] == a_["serial"] and s[1] == a_["site"] for s in v["scans"] if s[0] is a_))
    incons = [s for s in v["scans"] if s[0] and s[3] and s[4] and s[0]["tag"] != s[3]]
    check("label: exactly one scan reads a tag and a plate that belong to different units", len(incons) == 1, len(incons))
    clk = v["clock"]
    check("clock: every rewritten time is a Cessnock scan on Thursday 8 October", all(k[1].date() in (dt.date(2026, 10, 7), dt.date(2026, 10, 8)) for k in clk))
    check("clock: HH-07's Thursday reads 1 January 2025", all(x.date() == dt.date(2025, 1, 1) for x in clk.values()), len(clk))
    wit = d["clock_witness"]
    check("clock: a Thursday scan shows an asset bought after the date the clock wrote",
          any(k[0] == wit["id"] and clk[k].date() < wit["acquired"] for k in clk))
    for x, name in ((d["clock_only"], "moved asset"), (d["clock_nil"], "asset at nil")):
        rows = [s for s in v["scans"] if s[0] is x]
        check("clock: the %s is sighted only on Thursday" % name, rows and all((x["id"], s[2]) in clk for s in rows), len(rows))
    import docs as _docs
    src = open(_docs.__file__).read()
    check("label: no shipped sentence makes the tag govern where a plate was also read", "missing or cannot be read" not in src)
    start_utc = W.utc_from_local(W.WINDOW_START_LOCAL)
    trial_assets = {s[0]["id"] for s in v["scans"] if s[0] and s[2] < start_utc}
    for i in trial_assets - {d["trial_only"]["id"]}:
        check("trial: %s is also sighted inside the window" % i,
              any(s[0] and s[0]["id"] == i and start_utc <= s[2] < W.utc_from_local(COUNT_CUTOFF_LOCAL) for s in v["scans"]))
    ces = sorted((s for s in v["scans"] if s[1] == "CES"), key=lambda s: s[2])
    k_in = [j for j, s in enumerate(ces) if ((s[0]["id"] if s[0] else None), s[2]) in clk]
    before, after = ces[k_in[0] - 1], ces[k_in[-1] + 1]
    for nm, s in (("before", before), ("after", after)):
        check("clock: the scan %s the run is a tag scan inside the window" % nm,
              s[3] and start_utc <= s[2] < W.utc_from_local(COUNT_CUTOFF_LOCAL) and (s[0]["id"], s[2]) not in clk, s[3])
    t_ = d["trial_only"]
    rows = [s for s in v["scans"] if s[0] is t_]
    check("trial: the asset at nil is sighted only on 25 September", rows and all(s[2] < W.utc_from_local(W.WINDOW_START_LOCAL) for s in rows))
    check("trial: it is at nil on 30 September and written off", truth["eng"].nbv(t_, L.SEP26) == 0 and t_ in truth["written_off"])
    # each wrong reading: the committed figure holds, whole rubric blocks move by more than any reasonable band
    acc = lambda x: sum((r["acc_dec"] for r in x["rows"]), Z)

    def moves(x):
        out = {}
        for k, f in (("rows", lambda y: y["load_rows"]), ("cost", lambda y: y["load_cost"]), ("acc_dec", acc)):
            if f(x) != f(truth):
                out[k] = f(x) - f(truth)
        for s in SITES:
            for k in ("nbv_sep", "q4", "nbv_load", "h2", "nil_count", "nil_cost"):
                dd = x["sites"][s][k] - truth["sites"][s][k]
                if dd:
                    out["%s.%s" % (s, k)] = dd
        return out
    tbl = {}
    for name, kw, need in (
            ("tag before plate", dict(plate_first=False), ["%s.%s" % (s, k) for s in (b["site"], "CHA") for k in ("nbv_sep", "q4", "nbv_load", "h2")]),
            ("no window start", dict(start="none"), ["rows", "cost", "acc_dec", "MAI.nil_count", "MAI.nil_cost"]),
            ("HH-07 clock as written", dict(trust_clock=True), ["rows", "cost", "acc_dec", "CES.nil_count", "CES.nil_cost"]
             + ["%s.%s" % (s, k) for s in (d["clock_only"]["site"], "CES") for k in ("nbv_sep", "q4", "nbv_load", "h2")]),
            ("UTC-date start, clock as written", dict(start="utcdate", trust_clock=True), ["rows", "cost", "acc_dec"]),
            ("tag first, no window start", dict(plate_first=False, start="none"), ["rows", "CHA.h2"]),
            ("tag first, clock as written", dict(plate_first=False, trust_clock=True), ["rows", "CHA.h2", "CES.h2"])):
        x = S.solve(w, seen=naive_seen(w, **kw))
        check("separation: '%s' leaves the committed figure to the cent" % name, x["h2"] == H, str(x["h2"] - H))
        mv = moves(x)
        tbl[name] = mv
        for k in need:
            band = 0 if k in ("rows",) or k.endswith("nil_count") else D("10")
            check("scan device '%s' moves %s beyond the band" % (name, k), k in mv and abs(mv[k]) > band, mv.get(k))
    return tbl


def host_text(w):
    """The capex log keys only retirements, so each upgrade's system is identified from its request text.
    Every reading of that text (the register's model prefix, a prefix match, a case-blind containment)
    selects the same single in-service system, and it is the one the legacy ledger spread the upgrade over."""
    by_ref = {r["ref"]: r for r in w.approvals}
    ups = [a for a in w.assets if a["kind"] == "upgrade"]
    for a in ups:
        r = by_ref[a["approval"]]
        check("host text: %s carries no Existing Asset key" % r["ref"], r["existing"] == "", r["existing"])
        system, site = r["description"].rsplit(" for ", 1)[1].rsplit(", ", 1)
        pool = [h for h in w.assets if h["category"] == "Medical imaging equipment" and h["acquired"] <= a["acquired"]
                and (not h["disposed"] or h["disposed"] > a["acquired"]) and SITES[h["site"]] == site]
        reads = [[h["id"] for h in pool if h["description"].split(" - ")[0] == system],
                 [h["id"] for h in pool if h["description"].startswith(system)],
                 [h["id"] for h in pool if system.lower() in h["description"].lower()]]
        check("host text: %s names exactly one system under every reading" % r["ref"],
              all(x == [a["host"]] for x in reads), reads)
    check("host text: every upgrade checked", len(ups) == 16, len(ups))
    check("host text: Existing Asset filled only on replacement rows",
          all(r["type"] == "Replacement" for r in w.approvals if r["existing"]))


def MAP_V3_FULL():
    return dict(MAP_V3)


def footing(truth):
    for k in ("nbv_sep", "q4", "nbv_load", "h2", "nil_cost"):
        parts = sum(S.rnd(truth["sites"][s][k]) for s in truth["sites"])
        whole = S.rnd(sum((truth["sites"][s][k] for s in truth["sites"]), Z))
        check("footing: the four sites' %s, rounded, add to the rounded total" % k, parts == whole, (parts, whole))
    check("footing: the class book values, rounded, add to the rounded load book value",
          sum(S.rnd(v) for v in truth["classes"].values()) == S.rnd(truth["load_nbv"]))
    check("footing: the site charges add to the committed figure", S.rnd(sum((truth["sites"][s]["h2"] for s in truth["sites"]), Z)) == S.rnd(truth["h2"]))


def bins(truth):
    figs = {"h2": truth["h2"]}
    for s in SITES:
        for k in ("nbv_sep", "q4", "nbv_load", "h2", "nil_cost"):
            figs["%s.%s" % (s, k)] = truth["sites"][s][k]
    for c, v in truth["classes"].items():
        figs["class " + c] = v
    for k, v in figs.items():
        frac = (D(v) - D(int(D(v)))) % 1
        check("bins: %s sits clear of the rounding boundary" % k, abs(frac - D("0.5")) >= D("0.03"), str(v))
        check("tells: %s does not land on a round thousand" % k, S.rnd(v) % 1000 != 0, str(v))
    return figs
