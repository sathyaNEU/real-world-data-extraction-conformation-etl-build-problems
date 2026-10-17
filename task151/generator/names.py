"""Player names for the league, drawn the way a real major league's player population looks: about seven in ten
from the United States (every background), the rest from the Dominican Republic, Venezuela, Cuba, Puerto Rico, Mexico,
Colombia, Panama, Curacao, Canada, Japan, Korea and Australia, each origin with its own given names and surnames,
accents where the origin writes them, and a few generational suffixes."""
from __future__ import annotations

import unicodedata

US_FIRST = """Aaron Adam Alex Andrew Anthony Austin Bailey Ben Blake Bobby Brady Brandon Brendan Brent Brett Brian Brock Bryce
Caleb Cameron Carson Carter Casey Chad Chase Chris Christian Clay Cody Cole Colin Colton Connor Corey Craig Dalton Dane
Daniel Darius Darnell Dave David Dawson Derek Devin Dillon Drew Dustin Dylan Eli Elijah Eric Ethan Evan Garrett Gavin
Grady Grant Greg Griffin Hayden Hunter Ian Isaac Jace Jack Jackson Jacob Jake Jalen Jared Jarrett Jason Jay Jeff Jeremy
Jesse Joel Joey Jon Jonah Jordan Josh Justin Kade Kaleb Keegan Keith Kellen Kenny Kevin Kody Kyle Lance Landon Lane Logan
Lucas Luke Malik Marcus Mason Matt Max Micah Mike Mitch Nate Nathan Nick Noah Nolan Owen Parker Patrick Paul Peyton Pierce
Preston Quinn Reed Reese Riley Rob Ryan Sam Sawyer Scott Sean Seth Shane Spencer Stephen Taylor Terrell Thomas Tim Todd
Travis Trent Trevor Tristan Troy Ty Tyler Wade Walker Wes Wyatt Xavier Zach Zane""".split()
US_LAST = """Abbott Acker Adair Alderman Allard Ammons Ashby Atwell Bader Bagwell Banks Barlow Barnhart Bassett Beal Beckett
Bell Benning Bevis Bickford Birch Blakely Blevins Bolton Boone Boswell Bowden Boyer Bradshaw Brannon Bratton Briggs
Brinson Brock Broderick Bullock Burkett Burris Cahill Calhoun Callaway Carmody Carver Cash Chandler Childress Clary
Coble Cofield Colvin Conley Cordell Corley Cowan Crabtree Crandall Crisp Crowder Culver Dailey Dangerfield Darby Deaton
Delk Denning Dewitt Dickerson Dobbs Donnelly Dowell Driscoll Dudley Dunlap Durbin Eason Eckert Edmonds Ellery Embry
England Epps Ewing Fairley Farris Faulk Fenton Finley Fitch Fletcher Forsythe Fountain Fowler Frazee Fry Fuqua Gaines
Galloway Gant Garland Gentry Gibbs Gilley Gipson Glover Godwin Goins Granger Grubb Gwinn Hagan Hairston Hale Hammond
Harbin Hargrove Harlow Hartsell Haskins Hatcher Hawley Haynes Heflin Hendrix Herron Hickey Hinson Hollis Holloway Hooper
Horton Houck Howland Huff Hutto Ingram Isom Jarrell Jeter Jolley Kaplan Keel Kendrick Kimble Kincaid Kirby Knapp Kohler
Lacey Lamb Landry Langford Larkin Lattimore Ledford Lindsey Lockett Loftin Lowery Lusk Lyle Mabry Maddox Mallory Mangum
Marlowe Massey Mayfield McCants McCrory McDuffie McGowan McKinney McNair Meeks Merritt Mims Mobley Moody Mosley Munn
Nance Nash Neely Newsome Nix Noble Norwood Oakes Odom Overton Pace Paige Parrish Pate Peebles Pendleton Petty Pickett
Pittman Plunkett Poole Pruitt Purvis Quarles Rainey Ratliff Redd Reeder Rhodes Rigsby Roark Rollins Rooney Royster Rudd
Sadler Satterfield Schaefer Scruggs Settle Shanklin Shelby Shipley Shook Sizemore Slater Sloan Snead Sparks Spurlock
Stamper Stanfield Starling Stokes Strickland Stroud Sumner Swann Swope Talley Tankersley Teague Thigpen Tidwell Tillman
Toler Trammell Tubbs Tuttle Upshaw Vance Varner Vick Waddell Walden Waller Watts Weathers Weeks Wester Whitlock Wicker
Wilder Willard Winstead Witt Womack Woodall Worley Wynn Yancey Yates Yeager Youngblood Zeller""".split()

