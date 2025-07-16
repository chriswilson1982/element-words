# coding=utf-8

import os
import json
import yaml
from datetime import datetime
from bottle import Bottle, response, request, abort

# List of all element symbols
ELEMENTS = {"H": "Hydrogen", "He": "Helium", "Li": "Lithium", "Be": "Beryllium", "B": "Boron", "C": "Carbon", "N": "Nitrogen", "O": "Oxygen", "F": "Fluorine", "Ne": "Neon", "Na": "Sodium", "Mg": "Magnesium", "Al": "Aluminium", "Si": "Silicon", "P": "Phosphorus", "S": "Sulfur", "Cl": "Chlorine", "Ar": "Argon", "K": "Potassium", "Ca": "Calcium", "Sc": "Scandium", "Ti": "Titanium", "V": "Vanadium", "Cr": "Chromium", "Mn": "Manganese", "Fe": "Iron", "Co": "Cobalt", "Ni": "Nickel", "Cu": "Copper", "Zn": "Zinc", "Ga": "Gallium", "Ge": "Germanium", "As": "Arsenic", "Se": "Selenium", "Br": "Bromine", "Kr": "Krypton", "Rb": "Rubidium", "Sr": "Strontium", "Y": "Yttrium", "Zr": "Zirconium", "Nb": "Niobium", "Mo": "Molybdenum", "Tc": "Technetium", "Ru": "Ruthenium", "Rh": "Rhodium", "Pd": "Palladium", "Ag": "Silver", "Cd": "Cadmium", "In": "Indium", "Sn": "Tin", "Sb": "Antimony", "Te": "Tellurium", "I": "Iodine", "Xe": "Xenon", "Cs": "Cesium", "Ba": "Barium", "La": "Lanthanum", "Ce": "Cerium", "Pr": "Praseodymium", "Nd": "Neodymium", "Pm": "Promethium", "Sm": "Samarium", "Eu": "Europium", "Gd": "Gadolinium", "Tb": "Terbium", "Dy": "Dysprosium", "Ho": "Holmium", "Er": "Erbium", "Tm": "Thulium", "Yb": "Ytterbium", "Lu": "Lutetium", "Hf": "Hafnium", "Ta": "Tantalum", "W": "Tungsten", "Re": "Rhenium", "Os": "Osmium", "Ir": "Iridium", "Pt": "Platinum", "Au": "Gold", "Hg": "Mercury", "Tl": "Thallium", "Pb": "Lead", "Bi": "Bismuth", "Po": "Polonium", "At": "Astatine", "Rn": "Radon", "Fr": "Francium", "Ra": "Radium", "Ac": "Actinium", "Th": "Thorium", "Pa": "Protactinium", "U": "Uranium", "Np": "Neptunium", "Pu": "Plutonium", "Am": "Americium", "Cm": "Curium", "Bk": "Berkelium", "Cf": "Californium", "Es": "Einsteinium", "Fm": "Fermium", "Md": "Mendelevium", "No": "Nobelium", "Lr": "Lawrencium", "Rf": "Rutherfordium", "Db": "Dubnium", "Sg": "Seaborgium", "Bh": "Bohrium", "Hs": "Hassium", "Mt": "Meitnerium", "Ds": "Darmstadtium", "Rg": "Roentgenium", "Cn": "Copernicium", "Nh": "Nihonium", "Fl": "Flerovium", "Mc": "Moscovium", "Lv": "Livermorium", "Ts": "Tennessine", "Og": "Oganesson"}
ELEMENT_SYMBOLS = list(ELEMENTS.keys())

# Create Bottle app
app = Bottle()

# Constants
API_VERSION = "v1"
MAX_WORD_LENGTH = 50

# Helper functions
def create_error_response(code, message, details=None):
    """Create standardized error response"""
    error_response = {
        "error": {
            "code": code,
            "message": message,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    }
    if details:
        error_response["error"]["details"] = details
    return error_response

def create_success_response(data, meta=None):
    """Create standardized success response"""
    success_response = {
        "data": data,
        "meta": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": API_VERSION
        }
    }
    if meta:
        success_response["meta"].update(meta)
    return success_response

