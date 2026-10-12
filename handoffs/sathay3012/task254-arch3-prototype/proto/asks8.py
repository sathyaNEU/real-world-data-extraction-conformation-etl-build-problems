import numpy as np, importlib.util
src=open('search6.py').read().split("best=None; rng0")[0]
s6={}
exec(compile(src,'s6','exec'),s6)
P={'nschool': 178, 'summer': 0.654287064354632, 'dsd': 0.25661493747548575, 'jit': 8.007689541612194, 'onset': 25.372436212669186, 'oslope': 34.06724490267454, 'peak': 57.18403016686682, 'qmax': 2576.305524230817, 'dthr': 0.5017961982227336, 'shape': 1.0168772150974978, 'lag': 0.09917884329259773, 'art': 109.75051128777693, 'segsd': 0.2027488763807732, 'pinc': 0.15528319330550072}
DAYS,INC=s6['gen'](25403,P)
walk=s6['walk']; inst=s6['inst']; mid=s6['midread']
acc=7.0
deps=[6*60+m for m in range(30,85,5)]
Ew={d:np.mean([walk(tt,d)+acc for tt in DAYS]) for d in deps}
Ei={d:np.mean([inst(tt,d)+acc for tt in DAYS]) for d in deps}
Em={d:np.mean([mid(tt,d)+acc for tt in DAYS]) for d in deps}
print('slot  mean walked  mean inst  mean mid')
for d in deps: print(f'{d//60}:{d%60:02d}  {Ew[d]:6.2f}  {Ei[d]:6.2f}  {Em[d]:6.2f}')
# ---- Ask B cost model
R=96.50          # platform rate per vehicle hour
PRE=15; LAY=10; UNL=5; ALLOW=2.0   # minutes; deadhead allowance minutes per mile
MINB=1.75*60     # minimum paid block, minutes
def cost(d,E,m_out,m_back,buses,days):
    paid=PRE+ALLOW*m_out+LAY+E[d]+UNL+ALLOW*m_back
    paid=max(paid,MINB)
    report=d-LAY-ALLOW*m_out-PRE
    prem=max(0.0,6*60-report)
    per=R*paid/60+0.5*R*prem/60
    return buses*days*per, report
NEW=(15.6,16.4); OLD=(7.9,8.6)
DAYS27=252
cases={'golden (walked, new garage, 8 buses)':(Ew,NEW,8),'cracker (walked, Appendix B, 9 buses)':(Ew,OLD,9),
       'cracker escaped garage only (walked, new, 9 buses)':(Ew,NEW,9),'cracker escaped clock only (walked, old, 8)':(Ew,OLD,8),
       'mirror (instantaneous, Appendix B, 9 buses)':(Ei,OLD,9),'mirror escaped both (inst, new, 8)':(Ei,NEW,8)}
for k,(E,(mo,mb),b) in cases.items():
    row=[]
    for d in deps:
        c,rep=cost(d,E,mo,mb,b,DAYS27); row.append(round(c/100)*100)
    print(f'{k:52s}',' '.join(f'{x/1000:7.1f}' for x in row))
# report times and premium onset
for (mo,mb),lab in [(NEW,'new'),(OLD,'old')]:
    on=[d for d in deps if d-LAY-ALLOW*mo-PRE<6*60]
    print(lab,'premium applies through', f'{on[-1]//60}:{on[-1]%60:02d}' if on else None)
