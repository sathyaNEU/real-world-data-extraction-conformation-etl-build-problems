"""The world's constants: Ashcombe Valley Health's sterile compounding unit, its compounders, the products it
batch-compounds, how each tubing set's delivered volume moves, and the procedure the unit works to."""
import datetime as dt

SEED = 27267

ORG = "Ashcombe Valley Health"
HOSPITAL = "Ashcombe Valley Regional Hospital"
UNIT = "Sterile Compounding Unit"
CITY = "Peterborough, Ontario"
YEAR = 2026
FIRST_DAY = dt.date(2026, 1, 1)
LAST_DAY = dt.date(2026, 12, 31)
EXPORT_DAY = dt.date(2027, 1, 18)        # the server export, the register copies and the request
CUTOVER = dt.date(2027, 4, 5)           # the IV workflow system goes live
LIMIT_PER_100K = 10                     # the policy's line: out-of-tolerance doses per 100,000 doses made
CHECK_EVERY = {"syringe": 100, "bag": 20}   # after the first dose of each batch, every hundredth syringe and twentieth bag
SET_MAX_HOURS = 24                      # a set may carry consecutive batches of one product within 24 hours

PEOPLE = {"director": "Cynthia Underwood", "quality": "Erin Stewart", "lead_tech": "Jacob Burgess",
          "project": "Spencer Frank"}

# Stations. PC-1 to PC-3 are peristaltic compounders (a tubing set per set-up, calibrated gravimetrically at
# set-up); PC-4 is a syringe-driver compounder (a fluid path set, no peristaltic tubing); GC-1 is the gravimetric
# compounder that weighs every dose it fills. PC-3 was replaced on 14 July 2026 (a new unit, a new serial).
STATIONS = {
    "PC-1": {"model": "Vireo PX-40 peristaltic compounder", "serials": [("VPX40-21877", FIRST_DAY, None)]},
    "PC-2": {"model": "Vireo PX-40 peristaltic compounder", "serials": [("VPX40-22305", FIRST_DAY, None)]},
    "PC-3": {"model": "Vireo PX-40 peristaltic compounder",
             "serials": [("VPX40-19024", FIRST_DAY, dt.date(2026, 7, 13)), ("VPX40-30961", dt.date(2026, 7, 14), None)]},
    "PC-4": {"model": "Altus SD-6 syringe-driver compounder", "serials": [("ASD6-04412", FIRST_DAY, None)]},
    "GC-1": {"model": "Kestrel G2 gravimetric compounder", "serials": [("KG2-1187", FIRST_DAY, None)]},
}
REPLACED_ON = dt.date(2026, 7, 14)