def set_cors_headers():
    """Set CORS headers for all responses"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'

def set_json_headers():
    """Set standard JSON response headers"""
    response.content_type = "application/json; charset=UTF-8"
    set_cors_headers()

def get_available_symbols(reverse_symbols=False):
    """Get list of available element symbols, optionally including reversed"""
    if not reverse_symbols:
        return ELEMENT_SYMBOLS
    
    # Create list with both normal and reversed two-letter symbols
    symbols = list(ELEMENT_SYMBOLS)  # Start with all normal symbols
    for symbol in ELEMENT_SYMBOLS:
        if len(symbol) == 2:
            reversed_symbol = symbol[::-1]
            # Only add if it's not the same as the original (prevents duplicates)
            if reversed_symbol != symbol:
                symbols.append(reversed_symbol)
    return symbols

@app.hook('after_request')
def enable_cors():
    """Enable CORS for all responses"""
    set_cors_headers()

@app.route('/api/<version>/options', method='OPTIONS')
@app.route('/api/<version>/<path:path>', method='OPTIONS')
def handle_options(version=None, path=None):
    """Handle preflight OPTIONS requests"""
    set_cors_headers()
    return {}

# API Documentation endpoint
@app.get('/')
@app.get('/api')
def api_documentation():
    """API documentation and available endpoints"""
    response.content_type = "text/html; charset=UTF-8"
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Element Words API</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            h1 { color: #2d3748; }
            h2 { color: #4a5568; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }
            .endpoint { background: #f7fafc; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 4px solid #3182ce; }
            .method { background: #3182ce; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px; }
            .url { font-family: monospace; background: #edf2f7; padding: 2px 6px; border-radius: 4px; }
            .params { background: #fff5f5; border: 1px solid #fed7d7; padding: 10px; border-radius: 4px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1>Element Words API v1</h1>
        <p>A RESTful API for creating words from chemical element symbols.</p>
        
        <h2>Base URL</h2>
        <p><code>/api/v1</code></p>
        
        <h2>Endpoints</h2>
        
        <div class="endpoint">
            <p><span class="method">GET</span> <span class="url">/api/v1/words/{word}/combinations</span></p>
            <p><strong>Primary endpoint:</strong> Find all possible element combinations for a word</p>
            <div class="params">
                <strong>Path Parameters:</strong><br>
                • <code>word</code>: The word to analyze (max 50 characters, alphabetic only)<br><br>
                <strong>Query Parameters:</strong><br>
                • <code>allow_reversed_symbols</code> (optional): Set to "true" to allow both normal and reversed two-letter element symbols (He+eH, Li+iL, etc.)
            </div>
        </div>
        
        <div class="endpoint">
            <p><span class="method">GET</span> <span class="url">/api/v1/elements</span></p>
            <p>Get all chemical elements (reference data)</p>
        </div>
        
        <div class="endpoint">
            <p><span class="method">GET</span> <span class="url">/api/v1/elements/{symbol}</span></p>
            <p>Get a specific element by symbol</p>
        </div>
        
        <div class="endpoint">
            <p><span class="method">GET</span> <span class="url">/api/v1/openapi.yaml</span></p>
            <p>Get OpenAPI specification in YAML format</p>
        </div>
        
        <div class="endpoint">
            <p><span class="method">GET</span> <span class="url">/api/v1/openapi.json</span></p>
            <p>Get OpenAPI specification in JSON format</p>
        </div>
        
        <div class="endpoint">
            <p><span class="method">GET</span> <span class="url">/api/v1/docs</span></p>
            <p><strong>Interactive API documentation:</strong> Swagger UI interface</p>
        </div>
        
        <h2>Examples</h2>
        <ul>
            <li><code>GET /api/v1/words/hero/combinations</code> → H-Er-O</li>
            <li><code>GET /api/v1/words/hero/combinations?allow_reversed_symbols=true</code> → Use both normal and reversed symbols (He+eH, etc.)</li>
        </ul>
        
        <h2>Response Format</h2>
        <pre>{
  "data": { ... },
  "meta": {
    "timestamp": "2023-01-01T00:00:00Z",
    "version": "v1"
  }
}</pre>
        
        <h2>Error Format</h2>
        <pre>{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message",
    "timestamp": "2023-01-01T00:00:00Z"
  }
}</pre>
        
        <p><a href="https://github.com/chriswilson1982/element-words">GitHub Repository</a></p>
    </body>
    </html>
    """

