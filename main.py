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
            "message": message
        },
        "meta": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": API_VERSION
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

# Web Application
@app.get('/')
def element_words_app():
    """Element Words Web Application"""
    response.content_type = "text/html; charset=UTF-8"
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Element Words</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                padding: 40px;
                max-width: 800px;
                width: 100%;
            }
            
            h1 {
                text-align: center;
                color: #2d3748;
                margin-bottom: 10px;
                font-size: 2.5rem;
                font-weight: 700;
            }
            
            .subtitle {
                text-align: center;
                color: #718096;
                margin-bottom: 40px;
                font-size: 1.1rem;
            }
            
            .input-section {
                margin-bottom: 30px;
            }
            
            .input-group {
                display: flex;
                gap: 10px;
                margin-bottom: 15px;
                flex-wrap: wrap;
            }
            
            #wordInput {
                flex: 1;
                min-width: 250px;
                padding: 15px 20px;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                font-size: 1.1rem;
                transition: border-color 0.2s ease;
            }
            
            #wordInput:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            .btn {
                padding: 15px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 1.1rem;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s ease, box-shadow 0.2s ease;
            }
            
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
            }
            
            .btn:active {
                transform: translateY(0);
            }
            
            .btn:disabled {
                opacity: 0.6;
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }
            
            .checkbox-group {
                display: flex;
                align-items: center;
                gap: 10px;
                color: #4a5568;
            }
            
            .checkbox-group input[type="checkbox"] {
                width: 18px;
                height: 18px;
                accent-color: #667eea;
            }
            
            .loading {
                text-align: center;
                color: #718096;
                margin: 20px 0;
                font-size: 1.1rem;
            }
            
            .error {
                background: #fed7d7;
                color: #c53030;
                padding: 15px 20px;
                border-radius: 12px;
                margin: 20px 0;
                border-left: 4px solid #c53030;
            }
            
            .no-results {
                text-align: center;
                color: #718096;
                margin: 30px 0;
                font-size: 1.1rem;
            }
            
            .results {
                margin-top: 30px;
            }
            
            .solution {
                background: #f7fafc;
                border-radius: 16px;
                padding: 25px;
                margin-bottom: 20px;
                border-left: 4px solid #667eea;
                transition: transform 0.2s ease;
            }
            
            .solution:hover {
                transform: translateY(-2px);
                box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            }
            
            .solution-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 15px;
            }
            
            .solution-title {
                font-size: 1.2rem;
                font-weight: 600;
                color: #2d3748;
            }
            
            .element-count {
                background: #667eea;
                color: white;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 0.9rem;
                font-weight: 500;
            }
            
            .elements-container {
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
            }
            
            .element-tile {
                background: white;
                border: 2px solid #e2e8f0;
                border-radius: 12px;
                padding: 15px;
                min-width: 60px;
                text-align: center;
                position: relative;
                transition: all 0.2s ease;
                cursor: pointer;
            }
            
            .element-tile:hover {
                border-color: #667eea;
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            
            .element-tile.reversed {
                border-color: #ed8936;
                background: #fef5e7;
            }
            
            .element-tile.reversed:hover {
                border-color: #dd6b20;
            }
            
            .element-symbol {
                font-size: 1.4rem;
                font-weight: 700;
                color: #2d3748;
                margin-bottom: 4px;
            }
            
            .element-name {
                font-size: 0.8rem;
                color: #718096;
                font-weight: 500;
            }
            
            .element-number {
                position: absolute;
                top: 2px;
                right: 4px;
                font-size: 0.7rem;
                color: #a0aec0;
                font-weight: 500;
            }
            
            .reversed-indicator {
                position: absolute;
                top: 2px;
                left: 4px;
                width: 8px;
                height: 8px;
                background: #ed8936;
                border-radius: 50%;
            }
            
            .api-link {
                text-align: center;
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #e2e8f0;
            }
            
            .api-link a {
                color: #667eea;
                text-decoration: none;
                font-weight: 500;
            }
            
            .api-link a:hover {
                text-decoration: underline;
            }
            
            @media (max-width: 600px) {
                .container {
                    margin: 10px;
                    padding: 20px;
                }
                
                h1 {
                    font-size: 2rem;
                }
                
                .input-group {
                    flex-direction: column;
                }
                
                #wordInput {
                    min-width: 100%;
                }
                
                .solution-header {
                    flex-direction: column;
                    gap: 10px;
                    align-items: flex-start;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Element Words</h1>
            <p class="subtitle">Create words using chemical element symbols</p>
            
            <div class="input-section">
                <div class="input-group">
                    <input type="text" id="wordInput" placeholder="Enter a word (e.g., hero, water, science)" maxlength="50">
                    <button class="btn" onclick="searchWord()">Find Elements</button>
                </div>
                <div class="checkbox-group">
                    <input type="checkbox" id="allowReversed">
                    <label for="allowReversed">Allow reversed symbols (He + eH, Li + iL, etc.)</label>
                </div>
            </div>
            
            <div id="loading" class="loading" style="display: none;">
                Searching for element combinations...
            </div>
            
            <div id="error" class="error" style="display: none;"></div>
            
            <div id="noResults" class="no-results" style="display: none;">
                No element combinations found for this word. Try allowing reversed symbols or a different word.
            </div>
            
            <div id="results" class="results"></div>
            
            <div class="api-link">
                <a href="/api/v1/docs" target="_blank">View API Documentation</a>
            </div>
        </div>
        
        <script>
            const wordInput = document.getElementById('wordInput');
            const allowReversedCheckbox = document.getElementById('allowReversed');
            const loadingDiv = document.getElementById('loading');
            const errorDiv = document.getElementById('error');
            const noResultsDiv = document.getElementById('noResults');
            const resultsDiv = document.getElementById('results');
            
            // Allow Enter key to trigger search
            wordInput.addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    searchWord();
                }
            });
            
            // Clear results when input changes
            wordInput.addEventListener('input', function() {
                clearResults();
            });
            
            allowReversedCheckbox.addEventListener('change', function() {
                if (wordInput.value.trim()) {
                    searchWord();
                }
            });
            
            function clearResults() {
                loadingDiv.style.display = 'none';
                errorDiv.style.display = 'none';
                noResultsDiv.style.display = 'none';
                resultsDiv.innerHTML = '';
            }
            
            async function searchWord() {
                const word = wordInput.value.trim();
                if (!word) {
                    showError('Please enter a word');
                    return;
                }
                
                clearResults();
                loadingDiv.style.display = 'block';
                
                try {
                    const allowReversed = allowReversedCheckbox.checked;
                    const url = `/api/v1/words/${encodeURIComponent(word)}${allowReversed ? '?allow_reversed_symbols=true' : ''}`;
                    
                    const response = await fetch(url);
                    const data = await response.json();
                    
                    loadingDiv.style.display = 'none';
                    
                    if (!response.ok) {
                        showError(data.error?.message || 'An error occurred');
                        return;
                    }
                    
                    displayResults(data.data);
                } catch (error) {
                    loadingDiv.style.display = 'none';
                    showError('Network error. Please try again.');
                }
            }
            
            function showError(message) {
                errorDiv.textContent = message;
                errorDiv.style.display = 'block';
            }
            
            function displayResults(data) {
                if (!data.solutions || data.solutions.length === 0) {
                    noResultsDiv.style.display = 'block';
                    return;
                }
                
                const solutions = data.solutions;
                let html = '';
                
                solutions.forEach((solution, index) => {
                    const elementCount = solution.elements.length;
                    const elementCountText = elementCount === 1 ? '1 element' : `${elementCount} elements`;
                    
                    html += `
                        <div class="solution">
                            <div class="solution-header">
                                <div class="solution-title">${solution.representation}</div>
                                <div class="element-count">${elementCountText}</div>
                            </div>
                            <div class="elements-container">
                    `;
                    
                    solution.elements.forEach(element => {
                        const reversedClass = element.reversed ? ' reversed' : '';
                        const reversedIndicator = element.reversed ? '<div class="reversed-indicator"></div>' : '';
                        
                        html += `
                            <div class="element-tile${reversedClass}" title="${element.name} (${element.symbol})${element.reversed ? ' - Reversed symbol' : ''}">
                                <div class="element-number">${element.atomic_number}</div>
                                ${reversedIndicator}
                                <div class="element-symbol">${element.symbol}</div>
                                <div class="element-name">${element.name}</div>
                            </div>
                        `;
                    });
                    
                    html += `
                            </div>
                        </div>
                    `;
                });
                
                resultsDiv.innerHTML = html;
            }
            
            // Auto-focus input on page load
            window.addEventListener('load', function() {
                wordInput.focus();
            });
        </script>
    </body>
    </html>
    """

# API Documentation endpoint (moved to /api route)
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
                            <p><span class="method">GET</span> <span class="url">/api/v1/words/{word}</span></p>
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
                            <li><code>GET /api/v1/words/hero</code> → H-Er-O</li>
                <li><code>GET /api/v1/words/hero?allow_reversed_symbols=true</code> → Use both normal and reversed symbols (He+eH, etc.)</li>
        </ul>
        
        <h2>Response Format</h2>
        <pre>{
  "data": { ... },
  "meta": {
    "timestamp": "2025-07-01T00:00:00Z",
    "version": "v1"
  }
}</pre>
        
        <h2>Error Format</h2>
        <pre>{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable message"
  },
  "meta": {
    "timestamp": "2023-07-01T00:00:00Z",
    "version": "v1"
  }
}</pre>
        
        <p><a href="https://github.com/chriswilson1982/element-words">GitHub Repository</a></p>
        <p><a href="/">← Back to Element Words App</a></p>
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

# Health check endpoint
@app.get('/api/v1/health')
def health_check():
    """Health check endpoint"""
    set_json_headers()
    
    health_data = {
        "status": "healthy",
        "service": "Element Words API",
    }
    
    return create_success_response(health_data)

# Find word combinations
@app.get('/api/v1/words/<word>')
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