HISP_FIRST = """Adolfo Alberto Alejandro Alexis Andrés Ángel Aníbal Antonio Ariel Armando Brayan Carlos Cristian Daniel
Darwin Diego Edwin Elvis Emilio Enrique Ezequiel Fernando Francisco Freddy Gabriel Geraldo Gilberto Gregorio Héctor
Humberto Ignacio Iván Jairo Javier Jesús Joel Jonathan Jorge José Juan Julio Leonel Luis Manuel Marcos Mario Miguel
Moisés Nelson Néstor Omar Orlando Óscar Pablo Pedro Rafael Ramón Raúl Reinaldo Ricardo Roberto Rodolfo Rolando Rubén
Samuel Santiago Sergio Teoscar Tomás Ulises Víctor Wilmer Yandy Yeison Yoan Yordan Yunior""".split()
HISP_LAST = """Abreu Acevedo Acosta Alcántara Almonte Alvarado Arias Arroyo Báez Batista Beltré Bermúdez Bonilla
Cabrera Calderón Camacho Candelario Carrasco Castillo Castro Cedeño Cisneros Contreras Cordero Cruz Delgado Díaz Duarte
Encarnación Escobar Espinal Estévez Feliz Fermín Figueroa Franco Frías Galván García Gil Guerrero Gutiérrez Hernández
Herrera Jiménez León Liriano Lugo Machado Marte Martínez Medina Mejía Mercedes Montero Morel Moreno Núñez Ogando Olivares
Ortega Ortiz Paredes Peguero Peña Peralta Pimentel Polanco Quintero Ramírez Reyes Rivas Rodríguez Rojas Rosario Ruiz
Salazar Sánchez Santana Serrano Soto Suárez Tapia Tavárez Tejada Toribio Urías Valdez Vargas Vásquez Ventura Vizcaíno
Zapata""".split()
CUBAN_FIRST = """Yasiel Yoenis Yuli Lourdes Aledmys Yordan Andy Jorge Adrián Raidel Osvaldo Yadier""".split()
JP_FIRST = """Haruki Kenta Shota Takumi Yuto Ryosuke Daichi Kazuya Masato Seiya Tomoya""".split()
JP_LAST = """Arakawa Fujimoto Hayashi Ishikawa Kondo Matsuda Nakagawa Ogawa Sakamoto Takeda Yamaguchi""".split()
KR_FIRST = """Ha-seong Jung-ho Min-jae Seung-woo Ji-hwan Hyun-soo Dong-hyun""".split()
KR_LAST = """Kim Lee Park Choi Jung Kang Yoon""".split()
CA_FIRST = """Liam Noah Owen Tyler Jordan Logan Mathieu Étienne Gabriel Félix""".split()
CA_LAST = """Beaulieu Gagnon Lavoie Bouchard Tremblay MacLeod Fraser Campbell Robertson Henderson""".split()
AU_FIRST = """Liam Lachlan Mitchell Jarrod Darcy Callum""".split()
AU_LAST = """Kennelly Whitfield Doolan Halloran Cutler""".split()
CW_FIRST = """Jurickson Didi Ozhaino Jonathan Andrelton Wladimir Shurendell""".split()
CW_LAST = """Martis Profar Simmons Janga Balentina Isenia Cijntje""".split()

ORIGINS = [   # origin, share of the league's hitters
    ("US", 0.645), ("DR", 0.11), ("VE", 0.075), ("PR", 0.025), ("CU", 0.025), ("MX", 0.025), ("CO", 0.012),
    ("PA", 0.01), ("CW", 0.01), ("CA", 0.025), ("JP", 0.013), ("KR", 0.01), ("AU", 0.015),
]


