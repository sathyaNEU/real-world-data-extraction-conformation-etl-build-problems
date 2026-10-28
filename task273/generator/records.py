"""task273 architecture 4: the pack's data files, each in the form the system that keeps it exports."""
from __future__ import annotations

import csv
from datetime import date, timedelta

import numpy as np

import params as P

TRANSCRIPT = {  # gene: (current, the 2019 pipeline's)
    "CFTR": ("NM_000492.4", "NM_000492.3"), "PAH": ("NM_000277.3", "NM_000277.2"),
    "GJB2": ("NM_004004.6", "NM_004004.5"), "ACADM": ("NM_000016.6", "NM_000016.5"),
    "DHCR7": ("NM_001360.3", "NM_001360.2"), "GALT": ("NM_000155.4", "NM_000155.3"),
    "ATP7B": ("NM_000053.4", "NM_000053.3"), "PKHD1": ("NM_138694.4", "NM_138694.3"),
    "MMUT": ("NM_000255.4", "NM_000255.3"), "GAA": ("NM_000152.5", "NM_000152.4"),
    "USH2A": ("NM_206933.4", "NM_206933.3"), "SACS": ("NM_014363.6", "NM_014363.5"),
    "TMEM216": ("NM_001173990.3", "NM_001173990.2"), "SLC26A2": ("NM_000112.4", "NM_000112.3"),
    "HEXA": ("NM_000520.6", "NM_000520.5"), "ASPA": ("NM_000049.4", "NM_000049.3"),
    "FANCC": ("NM_000136.3", "NM_000136.2"), "SMPD1": ("NM_000543.5", "NM_000543.4"),
    "NPC1": ("NM_000271.5", "NM_000271.4"), "PEX1": ("NM_000466.3", "NM_000466.2"),
    "G6PC1": ("NM_000151.4", "NM_000151.3"), "IDUA": ("NM_000203.5", "NM_000203.4"),
    "ARSA": ("NM_000487.6", "NM_000487.5"), "NPHS1": ("NM_004646.4", "NM_004646.3"),
    "AGA": ("NM_000027.4", "NM_000027.3"), "BLM": ("NM_000057.4", "NM_000057.3"),
    "ELP1": ("NM_003640.5", "NM_003640.4"), "MCOLN1": ("NM_020533.3", "NM_020533.2"),
    "BCKDHB": ("NM_183050.4", "NM_183050.3"), "PMM2": ("NM_000303.3", "NM_000303.2")}


def write_csv(path, head, rows, delim=","):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, delimiter=delim, lineterminator="\n")
        wr.writerow(head)
        wr.writerows(rows)


def d(x):
    return "" if x is None else x.isoformat()


