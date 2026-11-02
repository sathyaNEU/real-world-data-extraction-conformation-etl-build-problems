"""The clean truth of the Tawi Bank world (task199, architecture 2).

Builds every posting, message, teller row, gateway row and salary row as plain Python records with their truth
labels, before any export layout or mess is applied. pack.py writes the exports from this; analysis.py and
verify.py never import it.
"""
import datetime as dt
import math
import numpy as np

import params as P

DAY = dt.timedelta(days=1)


# ---------------------------------------------------------------- calendar and rates
def is_business(d):
    return d.weekday() < 5 and d not in P.HOLIDAYS


def business_days(a, b):
    out, d = [], a
    while d <= b:
        if is_business(d):
            out.append(d)
        d += DAY
    return out


def add_business(d, n):
    k = 0
    while k < n:
        d += DAY
        if is_business(d):
            k += 1
    return d


def build_rates():
    """CBK-style mean rates for every business day of the logs' span, a random walk per currency."""
    rng = np.random.default_rng([P.SEED, 1])
    days = business_days(P.LOG_START, P.LOG_END)
    rates = {}
    for cur in ("USD", "EUR", "GBP"):
        x = P.FX_START[cur]
        series = {}
        for d in days:
            x = x + rng.normal(0.0, P.FX_SD[cur]) + (0.0015 if cur == "USD" else 0.0)
            series[d] = round(x, 4)
        rates[cur] = series
    return days, rates


def rate_on(rates, cur, d):
    """Mean rate for d, or the latest published before it (procedure 3.2)."""
    if cur == "KES":
        return 1.0
    s = rates[cur]
    while d not in s:
        d -= DAY
    return s[d]


# ---------------------------------------------------------------- accounts
def build_accounts(rng):
    accts = {}
    serial = 410000 + int(rng.integers(0, 9000))
    for c in P.CUSTOMERS:
        br = c["branch"][2]
        lst = []
        kinds = [("KES", "CA", "Current account")]
        if c["collection"]:
            kinds.append(("KES", "CL", "Collection account"))
        for f in c["fcy"]:
            kinds.append((f, "FC", "Foreign currency current account"))
        for cur, prod, desc in kinds:
            serial += int(rng.integers(7, 61))
            legacy = "%03d%07d%s" % (br, serial, {"CA": "01", "CL": "05", "FC": "21"}[prod] + "")
            legacy = legacy[:12] + str(sum(int(ch) for ch in legacy[:12]) % 10)
            new = "1%03d%s%07d%02d" % (br, {"KES": "1", "USD": "4", "EUR": "5"}[cur],
                                       int(rng.integers(1_000_000, 9_999_999)), int(rng.integers(10, 99)))
            lst.append(dict(cif=c["cif"], code=c["code"], cur=cur, prod=prod, desc=desc, legacy=legacy, new=new))
        accts[c["code"]] = lst
    return accts


