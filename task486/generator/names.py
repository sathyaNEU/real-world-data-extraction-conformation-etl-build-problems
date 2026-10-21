"""Name frequency lists for the internal identities (never shipped): Hispanic surnames weighted by the 2010
census counts (thousands) for the top of the list, the tail from faker's es_MX list at a small flat weight;
first names by rough U.S. frequency within Hispanic men and women; other names from faker's en_US weights."""
import numpy as np
from faker.providers.person.en_US import Provider as P
from faker.providers.person.es_MX import Provider as M

HS = {"Garcia": 1166, "Rodriguez": 1095, "Martinez": 1060, "Hernandez": 1043, "Lopez": 874, "Gonzalez": 841,
      "Perez": 681, "Sanchez": 612, "Ramirez": 557, "Torres": 437, "Flores": 433, "Rivera": 420, "Gomez": 387,
      "Diaz": 374, "Reyes": 331, "Morales": 330, "Cruz": 273, "Ortiz": 263, "Gutierrez": 268, "Chavez": 249,
      "Ramos": 233, "Ruiz": 225, "Alvarez": 217, "Mendoza": 213, "Castillo": 202, "Jimenez": 202, "Vasquez": 188,
      "Moreno": 196, "Herrera": 195, "Medina": 182, "Aguilar": 177, "Vargas": 174, "Guzman": 154, "Mendez": 150,
      "Castro": 155, "Romero": 168, "Fernandez": 140, "Munoz": 139, "Rojas": 87, "Soto": 136, "Delgado": 124,
      "Contreras": 119, "Salazar": 118, "Guerrero": 111, "Rios": 111, "Estrada": 105, "Ortega": 117, "Nunez": 92,
      "Dominguez": 104, "Sandoval": 102, "Juarez": 96, "Avila": 88, "Espinoza": 92, "Acosta": 98, "Silva": 101,
      "Valdez": 98, "Padilla": 86, "Cervantes": 73, "Campos": 85, "Vega": 87, "Rosales": 70, "Figueroa": 75,
      "Fuentes": 70, "Cortez": 71, "Navarro": 73, "Carrillo": 70, "Pacheco": 62, "Molina": 81, "Marquez": 78,
      "Ibarra": 59, "Salinas": 64, "Trujillo": 59, "Velasquez": 66, "Aguirre": 62, "Rangel": 49, "Lara": 61,
      "Valencia": 52, "Montoya": 55, "Calderon": 51, "Cabrera": 54, "Solis": 56, "Miranda": 62, "Leon": 61,
      "Nava": 40, "Zamora": 46, "Galvan": 44, "Ochoa": 49, "Robles": 54, "Duran": 61, "Villarreal": 49}
HM = {"Jose": 60, "Juan": 40, "Luis": 30, "Carlos": 28, "Jesus": 24, "Jorge": 20, "Miguel": 22, "Francisco": 18,
      "Antonio": 17, "Manuel": 15, "Pedro": 12, "Alejandro": 14, "Ricardo": 12, "Roberto": 12, "Javier": 13,
      "Fernando": 10, "Daniel": 14, "Mario": 10, "Rafael": 9, "Eduardo": 10, "Sergio": 9, "Raul": 9, "Ramon": 8,
      "Victor": 9, "Martin": 9, "Oscar": 9, "Arturo": 7, "Hector": 8, "Alberto": 7, "Jaime": 6, "Guillermo": 6,
      "Armando": 6, "Ruben": 6, "Enrique": 6, "Gerardo": 6, "Salvador": 5, "Rogelio": 4, "Pablo": 5,
      "Alfredo": 5, "Andres": 5, "Angel": 9, "David": 10, "Julio": 6, "Israel": 4, "Adrian": 6, "Gabriel": 6,
      "Marco": 4, "Cesar": 5, "Ernesto": 4, "Felipe": 4, "Gustavo": 4, "Hugo": 3, "Ivan": 4, "Lorenzo": 3,
      "Mauricio": 3, "Ignacio": 3, "Santiago": 3, "Agustin": 2, "Benjamin": 3, "Cristian": 4, "Diego": 4}
HF = {"Maria": 55, "Guadalupe": 14, "Rosa": 12, "Ana": 13, "Juana": 8, "Patricia": 10, "Carmen": 9,
      "Elizabeth": 10, "Laura": 9, "Martha": 8, "Teresa": 7, "Leticia": 6, "Veronica": 7, "Silvia": 6, "Alicia": 6,
      "Gloria": 5, "Adriana": 7, "Margarita": 6, "Claudia": 7, "Yolanda": 5, "Sandra": 6, "Isabel": 5, "Lucia": 4,
      "Angelica": 5, "Norma": 5, "Elena": 4, "Monica": 6, "Gabriela": 6, "Josefina": 3, "Irma": 3, "Blanca": 4,
      "Sofia": 4, "Diana": 5, "Erika": 4, "Graciela": 3, "Alejandra": 5, "Cristina": 4, "Beatriz": 3, "Esther": 3,
      "Lorena": 3, "Jessica": 6, "Vanessa": 4, "Daniela": 4, "Karina": 3, "Brenda": 4, "Marisol": 3, "Yesenia": 3,
      "Rocio": 2, "Araceli": 2, "Raquel": 3, "Lourdes": 2, "Dolores": 3, "Esperanza": 2, "Consuelo": 2}


def _w(d, tail=(), tw=0.0):
    names = list(d) + [t for t in tail if t not in d]
    w = np.array([float(d[n]) for n in d] + [tw] * (len(names) - len(d)))
    return names, w / w.sum()


HISP_LAST = _w(HS, tuple(dict.fromkeys(M.last_names)), 6.0)
HISP_MALE = _w(HM)
HISP_FEMALE = _w(HF)
OTHER_LAST = (list(P.last_names), np.array(list(P.last_names.values()), float) / sum(P.last_names.values()))
OTHER_MALE = (list(P.first_names_male), np.array(list(P.first_names_male.values()), float) / sum(P.first_names_male.values()))
OTHER_FEMALE = (list(P.first_names_female), np.array(list(P.first_names_female.values()), float) / sum(P.first_names_female.values()))
