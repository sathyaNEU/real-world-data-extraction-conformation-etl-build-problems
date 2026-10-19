"""task248 records: every data file of the pack, built from the simulator.

Layer 1, as the service's, the laboratory's and the water company's systems produce it: the laboratory's export keeps
every analysis run (a sample re-extracted after an inhibited run, or repeated after a high result, appears twice), the
composite's flow is the figure the plant operator writes on the chain-of-custody form from the autosampler's
controller, the contract laboratory that covered the January closure reports gene copies per microlitre of extract
under its own site names, the historian exports local time across the daylight saving changes and, since the
outstations moved to the new cellular network in October 2027, has gaps, held readings and meter faults, the paired
study's field team reports gene copies per millilitre in triplicate, and the travel times sit in the network
modeller's memo."""
import datetime as dt

import numpy as np
import pandas as pd

import estim as E
import params as P
import sim

TWO_CHANNEL = {"KSB": 0.24, "PLH": 0.27, "UWD": 0.22}     # channel A's share of the inflow once channel B is in
TWO_CHANNEL_FROM = dt.date(2027, 10, 18)
CONTRACT = (dt.date(2027, 12, 23), dt.date(2028, 1, 9))    # composites the contract laboratory analysed
# the contract method: wastewater concentrated (mL), the pellet resuspended (mL), the aliquot extracted (microlitres),
# the extract eluted (microlitres)
CONTRACT_ML, CONTRACT_RESUSP_ML, CONTRACT_ALIQ_UL, CONTRACT_UL = 100.0, 2.0, 200.0, 100.0
CONTRACT_BIAS = -0.05                                      # the contract method's recovery against the laboratory's
ASK_A = (dt.date(2027, 4, 1), dt.date(2028, 3, 31))         # the flow-data hours, local days
ASK_B = (dt.date(2027, 10, 4), dt.date(2028, 3, 30))        # the faecal-strength check's composites
FAULTS = (dt.date(2027, 10, 1), dt.date(2028, 3, 30))       # the historian's faults, local days
SPOIL_COUNTS = [0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 7, 7]
CONTRACT_SITE = {"ADN": "ARDENMOUTH NTH WWTP", "ADS": "ARDENMOUTH STH WWTP"}


def world():
    rng = np.random.default_rng(7)
    amp, shift = sim.amp27(rng)
    return sim.make(amp=amp, shift=shift)