# ---------------------------------------------------------------- name pools
LOCAL_FIRMS = [
    "Kirinyaga Agrovet Ltd", "Rongai Wholesalers", "Mutua & Sons Enterprises", "Kahawa Supermarkets Ltd",
    "Nyeri Fresh Produce Ltd", "Thika Road Motors", "Coastline Distributors", "Kisumu Lakeside Traders",
    "Machakos Builders Supplies", "Ngong Hills Hardware", "Embu Highway Stores", "Malindi Bay Resorts Ltd",
    "Eastleigh Textile Mart", "Kakamega Grain Millers", "Nakuru Agro Dealers", "Gikomba Traders Sacco",
    "Kitengela Steel Works", "Ruiru Packaging Ltd", "Athi River Cement Distributors", "Narok Transporters",
    "Kitale Seed Merchants", "Voi Petroleum Services", "Kilifi County Government", "Nairobi City Water",
    "Mombasa County Treasury", "Kenya Ports Logistics Ltd", "Lakeview Pharmacy", "Aga Mwema Hospital",
    "St. Jude Mission Hospital", "Afya Bora Clinics", "Tumaini Medical Centre", "Upendo Chemists",
    "Safari Trails Tours", "Big Five Holidays Ltd", "Tsavo Expeditions", "Rift Valley Safaris",
    "Highway Fleet Services", "Sunrise Bus Company", "Mlolongo Logistics", "Karatina Hardware",
    "Murang'a Building Centre", "Ol Kalou Farmers Coop", "Kenya Rural Roads Authority", "Kiambu County Government",
    "Westgate Electronics", "Moi Avenue Phones", "Luthuli Avenue Traders", "Biashara Street Wholesalers",
]
REGIONAL_BUYERS = [
    ("JUBA MERCHANDISE CENTRE CO LTD", "JUBA SOUTH SUDAN", "SS", "IVTBSSJB"),
    ("NILE CROSSING TRADERS LTD", "JUBA SOUTH SUDAN", "SS", "KDRNSSJB"),
    ("KAMPALA DOWNTOWN WHOLESALE LTD", "KAMPALA UGANDA", "UG", "CNTRUGKA"),
    ("GULU NORTHERN SUPPLIES LTD", "GULU UGANDA", "UG", "GULUUGKA"),
    ("GRANDS LACS COMMERCE SARL", "GOMA DR CONGO", "CD", "GOMACDKI"),
    ("KIGALI HORIZON IMPORTS LTD", "KIGALI RWANDA", "RW", "KGLIRWRW"),
]
SUPPLIERS_FCY = {
    "C01": [("TOKYO AUTO EXPORT CO LTD", "TOKYO JAPAN", "JP", "TKYOJPJT"),
            ("YOKOHAMA USED CARS INC", "YOKOHAMA JAPAN", "JP", "YKHMJPJT"),
            ("SHARJAH AUTO HUB FZE", "SHARJAH UAE", "AE", "SHRJAEAS")],
    "C04": [("GUANGZHOU HENGLI GARMENTS CO LTD", "GUANGZHOU CHINA", "CN", "GZHUCNBG"),
            ("YIWU SUNRISE COMMODITY CO LTD", "YIWU CHINA", "CN", "YIWUCNBY"),
            ("SHENZHEN BRIGHTWAY PLASTICS CO", "SHENZHEN CHINA", "CN", "SZHNCNBS"),
            ("KOWLOON BAY HOUSEWARES LIMITED", "KOWLOON HONG KONG", "HK", "KLNBHKHH")],
    "C05": [("GULF STAR SHIPPING LLC", "DUBAI UAE", "AE", "GLFSAEAD"),
            ("NHAVA SHEVA CONTAINER LINES PVT", "MUMBAI INDIA", "IN", "MMBIINBB")],
    "C06": [("COLOMBO PACKAGING SUPPLIES PVT", "COLOMBO SRI LANKA", "LK", "CMBOLKLX")],
    "C07": [("AALSMEER FLORAL SUPPLIES BV", "AALSMEER NETHERLANDS", "NL", "ALSMNL2A")],
    "C08": [("SHENZHEN NOVA MOBILE TECH CO", "SHENZHEN CHINA", "CN", "SZNVCNBS"),
            ("DEIRA ELECTRONICS TRADING LLC", "DUBAI UAE", "AE", "DEIRAEAD"),
            ("HANGZHOU LUMEN DISPLAY CO LTD", "HANGZHOU CHINA", "CN", "HGZHCNBH")],
    "C09": [("AHMEDABAD GENERICS LTD", "AHMEDABAD INDIA", "IN", "AHMDINBB"),
            ("HYDERABAD FORMULATIONS PVT LTD", "HYDERABAD INDIA", "IN", "HYDRINBB")],
    "C10": [("GOLDLINE ASSAY SERVICES DMCC", "DUBAI UAE", "AE", "GLDLAEAD")],
    "C12": [("TANGSHAN NORTH STEEL TRADING CO", "TANGSHAN CHINA", "CN", "TNGSCNBT"),
            ("ISKENDERUN REBAR SANAYI AS", "ISKENDERUN TURKEY", "TR", "ISKNTRIS")],
}
FCY_BUYERS = {
    "C01": REGIONAL_BUYERS[2:4] + REGIONAL_BUYERS[0:1],
    "C04": REGIONAL_BUYERS[0:2] + REGIONAL_BUYERS[2:3] + REGIONAL_BUYERS[4:5],
    "C05": [("BLUE OCEAN FORWARDING LLC", "DUBAI UAE", "AE", "BLOCAEAD"),
            ("MUMBAI PORTSIDE AGENCIES PVT", "MUMBAI INDIA", "IN", "PRTSINBB"),
            ("KAMPALA CARGO LINKS LTD", "KAMPALA UGANDA", "UG", "CGOLUGKA")],
    "C06": [("KARACHI TEA BLENDERS PVT LTD", "KARACHI PAKISTAN", "PK", "KRCHPKKA"),
            ("NILE VALLEY TEA PACKERS SAE", "ALEXANDRIA EGYPT", "EG", "ALXNEGCX"),
            ("THAMES ESTATE TEA MERCHANTS LTD", "LONDON UNITED KINGDOM", "GB", "THMSGB2L"),
            ("LAHORE CHAI DISTRIBUTORS", "LAHORE PAKISTAN", "PK", "LHRDPKKA")],
    "C07": [("FLORAHOLLAND CLOCK SETTLEMENTS BV", "AALSMEER NETHERLANDS", "NL", "FLRHNL2A"),
            ("BLUMEN GROSSHANDEL KOLN GMBH", "KOLN GERMANY", "DE", "KOLNDEFF")],
    "C08": REGIONAL_BUYERS[1:3] + REGIONAL_BUYERS[5:6],
    "C09": [],
    "C10": [("DESERT GOLD REFINERY DMCC", "DUBAI UAE", "AE", "DSGDAEAD"),
            ("AL MANARA BULLION TRADING LLC", "DUBAI UAE", "AE", "MNRAAEAD")],
    "C12": [("GULU NORTHERN SUPPLIES LTD", "GULU UGANDA", "UG", "GULUUGKA")],
}

# third-party receipt mix by channel (shares of the KES total), and the mean ticket per channel (KES)
MIX = {
    "C01": {"RTGS": 0.52, "EFT": 0.06, "CHQ": 0.07, "CASH": 0.05, "TT": 0.30},
    "C02": {"MPESA": 0.35, "CASH": 0.25, "RTGS": 0.30, "EFT": 0.10},
    "C03": {"RTGS": 0.88, "CHQ": 0.07, "EFT": 0.05},
    "C04": {"RTGS": 0.22, "PESALINK": 0.13, "CASH": 0.05, "TT": 0.60},
    "C05": {"RTGS": 0.55, "EFT": 0.20, "TT": 0.25},
    "C06": {"TT": 0.90, "RTGS": 0.10},
    "C07": {"TT": 0.95, "EFT": 0.05},
    "C08": {"MPESA": 0.30, "CASH": 0.20, "PESALINK": 0.20, "RTGS": 0.12, "TT": 0.18},
    "C09": {"RTGS": 0.62, "EFT": 0.28, "CHQ": 0.10},
    "C10": {"TT": 0.85, "RTGS": 0.15},
    "C11": {"POS": 0.45, "RTGS": 0.30, "MPESA": 0.17, "CASH": 0.08},
    "C12": {"MPESA": 0.25, "CASH": 0.25, "RTGS": 0.35, "EFT": 0.15},
}
TICKET = {"RTGS": 1_650_000, "EFT": 185_000, "PESALINK": 128_000, "CHQ": 410_000, "CASH": 118_000,
          "MPESA": 0, "POS": 0, "TT": 0}
TT_TICKET_USD = {"C01": 46_000, "C04": 118_000, "C05": 21_000, "C06": 172_000, "C07": 31_000, "C08": 38_000,
                 "C10": 205_000, "C12": 54_000}


