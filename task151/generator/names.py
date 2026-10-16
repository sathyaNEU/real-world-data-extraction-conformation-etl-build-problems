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