class Records:
    def __init__(self, W=None):
        self.W = W if W is not None else world()
        self.H = sim.hourly(self.W)
        self.C = sim.composites(self.W, self.H)
        self.study_rows = sim.study(self.W, self.H)
        self.codes = [p[0] for p in P.PLANTS]
        self._scada = None
        self._faults()
        self._sampler_faults()
        self._form_flows()

    # ------------------------------------------------------------ the historian's faults (Ask A)
    def _faults(self):
        """per plant: telemetry drop-outs (no row), blank values (a bad-quality reading), held readings (the outstation
        repeats its last reading while its link is down) and meter faults (zero or below); and a few blocks the
        historian re-sent after an outage, exported twice"""
        rng = np.random.default_rng(P.SEED + 7)
        loc = self.H["local"]
        n = len(loc)
        day = np.array([t.date() for t in loc])
        ok = (day >= FAULTS[0]) & (day <= FAULTS[1])
        S = P.NPLANT
        self.drop = np.zeros((S, n), dtype=bool)
        self.blank = np.zeros((S, n), dtype=bool)
        self.hold = np.zeros((S, n), dtype=bool)     # the held readings (every reading after the run's first)
        self.zero = np.zeros((S, n), dtype=bool)
        self.dup = np.zeros((S, n), dtype=bool)
        self.neg = {}
        for s in range(S):
            used = np.zeros(n, dtype=bool)

            def place(L, pad=2):
                for _ in range(500):
                    a = int(rng.choice(np.where(ok)[0]))
                    lo, hi = a - pad, a + L + pad
                    if hi >= n or not ok[a:a + L].all() or used[max(lo, 0):hi].any():
                        continue
                    used[max(lo, 0):hi] = True
                    return a
                raise RuntimeError("no room")
            for _ in range(int(rng.integers(2, 7))):
                L = int(rng.integers(1, 13))
                a = place(L)
                self.drop[s, a:a + L] = True
            for _ in range(int(rng.integers(0, 5))):
                a = place(1)
                self.blank[s, a] = True
            for _ in range(int(rng.integers(0, 4))):
                L = int(rng.integers(5, 13))            # the run's first reading and L - 1 held after it
                a = place(L)
                self.hold[s, a + 1:a + L] = True
            for _ in range(int(rng.integers(0, 3))):
                L = int(rng.integers(1, 4))
                a = place(L)
                self.zero[s, a:a + L] = True
                for h in range(a, a + L):
                    self.neg[(s, h)] = 0.0 if rng.random() < 0.5 else -round(float(rng.uniform(0.3, 2.4)), 2)
            for _ in range(int(rng.integers(0, 3))):
                L = int(rng.integers(3, 9))
                a = place(L)
                self.dup[s, a:a + L] = True

    def span_hours(self):
        """the hours the historian export spans, on the clock as it ran"""
        return len(self.H["hours"])

    def flow_valid(self):
        """each plant's hours (UTC hour index) with a valid inlet flow reading"""
        return ~(self.drop | self.blank | self.hold | self.zero)

    def scada(self):
        if self._scada is not None:
            return self._scada
        H = self.H
        rows = []
        stamps = [lt.strftime("%Y-%m-%d %H:%M") for lt in H["local"]]
        for s, code in enumerate(self.codes):
            F, T = H["F"][s], H["T"][s]
            last = None
            for h in range(len(stamps)):
                if self.drop[s, h]:
                    continue
                if self.hold[s, h]:
                    f, t = last
                elif self.blank[s, h]:
                    f, t = "", "%.1f" % T[h]
                elif self.zero[s, h]:
                    v = self.neg[(s, h)]
                    f, t = "%.2f" % v if v else "0.00", "%.1f" % T[h]
                else:
                    f, t = "%.2f" % F[h], "%.1f" % T[h]
                if not self.hold[s, h]:
                    last = (f, t)
                rows.append((code, stamps[h], f, t))
                if self.dup[s, h]:
                    rows.append((code, stamps[h], f, t))
        self._scada = pd.DataFrame(rows, columns=["plant_code", "timestamp_local", "inlet_flow_m3h", "inlet_temperature_c"])
        return self._scada

    # ------------------------------------------------------------ the samplers (Ask B)
    def _sampler_faults(self):
        """composites a blocked intake spoiled (the sampler drew mostly the channel's surface water): both targets far
        below the town's load. Each plant's count over the check's window comes from a seeded order of SPOIL_COUNTS;
        the window's first two and last two composites are never spoiled."""
        rng = np.random.default_rng(P.SEED + 13)
        counts = list(rng.permutation(SPOIL_COUNTS))
        idx = [i for i, c in enumerate(self.C) if ASK_B[0] <= c["d"] <= ASK_B[1]]
        inner = idx[2:-2]
        self.spoiled = {}
        for s in range(P.NPLANT):
            for i in rng.choice(inner, size=int(counts[s]), replace=False):
                self.spoiled[(s, int(i))] = float(rng.uniform(0.75, 1.1))
        for (s, i), drop in self.spoiled.items():
            self.C[i]["conc"] = self.C[i]["conc"].copy()
            self.C[i]["pconc"] = self.C[i]["pconc"].copy()
            self.C[i]["conc"][s] *= 10 ** -drop
            self.C[i]["pconc"][s] *= 10 ** -drop

    def _form_flows(self):
        """the flow the operator writes on the chain-of-custody form: the autosampler controller's flow total, which
        at a plant with two inlet channels covers the channel the sampler stands in"""
        rng = np.random.default_rng(P.SEED + 5)
        cal = rng.normal(0, 0.02, P.NPLANT)              # each controller's meter against the inlet meter
        self.form = {}
        for i, c in enumerate(self.C):
            for s, code in enumerate(self.codes):
                f = c["Fw"][s] * (1 + cal[s]) * (1 + rng.normal(0, 0.01))
                if code in TWO_CHANNEL and c["d"] >= TWO_CHANNEL_FROM:
                    f *= TWO_CHANNEL[code]
                self.form[(s, i)] = int(round(f))

    # ------------------------------------------------------------ the laboratory
    def results(self):
        """the laboratory's export: one row per sample, target and analysis run (a plate a day for each half of the
        plants, a re-extraction two days later)"""
        rng = np.random.default_rng(P.SEED + 11)
        rows = []
        self.runs = {}
        for i, c in enumerate(self.C):
            d = c["d"]
            if CONTRACT[0] <= d <= CONTRACT[1]:
                continue
            for s, code in enumerate(self.codes):
                flow = self.form[(s, i)]
                sid = "%s-%s" % (code, d.strftime("%y%m%d"))
                end = "%s 08:00" % d.isoformat()
                kind = rng.random()
                for tgt, val in (("N1", c["conc"][s]), ("PMMoV", c["pconc"][s])):
                    runs = []
                    if kind < 0.035:
                        runs.append(("rejected", val * 10 ** rng.normal(-0.6, 0.15), "inhibited: BCoV recovery below 1%"))
                        runs.append(("accepted", val, "re-extracted"))
                    elif kind < 0.05 and tgt == "N1":
                        runs.append(("accepted", val, ""))
                        runs.append(("check", val * 10 ** rng.normal(0, 0.04), "repeat of a high result"))
                    else:
                        runs.append(("accepted", val, ""))
                    self.runs[(s, i, tgt)] = runs
                    for k, (st, v, note) in enumerate(runs):
                        ad = d + dt.timedelta(days=1 + 2 * k)
                        plate = "P%s-%d" % (ad.strftime("%y%m%d"), 1 + (s >= 12))
                        rows.append((sid, code, end, tgt, plate, ad.isoformat(), "%.0f" % v, st, flow, note))
        return pd.DataFrame(rows, columns=["sample_id", "plant_code", "composite_end", "target", "plate", "analysed",
                                           "result_gc_per_l", "status", "composite_flow_m3", "comment"])

    def contract_rows(self):
        """the contract laboratory's results for the closure: gene copies per microlitre of extract"""
        rng = np.random.default_rng(P.SEED + 17)
        factor = contract_factor()                           # copies per microlitre of extract to copies per litre
        rows, k = [], 0
        for i, c in enumerate(self.C):
            d = c["d"]
            if not (CONTRACT[0] <= d <= CONTRACT[1]):
                continue
            for s, code in enumerate(self.codes):
                site = CONTRACT_SITE.get(code, P.PLANTS[s][1].upper() + " WWTP")
                received = next_working_day(d)
                for tgt, val in (("SARS-CoV-2 N1", c["conc"][s]), ("PMMoV", c["pconc"][s])):
                    v = val * 10 ** (CONTRACT_BIAS + rng.normal(0, 0.03)) / factor
                    rows.append(("WL%06d" % (418230 + k), site, d, received, tgt, float("%.3g" % v), self.form[(s, i)]))
                    k += 1
        return rows

    # ------------------------------------------------------------ the register, the travel times and the study
    def register(self):
        rows = []
        for p in P.PLANTS:
            rows.append((p[0], p[1] + " WWTP", p[2], p[3]))
        return pd.DataFrame(rows, columns=["plant_code", "plant_name", "serves", "population_served"])

    def travel(self):
        """the network model's population-weighted travel times and the sub-catchments behind them"""
        rng = np.random.default_rng(P.SEED + 19)
        out = []
        for p in P.PLANTS:
            tt = p[4]
            nsub = int(rng.integers(3, 9)) if tt > 200 else int(rng.integers(1, 4))
            lo = int(round(tt * rng.uniform(0.25, 0.6)))
            hi = int(round(tt * rng.uniform(1.25, 1.6)))
            out.append((p[0], p[1], nsub, tt, lo, hi))
        return out

    def study(self):
        """the paired upstream study as the field team keeps it: a row per plant, visit, point and replicate"""
        rng = np.random.default_rng(P.SEED + 23)
        rows = []
        missed = {("NTL", dt.date(2026, 6, 8)), ("ADS", dt.date(2026, 10, 26)), ("DNK", dt.date(2026, 12, 21))}
        for r in self.study_rows:
            d = r["d"]
            if (r["site"], d) in missed:
                continue
            up_end = dt.datetime.combine(d, dt.time(8, 0)) + dt.timedelta(minutes=int(rng.integers(-6, 19)))
            # the plant's sampler set to the travel time rounded to the quarter hour, started on the operator's round
            lag = dt.timedelta(minutes=int(15 * round(r["tt"] * 4)) + int(rng.integers(-5, 21)))
            ph, cond = rng.uniform(7.0, 7.8), rng.uniform(600, 1100)
            for point, n1, pm, T, end in (("upstream", r["up"], r["pm_up"], r["Tup"], up_end),
                                          ("plant", r["pl"], r["pm_pl"], r["Tin"], up_end + lag)):
                Tp = T + rng.normal(0, 0.2)
                for rep in (1, 2, 3):
                    rows.append((r["site"], d.isoformat(), point, (end - dt.timedelta(hours=24)).strftime("%Y-%m-%d %H:%M"),
                                 end.strftime("%Y-%m-%d %H:%M"), rep,
                                 "%.2f" % (n1 * 10 ** rng.normal(0, 0.03) / 1000.0),
                                 "%.0f" % (pm * 10 ** rng.normal(0, 0.03) / 1000.0),
                                 "%.1f" % Tp, "%.2f" % (ph + rng.normal(0, 0.05)), "%.0f" % (cond + rng.normal(0, 15))))
        return pd.DataFrame(rows, columns=["plant_code", "visit_date", "point", "composite_start", "composite_end",
                                           "replicate", "n1_copies_per_ml", "pmmov_copies_per_ml", "water_temperature_c", "ph",
                                           "conductivity_us_cm"])

    # ------------------------------------------------------------ the dashboard's own export (published basis)
    def dashboard(self):
        """the dashboard's published weekly levels and its alert episodes for winter 2027, on the load reaching the
        plant: each sample's accepted result times the form's flow, per person served"""
        dates = [c["d"] for c in self.C]
        lev_rows, eps = [], []
        for s, code in enumerate(self.codes):
            vals = []
            for i, c in enumerate(self.C):
                if (s, i, "N1") not in self.runs:
                    vals.append(None)
                    continue
                v = [x for x in self.runs[(s, i, "N1")] if x[0] == "accepted"][0][1]
                vals.append(np.log10(float("%.0f" % v) * self.form[(s, i)] * 1000.0 / P.PLANTS[s][3]))
            wk = E.weekly(dates, vals)
            lev, base = E.levels(dates, vals)
            for w in sorted(lev):
                if P.WINTER[0] <= w <= P.WINTER[1]:
                    nsamp = sum(1 for d, v in zip(dates, vals) if v is not None and E.monday(d) == w)
                    lev_rows.append((code, w, nsamp, round(wk[w], 3), round(base, 3), round(lev[w], 2), band(lev[w])))
            on, start, peak = False, None, None
            for w in sorted(lev):
                x = lev[w]
                if not on and x >= P.HIGH:
                    on, start, peak = True, w, x
                elif on:
                    peak = max(peak, x)
                    if x < P.LOW:
                        if P.WINTER[0] <= start <= P.WINTER[1]:
                            eps.append((code, start, w, round(peak, 2)))
                        on = False
            if on and P.WINTER[0] <= start <= P.WINTER[1]:
                eps.append((code, start, None, round(peak, 2)))
        return lev_rows, sorted(eps, key=lambda e: (e[1], self.codes.index(e[0])))

    # ------------------------------------------------------------ distractors
    def rainfall(self):
        rng = np.random.default_rng(P.SEED + 31)
        rows = []
        for i, d in enumerate(self.W["D"]):
            for gname in ("Ardenmouth Aero", "Kestrel Bay", "Pellingham", "Tarnbrook", "Upper Waldon", "Glenorrin"):
                mm = self.W["rain"][i] * rng.uniform(0.6, 1.4) if self.W["rain"][i] > 0 else \
                    (rng.gamma(0.5, 0.6) if rng.random() < 0.1 else 0.0)
                rows.append((gname, d.isoformat(), "%.1f" % mm))
        return pd.DataFrame(rows, columns=["gauge", "date_9am", "rainfall_mm"])

    def proficiency(self):
        """the laboratory's returns in the national external quality assessment scheme for wastewater SARS-CoV-2"""
        rng = np.random.default_rng(P.SEED + 37)
        rows = []
        for y in (2026, 2027):
            for q, m in enumerate((3, 6, 9, 11), 1):
                for k, assigned in enumerate((rng.uniform(3.6, 4.4), rng.uniform(4.6, 5.4))):
                    sd = 0.28
                    res = assigned + rng.normal(0.02, 0.12)
                    rows.append(("WW-%d-%d" % (y, q), dt.date(y, m, 1 + 7 * k), "EQA%d%02d%s" % (y % 100, q, "AB"[k]),
                                 "SARS-CoV-2 N1", round(assigned, 2), round(res, 2), round((res - assigned) / sd, 2)))
        return rows


HOLIDAYS = {dt.date(2027, 12, 27), dt.date(2027, 12, 28), dt.date(2028, 1, 3), dt.date(2028, 1, 4)}


def next_working_day(d):
    """the courier delivers on the next working day (New Zealand's Christmas and New Year holidays observed)"""
    r = d + dt.timedelta(days=1)
    while r.weekday() >= 5 or r in HOLIDAYS:
        r += dt.timedelta(days=1)
    return r


def contract_factor():
    """copies per microlitre of extract to copies per litre of wastewater: the extract holds the aliquot's copies, the
    aliquot is its share of the resuspended pellet, the pellet holds the concentrated wastewater's copies"""
    return CONTRACT_UL * (CONTRACT_RESUSP_ML * 1000.0 / CONTRACT_ALIQ_UL) / CONTRACT_ML * 1000.0


def band(x):
    if x >= P.VERY_HIGH:
        return "Very high"
    if x >= P.HIGH:
        return "High"
    if x >= P.LOW:
        return "Moderate"
    return "Low"