TILLS = {"C02": [str(5_120_000 + 3_917 * k) for k in range(16)], "C08": [str(6_480_311 + 7_043 * k) for k in range(5)],
         "C11": [str(7_002_514 + 1_309 * k) for k in range(3)], "C12": [str(8_311_906 + 5_167 * k) for k in range(4)]}
POS_MIDS = {"C11": ["4110%06d" % (215_300 + 4_211 * k) for k in range(3)]}


def _season(code, d):
    m = d.month
    if code == "C06":
        return 1.35 if m in (11, 12, 1, 2, 3) else 0.7
    if code == "C07":
        return 1.9 if m == 2 else (1.2 if m in (3, 4, 5, 12) else 0.85)
    if code == "C11":
        return 1.45 if m in (12, 1, 2, 3, 7, 8) else 0.65
    return 1.0


def _spread_dates(rng, code, n, days):
    w = np.array([_season(code, d) for d in days], dtype=float)
    w /= w.sum()
    idx = rng.choice(len(days), size=n, replace=True, p=w)
    return sorted(days[i] for i in idx)


def _lognormal_amounts(rng, n, mean, sigma=0.55):
    mu = math.log(mean) - sigma * sigma / 2.0
    return rng.lognormal(mu, sigma, size=n)


def _cents(x):
    return round(float(x), 2)


def _kes_amount(x, step=1.0):
    """Realistic KES amount: most transfers are whole shillings, some carry cents."""
    return round(float(x) / step) * step


