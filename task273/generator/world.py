"""task273 architecture 4: the world. The Study's members, the variants they carry, the reads the two kits put on
every register site, the calls the two pipelines made, the laboratory's variant register, and the programme's
2025/26 screening results."""
from __future__ import annotations

from datetime import date, timedelta

import numpy as np
from scipy.stats import binom

import params as P


def het_sensitivity(depth, phase):
    """Chance that a heterozygote read `depth` times passes the phase's calling rule (alternate reads ~ Bin(d, 1/2))."""
    k, f = P.CALLER[phase]["k"], P.CALLER[phase]["f"]
    d = np.asarray(depth, dtype=int)
    need = np.maximum(k, np.ceil(f * d - 1e-9)).astype(int)
    return np.where(d > 0, binom.sf(need - 1, d, 0.5), 0.0)


def _day(rng, a, b, n):
    span = (b - a).days
    return [a + timedelta(days=int(x)) for x in rng.integers(0, span + 1, n)]


class World:
    def __init__(self, seed=P.SEED):
        self.seed = seed
        kids = np.random.SeedSequence(seed).spawn(5)       # one stream per part, so tuning one moves no other
        r = [np.random.default_rng(k) for k in kids]
        self._members(r[0])
        self._register(r[1])
        self._genotypes(r[2])
        self._depth_and_calls(r[3])
        self._programme(r[4])

    # ------------------------------------------------------------------------------------------ members
    def _members(self, rng):
        rows = []
        sid = 0
        for area, phase, n in P.AREAS:
            a, b = P.PHASE_DATES[phase]
            enrol = sorted(_day(rng, a - timedelta(days=60), b - timedelta(days=45), n))
            for e in enrol:
                sid += 1
                rows.append(dict(area=area, phase=phase, enrolled=e,
                                 sequenced=e + timedelta(days=int(rng.integers(21, 140)))))
        order = rng.permutation(len(rows))           # study ids are issued centrally, not by area
        self.N = len(rows)
        self.area = np.array([rows[i]["area"] for i in range(self.N)])
        self.phase = np.array([rows[i]["phase"] for i in range(self.N)])
        self.enrolled = [rows[i]["enrolled"] for i in range(self.N)]
        self.sequenced = [rows[i]["sequenced"] for i in range(self.N)]
        ids = np.empty(self.N, dtype=object)
        nums = 100000 + rng.choice(890000, self.N, replace=False)
        for j, i in enumerate(order):
            ids[i] = "AGS%06d" % nums[j]
        self.study_id = ids
        self.sample_id = np.array(["KGL-%s-%05d" % ("19" if p == 1 else "22", k + 1)
                                   for k, p in enumerate(self.phase)], dtype=object)
        self.sex = rng.choice(["F", "M"], self.N, p=[0.56, 0.44])
        self.birth_year = np.clip(np.round(rng.normal(1971, 14, self.N)), 1932, 2006).astype(int)
        u = rng.random(self.N)
        self.withdrawn = u < P.WITHDRAWN_SHARE
        self.withdrawn_late = (u >= P.WITHDRAWN_SHARE) & (u < P.WITHDRAWN_SHARE + P.WITHDRAWN_LATE)
        self.qc_fail = rng.random(self.N) < P.QC_FAIL_SHARE
        self.withdraw_date = [None] * self.N
        for i in np.where(self.withdrawn)[0]:
            lo = max(self.sequenced[i] + timedelta(days=30), date(2020, 1, 1))
            self.withdraw_date[i] = _day(rng, lo, P.CENSUS - timedelta(days=3), 1)[0]
        for i in np.where(self.withdrawn_late)[0]:
            self.withdraw_date[i] = _day(rng, P.CENSUS + timedelta(days=1), P.EXTRACT - timedelta(days=0), 1)[0]
        # the reference cohort on the census date: consent in force and a released genotype
        self.cohort = (~self.withdrawn) & (~self.qc_fail)

    # ------------------------------------------------------------------------------------------ register
    def _register(self, rng):
        """Every register site: the P/LP variants of the 30 genes, plus uncertain and benign entries, plus the
        2026 reclassifications. Site ids are the laboratory's."""
        tex = np.random.default_rng(np.random.SeedSequence(self.seed + 4711))   # texture only: days, codons
        sites = []
        vid = 0
        for gene, cond, panel, (fm, ff), variants in P.CONDITIONS:
            for (c, p, legacy, share, cls, chrom, pos38, ref, alt) in variants:
                vid += 1
                sites.append(dict(gene=gene, c=c, p=p, legacy=legacy or c, share=share, cls=cls, chrom=chrom,
                                  pos38=pos38, ref=ref, alt=alt, klass="Pathogenic" if share >= .3 else
                                  "Likely pathogenic", since=date(2017 + int(rng.integers(0, 6)), int(rng.integers(1, 13)),
                                                                  int(rng.integers(1, 28))), history=[]))
        # reclassified entries
        for gene, c, frm, to, when in P.RECLASSIFIED:
            chrom = next(v[5] for g, *_r, vs in P.CONDITIONS if g == gene for v in vs)
            base = next(v[6] for g, *_r, vs in P.CONDITIONS if g == gene for v in vs)
            sites.append(dict(gene=gene, c=c, p=self._protein(c), legacy=c, share=0.0, cls="normal", chrom=chrom,
                              pos38=base + int(rng.integers(-9000, 9000)), ref="C", alt="T", klass=to, since=when,
                              history=[(date(2019 + int(rng.integers(0, 3)), int(rng.integers(1, 13)),
                                             int(tex.integers(1, 29))), "", frm),
                                       (when, frm, to)]))
        # uncertain and benign texture
        for gene, cond, panel, freqs, variants in P.CONDITIONS:
            chrom, base = variants[0][5], variants[0][6]
            for j in range(int(rng.integers(P.VUS_PER_GENE[0], P.VUS_PER_GENE[1] + 1))):
                cpos = int(rng.integers(30, P.CDS_LENGTH[gene] - 6))
                nt = "ACGT"
                r_, a_ = nt[int(rng.integers(0, 4))], nt[int(rng.integers(0, 4))]
                if r_ == a_:
                    a_ = "T" if r_ != "T" else "C"
                rng.integers(0, 20), rng.integers(0, 20)               # the register stream's draws, kept
                prot = self._codon_change(tex, cpos, r_, a_)
                sites.append(dict(gene=gene, c="c.%d%s>%s" % (cpos, r_, a_), p=prot, legacy="c.%d%s>%s" % (cpos, r_, a_),
                                  share=0.0, cls="normal", chrom=chrom, pos38=base + int(rng.integers(-20000, 20000)),
                                  ref=r_, alt=a_, klass="Uncertain significance" if j % 2 == 0 else "Likely benign",
                                  since=date(2018 + int(rng.integers(0, 7)), int(rng.integers(1, 13)),
                                             int(tex.integers(1, 29))), history=[]))
        order = sorted(range(len(sites)), key=lambda i: (sites[i]["gene"], sites[i]["pos38"]))
        self.sites = [sites[i] for i in order]
        sid = 10000 + int(rng.integers(3, 40))
        for k, s in enumerate(self.sites):
            s["site_id"] = "KGLV%05d" % sid
            sid += int(rng.integers(1, 23))
            s["pos37"] = s["pos38"] - P.BUILD_OFFSET[s["chrom"]]
        self.pathogenic = [s for s in self.sites if s["klass"] in ("Pathogenic", "Likely pathogenic") and s["share"] > 0]
        # the reclassified entries that the Study carries (GJB2 c.101T>C before its downgrade; PEX1's upgrade)
        self.study_reclass = [s for s in self.sites if s["history"] and s["gene"] in ("GJB2", "PEX1")]

    CODE = {a + b + c: aa for (a, b, c), aa in zip(
        [(x, y, z) for x in "TCAG" for y in "TCAG" for z in "TCAG"],
        "Phe Phe Leu Leu Ser Ser Ser Ser Tyr Tyr Ter Ter Cys Cys Ter Trp Leu Leu Leu Leu Pro Pro Pro Pro His His "
        "Gln Gln Arg Arg Arg Arg Ile Ile Ile Met Thr Thr Thr Thr Asn Asn Lys Lys Ser Ser Arg Arg Val Val Val Val "
        "Ala Ala Ala Ala Asp Asp Glu Glu Gly Gly Gly Gly".split())}

    def _codon_change(self, tex, cpos, ref, alt):
        """A protein change a single base change at this coding position can make: a codon carrying the reference
        base at the position, translated before and after."""
        k = (cpos - 1) % 3
        for _ in range(200):
            cod = "".join("TCAG"[int(tex.integers(0, 4))] for _ in range(3))
            cod = cod[:k] + ref + cod[k + 1:]
            new = cod[:k] + alt + cod[k + 1:]
            a1, a2 = self.CODE[cod], self.CODE[new]
            if a1 != "Ter" and a2 != "Ter":
                return "p.(%s%d%s)" % (a1, (cpos + 2) // 3, a2 if a2 != a1 else "=")
        return "p.?"

    @staticmethod
    def _protein(c):
        return {"c.101T>C": "p.(Met34Thr)", "c.1952_1960dup": "p.(Pro651_Gly653dup)",
                "c.2972C>T": "p.(Thr991Met)", "c.1139C>T": "p.(Thr380Met)", "c.3454G>C": "p.(Asp1152His)",
                "c.799G>A": "p.(Gly267Arg)", "c.1342G>A": "p.(Glu448Lys)",
                "c.1106G>A": "p.(Arg369His)", "c.9689del": "p.(Asn3230IlefsTer34)", "c.404C>T": "p.(Ser135Leu)",
                "c.1935C>A": "p.(Asp645Glu)", "c.4338_4339del": "p.(Cys1447GlnfsTer29)"}.get(c, "p.?")

    # ------------------------------------------------------------------------------------------ genotypes
    def _genotypes(self, rng):
        """Each member carries at most one disease-causing variant per gene (no compound heterozygotes, no
        homozygotes among the Study's adult volunteers)."""
        founder = np.isin(self.area, P.FOUNDER_AREAS)
        self.carries = {}                       # site_id -> boolean array of carriers
        self.gene_carrier = {}
        for gene, cond, panel, (fm, ff), variants in P.CONDITIONS:
            pi = np.where(founder, ff, fm) / 1000.0
            car = rng.random(self.N) < pi
            sites = [s for s in self.pathogenic if s["gene"] == gene]
            shares = np.array([s["share"] for s in sites])
            # founder areas carry the founder variant almost exclusively for the three founder genes
            pick = np.empty(self.N, dtype=int)
            for grp in (founder, ~founder):
                sh = shares.copy()
                if gene in ("SACS", "TMEM216", "SLC26A2"):
                    sh = np.array([0.985 if s["cls"] == "gc" else 0.015 for s in sites]) if grp is founder else shares
                sh = sh / sh.sum()
                idx = np.where(grp)[0]
                pick[idx] = rng.choice(len(sites), len(idx), p=sh)
            for j, s in enumerate(sites):
                self.carries[s["site_id"]] = car & (pick == j)
            self.gene_carrier[gene] = car
        # the Study's carriers of the two reclassified variants it holds
        for s in self.study_reclass:
            rate = 3.6 / 1000 if s["gene"] == "GJB2" else 0.45 / 1000
            self.carries[s["site_id"]] = rng.random(self.N) < rate
        # every other register site the Study genotypes: uncertain and benign entries carried at their own rates,
        # and the two variants only the programme has met (no Study carrier)
        for s in self.sites:
            if s["site_id"] in self.carries:
                continue
            if s["history"]:
                self.carries[s["site_id"]] = np.zeros(self.N, dtype=bool)
            else:
                self.carries[s["site_id"]] = rng.random(self.N) < rng.uniform(0.3, 3.2) / 1000

    # ------------------------------------------------------------------------------------------ depth and calls
    def _depth_and_calls(self, rng):
        self.study_sites = list(self.sites)
        self.depth = {}
        self.alt_reads = {}
        self.called = {}
        lib = np.exp(rng.normal(0, 0.10, self.N))
        for s in self.study_sites:
            d = np.zeros(self.N, dtype=int)
            for ph in (1, 2):
                m = self.phase == ph
                extra, size = P.DEPTH[(s["cls"], ph)]
                mu = extra * lib[m]
                d[m] = P.CALLER[ph]["floor"] + rng.negative_binomial(size, size / (size + mu))
            self.depth[s["site_id"]] = d
            car = self.carries[s["site_id"]]
            alt = np.where(car, rng.binomial(d, 0.5), 0)
            k = np.where(self.phase == 1, P.CALLER[1]["k"], P.CALLER[2]["k"])
            f = np.where(self.phase == 1, P.CALLER[1]["f"], P.CALLER[2]["f"])
            need = np.maximum(k, np.ceil(f * d - 1e-9))
            self.alt_reads[s["site_id"]] = alt
            self.called[s["site_id"]] = car & (alt >= need) & (~self.qc_fail)
        self.sens = {sid: np.where(self.phase == 1, het_sensitivity(self.depth[sid], 1),
                                   het_sensitivity(self.depth[sid], 2)) for sid in self.depth}

    # ------------------------------------------------------------------------------------------ the programme
    def _programme(self, rng):
        """The 2025/26 screening year: couples referred, each partner's sample and result for the panel's genes.
        Simultaneous screens test both partners for every panel gene; sequential screens test the first partner
        and then the second only for the genes the first carries. Results name every variant found in a panel
        gene with its class on the day the report was authorised."""
        panel_genes = [g for g, c, on, f, v in P.CONDITIONS if on]
        self.panel_genes = panel_genes
        a, b = date(2025, 2, 10), date(2026, 3, 27)
        ncouple = 2930
        req_dates = sorted(_day(rng, a, b, ncouple))
        rows = []
        person = 0
        pool = []                                           # earlier partners who may re-present with a new partner
        reg = {(s["gene"], s["c"]): s for s in self.sites}
        reclass = {(g, c): (frm, to, when) for g, c, frm, to, when in P.RECLASSIFIED}
        fq = {g: f[0] / 1000 for g, c, on, f, v in P.CONDITIONS}
        sites_by_gene = {g: [s for s in self.pathogenic if s["gene"] == g] for g in panel_genes}
        for ci, rd in enumerate(req_dates):
            couple = "CS%05d" % (21000 + ci)
            sequential = rng.random() < 0.31
            partners = []
            for letter in ("A", "B"):
                reuse = (letter == "B" and pool and rng.random() < 0.035)
                if reuse:
                    prev = pool.pop(int(rng.integers(0, len(pool))))
                    partners.append(dict(letter=letter, reuse=prev))
                    continue
                person += 1
                found = []
                for g in panel_genes:
                    if rng.random() < fq[g] * 1.02:
                        sh = np.array([s["share"] for s in sites_by_gene[g]])
                        s = sites_by_gene[g][int(rng.choice(len(sh), p=sh / sh.sum()))]
                        found.append((g, s["c"]))
                    # the variants reclassified in 2026 that the programme meets
                    for (pg, pc), rate in P.PROGRAMME_ONLY.items():
                        if pg == g and rng.random() < rate:
                            found.append((g, pc))
                    if rng.random() < 0.0045:                          # an uncertain finding, never reported
                        vus = [s for s in self.sites if s["gene"] == g and s["klass"] == "Uncertain significance"
                               and not s["history"]]
                        if vus:
                            found.append((g, vus[int(rng.integers(0, len(vus)))]["c"]))
                partners.append(dict(letter=letter, person=person, found=found,
                                     fail=rng.random() < 0.018))
            # timing: samples arrive, a failed sample is re-requested, results authorised, couples told together
            recv = rd + timedelta(days=int(rng.integers(4, 22)))
            res = {}
            for pt in partners:
                if "reuse" in pt:
                    res[pt["letter"]] = pt["reuse"]["result"]
                    continue
                r = recv + timedelta(days=int(rng.integers(9, 26)))
                if pt["fail"]:
                    r = r + timedelta(days=int(rng.integers(14, 30)))
                pt["result"] = r
                res[pt["letter"]] = r
            if sequential:
                # the second partner's sample is requested only once the first is reported, for its genes only
                a_found = {g for g, c in partners[0].get("found", partners[0].get("reuse", {}).get("found", []))
                           if self._class_on(reg, reclass, g, c, res["A"]) in ("Pathogenic", "Likely pathogenic")}
                if not a_found:
                    partners = partners[:1]
                else:
                    if "reuse" not in partners[1]:
                        partners[1]["result"] = res["A"] + timedelta(days=int(rng.integers(12, 30)))
                        res["B"] = partners[1]["result"]
                    partners[1]["targeted"] = sorted(a_found)
            told = max(res[p["letter"]] for p in partners)
            for pt in partners:
                src = pt.get("reuse", pt)
                genes = pt.get("targeted", panel_genes)
                found = [(g, c) for g, c in src["found"] if g in genes]
                rows.append(dict(couple=couple, letter=pt["letter"], person=src["person"], req=rd, recv=recv,
                                 result=src["result"], told=told, sequential=sequential, targeted=pt.get("targeted"),
                                 fail=src.get("fail", False) and "reuse" not in pt, reused="reuse" in pt,
                                 found=found, genes=genes,
                                 klass={(g, c): self._class_on(reg, reclass, g, c, src["result"]) for g, c in found}))
                if "reuse" not in pt and pt["letter"] == "A":
                    pool.append(dict(person=src["person"], found=src["found"], result=src["result"]))
        self.prog = rows

    @staticmethod
    def _class_on(reg, reclass, gene, c, when):
        if (gene, c) in reclass:
            frm, to, eff = reclass[(gene, c)]
            return to if when >= eff else frm
        s = reg.get((gene, c))
        return s["klass"] if s else "Uncertain significance"