def ascii_fold(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def draw_name(r, used):
    """One unused full name from an origin drawn by its share. Returns (name, origin)."""
    keys = [o for o, _ in ORIGINS]
    p = [w for _, w in ORIGINS]
    p = [x / sum(p) for x in p]
    for _ in range(200):
        o = keys[int(r.choice(len(keys), p=p))]
        if o == "US":
            if r.random() < 0.09:      # Hispanic-American players born in the United States
                first = HISP_FIRST[int(r.integers(len(HISP_FIRST)))]
                first = ascii_fold(first) if r.random() < 0.7 else first
                last = ascii_fold(HISP_LAST[int(r.integers(len(HISP_LAST)))])
            else:
                first = US_FIRST[int(r.integers(len(US_FIRST)))]
                last = US_LAST[int(r.integers(len(US_LAST)))]
            name = "%s %s" % (first, last)
            if r.random() < 0.035:
                name += " Jr."
        elif o in ("DR", "VE", "PR", "MX", "CO", "PA"):
            first = HISP_FIRST[int(r.integers(len(HISP_FIRST)))]
            last = HISP_LAST[int(r.integers(len(HISP_LAST)))]
            if o == "PR" and r.random() < 0.4:
                first = ascii_fold(first)
            name = "%s %s" % (first, last)
            if r.random() < 0.03:
                name += " Jr."
        elif o == "CU":
            first = CUBAN_FIRST[int(r.integers(len(CUBAN_FIRST)))] if r.random() < 0.6 else HISP_FIRST[int(r.integers(len(HISP_FIRST)))]
            name = "%s %s" % (first, HISP_LAST[int(r.integers(len(HISP_LAST)))])
        elif o == "JP":
            name = "%s %s" % (JP_FIRST[int(r.integers(len(JP_FIRST)))], JP_LAST[int(r.integers(len(JP_LAST)))])
        elif o == "KR":
            name = "%s %s" % (KR_FIRST[int(r.integers(len(KR_FIRST)))], KR_LAST[int(r.integers(len(KR_LAST)))])
        elif o == "CA":
            name = "%s %s" % (CA_FIRST[int(r.integers(len(CA_FIRST)))], CA_LAST[int(r.integers(len(CA_LAST)))])
        elif o == "AU":
            name = "%s %s" % (AU_FIRST[int(r.integers(len(AU_FIRST)))], AU_LAST[int(r.integers(len(AU_LAST)))])
        else:
            name = "%s %s" % (CW_FIRST[int(r.integers(len(CW_FIRST)))], CW_LAST[int(r.integers(len(CW_LAST)))])
        if name not in used and ascii_fold(name) not in used:
            used.add(name)
            used.add(ascii_fold(name))
            return name, o
    raise RuntimeError("name pool exhausted")


def legacy_code(name, taken):
    """The legacy statistics system's player code: four letters of the surname (padded with dashes), the first initial,
    and a three-digit sequence, as a retrosheet-style id."""
    base = ascii_fold(name.replace(" Jr.", "")).lower()
    parts = base.split()
    first, last = parts[0], "".join(parts[1:])
    last = "".join(c for c in last if c.isalpha())
    stem = (last[:4] + "----")[:4] + first[0]
    n = 1
    while "%s%03d" % (stem, n) in taken:
        n += 1
    code = "%s%03d" % (stem, n)
    taken.add(code)
    return code


# ---------------------------------------------------------------------------------------------- the league's names
# The league is renamed from these wider pools once every player exists, on its own stream (so no other draw moves):
# each pool runs roughly from the commonest name to the rarest, and a name is drawn with a weight falling with its rank,
# so a common surname recurs a few times across six seasons of a league and an uncommon one rarely does. The club's
# designed players keep their names.
W_US_LAST = """Smith Johnson Williams Brown Jones Miller Davis Wilson Anderson Taylor Thomas Moore Martin Jackson
Thompson White Harris Clark Lewis Robinson Walker Young Allen King Wright Scott Hill Green Adams Baker Nelson Hall
Campbell Mitchell Carter Roberts Phillips Evans Turner Parker Collins Edwards Stewart Morris Murphy Cook Rogers Morgan
Cooper Peterson Bailey Reed Kelly Howard Cox Ward Richardson Watson Brooks Wood James Bennett Gray Hughes Price
Sanders Myers Long Ross Foster Powell Jenkins Perry Russell Sullivan Bell Coleman Butler Henderson Fisher Simmons
Patterson Jordan Reynolds Hamilton Graham Cole West Hayes Gibson Bryant Ellis Stevens Murray Ford Marshall Owens
McDonald Harrison Kennedy Wells Alexander Griffin Hunt Palmer Robertson Black Holmes Stone Meyer Boyd Mills Warren Fox
Rose Rice Schmidt Hunter Freeman Dunn Hawkins Arnold Pierce Hansen Wagner Spencer Snyder Mason Andrews Tucker Grant
Porter Burns Crawford Shaw Dixon Elliott Gordon Payne Weaver Daniels Hoffman Lynch Webb Olson Carroll Duncan Riley
Berry Little Banks Willis Fuller Ray Watkins Austin Lane Knight Stephens Carpenter Hudson Matthews Wheeler Chapman
Oliver Montgomery Richards Williamson Johnston Hart Peters Cunningham Hicks Bradley Lawrence Ryan Fields Gilbert Burke
Day Harper Washington Barrett Lucas Garrett Perkins Dean Jacobs Fowler Hanson Holland George Craig McCoy Bishop
Hopkins Weber Howell Lowe Caldwell Lambert Newman Saunders Hale Hampton Douglas Ingram Lyons Moran Norris Frazier
Harvey Holt Keller Lowery Mack Patrick Fletcher Gardner Mann Morton Barber Barker Bates Beck Chandler Douglass Glover
Harmon Higgins Hogan Hubbard Jennings Klein McGee Pope Reeves Rowe Sutton Bowman Burton Cobb Conner Floyd Goodman
Hardy Hodges Lindsey Mathis McCarthy McKinney Medlin Nash Osborne Pratt Quinn Rhodes Sharp Sims Stokes Swanson
Thornton Townsend Vaughn Walsh Watts Wolfe Bowen Bush Christensen Cummings Erickson Gross Haynes Horton Jensen Kelley
Logan McBride McLaughlin Mueller Nichols Norton Pittman Reid Sherman Steele Summers Todd Underwood Wade Wolf Abbott
Atkins Ayers Ball Beasley Benson Blackwell Blair Boone Bowers Boyle Brewer Bridges Briley Buchanan Burgess Byrd Cannon
Carlson Carr Case Christian Clarke Cochran Collier Combs Conrad Copeland Cross Curry Dalton Davidson Dawson Delaney
Dickson Dillon Dorsey Doyle Drake Duffy Dyer Eaton English Erwin Farmer Farrell Ferguson Finch Fitzgerald Flowers
Flynn Forbes Franklin Frank Gaines Gallagher Gates Gentry Gill Goodwin Graves Greer Guthrie Hahn Hammond Hancock
Hardin Harrell Hartman Hatfield Hendricks Hensley Hess Hines Hobbs Hodge Holloway Hood Hooper Horne Houston Huff Hull
Humphrey Hurst Jacobson Jarvis Joyce Kane Kemp Kerr Kidd Kirk Kirkland Knapp Koch Lamb Lang Larson Leach Leonard
Lester Lloyd Love Lutz Lynn Maddox Malone Manning Marsh Massey Maxwell May McCall McClain McConnell McCormick McDaniel
McDowell McFarland McGuire McIntosh McKay McKenzie McLean McMillan McNeil Mercer Merritt Michael Middleton Miles
Monroe Moody Moss Mullins Nolan Odom Pace Page Parks Parrish Parsons Pate Patton Pearson Pennington Phelps Pickett
Pollard Potter Preston Pruitt Ramsey Randall Ratliff Reese Rich Richmond Riggs Rivers Roach Robbins Rollins Roth
Rowland Rush Sanford Savage Sawyer Schultz Schwartz Sellers Sexton Shannon Shelton Shepherd Short Singleton Skinner
Slater Sloan Small Snow Solomon Sparks Stafford Stanley Stark Stein Strickland Strong Tate Terrell Terry Tillman Tyler
Vance Vincent Walls Walton Ware Warner Waters Weeks Welch Whitaker Whitehead Whitley Wilcox Wilder Wiley Wilkerson
Wilkins Winters Wise Witt Woodard Woods Workman Wyatt Yates York Zimmerman Acker Ackerman Albright Aldridge Alford
Allison Ambrose Ames Archer Ash Ashley Avery Babcock Bacon Bader Baird Baldwin Ballard Barlow Barnett Barr Barron
Barton Bass Bauer Baxter Beach Beard Beatty Becker Bentley Berg Bernard Best Bird Blackburn Blake Blanton Bolton Bond
Booker Booth Bowling Boyer Bradford Bradshaw Brady Bray Brennan Britt Browning Bruce Bryan Buck Buckley Bullock Burch
Burnett Burris Byers Cain Callahan Calhoun Cameron Carey Carney Carson Carver Casey Cash Chambers Chaney Childers
Church Clay Clayton Clements Cline Coffey Compton Conley Connolly Cooley Corbett Cotton Cowan Crane Crosby Crowley
Cullen Cummins Dale Daugherty Davenport Decker Dennis Dewitt Dodson Dolan Donaldson Donovan Dougherty Downs Dudley
Duke Dunlap Durham Easley Eckert Elder Emerson Estes Everett Ewing Farley Faulkner Felton Fenton Finley Fischer
Fleming Foley Forrest Fountain Fry Fulton Gamble Gay Gibbs Gilmore Glass Glenn Golden Good Gould Grady Gregory
Griffith Grimes Gunn Hager Haley Haney Hanna Harding Harrington Hartley Haskins Hawk Hays Head Heath Hebert Henry
Herman Hickman Hinton Hoover Hope Hopper House Houck Howe Huber Huffman Hurley Hutchinson Hyde Irwin Jarrett Jefferson
Joyner Justice Kaufman Keith Kendall Kent Kerns Key Kimball Kinney Kirby Kline Knox Koehler Kramer Lacey Landry
Langley Larkin Lawson Layton Lee Lehman Levy Lindsay Livingston Lockhart Lott Lowry Lyle Mabry Macdonald Madden
Mahoney Marks Mathews McAllister McCann McCarty McClure McCray McCullough McGowan McGrath McHugh McKee McKnight
McMahon McNally McNamara Meadows Melton Merrill Metcalf Meyers Milligan Mohr Moon Moreland Morrow Moser Mosley Moyer
Mullen Munson Nance Neal Newsome Newton Noble Norman Nunn Oakley Orr Osborn Overton Owen Padgett Painter Paxton Peck
Pendleton Penn Petty Pierson Pike Pitts Poe Polk Pool Poole Powers Prince Pruett Pugh Purcell Rader Rankin Redmond
Reilly Rhoades Riddle Ritter Roark Rodgers Rooney Roper Rountree Rowan Royal Rucker Rudd Russo Rutherford Ryder
Sampson Sargent Satterfield Saylor Schaefer Schneider Schroeder Scruggs Seay Sears Settle Sharpe Shea Shields Shipley
Shoemaker Shore Sikes Simms Simpson Sizemore Slaughter Snead Sparrow Speer Spivey Spruill Stanton Starr Staton
Stephenson Stockton Stout Stroud Stuart Sumner Swain Swann Sweeney Talley Tanner Teague Thacker Tidwell Toler Trent
Trimble Truitt Tubbs Tuttle Upton Vick Waddell Walden Waller Walters Weathers Webster Whitfield Whitlock Whitman
Wicker Wilburn Willard Wills Wimberly Winn Womack Woodall Woodruff Worley Wynn Yancey Yeager Yoder Youngblood Zeller""".split()
W_HISP_LAST = """Rodríguez García Martínez Hernández Pérez González Ramírez Sánchez Díaz Gómez Torres Cruz Reyes
Morales Ortiz Gutiérrez Jiménez Ruiz Álvarez Castillo Romero Vargas Herrera Mendoza Moreno Castro Rivera Flores Ramos
Chávez Vásquez Delgado Peña Guerrero Rojas Santos Valdez Mejía Soto Núñez Marte Rosario Feliz Batista Polanco Cabrera
Tavárez Encarnación Abreu Almonte Beltré Liriano Santana Mercedes Paulino Tejada Peralta Arias Alcántara Brito Frías
Germán Javier Montás Ozuna Rondón Severino Taveras Ventura Acosta Acevedo Aguilar Alvarado Aponte Arroyo Ávila Báez
Benítez Bermúdez Bonilla Bravo Bueno Calderón Camacho Campos Cano Carrasco Carrillo Cedeño Cepeda Cisneros Colón
Contreras Cordero Correa Cortés Cuevas Durán Escobar Espinal Espinoza Estévez Estrada Fajardo Fermín Fernández
Figueroa Franco Fuentes Galván Gil Guzmán Ibarra Lara León Linares Lugo Luna Machado Maldonado Marín Márquez Mateo
Medina Mena Mesa Miranda Molina Montero Mora Morel Muñoz Navarro Nieves Ochoa Ogando Olivares Orozco Ortega Pacheco
Padilla Paredes Pimentel Pineda Quintero Quiñones Ríos Rivas Robles Rosa Rubio Salas Salazar Salcedo Sandoval Santiago
Serrano Sierra Silva Solano Solís Sosa Suárez Tapia Toribio Tovar Trujillo Urías Valencia Valenzuela Vega Velásquez
Vera Villa Villalobos Villanueva Vizcaíno Zambrano Zapata Zamora Adames Alfaro Andújar Aquino Aracena Baldera Bautista
Belén Betances Bisonó Blanco Burgos Cáceres Camilo Candelario Cardona Carmona Casilla Castellanos Castaño Cid
Concepción Crespo Cueto Duarte Echevarría Estrella Familia Fabián Florián Gálvez Garabito Genao Gonell Guante Guerra
Henríquez Hidalgo Inoa Jáquez Laureano Lebrón Lorenzo Luciano Manzanillo Matos Mazara Mieses Minaya Mojica Mondesí
Montilla Nolasco Olivo Pantaleón Payano Peguero Perdomo Pichardo Quezada Rijo Rincón Sáez Sención Soriano Tolentino
Ubiera Ureña Uceta Valera Vidal Vílchez Yépez Zabala""".split()
W_US_FIRST = """Michael Matt Chris Josh Jake Ryan Tyler Nick Andrew Daniel Brandon David James John Zach Justin Will
Anthony Kevin Kyle Alex Austin Jordan Cody Eric Ben Aaron Sam Dylan Steven Brian Tim Nathan Adam Patrick Sean Jason
Cameron Jeremy Mark Stephen Jesse Travis Jeff Ethan Caleb Jared Logan Hunter Trevor Bryan Evan Paul Taylor Connor
Dustin Noah Devin Gabe Ian Nate Greg Derek Corey Scott Bradley Marcus Blake Garrett Luke Shawn Peter Seth Mitch Shane
Spencer Wes Lucas Jack Brett Mason Isaac Colton Eli Chase Dalton Tanner Grant Carson Cole Riley Parker Brady Bryce Max
Owen Joey Danny Tommy Jimmy Bobby Johnny Charlie Andy Joe Tony Rob Jon Pat Steve Tom Dan Ricky Willie Robbie Kenny
Darius Malik Jalen Terrell Darnell Andre Xavier Isaiah Elijah Jaylen Dominic Trent Wade Clay Colin Brendan Brent Chad
Craig Dane Dawson Gavin Grady Griffin Hayden Jace Jackson Jacob Jarrett Jay Joel Jonah Kade Kaleb Keegan Keith Kellen
Kody Lance Landon Lane Micah Mike Nolan Pierce Preston Quinn Reed Reese Sawyer Todd Troy Ty Tristan Walker Wyatt Zane
Alec Beau Bennett Brooks Cade Carter Casey Clayton Cooper Curtis Drew Easton Everett Garrison Graham Harrison Heath
Hudson Jaxon Jensen Kai Keaton Lawson Levi Mack Myles Nash Otto Reid Rhett Rowan Ryder Silas Stone Tate Tucker Wilson
Zack Adrian Alan Albert Allen Arthur Billy Blaine Bo Brad Brody Bruce Calvin Carl Chance Cory Dallas Dean Dennis Denny
Don Doug Dwayne Ed Frank Gary Gene Glenn Gordon Hank Harold Jerry Jim Larry Lee Leo Louis Marty Matthew Mickey Neil
Ollie Perry Phil Ray Rex Rick Rodney Ron Roy Russ Sonny Stan Terry Vince Walt Wally""".split()
W_HISP_FIRST = """José Luis Juan Carlos Jesús Miguel Ángel Francisco Pedro Rafael Manuel Jorge Antonio Ramón Wilmer
Yeison Brayan Darwin Anderson Elvis Edwin Freddy Nelson Ronny Yohan Wander Jeison Johan Eury Eudy Robinson Starlin
Jean Jhonny Leonel Héctor Julio Mario Ricardo Roberto Sergio Víctor Óscar Omar Pablo Raúl Rubén Samuel Santiago Tomás
Andrés Alejandro Alexis Ariel Armando Cristian Diego Emilio Enrique Ezequiel Fernando Gabriel Geraldo Gilberto
Gregorio Humberto Ignacio Iván Jairo Javier Joel Jonathan Leonardo Marcos Moisés Néstor Orlando Ramiro Reinaldo
Rodolfo Rolando Ulises Yunior Aníbal Adolfo Alberto Brailyn Deivy Dilson Engel Erick Esteban Eugenio Félix Frankely
Gerson Harold Isaac Jefferson Jeremy Joander Jordany Keury Kelvin Leody Luisangel Maikel Melvin Noelvi Osmar Rafelin
Rangel Richard Rony Wilfredo Wilson Wilyer Yairo Yasmil Yerlin Yoel Yonathan Yordy""".split()
W_CU_FIRST = """Yoel Yunior Lázaro Osvaldo Dariel Raidel Yoandy Adrián Jorge Yasser Dayron Yoelvis Yusniel Alain
Yordanys Yanier Dairon Osmel Yanko Reinier""".split()
W_JP_FIRST = """Haruki Kenta Shota Takumi Yuto Ryosuke Daichi Kazuya Masato Seiya Tomoya Kosuke Yuki Hiroto Sota Kaito
Ren Yamato Keita Naoki""".split()
W_JP_LAST = """Sato Takahashi Tanaka Watanabe Ito Nakamura Kobayashi Kato Yamamoto Yoshida Yamada Sasaki Yamaguchi
Matsumoto Inoue Kimura Hayashi Shimizu Yamazaki Mori Ikeda Hashimoto Ishikawa Ogawa Okada Goto Fujimoto Kondo Sakamoto
Takeda Arakawa Nakagawa Matsuda Endo""".split()
W_KR_FIRST = """Min-jae Seung-woo Ji-hwan Dong-hyun Jae-won Sung-min Hyun-woo Joon-ho Tae-yang Young-jin Woo-jin Sang-hoon""".split()
W_KR_LAST = """Kim Lee Park Choi Jung Kang Cho Yoon Jang Lim Han Oh Seo Shin""".split()
W_CA_FIRST = """Liam Noah Owen Tyler Jordan Logan Mathieu Étienne Gabriel Félix Nicolas Alexandre Jacob Maxime Ryan Connor
Brett Cal Evan Zach""".split()
W_CA_LAST = """Tremblay Gagnon Roy Côté Bouchard Gauthier Morin Lavoie Fortin Gagné Ouellet Pelletier Bélanger Lévesque
Bergeron Leblanc Paquette Girard Beaulieu MacDonald MacLeod Fraser Campbell Robertson Henderson Stewart Murray""".split()
W_AU_FIRST = """Liam Lachlan Mitchell Jarrod Darcy Callum Hamish Riley Brodie Jye Kieran Tom""".split()
W_AU_LAST = """Kennelly Whitfield Doolan Halloran Cutler McGuire Burgess Wilkinson Harrington Moffat Pearce Kinnear""".split()
W_CW_FIRST = """Jonathan Rangel Jair Roger Xavier Darryl Gilmar Ruendel Shawn Elvis Jeremy Ronald""".split()
W_CW_LAST = """Martina Pietersz Maduro Statia Rosaria Winklaar Hooi Wernet Doran Janga Martis Isenia""".split()
# full names of well-known players of the real game, never drawn
FAMOUS = {ascii_fold(n).lower() for n in """Mike Trout|Aaron Judge|Bryce Harper|Mookie Betts|Freddie Freeman|Trea Turner|
Corey Seager|Pete Alonso|Francisco Lindor|Manny Machado|Rafael Devers|Jose Altuve|Carlos Correa|Ronald Acuna|Fernando
Tatis|Vladimir Guerrero|Juan Soto|Jose Ramirez|Yordan Alvarez|Julio Rodriguez|Bobby Witt|Kyle Tucker|Matt Olson|Austin
Riley|Paul Goldschmidt|Nolan Arenado|Marcus Semien|Christian Yelich|Kris Bryant|Anthony Rizzo|Javier Baez|Josh Donaldson|
Josh Hamilton|Ryan Howard|Ryan Braun|Matt Kemp|Adam Jones|Frank Thomas|David Wright|Alex Gordon|Chris Sale|David Price|
Adam Wainwright|Matt Carpenter|Chris Carpenter|Matt Holliday|David Freese|Andrew Miller|Trevor Bauer|Michael Brantley|
Carlos Santana|Edwin Encarnacion|Victor Martinez|Pedro Martinez|David Ortiz|Alex Rodriguez|Ivan Rodriguez|Francisco
Rodriguez|Eduardo Rodriguez|Felix Hernandez|Teoscar Hernandez|Keith Hernandez|Enrique Hernandez|Freddy Garcia|Salvador
Perez|Nelson Cruz|Gary Sanchez|Luis Castillo|Luis Severino|Jeremy Pena|Pedro Alvarez|Yadier Molina|Jose Abreu|Jose
Reyes|Jose Bautista|Jose Fernandez|Jose Berrios|Jose Quintana|Jose Iglesias|Carlos Gonzalez|Carlos Gomez|Carlos Beltran|
Carlos Delgado|Carlos Lee|Carlos Martinez|Carlos Rodon|Adrian Beltre|Adrian Gonzalez|Albert Pujols|Miguel Cabrera|
Johnny Cueto|Robinson Cano|Starlin Castro|Aramis Ramirez|Hanley Ramirez|Manny Ramirez|Dee Gordon|Joey Gallo|Josh Bell|
Kyle Seager|Kyle Schwarber|Kyle Hendricks|Kyle Lewis|Matt Chapman|Matt Harvey|Matt Cain|Jon Lester|John Lackey|Max
Fried|Chris Davis|Chris Taylor|Justin Turner|Justin Upton|Justin Verlander|Will Smith|Will Clark|Will Myers|Mike Moustakas|
Mike Napoli|Ryan Zimmerman|Ryan Mountcastle|Jacob deGrom|Jake Arrieta|Josh Hader|Bo Jackson|Reggie Jackson|Andrew
McCutchen|Andrew Benintendi|Jason Heyward|Ian Kinsler|Ian Happ|Brandon Crawford|Brandon Belt|Brandon Nimmo|Brandon
Lowe|Tim Anderson|Brett Gardner|Nick Castellanos|Nick Markakis|Daniel Murphy|Evan Longoria|Ben Zobrist|Hunter Pence|
Hunter Renfroe|Cody Bellinger|Austin Hays|Adam Duvall|Jose Altuve|Yoan Moncada|Yandy Diaz|Jorge Soler|Jorge Posada|
Luis Arraez|Luis Robert|Luis Gonzalez|Randy Arozarena|Willy Adames|Gleyber Torres|Ozzie Albies|Jurickson Profar|Didi
Gregorius|Andrelton Simmons|Kenley Jansen|Xander Bogaerts|Ha-seong Kim|Jung-ho Kang|Hyun-soo Kim|Shin-soo Choo|Seiya
Suzuki|Masataka Yoshida|Kenta Maeda|Shota Imanaga|Shohei Ohtani|Ichiro Suzuki|Hideki Matsui|Joey Votto|Larry Walker|
Justin Morneau|Russell Martin|Jason Bay|Liam Hendriks|Grant Balfour|Tommy Edman|Willson Contreras|Wilmer Flores|Wilson
Ramos|Elvis Andrus|Edwin Diaz|Edwin Rios|Oscar Gonzalez|Pablo Sandoval|Pedro Severino|Rafael Furcal|Rafael Palmeiro|
Juan Gonzalez|Juan Uribe|Juan Pierre|Jesus Aguilar|Jesus Luzardo|Miguel Tejada|Miguel Rojas|Miguel Sano|Miguel Andujar|
Ramon Laureano|Victor Robles|Victor Reyes|Jean Segura|Jonathan Villar|Jonathan India|Jonathan Lucroy|Freddy Peralta|
Starling Marte|Ketel Marte|Rafael Ortega|Robinson Chirinos|Elvis Luciano|Wander Franco|Noelvi Marte|Luisangel Acuna|
Maikel Franco|Leody Taveras|Jeison Guzman|Eury Perez|Brayan Bello|Johan Santana|Jhonny Peralta|Yohan Ramirez|Engel
Beltre|Wilyer Abreu|Yairo Munoz|Dilson Herrera|Harold Ramirez|Richard Rodriguez|Ronny Mauricio|Starlin Castro|Andres
Gimenez|Andres Torres|Andres Galarraga|Andres Chaparro|Ezequiel Duran|Ezequiel Tovar|Gabriel Moreno|Gabriel Arias|
Gilberto Celestino|Yasmani Grandal|Yuli Gurriel|Lourdes Gurriel|Aledmys Diaz|Yoenis Cespedes|Yasiel Puig|Jose Abreu""".replace(
    "\n", " ").split("|")}


def _ranked(pool, lead):
    """Weights falling with a name's rank in its pool: (rank + lead) to the power -0.8."""
    w = [(i + 1 + lead) ** -0.8 for i in range(len(pool))]
    s = sum(w)
    return [x / s for x in w]


def _clean(pool):
    """A pool with any repeat removed, order kept."""
    out, seen = [], set()
    for x in pool:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def rename_league(L, keep, r):
    """Every player outside `keep` renamed from the wider pools, keeping his origin and any generational suffix: no full
    name twice, no well-known player's name, a surname at most a dozen times (the commonest), and the designed players'
    surnames held back (a signing's surname at most once or twice more, and never with his first name or initial)."""
    first_of = lambda nm: ascii_fold(nm.replace(" Jr.", "")).split(" ", 1)[0].lower()
    last_of = lambda nm: ascii_fold(nm.replace(" Jr.", "")).split(" ", 1)[1].lower()
    used = {ascii_fold(L.players[k].name).lower() for k in keep}
    five = [k for k in ("P4", "P1", "P2", "P3", "P5") if k in keep]
    five_first = {last_of(L.players[k].name): first_of(L.players[k].name) for k in five}
    cap = {}
    for k in keep:
        cap[last_of(L.players[k].name)] = 2
    for k in five:
        cap[last_of(L.players[k].name)] = 0
    cap.update({"rivas": 1, "medina": 2})
    for staff in ("barnes", "armstrong", "wallace"):
        cap[staff] = 0
    count = {}
    pools = {}
    for nm, pool, lead in (("us_last", W_US_LAST, 40), ("hisp_last", W_HISP_LAST, 12), ("us_first", W_US_FIRST, 15),
                           ("hisp_first", W_HISP_FIRST, 12)):
        pc = _clean(pool)
        pools[nm] = (pc, _ranked(pc, lead))
    flat = lambda pool: (_clean(pool), [1.0 / len(_clean(pool))] * len(_clean(pool)))
    for nm, pool in (("cu_first", W_CU_FIRST), ("jp_first", W_JP_FIRST), ("jp_last", W_JP_LAST),
                     ("kr_first", W_KR_FIRST), ("kr_last", W_KR_LAST), ("ca_first", W_CA_FIRST), ("ca_last", W_CA_LAST),
                     ("au_first", W_AU_FIRST), ("au_last", W_AU_LAST), ("cw_first", W_CW_FIRST), ("cw_last", W_CW_LAST)):
        pools[nm] = flat(pool)
    pools["kr_last"] = (pools["kr_last"][0], _ranked(pools["kr_last"][0], 1))
    pools["jp_last"] = (pools["jp_last"][0], _ranked(pools["jp_last"][0], 4))

    def pick(nm):
        names, w = pools[nm]
        return names[int(r.choice(len(names), p=w))]

    for k in sorted((q for q in L.players if q not in keep), key=lambda q: (L.players[q].pid, q)):
        p = L.players[k]
        o = p.origin
        sfx = " Jr." if p.name.endswith(" Jr.") else ""
        for _ in range(2000):
            if o == "US":
                if r.random() < 0.09:
                    first, last = pick("hisp_first"), ascii_fold(pick("hisp_last"))
                    first = ascii_fold(first) if r.random() < 0.7 else first
                else:
                    first, last = pick("us_first"), pick("us_last")
            elif o in ("DR", "VE", "PR", "MX", "CO", "PA"):
                first, last = pick("hisp_first"), pick("hisp_last")
                if o == "PR" and r.random() < 0.4:
                    first = ascii_fold(first)
            elif o == "CU":
                first = pick("cu_first") if r.random() < 0.5 else pick("hisp_first")
                last = pick("hisp_last")
            else:
                first, last = pick(o.lower() + "_first"), pick(o.lower() + "_last")
            full = "%s %s" % (first, last)
            f, s = first_of(full), last_of(full)
            if ascii_fold(full).lower() in used or ascii_fold(full).lower() in FAMOUS:
                continue
            if count.get(s, 0) >= cap.get(s, 12):
                continue
            if s in five_first and (f == five_first[s] or f[0] == five_first[s][0]):
                continue
            if f in five_first.values() and s in five_first:
                continue
            break
        else:
            raise RuntimeError("no league name for %s" % k)
        used.add(ascii_fold(full).lower())
        count[s] = count.get(s, 0) + 1
        p.name = full + sfx
