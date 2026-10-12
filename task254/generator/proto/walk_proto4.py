import numpy as np, sys
ff = np.array([62,74,58,81,95,77,66,70,56,88,72,64,90, 75,95,110], float)
K=len(ff); E0=5*60; NE=72; ep=E0+5*np.arange(NE)
BN=9; QSEG=[4,5,6,7,8]
def gen_day(rng, demand, incident, school, P):
    tt=np.tile(ff,(NE,1))
    d=demand*(1.0 if school else P['summer'])
    t0=6*60+P['onset']-P['onset_slope']*(d-1)/0.25
    tp=7*60+P['peak']+10*(d-1)/0.25
    tc=8*60+50+30*(d-1)/0.25
    peak=max(0.0,P['qmax']*(d-P['dthr']))
    for i,t in enumerate(ep):
        tm=t+2.5
        if t0<tm<tc:
            f=(tm-t0)/(tp-t0) if tm<=tp else max(0.0,1-(tm-tp)/(tc-tp))
            f=f**P['shape']
            q=peak*f
            for j,k in enumerate(reversed(QSEG)):
                share=[0.30,0.25,0.20,0.15,0.10][j]
                lag=P['lag']*j
                g=0.0 if f<lag else (f-lag)/(1-lag) if tm<=tp else f
                tt[i,k]+=q*share*g
            tt[i,BN]+=0.20*q
        if 7*60+30<=tm<=8*60+30:
            w=1-abs(tm-(8*60+5))/30.0
            # arterial: own day factor, independent of freeway demand
            tt[i,13]+=P['art']*w*P['artf']; tt[i,14]+=1.3*P['art']*w*P['artf']; tt[i,15]+=0.9*P['art']*w*P['artf']
    if incident:
        k=int(rng.integers(1,13)); s=int(rng.integers(6*60+20,7*60+50)); L=int(rng.integers(25,70))
        extra=float(rng.integers(200,700))
        for i,t in enumerate(ep):
            if s<=t<s+L: tt[i,k]+=extra*(1-(t-s)/(L+10))
    # independent per-segment day effect (local weather, ramp metering, works)
    tt*=rng.lognormal(0,P['segsd'],size=K)[None,:]
    tt*=rng.lognormal(0,0.025,size=tt.shape)
    return tt
def ix(m): return int((m-E0)//5)
def walk(tt,dep,mode='floor'):
    t=dep*60.0
    for k in range(K):
        m=t/60.0
        if mode=='floor': v=tt[ix(m),k]
        elif mode=='interp':
            x=(m-E0-2.5)/5.0; i0=int(np.floor(x)); w=x-i0; v=(1-w)*tt[i0,k]+w*tt[i0+1,k]
        elif mode=='midfix':
            v=tt[ix(m),k]
            for _ in range(3): v=tt[ix(m+v/120.0),k]
        t+=v
    return (t-dep*60)/60.0
def inst(tt,dep): return tt[ix(dep)].sum()/60.0
def midread(tt,dep): return tt[ix(dep+ff.sum()/120.0)].sum()/60.0
def run(P, seed=25403, verbose=True):
    rng=np.random.default_rng(seed)
    N=250; DAYS=[]; INC=[]
    for dd in range(N):
        school=dd<P['nschool']
        demand=float(np.clip(rng.lognormal(0,P['dsd']),0.7,1.5))
        inc=rng.random()<P['pinc']
        P['artf']=float(rng.lognormal(0,0.35))
        DAYS.append(gen_day(rng,demand,inc,school,P)); INC.append(inc)
    INC=np.array(INC); A=np.stack(DAYS)
    P90=np.percentile(A,90,axis=0); P50=np.percentile(A,50,axis=0)
    ACC=8*60; acc=7.0
    deps=[6*60+m for m in range(25,100,5)]
    def sh(f, days=DAYS):
        return np.array([np.mean([d+acc+f(tt,d)<=ACC for tt in days]) for d in deps])
    sub=[tt for tt,m in zip(DAYS,INC) if not m]
    rows={'inst_day':sh(inst),'inst_noinc':sh(inst,sub),'mid_read':sh(midread),
          'GOLD walk_floor':sh(lambda tt,d:walk(tt,d,'floor')),
          'walk_interp':sh(lambda tt,d:walk(tt,d,'interp')),
          'walk_midfix':sh(lambda tt,d:walk(tt,d,'midfix')),
          'walk_noinc':sh(lambda tt,d:walk(tt,d,'floor'),sub)}
    prof={'walk_p90prof':[d+acc+walk(P90,d)<=ACC for d in deps],
          'inst_p90prof':[d+acc+P90[ix(d)].sum()/60<=ACC for d in deps],
          'walk_p50prof':[d+acc+walk(P50,d)<=ACC for d in deps]}
    out={}
    if verbose: print('slot           ', ' '.join(f'{d//60}:{d%60:02d}' for d in deps))
    for k,v in rows.items():
        lat=[d for d,x in zip(deps,v) if x>=0.9]; lat=lat[-1] if lat else None; out[k]=lat
        if verbose: print(f'{k:16s}', ' '.join(f'{x:4.2f}' for x in v), ' ->', f'{lat//60}:{lat%60:02d}' if lat else None)
    for k,v in prof.items():
        lat=[d for d,x in zip(deps,v) if x]; lat=lat[-1] if lat else None; out[k]=lat
        if verbose: print(f'{k:16s}', ' '.join(' yes' if x else '  no' for x in v), ' ->', f'{lat//60}:{lat%60:02d}' if lat else None)
    return out
P=dict(summer=0.8,onset=40,onset_slope=20,peak=45,qmax=2400,dthr=0.62,shape=1.6,lag=0.15,art=80,segsd=0.10,dsd=0.16,pinc=0.10,nschool=178)
if __name__=='__main__':
    run(P)