# Products. code: the compounders' own product number; vol: labelled volume (mL); tol: volume tolerance (per cent
# either way); sg: specific gravity; tare: container and cap (g); station; per week: batches on weekdays and on
# Saturdays; size: doses per batch (range); k: delivered volume lost per litre pumped through the set (per cent of
# target); a0, a0sd: the set-up calibration's start (per cent); s: dose-to-dose scatter (per cent); carry2, carry3:
# the chance a set carries a second, a third batch; verified: already weighed dose by dose on GC-1.
PRODUCTS = [
    # antibiotic syringes, PC-1
    dict(code="P0412", name="Cefazolin 2 g in 20 mL syringe", short="cefazolin 2 g syringe", vol=20, tol=5, sg=1.045,
         tare=14.8, station="PC-1", wk=(1.75, 1.0), size=(165, 199), k=0.50, a0=0.85, a0sd=0.30, s=0.55,
         carry2=0.20, carry3=0.25),
    dict(code="P0413", name="Cefazolin 1 g in 10 mL syringe", short="cefazolin 1 g syringe", vol=10, tol=5, sg=1.025,
         tare=8.9, station="PC-1", wk=(0.6, 0.2), size=(140, 220), k=0.55, a0=0.80, a0sd=0.30, s=0.60,
         carry2=0.05, carry3=0.0),
    dict(code="P0431", name="Cefoxitin 2 g in 20 mL syringe", short="cefoxitin 2 g syringe", vol=20, tol=5, sg=1.050,
         tare=14.8, station="PC-1", wk=(1.3, 0.5), size=(230, 300), k=0.62, a0=0.85, a0sd=0.30, s=0.55,
         carry2=0.10, carry3=0.0),
    # anaesthesia syringes, PC-2
    dict(code="P0507", name="Phenylephrine 100 mcg/mL 10 mL syringe", short="phenylephrine 10 mL syringe", vol=10,
         tol=5, sg=1.005, tare=8.9, station="PC-2", wk=(1.75, 1.0), size=(165, 199), k=1.05, a0=0.90, a0sd=0.30,
         s=0.60, carry2=0.20, carry3=0.25),
    dict(code="P0509", name="Ephedrine 5 mg/mL 10 mL syringe", short="ephedrine 10 mL syringe", vol=10, tol=5,
         sg=1.006, tare=8.9, station="PC-2", wk=(0.6, 0.3), size=(150, 210), k=0.70, a0=0.80, a0sd=0.30, s=0.60,
         carry2=0.05, carry3=0.0),
    dict(code="P0522", name="Ketamine 10 mg/mL 10 mL syringe", short="ketamine 10 mL syringe", vol=10, tol=5, sg=1.008,
         tare=8.9, station="PC-2", wk=(0.4, 0.2), size=(100, 160), k=0.75, a0=0.80, a0sd=0.30, s=0.62,
         carry2=0.05, carry3=0.0),
    # bags, PC-3 (a set every batch, by the unit's practice for bags)
    dict(code="P0610", name="Ampicillin 2 g in 50 mL bag", short="ampicillin 2 g bag", vol=50, tol=5, sg=1.020,
         tare=21.5, station="PC-3", wk=(1.0, 0.4), size=(70, 95), k=1.10, a0=2.20, a0sd=0.30, s=0.50,
         carry2=0.0, carry3=0.0),
    dict(code="P0614", name="Piperacillin-tazobactam 4.5 g in 100 mL bag", short="piperacillin-tazobactam bag",
         vol=100, tol=5, sg=1.030, tare=27.0, station="PC-3", wk=(1.0, 0.4), size=(72, 92), k=0.48, a0=2.40,
         a0sd=0.30, s=0.50, carry2=0.0, carry3=0.0),
    dict(code="P0618", name="Vancomycin 1 g in 200 mL bag", short="vancomycin 1 g bag", vol=200, tol=5, sg=1.006,
         tare=38.5, station="PC-3", wk=(0.6, 0.2), size=(38, 46), k=0.46, a0=2.40, a0sd=0.30, s=0.50,
         carry2=0.0, carry3=0.0),
    dict(code="P0625", name="Ondansetron 8 mg in 50 mL bag", short="ondansetron 8 mg bag", vol=50, tol=5, sg=1.004,
         tare=21.5, station="PC-3", wk=(0.4, 0.2), size=(60, 90), k=0.30, a0=0.60, a0sd=0.30, s=0.55,
         carry2=0.0, carry3=0.0),
    # syringe-driver products, PC-4 (no tubing drift)
    dict(code="P0702", name="Midazolam 1 mg/mL 50 mL syringe", short="midazolam 50 mL syringe", vol=50, tol=5,
         sg=1.003, tare=31.0, station="PC-4", wk=(0.55, 0.4), size=(100, 125), k=0.0, a0=-2.70, a0sd=0.12, s=0.72,
         carry2=0.0, carry3=0.0),
    dict(code="P0705", name="Heparin 1,000 units/mL 5 mL syringe", short="heparin 5 mL syringe", vol=5, tol=5,
         sg=1.004, tare=6.1, station="PC-4", wk=(0.6, 0.2), size=(120, 200), k=0.0, a0=-0.30, a0sd=0.15, s=0.70,
         carry2=0.0, carry3=0.0),
    # already weighed dose by dose on the gravimetric compounder (not candidates)
    dict(code="P0801", name="Potassium chloride 20 mmol in 100 mL bag", short="potassium chloride bag", vol=100,
         tol=5, sg=1.012, tare=27.0, station="GC-1", wk=(0.8, 0.4), size=(50, 80), k=0.0, a0=0.0, a0sd=0.05,
         s=1.15, carry2=0.0, carry3=0.0, verified=True),
    dict(code="P0806", name="Norepinephrine 4 mg in 250 mL bag", short="norepinephrine bag", vol=250, tol=5,
         sg=1.005, tare=44.0, station="GC-1", wk=(0.6, 0.2), size=(30, 50), k=0.0, a0=-0.60, a0sd=0.05, s=1.10,
         carry2=0.0, carry3=0.0, verified=True),
]
CANDIDATES = [p["code"] for p in PRODUCTS if not p.get("verified")]

# Hours the unit compounds (local time): weekdays two shifts 07:00 to 23:00, Saturdays 08:00 to 16:00, closed on
# Sundays and on the statutory holidays below.
HOLIDAYS = {dt.date(2026, 1, 1), dt.date(2026, 2, 16), dt.date(2026, 4, 3), dt.date(2026, 5, 18), dt.date(2026, 7, 1),
            dt.date(2026, 8, 3), dt.date(2026, 9, 7), dt.date(2026, 10, 12), dt.date(2026, 12, 25),
            dt.date(2026, 12, 26)}
SECONDS_PER_DOSE = {"PC-1": (21, 27), "PC-2": (17, 22), "PC-3": (48, 62), "PC-4": (34, 44), "GC-1": (70, 95)}
ABORT_RATE = 0.0035                     # a dose stopped mid-fill by an occlusion alarm, discarded and refilled
RESEAT_RATE = 0.06                      # a set re-seated after an alarm: a second SET_UP event on the same set lot
LETTER = {"PC-1": "A", "PC-2": "B", "PC-3": "C", "PC-4": "D", "GC-1": "G"}