# Get all elements (simple list, no pagination needed)
@app.get('/api/v1/elements')
def get_elements():
    """Get all chemical elements"""
    set_json_headers()
    
    elements_data = []
    for symbol, name in ELEMENTS.items():
        elements_data.append({
            "symbol": symbol,
            "name": name,
            "atomic_number": ELEMENT_SYMBOLS.index(symbol) + 1
        })
    
    meta = {"total_count": len(elements_data)}
    return create_success_response(elements_data, meta)

# Get specific element by symbol
@app.get('/api/v1/elements/<symbol>')
def get_element(symbol):
    """Get a specific element by symbol"""
    set_json_headers()
    
    symbol = symbol.strip().capitalize()
    
    if not symbol:
        response.status = 400
        return create_error_response("MISSING_SYMBOL", "Element symbol is required")
    
    if symbol not in ELEMENTS:
        response.status = 404
        return create_error_response("ELEMENT_NOT_FOUND", f"Element with symbol '{symbol}' not found")
    
    element_data = {
        "symbol": symbol,
        "name": ELEMENTS[symbol],
        "atomic_number": ELEMENT_SYMBOLS.index(symbol) + 1
    }
    
    return create_success_response(element_data)

# Find word combinations - the main API purpose
@app.get('/api/v1/words/<word>/combinations')
def get_word_combinations(word):
    """Find all possible element combinations for a word"""
    set_json_headers()
    
    # Input validation
    if not word:
        response.status = 400
        return create_error_response("MISSING_WORD", "Word parameter is required")
    
    # Check for reverse symbols option
    reverse_symbols = request.query.get('allow_reversed_symbols', '').lower() == 'true'
    
    # Sanitize input: remove non-alphabetic characters
    clean_word = ''.join(c for c in word if c.isalpha())
    if not clean_word:
        response.status = 400
        return create_error_response("INVALID_WORD", "Word must contain at least one alphabetic character")
    
    # Limit word length to prevent DoS attacks
    if len(clean_word) > MAX_WORD_LENGTH:
        response.status = 400
        return create_error_response("WORD_TOO_LONG", f"Word length exceeds maximum limit of {MAX_WORD_LENGTH} characters")
    
    try:
        combinations = find_combinations(clean_word, reverse_symbols=reverse_symbols)
        
        # Format solutions
        solutions = []
        for text_repr, symbols_tuple in combinations:
            # Map symbols back to original (non-reversed) symbols for element data
            # and track which symbols were reversed
            elements_data = []
            for symbol in symbols_tuple:
                is_reversed = False
                if reverse_symbols and len(symbol) == 2:
                    # Check if this symbol is a reversed version
                    original_symbol = symbol[::-1] if symbol[::-1] in ELEMENTS else symbol
                    is_reversed = (symbol[::-1] in ELEMENTS and symbol[::-1] != symbol)
                else:
                    original_symbol = symbol
                
                elements_data.append({
                    "symbol": original_symbol,
                    "name": ELEMENTS[original_symbol],
                    "atomic_number": ELEMENT_SYMBOLS.index(original_symbol) + 1,
                    "reversed": is_reversed
                })
            
            solution = {
                "representation": text_repr,
                "symbols": list(symbols_tuple),
                "elements": elements_data
            }
            solutions.append(solution)
        
        # Sort by number of elements used (fewer elements first)
        solutions.sort(key=lambda x: len(x['symbols']))
        
        meta = {}
        if reverse_symbols:
            meta["allow_reversed_symbols"] = True
        
        word_data = {
            "input_word": clean_word.lower(),
            "solutions": solutions
        }
        
        return create_success_response(word_data, meta)
        
    except Exception as e:
        response.status = 500
        return create_error_response("PROCESSING_ERROR", "Error processing word combinations")

