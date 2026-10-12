import numpy as np, itertools, sys
sys.path.insert(0,'/home/user/real-world-data-extraction-conformation-etl-build-problems/.work/notes/agent-scratch/task254-arch3/proto')
ff = np.array([62,74,58,81,95,77,66,70,56,88,72,64,90, 75,95,110], float)
K=len(ff); E0=5*60; NE=84; ep=E0+5*np.arange(NE)
def gen(rng,P,N=250):
    DAYS=[];INC=[]
    for dd in range(N):
        school = dd < P['nschool']
        d = float(np.clip(rng.lognormal(0,P['dsd']),0.6,1.7))*(1.0 if school else P['summer'])
        rain = rng.random() < 0.22
        if rain: d *= 1.12
        t0=6*60+P['onset']-P['oslope']*(d-1)
        tp=7*60+P['peak']+12*(d-1)
        tc=8*60+55+40*(d-1)
        peak=max(0.0,P['qmax']*(d-P['dthr']))
        tt=np.tile(ff,(NE,1))
        QS=P['qseg']; BN=QS[-1]+1
        for i,t in enumerate(ep):
            tm=t+2.5
            if t0<tm<tc:
                f=(tm-t0)/(tp-t0) if tm<=tp else max(0.0,1-(tm-tp)/(tc-tp))
                f=f**P['shape']; q=peak*f
                for j,k in enumerate(reversed(QS)):
                    share=P['qsh'][j]; lag=P['lag']*j
                    g=0.0 if f<lag else (f-lag)/(1-lag) if tm<=tp else f
                    tt[i,k]+=q*share*g
                tt[i,BN]+=0.15*q
            if 7*60+25<=tm<=8*60+35:
                w=max(0,1-abs(tm-(8*60))/35.0)
                tt[i,13]+=P['art']*w; tt[i,14]+=1.3*P['art']*w; tt[i,15]+=0.9*P['art']*w
        inc = rng.random()<P['pinc']
        if inc:
            k=int(rng.integers(1,13)); s=int(rng.integers(6*60+15,7*60+50)); L=int(rng.integers(30,80))
            extra=float(rng.uniform(250,900))
            for i,t in enumerate(ep):
                if s<=t<s+L: tt[i,k]+=extra*(1-(t-s)/(L+15))
        tt*=rng.lognormal(0,P['segsd'],size=K)[None,:]
        tt*=rng.lognormal(0,0.02,size=tt.shape)
        DAYS.append(tt); INC.append(inc)
    return DAYS,np.array(INC)
def ix(m): return int((m-E0)//5)
def walk(tt,dep,mode='floor'):
    t=dep*60.0
    for k in range(K):
        m=t/60.0
        if mode=='floor': v=tt[ix(m),k]
        elif mode=='interp':
            x=(m-E0-2.5)/5.0; i0=int(np.floor(x)); w=x-i0; v=(1-w)*tt[i0,k]+w*tt[i0+1,k]
        else:
            v=tt[ix(m),k]
            for _ in range(3): v=tt[ix(m+v/120.0),k]
        t+=v
    return (t-dep*60)/60.0
def inst(tt,dep): return tt[ix(dep)].sum()/60.0
def midread(tt,dep): return tt[ix(dep+ff.sum()/120.0)].sum()/60.0
deps=[6*60+m for m in range(10,100,5)]; ACC=8*60; acc=7.0
def evaluate(DAYS,INC):
    A=np.stack(DAYS); P90=np.percentile(A,90,axis=0); P50=np.percentile(A,50,axis=0)
    def sh(f,days=DAYS): return np.array([np.mean([d+acc+f(tt,d)<=ACC for tt in days]) for d in deps])
    sub=[tt for tt,m in zip(DAYS,INC) if not m]
    R={'inst':sh(inst),'inst_noinc':sh(inst,sub),'mid':sh(midread),'gold':sh(lambda a,d:walk(a,d)),
       'interp':sh(lambda a,d:walk(a,d,'interp')),'midfix':sh(lambda a,d:walk(a,d,'mf')),'walk_noinc':sh(lambda a,d:walk(a,d),sub)}
    Pr={'w90':np.array([d+acc+walk(P90,d)<=ACC for d in deps],float),'i90':np.array([d+acc+P90[ix(d)].sum()/60<=ACC for d in deps],float),
        'w50':np.array([d+acc+walk(P50,d)<=ACC for d in deps],float)}
    lat={}
    for k,v in list(R.items())+list(Pr.items()):
        thr=0.9 if k in R else 0.5
        ok=[d for d,x in zip(deps,v) if x>=thr]; lat[k]=ok[-1] if ok else None
    return R,Pr,lat
def score(R,lat):
    g=lat['gold']
    if g is None: return -1
    gi=deps.index(g)
    conds=[lat['interp']==g, lat['midfix']==g, lat['inst'] is not None and lat['inst']>=g+10,
           lat['mid'] is not None and lat['mid']!=g, lat['w90'] is not None and lat['w90']<=g-5,
           lat['i90']!=g, lat['w50']!=g, lat['inst_noinc']!=g, lat['walk_noinc']!=g]
    marg = R['gold'][gi]-0.9 >= 0.02 and 0.9-R['gold'][gi+1] >= 0.03
    ii=deps.index(lat['inst']) if lat['inst'] else None
    margd = ii is not None and R['inst'][ii]-0.9>=0.015 and 0.9-R['inst'][ii+1]>=0.015
    return sum(conds)+2*marg+margd
best=None
rng0=np.random.default_rng(7)
for trial in range(60):
    P=dict(nschool=178,summer=float(rng0.uniform(0.7,0.9)),dsd=float(rng0.uniform(0.18,0.3)),onset=float(rng0.uniform(20,50)),
           oslope=float(rng0.uniform(20,60)),peak=float(rng0.uniform(35,60)),qmax=float(rng0.uniform(1800,3200)),dthr=float(rng0.uniform(0.5,0.75)),
           shape=float(rng0.uniform(1.0,2.2)),lag=float(rng0.uniform(0.1,0.22)),qsh=[0.30,0.25,0.20,0.15,0.10],qseg=[6,7,8,9,10],
           art=float(rng0.uniform(50,120)),segsd=float(rng0.uniform(0.08,0.18)),pinc=float(rng0.uniform(0.08,0.15)))
    DAYS,INC=gen(np.random.default_rng(25403),P)
    R,Pr,lat=evaluate(DAYS,INC)
    s=score(R,lat)
    if best is None or s>best[0]:
        best=(s,P,R,Pr,lat)
        print('trial',trial,'score',s,{k:(f'{v//60}:{v%60:02d}' if v else None) for k,v in lat.items()})
s,P,R,Pr,lat=best
print(P)
print('slot ',' '.join(f'{d//60}:{d%60:02d}' for d in deps))
for k,v in R.items(): print(f'{k:10s}',' '.join(f'{x:4.2f}' for x in v))
for k,v in Pr.items(): print(f'{k:10s}',' '.join(f'{x:4.0f}' for x in v))
