"""Job titles people write in the census for each ISCO-08 unit group that Aldmere's workforce holds, with the unit
group's relative weight inside its sub-major group. Titles are the specific write-ins; vague write-ins are in world.py."""

TITLES = """1111:2:Member of the House of Assembly;Senator
1112:6:Permanent secretary;Assistant secretary, Department of Finance;Director of public works
1114:3:General secretary, trade union;Chief executive, chamber of commerce
1120:22:Managing director;Chief executive;CEO
1211:16:Finance manager;Financial controller;Head of finance
1212:9:HR manager;Human resources manager
1213:5:Policy manager;Strategy and planning manager
1219:12:Office manager;Operations manager;Business manager
1221:14:Sales manager;Marketing manager;Sales and marketing manager
1222:3:PR manager;Communications manager
1223:2:R&D manager
1311:5:Farm manager;Estate manager
1312:2:Fish farm manager
1321:10:Factory manager;Production manager;Plant manager
1323:9:Construction manager;Site manager;Project manager (construction)
1324:8:Logistics manager;Warehouse manager;Distribution manager
1330:5:IT manager;Head of IT services
1341:3:Nursery manager;Creche manager
1342:5:Practice manager;Hospital ward manager;Health centre manager
1343:3:Care home manager
1344:2:Social services manager
1345:6:School principal;Head teacher;Deputy principal
1346:5:Bank branch manager;Branch manager, credit union
1349:2:Practice manager, law firm
1411:6:Hotel manager;Guest house owner and manager
1412:8:Restaurant manager;Cafe owner
1420:18:Store manager;Shop owner;Retail manager
1431:3:Leisure centre manager;Gym manager
1439:3:Call centre manager;Travel agency manager
2111:1:Physicist
2112:1:Meteorologist
2113:2:Chemist;Analytical chemist
2114:1:Geologist
2120:2:Statistician;Actuary
2131:2:Marine biologist;Biologist
2132:1:Agricultural adviser
2133:3:Environmental officer;Environmental scientist
2141:3:Industrial engineer;Process engineer
2142:8:Civil engineer;Structural engineer
2143:1:Environmental engineer
2144:6:Mechanical engineer
2145:2:Chemical engineer
2149:2:Biomedical engineer
2151:5:Electrical engineer
2152:2:Electronics engineer
2153:2:Telecoms engineer
2161:4:Architect
2162:1:Landscape architect
2163:2:Product designer
2164:2:Town planner
2165:3:Land surveyor;Quantity surveyor
2166:5:Graphic designer;Web designer
2211:10:GP;General practitioner;Doctor
2212:7:Consultant anaesthetist;Surgeon;Consultant physician
2221:38:Staff nurse;Registered nurse;Clinical nurse manager
2222:4:Midwife
2240:2:Advanced paramedic
2250:2:Vet;Veterinary surgeon
2261:3:Dentist
2262:5:Pharmacist
2263:1:Health and safety officer
2264:4:Physiotherapist
2265:1:Dietitian
2266:2:Speech and language therapist
2267:1:Optometrist
2269:3:Occupational therapist;Radiographer
2310:12:Lecturer;University lecturer
2320:5:Further education tutor;Vocational trainer
2330:30:Secondary school teacher;Maths teacher;English teacher
2341:30:Primary school teacher;Teacher
2342:8:Early years educator;Montessori teacher
2352:5:Special needs teacher;SEN teacher
2353:3:English language teacher
2354:2:Music teacher;Piano teacher
2355:1:Art teacher
2359:2:Tutor;Education officer
2411:28:Accountant;Chartered accountant;Management accountant
2412:7:Financial adviser;Mortgage adviser
2413:6:Financial analyst;Investment analyst
2421:10:Management consultant;Business analyst
2422:7:Policy officer;Administrative officer, civil service
2423:9:HR officer;Recruitment consultant;HR business partner
2424:4:Training officer;Learning and development specialist
2431:8:Marketing executive;Digital marketing specialist
2432:3:PR executive;Communications officer
2433:5:Medical sales representative;Technical sales engineer
2434:3:IT sales executive;Account manager, software
2511:12:Systems analyst;Business systems analyst
2512:30:Software developer;Software engineer;Programmer
2513:10:Web developer;Front end developer
2514:8:Applications developer;Mobile app developer
2519:6:Software tester;QA engineer
2521:6:Database administrator;Data engineer
2522:10:Systems administrator;IT administrator
2523:10:Network engineer;Network administrator
2529:8:Cyber security analyst;Data analyst
2611:16:Solicitor;Barrister;Lawyer
2612:1:Judge
2619:2:Legal adviser;Notary
2621:1:Curator;Archivist
2622:3:Librarian
2631:3:Economist
2632:1:Social researcher
2634:4:Psychologist;Clinical psychologist
2635:18:Social worker;Counsellor
2636:4:Priest;Minister;Rector
2641:2:Writer;Copywriter
2642:5:Journalist;Reporter
2643:2:Translator;Interpreter
2651:3:Artist;Painter (artist)
2652:4:Musician;Singer
2653:1:Dance teacher
2654:3:Producer;TV producer
2655:2:Actor
2656:2:Radio presenter
2659:2:Entertainer
3111:6:Laboratory technician;Lab analyst
3112:7:Civil engineering technician;Site engineer
3113:6:Electrical technician
3114:4:Electronics technician
3115:9:Mechanical technician;Maintenance technician
3116:2:Process technician
3118:4:Draughtsman;CAD technician
3119:4:Engineering technician
3121:1:Quarry supervisor
3122:9:Production supervisor;Shift supervisor, factory
3123:9:Foreman, building site;Construction supervisor
3131:3:Power station operator
3132:3:Water treatment operator
3133:1:Process operator, chemical plant
3141:2:Laboratory technician, life sciences
3142:1:Agricultural technician
3151:3:Ship's engineer;Marine engineer
3152:4:Ship's officer;Harbour pilot
3153:3:Airline pilot;Pilot
3154:1:Air traffic controller
3211:6:Radiography technician;MRI technician
3212:8:Medical laboratory scientist;Phlebotomist
3213:6:Pharmacy technician;Dispenser
3221:20:Nursing assistant (associate);Enrolled nurse
3222:1:Midwifery assistant
3240:2:Veterinary nurse
3251:5:Dental nurse;Dental hygienist
3252:4:Health records officer;Medical coder
3253:2:Community health worker
3254:1:Dispensing optician
3255:2:Physiotherapy assistant
3256:4:Medical assistant
3257:3:Environmental health officer
3258:6:Paramedic;Ambulance driver
3259:2:Chiropodist;Podiatrist
3311:3:Stockbroker;Trader
3312:6:Loans officer;Credit controller
3313:12:Accounts technician;Accounting technician;Bookkeeper (qualified)
3314:2:Statistical assistant
3315:2:Loss adjuster;Valuer
3321:7:Insurance broker;Insurance agent
3322:18:Sales representative;Sales rep;Area sales representative
3323:5:Buyer;Purchasing officer
3324:1:Ship broker
3331:3:Freight forwarder;Customs clearance agent
3332:3:Event coordinator;Wedding planner
3333:2:Recruitment agent
3334:8:Estate agent;Property manager;Letting agent
3339:6:Business development executive;Sourcing agent
3341:9:Office supervisor;Team leader, administration
3342:2:Legal secretary
3343:14:Executive assistant;PA;Personal assistant
3344:5:Medical secretary
3351:3:Customs officer
3352:4:Tax officer;Revenue officer
3353:4:Social welfare officer
3354:1:Licensing officer
3355:3:Detective;Police inspector
3359:3:Inspector, Department of Agriculture
3411:5:Paralegal;Legal executive
3412:8:Care worker (social);Youth worker;Family support worker
3413:1:Pastoral worker
3421:2:Professional footballer
3422:5:Football coach;Swimming instructor
3423:6:Fitness instructor;Personal trainer
3431:3:Photographer
3432:3:Interior designer
3433:1:Museum technician
3434:12:Chef;Head chef;Sous chef
3435:2:Stage manager
3511:12:IT technician;Computer operator
3512:14:IT support;Helpdesk technician;Desktop support analyst
3513:8:Network technician;Systems technician
3514:3:Website administrator
3521:4:Sound engineer;Camera operator
3522:5:Telecoms technician;Cable technician
4110:30:Clerical officer;Office administrator;Administrator
4120:12:Secretary;Receptionist/secretary
4131:2:Typist
4132:6:Data entry clerk;Data entry operator
4211:12:Bank official;Bank teller;Cashier, bank
4212:3:Bookmaker;Croupier
4214:2:Debt collector
4221:4:Travel agent;Travel consultant
4222:18:Call centre agent;Customer service agent
4223:2:Switchboard operator
4224:5:Hotel receptionist;Front desk agent
4225:4:Information officer
4226:12:Receptionist;Medical receptionist
4227:1:Market research interviewer
4229:3:Customer care advisor
4311:30:Bookkeeper;Accounts assistant;Accounts payable clerk
4312:12:Insurance clerk;Claims handler
4313:7:Payroll administrator;Payroll clerk
4321:12:Stock controller;Storeman;Warehouse clerk
4322:4:Production planner;Production clerk
4323:5:Transport clerk;Dispatcher
4411:2:Library assistant
4412:12:Postman;Postal worker;Mail sorter
4413:1:Proof-reader
4415:3:Filing clerk
4416:3:HR assistant;Personnel clerk
4419:4:Administrative assistant
5111:3:Flight attendant;Cabin crew
5112:2:Bus conductor;Ticket inspector
5113:2:Tour guide
5120:22:Cook;Chef de partie
5131:24:Waiter;Waitress;Lounge staff
5132:12:Bartender;Barman
5141:12:Hairdresser;Barber
5142:7:Beautician;Nail technician
5151:3:Housekeeping supervisor
5152:2:Housekeeper
5153:4:Caretaker
5164:3:Dog groomer;Kennel assistant
5165:2:Driving instructor
5169:2:Funeral assistant
5211:4:Market trader
5221:9:Shopkeeper;Newsagent
5222:9:Shop supervisor;Supervisor, retail
5223:52:Sales assistant;Retail assistant;Shop assistant
5230:12:Cashier;Checkout operator
5242:1:Promotions staff
5244:3:Telesales agent
5245:2:Forecourt attendant
5246:4:Deli assistant;Counter assistant
5249:4:Sales advisor
5311:16:Childminder;Childcare worker
5312:12:Special needs assistant;Classroom assistant
5321:34:Healthcare assistant;Care assistant;Nursing home care assistant
5322:24:Home help;Home carer
5329:4:Hospital porter (care);Patient care assistant
5411:3:Firefighter
5412:14:Police officer;Police constable
5413:4:Prison officer
5414:12:Security guard;Security officer
5419:2:Lifeguard;Traffic warden
6111:8:Vegetable grower;Tillage farmer
6112:2:Fruit grower
6113:6:Gardener;Landscape gardener
6114:2:Crop farmer
6121:22:Dairy farmer;Beef farmer;Sheep farmer
6122:2:Poultry farmer
6130:8:Mixed farmer;Farmer
6210:2:Forestry worker
6221:2:Fish farmer
6222:3:Fisherman, inshore
6223:3:Fisherman, deep sea;Trawlerman
6310:1:Smallholder (own use)
7111:4:Builder;House builder
7112:6:Bricklayer;Blocklayer
7113:1:Stonemason
7114:2:Concrete finisher
7115:16:Carpenter;Joiner
7119:2:Scaffolder
7121:3:Roofer
7122:4:Tiler;Floor fitter
7123:4:Plasterer
7124:1:Insulation installer
7125:1:Glazier
7126:10:Plumber
7127:3:Refrigeration engineer;HVAC technician
7131:7:Painter and decorator
7132:2:Car sprayer
7133:1:Steeplejack
7211:1:Moulder
7212:8:Welder;Fabricator
7213:3:Sheet metal worker
7214:2:Steel erector
7222:3:Toolmaker
7223:5:CNC machinist;Machinist;Turner
7231:18:Mechanic;Motor mechanic;Car mechanic
7232:3:Aircraft mechanic
7233:6:Maintenance fitter;Plant fitter
7234:1:Bicycle mechanic
7311:1:Instrument technician
7313:1:Jeweller
7314:1:Potter
7316:1:Sign maker
7317:1:Furniture restorer
7318:1:Upholstery craft worker
7321:1:Pre-press technician
7322:3:Printer
7323:1:Bookbinder
7411:14:Electrician
7412:5:Electrical fitter
7413:3:Linesman
7421:4:Electronics repair technician
7422:4:Telecoms installer;Cable installer
7511:6:Butcher;Fishmonger
7512:6:Baker;Pastry chef (bakery)
7513:1:Cheesemaker
7522:3:Cabinet maker
7523:1:Woodworking machinist
7531:2:Tailor;Dressmaker
7533:1:Seamstress
7534:1:Upholsterer
7536:1:Cobbler
7543:2:Quality inspector
7544:1:Pest controller
8111:2:Miner;Quarry worker
8112:2:Crusher operator
8114:2:Concrete products operator
8121:2:Furnace operator
8131:4:Chemical process operator
8141:1:Rubber products operator
8142:4:Plastics machine operator;Injection moulding operator
8143:1:Paper machine operator
8153:2:Sewing machinist
8157:2:Laundry operator
8160:12:Food process operative;Machine operator, food plant
8171:1:Paper mill operator
8172:2:Sawmill operator
8181:1:Kiln operator
8183:6:Packing machine operator;Bottling line operator
8189:6:Machine operator;Production operative
8211:4:Assembler, machinery
8212:6:Electronics assembler;Assembly operator
8219:3:Assembly line worker
8311:1:Train driver
8321:1:Motorcycle courier
8322:24:Taxi driver;Van driver;Chauffeur
8331:10:Bus driver
8332:24:HGV driver;Lorry driver;Truck driver
8341:3:Tractor driver
8342:5:Digger driver;Plant operator
8343:2:Crane operator
8344:6:Forklift driver
8350:3:Deckhand
9111:8:Domestic cleaner
9112:40:Cleaner;Office cleaner;Hotel cleaner
9121:2:Laundry assistant
9122:4:Car valeter
9123:1:Window cleaner
9129:2:Cleaning operative
9211:4:Farm labourer;Farm hand
9212:5:Dairy worker;Milker
9213:2:Farm worker
9214:5:Garden labourer;Grounds worker
9215:1:Forestry labourer
9216:2:Fish farm worker
9311:2:Quarry labourer
9312:6:Groundworker;Roadworker
9313:22:Building labourer;General operative (construction)
9321:6:Packer;Hand packer
9329:16:General operative;Factory operative
9333:12:Warehouse operative;Loader;Docker
9334:8:Shelf stacker;Night filler
9411:6:Fast food crew member;Crew member
9412:14:Kitchen porter;Kitchen assistant
9510:2:Shoe shiner;Street performer
9520:2:Street trader
9611:4:Refuse collector;Bin man
9612:2:Recycling operative
9613:3:Street sweeper
9621:8:Courier;Delivery driver (parcels);Porter
9622:4:Handyman;Odd job man
9623:1:Meter reader
9629:4:Car park attendant;General worker"""


def titles():
    out = {}
    for line in TITLES.splitlines():
        code, w, t = line.split(":", 2)
        out[code] = (float(w), [x.strip() for x in t.split(";")])
    return out


if __name__ == "__main__":
    import isco08
    t = titles(); u = dict(isco08.units())
    assert all(c in u for c in t), [c for c in t if c not in u]
    sm = {}
    for c in t:
        sm.setdefault(c[:2], 0); sm[c[:2]] += 1
    print(len(t), sorted(sm.items()))
    assert len(sm) == 40