class Records:
    def __init__(self, w):
        self.w = w
        self.rng = np.random.default_rng(np.random.SeedSequence(w.seed + 901))

    # -------------------------------------------------------------------------------------- the Study
    def members(self):
        w = self.w
        head = ["study_id", "phase", "recruitment_area", "enrolled_on", "sex", "birth_year", "sample_id",
                "sequenced_on", "genotype_status", "consent_status", "consent_status_date"]
        rows = []
        for i in np.argsort(w.study_id):
            status = "Withheld after QC" if w.qc_fail[i] else "Released"
            wd = w.withdraw_date[i]
            rows.append([w.study_id[i], int(w.phase[i]), w.area[i], d(w.enrolled[i]), w.sex[i], int(w.birth_year[i]),
                         w.sample_id[i], d(w.sequenced[i]), status,
                         "Withdrawn" if wd is not None else "Active", d(wd) if wd is not None else d(w.enrolled[i])])
        return head, rows

    def depth(self):
        w = self.w
        sites = [s["site_id"] for s in w.study_sites]
        head = ["sample_id"] + sites
        rows = []
        for i in np.argsort(w.sample_id):
            if w.qc_fail[i]:
                continue
            rows.append([w.sample_id[i]] + [int(w.depth[s][i]) for s in sites])
        return head, rows

    def calls(self, phase):
        w = self.w
        head = ["sample_id", "chrom", "pos", "ref", "alt", "gene", "transcript", "hgvs_c", "genotype", "ad", "dp",
                "gq", "filter"]
        rows = []
        for s in w.study_sites:
            sid = s["site_id"]
            idx = np.where(w.called[sid] & (w.phase == phase))[0]
            for i in idx:
                dp = int(w.depth[sid][i])
                alt = int(w.alt_reads[sid][i])
                gq = int(min(99, 20 + 4 * alt + int(self.rng.integers(0, 9))))
                if phase == 1:
                    pos, name, tx = s["pos37"], s["legacy"], TRANSCRIPT[s["gene"]][1]
                else:
                    pos, name, tx = s["pos38"], s["c"], TRANSCRIPT[s["gene"]][0]
                rows.append([w.sample_id[i], "chr" + s["chrom"] if phase == 2 else s["chrom"], pos, s["ref"], s["alt"],
                             s["gene"], tx, name, "0/1", "%d,%d" % (dp - alt, alt), dp, gq, "PASS"])
        rows.sort(key=lambda r: (r[0], r[1], r[2]))
        return head, rows

    # -------------------------------------------------------------------------------------- the register
    def register_rows(self):
        w = self.w
        reg = []
        for s in w.sites:
            cur, leg = TRANSCRIPT[s["gene"]]
            reg.append([s["site_id"], s["gene"], cur, s["c"], s["p"], s["legacy"] if s["legacy"] != s["c"] else "",
                        s["chrom"], s["pos37"], s["pos38"], s["ref"], s["alt"], s["klass"], d(s["since"])])
        head = ["site_id", "gene", "transcript", "hgvs_c", "hgvs_p", "legacy_name", "chrom", "grch37_pos",
                "grch38_pos", "ref", "alt", "classification", "classified_on"]
        hist = []
        for s in w.sites:
            for when, frm, to in s["history"]:
                hist.append([s["site_id"], s["gene"], s["c"], d(when), frm or "(first entry)", to,
                             "Variant review group" if frm else "Initial curation"])
        hist.sort(key=lambda r: (r[3], r[0]))
        hhead = ["site_id", "gene", "hgvs_c", "effective_on", "from_class", "to_class", "decided_by"]
        return (head, reg), (hhead, hist)

    def conditions_rows(self):
        head = ["condition", "gene", "inheritance", "on_2026_27_panel", "nominated_by", "onset", "severity_grade"]
        rows = []
        by_kind = {"SACS": "Paediatric neurology", "TMEM216": "Paediatric neurology", "PMM2": "Paediatric neurology",
                   "MCOLN1": "Paediatric neurology", "ARSA": "Paediatric neurology", "NPC1": "Paediatric neurology",
                   "HEXA": "Clinical genetics", "ASPA": "Clinical genetics", "FANCC": "Clinical genetics",
                   "BLM": "Clinical genetics", "ELP1": "Clinical genetics", "SLC26A2": "Clinical genetics",
                   "NPHS1": "Renal medicine", "SMPD1": "Metabolic medicine", "G6PC1": "Metabolic medicine",
                   "IDUA": "Metabolic medicine", "AGA": "Metabolic medicine", "BCKDHB": "Metabolic medicine",
                   "PEX1": "Metabolic medicine"}
        for k, (gene, cond, panel, f, v) in enumerate(P.CONDITIONS):
            nom = "Review group (annual)" if panel else by_kind[gene]
            onset = "Childhood" if gene not in ("ATP7B",) else "Childhood or adolescence"
            rows.append([cond, gene, "Autosomal recessive", "Yes" if panel else "No", nom, onset,
                         "Severe" if gene not in ("GJB2", "ATP7B", "USH2A") else "Moderate to severe"])
        return head, rows

    # -------------------------------------------------------------------------------------- the programme
    def programme_rows(self):
        w = self.w
        head = ["request_id", "couple_ref", "partner", "screen_type", "sample_no", "sample_received",
                "result_authorised", "genes_tested", "gene", "hgvs_c", "classification"]
        import analysis as A
        reg = {(s["gene"], s["c"]): s for s in w.sites}

        def shown(r, g, c):
            # the LIMS wrote each finding's class at authorisation until its January 2026 upgrade, and the
            # register's class on the day of the export after it
            if r["result"] < P.LIMS_UPGRADE or (g, c) not in reg:
                return r["klass"][(g, c)]
            return A.class_on(reg[(g, c)], P.EXTRACT) or "Uncertain significance"
        rows = []
        samples = {}
        n = 0
        for r in w.prog:
            n += 1
            req = "RQ%06d" % (310000 + n)
            if r["person"] not in samples:
                samples[r["person"]] = "CS-%s-%04d" % (r["result"].strftime("%y%m"), 1000 + len(samples) % 9000)
            sample = samples[r["person"]]
            tested = "Panel (11 genes)" if r["targeted"] is None else ";".join(r["targeted"])
            base = [req, r["couple"], 1 if r["letter"] == "A" else 2,
                    "Sequential" if r["sequential"] else "Simultaneous", sample,
                    d(r["recv"]) if not r["reused"] else d(r["result"] - timedelta(days=17)), d(r["result"]), tested]
            if r["found"]:
                for g, c in sorted(r["found"]):
                    rows.append(base + [g, c, shown(r, g, c)])
            else:
                rows.append(base + ["", "", ""])
            if r["fail"]:
                rows.append([req, r["couple"], 1 if r["letter"] == "A" else 2,
                             "Sequential" if r["sequential"] else "Simultaneous", sample + "F", d(r["recv"]), "",
                             tested, "", "", "Sample failed: repeat requested"])
        rows.sort(key=lambda x: (x[0], x[4], x[8]))
        return head, rows

    # -------------------------------------------------------------------------------------- distractors
    def turnaround_rows(self):
        rng = self.rng
        head = ["month", "samples_received", "results_authorised", "median_days_receipt_to_result",
                "p90_days_receipt_to_result", "repeat_samples_requested"]
        rows = []
        m = date(2025, 4, 1)
        while m <= date(2026, 3, 1):
            rec = int(rng.integers(380, 520))
            rows.append([m.strftime("%Y-%m"), rec, rec + int(rng.integers(-25, 26)), round(float(rng.uniform(15, 21)), 1),
                         int(rng.integers(26, 38)), int(rng.integers(4, 13))])
            m = date(m.year + (m.month == 12), m.month % 12 + 1, 1)
        return head, rows

    def referral_rows(self):
        rng = self.rng
        head = ["month", "referral_source", "couples_referred", "couples_declined_after_counselling"]
        rows = []
        m = date(2023, 4, 1)
        while m <= date(2026, 9, 1):
            for src, base in (("General practice", 120), ("Maternity booking", 70), ("Fertility clinic", 28),
                              ("Self-referral (online)", 22)):
                c = int(rng.poisson(base * (1.0 + 0.012 * ((m.year - 2023) * 12 + m.month))))
                rows.append([m.strftime("%Y-%m"), src, c, int(rng.binomial(c, 0.07))])
            m = date(m.year + (m.month == 12), m.month % 12 + 1, 1)
        return head, rows
