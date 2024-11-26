# coding=utf-8

import os
from bottle import Bottle

# List of all element symbols
ELEMENT_SYMBOLS = [
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe", "Cs", "Ba", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr"
]

# Create Bottle app
app = Bottle()

# INDEX


@app.get('/')
def index():
    return "Welcome to Element Words!"


@app.get('/word/<response_type>/<word>')
def process_word(response_type, word):
    combinations = find_combinations(word)
    if combinations:
        count = len(combinations)
        sorted_results = sorted(combinations, key=lambda n: len(n[1]))
        if response_type == "text":
            summary = f"{count} solution{'' if count == 1 else 's'} using element symbols:"
            solutions = ""
            for solution, symbols in sorted_results:
                two_char_symbols = map(lambda x: x if len(
                    x) == 2 else x + " ", symbols)
                solutions += "<br />- ".join(two_char_symbols)
            return summary + "<br />" + solutions
        elif response_type == "json":
            return { 
                "word" : word.lower(),
                "solutions" : map(lambda result: {"text": result[0], "array": result[1] }, sorted_results)
                }
        else:
            return "Unrecognised response type."

    else:
        return "No solution found."


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