def find_combinations(word, path="", symbols=None, reverse_symbols=False):
    """
    Recursive function to find valid combinations of symbols forming the word.
    Returns a list of tuples, where each tuple contains:
      - A string representation of the solution.
      - A tuple of element symbols used to form the solution.
    """
    if symbols is None:
        symbols = []
    
    if not word:  # Base case: if the word is empty, return the path and symbols
        return [(path, tuple(symbols))]

    results = []
    seen = set()  # Track unique combinations to avoid duplicates
    
    # Get the appropriate symbol set (normal or reversed)
    available_symbols = get_available_symbols(reverse_symbols)
    
    # Try 1 or 2 character substrings of the word
    for i in range(1, min(3, len(word) + 1)):
        # Get the next 1 or 2 letters
        substring = word[:i]
        
        # For reversed symbols, we need to try different cases to match symbols like "eH"
        if reverse_symbols:
            # Try all possible case variations for the substring
            case_variations = [
                substring,  # as-is: "eh"
                substring.capitalize(),  # capitalize: "Eh" 
                substring.upper(),  # upper: "EH"
            ]
            
            # For 2-letter substrings, also try with second letter capitalized
            if len(substring) == 2:
                case_variations.append(substring[0].lower() + substring[1].upper())  # "eH"
            
            for variation in case_variations:
                if variation in available_symbols:
                    sub_results = find_combinations(
                        word[i:], path + variation, symbols + [variation], reverse_symbols)
                    for result in sub_results:
                        if result not in seen:
                            seen.add(result)
                            results.append(result)
        else:
            # Standard behavior: capitalize the prefix
            prefix = substring.capitalize()
            if prefix in available_symbols:
                sub_results = find_combinations(
                    word[i:], path + prefix, symbols + [prefix], reverse_symbols)
                for result in sub_results:
                    if result not in seen:
                        seen.add(result)
                        results.append(result)

    return results

# OpenAPI Specification endpoints
@app.get('/api/v1/openapi.yaml')
def get_openapi_yaml():
    """Serve OpenAPI specification in YAML format"""
    try:
        with open('openapi.yaml', 'r') as f:
            spec_content = f.read()
        response.content_type = "application/x-yaml"
        set_cors_headers()
        return spec_content
    except FileNotFoundError:
        response.status = 404
        set_json_headers()
        return create_error_response("NOT_FOUND", "OpenAPI specification not found")

@app.get('/api/v1/openapi.json')
def get_openapi_json():
    """Serve OpenAPI specification in JSON format"""
    try:
        with open('openapi.json', 'r') as f:
            spec_data = json.load(f)
        set_json_headers()
        return spec_data
    except FileNotFoundError:
        response.status = 404
        set_json_headers()
        return create_error_response("NOT_FOUND", "OpenAPI specification not found")

@app.get('/api/v1/docs')
def swagger_ui():
    """Serve Swagger UI for interactive API documentation"""
    response.content_type = "text/html; charset=UTF-8"
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Element Words API - Swagger UI</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@3.52.5/swagger-ui.css" />
        <style>
            html { box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }
            *, *:before, *:after { box-sizing: inherit; }
            body { margin:0; background: #fafafa; }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@3.52.5/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@3.52.5/swagger-ui-standalone-preset.js"></script>
        <script>
        window.onload = function() {
          SwaggerUIBundle({
            url: '/api/v1/openapi.json',
            dom_id: '#swagger-ui',
            deepLinking: true,
            presets: [
              SwaggerUIBundle.presets.apis,
              SwaggerUIStandalonePreset
            ],
            plugins: [
              SwaggerUIBundle.plugins.DownloadUrl
            ],
            layout: "StandaloneLayout"
          });
        };
        </script>
    </body>
    </html>
    """

# Error handlers
@app.error(404)
def error404(error):
    """Handle 404 errors"""
    set_json_headers()
    response.status = 404
    return create_error_response("NOT_FOUND", "The requested resource was not found")

@app.error(405)
def error405(error):
    """Handle 405 Method Not Allowed errors"""
    set_json_headers()
    response.status = 405
    return create_error_response("METHOD_NOT_ALLOWED", "The requested method is not allowed for this resource")

@app.error(500)
def error500(error):
    """Handle 500 Internal Server Error"""
    set_json_headers()
    response.status = 500
    return create_error_response("INTERNAL_ERROR", "An internal server error occurred")

# Run app
if __name__ == "__main__":
    if os.environ.get('APP_LOCATION') == 'heroku':
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    else:
        app.run(host='localhost', port=8080, debug=True)
