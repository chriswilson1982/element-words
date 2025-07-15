# Add these endpoints to your main.py to serve the OpenAPI spec

import yaml
import json
import os

# Add these routes to your existing main.py

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