class World:
    def __init__(self):
        self.rng = np.random.default_rng([P.SEED, 0])
        self.days_all, self.rates = build_rates()
        self.year_days = [d for d in self.days_all if P.YEAR_START <= d <= P.YEAR_END]
        self.accts = build_accounts(np.random.default_rng([P.SEED, 2]))
        self.cust = {c["code"]: c for c in P.CUSTOMERS}
        self.postings = []
        self.swift_out, self.swift_in = [], []
        self.teller, self.kra, self.payroll = [], [], []
        self._ref = 0
        self._build()

    # helpers
    def acct(self, code, cur="KES", prod=None):
        for a in self.accts[code]:
            if a["cur"] == cur and (prod is None or a["prod"] == prod):
                return a
        raise KeyError((code, cur, prod))

    def ref(self, prefix):
        self._ref += 1
        return "%s%07d" % (prefix, self._ref * 37 % 9_999_991)

    def post(self, code, acct, d, amount, channel, kind, cpty="", cpty_acct="", narrative="", ref=None, **extra):
        rec = dict(code=code, cif=self.cust[code]["cif"], acct=acct, cur=acct["cur"], value_date=d,
                   amount=_cents(amount), channel=channel, kind=kind, cpty=cpty, cpty_acct=cpty_acct,
                   narrative=narrative, ref=ref or self.ref(channel[:2]))
        rec.update(extra)
        self.postings.append(rec)
        return rec

    def kes(self, cur, amount, d):
        return amount * rate_on(self.rates, cur, d)

    # ------------------------------------------------------------ build
    def _build(self):
        for i, c in enumerate(P.CUSTOMERS):
            self._receipts(i, c)
            self._sweeps(i, c)
            self._declared_elsewhere(i, c)
            self._fx_conversions(i, c)
            self._outgoing(i, c)
        self._uturns()
        self._returns()
        self._cash_withdrawals()
        self._kra()
        self._payroll()
        self._charges()
        self._decollide()
        self.postings.sort(key=lambda r: (r["value_date"], r["cif"], r["acct"]["new"], r["ref"]))

    def _decollide(self):
        """No inward credit other than a genuine return may sit within USD 1,500 below an outward payment of the
        same customer in the 25 business days before it, so every pairing window and tolerance a reader might use
        finds the same pairs (determinism-check: a match by amount and time has one reading)."""
        outs = {}
        for m in self.swift_out:
            outs.setdefault((m["posting"]["code"], m["cur"]), []).append(m)
        for m in self.swift_in:
            if m["posting"]["kind"] in ("uturn_return", "return"):
                continue
            key = (m["posting"]["code"], m["cur"])
            for _ in range(50):
                hit = False
                for o in outs.get(key, []):
                    lag = (m["value_date"] - o["value_date"]).days
                    if 0 <= lag <= 40 and 0 <= o["amount"] - m["amount"] <= 1500.0:
                        hit = True
                        break
                if not hit:
                    break
                bump = round(m["amount"] * 0.0137 + 1733.0, 2)
                m["amount"] = round(m["amount"] + bump, 2)
                m["instructed"] = round(m["instructed"] + bump, 2)
                m["posting"]["amount"] = m["amount"]

    def _receipts(self, i, c):
        code = c["code"]
        total = c["tp"] * 1_000_000.0
        for j, (ch, share) in enumerate(sorted(MIX[code].items())):
            rng = np.random.default_rng([P.SEED, 10, i, j])
            amt_total = total * share * float(rng.uniform(0.975, 1.025))
            if ch in ("MPESA", "POS"):
                days = [d for d in self.year_days]
                tills = TILLS[code] if ch == "MPESA" else POS_MIDS[code]
                tw = rng.lognormal(0, 0.45, size=len(tills))
                tw = tw / tw.sum()
                for t_i, till in enumerate(tills):
                    w = np.array([_season(code, d) * (1.3 if d.weekday() == 0 else 1.0) for d in days])
                    vals = w / w.sum() * amt_total * tw[t_i] * rng.lognormal(0, 0.22, size=len(days))
                    keep = rng.random(len(days)) > (0.04 if ch == "MPESA" else 0.02)
                    for d, v, k in zip(days, vals, keep):
                        if not k:
                            continue
                        if ch == "MPESA":
                            self.post(code, self.acct(code, "KES", "CL" if c["collection"] else "CA"), d,
                                      _kes_amount(v), "MPESA", "tp", cpty="SAFARICOM PLC",
                                      narrative="MPESA C2B SETTLEMENT TILL %s" % till)
                        else:
                            self.post(code, self.acct(code, "KES", "CL" if c["collection"] else "CA"), d,
                                      _kes_amount(v, 0.01), "POS", "tp", cpty="TAWI MERCHANT SERVICES",
                                      narrative="POS SETTLEMENT MID %s" % till)
                continue
            if ch == "TT":
                cur = c["fcy"][0]
                usd_ticket = TT_TICKET_USD[code]
                fx_avg = P.FX_START[cur]
                n = max(8, int(round(amt_total / (usd_ticket * fx_avg))))
                vals = _lognormal_amounts(rng, n, usd_ticket, 0.6)
                dates = _spread_dates(rng, code, n, self.year_days)
                # scale so the KES value hits the share
                kes_val = sum(v * rate_on(self.rates, cur, d) for v, d in zip(vals, dates))
                vals = vals * (amt_total / kes_val)
                buyers = FCY_BUYERS[code]
                for k, (v, d) in enumerate(zip(vals, dates)):
                    b = buyers[int(rng.integers(0, len(buyers)))]
                    amt = round(float(v), 2) if rng.random() < 0.7 else round(float(v), -1)
                    self._inward_tt(code, cur, d, amt, b, kind="tp", rng=rng)
                continue
            n = max(6, int(round(amt_total / TICKET[ch])))
            vals = _lognormal_amounts(rng, n, TICKET[ch], 0.7 if ch != "CASH" else 0.5)
            vals = vals * (amt_total / vals.sum())
            dates = _spread_dates(rng, code, n, self.year_days)
            for v, d in zip(vals, dates):
                firm = LOCAL_FIRMS[int(rng.integers(0, len(LOCAL_FIRMS)))]
                if ch == "CASH":
                    if d.weekday() == 4 and rng.random() < 0.3 and d + DAY <= P.YEAR_END:
                        d = d + DAY
                    rec = self.post(code, self.acct(code, "KES", "CL" if c["collection"] else "CA"), d,
                                    _kes_amount(v, 50), "CASH", "tp", narrative="CASH DEPOSIT")
                    self.teller.append(dict(kind="DEP", posting=rec))
                elif ch == "CHQ":
                    self.post(code, self.acct(code), add_business(d, 2) if add_business(d, 2) <= P.YEAR_END else d,
                              _kes_amount(v), "CHQ", "tp", cpty=firm,
                              narrative="CHQ DEP %06d %s" % (int(rng.integers(100000, 999999)), firm.upper()[:22]))
                else:
                    self.post(code, self.acct(code), d, _kes_amount(v, 1 if ch != "RTGS" else 1), ch, "tp", cpty=firm,
                              cpty_acct="%010d" % int(rng.integers(10**9, 10**10 - 1)),
                              narrative="%s FROM %s" % (ch, firm.upper()[:28]))

    def _inward_tt(self, code, cur, d, amt, remitter, kind, rng, instructed=None, charges=None, uturn=None):
        name, city, ctry, bic = remitter[0], remitter[-3] if len(remitter) == 5 else remitter[1], \
            remitter[-2], remitter[-1]
        addr = remitter[1] if len(remitter) == 5 else ""
        if charges is None:
            charges = float(rng.choice([0.0, 0.0, 15.0, 20.0, 25.0, 30.0]))
        if instructed is None:
            instructed = round(amt + charges, 2)
        sref = "%s%s%04d" % (name.replace(" ", "")[:4], d.strftime("%y%m%d"), int(rng.integers(1, 9999)))
        rec = self.post(code, self.acct(code, cur), d, amt, "TT_IN", kind, cpty=name,
                        narrative="INWARD TT %s REF %s" % (name[:24], sref), ref=sref)
        msg = dict(direction="IN", posting=rec, ref=sref, value_date=d, cur=cur, amount=amt, instructed=instructed,
                   charges=charges, ordering=name, ordering_addr=addr, ordering_city=city, ordering_ctry=ctry,
                   ordering_bic=bic, ordering_acct="%s%02d%s" % (ctry, int(rng.integers(10, 99)),
                                                                  "".join(str(int(x)) for x in rng.integers(0, 10, 16))),
                   uturn=uturn)
        self.swift_in.append(msg)
        return rec

    def _outward_tt(self, code, cur, d, amt, bene, kind, rng, purpose="GOODS", uturn=None):
        name = bene[0]
        city = bene[-3] if len(bene) == 5 else bene[1]
        addr = bene[1] if len(bene) == 5 else ""
        ctry, bic = bene[-2], bene[-1]
        sref = "TW%s%05d" % (d.strftime("%y%m%d"), int(rng.integers(1, 99999)))
        rec = self.post(code, self.acct(code, cur), d, -amt, "TT_OUT", kind, cpty=name,
                        narrative="OUTWARD TT %s REF %s" % (name[:24], sref), ref=sref)
        inv = "%s-%s-%03d" % ("".join(w[0] for w in name.split()[:2]), d.strftime("%y%m"), int(rng.integers(1, 999)))
        msg = dict(direction="OUT", posting=rec, ref=sref, value_date=d, cur=cur, amount=amt, beneficiary=name,
                   bene_addr=addr, bene_city=city, bene_ctry=ctry, bene_bic=bic,
                   bene_acct="%03d-%06d-%03d" % (int(rng.integers(100, 999)), int(rng.integers(0, 999999)),
                                                  int(rng.integers(1, 999))),
                   remittance="/INV/%s %s" % (inv, purpose), uturn=uturn)
        self.swift_out.append(msg)
        return rec

    def _sweeps(self, i, c):
        code = c["code"]
        if code not in P.SWEEPS:
            return
        rng = np.random.default_rng([P.SEED, 20, i])
        total = P.SWEEPS[code] * 1_000_000.0
        days = self.year_days
        n = len(days) if code == "C02" else 52
        sel = days if n == len(days) else _spread_dates(rng, code, n, days)
        vals = rng.lognormal(0, 0.25, size=len(sel))
        vals = vals * (total / vals.sum())
        cl, ca = self.acct(code, "KES", "CL"), self.acct(code, "KES", "CA")
        for d, v in zip(sel, vals):
            amt = _kes_amount(v, 1000)
            r = self.ref("SW")
            self.post(code, cl, d, -amt, "SWEEP", "own_internal_dr", cpty=c["name"], cpty_acct=ca["new"],
                      narrative="SWEEP TO %s" % ca["new"], ref=r)
            self.post(code, ca, d, amt, "SWEEP", "own_internal", cpty=c["name"], cpty_acct=cl["new"],
                      narrative="SWEEP FROM %s" % cl["new"], ref=r)

    def _declared_elsewhere(self, i, c):
        code = c["code"]
        if code not in P.DECLARED_ELSEWHERE:
            return
        info = P.DECLARED_ELSEWHERE[code]
        rng = np.random.default_rng([P.SEED, 30, i])
        total = info["flow"] * 1_000_000.0
        if code == "C03":
            days = [d for d in self.year_days if d >= dt.date(2026, 2, 9)]
            n = 92
        else:
            days = self.year_days
            n = 6
        dates = _spread_dates(rng, code, n, days)
        vals = rng.lognormal(0, 0.45, size=n)
        vals = vals * (total / vals.sum())
        for d, v in zip(dates, vals):
            self.post(code, self.acct(code), d, _kes_amount(v, 1000), "RTGS", "own_external",
                      cpty=c["name"].upper(), cpty_acct=info["acct"],
                      narrative="RTGS A/C %s %s %s" % (info["acct"], info["bank"].split()[0].upper(),
                                                         c["legacy_name"][:22]))

    def _fx_conversions(self, i, c):
        """The customer's own currency conversions: a foreign currency account sold to its shilling account."""
        code = c["code"]
        if not c["fcy"] or code == "C04":
            return
        cur = c["fcy"][0]
        rng = np.random.default_rng([P.SEED, 40, i])
        n = 26 if code not in ("C06", "C10") else 48
        dates = _spread_dates(rng, code, n, self.year_days)
        share = {"C01": 0.28, "C05": 0.22, "C06": 0.55, "C07": 0.85, "C08": 0.16, "C09": 0.0, "C10": 0.45,
                 "C12": 0.05}[code]
        total_fcy = c["tp"] * 1_000_000.0 * MIX[code].get("TT", 0) * share / P.FX_START[cur]
        if total_fcy <= 0:
            return
        vals = rng.lognormal(0, 0.4, size=n)
        vals = vals * (total_fcy / vals.sum())
        fa, ka = self.acct(code, cur), self.acct(code)
        for d, v in zip(dates, vals):
            amt = round(float(v), -2)
            rate = round(rate_on(self.rates, cur, d) - P.FX_SPREAD[cur], 4)
            r = self.ref("FX")
            self.post(code, fa, d, -amt, "FX", "own_internal_dr", cpty=c["name"], cpty_acct=ka["new"],
                      narrative="FX DEAL SELL %s %s @%.4f" % (cur, "{:,.2f}".format(amt), rate), ref=r)
            self.post(code, ka, d, _cents(amt * rate), "FX", "own_internal", cpty=c["name"], cpty_acct=fa["new"],
                      narrative="FX DEAL BUY KES AGAINST %s %s" % (cur, "{:,.2f}".format(amt)), ref=r)

    def _outgoing(self, i, c):
        """Supplier payments (local and foreign) and sundry debits; they are not third-party receipts."""
        code = c["code"]
        rng = np.random.default_rng([P.SEED, 50, i])
        tp = c["tp"] * 1_000_000.0
        # local supplier payments
        n = int(tp / 1_150_000) + 90
        vals = _lognormal_amounts(rng, n, tp * 0.55 / n, 0.8)
        dates = _spread_dates(rng, code, n, self.year_days)
        for v, d in zip(vals, dates):
            firm = LOCAL_FIRMS[int(rng.integers(0, len(LOCAL_FIRMS)))]
            ch = "RTGS" if v > 1_000_000 else ("EFT" if rng.random() < 0.6 else "PESALINK")
            rec = self.post(code, self.acct(code), d, -_kes_amount(v), ch, "debit", cpty=firm,
                            cpty_acct="%010d" % int(rng.integers(10**9, 10**10 - 1)),
                            narrative="%s TO %s" % (ch, firm.upper()[:28]))
            fee = {"RTGS": 750.0, "EFT": 200.0, "PESALINK": 120.0}[ch]
            self.post(code, self.acct(code), d, -fee, "CHG", "debit", narrative="%s CHARGE %s" % (ch, rec["ref"]))
            self.post(code, self.acct(code), d, -round(fee * 0.2, 2), "CHG", "debit",
                      narrative="EXCISE DUTY ON %s CHARGE %s" % (ch, rec["ref"]))
        # foreign supplier payments
        if code in SUPPLIERS_FCY and c["fcy"]:
            cur = c["fcy"][0]
            sup = SUPPLIERS_FCY[code]
            n = {"C01": 70, "C04": 64, "C05": 40, "C06": 8, "C07": 10, "C08": 58, "C09": 46, "C10": 6, "C12": 30}[code]
            mean_usd = {"C01": 61_000, "C04": 54_000, "C05": 18_000, "C06": 22_000, "C07": 12_000, "C08": 41_000,
                        "C09": 52_000, "C10": 9_000, "C12": 68_000}[code]
            vals = _lognormal_amounts(rng, n, mean_usd, 0.6)
            dates = _spread_dates(rng, code, n, self.year_days)
            for v, d in zip(vals, dates):
                b = sup[int(rng.integers(0, len(sup)))]
                self._outward_tt(code, cur, d, round(float(v), 2), b, "debit", rng)

    def _uturns(self):
        """C04's own dollars sent out to one company and credited back from another a few days later."""
        code = "C04"
        rng = np.random.default_rng([P.SEED, 60])
        days = [d for d in self.year_days if dt.date(2025, 10, 20) <= d <= dt.date(2026, 9, 14)]
        starts = sorted(days[int(k)] for k in np.linspace(0, len(days) - 1, P.UTURN_CYCLES).round().astype(int))
        jitter = rng.integers(-3, 4, size=len(starts))
        starts = [days[min(max(days.index(s) + int(j), 0), len(days) - 1)] for s, j in zip(starts, jitter)]
        self.uturn_pairs = []
        for k, d in enumerate(starts):
            out_amt = round(float(rng.uniform(*P.UTURN_OUT_RANGE)), 2)
            bene = P.UTURN_BENEFICIARIES[int(rng.integers(0, len(P.UTURN_BENEFICIARIES)))]
            rem = P.UTURN_REMITTERS[int(rng.integers(0, len(P.UTURN_REMITTERS)))]
            lag = int(rng.integers(2, 7))
            leg1 = float(rng.choice([15.0, 18.0, 20.0, 22.0, 25.0, 28.0, 30.0]))
            leg2 = float(rng.choice([18.0, 20.0, 22.0, 25.0, 28.0, 32.0, 35.0, 38.0]))
            ret_d = add_business(d, lag)
            instructed = round(out_amt - leg1, 2)
            credited = round(instructed - leg2, 2)
            o = self._outward_tt(code, "USD", d, out_amt, bene, "uturn_out", rng, purpose="GENERAL MERCHANDISE",
                                 uturn=k)
            r = self._inward_tt(code, "USD", ret_d, credited, rem, "uturn_return", rng, instructed=instructed,
                                charges=leg2, uturn=k)
            self.uturn_pairs.append((o, r))
        # funding of the first cycle from its own shilling account
        d0 = add_business(starts[0], -1) if False else days[0]
        fa, ka = self.acct(code, "USD"), self.acct(code)
        rate = round(rate_on(self.rates, "USD", d0) + P.FX_SPREAD["USD"], 4)
        amt = 520_000.00
        ref = self.ref("FX")
        self.post(code, ka, d0, -_cents(amt * rate), "FX", "own_internal_dr", cpty=self.cust[code]["name"],
                  cpty_acct=fa["new"], narrative="FX DEAL BUY USD %s @%.4f" % ("{:,.2f}".format(amt), rate), ref=ref)
        self.post(code, fa, d0, amt, "FX", "own_internal", cpty=self.cust[code]["name"], cpty_acct=ka["new"],
                  narrative="FX DEAL SELL KES FOR USD %s" % "{:,.2f}".format(amt), ref=ref)
        # dollars bought from its shilling account to pay its suppliers in China
        dates = _spread_dates(rng, code, 16, self.year_days)
        vals = rng.lognormal(0, 0.3, size=16)
        vals = vals * (2_050_000.0 / vals.sum())
        for d, v in zip(dates, vals):
            a = round(float(v), -2)
            rate = round(rate_on(self.rates, "USD", d) + P.FX_SPREAD["USD"], 4)
            r = self.ref("FX")
            self.post(code, ka, d, -_cents(a * rate), "FX", "own_internal_dr", cpty=self.cust[code]["name"],
                      cpty_acct=fa["new"], narrative="FX DEAL BUY USD %s @%.4f" % ("{:,.2f}".format(a), rate), ref=r)
            self.post(code, fa, d, a, "FX", "own_internal", cpty=self.cust[code]["name"], cpty_acct=ka["new"],
                      narrative="FX DEAL SELL KES FOR USD %s" % "{:,.2f}".format(a), ref=r)
        # its regional dollar receipts are sold to its shilling account from time to time
        tt_total = sum(p["amount"] for p in self.postings if p["code"] == code and p["kind"] == "tp" and
                       p["cur"] == "USD")
        dates = _spread_dates(rng, code, 18, self.year_days)
        vals = rng.lognormal(0, 0.35, size=18)
        vals = vals * (tt_total * 0.9 / vals.sum())
        for d, v in zip(dates, vals):
            a = round(float(v), -2)
            rate = round(rate_on(self.rates, "USD", d) - P.FX_SPREAD["USD"], 4)
            r = self.ref("FX")
            self.post(code, fa, d, -a, "FX", "own_internal_dr", cpty=self.cust[code]["name"], cpty_acct=ka["new"],
                      narrative="FX DEAL SELL USD %s @%.4f" % ("{:,.2f}".format(a), rate), ref=r)
            self.post(code, ka, d, _cents(a * rate), "FX", "own_internal", cpty=self.cust[code]["name"],
                      cpty_acct=fa["new"], narrative="FX DEAL BUY KES AGAINST USD %s" % "{:,.2f}".format(a), ref=r)

    def _returns(self):
        """Payments of a customer's own that come back to it: a rejected wire and a supplier's refunds."""
        rng = np.random.default_rng([P.SEED, 70])
        # C08: one outward wire rejected by the beneficiary bank, returned less charges
        outs = [m for m in self.swift_out if m["posting"]["code"] == "C08"]
        m = outs[len(outs) // 3]
        ret_d = add_business(m["value_date"], 6)
        amt = round(m["amount"] - 35.0, 2)
        rec = self._inward_tt("C08", "USD", ret_d, amt, (m["beneficiary"], m["bene_addr"], m["bene_city"],
                                                          m["bene_ctry"], m["bene_bic"]), "return", rng,
                              instructed=round(m["amount"] - 15.0, 2), charges=20.0)
        msg = self.swift_in[-1]
        msg["return_of"] = m["ref"]
        rec["narrative"] = "RETURN OF FUNDS YR REF %s ACCOUNT CLOSED" % m["ref"]
        # C12: two refunds from a local steel supplier for short deliveries
        c12_pay = [p for p in self.postings if p["code"] == "C12" and p["kind"] == "debit" and
                   p["channel"] in ("RTGS", "EFT") and p["amount"] < -900_000]
        for p in (c12_pay[5], c12_pay[17]):
            d = add_business(p["value_date"], int(rng.integers(12, 30)))
            if d > P.YEAR_END:
                d = add_business(p["value_date"], 5)
            amt = _kes_amount(-p["amount"] * float(rng.uniform(0.18, 0.42)))
            self.post("C12", self.acct("C12"), d, amt, "EFT", "return", cpty=p["cpty"], cpty_acct=p["cpty_acct"],
                      narrative="EFT FROM %s REFUND SHORT DELIVERY" % p["cpty"].upper()[:22])
        # C09: an EFT to a pharmacy returned unapplied (account details wrong)
        c09_pay = [p for p in self.postings if p["code"] == "C09" and p["kind"] == "debit" and p["channel"] == "EFT"]
        p = c09_pay[11]
        self.post("C09", self.acct("C09"), add_business(p["value_date"], 1), -p["amount"], "EFT", "return",
                  cpty=p["cpty"], cpty_acct=p["cpty_acct"], narrative="EFT RETURN %s INVALID ACCOUNT" % p["ref"])

    def _cash_withdrawals(self):
        """Teller withdrawals; several customers withdraw near the reporting line, some split across branches."""
        rng = np.random.default_rng([P.SEED, 80])
        branches = ["101", "106", "118", "131", "214", "322", "337", "351", "142", "209"]
        plan = {"C02": 160, "C03": 120, "C04": 40, "C05": 30, "C08": 70, "C10": 150, "C11": 60, "C12": 110, "C01": 25,
                "C06": 24, "C07": 30, "C09": 12}
        for code, n in plan.items():
            c = self.cust[code]
            accs = [a for a in self.accts[code] if a["cur"] == "KES"]
            dates = _spread_dates(np.random.default_rng([P.SEED, 81, int(code[1:])]), code, n,
                                  [d for d in self.year_days])
            for d in dates:
                if d.weekday() == 4 and rng.random() < 0.35 and d + DAY <= P.YEAR_END and d + DAY not in P.HOLIDAYS:
                    d = d + DAY                                         # Saturday morning banking hall
                thr = P.CASH_THRESHOLD_USD * rate_on(self.rates, "USD", d)
                u = rng.random()
                if u < 0.45:
                    amt = float(rng.uniform(0.15, 0.9)) * thr
                elif u < 0.70:
                    amt = thr * float(rng.uniform(0.985, 1.012))       # near the line
                elif u < 0.85:
                    amt = thr * float(rng.uniform(1.05, 3.5))
                else:
                    # split the same day across two branches / two accounts
                    a1 = thr * float(rng.uniform(0.45, 0.8))
                    a2 = thr * float(rng.uniform(0.35, 0.7))
                    for k, a in enumerate((a1, a2)):
                        acc = accs[k % len(accs)]
                        br = c["branch"][2] if k == 0 else int(branches[int(rng.integers(0, len(branches)))])
                        rec = self.post(code, acc, d, -_kes_amount(a, 100), "CASH", "debit", narrative="CASH WITHDRAWAL")
                        self.teller.append(dict(kind="WDL", posting=rec, branch=br))
                    continue
                acc = accs[0]
                rec = self.post(code, acc, d, -_kes_amount(amt, 100), "CASH", "debit", narrative="CASH WITHDRAWAL")
                self.teller.append(dict(kind="WDL", posting=rec, branch=c["branch"][2]))
        # teller errors reversed the same day
        wd = [t for t in self.teller if t["kind"] == "WDL"]
        for t in wd[7::53]:
            p = t["posting"]
            rec = self.post(p["code"], p["acct"], p["value_date"], -p["amount"], "CASH", "reversal",
                            narrative="REV CASH WITHDRAWAL %s" % p["ref"])
            self.teller.append(dict(kind="REV", posting=rec, branch=t.get("branch"), reverses=p["ref"]))
        for t in self.teller:
            if "branch" not in t:
                t["branch"] = self.cust[t["posting"]["code"]]["branch"][2]

    def _kra(self):
        """Tax payments through the KRA gateway (VAT, PAYE, instalment tax), by tax period."""
        rng = np.random.default_rng([P.SEED, 90])
        months = []
        y, m = 2025, 8
        while (y, m) <= (2026, 9):
            months.append((y, m))
            m += 1
            if m == 13:
                y, m = y + 1, 1
        for i, c in enumerate(P.CUSTOMERS):
            code = c["code"]
            vat_base = c["tp"] * 1_000_000.0 * {"C06": 0.004, "C07": 0.005, "C10": 0.01}.get(code, 0.032) / 12
            paye_base = c["tp"] * 1_000_000.0 * 0.006 / 12
            for (y, m) in months:
                nm = (y + (m == 12), 1 if m == 12 else m + 1)
                due = dt.date(nm[0], nm[1], 20)
                for head, base in (("VAT", vat_base), ("PAYE", paye_base)):
                    amount = _kes_amount(base * float(rng.lognormal(0, 0.22)), 1)
                    late = rng.random() < (0.12 if head == "VAT" else 0.05)
                    pay = due - dt.timedelta(days=int(rng.integers(0, 6)))
                    if late:
                        pay = due + dt.timedelta(days=int(rng.integers(3, 16)))
                    while not is_business(pay):
                        pay -= DAY
                    if pay > P.LOG_END or pay < P.LOG_START:
                        continue
                    split = head == "VAT" and rng.random() < 0.10
                    prn = "%04d%02d%010d" % (pay.year, pay.month, int(rng.integers(10**9, 10**10 - 1)))
                    parts = [amount] if not split else [_kes_amount(amount * 0.6), amount - _kes_amount(amount * 0.6)]
                    for k, part in enumerate(parts):
                        pd_ = pay if k == 0 else add_business(pay, int(rng.integers(1, 4)))
                        rec = None
                        if P.YEAR_START <= pd_ <= P.YEAR_END:
                            rec = self.post(code, self.acct(code), pd_, -part, "KRA", "debit", cpty="KENYA REVENUE AUTHORITY",
                                            narrative="KRA PAYMENT PRN %s" % prn)
                        self.kra.append(dict(code=code, pin=c["kra"], prn=prn, head=head, period=(y, m),
                                             amount=part, pay_date=pd_, posting=rec, part=k + 1, parts=len(parts)))

    def _payroll(self):
        """Monthly salary batches (and weekly casual batches) through the bulk upload service."""
        rng = np.random.default_rng([P.SEED, 95])
        from faker import Faker
        fk = Faker("en_KE")
        fk.seed_instance(P.SEED % 100000)
        staff = {"C01": 46, "C02": 138, "C03": 212, "C04": 19, "C05": 64, "C06": 410, "C07": 520, "C08": 37,
                 "C09": 71, "C10": 14, "C11": 186, "C12": 52}
        self.staff = {}
        for i, c in enumerate(P.CUSTOMERS):
            code = c["code"]
            people = []
            for k in range(staff[code] + 12):
                nid = "%08d" % int(rng.integers(20_000_000, 39_999_999))
                people.append(dict(nid=nid, name=fk.name().upper(), net=round(float(rng.lognormal(math.log(48000), 0.55)), -1)))
            self.staff[code] = people
            for (y, m) in ((2026, 7), (2026, 8), (2026, 9)):
                active = people[:staff[code]] if m < 9 else people[3:staff[code] + 3]
                pay = dt.date(y, m, 28)
                while not is_business(pay):
                    pay -= DAY
                late_sep = (m == 9 and code in ("C03", "C07", "C11"))
                if late_sep:
                    pay = dt.date(2026, 10, 2)
                batch = "SAL-%s-%02d%02d-%03d" % (c["cif"][-4:], y % 100, m, int(rng.integers(1, 999)))
                total = 0.0
                rows = []
                for prs in active:
                    amt = prs["net"]
                    rows.append(dict(code=code, batch=batch, nid=prs["nid"], name=prs["name"], amount=amt,
                                     narrative="SALARY %s %d" % (dt.date(y, m, 1).strftime("%b").upper(), y),
                                     pay_date=pay, month=(y, m), kind="salary"))
                    total += amt
                # a supplementary batch for people left out of the main run
                if m == 9 and code in ("C02", "C06", "C09", "C12"):
                    extra = people[staff[code] + 3: staff[code] + 6]
                    sb = batch[:-3] + "%03d" % int(rng.integers(1, 999))
                    for prs in extra + active[:1]:
                        rows.append(dict(code=code, batch=sb, nid=prs["nid"], name=prs["name"] if prs is not active[0]
                                         else prs["name"].split()[0] + " " + prs["name"].split()[-1],
                                         amount=prs["net"] if prs is not active[0] else round(prs["net"] * 0.25, -1),
                                         narrative="SALARY SEP 2026" if prs is not active[0] else "SALARY SEP 2026 BALANCE",
                                         pay_date=add_business(pay, 2) if not late_sep else pay, month=(y, m),
                                         kind="salary"))
                # arrears for the previous month paid in September
                if m == 9 and code in ("C05", "C08", "C11"):
                    ab = batch[:-3] + "%03d" % int(rng.integers(1, 999))
                    for prs in people[staff[code]: staff[code] + 4]:
                        rows.append(dict(code=code, batch=ab, nid=prs["nid"], name=prs["name"],
                                         amount=round(prs["net"] * 0.5, -1), narrative="ARREARS AUG 2026",
                                         pay_date=dt.date(2026, 9, 15), month=(2026, 8), kind="arrears"))
                self.payroll.extend(rows)
            # weekly casual wages (construction, flowers, tea)
            if code in ("C03", "C06", "C07"):
                for wk in range(27, 40):
                    d = dt.date.fromisocalendar(2026, wk, 5)
                    if d > P.LOG_END:
                        continue
                    cb = "CAS-%s-W%02d" % (c["cif"][-4:], wk)
                    for k in range(int(rng.integers(18, 40))):
                        nid = "%08d" % int(rng.integers(20_000_000, 39_999_999))
                        self.payroll.append(dict(code=code, batch=cb, nid=nid, name=fk.name().upper(),
                                                 amount=round(float(rng.uniform(2800, 5200)), -1),
                                                 narrative="CASUALS WK%02d" % wk, pay_date=d, month=(2026, d.month),
                                                 kind="casual"))
        # post one debit per batch that falls inside the statements' window
        batches = {}
        for r in self.payroll:
            batches.setdefault((r["code"], r["batch"]), []).append(r)
        for (code, b), rows in sorted(batches.items()):
            d = rows[0]["pay_date"]
            if P.YEAR_START <= d <= P.YEAR_END:
                total = sum(r["amount"] for r in rows)
                self.post(code, self.acct(code), d, -total, "BULK", "debit", narrative="BULK PAYMENT %s" % b, ref=b)

    def _charges(self):
        """Bank charges with excise duty, one pair a month per account plus a charge per outward wire."""
        for c in P.CUSTOMERS:
            code = c["code"]
            for a in self.accts[code]:
                for (y, m) in [(2025, 10), (2025, 11), (2025, 12)] + [(2026, k) for k in range(1, 10)]:
                    d = dt.date(y, m, 28)
                    while not is_business(d):
                        d -= DAY
                    fee = 1500.0 if a["cur"] == "KES" else 15.0
                    self.post(code, a, d, -fee, "CHG", "debit", narrative="MONTHLY LEDGER FEE")
                    self.post(code, a, d, -round(fee * 0.2, 2), "CHG", "debit", narrative="EXCISE DUTY ON FEES")
        for m in self.swift_out:
            p = m["posting"]
            ka = self.acct(p["code"])
            fee_kes = round(2500.0 + 0.001 * m["amount"] * rate_on(self.rates, m["cur"], m["value_date"]), 2)
            fee_kes = min(fee_kes, 12000.0)
            self.post(p["code"], ka, m["value_date"], -fee_kes, "CHG", "debit", narrative="SWIFT CHARGE %s" % m["ref"])
            self.post(p["code"], ka, m["value_date"], -round(fee_kes * 0.2, 2), "CHG", "debit",
                      narrative="EXCISE DUTY ON SWIFT CHARGE %s" % m["ref"])


def kes_value(world, rec):
    return rec["amount"] * rate_on(world.rates, rec["cur"], rec["value_date"])
