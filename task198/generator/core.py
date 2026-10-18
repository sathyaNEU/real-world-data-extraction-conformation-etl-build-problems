"""task198 architecture 3: the clean truth.

Stratified two-stage design. Dwellings within PSUs (meshblocks), PSUs within strata. Each PSU is
worked by one interviewer and each interviewer works PSUs across every stratum, so the interviewer
groups cut across the replication groups the design supplies. The recorded outcome carries an area
effect at PSU level and a probing differential at interviewer level, redrawn each quarter.
"""
import numpy as np
CUR, CMP = "2026Q4", "2025Q4"
NAMED = "Manawatu-Whanganui"          # the region the prompt names
SIG_INT  = 0.100                       # between-interviewer SD of the probing differential
SIG_AREA = 0.050                       # between-PSU area effect SD
PSU_SIZE = 10
# region: (prevalence, true rise pts, strata, PSUs per stratum, interviewers)
REGIONS = {
 NAMED:                (0.224, 6.4, 4, 35,  4),     # the named region: a four-interviewer panel
 "Auckland":           (0.168, 0.4, 6, 40, 24),
 "Canterbury":         (0.159, 0.5, 5, 32, 16),
 "Wellington":         (0.173, 0.6, 4, 30, 12),
 "Waikato":            (0.197, 0.8, 4, 28, 11),
 "Bay of Plenty":      (0.216, 0.7, 3, 26,  9),
 "Otago":              (0.181, 0.9, 3, 22,  8),
 "Northland":          (0.243, 0.6, 3, 20,  7),
 "Hawke's Bay":        (0.231, 0.5, 3, 18,  7),
 "Taranaki":           (0.189, 0.6, 2, 18,  6),
 "Southland":          (0.206, 0.7, 2, 16,  5),
 "Gisborne":           (0.262, 0.8, 2, 12,  4),
}

def build(seed=31982198, sig_int=None):
    si = SIG_INT if sig_int is None else sig_int
    rng = np.random.default_rng(seed)
    rows = []          # (quarter, region, stratum, psu_id, interviewer_id, damp)
    pid = 0; iid = 0; psu_owner = {}; reg_ints = {}
    for r,(p0,rise,ns,npsu,ni) in REGIONS.items():
        reg_ints[r] = list(range(iid, iid+ni)); iid += ni
        for h in range(ns):
            for j in range(npsu):
                psu_owner[(r,h,pid)] = reg_ints[r][(h*npsu+j) % ni]   # cuts across strata
                pid += 1
    psus = {}
    for (r,h,k) in psu_owner: psus.setdefault(r,[]).append((h,k))
    for q in (CMP, CUR):
        d = {i: rng.normal(0, si) for i in range(iid)}       # redrawn each quarter
        for r,(p0,rise,ns,npsu,ni) in REGIONS.items():
            p = p0 + (rise/100.0 if q == CUR else 0.0)
            for (h,k) in psus[r]:
                a = rng.normal(0, SIG_AREA)
                i = psu_owner[(r,h,k)]
                pi = min(max(p + a + d[i], 0.01), 0.95)
                for y in rng.binomial(1, pi, PSU_SIZE):
                    rows.append((q, r, h, k, i, int(y)))
    return rows, reg_ints

# ---------------------------------------------------------------------------
# Ask-side truth. None of this is read by the main call, which uses only the
# dwelling records, the replicate weights, the design documentation, the quality
# framework, the concordance, the change note, the mode log and the workload log.
# ---------------------------------------------------------------------------
RNG=np.random.default_rng(5150198)
# ---- Ask 2 device: field cost claims. Two rate periods; the three largest field areas are paid on a
# consolidated monthly claim covering every assignment completed in the month, carrying no count.
RATE=(18.50, 19.75)                      # per completed interview, to 2026-09-30 / from 2026-10-01
AREAS=[("FA-%02d"%i, w) for i,w in enumerate([.16,.13,.11,.085,.075,.065,.06,.055,.05,.045,.04,.035,.03,.025,.02,.015],1)]
BIG={a for a,_ in AREAS[:3]}
def claims():
    rows=[]; per_q=collections.Counter()
    tot=sum(w for _,w in AREAS)
    for qi,(q,months) in enumerate([("2026Q1",(1,2,3)),("2026Q2",(4,5,6)),("2026Q3",(7,8,9)),("2026Q4",(10,11,12))]):
        n=[1780,1860,1915,1840][qi]
        for a,w in AREAS:
            k=int(round(n*w/tot))
            for m in months:
                km=int(round(k/3))
                rate=RATE[1] if m>=10 else RATE[0]
                if a in BIG:
                    rows.append(dict(q=q,area=a,month=m,lines=1,ivs=km,amt=round(rate*km,2),cons=True))
                else:
                    for _ in range(km): rows.append(dict(q=q,area=a,month=m,lines=1,ivs=1,amt=rate,cons=False))
                per_q[q]+=km
    return rows, per_q
CL,PERQ=claims()
golden_q={q:PERQ[q] for q in ("2026Q1","2026Q2","2026Q3","2026Q4")}
lines_q=collections.Counter()
for r in CL: lines_q[r['q']]+=1

# ---- Ask 3 device: population benchmarks. Amalgamated areas get the group total against each
# constituent; the true per-area figure is a published table split into two age bands to be added.
GROUPS={"TA-A":["TA-A1","TA-A2","TA-A3"],"TA-B":["TA-B1","TA-B2","TA-B3"],"TA-C":["TA-C1","TA-C2","TA-C3"]}
TRUE={}
base=[40200,31500,27400,24100,21800,19600,17300,15900,14200,12700]
codes=["TA-A1","TA-A2","TA-A3","TA-B1","TA-B2","TA-B3","TA-C1","TA-C2","TA-C3","TA-F"]
for c,v in zip(codes,base): TRUE[c]=v
GROUPTOT={g:sum(TRUE[c] for c in m) for g,m in GROUPS.items()}
memberof={c:g for g,m in GROUPS.items() for c in m}
IVS={c:int(round(v/1000*RNG.uniform(9.5,13.5))) for c,v in TRUE.items()}
# the one area the benchmarks file carries no figure for at all (returned by another team)
BLANK="TA-F"

def ask3_figures():
    g={}; nat={}
    for c in codes:
        g[(c,'pop')]=TRUE[c]; g[(c,'rate')]=round(1000.0*IVS[c]/TRUE[c],1)
        if c==BLANK: nat[(c,'pop')]=None; nat[(c,'rate')]=None       # blank sends everyone to the table
        elif c in memberof:
            nat[(c,'pop')]=GROUPTOT[memberof[c]]
            nat[(c,'rate')]=round(1000.0*IVS[c]/GROUPTOT[memberof[c]],1)
        else:
            nat[(c,'pop')]=TRUE[c]; nat[(c,'rate')]=g[(c,'rate')]     # ungrouped: file is right
    return g,nat
G3,N3=ask3_figures()
