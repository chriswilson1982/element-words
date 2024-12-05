# coding=utf-8

import os
from bottle import Bottle, response

# List of all element symbols
ELEMENTS = {"H": "Hydrogen", "He": "Helium", "Li": "Lithium", "Be": "Beryllium", "B": "Boron", "C": "Carbon", "N": "Nitrogen", "O": "Oxygen", "F": "Fluorine", "Ne": "Neon", "Na": "Sodium", "Mg": "Magnesium", "Al": "Aluminium", "Si": "Silicon", "P": "Phosphorus", "S": "Sulfur", "Cl": "Chlorine", "Ar": "Argon", "K": "Potassium", "Ca": "Calcium", "Sc": "Scandium", "Ti": "Titanium", "V": "Vanadium", "Cr": "Chromium", "Mn": "Manganese", "Fe": "Iron", "Co": "Cobalt", "Ni": "Nickel", "Cu": "Copper", "Zn": "Zinc", "Ga": "Gallium", "Ge": "Germanium", "As": "Arsenic", "Se": "Selenium", "Br": "Bromine", "Kr": "Krypton", "Rb": "Rubidium", "Sr": "Strontium", "Y": "Yttrium", "Zr": "Zirconium", "Nb": "Niobium", "Mo": "Molybdenum", "Tc": "Technetium", "Ru": "Ruthenium", "Rh": "Rhodium", "Pd": "Palladium", "Ag": "Silver", "Cd": "Cadmium", "In": "Indium", "Sn": "Tin", "Sb": "Antimony", "Te": "Tellurium", "I": "Iodine", "Xe": "Xenon", "Cs": "Cesium", "Ba": "Barium", "La": "Lanthanum", "Ce": "Cerium", "Pr": "Praseodymium", "Nd": "Neodymium", "Pm": "Promethium", "Sm": "Samarium", "Eu": "Europium", "Gd": "Gadolinium", "Tb": "Terbium", "Dy": "Dysprosium", "Ho": "Holmium", "Er": "Erbium", "Tm": "Thulium", "Yb": "Ytterbium", "Lu": "Lutetium", "Hf": "Hafnium", "Ta": "Tantalum", "W": "Tungsten", "Re": "Rhenium", "Os": "Osmium", "Ir": "Iridium", "Pt": "Platinum", "Au": "Gold", "Hg": "Mercury", "Tl": "Thallium", "Pb": "Lead", "Bi": "Bismuth", "Po": "Polonium", "At": "Astatine", "Rn": "Radon", "Fr": "Francium", "Ra": "Radium", "Ac": "Actinium", "Th": "Thorium", "Pa": "Protactinium", "U": "Uranium", "Np": "Neptunium", "Pu": "Plutonium", "Am": "Americium", "Cm": "Curium", "Bk": "Berkelium", "Cf": "Californium", "Es": "Einsteinium", "Fm": "Fermium", "Md": "Mendelevium", "No": "Nobelium", "Lr": "Lawrencium", "Rf": "Rutherfordium", "Db": "Dubnium", "Sg": "Seaborgium", "Bh": "Bohrium", "Hs": "Hassium", "Mt": "Meitnerium", "Ds": "Darmstadtium", "Rg": "Roentgenium", "Cn": "Copernicium", "Nh": "Nihonium", "Fl": "Flerovium", "Mc": "Moscovium", "Lv": "Livermorium", "Ts": "Tennessine", "Og": "Oganesson"}
ELEMENT_SYMBOLS = ELEMENTS.keys()

# Create Bottle app
app = Bottle()

# INDEX
@app.get('/')
def index():
    response.content_type = "text/html; charset=UTF8"
    return "<div style='font-family: sans-serif'><h1>Welcome to Element Words!</h1><p>Use the endpoint <strong>/word/&lt;input-word&gt;</strong> to find all solutions for constructing the word from the symbols of the chemical elements.</p></div>"

@app.get('/elements')
def elements():
    response.content_type = "application/json; charset=UTF8"
    return {
        "elements" : ELEMENTS
    }

@app.get('/symbols')
def symbols():
    response.content_type = "application/json; charset=UTF8"
    return {
        "symbols" : ELEMENT_SYMBOLS
    }

@app.get('/word/<word>')
def process_word(word):
    combinations = find_combinations(word)
    response.content_type = "application/json; charset=UTF8"
    if combinations:
        count = len(combinations)
        sorted_results = sorted(combinations, key=lambda n: len(n[1]))
        return {
            "word" : word.lower(),
            "solutions" : list(map(lambda result: {"text": result[0], "symbols": result[1], "elements": [ELEMENTS[x] for x in result[1]]}, sorted_results))
        }
    else:
        return {
            "word" : word.lower(),
            "solutions" : []
        }

def find_combinations(word, path="", symbols=[]):
    """
    Recursive function to find valid combinations of symbols forming the word.
    Returns a list of tuples, where each tuple contains:
      - A string representation of the solution.
      - A list of element symbols used to form the solution.
    """
    if not word:  # Base case: if the word is empty, return the path and symbols
        return [(path, tuple(symbols))]

    results = set()
    # Try 1 or 2 character substrings of the word
    for i in range(1, 3):
        # Get the next 1 or 2 letters, capitalized
        prefix = word[:i].capitalize()
        if prefix in ELEMENT_SYMBOLS:  # Check if it's a valid element symbol
            results.update(find_combinations(
                word[i:], path + prefix, symbols + [prefix]))

    return results

# Run app
if os.environ.get('APP_LOCATION') == 'heroku':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
else:
    app.run(host='localhost', port=8080, debug=True)
